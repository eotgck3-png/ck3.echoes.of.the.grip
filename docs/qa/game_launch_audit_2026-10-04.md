# Architecture & QA Review: Game Launch & Map Editor Runtime Audit

**Date:** 2026-10-04  
**Auditor:** Antigravity (Pair Programming / QA Audit)  
**Target Audience:** `eotg-architect`, `eotg-cartographer`, `eotg-scripter`, Orchestrator  
**Status:** Audit Complete — Ready for Architecture Review  
**Context:** Diagnostic review of the project state when launched under CK3 1.20 ("Crozier") with `-debug_mode -mapeditor`.  

---

## 1. Executive Summary

A deep-dive investigation into the project launch under `-debug_mode -mapeditor` revealed why the map rendered as solid neon magenta, along with several latent runtime script issues and playset configuration gaps.

The issues fall into three distinct tiers:
1. **Critical Map Blockers:** A DirectX 11 shader compilation failure crashing the terrain renderer, combined with the test map sub-mod not being installed/enabled in the launcher playset.
2. **Runtime Script Failures:** `create_character` throwing `Must specify gender data` when generating the syndicate patron envoy.
3. **Validation Warnings & Art Debt:** Variable initialization gaps, unused debug flags, and tracked missing art icons.

All offline tool pipelines (`check_all`, `eotg_lint`, 146 unit tests, spec conformance) are healthy and passing.

---

## 2. Critical Map & Renderer Issues

### 2.1 Issue 1: Terrain Shader Compile Failure (Magenta Map Viewport)
- **Severity:** Blocker (causes 100% solid magenta terrain in map editor and black terrain in-game).
- **Location:** [`gfx/FX/pdxterrain.shader` line 1802](file:///c:/Users/river/Documents/GitHub/ck3.echoes.of.the.grip/gfx/FX/pdxterrain.shader#L1802)
- **Runtime Error (`error.log`):**
  ```text
  [21:40:20][E][gfx_dx11_master_context.cpp:611]: Compile error:
  ... error X3013: 'ApplyProvinceEffectsTerrain': no matching 6 parameter function
  [21:40:20][E][pdx_terrain.cpp:1002]: Failed creating terrain effect 'PdxTerrain'
  [21:40:21][E][pdx_terrain.cpp:1009]: Failed creating terrain skirt effect 'PdxTerrainSkirt'
  ```
- **Root Cause:** In CK3 1.20, Paradox updated `ApplyProvinceEffectsTerrain` in `gfx/FX/province_effects.fxh` from 6 parameters to 8 parameters (adding `in float3 TerrainNormal` and `in float2 MapCoords`). When `province_effects.fxh` was updated to 1.20 in commit `b4b9578`, the call site in `pdxterrain.shader` was missed.
- **Remediation:**
  Update line 1802 in `gfx/FX/pdxterrain.shader`:
  ```diff
  -    ApplyProvinceEffectsTerrain( ConditionData, DetailDiffuse, DetailNormal, DetailMaterial, Input.WorldSpacePos, WaterNormalLerp );
  +    ApplyProvinceEffectsTerrain( ConditionData, DetailDiffuse, DetailNormal, DetailMaterial, Normal, Input.WorldSpacePos, ColorMapCoords, WaterNormalLerp );
  ```
  And clear `$HOME/Documents/Paradox Interactive/Crusader Kings III/shadercache/*`.

---

### 2.2 Issue 2: Test Map Sub-mod Not Installed in Playset
- **Severity:** High / Workflow Blocker (user is editing vanilla Europe rather than EotG map).
- **Location:** `Documents/Paradox Interactive/Crusader Kings III/dlc_load.json`, `docs/test_map/MAPEDITOR_STEPS.md`
- **Audit Findings:**
  - `dlc_load.json` currently contains only: `{"enabled_mods":["mod/eotg_stellar_rivers.mod"]}`.
  - The repository root only contains `map_data/seasons.txt` (by design, to avoid packaging unbaked map data in the main mod).
  - The test map sub-mod (`docs/test_map/`) has **not been installed** to `Documents/Paradox Interactive/Crusader Kings III/mod/eotg_test_map` via `python docs/test_map/install.py`.
- **Impact:** When the map editor opened, CK3 loaded the vanilla game map with mod materials and broken shaders. The test map's `heightmap.png` was never loaded for repacking.
- **Remediation:**
  1. Fix the shader in §2.1 first.
  2. Run `python docs/test_map/install.py --out "$HOME/Documents/Paradox Interactive/Crusader Kings III/mod/eotg_test_map"`.
  3. Enable **both** `Echoes of the Grip` and `EotG Test Map` in the CK3 launcher playset before running `-mapeditor`.

---

## 3. Runtime Script Failures

### 3.1 Issue 3: `create_character` Missing Gender Data
- **Severity:** High (script runtime failure during event execution).
- **Locations:**
  - Template: [`common/scripted_character_templates/eotg_augmentation_templates.txt:10`](file:///c:/Users/river/Documents/GitHub/ck3.echoes.of.the.grip/common/scripted_character_templates/eotg_augmentation_templates.txt#L10)
  - Event caller: [`events/eotg_augmentation_patron.txt:1033`](file:///c:/Users/river/Documents/GitHub/ck3.echoes.of.the.grip/events/eotg_augmentation_patron.txt#L1033) (`eotg_aug_patron.007`)
  - Effect caller: [`common/scripted_effects/eotg_augmentation_effects.txt:1371`](file:///c:/Users/river/Documents/GitHub/ck3.echoes.of.the.grip/common/scripted_effects/eotg_augmentation_effects.txt#L1371) (`eotg_aug_patron_accept_effect`)
- **Runtime Error (`error.log` logged 6 times):**
  ```text
  [21:39:42][E][jomini_script_system.cpp:304]: Script system error!
    Error: create_character effect [ Must specify gender data ]
    Script location: file: events/eotg_augmentation_patron.txt line: 1033 (eotg_aug_patron.007:immediate)
  ```
- **Root Cause:** `eotg_aug_patron_envoy_template` defines age, traits, and skills, but omits a `gender` specification. The callers invoke `create_character = { template = eotg_aug_patron_envoy_template ... }` without providing `gender` or `gender_female_chance`. In CK3/Jomini, character generation requires gender data either in the template or in the caller block.
- **Remediation:**
  Add a gender definition to `eotg_aug_patron_envoy_template` in `common/scripted_character_templates/eotg_augmentation_templates.txt`:
  ```pdx
  eotg_aug_patron_envoy_template = {
      age = { 35 55 }
      gender_female_chance = 50
      ...
  ```
  or specify `gender` explicitly at caller sites.

---

## 4. Validation Warnings & Technical Debt

### 4.1 Issue 4: Variable Used Before Initialization
- **Severity:** Medium (Jomini script validator error).
- **Location:** [`common/on_action/eotg_augmentation_on_actions.txt:1711`](file:///c:/Users/river/Documents/GitHub/ck3.echoes.of.the.grip/common/on_action/eotg_augmentation_on_actions.txt#L1711)
- **Runtime Error (`error.log`):**
  ```text
  [21:39:43][E][jomini_effect.cpp:1162]: Variable 'eotg_aug_nr_battle_bonus' is used but is never set.
  ```
- **Root Cause:** `change_variable = { name = eotg_aug_nr_battle_bonus add = 2 }` modifies the variable, but the engine's static checker demands an explicit `set_variable` initialization in the script codebase.
- **Remediation:** Ensure `eotg_aug_nr_battle_bonus` is initialized to 0 upon character/knight setup or via `set_variable` prior to arithmetic modification.

### 4.2 Issue 5: Frontier Diagnostic Variables Unread
- **Severity:** Low (engine notices write-only variables).
- **Runtime Warning (`error.log`):**
  ```text
  [21:39:43][E][jomini_effect.cpp:1146]: Variable 'eotg_frontier_debug_floor_dev' is set but is never used.
  [21:39:43][E][jomini_effect.cpp:1146]: Variable 'eotg_frontier_history' is set but is never used.
  ...
  ```
- **Context:** These variables store debug and historical state for the Frontier system. The engine flags variables that are set but never read in triggers or scripted effects. Benign, but should be suppressed or consumed when debug features are finalized.

### 4.3 Issue 6: Tracked Asset Debt
- **Missing Trait Icon:** `gfx/interface/icons/traits/eotg_total_integration.dds` (documented in `eotg_augmentation_traits.txt:160` as pending human art).
- **Stripped Map Objects:** `gfx/map/map_object_data/special.txt` produces asset warnings for vanilla landmarks stripped by `docs/tools/strip_map_objects.py`.

---

## 5. Verified Healthy Subsystems

| Check / Tool | Status | Details |
|---|---|---|
| **Python Unit Tests** | **PASS** | 146 tests ran in 7.33s with 0 failures (`docs/tools/tests/`). |
| **`eotg_lint.py`** | **PASS** | 0 findings, 0 new violations. |
| **Spec Conformance** | **PASS** | 27 specs reviewed, 25 fully built; 5 expected missing IDs confirmed. |
| **Religion 1.20 Port** | **PASS** | `port_religions_1_20.py --check` confirms output is current. |
| **Event Console Recipes** | **PASS** | `gen_test_recipes.py --check` confirms 184 recipes are up to date. |

---

## 6. Recommended Action Plan for Architecture & Team

1. **Immediate (Cartographer / Orchestrator):**
   - Apply the one-line fix to `gfx/FX/pdxterrain.shader:1802`.
   - Flush the local DirectX shader cache.
   - Run `python docs/test_map/install.py` to stage `eotg_test_map` in the Paradox mod folder.
   - Enable both mods in the launcher playset and proceed with `MAPEDITOR_STEPS.md` heightmap packing.

2. **Immediate (Scripter):**
   - Add `gender_female_chance = 50` to `eotg_aug_patron_envoy_template`.
   - Initialize `eotg_aug_nr_battle_bonus` with `set_variable` before incrementing.
