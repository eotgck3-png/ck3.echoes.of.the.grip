"""Run every model over the full grid and write results, charts and tables.

    python docs/tools/sim/run_all.py [--runs 10000] [--years 100] [--seed 20261103] [--out DIR]

Grid: Cartel, PMC, Corporation, Trade Oligarchy and Cybernetics x realm sizes 1/4/8/16
x policies ai/greedy; Frontier x 7 types x AI/player holder. Then the proposed tunings
(PROPOSALS) are rerun with what-if overrides for before/after numbers. Fixed seed.
"""
import argparse, json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from pdx_read import Script, assumptions_used
from common import series_stats, ASSUMPTIONS
from models import cartel, pmc, corporation, gobcorp, cybernetics, frontier

SIZES = (1, 4, 8, 16)
POLICIES = ('ai', 'greedy', 'greedy_all')
GOV = {'cartel': cartel, 'pmc': pmc, 'corporation': corporation, 'gobcorp': gobcorp}

# Proposed tunings: one script value or constant each, rerun on the scenario that shows
# the problem. 'metric' names the number the report quotes before/after.
PROPOSALS = [
    {'id': 'P1', 'system': 'corporation', 'override': {'eotg_corporation_court_erosion_value': -2},
     'scenarios': [(16, 'greedy_all'), (16, 'ai'), (16, 'greedy')], 'metric': 'dead_lo_20y'},
    {'id': 'P2', 'system': 'pmc', 'override': {'eotg_pmc_deliver_liege_value': 2},
     'scenarios': [(16, 'ai'), (1, 'ai'), (16, 'greedy_all')], 'metric': 'equilibrium'},
    # Structural variant beside P2 (owner call): the liege gains from one Deliver Results a year.
    {'id': 'P2-cap', 'system': 'pmc', 'override': {'pmc_deliver_liege_once_a_year': True},
     'scenarios': [(16, 'ai'), (1, 'ai'), (16, 'greedy_all')], 'metric': 'equilibrium'},
    {'id': 'P3', 'system': 'gobcorp', 'override': {'eotg_gobcorp_war_loss_value': -3},
     'scenarios': [(4, 'ai'), (16, 'ai')], 'metric': 'vassal_eq'},
    {'id': 'P4', 'system': 'cybernetics', 'override': {'eotg_aug_dev_gate_overclocked': 15},
     'scenarios': [(4, 'ai'), (4, 'greedy')], 'metric': 'reach_3'},
    {'id': 'P5', 'system': 'cartel', 'override': {'eotg_cartel_on_death.years': 5},
     'scenarios': [(4, 'ai'), (16, 'ai')], 'metric': 'post_succession_walkoffs_10y'},
]
# P6 (Take a Contract pay) is NOT simulated: the gold proxy (INCOME) is about 2x vanilla's
# medium gold, and vanilla's medium_gold_value has a floor of 50 (00_basic_values.txt:82,
# local audit), so at the floor a count and a duke both get 75 under P6. See REPORT M4.

# --checks: the 2,000-run side checks REPORT quotes (alternative values).
CHECKS = [
    {'id': 'P2-alt', 'system': 'pmc', 'override': {'eotg_pmc_deliver_liege_value': 1}, 'scenarios': [(16, 'ai')]},
    {'id': 'P3-alt', 'system': 'gobcorp', 'override': {'eotg_gobcorp_peace_gain_value': 2}, 'scenarios': [(4, 'ai'), (16, 'ai')]},
    {'id': 'P1-cap-alt', 'system': 'corporation', 'override': {'eotg_corporation_court_erosion_value': -3}, 'scenarios': [(16, 'greedy_all')]},
]
# --checks also sweeps the top's war share for the Trade Oligarchy knife-edge (M1).
WAR_SHARES = (0.10, 0.15, 0.20, 0.25, 0.30)


def gov_summary(name, r):
    s = series_stats(r['top'])
    out = {k: (v.tolist() if isinstance(v, np.ndarray) else v) for k, v in s.items()}
    out['vassal_eq'] = float(np.median(r['vassal_mean'][:, -20:])) if 'vassal_mean' in r else None
    out['counts'] = r.get('counts')
    if 'elections' in r:
        out['elections'] = r['elections']
    if 'payers' in r:
        out['payers_eq'] = float(np.mean(r['payers'][:, -20:]))
        out['succession'] = r.get('succession')
        out['derived'] = r.get('derived')
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--runs', type=int, default=10000)
    ap.add_argument('--years', type=int, default=100)
    ap.add_argument('--seed', type=int, default=20261103)
    ap.add_argument('--out', default=os.path.join(HERE, '..', '..', 'qa', 'mechanics_sim_2026-11-03'))
    ap.add_argument('--checks', action='store_true', help='also run the 2,000-run side checks and the war-share sweep')
    ap.add_argument('--hostile', action='store_true', help='also run the Frontier hostile-world variant (REPORT L2)')
    ap.add_argument('--only', default='', help='comma list of parts to run: gov,cyber,frontier,proposals,void (default all)')
    a = ap.parse_args()
    parts = set(a.only.split(',')) if a.only else {'gov', 'cyber', 'frontier', 'proposals', 'void'}
    os.makedirs(a.out, exist_ok=True)
    R = Script()
    res = {'meta': {'runs': a.runs, 'years': a.years, 'seed': a.seed}, 'gov': {}, 'cyber': {}, 'frontier': {}, 'proposals': []}
    series_for_chart = {}
    t0 = time.time()
    for name, mod in (GOV.items() if 'gov' in parts else ()):
        for size in SIZES:
            for pol in POLICIES:
                r = mod.run(R, size, pol, a.runs, a.years, a.seed)
                res['gov'][f'{name}|{size}|{pol}'] = gov_summary(name, r)
                if pol == 'ai':
                    series_for_chart[(name, size)] = series_stats(r['top'])
                print(f'{name} size {size} {pol}: {time.time() - t0:.0f}s', flush=True)
    cy_series = {}
    for size in (SIZES if 'cyber' in parts else ()):
        for pol in POLICIES:
            r = cybernetics.run(R, size, pol, a.runs, a.years, a.seed)
            res['cyber'][f'{size}|{pol}'] = {'end_states': r['end_states'], 'reach': r['reach'],
                                            'death_by_tier': r['death_by_tier'], 'derived': r['derived']}
            if size == 4:
                cy_series[pol] = r['tier']
    print(f'cybernetics: {time.time() - t0:.0f}s', flush=True)
    fr_curves = {}
    for ty in (frontier.TYPES if 'frontier' in parts else ()):
        for ai in (True, False):
            r = frontier.run(R, ty, ai, a.runs, a.years, a.seed)
            dy, st = r.pop('done_year'), r.pop('state')
            res['frontier'][f'{ty}|{"ai" if ai else "player"}'] = r
            if ai:
                fr_curves[ty] = np.array([np.mean((st == 1) & (dy <= y)) for y in range(1, 31)])
    for sp in ((0.0, 1.0) if 'frontier' in parts else ()):
        r = frontier.run(R, 'settlement', True, a.runs, a.years, a.seed, sponsored=sp)
        r.pop('done_year'); r.pop('state')
        res['frontier'][f'settlement|ai|sponsored={sp}'] = r
    print(f'frontier: {time.time() - t0:.0f}s', flush=True)
    # proposals: before/after
    for p in (PROPOSALS if 'proposals' in parts else []):
        if not p['scenarios']:
            continue
        row = {'id': p['id'], 'system': p['system'], 'override': p['override'], 'results': []}
        for size, pol in p['scenarios']:
            pair = {}
            for label, ov in (('before', {}), ('after', p['override'])):
                R.overrides = dict(ov)
                if p['system'] == 'cybernetics':
                    r = cybernetics.run(R, size, pol, a.runs, a.years, a.seed)
                    pair[label] = {**r['reach'], **r['end_states']}
                else:
                    r = GOV[p['system']].run(R, size, pol, a.runs, a.years, a.seed)
                    g = gov_summary(p['system'], r)
                    g.pop('p10'); g.pop('p50'); g.pop('p90')
                    if 'succession' in g:
                        g['post_succession_walkoffs'] = g['succession']['walkoffs_within_5y_per_succession']
                        g['post_succession_walkoffs_10y'] = g['succession']['walkoffs_within_10y_per_succession']
                    pair[label] = g
            R.overrides = {}
            row['results'].append({'size': size, 'policy': pol, **pair})
        res['proposals'].append(row)
        print(f'proposal {p["id"]}: {time.time() - t0:.0f}s', flush=True)
    if a.checks:
        res['checks'] = run_checks(R, a.years, a.seed)
        print(f'checks: {time.time() - t0:.0f}s', flush=True)
    if a.hostile:
        res['frontier_hostile'] = run_hostile(R, a.runs, a.years, a.seed)
        print(f'hostile: {time.time() - t0:.0f}s', flush=True)
    if 'void' in parts and os.path.exists(os.path.join(HERE, 'models', 'void.py')):
        from models import void
        res['void'] = void.run_all(R, a.runs, a.seed)
        void.chart(a.out, res['void'])
        print(f'void: {time.time() - t0:.0f}s', flush=True)
    res['assumptions'] = {k: str(v) for k, v in ASSUMPTIONS.items()}
    res['assumptions_reader'] = assumptions_used()
    json.dump(res, open(os.path.join(a.out, 'results.json'), 'w'), indent=1, default=float)
    if 'gov' in parts and 'cyber' in parts and 'frontier' in parts:
        charts(a.out, series_for_chart, cy_series, fr_curves, a.years)
    print('done', round(time.time() - t0), 's')


def run_checks(R, years, seed, runs=2000):
    import common
    out = []
    for c in CHECKS:
        for size, pol in c['scenarios']:
            R.overrides = dict(c['override'])
            g = gov_summary(c['system'], GOV[c['system']].run(R, size, pol, runs, years, seed))
            R.overrides = {}
            out.append({'id': c['id'], 'override': c['override'], 'size': size, 'policy': pol, 'runs': runs,
                        'equilibrium': g['equilibrium'], 'vassal_eq': g['vassal_eq'], 'dead_lo_20y': g['dead_lo_20y'], 'at_hi': g['at_hi']})
    base = common.WAR_START
    sweep = []
    for share in WAR_SHARES:
        common.WAR_START = 0.5 * share / (1 - share)   # stationary share = start / (start + end), end 0.5
        g = gov_summary('gobcorp', gobcorp.run(R, 4, 'ai', runs, years, seed))
        sweep.append({'war_share': share, 'top_eq': g['equilibrium'], 'vassal_eq': g['vassal_eq'],
                      'feed_per_year': (1 - share) * R.num('eotg_gobcorp_peace_gain_value') + share * R.num('eotg_gobcorp_war_loss_value')})
    common.WAR_START = base
    return {'side_checks': out, 'gobcorp_war_share_sweep': sweep}


def run_hostile(R, runs, years, seed):
    saved = (frontier.WAR_REACH, frontier.DANGEROUS, frontier.OCCUPIED)
    frontier.WAR_REACH, frontier.DANGEROUS, frontier.OCCUPIED = 0.25, 0.40, 0.06   # REPORT L2's hostile world
    out = {}
    for ty in frontier.TYPES:
        r = frontier.run(R, ty, True, runs, years, seed)
        r.pop('done_year'); r.pop('state')
        out[ty] = r
    frontier.WAR_REACH, frontier.DANGEROUS, frontier.OCCUPIED = saved
    return out


def charts(out, ser, cy, fr, years):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    labels = {'cartel': ('Cartel: dread (AI ruler)', 'Dread'), 'pmc': ('PMC: Standing (AI top)', 'Standing'),
              'corporation': ('Corporation: CEO Board Influence (AI)', 'Board Influence'),
              'gobcorp': ('Trade Oligarchy: First Prince Market Share (AI)', 'Market Share')}
    x = np.arange(1, years + 1)
    for name, (title, ylab) in labels.items():
        fig, ax = plt.subplots(figsize=(8, 4.5))
        for size in SIZES:
            s = ser[(name, size)]
            ax.plot(x, s['p50'], label=f'{size} vassals (median)')
            ax.fill_between(x, s['p10'], s['p90'], alpha=0.12)
        ax.set_xlabel('Game year'); ax.set_ylabel(ylab); ax.set_title(title + ', median and 10-90% band')
        ax.set_ylim(0, 100); ax.legend(); ax.grid(alpha=0.3)
        fig.tight_layout(); fig.savefig(os.path.join(out, f'chart_{name}.png'), dpi=110); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    names = {1: 'Augmented', 2: 'Enhanced', 3: 'Overclocked', 4: 'Neurofractured', 5: 'Seamless', 0: 'Died (natural)', -1: 'Died (cascade)'}
    for pol, ls in (('ai', '-'), ('greedy', '--')):
        t = cy[pol]
        for k in (2, 3, 4, 5, -1):
            ax.plot(x, (t == k).mean(axis=0), ls, label=f'{names[k]} ({pol})')
    ax.set_xlabel('Years since installation'); ax.set_ylabel('Share of rulers'); ax.set_title('Cybernetics: tier occupancy (duke, AI solid, player-like dashed)')
    ax.legend(fontsize=7, ncol=2); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(out, 'chart_cybernetics.png'), dpi=110); plt.close(fig)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    for ty, c in fr.items():
        ax.plot(np.arange(1, 31), c, label=ty)
    ax.set_xlabel('Years since establishment'); ax.set_ylabel('Share completed'); ax.set_title('Frontier: cumulative completion by type (AI holder)')
    ax.legend(); ax.grid(alpha=0.3)
    fig.tight_layout(); fig.savefig(os.path.join(out, 'chart_frontier.png'), dpi=110); plt.close(fig)


if __name__ == '__main__':
    main()
