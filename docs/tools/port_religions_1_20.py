"""Port v1 (CK3 1.19) religion files to the CK3 1.20 schema, into a staging folder.

    python docs/tools/port_religions_1_20.py [--src DIR] [--out DIR] [--check]

Input  (default): OLD PROJECT VERSION/common/religion/{religion_types,religion_family_types}
Output (default): docs/port/religion_1_20/common/religion/{religion_types,faith_types,
                  religion_family_types}  +  docs/port/religion_1_20/PORT_REPORT.md
Never writes to the live common/. Standard library only; output is deterministic
(same input -> byte-identical output). --check exits 1 if the staged output is stale.

Conversions (target shape: docs/qa/v1_lift_readiness_cloud.md §6, vanilla 1.20.0.3):
  religion   family / graphical_faith / piety_icon_group -> religion_details = { }
             religion-level `doctrine = x` lines, traits, localization: kept as they are
  faith      nested faiths = { } -> faith_types/<file>.txt, one top-level block each,
             with faith_details = { religion = <parent> color icon reformed_icon
             graphical_faith }; `doctrine = tenet_*` -> tenets = { },
             other `doctrine = x` -> doctrines = { }; tenet_monasticism ->
             doctrine_monasticism_encouraged (in doctrines)
  family     doctrine_background_icon = x.dds -> tenet_background_icon = x  (+ TODO for
             the _heretical_ / _neutral_ / _unknown_ siblings)
  dropped    eotg_religion_stampede (Nikios Khanate, deferred; CLAUDE.md invariant 9)
Every top-level block gets `# STOPGAP: replace from briefs`; comments are kept
where they attach to a node that survives.
"""
import argparse
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pdx_parse as P  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
DEFAULT_SRC = os.path.join(REPO, "OLD PROJECT VERSION", "common", "religion")
DEFAULT_OUT = os.path.join(REPO, "docs", "port", "religion_1_20")

STOPGAP = "# STOPGAP: replace from briefs"
DROP_RELIGIONS = {"eotg_religion_stampede": "Nikios Khanate content is deferred "
                                            "(CLAUDE.md invariant 9; owner decision)"}
RELIGION_DETAIL_KEYS = ("family", "graphical_faith", "piety_icon_group")
FAITH_DETAIL_KEYS = ("color", "icon", "reformed_icon", "graphical_faith")
DOCTRINE_RENAMES = {"tenet_monasticism": "doctrine_monasticism_encouraged"}
FAMILY_ICON_SIBLINGS = ("tenet_heretical_background_icon", "tenet_neutral_background_icon",
                        "tenet_unknown_background_icon")

UNVERIFIED = [
    "Religion-level `doctrine = x` lines are still valid in 1.20 as single lines "
    "(only the faith level was confirmed to use `tenets = { }` / `doctrines = { }` lists).",
    "Families keep `graphical_faith`, `piety_icon_group` and `hostility_doctrine` "
    "unchanged; only `doctrine_background_icon` was confirmed renamed.",
    "`tenet_background_icon` takes the v1 file name without `.dds` "
    "(`core_tenet_banner_christian`); vanilla 1.20 keys may be named `tenet_banner_*`. "
    "Check against game/common/religion/religion_family_types/.",
    "`faith_details = { religion = ... }` is the only required field; `color` moved inside "
    "it with no change of format (`{ r g b }` in 0-1 floats).",
    "Religion `traits = { virtues sins }` and `localization = { }` keep their 1.19 shape "
    "in 1.20.",
    "A faith with no `icon` falls back to a default icon rather than failing to load.",
    "`doctrine_monasticism_encouraged` is the right replacement for `tenet_monasticism` "
    "(`doctrine_types/20_doctrines.txt:2071` lists encouraged/accepted/absent/forbidden).",
]


def _node(key, value, op="=", comments=None, trailing=None, quoted=False):
    n = P.Node(key, op, value, 0, quoted=quoted)
    n.comments = list(comments or [])
    n.trailing = trailing
    return n


def _bare(key):
    return P.Node(key, None, None, 0)


def _comment_block(texts):
    n = P.Node("#", None, None, 0)
    n.comments = list(texts)
    return n


def _is_comment_node(n):
    return n.key == "#" and n.op is None and n.value is None


def _stopgap(node):
    if STOPGAP not in node.comments:
        node.comments = node.comments + [STOPGAP]


class Report:
    def __init__(self):
        self.lines = []
        self.todos = []
        self.dropped = []

    def add(self, section, text):
        self.lines.append((section, text))

    def todo(self, where, text):
        self.todos.append((where, text))


# ------------------------------------------------------------------ families
def port_family(fam, rep):
    out = []
    for c in fam.value:
        if c.key == "doctrine_background_icon" and isinstance(c.value, str):
            val = c.value[:-4] if c.value.lower().endswith(".dds") else c.value
            n = _node("tenet_background_icon", val, comments=c.comments,
                      trailing="# UNVERIFIED-VANILLA: was doctrine_background_icon = %s" % c.value)
            out.append(n)
            out.append(_comment_block(["# TODO: set %s (1.20 siblings of tenet_background_icon)"
                                       % s for s in FAMILY_ICON_SIBLINGS]))
            rep.add(fam.key, "`doctrine_background_icon = %s` -> `tenet_background_icon = %s`"
                    % (c.value, val))
            rep.todo(fam.key, "set %s" % ", ".join("`%s`" % s for s in FAMILY_ICON_SIBLINGS))
        else:
            out.append(c)
    fam.value = out
    _stopgap(fam)
    return fam


# ------------------------------------------------------------------ faiths
def port_faith(faith, religion_key, rep):
    details = [_node("religion", religion_key)]
    tenets, doctrines, rest, carried = [], [], [], []
    for c in faith.value:
        if _is_comment_node(c):
            rest.append(c)
            continue
        if c.key in FAITH_DETAIL_KEYS:
            details.append(c)
            continue
        if c.key == "doctrine" and isinstance(c.value, str):
            carried += c.comments
            if c.trailing:
                carried.append(c.trailing)
            name = c.value
            if name in DOCTRINE_RENAMES:
                new = DOCTRINE_RENAMES[name]
                doctrines.append(new)
                rep.add(faith.key, "`%s` -> `%s` (doctrines; not a tenet in 1.20)" % (name, new))
            elif name.startswith("tenet_"):
                tenets.append(name)
            else:
                doctrines.append(name)
            continue
        rest.append(c)
    have = {d.key for d in details}
    for k in ("icon", "reformed_icon", "graphical_faith"):
        if k not in have:
            rep.todo(faith.key, "faith_details has no `%s` (v1 had none)" % k)
    details_node = _node("faith_details", details)
    details_node.comments = ["# TODO: icon / reformed_icon / graphical_faith (none in v1)"] \
        if not ({"icon", "reformed_icon", "graphical_faith"} & have) else []
    body = [details_node]
    if tenets:
        body.append(_node("tenets", [_bare(t) for t in tenets]))
    if doctrines:
        body.append(_node("doctrines", [_bare(d) for d in doctrines]))
    if carried:
        body.append(_comment_block(carried))
    body += rest
    rep.add(faith.key, "moved out of `%s.faiths` to faith_types; faith_details = { religion = "
            "%s%s }; tenets: %s; doctrines: %s" % (
                religion_key, religion_key,
                "".join(" " + d.key for d in details[1:]),
                ", ".join(tenets) or "none", ", ".join(doctrines) or "none"))
    for r in rest:
        if not _is_comment_node(r):
            rep.add(faith.key, "kept `%s` unchanged" % r.key)
    if any("holy_site" in t for r in rest if _is_comment_node(r) for t in r.comments) or \
            any("holy_site" in t for t in carried):
        rep.todo(faith.key, "holy sites are commented out in v1; define them after Gate 1")
    out = _node(faith.key, body, comments=faith.comments)
    _stopgap(out)
    return out


# ------------------------------------------------------------------ religions
def port_religion(rel, rep):
    details, body, faiths = [], [], []
    for c in rel.value:
        if c.key in RELIGION_DETAIL_KEYS:
            details.append(c)
            continue
        if c.key == "faiths" and c.is_block:
            for f in c.value:
                if _is_comment_node(f) or not f.is_block:
                    if _is_comment_node(f):
                        continue
                    rep.todo(rel.key, "unexpected non-block `%s` in faiths" % f.key)
                    continue
                faiths.append(port_faith(f, rel.key, rep))
            continue
        body.append(c)
    if details:
        dn = _node("religion_details", details)
        body.insert(0, dn)
        rep.add(rel.key, "`%s` -> religion_details = { }" % "`, `".join(d.key for d in details))
    else:
        rep.todo(rel.key, "no family/graphical_faith/piety_icon_group found")
    ndoc = sum(1 for c in body if c.key == "doctrine")
    rep.add(rel.key, "kept %d religion-level `doctrine =` lines, plus %s" % (
        ndoc, ", ".join("`%s`" % c.key for c in body
                        if c.key not in ("doctrine", "religion_details") and not _is_comment_node(c))
        or "nothing else"))
    rel.value = body
    _stopgap(rel)
    return rel, faiths


# ------------------------------------------------------------------ files
HEADER = ("# GENERATED by docs/tools/port_religions_1_20.py from\n"
          "#   {src}\n"
          "# CK3 1.20 shape; staging only (docs/port/), NOT loaded by the game.\n"
          "# Do not hand-edit: change the converter or the source and re-run.\n")


def _write(path, src_rel, nodes, footer=None):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body = "\n\n".join(P.dump([n], tab="\t") for n in nodes)
    text = HEADER.format(src=src_rel) + "\n" + body + "\n"
    if footer:
        text += "\n".join(footer) + "\n"
    with open(path, "w", encoding="utf-8-sig", newline="\n") as fh:
        fh.write(text)


def _faith_file_name(name):
    stem, ext = os.path.splitext(name)
    return (stem.replace("religions", "faiths") if "religions" in stem else stem + "_faiths") + ext


def port(src, out, repo_root=REPO):
    """Run the conversion. Returns (report, [written paths])."""
    rep = Report()
    written = []
    target = os.path.join(out, "common", "religion")
    if os.path.isdir(target):
        shutil.rmtree(target)

    def rel_src(p):
        try:
            return os.path.relpath(p, repo_root).replace(os.sep, "/")
        except ValueError:
            return p.replace(os.sep, "/")

    fam_dir = os.path.join(src, "religion_family_types")
    for name in sorted(os.listdir(fam_dir)) if os.path.isdir(fam_dir) else []:
        if not name.endswith(".txt"):
            continue
        p = os.path.join(fam_dir, name)
        doc = P.parse_file(p, keep_comments=True)
        for line, msg in doc.errors:
            rep.todo(name, "parse error line %d: %s" % (line, msg))
        nodes = [port_family(n, rep) if n.is_block else n for n in doc.nodes]
        dst = os.path.join(target, "religion_family_types", name)
        _write(dst, rel_src(p), nodes, doc.footer_comments)
        written.append(dst)

    rel_dir = os.path.join(src, "religion_types")
    for name in sorted(os.listdir(rel_dir)) if os.path.isdir(rel_dir) else []:
        if not name.endswith(".txt"):
            continue
        p = os.path.join(rel_dir, name)
        doc = P.parse_file(p, keep_comments=True)
        for line, msg in doc.errors:
            rep.todo(name, "parse error line %d: %s" % (line, msg))
        rel_nodes, faith_nodes = [], []
        for n in doc.nodes:
            if n.is_block and n.key in DROP_RELIGIONS:
                fk = [f.key for b in P.find(n.value, "faiths") for f in b.value
                      if f.is_block]
                rep.dropped.append((n.key, fk, DROP_RELIGIONS[n.key], rel_src(p), n.line))
                # keep its leading comments out of the next block's header
                continue
            if n.is_block:
                r, fs = port_religion(n, rep)
                rel_nodes.append(r)
                faith_nodes += fs
            else:
                rel_nodes.append(n)
        dst = os.path.join(target, "religion_types", name)
        _write(dst, rel_src(p), rel_nodes, doc.footer_comments)
        written.append(dst)
        fdst = os.path.join(target, "faith_types", _faith_file_name(name))
        _write(fdst, rel_src(p), faith_nodes)
        written.append(fdst)

    report_path = os.path.join(out, "PORT_REPORT.md")
    with open(report_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(render_report(rep, [os.path.relpath(w, out).replace(os.sep, "/")
                                     for w in written], rel_src(src)))
    written.append(report_path)
    return rep, written


def render_report(rep, files, src):
    L = ["# Religion port report: CK3 1.19 -> 1.20 (generated)", "",
         "Generated by `docs/tools/port_religions_1_20.py` from `%s`. Staging only: "
         "nothing here is loaded by the game. Re-run the tool rather than editing; "
         "`--check` verifies the staged files are current." % src, "",
         "**Static, unvalidated.** Tiger 1.17 can't parse 1.20 religion folders; validate "
         "the staged files in game (or with a 1.20-aware Tiger) before moving them to "
         "`common/religion/`.", "",
         "## Files written", ""]
    L += ["- `%s`" % f for f in files]
    L += ["", "## Dropped", ""]
    if rep.dropped:
        for key, faiths, why, path, line in rep.dropped:
            L.append("- `%s` (%s:%d) with faith(s) %s: %s. Its loc keys in "
                     "`eotg_religions_l_english.yml` / `eotg_religion_gods_l_english.yml` are "
                     "untouched (loc is out of scope here)." % (
                         key, path, line, ", ".join("`%s`" % f for f in faiths) or "none", why))
    else:
        L.append("- none")
    L += ["", "## Transformations", ""]
    section = None
    for sec, text in rep.lines:
        if sec != section:
            L += ["", "### `%s`" % sec]
            section = sec
        L.append("- %s" % text)
    L += ["", "## TODO", ""]
    L += ["- `%s`: %s" % (w, t) for w, t in rep.todos] or ["- none"]
    L += ["", "## UNVERIFIED-VANILLA assumptions", ""]
    L += ["%d. %s" % (i, u) for i, u in enumerate(UNVERIFIED, 1)]
    L.append("")
    return "\n".join(L)


def _snapshot(out):
    snap = {}
    for d, _, files in os.walk(out):
        for f in files:
            p = os.path.join(d, f)
            with open(p, "rb") as fh:
                snap[os.path.relpath(p, out)] = fh.read()
    return snap


def main(argv=None):
    ap = argparse.ArgumentParser(description="Port v1 religions to the CK3 1.20 schema (staging).")
    ap.add_argument("--src", default=DEFAULT_SRC, help="v1 common/religion folder")
    ap.add_argument("--out", default=DEFAULT_OUT, help="staging folder (never live common/)")
    ap.add_argument("--check", action="store_true",
                    help="regenerate in a temp dir and exit 1 if --out differs")
    args = ap.parse_args(argv)
    out = os.path.abspath(args.out)
    live = os.path.join(REPO, "common")
    if out == live or out.startswith(live + os.sep):
        ap.error("refusing to write into the live common/ folder")
    if args.check:
        import tempfile
        with tempfile.TemporaryDirectory() as tmp:
            port(args.src, tmp)
            fresh = _snapshot(tmp)
        current = _snapshot(out) if os.path.isdir(out) else {}
        stale = sorted(set(fresh) ^ set(current) |
                       {k for k in fresh if k in current and fresh[k] != current[k]})
        for k in stale:
            print("stale: %s" % k)
        print("port output %s" % ("is current" if not stale else "is STALE (%d file(s))" % len(stale)))
        return 1 if stale else 0
    rep, written = port(args.src, out)
    for w in written:
        print("wrote %s" % os.path.relpath(w, REPO).replace(os.sep, "/"))
    print("dropped: %s" % (", ".join(d[0] for d in rep.dropped) or "none"))
    print("%d transformation line(s), %d TODO(s)" % (len(rep.lines), len(rep.todos)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
