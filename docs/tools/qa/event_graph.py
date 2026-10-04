"""Firing graph: what fires each augmentation event, sizes by file, and orphans.

Classifies every event as single, chain_head (fires a follow-up), chain_stage
(fired by another event), story (fired from a story cycle), decision (fired
only by a decision) or ORPHAN (nothing fires it). Sources are every
trigger_event in events/ and common/*/eotg_augmentation_*.txt.
Note: it does not read on_action `events = {}` lists; this system fires
everything through trigger_event, so that is enough here.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aug_parse import (common_files, event_files, load, load_events, root_arg,
                       short_file, walk)


def target_id(v):
    if isinstance(v, str):
        return v
    return next((x[2] for x in v if x[0] == "id"), None)


def main():
    p = root_arg(__doc__.splitlines()[0])
    p.add_argument("--list", action="store_true", help="print every event with its category and sources")
    args = p.parse_args()
    events = load_events(args.root)

    src = collections.defaultdict(set)
    for f in event_files(args.root):
        for k, o, v in load(f):
            if k in events and isinstance(v, list):
                for kk, oo, vv in walk(v):
                    if kk == "trigger_event" and target_id(vv):
                        src[target_id(vv)].add("ev:" + k)
    for f in common_files(args.root):
        kind = os.path.basename(f).split("_")[-1].replace(".txt", "")  # e.g. actions, stories, decisions
        for kk, oo, vv in walk(load(f)):
            if kk == "trigger_event" and target_id(vv):
                src[target_id(vv)].add(kind)

    size = collections.Counter()
    rows, orphans = [], []
    for eid, (f, body) in events.items():
        s = src.get(eid, set())
        kinds = {"event" if x.startswith("ev:") else x for x in s}
        has_next = any(kk == "trigger_event" for kk, oo, vv in walk(body))
        if not s:
            cat = "ORPHAN"
            orphans.append(eid)
        elif "stories" in kinds:
            cat = "story"
        elif "event" in kinds:
            cat = "chain_stage"
        elif "decisions" in kinds and "actions" not in kinds:
            cat = "decision"
        elif has_next:
            cat = "chain_head"
        else:
            cat = "single"
        size[(short_file(f), cat)] += 1
        rows.append((eid, cat, sorted(kinds)))

    files = sorted({a for a, b in size})
    cats = ["single", "chain_head", "chain_stage", "story", "decision", "ORPHAN"]
    print("file", *cats, sep="\t")
    for f in files:
        print(f, *[size[(f, c)] for c in cats], sep="\t")
    print("TOTAL", *[sum(size[(f, c)] for f in files) for c in cats], sep="\t")
    undefined = sorted(t for t in src if t.startswith(("eotg_aug", "eotg_fracture")) and t not in events)
    print("orphans (defined, never fired):", orphans)
    print("undefined (fired, never defined):", undefined)
    if args.list:
        for r in rows:
            print(*r)


if __name__ == "__main__":
    main()
