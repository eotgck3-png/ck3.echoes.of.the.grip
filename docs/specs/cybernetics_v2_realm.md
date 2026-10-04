# Spec: Cybernetics v2: realm policy (G7), the Implant Technician (G10), vanilla activities (G6)

**Author:** eotg-architect, 2026-10-04
**Authorized by:** the human, 2026-10-04 (relayed by the coordinator): G7 (realm augmentation policy), G10 (Implant Technician court position) and G6 (reactions in vanilla activities: tournaments, feasts, hunts, pilgrimages), from [`docs/qa/cybernetics_content_gaps_v2.md`](../qa/cybernetics_content_gaps_v2.md) Part 2. This is the last of the four content-gap batches.
**Index:** [cybernetics_v2.md](cybernetics_v2.md). Index §1 rules 1–12 and the §5 lore register (with today's never-name extension) apply to everything here.
**Builds on, does not re-spec:**
- [cybernetics_v2_procedures.md](cybernetics_v2_procedures.md): the roll (`eotg_aug_procedure_roll_effect` / `eotg_aug_procedure_effect`, params `PATIENT`, `PROVIDER`, `PROCEDURE`, `SURGEON`), `eotg_aug_proc_bad_factor`, `eotg_aug_save_surgeon_effect`, the price multipliers, `eotg_aug_procedure_apply_effect`.
- [cybernetics_v2_interactions.md](cybernetics_v2_interactions.md): Offer Augmentation, Demand Removal (whose deferred "refusal as a crime" G7 enables, §4.3), and the deferred "Lend Your Surgeon" (built here as §4.6, under the name **Borrow Their Technician**).
- [cybernetics_v2_procedures_lore.md](cybernetics_v2_procedures_lore.md): the 866 tech ceiling, the residue register, "word has got out".
- [`docs/lore/REVIEW_866.md`](../lore/REVIEW_866.md): LAW AT 866.

**Lore review: done** (eotg-lore-keeper, 2026-10-04): approved with must-fixes R1–R8, all folded in below. **Binding names and loc renderings:** [cybernetics_v2_realm_lore.md](cybernetics_v2_realm_lore.md).
**Also binding:** [cybernetics_v2_balance.md](cybernetics_v2_balance.md) (HQ1 pacing, HQ2 world targets, §9.2 observer run), [cybernetics_v2_trait_depth.md](cybernetics_v2_trait_depth.md) §5.2 (G9 stress rows: no option here writes its own `stress_impact` line for impatient, gluttonous, temperate or fickle).

**Build state.** Neither the procedures spec nor the interactions spec is built yet: there is no `events/eotg_augmentation_procedures.txt` and no `common/character_interactions/` in the tree. Their pieces that this spec amends (§3.2) are therefore **built together** with them, in the order procedures → interactions → this spec.

**Size.**
- **7 new events** (all visible): 6 activity events, 1 realm event. **Below the ~10 flag; no further yes needed.**
- 1 law group with 4 laws, 1 court position, 1 character interaction, 7 custom on_actions extending 13 vanilla activity hooks additively.
- 2 new namespaces (`eotg_aug_act`, `eotg_aug_realm`), 2 new event files.
- 3 new script folders: `common/law_groups/`, `common/laws/`, `common/court_positions/types/`.
- 4 new opinion modifiers. No new trait, static modifier, decision, story cycle or death reason.
- Art debt: 4 law icons and 1 court-position icon (§3.1, owner human).
- About 120 loc keys (§7).

---

## 0. Engine facts this spec rests on (vanilla 1.20.0.3 wins over the `.info` files)

All paths under `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`.

| Fact | Evidence |
|---|---|
| **1.20 splits laws in two.** A law **group** lives in `common/law_groups/` (`default`, `cumulative`, `flag`, `can_change_law_group`, `can_have_group`, `required_government_flag`). Each **law** lives in `common/laws/` and names its group with `law_group_type` and an `index`. | `common/law_groups/_law_groups.info:1-48`; `common/laws/_laws.info:1-10`; vanilla `common/law_groups/00_realm_law_groups.txt:22` (`camp_purpose`), `common/laws/00_realm_laws.txt:801-833` (`camp_purpose_wanderers`, `law_group_type = camp_purpose`) |
| **The skill's and Tiger's picture of laws is older.** The skill's `reference/common/laws/_laws.info:1-40` nests laws inside the group in one file. Vanilla 1.20 does not. Follow vanilla. Tiger 1.17 targets 1.18.3 and may flag `common/law_groups/` or `law_group_type`; check any such finding against `00_realm_law_groups.txt` / `00_realm_laws.txt` before treating it as real. | as left |
| **`flag = realm_law` puts a group in the My Realm window.** The window lists every group with that flag whose `IsAvailable` is true; `realm_law_no_number` hides the level number for a pick-one group. | `common/laws/_laws.info` "Hardcoded Flags" (`flag = realm_law - Will show up in My Realm window`); `gui/window_my_realm.gui:1280-1327` (visibility test at :1293, `realm_law_no_number` at :1303/:1309); `00_realm_law_groups.txt:70-76` (`crowned_laws`, a pick-one group with both flags) |
| **A pick-one policy law** carries its own `modifier`, `pass_cost`, `can_pass`, `on_pass` and `ai_will_do` (score > 0 is enacted; the highest wins; evaluated in the rare task tick). | `00_realm_laws.txt:2554-2646` (`mandala_decree_*`: prestige `pass_cost`, trait-weighted `ai_will_do`); `_laws.info` `ai_will_do` brief |
| **Law cooldown** is a variable set in `on_pass` and tested in `can_pass` with a `custom_description`. | `00_realm_laws.txt:76-118` (`crown_authority_1`: `has_crown_authority_cooldown`, `set_variable = { name = crown_authority_cooldown  years = @crown_authority_cooldown_years }`); `02_admininistrative_laws.txt:36-40, 70-77` |
| **`can_change_law_group`** leaves a group visible but locked for rulers who fail it. **`can_keep`** failing reverts the law to the group default within a month. Laws are inherited by heirs. | `_law_groups.info:28-34`; `_laws.info` `can_keep` brief and NOTES "Inheritance" |
| **Vassal opinion of a law** is expressed in the law's `modifier` through **vassal-stance** opinion modifiers (`zealot_opinion`, `glory_hound_opinion`, `parochial_opinion`, `belligerent_opinion`, `courtly_opinion`). Each vassal ruler holds one stance, scored from personality. | `00_realm_laws.txt:24-30, 133-141, 219-227` (crown authority); `common/vassal_stances/_vassal_stances.info:1-45` (`key_opinion` is generated per stance); stances at `common/vassal_stances/00_vassal_stances.txt:1` (courtly), `:172` (glory_hound: brave +50, ambitious +50), `:334` (parochial: content +50), `:510` (zealot: zealous +100, humble +100, cynical −50, at :523), `:996` (belligerent: ambitious +50) |
| **Refusing a demand is a crime only under law.** The demander's leverage is an opinion with `imprisonment_reason = yes` given through `reverse_add_opinion` on decline, gated on a law trigger and `target_is_liege_or_above`. The `ai_accept` side adds +50 with a "declining is a crime" desc, and the interaction desc gains a triggered line. | `common/character_interactions/00_religious_interactions.txt:160-180` (triggered desc), `:640-672` (`on_decline` branch); `common/opinion_modifiers/00_religious_opinions.txt:118-123` (`illegal_resisted_conversion_opinion`: −15, 10 years, `imprisonment_reason`, `revoke_title_reason`); `common/scripted_modifiers/00_religion_scripted_modifiers.txt:262-275` (+50, `ASK_FOR_CONVERSION_DECLINING_IS_A_CRIME`) |
| **Imprisonment through the vanilla helper.** | `common/scripted_effects/00_prison_effects.txt:1644` (`imprison_character_effect = { TARGET IMPRISONER }`); the mod already uses it (QA round 2 M5) |
| **Court positions** live in `common/court_positions/types/` (1.20). Fields per vanilla: `sort_order`, `max_available_positions`, `skill`, `court_position_asset`, `opinion`, `aptitude_level_breakpoints`, `aptitude`, `is_shown`, `valid_position`, `is_shown_character`, `valid_character`, `revoke_cost`, `salary`, `received_salary`, `scaling_employer_modifiers` (0–5 levels allowed), `custom_employer_modifier_description`, `modifier`, `on_court_position_received / _revoked / _invalidated / _vacated`, `ai_position_score` (hire > 0, fire < −50), `ai_candidate_score`. | `common/court_positions/types/_court_positions.info` (whole file); `00_court_positions.txt:41-562` (`court_physician_court_position`, base game, no DLC gate); `:10896-11193` (`court_artificer_court_position`) |
| **Court-position triggers and links:** `employs_court_position`, `has_court_position`, `aptitude = { court_position = X  value >= N }` (0–4 = terrible…excellent), `court_position:X` link. | `_court_positions.info` "Triggers" and "Links" sections |
| **Court-position helpers reused:** `base_court_position_validity_trigger = { EMPLOYER }`, `court_position_employee_shown_trigger`, `basic_gained/revoked/invalidated_court_position_effect`, `court_position_vacated_event_effect = { COURT_POSITION_TYPE }`, `court_position_physician_salary`, `regular_court_position_opinion`, `minor_court_position_prestige_revoke_cost`, `court_position_candidate_score_base_value`, `court_position_candidate_aptitude_value`, `court_position_debt_considerations_value`, `court_position_aptitude_low_penalty_value`, `general_aptitude_bonus`. | `scripted_triggers/00_court_position_triggers.txt:398-411, 494-497, 2053-2056`; `scripted_effects/00_court_position_effects.txt:7, 96, 147, 3414`; `script_values/00_court_position_values.txt:846, 2260, 2338`; `script_values/00_ep1_script_values.txt:353, 389` |
| **Activity hooks the mod can extend additively** (all base game except tournaments; tournaments are the Tours & Tournaments DLC, `has_ep2_dlc_trigger` = `has_dlc_feature = tours_and_tournaments`, `scripted_triggers/00_has_dlc_scripted_triggers.txt:110`). Root and scopes per hook in §4.7. | `common/on_action/dlc/ep2/ep2_tournament_on_actions.txt:28` (`tournament_active_state_pulse`), `:82, :140, :213, :244, :282, :316, :349` (contest random pulses), `:699` (`tournament_opening_on_action`); `common/on_action/activities/feast_on_actions.txt:50`; `hunt_on_actions.txt:17`; `pilgrimage_on_actions.txt:380` |
| **Activity levers vanilla events use:** `activity_tournament_change_contestant_score_effect = { SCORE = increase_major … decrease_minor }` (no-op unless the target is competing); `hunt_activity_success_change_effect = { CHANGE = increase_minor/_medium/_major }`; a contestant withdraws by `add_character_flag = tournament_not_competing` + `custom_tooltip = tournament_not_competing_tt` + `scope:activity = { remove_from_guest_subset = { name = contestant  target = … } }`. | `scripted_effects/04_dlc_ep2_tournament_effects.txt:13-60`; `script_values/04_ep2_tournament_values.txt:1962-1984`; `scripted_effects/00_hunt_effects.txt:948-966`; `script_values/04_ep2_hunt_values.txt:91-110`; `events/activities/tournaments/tournament_events.txt:4498-4499, 9315-9323`; `scripted_triggers/04_ep2_tournament_triggers.txt:21-37` (`activity_is_competing_trigger`, `activity_is_valid_tournament_contestant`, the `tournament_not_competing` opt-out) |
| **Triggered option names** (`name = { trigger = { … }  text = key }`). | `events/health_events.txt:1143-1146` |
| Scaled values used: `minor/medium/major_prestige_value` 75/150/350, `minor/medium/major_piety_value` 50/100/250, `minor_dread_gain` 10. | `script_values/00_basic_values.txt:731, 1001-1003, 1132-1134` |

---

## 1. Purpose & gate

The gaps doc's Part 2 headline: the system is rich in events about yourself and thin wherever CK3 lets you act on the realm and the people around you. This spec closes the last three gaps.

- **G7. A realm policy on augmentation.** A vanilla realm-law group, **Augmentation**, with four laws: **Ban**, **License**, **Tolerate** (default) and **Favor**. It changes which providers are open, how often back-street work is discovered, whether discovery and refusing a removal are **crimes** (vanilla's imprisonment-reason mechanism), how often augmentation offers come, and how vassals feel about their liege. It is **realm-local**: the independent ruler at the top of a realm sets it; everyone in the realm lives under it; there is no higher law.
- **G10. The Implant Technician.** A court position. It is the best surgeon a court can have for the procedure roll (through the roll's `SURGEON` parameter), makes the physician-route price and Maintenance cheaper, and makes Overclocked hardware run slightly cooler. It can be lent to another court (**Borrow Their Technician**, the interactions spec's deferred "Lend Your Surgeon", §4.6).
- **G6. Activities.** Augmented people at tournaments (barred entrants, running hot to win, cheating accusations), feasts, hunts and pilgrimages, through 6 events hooked additively into vanilla activity on_actions.

**Gate 3 (Systems), built against the temporary map** (`docs/agent_workflow.md` §5 rule 2; `CLAUDE.md` mod-exclusive exception). **Not blocked.**
- **Map-agnostic.** No title, province, character, culture or faith keys. Realm membership goes through `top_liege` / `liege`; vassal reactions through vanilla vassal stances (personality-scored, key-free). Faith reactions only through `zealous` / `cynical` and piety (index §1 rule 9).
- **Two testability limits, not blockers** (§9 item 12): tournaments need the Tours & Tournaments DLC; pilgrimages need holy sites, which the temporary map may not have until the faiths from the region briefs land.

---

## 2. Signature resource

Unchanged: **`eotg_fracture_risk`** (hidden, 0–100; pressure for Neurofractured) plus **tier** (track XP 0/50/100). For a character who has left, the read-only **`eotg_aug_former`** marker.

The law and the court position are **levers on the resource's sources**, not flavor; the events are flavor and each couples (invariant 5, index §1 rule 4):

| Piece | How it couples |
|---|---|
| Augmentation law | Changes the procedure roll (discovered weight, clinic odds), the initiation pulse's weights (how often tier changes begin), and whether discovery and refusal are crimes. Moves nothing directly. |
| Implant Technician | Better roll odds (`eotg_aug_proc_bad_factor`), and **−2 / −3 a year on Overclocked accrual** at average / excellent aptitude (§4.5). |
| act.001 *The Rules of the Field* | a, d move the entrants' risk; desc reads the lead entrant's tier and band. |
| act.002 *Past Spec* | a, d move root's risk; c moves it down at tier 3; desc reads band. |
| act.003 *Foul Play?* | c reads the accused's band in its branch trigger; d moves the accused's risk; desc reads the band. |
| act.004 *A Hum at the Table* | a moves root's risk; desc reads tier. |
| act.005 *Quarry in the Overlay* | a, d, e move root's risk; c moves it down at tier 3; desc reads focus and tier. |
| act.006 *At the Holy Site* | c moves risk down at tier 3; desc reads band. |
| realm.001 *Contraband Hardware* | b changes the subject's tier (removal through the roll); desc reads the subject's tier. |

**Hidden-risk rule** (index §1 rule 3) holds everywhere: no tooltip, toast, law `_effects` text, court-position description or desc quantifies risk, odds or chance. Every risk move is in `hidden_effect`. Vanilla UI numbers that are not the signature resource (tournament score, hunt success, law costs, vassal opinion) are fine.

---

## 3. Identifier table

All keys carry `eotg_`. No landed titles. Loc keys use the dot form for events (index §0, "Loc key form") and the vanilla forms for laws and court positions (`<key>`, `<key>_effects`, `<key>_desc`).

### 3.1 New

| Type | Key | Where | Owner |
|---|---|---|---|
| law group | `eotg_aug_policy_laws` (`default = eotg_aug_policy_tolerate`, `cumulative = no`, `flag = realm_law`, `flag = realm_law_no_number`) | `common/law_groups/eotg_augmentation_law_groups.txt` (**new folder**) | scripter |
| law | `eotg_aug_policy_ban` (index 0) | `common/laws/eotg_augmentation_laws.txt` (**new folder**) | scripter |
| law | `eotg_aug_policy_license` (index 1) | same | scripter |
| law | `eotg_aug_policy_tolerate` (index 2, the default) | same | scripter |
| law | `eotg_aug_policy_favor` (index 3) | same | scripter |
| character variable (timed, 10 years) | `eotg_aug_policy_cooldown` | each law's `on_pass`; read by each law's `can_pass` | scripter |
| scripted trigger | `eotg_aug_under_policy` (param `LAW` = `ban` / `license` / `tolerate` / `favor`): `top_liege ?= { has_realm_law = eotg_aug_policy_$LAW$ }` | `common/scripted_triggers/eotg_augmentation_triggers.txt` | scripter |
| scripted trigger | `eotg_aug_clinic_open` = `NOT = { eotg_aug_under_policy = { LAW = ban } }` | triggers | scripter |
| scripted trigger | `eotg_aug_is_contraband` (param `PROVIDER`): under `ban` (any provider), or under `license` with `PROVIDER = backstreet` | triggers | scripter |
| scripted trigger | `eotg_aug_refusal_is_crime` (param `ACTOR`; recipient scope): `target_is_liege_or_above = $ACTOR$` AND (`eotg_aug_under_policy = { LAW = ban }` OR (`eotg_aug_under_policy = { LAW = license }` AND `has_character_modifier = eotg_mod_illegal_implants`)) | triggers | scripter |
| scripted effect | `eotg_aug_contraband_effect` (patient scope; param `PROVIDER`) | `common/scripted_effects/eotg_augmentation_effects.txt` | scripter |
| opinion modifier | `eotg_opinion_aug_contraband` (−15, 10 years, `imprisonment_reason = yes`, `revoke_title_reason = yes`; the `illegal_resisted_conversion_opinion` shape) | `common/opinion_modifiers/eotg_augmentation_opinions.txt` | scripter |
| opinion modifier | `eotg_opinion_aug_defied_law` (−15, 10 years, `imprisonment_reason = yes`, `revoke_title_reason = yes`; loc "Refused a Lawful Order", lore R2) | opinions | scripter |
| opinion modifier | `eotg_opinion_aug_outlawed` (−20, decaying, `years = 10`) | opinions | scripter |
| opinion modifier | `eotg_opinion_aug_barred` (−15, `years = 5`) | opinions | scripter |
| court position | `eotg_aug_implant_technician_court_position` | `common/court_positions/types/eotg_augmentation_court_positions.txt` (**new folder**) | scripter |
| script value | `eotg_aug_technician_salary_value` (= vanilla `court_position_physician_salary`) | `common/script_values/eotg_augmentation_values.txt` | scripter |
| scripted trigger | `eotg_aug_has_surgeon_access` = `eotg_has_physician_access` OR `employs_court_position = eotg_aug_implant_technician_court_position` OR `eotg_aug_borrowed_technician_valid` | triggers | scripter |
| scripted trigger | `eotg_aug_borrowed_technician_valid`: `var:eotg_aug_borrowed_technician ?= { is_alive = yes  is_imprisoned = no  has_court_position = eotg_aug_implant_technician_court_position  NOT = { has_trait = blind } }` | triggers | scripter |
| scripted trigger | `eotg_aug_surgeon_is_technician` (true when `eotg_aug_save_surgeon_effect` would pick a technician: own or borrowed; used for option name variants) | triggers | scripter |
| scripted trigger | `eotg_aug_tournament_entrant` (character scope; §4.7) | triggers | scripter |
| character interaction | `eotg_aug_borrow_technician_interaction` ("Borrow Their Technician"; the deferred "Lend Your Surgeon", §4.6) | `common/character_interactions/eotg_augmentation_interactions.txt` (the interactions spec's file) | scripter |
| character variable (timed, 1 year) | `eotg_aug_borrowed_technician` → the lent technician | the interaction's `on_accept` | scripter |
| namespace | `eotg_aug_act` | `events/eotg_augmentation_activities.txt` (**new file**) | scripter |
| namespace | `eotg_aug_realm` | `events/eotg_augmentation_realm.txt` (**new file**) | scripter |
| event | `eotg_aug_act.001` *The Rules of the Field* (tournament host) | activities file | scripter |
| event | `eotg_aug_act.002` *Past Spec* (augmented player contestant) | activities file | scripter |
| event | `eotg_aug_act.003` *Foul Play?* (player tournament host) | activities file | scripter |
| event | `eotg_aug_act.004` *A Hum at the Table* (feast) | activities file | scripter |
| event | `eotg_aug_act.005` *Quarry in the Overlay* (hunt) | activities file | scripter |
| event | `eotg_aug_act.006` *At the Holy Site* (pilgrimage) | activities file | scripter |
| event | `eotg_aug_realm.001` *Contraband Hardware* (player liege) | realm file | scripter |
| custom on_action | `eotg_on_tournament_opening_aug` | `common/on_action/eotg_augmentation_on_actions.txt` | scripter |
| custom on_action | `eotg_on_tournament_contest_aug` | on_actions | scripter |
| custom on_action | `eotg_on_tournament_active_aug` | on_actions | scripter |
| custom on_action | `eotg_on_feast_aug` | on_actions | scripter |
| custom on_action | `eotg_on_hunt_aug` | on_actions | scripter |
| custom on_action | `eotg_on_pilgrimage_aug` | on_actions | scripter |
| character flags (cooldowns; **set only in the on_actions / the contraband effect**) | `eotg_flag_aug_act_tournament_cd` (1 year; act.002), `eotg_flag_aug_act_feast_cd` (2 years), `eotg_flag_aug_act_hunt_cd` (2 years), `eotg_flag_aug_act_pilgrimage_cd` (5 years), `eotg_flag_aug_contraband_cd` (on the liege, 1 year) | on_actions; `eotg_aug_contraband_effect` | scripter |
| activity variables (once per activity; **set only in the on_actions**) | `eotg_aug_act_entrants_ruled` (act.001), `eotg_aug_act_accusation_done` (act.003) | on_actions | scripter |
| saved scopes (event-local) | `eotg_aug_entrant`, `eotg_aug_accused`, `eotg_aug_accuser`, `eotg_contraband_subject`, `eotg_lent_technician` | the events and effects above | scripter |
| icons (art) | `gfx/interface/icons/laws/eotg_aug_policy_{ban,license,tolerate,favor}.dds` (the path vanilla derives from the law key: `gfx/interface/icons/laws/crown_authority_1.dds`, read by `[Law.GetIcon]`, `window_my_realm.gui:483`); `gfx/interface/icons/court_position_types/eotg_aug_implant_technician_court_position.dds` (vanilla `…/court_position_types/court_physician_court_position.dds`) | — | **human** (art debt; a stopgap copy of a vanilla icon under the new name is acceptable and is the human's call) |
| interaction icon | placeholder vanilla `learning` (as Examine) | — | human (art debt) |

**Shared opinion modifiers** are system-scoped (`eotg_opinion_aug_*`) per index §1 rule 1. None carries a government prefix.

**Reused, not new:** `eotg_opinion_aug_unease` (−10, timed), `eotg_opinion_aug_admiration`, `eotg_opinion_aug_reassured` (+15), `eotg_opinion_aug_forced_procedure` (interactions), `eotg_opinion_aug_passed_over` (−15); `eotg_mod_illegal_implants`, `eotg_mod_aug_lesson_prowess`, `eotg_mod_aug_lesson_learning`; the nine stress helpers; `eotg_add_fracture_risk`; `eotg_aug_demand_removal_effect` (interactions); `eotg_aug_procedure_effect`. Vanilla: `imprison_character_effect`, `activity_tournament_change_contestant_score_effect`, `hunt_activity_success_change_effect`, `tournament_not_competing` (flag and `tournament_not_competing_tt`), `pay_short_term_gold`, the vassal-stance opinion modifiers.

### 3.2 Amendments to the two unbuilt specs (additive; build them with those specs)

| Spec / piece | Amendment | Why |
|---|---|---|
| procedures `eotg_aug_procedure_roll_effect`, **discovered** entry | Under a Ban (`$PATIENT$ = { eotg_aug_under_policy = { LAW = ban } }`): `modifier = { add = 6  scope:eotg_proc_provider = flag:clinic }`, `modifier = { add = 6  scope:eotg_proc_provider = flag:physician }` (physician covers a technician surgeon), and ×2 for `backstreet`. Under License: backstreet ×1.5. Under Favor: backstreet ×0.5. The existing factor-0 rows (removal, discreet flag, already illegal) still apply after these. | G7: a ban makes all work illegal and raises discovery; licensing makes unlicensed work riskier to hide. Per 200: a back-street job is discovered 10 → 20 (Ban) / 15 (License) / 5 (Favor). |
| procedures `eotg_aug_proc_bad_factor` | (1) **License row:** provider clinic and the patient under License → ×0.8 ("vetted"). (2) **Technician rows**, mutually exclusive, when `scope:eotg_proc_surgeon = { has_court_position = eotg_aug_implant_technician_court_position }`: aptitude ≥ 4 ×0.5; ≥ 3 ×0.6; ≥ 2 ×0.75; else ×0.9 (`aptitude = { court_position = eotg_aug_implant_technician_court_position  value >= N }`). The learning and `lifestyle_physician` rows still apply on top; `min = 0.2` holds. | The reserved extension point (procedures §10: "the place a G10 technician or a G7 licence edict would add a line"). An excellent technician runs at about 2% bad, better than a clinic's 4%: a specialist at your own court. |
| procedures `eotg_aug_procedure_apply_effect`, **discovered** branch | After `eotg_mod_illegal_implants`: `eotg_aug_contraband_effect = { PROVIDER = <from scope:eotg_proc_provider> }` (an if-ladder over the provider flag; §4.3). | Discovery becomes a crime under Ban or License. |
| procedures `eotg_aug_save_surgeon_effect` | New order: (1) own technician (`employs_court_position = eotg_aug_implant_technician_court_position`; the holder is not blind) → `court_position:eotg_aug_implant_technician_court_position`; (2) a valid borrowed technician → `var:eotg_aug_borrowed_technician`; (3) own court physician (unchanged); (4) the patient (unchanged fallback). | One place decides who operates. |
| procedures script value `eotg_aug_price_mult_physician` | Becomes conditional in the payer's scope: `0.6` when the payer employs a technician, otherwise `0.75`. A borrowed technician pays the lending fee instead (§4.6) and stays at `0.75`. | "Cheaper maintenance" for procedures on the physician route. |
| procedures: every **clinic-provider option at a provider-choice point** (init.018.a; tier1.002 a, d, e; tier2.003 a, c, d; proc.001 a, f; proc.003 a, f) | `trigger` gains `eotg_aug_clinic_open = yes`; `show_as_unavailable = { eotg_aug_clinic_open = no }` with the tooltip `eotg_aug_clinic_closed_tt` (vanilla shape `tournament_events.txt:4496`). | Under a Ban the sanctioned clinics are closed; the choice is your own people or the back streets. |
| procedures: every **physician-provider option** (init.018.c; tier1.002.f; tier2.003.f; proc.001.b; proc.003.b) | Its `eotg_has_physician_access` test becomes `eotg_aug_has_surgeon_access`. It gains a second name: `name = { trigger = { eotg_aug_surgeon_is_technician = yes }  text = eotg_aug_opt_technician }`, the plain name otherwise. | The technician (own or borrowed) is offered wherever the physician is. |
| interactions: Offer / Demand / Salvage **physician send option**; Examine `is_available`; tamper.004.b; int.001 | `eotg_has_physician_access` → `eotg_aug_has_surgeon_access` (actor scope where it was actor scope). | As above. |
| interactions: Offer / Demand **clinic send option**; tamper.004.a | `is_valid` / `trigger` gains `scope:recipient = { eotg_aug_clinic_open = yes }` (tamper.004.a: root). | The patient's realm decides (LAW AT 866: "settled under the law of the realm where it is pressed"). |
| interactions: **Demand Removal** | (1) `desc` gains `triggered_desc = { trigger = { scope:recipient = { eotg_aug_refusal_is_crime = { ACTOR = scope:actor } } }  desc = eotg_aug_demand_removal_crime_desc }` (`00_religious_interactions.txt:160-180` shape). (2) `ai_accept` gains `modifier = { add = 50  desc = EOTG_AUG_AI_REFUSAL_IS_CRIME  scope:recipient = { eotg_aug_refusal_is_crime = { ACTOR = scope:actor } } }` (`00_religion_scripted_modifiers.txt:262-275`). (3) `on_decline` becomes an if/else: **if** the refusal is a crime, `scope:recipient = { reverse_add_opinion = { target = scope:actor  modifier = eotg_opinion_aug_defied_law  years = 10 } }` and the actor toast `eotg_aug_demand_crime_toast`; **else** the existing `eotg_opinion_aug_demanded_removal` line (`00_religious_interactions.txt:640-672`). (4) `ai_will_do` gains +30 when `scope:actor = { eotg_aug_under_policy = { LAW = ban } }`. | The interactions spec's deferred "refusal as a crime" (its §4.2 and §10). |
| interactions: **Offer Augmentation** | `ai_accept`: recipient under Ban −25 (`EOTG_AUG_AI_BANNED`), under Favor +15 (`EOTG_AUG_AI_FAVORED`). `ai_will_do`: `factor = 0.25` when the actor is under Ban. | The realm's law shapes willingness. |
| procedures DoD item 5 and interactions DoD item 4 | Read "none of maimed / one_eyed / blind / death / discovered … except **discovered under a Ban**". The severe tail stays back-street only. | Consistency with the first row. |

### 3.3 Changed (existing, built script; key kept)

| Key | Change | § |
|---|---|---|
| `eotg_on_yearly_aug_initiation_check` | Policy weights on the existing `random_list`, for the pulsing ruler (`root`): **Ban:** nothing entry ×2; the corporate offer (init.002) ×0; the Physician's Proposal (init.017) ×0.5; back-alley (init.010) ×1.5. **License:** back-alley ×0.5. **Favor:** nothing entry ×0.8. All as `modifier = { factor = N  eotg_aug_under_policy = { LAW = … } }`. | 4.2 |
| `eotg_on_yearly_aug_overclocked_check` | One accrual row after the vendor rows: `employs_court_position = eotg_aug_implant_technician_court_position` → −2, or −3 at aptitude ≥ 4 (in `hidden_effect` via `eotg_add_fracture_risk`, as the others). | 4.5 |
| `eotg_decision_maintenance_protocol` | `cost`: ×0.5 when employing a technician (in place of the physician's ×0.75). Overclocked risk drop: −12 with a technician, else −8. Its `selection_tooltip` text is unchanged (it does not quantify). | 4.5 |
| `eotg_decision_seek_augmentation` | `ai_will_do`: `modifier = { factor = 0.5  eotg_aug_under_policy = { LAW = ban } }`. | 4.2 |
| `on_action` header comment | Cooldown list gains the five flags and two activity variables from §3.1. | — |

---

## 4. Wiring

### 4.1 G7: the Augmentation law group

**Why a realm law** (and not a decision setting a flag or modifier, the gaps doc's sketch): vanilla expresses realm-wide policy as a law group (crown authority, camp purpose, mandala decree). A law brings, for free, the My Realm window, inheritance by the heir, a native cost and cooldown, an AI enactment hook (`ai_will_do`), and native vassal opinion through stance modifiers that show in every opinion breakdown. A decision would rebuild all of that by hand and still not appear where players look for laws.

**Group** (`common/law_groups/eotg_augmentation_law_groups.txt`; shape `00_realm_law_groups.txt:22-27, 70-76`):
```
eotg_aug_policy_laws = {
    default = eotg_aug_policy_tolerate
    cumulative = no
    flag = realm_law
    flag = realm_law_no_number
    can_change_law_group = {
        custom_tooltip = {
            text = eotg_aug_policy_set_by_liege_tt
            is_independent_ruler = yes
        }
    }
}
```
No `required_government_flag`: every government can hold it (map-agnostic; the mod's governments are not designed yet).

**Who is governed.** Each character lives under the law held by their **top liege** (`eotg_aug_under_policy`). An independent ruler governs themself. A vassal sees the group locked ("set by your liege"). A courtier, knight or spouse follows their employer's top liege. A character outside any realm is under no law, which reads as Tolerate. This is "realm-local, no higher authority": the top of each realm sets it, and nothing sits above that.

**The four laws** (`common/laws/eotg_augmentation_laws.txt`):

| | `eotg_aug_policy_ban` | `eotg_aug_policy_license` | `eotg_aug_policy_tolerate` (default) | `eotg_aug_policy_favor` |
|---|---|---|---|---|
| Fiction | Augmentation is prohibited in the realm. | Implant work must be done by sanctioned hands. | The ruler does not legislate it. Today's world. | The ruler openly favors the augmented at court. **No gold, no clinics, no programme** (§8). |
| `modifier` (vassal stances) | `zealot_opinion = 15`, `parochial_opinion = 5`, `glory_hound_opinion = -10`, `belligerent_opinion = -5` | `parochial_opinion = 5`, `courtly_opinion = 5`, `glory_hound_opinion = -5` | none | `glory_hound_opinion = 10`, `belligerent_opinion = 5`, `zealot_opinion = -15`, `parochial_opinion = -5` |
| `can_keep` | `is_independent_ruler = yes` | same | — (the default) | same |
| `can_pass` | `custom_description = { text = eotg_aug_policy_cooldown_tt  NOT = { has_variable = eotg_aug_policy_cooldown } }` | same | same | same |
| `pass_cost` | `prestige = major_prestige_value` | `prestige = medium_prestige_value` | `prestige = minor_prestige_value` | `prestige = medium_prestige_value` |
| `on_pass` | cooldown var 10 years; **every direct vassal and courtier with `eotg_is_augmented_any = yes`** gets `add_opinion = { modifier = eotg_opinion_aug_outlawed  target = root }` | cooldown | cooldown | cooldown |
| Procedure roll (§3.2) | clinics closed at choice points; discovered: clinic +6, physician +6, back streets ×2; discovery is a crime | clinic bad ×0.8; back-street discovered ×1.5; back-street discovery is a crime | unchanged | back-street discovered ×0.5 |
| Refusing Demand Removal | a crime | a crime only for someone holding `eotg_mod_illegal_implants` | not a crime | not a crime |
| Initiation pulse (§3.3) | nothing ×2, corporate ×0, physician's proposal ×0.5, back-alley ×1.5 | back-alley ×0.5 | unchanged | nothing ×0.8 |
| Implant Technician (§4.5) | not available to anyone governed, except the lawmaker | available | available only to augmented rulers | available |

**Stance mapping** (why these stances): the zealot stance is scored by `zealous` +100 and `cynical` −50 (`00_vassal_stances.txt:510-560`), so "zealots approve a ban" is "zealous vassals approve" without naming a faith. Glory hound and belligerent are scored by `ambitious` (+50 each, `:172`, `:996`): the gaps doc's "ambitious approve encouragement". Parochial (`content` +50, `:334`) likes order. Magnitudes sit inside crown authority's range (−30…+20, `00_realm_laws.txt:24-30, 133-141`).

**`ai_will_do`** (shape `00_realm_laws.txt:2576-2578, 2628-2645`; the cooldown stops churn, and heirs inherit, so a cynical heir of a zealous banner reverts):

| Law | Score |
|---|---|
| ban | 0, unless all of: NOT already held, `eotg_is_augmented_any = no`, `has_trait = zealous` → 10; +5 if `any_vassal = { count >= 3  eotg_is_augmented_any = yes }`; ×0 if `cynical` |
| license | 0, unless NOT held, NOT `zealous`, `OR = { has_trait = diligent  has_trait = just }`, `OR = { eotg_is_augmented_any = yes  any_vassal = { count >= 2  eotg_is_augmented_any = yes } }` → 5 |
| favor | 0, unless NOT held, NOT `zealous`, `eotg_is_augmented_any = yes`, `OR = { has_trait = ambitious  has_trait = cynical }` → 5 |
| tolerate | 10 if holding ban and `OR = { eotg_is_augmented_any = yes  has_trait = cynical }`; 10 if holding favor and `OR = { has_trait = zealous  eotg_is_augmented_any = no }`; 3 if holding license and `NOR = { has_trait = diligent  has_trait = just }`; else 0 |

**Law `_effects` loc** lists the behaviour in words, with no numbers about risk or odds: "Sanctioned clinics will not operate", "Unsanctioned implant work is a crime", "Refusing an order to remove implants is a crime". Vanilla uses `<law>_effects` for exactly this (`localization/english/laws_l_english.yml:83-89`).

### 4.2 G7: what the law does to procedures and offers

**Does a ban make back streets the only option?** Nearly. Under a Ban:
- **Sanctioned clinics close.** Every clinic option at a provider-choice point is shown unavailable with `eotg_aug_clinic_closed_tt` (§3.2). What is left is **your own people** (a physician or technician at your court) **or the back streets**.
- **All work is illegal.** Your own physician's work carries a discovery chance (+6 per 200, 3%) where it had none. Back-street discovery doubles (5% → 10%).
- **Install offers that arrive as events** (the wound offer, the aging offer, the Prosthetic, and the rest mapped to "clinic" in procedures §4.5) keep their fiction: someone is breaking the law to make you the offer. They roll as clinic, so under a Ban they also carry the +6 discovered weight. The corporate offer (init.002) does not come at all under a Ban (§3.3).

**Discovery as a crime: `eotg_aug_contraband_effect = { PROVIDER }`** (patient scope; called from the apply effect's discovered branch):
```
if = {
    limit = {
        eotg_aug_is_contraband = { PROVIDER = $PROVIDER$ }
        is_independent_ruler = no
        exists = liege
    }
    save_scope_as = eotg_contraband_subject
    reverse_add_opinion = { target = liege  modifier = eotg_opinion_aug_contraband }     # the liege gains the imprisonment reason
    liege = {
        if = {
            limit = { is_ai = no  NOT = { has_character_flag = eotg_flag_aug_contraband_cd } }
            add_character_flag = { flag = eotg_flag_aug_contraband_cd  years = 1 }       # cooldown authority: here only
            trigger_event = { id = eotg_aug_realm.001  days = { 3 10 } }
        }
    }
}
```
- The **direct liege** holds the reason, because the direct liege is who can imprison (vanilla's imprison interaction targets vassals and courtiers). The **top liege** sets the law. Both are the same realm.
- An AI liege simply holds a lawful reason to imprison, which vanilla AI already acts on. A player liege gets realm.001.
- The lawmaker (independent) is never a criminal under their own law: no one sits above them.
- init.004 (Desperation) applies `eotg_mod_illegal_implants` directly, outside the roll, so it raises no crime. That is accepted: the desperation install happens in the field, and nobody sees it.

### 4.3 G7: refusal as a crime (Demand Removal)

Specified in §3.2 (Demand Removal row), following vanilla's conversion demand exactly:
- **The trigger** `eotg_aug_refusal_is_crime = { ACTOR }`: the actor is the recipient's liege or above, and the recipient's realm bans augmentation, or licenses it and the recipient's hardware is unlicensed (`eotg_mod_illegal_implants`).
- **The desc** warns the player before sending.
- **The AI** gets +50 to accept when refusing is a crime.
- **On decline** the actor gains `eotg_opinion_aug_defied_law` ("Refused a Lawful Order") toward the refuser, with `imprisonment_reason` and `revoke_title_reason`: the liege may now lawfully arrest them or revoke a title. No event is needed. The vanilla imprison and revoke interactions do the rest.

### 4.4 realm.001 *Contraband Hardware*

- **Fired by:** `eotg_aug_contraband_effect`, to a player liege. 3–10 days.
- **Trigger** (world guard): `scope:eotg_contraband_subject ?= { is_alive = yes  is_imprisoned = no }`.
- **Portraits:** left root; right `scope:eotg_contraband_subject`.
- **Desc:**
  - base: word has reached you that `[eotg_contraband_subject.GetName]` has had implant work done in your realm, outside the law;
  - `desc_ban` or `desc_license` by root's governing law, each in two variants (lore R1): a `first_valid` on root `is_independent_ruler = yes` → `desc_ban` / `desc_license` ("Your law …"), else `desc_ban_v` / `desc_license_v` ("The law of your realm …");
  - a tier line on the subject (`desc_aug` / `_enh` / `_oc` / `_nf`): what was found;
  - `desc_courtier` when the subject is a courtier of root (they live under your roof).

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "Arrest them." | — | `imprison_character_effect = { TARGET = scope:eotg_contraband_subject  IMPRISONER = root }` (the opinion is the lawful reason) | 30; +20 just; +20 zealous; −20 compassionate |
| b | "Have it taken out." | subject `is_courtier_of = root`, NOT landed, `eotg_is_augmented_any = yes`, NOT Seamless; afford the removal at the provider below | `eotg_aug_demand_removal_effect = { PROVIDER = physician }` with a surgeon (`eotg_aug_has_surgeon_access`), else `{ PROVIDER = backstreet }`, run with `scope:actor` = root and `scope:recipient` = the subject (save both before the call); the subject gains `eotg_opinion_aug_forced_procedure`; root runs `eotg_aug_stress_tyranny_effect`. **Changes the subject's tier.** | 30; +20 zealous; +10 arbitrary; −20 compassionate |
| c | "A fine will do." | subject `gold >= minor_gold_value` | the subject `pay_short_term_gold = { target = root  gold = minor_gold_value }`; root `remove_opinion = { target = scope:eotg_contraband_subject  modifier = eotg_opinion_aug_contraband }` | 30; +20 greedy; +10 just |
| d | "Look the other way." | — | root `remove_opinion` as c; `eotg_aug_stress_lie_effect = yes` (root breaks its own law) | 20; +20 cynical; +10 lazy; −20 zealous |
| e [just] | "The realm's law holds, for everyone." | `has_trait = just` | as a, plus `add_prestige = minor_prestige_value` | 30; +30 just; +10 diligent |
| f [greedy] | "A fine. A large one." | `has_trait = greedy`; subject `gold >= medium_gold_value` | as c at `medium_gold_value`, plus the subject `add_opinion = { modifier = eotg_opinion_aug_unease  target = root  years = 5 }` | 30; +30 greedy; +10 arbitrary |

- Option b uses the interactions spec's removal effect and therefore its roll. Because a liege ordering the surgery on a household member is the "forced" case, the forced-procedure opinion applies.
- The tier line in the desc reads the subject's tier, and b changes it (coupling).
- An imprisoned subject can then be Salvaged (interactions §4.5). That is an existing lever, not new content.

### 4.5 G10: the Implant Technician

**`eotg_aug_implant_technician_court_position`** (`common/court_positions/types/eotg_augmentation_court_positions.txt`). Shape: `court_physician_court_position` (`00_court_positions.txt:41-562`) for the aptitude, salary and AI, and `court_artificer_court_position` (`:10896-11193`) for the received/revoked/vacated effects. **No DLC gate** (the physician has none; lesson 12).

| Field | Value |
|---|---|
| `sort_order` / `max_available_positions` / `skill` | 398 (just below the physician's 399) / 1 / `learning` |
| `court_position_asset` | one default: `animation = physician`, `background = "gfx/interface/illustrations/event_scenes/study_physician.dds"` (vanilla default asset, `:115-118`) |
| `opinion` | `regular_court_position_opinion` |
| `aptitude_level_breakpoints` | `{ 20 40 60 80 }` |
| `aptitude` | `value = 1`; learning ×1.5, max 45 (desc `court_position_skill_learning`); `lifestyle_physician` +15 / +30 / +45 by XP 0 / 50 / 100 (vanilla descs `court_position_physician_1/2/3_trait`, `:137-162`); `eotg_is_augmented_any = yes` +15 (desc `eotg_aug_technician_aptitude_augmented`: knows the hardware from the inside); `has_variable = eotg_aug_former` +5 (desc `eotg_aug_technician_aptitude_former`); education_learning +4…+20 (`:207-232` shape); `blind` −50 (`court_position_blind_trait`); `add = court_position_aptitude_low_penalty_value`, `add = general_aptitude_bonus` |
| `is_shown` | the physician's AI barony gate (`:336-344`); then `OR = { eotg_is_augmented_any = yes  eotg_aug_under_policy = { LAW = license }  eotg_aug_under_policy = { LAW = favor }  employs_court_position = eotg_aug_implant_technician_court_position }` (the gaps doc: "rulers with the trait or a licence edict"; Favor added) |
| `valid_position` | `custom_tooltip = { text = eotg_aug_technician_banned_tt  OR = { NOT = { eotg_aug_under_policy = { LAW = ban } }  is_independent_ruler = yes } }`. Under a Ban the position invalidates for everyone but the lawmaker, and vanilla's invalidation handles the holder. |
| `is_shown_character` | `scope:employee = { court_position_employee_shown_trigger = yes }` |
| `valid_character` | `scope:employee = { base_court_position_validity_trigger = { EMPLOYER = scope:liege }  is_adult = yes  is_landed = no  OR = { learning >= 8  has_trait = lifestyle_physician  eotg_is_augmented_any = yes } }` (`court_physician_validity_trigger` shape, `00_court_position_triggers.txt:494-497`). The same person may hold both physician and technician. |
| `revoke_cost` | `prestige = minor_court_position_prestige_revoke_cost` |
| `salary` / `received_salary` | the physician's gold/treasury split (`:379-411`) on `eotg_aug_technician_salary_value` |
| `scaling_employer_modifiers` | **none** (0 levels is allowed). The employer benefits are script-read from aptitude (below), not a modifier, so the position never helps an unaugmented employer and never needs a risk number in a tooltip. |
| `custom_employer_modifier_description` | `eotg_aug_implant_technician_employer_desc`: "Operates on you and those in your care, more safely and more cheaply than a physician. Services your implants, and keeps overclocked hardware running cooler." No numbers. |
| `modifier` (employee) | `monthly_learning_lifestyle_xp_gain_mult = 0.1` (artificer precedent, `:11136-11139`) |
| `on_court_position_received` / `_revoked` / `_invalidated` | `basic_gained_court_position_effect` / `basic_revoked_court_position_effect` / `basic_invalidated_court_position_effect` |
| `on_court_position_vacated` | `court_position_vacated_event_effect = { COURT_POSITION_TYPE = eotg_aug_implant_technician_court_position }` |
| `ai_position_score` | `value = -50`; +200 if `scope:liege` is tier 2, tier 3 or Neurofractured; +120 if tier 1; +50 if `scope:liege = { any_knight = { count >= 2  eotg_is_augmented_any = yes } }`; `add = court_position_debt_considerations_value`. An unaugmented liege scores −50 and never hires (hire > 0). |
| `ai_candidate_score` | `value = 50`; `add = court_position_candidate_score_base_value`; `add = court_position_candidate_aptitude_value` (the artificer's set, `:11179-11192`, without its role-specific petition line) |

**What the technician does** (all script-read; no new modifier):

| Lever | Where | Size |
|---|---|---|
| **Better procedure odds** | `eotg_aug_save_surgeon_effect` picks the technician first; `eotg_aug_proc_bad_factor`'s technician rows (§3.2) | ×0.9 → ×0.5 bad by aptitude, on top of the learning rows |
| **Cheaper procedures** | `eotg_aug_price_mult_physician` = 0.6 with a technician (§3.2) | 0.75 → 0.6 |
| **Cheaper maintenance** | `eotg_decision_maintenance_protocol` (§3.3) | cost ×0.5; Overclocked risk drop −12 instead of −8 |
| **Hardware runs cooler** | `eotg_on_yearly_aug_overclocked_check` (§3.3) | −2 a year (aptitude ≥ 4: −3), like the safe-vendor −3 |
| **Offered wherever a physician is** | `eotg_aug_has_surgeon_access` in the provider options and send options (§3.2), with the name variant "My implant technician." | — |

**Why the `SURGEON` parameter and not a new `PROVIDER`.** A fourth provider column would duplicate the physician column and complicate the procedures DoD ("the severe tail only in the back streets"). As a surgeon under `PROVIDER = physician`, the technician inherits that column's zero severe tail and improves it through the one factor the roll already has. The odds stay in one place (procedures goal 4).

**Not changed:** the T5 uses of `eotg_has_physician_access` in built content (init.006–.008, tier1.013–.015, `eotg_decision_consult_physician`, Excision). A technician is a surgeon, not a physician. Folding it into T5 would rewrite many built options for little gain (§10).

### 4.6 G10: Borrow Their Technician (`eotg_aug_borrow_technician_interaction`)

The interactions spec deferred this because "borrowing another court's physician needs a cross-court surgeon scope that G10 would define once". G10 defines it: `var:eotg_aug_borrowed_technician`, read by `eotg_aug_save_surgeon_effect` (§3.2).

The **actor borrows**; the recipient lends. One interaction serves both directions: the AI can ask the player for theirs.

| Field | Value |
|---|---|
| `category` / `icon` | `interaction_category_friendly` / `learning` (placeholder) |
| `desc` / `notification_text` | `eotg_aug_borrow_technician_interaction_desc` / `_notification` |
| `is_shown` | `scope:recipient != scope:actor`; `scope:recipient = { employs_court_position = eotg_aug_implant_technician_court_position }`; `scope:actor = { eotg_is_augmented_any = yes  NOT = { employs_court_position = eotg_aug_implant_technician_court_position } }`; relation `OR = { scope:actor = { is_allied_to = scope:recipient }  scope:actor = { is_vassal_of = scope:recipient }  scope:recipient = { is_vassal_of = scope:actor }  scope:actor = { is_close_family_of = scope:recipient }  scope:actor = { is_spouse_of = scope:recipient }  scope:actor = { has_relation_friend = scope:recipient } }` |
| `is_valid_showing_failures_only` | the actor has no valid borrowed technician; `scope:actor.short_term_gold >= minor_gold_value`; the lender's technician is not imprisoned and not blind; NOT `scope:actor = { is_at_war_with = scope:recipient }`; the **actor** is not under a Ban (`scope:actor = { eotg_aug_clinic_open = yes }`: the work would happen in the actor's realm) |
| `cooldown_against_recipient` | `{ years = 3 }` |
| `ai_min_reply_days` / `ai_max_reply_days` | 1 / 5 |
| `on_accept` | `scope:actor = { pay_short_term_gold = { target = scope:recipient  gold = minor_gold_value } }`; `scope:recipient.court_position:eotg_aug_implant_technician_court_position = { save_scope_as = eotg_lent_technician }`; `scope:actor = { set_variable = { name = eotg_aug_borrowed_technician  value = scope:eotg_lent_technician  years = 1 } }`; actor toast `eotg_aug_borrow_accepted_toast` |
| `on_decline` | actor toast `eotg_aug_borrow_declined_toast`. No opinion: it was a request. |

**The technician does not move** (lore R8): only the variable is set; no travel, no change of court. Loc says "will see to your implants for a year".

**Effect for a year:** the actor counts as having surgeon access (`eotg_aug_has_surgeon_access`). Every physician-route option in procedures, repairs, removals, Offer, Demand and Examine uses the lent technician as `SURGEON`, with the technician's aptitude rows, at the ordinary physician price (0.75; the actor already paid the fee).

**`ai_accept`** (lender's view):

| Modifier | add | desc key |
|---|---|---|
| base | 10 | |
| opinion ×0.5 | ± | `AI_OPINION_REASON` (vanilla) |
| allied | +20 | `EOTG_AUG_AI_ALLIED` |
| the actor is the lender's liege | +25 | `EOTG_AUG_AI_LIEGE` (interactions) |
| close family or spouse | +15 | `EOTG_AUG_AI_FAMILY` |
| greedy / generous | +15 / +10 | `EOTG_AUG_AI_GREEDY` (interactions) / `EOTG_AUG_AI_GENEROUS` |
| paranoid | −20 | `EOTG_AUG_AI_PARANOID` (interactions) |
| the lender is tier 3 or Neurofractured | −30 | `EOTG_AUG_AI_NEEDS_TECHNICIAN` |

**AI sending:** `ai_targets` allies, family (`max = 5`), liege, vassals (`max = 10`); `ai_frequency_by_tier` 0 / 0 / 48 / 36 / 36 / 36; `ai_will_do` base 0, +40 actor tier 3 or Neurofractured, +20 actor holds infection, Fragments or `eotg_mod_aug_tampered`, +20 actor has `eotg_aug_repair_injury`, `factor = 0.5` if the actor already has physician access, `factor = 0` if the actor cannot afford it.

### 4.7 G6: activity hooks

All hooks are extended **additively** (invariant 4): the mod file names the vanilla on_action with only `on_actions = { eotg_… }`. The mod already does this for `yearly_playable_pulse`, `on_death` and others. The vanilla on_action's own `trigger` still gates the whole block, ours included. **Cooldown authority lives in the custom on_action** (flags on the character, or variables on `scope:activity`, the vanilla once-per-activity marker shape at `feast_on_actions.txt:20-24`). No event `trigger` reads them.

**On stacking:** a child on_action can fire an event on the same tick as the vanilla parent's own random event. Vanilla does this itself (`tournament_passive_state_guest_pulse` has both `random_events` and `events`, `ep2_tournament_on_actions.txt:6-19`). Our children are once per activity or per 1–5 years, so a double event is rare. **Not** used: appending `random_events` to a vanilla pool. The project convention is `on_actions` children, and whether appended random_events merge into one pool is not settled by vanilla.

| Vanilla hook (file:line) | Root / scopes when it fires | Custom on_action | Gate (in the custom on_action) | Fires |
|---|---|---|---|---|
| `tournament_opening_on_action` (`ep2_tournament_on_actions.txt:699`; fired on `scope:host` 20 days into the tournament, `activity_types/tournament.txt:5617-5622`) | host; `involved_activity` | `eotg_on_tournament_opening_aug` | `involved_activity.activity_host ?= this` (`hunt_on_actions.txt:5-8` shape); `involved_activity = { NOT = { has_variable = eotg_aug_act_entrants_ruled }  any_attending_character = { eotg_aug_tournament_entrant = yes } }` | sets the activity variable; act.001 in 1–3 days. **AI hosts included**, so a player's augmented entry can be barred by an AI host (§4.8). |
| `contest_ongoing_event_melee_random_pulse` `:82`, `contest_ongoing_event_archery_random_pulse` `:140`, `contest_bout_joust_random_pulse` `:213`, `contest_bout_wrestling_random_pulse` `:244`, `contest_bout_duel_random_pulse` `:282`, `contest_bout_board_game_random_pulse` `:316`, `contest_ongoing_event_horse_race_random_pulse` `:349` (fired only for player contestants, `04_dlc_ep2_tournament_effects.txt:1994-2018`, `:599-603`) | player contestant; `involved_activity` | `eotg_on_tournament_contest_aug` (one custom on_action, seven parents) | `is_ai = no`; `activity_is_competing_trigger = yes`; `eotg_is_augmented_any = yes`; NOT Seamless; NOT `eotg_flag_aug_act_tournament_cd` | `random = { chance = 40  … }` sets the flag (1 year) and fires act.002 in 1 day. **Recital is excluded**: an overlay does not sing. |
| `tournament_active_state_pulse` (`:28`; `on_active_state_pulse`, character scope, `tournament.txt:6197-6199`) | each attendee; `scope:activity` | `eotg_on_tournament_active_aug` | `is_ai = no`; `scope:activity.activity_host = this`; `scope:activity = { NOT = { has_variable = eotg_aug_act_accusation_done } }`; at least one competing contestant who is augmented and not root, and one other competing contestant | `random = { chance = 25 … }` sets the activity variable; act.003 in 1–5 days |
| `feast_default_event_selection` (`feast_on_actions.txt:50`; guests weekly, hosts through the tombola, `:38-48`; `activity_types/feast.txt:4542-4552`) | ruler; `scope:activity` | `eotg_on_feast_aug` | `is_ai = no`; `exists = scope:activity`; `eotg_is_augmented_any = yes`; NOT Seamless; NOT `eotg_flag_aug_act_feast_cd` | `random = { chance = 35 … }` sets the flag (2 years); act.004 |
| `hunt_random_pulse` (`hunt_on_actions.txt:17`; days 7 and 14 for each player participant, `activity_types/hunt.txt:5030-5043`) | participant; `scope:activity`, `scope:host` | `eotg_on_hunt_aug` | `is_ai = no`; `eotg_is_augmented_any = yes`; NOT Seamless; NOT `eotg_flag_aug_act_hunt_cd` | `random = { chance = 50 … }` sets the flag (2 years); act.005 |
| `pilgrimage_destination_events` (`pilgrimage_on_actions.txt:380`; at the destination, `activity_types/pilgrimage.txt:2536-2540`) | pilgrim; `scope:activity` | `eotg_on_pilgrimage_aug` | `is_ai = no`; `eotg_is_augmented_any = yes`; NOT Seamless; NOT `eotg_flag_aug_act_pilgrimage_cd` | `random = { chance = 50 … }` sets the flag (5 years); act.006 |

**`eotg_aug_tournament_entrant`** (§3.1; character scope): `is_in_guest_subset = { name = contestant }`, `activity_is_valid_tournament_contestant = yes`, `eotg_is_augmented_any = yes`, NOT `eotg_total_integration` (`04_ep2_tournament_triggers.txt:21-37`).

**Why act.004–.006 are player-only:** their outcomes for an AI are a few points of hidden risk, which is noise against HQ2, and the pulses fire for every ruler at every feast. act.001 is the exception, because its outcome (barring) reaches player entrants.

**Event type and look:** `type = activity_event`, `window = widget_activity_locale_fullscreen_event` for the tournament ones (as `ep2_tournament_events.txt` 0021), themes `tournament_contest` (act.002), `tournament_grounds` (act.001, .003), `feast_activity` (act.004), `hunt_activity` (act.005), `pilgrimage_destination` (act.006) (`common/event_themes/`).

### 4.8 G6: the six activity events

Index §1 rule 6 applies: three universal options plus 1–2 trait-gated ones, every `ai_chance` with ≥ 2 trait modifiers, morally loaded options use a stress helper. **No option writes its own `stress_impact` line for impatient, gluttonous, temperate or fickle** (trait-depth §5.2). Risk moves are in `hidden_effect`. Tournament loc avoids horses and lances (index §5.6): "the arena", "the bout", "the field".

#### act.001 *The Rules of the Field* (tournament host)
- **Trigger:** `exists = scope:activity`; `involved_activity = { any_attending_character = { eotg_aug_tournament_entrant = yes } }`.
- **Immediate:** `involved_activity = { random_attending_character = { limit = { eotg_aug_tournament_entrant = yes }  weight = { base = 1  modifier = { add = 2  eotg_is_aug_tier3 = yes } }  save_scope_as = eotg_aug_entrant } }`. A chosen target (index rule 7 note), named in loc.
- **Desc:** base (the marshals have a question: some entrants carry hardware, and the rules of the field never imagined it); `desc_many` when two or more entrants qualify; `desc_entrant_oc` / `_nf` on `scope:eotg_aug_entrant` (reads tier); `desc_ban` when root is under a Ban: `desc_ban` if root `is_independent_ruler = yes` ("Your law …"), else `desc_ban_v` ("The law of your realm …"; lore R1).
- **"All entrants"** below means `involved_activity = { every_attending_character = { limit = { eotg_aug_tournament_entrant = yes } … } }`.

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "Let them compete." | — | all entrants: hidden risk +3 (they will run hot); `scope:eotg_aug_entrant` `add_opinion = { modifier = eotg_opinion_aug_admiration  target = root }`; every **zealous** attendee: `add_opinion = { modifier = eotg_opinion_aug_unease  target = root  years = 5 }`. Under a Ban: `eotg_aug_stress_lie_effect`. | 30; +20 cynical; +10 just; −20 zealous |
| b | "Bar them from the field." | — | all entrants: `add_character_flag = tournament_not_competing`, `custom_tooltip = tournament_not_competing_tt`, `involved_activity = { remove_from_guest_subset = { name = contestant  target = prev } }` (scripter: save the entrant as a scope first; vanilla `tournament_events.txt:9315-9323`), `add_opinion = { modifier = eotg_opinion_aug_barred  target = root }`; player entrants get the toast `eotg_aug_act.001.barred_toast` | 30; +20 zealous; +10 just; −10 cynical |
| c | "No powered output on the field." | — | all entrants: `activity_tournament_change_contestant_score_effect = { SCORE = decrease_minor }` (a handicap; the effect is a no-op for anyone not competing) | 30; +20 diligent; +10 content |
| d [cynical] | "Make them the main event." | `has_trait = cynical` | all entrants: hidden risk +5; root `add_prestige = minor_prestige_value`; zealous attendees as a | 30; +30 cynical; +10 arrogant |
| e [zealous] | "No one fights with hardware on my field." | `has_trait = zealous` | as b, plus `add_piety = minor_piety_value` | 30; +30 zealous; +10 stubborn |

**Coupling:** a and d move risk; the desc reads the entrant's tier.

#### act.002 *Past Spec* (augmented player contestant)
- **Trigger:** `activity_is_competing_trigger = yes`; `eotg_is_augmented_any = yes`; NOT Seamless.
- **Desc:** base (the hardware could give more than the field's rules expect); `desc_board` when `involved_activity = { has_current_phase = tournament_phase_board_game }` (the overlay is already three moves ahead; scripter confirms the phase key in `tournament.txt`), else `desc_physical`; `desc_hot` when tier 3 / Neurofractured or `eotg_aug_pressure_flicker = no` (reads band); `desc_ban` when the host is under a Ban.

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "Run it past spec." | — | `activity_tournament_change_contestant_score_effect = { SCORE = increase_major }`; hidden risk +4 (tier 3: +6; Neurofractured: +8); `random = { chance = 25  … }`: someone saw it: `involved_activity.activity_host = { add_opinion = { modifier = eotg_opinion_aug_unease  target = root  years = 5 } }`, `add_prestige = { value = minor_prestige_value  multiply = -1 }`, toast `eotg_aug_act.002.a.seen`; `eotg_aug_stress_embrace_effect` | 30; +20 ambitious; +20 arrogant; −20 craven |
| b | "Within the rules." | — | `SCORE = increase_minor` | 30; +20 just; +10 honest |
| c | "Throttle it down." | — | `SCORE = decrease_minor`; `add_prestige = minor_prestige_value`; tier 3: hidden risk −3 | 30; +20 humble; +10 content |
| d [deceitful] | "Let them think it's skill." | `has_trait = deceitful` | `SCORE = increase_medium`; hidden risk +3; no discovery roll | 30; +30 deceitful; +10 ambitious |
| e [honest] | "Declare the hardware to the marshal." | `has_trait = honest` | `involved_activity.activity_host = { add_opinion = { modifier = eotg_opinion_aug_admiration  target = root } }`; `add_prestige = minor_prestige_value` | 30; +30 honest; +10 just |

**Coupling:** a and d move risk; c moves it down at tier 3; the desc reads the band. This is the "rigged contest" beat, and its option a carries the "accused of cheating" risk for a player who is the one augmented.

#### act.003 *Foul Play?* (player tournament host)
- **Trigger:** `exists = scope:activity`; `scope:activity.activity_host = root`; the accused and accuser exist (mirror the on_action).
- **Immediate:** save `eotg_aug_accused` (a competing augmented contestant, not root; weight +2 at tier 3) and `eotg_aug_accuser` (a competing contestant, not root and not the accused; weight +5 if `has_relation_rival = scope:eotg_aug_accused`). Both are chosen targets, named in loc.
- **Desc:** base (`[eotg_aug_accuser.GetName]` claims `[eotg_aug_accused.GetName]` fights with hardware, not skill); `desc_hot` when the accused is tier 3 / NF or past the Flicker band (reads band); `desc_ban` / `desc_license` by root's governing law, each with its vassal variant `desc_ban_v` / `desc_license_v` (lore R1, as act.001).

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "Disqualify them." | — | the accused withdrawn as act.001.b, with `eotg_opinion_aug_barred`; the accuser `add_opinion = { modifier = eotg_opinion_aug_reassured  target = root }` | 30; +20 zealous; +10 just |
| b | "The accusation fails." | — | the accuser `add_opinion = { modifier = eotg_opinion_aug_unease  target = root  years = 5 }`; the accused `add_opinion = { modifier = eotg_opinion_aug_reassured  target = root }` | 30; +20 cynical; +10 trusting |
| c | "Have them examined." | `eotg_aug_has_surgeon_access = yes` | `if = { limit = { scope:eotg_aug_accused = { OR = { eotg_is_aug_tier3 = yes  eotg_neurofractured = yes  eotg_aug_pressure_flicker = no } } } …` withdraw them as a, toast `.c.hot` `}` `else = {` as b, toast `.c.clean` `}` | 30; +20 diligent; +10 paranoid |
| d | "Let them settle it on the field." | — | the accused: hidden risk +4, `activity_tournament_change_contestant_score_effect = { SCORE = increase_minor }`; the accuser: `SCORE = decrease_minor` | 30; +20 arrogant; +10 brave |
| e [just] | "Hear them both, then rule." | `has_trait = just` | as c without the surgeon trigger (the host's own judgment); plus `add_prestige = minor_prestige_value` | 30; +30 just; +10 diligent |

**Evidence is physical only (lore R6):** a strike too fast for an arm, heat off a casing, scorched heat sinks, a hands-on look. Never logs, telemetry, a signal, a jammer, a relay, "hacked", or anyone controlling the hardware. `.c.hot` / `.c.clean` never say who examined, because option e reaches them too.

**Coupling:** c and e read the band in their branch trigger; d moves risk; the desc reads the band.

#### act.004 *A Hum at the Table* (feast)
- **Trigger:** `exists = scope:activity`; `eotg_is_augmented_any = yes`; NOT Seamless.
- **Desc:** base (the servo in the wrist ticks as you lift the cup; the guests have noticed); `desc_host` when root hosts; `desc_oc` / `desc_nf` (reads tier).

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "Show them what it does." | — | `add_prestige = minor_prestige_value`; hidden risk +3; every zealous attendee `eotg_opinion_aug_unease` (5 years); every cynical attendee `eotg_opinion_aug_admiration` | 30; +20 gregarious; +20 arrogant; −20 shy |
| b | "Keep it out of sight." | — | `eotg_aug_stress_lie_effect = yes` | 30; +20 shy; +10 deceitful |
| c | "Answer their questions plainly." | — | `add_prestige = minor_prestige_value`; no opinion changes | 30; +20 honest; +10 diligent |
| d [gregarious] | "Make it the talk of the feast." | `has_trait = gregarious` | as a, with `add_prestige = medium_prestige_value` and hidden risk +4 | 30; +30 gregarious; +10 ambitious |
| e [shy] | "Excuse yourself early." | `has_trait = shy` | `add_prestige = { value = minor_prestige_value  multiply = -1 }`; `eotg_aug_stress_reject_effect`; no risk move | 30; +30 shy; +10 craven |

**Coupling:** a and d move risk; the desc reads tier.

#### act.005 *Quarry in the Overlay* (hunt)
- **Trigger:** `exists = scope:activity`; `eotg_is_augmented_any = yes`; NOT Seamless.
- **Desc:** base (the optics pick out a trail no one else sees); `desc_senses` when `var:eotg_aug_focus ?= flag:senses` (thread T7: the trail is truer); `desc_hum` when tier ≥ 2 and not senses focus (the game hears the coil whine before it sees you).

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "Let the optics track it." | — | `hunt_activity_success_change_effect = { CHANGE = increase_medium }` (`increase_major` with senses focus); hidden risk +2 (tier 3: +3) | 30; +20 ambitious; +10 diligent |
| b | "Hunt the old way." | — | `CHANGE = increase_minor` if `prowess >= 12`, else nothing; `add_prestige = minor_prestige_value` | 30; +20 humble; +10 brave |
| c | "Power down and wait." | — | `CHANGE = decrease_minor`; tier 3: hidden risk −3 | 30; +20 patient; +10 content |
| d [brave] | "Run it down at full output." | `has_trait = brave` | `CHANGE = increase_major`; hidden risk +4; `eotg_mod_aug_lesson_prowess` 5 years | 30; +30 brave; +10 wrathful |
| e [lifestyle_hunter] | "Tune it to the trail." | `has_trait = lifestyle_hunter` | `CHANGE = increase_major`; hidden risk +1 | 30; +30 lifestyle_hunter; +10 diligent |

**Coupling:** a, d and e move risk; c moves it down at tier 3; the desc reads focus and tier.

#### act.006 *At the Holy Site* (pilgrimage)
- **Trigger:** `exists = scope:activity`; `eotg_is_augmented_any = yes`; NOT Seamless.
- **Desc:** base (those who tend the site look at the hardware before they look at you; lore R5: never "keepers"); `desc_hot` when tier 3 / NF or past the Flicker band (reads band: the hardware is warm to the touch after the long approach). **Faith-neutral**: no doctrine, no god-name, no "blessing of the machine" claim (index §5 item 4; the zealous-vs-Industrial-Survivalism deferral).

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "Kneel as I am." | — | `add_piety = minor_piety_value`; zealous: `stress_impact = { zealous = minor_stress_impact_gain }` | 30; +20 humble; +10 just |
| b | "Cover it, and kneel." | — | `add_piety = minor_piety_value`; `eotg_aug_stress_lie_effect = yes` | 30; +20 deceitful; +10 shy |
| c | "Stay the week, and rest." | — | `stress_impact = { base = minor_stress_impact_loss }` (as Maintenance); tier 3 / NF: hidden risk −3 (the hardware cools) | 30; +20 content; +10 lazy |
| d [zealous] | "Keep the full vigil." | `has_trait = zealous` | `add_piety = medium_piety_value`; `stress_impact = { zealous = minor_stress_impact_loss }` | 30; +30 zealous; +10 humble |
| e [cynical] | "Leave before the rites." | `has_trait = cynical` | `add_piety = { value = minor_piety_value  multiply = -1 }`; `stress_impact = { cynical = minor_stress_impact_loss }` | 30; +30 cynical; +10 impatient |

e's `ai_chance` names impatient as a weight modifier only, which is not a stress line, so trait-depth §5.2 is not touched.

**Coupling:** c moves risk down at tier 3; the desc reads the band.

### 4.9 AI against the HQ2 world targets

HQ2 (balance §0): at game year 30, **25–40%** of AI count-tier-and-above rulers augmented; of those, **≥ 15%** Overclocked, Neurofractured or Seamless; **≥ 1 terminal outcome per 10 Neurofractured rulers per decade**.

| Lever | Pushes | Design guard | Expected effect at year 30 (first guess; the observer run decides) |
|---|---|---|---|
| **Ban** (AI) | augmented share **down** in governed realms | only unaugmented zealous independents enact it; heirs revert it if cynical or augmented; 10-year cooldown | zealous is roughly one ruler in eight; with heirs reverting, about 10% of independents hold a Ban at a time. A realm's whole hierarchy is governed, so perhaps 10–15% of count+ rulers. Their initiation weight roughly halves (nothing ×2; back-alley ×1.5 does not offset it). **About −2 to −4 points** on the census. |
| **License** (AI) | slightly **up** for safety, **down** at the back alley | diligent or just rulers with augmented vassals | back-alley initiations ×0.5 in those realms; clinic jobs safer. **About −0.5 point**; fewer back-street rejections out of the system. |
| **Favor** (AI) | augmented share **up** | augmented, ambitious or cynical, not zealous | nothing ×0.8 in governed realms; Offer acceptance +15. **About +1 to +2 points.** |
| Crime on discovery and refusal | slower, not fewer | AI lieges imprison at vanilla rates; Demand Removal +50 accept under Ban | **About −0.5 point.** It also feeds Salvage (more augmented prisoners). |
| **Technician** (AI) | the top band **up slightly** (Overclocked lasts longer) | hired only by augmented AI lieges; −2/−3 accrual a year | calm Overclocked accrual 12 → 10: the cascade comes about one pulse later. Raises the Overclocked share; the cascade and terminal rates fall slightly. Watch the terminal rate. |
| Borrow Their Technician (AI) | slower cascades | tier 3 / NF actors without a technician | Small. |
| Activities | top band **up slightly** | player-only except act.001 | negligible for AI. |

**Net:** the law levers roughly cancel (Ban −2 to −4 against Favor +1 to +2); the realm splits by its ruler's temperament, which is the design intent. The census should stay inside 25–40%.

**Tuning rule (balance §9.2):** change only the laws' `ai_will_do` numbers, the initiation-pulse policy factors, `ai_position_score` and the interaction weights. Do not change content.

**The observer run gains four counters** per decade: (1) share of count+ AI rulers governed by each law; (2) initiations per 10 governed rulers, split by law; (3) contraband crimes and Defied-Law refusals; (4) AI technicians employed, and the Overclocked→cascade median for rulers with and without one.

---

## 5. File placement

| Path | What |
|---|---|
| `common/law_groups/eotg_augmentation_law_groups.txt` | **new folder and file**: `eotg_aug_policy_laws` |
| `common/laws/eotg_augmentation_laws.txt` | **new folder and file**: the four laws |
| `common/court_positions/types/eotg_augmentation_court_positions.txt` | **new folder and file**: `eotg_aug_implant_technician_court_position` |
| `common/character_interactions/eotg_augmentation_interactions.txt` | the interactions spec's file: add `eotg_aug_borrow_technician_interaction`; the §3.2 amendments |
| `events/eotg_augmentation_activities.txt` | **new**: namespace `eotg_aug_act`; act.001–.006. Header in the siblings' style (fires-from map, resource line). UTF-8 with BOM. |
| `events/eotg_augmentation_realm.txt` | **new**: namespace `eotg_aug_realm`; realm.001 |
| `common/on_action/eotg_augmentation_on_actions.txt` | the 13 vanilla hooks, each `= { on_actions = { eotg_… } }`; the six custom on_actions; the policy factors in the initiation check; the technician row in the Overclocked check; header cooldown list |
| `common/scripted_triggers/eotg_augmentation_triggers.txt` | the §3.1 triggers and `eotg_aug_tournament_entrant` |
| `common/scripted_effects/eotg_augmentation_effects.txt` | `eotg_aug_contraband_effect`; the §3.2 procedures amendments |
| `common/script_values/eotg_augmentation_values.txt` | `eotg_aug_technician_salary_value`; `eotg_aug_price_mult_physician` made conditional; the bad-factor rows |
| `common/opinion_modifiers/eotg_augmentation_opinions.txt` | the four opinions |
| `common/decisions/eotg_augmentation_decisions.txt` | Maintenance and Seek changes (§3.3) |
| `events/eotg_augmentation_procedures.txt`, `_initiation.txt`, `_tier1.txt`, `_tier2.txt`, `_tamper.txt`, `_interactions.txt` | the §3.2 clinic and surgeon option amendments |
| `localization/english/eotg_augmentation_l_english.yml` | §7 |

**No `replace_path`. No vanilla file overridden.** Every vanilla on_action is extended additively; the law group, laws and court position are new keys in new files.

**New folders for the `CLAUDE.md` placement table** (orchestrator): `common/law_groups/`, `common/laws/`, `common/court_positions/types/`. (The interactions spec already asked for `common/character_interactions/` and `common/schemes/scheme_types/`.)

---

## 6. Vanilla precedent (consolidated)

| Mechanism | File:line | Used for |
|---|---|---|
| 1.20 law group / law split; `law_group_type`, `index` | `common/law_groups/_law_groups.info`; `common/laws/_laws.info`; `00_realm_law_groups.txt:22`; `00_realm_laws.txt:801-833` | §4.1 |
| `realm_law` and `realm_law_no_number` flags; My Realm listing | `_laws.info` hardcoded flags; `gui/window_my_realm.gui:1280-1327`; `00_realm_law_groups.txt:70-76` | §4.1 |
| `can_change_law_group` with a custom tooltip | `00_succession_law_groups.txt:1-15` | §4.1 |
| Pick-one policy: prestige pass cost, trait-weighted `ai_will_do` | `00_realm_laws.txt:2554-2646` (mandala decree) | §4.1 |
| Law cooldown variable in `on_pass`, `custom_description` in `can_pass` | `00_realm_laws.txt:76-118`; `02_admininistrative_laws.txt:36-40, 70-77` | §4.1 |
| Vassal-stance opinion modifiers in a law's `modifier` | `00_realm_laws.txt:24-30, 52-60, 133-141`; `vassal_stances/00_vassal_stances.txt:1, 172, 334, 510, 996`; `_vassal_stances.info` | §4.1 |
| Refusal as a crime: triggered desc, +50 accept, `reverse_add_opinion` with `imprisonment_reason` | `00_religious_interactions.txt:160-180, 640-672`; `00_religious_opinions.txt:118-123`; `00_religion_scripted_modifiers.txt:262-275` | §4.3 |
| Imprisonment helper | `scripted_effects/00_prison_effects.txt:1644` | realm.001 a/e |
| Court position: physician (aptitude, salary, AI) and artificer (effects, candidate score) | `court_positions/types/00_court_positions.txt:41-562, 10896-11193`; `_court_positions.info` | §4.5 |
| Court-position triggers, effects, values | `00_court_position_triggers.txt:398-411, 494-497, 2053-2056`; `00_court_position_effects.txt:7, 96, 147, 3414`; `00_court_position_values.txt:846, 2260, 2338`; `00_ep1_script_values.txt:353, 389` | §4.5 |
| Additive child on_actions on activity hooks; once-per-activity variable | `ep2_tournament_on_actions.txt:6-19, 28, 82-349, 699`; `feast_on_actions.txt:20-24, 38-50`; `hunt_on_actions.txt:5-8, 17`; `pilgrimage_on_actions.txt:380` | §4.7 |
| Activity fire sites (root, timing) | `activity_types/tournament.txt:5617-5622, 6197-6199`; `feast.txt:4542-4552`; `hunt.txt:5030-5043`; `pilgrimage.txt:2536-2540`; `04_dlc_ep2_tournament_effects.txt:599-603, 1994-2018` | §4.7 |
| Tournament score change; contestant withdrawal | `04_dlc_ep2_tournament_effects.txt:13-60`; `04_ep2_tournament_values.txt:1962-1984`; `tournament_events.txt:4498-4499, 9315-9323`; `04_ep2_tournament_triggers.txt:21-37` | act.001–.003 |
| A versus-bout player event (portraits, score effect, stress) | `events/dlc/ep2/ep2_tournament_events.txt` (`ep2_tournament_events.0021`) | act.002 |
| Hunt success change | `00_hunt_effects.txt:948-966`; `04_ep2_hunt_values.txt:91-110`; `hunt_events.txt:6376-6420` (`hunt.1023`) | act.005 |
| Triggered option names | `events/health_events.txt:1143-1146` | §3.2 name variants |
| `show_as_unavailable` on an option | `tournament_events.txt:4496` | clinic closed |
| DLC trigger for tournaments | `00_has_dlc_scripted_triggers.txt:110-112` | §1, §9 |

**Deviations, with reasons:**
- **No `scaling_employer_modifiers` on the technician.** Every vanilla position has some; the `.info` allows 0. A modifier would benefit an unaugmented employer and could not express the risk lever without a number.
- **No vassal-level policy.** Vanilla realm laws are per ruler. Here only the independent top ruler sets the policy and everyone below follows it, because the setting's law is realm-local and a patchwork of sub-realm policies would let a count license what the king bans.
- **No `random_events` appended to vanilla activity pools** (§4.7). Children with their own gate instead.

**Tiger:** Tiger 1.17 targets 1.18.3. Findings on `common/law_groups/`, `law_group_type`, `index`, or 1.20 court-position fields are checked against the vanilla files cited in §0 before being treated as real. The procedures paths into `increase_wounds_no_death_effect` still raise the 16 known-benign `20_health_effects.txt` errors.

---

## 7. Loc surface (eotg-localizer)

**Binding:** [cybernetics_v2_realm_lore.md](cybernetics_v2_realm_lore.md) (eotg-lore-keeper, 2026-10-04) gives the picked names, must-fixes R1–R8 and the exact renderings. Where it gives a rendering, the localizer uses it (polish allowed). The briefs below are fallback guidance only.

Rules:
- index §5 items 1–8 and today's never-name extension;
- US spelling ("Favor", "license" as noun and verb);
- bare `[x.GetName]`;
- appended desc lines start with `\n\n`;
- **no tooltip, toast, law `_effects`, court-position text or desc quantifies risk or odds**;
- **no "Accord", no "galactic", no "programme"/"program", no "subsidy", no "state clinic"**; clinics stay **unnamed** ("a sanctioned clinic", "sanctioned hands"); **no named authority** licenses anything: the ruler's own law does;
- tournament, hunt and pilgrimage text: per the binding register below (index §5.6).

**Binding register (LAW AT 866; lore R1–R8, Q1, Q2):**
- The law is never anyone's law but the realm's own, as set by the ruler at its head (R1). A vassal reads "the law of your realm"; only an independent ruler reads "your law".
- Never an unqualified "the law". Allowed: "your law", "your realm's law", "the law of your realm" (R2).
- `eotg_aug_policy_set_by_liege_tt`: "Set by the ruler at the head of your realm, for all of it." (R3)
- **No apparatus** (Q1 boundary, §8): never authorities, enforcers, inspectors, magistrates, tribunals, warrants, registries, permits, certification, regulation(s) or a named licensing body. Discovery is hearsay only ("word has got out", "word has reached you").
- **Favor** is the ruler's open regard at court. It never offers money, clinics, schooling or any scheme of the state's (New Cauldron, 1610). Never "encourage", "promote", "sponsor", "support", "invest", "programme"/"program", "patron" or "patronage" (Q2). Its `_effects` never implies the ruler pays, supplies or arranges anything.
- A lent technician "will see to your implants for a year"; never travel or joining your court (R8).
- **Tournaments:** allowed "the field", "the bout", "the arena", "the marshal", "the stands", "the trial grounds"; banned "lists", "joust", "tilt", "lance", "horse", "squire".
- **Hunts:** "the quarry" and "the trail" only; no Earth animals, hounds or mounts.
- **Foul play** is shown by physical evidence only (R6). The hum is audible hardware (R7).

No vanilla string needs a `replace/` override. Vanilla keys reused: `tournament_not_competing_tt`, `AI_OPINION_REASON`, `court_position_skill_learning`, `court_position_physician_1/2/3_trait`, `court_position_blind_trait`, `education_learning`, and the vassal-stance names (shown by the engine in opinion breakdowns).

| Keys | Count |
|---|---|
| **Law group and laws:** `eotg_aug_policy_laws`; `eotg_aug_policy_ban`, `_license`, `_tolerate`, `_favor`; each `_effects` and `_desc` (renderings in the lore file) | 13 |
| **Law tooltips:** `eotg_aug_policy_cooldown_tt`, `eotg_aug_policy_set_by_liege_tt`, `eotg_aug_clinic_closed_tt` | 3 |
| **Opinions:** `eotg_opinion_aug_contraband` ("Unlawful Implants"), `eotg_opinion_aug_defied_law` ("Refused a Lawful Order"), `eotg_opinion_aug_outlawed` ("Outlawed My Implants"), `eotg_opinion_aug_barred` ("Barred Me from the Field") | 4 |
| **Demand Removal amendments:** `eotg_aug_demand_removal_crime_desc`, `eotg_aug_demand_crime_toast`, `EOTG_AUG_AI_REFUSAL_IS_CRIME`; Offer: `EOTG_AUG_AI_BANNED`, `EOTG_AUG_AI_FAVORED` | 5 |
| **Court position:** `eotg_aug_implant_technician_court_position`, `_desc`, `eotg_aug_implant_technician_employer_desc`, `eotg_aug_technician_aptitude_augmented`, `eotg_aug_technician_aptitude_former`, `eotg_aug_technician_banned_tt` | 6 |
| **Option name variant:** `eotg_aug_opt_technician` ("My implant technician.") | 1 |
| **Borrow Their Technician:** `eotg_aug_borrow_technician_interaction`, `_desc`, `_notification`, `eotg_aug_borrow_accepted_toast`, `eotg_aug_borrow_declined_toast`, `EOTG_AUG_AI_ALLIED`, `EOTG_AUG_AI_FAMILY`, `EOTG_AUG_AI_GENEROUS`, `EOTG_AUG_AI_NEEDS_TECHNICIAN` | 9 |
| `eotg_aug_act.001.t`, `.desc`, `.desc_many`, `.desc_entrant_oc`, `.desc_entrant_nf`, `.desc_ban`, `.desc_ban_v`, `.a`–`.e`, `.barred_toast` | 13 |
| `eotg_aug_act.002.t`, `.desc`, `.desc_board`, `.desc_physical`, `.desc_hot`, `.desc_ban`, `.a`–`.e`, `.a.seen` | 12 |
| `eotg_aug_act.003.t`, `.desc`, `.desc_hot`, `.desc_ban`, `.desc_ban_v`, `.desc_license`, `.desc_license_v`, `.a`–`.e`, `.c.hot`, `.c.clean` | 14 |
| `eotg_aug_act.004.t`, `.desc`, `.desc_host`, `.desc_oc`, `.desc_nf`, `.a`–`.e` | 10 |
| `eotg_aug_act.005.t`, `.desc`, `.desc_senses`, `.desc_hum`, `.a`–`.e` | 9 |
| `eotg_aug_act.006.t`, `.desc`, `.desc_hot`, `.a`–`.e` | 8 |
| `eotg_aug_realm.001.t`, `.desc`, `.desc_ban`, `.desc_ban_v`, `.desc_license`, `.desc_license_v`, `.desc_aug`, `.desc_enh`, `.desc_oc`, `.desc_nf`, `.desc_courtier`, `.a`–`.f` | 17 |
| **Total** | **~124**: the first draft's ~115, plus the 5 R1 vassal variants and the 4 law `_desc` keys. Toasts with a title and a body (barred, demand crime, borrow accepted) may each need a body key; the localizer adds them if PX asks. |

**Briefs:**
- **Law names (picked):** group "Augmentation"; laws "Augmentation Prohibited", "Augmentation Licensed", "Augmentation Tolerated", "Augmentation Favored". `_effects` lines describe consequences plainly ("Sanctioned clinics will not operate in your realm"; "Unsanctioned implant work in your realm is a crime"; "Refusing your order to remove implants is a crime"). The Favor `_effects` must not suggest the ruler pays for, supplies or arranges implants.
- **`eotg_aug_policy_set_by_liege_tt`:** "Set by the ruler at the head of your realm, for all of it." (R3)
- **`eotg_aug_clinic_closed_tt`:** "No sanctioned clinic operates where augmentation is prohibited."
- **Court position:** "Implant Technician". `_desc`: a specialist in fitting and servicing implants, kept at court. Employer text: the brief in §4.5. No numbers.
- **Borrow Their Technician** (picked name). The fee is plain ("for a fee"). The technician does not travel (R8).
- **realm.001:** "word has reached you", the procedures register. The subject is named. The law is "your law" for an independent ruler and "the law of your realm" otherwise (R1). If guards appear: "your guards", not "wardens". Option b is "Have it taken out", clinical, not cruel.
- **act.001–.003:** the field's rules "never imagined" hardware. "Past spec" means the hardware is pushed past its rated output (bodily, local). act.002 is not titled "Running Hot": that is the shipped modifier `eotg_mod_aug_running_hot` (R4). No remote control, no signal (interactions §7).
- **act.004:** the servo tick, the dulled palate (the existing *Dulled Palate* register), the guests' eyes. The hum is **audible hardware** (servo tick, coil whine), never "at the edge of hearing" or faint "from somewhere" (lore R7).
- **act.005:** the optics and the coil whine (init.015's audible hardware, index §5 item 8). Nothing hunts "for" you; you see more.
- **act.006:** faith-neutral. Those who tend the site react to the person, not to any doctrine on machines. Say "the holy site" (a building, if one is needed: Sanctum). No god-name, doctrine, pray, bless or sacrament (index §5 item 4; lore R5).
- **Titles (picked):** *The Rules of the Field*, *Past Spec*, *Foul Play?*, *A Hum at the Table*, *Quarry in the Overlay*, *At the Holy Site*, *Contraband Hardware*.

---

## 8. Lore constraints

- **LAW AT 866** (SETTING LORE ERRATA; `REVIEW_866.md` "Law above the polity: None"): every law here is the ruler's own. The top ruler of a realm sets it; nothing sits above; no court, tribunal, arbiter or licensing body exists or is implied. A licence is granted "under your law", by no named office.
- **Not a state programme or subsidy** (New Cauldron's Cybernetics Accord, 1610): Ban, License and Tolerate regulate; **Favor is regard, not provision**. No law gives gold, lowers prices, opens clinics or supplies hardware. The only price effect in this spec belongs to the Technician, a private employee of one court. Never "Accord", never "galactic".
- **Sanctioned clinics stay unnamed** (index §5.3). Never name the 866 implant players (Blackstar, Shadow Markets, Black Contracts, Blackline, P&D, Calix, Pill Mob / Pillwake / Red Pills, Concrete Cartel; not "Trauma Team").
- **Tech ceiling** (procedures lore): the Technician fits and services. No remote diagnostics, no networked maintenance, no self-repair (975).
- **Faith:** zealous / cynical / piety only; the zealot vassal stance is personality-scored (§4.1). act.006 is faith-neutral.
- **Nikios Khanate:** not touched.
- **Lore review: done** (eotg-lore-keeper, 2026-10-04, [cybernetics_v2_realm_lore.md](cybernetics_v2_realm_lore.md)). Approved with R1–R8 (all wording), folded in above. Names picked (§7).
- **Q1. Arrest: approved, inside LAW AT 866.** Binding boundary for script and loc:
  1. The arrest is made by the subject's own liege, inside the realm, under that realm's own law, which the ruler at the head of the realm set.
  2. **No apparatus.** Never authorities, enforcers, inspectors, magistrates, tribunals, warrants, registries, permits or permit offices, certification, regulation(s), or a named licensing body. "Your court" as a household is fine. A licence is held "under your law".
  3. Discovery is hearsay only: "word has got out" or "word has reached you". No investigation, records, scans or implant register.
  4. Under Tolerate or Favor, and for the independent lawmaker themself: no arrest, and no authority (the procedures ruling stands there).
  5. The law never reaches outside the realm. No extradition, no foreign warrant.
  6. A Ban never "created or fed" the black market. The back streets are simply what is left under it.
  - The matching Discovery amendment is applied to [cybernetics_v2_procedures_lore.md](cybernetics_v2_procedures_lore.md).
- **Q2. Favor: kept; four laws.** Open regard is a personal stance, not provision. Its mechanics are approved (more offers, +15 Offer acceptance, back-street discovery ×0.5). Banned words are in §7.
- **Open, canon silent (optional vault questions, not blocking):** 866 hunt fauna (keep "the quarry"); who tends holy sites (keep "those who tend the site" until faith loc exists after Gate 1).

---

## 9. Definition of done

0. **Tiger, `px_lsp_diagnostics.js` and `px_vocab_check.py` clean** on the touched files, except the `CLAUDE.md` known-benign list (including the 16 `20_health_effects.txt` errors). Tiger findings on `common/law_groups/`, `law_group_type`, `index` or court-position fields are checked against the vanilla files in §0 first.
1. **Reachability (PX event graph):**
   - act.001 from `eotg_on_tournament_opening_aug`;
   - act.002 from `eotg_on_tournament_contest_aug`;
   - act.003 from `eotg_on_tournament_active_aug`;
   - act.004 from `eotg_on_feast_aug`; act.005 from `eotg_on_hunt_aug`; act.006 from `eotg_on_pilgrimage_aug`;
   - realm.001 from `eotg_aug_contraband_effect`.
   - Each custom on_action is listed under its vanilla hook(s) in `on_actions = { }` (13 hooks). `px_vocab_check.py` confirms every hook name is live (lesson 13).
2. **Cooldown authority:** `grep -n "eotg_flag_aug_act_\|eotg_flag_aug_contraband_cd\|eotg_aug_act_entrants_ruled\|eotg_aug_act_accusation_done"` finds the setters only in `common/on_action/eotg_augmentation_on_actions.txt` and `eotg_aug_contraband_effect`. No event `trigger` reads them. The law cooldown variable is read only in the laws' `can_pass`.
3. **Additive only:** no top-level `trigger` or `effect` is added to any vanilla on_action; each vanilla hook block in the mod contains only `on_actions = { }`.
4. **Coupling (QA audit 8):** every §4.8 event and realm.001 has an option that moves risk or tier, or reads the band or tier in a desc or branch trigger, per the §2 table.
5. **Hidden rule:** no new loc string contains a number, or the words "risk", "odds" or "chance", about the signature resource. Every risk move is in `hidden_effect`.
6. **Realm-locality:** `eotg_aug_under_policy` is the only reader of the law group (`grep -n "has_realm_law = eotg_aug_policy"` finds it only in that trigger and in the laws' own `ai_will_do`). Non-default laws have `can_keep = { is_independent_ruler = yes }`.
7. **Clinic closure:** with a Ban in force, every clinic option listed in §3.2 shows unavailable with the tooltip; the physician (or technician) and back-street options remain.
8. **Map-agnostic:** `grep -nE "title:|culture:|faith:|religion:|character:[0-9]" common/law_groups common/laws common/court_positions events/eotg_augmentation_activities.txt events/eotg_augmentation_realm.txt` returns nothing.
9. **Identifiers:** every new global key starts `eotg_`; `grep -rnE 'eotg_[ekdcb]_'` stays empty.
10. **Lore register:** `grep -niE "accord|galactic|program|subsid|state clinic|remote|signal|blackstar|p&d|calix|pill ?mob|concrete cartel|trauma team|telemetry|jamm|relay|hack|authorit|warrant|magistrat|inspector|registry|encourag|sponsor|patronag"` over the new loc keys returns nothing.
11. **Loc:** all §7 keys exist exactly once, with BOM and no `[scope:`.
12. **Human, in game (temporary map):**
    - **Law:** an independent ruler sees the **Augmentation** group in My Realm, can pass each law, pays the cost, and then sees the cooldown tooltip. A vassal sees it locked with the liege tooltip. The realm header still shows Crown Authority (not ours) through `GetActiveLawInGroupWithFlag('realm_law')` (`window_my_realm.gui:436`). Missing law icons render as a blank, not a crash (art debt). An heir inherits the law. A ruler who becomes a vassal reverts to Tolerated within a month.
    - **Ban:** zealot-stance vassals show the law's opinion line, augmented vassals show "Outlawed". Seek → init.018 shows the clinic unavailable. Back streets, 20 reloads → some "discovered", the liege (a player) gets realm.001; an AI liege holds the Unlawful Implants opinion. Demand Removal on an augmented vassal shows the crime line; refusal gives "Defied the Law" with the imprison option available.
    - **Technician:** an augmented ruler sees the position; hire; aptitude breakdown shows the augmented line. Procedure options read "My implant technician." Maintenance costs half. Under a Ban as a vassal, the position invalidates.
    - **Borrow Their Technician:** ask an ally who has a technician; after acceptance, procedure options offer the technician for a year.
    - **Activities:** host a tournament (DLC) with an augmented knight → act.001; bar them → they withdraw without vanilla's empty 0800 window. Compete augmented → act.002, the score moves. Feast, hunt → act.004 / act.005.
    - **Engine checks (not settled by vanilla):**
      - (a) a child `on_actions` block on a vanilla activity on_action fires, and the parent's `trigger` gates it;
      - (b) `scope:activity` / `involved_activity` is available in a custom on_action reached from a delayed `trigger_event = { on_action = … }` (the tournament opening, 20 days);
      - (c) the My Realm window lists a non-cumulative modded `realm_law` group with four laws;
      - (d) **pilgrimage** (act.006) needs holy sites; if the temporary map has none, this check waits for Gate 1 faiths and is recorded on the circleback board, not failed.
    - **Testers without Tours & Tournaments** see no tournament events (lesson 12). The feast, hunt and pilgrimage events are their fallback, and the law and Technician do not depend on any DLC.
13. **Observer run** (balance §9.2) gains the four §4.9 counters and is judged against HQ2.

---

## 10. Deferred

| Item | Why |
|---|---|
| **The accused-player perspective in act.003** (an AI host rules on the player) | act.002 option a already carries "someone saw it" for a player who runs hot. A second perspective doubles the event's loc. Revisit if testers want it. |
| **Seamless at activities** | No risk to move, and the court has left (end.011). A residue-coupled feast beat would repeat end.040–.042. |
| **Recital, weddings, tours, coronations, other activities** | Lean scope (the human's instruction). The hook pattern in §4.7 extends to any of them with one more `on_actions` line. |
| **Faith doctrines and cultural traditions on augmentation** | Already deferred to after Gate 1 (index §5, gaps G12). The law is the map-agnostic stand-in. |
| **Vassal-level (sub-realm) policies** | Realm-local means the realm's top; sub-realm patchworks are cut (§6). |
| **A fourth `PROVIDER` column for the technician** | The `SURGEON` route keeps odds in one place (§4.5). |
| **The technician in thread T5** (Consult the Physician, Excision, the Bridge, Rejection) | It would rewrite many built options. The technician is a surgeon, not a physician. |
| **Scaling employer modifiers on the technician** | §6 deviation. |
| **An "encourage" law that provides anything** (subsidy, state clinics, price cuts) | Forbidden by canon (§8). Favor is regard only, pending the lore-keeper's ruling. |
| **Ransom for augmented prisoners** | Unchanged from the interactions deferral (vanilla ransom script values would need an override). |
| **Bespoke art:** 4 law icons, 1 court-position icon, the interaction icon | Art debt for the human (§3.1). |
| **Men-at-arms (G11), the Clinic building (Q10)** | Unchanged deferrals. |

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Build docs/specs/cybernetics_v2_realm.md §3–§5 after the procedures and interactions specs land (including the §3.2 amendments to those two specs and the §3.3 changes to built script); then eotg-localizer (§7, renderings from docs/specs/cybernetics_v2_realm_lore.md), then eotg-qa (§9).
- files: docs/specs/cybernetics_v2_realm.md (lore R1–R8, Q1, Q2 and names folded in); docs/specs/cybernetics_v2_procedures_lore.md (Discovery amendment)
- new events (7; below the ~10 flag): eotg_aug_act.001 The Rules of the Field (tournament_opening_on_action → eotg_on_tournament_opening_aug); eotg_aug_act.002 Past Spec (7 contest random pulses → eotg_on_tournament_contest_aug); eotg_aug_act.003 Foul Play? (tournament_active_state_pulse → eotg_on_tournament_active_aug); eotg_aug_act.004 A Hum at the Table (feast_default_event_selection → eotg_on_feast_aug); eotg_aug_act.005 Quarry in the Overlay (hunt_random_pulse → eotg_on_hunt_aug); eotg_aug_act.006 At the Holy Site (pilgrimage_destination_events → eotg_on_pilgrimage_aug); eotg_aug_realm.001 Contraband Hardware (eotg_aug_contraband_effect). Also law group eotg_aug_policy_laws (4 laws), court position eotg_aug_implant_technician_court_position, interaction eotg_aug_borrow_technician_interaction (Borrow Their Technician).
- needs-loc (~124, §7; renderings binding in docs/specs/cybernetics_v2_realm_lore.md): law group, 4 laws with _effects and _desc (13); 3 law tooltips; 4 opinions; Demand/Offer amendment keys (5); court position keys (6); eotg_aug_opt_technician; Borrow Their Technician keys (9); eotg_aug_act.001–.006.* (66, including the R1 desc_ban_v / desc_license_v variants); eotg_aug_realm.001.* (17).
- needs-lore: none (review done; R1–R8, Q1, Q2 folded in). Optional vault questions: 866 hunt fauna, who tends holy sites.
- needs-human: §9 item 12 in-game checks, including engine checks (a)–(d) (child on_actions under vanilla activity hooks, activity scope after the delayed tournament opening, My Realm listing a modded realm_law group, pilgrimage needing holy sites); tournaments need the Tours & Tournaments DLC; art debt: 4 law icons, 1 court-position icon, the interaction icon; the observer run's four new counters (§4.9); the orchestrator adds common/law_groups/, common/laws/ and common/court_positions/types/ to the CLAUDE.md placement table.
