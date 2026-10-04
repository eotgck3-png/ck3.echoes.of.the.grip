"""Loc text that names a scope ([x.GetName]) whose event never saves it.

For every loc key used by an event, each [scope.Func] reference must be
saved in that event (save_scope_as / save_temporary_scope_as, or NAME = x on
the victim picker). Lines printed are candidates: the scope may legitimately
be saved upstream in a chain. The "saved in" column says where it is saved
anywhere in the system, for hand-checking.
"""
import collections
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aug_parse import (common_files, event_files, load_loc_keys, read, root_arg,
                       strip_comments_fast)


def event_bodies(root):
    bodies = {}
    for f in event_files(root):
        t = strip_comments_fast(read(f))
        for m in re.finditer(r"^(eotg_[a-z0-9_]+\.\d+)\s*=\s*\{", t, re.M):
            start = i = m.end()
            depth = 1
            while depth and i < len(t):
                depth += {"{": 1, "}": -1}.get(t[i], 0)
                i += 1
            bodies[m.group(1)] = (os.path.basename(f), t[start:i])
    return bodies


def main():
    root = root_arg(__doc__.splitlines()[0]).parse_args().root
    keys = load_loc_keys(root)
    bodies = event_bodies(root)

    saved_anywhere = collections.defaultdict(set)
    for f in event_files(root) + common_files(root):
        t = strip_comments_fast(read(f))
        base = os.path.basename(f)
        for m in re.finditer(r"save_(?:temporary_)?scope_as\s*=\s*([A-Za-z0-9_]+)", t):
            saved_anywhere[m.group(1)].add(base)
        for m in re.finditer(r"save_(?:temporary_)?scope_value_as\s*=\s*\{[^}]*name\s*=\s*([A-Za-z0-9_]+)", t):
            saved_anywhere[m.group(1)].add(base + " (value)")

    key_events = collections.defaultdict(set)
    for ev, (f, body) in bodies.items():
        for k in re.findall(r"\b(eotg_[a-z0-9_]+\.\d+\.[a-z0-9_.]+)", body):
            key_events[k].add(ev)

    for k, (line, txt) in keys.items():
        for scope in sorted(set(re.findall(r"\[([A-Za-z0-9_]+)\.", txt))):
            if scope == "ROOT":
                continue
            evs = key_events.get(k, set())
            pattern = r"(?:save_(?:temporary_)?scope_as|NAME)\s*=\s*" + scope + r"\b"
            if not any(re.search(pattern, bodies[e][1]) for e in evs):
                print(line, k, "scope", scope, "events", sorted(evs),
                      "saved in:", sorted(saved_anywhere.get(scope, [])))


if __name__ == "__main__":
    main()
