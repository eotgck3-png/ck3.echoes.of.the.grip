"""Build the 2D holding-type icons from the same silhouettes as the 3D marker emblems.

A player who learns the marker on the map should recognise the same shape in the UI. So the
icons are not drawn separately. They are the emblems' own outlines, taken from
docs/art/marker_emblems/silhouettes.json, which blender_marker_emblems.py writes from the
front, mirrored as the game shows it.

Two sets, at vanilla's paths, so they override vanilla's files (vanilla 1.20.1.1, scouted
2026-10-20):

  gfx/interface/icons/holding_types_tab/<holding>_holding.dds   70 x 60, all seven types
      The holding tabs in the county window and the ledger. The engine builds the path from the
      holding key (HOLDING_TYPE_TAB_ICON_PATH, 00_graphics.txt:755). Vanilla's are flat BLACK
      silhouettes on alpha, tinted by the UI at runtime, so these are too: no baked colour.
      The content sits about x 7-62, y 4-57.
  gfx/interface/icons/icon_holding_<castle|church|city|temple_citadel>.dds
      Concept links, tooltips and event windows. Vanilla's are full-colour painted sprites, so
      these carry the holding's marker colour with a dark outline that keeps them legible on
      both parchment and dark panels. Vanilla has no tribal, nomad or herder file here.
      Sizes are 60 x 60, and 120 x 120 for the citadel.

The pipeline follows C:/Users/river/MCP/AGENT_MCP_GUIDE.md:
  1. shapely unions the projected triangles into exact outlines (holes kept: the city's ring)
  2. VectorCraft thickens and unites them, fills them, and for the concept icons makes the
     dark outline as an offset path sent behind. The vector work goes to MCP staging/emblems/.
     The files are raised over the outline so thin parts (the herder's arms, the city's inner
     ring) survive at 60 px.
  3. the 4x PNG is downsampled with premultiplied alpha, so no dark fringe, into MCP
     staging/textures/
  4. scripts/convert_textures.py turns each into an uncompressed B8G8R8A8 DDS with mips,
     matching vanilla's format, in place of its default block compression

Usage:  python docs/tools/build_holding_icons.py <mod root>
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import numpy as np
from PIL import Image
from shapely.geometry import MultiPolygon, Polygon
from shapely.ops import unary_union

VECTORCRAFT = r"C:\Program Files\VectorCraft\vectorcraft-cli.exe"
MCP = "C:/Users/river/MCP"
STAGE_VEC = MCP + "/staging/emblems/eotg_holding"
STAGE_TEX = MCP + "/staging/textures/eotg_holding_icons"
CONVERT = MCP + "/scripts/convert_textures.py"
SILHOUETTES = os.path.join("docs", "art", "marker_emblems", "silhouettes.json")
OVERSAMPLE = 4

# holding type -> engine holding key (church_holding is vanilla's name for the temple)
KEYS = {
    "castle": "castle_holding",
    "city": "city_holding",
    "temple": "church_holding",
    "temple_citadel": "temple_citadel_holding",
    "tribal": "tribal_holding",
    "nomad": "nomad_holding",
    "herder": "herder_holding",
}
# build_marker_assets.py HOLDINGS: the same colour the marker glows in
COLOURS = {
    "castle": "#e2463e",
    "city": "#4288ff",
    "temple": "#f0cc38",
    "temple_citadel": "#fae48a",
}
OUTLINE = "#121722"

# (type, out path, canvas w, h, content box x0 y0 x1 y1, mode, offset in canvas px)
# Vanilla tab icons are chunky; at 0.45 px of offset these looked thin beside them, so the
# outline gains 0.85 px all round. That also keeps the herder's arms above 3 px.
TAB_BOX = (8, 4, 62, 57)
TARGETS = [(t, "gfx/interface/icons/holding_types_tab/%s.dds" % k, 70, 60, TAB_BOX, "tab", 0.85)
           for t, k in KEYS.items()]
TARGETS += [
    ("castle", "gfx/interface/icons/icon_holding_castle.dds", 60, 60, (5, 5, 55, 55), "concept", 1.8),
    ("temple", "gfx/interface/icons/icon_holding_church.dds", 60, 60, (5, 5, 55, 55), "concept", 1.8),
    ("city", "gfx/interface/icons/icon_holding_city.dds", 60, 60, (5, 5, 55, 55), "concept", 1.8),
    ("temple_citadel", "gfx/interface/icons/icon_holding_temple_citadel.dds", 120, 120,
     (10, 10, 110, 110), "concept", 3.6),
]


def outline(tris):
    """The union of every projected triangle: the silhouette as polygons with holes."""
    polys = [Polygon(t) for t in tris]
    polys = [p for p in polys if p.area > 1e-9]
    # A hair of buffer welds triangles that meet along an edge but don't quite share its
    # floats, then comes back off.
    return unary_union(polys).buffer(1e-4, join_style="mitre").buffer(-1e-4, join_style="mitre")


def fit(geom, box, pad):
    """Scale uniformly into `box`, less `pad` on every side, centred; flip y for SVG."""
    x0, y0, x1, y1 = box
    gx0, gy0, gx1, gy1 = geom.bounds
    s = min((x1 - x0 - 2 * pad) / (gx1 - gx0), (y1 - y0 - 2 * pad) / (gy1 - gy0))
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    mx, my = (gx0 + gx1) / 2, (gy0 + gy1) / 2

    def tf(pts):
        return [(cx + (x - mx) * s, cy - (y - my) * s) for x, y in pts]
    return tf


def svg_path(geom, tf):
    parts = []
    polys = geom.geoms if isinstance(geom, MultiPolygon) else [geom]
    for p in polys:
        for ring in [p.exterior] + list(p.interiors):
            pts = tf(list(ring.coords)[:-1])
            parts.append("M" + " L".join("%.3f %.3f" % q for q in pts) + " Z")
    return " ".join(parts)


def vectorcraft(svg_in, png_out, mode, offset, colour):
    steps = [("select.all", None),
             ("object.path.offsetPath", {"offset": offset, "joins": "round"})]
    if mode == "tab":
        steps += [("select.all", None), ("object.pathfinder.unite", None),
                  ("paint.setFill", {"color": "#000000"})]
    else:
        # the offset copy is the dark outline: it comes back selected, above the original
        steps += [("paint.setFill", {"color": OUTLINE}), ("object.arrange.sendToBack", None)]
    cmd = [VECTORCRAFT, "run", "--in", svg_in]
    for cid, params in steps:
        cmd += ["--cmd", cid]
        if params is not None:
            cmd += ["--params", json.dumps(params)]
    cmd += ["--export", png_out, "--scale", str(OVERSAMPLE)]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0 or '"error"' in res.stdout:
        sys.exit("VectorCraft failed on %s:\n%s%s" % (svg_in, res.stdout, res.stderr))


def downsample(png, w, h):
    """Box-filter down with premultiplied alpha, so edges don't pick up a dark fringe."""
    a = np.asarray(Image.open(png).convert("RGBA"), np.float64) / 255.0
    rgb, al = a[..., :3] * a[..., 3:], a[..., 3:]
    f = OVERSAMPLE
    H, W = a.shape[:2]
    if (W, H) != (w * f, h * f):
        sys.exit("%s is %dx%d, expected %dx%d" % (png, W, H, w * f, h * f))
    rgb = rgb.reshape(h, f, w, f, 3).mean((1, 3))
    al = al.reshape(h, f, w, f, 1).mean((1, 3))
    out = np.where(al > 1e-6, rgb / np.maximum(al, 1e-6), 0.0)
    img = np.concatenate([out, al], axis=2)
    return Image.fromarray(np.clip(img * 255.0 + 0.5, 0, 255).astype(np.uint8), "RGBA")


def main():
    mod_root = sys.argv[1] if len(sys.argv) > 1 else "."
    sil = json.load(open(os.path.join(mod_root, SILHOUETTES), encoding="utf-8"))
    os.makedirs(STAGE_VEC, exist_ok=True)
    os.makedirs(STAGE_TEX, exist_ok=True)
    shapes = {k: outline(v) for k, v in sil.items()}

    for holding, rel, w, h, box, mode, off in TARGETS:
        name = os.path.splitext(os.path.basename(rel))[0]
        geom = shapes[holding]
        tf = fit(geom, box, off)
        fill = "#000000" if mode == "tab" else COLOURS[holding]
        svg = os.path.join(STAGE_VEC, name + ".svg")
        with open(svg, "w", encoding="utf-8") as fh:
            fh.write('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
                     'viewBox="0 0 %d %d"><path fill-rule="evenodd" fill="%s" d="%s"/></svg>'
                     % (w, h, w, h, fill, svg_path(geom, tf)))
        big = os.path.join(STAGE_VEC, name + "@4x.png")
        vectorcraft(svg, big, mode, off, fill)
        png = os.path.join(STAGE_TEX, name + ".png")
        downsample(big, w, h).save(png)

        out_dir = os.path.join(mod_root, os.path.dirname(rel))
        os.makedirs(out_dir, exist_ok=True)
        subprocess.run([sys.executable, CONVERT, png, "-o", out_dir, "-f", "B8G8R8A8_UNORM"],
                       check=True, stdout=subprocess.DEVNULL)
        print("  %-28s %dx%d  %s" % (name, w, h, rel))


if __name__ == "__main__":
    main()
