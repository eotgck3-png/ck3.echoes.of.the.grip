# Holding solar-system models: engine feasibility

Investigation for `EotG_Holding_Solar_System_Feasibility_Brief.md`, 2026-10-18.
Installed game: **CK3 1.20.1.1 "Crozier"** (`launcher-settings.json`). All file citations below are
vanilla paths under `game/` unless marked *mod*. Nothing has been tested in game yet; every
"Verified" means verified in shipped game files or in this mod's already-working marker build.

Labels: **V** verified · **L** likely · **U** uncertain · **X** unsupported.

---

## 0. The short answer

| Question in the brief | Answer |
|---|---|
| Shared solar-system model for holdings? | **V.** The mod already does this: 18 primary holding buildings point at one shared mesh (`gfx/models/buildings/eotg_markers/`, built by `docs/tools/build_marker_assets.py`). |
| Holding type controls star colour? | **V.** Each holding type has its own primary building (`castle_01`, `city_01`, `temple_01`, `tribe_01`…), so each points at its own `pdxmesh` entry. These entries share one `.mesh` file and differ only in their `meshsettings` textures. The mod's `eotg_markers.asset` already does exactly this. A shader cannot read holding type (**X**), and it doesn't need to. |
| Variation without a unique model per county? | **V** for the selection mechanisms (`names = {}` random pool, `graphical_regions`, `graphical_cultures`, `graphical_faiths`, `governments`, `provinces`). **U** for whether the `names` pick is stable across save/load. |
| Buildings visibly change the holding? | **V, one way, and vanilla already does it.** `is_graphical_background = yes` buildings draw an extra mesh at the holding whenever their province-scope trigger is true, and vanilla's own trigger reads `has_building_or_higher`. Holding upgrades also swap models. **U** whether *more than one* background building can draw at once. That is **L**: the community *Holding Sprawl* mods drew farms, barracks and stables together around vanilla holdings through extra background buildings, but this has not been tested here. It is the question that decides the architecture. |
| Runtime assembly of an arbitrary system from the building list? | **X** as a general mechanism. Entities compose sub-meshes only statically (`attach`/`locator`), with no script-driven attach. The only runtime composition available is through separate background buildings, and that is unproven. |
| Best fallback | One dominant-infrastructure feature per holding, chosen by a priority trigger and drawn as one background mesh. A second, independent feature can go at the **special-building locator**, opened at runtime with `add_special_building_slot`. |

**Recommendation in one line:** prototype **F, Planetary Crown**: a star, one bold ring and 2–3 bodies,
with the star colour set by holding type through the existing marker pipeline. Add **one** building-driven
feature through a graphical-background building. Before production, prove two things: that two
background buildings render together (likely, but untested), and that a regular (non-special) building's `asset` is ignored.

---

## 1. How CK3 picks the model shown for a holding (Deliverable 1)

### 1.1 Three kinds of building draw on the map

Only buildings with an `asset` block draw anything. In vanilla these are:

| Kind | Where | Drawn at | Evidence |
|---|---|---|---|
| **Primary holding building** (`castle_01..04`, `city_01..04`, `temple_01..04`, `tribe_01..02`, `nomad_*`, citadels) | `00_castle_buildings.txt` etc. | `buildings` locator | **V.** Each level has its own `asset`, so the model changes as the holding upgrades. |
| **Graphical background building** (`walls_00..04`, `walls_01_tribal`) | `99_background_graphics_buildings.txt` | `buildings` locator, together with the holding | **V.** `is_graphical_background = yes`. It is never constructed and the AI skips it (`_buildings.info:406-409`). It shows when `is_enabled` is true, scopes `root` = province, `scope:holder`, `scope:county` (`_buildings.info:104-114`). |
| **Special / great / legendary building** (wonders, 215 mine variants, universities) | `00_special_buildings.txt`, `00_special_mines.txt`, `tgp_great_project_buildings.txt`… | `special_building` locator, a separate point next to the holding | **V.** `special_building_locators.txt` is a second `game_object_locator` with its own per-province positions. |

Regular economy and military buildings (farms, barracks, the `00_standard_*` files) have **no `asset`
in vanilla**. Whether the engine would draw one if given an asset is **U**. No vanilla precedent
exists, so assume not.

**Vanilla already changes a holding's look based on a building.** `walls_00.is_enabled` (`99_background_graphics_buildings.txt:4-30`)
switches the walls off when `has_building_or_higher = "city_wall_of_toledo_01"` and similar buildings
are present, and `walls_01..04` select by `fort_level`. Building presence and upgrade level driving a
visible mesh is therefore shipped behaviour, not a workaround.

### 1.2 The `asset` block (`_buildings.info:30-104`)

```
asset = {
    type = pdxmesh | entity          # all names in one asset must be the same type; meshes are cheaper
    name = "x_mesh"                  # repeatable
    names = { "a_mesh" "b_mesh" }    # "to randomize between multiple meshes/entities"
    illustration = "...dds"          # county-view picture
    soundeffect = { ... }
    governments = { ... }            # filter
    provinces = { 496 1000 }         # filter; "if set, the asset is only used in the listed provinces"
    graphical_regions = { ... }      # filter
    graphical_cultures = { ... }     # filter; matches culture `building_gfx`
    graphical_faiths = { ... }       # filter; faith > religion > family
    domicile_building = ...          # filter, checked against the owner's domicile
    requires_dlc_flag = ...
}
```

A building may list many `asset` entries, and the engine picks one. The precedence the `.info` gives
is provinces, then government, then graphical region, then culture and faith. Vanilla annotates
temple entries with the weights `graphical_faiths #+1`, `graphical_cultures #+2`, `graphical_regions #+4`
(`00_temple_buildings.txt:240-249`), so the best-scoring match wins and an entry with no filter is the
fallback. The mod's marker build relies on exactly that fallback.

Usage counts across vanilla: `name` 944, `graphical_regions` 692, `graphical_cultures` 655, `graphical_faiths` 349,
`names` 176, `provinces` 12, `domicile_building` 6, `governments` 5.

### 1.3 Meshes, materials, entities

- **`.asset` files** (`gfx/models/**`) declare `pdxmesh = { name file meshsettings… }`. Each
  `meshsettings` binds one material slot (`index`) to textures and a shader. **Colour variants are
  just several `pdxmesh` entries pointing at the same `.mesh` with different textures.** This is
  verified in *mod* `gfx/models/buildings/eotg_markers/eotg_markers.asset`, which has one geometry
  and three slots (pedestal, emblem, beam), with the colour per holding type.
- **Entities** wrap a mesh and add `locator`s, `attach = { "loc" = "other_entity" }`, `default_state`
  and looping `state`s with `event = { particle = … }`. For example, `holdings/fp3/fp3_building_persian_temple_01_a_01.asset:64-100`
  runs smoke particles on a looping idle state. Vanilla holdings use 83 locators, 77 attaches, 8 states
  and 6 particles in all. **Attach is static**: nothing in script picks which sub-entity is attached.
  An entity is the way to do an animated or particle star glow (**L**), not conditional modules.
- **Emissive in vanilla materials** is a single mask in the normal map's red channel, and the green and blue emissive channels are ignored (wiki `/3D_models`, standard_atlas table). Glow colour therefore comes from the diffuse or from the mod's own shader, not from a coloured emissive map.
- **`all_buildings.asset`** is a showroom entity (`building_all`) that lays out every holding on a grid. The wiki tells you to add your models to it, but the mod's markers work without that, so it is not required for display.
- **LOD**: `lod_percentages = { lod = { index = 1 percent = 3.0 } … }` on the mesh (same file, lines 5-8). It is **V** as a field, and 384 vanilla meshes use it.
- **Shaders**: the mod's `gfx/FX/pdxmesh.shader` already carries an emissive/fresnel marker effect,
  because plain lit colour turned into a grey smudge under fog (see the province-markers note). A
  shader cannot see holding type, buildings or variables (**X**). It can animate by time, for example
  spinning a ring in the vertex shader (**L**, and the per-file shader comment rules in `docs/pitfalls.md` apply).
- **Zoom**: the 3D `building_layer` uses `fade_in=0 fade_out=9` (`gfx/map/map_object_data/game_object_layers.txt:10-16`).
  The `NMapIcon` defines `HOLDING_VISIBLE_ZOOM_STEPS = { 0 4 }` / `HOLDING_SMALL_VISIBLE_ZOOM_STEPS = { 5 8 }` (`common/defines/graphic/00_graphics.txt:666-667`)
  govern the 2D holding icons, not the models.

### 1.4 What is placed where

`gfx/map/map_object_data/building_locators.txt` (`name="buildings"`) and `special_building_locators.txt`
(`name="special_building"`) hold one position, rotation and scale per **province id**. The holding
mesh, its background mesh and its special building all hang off these two points. Placement, scale
and rotation are per-province data, not per-model.

> **Gate 1 consequence (new finding):** the mod ships neither file and has no `map_data/` yet, so
> holdings currently sit on vanilla's locators. When the mod's own `definition.csv` lands, both
> locator files must be generated for the new province ids. Otherwise holdings and special
> buildings will float at vanilla coordinates. This belongs to the cartographer and should be added
> to the taskboard. The engine reads **one** list of each, keyed by province id: the last mod loaded wins, and the lists never merge.

### 1.5 What a mod can and cannot do

| Can (normal mod files) | Cannot |
|---|---|
| Replace any building's `asset` by redefining the building (the mod does this for 18 + 6) | Make a shader read holding type, buildings or variables |
| Add new `is_graphical_background` buildings with arbitrary province-scope triggers | Attach entity sub-parts conditionally from script |
| Add special-building slots at runtime (`add_special_building_slot`, 94 vanilla uses, e.g. `events/decisions_events/major_decisions_events.txt:994`) | Assemble a model from an arbitrary list of buildings |
| Own the locator files, layer fade distances and graphics defines | Change the number of locators per province (two: holding, special) |

---

## 2. Capability by brief question

**4.2 Colour by holding type: V.** It uses separate `pdxmesh` entries over shared geometry, which is
already built. Readability against the map palette is a tuning question, and the CB-30 placeholder
colours are still open.

**4.3 Variation:**

| Mechanism | Status | Stable across save/load | Maintenance |
|---|---|---|---|
| `names = { a b c }` random pool | **V** exists | **U**, must be tested | Low |
| `graphical_regions` | **V** | Yes, deterministic | Low; needs graphical regions in the mod's `map_data/geographical_regions` |
| `graphical_cultures` (race/culture later) | **V** | Yes | One `building_gfx` per race; multiplies variants per holding type |
| `graphical_faiths`, `governments` | **V** | Yes | Low |
| `provinces = { … }` | **V** | Yes | High; tied to province ids, so it breaks on the map swap |
| Background building gated on a province variable set once at game start | **L**: triggers and variables are verified, but re-evaluation timing is not | Yes (variables save) | Low; survives the map swap |

**4.4 Buildings change the look:**

| Behaviour | Status | Mechanism |
|---|---|---|
| Holding model changes as the holding upgrades | **V** | Per-level `asset` on `castle_01..04` |
| Building **presence** adds or swaps a visible mesh at the holding | **V** (vanilla walls) | Background building, `is_enabled = { has_building_or_higher = X }` |
| Building **level** selects the mesh | **V** | `has_building_or_higher = X_02`, highest level first |
| **Combinations** of buildings | **V** only as one prebuilt mesh per combination, chosen by trigger; **U** as separate stacked meshes | One background building per combination, or several background buildings (untested) |
| A building gets its own model next to the holding | **V** for special buildings at the special locator; **U/assume X** for regular buildings | `type = special` + slot |
| Update timing when a building completes | **U** | Background triggers may refresh on a province change, monthly, or only on reload |

**4.5 Dominant infrastructure: L.** Use one background building per feature category. Make the
`is_enabled` triggers mutually exclusive in priority order (highest-tier category wins, ties broken
by a fixed order), exactly as `walls_01..04` partition `fort_level`. No events or variables are
needed, so AI and player get identical results. A "score" is possible with a script value, but
`has_building_or_higher` alone is simpler and needs no upkeep.

**4.6 Modular: L.** Holding Sprawl (workshop 2818728722, now delisted) and Simple Holding Sprawl reportedly stack several background buildings around the vanilla holding. That is evidence from search snippets, not a test. If two or more background buildings can draw at once, a base plus independent
modules works. Every module is authored at the origin so they overlap correctly, because they all
share the holding's locator. If only one can draw, modules must be prebuilt complete variants. Either
way the base star sits on the primary holding building, so holding identity can never be lost to a
building change (brief principle 4).

**4.7 Performance:** these are estimates, since no documented limits exist. Vanilla holdings carry
3 LODs. The one community figure is about 10k polygons as a ceiling (Realms in Exile art wiki: "try to keep it way lower"). Aim for ≤ 3k triangles at LOD0, ≤ 2 material slots, 512² textures, and one atlas shared by
all variants. Thin orbit lines will alias out beyond mid zoom, so draw rings as flat bands at least
about 3 % of model diameter wide, or as an emissive decal. Alpha-blended glow risks sort errors
against the terrain, which is why the mod's beam uses `snap_to_terrain_alpha_to_coverage`; keep that.

---

## 3. Options matrix (Deliverable 2)

Ratings run 1 (poor) to 5 (strong). The engine feasibility rating is evidence-based. The others are
judgement against the constraints above.

| | Feasible | Read at zoom | Distinguishes holdings | Shows buildings | Asset effort (5 = least) | Perf risk (5 = least) | Maintenance | Race/culture fit |
|---|---|---|---|---|---|---|---|---|
| **A** Classic system | 5 | 3: thin orbits vanish | 3 | 3 | 4 | 4 | 4 | 4 |
| **B** Star cluster | 5 | 2: reads as noise | 2 | 2: features compete with stars | 4 | 4 | 4 | 3 |
| **C** Orbital network | 5 | 3 | 3 | **4**: stations are the natural module | 3 | 3 | 3 | 4 |
| **D** Celestial emblem | 5 | **5** | 3 | 2: little room for features | **5** | **5** | **5** | 3 |
| **E** Binary star | 5 | 3 | 4 as a special-holding accent | 2 | 4 | 4 | 4 | 3 |
| **F** Planetary crown | 5 | **4** | 4: the ring orientation and body count vary cheaply | **4**: one feature slot on the ring | **4** | **5** | **4** | **4** |
| **G** Galactic cluster | 5 | 1 | 2 | 2 | 2 | 2 | 2 | 2 |

All seven are equally feasible: the engine just draws a mesh. They separate on readability and on
leaving room for one building feature.

---

## 4. Recommended architecture (Deliverable 3)

1. **Base (primary holding building):** the Planetary Crown, a colour-coded emissive star with one bold
   ring band and 2–3 small bodies. It lives on the 18 primary buildings through
   `build_marker_assets.py`, replacing the current marker shape.
   - **Colour:** one `pdxmesh` per holding type over one `.mesh`, with only the star texture changing.
   - **Upgrade:** levels 1–4 may add a body or widen the ring through the per-level asset. This is free, since the mechanism is already present.
   - **Variation:** 3 arrangements in `names = { }` (ring tilt, body count) if `names` proves save-stable.
     Otherwise use `graphical_regions` once the mod's regions exist.
2. **Development feature (background building, one at a time):** `eotg_holding_feature_<category>`
   with `is_graphical_background = yes`. Triggers are prioritised and mutually exclusive, so the
   strongest infrastructure wins: a shipyard dock, fortress platform, agri-world, mining belt, trade
   ring, shrine-world or observatory, each authored at the origin to sit on the crown. Level tiers
   use `has_building_or_higher = X_03` above `X_01`, and the higher tier replaces the lower rather
   than stacking.
   - The **walls slot is the same mechanism** and the mod has already blanked it. The prototype must
     show whether the new feature coexists with `walls_*` or competes with it.
3. **Second feature (only if needed):** the special-building locator. A province opens a slot with
   `add_special_building_slot` when a signature regional project completes, and a `type = special`
   building draws its model beside the system. It is one per province and doubles as a wonder.
4. **Race/culture later:** `graphical_cultures` on the *feature* assets only, not the base, so races
   change station styling while holding-type colour stays universal. Growth is roughly races ×
   categories, not races × categories × holding types.
5. **Postpone or abandon:** runtime assembly from the full building list (X); per-county bespoke
   models (`provinces`, which breaks on the map swap); thin wire orbits; B and G; regular buildings with
   their own map models (no precedent).

**Fallback** if only one background building can draw and its triggers refresh only on reload: keep the
dominant-feature rule, but drive it from a province variable written in the building's `on_complete`
and read by the trigger. If the 3D path fails entirely, show the feature as a 2D map icon or a county
modifier icon instead.

---

## 5. Prototype plan (Deliverable 4)

Build it on the British Isles test sub-mod (`docs/test_submods/british_isles`), not the main mod,
using placeholder geometry. Reuse the existing marker mesh and add two primitive feature meshes,
a torus "dock" and a box "fortress".

| # | Test | Files | Pass | Fail means |
|---|---|---|---|---|
| T1 | Colour per holding type on a crown mesh | `eotg_markers.asset` + `build_marker_assets.py` shape table | Castle/city/temple/tribal show 4 distinct star colours | (Already passing for the marker; this re-checks the new shape.) |
| T2 | Background feature from building presence | New `common/buildings/eotg_zz_test_features.txt`: `eotg_feat_agri` (`is_enabled = { has_building_or_higher = farm_estates_01 }`) and `eotg_feat_fort` (`… = barracks_01`) | Building a farm makes the dock appear on that holding | Background buildings are limited to engine-known keys, so fall back to the special slot |
| T3 | **Two backgrounds at once** (highest risk) | A province holding both buildings | Both meshes are visible | Only one is drawn, so use prebuilt combinations (the §4 fallback) |
| T4 | Coexistence with `walls_*` | Same, while toggling `fort_level` | Feature and wall mesh both draw | Fold features into the `walls_*` definitions |
| T5 | Update timing | `add_building` from the console, then watch: immediate, next month, or after reload | Appears within a month | Use the variable fallback |
| T6 | Upgrade replaces | `farm_estates_02` gated above `_01` | Mesh swaps and does not stack | |
| T7 | Regular-building asset | Give `farm_estates_01` an `asset` directly | Documented either way | |
| T8 | `names` stability | 3-entry pool; save, reload, restart | Same pick per holding every time | Use region- or variable-based selection |
| T9 | Readability | Screenshots at zoom steps 0, 4, 8 with neighbouring holdings | Holding type readable at 8; feature readable at 4 | Thicken the ring and shrink the bodies |

**Test each change on a new game, not a loaded save.** A mod author reports that background buildings are resolved at game creation and tied to the save. That would also bear on T5. Check `error.log` for `asset`/`mesh` lines after each load. Tiger reports `unknown field 'assets'`
as benign. The "Unexpected token" lesson from `use_great_projects` applies to every new field.

---

## 6. Open questions, ranked (Deliverable 5)

| Rank | Question | Risk | Architecture impact |
|---|---|---|---|
| 1 | Can 2+ background buildings draw at once? (T3) | Med; **L** from Holding Sprawl, which reportedly found that asset order in the file matters | Decides modular vs prebuilt combinations |
| 2 | When do background triggers re-evaluate? (T5) | Med | Decides trigger-only vs variable-driven |
| 3 | Do features and `walls_*` coexist? (T4) | Med | Decides a new building key vs reusing walls |
| 4 | Is the `names` pick stable? (T8) | Med | Decides the variation source |
| 5 | Locator files for the mod's own map (Gate 1) | Low risk, certain work | Must be generated when `definition.csv` lands |
| 6 | Ring and emissive readability at zoom 4–8 (T9) | Med | Shape proportions |
| 7 | Do regular-building assets draw? (T7) | Low | Only opens an extra path |

**First to prototype:** the Planetary Crown base with one background feature. **Avoid:** runtime
assembly, per-province models, clusters. **Prove before production:** T3, T5 and T8.

---

## 7. Sources consulted

- Vanilla 1.20.1.1 files cited inline.
- Mod: `common/buildings/eotg_00_*_buildings.txt`, `eotg_99_background_graphics_buildings.txt`, `gfx/models/buildings/eotg_markers/eotg_markers.asset`.
- Paradox wiki: https://ck3.paradoxwikis.com/Holdings_modding (written for 1.3, partly verified), https://ck3.paradoxwikis.com/3D_models and https://ck3.paradoxwikis.com/Exporters. The brief's `Graphics_modding` and `3D_modelling` URLs return 404. Mirror: https://github.com/jesec/ck3-modding-wiki.
- Exporter: IO PDX Mesh, https://github.com/ross-g/io_pdx_mesh (Blender 3.6.4+ or Maya 2018+). The Clausewitz Maya exporter is internal only.
- Community mods, for **technique only** and never as precedent (house rule):
  - Holding Sprawl (2818728722), Holding Sprawl DTR (2824465219) and Simple Holding Sprawl use background-building sprawl.
  - Medieval Arts (2452585382) and its compatch show the single locator list.
  - COW-AGOT 3D Models (2971198450) replaces holding assets per tier.
  - Steam was rate-limited during this research, so these mod claims come from search snippets.
