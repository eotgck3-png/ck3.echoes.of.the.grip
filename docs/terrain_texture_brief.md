# Terrain texture brief — regeneration round 2

A spec for generating the 26 terrain textures for a Crusader Kings III total conversion whose map
is deep space. Self-contained: no prior context needed.

---

## 1. The goal

Produce 26 seamlessly tileable images that read as **regions of a galaxy** and that **sit together
as one coherent map** rather than as 26 separate pictures.

Each image is a *material* that CK3 paints across whole regions of the map. It is a **background
substrate**, not an illustration. The interesting things on screen — glowing travel lanes, realm
borders, stations — are drawn on top by the game. The terrain's job is to be readable, calm, and
distinguishable, and then get out of the way.

---

## 2. The one hard rule

> ### No point stars. No isolated bright specks. Continuous fields only.

This is not a stylistic preference. It is a hard technical constraint, and round 1 failed on it:
**25 of 26 images were unusable** because of it.

**Why.** CK3 tiles each texture ~337 times across the map and views it minified — roughly **5–9
source pixels collapse into every screen pixel**. Content that is *uniform* averages to the same
value regardless of how it lands on the pixel grid, so it stays stable. A sparse scatter of
very bright points averages to a *different* value per pixel depending on sub-pixel alignment, so
it sparkles when still and crawls when the camera moves. Mipmapping then averages the stars away
entirely while leaving the noise behind in the transition.

Measured, on the two properties that govern this:

| | local contrast | peak / mean |
|---|---|---|
| CK3's own shipped terrain (grass, rock, sand) | **0.06** | **0.3** |
| Round 1 starfield images | **1.20** | **13.1** |

20× and 40× over. No amount of blurring, darkening or processing fixes this — those only trade the
stars for mud. The content type has to change.

**Stars are handled separately.** They are drawn procedurally by the game's shader, at a stable
screen scale, so they stay crisp at every zoom and never alias. Do not put them in the texture.

---

## 3. What to make instead

Build every texture from **continuous, cloudy, connected fields**:

- nebula gas and dust
- haze, murk, fog banks
- dense particulate clouds
- soft mottling and marbling
- large soft voids *between* cloud masses

Think **weather map, smoke, ink in water, satellite cloud photography** — not night sky.

Variation should be **smooth and large-scale**. Bright areas may exist, but they must be *broad
soft regions*, never points, and never more than ~3× the image's average brightness.

---

## 4. Minimum requirements

### Hard gates — the pipeline cannot fix these

| Requirement | Limit | Why |
|---|---|---|
| **Local contrast** | **< 0.35** | fine detail amplitude vs local brightness — this is what shimmers |
| **Peak / mean** | **< 3.0** | the brightest 0.1% must not tower over the average |
| **Tiling** | **< 2.0** | must be seamless; use `--tile` in Midjourney |
| **Repeat risk** | **< 0.25** | no single dominant shape, or it grids across the map |
| **Resolution** | **≥ 1024×1024**, square | array requirement downstream |
| **Format** | PNG, RGB | |

### Handled automatically — do not spend effort on these

Brightness, saturation, contrast, colour grading, height maps, normal maps, roughness/metalness,
resizing, DDS conversion, mipmaps. The importer normalises all of it into a shared band so the
26 read as one map. **An image that is too bright or too colourful is fine. An image made of
points is not.**

### Naming
Filename must exactly equal the material id: `eotg_hills_01.png`.

---

## 5. Look at these first

Four images from round 1 already meet the spec. They are the target — study them before generating:

| File | Local contrast | Why it works |
|---|---|---|
| `eotg_drylands_02.png` | **0.20** | pure dust haze, no points at all — the single clean pass |
| `eotg_mountains_02.png` | 0.16 | dense opaque nebula, stars dimmed inside the gas |
| `eotg_mountains_01.png` | 0.24 | same, slightly brighter |
| `eotg_jungle_01.png` | 0.33 | chaotic gas, points subdued into the murk |

And the worst offenders, to recognise the failure mode: `eotg_desert_02` (1.90),
`eotg_plains_01` (1.64), `eotg_oasis_01` (1.17). All are beautiful images. All are starfields.

---

## 6. Prompts

Append to every prompt:

```
seamless tileable texture, continuous nebula gas and dust, smooth cloudy variation,
no stars, no bright points, no specks, even mid-tone, low contrast, soft and diffuse,
top-down flat lighting, no horizon, no focal subject
--tile --ar 1:1
```

The negatives matter as much as the subject. If the result has visible individual stars, reject it.

### The 26 files

Terrains with several variants need visibly different images that still share an identity.

**High-area terrains — these cover most of the map, keep them calmest**

| File | Terrain | Brief |
|---|---|---|
| `eotg_plains_01/02/03` | Open Cluster | very faint thin dust, almost empty, the calmest texture of all; open and navigable |
| `eotg_hills_01/02` | Broken Cluster | uneven clumpy dust with soft dark gaps, fragmented and irregular |
| `eotg_desert_01/02` | Barren Reach | nearly featureless thin haze, vast emptiness, cold and desaturated |
| `eotg_mountains_01/02` | Nebula Barrier | dense opaque violet nebula wall, thick and impassable |
| `eotg_taiga_01/02` | Frozen Cluster | cold blue-white frozen haze, pale icy fog |
| `eotg_drylands_01/02` | Arid Reach | warm brown-grey dust and thin haze, dry and depleted |
| `eotg_forest_01/02` | Dense Cluster | thick crowded gas, densely packed and complex, busy but soft |
| `eotg_steppe_01/02` | Frontier Reach | thin pale open haze, remote and sparse |

**Low-area terrains — one each, may be a little more characterful**

| File | Terrain | Brief |
|---|---|---|
| `eotg_jungle_01` | Nebula Wilds | chaotic rose and violet cloud, tangled and turbulent |
| `eotg_desert_mountains_01` | Barren Barrier | dark dense dust clouds, harsh and impassable, very dark |
| `eotg_wetlands_01` | Anomaly Fields | swirling distorted gas, lensing ripples, unstable teal and green |
| `eotg_farmlands_01` | Fertile Reach | rich warm golden gas, glowing softly, abundant |
| `eotg_floodplains_01` | Volatile Cluster | turbulent orange gas, churning and unstable |
| `eotg_oasis_01` | Sanctuary Systems | a soft calm warm glow, gentle and sheltered |
| `eotg_terraced_hills_01` | Layered Cluster | banded layered dust in soft strata, interconnected pockets |
| `eotg_edge_01/02` | System Edge | soft gradient from lit gas into empty void (01 violet-lit, 02 gold-lit) |

---

## 7. Checking before delivery

```
python docs/tools/import_terrain_textures.py <mod root> <your folder> --check
```

Writes nothing; scores every image and prints a verdict. Deliver only images reporting **GOOD**.
`local_contrast` and `peak_ratio` are the two to watch — if either FAILs, the image has points in
it and must be regenerated, not adjusted.

---

## 8. Priority

`plains` and `hills` are ~31% of the map between them and set its whole character — get those
right first. `oasis`, `farmlands` and `floodplains` are each under 0.5% and can be done last.
