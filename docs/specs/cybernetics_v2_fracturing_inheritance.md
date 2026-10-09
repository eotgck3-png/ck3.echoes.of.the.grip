# Spec: Cybernetics v2: *A Fracturing Inheritance* (the Neurofractured heir)

**Author:** eotg-architect, 2026-10-06
**Authorized by:** the owner, relayed by the coordinator on 2026-10-06. The request was for a branching tree in which a landed character learns that their heir has become Neurofractured. It must have at least 10 final outcomes, and three are required: the heir kills the character, the heir massacres the court, and the heir murders the next two in line. An addition the same day asked for variation: a profile rolled and stored at entry that changes which events fire, which options appear and the outcome odds, plus desc variants per profile.
**Lore review:** eotg-lore-keeper, 2026-10-06: CHANGES REQUIRED, wording and framing only; the structure passed canon. All items applied in this revision (§3.4; §5.3 .011, .012, .016, .019, .025, .027; §7.1; §10).
**Owner rulings:** §11 Q1–Q5 ruled 2026-10-06. Q5 changed the design: **only a player ruler gets the tree; AI-only occurrences resolve in one hidden event (§5.5).**
**Builds on:** [cybernetics_v2.md](cybernetics_v2.md) (index; its §1 rules and §5 register bind this file), [phase 3](cybernetics_v2_phase3.md) (Neurofractured, the Heir's Arc, Excision, abdication), [phase 6](cybernetics_v2_phase6.md) (non-ruler cascade), [new beats](cybernetics_v2_new_beats.md) §5.1 (Heir's Arc round 2), [balance](cybernetics_v2_balance.md) §5.2 and §5.10 (AI pacing).
**Writing rules:** `docs/qa/event_writing_review_2026-10-05.md` and `docs/proposals/gemini_rewrite_feedback_2026-10-06.md` §2–§4.

The design is in §5 (the tree) and §5A (variation). The other sections follow the architect template.

**Build deltas (2026-10-08).** These are QA fixes to the build, folded back into the spec so the spec states what ships:
1. **Line pick, places 1–6.** The succession-line pick covers places 1–6 through one script value, `eotg_aug_inherit_line_places = { value = 6 }`. Both the pick and `eotg_aug_inherit_line_eligible` read it. Before, the window was "1–5" in some places and `value <= 3` in the spec. It walks exact places, lowest first, not a weighted random heir (§3.2, §5.4.1, §9 V-13).
2. **Players skipped on both paths** (orchestrator ruling). `is_ai = yes` is in `eotg_aug_inherit_line_eligible` and in `eotg_aug_inherit_line_slot_effect`, so L13 never kills a player, on the tree or on the AI path. A side effect: `eotg_inh_second` can no longer be a player (§5.3 .005, §5.4.1, §5.5.4, DoD 12).
3. **.028 re-checks `eotg_aug_inherit_tree_runs = no`** in its trigger. If the ruler became a player during the delay and the chain is still valid, `on_trigger_fail` fires .001; otherwise it closes the chain (§5.5.1, §5.5.2, §5.5.4).
4. **OR-gated options stack `trait =` lines**, one per gating trait (vanilla `harm_events.txt` harm.0551.b). Scripter deviation 10 (one icon per OR-gated option) is **reversed**. This is the spec's rule from now on (§6 Deviations).
5. **.013.vc has `add_dread = 20`**, matching .009.e (§5.3 .013).
6. **Excision odds, self table, revised** after a lore-keeper flag. The ruler's own hands are no longer safer than the physician's table: 45 / 30 / 25, or 30 / 30 / 40 with `lifestyle_physician` (§5.4.3). **Applied.** Back-street table also corrected to 50 / 40 / 10 so the column sums to 100 (orchestrator ruling, §5.4.3).

**Build deltas (2026-10-09, event quality B10).** W5 re-gating, folded back into the spec (§5.3 node table):
7. **.001.e** is gated `highest_held_title_tier >= tier_duchy`, with no icon. AI base 10, −20 compassionate, −20 trusting; callous and paranoid keep +20 each. They are stress responses only, not gates.
8. **.009.d** is gated `education_martial` with `skill = martial`. AI +20 / +30 / +30 on education_martial_3 / _4 / _5, and brave +10 as a response. The text becomes "Choose the ground. If it comes for me, it meets me there."
9. **.027.c** gives the `just` stress relief only when there is no leave (`scope:eotg_inh_leave` absent). The scripter is applying this fix now.

---

## 1. Purpose & gate

The existing Neurofractured content is about a ruler who is breaking while the heir watches (the Heir's Arc, T3). This tree is the mirror image: **the ruler is sound and the heir is breaking**, and the ruler must decide what the dynasty does about it. Choices branch over 3–5 events into **17 final outcomes**, from a clean excision to the heir killing the ruler. **The tree is for player rulers** (owner Q5). When the ruler is AI, one hidden event picks an outcome by weighted roll and applies the same outcome effects, so the world sees the same results without the event cost (§5.5). When the tree starts, a **profile** is rolled and stored: how the heir's Neurofracture shows, and what the heir is to the ruler. The profile decides which middle events can fire, which options show, and the odds of every hidden roll, so two playthroughs don't read alike.

**Gate 3 (Systems), built against the temporary map** under `docs/agent_workflow.md` §5 rule 2. **Not blocked.** It is map-agnostic: it uses no title, province, culture, faith or character keys. The line of succession is read only through the ruler's `primary_title` and vanilla iterators.

This is **new events**, requested by the owner (memory rule "event expansion is the user's call": satisfied, since the owner asked).

---

## 2. Signature resource

**The heir's `eotg_fracture_risk`**, read as pressure (phase 3). The variable is hidden, runs 0–100, and is already on every Neurofractured character. A Neurofractured non-ruler drifts +6 a year (`eotg_on_yearly_aug_nonruler_check` step 4).

The tree couples to it as follows. QA audit 8 checks the column "Resource" in §5.3.
- **Moves.** Every non-terminal event has at least one option that calls `scope:eotg_inh_heir = { eotg_add_fracture_risk = { AMOUNT = n } }`. Calm, contained or loved heirs go down. Watched, cornered or rejected heirs go up.
- **Reads.** The heir's band (`eotg_aug_pressure_flicker` / `_fracture` / `_storm`, evaluated **in the heir's scope**) picks desc variants (.003, .022) and weights every violent roll (§5A.3). An heir who has been made worse along the way is more dangerous at the end.
- **Tier changes.** These count as coupling (index §1 rule 4): heir excised (.021), heir dead (.016–.019, .021, .027, L17), and the ruler cascading by choice (.020).

The ruler's own risk moves only in .020 (the ruler must already be Overclocked). **Hidden-risk rule (index §1 rule 3):** no tooltip, toast or desc shows a number, "risk", "pressure" or odds. The surgery odds are given in words, as end.001 does.

---

## 3. Identifier table

Namespace **`eotg_aug_inherit`**. Event ids `eotg_aug_inherit.001`–`.027`. Loc keys use the **dot form** (`eotg_aug_inherit.001.t / .desc_rage / .a`), per index §0 "Loc key form": the whole cybernetics tree is dot-form, so this file does not switch to `_NNNN_t`.

### 3.1 New: events (28)

| Id | Working title | Fired to | Kind |
|---|---|---|---|
| .001 | The Report | ruler | entry, choice |
| .002 | The Conversation | ruler | choice |
| .003 | The Physicians | ruler | choice (refused variant) |
| .004 | The Watch | ruler | choice |
| .005 | The Council | ruler | choice |
| .006 | The Terms | ruler | choice (accept / refuse variant) |
| .007 | The Answer | ruler | choice (accept / refuse variant) |
| .008 | The Ward | ruler | choice |
| .009 | The Pattern | ruler | choice, danger hub |
| .010 | The Table | ruler | choice → surgery |
| .011 | Passage Out | ruler | choice → **leaf L6** |
| .012 | The Shuttle That Never Docked | ruler | choice → **leaf L8** |
| .013 | Struck from the Line | ruler | outcome + choice (3 reactions) |
| .014 | The Hand-Off | ruler | choice → **leaves L9, L10** |
| .015 | The Offer | ruler | choice |
| .016 | The List | ruler | **leaf L13 (required)** |
| .017 | The Long Watch | ruler | **leaf L14 (required)** |
| .018 | The Last Audience | ruler | **leaf L15 (required)** or → .024 |
| .019 | The Quiet Room | ruler | **leaf L12** |
| .020 | Two Machines | ruler | **leaf L16** |
| .021 | After the Table | ruler | **leaves L1, L2, L3** |
| .022 | Kept Terms | ruler | **leaf L4** |
| .023 | The Locked Wing | ruler | **leaf L5** |
| .024 | Still Breathing | ruler | after a failed attempt on the ruler → L17 / L5 / L4 |
| .025 | The Seat | the heir, now ruler | aftermath of L15 |
| .026 | The Warden's Hand | the heir, now ruler | aftermath of L9 / L10 |
| .027 | The Line Shortens | ruler | **leaf L11** |
| .028 | (hidden) Resolution | **AI** ruler | `hidden = yes`; the whole tree as one weighted roll (§5.5) |

### 3.2 New: script

| Key | Type | File | Purpose |
|---|---|---|---|
| `eotg_on_yearly_aug_inherit_check` | custom on_action | `common/on_action/eotg_augmentation_on_actions.txt` | entry; cooldown authority (§5.1) |
| `eotg_aug_inherit_can_start` | scripted trigger (ruler scope) | `common/scripted_triggers/eotg_augmentation_triggers.txt` | entry gate, shared by both firing sites |
| `eotg_aug_inherit_tree_runs` | scripted trigger (ruler scope) | same | `is_ai = no`. Picks the tree or .028 (§5.5.1). One trigger, so widening it later is a one-line change. |
| `eotg_aug_inherit_heir_candidate` | scripted trigger (heir scope; param `RULER`) | same | the heir half of the gate |
| `eotg_aug_inherit_chain_valid` | scripted trigger (ruler scope) | same | world-state guard for every node: `var:eotg_inh_heir` exists and is alive. Nodes before a leaf also need the heir to be Neurofractured and still at root's court. **Reads no cooldown flag.** |
| `eotg_aug_inherit_start_effect` (param `SOURCE` = `report` / `cascade`) | scripted effect | `common/scripted_effects/eotg_augmentation_effects.txt` | sets the cooldown and active marker, rolls the profile and bond, picks the witness, fires .001 |
| `eotg_aug_inherit_scopes_effect` | scripted effect | same | run first in every `immediate`. Saves `scope:eotg_inh_heir`, `eotg_inh_witness`, `eotg_inh_second` and `eotg_inh_councillor` from the variables and live links. |
| `eotg_aug_inherit_close_effect` | scripted effect | same | runs at every leaf and in every `on_trigger_fail`. Removes the chain variables and flags, but keeps the heir's `eotg_flag_aug_inh_seen` and the ruler's cooldown. |
| `eotg_aug_inherit_roll_threat_effect` | scripted effect | same | sets `var:eotg_inh_threat` from the §5A.3 weights, unless already set |
| `eotg_aug_inherit_fire_threat_effect` (param `DAYS_MIN`, `DAYS_MAX`) | scripted effect | same | fires .016 / .017 / .018 / .019 by `var:eotg_inh_threat`, with the fallbacks in §5.4 |
| `eotg_aug_inherit_pick_line_effect` | scripted effect | same | saves `eotg_inh_next_1` and `eotg_inh_next_2`, the first two eligible people in places 1–6 of the line who are not the heir (§5.4.1) |
| `eotg_aug_inherit_line_slot_effect` (param `PLACE`) | scripted effect (title scope) | same | one exact place of the line; requires `is_ai = yes` (§5.4.1; build delta 2026-10-08) |
| `eotg_aug_inherit_line_eligible` | scripted trigger (ruler scope) | `common/scripted_triggers/eotg_augmentation_triggers.txt` | someone other than the heir and the ruler, `is_ai = yes`, stands in places 1–6. Gates `next_two` on both paths (§5.4.1, §5.5.4) |
| `eotg_aug_inherit_line_places` | script value, `value = 6` | `common/script_values/eotg_augmentation_values.txt` | the one bound for the line pick and the eligibility test (§5.4.1) |
| `eotg_aug_inherit_strike_effect` (param `NAME`) | scripted effect | same | massacre picker: picks one victim excluding anyone already struck (§5.4.2) |
| `eotg_aug_inherit_excision_effect` (param `TABLE` = `physician` / `back` / `self`) | scripted effect | same | the heir's surgery. Ruler-side odds, the heir as patient (§5.4.3). |
| `eotg_aug_inherit_ward_effect` (param `TYPE` = `house_arrest` / `dungeon`) | scripted effect | same | **tree only.** `eotg_aug_inherit_confine_effect = { TYPE }`, then a breakout roll that schedules .023 or .017 (§5A.4) |
| `eotg_aug_inherit_abdicate_effect` (params `WARDEN` = `yes` / `no`, `NOTIFY` = `yes` / `no`) | scripted effect | same | abdication to the heir (§5.4.4). NOTIFY fires .026; the tree passes `yes`, .028 passes `no`. |
| **leaf effects** (15, listed in §5.5.3) `eotg_aug_inherit_leaf_*_effect` and `eotg_aug_inherit_confine_effect` | scripted effects | same | each outcome's mechanics, written once. Called by the tree's leaf events **and** by .028, so the map outcomes match (owner Q5). |
| `eotg_aug_inherit_roll_effect` (param `CHANCE`, `NAME`) | scripted effect | same | every hidden roll in the tree goes through this. Honours the debug override `var:eotg_inh_force` (§9). |
| `eotg_aug_inherit_debug_effect` (params `PROFILE`, `BOND`, `THREAT`) | scripted effect, **debug only** | same | test recipes (§9). Never called by script. |
| `eotg_aug_inherit_ai_weight` | script value (ruler scope) — **optional; not built** (the AI throttle and §5.5.2 weights are inline in `eotg_on_yearly_aug_inherit_check`) | `common/script_values/eotg_augmentation_values.txt` | only if the scripter prefers values to inline `modifier` blocks for the §5.5.2 weights |

### 3.3 New: variables and flags (all on the **ruler** unless stated)

| Key | Type | Set by | Read by |
|---|---|---|---|
| `eotg_inh_heir` | char var → the heir | start effect | every node (via the scopes effect) |
| `eotg_inh_profile` | var, `flag:rage` / `flag:ledger` / `flag:cold` / `flag:certain` | start effect | descs, options, every roll (§5A) |
| `eotg_inh_bond` | var, `flag:rival` / `flag:estranged` / `flag:claimant` / `flag:favourite` / `flag:dutiful` | start effect | descs, rolls |
| `eotg_inh_source` | var, `flag:report` / `flag:cascade` | start effect | .001 desc |
| `eotg_inh_witness` | char var (may be unset) | start effect | .001, .004 |
| `eotg_inh_threat` | var, `flag:kill_ruler` / `flag:massacre` / `flag:next_two` / `flag:self` | roll-threat effect; preset by .002, .013, .015 | .009 desc, fire-threat |
| `eotg_inh_table` | var, `flag:physician` / `flag:back` / `flag:self` | .003 options | .010 desc and odds |
| `eotg_inh_reaction` | var, `flag:accept` / `flag:leave` / `flag:violent` | .013 immediate | .013 desc and options |
| `eotg_inh_old_ruler` | char var **on the heir** | abdicate effect | .026 |
| `eotg_inh_force` | var, `flag:pass` / `flag:fail` | **console only** | the roll effect (§9) |
| `eotg_inh_force_leaf` | var, a §5.5.2 branch key (`flag:massacre` …) | **console only** | .028's `random_list` (×1000 on that branch) |
| `eotg_inh_outcome` | var, the leaf (`flag:l1` … `flag:l17`), **kept after close** | every leaf effect | QA: the observer run reads the leaf distribution from it (§9 item 13); overwritten if the ruler ever gets a second occurrence |
| `eotg_flag_aug_inh_cooldown` | flag, 3 years | **on_action / start effect only** | on_action only (lesson 5) |
| `eotg_flag_aug_inh_active` | flag, 6 years (safety timeout) | start effect; cleared by close | the Heir's Arc start guards (§5.2) |
| `eotg_flag_aug_inh_coerced` | flag (chain) | .002.b | .003 refusal roll, .010 odds |
| `eotg_flag_aug_inh_gentle` | flag (chain) | .001.d | .006 acceptance |
| `eotg_flag_aug_inh_guarded` | flag (chain) | .002 (ledger), .009.b, .013 violent a | threat odds, .018 |
| `eotg_flag_aug_inh_talked` | flag (chain) | .006 (either variant) | hides .009.c (loop guard) |
| `eotg_flag_aug_inh_pattern_seen` | flag (chain) | .009 immediate | every route into .009 (loop guard, §5.4.5) |
| `eotg_flag_aug_inh_physicians_seen` | flag (chain) | .003 immediate | hides .006.b (loop guard) |
| `eotg_flag_aug_inh_struck` | flag on a massacre victim, 1 day | strike effect | strike effect (exclusion) |
| `eotg_inh_table_result` | var, `flag:clean` / `flag:maimed` / `flag:dead` | excision effect | .021 desc |
| `eotg_inh_dead_count` | var (number) | .017 immediate | .017 desc |
| `eotg_flag_aug_inh_ruler_ready` | flag (chain) | .009.d | .018 odds |
| `eotg_flag_aug_inh_buried_empty` | flag, **permanent** | .012.a | deferred return beat (§10) |
| `eotg_flag_aug_inh_seen` | flag **on the heir**, permanent | start effect | the gate: a given heir starts the tree once |
| `eotg_flag_aug_inh_marked` | flag **on the heir** (chain) | .007 refuse (ledger), .015.c | next-two weight |
| `eotg_aug_inh_presumed_dead` | var **on the heir**, permanent | .012.a | deferred return beat |

Chain flags have no duration and are removed by the close effect. Each one is also given `years = 6` so a lost chain cannot strand it.

### 3.4 New: data objects

| Type | Key | File | Contents |
|---|---|---|---|
| static modifier | `eotg_mod_aug_inh_terms` | `common/modifiers/eotg_augmentation_modifiers.txt` | On the ruler for 10 years: `vassal_opinion = -5` (a **succession risk**: the vassals doubt a succession that rests on terms holding; never taint or shame), `stress_gain_mult = 0.1`, `monthly_prestige_gain_mult = -0.1`. Add it to `eotg_clean_all_aug_modifiers`? **No**: the ruler may be unaugmented, and the modifier is about the heir. |
| static modifier | `eotg_mod_aug_inh_emptied_court` | same | On the ruler for 5 years after the massacre: `monthly_prestige_gain_mult = -0.15`, `general_opinion = -5`, `stress_gain_mult = 0.15` |
| opinion modifiers | **none new** | — | Reused: `eotg_opinion_aug_reassured`, `_unease`, `_fear`, `_disgust`, `_admiration`, `_grateful_patient`. Vanilla `disinherited_opinion` comes through `disinherit_effect`. |
| death reasons | **none new** | — | vanilla `death_murder_known`, `death_murder`, `death_execution`, `death_treatment`, `death_suicide`, `death_slaughtered_by_guards`; mod `eotg_death_cascade` (§5.4.6) |
| traits, story cycles, decisions | **none** | — | Lightest mechanism (§5.1). |
| icons / art | none new | — | Event backgrounds and themes are vanilla: `dread`, `murder`, `secret`, `family`, `medicine`, `realm`. Cite the vanilla `theme` keys when building. |
| name lists, CoAs, holy sites | n/a | — | Map-agnostic. |

**Owners:** scripter for everything in §3.1–§3.4, localizer for §7, and the lore-keeper reviews §7–§8 before the localizer writes.

---

## 4. File placement

| What | Path |
|---|---|
| events | **`events/eotg_augmentation_inherit.txt`** (new; index §3.5: a new namespace gets a new file) |
| loc | **`localization/english/eotg_aug_inherit_l_english.yml`** (new; UTF-8 **with BOM**) |
| on_action | `common/on_action/eotg_augmentation_on_actions.txt` (add the custom on_action; **append** it to the existing `yearly_playable_pulse = { on_actions = { … } }` list) |
| triggers | `common/scripted_triggers/eotg_augmentation_triggers.txt` |
| effects | `common/scripted_effects/eotg_augmentation_effects.txt` |
| modifiers | `common/modifiers/eotg_augmentation_modifiers.txt` (+ 4 loc keys in the new loc file) |

No new folder and no `replace_path`.

---

## 5. Wiring

### 5.1 Entry, and why it is not a story cycle

**Mechanism: a flag-and-variable chain**, not a story cycle. The tree is one bounded sequence of `trigger_event` stages, 6–24 months end to end, with no periodic tick. That is the shape of every vanilla multi-stage court chain (the court.2201 children-and-inheritance chain, `events/court_events/court_events_general.txt`). Index §1 rule 5 says "chain stages are fired with `trigger_event … days` from the previous stage; no flags". A story cycle would add an owner-death hook that this tree gets for free (an event to a dead ruler does not fire, and `on_trigger_fail` cleans up). It also leaves every existing story cycle untouched, which the owner asked for.

**Firing site A: the yearly check.** Append `eotg_on_yearly_aug_inherit_check` to `yearly_playable_pulse` (count+, per the phase 3 on_action map):
```
eotg_on_yearly_aug_inherit_check = {
    trigger = { eotg_aug_inherit_can_start = yes }
    effect = {
        random = {
            chance = 100                         # player: found out the first year it is true
            modifier = { factor = 0.4   is_ai = yes  highest_held_title_tier = tier_county }
            modifier = { factor = 0.55  is_ai = yes  highest_held_title_tier = tier_duchy }
            modifier = { factor = 0.7   is_ai = yes  highest_held_title_tier >= tier_kingdom }
            eotg_aug_inherit_start_effect = { SOURCE = report }
        }
    }
}
```
AI throttle shape: balance §5.10(a), from vanilla `yearly_on_actions.txt:3022-3030`.

**Firing site B: the cascade.** This is the moment the heir breaks. `eotg_aug_nr_cascade_effect` currently tells the employer through nr.006 *The Broken Champion*. Change its last block to:
```
employer ?= {
    if = {
        limit = {
            primary_heir ?= prev            # the champion is this liege's primary heir
            eotg_aug_inherit_can_start = yes
        }
        eotg_aug_inherit_start_effect = { SOURCE = cascade }
    }
    else = { trigger_event = { id = eotg_aug_nr.006  days = { 1 7 } } }
}
```
Without this, the ruler would get nr.006 (restrain, cut it out, execute: a three-way version of this tree) and then this tree a year later about the same cascade. The change touches one effect. **No story cycle changes** (owner Q2 in §11).

**Cooldown authority.** `eotg_flag_aug_inh_cooldown` (3 years) is set in `eotg_aug_inherit_start_effect`, which only the two firing sites call. It is read only in `eotg_aug_inherit_can_start`, which only the on_action and the cascade hook evaluate. **No event `trigger` reads it** (lesson 5; the 115-event v1 failure).

**`eotg_aug_inherit_can_start`** (ruler scope):
- `is_landed = yes`, `is_adult = yes`, `is_imprisoned = no`, `NOT = { has_trait = incapable }`;
- `eotg_is_unclaimed_folk = no` (the frontier placeholder guard every cybernetics on_action carries);
- `NOT = { has_trait = eotg_total_integration }`. A Seamless ruler has its own pool and no person left to decide.
- `NOT = { has_character_flag = eotg_flag_aug_inh_cooldown }`;
- `NOT = { has_variable = eotg_inh_heir }`, meaning no chain is running;
- **Heir's Arc exclusivity:** `NOT = { any_owned_story = { story_type = eotg_story_aug_heir_arc  NOT = { var:eotg_stage = 5 } } }`. The tree waits while an arc is live (stages 0–4). It may start while the arc is dormant at stage 5, waiting for round 2.
- `primary_heir ?= { eotg_aug_inherit_heir_candidate = { RULER = root } }`.

**`eotg_aug_inherit_heir_candidate`** (heir scope):
- `has_trait = eotg_neurofractured`;
- `is_alive = yes`, `is_adult = yes`;
- `is_ai = yes`. The heir's own choices are resolved in script, so a player-heir is never overridden.
- `is_landed = no` and `is_courtier_of = $RULER$`. Landed or foreign heirs are deferred (§10).
- `is_imprisoned = no`;
- `NOT = { has_character_flag = eotg_flag_aug_inh_seen }`.

**`eotg_aug_inherit_start_effect`:**
1. `add_character_flag = { flag = eotg_flag_aug_inh_cooldown  years = 3 }`, and `eotg_flag_aug_inh_active` for 6 years.
2. `primary_heir = { add_character_flag = eotg_flag_aug_inh_seen  save_scope_as = eotg_inh_heir }`, then `set_variable eotg_inh_heir`.
3. `set_variable eotg_inh_source = flag:$SOURCE$`.
4. Roll the profile (§5A.1) and set the bond (§5A.2).
5. **Tree path only** (`eotg_aug_inherit_tree_runs = yes`). Witness, first valid:
   - `court_position:court_physician_court_position` when `employs_court_position = court_physician_court_position` (the mod's existing shape, endgame.txt:98);
   - else `primary_spouse` if it is not the heir;
   - else `random_courtier = { limit = { is_adult = yes  NOT = { this = scope:eotg_inh_heir } } }`. That is a non-violent pick of a speaker, which index §6 item 6 allows. Save it as the variable.
6. Fire:
   - `eotg_aug_inherit_tree_runs = yes` → `trigger_event = { id = eotg_aug_inherit.001  days = { 3 10 } }`;
   - else → `trigger_event = { id = eotg_aug_inherit.028  days = { 30 180 } }`. The delay is the months the tree would have taken.

### 5.2 Collisions and exclusivity

| Running thing | Rule |
|---|---|
| **The Heir's Arc** (ruler Neurofractured, the heir watching) | The tree does not start while an arc is at stages 0–4 (gate above). While the tree runs, the arc must not start, so add `NOT = { has_variable = eotg_inh_heir }` to **both arc-start sites**: the NF check step 2 and the Overclocked check (balance §5.8(a)). That is one trigger line in each on_action; the story cycle is unchanged. A dormant arc at stage 5 can start round 2 only when the primary heir changes. In this tree that happens only at a leaf, and the close effect has run by then, so the two never interleave. **Accepted overlap:** if .013 disinherits and the reaction roll then fires a threat 30–60 days later, round 2 may start on the *new* heir meanwhile. It is about a different person, so it is allowed. |
| **The non-ruler lifecycle** (nr.001–.005 about the same heir) | Step 5 of `eotg_on_yearly_aug_nonruler_check` gains `NOT = { scope:eotg_nr_liege.var:eotg_inh_heir ?= this }`, so the liege gets no "champion" event about the heir mid-chain. Drift (step 4) keeps running, as it should: the heir gets worse while the ruler deliberates. |
| **nr.006** (the cascade) | Replaced for the primary heir, as in §5.1 site B. |
| **The ruler's own Neurofractured / Overclocked pools** | They run independently. A Neurofractured ruler can run this tree too, since only the Heir's Arc is exclusive. |
| **Countdown, Patron, Retinue** | No overlap: none of them reads the heir. |
| **Ruler death mid-chain** | Pending events to a dead ruler do not fire. The variables die with the ruler, and the heir's `seen` flag stays, so the tree never restarts for this heir under a new ruler. That is intended: the new ruler *is* usually this heir. |
| **Heir dies, leaves court or loses the trait mid-chain** | Each node's `trigger = { eotg_aug_inherit_chain_valid = yes }` fails, and `on_trigger_fail = { eotg_aug_inherit_close_effect = yes }` runs. Precedent: vanilla `on_trigger_fail`, `events/activities/coronation_activity/coronation_events.txt:3942`; skill `events.md` §on_trigger_fail. |

### 5.3 The tree

Delays are in days. "→ Lx" is a leaf. Universal options are lower-case letters; **[gated]** options name their gate. Each option's resource move is on the heir unless stated. Profile and bond odds are in §5A.

```
.001 The Report ─┬─ a ──────────────────────────► .002 The Conversation (14–30)
                 ├─ b ──────────────────────────► .003 The Physicians (30–60)
                 ├─ c ──────────────────────────► .004 The Watch (60–120)
                 ├─ d [compassionate] ──────────► .002 (gentle) (3–7)
                 └─ e [duchy+] ─────────────────► .005 The Council (14–30)

.002 The Conversation ─┬─ a ─────────────► .006 The Terms (7–14)
                       ├─ b ─────────────► .003 (coerced) (14–30)
                       ├─ c ─────────────► .007 The Answer (7–14)
                       ├─ p [profile, one shows] ─┬ rage    ► .006
                       │                          ├ ledger  ► .005 (guarded)
                       │                          ├ cold    ► .007 (accept +30)
                       │                          └ certain ► .009 (threat preset kill_ruler)
                       └─ d [wrathful] ──► .009 The Pattern (14–30)

.003 The Physicians ─┬─ a ──────────────► .010 The Table (physician) (14–30)
   (normal)          ├─ b ──────────────► .008 The Ward (7–14)
                     ├─ c ──────────────► .010 (back-street) (14–30)
                     └─ d [physician/learning] ► .010 (self) (14–30)
   (refused)         ├─ a ──────────────► .009 (7–14)
                     └─ b ──────────────► L6 Exiled (resolved in option)

.004 The Watch ─┬─ a ──────► .009 (30–90)
                ├─ b ──────► .011 Passage Out (7–14)
                ├─ c ──────► .005 (7–14)
                └─ d [intrigue≥14|deceitful] ► .012 The Shuttle That Never Docked (14–30)

.005 The Council ─┬─ a ───► .013 Struck from the Line (7–14)
                  ├─ b ───► .014 The Hand-Off (7–14)       [shown if the abdication is valid]
                  ├─ c ───► .009 (30–90)
                  └─ d ───► .015 The Offer (14–30)          [shown if scope:eotg_inh_second qualifies]

.006 The Terms ─(accept)─┬─ a ─► .022 Kept Terms (365)                 ► L4
                         ├─ b ─► .003 (no refusal) (14–30)
                         └─ c [ruler Overclocked] ─► .020 Two Machines (7–14) ► L16
               ─(refuse)─┬─ a ─► .005 (7–14)
                         └─ b ─► .009 (60–120)

.007 The Answer ─(accept)─┬─ a ─► L7 Disinherited (in option)
                          └─ b ─► .006 (accept forced) (7–14)
                ─(refuse)─┬─ a ─► .013 (violent +15) (7–14)
                          └─ b ─► .009 (60–120)

.008 The Ward ─┬─ a (comfortable) ─┐  ward effect: breakout roll
               └─ b (chains) ──────┴─► .023 The Locked Wing (90–180) ► L5
                                   └─► .017 The Long Watch (90–180, breakout) ► L14

.009 The Pattern ─┬─ a arrest ── success ► ward (dungeon) ► .023 / .017
   (threat rolled │             └ fail ──► fire threat (1–3)
    and shown)    ├─ b guard and wait ───► fire threat (30–90), guarded
                  ├─ c talk down [not talked] ─ success ► .006 (accept forced)
                  │                            └ fail ──► fire threat (7–14)
                  ├─ d [education_martial]► fire threat (14–30), ruler ready
                  └─ e [callous|sadistic] ► L17 (in option)

    fire threat:  kill_ruler ► .018 │ massacre ► .017 │ next_two ► .016 │ self ► .019

.010 The Table ─┬─ a ─► surgery (hidden) ─► .021 After the Table (3) ► L1 / L2 / L3
                ├─ b [compassionate] ─► as a, plus a vigil
                └─ c ─► .009 (30–60)

.011 Passage Out ─┬─ a ───────────────────────► L6
                  ├─ b (passage and credit) ──► L6
                  └─ c [vengeful|arbitrary] ───► L6 + disinherited

.012 The Shuttle ───────┬─ a ─► L8
                       └─ b ─► .009 (30–60)

.013 Struck (reaction rolled) ─(accept)──┬─ a ─► L7
                               ─(leave)───┬─ a ─► L6 (they leave on their own)
                                          └─ b ─► ward (dungeon) ► .023 / .017
                               ─(violent)─┬─ a ─► fire threat (30–60), guarded
                                          ├─ b ─► ward (dungeon) ► .023 / .017
                                          └─ c [callous] ─► L17

.014 The Hand-Off ─┬─ a ─► L9 Abdication under a warden ─► .026 to the heir (30)
                   ├─ b ─► L10 Quiet abdication ─────────► .026 to the heir (30)
                   └─ c ─► .009 (30–90)

.015 The Offer ─┬─ a ─► .027 The Line Shortens, sanctioned (30–90) ► L11
                ├─ b ─► roll: second acts ► .027 unsanctioned (60–120) ► L11
                │              else ────► .009 (30–90)
                └─ c [just] ─► .009, threat preset next_two, heir marked (14–30)

.018 The Last Audience ─ a/b/c ─ roll ─ success ► ruler dies ► .025 to the heir (3) ► L15
                                       └ fail ──► .024 Still Breathing (1)
.024 Still Breathing ─┬─ a ─► L17
                      ├─ b ─► ward (dungeon) ► .023 / .017
                      └─ c [forgiving] ─► L4 (terms applied here)
```

**Depth per path** (events the ruler sees, entry included): L4 via .002→.006→.022 is **4**. L1–L3 via .003→.010→.021 is **4**. L14 via .004→.009→.017 is **4**. L11 via .004→.005→.015→.027 is **5**. L13 via .002 (ledger)→.005→.015 c→.009→.016 is **6**, the longest. L6 via .004→.011 is **3**. L5 via .003→.008→.023 is **4**. L15 via .002 (certain)→.009→.018 is **4**. Most paths are 3–5.

**Loop guards.** Nothing revisits more than one node:
- **.009 runs at most once** (`eotg_flag_aug_inh_pattern_seen`). Every option that routes to .009 checks the flag: if it is set, the option calls `eotg_aug_inherit_fire_threat_effect` instead, with the same delay, and the tooltip says "Whatever [heir] is building will not wait." (`eotg_aug_inherit.route_threat_tt`).
- **.006 runs at most once** (`eotg_flag_aug_inh_talked`). Routes into .006 when the flag is set go to .022 (accept) or .009 (refuse) by the same rule.
- **.003 runs at most once.** When .003 has already been seen, .006.b is hidden by `eotg_flag_aug_inh_physicians_seen` (§3.3).
- The worst case is therefore about 7 events.

#### Node table (effects, gates, AI)

Notation:
- "H±n" means the heir's `eotg_add_fracture_risk = { AMOUNT = ±n }`.
- The stress helpers are the index §3.2 `eotg_aug_stress_*_effect` set.
- AI lines are `base; modifiers`. Every option has at least two trait modifiers (index §1 rule 6). Since owner Q5 the tree runs only for player rulers, so these weights matter only if the player hands the ruler to the AI mid-chain. They are kept for that case, for index §1 rule 6, and as the source of the AI defaults in §5.5.3.

**.001 The Report.** Desc: one of four profile variants, plus a bond line, plus a source line (cascade or report). Theme `family`. Left portrait the ruler; right portrait the witness if one exists, else the heir.

| Opt | Gate | Effect | Next | Resource | AI |
|---|---|---|---|---|---|
| a "Bring [heir] to me. I'll hear it from [heir_himher]." | — | — | .002 | H+0, reads the band in the desc | 30; +15 gregarious, +10 honest, −10 shy |
| b "Send for the physicians before anyone else." | — | — | .003 | H−3 (the heir is caught early) | 30; +20 diligent, +15 lifestyle_physician |
| c "Say nothing. Watch [heir]." | — | ruler stress helper `lie` | .004 | H+5 (nobody intervenes) | 20; +20 paranoid, +15 deceitful |
| d "I'll go to [heir] myself, before the next watch." | compassionate | `eotg_flag_aug_inh_gentle`; the heir gets `reassured` | .002 | H−5 | 30; +30 compassionate, +10 forgiving |
| e "The succession comes first." | `highest_held_title_tier >= tier_duchy` (no icon); callous and paranoid are stress responses only | — | .005 | H+5 | 10; +20 callous, +20 paranoid, −20 compassionate, −20 trusting |

**.002 The Conversation.** The heir is present (right portrait). Desc: four profile variants plus five bond lines.

| Opt | Gate | Effect | Next | Resource | AI |
|---|---|---|---|---|---|
| a "Stay. We face it together." | — | — | .006 | H−5 | 30; +20 compassionate, +10 trusting |
| b "You will see the physicians. That is not a request." | — | `eotg_flag_aug_inh_coerced`; the heir gets `unease` | .003 | H+5 | 30; +15 stubborn, +10 diligent |
| c "Give up the succession. Quietly." | — | — | .007 | H+3 | 25; +15 just, +10 content |
| p_rage "Sit with [heir] until it passes." | profile rage | 25% the ruler is wounded (`increase_wounds_effect`, REASON attacked), unless ruler prowess ≥ 12 | .006 | H−8 | 30; +20 brave, +10 patient |
| p_ledger "Show me the list." | profile ledger | `eotg_flag_aug_inh_guarded` (the names on it are guarded) | .005 | H+5 (exposed) | 30; +20 paranoid, +10 diligent |
| p_cold "Do you want to stop?" | profile cold | the .007 acceptance roll +30 | .007 | H−3 | 30; +15 compassionate, +10 honest |
| p_certain "You don't rule yet." | profile certain | `var:eotg_inh_threat = flag:kill_ruler`; ruler +50 prestige | .009 | H+10 | 30; +20 arrogant, +15 wrathful |
| d "Get out of my sight." | wrathful | the heir gets `disgust` | .009 | H+10 | 30; +30 wrathful, +10 arbitrary |

Up to 5 options show: 3 universal, 1 profile, and at most 1 trait.

**.003 The Physicians.** The speaker is `eotg_inh_surgeon`, the court physician if one exists. Otherwise the text names the clinic through the existing `[ROOT.Char.Custom('eotg_aug_cl_clinic_of_record')]` placeholder, with no new seller key. Desc variants by the heir's band (3), plus **refused** (the heir did not come; §5A.4). Sets `eotg_flag_aug_inh_physicians_seen`.

| Opt | Gate | Effect | Next | Resource | AI |
|---|---|---|---|---|---|
| a "Cut it out of [heir]." | gold ≥ `major_gold_value`; not refused | `eotg_inh_table = flag:physician` | .010 | reads the band; H+0 | 30; +20 brave, +15 diligent |
| b "Hold it down. Sedation, and a locked ward." | not refused | — | .008 | H−5 | 30; +20 craven, +15 content |
| c "Find someone cheaper." | gold ≥ `medium_gold_value`; not refused | `eotg_inh_table = flag:back` | .010 | H+0 | 20; +20 greedy, +10 arbitrary |
| d "I'll stand at the table myself." | `lifestyle_physician` OR `learning >= 14`; not refused | `eotg_inh_table = flag:self` | .010 | H−3 | 30; +25 lifestyle_physician, +10 brave |
| a_ref "Find [heir]. Bring [heir_himher] back." | refused | — | .009 | H+8 | 40; +15 stubborn, +10 wrathful |
| b_ref "Let [heir] go." | refused | `move_to_pool` → **L6** (no passage paid), close | — | H+5 | 30; +15 content, +10 craven |

If refused and the ruler cannot afford a/c/d, a_ref and b_ref still show. The non-refused variant always has b, so the event can never dead-end.

**.004 The Watch.** The speaker is `cp:councillor_spymaster` if employed, else the witness. Immediate: H+6 (months pass). The desc is one of four profile variants of what the watcher saw, so the player learns the profile here.

| Opt | Gate | Effect | Next | Resource | AI |
|---|---|---|---|---|---|
| a "Keep watching." | — | — | .009 | H+3 | 25; +20 paranoid, +10 patient |
| b "Put [heir] on the next ship out." | — | — | .011 | H+0 | 30; +15 craven, +10 content |
| c "Take this to the council." | — | — | .005 | H+0 | 30; +15 just, +10 diligent |
| d "Let [heir] be lost in transit." | `intrigue >= 14` OR deceitful | — | .012 | H−3 | 30; +25 deceitful, +10 schemer |

**.005 The Council.** Named actors: `eotg_inh_councillor` (`cp:councillor_chancellor`, else the spouse, else unnamed) and `eotg_inh_second`, the first eligible person in the line who is not the heir (§5.4.1). Since 2026-10-08 the line pick skips players, so the second is never a player and the `is_ai = yes` in option d's gate is now a belt-and-braces check. Desc base, plus a line when the second exists.

| Opt | Gate | Effect | Next | Resource | AI |
|---|---|---|---|---|---|
| a "Strike [heir] from the line." | — | — | .013 | H+5 | 30; +20 just, +15 callous |
| b "I'll step down while I can still set the terms." | `primary_heir = scope:eotg_inh_heir`, ruler `is_landed`; the heir is not imprisoned | — | .014 | H−5 | 15; +20 content, +15 humble, −20 ambitious |
| c "Nothing changes. [heir] stays first." | — | — | .009 | H+5 | 25; +15 stubborn, +10 trusting |
| d "Hear what [second] proposes." | the second exists, `is_ai = yes`, is adult, `NOT has_trait = eotg_neurofractured`, and ambitious OR `opinion of the heir < 0` | — | .015 | H+3 | 25; +20 ambitious, +15 callous |

**.006 The Terms.** Immediate: the acceptance roll (§5A.4). Sets `talked`. Desc: accept, or one of four profile refusal lines.

| Opt | Variant | Gate | Effect | Next | Resource | AI |
|---|---|---|---|---|---|---|
| a "Then we hold each other to it." | accept | — | the heir gets `eotg_mod_aug_sedated` (5 years) and `reassured`; the ruler gets `eotg_mod_aug_inh_terms` | .022 (365) | H−15 | 40; +20 compassionate, +10 forgiving |
| b "And the physicians are part of the terms." | accept | not physicians_seen | (no refusal roll at .003) | .003 | H−5 | 30; +20 diligent, +10 craven |
| c "Then I'll meet you where you are." | accept | ruler `eotg_is_aug_tier3 = yes` | — | .020 | H−5 | 10; +20 ambitious, +15 eccentric, `factor = 0` content |
| a "Then the council decides." | refuse | — | — | .005 | H+5 | 30; +15 stubborn, +10 just |
| b "I'll give you time." | refuse | — | — | .009 (60–120) | H+5 | 30; +15 patient, +10 trusting |

**.007 The Answer.** Immediate: the renunciation roll (§5A.4). Desc: the question, plus accept or refuse.

| Opt | Variant | Effect | Next | Resource | AI |
|---|---|---|---|---|---|
| a "Thank you." | accept | vanilla `disinherit_effect = { DISINHERITOR = root }` on the heir → **L7**, close | — | H−5 | 40; +15 compassionate, +10 honest |
| b "No. Stay my heir. I only had to know." | accept | — | .006, accept forced | H−8 | 20; +20 compassionate, +10 trusting |
| a "Then I'll do it for you." | refuse | — | .013, violent +15 | H+5 | 30; +20 stubborn, +10 callous |
| b "Forget I asked." | refuse | ledger profile: the heir gets `eotg_flag_aug_inh_marked` | .009 (60–120) | H+5 | 30; +15 craven, +10 forgiving |

**.008 The Ward.**

| Opt | Effect | Next | Resource | AI |
|---|---|---|---|---|
| a "Keep [heir] comfortable." | `remove_short_term_gold = minor_gold_value`; ward effect `TYPE = house_arrest`; the heir gets `eotg_mod_aug_sedated` (5 years); stress helper `tyranny` | ward roll | H−10 | 40; +20 compassionate, +10 generous |
| b "Chains, and a guard who doesn't talk." | ward effect `TYPE = dungeon` (breakout ×0.5); stress helper `cruelty` | ward roll | H+5 | 25; +20 callous, +15 paranoid |

**.009 The Pattern.** Immediate: sets `pattern_seen`, H+8, runs `eotg_aug_inherit_roll_threat_effect`. The desc is one of four threat variants: the warning sign the ruler sees, never the forecast of a plot (§8).

| Opt | Gate | Effect | Next | Resource | AI |
|---|---|---|---|---|---|
| a "Arrest [heir] before the next watch." | the heir is not imprisoned | arrest roll (§5A.4). Success: ward effect `TYPE = dungeon`. Fail: fire the threat in 1–3 days, with toast `eotg_aug_inherit.009.a_fail_tt`. Stress helper `tyranny`. | ward / threat | H+5 | 30; +20 paranoid, +15 just |
| b "Double the guard and wait." | — | `guarded`. Fire the threat (30–90). A `self` threat while guarded: a 50% roll, where a pass means the guard finds the heir in time and runs ward `house_arrest`. | threat / ward | H+3 | 30; +20 craven, +10 patient |
| c "Go to [heir]. Talk [heir_himher] down." | NOT `talked` | talk roll (§5A.4). Success: .006, accept forced. Fail: fire the threat (7–14). | .006 / threat | H−5 | 25; +20 compassionate, +15 gregarious |
| d "Choose the ground. If it comes for me, it meets me there." | `education_martial` (`skill = martial`); brave is a stress response only | `eotg_flag_aug_inh_ruler_ready`; fire the threat (14–30). Massacre: one victim fewer. Kill_ruler: .018 odds −20. | threat | H+0 | 30; +20 education_martial_3, +30 education_martial_4, +30 education_martial_5, +10 brave |
| e "End it before [heir] does." | callous OR sadistic | **L17**: the heir dies (`death_murder`, `killer = root`). Vanilla `add_kinslayer_trait_or_nothing_effect = { VICTIM = scope:eotg_inh_heir }` runs on root **first**, per the M4 policy. Stress helper `murder`; `add_dread = 20`; close. | — | tier change (death) | 20; +25 callous, +20 sadistic, `factor = 0` compassionate |

**.010 The Table.** The desc gives the odds in words by `eotg_inh_table`, with three variants: the physician's table, a back-street table, your own hands. It also adds one line if `coerced`. Shape: end.001.

| Opt | Effect | Next | Resource | AI |
|---|---|---|---|---|
| a "Begin." | pay (physician `major_gold_value`, back `medium_gold_value`, self `medium_gold_value`); `hidden_effect = { scope:eotg_inh_heir = { eotg_aug_inherit_excision_effect = { TABLE = … } } }`; fire .021 (3) | .021 | tier change | 40; +15 brave, +15 diligent |
| b "Begin. I'll stay with [heir] while they work." | compassionate; as a; the heir gets `reassured`; ruler stress minor loss | .021 | tier change | 30; +30 compassionate, +10 gregarious |
| c "Not today." | — | .009 (30–60) | H+5 | 15; +20 craven, +10 lazy |

**.011 Passage Out.** Every option is a leaf. **L6 Exiled.** Exile is a paid berth on an outbound ship, out of the realm's systems. The heir leaves court through `move_to_pool`, as end.011 does. **The text names no destination, no Unclaimed region and no polity** (lore review): the ship leaves, and that is all the ruler knows. **The heir stays in the line**, and the desc says so: exile moves the problem, it does not end it. Close.

| Opt | Gate | Effect | Resource | AI |
|---|---|---|---|---|
| a "Take the berth. Don't come back." | — | the heir gets `disgust` | H+5 | 30; +15 callous, +10 wrathful |
| b "Go, with passage and credit, and my word." | gold ≥ `medium_gold_value` | pay `medium_gold_value`; the heir gets `reassured` | H−5 | 30; +20 generous, +10 compassionate |
| c "Take the berth. You are no longer my heir." | vengeful OR arbitrary | `disinherit_effect`, then `move_to_pool` | H+8 | 30; +25 vengeful, +15 arbitrary |

**.012 The Shuttle That Never Docked.** **L8 Faked death** (a). Framing (lore review): the heir is lost in transit between systems, and the shuttle never docks. The court mourns someone who is on a ship elsewhere. Text may cite "residence logs". It never mentions a registry, a records office or a certificate, and no record "fails".
- pay `medium_gold_value`;
- `disinherit_effect`;
- the heir gets `eotg_aug_inh_presumed_dead` and `move_to_pool`;
- the ruler gets `eotg_flag_aug_inh_buried_empty`;
- stress helper `lie`;
- H−5;
- exposure roll (§5A.4). If exposed: every vassal with `opinion < 0` gets `disgust` for 5 years, the ruler loses 100 prestige, and the toast `eotg_aug_inherit.012.exposed_tt` fires. **The exposure is always a witness who saw the heir alive** (a dockhand or a fitter, unnamed, so no pronoun), never a failed record;
- close.

AI 30; +20 deceitful, +10 schemer. Option b "No. I can't do this." → .009 (30–60), H+3, AI 30; +15 honest, +10 just.

**.013 Struck from the Line.** Immediate: `disinherit_effect` on the heir, then the reaction roll (§5A.4) into `eotg_inh_reaction`. The ruler loses 150 prestige: the vanilla interaction costs dynasty prestige, and this is the event-side stand-in. Desc: accept, leave or violent.

| Opt | Variant | Effect | Resource | AI |
|---|---|---|---|---|
| a "It's done." | accept | **L7**, close | H−3 | 40; +10 content, +10 just |
| a "Let [heir] go." | leave | the heir `move_to_pool` → **L6**, close | H+5 | 30; +15 content, +10 craven |
| b "Bring [heir] back under guard." | leave | ward `dungeon` | H+8 | 30; +20 wrathful, +10 stubborn |
| a "Guard the new line." | violent | `guarded`; fire the threat (30–60; the threat is preset by the reaction roll, §5A.3) | H+5 | 30; +20 paranoid, +10 diligent |
| b "Lock [heir] up before [heir_heshe] moves." | violent | ward `dungeon`; stress helper `tyranny` | H+5 | 30; +15 just, +15 paranoid |
| c "End it." | violent; callous | **L17** as .009.e, including `add_dread = 20` (stated explicitly; built 2026-10-08) | tier change | 20; +25 callous, +15 vengeful |

**.014 The Hand-Off.**

| Opt | Effect | Resource | AI |
|---|---|---|---|
| a "Yes, with a warden at [heir_herhis] side." | **L9**: `eotg_aug_inherit_abdicate_effect = { WARDEN = yes }`; close | H−10 | 30; +20 humble, +15 content |
| b "Quietly. No warden. It's [heir_herhis] now." | **L10**: `eotg_aug_inherit_abdicate_effect = { WARDEN = no }`; the old ruler gets a major stress loss; close | H+10 | 15; +20 content, +10 trusting, −20 paranoid |
| c "Not yet." | → .009 (30–90) | H+5 | 30; +20 ambitious, +10 stubborn |

**.015 The Offer.** `eotg_inh_second` proposes to remove the heir. Their portrait is on the right.

| Opt | Gate | Effect | Next | Resource | AI |
|---|---|---|---|---|---|
| a "Do what you must. I don't want to know." | — | stress helper `murder` (complicity) | .027 sanctioned (30–90) | H+5 | 20; +20 callous, +10 ambitious, `factor = 0` compassionate |
| b "No. And if [heir] dies, I'll know whose hand it was." | — | the second gets `unease`. Then the "second acts anyway" roll (§5A.4): pass → .027 unsanctioned (60–120); fail → .009 (30–90). | .027 / .009 | H+3 | 40; +15 just, +15 honest |
| c "Say it to [heir]'s face." | just | the heir gets `eotg_flag_aug_inh_marked`; threat preset `next_two` | .009 (14–30) | H+10 | 30; +30 just, +10 honest |

**.016 The List: L13 (required).** See §5.4.1. The event also fires for Running Hot and Certainty heirs (threat weights §5A.3), so **the base desc must not assume a written list** (lore review). The desc is built as follows:
- `first_valid` on the profile:
  - `desc_ledger` (profile ledger): the list. The heir wrote the names down, and the two at the top are gone.
  - `desc_neutral` (every other profile): "[heir] had worked out who stood between [heir_herhis] and the seat."
- Then a count line: two dead, or `desc_one` (one dead, a short line).
- Then the child-victim line (`.child`, §11 Q1) when a victim was under 16.
- "Forecast" appears only in the heir's own words about the heir's own self (§8.1), never as the narration's explanation of the killings.

| Opt | Effect | Resource | AI |
|---|---|---|---|
| a "Take [heir] into custody." | ward `dungeon` (the breakout roll still applies); close is called by .023 / .017 | H−5 | 30; +20 just, +10 diligent |
| b "Execute [heir]." | **L17 within L13**: kinslayer (on root first), `death_execution` with `killer = root`; stress helper `murder`; close | tier change | 30; +20 vengeful, +15 wrathful |
| c "[heir] is all the line I have left." | the heir stays; every vassal with `opinion < 20` gets `disgust` for 5 years; stress helper `neglect`; close | H+10 | 15; +20 content, +10 craven |

**.017 The Long Watch: L14 (required).** See §5.4.2. Desc: the base, plus variants "from the ward" and "the ruler was there" (ready flag), plus the victim lines. Shape: fracture.004. The ruler gets `eotg_mod_aug_inh_emptied_court` (5 years) in `immediate`.

| Opt | Effect | Resource | AI |
|---|---|---|---|
| a "Take [heir] alive." | `imprison` the heir, type `dungeon`; close | H−5 | 30; +15 just, +10 brave |
| b "Cut [heir] down." | kinslayer on root; the heir `death = { death_reason = death_slaughtered_by_guards  killer = root }`; stress helper `murder`; close | tier change | 30; +20 wrathful, +15 vengeful |
| c "Hold [heir] until the shaking stops." | compassionate; `imprison` the heir, type `house_arrest`; 25% the ruler is wounded; ruler stress medium gain; close | H−10 | 30; +30 compassionate, +10 brave |

**.018 The Last Audience: L15 (required).** The heir comes to the ruler. Desc: five bond variants, the words the heir chooses. Each option sets a modifier on the attempt roll (§5A.4), then resolves it inside the option.

| Opt | Gate | Roll modifier | AI |
|---|---|---|---|
| a "Guards!" | — | −15 | 40; +20 craven, +10 paranoid |
| b "Say [heir]'s name. Make [heir_himher] hear it." | — | favourite or dutiful −25; otherwise +5 | 30; +20 compassionate, +10 honest |
| c "Face [heir] yourself." | brave | ruler prowess > heir prowess: −20; otherwise +5 | 30; +30 brave, +10 wrathful |

- **Success, L15.** The heir gets the kinslayer effect with `VICTIM = root`. The ruler dies by `death = { death_reason = death_murder_known  killer = scope:eotg_inh_heir }`. H−10, the release; this moves the heir's resource. .025 fires to the heir in 3 days. The player, if this was the player's ruler, continues as the heir by normal succession: vanilla lets a murderer inherit, and heir.005 has the same shape.
- **Failure.** The ruler gets `increase_wounds_effect` (REASON attacked). H+10. → .024 (1).

**.019 The Quiet Room: L12.** Only fired for threat `self`.
- Desc variant **cold**: `death = { death_reason = death_suicide }` (vanilla, public).
- Every other profile: `death = { death_reason = eotg_death_cascade }`. The variant states it plainly, "[heir] died in a neural cascade", with no machine agency and no "the hardware" (lore review). No ruler intervention.
- The death runs in `immediate`, before the options.
- The text is restrained: no method, no detail (§7.1, the L12 desc rule). Ruler: `stress_impact` major gain. 25% `depressed_1`, unless the ruler is callous.
- **Value-neutral** (lore review): canon gives no culture a stance on suicide, so no option moves prestige or piety. The options cost stress and close-family opinion only. Faith-gated reactions are a deferral (§10).

| Opt | Effect | AI |
|---|---|---|
| a "Lay [heir] to rest as my heir, not as a patient." | ruler stress minor loss; close family get `reassured` | 30; +20 compassionate, +10 just |
| b "Tell the court it was a cascade." | cold variant: stress helper `lie`, and close family get `unease`. Cascade variant: it is the truth, so no helper and no opinion. | 30; +15 deceitful, +10 craven |
| c "It settled itself." | callous; stress helper `neglect` is skipped (callous); close family get `disgust` | 20; +30 callous, +10 sadistic |

**.020 Two Machines: L16.** Coupling: the ruler's tier changes.

| Opt | Effect | AI |
|---|---|---|
| a "Take the limits off." | ruler `eotg_trigger_neurofracture = yes`. That is the full cascade path: fracture.0001, cooldown, Countdown end. Heir H−20. Mutual `admiration`. The ruler gets `eotg_flag_aug_heir_arc_done`: the arc's premise (an heir watching the ruler break) is spent. Close. | 20; +20 ambitious, +15 eccentric |
| b "No. One of us is enough." | **L4**: as .006 accept a; .022 in 365 days | 40; +20 content, +15 craven |

**.021 After the Table: L1 / L2 / L3.** Desc by the outcome: clean, maimed, dead. The surgery has already resolved. Close.
- **L1 (clean):** the heir runs `eotg_aug_excision_effect` and gets `eotg_opinion_aug_grateful_patient`; the ruler gets +100 prestige.
- **L2 (maimed):** the same, plus `maimed`; the heir gets `reassured`.
- **L3 (dead):** the heir dies of `death_treatment`.

Options: clean/maimed **a** "[heir] is still [heir]." (ruler stress minor loss; AI 40, +10 compassionate, +10 content) and **b** "Whatever's left of [heir_himher] is enough." (AI 30, +10 callous, +10 cynical). Dead **a** "Lay [heir] to rest." (stress medium gain; AI 40, +10 compassionate, +10 just) and **b** "The table had its odds. I chose them." (stress minor gain, +50 prestige; AI 30, +15 callous, +10 stubborn). Coupling: tier change.

**.022 Kept Terms: L4.** Desc reads the heir's band now: **holding** (flicker) or **slipping** (fracture or storm). Close at the end of either option.

| Opt | Variant | Effect | AI |
|---|---|---|---|
| a "Another year, then." | holding | H−5 | 40; +10 patient, +10 content |
| b "Tighten the terms." | holding; diligent | H−10; ruler stress minor gain | 30; +25 diligent, +10 paranoid |
| a "Then we start again. Now." | slipping | H−10; ruler stress medium gain | 40; +15 compassionate, +10 stubborn |
| b "I can't carry both of us." | slipping | the ruler removes `eotg_mod_aug_inh_terms`; H+10 | 30; +15 craven, +10 callous |

**.023 The Locked Wing: L5.** Fired only if the ward held. Desc variants: comfortable or chains.

| Opt | Gate | Effect | AI |
|---|---|---|---|
| a "Keep it so." | — | H−5; close | 40; +10 patient, +10 just |
| b "Visit [heir]." | compassionate | the heir gets `reassured`; H−5; ruler stress minor loss; close | 30; +30 compassionate, +10 gregarious |

**.024 Still Breathing.** The ruler is wounded and the heir is held by the guards.

| Opt | Gate | Effect | AI |
|---|---|---|---|
| a "Execute [heir]." | — | **L17** as .016.b | 40; +20 vengeful, +15 wrathful |
| b "Lock [heir] away." | — | ward `dungeon` | 30; +15 just, +15 craven |
| c "I forgive you. Don't make me regret it." | forgiving | **L4**: the heir gets `reassured`; H−10; ruler gets `eotg_mod_aug_inh_terms`; fire .022 (365) | 30; +30 forgiving, +10 compassionate |

**.025 The Seat** (to the heir, who now holds the titles. When the dead ruler was the player and the heir is the player's heir, the player continues as the heir by vanilla succession, so this is also the player's first event as the heir; same story role as .026, owner Q3). Root is the heir, whose risk is own-scope. Desc variants, each the heir's own belief and never "as I saw it would" (lore review): **ledger** "it went the way I had written it down"; **certain** "it went the way I'd already decided"; **rage/cold** a shared variant.

| Opt | Effect | AI |
|---|---|---|
| a "The seat was always going to be mine." | own risk +5; +100 prestige | 40; +20 callous, +10 arrogant |
| b "That wasn't a forecast. That was me." | own risk −10; stress major gain | 20; +20 compassionate, +10 honest |
| c "Take the seat." | own risk +0; +50 dread | 30; +20 ambitious, +10 wrathful |

**.026 The Warden's Hand** (to the heir, now ruler, and now the **player**, owner Q3; fires 3 days after the hand-off; `var:eotg_inh_old_ruler` on the heir). It is the tree's closing event: it names the old ruler, and the hand-off is told from the heir's side. Desc variants: a warden was installed (`has_active_diarchy = yes`), or none was (the quiet path, or the regency could not start).

| Opt | Variant | Effect | AI |
|---|---|---|---|
| a "Let [old_ruler] hold the controls a while." | warden | own risk −10 | 40; +15 humble, +10 content |
| b "I don't need a keeper." | warden | `end_diarchy = yes`; own risk +10; the old ruler gets `unease` | 20; +20 arrogant, +15 ambitious |
| a "Mine. Now it's mine." | none | own risk +10; +100 prestige | 30; +20 ambitious, +10 arrogant |
| b "Ask [old_ruler] to stay close." | none | own risk −5 | 30; +15 humble, +10 trusting |

**.027 The Line Shortens: L11.** Immediate, run by `eotg_inh_second`:
- the kinslayer effect with `VICTIM = scope:eotg_inh_heir`;
- `scope:eotg_inh_heir = { death = { death_reason = death_murder  killer = scope:eotg_inh_second } }`.
- **Unsanctioned** variant only: `add_secret = { type = secret_murder  target = scope:eotg_inh_heir }` on the second (vanilla `00_secret_types.txt:326`). When sanctioned, the ruler already knows.

The second becomes the primary heir by vanilla succession. Desc: sanctioned or unsanctioned. **"Sanctioned" is an internal name only** (lore review): the loc says "with your leave" or "without your leave". Coupling: the heir's tier change (death).

| Opt | Effect | AI |
|---|---|---|
| a "Let it stand." | sanctioned: no further effect. Unsanctioned: −50 prestige. Close. | 40; +15 callous, +10 content |
| b "Arrest [second]." | `imprison_character_effect` with `TARGET` the second; close | 30; +20 just, +10 paranoid |
| c "Execute [second]." | just; kinslayer on root; the second gets `death_execution` with `killer = root`; stress helper `murder`; `just` relief (`medium_stress_impact_loss`) only when `scope:eotg_inh_leave` is absent; close | 20; +25 just, +10 vengeful |

### 5.4 Mechanics that need more than a table row

#### 5.4.1 The next two in line (L13)

`eotg_aug_inherit_pick_line_effect` runs in the ruler's scope **before any death** (deaths reorder the line). **As built (2026-10-08):** it walks the exact places 1 to `eotg_aug_inherit_line_places`, lowest first, and fills `eotg_inh_next_1`, then `eotg_inh_next_2`, with the first two eligible people:
```
primary_title = {
    set_local_variable = { name = eotg_inh_line_place  value = 1 }
    while = {
        limit = { local_var:eotg_inh_line_place <= eotg_aug_inherit_line_places  NOT = { exists = scope:eotg_inh_next_2 } }
        eotg_aug_inherit_line_slot_effect = { PLACE = local_var:eotg_inh_line_place }   # random_title_heir at place = PLACE exactly
        change_local_variable = { name = eotg_inh_line_place  add = 1 }
    }
}
```
- **The bound is one script value:** `eotg_aug_inherit_line_places = { value = 6 }` in `common/script_values/eotg_augmentation_values.txt`. The pick (`eotg_aug_inherit_line_slot_effect`) and the eligibility test (`eotg_aug_inherit_line_eligible`) both read it, so "someone is eligible" and "the pick finds someone" can never disagree. Places 1–6, not 1–3: the wider window survives a line with a disinherited heir, a dead place or a skipped player in it. To retune, change only the value.
- **Eligible** (in both the slot effect and the trigger): alive, not the heir, not the ruler, and **`is_ai = yes`**. Players are skipped on **both paths**, tree and AI (orchestrator ruling 2026-10-08): L13 must never kill a human in multiplayer, whichever ruler's chain it is. A side effect: `eotg_inh_second`, which the scopes effect copies from `eotg_inh_next_1`, **can no longer be a player** (§5.3 .005, .015, .027).
- **Vanilla shape:** `disinherit_effect`, `common/scripted_effects/00_interaction_effects.txt:1620–1640`: `random_title_heir` with `$DISINHERITOR$.primary_title = { place_in_line_of_succession = { target = prev  value = 2 } }`. Place 1 is the primary heir. The trigger is documented in PX `triggers.log:8217` (title scope, `target`, comparison). The `while` on a local counter is vanilla `07_dlc_ep3_scripted_effects.txt:2814`.
- **Before a disinherit,** the heir is place 1, so the victims are the lowest two eligible places from 2 on. **After one** (from .013), the heir is out of the line, so they start from place 1. The single rule "the first two eligible who are not the heir" covers both.
- **Exact places, not a weighted random pick:** this replaces the earlier weighted `random_title_heir` draft, so the order follows the line. Whether place 1 is the primary heir and the places run in line order is still an in-game check (§9 V-13).
- The victims may be anywhere: at court, ruling elsewhere, or children. The murder is "arranged" and resolves in script, as vanilla murder schemes reach remote targets.
- **Effects in .016's `immediate`, for each saved victim:**
  - the heir runs the kinslayer effect on that victim;
  - the victim gets `death = { death_reason = death_murder_known  killer = scope:eotg_inh_heir }`. Vanilla `death_murder_known`: `bp1_yearly_events_claudia.txt:1919`, `ep3_contract_events.txt:8779`.
  - **Guarded** (`eotg_flag_aug_inh_guarded`, the ledger shown at .002 or .013's guard): a victim **at root's court** survives on a 50% roll and is wounded instead (`increase_wounds_effect`). Remote victims are not protected. **At least one victim always dies** whenever one exists: if both rolls would spare, the second roll is forced to kill. The required outcome is never voided.
- **Fewer than two:**
  - **One in line.** The single victim dies. Desc line `desc_one`: "There was only one name to cross out." H+10: the forecast the heir built ran past the list.
  - **None** (the heir is the only one in line). `eotg_aug_inherit_fire_threat_effect` never sends `next_two` here. It reroutes to `kill_ruler` (.018), because the only name left between the heir and the seat is the ruler's. The check is in the effect, not in .016's trigger, so .016 can never fire with an empty list.

#### 5.4.2 The massacre (L14)

The picker is `eotg_aug_inherit_strike_effect = { NAME = x }` in the ruler's scope. It has the body of `eotg_aug_pick_victim_effect` (family factor **0.25**, the Storm/Massacre convention from phase 0; knights ×1.5; under-16s ×0.25), plus:
- `NOT = { has_character_flag = eotg_flag_aug_inh_struck }` and `NOT = { this = scope:eotg_inh_heir }` in the limit;
- `add_character_flag = { flag = eotg_flag_aug_inh_struck  days = 1 }` on the pick.

The existing second-victim picker excludes only one person, so a massacre needs this one. `eotg_aug_victim_candidate` already excludes the Neurofractured, so it excludes the heir.

**Count:** 2 dead + 1 if the heir is in the Storm band + 1 for the rage profile − 1 when the ruler was ready (.009.d). Minimum 1, maximum 4. Then one wounded victim.
- Saved as `eotg_inh_dead_1` … `_4`, plus `eotg_inh_wounded`.
- Deaths: `death_murder_known` with `killer = scope:eotg_inh_heir`. No kinslayer for the heir: these are episode deaths, which the heir did not choose. Same rule as fracture.004's involuntary deaths (phase 0 M4 policy).
- **Loc names the first dead and the wounded survivor.** The variable `eotg_inh_dead_count` gives the total for a "[count] dead" line.
- **No candidates at all** (an empty court): the desc variant `desc_none` covers it. The ruler is wounded in place of the court (`increase_wounds_effect`), so the event still carries weight.
- **"From the ward":** if the heir is imprisoned, `release_from_prison` runs first. Precedent: the release effect on the prisoner, as index §2 lists.

#### 5.4.3 Excision on the heir (L1–L3)

`eotg_aug_inherit_excision_effect = { TABLE = … }` runs on the heir. It is written separately, not as a call to `eotg_aug_excision_surgery_effect`, because that effect reads `eotg_has_physician_access` and the Heir's Arc promise **on the patient**, and it fires end.002 to the patient. Here the **ruler's** physician operates. Weights:

| Outcome | physician | back | self |
|---|---|---|---|
| death (`death_treatment`) | 40 − 15 if the ruler has physician access | 50 | **45 − 15 if the ruler has `lifestyle_physician`** |
| survive, maimed | 30 | 40 | 30 |
| survive, clean | 30 + 15 if the ruler has physician access | 10 | **25 + 15 if the ruler has `lifestyle_physician`** |

**Why these numbers (revised 2026-10-08, lore-keeper flag).** The physician and back-street columns derive from end.001: its sanctioned table is `DEATH_BASE` 15 and its no-physician table 25 (`events/eotg_augmentation_endgame.txt:111, 202`), and `eotg_aug_excision_surgery_effect` adds +25 for a Neurofractured patient. That gives 40 and 50. The first draft's self column (30 / 30 / 40) had no derivation. It made the ruler's own hands, at `medium_gold_value` and with only `learning >= 14` required, safer than the paid physician's table at `major_gold_value` for any ruler without physician access. That inverts the purchase and contradicts .010's `desc_self`, which concedes that knowing the case "does not change the three ways this goes". Not intended.

The rule now: **the hands decide the self table.** A learned ruler without training (the `learning >= 14` gate) operates at 45 / 30 / 25: worse than a hired physician, better than a back-street fitter. A ruler with `lifestyle_physician` operates at 30 / 30 / 40, the first draft's numbers, kept for the case they fit. That is still slightly worse than the physician table with access (25 / 30 / 45), which the same ruler also qualifies for, because a full surgical team beats one pair of hands. The self table pays off through what it costs and what it does to the heir (`medium_gold_value`, H−3 at .003.d), not through better odds. Each column sums to 100 in every case: physician 40 / 30 / 30, or 25 / 30 / 45 with access; back-street 50 / 40 / 10 (the clean weight was 20 in an earlier draft, which summed to 110; corrected 2026-10-08, orchestrator ruling); self 45 / 30 / 25, or 30 / 30 / 40 with `lifestyle_physician`. The coerced and Storm modifiers below are added on top of these bases. The test is the ruler's own `lifestyle_physician`, not `eotg_has_physician_access`, because a court physician's employment says nothing about the ruler's hands.

Death +5 if `coerced` (the heir fought it). Death +10 if the heir is in the Storm band (this reads the resource). The survival branches run `eotg_aug_excision_effect`, the existing one: remove-all, `excised` marker, recovery, scar. The result is stored as `eotg_inh_table_result` for .021. The odds are surgical, as in end.001.

#### 5.4.4 Abdication (L9, L10)

`eotg_aug_inherit_abdicate_effect = { WARDEN = … }`. Run on the ruler. Same body as `eotg_aug_abdicate_effect` minus the restrained modifier and end.031: the old ruler here is sound.
1. `save_scope_as = eotg_inh_old_ruler_s`; the heir gets `set_variable eotg_inh_old_ruler`.
2. `is_ai = no` and the heir is AI → `set_player_character = scope:eotg_inh_heir`. Precedent: `tgp_dynastic_cycle_decisions.txt:2155–2170`. **The player follows the crown to the Neurofractured heir** (§11 Q3).
3. `depose = yes`. Precedent: `stress_threshold_events.txt:16775`.
4. WARDEN = yes: the heir runs `eotg_aug_start_containment_regency_effect = { KEEPER = scope:eotg_inh_old_ruler_s  SWING = 60 }`. That is the existing effect, with the **Q7 / CB-02 caveat** that a capable adult's regency may end early. If the effect cannot start (an ineligible government, or an existing diarchy), .026 shows its "none" variant. **The desc must hold on both paths.**
5. NOTIFY = yes: the heir gets `trigger_event = { id = eotg_aug_inherit.026  days = 3 }`. **Owner Q3:** the player now *is* the heir, and .026 is the tree's closing event from the heir's side. It must name the old ruler and make the hand-off read as story rather than as a character switch. Three days, not thirty, so the first thing the player sees as the heir is this event. The tree path always passes NOTIFY = yes. The ruler is always a player there, and the heir is always AI (gate), so `set_player_character` always runs.

#### 5.4.5 Routing into .009 after it has been seen

The route effect is a one-liner in each option: if `pattern_seen`, fire the threat; otherwise fire .009. The fire-threat effect:
1. `eotg_aug_inherit_roll_threat_effect` (no-op when preset);
2. `next_two` with no one eligible → `kill_ruler`;
3. `self` while the heir is in the ward (imprisoned) → `massacre`, as a breakout (`release_from_prison` first);
4. trigger the event.

#### 5.4.6 Death-reason choices

| Death | Reason | Vanilla source |
|---|---|---|
| the heir kills the ruler | `death_murder_known`, killer the heir | `00_event_deaths.txt`; ep3_contract_events.txt:8779 |
| the next two | `death_murder_known`, killer the heir | as above |
| the massacre | `death_murder_known`, killer the heir | as above |
| the ruler kills the heir in secret (.009.e) | `death_murder`, killer root | mod precedent fracture.txt:187 |
| executions (.016.b, .024.a, .027.c) | `death_execution`, killer root | vanilla, as heir.004 kill_c |
| the guards cut the heir down (.017.b) | `death_slaughtered_by_guards`, killer root | `00_event_deaths.txt:971` |
| surgery | `death_treatment` | `00_event_deaths.txt:214` |
| the heir's own end, cold | `death_suicide` | `00_event_deaths.txt:243` |
| the heir's own end, other profiles | `eotg_death_cascade` | mod (phase 3b) |
| the sibling's coup | `death_murder`, killer the second | vanilla |

---

### 5.5 The AI path: one hidden event (owner Q5, 2026-10-06)

#### 5.5.1 Who gets the tree

`eotg_aug_inherit_tree_runs` is `is_ai = no` on the ruler, and nothing more.

The owner left the wider gate to the architect: also run the tree when the heir or the ruler is the player's close family or direct liege. **Decided: no.** The tree's events go to the *ruler*, so an AI ruler's tree is invisible to the player whoever the player is related to. The full tree would cost 4–7 events and show the player nothing that .028 doesn't. Telling a related player what happened is a notification, deferred in §10 (now cross-referenced to this rule).

The heir is never a player (§5.1 gate), so `tree_runs = no` means no player is root of any event in the chain. Because .028 fires 30–180 days after the start, it re-checks `tree_runs = no` in its own trigger and hands a ruler who became a player to .001 (§5.5.2, §5.5.4).

**Throttle:** unchanged (×0.4 county, ×0.55 duke, ×0.7 king+ for AI). Precedent, cited by the owner: vanilla `random_yearly_playable_pulse` `chance_of_no_event` 30 / 70 for AI kings and dukes, "No need to waste performance here" (`common/on_action/yearly_on_actions.txt:3022-3037`). Ours is a single hidden event, so the lighter throttle is kept.

#### 5.5.2 .028 Resolution (hidden)

```
eotg_aug_inherit.028 = {
    type = character_event
    hidden = yes                               # vanilla court_yearly.1001 (events/yearly_events/court_yearly_events.txt:331)
    trigger = {
        eotg_aug_inherit_tree_runs = no            # re-check: the ruler may have become a player in the 30-180 day wait
        eotg_aug_inherit_chain_valid = { FULL = yes }
    }
    on_trigger_fail = {
        if = {
            limit = { eotg_aug_inherit_tree_runs = yes  eotg_aug_inherit_chain_valid = { FULL = yes } }
            trigger_event = eotg_aug_inherit.001   # the new player gets the tree
        }
        else = { eotg_aug_inherit_close_effect = yes }
    }
    immediate = {
        eotg_aug_inherit_scopes_effect = yes
        random_list = { <the 15 branches below; each runs its leaf effect, then the AI default> }
        eotg_aug_inherit_close_effect = yes
    }
}
```

**Weights.** Each branch has a base, additive `modifier`s and `factor = 0` gates. They are read from the stored profile and bond, the heir's band and the ruler's traits, so they track what the tree's choices and rolls produce. Each branch also has `modifier = { factor = 1000  var:eotg_inh_force_leaf ?= flag:<key> }` for testing. These are **first-pass numbers for the observer run** (§9 item 13), not a balance claim.

| Branch key | Leaf | Base | + | Gate (×0) / × |
|---|---|---|---|---|
| `excise` | L1 / L2 / L3 (the surgery roll decides) | 15 | ruler has physician access +15; diligent +10; brave +10; `coerced` n/a | gold < `medium_gold_value` |
| `terms` | L4 | 15 | cold +10; favourite +20; dutiful +10; ruler compassionate +10, forgiving +10 | ×0.25 certain; ×0.25 rival; ×0.5 estranged; ×0.5 rage |
| `confine` | L5 | 15 | ruler paranoid +10, craven +10, just +5; rage +5; cold +10 | — |
| `exile` | L6 | 10 | ruler craven +5, content +5; estranged +10 | — |
| `disinherit` | L7 | 10 | cold +20; dutiful +10; ruler just +10 | ×0.5 rival |
| `transit` | L8 | 3 | ruler deceitful +10; ruler intrigue ≥ 14 +5 | gold < `medium_gold_value` |
| `abdicate_warden` | L9 | 3 | ruler content +5, humble +5; ruler age ≥ 60 +10 | the .005.b validity test fails; ruler ambitious |
| `abdicate_quiet` | L10 | 1 | ruler trusting +3; ruler age ≥ 60 +5 | as above; ruler paranoid |
| `coup` | L11 | 0 | +15 if `scope:eotg_inh_second` passes the .005.d test; claimant +5; ruler callous +5 | no qualifying second |
| `heir_end` | L12 | 5 | cold +20; heir `stress_level >= 2` +5; favourite +5, dutiful +5 | ×0.25 certain |
| `next_two` | L13 | 5 | ledger +20; claimant +10 | nobody eligible in the line (§5.5.4) |
| `massacre` | L14 | 5 | rage +20; heir Storm band +10, Fracture +5; estranged +5 | — |
| `attempt` | L15, or L17 on failure | 5 | certain +20; rival +15; estranged +5 | ×0.5 favourite |
| `ruler_cascade` | L16 | 2 | ruler ambitious +5, eccentric +5 | ruler not `eotg_is_aug_tier3`; ruler content |
| `kill_heir` | L17 | 3 | ruler callous +10, sadistic +10 | ruler compassionate |

The heir's band enters through `massacre` and through the surgery's death odds, so .028 **reads** the resource. Every branch's leaf effect moves the heir's risk or changes a tier. That is the invariant 5 coupling (§9 item 3).

#### 5.5.3 Leaf effects (shared with the tree)

Each leaf's mechanics live in one scripted effect. The tree's leaf options call the same effect, so the same outcome has the same consequences on both paths. **The tree options keep only what is option-specific:** extra opinion, stress helpers, gold choices and follow-up `trigger_event`s. Every leaf effect sets `var:eotg_inh_outcome` on root.

| Effect | Leaf | Called by (tree) | Called by .028, then the **AI default** for the follow-up options |
|---|---|---|---|
| `eotg_aug_inherit_leaf_excise_effect = { TABLE }` (pay, then `eotg_aug_inherit_excision_effect`, store the result) | L1–L3 | .010 a / b | `excise`: TABLE `physician` if `employs_court_position = court_physician_court_position` and gold ≥ `major_gold_value`, else `back`. Follow-up (.021): none. |
| `eotg_aug_inherit_leaf_terms_effect` (heir sedated + reassured, ruler `eotg_mod_aug_inh_terms`, H−15) | L4 | .006 a, .020 b, .024 c (the tree adds the .022 follow-up) | `terms`. No .022 a year later on the AI path. |
| `eotg_aug_inherit_confine_effect = { TYPE }` (imprison, sedated on house arrest) | L5 | inside the ward effect; .016 a, .017 a / c | `confine`: TYPE `house_arrest` (the .008 a default, base 40 over b's 25). No breakout roll: the breakout's outcome is weighted into `massacre` instead. |
| `eotg_aug_inherit_leaf_exile_effect = { STYLE }` (`plain` / `credit` / `disinherit`) | L6 | .011 a / b / c, .003 b_ref, .013 leave a | `exile`: STYLE `plain` (.011 a; credit only if gold ≥ `medium_gold_value` and the ruler is generous) |
| `eotg_aug_inherit_leaf_disinherit_effect = { COST }` (vanilla `disinherit_effect`, H−5; COST = yes adds −150 prestige) | L7 | .007 a (`no`), .013 immediate (`yes`) | `disinherit`: COST `no` when the profile is cold or the bond dutiful (a renunciation), else `yes` |
| `eotg_aug_inherit_leaf_transit_effect` (the .012 a body, exposure roll included; the toast is guarded on `is_ai = no`) | L8 | .012 a | `transit` |
| `eotg_aug_inherit_abdicate_effect = { WARDEN  NOTIFY }` | L9 / L10 | .014 a / b (`NOTIFY = yes`) | `abdicate_warden` / `abdicate_quiet` with `NOTIFY = no` |
| `eotg_aug_inherit_leaf_coup_effect = { LEAVE }` (the .027 immediate) | L11 | .015 a (`yes`) / b (`no`) | `coup`: LEAVE 50/50 (`random`). Follow-up AI default: .027 a (let it stand). |
| `eotg_aug_inherit_leaf_heir_end_effect` (the .019 immediate: suicide when cold, else cascade; ruler stress) | L12 | .019 immediate | `heir_end`. Follow-up: none (the .019 options are only stress and opinion). |
| `eotg_aug_inherit_leaf_next_two_effect` (pick the line, then the deaths; §5.4.1) | L13 | .016 immediate | `next_two`. Follow-up AI default: .016 a, custody (confine `dungeon`, no breakout). |
| `eotg_aug_inherit_leaf_massacre_effect` (pickers, deaths, wounded, emptied-court modifier; §5.4.2) | L14 | .017 immediate | `massacre`. Follow-up AI default: .017 a, take the heir alive (confine `dungeon`). |
| `eotg_aug_inherit_leaf_attempt_effect = { MOD  NOTIFY }` (the .018 roll; on success the ruler dies; NOTIFY fires .025; on failure the ruler is wounded and NOTIFY fires .024) | L15 | .018 a / b / c (`NOTIFY = yes`, MOD per option) | `attempt`: MOD −15 (the .018 a default, "Guards!", base 40). On failure the AI default is .024 a (execute), so the leaf is **L17** through `kill_heir` REASON `execution`. NOTIFY `no`. |
| `eotg_aug_inherit_leaf_ruler_cascade_effect` (`eotg_trigger_neurofracture` on root, heir H−20, mutual admiration, arc-done flag) | L16 | .020 a | `ruler_cascade`. The cascade's own fracture.0001 still fires to the AI ruler, as any AI cascade does. |
| `eotg_aug_inherit_leaf_kill_heir_effect = { REASON }` (`murder` / `execution` / `guards`; kinslayer on root first) | L17 | .009 e, .013 c (`murder`); .016 b, .024 a (`execution`); .017 b (`guards`) | `kill_heir`: REASON `execution` |

**The AI-default rule** for any follow-up choice not listed: the option with the highest base `ai_chance`; on a tie, the less lethal option.

#### 5.5.4 AI-path rules

- **No player is killed off-screen, and no player is killed by L13 at all.** The L13 line pick (§5.4.1) requires `is_ai = yes` in both `eotg_aug_inherit_line_slot_effect` and `eotg_aug_inherit_line_eligible`, on **both paths** (orchestrator ruling 2026-10-08; earlier drafts excluded players on the AI path only). A player in places 1–6 (`eotg_aug_inherit_line_places`) is skipped and the next eligible person is taken. With nobody eligible, the `next_two` branch is gated out (×0) here, and on the tree path `next_two` reroutes to `kill_ruler` (§5.4.5). Massacre victims are courtiers, who are never players. The L15 victim is the AI ruler.
- **The ruler can become a player while .028 waits** (30–180 days: inheritance by a player, a character switch). .028's trigger re-checks `eotg_aug_inherit_tree_runs = no`. Its `on_trigger_fail` fires .001 if the ruler is now a player and `eotg_aug_inherit_chain_valid = { FULL = yes }` still holds, so the player gets the tree; otherwise it closes the chain (§5.5.2).
- **No visible event, toast or tooltip** reaches anyone on the AI path. Vanilla's own death and imprisonment notifications to related players still fire, and they are the only window.
- **Map outcomes match the tree.** Titles (disinherit, abdication, regency), deaths (with the same reasons and killers), traits, modifiers, opinions, the secret on an unsanctioned coup, and kinslayer all come from the shared leaf effects.
- **Exclusivity and cleanup** are identical to the tree: §5.2 guards, `on_trigger_fail`, and the close effect at the end of `immediate`.

## 5A. Variation

### 5A.1 The profile: how the Neurofracture shows

Rolled once in `eotg_aug_inherit_start_effect` and stored as `var:eotg_inh_profile`, as a `random_list` in the heir's scope. Shape: the flag variable is the mod's Patron terms (`eotg_aug_patron_accept_effect`). Weights come from vanilla traits and from the existing Neurofractured distortion modifier, which `eotg_apply_neurofracture_distortion` applies by the heir's highest skill.

| Profile | Key | What it looks like (for the text) | Base | + | × 0.5 if |
|---|---|---|---|---|---|
| **Running Hot** (violent rages) | `flag:rage` | breakage, bruised attendants, a hand that closes before the heir means it to; apologies afterward | 20 | wrathful +25, impatient +10, `eotg_mod_nf_martial_distortion` +15, prowess ≥ 12 +10, heir in the Storm band +10 | calm |
| **The Ledger** (paranoid forecasting) | `flag:ledger` | the heir keeps lists of who stands where and who is next. The heir **trusts the implant's half-beat forecast of the heir's own body, and has started applying the same certainty to other people.** The certainty is the heir's, never the machine's (§8). | 20 | paranoid +25, deceitful +10, `eotg_mod_nf_intrigue_distortion` +15 | trusting |
| **Flatline** (cold detachment) | `flag:cold` | the heir stops eating with the court and answers in complete, polite, empty sentences; nothing is wanted | 20 | callous +20, shy +10, content +10, `eotg_mod_nf_learning_distortion` or `_steward_distortion` +15 | compassionate |
| **Certainty** (grandiose) | `flag:certain` | the heir gives orders to the ruler's guards and is obeyed twice before anyone checks; speaks of "when I hold the seat" | 20 | arrogant +20, ambitious +20, `eotg_mod_nf_diplomacy_distortion` +15 | humble |

### 5A.2 The bond: what the heir is to the ruler

Set by `first_valid` from vanilla relations and opinion, read at entry and not re-read. A bond can't change mid-chain, so a desc stays true. Stored as `var:eotg_inh_bond`.

| Order | Bond | Condition |
|---|---|---|
| 1 | `flag:rival` | the heir `has_relation_rival = root` OR `has_relation_potential_rival = root` |
| 2 | `flag:estranged` | heir `opinion = { target = root  value <= -25 }` |
| 3 | `flag:claimant` | the heir is ambitious AND `opinion = { target = root  value < 20 }` |
| 4 | `flag:favourite` | root `has_relation_friend` / `_best_friend` / `_soulmate` with the heir, OR root's opinion of the heir ≥ 40, OR the heir's opinion of root ≥ 50 |
| 5 | `flag:dutiful` | fallback |

Bond lines say "your child" only under `is_child_of = root`, and "your heir" otherwise. The heir may be a sibling, a niece or a cousin. Never invent a relation (gemini feedback §4).

### 5A.3 Matrix: profile and bond × events, options and odds

**Which events and options appear:**

| | Running Hot | The Ledger | Flatline | Certainty |
|---|---|---|---|---|
| .001 desc | broken cup, bruised attendant | lists in the heir's quarters | an untouched plate, a too-polite note | the heir countermanding the guard roster |
| .002 profile option | p_rage "Sit with [heir] until it passes." → .006 | p_ledger "Show me the list." → .005 + guarded | p_cold "Do you want to stop?" → .007 (+30) | p_certain "You don't rule yet." → .009 (kill_ruler) |
| .004 desc (what the watcher saw) | a smashed panel | a list with the ruler's spouse on it | the heir sitting in the dark for a whole shift | a petitioner told to "come back when I'm seated" |
| .006 refusal line | "I'll break the terms. You know I will." | "You'd only be next on it." | "There's nothing to agree to." | "Terms are for people who might lose." |
| .007 | refuses 75% | refuses 85%; refusal marks the heir | **accepts 70%** | refuses 95% |
| .009 threat most likely | **massacre** | **next_two** | **self** | **kill_ruler** |
| .019 variant | cascade death | cascade death | **suicide** | cascade death |
| .025 desc (if they killed the ruler) | "it happened before I…" | "it went the way I had written it down" | — | "it went the way I'd already decided" |

**Threat weights** (`eotg_aug_inherit_roll_threat_effect`; a preset skips the roll):

| Threat → event | Base | Rage | Ledger | Cold | Certain | Bond | Other |
|---|---|---|---|---|---|---|---|
| `kill_ruler` → .018 | 15 | +0 | +10 | +0 | **+35** | rival +25, estranged +15, claimant +15, favourite −10 | ×0.5 guarded |
| `massacre` → .017 | 15 | **+40** | +5 | +0 | +10 | estranged +5 | heir Storm +15; Fracture +5 |
| `next_two` → .016 | 10 | +5 | **+40** | +0 | +10 | claimant +20 | heir `marked` +25; ×0 if nobody is in the line |
| `self` → .019 | 10 | +0 | +0 | **+40** | ×0.25 | favourite +10, dutiful +10 | heir `stress_level >= 2` +10 |

**After .013 the violent reaction presets the threat:** ledger or claimant → `next_two`; certain or rival → `kill_ruler`; rage → `massacre`. Flatline never rolls violent (below).

### 5A.4 Hidden rolls (all through `eotg_aug_inherit_roll_effect`; clamp 5–90)

| Roll | Where | Base | Profile | Bond | Other |
|---|---|---|---|---|---|
| heir refuses the physicians | .003 immediate | 0 | rage 20, ledger 40, cold 5, certain 30 | favourite −15, rival +20 | +20 coerced; 0 if sent from .006.b |
| heir accepts terms | .006 immediate | 50 | rage −15, ledger −10, cold +10, certain −20 | favourite +25, dutiful +10, claimant −10, estranged −20, rival −30 | +15 gentle; +10 if the heir is in Flicker; forced pass from .007.b / .009.c |
| heir renounces | .007 immediate | 0 | rage 25, ledger 15, cold 70 (+30 from p_cold), certain 5 | dutiful +15, favourite +10, claimant −20, rival −20 | −10 if the heir is in Storm |
| reaction to being struck out | .013 immediate | random_list | accept: base 40, cold +30, certain −20 · leave: 25, rage +10 · violent: 15, ledger +25, certain +25, rage +20, **cold ×0** | accept: dutiful +15, favourite +10, rival −20 · leave: estranged +20 · violent: rival +20 | violent +15 via .007 refuse a |
| ward breakout | ward effect | 0 | rage 30, certain 15, ledger 10, cold 0 | — | +15 heir Storm; ×0.5 dungeon; ×0.5 heir sedated |
| arrest succeeds | .009.a | 70 | rage −20, certain −10 | — | +10 guarded; +10 the ruler has a marshal (`cp:councillor_marshal`) |
| talk-down succeeds | .009.c | 0 | cold +10, rage −10 | favourite 60, dutiful 45, claimant 25, estranged 20, rival 10 | +10 the ruler is compassionate |
| the attempt on the ruler succeeds | .018 option | 45 | certain +10, rage +10 | — | heir prowess ≥ 12 +10; ruler prowess ≥ 12 −10; guarded −20; ruler ready −20; option modifier (§5.3) |
| the second acts anyway | .015.b | 15 | — | — | 40 if the second is ambitious OR intrigue ≥ 12 |
| the lost shuttle is exposed (a witness saw the heir alive) | .012.a | 25 | — | — | −10 ruler intrigue ≥ 14; +10 a spymaster is not employed |

**Toasts** for a roll the ruler did not see resolve: `.009.a_fail_tt` (the arrest failed), `.012.exposed_tt`, and `ward_breakout_tt` ("The ward's door was found open."), which fires with .017 when it comes from the ward. Shape: `send_interface_toast`, as balance §5.4.

### 5A.5 Why two playthroughs differ

- **4 profiles × 5 bonds = 20 openings.** Each one changes .001's desc, the option set at .002 (exactly one profile option shows), .004's desc, .006's refusal line and .018's words.
- **The middle depends on who the heir is.** Flatline almost never reaches a violent threat. Certainty almost never accepts terms. The Ledger is the only profile whose list can be read early (p_ledger) and guarded against.
- **The ruler's traits and skills gate 13 options.** Compassionate, callous, paranoid, wrathful, brave, sadistic, just, vengeful, arbitrary, forgiving and diligent; `lifestyle_physician` or `learning >= 14`; `intrigue >= 14` or deceitful; and the ruler being Overclocked. A playthrough sees roughly a third of the gated options.
- **The resource feeds back.** An heir made worse in the middle (watched, coerced, refused) reaches .009 in a higher band, which raises the massacre weight and the surgery's death odds.

---

## 6. Vanilla precedent

| What | Vanilla file | Used for |
|---|---|---|
| multi-stage court chain without a story cycle | `events/court_events/court_events_general.txt` (court.2201 and its children; disinherit option at :1663 / :1750) | the chain mechanism, disinheriting an heir in an event |
| `disinherit_effect = { DISINHERITOR = root }` | `common/scripted_effects/00_interaction_effects.txt:1507` | L6c, L7, L8, .013 |
| line of succession | the same file :1620–1640 (`random_title_heir` + `place_in_line_of_succession`); PX `ordered_title_heir` | the next two (§5.4.1) |
| `on_trigger_fail` | `events/activities/coronation_activity/coronation_events.txt:3942` | chain cleanup (§5.2) |
| kinslayer | `00_secret_effects.txt:433` `add_kinslayer_trait_or_nothing_effect` | every chosen family killing |
| secret murder | `common/secret_types/00_secret_types.txt:326` `secret_murder` | the unsanctioned coup |
| death reasons | `common/deathreasons/00_event_deaths.txt` (suicide :243, slaughtered_by_guards :971, treatment :214) | §5.4.6 |
| `death_murder_known` with a killer | `events/dlc/ep3/ep3_contract_events.txt:8779` | public murders |
| abdication and the player hand-off | `stress_threshold_events.txt:16775` (`depose`); `tgp_dynastic_cycle_decisions.txt:2155–2170` (`set_player_character`) | L9 / L10 |
| regency | `events/bookmark_events.txt:2247`, through the mod's containment effect | L9 |
| an heir kills the owner, the event to the killer | mod heir.005 (phase 3 §4), itself from vanilla murder outcomes | L15 + .025 |
| massacre picker, family factor | mod fracture.004 + `eotg_aug_pick_victim_effect` | L14 |
| AI tier throttle | `common/on_action/yearly_on_actions.txt:3022-3030` | §5.1 |
| `move_to_pool` | mod end.011 | L6, L8 |
| hidden resolution event | `events/yearly_events/court_yearly_events.txt:331` (`court_yearly.1001`, `hidden = yes`, trigger + immediate) | .028 |
| AI performance throttle | `common/on_action/yearly_on_actions.txt:3022-3037` (`chance_of_no_event` 30 / 70 for AI, "No need to waste performance here") | §5.5.1 |

**Deviations:**
- The excision helper is a separate effect, not a call to the existing one, because the patient is not the payer (§5.4.3).
- The massacre picker is new, because the existing one excludes only one victim (§5.4.2).
- **Not a deviation (2026-10-08):** an option gated on `OR = { trait_a trait_b }` carries one `trait = ` line per gating trait, so every icon shows. Vanilla does this in `events/harm_events.txt` harm.0551.b (event at :2259). Scripter deviation 10, which showed one icon, is reversed.
- `banish` is **not** used for exile. Vanilla uses it on prisoners (`00_prison_interactions.txt`) and in a tooltip on a tournament guest (`tournament_events.txt:16356`). Its side effects on a free courtier-heir are unverified, and `move_to_pool` is already proven in the mod.

---

## 7. Loc surface (eotg-localizer)

File `localization/english/eotg_aug_inherit_l_english.yml`, UTF-8 **with BOM**, Canadian English, dot-form keys. **About 226 keys**:

| Group | Keys |
|---|---|
| .001 | `.t`; `.desc_rage/_ledger/_cold/_certain`; `.bond_rival/_estranged/_claimant/_favourite/_dutiful`; `.src_cascade/_report`; `.a–.e` (17) |
| .002 | `.t`; `.desc_×4`; `.bond_×5`; `.a .b .c .p_rage .p_ledger .p_cold .p_certain .d` (18) |
| .003 | `.t`; `.desc_flicker/_fracture/_storm`; `.desc_refused`; `.a–.d`; `.a_ref .b_ref` (11) |
| .004 | `.t`; `.desc_×4`; `.a–.d` (9) |
| .005 | `.t .desc .desc_second`; `.a–.d` (7) |
| .006 | `.t .desc_accept`; `.refuse_×4`; `.a .b .c .ra .rb` (11) |
| .007 | `.t .desc .accept .refuse`; `.a .b .ra .rb` (8) |
| .008 | `.t .desc .a .b` (4) |
| .009 | `.t`; `.desc_kill_ruler/_massacre/_next_two/_self`; `.a–.e`; `.a_fail_tt` (11) |
| .010 | `.t`; `.desc_physician/_back/_self`; `.coerced`; `.a .b .c` (8) |
| .011–.015 | about 5 each, plus `.012.exposed_tt` (26) |
| .016 | `.t .desc_ledger .desc_neutral .desc_one .child`; `.a .b .c` (8) |
| .017 | `.t .desc .from_ward .ready .killed .wounded .none`; `.a .b .c` (10) |
| .018 | `.t`; `.desc_×5 bond`; `.a .b .c`; `.fail_tt` (10) |
| .019 | `.t .desc_cold .desc_cascade .a .b .c` (6) |
| .020–.027 | about 6 each (48) |
| shared | `eotg_aug_inherit.route_threat_tt`; `ward_breakout_tt`; 5 or 6 hidden-roll tooltips (8) |
| modifiers | `eotg_mod_aug_inh_terms` (+`_desc`), `eotg_mod_aug_inh_emptied_court` (+`_desc`) (4) |

**Placeholders:**
- The bare form only: `[eotg_inh_heir.GetFirstName]`, `[eotg_inh_heir.GetSheHe]`, `[eotg_inh_second.GetFirstName]`, `[eotg_inh_dead_1.GetFirstName]`, `[eotg_inh_witness.GetTitledFirstName]`, `[ROOT.Char.Custom('eotg_court_seat')]` for the seat word. **Never `[scope:…]`.**
- The heir is always a saved scope. Do not use `GetHeir`, which characters lack (feedback correction 2026-10-06).
- One scoped person takes `GetSheHe` / `GetHerHis` / `GetHerHim`, never "they".
- Unscoped people are rephrased so they need no pronoun.

**Vanilla `replace/` strings:** none. The vanilla death-reason, trait and modifier loc is reused unchanged.

**Every desc must be true on every path that shows it** (feedback §4):
- .006's accept desc is shown both after a roll and after a forced pass (.007.b, .009.c), so it must not say the heir was persuaded "at last".
- .016's desc must work with one victim, and only `desc_ledger` may mention a list.
- .017's base desc must work for an empty court.
- .026's warden desc is shown only when `has_active_diarchy = yes`.
- .021's maimed desc must not name a body part.
- .019.b "Tell the court it was a cascade." is true on the cascade variant and a lie on the cold one, so the option text must read right on both.

**Length:** descs about 45–80 words; options 5–9 words. Each event names at least one character besides the ruler. Witnesses come from saved scopes, never invented.

### 7.1 Lore wording fixes (eotg-lore-keeper, 2026-10-06; binding on the localizer)

*(Note 2026-10-08: speech in these lines is rendered with inner unescaped `"` (event_quality_v1 §12.2); narration is first person per §12.1. The approved wording itself is unchanged.)*

The option texts quoted in §5.3 are working text. Where this list differs, **this list wins.**

| Where | Use |
|---|---|
| "tonight" (3 places) | .001.d "I'll go to [heir] myself, before the next watch."; .009.a "Arrest [heir] before the next watch."; .022 slipping a "Then we start again. Now." |
| the ward, `TYPE = dungeon` | "the cells" |
| the ward, `TYPE = house_arrest` | "confined to quarters" |
| .018.c | "Face [heir] yourself." |
| .013.b (leave) | optional: "Bring [heir] back under guard." |
| "Bury" | "Lay [heir] to rest…" (.019.a, .021 dead a) |
| .006 rage refusal line | "I'll break the terms. You know I will." |
| .006 refuse a | "Then the council decides." |
| .025.a | "The seat was always going to be mine." |
| .026 none a | "Mine. Now it's mine." |
| .018 bond descs (5) | at most **one** spoken line from the heir per variant |
| .016.child (owner Q1) | the child's death is off-screen and in plain words: one sentence, the name and the fact. No method, no age emphasis, no scene. |
| .011 | "Passage Out": a paid berth on an outbound ship; b is "passage and credit". No destination, Unclaimed region or polity. Keep "[heir] is still in the line". |
| .012 | lost in transit ("the shuttle never docked"); exposure is a witness (a dockhand or a fitter) who saw the heir alive. "Residence logs" is allowed. Never a registry, records office or certificate. |
| .016 | `desc_ledger` is the only desc that mentions a list; `desc_neutral` is "[heir] had worked out who stood between [heir_herhis] and the seat." |
| .019 | cascade variant "[heir] died in a neural cascade"; .019.b "Tell the court it was a cascade." Never "the hardware". |
| .025 desc | ledger "it went the way I had written it down"; certain "it went the way I'd already decided". Never "as I saw it would". |
| .027 | "with your leave" / "without your leave". Never "sanctioned". |
| `eotg_mod_aug_inh_terms_desc` | "The realm's vassals do not trust a succession that rests on [heir]'s terms holding." Succession risk, never taint or shame. A modifier desc may not resolve an event scope; if it does not, write "your heir's terms". |

**The L12 desc (.019)** shows a death that is found, not a death in progress:
- clinical past tense;
- no method, no discovery scene, no last words;
- about 45 words.

Sample (lore-keeper): "[witness] found [heir]'s quarters in perfect order. [heir] had answered every message, settled every account, and left nothing unfinished but [heir_herself]." Write the placeholders in bare-scope form, e.g. `[eotg_inh_heir.GetHerselfHimself]`. The witness is `eotg_inh_witness`, with a no-witness fallback such as "The attendants found…".

**Also binding:**
- "half a second" stays banned in loc. Use the §8.1 tells instead.
- **The profile names are internal.** "Running Hot", "The Ledger", "Flatline" and "Certainty" never appear in player-facing text. If a label is ever needed for the cold profile, use "Flat Affect".

---

## 8. Lore constraints

Sources: SETTING LORE ERRATA "CYBERNETIC VOICE" (2026-10-03) and "CYBERNETICS AT 866" (2026-10-04); index §5 items 1–6; gemini feedback §2–§3.

1. **The heir's "voice" is a forecast of the heir's own body and choices, a beat early.** It is never prophecy and never foresight of other people's plots. The Ledger's lists are **the heir's belief**: certainty borrowed from a machine that is right about one person only. Allowed tells:
   - the heir's hand is on the cup before the heir reaches for it;
   - the heir stops mid-sentence, as if the end had already been said;
   - "I knew I'd say that."

   **Not allowed:** "it told me", "it showed me what you'll do", "the implant warned me".
2. **Never the Void.** The banned list from index §5.2 applies in full (Void, Orrin, Kyros, the Eye, whisper, "at the edge of hearing", possess, demon, pact, abyss, frenzy, "grip" as a metaphor, Carrigore, and the rest). The heir is not possessed; the heir is breaking.
3. **Medicine is clinical and local.** Clinics, physicians and back-street fitters. Seller names come only through the existing custom-loc placeholders. Nothing is licensed by a named body, and no authority sits above the realm (ERRATA "LAW AT 866").
4. **No remote kill, no off switch** (Blackstar, 1300). The heir cannot be "shut down": containment is chemical (sedation), physical (a ward) or surgical (excision).
5. **No mind upload or stored self** (c. 1825). The faked death is a person hidden away, nothing more.
6. **Multi-species and faith-neutral.** Use "self" and "personhood", never "human"; no monotheistic invocations. .019.a's burial is "as my heir", with no rite named.
7. **The setting is space-faring:** residence, quarters, the cells, the docks, the audience chamber, corridors, by the next watch. Gemini feedback §3's banned list applies (no castle, throne room, parchment, knight as a rank, horses, seasons, times of day).
8. **The overused phrases are off-limits:** "No one…", "the hardware" as a crutch, "the work" for surgery, "half a second", "It is not…".

**For the lore-keeper (non-blocking):**
- ~~Does a public stigma fit 866?~~ **Resolved (lore review 2026-10-06):** the −5 stays, framed as succession risk, never taint or shame. The desc wording is in §7.1.
- Is suicide as an outcome acceptable in tone? This is also owner Q2.

---

## 9. Definition of done

0. **Tiger, `px_lsp_diagnostics.js` and `px_vocab_check.py` all clean** on the touched files, except the known-benign list in `CLAUDE.md` §Validation. Tiger is the only one that checks scope.
1. **Reachability:** all 28 events are reachable (PX event graph + `px_event_report.py`). .001 (player) and .028 (AI) are fired from `eotg_aug_inherit_start_effect`, which is called by `eotg_on_yearly_aug_inherit_check` (`yearly_playable_pulse`, count+) and by `eotg_aug_nr_cascade_effect`. Everything else is fired from a chain stage. No event is fired by nothing.
2. **Lesson 5:** no event `trigger` reads `eotg_flag_aug_inh_cooldown`. `grep -n "eotg_flag_aug_inh_cooldown" events/` is empty.
3. **Invariant 5:** each of the 28 events moves the heir's `eotg_fracture_risk` in at least one option, reads the heir's band, or changes a tier (the heir's death or excision, or the ruler's cascade). The risk moves 1+ times in at least **20 events**. QA audit 8.
4. **Leaves:** all **17** leaf outcomes in §5.3 are reachable on the tree path, and all **15** branches of .028 on the AI path, with the recipes below. This includes **L13, L14 and L15** on both.
5. **Exclusivity:** with a live Heir's Arc at stages 0–4, the tree does not start. While the tree runs, neither Heir's Arc start site creates a story.
6. **Cleanup:** after every leaf and every `on_trigger_fail`, the ruler has no `eotg_inh_*` variable and no chain flag. Only the cooldown, `buried_empty` and the heir's `seen` remain.
7. **Hidden risk:** no tooltip shows a number, "risk", "pressure" or odds.
8. **Loc:** every key in §7 exists once, BOM present, no `[scope:`, Canadian spelling, no banned word (QA greps the §8 list).
9. **Victims:** L13 names its victims. L14 names its first dead and its wounded survivor. `random_courtier` appears only in the witness pick and inside the new strike picker.
10. **The AI path is silent.** .028 has `hidden = yes`. For an AI ruler, `eotg_aug_inherit_start_effect` fires .028 and never .001. No event in the chain has an AI ruler as root other than .028, apart from the existing fracture.0001 after L16.
11. **Leaf parity.** Each of the 15 leaf effects (§5.5.3) is called from .028 **and** from at least one tree event. .028 contains no outcome mechanics inline: grep its `immediate` for `death =`, `disinherit_effect`, `imprison`, `depose`; all must be empty.
12. **No player killed by L13:** the line pick excludes players on both paths. `is_ai = yes` is in both `eotg_aug_inherit_line_slot_effect` and `eotg_aug_inherit_line_eligible`, and both read `eotg_aug_inherit_line_places` (§5.4.1, §5.5.4). .028's trigger contains `eotg_aug_inherit_tree_runs = no`.
13. **Observer run** (balance §9.2): after 50 years, read `eotg_inh_outcome` on every ruler that has it. All 15 branches occur at least once. The three required leaves (L13, L14, L15) together are 15–40% of AI outcomes. Count the .028 firings per decade against the throttle. Retune §5.5.2 if any branch is absent or above 30%.
14. **Owner Q3:** after L9 / L10 on the tree path, the player is the heir and .026 is the first event they see, within 3 days.

### 9.1 Console recipes (debug mode; `docs/qa/HOW_TO_TEST_IN_GAME.md`)

**Setup (all leaves).** Play a count whose primary heir is an adult, unlanded AI courtier.
1. Make the heir Neurofractured and start the tree:
   - through the cascade hook: `effect primary_heir = { eotg_aug_initiate_effect = yes  add_trait_xp = { trait = eotg_cybernetics value = 100 }  eotg_aug_nr_cascade_effect = yes }`;
   - or directly: `effect primary_heir = { add_trait = eotg_neurofractured }`, then `effect eotg_aug_inherit_start_effect = { SOURCE = report }`.
2. Force the variation: `effect eotg_aug_inherit_debug_effect = { PROFILE = rage  BOND = dutiful  THREAT = none }`. It overwrites the profile and bond, and sets the threat only when it is not `none`.
3. Force every hidden roll: `effect set_variable = { name = eotg_inh_force  value = flag:pass }` (or `flag:fail`). Remove it with `effect remove_variable = eotg_inh_force`.
4. Set the heir's band: `effect primary_heir = { set_variable = { name = eotg_fracture_risk value = 70 } }` (10 Flicker / 45 Fracture / 70 Storm).
5. Skip delays: the console command `event` with the node's id (for example `event eotg_aug_inherit.010`) re-fires a node to yourself (the variables are already set). If a node's scopes are missing, re-run step 1.

| Leaf | Profile / bond / force | Path (options) |
|---|---|---|
| L1 clean excision | any / any / pass, physician employed | .001 b → .003 a → .010 a → .021 (clean needs the roll; run with `pass`, then repeat to see variety) |
| L2 maimed | any / any | as L1. To see it, re-roll, or set `eotg_inh_table_result = flag:maimed` before .021. |
| L3 dies on the table | any / any / risk 70 | .001 b → .003 c → .010 a (back-street; repeat for the death roll) |
| L4 reconciled | cold / favourite / pass | .001 a → .002 a → .006 a → wait 365 or `event eotg_aug_inherit.022` |
| L5 confined | cold / any / fail (no breakout) | .001 b → .003 b → .008 a → .023 |
| L6 exiled | any / any | .001 c → .004 b → .011 a |
| L7 disinherited | cold / dutiful / pass | .001 a → .002 p_cold → .007 a |
| L8 faked death | any / any; ruler intrigue ≥ 14 (`effect add_intrigue_skill = 15`) | .001 c → .004 d → .012 a |
| L9 abdication with warden | any / any | .001 e (be callous: `effect add_trait = callous`) → .005 b → .014 a → .026 as the heir |
| L10 quiet abdication | any / any | as L9, .014 b |
| L11 sibling's coup | any / any; second in line is an ambitious adult AI | .001 c → .004 c → .005 d → .015 a → .027 |
| L12 heir's death | cold / dutiful / THREAT = self | .001 c → .004 a → .009 b → .019 (suicide variant). With rage → cascade variant. |
| **L13 next two** | ledger / claimant / THREAT = next_two; 3+ people in the line | .001 c → .004 a → .009 b → .016. Repeat with only 1 person in the line (desc_one), and 0 (reroutes to .018). |
| **L14 massacre** | rage / estranged / THREAT = massacre; risk 70 | .001 c → .004 a → .009 b → .017. Also via the ward: .003 b → .008 a with `force = pass` (breakout) → .017 "from the ward". |
| **L15 heir kills the ruler** | certain / rival / THREAT = kill_ruler / pass | .001 a → .002 p_certain → .009 b → .018 a → (the ruler dies) → .025 as the heir |
| L16 ruler chooses Neurofracture | any / favourite / pass; ruler Overclocked (`effect eotg_aug_initiate_effect = yes`, then `add_trait_xp … 100`) | .001 a → .002 a → .006 c → .020 a |
| L17 ruler kills the heir | any / any; ruler callous | .001 c → .004 a → .009 e |

**Exclusivity checks:**
- **V-14:** be Neurofractured with the Heir's Arc at stage 1 (`event eotg_aug_heir.001`); run the on_action. The tree must not start.
- **V-15:** with the tree running, set risk ≥ 30 on yourself while Neurofractured and wait a pulse. No Heir's Arc story appears.

**V-13:** the line ordering in §5.4.1 picks the lowest two eligible places (places 2 and 3 when the heir is place 1 and nobody is skipped), not random title heirs. Check with 4+ people in the line. Then put a second player (or a test switch) at place 2 and confirm the pick skips to places 3 and 4.

**AI path (.028).** Pick an AI count whose primary heir is an adult, unlanded AI courtier; hover the count for their id `X`.
1. `effect character:X = { primary_heir = { add_trait = eotg_neurofractured } }`.
2. `effect character:X = { eotg_aug_inherit_start_effect = { SOURCE = report } }`. It must schedule .028 and **not** .001 (DoD 10). Check that `character:X` now has `eotg_inh_heir`.
3. Force a branch: `effect character:X = { set_variable = { name = eotg_inh_force_leaf  value = flag:massacre } }`, using any §5.5.2 key. A gated branch (×0) stays 0 under the force, which also tests the gates. Optionally force the profile and bond with `effect character:X = { eotg_aug_inherit_debug_effect = { … } }`.
4. Resolve now: `event eotg_aug_inherit.028 X`. The scheduled copy later fails its trigger and closes harmlessly.
5. Check:
   - `eotg_inh_outcome` on X;
   - the heir's and the victims' state in the character window (dead with the §5.4.6 reason, imprisoned, disinherited, gone from court);
   - for `abdicate_*`, the heir now holds X's titles and **you were not switched** (X was AI);
   - no chain variable or flag remains on X except the cooldown and `eotg_inh_outcome`.

| Branch | Extra setup |
|---|---|
| `excise` | gold ≥ `medium_gold_value` on X (`effect character:X = { add_gold = 500 }`); a physician for the `physician` table |
| `terms`, `confine`, `exile`, `disinherit`, `heir_end`, `massacre`, `kill_heir` | none (set `eotg_fracture_risk` 70 on the heir to see the Storm weights) |
| `transit` | gold as above |
| `abdicate_warden` / `_quiet` | X not ambitious (`effect character:X = { remove_trait = ambitious }`) |
| `coup` | X's second in line is an adult ambitious AI |
| `next_two` | 3+ people in X's line. Repeat with **you** in the line (play a landed sibling): you must be skipped (DoD 12). |
| `attempt` | force `eotg_inh_force = flag:pass` (L15: X dies) and `flag:fail` (L17: the heir is executed) |
| `ruler_cascade` | X Overclocked (`effect character:X = { eotg_aug_initiate_effect = yes  add_trait_xp = { trait = eotg_cybernetics value = 100 } }`) |

---

## 10. Deferred

| Cut | Why |
|---|---|
| **Landed heirs** (a vassal heir) and **heirs at another court** | Confinement, exile and the conversation all assume the heir is at the ruler's court. A landed heir needs war or a revoke path. The gate excludes both; build later on the same chain. |
| **A player heir** | The heir's choices are resolved in script. Running them as player events needs a second perspective for every node. |
| **The faked-death return beat** (the heir "lost in transit" reappears years later) | `eotg_flag_aug_inh_buried_empty` and the heir's `eotg_aug_inh_presumed_dead` are set now, so it can be built without a migration. New event; it's the owner's call. |
| **Faith-gated reactions to the heir's suicide** (prestige or piety by doctrine) | Canon gives no culture or faith a stance on suicide, so .019 is value-neutral now (lore review). Gate it on doctrines once v2 faiths exist from the region briefs. |
| **A vanilla secret for the faked death** | It needs a new `common/secret_types/` entry and folder. Not worth it for one leaf now. |
| **Notifications to other players or rulers** (e.g. a liege told of a vassal's massacre, or a player told what .028 decided about their relative) | Vanilla-shaped, but it is new events. With Q5's ruling this is the only way a player could see an AI occurrence beyond vanilla's death notices (§5.5.1). |
| **Reactions from the heir's spouse or children** | They would widen the cast past the 28 events. A later pass can add them as desc lines. |
| **A visible story-panel entry** | The hidden-risk rule; the system's stories are all invisible. |

---

## 11. Owner questions: ruled 2026-10-06

All five were answered by the owner on 2026-10-06, following the recommendations from community and vanilla research.

| # | Question | **Ruling** | Reason | Design change |
|---|---|---|---|---|
| Q1 | Child victims in L13 | **Allow.** Off-screen, plain wording. | Vanilla murder has no target age gate, and `murder_outcome` has child and infant variants. The game's T / PEGI 12 rating covers text references. | §7.1 row `.016.child` (one plain sentence, no scene). |
| Q2 | The heir's suicide (L12) | **Keep as framed.** | Vanilla `death_suicide` exists, trait-gated and oblique. Ours is limited to a Flatline adult heir and is never the player. | None. The lore review's value-neutral .019 and the L12 desc rule (§7.1) stand. |
| Q3 | Abdication passes play to the heir | **Keep.** | Players dislike a game over far more than a character switch. The heir needs a closing event, so the switch reads as story. | §5.4.4: .026 fires in 3 days, not 30, and names the old ruler from the heir's side. .025 plays the same role after L15. DoD 14. |
| Q4 | The cascade hook replaces nr.006 for the primary heir | **Yes.** | One cascade, one event. | None (§5.1 site B as specced). |
| Q5 | AI rulers run the full tree | **Changed: no.** The full tree runs only when the player is involved. AI-only occurrences resolve in one hidden event at entry, by a weighted `random_list` with the same profile and bond weights and the same leaf effects. Keep the tier throttle. Leaves that need a player choice with no AI analogue take the AI default from the matrix. | Performance. Precedent: vanilla `random_yearly_playable_pulse` `chance_of_no_event` 30 / 70 / 95 for AI ("No need to waste performance here"). | New §5.5 (.028, the 15 shared leaf effects, AI defaults, no off-screen player death). "Involved" is decided as **the ruler is a player** only (§5.5.1, with the reason). §3, §6, §9 updated. |

---

### HANDOFF (2026-10-08, build deltas)
- status: done (spec synced to the 2026-10-08 QA fixes; one design correction to the excision odds)
- next: eotg-scripter
- ask: In `eotg_aug_inherit_excision_effect` (`common/scripted_effects/eotg_augmentation_effects.txt`, about :3651–3682), apply the revised self column of §5.4.3. Death branch: add `modifier = { add = 15  scope:eotg_inh_table_kind = flag:self }` and `modifier = { add = -15  scope:eotg_inh_table_kind = flag:self  scope:eotg_inh_ruler = { has_trait = lifestyle_physician } }`. Clean branch: change the self modifier from `add = 10` to `add = -5`, and add `modifier = { add = 15  scope:eotg_inh_table_kind = flag:self  scope:eotg_inh_ruler = { has_trait = lifestyle_physician } }`. Update the inline comments (death "self 45 (30 with lifestyle_physician)", clean "self 25 (40 with lifestyle_physician)"). The maimed branch is unchanged. .028 never uses `self`. Then re-run Tiger and PX on the file.
- files: docs/specs/cybernetics_v2_fracturing_inheritance.md
- needs-loc: none required. Optional for eotg-localizer: `eotg_aug_inherit.010.desc_self` already reads as no better than the odds, so it fits. No key change.
- needs-lore: none (this answers the lore-keeper's flag)
- needs-human: none new; V-13 now also checks the player skip

### HANDOFF (2026-10-06, original)
- status: done (lore review and owner rulings of 2026-10-06 applied; nothing open)
- next: eotg-scripter
- ask: Build the spec: §3 identifiers (28 events, the 15 shared leaf effects, `eotg_aug_inherit_tree_runs`), §5.1 entry (the on_action, plus the `eotg_aug_nr_cascade_effect` hook), §5.2 guards in the two Heir's Arc start sites and the non-ruler step 5, the §5.3 tree for player rulers, the §5.5 hidden .028 for AI rulers, and the §5A profile, bond and roll tables. Then run §9 items 0–3 and 10–11 statically. Hand loc keys to eotg-localizer (§7, with §7.1 binding).
- files: docs/specs/cybernetics_v2_fracturing_inheritance.md
- needs-loc: about 226 keys in the new `localization/english/eotg_aug_inherit_l_english.yml` (§7, §7.1). .028 is hidden and needs no loc.
- needs-lore: none
- needs-human: in game: the §9.1 recipes (17 tree leaves, 15 AI branches), V-13 line ordering, V-14/V-15 exclusivity, Q7/CB-02 regency persistence for L9, DoD 14 (.026 after the switch), and the observer run's leaf distribution (DoD 13)
