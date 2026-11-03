"""PMC: Standing (eotg_pmc_standing), yearly steps.

Models (citations are where the script is read; numbers come from the reader):
- change effect + clamp: eotg_pmc_change_standing_effect -> eotg_pmc_standing_next_value
  (common/script_values/eotg_pmc_values.txt);
- start values and inheritance: eotg_pmc_standing_start_value / _inherit_value;
- battle feed: eotg_pmc_on_combat_won/_lost (common/on_action/eotg_pmc_on_actions.txt),
  amounts eotg_pmc_battle_won_value / _lost_value;
- drift: eotg_story_pmc_standing yearly effect_group (common/story_cycles/eotg_pmc_story.txt),
  eotg_pmc_drift_value above eotg_pmc_drift_threshold_value;
- decisions (common/decisions/eotg_pmc_decisions.txt): Take a Contract (top), Deliver
  Results (vassals), Recruit on Reputation (top sink), Stand Down (exit); cooldowns,
  costs, intervals and ai_will_do from the file.
"""
import numpy as np
from pdx_read import Ctx
from common import World, trait_ctx, annual_take, TIER_KEY, assume
from models.gov_common import change, start_values, inherit

V = 'eotg_pmc_standing_value'
KNIGHTS = assume('pmc_knights', 4, 'court knights held by a PMC top (knight_limit +2 from the government)')
KNIGHT_LIMIT = assume('pmc_knight_limit', 6, 'vanilla limit about 4 plus the government +2')


def run(R, size, policy, runs, years, seed):
    rng = np.random.default_rng(seed)
    w = World(rng, runs, size)
    nv = w.nv
    chg = lambda cur, amt: change(R, 'eotg_pmc_standing_next_value', V, 'eotg_pmc_standing_amount', cur, amt)
    top = start_values(R, 'eotg_pmc_standing_start_value', 'eotg_pmc_role_top', runs, True)
    vas = start_values(R, 'eotg_pmc_standing_start_value', 'eotg_pmc_role_top', (runs, nv), False)
    won = R.num('eotg_pmc_battle_won_value'); lost = R.num('eotg_pmc_battle_lost_value')
    drift = R.num('eotg_pmc_drift_value'); thr = R.num('eotg_pmc_drift_threshold_value')
    gain_c = R.num('eotg_pmc_contract_gain_value')
    d_gain = R.num('eotg_pmc_deliver_gain_value'); d_liege = R.num('eotg_pmc_deliver_liege_value')
    r_cost = R.num('eotg_pmc_recruit_cost_value'); r_spend = R.num('eotg_pmc_recruit_spend_value')
    D_take = R.decision('eotg_decision_pmc_take_contract')
    D_del = R.decision('eotg_decision_pmc_deliver_results')
    D_rec = R.decision('eotg_decision_pmc_recruit_on_reputation')
    D_exit = R.decision('eotg_decision_pmc_stand_down')
    contract_years = assume('pmc_under_contract_years', 2, 'eotg_pmc_under_contract_modifier years = 2 (decision effect)')
    cd_take = np.zeros(runs); cd_rec = np.zeros(runs); cd_del = np.zeros((runs, nv)); contract = np.zeros(runs)
    hist = np.zeros((runs, years)); vhist = np.zeros((runs, years))
    exited = np.zeros(runs, bool); takes = 0; recruits = 0; delivers = 0
    for y in range(years):
        w.step_war(); w.step_gold()
        # battles: the side's primary participant (the top as war leader)
        wins, losses = w.battles()
        for b in range(int(max(wins.max(), losses.max(), 0))):
            top = np.where(wins > b, chg(top, won), top)
            top = np.where(losses > b, chg(top, lost), top)
        # drift (story yearly tick)
        top = np.where(top > thr, chg(top, drift), top)
        vas = np.where(vas > thr, chg(vas, drift), vas)
        # Take a Contract
        ctx = Ctx({V: top, 'gold': w.top_gold, 'tier': w.top_tier, 'is_at_war': w.at_war,
                   'trig:eotg_pmc_role_top': True, **trait_ctx(w.top_traits)})
        valid = (~w.at_war) & (contract <= 0) & (cd_take <= 0) & ~exited
        if policy in ('greedy', 'greedy_all'):
            take = valid
        else:
            take = valid & annual_take(R, D_take, ctx, TIER_KEY[w.top_tier], rng, (runs,))
        pay = R.num('eotg_pmc_contract_pay_value', ctx)
        w.top_gold = w.top_gold + np.where(take, pay, 0)
        top = np.where(take, chg(top, gain_c), top)
        contract = np.where(take, contract_years, contract - 1)
        cd_take = np.where(take, D_take['cooldown_years'], cd_take - 1)
        takes += int(take.sum())
        # Recruit on Reputation (a sink; the greedy policy never spends its resource)
        if policy == 'ai':
            # ASSUMPTION: court knights vs the limit (Recruit's ai_will_do reads them)
            ctxr = ctx.child({V: top, 'number_of_knights': KNIGHTS, 'max_number_of_knights': KNIGHT_LIMIT})
            validr = (top >= r_cost) & (cd_rec <= 0) & ~exited
            rec = validr & annual_take(R, D_rec, ctxr, TIER_KEY[w.top_tier], rng, (runs,))
            top = np.where(rec, chg(top, r_spend), top)
            cd_rec = np.where(rec, D_rec['cooldown_years'], cd_rec - 1)
            recruits += int(rec.sum())
        # Deliver Results (each vassal)
        cost = np.zeros((runs, nv))
        for j in range(nv):
            vt = int(w.vtiers[j])
            cv = Ctx({V: vas[:, j], 'gold': w.v_gold[:, j], 'tier': vt, 'is_at_war': w.at_war,
                      'trig:eotg_pmc_role_vassal': True, **trait_ctx(w.v_traits, j)})
            c = R.cost_value(D_del, 'gold', cv)
            cost[:, j] = c
            ok = (~w.at_war) & (cd_del[:, j] <= 0) & (w.v_gold[:, j] >= c)
            if policy == 'greedy_all':
                dl = ok
            else:
                dl = ok & annual_take(R, D_del, cv, TIER_KEY[vt], rng, (runs,))
            vas[:, j] = np.where(dl, chg(vas[:, j], d_gain), vas[:, j])
            w.v_gold[:, j] -= np.where(dl, c, 0)
            top = np.where(dl, chg(top, d_liege), top)
            cd_del[:, j] = np.where(dl, D_del['cooldown_years'], cd_del[:, j] - 1)
            delivers += int(dl.sum())
        # Stand Down (AI only; recorded, the run continues as a PMC for the statistics)
        if policy == 'ai':
            cx = Ctx({V: top, 'martial': rng.normal(10, 4, runs), **trait_ctx(w.top_traits),
                      'trig:eotg_pmc_role_top': True})
            ex = annual_take(R, D_exit, cx, TIER_KEY[w.top_tier], rng, (runs,)) & ~exited
            exited |= ex
        # deaths: standing passes to the heir (landless heir: own = 0)
        dead = w.deaths(runs)
        top = np.where(dead, inherit(R, 'eotg_pmc_standing_inherit_value', 'eotg_pmc_standing', V,
                                     'eotg_pmc_predecessor', top, np.zeros(runs)), top)
        cd_take = np.where(dead, 0, cd_take); contract = np.where(dead, contract, contract)
        vdead = w.deaths((runs, nv))
        vinh = inherit(R, 'eotg_pmc_standing_inherit_value', 'eotg_pmc_standing', V,
                       'eotg_pmc_predecessor', vas, np.zeros((runs, nv)))
        vas = np.where(vdead, vinh, vas)
        hist[:, y] = top; vhist[:, y] = vas.mean(axis=1)
    return {'top': hist, 'vassal_mean': vhist,
            'counts': {'take_contract_per_run_year': takes / (runs * years),
                       'recruit_per_run_year': recruits / (runs * years),
                       'deliver_per_vassal_year': delivers / (runs * years * nv),
                       'stand_down_share': float(exited.mean())}}
