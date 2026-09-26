"""
Recolour the ground decals drawn under every holding.

CK3 blends a ground decal beneath each holding so the building sits in its landscape. On the
vanilla map that decal is grass and dirt; against the EotG void it reads as a bright green island
floating in space, and it is the single most visible medieval tell once the terrain goes dark.

Only 5 decal textures exist in the whole game (357 holding assets share them via the `decal_local`
shader), so this is a cheap, contained fix:

    building_mena_city_01_decal        western_city_01_decal
    building_mena_temple_islamic_decal western_temple_christian_decal
                                       western_walls_01_decal

This desaturates and darkens the diffuse while keeping the wear, edge shape and alpha intact, and
applies a faint palette tint, so the decal still grounds the building but reads as lit platform
rather than grass. The normal and properties maps are left alone - the surface relief is fine, it
is only the colour that was wrong.

Usage:  python build_holding_decals.py <mod root> [--tint violet|gold|neutral] [--darken 0.45]
"""
import os, sys, struct, io, glob
import numpy as np
from PIL import Image

GAME = r"D:\SteamLibrary\steamapps\common\Crusader Kings III\game"
SRC = os.path.join(GAME, "gfx", "models", "buildings", "holdings")
REL = os.path.join("gfx", "models", "buildings", "holdings")

TINTS = {
    "violet":  np.array([0.62, 0.52, 0.85], np.float32),
    "gold":    np.array([0.95, 0.82, 0.55], np.float32),
    "neutral": np.array([0.80, 0.82, 0.88], np.float32),
}


def dds_dxt5_with_mips(img, path):
    """DXT5 + full mip chain, matching the vanilla decal format (256x256, 9 mips)."""
    levels = [img.convert("RGBA")]
    while levels[-1].size[0] > 1 and levels[-1].size[1] > 1:
        w, h = levels[-1].size
        levels.append(levels[-1].resize((max(1, w // 2), max(1, h // 2)), Image.BOX))
    w, h = img.size
    flags = 0x1 | 0x2 | 0x4 | 0x1000 | 0x80000 | 0x20000
    linear = max(1, (w + 3) // 4) * max(1, (h + 3) // 4) * 16
    hdr = b"DDS " + struct.pack("<IIIIIII", 124, flags, h, w, linear, 0, len(levels)) + b"\0" * 44
    hdr += struct.pack("<II4sIIIII", 32, 0x4, b"DXT5", 0, 0, 0, 0, 0)
    hdr += struct.pack("<IIIII", 0x1000 | 0x400008, 0, 0, 0, 0)
    with open(path, "wb") as f:
        f.write(hdr)
        for lv in levels:
            buf = io.BytesIO()
            lv.save(buf, format="DDS", pixel_format="DXT5")
            f.write(buf.getvalue()[128:])


def main():
    root = sys.argv[1]
    tint_name = sys.argv[sys.argv.index("--tint") + 1] if "--tint" in sys.argv else "violet"
    darken = float(sys.argv[sys.argv.index("--darken") + 1]) if "--darken" in sys.argv else 0.45
    tint = TINTS[tint_name]

    out = os.path.join(root, REL)
    os.makedirs(out, exist_ok=True)

    files = sorted(glob.glob(os.path.join(SRC, "*_decal_diffuse.dds")))
    if not files:
        raise SystemExit(f"no decal textures found in {SRC}")

    for p in files:
        im = Image.open(p); im.load(); im = im.convert("RGBA")
        a = np.asarray(im).astype(np.float32) / 255.0
        rgb, alpha = a[..., :3], a[..., 3]

        # keep the luminance structure (wear, tracks, edges), throw away the hue
        lum = rgb[..., 0] * 0.2126 + rgb[..., 1] * 0.7152 + rgb[..., 2] * 0.0722
        newrgb = lum[..., None] * tint[None, None, :] * darken

        o = np.zeros_like(a)
        o[..., :3] = np.clip(newrgb, 0, 1)
        o[..., 3] = alpha                      # alpha is the decal's shape - never touch it
        dst = os.path.join(out, os.path.basename(p))
        dds_dxt5_with_mips(Image.fromarray((o * 255).astype(np.uint8), "RGBA"), dst)
        before = (rgb.reshape(-1, 3).mean(0) * 255).round(1)
        after = (o[..., :3].reshape(-1, 3).mean(0) * 255).round(1)
        print(f"  {os.path.basename(p):48s} {before} -> {after}")

    print(f"\n{len(files)} decal diffuse textures rewritten ({tint_name}, darken {darken})")
    print("normal / properties left as vanilla - only the colour was wrong")


if __name__ == "__main__":
    main()
