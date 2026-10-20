# Proposal: Holding Tier Progression (Levels 1–4 Visual Representation)

**Target:** `eotg-architect` (for review), `eotg-scripter`, Orchestrator  
**Date:** 2026-10-20  
**Context:** CK3 1.20.1.1 "Crozier"  
**Status:** Proposal for Architecture Review  
**Related Documents:** [`docs/marker_model_brief.md`](../marker_model_brief.md), [`docs/proposals/holding_solar_system_feasibility.md`](holding_solar_system_feasibility.md), [`docs/tools/build_marker_assets.py`](../tools/build_marker_assets.py), [`docs/tools/build_marker_mesh.py`](../tools/build_marker_mesh.py)

---

## 0. Executive Summary & Problem Statement

Holding upgrade levels in Crusader Kings 3 represent capital investment and infrastructural maturity:
* `castle_01` to `castle_04`
* `city_01` to `city_04`
* `church_01` to `church_04`
* `tribal_01` to `tribal_02`

Currently, `docs/tools/build_marker_assets.py` maps all four levels of each holding type to a single shared mesh (e.g. `eotg_marker_castle_mesh`). While this established a clean baseline for Gate 1 and the 7 base silhouettes, an upgraded Tier 4 sector capital looks visually indistinguishable on the map from a freshly colonized Tier 1 frontier system.

This proposal evaluates the options for **visually differentiating holding upgrade tiers (Levels 1–4)** under the mod's "Command Center Holotable" paradigm and recommends an automated, zero-manual-modeling implementation pipeline.

---

## 1. Engine Capabilities & Precedents

In CK3 1.20, each primary building level defines its own `assets` block:

```pdx
castle_01 = { assets = { asset = { name = "eotg_marker_castle_01_mesh" ... } } }
castle_02 = { assets = { asset = { name = "eotg_marker_castle_02_mesh" ... } } }
castle_03 = { assets = { asset = { name = "eotg_marker_castle_03_mesh" ... } } }
castle_04 = { assets = { asset = { name = "eotg_marker_castle_04_mesh" ... } } }
```

* **V (Verified):** The engine natively supports swapping the primary mesh on holding upgrade. Vanilla swaps between completely different castle meshes at each tier.
* **V (Verified):** Ambient audio emitter tiering is already supported in engine via `soundparameter = { "Tier" = 0/1/2/3 }` on the asset block.
* **V (Verified):** All markers in this mod are generated via Python pipelines (`docs/tools/build_marker_mesh.py`, `build_marker_assets.py`, and `blender_marker_emblems.py`). Any structural or dimensional variation can be scripted programmatically without manual 3D modeling.

---

## 2. Evaluation of Progression Axes

| Axis | How It Works | Strengths | Risks & Constraints |
| :--- | :--- | :--- | :--- |
| **A. Pure Scale / Size** | Scale factor applied to mesh per tier (e.g. 0.85x $\rightarrow$ 1.30x). | Instantly readable at any zoom level; highly intuitive. | Base plinth is already 4.08 units wide (`marker_model_brief.md`). Scaling past 1.35x risks clipping province labels and tight star clusters. |
| **B. Emissive Brightness** | Modulating `Properties.r` / diffuse brightness or beam alpha. | Zero geometric changes; draws eye to capital systems. | `EOTG_MARKER_EMISSIVE` already flattens 82% of lighting; over-brightening triggers severe bloom washout. Under-brightening Tier 1 looks like Fog of War. |
| **C. Projector Beam Height** | Changing vertical beam altitude (`make_beam_obj.py`) per tier. | Creates a dramatic "tactical skyline" across the galaxy; completely free of horizontal clipping. | Only affects the beam, not the core emblem geometry. |
| **D. Procedural Orbital Geometry** | Scripted addition of concentric orbital rings / sub-nodes around the core emblem. | Communicates "infrastructural density in orbit"; preserves core silhouette identity; authentic sci-fi holotable read. | Adds ~100–300 triangles per tier (still well within the 2,000 tris budget). |

---

## 3. The Recommended Architecture: The 3-Layer Progression Package

Rather than relying solely on size or brightness, the optimal strategy combines **Scale, Beam Altitude, and Procedural Orbital Structure**:

```
Tier 1 (Outpost/Relay):     Scale 0.85x  │  Low Beam   │  Bare Core Silhouette
Tier 2 (Established Hub):   Scale 1.00x  │  Med Beam   │  Core Silhouette + Single Equator Ring
Tier 3 (Major Sector Seat): Scale 1.15x  │  Tall Beam  │  Core Silhouette + Dual Rings + 2 Orbiting Sub-Nodes
Tier 4 (Cluster Capital):   Scale 1.30x  │  Pillar Beam│  Core Silhouette + Intricate Halo Cage + Sub-Nodes
```

```
     [Tier 1]                 [Tier 2]                 [Tier 3]                 [Tier 4]
       / \                     /  \                    /    \                  /      \
      |   |                  ( |  | )                (( |  | ))              ((( |  | )))
       \ /                    \ \/ /                  \ \  / /                \ \    / /
        |                       ||                      ||||                    ||||||
     [Short]                  [Medium]                 [Tall]                  [Pillar]
```

### Why this package succeeds:
1. **Preserves Silhouette Recognition:** The fundamental icon (Shield, Torus, Obelisk, Chevron) remains identical at the center of the marker across all 4 levels. A player always knows *what* holding type it is.
2. **Multi-Scale Readability:**
   * *Zoomed Far Out:* The **Projector Beam Height** and **Size difference** differentiate a backwater system from a core world.
   * *Zoomed In:* The **Orbital Rings and Sub-Nodes** look like sophisticated planetary defenses, drydocks, and satellite infrastructure.
3. **Safe from Shader Bloom & Clipping:** Keeps size within conservative bounds (0.85x to 1.30x) and maintains stable emissive brightness, avoiding blinding bloom or murky under-exposure.

---

## 4. Implementation Specification

### 4.1 Asset Authoring (`docs/tools/blender_marker_emblems.py`)
In the Blender headless script, wrap emblem generation in a 4-step loop:
* **Level 1 (`_01`):** Base emblem exported at `0.85` scale.
* **Level 2 (`_02`):** Base emblem at `1.00` scale + thin horizontal torus ring (radius = `emblem_radius * 1.35`).
* **Level 3 (`_03`):** Base emblem at `1.15` scale + dual inclined rings + 2 small diamond sub-satellite nodes.
* **Level 4 (`_04`):** Base emblem at `1.30` scale + 3 intersecting halo rings + 4 sub-satellite nodes.

### 4.2 Mesh & Beam Assembly (`docs/tools/build_marker_mesh.py`)
* Update `build_marker_mesh.py` to generate `eotg_marker_<type>_0<1-4>.mesh`.
* Pass height parameter to `make_beam_obj.py`:
  * `beam_height = base_height * (0.85 + 0.25 * tier)`

### 4.3 Building Definition Overrides (`common/buildings/`)
Update `build_marker_assets.py` to write explicit tiered asset references in:
* `common/buildings/eotg_00_castle_buildings.txt` (`castle_01` $\rightarrow$ `castle_04`)
* `common/buildings/eotg_00_city_buildings.txt` (`city_01` $\rightarrow$ `city_04`)
* `common/buildings/eotg_00_temple_buildings.txt` (`church_01` $\rightarrow$ `church_04`)
* `common/buildings/eotg_temple_citadel_buildings.txt` (Citadels 01 $\rightarrow$ 04)
* `common/buildings/eotg_00_tribal_buildings.txt` (`tribal_01` $\rightarrow$ `tribal_02`)

Nomads and Herders remain single-tier (`Tier 0`).

---

## 5. Review Questions for `eotg-architect`

1. **Tribal Scope:** Tribal holdings only have 2 upgrade levels (`tribal_01` and `tribal_02`). Recommend mapping `tribal_01` to Tier 1 geometry (bare) and `tribal_02` to Tier 2/3 geometry (single ring). Confirm approval.
2. **Audio Parameter Alignment:** Confirm whether vanilla ambient audio parameters (`Tier = 0..3`) should be retained or muted in favor of custom subspace ambience in Gate 3.
3. **Schedule / Gate Placement:** Confirm whether building this tiered asset pass belongs in the current 3D asset batch or should follow the completion of the 4 activity markers.

