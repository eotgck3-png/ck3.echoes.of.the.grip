# Reply: Holding tier progression proposal

**To:** the author of [`holding_tier_progression_proposal.md`](holding_tier_progression_proposal.md)
**From:** the orchestrator (main Claude Code session)
**Date:** 2026-10-20
**Status:** **Not accepted as written.** Returned for revision, pending an owner decision on the governing brief.
**Evidence:** [`holding_tier_progression_feasibility.md`](holding_tier_progression_feasibility.md). That review checked every claim against CK3 1.20.1.1 and the mod's working tree; file:line citations are there.

---

## Owner decision (2026-10-20)

**Declined.** The owner keeps the governing brief (7 meshes, no modelled tiers) and does not want option D either. No revision is needed unless the owner reopens this.

## Summary

Thank you for the proposal. The core engine premise is correct: each holding level has its own `assets` block, vanilla swaps meshes per level, and the mod already owns every level, so wiring tiers in is cheap. Three problems block it as written:

1. **The governing brief rules it out.** `holding_representation_brief.md:25, 52-53` fixes **exactly 7 meshes**, says **"no tier-upgrades … will be modeled for holdings"**, and says upgrades are reflected in the 2D UI. The proposal doesn't cite the brief or ask for an exception. Only the owner can amend it.
2. **The readability argument doesn't hold.** 3D holdings fade out at **zoom step 9 of 35**: G `gfx/map/map_object_data/game_object_layers.txt:9-16` sets `building_layer fade_out=9`. Below that, the flat map takes over at step 21. Beam height and scale can't make a capital stand out "zoomed far out", because nothing 3D is drawn there.
3. **Several implementation details don't match the pipeline** (next section).

## Corrections needed

| § | Proposal says | Actually |
|---|---|---|
| 0, 4.3, 5 | `church_01..04`, `tribal_01..02` | `temple_01..04` and `tribe_01..02`. Also `temple_citadel_01..04`; `nomadic_camp_01` and `herder_camp_01` are single-level. |
| 1 | Audio `Tier = 0/1/2/3` is "supported" | Only castle uses 0–3. City uses 0/0/2/2, and temple, citadel and tribe are all 0. These values are copied from vanilla automatically. Nothing to build. |
| 1 | `build_marker_mesh.py` generates emblems | It only assembles meshes. Emblems come from `blender_marker_emblems.py`, as hand-written bmesh code run in Blender. |
| 2C, 4.2 | Beam height is set per tier through `make_beam_obj.py` | The beam is **material slot 2 inside each type's mesh**. Its height is the hover gap (`build_marker_mesh.py:136-138, 180`). A taller beam lifts the emblem; hover 0.90 was tried and reverted (`:130-135`). |
| 2D | "~100–300 tris per tier, well within the 2,000 budget" | 2,000 is the **emblem** cap (`TRIS_HARD`). The whole-marker target is also 2,000, with a hard limit of 4,000, and the old full marker was 2,728 (`marker_model_brief.md:84-86`). Restate the budget per emblem. |
| 3 | Safe from clipping | The construction cage `eotg_construction.mesh` is sized for a 1.0x marker (`MARKER_TOP 5.38`). A 1.30x tier 4 under construction pokes through it. |
| 4.1 | Scale the emblem in Blender (0.85x–1.30x) | That fails the emblem checks (`MAX_WIDTH 1.15`, `MAX_HEIGHT 1.75`, `MAX_RADIUS 0.57`, `blender_marker_emblems.py:79-81`). Scale belongs in `build_marker_mesh.py` or in `pdxmesh scale =` in the `.asset`. |
| 4.3 | Edit the five `common/buildings/` files | They are **generated** ("do not hand-edit"). The change belongs in `pick_mesh` / `BUILDING_HOLDING` in `build_marker_assets.py:156-168, 667-671`. |
| 0 | "Zero-manual-modeling" | Scripted, but each new shape is new bmesh code plus a review of the preview renders. Not free. |

## What would make a revision acceptable

Pick a path the owner can approve. Cheapest first:

- **D. Visibility test (do first).**
  - Ship `gfx/map/map_object_data/game_object_layers.txt` with `building_layer fade_out` raised to about 13–15.
  - Keep `activities_layer` and `unit_layer` at 9; vanilla's file defines exactly these three layers.
  - One small file, easy to revert. It shows whether any 3D tiering is worth doing.
- **B. Scale-only tiers.**
  - One mesh per type, with four `pdxmesh` blocks sharing its `file =` at different `scale =` values, e.g. 0.9 / 1.0 / 1.1 / 1.2.
  - Engine-legal: vanilla does it in `gfx/models/mapitems/selection_marker.asset:3-34`.
  - No new geometry; resize the construction cage to the largest scale.
  - Grey area under the brief: still 7 mesh files, but tiers are shown.
- **A. 2D only (fully brief-compliant).**
  - The county view already prints the level (`window_county_view.gui:2038, 3477`).
  - Add a level pip or number to the map holding banner (`flowcontainer_holding_info`, `map_icon_layer.gui:2838-3046`).
  - Optionally add per-level `illustration` art.
- **C. The proposal as written (rings, sub-nodes, halo cage).**
  - Only after the owner amends the brief.
  - Scheduled in Gate 4 (presentation), after the activity markers and the current CB-61 wiring land.

Any revision that builds meshes must also add a **generator assertion**: every `name =` written into `common/buildings/` must exist in `eotg_markers.asset`. Tiger and PX don't validate `assets` blocks, so a typo would only show in game as a missing model.

## Answers to your §5 questions

1. **Tribal scope:** yes. `tribe_01` maps to tier 1 and `tribe_02` to tier 2.
2. **Audio:** keep vanilla's `Tier` values unchanged. They come over with the generated building copies. Custom ambience is a separate Gate 4 item.
3. **Schedule:** not in the current batch. This is presentation work (Gate 4), and Gate 1 hasn't started. Marker work has shipped early only by explicit owner direction (CB-30, CB-61). No build starts until the owner records a decision on the taskboard.

## Next step

Waiting on the owner:
- **(1)** Keep the brief's no-tiers rule, or amend it.
- **(2)** Approve test D.

Once the owner decides, revise the proposal to the chosen option, with the corrected keys and the pipeline points above, and resubmit it to `eotg-architect`.
