# Asset manifest — Echoes of the Grip (space map)

A handoff spec for producing art assets. Self-contained: you do not need the design history.

**Project:** a Crusader Kings III total conversion that renders the map as deep space. Land is
navigable space; the sea is void; rivers are glowing energy lanes. The rendering pipeline is
finished — what is missing is art.

**The single most important thing to understand:** you are producing **flat, tileable, dark
background textures**, not illustrations. Every texture repeats roughly **337 times** across the
map. Anything that reads as a picture will read as wallpaper.

---

## Priority 1 — Terrain textures (26 images)

### What to deliver
**26 PNG files.** That is the entire deliverable for this section. Normal maps, height maps,
roughness/metalness, DDS conversion and mipmaps are all **generated automatically** from your
image — do not produce them.

- **Format:** PNG, RGB
- **Size:** square, **1024×1024 minimum** (larger is fine, it gets centre-cropped and resized)
- **Must tile seamlessly.** If generating with Midjourney, use the `--tile` flag.
- **Filename = material id exactly.** `eotg_hills_01.png`. A wrong name is rejected.

### The 26 files

Terrains with multiple variants need visibly different images that still share an identity —
they are mixed across the map to stop large regions looking repetitive.

| Filename | Terrain name | Brief |
|---|---|---|
| `eotg_plains_01.png` | Open Cluster | sparse evenly scattered stars in open dark space, very faint dust, no obstacles, almost black, extremely subtle |
| `eotg_plains_02.png` | " | as above, even fewer stars |
| `eotg_plains_03.png` | " | as above, slightly more stars, faint dust lanes |
| `eotg_hills_01.png` | Broken Cluster | fragmented region of scattered stellar debris and rocky fragments between irregular star systems, uneven distribution, dark void between the rubble |
| `eotg_hills_02.png` | " | smaller, denser debris |
| `eotg_desert_01.png` | Barren Reach | almost entirely empty space, a very few isolated faint stars separated by vast darkness, no gas, no debris, cold and desaturated, near black |
| `eotg_desert_02.png` | " | emptier still |
| `eotg_mountains_01.png` | Nebula Barrier | dense opaque violet nebula wall, thick radiation clouds blocking the view, only a few stars dimly visible through the gas, imposing and impassable |
| `eotg_mountains_02.png` | " | thicker and darker, fewer stars |
| `eotg_taiga_01.png` | Frozen Cluster | cold blue-white region of icy bodies and frozen debris, pale frost-lit fragments, dim blue stars, hostile and cold |
| `eotg_taiga_02.png` | " | darker, more rock among the ice |
| `eotg_drylands_01.png` | Arid Reach | dry dusty region of space, warm brown-grey dust and thin haze, a scattering of isolated stars, depleted |
| `eotg_drylands_02.png` | " | dustier, fewer stars |
| `eotg_forest_01.png` | Dense Cluster | densely packed star cluster, many bright stars crowded close together, high system density, thin gas between them |
| `eotg_forest_02.png` | " | slightly fewer but larger stars |
| `eotg_steppe_01.png` | Frontier Reach | open remote space beyond the established routes, widely spaced pale stars, thin faint dust, empty and peripheral |
| `eotg_steppe_02.png` | " | sparser and paler |
| `eotg_jungle_01.png` | Nebula Wilds | vast chaotic nebula wilderness, dense unpredictable clouds of rose and violet gas, isolated stars half-hidden in the murk |
| `eotg_desert_mountains_01.png` | Barren Barrier | harsh empty barrier region, dark dense dust clouds and sparse debris, almost no stars, very dark |
| `eotg_wetlands_01.png` | Anomaly Fields | field of gravitational anomalies, concentric distortion rings and lensing arcs warping the starlight, unstable teal and green phenomena |
| `eotg_farmlands_01.png` | Fertile Reach | rich region dense with warm golden stars, many habitable systems close together, soft warm gas, abundant |
| `eotg_floodplains_01.png` | Volatile Cluster | cluster of unstable flaring stars, bright orange stellar flares and energetic gas, turbulent |
| `eotg_oasis_01.png` | Sanctuary Systems | a small pocket of calm favourable space, warm golden stars clustered together, gentle glow, surrounded by darkness |
| `eotg_terraced_hills_01.png` | Layered Cluster | layered stellar geography, stars gathered into interconnected pockets separated by raised bands of dust, constrained winding corridors between them |
| `eotg_edge_01.png` | System Edge | boundary between a lit region of space and the empty void, scattered small rocks and dust catching light, fading into blackness — **violet-lit** |
| `eotg_edge_02.png` | " | same, **gold-lit** |

### Subject-matter rule
These describe **astrography**, not civilisation. Build them from **star density, nebula density,
debris, and phenomena**.

**Do not include** stations, ships, wreckage, cities, buildings, roads, or any lights of
habitation. Those are separate map objects. A "Fertile Reach" is fertile whether or not anyone
lives there.

### If using Midjourney
Append to every prompt:
```
seamless tileable texture, top-down orthographic view of deep space, flat even lighting,
no horizon, no planet surface, no focal subject, dark low-contrast game terrain material
--tile --ar 1:1
```

### Quality bar — this is measurable, not subjective

A validator scores every image. Run it before delivering:

```
python docs/tools/import_terrain_textures.py <mod root> <your folder> --check
```

| Metric | Target | Meaning |
|---|---|---|
| tiling | < 2.0 | seam mismatch vs the image's own detail. Over ~6 = visible grid |
| repeat_risk | < 0.25 | big-shape energy × contrast — what actually reads as a grid |
| detail | > 0.004 | fine local variation; this becomes the height map |
| brightness | < 0.35 | mean luminance. Terrain is the backdrop |
| contrast | < 0.45 | p5–p95 luminance spread |
| lighting | < 0.10 | baked directional gradient / implied sun |
| saturation | < 0.55 | colour intensity of lit pixels |

`FAIL` on any metric = will look broken. Deliver only images reporting **GOOD** or
**USABLE (with warnings)**.

**The governing idea:** *a good terrain texture is fine detail with a flat large-scale average.*

Eyeball checks if you cannot run the validator:
- Squint. Obvious shapes surviving = too blobby.
- Any sense of "the sun is over there" = baked lighting, reject.
- Anything your eye lands on will appear ~337 times.
- Most AI space art is far too bright for a backdrop.
- At 100% zoom there must still be fine detail; a smooth gradient yields no height map.

### Where the work matters most
`plains` (25% of all land) and `hills` (6%) set the tone of the entire map. `oasis`, `farmlands`
and `floodplains` are each under 0.5% and can be done last.

---

## Priority 2 — Holding building textures (optional, high impact)

Holdings (castles, cities, temples) are still medieval stone and thatch. They share
**per-culture texture atlases**, so restyling them needs **no 3D modelling** — replacing one
atlas restyles every holding of that culture.

| File | Size | Covers |
|---|---|---|
| `building_western_atlas_diffuse.dds` | 131 KB, 512×512 | every western castle, city, temple, wall |
| `building_western_atlas_normal.dds` | 512×512 | " |
| `building_western_atlas_properties.dds` | 512×512 | " |

Source: `gfx/models/buildings/holdings/atlas/western/`. Equivalent folders exist for `mena`,
`mediterranean`, `indian`, `asian`, `mongol`, `persian`, `tibet`.

The atlas is a packed sheet of building materials — stone blocks, timber, roof tiles, thatch,
plaster. Deliver a **same-layout** replacement in sci-fi materials: dark hull plating, panel
seams, emissive strips, worn metal. **The layout must match exactly** — UVs are baked into the
meshes. Work over the original as a template.

Deliver as PNG at 512×512; DDS conversion is handled.

**Already done, do not redo:** the ground decals blended under each holding have been recoloured
from grass to dark violet (`docs/tools/build_holding_decals.py`).

---

## Priority 3 — Terrain icons (15 images)

Small UI icons shown in province tooltips and the terrain map mode.

- **Format:** PNG with alpha, **40×40**
- **Filenames:** `eotg_terrain_<terrain>.png` using the CK3 terrain keys listed in the table
  above (`plains`, `hills`, `mountains`, `desert`, `desert_mountains`, `oasis`, `jungle`,
  `forest`, `taiga`, `wetlands`, `steppe`, `floodplains`, `drylands`, `terraced_hills`,
  `farmlands`)
- Must be legible at 40px — strong silhouette, 2–3 tones, no fine detail
- Subject: the same astrographic idea as the matching texture

---

## Priority 4 — Battle backgrounds (15 images, lowest priority)

Widescreen art behind the battle UI. Vanilla placeholders work fine until these exist.

- **Format:** PNG, **1920×540**
- One per terrain, same naming basis as the icons
- These *are* illustrations — perspective, drama and lighting are wanted here, unlike the textures
- Subject: a fleet engagement in that terrain

---

## What is generated — do not produce these

| Asset | Produced by |
|---|---|
| Normal maps (DXT5nm/RRxG packing) | `import_terrain_textures.py` |
| Height maps | derived from image luminance |
| Roughness / metalness / specular | per-material presets |
| All DDS conversion and mipmaps | the tools |
| `colormap.dds` | `build_colormap.py` |
| `detail_index.tga` / `detail_intensity.tga` | `build_terrain_index.py` |
| Terrain material definitions | `build_terrain_materials.py` |

## Ingestion

Terrain textures:
```
python docs/tools/import_terrain_textures.py <mod root> <folder of PNGs>
```
Add `--seamless` if an image does not already tile. The tool centre-crops, resizes to 1024,
derives the height map, generates the normal map, applies the material's surface presets, and
writes three DXT5 files with full mip chains.

**Hard engine constraint:** every terrain texture ends up in a single GPU texture array, so all
of them must share resolution, format and mip count. The tools enforce 1024×1024 DXT5 with 11
mips. A mismatch crashes the game on load — this is why source images must be at least 1024
square.

## Reference
- `docs/terrain_scheme.md` — canonical terrain names and full descriptions
- `docs/terrain_texture_prompts.md` — prompts and quality criteria in full
- `docs/terrain_materials.md` — how CK3 layers terrain, and the asset spec in technical detail
