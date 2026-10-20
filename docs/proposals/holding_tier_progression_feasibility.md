# Feasibility: holding tier progression

Review of [`holding_tier_progression_proposal.md`](holding_tier_progression_proposal.md), 2026-10-20. Five read-only investigations, against CK3 **1.20.1.1** and the mod's working tree:
- vanilla building tiers;
- map rendering;
- the mod's marker pipeline;
- a QA risk review;
- alternatives.

G = `D:/SteamLibrary/steamapps/common/Crusader Kings III/game`.

## Verdict

**Technically feasible, but not recommended as written.**
- **Cheap on the script side:** swapping the model per level is a native engine feature, and the mod already owns every building level.
- **Its central argument fails:** the proposal says tiers would read when zoomed out. They can't, because 3D holdings vanish at zoom step 9 of 35.
- **It contradicts the governing brief:** the brief sets exactly 7 meshes, with no tier upgrades and upgrades shown in the 2D interface.
- **It has several factual errors** (§3).
- **Smaller alternatives get most of the value** (§4).

**Decision for the owner:** keep the brief's rule of no modelled tiers, or amend it. If amending, the recommended path is §4 options B and D, tested in game first.

---

## 1. What the engine allows (verified)

| Claim | Status | Evidence |
|---|---|---|
| Each building level has its own `assets` block, and vanilla swaps the mesh by level | **VERIFIED** | `building_western_castle_01..04_mesh` (G `common/buildings/00_castle_buildings.txt:189-192, 747, 1246`); `_buildings.info:37-102` |
| Scale can be set per mesh | **VERIFIED**: in the `.asset` file's `pdxmesh = { scale = }`, not in the building's `asset` block | G `gfx/models/buildings/holdings/building_indian_castle_01_western.asset:4` (0.9) |
| One `.mesh` reused at several scales | **VERIFIED, engine-legal** | G `gfx/models/mapitems/selection_marker.asset:3-4, 18-19, 33-34` (one mesh at 0.65 / 0.8 / 0.8) |
| `soundparameter "Tier" = 0..3` | **PARTIAL**: only castle uses 0–3; city uses 0/0/2/2; temple, citadel and tribe are all 0. The mod already carries these values over from vanilla. | G `00_castle_buildings.txt:26, 1579`; `_buildings.info:66` |
| The 2D UI already shows the level | **VERIFIED**: the county view prints `GetLevel` next to each building | G `gui/window_county_view.gui:2038, 3477, 3521` |
| Per-level 2D art is possible | **VERIFIED**: the holding window background is the per-asset `illustration` | G `gui/window_county_view.gui:1046` |

## 2. What the engine limits (verified)

- **3D holdings are visible only close in.**
  - G `gfx/map/map_object_data/game_object_layers.txt:9-16`: `building_layer` has `fade_out=9`.
  - Zoom runs over 35 steps (`00_graphics.txt:161`), and the flat map starts at step 21 (`:51`).
  - So markers show at camera heights 70 to about 396 out of 6500, roughly the closest quarter.
  - The mod doesn't override this.
  - Beam height and scale therefore cannot make a capital readable "zoomed far out" (proposal §3.2).
- **The 2D holding banners have the same reach.**
  - They are the `NMapIcon` `HOLDING_VISIBLE_ZOOM_STEPS {0 4}` and `HOLDING_SMALL {5 8}` (`00_graphics.txt:663-700`).
  - The banner is `flowcontainer_holding_info` in `gui/map_icon_layer.gui:2838-3046`.
  - Between steps 9 and 21 the map shows only title and capital labels.
- **Spacing is not the problem.**
  - Nearest-neighbour distance between vanilla building locators: median 25.5 map units, 1st percentile 11.6.
  - The plinth is 4.08 wide; at 1.30x with rings it is about 6 to 7.
  - Collisions would be rare, but label clipping was not measured.
  - The mod's own map will set the real spacing.
- **Performance is fine:** 7 → 20 distinct instanced meshes adds about 13 draw batches.

## 3. Errors in the proposal

1. **Wrong building keys.**
   - `church_01..04` is really `temple_01..04`, and `tribal_01..02` is really `tribe_01..02`. Proposal lines 15–17, 100, 102 and 110.
   - Real chain: `temple_01..04` (G `00_temple_buildings.txt:16, 1066, 1926, 2774`) and `tribe_01..02` (`00_tribal_buildings.txt:6, 168`).
   - Temple citadel is `temple_citadel_01..04`.
   - Nomad and herder each have a single building.
2. **The §4.3 files are generated output.** They say "do not hand-edit". The change belongs in `pick_mesh` / `BUILDING_HOLDING` in `docs/tools/build_marker_assets.py:156-168, 667-671`.
3. **The beam is not separate.**
   - It is material slot 2 inside each type's mesh, and its height is the hover gap (`build_marker_mesh.py:136-138, 180`).
   - A taller beam lifts the emblem. That was tried at hover 0.90 and reverted, because it "read as the pedestal having been stretched" (`:130-135`).
   - §4.2's `make_beam_obj.py` height formula isn't how the build works.
4. **Scaling in Blender fails the emblem checks.**
   - Emblems are normalised against `MAX_WIDTH 1.15`, `MAX_HEIGHT 1.75` and `MAX_RADIUS 0.57` (`blender_marker_emblems.py:79-81, 828-831`).
   - A 1.30x emblem with rings at 1.35x radius fails those checks.
   - Scale belongs in `build_marker_mesh.py` or `pdxmesh scale`.
5. **The triangle budget is misread.**
   - 2,000 triangles is the emblem cap (`TRIS_HARD`), and +300 per tier fits it.
   - The whole-marker target is also 2,000, with a hard limit of 4,000 (`marker_model_brief.md:84-86`). The old full marker was already 2,728.
6. **The construction cage.** `eotg_construction.mesh` is sized to a 1.0x marker (`MARKER_TOP 5.38`). A 1.30x tier 4 under construction pokes through it. The proposal's "free of clipping" claim misses this.
7. **"Zero manual modelling."** Each new shape is hand-written bmesh code (`blender_marker_emblems.py:250-340`), run in Blender, plus a review of the preview renders. It is scripted, but it is not free.
8. **The governing brief isn't cited.** The proposal never mentions that `holding_representation_brief.md:25, 52-53` fixes 7 meshes and no modelled tiers.

## 4. Options, cheapest first

| Option | What | Cost | Visible when | Brief |
|---|---|---|---|---|
| **A. 2D only** | The level is already in the county view. Add a level pip or number to the map holding banner (`flowcontainer_holding_info`, a GUI override). Optionally a per-level holding `illustration` (needs 4 images per type). | Low (pips; GUI override maintenance); art for illustrations | Steps 0–8 (banner); always in the window | **Complies** |
| **B. Scale-only tiers** | 1 mesh per type, 4 `pdxmesh` blocks with `scale` (e.g. 0.9 / 1.0 / 1.1 / 1.2). Points each level at its block. No new geometry. | Low: a generator change only; cage resized to the largest scale | Steps 0–8 | Grey area: still 7 mesh files, but tiers are shown. **Owner call.** |
| **C. The full proposal** (rings, sub-nodes, halo) | 20 meshes, new emblem geometry per tier, cage resize, generator restructure, preview review | Medium to high | Steps 0–8 | **Conflicts**; needs the brief amended |
| **D. Markers visible further out** | Ship `gfx/map/map_object_data/game_object_layers.txt` (3 layers; keep `activities_layer` and `unit_layer` at 9) with `building_layer fade_out` raised to about 13–15 | Very low: one 24-line file | Extends A to C to about step 15 | Independent of tiers |

**D affects every marker, not just tiers.** On a space map where holdings are star systems, keeping them visible further out may help on its own. It's untested and could add clutter at mid zoom. **Try D in game first:** one file, easy to revert, and it decides whether any 3D tiering is worth doing.

**Recommendation:**
1. Run the **D** test. It needs no owner change to the brief, but it changes how the map looks, so it needs the owner's go-ahead.
2. If tiers are still wanted, **B**: small, reversible, about 1 generator change.
3. Leave **C** for Gate 4 (presentation), and only after the brief is amended.
4. **A**'s level pips are the brief-compliant fallback.

## 5. The proposal's §5 questions

1. **Tribal:** `tribe_01` maps to tier 1 and `tribe_02` to tier 2. That is the natural mapping for any option.
2. **Audio:** keep vanilla's `Tier` sound values. They are copied from vanilla automatically and only castle and city vary. A custom ambience is a separate Gate 4 item.
3. **Schedule:** this is presentation work (Gate 4). Gate 1 hasn't started, and marker work has shipped early only by owner direction (CB-30, CB-61). Record the owner's decision on the taskboard before any build. It should come after the activity markers and the current CB-61 wiring, which another session has uncommitted.

## 6. If anything is built

- **Generator assertion** (QA): every `name =` written into `common/buildings/` must exist in `eotg_markers.asset`. Tiger and PX don't validate `assets` blocks (22 benign `assets` hits), so a typo would only show in game as a missing model.
- **In-game checks:**
  - each tier swaps on upgrade;
  - the largest tier fits the construction cage;
  - labels aren't clipped;
  - for D: the fade looks right on the space-map shaders.
- **Icon filenames:** the mod's new `gfx/interface/icons/icon_holding_*.dds` (uncommitted, another session) use the same filenames as vanilla's (`gui/map_icon_layer_templates.gui:937`). They will replace vanilla's holding icons everywhere those files are used. Confirm that is intended.
