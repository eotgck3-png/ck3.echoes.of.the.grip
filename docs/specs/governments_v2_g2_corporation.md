# Spec: Governments v2, Phase G2: the Corporation (`eotg_corporation_government`)

**Author:** cloud session (architect role), 2026-11-03. **Status:** draft, **unvalidated** (no game, Tiger or PX in the cloud). Next: eotg-lore-keeper (names, §8), then owner rulings (§14), then eotg-scripter in batches (§10). Batch CO1 is built on branch `claude/governments-g2-three-cloud` (§10).
**Parent specs:** `docs/specs/governments_v2.md` (§2, §5.2, §14), `docs/specs/government_template.md` (§2, §3.8, §3.11, §3.14, §3.15, §9). **Assessment:** `docs/qa/government_assessment_2026-10-11/corporation.md`. **Pattern:** `docs/specs/governments_v2_g2_cartel.md` (shipped). **Succession:** `docs/specs/governments_v2_g2_succession.md` §5.1 (the board election, built) and §2 (its board-influence hook).
**Vanilla:** CK3 1.20.1.1. **This session could not read vanilla.** Vanilla citations are either copied from shipped, locally validated mod files and specs ("via <file>") or marked `UNVERIFIED-VANILLA`.
**Scope:** the Corporation only. Internal keys use the prefix `eotg_corporation_`; the resource keeps its reserved name `eotg_corp_board_influence` (`governments_v2.md` §2, §3.3).

---

## 0. Kind of build (template §2 rule)

**A distinct government, not a reskin.** Its core verb differs from feudal's "conquer, then inherit":

> A CEO **spends their hold on the board** to push major acts through, and earns it back with results, while the directors below **court the board** to loosen that hold.

Vanilla's nearest verb is administrative influence ("you will have to engage in politics", template §2). Influence itself is not used: it needs the admin stack, and its top-bar display is gated on the mechanic (template §8.1, T11 unrun). G1 built none of this (assessment GAP G3).

---

## 1. Purpose & gate

G2 makes the board a number with two sides:
- **The CEO spends board influence** on a restructuring (a top-tier decision): more income, unhappy directors.
- **Directors build their own board influence** (a vassal-tier decision), and every gain **erodes the CEO's hold**: the board's favour is contested.
- **Results feed the hold.** A solvent, peaceful company gains each year; a company in debt loses.
- **The election reads it** (batch CO5). The board election built in the succession pass already weights a councillor seat as a proxy (`eotg_corporation_su_vote_board`). CO5 replaces that proxy with board-influence bands, so the number decides succession.

It also adds the entry and exit decisions, the grant fields and the display.

**Gate: 2, under the mod-exclusive exemption** (owner, 2026-10-08, `CLAUDE.md`). **Not blocked by Gate 1.** Map-agnostic. The British Isles test sub-mod supplies the Corporation: Hoël, k_brittany, with Konan II of d_brittany below him (`isles_assignments.csv:69-70`).

**Soft dependencies:** CB-49 (G1 in-game checks, especially V-G3, V-G17 for the city shape) and the succession pass's V-SU checks (for CO5).

---

## 2. Signature resource: `eotg_corp_board_influence` (scripted)

### 2.1 Decision: a dedicated variable, not vanilla influence

`governments_v2.md` §2 fixes `eotg_corp_board_influence`, a character variable from 0 to 100: **the ruler's hold on the board**. Reasons:
1. **Vanilla influence is admin-coded.** All five vanilla governments with `government_has_influence` are `mechanic_type = administrative`, and the top-bar widget keys on the mechanic (template §8.1, confirmed there). A non-admin Corporation would lose the HUD readout, and spending is unknown (T11).
2. **It must be per character and contested.** Directors hold their own value, which the election reads. Vanilla influence would work for that, but with unknown admin side effects.
3. **The template default:** a scripted pseudo-currency with a scaled modifier and a story counter, no `gui/`.

The §14.5 influence probe (T11) is **not needed** for this design. OQ1 lets the owner still ask for it.

### 2.2 Identifiers and authority

| Item | Key | Notes |
|---|---|---|
| The resource (character variable) | `eotg_corp_board_influence` | 0 to 100. On every landed Corporation ruler at every tier. **The reserved name is kept** (`governments_v2.md` §3.3), so it is shorter than the other keys. |
| Change effect (**the only writer**) | `eotg_corporation_change_board_influence_effect = { AMOUNT = <number or named value> }` | §2.3. The name follows `governments_v2.md` §2's rule `eotg_<gov>_change_<resource>_effect` and the assessment's recommendation. |
| Reader | `eotg_corporation_board_influence_value` | `var:eotg_corp_board_influence`, 0 when unset. All reads go through it, except the inheritance value and the story sync (PMC spec §2.2). |
| Clamp | `eotg_corporation_board_influence_next_value` | reader + `scope:eotg_corporation_board_amount`, clamped to `[0, 100]` |
| Start value | `eotg_corporation_board_influence_start_value` | 50 for `eotg_corporation_role_top` (the CEO starts holding the board), otherwise 20 (OQ5) |
| Inheritance | `eotg_corporation_board_influence_inherit_value` | heir scope: `max(0, 0.5 × predecessor's − heir's own)` (§2.4) |
| Story display mirror | `eotg_corporation_board_shown` (story variable) | display only |

### 2.3 The change effect

```
eotg_corporation_change_board_influence_effect = {
    save_scope_value_as = { name = eotg_corporation_board_amount  value = $AMOUNT$ }
    set_variable = { name = eotg_corp_board_influence  value = eotg_corporation_board_influence_next_value }
    eotg_corporation_sync_story_effect = yes
}
```
Rules as the PMC spec §2.3 and the Cartel amendment: AMOUNT is a number or a named value; callers gate spends in `is_valid`; every visible caller adds a custom tooltip naming the change.

### 2.4 Inheritance: the board must be won again

`eotg_corporation_on_death` (root is about to die): if root is a Corporation ruler with board influence and `exists = primary_heir`, save root as `scope:eotg_corporation_predecessor` and give `primary_heir` `eotg_corporation_change_board_influence_effect = { AMOUNT = eotg_corporation_board_influence_inherit_value }`. The heir ends with **the higher of its own value and half the predecessor's.**

- **Under the board election, `primary_heir` is the current vote leader**, and the vote is resolved at death with the same votes (succession spec §5.3 note, written for the Cartel and true of every election). So the influence lands on the elected successor.
- Init keeps an inherited value (it sets the start value only when the variable is unset), as the PMC spec §2.4.
- The 50% (lower than the PMC's 75%) is the fiction: a new chief must win the board.

### 2.5 Sources and sinks (template §3.11 "full")

| Direction | What | Who | Amount | Batch |
|---|---|---|---|---|
| Source (passive) | yearly: solvent and at peace (`gold > 0`, `is_at_war = no`) | any tier | +3/year | CO2 |
| Sink (penalty) | yearly: in debt (`gold < 0`) | any tier | −5/year | CO2 |
| Sink (choice) | Push Through a Restructuring (top decision, §4.1) | top | −25 | CO3 |
| Source (choice) | Court the Board (vassal decision, §4.2) | vassal | +15 own | CO3 |
| Sink (contest) | the same decision, **on the Corporation liege** ("every director's gain loosens the chief's hold") | top | −5 | CO3 |
| Conversion | Dissolve the Board (exit, §6.2) | top | all influence → legitimacy (×2, max 200) | CO4 |
| Read | the board election's vote strength (§5) | electors | bands at 40 / 75 | CO5 |

All numbers are first-pass (OQ6).

### 2.6 Init and teardown

As the PMC spec §2.6, with Corporation keys:
- `eotg_corporation_init_effect`: create `eotg_story_corporation_board` if absent; if `eotg_corp_board_influence` is unset, `eotg_corporation_change_board_influence_effect = { AMOUNT = eotg_corporation_board_influence_start_value }`; add `eotg_corporation_board_modifier` if missing; sync. Called from `eotg_corporation_on_game_start` (also after the lobby), `_on_government_change` (new government is Corporation), `_on_title_gain` (landed Corporation without the story).
- `eotg_corporation_teardown_effect`: end the story, remove the modifier. **The variable is not touched** (dormant; one writer). Called from `_on_government_change` (old government Corporation, `scope:old_government = { government_type_has_flag = eotg_government_is_corporation }`) and the story's monthly self-heal.

### 2.7 Display: layers 1 + 4, no `gui/`

**Layer 1.** `common/modifiers/eotg_corporation_modifiers.txt`:
```
eotg_corporation_board_modifier = {
    icon = stewardship_positive
    monthly_income_mult = 0.001     # +10% income at 100
    vassal_opinion = 0.1            # +10 vassal opinion at 100: the board backs the chief
    scale = {
        value = eotg_corporation_board_influence_value
        desc = eotg_corporation_board_scale_desc
        display_mode = scaled
    }
}
```
`stewardship_positive`, `monthly_income_mult` and `vassal_opinion` are used by shipped mod files. **UNVERIFIED-VANILLA:** fractional per-unit values under `display_mode = scaled` (PMC spec §2.7).

**Layer 4.** `common/story_cycles/eotg_corporation_story.txt`, key `eotg_story_corporation_board` ("The Board"): `visible = yes`; icon `story_icon_palace_politics.dds`; background `gfx/interface/illustrations/event_scenes/councilchamber.dds` (already used by a shipped mod file); `basic_counter` on `eotg_corporation_board_shown` (0–100); `modifiers = { eotg_corporation_board_modifier }`; `custom_string_key = eotg_story_corporation_board_info`. Monthly tick: self-heal or sync (CO1); yearly tick (CO2) for the results feed. **OQ4** (visible story).

---

## 3. Identifier table

### 3.1 Script objects

| Type | Key | File | Batch |
|---|---|---|---|
| scripted trigger (role ladder) | `eotg_corporation_role_top`, `_role_county`, `_role_duchy`, `_role_kingdom`, `_role_vassal`; `eotg_corporation_is_landed_corporation` | `common/scripted_triggers/eotg_corporation_triggers.txt` | CO1 |
| script value | `eotg_corporation_board_influence_value`, `_next_value`, `_start_value`, `_inherit_value` | `common/script_values/eotg_corporation_values.txt` | CO1 |
| script value | `eotg_corporation_results_gain_value` (3), `eotg_corporation_debt_loss_value` (−5) | same | CO2 |
| script value | `eotg_corporation_restructure_cost_value` (25), `eotg_corporation_restructure_spend_value` (−25), `eotg_corporation_court_gain_value` (15), `eotg_corporation_court_erosion_value` (−5) | same | CO3 |
| script value | `eotg_corporation_exit_legitimacy_value` (influence × 2, max `major_legitimacy_gain`, the Cartel's form), `eotg_corporation_exit_loss_value` (−influence) | same | CO4 |
| scripted effect | `eotg_corporation_change_board_influence_effect`, `eotg_corporation_sync_story_effect`, `eotg_corporation_init_effect`, `eotg_corporation_teardown_effect` | `common/scripted_effects/eotg_corporation_effects.txt` | CO1 |
| character modifier | `eotg_corporation_board_modifier` | `common/modifiers/eotg_corporation_modifiers.txt` | CO1 |
| character modifier | `eotg_corporation_restructured_modifier` (`monthly_income_mult = 0.1`, `build_gold_cost = -0.1`; 5 years) | same | CO3 |
| opinion modifier (shared, no government prefix) | `eotg_restructured_opinion` (−10, decaying over 5 years) | `common/opinion_modifiers/eotg_corporation_opinions.txt` | CO3 |
| story cycle | `eotg_story_corporation_board` | `common/story_cycles/eotg_corporation_story.txt` | CO1 / CO2 |
| on_action (mod) | `eotg_corporation_on_game_start`, `_on_government_change`, `_on_title_gain`, `_on_death` | `common/on_action/eotg_corporation_on_actions.txt` | CO1 |
| decision (top) | `eotg_decision_corporation_restructure` | `common/decisions/eotg_corporation_decisions.txt` | CO3 |
| decision (vassal) | `eotg_decision_corporation_court_board` | same | CO3 |
| decision (entry) | `eotg_decision_corporation_adopt` | same | CO4 |
| decision (exit) | `eotg_decision_corporation_dissolve_board` | same | CO4 |
| government (edit) | add `possible_grant_vassal_governments` (§7) | `common/governments/eotg_corporation_government.txt` | CO4 |
| election (edit) | `eotg_corporation_elective`: replace `eotg_corporation_su_vote_board` (councillor proxy) with `eotg_corporation_su_vote_board` bands reading the resource (§5) | `common/succession_election/eotg_government_elections.txt` | CO5 |
| variables | `eotg_corp_board_influence` (character); `eotg_corporation_board_shown` (story); scope value `eotg_corporation_board_amount`; saved scope `eotg_corporation_predecessor` | — | CO1 |

### 3.2 The story cycle in full

| Block | Content |
|---|---|
| `on_setup` | `set_variable eotg_corporation_board_shown = 0` (init syncs right after) |
| `on_end` | `story_owner` removes `eotg_corporation_board_modifier` |
| `on_owner_death` | `end_story = yes` (influence already moved in `_on_death`) |
| `effect_group` `months = 1` (CO1) | `first_valid`: (a) owner not a landed Corporation ruler → teardown; (b) otherwise → sync |
| `effect_group` `years = 1` (CO2) | `first_valid`: (a) owner landed Corporation, `gold < 0` → change by `eotg_corporation_debt_loss_value`; (b) owner landed Corporation, `gold > 0`, `is_at_war = no` → change by `eotg_corporation_results_gain_value`. **The only cadence authority** for the results feed. |

---

## 4. Decisions that move the resource

Shape: the Cartel's shipped decisions. Board influence is not a `cost` key; gate in `is_valid`, move in `effect`.

### 4.1 Top tier: `eotg_decision_corporation_restructure` ("Push Through a Restructuring")

| Field | Value |
|---|---|
| `is_shown` | `eotg_corporation_role_top = yes` |
| `is_valid` | custom tooltip `eotg_corporation_board_influence_value >= eotg_corporation_restructure_cost_value` (25) |
| `cooldown` | `{ years = 5 }` |
| `effect` | `eotg_corporation_change_board_influence_effect = { AMOUNT = eotg_corporation_restructure_spend_value }`. `add_character_modifier = { modifier = eotg_corporation_restructured_modifier years = 5 }`. `every_vassal` with `government_has_flag = eotg_government_is_corporation`: `add_opinion = { modifier = eotg_restructured_opinion target = root }`. Custom tooltips. |
| `ai_check_interval_by_tier` | barony 0, county 60, duchy 36, kingdom 36, empire 36, hegemony 36 |
| `ai_potential` | `eotg_corporation_role_top = yes` |
| `ai_will_do` | base 10. +20 if `eotg_corporation_board_influence_value >= 60`. +10 if greedy or ambitious. Factor 0 if `eotg_corporation_board_influence_value < 45` (keep 20 after the spend, so the election hold survives). |

**Why this decision:** the CEO's sink and the government's "major act": real money now, paid for with the hold on the board and the directors' goodwill.

### 4.2 Vassal tier: `eotg_decision_corporation_court_board` ("Court the Board")

| Field | Value |
|---|---|
| `is_shown` | `eotg_corporation_role_vassal = yes` |
| `cost` | `gold = medium_gold_value` (a vanilla value the repo already reads) |
| `cooldown` | `{ years = 5 }` |
| `effect` | Own: `eotg_corporation_change_board_influence_effect = { AMOUNT = eotg_corporation_court_gain_value }` (+15). If `liege = { eotg_corporation_role_top = yes }`: `liege = { eotg_corporation_change_board_influence_effect = { AMOUNT = eotg_corporation_court_erosion_value } }` (−5). Custom tooltips for both. |
| `ai_check_interval_by_tier` | barony 0, county 60, duchy 48, kingdom 48, empire 0, hegemony 0 |
| `ai_potential` | `eotg_corporation_role_vassal = yes` |
| `ai_will_do` | base 5. +15 if ambitious. +10 if the liege's opinion of root is below 0 (UNVERIFIED-VANILLA: `opinion` form; the Cartel uses `"opinion(scope:x)"` in a value). +10 if `eotg_corporation_board_influence_value < 30`. Factor 0 if `gold < medium_gold_value` or `eotg_corporation_board_influence_value >= 80`. |

**Why this decision:** a source at every non-top tier, and the "directors scheme for the board's favour" fiction as a number. A director with high influence gets more weight in the next election (CO5).

---

## 5. The election reads the board (CO5)

The succession pass built `eotg_corporation_elective` with vote strength +1 for `eotg_corporation_su_vote_board` "councillor of the holder" and named it **the board-influence hook** (succession spec §2, §5.1). CO5 replaces that one modifier's condition, keeping its loc key:

| Modifier | Add | Condition (new) |
|---|---|---|
| `eotg_corporation_su_vote_board` | +1 | `eotg_corporation_board_influence_value >= 40` |
| `eotg_corporation_su_vote_board_major` (new desc key) | +1 | `eotg_corporation_board_influence_value >= 75` |

- **Councillors who are not landed Corporation rulers have no variable**, so they lose the +1 they had. That is the point: a seat at the table is not the same as a hold on the board. OQ9 asks whether to keep the councillor +1 alongside.
- **The holder's own influence** feeds its own vote strength through the same modifiers, on top of `eotg_gov_su_vote_chair`.
- **Ownership:** the election file belongs to the succession pass. CO5 is a separate batch with its own QA (V-SU re-run), and must not land before CO1 is validated in game.

---

## 6. Entry and exit

Shapes: the Cartel's shipped transitions. `decision_group_type = major`.

### 6.1 Entry: `eotg_decision_corporation_adopt` ("Incorporate the Realm")

| Field | Value |
|---|---|
| `is_shown` | `is_landed = yes`; `highest_held_title_tier > tier_barony`; `is_independent_ruler = yes`; `OR = { government_has_flag = government_is_feudal  government_has_flag = government_is_clan }`; `NOR` the four mod identity flags and `eotg_government_is_unclaimed` |
| `is_valid` | custom tooltip `stewardship >= 12`; custom tooltip `gold >= medium_gold_value` (capital to put on the books) |
| `is_valid_showing_failures_only` | no `changed_government_recently`; `is_at_war = no`; `is_tributary = no` |
| `cost` | `prestige = 200` |
| `effect` | `set_variable changed_government_recently` (5 years); `change_government = eotg_corporation_government`. Init sets influence to 50. **Only the ruler converts.** **The capital stays as it is**: a castle-capital ruler becomes a city-primary government with a castle capital. UNVERIFIED-VANILLA (V-G17): whether that costs an invalid-holding penalty. OQ10 asks whether entry should require a Port capital. |
| `ai_potential` | **`always = no`** (OQ7) |
| `ai_will_do` (for later) | base 0. +10 if `stewardship >= 16`. +10 if greedy. Factor 0 if `primary_title.tier > tier_kingdom`. |

### 6.2 Exit: `eotg_decision_corporation_dissolve_board` ("Dissolve the Board")

| Field | Value |
|---|---|
| `is_shown` | `eotg_corporation_role_top = yes` |
| `is_valid_showing_failures_only` | no `changed_government_recently`; `is_at_war = no` |
| `cost` | `prestige = medium_prestige_value` |
| `effect`, in order | (1) `add_legitimacy = eotg_corporation_exit_legitimacy_value` (influence × 2, max 200: the hold on the board becomes personal standing). (2) `eotg_corporation_change_board_influence_effect = { AMOUNT = eotg_corporation_exit_loss_value }` (to 0). (3) `every_vassal_or_below` with the Corporation flag → `change_government = feudal_government`. (4) `changed_government_recently`. (5) `change_government = feudal_government`. |
| `ai_potential` | `eotg_corporation_role_top = yes`; `eotg_corporation_board_influence_value < 10` |
| `ai_will_do` | base 0. +10 if `gold < 0`. |

### 6.3 Forced and incidental transitions

As the PMC spec §6.3. In addition: **an elected heir from a cadet line** gets the influence through `primary_heir`, whatever the dynasty branch.

---

## 7. AI and grant fields

| Field | Corporation G2 | Why |
|---|---|---|
| `possible_grant_vassal_governments` | `{ theocracy_government ecclesiastical_government }` | As the Cartel and PMC. Does not list feudal. |
| `grant_vassal_ai_will_do` | not set | dead code (Cartel spec §7) |
| `ai = { }` | unchanged | — |

**How the AI lives on board influence:** gains it yearly when solvent; CEOs restructure only above 45; directors court only with gold to spare and below 80; cooldowns of 5 years; entry off; exit only when broken.

---

## 8. Lore constraints

- **A company state run by a board, polished at the top and cut-throat below** (`governments_v2.md` §5.2, lore ruling). **Text never names a corporation**: not Helix, not P&D (LQ4; cybernetics never-name list).
- **Helix's 866 structure is not "board and CEO"** (ERRATA "HELIX CORPORATION"). Text must not read as Helix's.
- **No authority above the polity** (ERRATA "LAW AT 866"): no registry, exchange, court or League. The board is internal to the realm.
- **Clinic coupling** (if ever): the ruler's own price only, never "programme" or "subsidy" (§5.2 rule).
- Bastion and Port; Canadian English; the knight term is dynamic ("Specialist").
- **For the lore-keeper:** do "Board Influence", "The Board", "Push Through a Restructuring", "Court the Board", "Incorporate the Realm" and "Dissolve the Board" fit 866 voice? Is "CEO" in loc acceptable beyond the rank table (it is already the top rank)?

---

## 9. Loc surface (`localization/english/eotg_corporation_l_english.yml`, one BOM)

| Object | Keys | Batch |
|---|---|---|
| modifier | `eotg_corporation_board_modifier`, `_desc`; `eotg_corporation_board_scale_desc` | CO1 |
| story | `eotg_story_corporation_board`, `_info`, `_label`, `_min_label`, `_max_label`, `_tt` | CO1 |
| decisions (×4) | `<key>`, `_desc`, `_tooltip`, `_confirm`; `eotg_decision_corporation_restructure_influence_tt`, `_effect_tt`; `eotg_decision_corporation_court_board_gain_tt`, `_erosion_tt`; `eotg_decision_corporation_adopt_stewardship_tt`, `_gold_tt`; `eotg_decision_corporation_dissolve_board_effect_tt` | CO3/CO4 |
| modifiers | `eotg_corporation_restructured_modifier`, `_desc` | CO3 |
| opinion | `eotg_restructured_opinion` | CO3 |
| election | `eotg_corporation_su_vote_board` (text update: "Hold on the board"), `eotg_corporation_su_vote_board_major` | CO5 |

---

## 10. Build batches


> **Amendment, 2026-11-03 (cloud build of CO2–CO5, unvalidated).**
> 1. **Built:** CO2 (story yearly results tick), CO3 (Restructure, Court the Board, `eotg_corporation_restructured_modifier`, shared `eotg_restructured_opinion`), CO4 (entry, exit, grant field), CO5 (the election's vote strength reads board influence), and all their loc (the CO6 loc part). CO6's lore-keeper and QA review remain.
> 2. **CO5 as built:** `eotg_corporation_su_vote_board` keeps its key and now fires at influence ≥ 40 for **any** elector, the holder included. A new `eotg_corporation_su_vote_board_major` fires at ≥ 75. The councillor condition is gone (OQ9 default). Candidates and electors are unchanged (owner ruling: dynasty-only candidates, unrestricted electors). Loc "Seat on the board" became "Hold on the board (40+)".
> 3. **Deviation:** the §4.2 "+10 if the liege dislikes root" AI term is not built (no opinion-comparison trigger form in v2 script).
> 4. **The yearly tick** uses `first_valid` with the landed check in each branch, not a group-level `trigger` beside `first_valid` (the Cartel uses one form or the other, never both).

| Batch | Contents | Static gate | In-game tests |
|---|---|---|---|
| **CO1, resource core** (**built**, unvalidated) | role ladder; CO1 values; change, sync, init, teardown; board modifier; story (monthly tick); on_actions incl. death inheritance; CO1 loc | Tiger, PX, vocab; one writer of `eotg_corp_board_influence` | V-CO1–V-CO5 |
| **CO2, results feed** (**built (cloud, unvalidated), 2026-11-03**) | story yearly tick; CO2 values | one cadence authority | V-CO6 |
| **CO3, decisions** (**built (cloud, unvalidated), 2026-11-03**) | Restructure, Court the Board; restructured modifier; shared opinion | `ai_will_do`; moves only through the change effect | V-CO7–V-CO9 |
| **CO4, transitions and grants** (**built (cloud, unvalidated), 2026-11-03**) | entry, exit, grant field | entry `ai_potential = always = no` | V-CO10–V-CO12 |
| **CO5, the election reads the board** (**built (cloud, unvalidated), 2026-11-03**) | election vote-strength edit (§5) | V-SU re-run | V-CO13 |
| **CO6, loc and review** (loc **built (cloud, unvalidated), 2026-11-03**; review pending) | §9 loc for CO2–CO5; lore review; QA | template §5.1 | V-CO14, V-CO15 |

---

## 11. Proposed events: OWNER APPROVAL REQUIRED (not in the build list)

| # | Proposal | Fires from | Coupling |
|---|---|---|---|
| E1 | **The Board Meets.** The projected election winner changes. Options: back the frontrunner (+5 influence, opinion with the old favourite −10); lobby against them (−10 influence, the frontrunner's own influence −10). | story yearly tick, top, when the vote leader differs from last year (a stored scope on the story) | moves and reads |
| E2 | **A Director Overreaches.** A vassal with influence ≥ 70 demands a seat on the council. Options: grant it (vassal +10, CEO −10); refuse (vassal opinion −25, a faction risk). | story yearly tick, top | moves and reads |
| E3 | **Quarterly Losses.** Debt for two years running. Options: cut costs (−levy, +5 influence); borrow (gold, −10 influence). | CO2 debt branch, second year | moves and reads |
| E4 | **Hostile Bid.** A neighbouring Corporation offers to buy a director's loyalty. | story yearly tick, vassal with influence ≥ 50 | moves |
| E5 | **The v1 lift.** v1 Corporation events (33), each audited to move or read influence or dropped. | `yearly_playable_pulse` via a mod on_action | audit per event |

---

## 12. Definition of done

**Static:** as the PMC spec §12, with Corporation keys. One writer of `eotg_corp_board_influence`. Every decision reads and moves it. CO5: the election file diff touches only the two vote-strength modifiers.

**In game (British Isles sub-mod, `-debug_mode`):**

| ID | Check | Pass |
|---|---|---|
| V-CO1 | error.log clean for the new files. | yes |
| V-CO2 | Hoël has the board modifier ("+5% income, +5 vassal opinion" at 50) and a visible "The Board" story reading 50. Konan reads 20. | yes |
| V-CO3 | Values clamp at 0 and 100 (debug path). | yes |
| V-CO4 | `kill` Hoël: the elected heir has max(own, 25) influence, a new story and the modifier. | yes |
| V-CO5 | Debug "Become feudal": story and modifier gone, variable dormant; back to Corporation: old value returns. | yes |
| V-CO6 | Solvent and at peace: +3 a year. In debt: −5 a year. | yes (CO2) |
| V-CO7 | Restructure: −25 influence, +10% income and −10% build cost for 5 years, Konan −10 opinion; blocked below 25; 5-year cooldown. | yes (CO3) |
| V-CO8 | Konan courts the board: +15 own, Hoël −5, medium gold paid. | yes (CO3) |
| V-CO9 | Hoël does not see Court the Board; Konan does not see Restructure. | yes (CO3) |
| V-CO10 | An independent feudal ruler with stewardship ≥ 12 and medium gold incorporates: Corporation, law, story, modifier, influence 50. Record the capital-holding result (OQ10). | yes / recorded (CO4) |
| V-CO11 | Dissolve the Board: legitimacy + 2 × influence (max 200); influence 0; Corporation vassals feudal. | yes (CO4) |
| V-CO12 | Grants: only the faith's theocratic type is offered; a county grant defaults to Corporation. | yes (CO4) |
| V-CO13 | The election tooltip shows "Hold on the board" for electors at ≥ 40 and the second bonus at ≥ 75; a landless councillor shows neither. | yes (CO5) |
| V-CO14 | 50-year observer run: influence stays in 0–100 and moves both ways; directors court; no AI adoption. | yes / recorded |
| V-CO15 | Save and reload: influence, counter and modifier survive. | yes |

---

## 13. Deferred

| Item | Why | Trigger |
|---|---|---|
| The third obligation "board seat" (`governments_v2.md` §14.1 P2) | needs CO5 data on how influence moves | after V-CO14 |
| `eotg_boardroom_war` CB; Sabotage Rival scheme | §14.1 P3 | after CO6 |
| `eotg_market_faction_cycle` lift (reader of `eotg_government_is_corporate`) | §5.3; joint with the Trade Oligarchy | after both G2 passes |
| Vanilla influence probe (T11) | not needed by this design | OQ1 |
| Clinic price coupling | cybernetics follow-up | owner |

---

## 14. Owner questions (each with a recommended default)

- **OQ1, scripted variable rather than vanilla influence (recommended: scripted).** Skip the T11 probe.
- **OQ2, 50% inheritance to the primary heir (recommended: yes).** The board must be won again. Alternatives: 75% (as the PMC) or 0% (a fresh start at the start value).
- **OQ3, directors' gains erode the CEO (recommended: yes, −5 per Court).** Makes the board contested. Alternative: no erosion (directors and CEO grow independently).
- **OQ4, a visible story (recommended: yes).**
- **OQ5, start values 50 (CEO) / 20 (director) (recommended: yes).**
- **OQ6, first-pass numbers (recommended: approve).** Results +3 / debt −5 a year; Restructure −25 for +10% income and −10% build cost for 5 years and −10 director opinion; Court +15 / −5 for medium gold; exit ×2 legitimacy max 200; modifier +10% income and +10 vassal opinion at 100.
- **OQ7, AI adoption (recommended: not yet).** As the Cartel.
- **OQ8, the events in §11 (recommended: none yet).**
- **OQ9, CO5: keep the councillor +1 alongside the influence bands (recommended: no).** A seat is not a hold. Yes keeps landless councillors' weight.
- **OQ10, entry requires a Port capital (recommended: no, record V-CO10 first).** If a castle capital is penalized under the city shape, add `capital_county` holding checks (UNVERIFIED-VANILLA form) before shipping CO4.
