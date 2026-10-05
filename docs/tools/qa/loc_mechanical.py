"""Mechanical check of the cybernetics loc file against the script.

Checks BOM, header, line shape, tabs, version numbers, unescaped inner quotes,
duplicate keys (in the file and across localization/), keys referenced by
script but missing, implied keys missing (decision _desc/_tooltip/_confirm,
modifier _desc, opinion, death reason, trait name/desc), unused keys, and
unresolved $KEY$ references. Reports "missing" hits for set_variable /
save_scope_value_as `name =` arguments too; those are false positives.
"""
import collections
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from aug_parse import (LOC_FILE, common_files, event_files, read, root_arg,
                       strip_comments_fast)
import textio  # noqa: E402  (aug_parse put docs/tools on sys.path)

FIELD_RE = re.compile(
    r"\b(title|desc|name|custom_tooltip|text|tooltip|confirm_text|selection_tooltip|"
    r"custom_description|custom_description_no_bullet|first_valid_desc|triggered_desc|"
    r"subject|opening|reason|fallback|flavor|confirm|effect_tooltip)\s*=\s*\"?([A-Za-z0-9_.\-]+)\"?")
SKIP = {"yes", "no", "root", "prev", "this"}


def top_keys(path):
    return re.findall(r"^([a-z][A-Za-z0-9_]*)\s*=\s*\{", strip_comments_fast(read(path)), re.M)


def main():
    root = root_arg(__doc__.splitlines()[0]).parse_args().root
    loc = os.path.join(root, LOC_FILE)
    with open(loc, "rb") as fh:
        raw = fh.read()
    print("BOM", raw[:3] == b"\xef\xbb\xbf")
    lines = textio.decode(raw)[0].split("\n")
    print("header", repr(lines[0]))

    keys = collections.OrderedDict()
    dups = []
    kre = re.compile(r'^ ([A-Za-z0-9_.\-]+):(\d+)? "(.*)"\s*(#.*)?$')
    for i, line in enumerate(lines[1:], 2):
        l2 = line.rstrip("\r")
        if "\t" in l2:
            print("TAB", i)
        if not l2.strip() or l2.strip().startswith("#"):
            continue
        m = kre.match(l2)
        if not m:
            print("BADSHAPE", i, l2[:120])
            continue
        k, num, txt = m.group(1), m.group(2), m.group(3)
        if num is None:
            print("NOVERSION", i, k)
        if re.search(r'(?<!\\)"', txt):
            print("INNERQUOTE", i, k, txt[:80])
        if k in keys:
            dups.append((k, keys[k][0], i))
        keys[k] = (i, txt)
    print("keys", len(keys), "duplicates in file", dups)

    tree = collections.defaultdict(list)
    for f in glob.glob(os.path.join(root, "localization", "**", "*.yml"), recursive=True):
        for i, line in enumerate(textio.read_lines(f), 1):
            m = re.match(r'^\s+([A-Za-z0-9_.\-]+):\d* "', line)
            if m:
                tree[m.group(1)].append((os.path.basename(f), i))
    print("duplicates across localization/", [(k, v) for k, v in tree.items() if len(v) > 1])

    files = event_files(root) + common_files(root)
    text = {f: read(f) for f in files}
    refs = collections.defaultdict(set)
    for f, t in text.items():
        for m in FIELD_RE.finditer(strip_comments_fast(t)):
            v = m.group(2)
            if v in SKIP or v.startswith(("scope", "flag")):
                continue
            refs[v].add(os.path.basename(f))

    implied = collections.defaultdict(set)
    common = os.path.join(root, "common")
    for k in top_keys(os.path.join(common, "decisions", "eotg_augmentation_decisions.txt")):
        for s in ("", "_desc", "_tooltip", "_confirm"):
            implied[k + s].add("decision")
    for k in top_keys(os.path.join(common, "modifiers", "eotg_augmentation_modifiers.txt")):
        implied[k].add("modifier")
        implied[k + "_desc"].add("modifier desc")
    for k in top_keys(os.path.join(common, "opinion_modifiers", "eotg_augmentation_opinions.txt")):
        implied[k].add("opinion")
    deaths = os.path.join(common, "deathreasons", "eotg_augmentation_deaths.txt")
    if os.path.exists(deaths):
        for k in top_keys(deaths):
            implied[k].add("death")
    for k in top_keys(os.path.join(common, "traits", "eotg_augmentation_traits.txt")):
        implied["trait_" + k].add("trait")
        implied["trait_" + k + "_desc"].add("trait desc")

    print("\nMISSING (referenced by script):")
    for k in sorted(refs):
        if k not in keys and not k.isdigit():
            print(" ", k, sorted(refs[k]))
    print("\nMISSING (implied):")
    for k in sorted(implied):
        if k not in keys:
            print(" ", k, sorted(implied[k]))

    tokens = set()
    for t in text.values():
        tokens |= set(re.findall(r"[A-Za-z0-9_.\-]+", strip_comments_fast(t)))
    dollar = set()
    for k, (i, txt) in keys.items():
        dollar |= set(re.findall(r"\$([A-Za-z0-9_.\-]+)\$", txt))
    print("\nUNUSED (defined, never referenced):")
    for k, (i, txt) in keys.items():
        if k not in tokens and k not in implied and k not in dollar:
            print(" ", i, k)
    print("\n$KEY$ unresolved:", [x for x in dollar if x not in keys and x not in tree])


if __name__ == "__main__":
    main()
