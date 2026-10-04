# Holding marker models — what the pipeline accepts

Seven models, one per holding type. Every number here is measured from the current pipeline
(`docs/tools/obj_to_pdxmesh.py`, `build_marker_mesh.py`, `build_marker_assets.py`) or from vanilla
CK3 1.19, not estimated.

---

## The one that matters most: detail is mostly wasted

**Design for silhouette.** The emblem slot renders at `EOTG_MARKER_EMISSIVE 0.82` — 82% of the lit
result is discarded and replaced with flat colour × 1.45 gain. Almost nothing that surface shading
would normally show you survives that.

Concretely, all three of these are thrown away:

| | why |
|---|---|
| **Texture detail** | the diffuse is a **single flat colour** per holding type, generated in code. UVs are read but the texture has no content to sample. |
| **Normal maps** | the asset binds `nonormal.dds`. There is no normal map slot in use. |
| **Fine surface relief** | washed out by the emissive flattening, then again by bloom. |

What *does* read: the outline against a dark map, the overall proportions, and large openings that
let the background through. A model that is distinctive in silhouette and plain on the surface will
look better here than a detailed one — the detail is not merely wasted, it muddies the outline.

There can be **up to 14,153 markers** on the map (vanilla `definition.csv` row count), typically
drawn at roughly 40–80 px tall. Assume the reader is seeing an icon, not a model.

---

## Format

Plain `.obj`. The parser is deliberately strict in one place and forgiving everywhere else.

- **Triangulate.** Any face with a corner count other than 3 aborts the build with
  `face with N corners: triangulate the .obj first`. Quads are not accepted.
- **Export normals (`vn`). Not optional in practice.** A missing normal silently becomes
  `(0, 1, 0)`. Nothing errors — but the winding check is then measured against straight-up
  normals and becomes meaningless, and the rim outline and beam both shade from the normal, so
  the marker comes out flat and wrong in a way that is hard to trace back.
- **UVs (`vt`) optional.** Missing ones default to `(0, 0)`. Harmless today, since the diffuse is
  a flat colour. Include them anyway if it is free — it costs nothing and leaves the door open.
- `o`, `g`, `s`, `usemtl`, `mtllib` lines are ignored. One object per file; no material splitting.
- No `.mtl` needed. Colour comes from the pipeline, not the model.

## Orientation and origin

- **Y-up.**
- **Centre on X and Z at the origin.** The beam sizes itself from `max(hypot(x, z))`, so a model
  authored off to one side produces a beam that is off-centre and too wide.
- **Y position is free.** The builder drops the model's lowest point and re-lifts it, so every
  holding floats the same `0.336` above the plinth regardless of where you authored it.

## Size

Author to roughly the current emblem's envelope and nothing needs rescaling:

| | source units | ×1.44 in world |
|---|---|---|
| current emblem | 1.141 × 1.712 × 1.141 | 1.64 × 2.46 × 1.64 |
| **target** | **≤ 1.15 wide, ≤ 1.75 tall** | ≤ 1.66 × 2.52 |
| radius from the Y axis | **≤ 0.57** | ≤ 0.82 |

For context, the plinth it stands on is 4.08 wide × 2.49 tall with a top face of radius 1.26, and
the whole marker is currently 4.08 × 5.29 × 4.08. Vanilla `building_western_castle_01` is
2.77 × 4.16 × 2.17, so the marker is already the larger object — growing it further is not free.

If a model is easier to author at some other scale, send it as-is and say so; `--emblem-scale` is
a per-build flag and I can set it per holding, or add normalisation so authored scale stops
mattering. Do not rescale by hand to hit the table above.

## Triangle budget

Measured from vanilla meshes and ours:

| mesh | tris |
|---|---|
| `building_western_feast_01` (vanilla) | 958 |
| `building_mena_feast_01` (vanilla) | 1,256 |
| `fp4_healers_camp_01_a` (vanilla) | 2,196 |
| `fp4_pyre_01_a` (vanilla, top end) | 3,874 |
| current emblem alone | 1,672 |
| `eotg_marker.mesh`, all three slots | 2,728 |

**Target ≤ 2,000 triangles per holding model. Hard ceiling 4,000**, which is vanilla's own top end
for a single building. Given the emissive flattening, spending triangles on surface detail buys
nothing — spend them on the outline.

## Winding

Faces must be wound **outward** (counter-clockwise seen from outside). This is checked, not
trusted: `check_winding()` compares every face's cross product against its authored normal and
**refuses to write the mesh** if more disagree than agree. An inverted model is invisible in game,
which looks exactly like a missing file — this project has already lost time to that once.

If a model comes out inverted the build says so and names the file; `--flip-winding` fixes it
without re-exporting. This is also the reason `vn` matters: no normals, no check.

---

## Delivering them

Seven files, in `gfx/models/buildings/eotg_markers/`, named for the holding-type keys the asset
generator already uses:

```
eotg_marker_castle.obj
eotg_marker_city.obj
eotg_marker_temple.obj
eotg_marker_temple_citadel.obj
eotg_marker_tribal.obj
eotg_marker_nomad.obj
eotg_marker_herder.obj
```

Matching those stems means mesh and colour pair up without a second mapping table to keep in sync.

### What adapts automatically

- The **projector beam** takes its radius from each model's own radius and its height from the
  hover gap, so a wider or narrower model gets a correctly fitted beam with no edit.
- The **plinth** is shared and unchanged.
- The **hover gap** is measured to each model's base, so all seven float identically.

### Two open questions for when they land

1. **Is colour still wanted?** Seven distinct silhouettes may make the seven colours redundant.
   Keeping both is the safer start and flattening later is easy.
2. **Whole marker or emblem only?** These slot in as the emblem above a shared plinth. If any is
   meant to *replace* the plinth too, the beam and the `Properties.r` emissive mask both need
   authoring per model — say so and it is a different job.
