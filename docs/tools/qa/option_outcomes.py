"""Outcome classes of every option: fixed, flat roll, weighted roll, duel, conditional.

weighted_roll = a random/random_list with a modifier block; conditional = a
fixed option whose effects branch on a trait or skill (if/limit). Also counts
follow-up trigger_events per file and how many are 30+ days out.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aug_parse import find, load_events, root_arg, short_file, walk

UNIT_DAYS = {"days": 1, "months": 30, "years": 365}
COND_KEYS = ("has_trait", "prowess", "intrigue", "learning", "martial", "diplomacy",
             "stewardship", "eotg_has_physician_access")


def delay_days(v):
    """Longest delay of a trigger_event block, in days (0 if immediate or unknown)."""
    if not isinstance(v, list):
        return 0
    for k, o, vv in v:
        if k in UNIT_DAYS:
            if isinstance(vv, str):
                n = int(vv) if vv.isdigit() else 0
            else:
                nums = [int(x[0]) for x in vv if x[0] and x[0].isdigit()]
                n = max(nums) if nums else 0
            return n * UNIT_DAYS[k]
    return 0


def main():
    root = root_arg(__doc__.splitlines()[0]).parse_args().root
    total = collections.Counter()
    byf = collections.defaultdict(collections.Counter)
    for eid, (f, body) in load_events(root).items():
        fn = short_file(f)
        for o in find(body, "option"):
            keys = [k for k, oo, v in walk(o)]
            rblocks = [v for k, oo, v in walk(o) if k in ("random_list", "random") and isinstance(v, list)]
            duel = "duel" in keys
            weighted = duel or any(any(k == "modifier" for k, oo, vv in walk(b)) for b in rblocks)
            cls = "fixed"
            if duel:
                cls = "duel"
            elif rblocks:
                cls = "weighted_roll" if weighted else "flat_roll"
            if cls == "fixed":
                for k, oo, v in o:
                    if k in ("trigger", "ai_chance", "name", "trait") or not isinstance(v, list):
                        continue
                    if any(kk == "limit" and isinstance(vv, list) and any(x[0] in COND_KEYS for x in walk(vv))
                           for kk, o2, vv in walk(v)):
                        cls = "conditional"
                        break
            total[cls] += 1
            byf[fn][cls] += 1
            for k, oo, v in walk(o):
                if k == "trigger_event":
                    byf[fn]["followup"] += 1
                    if delay_days(v) >= 30:
                        byf[fn]["followup_30d+"] += 1
    print("all options:", dict(total))
    for f in sorted(byf):
        print(f, dict(byf[f]))


if __name__ == "__main__":
    main()
