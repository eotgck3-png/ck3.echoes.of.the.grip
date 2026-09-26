# Terrain materials — asset spec and pipeline

How CK3 terrain is layered, what art the mod needs, and how the placeholder pipeline works.
Built 2026-09-24 against CK3 1.19.0.6. Gate 4 (presentation) work; see `docs/stellar_rivers_shader.md`
for the rest of the space-map pass.

## How CK3 layers terrain

Per pixel, top to bottom:

| Layer | File | Role |
|---|---|---|
| Material set | `materials.settings` | Names each material's `diffuse` / `normal` / `material` (properties) DDS + its mask |
| Which materials | `detail_index.tga` (map-res RGBA) | Each channel holds a **material index** — 4 candidate materials per pixel |
| How much of each | `detail_intensity.tga` (map-res RGBA) | The 4 matching weights |
| Blend | `detail_data.settings` → `"materials_limit": 4` | Samples those 4, tiled ~337x across the map, and **height-blends** them |
| Global tint | `colormap.dds` | One map-res image tinting everything — the cheapest source of regional colour variation |
| Overlays | snow, province effects, borders, FoW, lighting | Snow and weather visuals are disabled (see the shader doc) |

`materials.settings` has **two top-level blocks**: masked textures, then a second block for unmasked
textures that vanilla ships empty (`{
}`). Both are required — omitting the second produces
`No section for unmasked textures` and the file fails to parse.

Material indices are **positional** in `materials.settings`. The five dynamic materials
(`drought`, `drought_cracks`, `flood`, `summer_grass`, `winter_effect`) must stay first and in
that order — vanilla's own comment says so. Their effects are disabled in
`province_effects.fxh` / `dynamic_masks.fxh`, so they point at neutral textures and never draw.

**Visual terrain and gameplay terrain are separate systems.** Looks come from the above;
combat/supply/movement come from `common/province_terrain/`. They only need to agree for the
player's sanity, not for the engine.

## Asset spec (per material)

| File | Spec | Contents |
|---|---|---|
| `<id>_diffuse.dds` | 1024x1024, DXT5, full mip chain | RGB colour, **ALPHA = height** (drives the 4-way height blend) |
| `<id>_normal.dds` | same | **DXT5nm / RRxG**: G = normal.x, A = **-**normal.y, Z reconstructed (see `UnpackRRxGNormal`). *Not* a standard RGB normal map. |
| `<id>_properties.dds` | same | **G** = specular, **B** = metalness, **A** = roughness (R unused) |

Must be seamlessly tileable. Vanilla ships `normal_neutral.dds` and `material_neutral.dds`, so a
flat material can reuse those and ship diffuse only.

> **Every detail texture must be 1024x1024 DXT5 with a full 11-level mip chain.** CK3 loads them into
> a **texture array**, and every slice must share resolution, format and mip count — *including any
> vanilla texture you reference*, such as the `normal_neutral.dds` / `material_neutral.dds` used by
> the dynamic slots (both 1024). Generating placeholders at 512 crashed the game on load:
> `CreateTexture2D failed on: DXT5/512x512[31] — D3D: The parameter is incorrect`, preceded by one
> `in texture array has inconsistent properties` line per material. There is no partial failure mode
> here; one odd-sized texture takes down the whole array.

### Authoring rules that matter
The 4 slots are **not** layers stacked to build up a look. `CalcHeightBlendFactors` is a
winner-takes-most competition resolved per pixel by the **diffuse alpha**: with equal weights and
heights 0.9 vs 0.1 the result is 100%/0%, and a material at 20% weight with equal height contributes
*nothing*. Two materials only coexist in a narrow band (`detail_blend_range = 0.25`).

So **one material = one complete, standalone, tileable surface.** Consequences:
- Put high alpha on raised/dominant features and low in recesses, or every terrain boundary becomes a
  flat linear cross-fade instead of an interlocking edge.
- Keep each texture **low contrast at tile scale**. The main detail path samples with plain
  `PdxTex2DGrad` - no anti-tiling - so at ~337x repeat any strong one-off feature reads as a grid.
  Landmarks belong in map objects, not terrain textures.
- **No feature may touch two opposite edges of the tile.** Anything spanning edge to edge joins with
  its own copy in the neighbouring tile and becomes one unbroken line across the entire map. This
  shipped once: full-height lane lines produced vertical rails over the whole of Europe.
- Use per-material `tile_factor` (vanilla default 337.5; vanilla itself uses 200/500/900) so two
  variants of similar art read at different scales. The generator sets these.
- High-area terrains stay dark and low contrast (they are the backdrop for the glowing lanes and
  borders); rare, notable ones (Relay Nexus, Trade Corridor, Resource Corridor) may be brighter.

## The EotG terrain set

**26 materials (78 texture files)**, with variant count weighted by map area — repetition only
shows where a terrain is widespread, so plains gets 3, the mid-sized terrains 2, and the rare ones 1.
Names follow `docs/terrain_scheme.md`.

| CK3 terrain | EotG name | Variants | Placeholder look |
|---|---|---|---|
| plains | Open Cluster | **3** | sparse scattered stars, faint dust, near black |
| hills | Broken Cluster | **2** | stellar debris and rock between irregular stars |
| desert | Barren Reach | **2** | a very few isolated stars in vast darkness |
| mountains | Nebula Barrier | **2** | dense violet nebula wall, stars dimmed inside it |
| taiga | Frozen Cluster | **2** | icy fragments, pale frost-lit, dim blue stars |
| drylands | Arid Reach | **2** | warm brown dust and haze, scattered stars |
| forest | Dense Cluster | **2** | many bright stars packed close, thin gas |
| steppe | Frontier Reach | **2** | widely spaced pale stars, thin faint dust |
| jungle | Nebula Wilds | **1** | chaotic rose/violet gas, stars half-hidden |
| desert_mountains | Barren Barrier | **1** | dark dust and sparse debris, almost no stars |
| wetlands | Anomaly Fields | **1** | concentric lensing rings, teal phenomena |
| farmlands | Fertile Reach | **1** | dense warm golden stars, soft warm gas |
| floodplains | Volatile Cluster | **1** | flaring orange stars, energetic gas |
| oasis | Sanctuary Systems | **1** | a small calm pocket of warm golden stars |
| terraced_hills | Layered Cluster | **1** | star pockets between raised bands of dust |
| — | System Edge | **2** | land/void boundary, replaces vanilla's beach family |

Names and concepts are canonical in **`docs/terrain_scheme.md`** (2026-09-25), which supersedes the
v1 `needed_art_terrains.txt`. Terrain describes **astrography** — star density, nebula density,
debris, phenomena — never stations, wreckage or city lights, which belong to holdings and map
objects. Material ids stay keyed to the **vanilla** terrain key, so the rename costs no id churn.

## Tools

```
python docs/tools/build_terrain_materials.py <mod root>                    # placeholder art
python docs/tools/build_terrain_index.py     <mod root> [--game <dir>]     # paint onto a map
python docs/tools/build_colormap.py          <mod root> [--drift 0.045]    # neutral colormap
python docs/tools/import_terrain_textures.py <mod root> <img dir> [--seamless] [--check]
```

**Replacing a placeholder with real art** needs no code: drop an image named after the material id
(`eotg_hills_01.png`) into a folder and run `import_terrain_textures.py`. It centre-crops, resizes
to 1024, derives the height from luminance, generates the DXT5nm normal, takes spec/metal/rough from
the material's placeholder entry, and writes all three DDS files with the correct mip chain.
`--check` scores how well each image tiles before you commit; `--seamless` repairs one that does not.
Prompts for generating the art are in `docs/terrain_texture_prompts.md`.

1. **`build_terrain_materials.py`** — generates the 78 placeholder DDS files and writes
   `materials.settings`. Recipes are procedural (noise, scattered masses, slabs, lanes, crystal,
   gas) parameterised per terrain; edit the `TERRAINS` table to retune variant counts, colours,
   `contrast` and `tile`.
2. **`build_terrain_index.py`** — paints materials onto a map. Reads `provinces.png` +
   `definition.csv` + `common/province_terrain/` + `default.map` (for water), resolves ids to
   indices from `materials.settings`, and writes `detail_index.tga` / `detail_intensity.tga`.
   Variant lists are **discovered** from `materials.settings` (not assumed), so changing a terrain's
   variant count needs no edit here. Regions pick an adjacent pair of variants and blend within it by
   low-frequency noise, so a 3-variant terrain varies across the map while never using more than two
   of the four slots.

Point `--game` at the mod's own `map_data/` once it exists and the same script produces the real
thing — the vanilla-map output is throwaway, the script is not.

## Repo policy
`materials.settings` is committed. The DDS, the `masks/`, and the two `.tga` bakes are
**gitignored** (~390 MB, all regenerable in two commands). See `gfx/map/terrain/README.md`.

## Load-time failures hit while building this (all fixed)
| Symptom in `error.log` | Cause | Fix |
|---|---|---|
| `CreateTexture2D failed on: DXT5/512x512[31]`, many `inconsistent properties` lines, **crash on load** | Detail textures are a texture array; placeholders were 512 while vanilla's neutral textures are 1024 | Generate at 1024 (now the enforced default) |
| `No section for unmasked textures ... materials.settings` | Missing the second, empty top-level block | Generator emits it |
| `File '...' should be in utf8-bom encoding` | Plain-text config written without a BOM | BOM added to the defines / settings / environment files |
| `Invalid number of max particles ( 0 )` | Disabled particles used `max_particles=0` | `max_particles=1` with the emitter disabled |
| *(no error)* terrain tinted green/tan/white like Earth | Vanilla `colormap.dds` soft-lighting over the materials | Generate a neutral colormap (sRGB 186) |
| *(no error)* saturated orange haze over the ocean at distance | `relative_fog_color = { 0.6 0.2 -0.2 }` is **added** to `fog_color`; harmless over vanilla's blue fog, orange over our near-black one | `relative_fog_color = { 0 0 0 }` |
| *(no error)* long vertical streaks across the whole map | `lanes()` drew lines spanning the full tile height; tiled ~337x they join into continuous rails | Lanes are now **segments** strictly inside the tile, each with its own vertical span |
| *(no error)* solid bright teal polygons inland | Shore detection compared the heightmap to the **global** `_WaterHeight`; the 232 lake meshes sit at their own elevation, so every sample read as land and `rim` saturated | `EotgLandAt` takes the local water surface (`WorldSpacePos.y`) |
| *(no error)* coastlines banding into an oil-slick rainbow | Shore hue varied too fast in world space | `EOTG_HUE_SPREAD` 0.45 -> 0.28, `EOTG_HUE_REGION_SCALE` 0.0006 -> 0.00018 |

## Masks vs detail_index — resolved
`detail_index.tga` / `detail_intensity.tga` **are** authoritative at runtime. Confirmed in game
2026-09-24: terrain renders exactly as baked while the mod ships only 64x64 black dummy masks.
The masks are editor data; they must exist because `materials.settings` names them, but their
content is not read at load. Full-resolution masks are therefore not needed.

## The colormap
`colormap.dds` is soft-light blended over the blended detail materials:

    Diffuse = SoftLight( DetailDiffuse, ToLinear(colormap), (1 - properties.R) * COLORMAP_OVERLAY_STRENGTH )

with `ToLinear = pow(x, 2.2)` and `COLORMAP_OVERLAY_STRENGTH = 1.0`. `SoftLight(Base, 0.5) == Base`,
so the no-op value is **linear 0.5 = sRGB 186**. Vanilla's colormap is the green-Europe /
tan-Sahara / white-Alps tint and will soft-light straight over the EotG materials, recolouring them
back toward Earth — this was exactly what the first in-game test showed.

`docs/tools/build_colormap.py` writes a near-neutral replacement (centred on 186, ±0.045 drift
toward gold/violet on a low-frequency field) so the galaxy keeps regional character without the
materials being recoloured. Resolution is free — the shader samples it with normalised UVs — so it
is generated at half map size (4608x2304) rather than vanilla's 9216x4608.

**Per-material escape hatch:** opacity is `(1 - properties.R)`, so a material with **R = 255 ignores
the colormap entirely**. The generator currently writes R = 0 (full influence).

## Holding ground decals
CK3 blends a ground decal under every holding (`decal_local` shader, 357 holding assets). On the
vanilla map it is grass and dirt; against the void it reads as a bright green island and is the most
visible medieval tell once the terrain goes dark.

Only **5 decal textures** exist in the whole game, so the fix is contained:
`docs/tools/build_holding_decals.py <mod root> [--tint violet|gold|neutral] [--darken 0.45]`
desaturates and darkens the diffuse while preserving luminance structure and the alpha (which is the
decal's shape), and leaves normal/properties as vanilla - only the colour was wrong. Output is
256x256 DXT5 with 9 mips, matching the source exactly. Measured: western_city went
`(87, 99, 56)` olive -> `(26, 22, 36)` violet.

The **buildings themselves** are separate: they share per-graphical-culture texture atlases
(`building_western_atlas_diffuse.dds`, 131 KB, covers every western castle/city/temple). Retexturing
that one file would restyle all western holdings with no modelling - not yet done.

## Next
- Real textures at 1024 — map-independent, can be commissioned in parallel with Gate 1.
- Masks painted against the mod's own map, at Gate 1, with the cartographer.

## Terrain effects: kinds vs parameters

An effect is a **kind** - a shape-generating primitive in `pdxterrain.shader` - plus **parameters**,
which live in the `FX` presets in `docs/tools/build_terrain_hybrid.py`. A terrain row names a preset
(`fx="gaswall"`), not a magic number.

| kind | primitive | used by |
|---|---|---|
| 1 | shard - Voronoi ridge, masked into floes | Frozen Cluster |
| 2 | splat - rotated gaussians, sparse | Volatile Cluster |
| 3 | rings - lensing + starlight warp | Anomaly Fields |
| 4 | bands - warped sine field | Nebula Barrier (gas), Layered Cluster (strata) |
| 5 | filament - ridged, domain-warped noise | Nebula Wilds |

This matters for cost. Before, the effect id *was* the terrain's identity, so every new effect meant
editing the shader in four places and every terrain needed its own id. Now, **adding a terrain that
reuses a kind is one table row and no shader edit at all**; only a genuinely new shape costs shader
work, which is where that cost belongs. Kinds 4 and 5 already prove it: gas and strata were two
hard-coded effects that turned out to be the same field with a different direction and shaping.

Slots are packed `ModA.xyzw` = kinds 1-4 and `ModB.xyzw` = kinds 5-8, so there is room for three
more kinds before the packing has to grow.

**Parameters are not blended between two terrains sharing a kind.** Each kind takes them from
whichever material is heaviest at that pixel; only the *weight* cross-fades. Blending them would
produce a shape belonging to neither terrain.

### Terrain-derived gates

Two different questions, deliberately kept separate:

| gate | signal | cost | use for |
|---|---|---|---|
| `height=(lo,hi,floor)` | absolute altitude, 0..1 | 1 tap | how **high** the ground is |
| `slope=(lo,hi,floor)` | local gradient magnitude | 4 taps | how **broken** the ground is |

Both ramp the effect from `floor` strength at `lo` to full at `hi`, and `(0,0,0)` disables them.
The gradient is computed once per pixel and only when some active effect asks for it - either via
`slope`, or via `q[2]` contour alignment on kind 4.

`q[2]` on kind 4 rotates the bands toward the local contour (0 = use the fixed `p` direction,
1 = fully along the contour), so bands wrap around high ground instead of cutting across it.

Current assignments:

| terrain | effect | gate | why |
|---|---|---|---|
| Nebula Barrier | gaswall | height 0.12-0.34, contour 0.5 | gas thickens with altitude and banks along the ridge; passes stay readable |
| Barren Barrier | dustwall | height 0.10-0.30, contour 0.4 | the dust equivalent, drier and darker |
| Frozen Cluster | crystal | height 0.08-0.30 | ice gathers on high ground |
| Broken Cluster | debris | slope 0.12-0.55 | rubble where the ground is actually fragmented |
| Layered Cluster | strata | slope 0.10-0.45, contour 0.85 | strata follow the landform, and only where there is one |
| Nebula Wilds | filament | none | the thicket is not a landform effect |

Broken Cluster is the second-largest terrain (6.2%), so `debris` reuses the **filament** kind with a
broad, low-thinness setting - a 3-FBM field that mottles into chunks - rather than a sprite field,
whose 9-cell loop would be an order of magnitude more expensive across that much of the map.

### Cell-based effects must vary per anchor

Kinds 2 (splat) and 3 (rings) place features on a jittered grid. Jittering *position* is not
enough: if every feature is the same size, shape, spacing and brightness, the eye reads the repeat
instantly and the whole field looks like one decal stamped over and over. Anomaly Fields shipped
like that - identical teal circles, same radius, same ring spacing - and looked pasted on.

Everything that can vary now varies, all from the anchor's own hash, so it costs a few ALU and no
extra fetches:

| | rings (kind 3) | flares (kind 2) |
|---|---|---|
| radius / size | 0.62-1.38x | 0.65-1.35x |
| shape | ellipse, 0.68-1.32 aspect, own rotation | rotation (already) |
| ring spacing | 0.70-1.45x | - |
| brightness | 0.55-1.00x | 0.55-1.00x |
| phase | random | random |
| colour | lerped across a hue range per anchor | - |

The extra hashes needed *before* the reach test (radius, ellipse) are the only ones paid by
anchors that turn out not to reach the pixel; spacing, brightness, phase and hue are computed
after both cheap rejections.

### Motion

`EOTG_MOD_ANIMATE` (default 1) adds time to two effects: rings drift in phase at a per-anchor
signed rate, so anomalies breathe independently rather than in lockstep, and flares flicker, which
is what Volatile Cluster is supposed to be doing. **Set it to 0 if the shader fails to compile** -
`GlobalTime` is declared by includes this shader shares with `pdxwater.shader`, but it is the one
symbol used here that was not already proven in the terrain pass. With it off, both effects stay
varied, just static.

### Why terrain boundaries look blocky, and the jitter that fixes it

`DetailIndexTexture` holds material **ids**, so it has to be point-sampled - you cannot
interpolate between index 7 and index 9 and get anything meaningful. Boundaries therefore land on
axis-aligned map-texel edges. Vanilla gets away with this because the blocks are hidden behind
high-frequency tiled detail textures; this mod replaced those with a flat tint, so the raw texel
grid became visible as soon as you zoomed in.

`EOTG_BLEND_JITTER` (in texels) offsets the lookup by value noise, so the stair-steps become
irregular organic edges. **The noise is sampled in texel space**, not world space:
`EOTG_BLEND_JITTER_SCALE` is in cycles per texel and has to be around 1 or more. The first attempt
sampled it in world space at 0.22, which varied over several texels and therefore slid whole
boundaries sideways while leaving them just as blocky. Two octaves, because one alone gives a
smooth wobble rather than a ragged edge. The boundary still falls in the same place on average - it just
stops being a grid. Past about 1.5 texels, single pixels start defecting to the neighbouring
terrain and it reads as speckle instead of a coastline.

This is a per-pixel cost on all terrain (two value-noise samples), which is why the noise is a
single octave rather than FBM.

### Two different fixes for terrain edges

They solve different problems and you need both:

| | what it does | what it cannot do |
|---|---|---|
| `EOTG_BLEND_JITTER` | makes the edge **ragged** instead of a grid staircase | widen the transition - it moves the edge, it does not soften it |
| `EOTG_BLEND_SOFT_R` | makes the colours **fade** into each other over N texels | hide the texel grid on its own |

The mask carries barely a texel of blend, so there is no wider transition hiding in the texture to
recover: a gradient has to be *built* by averaging the neighbourhood. `EotgTintAt` is one tap of
colour, and the tint is the average of five - centre plus a four-tap cross whose orientation is
random per pixel. A fixed cross this small shows as a four-lobed smear; rotating it per pixel means
neighbouring pixels cover different directions and together they average to a disc.

Only the **tint** is blurred. Structure, stars and effects stay on the single centre tap - blurring
those would smear effects across borders rather than fade colours. The blur rides the same distance
fade as the effects, so it costs nothing at strategic zoom where texels are sub-pixel anyway.

### Relief shading is the main shape cue

`EOTG_SHADE[n]` (per terrain, 0 = flat) applies a directional hillshade from the height gradient:
slopes facing `EOTG_SHADE_DIR` brighten, slopes turned away darken. The engine does light the
terrain normals already, but this mod replaces the detail textures with a flat tint and then adds
effects on top, which washes that lighting out - which is why a mountain range read first as a
contour map and then as fog. An explicit term puts the shape back.

Give it only to terrains that ARE a landform (mountains 0.55, desert_mountains 0.45, hills 0.33,
terraced 0.30, taiga 0.28). Everything meant to read as an open region stays at 0, or the whole map
turns into a relief chart.

`EOTG_SHADE_GAIN` converts raw gradient into a usable range and is calibrated together with
`EOTG_GRAD_GAIN` - both are guesses until the real heightmap exists.

The gradient is now computed once per land pixel whenever effects are in range (`fade > 0.01`),
rather than being conditional on which effects want it: shading needs it almost everywhere that
matters, and the branch was no longer paying for itself.

### Making a landform legible

Two mechanisms, both driven by the single height sample the terrain path already takes:

**Altitude banding** (`q[2:4]` = frequency, amount, kind 4 only). Blends the band coordinate from
world space toward altitude. At amount 1 the bands are iso-elevation lines, so the field traces the
landform: a peak becomes nested rings, a ridge becomes strata following its spine. Nebula Barrier
runs at 0.45 with 38 bands across the height range.

The first attempt ran this at 0.85 with 105 bands and a near-white hypsometric crown, which read as
an *ink-on-paper topographic map* - hard black contour rings against white peaks - rather than as
gas. Three things caused that and all three matter: the band count was too high, the dark floor
(`dark`) was 0.22 so the gaps went almost black, and the high-altitude tint was nearly white. The
fix was to raise the dark floor to 0.58, cut the gain, and pull the crown back to a mid violet.
**If a banded effect starts looking like a contour map, `dark` is usually the culprit before the
band count is.**

**Hypsometric ramp** (`ALT` table). The terrain's own tint shifts toward a second colour as altitude
rises - Nebula Barrier goes from deep violet in the valleys to a pale lit crown on the peaks. This
makes height readable from colour, not just from lighting, which is what stops a range reading as a
flat wash. Set the amount to 0 for terrains meant to read as flat regions; it is for landforms.

Neither uses the gradient, so neither can produce the direction noise that the contour-alignment
attempt did.

> **Gradient-direction alignment was tried and removed.** It shipped once at
> 0.4-0.85 and tiled the map with moire: `EOTG_GRAD_EPS` was 1.0 world units, so both gradient taps
> landed inside a single heightmap texel and returned quantisation noise, and normalising that into
> a band direction gave every texel its own orientation. EPS is now 8.0 and the rotation fades out
> on flat ground, but do not re-enable it until the gradient has been checked against the real
> heightmap - a wrong direction field is far more visible than a wrong magnitude.
>
> **Noise-kind `scale` must stay in the 0.045-0.075 band.** The proven effects sit there. Filament
> shipped at 0.16 and debris at 0.42 - 2x and 8x too fine - and aliased badly under minification,
> which is the same failure that paused the texture pipeline in the first place. Check
> `scale * p[0]` (the effective frequency), not just `scale`.
>
> **Watch additive brightness:** an effect's peak is `gain * EOTG_MOD_GAIN` (1.6). Anything with
> its own bright colour over a broad field needs a much lower gain than a sparse one - filament at
> 0.75 put 1.2 of saturated pink on top of an already-saturated terrain and blew out the whole
> Nebula Wilds region.

> **All height- and slope-derived numbers are provisional.** `map_data/` has no heightmap yet, so
> they are tuned against the *vanilla* map and will need redoing once the real one exists. The two
> shader constants behind them, `EOTG_GRAD_EPS` and `EOTG_GRAD_GAIN`, set the tap spacing and
> normalise raw gradient into the 0..1 range the `slope` numbers assume - calibrate those first,
> then the per-terrain bands.

### Height coupling
Any preset may set `height=(lo, hi, floor)` in 0..1 heightmap units: the effect runs at `floor`
strength at height `lo` and full strength at `hi`. Nebula Barrier uses it, so the gas wall thickens
over high ground and thins in the passes - the chokepoints read as gaps you could move through
rather than as more wall. **The (lo, hi) band is map-specific and needs tuning against the real
heightmap**; the shipped 0.12/0.34 is a first guess at where sea level and ridgeline sit.

Cost: one extra multisampled height fetch, only for effects that enable it.

### Distance fade
Everything early-outs past `EOTG_MOD_FADE_FAR + RANGE` (440 + 170 world units), including the lens
field, which the caller now skips entirely when faded. At strategic zoom effects cost nothing.

## Previewing an effect before it ships

`docs/tools/preview_terrain_fx.py` reimplements the shader's own noise and effect maths in numpy,
runs it over the **real** CK3 heightmap, and scores the result against the aliasing gates in
`terrain_texture_brief.md` (`local_contrast < 0.35`, `peak_ratio < 3.0`) plus a sub-pixel crawl
test. It exists because the shader cannot be compiled here, and three shipped changes in a row came
back wrong in ways that were all predictable on paper.

It validates itself: the `current` panel reproduces the banding-over-relief look seen in game, so
the model can be trusted for a like-for-like comparison.

What it does **not** model: engine lighting, the colormap soft-light, and the detail-texture
structure. Read the output as the effect's contribution, not as a screenshot. The one free variable
is world units per heightmap pixel (`--wpp`), which is the same unknown that makes every
height-derived constant provisional.

    python docs/tools/preview_terrain_fx.py            # current vs candidate density shapes
    python docs/tools/preview_terrain_fx.py --wpp 0.5,1,2

### What it found about the nebula proposal

Measured on real relief, against the current look:

| | local contrast | peak | crawl | density response to camera |
|---|---|---|---|---|
| current bands | 0.046 | 1.11 | 0.0120 | n/a (view independent) |
| billow, gain 0.55 | 0.043 | 0.59 | **0.0029** | **0.85** |
| soft, gain 0.55 | 0.053 | 0.65 | 0.0064 | 0.94 |

Two things the preview caught that would otherwise have shipped:

1. **A ridged density field reads as lace, not gas.** `1 - |2n-1|` draws thin bright filaments in
   closed loops - the exact shape of the first attempt, and nothing like a nebula.
2. **Gain saturation kills parallax.** At the originally proposed 1.25, 94% of pixels sat above
   0.5 density: a uniform wash with no dynamic range, so the layers had nothing left to reveal as
   they slid. View response collapsed from 0.85 to 0.10. **Coverage has to stay near 0.15-0.40**,
   and that single number controls both whether it looks like a cloud and whether it moves.

### Saturation is the recurring failure, in three places now

Every "harsh black and white" report so far has been the same mistake: a signal mapped so steeply
that it spends most of its range against a limit, which turns a gradient into two flat values with
a hard edge between them.

| where | symptom | what fixed it |
|---|---|---|
| gas `dark` at 0.22 | contour-map rings | raise the floor |
| nebula density gain 1.25 | uniform wash, parallax dead (94% above 0.5) | cut gain to 0.55 |
| hillshade gain 220 with a hard clamp | solid black and white faces either side of every ridge | compress instead of clip |

Measured on real relief, the heightmap has median slope 0.0011 and p99 0.025 - a 20x spread. Any
*linear* mapping that is visible on gentle ground is therefore far past the rail on a mountain.
`EotgHillshade` now uses `x / (1 + |x|)`, which approaches the limit asymptotically: railed pixels
went from 8.6% to 0%, and the luminance swing from 6.8x to 4.65x.

**Contrast also compounds.** Hillshade and the gas bands multiply, so each looking acceptable alone
is not enough - the bands were imposing 2.43x on top of the shading and are now at 1.75x. When
checking a change, check the product.

### Tiling: the detail texture repeats, and on empty terrain you can see it

`tile_factor` repeats each structure texture across the map (260-600 times). Vanilla hides that
behind busy, high-frequency art; these textures are deliberately smooth low-contrast cloud, and on
a large terrain with no effect and almost no stars there is nothing left to hide the grid. The
Sahara showed it plainly - the same motif stamped in rows.

`EOTG_TILEBREAK[n]` mixes world-space FBM into the sampled detail. Noise in world space cannot
repeat, so the correlated part of the signal is diluted in proportion to the mix. Measured
autocorrelation at the tile period:

| mix | autocorrelation | reads as |
|---|---|---|
| 0.0 | 0.999 | wallpaper |
| 0.4 | 0.809 | grid clearly visible |
| 0.6 | 0.459 | grid still visible |
| 0.8 | 0.103 | broken up |

So **anything below about 0.65 does not solve it** - the first pass at 0.35-0.60 would have looked
barely different. The big empty terrains now sit at 0.70-0.85.

It uses a single FBM: what breaks a repeat is the *proportion* of uncorrelated signal, not how many
octaves it has, and this runs on most of the land.

Terrains with their own effect or dense stars (jungle, mountains, wetlands, floodplains, farmlands,
oasis, terraced) are left at 0 - their own content already breaks the tile, and this is not free.

### Kind 6: a nebula that is not a texture

Nebula Barrier runs on kind 6 rather than the band field. Three things make it behave like a
volume rather than a decal, none of which a flat 2D field can fake:

- **Parallax.** Three layers are offset against the view direction, so they slide over each other
  as the camera moves. Layer altitude scales with terrain height, so the effect is strongest over
  the tallest ground and the gas reads as sitting *above* the range.
- **Front-to-back compositing.** A near layer occludes a far one instead of averaging with it.
- **Grazing thickening.** Looking straight down you see through it; at a shallow angle you are
  looking through more of the volume, so it thickens. CK3's camera pitches as it zooms, so this
  responds continuously.

Plus emissive cores where the densest layer peaks - embedded stars lighting the gas from inside,
which is what reads as *dense* rather than as mist.

Measured with the shipped parameters against the real heightmap:

| | value | note |
|---|---|---|
| dense fraction | 0.26 | target 0.15-0.40; above that it saturates |
| view response | 0.852 | 0 would mean it is still just a texture |
| local contrast | 0.029 | gate < 0.35 |
| peak ratio | 0.448 | gate < 3.0 |
| sub-pixel crawl | 0.0028 | the band field it replaced was 0.0120 |

It is *steadier* than what it replaces, despite moving with the camera.

**`q[0]` (density gain) is the load-bearing number.** At 1.25, 94% of pixels sit above 0.5 density:
the field flattens to a wash and the parallax dies with it, because a saturated field has no
dynamic range left to reveal as it slides. Keep it near 0.55.

### Impassable provinces ARE Barren Barrier

`build_terrain_index.py` forces every province listed as `impassable_mountains` in `default.map`
onto the `desert_mountains` material, overriding whatever terrain it actually carries. So that one
entry is both Barren Barrier *and* every wasteland on the map - the Persian and steppe blanks
included. Changing it changes both, which is usually what you want, since they are the same idea.

It reads as dark rust on the dense nebula kind rather than as dark grey. "Recede, do not draw the
eye" was the original intent and it was right, but dark *grey* reads as unfinished rather than as
hostile; dark *rust* recedes just as well and looks deliberate.

Giving wastelands their own material instead would mean adding a key to `TERRAINS` **and** to the
separate list in `build_terrain_index.py`, then rebuilding the 170 MB index - worth knowing, but
not worth it while the two want to look alike.

### Peaks shift hue, not lightness

Three attempts at making summits read as different:

| | result |
|---|---|
| lighter lavender, 1.58x peak luminance | washed out - looked like the effect petering into grey |
| darker violet, 0.91x | barely distinguishable |
| **magenta at 1.21x, hue 258 -> 290** | reads as the gas getting hotter where it is thickest |

Lightness alone cannot carry this, because the hillshade is already using lightness for shape and
the two fight. Hue is a free channel.

### A feature belongs to the terrain it sits on, not the pixel being shaded

Stars were sliced in half across terrain borders. `EotgStars` took density and brightness from the
*shading pixel*, and those feed the sparsity threshold, the radius and the brightness - so a star
straddling a boundary had its existence, its size and its brightness each decided differently on
the two halves.

`EotgStarLayer` now calls `EotgStarParamsAt( starPos )` and reads the terrain **under the star**.
This is the same fix, for the same reason, as the lens rings gating on their own anchor - that
comment has been in the file all along, and stars needed it too.

The pattern generalises: **any effect that places a discrete feature must sample terrain at the
feature's anchor.** Per-pixel sampling is only correct for continuous fields (the bands, the
nebula, the tint), where there is no feature to cut.

Cost is controlled by ordering, exactly as in the lens: the conservative radius test uses
`EOTG_RADIUS_HI` and rejects before paying for the fetch, so only pixels that actually have a star
nearby (~30%) pay for one. The old early-out on pixel density had to go - it *was* the bug - and
removing it costs little because no terrain has zero density anyway.

### Flat-topped bands read as stripes

`EotgFxBands` with `grain = 0` takes the `smoothstep(0.22, 0.78)` branch: flat-topped bands with
clean corridors. On Layered Cluster that read as hard light/dark/light stripes (reported as an
"inverse oreo"). Turning grain on moves it to the noise-modulated branch, which breaks the layering
up along its length so it is a texture rather than a pattern. Contrast came down at the same time
(`dark` 0.26 -> 0.74, swing 2.43x -> 1.78x). Reach for grain before reaching for the band count.

### Pick the primitive from the concept, not from a cost guess

Broken Cluster is *"scattered systems, stellar debris"* - discrete chunks. It shipped on the
filament kind, a continuous noise field, which can only produce mottle. The reason given was cost,
on the assumption that a 3x3 sprite loop is dearer than a noise field. That was backwards:

| | hashes per pixel |
|---|---|
| filament: 3 x `EotgFbm`, each 3 octaves x 4 hashes | **36** |
| splat: 9 cells, most rejected on their first hash | **~17** |

`EotgFbm` is not cheap. A cell loop that rejects early usually beats it. Measured on real relief
the sprite version has identical crawl (0.0061) at higher local contrast (0.037 -> 0.083, gate
0.35) - and the higher contrast is the point, since debris should read as chunks.

Layered Cluster moved from world-space bands to **altitude** banding (`q[2:4]`), so its layers are
drawn by the landform. It is the one terrain named for elevation variation and it was the last one
still banding across the map regardless of shape. Grain stays on, because flat-topped altitude
bands are just hard contour lines - the same failure the gas wall had.

Neither change touched the shader. Both kinds already existed; only the parameter table moved.

### Two effects can use the same primitive and must not look the same

Debris on Broken Cluster read in game as "hills have more stars than everything else". Its star
density is 0.48, identical to plains - the extra points of light were the debris itself.

The sprite was 1.17:1 (round) with a 0.35 cross term, and that cross draws a perpendicular streak
through the sprite. A round dot with a cross through it is how you draw a star. Fixed by shape,
not brightness: 4:1 shards with no cross, which cannot be read as a point of light, and the sprite
already rotates per anchor so they lie at every angle.

Worth knowing about the dispatch while tuning this: `mul *= lerp( 1, lerp( DARK, 1, f ), w )`
darkens where the effect is ABSENT, so every effect is emissive by construction and its features
are always brighter than their surroundings. A "dark rubble" look is not reachable by lowering
gain - it needs an invert flag in the dispatch. Shape is the free axis; brightness is not.

### Hypsometric ramps are for landforms, and hills is not one

Hills ramped to warm tan at altitude, added when every terrain needed height legibility. It was the
source of the muddy patches reported first in the Alps and again as tan showing up inside mountain
ranges - hills sits interleaved with mountains all through a range, and tan is the one earth colour
on a violet map. Relief shading carries its form perfectly well alone. Mountains, Barren Barrier
and Frozen Cluster keep theirs: they are actual landforms whose altitude means something.
