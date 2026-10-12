"""Convert PNG/JPG source art into the DDS files CK3 expects, one profile per kind of art.

    python docs/tools/convert_art.py --profile <p> <src> <dst.dds> [--key-black]
                                     [--crop x,y,w,h] [--fit contain|cover]
                                     [--tone | --no-tone] [--backdrop x,y,w,h]
    python docs/tools/convert_art.py --batch jobs.csv
    python docs/tools/convert_art.py --list-profiles

Profiles come from the vanilla-measured "Format by kind" table in the art brief
(Desktop/EotG_Art_Needed.md, 2026-10-11). The DDS format of each profile copies the
majority header of vanilla's own files of that kind (gfx/interface/..., CK3 1.20):

  full-frame illustrations (decision, event_background, fullscreen, battle, holding)
      DXT1, no mipmaps          e.g. decisions/bp2_playdate.dds, event_scenes/alley.dds,
                                event_story/ep3_roman_restoration.dds, terrain_types/desert.dds,
                                holding_types/castle_india.dds
  innovation                    DXT1, full mip chain (8), culture_innovations/*_01.dds
  icons                         uncompressed 32-bit BGRA (A8R8G8B8); mipmaps as vanilla's
                                majority: full chain for interaction, scheme_icon,
                                government, splash, modifier, death; none for trait,
                                story_icon, terrain_icon, law.

Clean-up and marks (2026-10-12): --key-luma LO,HI (light silhouette on black, global
key + defringe), --erase POLY [--erase-grow N], --recolor X,Y,W,H=RRGGBB (neutralize a
red emblem), --alpha-threshold N (flat alpha; laws re-flatten after fitting),
--despeckle PX, --fill-holes R, --trim [--margin N], --badge up|down (modifier: 48 px silhouette plus
vanilla corner triangle, up top-left / down bottom-right) and --law-mark
ban|license|favor (flat black bar / seal / star with a 2 px cut gap).

Order of operations: load -> --crop -> --key-black/--key-luma -> --erase -> --recolor ->
--alpha-threshold -> --despeckle -> --fill-holes -> place (badge / trim / trait backdrop / law / fit) ->
tone -> law blackening -> DDS. Colour metrics are HSV over opaque pixels (alpha >= 128):
"brightness" is V (max channel), as in the trait tone commit 43ec7d7 (blademaster
S 0.32, V 0.33).

Batch CSV columns: src, profile, dst, flags (flags is a shell-style string, e.g.
"--key-black --crop 0,0,800,800"). Relative paths resolve against the CSV's folder.

Needs Pillow (>= 11.2, for DXT1/DXT5 encoding) and numpy; scipy for --key-black.
Exit 1 if any file fails.
"""
import argparse
import csv
import io
import os
import shlex
import struct
import sys
from dataclasses import dataclass

import numpy as np
from PIL import Image

# --------------------------------------------------------------------------- profiles


@dataclass(frozen=True)
class Profile:
    name: str
    size: tuple                 # (w, h)
    alpha: bool                 # RGBA output (else RGB, alpha discarded)
    fmt: str                    # "DXT1" | "BGRA"
    mips: bool                  # full mip chain (vanilla majority for this kind)
    fit: str                    # default fit: "cover" (full frame) or "contain" (icons)
    value: tuple = None         # (lo, hi) brightness range to clamp into, or None
    sat: tuple = None           # (lo, hi) saturation range to clamp into, or None
    sat_scale_floor: float = None  # interaction/scheme: cut sat toward sat[1], at most this factor
    special: str = None         # "trait" | "law" | "innovation"
    vanilla: str = ""           # header evidence
    note: str = ""


_FULL = "full frame"
PROFILES = {p.name: p for p in [
    Profile("decision", (1100, 440), False, "DXT1", False, "cover", (0.12, 0.21), (0.27, 0.44),
            vanilla="decisions/bp2_playdate.dds: DXT1, 0 mips (33 of 78 files at 1100x440 DXT1 no mip)",
            note="very dark; one light source"),
    Profile("event_background", (1592, 848), False, "DXT1", False, "cover", (0.15, 0.32), (0.33, 0.48),
            vanilla="event_scenes/alley.dds: DXT1, 0 mips (152 files)",
            note="also scheme illustration and court-position backdrop"),
    Profile("fullscreen", (3840, 1252), False, "DXT1", False, "cover", (0.27, 0.43), (0.22, 0.47),
            vanilla="event_story/ep3_roman_restoration.dds: DXT1, 0 mips (16 files)"),
    Profile("battle", (1200, 600), False, "DXT1", False, "cover", (0.53, 0.67), (0.21, 0.41),
            vanilla="illustrations/terrain_types/desert.dds: DXT1, 0 mips (15 files)"),
    Profile("holding", (2560, 1168), False, "DXT1", False, "cover", (0.27, 0.32), (0.18, 0.33),
            vanilla="holding_types/castle_india.dds: DXT1, 0 mips (29 files)"),
    Profile("innovation", (180, 120), False, "DXT1", True, "cover", (0.32, 0.40), (0.22, 0.39),
            special="innovation",
            vanilla="culture_innovations/innovation_administration_01.dds: DXT1, 8 mips (55 files)",
            note="filled; transparent source is laid on a dark vignette"),
    Profile("trait", (120, 120), True, "BGRA", False, "contain", (0.33, 0.33), (0.32, 0.32),
            special="trait",
            vanilla="traits/blademaster_1.dds: A8R8G8B8, 0 mips (267 files); mod's shipped traits match",
            note="teal backdrop scaled to 92 px at x 14-105, y 15-106"),
    Profile("interaction", (120, 120), True, "BGRA", True, "contain", None, (0.0, 0.37), 0.8,
            vanilla="character_interactions/antagonistic.dds: A8R8G8B8, 7 mips (115 files)"),
    Profile("scheme_icon", (120, 120), True, "BGRA", True, "contain", None, (0.0, 0.37), 0.8,
            vanilla="scheme_types/diplomacy.dds: A8R8G8B8, 7 mips (31 files)"),
    Profile("story_icon", (128, 128), True, "BGRA", False, "contain",
            vanilla="story_cycles/story_icon_conqueror.dds: A8R8G8B8, mipcount 1 (4 of 5)"),
    Profile("government", (70, 70), True, "BGRA", True, "contain",
            vanilla="government_types/celestial_government.dds: A8R8G8B8, 7 mips (15 of 27)"),
    Profile("splash", (70, 70), True, "BGRA", True, "contain",
            vanilla="splash_icons/splash_byzantine.dds: A8R8G8B8, 7 mips (7 of 8)"),
    Profile("modifier", (60, 60), True, "BGRA", True, "contain", (0.38, 0.50), (0.25, 0.52),
            vanilla="modifiers/administrative_mixed.dds: A8R8G8B8, 6 mips (238 files)",
            note="county_modifier_* measure V 0.47-0.50, S 0.31 (green) / 0.49 (red)"),
    Profile("death", (60, 60), True, "BGRA", True, "contain",
            vanilla="death_reason/death_disease.dds: A8R8G8B8, 6 mips (4 files)"),
    Profile("terrain_icon", (60, 60), True, "BGRA", False, "contain",
            vanilla="icons/terrain_types/desert.dds: A8R8G8B8, 0 mips (14 of 20)"),
    Profile("law", (96, 96), True, "BGRA", False, "contain", special="law",
            vanilla="laws/celestial_army_liege_law_0.dds: A8R8G8B8, mipcount 1 (31 of 46 at 96x96)",
            note="flat black silhouette; the game tints it"),
]}

TRAIT_BACKDROP = (14, 15, 92, 92)   # x, y, w, h on the 120 canvas (fc86da0)
LAW_MARGIN = 9                      # fit box margin; warn under 8
LAW_MARGIN_MIN = 8
OPAQUE = 128


# --------------------------------------------------------------------------- colour


def rgb_to_hsv(rgb):
    """float RGB (..., 3) in 0-1 -> H (0-1), S, V."""
    mx = rgb.max(-1)
    mn = rgb.min(-1)
    d = mx - mn
    s = np.where(mx > 0, d / np.maximum(mx, 1e-12), 0.0)
    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    dd = np.maximum(d, 1e-12)
    h = np.where(mx == r, ((g - b) / dd) % 6, np.where(mx == g, (b - r) / dd + 2, (r - g) / dd + 4))
    h = np.where(d > 0, h / 6.0, 0.0)
    return h, s, mx


def hsv_to_rgb(h, s, v):
    i = np.floor(h * 6).astype(int) % 6
    f = h * 6 - np.floor(h * 6)
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    choices = [(v, t, p), (q, v, p), (p, v, t), (p, q, v), (t, p, v), (v, p, q)]
    out = np.zeros(h.shape + (3,))
    for k, (a, b, c) in enumerate(choices):
        m = i == k
        out[m, 0], out[m, 1], out[m, 2] = a[m], b[m], c[m]
    return out


def measure(im):
    """(alpha_transparent_pct, alpha_partial_pct, mean_sat, mean_value) over opaque pixels."""
    a = np.asarray(im.convert("RGBA")).astype(np.float64) / 255.0
    al = a[..., 3]
    n = al.size
    transparent = 100.0 * np.count_nonzero(al == 0) / n
    partial = 100.0 * np.count_nonzero((al > 0) & (al < 1)) / n
    m = al >= OPAQUE / 255.0
    if not m.any():
        return transparent, partial, 0.0, 0.0
    _, s, v = rgb_to_hsv(a[..., :3][m])
    return transparent, partial, float(s.mean()), float(v.mean())


def _bisect(fn, target, lo, hi, increasing=True, it=40):
    for _ in range(it):
        mid = (lo + hi) / 2
        val = fn(mid)
        if (val < target) == increasing:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def _clamp_target(mean, rng):
    lo, hi = rng
    return lo if mean < lo else hi if mean > hi else None


def tone(im, prof, value_range=None, sat_range=None):
    """Move mean saturation / value of opaque pixels into the profile's range.
    Saturation: linear scale. Value: gamma (keeps black and white points)."""
    value_range = value_range or prof.value
    sat_range = sat_range or prof.sat
    if not value_range and not sat_range:
        return im
    mode = im.mode
    a = np.asarray(im.convert("RGBA")).astype(np.float64) / 255.0
    m = a[..., 3] >= OPAQUE / 255.0
    if not m.any():
        return im
    h, s, v = rgb_to_hsv(a[..., :3])
    if sat_range:
        cur = s[m].mean()
        tgt = _clamp_target(cur, sat_range)
        if tgt is not None and prof.sat_scale_floor and tgt < cur:
            tgt = max(tgt, cur * prof.sat_scale_floor)   # "down ~20% toward vanilla"
        if tgt is not None and cur > 0:
            sm = s[m]
            k = _bisect(lambda k: np.clip(sm * k, 0, 1).mean(), tgt, 0.0, 20.0)
            s = np.clip(s * k, 0, 1)
    if value_range:
        cur = v[m].mean()
        tgt = _clamp_target(cur, value_range)
        if tgt is not None and 0 < cur < 1:
            vm = v[m]
            g = _bisect(lambda g: (vm ** g).mean(), tgt, 0.05, 20.0, increasing=False)
            v = v ** g
    rgb = hsv_to_rgb(h, s, v)
    out = np.dstack([rgb, a[..., 3]])
    return Image.fromarray(np.round(out * 255).astype(np.uint8), "RGBA").convert(mode)


# --------------------------------------------------------------------------- geometry


def parse_box(text):
    parts = [int(p) for p in text.replace(" ", "").split(",")]
    if len(parts) != 4 or parts[2] <= 0 or parts[3] <= 0:
        raise ValueError(f"box must be x,y,w,h with positive w,h: {text!r}")
    return tuple(parts)


def crop(im, box):
    x, y, w, h = box
    if x < 0 or y < 0 or x + w > im.width or y + h > im.height:
        raise ValueError(f"crop {box} outside the {im.width}x{im.height} image")
    return im.crop((x, y, x + w, y + h))


def _resize(im, size):
    """Lanczos resize; RGBA goes through premultiplied alpha (no dark fringes)."""
    size = (max(1, int(round(size[0]))), max(1, int(round(size[1]))))
    if im.size == size:
        return im.copy()
    if im.mode == "RGBA":
        return im.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")
    return im.resize(size, Image.LANCZOS)


def fit(im, size, how, fill=(0, 0, 0, 0)):
    """contain: scale to fit, pad centred. cover: scale to fill, centre-crop. Never stretch."""
    tw, th = size
    sx, sy = tw / im.width, th / im.height
    s = min(sx, sy) if how == "contain" else max(sx, sy)
    w, h = max(1, round(im.width * s)), max(1, round(im.height * s))
    if how == "cover":   # make sure rounding never leaves a gap
        w, h = max(w, tw), max(h, th)
    r = _resize(im, (w, h))
    if how == "cover":
        x, y = (w - tw) // 2, (h - th) // 2
        return r.crop((x, y, x + tw, y + th)), s
    canvas = Image.new(im.mode, size, fill if im.mode == "RGBA" else fill[:3])
    canvas.paste(r, ((tw - w) // 2, (th - h) // 2))
    return canvas, s


def place(im, size, src_box, dst_box):
    """Scale uniformly so src_box maps onto dst_box (mean of the two axis scales), then
    paste onto a transparent canvas. Used for the trait backdrop."""
    sx, sy, sw, sh = src_box
    dx, dy, dw, dh = dst_box
    s = (dw / sw + dh / sh) / 2
    r = _resize(im.convert("RGBA"), (im.width * s, im.height * s))
    cx = dx + dw / 2 - (sx + sw / 2) * s
    cy = dy + dh / 2 - (sy + sh / 2) * s
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.paste(r, (int(round(cx)), int(round(cy))))   # no mask: copies alpha as is
    return canvas, s


def find_teal_backdrop(im):
    """Bounding box (x,y,w,h) of the teal backdrop tile: rows/columns where teal pixels
    reach 30% of the busiest row/column. None if there is no teal."""
    a = np.asarray(im.convert("RGBA")).astype(np.float64) / 255.0
    h, s, v = rgb_to_hsv(a[..., :3])
    teal = (h > 150 / 360) & (h < 210 / 360) & (s > 0.2) & (v > 0.15) & (a[..., 3] > 0.5)
    if teal.sum() < 0.02 * teal.size:
        return None
    cols, rows = teal.sum(0), teal.sum(1)
    xs = np.nonzero(cols >= 0.3 * cols.max())[0]
    ys = np.nonzero(rows >= 0.3 * rows.max())[0]
    return int(xs[0]), int(ys[0]), int(xs[-1] - xs[0] + 1), int(ys[-1] - ys[0] + 1)


def alpha_bbox(im, thresh=1):
    al = np.asarray(im.convert("RGBA"))[..., 3]
    ys, xs = np.nonzero(al >= thresh)
    if not len(xs):
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


# --------------------------------------------------------------------------- black key


def key_black(im, threshold=24, close_px=None, feather=1.0):
    """Turn a black background into alpha, without eating dark outlines.

    Background = near-black pixels (max channel <= threshold) connected to the image
    border (flood fill from the edges, never a global colour key, so black detail inside
    the art stays opaque). The foreground mask is then closed at outline width and
    hole-filled, so cracks and outlines touching the edge do not leak through
    (d0e5e2c). Only the outer edge is feathered: every pixel inside the mask is opaque.
    """
    from scipy import ndimage

    rgb = np.asarray(im.convert("RGB")).astype(np.int16)
    dark = rgb.max(-1) <= threshold
    lab, _ = ndimage.label(dark)
    border = np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))
    border = border[border != 0]
    bg = np.isin(lab, border)
    fg = ~bg
    if close_px is None:
        close_px = max(1, round(max(im.size) * 0.006))
    if close_px > 0:
        yy, xx = np.mgrid[-close_px:close_px + 1, -close_px:close_px + 1]
        disk = xx * xx + yy * yy <= close_px * close_px
        # pad so closing does not shrink at the image border
        pad = close_px + 1
        fgp = np.pad(fg, pad)
        fgp = ndimage.binary_closing(fgp, structure=disk)
        fg = fgp[pad:-pad, pad:-pad] | fg
    fg = ndimage.binary_fill_holes(fg)
    alpha = fg.astype(np.float64)
    if feather > 0:
        # outer feather only: distance from the mask, fading over `feather` px
        dist = ndimage.distance_transform_edt(~fg)
        alpha = np.where(fg, 1.0, np.clip(1.0 - dist / (feather + 1.0), 0, 1))
        # outside the mask the colour is the (black) background: a soft dark edge
    src_alpha = np.asarray(im.convert("RGBA"))[..., 3].astype(np.float64) / 255.0
    out = np.dstack([rgb.astype(np.uint8), np.round(alpha * src_alpha * 255).astype(np.uint8)])
    return Image.fromarray(out, "RGBA")


def key_luma(im, lo=0.06, hi=0.14):
    """Global luminance key for a light silhouette on solid black (e.g. a JPG with no
    alpha): luma <= lo -> alpha 0, >= hi -> 255, linear ramp between. The colour is then
    un-premultiplied against the black matte (defringe), so the soft edge has the
    silhouette's own colour, not a dark halo. Unlike key_black this also clears black
    holes enclosed by the art, which a silhouette needs."""
    a = np.asarray(im.convert("RGBA")).astype(np.float64) / 255.0
    rgb = a[..., :3]
    luma = rgb @ np.array([0.2126, 0.7152, 0.0722])
    alpha = np.clip((luma - lo) / max(hi - lo, 1e-6), 0, 1)
    # un-premultiply: the source colour is c = f * t + black * (1 - t), t ~ alpha
    rgb = np.where(alpha[..., None] > 0, np.clip(rgb / np.maximum(alpha[..., None], 1e-6), 0, 1), 0)
    out = np.dstack([rgb, alpha * a[..., 3]])
    return Image.fromarray(np.round(out * 255).astype(np.uint8), "RGBA")


# --------------------------------------------------------------------------- clean-up


def parse_poly(text):
    v = [float(p) for p in text.replace(" ", "").split(",")]
    if len(v) < 6 or len(v) % 2:
        raise ValueError(f"polygon must be x1,y1,x2,y2,x3,y3[,...]: {text!r}")
    return [(v[i], v[i + 1]) for i in range(0, len(v), 2)]


def _poly_mask(size, poly, grow=0):
    from PIL import ImageDraw
    from scipy import ndimage
    m = Image.new("L", size, 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    mask = np.asarray(m) > 0
    if grow > 0:
        yy, xx = np.mgrid[-grow:grow + 1, -grow:grow + 1]
        mask = ndimage.binary_dilation(mask, structure=xx * xx + yy * yy <= grow * grow)
    return mask


def erase_polys(im, polys, grow=0):
    """Clear alpha inside each polygon (source pixels), grown by `grow` px. Used to strip
    a badge baked into the source before re-stamping it in the vanilla corner."""
    a = np.asarray(im.convert("RGBA")).copy()
    for poly in polys:
        a[_poly_mask(im.size, poly, grow), 3] = 0
    return Image.fromarray(a, "RGBA")


def parse_recolor(text):
    box, _, colour = text.partition("=")
    colour = colour.strip().lstrip("#")
    if len(colour) != 6:
        raise ValueError(f"recolor must be x,y,w,h=RRGGBB: {text!r}")
    return parse_box(box), tuple(int(colour[i:i + 2], 16) for i in (0, 2, 4))


def recolor_red(im, box, colour, hue_tol=25 / 360, min_sat=0.3):
    """Inside box, give every red-hued pixel (hue within hue_tol of 0, sat >= min_sat) the
    hue and saturation of `colour`, scaling value so the patch's mean matches it; the
    painted shading survives. Used to neutralize a protected emblem (red cross)."""
    a = np.asarray(im.convert("RGBA")).astype(np.float64) / 255.0
    x, y, w, h = box
    sub = a[y:y + h, x:x + w]
    hh, s, v = rgb_to_hsv(sub[..., :3])
    red = ((hh <= hue_tol) | (hh >= 1 - hue_tol)) & (s >= min_sat) & (sub[..., 3] > 0)
    if red.any():
        th, ts, tv = (float(c) for c in rgb_to_hsv(np.array(colour, float) / 255.0))
        k = tv / max(v[red].mean(), 1e-6)
        hh = np.where(red, th, hh)
        s = np.where(red, ts, s)
        v = np.where(red, np.clip(v * k, 0, 1), v)
        sub[..., :3] = hsv_to_rgb(hh, s, v)
        a[y:y + h, x:x + w] = sub
    return Image.fromarray(np.round(a * 255).astype(np.uint8), "RGBA"), int(red.sum())


def alpha_threshold(im, t):
    """Flat alpha: >= t -> 255, else 0 (laws; sources with dithered/partial interiors)."""
    a = np.asarray(im.convert("RGBA")).copy()
    a[..., 3] = np.where(a[..., 3] >= t, 255, 0)
    return Image.fromarray(a, "RGBA")


def despeckle(im, min_px):
    """Drop connected visible components (8-connected, alpha > 0) under min_px pixels:
    caption specks and dither crumbs. Returns (image, pixels removed)."""
    from scipy import ndimage
    a = np.asarray(im.convert("RGBA")).copy()
    lab, n = ndimage.label(a[..., 3] > 0, structure=np.ones((3, 3)))
    if not n:
        return im, 0
    sizes = np.bincount(lab.ravel())
    small = sizes < min_px
    small[0] = False
    kill = small[lab]
    a[kill, 3] = 0
    return Image.fromarray(a, "RGBA"), int(kill.sum())


def fill_holes(im, radius):
    """Re-close a subject whose dark interior was keyed out upstream (the source PNG
    already has holes where dark joints, shadows and outlines were; the RGB under them
    is gone). Matte = visible mask (alpha >= 128) closed with a disk of `radius` px on a
    padded canvas (so the image edge does not shrink it), then hole-filled. Pixels added
    by the matte become opaque in the subject's own dark tone (mean of its darkest 10%),
    blended under whatever partial colour was there. Returns (image, pixels filled)."""
    from scipy import ndimage
    a = np.asarray(im.convert("RGBA")).astype(np.float64) / 255.0
    vis = a[..., 3] >= 0.5
    if not vis.any() or radius <= 0:
        return im, 0
    yy, xx = np.mgrid[-radius:radius + 1, -radius:radius + 1]
    disk = xx * xx + yy * yy <= radius * radius
    pad = radius + 1
    m = ndimage.binary_closing(np.pad(vis, pad), structure=disk)[pad:-pad, pad:-pad]
    m = ndimage.binary_fill_holes(m | vis)
    add = m & (a[..., 3] < 1.0)
    if not add.any():
        return im, 0
    rgb = a[..., :3]
    lum = rgb[vis] @ np.array([0.2126, 0.7152, 0.0722])
    dark = rgb[vis][lum <= np.quantile(lum, 0.10)].mean(0)
    al = a[..., 3][..., None]
    rgb = np.where(add[..., None], rgb * al + dark * (1 - al), rgb)
    alpha = np.where(add, 1.0, a[..., 3])
    out = np.dstack([rgb, alpha])
    return Image.fromarray(np.round(out * 255).astype(np.uint8), "RGBA"), int(add.sum())


def trim(im):
    bb = alpha_bbox(im)
    return im.crop((bb[0], bb[1], bb[2] + 1, bb[3] + 1)) if bb else im


# --------------------------------------------------------------------------- modifier badge
# Vanilla (gfx/interface/icons/modifiers/county_modifier_control_positive.dds and
# county_modifier_development_negative.dds, 60x60): an up triangle about 22 x 17 px at the
# TOP LEFT for good modifiers, a down triangle about 20 x 17 px at the BOTTOM RIGHT for bad
# ones, in the silhouette's own textured colour with a soft dark rim, overlapping a
# silhouette that fills most of the square.

BADGE_TRI = {"up": [(15.0, 3.5), (4.0, 21.0), (26.0, 21.0)],
             "down": [(37.0, 39.0), (57.0, 39.0), (47.0, 56.5)]}
BADGE_BOX = 48                                # silhouette fit box
BADGE_SIL_ORIGIN = {"up": (9, 8), "down": (3, 4)}   # pushed away from the badge corner


def _ss_mask(size, draw_fn, ss=4):
    """Anti-aliased L mask (0-1 float) drawn at ss x supersampling."""
    from PIL import ImageDraw
    w, h = size
    m = Image.new("L", (w * ss, h * ss), 0)
    draw_fn(ImageDraw.Draw(m), ss)
    return np.asarray(m.resize(size, Image.BOX)).astype(np.float64) / 255.0


def stamp_badge(im, direction, seed=7):
    """Stamp the vanilla-style corner triangle on a 60x60 modifier icon, coloured and
    grained like the silhouette's opaque pixels."""
    from scipy import ndimage
    a = np.asarray(im.convert("RGBA")).astype(np.float64) / 255.0
    size = im.size
    tri = BADGE_TRI[direction]
    m = _ss_mask(size, lambda d, s: d.polygon([(x * s, y * s) for x, y in tri], fill=255))
    # soft dark rim: the triangle grown ~1.5 px, offset down 1 px, blurred
    rim = ndimage.gaussian_filter(np.roll(ndimage.grey_dilation(m, size=(4, 4)), 1, axis=0), 0.8)
    rim = np.clip(rim * 0.7, 0, 1)
    base_a = a[..., 3]
    out_a = rim + base_a * (1 - rim)
    out_rgb = (a[..., :3] * (base_a * (1 - rim))[..., None]) / np.maximum(out_a, 1e-6)[..., None]
    # fill: per-pixel colours drawn from the silhouette itself (keeps its grain)
    solid = a[..., 3] >= 0.99
    pool = a[..., :3][solid] if solid.sum() >= 16 else np.array([[0.45, 0.53, 0.36]])
    rng = np.random.default_rng(seed)
    tex = pool[rng.integers(0, len(pool), size=(size[1], size[0]))]
    tex = np.stack([ndimage.gaussian_filter(tex[..., c], 0.5) for c in range(3)], -1)
    final_a = m + out_a * (1 - m)
    final_rgb = (tex * m[..., None] + out_rgb * (out_a * (1 - m))[..., None]) / np.maximum(final_a, 1e-6)[..., None]
    out = np.dstack([np.clip(final_rgb, 0, 1), final_a])
    return Image.fromarray(np.round(out * 255).astype(np.uint8), "RGBA")


def place_for_badge(im, size, direction):
    shape, s = fit(trim(im), (BADGE_BOX, BADGE_BOX), "contain")
    canvas = Image.new("RGBA", size, (0, 0, 0, 0))
    canvas.paste(shape, BADGE_SIL_ORIGIN[direction])
    return canvas, s


# --------------------------------------------------------------------------- law marks
# Ban = diagonal bar, License = seal disc with ribbon tails, Favor = star above a
# shrunken scroll. Flat black, cut off from the base by a transparent gap so they read
# at 32 px over the black gear.

LAW_MARK_GAP = 2.0
LAW_MARKS = ("ban", "license", "favor")
FAVOR_SCROLL_BOX = (9, 31, 78, 56)   # x, y, w, h: scroll shrunk under the star
FAVOR_STAR = (48.0, 19.5, 10.5)      # cx, cy, outer radius


def _star(cx, cy, r_out, r_in_ratio=0.45, points=5):
    import math
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_out * r_in_ratio
        ang = -math.pi / 2 + i * math.pi / points
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    return pts


def _mark_masks(kind, size):
    """(mark, cut) float masks: the mark itself and the grown area cleared around it."""
    import math
    g = LAW_MARK_GAP
    if kind == "ban":
        p0, p1, half = (17.0, 17.0), (79.0, 79.0), 4.5   # 9 px bar

        def bar(d, s, extra):
            dx, dy = p1[0] - p0[0], p1[1] - p0[1]
            n = math.hypot(dx, dy)
            ox, oy = -dy / n * (half + extra), dx / n * (half + extra)
            ex, ey = dx / n * extra, dy / n * extra
            q = [(p0[0] - ex + ox, p0[1] - ey + oy), (p1[0] + ex + ox, p1[1] + ey + oy),
                 (p1[0] + ex - ox, p1[1] + ey - oy), (p0[0] - ex - ox, p0[1] - ey - oy)]
            d.polygon([(x * s, y * s) for x, y in q], fill=255)
        return (_ss_mask(size, lambda d, s: bar(d, s, 0)),
                _ss_mask(size, lambda d, s: bar(d, s, g)))
    if kind == "license":
        cx, cy, r = 71.0, 67.5, 11.0                    # 22 px seal
        tails = [[(64, 74.5), (70, 74.5), (68, 85.5), (65, 82.5), (62, 84.5)],
                 [(72, 74.5), (78, 74.5), (80, 84.5), (77, 82.5), (74, 85.5)]]

        def seal(d, s, extra, ring):
            for t in tails:
                if extra:
                    xs = [p[0] for p in t]
                    ys = [p[1] for p in t]
                    d.rectangle(((min(xs) - extra) * s, (min(ys) - extra) * s,
                                 (max(xs) + extra) * s, (max(ys) + extra) * s), fill=255)
                else:
                    d.polygon([(x * s, y * s) for x, y in t], fill=255)
            rr = r + extra
            d.ellipse(((cx - rr) * s, (cy - rr) * s, (cx + rr) * s, (cy + rr) * s), fill=255)
            if ring:   # a thin inner ring: a stamped seal, not a ball
                ri, ro = r - 4.2, r - 2.6
                d.ellipse(((cx - ro) * s, (cy - ro) * s, (cx + ro) * s, (cy + ro) * s), fill=0)
                d.ellipse(((cx - ri) * s, (cy - ri) * s, (cx + ri) * s, (cy + ri) * s), fill=255)
        return (_ss_mask(size, lambda d, s: seal(d, s, 0, True)),
                _ss_mask(size, lambda d, s: seal(d, s, g, False)))
    if kind == "favor":
        cx, cy, r = FAVOR_STAR

        def star(d, s, extra):
            d.polygon([(x * s, y * s) for x, y in _star(cx, cy, r + extra * 1.6)], fill=255)
        return (_ss_mask(size, lambda d, s: star(d, s, 0)),
                _ss_mask(size, lambda d, s: star(d, s, g)))
    raise ValueError(f"unknown law mark {kind!r}")


def stamp_law_mark(im, kind):
    a = np.asarray(im.convert("RGBA")).astype(np.float64) / 255.0
    mark, cut = _mark_masks(kind, im.size)
    al = np.maximum(a[..., 3] * (1 - cut), mark)
    out = np.dstack([np.zeros(al.shape + (3,)), al])
    return Image.fromarray(np.round(out * 255).astype(np.uint8), "RGBA")


# --------------------------------------------------------------------------- DDS

DDSD_CAPS, DDSD_HEIGHT, DDSD_WIDTH, DDSD_PITCH = 0x1, 0x2, 0x4, 0x8
DDSD_PIXELFORMAT, DDSD_MIPMAPCOUNT, DDSD_LINEARSIZE = 0x1000, 0x20000, 0x80000
DDPF_ALPHAPIXELS, DDPF_FOURCC, DDPF_RGB = 0x1, 0x4, 0x40
DDSCAPS_COMPLEX, DDSCAPS_TEXTURE, DDSCAPS_MIPMAP = 0x8, 0x1000, 0x400000


def mip_count(w, h):
    n = 1
    while w > 1 or h > 1:
        w, h = max(1, w // 2), max(1, h // 2)
        n += 1
    return n


def _bc_payload(im, fourcc):
    """Block-compressed data for one level, via Pillow's encoder (header stripped)."""
    buf = io.BytesIO()
    im.save(buf, "DDS", pixel_format=fourcc)
    data = buf.getvalue()
    if data[84:88] != fourcc.encode():
        raise RuntimeError(f"Pillow wrote {data[84:88]!r}, expected {fourcc}")
    return data[128:]


def dds_bytes(im, fmt, mips):
    """Encode im as DDS. fmt 'DXT1' (RGB) or 'BGRA' (uncompressed A8R8G8B8).
    Header flags mirror vanilla's own files of the same shape."""
    w, h = im.size
    levels = mip_count(w, h) if mips else 1
    payload = []
    cur = im.convert("RGBA" if fmt == "BGRA" else "RGB")
    for i in range(levels):
        if i:
            cur = _resize(cur, (max(1, w >> i), max(1, h >> i)))
        if fmt == "BGRA":
            a = np.asarray(cur)
            payload.append(a[..., [2, 1, 0, 3]].tobytes())
        else:
            payload.append(_bc_payload(cur, fmt))
    flags = DDSD_CAPS | DDSD_HEIGHT | DDSD_WIDTH | DDSD_PIXELFORMAT
    caps = DDSCAPS_TEXTURE
    if fmt == "BGRA":
        if mips:
            flags |= DDSD_PITCH | DDSD_MIPMAPCOUNT
            pitch = w * 4
        else:
            flags |= DDSD_LINEARSIZE
            pitch = w * h * 4
        pf = struct.pack("<II4sIIIII", 32, DDPF_RGB | DDPF_ALPHAPIXELS, b"\0\0\0\0", 32,
                         0x00FF0000, 0x0000FF00, 0x000000FF, 0xFF000000)
    else:
        flags |= DDSD_LINEARSIZE | (DDSD_MIPMAPCOUNT if mips else 0)
        pitch = len(payload[0])
        pf = struct.pack("<II4sIIIII", 32, DDPF_FOURCC, fmt.encode(), 0, 0, 0, 0, 0)
    if mips:
        caps |= DDSCAPS_COMPLEX | DDSCAPS_MIPMAP
    header = struct.pack("<4sIIIIIII", b"DDS ", 124, flags, h, w, pitch, 0, levels if mips else 0)
    header += b"\0" * 44 + pf + struct.pack("<IIIII", caps, 0, 0, 0, 0)
    assert len(header) == 128
    return header + b"".join(payload)


def read_dds_header(path):
    """(w, h, format, mipcount) of a DDS file; format is the FourCC or 'BGRA'/'BGR'."""
    with open(path, "rb") as f:
        b = f.read(128)
    if b[:4] != b"DDS ":
        raise ValueError(f"{path}: not a DDS file")
    h, w = struct.unpack_from("<II", b, 12)
    mips = struct.unpack_from("<I", b, 28)[0]
    pfflags = struct.unpack_from("<I", b, 80)[0]
    if pfflags & DDPF_FOURCC:
        fmt = b[84:88].decode("latin1")
    else:
        bits = struct.unpack_from("<I", b, 88)[0]
        fmt = "BGRA" if (pfflags & DDPF_ALPHAPIXELS and bits == 32) else f"RGB{bits}"
    return w, h, fmt, mips


# --------------------------------------------------------------------------- pipeline


def _vignette(size, inner=(46, 52, 62), outer=(14, 16, 22)):
    """Dark blue-grey radial vignette, the innovation backdrop for transparent sources."""
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    r = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / np.sqrt(2)
    t = np.clip(r, 0, 1)[..., None]
    rgb = np.array(inner) * (1 - t) + np.array(outer) * t
    return Image.fromarray(rgb.astype(np.uint8), "RGB")


def snap_alpha(im, lo=3, hi=252):
    """Remove Lanczos ringing: alpha <= lo becomes 0, alpha >= hi becomes 255."""
    a = np.asarray(im.convert("RGBA")).copy()
    al = a[..., 3]
    al[al <= lo] = 0
    al[al >= hi] = 255
    return Image.fromarray(a, "RGBA")


def law_blacken(im):
    a = np.asarray(im.convert("RGBA")).copy()
    a[..., :3] = 0
    return Image.fromarray(a, "RGBA")


def convert(src, dst, profile, key=False, crop_box=None, fit_mode=None, do_tone=True,
            backdrop=None, key_threshold=24, value_range=None, sat_range=None,
            key_luma_range=None, erase=(), erase_grow=0, recolor=(), alpha_thresh=None,
            despeckle_px=None, fill_holes_px=None, do_trim=False, margin=0, badge=None, law_mark=None):
    """Convert one file. Returns a report dict (also has 'warnings')."""
    prof = PROFILES[profile]
    warnings = []
    if badge and profile != "modifier":
        raise ValueError("--badge needs the modifier profile")
    if law_mark and prof.special != "law":
        raise ValueError("--law-mark needs the law profile")
    im = Image.open(src)
    im.load()
    in_size = im.size
    src_has_alpha = im.mode in ("RGBA", "LA", "PA", "RGBa") or "transparency" in im.info
    im = im.convert("RGBA")
    if crop_box:
        im = crop(im, crop_box)
    if key:
        im = key_black(im, threshold=key_threshold)
    if key_luma_range:
        im = key_luma(im, *key_luma_range)
    if erase:
        im = erase_polys(im, erase, erase_grow)
    for box, colour in recolor:
        im, n = recolor_red(im, box, colour)
        if not n:
            warnings.append(f"--recolor {box}: no red pixels found")
    if alpha_thresh is not None:
        im = alpha_threshold(im, alpha_thresh)
    if despeckle_px:
        im, n = despeckle(im, despeckle_px)
        if n:
            warnings.append(f"despeckle removed {n} px")
    if fill_holes_px:
        im, n = fill_holes(im, fill_holes_px)
        if n:
            warnings.append(f"fill-holes closed {n} px")
    before = measure(im)
    if prof.alpha and not (key or key_luma_range) and not src_has_alpha:
        warnings.append("source has no alpha; a black background needs --key-black")

    tw, th = prof.size
    how = fit_mode or prof.fit
    if badge:
        out, scale = place_for_badge(im, prof.size, badge)
    elif do_trim and prof.special not in ("trait", "law"):
        shape, scale = fit(trim(im), (tw - 2 * margin, th - 2 * margin), how)
        out = Image.new("RGBA", prof.size, (0, 0, 0, 0))
        out.paste(shape, ((tw - shape.width) // 2, (th - shape.height) // 2))
    elif prof.special == "trait":
        box = backdrop or find_teal_backdrop(im)
        if box is None:
            warnings.append("no teal backdrop found; fell back to contain fit")
            out, scale = fit(im, prof.size, "contain")
        else:
            out, scale = place(im, prof.size, box, TRAIT_BACKDROP)
    elif prof.special == "law":
        if law_mark == "favor":   # shrink the base under the star
            bx, by, bw, bh = FAVOR_SCROLL_BOX
        else:
            bx, by, bw, bh = LAW_MARGIN, LAW_MARGIN, tw - 2 * LAW_MARGIN, th - 2 * LAW_MARGIN
        if alpha_thresh is not None:
            # flat source: fit at 4x, re-flatten, then box-filter down, so the edge is
            # a clean 1 px antialias like vanilla's laws, not resample blur or jaggies
            big, scale = fit(trim(im), (bw * 4, bh * 4), "contain")
            big = alpha_threshold(big, alpha_thresh)
            scale /= 4
            shape = big.convert("RGBa").resize((bw, bh), Image.BOX).convert("RGBA")
        else:
            shape, scale = fit(trim(im), (bw, bh), "contain")
        bb = alpha_bbox(shape)
        if bb:   # the base sits flush in its box (contain pads; drop the pad)
            shape = shape.crop((bb[0], bb[1], bb[2] + 1, bb[3] + 1))
        out = Image.new("RGBA", prof.size, (0, 0, 0, 0))
        out.paste(shape, (bx + (bw - shape.width) // 2, by + (bh - shape.height) // 2))
    else:
        out, scale = fit(im, prof.size, how)
    if scale > 1.5:
        warnings.append(f"upscaled x{scale:.2f}; source is small for this profile")

    if not prof.alpha:
        al = np.asarray(out)[..., 3]
        if (al < 255).any():
            if prof.special == "innovation":
                bg = _vignette(prof.size).convert("RGBA")
            else:
                bg = Image.new("RGBA", prof.size, (0, 0, 0, 255))
                warnings.append("transparent pixels composited onto black (profile has no alpha)")
            bg.alpha_composite(out)
            out = bg
        out = out.convert("RGB")

    if do_tone and prof.special != "law":
        out = tone(out, prof, value_range, sat_range)
    if prof.special == "law":
        out = law_blacken(out)
        if law_mark:
            out = stamp_law_mark(out, law_mark)
        bb = alpha_bbox(out, thresh=8)
        if bb:
            m = min(bb[0], bb[1], tw - 1 - bb[2], th - 1 - bb[3])
            if m < LAW_MARGIN_MIN:
                warnings.append(f"law shape margin {m}px < {LAW_MARGIN_MIN}px")

    if badge:   # after tone, so the badge takes the toned silhouette colour
        out = stamp_badge(out, badge)
    if prof.alpha:
        out = snap_alpha(out)
    after = measure(out)
    data = dds_bytes(out, prof.fmt, prof.mips)
    os.makedirs(os.path.dirname(os.path.abspath(dst)) or ".", exist_ok=True)
    with open(dst, "wb") as f:
        f.write(data)
    w, h, fmt, mips = read_dds_header(dst)
    return {
        "src": src, "dst": dst, "profile": profile, "in": in_size, "out": (w, h),
        "format": f"{fmt}, {'%d mips' % mips if mips else 'no mips'}",
        "alpha_before": before[:2], "alpha_after": after[:2],
        "sat": (before[2], after[2]), "val": (before[3], after[3]),
        "bytes": len(data), "warnings": warnings,
    }


def format_report(r):
    lines = [
        f"{r['src']} -> {r['dst']}  [{r['profile']}]",
        f"  size {r['in'][0]}x{r['in'][1]} -> {r['out'][0]}x{r['out'][1]}   format {r['format']}  ({r['bytes']} bytes)",
        f"  alpha: transparent {r['alpha_before'][0]:.1f}% -> {r['alpha_after'][0]:.1f}%,"
        f" partial {r['alpha_before'][1]:.1f}% -> {r['alpha_after'][1]:.1f}%",
        f"  saturation {r['sat'][0]:.3f} -> {r['sat'][1]:.3f}   brightness {r['val'][0]:.3f} -> {r['val'][1]:.3f}",
    ]
    lines += [f"  WARNING: {w}" for w in r["warnings"]]
    return "\n".join(lines)


# --------------------------------------------------------------------------- CLI


def _range(text):
    lo, hi = (float(p) for p in text.split(","))
    return lo, hi


def build_parser():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0],
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--profile", choices=sorted(PROFILES))
    p.add_argument("src", nargs="?")
    p.add_argument("dst", nargs="?")
    p.add_argument("--key-black", action="store_true",
                   help="key a black background (flood fill from the edges) into alpha")
    p.add_argument("--key-threshold", type=int, default=24,
                   help="max channel value counted as background black (default 24)")
    p.add_argument("--crop", type=parse_box, help="x,y,w,h in source pixels, applied first")
    p.add_argument("--fit", choices=("contain", "cover"),
                   help="default: cover for full-frame art, contain for icons")
    p.add_argument("--tone", dest="tone", action="store_true", default=True)
    p.add_argument("--no-tone", dest="tone", action="store_false")
    p.add_argument("--brightness", type=_range, help="override the profile's lo,hi brightness range")
    p.add_argument("--saturation", type=_range, help="override the profile's lo,hi saturation range")
    p.add_argument("--backdrop", type=parse_box,
                   help="trait only: backdrop tile box x,y,w,h (after crop); default auto-detect teal")
    p.add_argument("--key-luma", type=_range, metavar="LO,HI",
                   help="global luminance key for a light silhouette on black: luma <= LO "
                        "transparent, >= HI opaque, ramp between; colour defringed")
    p.add_argument("--erase", type=parse_poly, action="append", default=[], metavar="X1,Y1,X2,Y2,X3,Y3",
                   help="clear alpha inside this polygon (source px, after --crop); repeatable")
    p.add_argument("--erase-grow", type=int, default=0, help="grow every --erase polygon by N px")
    p.add_argument("--recolor", type=parse_recolor, action="append", default=[], metavar="X,Y,W,H=RRGGBB",
                   help="inside the box, give red-hued pixels this colour (keeps shading); repeatable")
    p.add_argument("--alpha-threshold", type=int, metavar="N",
                   help="flat alpha: >= N opaque, else transparent (applied before fitting)")
    p.add_argument("--despeckle", type=int, metavar="PX",
                   help="drop visible specks (8-connected components) smaller than PX pixels")
    p.add_argument("--fill-holes", type=int, metavar="R",
                   help="close holes keyed into the source upstream: matte closed at R px, "
                        "added pixels take the subject's dark tone")
    p.add_argument("--trim", action="store_true",
                   help="crop to the alpha bounding box before fitting (icons)")
    p.add_argument("--margin", type=int, default=0, help="with --trim: px kept clear on each side")
    p.add_argument("--badge", choices=("up", "down"),
                   help="modifier only: shrink to 48 px and stamp the vanilla corner triangle "
                        "(up = top left, good; down = bottom right, bad)")
    p.add_argument("--law-mark", choices=LAW_MARKS,
                   help="law only: stamp a flat black mark (ban bar, license seal, favor star)")
    p.add_argument("--batch", help="CSV with columns src,profile,dst,flags")
    p.add_argument("--list-profiles", action="store_true")
    return p


def _job_kwargs(a):
    return dict(key=a.key_black, crop_box=a.crop, fit_mode=a.fit, do_tone=a.tone,
                backdrop=a.backdrop, key_threshold=a.key_threshold,
                value_range=a.brightness, sat_range=a.saturation,
                key_luma_range=a.key_luma, erase=a.erase, erase_grow=a.erase_grow,
                recolor=a.recolor, alpha_thresh=a.alpha_threshold, despeckle_px=a.despeckle, fill_holes_px=a.fill_holes,
                do_trim=a.trim, margin=a.margin, badge=a.badge, law_mark=a.law_mark)


def run_batch(csv_path, out=sys.stdout):
    base = os.path.dirname(os.path.abspath(csv_path))
    parser = build_parser()
    failures = 0
    with open(csv_path, newline="", encoding="utf-8-sig") as f:
        for i, row in enumerate(csv.DictReader(f), start=2):
            if not row.get("src") or row["src"].lstrip().startswith("#"):
                continue
            src = os.path.join(base, row["src"].strip())
            dst = os.path.join(base, row["dst"].strip())
            try:
                a = parser.parse_args(["--profile", row["profile"].strip(), src, dst]
                                      + shlex.split(row.get("flags") or ""))
                print(format_report(convert(src, dst, a.profile, **_job_kwargs(a))), file=out)
            except (Exception, SystemExit) as e:   # noqa: BLE001 - report and continue
                failures += 1
                print(f"{csv_path}:{i}: FAILED {row.get('src')}: {e}", file=out)
    return failures


def main(argv=None):
    p = build_parser()
    a = p.parse_args(argv)
    if a.list_profiles:
        for pr in PROFILES.values():
            print(f"{pr.name:17} {pr.size[0]}x{pr.size[1]} {'RGBA' if pr.alpha else 'RGB '} "
                  f"{pr.fmt}{' +mips' if pr.mips else ''}  fit={pr.fit}  {pr.note}")
        return 0
    if a.batch:
        return 1 if run_batch(a.batch) else 0
    if not (a.profile and a.src and a.dst):
        p.error("--profile, src and dst are required (or --batch / --list-profiles)")
    try:
        print(format_report(convert(a.src, a.dst, a.profile, **_job_kwargs(a))))
    except (OSError, ValueError) as e:
        print(f"FAILED {a.src}: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
