# Spec: Governments v2, Phase G2: the Cartel (`eotg_cartel_government`)

**Author:** eotg-architect, 2026-10-18. **Status:** draft. Next: eotg-lore-keeper (names, §8), then owner rulings (§12), then eotg-scripter in batches (§10).
**Parent specs:** `docs/specs/governments_v2.md` (§2, §5.4, §14), `docs/specs/government_template.md` (§2, §3.8, §3.11, §3.14, §3.15, §9.2, §9.6 step 4). **Assessment:** `docs/qa/government_assessment_2026-10-11/cartel.md`.
**Vanilla:** CK3 **1.20.1.1**. `G/` means `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`. Every line number below was re-read against 1.20.1.1. Version drift against earlier specs is listed in §13.
**Scope:** the Cartel only. It is the first of the four G2 passes. PMC, Corporation and Trade Oligarchy follow separately. Succession is out of scope (CB-53).

---

## 0. Kind of build (template §2 rule)

**A distinct government, not a reskin.** Its core verb differs from feudal's "conquer, then inherit":

> A Cartel ruler spends **fear** to put independent neighbours on a **payment schedule**, and the schedule keeps the fear alive.

This verb exists in vanilla only as mandala's piety-paid "Embrace as Tributary". G1 borrowed that interaction unchanged, which is why the assessment found dread and tribute "never touch" (cartel.md GAPS 1–3). G2 closes that loop and builds nothing else.

---

## 1. Purpose & gate

G2 makes dread and tribute one system. Three things change:
- **Dread buys the schedule.** An own interaction puts an independent neighbour on a Cartel-only tributary contract. It costs dread instead of piety, and acceptance reads the target's fear of the ruler.
- **The schedule feeds dread.** Each payer raises the ruler's dread baseline, so dread drifts up towards a higher floor.
- **Losing fear loses payers.** Below a dread threshold, payers walk away one a year. This replaces the G1 behaviour where the whole network lapsed at every death.

The pass also adds one top-tier and one vassal-tier decision, an entry decision and an exit decision, the grant fields, and the dread display.

**Gate: 2, under the mod-exclusive exemption** (owner, 2026-10-08, `CLAUDE.md`). **Not blocked by Gate 1.** Everything is map-agnostic: no title, province, culture, faith or character key in script. The British Isles test sub-mod supplies the Cartel (k_leon, Alfonso VI, with Rodrigo of d_asturias and Pedru of c_pravia below him, `isles_assignments.csv:73-76`).

**Soft dependency: CB-49** (the G1 in-game checks are still unrun). Batch C1 can be built and statically checked now. The in-game V-C tests for C2 onward should run in the same session as CB-49 items 1, 2 and 8, because the V-C list assumes G1's V-G1–V-G4 pass.

---

## 2. Signature resource: dread (engine), coupled to tribute

### 2.1 Decision: dread, not a dedicated variable

`governments_v2.md` §2 already fixes the Cartel's resource as vanilla dread, and that spec is owner-approved. Template Q2 allows a universal currency only "if the government changes how it is gained or spent". G2 makes exactly that change, so dread stays. The reasons for not adding a new variable:

1. **The engine already acts on it.** Vassal and courtier AI reads intimidation. `has_dread_level_towards` (level 1 = intimidated, 2 = cowed) appears in `ai_accept` blocks across vanilla, e.g. `G/common/character_interactions/00_tributary_interactions.txt:3844-3863` (+25 / +50). A scripted variable would get none of this.
2. **Vanilla already uses dread to force tribute.** Mandala's `reassert_tributary_interaction` has a dread send-option: valid at `dread >= high_dread`, auto-accepted (`00_tributary_interactions.txt:5598-5604`, `:5925-5952`). G2 copies that shape.
3. **A second fear number would compete with the first.** A ruler would see "dread 60" in the character window and some other fear value in a story panel, and the two would disagree.
4. **It needs no new GUI.** The character window already shows dread.

The cost is that dread is not unique to the Cartel. That is accepted, because the Cartel is the only government whose **dread baseline, spending and payer retention** are tied to tribute.

### 2.2 Identifiers and authority

| Item | Key | Notes |
|---|---|---|
| The resource | `dread` (engine) | Range 0 to `max_dread`. The default is `MAX_DREAD = 100` (`G/common/defines/00_defines.txt:120`; government field `max_dread`, `G/common/governments/_governments.info:478-482`). The engine clamps to this range. |
| Change effect (the only writer in Cartel files) | `eotg_cartel_change_dread_effect = { AMOUNT = <value> }` | See §2.3. Vanilla content and other mod systems (cybernetics `add_dread`) still write dread directly. That is fine, because the authority rule covers Cartel content only. |
| Clamp value | `eotg_cartel_dread_clamped_value` | Reads `scope:eotg_cartel_dread_amount` and clamps to `[-dread, 100 - dread]`, so the tooltip shows the real change. |
| Payer count | `eotg_cartel_payer_count_value` | `every_tributary` with `has_subject_contract_group = eotg_cartel_tributary`, adding 1 each. |
| Baseline mirror (character variable) | `eotg_cartel_schedule_scale` | Equals `min(4 × payers, 40)`. Written only by `eotg_cartel_refresh_schedule_effect`. |
| Scale value | `eotg_cartel_schedule_scale_value` | Reads `var:eotg_cartel_schedule_scale` and defaults to 0. Shape: `prepare_travels_modifier_value`, `G/common/script_values/00_court_position_values.txt:2602-2611`. |
| Succession grace (character variable, timed 3 years) | `eotg_cartel_succession_grace` | Set on the primary heir at the death of a Cartel ruler who has payers (§6.3). While it is set, the walk-off (§5.4) is skipped. |
| Story display mirror (story variable) | `eotg_cartel_dread_shown` | For display only. No script ever reads it as the resource. |

### 2.3 The change effect

```
# common/scripted_effects/eotg_cartel_effects.txt (character scope)
eotg_cartel_change_dread_effect = {
    save_scope_value_as = { name = eotg_cartel_dread_amount  value = $AMOUNT$ }
    add_dread = eotg_cartel_dread_clamped_value     # clamped to [-dread, 100 - dread]
    eotg_cartel_sync_story_effect = yes             # refresh the story counter now, not at the monthly tick
}
```
- **Spends never go below zero.** Every caller gates the spend in `is_valid` with `dread >= <cost>` and a custom tooltip. The effect itself never checks affordability. Vanilla does the same with its literal-gated dread option (`:5598-5604`).
- **Gains.** The engine applies `dread_gain_mult` (Cartel +0.25) to positive changes. The clamp works on the pre-multiplier amount, and the engine re-clamps at the cap anyway. This is accepted.
- **Use vanilla magnitudes:** `miniscule/minor/medium/major/massive_dread_gain` and `_loss` (`G/common/script_values/00_basic_values.txt:725-734`), and the thresholds `low_dread 20` / `medium_dread 40` / `high_dread 80` (`:993-995`).

### 2.4 Fix: the `dread_decay_mult` sign

In vanilla a **negative** `dread_decay_mult` is the bonus (slower decay):
- `champion_court_position` aptitude levels go from -0.02 to -0.3 (`G/common/court_positions/types/00_court_positions.txt:6850-6870`);
- `tradition_ruling_caste` is -0.3 (`G/common/culture/traditions/00_realm_traditions.txt:2260, 2279`).

G1's `+0.25` (`common/governments/eotg_cartel_government.txt:59`) makes dread fade **faster**, which is a penalty (template §9.2 item 1). **Change it to `dread_decay_mult = -0.25`.** Dread drifts towards its baseline at `DREAD_MONTHLY_CHANGE = 0.5` per month (`00_defines.txt:122`), so -0.25 gives 0.375 per month. `dread_gain_mult = 0.25` stays. This changes a value, not a key or flag, so it is not save-breaking (template §4.10).

### 2.5 Sources and sinks (template §3.11 "full")

| Direction | What | Who | Amount |
|---|---|---|---|
| Source (passive) | `eotg_cartel_schedule_modifier`: `dread_baseline_add` scaled by payers | top | +4 per payer, cap +40 |
| Source (choice) | Lean on the Locals (vassal decision, §4.2) | vassal; liege gets a share | +20 own, +5 to a Cartel liege |
| Source (vanilla) | executions, imprisonments, murders (engine) | any | vanilla |
| Sink (choice) | Put on the Schedule (interaction, §5.2) | top | 10 / 15 / 25 / 35 by target tier; +10 to compel |
| Sink (choice) | Tighten the Schedule (top decision, §4.1) | top | 5 per low payer, min 10, max 40 |
| Sink (penalty) | a refused demand | top | −5 |
| Conversion | Go Legitimate (exit, §6.2) | top | half of dread lost; legitimacy gained |
| Consequence | dread below 20 means one payer walks each year (§5.4) | top | — |

All numbers are first-pass balance values (OQ6).

### 2.6 Init and teardown (template Q5 and §3.11)

| Effect | Does | Called from |
|---|---|---|
| `eotg_cartel_init_effect` | If there is no `eotg_story_cartel_schedule`, `create_story` it. If `eotg_cartel_schedule_modifier` is missing, add it (no duration). Run `eotg_cartel_refresh_schedule_effect`. Idempotent. | `eotg_cartel_on_game_start` (every Cartel ruler); `eotg_cartel_on_government_change` (new government is Cartel); `eotg_cartel_on_title_gain` (Cartel and no story: catches heirs and newly landed courtiers via `use_as_base_on_landed`) |
| `eotg_cartel_refresh_schedule_effect` | Sets `eotg_cartel_schedule_scale` = `min(4 × eotg_cartel_payer_count_value, 40)`. | init; on accept of the interaction; Tighten; walk-off; the monthly story tick |
| `eotg_cartel_teardown_effect` | Ends `eotg_story_cartel_schedule` if present (`random_owned_story` with `story_type`, then `end_story`). Removes `eotg_cartel_schedule_modifier`, `eotg_cartel_schedule_scale` and `eotg_cartel_succession_grace`. **Does not touch dread:** it is a universal currency and the fear lingers. Payers are ended by the exit decision explicitly (§6.2), and in any case by the contract group's validity check (§5.1). | `eotg_cartel_on_government_change` when `scope:old_government = { government_type_has_flag = eotg_government_is_cartel }` and the new one is not Cartel. The flag test on a government-type scope has vanilla precedent: `G/common/scripted_rules/01_grant_title_rules.txt:39-42`. Also from the story's own tick if its owner is no longer a landed Cartel ruler (self-healing, §3.2). |

### 2.7 Display: the template §3.15 default (layers 1 + 4, no `gui/`)

Dread itself already has engine UI (the character window). The default layers add the tribute link and a labelled counter.

**Layer 1, the scaled modifier.** `common/modifiers/eotg_cartel_modifiers.txt`:
```
eotg_cartel_schedule_modifier = {
    icon = dread_positive                       # vanilla modifier icon (00_*_modifiers use it)
    dread_baseline_add = 1
    scale = {
        value = eotg_cartel_schedule_scale_value
        desc = eotg_cartel_schedule_scale_desc
        display_mode = scaled
    }
}
```
Shape: `prepare_travels_character_modifier`, `G/common/modifiers/00_court_position_modifiers.txt:133-142`. It is added with `add_character_modifier` (`G/common/on_action/travel_on_actions.txt:1432`) and its value is variable-backed (`00_court_position_values.txt:2602-2611`). The character window then shows "+N Dread baseline", which tells the player that payers hold the fear up.

**Layer 4, the visible story with a `basic_counter`.** `common/story_cycles/eotg_cartel_story.txt`, key `eotg_story_cartel_schedule`:
- `visible = yes`.
- Icon: vanilla `gfx/interface/icons/story_cycles/story_icon_palace_politics.dds`. Background: vanilla `gfx/interface/illustrations/event_scenes/alley.dds`, as in the mod's kingpin story. No art debt.
- `visualization`:
  - `basic_counter = { variable_name = "eotg_cartel_dread_shown" min = 0 max = 100 label = eotg_story_cartel_schedule_dread_label min_label = …_min_label max_label = …_max_label tooltip = …_tt }` (`_story_cycles.info:92-100`; `book_translation_story_cycle.txt:10-18`);
  - `modifiers = { eotg_cartel_schedule_modifier }` (`_story_cycles.info` visualization list);
  - `custom_string_key = eotg_story_cartel_schedule_info`, which explains the thresholds: 20 keeps payers, 40 entry, 80 compels.
- **The variable lives on the story**, as the template requires. `eotg_cartel_sync_story_effect` copies `story_owner.dread` into it. It runs from the change effect and from the monthly tick, so it lags vanilla dread changes by up to 30 days. This is a display limitation and is stated in the tooltip loc.
- **OQ3:** this would be the mod's second visible story. The first is the kingpin (owner ruling 2026-10-06). That ruling's hidden-risk rule is cybernetics-specific, and the template (2026-10-11) makes a visible story the default. The owner may still prefer the modifier alone. In that case the story stays as an invisible ticker (`visible = no`) and nothing else changes.

---

## 3. Identifier table

All keys carry `eotg_`. There are no landed titles. Shared opinion modifiers carry no government prefix (invariant 7). The namespace `eotg_cartel` is reserved (`governments_v2.md` §3.3) but **no event is built in this pass** (§11).

### 3.1 Script objects

| Type | Key | File | Owner |
|---|---|---|---|
| government (edit) | `eotg_cartel_government`: `dread_decay_mult = -0.25`; remove `ask_for_tribute` (OQ1); add `possible_grant_vassal_governments` (§7) | `common/governments/eotg_cartel_government.txt` | scripter |
| subject contract group (tributary) | `eotg_cartel_tributary` | `common/subject_contracts/groups/eotg_government_contract_groups.txt` (append) | scripter |
| character interaction | `eotg_cartel_put_on_schedule_interaction` | `common/character_interactions/eotg_cartel_interactions.txt` | scripter |
| send-option flag | `eotg_cartel_compel` (read as `scope:eotg_cartel_compel`) | same | scripter |
| decision (top) | `eotg_decision_cartel_tighten_schedule` | `common/decisions/eotg_cartel_decisions.txt` | scripter |
| decision (vassal) | `eotg_decision_cartel_lean_on_locals` | same | scripter |
| decision (entry) | `eotg_decision_cartel_adopt` | same | scripter |
| decision (exit) | `eotg_decision_cartel_go_legitimate` | same | scripter |
| scripted trigger (role ladder, `governments_v2.md` §14.2) | `eotg_cartel_role_top` (landed, Cartel, `is_independent_ruler = yes`); `eotg_cartel_role_county` / `_duchy` / `_kingdom` (Cartel, not independent, `highest_held_title_tier = tier_<x>`); `eotg_cartel_role_vassal` (any of the three) | `common/scripted_triggers/eotg_cartel_triggers.txt` | scripter |
| scripted effect | `eotg_cartel_change_dread_effect`, `eotg_cartel_sync_story_effect`, `eotg_cartel_refresh_schedule_effect`, `eotg_cartel_init_effect`, `eotg_cartel_teardown_effect`, `eotg_cartel_walk_off_effect`, `eotg_cartel_start_schedule_effect` (§5.3) | `common/scripted_effects/eotg_cartel_effects.txt` | scripter |
| script value | `eotg_cartel_dread_clamped_value`, `eotg_cartel_payer_count_value`, `eotg_cartel_schedule_scale_value`, `eotg_cartel_schedule_cost_value` (target tier; +10 with compel), `eotg_cartel_tighten_cost_value`, `eotg_cartel_exit_legitimacy_value` (= `dread × 2`, max `major_legitimacy_gain` 200, `G/common/script_values/00_legitimacy_values.txt:174`) | `common/script_values/eotg_cartel_values.txt` | scripter |
| character modifier | `eotg_cartel_schedule_modifier` (§2.7) | `common/modifiers/eotg_cartel_modifiers.txt` | scripter |
| county modifier | `eotg_cartel_leaned_on_modifier` (`county_opinion_add = -15`, `tax_mult = 0.1`; 5 years) | same | scripter |
| opinion modifier (shared) | `eotg_refused_protection_opinion` (decaying; also the 3-year re-ask cooldown, as vanilla `tributary_request_denied_opinion` at `00_tributary_interactions.txt:4644-4650`) | `common/opinion_modifiers/eotg_cartel_opinions.txt` | scripter |
| opinion modifier (shared) | `eotg_compelled_to_pay_opinion` (−20, `monthly_change = 0.1`, decaying; shape `intimidated_tributary_opinion`, `G/common/opinion_modifiers/tgp_mandala_opinions.txt:40-43`) | same | scripter |
| opinion modifier (shared) | `eotg_schedule_tightened_opinion` (−15, decaying) | same | scripter |
| story cycle | `eotg_story_cartel_schedule` | `common/story_cycles/eotg_cartel_story.txt` | scripter |
| variables | `eotg_cartel_schedule_scale`, `eotg_cartel_succession_grace` (character); `eotg_cartel_dread_shown` (story); scope value `eotg_cartel_dread_amount` | — | scripter |
| vanilla variable (reused, not ours) | `changed_government_recently` (5 years; the vanilla guard set at `G/common/scripted_effects/tgp_mandala_scripted_effects.txt:1643-1646`, read at `G/common/decisions/dlc_decisions/tgp/tgp_east_asia_decisions.txt:129-130, 549-550`) | — | scripter |
| on_action (mod) | `eotg_cartel_on_game_start`, `eotg_cartel_on_government_change`, `eotg_cartel_on_title_gain`, `eotg_cartel_on_death` | `common/on_action/eotg_cartel_on_actions.txt` | scripter |
| icons | vanilla only: modifier `dread_positive`; interaction `icon_demand_tribute` (`G/gfx/interface/icons/character_interactions/icon_demand_tribute.dds`); decision picture `decision_realm.dds`; story icon and background as §2.7 | — | none (no art debt) |

### 3.2 The story cycle in full

| Block | Content |
|---|---|
| `on_setup` | `eotg_cartel_sync_story_effect` |
| `on_end` | `story_owner` removes `eotg_cartel_schedule_modifier` and `eotg_cartel_schedule_scale` (idempotent with teardown) |
| `on_owner_death` | `end_story = yes`. The heir gets a fresh story through `eotg_cartel_on_title_gain`. |
| `effect_group` `months = 1` | Two triggered effects. (a) Owner is not a landed Cartel ruler: `story_owner = { eotg_cartel_teardown_effect = yes }`. (b) Otherwise: `eotg_cartel_refresh_schedule_effect`, then `eotg_cartel_sync_story_effect`. Shape: `_story_cycles.info:119-170`. |
| `effect_group` `years = 1` | Trigger: the owner passes `eotg_cartel_role_top`, has at least one payer, has `dread < low_dread`, and has no `eotg_cartel_succession_grace`. Effect: `eotg_cartel_walk_off_effect` (§5.4). **This tick is the walk-off's only cadence authority** (invariant 4, lesson 5). Nothing else checks a cooldown for it. |

---

## 4. Decisions that move the resource (template §3.8 "full")

Both decisions follow the vanilla decision shape in `G/common/decisions/dlc_decisions/ep_3/06_ep3_admin_decisions.txt:170-290` (`estate_governor_patrols_decision`). That shape covers `picture`, `ai_check_interval_by_tier`, `cooldown`, `is_shown`, `is_valid`, `is_valid_showing_failures_only`, `effect`, `cost`, `ai_potential` and `ai_will_do`. Its fields are in `G/common/decisions/_decisions.info:245-275`. **Dread is not a `cost` key**: the supported keys are gold, piety, prestige, renown, influence, herd, treasury, treasury_or_gold, merit and barter_goods (`_decisions.info:258-265`). Dread is therefore gated in `is_valid` and paid in `effect` through the change effect.

### 4.1 Top tier: `eotg_decision_cartel_tighten_schedule` ("Tighten the Schedule")

| Field | Value |
|---|---|
| `is_shown` | `eotg_cartel_role_top = yes`; `any_tributary = { has_subject_contract_group = eotg_cartel_tributary }` |
| `is_valid` | custom tooltip: `any_tributary = { has_subject_contract_group = eotg_cartel_tributary  vassal_contract_obligation_level:default_tributary_taxes = 1 }` (the trigger form on a tributary is vanilla: `00_tributary_interactions.txt:5367-5375`). Custom tooltip: `dread >= eotg_cartel_tighten_cost_value`. |
| `cooldown` | `{ years = 5 }` (the decision's own cooldown is the only authority) |
| `effect` | `eotg_cartel_change_dread_effect = { AMOUNT = { value = eotg_cartel_tighten_cost_value multiply = -1 } }`. Then `every_tributary` with the group and taxes level 1: `tributary_contract_set_obligation_level = { type = default_tributary_taxes level = 2 }` (the effect form is vanilla: `G/common/scripted_effects/00_interaction_effects.txt:2992, 3003`), and `add_opinion = { modifier = eotg_schedule_tightened_opinion target = root }`. Then `eotg_cartel_refresh_schedule_effect`. |
| Levels | `default_tributary_taxes`: 0 none, 1 `tributary_tax_low` (`normal_tributary_tax`, subject opinion −5), 2 `tributary_tax_high` (`high_tributary_tax`, subject opinion −25) (`G/common/subject_contracts/contracts/default_tributary.txt:1-58`) |
| `eotg_cartel_tighten_cost_value` | 5 × the number of low payers, min 10, max 40 |
| `ai_check_interval_by_tier` | barony 0, county 60, duchy 36, kingdom 36, empire 36, hegemony 36 |
| `ai_potential` | `eotg_cartel_role_top = yes` |
| `ai_will_do` | base 0. +20 if `dread >= eotg_cartel_tighten_cost_value + medium_dread` (keeps a reserve above the walk-off line). +10 if greedy. −10 if compassionate. Factor 0 if `dread < eotg_cartel_tighten_cost_value + low_dread`. |

**Why this decision:** it is the second sink, and it creates the risk loop. High obligations cost each payer −25 contract opinion plus the decaying −15, and unhappy payers use vanilla `cease_paying_tribute_interaction` (`00_tributary_interactions.txt:1474`).

### 4.2 Vassal tier: `eotg_decision_cartel_lean_on_locals` ("Lean on the Locals")

| Field | Value |
|---|---|
| `is_shown` | `eotg_cartel_role_vassal = yes` (county, duchy and kingdom vassals: the role-ladder rule, lesson 4) |
| `is_valid` | `exists = capital_county`; `is_at_war = no` |
| `cooldown` | `{ years = 5 }` |
| `effect` | `eotg_cartel_change_dread_effect = { AMOUNT = medium_dread_gain }`. `capital_county = { add_county_modifier = { modifier = eotg_cartel_leaned_on_modifier years = 5 } }`. If `liege = { government_has_flag = eotg_government_is_cartel }`: `liege = { eotg_cartel_change_dread_effect = { AMOUNT = miniscule_dread_gain } }` ("word travels up"). |
| `ai_check_interval_by_tier` | barony 0, county 60, duchy 48, kingdom 48, empire 0, hegemony 0 |
| `ai_potential` | `eotg_cartel_role_vassal = yes`; `NOT = { has_trait = compassionate }` |
| `ai_will_do` | base 10. +20 if `dread < low_dread`. +15 each for sadistic, callous and arbitrary. −30 if just. Factor 0 if `dread >= high_dread`. |

**Why this decision:** it is a source at every non-top tier, and it gives the top a second source that depends on how its vassals behave. It also seeds "the top is under threat from within": high-dread vassals become the material for the deferred faction and takeover work (§11, CB-53).

---

## 5. Tribute: the own interaction and contract group

### 5.1 `eotg_cartel_tributary` (contract group)

```
eotg_cartel_tributary = {
    is_tributary = yes
    is_valid_tributary_contract = {                     # ends the schedule if the suzerain stops being Cartel
        scope:suzerain = { government_has_flag = eotg_government_is_cartel }
    }                                                   # shape: tributary_celestial, subject_contract_groups.txt:166-171
    tributary_can_break_free = { always = no }          # as tributary_subjugated :105
    suzerain_heir_succession = yes                      # OQ2: the schedule passes to the primary heir (info :55)
    tributary_heir_succession = yes                     # a payer's heir keeps paying (celestial :163)
    suzerain_line_type = line_suzerain
    tributary_line_type = line_tributary
    should_show_as_suzerain_realm_name = no
    should_show_as_suzerain_realm_color = yes
    contracts = {                                       # the four vanilla contracts of tributary_subjugated (:112-117)
        default_tributary_taxes
        default_tributary_prestige
        suzerain_war_participation_guarantee
        tributary_war_participation_obligation
    }
}
```
Field spec: `G/common/subject_contracts/groups/_subject_contract_groups.info:22-55`. Loc: `eotg_cartel_tributary` and `_desc`, matching the G1 groups (loc `:312-313`).

**Why an own group instead of vanilla `tributary_subjugated`.** G1's payers end up in `tributary_subjugated` (the final `else` at `00_interaction_effects.txt:2981-3011`), which has `suzerain_heir_succession = no` (`subject_contract_groups.txt:103-106`). The whole network lapses at every death, and the heir then has to pay piety to rebuild it (assessment GAP 3). Because G2 owns the interaction, it can choose the group directly. Retention then depends on dread (§5.4), not on the ruler surviving. Payers G1 created stay in `tributary_subjugated` and lapse as before, so no migration is needed.

### 5.2 `eotg_cartel_put_on_schedule_interaction` ("Put on the Schedule")

Shape: vanilla `offer_tributary_status_interaction` (`00_tributary_interactions.txt:4456-4735`) for targeting and AI, and `reassert_tributary_interaction` (`:5305`) for the dread send-option and auto-accept.

| Field | Value | Vanilla line |
|---|---|---|
| `category` / `common_interaction` / `icon` | `interaction_category_diplomacy` / yes / `icon_demand_tribute` | demand_tributary `:851-853` |
| `is_available` | `government_has_flag = eotg_government_is_cartel`; `is_landed = yes`; `is_independent_ruler = yes` | offer `:4463-4470` (which gates on `government_allows = ask_for_tribute`) |
| `is_shown` | Actor and recipient are different and not in the same suzerain bloc (`top_suzerain ?= scope:recipient.top_suzerain`). Recipient: independent, landed, `highest_held_title_tier >= tier_county`, `< tier_hegemony`, not `government_has_flag = cannot_be_vassal_or_liege` (excludes Unsworn placeholders), and `is_tributary = no`. Neighbour test: `scope:actor = { any_land_neighboring_realm_with_tributaries_owner = { this = scope:recipient } }`. | offer `:4472-4486`; demand_tributary neighbour test `:888-890` |
| `is_valid_showing_failures_only` | Actor: `can_have_tributaries_trigger = yes` (crown authority ≥ 1 and independent, `G/common/scripted_triggers/mpo_scripted_triggers.txt:912-916`), `is_physically_able = yes`, no truce with the recipient. Custom tooltip: `dread >= eotg_cartel_schedule_cost_value`. Recipient: no `eotg_refused_protection_opinion` towards the actor. | offer `:4488-4529` |
| `cost` | **none**. Dread is not a cost key (§4); it is paid in `on_accept`. | — |
| `send_option` | `flag = eotg_cartel_compel`, `localization = eotg_cartel_compel_option`, `is_valid = { scope:actor = { dread >= high_dread } }` | reassert `:5598-5604` |
| `auto_accept` | `scope:eotg_cartel_compel = { custom_description = { text = eotg_cartel_compel_tt  subject = scope:actor  object = scope:recipient  scope:eotg_cartel_compel = yes } }` | reassert `:5925-5952` |
| `on_accept` | `scope:actor = { eotg_cartel_change_dread_effect = { AMOUNT = { value = eotg_cartel_schedule_cost_value multiply = -1 } } }` (the cost value already includes +10 under compel); `eotg_cartel_start_schedule_effect = yes` (§5.3); if compel, recipient gets `eotg_compelled_to_pay_opinion`; actor toast `eotg_cartel_schedule_toast` | toast shape `:2176-2183` |
| `on_decline` | Recipient: `add_opinion = { modifier = eotg_refused_protection_opinion target = scope:actor years = 3 }`. Actor: `eotg_cartel_change_dread_effect = { AMOUNT = miniscule_dread_loss }` (a threat that is called costs fear). Actor: `trigger_event = char_interaction.0363` (vanilla "Demand Tributary Response: Refused" letter, `G/events/interaction_events/character_interaction_events.txt:2920`; it shows only the opinion tooltip, so nothing in it is wrong for us). | offer `:4642-4652`; demand_tributary `:991-1005` |
| `ai_targets` / `ai_frequency_by_tier` | `neighboring_rulers_including_tributary_borders` / county 24, others 12, barony 0 | `:4656-4667` |
| `ai_will_do` (actor) | base 0. + recipient gold / 10, max 100. `ai_military_threat_modifier` (SENDER actor, RECEIVER recipient, ×−1). −20 if the recipient is more than one tier above the actor. +25 if `dread >= high_dread`. Factor 0 if `scope:actor.realm_size < scope:recipient.realm_size`. Factor 0 if `dread < eotg_cartel_schedule_cost_value + low_dread` (never spend into walk-off). | `:4672-4735` |
| `ai_accept` (recipient) | base −25. `ai_military_threat_modifier` (SENDER recipient, RECEIVER actor, ×1). Intimidated +25, cowed +50 (`has_dread_level_towards` level 1 / 2). Confederation member −50. `ai_boldness` / 4, negated. `ai_greed` / 4, negated. Rival −10, nemesis −100. Tier: −25 per tier the recipient is above the actor. Opinion factor as vanilla. | threat `:4872`; dread levels `:3844-3863`; confederation `:4746-4750`; boldness and greed `:5126-5144`; rivals `:5146-5163` |
| `eotg_cartel_schedule_cost_value` | recipient's highest held tier: county 10, duchy 15, kingdom 25, empire 35; +10 if `scope:eotg_cartel_compel = yes` | — |

**AI acceptance against G1.** A Cartel using vanilla "Embrace" against a feudal target starts at −50 base −50 "wrong government" (`:4737-4738`, `:4970-4975`) and gets none of the mandala radiance or piety terms. G2 starts at −25 and adds up to +50 for fear. Measure it in V-C16.

### 5.3 How G2 relates to `mandala_embrace_tributary_effect` (corrects `governments_v2.md` §5.4)

In G1, vanilla Embrace runs `on_accept` → `mandala_embrace_tributary_effect` (`00_tributary_interactions.txt:4619, 4628` → `G/common/scripted_effects/tgp_mandala_scripted_effects.txt:2123-2141`). That effect does four things:

| Part | What it does | G2 keeps it? | Why |
|---|---|---|---|
| `add_opinion accepted_tributary_status_opinion` +20 (`:2124-2130`) | Gratitude. It also acts as Embrace's cooldown. | **No.** It is replaced by `eotg_compelled_to_pay_opinion` (compel only) and our own refusal cooldown. | Fear, not gratitude. The Cartel does not embrace. |
| `start_tributary_interaction_effect` (`00_interaction_effects.txt:2325`) | Picks a group by suzerain government. The Cartel falls to the final `else`, `tributary_subjugated`, at `:2981-3011`. | **Partly.** `eotg_cartel_start_schedule_effect` copies only the pieces it needs: `start_tributary = { contract_group = eotg_cartel_tributary suzerain = scope:actor }` (form `:2982-2985`); `tributary_contract_set_obligation_level` taxes 1 and prestige 0 (the low branch, `:2988-2993`); then `setup_tributary_truces_effect = { SUZERAIN = scope:actor TRIBUTARY = scope:recipient }` (`:3016`, the same truces vanilla gives). | Calling the vanilla effect would force `tributary_subjugated`. **New payers always start low**, so Tighten (§4.1) has something to tighten. |
| `trigger_event = char_interaction.0362` (`:2134-2136`; event `character_interaction_events.txt:2892`) | Acceptance letter to the actor. Its `immediate` shows `start_tributary_interaction_effect` as a tooltip. | **No.** The actor gets `eotg_cartel_schedule_toast` instead. | Its tooltip would describe the vanilla subjugated terms ("high taxes"), not the Cartel's group and low start, so it would misinform the player. 0363 on refusal is kept (§5.2). |
| `consume_all_criminal_reasons_effect` (`:2138-2141`; `G/common/scripted_effects/00_prison_effects.txt:2485`) | Consumes the actor's imprisonment, banish, execute and revoke reasons against the new payer. | **No.** | A Cartel does not forgive when it is paid: the grievance stays on the table. Vanilla's `demand_tributary_interaction` also consumes them (`:984-987`). This is a stated deviation. |

**The vanilla Embrace path itself (OQ1).** With `ask_for_tribute = yes` kept, Cartel rulers would see two tribute buttons. Vanilla Embrace costs piety (`:4532-4565`) and sends the notification "Come, see the light and join my gathering of devout tributaries…" (`G/localization/english/interactions_l_english.yml:1024`), which is wrong for a syndicate. Recommendation: **remove `ask_for_tribute`** from the Cartel. Nothing else reads the rule (`grep`: only `00_tributary_interactions.txt:4464` and `00_government_types.txt:934`). Removing it also hides the realm-window "tributarization chance" map mode (`_governments.info:260-266`), which would have shown vanilla Embrace odds, not ours. Starting a tributary does not need the rule: nomads and steppe admins create tributaries without it, through `demand_tributary_interaction` (`:850`, gated by `can_get_tributaries_peacefully_trigger`, `mpo_scripted_triggers.txt:918-928`). **`count_tributaries_for_title_requirements = yes` stays** (`_governments.info:283-292`). Whether it counts payers in a mod group is checked in V-C4.

### 5.4 The walk-off (dread-based retention)

`eotg_cartel_walk_off_effect` (story yearly tick, §3.2):
1. `random_tributary` limited to the Cartel group, weighted towards the payer with the lowest opinion of the owner. On it: `end_tributary = yes` (the vanilla effect, `00_tributary_interactions.txt:2104`).
2. Owner toast `eotg_cartel_walk_off_toast`, naming the payer (shape `:2176-2183`).
3. `eotg_cartel_refresh_schedule_effect`.

It removes one payer a year at most. The equilibrium is that 5 payers give +20 baseline, so dread drifts to the 20 floor and stays there. A small, unfeared schedule unravels and a large one holds itself up. That is the "fear is the currency" fiction as a number. No event fires (§11 proposes a letter event to replace the toast).

### 5.5 What `governments_v2.md` §5.4 should now say

The orchestrator should amend §5.4 or point it here:
- the tributary contract is `eotg_cartel_tributary` for payers made through G2;
- `ask_for_tribute` is removed (if OQ1 is approved);
- G1's V-G13 is superseded for the Cartel by V-C4–V-C7 and V-C11–V-C12.

---

## 6. Entry and exit (template Q5)

Shapes:
- entry: `convert_to_mandala_government_decision` (`G/common/decisions/dlc_decisions/tgp/tgp_east_asia_decisions.txt:57-245`) and `convert_to_tribalism_decision` (`G/common/decisions/80_major_decisions.txt:473-520`);
- exit: `mandala_adopt_clan_government_decision` (`tgp_east_asia_decisions.txt:523-587`) and `return_to_the_steppe_decision` (`G/common/decisions/dlc_decisions/tgp/tgp_steppe_decisions.txt:256`).

Both decisions use `decision_group_type = major`, as their precedents do.

### 6.1 Entry: `eotg_decision_cartel_adopt` ("Run the Realm as a Cartel"; name for lore-keeper)

| Field | Value |
|---|---|
| `is_shown` | `is_landed = yes`; `highest_held_title_tier > tier_barony`; `is_independent_ruler = yes`; `OR = { government_has_flag = government_is_feudal  government_has_flag = government_is_clan }` (vanilla flags; template §4.3 allows flag reads); `NOR` the four mod identity flags and `eotg_government_is_unclaimed` |
| `is_valid` | custom tooltip `dread >= medium_dread` (**reads the resource**: you are already feared) |
| `is_valid_showing_failures_only` | `NOT = { has_variable = changed_government_recently }` (vanilla tooltip key `not_changed_government_recently_tt`, `tgp_east_asia_decisions.txt:129-130`); `is_at_war = no`; `is_tributary = no` |
| `cost` | `prestige = 200` (vanilla literal, `convert_whole_realm_to_feudalism_decision`, `80_major_decisions.txt:438`) |
| `effect` | `set_variable = { name = changed_government_recently years = 5 }`, then `change_government = eotg_cartel_government`. `on_government_change` then runs the G1 law net and `eotg_cartel_init_effect`. **Only the ruler converts.** Vassals keep their governments. Grants made from now on become Cartel through `use_as_base_on_landed` (`_governments.info:73-77`). Forcing a whole feudal realm into crime would need vassal events (vanilla uses `major_decisions.0002` and `tgp_east_asia_decision_events.0015`), and new events need owner approval (§11). |
| `ai_check_interval_by_tier` | barony 0, others 72 |
| `ai_potential` | **`always = no` until OQ4** (AI adoption would contaminate the V-G11 leakage run) |
| `ai_will_do` (for when OQ4 allows it) | base 0. +10 if `dread >= high_dread`. +10 each for sadistic and callous. Factor 0 if `primary_title.tier > tier_duchy`. |

### 6.2 Exit: `eotg_decision_cartel_go_legitimate` ("Go Legitimate")

| Field | Value |
|---|---|
| `is_shown` | `eotg_cartel_role_top = yes` |
| `is_valid_showing_failures_only` | no `changed_government_recently`; `is_at_war = no` |
| `cost` | `prestige = medium_prestige_value` (150, `00_basic_values.txt:1002`) |
| `effect`, in order | (1) `add_legitimacy = eotg_cartel_exit_legitimacy_value`: **dread converts to legitimacy**, the herd → treasury refund pattern (`nomad_convert_herds_to_treasury_or_gold_special_troops_effect`, `G/common/scripted_effects/10_dlc_tgp_scripted_effects.txt:3869`). (2) `eotg_cartel_change_dread_effect = { AMOUNT = { value = dread multiply -0.5 } }`. (3) `every_tributary` in the Cartel group: `end_tributary = yes`. **The schedule belongs to the Cartel**; the contract's validity check would also end it, and doing it here makes the result shown and immediate. (4) `every_vassal_or_below` with `government_has_flag = eotg_government_is_cartel`: `change_government = feudal_government`. This avoids leaving orphan Cartel vassals under a feudal liege. `feudal_government` is code-referenced (`00_government_types.txt:3`). Naming it as an effect target is not a trigger dependency (template §4.3); the G1 debug decision does the same. (5) `set_variable = { name = changed_government_recently years = 5 }`. (6) `change_government = feudal_government`. Teardown then runs through `on_government_change` (§2.6), and the engine drops the Cartel law through `can_keep` (V-G16). |
| `ai_check_interval_by_tier` | barony 0, others 120 |
| `ai_potential` | `eotg_cartel_role_top = yes`; `dread < low_dread`; no payers |
| `ai_will_do` | base 0. +10 if just. +10 if honest. Factor 0 if any vassal of the realm passes `eotg_cartel_role_vassal` with `dread >= high_dread` (a feared boss below you is not the moment to go straight). |

### 6.3 Forced and incidental transitions

| Case | Behaviour |
|---|---|
| Ruler dies, heir is Cartel | Story `on_owner_death` ends the story. `eotg_cartel_on_death` (root is about to die, `G/common/on_action/death.txt:1-7`) sets `eotg_cartel_succession_grace` (3 years) on `primary_heir` if root has payers. Payers pass to the primary heir (`suzerain_heir_succession = yes`). The heir's `on_title_gain` runs `eotg_cartel_init_effect`. |
| Heir is not Cartel (erosion, T4) | The group's `is_valid_tributary_contract` ends the payers. The heir never gets a story. The grace variable expires on its own. |
| Ruler loses all land | The monthly story tick sees a non-landed owner and calls teardown. |
| Becomes a vassal (conquest) | The role changes from top to vassal. Payers end, because `can_have_tributaries_trigger` needs independence, and the engine is expected to end tributaries of a non-independent suzerain [engine, unverified]. V-C20 records what happens. Walk-off and Tighten stop (role-gated). Lean becomes available. |
| Debug decisions (G1) | They keep working. The init and teardown hooks cover them, because they go through `change_government`. |

---

## 7. AI and grant fields (template §3.14)

| Field | Feudal (`G/common/governments/00_government_types.txt`) | Cartel G2 | Why |
|---|---|---|---|
| `possible_grant_vassal_governments` | `{ theocracy_government ecclesiastical_government }` (`:40`) | **the same list** | Parity with every settled vanilla government: admin `:553`, celestial `:915`, meritocratic `:1354` and japan `01_japan_government_types.txt:86, 169`. `is_grant_government_shown` only offers the faith's own theocratic type (`G/common/scripted_rules/01_grant_title_rules.txt:37-46`), so this needs no faith key. It does **not** list `feudal_government`, which would be an erosion path out of the Cartel. |
| `grant_vassal_ai_will_do` | value 0, +10 for a settling nomad or herder liege (`:43-56`) | **not set** (default 0, `_governments.info:738-756`) | It is scored only when the *liege's* government lists the Cartel in its `possible_grant_vassal_governments`. No vanilla or mod government does, so the block would be dead code (robustness plan F5). Grants to a Cartel liege's courtiers already default to Cartel through `use_as_base_on_landed`. Revisit if a mod government ever lists the Cartel (e.g. a PMC → Cartel path). |
| Grant cooldown | The vanilla `grant_vassal_government_cooldown` (365 days, `G/common/character_interactions/00_grant_titles_interaction.txt:1379-1390`) | inherited | The Cartel carries `government_is_settled`, so a theocratic grant hits the theocracy branch of `is_grant_government_valid` (`01_grant_title_rules.txt:89-150`) with its cooldown. Nothing to add. |
| `ai = { }` | `use_legends = yes` (`:24-26`) | unchanged | `use_great_projects` is banned (CLAUDE.md). |
| `ai_will_do` on every own decision, interaction and contract level | — | §4, §5.2, §6 | template §5.1 item 7 |

**How the AI lives on dread:**
- **Gains:** vanilla engine dread from executions and imprisonments (hard-coded AI), the baseline from payers, and Lean for vassals.
- **Spends:** Put on the Schedule and Tighten, each blocked unless the reserve stays above `low_dread` after the spend, so the AI never spends itself into walk-off.
- **Avoids churn:** cooldowns of 5 years (decisions) and 3 years (refusal), the 3-year succession grace, and at most one walk-off a year.
- **Entry:** off (OQ4). **Exit:** only when broke in fear and payer-less.

---

## 8. Lore constraints

From `governments_v2.md` §11 and §17, which bind this spec unchanged:
- **The identity is the generic syndicate-state.** A council of bosses rules smuggling routes, salvage and black markets through fear, and "keeps its neighbours on a payment schedule" (`Third era Events.md:147-150`; `Third era Nations.md:1345-1348`; LQ1). The interaction and decision names come from that phrase. **No text names a nation or person**: not the Concrete Cartel, which is on the cybernetics never-name list (`cybernetics_v2.md:211`), and not the Slate Syndicate, which is post-866.
- **No authority above the polity at 866** (ERRATA "LAW AT 866"). The schedule is enforced only by the Cartel. No text mentions a court, registry, League or arbitration.
- **The B2 mafia vocabulary is banned** (LQ6): Don, capo, consigliere, omertà, made man, "the Family", fedora, tommy gun, underboss, outfit, **racket**. That means "protection racket" is out, while "protection", "payment schedule" and "payers" are fine.
- **Prose says Bastion and Port** (`[castle|E]` / `[city|E]`), never "castle" or "city".
- **Canadian English** (neighbour, honour, colour).
- **The knight term is dynamic** (CB-48). Use `Custom('KnightCulture…')` if any text mentions knights. No text here needs it.
- **For the lore-keeper (needs-lore):**
  - Do "Put on the Schedule", "Tighten the Schedule", "Lean on the Locals", "Run the Realm as a Cartel", "Go Legitimate" and "The Payment Schedule" fit 866 voice?
  - Is "Go Legitimate" acceptable when the government already has legitimacy?

---

## 9. Loc surface (`localization/english/eotg_cartel_l_english.yml`, UTF-8 with one BOM, bare `[x.GetName]`)

| Object | Keys |
|---|---|
| interaction | `eotg_cartel_put_on_schedule_interaction`, `_desc`; `eotg_cartel_put_on_schedule_notification`; `eotg_cartel_compel_option`; `eotg_cartel_compel_tt`; `eotg_cartel_schedule_dread_tt` (affordability tooltip); `eotg_cartel_schedule_refused_tt` (cooldown tooltip); `eotg_cartel_schedule_toast`, `eotg_cartel_schedule_toast_desc` |
| walk-off toast | `eotg_cartel_walk_off_toast`, `eotg_cartel_walk_off_toast_desc` |
| decisions (×4) | `<key>`, `<key>_desc`, `<key>_tooltip`, `<key>_confirm`, plus `eotg_decision_cartel_tighten_schedule_dread_tt`, `_payers_tt`; `eotg_decision_cartel_adopt_dread_tt`; `eotg_decision_cartel_go_legitimate_effect_tt` (payers released, vassals convert) |
| modifiers | `eotg_cartel_schedule_modifier`, `_desc`; `eotg_cartel_schedule_scale_desc`; `eotg_cartel_leaned_on_modifier`, `_desc` |
| opinion modifiers | `eotg_refused_protection_opinion`, `eotg_compelled_to_pay_opinion`, `eotg_schedule_tightened_opinion` |
| contract group | `eotg_cartel_tributary`, `eotg_cartel_tributary_desc` |
| story | `eotg_story_cartel_schedule`, `_info`, `_dread_label`, `_min_label`, `_max_label`, `_tt` (the tooltip states the up-to-a-month lag) |

**`replace/` overrides: none.** Vanilla `char_interaction.0363` is reused as is. No vanilla key is redefined.
**G1 loc touched: none.** The "Council Succession" rename belongs to CB-53.

---

## 10. Build batches (scripter → localizer → lore-keeper → QA, per batch)

| Batch | Contents | Static gate | In-game tests |
|---|---|---|---|
| **C1, resource core** (buildable now) | §2.4 sign fix; role-ladder triggers; script values; the change, sync, refresh, init and teardown effects; `eotg_cartel_schedule_modifier`; story cycle (monthly tick only); `eotg_cartel_on_actions.txt` (game start, government change, title gain, death grace) | Tiger, PX, vocab; grep shows `add_dread` only inside `eotg_cartel_change_dread_effect` in Cartel files | V-C1–V-C3, V-C19 |
| **C2, tribute** (after OQ1 and OQ2) | `eotg_cartel_tributary` group; the interaction; the 3 opinion modifiers; `eotg_cartel_start_schedule_effect`; walk-off tick and toast; remove `ask_for_tribute` | hand check of the group against `_subject_contract_groups.info`; `ai_will_do` and `ai_accept` present | V-C4–V-C7, V-C11, V-C12, V-C18, V-C20 |
| **C3, decisions** | Tighten (top), Lean (vassal), `eotg_cartel_leaned_on_modifier` | `ai_will_do` on both; each moves dread through the change effect | V-C8–V-C10 |
| **C4, transitions and grants** | entry and exit decisions; `possible_grant_vassal_governments` | the entry `ai_potential` follows OQ4 | V-C13–V-C15 |
| **C5, loc and review** | §9 loc; lore-keeper review of names; QA full pass | template §5.1 items 1–8 | V-C16, V-C17 |

**Save compatibility (template §4.10):** removing `ask_for_tribute` and adding a contract group change a shipped government. Note both in the C2 commit and on the taskboard. Old G1 payers stay in `tributary_subjugated`.

---

## 11. Proposed events: OWNER APPROVAL REQUIRED (not in the build list)

Owner rule: every new event, option or beat needs approval. None of these is in §10. Each one moves or reads dread (invariant 5). If approved, they would use namespace `eotg_cartel`, loc keys `eotg_cartel_NNNN_t` / `_desc` / `_a`, and the story ticks or `yearly_playable_pulse` as their only cooldown authority.

| # | Proposal | Fires from | Dread coupling |
|---|---|---|---|
| E1 | **Short Payment.** A high-taxes payer with opinion below −25 underpays. Options: make an example (−10 dread, a lump of the payer's gold, payer opinion −20); let it slide (−5 dread); drop them to low taxes (shown only if `dread < medium_dread`). | story yearly tick, top | moves and reads |
| E2 | **A Payer Walks.** A letter from the departing payer that replaces the walk-off toast. Options: let them go; or spend 15 dread to hold them one more year (if `dread >= 15`). | walk-off effect | moves and reads |
| E3 | **Word Travels Up.** The Cartel liege hears that a vassal has leaned on the locals twice inside 10 years. Options: reward (gold to the vassal, the vassal's dread unchanged); warn (the vassal loses 10 dread, the liege gains 5); ignore. | Lean decision effect (the counter lives on the vassal) | moves and reads |
| E4 | **The Ledger Changes Hands.** An heir inherits payers. Options: re-state the terms (spend 10 dread, grace becomes 5 years); trust the name (grace stays 3 years, +prestige). | `eotg_cartel_on_title_gain` (with grace present) | moves and reads |
| E5 | **The v1 lift.** Six tier-neutral v1 Cartel events (`eotg_cartel_flavor.0005 .0009 .0010 .0011 .0012 .0018`, robustness plan 0.3), each audited to move or read dread or else dropped (`governments_v2.md` §14.1 P2). | `yearly_playable_pulse` via a mod on_action, sections A (any tier, role trigger) and B (top) | audit per event |

---

## 12. Owner questions

**Ruled 2026-10-20 (owner):** OQ1 to OQ6 are accepted as recommended (remove `ask_for_tribute` in C2; payers pass to the heir; the story is visible; no AI adoption yet; no `max_dread` change yet; the first-pass numbers are approved). OQ7: no events approved yet; E1 to E5 stay proposals. Investigation X2: the kingpin chain is **made rarer** for Cartel rulers, not blocked (spec in `investigation_rulings_2026-10-18.md`). CB-53: **elective succession** will be built (`governments_v2_g2_succession.md`).

- **OQ1, remove `ask_for_tribute` (recommended: yes).** It drops vanilla "Embrace as Tributary" for Cartels: the piety cost, the "devout tributaries" notification and the tributarization map mode. "Put on the Schedule" becomes the one tribute verb. If the answer is no, Cartels show both buttons, and V-C7 changes to "both present".
- **OQ2, payers pass to the heir (recommended: yes).** The own group has `suzerain_heir_succession = yes`, and the dread walk-off (§5.4) replaces the G1 rule that tribute lapses at every death. This reverses G1's accepted "the tribute lapses" behaviour (`governments_v2.md` §5.4). It also interacts with CB-53: if a takeover succession lands, payers follow whoever becomes the primary heir.
- **OQ3, a visible story (recommended: yes).** It would be the mod's second visible story (`basic_counter` of dread plus the schedule modifier). The alternative is the modifier alone, with the story kept as an invisible ticker.
- **OQ4, may the AI adopt the Cartel (recommended: not yet).** Keep entry player-only until V-G11 (leakage) has run, then revisit.
- **OQ5, `max_dread = 150` for the Cartel (recommended: not yet).** It is a vanilla field (nomad `00_government_types.txt:665`, steppe_admin `:1143`) and would be a strong identity lever, but tune the §2.5 numbers first.
- **OQ6, first-pass numbers.** Approve the §2.5 and §4–§6 values (+4 baseline per payer, cap 40; costs 10/15/25/35 plus 10 to compel; Tighten 5 per payer, 10–40; Lean +20 and +5; walk-off below 20; grace 3 years; entry 200 prestige at dread 40; exit 150 prestige) or name changes.
- **OQ7, the events in §11.** Which (if any) of E1–E5 to approve.

---

## 13. Definition of done

**Static (eotg-qa):**
1. Tiger is clean except the CLAUDE.md known-benign list (expected: story fields `visible` / `icon` / `background` / `visualization`). PX LSP and `px_vocab_check.py` are clean over the new files. PX `locCoverage` shows no missing `eotg_` key.
2. Hand check: `eotg_cartel_tributary` against `_subject_contract_groups.info:22-55` and `subject_contract_groups.txt:103-118, 157-171`; the government edit against `_governments.info` and `00_government_types.txt:40`.
3. `grep add_dread` across the Cartel files returns one line, inside `eotg_cartel_change_dread_effect`. Every Cartel decision and the interaction reads `dread` (in `is_valid` or `ai_will_do`) **and** moves it through the change effect.
4. Every decision, the interaction and every new modifier and opinion modifier has loc. The interaction and all 4 decisions have `ai_will_do`, and the interaction has `ai_accept`.
5. `grep -rnE 'eotg_[ekdcb]_'` is empty. No title, culture, faith, province or character key appears in a new file. No `has_government` appears in any new trigger.
6. `ask_for_tribute` is absent from the Cartel file (if OQ1 is approved). `dread_decay_mult = -0.25`.
7. The walk-off has exactly one cadence authority (the story's yearly `effect_group`). No Cartel trigger duplicates a cooldown check.

**In game (human, British Isles sub-mod, `-debug_mode`). Run alongside CB-49:**

| ID | Check | Pass |
|---|---|---|
| V-C1 | error.log shows nothing from the new files. The story, group, interaction, decisions and modifiers load. | yes |
| V-C2 | Alfonso (k_leon) has `eotg_cartel_schedule_modifier` (+0 with no payers) and a visible "Payment Schedule" story whose counter equals his dread within a month. Rodrigo and Pedru (landed Cartel vassals) **also have the story** (QA C1, 2026-10-20: §2.6 gives it to every landed Cartel ruler; a top-only story would be lost on independence without a title gain, since vanilla has no general on-independence hook). | yes |
| V-C3 | `add_dread 50` on Alfonso and on a feudal ruler. After 12 months the Cartel's dread has fallen less (about 4.5 against 6). | yes |
| V-C4 | Put on the Schedule is shown against an adjacent independent ruler (the Spain pockets, `governments_v2.md` §12) and not against a vassal, an Unsworn placeholder or a ruler in Alfonso's bloc. The dread cost appears in the tooltip. On acceptance: the payer is in `eotg_cartel_tributary` at low taxes; dread falls by the cost; the modifier shows +4; and tributary land counts towards title creation (`count_tributaries_for_title_requirements`). | yes |
| V-C5 | At dread ≥ 80, the compel option auto-accepts, costs 10 more and gives the payer −20 "compelled" opinion. | yes |
| V-C6 | A refusal costs Alfonso 5 dread, sends the vanilla 0363 letter and blocks a re-ask for 3 years (tooltip). | yes |
| V-C7 | The vanilla "Embrace as Tributary" is absent for Alfonso, and no piety cost appears on any Cartel tribute action. | yes (OQ1) |
| V-C8 | Tighten the Schedule raises low payers to high, costs 5 per payer (10–40), applies −15 opinion and goes on a 5-year cooldown. | yes |
| V-C9 | Rodrigo (duke vassal) takes Lean on the Locals: about +25 dread (20 × 1.25), Alfonso +6 (5 × 1.25), and the capital county modifier shows for 5 years. | yes |
| V-C10 | Pedru (count vassal) sees Lean. Alfonso does not see Lean. Neither vassal sees Tighten or the interaction. | yes |
| V-C11 | `kill` Alfonso while he has payers: the heir keeps the payers, holds `eotg_cartel_succession_grace`, and has a new story and the modifier. | yes (OQ2) |
| V-C12 | On the heir: set dread to 0 and remove the grace variable. Within 12 months one payer leaves with the walk-off toast, and the modifier drops by 4. | yes |
| V-C13 | An independent feudal ruler with dread ≥ 40 takes the entry decision: becomes Cartel, gets the Cartel law, story and modifier, and `changed_government_recently` is set. Vassals keep their governments. A county granted afterwards becomes Cartel. | yes |
| V-C14 | Alfonso takes Go Legitimate: legitimacy rises by min(2 × dread, 200); dread halves; payers are released; Rodrigo and Pedru become feudal; story and modifier are gone; the Cartel law is replaced by a feudal one. | yes |
| V-C15 | Alfonso grants a temple county to a courtier: the government picker offers only his faith's theocratic type. A castle county grant defaults to Cartel. | yes |
| V-C16 | 50-year observer run: the AI Cartel uses the interaction and Tighten; dread stays within 0–100 and moves both ways; payer count does not fall to 0 and stay there through a walk-off cascade; no AI ruler takes the entry decision (OQ4); record the acceptance rate. | yes / recorded |
| V-C17 | Save with payers and the story, then reload: payers, story counter, modifier value and grace survive. | yes |
| V-C18 | Unsworn counties are never offered as targets. | yes |
| V-C19 | The modifier tooltip reads "+N Dread baseline" with N = 4 × payers (cap 40). The story tooltip states the lag. | yes |
| V-C20 | Alfonso is made a vassal (console): record what happens to his payers (expected: they end) and confirm Lean appears while Tighten does not. | recorded |

---

## 14. Deferred

| Item | Why | Trigger to revisit |
|---|---|---|
| Takeover or council succession; renaming "Council Succession" | Out of scope; CB-53 is pending with the owner. **Dependency:** payer inheritance and the grace both key on `primary_heir`, so they follow any future law automatically. | CB-53 ruling |
| The Cartel faction set (v1 §4.5: Shakedown, Hostile Takeover, Defection, Purge) | `governments_v2.md` §14.1 P3. It needs the takeover law to express its threat. | after CB-53 |
| Break free on low dread through `tributary_can_break_free` | The engine semantics are unknown: no script reader in vanilla (`grep`). Walk-off does the job in script. | if V-C16 shows walk-off is too blunt |
| A CB to force the schedule by war | The verb is coercion short of war. Vanilla tributary CBs are DLC-shaped. | G2 P3 |
| `opinion_of_liege`, `top_liege_character_modifier`, a military line (§3.7) | Not needed for the dread–tribute loop. Revisit with numbers from V-C16. | after V-C16 |
| `max_dread = 150` | OQ5 | after V-C16 |
| Kingpin weight tilt under a Cartel liege | `governments_v2.md` §5.4 "Coupling", optional | cybernetics follow-up |
| Proper icon and text icon | Art debt (human). The clan copies stay. | Gate 4 |
| Whole-realm conversion on entry | Needs vassal choice events (owner approval) | if OQ7 adds such an event |

**Version drift found while re-citing at 1.20.1.1 (for the orchestrator; earlier specs cite 1.20.0.3):**
- `mandala_embrace_tributary_effect` is now `tgp_mandala_scripted_effects.txt:2123` (was `:2130`).
- `return_to_the_steppe_decision` is now `tgp_steppe_decisions.txt:256` (template says `:243`).
- The theocracy governments moved to `G/common/governments/02_theocratic_government_types.txt`.
- The `_governments.info` grant fields are now `:729-756` (template says `:674-701`), and they now document the scripted rules `is_grant_government_shown` / `_valid` (`G/common/scripted_rules/01_grant_title_rules.txt`).
- Unchanged: `00_government_types.txt` feudal `:5-62` / `:40`, mandala `:934` / `:938`, and the tributary interaction lines cited in G1.

---

### HANDOFF
- status: done
- next: eotg-lore-keeper (names, §8), then human (OQ1–OQ7), then eotg-scripter (batch C1 is buildable now; C2 after OQ1/OQ2)
- ask: Review the §8 names and the §5.3 deviations for canon. Then the owner rules OQ1–OQ7. Then the scripter builds `docs/specs/governments_v2_g2_cartel.md` §10 batch C1 (dread sign fix, role ladder, change effect, scaled modifier, story, on_actions).
- files: docs/specs/governments_v2_g2_cartel.md
- needs-loc: §9 (interaction 9 keys, 2 toast keys, 4 decisions × 4 plus 5 tooltips, 5 modifier keys, 3 opinion modifiers, 2 group keys, 6 story keys)
- needs-lore: Are "Put on the Schedule", "Tighten the Schedule", "Lean on the Locals", "Run the Realm as a Cartel", "Go Legitimate" and "The Payment Schedule" canon-safe and B2-clean for 866?
- needs-human: OQ1–OQ7 (§12). V-C1–V-C20 run with CB-49. Orchestrator: amend `governments_v2.md` §5.4 per §5.5; record the version drift in §14; add OQs to the taskboard.
