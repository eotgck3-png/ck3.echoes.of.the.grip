"""
Generate gfx/map/terrain/colormap.dds for Echoes of the Grip.

The colormap is soft-light blended over the blended detail materials:

    Diffuse = SoftLight( DetailDiffuse, ToLinear(colormap), (1 - properties.R) * 1.0 )

and `ToLinear` is pow(x, 2.2). SoftLight( Base, 0.5 ) == Base exactly, so a colormap whose
*linear* value is 0.5 is a perfect no-op. That is sRGB 0.5^(1/2.2) = 0.7297 -> **186**.

Vanilla's colormap is the green-Europe / tan-Sahara / white-Alps tint, which soft-lights straight
over the EotG materials and washes them back to looking like Earth. This writes a near-neutral
replacement with only a slight low-frequency drift toward the purple/gold palette, so the galaxy
has regional character without the materials being recoloured.

Resolution is free: the shader samples it with normalised UVs (WorldSpacePos.xz *
WorldSpaceToTerrain0To1), so this does not have to match the map size. Vanilla is 9216x4608;
half that is plenty for a smooth tint and far cheaper to generate.

Per-material escape hatch: the opacity is (1 - properties.R), so a material with R = 255 ignores
the colormap completely. The generator currently writes R = 0 (full colormap influence).

Usage:  python build_colormap.py <mod root> [--size 4608x2304] [--drift 0.045]
"""
import os, sys
import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_terrain_materials import save_dds_dxt5   # shared DXT5 + mip-chain writer

NEUTRAL_SRGB = 186          # 0.5 ^ (1/2.2) * 255 -> soft-light no-op
# Global darkening lives here, not in the textures. Soft-light below the no-op darkens the terrain,
# which lets the textures stay bright enough to survive DXT5 compression without speckle.
# 186 = no-op, 106 reproduces a 0.13-brightness texture at ~0.05 on screen.
DEFAULT_LEVEL = 106
DEFAULT_SIZE = (4608, 2304)
DEFAULT_DRIFT = 0.045       # max deviation from neutral, in sRGB 0..1


def lowfreq(h, w, cells, seed):
    g = np.random.default_rng(seed).random((max(2, h // cells), max(2, w // cells))).astype(np.float32)
    return np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC),
                      dtype=np.float32) / 255.0


def main():
    root = sys.argv[1]
    W, H = DEFAULT_SIZE
    if "--size" in sys.argv:
        W, H = (int(v) for v in sys.argv[sys.argv.index("--size") + 1].lower().split("x"))
    drift = float(sys.argv[sys.argv.index("--drift") + 1]) if "--drift" in sys.argv else DEFAULT_DRIFT

    level = int(sys.argv[sys.argv.index("--level") + 1]) if "--level" in sys.argv else DEFAULT_LEVEL
    base = level / 255.0

    # Two independent low-frequency fields: one picks gold-vs-violet, one modulates how strongly.
    hue = lowfreq(H, W, 260, 3)
    amp = lowfreq(H, W, 150, 9)

    gold = np.array([1.00, 0.82, 0.42], np.float32)     # warm
    violet = np.array([0.62, 0.42, 1.00], np.float32)   # cool
    tint = gold[None, None, :] * (1 - hue[..., None]) + violet[None, None, :] * hue[..., None]
    # centre the tint on grey so it only pushes the hue, not the overall level
    tint = tint - tint.mean(axis=2, keepdims=True)

    rgb = base + tint * drift * (0.35 + 0.65 * amp[..., None])
    rgb = np.clip(rgb, 0.0, 1.0)

    out = np.zeros((H, W, 4), np.uint8)
    out[..., :3] = (rgb * 255).astype(np.uint8)
    out[..., 3] = 255            # ColorDarken = 1.0 (only used with cloud shadows, which are disabled)

    d = os.path.join(root, "gfx", "map", "terrain")
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "colormap.dds")
    print(f"writing {W}x{H} colormap (level sRGB {level}, no-op is {NEUTRAL_SRGB}, drift +-{drift:.3f}) ...")
    save_dds_dxt5(Image.fromarray(out, "RGBA"), p)
    print(f"  {p}  {os.path.getsize(p) / 1e6:.1f} MB")
    lo, hi = out[..., :3].min(), out[..., :3].max()
    print(f"  channel range {lo}..{hi}  ({NEUTRAL_SRGB} = exact no-op; lower darkens the terrain)")


if __name__ == "__main__":
    main()
