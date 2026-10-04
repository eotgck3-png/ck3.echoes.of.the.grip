"""Give vanilla's rock meshes a space-appropriate skin, without authoring any geometry.

A CK3 .asset separates geometry from material:

    pdxmesh = {
        name = "cliff_rock_01_mesh"
        file = "cliff_rock_01.mesh"                        <- geometry
        meshsettings = { texture_diffuse = "..." ... }     <- material
    }

so a mod can declare its own pdxmesh that reuses a vanilla .mesh with different textures. That
matters here because .mesh is Paradox's @@b@ binary format, and authoring one blind - with no way
to load it and look - is not a reasonable bet. The silhouette of a weathered rock reads perfectly
well as an asteroid; only the colour was wrong.

Only the DIFFUSE is replaced. Measured off vanilla's own rock textures:

    diffuse     R=G=B 0.266, A 0.498       neutral mid-grey
    normal      R,G carry data, B exactly 0, A varies      (a convention, not a guess to make)
    properties  R=G=B 0, A 0.623           alpha only

Reusing vanilla's normal and properties means the surface detail and lighting response stay
correct and there is no convention to get wrong - the one thing being changed is the thing that
was actually wrong, which is that the rock is Earth-grey on a violet map.

IMPORTANT: no .asset in the game references a texture or mesh by path - every reference is a bare
filename resolved against the .asset's own directory. So this writes into the mod's copy of
gfx/models/mapitems/cliffs/, where `cliff_rock_01.mesh` will resolve to vanilla's file.

Usage:  python docs/tools/build_debris_material.py <mod root>
"""
from __future__ import annotations

import os
import re
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_terrain_materials import save_dds_dxt5, fbm, norm01

SIZE = 1024
REL = os.path.join("gfx", "models", "mapitems", "cliffs")

# Vanilla rock sits at 0.266 neutral. Debris should be darker and cold - it is unlit rock a long
# way from anything, and it has to sit on a violet nebula without reading as a brown boulder.
BASE_DARK = np.array([0.125, 0.120, 0.150])     # deep cold grey, faint violet lean
BASE_LIGHT = np.array([0.330, 0.318, 0.365])    # exposed faces catching a little light
IRON_TINT = np.array([0.240, 0.150, 0.115])     # rusty mineral streaks, used sparingly

# Which vanilla meshes to reskin. Each becomes an eotg_ pdxmesh reusing that geometry.
MESHES = ("cliff_rock_01", "cliff_rock_02", "cliff_rock_03", "cliff_small_01")

# The meshsettings `name` is a shape name baked into the .mesh when it was exported, and it is NOT
# derivable from the filename: cliff_rock_01 is "cliff_rock_0Shape1" while cliff_small_01 is
# "cliff_small_01Shape". Guessing gives a mesh that loads and renders untextured, so it is read
# out of the vanilla .asset rather than constructed.
GAME_CLIFFS = os.path.join(
    r"D:\SteamLibrary\steamapps\common\Crusader Kings III\game",
    "gfx", "models", "mapitems", "cliffs")


def mesh_slots(mesh):
    """Every meshsettings block in a vanilla .asset, in order.

    A mesh can carry MORE THAN ONE material slot and they are not interchangeable: cliff_small_01
    has index 0 on rock and index 1 on `plains_01_rough_diffuse` - a grass cap. Emitting only
    index 0 leaves slot 1 untextured, which renders as flat pale facets on every rock. The shape
    name is also baked in at export and is not derivable from the filename (cliff_rock_01 is
    "cliff_rock_0Shape1", cliff_small_01 is "cliff_small_01Shape"), so the whole structure is read
    from vanilla rather than constructed.
    """
    path = os.path.join(GAME_CLIFFS, mesh + ".asset")
    if not os.path.exists(path):
        sys.exit("vanilla asset missing, cannot read its material slots: " + path)
    txt = open(path, encoding="utf-8-sig").read()
    slots = []
    for m in re.finditer(r"meshsettings\s*=\s*\{(.*?)\n\t\}", txt, re.S):
        b = m.group(1)
        nm = re.search(r'name\s*=\s*"([^"]+)"', b)
        ix = re.search(r"index\s*=\s*(\d+)", b)
        nrm = re.search(r'texture_normal\s*=\s*"([^"]+)"', b)
        spc = re.search(r'texture_specular\s*=\s*"([^"]+)"', b)
        if nm and ix:
            slots.append(dict(name=nm.group(1), index=int(ix.group(1)),
                              normal=nrm.group(1) if nrm else "nonormal.dds",
                              specular=spc.group(1) if spc else "noproperties.dds"))
    if not slots:
        sys.exit("no meshsettings found in " + path)
    return slots


def build_diffuse(seed):
    rng = np.random.default_rng(seed)
    # Two scales of mottling: broad shading across the body, fine grain for surface texture.
    broad = norm01(fbm(SIZE, octaves=4, base=3, rng=rng))
    fine = norm01(fbm(SIZE, octaves=5, base=14, rng=rng))
    mix = np.clip(broad * 0.70 + fine * 0.30, 0, 1)

    rgb = (BASE_DARK[None, None, :] * (1 - mix[..., None])
           + BASE_LIGHT[None, None, :] * mix[..., None])

    # Sparse mineral streaks: only where a separate field is high, so most of the rock stays cold.
    iron = np.clip((norm01(fbm(SIZE, octaves=4, base=7, rng=rng)) - 0.68) / 0.32, 0, 1) ** 1.5
    rgb = rgb * (1 - 0.55 * iron[..., None]) + IRON_TINT[None, None, :] * 0.55 * iron[..., None]

    # Pitting: small dark craters. Sparse, so the surface reads as pocked rather than noisy.
    pits = np.clip((norm01(fbm(SIZE, octaves=3, base=26, rng=rng)) - 0.74) / 0.26, 0, 1)
    rgb = rgb * (1 - 0.55 * pits[..., None])

    rgb = np.clip(rgb, 0, 1)
    a = np.full((SIZE, SIZE), 0.498, np.float32)        # match vanilla's alpha level
    out = np.dstack([rgb, a])
    return Image.fromarray((out * 255).astype(np.uint8), "RGBA")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    mod_root = sys.argv[1]
    outdir = os.path.join(mod_root, REL)
    os.makedirs(outdir, exist_ok=True)

    tex = "eotg_debris_01_diffuse.dds"
    img = build_diffuse(20260926)
    save_dds_dxt5(img, os.path.join(outdir, tex))
    lum = np.asarray(img).astype(np.float32)[..., :3].mean() / 255
    print(f"wrote {tex}  mean luminance {lum:.3f}  (vanilla rock was 0.266)")

    lines = [
        "﻿# MOD(eotg) GENERATED by docs/tools/build_debris_material.py - do not hand-edit.",
        "# Vanilla rock GEOMETRY with an EotG skin. No .mesh is authored: .asset separates the two,",
        "# and a weathered rock silhouette already reads as an asteroid - only the colour was wrong.",
        "# Normal and properties are deliberately vanilla's: their channel conventions are unusual",
        "# (normal has B=0, properties uses alpha only) and there is nothing to gain by guessing at",
        "# them when the thing being fixed is the diffuse.",
        "",
    ]
    for m in MESHES:
        slots = mesh_slots(m)
        lines += ["pdxmesh = {", f'\tname = "eotg_{m}_mesh"', f'\tfile = "{m}.mesh"', ""]
        for sl in slots:
            # Our diffuse goes on EVERY slot. Slot 1 of cliff_small_01 is a grass cap in vanilla;
            # on an asteroid it should be rock like the rest, and leaving it out is what made
            # every rock render with flat pale facets.
            lines += [
                "\tmeshsettings = {",
                f'\t\tname = "{sl["name"]}"',
                f'\t\tindex = {sl["index"]}',
                f'\t\ttexture_diffuse = "{tex}"',
                f'\t\ttexture_normal = "{sl["normal"]}"',
                f'\t\ttexture_specular = "{sl["specular"]}"',
                '\t\tshader = "standard"',
                '\t\tshader_file = "gfx/FX/pdxmesh.shader"',
                "\t}",
            ]
        lines += ["}", ""]
    path = os.path.join(outdir, "eotg_debris.asset")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    print(f"wrote {path}")
    print(f"  {len(MESHES)} meshes: " + ", ".join(f"eotg_{m}_mesh" for m in MESHES))
    for m in MESHES:
        sl = mesh_slots(m)
        detail = ", ".join(f'{s["index"]}:{s["name"]}' for s in sl)
        flag = "  <- multi-slot" if len(sl) > 1 else ""
        print(f"    eotg_{m}_mesh  <- {m}.mesh   slots {detail}{flag}")


if __name__ == "__main__":
    main()
