"""Spec-to-script conformance for the cybernetics specs. Python 3, standard library only.

    python docs/tools/spec_conformance.py              # write docs/qa/generated/spec_conformance.md
    python docs/tools/spec_conformance.py --check      # exit 1 if that file is stale
    python docs/tools/spec_conformance.py --json out.json [--root CHECKOUT] [--specs GLOB]

Automates checks 1-2 of docs/qa/cybernetics_spec_conformance_cloud.md:
  1. every backticked eotg_ identifier and event id in each spec
     (docs/specs/cybernetics_v2*.md) is extracted, classified (event, effect,
     trigger, modifier, opinion, flag, variable, decision, story, interaction,
     scheme, law, court position, ...) from its table's Type column, its
     heading, or its shape, and checked against the script: defined,
     referenced only, or missing;
  2. every mod definition in script (common/ top-level keys, events, flags,
     variables, saved scopes) that no spec mentions is listed.
A spec is "built" when any of its NEW events exists (its "New" identifier
section, else every event id it names). Unbuilt specs are reported apart.
Lines saying deferred / rejected / superseded / not built are exempt.
"""
import argparse
import collections
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import eotg_lint as L  # noqa: E402
import pdx_parse as P  # noqa: E402

DEFAULT_ROOT = os.path.dirname(os.path.dirname(HERE))
OUT_REL = "docs/qa/generated/spec_conformance.md"
SPEC_GLOB = "docs/specs/cybernetics_v2*.md"

EXEMPT_RE = re.compile(r"\b(deferred|rejected|superseded|not built)\b", re.I)
SPAN_RE = re.compile(r"`([^`]+)`")
TOKEN_RE = re.compile(r"(?<![\w/])(?:trait_track_|trait_)?eotg_[A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)*")
BRACE_RE = re.compile(r"(?<![\w/])((?:trait_track_|trait_)?eotg_[A-Za-z0-9_]*)\{([A-Za-z0-9_,\s]+)\}"
                      r"([A-Za-z0-9_]*)")
FILE_EXT_RE = re.compile(r"^\.(txt|yml|md|dds|gui|png|csv|mod)\b")
PLACEHOLDER_RE = re.compile(r"(^|_)[A-Z]+(_|$)")
EVENT_RE = re.compile(r"^eotg_\w+\.\d+$")
HEADING_RE = re.compile(r"^(#+)\s*(.*)$")
NEW_HEADING_RE = re.compile(r"^(?:[\d.]+\s*)?New\b", re.I)

# Type-column words -> kind (first match wins)
TYPE_WORDS = [
    ("scripted effect", "effect"), ("scripted trigger", "trigger"), ("script value", "script value"),
    ("opinion", "opinion"), ("modifier", "modifier"), ("flag", "flag"),
    ("saved scope", "scope"), ("scope", "scope"), ("variable", "variable"), ("char var", "variable"),
    ("decision", "decision"), ("story", "story"), ("interaction", "interaction"),
    ("scheme", "scheme"), ("law", "law"), ("court position", "court position"),
    ("on_action", "on_action"), ("namespace", "namespace"), ("event", "event"),
    ("trait", "trait"), ("loc", "loc"), ("template", "template"), ("death", "death reason"),
    ("activity", "activity"), ("building", "building"),
]
# heading words -> kind, for tables without a Type column
HEADING_WORDS = [("scripted triggers", "trigger"), ("scripted effects", "effect"),
                 ("modifiers", "modifier"), ("decisions", "decision"), ("opinion", "opinion")]
FOLDER_KIND = {"scripted_effects": "effect", "scripted_triggers": "trigger",
               "script_values": "script value", "modifiers": "modifier",
               "opinion_modifiers": "opinion", "decisions": "decision", "story_cycles": "story",
               "character_interactions": "interaction", "schemes": "scheme", "laws": "law",
               "law_groups": "law", "court_positions": "court position",
               "on_action": "on_action", "traits": "trait", "deathreasons": "death reason",
               "scripted_character_templates": "template", "activities": "activity",
               "buildings": "building"}


def shape_kind(tok):
    if EVENT_RE.match(tok):
        return "event"
    if "." in tok:
        return "loc"
    rules = [("eotg_flag_", "flag"), ("eotg_mod_", "modifier"), ("eotg_opinion_", "opinion"),
             ("eotg_story_", "story"), ("eotg_on_", "on_action"), ("eotg_death_", "death reason")]
    if tok.endswith(("_tt", "_desc", "_confirm", "_tooltip")):
        return "loc"
    for pre, kind in rules:
        if tok.startswith(pre):
            return kind
    if tok.startswith("eotg_decision_"):
        return "decision"
    for suf, kind in (("_effect", "effect"), ("_interaction", "interaction"), ("_trigger", "trigger"),
                      ("_value", "script value"), ("_court_position", "court position"),
                      ("_template", "template"), ("_scheme", "scheme"), ("_law", "law")):
        if tok.endswith(suf):
            return kind
    return None


def type_kind(text):
    t = text.lower()
    for word, kind in TYPE_WORDS:
        if word in t:
            return kind
    return None


# ------------------------------------------------------------------ spec parsing
class SpecId:
    __slots__ = ("token", "kind", "line", "exempt", "new")

    def __init__(self, token, kind, line, exempt, new):
        self.token, self.kind, self.line, self.exempt, self.new = token, kind, line, exempt, new


def _usable(tok):
    """False for prefixes (eotg_story_aug_), placeholders (eotg_aug_stress_X_effect)."""
    return not tok.endswith(("_", ".")) and not PLACEHOLDER_RE.search(tok.split(".")[0]) \
        and tok not in ("eotg", "eotg_")


def _normalise(tok, known=frozenset()):
    """`eotg_proc_surgeon.learning` (a scope used in loc) -> eotg_proc_surgeon.
    Kept whole when it is a known key or looks like an event-based loc key."""
    if "." not in tok or tok in known or re.match(r"^(?:trait_)?eotg_\w+\.\d", tok):
        return tok
    base, rest = tok.split(".", 1)
    if base in known or rest[:1].isupper():
        return base
    return tok


def expand_span(span, known=frozenset()):
    """eotg_ tokens in one backtick span, with {a,b} expanded; file paths skipped."""
    out = []
    for m in BRACE_RE.finditer(span):
        if FILE_EXT_RE.match(span[m.end():]) or "/" in span[:m.start()][-1:]:
            continue
        for alt in m.group(2).split(","):
            out.append(m.group(1) + alt.strip() + m.group(3))
    rest = BRACE_RE.sub(" ", span)
    for m in TOKEN_RE.finditer(rest):
        tok = m.group(0)
        ext = re.search(r"\.(txt|yml|md|dds|gui|png|csv|mod)$", tok)
        if ext or FILE_EXT_RE.match(rest[m.end():]):
            continue
        out.append(tok.rstrip("."))
    return [t for t in (_normalise(t, known) for t in out) if _usable(t)]


def resolve_shorthand(base, span, known):
    """`eotg_a_b_c`, `_d`: the key the suffix shorthand means, or None.
    Tries replacing the last segment, appending, then replacing more segments."""
    segs = base.split("_")
    cands = ["_".join(segs[:-1]) + span, base + span]
    cands += ["_".join(segs[:-k]) + span for k in range(2, max(2, len(segs) - 1))]
    for c in cands:
        if c in known:
            return c
    return None


def parse_spec(path, known=frozenset()):
    """([SpecId] in file order, one per occurrence; has a New section; [unresolved
    shorthand (line, text)])."""
    with open(path, encoding="utf-8-sig") as fh:
        lines = fh.read().splitlines()
    ids, unresolved = [], []
    heading, in_new, new_level = "", False, 0
    has_new = False
    header = None
    in_code = False
    for i, line in enumerate(lines, 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        h = HEADING_RE.match(line)
        if h:
            level, heading = len(h.group(1)), h.group(2).strip()
            if in_new and level <= new_level:
                in_new = False
            if NEW_HEADING_RE.match(heading):
                in_new, new_level, has_new = True, level, True
            header = None
            continue
        cells = None
        type_idx = key_idx = None
        if line.lstrip().startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            if header is None:
                header = [c.lower() for c in cells]
                continue
            type_idx = header.index("type") if "type" in header else None
            key_idx = header.index("key") if "key" in header else None
        else:
            header = None
            cells = [line]
        exempt = bool(EXEMPT_RE.search(line))
        head_kind = next((k for w, k in HEADING_WORDS if w in heading.lower()), None)
        row_type = type_kind(cells[type_idx]) if type_idx is not None and \
            type_idx < len(cells) else None
        row_type_text = cells[type_idx].lower() if row_type else ""
        prev = None
        for ci, cell in enumerate(cells):
            is_key = key_idx is None or ci == key_idx
            for span in SPAN_RE.findall(cell):
                if prev and re.match(r"^_[A-Za-z0-9_]+$", span):
                    tok = resolve_shorthand(prev, span, known)
                    if tok is None:
                        unresolved.append((i, "`%s` + `%s`" % (prev, span)))
                        continue
                    toks = [tok]
                else:
                    toks = expand_span(span, known)
                    if toks:
                        prev = toks[-1]
                for tok in toks:
                    kind = shape_kind(tok)
                    if kind not in ("event", "loc") or (row_type == "event" and is_key):
                        kind = (row_type if is_key else None) or kind or head_kind
                    new = in_new and is_key and "existing event" not in row_type_text
                    ids.append(SpecId(tok, kind, i, exempt, new))
    return ids, has_new, unresolved
def spec_text_tokens(paths, known=frozenset()):
    """Every eotg_ token and short event form mentioned anywhere in the specs."""
    toks = set()
    for p in paths:
        with open(p, encoding="utf-8-sig") as fh:
            text = fh.read()
        for span in SPAN_RE.findall(text):
            toks.update(expand_span(span, known))
        toks.update(_normalise(t.rstrip("."), known) for t in TOKEN_RE.findall(text))
        for m in re.finditer(r"\b([a-z][a-z0-9]*)\.(\d{3,4})\b", text):
            toks.add("short:%s.%s" % (m.group(1), m.group(2)))
    return toks


def short_event(eid):
    ns, num = eid.rsplit(".", 1)
    for pre in ("eotg_aug_", "eotg_"):
        if ns.startswith(pre):
            return "short:%s.%s" % (ns[len(pre):], num)
    return None


# ------------------------------------------------------------------ script index
class Script:
    def __init__(self, root):
        self.mod = L.Mod(root)
        self.defined = {}            # token -> kind
        for rel, doc in sorted(self.mod.docs.items()):
            if rel.startswith("common/"):
                folder = rel.split("/")[1]
                kind = FOLDER_KIND.get(folder, folder)
                for n in doc.nodes:
                    if n.is_block and n.key and n.key.startswith("eotg_"):
                        self.defined.setdefault(n.key, kind)
            for n, _ in P.walk(doc.nodes):
                if rel.startswith("events/") and n.key == "namespace" and isinstance(n.value, str):
                    self.defined.setdefault(n.value, "namespace")
                name, kind = None, None
                if n.key and L.FLAG_SETTERS.match(n.key) and n.key.startswith(("add_", "set_")):
                    kind = "flag"
                    name = n.value if isinstance(n.value, str) else None
                    if n.is_block:
                        f = P.first(n.value, "flag")
                        name = f.value if f is not None and isinstance(f.value, str) else None
                elif n.key in L.VAR_SETTERS:
                    kind = "variable"
                    f = P.first(n.value, "name") if n.is_block else None
                    name = f.value if f is not None else n.value if isinstance(n.value, str) \
                        else None
                elif n.key in ("save_scope_as", "save_temporary_scope_as"):
                    kind, name = "scope", n.value if isinstance(n.value, str) else None
                elif n.key in ("save_scope_value_as", "save_temporary_scope_value_as") \
                        and n.is_block:
                    f = P.first(n.value, "name")
                    kind = "scope"
                    name = f.value if f is not None and isinstance(f.value, str) else None
                if isinstance(name, str) and name.startswith("eotg_"):
                    self.defined.setdefault(name, kind)
        for _, eid, _ in self.mod.events():
            self.defined[eid] = "event"
        self.loc = set()
        for rel, line, key, value in L.iter_loc_values(self.mod):
            self.loc.add(key)
        self.tokens = set()
        for top in ("common", "events", "localization", "history", "gfx"):
            for f in L._iter_files(self.mod.root, top, (".txt", ".yml", ".gui")):
                text, _ = P.read_text(f)
                self.tokens.update(t.rstrip(".") for t in TOKEN_RE.findall(text))

    def status(self, tok, kind):
        if kind == "loc":
            return "defined" if tok in self.loc else (
                "referenced" if tok in self.tokens else "missing")
        if tok in self.defined or (tok in self.loc and kind is None):
            return "defined"
        if tok in self.tokens:
            return "referenced"
        return "missing"


# ------------------------------------------------------------------ analysis
def analyse(root, spec_glob=SPEC_GLOB):
    paths = sorted(glob.glob(os.path.join(root, *spec_glob.split("/"))))
    script = Script(root)
    known = set(script.defined) | script.loc | script.tokens
    specs = []
    for p in paths:
        ids, has_new, unresolved = parse_spec(p, known)
        rel = os.path.relpath(p, root).replace(os.sep, "/")
        by_tok = collections.OrderedDict()
        for sid in ids:
            e = by_tok.setdefault(sid.token, {"token": sid.token, "kind": None, "lines": [],
                                              "exempt_lines": [], "new": False})
            if sid.kind and not e["kind"]:
                e["kind"] = sid.kind
            (e["exempt_lines"] if sid.exempt else e["lines"]).append(sid.line)
            e["new"] = e["new"] or sid.new
        new_events = [t for t, e in by_tok.items() if (e["kind"] == "event") and
                      (e["new"] or not has_new) and e["lines"]]
        built = (not new_events) or any(t in script.defined for t in new_events)
        rows = []
        for tok, e in by_tok.items():
            kind = e["kind"] or script.defined.get(tok) or "unknown"
            rows.append({"token": tok, "kind": kind,
                         "status": script.status(tok, e["kind"]),
                         "line": (e["lines"] or e["exempt_lines"])[0],
                         "exempt": not e["lines"]})
        specs.append({"spec": rel, "built": built, "new_events": new_events,
                      "has_new_section": has_new, "ids": rows,
                      "unresolved_shorthand": ["l.%d: %s" % u for u in unresolved]})
    # a *_lore.md spec is built when its parent spec is
    by_name = {s["spec"]: s for s in specs}
    for s in specs:
        parent = by_name.get(s["spec"].replace("_lore.md", ".md"))
        if parent is not None and parent is not s:
            s["built"] = parent["built"]
            s["built_from"] = parent["spec"]
    mentioned = spec_text_tokens(paths, known)
    unmentioned = collections.defaultdict(list)
    for tok, kind in sorted(script.defined.items()):
        if tok in mentioned or (kind == "event" and short_event(tok) in mentioned):
            continue
        unmentioned[kind].append(tok)
    return {"specs": specs, "unmentioned": {k: v for k, v in sorted(unmentioned.items())}}


# ------------------------------------------------------------------ rendering
def _ids(rows):
    return ", ".join("`%s` (%s, l.%d)" % (r["token"], r["kind"], r["line"]) for r in rows)


def render(res):
    out = ["# Spec conformance: cybernetics specs vs script (generated)", "",
           "> **Generated by `docs/tools/spec_conformance.py`. Do not edit by hand.** "
           "`python docs/tools/spec_conformance.py --check` says whether this file is current.",
           "",
           "Automates checks 1–2 of `docs/qa/cybernetics_spec_conformance_cloud.md`. Each "
           "backticked `eotg_` identifier or event id in `docs/specs/cybernetics_v2*.md` is "
           "looked up in the script:",
           "- **present**: defined (a `common/` key, an event, a namespace, a flag or variable "
           "that is set, a saved scope, or a loc key);",
           "- **referenced only**: it appears in script or loc, but nothing defines or sets it "
           "(for a flag: read, never set);",
           "- **missing**: it appears nowhere in script or loc.",
           "",
           "A spec is **built** when any of its new events exists (the events in its \"New\" "
           "identifier section, else every event it names). Unbuilt specs are listed apart, so "
           "their expected gaps don't hide the real ones. Lines that say *deferred*, "
           "*rejected*, *superseded* or *not built* are **exempt**. The kind comes from the "
           "table's Type column, the heading, or the identifier's shape (then from where the "
           "script defines it); `unknown` when none applies.", "",
           "## Summary", "",
           "| Spec | Built | Ids | Present | Referenced only | Missing | Exempt |",
           "|---|---|---|---|---|---|---|"]
    for s in res["specs"]:
        rows = [r for r in s["ids"] if not r["exempt"]]
        c = collections.Counter(r["status"] for r in rows)
        out.append("| `%s` | %s | %d | %d | %d | %d | %d |" % (
            s["spec"].split("/")[-1], "yes" if s["built"] else "**no**", len(s["ids"]),
            c["defined"], c["referenced"], c["missing"], len(s["ids"]) - len(rows)))
    for title, want in (("Built specs: gaps", True), ("Unbuilt specs (expected gaps)", False)):
        out += ["", "## %s" % title, ""]
        any_spec = False
        for s in res["specs"]:
            if s["built"] != want:
                continue
            any_spec = True
            rows = [r for r in s["ids"] if not r["exempt"]]
            miss = [r for r in rows if r["status"] == "missing"]
            ref = [r for r in rows if r["status"] == "referenced"]
            ex = [r for r in s["ids"] if r["exempt"]]
            present = sum(1 for r in rows if r["status"] == "defined")
            out.append("### `%s`" % s["spec"])
            out.append("")
            if not want:
                out.append("- New events, none in script yet: %s" % (
                    ", ".join("`%s`" % e for e in s["new_events"]) or "none"))
            out.append("- Specced and present: %d" % present)
            out.append("- Specced, missing from script (%d): %s" % (len(miss), _ids(miss) or "none"))
            out.append("- Referenced only, never defined or set (%d): %s" % (
                len(ref), _ids(ref) or "none"))
            out.append("- Exempt (%d): %s" % (len(ex), _ids(ex) or "none"))
            if s["unresolved_shorthand"]:
                out.append("- Suffix shorthand that matches no key (%d, not counted): %s" % (
                    len(s["unresolved_shorthand"]), "; ".join(s["unresolved_shorthand"])))
            out.append("")
        if not any_spec:
            out.append("None.")
    out += ["## In script, mentioned in no spec", "",
            "Mod definitions (`common/` top-level keys, events, namespaces, flags and variables "
            "that are set, saved scopes) that no `cybernetics_v2*` spec names. An event also "
            "counts as mentioned by its short form (`tier1.005`).", ""]
    if not res["unmentioned"]:
        out.append("None.")
    for kind, toks in res["unmentioned"].items():
        out.append("- **%s** (%d): %s" % (kind, len(toks), ", ".join("`%s`" % t for t in toks)))
    out.append("")
    return "\n".join(out)


def main(argv=None):
    P.utf8_console()
    ap = argparse.ArgumentParser(description="Cybernetics spec vs script conformance.")
    ap.add_argument("--root", default=DEFAULT_ROOT, help="mod checkout (default: this repo)")
    ap.add_argument("--specs", default=SPEC_GLOB, help="spec glob, relative to --root")
    ap.add_argument("--out", help="output file (default: <root>/%s)" % OUT_REL)
    ap.add_argument("--check", action="store_true", help="exit 1 if the output file is stale")
    ap.add_argument("--json", metavar="FILE", help="also write the analysis as JSON")
    args = ap.parse_args(argv)
    root = os.path.abspath(args.root)
    out = os.path.abspath(args.out) if args.out else os.path.join(root, *OUT_REL.split("/"))
    res = analyse(root, args.specs)
    text = render(res)
    if args.json:
        with open(args.json, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(res, fh, indent=1)
            fh.write("\n")
    if args.check:
        cur = ""
        if os.path.exists(out):
            with open(out, "rb") as fh:
                cur = fh.read().decode("utf-8").replace("\r\n", "\n")
        ok = cur == text
        built = [x for x in res["specs"] if x["built"]]
        gaps = sum(1 for x in built for r in x["ids"] if not r["exempt"] and r["status"] == "missing")
        print("spec conformance report %s: %d spec(s), %d built, %d missing id(s) in built "
              "specs (%s)" % ("is current" if ok else "is STALE", len(res["specs"]), len(built),
                              gaps, out))
        return 0 if ok else 1
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    built = [s for s in res["specs"] if s["built"]]
    gaps = sum(1 for s in built for r in s["ids"] if not r["exempt"] and r["status"] == "missing")
    print("wrote %s: %d spec(s), %d built, %d missing id(s) in built specs"
          % (out, len(res["specs"]), len(built), gaps))
    return 0


if __name__ == "__main__":
    sys.exit(main())
