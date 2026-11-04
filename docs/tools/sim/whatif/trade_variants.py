import os
"""Scratch what-if for the Trade Oligarchy imbalance. Reads the repo sim read-only.
Variant loop = docs/tools/sim/models/gobcorp.py run(), with three knobs:
  dues      : First Prince gains DUES each year if >=1 Trade Oligarchy vassal is at peace
  top_war   : override war loss for the TOP only (None = script value)
  vas_liege : vassals lose this much in years their liege (the top) is at war
"""
import sys, json
REPO_SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_SIM)
import numpy as np
import common
from pdx_read import Script, Ctx
from common import World, trait_ctx, annual_take, TIER_KEY, series_stats
from models.gov_common import change, start_values, inherit

V = 'eotg_gobcorp_market_share_value'


def run(R, size, policy, runs, years, seed, dues=0.0, top_war=None, vas_liege=0.0, corner_squeeze=None):
    rng = np.random.default_rng(seed)
    w = World(rng, runs, size)
    nv = w.nv
    chg = lambda cur, amt: change(R, 'eotg_gobcorp_market_share_next_value', V, 'eotg_gobcorp_market_share_amount', cur, amt)
    top = start_values(R, 'eotg_gobcorp_market_share_start_value', 'eotg_gobcorp_role_top', runs, True)
    vas = start_values(R, 'eotg_gobcorp_market_share_start_value', 'eotg_gobcorp_role_top', (runs, nv), False)
    peace = R.num('eotg_gobcorp_peace_gain_value'); war = R.num('eotg_gobcorp_war_loss_value')
    twar = war if top_war is None else top_war
    cg = R.num('eotg_gobcorp_corner_gain_value'); cs = R.num('eotg_gobcorp_corner_squeeze_value') if corner_squeeze is None else corner_squeeze
    ug = R.num('eotg_gobcorp_undercut_gain_value'); ul = R.num('eotg_gobcorp_undercut_loss_value')
    D_c = R.decision('eotg_decision_gobcorp_corner_market')
    D_u = R.decision('eotg_decision_gobcorp_undercut_rival')
    cd_c = np.zeros(runs); cd_u = np.zeros((runs, nv))
    hist = np.zeros((runs, years)); vhist = np.zeros((runs, years))
    for y in range(years):
        w.step_war(); w.step_gold()
        top_at_war = w.at_war.copy()
        top = np.where(w.at_war, chg(top, twar), chg(top, peace))
        if dues:
            any_peace_vassal = (~w.v_at_war).any(axis=1)
            top = np.where(any_peace_vassal, chg(top, dues), top)
        vas = np.where(w.v_at_war, chg(vas, war), chg(vas, peace))
        if vas_liege:
            vas = np.where(top_at_war[:, None] & ~w.v_at_war, chg(vas, vas_liege), vas)
        ctx = Ctx({V: top, 'gold': w.top_gold, 'tier': w.top_tier, 'is_at_war': w.at_war,
                   'trig:eotg_gobcorp_role_top': True, **trait_ctx(w.top_traits),
                   'iter:any_vassal': float(nv)},
                  scopes={'any_vassal': Ctx({'count': float(nv), 'government_has_flag': 1.0,
                                             'eotg_government_is_gobcorp': 1.0})})
        cost = R.cost_value(D_c, 'gold', ctx)
        ok = (~w.at_war) & (top < 100) & (cd_c <= 0) & (w.top_gold >= cost)
        cn = ok if policy in ('greedy', 'greedy_all') else ok & annual_take(R, D_c, ctx, TIER_KEY[w.top_tier], rng, (runs,))
        top = np.where(cn, chg(top, cg), top)
        w.top_gold -= np.where(cn, cost, 0)
        vas = np.where(cn[:, None], chg(vas, cs), vas)
        cd_c = np.where(cn, D_c['cooldown_years'], cd_c - 1)
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
        dead = w.deaths(runs)
        top = np.where(dead, inherit(R, 'eotg_gobcorp_market_share_inherit_value', 'eotg_gobcorp_market_share', V,
                                     'eotg_gobcorp_predecessor', top, np.zeros(runs)), top)
        vdead = w.deaths((runs, nv))
        vas = np.where(vdead, inherit(R, 'eotg_gobcorp_market_share_inherit_value', 'eotg_gobcorp_market_share', V,
                                      'eotg_gobcorp_predecessor', vas, np.zeros((runs, nv))), vas)
        hist[:, y] = top; vhist[:, y] = vas.mean(axis=1)
    s = series_stats(hist)
    return {'top_eq': round(s['equilibrium'], 1), 'vas_eq': round(float(np.median(vhist[:, -20:])), 1),
            'top_at0': round(s['at_lo'], 3), 'top_at100': round(s['at_hi'], 3),
            'top_ge30': round(float(np.mean(hist[:, -20:] >= 30)), 3), 'top_ge60': round(float(np.mean(hist[:, -20:] >= 60)), 3)}


if __name__ == '__main__':
    R = Script()
    runs, years, seed = 2000, 100, 20261103
    variants = {
        'baseline': {},
        'P3 war -3 (all)': {'top_war': None},
        'A dues +1 (scale-free)': {'dues': 1.0},
        'B top war -2 only': {'top_war': -2.0},
        'C vassals -1 in liege war': {'vas_liege': -1.0},
        'A+C': {'dues': 1.0, 'vas_liege': -1.0},
    }
    out = []
    for name, kw in variants.items():
        for size in (1, 4, 16):
            for pol in ('ai', 'greedy'):
                if name.startswith('P3'):
                    R.overrides = {'eotg_gobcorp_war_loss_value': -3}
                r = run(R, size, pol, runs, years, seed, **kw)
                R.overrides = {}
                out.append((name, size, pol, r))
                print(name, size, pol, r, flush=True)
    # war-share sweep for baseline and A
    base = common.WAR_START
    for share in (0.10, 0.20, 0.30, 0.40):
        common.WAR_START = 0.5 * share / (1 - share)
        for name, kw in (('baseline', {}), ('A dues +1', {'dues': 1.0}), ('B top war -2', {'top_war': -2.0})):
            r = run(R, 4, 'ai', runs, years, seed, **kw)
            print('sweep', share, name, r, flush=True)
    common.WAR_START = base
