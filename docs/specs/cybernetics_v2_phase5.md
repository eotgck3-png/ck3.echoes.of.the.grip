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
  - `eotg_trigger_neurofracture` gains `random_owned_story = { limit = { story_type = eotg_story_aug_countdown }  end_story = yes }`. The cascade itself (fracture.0001) is the ending.
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

**.005 No One Asks Anymore.** You refused them, and the court stopped asking.
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
- **Amended 2026-10-04 by [cybernetics_v2_new_beats.md](cybernetics_v2_new_beats.md) §5.2 (human-approved):** a new tick entry, after the write-off and before the demand sequence, in both cadences. It fires **patron.008** *The Paper* once per story (story variable `eotg_paper_served`), when the owner has no implants, the envoy is present, demand < 4 and grievance < 3. That file is the authority.
- **`on_end`:** removes the open-ended `eotg_mod_aug_patron_clause`, and sends a living, free, landless envoy to the pool (round 2 M12; vanilla `hold_court_events_general.txt:508`).
- **`effect_group`:** `years = { 2 3 }` (`{ 3 4 }` if terms = read). Two `effect_group`s, one per cadence, with **identical** `first_valid` bodies. Script names: `eotg_envoy`, `eotg_demand`, `eotg_grievance`, `eotg_terms`.

  **Ratified 2026-10-04 (CB-26/CB-27 M7).** This is the order in `common/story_cycles/eotg_augmentation_stories.txt` (`eotg_story_aug_patron`). It replaces the order first specced here, which checked the envoy first.
  1. Owner `is_landed = no` → `end_story` (round 2; `story_cycle_take_mandate_of_heaven.txt:172-189`).
  2. Owner Neurofractured and `demand < 4` → set `demand = 4`, owner flag `eotg_flag_aug_patron_writeoff` (60 days), **.006** (balance §5.8 write-off).
  3. *(Specced, not yet built: the paper entry, patron.008, per [new_beats](cybernetics_v2_new_beats.md) §5.2.)*
  4. The `always` entry, an `if` / `else_if` chain:
     1. `grievance >= 3` **or** `demand >= 4` → **.006** *The Final Demand*.
     2. `var:envoy` missing, dead, or not the owner's courtier → **.007** *A New Envoy* (it creates the replacement and resets `envoy`).
     3. `demand = 0` → **.002**; `demand = 1` → **.003**.
     4. `demand = 2` → **.004** if any courtier passes `eotg_aug_patron_critic_candidate = { RULER = story_owner }`; otherwise set `demand = 3` and fire **.005**. The syndicate moves on to the Family Clause instead of stalling.
     5. Otherwise (`demand = 3`) → **.005**.

  **Why .006 comes before .007.** .007 c "Refuse them entry." adds grievance but no demand. With the envoy check first, an owner who refuses every new envoy has no envoy at court on the next tick, gets .007 again, and never reaches the Final Demand. With .006 first, the third refusal ends the loop. **The cost:** .006 can fire while the envoy is dead or has left court. §2.4 handles that case (the `_absent` descs, and the presence gate on the envoy's portrait and on the options that act on the envoy).

  **Why .004 is skipped.** With no valid critic, .004 would have nothing to name. If the last candidate goes in the 1–30 days before .004 fires, the event's own trigger fails, `demand` stays at 2, and the next tick tries again (or skips).

  Each demand event (.002–.005) increments `demand` in every option, in `after`. .006 ends the story in `after`. .007 does not count as a demand.

### 2.4 Events (`events/eotg_augmentation_patron.txt`, namespace `eotg_aug_patron`)
The envoy is saved as `scope:eotg_patron_envoy` from the story variable in each `immediate` (`var:eotg_envoy ?= { save_scope_as = … }`).

**Envoy presence (CB-27 M7, ratified 2026-10-04).** The tick fires 1–30 days before the event, and (§2.3) it can fire .006 with no envoy at court. So every place in .002–.006 that **shows, names or acts on** the envoy is gated on the scripted trigger `eotg_aug_patron_envoy_present`: `scope:eotg_patron_envoy ?= { is_alive = yes  is_courtier_of = root }`, evaluated in the event's root after `immediate`. Vanilla precedent: `events/story_cycles/peasant_affair/story_cycle_peasant_affair_events.txt:1173-1178` (an option acting on a story character requires them alive and at root's court). .007 creates its envoy in `immediate`, so it uses `exists`.

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
- **Presence gates (CB-27 follow-up):** the envoy's right portrait; c's duel and d's hook need `eotg_aug_patron_envoy_present`. On b, the envoy's disgust is applied only if present, and the grievance always is. a, b and e stay open with no envoy.

**.003 Exclusivity.** "Only our technicians may touch you now."
- **a** "Agree." `eotg_mod_aug_patron_clause` (until the story ends). Risk −5: their technicians are good.
- **b** "Refuse." `grievance +1`.
- **c** "Agree, on a trial basis." The clause for 3 years (`years = 3`).
- **d [diligent]** "Agree, but I audit their work." As a. Risk −8.
- **e [paranoid]** "Their hands will never touch me." `grievance +1`. Risk +5.
- **Presence gate (CB-27 follow-up):** the envoy's right portrait only. No option acts on the envoy.

**.004 The Errand.** "There is a critic at your court." Saved `eotg_critic`: a zealous courtier, else any courtier, both filtered by `eotg_aug_patron_critic_candidate` (adult, free, not root, not close family or spouse, not Neurofractured). The critic is a **chosen target**, not an episode victim, so index rule 7's picker does not apply (*CB-26 L4/S5*). The critic is named in loc.
- **Never the envoy (CB-27 M8, ratified 2026-10-04).** The envoy is a courtier, so without this the `else` branch could ask the owner to murder the syndicate's own envoy. `eotg_aug_patron_critic_candidate` itself excludes the owner's Patron story's `var:eotg_envoy`: it saves the candidate as a temporary scope and tests `NOT = { $RULER$ = { any_owned_story = { story_type = eotg_story_aug_patron  var:eotg_envoy ?= scope:eotg_critic_check } } }`. Vanilla shape: `events/court_events/01_ep3_court_events.txt:557-570`. It is in the trigger, not in a caller, so all three users get it with no new parameter: the tick's skip test, .004's `trigger`, and .004's pick.
- **The envoy as the only candidate.** If the envoy is the only courtier who would otherwise qualify, nobody passes, so the tick takes the §2.3 skip (`demand = 3`, **.005**). .004 never fires with the envoy as its only possible target.
- **Presence gate:** the envoy's lower-right portrait. The critic's right portrait is gated on `exists`.
- **a** "It will be done." `scope:eotg_critic = { death = { death_reason = death_murder  killer = root } }`. Helper murder. Risk +5.
- **b** "No." `grievance +1`.
- **c** "Warn the critic instead." The critic gets reassured. `grievance +2`.
- **d [sadistic]** "With pleasure." As a; stress: sadistic medium loss.
- **e [just]** "Never, and they will hear of your asking." `grievance +2`, +50 prestige.

**.005 The Family Clause.** "Your heir's implants will be ours." Saved `eotg_heir`: primary heir aged ≥ 12, unaugmented. Without one: "your next child" (`desc_no_heir`), and only the refusals **b** and **d** (grievance +2) remain; a, c and e need the heir (*CB-26 S15*).
- **a** "Agreed." The heir runs `eotg_aug_initiate_effect`, risk 10, gets unease toward root. ("They weren't buying the implant. They were buying your dynasty.")
- **b** "Never." `grievance +2`.
- **c** "Take more of me instead." Root risk +15.
- **d [compassionate]** "Not my child." As b; stress: compassionate medium loss.
- **e [ambitious]** "A strong heir is a strong house." As a; the heir gets admiration instead.
- **Presence gate (CB-27 follow-up):** the envoy's lower-right portrait. The heir's right portrait is gated on `exists`.

**.006 The Final Demand.** The desc depends on how it was reached, and on whether the envoy is present. `first_valid`, six keys (CB-27 M7, ratified 2026-10-04):

| Reached by | Envoy present | Envoy absent (`eotg_aug_patron_envoy_present = no`) |
|---|---|---|
| Write-off (`eotg_flag_aug_patron_writeoff`, balance §5.8) | `desc_writeoff` | `desc_writeoff_absent` |
| `grievance >= 3` (betrayal tone) | `desc_betrayal` | `desc_betrayal_absent` |
| `demand >= 4` (settlement tone) | `desc_settlement` | `desc_settlement_absent` |

The `_absent` variants deliver the terms by sealed message or courier, and never put the envoy in the room. The envoy's right portrait is gated on presence.

- **a** "Sign over the revenues." `eotg_mod_aug_patron_clause` becomes permanent (`monthly_income_mult -0.15`; use the `_final` variant key, see §4). Ungated: always available. `end_story`.
- **b** "Buy them out." `{ value = major_gold_value multiply = 2 }`, scaled by the terms like every bill. `end_story`.
- **c** "Betray them." `trigger = { eotg_aug_patron_envoy_present = yes }`: the envoy must be at court to be killed in person. `eotg_aug_patron_betray_effect` plus the murder stress helper. `end_story`.
- **d [deceitful]** "Sell them to a rival syndicate." 50%: clean exit, `add_gold = medium_gold_value`. 50%: `eotg_aug_patron_betray_effect`, with the murder stress helper only if the envoy is present. The lie stress helper applies on both branches. Not presence-gated: selling the syndicate out needs no envoy in the room. `end_story`.
- **e [brave]** "Come and take it from me." As c (same presence gate), +200 prestige.

**`eotg_aug_patron_betray_effect`** (ratified 2026-10-04; it supersedes the first spec of c, which applied every consequence unconditionally):
1. **If** `eotg_aug_patron_envoy_present`: the envoy dies (`death_murder`, killer root). The effect never murders someone who is not there. c and e are gated on the same test, so the guard matters only for d's failure branch.
2. **If** `eotg_is_augmented_any = yes`: `eotg_mod_aug_patron_throttle` for 5 years, risk +25, and `eotg_aug_try_start_countdown_effect` (which starts the Countdown only at tier 3 with none running). The throttle is a firmware restriction (CB-26 M6/W3), so it goes inside the augmented branch, with the risk. An owner who has left the system gets none of the three. This was the rulings §2 follow-up, now built.

**What betrayal costs, by case.** This records the built behavior. The open question in [new_beats](cybernetics_v2_new_beats.md) §10 is **resolved by [cybernetics_v2_reprisal.md](cybernetics_v2_reprisal.md)** (2026-10-04; .006 option f, and the collector, patron.009). Its §5.1 table supersedes this one once built.

| Owner | Envoy | Betrayal routes | Cost of betraying |
|---|---|---|---|
| augmented | present | c, e, d (50%) | murder, throttle, risk +25, maybe the Countdown |
| augmented | absent | d [deceitful] (50%) only | throttle, risk +25, maybe the Countdown; no murder |
| no implants | present | c, e, d (50%) | the envoy's murder (helper + vanilla consequences) only |
| no implants | absent | d [deceitful] only | **lie stress only**: d's failure does nothing else |

**.007 A New Envoy.** It creates the replacement (same template).
- **a** "Welcome them." —
- **b [paranoid]** "And how did the last one die?" Lesson intrigue.
- **c** "Refuse them entry." `grievance +1`. Risk +5.

## 3. The Iron Retinue — `eotg_story_aug_retinue` (A-10; T4) and I-09 The Arms Race

### 3.1 Start
- **init.020** (Phase 2 slot): when a retainer is augmented through it (a–d), `eotg_aug_has_retinue = no`, NOT `eotg_flag_aug_retinue_done` (round 2 H2), and the court has **at least one** augmented knight, run `eotg_aug_start_retinue_effect`. That effect sets `phase = 1` with exactly one augmented knight, so .001 *First of the Iron* fires, and `phase = 2` with two or more. *CB-26 M5:* as first specced (always `phase = 2`, from the second knight), nothing reached `phase = 1` and .001 was unreachable.
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

**.002 More Step Forward.** (Was "More Ask"; retitled 2026-10-04, owner-approved, 4168bb8.) Saved `eotg_cand_a`, `eotg_cand_b`.
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

**.004 Resentment in the Ranks.** (Was "The Unaugmented Resent"; retitled 2026-10-04, owner-approved, 4168bb8.) Every unaugmented knight gets `eotg_opinion_aug_passed_over`.
- **a** "Augment them too." `minor_gold_value` each (cap 3); install.
- **b** "Honour the unaugmented." `medium_gold_value`; replace passed_over with reassured.
- **c** "Let them resent." Retinue knights risk +3 each (isolation).
- **d [just]** "Equal pay. Equal honour." As b, at `minor_gold_value`.
- **e [callous]** "Replace them." `move_to_pool` the most resentful unaugmented knight.

`phase = 5`.

**.005 What the Programme Becomes.**
- **a** "Continue." `eotg_flag_aug_retinue_permanent` on each retinue knight (they carry it). Phase 6 reads it on the knight **or** the liege (balance §5.7: +5 progression chance; *CB-26 S16*).
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
- **e** "Two is enough." **Universal** (*CB-26 L12*): a and c cost gold and b commits to a programme, so this is the option nobody can be locked out of. `eotg_flag_suppress_progression` 3 years; content gets stress relief.

## 4. Data objects
| Key | Type | Values |
|---|---|---|
| `eotg_mod_aug_patron_clause` | modifier | `icon = stewardship_negative`, `monthly_income_mult = -0.05` |
| `eotg_mod_aug_patron_clause_final` | modifier | `icon = stewardship_negative`, `monthly_income_mult = -0.15` |
| `eotg_mod_aug_patron_throttle` | modifier | `icon = health_negative`, `stress_gain_mult = 0.15`, prowess −2 |
| `eotg_mod_aug_iron_retinue` | modifier | `icon = martial_positive`, `knight_effectiveness_mult = 0.1` |
| `eotg_opinion_aug_passed_over` | opinion | −15, applied `years = 5`; retinue.005.d applies `years = 10` (*CB-26 S17*) |
| `eotg_aug_patron_envoy_template` | character template | §2.2 |
| `eotg_aug_patron_envoy_present` | scripted trigger | §2.4 envoy presence (CB-27 M7). Users: patron.002–.006 portraits and options, `eotg_aug_patron_betray_effect` |
| `eotg_aug_patron_critic_candidate` | scripted trigger, `RULER` param | §2.4 .004; excludes the story's own envoy (CB-27 M8). Users: the tick (both cadences), patron.004 trigger and pick |
| `eotg_aug_patron_betray_effect` | scripted effect | §2.4 .006 (c, d failure, e) |
| `eotg_flag_aug_patron_writeoff` | character flag, 60 days | §2.3 entry 2; .006 desc |

On the owner's full removal (`eotg_clean_all_aug_modifiers`), `eotg_mod_aug_iron_retinue` and `eotg_mod_aug_patron_throttle` (a firmware restriction) are removed. **`eotg_mod_aug_patron_clause` and `_clause_final` stay:** the debt is contractual and survives the implants. The clause ends with the story's `on_end`; the final lien is permanent. *CB-26 M6.*

**Index correction:** `eotg_mod_aug_retinue_resentment` (listed in index §3.4) is **dropped**. Resentment is the `passed_over` opinion.

## 5. Deferred
- Inherited patron debt (the story passing to the heir).
- ~~**Betrayal with no hardware or no envoy**~~ **Specced 2026-10-04** in [cybernetics_v2_reprisal.md](cybernetics_v2_reprisal.md) (human-approved): .006 f and the collector (patron.009).
- A visible story-cycle panel for the Patron / Retinue: it would need art, and the Countdown must stay invisible regardless.
- Retinue knights as a men-at-arms-like unit.

## 6. Loc (≈ 140 keys)
- countdown.001–.006, patron.001–.007, retinue.001–.005 and init.019, at ~6 keys each;
- countdown **[voice]** variants (3);
- patron .006 desc variants: betrayal, settlement and write-off, each with an `_absent` form (6 keys; CB-27 M7);
- .005 no-heir variant;
- 4 modifiers and 1 opinion × 2 (`_retinue_resentment` was dropped; *CB-26 S18*).

## 7. Definition of done
0. **Validation, all three clean** on the phase's files, except the known-benign items listed in `CLAUDE.md` §Validation: Tiger 1.17.0 (scratch descriptor), `docs/tools/px_lsp_diagnostics.js` (PX language server, headless) and `docs/tools/px_vocab_check.py` (engine vocabulary + dead hooks). Tiger is the only one of the three that checks scope.
1. The Countdown is created only from the OC on_action or patron.006. It never shows a number, and `visible = no`.
2. No story-fired event checks a cooldown flag.
3. `eotg_trigger_neurofracture` and `eotg_aug_remove_all_effect` end the Countdown.
4. The envoy is created from a template using root's culture and faith by scope. No culture or faith keys.
5. **Human, in game:**
   - Console-set an Overclocked count to risk 55: Minor Anomalies within ~5 months.
   - Accept a patron: Repayment arrives in 2–3 years.
   - Augment one knight through the decision: the retinue story starts at phase 1, and *First of the Iron* follows (*CB-26 M5*).
6. **Patron tick and envoy (CB-27 M7/M8):**
   - The two Patron `first_valid` blocks are identical, in the §2.3 order.
   - `grep -n "scope:eotg_patron_envoy" events/eotg_augmentation_patron.txt`: in .002–.006, every portrait, option effect and opinion on the envoy sits under `eotg_aug_patron_envoy_present` (or inside the betray effect's own guard). The only exception is the `immediate` save.
   - `eotg_aug_patron_betray_effect` adds the throttle, the risk and the Countdown only inside `eotg_is_augmented_any = yes`.
   - **Human, in game:** kill the envoy by console after grievance reaches 3. .006 fires with `desc_betrayal_absent`, no right portrait, and no c or e; a non-deceitful owner sees a and b only.
