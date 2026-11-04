import os
"""Second pass: 0010 re-offer side effect of option A, and a per-stage (on-entry) cooldown variant."""
import sys, json
import numpy as np
SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SIM)
from pdx_read import Script
from models import void

RUNS, SEED, YEARS = 10000, 20261103, 100
STAGE_C = ('0020', '0021', '0022', '0023', '0024', '0025')
R = Script()


class EntryCd(void.Void):
    """Becoming Touched resets the cooldown to ENTRY years (whatever 0010/0011 set)."""
    ENTRY = 2
    def become_touched(self, m, year):
        super().become_touched(m, year)
        self.cd = np.where(m, self.ENTRY, self.cd)


def case(label, cls=void.Void, cd=None, entry=None):
    if entry is not None:
        cls.ENTRY = entry
    m = cls(R, RUNS, SEED, False)
    for e, y in (cd or {}).items():
        m.slots[e]['cooldown'] = y
    for y in range(1, YEARS + 1):
        m.step(y)
    sc = sum(m.fired[e] for e in STAGE_C)
    th = m.t_hollow - m.t_touch; th = th[~np.isnan(th)]
    r = {'case': label,
         'stage_c_per_100_seat_years': round(100 * sc / (RUNS * YEARS), 3),
         'stage_c_per_touched_ruler': round(sc / max(int(m.ever_touched.sum()), 1), 2),
         '0010_per_100_seat_years': round(100 * m.fired['0010'] / (RUNS * YEARS), 3),
         '0010_per_seeded_ruler': round(m.fired['0010'] / max(int(m.ever_seeded.sum()), 1), 2),
         '0011_per_100_seat_years': round(100 * m.fired['0011'] / (RUNS * YEARS), 3),
         'touched_years_median': float(np.median(th)) if len(th) else None,
         'ever_touched': round(float(np.mean(m.ever_touched)), 3),
         'ever_hollow': round(float(np.mean(m.ever_hollow)), 3)}
    print(json.dumps(r), flush=True)
    return r


out = [case('base'),
       case('A both 2', cd={'0010': 2, '0011': 2}),
       case('A 0011 only 2', cd={'0011': 2}),
       case('entry cd 2 (0010 stays 5 for refusers)', EntryCd, entry=2),
       case('entry cd 1', EntryCd, entry=1)]
json.dump(out, open(sys.argv[1], 'w', encoding='utf-8'), indent=1)
