# EotG Test Map (sub-mod)

**Test map: not mod content.** This is a throwaway world for testing Echoes of the Grip's map-agnostic
systems (cybernetics, Frontier) before the real map lands. It clears B-TEMPMAP on `circlebackTaskboard.md`.
The CK3Gen source (103 provinces, titles like `e_kronos`) is deliberately left unprefixed.

## Install

1. Install the main mod first (its launcher file must be named **Echoes of the Grip**; that is B-DESCRIPTOR).
2. From the repo root:
   ```
   python docs/test_map/install.py --out "C:/Users/<you>/Documents/Paradox Interactive/Crusader Kings III/mod/eotg_test_map"
   ```
   The script:
   - copies the sub-mod to `--out`, replacing an earlier install (it refuses any other existing folder, and anything inside the repo);
   - puts the terrain textures (`detail_index.tga`, `detail_intensity.tga`, `colormap.dds`) in `<out>/gfx/map/terrain`.
     If `docs/test_map/gfx/map/terrain/` has them and they are newer than their inputs, they are copied.
     Otherwise it runs `docs/test_map/build_terrain.py --out <out>/gfx/map/terrain` (~270 MB of output).
     The textures are gitignored (too big for GitHub). `materials.settings` and the terrain masks are NOT in the
     sub-mod; they come from the main mod;
   - writes the launcher file `eotg_test_map.mod` next to the folder, with `path=` set.
3. **Next step: the heightmap.** `map_data/heightmap.heightmap` (plus the packed and indirection PNGs) can only be
   produced in game. Follow [MAPEDITOR_STEPS.md](MAPEDITOR_STEPS.md) on the installed copy.
4. In the launcher, make a playset: **Echoes of the Grip**, then **EotG Test Map** (the descriptor declares the
   dependency on it; keep it below the main mod in the load order).
5. Start the **866** bookmark "The Kronos Test Map", or pick any ruler from the map.

Re-run `install.py` after any change in `docs/test_map/`; the installed copy is not linked to the repo.

## What is in the world

28 counties, 89 baronies (provinces 1-89), 12 sea zones (90-101), one impassable sea (102).
Cultures and faiths are vanilla: the mod has none yet (B-CULTURES, B-FAITHS).

| Realm | Ruler | Culture / rite | Counties |
|---|---|---|---|
| Empire of Kronos (`e_kronos` + `k_kronos`) | Emperor Aurelian Vaskar (900001), **lead 1, easy** | greek / slavic_rite (faith christian_faith) | 16: domain c_kronos, c_aphion_seam; 4 direct counts; dukes of Graveshelf (3 vassal counts), Sanctum Wilds, Silica Span (3 vassal counts) |
| Kingdom of Skeldscar (`k_skeldscar`) | King Ragnvald Skeldung (900040), **lead 2, medium** | norse / norse_pagan | 8: domain c_skeldscar, c_helios_shoal; 2 direct counts; duke of Karak Crossing (3 vassal counts) |
| Duchy of Wyveris (`d_wyveris`, independent) | Duke Sveinn Wyvar (900060), **lead 3, hard** | norse / slavic_rite | 4: domain c_wyveris, c_emberscar; 2 vassal counts |

24 landed rulers (1 emperor, 1 king, 4 dukes, 18 counts, all `feudal_government`) and 52 characters in all.
The Skeldscar-Wyveris war over c_klian (`claim_cb`) is running at the start (Sveinn attacking, Ragnvald defending).

### Cybernetics (`docs/qa/cybernetics_test_plan.md` §1c)

- **Development 10+** (the initiation gate): c_kronos 15, c_graveshelf 12, c_skeldscar 12, c_wyveris 12, c_silica_span 11,
  and 10 on c_aphion_seam, c_caelestis, c_the_surge, c_galenus, c_skeld_cast, c_winterstead, c_klian, c_karak_crossing,
  c_skeld_haven, c_rustshard. Rulers whose capital is **below 10**, for negative tests (no offers should come):
  Anthousa (c_helix_crossing 8), Leon (c_spectral_breach 5), Isaakios (c_muth 4), Helena (c_sanctum_channel 9),
  Duke Teodor (c_sanctum_wilds 7), Nikolaos (c_the_remnant 6), Ragnhild (c_the_void 7), Orm (c_shadow_hollow 5),
  Leif (c_warpmire 3), Gyda (c_twilight_moor 4).
- **Heirs (Heir's Arc):** Lysias, 17, heir of the Emperor; Eirik, 14, heir of the King (the minimum age);
  adult heirs at Caelestis (Ioannes), Graveshelf (Alexios, 16), Silica Span (Michael) and Karak Crossing (Freyja).
- **Spouses and young children:** Emperor (Irene 13, Romanos 7), King (Halfdan 10), Duke Sveinn (Arni 8), The Surge (Sophia 13).
- **Court physician candidates:** Melitta (900007, Emperor's court) and Gunnar (900046, King's court), both
  `lifestyle_physician`, learning 14-16. Court positions are not set in history: appoint them in game.
- **Knights and courtiers:** Demetrios and Stephanos (Emperor), Thorvald and Sigrid (King), Hakon (Duke Sveinn).
- **Prisoner:** Nikephoros Arkas (900008), imprisoned by the Emperor (for "Test it on a prisoner").
- **Vassals:** the Emperor has 3 dukes and 4 direct counts; the King has a duke and 2 counts.
- **War:** leads 2 and 3 start at war.
- **50+ with low prowess:** Basil (c_caelestis, 53), Konstantin (Duke of Silica Span, 50, also cynical and learned), Vagn (c_skeld_haven, 55).
- **Diarchy / regency:** all rulers are feudal.

### Frontier (Regions = counties)

**Counties with no empty holding slot:** c_kronos, c_graveshelf, c_skeldscar, c_wyveris (every barony built).

**Counties with empty slots** (`holding = none` on every non-capital barony): the other 24, namely
c_aphion_seam, c_caelestis, c_helix_crossing, c_spectral_breach, c_the_surge, c_galenus, c_muth, c_sanctum_channel,
c_sanctum_wilds, c_reogladra, c_silica_span, c_skeld_cast, c_the_remnant, c_winterstead, c_helios_shoal, c_klian,
c_the_void, c_karak_crossing, c_shadow_hollow, c_skeld_haven, c_warpmire, c_emberscar, c_rustshard, c_twilight_moor.
Low-development ones (c_reogladra 3, c_warpmire 3, c_muth 4, c_twilight_moor 4) test the development floors (Q4).

## What `replace_path` removes, and what it keeps

Replaced (each folder ships a file here; CLAUDE.md invariant 3): `common/landed_titles`, `common/province_terrain`,
`common/bookmarks/{bookmarks,groups,challenge_characters}`, `history/{characters,titles,provinces,province_mapping,wars,struggles,situations}`,
`map_data/geographical_regions`. The reasons are commented in `descriptor.mod`.

Kept on purpose: vanilla cultures, faiths and `history/cultures` (the world uses them),
`common/dynasties`, `common/coat_of_arms`, `common/bookmark_portraits` (keyed by name, unused), `history/artifacts` (empty in vanilla),
`gfx/map/map_object_data` (CK3Gen's seven locator files override vanilla's by name; the rest are cosmetic),
and vanilla script (decisions, events, situations, struggles, holy sites) that names vanilla titles or regions.
That script logs errors and does nothing; it does not stop the game.

## Edits to the CK3Gen output

- `localization/english/titles_l_english.yml` was renamed `eotg_test_map_titles_l_english.yml`. Under the old name it
  overrode vanilla's file of the same name and deleted `TITLE_NAME`, `TITLE_TIERED_NAME` and the other title-format keys.
- `history/provinces/00_provinces.txt`: `culture`, `faith` and `rite` added on the 28 county capitals (a county with
  no culture or faith breaks), and the empty slots of the four "full" counties above filled with cities and temples.

- **Adjacency reverted (2026-10-05).** CK3Gen exported the crossing as `79;42;sea;-1;...`. A `sea` crossing needs a
  sea-zone id in `Through` (every vanilla row has one; `-1` appears only in the end-of-file row), and the comment
  contained a non-ASCII arrow. Tiger reports `expected province id`, and the import was followed by two crashes in
  a row. The file is back to just the header and the end row. Report this to CK3Gen before importing again.
- **First-load crash fix (2026-10-05).** The first launch crashed while loading history. Two vanilla files named
  titles that the test map removes, and both are now overridden by files of the same name:
  - `history/titles/ce3/00_ecclesiastical_titles.txt` is an empty file. **`replace_path` does not reach
    subfolders**, so vanilla 1.20's new `ce3/` survived `replace_path="history/titles"`.
  - `history/faiths/00_christianity.txt` is a copy of vanilla with `religious_head = k_orthodox` commented out.
    Copy it from vanilla again after a CK3 update.

- **Rites and faith history (2026-10-05).** Kronos and Wyveris use `slavic_rite`, not `byzantine_rite`. In 1.20 a rite can
  name a `founder =` title, which becomes the rite's first holder. `byzantine_rite`'s founder is `d_et_constantinople`, and
  every other Christian rite except `slavic_rite` also names a vanilla title. A missing founder title crashes history
  loading **with nothing in error.log** (found by elimination: variant C with province history crashed, D without it got
  through). **And vanilla faith history begins at 867.1.1**, the earliest vanilla bookmark. At our 866 start Christianity has no
  main rite and no rites, so any `rite =` in history crashes. `history/faiths` is therefore replaced by
  `eotg_test_map_faiths.txt`, which sets `christian_faith` (main rite `slavic_rite`) and `norse_pagan` from 1.1.1. Faiths
  nobody uses stay "non-created", which `_faith_history.info` allows. **The real 866 map needs the same thing for every faith it uses.**
  Any rite used here must have no `founder`, or a founder title that exists on this map.
- **`-mapeditor` launches cannot start a game.** Picking a bookmark with `-mapeditor` among the launch options crashes
  after "Setup powerful vassals", with or without mods. Remove it from the launch options for play tests.

- **Re-import 2026-10-05** (CK3Gen `Output/Test`): the same 103 provinces, `provinces.png`, titles and title loc. Taken
  from it: `heightmap.png`, `rivers.png`, `adjacencies.csv` (a new crossing, 79 Caelestis to 42 The Verge; since REVERTED, see below) and
  `geographical_region.txt` (adds empty `material_*` and other filler regions). Not taken: its `00_provinces.txt`
  (the raw export, without our culture, faith and holding edits above) and `gfx/map/stellar_winds_flow.png`
  (no game file reads it; it is the input for animating the Stellar Winds in the map shader, if that ever lands).

## Known gaps

- **Heightmap:** missing until MAPEDITOR_STEPS.md is done. Until then the game falls back to vanilla's heightmap files,
  which do not match this map. The map session owns this.
- **Terrain art** was built for the vanilla map; visuals may look off. `map_data/seasons.txt` from CK3Gen (vanilla's, with
  tree seasons) overrides the main mod's tree-less one while the sub-mod is loaded.
- `map_data/` also lacks vanilla's `positions.txt` and `nodes.dat`, so vanilla's are used. Watch for pathing oddities.
- **Bookmark screen:** no bookmark map image, start button or per-character highlight images (missing-texture warnings).
  The portraits are placeholders copied from vanilla. Run `dump_bookmark_portraits` in game to regenerate them.
- **Rites:** 1.20 history writes `rite = x` (vanilla does so everywhere). Tiger 1.17 predates this and reports every
  `rite`/`faith` line in this sub-mod. That is version noise.
- Vanilla script naming vanilla characters, titles and regions (e.g. `character:90028` in `07_dlc_ep3_scripted_effects.txt`)
  logs errors in `error.log`. That is expected with a replaced world.
- Not set in history: court positions, a hostile spymaster, an augmented parent (A Parent's Hardware). Use the console
  toolkit in the test plan §2.
