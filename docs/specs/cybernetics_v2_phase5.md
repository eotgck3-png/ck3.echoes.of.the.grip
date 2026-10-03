# Cybernetics v2 — Phase 5: large arcs (The Countdown, The Patron, The Iron Retinue)
> **Note 2026-10-03:** the initiation check is now a weighted `random_list` (phase2 §1.1 amendment). Add this phase's initiation offers as list entries with their chance as the weight, never as `else_if` branches.

Index: [cybernetics_v2.md](cybernetics_v2.md). Rules in index §1 apply.

**Depends on:**
- Phase 0;
- **3a**, because the Countdown hands off to the cascade and Neurofractured;
- **4c**, because Countdown stage 5 fires tier3.020 *The Intervention*;
- Phase 2, for the initiation branch slots and init.018 / init.020.

**Purpose & gate.** Gate 3. Not blocked. These are the system's three multi-year stories, and each makes an earlier choice consequential:
- **The Countdown** turns the hidden risk into felt dread, and never shows a number.
- **The Patron** makes the moment of entry cost something for years.
- **The Iron Retinue** spreads augmentation to the people around you, and feeds Phase 6.

**Signature resource.**
- Countdown: its stages are chosen **by** `eotg_fracture_risk`, and every stage moves it.
- Patron: demands move risk through the firmware they control, and the betrayal path can start the Countdown.
- Retinue: events change knights' tiers or move knights' risk.

All three stories live in `common/story_cycles/eotg_augmentation_stories.txt` (created in Phase 3a), with `visible = no`. Shape copied from `game/common/story_cycles/story_cycle_murders_at_court.txt`. **The story's `effect_group` timing is its cooldown authority.** The events it fires check no flags.

---

## 1. The Countdown — `eotg_story_aug_countdown` (O-13; proposal §9.2)

### 1.1 Start, stop, and interaction with the yearly roll
- **Start** (in `eotg_on_yearly_aug_overclocked_check`, after accrual and before the threshold check): if `eotg_is_aug_tier3 = yes`, `eotg_aug_has_countdown = no`, and `var:eotg_fracture_risk >= 50` (or `>= 40` with `eotg_flag_aug_hidden_flaw`; Thread T6), run `create_story = eotg_story_aug_countdown`.
- **Also started by** patron.006 c/e (§2) under the same tier-3 condition.
- **While running:** the OC `random_list` "nothing" weight doubles: `modifier = { factor = 2  eotg_aug_has_countdown = yes }` on the nothing branch.
- **Ends:**
  - `eotg_trigger_neurofracture` gains `random_owned_story = { type = eotg_story_aug_countdown  end_story = yes }`. The cascade itself (fracture.0001) is the ending.
  - `eotg_aug_remove_all_effect` gains the same line (Phase 0 left the slot).
  - The Downgrade decision: if the halved risk is < 50, fire countdown.006 *The Quiet*, which ends the story.
- **`on_owner_death`:** `end_story = yes`.

### 1.2 Pacing
- `on_setup`: `set_variable = { name = last_stage  value = 0 }`.
- `effect_group`: `months = { 3 5 }`, `first_valid`:
  1. Owner is not tier 3 any more (regressed or removed) → countdown.006, `end_story`.
  2. Owner's risk < 35 → countdown.006, `end_story` (maintenance got ahead of it).
  3. Risk 50–59 and `last_stage < 1` → **.001**, `last_stage = 1`.
  4. Risk 60–69 and `last_stage < 2` → **.002**, `last_stage = 2`.
  5. Risk 70–74 and `last_stage < 3` → **.003**, `last_stage = 3`.
  6. Risk ≥ 75 and `last_stage < 4` → **.004**, `last_stage = 4`.
  7. `last_stage = 4`:
     - if the owner has `eotg_flag_aug_intervention_refused` → **.005**, `last_stage = 5`;
     - else, if a spouse or adult heir exists → fire **tier3.020** *The Intervention*, `last_stage = 5`.
  8. Otherwise nothing: the dread is in the silence.

Stages can skip: a ruler jumping from 55 to 72 gets .003 next. Each fires at most once.

### 1.3 Events (`events/eotg_augmentation_countdown.txt`, namespace `eotg_aug_countdown`)
Desc register escalates; **[voice]** variants as in Phase 3.

**.001 Minor Anomalies.** Clocks run wrong; cups are dropped.
- **a** "Maintenance. Now." `medium_gold_value`. Risk −8.
- **b** "Keep going." Risk +3.
- **c** "Tell no one." Helper lie. Risk +5.
- **d [diligent]** "Log every anomaly." Risk −5.
- **e [ambitious]** "Not now. Not when I am this close." +50 prestige. Risk +5.

**.002 Lost Time.** Days, not hours.
- **a** "Reconstruct the days." Lesson intrigue. Risk −3.
- **b** "Let them go." Risk +5.
- **c** "An archivist logs my every hour." −50 prestige. Risk −5.
- **d [paranoid]** "Someone took them from me." Helper tyranny on `picker(eotg_suspect, 0.05)`, house arrest. Risk +8.
- **e [calm]** "Breathe." Risk −6.

**.003 Contradictory Memories.** Two versions of one evening. **[voice]**: at voice ≥ 2, "one of them is its reconstruction".
- **a** "Trust the first." Risk +3.
- **b** "Trust the second." Risk +3.
- **c** "Trust neither." Stress medium gain. Risk −5.
- **d [honest]** "Ask the court which is true." −50 prestige. Risk −6.
- **e [stubborn]** "Both are true." Risk +8.

**.004 Violence.** `immediate`: picker(`eotg_victim`, 0.05), wounded (`REASON = attacked`), breach flag. No-one-near variant: "the wall, the door, your own hand".
- **a** "Pay their family." `medium_gold_value`. Helper wound. Risk −3.
- **b** "It was an accident." Helper lie + helper wound. Risk +5.
- **c** "Lock myself away." `eotg_mod_withdrawn_from_court` 1 year. Risk −8.
- **d [sadistic]** "It felt like clarity." +20 dread. Risk +10.
- **e [compassionate]** "Sit with them while they heal." The victim gets `eotg_opinion_aug_grateful_patient`; −25 prestige. Risk −5.

**.005 No One Asks Any More.** You refused them, and the court stopped asking.
- **a** "Good." Risk +5.
- **b** "Ask them to ask again." Remove the refused flag; fire tier3.020 in 30 days. Risk −3.
- **c [humble]** "Go to them yourself." As b. Risk −6.

**.006 The Quiet.** The countdown stops, for now.
- **a** "Breathe." Stress minor loss. Risk −5.
- **b [paranoid]** "It's waiting." Risk +3.

## 2. The Patron — `eotg_story_aug_patron` (I-05; T2; proposal §9.1)

### 2.1 Start
- Initiation branch **9** (Phase 2 slot): unaugmented, `OR = { ambitious greedy }`, `gold < medium_gold_value`, `is_landed = yes`. Chance 15. Sets `eotg_flag_aug_event_cooldown` 2 years. Fires **patron.001**.
- **init.018 e** (Phase 2 slot) "A patron will pay." Fires patron.001 in 1 day.

### 2.2 The envoy
**Naming (lore review):** the Patron is never named. In loc it is always "the syndicate" and its courtier is "the syndicate envoy". Never use Helix or the Pale Hand, or the words Consortium, Compact, Continuity, Rooks, "Corp"/"Co." after a name, or pale-hand/white-glove imagery. The Errand (.004) may stay ambiguous: "reported but unconfirmed".

The syndicate is off-map. Its face at court is an envoy created on acceptance:
```
create_character = { template = eotg_aug_patron_envoy_template  location = root.capital_province
                     culture = root.culture  faith = root.faith  save_scope_as = eotg_patron_envoy }
add_courtier = scope:eotg_patron_envoy
```
`eotg_aug_patron_envoy_template` goes in **`common/scripted_character_templates/eotg_augmentation_templates.txt`** (vanilla folder; shape `01_ep1_character_templates.txt` `prince_ali_template`):
- `age = { 35 55 }`;
- `random_traits_list` count 1 of `greedy` / `ambitious` / `deceitful`;
- `random_traits_list` count 1 of `education_stewardship_3` / `education_intrigue_3`;
- `random_traits = yes`;
- stewardship 10–14, intrigue 10–14.

Culture and faith come from root **by scope** (map-agnostic). The envoy is passed into the story with the passthrough-variable pattern (skill `story_cycles.md`, "Passing Variables to a Story").

### 2.3 Story
- **`on_setup`:** `envoy` (from passthrough), `demand = 0`, `grievance = 0`, `terms` (`flag:standard` / `flag:read` / `flag:greedy` from patron.001's option).
- **`on_owner_death`:** `end_story = yes`. Inherited debt is deferred (§5).
- **`effect_group`:** `years = { 2 3 }` (`{ 3 4 }` if terms = read), `first_valid`:
  1. `var:envoy` is dead or not the owner's courtier → **.007** *A New Envoy* (it creates the replacement and resets `envoy`).
  2. `grievance >= 3` → **.006** *The Final Demand* (betrayal framing).
  3. `demand = 0` → **.002**; `demand = 1` → **.003**; `demand = 2` → **.004**; `demand = 3` → **.005**; `demand >= 4` → **.006**.

  Each demand event increments `demand` in every option.

### 2.4 Events (`events/eotg_augmentation_patron.txt`, namespace `eotg_aug_patron`)
The envoy is saved as `scope:eotg_patron_envoy` from the story variable in each `immediate`.

**.001 The Patron's Offer.** "We would like to pay for it."
- **a** "Accept." Install (risk 0). Create the envoy. Start the story with terms = standard.
- **b** "Decline." —
- **c** "Accept, after reading every clause." As a, terms = read (longer intervals, milder demand values). Stress minor gain.
- **d [greedy]** "Accept, and ask for a stipend." As a, + `add_gold = minor_gold_value`, terms = greedy (demand values ×1.5).
- **e [paranoid]** "Who are you, really?" Decline. Lesson intrigue.

**.002 Repayment.** "A small matter of the invoice."
- **a** "Pay." `medium_gold_value` (×1.5 greedy, ×0.75 read).
- **b** "Refuse." `grievance +1`. The envoy gets disgust. Risk +5 ("the firmware hesitates").
- **c** "Renegotiate." `duel = { skill = diplomacy  target = scope:eotg_patron_envoy }`. Win: pay `minor_gold_value`. Lose: pay `major_gold_value`.
- **d [deceitful]** "Pay in promises." The envoy gets `add_hook = { type = indebted_hook  target = root }`. No gold.
- **e [honest]** "Ask for honest terms." 50%: halve the payment. 50%: `grievance +1`.

**.003 Exclusivity.** "Only our technicians may touch you now."
- **a** "Agree." `eotg_mod_aug_patron_clause` (until the story ends). Risk −5: their technicians are good.
- **b** "Refuse." `grievance +1`.
- **c** "Agree, on a trial basis." The clause for 3 years (`years = 3`).
- **d [diligent]** "Agree, but I audit their work." As a. Risk −8.
- **e [paranoid]** "Their hands will never touch me." `grievance +1`. Risk +5.

**.004 The Errand.** "There is a critic at your court." Saved `eotg_critic`: a zealous courtier, else a random courtier (`eotg_aug_victim_candidate`, not close family).
- **a** "It will be done." `scope:eotg_critic = { death = { death_reason = death_murder  killer = root } }`. Helper murder. Risk +5.
- **b** "No." `grievance +1`.
- **c** "Warn the critic instead." The critic gets reassured. `grievance +2`.
- **d [sadistic]** "With pleasure." As a; stress: sadistic medium loss.
- **e [just]** "Never, and they will hear of your asking." `grievance +2`, +50 prestige.

**.005 The Family Clause.** "Your heir's implants will be ours." Saved `eotg_heir`: primary heir aged ≥ 12, unaugmented. Without one: "your next child" → only `grievance +1` options.
- **a** "Agreed." The heir runs `eotg_aug_initiate_effect`, risk 10, gets unease toward root. ("They weren't buying the implant. They were buying your dynasty.")
- **b** "Never." `grievance +2`.
- **c** "Take more of me instead." Root risk +15.
- **d [compassionate]** "Not my child." As b; stress: compassionate medium loss.
- **e [ambitious]** "A strong heir is a strong house." As a; the heir gets admiration instead.

**.006 The Final Demand.** The desc depends on whether it was reached through `grievance` (betrayal tone) or `demand >= 4` (settlement tone).
- **a** "Sign over the revenues." `eotg_mod_aug_patron_clause` becomes permanent (`monthly_income_mult -0.15`; use the `_final` variant key, see §4). `end_story`.
- **b** "Buy them out." `{ value = major_gold_value multiply = 2 }`. `end_story`.
- **c** "Betray them." The envoy dies (`death_murder`, killer root); helper murder. `eotg_mod_aug_patron_throttle` 5 years. Risk +25. **If** tier 3 and no Countdown, start it. `end_story`.
- **d [deceitful]** "Sell them to a rival syndicate." 50%: clean exit, `add_gold = medium_gold_value`. 50%: as c. `end_story`.
- **e [brave]** "Come and take it from me." As c, +200 prestige.

**.007 A New Envoy.** It creates the replacement (same template).
- **a** "Welcome them." —
- **b [paranoid]** "And how did the last one die?" Lesson intrigue.
- **c** "Refuse them entry." `grievance +1`. Risk +5.

## 3. The Iron Retinue — `eotg_story_aug_retinue` (A-10; T4) and I-09 The Arms Race

### 3.1 Start
- **init.020** (Phase 2 slot): when a retainer is augmented through it and `NOT = { any_owned_story = { type = eotg_story_aug_retinue } }` and the root already has another augmented knight, start the story at `phase = 2`.
- **init.019 The Arms Race** b/d (below), starting at `phase = 2`.

### 3.2 Story
- **`on_setup`:** `phase` (from passthrough, default 1).
- **`on_owner_death`:** `end_story = yes`. Retinue knights keep their flag and implants, and Phase 6 keeps them alive in the world.
- **`effect_group`:** `years = { 1 2 }`, `chance = 70`. The phase selects **.001–.005**. .005 ends the story.

Every knight augmented through the story gets `eotg_flag_aug_iron_retinue` and `eotg_add_fracture_risk = { AMOUNT = 0 }`, so the variable exists.

### 3.3 Events (`events/eotg_augmentation_retinue.txt`, namespace `eotg_aug_retinue`)

**.001 First of the Iron.** Saved `eotg_volunteer`: an unaugmented knight.
- **a** "Augment them." `minor_gold_value`; the volunteer runs `eotg_aug_initiate_effect`. `phase = 2`.
- **b** "Not yet." — (the phase stays).
- **c** "The best hardware there is." `medium_gold_value`; install + `eotg_mod_implant_calibrated` 3 years. `phase = 2`.
- **d [ambitious]** "Them, and the next." Two knights (second via `ordered_knight`). `phase = 3`.
- **e [compassionate]** "Only if they truly want it." As a; the volunteer gets reassured.

**.002 More Ask.** Saved `eotg_cand_a`, `eotg_cand_b`.
- **a** "Both." 2× `minor_gold_value`.
- **b** "The stronger one." One install; the other gets `eotg_opinion_aug_passed_over`.
- **c** "Neither." Both get passed over.
- **d [greedy]** "They pay for it themselves." Both install at no cost; both get unease.
- **e [generous]** "At my expense, and with care." Both install + calibrated; `medium_gold_value`.

All set `phase = 3`.

**.003 The Iron Ranks** (renamed per lore review; the old name collided with a real-world movement). Apply `eotg_mod_aug_iron_retinue` to the owner (until reversal).
- **a** "Parade them." +100 prestige. Each retinue knight risk +3.
- **b** "Keep them quiet." —
- **c** "Train them harder." Lesson martial. Each retinue knight risk +8.
- **d [arrogant]** "Parade them past the vassals' gates." +150 prestige, +10 dread. Knights risk +3.
- **e [paranoid]** "And who watches the iron?" Each retinue knight gets fear toward root; risk −3 each.

`phase = 4`.

**.004 The Unaugmented Resent.** Every unaugmented knight gets `eotg_opinion_aug_passed_over`.
- **a** "Augment them too." `minor_gold_value` each (cap 3); install.
- **b** "Honour the unaugmented." `medium_gold_value`; replace passed_over with reassured.
- **c** "Let them resent." Retinue knights risk +3 each (isolation).
- **d [just]** "Equal pay. Equal honour." As b, at `minor_gold_value`.
- **e [callous]** "Replace them." `move_to_pool` the most resentful unaugmented knight.

`phase = 5`.

**.005 What the Programme Becomes.**
- **a** "Continue." `eotg_flag_aug_retinue_permanent` (Phase 6 progression ×2 for flagged knights).
- **b** "Stop recruiting." —
- **c** "Reverse it." Every retinue knight: 15% `death_treatment`; else `eotg_aug_remove_all_effect` + `eotg_mod_aug_removal_withdrawal`. Remove `eotg_mod_aug_iron_retinue`.
- **d** "Make it a privilege." Retinue knights get admiration; unaugmented knights get passed_over (`years = 10`).
- **e [zealous]** "Undo it. All of it." As c, +100 piety.

`end_story`.

**init.019 The Arms Race (I-09)** (`events/eotg_augmentation_initiation.txt`). Initiation branch **14** (Phase 2 slot): `any_knight = { count >= 2  eotg_is_augmented_any = yes }`, chance 20. Sets the cooldown 3 years.
- **a** "Then improve myself." `medium_gold_value`; install, risk 0.
- **b** "Start a programme." Create `eotg_story_aug_retinue` at `phase = 2`. Each augmented knight: risk +3 (the strain of being first).
- **c** "Look after the ones I have." `minor_gold_value` per knight (cap 3): calibrated, risk −5.
- **d [ambitious]** "All of it." a + b.
- **e [content]** "Two is enough." `eotg_flag_suppress_progression` 3 years.

## 4. Data objects
| Key | Type | Values |
|---|---|---|
| `eotg_mod_aug_patron_clause` | modifier | `icon = stewardship_negative`, `monthly_income_mult = -0.05` |
| `eotg_mod_aug_patron_clause_final` | modifier | `icon = stewardship_negative`, `monthly_income_mult = -0.15` |
| `eotg_mod_aug_patron_throttle` | modifier | `icon = health_negative`, `stress_gain_mult = 0.15`, prowess −2 |
| `eotg_mod_aug_iron_retinue` | modifier | `icon = martial_positive`, `knight_effectiveness_mult = 0.1` |
| `eotg_opinion_aug_passed_over` | opinion | −15, applied `years = 5` |
| `eotg_aug_patron_envoy_template` | character template | §2.2 |

All modifiers go into `eotg_clean_all_aug_modifiers` (patron and retinue modifiers are removed on the owner's full removal).

**Index correction:** `eotg_mod_aug_retinue_resentment` (listed in index §3.4) is **dropped**. Resentment is the `passed_over` opinion.

## 5. Deferred
- Inherited patron debt (the story passing to the heir).
- A visible story-cycle panel for the Patron / Retinue: it would need art, and the Countdown must stay invisible regardless.
- Retinue knights as a men-at-arms-like unit.

## 6. Loc (≈ 140 keys)
- countdown.001–.006, patron.001–.007, retinue.001–.005 and init.019, at ~6 keys each;
- countdown **[voice]** variants (3);
- patron .006 tone variants (2);
- .005 no-heir variant;
- 5 modifiers and 1 opinion × 2.

## 7. Definition of done
0. **Validation, all three clean** on the phase's files, except the known-benign items listed in `CLAUDE.md` §Validation: Tiger 1.17.0 (scratch descriptor), `docs/tools/px_lsp_diagnostics.js` (PX language server, headless) and `docs/tools/px_vocab_check.py` (engine vocabulary + dead hooks). Tiger is the only one of the three that checks scope.
1. The Countdown is created only from the OC on_action or patron.006. It never shows a number, and `visible = no`.
2. No story-fired event checks a cooldown flag.
3. `eotg_trigger_neurofracture` and `eotg_aug_remove_all_effect` end the Countdown.
4. The envoy is created from a template using root's culture and faith by scope. No culture or faith keys.
5. **Human, in game:**
   - Console-set an Overclocked count to risk 55: Minor Anomalies within ~5 months.
   - Accept a patron: Repayment arrives in 2–3 years.
   - Augment two knights through the decision: the retinue story starts.
