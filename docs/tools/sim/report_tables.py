"""Format results.json into the Markdown tables REPORT.md embeds.
    python docs/tools/sim/report_tables.py [results.json] > tables.md"""
import json, sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
p = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, '..', '..', 'qa', 'mechanics_sim_2026-11-03', 'results.json')
r = json.load(open(p))
pct = lambda v: f'{100 * v:.1f}%'
out = []
out.append('### Government resources (top ruler), 100 years, %d runs per cell\n' % r['meta']['runs'])
out.append('| System | Vassals | Policy | Equilibrium | Settles by year | At 0 | At 100 | 20y stuck at 0 | 20y stuck at 100 | Vassal median | Key counts |')
out.append('|---|---|---|---|---|---|---|---|---|---|---|')
for k, v in r['gov'].items():
    sysn, size, pol = k.split('|')
    counts = ', '.join(f'{a} {b:.3f}' for a, b in (v.get('counts') or {}).items())
    out.append(f"| {sysn} | {size} | {pol} | {v['equilibrium']:.1f} | {v['settle_year']} | {pct(v['at_lo'])} | {pct(v['at_hi'])} | "
               f"{pct(v['dead_lo_20y'])} | {pct(v['runaway_hi_20y'])} | {v['vassal_eq'] if v['vassal_eq'] is None else round(v['vassal_eq'], 1)} | {counts} |")
out.append('\n### Elections (at each top-ruler death)\n')
out.append('| System | Vassals | Policy | Elections | Resource leader\'s pick wins | Non-dynast would win without the dynasty rule |')
out.append('|---|---|---|---|---|---|')
for k, v in r['gov'].items():
    if v.get('elections'):
        sysn, size, pol = k.split('|'); e = v['elections']
        out.append(f"| {sysn} | {size} | {pol} | {e['elections']} | {pct(e['leader_pick_wins'])} | {pct(e['non_dynast_wins_without_rule'])} |")
out.append('\n### Cartel payers and succession\n')
out.append('| Vassals | Policy | Payers (last 20 y, mean) | Walk-offs within 5 y of a succession, per succession |')
out.append('|---|---|---|---|')
for k, v in r['gov'].items():
    if k.startswith('cartel'):
        _, size, pol = k.split('|')
        out.append(f"| {size} | {pol} | {v['payers_eq']:.2f} | {v['succession']['walkoffs_within_5y_per_succession']:.3f} |")
out.append('\n### Cybernetics (one ruler from installation; tier by realm size)\n')
out.append('| Vassals | Policy | Reach Enhanced | Reach Overclocked | OC within 20 y | Cascade (NF) | Seamless | Cascade death | Natural death | Median years to OC | to NF |')
out.append('|---|---|---|---|---|---|---|---|---|---|---|')
for k, v in r['cyber'].items():
    size, pol = k.split('|'); re_, es = v['reach'], v['end_states']
    out.append(f"| {size} | {pol} | {pct(re_['reach_2'])} | {pct(re_['reach_3'])} | {pct(re_['oc_within_20y'])} | {pct(re_['reach_4'])} | {pct(re_['reach_5'])} | "
               f"{pct(es['cascade_death'])} | {pct(es['natural_death'])} | {re_['median_years_to_3']} | {re_['median_years_to_4']} |")
out.append('\n### Frontier (one project; 100-year horizon)\n')
out.append('| Type / holder | Completed | Abandoned | Years to complete (median / p90) | Falters per project | Sponsor lapses per project |')
out.append('|---|---|---|---|---|---|')
for k, v in r['frontier'].items():
    out.append(f"| {k} | {pct(v['completed'])} | {pct(v['abandoned'])} | {v['years_to_complete_p50']} / {v['years_to_complete_p90']} | {v['falters_per_project']:.3f} | {v['sponsor_lapses_per_project']:.3f} |")
out.append('\n### Proposals, before and after\n')
for p in r['proposals']:
    out.append(f"**{p['id']}** `{p['system']}` override {p['override']}:\n")
    out.append('| Vassals | Policy | Metric | Before | After |'); out.append('|---|---|---|---|---|')
    for row in p['results']:
        for m in ('equilibrium', 'dead_lo_20y', 'at_hi', 'at_lo', 'vassal_eq', 'reach_3', 'oc_within_20y', 'cascade_death', 'post_succession_walkoffs', 'payers_eq'):
            if m in row['before'] and row['before'][m] is not None:
                b, a = row['before'][m], row['after'][m]
                out.append(f"| {row['size']} | {row['policy']} | {m} | {b:.3f} | {a:.3f} |")
    out.append('')
out.append('\n### ASSUMPTION list (models)\n')
for k, v in r['assumptions'].items():
    out.append(f'- `{k}`: {v}')
out.append('\n### ASSUMPTION list (reader: vanilla named values and unresolved names)\n')
for k, v in r['assumptions_reader'].items():
    out.append(f'- `{k}`: {v}')
print('\n'.join(out))
