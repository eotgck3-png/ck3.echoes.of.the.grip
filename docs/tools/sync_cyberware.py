"""Import the cyberware portrait set from the MCP asset workspace (docs/specs/cyberware_portraits_ship.md §4.2-4.4).

    python docs/tools/sync_cyberware.py plan   [--src C:/Users/river/MCP] [--no-wiring]
    python docs/tools/sync_cyberware.py copy   [--src ...] [--no-wiring] [--check]
    python docs/tools/sync_cyberware.py verify [--report PATH]

plan    dry run: added / changed / removed / unchanged per kind, totals. Exit 0 unless the
        source breaks a rule (then 1).
copy    copy the allowlist (spec §4.2), generate the wiring files B and C from the MCP draft
        (spec §4.4; skipped with --no-wiring), write docs/tools/cyberware_manifest.json.
        Deletes a destination file only if the PREVIOUS manifest lists it and the source no
        longer has it. Close the game first: the repo is the live mod through the junction.
copy --check
        copies nothing; exit 1 if anything would change (stale import). With --no-wiring the
        wiring files are not compared.
verify  re-hashes the working tree against the manifest; needs no MCP. Reports missing,
        changed and extra files in the managed folders, and git-LFS pointer files (a
        GIT_LFS_SKIP_SMUDGE checkout). --report writes a plain-text checksum list (put it in
        a scratchpad, not the repo). Exit 1 on any finding.

Allowlist, never more: the 20 model folders under gfx/models/portraits/eotg_cyberware/, the
face-mark decals, and the named script / loc files below. Denylist on top (spec §4.2): the MCP
descriptor, any DIRECTORY named for the race kit (chad_orc, male_head, female_head, textures),
common/ethnicities, gfx/coat_of_arms, gui, interface, and every basename that does not start
with eotg_.

Note on chad_orc (deviation from the letter of spec §4.2, reported 2026-11-03): 30 cyberware
meshes are NAMED eotg_*_chad_orc*.mesh (earpiece, dressing, ring race fits). They are part of
the 2,585-mesh set the spec counts and are referenced by three .asset files, so dropping them
would break those entities. The race-kit rule is therefore applied to path directories and to
non-eotg_ basenames (chad_orc_genes.txt, decals/chad_orc/, the head blendshapes), which is
every race-kit file in the workspace.

Standard library only; generated text goes through textio (exactly one BOM).
"""
import argparse
import datetime
import fnmatch
import hashlib
import json
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import textio  # noqa: E402

TOOL_VERSION = 1
DEFAULT_SRC = "C:/Users/river/MCP"
DEFAULT_DST = os.path.dirname(os.path.dirname(HERE))
MANIFEST_REL = "docs/tools/cyberware_manifest.json"
MOD_REL = "ck3_mod"
CATALOG_REL = "staging/cyberware/CATALOG.md"
DRAFT_REL = "staging/cyberware/eotg_wiring/eotg_cyberware_portrait_modifiers_draft.txt"

# Folders managed whole (recursive): every file must be eotg_* with one of these extensions.
TREES = [
    ("gfx/models/portraits/eotg_cyberware", True, (".mesh", ".dds", ".asset")),
    ("gfx/models/portraits/decals/eotg_face_mark", False, (".dds",)),
]
# Folders shared with other content: only these basenames (fnmatch) are imported.
NAMED = [
    ("common/genes", ["eotg_cyber_head_genes.txt", "eotg_cyber_body_genes.txt",
                      "eotg_wear_face_mark_genes.txt"]),
    ("gfx/portraits/accessories", ["eotg_cyber_*.txt", "eotg_wear_*.txt"]),
    ("gfx/portraits/portrait_modifiers", ["eotg_cyber_head_custom.txt", "eotg_cyber_body_custom.txt",
                                          "eotg_wear_face_mark_custom.txt"]),
    ("localization/english", ["eotg_cyber_head_l_english.yml", "eotg_cyber_body_l_english.yml",
                              "eotg_wear_face_mark_l_english.yml"]),
]
# In the NAMED folders, destination files with these prefixes count as ours for "extra" checks.
MANAGED_PREFIXES = ("eotg_cyber_", "eotg_wear_")
ALLOWED_EXT = (".mesh", ".dds", ".asset", ".txt", ".yml")
LFS_EXT = (".mesh", ".dds")

DENY_FILES = {"descriptor.mod"}
DENY_DIR_PARTS = {"chad_orc", "male_head", "female_head", "textures"}
DENY_PREFIXES = ("common/ethnicities/", "gfx/coat_of_arms/", "gui/", "interface/")

# Generated wiring files (spec §4.4): output path -> draft section letter.
OUT_B = "gfx/portraits/trait_portrait_modifiers/eotg_cyber_trait_modifiers.txt"
OUT_C = "gfx/portraits/portrait_modifiers/eotg_wear_game.txt"
# Exactly these substitutions on section B, each with its measured count (2026-11-03).
SUBS_B = [
    ("has_character_flag = eotg_aug_prosthetic_eye", "eotg_portrait_prosthetic_eye_trigger = yes", 10),
    ("has_character_flag = eotg_aug_prosthetic_arm", "eotg_portrait_prosthetic_arm_trigger = yes", 15),
    ("has_character_flag = eotg_aug_prosthetic_leg", "eotg_portrait_prosthetic_leg_trigger = yes", 9),
]
BANNER = re.compile(r"^# =+\s*$")
SECTION = re.compile(r"^# ([ABC])\. ")

MB = 1024 * 1024
HARD_LIMIT = 100 * MB
WARN_LIMIT = 50 * MB
LFS_POINTER_MAX = 1024
LFS_POINTER_HEAD = b"version https://git-lfs"
LOC_KEY = re.compile(r"^\s*([A-Za-z0-9_.\-']+):[0-9]*\s*\"")


class Stop(Exception):
    """A rule was broken; the run stops with exit 1."""


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def kind_of(rel):
    return "lfs" if rel.lower().endswith(LFS_EXT) else "text"


def denied(rel):
    """Return the reason a relative path is on the denylist, or None."""
    base = rel.rsplit("/", 1)[-1]
    if base in DENY_FILES:
        return "descriptor"
    if any(rel.startswith(p) for p in DENY_PREFIXES):
        return "denied folder"
    if any(part in DENY_DIR_PARTS for part in rel.split("/")[:-1]):
        return "race-kit folder"
    if not base.startswith("eotg_"):
        return "basename lacks eotg_"
    return None


def walk(root):
    """Relative posix paths of every file under root."""
    out = []
    for dirpath, _dirs, files in os.walk(root):
        for f in files:
            out.append(os.path.relpath(os.path.join(dirpath, f), root).replace("\\", "/"))
    return sorted(out)


def collect(mod):
    """-> (candidates [rel], excluded [(rel, reason)], errors [str]) from the MCP ck3_mod folder."""
    cands, errors = [], []
    for folder, recursive, exts in TREES:
        top = os.path.join(mod, folder)
        if not os.path.isdir(top):
            errors.append("source folder missing: %s" % folder)
            continue
        for sub in walk(top):
            if not recursive and "/" in sub:
                errors.append("unexpected subfolder file: %s/%s" % (folder, sub))
                continue
            rel = folder + "/" + sub
            why = denied(rel)
            if why:
                errors.append("%s: %s (allowlisted folder; refusing)" % (rel, why))
            elif not rel.lower().endswith(exts):
                errors.append("%s: extension not in %s" % (rel, ", ".join(exts)))
            else:
                cands.append(rel)
    for folder, patterns in NAMED:
        top = os.path.join(mod, folder)
        if not os.path.isdir(top):
            errors.append("source folder missing: %s" % folder)
            continue
        for base in sorted(os.listdir(top)):
            rel = folder + "/" + base
            if os.path.isdir(os.path.join(top, base)):
                continue
            if any(fnmatch.fnmatchcase(base, p) for p in patterns):
                why = denied(rel)
                if why:
                    errors.append("%s: %s (matches the allowlist; refusing)" % (rel, why))
                elif not base.lower().endswith(ALLOWED_EXT):
                    errors.append("%s: extension not allowed" % rel)
                else:
                    cands.append(rel)
            elif base.startswith(MANAGED_PREFIXES):
                errors.append("%s: new eotg_cyber_/eotg_wear_ file not on the allowlist; "
                              "add it to NAMED in this tool deliberately" % rel)
    taken = set(cands)
    excluded = [(rel, denied(rel) or "outside the allowlist") for rel in walk(mod) if rel not in taken]
    return sorted(cands), excluded, errors


def loc_keys(text):
    keys = []
    for line in text.split("\n"):
        m = LOC_KEY.match(line)
        if m:
            keys.append(m.group(1))
    return keys


def precheck(mod, dst, cands):
    """Spec §4.3 pre-copy checks. -> (errors, warnings)."""
    errors, warnings = [], []
    imported_keys = {}
    loc_dsts = set()
    for rel in cands:
        path = os.path.join(mod, rel)
        size = os.path.getsize(path)
        if size >= HARD_LIMIT:
            errors.append("%s: %d bytes (GitHub rejects files of 100 MB or more)" % (rel, size))
        elif size >= WARN_LIMIT:
            warnings.append("%s: %d bytes (50 MB or more)" % (rel, size))
        if rel.endswith(".yml"):
            loc_dsts.add(rel)
            with open(path, "rb") as fh:
                raw = fh.read()
            if not raw.startswith(textio.BOM):
                errors.append("%s: no UTF-8 BOM" % rel)
            if textio.stray_bom_offsets(raw):
                errors.append("%s: stray BOM after byte 0" % rel)
            text = textio.decode(raw)[0].replace("\r\n", "\n")
            if text.split("\n", 1)[0].strip() != "l_english:":
                errors.append("%s: first line is not l_english:" % rel)
            for k in loc_keys(text):
                if k in imported_keys:
                    errors.append("%s: loc key %s also defined in %s" % (rel, k, imported_keys[k]))
                imported_keys[k] = rel
    loc_root = os.path.join(dst, "localization")
    if imported_keys and os.path.isdir(loc_root):
        for sub in walk(loc_root):
            rel = "localization/" + sub
            if rel in loc_dsts or not rel.endswith(".yml"):
                continue
            for k in loc_keys(textio.read_text(os.path.join(dst, rel))[0].replace("\r\n", "\n")):
                if k in imported_keys:
                    errors.append("loc key %s (%s) is also defined in %s" % (k, imported_keys[k], rel))
    return errors, warnings


def render_wiring(draft_path, draft_sha):
    """-> {out_rel: bytes} for B and C (spec §4.4). Raises Stop on a count mismatch."""
    lines = textio.read_text(draft_path)[0].replace("\r\n", "\n").split("\n")
    starts = {}
    for i, line in enumerate(lines):
        m = SECTION.match(line)
        if m and i > 0 and BANNER.match(lines[i - 1]) and i + 1 < len(lines) and BANNER.match(lines[i + 1]):
            if m.group(1) in starts:
                raise Stop("draft: section %s banner appears twice" % m.group(1))
            starts[m.group(1)] = i
    if sorted(starts) != ["A", "B", "C"] or not starts["A"] < starts["B"] < starts["C"]:
        raise Stop("draft: expected section banners A, B, C in order; found %s" % sorted(starts))
    # Body runs from after the closing banner line to before the next section's opening banner.
    body_b = lines[starts["B"] + 2:starts["C"] - 1]
    body_c = lines[starts["C"] + 2:]

    def tidy(body):
        while body and not body[-1].strip():
            body = body[:-1]
        while body and not body[0].strip():
            body = body[1:]
        return "\n".join(body) + "\n"

    text_b, text_c = tidy(body_b), tidy(body_c)
    for old, new, want in SUBS_B:
        pat = re.compile(re.escape(old) + r"(?![A-Za-z0-9_])")
        text_b, n = pat.subn(new, text_b)
        if n != want:
            raise Stop("draft section B: %d x '%s', expected %d (spec §4.4); the draft changed shape"
                       % (n, old, want))
    header = ("# GENERATED by docs/tools/sync_cyberware.py from MCP eotg_cyberware_portrait_modifiers_draft.txt\n"
              "# (draft sha256 %s). Do not hand-edit: change MCP staging/cyberware/work/gen_wiring_draft.py "
              "and re-sync.\n\n" % draft_sha)
    # CRLF like every imported script file, so one checkout looks alike.
    return {OUT_B: textio.encode(header + text_b, bom=True, newline="\r\n"),
            OUT_C: textio.encode(header + text_c, bom=True, newline="\r\n")}


def load_manifest(dst):
    path = os.path.join(dst, MANIFEST_REL)
    if not os.path.isfile(path):
        return None
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def check_roots(src, dst, need_src):
    if not os.path.isfile(os.path.join(dst, "echoes_of_the_grip.mod")):
        raise Stop("--dst %s holds no echoes_of_the_grip.mod; refusing" % dst)
    if need_src and not os.path.isfile(os.path.join(src, MOD_REL, "descriptor.mod")):
        raise Stop("--src %s has no %s/descriptor.mod; not the MCP workspace" % (src, MOD_REL))


def build_plan(args):
    """Everything plan / copy need. -> dict."""
    src, dst = os.path.abspath(args.src), os.path.abspath(args.dst)
    check_roots(src, dst, True)
    mod = os.path.join(src, MOD_REL)
    cands, excluded, errors = collect(mod)
    if errors:
        raise Stop("source breaks the allowlist rules:\n  " + "\n  ".join(errors))
    perr, warnings = precheck(mod, dst, cands)
    if perr:
        raise Stop("pre-copy checks failed:\n  " + "\n  ".join(perr))
    prev = load_manifest(dst)
    prev_files = {e["dst"]: e for e in prev["files"]} if prev else {}

    draft_path = os.path.join(src, DRAFT_REL)
    draft_sha = sha256_file(draft_path) if os.path.isfile(draft_path) else None
    catalog_path = os.path.join(src, CATALOG_REL)
    catalog_sha = sha256_file(catalog_path) if os.path.isfile(catalog_path) else None

    entries, actions = [], {"added": [], "changed": [], "unchanged": [], "removed": []}
    for rel in cands:
        spath = os.path.join(mod, rel)
        sha = sha256_file(spath)
        e = {"dst": rel, "src": MOD_REL + "/" + rel, "bytes": os.path.getsize(spath),
             "sha256": sha, "kind": kind_of(rel)}
        entries.append(e)
        dpath = os.path.join(dst, rel)
        if not os.path.isfile(dpath):
            actions["added"].append(e)
        elif sha256_file(dpath) != sha:
            actions["changed"].append(e)
        else:
            actions["unchanged"].append(e)

    generated = {}
    if args.no_wiring:
        # Leave any earlier wiring output alone and keep its manifest entries.
        for rel, e in prev_files.items():
            if e["kind"] == "generated" and os.path.isfile(os.path.join(dst, rel)):
                entries.append(e)
        wiring_sha = prev.get("draft_sha256") if prev and any(
            e["kind"] == "generated" for e in entries) else None
    else:
        if draft_sha is None:
            raise Stop("wiring draft missing: %s" % DRAFT_REL)
        generated = render_wiring(draft_path, draft_sha)
        for rel, data in sorted(generated.items()):
            sha = hashlib.sha256(data).hexdigest()
            e = {"dst": rel, "src": DRAFT_REL + "#" + ("B" if rel == OUT_B else "C"),
                 "bytes": len(data), "sha256": sha, "kind": "generated"}
            entries.append(e)
            dpath = os.path.join(dst, rel)
            if not os.path.isfile(dpath):
                actions["added"].append(e)
            elif sha256_file(dpath) != sha:
                actions["changed"].append(e)
            else:
                actions["unchanged"].append(e)
        wiring_sha = draft_sha

    current = {e["dst"] for e in entries}
    for rel, e in sorted(prev_files.items()):
        if rel not in current and (e["kind"] != "generated" or not args.no_wiring):
            actions["removed"].append(e)

    if prev and draft_sha and prev.get("draft_sha256") and prev["draft_sha256"] != draft_sha:
        warnings.append("MCP wiring draft changed since the last sync (%s -> %s): B and C must be "
                        "regenerated (run copy without --no-wiring)" % (prev["draft_sha256"][:12], draft_sha[:12]))
    if prev and catalog_sha and prev.get("catalog_sha256") not in (None, catalog_sha):
        warnings.append("MCP CATALOG.md changed since the last sync")

    totals = {}
    for e in entries:
        t = totals.setdefault(e["kind"], {"files": 0, "bytes": 0})
        t["files"] += 1
        t["bytes"] += e["bytes"]
    manifest = {
        "tool_version": TOOL_VERSION,
        "source_root": src.replace("\\", "/"),
        "generated_at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "catalog_sha256": catalog_sha,
        "draft_sha256": wiring_sha,
        "spec": "docs/specs/cyberware_portraits_ship.md",
        "totals": totals,
        "files": sorted(entries, key=lambda e: e["dst"]),
    }
    return {"src": src, "dst": dst, "mod": mod, "excluded": excluded, "warnings": warnings,
            "actions": actions, "manifest": manifest, "generated": generated}


def print_plan(p, verbose):
    a = p["actions"]
    for w in p["warnings"]:
        print("WARNING: " + w)
    print("excluded from the source (not imported): %d file(s)" % len(p["excluded"]))
    if verbose:
        for rel, why in p["excluded"]:
            print("  skip  %-22s %s" % (why, rel))
    for key in ("added", "changed", "removed"):
        for e in a[key]:
            print("  %-8s %-9s %s" % (key, e["kind"], e["dst"]))
    for key in ("added", "changed", "removed", "unchanged"):
        by = {}
        for e in a[key]:
            by[e["kind"]] = by.get(e["kind"], 0) + 1
        print("%-9s %5d  %s" % (key, len(a[key]), ", ".join("%s %d" % kv for kv in sorted(by.items()))))
    for kind, t in sorted(p["manifest"]["totals"].items()):
        print("total %-9s %5d files %13d bytes" % (kind, t["files"], t["bytes"]))


def cmd_plan(args):
    p = build_plan(args)
    print_plan(p, True)
    return 0


def cmd_copy(args):
    p = build_plan(args)
    print_plan(p, args.verbose)
    a = p["actions"]
    if args.check:
        stale = len(a["added"]) + len(a["changed"]) + len(a["removed"])
        if load_manifest(p["dst"]) is None:
            print("STALE: no manifest at %s" % MANIFEST_REL)
            return 1
        if stale:
            print("STALE: %d file(s) would change; run copy" % stale)
            return 1
        print("up to date")
        return 0
    dst, mod = p["dst"], p["mod"]
    for e in a["added"] + a["changed"]:
        dpath = os.path.join(dst, e["dst"])
        os.makedirs(os.path.dirname(dpath), exist_ok=True)
        if e["kind"] == "generated":
            with open(dpath, "wb") as fh:
                fh.write(p["generated"][e["dst"]])
        else:
            shutil.copyfile(os.path.join(mod, e["dst"]), dpath)
        if sha256_file(dpath) != e["sha256"]:
            raise Stop("%s: hash mismatch after copy" % e["dst"])
    for e in a["removed"]:
        dpath = os.path.join(dst, e["dst"])
        if os.path.isfile(dpath):
            os.remove(dpath)
            print("  deleted  %s" % e["dst"])
    mpath = os.path.join(dst, MANIFEST_REL)
    tmp = mpath + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(p["manifest"], fh, indent=1, sort_keys=False)
        fh.write("\n")
    os.replace(tmp, mpath)
    print("wrote %s (%d files)" % (MANIFEST_REL, len(p["manifest"]["files"])))
    return 0


def managed_dst_files(dst):
    """Every destination file the tool would own: the whole trees, the eotg_cyber_/eotg_wear_
    files of the shared folders, and the wiring outputs."""
    out = set()
    for folder, _rec, _ext in TREES:
        top = os.path.join(dst, folder)
        if os.path.isdir(top):
            out.update(folder + "/" + s for s in walk(top))
    for folder, _pats in NAMED + [(os.path.dirname(OUT_B), None)]:
        top = os.path.join(dst, folder)
        if os.path.isdir(top):
            for base in os.listdir(top):
                if base.startswith(MANAGED_PREFIXES) and os.path.isfile(os.path.join(top, base)):
                    out.add(folder + "/" + base)
    return out


def is_lfs_pointer(path):
    if os.path.getsize(path) >= LFS_POINTER_MAX:
        return False
    with open(path, "rb") as fh:
        return fh.read(len(LFS_POINTER_HEAD)) == LFS_POINTER_HEAD


def cmd_verify(args):
    dst = os.path.abspath(args.dst)
    check_roots(None, dst, False)
    m = load_manifest(dst)
    if m is None:
        print("FAIL: no manifest at %s" % MANIFEST_REL)
        return 1
    findings, report = [], []
    listed = set()
    for e in m["files"]:
        rel = e["dst"]
        listed.add(rel)
        path = os.path.join(dst, rel)
        if not os.path.isfile(path):
            findings.append("missing  %s" % rel)
            report.append("%-64s %12s %-9s %s" % ("MISSING", "-", e["kind"], rel))
            continue
        if is_lfs_pointer(path):
            findings.append("lfs-pointer  %s (run git lfs pull)" % rel)
        sha = sha256_file(path)
        if sha != e["sha256"]:
            findings.append("changed  %s" % rel)
        report.append("%s %12d %-9s %s%s" % (sha, os.path.getsize(path), e["kind"], rel,
                                             "" if sha == e["sha256"] else "  CHANGED"))
    for rel in sorted(managed_dst_files(dst) - listed):
        findings.append("extra    %s (not in the manifest)" % rel)
        if is_lfs_pointer(os.path.join(dst, rel)):
            findings.append("lfs-pointer  %s" % rel)
    totals = m.get("totals", {})
    summary = ["manifest: %d files; %s" % (len(m["files"]), ", ".join(
        "%s %d (%d bytes)" % (k, v["files"], v["bytes"]) for k, v in sorted(totals.items()))),
        "draft_sha256: %s" % m.get("draft_sha256"),
        "findings: %d" % len(findings)]
    if args.report:
        with open(args.report, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(report + [""] + summary) + "\n")
    for f in findings[:200]:
        print(f)
    if len(findings) > 200:
        print("... %d more" % (len(findings) - 200))
    print("\n".join(summary))
    return 1 if findings else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("plan", "copy", "verify"):
        sp = sub.add_parser(name)
        sp.add_argument("--dst", default=DEFAULT_DST, help="repo root (must hold echoes_of_the_grip.mod)")
        if name != "verify":
            sp.add_argument("--src", default=DEFAULT_SRC, help="MCP workspace root (holds ck3_mod/)")
            sp.add_argument("--no-wiring", action="store_true",
                            help="do not generate (or compare) the wiring files B and C")
        if name == "copy":
            sp.add_argument("--check", action="store_true", help="copy nothing; exit 1 if stale")
            sp.add_argument("-v", "--verbose", action="store_true", help="list excluded source files")
        if name == "verify":
            sp.add_argument("--report", help="write a checksum report here (scratchpad)")
    args = ap.parse_args(argv)
    try:
        return {"plan": cmd_plan, "copy": cmd_copy, "verify": cmd_verify}[args.cmd](args)
    except Stop as exc:
        print("STOP: %s" % exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
