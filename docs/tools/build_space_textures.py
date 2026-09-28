import struct, os, sys, math, re
from PIL import Image, ImageFilter
import numpy as np
M = sys.argv[1]
PREV = os.path.dirname(os.path.abspath(__file__))

def dds_bgra(img, path, mips=True):
    """Uncompressed A8R8G8B8 DDS with a full mip chain."""
    levels = [img.convert("RGBA")]
    if mips:
        while levels[-1].size != (1, 1):
            w, h = levels[-1].size
            levels.append(levels[-1].resize((max(1, w // 2), max(1, h // 2)), Image.BOX))
    w, h = img.size
    flags = 0x1007 | 0x8 | (0x20000 if mips else 0)
    hdr = b"DDS " + struct.pack("<IIIIIII", 124, flags, h, w, w * 4, 0, len(levels)) + b"\0" * 44
    hdr += struct.pack("<IIIIIIII", 32, 0x41, 0, 32, 0xff0000, 0xff00, 0xff, 0xff000000)
    caps = 0x1000 | (0x400008 if mips else 0)
    hdr += struct.pack("<IIIII", caps, 0, 0, 0, 0)
    data = b"".join(np.asarray(lv)[:, :, [2, 1, 0, 3]].tobytes() for lv in levels)
    open(path, "wb").write(hdr + data)

def dds_rgb(img, path):
    img = img.convert("RGB"); w, h = img.size
    hdr = b"DDS " + struct.pack("<IIIIIII", 124, 0x1007 | 0x8, h, w, w * 3, 0, 0) + b"\0" * 44
    hdr += struct.pack("<IIIIIIII", 32, 0x40, 0, 24, 0xff0000, 0xff00, 0xff, 0) + struct.pack("<IIIII", 0x1000, 0, 0, 0, 0)
    open(path, "wb").write(hdr + np.asarray(img)[:, :, [2, 1, 0]].tobytes())

# Halos roughly halved on every border, 2026-09-27. They were authored at up to 0.45 of
# the texture against a 0.07 core, which is a wide soft glow either side of a thin line.
# At normal zoom that reads as a lit border; at maximum zoom the halo is enormous on
# screen and the borders become thick bands that swamp the terrain. The core is what
# carries the line, so the halo can come down without losing legibility.
# Border WIDTH is engine geometry, not the texture - proved by painting every border flat
# and full-alpha: they all came out the same thickness. So a border cannot be made thin.
# What it can be is quiet.
#
# Vanilla makes the high-frequency borders - province and county, which are on every
# boundary - PURE BLACK, and a wide dark band on a bright map reads as a seam. Ours were
# saturated lavender at luminance 0.81 on a dark map, so the same width read as neon.
# A dark map cannot use black, so these are desaturated and dim instead: light enough to
# separate two provinces, far too dull to glow. The realm borders stay coloured, because
# there are few of them and they are meant to be read.
hx = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
GOLD = hx("#FFC84D"); PALEGOLD = hx("#FFF2C0"); VIOLET = hx("#8A3BE0"); PURPLE = hx("#9A4FFF"); LAV = hx("#D6B4F0")
CRIMSON = hx("#E0325A"); TEAL = hx("#2FB8B0"); EMERALD = hx("#2E9C6A"); SAPPH = hx("#3A6CFF"); WHITE = (255, 255, 255)

# ---------------- borders: horizontal strip, x along the border, y across ----------------
# Vanilla's border textures are 85 wide x 86 tall, and the HEIGHT is the across-border axis -
# it is what sets how wide the border is drawn on the map. Ours were generated at 128x128, so
# every border on the map was about 1.5x wider than the engine expects before the halo was even
# counted. At normal zoom that just looks bold; at maximum zoom they become slabs.
#
# Match vanilla exactly. The halo is a FRACTION of the height, so the two interact: the halved
# halos in the previous commit were correct but could not fix this on their own.
BORDER_W, BORDER_H = 85, 86


def border(color, core=0.06, halo=0.35, strength=1.0, dash=None, core_col=None, size=None):
    w, h = (size, size) if size else (BORDER_W, BORDER_H)
    cc = core_col or tuple(min(255, int(c * 0.45 + 255 * 0.55)) for c in color)
    y = (np.arange(h) + 0.5) / h
    d = np.abs(y - 0.5) * 2
    a_core = np.exp(-(d * d) / (core * core))
    a_halo = np.exp(-(d * d) / (halo * halo)) * 0.45
    t = a_core / (a_core + a_halo + 1e-6)
    col = np.stack([cc[i] * t + color[i] * (1 - t) for i in range(3)], -1)  # (size,3)
    a = np.minimum(1.0, (a_core + a_halo) * strength)                      # (size,)
    x = (np.arange(w) + 0.5) / w
    k = np.ones(w)
    if dash:
        on, off = dash
        k = np.where((x % (on + off)) < on, 1.0, 0.15)
    img = np.zeros((h, w, 4), np.float32)
    img[:, :, :3] = col[:, None, :]
    img[:, :, 3] = (a[:, None] * k[None, :]) * 255
    return Image.fromarray(img.astype(np.uint8), "RGBA")

B = os.path.join(M, "gfx", "map", "borders")
spec = {
    "border_water": border(hx("#5A6478"), core=0.03, halo=0.07, strength=0.16),
    "border_province": border(hx("#6E7A90"), core=0.025, halo=0.05, strength=0.20, dash=(0.18, 0.12)),
    "border_county": border(hx("#7E8AA2"), core=0.030, halo=0.06, strength=0.30),
    "border_domain": border(GOLD, core=0.040, halo=0.10, strength=0.55),
    "border_other_realm": border(GOLD, core=0.045, halo=0.11, strength=0.65),
    "border_my_realm": border(PURPLE, core=0.045, halo=0.11, strength=0.65),
    "border_sub_realm": border(hx("#8E7AB8"), core=0.035, halo=0.08, strength=0.35),
    "border_hovered_realm": border(PALEGOLD, core=0.065, halo=0.22, strength=1.0, core_col=WHITE),
    "border_hovered_realm_flat_map": border(PALEGOLD, core=0.065, halo=0.22, strength=1.0, core_col=WHITE),
    "border_highlighted_province": border(GOLD, core=0.07, halo=0.35, strength=1.0, dash=(0.3, 0.1)),
    "selection_highlight": border(GOLD, core=0.08, halo=0.4, strength=1.0, dash=(0.3, 0.1), core_col=WHITE),
    "selection_highlight_flat_map": border(GOLD, core=0.08, halo=0.4, strength=1.0, dash=(0.3, 0.1), core_col=WHITE),
    "border_selected_realm": border(PALEGOLD, core=0.09, halo=0.5, strength=1.0, core_col=WHITE),
    "border_selected_realm_flat_map": border(PALEGOLD, core=0.09, halo=0.5, strength=1.0, core_col=WHITE),
    "border_selected_realm_diplomatic": border(TEAL, core=0.09, halo=0.5, strength=1.0),
    "border_selected_realm_diplomatic_flat_map": border(TEAL, core=0.09, halo=0.5, strength=1.0),
    "border_selected_realm_overlord": border(GOLD, core=0.09, halo=0.5, strength=1.0, core_col=WHITE),
    "border_selected_realm_overlord_flat_map": border(GOLD, core=0.09, halo=0.5, strength=1.0, core_col=WHITE),
    "border_selected_realm_overlord_diplomatic": border(TEAL, core=0.09, halo=0.5, strength=1.0, core_col=WHITE),
    "border_selected_realm_overlord_diplomatic_flat_map": border(TEAL, core=0.09, halo=0.5, strength=1.0, core_col=WHITE),
    "border_impassable": border(CRIMSON, core=0.05, halo=0.25, strength=0.7, dash=(0.12, 0.12)),
    "border_war": border(CRIMSON, core=0.08, halo=0.4, strength=1.0),
    "border_war_ally": border(TEAL, core=0.08, halo=0.4, strength=1.0),
    "border_war_target": border(CRIMSON, core=0.09, halo=0.45, strength=1.0, core_col=WHITE),
    "border_civil_war": border(hx("#FF7A30"), core=0.08, halo=0.4, strength=1.0),
    "border_realm_explorer_independent": border(GOLD, core=0.07, halo=0.35, strength=1.0),
    "border_realm_explorer_vassal": border(PURPLE, core=0.06, halo=0.3, strength=0.9),
    "epidemic": border(EMERALD, core=0.08, halo=0.4, strength=1.0),
    "migrate": border(SAPPH, core=0.08, halo=0.4, strength=1.0),
    "migrate_domain": border(SAPPH, core=0.07, halo=0.3, strength=0.9),
    "my_top_realm": border(PALEGOLD, core=0.08, halo=0.4, strength=1.0, core_col=WHITE),
    "struggle": border(CRIMSON, core=0.07, halo=0.35, strength=1.0),
    "struggle_involved": border(GOLD, core=0.07, halo=0.35, strength=1.0),
    "struggle_uninvolved": border(VIOLET, core=0.06, halo=0.3, strength=0.8),
    "struggle_interloper": border(TEAL, core=0.07, halo=0.35, strength=1.0),
}
for n, im in spec.items():
    dds_bgra(im, os.path.join(B, n + ".dds"))
print("borders:", len(spec))
# preview sheet
sheet = Image.new("RGBA", (256, 32 * 6), (30, 30, 40, 255))
for i, n in enumerate(["border_county", "border_other_realm", "border_my_realm", "selection_highlight", "border_war", "border_impassable"]):
    sheet.alpha_composite(spec[n].resize((256, 32)), (0, 32 * i))
sheet.save(os.path.join(PREV, "borders_new.png"))

# ---------------- movement arrows: 256x256 atlas; left half shaft, right half head; bottom half = passed ----------------
def arrow_atlas(color, core_col=WHITE, size=256):
    h = size // 2; w = size // 2
    img = np.zeros((size, size, 4), np.float32)
    yy = (np.arange(h) + 0.5) / h
    d = np.abs(yy - 0.5) * 2                       # (h,)
    uu = (np.arange(w) + 0.5) / w                  # (w,)
    # shaft
    ac = np.exp(-(d * d) / (0.08 ** 2)); ah = np.exp(-(d * d) / (0.4 ** 2)) * 0.4
    t = ac / (ac + ah + 1e-6); a = ac + ah
    shaft_col = np.stack([core_col[i] * t + color[i] * (1 - t) for i in range(3)], -1)  # (h,3)
    # head: triangle pointing +x
    half = np.maximum(0.02, 0.48 * (1 - (uu - 0.05) / 0.9))                              # (w,)
    dd = d[:, None] / (half[None, :] * 2)                                                 # (h,w)
    inside = (dd <= 1) & (uu[None, :] >= 0.05) & (uu[None, :] <= 0.95)
    edge = np.where(inside, np.exp(-((1 - dd) ** 2) / (0.25 ** 2)), 0)
    fill = np.where(inside, 0.35 * np.exp(-(dd * dd) / (0.8 ** 2)), 0)
    ta = edge / (edge + fill + 1e-6); aa = edge * 0.9 + fill
    head_col = np.stack([core_col[i] * ta + color[i] * (1 - ta) for i in range(3)], -1)  # (h,w,3)
    for row, dim in ((0, 1.0), (1, 0.45)):
        img[row * h:(row + 1) * h, :w, :3] = shaft_col[:, None, :]
        img[row * h:(row + 1) * h, :w, 3] = np.minimum(1, a * dim)[:, None] * 255
        img[row * h:(row + 1) * h, w:, :3] = head_col
        img[row * h:(row + 1) * h, w:, 3] = np.minimum(1, aa * dim) * 255
    return Image.fromarray(img.astype(np.uint8), "RGBA")

A = os.path.join(M, "gfx", "map", "movement_arrows")
arrows = {"movearrow_move": GOLD, "attackarrow_move": CRIMSON, "retreatarrow_move": VIOLET, "shortarrow": PALEGOLD,
          "locked_shortarrow": hx("#8878A0"), "arrow_locked": hx("#8878A0"), "arrow_silk_road": TEAL}
for n, c in arrows.items():
    im = arrow_atlas(c)
    dds_bgra(im, os.path.join(A, n + ".dds")); dds_bgra(im, os.path.join(A, n + "_flat_map.dds"))
arrow_atlas(GOLD).save(os.path.join(PREV, "arrow_new.png"))
print("arrows:", len(arrows) * 2)

# ---------------- flat map: the zoomed-out view ------------------------------------------------
#
# THIS TEXTURE, not any shader, is what the player sees at full zoom out. PixelShaderFlatMap in
# pdxterrain.shader does nothing but read it, so nothing here can be faded or gated at runtime.
# Several rounds of shader edits were spent on artefacts that live in this file. If something is
# only visible when fully zoomed out, look here first.
#
# The land/sea mask comes from the GAME DATA - provinces.png keyed through definition.csv against
# the sea and lake lists in default.map. The previous version guessed it from the colours of
# vanilla's parchment map, which also classified the compass rose, the cartouches and assorted
# ink as land: that is where the purple circle near Iceland and the stray blobs between Iceland
# and Norway came from. A heuristic over someone else's artwork was never going to be right.
FLATMAP_STARS  = False   # point stars, masked to sea. Off - this was "stars in the ocean".
FLATMAP_NEBULA = 1.0     # the slow cloud over open water; this is the ocean's only colour
FLATMAP_COAST  = 0.45    # coastline rim

Image.MAX_IMAGE_PIXELS = None
W, H = 4608, 2304
GAME = r"D:\SteamLibrary\steamapps\common\Crusader Kings III\game"


def land_sea_mask(w, h):
    """Exact land mask at (w, h), from province data rather than from the paper map's pixels.

    Rivers are deliberately counted as LAND. They are river_provinces in default.map, but drawing
    them as water threads a dark line down every valley and then rims it with the coast glow,
    which reads as noise at strategic zoom. The mod draws its stellar lanes with the river
    shaders instead.
    """
    water = set()
    txt = open(os.path.join(GAME, "map_data", "default.map"), encoding="utf-8-sig").read()
    for kind in ("sea_zones", "lakes", "impassable_seas"):
        for m in re.finditer(kind + r"\s*=\s*(RANGE|LIST)\s*\{([^}]*)\}", txt):
            nums = [int(x) for x in m.group(2).split()]
            if m.group(1) == "RANGE" and len(nums) == 2:
                water.update(range(nums[0], nums[1] + 1))
            else:
                water.update(nums)

    lut = np.zeros(1 << 24, np.int32)
    for line in open(os.path.join(GAME, "map_data", "definition.csv"),
                     encoding="utf-8-sig", errors="replace"):
        f = line.strip().split(";")
        if len(f) < 4 or not f[0].isdigit():
            continue
        try:
            i, r, g, b = int(f[0]), int(f[1]), int(f[2]), int(f[3])
        except ValueError:
            continue
        lut[(r << 16) | (g << 8) | b] = i

    prov = np.array(Image.open(os.path.join(GAME, "map_data", "provinces.png")).convert("RGB"))
    key = (prov[:, :, 0].astype(np.uint32) << 16) | (prov[:, :, 1].astype(np.uint32) << 8) | prov[:, :, 2]
    ids = lut[key]
    land = (~np.isin(ids, np.fromiter(water, np.int32))) & (ids > 0)
    return np.asarray(Image.fromarray((land * 255).astype(np.uint8)).resize((w, h), Image.BOX)
                      ).astype(np.float32) / 255.0


lmf = land_sea_mask(W, H)
lm8 = Image.fromarray((lmf * 255).astype(np.uint8))
blur = np.asarray(lm8.filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255.0
coast = np.clip(1.0 - np.abs(blur - 0.5) * 2.0, 0, 1) ** 2

rng = np.random.default_rng(7)
noise = rng.random((H, W)).astype(np.float32)
big = np.asarray(Image.fromarray((noise * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))).astype(np.float32) / 255.0
big = (big - big.min()) / (big.max() - big.min() + 1e-6)

out = np.zeros((H, W, 3), np.float32)

# Land: unchanged. Political colour is blended over this by the shader, so it only needs to be a
# dark, slightly varied base.
land_col = np.array([0.10, 0.09, 0.14]); land_tint = np.array([0.16, 0.10, 0.24])
out += (land_col[None, None, :] * (1 - big[..., None]) + land_tint[None, None, :] * big[..., None]) * lmf[..., None]

# Sea: near-black, plus a slow nebula. Two blurred octaves so the clouds have structure without
# the speckle that a single noise field gives at this resolution. Kept low-contrast on purpose -
# every previous version of this map failed by making an effect strong enough to become a smear.
sea = 1.0 - lmf
out += np.array([0.022, 0.020, 0.046])[None, None, :] * sea[..., None]
if FLATMAP_NEBULA > 0:
    # Proper fBm, not blurred white noise. Gaussian-blurring a full-resolution random field
    # collapses it to almost a constant - the variance goes with the blur radius - so the first
    # attempt produced a nebula with sea luminance p50 13.7 and no visible structure at all.
    # Summing upscaled low-resolution grids keeps the large shapes and the contrast.
    def fbm(w, h, base, octaves, seed, gain=0.5):
        r = np.random.default_rng(seed)
        acc = np.zeros((h, w), np.float32)
        amp, res = 1.0, base
        for _ in range(octaves):
            g = r.random((max(2, res // 2), max(2, res))).astype(np.float32)
            up = np.asarray(Image.fromarray((g * 255).astype(np.uint8))
                            .resize((w, h), Image.BICUBIC)).astype(np.float32) / 255.0
            acc += up * amp
            amp *= gain
            res *= 2
        acc -= acc.min()
        return acc / (acc.max() + 1e-6)

    n_a = fbm(W, H, 6, 5, 11)      # the clouds themselves
    n_b = fbm(W, H, 3, 4, 23)      # slow hue drift between violet and teal
    # smoothstep, not a clip. Clipping flattened whole seas to pure black with a visible hard
    # edge where the field crossed the threshold - the same saturation failure documented for the
    # terrain effects. A smooth ramp keeps the gradient at both ends.
    t = np.clip((n_a - 0.14) / 0.78, 0, 1)
    cloud = t * t * (3.0 - 2.0 * t)
    deep = np.array([0.20, 0.13, 0.38])      # violet
    warm = np.array([0.06, 0.24, 0.30])      # teal
    mix = np.clip(n_b * 1.5 - 0.25, 0, 1)[..., None]
    out += (deep[None, None, :] * (1 - mix) + warm[None, None, :] * mix) *            (cloud * sea)[..., None] * FLATMAP_NEBULA

if FLATMAP_STARS:
    stars = (noise > 0.9975).astype(np.float32) * sea
    out += np.array([0.9, 0.85, 0.7])[None, None, :] * stars[..., None] * 0.7

# Coast: a cool rim, not the old gold+violet. The warm version read as a magenta smear wherever
# an island was smaller than the band - which, at this resolution, is most islands.
coast_col = np.array([0.55, 0.72, 0.95]) * 0.60 + np.array([0.80, 0.70, 1.00]) * 0.40
out += coast_col[None, None, :] * coast[..., None] * FLATMAP_COAST

out = np.clip(out, 0, 1)
fm = Image.fromarray((out * 255).astype(np.uint8))
dds_rgb(fm, os.path.join(M, "gfx", "map", "terrain", "flat_maps", "flatmap.dds"))
fm.resize((1152, 576)).save(os.path.join(PREV, "flatmap_new_preview.png"))
print("flatmap written", fm.size)
