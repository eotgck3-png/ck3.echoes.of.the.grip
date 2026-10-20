"""Author the marker plinth's brushed-metal base in PhotoCraft.

The plinth stopped being carved stone on 2026-10-20. The holding representation brief frames
holdings as holographic beacons on a star table, "not physical miniature structures", so the
plinth is now a projector base: dark brushed gunmetal with glowing trims. This script makes
only the metal. build_marker_assets.py composites the trims over it in each holding's colour
and makes it seamless where U wraps round the lathe.

Brushed metal is noise smeared along one axis. U runs round the plinth, so the smear is
horizontal, giving circumferential brushing, like turned metal.

PhotoCraft writes only inside the MCP workspace (C:/Users/river/MCP), so the image is authored
in staging/textures/ as the workflow guide prescribes, then copied to
docs/art/marker_plinth/eotg_plinth_metal.png, which is the committed source.

Usage:  python docs/tools/build_plinth_material.py <mod root>
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys

PHOTOCRAFT = r"C:\Program Files\PhotoCraft\photocraft-cli.exe"
STAGING = r"C:\Users\river\MCP\staging\textures\eotg_plinth\eotg_plinth_metal.png"
DEST = os.path.join("docs", "art", "marker_plinth", "eotg_plinth_metal.png")

# Base value: about (58, 64, 77) once noise averages out. Darker than the old stone (74-132), so
# the trims and emblem read as the light source, but not so dark that the plinth's outline
# drowns in the dark map.
BASE = "#3a404d"

STEPS = [
    ("edit.fill", {"contents": "color", "color": BASE}),
    ("filter.noise.addNoise", {"amount": 22, "distribution": "gaussian",
                               "monochromatic": True, "seed": 866}),
    ("filter.blur.motionBlur", {"angle": 0, "distance": 60}),
    # fine grain back on top, so the brushing does not look airbrushed
    ("filter.noise.addNoise", {"amount": 3, "distribution": "gaussian",
                               "monochromatic": True, "seed": 7}),
]


def main():
    mod_root = sys.argv[1] if len(sys.argv) > 1 else "."
    os.makedirs(os.path.dirname(STAGING), exist_ok=True)
    cmd = [PHOTOCRAFT, "run", "--new",
           json.dumps({"width": 512, "height": 512, "mode": "rgb", "depth": 8,
                       "background": "white"})]
    for cid, params in STEPS:
        cmd += ["--cmd", cid, "--params", json.dumps(params)]
    cmd += ["--out", STAGING, "--format", "png"]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL)
    dest = os.path.join(mod_root, DEST)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.copyfile(STAGING, dest)
    print("wrote", dest)


if __name__ == "__main__":
    main()
