"""Turn an observer run's log into the 12 measurements of balance spec §9.2,
plus [13], the interaction counters of docs/specs/cybernetics_v2_interactions.md
§9 item 10.

Reads every line that contains "EOTG_OBS <key>" (the resolved loc text) or a
raw "eotg_obs_<key>" (if the loc did not resolve). Each line may carry
y=<game year> and id=<character id>. Game years fall back to counting the
yearly marker lines when y= is missing.

Usage:
  python tools/parse_observer_log.py <debug.log> [more logs...] [--start-year 866]
Prints a plain-text report. Several logs (e.g. the 3 seeds) can be passed;
each is reported, then pooled where that makes sense.
"""

import collections
import re
import statistics
import sys

LINE = re.compile(r"(?:EOTG_OBS (\w+)|eotg_obs_(\w+))(?:.*?\by=(\d+))?(?:.*?\bid=(\d+))?")
TIME = re.compile(r"^\[(\d\d):(\d\d):(\d\d)\]")
STATES = ("none", "t1", "t2", "t3", "nf", "ti")
TTS = ("county", "duchy", "kingdom")
# Decision -> census states whose rulers can take it (for "per 10 eligible").
DEC_POOL = {
    "partial_removal": ("t2",), "overclock_regression": ("t3",),
    "maintenance_protocol": ("t1", "t2", "t3"), "consult_physician": ("t1", "t2", "t3", "nf"),
    "seek_augmentation": ("none",), "remove_implants": ("t1",),
    "augment_retainer": ("t1", "t2", "t3", "nf"), "aug_restraints": ("nf",),
    "aug_sedation": ("nf",), "aug_appoint_warden": ("nf",), "aug_embrace_cascade": ("nf",),
    "aug_excision": ("nf", "t3"), "aug_pursue_next_stage": ("t1", "t2"),
}


def pct(a, b):
    return f"{100.0 * a / b:5.1f}%" if b else "   n/a"


def med_iqr(xs):
    if not xs:
        return "n/a"
    xs = sorted(xs)
    if len(xs) < 4:
        return f"median {statistics.median(xs):.1f} (n={len(xs)})"
    q = statistics.quantiles(xs, n=4)
    return f"median {statistics.median(xs):.1f}, IQR {q[0]:.1f}-{q[2]:.1f} (n={len(xs)})"


def parse(path, start_year):
    events = []       # (year, key, id)
    year = start_year
    marks = []        # (year, seconds) from yearly markers
    for raw in open(path, encoding="utf-8", errors="replace"):
        m = LINE.search(raw)
        if not m:
            continue
        key = m.group(1) or m.group(2)
        y = int(m.group(3)) if m.group(3) else None
        cid = m.group(4)
        if key == "year":
            year = y if y else year + 1
            t = TIME.match(raw)
            if t:
                h, mi, s = map(int, t.groups())
                marks.append((year, h * 3600 + mi * 60 + s))
        elif key == "start" and y:
            year = y
        events.append((y if y else year, key, cid))
    return events, marks


def report(path, events, marks, start_year):
    print("=" * 78)
    print("LOG:", path)
    if not events:
        print("no EOTG_OBS lines: see README 'If the log is empty'")
        return
    y0 = min(e[0] for e in events)
    dec = lambda y: (y - y0) // 10
    # ---- 1, 5, 8, 9: censuses ----
    censuses, cur = [], None
    for y, k, cid in events:
        if k == "census_begin":
            cur = {"year": y, "c": collections.Counter()}
        elif k == "census_end" and cur:
            censuses.append(cur)
            cur = None
        elif cur is not None:
            cur["c"][k] += 1
    print("\n[1] CENSUS: augmented share of count+ rulers, by title tier (HQ2 at year 30:")
    print("    25-40% augmented; of those >= 15% t3 / nf / ti)")
    for c in censuses:
        cc = c["c"]
        print(f"  year {c['year']} (+{c['year'] - y0}):")
        for tt in TTS + ("all",):
            tts = TTS if tt == "all" else (tt,)
            n = {s: sum(cc[f"census_{s}_{t}"] for t in tts) for s in STATES}
            tot = sum(n.values())
            aug = tot - n["none"]
            top = n["t3"] + n["nf"] + n["ti"]
            print(f"    {tt:8} rulers {tot:5}  augmented {pct(aug, tot)}  "
                  + "  ".join(f"{s} {n[s]}" for s in STATES[1:])
                  + f"  | top (t3+nf+ti) {pct(top, aug)} of augmented")
    # ---- flows per decade ----
    by_dec = collections.defaultdict(collections.Counter)
    for y, k, cid in events:
        by_dec[dec(y)][k] += 1
    print("\n[2] FLOWS per decade")
    for d in sorted(by_dec):
        c = by_dec[d]
        print(f"  decade {d} (years {y0 + 10 * d}-{y0 + 10 * d + 9}):")
        print(f"    initiations: random {c['init_random']}  seek {c['init_seek']}  (non-rulers {c['init_nonruler']})")
        print(f"    T1->T2: pursue {c['prog_12_pursue']}  offer {c['prog_12_offer']}  (non-rulers {c['prog_12_nonruler']})")
        print(f"    T2->T3: pursue {c['prog_23_pursue']}  offer {c['prog_23_offer']}  (non-rulers {c['prog_23_nonruler']})")
        print(f"    regressions: OC->Enh {c['regress_32']}  Enh->Aug {c['regress_21']}")
        print(f"    cascades: rulers {c['cascade_ruler']}  non-rulers {c['cascade_nonruler']}")
        print(f"    terminal: death {c['term_death']}  seamless {c['term_seamless']}  excision {c['term_excision']}"
              f" (died on the table {c['term_excision_death']})  abdication {c['term_abdication']}")
    # ---- 3: timing ----
    first = {}
    for y, k, cid in events:
        if cid and k in ("init_random", "init_seek", "prog_12_pursue", "prog_12_offer",
                         "prog_23_pursue", "prog_23_offer", "init_nonruler", "cascade_nonruler",
                         "cascade_ruler", "term_death", "term_seamless", "term_excision",
                         "term_excision_death", "term_abdication", "death_nf"):
            first.setdefault((cid, k), y)
    def span(a_keys, b_keys):
        out = []
        ids = {cid for (cid, k) in first if k in a_keys}
        for cid in ids:
            a = min(first[(cid, k)] for k in a_keys if (cid, k) in first)
            bs = [first[(cid, k)] for k in b_keys if (cid, k) in first and first[(cid, k)] >= a]
            if bs:
                out.append(min(bs) - a)
        return out
    init = ("init_random", "init_seek")
    print("\n[3] TIMING (AI; observe mode has no player). Target: Overclocked median 18-28 years")
    print("    initiation -> Enhanced:   ", med_iqr(span(init, ("prog_12_pursue", "prog_12_offer"))))
    print("    initiation -> Overclocked:", med_iqr(span(init, ("prog_23_pursue", "prog_23_offer"))))
    if not any(cid for _, _, cid in events):
        print("    (no id= values in the log: the loc did not resolve; timing is unavailable)")
    # ---- 4: decisions ----
    print("\n[4] DECISIONS: AI takes per decade, and per 10 eligible rulers (eligible = mean census")
    print("    count of the decision's tiers at the decade's two censuses). Every decision > 0.")
    cens_by_year = {c["year"]: c["c"] for c in censuses}
    def pool(d, states):
        ys = [y for y in cens_by_year if y0 + 10 * d <= y <= y0 + 10 * d + 10]
        if not ys:
            return 0
        return statistics.mean(sum(cens_by_year[y][f"census_{s}_{t}"] for s in states for t in TTS) for y in ys)
    for d in sorted(by_dec):
        row = []
        for name, states in DEC_POOL.items():
            n = by_dec[d][f"dec_{name}"]
            p = pool(d, states)
            row.append(f"{name} {n}" + (f" ({10.0 * n / p:.2f}/10)" if p else ""))
        print(f"  decade {d}: " + "; ".join(row))
        oc_exits = by_dec[d]["regress_32"] + by_dec[d]["cascade_ruler"]
        print(f"    regression share of OC exits: {pct(by_dec[d]['regress_32'], oc_exits)} (target 35-65%)")
    # ---- 5: non-rulers ----
    print("\n[5] NON-RULERS: augmented knights by state at each census; nr cascades; years to cascade")
    for c in censuses:
        print(f"  year {c['year']}: " + "  ".join(f"{s} {c['c'][f'knight_{s}_all']}" for s in STATES[1:]))
    print("    non-ruler cascades (nr.006):", sum(1 for _, k, _ in events if k == "cascade_nonruler"))
    print("    augmentation -> cascade:", med_iqr(span(("init_nonruler",), ("cascade_nonruler",))), "(target median 15-25)")
    # ---- 6: event volume ----
    print("\n[6] EVENT VOLUME: yearly-list events per ruler-year, by state and title tier")
    print("    (targets: t3 counts <= 0.5 plus the Countdown; nf counts <= 0.4)")
    for d in sorted(by_dec):
        ys = [y for y in cens_by_year if y0 + 10 * d <= y <= y0 + 10 * d + 10]
        if not ys:
            continue
        cells = []
        for s in STATES:
            for t in TTS:
                rulers = statistics.mean(cens_by_year[y][f"census_{s}_{t}"] for y in ys)
                n = by_dec[d][f"ev_{s}_{t}"]
                if rulers:
                    cells.append(f"{s}/{t} {n / (rulers * 10):.2f}")
        print(f"  decade {d}: " + "  ".join(cells))
    # ---- 7: gold gate ----
    print("\n[7] GOLD GATE: past settling and dev gate, short of gold for Pursue (lever if > 70%)")
    for d in sorted(by_dec):
        c = by_dec[d]
        print(f"  decade {d}: T1 fail {pct(c['gold_t1_fail'], c['gold_t1_fail'] + c['gold_t1_ok'])}"
              f"   T2 fail {pct(c['gold_t2_fail'], c['gold_t2_fail'] + c['gold_t2_ok'])}")
    # ---- 8: dev gate ----
    print("\n[8] DEV GATE: count+ capitals by development (decides eotg_aug_dev_gate_*)")
    for c in censuses:
        cc = c["c"]
        tot = sum(cc[k] for k in ("dev_lt10", "dev_10_14", "dev_15_19", "dev_20_34", "dev_35p"))
        ge = lambda ks: sum(cc[k] for k in ks)
        print(f"  year {c['year']}: >=10 {pct(tot - cc['dev_lt10'], tot)}  "
              f">=15 {pct(ge(('dev_15_19', 'dev_20_34', 'dev_35p')), tot)}  "
              f">=20 {pct(ge(('dev_20_34', 'dev_35p')), tot)}  >=35 {pct(cc['dev_35p'], tot)}")
    # ---- 9: NF span ----
    print("\n[9] NEUROFRACTURED: cascade -> end (first terminal or death)")
    print("    span:", med_iqr(span(("cascade_ruler",), ("term_death", "term_seamless", "term_excision",
                                                         "term_excision_death", "term_abdication", "death_nf"))))
    for c in censuses:
        nf = sum(c["c"][f"census_nf_{t}"] for t in TTS)
        print(f"    year {c['year']}: on Sedation {pct(c['c']['nf_sedated'], nf)} of {nf} NF rulers")
    cc = collections.Counter(k for _, k, _ in events if k.startswith("courses_"))
    print("    Sedation courses at the terminal:", dict(cc))
    # ---- 10: countdown ----
    print("\n[10] COUNTDOWN: stage hits (stage 3 should be >= 60% of Countdowns that reach stage 4)")
    allc = collections.Counter(k for _, k, _ in events if k.startswith("cd_"))
    print("    ", dict(sorted(allc.items())))
    runs = collections.defaultdict(set)
    for y, k, cid in events:
        if cid and k.startswith("cd_"):
            if k == "cd_start":
                runs[cid] = set()
            runs[cid].add(k)
    reach4 = [r for r in runs.values() if "cd_4" in r]
    print(f"    of Countdowns reaching stage 4, stage 3 seen in {pct(sum('cd_3' in r for r in reach4), len(reach4))}"
          " (by owner id; last run per owner)")
    # ---- 11: arcs ----
    print("\n[11] ARCS per decade: starts / ends (ended by owner death in brackets)")
    for d in sorted(by_dec):
        c = by_dec[d]
        print(f"  decade {d}: heir starts OC {c['arc_heir_start_oc']} NF {c['arc_heir_start_nf']},"
              f" ends {c['arc_heir_end']} ({c['arc_heir_end_death']});"
              f" patron {c['arc_patron_start']} / {c['arc_patron_end']} ({c['arc_patron_end_death']});"
              f" retinue {c['arc_retinue_start']} / {c['arc_retinue_end']} ({c['arc_retinue_end_death']})")
    # ---- 12: performance ----
    print("\n[12] PERFORMANCE: game days per real minute, years 40-50 (from the year markers)")
    m = [(y, s) for y, s in marks if y0 + 40 <= y <= y0 + 50]
    if len(m) >= 2:
        secs = m[-1][1] - m[0][1]
        if secs < 0:
            secs += 86400
        years = m[-1][0] - m[0][0]
        print(f"    {365.0 * years / (secs / 60.0):.0f} days/min over {years} years ({secs} s)" if secs else "    n/a")
    else:
        print("    n/a: no time-stamped year markers for years 40-50 in this log")
    # ---- 13: interactions (interactions spec §9 item 10; judged against HQ2, §4.7) ----
    print("\n[13] INTERACTIONS per decade (interactions spec 9.10; read beside [1] and [2])")
    for d in sorted(by_dec):
        c = by_dec[d]
        print(f"  decade {d}: offer installs landed {c['int_offer_landed']} unlanded {c['int_offer_unlanded']};"
              f" demand removals {c['int_demand']}; examinations {c['int_examine']};"
              f" tamper starts {c['tamper_start']} successes {c['tamper_success']}"
              f" failures {c['tamper_failure']} discovered {c['tamper_discovered']};"
              f" salvages {c['int_salvage']} (died on the table {c['int_salvage_death']})")
    tot = collections.Counter(k for _, k, _ in events if k.startswith(("int_", "tamper_")))
    print("    whole run:", dict(sorted(tot.items())) or "none (any non-zero count answers engine check (c))")


def main(argv):
    start = 866
    if "--start-year" in argv:
        start = int(argv[argv.index("--start-year") + 1])
    paths = [a for a in argv if not a.startswith("--") and not a.isdigit()]
    if not paths:
        sys.exit(__doc__)
    for p in paths:
        ev, marks = parse(p, start)
        report(p, ev, marks, start)


if __name__ == "__main__":
    main(sys.argv[1:])
