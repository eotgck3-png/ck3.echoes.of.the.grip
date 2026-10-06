# Pitfalls — things this project has got wrong more than once

Consult this **before** debugging a visual or shader problem, and add to it whenever something
costs more than one attempt.

Entries are ordered by how often they have bitten. Each one gives the **symptom** you will
actually see, the **cause**, and how to **confirm** it before changing anything — the confirm
step is the one that keeps getting skipped.

## The rule that would have saved the most time

**A change that produces no visible result is evidence, not a dead end.** It almost always means
you are editing something that is not being drawn, and the next move is to find out *what is*,
not to look for a second mechanism inside the thing you already changed.

This went wrong twice in one session, in both directions:

- Borders bloomed at maximum zoom. Sharpening the terrain shader's border alpha changed nothing
  — because the bands were border *meshes* from `pdxborder.shader`, a different system entirely
  (§1). The null result was the answer on the first try; it was read as "not strong enough" and
  the search moved on to new mechanisms instead of new systems.
- Navigable rivers kept looking like sea. Measurement said the detector should fire hard, so the
  effect should have been unmissable. The gap between "this must be visible" and "it is not" was
  the finding: the detector's floor was 0.5 rather than 0, leaving 0.04 of usable range.

The same shape appears in §13: inferring a slope from a single point. Both skip the step that
would say whether the thing being reasoned about is the thing in play.

**So:** when a change lands and nothing moves, stop and prove the code is executing before
touching a constant. A temporary diagnostic that paints the suspect system an unmistakable colour
costs one launch and ends the argument — `EOTG_DIAG_LANE` in `pdxwater.shader` is the worked
example, and it found the real bug on its first run. Say so plainly when you hand over a
diagnostic build, though: it repaints the map, and it is unkind to let someone launch expecting a
fix and get a test instrument.

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
- `pdxterrain.shader` called the old 6-argument `ApplyProvinceEffectsTerrain` (1.20 added
  `TerrainNormal` and `MapCoords`) ⇒ `PdxTerrain` / `PdxTerrainSkirt` failed to compile,
  magenta terrain under `-mapeditor`. **The normal game looked fine for a full day**: the
  call sits only in `MainCode PixelShader`, the low-spec entry point never references
  province effects, so `PdxTerrainLowSpec` still compiled and the game silently used it.
  A map that renders does NOT mean the high-spec terrain effect compiled — check
  `error.log` for `pdx_terrain.cpp` after every shader change, not just when it looks wrong.
  This one was self-inflicted: porting an `.fxh` without auditing the calls INTO it.

**Confirm.** `grep "pdx_terrain.cpp" error.log` — it names the failing effect directly. Do **not**
start from `Compile error`; the decal errors appear first and are a *symptom of a different file*.

**Prevent.** After every CK3 update, diff each override against the game's copy. A `.shader` is
self-contained and can only break itself; an **`.fxh` breaks everything that includes it**, so
check those first. Comparing which SYMBOLS exist is not enough — that is how the
`ApplyProvinceEffectsTerrain` break survived the first sweep. Compare the **arity of every
call site** against vanilla's declarations as well. Beware a naive comma split when counting
args: `float2( a, b )` reads as two, and `province_effects.fxh` is a verbatim vanilla copy,
so any mismatch reported *inside it* is a bug in the checker, not in the file — a useful
built-in control. Known drifted-but-harmless right now: `pdxwater.shader`,
`surroundmap.shader`, `clouds.fxh` (verified: nothing outside it calls `GetCloud`).

### It is not only shaders. It is every vanilla file we copy and edit.

The entries above are all `.shader`/`.fxh`, and that framing hid the real surface. Measured
2026-10-04: **108 tracked files shadow a vanilla path, across 16 directories.** None is
byte-identical to vanilla. Only `gfx/FX` had ever been checked — **12 of them, about 21% of what
can actually go stale.**

Split them before checking, or a sweep drowns in false positives:

- **Can go stale — vanilla TEXT we copied and then edited (57 files).** `map_object_data` 31
  (the largest group, and until now entirely unchecked), `gfx/FX` 12, `gfx/particles` 4,
  `gfx/map/rivers` 2, and one each of `fonts.font`, `environment.txt`, `posteffect_volumes.txt`,
  `table_styles.txt`, `materials.settings`, `water.settings`, `seasons.txt`,
  `terrain_ambience_layer_default.txt`.
- **Cannot go stale — art wholly replaced by our own generators (51 files).** `gfx/map/borders`
  35, `gfx/map/movement_arrows` 14, `colormap.dds`, `flatmap.dds`. These differ from vanilla *by
  design*; a game update cannot invalidate them, and they do not belong in a staleness check.

**Generated copies are the easy ones to forget**, because nobody edited them by hand and they
look like build output rather than like overrides. They are overrides. Anything a tool in
`docs/tools/` copies out of vanilla and rewrites — `build_marker_assets.py` for
`common/buildings/`, `strip_map_objects.py` for `gfx/map/map_object_data/` — is a vanilla
snapshot frozen at the version it was generated against, and the fix is simply to **re-run the
generator after a CK3 update**. Two real cases:

- `common/buildings/eotg_*` (2026-10-04): four of seven were pre-1.20 copies silently overriding
  1.20 gameplay. `eotg_00_tribal_buildings.txt` had lost `flag = tribe`, which produced 9
  `has_construction_with_flag 'tribe'` errors from *vanilla's* `bp2_yearly_events_6`; castle and
  temple were missing 1.20 `province_rite_modifier` blocks; the citadel had hard-coded fervor
  numbers where 1.20 uses `*_fervor_gain`. Re-running `build_marker_assets.py` fixed all four and
  preserved every marker hook.
- `gfx/particles` (1.20): vanilla renamed the compound node `"Radians to Degrees"` to
  `radians_to_degrees`, so four 1.19 bird copies could not resolve it and the engine dropped the
  node links. Cosmetic *only because those emitters are disabled anyway* — the same break in
  `map_object_data` would not have been.

**The detection is cheap and does not need the game running.** For each tracked file, test whether
the same relative path exists under the game folder; if it does, it is an override. Skip
`.dds`/`.png`/`.tga` as replaced art. Diff everything else against the current vanilla copy after
every patch. That rule alone would have caught `gfx/particles`, `map_object_data`, `seasons.txt`
and `fonts.font` the first time.

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

**Cause.** `build_terrain_hybrid.py` and `build_colormap.py` rewrite these files unconditionally, and the arguments that produced the shipped ones are not the defaults. Run either with its defaults and the map's look changes — not subtly enough to miss in game, but a `.dds` diff tells you nothing readable, and the files are gitignored by default so git will not report it either.

**They ARE reproducible, and half the recipe was already written down** — `gfx/map/terrain/README.md` has carried `build_colormap.py --level 132` all along, in the folder those files live in, and `.gitignore` even points at that README. It was not read. The `--source` image for the structure bakes genuinely was unrecorded; it is now. Verified byte-identical 2026-10-04 — 9/9 structure bakes and the colormap:

```
python docs/tools/build_terrain_hybrid.py <root> --source "<the smoked carbon-glass PNG in Downloads>"
python docs/tools/build_colormap.py <root> --level 132
```

The exact source filename is in `gfx/map/terrain/README.md`. Note `--level 132`, not the tool's default of 106.

**This was first recorded here as "irreproducible", which was wrong**, and the three ways it went wrong are the useful part:

1. **The search did not include the obvious place.** It covered the repo, the mod folder and the backup, but not `Downloads`, so "I cannot find it" was written down as "it is gone".
2. **The folder's own README was never read.** `--level 132` was sitting in `gfx/map/terrain/README.md` the whole time. Before declaring an artifact unreproducible, read the README next to it.
3. **A slope was inferred from a single data point.** The colormap was ruled out by measuring **one** level (131 → mean 131.33), assuming `mean = level + 0.33`, and extrapolating that 132 would land on 132.33 and miss the target of 131.47. It does not — 132 reproduces the file exactly. One point gives you no slope; test the neighbouring value instead of extrapolating to it.

**Rule.** Keep treating these as tracked inputs (`.gitignore` exception, 2026-10-04). The reason is not that they are irreplaceable but that they are **easy to replace wrong**, which still argues for the guard. Don't run either generator over them unless you mean to replace the look; if you do, commit the new output together with the exact command and source image. `docs/test_map/build_terrain.py` has a checksum guard that refuses to write into the main mod's `gfx/` and verifies these ten files before and after — copy that pattern before pointing any generator at the repo.

**Confirm.** `git status gfx/map/terrain/` shows them modified after any tool run. `git checkout` restores them.

## 14. A doubled BOM crashes the game, and no checker catches it

**Symptom.** The game crashes during load (EXCEPTION_ACCESS_VIOLATION). error.log has tens of thousands of `pdx_persistent_reader` errors, mostly in VANILLA files ("Named value not found: =", "Unexpected token"), and events load short (e.g. 11 of 21 in one file).

**Cause.** A mod script file that starts with two or three UTF-8 BOMs (`EF BB BF EF BB BF …`). The engine strips one BOM and reads the next as part of the first key: "Invalid scripted_value key '\ufeff'". In `common/script_values/` that corrupts the named-value table, so every later file that uses a named value (`medium_gold_value` in `gold >= { … }`, and so on) fails to parse, including vanilla files. Found 2026-10-04 in three Frontier files after a tool re-saved BOM files with `utf-8-sig` (fixed in the commit after ef514e8).

**Confirm.** error.log: `grep "Invalid scripted_value key" error.log`, or any `jomini_named_values` error naming a mod file. Or count the BOMs in every tracked text file; there should be exactly one, at byte 0:
`python -c "import subprocess;[print(f) for f in subprocess.run(['git','ls-files'],capture_output=True,text=True).stdout.split() if f.endswith(('.txt','.yml')) and open(f,'rb').read().count(b'\xef\xbb\xbf')>1]"`

**Rule.** When rewriting a file that already starts with a BOM, read it with `utf-8-sig` (which strips the BOM) before writing it with `utf-8-sig`. Tiger, PX and eotg_lint all missed this; eotg_lint is getting a rule for it.

---

## 15. `count=0` is not enough: the engine still validates the asset

**Symptom.** 99 × `Map object type has no valid asset` in `error.log` on load. Nothing looks wrong
on the map, because the objects are meant to be invisible anyway.

**Cause.** `docs/tools/strip_map_objects.py` switches off vanilla's 3D map clutter (trees, deer,
bridges, the Great Wall, map-table props) by rewriting each `object={ … }` with `count=0` and an
empty `transform`. The first version rebuilt each block from a hand-picked set of fields — `name`,
`render_pass`, `layer` — and so **dropped the `entity=` / `pdxmesh=` line**. The engine validates
the asset reference whether or not any instances are placed, so every stripped object logged an
error. 99 objects across 30 files, which is exactly the number of error lines.

**The vanilla answer was sitting right there.** Vanilla ships `coast_foam.txt` with `count=0`, and
it still carries `entity="env_coast_foam_l"`. Copy the whole declaration and change only `count`
and `transform`; do not reconstruct it from the fields you happened to think of. The script now
carries every attribute through generically rather than by listing them, because the attribute set
varies — `animals`/`env_effects` use `entity=`, `bridges`/`cliffs`/`special` use `pdxmesh=` — and
a future version may add more. It also preserved `clamp_to_water_level` and `generated_content`,
which the field list had been silently discarding too.

**Watch the performance trap in that fix.** `transform` holds one line per placed instance —
550,631 of them across these files — so a parser that accumulates its value with `buf += line`
is quadratic and turns a one-second run into minutes. Record the key, skip the body: it is
discarded on output anyway.

**Confirm.** `grep -c "no valid asset" error.log`, or offline:
`python -c "import re,glob,io;print(sum(1 for f in glob.glob('gfx/map/map_object_data/**/*.txt',recursive=True) for b in re.finditer(r'object=\{(.*?)\}',io.open(f,encoding='utf-8-sig').read(),re.S) if not re.search(r'(entity|pdxmesh)=',b.group(1))))"`
— it should print `0`.

---

## 16. Overriding a vanilla scripted trigger: copy the WHOLE block, place each line by hand

**Symptom.** None at first: an override that is subtly wrong still loads. It silently changes every caller.
`herders_and_tributary_constraints` is called by 17 casus belli groups, so one wrong line changes war for
everyone.

**What happened (Unclaimed Regions, 2026-10-06).** War immunity for unclaimed placeholders needs our flag added
to vanilla's `herders_and_tributary_constraints` (00_war_and_peace_triggers.txt). It went wrong three ways
before it shipped:
1. **The line range was wrong.** The spec said 1144-1160; the trigger runs **1144-1195**. Copying the stated range
   would have cut it off mid-block.
2. **Wrong nesting.** The instructions put our flag "beside" `government_has_flag = government_is_herder`. That line
   sits inside a `custom_tooltip`, and two triggers in one `custom_tooltip` are ANDed: "NOT (herder AND
   unclaimed)" gives no immunity at all. Our flag must be a separate child of the `NOR`.
3. **Unset scope.** The attacker line read `scope:attacker` at the top level. Vanilla only reads it inside
   `trigger_if = { limit = { exists = scope:defender } }`; at the top level it would have broken all 17 groups.
   The attacker line is root-scoped instead (root is the attacker in `allowed_for_character`).

**Rules.**
- Copy the block **programmatically**: assert the first and last lines and the next key's line, then
  check the braces balance.
- Diff the result against vanilla. The ONLY differences may be the lines you meant to add.
- Override **by key in a differently named file** (`eotg_vanilla_overrides_triggers.txt`), never by vanilla's
  path, which would replace the whole file.
- Re-copy after every CK3 update (§2).
- Tiger reports `strict-scopes ... expects scope:attacker` once per caller on the copied block. That's benign:
  the engine sets the scope, and Tiger simply doesn't report on vanilla's own copy.

**Confirm.** In game, `logs/database_conflicts.log` should show `Overriding entry
'herders_and_tributary_constraints'` naming the mod file. An ordinary claim CB must still be offered against a
non-placeholder (V-U2), which proves the attacker line didn't block everything.

