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
    python docs/tools/build_marker_mesh.py <mod root> [--profile chess] [--pedestal-scale 1.7]
                                           [--emblem-scale 1.2] [--hover 0.28]
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from obj_to_pdxmesh import build_part, write_mesh, load_obj  # noqa: E402

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
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mod_root")
    ap.add_argument("--profile", default="chess", help="pedestal profile in make_marker_obj.py")
    ap.add_argument("--pedestal-scale", type=float, default=1.7)
    ap.add_argument("--emblem-scale", type=float, default=1.2)
    ap.add_argument("--hover", type=float, default=0.28,
                    help="gap between the pedestal top and the emblem's base, in world units")
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

    out = os.path.join(outdir, MESH)
    write_mesh([pedestal, emblem], out, SHAPE, MATERIALS)

    lo = np.minimum(pedestal["lo"], emblem["lo"])
    hi = np.maximum(pedestal["hi"], emblem["hi"])
    print("\nwrote %s" % out)
    print("  shape %s, 2 material slots (0 pedestal, 1 emblem)" % SHAPE)
    print("  overall %.2f x %.2f x %.2f   base at y=%.2f   emblem floats %.2f above the pedestal"
          % (hi[0]-lo[0], hi[1]-lo[1], hi[2]-lo[2], lo[1], a.hover))
    print("  (vanilla building_western_castle_01 is 2.77 x 4.16 x 2.17)")


if __name__ == "__main__":
    main()
