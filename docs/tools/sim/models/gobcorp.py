"""Trade Oligarchy: Market Share (eotg_gobcorp_market_share), yearly steps.

Reads: eotg_gobcorp_market_share_next_value / _start_value / _inherit_value and the
TO2-TO5 values (common/script_values/eotg_gobcorp_values.txt); the yearly peace/war
tick (common/story_cycles/eotg_gobcorp_story.txt); the decisions
(common/decisions/eotg_gobcorp_decisions.txt): Corner the Market (top; each Prince
drained at most once a year, eotg_gobcorp_cornered 1 year, as merged) and Undercut a
Rival Prince (vassals; rival weighted by eotg_gobcorp_rival_weight_value); the
wealth election (eotg_gobcorp_elective).
"""
import numpy as np
from pdx_read import Ctx
from common import World, trait_ctx, annual_take, TIER_KEY
from models.gov_common import change, start_values, inherit, election

V = 'eotg_gobcorp_market_share_value'


def run(R, size, policy, runs, years, seed):
    rng = np.random.default_rng(seed)
    w = World(rng, runs, size)
    nv = w.nv
    chg = lambda cur, amt: change(R, 'eotg_gobcorp_market_share_next_value', V, 'eotg_gobcorp_market_share_amount', cur, amt)
    top = start_values(R, 'eotg_gobcorp_market_share_start_value', 'eotg_gobcorp_role_top', runs, True)
    vas = start_values(R, 'eotg_gobcorp_market_share_start_value', 'eotg_gobcorp_role_top', (runs, nv), False)
    peace = R.num('eotg_gobcorp_peace_gain_value'); war = R.num('eotg_gobcorp_war_loss_value')
    cg = R.num('eotg_gobcorp_corner_gain_value'); cs = R.num('eotg_gobcorp_corner_squeeze_value')
    ug = R.num('eotg_gobcorp_undercut_gain_value'); ul = R.num('eotg_gobcorp_undercut_loss_value')
    D_c = R.decision('eotg_decision_gobcorp_corner_market')
    D_u = R.decision('eotg_decision_gobcorp_undercut_rival')
    cd_c = np.zeros(runs); cd_u = np.zeros((runs, nv))
    hist = np.zeros((runs, years)); vhist = np.zeros((runs, years)); vmin = np.zeros((runs, years))
    corners = 0; undercuts = 0; elections = []
    for y in range(years):
        w.step_war(); w.step_gold()
        top = np.where(w.at_war, chg(top, war), chg(top, peace))
        vas = np.where(w.at_war[:, None], chg(vas, war), chg(vas, peace))
        cornered = np.zeros((runs, nv), bool)
        # Corner the Market (top): a source for the top, a sink for every Prince
        ctx = Ctx({V: top, 'gold': w.top_gold, 'tier': w.top_tier, 'is_at_war': w.at_war,
                   'trig:eotg_gobcorp_role_top': True, **trait_ctx(w.top_traits),
                   'iter:any_vassal': float(nv)},
                  scopes={'any_vassal': Ctx({'count': float(nv), 'government_has_flag': 1.0,
                                             'eotg_government_is_gobcorp': 1.0})})
        cost = R.cost_value(D_c, 'gold', ctx)
        ok = (~w.at_war) & (top < 100) & (cd_c <= 0) & (w.top_gold >= cost)
        if policy in ('greedy', 'greedy_all'):
            cn = ok
        else:
            # the "3+ Trade Oligarchy vassals" AI term (any_vassal = { count >= 3 ... }) is
            # fed the realm size through the any_vassal scope above
            cn = ok & annual_take(R, D_c, ctx, TIER_KEY[w.top_tier], rng, (runs,))
        top = np.where(cn, chg(top, cg), top)
        w.top_gold -= np.where(cn, cost, 0)
        drain = cn[:, None] & ~cornered
        vas = np.where(drain, chg(vas, cs), vas)
        cornered |= drain
        cd_c = np.where(cn, D_c['cooldown_years'], cd_c - 1)
        corners += int(cn.sum())
        # Undercut a Rival Prince (each vassal), rival weighted by share + 1
        if nv >= 2:
            for j in range(nv):
                vt = int(w.vtiers[j])
                cv = Ctx({V: vas[:, j], 'gold': w.v_gold[:, j], 'tier': vt, 'trig:eotg_gobcorp_role_vassal': True,
                          **trait_ctx(w.v_traits, j)})
                c = R.cost_value(D_u, 'gold', cv)
                okj = (cd_u[:, j] <= 0) & (w.v_gold[:, j] >= c)
                uc = okj if policy == 'greedy_all' else okj & annual_take(R, D_u, cv, TIER_KEY[vt], rng, (runs,))
                wts = np.asarray(R.num('eotg_gobcorp_rival_weight_value', Ctx({V: vas})), float) * np.ones_like(vas)
                wts[:, j] = 0
                cum = np.cumsum(wts, axis=1)
                pick = (cum < rng.random((runs, 1)) * cum[:, -1:]).sum(axis=1)
                rival = np.zeros((runs, nv), bool); rival[np.arange(runs), np.clip(pick, 0, nv - 1)] = True
                rival &= uc[:, None]
                vas = np.where(rival, chg(vas, ul), vas)
                vas[:, j] = np.where(uc, chg(vas[:, j], ug), vas[:, j])
                w.v_gold[:, j] -= np.where(uc, c, 0)
                cd_u[:, j] = np.where(uc, D_u['cooldown_years'], cd_u[:, j] - 1)
                undercuts += int(uc.sum())
        # deaths: the wealth election (electors: up to 9 richest Princes), heir 75%
        dead = w.deaths(runs)
        if dead.any():
            idx = np.where(dead)[0]
            k = min(nv, 8)
            order = np.argsort(-w.v_gold[idx].mean(axis=0))[:k]
            powerful = np.zeros((len(idx), k + 1), bool)
            e = election(R, rng, 'eotg_gobcorp_elective', top[idx], vas[idx][:, order],
                         np.concatenate([[w.top_tier], w.vtiers[order]]), powerful, V)
            e['n'] = len(idx); elections.append(e)
        top = np.where(dead, inherit(R, 'eotg_gobcorp_market_share_inherit_value', 'eotg_gobcorp_market_share', V,
                                     'eotg_gobcorp_predecessor', top, np.zeros(runs)), top)
        vdead = w.deaths((runs, nv))
        vas = np.where(vdead, inherit(R, 'eotg_gobcorp_market_share_inherit_value', 'eotg_gobcorp_market_share', V,
                                      'eotg_gobcorp_predecessor', vas, np.zeros((runs, nv))), vas)
        hist[:, y] = top; vhist[:, y] = vas.mean(axis=1); vmin[:, y] = vas.min(axis=1)
    from models.corporation import _merge
    return {'top': hist, 'vassal_mean': vhist, 'vassal_min': vmin, 'elections': _merge(elections),
            'counts': {'corner_per_run_year': corners / (runs * years),
                       'undercut_per_vassal_year': undercuts / (runs * years * nv)}}
