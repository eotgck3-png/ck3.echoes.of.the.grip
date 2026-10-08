# EotG Test: British Isles (sub-mod)

**Test only, never shipped.** This sub-mod is a testing ground on the **vanilla map** while the real map is
being made. It runs with the main mod's shaders, cybernetics, Frontier and Unclaimed Regions.

- **Start:** the vanilla **1066** bookmark (1066.9.15), the same date as the Corsica sub-mod. Vanilla faith
  history starts at 867, so a 1066 start doesn't hit the 866 faith-history pitfall.
- **The test zone** is de jure `e_britannia`, `e_france` and `e_spain`. Vanilla 1.20 has no `e_francia` or
  `e_hispania`; it uses `e_france` and `e_spain`.
  - **The Isles** keep vanilla's 1066 rulers, with a mix of governments: feudal, clan, tribal, administrative,
    republic, theocracy and a landless adventurer. Four highland and western counties start **Unclaimed**.
  - **France and Spain:** 185 counties are independent **Unsworn** counties. Six small vanilla realms remain
    there as neighbours: feudal, republic, clan, theocracy, tribal and feudal.
  - **Outside the zone** the map and titles are vanilla but empty.
    - Every county belongs to one of 35 inert **Void** holders, one per empire, painted near-black.
    - Their non-capital baronies have no holding.
    - Every living history character out there dies the day before the start.
    - Nothing out there plays, raises troops or goes to war.

Everything under `history/`, `common/bookmarks/`, `common/scripted_triggers/` and
`localization/english/eotg_test_bi_generated_l_english.yml` is **generated** by `tools/gen_history.py`, so don't
edit it by hand. To change who rules what, edit the two CSV files and regenerate.

## Install

1. **Run the generator. This step is mandatory.** The generated output (`history/`, `common/bookmarks/`,
   `common/scripted_triggers/`, `localization/`) is not committed. `descriptor.mod` declares
   `replace_path="history/titles"`, so loading the sub-mod without generating replaces vanilla's title history
   with a missing folder. That is the silent history-load crash in `docs/pitfalls.md`.
   ```
   python docs/test_submods/british_isles/tools/gen_history.py
   ```
   - Run it from a **repo checkout**: it reads the main mod's `common/scripted_triggers/` override three folders up.
   - It takes up to about 100 s, prints a summary and ends with `OK`.
   - Any `ERROR:` or `VALIDATION:` line means it wrote something you shouldn't load.
   - Run it again after any CSV edit, CK3 update, or change to the main mod's trigger override.
2. Copy this folder to `Documents/Paradox Interactive/Crusader Kings III/mod/eotg_test_british_isles`.
   You can leave out `tools/`, `*.csv` and this README.
3. Write `mod/eotg_test_british_isles.mod` with the contents of `descriptor.mod` (including its `replace_path`
   line), plus `path="<that folder>"`.
4. **Playset order:** **Echoes of the Grip** first, then **EotG Test: British Isles**.
   - Don't load the EotG Test Map: it replaces the vanilla map.
   - Don't load the Corsica/Sardinia sub-mod (`frontier_vanilla`): Italy is outside this zone. It is a separate
     playset.
5. Start a **new game**. This only works from the 1066 bookmark, and the setup runs on `on_game_start`.

## Start characters

The bookmark screen lists only characters who have a **vanilla bookmark portrait**. Tiger reports a missing
portrait as a crash, and portraits can't be made outside the game. Everyone else is **picked on the map**: use
the bookmark, then click their realm.

| Character (history id) | Title | Government | Where |
|---|---|---|---|
| **Edwin of Mercia (5644)**, the main test start: a feudal duke with vassals | d_lancaster + d_hereford, vassal of England | feudal | map |
| **Murchad ua Briain (83355)**, the tribal start, with a vassal in Ormond | d_munster | tribal | bookmark |
| Harold Godwinson (122) | k_england | feudal | bookmark |
| Malcolm III (984) | k_scotland | clan (his vassals too) | bookmark |
| Bleddyn ap Cynfyn (6358) | k_wales (granted for the test; not vanilla) | administrative | map |
| Cadwgan ap Meurig (6362) | c_glamorgan + c_monmouthshire | republic | map |
| Cadoc (161281) | c_cornwall, independent | ecclesiastical (theocracy) | map |
| Hereward the Wake (90028) | d_laamp_wake | landless adventurer (vanilla) | bookmark |
| William of Normandy (140) | d_normandy + c_rouen, c_bayeux, c_alencon | feudal | bookmark |

Clan was chosen for Scotland because 1.20 `clan_government` has no faith or culture gate. The Durham and
Worcester bishops keep vanilla's `ecclesiastical_government` under feudal England.

**The France/Spain pockets** (all independent): William of Normandy (feudal, above); the Taifa of Córdoba
(20852; republic, as in vanilla); the Taifa of Toledo (3924; clan); the Archbishop of Reims (91173;
ecclesiastical); Gipuzkoa (200164; tribal); and Barcelona (110520; feudal count).

**Unclaimed in the Isles:** `c_caithness`, `c_sutherland` and `c_ross` in the Highlands, and `c_mayo` in
Connacht.
- Each has its own pre-made Unsworn placeholder with the county's 1066 culture and rite.
- `c_sutherland` also starts **Unknown** (Frontier Phase 3a).
- The Scottish and Irish realms around them can try *Raise Your Colours*.

## Assignments (generated)

`isles_assignments.csv` is the editable table (its header explains every column). `bookmark_characters.csv` lists
the bookmark entries. The table below is rewritten by the generator.

<!-- BEGIN GENERATED TABLE -->
| Zone | Kingdom | County | Holder at 1066.9.15 | Government |
|---|---|---|---|---|
| isles | k_england | c_bedford | 131 Eadgifu | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_berkshire | 122 Harold | feudal_government |
| isles | k_england | c_buckinghamshire | 131 Eadgifu | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_cambridgeshire | 132 Gyrth | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_cheshire | 90027 Eadric | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_cornwall | 161281 Cadoc | ecclesiastical_government |
| isles | k_england | c_cumberland | 963 Dolfin | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_derby | 5644 Eadwin | feudal_government (vassal of 122 Harold) |
| isles | k_england | c_devon | 101534 Gyda | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_dorset | 115 Eadmund | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_durham | 131601 E_thelwine | vanilla (ecclesiastical_government) (vassal of 122 Harold) |
| isles | k_england | c_east_riding | 5660 Morcar | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_essex | 132 Gyrth | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_gloucestershire | 82040 Wulfstan | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_hampton | 122 Harold | feudal_government |
| isles | k_england | c_hertfordshire | 131 Eadgifu | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_huntingdonshire | 198 Waltheof | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_isle_of_wight | 122 Harold | feudal_government |
| isles | k_england | c_kent | 5604 Stigand | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_lancashire | 5644 Eadwin | feudal_government (vassal of 122 Harold) |
| isles | k_england | c_leicestershire | 5644 Eadwin | feudal_government (vassal of 122 Harold) |
| isles | k_england | c_lincolnshire | 5660 Morcar | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_middlesex | 122 Harold | feudal_government |
| isles | k_england | c_norfolk | 5650 Ralf | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_north_riding | 5660 Morcar | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_northamptonshire | 198 Waltheof | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_northumberland | 191 Osulf | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_nottinghamshire | 5644 Eadwin | feudal_government (vassal of 122 Harold) |
| isles | k_england | c_oxfordshire | 122 Harold | feudal_government |
| isles | k_england | c_shropshire | 90027 Eadric | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_somerset | 115 Eadmund | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_staffordshire | 113 Margaret | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_suffolk | 132 Gyrth | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_surrey | 130 Leofwine | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_sussex | 130 Leofwine | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_warwickshire | 112 Eadgar | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_west_riding | 5660 Morcar | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_westmorland | 191 Osulf | vanilla (default) (vassal of 122 Harold) |
| isles | k_england | c_wiltshire | 122 Harold | feudal_government |
| isles | k_england | c_worcestershire | 82040 Wulfstan | vanilla (ecclesiastical_government) (vassal of 122 Harold) |
| isles | k_ireland | c_ailech | 929 A_ed | tribal_government |
| isles | k_ireland | c_athlone | 6120 Conchobar | tribal_government |
| isles | k_ireland | c_breifne | 1000 A_ed | tribal_government |
| isles | k_ireland | c_connacht | 910 A_ed | tribal_government |
| isles | k_ireland | c_desmond | 83252 Muiredach | tribal_government |
| isles | k_ireland | c_dublin | 924 Murchad | tribal_government |
| isles | k_ireland | c_ennis | 83355 Murchad | tribal_government |
| isles | k_ireland | c_leinster | 922 Diarmait | tribal_government |
| isles | k_ireland | c_mayo | eotg_test_bi_unsworn_mayo | Unclaimed (Unsworn placeholder) |
| isles | k_ireland | c_oriel | 930 Domnall | tribal_government |
| isles | k_ireland | c_ormond | 83370 RO_gnvaldr | tribal_government (vassal of 83355 Murchad) |
| isles | k_ireland | c_ossory | 1020 Domnall | tribal_government |
| isles | k_ireland | c_thomond | 83355 Murchad | tribal_government |
| isles | k_ireland | c_ulster | 6180 CU__Uladh | tribal_government |
| isles | k_scotland | c_angus | 994 Malmure | clan_government (vassal of 984 Malcolm) |
| isles | k_scotland | c_annandale | 166433 Malcolm | vanilla (default) (vassal of 122 Harold) |
| isles | k_scotland | c_argyll | 131104 Gilla-BrI_gte | vanilla (feudal_government) (vassal of 5788 GudrOEd) |
| isles | k_scotland | c_atholl | 994 Malmure | clan_government (vassal of 984 Malcolm) |
| isles | k_scotland | c_ayrshire | 131526 Comgal | vanilla (feudal_government) (vassal of 5788 GudrOEd) |
| isles | k_scotland | c_buchan | 131006 CinA_ed | clan_government (vassal of 984 Malcolm) |
| isles | k_scotland | c_caithness | eotg_test_bi_unsworn_caithness | Unclaimed (Unsworn placeholder) |
| isles | k_scotland | c_carrick | 131526 Comgal | vanilla (feudal_government) (vassal of 5788 GudrOEd) |
| isles | k_scotland | c_dunbar | 85018 Gospatric | clan_government (vassal of 984 Malcolm) |
| isles | k_scotland | c_fife | 131002 Duib | clan_government (vassal of 984 Malcolm) |
| isles | k_scotland | c_galloway | 131525 Fionnghall | vanilla (feudal_government) (vassal of 5788 GudrOEd) |
| isles | k_scotland | c_gowrie | 984 Malcolm | clan_government |
| isles | k_scotland | c_inner_hebrides | 5788 GudrOEd | vanilla (feudal_government) |
| isles | k_scotland | c_inverness | 6008 MA_elSnechtai | clan_government (vassal of 984 Malcolm) |
| isles | k_scotland | c_isle_of_man | 131524 Gofraid | vanilla (feudal_government) |
| isles | k_scotland | c_lanarkshire | 82001 Eadulf | clan_government (vassal of 984 Malcolm) |
| isles | k_scotland | c_lennox | 984 Malcolm | clan_government |
| isles | k_scotland | c_linlithgowshire | 984 Malcolm | clan_government |
| isles | k_scotland | c_lothian | 85018 Gospatric | clan_government (vassal of 984 Malcolm) |
| isles | k_scotland | c_mearns | 994 Malmure | clan_government (vassal of 984 Malcolm) |
| isles | k_scotland | c_moray | 6008 MA_elSnechtai | clan_government (vassal of 984 Malcolm) |
| isles | k_scotland | c_outer_hebrides | 131526 Comgal | vanilla (feudal_government) (vassal of 5788 GudrOEd) |
| isles | k_scotland | c_ross | eotg_test_bi_unsworn_ross | Unclaimed (Unsworn placeholder) |
| isles | k_scotland | c_strathearn | 82011 Murethach | clan_government (vassal of 984 Malcolm) |
| isles | k_scotland | c_sutherland | eotg_test_bi_unsworn_sutherland | Unclaimed (Unsworn placeholder) |
| isles | k_scotland | c_teviotdale | 82001 Eadulf | clan_government (vassal of 984 Malcolm) |
| isles | k_wales | c_anglesey | 6358 Bleddyn | administrative_government |
| isles | k_wales | c_brecknockshire | 131704 Bleddyn | vanilla (default) (vassal of 138496 Maredudd) |
| isles | k_wales | c_caernarfonshire | 6358 Bleddyn | administrative_government |
| isles | k_wales | c_cardiganshire | 138496 Maredudd | vanilla (default) |
| isles | k_wales | c_carmarthenshire | 138496 Maredudd | vanilla (default) |
| isles | k_wales | c_denbighshire | 81841 Maredudd | administrative_government (vassal of 6358 Bleddyn) |
| isles | k_wales | c_glamorgan | 6362 Cadwgan | republic_government |
| isles | k_wales | c_hereford | 82040 Wulfstan | vanilla (default) (vassal of 122 Harold) |
| isles | k_wales | c_maldwyn | 40504 Rhiwallon | administrative_government (vassal of 6358 Bleddyn) |
| isles | k_wales | c_merioneth | 6358 Bleddyn | administrative_government |
| isles | k_wales | c_monmouthshire | 6362 Cadwgan | republic_government |
| isles | k_wales | c_pembrokeshire | 138496 Maredudd | vanilla (default) |
| isles | k_wales | c_sir_faesyfed | 40504 Rhiwallon | administrative_government (vassal of 6358 Bleddyn) |
| mainland | k_andalusia | c_cabra | 20852 Abd-al-Malik | republic_government |
| mainland | k_andalusia | c_calatrava | 3924 Yahya | clan_government |
| mainland | k_andalusia | c_cordoba | 20852 Abd-al-Malik | republic_government |
| mainland | k_andalusia | c_toledo | 3924 Yahya | clan_government |
| mainland | k_aragon | c_barcelona | 110520 Ramon-Berenguer | feudal_government |
| mainland | k_aragon | c_girona | 110520 Ramon-Berenguer | feudal_government |
| mainland | k_france | c_alencon | 140 William | feudal_government |
| mainland | k_france | c_bayeux | 140 William | feudal_government |
| mainland | k_france | c_reims | 91173 Gervais | ecclesiastical_government |
| mainland | k_france | c_rouen | 140 William | feudal_government |
| mainland | k_navarra | c_ipuskoa | 200164 Beila | tribal_government |

Every other county of e_france, e_spain (185) is an independent Unsworn county; every county outside the zone (3187) belongs to one of 35 void holders.
<!-- END GENERATED TABLE -->

## How it is built (why it loads)

- **Map and titles stay vanilla.** The owner asked for an impassable outside world, but that would have meant
  deleting about 4,400 counties and 10,400 baronies. About 8,000 references in about 600 vanilla files name those
  titles (decisions, on_actions, holy sites, rites, regions), and each is a possible silent load crash. Holding
  them with a few inert characters gets nearly the same load and tick saving without that risk (owner decision
  M1, 2026-10-08).
- **`replace_path="history/titles"`** is the only folder replaced. The sub-mod ships a **complete** copy:
  - all 184 vanilla title-history files, each with one `1066.9.15` block added to every title whose holder
    changes;
  - any vanilla block that was on 1066.9.15 itself moved to 1066.9.13.

  It is never an empty folder (pitfalls: silent history-load crashes). Without the replace, a vanilla title
  history file added by a CK3 patch would bring real rulers back outside the zone.
- **Every other history change overrides vanilla files by name**, as vanilla-byte copies with a few lines added,
  each marked `# EOTG TEST`:
  - `history/characters`: the out-of-zone death lines;
  - `history/provinces`: `holding = none` and the capital holding changes;
  - `history/wars`: the four wars active on 1066.9.15 removed, including Hastings and Stamford Bridge;
  - three struggle/situation histories: the Great Steppe, and the TGP dynastic cycle and silk road. Vanilla
    starts these only behind a DLC check, so everything copes with their absence.
- **Characters are retired, not deleted.** Out-of-zone characters alive at the start get
  `1066.9.14 = { death = yes }`, and their later history blocks are dropped.
  - Every reference to them (father, spouse, title history) still resolves to a dead character, so no
    reference dangles.
  - Kept alive: holders in the zone, their spouses, parents, children and siblings, every character of an
    Isles culture, and the holders of faith-head and Isles landless titles. That includes the Pope, the
    archbishops of York and Canterbury, and Hereward.
  - A kept family member whose vanilla employer is retired is moved to a landed relative with
    `1066.9.15 = { employer = ... }`: Tostig (124) goes to his mother Gyda (101534). A kept ruler keeps their
    vanilla employer line: Ælfwine (161260) is a landless adventurer whose employer (336) is retired.
  - Characters born on or after 1066.9.14 are never retired.
- **Liege check:** every title with a holder, the kept faith-head titles included, gets `liege = 0` if its
  vanilla liege title is vacant at the start. For example, d_sunni and d_patriarchate_in_the_east had
  k_persia, d_coptic_papacy and d_samaritan had k_egypt, and d_apostolic_church had k_armenia.
- **The Unsworn are pre-made history characters**: one per Unclaimed county, with `eotg_unclaimed_folk` and
  `government = eotg_unclaimed_government`.
  - The main mod's `eotg_unclaimed_game_start_effect` adopts each one as it is, so there is no
    `create_character` and no title transfer at game start.
  - That is lighter than the single-seed split: about 190 adoptions against 190 creations and transfers.
- **Void holders** use the sub-mod's own `eotg_test_void_government`, not the Unclaimed government. If they
  used the Unclaimed government, the main mod's split would turn them into about 3,200 placeholders. They are
  mortal, and the engine picks their heirs. Two things keep a heir under the void government:
  - `use_as_base_on_landed` and `sticky_government` in the government;
  - a safety net on `on_title_gain`: a new holder of a county marked `eotg_test_void_county` at game start is
    switched to it, unless he also holds a county outside the void.
- **War immunity:** `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt` has the **same file name** as
  the main mod's override, so it replaces it.
  - Its body is vanilla's `herders_and_tributary_constraints` plus the main mod's two `# EOTG` lines plus two
    `# EOTG TEST` lines for void holders.
  - The generator asserts that the diff from vanilla is exactly those four lines (pitfalls §16).
  - **Regenerate whenever the main mod's override, or vanilla's trigger, changes.** The generator stops if the
    main mod's file is no longer vanilla plus its two lines.
- **Bookmark:** `00_bookmarks.txt` and `00_bookmark_groups.txt` are overridden by name, leaving only
  `bm_1066_hastings` in `bm_group_1066`. The 867 and 1178 starts are gone, because their title history no longer
  exists.
- **Challenge characters:** `00_challenge_characters.txt` is overridden by name (generated). It keeps only the
  1066.9.15 entries whose character is alive and still holds the listed title here: Eadgar of Warwickshire
  (112), Guðrøðr of the Western Isles (5788) and Ramon Berenguer of Barcelona (110520).

## Regenerate

```
python docs/test_submods/british_isles/tools/gen_history.py [--game "<CK3>/game"]
```

- It reads vanilla's `common/landed_titles`, `common/religion`, `common/culture`, `common/governments`,
  `common/bookmarks`, `common/bookmark_portraits`, `history/titles`, `history/characters`, `history/provinces`
  and `history/wars`, plus the main mod's trigger override.
- It deletes and rewrites only its own output inside this folder.
- It needs a **repo checkout**, because it reads the main mod's override at `../../../common/scripted_triggers/`.
- **To move the zone**, edit the one line `ZONE_EMPIRES = [...]` at the top. For example, add `e_germany` for the
  Low Countries; its realms then become Unsworn like France and Spain.
- **Run it again after every CK3 update.** Every override here is a vanilla snapshot (pitfalls §2).

## Known limitations

- **Vanilla-map sub-mods stop working once the main mod ships its full `map_data/`.** That applies to this one
  and Corsica alike. Today the main mod ships only `map_data/seasons.txt`, and a sub-mod can't practically ship
  the whole vanilla map back.
- **Only the 1066 start exists.** Custom start dates point at people who are now dead. Don't use them.
- **The outside world is not impassable.** Void land is ordinary land with no levies and no wars. Armies can walk
  into it, but no casus belli is offered against it.
- **Generated barons:** Isles and pocket counties still get vanilla's engine-generated mayors and bishops, which is
  intended. Void and Unsworn counties don't, because their non-capital baronies have no holding.
- **Tiger noise:** history is now mod files, so Tiger reports vanilla's own history quirks in them. Count only
  findings on lines marked `# EOTG TEST` or in `eotg_test_bi_*` files.
  - Tiger 1.17 also doesn't know the 1.20 `rite` field (about 78,000 lines). That is benign.
- **Not historical:** k_wales is granted to Bleddyn. Glamorgan becomes a republic, Cornwall a theocracy and
  Ireland tribal. Each changed capital barony becomes a city, temple or tribal holding.
