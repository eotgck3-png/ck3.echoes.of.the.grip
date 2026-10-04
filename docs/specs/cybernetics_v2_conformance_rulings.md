# Cybernetics v2 — conformance rulings (CB-26)

**Author:** eotg-architect, 2026-10-04
**Answers:** `docs/qa/cybernetics_spec_conformance_cloud.md` (CB-24), including its §6 local verification.
**Checked against:** the script at `1578f85` (round 2 and the balance amendment are in, from `2e6cef2`), and [cybernetics_v2_balance.md](cybernetics_v2_balance.md), the newest amendment. Line numbers in the report are stale, so every finding was re-found by event id.
**Gate:** 3 (Systems), on the temporary map. Not blocked.

**Not ruled here:**
- **M7 and M8.** The Cybernetics session is fixing these in script under CB-27. This file gives no instruction that touches patron.004, patron.006, `eotg_aug_patron_critic_candidate` or `eotg_aug_patron_betray_effect`. The architect's half of M7 (ratifying the Patron tick order in phase 5 §2.3) waits for that fix to land.
- **L2, L5, L13.** These belong to the scripter and need no spec ruling. **L3** is moot (§6 of the report).

**Verdicts:**
- **RATIFY:** the script is right. The spec text is amended in this commit.
- **REJECT:** the spec is right, or a third answer is better. There is a work item for the scripter or localizer in §2.
- **RESOLVED:** round 2 or the balance amendment already changed it.

Nothing here adds an event, an option or a story beat. §3 lists the two places where the human could choose to add one.

---

## 1. Rulings

### 1.1 MEDIUM

| # | Verdict | Ruling | Spec edited |
|---|---|---|---|
| M1 | **REJECT** (third answer) | **tier2.011.c.** The steward gate and the stewardship × 2 weight are **ratified**. The option's text names the steward, and vanilla gates options on a councillor existing (`events/dlc/ep3/ep3_yearly_1.txt:174`, `trigger = { exists = cp:councillor_spymaster }`). Losing one universal option when there is no steward is acceptable. On success the steward trims the plan, so the result is a **new modifier `eotg_mod_aug_optimised_levies_trimmed`**: `domain_tax_mult = 0.05`, no `vassal_opinion`. Half the gain with no penalty keeps c a real choice against a (full gain, penalty, risk +3), not a strictly better gamble. The success text stays as it is: it now describes what happens. **Work item W1.** | phase4 §4 (tier2.011), §7; index §3.4 |
| M2 | **RATIFY** | **tier2.003.d:** the surgery helper plus one extra ambitious minor-loss line, not surgery plus embrace. Stacking both helpers counts the zealous and ambitious lines twice. The option is gated on ambitious, so its own line is the one that matters. Index rule 6 (one stress helper on a morally loaded option) is met. | phase1 §3 |
| M3 | **RATIFY** | **init.006.c:** the physician gets `eotg_opinion_aug_admiration` (10 years). `eotg_opinion_aug_grateful_patient` displays as "Grateful Patient". Putting it on the physician would label the doctor as the patient. Every other use in the script puts it on the person who was treated. | phase2 §2 |
| M4 | **RATIFY a / REJECT e** | **init.006.** Option a is full price. The ×0.75 belongs to c, which is the physician's path; if a were discounted too, c would be "a, plus calibration, for the same price". Option e is "as a", so it is full price too. **Work item W2** (remove e's discount). | phase2 §2 |
| M5 | **RATIFY** | **init.020 → Iron Retinue.** It starts once the court has **one** augmented knight, at `phase = 1` with exactly one and `phase = 2` with two or more (`eotg_aug_start_retinue_effect`). As specced (always `phase = 2`, from the second knight), nothing could ever reach `phase = 1`, so retinue.001 *First of the Iron* was unreachable. | phase5 §3.1, §7 item 5 |
| M6 | **RATIFY clauses / REJECT throttle** | `eotg_mod_aug_patron_clause` and `_clause_final` survive full removal: the debt is contractual, not hardware. That is better design than the spec's line. `eotg_mod_aug_patron_throttle` is "a restriction in the firmware" (its own loc), so it must go with the firmware. **Work item W3** (clean-up effect only; nothing in the patron.006 area). | phase5 §4 |
| M9 | **RATIFY** | nr.002 fires from step 2, on a real progression of a knight, when the liege is not on cooldown. It sets the liege cooldown, and step 5 is skipped for that character that year. It is not a step-5 list entry. | phase6 §1 |
| M10 | **RATIFY** | **nr.004.d [just] "A trial."** It has no tyranny stress helper. A trial is the just ruler's due process: the option gives just a minor stress *loss*, and the helper's just medium gain would cancel it. Vanilla tyranny still comes from `imprison_character_effect`. | phase6 §3 |
| M11 | **RATIFY** | **The Heir's Arc runs once per ruler.** heir.004, and the story's landless exit, set the permanent `eotg_flag_aug_heir_arc_done`, and both start sites read it. The arc builds to one climax (ally / usurp / kill). Restarting it the year after, for every new heir, would turn that climax into a loop. Balance §5.8(a) already reads the flag. A later heir's arc is new scope (§3). | phase3 §1 step 2, §4 |
| M12 | **RATIFY** (drop) | fracture.007 *Dead Reckoning* comes **out** of Thread T1's payoff list. Phase 3 never specced a voice variant for it, and its ledger premise doesn't need one. | index §4 T1 |

### 1.2 LOW: script against spec

| # | Verdict | Ruling | Spec edited |
|---|---|---|---|
| L1 | **RATIFY** | No `is_valid_showing_failures_only` gold check on the regressions. `cost` alone is the vanilla convention (report §6, item 1). Whether the engine shows the reason is part of the in-game check list. | phase0 §1.3 |
| L4 | **RATIFY** (with S5) | Index rule 7 covers **episode** victims: people the implant hurts in a fit. The Errand's critic is a **chosen** target. The syndicate names them, and the ruler decides whether to kill them. Chosen targets are picked by their own scripted trigger and named in loc. Rule 7 and done-item 6 now say so. (The envoy exclusion is CB-27 M8 and is not specced here.) | index §1 rule 7, §6 item 6; phase5 §2.4 |
| L6 | **RATIFY** | fracture.002 uses `FAMILY_FACTOR` 0.25 in Storm and 0.05 otherwise, per phase 0 §2.2 and phase 3 done-item 4. | phase1 §5 |
| L7 | **RATIFY** | init.008's complication uses `increase_wounds_no_death_effect = { REASON = wounds }`. The vanilla reason is valid (report §6). | phase2 §2 |
| L8 | **RATIFY** | init.012's lost branch uses `increase_wounds_no_death_effect = { REASON = treatment }`, so an already-wounded ruler is not reset to rank 1. | phase2 §2 |
| L9 | **RATIFY** (rule loosened) | `ai_chance` base 30 is the **default**, not a rule. A decline or a no-op may go down to 10. The option an offer exists to sell may go up to 40. Every option still has ≥ 2 trait modifiers. Vanilla bases range from 0 to 100. | index §1 rule 6; phase2 §2 |
| L10 | **RATIFY** | Vanilla placeholder decision art is accepted: `decision_smith`, `decision_physician`, `decision_knight_kneeling`, `decision_prison`, `decision_realm` and `decision_misc`, plus the mod's `eotg_decision_partial_removal.dds` reused for Remove Implants (CB-05). Bespoke art stays human art debt. | phase2 §3, phase3 §8 |
| L11 | **RATIFY** | **Back-alley retry:** 50% per pulse while `eotg_flag_aug_backalley_retry` (2 years) is held. While the flag is held, the normal initiation list does not roll. The ruler is looking for a surgeon, so nothing else is offered. The Sickly Child block is outside the list and still rolls. | phase2 §2 (init.012) |
| L12 | **RATIFY** | **init.019.e "Two is enough."** is a universal option with no gate. a and c cost gold, and b commits to a programme, so e is the only option nobody can be locked out of. Content characters still get its relief. | phase5 §3.3 |
| L14 | **REJECT** (the spec's intent stands) | "Callers name them in loc" has to happen somewhere. The forgetting is a 25% roll that runs on the click, so no option tooltip can name the person in advance. The name is reported after the fact, with a toast inside `eotg_aug_forget_relation_effect`, using the vanilla hidden-outcome toast pattern (hunt.8540, as tier3.014.b already does). **Work item W4.** | phase3 §2 |
| L15 | **REJECT** | The reveal has **6** variants, as phase 3 budgets. Today, a ruler who **spared** a real traitor (fracture.019.e, "No. Not them.") is told "You were right", and their option reads "As I knew." with +100 prestige. Add `desc_true_spared` and a name variant on the fallback option. On that path there is no prestige; risk +5 stays (the implant was right and was overruled). **Work item W5.** | phase3 §3 (fracture.020) |
| L16 | **RATIFY** | tier1.011.c also adds risk +2. | phase4 §2 |
| L17 | **RATIFY** | tier1.012.a also sets `eotg_flag_suppress_progression` for 1 year and adds the reject helper (the purity pledge). Without it, a strictly beat c. | phase4 §2 |
| L18 | **RATIFY** | tier1.013.a also gives `eotg_mod_withdrawn_from_court` for 3 months. Without it, a strictly beat b. (Balance §5.6 has since made b a roll; a's cost stays.) | phase4 §2 |
| L19 | **RATIFY** | tier1.016.a also adds risk +2: the event couples on its own (index rule 4). | phase4 §2 |
| L20 | **RATIFY** | tier3.019.b also gives +50 prestige (authority kept). Balance §5.6's stewardship roll sits on top of that. | phase4 §6 |
| L21 | **RATIFY** | tier3.023.c also gives a 5-year `eotg_mod_aug_lesson_martial`. Without it, c had no upside against b. | phase4 §6 |
| L22 | **RATIFY** | tier3.014.b reports what you learned with a toast inside `hidden_effect` (hunt.8540; report §6 item 4). Round 2 M7 also hid a's outcome behind a neutral tooltip. | phase4 §6 |
| L23 | **RATIFY** | tier2.015: a, c and d fire .016. b ("Purge and reinstall") ends the chain, because nothing is left to find. The tamperer is a rival, else a picker courtier (0.05), else a vassal. | phase4 §4 |
| L24 | **RATIFY** | tier1.012's branch trigger: a zealous ruler, or a zealous or `theologian` courtier. The bare `cynical` is dropped: it let the event fire with nobody to ask for the tithe. | phase4 §1 |

### 1.3 LOW: contradictions inside the specs

| # | Verdict | Ruling | Spec edited |
|---|---|---|---|
| S1 | RATIFY phase 3 | `eotg_aug_voice` runs 0–5. 5 is Seamless ("no voice now"). | index §3.3 |
| S2 | RATIFY script | The story filter is `story_type`, and `random_owned_story` filters inside `limit`. Both forms are vanilla. The index lists the four `eotg_aug_has_*` story triggers. | index §3.1; phase3 §1, §6; phase5 §1.1, §3.1 |
| S3 | RATIFY phase 3 | Embrace the Cascade needs Neurofractured **and** Storm **and** (voice ≥ 3 or `eotg_flag_aug_may_embrace`), with a 5-year cooldown (round 2). | index §4 T1 |
| S4 | RATIFY phase 3 | `eotg_aug_start_containment_regency_effect` takes `KEEPER` and `SWING`. | index §3.2 |
| S5 | RATIFY | As L4. | as L4 |
| S6 | RATIFY phase 4 | The clarity focus read is tier3.**024**'s roll (decisive +15 at limbs or senses). tier3.023 reads none. | index §4 T7 |
| S7 | RATIFY index | First Contact's branch weight ×1.5 at nerves focus. Phase 4 now records it. | phase4 §5 |
| S8 | RATIFY | "Prefer +" (index rule 4) is the rule. Phase 4's "+ only" is reworded, with tier1.018 a/d (the copycat's risk −10) as the stated exception: a calm option that cleans up someone else's botched install. | phase4 header |
| S9 | RATIFY the ban | First Contact a is "Reply to it." | phase4 §6 |
| S10 | **REJECT** (cap) | tier3.022's insight outcome advances the voice to **1**, not 2, so First Contact (beat 2) still gets its scene. `desc_insight` already reads as a first notice. **Work item W6.** | phase4 §6 |
| S11 | RATIFY | Convention reworded: universal options come first, trait options after. A universal option may follow a trait option where an event gained one later. | phase3 §3; phase4 header |
| S12 | RATIFY | Rule 6's shape (3 universal plus 1–2 trait options) applies to choice events. Chain-outcome stages and notifications may have one or two options. | index §1 rule 6 |
| S13 | RATIFY index | `on_death` is at `game/common/on_action/death.txt:7` (lines 1–5 are its comment header). | phase2 §1.2 |
| S14 | RATIFY script | init.013.e's "+5 risk if already augmented" was a dead clause: init.013 fires only for unaugmented rulers. Deleted. | phase2 §2 |
| S15 | RATIFY | Without an heir, patron.005 offers only b and d (grievance +2). a, c and e need the heir. | phase5 §2.4 |
| S16 | RATIFY | `eotg_flag_aug_retinue_permanent` is read on the knight **or** the liege (balance §5.7). | phase5 §3.3; phase6 §1 |
| S17 | RATIFY | `eotg_opinion_aug_passed_over` defaults to 5 years. retinue.005.d applies it for 10 (a standing privilege is a lasting slight). | phase5 §4 |
| S18 | RATIFY | 4 modifiers and 1 opinion (`_retinue_resentment` was dropped). | phase5 §6 |
| S19 | RATIFY | nr.005 has a generic desc. The vanilla trait-gain and trait-loss tooltips name what changed. | phase6 §3 |

### 1.4 Event names updated

These are the titles changed in `5a97355`, plus three earlier drifts found by the same check:

| Event | Was (spec) | Now (loc and spec) |
|---|---|---|
| init.002 | A Corporate Offer | **A Vendor's Pitch** |
| init.005 | A Familiar Change | **Back From the Capital** |
| tier2.005 | The Confessor's Warning | **The Advisor's Warning** |
| fracture.024 | The Familiar Change | **The Same Pattern** |
| nr.005 (5a97355) | The Familiar Change | **Not Quite Them** |
| countdown.005 (5a97355) | No One Asks Any More | **No One Asks Anymore** |
| fracture.019 (earlier) | The False Traitor | **The Flagged Name** |
| fracture.022 (earlier) | The Second Voice | **We** |

Edited in: index §4 (T1, T4); phase1 §1 and §3; phase3 §1 and §3; phase5 §1.3; phase6 header and §1; balance §5.3.

---

## 2. Work items (REJECTs)

All are small. None touches patron.004, patron.006, the critic trigger or the betray effect.

| # | Owner | Finding | Instruction |
|---|---|---|---|
| **W1** | scripter | M1 | (1) `common/modifiers/eotg_augmentation_modifiers.txt`, next to `eotg_mod_aug_optimised_levies`: add `eotg_mod_aug_optimised_levies_trimmed = { icon = stewardship_positive  domain_tax_mult = 0.05 }`, with no `vassal_opinion`. (2) In `eotg_aug_tier2.011` option c, change the success branch's `add_character_modifier` to the trimmed key (still `years = 3`). Keep the steward gate and the weight. (3) Add `remove_character_modifier = eotg_mod_aug_optimised_levies_trimmed` to `eotg_clean_all_aug_modifiers`, under the Phase 4 block. |
| **W1-loc** | localizer | M1 | Add `eotg_mod_aug_optimised_levies_trimmed` (name, e.g. "Trimmed Levy Plan") and `eotg_mod_aug_optimised_levies_trimmed_desc`. The desc says the steward cut the parts the vassals would have felt; it does not quantify. `eotg_aug_tier2.011.c.success` is unchanged. US spelling. |
| **W2** | scripter | M4 | `eotg_aug_init.006` option e: replace both the `gold >=` trigger value and the `remove_short_term_gold` value with plain `medium_gold_value` (drop the physician `if`/`multiply = 0.75`). Fix the comment: "As a, plus a lesson; full price, as a." |
| **W3** | scripter | M6 | `eotg_clean_all_aug_modifiers`: add `remove_character_modifier = eotg_mod_aug_patron_throttle`. Reword the Phase 5 comment: the clause modifiers stay (the debt survives), and the throttle goes with the firmware. Do not touch `eotg_aug_patron_betray_effect` (CB-27 M7 is in it). |
| **W4** | scripter | L14 | `eotg_aug_forget_relation_effect`: inside the closing `if = { limit = { exists = scope:eotg_forgotten } … }`, after the opinion, add `hidden_effect = { send_interface_toast = { title = eotg_aug_forget_relation_toast  left_icon = scope:eotg_forgotten } }`. Same shape as tier3.014.b (vanilla hunt.8540). |
| **W4-loc** | localizer | L14 | `eotg_aug_forget_relation_toast`: one line naming `[eotg_forgotten.GetName]`. The ruler looks at them and the relationship is not there any more. Neurofractured register (index §5 items 1–2: no "whisper", "Void", "possess"). Do not name the relation type (it varies). |
| **W5** | scripter | L15 | `eotg_fracture.020`: (1) in the desc `first_valid`, **before** `desc_true`, add `triggered_desc = { trigger = { var:eotg_aug_accusation_true = flag:yes  var:eotg_aug_accusation_action = flag:spared }  desc = eotg_fracture.020.desc_true_spared }`. (2) In the merged fallback option's `name` block, add a first entry for the same condition, with text `eotg_fracture.020.c_spared`. (3) In that option's true branch, give the +100 prestige only when the action is **not** `flag:spared`. Risk +5 stays on every true path. Keep round 2 H1's opinion logic as it is. |
| **W5-loc** | localizer | L15 | `eotg_fracture.020.desc_true_spared`: [eotg_accused.GetName] was what the flag said, and you refused to act on it. Voice register; do not say the implant "was right" in the voice's own words. `eotg_fracture.020.c_spared`: a short admission, e.g. "It was right. I was not." |
| **W6** | scripter | S10 | `eotg_aug_tier3.022`, insight branch: `eotg_aug_voice_advance_effect = { STAGE = 2 }` → `{ STAGE = 1 }`. No loc change. |

**Follow-up after CB-27 M7 lands (scripter, not now):** `eotg_aug_patron_betray_effect` adds the throttle even to an owner who has left the system. Put the `add_character_modifier` inside the existing `eotg_is_augmented_any = yes` branch, as the risk already is.

**Validation for W1–W6:** Tiger, `px_lsp_diagnostics.js` and `px_vocab_check.py` on the touched files, except the known-benign items in `CLAUDE.md` §Validation. QA re-runs audit 8 (coupling) on tier2.011, fracture.020 and tier3.022.

---

## 3. For the human (new scope, not specced)

These would add beats. They are listed so the choice is visible. Nothing is built.
1. **A second Heir's Arc for a later heir** (M11), for example after heir.004 executes the first heir. Today the arc runs once per ruler.
2. **A Patron arc beat for an owner who has had the implants removed** (M6). Today the debt simply continues: the clause keeps charging, and the story's demands go on reading the variable.

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Apply work items W1–W6 in `docs/specs/cybernetics_v2_conformance_rulings.md` §2 (none touch patron.004/.006 or the betray effect), run the three validators, then hand W1-loc, W4-loc and W5-loc to the localizer.
- files: docs/specs/cybernetics_v2_conformance_rulings.md, docs/specs/cybernetics_v2.md, docs/specs/cybernetics_v2_phase0.md, docs/specs/cybernetics_v2_phase1.md, docs/specs/cybernetics_v2_phase2.md, docs/specs/cybernetics_v2_phase3.md, docs/specs/cybernetics_v2_phase4.md, docs/specs/cybernetics_v2_phase5.md, docs/specs/cybernetics_v2_phase6.md, docs/specs/cybernetics_v2_balance.md
- needs-loc: eotg_mod_aug_optimised_levies_trimmed, eotg_mod_aug_optimised_levies_trimmed_desc, eotg_aug_forget_relation_toast, eotg_fracture.020.desc_true_spared, eotg_fracture.020.c_spared
- needs-lore: none (W4-loc and W5-loc follow the existing voice register rules)
- needs-human: §3, two optional new-scope beats (later-heir arc; post-removal patron beat); the L1 in-game check that an unaffordable regression decision shows its cost reason
