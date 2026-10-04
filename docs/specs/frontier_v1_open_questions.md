# Frontier v1: open questions, now decided

**Status:**
- Written 2026-10-04, after the owner's answers to Q1, Q2, Q12 and the lore questions (`frontier_v1.md` §R).
- **Updated the same day** with the owner's decisions and the local verification ([`frontier_v1_verification.md`](frontier_v1_verification.md) §2–§4; applied in `frontier_v1.md` §V).

**Where to change it** names the file and key, so any later change is local.

## A. Owner design questions (spec §17): DECIDED 2026-10-04

**The owner accepted every built default, with one change: Q4, pacing doubled.**

| # | Question | Decision (as built) | Where to change it |
|---|---|---|---|
| Q3 | Should Invest be a decision, or only event options? | **Accepted.** A decision: minor gold for **+5** progress (halved with the pacing), once a year per Region | `common/decisions/eotg_frontier_decisions.txt` |
| Q4 | Pacing to Settled | **Doubled:** about 10–16 years unsponsored, 8–10 sponsored. The sum of the yearly inputs is × `eotg_frontier_pace_value` (0.5). Strain rescaled to 0–8 (failure at `eotg_frontier_strain_fail_value`) | `common/script_values/eotg_frontier_values.txt` |
| Q5 | Does the sponsor's money go to the project or the holder? | **Accepted.** To the project. It is spent and gives the sponsor bonus to the yearly gain | `eotg_frontier_sponsor_pay_effect` |
| Q6 | One shared "New Settlement" modifier, or one per type? | **Accepted.** One shared modifier (10 years) | `common/modifiers/eotg_frontier_modifiers.txt` |
| Q7 | Can Establish be taken while at war? | **Accepted.** No; war also adds strain | `eotg_decision_frontier_establish` |
| Q8 | Should there be a founder-change hook? | **Accepted.** No; the brief's 8 hooks only | `common/on_action/eotg_frontier_on_actions.txt` |
| Q9 | Does Withdraw drop every sponsorship at once? | **Accepted.** A ruler sponsors one at a time, so Withdraw ends that one | `eotg_decision_frontier_withdraw` |
| Q10 | Opinion modifiers between sponsor and holder | **Accepted.** Phase 2 | — |
| Q11 | AI Frontiers only in Regions marked Unsettled | **Accepted.** Yes | `eotg_frontier_mark_unsettled_effect` |
| Q13 | A sixth strain cause, **Hardship** (from an event choice) | **Accepted.** `flag:hardship` | `eotg_frontier_add_strain_effect` callers; loc `eotg_frontier.005.desc_hardship` |
| Q14 | Founder validity | **Accepted, then widened by the orchestrator ruling (verification Q3):** alive, adult and free, plus one of: is the holder; is in the holder's realm; **or the holder is vassal or below of the founder** | `eotg_frontier_has_valid_founder` |
| Q15 | Show a count of open Systems? | **Accepted.** Wording without a number | loc `eotg_frontier_mod_unsettled_desc` |
| Q16 | The settlers' leader on a Settlement completion | **Accepted.** A courtier of the holder, culture and faith by scope, not landed | `eotg_frontier_create_leader_effect` |

## A2. Orchestrator rulings from the verification (applied)

| Verification item | Ruling | Where |
|---|---|---|
| Q3 | The founder stays valid when the holder is vassal or below of the founder | `eotg_frontier_has_valid_founder` |
| Q4 | Relative development floor: `min(type floor, starting development + milestone development not yet granted)`. "Waiting on development / control" shows as the stage modifier and in the Invest tooltip | `eotg_frontier_min_dev_value`, `eotg_frontier_dev_reachable_value`, `eotg_frontier_mod_waiting_*`, `eotg_decision_frontier_invest_waiting_tt` |
| Q5 | Milestone development is granted once per Region, ever (permanent `eotg_frontier_dev_granted`); Abandon keeps its −1 | `eotg_frontier_grant_milestone_dev_effect` |
| Q9 | A calendar-year tick marker (`eotg_frontier_tick_year = current_year`) | `eotg_on_yearly_frontier_tick` |

## B. Engine verification (spec §16): RESOLVED by eotg-vanilla-scout, 2026-10-04

**Confirmed against vanilla 1.20.0.3:** V1 (title variables), V2, V4, V5, V6, V7, V8 (the effect), V10, V11, V12 (the effect), V13, V14, V15, V18, V19, V23, V24, `clamp_variable`, timed variables. The markers are dropped in script.

**Wrong as designed, now fixed:**
- **V21 / E2:** `primary_heir` of a dead character is readable only in `on_death`. `eotg_frontier_on_sponsor_death` (additive `on_death`) records the heir on the Region (`eotg_frontier_pending_heir`) and clears the sponsor; the next yearly tick hands the backing on or records the lapse (orchestrator ruling, follow-up: in `on_death` the heir has usually not inherited yet).
- **E1:** `barony_cannot_construct_holding = no` added to the empty-slot check and pick.
- **E3:** gold values are only read in a character scope (unchanged, checked).

**TEST-IN-GAME** (in `frontier_v1_test_plan.md` §0):
1. A county variable survives save, reload and a holder change (V1).
2. `set_holding_type` on an empty province: does a barony appear, and who holds it (V8)?
3. Do saved scopes reach the custom on_actions (V12)?

**New in the fix pass, since confirmed against vanilla 1.20.0.3 (markers dropped):**
- `current_year` as a set_variable value (game_start.txt:987-991). The comparison is written vanilla's way, `current_year > var:eotg_frontier_tick_year` (00_empire_faith_gate_triggers.txt:234, yearly_on_actions.txt:546);
- `development_level` / `county_control` as values in county scope (03_dlc_fp2_script_values.txt:88-91; 09_mpo_wars.txt:1335);
- `[x.MakeScope.Var('name').GetValue|0]` in the debug readout's loc (coronation_activity_l_english.yml:675, 817).

**Follow-up owner decision:** the flavor-event cooldown is **3 years** (`eotg_frontier_event_roll_effect`), about 4–5 events per typical project at most.

**Not used:** V9 (barony grant from script: the holding stays with the holder), V16, V17, V20, V22 (n/a).
