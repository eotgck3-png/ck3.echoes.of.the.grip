"""CPU preview of the terrain effect shaders, so a look can be judged before it ships.

Why this exists. pdxterrain.shader cannot be compiled or run here, so every visual change has been
going straight to the game unverified - and three of them came back wrong (moire from normalised
gradients, a blown-out pink from a bad gain, a blend jitter at the wrong frequency). All three were
predictable on paper. This reimplements the shader's own maths in numpy, runs it over the REAL
heightmap, and scores the result against the project's existing aliasing gates.

What it is faithful to. EotgStarHash / EotgValueNoise / EotgFbm are ported exactly, so the noise
matches what the GPU will produce. EotgFxBands is ported exactly, including altitude banding. The
hypsometric ramp and hillshade are ported. Engine lighting, the colormap soft-light and the
detail-texture structure are NOT modelled - so treat the output as "what the effect contributes",
not a screenshot.

The one genuine unknown is WORLD UNITS PER HEIGHTMAP PIXEL, which sets how the scale parameters
land. --wpp sweeps it; everything height-derived in the shader inherits that uncertainty.

Usage:
    python docs/tools/preview_terrain_fx.py                 # current vs proposed, auto-picked relief
    python docs/tools/preview_terrain_fx.py --wpp 0.5,1,2   # sweep the scale unknown
    python docs/tools/preview_terrain_fx.py --crop 4000 2000
"""
from __future__ import annotations

import argparse
import os
import sys

import numpy as np
from PIL import Image

Image.MAX_IMAGE_PIXELS = None

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
HEIGHTMAP = r"D:\SteamLibrary\steamapps\common\Crusader Kings III\game\map_data\heightmap.png"
OUT = os.path.join(HERE, "preview_nebula.png")

# ---------------------------------------------------------------- shader maths, ported verbatim

def star_hash(x, y):
    """EotgStarHash: frac( sin( dot( p, (127.1, 311.7) ) ) * 43758.5453 )"""
    return np.modf(np.sin(x * 127.1 + y * 311.7) * 43758.5453)[0] % 1.0


def value_noise(x, y):
    """EotgValueNoise: bilinear hash lattice with smoothstep interpolation."""
    ix, iy = np.floor(x), np.floor(y)
    fx, fy = x - ix, y - iy
    fx = fx * fx * (3.0 - 2.0 * fx)
    fy = fy * fy * (3.0 - 2.0 * fy)
    a = star_hash(ix, iy)
    b = star_hash(ix + 1.0, iy)
    c = star_hash(ix, iy + 1.0)
    d = star_hash(ix + 1.0, iy + 1.0)
    return (a + (b - a) * fx) + ((c + (d - c) * fx) - (a + (b - a) * fx)) * fy


def fbm(x, y):
    """EotgFbm: 3 octaves, amp 0.5 halving, freq 2.03x."""
    s = np.zeros_like(x)
    amp = 0.5
    px, py = x.copy(), y.copy()
    for _ in range(3):
        s += amp * value_noise(px, py)
        px *= 2.03
        py *= 2.03
        amp *= 0.5
    return s


def fx_bands(xz_x, xz_y, scale, P, Q, h01):
    """EotgFxBands, including the altitude-banding blend."""
    px, py = xz_x * scale, xz_y * scale
    warp = fbm(px * Q[0], py * Q[0])
    coord = (px * P[0] + py * P[1]) * P[2] * (1.0 - Q[3]) + (h01 * Q[2]) * Q[3]
    t = 0.5 + 0.5 * np.sin(coord + warp * P[3])
    if Q[1] > 0.0:
        return np.clip(t * t * (0.45 + Q[1] * fbm(px * 1.7, py * 1.7)), 0, 1)
    return np.clip((np.clip(t, 0, 1) - 0.22) / (0.78 - 0.22), 0, 1) ** 2 * (3 - 2 * np.clip((np.clip(t, 0, 1) - 0.22) / (0.78 - 0.22), 0, 1))


# ---------------------------------------------------------------- the proposal

def _density(px, py, shape):
    """Candidate density fields. The shape of the noise is what decides whether this reads as
    dense gas or as something else entirely - the first attempt used a ridged inversion and came
    out as lace, which is why these are compared side by side rather than chosen on paper."""
    if shape == "ridged":            # 1 - |2n-1| : thin bright filaments. Reads as veins/lace.
        return np.clip(1.0 - np.abs(fbm(px, py) * 2.0 - 1.0), 0, 1) ** 1.6
    if shape == "soft":              # smoothstep on plain fbm : soft rounded clumps
        t = np.clip((fbm(px, py) - 0.30) / 0.45, 0, 1)
        return t * t * (3 - 2 * t)
    if shape == "billow":            # |2n-1| : puffy cauliflower, bright where noise is extreme
        return np.clip(np.abs(fbm(px, py) * 2.0 - 1.0), 0, 1) ** 0.8
    if shape == "dense":
        # Big clouds with clear voids, then a finer octave for edge detail. A nebula is mostly
        # structure at LARGE scale - uniform mid-frequency mottle reads as haze, not as a cloud.
        big = fbm(px * 0.45, py * 0.45)
        t = np.clip((big - 0.26) / 0.34, 0, 1)
        t = t * t * (3 - 2 * t)
        fine = np.abs(fbm(px * 1.9, py * 1.9) * 2.0 - 1.0)
        return np.clip(t * (0.72 + 0.55 * fine), 0, 1)
    if shape == "turb":              # turbulence: summed |octaves|, wispy but dense
        acc = np.zeros_like(px)
        amp, fx_, fy_ = 0.6, px.copy(), py.copy()
        for _ in range(4):
            acc += amp * np.abs(value_noise(fx_, fy_) * 2.0 - 1.0)
            fx_ *= 2.07
            fy_ *= 2.07
            amp *= 0.55
        return np.clip(1.0 - acc, 0, 1) ** 1.2
    raise SystemExit("unknown shape " + shape)


def fx_nebula(xz_x, xz_y, h01, view_xz, view_up, time, p):
    """Proposed kind 6: layers parallaxed against the view, composited front to back, thickened at
    grazing angles, with emissive cores. Returns (density 0..1, emission 0..1)."""
    trans = np.ones_like(xz_x)          # front-to-back transmittance
    dens = np.zeros_like(xz_x)
    emis = np.zeros_like(xz_x)
    n = p["layers"]
    for i in range(n):
        # Layer altitude above the surface; higher ground lifts it further, so parallax is
        # strongest exactly where the mountain is tallest.
        alt = p["layer_alt"] * (i + 1) * (0.30 + 0.70 * h01)
        ox = view_xz[0] * alt * p["parallax"]
        oy = view_xz[1] * alt * p["parallax"]
        sc = p["scale"] * (1.0 + 0.45 * i)
        px = (xz_x + ox) * sc
        py = (xz_y + oy) * sc
        if p["churn"] > 0.0:
            px = px + np.sin(time * p["churn"] * (0.6 + 0.3 * i)) * 0.9
            py = py + np.cos(time * p["churn"] * (0.5 + 0.4 * i)) * 0.9
        d = _density(px, py, p["shape"])
        # Front-to-back: a layer only shows through what is still transparent in front of it.
        # This is what makes stacked layers read as depth instead of as an average.
        contrib = d * trans
        dens += contrib
        trans *= (1.0 - d * p["opacity"])
        if i == 0:
            emis = np.clip(d - p["emit_thresh"], 0, 1) / max(1e-3, 1 - p["emit_thresh"])
    graze = 1.0 / max(1e-2, abs(view_up))
    dens = np.clip(dens * p["gain"] * min(graze, p["graze_max"]), 0, 1)
    return dens, np.clip(emis, 0, 1)


# ---------------------------------------------------------------- metrics (as import_terrain_textures)

def box_blur(a, r):
    k = 2 * r + 1
    pad = np.pad(a, r, mode="reflect")
    c = np.cumsum(np.cumsum(pad, axis=0), axis=1)
    c = np.pad(c, ((1, 0), (1, 0)))
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def metrics(rgb):
    lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
    mean_l = lum.mean()
    lc = float((lum - box_blur(lum, 4)).std() / (mean_l + 1e-6))
    pr = float((np.percentile(lum, 99.9) - mean_l) / (mean_l + 1e-6))
    return lc, pr


def minify_crawl(render_fn, shift):
    """Render the same content offset by a sub-pixel amount and minified; a stable field gives
    nearly the same image, a sparkly one does not. This is the 'crawls when the camera moves'
    failure, measured rather than eyeballed."""
    a = render_fn(0.0)
    b = render_fn(shift)
    f = 6
    h, w = a.shape[0] // f * f, a.shape[1] // f * f
    da = a[:h, :w].reshape(h // f, f, w // f, f, 3).mean(axis=(1, 3))
    db = b[:h, :w].reshape(h // f, f, w // f, f, 3).mean(axis=(1, 3))
    la = 0.2126 * da[..., 0] + 0.7152 * da[..., 1] + 0.0722 * da[..., 2]
    lb = 0.2126 * db[..., 0] + 0.7152 * db[..., 1] + 0.0722 * db[..., 2]
    return float(np.abs(la - lb).mean() / (la.mean() + 1e-6))


# ---------------------------------------------------------------- scene

def load_relief(crop, want):
    im = Image.open(HEIGHTMAP)
    W, H = im.size
    small = np.asarray(im.resize((W // 64, H // 64), Image.BILINEAR), dtype=np.float32)
    small /= small.max() + 1e-6
    if want is None:
        # pick the most mountainous window we can find rather than guessing at geography
        s = 12
        best, bxy = -1, (0, 0)
        for yy in range(0, small.shape[0] - s, 4):
            for xx in range(0, small.shape[1] - s, 4):
                blk = small[yy:yy + s, xx:xx + s]
                if blk.mean() < 0.02:
                    continue
                v = blk.std()
                if v > best:
                    best, bxy = v, (xx * 64, yy * 64)
        want = bxy
    x0, y0 = want
    x0 = int(np.clip(x0, 0, W - crop[0]))
    y0 = int(np.clip(y0, 0, H - crop[1]))
    box = (x0, y0, x0 + crop[0], y0 + crop[1])
    h = np.asarray(im.crop(box), dtype=np.float32)
    h /= 65535.0 if h.max() > 1.5 else 1.0
    return h, (x0, y0)


TINT_LOW = np.array([0.389, 0.224, 0.764])
TINT_HI = np.array([0.812, 0.710, 1.000])
SHADE_DIR = np.array([-0.60, -0.80])


def hypso(h01):
    t = np.clip((h01 - 0.13) / (0.46 - 0.13), 0, 1)
    t = t * t * (3 - 2 * t) * 0.65
    return TINT_LOW[None, None, :] * (1 - t[..., None]) + TINT_HI[None, None, :] * t[..., None]


def hillshade(h01, wpp, gain=120.0, amount=0.55):
    e = max(1, int(round(8.0 / wpp)))
    gx = (np.roll(h01, -e, 1) - np.roll(h01, e, 1)) / (2 * e * wpp)
    gy = (np.roll(h01, -e, 0) - np.roll(h01, e, 0)) / (2 * e * wpp)
    x = (gx * SHADE_DIR[0] + gy * SHADE_DIR[1]) * gain
    s = x / (1.0 + np.abs(x))       # matches EotgHillshade: compress, never clip
    return 1.0 + amount * s


# Defaults are the configuration the sweep settled on. GAIN IS THE CRITICAL ONE: at 1.25 the
# density field saturated (94% of pixels above 0.5), which flattened it into a uniform wash and
# destroyed the parallax at the same time - measured view response collapsed from 0.85 to 0.10.
# A field with no dynamic range left cannot move. Keep coverage roughly 0.15-0.40.
NEB = dict(layers=3, layer_alt=26.0, parallax=1.0, scale=0.055, churn=0.0, shape="billow",
           opacity=0.85, gain=0.55, graze_max=2.1, emit_thresh=0.55)


def density_only(h01, wpp, cfg, view):
    hh, ww = h01.shape
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    p = dict(NEB); p.update(cfg)
    d, _ = fx_nebula(xx * wpp, yy * wpp, h01, view["xz"], view["up"], 0.0, p)
    return d


def render(h01, wpp, mode, view, time=0.0, sub=0.0):
    hh, ww = h01.shape
    yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32)
    X = (xx + sub) * wpp
    Y = (yy + sub) * wpp

    base = hypso(h01)
    shade = hillshade(h01, wpp)[..., None]

    if isinstance(mode, str) and mode == "current":
        f = fx_bands(X, Y, 0.055, (1.0, 0.35, 2.2, 2.8), (0.5, 0.70, 30.0, 0.30), h01)
        col = base * shade
        add = TINT_LOW[None, None, :] * f[..., None] * 0.34 * 1.6
        mul = (0.58 + (1 - 0.58) * f)[..., None]
        return np.clip(col * mul + add, 0, 1)

    p = dict(NEB)
    p.update(mode if isinstance(mode, dict) else {})
    dens, emis = fx_nebula(X, Y, h01, view["xz"], view["up"], time, p)
    col = base * shade
    body = TINT_LOW * 0.55 + TINT_HI * 0.45
    add = body[None, None, :] * dens[..., None] * 0.42
    core = np.array([1.00, 0.86, 0.72])
    add = add + core[None, None, :] * emis[..., None] * 0.30
    mul = (1.0 - 0.55 * dens)[..., None]
    return np.clip(col * mul + add, 0, 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--wpp", default="1.0", help="world units per heightmap pixel, comma separated")
    ap.add_argument("--crop", type=int, nargs=2, default=(560, 420))
    ap.add_argument("--at", type=int, nargs=2, default=None)
    args = ap.parse_args()

    h01, at = load_relief(tuple(args.crop), tuple(args.at) if args.at else None)
    print(f"relief crop {args.crop[0]}x{args.crop[1]} at {at}  "
          f"height {h01.min():.3f}-{h01.max():.3f} mean {h01.mean():.3f}")

    # two camera angles: overhead-ish and a shallow one, to see whether parallax/grazing respond
    cams = {
        "steep": dict(xz=(0.25, 0.42), up=0.88),
        "shallow": dict(xz=(0.78, 0.55), up=0.34),
    }

    wpps = [float(x) for x in args.wpp.split(",")]
    wpp = wpps[0]
    panels, labels = [], []
    img = render(h01, wpp, "current", cams["steep"])
    lc, pr = metrics(img)
    panels.append(img); labels.append("current")
    print("")
    print(f"{'panel':22} {'lc<0.35':>8} {'peak<3':>8} {'view resp':>10} {'crawl':>8}"
          f" {'dens resp':>9} {'dense%':>7}")
    print(f"{'current':22} {lc:8.3f} {pr:8.3f} {'-':>10} "
          f"{minify_crawl(lambda s: render(h01, wpp, 'current', cams['steep'], sub=s), 0.5):8.4f}")
    for shape in ("soft", "billow", "turb", "dense"):
        cfg = dict(shape=shape)
        a = render(h01, wpp, cfg, cams["steep"])
        b = render(h01, wpp, cfg, cams["shallow"])
        lc, pr = metrics(a)
        la = 0.2126*a[...,0] + 0.7152*a[...,1] + 0.0722*a[...,2]
        lb = 0.2126*b[...,0] + 0.7152*b[...,1] + 0.0722*b[...,2]
        vr = float(np.abs(la-lb).mean()/(la.mean()+1e-6))
        da = density_only(h01, wpp, cfg, cams["steep"])
        db = density_only(h01, wpp, cfg, cams["shallow"])
        dvr = float(np.abs(da-db).mean()/(da.mean()+1e-6))
        cov = float((da > 0.5).mean())
        cr = minify_crawl(lambda s: render(h01, wpp, cfg, cams["steep"], sub=s), 0.5)
        gate = "PASS" if (lc < 0.35 and pr < 3.0) else "FAIL"
        print(f"{shape:22} {lc:8.3f} {pr:8.3f} {vr:10.3f} {cr:8.4f} {dvr:9.3f} {cov:7.2f}   {gate}")
        panels.append(a); labels.append(shape)

    pad = 8
    ph, pw = panels[0].shape[:2]
    cols = len(panels)
    sheet = np.zeros((ph, pw * cols + pad * (cols - 1), 3), dtype=np.float32)
    for i, pnl in enumerate(panels):
        sheet[:, i * (pw + pad):i * (pw + pad) + pw] = pnl
    Image.fromarray((np.clip(sheet, 0, 1) ** (1 / 2.2) * 255).astype(np.uint8)).save(OUT)
    print(f"\nwrote {OUT}   panels left to right: {', '.join(labels)}")


if __name__ == "__main__":
    main()
