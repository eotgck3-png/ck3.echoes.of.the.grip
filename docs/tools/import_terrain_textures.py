"""
Turn hand-made / Midjourney terrain images into CK3 detail materials.

Drop images into a folder, named after the material they replace:

    eotg_hills_01.png        ->  eotg_hills_01_{diffuse,normal,properties}.dds
    eotg_plains_02.jpg
    eotg_edge_01.png

Everything CK3 requires is handled here, because almost none of it is visible in a source image:
  * centre-cropped to square and resized to exactly 1024x1024
  * written as DXT5 with a full 11-level mip chain (the detail textures are a TEXTURE ARRAY -
    every slice must match or the game crashes on load)
  * height packed into the diffuse alpha, derived from luminance
  * normal map generated from that height in DXT5nm / RRxG packing (X in green, Y in alpha,
    inverted) - NOT a standard RGB normal map
  * specular / metalness / roughness taken from the material's entry in build_terrain_materials.py,
    so an imported texture keeps the same surface response as the placeholder it replaces

Optional help:
  --seamless   make the image tile (offset-and-blend). Midjourney's --tile already does this, so
               only use it for sources that are not already seamless.
  --contrast X pull the image toward its own dark end (0..1, 1 = unchanged). The map tiles a
               texture ~337x, so high contrast reads as a grid. Defaults to the value the
               placeholder for that material used.
  --coherent   normalise every texture into one shared value/saturation band, so terrains differ
               by hue and structure rather than brightness and vividness. Also rolls off
               highlights, which is what causes confetti speckle at map tiling scale.
  --soften S   0..1, reduce the amplitude of the finest COLOUR detail (default 0.55 with
               --coherent). This is what removes DXT5 chroma speckle. The height map is taken
               before softening, so terrain boundaries keep their full interlocking detail.
  --check      score every image against the quality limits and write nothing.

Usage:
    python import_terrain_textures.py <mod root> <input dir> [--seamless] [--contrast 0.8] [--check]
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_terrain_materials import write_material, TERRAINS, EDGES

SIZE = 512
EXTS = (".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tga")

# --coherent targets. Every material is normalised into this band so the set reads as one map.
# Do NOT raise these to match vanilla's ~0.41. Vanilla terrain is daylight Earth and is meant to
# be bright; ours is dark space. Soft-light can never darken below b*b, so a 0.33 texture cannot
# be brought under 0.109 on screen no matter what the colormap does - it just washes out.
# Textures are deliberately NOT darkened to the final on-screen level. DXT5 stores block endpoints
# as RGB565 (8/255 steps in red), so a texture spanning only 0..30/255 has ~4 usable levels and
# bands into coloured speckle - which the game's exposure then amplifies. Keep the signal well clear
# of that noise floor here and do the darkening in the colormap instead (build_colormap.py --level).
BRIGHT_TARGET = 0.130     # mean luminance for ordinary terrain
BRIGHT_NOTABLE = 0.175    # the rare, meant-to-be-noticed terrains get a little headroom
SAT_CAP = 0.30            # shared saturation ceiling
NOTABLE = ("farmlands", "oasis", "floodplains", "wetlands")


def material_params():
    """material id -> the params dict used by the placeholder, for spec/metal/rough/contrast."""
    out = {}
    for terr, (_pretty, variants) in TERRAINS.items():
        for suffix, _kind, p in variants:
            out[f"eotg_{terr}_{suffix}"] = p
    for mid, _kind, p in EDGES:
        out[mid] = p
    return out


def center_square(im):
    w, h = im.size
    s = min(w, h)
    return im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s))


def analyse(a):
    """Score a 1024x1024 RGB float image (0..1) on the things that decide whether it works.

    The governing idea: a good terrain texture is **fine detail with a flat large-scale average**.
    It tiles ~337x across the map, so any big shape or brightness gradient repeats into an obvious
    grid, while fine local variation is what the height blend needs to interlock terrains.
    """
    lum = a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722
    h, w = lum.shape
    m = {}

    # tiling: how big the wrap seam is relative to the image's own neighbour-to-neighbour detail
    sx = np.abs(lum[:, 0] - lum[:, -1]).mean(); sy = np.abs(lum[0, :] - lum[-1, :]).mean()
    nx = np.abs(np.diff(lum, axis=1)).mean(); ny = np.abs(np.diff(lum, axis=0)).mean()
    m["tiling"] = float((sx + sy) / (nx + ny + 1e-8) / 2.0)

    # large-scale energy share: how much of the variation sits in big blobs rather than detail
    F = np.fft.fftshift(np.fft.fft2(lum - lum.mean()))
    P = (F.real ** 2 + F.imag ** 2)
    fy, fx = np.mgrid[-h // 2:h // 2, -w // 2:w // 2]
    r = np.sqrt(fx * fx + fy * fy)
    tot = P[r > 0].sum() + 1e-12
    m["blobbiness"] = float(P[(r > 0) & (r <= 4)].sum() / tot)

    # local detail available to drive the height map
    k = max(3, h // 64) | 1
    blur = np.asarray(Image.fromarray((lum * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(k)), dtype=np.float32) / 255.0
    m["detail"] = float((lum - blur).std())

    m["brightness"] = float(lum.mean())
    m["contrast"] = float(np.percentile(lum, 95) - np.percentile(lum, 5))

    # baked directional lighting: best-fit linear ramp across the image
    yy, xx = np.mgrid[0:h, 0:w]
    A = np.stack([xx.ravel() / w, yy.ravel() / h, np.ones(h * w)], 1).astype(np.float32)
    coef, *_ = np.linalg.lstsq(A[::37], lum.ravel()[::37], rcond=None)
    m["lighting"] = float(math.hypot(coef[0], coef[1]))

    mx = a.max(axis=2); mn = a.min(axis=2)
    lit = mx > 0.05                      # ignore the noise floor; ratios there are meaningless
    m["saturation"] = float(((mx[lit] - mn[lit]) / mx[lit]).mean()) if lit.any() else 0.0

    # Local contrast and peak ratio: the two properties that decide whether a texture survives
    # minification. Terrain is viewed with 5-9 source pixels collapsing into each screen pixel, so
    # uniform content averages to the same value regardless of sub-pixel alignment and stays stable,
    # while sparse very-bright points average differently per pixel and sparkle. Measured on vanilla
    # terrain: local contrast 0.06, peak/mean 0.3. Measured on a starfield: 1.20 and 13.1.
    blur4 = np.asarray(Image.fromarray((lum * 255).astype(np.uint8)).filter(
        ImageFilter.GaussianBlur(4)), dtype=np.float32) / 255.0
    mean_l = float(lum.mean())
    m["local_contrast"] = float((lum - blur4).std() / (mean_l + 1e-6))
    m["peak_ratio"] = float((np.percentile(lum, 99.9) - mean_l) / (mean_l + 1e-6))

    # A big shape only repeats visibly if it also has contrast. Nebula terrains are legitimately
    # blobby (measured 0.85-0.95) but low contrast, so judging on blobbiness alone rejects them.
    m["repeat_risk"] = m["blobbiness"] * m["contrast"]
    return m


# metric -> (good_max, warn_max, direction, blurb).  direction -1 means "higher is better".
#
# Calibrated so that all 26 shipped placeholders pass. WARN is deliberately reachable by design
# choices that are correct but have a real cost: a Barren Reach is meant to be near-featureless
# (low detail => terrain boundaries cross-fade instead of interlocking), and Volatile Cluster /
# Anomaly Fields are meant to be vivid. FAIL is reserved for values that will actually look broken.
LIMITS = {
    # The two that matter most and that the importer CANNOT fix for you. Vanilla terrain sits at
    # 0.06 / 0.3; a starfield at 1.20 / 13.1. Above the FAIL line the texture will sparkle and
    # crawl under minification no matter how it is processed afterwards.
    "local_contrast": (0.35, 0.60, 1, "fine detail amplitude vs local level - what shimmers"),
    "peak_ratio":     (3.0,  6.0,  1, "how far the brightest points sit above the mean"),
    "tiling":      (2.0,  6.0,   1, "wrap seam vs internal detail"),
    "repeat_risk": (0.25, 0.40,  1, "big shapes x contrast - what actually reads as a grid"),
    "detail":      (0.004, 0.0002, -1, "local variation available for the height map"),
    "brightness":  (0.90, 0.95,  1, "mean luminance (normalised on import, so not a gate)"),
    "contrast":    (0.45, 0.65,  1, "p5-p95 luminance spread"),
    "lighting":    (0.10, 0.20,  1, "baked directional gradient / horizon"),
    "saturation":  (0.90, 0.95,  1, "colour intensity (capped on import, so not a gate)"),
}


def verdict(metric, value):
    good, warn, direction, _ = LIMITS[metric]
    if direction == 1:
        return "OK" if value <= good else ("WARN" if value <= warn else "FAIL")
    return "OK" if value >= good else ("WARN" if value >= warn else "FAIL")


def seam_error(a):
    """Mean absolute difference across the wrap seams, 0..1. ~0 means it already tiles."""
    x = np.abs(a[:, 0].astype(np.float32) - a[:, -1].astype(np.float32)).mean()
    y = np.abs(a[0, :].astype(np.float32) - a[-1, :].astype(np.float32)).mean()
    # compare against the image's own average neighbour difference, so flat images are not
    # flattered and busy ones are not punished
    nx = np.abs(np.diff(a.astype(np.float32), axis=1)).mean()
    ny = np.abs(np.diff(a.astype(np.float32), axis=0)).mean()
    return float((x + y) / (nx + ny + 1e-6) / 2.0)


def make_seamless(a):
    """Offset-and-blend, applied per axis.

    Blending with a half-offset copy under weight 0.5*(1-cos(2*pi*t)) puts the original's
    *interior* at the wrap edges, so opposite edges become neighbours and the tile closes.
    Costs a little sharpness; Midjourney's --tile avoids needing this at all.
    """
    a = a.astype(np.float32)
    h, w = a.shape[:2]
    for axis, n in ((1, w), (0, h)):
        t = np.arange(n, dtype=np.float32) / n
        m = 0.5 * (1.0 - np.cos(2.0 * np.pi * t))          # 0 at the seam, 1 at the centre
        m = m.reshape((1, n, 1) if axis == 1 else (n, 1, 1))
        a = a * m + np.roll(a, n // 2, axis=axis) * (1.0 - m)
    return a


def main():
    root, indir = sys.argv[1], sys.argv[2]
    check = "--check" in sys.argv
    seamless = "--seamless" in sys.argv
    contrast_override = float(sys.argv[sys.argv.index("--contrast") + 1]) if "--contrast" in sys.argv else None
    coherent = "--coherent" in sys.argv
    # softening defaults on with --coherent, since the speckle it fixes is the main reason to use it
    soften = float(sys.argv[sys.argv.index("--soften") + 1]) if "--soften" in sys.argv else (0.75 if coherent else 0.0)

    params = material_params()
    outdir = os.path.join(root, "gfx", "map", "terrain")
    os.makedirs(outdir, exist_ok=True)

    files = [f for f in sorted(os.listdir(indir)) if f.lower().endswith(EXTS)]
    if not files:
        raise SystemExit(f"no images found in {indir}")

    done, skipped = 0, []
    for f in files:
        mid = os.path.splitext(f)[0]
        if mid not in params:
            skipped.append((f, "name does not match any material id"))
            continue

        im = Image.open(os.path.join(indir, f)).convert("RGB")
        src = im.size
        im = center_square(im).resize((SIZE, SIZE), Image.LANCZOS)
        a = np.asarray(im).astype(np.float32) / 255.0

        err = seam_error(np.asarray(im))
        if check:
            m = analyse(a)
            bad = [k for k in LIMITS if verdict(k, m[k]) == "FAIL"]
            warn = [k for k in LIMITS if verdict(k, m[k]) == "WARN"]
            overall = "UNUSABLE" if bad else ("USABLE (with warnings)" if warn else "GOOD")
            print()
            print(f"  {f}   source {src[0]}x{src[1]}   ->  {overall}")
            for k, (_g, _w, _d, blurb) in LIMITS.items():
                v = verdict(k, m[k])
                mark = {"OK": "  ok ", "WARN": " warn", "FAIL": " FAIL"}[v]
                print(f"      {k:12s} {m[k]:8.3f} {mark}   {blurb}")
            if min(src) < SIZE:
                print(f"      resolution   {min(src):8d}  warn   short side under {SIZE}; will be upscaled and soft")
            if bad:
                print(f"      -> fix: {', '.join(bad)}")
            continue
        if seamless:
            a = np.clip(make_seamless(a * 255.0) / 255.0, 0, 1)

        p = params[mid]

        # --coherent: normalise every texture into one shared value/saturation band.
        #
        # A single global "tame" multiplier cannot fix a patchwork, because the textures start at
        # wildly different brightness and saturation - scaling them all by the same amount
        # preserves the spread that causes it. Normalising to a common target instead means the
        # terrains differ by HUE and STRUCTURE only, which keeps them distinguishable when you look
        # for them without any of them shouting.
        if coherent:
            # 1. highlight rolloff - the confetti comes from dense bright pinpoints going
            #    sub-pixel once tiled ~337x; a Reinhard knee calms them without flattening
            k = 2.6
            a = a * (1.0 + k) / (1.0 + k * a)

            # 2. cap saturation toward a shared ceiling
            lum = (a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722)[..., None]
            mx = a.max(axis=2); mn = a.min(axis=2); litm = mx > 0.05
            cur = float(((mx[litm] - mn[litm]) / mx[litm]).mean()) if litm.any() else 0.0
            if cur > SAT_CAP:
                g = SAT_CAP / cur
                a = lum + (a - lum) * g

            # 3. normalise mean luminance to the target for this material
            target = BRIGHT_NOTABLE if any(t in mid for t in NOTABLE) else BRIGHT_TARGET
            cl = float((a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722).mean())
            if cl > 1e-4:
                a = a * (target / cl)
            a = np.clip(a, 0.0, 1.0)

        c = contrast_override if contrast_override is not None else p.get("contrast", 1.0)
        if c != 1.0:
            # pull toward the image's own darkest tone rather than toward black, so the
            # source's colour identity survives the contrast reduction
            floor = np.percentile(a.reshape(-1, 3), 2, axis=0)[None, None, :]
            a = floor + (a - floor) * c

        lum = a[..., 0] * 0.2126 + a[..., 1] * 0.7152 + a[..., 2] * 0.0722
        lo, hi = float(lum.min()), float(lum.max())
        height = (lum - lo) / (hi - lo + 1e-6)          # alpha = height, drives the 4-way blend

        # Soften only the finest scale of the COLOUR, never the height.
        #
        # DXT5 fits two RGB565 endpoints per 4x4 block, so blocks containing pinpoint stars on a
        # dark field get a wide endpoint spread and the in-between pixels land on wrong hues -
        # measured ~16% chroma error, which is the coloured speckle. Brightening does not help
        # (the error scales with the block's range, not with absolute level); reducing the
        # amplitude of the finest detail does. That detail is invisible at map zoom anyway, because
        # the mip chain averages it to flat grey - but it is exactly what the height blend needs,
        # so the alpha above keeps the full-detail version.
        if soften > 0.0:
            # Low-pass the colour to just under what the screen can resolve.
            #
            # One texture tile spans ~27 world units (detail_tile_factor 337.5 across a 9216-unit
            # map). At normal play zoom that tile lands on 55-110 screen pixels, so 5-9 source
            # pixels average into every screen pixel and the GPU is sampling mip 2-3. Pinpoint
            # stars 1-3 px wide are therefore sub-pixel at every playable zoom: they can never be
            # seen as stars, only as shimmer. Removing them costs nothing and is what kills the
            # confetti. Radius scales with soften; 1.0 clears detail finer than ~7 px.
            radius = 3.0 * soften
            blur = np.stack([np.asarray(Image.fromarray((a[..., c] * 255).astype(np.uint8))
                                        .filter(ImageFilter.GaussianBlur(radius)), dtype=np.float32) / 255.0
                             for c in range(3)], axis=2)
            a = np.clip(blur + (a - blur) * (1.0 - soften), 0.0, 1.0)

        spec = np.full((SIZE, SIZE), p.get("spec", 0.15), np.float32) + height * p.get("spec_h", 0.1)
        metal = np.full((SIZE, SIZE), p.get("metal", 0.0), np.float32)
        rough = np.clip(np.full((SIZE, SIZE), p.get("rough", 0.85), np.float32)
                        - height * p.get("rough_h", 0.15), 0, 1)

        write_material(outdir, mid, np.clip(a, 0, 1), height, spec, metal, rough, SIZE)
        flag = "" if err < 2.0 else ("  [seam " + ("fixed" if seamless else "VISIBLE - rerun with --seamless") + "]")
        print(f"  {mid:26s} <- {f}{flag}")
        done += 1

    if not check:
        print(f"\nimported {done} material(s)")
    for f, why in skipped:
        print(f"  SKIPPED {f}: {why}")
    if skipped:
        print("\nValid material ids:")
        for k in sorted(params):
            print("   ", k)


if __name__ == "__main__":
    main()
