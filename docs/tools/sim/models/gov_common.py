"""Helpers shared by the three scripted-resource government models (PMC, Corporation,
Trade Oligarchy): the single-writer change effect, init, inheritance, and the
election machinery (the elector_vote_strength block read from the script)."""
import numpy as np
from pdx_read import Ctx
from common import assume


def change(R, next_value, value_name, amount_scope, cur, amount):
    """Apply the government's change effect: set var = <gov>_next_value, which reads
    the current value and scope:<amount>, clamped (the script's own formula)."""
    ctx = Ctx({value_name: cur, 'scope:' + amount_scope: amount})
    return np.asarray(R.num(next_value, ctx), float) * np.ones_like(cur, dtype=float)


def start_values(R, start_name, role_top_name, n_shape, is_top):
    """<gov>_start_value: reads the role-top trigger (40/20 or 50/20)."""
    ctx = Ctx({'trig:' + role_top_name: is_top})
    return np.asarray(R.num(start_name, ctx), float) * np.ones(n_shape)


def inherit(R, inherit_name, var_name, value_name, pred_scope, dead_value, heir_value):
    """<gov>_inherit_value in the heir's scope: max(0, factor * predecessor - own)."""
    ctx = Ctx({'scope:%s.var:%s' % (pred_scope, var_name): dead_value, value_name: heir_value})
    return np.asarray(R.num(inherit_name, ctx), float)


ELECT_ASSUME = assume('election_model', {
    'dynasty_candidates': 3,
    'candidate_skill': 'N(12, 4) stewardship+diplomacy, scored by each election\'s own skill value',
    'self_vote': 'an elector who is a candidate votes for themself (vanilla elector_self_voting_pattern)',
    'holder_pattern': 'the holder backs the dynasty candidate with the best skill',
    'elector_noise': 'N(0, 15) per elector and candidate on the candidate score',
    'non_dynasty_candidates_without_rule': 'every landed vassal elector of the same government',
}, 'vanilla voting patterns are scripted modifiers this session cannot read; this is a proxy')


def vote_strength(R, election_key, ctx):
    """Evaluate <election>.elector_vote_strength (base + modifiers) from the script."""
    node = R.node(election_key)
    vs = [c for c in node.children if c.key == 'elector_vote_strength'][0]
    d = {'ai_will_do': vs}
    return R.ai_will_do(d, ctx)


def run_election(rng, strengths, elector_is_candidate_mask, n_dyn, skill_dyn, skill_el,
                 holder_index, el_resource):
    """One election per run, vectorised over runs.
    strengths: (runs, E) vote strength per elector; elector 0 is the holder.
    Candidates: n_dyn dynasty members (+ the electors flagged in elector_is_candidate_mask
    when the dynasty rule is absent). Returns (winner_is_dynasty, winner_is_resource_leader_pick).
    """
    runs, E = strengths.shape
    cand_skill = np.concatenate([skill_dyn, np.where(elector_is_candidate_mask, skill_el, -1e9)], axis=1)
    C = cand_skill.shape[1]
    best_dyn = np.argmax(skill_dyn, axis=1)
    votes = np.zeros((runs, C))
    picks = np.zeros((runs, E), int)
    for e in range(E):
        score = cand_skill + rng.normal(0, 15, (runs, C))
        # self-vote
        if e > 0:
            selfc = n_dyn + e
            score[:, selfc] = np.where(elector_is_candidate_mask[:, e], 1e9, score[:, selfc])
        if e == holder_index:
            score = np.full((runs, C), -1e9)
            score[np.arange(runs), best_dyn] = 1.0
        pick = np.argmax(score, axis=1)
        picks[:, e] = pick
        votes[np.arange(runs), pick] += strengths[:, e]
    winner = np.argmax(votes, axis=1)
    # the resource leader: the elector with the highest resource; did their pick win?
    leader = np.argmax(el_resource, axis=1)
    leader_pick = picks[np.arange(runs), leader]
    return winner < n_dyn, leader_pick == winner


class ScopeCtx(Ctx):
    """A Ctx whose sub-scopes are given as a dict of Ctx (e.g. {'liege': ..., 'opinion': ...})."""
    pass


def election(R, rng, key, holder_res, el_res, el_tier, powerful, value_name, n_dyn=3):
    """Run one board/charter election per run with and without the dynasty rule.
    holder_res: (runs,) the dying holder's resource; el_res: (runs, E-1) the electors'.
    Returns dict of rates."""
    runs = holder_res.shape[0]
    res = np.concatenate([holder_res[:, None], el_res], axis=1)
    tiers = np.concatenate([np.full((runs, 1), el_tier[0]), el_tier[1:][None, :].repeat(runs, 0)], axis=1)
    E = res.shape[1]
    strengths = np.zeros((runs, E))
    for e in range(E):
        ctx = Ctx({'this': float(e), 'scope:holder': 0.0, 'liege': (-1.0 if e == 0 else 0.0),
                   value_name: res[:, e], 'highest_held_title_tier': float(tiers[0, e]),
                   'is_powerful_vassal': (powerful[:, e] if e else False)})
        strengths[:, e] = np.asarray(vote_strength(R, key, ctx), float) * np.ones(runs)
    skill_dyn = rng.normal(12, 4, (runs, n_dyn))
    skill_el = rng.normal(12, 4, (runs, E))
    with_rule = run_election(rng, strengths, np.zeros((runs, E), bool), n_dyn, skill_dyn, skill_el, 0, res)
    cand = np.ones((runs, E), bool); cand[:, 0] = False
    no_rule = run_election(rng, strengths, cand, n_dyn, skill_dyn, skill_el, 0, res)
    return {'leader_pick_wins': float(with_rule[1].mean()),
            'non_dynast_wins_without_rule': float(1 - no_rule[0].mean()),
            'leader_pick_wins_without_rule': float(no_rule[1].mean()),
            'mean_strength_by_resource_quartile': [float(strengths[:, 1:][np.digitize(res[:, 1:], [25, 50, 75]) == q].mean()) if np.any(np.digitize(res[:, 1:], [25, 50, 75]) == q) else None for q in range(4)]}
