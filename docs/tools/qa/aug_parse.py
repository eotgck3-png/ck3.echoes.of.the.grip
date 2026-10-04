"""Shared parser for the cybernetics (augmentation) QA scripts.

A small Paradox-script reader: strips comments, tokenizes and nests blocks
into lists of (key, operator, value) tuples, where value is a string or a
nested list. Good enough for counting and graph walks; not a validator.
Tiger remains the authority on syntax.
"""
import argparse
import collections
import glob
import os
import re

PERS = (
    "lustful chaste gluttonous temperate greedy generous lazy diligent wrathful "
    "calm patient impatient arrogant humble deceitful honest craven brave shy "
    "gregarious ambitious content arbitrary just cynical zealous paranoid trusting "
    "compassionate callous sadistic stubborn fickle eccentric vengeful forgiving"
).split()

LOC_FILE = "localization/english/eotg_augmentation_l_english.yml"


def root_arg(description):
    """Argument parser with the repo root as an optional positional (default: cwd)."""
    p = argparse.ArgumentParser(description=description)
    p.add_argument("root", nargs="?", default=".",
                   help="path to the mod repo root (default: current directory)")
    return p


def event_files(root):
    return sorted(glob.glob(os.path.join(root, "events", "eotg_augmentation_*.txt")))


def common_files(root):
    return sorted(glob.glob(os.path.join(root, "common", "*", "eotg_augmentation_*.txt")))


def read(path):
    with open(path, encoding="utf-8-sig") as fh:
        return fh.read()


def strip_comments(text):
    """Remove # comments that are not inside double quotes."""
    out = []
    for line in text.split("\n"):
        quoted = False
        res = ""
        for ch in line:
            if ch == '"':
                quoted = not quoted
            if ch == "#" and not quoted:
                break
            res += ch
        out.append(res)
    return "\n".join(out)


def strip_comments_fast(text):
    """Cruder comment strip (ignores quotes); fine for key/scope scans."""
    return re.sub(r"#[^\n]*", "", text)


def _parse(tokens, i=0):
    items = []
    while i < len(tokens):
        tok = tokens[i]
        if tok == "}":
            return items, i + 1
        if tok == "{":
            v, i = _parse(tokens, i + 1)
            items.append((None, None, v))
            continue
        if i + 1 < len(tokens) and tokens[i + 1] in ("=", "<", ">", "<=", ">=", "!=", "?="):
            op = tokens[i + 1]
            if i + 2 < len(tokens) and tokens[i + 2] == "{":
                v, i = _parse(tokens, i + 3)
                items.append((tok, op, v))
            else:
                items.append((tok, op, tokens[i + 2] if i + 2 < len(tokens) else None))
                i += 3
        else:
            items.append((tok, None, None))
            i += 1
    return items, i


def load(path):
    """Parse one script file into nested (key, op, value) tuples."""
    t = strip_comments(read(path)).replace("?=", " ?= ")
    toks = re.findall(r'"[^"]*"|[{}]|\?=|[<>!=]=|[<>=]|[^\s{}<>=!?"]+', t)
    return _parse(toks)[0]


def walk(items):
    """Depth-first over every (key, op, value) in a parsed block."""
    for k, op, v in items:
        yield k, op, v
        if isinstance(v, list):
            yield from walk(v)


def find(items, key):
    """Values of the direct children named key."""
    return [v for k, op, v in items if k == key]


def load_events(root):
    """{event_id: (file_basename, parsed_body)} for every augmentation event."""
    events = {}
    for f in event_files(root):
        for k, op, v in load(f):
            if k and isinstance(v, list) and re.match(r"eotg_.*\.\d+$", k):
                events[k] = (os.path.basename(f), v)
    return events


def short_file(basename):
    return basename.replace("eotg_augmentation_", "").replace(".txt", "")


def load_loc_keys(root):
    """OrderedDict key -> (line_no, text) from the cybernetics loc file."""
    keys = collections.OrderedDict()
    kre = re.compile(r'^ ([A-Za-z0-9_.\-]+):(\d+)? "(.*)"\s*(#.*)?$')
    with open(os.path.join(root, LOC_FILE), encoding="utf-8-sig") as fh:
        for i, line in enumerate(fh, 1):
            m = kre.match(line.rstrip("\r\n"))
            if m:
                keys[m.group(1)] = (i, m.group(3))
    return keys
