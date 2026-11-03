"""Cybernetics: the tier ladder for one augmented ruler, yearly steps.

Reads:
- settling minimum: eotg_aug_initiate_effect add_character_flag eotg_flag_aug_settling
  years (common/scripted_effects/eotg_augmentation_effects.txt);
- progression: eotg_decision_aug_pursue_next_stage (cooldown, interval, ai_potential,
  ai_will_do; common/decisions/eotg_augmentation_decisions.txt); dev gates
  eotg_aug_dev_gate_enhanced / _overclocked (common/script_values/eotg_augmentation_values.txt);
- hidden risk at Overclocked: every eotg_add_fracture_risk call in
  eotg_on_yearly_aug_overclocked_check with its conditions
  (common/on_action/eotg_augmentation_on_actions.txt), incl. eotg_aug_oc_wear_relief_value;
- the cascade: eotg_neurofracture_threshold_met (common/scripted_triggers/eotg_augmentation_triggers.txt)
  -> eotg_trigger_neurofracture (risk reset to 0);
- Neurofractured drift: eotg_aug_nf_drift_value; terminal at the >= 95 test in
  eotg_on_yearly_aug_neurofractured_check;
- the terminal event eotg_fracture.027 (events/eotg_augmentation_fracture.txt): each
  option's ai_chance and its random_list outcomes (death / Seamless / survive).
"""
import numpy as np
from pdx_read import Ctx
from common import World, trait_ctx, annual_take, TIER_KEY, assume, MORTALITY

DEV_CDF = assume('capital_dev_share_at_least', {10: 0.486, 20: 0.163, 35: 0.013},
                 'cited: balance spec §5.1 (vanilla history titles, n = 4,288); log-linear between points')
FOLLOW = assume('pursue_event_follow_through', 0.9, 'the sought event: decline options carry factor 0.1 (balance §5.1 item 3)')
UNSOUGHT = assume('unsolicited_upgrade_per_year', 0.03, 'the random Upgrade branches in the tier pools (weights 30 / 25)')
AFFORD = assume('upgrade_affordable_share', 0.7, 'eotg_aug_can_afford_upgrade / gold >= major_gold_value when the AI wants it')
STRESS = assume('stress_level_dist', {0: 0.35, 1: 0.35, 2: 0.2, 3: 0.1}, 'Overclocked and later (stress_gain_mult +0.4); resampled with 70% persistence')
FLAGS = assume('vendor_flag_shares', {'eotg_flag_aug_hidden_flaw': 0.15, 'eotg_flag_aug_vendor_bold': 0.10,
                                      'eotg_flag_aug_vendor_safe': 0.10}, 'install vendor outcomes')
CALM = assume('event_option_risk_relief_per_year', -2.0, 'calm options in the Overclocked / NF pools, averaged')
SURVIVE_RISK = assume('terminal_survivor_risk_reset', 60.0, 'a non-fatal, non-Seamless terminal outcome leaves risk at 60 (fracture.029 sets 60)')
DEV_GROWTH = assume('capital_dev_growth_per_year', 0.1, 'vanilla development growth of a capital, about +1 a decade')
TECH = assume('implant_technician_employed', False, 'no Implant Technician court position (wear relief reads it)')
PHYS = assume('physician_access', 0.5, 'eotg_has_physician_access at the terminal')


def _dev_share(x):
    xs = sorted(DEV_CDF); ys = [np.log(DEV_CDF[k]) for k in xs]
    return float(np.exp(np.interp(x, xs, ys)))


def _terminal(R):
    ev = R.node('eotg_fracture.027')
    opts = []
    for o in [c for c in ev.children if c.key == 'option']:
        ai = [c for c in o.children if c.key == 'ai_chance']
        rls = R.find_deep(o, 'random_list')
        if not rls:
            continue
        outs = []
        for base, mods, body in R.random_list_entries(rls[0]):
            keys = {n.key for n, _ in __import__('pdx_parse').walk(body)}
            kind = 'death' if 'eotg_aug_cascade_death_effect' in keys else ('seamless' if 'eotg_aug_total_integration_effect' in keys else 'survive')
            outs.append((base, mods, kind))
        opts.append(({'ai_will_do': ai[0]} if ai else None, outs))
    return opts


def run(R, size, policy, runs, years, seed):
    rng = np.random.default_rng(seed)
    w = World(rng, runs, size)
    tier_key = TIER_KEY[w.top_tier]
    settle_years = float(R.find_deep(R.node('eotg_aug_initiate_effect'), 'years')[0].value)
    D = R.decision('eotg_decision_aug_pursue_next_stage')
    gate2 = R.num('eotg_aug_dev_gate_enhanced'); gate3 = R.num('eotg_aug_dev_gate_overclocked')
    oc_calls = R.change_calls(R.node('eotg_on_yearly_aug_overclocked_check'), 'eotg_add_fracture_risk')
    terminal = _terminal(R)
    flags = {k: rng.random(runs) < p for k, p in FLAGS.items()}
    # capital development: sampled from the vanilla distribution (log-linear CDF), then grows
    u = rng.random(runs)
    xs = sorted(DEV_CDF); ys = np.log([DEV_CDF[k] for k in xs])
    dev = np.interp(np.log(np.clip(u, 1e-6, 1)), ys[::-1], np.array(xs, float)[::-1])
    dev = np.where(u > DEV_CDF[10], rng.uniform(0, 10, runs), dev)
    tier = np.ones(runs, int)            # 1, 2, 3 = OC, 4 = NF, 5 = Seamless, 0 = dead (natural), -1 = cascade death
    settle = np.full(runs, settle_years); cd = np.zeros(runs); risk = np.zeros(runs)
    stress = rng.choice(4, runs, p=list(STRESS.values()))
    t_reach = {2: np.full(runs, np.nan), 3: np.full(runs, np.nan), 4: np.full(runs, np.nan), 5: np.full(runs, np.nan)}
    death_tier = np.zeros(runs, int); dead_year = np.full(runs, np.nan)
    hist_risk = np.zeros((runs, years)); hist_tier = np.zeros((runs, years))
    for y in range(years):
        w.step_war(); w.step_gold()
        alive = tier > 0
        resamp = rng.random(runs) > 0.7
        stress = np.where(resamp, rng.choice(4, runs, p=list(STRESS.values())), stress)
        base = {**trait_ctx(w.top_traits), 'is_at_war': w.at_war, 'stress_level': stress.astype(float),
                'employs_court_position': -1.0, 'eotg_aug_implant_technician_court_position': 0.0,
                'trig:has_active_diarchy': False, 'has_active_diarchy': False,
                **{'has_character_flag:' + k: v for k, v in flags.items()}}
        # progression (tiers 1-2)
        can = alive & ((tier == 1) | (tier == 2)) & (settle <= 0) & (cd <= 0)
        dev = dev + DEV_GROWTH
        gate_ok = np.where(tier == 1, dev >= gate2, dev >= gate3) & (rng.random(runs) < AFFORD)
        ctx = Ctx({**base, 'trig:eotg_is_aug_tier1': tier == 1, 'trig:eotg_is_aug_tier2': tier == 2,
                   'trig:eotg_aug_pressure_flicker': False, 'tier': w.top_tier,
                   'short_term_gold': np.full(runs, 1e6), 'gold': np.full(runs, 1e6)})
        if policy in ('greedy', 'greedy_all'):
            seek = can & gate_ok
        else:
            seek = can & gate_ok & annual_take(R, D, ctx, tier_key, rng, (runs,))
        cd = np.where(seek, D['cooldown_years'], cd - 1)
        up = (seek & (rng.random(runs) < FOLLOW)) | (alive & ((tier == 1) | (tier == 2)) & (settle <= 0) & gate_ok & (rng.random(runs) < UNSOUGHT))
        tier = np.where(up, tier + 1, tier)
        settle = np.where(up, settle_years, settle - 1)
        for t in (2, 3):
            t_reach[t] = np.where(up & (tier == t) & np.isnan(t_reach[t]), y + 1, t_reach[t])
        # Overclocked accrual: the on_action's calls, each under its conditions
        oc = alive & (tier == 3)
        if oc.any():
            cctx = Ctx({**base, 'trig:eotg_is_aug_tier3': True})
            add = np.zeros(runs)
            for conds, amt, _ in oc_calls:
                c = True
                for cl in conds:
                    c = np.logical_and(c, R.eval_trigger(cl, cctx))
                a = R.resolve(amt, cctx)
                add = add + np.where(c, a, 0.0)
            risk = np.where(oc, np.maximum(0, risk + add + CALM), risk)
            thr = np.asarray(R.eval_trigger(R.node('eotg_neurofracture_threshold_met').children,
                                            Ctx({'trig:eotg_is_aug_tier3': True, 'has_variable:eotg_fracture_risk': True,
                                                 'var:eotg_fracture_risk': risk})), bool)
            cas = oc & thr
            tier = np.where(cas, 4, tier); risk = np.where(cas, 0, risk)
            t_reach[4] = np.where(cas & np.isnan(t_reach[4]), y + 1, t_reach[4])
        # Neurofractured drift and the terminal
        nf = alive & (tier == 4)
        if nf.any():
            dctx = Ctx({'stress_level': stress.astype(float), 'has_character_flag:eotg_flag_aug_sedated': False,
                        'has_character_flag:eotg_flag_aug_restrained': False, 'has_variable:eotg_aug_sedation_courses': False,
                        'var:eotg_aug_sedation_courses': 0.0})
            drift = np.asarray(R.num('eotg_aug_nf_drift_value', dctx), float) * np.ones(runs)
            risk = np.where(nf, risk + drift + CALM, risk)
            term = nf & (risk >= 95)
            if term.any():
                tctx = Ctx({**base, 'health': rng.normal(4, 1.5, runs), 'trig:eotg_has_physician_access': rng.random(runs) < PHYS,
                            'var:eotg_aug_voice': rng.integers(0, 6, runs).astype(float),
                            'has_character_flag:eotg_flag_aug_may_embrace': rng.random(runs) < 0.3})
                # the AI picks an option by ai_chance; the greedy player the best Seamless odds
                ow = [np.asarray(R.ai_will_do(a, tctx), float) * np.ones(runs) if a else np.ones(runs) for a, _ in terminal]
                outw = []
                for a, outs in terminal:
                    ws = [(R.weight(b, m, tctx) * np.ones(runs), k) for b, m, k in outs]
                    outw.append(ws)
                if policy in ('greedy', 'greedy_all'):
                    seam = [sum(wt for wt, k in ws if k == 'seamless') / sum(wt for wt, _ in ws) for ws in outw]
                    pick = np.argmax(np.stack(seam, 1), axis=1)
                else:
                    W = np.stack(ow, 1); cum = np.cumsum(W, 1)
                    pick = (cum < rng.random((runs, 1)) * cum[:, -1:]).sum(1)
                r = rng.random(runs); res = np.full(runs, 'survive', dtype=object)
                for oi, ws in enumerate(outw):
                    tot = sum(wt for wt, _ in ws); acc = np.zeros(runs)
                    for wt, k in ws:
                        hit = (pick == oi) & (r >= acc / tot) & (r < (acc + wt) / tot)
                        res = np.where(hit, k, res); acc = acc + wt
                died = term & (res == 'death'); seamless = term & (res == 'seamless')
                tier = np.where(died, -1, np.where(seamless, 5, tier))
                death_tier = np.where(died, 4, death_tier); dead_year = np.where(died, y + 1, dead_year)
                t_reach[5] = np.where(seamless & np.isnan(t_reach[5]), y + 1, t_reach[5])
                risk = np.where(term & (res == 'survive'), SURVIVE_RISK, risk)
        # natural death
        nat = (tier > 0) & (rng.random(runs) < MORTALITY)
        death_tier = np.where(nat, tier, death_tier); dead_year = np.where(nat, y + 1, dead_year)
        tier = np.where(nat, 0, tier)
        hist_risk[:, y] = risk; hist_tier[:, y] = tier
    end = {'natural_death': float(np.mean(tier == 0)), 'cascade_death': float(np.mean(tier == -1)),
           'seamless': float(np.mean(tier == 5)), 'alive_NF': float(np.mean(tier == 4)),
           'alive_OC': float(np.mean(tier == 3)), 'alive_T1_T2': float(np.mean((tier == 1) | (tier == 2)))}
    reach = {f'reach_{t}': float(np.mean(~np.isnan(t_reach[t]))) for t in t_reach}
    reach.update({f'median_years_to_{t}': (float(np.nanmedian(t_reach[t])) if np.any(~np.isnan(t_reach[t])) else None) for t in t_reach})
    reach['oc_within_20y'] = float(np.mean(t_reach[3] <= 20))
    by_tier = {f'natural_death_at_tier_{t}': float(np.mean((tier == 0) & (death_tier == t))) for t in (1, 2, 3, 4, 5)}
    return {'risk': hist_risk, 'tier': hist_tier, 'end_states': end, 'reach': reach, 'death_by_tier': by_tier,
            'derived': {'settle_years': settle_years, 'gate_enhanced': gate2, 'gate_overclocked': gate3,
                        'p_dev_gate_enhanced': _dev_share(gate2), 'p_dev_gate_overclocked': _dev_share(gate3),
                        'oc_calls': [(len(c), a, l) for c, a, l in oc_calls]}}
