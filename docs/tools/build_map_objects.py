"""Scatter map objects across terrain, the way vanilla scatters trees.

Why this exists. Everything else in this mod paints the ground: it is all pixels in
pdxterrain.shader, and pixels can only ever be a surface. Map objects are real geometry sitting on
the map - they parallax correctly, take the lighting, and occupy part of a province rather than all
of it. That is how vanilla gives a province local character, and it is the one tool we have that
cannot be mistaken for a texture. Broken Cluster's debris is the obvious first use: as a shader
effect it kept reading as extra stars, because a small bright blob on a dark field IS a star.

How CK3 stores this. An object entry names a `pdxmesh` and carries an explicit transform per
instance - vanilla's tree files run to 138k instances and 13 MB. The format, verified against
gfx/map/map_object_data/generated/:

    transform = "X Y Z  qx qy qz qw  sx sy sz"   (10 floats, one instance per line)
    count     = must equal the number of transform lines

  * Y is always 0 in vanilla's files: the engine clamps objects to terrain height.
  * World units are 1:1 with provinces.png pixels, and the map is 9216x4608, NOT 8192x4096.
  * **Z is flipped relative to image rows**: pixel_row = height - world_Z. Determined empirically -
    palm placements score 1641/4000 on land read directly and 4000/4000 flipped.
  * Vanilla trees use a yaw-only quaternion. Debris wants to tumble, so full rotations are used
    here; that is the one part of the format not copied from a working vanilla file.

Layers come from vanilla `layers.txt` and carry their own fade distances - `tree_high_layer` fades
out by zoom 9, so scattered objects disappear on their own at strategic zoom.

**The output is disposable.** Placements are tied to whatever map they were generated against, and
this mod will ship its own. docs/stellar_rivers_shader.md already says these files should simply
not exist once that happens. The durable artifact is this script, not what it emits, so the output
is gitignored.

Usage:
    python docs/tools/build_map_objects.py <mod root> [--game <dir>] [--dry-run] [--seed N]
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

GAME = r"D:\SteamLibrary\steamapps\common\Crusader Kings III\game"

# name -> what to scatter and where. Counts are deliberately low for now: this is a proof that
# the pipeline works end to end, and the placements are thrown away with the vanilla map anyway.
# name -> what to scatter and where.
#   mesh     a pdxmesh name that exists in the game's .asset files
#   terrains province_terrain values to scatter across
#   count    how many instances in total. Vanilla trees use 100k+; debris should be sparse enough
#            to read as scattered objects rather than ground cover.
#   scale    (min, max) uniform scale. 1.0 is the mesh's native size, and a cliff mesh is large,
#            so these are small. Needs eyeballing in game - it is the one value with no way to
#            check it from here.
#   tumble   True gives a full random orientation, False yaw only (vanilla's tree behaviour)
OBJECT_SETS = {
    # Mesh choice matters more than anything else here. Bounding boxes read out of the .mesh files:
    #   cliff_rock_01  3.02 long, flatness 0.53, 35 verts   <- a SLAB. Reads as a flat dark wedge.
    #   cliff_rock_02  1.95 long, flatness 0.75, 31 verts
    #   cliff_rock_03  2.60 long, flatness 0.81, 55 verts
    #   cliff_small_01 3.45 long, flatness 0.88, 128 verts  <- chunkiest and most detailed
    # flatness is min/max extent, so 1.0 is a cube and 0.5 is a plate. Anything low reads as a
    # shard rather than a rock once it tumbles, so the flat ones are not used.
    #
    # Scale is bracketed by two failed passes rather than reasoned from first principles:
    #   0.5-1.7 world unit chunks were all but invisible;
    #   2.4-6.9 were comically large, single rocks spanning a good part of a province.
    # So the readable range is roughly 1-2.5 units for field debris. Note the first of those was
    # also on the flat 35-vert slab, which reads smaller than a chunky mesh at equal scale.
    "eotg_debris_field": dict(
        mesh="eotg_cliff_small_01_mesh",     # 3.45 native -> 2.4-6.9 units
        layer="tree_high_layer",
        terrains=("hills",),
        count=11000,
        scale=(0.26, 0.62),
        tumble=True,
    ),
    "eotg_debris_field_b": dict(
        mesh="eotg_cliff_rock_03_mesh",      # 2.60 native -> 2.1-5.2 units
        layer="tree_high_layer",
        terrains=("hills",),
        count=6000,
        scale=(0.34, 0.80),
        tumble=True,
    ),
    # Impassable provinces are forced onto desert_mountains by build_terrain_index, so this also
    # litters every wasteland - which suits a barrier you are not meant to cross. Bigger chunks.
    "eotg_debris_barrier": dict(
        mesh="eotg_cliff_small_01_mesh",     # 3.45 native -> 5.2-12.1 units
        layer="tree_high_layer",
        terrains=("desert_mountains",),
        count=4500,
        scale=(0.45, 1.05),
        tumble=True,
    ),
}


def load_province_terrain(game):
    path = os.path.join(game, "common", "province_terrain", "00_province_terrain.txt")
    txt = open(path, encoding="utf-8-sig").read()
    default_land = re.search(r"default_land\s*=\s*(\w+)", txt).group(1)
    out = {}
    for m in re.finditer(r"^\s*(\d+)\s*=\s*(\w+)", txt, re.M):
        out[int(m.group(1))] = m.group(2)
    return out, default_land


def load_water(game):
    txt = open(os.path.join(game, "map_data", "default.map"), encoding="utf-8-sig").read()
    ids = set()
    for key in ("sea_zones", "river_provinces", "lakes", "impassable_seas"):
        for m in re.finditer(key + r"\s*=\s*(RANGE|LIST)\s*\{([^}]*)\}", txt):
            n = [int(x) for x in m.group(2).split()]
            ids.update(range(n[0], n[1] + 1) if m.group(1) == "RANGE" and len(n) == 2 else n)
    return ids


def province_ids(game):
    im = Image.open(os.path.join(game, "map_data", "provinces.png")).convert("RGB")
    W, H = im.size
    a = np.asarray(im)
    lut = np.zeros(1 << 24, np.uint16)
    with open(os.path.join(game, "map_data", "definition.csv"), encoding="utf-8-sig") as f:
        for row in csv.reader(f, delimiter=";"):
            if len(row) > 3 and row[0].strip().isdigit():
                lut[(int(row[1]) << 16) | (int(row[2]) << 8) | int(row[3])] = int(row[0])
    key = (a[:, :, 0].astype(np.uint32) << 16) | (a[:, :, 1].astype(np.uint32) << 8) | a[:, :, 2]
    return lut[key], W, H


def random_quats(rng, n, tumble):
    """Unit quaternions as (x, y, z, w), matching the order vanilla writes."""
    if not tumble:
        ang = rng.uniform(0.0, 2.0 * np.pi, n)
        z = np.zeros(n)
        return np.stack([z, np.sin(ang / 2), z, np.cos(ang / 2)], axis=1)
    # Shoemake: uniform over SO(3), so debris is not biased toward any axis
    u1, u2, u3 = rng.random(n), rng.random(n), rng.random(n)
    s1, s2 = np.sqrt(1 - u1), np.sqrt(u1)
    return np.stack([s1 * np.sin(2 * np.pi * u2), s1 * np.cos(2 * np.pi * u2),
                     s2 * np.sin(2 * np.pi * u3), s2 * np.cos(2 * np.pi * u3)], axis=1)


def sample_positions(rng, mask, want, W, H):
    """Rejection sampling: eligible terrain is a small fraction of the map, so drawing points and
    testing is far cheaper in memory than materialising every eligible pixel index."""
    xs, zs = [], []
    got = 0
    tries = 0
    while got < want and tries < 400:
        tries += 1
        batch = max(want * 4, 20000)
        px = rng.integers(0, W, batch)
        py = rng.integers(0, H, batch)
        keep = mask[py, px]
        if not keep.any():
            continue
        kx, ky = px[keep], py[keep]
        take = min(want - got, kx.size)
        # sub-pixel jitter so objects do not sit on a lattice
        xs.append(kx[:take] + rng.random(take))
        zs.append(H - (ky[:take] + rng.random(take)))
        got += take
    if got < want:
        print(f"    only placed {got}/{want} - eligible area may be too small")
    return np.concatenate(xs), np.concatenate(zs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mod_root")
    ap.add_argument("--game", default=GAME)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seed", type=int, default=20260926)
    args = ap.parse_args()

    rng = np.random.default_rng(args.seed)
    print("loading province map ...")
    pid, W, H = province_ids(args.game)
    print(f"  {W}x{H}  (world units are 1:1 with these pixels)")
    pterr, default_land = load_province_terrain(args.game)
    water = load_water(args.game)

    maxid = int(pid.max())
    outdir = os.path.join(args.mod_root, "gfx", "map", "map_object_data", "generated")
    os.makedirs(outdir, exist_ok=True)

    for name, cfg in OBJECT_SETS.items():
        want_terrain = set(cfg["terrains"])
        keep = np.zeros(maxid + 1, bool)
        for p, t in pterr.items():
            if p <= maxid and t in want_terrain and p not in water:
                keep[p] = True
        if default_land in want_terrain:
            print(f"  NOTE {name}: {default_land} is the default land terrain; unlisted provinces "
                  f"count as it, which this does not model")
        mask = keep[pid]
        frac = float(mask.mean())
        print(f"\n{name}: {cfg['mesh']} over {'/'.join(cfg['terrains'])}")
        print(f"  eligible area {frac * 100:.2f}% of the map, {int(mask.sum())} pixels")
        if frac <= 0.0:
            print("  nothing eligible, skipped")
            continue

        n = cfg["count"]
        xs, zs = sample_positions(rng, mask, n, W, H)
        n = xs.size
        q = random_quats(rng, n, cfg["tumble"])
        lo, hi = cfg["scale"]
        sc = rng.uniform(lo, hi, n)
        dens = n / (mask.sum() + 1e-9)
        print(f"  {n} instances, {dens * 1000:.2f} per 1000 eligible pixels, scale {lo}-{hi}")

        if args.dry_run:
            continue

        rows = [
            f"{xs[i]:.6f} 0.000000 {zs[i]:.6f} {q[i,0]:.6f} {q[i,1]:.6f} {q[i,2]:.6f} {q[i,3]:.6f} "
            f"{sc[i]:.6f} {sc[i]:.6f} {sc[i]:.6f}"
            for i in range(n)
        ]
        body = (
            "\ufeff# MOD(eotg) GENERATED by docs/tools/build_map_objects.py - do not hand-edit.\n"
            "# Placements are specific to the map they were generated against and are disposable;\n"
            "# the generator is the thing worth keeping.\n"
            "object={\n"
            f'\tname="{name}"\n'
            "\trender_pass=Map\n"
            "\tclamp_to_water_level=no\n"
            "\tgenerated_content=yes\n"
            f'\tlayer="{cfg["layer"]}"\n'
            f'\tpdxmesh="{cfg["mesh"]}"\n'
            f"\tcount={n}\n"
            '\ttransform="' + "\n".join(rows) + '"}\n'
        )
        path = os.path.join(outdir, name + ".txt")
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
        print(f"  wrote {path}  ({os.path.getsize(path) / 1048576:.1f} MB)")


if __name__ == "__main__":
    sys.exit(main())
