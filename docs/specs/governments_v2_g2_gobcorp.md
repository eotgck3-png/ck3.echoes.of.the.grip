# Spec: Governments v2, Phase G2: the Trade Oligarchy (`eotg_gobcorp_government`)

**Author:** cloud session (architect role), 2026-11-03. **Status:** draft, **unvalidated** (no game, Tiger or PX in the cloud). Next: eotg-lore-keeper (names, §8), then owner rulings (§14), then eotg-scripter in batches (§10). Batch TO1 is built on branch `claude/governments-g2-three-cloud` (§10).
**Parent specs:** `docs/specs/governments_v2.md` (§2, §5.3, §14, OQ3 display name), `docs/specs/government_template.md` (§2, §3.8, §3.11, §3.14, §3.15, §9). **Assessment:** `docs/qa/government_assessment_2026-10-11/gobcorp.md`. **Pattern:** `docs/specs/governments_v2_g2_cartel.md` (shipped). **Succession:** `docs/specs/governments_v2_g2_succession.md` §5.2 (the wealth-weighted election, built) and §2 (its market-share hook).
**Vanilla:** CK3 1.20.1.1. **This session could not read vanilla.** Vanilla citations are copied from shipped, locally validated mod files and specs ("via <file>"), or marked `UNVERIFIED-VANILLA`.
**Naming:** the internal key is `gobcorp` (`eotg_gobcorp_*`). **Player text says "Trade Oligarchy", "Trade Prince", "First Prince", "the charter". It never says "Gob-Corp"** (owner OQ3, 2026-10-08).

---

## 0. Kind of build (template §2 rule)

**A distinct government, not a reskin.** Its core verb differs from feudal's "conquer, then inherit":

> A Trade Prince **competes inside the charter for market share**: every point won is taken from a partner, and market share is both income and votes.

No vanilla government has this verb. The nearest is the republic's wealth-based election, which is not playable. G1 built none of it (assessment GAP G2).

---

## 1. Purpose & gate

G2 makes "power is bought and counted" (the government desc) a number:
- **Market share is a Prince's slice of the realm's trade**, 0 to 100, held by every Trade Oligarchy ruler at every tier.
- **The First Prince can corner the market** (top-tier decision): a big gain paid in gold, taken from every partner Prince.
- **A Prince can undercut a rival Prince** (vassal-tier decision): a gain taken from one named partner.
- **Peace grows trade; war shrinks it** (yearly).
- **The election reads it** (batch TO5). The wealth-weighted election built in the succession pass reads gold as a stand-in (`eotg_gobcorp_su_vote_wealth_1/2/3`). TO5 replaces the gold bands with market-share bands, as `governments_v2.md` §2 intended: "vote weight is derived from it, so one number drives both the market and the vote".

It also adds the entry and exit decisions, the grant fields and the display.

**Gate: 2, under the mod-exclusive exemption.** Not blocked by Gate 1. Map-agnostic. The British Isles test sub-mod supplies the Trade Oligarchy: Count Bertrand, d_provence, independent duke (`isles_assignments.csv:77`). **There is no Trade Oligarchy vassal in the test data**, so the vassal-tier checks need a console-made vassal (V-TO9).

**Soft dependencies:** CB-49 (V-G3, V-G17, city shape) and the succession pass's V-SU checks (for TO5).

---

## 2. Signature resource: `eotg_gobcorp_market_share` (scripted)

### 2.1 Decision: a dedicated variable

`governments_v2.md` §2 fixes `eotg_gobcorp_market_share`, a character variable from 0 to 100. Reasons:
1. **No engine currency means a share of trade.** Gold is the obvious stand-in (the election uses it now), but gold is spent on everything, so it can't also be a position in a market.
2. **It must be per Prince and contestable**, so partners can take it from each other. A per-character variable does that directly.
3. **The template default** (scaled modifier plus story counter, no `gui/`).

**"Share" is an index, not a true fraction:** the shares of all Princes need not sum to 100. Zero-sum moves are modelled by the decisions (§4), not by a global total. A true sum-to-100 market would need a global list over every Prince on each change. Rejected for cost and complexity (OQ3).

### 2.2 Identifiers and authority

| Item | Key | Notes |
|---|---|---|
| The resource (character variable) | `eotg_gobcorp_market_share` | 0 to 100, on every landed Trade Oligarchy ruler |
| Change effect (**the only writer**) | `eotg_gobcorp_change_market_share_effect = { AMOUNT = <number or named value> }` | `governments_v2.md` §2's naming rule |
| Reader | `eotg_gobcorp_market_share_value` | `var:eotg_gobcorp_market_share`, 0 when unset. All reads go through it, except the inheritance value and the story sync (PMC spec §2.2). |
| Clamp | `eotg_gobcorp_market_share_next_value` | reader + `scope:eotg_gobcorp_market_share_amount`, clamped to `[0, 100]` |
| Start value | `eotg_gobcorp_market_share_start_value` | 40 for `eotg_gobcorp_role_top`, otherwise 20 (OQ5) |
| Inheritance | `eotg_gobcorp_market_share_inherit_value` | heir scope: `max(0, 0.75 × predecessor's − heir's own)` (§2.4) |
| Story display mirror | `eotg_gobcorp_market_share_shown` (story variable) | display only |

### 2.3 The change effect

```
eotg_gobcorp_change_market_share_effect = {
    save_scope_value_as = { name = eotg_gobcorp_market_share_amount  value = $AMOUNT$ }
    set_variable = { name = eotg_gobcorp_market_share  value = eotg_gobcorp_market_share_next_value }
    eotg_gobcorp_sync_story_effect = yes
}
```
Rules as the PMC spec §2.3 and the Cartel amendment.

### 2.4 Inheritance: the house keeps its book

`eotg_gobcorp_on_death`: if root is a Trade Oligarchy ruler with market share and `exists = primary_heir`, save root as `scope:eotg_gobcorp_predecessor`; `primary_heir` gets `eotg_gobcorp_change_market_share_effect = { AMOUNT = eotg_gobcorp_market_share_inherit_value }`. The heir ends with the higher of its own share and 75% of the predecessor's. Under the wealth-weighted election, `primary_heir` is the vote leader (succession spec), so the share follows the elected successor. Init keeps an inherited value.

### 2.5 Sources and sinks (template §3.11 "full")

| Direction | What | Who | Amount | Batch |
|---|---|---|---|---|
| Source (passive) | yearly at peace (`is_at_war = no`) | any tier | +1/year | TO2 |
| Sink (penalty) | yearly at war (`is_at_war = yes`): war is bad for trade | any tier | −4/year | TO2 |
| Source (choice) | Corner the Market (top decision, §4.1) | top | +15, for gold | TO3 |
| Sink (contest) | the same decision, on **every** Trade Oligarchy vassal of the First Prince | vassals | −5 each | TO3 |
| Source (choice) | Undercut a Rival Prince (vassal decision, §4.2) | vassal | +10, for gold | TO3 |
| Sink (contest) | the same decision, on **one** rival Prince under the same liege | vassal | −10 | TO3 |
| Conversion | Dissolve the Charter (exit, §6.2) | top | all share → gold (×5, max 500) | TO4 |
| Read | the wealth-weighted election's vote strength (§5) | electors | bands at 30 / 60 / 90 | TO5 |

All numbers are first-pass (OQ6).

### 2.6 Init and teardown

As the PMC spec §2.6, with Trade Oligarchy keys: `eotg_gobcorp_init_effect` (story, start value if unset, `eotg_gobcorp_market_share_modifier`, sync) from `eotg_gobcorp_on_game_start` (and after the lobby), `_on_government_change`, `_on_title_gain`; `eotg_gobcorp_teardown_effect` (end story, remove modifier; **variable kept dormant**) from `_on_government_change` (`scope:old_government = { government_type_has_flag = eotg_government_is_gobcorp }`) and the monthly self-heal.

### 2.7 Display: layers 1 + 4, no `gui/`

**Layer 1.** `common/modifiers/eotg_gobcorp_modifiers.txt`:
```
eotg_gobcorp_market_share_modifier = {
    icon = stewardship_positive
    monthly_income_mult = 0.0015    # +15% income at 100 (on top of the government's +10%)
    scale = {
        value = eotg_gobcorp_market_share_value
        desc = eotg_gobcorp_market_share_scale_desc
        display_mode = scaled
    }
}
```
**UNVERIFIED-VANILLA:** fractional per-unit values under `display_mode = scaled` (PMC spec §2.7).

**Layer 4.** `common/story_cycles/eotg_gobcorp_story.txt`, key `eotg_story_gobcorp_market` ("The Charter Market"): `visible = yes`; icon `story_icon_palace_politics.dds`; background `gfx/interface/illustrations/event_scenes/corridor.dds` (already used by a shipped mod file); `basic_counter` on `eotg_gobcorp_market_share_shown`; `modifiers = { eotg_gobcorp_market_share_modifier }`; `custom_string_key = eotg_story_gobcorp_market_info`. Monthly tick: self-heal or sync (TO1); yearly tick (TO2). **OQ4** (visible story).

---

## 3. Identifier table

### 3.1 Script objects

| Type | Key | File | Batch |
|---|---|---|---|
| scripted trigger (role ladder) | `eotg_gobcorp_role_top`, `_role_county`, `_role_duchy`, `_role_kingdom`, `_role_vassal`; `eotg_gobcorp_is_landed_gobcorp` | `common/scripted_triggers/eotg_gobcorp_triggers.txt` | TO1 |
| scripted trigger | `eotg_gobcorp_is_rival_prince_of = { PRINCE = <character> }` (a Trade Oligarchy vassal of the same liege, not PRINCE) | same | TO3 |
| script value | `eotg_gobcorp_market_share_value`, `_next_value`, `_start_value`, `_inherit_value` | `common/script_values/eotg_gobcorp_values.txt` | TO1 |
| script value | `eotg_gobcorp_peace_gain_value` (1), `eotg_gobcorp_war_loss_value` (−4) | same | TO2 |
| script value | `eotg_gobcorp_corner_gain_value` (15), `eotg_gobcorp_corner_squeeze_value` (−5), `eotg_gobcorp_undercut_gain_value` (10), `eotg_gobcorp_undercut_loss_value` (−10) | same | TO3 |
| script value | `eotg_gobcorp_exit_gold_value` (share × 5, max 500), `eotg_gobcorp_exit_loss_value` (−share) | same | TO4 |
| scripted effect | `eotg_gobcorp_change_market_share_effect`, `eotg_gobcorp_sync_story_effect`, `eotg_gobcorp_init_effect`, `eotg_gobcorp_teardown_effect` | `common/scripted_effects/eotg_gobcorp_effects.txt` | TO1 |
| character modifier | `eotg_gobcorp_market_share_modifier` | `common/modifiers/eotg_gobcorp_modifiers.txt` | TO1 |
| opinion modifier (shared, no government prefix) | `eotg_market_cornered_opinion` (−10, decaying over 5 years); `eotg_undercut_opinion` (−15, decaying over 5 years) | `common/opinion_modifiers/eotg_gobcorp_opinions.txt` | TO3 |
| story cycle | `eotg_story_gobcorp_market` | `common/story_cycles/eotg_gobcorp_story.txt` | TO1 / TO2 |
| on_action (mod) | `eotg_gobcorp_on_game_start`, `_on_government_change`, `_on_title_gain`, `_on_death` | `common/on_action/eotg_gobcorp_on_actions.txt` | TO1 |
| decision (top) | `eotg_decision_gobcorp_corner_market` | `common/decisions/eotg_gobcorp_decisions.txt` | TO3 |
| decision (vassal) | `eotg_decision_gobcorp_undercut_rival` | same | TO3 |
| decision (entry) | `eotg_decision_gobcorp_adopt` | same | TO4 |
| decision (exit) | `eotg_decision_gobcorp_dissolve_charter` | same | TO4 |
| government (edit) | add `possible_grant_vassal_governments` (§7) | `common/governments/eotg_gobcorp_government.txt` | TO4 |
| election (edit) | `eotg_gobcorp_elective`: the three wealth modifiers read market share instead of gold (§5) | `common/succession_election/eotg_government_elections.txt` | TO5 |
| variables | `eotg_gobcorp_market_share` (character); `eotg_gobcorp_market_share_shown` (story); scope value `eotg_gobcorp_market_share_amount`; saved scopes `eotg_gobcorp_predecessor`, `eotg_gobcorp_rival` | — | TO1/TO3 |

### 3.2 The story cycle in full

| Block | Content |
|---|---|
| `on_setup` | `set_variable eotg_gobcorp_market_share_shown = 0` |
| `on_end` | `story_owner` removes `eotg_gobcorp_market_share_modifier` |
| `on_owner_death` | `end_story = yes` |
| `effect_group` `months = 1` (TO1) | `first_valid`: (a) owner not a landed Trade Oligarchy ruler → teardown; (b) otherwise → sync |
| `effect_group` `years = 1` (TO2) | `first_valid`: (a) owner landed, at war → `eotg_gobcorp_war_loss_value`; (b) owner landed, at peace → `eotg_gobcorp_peace_gain_value`. The only cadence authority. |

---

## 4. Decisions that move the resource

Shape: the Cartel's shipped decisions. Market share is not a `cost` key; gate in `is_valid`, move in `effect`.

### 4.1 Top tier: `eotg_decision_gobcorp_corner_market` ("Corner the Market")

| Field | Value |
|---|---|
| `is_shown` | `eotg_gobcorp_role_top = yes` |
| `is_valid` | `is_at_war = no`; custom tooltip `eotg_gobcorp_market_share_value < 100` |
| `cost` | `gold = major_gold_value` (verified in v2 script, amendment 2026-11-03) |
| `cooldown` | `{ years = 5 }` |
| `effect` | Own: `eotg_gobcorp_change_market_share_effect = { AMOUNT = eotg_gobcorp_corner_gain_value }` (+15). `every_vassal` with `government_has_flag = eotg_government_is_gobcorp`: `eotg_gobcorp_change_market_share_effect = { AMOUNT = eotg_gobcorp_corner_squeeze_value }` (−5) and `add_opinion = { modifier = eotg_market_cornered_opinion target = root }`. Custom tooltips. |
| `ai_check_interval_by_tier` | barony 0, county 60, duchy 36, kingdom 36, empire 36, hegemony 36 |
| `ai_potential` | `eotg_gobcorp_role_top = yes` |
| `ai_will_do` | base 10. +20 if `eotg_gobcorp_market_share_value < 40`. +10 if greedy. −10 if the realm has 3 or more Trade Oligarchy vassals (they resent it; UNVERIFIED-VANILLA count form: `any_vassal = { count >= 3 … }`). Factor 0 if `gold < major_gold_value`. |

**Why this decision:** the First Prince is first among equals, not above them (LQ2). Cornering the market is how they pull ahead, and it costs the partners. That keeps "no single head" alive as a risk: a First Prince who corners too often is hated by the people who elect the next one.

### 4.2 Vassal tier: `eotg_decision_gobcorp_undercut_rival` ("Undercut a Rival Prince")

| Field | Value |
|---|---|
| `is_shown` | `eotg_gobcorp_role_vassal = yes` |
| `is_valid` | custom tooltip: `liege = { any_vassal = { eotg_gobcorp_is_rival_prince_of = { PRINCE = root } } }` (a rival exists) |
| `cost` | `gold = minor_gold_value` |
| `cooldown` | `{ years = 5 }` |
| `effect` | `liege = { random_vassal = { limit = { eotg_gobcorp_is_rival_prince_of = { PRINCE = root } } weight = { base = 1  modifier = { add = eotg_gobcorp_market_share_value } } save_scope_as = eotg_gobcorp_rival } }` (the bigger the rival, the likelier the target). Rival: −10 and `add_opinion = { modifier = eotg_undercut_opinion target = root }`. Own: +10. Toast naming the rival. |
| `ai_check_interval_by_tier` | barony 0, county 60, duchy 48, kingdom 48, empire 0, hegemony 0 |
| `ai_potential` | `eotg_gobcorp_role_vassal = yes` |
| `ai_will_do` | base 10. +15 if greedy, +10 if ambitious. −20 if compassionate. Factor 0 if `gold < minor_gold_value`. |

**Why this decision:** "rivalry inside the charter" (the government desc), as a number. The rival is a weighted random pick, so no picker widget is needed (the Cartel's county picker carries known Tiger noise). **UNVERIFIED-VANILLA:** a `weight` block on `random_vassal` reading a script value of the candidate (the Cartel's walk-off uses the same shape on `random_tributary`, so it is likely).

---

## 5. The election reads market share (TO5)

The succession pass built `eotg_gobcorp_elective` with three wealth modifiers on gold (`>= 100 / 300 / 1000`) and named them **the market-share hook** (succession spec §2, §5.2). TO5 changes only their conditions, keeping their loc keys and adding no modifier:

| Modifier | Add | Condition (new) |
|---|---|---|
| `eotg_gobcorp_su_vote_wealth_1` | +1 | `eotg_gobcorp_market_share_value >= 30` |
| `eotg_gobcorp_su_vote_wealth_2` | +1 | `eotg_gobcorp_market_share_value >= 60` |
| `eotg_gobcorp_su_vote_wealth_3` | +1 | `eotg_gobcorp_market_share_value >= 90` |

- **Elector selection stays on gold** (`eotg_gobcorp_su_prince_priority_value`, "the eight richest"). OQ9 asks whether to sort electors by market share too.
- **Loc:** "Wealthy / Very wealthy / Vastly wealthy" becomes "Market share 30+ / 60+ / 90+" (localizer, TO6).
- Separate batch with its own V-SU re-run, after TO1 is validated.

---

## 6. Entry and exit

Shapes: the Cartel's shipped transitions. `decision_group_type = major`.

### 6.1 Entry: `eotg_decision_gobcorp_adopt` ("Sign the Charter")

| Field | Value |
|---|---|
| `is_shown` | `is_landed = yes`; `highest_held_title_tier > tier_barony`; `is_independent_ruler = yes`; `OR = { government_has_flag = government_is_feudal  government_has_flag = government_is_clan }`; `NOR` the four mod identity flags and `eotg_government_is_unclaimed` |
| `is_valid` | custom tooltip `gold >= medium_gold_value`; custom tooltip `stewardship >= 10` |
| `is_valid_showing_failures_only` | no `changed_government_recently`; `is_at_war = no`; `is_tributary = no` |
| `cost` | `prestige = 200` |
| `effect` | `changed_government_recently` (5 years); `change_government = eotg_gobcorp_government`. Init sets share 40. **Only the ruler converts.** Capital-holding question as the Corporation (OQ10 there). |
| `ai_potential` | **`always = no`** (OQ7) |
| `ai_will_do` (for later) | base 0. +10 if greedy. +10 if `stewardship >= 14`. Factor 0 if `primary_title.tier > tier_kingdom`. |

### 6.2 Exit: `eotg_decision_gobcorp_dissolve_charter` ("Dissolve the Charter")

| Field | Value |
|---|---|
| `is_shown` | `eotg_gobcorp_role_top = yes` |
| `is_valid_showing_failures_only` | no `changed_government_recently`; `is_at_war = no` |
| `cost` | `prestige = medium_prestige_value` |
| `effect`, in order | (1) `add_gold = eotg_gobcorp_exit_gold_value` (share × 5, max 500: the book is sold). (2) change by `eotg_gobcorp_exit_loss_value` (to 0). (3) `every_vassal_or_below` with the flag → `change_government = feudal_government`. (4) `changed_government_recently`. (5) `change_government = feudal_government`. |
| `ai_potential` | `eotg_gobcorp_role_top = yes`; `eotg_gobcorp_market_share_value < 10` |
| `ai_will_do` | base 0. +10 if at war for long (UNVERIFIED-VANILLA war-length trigger; fallback `is_at_war = yes`). |

### 6.3 Forced and incidental transitions

As the PMC spec §6.3.

---

## 7. AI and grant fields

| Field | Trade Oligarchy G2 | Why |
|---|---|---|
| `possible_grant_vassal_governments` | `{ theocracy_government ecclesiastical_government }` | As the Cartel. Does not list feudal. |
| `grant_vassal_ai_will_do` | not set | dead code |
| `ai = { }` | unchanged (`use_legends`, `arrange_marriage`) | — |

**How the AI lives on market share:** grows at peace; the First Prince corners when behind and rich; Princes undercut when greedy and solvent; cooldowns of 5 years; entry off; exit only when broken.

---

## 8. Lore constraints

- **Trade Princes bound by a shared charter, competing for market share, with no single head** (`governments_v2.md` §5.3; `Third era Nations.md:2019-2024`, via that spec). The top rank is **First Prince**, first among equals (LQ2).
- **No outside body** (ERRATA "LAW AT 866"): the charter binds the Princes to each other only. No exchange, registry, court, League or arbiter certifies a market. Text never says "the market authority" or similar.
- **Species-neutral** (owner OQ3): the desc and every new string describe the form, never goblins or ogres. **No "Gob-Corp" anywhere in player text.** Never name the Gob-Ogre Trade League.
- **The vassal-group word "trade bloc" collides with the "Bloc" kingdom rank** (assessment P5). New text avoids "bloc".
- Bastion and Port; Canadian English; the knight term is dynamic ("Strongarm").
- **For the lore-keeper:** do "Market Share", "The Charter Market", "Corner the Market", "Undercut a Rival Prince", "Sign the Charter" and "Dissolve the Charter" fit 866 voice?

---

## 9. Loc surface (`localization/english/eotg_gobcorp_l_english.yml`, one BOM)

| Object | Keys | Batch |
|---|---|---|
| modifier | `eotg_gobcorp_market_share_modifier`, `_desc`; `eotg_gobcorp_market_share_scale_desc` | TO1 |
| story | `eotg_story_gobcorp_market`, `_info`, `_label`, `_min_label`, `_max_label`, `_tt` | TO1 |
| decisions (×4) | `<key>`, `_desc`, `_tooltip`, `_confirm`; `eotg_decision_gobcorp_corner_market_share_tt`, `_squeeze_tt`; `eotg_decision_gobcorp_undercut_rival_rival_tt`, `_gain_tt`, `_toast`, `_toast_desc`; `eotg_decision_gobcorp_adopt_gold_tt`, `_stewardship_tt`; `eotg_decision_gobcorp_dissolve_charter_effect_tt` | TO3/TO4 |
| opinion | `eotg_market_cornered_opinion`, `eotg_undercut_opinion` | TO3 |
| election (text update) | `eotg_gobcorp_su_vote_wealth_1/2/3` | TO5 |

---

## 10. Build batches


> **Amendment, 2026-11-03 (cloud build of TO2–TO5, unvalidated).**
> 1. **Built:** TO2 (story yearly trade-and-war tick), TO3 (Corner, Undercut, `eotg_gobcorp_is_rival_prince_of`, `eotg_gobcorp_rival_weight_value`, shared `eotg_market_cornered_opinion` and `eotg_undercut_opinion`), TO4 (entry, exit, grant field), TO5 (vote strength reads market share), and all their loc (the TO6 loc part), including the election tooltips and the law description ("Market share adds voting power"). TO6's lore-keeper and QA review remain.
> 2. **`major_gold_value` is verified**: v2 script reads it 72 times. The §4.1 UNVERIFIED note is withdrawn. The `any_vassal = { count >= 3 }` form is verified too (`eotg_augmentation_laws.txt:90-93`).
> 3. **`eotg_gobcorp_is_rival_prince_of`** checks role and `this != PRINCE` only. Callers iterate PRINCE's liege's vassals, which is what makes the rival a charter partner.
> 4. **Deviation:** the exit's AI "+10 at war for long" became "+10 in debt" (the decision needs peace, and no war-length trigger is used in v2).

| Batch | Contents | Static gate | In-game tests |
|---|---|---|---|
| **TO1, resource core** (**built**, unvalidated) | role ladder; TO1 values; change, sync, init, teardown; modifier; story (monthly tick); on_actions incl. death inheritance; TO1 loc | Tiger, PX, vocab; one writer of `eotg_gobcorp_market_share` | V-TO1–V-TO5 |
| **TO2, trade and war** (**built (cloud, unvalidated), 2026-11-03**) | story yearly tick; TO2 values | one cadence authority | V-TO6 |
| **TO3, decisions** (**built (cloud, unvalidated), 2026-11-03**) | Corner, Undercut, rival trigger, two shared opinions | `ai_will_do`; moves only through the change effect | V-TO7–V-TO9 |
| **TO4, transitions and grants** (**built (cloud, unvalidated), 2026-11-03**) | entry, exit, grant field | entry `ai_potential = always = no` | V-TO10–V-TO12 |
| **TO5, the election reads market share** (**built (cloud, unvalidated), 2026-11-03**) | three condition edits (§5) | V-SU re-run | V-TO13 |
| **TO6, loc and review** (loc **built (cloud, unvalidated), 2026-11-03**; review pending) | §9 loc for TO2–TO5; lore; QA | template §5.1 | V-TO14, V-TO15 |

---

## 11. Proposed events: OWNER APPROVAL REQUIRED (not in the build list)

| # | Proposal | Fires from | Coupling |
|---|---|---|---|
| E1 | **A Partner Calls In a Debt.** A Prince with a higher share than yours demands repayment. Options: pay (gold); refuse (−10 share, opinion −20). | story yearly tick, vassal | moves and reads |
| E2 | **Buy a Vote.** Before an election, spend gold to raise one elector's opinion of your candidate, or market share to sway them (succession spec §12 suggestion). | story yearly tick, when the ruler is old or ill | moves |
| E3 | **Price War.** Two Princes undercut each other twice in 10 years. Options for the First Prince: arbitrate (both −5, +opinion); take a side (one +10, one −10). | Undercut effect (a counter on the vassal) | moves and reads |
| E4 | **A Ruinous War.** At war for 3 years: options to buy peace with share. | TO2 war branch | moves and reads |
| E5 | **The v1 lift.** v1 Trade Oligarchy events (27), audited to move or read share or dropped. | `yearly_playable_pulse` via a mod on_action | audit per event |

---

## 12. Definition of done

**Static:** as the PMC spec §12, with Trade Oligarchy keys. One writer of `eotg_gobcorp_market_share`. No "Gob-Corp" in any loc string (`grep -i "gob-corp" localization` is empty apart from comments).

**In game (British Isles sub-mod, `-debug_mode`):**

| ID | Check | Pass |
|---|---|---|
| V-TO1 | error.log clean for the new files. | yes |
| V-TO2 | Bertrand has the modifier ("+6% income" at 40) and a visible "The Charter Market" story reading 40. | yes |
| V-TO3 | Values clamp at 0 and 100 (debug path). | yes |
| V-TO4 | `kill` Bertrand: the elected heir has max(own, 30) share, a new story and the modifier. | yes |
| V-TO5 | Debug "Become feudal": story and modifier gone, variable dormant; back: old value returns. | yes |
| V-TO6 | At peace +1 a year; at war −4 a year. | yes (TO2) |
| V-TO7 | Corner the Market: +15 own, every Trade Oligarchy vassal −5 and −10 opinion, major gold paid, 5-year cooldown. | yes (TO3) |
| V-TO8 | A vassal undercuts: +10 own, one rival −10 with −15 opinion, toast names the rival. With no rival, the decision is invalid with a tooltip. | yes (TO3) |
| V-TO9 | Make two Trade Oligarchy vassals by console (grant counties) to run V-TO8. | setup |
| V-TO10 | An independent feudal ruler with medium gold and stewardship ≥ 10 signs the charter: Trade Oligarchy, law, story, share 40. | yes (TO4) |
| V-TO11 | Dissolve the Charter: gold + 5 × share (max 500); share 0; vassals feudal. | yes (TO4) |
| V-TO12 | Grants: only the faith's theocratic type; a county grant defaults to Trade Oligarchy. | yes (TO4) |
| V-TO13 | Election tooltip shows the market-share bands; gold no longer adds vote strength. | yes (TO5) |
| V-TO14 | 50-year observer run: share in 0–100, moving both ways; no AI adoption. | yes / recorded |
| V-TO15 | Save and reload: share, counter and modifier survive. | yes |

---

## 13. Deferred

| Item | Why | Trigger |
|---|---|---|
| A true sum-to-100 market across all Princes | cost and complexity (§2.1) | OQ3 |
| Frontier trade-network coupling (`eotg_frontier_set_trade_network_effect`) | `governments_v2.md` §5.3 Coupling | Frontier follow-up |
| `eotg_market_faction_cycle` lift (reads `eotg_government_is_corporate`) | joint with the Corporation | after both G2 passes |
| Third obligation ("enforcement rights"); proxy-war CB; Sabotage Rival scheme | §14.1 P2/P3 | after V-TO14 |
| `diplomacy = -1` tuning (assessment P4) | design | owner, OQ11 |

---

## 14. Owner questions (each with a recommended default)

- **OQ1, a scripted 0–100 variable (recommended: yes).**
- **OQ2, 75% inheritance to the primary heir (recommended: yes).** The house keeps its book. Alternative: 50%, as the Corporation.
- **OQ3, share as an index, not a true fraction of a fixed market (recommended: index).** Zero-sum moves come from the decisions.
- **OQ4, a visible story (recommended: yes).**
- **OQ5, start values 40 (First Prince) / 20 (Prince) (recommended: yes).**
- **OQ6, first-pass numbers (recommended: approve).** Peace +1 / war −4 a year; Corner +15 own, −5 to each vassal, major gold, 5 years; Undercut +10 / −10, minor gold, 5 years; exit ×5 gold max 500; modifier +15% income at 100.
- **OQ7, AI adoption (recommended: not yet).** As the Cartel.
- **OQ8, the events in §11 (recommended: none yet).**
- **OQ9, TO5: sort electors by market share instead of gold (recommended: no, keep gold for selection).** Only vote strength moves to share in TO5.
- **OQ10, Corner the Market hits all vassal Princes, including counts (recommended: yes).** Alternative: only duke- and kingdom-tier Princes.
- **OQ11, change the government's `diplomacy = -1` to `+1` (recommended: yes, separately).** Assessment P4; outside this pass's batches.
