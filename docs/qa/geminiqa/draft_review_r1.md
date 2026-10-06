# GeminiQA: Cross-Check of Writer Drafts (Round 1)

**Reviewer:** GeminiQA (Independent Read-Only QA Reviewer)  
**Date:** 2026-10-06  
**Target:** Writer Drafts W1 through W4:
- `docs/proposals/inherit_text_gemini_r1.md` & `inherit_text_gemini_r1_selfreview.md`
- `docs/proposals/kingpin_text_gemini_r1.md` & `kingpin_text_gemini_r1_selfreview.md`
**References:**
- `docs/specs/cybernetics_v2_fracturing_inheritance.md` §5.3, §7.1
- `docs/specs/cybernetics_v2_kingpin.md` §5.8, §7.1, £7.4
- `docs/proposals/kingpin_fragments_r1_apply_instructions.md`

---

## 1. Findings (Ordered by Severity, then File)

### BLOCKER Findings
*(None detected. No broken scope brackets, missing key blocks, or invalid syntax found in the draft files.)*

---

3## MAJOR Findings

#### GQD-001
- **Severity:** MAJOR
- **Category:** 8 (Style guide & banned words / LAW AT 866)
- **Location:** `docs/proposals/inherit_text_gemini_r1.md:328`
- **Key / Context:** Event `eotg_aug_inherit.025`, key `eotg_aug_inherit.025.desc_rage_cold`.
-* *Evidence:**
  `docs/proposals/inherit_text_gemina_r1.md:328`:
  ```yaml
  eotg_aug_inherit.025.desc_rage_cold:0 "The audience chamber is dead silent as you take [ROOT.Char.Custom('eotg_court_seat')]. The former ruler lies dead in the corridor behind you. The throne is yours now, bought with cold steel and shattered nerves."
  ```
- **Why it is wrong:** The word `throne` is explicitly and strictly banned across the entire mod (`docs/pitfalls.md`, `CLAUDE.md`, style rules). While the sentence starts by correctly using `[ROOT.Char.Custom('eotg_court_seat')]`, the third sentence introduces `The throne is yours now`, directly violating the banned vocabulary rule.
- **Suggested fix:** Replace `The throne is yours now` with `The seat is yours now`, `The command is yours now`, or `The rule is yours now`.
- **Confidence:** High.

---

### MINOR Findings

#### GQD-002
- **Severity:** MINOR
- **Category:** 8 (Style guide & banned words)
- **Location:** `docs/proposals/inherit_text_gemina_r1.md:70, 134`
- **Key / Context:** Event `eotg_aug_inherit.004` (`desc_rage`) and `eotg_aug_inherit.009` (`desc_kill_ruler`).
- **Evidence:**
  `docs/proposals/inherit_text_gemini_r1.md:70`:
  ```yaml
  eotg_aug_inherit.004.desc_rage:0 "The watch reports that [eotg_inh_heir.GetFirstName] spent the night pacing the maintenance tunnels beneath the residence..."
  ```
  `docs/proposals/inherit_text_gemini_r1.md:134`:
  ```yaml
  eotg_aug_inherit.009.desc_kill_ruler:0 "The warning signs are unmistakable. Sentry logs show [eotg_inh_heir.GetFirstName] studying the guard rotations around your private bedchamber, questioning sentries about night access codes..."
  ```
- **Why it is wrong:** The word `night` is a forbidden time-of-day word under EOTG setting rules. The universe of space stations, deep-space habitats, and asynchronous planetary orbits rejects Earth-centric diurnal cycles.
- **Suggested fix:**
  - In `.004.desc_rage`: replace `spent the night pacing` with `spent the off-cycle pacing` or `spent the late watch pacing`.
  - In `.009.desc_kill_ruler`: replace `night access codes` with `off-hours access codes` or `dark-cycle access codes`.
- **Confidence:** High.

#### GQD-003
- **Severity:** MINOR
- **Category:** 8 (Style guide & banned words)
- **Location:** `docs/proposals/kingpin_text_gemini_r1.md:379`
- **Key / Context:** Event `eotg_aug_kingpin.068`, key `eotg_aug_kingpin.068.desc_war`.
- **Evidence:**
  `docs/proposals/kingpin_text_gemini_r1.md:379`:
  ```yaml
  eotg_aug_kingpin.068.desc_war:0 "\\n\\nThe violence erupted across both the frontline encampments and the command staff, shattering the rebellion in a single bloody night."
  ```
- **Why it is wrong:** Forbidden diurnal time-of-day word `night`.
- **Suggested fix:** Replace `in a single bloody night` with `in a single bloody cycle` or `in a single bloody strike`.
- **Confidence:** High.

#### GQD-004
- **Severity:** MINOR
- **Category:** 8 (Style guide / Option length)
- **Location:** `docs/proposals/inherit_text_gemina_r1.md:154, 252` and `docs/proposals/kingpin_text_gemini_r1.md:95, 96, 126, 178`
- **Key / Context:** Overly terse 2-word options (`eotg_aug_inherit.010.a`: "Begin.", `eotg_aug_inherit.018.a`: "Guards!", `eotg_aug_kingpin.006.b_grandeur``: "No.", `eotg_aug_kingpin.012.b`: "Talk.", `eotg_aug_kingpin.033.a_syndicate`: "Buy.").
- **Evidence:** The writer self-review caught several 2-word options in earlier rounds and corrected them, but several 2-word options remain. Spec §7 states target option length is 5–9 words framed as character choices.
-* *Suggested fix:** Expand 2-word choices into full character intent, e.g. "Order the surgical procedure to begin.", "Call the household guard at once.", "Refuse the demands of the syndicate.", "Hear what terms they offer first."
- **Confidence:** High.


---

3## NOTE / VERIFICATION Findings

#### GQD-005
- **Severity:** NOTE
- **Category:** 1 (Truth against spec options / Verified)
- **Location:** Both drafts (`inherit_text_gemina_r1.md` and `kingpin_text_gemini_r1.md`).
- **Evidence:**
  All option keys match spec option effects in `cybernetics_v2_fracturing_inheritance.md` £5.3 and `cybernetics_v2_kingpin.md` §5.8.
  - In Fracturing Inheritance: `.l01.d`, `.009.a`, `.022 slipping af, `.o18.c`, `.006`, `.o25.a`, and `.026` binding wording from §7.1 is followed verbatim.
  - In Neurofractured Kingpin: `.013 `` ("Execute [eotg_kp.GetFirstName]. Now.") and L1 compassionate ("proper rites") match §7.4 binding instructions.
  - Zero forbidden terms from Kingpin §7.4 (`warrant`, `police`, `puppet`, `clean house`) appear in localized prose.
  - No fragment key collisions: non-fragment text in W3 cleanly complements `kingpin_fragments_gemina_r1.md`.
- **Status:** PASS. Documented and verified.

---

## 2. Invariant & Conformance Summary Table

| Check | Target | Status | Notes |
|---|---|---|---|
| **Binding Wording (§7.1 / §7.4)** | Both drafts | PASS | All required literal strings from spec £7.1 and §7.4 are present. |
| **Truth against Options** | §5.3, §5.8 | PASS | Option keys and outcomes match spec logic. |
| **Bracket & Scope Syntax** | All 33 distinct bracket scopes | PASS | Bare scopes used (`[eotg_kp.GetFirstName]`); zero illegal `[scope:xxx]`; zero `'s` after `Custom()`. |
| **Banned Vocabulary** | Both drafts | FAIL(4 instances: GQD-001, GQD-002, GQD-003) | 1 instance of `throne` (GQD_001); 3 instances of `night` (GQD-002, GQD-003). |
| **Voice & Pronouns** | Both drafts | PASS | First-person ruler voice preserved; dynamic pronoun functions used (`GetSheHe`, `GetHerHim`, `GetHerHis`) rather than singular 'they' for individuals. |
| **Writer Claimed Checks** | Self-review tables | VERIFIED | Writer self-review checks accurately report previous corrections; independent QA confirmed residual issues. |

---

## 3. Total Findings
- **BLOCKER:** 0
- **MAJOR:** 1 (GQD-001)
- **MINOR:** 3 (GQD-002, GQD-003, GQD-004)
-* *NOTE:** 1 (GQD-005)
