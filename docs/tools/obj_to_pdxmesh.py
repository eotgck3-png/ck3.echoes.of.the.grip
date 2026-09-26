"""Convert a triangulated .obj into Paradox's PDX @@b@ .mesh format.

Why this is written rather than exported. io_pdx_mesh in Blender is the safe route and remains the
right one for anything complicated. This exists so a marker mesh can go from .obj to in-game
without a round trip, and because the format turned out to be simple enough to write once its
layout had been read out of a real file.

Layout, decoded from gfx/models/mapitems/cliffs/cliff_rock_02.mesh:

    "@@b@"
    !<len><name> <type> ...            a property
        type 'i' : u32 count, then count * int32
        type 'f' : u32 count, then count * float32
        type 's' : u32 count, then u32 BYTE LENGTH, then that many bytes (null terminated)
    [<name>\\0                          an object; the number of leading '[' is its depth

    [object
     [[<ShapeName>
      [[[mesh        p, n, ta, u0, tri, boundingsphere
       [[[[aabb      min, max
       [[[[material  shader, diff, n, spec
     [[locator

Vertex data is per-vertex and parallel: p is 3 floats, n is 3, ta is 4 (xyz + handedness), u0 is 2.

TWO THINGS CANNOT BE CHECKED WITHOUT RENDERING, so both are switchable:
  * winding order - if the model looks hollow or invisible, it is inside out: use --flip-winding.
    A closed mesh that is backface-culled the wrong way shows its interior, which usually reads as
    nothing at all.
  * V orientation - if a texture appears upside down, use --flip-v. Irrelevant for a flat colour.

Usage:
    python docs/tools/obj_to_pdxmesh.py in.obj out.mesh --shape MyShape [--flip-winding] [--flip-v]
                                        [--scale 1.0] [--drop-y 0.0] [--verify]
"""
from __future__ import annotations

import argparse
import struct
import sys

import numpy as np


# ---------------------------------------------------------------- writing

def prop_f(name, values):
    b = name.encode("latin1")
    a = np.asarray(values, np.float32).ravel()
    return b"!" + bytes([len(b)]) + b + b"f" + struct.pack("<I", a.size) + a.tobytes()


def prop_i(name, values):
    b = name.encode("latin1")
    a = np.asarray(values, np.int32).ravel()
    return b"!" + bytes([len(b)]) + b + b"i" + struct.pack("<I", a.size) + a.tobytes()


def prop_s(name, text):
    b = name.encode("latin1")
    s = text.encode("latin1") + b"\0"
    return b"!" + bytes([len(b)]) + b + b"s" + struct.pack("<I", 1) + struct.pack("<I", len(s)) + s


def obj_node(depth, name):
    return b"[" * depth + name.encode("latin1") + b"\0"


# ---------------------------------------------------------------- reading the obj

def load_obj(path):
    """Returns per-corner arrays. An .obj indexes p/n/uv separately, so a corner is the unit that
    carries a consistent (position, normal, uv) triple - which is what a GPU vertex is too."""
    P, N, T, tris = [], [], [], []
    for line in open(path, encoding="utf-8", errors="ignore"):
        w = line.split()
        if not w:
            continue
        if w[0] == "v":
            P.append([float(x) for x in w[1:4]])
        elif w[0] == "vn":
            N.append([float(x) for x in w[1:4]])
        elif w[0] == "vt":
            T.append([float(x) for x in w[1:3]])
        elif w[0] == "f":
            if len(w) != 4:
                sys.exit("face with %d corners: triangulate the .obj first" % (len(w) - 1))
            tri = []
            for tok in w[1:]:
                bits = (tok.split("/") + ["", ""])[:3]
                vi = int(bits[0]) - 1
                ti = int(bits[1]) - 1 if bits[1] else -1
                ni = int(bits[2]) - 1 if bits[2] else -1
                tri.append((vi, ti, ni))
            tris.append(tri)
    return np.array(P, np.float64), np.array(N, np.float64), np.array(T, np.float64), tris


def build_vertices(P, N, T, tris, flip_v):
    """One GPU vertex per unique (position, uv, normal) triple."""
    lut, pos, nrm, uv, idx = {}, [], [], [], []
    for tri in tris:
        for vi, ti, ni in tri:
            key = (vi, ti, ni)
            if key not in lut:
                lut[key] = len(pos)
                pos.append(P[vi])
                nrm.append(N[ni] if ni >= 0 and ni < len(N) else (0.0, 1.0, 0.0))
                if ti >= 0 and ti < len(T):
                    u, v = T[ti]
                else:
                    u, v = 0.0, 0.0
                uv.append((u, 1.0 - v if flip_v else v))
            idx.append(lut[key])
    return (np.array(pos, np.float64), np.array(nrm, np.float64),
            np.array(uv, np.float64), np.array(idx, np.int32).reshape(-1, 3))


def tangents(pos, nrm, uv, tri):
    """Per-vertex tangent with handedness in w, the usual Lengyel accumulation. The engine needs
    `ta` present and normalised; exact handedness only matters once a real normal map is used."""
    tan = np.zeros((len(pos), 3), np.float64)
    bit = np.zeros((len(pos), 3), np.float64)
    for a, b, c in tri:
        e1, e2 = pos[b] - pos[a], pos[c] - pos[a]
        d1, d2 = uv[b] - uv[a], uv[c] - uv[a]
        den = d1[0] * d2[1] - d2[0] * d1[1]
        if abs(den) < 1e-12:
            continue
        r = 1.0 / den
        t = (e1 * d2[1] - e2 * d1[1]) * r
        bt = (e2 * d1[0] - e1 * d2[0]) * r
        for i in (a, b, c):
            tan[i] += t
            bit[i] += bt
    out = np.zeros((len(pos), 4), np.float64)
    for i in range(len(pos)):
        n = nrm[i]
        t = tan[i] - n * float(np.dot(n, tan[i]))
        ln = float(np.linalg.norm(t))
        t = t / ln if ln > 1e-9 else np.array([1.0, 0.0, 0.0])
        w = -1.0 if float(np.dot(np.cross(n, t), bit[i])) < 0.0 else 1.0
        out[i, :3] = t
        out[i, 3] = w
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("obj")
    ap.add_argument("out")
    ap.add_argument("--shape", default="eotg_markerShape")
    ap.add_argument("--diffuse", default="eotg_marker_diffuse.dds")
    ap.add_argument("--normal", default="nonormal.dds")
    ap.add_argument("--specular", default="noproperties.dds")
    ap.add_argument("--shader", default="standard")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--drop-y", type=float, default=0.0,
                    help="subtract this from Y; use the model's min Y to sit it on the ground")
    ap.add_argument("--flip-winding", action="store_true")
    ap.add_argument("--flip-v", action="store_true")
    ap.add_argument("--verify", action="store_true")
    a = ap.parse_args()

    P, N, T, tris = load_obj(a.obj)
    pos, nrm, uv, tri = build_vertices(P, N, T, tris, a.flip_v)
    if a.flip_winding:
        tri = tri[:, [0, 2, 1]]
    if a.scale != 1.0:
        pos = pos * a.scale
    if a.drop_y:
        pos = pos.copy()
        pos[:, 1] -= a.drop_y * (a.scale if a.scale != 1.0 else 1.0)

    ta = tangents(pos, nrm, uv, tri)
    lo, hi = pos.min(0), pos.max(0)
    ctr = (lo + hi) / 2.0
    radius = float(np.linalg.norm(pos - ctr, axis=1).max())

    body = b"@@b@"
    body += prop_i("pdxasset", [1, 0])
    body += obj_node(1, "object")
    body += obj_node(2, a.shape)
    body += obj_node(3, "mesh")
    body += prop_f("p", pos)
    body += prop_f("n", nrm)
    body += prop_f("ta", ta)
    body += prop_f("u0", uv)
    body += prop_i("tri", tri)
    body += prop_f("boundingsphere", [ctr[0], ctr[1], ctr[2], radius])
    body += obj_node(4, "aabb")
    body += prop_f("min", lo)
    body += prop_f("max", hi)
    body += obj_node(4, "material")
    body += prop_s("shader", a.shader)
    body += prop_s("diff", a.diffuse)
    body += prop_s("n", a.normal)
    body += prop_s("spec", a.specular)
    body += obj_node(1, "locator")

    open(a.out, "wb").write(body)
    print(f"wrote {a.out}")
    print(f"  vertices {len(pos)}  triangles {len(tri)}")
    print(f"  size {hi[0]-lo[0]:.3f} x {hi[1]-lo[1]:.3f} x {hi[2]-lo[2]:.3f}   minY {lo[1]:.3f}")
    print(f"  boundingsphere r={radius:.3f}   winding {'FLIPPED' if a.flip_winding else 'as authored'}")

    if a.verify:
        verify(a.out, len(pos), len(tri))


def verify(path, nverts, ntris):
    """Read the file back with an independent parse and check the structure survives a round trip.
    This cannot tell you the winding is right - only that the container is well formed."""
    d = open(path, "rb").read()
    assert d[:4] == b"@@b@", "bad magic"
    i, seen = 4, {}
    while i < len(d):
        c = d[i:i + 1]
        if c == b"[":
            j = i
            while d[j:j + 1] == b"[":
                j += 1
            e = d.index(b"\0", j)
            seen.setdefault("objects", []).append((j - i, d[j:e].decode("latin1")))
            i = e + 1
            continue
        if c == b"!":
            ln = d[i + 1]
            name = d[i + 2:i + 2 + ln].decode("latin1")
            i = i + 2 + ln
            t = d[i:i + 1]
            i += 1
            n = struct.unpack_from("<I", d, i)[0]
            i += 4
            # NOTE first occurrence wins. "n" is used twice - vertex normals inside the mesh and
            # the normal-map filename inside the material - and letting the second overwrite the
            # first made the verifier report a mismatch on a file that was perfectly fine.
            if t == b"s":
                bl = struct.unpack_from("<I", d, i)[0]
                i += 4 + bl
                seen.setdefault(name, ("s", bl))
            else:
                i += 4 * n
                seen.setdefault(name, (t.decode(), n))
            continue
        i += 1
    ok = True
    for k, want in (("p", nverts * 3), ("n", nverts * 3), ("ta", nverts * 4),
                    ("u0", nverts * 2), ("tri", ntris * 3)):
        got = seen.get(k, (None, -1))[1]
        flag = "ok" if got == want else "MISMATCH"
        if got != want:
            ok = False
        print(f"    {k:15} {got:7d} (expected {want}) {flag}")
    print("    objects: " + ", ".join(f"{'['*d}{n}" for d, n in seen.get("objects", [])))
    print("  round trip " + ("clean" if ok else "FAILED"))


if __name__ == "__main__":
    main()
