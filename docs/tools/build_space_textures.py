import struct, os, sys, math
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

hx = lambda h: tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))
GOLD = hx("#FFC84D"); PALEGOLD = hx("#FFF2C0"); VIOLET = hx("#8A3BE0"); PURPLE = hx("#9A4FFF"); LAV = hx("#D6B4F0")
CRIMSON = hx("#E0325A"); TEAL = hx("#2FB8B0"); EMERALD = hx("#2E9C6A"); SAPPH = hx("#3A6CFF"); WHITE = (255, 255, 255)

# ---------------- borders: horizontal strip, x along the border, y across ----------------
def border(color, core=0.06, halo=0.35, strength=1.0, dash=None, core_col=None, size=128):
    cc = core_col or tuple(min(255, int(c * 0.45 + 255 * 0.55)) for c in color)
    y = (np.arange(size) + 0.5) / size
    d = np.abs(y - 0.5) * 2
    a_core = np.exp(-(d * d) / (core * core))
    a_halo = np.exp(-(d * d) / (halo * halo)) * 0.45
    t = a_core / (a_core + a_halo + 1e-6)
    col = np.stack([cc[i] * t + color[i] * (1 - t) for i in range(3)], -1)  # (size,3)
    a = np.minimum(1.0, (a_core + a_halo) * strength)                      # (size,)
    x = (np.arange(size) + 0.5) / size
    k = np.ones(size)
    if dash:
        on, off = dash
        k = np.where((x % (on + off)) < on, 1.0, 0.15)
    img = np.zeros((size, size, 4), np.float32)
    img[:, :, :3] = col[:, None, :]
    img[:, :, 3] = (a[:, None] * k[None, :]) * 255
    return Image.fromarray(img.astype(np.uint8), "RGBA")

B = os.path.join(M, "gfx", "map", "borders")
spec = {
    "border_water": border(VIOLET, core=0.05, halo=0.2, strength=0.25),
    "border_province": border(LAV, core=0.04, halo=0.15, strength=0.35, dash=(0.18, 0.12)),
    "border_county": border(LAV, core=0.05, halo=0.2, strength=0.6),
    "border_domain": border(GOLD, core=0.06, halo=0.3, strength=0.9),
    "border_other_realm": border(GOLD, core=0.07, halo=0.35, strength=1.0),
    "border_my_realm": border(PURPLE, core=0.07, halo=0.35, strength=1.0),
    "border_sub_realm": border(VIOLET, core=0.05, halo=0.25, strength=0.7),
    "border_hovered_realm": border(PALEGOLD, core=0.08, halo=0.45, strength=1.0, core_col=WHITE),
    "border_hovered_realm_flat_map": border(PALEGOLD, core=0.08, halo=0.45, strength=1.0, core_col=WHITE),
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

# ---------------- flat map: the zoomed-out view, derived from the vanilla paper map ------------
#
# THIS TEXTURE, not any shader, is what the player sees at full zoom out. PixelShaderFlatMap in
# pdxterrain.shader does nothing but read it. Two things baked in here were chased through
# pdxwater, surroundmap and pdxterrain for several rounds before anyone looked at the texture:
#
#   * FLATMAP_STARS  - random points masked to SEA ONLY, i.e. literally "stars in the ocean"
#   * FLATMAP_COAST  - a band around every coastline in gold+violet, which reads as a pink loop
#                      around small islands, where the band is the entire island
#
# Neither can be faded by a shader, because neither is computed at runtime. If something is
# visible only when fully zoomed out, check this file first.
FLATMAP_STARS = False      # off: the ocean is clean at strategic zoom
FLATMAP_COAST = 0.30       # was 0.9; enough to read a coastline, not enough to be a smear

Image.MAX_IMAGE_PIXELS = None
src = Image.open(r"D:\SteamLibrary\steamapps\common\Crusader Kings III\game\gfx\map\terrain\flat_maps\flatmap.dds").convert("RGB")
W, H = 4608, 2304
src = src.resize((W, H), Image.BOX)
a = np.asarray(src).astype(np.int16)
landmask = ((a[:, :, 0] - a[:, :, 2]) > 28) & (a[:, :, 0] > 120)
lm = Image.fromarray((landmask * 255).astype(np.uint8)).filter(ImageFilter.MedianFilter(5))
lmf = np.asarray(lm).astype(np.float32) / 255.0
blur = np.asarray(lm.filter(ImageFilter.GaussianBlur(6))).astype(np.float32) / 255.0
coast = np.clip(1.0 - np.abs(blur - 0.5) * 2.0, 0, 1) ** 2
rng = np.random.default_rng(7)
noise = rng.random((H, W)).astype(np.float32)
big = np.asarray(Image.fromarray((noise * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(18))).astype(np.float32) / 255.0
big = (big - big.min()) / (big.max() - big.min() + 1e-6)
out = np.zeros((H, W, 3), np.float32)
land_col = np.array([0.10, 0.09, 0.14]); land_tint = np.array([0.16, 0.10, 0.24])
out += (land_col[None, None, :] * (1 - big[..., None]) + land_tint[None, None, :] * big[..., None]) * lmf[..., None]
out += np.array([0.008, 0.006, 0.012])[None, None, :] * (1 - lmf[..., None])
if FLATMAP_STARS:
    stars = (noise > 0.9975).astype(np.float32) * (1 - lmf)
    out += np.array([0.9, 0.85, 0.7])[None, None, :] * stars[..., None] * 0.7
coast_col = np.array([0.95, 0.75, 0.45]) * 0.55 + np.array([0.75, 0.55, 0.95]) * 0.45
out += coast_col[None, None, :] * coast[..., None] * FLATMAP_COAST
out = np.clip(out, 0, 1)
fm = Image.fromarray((out * 255).astype(np.uint8))
dds_rgb(fm, os.path.join(M, "gfx", "map", "terrain", "flat_maps", "flatmap.dds"))
fm.resize((1024, 512)).save(os.path.join(PREV, "flatmap_new_preview.png"))
print("flatmap written", fm.size)
