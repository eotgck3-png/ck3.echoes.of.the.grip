"""Check mod script against the CK3 engine vocabulary bundled with PX Toolkit.

PX Toolkit (VS Code extension jdeffner.px-toolkit) ships a script_docs dump of the
game's effects, triggers, event targets, modifiers and on_actions. This script uses
that dump plus the keys vanilla actually writes to flag names the engine would not
recognise -- the silent-failure class Tiger sometimes misses or buries.

A left-hand key is reported when it is none of:
  - an effect, trigger, event target, on_action or modifier in the PX dump
  - a key used anywhere on the left of `=` in vanilla common/ or events/
  - a top-level definition in the mod tree (scripted effects/triggers, events, ...)
References are also checked: event ids fired, traits, and modifiers named by
`modifier =` must be defined in vanilla or the mod.

Usage:
  python docs/tools/px_vocab_check.py <file-or-dir> [...]
Exit status is 1 when anything is reported.
"""

import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import textio  # noqa: E402

GAME = Path("D:/SteamLibrary/steamapps/common/Crusader Kings III/game")
PX = Path.home() / ".vscode/extensions"
MOD = Path(os.environ.get("EOTG_MOD_ROOT") or Path(__file__).resolve().parents[2])
CACHE = Path(os.environ.get("TEMP", "/tmp")) / "eotg_px_vanilla_keys.json"

KEY_RE = re.compile(r"(?<![\w.:$@])([A-Za-z_][\w]*)\s*(\?=|<=|>=|!=|==|=|<|>)")
TOP_RE = re.compile(r"^([A-Za-z_][\w.]*)\s*=\s*\{", re.M)
REF_RES = {
    "event": re.compile(r"\bid\s*=\s*([\w]+\.\d+)"),
    "trait": re.compile(r"\b(?:add_trait|remove_trait|add_trait_force_tooltip)\s*=\s*([A-Za-z_]\w*)"),
    # has_trait also accepts a group: "this trait or a trait of this trait group"
    "trait_or_group": re.compile(r"\bhas_trait\s*=\s*([A-Za-z_]\w*)"),
    "modifier": re.compile(r"\bmodifier\s*=\s*([A-Za-z_]\w*)"),
}


def strip_comments(text):
    out = []
    for line in text.splitlines():
        in_str = False
        for i, ch in enumerate(line):
            if ch == '"':
                in_str = not in_str
            elif ch == "#" and not in_str:
                line = line[:i]
                break
        out.append(line)
    return out


def read(path):
    return textio.read_text(path)[0]


def px_vocab():
    dirs = sorted(PX.glob("jdeffner.px-toolkit-*"))
    if not dirs:
        sys.exit("PX Toolkit not found under " + str(PX))
    docs = dirs[-1] / "data/ck3/script_docs"
    names, templates = set(), []
    for log in ("effects.log", "triggers.log", "event_targets.log"):
        names |= set(re.findall(r"^([a-z_][\w]*) - ", read(docs / log), re.M))
    hooks = set(re.findall(r"^([a-z_][\w]*):\s*$", read(docs / "on_actions.log"), re.M))
    names |= hooks
    for tag in re.findall(r"^Tag: (\S+)", read(docs / "modifiers.log"), re.M):
        if "$" in tag:
            templates.append(re.compile("^" + re.sub(r"\\\$\w+\\\$", r"\\w+", re.escape(tag)) + "$"))
        else:
            names.add(tag)
    return names, templates, hooks, dirs[-1].name


def definitions(root, sub):
    found = set()
    base = root / sub
    if base.exists():
        for f in base.rglob("*.txt"):
            found |= set(TOP_RE.findall("\n".join(strip_comments(read(f)))))
    return found


def trait_groups(root):
    found = set()
    base = root / "common/traits"
    if base.exists():
        for f in base.rglob("*.txt"):
            # `group_equivalence` makes has_trait accept the group too (vanilla: has_trait = lunatic
            # matches lunatic_1 / lunatic_genetic, used ~150 times).
            found |= set(re.findall(r"^\s*group(?:_equivalence)?\s*=\s*(\w+)", read(f), re.M))
    return found


def vanilla_index():
    if CACHE.exists():
        return {k: set(v) for k, v in json.loads(textio.read_text(CACHE)[0]).items()}
    keys = set()
    for sub in ("common", "events", "history"):
        for f in (GAME / sub).rglob("*.txt"):
            for line in strip_comments(read(f)):
                keys.update(m.group(1) for m in KEY_RE.finditer(line))
    index = {
        "keys": keys,
        "events": set(),
        "traits": definitions(GAME, "common/traits"),
        "groups": trait_groups(GAME),
        "on_actions": definitions(GAME, "common/on_action"),
        "modifiers": definitions(GAME, "common/modifiers")
        | definitions(GAME, "common/opinion_modifiers")
        | definitions(GAME, "common/static_modifiers"),
    }
    for f in (GAME / "events").rglob("*.txt"):
        index["events"] |= set(re.findall(r"^([\w]+\.\d+)\s*=", read(f), re.M))
    textio.write_text(str(CACHE), json.dumps({k: sorted(v) for k, v in index.items()}), bom=False)
    return index


def mod_index():
    mod = {
        "defs": set(),
        "events": set(),
        "traits": definitions(MOD, "common/traits"),
        "groups": trait_groups(MOD),
        "modifiers": definitions(MOD, "common/modifiers") | definitions(MOD, "common/opinion_modifiers"),
    }
    for sub in ("common", "events"):
        mod["defs"] |= definitions(MOD, sub)
    # Parameter names of the mod's own scripted effects/triggers ($AMOUNT$, $EXCLUDE$, ...)
    # appear as keys at their call sites: eotg_add_fracture_risk = { AMOUNT = 5 }.
    for sub in ("common/scripted_effects", "common/scripted_triggers"):
        for f in (MOD / sub).rglob("*.txt") if (MOD / sub).exists() else []:
            mod["defs"] |= set(re.findall(r"\$([A-Za-z_]\w*)\$", read(f)))
    for f in (MOD / "events").rglob("*.txt") if (MOD / "events").exists() else []:
        mod["events"] |= set(re.findall(r"^([\w]+\.\d+)\s*=", read(f), re.M))
    return mod


def main(targets):
    names, templates, hooks, px_name = px_vocab()
    van = vanilla_index()
    mod = mod_index()
    known = names | van["keys"] | mod["defs"]
    on_actions = hooks | van["on_actions"]
    pools = {
        "event": van["events"] | mod["events"],
        "trait": van["traits"] | mod["traits"],
        "trait_or_group": van["traits"] | mod["traits"] | van["groups"] | mod["groups"],
        "modifier": van["modifiers"] | mod["modifiers"],
    }
    problems = 0
    files = []
    for t in targets:
        p = Path(t)
        files += sorted(p.rglob("*.txt")) if p.is_dir() else [p]
    for f in files:
        lines = strip_comments(read(f))
        # A non-eotg_ top-level key in common/on_action extends a vanilla hook, so it must
        # be one the game fires. v1 hooked `on_yearly_playable` (named only in the .info
        # prose; the real hook is yearly_playable_pulse) and none of its events ever ran.
        if "on_action" in f.parts:
            for n, line in enumerate(lines, 1):
                m = TOP_RE.match(line)
                if m and not m.group(1).startswith("eotg_") and m.group(1) not in on_actions:
                    print(f"{f}:{n}: '{m.group(1)}' is not an engine or vanilla on_action")
                    problems += 1
        for n, line in enumerate(lines, 1):
            for m in KEY_RE.finditer(line):
                k = m.group(1)
                if k in known or k.isdigit() or any(t.match(k) for t in templates):
                    continue
                print(f"{f}:{n}: unknown key '{k}'")
                problems += 1
            for kind, rx in REF_RES.items():
                for ref in rx.findall(line):
                    if ref not in pools[kind]:
                        print(f"{f}:{n}: undefined {kind} '{ref}'")
                        problems += 1
    print(f"-- {len(files)} files, {problems} findings (engine vocab: {px_name})")
    return 1 if problems else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1:]))
