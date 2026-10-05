"""Build the test map's terrain textures. Called by install.py; runnable on its own.

The test map is 8192x4096. The main mod's terrain textures are built for the vanilla map
(9216x4608), and a terrain index whose size does not match provinces.png renders as garbage or as
a black map, so the sub-mod needs its OWN copies of the three map-sized files:

    detail_index.tga       8192x4096   ~134 MB
    detail_intensity.tga   8192x4096   ~134 MB
    colormap.dds           4096x2048   ~11 MB   (half-res is fine; it is soft-lit)

Those three and nothing else. materials.settings, the terrain masks and the structure textures are
all map-size INDEPENDENT and come from the main mod. The sub-mod deliberately does not ship copies
of them: a duplicate would silently override the real file later and desync the indices.

They are not committed. detail_index.tga alone is 134 MB, over GitHub's 100 MB per-file limit, so
committing it would break every push. They are gitignored and built here instead, which is sound
because unlike the main mod's colormap these ARE reproducible — both generators seed their noise
explicitly and every input is in the repo.

================================================================================================
THE INDEX DEPENDS ON THE MAIN MOD'S materials.settings *ORDER*. REBUILD IF THAT CHANGES.
================================================================================================
detail_index.tga stores POSITIONAL material ids - the index of each material in the main mod's
materials.settings, not its name. Add, remove or reorder an entry in the TERRAINS table of
docs/tools/build_terrain_hybrid.py and every id in this map's index silently points at the wrong
material: the map still loads, it just paints the wrong terrains. Nothing detects this. Rerun this
script after any change to that table.

WHY A TEMP DIR. build_terrain_index.py takes one mod root and uses it for BOTH reading
materials.settings and writing its output, so it cannot read from the main mod and write somewhere
else. Rather than drop a stale materials.settings into the sub-mod, this stages the main mod's copy
into a temp directory, builds there, and moves the three results to --out. Nothing is left behind.

Usage:
    python docs/test_map/build_terrain.py [--out <dir>] [--level 132] [--size 4096x2048]

--out defaults to docs/test_map/gfx/map/terrain. install.py should pass the INSTALLED sub-mod's
gfx/map/terrain instead, so the textures land where the game will read them.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))          # docs/test_map
REPO = os.path.dirname(os.path.dirname(HERE))              # repo root
TOOLS = os.path.join(REPO, "docs", "tools")
REL = os.path.join("gfx", "map", "terrain")

# The main mod's colormap and structure bakes are tracked, and they ARE reproducible - but only
# from one specific source image and one specific --level, neither of which is obvious. They are
# therefore easy to replace WRONG: a well-meaning rerun with the defaults silently swaps them for
# something subtly different, and a .dds diff tells you nothing readable. See docs/pitfalls.md
# section 13 and gfx/map/terrain/README.md for the exact commands. This script must never touch
# them, so it checksums them before and after and fails loudly rather than letting a redirect bug
# replace them quietly.
GUARDED = ["colormap.dds"] + [
    "eotg_structure_%s_%s.dds" % (n, k) for n in "abc" for k in ("diffuse", "normal", "properties")
]
OUTPUTS = ["detail_index.tga", "detail_intensity.tga", "colormap.dds"]


def guard_digest() -> str:
    h = hashlib.sha1()
    for name in GUARDED:
        p = os.path.join(REPO, REL, name)
        h.update(name.encode())
        h.update(open(p, "rb").read() if os.path.exists(p) else b"<missing>")
    return h.hexdigest()


def refuse_if_inside_main_gfx(out: str) -> None:
    """The one thing this script must never do is write into the main mod's gfx/."""
    forbidden = os.path.realpath(os.path.join(REPO, "gfx"))
    real = os.path.realpath(out)
    if real == forbidden or real.startswith(forbidden + os.sep):
        sys.exit("REFUSING: --out is inside the main mod's gfx/ (%s).\nThat directory holds "
                 "tracked art that is easy to replace wrong; see docs/pitfalls.md section 13." % real)


def run(script: str, *args: str) -> None:
    cmd = [sys.executable, os.path.join(TOOLS, script)] + list(args)
    r = subprocess.run(cmd, cwd=REPO)
    if r.returncode != 0:
        sys.exit("%s failed (exit %d)" % (script, r.returncode))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=os.path.join(HERE, *REL.split(os.sep)),
                    help="where the three textures are written (default: docs/test_map/gfx/map/terrain)")
    ap.add_argument("--size", default="4096x2048", help="colormap size, half the map is plenty")
    # 132 is the main mod's own colormap level - at this size it reproduces the tracked file
    # BYTE-IDENTICALLY, so the test map reads at exactly the main mod's tone rather than merely
    # close to it. This said 131 until 2026-10-04, which was wrong: 131 gives mean 131.33 against
    # the main mod's 131.47 and a visibly wider dark tail. The tool's own default of 106 is
    # markedly darker again.
    ap.add_argument("--level", default="132", help="colormap sRGB level; 132 matches the main mod")
    a = ap.parse_args()

    out = os.path.abspath(a.out)
    refuse_if_inside_main_gfx(out)

    src_materials = os.path.join(REPO, REL, "materials.settings")
    if not os.path.exists(src_materials):
        sys.exit("missing the main mod's materials.settings at " + src_materials)

    before = guard_digest()
    os.makedirs(out, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="eotg_testmap_terrain_")
    try:
        staged = os.path.join(tmp, REL)
        os.makedirs(staged, exist_ok=True)
        shutil.copy2(src_materials, os.path.join(staged, "materials.settings"))

        # Both builds write into the temp root; nothing is written to --out until they succeed.
        run("build_terrain_index.py", tmp, "--game", HERE)
        run("build_colormap.py", tmp, "--size", a.size, "--level", a.level)

        print("\nmoving into %s" % out)
        for name in OUTPUTS:
            src = os.path.join(staged, name)
            if not os.path.exists(src):
                sys.exit("expected output missing: " + name)
            dst = os.path.join(out, name)
            if os.path.exists(dst):
                os.remove(dst)
            shutil.move(src, dst)
            print("  %-22s %7.1f MB" % (name, os.path.getsize(dst) / 1048576.0))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if guard_digest() != before:
        sys.exit("ABORT: the main mod's protected terrain art changed during this run. "
                 "Restore it from git immediately (docs/pitfalls.md section 13).")
    print("\nmain mod gfx/ verified untouched (checksum %s)" % before[:12])
    print("NOTE: this index is bound to the ORDER of the main mod's materials.settings. "
          "Rerun this script if that file's entries change.")


if __name__ == "__main__":
    main()
