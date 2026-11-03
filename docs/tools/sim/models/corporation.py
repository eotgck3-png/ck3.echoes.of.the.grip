"""Corporation: Board Influence (eotg_corp_board_influence), yearly steps.

Reads: eotg_corporation_board_influence_next_value / _start_value / _inherit_value and
the CO2-CO5 values (common/script_values/eotg_corporation_values.txt); the yearly
results tick (common/story_cycles/eotg_corporation_story.txt); the decisions
(common/decisions/eotg_corporation_decisions.txt): Push Through a Restructuring (top),
Court the Board (vassals, with the merged once-a-year erosion cap read as written:
eotg_corp_board_eroded 1 year, and only while the CEO's influence is below the
director's projected value, eotg_corporation_court_projected_value); the board
election's elector_vote_strength (common/succession_election/eotg_government_elections.txt).
"""
import numpy as np
from pdx_read import Ctx
from common import World, trait_ctx, annual_take, TIER_KEY, assume
from models.gov_common import change, start_values, inherit, election

V = 'eotg_corporation_board_influence_value'
LIEGE_DISLIKES = assume('corp_liege_dislikes_director', 0.25, 'share of directors whose CEO opinion of them is below 0')
COUNCILLOR = assume('corp_director_is_powerful_or_councillor', 0.5, 'chance a director qualifies as an elector beyond the top 6 by tier')


def run(R, size, policy, runs, years, seed):
    rng = np.random.default_rng(seed)
    w = World(rng, runs, size)
    nv = w.nv
    chg = lambda cur, amt: change(R, 'eotg_corporation_board_influence_next_value', V, 'eotg_corporation_board_amount', cur, amt)
    top = start_values(R, 'eotg_corporation_board_influence_start_value', 'eotg_corporation_role_top', runs, True)
    vas = start_values(R, 'eotg_corporation_board_influence_start_value', 'eotg_corporation_role_top', (runs, nv), False)
    gain = R.num('eotg_corporation_results_gain_value'); debt = R.num('eotg_corporation_debt_loss_value')
    rcost = R.num('eotg_corporation_restructure_cost_value'); rspend = R.num('eotg_corporation_restructure_spend_value')
    cgain = R.num('eotg_corporation_court_gain_value'); cero = R.num('eotg_corporation_court_erosion_value')
    D_res = R.decision('eotg_decision_corporation_restructure')
    D_court = R.decision('eotg_decision_corporation_court_board')
    cd_res = np.zeros(runs); cd_court = np.zeros((runs, nv))
    hist = np.zeros((runs, years)); vhist = np.zeros((runs, years))
    erosions = np.zeros(runs); courts = 0; restructures = 0
    elections = []
    for y in range(years):
        w.step_war(); w.step_gold()
        # yearly results tick (first_valid: debt, then solvent at peace)
        top = np.where(w.top_gold < 0, chg(top, debt), np.where((w.top_gold > 0) & ~w.at_war, chg(top, gain), top))
        vas = np.where(w.v_gold < 0, chg(vas, debt), np.where((w.v_gold > 0) & ~w.at_war[:, None], chg(vas, gain), vas))
        # Restructure (top sink; the greedy policy keeps its resource)
        if policy == 'ai':
            ctx = Ctx({V: top, 'gold': w.top_gold, 'tier': w.top_tier, 'trig:eotg_corporation_role_top': True,
                       **trait_ctx(w.top_traits)})
            ok = (top >= rcost) & (cd_res <= 0)
            rs = ok & annual_take(R, D_res, ctx, TIER_KEY[w.top_tier], rng, (runs,))
            top = np.where(rs, chg(top, rspend), top)
            cd_res = np.where(rs, D_res['cooldown_years'], cd_res - 1)
            restructures += int(rs.sum())
        # Court the Board, vassal by vassal; erosion at most once a year per CEO
        eroded = np.zeros(runs, bool)
        for j in range(nv):
            vt = int(w.vtiers[j])
            dislikes = rng.random(runs) < LIEGE_DISLIKES
            liege = Ctx(scopes={'opinion': Ctx({'target': 0.0, 'root': 0.0, 'value': np.where(dislikes, -10.0, 10.0)})})
            cv = Ctx({V: vas[:, j], 'gold': w.v_gold[:, j], 'tier': vt, 'trig:eotg_corporation_role_vassal': True,
                      **trait_ctx(w.v_traits, j)}, scopes={'liege': liege})
            cost = R.cost_value(D_court, 'gold', cv)
            ok = (cd_court[:, j] <= 0) & (w.v_gold[:, j] >= cost)
            ct = ok if policy == 'greedy_all' else ok & annual_take(R, D_court, cv, TIER_KEY[vt], rng, (runs,))
            projected = np.asarray(R.num('eotg_corporation_court_projected_value', Ctx({V: vas[:, j]})), float)
            erode = ct & ~eroded & (top < projected)
            vas[:, j] = np.where(ct, chg(vas[:, j], cgain), vas[:, j])
            w.v_gold[:, j] -= np.where(ct, cost, 0)
            top = np.where(erode, chg(top, cero), top)
            eroded |= erode
            erosions += erode
            cd_court[:, j] = np.where(ct, D_court['cooldown_years'], cd_court[:, j] - 1)
            courts += int(ct.sum())
        # deaths: the board election, then the heir inherits half
        dead = w.deaths(runs)
        if dead.any():
            idx = np.where(dead)[0]
            k = min(nv, 6)
            order = np.argsort(-w.vtiers)[:k]
            powerful = np.concatenate([np.zeros((len(idx), 1), bool), rng.random((len(idx), k)) < COUNCILLOR], axis=1)
            e = election(R, rng, 'eotg_corporation_elective', top[idx], vas[idx][:, order],
                         np.concatenate([[w.top_tier], w.vtiers[order]]), powerful, V)
            e['n'] = len(idx); elections.append(e)
        top = np.where(dead, inherit(R, 'eotg_corporation_board_influence_inherit_value', 'eotg_corp_board_influence', V,
                                     'eotg_corporation_predecessor', top, np.zeros(runs)), top)
        vdead = w.deaths((runs, nv))
        vas = np.where(vdead, inherit(R, 'eotg_corporation_board_influence_inherit_value', 'eotg_corp_board_influence', V,
                                      'eotg_corporation_predecessor', vas, np.zeros((runs, nv))), vas)
        hist[:, y] = top; vhist[:, y] = vas.mean(axis=1)
    return {'top': hist, 'vassal_mean': vhist, 'elections': _merge(elections),
            'counts': {'court_per_vassal_year': courts / (runs * years * nv),
                       'erosion_per_run_year': float(erosions.mean() / years),
                       'restructure_per_run_year': restructures / (runs * years)}}


def _merge(es):
    if not es:
        return {}
    n = sum(e['n'] for e in es)
    out = {'elections': n}
    for k in ('leader_pick_wins', 'non_dynast_wins_without_rule', 'leader_pick_wins_without_rule'):
        out[k] = sum(e[k] * e['n'] for e in es) / n
    return out
