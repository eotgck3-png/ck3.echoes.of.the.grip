# Cybernetics v2 — Phase 2: entry hooks and decisions

Index: [cybernetics_v2.md](cybernetics_v2.md). Rules in index §1 apply. Needs Phase 0.

**Purpose & gate.** Gate 3. Not blocked. This phase answers *"why would I put this inside myself?"*:
- seven new entry hooks, plus a decision-driven hub so the player chooses when to enter;
- the parent-death hook for inherited hardware;
- four decisions: in, out, maintenance with a physician, and augmenting others.

It ships alone. The Patron (I-05) and The Arms Race (I-09) are Phase 5. Each leaves a marked slot here.

**Signature resource.** Every accept path sets `eotg_fracture_risk` on whoever is installed: root, a child, or a retainer. Stage-2 events move it. Every event couples.

---

## 1. Wiring

### 1.1 `eotg_on_yearly_aug_initiation_check` (existing, extended)

> **Amended 2026-10-03 after Phase 2 QA (orchestrator ruling, in-file precedent: the tier checks' `random_list`):** the priority `if/else_if` chain below starved its lower branches, because persistent conditions such as physician access, physical loss and infirmity claimed the pulse and then fired nothing most years. The check is now ONE weighted `random_list`: each branch's limit becomes the entry `trigger`, its old chance becomes the weight, and a nothing-entry of 100 is added. Each entry still sets its own cooldown flag. Declining init.006/.007 sets a 10-year declined flag that multiplies that entry's weight by 0.25. **Phase 5 adds the patron and arms-race offers as entries in that list,** not as chain branches. The back-alley retry and the Sickly Child blocks are unchanged.
The existing outer gate (`eotg_can_receive_augmented = yes`, cooldown `eotg_flag_aug_event_cooldown` absent) stays. Inside it, the `if/else_if` priority chain becomes the order below. New branches are marked ★. Each branch sets `eotg_flag_aug_event_cooldown` (2 years unless stated) **in the branch**, then fires the event.

| # | Branch (limit) | Chance | Event |
|---|---|---|---|
| 1 | wounded + at war (existing) | 50 | init.004 |
| 2 ★ | `eotg_has_physical_loss = yes` | 40 | **init.006** The Prosthetic |
| 3 | wounded (existing) | 40 | init.001 |
| 4 ★ | `OR = { has_trait = incapable  has_trait = infirm }` | 30 | **init.007** The Neural Bridge |
| 5 ★ | `has_variable = eotg_parent_hardware` | 60 | **init.013** A Parent's Hardware |
| 6 ★ | `eotg_has_physician_access = yes` | 12 | **init.017** The Physician's Proposal |
| 7 ★ | `has_trait = cynical` + `learning >= 12` | 20 | **init.009** The Cynic's Argument |
| 8 | wealthy landed (existing; gold threshold per Phase 0 §1.5) | 10 | init.002 |
| 9 ★ (Phase 5 slot) | Patron: `OR = { ambitious greedy }`, `gold < medium_gold_value` | — | patron.001 (Phase 5) |
| 10 ★ | `OR = { gold < medium_gold_value  has_trait = deceitful  is_at_war = yes }` | 10 | **init.010** Back-Alley Surgery |
| 11 ★ | `prowess <= 6` + `OR = { any_relation = { type = rival  prowess >= 12 }  is_at_war = yes }` | 15 | **init.016** The Duel Shame |
| 12 | age ≥ 50, prowess ≤ 8 (existing) | 15 | init.003 |
| 13 | augmented peer (existing) | 20 | init.005 (3-year flag) |
| 14 ★ (Phase 5 slot) | Arms Race | — | init.019 (Phase 5) |

**Separate block, outside the unaugmented gate** (the ruler may be augmented or not; the child must not be):

| Branch | Chance | Cooldown flag (set here) | Event |
|---|---|---|---|
| `any_child = { is_alive = yes  age < 16  OR = { has_trait = ill  has_trait = incapable }  eotg_is_augmented_any = no }`, ruler `gold >= minor_gold_value` | 25 | `eotg_flag_aug_child_offer_cooldown` 5 years | **init.014** The Sickly Child |

### 1.2 `on_death` (vanilla hook, extended additively)
```
on_death = { on_actions = { eotg_on_death_aug_hardware } }
eotg_on_death_aug_hardware = {
    trigger = { OR = { has_trait = eotg_cybernetics  has_trait = eotg_neurofractured } }
    effect = {
        every_child = {
            limit = { is_alive = yes  eotg_is_augmented_any = no }
            set_variable = { name = eotg_parent_hardware  value = root  years = 5 }
        }
        if = { limit = { has_trait = eotg_neurofractured }
            every_child = { limit = { is_alive = yes } add_character_flag = { flag = eotg_flag_aug_hardware_fractured  years = 5 } } }
    }
}
```
Root = the dying character (`game/common/on_action/death.txt:7`; lines 1–5 are its comment header). A custom on_action's `trigger`/`effect` blocks are fine. The rule only forbids putting them on the **vanilla** hook.

### 1.3 Decisions → events
`eotg_decision_seek_augmentation` → init.018. `eotg_decision_augment_retainer` → init.020. The other two decisions resolve in their own effect blocks.

---

## 2. Events (`events/eotg_augmentation_initiation.txt`, namespace `eotg_aug_init`)

"install" = `eotg_aug_initiate_effect = yes` + `set_variable = { name = eotg_fracture_risk  value = N }` (inside `hidden_effect`, as the existing events do). "phys" = `eotg_has_physician_access = yes`. Gold uses Phase 0 script values. Every option has an `ai_chance`, base 30 by default (10–40 by index §1 rule 6, *CB-26 L9*: declines and no-ops lower, the offer's main sale higher), with trait modifiers matching its stress helper.

### init.006 — The Prosthetic (I-01) · S
- **Fires:** branch 2. **Trigger:** `eotg_has_physical_loss = yes`. **Desc:** `triggered_desc` per loss (blind / one_legged / maimed / one_eyed), worst first, matching `eotg_aug_restore_loss_effect`'s order.
- **a** "Replace what I lost." Cost `medium_gold_value`, full price: the physician discount belongs to c, which would otherwise be "a plus calibration at the same price" (*CB-26 M4*). Install, risk 0. `eotg_aug_restore_loss_effect`. Helper surgery.
- **b** "I will learn to live with it." Stress: content and humble minor loss, ambitious minor gain. +50 prestige.
- **c** (`trigger` phys; no trait icon) "My physician holds the knife." As a, cost ×0.75. Also `eotg_mod_implant_calibrated` 3 years. If a court physician exists, they get `eotg_opinion_aug_admiration` toward root (10 years), as init.017.a. `eotg_opinion_aug_grateful_patient` is displayed as "Grateful Patient" and only ever sits on the person treated (*CB-26 M3*).
- **d [zealous]** "As I was made, and as I was unmade." +100 piety, `eotg_flag_suppress_progression` 5 years. Stress: zealous medium loss.
- **e [cynical]** "Make it better than the original." As a (full price), + lesson prowess, risk set to 5.
- **Risk:** a/c/e set it. **Saved scopes:** `eotg_physician` (`court_position:court_physician_court_position`, if employed; precedent `events/activities/hunt_activity/hunt_events.txt:21052`).

### init.007 / init.008 — The Neural Bridge (I-02) · M, 2 stages
**init.007 (stage 1).** Fires on branch 4. **Trigger:** `OR = { incapable infirm }`.
- **a** "Build the bridge." Cost `major_gold_value`. Install, risk **30** (a last resort starts hot). `eotg_mod_aug_bridge_strain` 2 years. Trigger init.008 in 90–180 days. Helper surgery.
- **b** "Let me be as I am." Stress: content and humble medium loss. +50 piety.
- **c** (phys) "Only under my physician's eye." As a, risk 20, cost ×0.75.
- **d [craven]** "Not into my head. Never into my head." As b. Stress: craven medium loss.
- **e [ambitious]** "Run it at full current." As a, risk 40. On success at stage 2, also lesson intrigue + lesson martial.

**init.008 (stage 2, the outcome).** `immediate` rolls `random_list`; the chosen branch sets a local flag that picks the desc and options.

| Outcome | Weight | Effect |
|---|---|---|
| success | 50 (+15 phys) | `remove_trait = incapable` (or `infirm`, whichever is held). +50 prestige |
| partial | 30 | trait stays; risk +10; desc "your hands answer, your words do not" |
| complication | 20 (−10 phys) | `increase_wounds_no_death_effect = { REASON = wounds }` (no death before the event opens; *CB-26 L7*), risk +15 |

Options:
- **a** "Then this is who I am now." Ends the chain.
- **b** (partial / complication only) "Again. Recalibrate it." Cost `medium_gold_value`. 50%: success effects; 50%: risk +10 more.
- **c [stubborn]** (partial / complication) "I will make it work by will alone." Lesson martial, risk +5. Stress: stubborn minor loss.

### init.009 — The Cynic's Argument (I-03) · S
- **Fires:** branch 7. **Trigger:** cynical, learning ≥ 12. **Desc:** the ruler argues the case against their own court; variant if any zealous courtier exists.
- **a** "Flesh is not sacred. I will prove it." Cost `medium_gold_value`. Install, risk 0. −50 piety. Every zealous courtier gets `eotg_opinion_aug_disgust` (8 years).
- **b** "Argue it, but leave my body out of it." Lesson learning, +50 prestige.
- **c** "Publish the argument." +100 prestige, −100 piety, zealous courtiers get `eotg_opinion_aug_disgust`. No install. Sets `eotg_flag_aug_published_cynic` (10 years), which makes the next init.018 option a cost ×0.75: the syndicates court you.
- **d [ambitious]** "Every advantage, every time." As a, risk 5, +50 prestige.
- **e [erudite]** "Write the treatise first." As b, + `eotg_flag_suppress_progression` 1 year. Stress: erudite minor loss. (Replaces the proposal's `curious`: `curious` is a childhood trait.)
- **Risk:** a/d set it.

### init.010 / .011 / .012 — Back-Alley Surgery (I-04) · M, 3 stages
**init.010 (stage 1).** Fires on branch 10.
- **a** "Cheap is cheap." Cost `tiny_gold_value`. Install, risk 5. Trigger init.011 in 180–540 days.
- **b** "Not from those hands." Stress: craven and content minor loss.
- **c [deceitful]** "And no one hears of it." As a. Also sets `eotg_flag_aug_backalley_discreet`, which removes the *discovered* outcome at stage 2. Helper lie.
- **d [craven]** "Put me under first. All the way under." As a, risk 10 (sloppy anaesthesia). Stress: craven medium loss.

**init.011 (stage 2, "The Scar Itches").** Also reached from init.018 b. `immediate` rolls:

| Outcome | Weight | Effect (applied in `immediate`, hidden) | Desc |
|---|---|---|---|
| clean | 35 | — | "clean" |
| **hidden flaw** | 15 | `add_character_flag = eotg_flag_aug_hidden_flaw` (Thread T6) | **identical to "clean"**: the player cannot tell |
| infection | 20 | `eotg_mod_aug_infection` 2 years | infection |
| rejection | 15 | — (stage 3) | rejection |
| discovered | 10 (0 if discreet) | `eotg_mod_illegal_implants` | discovered |
| excellent | 5 | `eotg_mod_aug_clean_install` 10 years | excellent |

Options:
- **a** "Good." / "Keep going." (all outcomes)
- **b** (infection) "Fetch a physician." Cost `minor_gold_value` (free if phys). Remove `eotg_mod_aug_infection`.
- **c** (infection) "Sweat it out." Risk +5. 25% `add_trait = ill`.
- **d** (rejection) "Cut it out before it spreads." Trigger init.012.
- **e** (rejection) "It will settle." Risk +10. 30%: trigger init.012 in 60 days anyway.
- **f [lazy]** (infection) "Bandage it and forget it." As c, helper neglect.

**init.012 (stage 3, rejection resolved).** `immediate` rolls: 60% the implant is lost (`eotg_aug_remove_all_effect`, `increase_wounds_no_death_effect = { REASON = treatment }`, so an already-wounded ruler is not reset to rank 1; *CB-26 L8*); 40% saved (risk +10). One option: **a** "So be it." **b [brave]** (lost) "Find me another surgeon." Sets `eotg_flag_aug_backalley_retry` 2 years, which lets init.010 fire again regardless of cooldown. The flag is read **in the on_action**, not the event: while it is held, each pulse rolls a 50% retry (spending the flag and setting the normal 2-year cooldown) **instead of** the initiation list. The Sickly Child block is outside the list and still rolls. *CB-26 L11.*

### init.013 — A Parent's Hardware (I-06) · M
- **Fires:** branch 5. **Saved:** `scope:eotg_dead_parent = var:eotg_parent_hardware`. **Desc:** variant if `eotg_flag_aug_hardware_fractured` ("they say it was the implant that broke them").
- **a** "Install them." Cost `tiny_gold_value`. Install, risk **15** (25 if fractured). `eotg_flag_aug_hidden_flaw`. **If** `scope:eotg_dead_parent` had `var:eotg_aug_voice >= 2`, run `eotg_aug_voice_advance_effect = { STAGE = 1 }`: the parent's echo (Thread T1).
- **b** "Sell them." `add_gold = medium_gold_value`.
- **c** "Destroy them." +50 piety. Stress: zealous and compassionate minor loss.
- **d [greedy]** "Sell them to the highest bidder, and let it be known." `add_gold = { value = medium_gold_value multiply = 1.5 }`, −50 prestige.
- **e [eccentric]** "Keep them. Take them apart. Learn." Lesson learning. (init.013 fires only for unaugmented rulers, so the event couples via a; the old "+5 risk if already augmented" clause was dead and is deleted, *CB-26 S14*.)
- **All options:** `remove_variable = eotg_parent_hardware` and the fractured flag.

### init.014 / .015 — The Sickly Child (I-07) · M, 2 stages *(Q8: tone review)*
**init.014.** Fires from the separate block in §1.1. **Saved:** `eotg_sick_child` (`random_child` with the branch limit, ordered by youngest: use `ordered_child = { order_by = { value = 0 subtract = age } }`).
- **a** "Save them, whatever it takes." Cost `medium_gold_value`. The child runs `eotg_aug_initiate_effect`, `remove_trait = ill` / `incapable`, risk 10 on the child, `eotg_flag_aug_child_patient`. Trigger init.015 in 365–730 days. Root stress: compassionate minor loss, zealous medium gain, just minor gain.
- **b** "Pray, and wait." **Vanilla precedent:** `health.2101.a` "Isolate them and pray for redemption" (`game/events/health_events.txt:5763`, loc `health_events_l_english.yml:211`) has **no piety, no stress and no recovery roll**. The illness simply runs its normal vanilla course. Follow it exactly: no effect. The text must not imply the gods are absent or deaf (the gods have intervened since 850 AG); it frames the outcome as theirs to decide.
- **c** "The experimental procedure. It's cheaper." Cost `tiny_gold_value`. 60%: as a. 40%: the child dies (`death = { death_reason = death_treatment }`, **no killer**; vanilla reason, `game/common/deathreasons/00_event_deaths.txt`). Changed per lore review: the vanilla `death_attempted_treatment` text ("died trying to cure himself/herself") wrongly makes the child the one who chose. Helper murder on root (an unlicensed gamble with a child's life).
- **d [compassionate]** "Sit with them through every hour of it." As a; the child gets `eotg_opinion_aug_reassured` toward root. Stress: compassionate medium loss.
- **e [zealous]** "No machine touches my child." As b, +100 piety. Stress: zealous medium loss.

**init.015 ("The Child Who Hums").** The child is adapting. The hum is **audible hardware** others can hear (coil whine, fan noise): never singing, never "at the edge of hearing". Narrate from the parent's side, with no spectacle on the child's body. Root options:
- **a** "They are alive. That is all." No effect.
- **b** "Teach them to hide it." Helper lie. Child +lesson intrigue.
- **c** "Let them be what they are." Child: +5 risk, +lesson prowess.
- **d [paranoid]** "Have the hardware checked. Every month." Cost `minor_gold_value`, child risk −5.

Coupling: moves the child's risk. The flagged child feeds Phase 6 and the Heir's Arc.

### init.016 — The Duel Shame (I-08) · S
- **Fires:** branch 11. **Saved:** `eotg_rival`, `random_relation = { type = rival  limit = { prowess >= 12 } }` if any. **Desc:** a variant if no rival ("the war has shown everyone").
- **a** "Then make me faster." Cost `medium_gold_value`. Install, risk 0. Helper surgery.
- **b** "Train harder." Lesson prowess. Stress: base minor gain, diligent minor loss.
- **c** "Let them talk." −50 prestige. Stress: content minor loss, arrogant medium gain.
- **d [brave]** (needs `eotg_rival`) "Again. As I am." `duel = { skill = prowess  target = scope:eotg_rival … }`. Win (weighted by the prowess gap, vanilla compare_modifier shape) +200 prestige. Lose: `increase_wounds_effect = { REASON = duel }`.
- **e [arrogant]** "They will regret it." As a, +10 dread, risk 5.

### init.017 — The Physician's Proposal (I-10) · S
- **Fires:** branch 6. **Saved:** `eotg_physician` (court physician, or root if self-physician; the desc changes for the self case).
- **a** "Do it, then." Cost `medium_gold_value` ×0.75. Install, risk 0. `eotg_mod_implant_calibrated` 3 years. The physician gets `eotg_opinion_aug_admiration`.
- **b** "Not yet." No effect.
- **c** "On a volunteer first." Picks an unaugmented knight (picker logic with `limit = { is_knight = yes  eotg_is_augmented_any = no }`; save `eotg_volunteer`). The volunteer runs `eotg_aug_initiate_effect`. Root gets lesson learning. Couples via the knight's tier change.
- **d [trusting]** "I trust your hands." As a, cost ×0.5.
- **e [paranoid]** "And who paid you to suggest it?" The physician gets `eotg_opinion_aug_unease`; root gets lesson intrigue.

### init.018 — The Offer You Sought (I-11) · S, the decision hub
- **Fires:** `eotg_decision_seek_augmentation`.
- **a** "A sanctioned clinic." Cost `medium_gold_value` (×0.75 if `eotg_flag_aug_published_cynic`). Install, risk 0. `eotg_mod_implant_calibrated` 2 years.
- **b** "The back streets." Cost `tiny_gold_value`. Install, risk 5. Trigger **init.011** in 180–540 days. This shares Back-Alley stage 2.
- **c** (phys) "My own physician." Cost ×0.75. Install, risk 0. Calibrated 3 years.
- **d** "Not yet." No effect.
- *(Phase 5 adds **e** "A patron will pay." → starts `eotg_story_aug_patron`.)*

### init.020 — Choosing the Volunteer · S, the retainer decision hub
- **Fires:** `eotg_decision_augment_retainer`. `immediate` saves up to three candidates (adult, unaugmented, alive):
  - `eotg_cand_best`: `ordered_knight` by prowess;
  - `eotg_cand_any`: a random other knight;
  - `eotg_cand_courtier`: `random_courtier` with `is_knight = no`.
- **a / b / c** "[cand].GetName" (each `trigger = { exists = scope:… }`). Cost `minor_gold_value`. That character runs `eotg_aug_initiate_effect`, gets risk 0, and gets `eotg_opinion_aug_grateful_patient`.
- **d [callous]** "Whoever survives it best." The best candidate, cost ×0.5. The candidate gets `eotg_opinion_aug_unease` instead.
- **e** "None of them." No effect.
- *(Phase 5: the second time this resolves in an a/b/c/d, start `eotg_story_aug_retinue` if absent.)*

---

## 3. Decisions (`common/decisions/eotg_augmentation_decisions.txt`)

| Key | is_shown | is_valid | Cost | Cooldown | Effect | AI |
|---|---|---|---|---|---|---|
| `eotg_decision_seek_augmentation` | `eotg_is_augmented_any = no`, `is_adult = yes` | `eotg_can_receive_augmented = yes`, `gold >= tiny_gold_value` | none (the hub charges) | `cooldown = { years = 3 }` | `trigger_event = eotg_aug_init.018` | `ai_potential = { eotg_ai_wants_augmentation = yes }`, `ai_check_interval = 120`, `ai_will_do` base 10, +20 ambitious, +20 cynical, −50 zealous |
| `eotg_decision_remove_implants` | `eotg_is_aug_tier1 = yes` | — | `medium_gold_value` | — | `eotg_aug_remove_all_effect`, `eotg_mod_aug_removal_withdrawal` 3 years, helper reject, `custom_tooltip` | `ai_potential = { stress_level >= 2 }`, +20 content, +20 zealous |
| `eotg_decision_consult_physician` | `has_trait = eotg_cybernetics`, `eotg_has_physician_access = yes` | — | `minor_gold_value` (×0.5 if self-physician) | `cooldown = { years = 3 }` | `eotg_mod_implant_calibrated` 5 years; remove `eotg_mod_aug_infection`; if tier 3, risk −12 (maintenance gives −8); the court physician (if any) gets lesson learning | `ai_check_interval = 60`, base 10, +30 if tier 3 |
| `eotg_decision_augment_retainer` | `has_trait = eotg_cybernetics` | `OR = { any_knight = {…unaugmented adult} any_courtier = {…} }`, `gold >= minor_gold_value` | none (the hub charges) | `cooldown = { years = 2 }` | `trigger_event = eotg_aug_init.020` | base 5, +15 ambitious, +10 callous |

Picture (*CB-26 L10*, placeholders accepted): Seek `decision_smith.dds`; Remove Implants reuses the mod's `eotg_decision_partial_removal.dds` (CB-05); Consult Physician `decision_physician.dds`; Augment a Retainer `decision_knight_kneeling.dds`. All under `gfx/interface/illustrations/decisions/`, all present in 1.20. Bespoke art is human art debt.

---

## 4. Data objects
| Key | Type | Values |
|---|---|---|
| `eotg_mod_aug_removal_withdrawal` | modifier | `icon = health_negative`, prowess −2, `stress_gain_mult = 0.1` |
| `eotg_mod_aug_infection` | modifier | `icon = health_negative`, health −1 |
| `eotg_mod_aug_clean_install` | modifier | `icon = prowess_positive`, prowess +2, `stress_gain_mult = -0.05` |
| `eotg_mod_aug_bridge_strain` | modifier | `icon = health_negative`, `stress_gain_mult = 0.15`, diplomacy −1 |
| `eotg_opinion_aug_grateful_patient` | opinion | +20, no decay; applied with `years = 10` |

All four modifiers go into `eotg_clean_all_aug_modifiers`.

## 5. Loc (≈120 keys)
- 14 events (init.006–.018 and .020) × title + desc + options, plus desc variants: init.006 ×4 losses, init.008 ×3 outcomes, init.011 ×5 desc outcomes (**clean and hidden flaw share one key**), init.013 fractured, init.016 no-rival, init.017 self-physician.
- 4 decisions × (name, desc, tooltip, confirm).
- 4 modifiers × 2; 1 opinion.

## 6. Definition of done
0. **Validation, all three clean** on the phase's files, except the known-benign items listed in `CLAUDE.md` §Validation: Tiger 1.17.0 (scratch descriptor), `docs/tools/px_lsp_diagnostics.js` (PX language server, headless) and `docs/tools/px_vocab_check.py` (engine vocabulary + dead hooks). Tiger is the only one of the three that checks scope.
1. Every ★ branch in §1.1 fires its event and sets its flag in the branch.
2. `on_death` is extended only through `on_actions = { eotg_on_death_aug_hardware }`.
3. init.011's hidden-flaw outcome uses the same desc key as clean.
4. No event `trigger` reads `eotg_flag_aug_event_cooldown`, `_child_offer_cooldown` or `_backalley_retry`.
5. **Human, in game:**
   - A `maimed` count is offered The Prosthetic, and accepting removes `maimed`.
   - Seek Augmentation appears for an unaugmented count, and the hub's three paths install.
   - Killing an augmented parent leaves the heir a Parent's Hardware offer within ~2 years.
