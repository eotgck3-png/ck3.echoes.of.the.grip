"""Events with two or fewer options, and hidden-roll options per file.

A hidden-roll option is one with a hidden_effect containing random or
random_list: the "implant decides" pattern, where the result is not shown.
"""
import collections
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aug_parse import find, load_events, root_arg, walk


def main():
    root = root_arg(__doc__.splitlines()[0]).parse_args().root
    events = load_events(root)
    print("events with <= 2 options:")
    for eid, (f, body) in events.items():
        n = len(find(body, "option"))
        if n <= 2:
            print(" ", eid, n)
    hidden = collections.Counter()
    for eid, (f, body) in events.items():
        for o in find(body, "option"):
            for k, oo, v in o:
                if k == "hidden_effect" and isinstance(v, list) and \
                        any(kk in ("random_list", "random") for kk, _, _ in walk(v)):
                    hidden[f] += 1
    print("hidden-roll options by file:", dict(hidden))


if __name__ == "__main__":
    main()
