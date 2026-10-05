# Spec: Frontier Systems v2 (Phase 2 content)

**Author:** cloud agent (architect role), 2026-10-05. **Status: built on branch `claude/frontier-v2-cloud`; NOT merged.** The owner asked that nothing lands until the local session verifies it (Tiger, PX, a vanilla check of the engine claims in §15, a lore pass) and the owner reviews it.

**Source of intent:** [`docs/design/frontier_systems.md`](../design/frontier_systems.md) §4, §9–§13 and §22 Phase 2 (cited as *design §n*). Phase 1 is [`frontier_v1.md`](frontier_v1.md); its rulings (§R), verification fixes (§V) and the owner decisions in [`frontier_v1_verification.md`](frontier_v1_verification.md) §4 all still bind. This spec only adds.

**Written without game files.** As in Phase 1: no vanilla 1.20 files, no Tiger, no PX. Engine facts carry a confidence and a source (§1). Anything not used by the mod's own verified script is marked `# UNVERIFIED-VANILLA` in script and listed in §15.

**Size (as built):**
- **Events:** 9 new (.020, .021, .030–.036). Seven are flavor events that share Phase 1's one roll and its 3-year cooldown, so a project still sees about the same number of prompts (§9.1).
- **Decisions:** 2 new (Survey a Region, Build Frontier Infrastructure).
- **Modifiers:** 24 new county modifiers: 10 traits, 8 infrastructure, 5 settlement legacies, 1 concessions.
- **Opinion modifiers:** 3. **Character templates:** 3. **Hooks:** 2 new integration on_actions.
- **No** buildings, holding types, gfx, story cycles or GUI.

---

## 0. Rules this phase builds under

Everything in Phase 1 §R and §V, plus:
- **Map-agnostic.** No title, province, culture, faith or character keys. Traits and infrastructure are county modifiers on whatever county the state variables are on. It works on the vanilla map through the debug decisions and on the test map.
- **Time-neutral text.** Nothing era-specific: no Exodus, no dates, no named powers. Ruins are "older than any record", never dated.
- **Loc:** Canadian English (L013b), gendered pronouns for single scoped characters, no em dashes, exactly one BOM (L016), bare `[x.GetName]`.
- **Glossary:** a county is a **Region**, a holding a **System**. No "charter", no named factions, no Void, nothing from the cybernetics never-name list (`cybernetics_v2.md` §5), no "humanity"/"human" (multi-species), no medieval leaks (masons, palace, horses).
- **Tech ceiling (CYBERNETICS AT 866):** stations, beacons and complexes are built and kept running by hand. Nothing repairs itself, nothing is remote-controlled, no state programme pays for anything.
- **LAW AT 866:** no authority above the polity. A sponsor gets no claim and no say (.031 is about exactly that).
- **Invariant 5:** every new event reads or moves progress or strain. **qa_noopt:** every event has at least one option with no trigger.
- **Pacing:** the doubled pacing and the 3-year cooldown stand. New gain inputs are small and mostly bought (infrastructure costs gold), so an unaided project still takes about 10–16 years (§6.4).

---

## 1. Engine facts (new in Phase 2)

Confidence: **H** = used by the mod's verified script; **M** = skill reference only; **L** = general knowledge.

| # | Fact | Source | Conf. |
|---|---|---|---|
| F1 | Static county modifiers as state, read with `has_county_modifier` | Phase 1 (V4) | H |
| F2 | `random_list` entries take `trigger = { }` and `modifier = { add = n <triggers> }` | `events/eotg_augmentation_fracture.txt:4459` | H |
| F3 | `save_scope_value_as = { name = x value = flag:y }`, read back as `scope:x = flag:y` | `events/eotg_augmentation_fracture.txt:1422` | H |
| F4 | `add_opinion = { modifier = x target = y years = n }`; opinion modifiers `opinion = n` | `events/eotg_augmentation_activities.txt:131`; `common/opinion_modifiers/eotg_augmentation_opinions.txt` | H |
| F5 | `add_piety = minor_piety_value`, `minor_prestige_value`, `decent_skill_rating` | `eotg_augmentation_activities.txt:220`; aug events | H |
| F6 | `piety_level >= n` as a character trigger | general knowledge; vanilla decisions | **L** (§15 V2-1) |
| F7 | `county_opinion_add` as a county-modifier line | `common/buildings/eotg_00_city_buildings.txt:60` (building county modifier) | M (§15 V2-2) |
| F8 | Scripted-effect parameters substituted as a whole token (`add_county_modifier = $TRAIT$`, `flag:$FLAG$`) | Phase 1: `HOOK = $HOOK$`, `flag:$TYPE$` | H |
| F9 | `create_character` with a template, `add_courtier` | Phase 1 (E13) | H |
| F10 | A script value on the left of a trigger comparison (`my_value < 2`) | general knowledge | **L** (§15 item 5) |
| F11 | A script value as an effect amount (`change_development_level = my_value`) | general knowledge; Phase 1 uses `change_variable = { add = <script value> }` | M (§15 item 6) |

**Buildings vs county modifiers (design §9, decided):** vanilla buildings need a `type_icon`, a 3D `asset` and an `illustration` (skill `reference/common/buildings/_buildings.info:30-55, 345`), and they live in the holding's build menu. That is gfx and GUI work, and `gfx/` is out of scope. **Infrastructure is county modifiers**, built through a decision, as Phase 1's stages are. A building surface stays possible later (deferral D2-3).

---

## 2. Data model (new state, all on the county title)

| Key | Kind | Meaning |
|---|---|---|
| traits (§5) | county modifiers `eotg_frontier_trait_*` | **The Region's known nature.** Present = known. They stay through abandonment (resource knowledge, design §3.4) and are converted into results and removed when the Region settles. |
| infrastructure (§4) | county modifiers `eotg_frontier_infra_*` | **What the project has built.** Removed and converted into results on settling; lost on abandonment. |
| `eotg_frontier_surveyed` | variable, yes, timed 5 years | A survey ran here recently (Survey's own gate; not an event cooldown). |
| `eotg_frontier_survey_data` | variable, yes | Survey results on file: the next project starts `eotg_frontier_survey_bonus_value` ahead. Consumed by `eotg_frontier_start_effect`. |
| `eotg_frontier_built` | variable, yes, timed 1 year | Infrastructure was built here this year (one build a year per Region). |
| `flag:danger` | value of `eotg_frontier_last_cause` | The new strain cause from the Dangerous trait (§5.3). |

Saved scopes: `eotg_frontier_discovered` (a flag value: the trait just revealed, for the discovery hook and .020's desc), `eotg_frontier_infrastructure` (a flag value: what was just built, for its hook), `eotg_frontier_found` (.035's flag value: ruins or a derelict), `eotg_frontier_rival` (.030), `eotg_frontier_overlord` (.032, the holder's liege), `eotg_frontier_figure` (a created local figure); internal: `eotg_frontier_toast_target`.

---

## 3. New identifiers

### 3.1 Modifiers, opinions, templates
| Type | Key | Notes |
|---|---|---|
| static modifier | `eotg_frontier_trait_rich_resources` | Rich Resources (§5) |
| static modifier | `eotg_frontier_trait_trade_route` | Valuable Trade Route |
| static modifier | `eotg_frontier_trait_strategic` | Strategic Location |
| static modifier | `eotg_frontier_trait_habitable` | Habitable |
| static modifier | `eotg_frontier_trait_ancient_ruins` | Ancient Ruins |
| static modifier | `eotg_frontier_trait_ancient_infrastructure` | Ancient Infrastructure |
| static modifier | `eotg_frontier_trait_anomalous` | Anomalous |
| static modifier | `eotg_frontier_trait_hostile` | Hostile Environment |
| static modifier | `eotg_frontier_trait_remote` | Remote |
| static modifier | `eotg_frontier_trait_dangerous` | Dangerous |
| static modifier | `eotg_frontier_infra_habitat` | Habitat (§4) |
| static modifier | `eotg_frontier_infra_orbital_station` | Orbital Station |
| static modifier | `eotg_frontier_infra_navigation_beacon` | Navigation Beacon |
| static modifier | `eotg_frontier_infra_trade_station` | Trade Station |
| static modifier | `eotg_frontier_infra_mining_complex` | Mining Complex |
| static modifier | `eotg_frontier_infra_research_facility` | Research Facility |
| static modifier | `eotg_frontier_infra_mission` | Mission |
| static modifier | `eotg_frontier_infra_garrison_post` | Garrison Post |
| static modifier | `eotg_frontier_mod_legacy_trade` | settlement legacy, 25 years (§7) |
| static modifier | `eotg_frontier_mod_legacy_industry` | settlement legacy, 25 years |
| static modifier | `eotg_frontier_mod_legacy_defence` | settlement legacy, 25 years |
| static modifier | `eotg_frontier_mod_legacy_learning` | settlement legacy, 25 years |
| static modifier | `eotg_frontier_mod_legacy_faith` | settlement legacy, 25 years |
| static modifier | `eotg_frontier_mod_concessions` | .032: terms granted to the settlers, 10 years |
| opinion modifier | `eotg_frontier_opinion_pleased` | +10, timed by the caller |
| opinion modifier | `eotg_frontier_opinion_slighted` | −10, timed by the caller |
| opinion modifier | `eotg_frontier_opinion_dropped` | −20, timed by the caller (.030: a backer let go) |
| character template | `eotg_frontier_commander_template` | Military result (§7) |
| character template | `eotg_frontier_elder_template` | Religious result |
| character template | `eotg_frontier_official_template` | Administrative result |

### 3.2 Scripted effects (county scope unless noted)
| Type | Key | Does |
|---|---|---|
| scripted effect | `eotg_frontier_reveal_trait_effect` | rolls one trait the Region doesn't have (weighted, exclusive pairs respected) and adds it; **the public discovery entry point** for a future Exploration system (§8) |
| scripted effect | `eotg_frontier_add_trait_effect` | (`TRAIT`, `FLAG`) adds that trait if there is room; saves `scope:eotg_frontier_discovered`; fires `eotg_frontier_on_discovery` |
| scripted effect | `eotg_frontier_add_infra_effect` | (`INFRA`, `FLAG`) adds that infrastructure, marks the year, fires `eotg_frontier_on_infrastructure_built` |
| scripted effect | `eotg_frontier_clear_infra_effect` | removes every infrastructure modifier (abandonment, settling) |
| scripted effect | `eotg_frontier_clear_traits_effect` | removes every trait modifier (settling) |
| scripted effect | `eotg_frontier_settle_rewards_effect` | converts traits and infrastructure into normal results (§7) |
| scripted effect | `eotg_frontier_create_figure_effect` | (`TEMPLATE`) a local figure, courtier of the holder, holder's culture and faith by scope |
| scripted effect | `eotg_frontier_flavor_pick_effect` | the weighted flavor pool (§9.1) |
| scripted effect | `eotg_frontier_find_rival_backer_effect` | saves `scope:eotg_frontier_rival`: an AI who would back the Frontier and is not its backer or holder |
| scripted effect | `eotg_frontier_discovery_toast_effect` | the holder's "new findings" toast |
| scripted effect | `eotg_frontier_file_survey_effect` | .020: progress +2 on a Frontier, else survey data on file |

### 3.3 Scripted triggers
| Type | Key | True when |
|---|---|---|
| scripted trigger | `eotg_frontier_trait_room` | county: fewer known traits than `eotg_frontier_trait_max_value` |
| scripted trigger | `eotg_frontier_infra_room` | county: a Frontier with fewer infrastructure than its slots, and none built this year |
| scripted trigger | `eotg_frontier_can_survey` | county: Unsettled, Frontier or Abandoned; trait room; not surveyed in the last 5 years |
| scripted trigger | `eotg_frontier_holds_surveyable` | character: holds such a Region |
| scripted trigger | `eotg_frontier_holds_buildable` | character: holds a Frontier with infrastructure room |
| scripted trigger | `eotg_frontier_danger_strains` | county: Dangerous, control below 60, no Garrison Post, not a Military project |
| scripted trigger | `eotg_frontier_quiet_eases` | county: a quiet year may ease strain (not Hostile, or an Orbital Station) |
| scripted trigger | `eotg_frontier_war_strains` | county: war adds strain (not a Military project) |

### 3.4 Script values
| Type | Key | Value |
|---|---|---|
| script value | `eotg_frontier_trait_count_value` | known traits on the Region |
| script value | `eotg_frontier_trait_max_value` | 2 |
| script value | `eotg_frontier_infra_count_value` | infrastructure built |
| script value | `eotg_frontier_infra_slots_value` | 1, or 2 from Foothold (progress ≥ 33) |
| script value | `eotg_frontier_trait_rate_value` | the traits' yearly input (§5.2) |
| script value | `eotg_frontier_infra_rate_value` | infrastructure's yearly input (§4.2) |
| script value | `eotg_frontier_type_input_value` | the type's own yearly input (§6.2) |
| script value | `eotg_frontier_low_control_value` | the Low Control strain line: 40, Administrative 50 |
| script value | `eotg_frontier_infra_cost_value` | `medium_gold_value` (character scope) |
| script value | `eotg_frontier_survey_cost_value` | `minor_gold_value` (character scope) |
| script value | `eotg_frontier_survey_bonus_value` | 5: the head start from survey data |
| script value | `eotg_frontier_reward_dev_value` | development from traits and infrastructure on settling, +1 per source, at most 3 (§7) |

### 3.5 Decisions, hooks, events
| Type | Key | Notes |
|---|---|---|
| decision | `eotg_decision_frontier_survey` | Survey a Region → .020 (§8) |
| decision | `eotg_decision_frontier_build` | Build Frontier Infrastructure → .021 (§4) |
| on_action | `eotg_frontier_on_discovery` | integration hook: a trait was revealed (§8) |
| on_action | `eotg_frontier_on_infrastructure_built` | integration hook: infrastructure was built |
| event | `eotg_frontier.020` | *Survey Report* |
| event | `eotg_frontier.021` | *What to Build* |
| event | `eotg_frontier.030` | *A Rival Backer* |
| event | `eotg_frontier.031` | *The Backer Wants a Say* |
| event | `eotg_frontier.032` | *Terms Demanded* |
| event | `eotg_frontier.033` | *A Quarrel in the Camps* |
| event | `eotg_frontier.034` | *A Supply Run Lost* |
| event | `eotg_frontier.035` | *What the Crews Found* |
| event | `eotg_frontier.036` | *A Rich Seam* |

### 3.6 Phase 1 identifiers changed
| Key | Change |
|---|---|
| `eotg_frontier_yearly_gain_value` | adds the trait, infrastructure and type inputs (before the pace multiplier) |
| `eotg_frontier_min_dev_value` | Ancient Infrastructure −1 (still capped by `eotg_frontier_dev_reachable`) |
| `eotg_frontier_min_control_value` | Strategic Location +10, Remote −10 |
| `eotg_frontier_start_effect` | consumes survey data; reveals one trait if none is known |
| `eotg_frontier_tick_effect` | Low Control line by type; Military ignores war; the Dangerous cause; Hostile blocks the quiet-year ease |
| `eotg_frontier_event_roll_effect` | the player branch calls `eotg_frontier_flavor_pick_effect` (§9.1) |
| `eotg_frontier_complete_effect` | per-type figures; then `eotg_frontier_settle_rewards_effect` |
| `eotg_frontier_abandon_effect` | loses the infrastructure (traits stay) |
| `eotg_frontier.001` | type requirements (§6.1), trait-aware AI chances, a "surveys on file" desc line |
| `eotg_frontier.005` | desc for the Danger cause |

---

## 4. Frontier infrastructure (design §9)

### 4.1 Building it
- **Decision `eotg_decision_frontier_build`:** shown to a holder of a Frontier with room (`eotg_frontier_holds_buildable`). It picks the most advanced such Region and fires .021, *What to Build*, which charges `eotg_frontier_infra_cost_value` in the option chosen (as .001 does).
- **Slots:** 1 from the start, 2 from Foothold (progress ≥ 33). One build a year per Region (`eotg_frontier_built`).
- **Not every Frontier needs it** (design §9): nothing requires infrastructure.

### 4.2 The set: data rows
Each infrastructure is a county modifier with one small line (the display) plus rows in the yearly input and the settle conversion.

| Infrastructure | Offered when | Yearly input (pre-pace) | Counters | Becomes on settling |
|---|---|---|---|---|
| Habitat | any type | +1; +3 for Settlement | — | +1 development |
| Orbital Station | any type | +1; +3 for Administrative | Hostile Environment (rate and the quiet-year ease) | +10 control |
| Navigation Beacon | any type | +1 | Remote (rate; lowers .034's weight) | +1 development |
| Trade Station | Trade, or Valuable Trade Route | +1; +3 for Trade | — | `eotg_frontier_mod_legacy_trade` |
| Mining Complex | Mining, or Rich Resources | +1; +3 for Mining | — | `eotg_frontier_mod_legacy_industry` |
| Research Facility | Research, Anomalous or Ancient Ruins | +1; +3 for Research | — | `eotg_frontier_mod_legacy_learning` |
| Mission | Religious | +1; +3 for Religious | — | `eotg_frontier_mod_legacy_faith` |
| Garrison Post | Military, Strategic Location or Dangerous | +1; +3 for Military | Dangerous (its strain cause) | `eotg_frontier_mod_legacy_defence` |

"+1; +3" means +1 for any project and +3 when the infrastructure fits the type. Two built pieces add at most +6 a year before the ×0.5 pace.

**Abandonment loses the infrastructure** (design §12 "lose infrastructure"). The expansion (§B2) lets some of it survive as salvage.

---

## 5. Frontier traits (design §10)

### 5.1 The set
Lightweight Region traits, as county modifiers with one small line each. A Region holds at most **2** (`eotg_frontier_trait_max_value`). Habitable and Hostile Environment exclude each other.

| Trait | Kind | Display line |
|---|---|---|
| Rich Resources | + | tax +5% |
| Valuable Trade Route | + | tax +5% |
| Strategic Location | + | levies +5% |
| Habitable | + | development growth +5% |
| Ancient Ruins | research | development growth +5% |
| Ancient Infrastructure | + | tax +5% |
| Anomalous | research | control growth −5% |
| Hostile Environment | − | control growth −10%, development growth −5% |
| Remote | − | control growth −10% |
| Dangerous | − | levies −5%, control growth −5% |

### 5.2 Effects: requirements, speed, risk, rewards, event weights
| Trait | Yearly input (pre-pace) | Requirements | Risk | Rewards on settling | Event weights |
|---|---|---|---|---|---|
| Rich Resources | +1; +3 Mining | — | — | +1 development; industry legacy | .036 off (already known) |
| Valuable Trade Route | +1; +3 Trade | — | — | trade legacy | .030 +10 |
| Strategic Location | +1; +3 Military | control floor +10 | — | defence legacy | .032 +10 |
| Habitable | +1; +3 Settlement | — | — | +1 development | .033 +5 |
| Ancient Ruins | 0; +3 Research, +2 Religious | — | — | learning legacy | .035 finds a derelict instead |
| Ancient Infrastructure | +2 | development floor −1 | — | +1 development | — |
| Anomalous | −1; +4 Research | — | — | learning legacy | .035 +10 |
| Hostile Environment | −2 (0 with an Orbital Station) | — | a quiet year doesn't ease strain (unless an Orbital Station) | — | .002 +10 |
| Remote | −2 (0 with a Navigation Beacon) | control floor −10 | — | — | .034 +10 (−5 with a Beacon) |
| Dangerous | 0 | — | **strain cause Danger** each year while control < 60 (not with a Garrison Post or a Military project) | — | .034 +10 |

Strain is still never a roll (§R): Danger is a named, counterable condition read by the tick, and .005 names it.

### 5.3 Where traits come from
1. **Establish:** a Region with no known trait reveals one when its project starts ("the first expedition learns the place").
2. **Survey** (§8): reveals one, or two if the player pays to go deeper.
3. **Events:** .035 (ruins or a derelict) and .036 (a rich seam) can add one mid-project.

`eotg_frontier_reveal_trait_effect` rolls among the traits the Region lacks, all equally weighted (10 each), so about 60% of reveals are good news and 30% bad. Negative traits are real costs, but each one has a counter, and Remote eases a requirement.

---

## 6. Project types made distinct (design §4.1)

Still one engine and one set of rows keyed on `var:eotg_frontier_type` (Phase 1 §5). Phase 2 adds a row to each channel.

### 6.1 Requirements
| Type | To start (in .001) | Floors (dev / control) | Ongoing |
|---|---|---|---|
| Settlement | — | 2 / 40 | — |
| Trade | — | 3 / 50 | — |
| Mining | — | 2 / 50 | — |
| Military | **minor prestige** (`minor_prestige_value`) | 2 / 70 | **war adds no strain** |
| Religious | **minor piety** (`minor_piety_value`) | 2 / 50 | — |
| Research | someone at court who can read the surveys: the founder candidate or you with learning ≥ `decent_skill_rating` | 3 / 50 | — |
| Administrative | duke or above, or not the capital Region (Phase 1) | 3 / 80 | **Low Control strain below 50** (not 40) |

Traits adjust the floors (§5.2); the development floor stays capped by what the Region can still reach (Phase 1 Q4).

### 6.2 Inputs: `eotg_frontier_type_input_value` (pre-pace)
| Type | Input | Normal CK3 source |
|---|---|---|
| Settlement | +2 while control ≥ 60 | county control |
| Trade | +3 in a year the backer paid | the sponsor payment |
| Mining | development ÷ 5, at most +3 | development |
| Military | the holder's martial ÷ 6, at most +3 | the holder's martial |
| Religious | +1 at piety level ≥ 1, +2 at ≥ 3 (holder) | the holder's piety level |
| Research | 0: its inputs are the founder's learning (Phase 1) and the research traits | traits |
| Administrative | the holder's stewardship ÷ 6, at most +3 | the holder's stewardship |

### 6.3 Results: see §7.

### 6.4 Pacing check (owner targets: 10–16 years unsponsored, 8–10 sponsored)
- **Typical, unaided:** base 10 + development 1 + founder 3 + type 1 = 15 × 0.5 ≈ **7.5 a year → 13–14 years.** Unchanged in practice from Phase 1.
- **A good fit, two pieces of infrastructure, a matching trait:** + infrastructure 6 + trait 3 → 24 × 0.5 = **12 a year → about 9 years**. That costs two medium gold payments, the same order as a sponsor.
- **Two bad traits, nothing built:** −4 → 11 × 0.5 ≈ **5.5 a year → about 18 years**, unless countered.
- One number still retunes everything: `eotg_frontier_pace_value`.

---

## 7. Better settlement outcomes (design §3.3, §4.1)

`eotg_frontier_complete_effect` runs, in order: the **type row** (Phase 1, plus a local figure for three types), then **`eotg_frontier_settle_rewards_effect`**, then the Phase 1 settle.

**Type rows, Phase 2 additions:**
| Type | Phase 1 result | Added |
|---|---|---|
| Settlement | Port, +1 development, the settlers' leader | — |
| Trade | Port, +1 development | trade legacy |
| Mining | +2 development | industry legacy |
| Military | Bastion, +15 control | **a garrison commander** (courtier, martial) |
| Religious | Sanctum, +1 development | **a mission elder** (courtier, learning); faith legacy |
| Research | +2 development, founder learning +1 | learning legacy |
| Administrative | control 100, +1 development | **a Region official** (courtier, stewardship) |

**Traits and infrastructure** (`eotg_frontier_settle_rewards_effect`, one row each, §4.2 and §5.2). A legacy is added once even if several sources grant it. Then every trait and infrastructure modifier is removed: normal CK3 takes over (design §2.3).

**Legacy modifiers** (25 years each; only confirmed modifier keys):
| Modifier | Lines |
|---|---|
| `eotg_frontier_mod_legacy_trade` | tax +10% |
| `eotg_frontier_mod_legacy_industry` | tax +10%, development growth +5% |
| `eotg_frontier_mod_legacy_defence` | levies +15%, control growth +0.1 a month |
| `eotg_frontier_mod_legacy_learning` | development growth +15% |
| `eotg_frontier_mod_legacy_faith` | county opinion +5, control growth +10% |

---

## 8. Discoveries (design §13)

- **Decision `eotg_decision_frontier_survey`** (Survey a Region): cost `eotg_frontier_survey_cost_value`. Shown to a holder of a Region that `eotg_frontier_can_survey`: Unsettled, Abandoned or a Frontier, with trait room, not surveyed in 5 years. It picks the most developed such Region, marks it surveyed and fires .020.
- **.020 *Survey Report*** reveals a trait in `immediate`; the desc names it.
  - **(a) "File the report."** Before a project, the survey data gives the next project a head start (`eotg_frontier_survey_bonus_value`); during one, progress +2. Ungated.
  - **(b) "Send them deeper."** Costs the survey cost again: a second trait (if there is room), plus (a)'s result.
- **Hook for a future Exploration system:** any system can call `eotg_frontier_reveal_trait_effect` on a county (map-agnostic), and listen to **`eotg_frontier_on_discovery`** (root = the holder; `scope:eotg_frontier_county`; `scope:eotg_frontier_discovered` = the trait's flag). Exploration itself (known/unknown/partially explored) is **not built** (deferral D7 stands).

---

## 9. Events (design §11)

### 9.1 The budget, and the one roll
Phase 1's roll was: 30 .002, 20 .003, 50 nothing, at most every 3 years. Phase 2 keeps the **same frequency** and widens the pool:
- **Players:** the founderless .002 variant still comes first. Otherwise a 50% chance that an event comes at all; if it does, `eotg_frontier_flavor_pick_effect` picks one from the pool by weight, and only then is the 3-year cooldown set.
- **Pool weights:** .002 20 (+10 Hostile); .003 20 (no backer, a candidate exists); .030 10 (+10 Valuable Trade Route; a backer and a rival exist); .031 10 (a backer); .032 10 (+10 Strategic; from Foothold); .033 10 (+5 Habitable; a founder who is not the holder); .034 5 (+10 Remote, +10 Dangerous, −5 when a Navigation Beacon serves a Remote Region, so it never reaches 0); .035 10 (+10 Research or Anomalous; trait room); .036 10 (+10 Mining; trait room; no Rich Resources yet).
- **Result:** a typical 13-year project sees about 3 flavor events, plus .001 and .004: **about 5 Frontier prompts in total**, inside the 4–6 budget. Survey (.020) and Build (.021) are player-initiated pick events, not prompts.
- **AI holders** still get no flavor events (Phase 1). Traits, infrastructure and type inputs apply to them all the same.

### 9.2 The new events
Root is the Region's holder (or the decision taker); the Region is `scope:eotg_frontier_county`. Every option that changes the Region re-checks its state; the last option of each flavor event has no trigger and guards its own effects.

| ID | Title | Fired by | Options (ungated one in **bold**) | Couples |
|---|---|---|---|---|
| `eotg_frontier.020` | *Survey Report* | Survey decision | **(a) file it**; (b) send them deeper (gold) | progress +2, or survey data (head start) |
| `eotg_frontier.021` | *What to Build* | Build decision | one per infrastructure the Region is offered (gold); **(i) not now** | infrastructure → yearly progress input |
| `eotg_frontier.030` | *A Rival Backer* | roll | (a) take the new terms: the rival backs it, progress +3, the old backer is slighted; **(b) keep faith: the backer is pleased, strain −1** | progress / strain |
| `eotg_frontier.031` | *The Backer Wants a Say* | roll | (b) honour them publicly (prestige to them, progress +2); (c) a share of the first returns (gold, strain −1); **(a) the Region is yours: no say; the backer is slighted, strain +1** | progress / strain |
| `eotg_frontier.032` | *Terms Demanded* | roll | the settlers ask for lighter dues, or (if you have one) your liege asks for a share: (a) grant the settlers' terms (concessions modifier, strain −1) or (d) pay the liege's share (gold, strain −1); (c) talk them round (diplomacy); **(b) refuse: strain +1** (liege slighted) | strain |
| `eotg_frontier.033` | *A Quarrel in the Camps* | roll | (a) back the founder (progress +3, strain +1); (c) settle it yourself (gold, strain −1); **(b) side with the settlers (strain −1, progress −2, founder slighted)** | progress / strain |
| `eotg_frontier.034` | *A Supply Run Lost* | roll | (a) replace it (gold); (c) the backer covers it (by arrangement); **(b) make do: progress −3, strain +1** | progress / strain |
| `eotg_frontier.035` | *What the Crews Found* | roll | ruins or a derelict station: (a) study or restore it (trait Ancient Ruins or Ancient Infrastructure; progress −2, or +3 for Research); **(b) strip it for parts: progress +4** | progress; a trait |
| `eotg_frontier.036` | *A Rich Seam* | roll | (a) survey it properly (gold): trait Rich Resources, progress +2; **(b) work it now: progress +4, strain +1** | progress / strain; a trait |

**LAW AT 866 in .031:** the backer asks for a say in how the Region is run. No option gives one. Their money buys them what it always bought (a part in the venture's success), and the options are about how to keep them content without it.

**.032's "local ruler":** a Frontier's holder already rules it, so the demand comes either from the people on the ground (the settlers, everywhere) or, when the holder is a vassal, from their own liege. That is a relationship inside the realm, which LAW AT 866 allows.

### 9.3 Phase 1 event changes
- `.001`: Military costs prestige, Religious piety, Research needs learning (§6.1); AI chances favour the type the known traits suit; a desc line when traits are already known.
- `.005`: `desc_danger`.

---

## 10. Hooks (design §14)
Two new empty integration on_actions, fired like Phase 1's:
| Hook | Fired from | Extra scopes |
|---|---|---|
| `eotg_frontier_on_discovery` | `eotg_frontier_add_trait_effect` | `scope:eotg_frontier_discovered` (flag) |
| `eotg_frontier_on_infrastructure_built` | `eotg_frontier_add_infra_effect` | — |

---

## 11. Player and AI entry points
| Decision | AI interval | ai_potential | ai_will_do |
|---|---|---|---|
| Survey a Region | county 60, duchy+ 48 (barony 0) | holds a surveyable Region; gold ≥ 3 × survey cost | base 5; +10 Unsettled (not yet a Frontier); +5 learning ≥ 12 |
| Build Frontier Infrastructure | all tiers 24 (barony 0) | holds a buildable Frontier; gold ≥ 2 × infrastructure cost | base 15; +10 strain ≥ 4; −10 greedy |

.021's AI chances favour the infrastructure that fits the type, then the one that counters a known negative trait.

---

## 12. Loc surface (as built)
`localization/english/eotg_frontier_l_english.yml` (the one Frontier loc file), Canadian English. Phase 2 adds about 190 keys (exact count in the handoff): 24 modifiers × 2, 3 opinions, 2 decisions × 4 plus their tooltips, 9 events, the .020 trait lines, the .001/.005 variants, and 1 toast.

## 13. Definition of done (Phase 2)
1. eotg_lint: 0 findings in Frontier files (incl. L013b, L016). check_all passes. spec_conformance: frontier_v2 shows 0 missing ids.
2. Every new event is fired by something, has an ungated option, and reads or moves progress or strain.
3. On the test map, through `frontier_v2_test_plan.md`: each trait can be revealed by Survey, Establish and the two discovery events; each infrastructure can be built where offered; each type's requirement and input behaves as §6; a settled Region gets the §7 results and loses its trait and infrastructure modifiers; an abandoned one keeps its traits and loses its infrastructure.
4. Pacing (§6.4) is unchanged for an unaided project; no project sees more than about 6 prompts.

## 14. Deferrals
- **D2-1:** a custom holding type or building for infrastructure (needs gfx).
- **D2-2:** exploration states (known, unknown, partially explored; design §13), built on `eotg_frontier_on_discovery`.
- **D2-3:** AI flavor events (AI holders still get none).
- **D2-4:** an opinion between a backer and the founder (only holder ↔ backer and holder ↔ founder exist).

## 15. Verification list for the local session (eotg-vanilla-scout, vanilla 1.20.0.3)
1. **(F6)** `piety_level >= n` as a character trigger (marked `# UNVERIFIED-VANILLA` in `eotg_frontier_type_input_value`).
2. **(F7)** `county_opinion_add` inside a static county modifier (`eotg_frontier_mod_legacy_faith`, `eotg_frontier_mod_concessions`; marked).
3. **(F8)** `add_county_modifier = $TRAIT$` and `has_county_modifier = $TRAIT$` with a whole-token parameter. Phase 1's `HOOK = $HOOK$` and `flag:$TYPE$` are the precedent (H), so this is low risk; listed for completeness.
4. In-game (TEST-IN-GAME): a county modifier added to an Unsettled Region survives a holder change (as V1 did for variables).
5. **(F10)** A script value on the **left** of a trigger comparison (`eotg_frontier_trait_count_value < eotg_frontier_trait_max_value`, `eotg_frontier_reward_dev_value > 0`, `eotg_frontier_infra_count_value < eotg_frontier_infra_slots_value`). Phase 1 only used script values on the right (marked in `eotg_frontier_triggers.txt`). Fallback if it fails: `calc_true_if`, or move the count into a variable.
6. **(F11)** `change_development_level = eotg_frontier_reward_dev_value` (a script value as the amount; marked).

## 16. Questions for the owner
- **Q2-1. Traits after settling:** removed (as built, "the Frontier is temporary"), with their value paid out as results. Or should they stay on the Region as permanent descriptors?
- **Q2-2. Infrastructure cost:** `medium_gold_value` each, at most two. Too cheap, too dear?
- **Q2-3. Negative traits:** a reveal is about 30% bad news. Keep that, or weight reveals toward good news?
- **Q2-4. Type costs:** Military costs minor prestige and Religious minor piety to start. Keep, or make them gold like the rest?
- **Q2-5. .032's liege variant:** a vassal's liege asks for a share of a vassal's Frontier. Is that welcome, or should .032 be settlers-only?
- **Q2-6. Three new courtiers** (commander, elder, official) on completion. Keep, or only Settlement's leader as in Phase 1?

---

## B. Expansion (optional; separate commits, accept or drop independently)
*(Filled in after A was built and validated; see the subsections below.)*

---

### HANDOFF
- status: built on `claude/frontier-v2-cloud`, unverified in game, NOT merged.
- next: eotg-vanilla-scout (§15) → eotg-qa (Tiger, PX) → eotg-lore-keeper (loc) → owner (`frontier_v2_test_plan.md`).
- files: `common/*/eotg_frontier_*`, `events/eotg_frontier_events.txt`, `localization/english/eotg_frontier_l_english.yml`, this spec, `frontier_v2_test_plan.md`.
