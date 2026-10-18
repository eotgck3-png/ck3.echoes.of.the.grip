# Map terrains and shaders

How the space map is actually rendered, as of 2026-10-15. Read this before touching anything in
`gfx/FX/` or `docs/tools/build_terrain_*`.

`docs/pitfalls.md` is the companion: this file says how the system works, that one says how it
breaks. Neither repeats the other.

---

## The one change that invalidates the older docs

The map originally needed **26 hand-made tiling textures**, one or more per terrain. It does not
any more. `docs/asset_manifest.md` and `docs/terrain_texture_brief.md` still describe that
pipeline and are **obsolete for terrain** — do not commission art from them.

**Why it changed.** Terrain is tiled ~337 times across the map and viewed minified, roughly 5–9
source pixels per screen pixel. Point stars baked into a texture average differently depending on
sub-pixel alignment, so they sparkle when still and crawl when the camera moves. Measured: round-1
starfield textures had local contrast **1.20** and peak/mean **13.1** against vanilla terrain's
**0.06** and **0.3** — 20× and 40× over. That is a property of the content type, not a tuning
problem, and 25 of 26 textures failed on it.

**What replaced it.** One shared source image bakes into three low-contrast "structure" textures
used by *every* terrain. Everything that distinguishes terrains is generated in the shader, at a
stable world scale, where it cannot alias.

So: **terrain art is one image, not fifteen.**

---

## How a terrain gets its look

Five axes, all driven from one table (`TERRAINS` in `docs/tools/build_terrain_hybrid.py`):

| axis | source | notes |
|---|---|---|
| **tint** | per terrain | the dominant read; the structure texture is greyscale and gets tinted |
| **structure amount** | per terrain | how much of the shared cloud texture shows, 0 = flat tint |
| **stars** | per terrain | density, mean size, brightness, colour temperature, and the *shape* of each distribution |
| **effect** | per terrain | one procedural "kind" (nebula, bands, filaments, floes…) |
| **tile scale** | per terrain | `tile_factor`, how often the structure texture repeats |

A sixth, **secondary effect**, is rare by design — see below.

### Terrain is unlit

`EOTG_TERRAIN_EMISSIVE` replaces the sun entirely. Vanilla multiplies terrain by a ×8 warm-white
sun; here the albedo goes straight to screen, so the table's numbers are what you see. Everything
downstream was retuned for a near-black map — see `pitfalls.md` §5, because this is the single
most common cause of "why is this effect so loud".

### Stars are procedural and deterministic

`EotgStarHash` is a pure function of world position. No time input, no seed, no per-machine
state — every player sees the same stars in the same places. Three rules that must not be undone
(also in `pitfalls.md` §8):

- **Terrain is sampled at the STAR's position, not the pixel's.** The per-pixel version cut stars
  in half at terrain borders.
- **One continuous world lattice.** Density varies *occupancy*, never cell size; scaling the cell
  stretches the lattice across every boundary.
- **No per-terrain seed.** It would change the lattice at borders — the exact province-seam
  artifact the design forbids.

Size is independent of density, so a sparse terrain can still have large stars. That matters:
Barren Reach is meant to read as *isolated*, not *featureless*.

---

## The 15 terrains

`impassable` is a render-only material slot, not a CK3 terrain. The mod defines no
`common/terrain_types/` and reuses vanilla's 15 keys.

| CK3 key | EotG name | Tint | Core idea | What the shader draws |
|---|---|---|---|---|
| plains | **Open Cluster** | `#6a7290` | accessible, few hazards | mid stars, no effect, rare strands |
| hills | **Broken Cluster** | `#85796a` | fragmented, irregular | debris, rare strands |
| desert | **Barren Reach** | `#3f4a62` | sparse, inhospitable | very few stars but **large** |
| mountains | **Nebula Barrier** | `#5c3f9e` | chokepoint barrier | dense nebula, few small dim stars |
| taiga | **Frozen Cluster** | `#8fc0e0` | cold, hostile, high potential | crystalline pack-ice floes |
| drylands | **Arid Reach** | `#a8874a` | arid, not undeveloped | dry dust |
| forest | **Dense Cluster** | `#90a0b8` | many systems packed | **most stars, all small** |
| steppe | **Frontier Reach** | `#8ea8ae` | remote, peripheral | thin strands, sparse |
| jungle | **Nebula Wilds** | `#d05c86` | dense, mysterious, dangerous | tangled filaments |
| desert_mountains | **Barren Barrier** | `#6b3a32` | sparse hostile barrier | dead nebula, rare strands |
| wetlands | **Anomaly Fields** | `#3fbfb0` | unpredictable hazards | lensing rings that **bend the star field** |
| farmlands | **Fertile Reach** | `#ffc861` | high natural potential | max stars, large and bright |
| floodplains | **Volatile Cluster** | `#e08a45` | potential with instability | anisotropic flares |
| oasis | **Sanctuary Systems** | `#fff2e4` | favourable pocket | brightest on the map, few very large stars |
| terraced_hills | **Layered Cluster** | `#5d7f8a` | layered, defensive | banded strata |
| *(impassable)* | **Impassable Barrier** | `#6b3a32` | not navigable | dead nebula + strata; **~21% of the map** |

"Core idea" is the owner's, from `docs/terrain_scheme.md` — that file remains canonical for naming
and intent. Land percentages live there too.

**Impassable matters more than its row suggests.** `build_terrain_index.py` forces every
`impassable_mountains` province to this material, which is about a fifth of the map. Before that
fix those provinces inherited whatever terrain they happened to carry — 502 of them fell through
to `plains`, and 19 to `farmlands`, so impassable wasteland was being drawn as Fertile Reach at
full star density.

### Distinctness is fragile

Run `docs/tools/check_terrain_distinctness.py` after any edit to the table. Terrains were once
crowded into three hue families and collided in pairs. The **effect** axis is the strongest
separator: when it was audited, every terrain carrying an effect cleared the threshold and every
weak pair either lacked one or shared one.

---

## The effect registry

`FX` in `build_terrain_hybrid.py` maps a name to a *kind* (the shape-making code in the shader)
plus parameters. Kinds are implemented in `pdxterrain.shader`; adding a parameter set is cheap,
adding a kind is not.

| kind | fx entries using it |
|---|---|
| splat | `flare`, `debris`, `dust`, `iceshard`\* |
| bands | `strata`, `gaswall`\*, `dustwall`\* |
| nebula | `nebula`, `nebula_dead`, `haze` |
| filament | `filament`, `strands` |
| floe | `packice` |
| lens | `lens` |
| cluster | `pleiades`\* |

\* defined but currently unused — available without new shader code.

Effects **darken as well as add**. An additive-only effect reads as haze laid on top; structure
needs bright cores *and* dark voids. Each returns a 0–1 field: the bright end is emitted, the dark
end multiplies the base down.

### Secondary effects are deliberately rare

A terrain may declare a second, weakened effect. Two things make it work:

- **The cap is baked at generation**, not enforced at runtime: gain ×0.35, darkening pulled 70%
  toward neutral. It cannot be bypassed.
- **Rarity is spatial, not per-province** — a large-scale noise field covering ~11.5% of area.
  Keying it to province ids would put the effect's edges exactly on province boundaries, which is
  the seam the star lattice was rebuilt to avoid.

Mechanically, every `EOTG_FX_*` array is doubled to `2N`; an index of `t + N` reads the secondary,
so the dispatch code needed no changes at all. A secondary must be a **different kind** from the
primary — they share a slot, and the heavier weight wins. The generator aborts if you try.

---

## Beyond terrain

The same map pass handles several other systems. All are full-file vanilla overrides.

| file | what it does |
|---|---|
| `pdxterrain.shader` | terrain, stars, effects, coast shelf, borders, altitude banding |
| `pdxwater.shader` | void ocean, nebula, shore glow, navigable rivers |
| `river_surface.shader` | the gold/violet "stellar wind" lanes |
| `river_bottom.shader` | `clip(-1)` — discards the riverbed |
| `surroundmap.shader` | beyond the map edge |
| `clouds.fxh`, `dynamic_masks.fxh`, `paper_transition.fxh`, `province_effects.fxh` | weather, snow, paper-map transition, province effects — mostly gutted |

**Coast.** The land side was once a 1.8-unit painted band with no effect while the water side
reached ~5 units, so the transition read one-sided. The land now has a shelf edge (bright lip,
dark inland band) and tidal combing, with stars elongating along the coast normal. Altitude cannot
drive this: water is carved to exactly 0, but a band 0.030 above the waterline already covers
19.7% of land, so low-lying inland would all become beach. It is ring-sampled distance.

**Navigable rivers** are water provinces, so the sea shader draws them while the thin rivers
beside them are lanes. There is no separate river effect to hook. Enclosure is detected
geometrically and the sea treatment is switched *off* there — no nebula, no shore rim — rather
than inventing a third look.

**Borders.** 35 textures across *independent sets*, generated by `build_space_textures.py`. The
character-selection screen uses its own (`border_realm_explorer_*`). Border **width is engine
geometry and cannot be changed** — only brightness. Cut `halo`, never `strength`. See
`pitfalls.md` §1; this has been "fixed" five times.

---

## Generators

| tool | writes |
|---|---|
| `build_terrain_hybrid.py` | the 3 structure textures, `materials.settings`, `eotg_terrain_params.fxh` |
| `build_terrain_index.py` | `detail_index.tga`, `detail_intensity.tga` |
| `build_colormap.py` | `colormap.dds` |
| `build_space_textures.py` | 35 border textures, movement arrows, flatmap |
| `check_terrain_distinctness.py` | read-only audit |

**`build_terrain_hybrid.py` writes `materials.settings` and `eotg_terrain_params.fxh` in the same
run, deliberately.** Material indices are positional in `materials.settings` and the `.fxh` is a
lookup table keyed off that ordering. Running the superseded `build_terrain_materials.py` on its
own rewrites one without the other and every terrain reads another terrain's tint, stars and
effect. Nothing errors, and the `.fxh` is gitignored so git reports nothing.
`build_terrain_materials.py` is **a library now, not an entry point** — five tools import helpers
from it, so it must stay.

### The exact rebuild commands

Both generators rewrite unconditionally and **the shipped arguments are not the defaults**:

```
python docs/tools/build_terrain_hybrid.py <root> --source "<smoked carbon-glass PNG in Downloads>"
python docs/tools/build_colormap.py       <root> --level 132
```

Verified byte-identical 2026-10-04 (9/9 structure bakes and the colormap). The exact `--source`
filename is in `gfx/map/terrain/README.md`. `--level 132`, not the tool's default of 106.

The structure bakes and `colormap.dds` are **tracked** via `.gitignore` exceptions — not because
they are irreplaceable but because they are easy to replace *wrong*. `docs/test_map/build_terrain.py`
has the guard pattern: it refuses an output path inside the main mod's `gfx/` and checksums those
ten files before and after. Copy it before pointing any generator at the repo.

---

## Art status

**The game loads the repo directly** — `Documents/Paradox Interactive/Crusader Kings III/mod/eotg_stellar_rivers`
is a directory junction to it (2026-10-04). Edit `gfx/` here; there is no sync step. Shader changes
need a **full restart**, not a reload.

| asset | status |
|---|---|
| structure source image | 1 needed, present |
| terrain textures | **not needed** — superseded by the hybrid pipeline |
| border textures | 35, generated |
| **terrain icons** | **15 missing.** Vanilla ships 20, we ship 0, so medieval icons are showing |
| battle backgrounds | none; vanilla placeholders in use |

**Icon spec:** 15 `.dds`, **60×60 RGBA**, named by CK3 key (`plains.dds`, `hills.dds`, …) in
`gfx/interface/icons/terrain_types/`. Legible at 60px — strong silhouette, 2–3 tones, no fine
detail. Use the terrain's tint so the icon matches what the map shows. Vanilla also has `sea.dds`
and `coastal_sea.dds` if the void wants its own.

**Known discrepancy:** `gfx/map/terrain/eotg_hologram_source.png` is tracked as the structure
source but is the *old* holographic grid (651,612 bytes), not the smoked carbon-glass image the
shipped bakes came from (1,684,506 bytes). Harmless until someone rebuilds from it.

---

## Current tuning values

Starting points if something reads wrong. All in `pdxterrain.shader` unless noted.

| constant | value | effect |
|---|---|---|
| `EOTG_TERRAIN_EMISSIVE` | 1.20 | overall terrain brightness (terrain is unlit) |
| `EOTG_TERRAIN_LEVEL` | 0.55 | albedo level before emission |
| `EOTG_STRUCTURE_SCALE` | 0.90 | how much of the structure texture survives |
| `EOTG_STRUCTURE_FLOOR` | 0.30 | level the structure fades toward at amount 0 |
| `EOTG_OCC_MAX` / `_DENSITY_GAMMA` | 0.45 / 1.00 | star occupancy at density 1, and the curve (currently linear) |
| `EOTG_STAR_FINE_CELL` / `_COARSE_CELL` | 2.83 / 8.49 | star lattice spacing — shrink to add stars, don't raise occupancy |
| `EOTG_RADIUS_LO` / `_HI` | 0.75 / 1.30 | star size range |
| `EOTG_SHELF_DARK` | 0.62 | coast inland shadow; most likely to look like a pasted drop shadow |
| `EOTG_COMB_GAIN` / `_STRETCH` | 0.12 / 1.4 | tidal combing strength and star elongation |
| `EOTG_FX2_LO` / `_HI` | 0.68 / 0.88 | secondary-effect patch coverage (~11.5%) |
| `EOTG_POLITICAL_OPACITY` | 0.55 | realm fill over terrain |
| `EOTG_BORDER_SHARPEN` | 2.6 | discards the gradient border's soft tail |
| `EOTG_RIVER_DARK` (`pdxwater`) | 0.30 | how far navigable rivers are taken down |

---

## Before you change anything

1. **Read `docs/pitfalls.md`.** Especially the intro rule, §1 (borders), §2 (stale overrides),
   §5 (the map is near-black) and §13 (generators).
2. **Confirm which system draws the thing you are about to change.** Terrain overlay, border mesh
   and water are three different systems that look adjacent on screen.
3. **A change that produces no visible result is evidence**, not a prompt to try a bigger number.
4. **Check `error.log` for `pdx_terrain.cpp` after every shader change.** A map that renders does
   not prove the high-spec effect compiled — the low-spec path is a silent fallback, and it hid a
   broken `PdxTerrain` for a full day.
