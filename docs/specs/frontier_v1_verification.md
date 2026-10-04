# Frontier v1: local verification and fix list (for the cloud author)

**Branch verified:** `claude/frontier-v1-cloud` (based on bf7b3b8), checked out locally on 2026-10-04.

Three checks:
1. **Lore** (eotg-lore-keeper): this file, §1.
2. **QA:** Tiger, PX, eotg_lint, and code and state-machine review: §2 (pending).
3. **Engine:** the 24 checks, against vanilla 1.20.0.3 (eotg-vanilla-scout): §3 (pending).

Apply every MUST and SHOULD item on the same branch, re-run the tools, and push. Optional items are the owner's taste calls (§4).

---

## 1. Lore and register (eotg-lore-keeper)

**Verdict: canon is clean.**
- Nothing contradicts canon at 866.
- No named factions, no Void, no tech-ceiling breach.
- No medieval words.
- US spelling, no dashes, BOM present.
- Glossary used correctly (Region, System, Port, Bastion, Sanctum).

### MUST
- **N1. `eotg_decision_frontier_sponsor_desc`.** "gain a say in how it turns out" implies authority over another ruler's Region (LAW AT 866). Write instead: "Other rulers are trying to settle the open places of the galaxy. You could put your money behind one of them. It buys you no claim and no say, only a part in whether the venture succeeds."
- **N2. Settlement is not annexation.** The holder owns the Region the whole time.
  - `eotg_frontier_mod_new_settlement_desc` becomes "The Frontier here has become a permanent settlement. Its first years are busy ones."
  - `eotg_frontier.004.desc`: its last two sentences become "...The settlers write like people who intend to stay. [eotg_frontier_county.GetName] is no longer a Frontier."
- **P1. `eotg_frontier.003.desc_replace`.** "them" refers to a single, unscoped sponsor. Use: "\n\nThe Frontier already has a backer. Accepting would end that arrangement." Alternatively, save `scope:eotg_frontier_old_sponsor` in `immediate` and name them.

### SHOULD
- **I1. `.001.desc` when the candidate is root.** The decision sets the candidate to root if no courtier out-stewards the taker, which tells the player about themselves in the third person.
  - Split the desc with `first_valid` into:
    - opener: "[eotg_frontier_county.GetName] has never been properly settled. Its Systems are open: rock and ice, a few hardy families, signals nobody has answered in years."
    - `_other`: "\n\n[eotg_frontier_candidate.GetFirstName] has looked over the surveys and thinks it can be done. The question is what we build first."
    - `_self`: "\n\nYou have looked over the surveys yourself, and it can be done. The question is what we build first."
  - `.001.start_tt` gets the same: when founder = root, "...with you leading the work."
- **I2. `.004.desc_settlement/_trade/_military/_religious` promise a holding.** If no barony slot is free, §5.3 gives development and control instead (V8 fallback). Use wording that is true either way (option B):
  - settlement: "\n\nThe settlers have built homes, berths and a market, and they have already chosen someone to speak for them."
  - trade: "\n\nShips that used to pass through now stop. The trading post has become a real port of call."
  - military: "\n\nThe garrison has dug in for good, and the approaches to the Region are watched day and night."
  - religious: "\n\nThe mission has put down roots, and the faithful have made the place their own."
- **I3. The backer pays by arrangement, not on request.** The script takes the gold without the backer choosing.
  - `.002.c` "Call on our backing. This is what it is for."
  - `.005.d` "Call on our backer for everything the arrangement allows."
  - `.005.sponsor_tt` "Under the arrangement, the backer pays double, and the pressure on the Frontier eases a great deal."
- **I4. `.005.desc_low_control`** becomes "\n\nYour officials never had much hold out here, and the settlers stopped looking to them."
- **I5. `.004.desc_mining`** becomes "\n\nThe mines are running steadily, and the ore is paying its way." (once Settled, there is no next stage)
- **I6. `.010.desc`** becomes "Other rulers are trying to settle open Regions, and some could use a backer. Whichever you choose, its holder will decide whether to take your money."
- **R1. `.004.a`** becomes "Pay [eotg_frontier_founder.GetFirstName] well, for all of it." ("a purse" is court language)
- **R2. `eotg_frontier_mod_unsettled_desc`** becomes "No permanent settlement has taken hold here yet. Systems remain open for settlement, along with whatever earlier travelers left behind." (passive "recognized" implies a registry)

### OPTIONAL (owner's taste, §4)
- **R3. `.003.desc`:** "The offer comes with no claim attached. If the Frontier succeeds, [eotg_frontier_sponsor.GetSheHe] will share the credit. If it fails, the loss."
- **S1.** "A Hard Season" becomes "A Hard Year" (`eotg_frontier_mod_hard_season` and `.002.t`).
- **S2. Exodus flavor.** In `.001.desc`, add "Exodus stragglers who never moved on". In `.004.desc_settlement`, open with "Exodus families and settlers from nearer systems…". Keep it generic and name no source polity.

---

## 2. QA (eotg-qa, Tiger + PX + lint + code and state-machine review)

**Verdict: FAIL, 1 blocker.**
- Tiger: 0 errors and 7 warnings in `eotg_frontier_*` (the warnings are the missing `_tooltip` loc below).
- PX: nothing in Frontier files.
- eotg_lint: 0 in Frontier files.
- Every invariant is clean: prefixes, no map keys, additive `yearly_playable_pulse`, cooldown authority, all 6 events fired and coupled, `debug_only` gates.
- No permanently stuck state.

Vanilla-confirmed during QA:
- `debug_only = yes` (test_decision.txt:9);
- the empty-slot holding build (01_dlc_fp1_scripted_effects.txt:519-530) and the grant (hold_court_events_general.txt:6873-6890);
- title-scope `set_variable` (00_major_decisions_scripted_effects_3.txt:1100). Persistence across a holder change still needs the in-game test.

### MUST (blocker)
- **Q-B1. Options and resolution effects never re-check the Region's state.**
  - **How it breaks:**
    - Establish has no cooldown, so .001 can be open twice and start the same Region twice (double cost, `active_count` +2, list entry twice).
    - .004 or .005 left open past the next tick re-fires.
    - Abandon while .004/.005 is open resolves a Region that is no longer a Frontier, so the second complete/abandon builds another holding, decrements the count again, and reads removed variables (error.log).
  - **Fix both:**
    1. Add `scope:eotg_frontier_county = { eotg_frontier_can_establish = yes }` to each .001 type option's trigger, and `eotg_frontier_is_frontier = yes` to the .002–.005 options. Also guard the bodies of start, complete and abandon with the matching state `limit`.
    2. Remove the second source of truth. Drop `eotg_frontier_active_count`, and make `eotg_frontier_ai_room` read `NOT = { any_in_global_list = { variable = eotg_frontier_active count >= eotg_frontier_ai_cap_value } }` (the `count` form is vanilla: yearly_on_actions.txt:846).
  - **Where:** events.txt:62-166, 509-553, 618-693; decisions.txt:302-316; effects.txt:70-86, 452-495, 590-615.

### SHOULD
- **Q1.** Seven decisions have no `<decision>_tooltip` loc (decisions.txt:20, 105, 181, 225, 285, 339, 384), so they show raw keys. Add them, matching the augmentation pattern.
- **Q2. Saved scopes leak within a pulse and across counties.**
  - In a tick, a failed sponsor payment saves `scope:eotg_frontier_old_sponsor` (effects.txt:144), and a .003 fired in the same pulse inherits it. The lapsed sponsor then gets the wrong toast, and the `sponsor_changed` hook gets the wrong old_sponsor.
  - `save_hook_scopes` (effects.txt:30-40) leaves the previous county's sponsor and founder in place when a variable is absent.
  - **Fix:**
    - add `else = { clear_saved_scope = … }` in `save_hook_scopes` and `find_sponsor_candidate`;
    - clear `old_sponsor` at the start of `set_sponsor` and `tick_effect`;
    - use `save_temporary_scope_as` for internal scopes (`_holder`, `_change`, `_heir_sponsor`, `_lapsed_sponsor`, `_sponsor_candidate`).
- **Q3. Founder validity on a holder change** (triggers.txt:56-68). When the founder-holder grants the Region to a vassal, the founder becomes the new holder's liege and turns invalid, so No Founder strain starts and an AI holder silently replaces them. **Orchestrator ruling:** the founder stays valid if alive, adult and free, and any of these holds:
  - they are the holder;
  - they are in the holder's realm (employer or vassal-or-below);
  - **the holder is vassal-or-below of the founder.**
  Update spec §2.5/§12.6 and the test plan to match.
- **Q4. Completion floors can stall silently** (values.txt:52-64). Trade, Research and Administrative need development 3, but milestones give only +2, so a dev-0 Region sits at 100 progress indefinitely. **Orchestrator ruling:**
  - (a) make each floor relative: `min(type floor, starting development + 2)`, recording `var:eotg_frontier_start_dev` at start;
  - (b) the stage modifier / Invest tooltip says what completion is waiting on (e.g. "Waiting on development") when progress is full but the floor isn't met.
- **Q5. A development-farming loop:** start → 66 (+2 dev) → Abandon (−1 only) → resettle. **Orchestrator ruling:** milestone development is granted once per Region, ever. Record the milestones reached in the Region's permanent history, and skip any already granted on later attempts. Abandon keeps its −1.
- **Q6.** `eotg_decision_frontier_establish_effect_tt` says "your least settled Region", but the script picks the highest development. Fix the loc to say what the script does.
- **Q7.** .010's desc doesn't name each offer's stage (spec §9). Add stage words per offer.
- **Q8. The hook contract drifts from spec §7:**
  - `on_project_progressed` fires on zero or clamped gain; fire only when gain > 0;
  - `on_development_changed` fires for Military even when a holding was built;
  - `on_settled` and `on_abandoned` bypass `fire_hook_effect`.
  Make all of them match §7.
- **Q9. Tick window.** The 300-day `eotg_frontier_ticked` (on_actions.txt:31) allows two ticks in about 12 months across holders. **Orchestrator ruling:** use a calendar-year marker, e.g. store `current_year` and skip when equal, so there is exactly one tick per in-game year.

### Notes (fix in passing)
- modifiers.txt:58: the comment says `hard_season` comes from .002 option a; it's option b.
- decisions.txt:338: the path should be `docs/specs/frontier_v1_test_plan.md`.
- `..._debug_mark_unsettled_valid_tt` says "no Frontier history yet", but a settled Region passes. Reword it, or check history.
- AI-to-AI sponsor offers skip the sponsor's 4× gold `ai_potential` gate (spec §8.4, effects.txt:401-419). Apply it.
- `create_title_and_vassal_change` is called in barony scope (effects.txt:517); vanilla calls it at character scope. Move it, or mark it for the V8 in-game check.
- .001 third-person candidate: see §1 I1.

### Test plan fixes (`docs/specs/frontier_v1_test_plan.md`)
- **§0.4-5:** kill the founder BEFORE granting the Region away, or check for the .002 variant. With the Q3 ruling, granting no longer invalidates the founder.
- **§1:** the debug decision marks only the capital, and only with no state. Give the console line for marking another county, and say "finish or abandon one Region before marking the next".
- **§4.2:** add setup for an AI liege or ally who passes `can_sponsor`.
- **Readout:** strain is invisible. Optionally add a `debug_only` decision or tooltip that prints progress, strain and the floors. That's new script, but debug-only, and it is APPROVED as test tooling.


## 3. Engine checks V1–V24 (eotg-vanilla-scout, vanilla 1.20.0.3 + PX engine dump)

**Verdict:**
- Nothing the Frontier code calls is missing from 1.20 (`px_vocab_check`: 0 findings).
- Two items are WRONG as designed, and one guard is missing.
- Three behaviours need in-game tests.

**CONFIRMED** (drop the `UNVERIFIED-VANILLA` markers, citing the file in the comment if useful):

| Check | Feature | Vanilla evidence |
|---|---|---|
| V1 | `c_` title variables: set, read and remove from character scope | province_on_actions.txt:904; ep3_decisions.txt:1531; 00_tribal_interactions.txt:154 |
| V2 | global title lists, with the exact names used | game_start.txt:200; 00_major_decisions_scripted_effects.txt:3545; 00_legends.txt:40-46; 06_ep3_laamp_interactions.txt:1949 |
| V4 | county modifiers, including the timed `years =` form | |
| V5 | `change_development_level`, negatives included | mpo_decisions.txt:6887 |
| V6 | the `development_level` / `county_control` triggers | |
| V7 | `has_holding`, `random_county_province`, `title_province` | |
| V8 | `set_holding_type` on an empty province (but see fix 1) | 00_decisions_effects.txt:1347 |
| V10 | `debug_only` (debug mode only) | |
| V11 | `is_occupied` | |
| V12 | `trigger_event = { on_action = x }` | |
| V13 | `every_held_title` with `tier_county`; `yearly_playable_pulse` reaches every county holder | |
| V14 | `switch` on `var:` with flag values | |
| V15 | `random_ally` | |
| V18 | the icon keys | |
| V19 | `history/titles` variables (on a duchy) | |
| V23 | negative `add_gold`, `remove_short_term_gold` | |
| V24 | `send_interface_toast` with `title` + `left_icon` | |
| extra | `clamp_variable`; `set_variable` with `years =` | |

The decision picture `decision_realm.dds` and `theme = realm` exist.

### MUST
- **E1. `eotg_frontier_build_holding_effect`** (effects.txt ~499-530): add `barony_cannot_construct_holding = no` to BOTH the outer `any_county_province` limit and the `random_county_province` limit. Vanilla puts it in every empty-slot picker. Without it, the outer check can pass while the pick matches nothing, so nothing is built AND the development/control fallback is skipped. Keep the guarded `change_title_holder` block.
- **E2. Dead sponsor hand-off (V21): WRONG as designed.** `primary_heir` of a dead character is read only in `on_death` in vanilla (death.txt:31-51); a year later it's almost certainly empty, so the hand-off never works.
  - Move it to an additive `on_death = { on_actions = { eotg_frontier_on_sponsor_death } }`. In that on_action's effect, root is the dying character: if `has_variable = eotg_frontier_sponsoring`, run the hand-off on `var:eotg_frontier_sponsoring` using `primary_heir`.
  - Keep the yearly check only as the lapse fallback.
- **E3. V22:** `minor_gold_value` / `medium_gold_value` (01_dynamic_values.txt:53) read character triggers. They must only ever be evaluated inside a character scope (`holder = { }` or `var:sponsor = { }`). The current code does this; make sure no fix moves them to county scope.

### SHOULD
- **E4. V10:** the debug decisions only show in debug mode. That's fine (the owner's testing guide requires `-debug_mode`). Say so in the test plan.
- **E5. V12:** if saved scopes don't carry into the custom on_actions (BEHAVIOUR), fall back to the spec's empty scripted effects. Keep the fallback documented next to `fire_hook_effect`.
- **E6. Markers:** CONFIRMED items lose `UNVERIFIED-VANILLA`. The three behaviours below get `# TEST-IN-GAME: <what>` instead.

### In-game tests (add to `frontier_v1_test_plan.md` §0)
1. A county variable survives save, reload and a holder change (V1).
2. `set_holding_type` on a `holding = none` province: does a barony appear, and who holds it (V8)?
3. Do saved scopes reach the custom on_actions (V12)?


## 4. Owner decisions (2026-10-04)
- **Q3–Q16:** the built defaults are ACCEPTED, with one change. **Q4 pacing is DOUBLED:** about 10–16 years unsponsored and about 8–10 sponsored to Settled.
  - Scale the base rates and bonuses in `common/script_values/eotg_frontier_values.txt` (`eotg_frontier_base_rate_value` and the related values).
  - Re-check every time-based strain, failure or abandonment threshold so they don't fire twice as often relative to progress. Strain over a 2× longer project must stay proportionate.
  - Update the spec's pacing section and `frontier_v1_open_questions.md`.
- **Optional lore items.** Owner rule: "whatever makes the most sense that can apply in any time period in the setting".
  - **S1 APPLY:** "A Hard Year" (a year is time-neutral; a season is planetary).
  - **R3 APPLY:** the sponsor line "no claim attached… share the credit… the loss" (timeless).
  - **S2 DO NOT APPLY:** the Exodus is a specific era (ongoing at 866, not forever). Frontier text must read true in any period of the setting.
  - **Standing rule for all Frontier text:** time-neutral. No era-specific events, dates or factions.
