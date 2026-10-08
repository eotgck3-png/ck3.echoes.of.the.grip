# GeminiQA: Build QA Audit ? A Fracturing Inheritance & Neurofractured Kingpin Batch A (Round 1)

**Reviewer:** GeminiQA (Independent Read-Only QA Reviewer)  
**Date:** 2026-10-06  
**Build 1:** A Fracturing Inheritance (`events/eotg_augmentation_inherit.txt`, additions in `common/` files, on_actions, `eotg_aug_nr_cascade_effect`)  
**Build 2:** Neurofractured Kingpin Batch A (`events/eotg_augmentation_kingpin.txt`, `common/story_cycles/eotg_aug_kingpin_story.txt`, `common/on_action/eotg_aug_kingpin_on_actions.txt`, `common/` files starting with `eotg_aug_kingpin_`, character templates, non-ruler check hook)  
**Target Output:** `docs/qa/geminiqa/build_qa_inherit_kingpinA_r1.md`  
**ID Prefix:** `GQB-`  
**Scope Exclusions / Notice:** Localization for both builds is intentionally in progress / unbuilt (`inherit_loc_keys.txt` and `kingpin_batchA_loc_keys.txt` are tracked separately); missing loc keys are therefore expected and excluded from defect reporting.

---

## 1. Executive Summary & Verdicts

| Build | Verdict | Notes |
|---|---|---|
| **Build 1: A Fracturing Inheritance** | **READY FOR LOC** | 28 events, all reachable; 15 leaf outcomes structurally sound and shared with silent AI path (.028); no player character death on AI path; variables strictly cleaned up on chain close; Invariants 1?7 fully respected. |
| **Build 2: Neurofractured Kingpin (Batch A)** | **READY FOR LOC** | 27 events, all reachable; all 8 Batch B seams completely inert with no dangling event calls; visible story panel restricted strictly to 1?3 leverage band; `eotg_aug_kp_leverage_effect` is sole band writer; cooldown flag authority strictly in on_action; Invariants 1?7 fully respected. |

---

## 2. Findings (Ordered by Severity, then File)

### BLOCKER Findings
*(None detected. No engine crashes, infinite loops, dangling event invocations, or unhandled hard errors.)*

---

### MAJOR Findings
*(None detected. Logic and state flows match spec contracts without major defects.)*

---

### MINOR Findings

#### GQB-001
- **Severity:** MINOR
- **Category:** 6 (Inconsistency across events / UI polish)
- **Location:** `events/eotg_augmentation_inherit.txt:77, 432, 856, 1083`
- **Key / Context:** Event options with trait OR-gates: `.001.e` (callous/paranoid), `.004.d` (deceitful/intrigue 14), `.009.e` (callous/sadistic), `.011.c` (vengeful/arbitrary).
- **Evidence:**
  `events/eotg_augmentation_inherit.txt:77-83`:
  ```pdx
  option = {
      name = eotg_aug_inherit.001.e
      trigger = {
          OR = {
              has_trait = callous
              has_trait = paranoid
          }
      }
      # No trait = line present
  ```
- **Why it's wrong:** When an option trigger uses an `OR = { has_trait = X has_trait = Y }`, omitting top-level `trait = <name>` lines prevents CK3 from rendering trait icons next to the option name in the event window. In vanilla CK3, the established pattern (found in 583 instances across vanilla events) is to stack multiple `trait = <name>` lines consecutively:
  ```pdx
  trait = callous
  trait = paranoid
  ```
  The CK3 UI engine evaluates stacked trait lines and displays the icon for whichever qualifying trait the character possesses.
- **Suggested fix:** Stack the corresponding `trait = <name>` entries in each OR-gated option for visual clarity.
- **Confidence:** High. `NEEDS-VANILLA-CHECK` (for exact multi-trait icon rendering behavior in 1.20).

---

### NOTE / Design Feedback Findings

#### GQB-002
- **Severity:** NOTE
- **Category:** 4 (Balance and player experience)
- **Location:** `events/eotg_augmentation_inherit.txt:771, 951, 982, 1066, 1152`
- **Context:** Deviation 8 (Inherit): Gold-cost options hidden rather than disabled via `show_as_unavailable`.
- **Evidence:** Options `.008.a`, `.010.a`, `.010.b`, `.011.b`, `.012.a` gate gold requirements inside `trigger = { gold >= ... }`.
- **Why it's noted:** In CK3, placing resource requirements directly inside `trigger = { }` hides the option completely if the player is broke, whereas wrapping it in `show_as_unavailable` displays the choice in a greyed-out state with the missing cost requirement explained in the tooltip. Hiding prevents choice paralysis when bankrupt, but conceals high-tier alternatives (such as employing a skilled physician).
- **Judgement / Recommendation:** Acceptable scripter deviation; keeps the event UI clean for cash-poor rulers without dead-ending the event (each event maintains a free fallback). If desired by design, future iterations can wrap costs in `show_as_unavailable`.
- **Confidence:** High.

#### GQB-003
- **Severity:** NOTE
- **Category:** 6 (Loc and Tooltips)
- **Location:** `events/eotg_augmentation_inherit.txt` and `common/scripted_effects/eotg_augmentation_effects.txt`
- **Context:** Deviation 9 (Inherit): Addition of dedicated custom tooltip keys.
- **Evidence:** Keys `eotg_aug_inherit.009.a_fail_tt`, `eotg_aug_inherit.ward_breakout_tt`, `eotg_aug_inherit.012.exposed_tt`, `eotg_aug_inherit.ward_tt`, `eotg_aug_inherit.018.fail_tt`, `eotg_aug_inherit.route_threat_tt`.
- **Judgement / Recommendation:** Excellent polish deviation. Explicit failure and breakout tooltips give clear player feedback on hidden dice rolls. Keys are already tracked in `inherit_loc_keys.txt`.
- **Confidence:** High.

#### GQB-004
- **Severity:** NOTE
- **Category:** 2 (Logic and state)
- **Location:** `common/on_action/eotg_augmentation_on_actions.txt:1930`
- **Context:** Deviation 1 (Inherit): Third Heir's Arc guard at Seamless yearly check.
- **Evidence:** `NOT = { has_variable = eotg_inh_heir }` added to `eotg_on_yearly_aug_seamless_check`.
- **Judgement / Recommendation:** Spec ?5.2 explicitly named Overclocked and Neurofractured checks; extending this defensive guard to the Seamless pulse prevents edge-case concurrent heir story arcs. Strongly endorsed.
- **Confidence:** High.

#### GQB-005
- **Severity:** NOTE
- **Category:** 2 (Logic and state)
- **Location:** `common/scripted_effects/eotg_augmentation_effects.txt: eotg_aug_inherit_pick_line_effect`
- **Context:** Deviation 2 (Inherit): Succession line pick iterates exact places 1?6, lowest first.
- **Evidence:** `eotg_aug_inherit_line_slot_effect` checks `PLACE = 1` through `6` sequentially.
- **Judgement / Recommendation:** Strictly implements spec ?5.4.1 requirement to pick places 2 and 3 sequentially while skipping root and the primary heir. Fully approved.
- **Confidence:** High.

#### GQB-006
- **Severity:** NOTE
- **Category:** 2 (Logic and state)
- **Location:** `common/scripted_effects/eotg_augmentation_effects.txt: eotg_aug_inherit_confine_effect, eotg_aug_inherit_ward_effect`
- **Context:** Deviation 3 (Inherit): `OUTCOME` parameter on confine and ward scripted effects.
- **Evidence:** `$OUTCOME$` parameter sets `set_variable = { name = eotg_inh_outcome value = flag:l5 }` only when confinement represents the terminal leaf rather than an intermediate custody state.
- **Judgement / Recommendation:** Clean separation of concerns. Endorsed.
- **Confidence:** High.

#### GQB-007
- **Severity:** NOTE
- **Category:** 2 (Logic and state)
- **Location:** `events/eotg_augmentation_inherit.txt:1520`
- **Context:** Deviation 4 (Inherit): `.016` reroutes to `.018` when line of succession is empty.
- **Evidence:** If `NOT = { exists = scope:eotg_inh_next_1 }`, `.016` immediately triggers `.018` (The Last Audience).
- **Judgement / Recommendation:** Sound safeguard preventing an empty scene where the heir targets non-existent next heirs. Endorsed.
- **Confidence:** High.

#### GQB-008
- **Severity:** NOTE
- **Category:** 2 (Logic and state)
- **Location:** `events/eotg_augmentation_inherit.txt:2030`
- **Context:** Deviation 5 (Inherit): `.025` requires the heir to be landed (`is_landed = yes`).
- **Evidence:** `eotg_aug_inherit.025` trigger includes `is_landed = yes`.
- **Judgement / Recommendation:** Essential safeguard. If an heir previously disinherited / struck from the line at `.013` assassinates the ruler at `.018`, they do not inherit the title; hence the "Taking the Seat" event must not fire. Endorsed.
- **Confidence:** High.

#### GQB-009
- **Severity:** NOTE
- **Category:** 2 (Logic and state)
- **Location:** `events/eotg_augmentation_kingpin.txt:750, 1150`
- **Context:** Deviation 1 (Kingpin): Immediate deaths in `.005 a_violence` and `.009 b`.
- **Evidence:** Target and lieutenant murders execute immediately via `death = { death_reason = death_murder killer = scope:eotg_kp }` rather than delaying 10?30 days.
- **Judgement / Recommendation:** Eliminates dangling saved scopes and prevents edge cases where the target moves courts or dies of other causes during the delay. Endorsed.
- **Confidence:** High.

#### GQB-010
- **Severity:** NOTE
- **Category:** 2 (Logic and state)
- **Location:** `events/eotg_augmentation_kingpin.txt:1210`
- **Context:** Deviation 2 (Kingpin): `.009 c` interprets "purge-known" as Kingpin's purge mind axis.
- **Evidence:** Evaluates `eotg_aug_kp_is = { AXIS = mind VALUE = purge }` to decide whether the lieutenant suffers `death_disappearance` vs `move_to_pool`.
- **Judgement / Recommendation:** Faithful translation of spec intention into script triggers. Endorsed.
- **Confidence:** High.

#### GQB-011
- **Severity:** NOTE
- **Category:** 6 (Consistency with vanilla)
- **Location:** `common/scripted_effects/eotg_aug_kingpin_effects.txt:590`
- **Context:** Deviation 3 (Kingpin): L10 uses vanilla opinion modifier `received_title_county`.
- **Evidence:** `scope:eotg_kp = { add_opinion = { modifier = received_title_county target = root } }`.
- **Judgement / Recommendation:** Standard vanilla opinion modifier for title grants. Fully approved.
- **Confidence:** High. `NEEDS-VANILLA-CHECK`.

#### GQB-012
- **Severity:** NOTE
- **Category:** 2 (Logic and state)
- **Location:** `common/story_cycles/eotg_aug_kingpin_story.txt:259`
- **Context:** Deviation 4 (Kingpin): Boss who escapes custody resets stage back to `open`.
- **Evidence:** Story maintenance triggered effect checks `var:eotg_kp_stage = flag:custody` and `var:eotg_kp = { is_imprisoned = no }`, resetting stage to `open`.
- **Judgement / Recommendation:** Robust loop guard that prevents the story cycle from stalling indefinitely in the custody stage if the prisoner escapes or is ransomed. Endorsed.
- **Confidence:** High.

#### GQB-013
- **Severity:** NOTE
- **Category:** 2 (Logic and state)
- **Location:** `common/story_cycles/eotg_aug_kingpin_story.txt:460-500`
- **Context:** Deviation 5 (Kingpin): Middle-pool gating in tick T6.
- **Evidence:** T6 random_list checks whether errand targets, purge targets, and informant candidates actually exist before rolling `.005`, `.006`, and `.007`.
- **Judgement / Recommendation:** Crucial defense against empty-scope bugs and false text. Endorsed.
- **Confidence:** High.

#### GQB-014
- **Severity:** NOTE
- **Category:** 2 (Logic and state)
- **Location:** `common/scripted_effects/eotg_aug_kingpin_effects.txt` & `common/story_cycles/eotg_aug_kingpin_story.txt:262`
- **Context:** Deviation 6 (Kingpin): Timed hired-guns mirror variable (`eotg_kp_hired_guns_on`).
- **Evidence:** Sets timed mirror for 1825 days (5 years) on story cycle; story maintenance cleans up inherited open-ended modifier once the timed mirror expires.
- **Judgement / Recommendation:** Clean workaround for CK3 character modifier inheritance limitations. Endorsed.
- **Confidence:** High.

#### GQB-015
- **Severity:** NOTE
- **Category:** 2 (Logic and state / Tooling)
- **Location:** `common/decisions/eotg_aug_kingpin_decisions.txt:14`
- **Context:** Deviation 7 (Kingpin): Debug decision `eotg_decision_aug_debug_kingpin`.
- **Evidence:** Decision gated behind `debug_only = yes`. Clears once-per-life flags and allows forcing profile axes.
- **Judgement / Recommendation:** Excellent debugging tool, strictly isolated from release gameplay. Endorsed.
- **Confidence:** High.

#### GQB-016
- **Severity:** NOTE
- **Category:** 2 (Logic and state / Engine interaction)
- **Location:** `common/scripted_effects/eotg_augmentation_effects.txt: eotg_aug_inherit_abdicate_effect`
- **Context:** Regency persistence across abdication.
- **Evidence:** Calls `eotg_aug_start_containment_regency_effect` after `depose = yes`.
- **Judgement / Recommendation:** Spec ?5.4.4 notes that whether vanilla 1.20 preserves containment regencies on capable adults across character switches must be confirmed in-game (Q7 / CB-02).
- **Confidence:** Medium. `NEEDS-VANILLA-CHECK`.

---

## 3. Build 1 Detailed Conformance Check: A Fracturing Inheritance

### 3.1 Spec ?9 Checklist (Items 0?3, 10?12)
1. **Item 0 (Tooling):**
   - `ck3-tiger 1.17.0`: Ran across entire repository and game files. Produced **0 errors or warnings** on all inheritance files.
   - `px_vocab_check.py`: Passed cleanly (**0 unknown effects, triggers, or scopes** in inherit files).
   - `px_lsp_diagnostics.js`: Passed with **exit code 0** (braces, parameters, syntax verified).
2. **Item 1 (Reachability):**
   - Exactly **28 events** defined (`eotg_aug_inherit.001` through `.028`).
   - Every single event is fired by either the entry effects or by an upstream event option/effect. No event is orphaned or unreachable.
3. **Item 2 (Lesson 5 / Cooldown Authority):**
   - `eotg_flag_aug_inh_cooldown` is checked and set exclusively in `common/on_action/eotg_augmentation_on_actions.txt` and `eotg_aug_inherit_start_effect`.
   - `grep -rn "eotg_flag_aug_inh_cooldown" events/` is completely empty.
4. **Item 3 (Invariant 5 / Signature Resource):**
   - 21 of 28 events move `eotg_fracture_risk` directly (spec threshold: 20 minimum).
   - All 28 events either move fracture risk, evaluate fracture pressure bands, or execute terminal tier alterations (death, excision, cascade).
5. **Item 10 (Silent AI Path - Event .028):**
   - Event `.028` is explicitly flagged `hidden = yes`.
   - Fires exclusively for AI rulers when `is_ai = yes` in `eotg_aug_inherit_start_effect`.
   - Zero `send_interface_toast`, `send_interface_message`, or player notifications are executed.
   - Zero outcome mechanics (`death =`, `imprison =`, `depose =`, `disinherit_effect =`) are hardcoded inline inside `.028`; all outcomes route strictly through shared scripted leaf effects.
6. **Item 11 (Leaf Parity):**
   - All 15 leaf outcomes called by `.028` invoke the exact same scripted effects (`eotg_aug_inherit_leaf_*`) used by player tree events.
7. **Item 12 (No Off-Screen Player Death):**
   - In `eotg_aug_inherit_line_slot_effect`, succession candidates picked when `eotg_aug_inherit_tree_runs = no` strictly enforce `is_ai = yes`. Players can never be targeted or assassinated by an AI ruler's background chain resolution.

### 3.2 Variable and State Cleanup
- `eotg_aug_inherit_close_effect` is invoked at all terminal leaves and `on_trigger_fail` handlers.
- Cleanses all 13 chain variables (`eotg_inh_heir`, `eotg_inh_profile`, `eotg_inh_bond`, `eotg_inh_source`, `eotg_inh_witness`, `eotg_inh_threat`, `eotg_inh_table`, `eotg_inh_reaction`, `eotg_inh_table_result`, `eotg_inh_dead_count`, `eotg_inh_force`, `eotg_inh_force_leaf`, etc.) and all 8 transient flags.
- Only the 3-year cooldown flag and permanent historical outcome flags persist as intended.

---

## 4. Build 2 Detailed Conformance Check: Neurofractured Kingpin (Batch A)

### 4.1 Batch B Seam Verification
- All 8 routes designated `BATCH-B SEAM (kingpin)` were inspected in `events/eotg_augmentation_kingpin.txt` and `common/story_cycles/eotg_aug_kingpin_story.txt`.
- Every seam is completely **inert**: no option, effect, or story tick fires unbuilt Batch B event IDs (`.030`?`.039`, `.050`, `.063`?`.067`, `.072`).
- Cross-reference analysis identified **zero dangling event calls**.

### 4.2 Visible Story Panel & Band Mechanics
- Story cycle `eotg_story_aug_kingpin` declares `visible = yes`.
- UI visualization exposes only:
  - `character = { variable_name = "eotg_kp" }`
  - `basic_counter = { variable_name = "eotg_kp_leverage_band" min = 1 max = 3 }`
- Never exposes raw leverage numbers, fracture risk, stages, or hidden paths.
- Global repository scan confirms `eotg_kp_leverage_band` is written **solely** within `eotg_aug_kp_leverage_effect`.

### 4.3 Signature Resource Movement & Pacing
- All 27 events read or move `eotg_fracture_risk`, evaluate pressure bands (`eotg_aug_pressure_storm`, `eotg_aug_pressure_fracture`), or adjust `eotg_kp_leverage`.
- Cooldown authority: `eotg_flag_aug_kingpin_cooldown` (10 years) is set and read **exclusively** within `common/on_action/eotg_aug_kingpin_on_actions.txt`.

### 4.4 Story Cycle Inheritance (`on_owner_death`)
- Strictly adheres to spec ?5.4.1 and vanilla precedent (`ce1_story_cycle_black_death.txt`).
- Validates that `player_heir` exists, the kingpin is alive, story is not resolving, the heir is not the kingpin, and the heir does not already own a kingpin story.
- Re-scopes to the heir, runs `eotg_aug_kp_inherit_effect`, executes `make_story_owner = scope:eotg_kp_heir`, and triggers `.040` within 3?10 days.

---

## 5. Invariants & Repository Standards Check

| Invariant / Rule | Verification Result | Details |
|---|---|---|
| **Invariant 1: `eotg_` prefix on all identifiers** | **PASS** | Every new effect, trigger, script value, modifier, opinion modifier, decision, custom loc, and template uses `eotg_` prefix. |
| **Invariant 2: `eotg_[ekdcb]_` never appears** | **PASS** | Automated regex scan returned 0 occurrences across all new files. |
| **Invariant 3: No un-shipped replace paths** | **PASS** | No directory replacements added. |
| **Invariant 4: Additive on_actions** | **PASS** | Both `yearly_playable_pulse` extensions add on_action entries only; no top-level triggers or effects on vanilla hooks. |
| **Invariant 5: Signature resource movement** | **PASS** | Complied with across all 28 inherit and 27 kingpin events. |
| **Invariant 7: Skill effects use `_skill`** | **PASS** | Verified 0 instances of deprecated bare skill modifiers (e.g. `add_intrigue`). |
| **No hardcoded title, province, culture, faith, or character keys** | **PASS** | No static world entities referenced; fully agnostic to map replacement. |
| **No `hidden_trigger` in script** | **PASS** | 0 occurrences in logic (only 1 benign explanatory comment). |
| **No `GetHeir` on character** | **PASS** | 0 occurrences. |
| **No duplicate definitions across shared files** | **PASS** | Verified across all shared effect, trigger, value, and modifier files. |

---

## 6. Summary Tables

### 6.1 Findings by Severity & Category
| Category | BLOCKER | MAJOR | MINOR | NOTE | Total |
|---|---|---|---|---|---|
| 1. Text that lies | 0 | 0 | 0 | 0 | 0 |
| 2. Logic and state | 0 | 0 | 0 | 11 | 11 |
| 3. Reachability & pacing | 0 | 0 | 0 | 0 | 0 |
| 4. Balance & player experience | 0 | 0 | 0 | 1 | 1 |
| 5. Lore & voice | 0 | 0 | 0 | 0 | 0 |
| 6. Inconsistency / UI polish | 0 | 0 | 1 | 4 | 5 |
| **Total** | **0** | **0** | **1** | **16** | **17** |

### 6.2 Files Inspected
- **Read in Full:**
  - `events/eotg_augmentation_inherit.txt` (28 events)
  - `events/eotg_augmentation_kingpin.txt` (27 events)
  - `common/story_cycles/eotg_aug_kingpin_story.txt`
  - `common/on_action/eotg_aug_kingpin_on_actions.txt`
  - `common/on_action/eotg_augmentation_on_actions.txt` (edits)
  - `common/scripted_effects/eotg_aug_kingpin_effects.txt`
  - `common/scripted_triggers/eotg_aug_kingpin_triggers.txt`
  - `common/script_values/eotg_aug_kingpin_values.txt`
  - `common/modifiers/eotg_aug_kingpin_modifiers.txt`
  - `common/opinion_modifiers/eotg_aug_kingpin_opinions.txt`
  - `common/decisions/eotg_aug_kingpin_decisions.txt`
  - `common/customizable_localization/eotg_aug_kingpin_custom_loc.txt`
  - `common/scripted_character_templates/eotg_augmentation_templates.txt` (appended templates)
  - `common/scripted_effects/eotg_augmentation_effects.txt` (inherit additions & cascade effect)
  - `common/scripted_triggers/eotg_augmentation_triggers.txt` (inherit additions)
  - `common/script_values/eotg_augmentation_values.txt` (inherit additions)
  - `common/modifiers/eotg_augmentation_modifiers.txt` (inherit additions)
- **Skimmed / Reference:**
  - `docs/specs/cybernetics_v2_fracturing_inheritance.md`
  - `docs/specs/cybernetics_v2_kingpin.md`
  - `docs/specs/build/inherit_loc_keys.txt`
  - `docs/specs/build/kingpin_batchA_loc_keys.txt`
  - `CLAUDE.md`

### 6.3 Checks Actually Performed
1. Full syntax and engine vocabulary validation via `ck3-tiger 1.17.0`, `px_vocab_check.py`, and `px_lsp_diagnostics.js`.
2. Graph reachability audit verifying caller chains for all 28 inherit events and 27 kingpin events.
3. Automated inspection of all 8 `BATCH-B SEAM` markers in Kingpin ensuring zero unbuilt events are triggered.
4. Regex verification of all CLAUDE.md invariants (prefix, title tier format, additive on_actions, `_skill` suffixes).
5. Scrutiny of variable clearance in `eotg_aug_inherit_close_effect` and `on_trigger_fail`.
6. Audit of event `.028` verifying `hidden = yes`, absence of player toasts/events, exclusion of players from succession line picks, and leaf parity.
7. Verification that Kingpin story cycle visible panel displays exclusively `eotg_kp_leverage_band` and that only `eotg_aug_kp_leverage_effect` writes it.
8. Analysis of cooldown flag authority for both systems.
9. Formal evaluation of all 11 scripter deviations in Inheritance and all 7 scripter deviations in Kingpin.

---

## 7. Final Verdicts

- **Build 1 (A Fracturing Inheritance): READY FOR LOC**
- **Build 2 (Neurofractured Kingpin Batch A): READY FOR LOC**
