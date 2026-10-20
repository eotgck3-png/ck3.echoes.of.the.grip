# Spec: Vanilla integration v1 — top-bar alerts and game concepts

Term update 2026-10-20: player-facing county term is Shoal (was Region).

**Author:** eotg-architect, 2026-10-20. **Source:** `docs/qa/system_investigation_2026-10-18/REPORT.md` §5 ranks 1 and 2, approved by the owner.
**Game:** CK3 1.20.1.1. `G` = `D:/SteamLibrary/steamapps/common/Crusader Kings III/game`. Every shape below is cited as `file:line` in `G`.
**Status:** spec only. Nothing here is built.

---

## 1. Purpose and gate

Players can't find the mod's systems. The decisions sit in the generic list, nothing in the top bar points at a Frontier going wrong, and terms like Strain, Seamless, Unsworn or Trade Oligarchy have no tooltip or encyclopedia page. This spec adds two vanilla presentation layers:
- **INT1, alerts:** top-bar important actions;
- **INT2, game concepts:** linkable `[x|E]` terms and encyclopedia entries;
- **INT3:** a later localizer pass that links existing strings to the new concepts.

**Gate.** This is Gate 4 (presentation) work, but only for systems that are already built and exempt from the Gate 1 block:
- cybernetics (exempt 2026-10-02);
- the four governments (exempt 2026-10-08);
- Frontier and Unclaimed Shoals (built against the temporary map).

Every trigger used here is a character, county-variable or trait read. Nothing names a title, province, culture or faith, so the work survives the map swap. **Not blocked**, as long as the orchestrator accepts that Frontier and Unclaimed alerts sit under the same exemption as the systems they describe. **Orchestrator: confirm this on the gate board.**

## 2. Signature resource

This is an integration layer with no events and no flavor, so invariant 5 has nothing to bind. Each alert **reads** its system's signature resource and never moves it:

| Alert | Resource it reads |
|---|---|
| `eotg_action_frontier_breaking` | county variable `eotg_frontier_strain` |
| `eotg_action_frontier_founderless` | county variable `eotg_frontier_founder`, through `eotg_frontier_has_valid_founder` (`common/scripted_triggers/eotg_frontier_triggers.txt:65`) |
| `eotg_action_aug_calibration_lapsed` | the character modifier `eotg_mod_implant_calibrated` (`common/modifiers/eotg_augmentation_modifiers.txt:6`), which sits on the Integration track holder |

Concepts read nothing. They are data and loc.

**Never surfaced:** `eotg_fracture_risk` and the pressure band. Balance §5.2 says "the AI may read the band; the player never sees it". No alert or concept may expose that number, and that includes concept text.

## 3. Engine facts (read before building)

**E1. `should_create_alert` only narrows. It doesn't enable.**
- Vanilla's alert fires only when all three of these hold (`00_action_take_decision_or_interaction.txt:9-15`): `is_important_decision`, `should_decision_create_alert` and `can_execute_decision`.
- A decision is important only if its **group** has `important_decision_group = yes`, or the player toggles it on:
  - `_decisions.info:5-6`;
  - `_decision_group_types.info:5`;
  - vanilla groups with the flag: `oaths` (`00_decision_group_types.txt:5-9`), `nomad_major` (`:26-30`) and `major` (`:42-46`).
- Every mod decision today has no `decision_group_type`, so it falls in `decisions` (`_decisions.info:57-60`), which isn't important. **So `should_create_alert` on its own would change nothing.**
- To alert by default, a decision must also move to an important group. ~~Vanilla pam does exactly that: `decision_group_type = major` plus `should_create_alert` (`pam_decisions.txt:4211-4212`).~~ **Corrected 2026-10-20 (QA INT1):** that citation is `pam_proclaim_crusade_age_tenet_decision`, which sets `should_create_alert = { always = no }`. It is a precedent for switching an alert off, not on.

**E1a. A decision with a `select_scope_object` picker can't be relied on to alert (QA INT1, verified 2026-10-20).**
- `can_execute_decision` includes `is_valid_showing_failures_only` (`_decisions.info:227`). The mod's pickers read `scope:selected_item ?= { … }` there, and nothing sets the selection when an alert is evaluated. So the test fails, and an alert or `unimportant` built on `can_execute_decision` is wrong.
- Of the ten vanilla `major` picker decisions, six set `should_create_alert = { always = no }`: `bulls_decisions.txt:253,319,473,734`, `pam_saint_decisions.txt:195` (`pam_choose_consecration_site_decision`) and `pam_decisions.txt:4212`. The other four set nothing, and their failures-only blocks read `exists = scope:selected_item` (`pam_decisions.txt:3656,4459`; `pam_antipope_decisions.txt:58`). QA's "every" overstates it. Even so, no vanilla picker decision is known to raise a working alert. The only vanilla decisions with alerts switched on are the tribute missions (`tgp_tribute_mission_decisions.txt:9` and onward). They use `decision_option_list_controller`, and their failures-only block doesn't read a selection.
- **Rule:** a picker decision gets `should_create_alert = { always = no }`. When it should be nudged, a **custom important action** tests selection-free scripted triggers that mirror the decision's `is_shown` and `is_valid`, and never calls `can_execute_decision`.

**E2. Decision alerts need no new loc.** `action_take_decision` builds its strings from the decision itself:
- `[decision.GetTitleForPlayer]` and `[decision.GetDescriptionForPlayer]` (`G/localization/english/important_actions_l_english.yml:314-317`);
- the click opens `decision_detail` (`00_action_take_decision_or_interaction.txt:42-44`).

**E3. A custom alert that opens a decision** is vanilla `action_pam_decision_confession` (`pam_actions.txt:686-706`):
- `type = alert`;
- `icon = action_take_decision`;
- `can_execute_decision = <bare key>` in `check_create_action`;
- `decision:<key> = { open_view_data = decision_detail }` in `effect`.

Loc shape: `important_actions_l_english.yml:1479-1482`.

**E4. A per-title combined alert** is vanilla `action_wrong_holding_type` (`00_realm_actions.txt:213-256`):
- `combine_into_one = yes` and `is_dangerous = yes`;
- `every_held_title` → `try_create_important_action = { … landed_title = this }`;
- `effect` reads `scope:landed_title`.

The title-view click is `00_title_actions.txt:62-68`, and the combined loc keys are at `important_actions_l_english.yml:166-173`. The `.info` lists every loc suffix (`_important_actions.info:35-46`).

**E5. Icons are names, not paths.** `icon = <name>` resolves to `gfx/interface/icons/alerts/<name>.dds` (58 files; for example `icon = action_no_heir`, `00_inheritance_actions.txt:49`). With no `icon`, the action key itself is used (`_important_actions.info:7`), so **every mod action must set `icon`**, or it shows no icon.

**E6. AI is unaffected.** Important actions are evaluated for the player character only (`_important_actions.info:13`, "Scope: player character"). `should_create_alert` doesn't touch `ai_potential` or `ai_will_do`.

**E7. Concepts** (`_game_concepts.info:1-66`):
- Loc keys are `game_concept_<key>` and `game_concept_<key>_desc`. A missing `_desc` logs an error (`:6`).
- Each alias needs its own `game_concept_<alias>` and shares the original's desc (`:10-12`). Aliases are not listed in the encyclopedia (`:13`).
- An alias that collides with an existing key or alias is logged and skipped (`:14`).
- `parent` must exist (`:21`), and it may be a vanilla key.
- `texture` is optional. With none, there is no icon (`:30-31`).
- Links can take two forms: `[key|E]`, or `[Concept('key','Custom Text')|E]` (`:64-66`). The mod already uses the `Concept(...)` form for knights.

**E8. Vanilla already has a `region` concept** ("Region", a geographical area: `00_game_concepts.txt:2414-2416`; `game_concepts_l_english.yml:1479-1481`). The mod calls a County a "Shoal" (owner 2026-10-20; the v1 glossary said "Region", `OLD PROJECT VERSION/docs/localization_crusade.md:15-27`). Two consequences:
- **Never** link `[region|E]` for a mod Shoal. Link the county concept with display text: `[Concept('county','Shoal')|E]`.
- When CB-08's `replace/` renames `game_concept_county` to "Shoal", it no longer shares a name with vanilla's "Region" entry, so the re-wording of `game_concept_region` (below, §11) may be moot. **Confirm with the owner.**

---

## 4. Identifier table

### 4.1 INT1: decision edits (no new keys)

All in `common/decisions/`. "Group" means the `decision_group_type` added to the decision.

| Decision | File:line | Group | `should_create_alert` | Why |
|---|---|---|---|---|
| `eotg_decision_frontier_establish` | `eotg_frontier_decisions.txt:32` | **none** (remove `major`; rev. 2026-10-20) | `always = no` (rev. 2026-10-20) | Picker decision (E1a). The nudge is the custom action `eotg_action_frontier_establish_ready` (§4.2). `major` existed only for E1, so it goes too, and needs-human (1) closes. |
| `eotg_decision_unclaimed_raise_colours` | `eotg_unclaimed_decisions.txt:22` | **none** (remove `major`; rev. 2026-10-20) | `always = no` (rev. 2026-10-20) | Picker decision (E1a). The nudge is the custom action `eotg_action_unclaimed_colours_ready` (§4.2). |
| `eotg_decision_frontier_appoint_founder` | `eotg_frontier_decisions.txt:561` | none (stays `decisions`) | `always = no` | The custom alert `eotg_action_frontier_founderless` replaces it, per county. `always = no` stops a duplicate if the player toggles the decision on (vanilla form `bulls_decisions.txt:253`). |
| `eotg_decision_maintenance_protocol` | `eotg_augmentation_decisions.txt:171` | none | `NOT = { has_character_modifier = eotg_mod_implant_calibrated }` | Only matters if the player opts in. A narrowing filter, no default alert. |
| `eotg_decision_consult_physician` | `eotg_augmentation_decisions.txt:417` | none | same as Maintenance | As above. |
| all `*_debug_*` decisions (`eotg_frontier_decisions.txt:692,737,781,1197`; `eotg_unclaimed_decisions.txt:172,226`; `eotg_government_debug_decisions.txt`; `eotg_aug_kingpin_decisions.txt:16`) | — | none | `always = no` | Debug decisions never alert, even under `-debug_mode`. |

**Not changed, with reasons:**
- **Seek Augmentation:** it is always available to any adult with a little gold, so an alert would never go away.
- **Pursue Next Stage, Self-Repair, Excision, Embrace the Cascade, Restraints, Sedation, Appoint Warden, Augment Retainer, Partial Removal, Overclock Regression, Remove Implants:** these are personal choices with their own event prompts. Players can still toggle any of them important in the vanilla UI.
- **Invest, Sponsor, Withdraw, Abandon, Survey, Build, Explore:** routine. Invest is yearly, so an alert for it would be constant noise.

~~**Owner check:** moving Establish and Raise Colours into `major` also moves them to the top block with big buttons.~~ **Withdrawn 2026-10-20:** both stay in the default `decisions` group (E1a).

**Comment fix (QA INT1, should-fix 3):** the comments at `eotg_frontier_decisions.txt:36-39` and `eotg_unclaimed_decisions.txt:26-29` cite `pam_decisions.txt:4211-4212` as alert precedent. Replace them with: "picker decision, alert off as `pam_saint_decisions.txt:193-195`; the nudge is the custom action `eotg_action_...` (integration_v1.md §4.2, E1a)".

### 4.2 INT1: custom important actions

File: `common/important_actions/eotg_important_actions.txt` (new folder). Vanilla convention names actions `action_<x>`; invariant 1 makes them `eotg_action_<x>`.

| Key | `type` | `icon` (vanilla, reused) | `is_dangerous` | `combine_into_one` | `priority` | Shows exactly when | Gone when | `unimportant` | Click (`effect`) |
|---|---|---|---|---|---|---|---|---|---|
| `eotg_action_frontier_breaking` | `alert` | `action_title_lost_from_realm_on_succession` | yes | yes | 460 | per held county: `tier = tier_county`, `eotg_frontier_is_frontier = yes`, `eotg_frontier_strain_is_breaking = yes` | strain falls below the breaking band, or the Frontier completes, fails or is abandoned | none | `scope:landed_title = { open_view_data = { view = title_view_window } }` (`00_title_actions.txt:62-68`) |
| `eotg_action_frontier_founderless` | `alert` | `action_empty_council_position` | yes | yes | 450 | per held county: `tier = tier_county`, `eotg_frontier_is_frontier = yes`, `eotg_frontier_has_valid_founder = no` (the per-county form of `eotg_frontier_holds_founderless`, `eotg_frontier_triggers.txt:346-352`) | a valid founder is set, or the county stops being a Frontier **rev. 2026-10-20 (QA S1):** `eotg_frontier_founder_candidate_exists = no` (nobody can lead). Never `can_execute_decision` (E1a). Scope: root is the player, as in `effect` (`_important_actions.info:22-24`; bare character triggers as `00_diarchy_actions.txt:538-541`) | `decision:eotg_decision_frontier_appoint_founder = { open_view_data = decision_detail }` (E3) |
| `eotg_action_frontier_establish_ready` (new 2026-10-20) | `alert` | `action_take_decision` | no | **no** (one instance, `actor = root` only) | 300 | `eotg_frontier_establish_alertable = yes` (below) | a Frontier is established (`holds_frontier` turns yes), war starts, gold drops below the cost, or no held Shoal is Unsettled | none | `decision:eotg_decision_frontier_establish = { open_view_data = decision_detail }` |
| `eotg_action_unclaimed_colours_ready` (new 2026-10-20) | `alert` | `action_take_decision` | no | **no** | 290 | `eotg_unclaimed_colours_alertable = yes` (below) | colours are raised (the 5-year `eotg_unclaimed_colours_cd` is set, and the Shoal is now held and Unsettled, so the Establish alert takes over), gold or prestige drop, no Unclaimed Shoal is in reach, or a Frontier runs | none | `decision:eotg_decision_unclaimed_raise_colours = { open_view_data = decision_detail }` |
| `eotg_action_aug_calibration_lapsed` | `alert` | `action_take_decision` | no | no | 100 | `has_trait = eotg_cybernetics`, `NOT = { has_character_modifier = eotg_mod_implant_calibrated }`, `can_execute_decision = eotg_decision_maintenance_protocol`, and `NOT = { is_important_decision = eotg_decision_maintenance_protocol }` (no duplicate if the player toggled it) | calibration is re-applied by Maintenance or Consult the Physician, or the trait is lost | none | `decision:eotg_decision_maintenance_protocol = { open_view_data = decision_detail }` |

**Spam budget:**
- Breaking and founderless are each one combined, expandable entry, however many Shoals qualify. They are dangerous, so they sort above normal alerts, and both mean a Frontier may fail.
- Calibration shows at most once per lapse, about every 3 to 7 years per augmented ruler (`eotg_augmentation_decisions.txt:171-240`, modifier 3 or 5 years), and clears when acted on.
- No alert fires for a Frontier the player only **backs** (sponsor): it isn't theirs to fix.
- `soundeffect` is omitted, so the default define is used (`_important_actions.info:26`).

**Considered and rejected:**
- **"An augmentation offer is open."** Offers arrive as events or the interaction `eotg_aug_offer_augmentation_interaction`. Both already notify, and no persistent "offer open" state exists to read. An alert would duplicate the popup.
- **"A Frontier is claimable."** Covered by `eotg_action_unclaimed_colours_ready` (rev. 2026-10-20; it replaces the decision alert).

**Shape of the two decision-nudge actions (rev. 2026-10-20).**
- **Vanilla `action_take_decision`** (`00_action_take_decision_or_interaction.txt:5-47`):
  - `type = alert`, no `icon` (the key is the icon name, `_important_actions.info:7`) and no `priority` (default -1, `:9`);
  - an `every_decision` loop;
  - its click falls through to `scope:decision = { open_view_data = decision_detail }` (`:43-45`).
- **A fixed decision is opened by name**, as in `pam_actions.txt:686-706` and `tgp_actions.txt:128`. `action_pam_decision_confession` has:
  - `type = alert` and `icon = action_take_decision`;
  - an `if` wrapped around `try_create_important_action = { important_action_type = ... actor = root }`;
  - `effect = { decision:pam_decision_confession = { open_view_data = decision_detail } }`.
- **The mod copies the pam form exactly**, with one difference: the `limit` is the selection-free `*_alertable` trigger, not `can_execute_decision`.
- **Priorities:** 300 and 290 sit under the two dangerous Frontier alerts (460 and 450; dangerous alerts sort first anyway, `:9`) and above the vanilla decision alert (-1).
- **Spam:** at most one entry each, and it stays until its condition clears. The two never show together: Colours requires `holds_establishable = no`, and Establish requires it to be yes.
- **"Strained" (strain 4-5).** Too frequent. Breaking only.

**New scripted triggers (rev. 2026-10-20, QA S1/S2).** All are selection-free: they never read `scope:selected_item`.

| Key | File | Scope | Body | Notes |
|---|---|---|---|---|
| `eotg_frontier_founder_candidate_exists` | `eotg_frontier_triggers.txt`, directly above `eotg_frontier_holds_founderless` | character | the `OR` now at `eotg_frontier_decisions.txt:595-605`: `OR = { AND = { is_adult = yes is_imprisoned = no } any_courtier = { is_adult = yes is_imprisoned = no } }` | **Single source.** Appoint a Founder's `is_valid` becomes `custom_description = { text = eotg_decision_frontier_appoint_founder_candidate_tt eotg_frontier_founder_candidate_exists = yes }`. The tooltip key doesn't change. |
| `eotg_frontier_establish_alertable` | `eotg_frontier_triggers.txt`, character-scope block | character | `eotg_frontier_holds_establishable = yes` (`is_shown`, `:55-57`); `gold >= eotg_frontier_establish_cost_value` and `is_at_war = no` (`is_valid`, `:59-71`); `eotg_frontier_holds_frontier = no` (the old `should_create_alert` filter) | A mirror. `holds_establishable` also covers the picker test (`:73-79`): it is `any_held_title` with `eotg_frontier_can_establish`. Put keep-in-step comments both ways, on this trigger and on the decision's `is_valid`. |
| `eotg_unclaimed_colours_alertable` | `common/scripted_triggers/eotg_unclaimed_triggers.txt`, after `eotg_unclaimed_colours_ready` | character (root must be the actor; in `check_create_action` root is the player) | `eotg_unclaimed_can_claim = yes`; `any_in_global_list = { variable = eotg_unclaimed_counties eotg_unclaimed_is_unclaimed = yes holder ?= { eotg_is_unclaimed_holder = yes } eotg_unclaimed_in_reach = { ACTOR = root } }` (`is_shown` plus the picker test, `eotg_unclaimed_decisions.txt:43-48,64-71`); `eotg_unclaimed_colours_ready = yes`, `gold >= eotg_unclaimed_claim_gold_value` and `prestige >= eotg_unclaimed_claim_prestige_value` (`is_valid`, `:50-62`); `eotg_frontier_holds_frontier = no` and `eotg_frontier_holds_establishable = no` (the old filter) | A mirror, with the same keep-in-step comments. The `eotg_unclaimed_colours_cd` variable stays the cooldown authority; the alert only reads it. |

**Trigger-file order fix (QA should-fix 4):** in `eotg_frontier_triggers.txt:385-395`, `eotg_frontier_strain_is_breaking`, a county-scope trigger, sits between the comment `# frontier_v4.md A4.2: holds a Frontier with no valid founder ...` and `eotg_frontier_holds_founderless`. Move it, with its comment, into the county-scope block above `# -- Character scope --`. The A4.2 comment must sit directly on `eotg_frontier_holds_founderless`.

**Existing trigger** (county scope), in `common/scripted_triggers/eotg_frontier_triggers.txt`:

| Key | Body | Notes |
|---|---|---|
| `eotg_frontier_strain_is_breaking` | `exists = var:eotg_frontier_strain` and `var:eotg_frontier_strain >= 6` | One home for the breaking threshold. In the same batch, the two existing literals switch to it: `eotg_frontier_decisions.txt:547` and `eotg_frontier_effects.txt:623`. Strain is clamped to 0-8 (`eotg_frontier_effects.txt:550,557`). |

### 4.3 INT2: game concepts

File: `common/game_concepts/eotg_game_concepts.txt` (new folder). No `texture` (§10). For the shape, see `06_ce1_game_concepts.txt:1-22`: parent first, then children with `parent =` and `alias = { }`.

| Key | `parent` | `alias` | Name (`game_concept_<key>`) | Lore review |
|---|---|---|---|---|
| `eotg_augmentation` | — | `eotg_implant` `eotg_implants` | Augmentation (aliases: Implant, Implants) | **yes** |
| `eotg_aug_integration` | `eotg_augmentation` | `eotg_aug_stage` `eotg_aug_stages` | Integration (aliases: Stage, Stages) | no |
| `eotg_overclocked` | `eotg_augmentation` | — | `$trait_eotg_cybernetics_3$` | no |
| `eotg_neurofractured` | `eotg_augmentation` | — | `$trait_eotg_neurofractured$` | **yes** |
| `eotg_seamless` | `eotg_augmentation` | — | `$trait_eotg_total_integration$` | **yes** |
| `eotg_aug_policy` | `eotg_augmentation` | `eotg_aug_policies` | Augmentation Law(s) | **yes** (LAW AT 866) |
| `eotg_implant_technician` | `eotg_augmentation` | `eotg_implant_technicians` | `$eotg_aug_implant_technician_court_position$` | no |
| `eotg_frontier` | — | `eotg_frontiers` | Frontier / Frontiers | **yes** |
| `eotg_frontier_progress` | `eotg_frontier` | — | Frontier Progress | no |
| `eotg_frontier_strain` | `eotg_frontier` | `eotg_strain` | Strain | no |
| `eotg_frontier_founder` | `eotg_frontier` | `eotg_founder` `eotg_founders` | Founder / Founders | no |
| `eotg_local_ruler` | `eotg_frontier` | `eotg_local_rulers` | Local Ruler(s) | no |
| `eotg_frontier_sponsor` | `eotg_frontier` | `eotg_backer` `eotg_backers` | Backer(s) (the loc's word; the decision is "Back a Frontier", `eotg_frontier_l_english.yml:18`) | **yes** (no claim, no say) |
| `eotg_frontier_project` | `eotg_frontier` | `eotg_frontier_projects` | Frontier Project(s): the seven types | no |
| `eotg_unsettled_region` | `eotg_frontier` | `eotg_unsettled_regions` | Unsettled Shoal(s) | no |
| `eotg_region_charts` | `eotg_frontier` | — | name taken by the localizer from the Explore and `.042` loc (Unknown / Partial / Known) | no |
| `eotg_unclaimed_region` | — | `eotg_unclaimed_regions` | Unclaimed Shoal(s) | **yes** (LAW AT 866: no filing, registration or recognition) |
| `eotg_unsworn` | `eotg_unclaimed_region` | — | `$trait_eotg_unclaimed_folk$` | **yes** |
| `eotg_pmc` | `government` (vanilla, `00_game_concepts.txt:516`) | — | `$eotg_pmc_government$` | **yes** |
| `eotg_corporation` | `government` | — | `$eotg_corporation_government$` | **yes** |
| `eotg_cartel` | `government` | — | `$eotg_cartel_government$` | **yes** |
| `eotg_trade_oligarchy` | `government` | — | `$eotg_gobcorp_government$` | **yes** |

Notes on the table:
- **"Region types"** in the brief is covered by four entries. A Region can be Unsettled, Unclaimed or a Frontier, and it carries a chart level and a project type.
- **Governments parent to vanilla `government`, not to a new mod parent.** The tooltip then says these are forms of government, as vanilla's do, and no new prose is needed. **Deviation from the brief** ("under a parent"): the parent exists, but it is vanilla's.
- **Script keys and concept keys differ in two places:**
  - `eotg_trade_oligarchy` is the concept for `eotg_gobcorp_government`, because the concept key is what loc authors type.
  - `eotg_seamless` is the concept for the trait `eotg_total_integration`.
- **Names reuse existing keys** through `$key$` wherever a key already exists, so each term has one source (invariant 6).

**Collision check (done 2026-10-20).**
- All 2,585 vanilla concept keys and aliases were extracted from `G/common/game_concepts/*.txt` (scratchpad `vanilla_concepts.txt`).
- None starts with `eotg`. The mod has no `common/game_concepts/` today.
- All 22 keys and 16 aliases above are unique, both among themselves and against vanilla.
- **Re-run this grep in QA**, because a later DLC could add keys.

**Desc content: what each `_desc` must say (facts only; the localizer writes the prose).**
- `eotg_augmentation`: elective cybernetic implants; who fits them (clinics, physicians, back-street fitters); progress along Integration; the costs (stress, wear, the risk of fracture, named but never quantified); and that realm law can ban, license, tolerate or favour it. Links: `[eotg_aug_integration|E]`, `[eotg_aug_policy|E]`, `[eotg_implant_technician|E]`.
- `eotg_aug_integration`: one trait with a track. The stages are Augmented, Enhanced and Overclocked. Moving up a stage is a decision or an offer, and stepping down is a procedure. **No XP numbers.**
- `eotg_overclocked`: the top stage. Strongest benefits; heaviest wear; maintenance matters.
- `eotg_neurofractured`: what a fracture is (the person and the machine no longer agree); Excision exists. **Never imply a cure rate.**
- `eotg_seamless`: a complete integration with nothing left in the person that argues back. Says that text reads differently for them. **Lore-sensitive.**
- `eotg_aug_policy`: the four positions, set by the top ruler for the realm (`eotg_aug_policy_set_by_liege_tt`). **No authority above the realm.**
- `eotg_implant_technician`: a court position; cheaper and safer procedures; can be lent.
- `eotg_frontier`: a project to settle a Shoal that is Unsettled or abandoned; held by the Shoal's holder; ends in a new holding or in failure.
- `eotg_frontier_progress`: grows yearly from investment, infrastructure and events; bands such as Foothold unlock infrastructure slots.
- `eotg_frontier_strain`: the settlers' hardship. It rises with no founder, war, danger and quarrels. At breaking point the Frontier can fail.
- `eotg_frontier_founder`: leads the work. Without one, strain climbs. Appointed by decision.
- `eotg_local_ruler`: on completion, a founder may be given the new holding as its ruler (`frontier_v4.md` "Founder first").
- `eotg_frontier_sponsor`: another ruler pays toward the work. **No claim and no say over the Shoal.**
- `eotg_frontier_project`: the seven types (Settlement, Trade, Mining, Military, Religious, Research, Administrative), chosen at establishment.
- `eotg_unsettled_region`: a Shoal whose Systems were never properly settled; where a Frontier can start.
- `eotg_region_charts`: Unknown, Partial or Known; expeditions chart a Shoal; charts give a later Frontier a head start.
- `eotg_unclaimed_region`: a Shoal no ruler holds, kept by a placeholder; it can be claimed with Raise Your Colours at a cost in gold and prestige; it costs attackers attrition. **No filing, registration or recognition.**
- `eotg_unsworn`: the scattered people of an Unclaimed Shoal; no court and no oath.
- Governments: one paragraph each, drawn from the existing `eotg_*_government_desc` keys. The concept desc may simply be `$eotg_pmc_government_desc$` and so on, the cheapest option with one source.

Inside descs, link a Shoal with `[Concept('county','Shoal')|E]` (E8), never `[region|E]`.

---

## 5. File placement

| Path | Owner | New folder? |
|---|---|---|
| `common/important_actions/eotg_important_actions.txt` | eotg-scripter | **yes**: add to the CLAUDE.md placement table |
| `common/game_concepts/eotg_game_concepts.txt` | eotg-scripter | **yes**: add to the CLAUDE.md placement table |
| `common/scripted_triggers/eotg_frontier_triggers.txt` (one new trigger) | eotg-scripter | no |
| `common/decisions/eotg_*.txt` (edits per §4.1) | eotg-scripter | no |
| `localization/english/eotg_important_actions_l_english.yml` | eotg-localizer | no (UTF-8 BOM) |
| `localization/english/eotg_game_concepts_l_english.yml` | eotg-localizer | no (UTF-8 BOM) |

No `replace_path`. No `replace/` file in this spec: the `game_concept_region` and `game_concept_county` renames belong to CB-08.

## 6. Wiring

- **Alerts:** no on_action. The engine evaluates `check_create_action` for the player (E6). No decision alert remains (rev. 2026-10-20, E1a): the two decision nudges are custom actions.
- **Concepts:** no wiring. They are reachable from any loc string and from the encyclopedia.
- **Tiers:** all three actions and both decision alerts work at every tier the decision or system exists at (county and above for Frontier; any ruler for calibration). Nothing is gated to emperor level.
- **Cooldowns:** none added. The alerts read the cooldown state that already exists (the `eotg_unclaimed_colours_cd` variable through `eotg_unclaimed_colours_ready`; Maintenance through `can_execute_decision`) and never set one, so cooldown authority stays where it is.

## 7. Vanilla precedent (cited)

| Thing | Vanilla source |
|---|---|
| Decision alert pipeline | `common/important_actions/00_action_take_decision_or_interaction.txt:5-45` |
| Importance through the group | `_decisions.info:5-6`; `common/decision_group_types/_decision_group_types.info:5`; `00_decision_group_types.txt:42-46` |
| ~~`major` + `should_create_alert`~~ (withdrawn) | `pam_decisions.txt:4211-4212` is an `always = no` case (E1) |
| Picker decision, alert off | `pam_saint_decisions.txt:193-195`; `bulls_decisions.txt:251-253` (E1a) |
| Fixed-decision nudge action | `pam_actions.txt:686-706`, `:1170-1189`; `tgp_actions.txt:128` |
| `should_create_alert = { always = no }` | `common/decisions/dlc_decisions/pam/bulls_decisions.txt:253` |
| Custom alert that opens a decision | `common/important_actions/pam_actions.txt:686-706`; loc `localization/english/important_actions_l_english.yml:1479-1482` |
| Per-title, combined, dangerous alert | `common/important_actions/00_realm_actions.txt:213-256`; loc `important_actions_l_english.yml:166-173` |
| Title-view click, `priority` | `common/important_actions/00_title_actions.txt:2-4,62-68` |
| Icon by name | `00_inheritance_actions.txt:49`; folder `gfx/interface/icons/alerts/` |
| Action fields and loc suffixes | `common/important_actions/_important_actions.info:3-46` |
| Concept fields, aliases, link syntax | `common/game_concepts/_game_concepts.info:1-66` |
| Parent and alias layout | `common/game_concepts/06_ce1_game_concepts.txt:1-22` |
| Concept with custom display text | `_game_concepts.info:65` |

## 8. Loc surface

**Decision alerts (§4.1):** none remain (rev. 2026-10-20, E1a). The two decision nudges are now the custom actions below.

**Custom actions (§4.2)**, in `eotg_important_actions_l_english.yml`, following the vanilla tone (`important_actions_l_english.yml:166-173,1479-1482`):

| Action | Keys |
|---|---|
| `eotg_action_frontier_breaking` | `<k>`, `<k>_label`, `<k>_desc`, `<k>_click`, `<k>_combined_label`, `<k>_combined_group_label` (uses `$NUM$`), `<k>_combined_group_name`, `<k>_combined_group_description` |
| `eotg_action_frontier_founderless` | the same 8, plus `<k>_unimportant` and `<k>_combined_unimportant` |
| `eotg_action_frontier_establish_ready` (new) | all 10 suffixes from the lint convention (`docs/tools/eotg_lint_loc_conventions.json` `important_actions`; `_important_actions.info:35-46`). The `_combined_*` and `_unimportant` ones never show at runtime (`combine_into_one = no`, no `unimportant`), but they are written for lint parity. Intent: "Decision Available: Establish a Frontier"; you hold an Unsettled Shoal and can afford to settle it. |
| `eotg_action_unclaimed_colours_ready` (new) | the same 10. Intent: "Decision Available: Raise Your Colours"; an Unclaimed Shoal lies within reach. LAW AT 866: never "claim filed / recognized". |
| `eotg_action_aug_calibration_lapsed` | `<k>`, `<k>_label`, `<k>_desc`, `<k>_click` |

That makes 42 keys: 8 + 10 + 10 + 10 + 4. The previous 22 is superseded. In per-title keys the title is `[landed_title.GetName]` (bare, never `[scope:`).

**Concepts (§4.3)**, in `eotg_game_concepts_l_english.yml`: 22 × (`game_concept_<k>` + `_desc`) + 16 alias names = **60 keys**.

**Voice:**
- Alerts are UI voice (vanilla's), not character voice, so there are no `_seamless` variants. A Seamless voice for alerts is deferred (§10).
- Canadian English throughout (colour, favour, -ize).
- Glossary terms throughout: **Shoal** (the county tier, owner 2026-10-20; it replaces "Shoal"), System, Sector, Port, Bastion.
- Never "County".

**`replace/` flags (CB-08, not this spec):**
- `game_concept_county` → "Shoal";
- `game_concept_region` needs a new name (E8).

## 9. Lore constraints

- **LAW AT 866** (SETTING LORE ERRATA): no authority above the realm. Nothing is filed, registered, licensed, recognized or chartered by any outside body. This binds the Augmentation, Augmentation Law, Unclaimed Shoal, Backer and government concept descs.
- **Never-name lists** (`docs/specs/cybernetics_v2.md` §5.2-5.3, extended in `docs/lore/REVIEW_866.md:38-39`): no Blackstar, P&D, Calix, Pill Mob, Concrete Cartel, Trauma Team and so on in concept text. No state augmentation programmes, and no remote-kill implants.
- **866 AG:** there is no Galactic League, so concept text must never imply a galaxy-wide order.
- **Fracture risk stays hidden** (§2).
- **Knights:** never hard-code "knight" (dynamic term). Not expected here, but it binds every desc.
- **Route to eotg-lore-keeper before the localizer writes:** the 12 rows marked **yes** in §4.3. The content notes above are the brief for that review. The alert texts need no lore review: they describe mechanics only.

## 10. Deferred

- **Textures.** No `texture =` on any concept for now. When art lands, concept icons go to `gfx/interface/icons/eotg_concepts/<concept_key>.dds` (the path form in `_game_concepts.info:33`). Existing assets could stand in later:
  - `eotg_cybernetics.dds` and `eotg_neurofractured.dds` (trait icons);
  - `eotg_mod_aug_self_repair.dds`;
  - `gfx/interface/icons/government_types/`.
- **Custom alert icons.** All three reuse vanilla alert icons. Custom ones would go in `gfx/interface/icons/alerts/eotg_action_*.dds`, with `icon =` pointing at the name.
- **A mod "EotG" concept hub parent.** Not needed; possible later.
- **Seamless-voice alert text.** Possible through `Custom()` loc later.
- **The Kingpin and Void concepts.** Void isn't lifted yet. Kingpin needs CB-57 X2 settled first.
- **A "Strained" (strain 4-5) alert.** Rejected as noise. Revisit after play-testing.

---

## 11. Batches

| Batch | Agent | Contents | Depends on |
|---|---|---|---|
| **INT1a** | eotg-scripter | §4.1 decision edits, §4.2 actions file, `eotg_frontier_strain_is_breaking` plus the two call-site switches | — |
| **INT1b** | eotg-localizer | §8 action keys (22) | INT1a |
| **INT2a** | eotg-scripter | §4.3 concepts file | — (parallel with INT1) |
| **INT2b** | eotg-lore-keeper | Review the 12 lore rows' content notes; rule on wording limits | INT2a not needed |
| **INT2c** | eotg-localizer | §8 concept keys (60) | INT2a, INT2b |
| **INT3** | eotg-localizer | The linking pass (§12) | INT2c, and QA green on INT2 |

**Orchestrator, on dispatch:**
- add `common/important_actions/` and `common/game_concepts/` to the CLAUDE.md placement table;
- add a taskboard item for the `game_concept_region` rename under CB-08.

## 12. INT3: the linking pass

**Rule (vanilla density).** Vanilla links concepts in about 11% of decision descs (57 of 515), and in 25 of 10,651 event desc keys. So:
- **Link:** `*_desc` of decisions, traits, interactions, laws (`*_effects`), court positions and modifiers; `*_tooltip`, `*_selection_tt`, `*_tt` and effect tooltips; government `_desc`; the concept descs themselves.
- **Don't link:** event `.desc` body text, option text, toasts, names.
- **Link once:** the first mention per string only.

**Syntax:**
- `[eotg_frontier|E]` when the display text equals the concept name.
- `[Concept('eotg_frontier','Frontiers')|E]` when it doesn't (plural, case, inflection), unless an alias already covers it.
- `[Concept('county','Shoal')|E]` for Shoal, until CB-08 lands.

**Priority targets** (non-event lines mentioning the term, counted 2026-10-20 across `localization/english/*.yml`):

| Term | Lines |
|---|---|
| Frontier | 186 (decisions, tooltips, modifiers) |
| PMC, Corporation, Cartel | 69 each (government loc) |
| Unsworn | 20 |
| strain | 19 |
| Trade Oligarchy | 15 |
| Unclaimed Shoal | 14 |
| Unsettled | 10 |
| Overclocked | 10 |
| founder | 8 |
| Implant Technician | 5 |
| Neurofractured, Seamless | 2 each |

**Order:** decision `_desc` and `_tooltip` first, then trait descs, then laws and the court position, then government descs.

**Exclusions:**
- Strings already in a `Concept('knight', …)` construct.
- The generated seller-name loc (`eotg_aug_seller_names_l_english.yml`, generated; never hand-edit).
- `_seamless` variant strings: leave them unlinked, since the flat voice is deliberate.

The localizer lists every converted key in its handoff.

## 13. Definition of done

1. **Tiger:** clean, apart from the CLAUDE.md known-benign list, on all touched files.
2. **PX LSP:** no `missing-required-loc` for any `eotg_action_*` or `game_concept_eotg_*` key.
3. **`error.log` after a load** has none of these:
   - "alias collides";
   - a missing `game_concept_*_desc`;
   - an unknown concept `parent`;
   - an unknown important-action icon;
   - "Unexpected token" in `important_actions` or `game_concepts`.
4. **Greps** over the INT files must be empty:
   - `grep -rn 'scope:' localization/english/eotg_important_actions_l_english.yml localization/english/eotg_game_concepts_l_english.yml`;
   - `grep -rnE 'eotg_[ekdcb]_' common/important_actions common/game_concepts`;
   - `grep -rn '\[region|E\]' localization`.
5. **Concept parity:** every key and alias in `eotg_game_concepts.txt` has `game_concept_<x>`, and every non-alias key has `_desc` (QA script: compare the two lists).
6. **In game (sub-mod or temporary map; `docs/qa/HOW_TO_TEST_IN_GAME.md`):**
   - a. A ruler with an Unsettled Shoal, enough gold, at peace and with no Frontier sees `eotg_action_frontier_establish_ready` exactly once. Clicking it opens the Establish decision. After establishing, the alert is gone. Toggling the decision "important" adds no second alert.
   - b. With an Unclaimed Shoal in reach and the cooldown ready, while holding no Frontier and no establishable Shoal, `eotg_action_unclaimed_colours_ready` shows, and clicking it opens Raise Your Colours. After raising colours it goes, and (a) appears instead. It never shows alongside (a).
   - b2. A founderless Frontier, with an adult free courtier at court, shows the founderless entry as **important** (not greyed). With no candidate (a child ruler and no adult courtiers), it shows as unimportant.
   - b3. `grep -n 'can_execute_decision' common/important_actions/eotg_important_actions.txt` matches only the calibration action (Maintenance has no picker).
   - c. `-debug_mode`:
     - set a Frontier's founder to none: one dangerous "founderless" group entry appears;
     - make two Frontiers founderless: the group shows 2;
     - appoint a founder: that entry clears;
     - the Appoint a Founder decision alert never also appears.
   - d. Raise a Frontier's strain to 6 or more (debug tick or event options): the "breaking" group appears, and clicking opens the Shoal's title view. At 5, it's gone.
   - e. An augmented ruler with `eotg_mod_implant_calibrated` removed and Maintenance off cooldown sees the calibration alert. Taking Maintenance clears it. Toggling Maintenance "important" in the decision UI replaces it with the vanilla decision alert, never both.
   - f. No debug decision ever alerts.
   - g. The encyclopedia lists Augmentation, Frontier and Unclaimed Shoal with their children. The four governments appear under vanilla Government. Hovering `[eotg_frontier_strain|E]` in any converted string shows the tooltip with "Frontier" as the parent.
7. **AI:** the `ai_will_do` and `ai_potential` of every touched decision are byte-identical before and after (diff check).

## 14. Verification items (eotg-vanilla-scout, before INT1a merges)

- **V1.** `is_important_decision = <bare key>`. Vanilla shows only `= scope:decision` (`00_action_take_decision_or_interaction.txt:12`). If the bare key is rejected, use `decision:eotg_decision_maintenance_protocol`. `can_execute_decision = <bare key>` is proven (`pam_actions.txt:693`).
- **V2.** `should_create_alert` scope: assumed to be the character (as `is_valid`). Confirm on any vanilla non-`always` use, or in game with test 6a.
- **V3.** A mod concept with a vanilla `parent = government` renders the parent line (CONCEPT_TEXT, `core_l_english.yml:848`). The fallback is a mod parent `eotg_governments`, plus 2 loc keys.

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Build INT1a (§4.1 decision edits, §4.2 `common/important_actions/eotg_important_actions.txt`, the `eotg_frontier_strain_is_breaking` trigger and its two call sites) and INT2a (§4.3 `common/game_concepts/eotg_game_concepts.txt`) from `docs/specs/integration_v1.md`, after eotg-vanilla-scout clears V1-V3 (§14).
- files: docs/specs/integration_v1.md
- needs-loc: 22 action keys (§8) after INT1a; 60 concept keys (§8) after INT2a and lore review; INT3 linking pass (§12) after INT2 passes QA
- needs-lore: review the 12 lore-flagged concept rows and content notes in §4.3 (Augmentation, Neurofractured, Seamless, Augmentation Law, Frontier, Backer, Unclaimed Shoal, Unsworn, PMC, Corporation, Cartel, Trade Oligarchy) against LAW AT 866 and the never-name lists
- needs-human: (1) confirm Establish and Raise Your Colours in the vanilla `major` decision block (big buttons, top of list); (2) the CB-08 rename of vanilla `game_concept_region` to avoid two "Region" encyclopedia entries; (3) the orchestrator adds `common/important_actions/` and `common/game_concepts/` to the CLAUDE.md placement table

### HANDOFF (eotg-scripter, INT1 Frontier/Unclaimed side, 2026-10-20)
- status: partial
- built: §4.1 rows for Establish and Raise Your Colours (`major` + `should_create_alert`), Appoint a Founder and the six Frontier/Unclaimed debug decisions (`always = no`); §4.2 `eotg_action_frontier_breaking` and `eotg_action_frontier_founderless` in `common/important_actions/eotg_important_actions.txt`; `eotg_frontier_strain_is_breaking` with three call sites switched (decisions, effects, and event `.002`, which also used the literal).
- deferred (cybernetics files in use by another scripter): §4.2 `eotg_action_aug_calibration_lapsed`; the §4.1 rows for Maintenance Protocol and Consult Physician; the debug rows in `eotg_government_debug_decisions.txt` and `eotg_aug_kingpin_decisions.txt`. Spec V1 (`is_important_decision` with a bare key) still applies to the deferred alert.
- test-in-game: ~~`can_execute_decision` with no item picked~~ superseded (2026-10-20 rework): the alerts now use selection-free mirror triggers and no `can_execute_decision`; run tests 6a to 6d and 6f.
- needs-loc: 18 keys, `docs/specs/build/INT1_loc_keys.txt`.

### HANDOFF (eotg-architect, INT1 QA fix-first, 2026-10-20)
- status: done
- next: eotg-scripter
- ask: Fix INT1 per the rev. 2026-10-20 rows in §3 (E1a), §4.1 and §4.2. The build list:
  1. Establish and Raise Your Colours: remove `decision_group_type = major`, set `should_create_alert = { always = no }`, and correct the comments (`eotg_frontier_decisions.txt:36-39`, `eotg_unclaimed_decisions.txt:26-29`).
  2. Add the triggers `eotg_frontier_founder_candidate_exists` (and use it in Appoint a Founder's `is_valid`), `eotg_frontier_establish_alertable` and `eotg_unclaimed_colours_alertable`.
  3. The founderless action's `unimportant` becomes `eotg_frontier_founder_candidate_exists = no`.
  4. Add `eotg_action_frontier_establish_ready` (300) and `eotg_action_unclaimed_colours_ready` (290), in the `action_pam_decision_confession` shape.
  5. Move `eotg_frontier_strain_is_breaking` into the county-scope block.
- files: docs/specs/integration_v1.md
- needs-loc: 20 new keys (2 actions x 10 suffixes, §8), using Shoal; update `docs/specs/build/INT1_loc_keys.txt`
- needs-human: none new (the `major` big-button question is withdrawn)
