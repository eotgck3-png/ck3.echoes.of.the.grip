# Localization QA Audit & Polish Report

**Date:** 2026-10-04  
**Scope:** `localization/english/eotg_augmentation_l_english.yml`, `localization/english/eotg_frontier_l_english.yml`  
**Setting Standard:** Galactic Age / Sci-Fi Fantasy (Third Era, 866 AG; Void, Interstellar Dynasties, Cybernetics, Feudal Ranks)  
**Language Standard:** Canadian English (Oxford `-ize`, British `-our`, `-re`, doubled consonants like `traveller`, Canadian administrative/legal precision)

---

## 1. Executive Summary

A comprehensive quality assurance deep dive was conducted across all active mod localization files (`eotg_augmentation_l_english.yml` and `eotg_frontier_l_english.yml`, totaling over 2,500 lines). The QA pass audited narrative tone, grammatical correctness, sentence rhythm, UI string formatting, pronoun consistency, and setting immersion.

All identified defects—ranging from incomplete sentence fragments and hardcoded assumptions to 21st-century software jargon and American spellings—have been corrected in the working tree. Furthermore, the repository's automated style validation tool (`docs/tools/eotg_lint.py` and `docs/tools/eotg_lint_style.json`) has been aligned to Canadian English, achieving 0 errors and 0 warnings.

---

## 2. Categorized Changes & Rationale

### A. Grammar, Syntax & Fragment Corrections
* **`eotg_frontier.003.desc`**
  * *Before:* `"If the Frontier succeeds, [eotg_frontier_sponsor.GetSheHe] will share the credit. If it fails, the loss."`
  * *After:* `"If the Frontier succeeds, [eotg_frontier_sponsor.GetSheHe] will share the credit. If it fails, [eotg_frontier_sponsor.GetSheHe] will share the loss."`
  * *Rationale:* The second conditional was a truncated fragment lacking a subject and verb. Completing the clause restores parallel rhetorical symmetry and clarity.

* **`eotg_aug_init.011.d.tt`**
  * *Before:* `"The surgeon cuts the rejected hardware out. How the body takes it follows."`
  * *After:* `"The surgeon cuts the rejected hardware out. The body's reaction follows."`
  * *Rationale:* Replaced awkward, clunky syntax with clean, idiomatic phrasing fitting CK3 tooltip conventions.

* **`eotg_aug_proc.020.desc_fragments`**
  * *Before:* `"Now and then the fragments left in catch: a sting along the old line of the cabling, then nothing."`
  * *After:* `"Now and then the fragments left inside catch: a sting along the old line of the cabling, then nothing."`
  * *Rationale:* "left in catch" had colliding prepositions/verbs creating a momentary parsing stall; "left inside catch" provides immediate syntactic clarity.

* **`eotg_aug_policy_cooldown_tt`**
  * *Before:* `"The Augmentation law has not been changed recently"`
  * *After:* `"The augmentation law has not been changed recently"`
  * *Rationale:* Removed ungrammatical mid-sentence capitalization of common noun "augmentation".

---

### B. Galactic Age / Sci-Fi Fantasy Tone & Immersion
* **`eotg_aug_tier1.003.desc`**
  * *Before:* `"A lord does not twitch."`
  * *After:* `"A liege does not twitch."`
  * *Rationale:* Replaced hardcoded male title `lord` with gender-neutral feudal sovereign title `liege`, properly accommodating female rulers, alien dynasties, and galactic peerage.

* **`eotg_fracture.017.desc`**
  * *Before:* `"formatted like a permissions dialog"`
  * *After:* `"formatted like an access prompt"`
  * *Rationale:* Replaced anachronistic 21st-century desktop OS GUI terminology ("permissions dialog") with universe-appropriate cybernetic system terminology ("access prompt").

* **`eotg_aug_tier2.003.desc` & `desc_sought`**
  * *Before:* `"unusual for these people"`
  * *After:* `"unusual for their trade"`
  * *Rationale:* "These people" sounded colloquial, vague, and modern; "their trade" grounds the interaction in galactic clinic commerce and technician guilds.

* **`eotg_fracture.004.desc`**
  * *Before:* `"what actually happened"`
  * *After:* `"what truly happened"`
  * *Rationale:* Replaced conversational modern filler ("actually") with elevated narrative prose fitting space-opera feudal chronicles.

* **`eotg_aug_tier3.021.c.yours`**
  * *Before:* `"Your memory is what is wrong."`
  * *After:* `"The flaw is in your memory."`
  * *Rationale:* Elevated clunky, repetitive spoken phrasing to sharp, clinical aristocratic dialogue.

---

### C. Repetition Elimination & Title Flow
* **`eotg_aug_tier3.011.t`**
  * *Before:* `"The Feast You Didn't Eat"`
  * *After:* `"The Uneaten Feast"`
  * *Rationale:* Eliminates casual contraction in event titles; matches the solemn, literary tone of other tier 3 mental dissolution events.

* **`eotg_aug_retinue.002.t`**
  * *Before:* `"More Ask"`
  * *After:* `"More Step Forward"`
  * *Rationale:* "More Ask" sounded grammatically abrupt and unpolished.

* **`eotg_aug_retinue.004.t`**
  * *Before:* `"The Unaugmented Resent"`
  * *After:* `"Resentment in the Ranks"`
  * *Rationale:* Converted awkward subject-verb title into a punchy martial event heading.

* **`eotg_aug_nr.003.t`**
  * *Before:* `"Something Is Wrong With Them"`
  * *After:* `"Something Is Wrong"`
  * *Rationale:* Tightened title cadence, letting the suspense speak for itself.

* **`eotg_aug_nr.005.t`**
  * *Before:* `"Not Quite Them"`
  * *After:* `"A Changed Champion"`
  * *Rationale:* Replaced vague pronoun phrasing with evocative, character-focused titular framing.

* **`eotg_aug_proc.020.desc_rejected`**
  * *Before:* `"Your body threw the hardware out. It still reaches for what it threw out."`
  * *After:* `"Your body rejected the hardware. It still reaches for what was cast out."`
  * *Rationale:* Eliminated immediate repetition of the colloquial verb phrase "threw out".

* **`eotg_aug_tamper.002.desc`**
  * *Before:* `"For one night [target.GetName]'s hardware was in the agents' hands, panel open, while [target.GetSheHe] slept under a dose."`
  * *After:* `"For one night [target.GetName]'s hardware was in their hands, panel open, while [target.GetSheHe] slept under a dose."`
  * *Rationale:* Replaced redundant repetition of "agents" immediately after "The agents report before dawn."

* **`eotg_aug_tamper.003.desc_discovered`**
  * *Before:* `"Worse, the agents were seen. [target.GetName] will know who sent the agents."`
  * *After:* `"Worse, the agents were seen. [target.GetName] will know who sent them."`
  * *Rationale:* Replaced clumsy echo of "agents" in back-to-back sentences.

---

### D. Formatting & Engine Fixes
* **`eotg_aug_end.009.b`**
  * *Before:* `"...No."`
  * *After:* `"... No."`
  * *Rationale:* Corrected missing typographic space following ellipsis.

* **`eotg_aug_end.011.desc`**
  * *Before:* `"[eotg_target.MakeScope.Var('eotg_aug_times_installed').GetValue]"`
  * *After:* `"[eotg_target.MakeScope.Var('eotg_aug_times_installed').GetValue|0]"`
  * *Rationale:* Added `|0` integer formatter to prevent the Clausewitz engine from rendering raw script floating-point values (e.g. `1.000000`).

* **`eotg_aug_init.011.desc_discovered` & `eotg_aug_proc.outcome_discovered`**
  * *Before:* `"Word has got out."`
  * *After:* `"Word has gotten out."`
  * *Rationale:* Standardized on "gotten", standard in Canadian and North American formal usage.

* **UTF-8 BOM Preservation:**
  * Re-verified and ensured that both `.yml` files begin with byte-order mark (`\xef\xbb\xbf`), required by the CK3 Clausewitz engine.

---

### E. Canadian English Alignment
Conformed mod localization to Canadian English standards (British spelling for `-our`, `-re`, and double `-ll-`, combined with North American vocabulary):
* `travelers` → `travellers` (`eotg_frontier_mod_unsettled_desc`)
* `traveled` → `travelled` (`eotg_aug_init.016.desc`)
* `theater` → `theatre` (`eotg_aug_tier1.005.e`, `eotg_aug_init.007.a.failure`)
* `color` → `colour` (`eotg_aug_init.011.desc_infection`)
* `re-priced` → `repriced` (`eotg_aug_patron.008.desc`)
* `favor` / `favorably` / `favored` → `favour` / `favourably` / `favoured`:
  * `eotg_aug_init.020.desc`
  * `eotg_aug_tier3.019.desc`
  * `eotg_aug_retinue.003.desc`
  * `eotg_aug_policy_favor`
  * `EOTG_AUG_AI_FAVORED`
* `honor` / `honors` → `honour` / `honours`:
  * `eotg_frontier.004.b`
  * `eotg_fracture.004.c`
  * `eotg_aug_retinue.001.desc`
  * `eotg_aug_retinue.004.b`
  * `eotg_aug_retinue.004.d`

---

## 3. Tooling & Linter Updates

* **`docs/tools/eotg_lint_style.json`:**
  * Adjusted the linter configuration so that Canadian standard spellings (`colour`, `armour`, `honour`, `favour`, `behaviour`, `rumour`, `labour`, `valour`, `vigour`, `neighbour`, `harbour`, `splendour`, `centre`, `theatre`, `metre`, `traveller`, `cancelled`, `labelled`) are recognized as valid project standards.
* **`docs/tools/eotg_lint_pronoun_allowlist.txt`:**
  * Added `eotg_aug_tamper.003.desc_discovered` where "them" correctly refers to the infiltration agents rather than the single scoped target.
* **Validation Outcome:**
  * Ran `python docs/tools/eotg_lint.py`:
  * **Result:** `0 finding(s), 0 new`. Zero errors, zero warnings.

---

## 4. Verification Checklist

- [x] All localization keys valid and parsed.
- [x] Clausewitz UTF-8 with BOM format verified on disk.
- [x] No orphaned brackets or corrupted variable links.
- [x] Galactic Age sci-fi fantasy worldbuilding terminology respected.
- [x] Canadian English spelling and syntax enforced consistently.
- [x] Linter (`eotg_lint.py`) passes with exit code 0.
