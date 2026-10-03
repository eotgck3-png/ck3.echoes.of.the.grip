"""Build the province marker as ONE mesh with TWO materials: a stone pedestal and a glowing emblem.

A CK3 .mesh may hold several `mesh` blocks under a single shape, each with its own vertices and
its own material. The .asset addresses them by position - `index = 0`, `index = 1` - and gives
each its own textures. Vanilla does this for cliff_small_01 (rock slot 0, grass cap slot 1).

That is what lets one model light two ways. Both slots run the same effect, because the effect
also carries PDX_MESH_SNAP_VERTICES_TO_TERRAIN and a part that did not snap would sit at sea
level while the rest of the model stood on the ground. The difference between stone and glow is
therefore made in the TEXTURE, not the shader: EOTG_MARKER multiplies its emissive and rim by
Properties.r, so the pedestal (r = 0, i.e. plain noproperties.dds) lights as ordinary stone and
the emblem (r = 1) glows.

Geometry:
  index 0  the pedestal, lathed by make_marker_obj.py
  index 1  the supplied emblem, scaled and lifted to float just above the pedestal's top

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
MESH = "eotg_marker.mesh"

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

    emblem_obj = os.path.join(outdir, "eotg_marker_source.obj")
    if not os.path.exists(emblem_obj):
        sys.exit("missing the supplied emblem at " + emblem_obj)

    tmp = os.environ.get("TEMP", ".")
    ped_obj = os.path.join(tmp, "eotg_pedestal_%s.obj" % a.profile)
    subprocess.run([sys.executable, os.path.join(here, "make_marker_obj.py"),
                    a.profile, ped_obj], check=True, stdout=subprocess.DEVNULL)

    print("parts:")
    pedestal = build_part(ped_obj, a.pedestal_scale, 0.0, False, False, 0.0, False, "pedestal")

    # The supplied emblem is authored off the origin - its lowest point is at y = 0.837, so it
    # already floats. Drop that out first and re-apply a deliberate gap, otherwise the hover
    # would scale with the emblem and stop being a decision.
    P, _, _, _ = load_obj(emblem_obj)
    emblem_min_y = float(np.asarray(P, np.float64)[:, 1].min())
    lift = float(pedestal["hi"][1]) + a.hover
    emblem = build_part(emblem_obj, a.emblem_scale, lift, False, False, emblem_min_y, False,
                        "emblem")

    # The beam spans the GAP ONLY - pedestal top to emblem base - and stops there. It used to run
    # the full height of the emblem, which is what put a still-bright cone inside the model and
    # gave it a visible edge; geometry that ends where the model begins cannot cut off against it.
    # Every number is derived from the two parts just built, so a taller or wider emblem gets a
    # taller or wider beam without this file being touched.
    ped_r = top_radius(pedestal)
    emb_r = float(np.hypot(emblem["pos"][:, 0], emblem["pos"][:, 2]).max())
    beam_y0 = float(pedestal["hi"][1])
    beam_h = float(emblem["lo"][1]) - beam_y0
    beam_path = os.path.join(tmp, "eotg_beam.obj")
    beam_obj(beam_path, a.beam_segments, ped_r * BEAM_R0_OF_PEDESTAL,
             emb_r * BEAM_R1_OF_EMBLEM, 0.0, beam_h)
    # offset_y rather than baking y0 into the .obj, so the generated file stays a plain frustum
    # sitting at the origin and is readable on its own.
    beam = build_part(beam_path, 1.0, beam_y0, False, False, 0.0, False, "beam")

    out = os.path.join(outdir, MESH)
    write_mesh([pedestal, emblem, beam], out, SHAPE, MATERIALS)

    lo = np.minimum(pedestal["lo"], emblem["lo"])
    hi = np.maximum(pedestal["hi"], emblem["hi"])
    print("\nwrote %s" % out)
    print("  shape %s, 3 material slots (0 pedestal, 1 emblem, 2 beam)" % SHAPE)
    print("  beam r %.2f -> %.2f, y %.2f..%.2f  (pedestal top r %.2f, emblem r %.2f)"
          % (ped_r * BEAM_R0_OF_PEDESTAL, emb_r * BEAM_R1_OF_EMBLEM, beam_y0, beam_y0 + beam_h,
             ped_r, emb_r))
    print("  overall %.2f x %.2f x %.2f   base at y=%.2f   emblem floats %.2f above the pedestal"
          % (hi[0]-lo[0], hi[1]-lo[1], hi[2]-lo[2], lo[1], a.hover))
    print("  (vanilla building_western_castle_01 is 2.77 x 4.16 x 2.17)")


if __name__ == "__main__":
    main()
