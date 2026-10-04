"""How options move eotg_fracture_risk, per file.

Counts options whose top level calls eotg_add_fracture_risk (moves nested in
if/random blocks or on other scopes are not counted), how many are positive
or negative, and the mean / min / max amount.
"""
import collections
import os
import statistics
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aug_parse import find, load_events, root_arg, short_file


def main():
    root = root_arg(__doc__.splitlines()[0]).parse_args().root
    byf = collections.defaultdict(list)
    for eid, (f, body) in load_events(root).items():
        for o in find(body, "option"):
            total, has = 0, False
            for k, oo, v in o:
                if k == "eotg_add_fracture_risk" and isinstance(v, list):
                    amount = next((x[2] for x in v if x[0] == "AMOUNT"), "0")
                    try:
                        total += int(amount)
                        has = True
                    except ValueError:
                        pass
            byf[short_file(f)].append(total if has else None)
    for f, vals in sorted(byf.items()):
        moved = [x for x in vals if x is not None]
        print(f, "options", len(vals), "with_risk", len(moved),
              "pos", sum(1 for x in moved if x > 0), "neg", sum(1 for x in moved if x < 0),
              "mean", round(statistics.mean(moved), 1) if moved else "-",
              "min", min(moved) if moved else "-", "max", max(moved) if moved else "-")


if __name__ == "__main__":
    main()
