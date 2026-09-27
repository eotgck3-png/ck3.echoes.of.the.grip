"""Build the galactic province markers: one mesh, one colour per HOLDING TYPE.

The marker is a stone pedestal with a glowing emblem floating above it. Both are slots of a
single mesh (build_marker_mesh.py); this script writes the .asset that textures them and the
building overrides that make every holding draw it.

Colour says what KIND of holding this is - castle, city, temple, tribal, nomad - not who owns
it. So there is no `governments` filter: each holding's primary building simply names the mesh
for its own type. That also means the colour survives conquest, and survives a holding upgrade,
because every level of every primary building points at the same entry.

Holding graphics come from more places than is obvious, and all of them have to be covered or
medieval geometry keeps showing up:

  5 files with `assets = { asset = ... }`   castle, city, temple, temple citadel, tribal
  00_nomad_buildings.txt, bare `asset = `   nomad and herder camps
  99_background_graphics_buildings.txt      the WALLS ringing every holding, and - because the
                                            wall meshes carry the ground decal in a decal_plane
                                            sub-mesh - the patch of dirt underneath. Pointing
                                            these at western_walls_00_mesh, vanilla's own empty
                                            "no walls" mesh, removes both.

Special and legendary buildings also carry assets, but they are placed by history and this mod
places none yet. When it does, they will need the same treatment.

Usage:  python docs/tools/build_marker_assets.py <mod root>
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
SIZE = 128
MESH = "eotg_marker.mesh"
SHAPE = "eotg_markerShape"

# snap_to_terrain, not a new name. A NEW Effect declared in a shader file does not register - the
# lookup falls through to a default and the material is never created, so the mesh draws nothing.
# The mod's pdxmesh.shader adds EOTG_MARKER to this existing effect instead.
SHADER = "snap_to_terrain"

# The palette was supplied for governments; it is reused here for holding types, which is what
# the colour now means. Castle keeps gold, city keeps cyan, temple keeps violet.
HOLDINGS = [
    ("castle",         (231, 184,  75)),
    ("city",           ( 70, 199, 217)),
    ("temple",         (167, 124, 255)),
    ("temple_citadel", (206, 160, 255)),   # a temple variant, so a lighter violet
    ("tribal",         ( 85, 185, 107)),
    ("nomad",          (217,  87,  87)),
    ("herder",         (217, 138,  58)),
]

# Which holding type each primary building belongs to. Longest prefix wins, so temple_citadel_
# must be tested before temple_.
BUILDING_HOLDING = [
    ("temple_citadel_", "temple_citadel"),
    ("castle_",         "castle"),
    ("city_",           "city"),
    ("temple_",         "temple"),
    ("tribe_",          "tribal"),
    ("nomadic_camp_",   "nomad"),
    ("herder_camp_",    "herder"),
]

HOLDING_FILES = ("00_castle_buildings.txt", "00_city_buildings.txt", "00_temple_buildings.txt",
                 "temple_citadel_buildings.txt", "00_tribal_buildings.txt",
                 "00_nomad_buildings.txt")
WALLS_FILE = "99_background_graphics_buildings.txt"
EMPTY_WALL_MESH = "western_walls_00_mesh"

GAME = r"D:\SteamLibrary\steamapps\common\Crusader Kings III\game"


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


def holding_of(key):
    for prefix, holding in BUILDING_HOLDING:
        if key.startswith(prefix):
            return holding
    return None


def strip_assets(block):
    """Remove every asset declaration from a building block, in either spelling.

    Returns (block_without_assets, illustration, soundeffect). The illustration and sound are
    carried out because they are per-asset in vanilla, and dropping them silently costs the
    holding its picture in the UI and its ambient audio - a regression that is invisible on the
    map and only shows up when you click the holding.
    """
    illustration = soundeffect = None
    fallback_illu = fallback_snd = None
    while True:
        m = re.search(r"\n\t(assets|asset)\s*=\s*\{", block)
        if not m:
            break
        end = find_block(block, block.index("{", m.end() - 1))
        chunk = block[m.start():end]

        # Prefer a base-game asset. Vanilla lists DLC variants first, so taking the first match
        # gives castles a Norse illustration and Norse ambience for every culture. An asset with
        # no requires_dlc_flag is the one everyone sees.
        for am in re.finditer(r"\n\t+asset\s*=\s*\{", chunk):
            aend = find_block(chunk, chunk.index("{", am.end() - 1))
            entry = chunk[am.start():aend]
            dlc = "requires_dlc_flag" in entry
            im = re.search(r"illustration\s*=\s*(\S+)", entry)
            sm = re.search(r"soundeffect\s*=\s*\{", entry)
            snd = None
            if sm:
                send = find_block(entry, entry.index("{", sm.end() - 1))
                snd = entry[sm.start():send]
            if im and fallback_illu is None:
                fallback_illu = im.group(1)
            if snd and fallback_snd is None:
                fallback_snd = snd
            if not dlc:
                if im and illustration is None:
                    illustration = im.group(1)
                if snd and soundeffect is None:
                    soundeffect = snd
        block = block[:m.start()] + block[end:]
    return block, illustration or fallback_illu, soundeffect or fallback_snd


def asset_block(mesh_name, illustration, soundeffect):
    out = ["\n\tassets = {", "\t\tasset = {", "\t\t\ttype = pdxmesh",
           '\t\t\tname = "%s"' % mesh_name]
    if illustration:
        out.append("\t\t\tillustration = %s" % illustration)
    if soundeffect:
        out.append("\t\t\t" + soundeffect)
    out += ["\t\t}", "\t}"]
    return "\n".join(out)


def override_file(src, outdir, pick_mesh, header_note):
    """Copy every building that declares an asset, with our asset swapped in.

    Buildings merge by key, so emitting only the ones that define a model leaves every other
    vanilla building untouched. Everything else in the block is copied verbatim, including
    is_enabled, so gameplay and the wall-selection logic are unchanged - only what is drawn
    changes.
    """
    txt = open(src, encoding="utf-8-sig").read()

    # `@name = value` reader variables are FILE-scoped, so a copied building referring to
    # @holding_illustration_india resolves to nothing unless the definition travels with it.
    defs = re.findall(r"^@[A-Za-z_][A-Za-z0-9_]*\s*=\s*[^\n]+$", txt, re.M)

    kept, names = [], []
    for m in re.finditer(r"^([a-z0-9_]+)\s*=\s*\{", txt, re.M):
        key = m.group(1)
        end = find_block(txt, txt.index("{", m.start()))
        block = txt[m.start():end]
        if not re.search(r"\n\t(assets|asset)\s*=\s*\{", block):
            continue
        mesh_name = pick_mesh(key)
        if mesh_name is None:
            continue
        stripped, illu, snd = strip_assets(block)
        close = stripped.rindex("}")
        newblock = stripped[:close].rstrip() + "\n" + asset_block(mesh_name, illu, snd) + "\n}"
        kept.append(newblock)
        names.append(key)

    if not kept:
        return []
    out = os.path.join(outdir, "eotg_" + os.path.basename(src))
    header = ("\ufeff# MOD(eotg) GENERATED by docs/tools/build_marker_assets.py - do not "
              "hand-edit.\n# " + header_note + "\n# Vanilla definitions are copied verbatim with "
              "ONLY the asset declarations replaced,\n# so gameplay is untouched. Buildings merge "
              "by key, so every other building in the\n# vanilla file is left alone.\n\n")
    if defs:
        header += "\n".join(defs) + "\n\n"
    open(out, "w", encoding="utf-8", newline="\n").write(header + "\n\n".join(kept) + "\n")
    return names


def flat(rgb):
    a = np.zeros((SIZE, SIZE, 4), np.uint8)
    a[..., 0], a[..., 1], a[..., 2] = rgb
    a[..., 3] = 255
    return Image.fromarray(a, "RGBA")


def stone_texture(seed=7, size=256):
    """A quiet veined stone for the pedestal.

    Deliberately low contrast. The pedestal's job is to be legible and then get out of the way -
    it sits directly under a light source the player is meant to read, and busy rock would
    compete with it. Value sits mid-dark so it separates from both the pale and the dark terrain.
    """
    rng = np.random.default_rng(seed)
    y, x = np.mgrid[0:size, 0:size].astype(np.float64)
    field = np.zeros((size, size))
    amp, freq = 1.0, 2.0
    for _ in range(5):                       # value noise, a few octaves
        g = rng.random((int(freq) + 2, int(freq) + 2))
        yi = (y / size * freq).astype(int)
        xi = (x / size * freq).astype(int)
        fy = (y / size * freq) - yi
        fx = (x / size * freq) - xi
        fy, fx = fy * fy * (3 - 2 * fy), fx * fx * (3 - 2 * fx)
        v = (g[yi, xi] * (1 - fx) * (1 - fy) + g[yi, xi + 1] * fx * (1 - fy)
             + g[yi + 1, xi] * (1 - fx) * fy + g[yi + 1, xi + 1] * fx * fy)
        field += v * amp
        amp *= 0.5
        freq *= 2.0
    field = (field - field.min()) / (np.ptp(field) + 1e-9)
    veins = np.abs(np.sin((x * 0.055 + field * 7.0)))
    veins = np.clip(1.0 - veins, 0.0, 1.0) ** 6

    base = np.array([74, 78, 92], np.float64)      # cool grey, slightly blue
    light = np.array([132, 136, 150], np.float64)
    img = base + (light - base) * (0.35 * field + 0.65 * veins)[..., None]
    a = np.zeros((size, size, 4), np.uint8)
    a[..., :3] = np.clip(img, 0, 255).astype(np.uint8)
    a[..., 3] = 255
    return Image.fromarray(a, "RGBA")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    mod_root = sys.argv[1]
    outdir = os.path.join(mod_root, REL)
    os.makedirs(outdir, exist_ok=True)
    if not os.path.exists(os.path.join(outdir, MESH)):
        sys.exit(MESH + " is missing - run build_marker_mesh.py first")

    # Slot 1 glows because its properties map has r = 1; EOTG_MARKER multiplies its emissive and
    # rim by Properties.r. Slot 0 keeps vanilla's noproperties.dds (all zero, roughness 1) and so
    # lights as ordinary stone. That is what lets both slots share one effect - and they must,
    # because the effect carries the terrain snap and a slot without it would sit at sea level.
    glow = np.zeros((SIZE, SIZE, 4), np.uint8)
    glow[..., 0] = 255
    glow[..., 3] = 255
    save_dds_dxt5(Image.fromarray(glow, "RGBA"), os.path.join(outdir, "eotg_marker_glow_properties.dds"))
    save_dds_dxt5(stone_texture(), os.path.join(outdir, "eotg_marker_stone_diffuse.dds"))

    lines = ["\ufeff# MOD(eotg) GENERATED by docs/tools/build_marker_assets.py - do not hand-edit.",
             "# One mesh, two material slots: 0 is the stone pedestal, 1 the glowing emblem.",
             "# One entry per HOLDING TYPE - the colour says what kind of holding it is.",
             ""]
    for name, rgb in HOLDINGS:
        tex = "eotg_marker_%s_diffuse.dds" % name
        save_dds_dxt5(flat(rgb), os.path.join(outdir, tex))
        lines += [
            "pdxmesh = {",
            '\tname = "eotg_marker_%s_mesh"' % name,
            '\tfile = "%s"' % MESH,
            "",
            "\tmeshsettings = {",
            '\t\tname = "%s"' % SHAPE,
            "\t\tindex = 0",
            '\t\ttexture_diffuse = "eotg_marker_stone_diffuse.dds"',
            '\t\ttexture_normal = "nonormal.dds"',
            '\t\ttexture_specular = "noproperties.dds"',
            '\t\tshader = "%s"' % SHADER,
            "\t}",
            "\tmeshsettings = {",
            '\t\tname = "%s"' % SHAPE,
            "\t\tindex = 1",
            '\t\ttexture_diffuse = "%s"' % tex,
            '\t\ttexture_normal = "nonormal.dds"',
            '\t\ttexture_specular = "eotg_marker_glow_properties.dds"',
            '\t\tshader = "%s"' % SHADER,
            "\t}",
            "}",
            "",
        ]
    path = os.path.join(outdir, "eotg_markers.asset")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print("wrote %s" % path)
    for name, rgb in HOLDINGS:
        print("  %-15s rgb%s" % (name, rgb))

    print("\noverriding holding buildings (colour by holding type):")
    bdir = os.path.join(mod_root, "common", "buildings")
    os.makedirs(bdir, exist_ok=True)
    total = 0
    for fn in HOLDING_FILES:
        src = os.path.join(GAME, "common", "buildings", fn)
        if not os.path.exists(src):
            print("  skipped, not in this install: %s" % fn)
            continue
        names = override_file(
            src, bdir,
            lambda k: ("eotg_marker_%s_mesh" % holding_of(k)) if holding_of(k) else None,
            "Every level of every primary building points at the same entry, so the marker "
            "does not change on upgrade.")
        total += len(names)
        print("  %-36s %d  %s" % ("eotg_" + fn, len(names), ", ".join(names)))
    print("  %d primary buildings now draw the marker" % total)

    print("\nremoving the walls and the dirt patch under them:")
    src = os.path.join(GAME, "common", "buildings", WALLS_FILE)
    if os.path.exists(src):
        names = override_file(
            src, bdir, lambda k: EMPTY_WALL_MESH,
            "Walls off. The wall meshes carry the holding's ground decal in a decal_plane "
            "sub-mesh,\n# so pointing them at vanilla's empty western_walls_00_mesh removes the "
            "dirt patch too.\n# is_enabled is left exactly as vanilla wrote it; only the mesh "
            "changes.")
        print("  %-36s %d  %s" % ("eotg_" + WALLS_FILE, len(names), ", ".join(names)))


if __name__ == "__main__":
    main()
