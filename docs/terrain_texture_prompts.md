# Terrain textures — Midjourney prompt pack

Prompts for the 26 EotG terrain materials, written from the **2026-09-25 terrain scheme**
(`docs/terrain_scheme.md`), which supersedes the v1 `needed_art_terrains.txt`.

Generate, drop the files in a folder, run one command.

## 1. Settings

Append this to every prompt:

```
seamless tileable texture, top-down orthographic view of deep space, flat even lighting,
no horizon, no planet surface, no focal subject, dark low-contrast game terrain material
--tile --ar 1:1
```

- **`--tile` is the important one.** It makes Midjourney produce a seamless tile. Without it the
  texture shows a visible grid across the whole map, and the importer's `--seamless` repair costs
  sharpness.
- `--ar 1:1`. Any resolution — the importer centre-crops and resizes to 1024.
- Output **PNG**, named exactly after the material id (`eotg_hills_01.png`).

## 2. The visual language

The scheme describes **astrography, not civilisation** — terrain is explicitly decoupled from
development ("high natural potential, not high existing development"). So every texture is built
from the same four ingredients, varied in density and colour:

| Ingredient | Reads as |
|---|---|
| **Star density** | how many systems are here |
| **Nebula density** | how hard it is to see and move through |
| **Debris / rock** | fragmented, irregular routes |
| **Phenomena** (lensing, flares, ice) | the specific hazard |

Do **not** prompt for stations, ships, wreckage, cities or lights-of-civilisation. Those belong to
holdings and map objects; a Fertile Reach is fertile whether or not anyone lives there.

## 3. Will my image work? — run the checker

```
python docs/tools/import_terrain_textures.py <mod root> <folder> --check
```

It writes nothing and scores every image:

```
  eotg_hills_01.png   source 1456x816   ->  UNUSABLE
      tiling          7.808  FAIL   wrap seam vs internal detail
      repeat_risk     0.088   ok    big shapes x contrast - what actually reads as a grid
      detail          0.052   ok    local variation available for the height map
      brightness      0.283   ok    mean luminance - terrain is the backdrop
      contrast        0.237   ok    p5-p95 luminance spread
      lighting        0.160  warn   baked directional gradient / horizon
      saturation      0.216   ok    colour intensity of the lit pixels
      resolution        816  warn   short side under 1024; will be upscaled and soft
      -> fix: tiling
```

Thresholds are calibrated so that **all 26 shipped placeholders pass**. `FAIL` means it will
actually look broken; `warn` means a real cost you may be accepting deliberately.

### The one idea behind all of it

**A good terrain texture is fine detail with a flat large-scale average.**

The texture repeats ~337× across the map. Anything large — a dominant nebula shape, a brightness
gradient, a memorable feature — repeats into a visible grid. Fine local variation does not, and it
is exactly what the height map needs to make terrain boundaries interlock instead of cross-fade.

### What each number means

| Metric | Want | Why it matters |
|---|---|---|
| **tiling** | < 2 | Difference across the wrap seam, relative to the image's own detail. Over ~6 and you see a grid. `--tile` in Midjourney fixes this at source. |
| **repeat_risk** | < 0.25 | Big-shape energy × contrast. A big shape is only a problem if it also has contrast — which is why nebula terrains (legitimately blobby) still pass. |
| **detail** | > 0.004 | Local variation. This becomes the height map. Too flat and terrain edges cross-fade into mud instead of interlocking. |
| **brightness** | < 0.35 | Terrain is the backdrop; the lanes, borders and coastlines carry the image. Midjourney defaults far brighter than this. |
| **contrast** | < 0.45 | Large luminance swings read as a grid at tiling scale. |
| **lighting** | < 0.10 | A best-fit brightness ramp across the image — i.e. baked sun or a horizon. CK3 lights terrain itself, so baked lighting fights the game's sun from every angle. |
| **saturation** | < 0.55 | Of the lit pixels. Rare terrains (Volatile, Anomaly, Frozen) are allowed to run hotter. |

### Judging by eye, if you'd rather not run it

- **Squint at it.** If it still has obvious shapes, it is too blobby. It should go almost uniform.
- **Look for a light source.** Any sense of "the sun is over there" is baked lighting — reject it.
- **Is there one thing your eye goes to?** That thing will appear ~337 times.
- **Is it dark?** Most Midjourney space art is far too bright for a backdrop.
- **Zoom to 100%.** There should still be fine detail; a smooth gradient gives you no height map.

## 4. Prompts

> **Under the hybrid pipeline, colour in these prompts is art direction, not output.** The three
> shared structure textures are greyscale; each terrain's colour, cloud amount, star density and
> feature scale come from the `TERRAINS` table in `docs/tools/build_terrain_hybrid.py`. Read the
> prompts for *character* (wall vs thicket, debris vs dust), and change the table for *colour*.
> After any table change run `python docs/tools/check_terrain_distinctness.py`, which scores all
> 105 pairs and fails on a collision. The palette is deliberately spread: the 15 terrains were
> once crowded into 3 hue families and several pairs were indistinguishable in game.

`_01` is the base. For `_02` / `_03` variants rerun with the bracketed change, or use Midjourney's
*Vary* — each variant gets a different `tile_factor`, so similar art still reads at a different scale.

### High-area terrains — keep these very dark and quiet

**`eotg_plains_01/02/03` — Open Cluster** *(25% of all land; the quietest thing on the map)*
> sparse evenly scattered stars in open dark space, very faint dust, no obstacles, almost black, extremely subtle, minimal detail
> *(02: even fewer stars. 03: slightly more stars, faint dust lanes)*

**`eotg_hills_01/02` — Broken Cluster**
> fragmented region of scattered stellar debris and rocky fragments between irregular star systems, uneven distribution, dark void between the rubble
> *(02: smaller, denser debris)*

**`eotg_desert_01/02` — Barren Reach**
> almost entirely empty space, a very few isolated faint stars separated by vast darkness, no gas, no debris, cold and desaturated, near black
> *(02: emptier still)*

**`eotg_mountains_01/02` — Nebula Barrier** *(a **wall**: large, smooth, solid, cold, starless)*
> vast smooth wall of deep indigo-violet gas, one enormous unbroken mass filling the frame, cold and opaque, no stars visible at all, soft slow gradients with no fine detail, imposing and impassable
> *(02: darker and flatter still)*

> **Must not converge with Nebula Wilds (jungle).** These two read as the same purple cloud in
> game. Keep Barrier **cold** (indigo, no red), **low frequency** (few huge shapes), **starless**,
> and **large scale**; Wilds is warm, fine, star-flecked and small scale. Hue, temperature,
> luminance, feature scale and star density all have to differ — any one of them alone is not
> enough at terrain minification.

**`eotg_taiga_01/02` — Frozen Cluster**
> cold blue-white region of icy bodies and frozen debris, pale frost-lit fragments, dim blue stars, hostile and cold
> *(02: darker, more rock among the ice)*

**`eotg_drylands_01/02` — Arid Reach**
> dry dusty region of space, warm brown-grey dust and thin haze, a scattering of isolated stars, low resources, sun-scorched and depleted
> *(02: dustier, fewer stars)*

**`eotg_forest_01/02` — Dense Cluster**
> densely packed star cluster, many bright stars crowded close together, high system density, thin gas between them, crowded and complex
> *(02: slightly fewer but larger stars)*

**`eotg_steppe_01/02` — Frontier Reach**
> open remote space beyond the established routes, widely spaced pale stars, thin faint dust, empty and peripheral, unclaimed
> *(02: sparser and paler)*

### Low-area terrains — one each; these may be brighter and should draw the eye

**`eotg_jungle_01` — Nebula Wilds** *(a **thicket**: fine, tangled, warm, star-flecked)*
> tangled thicket of warm rose and crimson gas filaments, many thin interwoven strands at small scale, no blue or violet anywhere, numerous dim stars showing through the gaps between strands, chaotic and overgrown
>
> Counterpart to Nebula Barrier (mountains) — see the warning under that entry. Warm hue only; if
> any violet creeps in, the two terrains stop being tellable apart.

**`eotg_desert_mountains_01` — Barren Barrier**
> harsh empty barrier region, dark dense dust clouds and sparse debris, almost no stars, hostile and impassable, very dark

**`eotg_wetlands_01` — Anomaly Fields**
> field of gravitational anomalies, concentric distortion rings and lensing arcs warping the starlight, unstable teal and green phenomena, unpredictable

**`eotg_farmlands_01` — Fertile Reach**
> rich region dense with warm golden stars, many habitable systems close together, soft warm gas, abundant and inviting, high natural potential

**`eotg_floodplains_01` — Volatile Cluster**
> cluster of unstable flaring stars, bright orange stellar flares and energetic gas, productive but dangerous, turbulent

**`eotg_oasis_01` — Sanctuary Systems**
> a small pocket of calm favourable space, warm golden stars clustered together, gentle glow, sheltered and safe, surrounded by darkness

**`eotg_terraced_hills_01` — Layered Cluster**
> layered stellar geography, stars gathered into interconnected pockets separated by raised bands of dust, constrained winding corridors between them, naturally defensible

**`eotg_edge_01/02` — System Edge** *(the land/void boundary; replaces vanilla's beaches)*
> boundary between a lit region of space and the empty void, scattered small rocks and dust catching light, fading out into blackness
> *(01: violet-lit. 02: gold-lit)*

## 5. Importing

```
python docs/tools/import_terrain_textures.py <mod root> <folder of images> [--seamless]
```

- `--check` scores how well each image tiles and writes nothing. Under ~2 tiles cleanly, over ~6
  will show a visible grid.
- `--seamless` repairs a non-tiling image. Only needed if you forgot `--tile`.
- `--contrast X` overrides the per-material contrast reduction.
- Wrongly-named files are skipped and the valid ids listed.

Import writes the three DDS files with the correct packing straight into `gfx/map/terrain/`.
Nothing else needs regenerating — `materials.settings` and the terrain index already use these ids.

## 6. Loop

1. Generate a few candidates for one terrain.
2. `--check`, import the best.
3. Launch, look, iterate.

Start with **Open Cluster** and **Broken Cluster** — plains and hills are ~31% of all land between
them and set the tone of the whole map. Sanctuary Systems and Fertile Reach are under 0.5% each and
can wait.
