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

WINDING IS CHECKED, NOT GUESSED. An earlier version of this file claimed winding could only be
verified by rendering. That was wrong, and it cost a build: a mesh whose triangles are wound
against their own authored normals is backface-culled everywhere and draws nothing at all.
check_winding() compares each triangle's geometric normal (cross of its edges) with the normal
the author gave it, and refuses to write a mesh where they disagree. Measured on a mesh known to
render correctly in game, agreement is 1672 of 1672; on the broken one it was 0 of 960.
Use --flip-winding to correct a source that fails, or --force to write anyway.

Still not checkable offline:
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


def check_winding(pos, nrm, tri):
    """How many triangles are wound so their geometric normal matches the authored one.

    A triangle (a,b,c) faces along cross(b-a, c-a). If that opposes the normal the modeller gave
    those vertices, the face is pointing the wrong way, and a closed mesh wound that way is culled
    on every face - it renders as nothing, which looks exactly like a missing file or a bad shader
    and sends you looking in the wrong place.
    """
    a, b, c = pos[tri[:, 0]], pos[tri[:, 1]], pos[tri[:, 2]]
    geo = np.cross(b - a, c - a)
    ln = np.linalg.norm(geo, axis=1)
    ok = ln > 1e-12
    geo[ok] /= ln[ok][:, None]
    shading = (nrm[tri[:, 0]] + nrm[tri[:, 1]] + nrm[tri[:, 2]]) / 3.0
    d = (geo * shading).sum(1)[ok]
    return int((d > 0).sum()), int((d < 0).sum())


# The shader name baked into the .mesh material is NOT where a custom effect goes. That name is
# resolved against the engine's default shader file, not against whatever the .asset names, so a
# mod effect put here fails to resolve and the material is never created - the mesh then draws
# nothing, with only this in error.log:
#
#   Failed to create material with shader eotg_marker (in gfx/FX/court_scene.shader)
#
# court_scene.shader is simply where it looked; it has nothing to do with the mod. The custom
# effect belongs in the .asset meshsettings, as `shader` plus `shader_file`, which does override.
# These are the names vanilla's own holding meshes embed.
MESH_SHADERS = ("standard", "standard_atlas", "snap_to_terrain", "snap_to_terrain_atlas",
                "decal_local")


def build_part(obj_path, scale, offset_y, flip_v, flip_winding, drop_y, force, label):
    """Load one .obj and return the arrays a sub-mesh needs, already placed.

    A CK3 .mesh can hold several `mesh` blocks under one shape, each with its own vertices and
    its own material; the .asset addresses them with `index = 0`, `index = 1` and so on. That is
    how one model gets two surfaces that light differently - a stone pedestal and a glowing
    emblem - without needing two separate meshes placed at the same spot.
    """
    P, N, T, tris = load_obj(obj_path)
    pos, nrm, uv, tri = build_vertices(P, N, T, tris, flip_v)
    if flip_winding:
        tri = tri[:, [0, 2, 1]]
    pos = pos * scale
    if drop_y:
        pos = pos.copy()
        pos[:, 1] -= drop_y * scale
    if offset_y:
        pos = pos.copy()
        pos[:, 1] += offset_y

    agree, disagree = check_winding(pos, nrm, tri)
    if disagree > agree and not force:
        sys.exit(
            "\nWINDING IS INVERTED in %s: %d of %d triangles are wound against their own "
            "normals.\nThe engine would backface-cull this mesh and draw nothing, which looks "
            "exactly like a missing file. Re-run with --flip-winding, or --force."
            % (obj_path, disagree, agree + disagree))

    ta = tangents(pos, nrm, uv, tri)
    lo, hi = pos.min(0), pos.max(0)
    print("  %-10s verts %5d  tris %5d  size %.2f x %.2f x %.2f  y %.2f..%.2f  winding %d/%d"
          % (label, len(pos), len(tri), hi[0]-lo[0], hi[1]-lo[1], hi[2]-lo[2], lo[1], hi[1],
             agree, agree + disagree))
    return dict(pos=pos, nrm=nrm, uv=uv, tri=tri, ta=ta, lo=lo, hi=hi)


def write_mesh(parts, out, shape, materials):
    """Write one shape holding `parts` sub-meshes, in order; index N is parts[N]."""
    body = b"@@b@" + prop_i("pdxasset", [1, 0])
    body += obj_node(1, "object")
    body += obj_node(2, shape)
    for part, mat in zip(parts, materials):
        ctr = (part["lo"] + part["hi"]) / 2.0
        radius = float(np.linalg.norm(part["pos"] - ctr, axis=1).max())
        body += obj_node(3, "mesh")
        body += prop_f("p", part["pos"])
        body += prop_f("n", part["nrm"])
        body += prop_f("ta", part["ta"])
        body += prop_f("u0", part["uv"])
        body += prop_i("tri", part["tri"])
        body += prop_f("boundingsphere", [ctr[0], ctr[1], ctr[2], radius])
        body += obj_node(4, "aabb")
        body += prop_f("min", part["lo"])
        body += prop_f("max", part["hi"])
        body += obj_node(4, "material")
        body += prop_s("shader", mat["shader"])
        body += prop_s("diff", mat["diff"])
        body += prop_s("n", mat["normal"])
        body += prop_s("spec", mat["spec"])
    body += obj_node(1, "locator")
    open(out, "wb").write(body)
    return body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("obj")
    ap.add_argument("out")
    ap.add_argument("--shape", default="eotg_markerShape")
    ap.add_argument("--diffuse", default="eotg_marker_diffuse.dds")
    ap.add_argument("--normal", default="nonormal.dds")
    ap.add_argument("--specular", default="noproperties.dds")
    ap.add_argument("--shader", default="standard", choices=sorted(MESH_SHADERS),
                    help="the material shader name baked into the .mesh. Leave it at 'standard'; "
                         "a custom effect belongs in the .asset, not here (see MESH_SHADERS)")
    ap.add_argument("--scale", type=float, default=1.0)
    ap.add_argument("--drop-y", type=float, default=0.0,
                    help="subtract this from Y; use the model's min Y to sit it on the ground")
    ap.add_argument("--flip-winding", action="store_true")
    ap.add_argument("--flip-v", action="store_true")
    ap.add_argument("--verify", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="write even if the winding check fails")
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

    agree, disagree = check_winding(pos, nrm, tri)
    if disagree > agree and not a.force:
        sys.exit(
            "\nWINDING IS INVERTED: %d of %d triangles are wound against their own normals.\n"
            "The engine would backface-cull this mesh and draw nothing, which looks exactly\n"
            "like a missing file. Re-run with --flip-winding, or --force to write it anyway."
            % (disagree, agree + disagree))

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
    print(f"  boundingsphere r={radius:.3f}   winding {'FLIPPED' if a.flip_winding else 'as authored'}"
          f"   faces agreeing with their normals {agree}/{agree + disagree}")

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
