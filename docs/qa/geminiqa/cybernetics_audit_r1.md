# GeminiQA: Shipped Cybernetics Audit (Round 1)

**Reviewer:** GeminiQA (Independent Read-Only QA Reviewer)  
**Date:** 2026-10-06  
**Target:** Shipped Cybernetics System (`events/eotg_augmentation_*.txt`, related `common/` files, `localization/english/eotg_augmentation_l_english.yml`)  
**Scope Exclusions:** `events/eotg_augmentation_kingpin.txt` and `events/eotg_augmentation_inherit.txt` (currently in active construction).

---

## 1. Findings (Ordered by Severity, then File)

### BLOCKER Findings
*(None detected. No fatal engine crashes, hard lockups, or broken infinite recursion loops found in the shipped cybernetics suite.)*

---

### MAJOR Findings

#### GQA-001
- **Severity:** MAJOR
- **Category:** 1 (Text that lies)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:2242` and `common/decisions/eotg_augmentation_decisions.txt:63, 120, 380`
- **Key / Context:** `NOT_eotg_decision_aug_removal_booked_tt` used in `eotg_decision_partial_removal`, `eotg_decision_overclock_regression`, and `eotg_decision_remove_implants`.
- **Evidence:**
  `localization/english/eotg_augmentation_l_english.yml:2242`:
  ```yaml
  NOT_eotg_decision_aug_removal_booked_tt:0 "[recipient.GetFirstName] already has a procedure booked"
  ```
  `common/decisions/eotg_augmentation_decisions.txt:62-65`:
  ```pdx
  custom_description = {
      text = eotg_decision_aug_removal_booked_tt
      NOT = { has_variable = eotg_aug_removal_kind }
  }
  ```
- **Why it's wrong:** In character interactions (`eotg_aug_demand_removal_interaction:490`), `scope:recipient` is defined and valid. However, the exact same trigger loc key (`eotg_decision_aug_removal_booked_tt` / `NOT_eotg_decision_aug_removal_booked_tt`) is also used in three personal decisions (`partial_removal`, `overclock_regression`, `remove_implants`). In a decision's `is_valid` block, `root` is the character taking the decision, and `scope:recipient` does not exist. When the requirement fails and the player views the decision tooltip, `[recipient.GetFirstName]` evaluates to an empty string, rendering as `" already has a procedure booked"`.
- **Suggested fix:** Decouple the interaction and decision tooltips, or rephrase `NOT_eotg_decision_aug_removal_booked_tt` without relying on `[recipient.GetFirstName]`, e.g.:
  ```yaml
  NOT_eotg_decision_aug_removal_booked_tt:0 "Already have a procedure booked"
  ```
  Or introduce a dedicated key `eotg_aug_demand_removal_booked_tt` for the interaction.
- **Confidence:** High.

#### GQA-002
- **Severity:** MAJOR
- **Category:** 1 (Text that lies)
- **Location:** `events/eotg_augmentation_tamper.txt:282-293` & `localization/english/eotg_augmentation_l_english.yml:2040`
- **Key / Context:** Event `eotg_aug_tamper.004` (A Fault in the Hardware), key `eotg_aug_tamper.004.desc_known`.
- **Evidence:**
  `events/eotg_augmentation_tamper.txt:282-293`:
  ```pdx
  first_valid = {
      triggered_desc = {
          trigger = {
              OR = {
                  exists = scope:scheme_discovered
                  exists = scope:eotg_tamper_signed
              }
          }
          desc = eotg_aug_tamper.004.desc_known
      }
      desc = eotg_aug_tamper.004.desc_unknown
  }
  ```
  `localization/english/eotg_augmentation_l_english.yml:2040`:
  ```yaml
  eotg_aug_tamper.004.desc_known:0 "\n\n[owner.GetName]'s people opened the panel while you slept, and made sure you would know it."
  ```
- **Why it's wrong:** The description asserts that the agents `"made sure you would know it"`. That statement is only true when option `.002.b` (`[sadistic] "Let them know whose hands."`) was selected, which explicitly saves `eotg_tamper_signed`. On the path where the scheme owner chose option `.002.a` (`"Quietly done."`), the owner intended stealth; if `scope:scheme_discovered` was set, the agents were caught/seen accidentally, not because they intentionally left a signature. Claiming they `"made sure you would know it"` is false on the stealth-but-discovered path.
- **Suggested fix:** Split into two `triggered_desc` blocks: one checking `exists = scope:eotg_tamper_signed` showing `desc_known_signed` (`"[owner.GetName]'s people opened the panel while you slept, and made sure you would know it."`), and one checking `exists = scope:scheme_discovered` showing `desc_known_discovered` (`"[owner.GetName]'s people were seen leaving your quarters after tampering with your diagnostic panel."`).
- **Confidence:** High.

#### GQA-003
- **Severity:** MAJOR
- **Category:** 1 (Text that lies / omission of major outcome)
- **Location:** `events/eotg_augmentation_tier3.txt:2520-2525` & `localization/english/eotg_augmentation_l_english.yml:1350`
- **Key / Context:** Event `eotg_aug_tier3.018` (The Plot: The Truth), key `eotg_aug_tier3.018.desc_false`.
- **Evidence:**
  `events/eotg_augmentation_tier3.txt:2524`:
  ```pdx
  desc = eotg_aug_tier3.018.desc_false
  ```
  `localization/english/eotg_augmentation_l_english.yml:1350`:
  ```yaml
  eotg_aug_tier3.018.desc_false:0 "The inquiry is complete, and the implant was wrong. There was no plot. Nothing [eotg_conspirator.GetFirstName] did could have been read as one by anyone but the implant. The cleared logs are on file, and the record is not kind to your judgment."
  ```
- **Why it's wrong:** If the ruler chose `.017.d` (`"Execute them."`), `scope:eotg_conspirator` was executed and is dead (`killer = root`). In `.018`, if the plot was false (`scope:eotg_plot_truth = flag:false`), the event falls back to `desc_false`. The right portrait displays the character as dead, yet the text talks about them as if they are simply cleared of wrongdoing (`"Nothing [eotg_conspirator.GetFirstName] did could have been read as one..."`), completely omitting the fact that an innocent person was executed. In contrast, `eotg_fracture.020` properly provides a dedicated `desc_false_executed` variant.
- **Suggested fix:** Add a `triggered_desc` in `eotg_aug_tier3.018`:
  ```pdx
  triggered_desc = {
      trigger = {
          scope:eotg_plot_action = flag:executed
          scope:eotg_plot_truth = flag:false
      }
      desc = eotg_aug_tier3.018.desc_false_executed
  }
  ```
  With loc acknowledging that the accused was wrongfully put to death.
- **Confidence:** High.

---

### MINOR Findings

#### GQA-004
- **Severity:** MINOR
- **Category:** 2 (Logic and state)
- **Location:** `common/scripted_effects/eotg_augmentation_effects.txt:1006` (and lines 466, 1120)
- **Key / Context:** Scripted effect `eotg_aug_start_containment_regency_effect`.
- **Evidence:**
  `common/scripted_effects/eotg_augmentation_effects.txt:1006`:
  ```pdx
  add_character_flag = eotg_flag_aug_containment_regency
  ```
- **Why it's wrong:** The character flag `eotg_flag_aug_containment_regency` is set when initiating a containment regency, and is removed in `eotg_aug_total_integration_effect` and `eotg_aug_excision_effect`. However, `has_character_flag = eotg_flag_aug_containment_regency` is never checked anywhere in `events/`, `common/`, or `localization/`. It is completely dead state.
- **Suggested fix:** Either remove the redundant flag or check it in regency/diarchy triggers where containment status is evaluated.
- **Confidence:** High.

#### GQA-005
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:62`
- **Key / Context:** `eotg_mod_oc_learning_bonus_desc`.
- **Evidence:**
  ```yaml
  eotg_mod_oc_learning_bonus_desc:0 "Information floods in. Processing is flawless. Sleep is gone."
  ```
- **Why it's wrong:** The term `"flawless"` is on the explicitly banned words list in `docs/proposals/gemini_rewrite_feedback_2026-10-06.md` §3 ("invincible, unstoppable, flawless, living weapons..."). The setting insists on imperfect, strained technology rather than infallible perfection.
- **Suggested fix:** Replace with:
  ```yaml
  eotg_mod_oc_learning_bonus_desc:0 "Information floods in. Processing runs without pause. Sleep is gone."
  ```
- **Confidence:** High.

#### GQA-006
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:1814`
- **Key / Context:** `eotg_aug_proc.002.desc_upgrade`.
- **Evidence:**
  ```yaml
  eotg_aug_proc.002.desc_upgrade:0 "The upgraded component has been in place for some weeks now. A diagnostic scroll..."
  ```
- **Why it's wrong:** The term `"scroll"` is on the banned words list in §3 ("parchment, scroll, sheepskin, wax seal, signet ring, scribes" -> use "the contract, the documents, the record, archivists, the logs"). Hardware diagnostics in this setting produce readouts or records, not scrolls.
- **Suggested fix:** Replace `"A diagnostic scroll"` with `"A diagnostic readout"`:
  ```yaml
  eotg_aug_proc.002.desc_upgrade:0 "The upgraded component has been in place for some weeks now. A diagnostic readout confirms the leads settled into tolerance."
  ```
- **Confidence:** High.

#### GQA-007
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:537`
- **Key / Context:** `eotg_fracture.010.desc`.
- **Evidence:**
  ```yaml
  eotg_fracture.010.desc:0 "Your implant's overlay renders what it expects the mirror to show. This morning..."
  ```
- **Why it's wrong:** Contains the banned time-of-day word `"morning"`. Planetary/space stations operate on shifts/watches rather than universal planetary mornings (§3, work queue W5).
- **Suggested fix:** Replace `"This morning"` with `"This watch"`, `"On this shift"`, or `"Today"`.
- **Confidence:** High.

#### GQA-008
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:714`
- **Key / Context:** `eotg_fracture.026.desc_voice4`.
- **Evidence:**
  ```yaml
  eotg_fracture.026.desc_voice4:0 "\n\nThe access you granted is idle, not revoked. You can read the queue. By morning..."
  ```
- **Why it's wrong:** Contains `"By morning"`, which is on the banned time-of-day phrases list in §3.
- **Suggested fix:** Replace `"By morning"` with `"By the next watch"` or `"Before the next shift"`.
- **Confidence:** High.

#### GQA-009
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:1281`
- **Key / Context:** `eotg_aug_tier3.013.desc`.
- **Evidence:**
  ```yaml
  eotg_aug_tier3.013.desc:0 "[eotg_finder.GetFirstName] found you in the lower corridor before dawn..."
  ```
- **Why it's wrong:** Contains `"dawn"`, which is banned under §3 and work queue W5.
- **Suggested fix:** Replace `"before dawn"` with `"before the cycle change"` or `"in the quiet hours"`.
- **Confidence:** High.

#### GQA-010
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:756`
- **Key / Context:** `eotg_aug_heir.001.e`.
- **Evidence:**
  ```yaml
  eotg_aug_heir.001.e:0 "[eotg_heir.GetSheHe|U] wants the throne."
  ```
- **Why it's wrong:** Uses the medieval term `"throne"`. The mod setting rule prohibits medieval vocabulary like castle, throne room, throne (§3).
- **Suggested fix:** Replace with `"[eotg_heir.GetSheHe|U] wants the seat."` or `"[eotg_heir.GetSheHe|U] wants the realm."`
- **Confidence:** High.

#### GQA-011
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:1437`
- **Key / Context:** `eotg_aug_countdown.003.desc`.
- **Evidence:**
  ```yaml
  eotg_aug_countdown.003.desc:0 "There are two versions of last night's dinner, and both are vivid..."
  ```
- **Why it's wrong:** Uses `"last night"`. Time-of-day references are banned under §3 / W5.
- **Suggested fix:** Replace `"last night's dinner"` with `"the prior watch's meal"` or `"yesterday's meal"`.
- **Confidence:** High.

#### GQA-012
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:433`
- **Key / Context:** `eotg_aug_init.015.desc`.
- **Evidence:**
  ```yaml
  eotg_aug_init.015.desc:0 "The fever broke. The child eats, sleeps, laughs. And at night, when the house sleeps..."
  ```
- **Why it's wrong:** Uses `"at night"`. Banned under §3 / W5.
- **Suggested fix:** Replace `"And at night, when the house sleeps"` with `"And when the quarters go dark"` or `"And during the dark cycles"`.
- **Confidence:** High.

#### GQA-013
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:973`
- **Key / Context:** `eotg_aug_tier1.011.e`.
- **Evidence:**
  ```yaml
  eotg_aug_tier1.011.e:0 "Make it the evening's entertainment."
  ```
- **Why it's wrong:** Uses `"evening"`. Banned under §3 / W5.
- **Suggested fix:** Replace with `"Make it the gathering's entertainment."` or `"Make it our entertainment."`
- **Confidence:** High.

#### GQA-014
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:1701`
- **Key / Context:** `eotg_aug_tier2.004.b.success`.
- **Evidence:**
  ```yaml
  eotg_aug_tier2.004.b.success:0 "[eotg_aug_spouse.GetSheHe|U] wants to believe you, and for tonight [eotg_aug_spouse.GetSheHe] lets it rest."
  ```
- **Why it's wrong:** Uses `"tonight"`. Banned under §3 / W5.
- **Suggested fix:** Replace with `"...and for now [eotg_aug_spouse.GetSheHe] lets it rest."`
- **Confidence:** High.

#### GQA-015
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:807`
- **Key / Context:** `eotg_aug_end.001.b`.
- **Evidence:**
  ```yaml
  eotg_aug_end.001.b:0 "Not today."
  ```
- **Why it's wrong:** Uses `"today"`. Banned under §3 / W5.
- **Suggested fix:** Replace with `"Not now."` or `"Not yet."`
- **Confidence:** High.

#### GQA-016
- **Severity:** MINOR
- **Category:** 5 (Lore and voice)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:1418`
- **Key / Context:** `eotg_aug_countdown.001.desc`.
- **Evidence:**
  ```yaml
  eotg_aug_countdown.001.desc:0 "Clocks run wrong. A cup leaves your hand and you watch it fall..."
  ```
- **Why it's wrong:** Uses `"Clocks run wrong"` and `"today"`. Clockwork vocabulary is banned under §3.
- **Suggested fix:** Replace `"Clocks run wrong"` with `"Chronometers drift"` or `"Timers slip"`.
- **Confidence:** High.

---

### NOTE Findings

#### GQA-017
- **Severity:** NOTE
- **Category:** 3 (Reachability and pacing)
- **Location:** `events/eotg_augmentation_procedures.txt:706-750`
- **Key / Context:** Event `eotg_aug_proc.004` (A Part Replaced).
- **Evidence:**
  `events/eotg_augmentation_procedures.txt:706-713`:
  ```pdx
  # A Part Replaced (lore N1). The Seamless repair: no roll, no gold, no risk
  # (risk is a no-op at Seamless by design).
  ```
- **Why it's wrong:** Invariant 5 requires flavor events to read or move the system's signature resource (`eotg_fracture_risk`). This event does not touch risk, but it is explicitly specced as the Seamless (Total Integration) repair notification where risk is permanently disabled and residue is read in `desc_residue`. Conformance is verified as deliberate.
- **Suggested fix:** No change required; documented in code comments.
- **Confidence:** High.

#### GQA-018
- **Severity:** NOTE
- **Category:** 3 (Reachability and pacing)
- **Location:** `events/eotg_augmentation_procedures.txt:753-885`
- **Key / Context:** Event `eotg_aug_proc.020` (Phantom Static).
- **Evidence:**
  `events/eotg_augmentation_procedures.txt:792-796`:
  ```pdx
  trigger = {
      eotg_is_augmented_any = no
      has_variable = eotg_aug_former
  }
  ```
- **Why it's wrong:** Invariant 5 check flags `eotg_aug_proc.020` because it does not move or read `eotg_fracture_risk` on the root character. This is deliberate: root has left the cybernetics system (`eotg_is_augmented_any = no`), so they have no active fracture risk. Re-entry options (.c and .d) route into initiation.
- **Suggested fix:** No change required.
- **Confidence:** High.

---

## 2. Summary Table

| Severity | Count |
|---|---|
| BLOCKER | 0 |
| MAJOR | 3 |
| MINOR | 13 |
| NOTE | 2 |
| **Total** | **18** |

### Breakdown by Category

| Category | Description | Count |
|---|---|---|
| 1 | Text that lies / omission of outcomes | 3 |
| 2 | Logic and state | 1 |
| 3 | Reachability and pacing | 2 |
| 4 | Balance and player experience | 0 |
| 5 | Lore and voice (banned words, register) | 12 |
| 6 | Inconsistency across events | 0 |
| **Total** | | **18** |

---

## 3. Files Inspected

### Files Read in Full
- `events/eotg_augmentation_tamper.txt`
- `events/eotg_augmentation_procedures.txt`
- `events/eotg_augmentation_activities.txt`
- `events/eotg_augmentation_realm.txt`
- `events/eotg_augmentation_retinue.txt`
- `events/eotg_augmentation_patron.txt`
- `events/eotg_augmentation_countdown.txt`
- `events/eotg_augmentation_endgame.txt`
- `events/eotg_augmentation_heir.txt`
- `events/eotg_augmentation_nonruler.txt`
- `events/eotg_augmentation_tier1.txt`
- `events/eotg_augmentation_tier2.txt`
- `events/eotg_augmentation_tier3.txt`
- `events/eotg_augmentation_fracture.txt`
- `events/eotg_augmentation_initiation.txt`
- `common/character_interactions/eotg_augmentation_interactions.txt`
- `common/court_positions/types/eotg_augmentation_court_positions.txt`
- `common/deathreasons/eotg_augmentation_deaths.txt`
- `common/decisions/eotg_augmentation_decisions.txt`
- `common/law_groups/eotg_augmentation_law_groups.txt`
- `common/laws/eotg_augmentation_laws.txt`
- `common/modifiers/eotg_augmentation_modifiers.txt`
- `common/on_action/eotg_augmentation_on_actions.txt`
- `common/opinion_modifiers/eotg_augmentation_opinions.txt`
- `common/schemes/scheme_types/eotg_augmentation_schemes.txt`
- `common/scripted_character_templates/eotg_augmentation_templates.txt`
- `common/scripted_effects/eotg_augmentation_effects.txt`
- `common/scripted_triggers/eotg_augmentation_triggers.txt`
- `common/script_values/eotg_augmentation_values.txt`
- `common/story_cycles/eotg_augmentation_stories.txt`
- `common/traits/eotg_augmentation_traits.txt`
- `localization/english/eotg_augmentation_l_english.yml`

### Files Skimmed / Cross-Referenced
- `common/customizable_localization/eotg_aug_seller_names.txt`
- `localization/english/eotg_aug_seller_names_l_english.yml`
- `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/common/traits/00_traits.txt`
- `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/common/court_positions/types/00_court_positions.txt`
- `C:/Users/river/.claude/skills/ck3-modding/SKILL.md`

---

## 4. Checks Actually Performed

- [x] Full scan of `localization/english/eotg_augmentation_l_english.yml` against banned word lists (feedback §3, clockwork, medieval terms, time-of-day).
- [x] Check for singular "they/their/them" referring to single scoped characters across all cybernetics loc strings.
- [x] Scan for uncapitalized sentence-initial pronoun functions (`[x.GetSheHe]` without `|U`).
- [x] Verification of `[scope:` references in localization (0 found; all use bare scope syntax).
- [x] Check for `eotg_[ekdcb]_` title naming violations in all files (0 found in script/loc).
- [x] Cross-reference of scope saves in `events/` against scope references in `localization/` (verified across all non-excluded event files).
- [x] Audit of all `random_list` blocks in `events/` and `common/` for zero-weight risks (none found).
- [x] Variable and flag lifecycle check (set vs read) across all cybernetics scripts.
- [x] Signature resource audit (Invariant 5) across all non-hidden cybernetics events.
- [x] Engine vocabulary check via `docs/tools/px_vocab_check.py`.
- [x] Linter rules execution via `docs/tools/eotg_lint.py`.
- [x] Mechanical localization audit via `docs/tools/qa/loc_mechanical.py`.
- [x] Event graph reachability analysis via `docs/tools/qa/event_graph.py`.
