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
  family     doctrine_background_icon = x.dds -> the vanilla tenet-icon set
             (tenet_background_icon / _heretical_ / _neutral_ / _unknown_);
             graphical_faith christian_gfx -> orthodox_gfx (not a vanilla value)
  religion   + doctrine = <family hostility_doctrine> (vanilla religions all carry one)
  faith      + icon = <placeholder vanilla faith icon> (no eotg_* faith art exists)
  holy sites commented v1 `holy_site = x` lines -> `holy_sites = { }` /
             `eminent_holy_sites = { }` list-form comments
Verified against vanilla 1.20.0.3: docs/port/religion_1_20/VERIFY_2026-10-04.md.
  dropped    eotg_religion_stampede (Nikios Khanate, deferred; CLAUDE.md invariant 9)
Every top-level block gets `# STOPGAP: replace from briefs`; comments are kept
where they attach to a node that survives.
"""
import argparse
import os
import re
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
# Vanilla tenet-icon set, common/religion/religion_family_types/00_religion_family_types.txt:4-7
# (VERIFY_2026-10-04.md fix 1). core_tenet_banner_christian does not exist in 1.20.
FAMILY_TENET_ICONS = (
    ("tenet_background_icon", "tenet_banner_known_core"),
    ("tenet_heretical_background_icon", "tenet_banner_unknown_heretical"),
    ("tenet_neutral_background_icon", "tenet_banner_known_neutral"),
    ("tenet_unknown_background_icon", "tenet_banner_unknown_neutral"),
)
# graphical_faith values that are not vanilla (fix 2: rf_abrahamic uses orthodox_gfx)
GFX_RENAMES = {"christian_gfx": "orthodox_gfx"}
# Placeholder faith icons until eotg_* faith art exists (fix 3). Basenames of files in
# game/gfx/interface/icons/faith/ -- UNVERIFIED-VANILLA: the local session must confirm
# each basename exists and edit this table if not. Keyed by religion family.
FAITH_ICON_BY_FAMILY = {
    "eotg_rf_divine_order": "orthodox",
}
DEFAULT_FAITH_ICON = "germanic_pagan"
HOLY_SITE_RE = re.compile(r"^#\s*holy_site\s*=\s*([\w.]+)")

# Assumptions A1-A7 of the first run, settled by VERIFY_2026-10-04.md (vanilla 1.20.0.3)
CONFIRMED = [
    "A1: religion-level `doctrine = x` lines are valid in 1.20 as single lines.",
    "A2 (corrected): families keep `graphical_faith`, `piety_icon_group` and "
    "`hostility_doctrine`, but `christian_gfx` is not a vanilla `graphical_faith`; "
    "`eotg_rf_divine_order` now uses `orthodox_gfx` (as `rf_abrahamic`).",
    "A3 (corrected): `doctrine_background_icon` became four fields; families now use the "
    "vanilla set `tenet_banner_known_core` / `tenet_banner_unknown_heretical` / "
    "`tenet_banner_known_neutral` / `tenet_banner_unknown_neutral` "
    "(`00_religion_family_types.txt:4-7`). `core_tenet_banner_christian.dds` does not exist "
    "in 1.20, and `core_tenet_banner_pagan` has no `_small` pair.",
    "A4: `faith_details = { religion = ... }` is the only required field; `color` moves "
    "inside it unchanged (`{ r g b }`, 0-1 floats).",
    "A5: religion `traits = { virtues sins }` and `localization = { }` keep their shape.",
    "A7: `doctrine_monasticism_encouraged` replaces `tenet_monasticism` "
    "(`doctrine_types/20_doctrines.txt:2071`).",
    "All 23 tenet keys and all 59 doctrine keys used resolve in 1.20; no unrecognised fields.",
]
UNVERIFIED = [
    "Placeholder faith icon basenames (`%s` for Divine Order, `%s` otherwise) exist in "
    "`game/gfx/interface/icons/faith/`. A6 (a missing `icon` falling back) stays unproven, "
    "so an explicit icon is emitted instead; edit `FAITH_ICON_BY_FAMILY` if a basename is "
    "wrong." % (FAITH_ICON_BY_FAMILY["eotg_rf_divine_order"], DEFAULT_FAITH_ICON),
    "BEHAVIOUR: whether a religion's hostility doctrine is required. It is now emitted from "
    "the family's `hostility_doctrine`, as every vanilla religion carries one "
    "(`00_christianity.txt:10`, `00_paganism.txt:9`).",
]
DESIGN_CALLS = [
    "Empty doctrine groups are NOT filled: theism, monasticism (except Coldiron's faith), "
    "sacraments, coronation, preservation. Vanilla religions fill them; whether an empty "
    "group breaks anything is BEHAVIOUR for an in-game load test, and the choice of values "
    "is a design call for the human/architect when religions are ported (B-FAITHS).",
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
    have_icon = False
    for c in fam.value:
        if c.key == "doctrine_background_icon" and isinstance(c.value, str):
            have_icon = True
            for k, v in FAMILY_TENET_ICONS:
                n = _node(k, v)
                if k == "tenet_background_icon":
                    n.comments = list(c.comments)
                    n.trailing = "# was doctrine_background_icon = %s (1.19)" % c.value
                out.append(n)
            rep.add(fam.key, "`doctrine_background_icon = %s` -> vanilla tenet-icon set (%s)"
                    % (c.value, ", ".join("`%s = %s`" % kv for kv in FAMILY_TENET_ICONS)))
        elif c.key == "graphical_faith" and isinstance(c.value, str) and c.value in GFX_RENAMES:
            new = GFX_RENAMES[c.value]
            n = _node("graphical_faith", new, comments=c.comments, quoted=c.quoted,
                      trailing=c.trailing)
            out.append(n)
            rep.add(fam.key, "`graphical_faith = \"%s\"` -> `\"%s\"` (not a vanilla value)"
                    % (c.value, new))
        else:
            out.append(c)
    if not have_icon:
        out += [_node(k, v) for k, v in FAMILY_TENET_ICONS]
        rep.add(fam.key, "added the vanilla tenet-icon set (v1 had no background icon)")
    fam.value = out
    _stopgap(fam)
    return fam


def family_hostility(fam):
    h = P.first(fam.value, "hostility_doctrine")
    return h.value if h is not None and isinstance(h.value, str) else None


# ------------------------------------------------------------------ faiths
def _holy_sites(lines):
    """Split comment lines into (holy-site keys, other lines)."""
    sites, other = [], []
    for t in lines:
        m = HOLY_SITE_RE.match(t)
        if m:
            sites.append(m.group(1))
        else:
            other.append(t)
    return sites, other


def port_faith(faith, religion_key, rep, family=None):
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
    if "icon" not in have:
        icon = FAITH_ICON_BY_FAMILY.get(family, DEFAULT_FAITH_ICON)
        details.append(_node("icon", icon, trailing="# placeholder vanilla icon (no eotg_ faith "
                                                    "art yet); UNVERIFIED-VANILLA basename"))
        have.add("icon")
        rep.add(faith.key, "added placeholder `icon = %s` (family %s)" % (icon, family))
        rep.todo(faith.key, "replace placeholder `icon = %s` with eotg faith art (B-ART)" % icon)
    for k in ("reformed_icon", "graphical_faith"):
        if k not in have:
            rep.todo(faith.key, "faith_details has no `%s` (optional; v1 had none)" % k)
    details_node = _node("faith_details", details)
    missing = [k for k in ("reformed_icon", "graphical_faith") if k not in have]
    details_node.comments = (["# TODO: %s (none in v1)" % " / ".join(missing)] if missing else [])
    body = [details_node]
    if tenets:
        body.append(_node("tenets", [_bare(t) for t in tenets]))
    if doctrines:
        body.append(_node("doctrines", [_bare(d) for d in doctrines]))
    # commented v1 `holy_site = x` lines -> the 1.20 list form (VERIFY fix 6)
    sites, carried = _holy_sites(carried)
    kept_rest = []
    for r in rest:
        if _is_comment_node(r):
            ss, other = _holy_sites(r.comments)
            sites += ss
            if other:
                kept_rest.append(_comment_block(other))
        else:
            kept_rest.append(r)
    rest = kept_rest
    if carried:
        body.append(_comment_block(carried))
    if sites:
        body.append(_comment_block([
            "# holy_sites = { %s }    # TODO: define holy sites + counties after Gate 1"
            % " ".join(sites),
            "# eminent_holy_sites = { }    # TODO: choose the eminent subset (1.20 list form)"]))
        rep.add(faith.key, "commented v1 `holy_site =` lines -> `holy_sites = { %s }` / "
                "`eminent_holy_sites = { }` (list form, still commented)" % " ".join(sites))
    body += rest
    rep.add(faith.key, "moved out of `%s.faiths` to faith_types; faith_details = { religion = "
            "%s%s }; tenets: %s; doctrines: %s" % (
                religion_key, religion_key,
                "".join(" " + d.key for d in details[1:]),
                ", ".join(tenets) or "none", ", ".join(doctrines) or "none"))
    for r in rest:
        if not _is_comment_node(r):
            rep.add(faith.key, "kept `%s` unchanged" % r.key)
    if sites:
        rep.todo(faith.key, "holy sites are commented out in v1; define them after Gate 1")
    out = _node(faith.key, body, comments=faith.comments)
    _stopgap(out)
    return out


# ------------------------------------------------------------------ religions
def port_religion(rel, rep, hostility_by_family=None):
    details, body, faiths = [], [], []
    fam = P.first(rel.value, "family")
    fam_key = fam.value if fam is not None and isinstance(fam.value, str) else None
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
                faiths.append(port_faith(f, rel.key, rep, family=fam_key))
            continue
        body.append(c)
    for i, d in enumerate(details):
        if d.key == "graphical_faith" and isinstance(d.value, str) and d.value in GFX_RENAMES:
            details[i] = _node("graphical_faith", GFX_RENAMES[d.value], comments=d.comments,
                               quoted=d.quoted, trailing=d.trailing)
            rep.add(rel.key, "`graphical_faith = \"%s\"` -> `\"%s\"` (not a vanilla value)"
                    % (d.value, GFX_RENAMES[d.value]))
    if details:
        dn = _node("religion_details", details)
        body.insert(0, dn)
        rep.add(rel.key, "`%s` -> religion_details = { }" % "`, `".join(d.key for d in details))
    else:
        rep.todo(rel.key, "no family/graphical_faith/piety_icon_group found")
    hostility = (hostility_by_family or {}).get(fam_key)
    has_h = any(c.key == "doctrine" and isinstance(c.value, str)
                and c.value.endswith("_hostility_doctrine") for c in body)
    if hostility and not has_h:
        body.insert(1 if details else 0, _node(
            "doctrine", hostility, trailing="# from family %s hostility_doctrine" % fam_key))
        rep.add(rel.key, "added `doctrine = %s` (matches family `%s`)" % (hostility, fam_key))
    elif not hostility and not has_h:
        rep.todo(rel.key, "no hostility doctrine: family `%s` not found" % fam_key)
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

    hostility = {}
    fam_dir = os.path.join(src, "religion_family_types")
    for name in sorted(os.listdir(fam_dir)) if os.path.isdir(fam_dir) else []:
        if not name.endswith(".txt"):
            continue
        p = os.path.join(fam_dir, name)
        doc = P.parse_file(p, keep_comments=True)
        for line, msg in doc.errors:
            rep.todo(name, "parse error line %d: %s" % (line, msg))
        nodes = [port_family(n, rep) if n.is_block else n for n in doc.nodes]
        for n in nodes:
            if n.is_block and n.key:
                hostility[n.key] = family_hostility(n)
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
                r, fs = port_religion(n, rep, hostility)
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
         "**Structure verified against vanilla 1.20.0.3** (`VERIFY_2026-10-04.md`); the "
         "behaviour items below still need an in-game load test. Tiger 1.17 can't parse 1.20 "
         "religion folders.", "",
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
    L += ["", "## Confirmed against vanilla 1.20.0.3", "",
          "From `VERIFY_2026-10-04.md` (eotg-vanilla-scout, local)."]
    L += ["- %s" % c for c in CONFIRMED]
    L += ["", "## UNVERIFIED-VANILLA", ""]
    L += ["%d. %s" % (i, u) for i, u in enumerate(UNVERIFIED, 1)]
    L += ["", "## Design calls (not port bugs; not filled)", ""]
    L += ["- %s" % d for d in DESIGN_CALLS]
    L.append("")
    return "\n".join(L)


def _snapshot(out):
    snap = {}
    for d, _, files in os.walk(out):
        for f in files:
            p = os.path.join(d, f)
            rel = os.path.relpath(p, out).replace(os.sep, "/")
            # only what port() generates; hand-written notes (VERIFY_*.md) are not compared
            if not (rel == "PORT_REPORT.md" or rel.startswith("common/religion/")):
                continue
            with open(p, "rb") as fh:
                # line-ending-insensitive: a Windows checkout (core.autocrlf) turns the
                # committed LF files into CRLF; that is not staleness
                snap[os.path.relpath(p, out).replace(os.sep, "/")] = \
                    fh.read().replace(b"\r\n", b"\n")
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
