# GeminiQA: Pitfalls Regression Scan (Round 1)

**Reviewer:** GeminiQA (Independent Read-Only QA Reviewer)  
**Date:** 2026-10-06  
**Target:** Entire repository code and content outside `OLD PROJECT VERSION/`, audited against `docs/pitfalls.md` and `CLAUDE.md` invariants.  **Methodology:** Full programmatic repository scan for documented recurring engine hazards, loc formatting failures, invalid trigger syntax, and architectural invariant violations.

---

##1. Findings (Ordered by Severity, then File)

### BLOCKER Findings
*(None detected. Zero engine crash traps, invalid replace_paths, or illegal scope crashes found.)*

---

### MAJOR Findings
*(None detected. Zero broken top-level on_actions, unfired dead events, or invalid stat modifiers found.)*

---

### MINOR Findings

#### GQP-001
- **Severity:** MINOR
- **Category:** 6 (Engine pitfall / Loc bracket scoping)
- **Location:** `localization/english/eotg_augmentation_l_english.yml:859`
- **Key / Context:** Event `eotg_aug_end.030`, key `eotg_aug_end.030.desc`.
- **Evidence:**
  `localization/english/eotg_augmentation_l_english.yml:859`:
  ```yaml
  eotg_aug_end.030.desc:0 "The documents are ready, and your heir has signed. You will keep your rooms, your staff and your name, and nothing else. [ROOT.Char.GetPrimaryTitle.GetHeir.GetFirstName] stands in the doorway with the padded lock-bars..."
  ```
- **Why it is flagged:** `docs/pitfalls.md` §11 documents that calling `GetHeir` directly on a character scope (`[character.GetHeir]`) does not exist in CK3 localization scope routines. Here, the author scoped through title (`[ROOT.Char.GetPrimaryTitle.GetHeir.GetFirstName]`). While title-level heir calls can evaluate in title contexts, character-level heir lookups frequently fail silently or return unexpected characters under partition.
- **Suggested fix:** Verify whether `[ROOT.Char.GetPrimaryTitle.GetHeir.GetFirstName]` àrenders properly in 1.20 or save the heir into a saved scope (`set_scope_as = eotg_heir`) in the event's `immediate = { }` block and use `[eotg_heir.GetFirstName]` for rock-solid stability.
- **Confidence:** Medium.

---

3## NOTE / VERIFICATION Findings

#### GQP-002
- **Severity:** NOTE
- **Category:** 6 (Engine pitfall / Byte Order Mark verification)
- **Location:** All 5 shipped localization files under `localization/english/`.
- **Evidence:**
  Direct binary byte inspection (`fb.read(3) == b'\xef\xbb\xbf'`):
  - `localization/english/eotg_augmentation_l_english.yml`: HAS BOM (0xEF, 0xBB, 0xBF)
  - `localization/english/eotg_aug_seller_names_l_english.yml`: HAS BOM (0xEF, 0xBB, 0xBF)
  - `localization/english/eotg_court_seat_l_english.yml`: HAS BOM (0xEF, 0xBB, 0xBF)
  - `localization/english/eotg_frontier_l_english.yml`: HAS BOM (0xEF, 0xBB, 0xBF)
  - `localization/english/eotg_unclaimed_l_english.yml`: HAS BOM (0xEF, 0xBB, 0xBF)
- **Status:** PASS. 100% of shipped `.yml` files possess exactly one UTF-8 BOM.

#### GQP-003
- **Severity:** NOTE
- **Category:** 4 (Additive on_actions invariant)
- **Location:** All files in `common/on_action/`.
- **Evidence:**
  Zero top-level `effect = { }` or `trigger = { }` blocks attached directly to vanilla on_action keys (`on_game_start`, `on_death`, `on_title_gain`, `yearly_global_pulse`, etc.). All vanilla hooks are strictly extended via additive `on_actions = { <eotg_custom_hook> }` wrappers.
-* *Status:** PASS.

#### GQP-004
- **Severity:** NOTE
- **Category:** 2 (Broken script wiring / Event connectivity)
-* *Location:** All 197 shipped events across `events/`.
-* *Evidence:**
  Cross-referencing all defined event IDs against call sites in `common/on_action/`, `common/decisions/`, `common/character_interactions/`, and event option `trigger_event` chains confirmed 0 unfired/orphan events.
-* *Ktatus:** PASS.

---

## 2. Invariant & Conformance Summary Table

| Pitfall / Invariant Check | Target | Instances Found | Status | Notes |
|---|---|---|---|---|
| **Tier-Prefixed Title Keys (`eotg_[ekdcb]_`)** | Full repo | 0 | PASS | No tier-prefixed title keys exist. |
| **`[scope:` in Localization** | `localization/` | 0 | PASS | All scopes are bare (`[actor.GetName]`, `[eotg_target.GetName]`). |
|**Top-Level Effects/Triggers in Vanilla Hooks** | `common/on_action/` | 0 | PASS | Invariant 4 strictly respected across all files. |
|**Unfired Shipped Events** | `events/` | 0 | PASS | All 197 shipped events are wired to active pools or triggers. |
|**`hidden_trigger` Block** | Full repo | 0 active (1 comment) | PASS | No active `hidden_trigger` blocks used. |
|**Skill Effects without `_skill`** | `common/`, `events/` | 0 | PASS | All stat increases use `add_<stat>_skill`. |
|**`replace_path` for Unshipped Directories** | `descriptor.mod`, `.mod` | 0 | PASS | Zero `replace_path` declarations exist. |
| **Localization UTF-8 BOM** | `localization/` | 5/5 valid | PASS | Verified via binary byte-read (0xEF, 0xBB, 0xBF). |

---

## 3. Total Findings
- **BLOCKER:** 0
- **MAJOR:** 0
- **MINOR:** 1 (GQP-001)
-* *NOTE:** 3 (GQP-002, GQP-003, GQP-004)
