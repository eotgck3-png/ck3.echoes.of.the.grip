"""AI weights per option for events whose id starts with a prefix.

Usage: python option_ai_weights.py [root] --prefix eotg_aug_init --effects eotg_aug_initiate_effect,eotg_add_fracture_risk
For each option: trait gate, ai_chance base and modifiers, and which of the
named effects it calls. Used to estimate how often the AI accepts offers.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aug_parse import find, load_events, root_arg, walk


def main():
    p = root_arg(__doc__.splitlines()[0])
    p.add_argument("--prefix", required=True, help="event id prefix, e.g. eotg_aug_init")
    p.add_argument("--effects", default="", help="comma-separated effect names to flag")
    args = p.parse_args()
    flags_wanted = [x for x in args.effects.split(",") if x]
    for eid, (f, body) in load_events(args.root).items():
        if not eid.startswith(args.prefix):
            continue
        print(eid)
        for o in find(body, "option"):
            name = next((v for k, oo, v in o if k == "name" and isinstance(v, str)), "?")
            gate = [v for t in find(o, "trigger") for k, oo, v in walk(t) if k == "has_trait"]
            base, mods = 0, []
            for a in find(o, "ai_chance"):
                for k, oo, v in a:
                    if k == "base":
                        base = v
                    if k == "modifier" and isinstance(v, list):
                        amount = next((x[2] for x in v if x[0] in ("add", "factor")), "")
                        cond = ",".join(f"{x[0]}={x[2]}" for x in v if x[0] not in ("add", "factor"))
                        mods.append(f"{amount}:{cond[:30]}")
            hit = [e for e in flags_wanted if any(k == e for k, oo, v in walk(o))]
            print(f"  {name.split('.')[-1]} gate={gate} base={base} {hit} mods={mods}")


if __name__ == "__main__":
    main()
