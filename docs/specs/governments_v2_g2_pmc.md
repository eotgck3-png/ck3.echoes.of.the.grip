# Spec: Governments v2, Phase G2: the PMC (`eotg_pmc_government`)

**Author:** cloud session (architect role), 2026-11-03. **Status:** draft, **unvalidated** (no game, Tiger or PX in the cloud). Next: eotg-lore-keeper (names, §8), then owner rulings (§14), then eotg-scripter in batches (§10). Batch P1 is built on branch `claude/governments-g2-three-cloud` (§10).
**Parent specs:** `docs/specs/governments_v2.md` (§2, §5.1, §14), `docs/specs/government_template.md` (§2, §3.8, §3.11, §3.14, §3.15, §9). **Assessment:** `docs/qa/government_assessment_2026-10-11/pmc.md`. **Pattern:** `docs/specs/governments_v2_g2_cartel.md` (shipped). **Succession:** `docs/specs/governments_v2_g2_succession.md` §11 (the PMC keeps single heir; the commander may designate any child).
**Vanilla:** CK3 1.20.1.1. `G/` means `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`. **This session could not read vanilla.** Every vanilla citation below is either (a) copied from a shipped, locally validated mod file or spec that cites it, named as "via <file>", or (b) marked `UNVERIFIED-VANILLA`.
**Scope:** the PMC only. Corporation and Trade Oligarchy have their own G2 specs (`governments_v2_g2_corporation.md`, `governments_v2_g2_gobcorp.md`).

---

## 0. Kind of build (template §2 rule)

**A distinct government, not a reskin.** Its core verb differs from feudal's "conquer, then inherit":

> A PMC ruler **sells the company's force on contract** to earn **standing**, and standing is what the next contract pays for.

Vanilla's nearest verb is the landless adventurer's contracts. G1 built none of it (assessment GAP 1: "no core verb, no resource"). G2 adds the resource, the contract decision that earns it, a field-results feed, and the transitions.

---

## 1. Purpose & gate

G2 gives the PMC one number that the player watches and the AI reads:
- **Standing earns contracts.** A top-tier decision sells the company's service for gold that scales with standing, and a completed sale raises standing.
- **Results move standing.** Battles won and lost by a PMC war leader move it, which is the desc's "rank is earned by results in the field".
- **Standing buys talent.** A sink decision turns standing into a skilled Operator for the court.
- **Vassal contractors earn their own standing**, and some of it travels up the chain of command.

It also adds the entry and exit decisions, the grant fields and the standing display.

**Gate: 2, under the mod-exclusive exemption** (owner, 2026-10-08, `CLAUDE.md`). **Not blocked by Gate 1.** Everything is map-agnostic: no title, province, culture, faith or character key in script. The British Isles test sub-mod supplies the PMC: Raoul of Valois, d_valois, independent duke (`isles_assignments.csv:68`).

**Soft dependency: CB-49** (the G1 in-game checks). Batch P1 can be built and statically checked now. Run the in-game V-P tests alongside CB-49 items for the PMC (V-G1, V-G3, V-G4, V-G9).

---

## 2. Signature resource: `eotg_pmc_standing` (scripted)

### 2.1 Decision: a dedicated variable, not an engine currency

`governments_v2.md` §2 fixes the PMC's resource as `eotg_pmc_standing`, a character variable from 0 to 100, and that spec is owner-approved. Reasons it stays scripted:
1. **No engine currency means "market reputation".** Prestige is the nearest, but every ruler has it and it already buys everything (template Q2: a universal currency counts only if the government changes how it is gained or spent).
2. **Influence would need the admin stack** (template §8.1, T11 unrun).
3. **The template default** is a scripted pseudo-currency shown through a scaled modifier plus a story counter, with no `gui/` (template Q2, §3.15).

The cost is that no engine system reads it. The AI reads it only through our own `ai_will_do` terms, and no level table comes with it. Accepted.

### 2.2 Identifiers and authority

| Item | Key | Notes |
|---|---|---|
| The resource (character variable) | `eotg_pmc_standing` | 0 to 100. Set on every landed PMC ruler at every tier. |
| Change effect (**the only writer**) | `eotg_pmc_change_standing_effect = { AMOUNT = <number or named value> }` | §2.3. No other script writes `eotg_pmc_standing`: not init, not teardown, not inheritance. All of them call this effect. |
| Reader | `eotg_pmc_standing_value` | `var:eotg_pmc_standing`, 0 when unset. Shape: `eotg_cartel_schedule_scale_value` (`common/script_values/eotg_cartel_values.txt`). Every other script reads standing through this value. The two exceptions read `var:` directly where it is guaranteed set: the inheritance value and the story sync. |
| Clamp | `eotg_pmc_standing_next_value` | reader + `scope:eotg_pmc_standing_amount`, clamped to `[0, 100]` |
| Start value | `eotg_pmc_standing_start_value` | 40 for `eotg_pmc_role_top`, otherwise 20 (OQ5) |
| Inheritance | `eotg_pmc_standing_inherit_value` | heir scope: `max(0, 0.75 × predecessor's standing − heir's own)` (§2.4) |
| Story display mirror (story variable) | `eotg_pmc_standing_shown` | Display only. Never read as the resource. |

### 2.3 The change effect

```
# common/scripted_effects/eotg_pmc_effects.txt (character scope)
eotg_pmc_change_standing_effect = {
    save_scope_value_as = { name = eotg_pmc_standing_amount  value = $AMOUNT$ }
    set_variable = { name = eotg_pmc_standing  value = eotg_pmc_standing_next_value }   # clamped to [0, 100]
    eotg_pmc_sync_story_effect = yes                   # refresh the story counter now
}
```
- **The AMOUNT rule (Cartel amendment 2026-10-20):** a number or a **named** script value, never an inline `{ }` block (Tiger `error(macro)`). Every negative change therefore gets a named `*_spend_value` / `*_loss_value`.
- **Spends never go below zero.** Callers gate spends in `is_valid` with `eotg_pmc_standing_value >= <cost>` and a custom tooltip. The effect never checks affordability (Cartel §2.3).
- **The effect has no tooltip of its own** (`set_variable` shows nothing). Every visible caller adds a custom tooltip naming the change (template §3.15 layer 2). This is the main difference from the Cartel, whose `add_dread` has an engine tooltip.
- `save_scope_value_as` form: via `eotg_cartel_effects.txt` (`G/common/scripted_effects/00_administrative_effects.txt:101-104`).

### 2.4 Inheritance: standing follows `primary_heir`

The brief requires resources to follow `primary_heir`. Standing belongs to the company more than to the commander, so most of it carries over.

`eotg_pmc_on_death` (root is about to die; `G/common/on_action/death.txt:1-7`, via `eotg_cartel_on_actions.txt`): if root is PMC, has standing, and `exists = primary_heir`, then save root as `scope:eotg_pmc_predecessor`, and on `primary_heir` run `eotg_pmc_change_standing_effect = { AMOUNT = eotg_pmc_standing_inherit_value }`. The heir ends with **the higher of its own standing and 75% of the predecessor's.**

- **The heir may not be a PMC yet** (a landless child). The variable is written anyway. When the heir takes the title, `eotg_pmc_on_title_gain` runs init, which sets the start value **only if no variable exists**, so the inherited standing is kept, even if it is below the start value. A bad name carries over.
- **The heir is not PMC at all** (erosion): the variable stays dormant. Nothing reads it without the government flag.
- **Designated heirs** (`designate_heir_interaction`, crown authority 3; succession spec §11) are the `primary_heir`, so this follows the commander's pick automatically.

### 2.5 Sources and sinks (template §3.11 "full")

| Direction | What | Who | Amount | Batch |
|---|---|---|---|---|
| Source (choice) | Take a Contract (top decision, §4.1) | top | +10 (and gold) | P3 |
| Source (choice) | Deliver Results (vassal decision, §4.2) | vassal; PMC liege gets a share | +15 own, +5 liege | P3 |
| Source (passive) | battle won as a PMC side's primary participant (§5.1) | any tier | +2 per battle | P2 |
| Sink (penalty) | battle lost as a PMC side's primary participant (§5.1) | any tier | −3 per battle | P2 |
| Sink (drift) | yearly: above 60, standing falls by 2 ("the market forgets") | any tier | −2/year | P2 |
| Sink (choice) | Recruit on Reputation (top decision, §4.3, OQ3) | top | −20; a skilled Operator joins the court | P3 |
| Conversion | Stand Down the Company (exit, §6.2) | top | all standing → prestige (×4, max 400) | P4 |

The equilibrium: a company that takes a contract every 3 years and fights now and then sits between 40 and 70; an idle one slides to 60 and stays; a losing one bleeds. All numbers are first-pass (OQ6).

### 2.6 Init and teardown (template Q5 and §3.11)

| Effect | Does | Called from |
|---|---|---|
| `eotg_pmc_init_effect` | If there is no `eotg_story_pmc_standing`, `create_story` it. If `eotg_pmc_standing` is unset, `eotg_pmc_change_standing_effect = { AMOUNT = eotg_pmc_standing_start_value }`. If `eotg_pmc_standing_modifier` is missing, add it (no duration). Sync. Idempotent. | `eotg_pmc_on_game_start` (every landed PMC ruler; also after the lobby), `eotg_pmc_on_government_change` (new government is PMC), `eotg_pmc_on_title_gain` (landed PMC without the story: heirs, newly landed courtiers via `use_as_base_on_landed`) |
| `eotg_pmc_teardown_effect` | Ends the story if present (`random_owned_story` with `story_type`, then `end_story`). Removes `eotg_pmc_standing_modifier`. **Does not touch `eotg_pmc_standing`**: the reputation lingers, dormant, and the change effect stays the only writer. The exit decision zeroes it explicitly (§6.2). | `eotg_pmc_on_government_change` (old government PMC, new one not, read as `scope:old_government = { government_type_has_flag = eotg_government_is_pmc }`, the Cartel's verified form); the story's monthly tick if its owner is no longer a landed PMC ruler (self-healing, §3.2) |

### 2.7 Display: the template §3.15 default (layers 1 + 4, no `gui/`)

**Layer 1, the scaled modifier.** `common/modifiers/eotg_pmc_modifiers.txt`:
```
eotg_pmc_standing_modifier = {
    icon = martial_positive
    monthly_prestige = 0.01            # +1 prestige a month at 100 standing
    knight_effectiveness_mult = 0.001  # +10% knight effectiveness at 100 standing
    scale = {
        value = eotg_pmc_standing_value
        desc = eotg_pmc_standing_scale_desc
        display_mode = scaled
    }
}
```
Shape: `eotg_cartel_schedule_modifier` (shipped; `G/common/modifiers/00_court_position_modifiers.txt:133-142` via it). `martial_positive`, `monthly_prestige` and `knight_effectiveness_mult` are used by shipped mod modifiers and governments. **Here the scale reads the resource itself**, so no separate scale variable is needed (the Cartel needed one because its scale was a payer count). **UNVERIFIED-VANILLA:** fractional per-unit values (0.01, 0.001) under `display_mode = scaled`. The Cartel used an integer (`dread_baseline_add = 1`). V-P2 checks the tooltip.

**Layer 4, the visible story with a `basic_counter`.** `common/story_cycles/eotg_pmc_story.txt`, key `eotg_story_pmc_standing` ("The Company's Name"):
- `visible = yes`; icon `story_icon_palace_politics.dds` (the only story icon the mod has used, via the Cartel); background `gfx/interface/illustrations/event_scenes/ep3_military_tent.dds` (already used by a shipped mod file).
- `visualization`: `custom_string_key = eotg_story_pmc_standing_info`; `basic_counter = { variable_name = "eotg_pmc_standing_shown" min = 0 max = 100 label … min_label … max_label … tooltip … }`; `modifiers = { eotg_pmc_standing_modifier }`.
- **The mirror lives on the story** (template rule). `eotg_pmc_sync_story_effect` copies the owner's standing into it from the change effect and the monthly tick. Unlike the Cartel's dread, standing changes **only** through the change effect, so the counter never lags. The monthly sync is a safety net.
- `on_setup` seeds the counter at 0, and init syncs right after `create_story` (the Cartel's ordering, avoiding a read of an unset variable in `on_setup`).
- **OQ4:** this would be the mod's third visible story (kingpin, Cartel). The alternative is the modifier alone, with an invisible ticker.

---

## 3. Identifier table

All keys carry `eotg_`. No landed titles. Shared opinion modifiers carry no government prefix (invariant 7). Namespace `eotg_pmc` is reserved (`governments_v2.md` §3.3); **no event is built** (§11).

### 3.1 Script objects

| Type | Key | File | Batch |
|---|---|---|---|
| scripted trigger (role ladder, `governments_v2.md` §14.2) | `eotg_pmc_role_top` (landed, PMC, independent); `eotg_pmc_role_county` / `_duchy` / `_kingdom` (PMC, not independent, by `highest_held_title_tier`); `eotg_pmc_role_vassal` (any of the three); `eotg_pmc_is_landed_pmc` | `common/scripted_triggers/eotg_pmc_triggers.txt` | P1 |
| script value | `eotg_pmc_standing_value`, `eotg_pmc_standing_next_value`, `eotg_pmc_standing_start_value`, `eotg_pmc_standing_inherit_value` | `common/script_values/eotg_pmc_values.txt` | P1 |
| script value | `eotg_pmc_contract_pay_value` (50 + 3 × standing), `eotg_pmc_recruit_cost_value` (20), `eotg_pmc_recruit_spend_value` (−20), `eotg_pmc_battle_won_value` (2), `eotg_pmc_battle_lost_value` (−3), `eotg_pmc_drift_value` (−2) | same | P2/P3 |
| script value | `eotg_pmc_exit_prestige_value` (standing × 4, max 400), `eotg_pmc_exit_standing_loss_value` (−standing) | same | P4 |
| scripted effect | `eotg_pmc_change_standing_effect`, `eotg_pmc_sync_story_effect`, `eotg_pmc_init_effect`, `eotg_pmc_teardown_effect` | `common/scripted_effects/eotg_pmc_effects.txt` | P1 |
| character modifier | `eotg_pmc_standing_modifier` (§2.7) | `common/modifiers/eotg_pmc_modifiers.txt` | P1 |
| character modifier | `eotg_pmc_under_contract_modifier` (`levy_size = -0.25`; 2 years: the force is away on the client's business) | same | P3 |
| story cycle | `eotg_story_pmc_standing` | `common/story_cycles/eotg_pmc_story.txt` | P1 (monthly tick); P2 adds the yearly tick |
| on_action (mod) | `eotg_pmc_on_game_start`, `eotg_pmc_on_government_change`, `eotg_pmc_on_title_gain`, `eotg_pmc_on_death` | `common/on_action/eotg_pmc_on_actions.txt` | P1 |
| on_action (mod) | `eotg_pmc_on_combat_won`, `eotg_pmc_on_combat_lost` (on `on_combat_end_winner` / `_loser`) | same | P2 |
| decision (top) | `eotg_decision_pmc_take_contract` | `common/decisions/eotg_pmc_decisions.txt` | P3 |
| decision (vassal) | `eotg_decision_pmc_deliver_results` | same | P3 |
| decision (top, sink) | `eotg_decision_pmc_recruit_on_reputation` (OQ3) | same | P3 |
| character template | `eotg_pmc_operator_template` (prowess 12–18, martial 8–14, age 22–35) | `common/scripted_character_templates/eotg_pmc_templates.txt` | P3 |
| decision (entry) | `eotg_decision_pmc_adopt` | same decisions file | P4 |
| decision (exit) | `eotg_decision_pmc_stand_down` | same | P4 |
| government (edit) | `eotg_pmc_government`: add `possible_grant_vassal_governments` (§7) | `common/governments/eotg_pmc_government.txt` | P4 |
| variables | `eotg_pmc_standing` (character); `eotg_pmc_standing_shown` (story); scope value `eotg_pmc_standing_amount`; saved scope `eotg_pmc_predecessor` | — | P1 |
| vanilla variable (reused) | `changed_government_recently` (5 years; as the Cartel's transitions) | — | P4 |
| icons | vanilla only: modifier `martial_positive`; decision picture `decision_realm.dds`; story icon and background as §2.7 | — | none (no art debt) |

### 3.2 The story cycle in full

| Block | Content |
|---|---|
| `on_setup` | `set_variable eotg_pmc_standing_shown = 0` (init syncs right after) |
| `on_end` | `story_owner` removes `eotg_pmc_standing_modifier` (idempotent with teardown) |
| `on_owner_death` | `end_story = yes`. The heir gets a fresh story through `eotg_pmc_on_title_gain`. Standing has already moved to the heir in `eotg_pmc_on_death`. |
| `effect_group` `months = 1` (P1) | `first_valid`: (a) owner is not a landed PMC ruler → `story_owner = { eotg_pmc_teardown_effect = yes }`; (b) otherwise → `eotg_pmc_sync_story_effect`. |
| `effect_group` `years = 1` (P2) | Trigger: owner is a landed PMC ruler with `eotg_pmc_standing_value > 60`. Effect: `eotg_pmc_change_standing_effect = { AMOUNT = eotg_pmc_drift_value }`. **This tick is the drift's only cadence authority** (invariant 4, lesson 5). |

---

## 4. Decisions that move the resource (template §3.8 "full")

Shape for all: the Cartel's shipped decisions (`common/decisions/eotg_cartel_decisions.txt`), which follow `estate_governor_patrols_decision` (`G/common/decisions/dlc_decisions/ep_3/06_ep3_admin_decisions.txt:170-290`, via the Cartel spec §4). **Standing is not a `cost` key** (the supported keys per `_decisions.info:258-265`, via the Cartel spec), so it is gated in `is_valid` and moved in `effect`. Each decision's own `cooldown` is its only cadence authority.

### 4.1 Top tier: `eotg_decision_pmc_take_contract` ("Take a Contract")

| Field | Value |
|---|---|
| `is_shown` | `eotg_pmc_role_top = yes` |
| `is_valid` | `is_at_war = no`. Custom tooltip `eotg_decision_pmc_take_contract_free_tt`: `NOT = { has_character_modifier = eotg_pmc_under_contract_modifier }` (a state, not a cooldown: the force is still away). |
| `cooldown` | `{ years = 3 }` |
| `effect` | `add_gold = eotg_pmc_contract_pay_value` (50 + 3 × standing: 50 to 350; **reads the resource**). `eotg_pmc_change_standing_effect = { AMOUNT = 10 }` with custom tooltip `eotg_decision_pmc_take_contract_standing_tt`. `add_character_modifier = { modifier = eotg_pmc_under_contract_modifier years = 2 }`. |
| `ai_check_interval_by_tier` | barony 0, county 36, duchy 36, kingdom 36, empire 36, hegemony 36 |
| `ai_potential` | `eotg_pmc_role_top = yes` |
| `ai_will_do` | base 20. +20 if `gold < medium_gold_value` (a vanilla value the repo already reads). +10 if greedy. Factor 0 if `is_at_war = yes` or any neighbouring independent ruler is at war with the actor (UNVERIFIED-VANILLA: no cheap neighbour-threat check verified; the simple `is_at_war` gate is the fallback). |

**Why this decision:** it is the core verb. The pay scales with standing, so standing is worth having, and every sale raises it. The 2-year levy cut is the cost: the company is busy.

### 4.2 Vassal tier: `eotg_decision_pmc_deliver_results` ("Deliver Results")

| Field | Value |
|---|---|
| `is_shown` | `eotg_pmc_role_vassal = yes` (county, duchy and kingdom vassals: lesson 4) |
| `is_valid` | `is_at_war = no` |
| `cost` | `gold = minor_gold_value` (a vanilla value the repo already reads; the vassal pays its crews a bonus) |
| `cooldown` | `{ years = 5 }` |
| `effect` | Own: `eotg_pmc_change_standing_effect = { AMOUNT = 15 }`. If `liege = { government_has_flag = eotg_government_is_pmc }`: `liege = { eotg_pmc_change_standing_effect = { AMOUNT = 5 } }` ("results travel up the chain"). Custom tooltips for both. |
| `ai_check_interval_by_tier` | barony 0, county 60, duchy 48, kingdom 48, empire 0, hegemony 0 |
| `ai_potential` | `eotg_pmc_role_vassal = yes` |
| `ai_will_do` | base 10. +20 if `eotg_pmc_standing_value < 30`. +10 if ambitious. Factor 0 if `eotg_pmc_standing_value >= 80` or `gold < minor_gold_value`. |

**Why this decision:** it is a source at every non-top tier, and it makes the top's standing partly depend on its contractors (the role-ladder rule).

### 4.3 Top-tier sink: `eotg_decision_pmc_recruit_on_reputation` ("Recruit on Reputation"; OQ3)

| Field | Value |
|---|---|
| `is_shown` | `eotg_pmc_role_top = yes` |
| `is_valid` | custom tooltip `eotg_pmc_standing_value >= eotg_pmc_recruit_cost_value` (20) |
| `cooldown` | `{ years = 5 }` |
| `effect` | `eotg_pmc_change_standing_effect = { AMOUNT = eotg_pmc_recruit_spend_value }`. `create_character = { template = eotg_pmc_operator_template location = root.capital_province culture = root.culture faith = root.faith save_scope_as = eotg_pmc_recruit }`, `add_courtier = scope:eotg_pmc_recruit` (shape: the shipped `eotg_aug_kingpin_effects.txt` / `eotg_augmentation_effects.txt:1477-1484`). Toast naming the recruit. |
| `ai_will_do` | base 5. +10 if the court has fewer knights than its limit (UNVERIFIED-VANILLA: a knight-count trigger; fallback: drop the term). Factor 0 if `eotg_pmc_standing_value < 40` (keep a reserve). |

**Why this decision:** the second player-chosen sink, and the one that makes standing a currency rather than a score. The Operator is a generated character, so the decision stays map-agnostic.

---

## 5. Results in the field (P2)

### 5.1 Battle results

`on_combat_end_winner` / `on_combat_end_loser` (root = a combat side; `G/common/on_action/combat_on_actions.txt:12-14, :523-525`, via `eotg_augmentation_on_actions.txt:1870-1872`). Additive hooks to `eotg_pmc_on_combat_won` / `_lost`:
- `side_primary_participant = { if = { limit = { eotg_pmc_is_landed_pmc = yes } eotg_pmc_change_standing_effect = { AMOUNT = eotg_pmc_battle_won_value } } }` (or `_lost_value`).
- **UNVERIFIED-VANILLA:** the link from a combat side to its primary participant. The mod has only used `every_side_knight` on that scope. Check `_on_actions.info` / `combat_on_actions.txt` for the side's war-leader link (`side_primary_participant` expected). If none exists, the fallback is war results on the war on_actions (names unverified too) or dropping P2's battle feed.
- **Cost:** one trigger per battle per side. No event, so no cooldown.
- **Clamp guards spam:** a long winning war maxes at 100 and stops.

### 5.2 Drift

The story's yearly tick (§3.2) lowers standing above 60 by 2 a year: reputation needs refreshing. The tick is the only authority.

---

## 6. Entry and exit (template Q5)

Shapes: the Cartel's shipped `eotg_decision_cartel_adopt` / `eotg_decision_cartel_go_legitimate` (which cite `convert_to_mandala_government_decision`, `mandala_adopt_clan_government_decision`, `convert_whole_realm_to_feudalism_decision`). Both use `decision_group_type = major`.

### 6.1 Entry: `eotg_decision_pmc_adopt` ("Run the Realm as a Company")

| Field | Value |
|---|---|
| `is_shown` | `is_landed = yes`; `highest_held_title_tier > tier_barony`; `is_independent_ruler = yes`; `OR = { government_has_flag = government_is_feudal  government_has_flag = government_is_clan }`; `NOR` the four mod identity flags and `eotg_government_is_unclaimed` (the Cartel's form) |
| `is_valid` | custom tooltip `martial >= 12` (you already command), and custom tooltip: at least 3 knights (UNVERIFIED-VANILLA: knight count trigger; fallback: `martial >= 14` alone) |
| `is_valid_showing_failures_only` | no `changed_government_recently`; `is_at_war = no`; `is_tributary = no` |
| `cost` | `prestige = 200` (the Cartel's value, vanilla literal via it) |
| `effect` | `set_variable = { name = changed_government_recently years = 5 }`, then `change_government = eotg_pmc_government`. `on_government_change` runs the G1 law net and `eotg_pmc_init_effect` (standing starts at 40). **Only the ruler converts.** |
| `ai_potential` | **`always = no`** (as the Cartel, owner ruling 2026-10-20 OQ4; OQ7 here) |
| `ai_will_do` (for later) | base 0. +10 if `martial >= 16`. +10 if the ruler has a commander trait (UNVERIFIED-VANILLA: trait list). Factor 0 if `primary_title.tier > tier_duchy`. |

### 6.2 Exit: `eotg_decision_pmc_stand_down` ("Stand Down the Company")

| Field | Value |
|---|---|
| `is_shown` | `eotg_pmc_role_top = yes` |
| `is_valid_showing_failures_only` | no `changed_government_recently`; `is_at_war = no`; `NOT = { has_character_modifier = eotg_pmc_under_contract_modifier }` (finish the job first) |
| `cost` | `prestige = medium_prestige_value` (the Cartel's exit value) |
| `effect`, in order | (1) `add_prestige = eotg_pmc_exit_prestige_value` (standing × 4, max 400: **the reputation converts**, the herd → treasury refund pattern). (2) `eotg_pmc_change_standing_effect = { AMOUNT = eotg_pmc_exit_standing_loss_value }` (to 0). (3) `every_vassal_or_below` with `government_has_flag = eotg_government_is_pmc`: `change_government = feudal_government`. (4) `set_variable changed_government_recently` (5 years). (5) `change_government = feudal_government`. Teardown runs through `on_government_change`. |
| `ai_potential` | `eotg_pmc_role_top = yes`; `eotg_pmc_standing_value < 10` |
| `ai_will_do` | base 0. +10 if content. +10 if `martial < 8`. |

**Deferred:** v1's PMC → Corporation "evolution" decision (`governments_v2.md` §14.1 P3). It would convert standing into board influence. OQ8.

### 6.3 Forced and incidental transitions

| Case | Behaviour |
|---|---|
| Ruler dies, heir is PMC | `eotg_pmc_on_death` passes standing (§2.4). The story ends in `on_owner_death`. The heir's `on_title_gain` runs init (keeps the inherited value). |
| Heir is not PMC | The variable sits dormant on the heir. No story. |
| Ruler loses all land | The monthly tick sees a non-landed owner and calls teardown. The variable stays (dormant). |
| Becomes a vassal | Role changes from top to vassal. Take a Contract and Recruit stop (role-gated); Deliver Results appears. The story stays (every landed PMC ruler has one). |
| Debug decisions (G1) | Keep working: they go through `change_government`, so init and teardown run. |

---

## 7. AI and grant fields (template §3.14)

| Field | PMC G2 | Why |
|---|---|---|
| `possible_grant_vassal_governments` | `{ theocracy_government ecclesiastical_government }` | Parity with feudal (`00_government_types.txt:40`, via the Cartel spec §7, which also chose it). It offers only the faith's own theocratic type (`01_grant_title_rules.txt:37-46`, via the Cartel spec), so no faith key is needed. It does **not** list `feudal_government`. Closes assessment recommendation 3. |
| `grant_vassal_ai_will_do` | not set | Dead code unless another government lists the PMC (Cartel spec §7 reasoning). Revisit with the PMC → Corporation path (OQ8). |
| `ai = { }` | unchanged (`use_legends = yes`) | `use_great_projects` is banned. |
| `ai_will_do` on every own decision | §4, §6 | template §5.1 item 7 |

**How the AI lives on standing:**
- **Gains:** Take a Contract when poor and at peace; battles won (P2); Deliver Results for vassals.
- **Spends:** Recruit only above a 40 reserve.
- **Avoids churn:** cooldowns of 3 and 5 years; the under-contract state blocks overlap; drift only above 60.
- **Entry:** off (OQ7). **Exit:** only when standing is near zero.

---

## 8. Lore constraints

From `governments_v2.md` §5.1, §11 and §17, binding unchanged:
- **Mod-original but plausible** (LQ3). No PMC state is named at 866. **Never give the 7th Legion this government, and no text names it or LFTx** (succession spec §10).
- **No authority above the polity at 866** (ERRATA "LAW AT 866"): no registry, court, League, licence or arbitration. Contracts are enforced only by the parties. The client in "Take a Contract" is **unnamed**: "a client", "a paymaster".
- **No remote-kill, state augmentation programme or AI Secretariat framing** (ERRATA "CYBERNETICS AT 866").
- **The knight term is dynamic** (CB-48). Text that mentions knights uses `Custom('KnightCulture…')`. The Operator in §4.3 is a character, so the toast names them; it doesn't say "knight".
- **Prose says Bastion and Port** (`[castle|E]` / `[city|E]`), never "castle" or "city".
- **Canadian English** (honour, colour).
- **For the lore-keeper (needs-lore):**
  - Do "Standing", "The Company's Name", "Take a Contract", "Deliver Results", "Recruit on Reputation", "Run the Realm as a Company" and "Stand Down the Company" fit 866 voice?
  - Is selling force to an unnamed client compatible with the no-authority errata? (It is a private deal.)

---

## 9. Loc surface (`localization/english/eotg_pmc_l_english.yml`, UTF-8 with one BOM, bare `[x.GetName]`)

| Object | Keys | Batch |
|---|---|---|
| modifier | `eotg_pmc_standing_modifier`, `_desc`; `eotg_pmc_standing_scale_desc` | P1 |
| story | `eotg_story_pmc_standing`, `_info`, `_label`, `_min_label`, `_max_label`, `_tt` | P1 |
| decisions (×5) | `<key>`, `_desc`, `_tooltip`, `_confirm`; plus `eotg_decision_pmc_take_contract_free_tt`, `_standing_tt`; `eotg_decision_pmc_deliver_results_standing_tt`, `_liege_tt`; `eotg_decision_pmc_recruit_on_reputation_standing_tt`, `_toast`, `_toast_desc`; `eotg_decision_pmc_adopt_martial_tt`; `eotg_decision_pmc_stand_down_effect_tt` | P3/P4 |
| modifier | `eotg_pmc_under_contract_modifier`, `_desc` | P3 |

**`replace/` overrides: none.** **G1 loc touched: none.**

---

## 10. Build batches (scripter → localizer → lore-keeper → QA, per batch)

| Batch | Contents | Static gate | In-game tests |
|---|---|---|---|
| **P1, resource core** (**built** on `claude/governments-g2-three-cloud`, unvalidated) | role-ladder triggers; P1 script values; change, sync, init, teardown effects; `eotg_pmc_standing_modifier`; story (monthly tick); `eotg_pmc_on_actions.txt` (game start, after lobby, government change, title gain, death inheritance); P1 loc | Tiger, PX, vocab; `grep "name = eotg_pmc_standing"` returns one line, inside `eotg_pmc_change_standing_effect` | V-P1–V-P5 |
| **P2, field results** | combat hooks; story yearly drift tick; P2 values | the side link verified (§5.1); drift has one authority | V-P6, V-P7 |
| **P3, decisions** | Take a Contract, Deliver Results, Recruit on Reputation (OQ3); under-contract modifier; operator template | `ai_will_do` on all three; each moves standing through the change effect only | V-P8–V-P11 |
| **P4, transitions and grants** | entry and exit; `possible_grant_vassal_governments` | entry `ai_potential = always = no` | V-P12–V-P14 |
| **P5, loc and review** | §9 loc for P2–P4; lore-keeper names; QA full pass | template §5.1 items 1–8 | V-P15, V-P16 |

**Save compatibility (template §4.10):** P1–P3 add keys only. P4 edits a shipped government (adds a grant field), which is not save-breaking. Note it in the P4 commit.

---

## 11. Proposed events: OWNER APPROVAL REQUIRED (not in the build list)

Owner rule: every new event, option or beat needs approval. None is in §10. Each moves or reads standing (invariant 5). If approved: namespace `eotg_pmc`, loc `eotg_pmc_NNNN_t` / `_desc` / `_a`, cooldown only in the story ticks or a mod on_action on `yearly_playable_pulse`.

| # | Proposal | Fires from | Standing coupling |
|---|---|---|---|
| E1 | **The Client Won't Pay.** During a contract, the paymaster withholds the last instalment. Options: walk away (−5 standing, keep peace); collect by force (a claim or opinion hit on a random independent neighbour; +5 standing if the ruler's martial ≥ 14); renegotiate (gold back, +0). | story yearly tick while under contract | moves and reads |
| E2 | **A Rival Company.** A neighbouring PMC undercuts the price. Options: match it (lower the next contract's pay, keep standing); outbid on reputation (spend 10 standing, next contract +50% pay). | story yearly tick, top, standing ≥ 50 | moves and reads |
| E3 | **Atrocity in the Field.** A contractor vassal's crew commits an outrage on a contract. Options: discipline them (vassal opinion −20, standing +5); cover it up (standing −10 if discovered later, a secret). | Deliver Results effect (a counter on the vassal) | moves and reads |
| E4 | **The Commander's Last Order.** The dying commander names a successor on results. Options shift standing between the designated heir and the oldest child. | `eotg_pmc_on_death` | moves |
| E5 | **The v1 lift.** v1 PMC events (`OLD PROJECT VERSION/events/eotg_pmc_*`, 32 events), each audited to move or read standing or dropped (`governments_v2.md` §14.1 P2). | `yearly_playable_pulse` via a mod on_action | audit per event |

---

## 12. Definition of done

**Static (eotg-qa):**
1. Tiger clean except the CLAUDE.md known-benign list (expected: story `visible` / `icon` / `background` / `visualization`). PX LSP and `px_vocab_check.py` clean over the new files. PX `locCoverage` shows no missing `eotg_` key.
2. `grep -rn "name = eotg_pmc_standing$\|name = eotg_pmc_standing " common` returns one writer, inside `eotg_pmc_change_standing_effect`. No `var:eotg_pmc_standing` outside `eotg_pmc_standing_value`, the inheritance value and `eotg_pmc_sync_story_effect`.
3. Every PMC decision reads standing (`is_valid` or `ai_will_do`) **and** moves it through the change effect.
4. Every decision and modifier has loc. All five decisions have `ai_will_do`.
5. `grep -rnE 'eotg_[ekdcb]_'` is empty. No title, culture, faith, province or character key in a new file. No `has_government` in any new trigger.
6. The drift has one cadence authority (the story's yearly `effect_group`).

**In game (human, British Isles sub-mod, `-debug_mode`). Run alongside CB-49:**

| ID | Check | Pass |
|---|---|---|
| V-P1 | error.log shows nothing from the new files. The story, modifier and on_actions load. | yes |
| V-P2 | Raoul (d_valois) has `eotg_pmc_standing_modifier` reading "+0.4 monthly prestige, +4% knight effectiveness" (40 standing) and a visible "The Company's Name" story whose counter reads 40. A PMC vassal, if any, reads 20. | yes |
| V-P3 | Console: run the change effect through a debug path (or `set_variable`, then the monthly tick) — the counter matches within a month; values below 0 or above 100 clamp. | yes |
| V-P4 | `kill` Raoul: the heir has 30 standing (75% of 40) or their own higher value, a new story and the modifier. A landless heir keeps the inherited value instead of the start value. | yes |
| V-P5 | Debug "Become feudal" on Raoul: story and modifier are gone; `eotg_pmc_standing` remains on the character (dormant). "Become a PMC" again: the old value returns, not 40. | yes |
| V-P6 | A PMC wins a battle as war leader: +2. Loses one: −3. | yes (P2) |
| V-P7 | Set standing 80, wait a year: 78. At 60, no drift. | yes (P2) |
| V-P8 | Take a Contract: gold +50 + 3 × standing, standing +10, levy −25% for 2 years; blocked while under contract; 3-year cooldown. | yes (P3) |
| V-P9 | A PMC vassal takes Deliver Results: own +15, PMC liege +5, minor gold paid. | yes (P3) |
| V-P10 | Recruit on Reputation: −20 standing, a skilled Operator joins the court; blocked below 20. | yes (P3) |
| V-P11 | Raoul does not see Deliver Results; vassals do not see Take a Contract or Recruit. | yes (P3) |
| V-P12 | An independent feudal ruler with martial ≥ 12 takes the entry decision: becomes PMC with the PMC law, story, modifier and 40 standing; `changed_government_recently` set. | yes (P4) |
| V-P13 | Raoul takes Stand Down: prestige + 4 × standing (max 400); standing 0; PMC vassals become feudal; the law is replaced. | yes (P4) |
| V-P14 | Raoul grants a temple county: only his faith's theocratic type is offered. A castle county grant defaults to PMC. | yes (P4) |
| V-P15 | 50-year observer run: the AI PMC takes contracts and stays within 0–100; no AI ruler takes the entry decision. | yes / recorded |
| V-P16 | Save and reload: standing, story counter and modifier survive. | yes |

---

## 13. Deferred

| Item | Why | Trigger to revisit |
|---|---|---|
| PMC → Corporation evolution decision | v1 §6.3; needs both resources built | OQ8 |
| Standing in vassal contracts (a third obligation: "field commission") | `governments_v2.md` §14.1 P2 | after V-P15 |
| A standing-weighted succession | Rejected by the succession spec §11 (no mirroring); designate heir already gives merit | only if the owner asks |
| Standing-gated mercenary prices | No verified per-character merc-cost hook beyond the existing modifier | after V-P15 |
| Cybernetics "hired crew" kingpin weight; Frontier "Guns for Hire" branch | `governments_v2.md` §5.1 Coupling, optional | cybernetics / Frontier follow-ups |
| Proper icon | Art debt (human) | Gate 4 |

---

## 14. Owner questions (each with a recommended default)

- **OQ1, resource confirmed as a scripted 0–100 variable (recommended: yes).** As `governments_v2.md` §2.
- **OQ2, standing passes 75% to the primary heir (recommended: yes).** The company's name outlives the commander. Alternative: 100% (the name is the company's alone) or 50%.
- **OQ3, include the Recruit on Reputation sink (recommended: yes).** It is a third decision beyond the required two, and the only player-chosen sink. Without it, standing is spent only by drift and defeat.
- **OQ4, a visible story (recommended: yes).** The mod's third visible story. Alternative: the modifier alone.
- **OQ5, start values 40 (top) / 20 (vassal) (recommended: yes).**
- **OQ6, first-pass numbers (recommended: approve).** Contract +10 and 50 + 3 × standing gold, 3-year cooldown, 2-year −25% levy; Deliver +15 / +5 for minor gold; Recruit −20; battles +2 / −3; drift −2 above 60; exit ×4 max 400; modifier +1 prestige/month and +10% knight effectiveness at 100.
- **OQ7, AI adoption of the PMC (recommended: not yet).** As the Cartel: player-only until V-G11 (leakage) has run.
- **OQ8, a PMC → Corporation evolution decision (recommended: defer).** Build after both resources exist.
- **OQ9, the events in §11 (recommended: none yet).**
