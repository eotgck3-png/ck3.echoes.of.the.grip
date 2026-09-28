"""
Paint EotG terrain materials onto a map.

Reads the authoritative terrain assignment (provinces.png + definition.csv +
common/province_terrain) and writes the two textures CK3 samples at runtime:

    gfx/map/terrain/detail_index.tga      RGBA, each channel = a material index (4 slots per pixel)
    gfx/map/terrain/detail_intensity.tga  RGBA, the matching blend weights

Material indices are positional in materials.settings, so this script reads that file
to resolve ids -> indices rather than hardcoding them.

Variant count is per-terrain (area-weighted), so this discovers each terrain's variants from
materials.settings rather than assuming two. Regions pick an adjacent pair of variants and blend
within it by low-frequency noise, so the map does not look uniformly tiled and no terrain ever
needs more than two of the four slots. Coastal land gets an edge material.

Usage:
    python build_terrain_index.py <mod root> [--game <CK3 game dir>]

On the vanilla map this is throwaway output (it bakes vanilla's landmass) - it exists so the
material set can be seen working before the mod's own map_data lands. Point --game at the
mod's own map later and the same script produces the real thing.
"""
import os, sys, re, csv
import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
GAME = r"D:\SteamLibrary\steamapps\common\Crusader Kings III\game"

# "impassable" is never named by province_terrain - it exists only as the override target below.
TERRAINS = ["plains", "farmlands", "hills", "mountains", "desert", "desert_mountains", "oasis",
            "jungle", "forest", "taiga", "wetlands", "steppe", "floodplains", "drylands",
            "terraced_hills", "impassable"]
SEA_MAT = "eotg_desert_01"          # under the void shader, never visible; must still be valid
EDGE_MATS = ("eotg_edge_01", "eotg_edge_02")


def material_indices(mod_root):
    """Resolve material id -> positional index from the mod's materials.settings."""
    p = os.path.join(mod_root, "gfx", "map", "terrain", "materials.settings")
    ids = re.findall(r'id\s*=\s*"([^"]+)"', open(p, encoding="utf-8-sig").read())
    return {mid: i for i, mid in enumerate(ids)}, ids


def discover_variants(ids):
    """terrain -> [material ids], read from materials.settings rather than assumed.

    Anchored so 'desert' does not swallow 'desert_mountains_01'. Variant count is per-terrain
    (area-weighted), so this must not assume two.
    """
    out = {}
    for t in TERRAINS:
        pat = re.compile(rf"^eotg_{re.escape(t)}_(\d+)$")
        v = sorted((m.group(0) for m in (pat.match(i) for i in ids) if m),
                   key=lambda s: int(s.rsplit("_", 1)[1]))
        if not v:
            raise SystemExit(f"no materials found for terrain '{t}' in materials.settings")
        out[t] = v
    return out


def load_province_terrain(game):
    """province id -> terrain name, honouring the default_* fallbacks."""
    txt = open(os.path.join(game, "common", "province_terrain", "00_province_terrain.txt"),
               encoding="utf-8-sig").read()
    default_land = re.search(r"default_land\s*=\s*(\w+)", txt).group(1)
    out = {}
    for m in re.finditer(r"^(\d+)\s*=\s*(\w+)", txt, re.M):
        out[int(m.group(1))] = m.group(2)
    return out, default_land


def load_water_provinces(game):
    """Sea/lake/river province ids. province_terrain lists only land, so water comes from default.map."""
    txt = open(os.path.join(game, "map_data", "default.map"), encoding="utf-8-sig").read()
    ids = set()
    for key in ("sea_zones", "river_provinces", "lakes", "impassable_seas"):
        for m in re.finditer(key + r"\s*=\s*(RANGE|LIST)\s*\{([^}]*)\}", txt):
            nums = [int(n) for n in m.group(2).split()]
            if m.group(1) == "RANGE" and len(nums) == 2:
                ids.update(range(nums[0], nums[1] + 1))
            else:
                ids.update(nums)
    return ids


IMPASSABLE_TERRAIN = "impassable"   # its own material since 2026-09-27. It used to be
                                    # desert_mountains, but the two sets are disjoint, so the
                                    # 1188 wastelands and 304 real Barren Barriers could not be
                                    # tuned apart. Darkest and emptiest on the map: impassable
                                    # should recede, not draw the eye.


def load_impassable_land(game):
    """Province ids declared impassable_mountains in default.map."""
    txt = open(os.path.join(game, "map_data", "default.map"), encoding="utf-8-sig").read()
    ids = set()
    for m in re.finditer(r"impassable_mountains\s*=\s*(RANGE|LIST)\s*\{([^}]*)\}", txt):
        nums = [int(n) for n in m.group(2).split()]
        if m.group(1) == "RANGE" and len(nums) == 2:
            ids.update(range(nums[0], nums[1] + 1))
        else:
            ids.update(nums)
    return ids


def main():
    mod_root = sys.argv[1]
    game = sys.argv[sys.argv.index("--game") + 1] if "--game" in sys.argv else GAME

    idx_of, all_ids = material_indices(mod_root)
    variants = discover_variants(all_ids)
    print(f"materials.settings: {len(all_ids)} entries; "
          f"{sum(len(v) for v in variants.values())} terrain materials across {len(variants)} terrains")
    for mid in list(EDGE_MATS) + [SEA_MAT]:
        if mid not in idx_of:
            raise SystemExit(f"material id missing from materials.settings: {mid}")

    # --- province id per pixel -------------------------------------------------
    print("loading provinces.png ...")
    prov = np.asarray(Image.open(os.path.join(game, "map_data", "provinces.png")).convert("RGB"))
    H, W, _ = prov.shape
    print(f"  {W}x{H}")

    lut = np.zeros(1 << 24, np.uint16)
    with open(os.path.join(game, "map_data", "definition.csv"), encoding="utf-8-sig") as f:
        for row in csv.reader(f, delimiter=";"):
            if len(row) < 4 or not row[0].strip().isdigit():
                continue
            pid, r, g, b = (int(row[0]), int(row[1]), int(row[2]), int(row[3]))
            lut[(r << 16) | (g << 8) | b] = pid
    key = (prov[:, :, 0].astype(np.uint32) << 16) | (prov[:, :, 1].astype(np.uint32) << 8) | prov[:, :, 2]
    pid = lut[key]
    del key, prov

    # --- terrain per pixel -----------------------------------------------------
    pterr, default_land = load_province_terrain(game)
    names = TERRAINS
    tcode = {n: i for i, n in enumerate(names)}
    SEA = 254
    maxid = int(pid.max())
    tlut = np.full(maxid + 1, tcode[default_land], np.uint8)
    for p in load_water_provinces(game):
        if p <= maxid:
            tlut[p] = SEA
    for p, t in pterr.items():
        if p > maxid:
            continue
        tlut[p] = SEA if t in ("sea", "coastal_sea") else tcode.get(t, tcode[default_land])
    # Impassable land overrides province_terrain: a barrier should read as a barrier
    # everywhere, not inherit the terrain it happens to carry.
    imp = load_impassable_land(game)
    n_imp = 0
    for p in imp:
        if p <= maxid and tlut[p] != SEA:
            tlut[p] = tcode[IMPASSABLE_TERRAIN]
            n_imp += 1
    print(f"  impassable land forced to {IMPASSABLE_TERRAIN}: {n_imp} provinces")
    tlut[0] = SEA                       # province 0 is the map's unassigned colour
    terr = tlut[pid]
    del pid

    water = terr == SEA
    print(f"  land {100 * (~water).mean():.1f}%  sea {100 * water.mean():.1f}%")

    # --- variant mix + coastal edge -------------------------------------------
    def lowfreq(cells, seed):
        g = np.random.default_rng(seed).random((H // cells + 2, W // cells + 2)).astype(np.float32)
        return np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC),
                          dtype=np.float32) / 255.0
    mixf = lowfreq(64, 7)     # blend weight within a variant pair
    pickf = lowfreq(220, 11)  # which adjacent pair of variants a region uses

    # coastal band: land pixels within a few px of water (cheap dilate by shifting)
    edge = np.zeros((H, W), bool)
    for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1), (2, 0), (-2, 0), (0, 2), (0, -2)):
        edge |= np.roll(water, (dy, dx), axis=(0, 1))
    edge &= ~water

    index = np.zeros((H, W, 4), np.uint8)
    inten = np.zeros((H, W, 4), np.uint8)

    # --- neighbouring terrain, for cross-terrain blending ----------------------
    # Slots 0/1 hold this pixel's own terrain. Without a *different* terrain sharing the pixel,
    # CalcHeightBlendFactors has nothing to interlock and every boundary is a hard province-shaped
    # cut. So find, for each pixel near a boundary, which other terrain is closest, and how close.
    # Nearer boundary -> heavier weight; the height maps then shape the actual edge.
    NONE = 255
    near_t = np.full((H, W), NONE, np.uint8)
    near_w = np.zeros((H, W), np.float32)
    land = terr != SEA
    for radius, weight in ((20, 0.08), (16, 0.14), (12, 0.22), (9, 0.30), (6, 0.38), (4, 0.45), (2, 0.50)):
        for dy, dx in ((radius, 0), (-radius, 0), (0, radius), (0, -radius),
                       (radius, radius), (radius, -radius), (-radius, radius), (-radius, -radius)):
            other = np.roll(terr, (dy, dx), axis=(0, 1))
            m = land & (other != terr) & (other != SEA)
            near_t[m] = other[m]
            near_w[m] = weight
    has_near = near_t != NONE
    print(f"  cross-terrain blend band covers {100 * has_near.mean():.1f}% of the map")

    for n in names:
        m = (terr == tcode[n]) & ~edge
        if not m.any():
            continue
        V = variants[n]
        if len(V) == 1:
            index[..., 0][m] = idx_of[V[0]]
            inten[..., 0][m] = 255
        else:
            # regions pick an adjacent pair of variants, then blend within that pair,
            # so a 3-variant terrain varies across the map without ever needing 3 slots
            vidx = np.array([idx_of[v] for v in V], np.uint8)
            sel = np.clip((pickf[m] * (len(V) - 1)).astype(np.int32), 0, len(V) - 2)
            index[..., 0][m] = vidx[sel]
            index[..., 1][m] = vidx[sel + 1]
            w = np.clip(mixf[m] * 1.6 - 0.3, 0.08, 0.92)
            inten[..., 0][m] = (w * 255).astype(np.uint8)
            inten[..., 1][m] = ((1 - w) * 255).astype(np.uint8)
        print(f"  {n:17s} {100 * m.mean():5.2f}%  {len(V)}x -> {', '.join(V)}")

    # slot 2: the neighbouring terrain, so the height blend can interlock the two
    for n in names:
        m = has_near & (near_t == tcode[n]) & ~edge & (terr != SEA)
        if not m.any():
            continue
        index[..., 2][m] = idx_of[variants[n][0]]
        inten[..., 2][m] = (near_w[m] * 255).astype(np.uint8)

    index[..., 0][edge] = idx_of[EDGE_MATS[0]]
    index[..., 1][edge] = idx_of[EDGE_MATS[1]]
    inten[..., 0][edge] = 200
    inten[..., 1][edge] = 120
    print(f"  {'edge':17s} {100 * edge.mean():5.2f}% -> {EDGE_MATS[0]} / {EDGE_MATS[1]}")

    index[..., 0][water] = idx_of[SEA_MAT]
    inten[..., 0][water] = 255

    out = os.path.join(mod_root, "gfx", "map", "terrain")
    os.makedirs(out, exist_ok=True)
    print("writing detail_index.tga ...")
    Image.fromarray(index, "RGBA").save(os.path.join(out, "detail_index.tga"))
    print("writing detail_intensity.tga ...")
    Image.fromarray(inten, "RGBA").save(os.path.join(out, "detail_intensity.tga"))
    for f in ("detail_index.tga", "detail_intensity.tga"):
        print(f"  {f}: {os.path.getsize(os.path.join(out, f)) / 1e6:.0f} MB")


if __name__ == "__main__":
    main()
