"""
Generate placeholder terrain materials for Echoes of the Grip.

Produces, for every EotG terrain, a set of CK3 detail materials:
    <id>_diffuse.dds     RGB colour, ALPHA = height  (height drives CK3's 4-way height blend)
    <id>_normal.dds      DXT5nm / RRxG packing: G = normal.x, A = -normal.y  (see UnpackRRxGNormal)
    <id>_properties.dds  G = specular, B = metalness, A = roughness  (R unused)

All textures are seamlessly tileable (detail textures repeat ~337x across the map width)
and are written as DXT5 with a full mip chain.

These are PLACEHOLDERS: procedural programmer-art whose job is to make the whole terrain
pipeline testable before real textures are commissioned. Replacing one is a file copy.

Usage:  python build_terrain_materials.py <mod root> [--size 512]
"""
import os, sys, struct, io, math
import numpy as np
from PIL import Image

SIZE = 512          # MUST be consistent across the whole array: detail textures load into a texture array and every
                    # slice must share resolution/format/mips - including vanilla's
                    # normal_neutral.dds / material_neutral.dds (1024) used by the dynamic slots.
                    # Mixing sizes fails CreateTexture2D and crashes on load.
RNG = np.random.default_rng(20260924)

# ---------------------------------------------------------------- tileable noise helpers

def _wrap_grid(n, rng):
    return rng.random((n, n)).astype(np.float32)

def vnoise(size, n, rng):
    """Value noise from an n x n lattice, smoothly upsampled with wraparound -> tileable."""
    g = _wrap_grid(n, rng)
    g = np.pad(g, ((0, 1), (0, 1)), mode="wrap")          # wrap edge for interpolation
    ys = np.linspace(0, n, size, endpoint=False, dtype=np.float32)
    xs = np.linspace(0, n, size, endpoint=False, dtype=np.float32)
    y0 = np.floor(ys).astype(int); x0 = np.floor(xs).astype(int)
    fy = (ys - y0)[:, None]; fx = (xs - x0)[None, :]
    fy = fy * fy * (3 - 2 * fy); fx = fx * fx * (3 - 2 * fx)   # smoothstep
    a = g[y0][:, x0]; b = g[y0][:, x0 + 1]; c = g[y0 + 1][:, x0]; d = g[y0 + 1][:, x0 + 1]
    return (a * (1 - fx) + b * fx) * (1 - fy) + (c * (1 - fx) + d * fx) * fy

def fbm(size, octaves=5, base=4, gain=0.5, rng=None):
    rng = rng or RNG
    out = np.zeros((size, size), np.float32); amp = 1.0; tot = 0.0; n = base
    for _ in range(octaves):
        out += amp * vnoise(size, n, rng); tot += amp; amp *= gain; n *= 2
    return out / tot

def _wrapped_stamp(acc, cy, cx, r, size, profile):
    """Add a radially-symmetric stamp at (cy,cx), wrapping at the edges."""
    r = int(max(1, r))
    ys = (np.arange(cy - r, cy + r + 1) % size)
    xs = (np.arange(cx - r, cx + r + 1) % size)
    dy = np.arange(-r, r + 1)[:, None]; dx = np.arange(-r, r + 1)[None, :]
    d = np.sqrt(dy * dy + dx * dx) / r
    m = profile(np.clip(d, 0, 1))
    acc[np.ix_(ys, xs)] = np.maximum(acc[np.ix_(ys, xs)], m)

def rocks(size, count, rmin, rmax, rng, sharp=False):
    """Scattered rounded masses -> asteroid / rubble fields."""
    acc = np.zeros((size, size), np.float32)
    prof = (lambda d: np.clip(1 - d, 0, 1) ** 0.6) if sharp else (lambda d: np.sqrt(np.clip(1 - d * d, 0, 1)))
    for _ in range(count):
        cy, cx = rng.integers(0, size, 2)
        r = rng.uniform(rmin, rmax) * size
        _wrapped_stamp(acc, int(cy), int(cx), r, size, prof)
    return acc

def blocks(size, count, wmin, wmax, rng, height_var=0.6):
    """Axis-aligned slabs -> station / fortification geometry."""
    acc = np.zeros((size, size), np.float32)
    for _ in range(count):
        h = rng.uniform(1 - height_var, 1.0)
        bw = int(rng.uniform(wmin, wmax) * size); bh = int(rng.uniform(wmin, wmax) * size)
        if rng.random() < 0.5: bw, bh = bh, bw
        cy, cx = int(rng.integers(0, size)), int(rng.integers(0, size))
        ys = (np.arange(cy, cy + bh) % size); xs = (np.arange(cx, cx + bw) % size)
        acc[np.ix_(ys, xs)] = np.maximum(acc[np.ix_(ys, xs)], h)
    return acc

def lanes(size, count, width, rng, vertical=True, wobble=0.0, segment=True):
    """Transit corridors.

    A lane that spans the full tile height joins up with its own copy in the next tile, producing
    one continuous rail across the entire map once the texture repeats ~337x. So by default each
    lane is a SEGMENT occupying a random vertical span strictly inside the tile, fading to zero at
    both ends; spans differ per lane, so there is no banding at the tile seams either.
    Pass segment=False only for a texture that is genuinely meant to read as unbroken.
    """
    acc = np.zeros((size, size), np.float32)
    t = np.arange(size, dtype=np.float32)
    for _ in range(count):
        pos = rng.uniform(0, size)
        amp = wobble * size
        off = pos + amp * np.sin(2 * np.pi * t / size * rng.integers(1, 3) + rng.uniform(0, 6.28))
        w = width * size * rng.uniform(0.6, 1.4)
        d = np.abs(((np.arange(size)[None, :] - off[:, None] + size / 2) % size) - size / 2)
        prof = np.exp(-(d / w) ** 2) * rng.uniform(0.6, 1.0)
        if segment:
            L = rng.uniform(size * 0.22, size * 0.55)
            s0 = rng.uniform(0.0, size - L)
            u = (t - s0) / L
            env = np.clip(1.0 - (2.0 * u - 1.0) ** 2, 0.0, 1.0) ** 0.7
            env[(t < s0) | (t > s0 + L)] = 0.0
            prof = prof * env[:, None]
        acc = np.maximum(acc, prof)
    return acc if vertical else acc.T

def crystal(size, count, rmin, rmax, rng):
    """Angular faceted shards -> ice / crystalline."""
    acc = np.zeros((size, size), np.float32)
    for _ in range(count):
        cy, cx = int(rng.integers(0, size)), int(rng.integers(0, size))
        r = int(rng.uniform(rmin, rmax) * size)
        ys = (np.arange(cy - r, cy + r + 1) % size); xs = (np.arange(cx - r, cx + r + 1) % size)
        dy = np.arange(-r, r + 1)[:, None] / r; dx = np.arange(-r, r + 1)[None, :] / r
        ang = rng.uniform(0, 3.14); ca, sa = math.cos(ang), math.sin(ang)
        u = dx * ca - dy * sa; v = dx * sa + dy * ca
        d = np.maximum(np.abs(u) * rng.uniform(1.0, 2.2), np.abs(v))   # diamond/shard
        m = np.clip(1 - d, 0, 1) ** 0.5
        acc[np.ix_(ys, xs)] = np.maximum(acc[np.ix_(ys, xs)], m)
    return acc

def sparks(size, count, rng, r=0.004):
    """Small bright points -> running lights / beacons."""
    acc = np.zeros((size, size), np.float32)
    for _ in range(count):
        cy, cx = int(rng.integers(0, size)), int(rng.integers(0, size))
        _wrapped_stamp(acc, cy, cx, max(1, r * size), size, lambda d: np.clip(1 - d, 0, 1) ** 2)
    return acc

def norm01(a):
    lo, hi = float(a.min()), float(a.max())
    return (a - lo) / (hi - lo + 1e-8)

def starfield(size, count, rng, rmin=0.0015, rmax=0.006, falloff=2.5):
    """Points of light = systems. Density is the main signal separating cluster types."""
    acc = np.zeros((size, size), np.float32)
    for _ in range(count):
        cy, cx = int(rng.integers(0, size)), int(rng.integers(0, size))
        r = rng.uniform(rmin, rmax) * size
        b = rng.uniform(0.35, 1.0) ** 1.6          # most stars dim, a few bright
        _wrapped_stamp(acc, cy, cx, r, size, lambda d, b=b: b * np.clip(1 - d, 0, 1) ** falloff)
    return acc

def nebula(size, rng, scale=3, octaves=6, sharp=1.0):
    """Gas cloud. sharp > 1 tightens it into walls, < 1 leaves it diffuse."""
    a = norm01(fbm(size, octaves, scale, rng=rng))
    return np.clip(a ** sharp, 0, 1)

def anomaly(size, count, rng, rmin=0.05, rmax=0.18):
    """Concentric distortion rings -> gravitational lensing / unstable objects."""
    acc = np.zeros((size, size), np.float32)
    for _ in range(count):
        cy, cx = int(rng.integers(0, size)), int(rng.integers(0, size))
        r = int(rng.uniform(rmin, rmax) * size)
        ys = (np.arange(cy - r, cy + r + 1) % size); xs = (np.arange(cx - r, cx + r + 1) % size)
        dy = np.arange(-r, r + 1)[:, None] / r; dx = np.arange(-r, r + 1)[None, :] / r
        d = np.sqrt(dy * dy + dx * dx)
        rings = np.cos(d * rng.uniform(8.0, 16.0)) * 0.5 + 0.5
        m = np.clip(1 - d, 0, 1) ** 1.5 * rings
        acc[np.ix_(ys, xs)] = np.maximum(acc[np.ix_(ys, xs)], m)
    return acc

def flares(size, count, rng, r=0.02):
    """Bright unstable stars with radial spikes -> volatile systems."""
    acc = np.zeros((size, size), np.float32)
    for _ in range(count):
        cy, cx = int(rng.integers(0, size)), int(rng.integers(0, size))
        rr = int(max(3, r * size * rng.uniform(0.6, 1.5)))
        ys = (np.arange(cy - rr, cy + rr + 1) % size); xs = (np.arange(cx - rr, cx + rr + 1) % size)
        dy = np.arange(-rr, rr + 1)[:, None] / rr; dx = np.arange(-rr, rr + 1)[None, :] / rr
        d = np.sqrt(dy * dy + dx * dx)
        core = np.clip(1 - d, 0, 1) ** 3
        spike = np.clip(1 - np.minimum(np.abs(dx), np.abs(dy)) * 6.0, 0, 1) * np.clip(1 - d, 0, 1) ** 1.2
        acc[np.ix_(ys, xs)] = np.maximum(acc[np.ix_(ys, xs)], np.clip(core + spike * 0.7, 0, 1))
    return acc

# ---------------------------------------------------------------- DDS output (DXT5 + mips)

def _dxt5_payload(img):
    """Compress one RGBA image to raw BC3 blocks via Pillow, stripping the 128-byte header."""
    buf = io.BytesIO()
    img.convert("RGBA").save(buf, format="DDS", pixel_format="DXT5")
    return buf.getvalue()[128:]

def save_dds_dxt5(img, path):
    """DXT5 with a full mip chain, matching vanilla detail textures."""
    levels = [img.convert("RGBA")]
    while levels[-1].size[0] > 1 and levels[-1].size[1] > 1:
        w, h = levels[-1].size
        levels.append(levels[-1].resize((max(1, w // 2), max(1, h // 2)), Image.BOX))
    w, h = img.size
    flags = 0x1 | 0x2 | 0x4 | 0x1000 | 0x80000 | 0x20000          # caps|h|w|pixelformat|linearsize|mipmapcount
    linear = max(1, (w + 3) // 4) * max(1, (h + 3) // 4) * 16
    hdr = b"DDS " + struct.pack("<IIIIIII", 124, flags, h, w, linear, 0, len(levels)) + b"\0" * 44
    hdr += struct.pack("<II4sIIIII", 32, 0x4, b"DXT5", 0, 0, 0, 0, 0)
    hdr += struct.pack("<IIIII", 0x1000 | 0x400008, 0, 0, 0, 0)
    assert len(hdr) == 128
    with open(path, "wb") as f:
        f.write(hdr)
        for lv in levels:
            f.write(_dxt5_payload(lv))

def save_dds_uncompressed(img, path):
    """Uncompressed A8R8G8B8 with a full mip chain.

    BC3/DXT5 fits two RGB565 endpoints per 4x4 block, so dark textures with pinpoint highlights
    get a wide endpoint spread and the in-between pixels land on wrong hues - measured ~16% chroma
    error on these, which reads as coloured speckle once the map lifts it with exposure. At 512
    uncompressed the VRAM cost is identical to 1024 DXT5 (1.4 MB per slice) and the artifact is
    gone entirely; at map zoom the resolution difference is not visible because mip 1-3 is what
    gets sampled. Vanilla ships thousands of uncompressed DDS, so the engine is fine with it.
    """
    levels = [img.convert("RGBA")]
    while levels[-1].size[0] > 1 and levels[-1].size[1] > 1:
        w, h = levels[-1].size
        levels.append(levels[-1].resize((max(1, w // 2), max(1, h // 2)), Image.BOX))
    w, h = img.size
    flags = 0x1 | 0x2 | 0x4 | 0x1000 | 0x8 | 0x20000      # caps|h|w|pitch|pixelformat|mipmapcount
    hdr = b"DDS " + struct.pack("<IIIIIII", 124, flags, h, w, w * 4, 0, len(levels)) + bytes(44)
    hdr += struct.pack("<IIIIIIII", 32, 0x41, 0, 32, 0x00ff0000, 0x0000ff00, 0x000000ff, 0xff000000)
    hdr += struct.pack("<IIIII", 0x1000 | 0x400008, 0, 0, 0, 0)
    assert len(hdr) == 128
    with open(path, "wb") as f:
        f.write(hdr)
        for lv in levels:
            f.write(np.asarray(lv)[:, :, [2, 1, 0, 3]].tobytes())   # BGRA


def write_material(outdir, mid, rgb, height, spec, metal, rough, size):
    """rgb: HxWx3 float 0..1; height/spec/metal/rough: HxW float 0..1"""
    # diffuse: colour + height in alpha
    d = np.dstack([np.clip(rgb, 0, 1) * 255, np.clip(height, 0, 1) * 255]).astype(np.uint8)
    save_dds_uncompressed(Image.fromarray(d, "RGBA"), os.path.join(outdir, f"{mid}_diffuse.dds"))

    # normal from height, packed RRxG (G = x, A = -y) per UnpackRRxGNormal
    hpad = np.pad(height, 1, mode="wrap")
    gx = (hpad[1:-1, 2:] - hpad[1:-1, :-2]) * 0.5
    gy = (hpad[2:, 1:-1] - hpad[:-2, 1:-1]) * 0.5
    strength = 6.0
    nx, ny = -gx * strength, -gy * strength
    nz = np.ones_like(nx)
    ln = np.sqrt(nx * nx + ny * ny + nz * nz)
    nx, ny = nx / ln, ny / ln
    n = np.zeros((size, size, 4), np.uint8)
    n[:, :, 0] = np.clip((nx * 0.5 + 0.5) * 255, 0, 255)      # R: copy of x (unused by shader)
    n[:, :, 1] = np.clip((nx * 0.5 + 0.5) * 255, 0, 255)      # G: x
    n[:, :, 2] = 255
    n[:, :, 3] = np.clip((-ny * 0.5 + 0.5) * 255, 0, 255)     # A: -y
    save_dds_uncompressed(Image.fromarray(n, "RGBA"), os.path.join(outdir, f"{mid}_normal.dds"))

    # properties: G = spec, B = metal, A = rough
    p = np.zeros((size, size, 4), np.uint8)
    p[:, :, 1] = np.clip(spec * 255, 0, 255)
    p[:, :, 2] = np.clip(metal * 255, 0, 255)
    p[:, :, 3] = np.clip(rough * 255, 0, 255)
    save_dds_uncompressed(Image.fromarray(p, "RGBA"), os.path.join(outdir, f"{mid}_properties.dds"))

# ---------------------------------------------------------------- terrain recipes

def mix(base, accent, t):
    base = np.array(base, np.float32); accent = np.array(accent, np.float32)
    return base[None, None, :] * (1 - t[..., None]) + accent[None, None, :] * t[..., None]

HX = lambda s: tuple(int(s[i:i + 2], 16) / 255 for i in (1, 3, 5))

def build(kind, size, seed, p):
    """Return (rgb, height, spec, metal, rough) for one material variant."""
    rng = np.random.default_rng(seed)
    grain = fbm(size, 5, 8, rng=rng)
    dark, light = HX(p["dark"]), HX(p["light"])
    metal_v = p.get("metal", 0.0); rough_v = p.get("rough", 0.85); spec_v = p.get("spec", 0.15)

    # --- astrographic vocabulary: star density + nebula density + debris + phenomena ---------
    if kind == "open":            # ordinary navigable space
        st = starfield(size, p.get("stars", 260), rng)
        neb = nebula(size, rng, 3, 6) * p.get("neb", 0.18)
        h = np.clip(st * 0.7 + neb * 0.3, 0, 1); t = np.clip(st * 1.0 + neb, 0, 1)
    elif kind == "dense":         # systems packed close together
        st = starfield(size, p.get("stars", 900), rng, rmin=0.003, rmax=0.010, falloff=1.8)
        neb = nebula(size, rng, 4, 6) * p.get("neb", 0.12)
        h = np.clip(st * 0.9 + neb * 0.25, 0, 1); t = np.clip(st * 1.45 + neb * 0.7, 0, 1)
    elif kind == "barren":        # very few viable systems, long empty distances
        st = starfield(size, p.get("stars", 45), rng, rmax=0.004)
        neb = nebula(size, rng, 2, 5) * p.get("neb", 0.10)
        h = np.clip(st * 0.6 + neb * 0.25, 0, 1); t = np.clip(st * 0.9 + neb, 0, 1)
    elif kind == "broken":        # scattered systems + stellar debris, irregular routes
        R = rocks(size, p.get("n", 170), p.get("rmin", 0.012), p.get("rmax", 0.05), rng)
        st = starfield(size, p.get("stars", 200), rng)
        h = np.clip(R * 0.8 + st * 0.5 + norm01(grain) * 0.15, 0, 1)
        t = np.clip(R * 0.7 + st * 0.9 + norm01(grain) * 0.15, 0, 1)
    elif kind == "nebula_wall":   # dense nebula / radiation forming a chokepoint
        neb = nebula(size, rng, 2, 6, sharp=p.get("sharp", 1.9))
        st = starfield(size, p.get("stars", 90), rng, rmax=0.004)
        h = np.clip(neb * 0.9 + st * 0.3, 0, 1)
        t = np.clip(neb * 1.15 + st * 0.5 * (1.0 - neb), 0, 1)   # stars dim inside the cloud
    elif kind == "wilds":         # chaotic nebula hiding isolated systems
        a = nebula(size, rng, 3, 6); b = nebula(size, rng, 6, 6)
        st = starfield(size, p.get("stars", 150), rng)
        neb = np.clip(a * 0.7 + b * 0.6, 0, 1)
        h = np.clip(neb * 0.8 + st * 0.4, 0, 1)
        t = np.clip(neb * 1.1 + st * 0.7 * (1.0 - neb * 0.8), 0, 1)
    elif kind == "frozen":        # icy bodies, cold and hostile
        C = crystal(size, p.get("n", 120), 0.02, 0.07, rng)
        st = starfield(size, p.get("stars", 180), rng)
        h = np.clip(C * 0.85 + st * 0.4 + norm01(grain) * 0.15, 0, 1)
        t = np.clip(C * 0.9 + st * 0.7, 0, 1)
    elif kind == "anomaly":       # gravitational / radiation phenomena, unpredictable
        A = anomaly(size, p.get("n", 14), rng)
        neb = nebula(size, rng, 4, 6) * 0.5
        st = starfield(size, p.get("stars", 120), rng)
        h = np.clip(A * 0.8 + neb * 0.4 + st * 0.3, 0, 1)
        t = np.clip(A * 1.0 + neb * 0.8 + st * 0.6, 0, 1)
    elif kind == "volatile":      # productive but unstable
        F = flares(size, p.get("n", 26), rng)
        neb = nebula(size, rng, 4, 6) * 0.6
        st = starfield(size, p.get("stars", 220), rng)
        h = np.clip(F * 0.9 + neb * 0.35 + st * 0.3, 0, 1)
        t = np.clip(F * 1.2 + neb * 0.9 + st * 0.6, 0, 1)
    elif kind == "fertile":       # high concentration of favourable systems
        st = starfield(size, p.get("stars", 520), rng, rmax=0.008, falloff=2.0)
        neb = nebula(size, rng, 4, 6) * p.get("neb", 0.35)
        h = np.clip(st * 0.85 + neb * 0.3, 0, 1); t = np.clip(st * 1.15 + neb, 0, 1)
    elif kind == "sanctuary":     # a small favourable pocket
        st = starfield(size, p.get("stars", 300), rng, rmax=0.010, falloff=1.8)
        neb = nebula(size, rng, 5, 6) * 0.30
        h = np.clip(st * 0.9 + neb * 0.3, 0, 1); t = np.clip(st * 1.3 + neb, 0, 1)
    elif kind == "rocks":         # scattered debris catching light -> the land/void boundary
        R = rocks(size, p.get("n", 200), p.get("rmin", 0.006), p.get("rmax", 0.025), rng)
        st = starfield(size, p.get("stars", 80), rng)
        h = np.clip(R * 0.85 + norm01(grain) * 0.2, 0, 1)
        t = np.clip(R * 0.9 + st * 0.5 + norm01(grain) * 0.2, 0, 1)
    elif kind == "layered":       # layered geography: pockets linked by constrained corridors
        base = norm01(fbm(size, 4, 3, rng=rng))
        steps = p.get("steps", 5)
        band = np.floor(base * steps) / steps
        st = starfield(size, p.get("stars", 220), rng)
        pocket = 1.0 - band                      # systems concentrate in the low, linked pockets
        h = np.clip(band * 0.7 + st * pocket * 0.5, 0, 1)
        t = np.clip(band * 0.55 + st * pocket * 1.1, 0, 1)
    else:
        raise ValueError(kind)

    # contrast < 1 compresses the colour swing toward the dark end. High-area "backdrop"
    # terrains want this low: the texture tiles ~337x, so strong contrast reads as an obvious grid,
    # and the terrain is meant to sit behind the glowing lanes/borders rather than compete with them.
    t = np.clip(t, 0, 1).astype(np.float32) * p.get("contrast", 1.0)
    rgb = mix(dark, light, t)
    spec = np.full((size, size), spec_v, np.float32) + (h * p.get("spec_h", 0.1))
    metal = np.full((size, size), metal_v, np.float32)
    rough = np.clip(np.full((size, size), rough_v, np.float32) - h * p.get("rough_h", 0.15), 0, 1)
    return rgb.astype(np.float32), h.astype(np.float32), spec, metal, rough


# terrain -> (EotG name, [ (variant suffix, kind, params) ... ] )
#
# Variant count is weighted by how much map area the terrain covers: repetition only shows where a
# terrain is widespread, so plains gets 3, the mid-sized terrains 2, and the rare ones 1.
# Colours stay dark and low-contrast on the high-area "backdrop" terrains; the rare, notable ones
# (relay nexus, trade corridor, extraction) are allowed to be brighter because they should draw the eye.
# "tile" sets a per-material tile_factor (vanilla default 337.5) so two variants of similar art
# read at different scales.
# ---- active set: 24 terrain materials + 2 edge, allocated by map area --------------------
#
# Names and concepts per the 2026-09-25 terrain scheme, which describes ASTROGRAPHY (star density,
# nebulae, debris, phenomena) rather than civilisation. Terrain is explicitly decoupled from
# development: a Fertile Reach is high natural potential, not a built-up one.
#
# Material ids stay keyed to the VANILLA terrain key (eotg_plains_*, eotg_forest_*, ...) because
# that is what the engine and the terrain index use. Only the display names change, and those live
# in localisation.
#
# Variant count is weighted by how much map area the terrain covers.
TERRAINS = {
 # --- high area: dark, low contrast, multiple variants to defeat tiling -------------------
 "plains":       ("Open Cluster",           [("01","open",  dict(dark="#07070d", light="#4a5068", stars=260, neb=0.18, contrast=0.8, rough=0.9)),
                                             ("02","open",  dict(dark="#06060c", light="#424860", stars=180, neb=0.12, contrast=0.75, rough=0.9)),
                                             ("03","open",  dict(dark="#07070d", light="#464c64", stars=330, neb=0.20, contrast=0.75, rough=0.9, tile=520))]),
 "hills":        ("Broken Cluster",         [("01","broken",dict(dark="#09090e", light="#4e463c", n=170, rmin=0.012, rmax=0.05, stars=200, contrast=0.9, rough=0.92)),
                                             ("02","broken",dict(dark="#08080d", light="#443d35", n=280, rmin=0.006, rmax=0.026, stars=150, contrast=0.85, rough=0.93, tile=700))]),
 "desert":       ("Barren Reach",           [("01","barren",dict(dark="#050509", light="#1e2230", stars=45, neb=0.10, contrast=0.8, rough=0.95)),
                                             ("02","barren",dict(dark="#050508", light="#1a1e2a", stars=28, neb=0.07, contrast=0.75, rough=0.95, tile=220))]),
 "mountains":    ("Nebula Barrier",         [("01","nebula_wall",dict(dark="#08060f", light="#55407e", stars=90, sharp=1.9, contrast=0.9, rough=0.85)),
                                             ("02","nebula_wall",dict(dark="#07050d", light="#493768", stars=60, sharp=2.2, contrast=0.85, rough=0.85, tile=520))]),
 "taiga":        ("Frozen Cluster",         [("01","frozen",dict(dark="#060a11", light="#52708c", n=110, stars=180, contrast=0.8, spec=0.4, rough=0.35)),
                                             ("02","frozen",dict(dark="#05080e", light="#465f78", n=85, stars=130, contrast=0.75, spec=0.35, rough=0.4, tile=620))]),
 "drylands":     ("Arid Reach",             [("01","barren",dict(dark="#0a0806", light="#4a4034", stars=150, neb=0.20, contrast=0.85, rough=0.92)),
                                             ("02","barren",dict(dark="#080705", light="#40382e", stars=110, neb=0.16, contrast=0.8, rough=0.92, tile=450))]),
 "forest":       ("Dense Cluster",          [("01","dense", dict(dark="#08090f", light="#7a8296", stars=1100, neb=0.22, contrast=0.85, rough=0.9)),
                                             ("02","dense", dict(dark="#07080d", light="#6a7285", stars=800, neb=0.18, contrast=0.8, rough=0.9, tile=600))]),
 "steppe":       ("Frontier Reach",         [("01","open",  dict(dark="#08080e", light="#4e5468", stars=130, neb=0.14, contrast=0.8, rough=0.9)),
                                             ("02","open",  dict(dark="#07070c", light="#464c60", stars=95, neb=0.10, contrast=0.75, rough=0.9, tile=550))]),
 # --- low area: one variant each; the notable ones may be brighter ------------------------
 "jungle":       ("Nebula Wilds",           [("01","wilds", dict(dark="#0e0814", light="#9a5a8e", stars=150, contrast=0.9, rough=0.85))]),
 "desert_mountains":("Barren Barrier",      [("01","nebula_wall",dict(dark="#06060c", light="#3e3a52", stars=35, sharp=2.4, contrast=0.85, rough=0.9))]),
 "wetlands":     ("Anomaly Fields",         [("01","anomaly",dict(dark="#06100f", light="#2fa89e", n=14, stars=120, contrast=0.9, spec=0.3, rough=0.5))]),
 "farmlands":    ("Fertile Reach",          [("01","fertile",dict(dark="#100c08", light="#e8c060", stars=520, neb=0.35, spec=0.25, rough=0.7))]),
 "floodplains":  ("Volatile Cluster",       [("01","volatile",dict(dark="#120a06", light="#e07838", n=26, stars=220, spec=0.3, rough=0.65))]),
 "oasis":        ("Sanctuary Systems",      [("01","sanctuary",dict(dark="#120e09", light="#ffd98a", stars=300, spec=0.3, rough=0.6))]),
 "terraced_hills":("Layered Cluster",       [("01","layered",dict(dark="#0a090e", light="#4a4650", steps=5, stars=150, contrast=0.85, rough=0.9))]),
}

# the land/void boundary - vanilla's beach_02 family equivalent
EDGES = [("eotg_edge_01","rocks",dict(dark="#0a0a12", light="#6a2fae", n=220, rmin=0.006, rmax=0.025, contrast=0.9, spec=0.3, rough=0.6)),
         ("eotg_edge_02","rocks",dict(dark="#0b0a10", light="#c99a3c", n=180, rmin=0.008, rmax=0.03, contrast=0.9, spec=0.3, rough=0.6, tile=480))]


def main():
    root = sys.argv[1]
    size = SIZE
    if "--size" in sys.argv: size = int(sys.argv[sys.argv.index("--size") + 1])
    outdir = os.path.join(root, "gfx", "map", "terrain")
    os.makedirs(outdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, "masks"), exist_ok=True)

    entries = []   # (id, terrain, pretty, tile_factor|None)
    previews = []
    seed = 1000
    for terr, (pretty, variants) in TERRAINS.items():
        for suffix, kind, p in variants:
            mid = f"eotg_{terr}_{suffix}"
            rgb, h, spec, metal, rough = build(kind, size, seed, p); seed += 1
            write_material(outdir, mid, rgb, h, spec, metal, rough, size)
            entries.append((mid, terr, pretty, p.get("tile")))
            previews.append((mid, (rgb * 255).astype(np.uint8)))
            print("  ", mid, kind)
    for mid, kind, p in EDGES:
        rgb, h, spec, metal, rough = build(kind, size, seed, p); seed += 1
        write_material(outdir, mid, rgb, h, spec, metal, rough, size)
        entries.append((mid, "edge", "System Edge", p.get("tile")))
        previews.append((mid, (rgb * 255).astype(np.uint8)))
        print("  ", mid, kind)

    # ---- materials.settings ------------------------------------------------
    # The five dynamic materials MUST stay first and in this order (material index is
    # positional - materials.settings says "don't change the order of these"). Their
    # effects are disabled in province_effects.fxh / dynamic_masks.fxh, so they point
    # at a neutral placeholder and never draw.
    L = ["# MOD(eotg) terrain materials. Generated by docs/tools/build_terrain_materials.py",
         "# Placeholder programmer-art: replace the DDS files, keep the ids.",
         "", "{",
         "\t# Dynamic materials - reliant on material index, DO NOT REORDER.",
         "\t# Effects are disabled in the shaders; these point at neutral textures and never draw."]
    for dyn in ["drought", "drought_cracks", "flood", "summer_grass", "winter_effect"]:
        L += ["\t{", f'\t\tname     = "{dyn}"', '\t\tdiffuse  = "eotg_desert_01_diffuse.dds"',
              '\t\tnormal   = "normal_neutral.dds"', '\t\tmaterial = "material_neutral.dds"',
              f'\t\tmask     = "masks/{dyn}_mask.png"', f'\t\tid       = "{dyn}"', "\t}"]
    L += ["", "\t# EotG terrain materials"]
    for mid, terr, pretty, tile_f in entries:
        L += ["\t{", f'\t\tname     = "{mid}"', f'\t\tdiffuse  = "{mid}_diffuse.dds"',
              f'\t\tnormal   = "{mid}_normal.dds"', f'\t\tmaterial = "{mid}_properties.dds"',
              f'\t\tmask     = "masks/{mid}_mask.png"', f'\t\tid       = "{mid}"']
        if tile_f:
            L += [f'\t\ttile_factor = {tile_f}']
        L += [f'\t\t# {terr} -> {pretty}', "\t}"]
    L += ["}", "", "# unmasked textures (vanilla ships this block empty; the parser requires it)",
          "{", "}", ""]
    open(os.path.join(outdir, "materials.settings"), "w", encoding="utf-8", newline="\n").write("\n".join(L))
    print(f"materials.settings: {len(entries) + 5} entries ({len(entries)} EotG + 5 dynamic)")

    # ---- preview sheet -----------------------------------------------------
    cols = 4; tile = 192
    rows = (len(previews) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tile, rows * (tile + 16)), (18, 18, 24))
    from PIL import ImageDraw
    dr = ImageDraw.Draw(sheet)
    for i, (mid, arr) in enumerate(previews):
        im = Image.fromarray(arr).resize((tile, tile), Image.BOX)
        x, y = (i % cols) * tile, (i // cols) * (tile + 16)
        sheet.paste(im, (x, y)); dr.text((x + 3, y + tile + 2), mid, fill=(200, 200, 210))
    prev = os.path.join(os.path.dirname(os.path.abspath(__file__)), "terrain_preview.png")
    sheet.save(prev); print("preview:", prev)

if __name__ == "__main__":
    main()
