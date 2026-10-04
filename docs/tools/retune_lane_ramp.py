"""Remove the grass-green band from the stellar lane ramp.

`gfx/map/rivers/eotg_lane_ramp.dds` is a 256x1 colour ramp, and it is sampled by more than its
name suggests: the stellar river lanes, the void nebula over open water, the shore glow and the
brighter stars all read their hue from it (`EotgRamp` in pdxwater.shader). One band was wrong for
all four.

25 of its 256 entries are green-dominant, in two runs:

    t 0.14-0.22   rgb(57,160,108)   grass green   <- the problem
    t 0.49-0.50   rgb(47,184,176)   teal          <- fine, reads as cyan

The green is EMERALD (#2E9C6A) from the palette in build_space_textures.py. It is the one hue
that cannot occur in the arc it sits in - the ramp goes warm cream at t~0.08 to pale violet at
t~0.25, and a nebula crossing that arc passes through rose, not through grass. On the map it
showed up as murky green blotches in open water, which reads as shallow sea: exactly the
medieval tell the whole space grade is trying to remove.

This patches the shipped file rather than regenerating it. Regenerating was tried and rejected:
the ramp has fine structure that a stop table does not reproduce - even 32 stops leave a maximum
error of 26 per channel, which would visibly change the lanes. Running it twice is a no-op: it checks
the band for green first and exits if there is none. Without that guard it was not quite
idempotent - the endpoints it rebuilds from are re-read as rounded bytes, so each run drifted
them by up to 1 per channel.

Usage:  python docs/tools/retune_lane_ramp.py <mod root>
"""
from __future__ import annotations

import os
import sys

import numpy as np
from PIL import Image



def dds_rgb(img, path):
    """Uncompressed 24-bit DDS, byte-identical in layout to the shipped ramp.

    Copied rather than imported from build_space_textures.py: that module does its work at
    import time, so importing it here silently regenerated every border, arrow and the flatmap.
    """
    import struct
    img = img.convert("RGB")
    w, h = img.size
    hdr = b"DDS " + struct.pack("<IIIIIII", 124, 0x1007 | 0x8, h, w, w * 3, 0, 0) + b"\0" * 44
    hdr += struct.pack("<IIIIIIII", 32, 0x40, 0, 24, 0xff0000, 0xff00, 0xff, 0)
    hdr += struct.pack("<IIIII", 0x1000, 0, 0, 0, 0)
    open(path, "wb").write(hdr + np.asarray(img)[:, :, [2, 1, 0]].tobytes())

REL = os.path.join("gfx", "map", "rivers", "eotg_lane_ramp.dds")
LO, HI = 32, 62                       # the green band, inclusive
ROSE = np.array([236.0, 152.0, 176.0])
BUMP = 0.75                           # how far toward rose at the middle of the band


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    path = os.path.join(sys.argv[1], REL)
    ramp = np.array(Image.open(path).convert("RGB"))[0].astype(np.float64)

    band = ramp[LO:HI + 1]
    if not ((band[:, 1] > band[:, 0]) & (band[:, 1] > band[:, 2])).any():
        print("already retuned - no green left in the band, nothing written")
        return

    before = int(((ramp[:, 1] > ramp[:, 0]) & (ramp[:, 1] > ramp[:, 2])).sum())

    a, b = ramp[LO].copy(), ramp[HI].copy()
    for i in range(LO, HI + 1):
        t = (i - LO) / (HI - LO)
        s = t * t * (3.0 - 2.0 * t)                  # smoothstep between the two neighbours
        base = a * (1.0 - s) + b * s
        bump = np.sin(np.pi * t) * BUMP              # zero at both ends, so this is idempotent
        ramp[i] = base * (1.0 - bump) + ROSE * bump

    after = int(((ramp[:, 1] > ramp[:, 0]) & (ramp[:, 1] > ramp[:, 2])).sum())
    dds_rgb(Image.fromarray(ramp.astype(np.uint8)[None, :, :]), path)
    print("wrote %s" % path)
    print("  green-dominant entries %d -> %d  (what remains is the teal at t~0.49)"
          % (before, after))
    print("  band t %.2f-%.2f rebuilt as %s -> rose -> %s"
          % (LO / 256, HI / 256, tuple(int(v) for v in a), tuple(int(v) for v in b)))


if __name__ == "__main__":
    main()
