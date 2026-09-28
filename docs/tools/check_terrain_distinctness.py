"""Terrain distinctness check: which terrain pairs will read as the same thing on the map?

Why this exists. Nebula Barrier (mountains) and Nebula Wilds (jungle) shipped looking identical -
they differed on only 2 of 7 axes and shared the two that carry most of the signal. That is not
visible by reading the table, because the thing that matters is *perceptual* distance after the
tint saturation and the colormap wash, not the distance between two hex strings.

This reads TERRAINS straight out of build_terrain_hybrid.py (so it cannot drift), models what
actually reaches the screen, and ranks every pair by collision risk.

What it models
  1. TINT_SATURATION is applied exactly as the generator applies it.
  2. The colormap soft-lights toward neutral, so a swatch that looks distinct washes out in game.
     WASH approximates that. This is the conservative view and it is the operative number.
  3. Colour distance is CIEDE2000, not RGB or CIE76. CIE76 overstates differences between
     saturated colours, which is exactly where it would tell us a real collision is fine.
  4. Secondary axes (stars, structure amount, feature scale, structure texture, modifier) can
     partially rescue a pair whose colours are close, but they cannot fully substitute: at
     terrain minification colour is most of what survives.
  5. Pairs of common terrains matter more than pairs of rare ones, so risk is weighted by
     land area - two 25% terrains colliding is a map-wide problem, two 0.3% ones is not.

Limits. This is a triage heuristic, not ground truth: it cannot see the structure textures, the
lighting, or what a modifier actually draws. Its job is to tell you which pairs to go and look at,
and to fail loudly when a pair is indefensible. The map is the real test.

Usage:  python docs/tools/check_terrain_distinctness.py [--all] [--wash 0.30]
Exit 1 if any pair is CRITICAL.
"""
from __future__ import annotations

import argparse
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "build_terrain_hybrid.py")

# Land area % per terrain, from docs/terrain_scheme.md (measured on the vanilla map). Relative
# weights are what matter; the mod's own map will differ but the shape - a few dominant terrains
# and a long tail - is expected to hold.
AREA = {
    "plains": 24.5, "hills": 6.2, "desert": 4.3, "mountains": 3.9, "taiga": 3.6,
    "drylands": 3.2, "forest": 2.6, "steppe": 2.6, "jungle": 1.6, "desert_mountains": 1.0,
    "wetlands": 0.9, "farmlands": 0.4, "floodplains": 0.4, "oasis": 0.3, "terraced_hills": 0.2,
    # 21.4 makes this the largest single surface on the map, ahead of plains. Measured by
    # build_terrain_index.py, which forces every impassable province into it.
    "impassable": 21.4,
}

# Pairs that are MEANT to share a colour, so a zero distance between them is a decision and
# not a regression. They are still printed, as TWIN, but they do not fail the run.
#
# Only one so far. impassable/desert_mountains were a single material until 2026-09-27 and
# were split because their province sets are disjoint and their star densities had to
# diverge; the split was never intended to change what either one looks like, so every other
# field of the two is identical on purpose. Do NOT add a pair here to silence a collision you
# did not intend - the whole value of this script is that it fails.
INTENDED_TWINS = {frozenset(("desert_mountains", "impassable"))}

# Thresholds on the washed CIEDE2000 distance. Large adjacent fields of flat colour are about the
# easiest case for the eye, but terrain is minified, noisy and lit, which eats the margin.
DE_CRITICAL = 8.0    # below this they are the same colour in practice
DE_WATCH = 14.0      # below this they are distinguishable only if something else differs


def parse_terrains(path: str):
    src = open(path, encoding="utf-8").read()
    block = re.search(r"^TERRAINS = \{(.*?)^\}", src, re.S | re.M)
    if not block:
        sys.exit(f"could not find TERRAINS in {path}")
    sat = re.search(r"^TINT_SATURATION\s*=\s*([\d.]+)", src, re.M)
    rows = {}
    row_re = re.compile(
        r'"(\w+)":\s*\(\s*"([^"]+)",\s*"(#[0-9a-fA-F]{6})",\s*(\d+),\s*(\d+),\s*'
        r'([\d.]+),\s*([\d.]+),\s*([\d.]+),\s*"(\w+)"\s*\)')
    for m in row_re.finditer(block.group(1)):
        rows[m.group(1)] = dict(
            pretty=m.group(2), tint=m.group(3), structure=int(m.group(4)),
            tile=int(m.group(5)), amount=float(m.group(6)),
            star_density=float(m.group(7)), star_bright=float(m.group(8)),
            fx=m.group(9))
    return rows, float(sat.group(1)) if sat else 1.45


def hx(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def apply_saturation(rgb, sat):
    grey = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    return tuple(min(1.0, max(0.0, grey + (c - grey) * sat)) for c in rgb)


def wash(rgb, amount):
    """Approximate the colormap soft-lighting everything toward neutral: keeps lightness,
    pulls chroma in. Conservative, because chroma is what most of these terrains rely on."""
    grey = 0.2126 * rgb[0] + 0.7152 * rgb[1] + 0.0722 * rgb[2]
    return tuple(c + (grey - c) * amount for c in rgb)


def srgb_to_lab(rgb):
    def lin(c):
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b) / 1.0
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883

    def f(t):
        return t ** (1 / 3) if t > 216 / 24389 else (841 / 108) * t + 4 / 29
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def ciede2000(lab1, lab2):
    L1, a1, b1 = lab1
    L2, a2, b2 = lab2
    C1, C2 = math.hypot(a1, b1), math.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - math.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7))) if Cb > 0 else 0.5
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = math.hypot(a1p, b1), math.hypot(a2p, b2)
    h1p = math.degrees(math.atan2(b1, a1p)) % 360 if (a1p or b1) else 0.0
    h2p = math.degrees(math.atan2(b2, a2p)) % 360 if (a2p or b2) else 0.0
    dLp = L2 - L1
    dCp = C2p - C1p
    if C1p * C2p == 0:
        dhp = 0.0
    else:
        dh = h2p - h1p
        dhp = dh - 360 if dh > 180 else (dh + 360 if dh < -180 else dh)
    dHp = 2 * math.sqrt(C1p * C2p) * math.sin(math.radians(dhp) / 2)
    Lbp = (L1 + L2) / 2
    Cbp = (C1p + C2p) / 2
    if C1p * C2p == 0:
        hbp = h1p + h2p
    else:
        s = h1p + h2p
        if abs(h1p - h2p) > 180:
            hbp = (s + 360) / 2 if s < 360 else (s - 360) / 2
        else:
            hbp = s / 2
    T = (1 - 0.17 * math.cos(math.radians(hbp - 30)) + 0.24 * math.cos(math.radians(2 * hbp))
         + 0.32 * math.cos(math.radians(3 * hbp + 6)) - 0.20 * math.cos(math.radians(4 * hbp - 63)))
    dTh = 30 * math.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * math.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7)) if Cbp > 0 else 0.0
    Sl = 1 + (0.015 * (Lbp - 50) ** 2) / math.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -math.sin(math.radians(2 * dTh)) * Rc
    return math.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2
                     + Rt * (dCp / Sc) * (dHp / Sh))


def secondary_separation(a, b):
    """How much non-colour difference there is, 0..1, with the reason. These rescue a close pair
    only partially - at minification, colour carries most of the signal."""
    parts = []
    score = 0.0
    ds = abs(a["star_density"] - b["star_density"])
    if ds >= 0.30:
        score += 0.30 * min(1.0, ds / 0.5)
        parts.append(f"stars {a['star_density']:.2f}/{b['star_density']:.2f}")
    da = abs(a["amount"] - b["amount"])
    if da >= 0.20:
        score += 0.20 * min(1.0, da / 0.5)
        parts.append(f"cloud {a['amount']:.2f}/{b['amount']:.2f}")
    ratio = max(a["tile"], b["tile"]) / min(a["tile"], b["tile"])
    if ratio >= 1.6:
        score += 0.20 * min(1.0, (ratio - 1.6) / 1.4 + 0.4)
        parts.append(f"scale {a['tile']}/{b['tile']} ({ratio:.1f}x)")
    if a["structure"] != b["structure"]:
        score += 0.12
        parts.append(f"tex {a['structure']}/{b['structure']}")
    if a["fx"] != b["fx"] and (a["fx"] != "none" or b["fx"] != "none"):
        score += 0.30
        parts.append(f"fx {a['fx']}/{b['fx']}")
    return min(1.0, score), ", ".join(parts) if parts else "nothing"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all", action="store_true", help="print every pair, not just the risky ones")
    ap.add_argument("--wash", type=float, default=0.30,
                    help="how far the colormap pulls tints toward neutral (0 = none)")
    args = ap.parse_args()

    terrains, sat = parse_terrains(SOURCE)
    print(f"{len(terrains)} terrains from build_terrain_hybrid.py  "
          f"(TINT_SATURATION={sat}, colormap wash={args.wash})\n")

    lab = {}
    for k, t in terrains.items():
        eff = wash(apply_saturation(hx(t["tint"]), sat), args.wash)
        lab[k] = srgb_to_lab(eff)
        t["L"] = lab[k][0]

    names = list(terrains)
    rows = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            de = ciede2000(lab[a], lab[b])
            sec, why = secondary_separation(terrains[a], terrains[b])
            # weight: geometric mean of land share, normalised against the largest possible pair
            w = math.sqrt(AREA.get(a, 0.5) * AREA.get(b, 0.5))
            if frozenset((a, b)) in INTENDED_TWINS:
                verdict = "TWIN"
            elif de < DE_CRITICAL:
                verdict = "CRITICAL" if sec < 0.45 else "WATCH"
            elif de < DE_WATCH:
                verdict = "WATCH" if sec < 0.30 else "ok"
            else:
                verdict = "ok"
            rows.append((verdict, de, sec, w, a, b, why))

    order = {"CRITICAL": 0, "WATCH": 1, "TWIN": 2, "ok": 3}
    rows.sort(key=lambda r: (order[r[0]], -r[3], r[1]))

    hdr = f"{'':9} {'dE00':>6} {'other':>6} {'wt':>5}  pair"
    print(hdr)
    print("-" * 78)
    shown = 0
    for verdict, de, sec, w, a, b, why in rows:
        if verdict == "ok" and not args.all:
            continue
        shown += 1
        print(f"{verdict:9} {de:6.1f} {sec:6.2f} {w:5.1f}  {a} / {b}")
        print(f"{'':9} {terrains[a]['pretty']} vs {terrains[b]['pretty']}  -  separated by: {why}")
    if not shown:
        print("no pairs below the thresholds")

    crit = [r for r in rows if r[0] == "CRITICAL"]
    watch = [r for r in rows if r[0] == "WATCH"]
    twin = [r for r in rows if r[0] == "TWIN"]
    print(f"\n{len(crit)} critical, {len(watch)} watch, {len(twin)} intended twin, "
          f"{len(rows) - len(crit) - len(watch) - len(twin)} ok  (of {len(rows)} pairs)")

    # Per-terrain: the nearest neighbour is what a player actually notices
    print("\nnearest neighbour per terrain:")
    for k in sorted(names, key=lambda n: -AREA.get(n, 0)):
        best = min((r for r in rows if k in (r[4], r[5])), key=lambda r: r[1])
        other = best[5] if best[4] == k else best[4]
        print(f"  {AREA.get(k, 0):5.1f}%  {k:17} closest to {other:17} dE {best[1]:5.1f}  [{best[0]}]")

    return 1 if crit else 0


if __name__ == "__main__":
    sys.exit(main())
