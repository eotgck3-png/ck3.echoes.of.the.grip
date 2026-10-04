# Frontier v1: open questions to revisit

**Status:** written 2026-10-04, after the owner's answers to Q1, Q2, Q12 and the lore questions (recorded in `frontier_v1.md` §R).

Everything below is **still open**. Phase 1 is built on the **default** shown for each item, so each one can be changed later without touching the architecture. **Where to change it** names the file and key, so a change is local.

## A. Owner design questions (from spec §17)

| # | Question | Default built | Where to change it |
|---|---|---|---|
| Q3 | Should Invest be a decision, or only event options? | A decision: `eotg_decision_frontier_invest`, minor gold for +10 progress, once a year per Region | `common/decisions/eotg_frontier_decisions.txt` |
| Q4 | Pacing: about 5–8 years unsponsored and 4–5 sponsored to Settled. OK? | As stated | the base rates in `eotg_frontier_base_rate_value`; the bonuses in `common/script_values/eotg_frontier_values.txt` |
| Q5 | Does the sponsor's money go to the project, or to the holder? | To the project. It's spent, the holder gets nothing, and it gives +6 progress | `eotg_frontier_sponsor_pay_effect` |
| Q6 | One shared "New Settlement" modifier, or one per type? | One shared modifier (`eotg_frontier_mod_new_settlement`, 10 years) | `common/modifiers/eotg_frontier_modifiers.txt` |
| Q7 | Can Establish be taken while at war? | No (`is_valid`). War also adds strain | `eotg_decision_frontier_establish` |
| Q8 | Should there be a founder-change hook (`eotg_frontier_on_founder_changed`)? | No hook. The brief's 8 hooks only | `common/on_action/eotg_frontier_on_actions.txt` |
| Q9 | Does Withdraw drop every sponsorship at once, or one at a time? | All at once (a ruler can only sponsor one anyway, `eotg_frontier_can_sponsor`) | `eotg_decision_frontier_withdraw` |
| Q10 | Opinion modifiers between sponsor and holder: Phase 1 or Phase 2? | Phase 2. No opinion modifiers in Phase 1 | — |
| Q11 | Do AI frontiers appear only in Regions marked Unsettled? On the vanilla map, that means only after the debug decision | Yes | — (marking is the single entry `eotg_frontier_mark_unsettled_effect`) |
| Q13 (new) | Strain from an event choice needs a label so .005 can name it. Is a sixth cause, **Hardship**, OK alongside the five named ones? | Yes, `flag:hardship` | `eotg_frontier_add_strain_effect` callers; loc `eotg_frontier_cause_hardship` |
| Q14 (new) | Founder validity: alive, adult, not imprisoned, and either the Region's holder or living in the holder's realm. Is "in the holder's realm" right for "founder leaving"? | As stated | `eotg_frontier_founder_valid` |
| Q15 (new) | Should the player see how many Systems remain open in a Region ("2 Systems remain open")? Showing a count needs a script value in loc (UNVERIFIED). | Wording without a number: "Systems remain open for settlement here" | loc `eotg_frontier_mod_unsettled_desc` and the decision descs |
| Q16 (new) | Who is the settlers' leader created on a Settlement completion? | A courtier of the holder, with the holder's culture and faith by scope; not landed | `eotg_frontier_complete_settlement_effect` |

## B. Engine verification (from spec §16, for eotg-vanilla-scout on 1.20.0.3)

The owner's binding fallbacks are in spec §R. The three that decide the architecture come first.

| # | Question | Built as | Fallback if false |
|---|---|---|---|
| V1 | Do variables work on a **landed_title** scope? Do they persist through save/reload and a holder change? Test: mark the Region, start a project, save and reload, change the holder, kill the founder. | County-title variables | A story cycle holds the state. **Never on the founder.** |
| V8 | Can script create a holding in an empty barony slot (`set_holding_type`)? Who holds the new barony? | `set_holding_type` on the first province with `has_holding = no` | Every type gets +1 development and +10 control instead of a holding |
| V12 | Does `trigger_event = { on_action = x }` fire a custom on_action with root and saved scopes intact? | The 8 hooks as custom on_actions | Empty scripted effects. Never hard-code Greater Drift. |
| V2 | Can a global variable list hold title scopes? Exact names: `add_to_global_variable_list`, `remove_list_global_variable`, `every_in_global_list`, `ordered_in_global_list`, and a list-size trigger | As named | A global counter variable for the AI cap; the Sponsor pick via `every_county` (expensive) |
| V4 | `add_county_modifier` / `remove_county_modifier` / `has_county_modifier` on a county title; county modifier icon keys (V18) | As named, with icons from the vanilla county modifier set | — |
| V5 | Does `change_development_level` exist in 1.20 on a county? | Used for milestones and results | `change_development_progress`, or a modifier |
| V6 | `development_level` and `county_control` as triggers on a county | Used for the completion floors | — |
| V7 | `has_holding`, `every_county_province` / `random_county_province`, `title_province` | Used to find an open System | — |
| V9 | Granting a barony from script (no longer needed: the holding stays with the holder, Q12) | Not used | — |
| V10 | Is `debug_only = yes` valid in a decision's `is_shown`? | Used | A game rule, or a console flag (spec §8.5 B/C) |
| V11 | An "occupied" trigger for the Region's capital province | `is_occupied = yes` on `title_province` of the county capital | Drop the Occupation cause |
| V13 | `every_held_title` with `tier = tier_county`. Does `yearly_playable_pulse` reach every county holder? | Used | `every_realm_county` with a holder filter |
| V14 | `switch = { trigger = var:x flag:a = { } }` with flag values | Used for the type tables | An `if` / `else_if` chain |
| V15 | `random_ally` (AI sponsor candidates) | The liege first, then `random_ally` | The liege only |
| V16 | Title-targeted interactions (`target_type = title`) | Not used (decisions + .010) | — |
| V17 | Distance between a character and a county (Sponsor pick ordering) | Not used. The order is by the holder's opinion | — |
| V19 | Can `history/titles/` set a title variable (for marking Unsettled on the real map, after Gate 1)? | Not used in Phase 1 | An on_game_start effect over a data list |
| V20 | Is `common/great_projects/` DLC-gated? (deferral D6 only) | Not used | — |
| V21 | Is `primary_heir` of a **dead** sponsor readable from the yearly tick? | Used for the sponsor hand-off | The sponsor simply lapses |
| V22 | Are `minor_gold_value` and `medium_gold_value` usable from a county-scope effect, or must they go through `holder = { }`? | Always read inside the character scope | — |
| V23 (new) | `add_prestige`, `add_gold` and `remove_short_term_gold` / `add_gold = -x` for payments; `pay_short_term_gold`? | `add_gold` with a negative value for payments, inside an `if` that checks `gold >=` | — |
| V24 (new) | `send_interface_toast = { title = … left_icon = … }` shape for the sponsor and founder notices | As in the v2 cybernetics script | `custom_tooltip` inside a hidden event; not added |

## C. Lore (answered; recorded in spec §R)
Nothing is open. If the lore-keeper later finds a contradiction in the loc, add it here.
