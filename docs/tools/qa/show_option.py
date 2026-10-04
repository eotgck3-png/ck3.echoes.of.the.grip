"""Print the script of one or more options by loc key, ai_chance removed.

Usage: python show_option.py [root] --key eotg_fracture.011.c --key eotg_aug_tier2.004.a
Handy for comparing an option's text with what it actually does.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aug_parse import read, root_arg, strip_comments_fast


def block(text, start):
    depth = 0
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return text[start:i + 1]
    return text[start:]


def main():
    p = root_arg(__doc__.splitlines()[0])
    p.add_argument("--key", action="append", required=True, help="option loc key (repeatable)")
    p.add_argument("--max-chars", type=int, default=1400)
    args = p.parse_args()
    src = {f: strip_comments_fast(read(f))
           for f in glob.glob(os.path.join(args.root, "events", "eotg_augmentation_*.txt"))}
    for key in args.key:
        for f, t in src.items():
            m = re.search(r"name\s*=\s*" + re.escape(key) + r"\b", t)
            if m:
                s = t.find("{", t.rfind("option", 0, m.start()))
                b = re.sub(r"ai_chance\s*=\s*\{(?:[^{}]|\{[^{}]*\})*\}", "", block(t, s))
                b = re.sub(r"\n\s*\n", "\n", b)
                print("=====", key, "(" + os.path.basename(f) + ")")
                print(b[:args.max_chars])
                break
        else:
            print("=====", key, "NOT FOUND")


if __name__ == "__main__":
    main()
