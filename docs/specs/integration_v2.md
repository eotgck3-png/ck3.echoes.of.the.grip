# Integration v2: character memories (INT4) and game rules (INT5)

Architect, 2026-10-20. Source: `docs/qa/system_investigation_2026-10-18/REPORT.md` §5, ranks 4 and 5. Sibling specs, which this one does not duplicate: `integration_v1.md` (alerts, game concepts) and `investigation_rulings_2026-10-18.md` (secrets for S1/S4).

`G` = `D:/SteamLibrary/steamapps/common/Crusader Kings III/game` (1.20.1.1). Every repository line number below was read on 2026-10-20. If a file has moved since then, re-anchor by the quoted text, not by the number.

---

## 1. Purpose and gate

**INT4** gives the biggest cybernetics and Frontier beats a vanilla **character memory**. The memory shows in the vanilla memory UI, and vanilla's memory readers (feasts, coronations) can pick it up. Later events can also read it back. INT4 adds no events or options. It adds `create_character_memory` to scripted effects that existing events, decisions and on_actions already call.

**INT5** adds three **game rules**: cybernetics event frequency, AI augmentation uptake, and Frontier difficulty. The owner and testers can then tune the systems from the lobby without editing script.

**Gate:** both batches are exempt from the Gate 1 hold. They touch only cybernetics (a mod-exclusive system, 2026-10-02) and Frontier, and neither batch names a title, province, character, culture or faith. Region names reach loc through a memory variable. **Not blocked.**

## 2. Signature resource

There is no new resource. Each batch is tied to the existing ones:

- **INT4:** every memory is created at the moment a signature resource crosses a defining line. Those lines are:
  - the `eotg_cybernetics` tier and XP;
  - `eotg_fracture_risk` reaching the cascade;
  - `eotg_aug_residue` starting (Seamless);
  - `eotg_frontier_progress` reaching 100;
  - `eotg_frontier_strain` reaching failure, or a chosen abandonment;
  - the Frontier state starting.

  The memory is the record of that crossing. It is not a vignette, because it has no window of its own.
- **INT5:** two rules scale a resource directly. Frontier difficulty scales the yearly `eotg_frontier_progress` gain and the quiet-year `eotg_frontier_strain` ease. The two cybernetics rules scale how often resource-moving pool events fire.

## 3. Identifier table

| Type | Exact name | Owner | Notes |
|---|---|---|---|
| memory type | `eotg_aug_initiated_memory` | scripter | |
| memory type | `eotg_aug_overclocked_memory` | scripter | the threshold: Enhanced → Overclocked |
| memory type | `eotg_aug_cascade_memory` | scripter | the fracture |
| memory type | `eotg_aug_seamless_memory` | scripter | Total Integration |
| memory type | `eotg_aug_excised_memory` | scripter | endgame survivor |
| memory type | `eotg_aug_restrained_memory` | scripter | endgame: abdication, on the old ruler |
| memory type | `eotg_aug_locked_wing_memory` | scripter | endgame: abdication, on the successor |
| memory type | `eotg_frontier_founded_memory` | scripter | |
| memory type | `eotg_frontier_settled_memory` | scripter | completion |
| memory type | `eotg_frontier_abandoned_memory` | scripter | failure or choice |
| memory category | `eotg_cybernetics`, `eotg_frontier` | scripter | Free strings (`_character_memories.info:3`). Mixed with vanilla categories (§5.1). |
| memory participant tag | `eotg_successor`, `eotg_predecessor`, `eotg_founder` | scripter | local to the type, prefixed anyway |
| memory variable | `eotg_region` (county title), `eotg_failed` (flag) | scripter | Variables are for non-character references (`.info:38-41`). |
| saved scope (temporary) | `eotg_mem_region`, `eotg_mem_founder`, `eotg_mem_below_oc` | scripter | `save_temporary_scope_as` only |
| game rule | `eotg_aug_event_frequency` | scripter | |
| setting | `eotg_aug_events_normal` (default), `eotg_aug_events_low`, `eotg_aug_events_high`, `eotg_aug_events_off` | scripter | Setting keys are what `has_game_rule` reads, so they must be globally unique. |
| game rule | `eotg_aug_ai_uptake` | scripter | |
| setting | `eotg_aug_ai_uptake_normal` (default), `eotg_aug_ai_uptake_low`, `eotg_aug_ai_uptake_high` | scripter | |
| game rule | `eotg_frontier_difficulty` | scripter | |
| setting | `eotg_frontier_difficulty_normal` (default), `eotg_frontier_difficulty_easy`, `eotg_frontier_difficulty_hard` | scripter | |
| game rule category | `eotg` | scripter | The dropdown reads categories from data (`G/gui/game_rules.gui:103`). |
| scripted trigger | `eotg_aug_flavour_rule_allows` | scripter | `NOT = { has_game_rule = eotg_aug_events_off }` |
| scripted modifier | `eotg_aug_rule_frequency_modifier` | scripter | |
| scripted modifier | `eotg_aug_rule_ai_uptake_modifier` | scripter | |
| memory icons | reused vanilla `.dds` (§5.1 table) | none now | Owner may commission `eotg_*` icons later; not blocking. |

No landed titles, so no tier-first keys.

## 4. File placement

| File | Content |
|---|---|
| `common/character_memory_types/eotg_memories.txt` | the 10 types (new folder) |
| `common/game_rules/eotg_game_rules.txt` | the 3 rules (new folder) |
| `common/scripted_modifiers/eotg_rule_modifiers.txt` | the 2 modifiers (new folder) |
| `common/scripted_triggers/eotg_augmentation_triggers.txt` | append `eotg_aug_flavour_rule_allows` |
| `common/scripted_effects/eotg_augmentation_effects.txt`, `eotg_frontier_effects.txt` | memory call sites (§5.3) |
| `common/on_action/eotg_augmentation_on_actions.txt`, `common/decisions/eotg_augmentation_decisions.txt`, `common/script_values/eotg_frontier_values.txt` | rule hooks (§6.3) |
| `localization/english/eotg_memories_l_english.yml`, `eotg_game_rules_l_english.yml` | new files, UTF-8 with BOM |

**Main session:** add `common/character_memory_types/`, `common/game_rules/` and `common/scripted_modifiers/` to the CLAUDE.md placement list. No `replace_path` is involved, and every file is additive.

---

## 5. INT4: memories

### 5.1 Type definitions

Every type uses this shape (vanilla `G/common/character_memory_types/character_memories_filippa_events.txt:526-537`):

- `categories`;
- `icon`;
- `description`, `second_perspective_description` and `third_perspective_description`, each `first_valid` / `desc`;
- `participants`, only where listed below;
- `duration = { years = memory_default_duration }`. This is a vanilla script value (`G/common/script_values/00_memory_values.txt:1`): 5 years, +125 for rulers and ruler kin.

Triggered variants follow `character_memories_1.txt:5-39` (`first_valid` → `triggered_desc`). Root is the memory and `scope:owner` is its owner (`.info:15-17`).

| Type | Categories | Participants | Variables | Icon (vanilla `gfx/interface/icons/memory_types/`) | Desc variants |
|---|---|---|---|---|---|
| `eotg_aug_initiated_memory` | `eotg_cybernetics major` | none | none | `icon_wounded.dds` | one |
| `eotg_aug_overclocked_memory` | `eotg_cybernetics` | none | none | `martial.dds` | one |
| `eotg_aug_cascade_memory` | `eotg_cybernetics negative major private` | none | none | `intimidation.dds` | one |
| `eotg_aug_seamless_memory` | `eotg_cybernetics major private` | none | none | `_default.dds` | one |
| `eotg_aug_excised_memory` | `eotg_cybernetics negative private` | none | none | `icon_wounded.dds` | one |
| `eotg_aug_restrained_memory` | `eotg_cybernetics negative title private` | `eotg_successor` | none | `prison.dds` | one |
| `eotg_aug_locked_wing_memory` | `eotg_cybernetics title family` | `eotg_predecessor` | none | `succession_chaotic.dds` | one |
| `eotg_frontier_founded_memory` | `eotg_frontier positive` | `eotg_founder` | `eotg_region` | `great_project_memory.dds` | `_self` when `memory_participant:eotg_founder = scope:owner`, else `_sent` |
| `eotg_frontier_settled_memory` | `eotg_frontier positive major` | `eotg_founder` | `eotg_region` | `monument.dds` | `_self` / `_sent`, same test |
| `eotg_frontier_abandoned_memory` | `eotg_frontier negative` | none | `eotg_region`, `eotg_failed` | `war_ended_negative.dds` | `_failed` when `has_variable = eotg_failed`, else `_chosen` |

**Why mix in vanilla categories.** Vanilla reads memory categories in 116 places. Two examples:

- Feast toasts take `positive` memories that are not `private` (`G/events/activities/feast_activity/main_events/feast_default_events_alex.txt:32-36`).
- Coronation rewards pay prestige for `major` and dynasty prestige for `family` (`coronation_events_1.txt:3585-3602`).

So a settled Frontier can be toasted at a feast for free. `private` keeps the cascade, Seamless, excision and restraints out of public toasts.

**The consequence:** vanilla splices `GetDescription` into its own sentences (`bp1_yearly_events_chad_l_english.yml:101`, "think back to when [pilgrimage_memory.GetDescription]"). Every `_desc` must therefore follow the `.info` standard (`.info:5-12`): a first-person, past-tense, lower-case clause that can follow "when".

**Participants and the self case.** The Frontier types always pass `eotg_founder`. When the project has no founder, or the founder is the holder, the holder passes itself, and the `_self` variant renders. Participants are never omitted, so no expected tag is missing (`.info:42-44`). A dead founder is valid: vanilla `relative_died` uses a dead participant (`character_memories_1.txt:41`).

### 5.2 Creation shape

```
create_character_memory = { type = X  participants = { tag = scope:y } }   # .info:66-73
scope:new_memory = { set_variable = { name = eotg_region  value = scope:eotg_mem_region } }
```

The variable is set on `scope:new_memory` right after creation: vanilla `G/events/decisions_events/ep4_decision_events.txt:49-61`. The loc reads it as `[ROOT.Var('eotg_region').Title.GetBaseName]` (vanilla `memories_l_english.yml:659`).

### 5.3 Call sites

Rewiring only. Each memory goes into the single scripted effect that every path to the beat already runs through. The initiation effect alone has more than 30 event-option callers, so effect-level placement avoids missing paths, including the AI and on_action paths.

| # | Memory | File:line (insert point) | Scope / owner | Reached from (unchanged) |
|---|---|---|---|---|
| M1 | initiated | `eotg_augmentation_effects.txt:130-139` `eotg_aug_initiate_effect`, **inside** the `limit = { eotg_is_augmented_any = no }` branch (lines 132-136) | the initiate | the initiation events (`events/eotg_augmentation_initiation.txt`: .001 a/d/e, .002 a/c/d, .003, .004 a/e, .005-.020 install options), plus effect callers `eotg_augmentation_effects.txt:713, 732, 1377, 1507, 2611` (child, retainer, knight installs). A knight re-initiated while augmented gets no second memory. |
| M2 | overclocked | `eotg_augmentation_effects.txt:151-166` `eotg_aug_set_integration_effect`. Before `add_trait_xp`: `if = { limit = { eotg_is_aug_tier3 = no } save_temporary_scope_value_as = { name = eotg_mem_below_oc value = yes } }`. After `eotg_aug_refresh_synergy_effect`: `if = { limit = { exists = scope:eotg_mem_below_oc eotg_is_aug_tier3 = yes } create… }` | the character | `events/eotg_augmentation_tier2.txt:433, 497, 532, 600, 632` (tier2.003 a/c/d/f/g); `eotg_augmentation_on_actions.txt:1625` (non-ruler progression). Regressions (XP 0/50) never pass the test. |
| M3 | cascade | `eotg_augmentation_effects.txt:289-311` `eotg_trigger_neurofracture`, after `add_trait = eotg_neurofractured` (line 291) | the character | `eotg_augmentation_on_actions.txt:1028-1040` (threshold), tier3.002 c, phase-4 early cascade |
| M4 | seamless | `eotg_augmentation_effects.txt:1060` `eotg_aug_total_integration_effect`, after `add_trait = eotg_total_integration` (line 1062) | the character | `eotg_fracture.027` (integration outcome), `eotg_aug_end.009` a/c |
| M5 | excised | `eotg_augmentation_effects.txt:1031` `eotg_aug_excision_effect`, first line of the body | the survivor | `eotg_aug_excision_surgery_effect` (both survival branches) ← `eotg_aug_end.001` a/c/d/e |
| M6 | restrained | `eotg_augmentation_effects.txt:1273-1289` `eotg_aug_abdicate_effect`, after `add_character_flag = eotg_flag_aug_abdicated` (line 1285); `participants = { eotg_successor = scope:eotg_successor }` | the old ruler | `eotg_aug_end.030` a/b |
| M7 | locked wing | same effect, inside `scope:eotg_successor = { }` (lines 1286-1288), before the `trigger_event`; `participants = { eotg_predecessor = scope:eotg_old_ruler }` | the successor | same |
| M8 | founded | `eotg_frontier_effects.txt:156-198` `eotg_frontier_start_effect`, inside the guard after `eotg_frontier_set_founder_effect` (line 185). `save_temporary_scope_as = eotg_mem_region`; `holder = { create… participants = { eotg_founder = $FOUNDER$ } }`; set `eotg_region` | the county holder | `events/eotg_frontier_events.txt:117, 135, 154, 178, 212, 235, 262` (.001 a-g) |
| M9 | settled | `eotg_frontier_effects.txt:1121-1214` `eotg_frontier_complete_effect`, before `eotg_frontier_reward_sponsor_effect` (line 1211), while the founder var and `scope:eotg_frontier_holder` (line 1125) are still live. `eotg_founder` = `scope:eotg_frontier_founder` (saved at 1124) if it exists, else the holder | `scope:eotg_frontier_holder` | `events/eotg_frontier_events.txt:894, 919, 935` (.004 a/b/c) |
| M10 | abandoned | `eotg_frontier_effects.txt:1604-1650` `eotg_frontier_abandon_effect`, right after `eotg_frontier_save_hook_scopes_effect` (line 1607), before any clear. `holder = { create… }`, set `eotg_region`; `if = { limit = { always = $FAILED$ } scope:new_memory = { set_variable = eotg_failed } }` (the `always = $PARAM$` shape already used at line 1609) | the holder, **before** the Unclaimed release in the `eotg_frontier_on_abandoned` hook | `events/eotg_frontier_events.txt:1128` (.005 a, failed); `common/decisions/eotg_frontier_decisions.txt:535` (chosen) |

Tooltips: vanilla leaves `create_character_memory` visible in options (`G/events/activities/coronation_activity/coronation_events.txt:276-278`), so do not wrap it in `hidden_effect` unless a QA screenshot shows noise. M10's decision call is already hidden (`eotg_frontier_decisions.txt:533`).

**Governments: none.** No gameplay path adopts a government. `change_government` appears only in the debug decisions (`common/decisions/eotg_government_debug_decisions.txt`) and the Unclaimed placeholder machinery. See §10.

### 5.4 Reading memories later (suggestions only, for the owner)

The engine's triggers are `has_memory_type` and `has_memory_category` (`.info:78-79`), used inside `any_memory` / `random_memory` (`G/events/activities/coronation_activity/coronation_events_klank.txt:1100-1101`). Vanilla also accepts the `memory_type = X` list filter (`G/events/dlc/bp1/bp1_yearly_events_chad.txt:2890-2891, 2902-2907`). Recall shape: `random_memory = { … save_scope_as = x }` in `immediate`, then `[x.GetDescription]` or `[x.MakeScope.Var('…')…]` in loc (`pilgrimage_events_l_english.yml:1000`).

Candidates, none of which are built here (event expansion is the owner's call):

1. **`eotg_frontier.001` on a resettle.** If the holder holds an `eotg_frontier_abandoned_memory` whose `var:eotg_region` is this county, add a desc line: "I sent settlers here once before."
2. **`eotg_aug_end.002` Silence.** Recall `eotg_aug_initiated_memory` ("the day I first took them").
3. **`eotg_aug_end.040` The Ledger Balances (Seamless).** Read `eotg_aug_initiated_memory` as a fact the Seamless ruler recites without feeling.
4. **`eotg_fracture.005` What the Heir Saw.** The heir's own `eotg_aug_locked_wing_memory` (vanilla participant check: `any_memory_participant`, `feast_default_events_alex.txt:70-74`).

---

## 6. INT5: game rules

### 6.1 Rule definitions

The shape follows `conquerors_frequency` (`G/common/game_rules/00_game_rules.txt:130-175`): `categories`, `default`, and empty setting blocks. Rules that exist only for script to read have no `apply_modifier` or `flag` (`natural_disaster_earthquakes`, `00_game_rules.txt:1620-1632`). No setting carries `flag = blocks_achievements`, because achievements are already off in a total conversion.

| Rule | Categories | Default | Settings, in display order |
|---|---|---|---|
| `eotg_aug_event_frequency` | `{ eotg flavor }` | `eotg_aug_events_normal` | normal, low, high, off |
| `eotg_aug_ai_uptake` | `{ eotg ai }` | `eotg_aug_ai_uptake_normal` | normal, low, high |
| `eotg_frontier_difficulty` | `{ eotg difficulty }` | `eotg_frontier_difficulty_normal` | normal, easy, hard |

### 6.2 How script reads a rule

Script reads a rule with `has_game_rule = <setting key>`, a global trigger that works in any scope. Vanilla uses it in three places:

- an on_action `random_list` weight (`G/common/on_action/dlc/tgp/tgp_natural_disaster_on_actions.txt:15-27`);
- script values (`G/common/script_values/00_basic_values.txt:1875-1896`, `if`/`else_if` on `has_game_rule`);
- a scripted modifier (`G/common/scripted_modifiers/00_faction_modifiers.txt:1004-1036`).

The `.info` for scripted modifiers shows the call inside a `random_list` row (`_scripted_modifiers.info`, "Example invocation").

**Invariant 4:** the rules are read only in on_actions, decisions, scripted effects and script values, never in an event's `trigger = {}`. Cooldowns stay where they are, and the rules change no cooldown flag or duration.

### 6.3 Hook points

**`eotg_aug_event_frequency`**

- **low / high.** Add `eotg_aug_rule_frequency_modifier = yes` to every "nothing this year" row in `common/on_action/eotg_augmentation_on_actions.txt`: lines **223, 428, 764, 917, 1200, 1360, 1454, 1527, 1781, 2014** (the row's weight line). Body:
  ```
  modifier = { factor = 2    has_game_rule = eotg_aug_events_low }
  modifier = { factor = 0.5  has_game_rule = eotg_aug_events_high }
  ```
  This is the earthquake shape (`tgp_natural_disaster_on_actions.txt:15-21`, a rule-keyed modifier on the no-event row). Mechanics are untouched: risk accrual, drift, the cascade threshold, the terminal step and the Countdown story.
- **off.** Add `eotg_aug_flavour_rule_allows = yes` beside each event-gating `eotg_aug_available_for_pulse_events = yes` in the same file: lines **195, 234, 454, 604, 616, 787, 1037, 1298, 1923, 1957**.
  - **Not at line 1289.** That is the terminal step, `eotg_fracture.027`, which is mechanics.
  - Also add it to the non-ruler pool's enclosing `limit` (the `if` that opens the `random_list` at line 1707).
  - Also add it to the `trigger` of `eotg_on_birth_aug_parent_check` (557) and of the six activity hooks (2158, 2178, 2200, 2231, 2250, 2270).
  - Effect of "off": no yearly cybernetics events for anyone. Entry stays open through `eotg_decision_seek_augmentation` and the interactions. Installed hardware still wears: risk, Countdown, Cascade and the endgame decisions all still run.
  - The scripter confirms that no other gate site exists with `grep -n eotg_aug_available_for_pulse_events`.

**`eotg_aug_ai_uptake`**

- Add `eotg_aug_rule_ai_uptake_modifier = yes` to the two initiation nothing rows (lines **223, 428**) and to the `ai_will_do` of `eotg_decision_seek_augmentation` (`common/decisions/eotg_augmentation_decisions.txt:341-349`). There is one modifier body per use. Nothing rows **raise** the weight to lower uptake. `ai_will_do` takes the inverse:
  ```
  # nothing rows
  modifier = { factor = 3    is_ai = yes  has_game_rule = eotg_aug_ai_uptake_low }
  modifier = { factor = 0.5  is_ai = yes  has_game_rule = eotg_aug_ai_uptake_high }
  ```
  For the decision, use inline `modifier = { factor = 0.33 … low }` and `{ factor = 2 … high }`, not the scripted modifier.

**`eotg_frontier_difficulty`** applies to **player-held Regions only** (`holder = { is_ai = no }`). This mirrors vanilla `difficulty`, which splits `player:` from `ai:` (`00_game_rules.txt:1-30`). The AI's expansion pace stays as tuned.

- **Progress.** `common/script_values/eotg_frontier_values.txt:220-222`, `eotg_frontier_pace_value` (the one pace knob, per the comment at :200-202) becomes `value = 0.5`, plus:
  - easy: `if = { limit = { has_game_rule = eotg_frontier_difficulty_easy holder ?= { is_ai = no } } value = 0.65 }`
  - hard: `else_if … hard … value = 0.4`

  The legibility bands read the post-pace gain (`eotg_frontier_years_left_value`, :229-237), so their words stay accurate.
- **Strain.** `common/scripted_effects/eotg_frontier_effects.txt:748-751`, the tick's quiet-year `else_if`, which `eotg_on_yearly_frontier_tick` (`common/on_action/eotg_frontier_on_actions.txt:28-56`) is the only caller of.
  - easy: a second `eotg_frontier_ease_strain_effect`;
  - hard: the ease runs inside `random = { chance = 50 }`.

  Gate on `scope:eotg_frontier_holder = { is_ai = no }` (saved at :680). `eotg_frontier_strain_fail_value` (8) is **not** changed, because the strain bands (4 and 6) in `.002` and in the AI gates are tied to it.

### 6.4 Saves

- Rules are fixed in the lobby. They can be read in-game but not changed, so a setting lasts for the whole campaign.
- When a rule is added mid-campaign, a save made before the patch is expected to load with the rule's **default** (normal). TEST-IN-GAME **T-R5**.
- **Setting keys are permanent once shipped.** If a key is renamed or removed, saves holding it lose it, and every `has_game_rule` on the old key silently goes false.
- Retuning the numbers in §6.3 is save-safe. Renaming or removing a setting is not.

### 6.5 Loc

| Key pattern (`_game_rules.info:18-21`) | Keys |
|---|---|
| `game_rule_category_<cat>` | `game_rule_category_eotg` ("Echoes of the Grip") |
| `rule_<rule>` | `rule_eotg_aug_event_frequency`, `rule_eotg_aug_ai_uptake`, `rule_eotg_frontier_difficulty` |
| `setting_<setting>` + `_desc` | 10 settings × 2 = 20 keys |

The text follows vanilla `game_rules_l_english.yml:246-256`: a short `#high …#!` name plus a one-sentence desc. Descs use **relative words, not numbers** ("fewer", "much rarer"), so retuning §6.3 needs no loc change. Canadian English. Frontier text uses Region/System terms (glossary).

---

## 7. Loc surface (INT4)

Four base keys per type, following vanilla `memories_filippa_l_english.yml:138-141`:

- `<type>`: the name, no perspective, lower case;
- `<type>_desc`: first person;
- `<type>_desc_second_perspective`;
- `<type>_desc_third_perspective`, using `[owner.GetName]`.

Variant types replace the bare `_desc*` keys with suffixed ones (`_self`/`_sent`, `_failed`/`_chosen`), each in the three perspectives. That is 49 keys in total:

- seven single-variant types × 4 = 28;
- the three variant types × (1 name + 2 variants × 3 perspectives) = 21.

Count exactly when writing. Drafts for the localizer, which lore-keeper confirms:

| Type | `_desc` draft (first person) |
|---|---|
| initiated | "I took my first implants" |
| overclocked | "I let the implants run past their rating" |
| cascade | "I went through the Neural Cascade" |
| seamless | "I handed over the controls, and the seam closed" |
| excised | "I had the implants cut out of me" |
| restrained | "I gave my throne to [eotg_successor.GetFirstName] and went into restraints" |
| locked wing | "I took the throne while [eotg_predecessor.GetFirstName] lived on in the locked wing" |
| founded `_self` / `_sent` | "I led an expedition into [ROOT.Var('eotg_region').Title.GetBaseName]" / "I sent [eotg_founder.GetFirstName] into …" |
| settled `_self` / `_sent` | "I saw [region] made a System of the realm" / "[eotg_founder.GetFirstName] and I saw …" |
| abandoned `_failed` / `_chosen` | "I watched the venture in [region] fail" / "I gave up the venture in [region]" |

Loc rules:

- Bare `[x.GetName]`, never `scope:`.
- No `replace/` overrides.
- No numbers, and no "humanity": the register is "self" / "personhood" (`events/eotg_augmentation_endgame.txt:32`).

## 8. Lore constraints

- **Seamless.** No second voice and no seam; personality is gone (`eotg_augmentation_effects.txt:1051-1058`). The Seamless memory is a flat statement, not a lament. Lore-keeper should rule on whether the first person suits a Seamless owner. The fallback is a neutral desc in every perspective.
- **Frontier.** Players see consequences, never numbers (`frontier_v1.md` §R). Region and System are the glossary terms. LAW AT 866: the holder owns the Region politically, so the memory goes to the holder, not the founder.
- **Era.** These are 866 AG mechanics. No Galactic League. No Nikios content.
- **Uncertain**, route to `eotg-lore-keeper`: the in-world name for "restraints" and the "locked wing" (the endgame events already use them, so match those keys).

## 9. Definition of done

**INT4**

1. `common/character_memory_types/eotg_memories.txt` defines exactly the 10 types in §5.1, each with `duration`, `icon`, `categories` and three description blocks. Participants are only as listed.
2. `grep -rn create_character_memory common events` returns exactly 10 hits, at the M1-M10 sites. No event file gains an event or an option.
3. Every loc key in §7 exists exactly once (UTF-8 BOM). PX `missing-required-loc` is clean for the new types.
4. Tiger and PX are clean apart from the known-benign list. `px_vocab_check.py` knows `create_character_memory` and `has_memory_type`.
5. **In game (T-M1..T-M4):**
   - T-M1: seeking augmentation (decision) adds "took my first implants" to the character's memories.
   - T-M2: debug-progressing to Overclocked adds M2 once, and a regression adds none.
   - T-M3: a Frontier founded, completed by `.004 c`, then a second founded and abandoned via the decision, gives M8, M9 and M10 `_chosen`, with the Region name rendered.
   - T-M4: the third-person text shows on another character's view.

**INT5**

6. Three rules appear in the lobby under the "Echoes of the Grip" category and under flavor / ai / difficulty, with all loc rendering.
7. `grep -rn has_game_rule events` returns nothing. Every read sits in an on_action, decision, scripted modifier, scripted trigger, scripted effect or script value.
8. **T-R1, frequency off:** 20 observer years show no `eotg_aug_*` pool event in `game.log`, while `eotg_fracture.0001` still fires for an AI past threshold.
9. **T-R2, frequency high:** 20 observer years give a pool-event count of at least 1.5× normal, from the same seed and start.
10. **T-R3, AI uptake low:** the AI augmented count after 30 years is below normal's.
11. **T-R4, Frontier hard:** a player Frontier's progress after 5 ticks is below normal's from the same start, while an AI Frontier's progress is unchanged.
12. **T-R5:** a save from before INT5 loads, the rules read default, and nothing errors.

## 10. Deferred

- **Government adoption memory:** there is no gameplay adoption path (§5.3). Revisit when a non-debug adoption decision or event exists (governments_v2).
- **Unclaimed attrition rule:** attrition is the static government field `supply_limit_mult_for_others = -0.5` (`common/governments/eotg_unclaimed_government.txt:92`), which script cannot change per game. The only scriptable route is the symmetric county-modifier fallback (`frontier_unclaimed_regions.md` §7.3), which is unverified until V-U3. Revisit after V-U3. A rule could then swap `eotg_unclaimed_mod_unclaimed` for a variant, applied at game start and on release.
- **Frontier flavour-event frequency rule:** not requested. The hook would be `eotg_frontier_event_roll_effect`'s nothing weight (`eotg_frontier_effects.txt:894`).
- **The Countdown and the Heir's Arc under "off":** they stay on, because the Countdown is the cascade's only warning. Revisit if testers ask.
- **Bespoke `eotg_*` memory icons:** vanilla icons for now. These are art, owned by the owner.
- **The §5.4 read-back events:** owner decision.

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Build INT4 (§5: 10 memory types and the M1-M10 call sites) and INT5 (§6: 3 rules, 2 scripted modifiers, 1 scripted trigger and the listed hook lines) from docs/specs/integration_v2.md, then hand the §7 and §6.5 keys to eotg-localizer.
- files: docs/specs/integration_v2.md
- needs-loc: 49 memory keys (§7), game_rule_category_eotg, 3 rule_* keys, 10 setting_* and 10 setting_*_desc keys (§6.5)
- needs-lore: whether a Seamless owner's memory takes the first person; in-world names for "restraints" and "locked wing" (§8)
- needs-human: add character_memory_types/, game_rules/ and scripted_modifiers/ to the CLAUDE.md placement list; T-M1..T-M4 and T-R1..T-R5 in game
