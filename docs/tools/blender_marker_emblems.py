"""Build the seven holding-marker emblems in Blender, one silhouette per holding type.

Reference: the holding representation brief (section 3.1, "Strict budget: exactly 7 meshes") and
docs/marker_model_brief.md, which says what the pipeline accepts. Each emblem floats above the
shared plinth and beam that build_marker_mesh.py makes. The plinth is not modelled here.

    castle          Fortress Shield / Aegis Diamond   a diamond core with angled defensive fins
    city            Gateway Ring                      a segmented halo around an inner ring
    temple          Crystal Spire                     a vertical faceted needle with two shards
    tribal          Crossed Wedges                    two saw-toothed blades crossed, with a chevron
    nomad           Flotilla Arrowhead                a swept delta with two escort deltas
    herder          Tri-Point Satellite Hub           a hub with three arms ending in panels
    temple_citadel  Crowned Spire                     the Sanctum needle inside the Bastion's upper fins

Not holdings, on the low puck instead of the plinth (build_marker_mesh.py SITES):
    feast, hunt, tournament, wedding     activity sites: chalice, reticle, podium, linked rings
    camp                                 adventurer camp: a landed shuttle, side-on
    quarantine, decon, purge             epidemic sites: hub, decontamination grid, orbital purge

And the construction cage (build_cage): a translucent wireframe drawn AROUND the holding's
own marker while something is being built, in world units, exported as eotg_construction.obj.

Design for silhouette. The emblem renders at EOTG_MARKER_EMISSIVE 0.82, which is flat colour. So
these are bold outlines with open gaps and no surface detail. The flat shapes (ring, blades,
deltas, hub) stand in a plane tilted back PLATE_TILT degrees, so they face the map camera, which
looks down from the south. Upright shapes (spire, diamond) stay vertical.

Space. Shapes are written in Blender (Z-up). The OBJ export maps them to the pipeline's Y-up with
forward -Z, as obj_to_pdxmesh expects. Blender +Y is the camera side (south). CK3's world is
left-handed and this export is a plain rotation, so the game shows the MIRROR of a Blender view.
The previews are flipped to match the game. All seven are symmetric or near it, so this matters
only for the previews.

Envelope (marker brief, "Size"; source units, before build_marker_mesh's x1.44):
width <= 1.15, height <= 1.75, radius from the Y axis <= 0.57, centred on X and Z. Every limit
is checked, as are triangles (<= 1500 target, 2000 hard), closed parts, and normals that agree
with the winding.

Pipeline (C:/Users/river/MCP/AGENT_MCP_GUIDE.md, recipe A), used when that workspace is present:
uv_helpers.unwrap_and_export_uv writes the UVs (layout SVG to MCP staging/uv/marker_emblems/),
and export_helpers.export_lod_chain writes LOD0-2 FBX to MCP staging/exports/marker_emblems/.
The texture steps don't apply, because the brief rules out detailed textures and the diffuse is a
flat colour made by build_marker_assets.py.

Outputs:
    gfx/models/buildings/eotg_markers/eotg_marker_<type>.obj   the deliverable (marker brief)
    docs/art/marker_emblems/eotg_marker_emblems.blend          the source scene
    docs/art/marker_emblems/previews/*.png                     review renders (do_render)
    docs/art/marker_emblems/manifest.json                      stats and every check's result
    docs/art/marker_emblems/silhouettes.json                   front-view outlines for the 2D icons

Usage:
    live      python docs/tools/blender_mcp_exec.py docs/tools/blender_marker_emblems.py \
                  --call "build(r'<mod root>', do_render=True)"
    headless  blender -b --factory-startup --python docs/tools/blender_marker_emblems.py -- <mod root> [--render]
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

MCP_ROOT = "C:/Users/river/MCP"
REL_GFX = os.path.join("gfx", "models", "buildings", "eotg_markers")
REL_ART = os.path.join("docs", "art", "marker_emblems")

# The site puck and glyph placement, as build_marker_mesh.py SITES builds them (previews only)
SITE_PEDESTAL_SCALE = 1.30
SITE_EMBLEM_SCALE = 1.20
SITE_HOVER = 0.22

# marker brief limits, source units
MAX_WIDTH = 1.15
MAX_HEIGHT = 1.75
MAX_RADIUS = 0.57
CENTRE_TOL = 0.03
TRIS_TARGET = 1500
TRIS_HARD = 2000

# The marker the construction cage must enclose (build_marker_mesh.py output)
PLINTH_FOOT_R = 2.04
MARKER_TOP = 5.38

PLATE_TILT = 20.0       # degrees the flat emblems lean back to face the map camera. 30 read
                        # better head-on but pushed tribal, nomad and herder past the 0.57 radius

# The plinth and placement, exactly as build_marker_mesh.py builds them. Used only for previews.
PEDESTAL_SCALE = 2.04
EMBLEM_SCALE = 1.44
HOVER = 0.336

# Colours from build_marker_assets.py HOLDINGS (the in-game diffuse is this flat colour).
COLOURS = {
    "castle":         (226,  70,  62),
    "city":           ( 66, 136, 255),
    "temple":         (240, 204,  56),
    "temple_citadel": (250, 228, 138),
    "tribal":         ( 85, 185, 107),
    "nomad":          (167, 124, 255),
    "herder":         (238, 232, 246),
    # sites, not holdings: one cool cyan for the gatherings and the camp, magenta for hazards
    "feast":          (110, 225, 240),
    "hunt":           (110, 225, 240),
    "tournament":     (110, 225, 240),
    "wedding":        (110, 225, 240),
    "camp":           (110, 225, 240),
    "quarantine":     (236,  72, 196),
    "decon":          (236,  72, 196),
    "purge":          (236,  72, 196),
}
CONSTRUCTION = (255, 162, 48)       # amber, which no holding uses
HOLDING_ORDER = ["castle", "city", "temple", "temple_citadel", "tribal", "nomad", "herder"]
SITE_ORDER = ["feast", "hunt", "tournament", "wedding", "camp", "quarantine", "decon", "purge"]
ORDER = HOLDING_ORDER + SITE_ORDER


# ---------------------------------------------------------------- primitives

def T(x=0.0, y=0.0, z=0.0):
    return Matrix.Translation((x, y, z))


def R(deg, axis):
    return Matrix.Rotation(math.radians(deg), 4, axis)


def S(x, y=None, z=None):
    return Matrix.Diagonal((x, x if y is None else y, x if z is None else z, 1.0))


FACE = R(PLATE_TILT, "X")   # a plate authored in the XZ plane, leaned back toward north


def _xf(bm, verts, mat):
    bmesh.ops.transform(bm, matrix=mat, verts=list(verts))


def lathe(bm, profile, segs, mat=Matrix(), phase=0.0):
    """Revolve a (r, z) profile around Z. r == 0 points become single poles, so a profile that
    starts and ends on the axis is a closed solid."""
    rows = []
    for r, z in profile:
        if r <= 1e-9:
            rows.append([bm.verts.new((0.0, 0.0, z))])
        else:
            rows.append([bm.verts.new((r * math.cos(phase + 2 * math.pi * i / segs),
                                       r * math.sin(phase + 2 * math.pi * i / segs), z))
                         for i in range(segs)])
    for a, b in zip(rows, rows[1:]):
        for i in range(segs):
            j = (i + 1) % segs
            if len(a) == 1 and len(b) == 1:
                break
            if len(a) == 1:
                bm.faces.new((a[0], b[i], b[j]))
            elif len(b) == 1:
                bm.faces.new((a[i], b[0], a[j]))
            else:
                bm.faces.new((a[i], b[i], b[j], a[j]))
    if len(rows[0]) > 1:
        bm.faces.new(list(reversed(rows[0])))
    if len(rows[-1]) > 1:
        bm.faces.new(rows[-1])
    _xf(bm, [v for row in rows for v in row], mat)


def plate(bm, pts, thick, mat=Matrix()):
    """A flat prism: polygon `pts` (x, z) in the XZ plane, `thick` deep along Y, centred on y=0.
    Concave outlines are fine; the OBJ export triangulates them."""
    front = [bm.verts.new((x, -thick / 2, z)) for x, z in pts]
    back = [bm.verts.new((x, thick / 2, z)) for x, z in pts]
    n = len(pts)
    bm.faces.new(front)
    bm.faces.new(list(reversed(back)))
    for i in range(n):
        j = (i + 1) % n
        bm.faces.new((front[i], back[i], back[j], front[j]))
    _xf(bm, front + back, mat)


def torus_arc(bm, R0, r, a0, a1, segs, sides, mat=Matrix()):
    """A piece of torus in the XZ plane from angle a0 to a1 (degrees), capped at both ends.
    a0 == a1 - 360 gives a full ring with no caps."""
    full = abs((a1 - a0) - 360.0) < 1e-6
    n = segs if full else segs + 1
    rings = []
    for i in range(n):
        a = math.radians(a0 + (a1 - a0) * i / segs)
        c = Vector((R0 * math.cos(a), 0.0, R0 * math.sin(a)))
        radial = Vector((math.cos(a), 0.0, math.sin(a)))
        ring = []
        for k in range(sides):
            b = 2 * math.pi * k / sides
            p = c + radial * (r * math.cos(b)) + Vector((0, r * math.sin(b), 0))
            ring.append(bm.verts.new(p))
        rings.append(ring)
    for i in range(n if full else n - 1):
        p, q = rings[i], rings[(i + 1) % n]
        for k in range(sides):
            m = (k + 1) % sides
            bm.faces.new((p[k], p[m], q[m], q[k]))
    if not full:
        bm.faces.new(rings[0])
        bm.faces.new(list(reversed(rings[-1])))
    _xf(bm, [v for ring in rings for v in ring], mat)


def box(bm, size, mat=Matrix()):
    res = bmesh.ops.create_cube(bm, size=1.0, matrix=mat @ S(*size), calc_uvs=False)
    return res["verts"]


def ico(bm, radius, mat=Matrix(), subdiv=2):
    bmesh.ops.create_icosphere(bm, subdivisions=subdiv, radius=radius, matrix=mat,
                               calc_uvs=False)


def mirror_x(pts):
    return [(-x, z) for x, z in reversed(pts)]


# ---------------------------------------------------------------- the seven emblems

def spire(bm, h, r, mat=Matrix(), segs=6):
    """The faceted needle shared by temple and temple_citadel."""
    lathe(bm, [(0.0, 0.0), (r * 0.80, h * 0.14), (r, h * 0.32), (r * 0.62, h * 0.80),
               (0.0, h)], segs, mat, phase=math.pi / segs)


def fins(bm, upper=True, lower=True, spread=1.0):
    """The Bastion's angled defensive fins, one pair per tier, swept up and out."""
    # The inner edge stands clear of whatever is in the middle. Touching, the fins and the core
    # merged into one flat-coloured mass and the whole emblem read as a crown.
    if upper:
        u = [(0.33, 0.76), (0.56 * spread, 1.02), (0.56 * spread, 1.46), (0.36, 1.12)]
        plate(bm, u, 0.07)
        plate(bm, mirror_x(u), 0.07)
    if lower:
        lo = [(0.31, 0.26), (0.54 * spread, 0.36), (0.54 * spread, 0.74), (0.33, 0.58)]
        plate(bm, lo, 0.07)
        plate(bm, mirror_x(lo), 0.07)


def em_castle(bm):
    # The Aegis Diamond: a square bipyramid turned so an edge faces the camera, which shows a
    # crisp rhombus outline, flanked by two tiers of fins that make it read as a shield crest.
    lathe(bm, [(0.0, 0.0), (0.24, 0.80), (0.0, 1.70)], 4, phase=0.0)
    fins(bm)


def em_city(bm):
    # The Gateway Ring: an outer halo broken into eight segments, a thin unbroken inner ring, and
    # nothing in the middle, because the open centre IS the read. Leaned back to face the camera.
    c = T(0, 0, 0.56) @ FACE
    seg, gap = 45.0, 9.0
    for i in range(8):
        a0 = 90 + i * seg + gap / 2
        torus_arc(bm, 0.47, 0.075, a0, a0 + seg - gap, 6, 6, c)
    torus_arc(bm, 0.29, 0.032, 0, 360, 32, 5, c)
    # four short spokes tie the rings together at the cardinal points, so the inner ring is
    # not left floating
    for a in (0, 90, 180, 270):
        m = c @ R(-a, "Y") @ T(0.38, 0, 0)
        box(bm, (0.13, 0.04, 0.04), m)


def em_temple(bm):
    # The Crystal Spire: one tall faceted needle with two short shards leaning off its base.
    # Narrow on purpose; it is the only tall-and-thin emblem without fins.
    spire(bm, 1.74, 0.17)
    for sx in (-1, 1):
        spire(bm, 0.78, 0.10, T(sx * 0.21, 0, 0.0) @ R(sx * 16, "Y"))


def em_temple_citadel(bm):
    # The Crowned Spire: the Sanctum needle standing inside the Bastion's upper fins. Fins say
    # "fortified", the needle says "temple", and the fins rising to the needle's shoulders are
    # the crown. Two things were tried and dropped. A ring of crown points fused with the
    # needle's base into a blob in flat colour. With BOTH fin tiers it became a castle with a
    # thinner core, and at icon size the two could not be told apart.
    spire(bm, 1.74, 0.16)
    fins(bm, upper=True, lower=False)


def em_tribal(bm):
    # The Crossed Wedges: two broad blades crossed in an X, each tapering to a point with a saw
    # edge, over a chevron. Aggressive and spiky; the only emblem whose outline is all angles.
    def blade(sign):
        L, w = 1.70, 0.17
        # authored along +Z from the origin, then rotated into the X
        pts = [(-w / 2, 0.0), (w / 2, 0.0)]
        # The saw edge bows outward slightly. Dead straight, the tooth roots were collinear, and
        # the OBJ triangulator joined three of them into zero-area triangles that fail the
        # winding check.
        def edge(z):
            return w / 2 + 0.03 * math.sin(math.pi * z / L)
        teeth = 3
        for t in range(teeth):
            z0 = 0.30 + t * 0.34
            pts += [(edge(z0), z0), (edge(z0) + 0.14, z0 + 0.06), (edge(z0 + 0.22), z0 + 0.22)]
        pts += [(w / 2 * 0.6, L * 0.86), (0.0, L), (-w / 2, L * 0.80)]
        plate(bm, pts, 0.08, T(0, 0, 0.28) @ FACE @ R(sign * 28, "Y") @ T(0, 0, -0.80))
    blade(1)
    blade(-1)
    chev = [(0.0, 0.00), (0.40, 0.30), (0.40, 0.44), (0.0, 0.18), (-0.40, 0.44), (-0.40, 0.30)]
    plate(bm, chev, 0.08, T(0, 0, 0.0) @ FACE)


def em_nomad(bm):
    # The Flotilla Arrowhead: a swept delta pointing up, notched trailing edge, with two small
    # escort deltas off its wings. The only emblem that points, so it reads as moving.
    delta = [(0.0, 1.66), (0.34, 0.50), (0.12, 0.68), (0.0, 0.54), (-0.12, 0.68), (-0.34, 0.50)]
    plate(bm, delta, 0.09, FACE)
    # a raised keel so it has a body from the side
    plate(bm, [(0.0, 1.40), (0.05, 0.66), (0.0, 0.58), (-0.05, 0.66)], 0.14, FACE)
    # the escorts fly BELOW the wingtips with clear space between; level with them, they fused
    # into the wings and read as feet
    esc = [(0.0, 0.46), (0.12, 0.06), (0.04, 0.13), (0.0, 0.09), (-0.04, 0.13), (-0.12, 0.06)]
    for sx in (-1, 1):
        plate(bm, [(x + sx * 0.33, z - 0.06) for x, z in esc], 0.08, FACE)


def em_herder(bm):
    # The Tri-Point Satellite Hub: a hub with three arms at 120 degrees, each ending in a square
    # harvester panel turned to a diamond. A Y with weights on it; reads as dispersed, not armed.
    centre = T(0, 0, 0.80) @ FACE
    ico(bm, 0.15, centre, subdiv=2)
    torus_arc(bm, 0.22, 0.025, 0, 360, 24, 5, centre)
    for a in (90, 210, 330):
        arm = centre @ R(-a, "Y")
        box(bm, (0.26, 0.05, 0.05), arm @ T(0.27, 0, 0))
        plate(bm, [(0.0, -0.12), (0.12, 0.0), (0.0, 0.12), (-0.12, 0.0)], 0.05,
              arm @ T(0.46, 0, 0) @ R(a, "Y"))


def strut(bm, p0, p1, w):
    """A square-section bar from p0 to p1: one member of a lattice.

    It overruns each end by 0.49 w, not 0.5 w. At exactly half a width, the corners of struts
    meeting at a joint coincide, the weld merges them, and the joint stops being closed."""
    a, b = Vector(p0), Vector(p1)
    d = b - a
    rot = d.to_track_quat("Z", "Y").to_matrix().to_4x4()
    box(bm, (w, w, d.length + 0.98 * w), T(*((a + b) / 2)) @ rot)


# ---------------------------------------------------------------- construction cage
#
# Not an emblem. The engine draws the `construction` entity at the HOLDING'S OWN locator,
# around whatever holding model stands there: vanilla's scaffold is a cage centred on the
# origin, about 4.7 x 6.3 x 5.0, which encloses a castle (2.77 x 4.16 x 2.17). So this is a
# translucent wireframe cage around the marker (plinth 4.08 wide, marker up to 5.38 tall),
# authored in WORLD units with no plinth of its own. A first version put a second plinth and
# emblem there, which would have collided with the holding's own marker.
#
# Half built: the lower rings are closed, the top ring is only part-way round, and two uprights
# stop short. It is drawn on the beam's blending effect, so it reads as projected light.

CAGE_R = 2.30          # clear of the plinth's foot (2.04)
CAGE_H = 5.80          # clear of the tallest marker (5.38)
CAGE_W = 0.045         # strut width: thin, so it reads as a wireframe and not a scaffold


def build_cage(bm):
    n = 8
    pts = [(CAGE_R * math.cos(2 * math.pi * (k + 0.5) / n),
            CAGE_R * math.sin(2 * math.pi * (k + 0.5) / n)) for k in range(n)]
    rings = (0.06, 1.95, 3.85, CAGE_H)
    short = {2, 5}                         # uprights not yet run to the top
    for k, (x, y) in enumerate(pts):
        strut(bm, (x, y, rings[0]), (x, y, rings[2] if k in short else rings[3]), CAGE_W)
    for z in rings[:3]:
        for k in range(n):
            (x0, y0), (x1, y1) = pts[k], pts[(k + 1) % n]
            strut(bm, (x0, y0, z), (x1, y1, z), CAGE_W)
    # the top ring, only part-way round: the segments whose both uprights reach the top
    for k in range(n):
        if k in short or (k + 1) % n in short:
            continue
        (x0, y0), (x1, y1) = pts[k], pts[(k + 1) % n]
        strut(bm, (x0, y0, rings[3]), (x1, y1, rings[3]), CAGE_W)
    # diagonal bracing on alternate bays of the middle tier
    for k in range(0, n, 2):
        (x0, y0), (x1, y1) = pts[k], pts[(k + 1) % n]
        strut(bm, (x0, y0, rings[1]), (x1, y1, rings[2]), CAGE_W * 0.8)


# ---------------------------------------------------------------- holy-site landmark
#
# The Precursor Monolith, a placeholder for every holy site's landmark (owner, 2026-10-20: "so
# we can revisit this later"). It stands at the SPECIAL-BUILDING locator, beside the holding,
# with no plinth: a dark tapered slab with glowing seams, a tilted halo and three shards
# orbiting it. World units. Vanilla's generic cathedral there is about 11 x 6 x 6; this is
# kept slimmer and taller, so it reads as one object and not as a second holding.
#   body  slot 0, dark metal, lit normally (mask 0)
#   glow  slot 1, the seams, halo and shards (mask 1)

MONOLITH_GLOW = (150, 240, 220)      # pale teal: no holding or site uses it
MONOLITH_BODY = (72, 78, 94)        # dark, but a step above the map so its outline holds


def build_monolith_body(bm):
    lathe(bm, [(0.0, 0.0), (0.92, 0.0), (0.92, 0.22), (0.70, 0.40), (0.60, 4.70),
               (0.34, 5.30), (0.0, 5.42)], 4, S(1.0, 0.42, 1.0), phase=math.pi / 4)


def build_monolith_glow(bm):
    # seams: two vertical lines up the front and back faces, and a band near the top
    for sy in (-1, 1):
        for x in (-0.20, 0.20):
            box(bm, (0.05, 0.04, 3.6), T(x, sy * 0.265, 2.55))
        box(bm, (0.62, 0.04, 0.06), T(0, sy * 0.25, 4.45))
    # the halo, tilted, clear of the slab
    torus_arc(bm, 1.30, 0.05, 0, 360, 40, 6, T(0, 0, 3.2) @ R(90, "X") @ R(14, "X") @ R(8, "Y"))
    # three shards orbiting at different heights
    for a, z in ((30, 2.2), (150, 3.0), (270, 3.8)):
        lathe(bm, [(0.0, -0.20), (0.11, 0.0), (0.0, 0.20)], 4,
              T(*(Vector((math.cos(math.radians(a)), math.sin(math.radians(a)), 0)) * 1.62))
              @ T(0, 0, z) @ R(25, "Y"))


# ---------------------------------------------------------------- site glyphs
#
# Not holdings: activity sites, the adventurer camp and epidemic sites. They stand on the low
# puck (build_marker_mesh.py SITES), not the holding plinth, and are kept clear of every
# holding silhouette: no X (tribal), no up-pointing arrow (nomad), no tall spire.

def em_feast(bm):
    # A chalice: universal for a banquet, and round from every side.
    lathe(bm, [(0.0, 0.0), (0.30, 0.0), (0.30, 0.06), (0.10, 0.14), (0.06, 0.30),
               (0.06, 0.62), (0.16, 0.70), (0.36, 0.86), (0.44, 1.12), (0.47, 1.30),
               (0.40, 1.30), (0.34, 1.10), (0.20, 0.90), (0.0, 0.84)], 16)


def em_hunt(bm):
    # A targeting reticle: ring, four ticks pointing in, a centre pip. Faces the camera.
    c = T(0, 0, 0.58) @ FACE
    torus_arc(bm, 0.44, 0.06, 0, 360, 32, 6, c)
    for a in (0, 90, 180, 270):
        box(bm, (0.26, 0.07, 0.07), c @ R(-a, "Y") @ T(0.40, 0, 0))
    ico(bm, 0.09, c, subdiv=2)


def em_tournament(bm):
    # A victory podium, 2-1-3, with a star over first place.
    for x, h in ((-0.34, 0.42), (0.0, 0.64), (0.34, 0.28)):
        box(bm, (0.32, 0.36, h), T(x, 0, h / 2))
    star = []
    for k in range(10):
        r = 0.26 if k % 2 == 0 else 0.11
        a = math.pi / 2 + k * math.pi / 5
        star.append((r * math.cos(a), r * math.sin(a)))
    plate(bm, star, 0.08, T(0, 0, 1.0) @ FACE)


def em_wedding(bm):
    # Two interlocked rings, one turned slightly through the other so they read as linked.
    c = T(0, 0, 0.55) @ FACE
    torus_arc(bm, 0.30, 0.055, 0, 360, 32, 6, c @ T(-0.17, 0, 0) @ R(12, "Z"))
    torus_arc(bm, 0.30, 0.055, 0, 360, 32, 6, c @ T(0.17, 0, 0) @ R(-12, "Z"))


def em_camp(bm):
    # The Expeditionary Shuttle, landed: a capsule fuselage lying east-west so the camera sees
    # it side-on, swept wings, a tail fin and three landing legs. Horizontal on purpose: the
    # nomad emblem is an arrow pointing UP, and the hunt is a reticle.
    body = T(0, 0, 0.42) @ R(90, "Y")             # lathe axis Z turned to point along +X
    lathe(bm, [(0.0, -0.56), (0.10, -0.52), (0.17, -0.36), (0.18, 0.20), (0.14, 0.42),
               (0.0, 0.56)], 10, body)
    # wings: a delta each side, flat, slightly swept back toward -x (the tail)
    for sy in (-1, 1):
        box(bm, (0.34, 0.30, 0.035), T(-0.10, sy * 0.26, 0.38) @ R(sy * -8, "X"))
    # tail fin
    plate(bm, [(-0.50, 0.0), (-0.30, 0.0), (-0.44, 0.26), (-0.54, 0.26)], 0.04,
          T(0, 0, 0.52))
    # landing legs with foot pads
    for x, y in ((0.30, 0.0), (-0.28, 0.20), (-0.28, -0.20)):
        strut(bm, (x * 0.8, y * 0.6, 0.30), (x, y, 0.04), 0.035)
        box(bm, (0.10, 0.10, 0.03), T(x, y, 0.02))


def em_quarantine(bm):
    # Quarantine Hub (epidemic, major): a sealed dome inside a broken hazard ring of three
    # arcs. Replaces the mass-burial site.
    lathe(bm, [(0.0, 0.0), (0.30, 0.0), (0.30, 0.08), (0.27, 0.22), (0.18, 0.38),
               (0.0, 0.44)], 16)
    for k in range(3):
        a0 = 90 + k * 120 + 14
        torus_arc(bm, 0.47, 0.05, a0, a0 + 92, 10, 6, T(0, 0, 0.60) @ FACE)
    lathe(bm, [(0.0, 0.44), (0.03, 0.44), (0.03, 1.02), (0.0, 1.06)], 6)
    ico(bm, 0.08, T(0, 0, 1.10), subdiv=2)


def em_decon(bm):
    # Decontamination Grid (epidemic, recovery): a lattice panel with a medical cross standing
    # proud of it. Replaces the healers' camp.
    c = T(0, 0, 0.56) @ FACE
    n, half = 4, 0.42
    for k in range(n + 1):
        t = -half + 2 * half * k / n
        box(bm, (0.035, 0.04, 2 * half + 0.035), c @ T(t, 0, 0))
        # a hair shorter than the uprights, so bar corners never coincide and weld open
        box(bm, (2 * half + 0.031, 0.04, 0.035), c @ T(0, 0, t))
    cross = [(-0.09, -0.30), (0.09, -0.30), (0.09, -0.09), (0.30, -0.09), (0.30, 0.09),
             (0.09, 0.09), (0.09, 0.30), (-0.09, 0.30), (-0.09, 0.09), (-0.30, 0.09),
             (-0.30, -0.09), (-0.09, -0.09)]
    plate(bm, cross, 0.10, c @ T(0, 0.06, 0))


def em_purge(bm):
    # Orbital Purge (epidemic, apocalyptic): a beam stabbing down from a firing ring into an
    # impact ring on the ground. Replaces the pyre.
    lathe(bm, [(0.0, 0.08), (0.05, 0.10), (0.11, 1.30), (0.0, 1.30)], 10)
    torus_arc(bm, 0.22, 0.04, 0, 360, 24, 5, T(0, 0, 1.34) @ R(90, "X"))
    # the impact ring: a square-section torus squashed flat, lying on the ground
    torus_arc(bm, 0.33, 0.17, 0, 360, 32, 4, T(0, 0, 0.03) @ S(1, 1, 0.16) @ R(90, "X"))
    lathe(bm, [(0.0, 0.0), (0.10, 0.0), (0.10, 0.04), (0.0, 0.04)], 12)
    for a in range(0, 360, 60):
        m = R(a, "Z") @ T(0.30, 0, 0.0)
        lathe(bm, [(0.0, 0.0), (0.05, 0.0), (0.0, 0.26)], 4, m @ R(32, "Y"))


EMBLEMS = {
    "feast": em_feast,
    "hunt": em_hunt,
    "tournament": em_tournament,
    "wedding": em_wedding,
    "camp": em_camp,
    "quarantine": em_quarantine,
    "decon": em_decon,
    "purge": em_purge,
    "castle": em_castle,
    "city": em_city,
    "temple": em_temple,
    "temple_citadel": em_temple_citadel,
    "tribal": em_tribal,
    "nomad": em_nomad,
    "herder": em_herder,
}


# ---------------------------------------------------------------- objects

def srgb(rgb):
    def lin(c):
        c /= 255.0
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return tuple(lin(c) for c in rgb)


def emissive(name, rgb, strength=1.6):
    """Flat colour, no lighting: what EOTG_MARKER_EMISSIVE leaves of the emblem in game."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*srgb(rgb), 1.0)
    em.inputs["Strength"].default_value = strength
    nt.links.new(em.outputs[0], out.inputs[0])
    return m


def hologram(name, rgb, alpha=0.40, strength=1.6):
    """Emissive and see-through: the construction cage as the beam's blending effect draws it
    (texture alpha x a view fade x 0.45 gain in game, so it never reads as solid)."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    em = nt.nodes.new("ShaderNodeEmission")
    em.inputs["Color"].default_value = (*srgb(rgb), 1.0)
    em.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    mix.inputs[0].default_value = alpha
    nt.links.new(tr.outputs[0], mix.inputs[1])
    nt.links.new(em.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    return m


def lit(name, rgb, rough=0.85):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    p = m.node_tree.nodes.get("Principled BSDF")
    p.inputs["Base Color"].default_value = (*srgb(rgb), 1.0)
    p.inputs["Roughness"].default_value = rough
    return m


def make_object(name, build, mat, coll, normalise=True):
    bm = bmesh.new()
    build(bm)
    bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=1e-6)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    non_manifold = sum(1 for e in bm.edges if not e.is_manifold)
    # Normalise to the brief's origin: centred on X and Y (Blender's ground plane), base at 0.
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    if normalise:
        shift = Vector((-(min(xs) + max(xs)) / 2, -(min(ys) + max(ys)) / 2, -min(zs)))
        bmesh.ops.translate(bm, vec=shift, verts=list(bm.verts))
    for f in bm.faces:
        f.smooth = True
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    me.uv_layers.new(name="UVMap")
    ob = bpy.data.objects.new(name, me)
    ob.data.materials.append(mat)
    # hard edges stay hard; flat emissive hides shading anyway, but the rim term reads normals
    mod = ob.modifiers.new("split", "EDGE_SPLIT")
    mod.split_angle = math.radians(35)
    coll.objects.link(ob)
    ob["non_manifold_edges"] = non_manifold
    return ob


def tri_count(ob):
    return sum(len(p.vertices) - 2 for p in ob.data.polygons)


def envelope(ob):
    xs = [v.co.x for v in ob.data.vertices]
    ys = [v.co.y for v in ob.data.vertices]
    zs = [v.co.z for v in ob.data.vertices]
    return dict(width_x=max(xs) - min(xs), depth=max(ys) - min(ys), height=max(zs) - min(zs),
                radius=max(math.hypot(x, y) for x, y in zip(xs, ys)),
                centre=((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))


# ---------------------------------------------------------------- scene

REF = None


def reset_scene():
    """Clear the scene without read_factory_settings, which in a live Blender would unload the
    MCP addon whose socket is running this code."""
    global REF
    for ob in list(bpy.data.objects):
        bpy.data.objects.remove(ob, do_unlink=True)
    for coll in list(bpy.data.collections):
        bpy.data.collections.remove(coll)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.cameras, bpy.data.lights,
                  bpy.data.worlds, bpy.data.images):
        for d in list(block):
            if d.users == 0:
                block.remove(d)
    REF = bpy.data.collections.new("reference (not exported)")
    bpy.context.scene.collection.children.link(REF)


def plinth_material(mod_root, key, diffuse=None, properties="eotg_marker_plinth_properties.dds"):
    """The plinth as the game draws it, roughly: the type's plinth diffuse lit normally, plus the
    same diffuse as emission where the properties mask is set (EOTG_MARKER: Properties.r gates
    the flat emissive). Read straight from the DDS files build_marker_assets.py writes."""
    d = os.path.join(mod_root, REL_GFX)
    m = bpy.data.materials.new("plinth_" + key)
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    bsdf.inputs["Roughness"].default_value = 0.55
    bsdf.inputs["Metallic"].default_value = 0.5
    diff = nt.nodes.new("ShaderNodeTexImage")
    diff.image = bpy.data.images.load(
        os.path.join(d, diffuse or "eotg_marker_%s_plinth_diffuse.dds" % key), check_existing=True)
    props = nt.nodes.new("ShaderNodeTexImage")
    props.image = bpy.data.images.load(os.path.join(d, properties), check_existing=True)
    props.image.colorspace_settings.name = "Non-Color"
    sep = nt.nodes.new("ShaderNodeSeparateColor")
    gain = nt.nodes.new("ShaderNodeMath")
    gain.operation = "MULTIPLY"
    gain.inputs[1].default_value = 1.6
    nt.links.new(diff.outputs["Color"], bsdf.inputs["Base Color"])
    nt.links.new(diff.outputs["Color"], bsdf.inputs["Emission Color"])
    nt.links.new(props.outputs["Color"], sep.inputs[0])
    nt.links.new(sep.outputs[0], gain.inputs[0])
    nt.links.new(gain.outputs[0], bsdf.inputs["Emission Strength"])
    return m


def pedestal(mod_root, profile="chess", scale=PEDESTAL_SCALE, name="ref_pedestal"):
    """The shared plinth (or the sites' puck), regenerated as build_marker_mesh.py does, for
    previews only."""
    tmp = os.path.join(os.environ.get("TEMP", "."), "eotg_ref_%s.obj" % profile)
    subprocess.run([sys.executable, os.path.join(mod_root, "docs", "tools", "make_marker_obj.py"),
                    profile, tmp], check=True, stdout=subprocess.DEVNULL)
    bpy.ops.wm.obj_import(filepath=tmp, forward_axis="NEGATIVE_Z", up_axis="Y")
    ped = bpy.context.selected_objects[0]
    ped.name = name
    ped.data.transform(S(scale))
    ped.data.materials.clear()
    ped.data.materials.append(lit("ref_stone", (120, 116, 110)))
    for c in ped.users_collection:
        c.objects.unlink(ped)
    REF.objects.link(ped)
    return ped, max(v.co.z for v in ped.data.vertices)


def mcp_helpers():
    path = os.path.join(MCP_ROOT, "scripts", "blender")
    if not os.path.isdir(path):
        return None
    if path not in sys.path:
        sys.path.append(path)
    import importlib
    import export_helpers
    import uv_helpers
    importlib.reload(export_helpers)
    importlib.reload(uv_helpers)
    return uv_helpers, export_helpers


def camera(name, loc, target, ortho=None, lens=50):
    cam = bpy.data.objects.new(name, bpy.data.cameras.new(name))
    REF.objects.link(cam)
    cam.location = loc
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    if ortho:
        cam.data.type = "ORTHO"
        cam.data.ortho_scale = ortho
    else:
        cam.data.lens = lens
    return cam


def view_south(target, dist, pitch):
    p = math.radians(pitch)
    return (target[0], target[1] + dist * math.cos(p), target[2] + dist * math.sin(p))


def render(path, cam, res):
    sc = bpy.context.scene
    sc.camera = cam
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.resolution_percentage = 100
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    # mirror left-right so the preview shows what the game shows (module docstring)
    import numpy as np
    img = bpy.data.images.load(path, check_existing=False)
    w, h = img.size
    px = np.empty(w * h * 4, np.float32)
    img.pixels.foreach_get(px)
    img.pixels.foreach_set(px.reshape(h, w, 4)[:, ::-1, :].ravel())
    img.save()
    bpy.data.images.remove(img)


def setup_render():
    sc = bpy.context.scene
    for eng in ("BLENDER_EEVEE", "BLENDER_EEVEE_NEXT"):
        try:
            sc.render.engine = eng
            break
        except TypeError:
            continue
    world = bpy.data.worlds.new("eotg_space")
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.004, 0.006, 0.012, 1)
    sc.world = world
    sc.view_settings.view_transform = "Standard"
    sun = bpy.data.objects.new("ref_sun", bpy.data.lights.new("ref_sun", "SUN"))
    sun.data.energy = 3.0
    sun.rotation_euler = (math.radians(35), 0, math.radians(200))
    REF.objects.link(sun)
    me = bpy.data.meshes.new("ref_ground")
    bm = bmesh.new()
    box(bm, (600, 600, 0.01), T(0, 0, -0.006))
    bm.to_mesh(me)
    bm.free()
    ground = bpy.data.objects.new("ref_ground", me)
    ground.data.materials.append(lit("ref_ground", (14, 18, 34), 0.95))
    REF.objects.link(ground)
    return ground


# ---------------------------------------------------------------- build

def build(mod_root, do_render=False, lods=True):
    gfx_dir = os.path.join(mod_root, REL_GFX)
    art_dir = os.path.join(mod_root, REL_ART)
    prev_dir = os.path.join(art_dir, "previews")
    os.makedirs(prev_dir, exist_ok=True)

    reset_scene()
    coll = bpy.data.collections.new("emblems")
    bpy.context.scene.collection.children.link(coll)

    objs = {}
    for key in ORDER:
        objs[key] = make_object("eotg_marker_" + key, EMBLEMS[key],
                                emissive("em_" + key, COLOURS[key]), coll)
    cage = make_object("eotg_construction", build_cage, hologram("em_construction", CONSTRUCTION),
                       coll)
    mono = [make_object("eotg_precursor_monolith__body", build_monolith_body,
                        lit("em_monolith_body", MONOLITH_BODY, 0.5), coll, normalise=False),
            make_object("eotg_precursor_monolith__glow", build_monolith_glow,
                        emissive("em_monolith_glow", MONOLITH_GLOW), coll, normalise=False)]
    bpy.context.view_layer.update()

    report = dict(reference="holding representation brief s3.1 + docs/marker_model_brief.md",
                  models={})
    failures = []
    for key, ob in objs.items():
        env = envelope(ob)
        tris = tri_count(ob)
        checks = {}

        def check(label, ok, detail):
            checks[label] = dict(ok=bool(ok), detail=detail)
            if not ok:
                failures.append("%s: %s (%s)" % (key, label, detail))
        check("closed", ob["non_manifold_edges"] == 0, int(ob["non_manifold_edges"]))
        check("tris", tris <= TRIS_TARGET, "%d (target %d, hard %d)" % (tris, TRIS_TARGET,
                                                                      TRIS_HARD))
        check("width", max(env["width_x"], env["depth"]) <= MAX_WIDTH,
              "%.3f x %.3f" % (env["width_x"], env["depth"]))
        check("height", env["height"] <= MAX_HEIGHT, "%.3f" % env["height"])
        check("radius", env["radius"] <= MAX_RADIUS, "%.3f" % env["radius"])
        check("centred", max(abs(c) for c in env["centre"]) <= CENTRE_TOL,
              "%.3f, %.3f" % env["centre"])
        report["models"][key] = dict(tris=tris, **{k: (round(v, 4) if isinstance(v, float)
                                                    else [round(c, 4) for c in v])
                                                 for k, v in env.items()}, checks=checks)

    env = envelope(cage)
    inner = min(math.hypot(v.co.x, v.co.y) for v in cage.data.vertices)
    ctris = tri_count(cage)
    cchecks = {}
    for label, ok, detail in (
            ("closed", cage["non_manifold_edges"] == 0, int(cage["non_manifold_edges"])),
            ("tris", ctris <= TRIS_HARD, "%d" % ctris),
            ("clears the plinth", inner >= PLINTH_FOOT_R + 0.1,
             "inner radius %.2f vs plinth foot %.2f" % (inner, PLINTH_FOOT_R)),
            ("over the tallest marker", env["height"] >= MARKER_TOP + 0.2,
             "%.2f vs %.2f" % (env["height"], MARKER_TOP))):
        cchecks[label] = dict(ok=bool(ok), detail=detail)
        if not ok:
            failures.append("construction: %s (%s)" % (label, detail))
    report["construction"] = dict(tris=ctris, inner_radius=round(inner, 3),
                                  height=round(env["height"], 3), checks=cchecks)
    # the monolith: closed parts, within budget, and the glow clear of the slab's faces except
    # where the seams sit on them
    mtris = sum(tri_count(o) for o in mono)
    for o in mono:
        if o["non_manifold_edges"]:
            failures.append("monolith: %s not closed (%d)" % (o.name, o["non_manifold_edges"]))
    if mtris > TRIS_HARD:
        failures.append("monolith: %d tris" % mtris)
    report["monolith"] = dict(tris=mtris, body=envelope(mono[0])["height"])

    # ---- the guide's recipe A (UVs, LOD chain), then the deliverable OBJ
    helpers = mcp_helpers()
    report["mcp_pipeline"] = bool(helpers)
    special_dir = os.path.join(mod_root, "gfx", "models", "buildings", "special")
    os.makedirs(special_dir, exist_ok=True)
    for ob in mono:
        # make_object rests every object on z = 0; the glow has to keep the body's frame
        ob.location = (0, 0, 0)
    for ob in mono:
        bpy.ops.object.select_all(action="DESELECT")
        ob.select_set(True)
        bpy.context.view_layer.objects.active = ob
        bpy.ops.wm.obj_export(filepath=os.path.join(special_dir, ob.name + ".obj"),
                              export_selected_objects=True, export_triangulated_mesh=True,
                              export_normals=True, export_uv=True, export_materials=False,
                              apply_modifiers=True, forward_axis="NEGATIVE_Z", up_axis="Y")
    for key, ob in list(objs.items()) + [("construction", cage)]:
        if helpers:
            uv_helpers, export_helpers = helpers
            uv_helpers.unwrap_and_export_uv(
                ob.name, os.path.join(MCP_ROOT, "staging", "uv", "marker_emblems", ob.name + ".svg"))
            if lods:
                export_helpers.export_lod_chain(
                    ob.name, os.path.join(MCP_ROOT, "staging", "exports", "marker_emblems"))
        bpy.ops.object.select_all(action="DESELECT")
        ob.select_set(True)
        bpy.context.view_layer.objects.active = ob
        bpy.ops.wm.obj_export(filepath=os.path.join(gfx_dir, ob.name + ".obj"),
                              export_selected_objects=True, export_triangulated_mesh=True,
                              export_normals=True, export_uv=True, export_materials=False,
                              apply_modifiers=True, forward_axis="NEGATIVE_Z", up_axis="Y")

    # ---- the outlines the 2D holding icons are drawn from (build_holding_icons.py): every
    # triangle seen from the front (the camera side), mirrored as the game mirrors a Blender
    # view, so a 3D marker and its 2D icon are the same shape
    dg = bpy.context.evaluated_depsgraph_get()
    sil = {}
    for key, ob in objs.items():
        ev = ob.evaluated_get(dg)
        me = ev.to_mesh()
        me.calc_loop_triangles()
        V = [(round(-v.co.x, 5), round(v.co.z, 5)) for v in me.vertices]
        sil[key] = [[V[i] for i in t.vertices] for t in me.loop_triangles]
        ev.to_mesh_clear()
    with open(os.path.join(art_dir, "silhouettes.json"), "w", encoding="utf-8") as fh:
        json.dump(sil, fh, separators=(",", ":"))

    # ---- previews
    if do_render:
        ground = setup_render()
        ped, ped_top = pedestal(mod_root)
        plinth_mats = {k: plinth_material(mod_root, k) for k in HOLDING_ORDER}
        lift = ped_top + HOVER

        def stage(key, offset):
            """Place emblem `key` as build_marker_mesh.py would: scaled, base at the hover."""
            ob = objs[key]
            ob.scale = (EMBLEM_SCALE,) * 3
            ob.location = Vector(offset) + Vector((0, 0, lift))
            ob.hide_render = False

        def hide_all():
            for ob in objs.values():
                ob.hide_render = True

        tgt = (0, 0, 3.6)
        near = camera("cam_near", view_south(tgt, 15.0, 45), tgt, lens=50)
        cage.hide_render = True
        for o in mono:
            o.hide_render = True
        for key in HOLDING_ORDER:
            hide_all()
            stage(key, (0, 0, 0))
            ped.data.materials[0] = plinth_mats[key]
            render(os.path.join(prev_dir, key + "_near.png"), near, (560, 640))
        # construction: the cage around a castle, as the game would draw it
        hide_all()
        stage("castle", (0, 0, 0))
        ped.data.materials[0] = plinth_mats["castle"]
        cage.hide_render = False
        wide = camera("cam_construction", view_south((0, 0, 3.0), 22.0, 45), (0, 0, 3.0), lens=50)
        render(os.path.join(prev_dir, "construction_near.png"), wide, (560, 640))
        cage.hide_render = True

        # the lineup: all seven on plinths, at roughly 40-80 px tall (marker brief)
        sp = 7.0
        copies = []
        hide_all()
        for i, key in enumerate(HOLDING_ORDER):
            off = ((i - (len(HOLDING_ORDER) - 1) / 2) * sp, 0, 0)
            stage(key, off)
            c = objs[key].copy()
            REF.objects.link(c)
            copies.append(c)
            p = ped.copy()
            p.data = ped.data.copy()
            p.data.materials[0] = plinth_mats[key]
            p.location = off
            REF.objects.link(p)
            copies.append(p)
            objs[key].hide_render = True
        ped.hide_render = True
        far = camera("cam_far", view_south((0, 0, 2.5), 90, 55), (0, 0, 2.5), ortho=60)
        render(os.path.join(prev_dir, "lineup_far.png"), far, (1040, 260))

        # silhouette test: black shapes on white, emblems only, at icon size
        ground.hide_render = True
        bpy.context.scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = \
            (1, 1, 1, 1)
        black = emissive("sil_black", (0, 0, 0), 1.0)
        for c in copies:
            if c.name.startswith("ref_pedestal"):
                c.hide_render = True
            else:
                c.data = c.data.copy()
                c.data.materials.clear()
                c.data.materials.append(black)
        render(os.path.join(prev_dir, "silhouettes.png"), far, (1040, 260))
        for c in copies:
            bpy.data.objects.remove(c, do_unlink=True)
        ped.hide_render = False
        ground.hide_render = False
        bpy.context.scene.world.node_tree.nodes["Background"].inputs["Color"].default_value = \
            (0.004, 0.006, 0.012, 1)

        # sites: each glyph on the puck, as build_marker_mesh.py SITES builds them
        ped.hide_render = True
        puck, puck_top = pedestal(mod_root, "disc", SITE_PEDESTAL_SCALE, "ref_puck")
        site_mats = {k: plinth_material(mod_root, "site_" + k, "eotg_site_%s_puck_diffuse.dds" % k,
                                        "eotg_site_puck_properties.dds") for k in SITE_ORDER}
        puck.data.materials[0] = site_mats[SITE_ORDER[0]]
        tgt = (0, 0, 1.3)
        close = camera("cam_site", view_south(tgt, 9.0, 45), tgt, lens=50)
        for key in SITE_ORDER:
            hide_all()
            ob = objs[key]
            ob.scale = (SITE_EMBLEM_SCALE,) * 3
            ob.location = (0, 0, puck_top + SITE_HOVER)
            ob.hide_render = False
            puck.data.materials[0] = site_mats[key]
            render(os.path.join(prev_dir, key + "_near.png"), close, (560, 640))
        hide_all()
        puck.hide_render = True

        # the monolith, standing on the ground at its own locator
        for o in mono:
            o.hide_render = False
        tgt = (0, 0, 2.7)
        mcam = camera("cam_monolith", view_south(tgt, 11.0, 35), tgt, lens=50)
        render(os.path.join(prev_dir, "monolith_near.png"), mcam, (560, 640))
        for o in mono:
            o.hide_render = True
        ped.hide_render = False

        # leave the scene browsable: emblems in a row on their plinths' height
        for i, key in enumerate(ORDER):
            objs[key].location = ((i - (len(ORDER) - 1) / 2) * 2.0, 0, 0)
            objs[key].scale = (1, 1, 1)
            objs[key].hide_render = False
        cage.location = (0, -8.0, 0)
        cage.hide_render = False
        for o in mono:
            o.location = (8.0, -8.0, 0)
            o.hide_render = False
        ped.hide_render = True
        ped.hide_viewport = True

    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(art_dir, "eotg_marker_emblems.blend"),
                                compress=True, copy=not bpy.app.background)
    report["failures"] = failures
    with open(os.path.join(art_dir, "manifest.json"), "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=1)
    print("emblems %d, failures %d" % (len(objs), len(failures)))
    for f in failures:
        print("  FAIL", f)
    for key in ORDER:
        m = report["models"][key]
        print("  %-15s tris %4d  w %.2f  d %.2f  h %.2f  r %.2f" % (
            key, m["tris"], m["width_x"], m["depth"], m["height"], m["radius"]))
    return report


if __name__ == "__main__":
    argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    build(os.path.abspath(argv[0]) if argv else os.getcwd(), do_render="--render" in argv,
          lods="--no-lods" not in argv)
