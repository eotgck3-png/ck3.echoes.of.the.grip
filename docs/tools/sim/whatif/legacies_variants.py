"""Variant runs of docs/tools/sim/models/legacies.py (read-only use of the repo).

Differences from the repo model, each behind an override key:
  floor_mode   'sim'  : repo behaviour (any att <= floor never decays; att > floor stops at floor)
               'spec' : spec 3.1 step 1a (marker set at >= 25; marked sites stop at 25;
                        unmarked sites decay to 0; an option that drops below 25 clears the marker)
  floor_skip_sealed : the floor does not hold condition 5 (Sealed) sites
  drain_start  : the Extracted drain applies only while integrity <= this value
  hostile_transfer_annual : extra non-death transfers per site-year that fire 0105 regardless of dynasty
"""
import os, sys
import numpy as np
SIM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SIM); sys.path.insert(0, os.path.join(SIM, 'models'))
import legacies as L
from pdx_read import Script, Ctx
from common import MORTALITY, per_check_to_annual


def run(R, n_sites, years, seed, is_ai, ov):
    rng = np.random.default_rng(seed)
    tables = {e: L.option_table(R, e) for e in L.EVENTS}
    pn = L.pulse_numbers(R); sn = L.seed_numbers(R)
    D = R.decision('eotg_decision_survey_legacies')
    p_ai = float(per_check_to_annual(np.mean([R.ai_will_do(D, Ctx({'stewardship': st, 'learning': le, 'trait:curious': False, 'trait:content': False}))
                                              for st in (8, 14) for le in (8, 14)]), D['interval']['all']))
    fam_w = np.array([w for w, f in sn['families']]); fams = [f for w, f in sn['families']]
    decay = ov.get('decay', pn['decay'])
    peak = np.zeros(n_sites)
    sites = []
    for i in range(n_sites):
        s = L.Site(); s.family = fams[rng.choice(len(fams), p=fam_w / fam_w.sum())]
        s.known = False; s.cond = 1; s.integ = sn['start_integrity']; s.att = 0.0; s.cd = 0.0
        s.zeroed = 0; s.zero_year = None; s.disc_year = None; s.aftermath = 0; s.events = {}
        sites.append(s)
    marked = np.zeros(n_sites, bool)
    cond_end = np.zeros(n_sites, int); att_end = np.full(n_sites, np.nan)
    flag = np.zeros(n_sites); survey_cd = rng.integers(0, L.SURVEY_COOLDOWN, n_sites).astype(float)
    floor = ov.get('floor', 0.0); mode = ov.get('floor_mode', 'sim')
    a = {c['event']: c for c in pn['aftermath']}

    def mark(i, s):
        if mode == 'spec':
            if s.att >= floor and floor > 0:
                marked[i] = True
            elif s.att < floor:
                marked[i] = False

    def fire_and_mark(eid, i, s, y):
        L.fire(R, eid, s, rng, y, tables); mark(i, s)

    for y in range(years):
        for i, s in enumerate(sites):
            s.cd -= 1; flag[i] -= 1; survey_cd[i] -= 1
            transfer = False; same = False
            if rng.random() < MORTALITY:
                survey_cd[i] = 0
                transfer = True
                same = rng.random() < ov.get('heir_same_dynasty_share', 0.0)
            if not transfer and rng.random() < ov.get('hostile_transfer_annual', 0.0):
                transfer = True; same = False
            if transfer and s.known and s.cd <= 0 and not same:
                s.cd = 3.0
                fire_and_mark('0105', i, s, y)
            if not s.known and survey_cd[i] <= 0:
                take = (rng.random() < p_ai) if is_ai else True
                if take:
                    survey_cd[i] = L.SURVEY_COOLDOWN
                    s.known = True; s.disc_year = y; s.cond = 2; s.cd = L.DISCOVERY_CD
                    fire_and_mark(L.FAMILY_EVENT[s.family], i, s, y)
            if s.known:
                floored = (s.cond != 5) or not ov.get('floor_skip_sealed')
                if mode == 'sim':
                    if floored and s.att > floor:
                        s.att = max(floor, s.att + decay)
                    elif not floored and s.att > 0:
                        s.att = max(0.0, s.att + decay)
                else:
                    if s.att > 0:
                        if marked[i] and floored:
                            if s.att > floor:
                                s.att = max(floor, s.att + decay)
                        else:
                            s.att = max(0.0, s.att + decay)
                    mark(i, s)
                peak[i] = max(peak[i], s.att)
                if flag[i] <= 0:
                    ready = s.cd <= 0
                    if ready and s.att >= ov.get('gate_0101', 50):
                        c = a['0101']
                        if rng.random() < ov.get('chance_0101', c['chance']) / 100:
                            flag[i] = c['flag_years']; s.cd = c['site_cd']; s.aftermath += 1
                            fire_and_mark('0101', i, s, y)
                    elif ready and s.cond == 4 and rng.random() < L.POWERFUL:
                        c = a['0102']
                        if rng.random() < c['chance'] / 100:
                            flag[i] = c['flag_years']; s.cd = c['site_cd']; s.aftermath += 1
                            fire_and_mark('0102', i, s, y)
                    elif ready and s.integ <= 50 and s.cond in (3, 5):
                        c = a['0103']
                        if rng.random() < c['chance'] / 100:
                            flag[i] = c['flag_years']; s.cd = c['site_cd']; s.aftermath += 1
                            fire_and_mark('0103', i, s, y)
                dr = ov.get('extracted_drain')
                if s.cond == 4 and dr and s.integ <= ov.get('drain_start', 1000):
                    q = []
                    L.change_integrity(s, dr, y, q)
                    if q and ov.get('drain_fires_0104', True):
                        fire_and_mark('0104', i, s, y)   # repo model drops the queue; v2 fires 0104 at the crossing
        if y == years - 1:
            for i, s in enumerate(sites):
                cond_end[i] = s.cond if s.known else 1
                att_end[i] = s.att if s.known else np.nan
    zero = np.array([(s.zero_year - s.disc_year) if (s.zero_year is not None and s.disc_year is not None) else np.nan for s in sites])
    ev = lambda e: float(np.mean([s.events.get(e, 0) for s in sites]) * 100 / years)
    return {
        'cond': {c: float(np.mean(cond_end == c)) for c in range(1, 7)},
        'zero': float(np.mean(~np.isnan(zero))), 'zero_med': float(np.nanmedian(zero)) if np.any(~np.isnan(zero)) else None,
        'after': float(np.mean([s.aftermath for s in sites]) * 100 / years),
        'e0101': ev('0101'), 'e0104': ev('0104'), 'e0105': ev('0105'),
        'peak25': float(np.mean(peak >= 25)), 'peak50': float(np.mean(peak >= 50)),
        'att_med': float(np.nanmedian(att_end)), 'att_ge25': float(np.nanmean(att_end >= 25)),
    }


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20000
    R = Script(repo=L.V1)
    pkg = {'heir_same_dynasty_share': 0.9, 'extracted_drain': -1, 'floor': 25, 'gate_0101': 25}
    runs = [
        ('P0 package, repo floor semantics (reproduce)', True, dict(pkg, floor_mode='sim', drain_fires_0104=False)),
        ('P0b package, repo floor, 0104 fired at the drain crossing', True, dict(pkg, floor_mode='sim')),
        ('P1 package, spec floor (marker)', True, dict(pkg, floor_mode='spec')),
        ('P2 P1 + floor skips Sealed', True, dict(pkg, floor_mode='spec', floor_skip_sealed=True)),
        ('P3 P1, drain -1 only at integrity <= 50', True, dict(pkg, floor_mode='spec', drain_start=50)),
        ('P4 P1, drain -0.5', True, dict(pkg, floor_mode='spec', extracted_drain=-0.5)),
        ('P5 P1 + hostile transfers 1%/yr fire 0105', True, dict(pkg, floor_mode='spec', hostile_transfer_annual=0.01)),
        ('P6 P1, 0105 at every succession (no gate)', True, dict(pkg, floor_mode='spec', heir_same_dynasty_share=0.0)),
        ('P7 P1, gate 50 (v1) with floor 25', True, dict(pkg, floor_mode='spec', gate_0101=50)),
        ('P8 P1, player holder', False, dict(pkg, floor_mode='spec')),
    ]
    if len(sys.argv) > 2 and sys.argv[2] == 'q10':
        sp = dict(pkg, floor_mode='spec')
        runs = [('Q1 P1 baseline (gate 25, floor 25, decay -2)', True, sp),
                ('Q2 decay -1', True, dict(sp, decay=-1)),
                ('Q3 0101 chance 40', True, dict(sp, chance_0101=40)),
                ('Q4 gate 20, floor 20', True, dict(sp, gate_0101=20, floor=20)),
                ('Q5 gate 15, floor 15', True, dict(sp, gate_0101=15, floor=15)),
                ('Q6 gate 25, floor 25, decay -1, chance 40', True, dict(sp, decay=-1, chance_0101=40))]
    pct = lambda x: f'{100 * x:.1f}%'
    print('| Run | Governed | Extracted | Sealed | Unstable | reach 0 (median y) | aftermath/site-c | 0101 | 0104 | 0105 | att end median; share >= 25 | peak >= 25 / >= 50 |')
    print('|---|---|---|---|---|---|---|---|---|---|---|---|')
    for name, ai, ov in runs:
        r = run(R, n, 100, 20261103, ai, ov)
        c = r['cond']
        print(f"| {name} | {pct(c[3])} | {pct(c[4])} | {pct(c[5])} | {pct(c[6])} | {pct(r['zero'])} ({r['zero_med']}) | {r['after']:.2f} | {r['e0101']:.2f} | {r['e0104']:.2f} | {r['e0105']:.2f} | {r['att_med']:.0f}; {pct(r['att_ge25'])} | {pct(r['peak25'])} / {pct(r['peak50'])} |", flush=True)


if __name__ == '__main__':
    main()
