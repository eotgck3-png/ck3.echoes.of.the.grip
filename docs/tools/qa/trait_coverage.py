"""Per-file event/option statistics and personality-trait coverage.

For every augmentation event: option counts, trait-gated options, rolled /
duel / follow-up options, stress-helper use, risk moves. Then, for each of
vanilla's 36 personality traits: how often it gates an option, appears in a
stress response (stress_impact or an eotg_aug_stress_* helper), weights an
ai_chance, and is mentioned anywhere. Ends with non-personality traits used.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aug_parse import (PERS, common_files, event_files, find, load, load_events,
                       read, root_arg, strip_comments, walk)

SKILLS = ("prowess", "intrigue", "learning", "martial", "diplomacy", "stewardship")


def main():
    root = root_arg(__doc__.splitlines()[0]).parse_args().root
    events = load_events(root)

    helpers = {}
    eff = load(os.path.join(root, "common", "scripted_effects", "eotg_augmentation_effects.txt"))
    for k, op, v in eff:
        if k and k.startswith("eotg_aug_stress_"):
            helpers[k] = {kk for kk, o, vv in walk(v) if kk in PERS}

    gated, stress, aichance, anyref, nonpers = (collections.Counter() for _ in range(5))
    perfile = collections.defaultdict(collections.Counter)
    optcounts = collections.Counter()
    allopt = 0

    for eid, (f, body) in events.items():
        opts = find(body, "option")
        pf = perfile[f]
        pf["events"] += 1
        pf["options"] += len(opts)
        optcounts[len(opts)] += 1
        if len(opts) == 1:
            pf["single_opt"] += 1
        if any(k == "hidden" and v == "yes" for k, o, v in body):
            pf["hidden"] += 1
        if any(k == "trigger_event" for k, o, v in walk(body)):
            pf["ev_with_trigger_event"] += 1
        if any(k in ("random_list", "random") for blk in find(body, "immediate") for k, o, v in walk(blk)):
            pf["immediate_random"] += 1
        if any(k == "triggered_desc" for k, o, v in walk(body)):
            pf["ev_triggered_desc"] += 1

        for o in opts:
            allopt += 1
            keys = [k for k, oo, v in walk(o)]
            gtraits = {v for t in find(o, "trigger") for k, oo, v in walk(t)
                       if k == "has_trait" and isinstance(v, str)}
            gtraits |= {v for v in find(o, "trait") if isinstance(v, str)}
            for t in gtraits:
                if t in PERS:
                    gated[t] += 1
                else:
                    nonpers[("gate", t)] += 1
            if gtraits:
                pf["trait_gated"] += 1
            if any(k in ("random_list", "random", "duel") for k in keys):
                pf["opt_random"] += 1
            if "duel" in keys:
                pf["opt_duel"] += 1
            if "trigger_event" in keys:
                pf["opt_followup"] += 1
            skill = any(
                kk in SKILLS or kk == "has_trait"
                for k, oo, v in walk(o) if k in ("random_list", "random", "duel") and isinstance(v, list)
                for kk, o2, vv in walk(v)
            )
            if skill:
                pf["opt_rand_skill_or_trait"] += 1
            for k, oo, v in walk(o):
                if k == "stress_impact" and isinstance(v, list):
                    for kk, o2, vv in v:
                        if kk in PERS:
                            stress[kk] += 1
                if k in helpers:
                    for t in helpers[k]:
                        stress[t] += 1
                    pf["opt_helper"] += 1
                if k == "has_trait" and isinstance(v, str) and v not in PERS:
                    nonpers[("any", v)] += 1
            for v in find(o, "ai_chance"):
                for k, oo, vv in walk(v):
                    if k == "has_trait" and isinstance(vv, str):
                        if vv in PERS:
                            aichance[vv] += 1
                        else:
                            nonpers[("ai", vv)] += 1
            if "eotg_add_fracture_risk" in keys:
                pf["opt_risk"] += 1

    for f in event_files(root) + common_files(root):
        t = strip_comments(read(f))
        for p in PERS:
            anyref[p] += len(re.findall(r"\b" + p + r"\b", t))

    print("events", len(events), "options", allopt, "options-per-event", sorted(optcounts.items()))
    cols = ["events", "options", "single_opt", "hidden", "trait_gated", "opt_random",
            "opt_rand_skill_or_trait", "opt_duel", "opt_followup", "opt_helper", "opt_risk",
            "ev_with_trigger_event", "immediate_random", "ev_triggered_desc"]
    print("file", *cols, sep="\t")
    tot = collections.Counter()
    for f in sorted(perfile):
        print(f.replace("eotg_augmentation_", ""), *[perfile[f][c] for c in cols], sep="\t")
        tot.update(perfile[f])
    print("TOTAL", *[tot[c] for c in cols], sep="\t")

    print("\ntrait\tgated\tstress\tai\tanyref")
    for p in PERS:
        print(p, gated[p], stress[p], aichance[p], anyref[p], sep="\t")
    print("traits covered: gated", sum(1 for p in PERS if gated[p]),
          "stress", sum(1 for p in PERS if stress[p]),
          "ai", sum(1 for p in PERS if aichance[p]),
          "any", sum(1 for p in PERS if anyref[p]), "of", len(PERS))

    byt = collections.defaultdict(dict)
    for (kind, t), n in nonpers.items():
        byt[t][kind] = byt[t].get(kind, 0) + n
    print("\nnon-personality traits (gate / ai / any):")
    for t in sorted(byt):
        print(" ", t, byt[t])


if __name__ == "__main__":
    main()
