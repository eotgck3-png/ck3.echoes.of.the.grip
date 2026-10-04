# Pitfalls — things this project has got wrong more than once

Consult this **before** debugging a visual or shader problem, and add to it whenever something
costs more than one attempt.

Entries are ordered by how often they have bitten. Each one gives the **symptom** you will
actually see, the **cause**, and how to **confirm** it before changing anything — the confirm
step is the one that keeps getting skipped.

---

## 1. A border looks wrong → find out WHICH SCREEN first

**Symptom.** Borders look neon, too wide, or wrong-coloured. Tuning them appears to do nothing.

**Cause.** There is no single set of borders. `docs/tools/build_space_textures.py` generates
**35 textures** across several independent sets, tuned at different times:

| set | used on |
|---|---|
| `border_province` / `county` / `other_realm` / `my_realm` / `domain` | ordinary gameplay |
| `border_realm_explorer_independent` / `_vassal` | **character selection screen** |
| `border_selected_realm*` / `hovered_realm*` / `my_top_realm` / `selection_highlight` | selection and hover |
| `border_war*` / `civil_war` / `struggle*` / `epidemic` / `migrate*` | situational overlays |

Tuning the gameplay set changes nothing on the selection screen, and vice versa. This has been
"fixed" at least five times (`f7a94a8`, `69b1f5f`, `4b35668`, `89ed1f9`, and 2026-10-01), each
pass touching only the set that was visible at the time.

**Confirm.** Identify the screen from the UI in the screenshot. "Random Character", "Open For
Multiplayer", "Click to select" ⇒ character selection ⇒ `realm_explorer_*`, **not** the realm
borders.

**Also true:**
- **Border WIDTH is engine geometry, not the texture.** Proved by painting every border flat and
  full-alpha: all came out the same thickness. A border cannot be made thinner — only quieter.
- Cut **halo**, not **strength**. Cutting weight is what made borders invisible in an earlier
  pass; the core carries legibility, the halo is what becomes a slab at maximum zoom.
- Several border types draw **simultaneously** at close zoom (see `zoom_min`/`zoom_max` in
  vanilla `gfx/map/borders/settings.txt`), so thickness stacks.

---

## 2. After a CK3 update: stale full-file overrides

**Symptom.** Black map, or hundreds of errors in files the mod does not even touch.

**Cause.** The mod ships full-file copies of vanilla shaders. When the game updates, a changed
function signature or struct member breaks them. In 1.19.0.6 → 1.20.0.3 this happened twice:

- `province_effects.fxh` lost `_DivergentRites` ⇒ **278 errors in vanilla's `pdxmesh_decal.shader`
  and 7 in `tree.shader`.** An `.fxh` is *included by vanilla shaders*, so a stale one breaks
  files that have nothing to do with the mod.
- `pdxterrain.shader` called the old 5/6-argument `GetBorderColorAndBlendGame` ⇒ black map.

**Confirm.** `grep "pdx_terrain.cpp" error.log` — it names the failing effect directly. Do **not**
start from `Compile error`; the decal errors appear first and are a *symptom of a different file*.

**Prevent.** After every CK3 update, diff each override against the game's copy. A `.shader` is
self-contained and can only break itself; an **`.fxh` breaks everything that includes it**, so
check those first. Known drifted-but-harmless right now: `pdxwater.shader`,
`surroundmap.shader`, `clouds.fxh` (verified: nothing outside it calls `GetCloud`).

---

## 3. Black map = the terrain shader failed to compile

Three distinct causes so far, all producing the identical symptom:

1. **An HLSL reserved word used as an identifier** — `line`, `point`, `sample`, `texture`,
   `matrix`, `vector`, `half`, `dot`, `step`. (`33e313c`)
2. **HLSL written outside a `Code [[ ]]` block** — the config parser reads it as tokens and every
   Effect in the file dies silently.
3. **A stale vanilla function signature** (see §2).

**Comment syntax is load-bearing:** `#` outside `Code [[ ]]`, `//` inside. One wrong `//` kills
every Effect in the file.

**Pre-flight checks** that catch 1 and 2 without launching:

```bash
F=".../pdxterrain.shader"
grep -c '^\s*\[\['  "$F"; grep -c '^\s*\]\]' "$F"          # must match
awk '/^[ \t]*\[\[/{d=1;next} /^[ \t]*\]\]/{d=0;next} d==1{o+=gsub(/{/,"{"); c+=gsub(/}/,"}")} END{print o,c}' "$F"
awk '/^[ \t]*\[\[/{d=1;next} /^[ \t]*\]\]/{d=0;next} /Eotg[A-Z]/{if(d==0) print "OUTSIDE:",NR}' "$F"
```

Note `[ \t]` works in gawk but **not** in grep bracket expressions — use `\s` for grep, or the
block count silently reads 0.

---

## 4. Hard thresholds in ring sampling → banded, blotchy output

**Symptom.** A field that should be a smooth gradient comes out in visible steps or blotches.

**Cause.** N binary taps can only produce N+1 values. Hit twice: the terraced shore on the water
side, then the identical bug on the land side, because the land version used a threshold
(`0.004`) far **below** the data range it was testing (coastal land is 0.044–0.090), making every
tap return exactly 0 or 1.

**Rule.** The softness band must **straddle** the data range, not sit outside it. Add per-pixel
jitter to the ring angle as well — it decorrelates whatever quantisation survives into dither,
and beats simply adding more taps.

**Confirm.** Count distinct output values across the band in numpy before launching. 7 values is
a bug; thousands is correct.

---

## 5. The map is near-black, so every downstream value reads differently

Terrain is **unlit emissive at ~0.07**. Vanilla composites over terrain at ~0.5 lit. So anything
tuned against vanilla will be far too loud here:

- Border colour lerped over terrain ⇒ the border *replaces* the terrain instead of tinting it.
- A gradient's faint outer tail, invisible on a bright map, is a clearly visible band.
- Any effect's "subtle" default is not subtle.

**Any change to terrain brightness re-exposes all of this.** It is not a recurring bug, it is a
standing consequence — expect to retune borders and overlays whenever `EOTG_TERRAIN_LEVEL`,
`EOTG_STRUCTURE_SCALE` or the emissive gain moves.

---

## 6. Texture metrics pass; the tiling still looks wrong

**Symptom.** A texture scores inside every limit and still reads as wallpaper.

**Cause.** `local_contrast` and `peak_ratio` measure *amplitude*. They do not measure whether the
energy sits in one **large smooth shape**, which is what repeats visibly. A diffraction texture
scored better than the grid on an FFT repeat index (0.6 vs 6.4) and looked far worse, because the
repeated element was a broad lozenge whose energy spreads across many frequencies.

**Confirm.** Render **5×5 or 6×6 tiles, minified**, and look at it. That test has overturned the
metrics three times. The metrics are a gate, not a verdict.

Related: **line-mode vs cloud-mode normalisation** in `build_terrain_hybrid.py`. A thin bright
network (a grid: ~2.5% of pixels bright) keeps its peaks; a broad cloud (~24% bright) must be
clamped or it reads as snow. Choosing wrong flattens the texture to invisible or blows it out.

---

## 7. Check for a generator before hand-editing any asset

**Symptom.** You "fix" a `.dds`/`.tga`/`.settings` by hand and silently discard someone's tuning,
or the next generator run reverts you.

Most binary assets in this mod are **generated**: `build_space_textures.py` (35 border textures +
arrows + flatmap), `build_terrain_hybrid.py`, `build_terrain_index.py`, `build_colormap.py`,
`build_holding_decals.py`, `build_marker_assets.py`.

**Rule.** `ls docs/tools/` and grep for the filename before touching a generated file. Change the
generator and re-run it. (Learned by hand-writing four border `.dds` files over generated ones —
with a malformed DDS header, so they read back with zero alpha.)

---

## 8. Star-field invariants — do not undo these

- **Sample terrain at the STAR's position, not the pixel's.** `EotgStarParamsAt(starPos)` is
  deliberate: the per-pixel version cut stars off at terrain borders.
- **One continuous world lattice.** Density must *not* scale the cell size — that stretches the
  lattice across every terrain boundary. Vary **occupancy** instead.
- **No per-terrain random seed.** It would change the lattice at terrain borders, which is the
  exact province-seam artifact the design forbids. If two terrains look alike, vary their
  parameters, not their seed.
- Count scales as **occupancy × 1/cell²** — a linear occupancy map cannot produce a wide dynamic
  range, and raising occupancy past ~45% makes the lattice itself visible. To multiply star
  count, shrink the cell; to change character, change occupancy.

---

## 9. Engine constraints that look like bugs

- **Terrain texture array**: every slice must share resolution, format and mip count — *including
  vanilla textures referenced*. A mismatch is `CreateTexture2D failed` and a crash on load.
- **`materials.settings` has two top-level blocks.** Omitting the second gives
  `No section for unmasked textures`.
- **Colormap no-op is sRGB 186**, not 128 — it is soft-light blended through `pow(x, 2.2)`.
  Soft-light also cannot darken below `b²`.
- **`cw/pdxterrain.fxh` is engine-internal**, not a shipped file. `CalculateDetails` cannot be
  overridden, so the detail UV cannot be separated from the index lookup.
- **`SEA_MAT` is `eotg_desert_01`** — the sea reuses Barren Reach's material, so water cannot be
  identified from the detail index. Only the `eotg_edge_*` band is distinguishable.
- **Sampling a texture inside divergent control flow needs explicit LOD** — use `PdxTex2DLod0`.

---

## 10. Searching the game directory times out

`grep -r` over `D:/SteamLibrary/.../game` exceeds the tool timeout and so does ripgrep. Bound every
search: `game/gfx/FX` for shaders, `game/common/defines` for settings. Use `timeout 60` so a bad
pattern fails fast instead of being backgrounded.

---

## 11. Not everything is tunable

`GB_EdgeWidth`, `GB_GradientWidth`, `GB_GradientAlphaInside/Outside`, `GB_EdgeAlpha`,
`GB_PreLightingBlend` appear **only as usage** in `jomini_province_overlays.fxh`, never as a
declaration, and no settings file backs them. The gradient province overlay is engine-controlled
and **cannot be configured from a mod** — the only lever is recomputing the border from
`CalcDistanceFieldValue` in our own shader. Do not go looking for the settings file again.

## 12. Script that loads cleanly but never runs: a hook name from `.info` prose

**Symptom.** A lifted v1 system passes Tiger, every event is "fired by something", and nothing
ever happens in game.

**Cause.** v1 extended `on_yearly_playable`. That name appears only in the *comments* of vanilla
`common/on_action/_on_actions.info`. The hook the game actually fires is `yearly_playable_pulse`
(`yearly_on_actions.txt:973`; the PX Toolkit engine dump lists only that). A mod that writes
`on_yearly_playable = { on_actions = { ... } }` just defines a new on_action nobody calls, so
Tiger has nothing to complain about. All of v1's augmentation, legacy and hub flavour
(`eotg_on_actions.txt`) hung off it, so none of those events could ever have fired.

**Confirm.** `python docs/tools/px_vocab_check.py common events` reports any non-`eotg_`
top-level key in `common/on_action/` that is neither in the engine dump nor defined by vanilla.
Run it on every lift. Never take a hook name from an `.info` file without finding it defined in
a vanilla `.txt`.

## 13. Rerunning a terrain generator destroys the current map look

**Symptom.** After an unrelated terrain tweak, the terrain structure looks different and nobody changed it on purpose.

**Cause.** The `eotg_structure_{a,b,c}_{diffuse,normal}.dds` bakes in game since 2026-10-01 came from `docs/tools/build_terrain_hybrid.py --source <image>` run against an image that isn't in the repo and can't be found. No invocation of the committed tool reproduces them: procedural, `eotg_hologram_source.png` and `--cloud` all give 0/6 matches. The tool is deterministic and unchanged since 09-27. `build_terrain_hybrid.py` rewrites these files unconditionally.

**Same trap, second case:** `gfx/map/terrain/colormap.dds` (09-25) predates the only committed `build_colormap.py` (643b6e7, 09-26). No `--level` or `--drift` reproduces it: the default output is visibly darker (mean 106 vs 131). Only the holding decals (`build_holding_decals.py`) were verified to reproduce byte for byte.

**Rule.** These files (9 structure bakes + colormap) are tracked inputs now (`.gitignore` exception, 2026-10-04). Don't run `build_terrain_hybrid.py` or `build_colormap.py` over them unless you mean to replace the look. If you do, commit the new bakes together with the exact command and its source image.

**Confirm.** `git status gfx/map/terrain/` shows them modified after any tool run. `git checkout` restores them.
