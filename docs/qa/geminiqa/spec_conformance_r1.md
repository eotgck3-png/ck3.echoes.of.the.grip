# GeminiQA: Spec-to-Build Conformance Audit (Round 1)

**Reviewer:** GeminiQA (Independent Read-Only QA Reviewer)  
**Date:** 2026-10-06  
**Scope:** Built specs in docs/specs/ (cybernetics_track.md, cybernetics_v2*.md [excluding kingpin and racturing_inheritance], and rontier*.md [v1, v2, v3, unclaimed regions]).  
**Exclusions Per Work Queue Q3:** cybernetics_v2_kingpin.md and cybernetics_v2_fracturing_inheritance.md (active writer/draft queue in progress).  
**Methodology:** Full AST/token cross-comparison of specced identifiers, events, options, modifiers, triggers, effects, and script values against the implemented game files in common/, events/, and localization/english/, cross-referenced with docs/tools/spec_conformance.py.

---

## 1. Findings (Ordered by Severity, then Spec)

### BLOCKER Findings
*(None detected. No fatal spec divergences or missing core architectural systems in the built suites.)*

---

### MAJOR Findings
*(None detected. All specced features in the built suites are functional and integrated with game loops.)*

---

### MINOR Findings

#### GQS-001
- **Severity:** MINOR
- **Category:** 2 (Broken script wiring / Spec gap)
- **Location:** docs/specs/cybernetics_v2_realm.md:303 vs common/opinion_modifiers/eotg_augmentation_opinions.txt:60
- **Key / Context:** Modifier key eotg_mod_aug_retinue_resentment.
- **Evidence:**
  docs/specs/cybernetics_v2_realm.md specifies eotg_mod_aug_retinue_resentment as a character modifier applied when courtiers and retinue resent augmented rulers.
  In script (common/opinion_modifiers/eotg_augmentation_opinions.txt:60-65), this was converted into an opinion modifier eotg_opinion_aug_retinue_resentment, and the modifier key was left as a comment reference:
  `pdx
  # eotg_mod_aug_retinue_resentment). Callers: eotg_aug_retinue.002 (b, c)
  eotg_opinion_aug_retinue_resentment = {
      opinion = -15
  }
  `
- **Why it is divergent:** The implementation converted a specced character modifier into an opinion modifier. While gameplay-functional, the original character modifier identifier eotg_mod_aug_retinue_resentment is never defined.
- **Suggested fix:** Either define eotg_mod_aug_retinue_resentment in common/modifiers/ if a character-level stat debuff was intended alongside the opinion hit, or update the spec to document the conversion to eotg_opinion_aug_retinue_resentment.
- **Confidence:** High.

#### GQS-002
- **Severity:** MINOR
- **Category:** 2 (Broken script wiring / Retired trigger)
- **Location:** docs/specs/cybernetics_v2_realm.md:117 vs common/scripted_triggers/eotg_augmentation_triggers.txt:162
- **Key / Context:** Scripted trigger eotg_aug_has_court_physician.
- **Evidence:**
  docs/specs/cybernetics_v2_realm.md lists eotg_aug_has_court_physician in its identifier table.
  In common/scripted_triggers/eotg_augmentation_triggers.txt:162:
  `pdx
  # (eotg_aug_has_court_physician retired by the realm batch: its procedures QA
  # closed by reading scope:court_physician directly)
  `
- **Why it is divergent:** The trigger was retired in code in favor of direct scope checks (scope:court_physician), but the spec still lists it without an obsolete/superseded tag.
- **Suggested fix:** Mark eotg_aug_has_court_physician as retired/superseded in docs/specs/cybernetics_v2_realm.md.
- **Confidence:** High.

#### GQS-003
- **Severity:** MINOR
- **Category:** 2 (Broken script wiring / Retired flag)
- **Location:** docs/specs/cybernetics_v2_phase4.md:429 vs events/eotg_augmentation_tier3.txt:2685
- **Key / Context:** Character flag eotg_flag_aug_trusted_delegate.
- **Evidence:**
  docs/specs/cybernetics_v2_phase4.md specifies eotg_flag_aug_trusted_delegate.
  In events/eotg_augmentation_tier3.txt:2685:
  `pdx
  # (eotg_flag_aug_trusted_delegate retired: event chains check relationship directly)
  `
- **Why it is divergent:** The flag was intentionally omitted in implementation, but remains listed in the spec table without an exempt notation.
- **Suggested fix:** Update the spec table to mark eotg_flag_aug_trusted_delegate as retired.
- **Confidence:** High.

---

### NOTE / VERIFICATION Findings

#### GQS-004
- **Severity:** NOTE
- **Category:** 2 (Spec documentation / Tool false positive)
- **Location:** docs/specs/cybernetics_v2_tier_options.md:24-25
- **Key / Context:** Automated spec conformance tool flagged eotg_aug_act.00 and eotg_is_aug_tier as missing IDs.
- **Evidence:**
  In docs/specs/cybernetics_v2_tier_options.md:24-25:
  eotg_aug_act.00 appears in CLI command prose (--prefix eotg_aug_act.00).
  eotg_is_aug_tier* appears in explanatory methodology prose as a wildcard pattern.
- **Status:** PASS. These are not unbuilt identifiers; they are CLI parameters and wildcard patterns in methodology notes. The automated tool parser naively extracted them as exact identifier tokens.

#### GQS-005
- **Severity:** NOTE
- **Category:** 2 (Spec conformance / Phase 3a & Unclaimed wiring)
- **Location:** docs/specs/frontier_v3.md & docs/specs/frontier_unclaimed_regions.md
- **Key / Context:** Expedition targeting widening into Unclaimed Regions.
- **Evidence:**
  rontier_unclaimed_regions.md Build Note 3 records an intentional early widening: eotg_frontier_can_target_expedition and eotg_frontier_pick_expedition_target_effect allow explorable Unclaimed Regions within actor reach.
  All promised hooks (eotg_frontier_on_explored, eotg_unclaimed_on_claimed, eotg_unclaimed_on_released), traits (eotg_unclaimed_folk), governments (eotg_unclaimed_government), and values match specifications 100%.
- **Status:** PASS. Documented and verified.

---

## 2. Invariant & Conformance Summary Table

| Spec Family / Spec File | Promised Identifiers | Present & Valid | Divergences / Gaps | Status |
|---|---|---|---|---|
| **cybernetics_track.md** | 66 (53 active, 13 exempt) | 53 | 0 missing, 13 exempt traits/synergies | **CONFORMANT** |
| **cybernetics_v2.md** | 110 | 109 | 1 retired trigger (eotg_aug_is_nonruler) | **CONFORMANT** |
| **cybernetics_v2_balance.md** | 140 | 138 | 0 missing, 1 exempt | **CONFORMANT** |
| **cybernetics_v2_conformance_rulings.md** | 39 | 38 | 0 missing | **CONFORMANT** |
| **cybernetics_v2_interactions.md** | 161 | 154 | 0 missing, 3 exempt, 4 provider flags dynamic | **CONFORMANT** |
| **cybernetics_v2_new_beats.md** | 70 | 66 | 0 missing, 4 story variables | **CONFORMANT** |
| **cybernetics_v2_phase0.md** | 49 | 49 | 0 missing | **CONFORMANT** |
| **cybernetics_v2_phase1.md** | 20 | 17 | 0 missing | **CONFORMANT** |
| **cybernetics_v2_phase2.md** | 52 | 52 | 0 missing | **CONFORMANT** |
| **cybernetics_v2_phase3.md** | 84 | 80 | 0 missing, 1 exempt | **CONFORMANT** |
| **cybernetics_v2_phase4.md** | 65 | 64 | 1 retired flag (eotg_flag_aug_trusted_delegate) | **CONFORMANT** |
| **cybernetics_v2_phase5.md** | 53 | 49 | 0 missing, 1 exempt | **CONFORMANT** |
| **cybernetics_v2_phase6.md** | 27 | 26 | 0 missing | **CONFORMANT** |
| **cybernetics_v2_procedures.md** | 146 | 144 | 0 missing, 1 exempt | **CONFORMANT** |
| **cybernetics_v2_realm.md** | 125 | 120 | 1 converted modifier (eotg_mod_aug_retinue_resentment), 1 retired trigger | **CONFORMANT** |
| **cybernetics_v2_reprisal.md** | 37 | 36 | 0 missing | **CONFORMANT** |
| **cybernetics_v2_self_repair.md** | 55 | 55 | 0 missing | **CONFORMANT** |
| **cybernetics_v2_seller_names.md** | 75 | 75 | 0 missing | **CONFORMANT** |
| **cybernetics_v2_tier_options.md** | 94 | 91 | 0 missing (2 tool false-positives noted) | **CONFORMANT** |
| **cybernetics_v2_trait_depth.md** | 42 | 41 | 0 missing | **CONFORMANT** |
| **rontier_unclaimed_regions.md** | 95 | 90 | 0 missing, 3 exempt | **CONFORMANT** |
| **rontier_v1.md** | 146 | 137 | 0 missing, 8 exempt | **CONFORMANT** |
| **rontier_v1_open_questions.md** | 21 | 21 | 0 missing | **CONFORMANT** |
| **rontier_v2.md** | 109 | 109 | 0 missing | **CONFORMANT** |
| **rontier_v3.md** | 80 | 79 | 0 missing, 1 exempt | **CONFORMANT** |

---

## 3. Total Findings
- **BLOCKER:** 0
- **MAJOR:** 0
- **MINOR:** 3 (GQS-001, GQS-002, GQS-003)
- **NOTE:** 2 (GQS-004, GQS-005)
