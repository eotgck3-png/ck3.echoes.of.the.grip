"""Event reachability and loc coverage from PX Toolkit's own analysis.

Reads the JSON that `px_lsp_diagnostics.js --request=eventGraph --request=locCoverage`
writes (PX's Event Graph panel data and its localization coverage), and reports:
  - mod events that no hook can reach (walking edges from every non-event root:
    on_actions, decisions, story cycles, ...); CLAUDE.md invariant 4
  - missing loc keys, limited to eotg_ identifiers by default

Usage:
  ELECTRON_RUN_AS_NODE=1 ".../Code.exe" docs/tools/px_lsp_diagnostics.js events \
      --request=eventGraph --request=locCoverage --out=<dir>
  python docs/tools/px_event_report.py <dir> [--all-loc] [--root CHECKOUT]
--root is the mod checkout the JSON was made from (default: the repo holding this
script); its script supplies the variable / scope / flag names PX wrongly asks loc for.
Exit status 1 when an event is unreachable or an eotg_ loc key is missing.
"""

import argparse
import collections
import re
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import pdx_parse  # noqa: E402  (utf8_console)

DEFAULT_ROOT = Path(__file__).resolve().parents[2]


# PX asks for loc it does not need: building mesh asset names, and variable names it assumes
# are displayed. eotg_fracture_risk is hidden by design (spec cybernetics_track.md Q1).
KNOWN_BENIGN = re.compile(r"(_mesh$|^eotg_fracture_risk$)")


def main(out_dir, all_loc, root=None):
    d = Path(out_dir)
    graph = json.loads((d / "px_eventGraph.json").read_text(encoding="utf-8"))
    nodes = {n["id"]: n for n in graph["nodes"]}
    edges = collections.defaultdict(set)
    incoming = collections.defaultdict(set)
    for e in graph["edges"]:
        edges[e["from"]].add(e["to"])
        incoming[e["to"]].add(e["from"])

    # PX's graph has no story-cycle edges (story cycles fire events from effect_group
    # blocks), and omits events reached only that way. So: take the event list from the
    # event files, and treat every story cycle that some mod script starts with
    # `create_story` as a root whose events are reached.
    mod_root = Path(root).resolve() if root else DEFAULT_ROOT
    def strip(text):
        return "\n".join(l.split("#", 1)[0] for l in text.splitlines())
    script = {f: strip(f.read_text(encoding="utf-8-sig", errors="replace"))
              for sub in ("common", "events") for f in (mod_root / sub).rglob("*.txt")}
    defined = {}
    for f, text in script.items():
        if "events" in f.parts:
            for m in re.finditer(r"^([\w]+\.\d+)\s*=\s*\{", text, re.M):
                defined[m.group(1)] = (f, text[:m.start()].count("\n") + 1)
    created = {m for text in script.values() for m in re.findall(r"create_story\s*=\s*\{?\s*(?:type\s*=\s*)?(\w+)", text)}
    story_roots, unstarted = set(), []
    for f, text in script.items():
        if "story_cycles" not in f.parts:
            continue
        for m in re.finditer(r"^(\w+)\s*=\s*\{", text, re.M):
            story = m.group(1)
            nxt = re.search(r"^\w+\s*=\s*\{", text[m.end():], re.M)
            body = text[m.end(): m.end() + nxt.start()] if nxt else text[m.end():]
            fired = set(re.findall(r"\bid\s*=\s*([\w]+\.\d+)", body))
            if story in created:
                story_roots |= fired
            else:
                unstarted.append(story)
    name_re = (r"(?:set_variable|change_variable|remove_variable|has_variable|set_local_variable|"
               r"save_scope_as|save_temporary_scope_as|save_scope_value_as|save_temporary_scope_value_as|"
               r"add_character_flag|has_character_flag|remove_character_flag|add_to_variable_list)"
               r"\s*=\s*(?:\{[^}]*?(?:name|flag)\s*=\s*)?(\w+)")
    script_names = {n for text in script.values() for n in re.findall(name_re, text)}
    script_names |= {n for text in script.values() for n in re.findall(r"\b(?:var|scope|local_var|flag):(\w+)", text)}

    for story in unstarted:
        print(f"!! story cycle {story} is never started (no create_story); its events count as unreached")

    # Anything that is not an event is a hook the game or the player drives.
    reach, stack = set(), [n for n, v in nodes.items() if v["kind"] != "event"] + sorted(story_roots)
    while stack:
        x = stack.pop()
        if x not in reach:
            reach.add(x)
            stack.extend(edges[x])

    events = sorted(set(defined) | {n for n, v in nodes.items() if v["kind"] == "event" and v.get("source") == "mod"})
    dead = [e for e in events if e not in reach]
    problems = 0
    if graph.get("truncated"):
        print("!! PX truncated the event graph; reachability is incomplete")
    if story_roots:
        print(f"-- {len(story_roots)} events reached from started story cycles (outside PX's graph)")
    for e in dead:
        n = nodes.get(e) or {"file": defined[e][0], "line": defined[e][1]}
        print(f"{n.get('file')}:{n.get('line')}: event {e} is unreachable "
              f"(fired by: {', '.join(sorted(incoming[e])) or 'nothing'})")
        problems += 1
    print(f"-- {len(events)} mod events, {len(events) - len(dead)} reachable, {len(dead)} unreachable "
          f"({collections.Counter(v['kind'] for v in nodes.values())})")

    cov_file = d / "px_locCoverage.json"
    if cov_file.exists():
        for lang in json.loads(cov_file.read_text(encoding="utf-8")):
            # PX's coverage scan walks every subfolder, including the frozen v1 tree; its
            # definition index does not, so only the coverage needs filtering.
            # PX also asks for loc on names the mod only uses as variables, saved scopes or
            # flags (eotg_aug_escrow, eotg_scrambled_into, ...). Those are never displayed.
            live = [m for m in lang["missing"]
                    if "OLD PROJECT VERSION" not in m["file"] and not KNOWN_BENIGN.search(m["key"])
                    and m["key"] not in script_names]
            lang["missing"] = live
            missing = [m for m in live if all_loc or m["key"].startswith(("eotg_", "trait_eotg_"))]
            for m in missing:
                print(f"{m['file']}:{m['line']}: missing {lang['language']} loc '{m['key']}'")
            problems += len(missing)
            print(f"-- loc {lang['language']}: {lang['defined']} defined, {len(missing)} missing"
                  f"{'' if all_loc else ' (eotg_ keys)'}, {len(lang['missing'])} missing in total")
    return 1 if problems else 0


def cli(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("out_dir", help="where px_lsp_diagnostics.js wrote its JSON")
    ap.add_argument("--all-loc", action="store_true", help="report every missing key, not only eotg_")
    ap.add_argument("--root", default=None, help="the mod checkout the JSON describes")
    a = ap.parse_args(argv)
    pdx_parse.utf8_console()
    return main(a.out_dir, a.all_loc, a.root)


if __name__ == "__main__":
    sys.exit(cli())
