# Cybernetics v2 — Phase 0: balance calls and shared foundations

Index: [cybernetics_v2.md](cybernetics_v2.md). Rules in index §1 apply.

**Purpose & gate.** Gate 3. Not blocked. This phase changes no content and adds no events. It does two things:
- applies the logic audit's remaining design calls (B1–B6, recommendations as written; if the human overrides one, only the matching row here changes);
- defines the helpers every later phase calls.

It ships alone: after it, the existing 31 events play with the new pacing.

**Signature resource.** `eotg_fracture_risk` (hidden). This phase changes how it accrues and drifts, and nothing else.

Existing script is referenced by **on_action name / effect name / decision key**, never by line. The scripter's in-flight fixes (index §1 rule 12) land first.

---

## 1. Balance changes

### 1.1 B2: Overclocked accrual (in `eotg_on_yearly_aug_overclocked_check`)
Replace the accrual block (base, stress, paranoid, war) with:

| Condition | `eotg_add_fracture_risk` AMOUNT |
|---|---|
| always | 12 |
| `stress_level = 1` | +8 |
| `stress_level = 2` | +16 |
| `stress_level >= 3` | +24 |
| `has_trait = paranoid` | +12 (unchanged) |
| `is_at_war = yes` | +10 (unchanged) |
| `has_character_flag = eotg_flag_aug_hidden_flaw` | +4 (new; set in Phase 2) |
| `has_character_flag = eotg_flag_aug_vendor_safe` | −3 (new; set in Phase 4b) |
| `has_character_flag = eotg_flag_aug_vendor_bold` | +3 (new; set in Phase 4b) |

Write these as separate `if` blocks. Do not use one parameterised value: the stress-level rows are mutually exclusive `if/else_if`.

`eotg_neurofracture_threshold_met`: delete the `AND = { … >= 60  stress >= 200 }` branch. The body becomes `eotg_is_aug_tier3 = yes`, `has_variable = eotg_fracture_risk`, `var:eotg_fracture_risk >= 80`. Update the on_action header comment ("Threshold: 80").

### 1.2 B1: Neurofractured drift (in `eotg_on_yearly_aug_neurofractured_check`)
Insert a drift block at the top of the effect, **outside** the cooldown `if`, limited to `has_trait = eotg_neurofractured`:

| Condition | AMOUNT |
|---|---|
| always | +8 |
| `stress_level = 1 / 2 / >=3` | +4 / +8 / +12 |
| `has_character_flag = eotg_flag_aug_sedated` (Phase 3b) | −6 |
| `has_character_flag = eotg_flag_aug_restrained` (Phase 3b) | −4 |

Until Phase 3a replaces the pool, the existing ≥30/≥60 weight modifiers in the NF `random_list` now see real values. No other change.

### 1.3 B3: regression decisions (`common/decisions/eotg_augmentation_decisions.txt`)
| Decision | Change |
|---|---|
| `eotg_decision_partial_removal` | `is_valid`: drop `stress >= 100`. `cost = { gold = { value = medium_gold_value  if = { limit = { OR = { stress_level >= 2  has_character_flag = eotg_flag_aug_intervention_discount } } multiply = 0.75 } } }`. No `is_valid_showing_failures_only` gold check: `cost` alone is the vanilla convention (vanilla never tests gold in `is_valid`). *Amended 2026-10-04, CB-26 L1.* |
| `eotg_decision_overclock_regression` | `is_valid`: drop `stress >= 200`. Cost as above with `major_gold_value`. **Effect: add** `change_variable = { name = eotg_fracture_risk  multiply = 0.5 }` before `eotg_aug_set_integration_effect = { XP = 50 }`. Remove `eotg_flag_aug_intervention_discount` if present. |
| `eotg_decision_maintenance_protocol` | `cost = { gold = minor_gold_value }`. If `eotg_has_physician_access = yes`, multiply by 0.75. The tooltip text is already reworded (track spec Q1). |

`ai_potential` for both regressions: replace the stress thresholds with `stress_level >= 2` (AI keeps its "only when hurting" behaviour). `ai_will_do` unchanged.

Loc: revise `eotg_decision_partial_removal_tooltip` and `eotg_decision_overclock_regression_tooltip` ("Some of the damage remains." for the latter: no number).

### 1.4 B4: cooldown durations (on_action branches only)
| On_action | Flag | Old | New |
|---|---|---|---|
| `eotg_on_yearly_aug_overclocked_check` | `eotg_flag_oc_event_cooldown` | `months = 6` | `months = 11` |
| `eotg_on_yearly_aug_neurofractured_check` | `eotg_flag_nf_event_cooldown` | `months = 12` (all branches but Massacre) | `months = 11` |
| same, Court Massacre branch | same | `years = 2` | `months = 23` |
| `eotg_trigger_neurofracture` (effect) | same | `months = 12` | `months = 11` |

### 1.5 B5: gold mapping for existing costs
Applied in Phase 1, when each event is touched anyway. Listed here so there is one table:

| Site (event.option / decision) | Flat today | Scaled |
|---|---|---|
| tier1.001.b Recalibrate | 25 | `tiny_gold_value` |
| tier1.002.a The Upgrade | 100 | `medium_gold_value` (moves to tier1.002 stage 1 in Phase 4a) |
| tier2.001.c Increase responsiveness | 50 | `minor_gold_value` |
| tier2.003.a The Next Stage | 200 | `major_gold_value` |
| tier2.003.c Test on prisoners | 100 (in-flight fix) | `medium_gold_value` |
| tier3.004.b Override protocols | 75 | `minor_gold_value` |
| on_action gate checks (`gold >= 100` / `gold >= 200` in the tier-1/2 random_list branch triggers) | flat | `gold >= medium_gold_value` / `gold >= major_gold_value` |
| init on_action "Corporate offer" (`gold >= 500`) | flat | `gold >= { value = major_gold_value multiply = 1.5 }` |
| fracture.007.a Write them down (`add_gold = 75`) | flat | `add_gold = minor_gold_value` |

Trigger forms need the value in a script value. Use `gold >= medium_gold_value`, which vanilla accepts in triggers (`common/decisions/10_religious_decisions.txt:3054`).

### 1.6 B6: lesson modifiers (`common/modifiers/eotg_augmentation_modifiers.txt`)
| Key | Icon | Effect | Applied |
|---|---|---|---|
| `eotg_mod_aug_lesson_prowess` | `prowess_positive` | `prowess = 2` | `years = 5` |
| `eotg_mod_aug_lesson_learning` | `learning_positive` | `learning = 2` | `years = 5` |
| `eotg_mod_aug_lesson_intrigue` | `intrigue_positive` | `intrigue = 2` | `years = 5` |
| `eotg_mod_aug_lesson_martial` | `martial_positive` | `martial = 2` | `years = 5` |

`prowess_positive.dds` exists in `game/gfx/interface/icons/modifiers/` (checked). Phase 1 lists which options switch. All four go into `eotg_clean_all_aug_modifiers`.

---

## 2. Shared foundations

### 2.1 Triggers (`common/scripted_triggers/eotg_augmentation_triggers.txt`)
```
eotg_aug_pressure_flicker  = { OR = { NOT = { has_variable = eotg_fracture_risk }  var:eotg_fracture_risk < 30 } }
eotg_aug_pressure_fracture = { has_variable = eotg_fracture_risk  var:eotg_fracture_risk >= 30  var:eotg_fracture_risk < 60 }
eotg_aug_pressure_storm    = { has_variable = eotg_fracture_risk  var:eotg_fracture_risk >= 60 }
eotg_has_physical_loss     = { OR = { has_trait = maimed  has_trait = one_legged  has_trait = one_eyed  has_trait = blind } }
eotg_has_physician_access  = { OR = { has_trait = lifestyle_physician  employs_court_position = court_physician_court_position } }
eotg_aug_is_nonruler       = { eotg_is_augmented_any = yes  highest_held_title_tier < tier_county }
eotg_aug_victim_candidate  = { is_alive = yes  is_imprisoned = no  NOT = { this = root }  NOT = { has_trait = eotg_neurofractured } }
```
(Shown as logic; the scripter writes normal block layout.) `employs_court_position = court_physician_court_position` is vanilla (`events/activities/hold_court_activity/hold_court_events_general.txt:11143`).

`eotg_is_augmented_any` gains `has_trait = eotg_total_integration` in Phase 3b.

### 2.2 `eotg_aug_pick_victim_effect = { NAME = x  FAMILY_FACTOR = y }`
Picks one courtier of the current scope (the ruler) and saves them as `scope:$NAME$`. If no candidate exists, nothing is saved: callers must guard with `exists = scope:$NAME$` before using it, and every caller's loc needs a "no one was near" variant.
```
random_courtier = {
    limit = { eotg_aug_victim_candidate = yes }
    weight = {
        base = 100
        modifier = { factor = 1.5   is_knight = yes }                                     # guards and knights stand closest
        modifier = { factor = $FAMILY_FACTOR$  OR = { is_close_family_of = root  is_spouse_of = root } }
        modifier = { factor = 0.25  age < 16 }
    }
    save_scope_as = $NAME$
}
```
**Family factor by context:** 0.05 for Overclocked and Flicker/Fracture-band sites; 0.25 for Storm-band and Court Massacre sites; 0 where family must never be hit (the scripter passes 0; vanilla accepts a 0 factor). Family is "possible but rare, and deliberate when it happens". The Storm factor is that deliberate escalation.

For multi-victim sites the caller calls it twice with different `NAME`s. The second call adds `NOT = { this = scope:<first> }` through a wrapper `eotg_aug_pick_second_victim_effect = { NAME  FAMILY_FACTOR  EXCLUDE }` (same body plus that limit).

Victims hurt in an episode get `add_character_flag = { flag = eotg_flag_aug_breach_victim  days = 30 }` from the caller, so "execute the survivors" (fracture.002.c) only reaches people hurt in that episode. Audit §1.5.

### 2.3 Other effects
| Effect | Body |
|---|---|
| `eotg_aug_remove_all_effect` | If held, remove `eotg_cybernetics`, `eotg_neurofractured` and (from 3b) `eotg_total_integration`. Run `eotg_clean_all_aug_modifiers = yes`. `remove_variable` `eotg_fracture_risk`, `eotg_aug_voice`, `eotg_aug_focus`. `remove_character_flag` `eotg_flag_aug_vendor_safe` / `_bold`. Phase 5 adds: end any owned `eotg_story_aug_countdown`. Does **not** add withdrawal (callers choose). |
| `eotg_aug_restore_loss_effect` | Removes **one** physical-loss trait, priority `blind` > `one_legged` > `maimed` > `one_eyed` (worst first). `if/else_if` chain like `eotg_aug_heal_wounds_effect`. |
| `eotg_aug_voice_advance_effect = { STAGE = n }` | `if = { limit = { OR = { NOT = { has_variable = eotg_aug_voice }  var:eotg_aug_voice < $STAGE$ } }  set_variable = { name = eotg_aug_voice  value = $STAGE$ } }`. Never lowers it. |

### 2.4 Stress helpers (each is one `stress_impact = { … }`; callers add their own `base` in a separate `stress_impact` when needed)
| Effect | Gains | Losses |
|---|---|---|
| `eotg_aug_stress_surgery_effect` (undergo or deepen implants) | craven medium, zealous medium, humble minor | brave minor, cynical minor, ambitious minor |
| `eotg_aug_stress_embrace_effect` (lean into the machine) | zealous medium, content minor, humble minor | cynical minor, ambitious minor, eccentric minor |
| `eotg_aug_stress_reject_effect` (refuse or restrain it) | ambitious minor, arrogant minor, cynical minor, impatient minor (G9), gluttonous minor (G9) | content minor, zealous minor, humble minor, temperate minor (G9) |
| `eotg_aug_stress_wound_effect` (harm someone, non-lethal) | compassionate medium, forgiving minor, just minor | sadistic minor, wrathful minor |
| `eotg_aug_stress_murder_effect` (kill, execute) | compassionate **major**, just medium, forgiving medium | sadistic medium, wrathful minor |
| `eotg_aug_stress_cruelty_effect` (menace, mass fear) | compassionate minor, forgiving minor, shy minor | sadistic minor, arrogant minor, wrathful minor |
| `eotg_aug_stress_tyranny_effect` (arrest, punish vassals) | just medium, compassionate minor, trusting minor | arbitrary minor, paranoid minor, vengeful minor |
| `eotg_aug_stress_lie_effect` (deceive) | honest medium, just minor | deceitful minor |
| `eotg_aug_stress_neglect_effect` (ignore symptoms or maintenance) | diligent minor, paranoid minor | lazy minor, fickle minor (G9) |

"minor/medium/major" means `minor_stress_impact_gain` / `_loss` etc. (vanilla values 20/40/80 and −15/−30/−65; `common/script_values/`).

---

## 3. Loc (eotg-localizer)
- `eotg_mod_aug_lesson_{prowess,learning,intrigue,martial}` + `_desc` (8). Proposed names: "Lesson in the Body", "Lesson in Memory", "Lesson in Faces", "Lesson in Formation". Register: something learned through the implant.
- Revised: `eotg_decision_partial_removal_tooltip`, `eotg_decision_overclock_regression_tooltip`. No numbers about risk.
- Each picker caller supplies its own "no one was near" desc variant (Phase 1/3/4).

## 4. Definition of done
0. **Validation, all three clean** on the phase's files, except the known-benign items listed in `CLAUDE.md` §Validation: Tiger 1.17.0 (scratch descriptor), `docs/tools/px_lsp_diagnostics.js` (PX language server, headless) and `docs/tools/px_vocab_check.py` (engine vocabulary + dead hooks). Tiger is the only one of the three that checks scope.
1. `eotg_neurofracture_threshold_met` contains no `stress` reference; the threshold is 80.
2. The OC accrual block has the 9 rows of §1.1; the NF drift block has the 4 rows of §1.2 and runs outside the cooldown check.
3. Neither regression decision has a stress term in `is_valid`; both costs use script values; the Downgrade halves risk.
4. The four flag durations of §1.4 are applied.
5. The 4 lesson modifiers and all §2 helpers exist; `eotg_clean_all_aug_modifiers` removes the lesson modifiers.
6. Tiger clean (known-benign excepted).
7. **Human, in game:**
   - Overclocked count at stress 0: no cascade before the 7th pulse. Console `add_stress 250`: cascade within 3 pulses.
   - A Neurofractured count with no choices made reaches the ≥30 band in ~3–4 years.
   - Downgrade Protocol is takeable at stress 0.
