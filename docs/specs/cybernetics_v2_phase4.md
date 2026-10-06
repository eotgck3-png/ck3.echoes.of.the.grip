# Cybernetics v2 — Phase 4: tier content (Augmented, Enhanced, Overclocked)

Index: [cybernetics_v2.md](cybernetics_v2.md). Rules in index §1 apply. Needs Phase 0. The three sub-phases **4a / 4b / 4c** ship independently. Within a tier, all events in that sub-phase ship together.

**Purpose & gate.** Gate 3. Not blocked. Each tier gets its own *kind* of story (proposal §11), not just bigger numbers:

| Tier | Feel | What the events are about |
|---|---|---|
| Augmented | "This is useful." | novelty, the body, the court's eyes, performance |
| Enhanced | "This is becoming part of me." | relationships, judgement, dependence |
| Overclocked | "Something is wrong." | lost time, false memory, malfunction, the voice answering |

**Signature resource.** Every event moves `eotg_fracture_risk` (on root or on a saved augmented character) or changes tier. Below Overclocked, prefer + moves (index §1 rule 4): "calm" choices pay in another resource. The stated exception is tier1.018 a/d, where the copycat's risk −10 is a calm option cleaning up someone else's botched install (*CB-26 S8*).

Conventions: as in Phase 3 §3. Universal options come first (usually **a–c**), trait options after (usually **d–f**). Helpers and lessons are from Phase 0. "phys" = `eotg_has_physician_access = yes`.

---

# 4a — Augmented (`events/eotg_augmentation_tier1.txt`)

## 1. Wiring: `eotg_on_yearly_aug_tier1_check`, random_list additions
The existing branches are unchanged (gold per Phase 0 §1.5). Raise "nothing" from 100 → **150**. Each new branch sets `eotg_flag_aug_event_cooldown` `years = 2`.

| Weight | Trigger | Event |
|---|---|---|
| 20 | — | tier1.007 Firmware Itch |
| 15 | — | tier1.008 Dulled Palate |
| 15 | `OR = { is_married = yes  any_relation = { type = lover } }` | tier1.009 A Lover's Touch |
| 15 | `any_knight = { is_alive = yes }` | tier1.010 The Training Yard |
| 20 | — | tier1.011 The Stare |
| 15 | `OR = { has_trait = zealous  any_courtier = { is_alive = yes  OR = { has_trait = zealous  has_trait = theologian } } }`. Someone must ask for the tithe; the bare `cynical` term is dropped (*CB-26 L24*). | tier1.012 A Tithe for Purity |
| 8 | — | tier1.013 Rejection (stage 1) |
| 12 | `OR = { any_knight = { eotg_is_augmented_any = no  prowess >= 10 }  any_relation = { type = rival } }` | tier1.016 The Challenge |
| 10 | `OR = { any_vassal = { eotg_is_augmented_any = no } any_courtier = { eotg_is_augmented_any = no  is_adult = yes } }` | tier1.018 Copycat |
| 15 | — | tier1.020 Something Is Missing |

Expected: one Augmented event roughly every 3 years, from a 16-event pool.

## 2. Events

**tier1.007 Firmware Itch (A-01).** The implant asks for an update.
- **a** "Schedule the technicians." `remove_short_term_gold = tiny_gold_value`. `eotg_mod_implant_calibrated` 1 year.
- **b** "Later." Helper neglect. Risk +3.
- **c** "Do it myself." 50%: calibrated 2 years. 50%: `eotg_mod_aug_infection` 1 year, risk +5.
- **d [diligent]** "Every week, by the book." Calibrated 2 years. Stress: diligent minor loss.
- **e [lazy]** "If it breaks, it'll tell me." Risk +5. Stress: lazy minor loss.

**tier1.008 Dulled Palate (A-02).** Taste is going.
- **a** "Spice everything." `remove_short_term_gold = minor_gold_value`. Stress minor loss. Risk +2: the implant is retuned to compensate.
- **b** "Food is fuel." `eotg_mod_aug_dulled_senses` 3 years. Risk +3.
- **c** "Retune the receptors." `tiny_gold_value`. Risk +4.
- **d [gluttonous]** "Then I'll eat until I taste something." `change_current_weight = 20` (vanilla). Stress: gluttonous medium loss. Risk +3.
- **e [temperate]** "I won't miss it." Stress: temperate medium loss.

**tier1.009 A Lover's Touch (A-03).** Saved `eotg_partner`: lover, else spouse.
- **a** "Guide their hand to it." 50% `eotg_partner` admiration / 50% unease. Risk +2.
- **b** "Keep it covered." The partner gets unease. Stress minor gain.
- **c** "Have it smoothed and warmed." `minor_gold_value`. The partner gets reassured. Risk +3.
- **d [lustful]** "Show them what it can do." Admiration. Stress: lustful minor loss. Risk +4.
- **e [chaste]** "Then let us not." Unease. Stress: chaste medium loss.

**tier1.010 The Training Yard (A-04).** The machine is outperforming its owner. Saved `eotg_sparring_partner`: `ordered_knight` by prowess.
- **a** "Let the implant fight." Lesson prowess. 20%: partner `increase_wounds_effect = { REASON = fight }`. Risk +4.
- **b** "Override it. Use my own reflexes." Lesson martial. Stress minor gain.
- **c** "Spar with it switched off." −25 prestige. Stress minor loss.
- **d [brave]** "Three at once." Lesson prowess, +100 prestige. 25%: root wounded (fight). Risk +6.
- **e [craven]** "Never again without it." Risk +5. Stress: craven medium loss.
- **f [lifestyle_blademaster]** "The machine is good. I am better." `duel = { skill = prowess  target = scope:eotg_sparring_partner }`. Win: +150 prestige. Lose: −50 prestige and `eotg_flag_aug_challenge_due` 2 years (raises the Challenge's weight ×2; the on_action reads it). Risk +3.

**tier1.011 The Stare (A-05).** A hall full of eyes.
- **a** "Ignore them." Stress minor gain.
- **b** "Stare back." +5 dread. Risk +2.
- **c** "Explain what it does." +25 prestige. Risk +2 (*CB-26 L16*).
- **d [shy]** "Cover it with cloth from now on." −25 prestige. Stress: shy medium loss.
- **e [gregarious]** "Make it the evening's entertainment." +75 prestige. Risk +3. Stress: gregarious minor loss.

**tier1.012 A Tithe for Purity (A-06).** Saved `eotg_pious`: a zealous courtier, else a `theologian` courtier. If the ruler is zealous and no such courtier exists, the variant is "your own conscience".
- **a** "Pay the tithe." `minor_gold_value`, +50 piety. `eotg_pious` gets reassured. The purity pledge: `eotg_flag_suppress_progression` 1 year and helper reject. Without it, a strictly beat c (*CB-26 L17*).
- **b** "Refuse." −25 piety. `eotg_pious` gets disgust.
- **c** "Pay it, and keep upgrading." `minor_gold_value`, +25 piety. Risk +3.
- **d [zealous]** "Fast and pray for a month." +100 piety. `eotg_flag_suppress_progression` 2 years.
- **e [cynical]** "Tithe this." −50 piety, +50 prestige. Disgust. Risk +2.

**tier1.013 / .014 / .015 Rejection (A-07, M).** The body pushes back.
- *.013 Fever.*
  - **a** "Rest." `eotg_mod_withdrawn_from_court` 3 months. → .014 in 30–60 days, flag `rested`. Without the cost, a strictly beat b (*CB-26 L18*).
  - **b** "Keep working." Risk +5. → .014.
  - **c** (phys) "My physician." → .014, flag `treated`.
  - **d [stubborn]** "I don't get sick." Risk +5. → .014.
- *.014 Crisis.*
  - **a** "Fight it." → .015.
  - **b** "Take it out before it takes me." `eotg_aug_remove_all_effect`, `eotg_mod_aug_removal_withdrawal` 2 years. Ends the chain (tier exit).
  - **c [brave]** "Keep it in, whatever it costs." → .015 with failure +10.
- *.015 Outcome.* `immediate` rolls:
  - recover: 50, +10 rested, +15 treated;
  - **implant fails**: 25 → `eotg_aug_remove_all_effect`, `add_trait = wounded_1`;
  - recover scarred: 25 → risk +15.

  Options:
  - **a** "So be it."
  - **b** (failed) "Put a new one in." `medium_gold_value`. `eotg_aug_initiate_effect`, risk 10.

**tier1.016 / .017 The Challenge (A-08, M).** Saved `eotg_challenger`: `ordered_knight` by prowess (unaugmented, prowess ≥ 10), else a rival.
- *.016.*
  - **a** "Accept." Risk +2: the implant spins up for the bout (*CB-26 L19*). → .017.
  - **b** "Refuse." −100 prestige. The challenger gets disgust.
  - **c** "Send my champion." The best knight duels. Win +50 prestige / lose −50.
  - **d [arrogant]** "Accept, with the implant switched off." → .017, flag `unaided` (root prowess counts −2 per tier in the duel weights; the win reward doubles).
  - **e [craven]** "Decline with a smile." −50 prestige. Stress: craven minor loss.
- *.017 The Bout.* `duel = { skill = prowess  target = scope:eotg_challenger }` with four weighted outcomes (compare_modifier shape, `chariot_ongoing_events_jp.txt:195`):

| Outcome | Weighting | Effect |
|---|---|---|
| victory | +10 if `eotg_aug_focus = flag:limbs` | +150 prestige, risk +3 |
| narrow victory | — | +75 prestige, risk +8 ("you let it take over") |
| defeat | — | −100 prestige, stress minor gain |
| severe | — | `increase_wounds_effect = { REASON = duel }` |

One option: **a** "Done."

**tier1.018 / .019 Copycat (A-09, M).** Saved `eotg_copycat`: an unaugmented vassal or adult courtier. In `immediate` they get `eotg_aug_initiate_effect`, risk 20 and `eotg_mod_aug_infection`: a botched black-market job.
- *.018 Their plea.*
  - **a** "Pay for their treatment." `medium_gold_value`. The copycat gets `eotg_opinion_aug_grateful_patient`; their risk −10.
  - **b** "Refuse." Disgust.
  - **c** "Help them, for a price." `add_hook = { type = favor_hook  target = scope:eotg_copycat }`. Their risk +10.
  - **d [generous]** "Pay, and have it done properly." As a, plus their `eotg_mod_implant_calibrated` 3 years.
  - **e [callous]** "Not my problem. Get them out of my hall." If a courtier: `move_to_pool`; else fear.

  All but e → .019 in 1–2 years.
- *.019 Their fate.* `immediate` rolls on the copycat:
  - recovered 50: grateful;
  - worse 35: their risk +20 (they now feed Phase 6);
  - dead 15: `death_reason = death_treatment`.

  **a** "I see." Coupling: moves the copycat's risk.

**tier1.020 Something Is Missing (A-11).** You cannot remember what rain felt like. (The proposal's `curious` is a childhood trait: replaced.)
- **a** "Try to remember." Stress minor gain.
- **b** "Let it go." Stress minor loss. Risk +3.
- **c** "What else can I replace?" Lesson learning. Risk +8. Flag `eotg_flag_aug_replace_more` 5 years (the next tier1.002 cost ×0.85).
- **d [eccentric]** "Fascinating." Lesson learning. Risk +5.
- **e [erudite]** "Write every sensation down before it goes." Lesson learning. Stress minor loss.

**A-12 The First Upgrade.** The existing **tier1.002** becomes stage 1 of 3.
- *tier1.002* (existing, Phase 1 gold): **a** "Proceed" now pays and fires **.021** in 1 day; it no longer sets integration. b and c are unchanged.
  - **d [ambitious]** "Because I can." As a. Risk +3.
  - **e [craven]** "Is it safe? Tell me it's safe." As a; `.021` gets the variant "the surgeon's reassurance". Stress: craven minor gain.
- ***tier1.021 What Will You Change?*** Sets `eotg_aug_focus` (Thread T7). Fires .022 in 30–60 days.
  - **a** "My limbs." `flag:limbs`.
  - **b** "My senses." `flag:senses`.
  - **c** "My nerves." `flag:nerves`. Risk +5.
  - **d [lifestyle_blademaster]** "My sword arm." `flag:limbs`, lesson prowess.
  - **e [eccentric]** "The part that thinks." `flag:nerves`, `eotg_aug_voice_advance_effect = { STAGE = 1 }`, risk +5.
- ***tier1.022 Installation.*** `immediate`: clean 70 (+15 phys) / complication 30 (risk +10, `eotg_mod_aug_infection` 1 year). **All options run** `eotg_aug_set_integration_effect = { XP = 50 }`.
  - **a** "Rise."
  - **b [humble]** "What have I done?" Stress: humble minor gain, +25 piety.

  Coupling: tier change.

---

# 4b — Enhanced (`events/eotg_augmentation_tier2.txt`)

## 3. Wiring
**`eotg_on_yearly_aug_tier2_check` additions.** "Nothing" 100 → **150**. Each branch sets `eotg_flag_enh_event_cooldown` 2 years.

| Weight | Trigger | Event |
|---|---|---|
| 20 | `any_courtier = { is_adult = yes }` | tier2.007 Numbers, Not Faces |
| 40 | `has_variable = eotg_aug_grief_for` | tier2.008 The Late Grief |
| 20 | — | tier2.009 Perfect Recall |
| 15 | `is_landed = yes` | tier2.011 Market Ledger |
| 20 | `exists = cp:councillor_spymaster` | tier2.012 Trust Protocol |
| 12 | NOT `eotg_flag_aug_vendor_done`; the branch sets it permanently | tier2.013 The Bidding War |
| 10 | — | tier2.015 Tampering |
| 15 | — | tier2.019 The Cold Calculation |
| 20 | `OR = { NOT = { has_variable = eotg_aug_voice }  var:eotg_aug_voice < 1 }` + `OR = { var:eotg_fracture_risk >= 10  var:eotg_aug_focus = flag:nerves }` | tier2.020 The Second Self |

**`on_birth_child` → `eotg_on_birth_aug_parent_check`** (new custom on_action). Root is the newborn (`game/common/on_action/child_birth_on_actions.txt:855`). The effect checks each of `scope:father` and `scope:mother`:
```
scope:father ?= { if = { limit = { OR = { eotg_is_aug_tier2 = yes  eotg_is_aug_tier3 = yes }
                                   NOT = { has_character_flag = eotg_flag_aug_birth_cooldown } }
    add_character_flag = { flag = eotg_flag_aug_birth_cooldown  years = 3 }
    root = { save_scope_as = eotg_newborn }
    trigger_event = { id = eotg_aug_tier2.010  days = 3 } } }
```
The mother block is the same. The cooldown flag lives here.

**`on_death` → `eotg_on_death_aug_grief`** (new custom on_action, added next to Phase 2's):
```
every_close_family_member = { limit = { eotg_is_aug_tier2 = yes }
    set_variable = { name = eotg_aug_grief_for  value = root  years = 1 } }
```
If `scope:killer` exists, also set `eotg_aug_grief_killer`. `every_close_family_member` is vanilla (PX effects).

## 4. Events

**tier2.007 Numbers, Not Faces (E-01).** A case before you, reduced to probabilities. Saved `eotg_petitioner`: a random adult courtier.
- **a** "Follow the numbers." `add_gold = minor_gold_value`. The petitioner gets disgust. Risk +4. Helper cruelty.
- **b** "Follow my conscience." +50 prestige. Stress minor gain.
- **c** "Split the difference." —
- **d [just]** "The law, not the ledger." +100 prestige. Stress: just medium loss.
- **e [arbitrary]** "The ledger *is* the law now." `add_gold = medium_gold_value`, `add_tyranny = 5`. Risk +5.

**tier2.008 The Late Grief (E-02).** Saved `eotg_mourned = var:eotg_aug_grief_for`. All options `remove_variable` it.
- **a** "Grieve now. Alone." Stress medium loss.
- **b** "It was months ago. Move on." Risk +4.
- **c** "Visit the grave." +25 piety.
- **d [forgiving]** "Forgive them what was left unsaid." Stress: forgiving medium loss.
- **e [vengeful]** (needs `var:eotg_aug_grief_killer`) "Someone did this." +10 dread. The killer gets `eotg_opinion_aug_fear`. Risk +5.

**tier2.009 Perfect Recall (E-03).**
- **a** "Forget nothing." Lesson intrigue. Risk +3.
- **b** "Purge the archive." Stress minor loss.
- **c** "Bring it to council." +50 prestige. Risk +3.
- **d [honest]** "And remind everyone of every promise they made." Vassals with opinion < 0 get unease; +100 prestige.
- **e [deceitful]** "Know every lie, and keep telling mine." Lesson intrigue. Helper lie. Risk +5.

**tier2.010 Absent at the Birth (E-04).** Fired from `on_birth_child`. Saved `eotg_newborn`. Options a, b and e set `eotg_flag_aug_absent_at_birth` on the child (Thread T3).
- **a** "Hold the child. Feel nothing." Risk +3.
- **b** "Leave the room." The spouse gets unease.
- **c** "Switch it off for the day." Stress medium gain. No flag.
- **d [compassionate]** "Stay until something comes." The spouse gets reassured. Stress minor gain. No flag.
- **e [callous]** "There will be others." The spouse gets disgust. Risk +3.

**tier2.011 Market Ledger (E-05).**
- **a** "Implement it." `eotg_mod_aug_optimised_levies` 3 years. Risk +3.
- **b** "Ignore it." —
- **c** "Have the steward check the arithmetic." Gated on a living steward who is not root (the option names them; vanilla precedent `events/dlc/ep3/ep3_yearly_1.txt:174`). 50% + steward stewardship × 2: `eotg_mod_aug_optimised_levies_trimmed` 3 years (half the tax gain, no vassal penalty). Else nothing. *CB-26 M1.*
- **d [greedy]** "Squeeze harder." As a, plus `add_gold = medium_gold_value`, `add_tyranny = 5`. Risk +5.
- **e [generous]** "Spend the surplus on alms." `remove_short_term_gold = minor_gold_value`, +50 piety; vassals reassured.

**tier2.012 Trust Protocol (E-06).** Saved `eotg_flagged = cp:councillor_spymaster`. `immediate` sets the truth: 30% true (+20 if `eotg_aug_focus = flag:senses`; Thread T7).
- **a** "Investigate quietly." Lesson intrigue. Risk +3. The desc reveals truth **only** at senses focus.
- **b** "Take their keys." The flagged spymaster gets disgust. If false → **.021** in 60–120 days.
- **c** "Ignore it." Risk +4.
- **d [trusting]** "I trust them more than it." Reassured. Risk +5.
- **e [paranoid]** "Arrest them." `imprison`, helper tyranny. If false → .021.

**tier2.021 The Report Was Wrong** (E-06 follow-up). It establishes, before Overclocked, that the implant lies.
- **a** "Apologise." Release if imprisoned; `eotg_opinion_aug_falsely_accused` → reassured. Risk +2.
- **b** "It was right to be careful." Helper lie. Risk +5.

**tier2.013 / .014 The Bidding War (E-07, M).** The choice sets the Overclocked accrual curve (Phase 0 §1.1), not Integration.
- *.013.*
  - **a** "The careful vendor." `eotg_flag_aug_vendor_safe`.
  - **b** "The bold vendor." `eotg_flag_aug_vendor_bold`, `eotg_mod_aug_bold_firmware`. Risk +5.
  - **c** "Play them against each other." Intrigue `random_list`. Success: → .014 with a discount. Failure: both walk away.
  - **d [greedy]** "Take money from both." `add_gold = major_gold_value`, `eotg_flag_aug_vendor_bold` + `eotg_flag_aug_hidden_flaw` (T6). Risk +5.
  - **e [patient]** "Wait for a better offer." → .014 in 1 year.
- *.014 The Vendors Return.*
  - **a** Careful (safe flag, + `add_gold = minor_gold_value` rebate).
  - **b** Bold (bold flag + firmware; risk +3).
  - **c** "Neither." —

**tier2.015 / .016 Tampering (E-08, M).** Saved `eotg_tamperer`: a rival, else a courtier from the victim picker (0.05), else a vassal. **a, c and d fire .016; b ends the chain** (the purge leaves nothing to find). *CB-26 L23.*
- *.015.*
  - **a** "Trace it." `duel = { skill = intrigue  target = scope:eotg_tamperer }` → .016 with the result.
  - **b** "Purge and reinstall." `medium_gold_value`. Risk +2.
  - **c** "Say nothing." Risk +8.
  - **d [paranoid]** "Lock down the court." Helper tyranny. 50%: imprison the tamperer (house arrest). → .016.
- *.016 What Was Done.* Outcome from .015 a/d, else rolled:

| Outcome | Effect |
|---|---|
| culprit named | imprison option; tamperer gets fear |
| malfunction | `eotg_mod_aug_tampered` 1 year |
| risk | +10 |
| **nothing found** | desc says "nothing"; **risk +10 hidden**: unreliable |

**a** "Understood." **b** (culprit) "Make an example." `death_execution`, helper murder.

**tier2.004 / .017 / .018 The Space Between Us (E-09, M/L).** The existing **.004** is stage 1 (Phase 1 options a–d). Each option sets `eotg_aug_marriage_strain` (a 0, b +1, c +2, d 0) and fires **.017** in 180–365 days if still married.
- *.017 Confrontation.* The spouse demands change.
  - **a** "I'll have it dialled down." Remove `eotg_mod_aug_affect_dampened`. Strain −1. `minor_gold_value`.
  - **b** "This is who I am now." Strain +1. Risk +3.
  - **c** "Then let us start again." `medium_gold_value`, as a gift. Strain −1.
  - **d [lustful]** "Remind them what remains." Strain −1. Risk +2.
  - **e [stubborn]** "No." Strain +2.

  All → .018 in 1 year.
- *.018 Resolution,* by strain:
  - ≤ 0 **reconciliation**: spouse admiration, stress medium loss;
  - 1–2 **estrangement**: spouse disgust, `eotg_flag_aug_estranged` on the spouse (Heir's Arc reads it: if the estranged spouse is the heir's parent, `heir_dread +1`), risk +5;
  - ≥ 3 **divorce**.

  Options:
  - **a** (divorce) "Grant it." `divorce = scope:spouse`.
  - **b** (divorce) "Refuse." The spouse gets disgust (10 years). Risk +5.
  - **c** (others) "So it is."

**tier2.019 The Cold Calculation (E-10).** The optimal solution costs lives.
- **a** "Do it." `add_gold = medium_gold_value`, +50 prestige. Helper cruelty. Risk +5.
- **b** "Refuse." Stress minor gain.
- **c** "Find a third way." 50% / 50% (+learning × 2): half the gold, no cruelty.
- **d [compassionate]** "No sum is worth that." +50 piety. Stress: compassionate medium loss.
- **e [callous]** "The arithmetic is clear." `add_gold = major_gold_value`, +10 dread. Risk +5.
- **f [just]** "Put it before the council." 50%: council accepts (as a, no cruelty stress). 50%: refuses.

**tier2.020 The Second Self (E-11; T1 beat 1).** All options run `eotg_aug_voice_advance_effect = { STAGE = 1 }`. (`pensive` and `curious` are childhood traits: replaced with shy and eccentric.)
- **a** "Reject the thought." Stress minor gain.
- **b** "Encourage it." Risk +6.
- **c** "Designate it." Risk +4. The designation is never shown: loc says "you designated it". It is a tool, not a spirit.
- **d [eccentric]** "Talk back." Risk +6.
- **e [shy]** "At last, someone who understands." Risk +5. Stress: shy minor loss.

**E-12 The Next Stage** (existing tier2.003): add `triggered_desc` variants on `eotg_aug_focus` (3) and on `var:eotg_aug_voice >= 1` ("it wants this too"). No other change beyond Phase 1.

---

# 4c — Overclocked (`events/eotg_augmentation_tier3.txt`)

## 5. Wiring: `eotg_on_yearly_aug_overclocked_check` random_list additions
"Nothing" 100 → **200** (Phase 5 doubles it again while the Countdown runs). Cooldown `months = 11` (Phase 0).

| Weight | Trigger | Event |
|---|---|---|
| 20 | — | tier3.008 Tremor |
| 20 | `any_courtier = { is_adult = yes }` | tier3.009 Phantom Orders |
| 15 | — | tier3.010 Heat Spike |
| 15 | — | tier3.011 The Feast You Didn't Eat |
| 30 (×1.5 at `eotg_aug_focus = flag:nerves`, Thread T7) | voice < 2, NOT `eotg_flag_aug_first_contact_done` (set here, permanent) | tier3.012 First Contact |
| 15 | — | tier3.013 Sleepwalker |
| 15 | `any_courtier = { is_adult = yes }` | tier3.014 The Missing Conversation |
| 10 | — | tier3.016 The Bleed |
| 20 | `OR = { any_vassal = {…}  any_courtier = { eotg_aug_victim_candidate = yes } }` | tier3.017 The Plot |
| 15 | `OR = { is_married = yes  exists = cp:councillor_chancellor }` | tier3.019 The Delegation, Revisited |
| 30 | `var:eotg_fracture_risk >= 40`, `OR = { is_married = yes  primary_heir ?= { is_adult = yes } }`, NOT `eotg_flag_aug_intervention_refused` | tier3.020 The Intervention |
| 30 | `is_at_war = yes` | tier3.023 The Clarity Campaign |

tier3.015 is fired by tier3.007 (a/d alliance, b/c rivalry) in 1–2 years if `scope:other_machine` is alive and still tier 3.

## 6. Events

**tier3.008 Tremor (O-01).**
- **a** "Hide your hands." Risk +5.
- **b** "Have it serviced." `minor_gold_value`. Risk −5.
- **c** "Let the court see." −25 prestige. Risk −2.
- **d [patient]** "Wait for it to pass." Risk −3.
- **e [impatient]** "Fix it myself, now." 50% risk −8 / 50% risk +10 and `increase_wounds_effect = { REASON = burned }`.

**tier3.009 Phantom Orders (O-02).** Saved `eotg_order_recipient`. `immediate` picks the order: harmless / harsh / costly.
- **a** "Let it stand." Harsh: `add_tyranny = 5`. Costly: `minor_gold_value`. Risk +5.
- **b** "Countermand it." −50 prestige. Risk −3.
- **c** "Ask what else I have ordered." Risk +3.
- **d [calm]** "Breathe. Decide again." Risk −6.
- **e [wrathful]** "If I ordered it, it was right." +10 dread. Risk +6.

**tier3.010 Heat Spike (O-03).**
- **a** "Emergency maintenance." `medium_gold_value`. Risk −8.
- **b** "Push through." `eotg_mod_aug_overheated` 1 year. Risk +8.
- **c** "Shut it down for a week." −50 prestige. Risk −10.
- **d [brave]** "Push harder." As b, + lesson prowess. Risk +12.
- **e [craven]** "Shut it all down. Now." −100 prestige. Risk −12.

**tier3.011 The Feast You Didn't Eat (O-04).**
- **a** "Laugh along." Helper lie. Risk +3.
- **b** "Admit you don't remember." −50 prestige. Risk −3.
- **c** "Ask who served you." Risk +3.
- **d [gluttonous]** "Then I'll eat it again." `change_current_weight = 10`. Risk +3.
- **e [temperate]** "I would never have eaten that much." −25 prestige. Risk −3.

**tier3.012 First Contact (O-05; T1 beat 2).** All options run `eotg_aug_voice_advance_effect = { STAGE = 2 }`. Desc variants: voice 0 = "a thought that arrives a half-second before you think it"; voice 1 = "the second self replies". Never "answers" (the Void faith's verb).
- **a** "Reply to it." Risk +8. (*CB-26 S9*: the ban on "answers" holds.)
- **b** "Ignore it." Stress medium gain. Risk −3.
- **c** "Tell someone you trust." The spouse (or a friend) gets reassured. Risk −3.
- **d [paranoid]** "It is lying to me." Risk +5.
- **e [zealous]** "No device speaks for me." +50 piety. Risk −5.

**Lore note:** the voice is technological. Follow the register rule and banned-word list in index §5, here and in every **[voice]** line (fracture.010, .011, .013, .017, .022, .026, .027 and the Countdown variants). Zealous lines reject the *machine*, never a spirit.

**tier3.013 Sleepwalker (O-06).** Saved `eotg_finder`: a knight, else a courtier.
- **a** "Double the guard on my door." `minor_gold_value`. Risk −3.
- **b** "I meant to be there." Helper lie. Risk +3.
- **c** "Follow me next time." The finder gets admiration.
- **d [shy]** "Never speak of it." The finder gets `add_hook = { type = favor_hook  target = root }`, as their secret. Risk +3.
- **e [paranoid]** "Who let me out?" The finder gets fear. Risk +5.

**tier3.014 The Missing Conversation (O-07).** Saved `eotg_claimant`. `immediate` sets truth: 60% true / 40% exploiting.
- **a** "Trust them." If exploiting: `minor_gold_value` lost. Risk +3.
- **b** "Investigate." Intrigue `random_list` inside `hidden_effect`; what you learned is reported by toast (`.toast_lie` / `.toast_true` / `.toast_unknown`), the vanilla hidden-outcome pattern (hunt.8540). A desc cannot report it: it shows before the click. Round 2 M7 also hides a's outcome behind a neutral tooltip. *CB-26 L22.*
- **c** "Pretend to remember." Helper lie. Risk +5.
- **d [trusting]** "Of course." Reassured. Risk +3.
- **e [paranoid]** "Liar." Fear. Helper tyranny. Risk +5.

**tier3.015 Two Machines: The Next Meeting (O-08).** Branches on the flag set by .007's option.
- *Alliance:*
  - **a** "Swear it." `set_relation_friend = { target = scope:other_machine  reason = <loc key> }`. Both risk −5.
  - **b** "Spar to keep each other sharp." Both get lesson prowess. Both risk +8.
- *Rivalry:*
  - **c** "Settle it." Prowess duel. The loser is wounded (duel); the winner +150 prestige. Both risk +10.
  - **d** "Have them watched." Lesson intrigue. Risk +3.
- **e [vengeful]** (rivalry) "End it." Helper murder; `death_murder` killer root, 40% success, else exposed (−200 prestige). Risk +12.

**tier3.016 / .022 The Bleed (O-10, M).** `immediate`: risk +15.
- *.016.*
  - **a** "Lie down. Wait." → .022.
  - **b** "Purge it." `major_gold_value`, or free with phys. Risk −10. → .022 with early cascade ×0.5.
  - **c** "Ride it." Lesson martial. Risk +10. → .022 with insight +15.
  - **d [brave]** "Ride it, and smile." As c, +75 prestige.
- *.022 Outcome.* `immediate` rolls:
  - **early cascade**: 20, +20 if `eotg_neurofracture_threshold_met`; runs `eotg_trigger_neurofracture`;
  - **scarring**: 45; `add_trait = scarred`, `eotg_mod_aug_overheated` 3 years;
  - **insight**: 35; lesson learning + lesson intrigue, voice advance **1**. Beat 2 belongs to First Contact's scene; advancing to 2 here would close its branch unseen. *CB-26 S10.*

  **a** "..."

**tier3.017 / .018 The Plot (O-09, M).** `immediate`: `eotg_conspirator` = a random vassal, else picker(…, 0.05). Truth 30% (+20 at senses focus).
- *.017.*
  - **a** "Arrest them." `imprison` (dungeon), helper tyranny. Risk +5.
  - **b** "Execute them." `death_execution`, helper murder. Risk +10.
  - **c** "Investigate in secret." Intrigue `random_list`; .018 then says whether you learned the truth. Risk +3.
  - **d** "Ignore it." Risk +8.
  - **e [paranoid]** "Arrest them all." `eotg_aug_pick_second_victim_effect` for a second suspect; both imprisoned. Helper tyranny. Risk +12.
  - **f [just]** "A trial, in open court." −50 prestige. If true: imprisonment with no tyranny. If false: release.

  All options → .018 in 120–240 days.
- *.018 The Truth,* by truth × action:

| Case | Effect |
|---|---|
| false + executed | `eotg_opinion_aug_falsely_accused` on the conspirator's close family and vassals; `add_tyranny = 10` |
| false + imprisoned | **a** "Release them." / **b** "Keep them." (helper lie, risk +5) |
| true | +150 prestige ("the machine was right") |
| ignored + true | `increase_wounds_effect = { REASON = attacked }` on root: "an attempt was made"; risk +5 |

**tier3.019 / .021 The Delegation, Revisited (O-12).** Saved `eotg_delegate`: `cp:councillor_chancellor`, else the spouse.
- *.019.*
  - **a** "Delegate to them." The delegate gets admiration. Risk −5. ~~and `eotg_flag_aug_trusted_delegate`~~ (flag dropped, architect decision 2026-10-05, below). → .021 in 180–360 days.
  - **b** "Keep everything in my own hands." +50 prestige (authority kept; without it, a strictly beat b; *CB-26 L20*). Risk and lesson per balance §5.6's stewardship roll.
  - **c [humble]** "Delegate everything." As a, + `eotg_mod_withdrawn_from_court` 1 year. Risk −8.
- *.021 The Other Order.* The delegate swears you ordered something you didn't. `immediate`: 50% you did, and your memory is wrong.
  - **a** "Back them." −50 prestige. Risk +3.
  - **b** "Overrule them." The delegate gets disgust. Risk +5.
  - **c** "Check the logs." The truth is revealed: if you did, risk +5.

~~Phase 3a's Containment Regency may use the trusted delegate as keeper when there is no spouse or adult heir. This is an optional cross-phase read.~~ **Dropped (architect decision, 2026-10-05; QA `docs/qa/loc_bug_hunt_2026-10-05.md` found the flag set at tier3.019.a/.c and read nowhere).** `eotg_flag_aug_trusted_delegate` is removed: the scripter deletes both sets in tier3.019 (a and c, which inherits a). Why: the read was optional and never built; .021 works from the saved `eotg_delegate` scope, not the flag; the delegate is the chancellor or the spouse, and the spouse is already fracture.025's first keeper, so the read would add only the chancellor; and a new keeper branch is new event content, which is the owner's call, not a fix. If the owner later wants the chancellor as a fallback keeper, re-add the flag with fracture.025's keeper picker as its reader.

**tier3.020 The Intervention (O-11).** Saved `eotg_intervener`: the spouse, else the adult heir.
- **a** "I'll schedule the downgrade." `eotg_flag_aug_intervention_discount` 2 years (B3). Reassured. Risk −5.
- **b** "No." `eotg_flag_aug_intervention_refused` 2 years (T3). Disgust. Risk +5.
- **c** "Later." Risk +3.
- **d [compassionate]** "You're right. I'm frightened." As a, plus admiration. Risk −8.
- **e [stubborn]** "Never." As b. Risk +8.
- **f [paranoid]** "Who sent you?" Fear, + the refused flag. Risk +6.

**tier3.023 / .024 The Clarity Campaign (O-14).**
- *.023.*
  - **a** "Follow it." `eotg_mod_aug_clarity_campaign` 1 year. Risk +10. → .024 in 180–270 days.
  - **b** "Reject it." Stress minor gain. Risk −3.
  - **c** "Not yet. Gather more." Lesson martial (5 years). Risk +3. (*CB-26 L21*: without the lesson, c had no upside against b.)
  - **d [brave]** "And I lead the charge." As a, + lesson prowess. Risk +12.
  - **e [craven]** "Command from the capital." −50 prestige. Risk −3.
- *.024 The Engagement.* `immediate` rolls:
  - **decisive**: 50, +15 if focus limbs or senses; +300 prestige;
  - **overreach**: 30; risk +15, `increase_wounds_effect = { REASON = battle }`, −100 prestige;
  - **inconclusive**: 20.

  Options:
  - **a** "As foreseen."
  - **b [arrogant]** (decisive) "As I foresaw." +100 prestige more. Risk +5.

The war itself is not modified: no war-score effect, map-agnostic.

---

## 7. Data objects (all go into `eotg_clean_all_aug_modifiers`)
| Key | Contents |
|---|---|
| `eotg_mod_aug_dulled_senses` | `icon = health_negative`, `stress_loss_mult = -0.1` |
| `eotg_mod_aug_bold_firmware` | `icon = prowess_positive`, prowess +2 (no expiry; removed with the implants) |
| `eotg_mod_aug_optimised_levies` | `icon = stewardship_positive`, `domain_tax_mult = 0.1`, `vassal_opinion = -5` |
| `eotg_mod_aug_optimised_levies_trimmed` | `icon = stewardship_positive`, `domain_tax_mult = 0.05` (tier2.011.c success; *CB-26 M1*) |
| `eotg_mod_aug_tampered` | `icon = intrigue_negative`, prowess −2, diplomacy −2 |
| `eotg_mod_aug_overheated` | `icon = health_negative`, health −0.5, prowess +2 |
| `eotg_mod_aug_clarity_campaign` | `icon = martial_positive`, `advantage = 15`, `enemy_hard_casualty_modifier = 0.15` |

All modifier tags were checked against the PX modifier list.

Local saved variables used by chains (`eotg_aug_marriage_strain`, truth/outcome flags) are removed by the last stage of their chain.

## 8. Loc (≈ 290 keys)
- 4a: 16 events (incl. tier1.021/.022) plus the tier1.002 d/e options.
- 4b: 15 events, plus E-12 variants (4).
- 4c: 17 events.
- 7 modifiers × 2 (incl. `_optimised_levies_trimmed`, CB-26 M1).
- Outcome desc variants are listed per event above (Challenge 4, Copycat 3, Tampering 4, Space resolution 3, Plot 4, Bleed 3, Clarity 3).

## 9. Definition of done
0. **Validation, all three clean** on the phase's files, except the known-benign items listed in `CLAUDE.md` §Validation: Tiger 1.17.0 (scratch descriptor), `docs/tools/px_lsp_diagnostics.js` (PX language server, headless) and `docs/tools/px_vocab_check.py` (engine vocabulary + dead hooks). Tiger is the only one of the three that checks scope.
1. Every new event is fired by a §1 / §3 / §5 branch, the `on_birth_child` / `on_death` on_actions, or a chain stage.
2. `eotg_aug_set_integration_effect` is called only in tier1.022 (plus the existing callers). It is no longer called in tier1.002.
3. No `curious` / `pensive`. No positive permanent skill in repeatable options.
4. `on_birth_child` and `on_death` are extended only via `on_actions = { }`.
5. **Human, in game:**
   - The First Upgrade asks what to change and installs at stage 3.
   - A child born to an Enhanced parent fires Absent at the Birth.
   - First Contact fires once.
   - The Plot's reveal arrives months later.
