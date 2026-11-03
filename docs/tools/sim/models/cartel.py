"""Cartel: dread (engine), the scaled baseline and the payment-schedule lifecycle.

Reads:
- dread decay/gain multipliers: eotg_cartel_government character_modifier
  (common/governments/eotg_cartel_government.txt);
- the baseline: eotg_cartel_refresh_schedule_effect's set_variable value
  (common/scripted_effects/eotg_cartel_effects.txt), shown by eotg_cartel_schedule_modifier;
- demand: eotg_cartel_put_on_schedule_interaction (ai_frequency_by_tier, ai_will_do,
  ai_accept; common/character_interactions/eotg_cartel_interactions.txt) and
  eotg_cartel_schedule_cost_value (common/script_values/eotg_cartel_values.txt);
- enforcement: eotg_decision_cartel_tighten_schedule; vassal source: _lean_on_locals
  (common/decisions/eotg_cartel_decisions.txt), amounts read from their change calls;
- default: the walk-off, eotg_story_cartel_schedule yearly effect_group trigger
  (common/story_cycles/eotg_cartel_story.txt), and the succession grace years
  (eotg_cartel_on_death, common/on_action/eotg_cartel_on_actions.txt);
- Kingpin rarity: eotg_on_yearly_aug_kingpin_check random_list
  (common/on_action/eotg_aug_kingpin_on_actions.txt).
Dread: monthly steps; decisions and the interaction: yearly attempts.
"""
import numpy as np
from pdx_read import Ctx, VANILLA_DEFAULTS, per_check_to_annual
from common import World, trait_ctx, annual_take, TIER_KEY, assume

DREAD_MONTHLY = assume('DREAD_MONTHLY_CHANGE', 0.5, 'cited: 00_defines.txt:122 (Cartel spec §2.4)')
MAX_DREAD = assume('MAX_DREAD', 100, 'cited: 00_defines.txt:120')
N_TARGETS = assume('cartel_independent_neighbours', 6, 'independent neighbouring rulers that can be put on the schedule')
TARGET_TIERS = assume('cartel_target_tier_mix', {2: 0.5, 3: 0.35, 4: 0.15}, 'neighbour highest-tier mix')
INTIM = assume('dread_level_thresholds', (40, 80), 'has_dread_level_towards level 1 at dread>=40, level 2 at >=80 (engine; boldness-relative in vanilla)')
CEASE = assume('payer_cease_paying_per_year', {1: 0.03, 2: 0.08}, 'vanilla cease_paying_tribute by a low/high-tax payer')
HEIR_DREAD = assume('heir_starting_dread', 0.0, 'dread is personal; the heir starts with none')
KP_DREAD = assume('kingpin_chain_dread', 20.0, 'net dread from a kingpin chain (beats +5..+30, spec I2d §7.2)')
VANILLA_DREAD = assume('vanilla_dread_income', (0.6, 12.0), 'dread from vanilla acts (executions, imprisonments, murders): Poisson 0.6 acts a year x +12 before the gain multiplier; the AI Cartel with none sits at 0')
NO_RIVALS = assume('cartel_target_rivalry', 'none', 'no target is a rival or nemesis of the actor in ai_accept')
OPINION_SD = assume('recipient_opinion_sd', 15.0, 'opinion of the actor ~ N(0, 15) in ai_accept')


def _govmod(R, key):
    n = R.node('eotg_cartel_government')
    cm = [c for c in n.children if c.key == 'character_modifier'][0]
    return float([c for c in cm.children if c.key == key][0].value)


def run(R, size, policy, runs, years, seed):
    rng = np.random.default_rng(seed)
    w = World(rng, runs, size)
    nv = w.nv
    decay = DREAD_MONTHLY * (1 + _govmod(R, 'dread_decay_mult'))
    gain_mult = 1 + _govmod(R, 'dread_gain_mult')
    refresh = R.node('eotg_cartel_refresh_schedule_effect')
    base_node = [c for c in R.find_deep(refresh, 'value') if c.is_block][0]
    D_t = R.decision('eotg_decision_cartel_tighten_schedule')
    D_l = R.decision('eotg_decision_cartel_lean_on_locals')
    lean_calls = R.change_calls(R.node('eotg_decision_cartel_lean_on_locals'), 'eotg_cartel_change_dread_effect')
    lean_own = R.resolve(lean_calls[0][1], Ctx()); lean_liege = R.resolve(lean_calls[1][1], Ctx())
    inter = R.node('eotg_cartel_put_on_schedule_interaction')
    freq = {c.key: float(c.value) for c in [x for x in inter.children if x.key == 'ai_frequency_by_tier'][0].children}
    ai_do = {'ai_will_do': [x for x in inter.children if x.key == 'ai_will_do'][0]}
    ai_acc = {'ai_will_do': [x for x in inter.children if x.key == 'ai_accept'][0]}
    story = R.effect_group_intervals('eotg_story_cartel_schedule')
    walk_trig = [c for c in [g for y, g in story if y and y >= 1][0].children if c.key == 'trigger'][0]
    grace_years = float([c for c in R.find_deep(R.node('eotg_cartel_on_death'), 'years')][0].value)
    grace_years = R.overrides.get('eotg_cartel_on_death.years', grace_years)   # what-if hook
    low_dread = VANILLA_DEFAULTS['low_dread'][0]
    tiers_c = {'tier_county': 2.0, 'tier_duchy': 3.0, 'tier_kingdom': 4.0, 'tier_empire': 5.0}

    dread = np.zeros(runs); vdread = np.zeros((runs, nv))
    tgt_tier = rng.choice(list(TARGET_TIERS), size=(runs, N_TARGETS), p=list(TARGET_TIERS.values()))
    payer = np.zeros((runs, N_TARGETS), int)       # 0 none, 1 low tax, 2 high tax
    blocked = np.zeros((runs, N_TARGETS))          # refusal cooldown (years)
    grace = np.zeros(runs); cd_t = np.zeros(runs); cd_l = np.zeros((runs, nv))
    hist = np.zeros((runs, years)); phist = np.zeros((runs, years))
    walkoffs = 0; accepts = 0; refusals = 0; tightens = 0; leans = 0
    post_succ_walks = 0; post_succ_walks10 = 0; successions_with_payers = 0  # walk-offs within 5 years of a succession
    since_succ = np.full(runs, 99.0); payers_at_succ = np.zeros(runs)
    for y in range(years):
        w.step_war(); w.step_gold()
        npay = (payer > 0).sum(axis=1).astype(float)
        base = np.asarray(R.eval_value(base_node, Ctx({'eotg_cartel_payer_count_value': npay})), float) * np.ones(runs)
        acts = rng.poisson(VANILLA_DREAD[0], runs)
        dread = np.minimum(MAX_DREAD, dread + acts * VANILLA_DREAD[1] * gain_mult)
        for m in range(12):   # monthly drift toward the baseline
            dread = np.where(dread > base, np.maximum(base, dread - decay), np.minimum(base, dread + decay))
            vdread = np.maximum(0, vdread - decay)
        # Lean on the Locals (vassals)
        for j in range(nv):
            vt = int(w.vtiers[j])
            cv = Ctx({'dread': vdread[:, j], 'low_dread': low_dread, 'is_at_war': w.v_at_war[:, j],
                      'trig:eotg_cartel_role_vassal': True, **trait_ctx(w.v_traits, j)})
            ok = (~w.v_at_war[:, j]) & (cd_l[:, j] <= 0)
            ln = ok if policy == 'greedy_all' else ok & annual_take(R, D_l, cv, TIER_KEY[vt], rng, (runs,))
            vdread[:, j] = np.where(ln, np.minimum(MAX_DREAD, vdread[:, j] + lean_own * gain_mult), vdread[:, j])
            dread = np.where(ln, np.minimum(MAX_DREAD, dread + lean_liege * gain_mult), dread)
            cd_l[:, j] = np.where(ln, D_l['cooldown_years'], cd_l[:, j] - 1)
            leans += int(ln.sum())
        # Put on the Schedule: one attempt per ai_frequency period
        free = (payer == 0) & (blocked <= 0)
        has_free = free.any(axis=1)
        choice = np.argmax(free * rng.random((runs, N_TARGETS)), axis=1)
        rt = tgt_tier[np.arange(runs), choice].astype(float)
        compel = (dread >= VANILLA_DEFAULTS['high_dread'][0]).astype(float)
        cctx = Ctx({'scope:recipient.highest_held_title_tier': rt, 'scope:eotg_cartel_compel': compel, **tiers_c})
        cost = np.asarray(R.num('eotg_cartel_schedule_cost_value', cctx), float) * np.ones(runs)
        afford = dread >= cost
        if policy in ('greedy', 'greedy_all'):
            attempt = has_free & (dread >= cost + low_dread)
        else:
            rg = rng.normal(INCOME_GOLD := 100, 50, runs)
            actx = Ctx({'scope:recipient.gold': rg, 'scope:actor.dread': dread, 'high_dread': VANILLA_DEFAULTS['high_dread'][0],
                        'low_dread': low_dread, 'scope:recipient.tier_difference(scope:actor)': rt - w.top_tier,
                        'scope:actor.realm_size': float(nv + 1) * 3, 'scope:recipient.realm_size': (rt - 1) * 3,
                        **cctx.values})
            pct = np.asarray(R.ai_will_do(ai_do, actx), float) * np.ones(runs)
            interval = freq.get(TIER_KEY[w.top_tier], 12)
            attempt = has_free & afford & (rng.random(runs) < per_check_to_annual(pct, interval))
        lvl = np.where(dread >= INTIM[1], 2.0, np.where(dread >= INTIM[0], 1.0, 0.0))
        rec = Ctx({'level': lvl, 'target': 0.0, 'scope:actor': 0.0})
        acc_ctx = Ctx({'ai_boldness': rng.normal(0, 30, runs), 'ai_greed': rng.normal(0, 30, runs),
                       'scope:actor.highest_held_title_tier': float(w.top_tier)},
                      scopes={'scope:recipient': Ctx({'is_confederation_member': False, 'has_relation_rival': -1.0,
                                                      'has_relation_nemesis': -1.0, 'scope:actor': 0.0,
                                                      'highest_held_title_tier': rt,
                                                      'scope:actor.highest_held_title_tier': float(w.top_tier)},
                                                     scopes={'has_dread_level_towards': rec}),
                              'has_dread_level_towards': rec})
        acc_ctx.values['scope:recipient.highest_held_title_tier'] = rt
        score = np.asarray(R.ai_will_do(ai_acc, acc_ctx), float) + rng.normal(0, OPINION_SD, runs)
        accept = attempt & ((compel > 0) | (score > 0))
        refuse = attempt & ~accept
        dread = np.where(accept, np.maximum(0, dread - cost), dread)
        dread = np.where(refuse, np.maximum(0, dread + VANILLA_DEFAULTS['miniscule_dread_loss'][0]), dread)
        payer[np.arange(runs), choice] = np.where(accept, 1, payer[np.arange(runs), choice])
        blocked[np.arange(runs), choice] = np.where(refuse, 3, blocked[np.arange(runs), choice])
        accepts += int(accept.sum()); refusals += int(refuse.sum())
        # Tighten the Schedule (top, AI only: a dread sink)
        low = (payer == 1).sum(axis=1).astype(float)
        tctx = Ctx({'eotg_cartel_low_payer_count_value': low, 'dread': dread, 'low_dread': low_dread,
                    'medium_dread': VANILLA_DEFAULTS['medium_dread'][0], 'trig:eotg_cartel_role_top': True,
                    **trait_ctx(w.top_traits)})
        tcost = np.asarray(R.num('eotg_cartel_tighten_cost_value', tctx), float) * np.ones(runs)
        if policy == 'ai':
            okt = (low > 0) & (dread >= tcost) & (cd_t <= 0)
            tg = okt & annual_take(R, D_t, tctx, TIER_KEY[w.top_tier], rng, (runs,))
            dread = np.where(tg, dread - tcost, dread)
            payer = np.where(tg[:, None] & (payer == 1), 2, payer)
            cd_t = np.where(tg, D_t['cooldown_years'], cd_t - 1)
            tightens += int(tg.sum())
        # vanilla cease paying
        cease = ((payer == 1) & (rng.random(payer.shape) < CEASE[1])) | ((payer == 2) & (rng.random(payer.shape) < CEASE[2]))
        payer = np.where(cease, 0, payer)
        # walk-off: the story's yearly trigger, read from the script
        npay = (payer > 0).sum(axis=1).astype(float)
        owner = Ctx({'trig:eotg_cartel_role_top': True, 'eotg_cartel_payer_count_value': npay, 'dread': dread,
                     'low_dread': low_dread, 'has_variable:eotg_cartel_succession_grace': grace > 0})
        walk = np.asarray(R.eval_trigger(walk_trig.children, Ctx(scopes={'story_owner': owner})), bool) * np.ones(runs, bool)
        # the walker: the lowest-opinion payer ~ a random payer
        wk = np.argmax((payer > 0) * rng.random(payer.shape), axis=1)
        payer[np.arange(runs), wk] = np.where(walk, 0, payer[np.arange(runs), wk])
        walkoffs += int(walk.sum())
        since_succ += 1
        post_succ_walks += int(((since_succ <= 5) & walk & (payers_at_succ > 0)).sum())
        # H2a fix 3: the 5-year window equals a 5-year grace, so P5 reads 0 by
        # construction; the 10-year window shows what the longer grace really buys.
        post_succ_walks10 += int(((since_succ <= 10) & walk & (payers_at_succ > 0)).sum())
        # succession
        dead = w.deaths(runs)
        successions_with_payers += int((dead & (npay > 0)).sum())
        payers_at_succ = np.where(dead, npay, payers_at_succ)
        since_succ = np.where(dead, 0, since_succ)
        grace = np.where(dead & (npay > 0), grace_years, grace - 1)
        dread = np.where(dead, HEIR_DREAD, dread)
        blocked -= 1
        hist[:, y] = dread; phist[:, y] = (payer > 0).sum(axis=1)
    return {'top': hist, 'payers': phist,
            'counts': {'accept_per_run_year': accepts / (runs * years), 'refusal_per_run_year': refusals / (runs * years),
                       'walkoff_per_run_year': walkoffs / (runs * years), 'tighten_per_run_year': tightens / (runs * years),
                       'lean_per_vassal_year': leans / (runs * years * nv)},
            'succession': {'walkoffs_within_5y_per_succession': post_succ_walks / max(1, successions_with_payers),
                           'walkoffs_within_10y_per_succession': post_succ_walks10 / max(1, successions_with_payers)},
            'derived': {'monthly_decay': decay, 'gain_mult': gain_mult, 'grace_years': grace_years}}


def kingpin_rates(R):
    """Yearly kingpin-chain start chance from the on_action random_list, for an AI
    augmented ruler, Cartel vs not (other modifiers off)."""
    n = R.node('eotg_on_yearly_aug_kingpin_check')
    rl = R.find_deep(n, 'random_list')[0]
    entries = R.random_list_entries(rl)
    out = {}
    for cartel in (False, True):
        for ai in (True, False):
            ctx = Ctx({'trig:eotg_aug_has_patron': False, 'trig:eotg_is_augmented_any': True,
                       'trig:eotg_aug_under_policy': False, 'has_character_modifier:eotg_mod_illegal_implants': False,
                       'is_ai': ai, 'government_has_flag': 1.0 if cartel else 0.0, 'eotg_government_is_cartel': 1.0},
                      scopes={'any_courtier': Ctx({'trig:eotg_is_augmented_any': False}),
                              'any_vassal': Ctx({'trig:eotg_is_augmented_any': False})})
            ws = [float(R.weight(b, m, ctx)) for b, m, _ in entries]
            out[('cartel' if cartel else 'other') + ('_ai' if ai else '_player')] = ws[0] / sum(ws)
    return out
