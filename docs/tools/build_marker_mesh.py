"""Build the province markers: one mesh per holding type, each a plinth, an emblem and a beam.

A CK3 .mesh may hold several `mesh` blocks under a single shape, each with its own vertices and
its own material. The .asset addresses them by position - `index = 0`, `index = 1` - and gives
each its own textures. Vanilla does this for cliff_small_01 (rock slot 0, grass cap slot 1).

That is what lets one model light two ways. Both slots run the same effect, because the effect
also carries PDX_MESH_SNAP_VERTICES_TO_TERRAIN and a part that did not snap would sit at sea
level while the rest of the model stood on the ground. The difference between stone and glow is
therefore made in the TEXTURE, not the shader: EOTG_MARKER multiplies its emissive and rim by
Properties.r. The plinth's mask is 1 only on its trim lines, so the body lights as plain metal
while the trims glow (build_marker_assets.py), and the emblem's mask is 1 everywhere.

Geometry, the same in all seven meshes except the emblem:
  index 0  the pedestal, lathed by make_marker_obj.py
  index 1  that holding type's emblem (eotg_marker_<type>.obj, from blender_marker_emblems.py),
           scaled and lifted to float just above the pedestal's top
  index 2  the projector beam, fitted to that emblem's width

Usage:
    python docs/tools/build_marker_mesh.py <mod root> [--profile chess] [--pedestal-scale 2.04]
                                           [--emblem-scale 1.44] [--hover 0.336]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from obj_to_pdxmesh import build_part, write_mesh, load_obj  # noqa: E402
from make_beam_obj import beam_obj  # noqa: E402

REL = os.path.join("gfx", "models", "buildings", "eotg_markers")
SHAPE = "eotg_markerShape"
MESH = "eotg_marker_%s.mesh"      # one per holding type: the shared plinth, that type's emblem,
                                  # and a beam fitted to it

# The seven holding types (holding representation brief s3.1). Each has its own emblem,
# authored by blender_marker_emblems.py as eotg_marker_<type>.obj in REL. The names match
# build_marker_assets.py HOLDINGS, so mesh and colour pair up with no second table.
TYPES = ("castle", "city", "temple", "temple_citadel", "tribal", "nomad", "herder")

# Sites are not holdings: activity sites, the adventurer camp and epidemic sites. They stand on
# the low "disc" puck, smaller than a holding's plinth, so a site never reads as a holding. They
# share the marker's three material slots, so build_marker_assets.py textures them the same way.
SITES = ("feast", "hunt", "tournament", "wedding", "camp", "quarantine", "decon", "purge")
SITE_MESH = "eotg_site_%s.mesh"
SITE_PROFILE = "disc"
SITE_PEDESTAL_SCALE = 1.30       # 2.6 wide: about half the holding plinth's footprint
SITE_EMBLEM_SCALE = 1.20
SITE_HOVER = 0.22

# The holy-site landmark replaces vanilla's cathedral meshes by path, so it lives in their folder
MONOLITH_DIR = os.path.join("gfx", "models", "buildings", "special")
MONOLITH_MESH = "eotg_precursor_monolith.mesh"
MONOLITH_SHAPE = "eotg_precursor_monolithShape"
MONOLITH_MATERIALS = [
    dict(shader="snap_to_terrain", diff="eotg_monolith_body_diffuse.dds", normal="nonormal.dds",
         spec="noproperties.dds"),
    dict(shader="snap_to_terrain", diff="eotg_monolith_glow_diffuse.dds", normal="nonormal.dds",
         spec="eotg_marker_glow_properties.dds"),
]

# The construction cage: not a marker. The engine draws the `construction` entity at the
# holding's own locator, around the holding model, so this is one translucent wireframe in world
# units (blender_marker_emblems.py build_cage), on the beam's blending effect, with no plinth.
CAGE_OBJ = "eotg_construction.obj"
CAGE_MESH = "eotg_construction.mesh"
CAGE_SHAPE = "eotg_constructionShape"
CAGE_MATERIAL = dict(shader="snap_to_terrain_alpha_to_coverage",
                     diff="eotg_construction_diffuse.dds", normal="nonormal.dds",
                     spec="eotg_marker_glow_properties.dds")


def emblem_path(outdir, holding):
    return os.path.join(outdir, "eotg_marker_%s.obj" % holding)

# Slot 0 is the pedestal, slot 1 the emblem. The diffuse names here are only the defaults baked
# into the mesh; the .asset overrides both per government, which is how nine colours share one
# mesh file. `spec` is what decides which slot glows - see the module docstring.
MATERIALS = [
    dict(shader="standard", diff="eotg_marker_stone_diffuse.dds",
         normal="nonormal.dds", spec="noproperties.dds"),
    dict(shader="standard", diff="eotg_marker_neutral_diffuse.dds",
         normal="nonormal.dds", spec="eotg_marker_glow_properties.dds"),
    # The beam. It is the one slot that must NOT be opaque, so it is the one slot on a different
    # effect - see make_beam_obj.py for why this particular vanilla name and no other.
    dict(shader="snap_to_terrain_alpha_to_coverage", diff="eotg_marker_neutral_beam.dds",
         normal="nonormal.dds", spec="eotg_marker_glow_properties.dds"),
]

# Beam proportions, as multiples of what they sit against, so they survive the emblem being
# replaced. The base is deliberately narrower than the pedestal's top face - a projector aperture
# is smaller than the plinth it is set into - and the top is wider than the emblem so the emblem
# sits INSIDE the light rather than balancing on top of it.
BEAM_R0_OF_PEDESTAL = 0.55
BEAM_R1_OF_EMBLEM = 1.15   # slightly wider than the emblem, so from directly above the beam still
                           # shows as a ring around it instead of hiding behind it


def top_radius(part, frac=0.12):
    """Radius of a part's topmost band, not of its bounding box.

    The pedestal is a lathe with a flared foot, so its bounding box is much wider than its top
    face. Sizing the beam off the box would plant an aperture wider than the plinth it rises from.
    """
    import numpy as np
    pos = part["pos"]
    hi_y, lo_y = float(part["hi"][1]), float(part["lo"][1])
    band = max((hi_y - lo_y) * frac, 1e-6)
    top = pos[pos[:, 1] >= hi_y - band]
    if not len(top):
        top = pos
    return float(np.hypot(top[:, 0], top[:, 2]).max())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mod_root")
    ap.add_argument("--profile", default="chess", help="pedestal profile in make_marker_obj.py")
    ap.add_argument("--pedestal-scale", type=float, default=2.04)   # 1.70 +20%
    ap.add_argument("--emblem-scale", type=float, default=1.44)    # 1.20 +20%
    # 0.28 +20% as well, so the gap grows with the model instead of closing up.
    # 0.28 +20% as well, so the gap grows with the model instead of closing up.
    #
    # This was briefly raised to 0.90 to give the beam room to fade in, and that was a mistake:
    # the beam fills the gap, so a taller gap is a taller cone sitting on the plinth, and at the
    # opacity it had it read as the PEDESTAL having been stretched upwards rather than as light.
    # The marker's proportions are not the beam's to spend. The gap is back where it was, the beam
    # is whatever height fits in it, and the cone was made fainter and more coloured instead -
    # which is what should have been done in the first place.
    ap.add_argument("--hover", type=float, default=0.336,
                    help="gap between the pedestal top and the emblem's base, in world units; "
                         "this is also exactly how tall the beam is")
    ap.add_argument("--beam-segments", type=int, default=48,
                    help="radial segments in the projector beam")
    a = ap.parse_args()

    here = os.path.dirname(os.path.abspath(__file__))
    outdir = os.path.join(a.mod_root, REL)
    os.makedirs(outdir, exist_ok=True)

    missing = [t for t in TYPES if not os.path.exists(emblem_path(outdir, t))]
    if missing:
        sys.exit("missing emblems: " + ", ".join(emblem_path(outdir, t) for t in missing)
                 + "\n(generate them with docs/tools/blender_marker_emblems.py)")

    tmp = os.environ.get("TEMP", ".")
    ped_obj = os.path.join(tmp, "eotg_pedestal_%s.obj" % a.profile)
    subprocess.run([sys.executable, os.path.join(here, "make_marker_obj.py"),
                    a.profile, ped_obj], check=True, stdout=subprocess.DEVNULL)

    print("pedestal:")
    pedestal = build_part(ped_obj, a.pedestal_scale, 0.0, False, False, 0.0, False, "pedestal")
    ped_r = top_radius(pedestal)
    beam_y0 = float(pedestal["hi"][1])

    for holding in TYPES:
        print("\n%s:" % holding)
        # Emblems are authored with their lowest point at y = 0 (blender_marker_emblems.py),
        # but drop whatever the minimum is anyway and re-apply a deliberate gap, so the hover is
        # a decision and not an accident of authoring.
        src = emblem_path(outdir, holding)
        P, _, _, _ = load_obj(src)
        emblem_min_y = float(np.asarray(P, np.float64)[:, 1].min())
        lift = beam_y0 + a.hover
        emblem = build_part(src, a.emblem_scale, lift, False, False, emblem_min_y, False,
                            "emblem")

        # The beam spans the GAP ONLY - pedestal top to emblem base - and stops there. It used to
        # run the full height of the emblem, which put a still-bright cone inside the model and
        # gave it a visible edge; geometry that ends where the model begins cannot cut off
        # against it. Every number comes from the parts just built, so each emblem gets a beam
        # fitted to its own width.
        emb_r = float(np.hypot(emblem["pos"][:, 0], emblem["pos"][:, 2]).max())
        beam_h = float(emblem["lo"][1]) - beam_y0
        beam_path = os.path.join(tmp, "eotg_beam_%s.obj" % holding)
        beam_obj(beam_path, a.beam_segments, ped_r * BEAM_R0_OF_PEDESTAL,
                 emb_r * BEAM_R1_OF_EMBLEM, 0.0, beam_h)
        # offset_y rather than baking y0 into the .obj, so the generated file stays a plain
        # frustum sitting at the origin and is readable on its own.
        beam = build_part(beam_path, 1.0, beam_y0, False, False, 0.0, False, "beam")

        out = os.path.join(outdir, MESH % holding)
        write_mesh([pedestal, emblem, beam], out, SHAPE, MATERIALS)
        lo = np.minimum(pedestal["lo"], emblem["lo"])
        hi = np.maximum(pedestal["hi"], emblem["hi"])
        tris = sum(len(x["tri"]) for x in (pedestal, emblem, beam))
        print("  wrote %s  (%d tris)" % (out, tris))
        print("  beam r %.2f -> %.2f, y %.2f..%.2f   overall %.2f x %.2f x %.2f"
              % (ped_r * BEAM_R0_OF_PEDESTAL, emb_r * BEAM_R1_OF_EMBLEM, beam_y0,
                 beam_y0 + beam_h, hi[0] - lo[0], hi[1] - lo[1], hi[2] - lo[2]))
    print("\n(vanilla building_western_castle_01 is 2.77 x 4.16 x 2.17)")

    # Sites: activities, the adventurer camp and epidemics. Same build as a holding, but on the
    # low "disc" puck, so a site can never be mistaken for a holding on its plinth.
    site_obj = os.path.join(tmp, "eotg_puck_%s.obj" % SITE_PROFILE)
    subprocess.run([sys.executable, os.path.join(here, "make_marker_obj.py"),
                    SITE_PROFILE, site_obj], check=True, stdout=subprocess.DEVNULL)
    print("\npuck:")
    puck = build_part(site_obj, SITE_PEDESTAL_SCALE, 0.0, False, False, 0.0, False, "puck")
    puck_r = top_radius(puck)
    puck_top = float(puck["hi"][1])
    for site in SITES:
        print("\n%s:" % site)
        src = emblem_path(outdir, site)
        if not os.path.exists(src):
            sys.exit("missing %s (generate it with docs/tools/blender_marker_emblems.py)" % src)
        P, _, _, _ = load_obj(src)
        emblem_min_y = float(np.asarray(P, np.float64)[:, 1].min())
        emblem = build_part(src, SITE_EMBLEM_SCALE, puck_top + SITE_HOVER, False, False,
                            emblem_min_y, False, "glyph")
        emb_r = float(np.hypot(emblem["pos"][:, 0], emblem["pos"][:, 2]).max())
        beam_path = os.path.join(tmp, "eotg_beam_%s.obj" % site)
        beam_obj(beam_path, a.beam_segments, puck_r * BEAM_R0_OF_PEDESTAL,
                 emb_r * BEAM_R1_OF_EMBLEM, 0.0, float(emblem["lo"][1]) - puck_top)
        beam = build_part(beam_path, 1.0, puck_top, False, False, 0.0, False, "beam")
        out = os.path.join(outdir, SITE_MESH % site)
        write_mesh([puck, emblem, beam], out, SHAPE, MATERIALS)
        hi = np.maximum(puck["hi"], emblem["hi"])
        lo = np.minimum(puck["lo"], emblem["lo"])
        print("  wrote %s  (%.2f x %.2f x %.2f)" % (out, hi[0] - lo[0], hi[1] - lo[1],
                                                   hi[2] - lo[2]))

    # The holy-site landmark: two parts authored in one frame, so no re-basing.
    print("\nprecursor monolith:")
    sdir = os.path.join(a.mod_root, MONOLITH_DIR)
    parts = []
    for part in ("body", "glow"):
        src = os.path.join(sdir, "eotg_precursor_monolith__%s.obj" % part)
        if not os.path.exists(src):
            sys.exit("missing %s (generate it with docs/tools/blender_marker_emblems.py)" % src)
        parts.append(build_part(src, 1.0, 0.0, False, False, 0.0, False, part))
    write_mesh(parts, os.path.join(sdir, MONOLITH_MESH), MONOLITH_SHAPE, MONOLITH_MATERIALS)
    print("  wrote %s" % os.path.join(sdir, MONOLITH_MESH))

    print("\nconstruction cage:")
    cage_src = os.path.join(outdir, CAGE_OBJ)
    if not os.path.exists(cage_src):
        sys.exit("missing %s (generate it with docs/tools/blender_marker_emblems.py)" % cage_src)
    cage = build_part(cage_src, 1.0, 0.0, False, False, 0.0, False, "cage")
    write_mesh([cage], os.path.join(outdir, CAGE_MESH), CAGE_SHAPE, [CAGE_MATERIAL])
    print("  wrote %s" % os.path.join(outdir, CAGE_MESH))


if __name__ == "__main__":
    main()
