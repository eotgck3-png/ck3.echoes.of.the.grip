"""Frontier Systems: one project per run, yearly ticks, by type.

Reads (common/script_values/eotg_frontier_values.txt unless noted):
- yearly gain: eotg_frontier_yearly_gain_value (base rate by type, development and
  control bonuses, founder skill, sponsor bonus, traits/infra/type input, x pace);
- completion: eotg_frontier_completion_met (common/scripted_triggers/eotg_frontier_triggers.txt)
  with eotg_frontier_min_dev_value / _min_control_value;
- strain: the causes in eotg_frontier_tick_effect (common/scripted_effects/eotg_frontier_effects.txt):
  no founder, low control (eotg_frontier_low_control_value), occupied, war, danger; the
  quiet-year ease; sponsor lapse (eotg_frontier_check_sponsor_effect / _sponsor_pay_effect,
  rulings I2c / F2); the fail point eotg_frontier_strain_fail_value;
- the falter event eotg_frontier.005 (events/eotg_frontier_events.txt): options a
  (abandon), b (restart: half progress, strain 4), e (lead it: restart) by ai_chance;
  the sponsor's bail-out option d (strain 2) when the sponsor can pay twice.
"""
import numpy as np
from pdx_read import Ctx, VANILLA_DEFAULTS
from common import assume, MORTALITY, INCOME, SAVE_SHARE, TRAIT_FREQ

TYPES = ['settlement', 'trade', 'mining', 'military', 'religious', 'research', 'administrative']
START_DEV = assume('frontier_start_dev', (0, 3), 'an Unsettled Shoal starts at development 0-3')
START_CONTROL = assume('frontier_start_control', (30, 70), 'county control at the start')
CONTROL_GROWTH = assume('frontier_control_growth_per_year', 10, 'vanilla control recovery toward 100')
DEV_MILESTONES = assume('frontier_dev_milestones', (33, 66), '+1 development at each milestone (at most 2), eotg_frontier_milestone_effect')
FOUNDER_SKILL = assume('frontier_founder_skill', (10, 4), 'founder type skill ~ N(10, 4)')
SPONSORED = assume('frontier_sponsored_share', 0.4, 'share of projects with a sponsor at start')
SPONSOR_BROKE = assume('frontier_sponsor_cannot_pay_per_year', 0.05, 'sponsor gold below the yearly payment')
SPONSOR_RICH = assume('frontier_sponsor_can_pay_twice', 0.6, 'at the falter, the sponsor holds 2x the payment')
OCCUPIED = assume('frontier_occupied_per_year', 0.02, 'the Shoal is occupied in a given year')
WAR_REACH = assume('frontier_war_reaches_per_year', 0.07, 'holder at war (~23%) x the war reaching the Shoal (~0.3)')
DANGEROUS = assume('frontier_trait_dangerous', 0.15, 'Shoals with the Dangerous trait')
HOSTILE = assume('frontier_trait_hostile', 0.15, 'Shoals with the Hostile trait (no quiet-year ease)')
EVENT_PROGRESS = assume('frontier_event_progress_per_year', 0.5, 'mean progress from the flavour pool')
EVENT_STRAIN = assume('frontier_event_strain_per_year', 0.1, 'chance the flavour pool adds 1 strain')
PLAYER_APPOINTS = assume('frontier_player_appoints_founder', 0.8, 'a player holder replaces a dead founder within the year')
HOLDER_SKILL = assume('frontier_holder_skill', 10.0, 'the holder\'s type skill read by eotg_frontier_type_input_value')
HOLDER_GOLD_OK = assume('frontier_holder_gold_2x_minor', 0.6, 'holder gold >= 2 x minor_gold_value at the falter')


def run(R, ftype, holder_ai, runs, years, seed, sponsored=None):
    rng = np.random.default_rng(seed)
    t = np.full(runs, 'flag:' + ftype, dtype=object)
    dev = rng.integers(START_DEV[0], START_DEV[1] + 1, runs).astype(float)
    reach = dev + 2
    ctrl = rng.uniform(*START_CONTROL, runs)
    progress = np.zeros(runs); strain = np.zeros(runs); granted = np.zeros(runs)
    founder_ok = np.ones(runs, bool)
    skill = rng.normal(*FOUNDER_SKILL, runs)
    spons = rng.random(runs) < (SPONSORED if sponsored is None else sponsored)
    dangerous = rng.random(runs) < DANGEROUS; hostile = rng.random(runs) < HOSTILE
    traits = {k: rng.random(runs) < p for k, p in TRAIT_FREQ.items()}
    state = np.zeros(runs, int)   # 0 running, 1 completed, 2 abandoned
    done_year = np.full(runs, np.nan); lapses = 0; falters = 0; restarts = 0
    fail_at = R.num('eotg_frontier_strain_fail_value')
    ev = R.node('eotg_frontier.005')
    opts = {}
    for o in [c for c in ev.children if c.key == 'option']:
        name = [c for c in o.children if c.key == 'name' and not c.is_block]
        ai = [c for c in o.children if c.key == 'ai_chance']
        if name and ai:
            opts[name[0].value.split('.')[-1]] = {'ai_will_do': ai[0]}
    minor = VANILLA_DEFAULTS['minor_gold_value'][0]
    for y in range(years):
        run_ = state == 0
        # founder: deaths, AI auto-pick in the tick, player appoints
        fd = rng.random(runs) < MORTALITY
        founder_ok &= ~fd
        skill = np.where(fd, rng.normal(*FOUNDER_SKILL, runs), skill)
        if holder_ai:
            repick = ~founder_ok
        else:
            repick = ~founder_ok & (rng.random(runs) < PLAYER_APPOINTS)
        founder_ok |= repick
        add = np.zeros(runs)
        add += ~founder_ok
        ctx = Ctx({'var:eotg_frontier_type': t, 'development_level': dev, 'county_control': ctrl,
                   'has_variable:eotg_frontier_dev_reachable': True, 'var:eotg_frontier_dev_reachable': reach,
                   'trig:eotg_frontier_has_valid_founder': founder_ok,
                   'var:eotg_frontier_founder.martial': skill, 'var:eotg_frontier_founder.learning': skill,
                   'var:eotg_frontier_founder.stewardship': skill,
                   'has_county_modifier:eotg_frontier_trait_dangerous': dangerous,
                   'has_county_modifier:eotg_frontier_trait_hostile': hostile,
                   'var:eotg_frontier_progress': progress, 'var:eotg_frontier_strain': strain,
                   'holder.martial': HOLDER_SKILL, 'holder.stewardship': HOLDER_SKILL, 'holder.learning': HOLDER_SKILL,
                   'piety_level': 2.0, 'var:eotg_frontier_trade_network_bonus': 0.0},
                  scopes={'holder': Ctx({'is_ai': holder_ai})})
        lowc = R.num('eotg_frontier_low_control_value', ctx)
        add += ctrl < lowc
        add += rng.random(runs) < OCCUPIED
        add += (rng.random(runs) < WAR_REACH) & (ftype != 'military')
        minc = R.num('eotg_frontier_min_control_value', ctx)
        add += dangerous & (ctrl < minc) & (ftype != 'military')
        # sponsor: death or cannot pay -> lapse (+1 strain); paid -> sponsor bonus this tick
        lapse = spons & ((rng.random(runs) < MORTALITY) | (rng.random(runs) < SPONSOR_BROKE))
        add += lapse
        lapses += int((lapse & run_).sum())
        spons &= ~lapse
        add += rng.random(runs) < EVENT_STRAIN
        strain = np.where(run_, np.clip(strain + add, 0, fail_at), strain)
        ease = run_ & (add == 0) & ~hostile
        strain = np.where(ease, np.maximum(0, strain - 1), strain)
        ctx.values['has_variable:eotg_frontier_sponsor_paid'] = spons
        gain = np.asarray(R.num('eotg_frontier_yearly_gain_value', ctx), float) * np.ones(runs)
        old = progress.copy()
        progress = np.where(run_, np.clip(progress + gain + EVENT_PROGRESS, 0, 100), progress)
        for m in DEV_MILESTONES:
            hit = run_ & (old < m) & (progress >= m) & (granted < 2)
            dev = dev + hit; granted = granted + hit
        ctrl = np.minimum(100, ctrl + CONTROL_GROWTH)
        ctx.values.update({'development_level': dev, 'county_control': ctrl, 'var:eotg_frontier_progress': progress})
        mind = R.num('eotg_frontier_min_dev_value', ctx)
        complete = run_ & (progress >= 100) & (dev >= mind) & (ctrl >= R.num('eotg_frontier_min_control_value', ctx))
        state = np.where(complete, 1, state); done_year = np.where(complete, y + 1, done_year)
        falter = run_ & ~complete & (strain >= fail_at)
        if falter.any():
            falters += int(falter.sum())
            rich = spons & (rng.random(runs) < SPONSOR_RICH)
            goldok = rng.random(runs) < HOLDER_GOLD_OK
            fctx = Ctx({'gold': np.where(goldok, 3 * minor, minor), 'trig:eotg_frontier_has_valid_sponsor': spons,
                        'exists': True, 'scope:eotg_frontier_candidate': True,
                        **{'trait:' + k: v for k, v in traits.items()}, 'trait:diligent': traits['ambitious']},
                       scopes={'scope:eotg_frontier_county': Ctx({'trig:eotg_frontier_has_valid_sponsor': rich},
                                                                  scopes={'var:eotg_frontier_sponsor': Ctx({'gold': np.where(rich, 1e6, 0)})})})
            ws = {k: np.asarray(R.ai_will_do(d, fctx), float) * np.ones(runs) for k, d in opts.items() if k in ('a', 'b', 'e')}
            tot = sum(ws.values()) + 1e-9
            r = rng.random(runs)
            p_ab = ws.get('a', 0) / tot
            abandon = falter & ~rich & (r < p_ab)
            restart = falter & ~rich & ~abandon
            state = np.where(abandon, 2, state); done_year = np.where(abandon, y + 1, done_year)
            progress = np.where(restart, np.floor(progress * 0.5), progress)
            strain = np.where(restart, 4, np.where(falter & rich, 2, strain))
            restarts += int(restart.sum())
    yrs = done_year[state == 1]
    return {'completed': float(np.mean(state == 1)), 'abandoned': float(np.mean(state == 2)),
            'running_at_end': float(np.mean(state == 0)),
            'years_to_complete_p50': float(np.median(yrs)) if yrs.size else None,
            'years_to_complete_p90': float(np.percentile(yrs, 90)) if yrs.size else None,
            'falters_per_project': falters / runs, 'restarts_per_project': restarts / runs,
            'sponsor_lapses_per_project': lapses / runs, 'done_year': done_year, 'state': state}
