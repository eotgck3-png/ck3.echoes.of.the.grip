# EotG Test: British Isles (sub-mod)

**Test only, never shipped.** This sub-mod is a testing ground on the **vanilla map** while the real map is
being made. It runs with the main mod's shaders, cybernetics, Frontier and Unclaimed Regions.

- **Start:** the vanilla **1066** bookmark (1066.9.15), the same date as the Corsica sub-mod. Vanilla faith
  history starts at 867, so a 1066 start doesn't hit the 866 faith-history pitfall.
- **The test zone** is de jure `e_britannia`, `e_france` and `e_spain`. Vanilla 1.20 has no `e_francia` or
  `e_hispania`; it uses `e_france` and `e_spain`.
  - **The Isles** keep vanilla's 1066 rulers, with a mix of governments: feudal, clan, tribal, administrative,
    republic, theocracy and a landless adventurer. Four highland and western counties start **Unclaimed**.
  - **France and Spain:** 161 counties are independent **Unsworn** counties. Six small vanilla realms remain
    there as neighbours: feudal, republic, clan, theocracy, tribal and feudal. Four whole realms test the
    **mod governments**: PMC (Paris), Corporation (Brittany), Cartel (León) and Gob-Corp (Provence). Until those
    governments exist they run on feudal stand-ins; see [Mod governments](#mod-governments).
  - **Outside the zone** the map and titles are vanilla but empty.
    - Every county belongs to one of 35 inert **Off-Map** holders, one per empire, painted near-black.
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

## Mod-government realms (pockets)

Rows with `scope = pocket` in `isles_assignments.csv` (owner request 2026-10-08). Each is a whole duchy or
kingdom held by one character, with every county de jure under it in the zone. None of its counties is
Unsworn. Pick the holders **on the map**: none of them has a vanilla bookmark portrait.

| Test | Title (vanilla 1.20) | Holder | Holds himself | Vassal counts |
|---|---|---|---|---|
| PMC | `d_valois`, the Paris duchy | Philippe I (214), 14 years old | Île-de-France, Brie, Beaumont | Herbert of Vermandois (418); Raoul of Valois (40406, Valois and Amiens); Renaud of Clermont (303412) |
| Corporation | `k_brittany` | Duke Konan II (348), who also keeps `d_brittany` | Vannes, Rennes | Hoël (178, Nantes and Cornouaille); Morvan (10059, Léon); Edouarzh (346, Penthièvre) |
| Cartel | `k_leon` | Alfonso VI (108500) | León, Benavente, Salamanca | Urraca (108501, Zamora); Rodrigo (108512, Oviedo); Pedru (Pravia); a generated count in Ávila |
| Gob-Corp | `d_provence` | Count Bertrand (420) | Venaissin (Arles), Provence (Marseille, Toulon) | Jaufret (40802, Forcalquier); a generated count in Nice |

- **Vanilla 1.20 has no `d_paris` or `d_ile_de_france`.** Paris is `b_paris` in `c_ile_de_france`, the capital
  of `d_valois`, which is de jure under `k_france`.
- **The coast:** `d_provence` was picked over `d_languedoc`, the only other southern French duchy on the
  Mediterranean (`d_toulouse` is landlocked). Measured on vanilla `provinces.png`, Provence has 413 sea-edge
  pixels and 7 coastal baronies, including Marseille, Toulon, Arles and Nice. Languedoc has 187 pixels and 5
  baronies. Provence was Imperial in 1066 (liege `e_hre`); here it is independent.
- **How the holder is chosen** (`holder = auto`): the title's 1066 holder if eligible. Otherwise the 1066
  holders of the titles under it, tier by tier, with the capital's branch first. Otherwise a generated
  `eotg_test_bi_ruler_*` character with the capital's culture and rite. A holder is not eligible if he is dead,
  a churchman (ecclesiastical or theocracy title), an Isles ruler, or already landed by another row. You can
  also write a character id, or `generated`.
- **Vassals:** the holder keeps the capital county plus his own 1066 counties, up to `demesne` (default 3).
  - Every other county goes to its 1066 holder, with `liege = <pocket title>`, as vanilla history writes
    vassalage.
  - If that holder is not eligible, or is the pocket holder already at his demesne cap, the county gets a
    generated `eotg_test_bi_vassal_*` count with the county's culture and rite.
  - The holder and all vassals get the row's government.
  - De jure duchies in a kingdom stay vacant unless the holder held them in 1066 (Konan keeps `d_brittany`).
- Counties that have their own CSV row are left to that row.

### Mod governments

The four government keys (`eotg_pmc_government`, `eotg_corporation_government`, `eotg_cartel_government`,
`eotg_gobcorp_government`) are the planned names and are not defined yet. The generator has a switch:

- **`off` (the default for now):** any CSV government that is not a vanilla key is replaced by the row's
  `standin` column (blank = `feudal_government`). The sub-mod loads today, and the realms, holders and vassals
  are already in place. The `holding` column is ignored while a stand-in is used.
- **`on`:** the CSV governments are written as given. The generator **refuses** (it prints `ERROR` and
  `NOTHING WRITTEN`, and leaves the installed output untouched) if a key is not defined in vanilla, the main
  mod's `common/governments/` or this sub-mod's.

To switch on once the scripter reports the governments are built:
```
python docs/test_submods/british_isles/tools/gen_history.py --mod-governments on
```
To make it permanent, set `MOD_GOVERNMENTS_DEFAULT = 'on'` at the top of `tools/gen_history.py`. If the
architect renames a government, edit the `government` column of its row. If a government needs a particular
capital holding (for example `city_holding`), put it in the `holding` column.

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
| mainland | k_brittany | c_cornouaille | 178 HoE_l | feudal_government (stand-in for eotg_corporation_government) (vassal of 348 Konan) |
| mainland | k_brittany | c_french_leon | 10059 Morvan | feudal_government (stand-in for eotg_corporation_government) (vassal of 348 Konan) |
| mainland | k_brittany | c_nantes | 178 HoE_l | feudal_government (stand-in for eotg_corporation_government) (vassal of 348 Konan) |
| mainland | k_brittany | c_penthievre | 346 Edouarzh | feudal_government (stand-in for eotg_corporation_government) (vassal of 348 Konan) |
| mainland | k_brittany | c_rennes | 348 Konan | feudal_government (stand-in for eotg_corporation_government) |
| mainland | k_brittany | c_vannes | 348 Konan | feudal_government (stand-in for eotg_corporation_government) |
| mainland | k_burgundy | c_forcalquier | 40802 Jaufret | feudal_government (stand-in for eotg_gobcorp_government) (vassal of 420 Bertrand) |
| mainland | k_burgundy | c_nice | eotg_test_bi_vassal_nice EufE_mia | feudal_government (stand-in for eotg_gobcorp_government) (vassal of 420 Bertrand) |
| mainland | k_burgundy | c_provence | 420 Bertrand | feudal_government (stand-in for eotg_gobcorp_government) |
| mainland | k_burgundy | c_venaissin | 420 Bertrand | feudal_government (stand-in for eotg_gobcorp_government) |
| mainland | k_france | c_alencon | 140 William | feudal_government |
| mainland | k_france | c_amiens | 40406 Raoul | feudal_government (stand-in for eotg_pmc_government) |
| mainland | k_france | c_bayeux | 140 William | feudal_government |
| mainland | k_france | c_beaumont | 214 Philippe | feudal_government (stand-in for eotg_pmc_government) (vassal of 40406 Raoul) |
| mainland | k_france | c_brie_francaise | 214 Philippe | feudal_government (stand-in for eotg_pmc_government) (vassal of 40406 Raoul) |
| mainland | k_france | c_clermont | 303412 Renaud | feudal_government (stand-in for eotg_pmc_government) (vassal of 40406 Raoul) |
| mainland | k_france | c_ile_de_france | 40406 Raoul | feudal_government (stand-in for eotg_pmc_government) |
| mainland | k_france | c_reims | 91173 Gervais | ecclesiastical_government |
| mainland | k_france | c_rouen | 140 William | feudal_government |
| mainland | k_france | c_valois | 40406 Raoul | feudal_government (stand-in for eotg_pmc_government) |
| mainland | k_france | c_vermandois | 418 Herbert | feudal_government (stand-in for eotg_pmc_government) (vassal of 40406 Raoul) |
| mainland | k_leon | c_asturias_de_oviedo | 108512 Rodrigu | feudal_government (stand-in for eotg_cartel_government) (vassal of 108500 Alfonso) |
| mainland | k_leon | c_avila | eotg_test_bi_vassal_avila Facundu | feudal_government (stand-in for eotg_cartel_government) (vassal of 108500 Alfonso) |
| mainland | k_leon | c_benavente | 108500 Alfonso | feudal_government (stand-in for eotg_cartel_government) |
| mainland | k_leon | c_leon | 108500 Alfonso | feudal_government (stand-in for eotg_cartel_government) |
| mainland | k_leon | c_pravia | asturleonese0078 Pedru | feudal_government (stand-in for eotg_cartel_government) (vassal of 108500 Alfonso) |
| mainland | k_leon | c_salamanca | 108500 Alfonso | feudal_government (stand-in for eotg_cartel_government) |
| mainland | k_leon | c_zamora | 108501 Urraca | feudal_government (stand-in for eotg_cartel_government) (vassal of 108500 Alfonso) |
| mainland | k_navarra | c_ipuskoa | 200164 Beila | tribal_government |

Mod-government pockets (mod governments **off**):

| Pocket | Holder | How chosen | CSV government | Generated with | Demesne | Vassal counts |
|---|---|---|---|---|---|---|
| d_valois | 40406 Raoul | named in the CSV | eotg_pmc_government | feudal_government | c_ile_de_france, c_valois, c_amiens | c_brie_francaise: 214 Philippe; c_vermandois: 418 Herbert; c_beaumont: 214 Philippe; c_clermont: 303412 Renaud |
| k_brittany | 348 Konan | vanilla 1066 holder of d_brittany | eotg_corporation_government | feudal_government | c_vannes, c_rennes | c_nantes: 178 HoE_l; c_cornouaille: 178 HoE_l; c_french_leon: 10059 Morvan; c_penthievre: 346 Edouarzh |
| k_leon | 108500 Alfonso | vanilla 1066 holder of k_leon | eotg_cartel_government | feudal_government | c_leon, c_benavente, c_salamanca | c_zamora: 108501 Urraca; c_avila: eotg_test_bi_vassal_avila Facundu; c_asturias_de_oviedo: 108512 Rodrigu; c_pravia: asturleonese0078 Pedru |
| d_provence | 420 Bertrand | vanilla 1066 holder of d_provence | eotg_gobcorp_government | feudal_government | c_venaissin, c_provence | c_nice: eotg_test_bi_vassal_nice EufE_mia; c_forcalquier: 40802 Jaufret |

Every other county of e_france, e_spain (161) is an independent Unsworn county; every county outside the zone (3187) belongs to one of 35 offmap holders.
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
- **Off-Map holders** use the sub-mod's own `eotg_test_offmap_government`, not the Unclaimed government. If they
  used the Unclaimed government, the main mod's split would turn them into about 3,200 placeholders. They are
  mortal, and the engine picks their heirs. Two things keep a heir under the offmap government:
  - `use_as_base_on_landed` and `sticky_government` in the government;
  - a safety net on `on_title_gain`: a new holder of a county marked `eotg_test_offmap_county` at game start is
    switched to it, unless he also holds a county outside the offmap.
- **War immunity:** `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt` has the **same file name** as
  the main mod's override, so it replaces it.
  - Its body is vanilla's `herders_and_tributary_constraints` plus the main mod's two `# EOTG` lines plus two
    `# EOTG TEST` lines for offmap holders.
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
python docs/test_submods/british_isles/tools/gen_history.py [--game "<CK3>/game"] [--mod-governments on|off]
```

- It reads vanilla's `common/landed_titles`, `common/religion`, `common/culture`, `common/governments`,
  `common/holdings`, `common/bookmarks`, `common/bookmark_portraits`, `history/titles`, `history/characters`,
  `history/provinces` and `history/wars`. It also reads the main mod's trigger override and the main mod's and
  this sub-mod's `common/governments/`.
- It deletes and rewrites only its own output inside this folder.
- If the CSV has an error (an unknown title, a dead holder, an undefined mod government with
  `--mod-governments on`), it stops **before** deleting anything. The installed sub-mod keeps its last good
  output.
- It needs a **repo checkout**, because it reads the main mod at `../../../common/`.
- **To move the zone**, edit the one line `ZONE_EMPIRES = [...]` at the top. For example, add `e_germany` for the
  Low Countries; its realms then become Unsworn like France and Spain.
- **Run it again after every CK3 update.** Every override here is a vanilla snapshot (pitfalls §2).

## Known limitations

- **Vanilla-map sub-mods stop working once the main mod ships its full `map_data/`.** That applies to this one
  and Corsica alike. Today the main mod ships only `map_data/seasons.txt`, and a sub-mod can't practically ship
  the whole vanilla map back.
- **Only the 1066 start exists.** Custom start dates point at people who are now dead. Don't use them.
- **The outside world is not impassable.** Off-Map land is ordinary land with no levies and no wars. Armies can walk
  into it, but no casus belli is offered against it.
- **Generated barons:** Isles and pocket counties still get vanilla's engine-generated mayors and bishops, which is
  intended. Off-Map and Unsworn counties don't, because their non-capital baronies have no holding.
- **Tiger noise:** history is now mod files, so Tiger reports vanilla's own history quirks in them. Count only
  findings on lines marked `# EOTG TEST` or in `eotg_test_bi_*` files.
  - Tiger 1.17 also doesn't know the 1.20 `rite` field (about 78,000 lines). That is benign.
- **Not historical:** k_wales is granted to Bleddyn. Glamorgan becomes a republic, Cornwall a theocracy and
  Ireland tribal. Each changed capital barony becomes a city, temple or tribal holding.
