# Glossary proposal: medieval UI terms, tier words and terrain words (CB-08)

> **Orchestrator note (2026-10-04):** written before the canon precedence ruling. The dated `docs/lore/` entries now outrank the SETTING LORE body (see `docs/lore/REVIEW_866.md`). Re-check canon claims here against that digest before acting on them. This is a proposal, not a ruling.


> **This is a proposal. It decides nothing.** It is static and unvalidated: a cloud session wrote it with no game files, no Tiger and no PX. It is built from `OLD PROJECT VERSION/` and the v2 root. Anything that depends on how the engine behaves is marked `UNVERIFIED-VANILLA`. The human rules on every option here, and eotg-localizer carries out the ruling.
>
> **Date:** 2026-10-04 · **Branch:** `claude/canon-void-glossary-cloud`

## 0. Scope

**What CB-08 asks** (`circlebackTaskboard.md`):
> "cybernetics text uses vanilla UI terms: court, courtier, vassal, knight, household, gold, liege. The interim ruling keeps terms that match the game UI the player sees. A real decision would go in the reflavor glossary and `localization/english/replace/`."

**What is folded in from `docs/qa/v1_lift_readiness_cloud.md`:**
- §3 item 5: tier words against terrain words (System, Region, Sector, Expanse, Cluster).
- The §2 RP findings:
  - prose that still says "County";
  - "Region" also used by intake;
  - the "Strike Speeders" name clash;
  - "Void" used for ordinary space;
  - substitutions missing from the glossary;
  - ruler ranks never overridden.

**Where `replace/` lives.** v2 has no `localization/english/replace/` yet. Every `replace/X` path below means the v1 copy at `OLD PROJECT VERSION/localization/english/replace/X`: 52 files, rated READY-WITH-FIXES by the audit.

**What was not opened** (by instruction): the v2 cybernetics loc, script and specs, `gfx/` and `map_data/`. Whatever is ruled here, the localizer must grep the cybernetics loc afterwards for each term.

**The real glossary is misquoted in v2 files.** The real glossary (`OLD PROJECT VERSION/docs/localization_crusade.md:15-27`) is:

| Vanilla | Mod term |
|---|---|
| Barony | System |
| County | Region |
| Duchy | Sector |
| Kingdom | Expanse |
| Empire | Cluster |
| Castle | Bastion |
| City | Port |
| Temple | Sanctum |
| Tribe | Clanhold |
| Peasant | Commoner |
| Serf | Bonded worker |

Two v2 files misquote it, and the localizer applies the wrong version to new text:
- `.claude/agents/eotg-localizer.md`:
  - line 3 calls it "the County->System glossary";
  - line 25 says "County→System, Duchy→Sector, castles→holdings, peasants→commoners". That is wrong twice: System is the barony word, and castles become **Bastion**, not "holdings".
- `OLD VERSION CATALOG.md:26,91` repeats the same errors.

This is an orchestrator fix (audit `:268`).

---

## 1. Principles (proposed)
1. **Rename only what the player reads as a UI term.**
   - Overriding a concept's display key (e.g. `game_concept_county:0 "Region"`, `replace/eotg_holdings_concepts_l_english.yml:78`) changes every `[county|E]` link and every `$game_concept_county$` self-reference (`localization_crusade.md:65-72`).
   - Plain prose does not follow a concept rename. Every rename therefore leaves mixed text until the prose is swept (§4 is a live example).
   - So rename only where the prose sweep is affordable, or where mixed text is tolerable.
2. **One concept, one word, and one word, one concept.** No tier word may double as a terrain, building, unit, canon entity or player-facing docs term.
3. **Tier words are reserved.** In player text, System, Region, Sector, Expanse and Cluster (any case, singular or plural) mean the title tier only. Lowercase "system" meaning a mechanism is tolerated.
4. **Other reserved words:**
   - **Void**: the canon entity (SETTING LORE `:10-16`; CB-11).
   - **Grip**: the canon cataclysm.
   - **Fringe**: a v1 government.
   - **Belt Claims**: a building (`localization_crusade.md:117`).
   - **Strike Speeders**: the mod's own men-at-arms.
5. **Keep a vanilla term when renaming costs more than it gains.** Feudal-space words (court, vassal, liege) read naturally in the genre. Words that break immersion are the ones to remove: horses, peasants, castles, wheat.
6. **Multi-species, space setting.** No term should assume humans or planets. Species- or culture-flavoured variants come later, at culture or government level, from intake briefs.
7. **The glossary governs player-facing loc only.** Docs, specs, intake briefs and canon notes keep the vanilla tier words. The ERRATA itself says "THREE COUNTIES … DIFFERENT duchies".
8. **Reflavor goes through `replace/` concept keys,** with one definition per key (invariant 6). `UNVERIFIED-VANILLA`: does `replace/` override by key regardless of filename? None of the 52 file names matches a vanilla file name (audit `:253`).
9. **No guessed lore.** Currency and FTL-lane words go to lore-keeper and the vault.

---

## 2. CB-08 term table

**How to read the counts:**
- **"raw"** = `grep -c -i -w` hits, which include keys, comments and links.
- **"prose values"** = value lines containing the word or its inflections after stripping `[...]` and `$...$`.
- **"v1 mod"** = the 32 non-augmentation v1 loc files. Most hits there are in government files from the rewrite column.
- **"replace"** = the 52 `replace/` files.

The `game_concept_*` names in the last column are `UNVERIFIED-VANILLA`, inferred from `game_concept_county` / `_counties`. vanilla-scout must confirm them.

| Term | `replace/` today | Occurrences | Options | Recommendation | Keys touched if renamed |
|---|---|---|---|---|---|
| **court** | Not renamed; kept as a link (`replace/eotg_story_cycles_commoner_l_english.yml:33`, `replace/eotg_story_cycles_l_english.yml:37`) | v1 mod: raw 103, prose 100 (mostly elven gov files; lift column: void 11, legacy 5). replace: raw 53, prose 18 | (a) keep; (b) "Retinue"; (c) "Hall" | **(a) keep.** Genre-native, and a rename would leave vanilla prose saying "court". | `game_concept_court(s)` (+ grandeur and position concepts) |
| **courtier** | Not renamed (e.g. `replace/eotg_hunt_events_l_english.yml:20`) | v1 mod: prose 2. replace: raw 4, prose 8 | (a) keep; (b) "Retainer"; (c) "Attendant" | **(a) keep.** It stands or falls with "court". | `game_concept_courtier(s)` |
| **vassal** | Not renamed; linked (`replace/eotg_holdings_concepts_l_english.yml:88`, `replace/eotg_game_concepts_wars_commoner_l_english.yml:14,19`, `replace/eotg_burgher_corvee_concepts_l_english.yml:41`) | v1 mod: raw 21, prose 28. replace: raw 8, prose 9 | (a) keep; (b) "Client"; (c) "Subordinate"; government flavour (e.g. corporate "subsidiary") lives in government loc | **(a) keep** in the generic glossary. Per-government wording belongs to the governments rewrite. | `game_concept_vassal(s)` |
| **knight** | Deliberately not renamed. The `$…$` passthroughs go to the culture's MountedWarriorTerm (`replace/eotg_custom_loc_wordbank_l_english.yml:23-25`). `localization_crusade.md:87`: "arguably setting-appropriate" (321 vanilla lines). | v1 mod: prose 4. replace: raw 8, prose 4 | (a) keep generic, reflavour per culture later (mechanism `UNVERIFIED-VANILLA`); (b) "Champion"; (c) "Paladin" | **(a).** Canon has Elrossi Holy Orders as "crusading forces" (`localization_crusade.md:163-165`). | `game_concept_knight(s)`; under (a), culture-level keys only |
| **household** | Not renamed (e.g. `replace/eotg_misc_rules_diarchy_raids_l_english.yml:67`) | v1 mod: prose 6. replace: prose 2 | (a) keep; (b) "crew" in some government contexts | **(a) keep.** Neutral word. | none, unless a concept exists (`UNVERIFIED-VANILLA`) |
| **gold** | Not renamed. Some uses mean the metal, not money (`replace/eotg_sin_sermon_serf_misc_l_english.yml:87`). | v1 mod: raw 43, prose 42 (governments, mostly). replace: raw 17, prose 13 | (a) keep; (b) "Credits"; (c) a canon currency name (none exists in SETTING LORE) | **Ask the vault; keep "Gold" until it answers.** "Credits" changes what the icon means (B-ART) and needs a coin, purse and hoard prose sweep. | `game_concept_gold` + forms; icon text |
| **liege** | Not renamed; linked (`replace/eotg_game_concepts_wars_commoner_l_english.yml:14,19`) | v1 mod: 0. replace: raw 26, prose 18 | (a) keep; (b) "Overlord" (vanilla may use it elsewhere, `UNVERIFIED-VANILLA`); (c) "Patron" | **(a) keep.** Paired with vassal: rename both or neither. | `game_concept_liege(s)` |
| **Ruler ranks** (Baron, Count, Duke, King, Emperor; audit `:251`) | Not overridden, so the UI shows "Count of X (Region)". `replace/eotg_title_tiers_l_english.yml:14-15` leaves culture variants alone. Visible seam: `replace/eotg_holdings_concepts_l_english.yml:88` "[counts\|E] as [vassals\|E]". | replace: count 2 (+1 link), king/queen 3, emperor 3 | (a) keep the medieval ranks; (b) a neutral ladder (needs lore); (c) keep generic, add culture and government ranks from intake | **(a) now, (c) later.** | the generic ruler-title keys in vanilla `culture_titles_l_english.yml` (`UNVERIFIED-VANILLA`) |

---

## 3. Tier words and terrain words

### 3.1 Where each word collides
The tier words are set in `replace/eotg_holdings_concepts_l_english.yml:76-85`, `replace/eotg_title_tiers_l_english.yml:46-92` and `localization_crusade.md:17-21`.

| Word | As a tier | As a v1 terrain | As a v2 terrain | Other uses |
|---|---|---|---|---|
| **System** | Barony (`holdings_concepts:76-77`, `title_tiers:46,96`) | `replace/eotg_terrains_l_english.yml:17-18` "Flooded System Expanse" | `docs/terrain_scheme.md:41` "Sanctuary Systems" | `replace/eotg_traditions_l_english.yml:37` "Systems Engineers"; lowercase at `traditions:6,27,38,53,56,61` |
| **Region** | County (`holdings_concepts:78-79,91-102`, `title_tiers:56,97`) | `terrains:3-4` "Asteroid Belt Region" | — | intake (§5.5); script `geographical_region` ids; lowercase at `traditions:12,15,18,21,27,33,50,56,124` |
| **Sector** | Duchy (`holdings_concepts:80-81`, `title_tiers:66`) | `terrains:5-6` "Fortified Sector", `:22` "Failing Frontier Sector"; wordbank `:48` | — | `traditions:20` "Fortified Sector Dwellers", `:78` "Sector Isolationism" |
| **Expanse** | Kingdom (`holdings_concepts:82-83`, `title_tiers:76,80`; tribal empire "High Expanse" `:90`) | `terrains:2` "Open Transit Expanse", `:17-18`, `:19` "Longlane Expanse"; wordbank `:44,53` | — | `traditions:29,30`; `OLD PROJECT VERSION/localization/english/eotg_maa_l_english.yml:30`; title names "The Lanius Expanse", "Coreward Expanse" (a duchy) |
| **Cluster** | Empire (`holdings_concepts:84-85`, `title_tiers:86,88` "Holy Cluster") | `terrains:12-13` "Debris Cluster"; wordbank `:57` | **Six terrains** in `docs/terrain_scheme.md:28,29,32,34,40,42`: Open, Broken, Frozen, Dense, Volatile and Layered Cluster | `traditions:9`; title "The Myr Cluster" |

**How big the Cluster clash is.** By the scheme's own figures, the six "… Cluster" terrains cover 24.5 + 6.2 + 3.6 + 2.6 + 0.4 + 0.2 ≈ **37.5% of the land**. "Cluster" would be the most common terrain word on the map, and it is also the empire tier word.

**Smaller overlaps** (same principle, not in the audit):
- **Reach:** four v2 terrains (Barren, Arid, Frontier, Fertile Reach) against about 25 v1 proper names (e.g. "Xerxes Reach"). Cosmetic. The v1 titles are in the rewrite column.
- **Belt:** the wordbank's "terraced belt claims" (`wordbank:47`) against the building "Belt Claims".
- **Drift:** "Dense Drift Zone" (`terrains:10`) against the title "The Far Drift".

### 3.2 Options
**A. Keep the tier words and rename the terrains (recommended).**
- The tier ladder is the author's decision (`localization_crusade.md:12-13`) and is linked from about 110 keys.
- v2 terrains have no loc yet (`terrain_scheme.md:105-108`).
- Proposed names below. They avoid System, Region, Sector, Expanse, Cluster, Void, Grip, Fringe, Belt and Drift.

| CK3 key | v2 name now | **A1: family swap** | A2: individual names | Inline form |
|---|---|---|---|---|
| plains | Open Cluster | **Open Starfield** | Open Space | open starfield(s) |
| hills | Broken Cluster | **Broken Starfield** | Shattered Field | broken starfield(s) |
| desert | Barren Reach | Barren Reach | Barren Waste | barren reach(es) |
| mountains | Nebula Barrier | Nebula Barrier | (same) | nebula barrier(s) |
| taiga | Frozen Cluster | **Frozen Starfield** | Frost Shoals | frozen starfield(s) |
| drylands | Arid Reach | Arid Reach | Parched Space | arid reach(es) |
| forest | Dense Cluster | **Dense Starfield** | Thick Stars | dense starfield(s) |
| steppe | Frontier Reach | Frontier Reach | Outer Dark | frontier reach(es) |
| jungle | Nebula Wilds | Nebula Wilds | (same) | nebula wilds |
| desert_mountains | Barren Barrier | Barren Barrier | (same) | barren barrier |
| wetlands | Anomaly Fields | Anomaly Fields | (same) | anomaly field(s) |
| farmlands | Fertile Reach | Fertile Reach | Fertile Deep | fertile reach |
| floodplains | Volatile Cluster | **Volatile Starfield** | Flux Field | volatile starfield |
| oasis | Sanctuary Systems | **Sanctuary Pockets** (the scheme's own "favourable pocket", `:41`) | Sanctuary Haven | sanctuary pocket(s) |
| terraced_hills | Layered Cluster | **Layered Starfield** | Tiered Stars | layered starfield |

- **A1** changes only the 7 names that contain a tier word, and keeps the scheme's "X + family" logic.
- **Risks:**
  - "Starfield" sits next to "Anomaly Fields". Lore-keeper should check they read as distinct.
  - A2's "Outer Dark" echoes v1's "the open dark" (`replace/eotg_mounts_ui_l_english.yml:60`).
- **All names are proposals** for lore-keeper and the human.

**B. Change the tier words instead** (e.g. Cluster → "Dominion", Region → "Territory").
- Costs about 110 keys plus the title-tier variants ("Holy Cluster", `title_tiers:88`).
- Undoes an author decision whose reasoning rests on v1 title names ("The Myr Cluster", `localization_crusade.md:21`). The audit already says to recheck that reasoning after Gate 1 (`:248`).
- The candidate words collide too: "Hegemony" is a vanilla tier (`UNVERIFIED-VANILLA`), "Imperium" is in proper names, and "province" and "domain" are vanilla concepts.
- Not recommended unless the Gate 1 names make "Cluster" or "Region" wrong anyway.

**C. Tolerate the overlap and qualify by context**, using the "Coreward Expanse" precedent (`localization_crusade.md:39-41`).
- That precedent covered one proper name. This would be a terrain covering ~37% of the map, which is exactly the double meaning the "Realm" rejection avoided (`localization_crusade.md:31-35`).
- Not recommended.

**Recommendation: A1.** The localizer should also sweep lowercase tier words that mean "an area of space" out of flavor prose (the traditions file).

**Files affected under A** (after the ruling):
- `replace/eotg_terrains_l_english.yml`: all of it. Add the missing terrains and `combat_*` keys. The singular `combat_mountain` (`:6`) is `UNVERIFIED-VANILLA`.
- `replace/eotg_custom_loc_wordbank_l_english.yml:44-67`, in the same change. The two files must stay in sync (`localization_crusade.md:136-141`).
- `replace/eotg_traditions_l_english.yml:11-33,78-79,101,124,127`.
- `OLD PROJECT VERSION/localization/english/eotg_maa_l_english.yml:30`, if the men-at-arms are lifted.
- **`docs/terrain_scheme.md`** belongs to another session's map work. **Propose the change; don't edit it.** Its table (`:28-42`) and descriptions (`:50-101`) follow the ruling. Material ids are unaffected (`:111-112`).

---

## 4. County → Region: the 32 prose lines that still say "County"

**How they were found:** parse every value in the 52 `replace/` files, strip `[...]` and `$...$`, and match `\bcount(y|ies)\b`. That gives **32 value lines in 29 distinct keys**; this session re-ran the count and confirmed 32. Keys, comments, links and the ruler rank "Count" were excluded. Rows marked ⧉ are byte-identical duplicates across two files, so after the dedupe (§6.2 step 0) only one copy needs the edit.

**Two ways to fix:**
- **(i) Plain text:** "County" → "Region".
- **(ii) A self-reference:** `$game_concept_county$`, which follows any future ruling. This pattern is already used at `replace/eotg_holdings_concepts_l_english.yml:88`. Whether `$…$` works inside modifier `_desc` keys is `UNVERIFIED-VANILLA`.

The table shows (i).

| # | file:line | Key | Current | Proposed |
|---|---|---|---|---|
| 1 | `eotg_county_hunt_tour_modifiers_l_english.yml:24` | `hunt_peasants_denied_forest_modifier_desc` | "The commoners of this County have been denied…" | "…of this Region…" |
| 2 | `…:29` | `hunt_peasants_hunted_modifier_desc` | "afraid of settling in this County" | "…in this Region" |
| 3 | `…:42` | `hunt_protected_peasants_modifier_desc` | "The commoners of this county feel safe." | "…of this region…" |
| 4 | `…:48` | `hunt_punished_trappers_modifier_desc` | "this county's commoners" | "this region's commoners" |
| 5 | `…:60` | `liege_respected_fighter_modifier_desc` | "A local commoner leader from this county" | "…from this region" |
| 6 | `…:76` | `marshal_task_organized_service_modifier_desc` | "The commoners in this county have been organized" | "…in this region…" |
| 7 | `…:79` | `steward_realm_identity_modifier_desc` | "The commoners of this County considers" | "…of this Region consider" (also fixes the grammar) |
| 8 | `…:84` | `county_corruption_lack_of_courts_modifier_desc` | "…commoner cases in this County" | "…in this Region" |
| 9 | `…:93` | `small_investment_in_revolt_modifier_desc` | "…under foreign influence in this County" | "…in this Region" |
| 10 | `…:97` | `medium_investment_in_revolt_modifier_desc` | "…refuse work in this County" | "…in this Region" |
| 11 | `…:101` | `high_investment_in_revolt_modifier_desc` | "…rioting all over this County, " | "…all over this Region, " |
| 12 | `…:106` | `entertained_peasants_desc` | "The commoners in this county were entrained" | "…in this region were entertained" (also fixes a typo) |
| 13 | `…:111` | `scared_peasants_desc` | "Commoners in this county were terrified" | "…in this region…" |
| 14 | `…:114` | `martially_inspired_desc` | "The commoners in this county have been martially inspired." | "…in this region…" |
| 15 | `…:117` | `inspired_by_tales_desc` | "The commoners in this county have been inspired" | "…in this region…" |
| 16 | `eotg_ep1_ep3_laamp_misc_l_english.yml:53` ⧉ | `ep3_surplus_manpower_desc` | "This county has a surplus of fit commoners" | "This region has…" |
| 17 | `eotg_ep3_dlc_commoner_l_english.yml:107` | `ep3_laamp_peasant_war.peasant_army` | "Commoners in every county will raise" | "…in every region…" |
| 18 | `eotg_ep3_dlc_commoner_l_english.yml:120` ⧉ | `ep3_surplus_manpower_desc` | duplicate of #16 | — |
| 19 | `eotg_fp1_fp2_fp3_events_l_english.yml:60` ⧉ | `fp3_wheat_shortage_modifier_desc` | "The royal baker in this county is hoarding wheat" | "…in this region…" (also: wheat, maund) |
| 20 | `eotg_fp_dlc_commoner_l_english.yml:22` | `held_grand_sacrifice_fp1_modifier_desc` | "The commoners of this county rest easy" | "…of this region…" |
| 21 | `eotg_fp_dlc_commoner_l_english.yml:25` | `commoners_grand_sacrifice_fp1_modifier_desc` | "The commoners in this county still talk" | "…in this region…" |
| 22 | `eotg_fp_dlc_commoner_l_english.yml:59` | `rice_fields_modifier_desc` | "Commoners in this County are growing nutritious rice" | "…in this Region…" (also: rice) |
| 23 | `eotg_fp_dlc_commoner_l_english.yml:109` ⧉ | `fp3_wheat_shortage_modifier_desc` | duplicate of #19 | — |
| 24 | `eotg_gui_factions_memories_l_english.yml:21` | `FACTION_WINDOW_COUNTY_MEMBER_TT` | "#I Click to view County#!" | "#I Click to view Region#!" |
| 25 | `…:39` | `event_window_widget_peasant_leader_tooltip_widget` | "commoners from all supported counties will join" | "…supported regions…" |
| 26 | `…:96` | `reactive_advice_protect_against_factions_2_desc` | "Counties with a low [county_opinion\|E]" | "Regions with a low…" |
| 27 | `eotg_sin_vice_events_l_english.yml:89` | `refused_to_repent_desc` | "The locals of this county recently demanded" | "…of this region…" |
| 28 | `eotg_tgp_dlc_commoner_l_english.yml:64` ⧉ | `tgp_executed_peasants_county_modifier_desc` | "This county has not forgotten" | "This region has not forgotten" |
| 29 | `…:82` | `upset_peasants_modifier_desc` | "the commoners of this county are unruly" | "…of this region…" |
| 30 | `…:88` | `well_armed_peasants_modifier_desc` | "The commoners in this county are allowed to keep large amounts of spears." | "…in this region…" (also: spears) |
| 31 | `eotg_tgp_ep3_legends_l_english.yml:43` ⧉ | `tgp_executed_peasants_county_modifier_desc` | duplicate of #28 | — |
| 32 | `eotg_yearly_events_l_english.yml:70` | `buzzed_peasants_county_modifier_desc` | "The common folk of this county are quite pleased" | "…of this region…" |

All paths are under `OLD PROJECT VERSION/localization/english/replace/`.

**Notes:**
- Lowercase "region" here *is* the tier (the county the modifier sits on), so it is correct. In the traditions file, by contrast, "regions" means areas of space and should go.
- Medieval words remain in the same strings: forests (#1), wheat and maund (#19), rice (#22), spears (#30), levy (#7), gods (#20-21). They are out of scope, but the localizer can fix them in the same edit.

---

## 5. Other glossary gaps
1. **burgher → "contractor".** Already applied (`replace/eotg_burgher_corvee_concepts_l_english.yml:11`, plus `eotg_fp1_fp2_fp3_events_l_english.yml:8` and `eotg_sin_sermon_serf_misc_l_english.yml:20`) but missing from the glossary table.
   - Add the row Burgher → **Contractor**.
   - Risk: vanilla Roads to Power calls landless adventurers' jobs "contracts", which v1 also overrides (`eotg_activities_contracts_commoner_l_english.yml`). "Contractor" may then read as "takes contracts" (`UNVERIFIED-VANILLA`).
   - Alternatives: "Guildsman", "Freeholder".
2. **chivalry → "Valor".** Applied at `replace/eotg_mounts_ui_l_english.yml:62-68` and in prose at `localization_crusade.md:126`. Add the row to the glossary.
3. **court eunuchs → "Chamber Custodians".** Applied at `replace/eotg_traditions_l_english.yml:72`. Add the row to the glossary.
4. **"Void" used for ordinary space** (`replace/eotg_traditions_l_english.yml:5,6,8,9,32,33,113`) collides with the canon Void (SETTING LORE `:10-16`; CB-11). Canon has **no** word for FTL routes; the nearest is SETTING LORE `:134`, "Spacecraft and space travel becoming practical". So every replacement below **needs lore**:

   | Line | Current | Proposal | Fallback |
   |---|---|---|---|
   | `:5` | "Voidfarers" | "Starfarers" | "Deepfarers" |
   | `:6` | "unstable voidlanes" | "unstable starlanes" | "unstable transit lanes" |
   | `:8` | "Voidlane Commerce" | "Starlane Commerce" | "Lane Commerce" |
   | `:9` | "protected void corridors … across the clusters" | "protected transit corridors … across the stars" | — |
   | `:32` | "Void Trawlers" | "Deep Trawlers" | "Wreck Trawlers" |
   | `:33` | "dangerous void regions" | "dangerous dead space" | — |
   | `:113` | "aggressive void assaults" | "aggressive boarding assaults" | — |

   v1 already leans toward "lane" ("Longlane", `terrains:19`). If "starlane" is ruled, record in the glossary: **Starlane** = an ordinary FTL route; **Void** = the canon entity only. Related: the v2 map docs call the sea "Deep Void" (`docs/terrain_conversions.md:102`), which would collide if it ever reaches loc.
5. **"Region" has three meanings:**
   - (a) the county tier, which players see;
   - (b) intake's planning unit (`intake/README.md:23-32`; `intake/templates/REGION.md:12`, which itself says "counties and duchies"; folder names like `myr_cluster` also carry the empire word);
   - (c) script `geographical_region` ids.

   **Proposal:** don't rename intake. It is a contract with the external exporter, and players never see it. Add a glossary note: "*Region* in player text = the county tier only. In docs, say *intake region* for a brief folder and *geographical region* for script regions." Optionally the architect could use "intake region" in `docs/specs/regions/` headings.
6. **"Strike Speeders" name clash.** Vanilla `horse_archers:0 "Strike Speeders"` (`replace/eotg_mounts_ui_l_english.yml:53-54`) has the same name as the mod's own `eotg_maa_strike_speeders` (`OLD PROJECT VERSION/localization/english/eotg_maa_l_english.yml:29`). Options:
   - **(a) Recommended:** rename the vanilla unit to **"Skimmer Gunners"**. This matches the existing building note "skimmer gunnery tech (feeds Strike Speeders)" (`replace/eotg_buildings_setting_l_english.yml:28`).
   - (b) Rename the mod's own unit.
   - (c) Hide vanilla men-at-arms (audit decision 8). This alone does not fix the loc.
7. **Reserved non-tier words** (principle 4) should be listed in the glossary. The "terraced belt claims" overlap is handled by the terrain rewrite.
8. **Docs drift** (orchestrator):
   - the glossary misquotes in §0;
   - `.claude/agents/eotg-localizer.md:14` says "49 `replace/` files", but there are 52 (audit `:238`).

---

## 6. Decisions and follow-on work

### 6.1 Decisions for the human (one line each)
1. CB-08: keep court, courtier, vassal, liege and household as vanilla terms? (Proposed: yes.)
2. Knight: keep it generic, and reflavor per culture later from intake? (Proposed: yes.)
3. Gold: keep "Gold", adopt "Credits", or ask the vault for a currency first? (Proposed: ask the vault; keep "Gold" meanwhile.)
4. Ruler ranks: keep vanilla now, with culture and government ranks later? (Proposed: yes.)
5. Tier vs terrain: A (rename terrains), B (rename tiers) or C (tolerate)? (Proposed: A.)
6. If A: the A1 family swap ("… Starfield", "Sanctuary Pockets") or the A2 individual names? Either way the names go to lore-keeper.
7. Keep "Reach" in the four terrain names? (Proposed: yes; cosmetic.)
8. Ban lowercase tier words meaning "an area of space" from flavor prose? (Proposed: yes.)
9. County → Region prose: plain text or `$game_concept_county$` self-references? (The latter is `UNVERIFIED-VANILLA` in modifier descs.)
10. Add burgher → Contractor, chivalry → Valor and eunuchs → Chamber Custodians to the glossary? (Proposed: yes; check "contractor" against vanilla "contracts".)
11. "Void" for ordinary space: "starlane", or a vault term? (Proposed: ask the vault; fall back to "starlane".)
12. Rename vanilla `horse_archers` to "Skimmer Gunners"? (Proposed: yes.)
13. "Region" in intake: a glossary note only, no rename? (Proposed: yes.)

### 6.2 Follow-on work for the localizer once ruled
0. **Prerequisite: dedupe `replace/`.**
   - 166 keys are duplicated and 44 of them conflict (`localization_crusade.md:203-261`; audit `:242`).
   - Merge the 44, delete the 122 identical copies, and rerun the check at `localization_crusade.md:268-271`.
   - Do this before §4, because rows #16/18, #19/23 and #28/31 are duplicate pairs.
1. vanilla-scout confirms:
   - the `game_concept_*` names;
   - the generic ruler-title keys;
   - how culture-level knight terms work;
   - whether `replace/` overrides by key regardless of filename;
   - `combat_mountain`;
   - `$…$` inside modifier descs.
2. Rewrite the glossary as a v2 doc: the full table, the new rows, the reserved-word list, the Region note, and the CB-08 outcome for each term.
3. For each term ruled "rename": override the concept keys, sweep the `replace/` prose (§2 counts), **then grep the v2 cybernetics loc for the term and revise it**, as CB-08's next step requires.
4. For each term ruled "keep": grep the cybernetics loc once to confirm it agrees with the final glossary.
5. Terrains:
   - Rewrite `replace/eotg_terrains_l_english.yml` and the wordbank `:44-67` together.
   - Then do the traditions file, which is blocked until the terrain ruling (audit `:245`).
   - Send the new names to the owner of `docs/terrain_scheme.md`.
6. Apply the 29 County → Region edits from §4, after the dedupe.
7. Rename vanilla `horse_archers` (§5.6), and remove "Void" from the traditions file (§5.4).
8. Orchestrator: fix `.claude/agents/eotg-localizer.md:3,14,25` and `OLD VERSION CATALOG.md:26,91`.
9. Validation:
   - the full CLAUDE.md check set (Tiger and PX), plus the BOM, duplicate and `[scope:` checks;
   - then QA;
   - then lore-keeper for the new terrain and lane names.

---

## 7. Handoff
### HANDOFF (cloud session, unvalidated)
- **branch:** `claude/canon-void-glossary-cloud`
- **status:** done (proposal; nothing ruled)
- **files:** `docs/specs/glossary_proposal_cloud.md`
- **unverified-vanilla:** §6.2 step 1; principle 8; §5.1 ("contracts"); §2 "overlord".
- **needs-human:** §6.1 (13 decisions).
- **needs-lore:** the terrain names (§3.2), the lane word (§5.4), currency (§2 gold).
- **needs-loc:** all of §6.2, once ruled.
- **taskboard (proposed):**
  - CB-08 next step: "rule on glossary_proposal_cloud.md §6.1";
  - add the `replace/` dedupe as a localizer item (prerequisite to the `replace/` lift);
  - add the agent and catalog glossary misquote fix as an orchestrator item.
