"""Build the galactic province markers: one mesh, one flat-colour texture per government.

CK3 picks a holding's model from the `assets` block of whichever holding building is built, and
an asset entry can be filtered by government:

    asset = {
        type = pdxmesh
        name = "eotg_marker_feudal_mesh"
        governments = { feudal_government }
    }

Government is one of the highest-priority selection criteria - above graphical region - and
vanilla already uses it (tribal, nomad, and a steppe_admin/celestial/meritocratic group). An entry
with no `governments` is the fallback.

Only 18 buildings in the whole game carry an assets block: 4 castle, 4 city, 4 temple, 4 temple
citadel, 2 tribal. Listing every colour against every one of them is what makes the marker survive
a holding upgrade unchanged - the model is the same at all levels, only the government decides the
colour.

Geometry is shared. Eleven pdxmesh entries point at the same .mesh file and differ only in
texture_diffuse, so there is one mesh on disk and no duplicated vertices.

Shape is switchable. The supplied atom glyph is one option; make_marker_obj.py generates the
others as lathed solids. Pass the name as a second argument:

    python docs/tools/build_marker_assets.py <mod root> [atom|podium|chess|disc]
"""
from __future__ import annotations

import os
import re
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_terrain_materials import save_dds_dxt5

REL = os.path.join("gfx", "models", "buildings", "eotg_markers")
SIZE = 128                       # a flat colour needs no resolution; mips still required

# The palette, as supplied. Government keys are the real 1.19 ones - note `nomad_government`,
# not `nomadic`. "Military" has no vanilla equivalent so it covers the two closest; "neutral" is
# the fallback and carries every government not named here (wanua, herder, celestial, mandala,
# steppe_admin, meritocratic, landless_adventurer).
MARKERS = [
    ("feudal",         (231, 184,  75), ["feudal_government"]),
    ("clan",           (217, 138,  58), ["clan_government"]),
    ("republic",       ( 70, 199, 217), ["republic_government"]),
    ("theocracy",      (167, 124, 255), ["theocracy_government"]),
    ("tribal",         ( 85, 185, 107), ["tribal_government"]),
    ("nomadic",        (217,  87,  87), ["nomad_government", "herder_government"]),
    ("administrative", ( 95, 158, 234), ["administrative_government", "steppe_admin_government"]),
    ("military",       (184, 193, 204), ["mercenary_government", "holy_order_government"]),
    ("neutral",        (232, 244, 255), []),          # fallback: no governments filter
]

# Which solid the marker is. Each was checked watertight before conversion - an open shell
# renders with holes, which is what killed the asteroid attempt. `file` and `shape` must agree
# with what obj_to_pdxmesh.py was told, or the engine finds no geometry and draws nothing.
SHAPES = {
    "atom":   ("eotg_marker.mesh",        "eotg_markerShape"),
    "podium": ("eotg_marker_podium.mesh", "eotg_marker_podiumShape"),
    "chess":  ("eotg_marker_chess.mesh",  "eotg_marker_chessShape"),
    "disc":   ("eotg_marker_disc.mesh",   "eotg_marker_discShape"),
}
DEFAULT_SHAPE = "chess"

# Our own effect, added to gfx/FX/pdxmesh.shader. snap_to_terrain runs the marker through full PBR
# lighting and distance fog, which turns a saturated flat colour into a grey smudge; eotg_marker
# keeps the colour and adds a fresnel outline. Reverting is a one-word change here.
SHADER = "eotg_marker"

GAME = r"D:\SteamLibrary\steamapps\common\Crusader Kings III\game"

# Only these files contain buildings with an assets block - 18 buildings out of 981.
HOLDING_FILES = ("00_castle_buildings.txt", "00_city_buildings.txt", "00_temple_buildings.txt",
                 "temple_citadel_buildings.txt", "00_tribal_buildings.txt")


def find_block(text, start):
    """Index just past the matching close brace for the block opening at `start`."""
    depth = 0
    i = start
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced braces")


def override_buildings(mod_root, assets_block):
    """Copy each building that has an assets block, with our assets swapped in.

    Buildings are merged by KEY, so emitting only the 18 that define a model leaves the other 963
    vanilla definitions untouched. Every other field of those 18 is copied verbatim, so gameplay
    is unchanged - this only decides what is drawn.

    The copies go stale if a patch edits those buildings; re-running re-reads vanilla, which is
    why this is generated rather than hand-written.
    """
    outdir = os.path.join(mod_root, "common", "buildings")
    os.makedirs(outdir, exist_ok=True)
    total = 0
    for fn in HOLDING_FILES:
        src = os.path.join(GAME, "common", "buildings", fn)
        if not os.path.exists(src):
            print(f"  skipped, not in this install: {fn}")
            continue
        txt = open(src, encoding="utf-8-sig").read()

        # The `@name = value` reader variables. These are FILE-SCOPED, so a copied building that
        # says `illustration = @holding_illustration_india` resolves to nothing unless the
        # definition travels with it. Leaving them behind cost four unresolved illustrations
        # before Tiger caught it - the game would simply have drawn no picture.
        defs = re.findall(r"^@[A-Za-z_][A-Za-z0-9_]*\s*=\s*[^\n]+$", txt, re.M)

        kept = []
        for m in re.finditer(r"^([a-z0-9_]+)\s*=\s*\{", txt, re.M):
            end = find_block(txt, txt.index("{", m.start()))
            block = txt[m.start():end]
            am = re.search(r"\n\tassets\s*=\s*\{", block)
            if not am:
                continue
            aend = find_block(block, block.index("{", am.start() + 1))
            newblock = block[:am.start()] + "\n" + assets_block.rstrip("\n") + block[aend:]
            kept.append(newblock)
            total += 1
        if kept:
            out = os.path.join(outdir, "eotg_" + fn)
            header = (
                "\ufeff# MOD(eotg) GENERATED by docs/tools/build_marker_assets.py - do not hand-edit.\n"
                "# Vanilla definitions copied verbatim with ONLY the assets block replaced, so\n"
                "# gameplay is untouched and only the model drawn on the map changes.\n"
                "# Buildings merge by key, so the other buildings in the vanilla file are\n"
                "# left alone.\n\n")
            if defs:
                header += "\n".join(defs) + "\n\n"
            body = header + ("\n\n".join(kept)) + "\n"
            open(out, "w", encoding="utf-8", newline="\n").write(body)
            print(f"  {os.path.basename(out):36} {len(kept)} buildings")
    return total


def build_texture(rgb):
    """Flat colour. The marker carries no surface detail on purpose - it is a map symbol, and the
    silhouette plus the colour is the whole of the information it conveys."""
    a = np.zeros((SIZE, SIZE, 4), np.uint8)
    a[..., 0], a[..., 1], a[..., 2] = rgb
    a[..., 3] = 255
    return Image.fromarray(a, "RGBA")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    mod_root = sys.argv[1]
    shape_key = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_SHAPE
    if shape_key not in SHAPES:
        sys.exit("shape must be one of: " + ", ".join(sorted(SHAPES)))
    mesh_file, shape_name = SHAPES[shape_key]

    outdir = os.path.join(mod_root, REL)
    os.makedirs(outdir, exist_ok=True)

    if not os.path.exists(os.path.join(outdir, mesh_file)):
        sys.exit(mesh_file + " is missing - run obj_to_pdxmesh.py first")
    print("shape: %s  (%s)" % (shape_key, mesh_file))

    lines = [
        "﻿# MOD(eotg) GENERATED by docs/tools/build_marker_assets.py - do not hand-edit.",
        "# One shared mesh, one flat colour per government. Selection happens in the buildings"
        " files,",
        "# where each asset entry carries a `governments = { ... }` filter.",
        "",
    ]
    for name, rgb, govs in MARKERS:
        tex = f"eotg_marker_{name}_diffuse.dds"
        save_dds_dxt5(build_texture(rgb), os.path.join(outdir, tex))
        lines += [
            "pdxmesh = {",
            f'\tname = "eotg_marker_{name}_mesh"',
            f'\tfile = "{mesh_file}"',
            "",
            "\tmeshsettings = {",
            f'\t\tname = "{shape_name}"',
            "\t\tindex = 0",
            f'\t\ttexture_diffuse = "{tex}"',
            '\t\ttexture_normal = "nonormal.dds"',
            '\t\ttexture_specular = "noproperties.dds"',
            f'\t\tshader = "{SHADER}"',
            # NO shader_file. Zero of vanilla's building assets set it; the only assets that do
            # are court and portrait ones, and every one of those points at court_scene.shader.
            # Setting it on a map asset pins the effect lookup to that court pipeline, where
            # eotg_marker does not exist, and the material is never created:
            #   Failed to create material with shader eotg_marker (in gfx/FX/court_scene.shader)
            # Left out, a building mesh resolves its effect against pdxmesh.shader, which is
            # where ours is defined.
            "\t}",
            "}",
            "",
        ]
    path = os.path.join(outdir, "eotg_markers.asset")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print(f"wrote {path}")
    for name, rgb, govs in MARKERS:
        who = ", ".join(govs) if govs else "FALLBACK (everything else)"
        print(f"  {name:15} rgb{rgb}  <- {who}")

    # The asset block that every holding building needs, ordered so the fallback comes last.
    snippet = ["\t\tassets = {"]
    for name, rgb, govs in MARKERS:
        snippet.append("\t\t\tasset = {")
        snippet.append("\t\t\t\ttype = pdxmesh")
        snippet.append(f'\t\t\t\tname = "eotg_marker_{name}_mesh"')
        if govs:
            snippet.append("\t\t\t\tgovernments = { " + " ".join(govs) + " }")
        snippet.append("\t\t\t}")
    snippet.append("\t\t}")
    frag = os.path.join(outdir, "assets_block.txt")
    open(frag, "w", encoding="utf-8", newline="\n").write("\n".join(snippet) + "\n")
    print(f"\nwrote {frag}")
    print("")
    print("overriding the holding buildings:")
    n = override_buildings(mod_root, "\n".join(snippet))
    print(f"  {n} buildings now draw the marker")


if __name__ == "__main__":
    main()
