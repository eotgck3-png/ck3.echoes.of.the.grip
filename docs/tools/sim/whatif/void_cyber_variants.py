import os
"""What-if runs for the decisions memo. Reads the repo's sim models; writes nothing to the repo."""
import sys, json
import numpy as np
SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SIM)
from pdx_read import Script
from models import void, cybernetics

RUNS, SEED, YEARS = 10000, 20261103, 100
STAGE_C = ('0020', '0021', '0022', '0023', '0024', '0025')
R = Script()


def void_case(label, ov=None, cd=None, is_ai=False, years=YEARS):
    R.overrides = dict(ov or {})
    m = void.Void(R, RUNS, SEED, is_ai)
    for e, y in (cd or {}).items():
        m.slots[e]['cooldown'] = y
    depth100 = np.full(RUNS, np.nan)
    for y in range(1, years + 1):
        m.step(y)
        depth100 = np.where(m.hollow & (m.depth >= 100) & np.isnan(depth100), y, depth100)
    R.overrides = {}
    th = m.t_hollow - m.t_touch; th = th[~np.isnan(th)]
    sc = sum(m.fired[e] for e in STAGE_C)
    n_touched = int(np.sum(m.ever_touched))
    hd = depth100 - m.t_hollow; hd = hd[~np.isnan(hd)]
    return {'case': label,
            'stage_c_per_100_seat_years': round(100 * sc / (RUNS * years), 3),
            'stage_c_per_touched_ruler': round(sc / max(n_touched, 1), 2),
            'touched_years_median': float(np.median(th)) if len(th) else None,
            'touched_years_q': [float(v) for v in np.percentile(th, [25, 75])] if len(th) else None,
            'ever_touched': round(float(np.mean(m.ever_touched)), 3),
            'ever_hollow': round(float(np.mean(m.ever_hollow)), 3),
            'hollow_reaching_depth100_share': round(float(np.mean(~np.isnan(depth100[m.ever_hollow]))) if m.ever_hollow.any() else 0, 3),
            'years_hollow_to_depth100_median': float(np.median(hd)) if len(hd) else None,
            'voidwalkers_per_100_seat_years': round(100 * m.vw_created / (RUNS * years), 3)}


out = {'void': [], 'cyber': []}
cases = [
    ('base', None, None),
    ('A cd=2 (0010/0011)', None, {'0010': 2, '0011': 2}),
    ('A1 cd=1 (stage entry, vanilla per-level shape)', None, {'0010': 1, '0011': 1}),
    ('A3 cd=3', None, {'0010': 3, '0011': 3}),
    ('B touched +2', {'void.term.has_trait=eotg_void_touched': 2}, None),
    ('A+B', {'void.term.has_trait=eotg_void_touched': 2}, {'0010': 2, '0011': 2}),
    ('A + touched +4', {'void.term.has_trait=eotg_void_touched': 4}, {'0010': 2, '0011': 2}),
    ('V2 0004=25', {'void.slot.0004.chance': 25}, None),
    ('A + V2 0004=20', {'void.slot.0004.chance': 20}, {'0010': 2, '0011': 2}),
    ('A + V2 0004=25', {'void.slot.0004.chance': 25}, {'0010': 2, '0011': 2}),
]
for label, ov, cd in cases:
    r = void_case(label, ov, cd); out['void'].append(r); print(json.dumps(r), flush=True)
r = void_case('base AI 1%', None, None, is_ai=True); out['void'].append(r); print(json.dumps(r), flush=True)
r = void_case('A AI 1%', None, {'0010': 2, '0011': 2}, is_ai=True); out['void'].append(r); print(json.dumps(r), flush=True)

for gate in (20, 18, 17, 15):
    for size, pol in ((4, 'greedy'), (4, 'ai')):
        R.overrides = {'eotg_aug_dev_gate_overclocked': gate}
        r = cybernetics.run(R, size, pol, RUNS, YEARS, SEED)
        R.overrides = {}
        row = {'gate': gate, 'size': size, 'policy': pol,
               'reach_2': round(r['reach'].get('reach_2', 0), 3), 'reach_3': round(r['reach']['reach_3'], 3),
               'oc_within_20y': round(r['reach']['oc_within_20y'], 3),
               'median_years_to_3': r['reach'].get('median_years_to_3'),
               'cascade_death': round(r['end_states']['cascade_death'], 3), 'seamless': round(r['end_states']['seamless'], 3)}
        out['cyber'].append(row); print(json.dumps(row), flush=True)

json.dump(out, open(sys.argv[1], 'w', encoding='utf-8'), indent=1)
