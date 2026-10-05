# QA & Architecture Report: Map Editor Magenta Terrain Root Cause & 1.20 Shader Compatibility

**Date:** 2026-10-04  
**Author:** Antigravity (Pair Programming / QA Audit)  
**Target Audience:** `eotg-architect`, `eotg-cartographer`, Orchestrator  
**Status:** Audit Complete — Fix Ready for Review  
**Related Specs / Boards:** `circlebackTaskboard.md` (`B-TEMPMAP`), `docs/pitfalls.md` (§2, §3), `CLAUDE.md`  

---

## 1. Executive Summary

When launching Crusader Kings III with the current working tree under `-debug_mode -mapeditor`, the entire map viewport renders as a solid **neon magenta / pink** surface (`RGB 255, 0, 255`). The map editor UI loads successfully, and the material dock displays mod materials (`eotg_mountains_01`, `eotg_taiga_01`, etc.), but no terrain geometry shading or textures are visible.

### Verdict
- **Is the custom space shader architecture the root problem?** **No.** The custom shader architecture (`pdxterrain.shader`, `eotg_terrain_params.fxh`) is fully supported by the Clausewitz/Jomini engine.
- **Root cause:** A single **call-site signature mismatch** in `gfx/FX/pdxterrain.shader` resulting from the CK3 1.20 ("Crozier") patch. The HLSL compiler failed with error `X3013`, aborting the pixel shader compile and causing the engine to drop into its unshaded magenta missing-material fallback.

---

## 2. Evidence & Runtime Trace

From `Documents/Paradox Interactive/Crusader Kings III/logs/error.log` (launch timestamp `21:40`):

```text
[21:40:20][E][gfx_dx11_master_context.cpp:611]: Compile error:
 C:\Users\river\Documents\Paradox Interactive\Crusader Kings III\shadercache\dx11\ps_5_0\000000000BA662EA.scache(1737,11-85): warning X3206: implicit truncation of vector type
C:\Users\river\Documents\Paradox Interactive\Crusader Kings III\shadercache\dx11\ps_5_0\000000000BA662EA.scache(6442,7-133): error X3013: 'ApplyProvinceEffectsTerrain': no matching 6 parameter function

[21:40:20][E][gfx_dx11_shaderstate.cpp:165]: Failed getting shader for PixelShader
[21:40:20][E][gfx_dx11_master_context.cpp:525]: Failed creating shader state
[21:40:20][E][pdx_terrain.cpp:1002]: Failed creating terrain effect 'PdxTerrain' (gfx/FX/pdxterrain.shader)

[21:40:21][E][gfx_dx11_master_context.cpp:611]: Compile error:
 C:\Users\river\Documents\Paradox Interactive\Crusader Kings III\shadercache\dx11\ps_5_0\0000000041772646.scache(1737,11-85): warning X3206: implicit truncation of vector type
C:\Users\river\Documents\Paradox Interactive\Crusader Kings III\shadercache\dx11\ps_5_0\0000000041772646.scache(6442,7-133): error X3013: 'ApplyProvinceEffectsTerrain': no matching 6 parameter function

[21:40:21][E][gfx_dx11_shaderstate.cpp:165]: Failed getting shader for PixelShader
[21:40:21][E][gfx_dx11_master_context.cpp:525]: Failed creating shader state
[21:40:21][E][pdx_terrain.cpp:1009]: Failed creating terrain skirt effect 'PdxTerrainSkirt' (gfx/FX/pdxterrain.shader)
```

Both `PdxTerrain` (main terrain surface) and `PdxTerrainSkirt` (terrain edge skirts) failed compilation at engine initialization.

---

## 3. Technical Breakdown

### 3.1 The 1.20 Signature Change
In CK3 1.20, Paradox updated `ApplyProvinceEffectsTerrain` in `gfx/FX/province_effects.fxh` to accept **8 parameters** instead of the pre-1.20 6 parameters:

```hlsl
// gfx/FX/province_effects.fxh (Line 691)
void ApplyProvinceEffectsTerrain(
    in EffectIntensities ConditionData,
    inout float4 Diffuse,
    inout float3 Normal,
    inout float4 Properties,
    in float3 TerrainNormal,      // [NEW in CK3 1.20] Arg 5
    float3 WorldSpacePos,         // Arg 6
    in float2 MapCoords,          // [NEW in CK3 1.20] Arg 7
    inout float WaterNormalLerp   // Arg 8
)
```

### 3.2 The Stale Call Site in Mod Code
In commit `b4b9578` ("CK3 1.20 compatibility, coast and star work, quieter borders"), the mod's copy of `gfx/FX/province_effects.fxh` was upgraded to the 1.20 definition. However, the call site in `gfx/FX/pdxterrain.shader` line 1802 was missed and retained the pre-1.20 6-parameter call:

```hlsl
// gfx/FX/pdxterrain.shader (Line 1802 - CURRENT BROKEN STATE)
ApplyProvinceEffectsTerrain( ConditionData, DetailDiffuse, DetailNormal, DetailMaterial, Input.WorldSpacePos, WaterNormalLerp );
```

### 3.3 Vanilla 1.20 Reference
In vanilla CK3 1.20 (`D:/SteamLibrary/steamapps/common/Crusader Kings III/game/gfx/FX/pdxterrain.shader`, line 517):

```hlsl
ApplyProvinceEffectsTerrain( ConditionData, DetailDiffuse, DetailNormal, DetailMaterial, Normal, Input.WorldSpacePos, ColorMapCoords, WaterNormalLerp );
```

The mod's call site omitted `Normal` (arg 5) and `ColorMapCoords` (arg 7).

---

## 4. Architectural Analysis & Options

The architecture must decide between two approaches:

### Option A: Apply the 1.20 Call-Site Fix (Recommended)
- **Action:** Patch line 1802 in `gfx/FX/pdxterrain.shader` to pass `Normal` and `ColorMapCoords`.
- **Pros:**
  - Preserves the full EotG custom space aesthetic (void oceans, nebula tints, procedural starfield lattice, stellar wind lanes).
  - Eliminates the shader compile error cleanly.
  - Zero regression on existing mod assets or heightmap workflow.
- **Cons:** None. This was an unintended oversight during the 1.20 compatibility pass.

### Option B: Temporary Fallback to Vanilla Shaders
- **Action:** If the cartographer wants to edit heightmaps/provinces entirely decoupled from custom space shaders:
  - Temporarily rename/remove `gfx/FX/pdxterrain.shader`, `gfx/FX/eotg_terrain_params.fxh`, and `gfx/map/terrain/materials.settings`.
  - As documented in `gfx/map/terrain/README.md`, the engine falls back to vanilla Earth terrain (grass/rock/sand) without crashing.
- **Pros:** Isolate map geometry tools from custom shader code during pure heightmap sculpting.
- **Cons:** You lose space terrain visualization during editing; you still have to fix Option A before release.

---

## 5. Proposed Remediation

### 5.1 Code Change (`gfx/FX/pdxterrain.shader`)
```diff
--- a/gfx/FX/pdxterrain.shader
+++ b/gfx/FX/pdxterrain.shader
@@ -1799,7 +1799,7 @@ PixelShader =
 						float WaterNormalLerp = 0.0f;
 						EffectIntensities ConditionData;
 						BilinearSampleProvinceEffectsMask( ColorMapCoords, ConditionData );
-						ApplyProvinceEffectsTerrain( ConditionData, DetailDiffuse, DetailNormal, DetailMaterial, Input.WorldSpacePos, WaterNormalLerp );
+						ApplyProvinceEffectsTerrain( ConditionData, DetailDiffuse, DetailNormal, DetailMaterial, Normal, Input.WorldSpacePos, ColorMapCoords, WaterNormalLerp );
 
 						// Use the property that only water has lower roughness to adjust the terrain normals to face upward.
 						float WaterNormalAdjustment = smoothstep( 0.6f, 1.0f, 1 - DetailMaterial.a);
```

### 5.2 Cache Flush
After updating the file, the DirectX shader cache in the user's documents directory must be cleared:
```powershell
Remove-Item -Recurse -Force "$HOME\Documents\Paradox Interactive\Crusader Kings III\shadercache\*"
```

### 5.3 Pitfalls Documentation Update
Add this failure mode to `docs/pitfalls.md` §2 ("Stale full-file overrides"):
- Note that `ApplyProvinceEffectsTerrain` in `province_effects.fxh` gained `TerrainNormal` and `MapCoords` in 1.20, matching the symptom described in §2/§3.
