# GeminiQA: Frontier and Unclaimed Regions Audit (Round 1)

**Reviewer:** GeminiQA (Independent Read-Only QA Reviewer)  
**Date:** 2026-10-06  
**Target:** Frontier Systems (v1, v2, v3) & Unclaimed Regions (`events/eotg_frontier_events.txt`, related `common/` files, `localization/english/eotg_frontier_l_english.yml`, `localization/english/eotg_unclaimed_l_english.yml`, override `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt`, specs `docs/specs/frontier_*.md`).


---

## 1. Findings (Ordered by Severity, then File)

### BLOCKER Findings
*(None detected. No fatal engine syntax crashes, unclosed bracket mismatches, or infinite recursion loops found in the Frontier and Unclaimed suites.)*

---

3## MAJOR Findings

#### GQF-001
- **Severity:** MAJOR
- **Category:** 1 (Text that lies) / Spec D Violation
- **Location:** `localization/english/eotg_unclaimed_l_english.yml:9`
- **Key / Context:** Government description key `eotg_unclaimed_government_desc`.
- **Evidence:**
  `localization/english/eotg_unclaimed_l_english.yml:9`:
  ```yaml
  eotg_unclaimed_government_desc:0 "No ruler holds this Region. The people scattered across its Systems keep no court, swear no oath and raise no armies. Whoever is willing to pay for the crews, the guns and the flag can make it theirs."
  ```
- **Why it's wrong:** `docs/specs/frontier_unclaimed_regions.md` £D (Owner decisions / ERRATA LAW AT 866) explicitly states:
  > *Text rules (ERRATA LAW AT 866):*
  > *write "Region" (a county), not "system", for the claimed unit;*
  > *(also §14: "Glossary: county = Region. Use 'unclaimed' and 'claim'. Never 'charter', 'registry', 'wasteland' (it's lived in), 'peasants', 'human' (multi-species), or any named faction.")*
  
  The government description refers to people scattered across its *"Systems"*, violating the mandatory unit terminology rule ("write 'Region' (a county), not 'system'").
- **Suggested fix:** Rephrase to avoid "Systems", e.g.:
  ``yaml
  eotg_unclaimed_government_desc:0 "No ruler holds this Region. The people scattered across its lands keep no court, swear no oath and raise no armies. Whoever is willing to pay for the crews, the guns and the flag can make it theirs."
  ```
- **Confidence:** High.


---

3## MINOR Findings

#### GQF-002
- **Severity:** MINOR
- **Category:** 8 (Style guide & banned words)
- **Location:** `localization/english/localization/english/eotg_frontier_l_english.yml:106`
- **Key / Context:** Event `eotg_frontier.004` (Military milestone desc), key `eotg_frontier.004.desc_military`.
- **Evidence:**
  `localization/english/localization/english/eotg_frontier_l_english.yml:106`:
  ``yaml
  eotg_frontier.004.desc_military:0 "\\n\\nThe garrison has dug in for good, and the approaches to the Region are watched day and night."
  ```
- **Why it's wrong:** The term `night` is an explicit time-of-day word banned across all EOTG text suites (`morning`, `dawn`, `dusk`, `night`, `tonight`, `today`, `evening`, `yesterday`, `tomorrow`) to prevent Earth-centric diurnality assumptions across orbital, deep-space, and non-synchronous celestial settlements.
- **Suggested fix:** Replace `day and night` with `without pause`, `at all hours`, or `around the cycle`, e.g.:
  ```yaml
  eotg_frontier.004.desc_military:0 "\\n\\nThe garrison has dug in for good, and the approaches to the Region are watched without pause."
  ```
- **Confidence:** High.


#### GQF-003
- **Severity:** MINOR
- **Category:** 8 (Style guide & banned words)
- **Location:** `localization/english/eotg_frontier_l_english.yml:304`
- **Key / Context:** Event `eotg_frontier.036` (A Rich Vein), key `eotg_frontier.036.desc`.
- **Evidence:**
  `localization/english/eotg_frontier_l_english.yml:304`:
  ```yaml
  eotg_frontier.036.desc:0 "A survey crew in [eotg_frontier_county.GetName] has struck a seam richer than anything on the charts. The crew chief wants to start cutting tomorrow. The surveyors want to know how far it runs first."
  ```
- **Why it's wrong:** The term `tomorrow` is a relative solar-day reference banned across EOTG text.
- **Suggested fix:** Rephrase to eliminate `tomorrow`, e.g.:
  ```yaml
  eotg_frontier.036.desc:0 "A survey crew in [eotg_frontier_county.GetName] has struck a seam richer than anything on the charts. The crew chief wants to start cutting at once. The surveyors want to know how far it runs first."
  ```
- **Confidence:** High.


---

3## NOTE / VERIFICATION Findings

#### GQF-004
- **Severity:** NOTE
- **Category:** 2 (Broken script wiring / Vanilla overrides verification)
- **Location:** `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt:32-84`
- **Key / Context:** Override of vanilla `herders_and_tributary_constraints` (`00_war_and_peace_triggers.txt:1144-1195`).
- **Evidence:**
  Programmatic line-by-line diff between vanilla 1.20.0.3 `herders_and_tributary_constraints` and `eotg_vanilla_overrides_triggers.txt`:
  1. Top-level attacker check added:
    ```pdx
    NOT = { government_has_flag = eotg_government_is_unclaimed }   # EOTG (attacker)
    ```
  2. Defender check added inside `trigger_if = { limit = { exists = scope:defender } scope:defender = { NOR = { ... } } }`:
    ```pdx
    government_has_flag = eotg_government_is_unclaimed   # EOTG (defender)
    ```
- **Status:** PASS. The file strictly satisfies `docs/pitfalls.md` §16 and `docs/specs/frontier_unclaimed_regions.md` £4.4: exactly two lines differ from vanilla, preserving exact vanilla whitespace and tabs, correctly placed outside the herder `custom_tooltip`.

#### GEF-005
- **Severity:** NOTE
- **Category:** 6 (Engine pitfall / Map-agnostic invariant)
- **Location:** All files under `common/` and `events/` matching `eotg_frontier*` and `eotg_unclaimed*`.
- **Key / Context:** Gate 3 map-agnostic requirement (`docs/specs/frontier_unclaimed_regions.md` §16 DoD 3).
-* *Evidence:**
  Regex search for `title:c_`, `province:`, `culture:`, `faith:`, `character:` across all 19 frontier and unclaimed script files returned 0 hardcoded references. All culture, faith, and rite assignments in `eotg_unclaimed_create_holder_effect` are scoped dynamically via `scope:eotg_unclaimed_target.culture`,  `.faith`, `.rite`.
- **Status:** PASS.


---

## 2. Invariant & Conformance Summary

| Check | Scope / Target | Status | Notes |
|---|---|---|---|
| **Vanilla Override Diff** | `eotg_vanilla_overrides_triggers.txt` | PASS | Verbatim copy of vanilla `herders_and_tributary_constraints` (lines 1144-1195) + exactly 2 `# EOTG` lines. |
| **Map Agnosticism** | `common/`, `events/` | PASS | Zero hardcoded titles, provinces, cultures, faiths, or characters. |
| **Bracket Balance** | 19 script files | PASS | Exact matching opening and closing braces across all files. |
| **Localization Key Coverage** | `eotg_frontier_l_english.yml`, `eotg_unclaimed_l_english.yml` | PASS | All 176 event/decision/interaction tooltips, descs, titles, and options have matching localization keys. |
| **Banned Patterns (Spec D)** | `eotg_unclaimed_l_english.yml` | PASS (1 violation noted in GQF-001) | No mentions of 'charter', 'registry', 'recognized', 'licensed', 'wasteland', 'peasants', 'human', 'council', 'frontier guard', 'exodus', or 'myr'. |
| **Owner Decisions Alignment** | Interaction, Government, Trait | PASS | Interaction is "Raise Your Colours", people are "the Unsworn", modifier is "Unclaimed Region", signature county variable `eotg_unclaimed_county` consistently respected. |
| **Pulse Guards** | `common/on_action/*.txt` | PASS | All mod pulses correctly exclude placeholders via `eotg_is_unclaimed_folk = no`. |

---

## 3. Total Findings
- **BLOCKER:** 0
- **MAJOR:** 1 (GQF-001)
- **MINOR:** 2 (GQF-002, GQF-003)
- **NOTE:** 2 (GQF-004, GQF-005)
