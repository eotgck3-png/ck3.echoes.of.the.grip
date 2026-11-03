# Spec: Confluence Legacies v2 (lift spec and audit; nothing built)

**Author:** cloud session, 2026-11-03 (final queue, H3). **Status:** spec only. **No game script, events or loc are written** until the owner rules Legacies mod-exclusive (Q7). Next: owner rulings (§11), then eotg-lore-keeper (§8), then one scripter pass, then the localizer.

**Sources:**
- the readiness audit: `docs/qa/v1_lift_readiness_cloud.md` §2 "L. Confluence Legacies v1" and §3 item 7;
- `OLD VERSION CATALOG.md` §2.4 and §4 (the lessons);
- the pitch: `OLD PROJECT VERSION/docs/confluence_legacies_system_pitch.md`;
- the v1 files: `OLD PROJECT VERSION/events/eotg_legacy_events.txt` (16 events), `OLD PROJECT VERSION/common/{decisions,modifiers,on_action,opinion_modifiers,scripted_effects,scripted_triggers}/eotg_legacy_*`, and `OLD PROJECT VERSION/localization/english/eotg_legacy_l_english.yml` (127 keys).

**Canon:** the SETTING LORE ERRATA block, then `docs/lore/REVIEW_866.md` (Settled item 6; the ERAS draft, which follows from SOURCE PRECEDENCE).

**Pattern copied:** `docs/specs/void_corruption_v2.md` and the merged Void files. That means:
- one clamped writer per variable;
- cooldowns only in the on_action or decision;
- `yearly_playable_pulse`;
- an inert trigger for anything map-coupled;
- an identifier table and a fate table.

**Engine citations** are to v2 script that already does the same thing; anything else is marked UNVERIFIED-VANILLA.

---

## 0. Kind of build

**A mod-exclusive candidate, lifted with fixes.** Legacies keeps all state on county titles and needs only "a landed ruler holds counties", so once the 7 history characters and the Exodus path are removed it runs on any map, the temporary one included. It still needs the owner's mod-exclusive ruling (audit §3 Q7) before it may be built ahead of Gate 1.

**Core verb:** *a ruler finds what the Grip buried under their ground, then chooses to recover, exploit, seal or claim it. That choice sets the site's condition, its remaining integrity and how much attention it draws, and attention brings rivals, vassals and cults back for it.*

---

## 1. Purpose & gate

- **Purpose.** v1 was complete and never ran: it sat on the dead `on_yearly_playable` hook (audit HIGH row 1). v2 makes it run, removes the map coupling (HIGH rows 2 and 3), settles the canon text (HIGH row 4) and resolves every MED and LOW row (§5).
- **Gate.** The mod-exclusive exemption (CLAUDE.md, 2026-10-02), pending Q7. Until then this spec is the build order; nothing is written.

---

## 2. Resources and the state machine

### 2.1 Variables (all on the county title; a site outlives its holder: pitch rule "a Legacy remembers")

| Variable | Range | Meaning | Single writer (v2) | v1 writer(s) |
|---|---|---|---|---|
| `eotg_legacy_family` | 1–4 | 1 Buried Metropolis, 2 Archive Fragment, 3 Relic Works, 4 Planar Pocket (v1 "Hell Pocket", name pending Q2) | `eotg_legacy_seed_effect` (once) | `eotg_se_legacy_seed` (`eotg_legacy_effects.txt:9-14`) |
| `eotg_legacy_known` | set / unset | discovered | `eotg_legacy_make_known_effect` | `eotg_se_legacy_make_known` (`:17-23`) |
| `eotg_legacy_condition` | 1–6 | 1 dormant, 2 exposed, 3 governed, 4 extracted, 5 sealed, 6 unstable | `eotg_legacy_set_condition_effect` (also refreshes the county modifier) | `eotg_se_legacy_set_condition` (`:28-31`); `eotg_se_legacy_make_known` also wrote it (`:19-22`), a second writer |
| `eotg_legacy_integrity` | 0–100 | how much of the site remains (starts 80) | `eotg_legacy_change_integrity_effect` | `eotg_se_legacy_add_integrity` (`:96-114`) |
| `eotg_legacy_attention` | 0–100 | how far word has spread (starts 0) | `eotg_legacy_change_attention_effect` | `eotg_se_legacy_add_attention` (`:82-92`) |
| `eotg_legacy_site_cd` | timed | the site is quiet while it exists | `eotg_legacy_set_site_cooldown_effect`, called **only** from firing points (§3) | `eotg_se_legacy_cooldown` (`:117-119`), called from ~30 event options |

**Writer shape (copy of `eotg_void_change_exposure_effect`):**
1. create the variable at 0 if missing;
2. `change_variable` by `$AMOUNT$`;
3. `clamp_variable` to 0–100;
4. refresh what depends on it.

**Every AMOUNT is a literal or a named script value** (an inline block is not a valid `$AMOUNT$`, Void spec §2).

**The make-known fix.** `eotg_legacy_make_known_effect` no longer writes the condition itself. It calls `eotg_legacy_set_condition_effect = { CONDITION = 2 }` when the condition is 1, so the condition has exactly one writer and the modifier refresh always runs.

### 2.2 Bands

**Attention bands** (v1 comment, `eotg_legacy_triggers.txt:12-13`; read by triggers only, no new modifiers):

| Attention | Band | What reads it |
|---|---|---|
| 0–24 | Obscure | nothing |
| 25–49 | Rumoured | the rival-claim aftermath (0101) at ≥ 25 (`eotg_legacy_rival_gate_value`, Q10); decay stops at 25 once reached (`eotg_legacy_attention_floor_value`) |
| 50–74 | Contested | nothing new (v1 gated 0101 here; the sim shows it never fires, Q10) |
| 75–100 | Renowned | nothing new (the old ×1.5 idea is dropped, Q10) |

**Integrity:**

| Integrity | What happens |
|---|---|
| ≤ 50 | the cult aftermath (0103) can roll on governed or sealed sites |
| 0 | the condition becomes Unstable and 0104 fires, **once, on the crossing** (§5, MED-2) |

### 2.3 Conditions and transitions

```
 seed (game start, survey fallback 0002/0003)
   |
 [1 dormant, hidden] --discovery (survey; fire_discovery)--> [2 exposed, known]
                                                                |
                         family event 0010 / 0020 / 0030 / 0040 (the core choice)
            +--------------------+--------------------+--------------------+
            v                    v                    v                    v
      [3 governed]         [4 extracted]          [5 sealed]          (claim: 0021 heir;
      Recover              Exploit                 Seal                 0041 debt)
            |                    |                    |
            +------- integrity reaches 0 (any writer) ------> [6 unstable] -> 0104 (once)
                                                                  0104.c "deeper" -> [2 exposed]
                                                                  0104.a "stabilize" -> [5 sealed]
```

**County modifier by condition** (single owner: `eotg_legacy_refresh_modifier_effect`, v1 `:36-79`):

| Condition | Modifier |
|---|---|
| 3 governed | by family: `eotg_mod_legacy_metropolis_governed`, `_archive_governed`, `_works_governed`, `_planar_warded` |
| 4 extracted | `eotg_mod_legacy_extracted_site` |
| 5 sealed | `eotg_mod_legacy_sealed_site` |
| 6 unstable | `eotg_mod_legacy_unstable_site` |
| 1, 2 | none |

**Sources of motion (as v1; the sim in §12 checks the equilibria):**
- **attention:**
  - −2 a year on every known held site with attention > 0, in the yearly pulse (v1 `eotg_legacy_on_actions.txt:32-39`; value `eotg_legacy_attention_decay_value`);
  - event options: −20 to +35.
- **integrity:** event options only, −30 to +15. **There is no passive drain** (Q8 asks whether Extracted sites should drain).

---

## 3. Hooks and cooldown authority

All three hooks are extended **additively** (`on_actions = { }`), never with a top-level effect (invariant 4). Each is confirmed by existing v2 usage.

| Hook | v2 on_action | Root / scopes | v2 precedent |
|---|---|---|---|
| `yearly_playable_pulse` | `eotg_on_yearly_legacy_check` | a playable ruler | `common/on_action/eotg_frontier_on_actions.txt:10-14,35`, `eotg_void_on_actions.txt:27-31` (the dead `on_yearly_playable` is lesson 13) |
| `on_title_gain` | `eotg_on_title_gain_legacy_check` | root = new holder; `scope:title` | `common/on_action/eotg_cartel_on_actions.txt:36-39` ("root = the new holder; scope:title; scope:previous_holder"), `eotg_government_on_actions.txt:36` |
| `on_game_start_after_lobby` | `eotg_on_game_start_legacy_seed` | none (global) | `common/on_action/eotg_augmentation_on_actions.txt:159-163`, `eotg_cartel_on_actions.txt:21` |

### 3.1 The yearly check (`eotg_on_yearly_legacy_check`)

Gate: `is_landed = yes`, `is_adult = yes` (as v1 `:26-29`). Steps, in order:

1. **Attention decay and Extracted drain.**
   - `every_held_title = { limit = { tier = tier_county  eotg_legacy_is_known_site = yes  var:eotg_legacy_attention > eotg_legacy_attention_floor_value } eotg_legacy_change_attention_effect = { AMOUNT = eotg_legacy_attention_decay_value } }`, where the floor is 25 (Q10). The floor applies only to sites that have reached it: below 25, the floor is 0. That needs a site flag `eotg_legacy_reached_rumoured`, set by the attention writer when the value crosses 25.
   - Then, for condition 4, `eotg_legacy_change_integrity_effect = { AMOUNT = eotg_legacy_extracted_drain_value }` (−1, Q8).
2. **One aftermath roll a year**, gated by `NOT = { has_character_flag = eotg_flag_legacy_aftermath_cd }`. This is the first-valid chain v1 used (`:61-155`), with the chances from named values:
   - 0101 at 25%: a known site with attention ≥ `eotg_legacy_rival_gate_value` (25, Q10; v1 had 50) that is ready;
   - else 0102 at 20%: a powerful vassal and an extracted site that is ready;
   - else 0103 at 15%: a governed or sealed site with integrity ≤ 50 that is ready.

   Each branch, **at fire time**:
   - sets `eotg_flag_legacy_aftermath_cd` (2 years);
   - saves the chosen county as `scope:eotg_legacy_county`;
   - calls `eotg_legacy_set_site_cooldown_effect` on it (4, 5 and 5 years, as v1);
   - fires the event.
3. **No passive discovery.** v1's only passive path was the Titan Exodus haven (`:43-58`). It is dropped (§4.2); discovery is by survey only.

### 3.2 Title gain (`eotg_on_title_gain_legacy_check`)

As v1 `:163-180`, plus NEW-5. The trigger: `scope:title` is a county, a known site and ready, **and** the title changed dynasty (`NOT = { scope:previous_holder ?= { dynasty = root.dynasty } }`; UNVERIFIED-VANILLA). Effect: save the county, set a 3-year site cooldown, then fire 0105.

### 3.3 Cooldown authority (the rule, copied from the Void)

- **The site cooldown** `eotg_legacy_site_cd` is set **only** at a firing point:
  - the yearly check (aftermath);
  - the title-gain check;
  - `eotg_legacy_fire_discovery_effect` (3 years, called by the survey and by the 0002/0003 options that reveal a site);
  - the family events' entry, set once by the discovery that fires them.
- **v1 set it in about 30 event options,** with 2 or 3 years by option (fate table §7, "cooldown moved"). v2 removes every option-level `eotg_se_legacy_cooldown`; the discovery sets 3 years before the family event fires.
- **No event trigger reads the site cooldown** except the aftermath and title-gain gates (lesson 5).
- **The ruler cooldowns:**
  - the aftermath flag, as above;
  - the survey's decision `cooldown = { years = 5 }`, which replaces the flag `eotg_legacy_survey_cooldown` (`eotg_legacy_decisions.txt:28,39`), as the Void Commune decision does.

---

## 4. Map-agnostic design

### 4.1 Seeding that works on any map (`eotg_on_game_start_legacy_seed`)

- **v1:**
  - seeded 7 named history characters' capitals (`eotg_legacy_on_actions.txt:189-201`, `eotg_se_legacy_seed_capital`, `eotg_legacy_effects.txt:148-166`);
  - and then, for 30% of independent rulers, one random held county (`:204-215`).

  The 7 characters break the temporary-map rule (audit HIGH row 2), and a share of *rulers* scales with how fragmented the map is.
- **v2:** density per **county**, so the share of the galaxy holding a site is the same on any map:
  - `every_county = { limit = { NOT = { has_variable = eotg_legacy_family } } random = { chance = eotg_legacy_seed_chance_value  eotg_legacy_seed_random_effect = yes } }`;
  - default `eotg_legacy_seed_chance_value = 3` (Q9), giving about 3 sites per 100 counties;
  - family weights 30 / 30 / 25 / 15, as v1 (`eotg_legacy_effects.txt:170-177`).
  - UNVERIFIED-VANILLA: `every_county` in a game-start on_action. v2 iterates rulers there (`eotg_cartel_on_actions.txt:52`); `every_county` is a vanilla global iterator, but no v2 file uses it yet.
- **Dynamic seeding** stays as v1: the survey's fallback events (0002, 0003) can seed a site in a held county that has none (§5 MED-1 adds the guard).
- **The 7 named capitals return as bookmark seeding after Gate 1,** owned by eotg-cartographer, in a bookmark-only effect that names title keys, not characters. **Taskboard note for the human:** "Legacies: re-add bookmark seeding of named sites (v1 had 7 history characters) once Gate 1 places them".

### 4.2 The Titan Exodus path is dropped

- **What it was:** the haven-reputation passive discovery (`eotg_legacy_on_actions.txt:43-58`, reading `eotg_exodus_haven_reputation` from `eotg_exodus_modifiers.txt:57`). Titan Exodus is in neither catalog column and not in v2 (audit HIGH row 3).
- **v2** keeps no Exodus code and no inert stub.
- **Taskboard note for the human:** "Legacies: re-add the Exodus-haven discovery path (10%/yr for a haven holding a hidden site) when Titan Exodus is lifted". Q4 asks the owner.

### 4.3 Nothing else is coupled

- No title, province, culture or faith key appears in the v1 effects, triggers, modifiers or events beyond the seeding above. The two faith-flavoured options (0040.c `zealous`, 0103) read traits, not faiths.
- `eotg_` prefix check: every v1 identifier is already prefixed. The renames in §6 are for v2 naming consistency (`eotg_mod_`, `eotg_opinion_`, `_effect`), not collisions.

---

## 5. Performance and every MED/LOW audit row

### 5.1 PERF (MED-3): the yearly pulse iterates held counties, not the sub-realm

- **v1 problem:** `every_sub_realm_county = { limit = { holder = root … } }` (`eotg_legacy_on_actions.txt:32,50,69,79,97,107,124,138`) walks a king's whole sub-realm every year to find the few counties they hold directly.
- **v2:** `every_held_title = { limit = { tier = tier_county … } }`, and the `any_`/`random_` forms of the same. These walk only the titles the ruler holds.
- **Precedent:** `common/on_action/eotg_frontier_on_actions.txt:35` (the yearly Frontier tick: `every_held_title` with `tier = tier_county`, "confirmed (verification V13)"); also `eotg_frontier_effects.txt:1810` (`every_held_title`) and `:2688,2706` (`any_held_title`).
- **Same for the triggers:** `eotg_legacy_holds_hidden_site` (v1 `eotg_st_holds_hidden_legacy`, `eotg_legacy_triggers.txt:66-71`) becomes `any_held_title = { tier = tier_county  eotg_legacy_is_hidden_site = yes }`.
- **Cost:** with about 3% of counties seeded, a ruler holding 5 counties tests 5 titles a year, not every county under them.

### 5.2 The other audit rows

| Audit row | v2 design |
|---|---|
| **MED-1** survey re-seed (`eotg_legacy_decisions.txt:56-58`) | The fallback's county pick becomes `random_held_title = { limit = { tier = tier_county  eotg_legacy_is_site = no } save_scope_as = eotg_legacy_county }`, which revives the dead `eotg_st_legacy_site` as `eotg_legacy_is_site`. If every held county already has a site, the fallback fires 0004 (nothing found) instead of 0002/0003. The seed effect itself also guards: `eotg_legacy_seed_effect` does nothing on a county that has `eotg_legacy_family` (belt and braces; the old modifier can never be orphaned). |
| **MED-2** 0104 re-fires at 0 (`eotg_legacy_effects.txt:102-112`) | `eotg_legacy_change_integrity_effect` saves the old value first (`save_temporary_scope_value_as = { name = eotg_legacy_integrity_before value = var:eotg_legacy_integrity }`; shape from `eotg_pmc_change_standing_effect`, which saves its amount the same way). After the clamp: **if** `scope:eotg_legacy_integrity_before > 0` and the new value is 0, set condition 6 and fire 0104 to the holder. A further loss at 0 does nothing. |
| **MED-3** perf | §5.1. |
| **MED-4** 0004 vignette (`eotg_legacy_events.txt:247-263`; invariant 5) | "Honest Geology" keeps its one option and gains a resource move. If the realm holds a known site, every known held site loses 5 attention ("the honest report cools the rumours"). Otherwise it sets the ruler flag `eotg_flag_legacy_survey_lead` (5 years), and the next survey's 0002 weight rises by 20 (a `modifier` in the decision's `random_list`, as v1 already uses at `:65-72`). The +10 prestige stays. |
| **LOW-1** `add_trait = wounded_1` (0003.a, `eotg_legacy_events.txt:171`) | `increase_wounds_effect = { REASON = attacked }` (v2 use: `eotg_augmentation_effects.txt:4341`), **guarded** by `NOT = { has_trait = wounded_3 }`, because vanilla kills a character it wounds at rank 3 (`20_health_effects.txt:1342-1351`, cited by the H1 harness). REASON key: UNVERIFIED-VANILLA beyond `attacked`. |
| **LOW-2** orphan heir (0021, `:611-619`) | Prefer an existing character: `random_pool_character = { province = root.capital_province  limit = { is_adult = yes  NOT = { exists = dynasty } } save_scope_as = eotg_legacy_heir }`; create from a new template `eotg_legacy_heir_template` only if none exists. Options b–d then leave a pool character as it was, not a fresh orphan. UNVERIFIED-VANILLA: `random_pool_character` with `province =`. |
| **LOW-3** dead definitions | `eotg_legacy_enclave_protected` (opinion): **cut** (nobody else is in 0011's scope to hold it). `eotg_st_legacy_site`: **revived** as `eotg_legacy_is_site` (MED-1). `eotg_st_holds_known_legacy`: **cut** (the yearly check iterates directly). |
| **LOW-4** the 8 `eotg_st_edu_*` helpers (`eotg_legacy_triggers.txt:74-126`) | They move to a shared file, `common/scripted_triggers/eotg_shared_education_triggers.txt`, as `eotg_education_<skill>_at_least_<n>`. Each **adds rank 5**, which 1.20 introduced (v1 stops at 4; v2 reads `education_learning_5` at `eotg_augmentation_decisions.txt:1138`). Where an option only needs "has this education", it uses `has_trait = education_<skill>` per `event_quality_v1.md` §13.1. |
| **LOW-5** redundant gold check | The survey's `is_valid` / `is_valid_showing_failures_only` `gold >= 50` (`eotg_legacy_decisions.txt:26,32`) are removed: `cost = { gold = 50 }` already blocks it, as every v2 decision does (`eotg_cartel_decisions.txt`). |
| **LOW-6** names to confirm | `monthly_county_control_decline_add`: confirmed by v2 use (`common/modifiers/eotg_aug_kingpin_modifiers.txt:82,95`). `on_title_gain` and `on_game_start_after_lobby`: confirmed (§3). |
| **NEW-1** (this audit) empty option | 0102.b "Leverage" (`eotg_legacy_events.txt:1252`) has no effect at all. v2: the vassal gains `eotg_opinion_legacy_concession_honored`, and the site gains −5 attention (the dispute settled quietly), so it differs from .c. |
| **NEW-2** (this audit) loc keys | v1 keys are `eotg_legacy_0002_desc` / `_title` / `_opt_<name>`; v2 uses the Void form `eotg_legacy.0002.t` / `.desc` / `.a`… (§6.3). |
| **NEW-4** (this audit) direct integrity writes | 0104.a and 0104.c set `eotg_legacy_integrity` directly to 20 and 40 (`eotg_legacy_events.txt:1374,1401`), bypassing the writer. v2: `eotg_legacy_change_integrity_effect = { AMOUNT = 20 }` / `40`, from 0. |
| **NEW-5** (sim, Appendix B) 0105 at every succession | `on_title_gain` fires on inheritance too, so 0105 fires for every known, ready site at every holder death (2.6 per site-century), and its reseal option ratchets sites into Sealed (63% of sites end Sealed). v2: the title-gain check also requires a dynasty change: `NOT = { scope:previous_holder ?= { dynasty = root.dynasty } }` (UNVERIFIED-VANILLA: `scope:previous_holder` is named in `eotg_cartel_on_actions.txt:36`; the `?=` form follows v2 use). Sealed falls to 26%, Governed rises to 54%. |
| **NEW-3** (this audit) the survey pick | The survey's discovery branch uses `random_held_title` with `eotg_legacy_is_hidden_site = yes` (as §5.1), replacing `random_sub_realm_county` + `holder = root`. |

---

## 6. Identifier table (v1 → v2)

### 6.1 Script objects

| v1 | v2 | Type | Change |
|---|---|---|---|
| on_yearly_playable hook | `yearly_playable_pulse` | vanilla hook | the dead hook replaced |
| `eotg_on_yearly_legacy_pulse` | `eotg_on_yearly_legacy_check` | on_action | `every_held_title`; cooldown at fire time |
| `eotg_on_title_gain_legacy_check` | same | on_action | |
| `eotg_legacy_seed_start` | `eotg_on_game_start_legacy_seed` | on_action | per-county density; no history characters |
| `eotg_se_legacy_seed` | `eotg_legacy_seed_effect` | effect | guard on an existing site |
| `eotg_se_legacy_make_known` | `eotg_legacy_make_known_effect` | effect | condition through the writer |
| `eotg_se_legacy_set_condition` | `eotg_legacy_set_condition_effect` | effect | **single writer** of condition |
| `eotg_se_legacy_refresh_modifier` | `eotg_legacy_refresh_modifier_effect` | effect | renamed modifiers |
| `eotg_se_legacy_add_attention` | `eotg_legacy_change_attention_effect` | effect | **single writer**; `clamp_variable` |
| `eotg_se_legacy_add_integrity` | `eotg_legacy_change_integrity_effect` | effect | **single writer**; crossing-only 0104 |
| `eotg_se_legacy_cooldown` | `eotg_legacy_set_site_cooldown_effect` | effect | called from firing points only |
| `eotg_se_legacy_fire_discovery` | `eotg_legacy_fire_discovery_effect` | effect | sets the 3-year site cooldown |
| `eotg_se_legacy_seed_capital` | not lifted | effect | history characters (§4.1) |
| `eotg_se_legacy_seed_random` | `eotg_legacy_seed_random_effect` | effect | |
| `eotg_st_legacy_site` | `eotg_legacy_is_site` | trigger | revived (MED-1) |
| `eotg_st_legacy_known_site` | `eotg_legacy_is_known_site` | trigger | |
| `eotg_st_legacy_hidden_site` | `eotg_legacy_is_hidden_site` | trigger | |
| `eotg_st_legacy_condition` | `eotg_legacy_condition_is` | trigger | `$CONDITION$` |
| `eotg_st_legacy_attention_at_least` | `eotg_legacy_attention_at_least` | trigger | `$VALUE$` |
| `eotg_st_legacy_integrity_at_most` | `eotg_legacy_integrity_at_most` | trigger | `$VALUE$` |
| `eotg_st_legacy_ready` | `eotg_legacy_site_ready` | trigger | reads `eotg_legacy_site_cd`; firing gates only |
| `eotg_st_holds_known_legacy` | cut | trigger | dead (LOW-3) |
| `eotg_st_holds_hidden_legacy` | `eotg_legacy_holds_hidden_site` | trigger | `any_held_title` |
| `eotg_st_edu_learning_2` … `eotg_st_edu_diplomacy_3` (8) | `eotg_education_<skill>_at_least_<n>` in `eotg_shared_education_triggers.txt` | trigger | shared, rank 5 added (LOW-4) |
| `eotg_decision_survey_legacies` | `eotg_decision_legacy_survey` | decision | `cooldown` block; no redundant gold |
| `eotg_legacy_metropolis_governed` | `eotg_mod_legacy_metropolis_governed` | county modifier | |
| `eotg_legacy_archive_governed` | `eotg_mod_legacy_archive_governed` | county modifier | |
| `eotg_legacy_works_governed` | `eotg_mod_legacy_works_governed` | county modifier | |
| `eotg_legacy_hellpocket_warded` | `eotg_mod_legacy_planar_warded` | county modifier | name pending Q2 |
| `eotg_legacy_extracted_site` | `eotg_mod_legacy_extracted_site` | county modifier | |
| `eotg_legacy_sealed_site` | `eotg_mod_legacy_sealed_site` | county modifier | |
| `eotg_legacy_unstable_site` | `eotg_mod_legacy_unstable_site` | county modifier | |
| `eotg_legacy_loyal_enclave` | `eotg_mod_legacy_loyal_enclave` | county modifier | |
| `eotg_legacy_grim_rumors` | `eotg_mod_legacy_grim_rumours` | county modifier | Canadian spelling in the key too |
| `eotg_legacy_arsenal` | `eotg_mod_legacy_arsenal` | character modifier | |
| `eotg_legacy_warden` | `eotg_mod_legacy_warden` | character modifier | |
| `eotg_legacy_claim_defied` | `eotg_opinion_legacy_claim_defied` | opinion | |
| `eotg_legacy_taxed_concession` | `eotg_opinion_legacy_taxed_concession` | opinion | |
| `eotg_legacy_concession_honored` | `eotg_opinion_legacy_concession_honoured` | opinion | Canadian spelling |
| `eotg_legacy_enclave_protected` | cut | opinion | dead (LOW-3) |
| none | `eotg_legacy_heir_template` | character template | LOW-2 fallback (shape: `eotg_pmc_operator_template`) |
| none | `eotg_legacy_survivor_template` | character template | 0003.a (v1 inline `create_character` with `age = 32`) |
| none | `eotg_legacy_seed_chance_value` (3), `eotg_legacy_attention_decay_value` (−2), `eotg_legacy_aftermath_rival_chance_value` (25), `_vassal_chance_value` (20), `_cult_chance_value` (15), `eotg_legacy_extracted_drain_value` (−1, Q8), `eotg_legacy_attention_floor_value` (25, Q10), `eotg_legacy_rival_gate_value` (25, Q10) | script values | named, so the sim reads them and the owner can tune them |

### 6.2 Variables, flags and scopes

| v1 | v2 | Change |
|---|---|---|
| `eotg_legacy_family`, `_known`, `_condition`, `_integrity`, `_attention` (county) | same | the writers above |
| `eotg_legacy_cooldown` (county, timed) | `eotg_legacy_site_cd` | named like the Frontier's `eotg_frontier_event_cd` |
| `eotg_legacy_aftermath_recent` (ruler flag) | `eotg_flag_legacy_aftermath_cd` | `eotg_flag_` prefix, as the Void |
| `eotg_legacy_survey_cooldown` (ruler flag) | removed | decision `cooldown` block |
| none | `eotg_flag_legacy_survey_lead` (ruler flag, 5 years) | MED-4 |
| scopes `eotg_legacy_county`, `eotg_legacy_heir`, `eotg_legacy_survivor` | same | already prefixed |

### 6.3 Events and loc keys

- **Namespace:** `eotg_legacy`, with the 16 ids unchanged: 0002, 0003, 0004, 0010, 0011, 0020, 0021, 0030, 0031, 0040, 0041, 0101, 0102, 0103, 0104, 0105.
- **File:** `events/eotg_legacy_events.txt`. Keep one file, or split it, as the Void split, into `eotg_legacy_survey.txt` (0002–0004), `eotg_legacy_family.txt` (0010–0041) and `eotg_legacy_aftermath.txt` (0101–0105).
- **Loc keys:**
  - `eotg_legacy_0010_title` becomes `eotg_legacy.0010.t`;
  - `_desc` becomes `.desc`;
  - `eotg_legacy_0010_opt_restore` becomes `eotg_legacy.0010.a`, and so on in option order (the fate table gives each letter).
- **Modifier, opinion and decision loc** follow §6.1.

---

## 7. Event and option fate table (all 16 v1 events)

**Fates:**
- **lifted:** effects unchanged, apart from renames and the global changes below;
- **fixed:** the script changes;
- **reworded:** the loc changes so it matches the effect, or for canon;
- **dropped:** nothing is dropped.

**Global changes, all events (fixed):**
- every option-level `eotg_se_legacy_cooldown` is removed ("cooldown moved", §3.3);
- `eotg_se_legacy_*` / `eotg_st_*` become the v2 names;
- `eotg_st_edu_*` become the shared triggers;
- `has_trait = <personality>` gates gain the `trait =` icon and a stress entry (event_quality §13.1 step 5);
- an `override_background` is added from `common/event_backgrounds/` (`eotg_bg_cavern`, `eotg_bg_vault`, `eotg_bg_council` or `eotg_bg_barren_world`).

**Option letters** are in v1 order.

| Event | Option | Fate | Notes |
|---|---|---|---|
| **0002** The Map That Contradicts the Sky (survey) | desc | reworded | §8 (keeps "Second Era"; drops the dash) |
| | a excavate | fixed | Seeds only a county **without** a site (MED-1); the reveal goes through `fire_discovery` (which sets the 3-year cooldown). The v1 option-level cooldown is moved. |
| | b recalculate [learning edu ≥ 2] | fixed | The seed guard; shared education trigger |
| | c sell [greedy] | lifted | `trait = greedy` |
| | d burn [paranoid] | lifted | `trait = paranoid` |
| **0003** The Surveyors Have Stopped Reporting | desc | reworded | |
| | a relief [brave or martial edu ≥ 2] | fixed | `increase_wounds_effect` guarded against `wounded_3` (LOW-1); the survivor comes from `eotg_legacy_survivor_template` |
| | b recover [compassionate] | lifted | |
| | c abandon [callous] | lifted | `eotg_mod_legacy_grim_rumours` |
| | d investigate [intrigue edu ≥ 3] | lifted | |
| | e wait | fixed | The seed guard (MED-1) |
| **0004** Honest Geology | a | fixed | **Invariant 5 (MED-4):** −5 attention on known held sites, or `eotg_flag_legacy_survey_lead` |
| **0010** The Street of Foreign Suns (Metropolis) | desc | reworded | "eight centuries" and "Confluence" (§8) |
| | a restore | fixed | Cooldown moved; fires 0011 |
| | b concessions [stewardship edu ≥ 2] | fixed | Cooldown moved |
| | c sell [greedy] | fixed | Cooldown moved |
| | d monument [ambitious] | fixed | Cooldown moved |
| | e seal | fixed | Cooldown moved |
| **0011** What the District Wants | a protect | lifted | `eotg_mod_legacy_loyal_enclave` 30 years |
| | b refuse | lifted | |
| | c reform | lifted | |
| | d press | lifted | |
| **0020** The Court in the Vault (Archive) | desc | reworded | |
| | a custody [learning edu ≥ 2] | fixed | Cooldown moved; fires 0021 |
| | b witness [diplomacy edu ≥ 2] | fixed | Cooldown moved |
| | c mandate [ambitious] | fixed | Cooldown moved |
| | d copy [cynical or intrigue edu ≥ 3] | fixed | Cooldown moved; one personality gate (§13.1) |
| | e catalogue | fixed | Cooldown moved |
| **0021** The Archive Names an Heir | immediate | fixed | Pool character first, template fallback (LOW-2) |
| | desc | reworded | "survived the Confluence" (§8) |
| | a recognize | lifted | Adds the heir to court |
| | b instrument | lifted | |
| | c publish [just] | lifted | |
| | d suppress [arbitrary] | lifted | |
| **0030** The Foundry Still Burns (Relic Works) | desc | reworded | "eight centuries deep" (§8) |
| | a audit [stewardship edu ≥ 2] | fixed | Cooldown moved |
| | b arm [martial edu ≥ 2] | fixed | Cooldown moved |
| | c output [greedy] | fixed | Cooldown moved (v1 used 2 years here) |
| | d slow | fixed | Cooldown moved |
| | e seal | fixed | Cooldown moved |
| **0031** What the Works Produce | a–f | lifted | Six condition-3 options (a exclusive, b divide, c charter [diplomacy edu ≥ 3], d assure [intrigue edu ≥ 2], e relief, f burnout); `eotg_opinion_legacy_concession_honoured` |
| **0040** The Infernal Ledger (Planar Pocket) | title, desc | reworded | "Hell's administrative layers" and "Confluence" (§8); title pending Q2 |
| | a bargain | fixed | Cooldown moved; fires 0041 |
| | b audit [stewardship edu ≥ 3] | fixed | Cooldown moved |
| | c reject [zealous] | fixed | **v1 writes condition 5 then 6 and the cooldown twice.** v2 makes one condition write (6, unstable) and no cooldown. |
| | d warden [brave] | fixed | Cooldown moved; `eotg_mod_legacy_warden` |
| | e seal | fixed | Cooldown moved |
| **0041** The Debt Comes Due | a gold | lifted | |
| | b kind | lifted | `change_development_level = -1` |
| | c defy | fixed | Cooldown moved |
| **0101** The Rival's Archaeologist | a negotiate | lifted | |
| | b expose | fixed | v1 adds +50 and then −25 prestige in one option; v2 makes it a single +25 |
| | c defy | lifted | `eotg_opinion_legacy_claim_defied` |
| **0102** The Concession's Beneficiaries (powerful vassal) | a tax | lifted | |
| | b leverage | fixed | **Empty in v1 (NEW-1):** now vassal +opinion and attention −5 |
| | c accept | lifted | |
| **0103** The Cult Beneath the Monument | a purge | lifted | |
| | b infiltrate [intrigue edu ≥ 2] | lifted | |
| | c tolerate | lifted | |
| **0104** The Exhausted Legacy | fired by | fixed | Fires on the crossing only (MED-2) |
| | a stabilize | fixed | Cooldown moved; the direct integrity set (20) goes through the writer (NEW-4) |
| | b abandon | fixed | Cooldown moved |
| | c deeper [learning ≥ 16] | fixed | Cooldown moved; the direct integrity set (40) goes through the writer (NEW-4) |
| **0105** The Seam Changes Hands | a honour | lifted | |
| | b strip | lifted | |
| | c reseal | fixed | Cooldown moved |

**Counts:** 16 events, 62 options. None dropped; 32 options fixed, 30 lifted (plus 0021's immediate and 0104's trigger, both fixed). Option loc is reworded wherever its desc is.

---

## 8. Canon and loc plan

### 8.1 Rulings the text builds to (pending owner, Q2 and Q3)

- **Sites are pre-Grip.**
  - The ERAS rule (REVIEW_866.md, Draft errata) places the **Second Era before the Grip** and the Third Era from 0 AG.
  - **v1's "Second Era" wording is therefore consistent** with pre-Grip sites. The audit's contradiction (HIGH row 4) read the SETTING LORE body's dating (Second Era ~131–850 AG), which SOURCE PRECEDENCE now outranks.
  - **Keep "Second Era".**
- **"Eight centuries" is wrong** at 866 AG (the Grip was 866 years ago; REVIEW Settled item 6).
  - Use "nearly nine centuries". It holds from 801 to 900 AG, so it covers the 866 bookmark and later starts in that window.
  - Never hard-code "866 years": that goes stale, the Void's lesson.
- **"The Confluence" has no canon source** (REVIEW item 6).
  - **Default (Q2): drop it as a proper noun and say what canon says: the Grip fused these places.**
  - The system's player-facing name becomes "Grip Legacies"; internal keys keep `eotg_legacy_`.
  - If the vault confirms "the Confluence", restore it with a source.
- **"Hell's administrative layers" and "infernal" have no canon source.**
  - The Rift is canon, but it is a separate god-prison plane (REVIEW_866.md:35); don't conflate the two.
  - **Default (Q2):** "a fragment of another plane", with the family name "Planar Pocket".

### 8.2 Every flagged line (file:line in `OLD PROJECT VERSION/localization/english/eotg_legacy_l_english.yml`)

| Line | Key | Problem | Proposed rewrite (sense; exact strings in Appendix A) |
|---|---|---|---|
| 3–8 | header comments | "Confluence", "Hell" | rewrite the comment |
| 13 | `eotg_decision_survey_legacies` | "Confluence" | "Survey for Grip Legacies" |
| 14 | `…_desc` | "The Confluence", "eight centuries", dash | "The Grip left every settled system stitched together… buried under nearly nine centuries of ordinary life." |
| 15 | `…_tooltip` | "Confluence sites" | "…for sites the Grip buried" |
| 21 | `eotg_legacy_0002_desc` | dash | keep "Second Era"; drop the dash |
| 41 | `eotg_legacy_0010_desc` | "eight centuries", "Confluence", dash | "…vapour lamps that failed nearly nine centuries ago… folded into our ground by the Grip…" |
| 58 | `eotg_legacy_0020_desc` | dash | "Second Era" kept |
| 66 | `eotg_legacy_0021_desc` | "survived the Confluence", "rumors", dashes | "survived the Grip"; "rumours" |
| 74 | `eotg_legacy_0030_desc` | "eight centuries deep", "meters", dash | "nearly nine centuries deep"; "metres" |
| 91–93 | 0040 header, `_title`, `_desc` | "Hell", "infernal", "Confluence" | "another plane"; title "The Foreign Ledger" (pending Q2) |
| 135 | `…metropolis_governed_desc` | "eight centuries" | "nearly nine centuries" |
| 137, 139, 155 | archive, works, arsenal descs | "Second Era" (ok); "armor" | "armour" |
| 140–141 | `…hellpocket_warded` + desc | "infernal fragment" | "Warded Seam": "The fragment of another plane…" |
| 143, 145, 149 | extracted, sealed, enclave descs | "Confluence site" / "from the Confluence" | "The Grip-buried site here…"; "recovered from beneath the ground" |
| 147 | `…unstable_site_desc` | (canon ok) | keep |
| 150 | `…grim_rumors` | "Rumors" | "Grim Rumours" |
| 156–157 | `…warden` + desc | "infernal gate" | "Warden of the Seam"; "a contained gate to another plane" |
| pitch `:5` | (doc) | "the Confluence" | the pitch doc is reference only; no change |

**Also across all 127 keys:**
- remove every em dash (v2 house rule: no dashes);
- US to Canadian spelling: honor → honour, armor → armour, rumors → rumours, meters → metres, vapor → vapour, recognize stays;
- `[eotg_legacy_county.GetName]` stays bare (invariant 6).

### 8.3 Register and voice

- **The register is physical and archaeological:**
  - instruments, strata, dust, lamps, ledgers, the weight of old machinery;
  - things that are *there* and can be measured.
- **It is not the Void's register.** The Void is an outside presence at the edge of hearing (Void spec §5 R10). A Legacy never whispers, presses or offers; its strangeness is a measurable wrongness: the wrong stars, the wrong alphabet, a foundry still warm.
- **It is not the cybernetic register** either. No inner voice and no forecast: the ERRATA CYBERNETIC "VOICE" rule.
- **Voice mix** (`event_quality_v1.md` §12.1, R1), about 60% first person, 35% third and 5% second:
  - main descs open in first person, present tense ("Beneath [eotg_legacy_county.GetName] my excavators break into a boulevard.");
  - aftermath descs about rivals and vassals can be neutral (third person);
  - second person only in NPC speech and the decision text.
  - v1 is mostly second person ("your antechamber"), so the localizer converts it.
  - One NPC line per desc at most, in straight double quotes, with `#EMP` at most once per event.
- **No medieval drift:**
  - "smith" becomes "machinist";
  - "fields" becomes "the plain" or "the ground";
  - "antechamber" becomes "the outer office";
  - "badland" is ok.
- **Never hard-code "knight"** (none in v1).

---

## 9. Test list (V-L1…), each a harness decision later

| ID | Setup (harness) | Assert (downstream, not the setup) |
|---|---|---|
| V-L1 | Game start on any map (the temporary map) | about 3% of counties have `eotg_legacy_family`; no county seeded twice; none named by a character id |
| V-L2 | Seed a held county (effect), run the survey effect | the site is known, condition 2, 3-year site cooldown, and the family event fires within 15 days |
| V-L3 | Survey when every held county has a site | 0004 fires (not 0002/0003); no `eotg_legacy_family` changes (MED-1) |
| V-L4 | Known site, attention 10, run the yearly pulse twice | attention 6 (−2 a year); never below 0 |
| V-L5 | Integrity 5, change −10, then −10 again | 0104 fired exactly once; condition 6; unstable modifier only (MED-2) |
| V-L6 | Set condition 3 for each family | exactly the matching governed modifier; switching to 4 removes it |
| V-L7 | Attention 60, site ready, aftermath flag clear, pulse with the 0101 chance forced (override) | `eotg_flag_legacy_aftermath_cd` and the site cooldown set by the **on_action**; the 0101 event pending |
| V-L8 | The same, with the flag already set | nothing fires and no cooldown changes |
| V-L9 | Grant a known, ready site's county to another ruler | 0105 fires to the new holder; 3-year site cooldown |
| V-L10 | 0003.a on a ruler at `wounded_2` | wound rank 3 at most; never death (LOW-1) |
| V-L11 | 0021 with an adult dynasty-less pool character in the capital | no new character created (LOW-2); else one from the template |
| V-L12 | 0004 with a known held site | every known held site −5 attention (MED-4) |
| V-L13 | 0004 with no known site | `eotg_flag_legacy_survey_lead` set; the next survey's 0002 weight +20 (LOOK) |
| V-L14 | A ruler holding 5 counties in a 200-county sub-realm | the yearly pulse touches only held titles (LOOK: script profiler) |
| V-L15 | 0102.b | the vassal gains the honoured opinion; attention −5 (NEW-1) |
| V-L16 | 0040.c | condition 6 once; no site cooldown written by the event |
| V-L17 | Survey twice | blocked by the decision `cooldown` (5 years); no gold check duplicated in the tooltip |
| V-L19 | Inherit a known site within the dynasty | 0105 does not fire (NEW-5); a non-dynasty grant does fire it |
| V-L20 | An Extracted site at integrity 3, three yearly pulses | integrity 0 after the third; 0104 once (Q8, MED-2) |
| V-L21 | Attention 30 on a known site, ten pulses | it stops at 25 (the floor); 0101 can roll (Q10) |
| V-L18 | Loc | every key resolves; no "Confluence", "Hell", "eight centuries", dash, `[scope:` or US spelling |

---

## 10. Owner questions (each with a recommended default)

- **Q7. Is Legacies mod-exclusive,** so it can be built and tested on the temporary map before Gate 1? **Default: yes.** After §4 it depends on no map data.
- **Q2. "The Confluence" and "Hell".** **Default:**
  - drop "the Confluence" for "the Grip", and name the system "Grip Legacies" in player text;
  - make the fourth family "Planar Pocket" ("another plane", never Hell, never the Rift).
  - Send both terms to the vault.
- **Q3. Pre-Grip dating.** **Default:** sites are pre-Grip; "Second Era" stays (ERAS); "eight centuries" becomes "nearly nine centuries".
- **Q4. Exodus re-entry.** **Default:** drop the haven path now; a taskboard note re-adds it, with its 10%/yr, when Titan Exodus is lifted.
- **Q9. Seeding density.** **Default:** `eotg_legacy_seed_chance_value = 3` (about 3% of counties).
  - Sim (Appendix B): 82% of seeded sites are found within 25 years by AI holders (median 10 years), and at once by players.
  - For a player, **game-start density matters less than the survey's own seeding.** A survey that finds nothing creates a new site 20% of the time, about 4 new sites per player-century at one survey every 5 years.
  - If players should not accumulate sites, cut 0002.a's seeding branches (30 + 25 of 100) in half. That is a value change; the owner decides.
- **Q8 (new). Integrity has no passive drain**, so an Extracted site keeps its tax bonus forever, and in the sim no site ever reaches 0 integrity from play: 0104 fires 0.00 times per site-century. **Default (revised by the sim): −1 a year on condition 4 (Extracted)**, a value (`eotg_legacy_extracted_drain_value`) read in the yearly check.
  - Result: 12% of sites reach 0, a median 59 years after discovery.
  - Extracted ends at 1% rather than 11%, and Unstable at 9%. Exploitation now has the cost the pitch describes.
  - −2 is too fast (16.5% reach 0 in a median 34 years).
- **Q10 (new). The rival claim (0101) never fires,** at 0.0004 per site-century. Attention peaks at discovery, then the 3-year discovery cooldown blocks every aftermath while −2 a year decay erodes it, so attention ≥ 50 is never met when a roll is allowed; the median attention on a known site is 0.
  - **Default:** gate 0101 at **25** (Rumoured), and stop the decay at 25 once a site has reached it (a floor, read from `eotg_legacy_attention_floor_value`). Together these give 0101 0.61 per site-century.
  - Either change alone does little: gate 25 alone gives 0.06, and the floor alone gives 0.
  - The Renowned ×1.5 weight (old Q10) is moot until attention can reach 75; it is dropped.

---

## 11. Proposed events: OWNER APPROVAL REQUIRED

None are part of the lift. The pitch describes beats v1 never built. They are listed so they are not lost; **none is to be built without approval:**
- The Boundary Moves Overnight (survey);
- The Memory That Refuses to Be Read (Archive);
- The Concession War, as a war beat;
- the War Graveyard family (The Arsenal Beneath the Field, The Dead Fleet's Oath);
- The Gate Wants a Warden (Planar);
- the Living Legacy family (The People Below the Ruins, The Child of Two Worlds);
- the Ecological Graft family (The Forest Eats the Bulkhead).

---

## 12. Numbers (the sim)

`docs/tools/sim/models/legacies.py` (this branch) reads the v1 option and on_action amounts through `pdx_read.py` and models the v2 design: per-county seeding, survey-only discovery, the −2 a year decay, the aftermath chances, the crossing-only 0104, and title-gain 0105.

Its results are in Appendix B and in `docs/qa/mechanics_sim_2026-11-03/legacies_v2_sim.md`. They justify the revised defaults Q8, Q9 and Q10 and the finding NEW-5.

---

## Appendix A: replacement loc for every flagged line (draft for the localizer)

These are exact strings with the v2 keys (§6.3), written to §8:
- first person in the main descs, neutral in modifier text;
- no dashes, Canadian spelling, bare `[x.GetName]`;
- "Second Era" kept (ERAS); "nearly nine centuries"; "the Grip" for "the Confluence"; "another plane" for "Hell" (the Q2 and Q3 defaults).

They go into a UTF-8-with-BOM `localization/english/eotg_legacy_l_english.yml` at build time. This markdown block carries no BOM. The v1 line each replaces is in the comment above it. Keys not listed here are reworded at build time for voice, dashes and spelling only.

```yaml
 # v1 :13
 eotg_decision_legacy_survey:0 "Survey for Grip Legacies"
 # v1 :14
 eotg_decision_legacy_survey_desc:0 "The Grip left every settled system stitched together from wreckage: districts, machines and archives from worlds that no longer exist, buried under nearly nine centuries of ordinary life. A proper survey of the domain may find what the ground has been keeping."
 # v1 :15
 eotg_decision_legacy_survey_tooltip:0 "Commission a survey of your held counties for sites the Grip buried"
 # v1 :21 (Second Era kept; the dash removed; first person)
 eotg_legacy.0002.desc:0 "My survey team returns not with ore samples but with a star chart. It is Second Era work, beautifully drawn and meticulously wrong: its route network will not match the present heavens however my navigators turn it. One of its terminals falls squarely inside [eotg_legacy_county.GetName], on ground the maps of the living call empty."
 # v1 :41
 eotg_legacy.0010.desc:0 "Beneath [eotg_legacy_county.GetName] my excavators break into a boulevard. Shopfronts stand intact under vapour lamps that failed nearly nine centuries ago. The architecture belongs to no local tradition. The signage reads right to left in an alphabet my archivists cannot place, and the orrery in the plaza models a star system that is not ours. An entire district of a vanished city-world, folded into this ground by the Grip, has been waiting all this time under the plain."
 # v1 :58
 eotg_legacy.0020.desc:0 "The vault under [eotg_legacy_county.GetName] holds no treasure. It holds paperwork, which may be worse: the complete legal apparatus of a dead Second Era polity. Land registers, genealogies, treaties, and a succession protocol still formally in force, waiting for claimants from a world that no longer exists. I understand at once that whoever keeps these records decides what they mean, and that whoever decides what they mean inherits a dead court's authority, and its enemies."
 # v1 :66 (the heir's speech replaces the second-person close)
 eotg_legacy.0021.desc:0 "My genealogists were thorough, and thoroughness has consequences. The dead court's succession protocol, applied to the living, produces a name: [eotg_legacy_heir.GetName], whose line survived the Grip without knowing what it carried. The finding is defensible. The finding is dangerous. And the finding is standing in my outer office, having heard the rumours first. "I did not ask for this," [eotg_legacy_heir.GetSheHe] says. "But I am not going to refuse it.""
 # v1 option :0021 instrument (dash)
 eotg_legacy.0021.b:0 "Support [eotg_legacy_heir.GetHerHim] at arm's length, on my terms."
 # v1 :74
 eotg_legacy.0030.desc:0 "Eight hundred metres under [eotg_legacy_county.GetName], my survey lights fall on a foundry floor that never cooled. Second Era fabricators idle at their stations, feedstock hoppers half full, a maintenance queue nearly nine centuries deep and patiently waiting. It could produce again. Its safety systems were engineered for a workforce, an atmosphere and a world that no longer exist, details the first eager concession bidder will not mention."
 # v1 :92 (title pending Q2)
 eotg_legacy.0040.t:0 "The Foreign Ledger"
 # v1 :93
 eotg_legacy.0040.desc:0 "The sealed badland in [eotg_legacy_county.GetName] is not a wasteland. Past the heat-shimmer boundary there are roads, tollhouses and a working market: a fragment of another plane's administration, folded into this ground by the Grip and carrying on with commendable procedure. Its clerks have noticed the new management, and they have prepared terms. The ledger they set before me is old, precise and patient, and it is signed at the bottom by everything it has ever owned."
 # v1 :97 (reject; "blasphemy" is a stance, not a canon claim: kept)
 eotg_legacy.0040.c:0 "This is blasphemy, and blasphemy burns."
 # v1 :135
 eotg_mod_legacy_metropolis_governed_desc:0 "A recovered district of a vanished city-world lives again beneath this county, its streets lit for the first time in nearly nine centuries."
 # v1 :137 (unchanged in sense; key renamed)
 eotg_mod_legacy_archive_governed_desc:0 "A Second Era archive is kept here under a proper chain of custody, its records lending weight to the county's law."
 # v1 :139
 eotg_mod_legacy_works_governed_desc:0 "Second Era industry runs beneath this county under audited concessions, producing wealth at a sustainable burn."
 # v1 :140-141 (name pending Q2)
 eotg_mod_legacy_planar_warded:0 "Warded Seam"
 eotg_mod_legacy_planar_warded_desc:0 "The fragment of another plane beneath this county is contained under permanent watch, and the watchers are taken seriously."
 # v1 :143
 eotg_mod_legacy_extracted_site_desc:0 "The site the Grip buried here is being stripped for value faster than it can ever be restored."
 # v1 :145 (the dash removed)
 eotg_mod_legacy_sealed_site_desc:0 "The site the Grip buried here is closed, forbidden and quiet. For now."
 # v1 :149
 eotg_mod_legacy_loyal_enclave_desc:0 "A community recovered from beneath the ground holds protected status here, and repays it in loyalty."
 # v1 :150-151
 eotg_mod_legacy_grim_rumours:0 "Grim Rumours"
 eotg_mod_legacy_grim_rumours_desc:0 "Abandoned surveyors, sealed galleries, songs after dark: the county repeats stories its lord would prefer it forgot."
 # v1 :154-155
 eotg_mod_legacy_arsenal_desc:0 "Second Era fabricators turn out arms and armour for the levies, equipment no living machinist could copy."
 # v1 :156-157 (name pending Q2)
 eotg_mod_legacy_warden:0 "Warden of the Seam"
 eotg_mod_legacy_warden_desc:0 "This ruler personally holds the wardenship of a contained gate to another plane. The honour is immense. So is the weight."
```

**Lore checks for eotg-lore-keeper:**
- "Second Era" as pre-Grip (ERAS);
- "nearly nine centuries";
- "another plane", which must not read as the Rift (a separate god-prison plane);
- the 0021 heir line, which may assume nothing beyond the trigger: any adult, so it uses `GetSheHe`.


---

## Appendix B: the sim (v2 design, v1 numbers)

**Run:** `python docs/tools/sim/models/legacies.py --md docs/qa/mechanics_sim_2026-11-03/legacies_v2_sim.md` (about 1 minute; numpy only). It runs 20,000 sites × 100 years per scenario, seed 20261103. The full tables are in that file.

**Model:** site-centric, one site per holder, which is the common case at 3% density. **It reads from the v1 script:**
- every option's AI weight, gate, attention and integrity amounts, condition writes, direct integrity sets, `random_list` branches and follow-up events;
- the survey's `ai_will_do`, its check interval and the fallback weights;
- the yearly pulse's decay, aftermath chances, site cooldowns and flag years;
- the seed weights and the start integrity.

**ASSUMPTIONS:**
- a gated option is open to the holder 30% of the time;
- a powerful vassal is present 50% of the time;
- players survey every 5 years;
- in the 0105 what-if, 90% of holder deaths are inheritance within the dynasty;
- AI weights also stand in for players' choices.

| Finding | Evidence (AI holder unless noted) | Spec change |
|---|---|---|
| **B1. Discovery is slow for the AI and instant for players** | AI holders survey 6.9% a year (read), so 47% / 82% / 97% of sites are found by 10 / 25 / 50 years, median 10. A player finds every site in the first survey. | None. Q9 notes that player-side seeding comes from the survey. |
| **B2. Sealed is the absorbing state** | 63% of sites end Sealed (Governed 26%, Extracted 11%). 0105 fires 2.6 times per site-century, once per succession, and its reseal option sends a site to Sealed, which nothing but 0104.c leaves. | **NEW-5:** 0105 only on a dynasty change. Sealed 26%, Governed 54%. |
| **B3. Integrity never runs out** | 0% of sites reach 0 in 100 years, and 0104 fires 0.00 per site-century, so Extracted is a free +20% tax forever. | **Q8:** −1 a year on Extracted. 12% reach 0 (median 59 years); Extracted 1%. |
| **B4. The rival claim is dead** | 0101 fires 0.0004 per site-century; the median attention on a known site is 0. | **Q10:** gate 25 plus a floor at 25 gives 0.61 per site-century. |
| **B5. Survey seeding dominates for players** | 0.20 new sites per survey that finds nothing (0002 40% × 0.43 + 0003 20% × 0.15, read), so about 4 per player-century. | **Q9** note (an optional value change). |

**The recommended package** (NEW-5, Q8 at −1, Q10's gate 25 with floor 25), AI holder, at the end of 100 years:

| Condition | Share of sites |
|---|---|
| Governed | 54% |
| Extracted | 2% |
| Sealed | 27% |
| Unstable | 18% |

- 17% of sites reach 0 integrity (median 69 years);
- aftermath events run 1.12 per site-century;
- 0101 fires 0.35 per site-century.

**Unstable at 18% is the cost of exploitation, now visible.** If that is too high, use drain −1 only below integrity 50 (a condition on the value).
