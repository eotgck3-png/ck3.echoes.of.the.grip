# Spec: Cybernetics v2 — balance and design amendment (QA round 2 §4)

**Author:** eotg-architect, 2026-10-04
**Answers:** `docs/qa/cybernetics_qa_round2.md` §4.3, issues 1–10, and the AI gaps in the §4.1 scorecard ("Everyone takes part, AI included": partly; 10 of 13 decisions unused; non-rulers progress at 4% a year).
**Builds on:** [cybernetics_v2.md](cybernetics_v2.md) (index; its §1 rules bind this file), phases 0–6, [cybernetics_track.md](cybernetics_track.md).
**Not in scope:** round 2 §1–§2 (scripter batch A, in flight) and §3 (localizer, in flight). Where this spec touches an option that batch A also fixes, batch A lands first and this spec applies on top (index §1 rule 12). Each case is listed in §5.0.

**Amended 2026-10-04** (coordinator relay): the human resolved HQ1 and HQ2 (both defaults). The lore-keeper's must-fixes M1–M8 are applied (§5.1, §5.4, §5.9, §7, §8). Further rulings are recorded:
- congenital re-activation (§5.9);
- heir.006 kinslayer (§5.0);
- the 5-year Embrace cooldown (§5.0);
- ~~US spelling~~ (§8); superseded: Canadian English (supersedes US spelling: owner ruling 2026-10-04, loc commit 4168bb8).

The exact player-facing wording is in the lore-keeper's report, which goes to the localizer directly. It covers the toasts, the Pursue decision, the sought descs, the Embrace roll, the Heir/Patron/Retinue variants and the license clause. This spec states the rules. Where it quotes a line, the quote is binding.

**New events: none.** Every change converts an existing option or event, adds options to existing events, adds one decision, or changes weights, gates and costs. **Nothing here needs the human's approval for new events.**

---

## 0. Human decisions (resolved 2026-10-04)

Both questions concerned pacing intent, which vanilla cannot settle. **The human accepted both defaults on 2026-10-04.** Nothing in this spec is open.

| # | Question | **Resolution** | Why |
|---|---|---|---|
| **HQ1** | **What is the fastest the player should be able to climb?** This spec sets a minimum of 5 years at Augmented and 5 at Enhanced, so initiation to Overclocked takes at least 10 years for a player who pushes. | **Resolved: 10 years minimum (5 + 5).** | One 20–30-year reign then shows Augmented, Enhanced, Overclocked, the cascade (calm: 7 pulses) and most of Neurofractured (6–12 years to the terminal). Ten years still covers about 4 Augmented and Enhanced flavor events and one chain. A shorter minimum skips most of the 43 tier-1 and tier-2 events. A longer one recreates issue 1. |
| **HQ2** | **What should the world look like?** These are the bands the 50-year observer run (§9.2) is judged against. | **Resolved: "common, with a dangerous top".** At **game year 30**, among AI count-tier-and-above rulers: **25–40% augmented**. Of those, **≥ 15% Overclocked, Neurofractured or Seamless**. At least **one terminal outcome per 10 Neurofractured rulers per decade**. Round 2's likely world is everyone Augmented and no one Overclocked; that is the failure case. | The goal is "everyone takes part", but in a setting where cybernetics is still developing (canon: SETTING LORE). A world where most rulers are augmented reads as normal, not as a choice. |

Everything else is decided below from vanilla precedent (the standing rule, index §0).

---

## 1. Purpose & gate

Round 2 found the system sound on engine and loc but weak where the design goals live:
- progression is a lottery that takes decades;
- the AI never uses the decision layer;
- the world fills with Augmented rulers and almost no Overclocked or Neurofractured ones;
- Neurofractured plays like Overclocked;
- Neurofractured can be paused and Seamless can't be lost;
- 91% of outcomes are fixed;
- the non-ruler lifecycle is invisible;
- the arcs don't react to the ruler's state;
- the vanilla mental-health layer is ignored;
- nothing throttles the AI at the top.

This spec fixes each with exact identifiers, numbers and file locations.

**Gate 3 (Systems), against the temporary map** (`docs/agent_workflow.md` §5 rule 2). **Not blocked.** It is map-agnostic: no title, province, culture, faith or character keys. It reads development only through script values (§5.1), so the real map can retune them without a script change.

**Build order.** Batch A (round 2 §7.1) lands first. Then:
- **Part B1, mechanics:** issues 1, 2, 3, 5 and 10, plus the script-values file;
- **Part B2, content:** issues 4, 6, 7, 8 and 9.

B1 can ship and go to the observer run (§9.2) before B2 is built. B2 does not change any number that the run measures, except the non-ruler rate.

---

## 2. Signature resource

**`eotg_fracture_risk`** (hidden character variable, 0–100) is unchanged. The tier state is the XP on `eotg_cybernetics`, at exactly 0, 50 or 100.

How this spec touches them:
- **XP** still changes only in `eotg_aug_set_integration_effect`. The new decision fires `eotg_aug_tier1.002` or `eotg_aug_tier2.003`, which reach the existing set-integration call sites (tier1.022, tier2.003 a/c/d). No new `add_trait_xp` anywhere.
- **Risk stays hidden.**
  - The override odds (§5.4) and the AI weights read the variable. No tooltip, toast or decision tooltip shows a number or the word "risk".
  - Every risk move inside a new roll sits in `hidden_effect`, as the existing install effects already do.
  - Override toasts describe what happened, not how likely it was.
- **Coupling (invariant 5).** Every option this spec adds or converts moves risk on root or a saved augmented character, changes tier, or reads the band. Converted events keep at least one coupling option. QA audit 8 re-runs on every touched event.

---

## 3. Identifier table

All keys carry the `eotg_` prefix. No landed titles are involved. Loc keys use the existing dot form (index §0, "Loc key form").

### 3.1 New

| Type | Key | Where | Owner | Issue |
|---|---|---|---|---|
| decision | `eotg_decision_aug_pursue_next_stage` | `common/decisions/eotg_augmentation_decisions.txt` | scripter | 1 |
| character flag (timed, 5 years) | `eotg_flag_aug_settling` | set in `eotg_aug_initiate_effect` and `eotg_aug_set_integration_effect` | scripter | 1 |
| character flag (timed, 60 days) | `eotg_flag_aug_sought_upgrade` | set by the new decision; read by tier1.002 / tier2.003 desc and `ai_chance` | scripter | 1 |
| script values file (new; vanilla folder, no `replace_path`) | `common/script_values/eotg_augmentation_values.txt` | — | scripter | 1, 4, 5, 7 |
| script value | `eotg_aug_dev_gate_enhanced` (15) | values file | scripter | 1 |
| script value | `eotg_aug_dev_gate_overclocked` (20) | values file | scripter | 1 |
| script value | `eotg_aug_override_chance` | values file | scripter | 4 |
| script value | `eotg_aug_nf_drift_value` | values file | scripter | 5 |
| script value | `eotg_aug_sedation_relief_value` | values file | scripter | 5 |
| script value | `eotg_aug_nr_progress_chance` | values file | scripter | 7 |
| character variable (permanent) | `eotg_aug_sedation_courses` | incremented by `eotg_decision_aug_sedation` | scripter | 5 |
| character flag (timed, 30 days) | `eotg_flag_aug_embrace_failed` | end.009 roll → read by fracture.029's desc | scripter | 5 |
| character flags (timed, 2 years) | `eotg_flag_aug_chain_edge`, `eotg_flag_aug_chain_strain` | chain-head rolls → read and cleared by the next stage | scripter | 6 |
| saved scope values (event-local) | `eotg_override`, `eotg_misled`, `eotg_letter_shown` | converted fracture events | scripter | 4 |
| character variable (non-rulers, 0–10) | `eotg_aug_nr_battle_bonus` | combat on_action → read by the progression chance | scripter | 7 |
| character flag (permanent) | `eotg_flag_aug_congenital_masked` | set by init.006.f; read and cleared by `eotg_aug_remove_all_effect` and both regression decisions | scripter | 9 |
| custom on_action | `eotg_on_combat_aug_knights` | `common/on_action/eotg_augmentation_on_actions.txt` | scripter | 7 |

**No new modifiers, opinions, traits, story cycles, namespaces or icons.** Decision art is a placeholder: vanilla `decision_smith.dds`, as `eotg_decision_seek_augmentation` uses. Bespoke art is human art debt, as for the other placeholders.

### 3.2 Changed (key kept)

| Key | Change | Issue |
|---|---|---|
| `eotg_cybernetics` (trait) | adds `monthly_income_mult`: base −0.03, track 50 −0.02, track 100 −0.03 (totals −3 / −5 / −8%) | 3 |
| `eotg_can_progress_to_enhanced` / `_overclocked` | dev gate through the script values; adds `NOT = { has_character_flag = eotg_flag_aug_settling }` | 1 |
| `eotg_aug_initiate_effect` | sets `eotg_flag_aug_settling` (5 years) when the character was unaugmented | 1 |
| `eotg_aug_set_integration_effect` | sets `eotg_flag_aug_settling` (5 years). Still the only `add_trait_xp`. | 1 |
| `eotg_aug_remove_all_effect`, `eotg_aug_total_integration_effect` | `remove_variable` `eotg_aug_sedation_courses` and `eotg_aug_nr_battle_bonus` | 5, 7 |
| `eotg_aug_remove_all_effect`, `eotg_decision_partial_removal`, `eotg_decision_overclock_regression` | re-activate a masked congenital trait (`make_trait_active`) | 9 |
| heir.006 (batch A) | `add_kinslayer_trait_or_nothing_effect` on the murdering heir | ruling |
| all 12 existing decisions | `ai_check_interval` → `ai_check_interval_by_tier`; new `ai_potential` / `ai_will_do` (§5.2) | 2 |
| `eotg_decision_aug_sedation` | increments `eotg_aug_sedation_courses` | 5 |
| 5 yearly `random_list`s (initiation, tier 1, tier 2, Overclocked, the 3 NF bands) | AI-only modifiers on the "nothing" entry | 3, 10 |
| `eotg_story_aug_countdown` | stage windows 60–67 / 68–76 / ≥ 77 | 10 |
| `eotg_story_aug_heir_arc` | starts from Overclocked; stages ≥ 1 wait for Neurofractured; reads `eotg_flag_aug_child_patient` | 8 |
| `eotg_story_aug_patron`, `eotg_story_aug_retinue` | Neurofractured short-circuit in the tick | 8 |
| `eotg_on_yearly_aug_nonruler_check` | rates (§5.7) | 7 |

---

## 4. File placement

| Path | What changes |
|---|---|
| `common/script_values/eotg_augmentation_values.txt` | **new file**, vanilla folder (`game/common/script_values/`). Orchestrator: add `common/script_values/` to the placement table in `CLAUDE.md`. |
| `common/decisions/eotg_augmentation_decisions.txt` | new decision; AI fields on all 12; sedation counter |
| `common/on_action/eotg_augmentation_on_actions.txt` | nothing-weight modifiers; Heir's Arc start at Overclocked; NF drift via script value; non-ruler rates; combat hook |
| `common/scripted_triggers/eotg_augmentation_triggers.txt` | `eotg_can_progress_to_*` |
| `common/scripted_effects/eotg_augmentation_effects.txt` | settle flag; variable clean-up |
| `common/story_cycles/eotg_augmentation_stories.txt` | Countdown windows; Heir's Arc; Patron and Retinue ticks |
| `common/traits/eotg_augmentation_traits.txt` | income modifier on the track |
| `events/eotg_augmentation_{initiation,tier1,tier2,tier3,fracture,endgame,heir,patron,retinue}.txt` | option conversions and additions (§5.4–§5.9) |
| `localization/english/eotg_augmentation_l_english.yml` | §7 (localizer) |

---

## 5. Wiring — the amendments, issue by issue

**Monte-Carlo assumptions.** These are round 2's, rerun with its own `sim.py`:
- one roll per pulse, `W / (W + nothing)`;
- a 1–2-year cooldown block after an event fires;
- acceptance 1.0 for the player and 0.45 for the AI;
- no deaths.

Added for this spec:
- AI decision checks once a year, with probability `ai_will_do`%;
- gold available 60% of the time;
- 90% follow-through in the fired event.

Scripts: `sim2.py` to `sim5.py` in this session's scratchpad.

> Round 2 quoted 32–44 years from initiation to Overclocked by adding the two steps' medians. Adding the two distributions instead gives a median of 39–53 years, with only 15–22% of players at Overclocked within 20 years. That is the baseline below.

### 5.0 Overlap with batch A (land batch A first)
| Item here | Batch A item on the same code |
|---|---|
| §5.4 fracture.019 override | **H1** (fracture.020 outcome logic). The override must set the same "arrested" marker that H1's reveal reads. |
| §5.4 fracture.011 misleading desc | **M8** (no-witness variants) |
| §5.5 end.009 roll | low-priority "Embrace the Cascade has no cooldown". **This spec depends on it:** without a cooldown, end.009.b ("...No.", risk −10) is a repeatable risk pump. **Batch A set it at `cooldown = { years = 5 }`. Build on that.** |
| §5.8 Retinue tick | **H2** (`eotg_flag_aug_retinue_done`) |
| §5.7 non-ruler rates | **M13** (the non-ruler cascade ends the Countdown) |
| heir.006 (batch A's hidden kill stage, from the **H3** fix) | **Ruling 2026-10-04:** in heir.006, the heir who murders the ruler gets vanilla `add_kinslayer_trait_or_nothing_effect` (`common/scripted_effects/00_secret_effects.txt:433`, round 2 M4). Run it in the heir's scope, with the ruler as the victim. It is a deliberate killing, so kinslayer applies (§10 policy). |

---

### 5.1 Issue 1 — progression is a lottery (TOP)

**Decision: the "Pursue the Next Stage" decision (option A), not a separate progression roll (option B).**

| | A: decision | B: own roll, odds growing with time at tier |
|---|---|---|
| Player who always pushes | median **12 years** (5 + 5 minimum, 100% within 20) | median 20 years (58% within 20) |
| AI, `ai_will_do` 15 / 25 / 40 | median 28 / 21 / 18 years; within 20 years: 24% / 45% / 70% | median 25 years (21% within 20) |
| Agency | the player chooses when; the gates are visible | still a lottery, with a better curve |
| Vanilla shape | yes (see precedent below) | no vanilla analogue for a personal state |
| AI tuning | per-trait `ai_will_do`, by tier | one curve for everyone |

Option A answers the design complaint directly ("no decision lets the player pursue the next stage"). It also gives the AI a tunable, personality-driven lever, which issue 2 needs anyway.

**`eotg_decision_aug_pursue_next_stage`:**

| Field | Value |
|---|---|
| `picture` | `gfx/interface/illustrations/decisions/decision_smith.dds` (placeholder, as Seek) |
| `is_shown` | `OR = { eotg_is_aug_tier1 = yes  eotg_is_aug_tier2 = yes }`, `highest_held_title_tier >= tier_county` (the population the yearly pulse serves) |
| `is_valid_showing_failures_only` | `is_available_adult = yes` |
| `is_valid` | `custom_tooltip = { text = eotg_decision_aug_pursue_next_stage_settling_tt  NOT = { has_character_flag = eotg_flag_aug_settling } }`; `custom_tooltip = { text = eotg_decision_aug_pursue_next_stage_suppressed_tt  NOT = { has_character_flag = eotg_flag_suppress_progression } }`; `trigger_if = { limit = { eotg_is_aug_tier1 = yes }  capital_county = { development_level >= eotg_aug_dev_gate_enhanced }  eotg_aug_can_afford_upgrade = yes }`; `trigger_else = { capital_county = { development_level >= eotg_aug_dev_gate_overclocked }  gold >= major_gold_value }` |
| `cost` | none. The fired event charges, as `eotg_decision_seek_augmentation` does; a decision cost would charge twice. |
| `cooldown` | `{ years = 2 }` (declining in the event must not be spammable) |
| `effect` | `custom_tooltip = eotg_decision_aug_pursue_next_stage_tooltip`; `add_character_flag = { flag = eotg_flag_aug_sought_upgrade  days = 60 }`; `if tier1` → `trigger_event = eotg_aug_tier1.002`, `else` → `trigger_event = eotg_aug_tier2.003` |
| `ai_check_interval_by_tier` | `barony = 0  county = 24  duchy = 12  kingdom = 12  empire = 12  hegemony = 12` |
| `ai_potential` | `is_at_war = no`; `stress_level < 2`; NOT `zealous`; NOT `content`; `trigger_if tier1: short_term_gold >= medium_gold_value`, `else: short_term_gold >= major_gold_value` |
| `ai_will_do` | `base = 15`; +20 `ambitious`; +10 `brave`; +10 `arrogant`; +10 `cynical`; −10 `craven`; −10 `paranoid`; `factor = 0.5` if tier 2 and `eotg_aug_pressure_flicker = no` (AI prudence at Enhanced; the AI may read the variable, the player never sees it) |

**Changes around it:**
1. **Minimum time at tier.** `eotg_flag_aug_settling`, `years = 5`:
   - set in `eotg_aug_initiate_effect` (inside its existing "was unaugmented" branch);
   - set in `eotg_aug_set_integration_effect` (every call, including the two regressions: relapse is slower too);
   - read in both `eotg_can_progress_to_*` triggers, so the random Upgrade branches respect the same gate;
   - read in the decision's `is_valid` through a `custom_tooltip`, so the player never sees a raw flag name.
2. **Development gates move to script values and come down: Enhanced 20 → 15, Overclocked 35 → 20.** The initiation gate stays at 10.
   - **Evidence:** across vanilla's `history/titles` development entries (n = 4,288), only **1.3% reach 35** and 16.3% reach 20, while 48.6% reach 10.
   - Round 2's simulation ignored this gate. Development 35 is a second hidden lottery and a likely cause of "almost no Overclocked".
   - These defaults are provisional. The observer run measures the temporary map's distribution (§9.2 item 8), and the real map retunes the two script values.
   - This changes track spec §2.2 rule 4 ("gates unchanged"). That rule protected the XP rework's pacing, not the numbers themselves.
3. **The event follows through when sought.**
   - `eotg_aug_tier1.002` options b, c and `eotg_aug_tier2.003` options b, e: add `ai_chance` `modifier = { factor = 0.1  has_character_flag = eotg_flag_aug_sought_upgrade }`. (Corrected 2026-10-04 after B1 QA: tier2.003.c is a follow-through option, since it pays and sets XP 100, so it must not get the decline factor.)
   - `eotg_on_game_start_aug_init` also sets `eotg_flag_aug_settling` (5 years) on characters who start augmented, so HQ1's 10-year minimum holds from game start. (Ruled 2026-10-04.)
   - Both events: a first `triggered_desc` on the flag (`.desc_sought`).
   - tier1.022 `immediate` and every tier2.003 option: `remove_character_flag = eotg_flag_aug_sought_upgrade`.
4. **The random Upgrade branches stay** (tier 1 weight 30, tier 2 weight 25), as the unsolicited offer. They are now gated by the settle flag as well.

**Vanilla precedent:**
- `common/decisions/00_lifestyle_decisions.txt:342` `commission_epic_decision`: a gold-gated decision that fires an event chain (`trigger_event = commission_epic.0001`), with a `cooldown`, `ai_check_interval_by_tier` (`county = 0`, `duchy+ = 120`), `ai_potential` on `short_term_gold`, and `show_as_tooltip` (:395).
- The `custom_tooltip` trigger wrapper: `00_lifestyle_decisions.txt:527`.
- The trigger-side script value on the right-hand side: `gold >= medium_gold_value` (`10_religious_decisions.txt:3054`, already cited in Phase 0).

**Pacing:** see the table above. Content behind the wait (71 of 152 events) becomes reachable within one reign for a player who pushes. The AI reaches Overclocked in 18–28 years if it survives. Combined with issue 2's regressions, the observer run should show a visible Overclocked and Neurofractured population.

**Risks:**
- A player can rush to Overclocked and see few tier-1 and tier-2 events. The 5-year floor bounds this (HQ1).
- Gold-poor AI counts may never qualify. The observer run measures the gold-gate failure rate (§9.2 item 7).
- The settle flag on knights (through `eotg_aug_initiate_effect`) is harmless; Phase 6 does not read it.

---

### 5.2 Issue 2 — the AI's decision layer is inert

**Recommendation:** all 12 existing decisions switch to `ai_check_interval_by_tier`, with conditional `ai_will_do`. `ai_will_do` is the % chance per check (`_decisions.info:143`). Barony is always 0: the system serves count-tier rulers and above. Cheap `ai_potential` lines come first, so the 12-month checks cost little. Vanilla checks kingdom-tier dynasty decisions every month (`00_dynasty_decisions.txt:14`).

| Decision | interval by tier (county / duchy / kingdom+) | `ai_potential` | `ai_will_do` |
|---|---|---|---|
| `eotg_decision_overclock_regression` | 12 / 12 / 6 | `eotg_is_aug_tier3 = yes`, `OR = { stress_level >= 2  eotg_aug_has_countdown = yes  eotg_aug_pressure_storm = yes }` | base 0; **+50** Countdown running **and** `stress_level >= 2`; +25 Countdown running (and stress < 2); +20 `eotg_aug_pressure_storm`; +15 `content`; +15 `craven`; +10 has `eotg_flag_aug_intervention_discount`; −20 `ambitious`; −15 `arrogant`; −15 `stubborn` |
| `eotg_decision_partial_removal` | 36 / 24 / 24 | tier 2, `stress_level >= 2` | base 5; +20 `stress_level >= 3`; +15 `content`; +15 `zealous`; −15 `ambitious` |
| `eotg_decision_maintenance_protocol` | 12 / 12 / 12 | `has_trait = eotg_cybernetics`, NOT `eotg_flag_maintenance_cooldown` | base 10; **+50** tier 3; +30 Countdown running; +20 tier 2 and NOT `has_character_modifier = eotg_mod_implant_calibrated`; +10 `diligent`; −10 `lazy`; −10 `callous` |
| `eotg_decision_consult_physician` | 12 / 12 / 12 | as `is_shown` | base 10; **+50** tier 3; +20 Countdown running; +10 `diligent`; −10 `lazy` |
| `eotg_decision_seek_augmentation` | **0** / 36 / 24 | `eotg_ai_wants_augmentation = yes` (unchanged) | base 10; +15 `ambitious`; +10 `cynical`; +10 `prowess <= 6`; `factor = 0` `zealous`. **County 0** on purpose: counts are offered, never seek (issue 3). |
| `eotg_decision_remove_implants` | 36 / 24 / 24 | tier 1, `OR = { stress_level >= 2  has_trait = zealous }` | base 5; +20 `content`; +20 `zealous`; +15 `stress_level >= 3`; −15 `ambitious` |
| `eotg_decision_augment_retainer` | 36 / 24 / 12 | `has_trait = eotg_cybernetics`, `any_knight = { eotg_aug_retainer_candidate = yes }` | base 10; +15 `ambitious`; +10 `callous`; +10 `is_at_war = yes`; −10 `compassionate` |
| `eotg_decision_aug_restraints` | 12 / 12 / 12 | NF, NOT restrained, `OR = { stress_level >= 1  eotg_aug_pressure_flicker = no }` (**drops** the compassionate/content-only gate) | base 15; +25 `eotg_aug_pressure_storm`; +20 `compassionate`; +10 `humble`; +15 `has_active_diarchy = yes`; −10 `arrogant`; −20 `sadistic` |
| `eotg_decision_aug_sedation` | 12 / 12 / 12 | NF, NOT sedated, `OR = { stress_level >= 1  eotg_aug_pressure_flicker = no }` | base 20; +25 storm band; +15 `craven`; +10 `content`; −10 `stubborn`; `factor = 0.5` if `var:eotg_aug_sedation_courses >= 2` (the AI respects tolerance, §5.5) |
| `eotg_decision_aug_appoint_warden` | 12 / 12 / 12 | as `is_shown`, plus `eotg_aug_has_warden_candidate = { RULER = root }` | base 5; +30 storm band; +20 adult primary heir; +15 Heir's Arc at stage ≥ 2; +10 `humble`; −10 `ambitious`; −20 `paranoid` |
| `eotg_decision_aug_embrace_cascade` | 24 / 24 / 24 | as `is_shown` | base 3; +15 `ambitious`; +10 `callous`; +10 `var:eotg_aug_voice >= 4`; `factor = 0` `compassionate` |
| `eotg_decision_aug_excision` | 24 / 24 / 24 | `eotg_aug_can_afford_excision = yes`, `OR = { has_trait = eotg_neurofractured  AND = { eotg_is_aug_tier3 = yes  eotg_aug_has_countdown = yes } }`, `stress_level >= 2` | base 5; +25 NF in storm band; +15 `eotg_flag_aug_promised_treatment`; +15 `eotg_has_physician_access = yes`; +10 `zealous`; +10 `content`; −15 `ambitious`; −10 `craven` |
| `eotg_decision_aug_pursue_next_stage` (new) | 24 / 12 / 12 | §5.1 | §5.1 |

**Vanilla precedent:**
- `00_artifact_decisions.txt:616`: `commission_artifact_decision` uses `ai_check_interval_by_tier` (36 at every tier) and `ai_will_do` base 100 with `factor = 0` gates.
- `00_dynasty_decisions.txt:14`: county 12 / duchy 6 / kingdom+ 1 months.
- `00_lifestyle_decisions.txt:342`: county 0 means "this tier never checks".
- Every tier key, `hegemony` included, is required (`_decisions.info:110`).

**Pacing (AI Overclocked, `sim5.py`; maintenance and physician take −8 and −12 at the AI rates above):**

| Accrual | Regress | Cascade | Median years to cascade |
|---|---|---|---|
| calm (12 a year) | 62–66% | 34–38% | 8–11 |
| stress level 1 (20) | 28–48% | 52–72% | 4–5 |
| stress level 2 (28) | ~50% | ~50% | 3–4 |

Today almost every AI Overclocked ruler cascades. Afterwards roughly half regress and half break. After 5 years settling, the regressed ones can climb again (relapse).

**Owner ruling, 2026-10-05: one removal step per stage** (source: the owner; `docs/handoffs/orchestrator_2026-10-05_cyber-fix-batch.md` part B; full table in phase3 §8). Augmented: Remove the Implants. Enhanced: Partial Implant Removal **only**. Overclocked: Downgrade Protocol, plus Excision (Cut It Out) as the last resort. Neurofractured: Excision. `eotg_decision_aug_excision`'s `is_shown` drops tier 2 and becomes `OR = { eotg_is_aug_tier3 = yes  has_trait = eotg_neurofractured }`. The `ai_potential` above already excludes tier 2 and needs no change. Partial Removal is now the only removal at Enhanced, for the AI as for the player. At Overclocked the AI weighs Downgrade (above) against Excision (Countdown running only), and the 35–65% regression share (§9.2 item 4) still applies.

Excision, Warden, Restraints and Sedation should each show ≥ 1 AI use per 10 Neurofractured AI rulers in the observer run (§9.2 item 4).

**Risks:**
- An AI that maintains diligently stretches Overclocked. That is intended, but watch the share at Overclocked.
- AI regression plus the Pursue decision can loop (climb, regress, climb). The 5-year settle per step bounds it to at most one cycle per ~10 years.
- Twelve-month checks on all count-tier-and-above AIs: `ai_potential` leads with a trait test, which is cheap.

---

### 5.3 Issue 3 — wide spread, shallow depth

**Recommendation, three levers:**

**(a) AI throttle on the initiation list** (`eotg_on_yearly_aug_initiation_check`). Add these to the `100 = { }` nothing entry:
```
modifier = { factor = 6  is_ai = yes  highest_held_title_tier < tier_duchy }
modifier = { factor = 3  is_ai = yes  highest_held_title_tier = tier_duchy }
modifier = { factor = 2  is_ai = yes  highest_held_title_tier >= tier_kingdom }
```
- These follow vanilla's tiering: counts are throttled hardest, kings least (`yearly_on_actions.txt:3022-3030`: AI kingdom+ 30%, duchy 70%, count 95% no-event).
- They are gentler than vanilla's 95% for counts. Vanilla throttles flavor; this list creates world state, and the AI must still take part.
- **The "Back From the Capital" entry (init.005, weight 20; formerly *A Familiar Change*) gets `modifier = { factor = 0.5  is_ai = yes }`.** It is the contagion branch: every augmented vassal or courtier raises it.

**(b) AI throttle on the tier-1 and tier-2 lists.** Nothing entry ×2 for AI counts only (`is_ai = yes`, `highest_held_title_tier < tier_duchy`). Their 0.35–0.4 events a year is fine for the player, but in a wider world it is pure AI noise.

**(c) An ongoing cost at Augmented.** Add `monthly_income_mult` to `eotg_cybernetics`:

| Level | Delta | Total |
|---|---|---|
| base | −0.03 | −3% |
| track 50 | −0.02 | −5% |
| track 100 | −0.03 | −8% |

- The cost is realm-relative and map-agnostic, and it shows natively in the trait tooltip.
- Loc framing (trait desc, localizer): firmware licenses and servicing, written in the existing transactional tone.
- It makes Augmented a subscription, not a free +2 prowess and +0.5 health.
- Precedent: vanilla `profligate` carries `monthly_income_mult = -0.10` (`game/common/traits/00_traits.txt:5060`, value at :5067).

**Vanilla precedent:**
- `yearly_on_actions.txt:3022-3030`: tiered AI no-event chances.
- `common/on_action/dlc/mpo/mpo_on_actions_2.txt:468-474` and `:528-534`: AI-only weight modifiers (`modifier = { factor = 2 / 0.5  is_ai = yes }`), "be a bit kinder to the AI".
- `00_traits.txt:5067`: ongoing income cost in a trait.

**Pacing (`sim3.py`; eligible AI, initiation within 20 years; W is the typical non-nothing weight):**

| W | Today | Count ×6 | Duke ×3 | King ×2 |
|---|---|---|---|---|
| 35 | 0.85 | 0.38 | 0.58 | ~0.74 |
| 57 | 0.91 | 0.51 | 0.71 | ~0.82 |
| 80 | 0.94 | 0.63 | 0.80 | ~0.88 |

This model runs about 15–20 points above round 2's measured 55–80%. Scaled to round 2, expect about 30–45% of counts, 45–65% of dukes and 55–75% of kings within 20 years, against 55–80% today. The contagion halving lowers the high-W rows further. Seek adds only a few points, and only for dukes and above.

**Risks:**
- Factors this large are blunt. **They are first guesses for the observer run** (HQ2 bands), not final numbers.
- The income cost also drains AI gold, which slows the Pursue decision slightly. That is acceptable.

---

### 5.4 Issue 4 — Neurofractured events look like Overclocked events

**Recommendation:**
- six Fracture/Storm events get a **hidden override** on their calm options;
- two Storm events lose their third universal option;
- three Flicker events get **misleading** descs.

Override odds rise by band and come from one script value.

**`eotg_aug_override_chance`** (values file):

| Condition | Value |
|---|---|
| base | 0 |
| `eotg_aug_pressure_fracture = yes` | 25 |
| `eotg_aug_pressure_storm = yes` | 40 |
| `var:eotg_aug_voice >= 4` (access was granted) | +15 |
| `has_character_flag = eotg_flag_aug_sedated` | −10 |

Clamp it with `min = 0  max = 60`. Flicker stays at 0: Flicker lies, it does not seize.

**The override pattern (each listed option):**
```
show_as_tooltip = { <the option's own effects> }          # the player sees only what they chose
hidden_effect = {
    random = { chance = eotg_aug_override_chance  save_scope_value_as = { name = eotg_override  value = yes } }
    if = { limit = { exists = scope:eotg_override }
        <the OVERRIDE option's effects, risk included>
        stress_impact = { base = minor_stress_impact_gain }   # losing the hand is stressful
        send_interface_toast = { title = <event>.override_tt  left_icon = root } }
    else = { <the option's own effects> }
}
```
- The chosen option's own stress helper stays visible and applies either way (intent).
- **Toast register (lore M8, binding).** The toast reports an order that was **the ruler's own, already given and already carried out**: the guards are already at the door, the levies already march.
  - It never says or implies that control was taken: no "took control", "seized", "against your will", "something" or "it decided".
  - It never names the implant.
  - It never uses "override", "risk", "static" or any number. `eotg_override` is a script-only name.
  - Exact text: the lore-keeper report.
- In-mod precedent: fracture.017.b and .e (the tooltip shows only the denial).

| Event (band) | Overridden options | Override result | Toast key |
|---|---|---|---|
| **fracture.019** *The Flagged Name* (Fracture) | b "Have them watched.", e [trusting] "No. Not them." | a's effects (arrest, helper tyranny, risk +5): the order to arrest was yours. Sets the same "arrested" marker that fracture.020 reads (after **H1**). | `eotg_fracture.019.override_tt` |
| **fracture.023** *The Wrong War* (Fracture) | a (both variants: "Stand them down." / "Recall the envoys."), e [calm] "Wait for the scouts." | b's effects (gold spent, unease, risk +8) | `eotg_fracture.023.override_tt` |
| **fracture.016** *Blood on the Sleeve* (Fracture) | c "Confess it to the court." | b's effects (helper lie, risk +10): you have already told the court it was an accident | `eotg_fracture.016.override_tt` |
| **fracture.024** *The Same Pattern* (Fracture) | d [compassionate] "Sit with them." | c's effects (house arrest, helper tyranny, their risk −10, root +5) | `eotg_fracture.024.override_tt` |
| **fracture.025** *Containment Regency* (Storm) | a "Let them.", e [content] "Take it. Please, take it." | d's effects (keeper under house arrest, helper tyranny, risk +12). Design intent: the implant refuses to give up access. **The toast only reports that the ruler's own guards already hold the keeper** (M8). | `eotg_fracture.025.override_tt` |
| **fracture.006** *The Warrant* (Storm) | b "Offer concessions…", d [just] "Submit to their tribunal." | a's effects (crush; imprison `eotg_warrant_vassal`) | `eotg_fracture.006.override_tt` |

**Storm loses a universal option** (QA: "Drop the third universal option in Storm"):
- **fracture.002.b** "Someone. Anyone. Help me contain this." gets `trigger = { eotg_aug_pressure_storm = no }`. It stays in the Fracture band.
- **fracture.004.c** "Bury them with honors." becomes a **[zealous]** trait option (`trigger` + `trait = zealous`; effects unchanged). The Court Massacre is Storm-only, so it now has two universal options.

**Misleading descs in Flicker.** Each gets `random = { chance = 25  save_scope_value_as = { name = eotg_misled  value = yes } }` in `immediate`.
- **fracture.009** *Lost Hour.*
  - When misled, the bad outcome happens in `immediate` (hidden): 60% `remove_short_term_gold = minor_gold_value`, 40% picker-wounded victim. `eotg_fracture.009.desc_misled` **replaces** the base desc (lore M3):
    - it is the first `triggered_desc` in a `first_valid`, with trigger `exists = scope:eotg_misled`, and the base desc is the fallback;
    - it keeps the hook (the lost hour) and says the minutes record you in council the whole hour;
    - it never mentions a "steward".
  - Options a, c and e (the investigating ones) also send `eotg_fracture.009.misled_tt` ("The minutes were written afterwards. In your hand."). b and d do not.
  - Precedent: init.011's hidden flaw shares the "clean" desc.
- **fracture.011** *Conversations With No One.*
  - When misled and a witness exists, the event **reuses the existing no-witness desc, `eotg_fracture.011.desc_none`.** The misled path must be indistinguishable from a genuine no-witness event (lore M4). No new desc key.
  - Every witness-gated option adds `NOT = { exists = scope:eotg_misled }` to its trigger, so the misled path shows exactly the no-witness option set.
  - **No witness name may appear anywhere on the misled path:** desc, options, tooltips or portrait. The witness portrait gets the same guard.
  - The witness gets `eotg_opinion_aug_unease` anyway (hidden). The opinion is the only tell.
  - Lands on top of round 2's **M8** (no-witness variants).
- **fracture.015** *The Unsent Letter.*
  - `immediate` sets the true type as now. When misled, it also saves `eotg_letter_shown`, a different type, which picks the desc.
  - b "Send it" and **d [honest]** ("Send it with a note…") both apply the **true** type's effects inside `hidden_effect`, behind the neutral tooltip `eotg_fracture.015.b.tt`. d keeps its own reassurance on top.
  - The reveal toast (`eotg_fracture.015.b.reveal_confession` / `_threat` / `_devotion`) fires **only when misled** (lore M5), from b or d. When the player was not misled, the desc was already true and there is nothing to reveal.
  - This reuses the existing three type descs; no new desc keys. The neutral tooltip is the same fix shape round 2 prescribed for tier3.014.a (M7).

**Vanilla precedent:**
- Forced madness: `events/trait_specific_events/trait_specific_ongoing_events.txt:27` (`trait_specific_ongoing.1001`). The lunatic episode applies its effect whatever the player wants, in a single option.
- Every-choice-costs: the mental-break events, `events/stress_events/stress_threshold_events.txt` (Level 1–3 breaks, headers :11, :25, :37), where every option grants a coping trait.
- `random` with a script-value `chance`: `events/activities/hunt_activity/hunt_events.txt:4196`.
- `show_as_tooltip`: `00_lifestyle_decisions.txt:395`.
- `send_interface_toast`: `events/activities/chariot_race_activity/chariot_ongoing_events_jp.txt:195-225`.

**Pacing:**
- Fracture band: override-eligible events are about 42% of what fires. At a 25% override on a calm pick, the redirect adds about +0.4 risk a year.
- Storm: about +0.6–1 a year, plus the two removed calm options (about +0.5).
- Net: the terminal arrives about 0.5–1 year sooner for a ruler who plays calm. The Neurofractured span stays at about 6–12 years. The point is the feel: in Storm, about 40% of calm choices are taken away from you.

**Risks:**
- Override plus the tooltip can feel unfair. The toast and the visible stress make clear that the implant acted, not a bug. **This needs an in-game read** (§9.1 item 3).
- Misleading descs must never quantify risk or name the mechanic. Lore must-fixes M3–M5 apply (§8 item 10).
- fracture.019 depends on H1's marker names. The scripter coordinates them.

---

### 5.5 Issue 5 — Neurofractured can be paused; Seamless is a guaranteed win

**(a) Sedation tolerance and a drift floor.** One script value replaces the drift block's separate `eotg_add_fracture_risk` calls in `eotg_on_yearly_aug_neurofractured_check` step 1: `eotg_add_fracture_risk = { AMOUNT = eotg_aug_nf_drift_value }`.

`eotg_aug_nf_drift_value`:
- value 8;
- stress level +4 / +8 / +12 (unchanged rows);
- if `eotg_flag_aug_sedated`: add `eotg_aug_sedation_relief_value`;
- if `eotg_flag_aug_restrained`: add −4;
- **`min = 2`**.

`eotg_aug_sedation_relief_value`, by course number: **−6** on the first course, **−3** on the second, **0** from the third on.

`eotg_decision_aug_sedation`'s effect adds `increment_variable_effect = { VAR = eotg_aug_sedation_courses  VAL = 1 }` before setting the flag.

| Calm Neurofractured ruler, fully treated | Today | After |
|---|---|---|
| Net drift, first course | −2 a year (paused indefinitely) | +2 (floor) |
| Second course | −2 | +2 |
| Third course on | −2 | +4 |
| Years from cascade to the terminal (95), ignoring options | never | ~30 |

At `stress_level >= 1`, which is common at +60% stress gain, the first course nets +2 and the third +8. **The mode can be slowed but never paused.** Restraints get no tolerance (the floor already prevents the pause), and the treatment costs stay as they are.

**(b) Seamless becomes a weighted roll.** `eotg_aug_end.009` a "Yes." and c [ambitious] "Yes. All of it." replace the direct `eotg_aug_total_integration_effect` with a visible `random_list`, each branch with a `desc`. Vanilla shows option odds, and this is not the hidden risk. The weights mirror fracture.027's terminal table:

| Outcome | Base | Modifiers | Effect |
|---|---|---|---|
| Seamless | 40 | +20 `var:eotg_aug_voice >= 4`; +15 `eotg_flag_aug_may_embrace`; +10 on option c | `eotg_aug_total_integration_effect` (c keeps +200 prestige) |
| Cascade death | 30 | +15 `stress_level >= 3`; +10 `health < 2` (as fracture.027) | `eotg_aug_cascade_death_effect` |
| Storm episode | 30 | — | `add_character_flag = { flag = eotg_flag_aug_embrace_failed  days = 30 }`; `trigger_event = { id = eotg_fracture.029  days = 3 }`. fracture.029 is existing; it sets risk to 60, wounds up to two and adds +50 dread. It gets a first `triggered_desc` on the flag, `eotg_fracture.029.desc_embrace`. |

**Seamless ongoing cost: rejected.** The trait already carries:
- diplomacy −8, `attraction_opinion` −60, `general_opinion` −20;
- no children;
- `eotg_opinion_aug_unmade` on every vassal;
- the court exodus (end.011).

With a 22–40% death chance on the way in, Seamless is a gamble that pays off big, not a guaranteed win. A gold drain on top would double the cost.

**Vanilla precedent:**
- Counter variable: `increment_variable_effect` (`common/scripted_effects/00_debug_and_shortcut_effects.txt:6`), as `commission_artifact_decision` uses it (`00_artifact_decisions.txt:609`).
- Clamped script values: `common/script_values/` (`min`/`max`).
- Weighted outcome list with modifiers: `events/health_events.txt:11686`.

**Pacing:**
- A treated calm ruler's Neurofractured span goes from unbounded to about 30 years. An untreated one is unchanged.
- Embrace, best case (voice 4 plus the flag): Seamless 56%, death 21%, Storm 21%. Worst case: Seamless 36%, death 50%.

**Risks:**
- The floor of 2 applies to drift only. Calm event options still lower risk, so the player keeps agency through choices, not through a paid pause.
- The scripter must confirm that a script-value `AMOUNT` resolves inside `eotg_add_fracture_risk`'s `change_variable = { add = $AMOUNT$ }`. Vanilla accepts script values there.

---

### 5.6 Issue 6 — 91% of outcomes are fixed

**Recommendation:** in each of the 23 chain heads (round-2 graph, rerun here), one **universal** option becomes a skill-weighted or trait-weighted roll. Seven heads already have one, and end.010 is a one-option notification; those are skipped.

Two shapes, both from vanilla:
- **Skill check against a fixed bar:** `duel = { skill = S  value = <rating>  50 = { compare_modifier = { value = scope:duel_value  multiplier = 3.5  min = -49 } … }  50 = { compare_modifier = { value = scope:duel_value  multiplier = -3.5  min = -49 } … } }` (`events/activities/chariot_race_activity/chariot_race_events.txt:1947`). Ratings are from `common/script_values/00_basic_values.txt:470-479`: average 8, medium 10, decent 12, high 15.
- **Contest against a person:** the same with `target = scope:x` (`chariot_ongoing_events_jp.txt:195`).
- **Trait-weighted list:** `random_list` with `modifier = { add = N  has_trait = X }` (`health_events.txt:11686`).

**Chain edge.** The success and failure flags carry into the chain's next stage, so the roll matters downstream:
- `eotg_flag_aug_chain_edge` (2 years): +15 to the next stage's good outcome;
- `eotg_flag_aug_chain_strain` (2 years): +10 to its bad outcome;
- the consuming stage removes both flags in `immediate`, after its roll.

Every branch keeps its risk moves in `hidden_effect` and gets a `desc` (the vanilla duel-branch tooltip). Keys are `<event>.<option>.success` and `.failure`.

| Head | Option (universal) | Roll | Success | Failure | Consumer |
|---|---|---|---|---|---|
| init.007 | a "Build the bridge." | trait list 60/40: +20 `diligent`, +15 `patient`, −15 `impatient`, −10 `craven` | edge | — | init.008 success |
| init.010 | a "Cheap is cheap." | intrigue vs `average_skill_rating` | edge | strain | init.011: edge → clean +15; strain → infection +10 |
| init.014 | c (experimental) | existing 60/40 gains +15 `eotg_has_physician_access`, +10 root `learning >= decent_skill_rating` | — | — | — |
| tier1.002 | a "Pay for the upgrade…" | stewardship vs `medium_skill_rating` | edge | — | tier1.022 clean |
| tier1.013 | b "Keep working." | trait list 50/50: +15 `diligent`, +10 `prowess >= decent_skill_rating`, −15 `lazy` | risk +0 | risk +5, strain | tier1.015 failure |
| tier1.018 | c "Help them, for a price." | intrigue contest vs `scope:eotg_copycat` | as today (hook; copycat risk +10) | no hook; copycat unease; copycat risk +10 | — |
| tier2.004 | b (today's 50/50 gamble) | diplomacy contest vs the saved spouse | reassured | disgust | — |
| tier2.012 | a "Investigate quietly." | intrigue contest vs `scope:eotg_flagged`; +15 success if `var:eotg_aug_focus ?= flag:senses` | truth toast (`.success_true` / `.success_false`), lesson intrigue | risk +3, nothing learned | — |
| tier3.007 | c "Compare calibrations." | learning contest vs `scope:other_machine` (the saved scope; batch A may rename it `eotg_other_machine`) | both lesson prowess; root +5, other +10 | root +10, other +5; only the other gets the lesson | — |
| tier3.016 | c "Ride it." | prowess vs `decent_skill_rating` | edge, lesson martial | strain | tier3.022: insight / early cascade |
| tier3.019 | b "Keep everything in my own hands." | stewardship vs `high_skill_rating` | risk +2, lesson learning | risk +8, stress minor gain | — |
| tier3.023 | a "Follow it." | martial vs `decent_skill_rating` | edge | strain | tier3.024: decisive / overreach |
| fracture.007 | a "Write them down." | learning vs `medium_skill_rating` | `add_gold = minor_gold_value`, risk +10 | risk +15, no gold | — |
| fracture.019 | b / e | **the §5.4 override** counts as this head's roll | | | |
| fracture.026 | a "Ask for help." | diplomacy vs `medium_skill_rating` | as today (regency at swing 50 / withdrawn; risk −15) | `eotg_mod_withdrawn_from_court` 2 years only; risk −8 | — |
| end.031 | a "Keep them comfortable." | stewardship vs `medium_skill_rating` | old ruler risk −10 | old ruler risk −3 | — |

**Skipped (already rolled, or forced by design):**
- tier1.016.c (duel), tier2.013.c (intrigue list), tier2.015.a (duel), tier3.017.c (intrigue list), fracture.017.b and .c (override, intrigue list);
- fracture.027 (all rolls), end.010 (notification).

**Pacing:** none intended. Each roll's expected risk is within ±2 of the fixed value it replaces. Fixed outcomes go from about 91% to about 86% of options. **The headline change is that every chain now has a moment where the character's skills or traits decide.**

**Risks:**
- Duel odds show in the tooltip as percentages. That is vanilla behaviour, and they never touch risk.
- Each consumer stage must clear both flags, or an old edge leaks into a later chain. QA greps for this.

---

### 5.7 Issue 7 — the non-ruler lifecycle is too slow to see

**Recommendation (`eotg_on_yearly_aug_nonruler_check`):**

**Step 2, progression:** `chance = eotg_aug_nr_progress_chance`.

| Condition | Chance |
|---|---|
| base | 10 |
| `eotg_aug_is_retinue_knight = yes` | +5 |
| retinue knight with the permanent flag (on the knight or the liege) | +5 more |
| `has_character_flag = eotg_flag_aug_child_patient` | +5 (issue 8) |
| `var:eotg_aug_nr_battle_bonus` | + its value (0–10) |

On progression, `remove_variable = eotg_aug_nr_battle_bonus`.

**Step 3, accrual:** base **6 → 10**; the +6 at `stress_level >= 2` stays. Cascade at 80, unchanged.

**Battle accrual:** a new custom on_action, extended additively:
```
on_combat_end_winner = { on_actions = { eotg_on_combat_aug_knights } }
on_combat_end_loser  = { on_actions = { eotg_on_combat_aug_knights } }
eotg_on_combat_aug_knights = {          # root = the combat side
    effect = {
        every_side_knight = {
            limit = { eotg_is_augmented_any = yes  highest_held_title_tier < tier_county }
            if = { limit = { OR = { eotg_is_aug_tier1 = yes  eotg_is_aug_tier2 = yes } }
                change_variable = { name = eotg_aug_nr_battle_bonus  add = 2 }
                clamp_variable  = { name = eotg_aug_nr_battle_bonus  min = 0  max = 10 } }
            else = { eotg_add_fracture_risk = { AMOUNT = 2 } }   # tier 3 and Neurofractured
        }
    }
}
```
Step 4 drift (+6) is unchanged.

**Vanilla precedent:**
- `game/common/on_action/combat_on_actions.txt:12-14` (`on_combat_end_winner`, root = winning combat side) and `:523-525` (loser);
- `every_side_knight` at `:190`, used there for knight artifacts.

**Pacing (`sim4.py`; a knight augmented at 25; 30% of years at war, 2 battles each):**

| | Median years to cascade | Broken within 15 years | Within 25 years |
|---|---|---|---|
| Today | 54 | 1% | 10% |
| Today, retinue (8%) | 33 | 2% | 29% |
| **Proposed** | **19** | 29% | 79% |
| Proposed, retinue | 16 | 45% | 91% |
| Proposed, permanent retinue | 14 | 59% | 96% |

The QA target was "about 10% a year, battle accrual, a faster track for retinue knights". This puts a knight's whole arc inside one liege's reign.

**Risks:**
- More non-ruler cascades means more nr.006 (outside the cooldown). The observer run counts them (§9.2 item 5).
- The combat hook runs on every battle in the world. `limit` leads with the trait test, and knights per side are few.

---

### 5.8 Issue 8 — Patron and Retinue are side piles, and one seed goes nowhere

**Recommendation:**

**Heir's Arc**

**(a) Seeds from Overclocked.**
- In `eotg_on_yearly_aug_overclocked_check`, after the Countdown block, create `eotg_story_aug_heir_arc` when all of these hold:
  - `eotg_aug_has_countdown = yes`;
  - `eotg_aug_has_heir_arc = no`;
  - NOT `eotg_flag_aug_heir_arc_done`;
  - `primary_heir ?= { is_alive = yes  age >= 14 }`.
- In the story:
  - triggered effects 3–5 (fracture.005, heir.003, heir.004) add `story_owner = { OR = { has_trait = eotg_neurofractured  has_trait = eotg_total_integration } }` to their triggers, so only stage 0 (heir.001 *Concern*) can fire at Overclocked;
  - branch 0 also ends the story when the owner is tier 1 or tier 2. It does not set the done flag, so a later climb can restart it.
- heir.001 gets a first `triggered_desc` for a tier-3 owner: `eotg_aug_heir.001.desc_overclocked`.

**(b) `eotg_flag_aug_child_patient` is read.**
- Heir's Arc `on_setup`: if `var:eotg_heir` has the flag, `eotg_heir_dread` −1 (clamped at 0).
- heir.004: **Ally** +20 and **Kill** `factor = 0.5` if the heir has the flag.
- heir.001 gets a second variant, `desc_patient` ("they were a child when the machine saved them").
- Non-rulers: +5 progression (§5.7).

**Patron (`eotg_story_aug_patron`)**
- **Neurofractured write-off.** A new first entry in both cadences' tick: if `story_owner = { has_trait = eotg_neurofractured }` and `var:eotg_demand < 4`, set `eotg_demand = 4`, set the owner flag `eotg_flag_aug_patron_writeoff` (60 days; a timed flag, no new key type) and fire patron.006. patron.006 gets the first `triggered_desc` `eotg_aug_patron.006.desc_writeoff` ("The syndicate does not service broken units.").
- **Tier 3 scales the firmware lever.**
  - patron.002.b, .003.b, .003.e and .007.c, which carry risk +5 ("the firmware hesitates"): **+8 when `eotg_is_aug_tier3 = yes`**.
  - patron.003.a and .d (−5 / −8): **−8 / −12 at tier 3**.
- **New option patron.002.f** (`trigger = { eotg_is_aug_tier3 = yes }`, universal at that tier): "Let their technicians service the debt." No gold; the demand counts as paid; risk +10 (hidden).
- **Voice:** patron.003 gets a desc variant at `var:eotg_aug_voice >= 2`, `eotg_aug_patron.003.desc_voice` (the model has already read the clause). Register rules apply (§8).

**Retinue (`eotg_story_aug_retinue`)**
- **Neurofractured short-circuit.** A new first entry in the tick: if the owner is Neurofractured and `var:eotg_phase < 5`, set `eotg_phase = 5`. retinue.005 gets the first `triggered_desc` `eotg_aug_retinue.005.desc_fractured` ("The iron looks to you for orders you cannot give."). It lands on top of **H2**: .005 still sets the done flag.
- **New option retinue.003.f** (`trigger = { eotg_is_aug_tier3 = yes }`): "Lock their timing to mine." Each retinue knight risk +5, owner risk +5, owner lesson martial.
- retinue.003 and .004 get desc variants for a tier-3 owner at voice ≥ 2: `…desc_voice` (the model has started counting them).

**Vanilla precedent:**
- Story `effect_group` `first_valid` with conditional entries: `game/common/story_cycles/story_cycle_murders_at_court.txt` (already the shape used).
- Seeds only shift weights: index §4 T3.

**Pacing:**
- The Heir's Arc adds at most one event at Overclocked (heir.001).
- The Patron write-off ends the debt about 2–6 years sooner for broken owners.
- The Retinue short-circuit ends the Program early once the owner breaks.

**Risks:**
- An Overclocked-started arc whose owner regresses ends. That is intended, and the arc can restart.
- patron.002.f's "demand counts as paid" must increment `eotg_demand`, as every demand option does.

---

### 5.9 Issue 9 — the vanilla stress and mental-health layer is ignored

**Recommendation:** add trait-gated options inside existing events. Each uses `trigger = { has_trait = X }` plus `trait = X`, `ai_chance` base 30 with +30 for its own trait, and moves risk.

Vanilla coping traits are `drunkard`, `flagellant`, `reclusive` and `irritable` (`00_traits.txt:4845, 5025, 4951, 4983`). `has_trait = lunatic` and `has_trait = possessed` match through `group_equivalence` (`:5426-5428`, `:5495-5497`), as vanilla's own `trait_specific_ongoing.1001` trigger does.

| Event | New option | Effect |
|---|---|---|
| fracture.003 *Lucid Moment* (Flicker) | f [flagellant] "Pain keeps me here." | risk −8; flagellant major stress loss; 20% `increase_wounds_effect` (a vanilla reason already used in the file) |
| fracture.008 *Wrong Name* (Flicker) | f [irritable] "Then that is your name now!" | +5 dread; `eotg_named` fear; risk +5; irritable minor stress loss |
| fracture.009 *Lost Hour* (Flicker) | f [drunkard] "I was drinking. That is all it was." | helper lie; risk +5; drunkard minor stress loss |
| fracture.010 *The Mirror Doesn't Blink* (Flicker) | f [lunatic] "That is the real one. I am the reflection." | voice advance 2; risk +5 |
| fracture.010 | g [lifestyle_mystic] "Sit before it until it blinks." | +25 piety; risk −5 (closes the spec's unused `lifestyle_mystic`) |
| fracture.014 *The Door* (Flicker) | f [reclusive] "Seal my own door instead." | `eotg_mod_withdrawn_from_court` 1 year; risk −3; reclusive minor stress loss |
| fracture.016 *Blood on the Sleeve* (Fracture) | f [drunkard] "Wine. It's only wine." | helper lie; risk +8 |
| fracture.021 *The Missing Courtier* (Fracture) | e [reclusive] "Then no one else comes in." | withdrawn 1 year; risk −3 |
| fracture.022 *We* (Fracture) | f, `trigger = { has_trait = possessed }` with **no `trait =` field**, so the vanilla Possessed icon and tooltip never show (lore M1): "A small seizure. They pass." | helper lie; risk +5 |
| fracture.023 *The Wrong War* (Fracture) | f [lunatic], two keys by war state, as a and b already have (lore M2). At peace, `eotg_fracture.023.f`: "The war is real. The rest of you are behind." At war, `eotg_fracture.023.f_war`: "The war is over. The rest of you are behind." | +10 dread; risk +10 |
| **init.006** *The Prosthetic* | f (`trigger = { OR = { has_trait = clubfooted  has_trait = hunchbacked } }`), name per the lore-keeper report | as a, plus `minor_gold_value`; `make_trait_inactive` on the held trait (the genes still pass to children); set `eotg_flag_aug_congenital_masked`; risk set to 5; helper surgery. The option name follows the M6 wording rule. |
| **tier1.010** *The Training Yard* | g [physique_good] "The body was already good. Now it is better." | lesson prowess; +50 prestige; risk +3 |
| tier1.010 | h [physique_bad] "Finally, a body that keeps up." | lesson prowess; risk +5; stress minor loss |
| tier1.011 *The Stare* | f [beauty_good] "Let them look. They always have." | +50 prestige; risk +2 |

**init.006 reach.**
- The initiation entry for The Prosthetic widens to `OR = { eotg_has_physical_loss = yes  has_trait = clubfooted  has_trait = hunchbacked }`, with `modifier = { factor = 0.5  eotg_has_physical_loss = no }`.
- init.006 gets `desc_congenital`, which **replaces** the base desc (lore M6). It is the first `triggered_desc` in the desc's `first_valid`, on `eotg_has_physical_loss = no`. The loss variants follow, unchanged.
- Optional (scripter's call): **b_congenital**, a variant of option b for a ruler with only a congenital trait. Key `eotg_aug_init.006.b_congenital`: "I have lived with it this long." Same effects as b; the option picks its `name` by `eotg_has_physical_loss`.
- **Wording rule (lore M6):** no init.006.f text, desc or tooltip may use "cure", "fix", "correct", "defect", "deformity" or "normal". The prosthesis is hardware that compensates. The f option's name follows the lore-keeper report.
- **Re-activation (ruling 2026-10-04).** Removing the prosthesis re-activates the masked trait.
  - init.006.f sets a permanent flag, `eotg_flag_aug_congenital_masked`, on root.
  - When the flag is set, `eotg_aug_remove_all_effect` (Remove Implants, Excision, Rejection failure) and both regression decisions (`eotg_decision_partial_removal`, `eotg_decision_overclock_regression`) run `make_trait_active` on whichever of `clubfooted` / `hunchbacked` is inactive, then remove the flag.
  - `make_trait_active` is the counterpart of vanilla `make_trait_inactive`. The scripter confirms it in PX `effects.log`.
- Options a, c and e gain `trigger = { eotg_has_physical_loss = yes }`, so a congenital-only ruler sees b, d and f.

**Vanilla precedent:**
- `make_trait_inactive` on a genetic trait: `events/trait_specific_events/trait_specific_events.txt:220` (`lunatic_genetic`).
- `clubfooted` and `hunchbacked` are `genetic = yes` (`00_traits.txt:8093`, `8127`).

**Pacing:** none.

**Risks:**
- The lunatic and possessed lines sit near the banned vocabulary. The lore-keeper cleared them with the M1 and M2 wording (§8 items 2–3).
- Training Yard reaches 8 options in total, but at most about 4 show for any one character.

---

### 5.10 Issue 10 — pacing and AI cost at the top

**Recommendation:**

**(a) AI-only nothing-weights** (exclusive tiers, same shape as §5.3):

| List | AI count | AI duke | AI king+ |
|---|---|---|---|
| Overclocked nothing (200) | ×3 | ×2 | ×1.5 |
| NF Storm nothing (40), Fracture nothing (60), Flicker nothing (60) | ×2.5 | ×1.75 | ×1.25 |

The existing Countdown ×2 stays and stacks multiplicatively. Accrual, drift, the cascade and the terminal are **not** throttled: only flavor is.

**(b) Countdown stage windows** (`eotg_story_aug_countdown` triggered effects 4–6):

| Stage | Today | After |
|---|---|---|
| .002 Lost Time | 60–69 | **60–67** |
| .003 Contradictory Memories | 70–74 | **68–76** |
| .004 Violence | ≥ 75 | **≥ 77** |

.001 stays at 50–59. The `eotg_last_stage` logic is unchanged.

**Vanilla precedent:** `yearly_on_actions.txt:3022-3030`; `mpo_on_actions_2.txt:468-474`.

**Pacing:**
- AI count Overclocked roll: from about 0.62 to about 0.35 events a year (typical eligible weight ~330). Duke about 0.45. Kings barely change.
- NF lists drop about 40% for AI counts.
- Calm accrual (12–15 a year) now lands in stage 3's 9-point window from about 9 of 12 start points (risk 56–64), against about 5 of 12 today.

**Risks:**
- AI counts at Storm see fewer Warrants and Regencies. At county tier this rarely touches the player.
- Stage 3 can still be jumped at high accrual (≥ 20 a year). That is accepted: "Stages can skip" (Phase 5 §1.2).

---

## 6. Vanilla precedent (consolidated)

All paths are under `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`.

| Mechanism | File:line | Used in |
|---|---|---|
| Decision that fires an event chain, with gold, a cooldown, AI by tier and `short_term_gold` potential | `common/decisions/00_lifestyle_decisions.txt:342` (`commission_epic_decision`) | §5.1 |
| `ai_check_interval_by_tier` with `factor = 0` `ai_will_do` | `common/decisions/00_artifact_decisions.txt:616` | §5.2 |
| Fast tiered checks | `common/decisions/00_dynasty_decisions.txt:14` | §5.2 |
| `ai_will_do` is a % per check; all tiers required | `ck3-modding/reference/common/decisions/_decisions.info:110, 143` | §5.2 |
| `custom_tooltip` trigger wrapper | `00_lifestyle_decisions.txt:527` | §5.1 |
| Tiered AI no-event throttle | `common/on_action/yearly_on_actions.txt:3022-3030` | §5.3, §5.10 |
| AI-only weight modifier | `common/on_action/dlc/mpo/mpo_on_actions_2.txt:468-474, 528-534` | §5.3, §5.10 |
| Ongoing income cost in a trait | `common/traits/00_traits.txt:5060/5067` (`profligate`) | §5.3 |
| Forced madness episode | `events/trait_specific_events/trait_specific_ongoing_events.txt:27` | §5.4 |
| Every option carries the cost | `events/stress_events/stress_threshold_events.txt` (:11, :25, :37) | §5.4 |
| `random` with a script-value chance | `events/activities/hunt_activity/hunt_events.txt:4196` | §5.4 |
| `show_as_tooltip` | `00_lifestyle_decisions.txt:395` | §5.4 |
| Toast | `events/activities/chariot_race_activity/chariot_ongoing_events_jp.txt:195-225` | §5.4 |
| Counter variable | `common/scripted_effects/00_debug_and_shortcut_effects.txt:6`; `00_artifact_decisions.txt:609` | §5.5 |
| Weighted outcome list | `events/health_events.txt:11686` | §5.5, §5.6 |
| Skill check against a fixed bar | `events/activities/chariot_race_activity/chariot_race_events.txt:1947` | §5.6 |
| Skill contest | `chariot_ongoing_events_jp.txt:195` | §5.6 |
| Skill ratings | `common/script_values/00_basic_values.txt:470-479` | §5.6 |
| Combat hooks; `every_side_knight` | `common/on_action/combat_on_actions.txt:12-14, 190, 523-525` | §5.7 |
| Group traits | `00_traits.txt:5426-5428` (lunatic), `:5495-5497` (possessed) | §5.9 |
| `make_trait_inactive` on a genetic trait (`make_trait_active` reverses it) | `events/trait_specific_events/trait_specific_events.txt:220` | §5.9 |
| Kinslayer from a deliberate killing | `common/scripted_effects/00_secret_effects.txt:433` | heir.006 |
| `debug_log` | `common/casus_belli_types/00_religious_war.txt:3363` | §9.2 |

**Deviations from vanilla, with reasons:**
1. The initiation throttle on AI counts is milder than vanilla's 95%. That list creates world state, not flavor.
2. Overrides apply through `hidden_effect` after a `show_as_tooltip`. Vanilla's forced episodes have one option instead. Here the choice the player made is part of the horror.

---

## 7. Loc surface (eotg-localizer)

File: `localization/english/eotg_augmentation_l_english.yml`. Rules: BOM, dot-form keys, bare `[x.GetName]`, one definition per key, no `replace/`. **No vanilla string needs a `replace/` override.**

**Decision (6):**
- `eotg_decision_aug_pursue_next_stage`, `_desc`, `_tooltip`, `_confirm`. Wording is in the lore-keeper report. `_confirm` is "Send for the surgeons" (recorded pick).
- `eotg_decision_aug_pursue_next_stage_settling_tt` ("The last work has not settled yet."; no countdown number needed);
- `eotg_decision_aug_pursue_next_stage_suppressed_tt`: "You resolved to wait before going any further." (lore M7).

**Desc variants:**
- `eotg_aug_tier1.002.desc_sought`, `eotg_aug_tier2.003.desc_sought`;
- `eotg_fracture.009.desc_misled` (fracture.011 reuses its existing `desc_none`: no new key, lore M4);
- `eotg_fracture.029.desc_embrace`;
- `eotg_aug_heir.001.desc_overclocked`, `eotg_aug_heir.001.desc_patient`;
- `eotg_aug_patron.006.desc_writeoff`, `eotg_aug_patron.003.desc_voice`;
- `eotg_aug_retinue.005.desc_fractured`, `eotg_aug_retinue.003.desc_voice`, `eotg_aug_retinue.004.desc_voice`;
- `eotg_aug_init.006.desc_congenital`;
- optional `eotg_aug_init.006.b_congenital`;
- `eotg_fracture.023.f_war` (lore M2).

**Override and reveal toasts:**
- `eotg_fracture.{019,023,016,024,025,006}.override_tt` (6);
- `eotg_fracture.009.misled_tt`;
- `eotg_fracture.015.b.tt` and `eotg_fracture.015.b.reveal_{confession,threat,devotion}` (4).

**Roll outcome descs** (each `<event>.<option>.success` / `.failure`, 2 per row, 14 rows; init.014.c reuses its existing outcome keys):
- init.007.a, init.010.a;
- tier1.002.a, tier1.013.b, tier1.018.c;
- tier2.004.b (replaces its two gamble keys if they exist), tier2.012.a (`.success_true`, `.success_false`, `.failure`);
- tier3.007.c, tier3.016.c, tier3.019.b, tier3.023.a;
- fracture.007.a, fracture.026.a;
- end.009.a and .c (3 outcome descs each: `.seamless`, `.death`, `.storm`; 6 keys);
- end.031.a.

**New option names:**
- fracture.003.f, .008.f, .009.f, .010.f, .010.g, .014.f, .016.f, .021.e, .022.f, .023.f;
- init.006.f; tier1.010.g, .010.h; tier1.011.f;
- patron.002.f; retinue.003.f.

**Changed text:**
- `trait_eotg_cybernetics_{1,2,3}_character_desc`: one clause on licenses and servicing (the upkeep; lore-keeper wording);
- `eotg_decision_aug_sedation_tooltip`: "each course works less well than the last", with no number;
- `eotg_decision_aug_embrace_cascade_tooltip`: no longer promises the outcome;
- `eotg_fracture.004.c`: unchanged text; it is now a zealous option.

**Approximately 96 keys:**
- the earlier ~95;
- minus `eotg_fracture.011.desc_misled` (not built: `desc_none` is reused);
- plus `eotg_fracture.023.f_war`;
- plus the optional `eotg_aug_init.006.b_congenital`.

---

## 8. Lore constraints

From index §5 (lore review 2026-10-03, binding) and `OLD PROJECT VERSION/docs/SETTING LORE` (the ERRATA block overrides the body).
1. **Voice register.** The voice is internal: precise, legible, *you, a half-second early*. The six override toasts and the three misleading descs show the implant **acting**, never speaking from somewhere. Never "whisper", "answers", "speaks from", "possess", "the Eye", "breach", "grip" as a metaphor, and so on (index §5.2).
2. **fracture.022.f [possessed]** must not use "possess", "possessed" or "possession" in its text. It also has **no `trait =` field**, so the vanilla icon and tooltip never put the word on screen (lore M1). Vanilla's `possessed` is temporal-lobe epilepsy (`00_traits.txt:5495` comment), so frame it as a small seizure. The event's shipped title is *We*.
3. **fracture.010.f and .023.f [lunatic].** The belief must stay internal or visual: a reflection, a war only they see. **Never an external voice, not even as the character's belief** (index §5.1). Cleared by the lore-keeper on 2026-10-04 with the M2 wording ("The rest of you are behind.").
4. **"Static", never "pressure"**, is the player word for the hidden resource (round 2 §3.2). Nothing quantifies risk.
5. **The Patron's syndicate:** Named once per story from the owner's `[syndicates]` list of canon syndicates; 'the syndicate' / 'the syndicate envoy' on later mentions. Reprisal P7 and U1 still bind: the name never appears with P7's ownership words, and the lien desc (`eotg_mod_aug_patron_clause_final_desc`) never names the syndicate. (Owner ruling 2026-10-05, CB-42; `cybernetics_v2_seller_names.md` §5.4.) The Pursue decision names the clinic of record, or reads 'a sanctioned clinic' when there is none (lore-keeper ruling 2026-10-05; `cybernetics_v2_seller_names.md`). The licensing authority stays unnamed (index §5.3).
6. **Self/personhood, never "humanity"** (Seamless outcomes in end.009). **No monotheistic invocations** (fracture.010.g mystic).
7. Firmware **licenses** in the trait desc are local servicing contracts, never a galactic or League authority. **No Galactic League exists at 866 AG.**
9. **Override toasts (lore M8):** the order is the ruler's own and has already been carried out. Banned: "took control", "seized", "against your will", "something", "it decided", "override", "risk", "static", any number, and naming the implant.
10. **Misleading paths (lore M3–M5):**
    - a misled desc replaces the base desc; it is never added to it;
    - a misled fracture.011 is indistinguishable from a genuine no-witness event;
    - a reveal fires only when the player was actually misled.
11. **Congenital (lore M6):** never "cure", "fix", "correct", "defect", "deformity" or "normal".
12. ~~**US spelling throughout** (license, honor, color) in all new and changed text.~~ **Superseded:** Canadian English (supersedes US spelling: owner ruling 2026-10-04, loc commit 4168bb8); e.g. licence (noun), honour, colour.
8. Congenital masking (init.006.f) is hardware compensation, not a cure. The genes pass on: `make_trait_inactive`.

Lore review complete (2026-10-04): must-fixes M1–M8 are applied above. The exact wording is in the lore-keeper's report, which goes to the localizer.

---

## 9. Definition of done

**0. Validation.** All three tools clean on the touched files, except the known-benign items in `CLAUDE.md` §Validation:
- Tiger 1.17.0;
- `docs/tools/px_lsp_diagnostics.js`;
- `docs/tools/px_vocab_check.py`.

Tiger may not know the `hegemony` tier key if it predates it. If it reports that key, QA classifies it against vanilla's own use (`00_artifact_decisions.txt:616`) before calling it real.

**Static (QA):**
1. `grep -rn "add_trait_xp" common events` matches only inside `eotg_aug_set_integration_effect`.
2. `grep -n "ai_check_interval = " common/decisions/eotg_augmentation_decisions.txt` returns nothing. All 13 decisions have `ai_check_interval_by_tier` with all six keys and `barony = 0`.
3. `eotg_decision_aug_pursue_next_stage` exists, has no `cost`, and fires only tier1.002 or tier2.003. Both `eotg_can_progress_to_*` triggers read `eotg_flag_aug_settling` and the dev-gate script values. No literal 20 or 35 remains in them.
4. The nothing entries of the initiation, tier-1, tier-2, Overclocked and three NF lists carry the `is_ai` tier modifiers in §5.3 and §5.10.
5. The NF drift block makes exactly one `eotg_add_fracture_risk` call with `AMOUNT = eotg_aug_nf_drift_value`. The script value has `min = 2`. The sedation decision increments `eotg_aug_sedation_courses`.
6. end.009 a and c contain no direct `eotg_aug_total_integration_effect` outside the roll.
7. The six override events use `show_as_tooltip` plus `hidden_effect`, with `random = { chance = eotg_aug_override_chance … }`. fracture.002.b is gated off in Storm. fracture.004.c is zealous-gated.
8. Every consumer stage in §5.6 (init.008, init.011, tier1.015, tier1.022, tier3.022, tier3.024) removes both `eotg_flag_aug_chain_edge` and `_strain`.
9. `on_combat_end_winner` and `on_combat_end_loser` are extended only via `on_actions = { eotg_on_combat_aug_knights }`.
10. QA audit 8 (coupling) passes on every touched event. No event `trigger` reads a cooldown or settle flag. `eotg_flag_aug_settling` is read only by triggers, `is_valid` and the on_action branches.
11. No new event ids exist (event count stays at 153: the 152 of v2 plus round 2's hidden heir.006).
12. Loc: every §7 key is defined once; BOM present; no `[scope:`; no number or "risk" in any new toast or tooltip.

### 9.1 In-game checks (human, temporary map)
1. An Augmented count with gold and capital development ≥ 15 sees Pursue the Next Stage greyed out with the settling tooltip, then valid 5 years after initiation. Taking it fires The Upgrade with the sought desc, and Integration reaches Enhanced at stage 3.
2. Console `add_trait_xp eotg_cybernetics 100` on an AI count with risk 60 and stress 250: within ~2 years the AI takes Downgrade Protocol or Maintenance. The observer log confirms which.
3. A Neurofractured count with console risk 45: across ~10 Fracture events, some calm choices are overridden. Each override shows its toast, and none shows a number.
4. A Neurofractured count with Sedation and Restraints, stress 0: risk still rises by at least 2 a year. A third Sedation course gives no relief.
5. Embrace the Cascade three times on copies of a save: the outcomes vary.
6. An augmented knight who fights a battle has a nonzero `eotg_aug_nr_battle_bonus` (console `get_variable` or the debug tooltip).

### 9.2 The 50-year observer run (round 2 §6.1), and what it must measure
**Run it after Part B1, before any further tuning.** If it is cheap, also run once on the current build as a baseline.

**Instrumentation.** The scripter builds it as a **throwaway sub-mod in the session scratchpad, never committed** and loaded after the main mod:
- global-variable counters, incremented by hooks on the events and decisions below;
- a census every 10 game years, written with `debug_log` to `game.log`.

**Setup:**
- observer mode on the temporary map, 50 years at max speed;
- **3 seeds**;
- save at years 10, 20, 30, 40 and 50.

**Measure:**
1. **Census.** Augmented rulers by tier (Augmented / Enhanced / Overclocked / Neurofractured / Seamless) as a share of all count-tier-and-above rulers, split by county, duchy and kingdom+ tier, at each checkpoint. Judged against HQ2.
2. **Flows per decade:**
   - initiations, by source: random list vs Seek;
   - progressions T1→T2 and T2→T3, by source: Pursue vs random offer;
   - cascades; terminal outcomes (death / Seamless / excision / abdication); non-ruler cascades.
3. **Timing:** median and inter-quartile years from initiation to Enhanced and to Overclocked, AI only, from logged dates. Target: the §5.1 AI rows, median 18–28 years.
4. **Decision usage:** AI takes of all 13 decisions per decade, per 10 eligible rulers. Every decision > 0. Regression share of AI Overclocked exits 35–65% (§5.2).
5. **Non-rulers:** augmented knights by tier, nr.006 count, median years from augmentation to cascade. Target: median 15–25 years (§5.7).
6. **Event volume:** events fired per AI ruler per year, by tier and title tier. Target: Overclocked counts ≤ 0.5 a year plus the Countdown; Neurofractured counts ≤ 0.4.
7. **Gold gate:** at each yearly pulse, the share of tier-1 and tier-2 AI rulers past settling and past the dev gate who fail `short_term_gold` for the Pursue decision. If > 70%, the costs are the lever.
8. **Dev gate:** at year 0 and year 30, the share of count-tier-and-above capitals with development ≥ 10 / 15 / 20 / 35. **This decides `eotg_aug_dev_gate_*`.**
9. **Neurofractured span:** years from cascade to the terminal; the share of Neurofractured rulers on Sedation; the course count at the terminal.
10. **Countdown:** the hit rate per stage, .001–.005. Stage 3 should be ≥ 60% of Countdowns that reach stage 4.
11. **Arcs:** Patron, Retinue and Heir's Arc starts and completions per decade. Heir's Arcs started at Overclocked.
12. **Performance:** game days per real minute at max speed, years 40–50, with and without the main mod. Flag any drop over 10%.

**Tuning rule after the run.** Change only:
- the script values in `eotg_augmentation_values.txt`;
- the `is_ai` nothing factors;
- `ai_will_do` numbers.

Make one change set per run, and rerun before touching event content.

---

## 10. Deferred

| Item | Why |
|---|---|
| A Seamless ongoing realm cost | Rejected (§5.5): the trait and its fallout already carry the cost; the roll removes the guarantee. |
| Restraint tolerance | The drift floor already prevents the pause. Add it only if the observer run shows Neurofractured spans over 25 years. |
| Augmented's +0.5 health | It is the other half of the freebie. Leave it until the run shows whether the income cost suffices; the track spec's totals stay otherwise. |
| A visible "years until settled" counter on the decision | It needs a variable-date loc function; the flag tooltip is enough for now. |
| AI throttle inside the Countdown story | At most 6 events per Overclocked lifetime, and stage 5 feeds AI regression context. Revisit if §9.2 item 6 fails. |
| Thin personality traits (chaste, fickle, impatient, lustful, gluttonous, temperate) | Not in round 2's issue list; a later content pass. |
| Kinslayer policy (M4), imprisonment consistency (M5/M6) | Round 2 §2, scripter batch A. If batch A needs the call: deliberate killings take vanilla `add_kinslayer_trait_or_nothing_effect`; involuntary episodes (picker victims in .002, .004, .016, .029, countdown.004) do not, because the implant chose the victim. Use `imprison_character_effect` everywhere (round 2's own fix). |
| The Clinic (Q10), Nikios content | As before (index Q10; invariant 9). |
| Battle hooks for rulers | Rulers already accrue +10 a year at war in the Overclocked check. |

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: After batch A (round 2 §7.1) lands, build Part B1 of `docs/specs/cybernetics_v2_balance.md` (§5.1, 5.2, 5.3, 5.5, 5.10 and the script-values file). Hand B1 to QA, then build the throwaway observer sub-mod (§9.2) for the human's 50-year run. Build Part B2 (§5.4, 5.6, 5.7, 5.8, 5.9); lore review is complete (M1–M8 applied), so B2 is not blocked.
- files: docs/specs/cybernetics_v2_balance.md
- needs-loc: §7 (~96 keys) using the lore-keeper report's exact wording; lore M1–M8 and Canadian English (supersedes US spelling: owner ruling 2026-10-04, loc commit 4168bb8) bind
- needs-lore: none (M1–M8 applied 2026-10-04; the localizer works from the lore-keeper report)
- needs-human: run the 50-year observer run (§9.2) after B1; in-game checks §9.1; the orchestrator adds `common/script_values/` to the CLAUDE.md placement table (HQ1 and HQ2 resolved 2026-10-04)
