# Spec: Frontier Systems v1 (Phase 1 core)

**Author:** cloud agent (architect role), 2026-10-04. **Status: owner rulings applied (2026-10-04, §R). Phase 1 is being built on the remaining defaults.** The questions still open are listed in [`frontier_v1_open_questions.md`](frontier_v1_open_questions.md).
**Source of intent:** [`docs/design/frontier_systems.md`](../design/frontier_systems.md) (the owner's brief, cited below as *design §n*). This spec records the implementation decisions; the brief is not edited.
**Taskboard:** CB-37. **Gate:** 3 (Systems), built as a **mod-exclusive system against the vanilla/temporary map** (`docs/agent_workflow.md` §5 rule 2). It is not blocked by Gate 1, and it is map-agnostic (§1).
**Written without game files.** This was a cloud session with no vanilla 1.20 files, no Tiger and no PX. Every engine claim carries a confidence and a source in §0. Anything not confirmed by the mod's own verified v2 script is **UNVERIFIED-VANILLA** and appears in §16, "Verification list for the local session".

**Sources used, by precedence** (CLAUDE.md):
1. `docs/pitfalls.md`.
2. The CLAUDE.md invariants and the catalog lessons.
3. Vanilla game files. These were not available here, so every claim that needs them is flagged.
4. The ck3-modding skill (github.com/Sililex/ck3-claude-skill, cloned read-only outside the repo; `reference/common/*/*.info`).
5. `OLD PROJECT VERSION/docs/CK3_Modding_Complete_Reference_v1_19.md`, as a last resort.

Shape examples come from the mod's verified v2 script: `common/*/eotg_augmentation_*` and `events/eotg_augmentation_*.txt`.

**Size (Phase 1, proposed):**
- **Events: 6 required + 1 optional.** The owner approves the count (§9).
- **Decisions: 5 player/AI + 2 debug.** No events behind Abandon or Withdraw.
- **Custom on_actions:** 2 internal + 8 integration hooks, mostly empty.
- **Scripted effects and triggers:** about 18 effects, 10 triggers and 12 script values.
- **Modifiers:** 7 static county modifiers.
- **Story cycles:** none. No traits, no new holding types, no gfx.
- **Loc:** about 120 keys.

---

## V. Verification fixes (2026-10-04): these override §R, §B and everything below

From [`frontier_v1_verification.md`](frontier_v1_verification.md) (local lore, QA and engine pass) and the owner's §4 decisions. The per-item table is in `docs/handoffs/cloud_2026-10-04_frontier-fixes.md`.

- **Pacing doubled (owner):** about **10–16 years unsponsored, 8–10 sponsored**.
  - The yearly gain sum is multiplied by `eotg_frontier_pace_value` = 0.5. Every input keeps its relative weight.
  - One-off gains are halved too: Invest +5, .002 "push through" +4, an accepted backing +3.
- **Strain rescaled with the pacing:** hidden **0–8** (was 0–4). Failure is at `eotg_frontier_strain_fail_value` = 8. The .002 desc bands are 4 and 6, and the AI gates are Invest ≥ 4, Abandon ≥ 6. .005 restart sets strain 4; the backer branch sets 2.
  - Per-cause +1 and the quiet-year −1 are unchanged, so a cause held for the same share of a project fails it equally often.
  - **Flavor cooldown 3 years (owner decision, follow-up):** `years = 3` in `eotg_frontier_event_roll_effect`. Expect about **4–5 flavor events per typical project** (10–16 years, one roll at most every 3 years). That is the ceiling; with the roll's 50% "nothing" weight a project often sees fewer.
- **One record of active Frontiers (Q-B1):**
  - `eotg_frontier_active_count` is superseded (removed). `eotg_frontier_ai_room` reads `any_in_global_list = { variable = eotg_frontier_active count >= cap }`.
  - Every .001–.005 option that changes a Region re-checks its state. Start, complete, abandon and restart are guarded by a state `limit`.
  - .002, .004 and .005 carry a "The moment has passed" option, shown only when the Region has left the Frontier state.
- **Founder validity (Q3, orchestrator ruling):** alive, adult and free, plus one of:
  - is the holder;
  - is in the holder's realm (employer, or vassal or below);
  - **the holder is vassal or below of the founder.**
- **Relative development floor (Q4):** the floor is `min(type floor, eotg_frontier_dev_reachable)`.
  - `eotg_frontier_dev_reachable` = starting development + the milestone development this Region has not yet been granted, recorded at start.
  - At full Establishment with a floor unmet, the stage modifier becomes `eotg_frontier_mod_waiting_development` / `_waiting_control`. The Invest tooltip says so too.
- **Milestone development once per Region, ever (Q5):** permanent history `eotg_frontier_dev_granted` (0–2). Abandon keeps its −1.
- **Tick (Q9):** a calendar-year marker, `eotg_frontier_tick_year = current_year`, replaces the 300-day `eotg_frontier_ticked` (superseded). That gives exactly one tick per in-game year.
- **Sponsor death (E2; orchestrator ruling, follow-up):** an additive `on_death` → `eotg_frontier_on_sponsor_death` records the dying sponsor's `primary_heir` on the Region as `eotg_frontier_pending_heir` (and the dead backer as `eotg_frontier_pending_from`) and clears the sponsor. Vanilla reads `primary_heir` of the dying only there, but the heir has usually not inherited yet, so `eotg_frontier_can_sponsor` would fail. The Region's **next yearly tick** (`eotg_frontier_resolve_pending_heir_effect`) makes the heir the sponsor if they are alive, can sponsor (which includes backing nothing else) and are not the holder, firing `sponsor_changed`; otherwise the backing lapses (Sponsor Lapse, strain +1). A backer found in between wins with no lapse; an heir who now holds the Region is dropped with no strain. The pending variables are removed either way, and when the project ends.
- **Sponsor never the holder (§R rule):** `eotg_frontier_check_sponsor_effect` drops a sponsor who has become the holder (inherited or was given the Region), with no strain.
- **Holding build (E1):** both the check and the pick need `has_holding = no` and `barony_cannot_construct_holding = no`. The grant runs at character scope.
- **Hooks (Q8):**
  - `progressed` fires only on a real gain;
  - `development_changed` fires only where development changed;
  - `settled` and `abandoned` go through `eotg_frontier_trigger_hook_effect`, with the scopes saved before the clear.
- **Saved-scope hygiene (Q2):** absent hook scopes are cleared, and `old_sponsor` is cleared before reuse. Internal scopes are temporary.
- **Debug readout (approved test tooling):** `eotg_decision_frontier_debug_readout` toasts each held Frontier's progress, strain and floors.
- **Text:** time-neutral in any period of the setting (owner rule). S1 ("A Hard Year") and R3 (the sponsor credit line) are applied; S2 (Exodus) is not.
- **Markers:** every item the verification confirmed has lost its UNVERIFIED-VANILLA marker. Three behaviours are `# TEST-IN-GAME`: V1 (variables persist), V8 (the barony a new holding creates) and V12 (scopes reach custom on_actions). They're in `frontier_v1_test_plan.md` §0.
  - **New in this pass, since confirmed against vanilla 1.20.0.3 (markers dropped):**
    - `current_year` as a set_variable value (game_start.txt:987-991); the comparison uses vanilla's orientation, `current_year > var:eotg_frontier_tick_year` (00_empire_faith_gate_triggers.txt:234);
    - `development_level` / `county_control` as values in county scope (03_dlc_fp2_script_values.txt:88-91);
    - `[x.MakeScope.Var('name').GetValue|0]` in the debug toast's loc (coronation_activity_l_english.yml:675).

---

## R. Owner rulings (2026-10-04): these override anything below

- **Terminology (Q1).** Follow the glossary:
  - **Region** = the county. A **Frontier Region** is a county in the Frontier state.
  - **System** = a barony or holding, so a new holding is a **new System**.
  - **Frontier** = the Region's developmental state. A **Frontier Project** is an attempt to establish something in the Region.
  - **Player text shows the fiction, never the implementation:** "Systems remain open for settlement here", never "empty holding slot".
- **Events (Q2).** 6 core events: .001–.005 and .010. **The founder-death event (.006) is cut.**
  - A founder who becomes **invalid** (dead, imprisoned, a child, or otherwise unable) is just the strain cause **No Founder**, detected by the yearly tick.
  - The player replaces the founder through a variant of .002, *The Frontier Without a Founder* (§9). It is the same event id, so the count stays at 6.
- **The new holding (Q12)** always goes to the **current county holder**, the political owner. **The founder and sponsor never own the result by default.** The founder's reward is prestige, gold or recognition (the .004 options), never the holding.
- **The architectural rule.** The **Region** owns the Frontier state. The **current county holder** owns the Region politically. The **Founder** starts the project. The **Sponsor** supports it. These are four distinct things and are never collapsed. There is no Greater Drift dependency; later systems consume Frontier through the Sponsor input and the hooks.
- **Engine fallbacks are binding.**
  - **County-title variables (V1).** Use them if they work and persist (test plan: mark, start, save and reload, change the holder, kill the founder). Otherwise use the **story-cycle fallback**. **The state never moves onto the founder.**
  - **Holding creation (V8).** If it isn't reliable, every type uses the development/control fallback. It does not block the feature.
  - **Hooks (V12).** If on_actions can't be fired with their scopes, they become empty scripted effects. Greater Drift behaviour is never hard-coded.
- **The values.** Progress is hidden at 0–100 and strain at 0–4. Players see consequences ("progressing / struggling / at risk / thriving / abandoned"), never numbers. Strain is never a random roll.
  - **The five named causes stay:** No Founder, Low Control, Occupation, War, Sponsor Lapse.
  - **Hardship** (strain from an event choice) is kept as a sixth label so that .005 can always name a cause. This needs confirmation; see the open questions file.
- **Abandoned:** resettlable, keeps its traces, and gives a modest head start. As specified.
- **AI:** a cap of 8 active frontiers on the map, at most 1 per ruler. As specified; tune later.
- **Lore (§15 answered).**
  - **Exodus settlers are allowed.** REVIEW_866 dates the Exodus from 131 AG and has it ongoing at 866, so "Exodus arrivals" and "Exodus descendants" are both canon-safe.
  - **Older ruins, derelict stations and lost colonies are encouraged**, especially in Research text. Ruins do not mean the Region was politically settled.
  - **Avoid "charter"** where it implies an authority above the polity. Prefer foundation, establishment, expedition, venture, outpost, grant.
  - **No named factions.**
  - **No Void** in Research text.
  - **The register:** people establishing themselves in a vast, partly developed galaxy, not a central colonial authority.

**Design consequences applied in the build (and below):**
- **Founder and sponsor validity are read by the yearly tick.** The `on_death` hook and the per-character county lists are dropped. That removes dependencies E2 and E6.
- **Sponsor validity:** superseded by §V (E2): `on_death` records the heir and clears the sponsor; the next tick hands the backing to the heir or records **Sponsor Lapse**.
- **A founder is valid when** alive, adult, not imprisoned, and either the county holder or living in the holder's realm.
- **Withdraw and Sponsor** find their counties through the global list `eotg_frontier_active`.

---

## B. Build notes (Phase 1 as built, 2026-10-04): where the script differs from the sections below

These are small simplifications made while building. Each keeps the architecture.

1. **`eotg_frontier_mark_unsettled_effect` takes no `DEV_LOSS`.** A parameter that subtracts development has no safe text form when it is 0. The cartographer lowers development separately when the real map lands (D3).
2. **`eotg_frontier_abandon_effect` takes `FAILED = yes|no`, not `CAUSE`.** The cause is already recorded in `eotg_frontier_last_cause`.
3. **Type eligibility:** one shared trigger, `eotg_frontier_can_establish`, plus `eotg_frontier_admin_eligible` for Administrative. A `$TYPE$` switch would need identifier substitution (V14). The data rows (rate, floors, results) are if/else_if chains on `var:eotg_frontier_type` (the mod's verified shape), not `switch`.
4. **.001** has one option per type plus "Not now". The founder is the decision's candidate (the best steward at court, or the taker). The "lead it yourself" and "another Region" re-fires were cut to keep .001 simple.
5. **.005 option c** "Scale it back" switches the type to Settlement (the generic type) rather than re-opening the type pick.
6. **The sponsor carries one back-reference variable,** `eotg_frontier_sponsoring` (the Region). That makes "is this character a sponsor?" correct in any scope; a global-list search would read `root` wrongly from another character's scope. It is written only by the set/clear sponsor effects. **The Frontier state itself stays on the Region.**
7. **(Superseded by §V, Q-B1: the counter is gone; the cap reads the list.)** The AI-cap count was a global variable, `eotg_frontier_active_count`. The global list `eotg_frontier_active` is used only for iteration (Sponsor, .010).
8. **The decision picture** uses one vanilla illustration path (UNVERIFIED). This system adds no gfx.
9. **Completion and failure events go to AI holders too,** who choose by `ai_chance`. That is fewer code paths than a separate AI resolution. .002 goes to players only; AI-to-AI sponsor offers resolve in script.
10. **Loc:** 118 keys. They were checked against eotg_lint L003, L010 and L011, and against the round-4 rules L013 (house style) and L014 (unused keys): 0 findings.

---

## 0. Engine facts

Confidence key:
- **H**: used by the mod's own v2 script, which is verified against 1.20.
- **M**: in the skill reference or v1 script, but not yet seen in v2.
- **L**: believed from general CK3 knowledge, with no source available here.

Every M and L fact is in §16.

| # | Fact | Source | Conf. |
|---|---|---|---|
| E1 | The yearly hook is `yearly_playable_pulse`. Extend it via `on_actions = { }` in our own file; `on_yearly_playable` is dead. | CLAUDE.md inv. 4; catalog §4.13; `common/on_action/eotg_augmentation_on_actions.txt` | H |
| E2 | `on_death` can be extended additively. Root is the dying character, who is still alive inside the hook. | `eotg_augmentation_on_actions.txt` (on_death → custom); skill `story_cycles.md` ("while they're still alive") | H |
| E3 | `set_variable = { name = x value = <scope or flag:y or number> days/years = n }`, plus `has_variable`, `var:x`, `change_variable` and `remove_variable`, work on **character** scopes. | eotg_augmentation_effects/triggers | H |
| E4 | The same variable effects work on **landed_title** scopes, and title variables persist across holder changes. | skill `variables.md` (variables on "any scope that supports them"); not used on titles in v2 | M |
| E5 | Global variable lists: `add_to_global_variable_list`, `remove_list_global_variable`, `every_in_global_list` / `random_in_global_list` / `any_in_global_list` / `ordered_in_global_list = { variable = x }`, and a size trigger. | eotg_lint knows `add_to_global_variable_list` (L001 setter list); iterators from general knowledge | L |
| E6 | Character variable lists `add_to_variable_list` / `every_in_list = { variable = x }` can hold title scopes. | `add_to_variable_list` used by the mod; title scopes unverified | M |
| E7 | `add_county_modifier = { modifier = x years = n }` (or bare `= x`), and `remove_county_modifier`, `has_county_modifier`, run on a county title scope. | v1 `eotg_legacy_effects.txt:51-77`; reference v1_19:1043 | M |
| E8 | `change_county_control = n` runs on a county title. | `common/buildings/eotg_temple_citadel_buildings.txt:257` | H (effect exists) |
| E9 | `change_development_level = n` runs on a county title. | v1 `eotg_elven_expanded_events.txt:254` (`capital_county = { change_development_level = 1 }`) | M |
| E10 | The `development_level` and `county_control` triggers run on a county title. | `common/buildings/*` (as a modifier key), v1 events | M |
| E11 | **A county always has a holder.** CK3 has no unheld county with land (uncolonised wasteland is an impassable province, not a county). Every holding slot that is filled has a barony title holder. Empty barony slots (`has_holding = no` on the province) are normal. | general CK3; skill `holdings.info` names `has_holding` | M |
| E12 | Script can **create a holding in an empty barony slot**: on the province, `set_holding_type = city_holding \| castle_holding \| church_holding`. Who then holds the new barony title is UNVERIFIED (the county holder, or nobody until granted). | general knowledge only | **L** |
| E13 | `create_character = { template/location/culture/faith … save_scope_as }`, then `add_courtier`. | `eotg_augmentation_effects.txt:1367-1374` | H |
| E14 | A barony is granted with `create_title_and_vassal_change` + `change_title_holder = { holder = X change = scope:change title = Y }` + `resolve_title_and_vassal_change`. | v1 uses `create_title_and_vassal_change` (3 files); exact shape unverified | M |
| E15 | Decision fields: `is_shown`, `is_valid`, `is_valid_showing_failures_only`, `cost`, `effect`, `ai_check_interval_by_tier` (every tier key required), `ai_potential`, `ai_will_do`. | `common/decisions/eotg_augmentation_decisions.txt` header and body | H |
| E16 | `debug_only = yes` is a trigger that is true only when the game runs in debug mode. Usable in a decision's `is_shown`. | skill `_decisions.info:72` (named inside an `is_valid` example) | M |
| E17 | `trigger_event = { on_action = <custom on_action> }` fires a custom on_action from script, keeping root and any saved scopes. | general knowledge | **L** |
| E18 | `every_held_title` (character → titles) with `tier = tier_county`. | general knowledge | **L** |
| E19 | `send_interface_toast` and `custom_tooltip` render text in event and decision tooltips. | eotg_lint TOOLTIP_KEYS; v2 events | H |
| E20 | Vanilla gold script values `minor_gold_value` / `medium_gold_value` / `major_gold_value` (realm-relative). | `eotg_augmentation_decisions.txt` header; v2 triggers | H |
| E21 | **Great projects** (`common/great_projects/types/`) are an engine framework with founder, owner, province, `cost`, `construction_time`, `is_valid`, `on_complete` and `on_cancel`. Its DLC gating, if any, is unknown. Considered and **not chosen** for Phase 1 (§2 option C). | skill `reference/common/great_projects/types/_great_project_types.info` | M (schema) / unknown (gating) |
| E22 | A story cycle is owned by a character. It ends on owner death unless `on_owner_death` hands it on (`make_story_owner`). | skill `story_cycles.md:56-61`; the mod's 4 story cycles | H |
| E23 | A character that died stays a valid scope (`is_alive = no`). A variable holding them still resolves. | general knowledge; v2 relies on it (`var:eotg_heir = { is_alive = no }` in `eotg_augmentation_stories.txt`) | H |
| E24 | The neighbor iterators `random_neighboring_top_liege_realm_owner` and `random_ally` exist for characters. | general knowledge | **L** |
| E25 | `random_county_province` / `every_county_province` (county → its provinces), and `title_province` (barony → province). | general knowledge; reference v1_19:458 (`title:c_paris.title_province`) | M |

**Contradictions noted between sources** (precedence followed):
- **Story cycles:** the v1_19 reference (§12) teaches `start_story` / `on_monthly` / `should_end`. The mod's verified v2 story cycles use `create_story` and `effect_group`. v2 wins; this spec uses no story cycle anyway.
- **Title keys:** `OLD PROJECT VERSION/CONTRIBUTING.md` still shows title keys as `eotg_k_cauldron`, the v1 form that cost the map. CLAUDE.md invariant 2 (tier-first) wins. This spec creates no titles.

---

## 1. Purpose and gate

- **The loop:** Unsettled → Frontier → Settled, with Abandoned as a resettlable dead end (design §3).
- **What it adds:** a temporary developmental state on a county. It holds a Project (type, Founder, Sponsor, hidden progress) that ends in **normal CK3 outcomes**: a holding, development, control, a local character, a time-limited county modifier.
- **What it doesn't add:** no government, claims, factions, culture or religion system, and no title hierarchy (design §2.2, §20).
- **Map-agnostic:** no title, province, culture, faith or character keys anywhere.
  - The Unsettled status is **data**: a variable plus a modifier on the county title.
  - On the vanilla map, a debug-only decision creates it (§8.5). After Gate 1, the cartographer marks counties through the same one effect (§2.3, deferral D3).
- **Standalone:** it works with no other EotG system present (design §25). It reads no cybernetics, void or government state.
  - **Out of scope:** Greater Drifts, Corporations, Exploration, Patronage and the Nikios Khanate. None is referenced, beyond the generic hooks in §7.

---

## 2. Unit, state storage, and what "Unsettled" means

### 2.1 The unit: the county, which players see as a Region

**The unit is the county (`c_` title), and players see it as a Region** (ruling Q1, following the glossary in `OLD PROJECT VERSION/docs/localization_crusade.md`).
- **Why the county:** **development** and **county control**, the two CK3 values the design wants progress driven by (design §8), live on the county.
- **Settling:** a Frontier Region is settled **System by System**. Its free barony slots are the Systems still open to settlement, and a completed project establishes one of them as a new holding (§5.3).
- **Player text** never mentions slots or holdings counts (§R).

### 2.2 Where the Frontier state lives: options

| Option | Holds state in | Survives founder death | Survives owner change | Cost |
|---|---|---|---|---|
| **A. County title variables + county modifiers** (recommended) | `var:eotg_frontier_*` on the `c_` title; a tier modifier on the county for display | yes (the founder is just a variable) | yes (title variables persist, E4) | needs E4 verified |
| B. A story cycle per frontier, owned by the founder or holder | story variables | only with an `on_owner_death` hand-off; the owner must be a character (E22) | needs a hand-off on every holder change, or the story dies with the wrong person | a hand-off for every case; finding a county's story means iterating stories |
| C. A vanilla **great project** (E21) | the engine project object | the engine keeps a founder **and** an owner | owner rule `province_owner` | **DLC gating unknown** (lesson 12); project UI and illustrations needed (Gate 4); behaviour on cancel and invalidation untested |
| D. Capital province variables | `var:` on the province | yes | yes | development and control live on the county, so this doubles the scope hops; a capital-barony change would orphan it |

**Recommendation: A.**
- **The state belongs to the place.** The founder, sponsor and holder can all change while the place stays the same, and only the title outlives all three.
- **Cost of the choice:** if E4 is false, B is the fallback. A story owned by the county holder, with `on_owner_death` → `make_story_owner = story_owner.primary_heir`, and an `on_title_lost` hand-off (more UNVERIFIED).
- **C is deferral D6** for a Phase 2 look-and-feel pass, once its gating is known.

### 2.3 "Unsettled" in engine terms: options

The engine needs every county to have a holder and a capital holding (E11). So Unsettled cannot mean "nobody here".

| Option | What an Unsettled county is | Settling means | Risks |
|---|---|---|---|
| **(a) A normally held county flagged Unsettled** (recommended) | an ordinary county with its capital holding and holder, plus `var:eotg_frontier_state = flag:unsettled` and the county modifier `eotg_frontier_mod_unsettled` (low output, slow control growth: "no recognized settlement yet"). Its **empty barony slots** are the systems not yet settled. | the project's completion builds a holding in an empty slot where the type calls for one (E12), raises development and control, and adds a time-limited modifier | E12 (holding creation) is the one L-confidence dependency. Fallback: a type whose slot effect fails gives development and control only (§5.3). |
| (b) The county's only holding is minimal | needs a new, near-empty holding type (`common/holdings/`, buildings, a game concept, an icon) | upgrading the holding type | new holding type, gfx and loc (Gate 4); `can_be_inherited` and holding-swap rules unverified; too heavy for Phase 1 |
| (c) A county with no holder | not possible in the engine (E11) | — | — |

**Recommendation: (a).**
- **It is the design's own reading.** Unsettled "does not necessarily mean literally empty" (design §3.1). It means no *recognized permanent settlement*. A county whose capital is, say, a mining camp or a beacon fits that.
- **Display:** the "camp" exists only as the modifier name and description.
- **Entry point:** the single effect `eotg_frontier_mark_unsettled_effect` (county scope). It optionally drops development by `$DEV_LOSS$`, the one map knob for the cartographer later.

**Behaviours the local session must verify for (a)** (in §16): E11 (empty slots are normal, and `has_holding` exists); E12 (`set_holding_type` on an empty slot, and who holds the new barony); E7, E8, E9 and E10 (development and control effects and triggers on a county scope); E25 (iterating a county's provinces).

### 2.4 State variables (all on the county title)

| Variable | Values | Meaning |
|---|---|---|
| `eotg_frontier_state` | `flag:unsettled` / `flag:frontier` / `flag:abandoned` | **Absent = a normal, settled county.** No `flag:settled` state is kept: Settled *is* normal CK3 (design §3.3). |
| `eotg_frontier_type` | `flag:settlement` / `flag:trade` / `flag:mining` / `flag:military` / `flag:religious` / `flag:research` / `flag:administrative` | The project type, present while Frontier. |
| `eotg_frontier_progress` | 0–100 (hidden) | **The signature resource, "Establishment"** (§6). |
| `eotg_frontier_strain` | 0–8 (hidden; §V) | Pressure toward failure (§6.3). |
| `eotg_frontier_founder` | character | Design §5. |
| `eotg_frontier_sponsor` | character (may be absent) | Design §6. The *realm* is read through the character at runtime. |
| `eotg_frontier_sponsor_paid` | yes, timed 360 days | Set by a successful sponsor payment this year. Read by the tick. |
| `eotg_frontier_milestone` | 0 / 1 / 2 | Which development milestones have been paid out (§6.2). |
| `eotg_frontier_pending_heir` / `eotg_frontier_pending_from` | character, between a sponsor's death and the next tick | The heir hand-off (§V, E2 ruling); removed by that tick or when the project ends. |
| `eotg_frontier_tick_year` | the calendar year of the last tick | **Cooldown authority for the yearly tick** (§V, Q9): exactly one tick per in-game year, whoever holds the Region (§6.1). |
| `eotg_frontier_event_cd` | yes, timed 3 years (owner) | **Cooldown authority for flavor events**, set only in the tick's event roll (§6.4). |
| `eotg_frontier_attempts` | integer, permanent | Times a project here has ended in abandonment (a persistent trace, design §3.4). |
| `eotg_frontier_former_type` | type flag, permanent once set | What the last failed project was. |
| `eotg_frontier_history` | `flag:settled`, permanent | Set on completion. Read by nothing in Phase 1; it's a hook for future systems (design §14). |
| `eotg_frontier_last_cause` | `flag:no_founder` / `flag:low_control` / `flag:occupied` / `flag:war` / `flag:sponsor_lapsed` / `flag:events` | The latest strain cause. Read by .005's desc (§6.3). |
| `eotg_frontier_invested` | yes, timed 1 year | Limits Invest to once a year per county (§8.2). |
| `eotg_frontier_dev_reachable` | development | Q4: the development this project can still reach (§V). |
| `eotg_frontier_dev_granted` | 0–2, permanent | Q5: milestone development already granted to this Region (§V). |
| `eotg_frontier_debug_dev` / `_debug_control` / `_debug_floor_dev` / `_debug_floor_control` | timed 30 days | the debug readout's numbers (§V). |
| `eotg_frontier_tick_strained` | yes, timed 1 day | Set by any strain this tick; a quiet tick (none set) eases strain by 1. |

**Global variable list** `eotg_frontier_active`: every county currently in `flag:frontier`. It drives the AI throttle (§8.4), the Sponsor decision and debugging (E5).

**No character lists.** Founder and sponsor validity are read by the yearly tick (§R), so nothing has to find counties from a character.

### 2.5 The political owner

The political owner is **the county title's holder, read live** (`holder`) and never stored (design §7). An owner change needs no handling: the next tick runs on the new holder's pulse and the new holder gets the events. The Founder and Sponsor are untouched by an owner change (design §7).

---

## 3. Identifier table

All new. Namespace `eotg_frontier`. Files in §11.

### 3.1 Data and state
| Type | Key | Notes |
|---|---|---|
| title variables | `eotg_frontier_state`, `_type`, `_progress`, `_strain`, `_founder`, `_sponsor`, `_sponsor_paid`, `_milestone`, `_ticked`, `_event_cd`, `_attempts`, `_former_type`, `_history`, `_last_cause`, `_invested` | §2.4 |
| global variable list | `eotg_frontier_active` | §2.4 |
| saved scopes (event chains) | `eotg_frontier_county`, `eotg_frontier_founder`, `eotg_frontier_sponsor`, `eotg_frontier_candidate` (founder candidate), `eotg_frontier_old_sponsor`, `eotg_frontier_offer_1/_2/_3` (Sponsor pick); internal: `eotg_frontier_holder`, `_change`, `_heir_sponsor`, `_lapsed_sponsor`, `_leader`, `_sponsor_candidate` | the hook scopes too (§7) |
| static modifiers (county) | `eotg_frontier_mod_unsettled`, `eotg_frontier_mod_outpost` (progress 0–32), `eotg_frontier_mod_foothold` (33–65), `eotg_frontier_mod_established` (66–99), `eotg_frontier_mod_new_settlement` (10 years after completion), `eotg_frontier_mod_abandoned_works` (10 years after abandonment), `eotg_frontier_mod_hard_year` (2 years, from .002) | each also needs `_desc` loc |

### 3.2 Scripted effects (`common/scripted_effects/eotg_frontier_effects.txt`), as built
County scope unless noted.

| Key | Does |
|---|---|
| `eotg_frontier_save_hook_scopes_effect` | saves `scope:eotg_frontier_county`, `_founder` and `_sponsor` from the county's variables |
| `eotg_frontier_fire_hook_effect` (`HOOK`) | saves the hook scopes, then `holder = { trigger_event = { on_action = $HOOK$ } }` |
| `eotg_frontier_mark_unsettled_effect` | **the only entry point**: state `unsettled` plus the modifier (an Abandoned Region keeps its state) |
| `eotg_frontier_start_effect` (`TYPE`, `FOUNDER`) | → frontier: variables, the resettle head start, list, counter, stage modifier; the started hook |
| `eotg_frontier_unlist_effect` | out of the active list (the one record; §V) |
| `eotg_frontier_trigger_hook_effect` (`HOOK`) | fires a hook with the scopes as saved (§V, Q8) |
| `eotg_frontier_start_tooltip_effect` | character: .001's start tooltip, in the right person (lore I1) |
| `eotg_frontier_on_sponsor_death_effect` | character (dying): records `pending_heir` / `pending_from` on the Region, clears the sponsor (§V, E2) |
| `eotg_frontier_resolve_pending_heir_effect` | county, in the tick: the heir becomes the sponsor, or the backing lapses (§V) |
| `eotg_frontier_clear_pending_heir_effect` | removes the pending hand-off variables |
| `eotg_frontier_grant_milestone_dev_effect` (`LEVEL`) | +1 development once per Region, ever (§V, Q5) |
| `eotg_frontier_raise_dev_effect` (`AMOUNT`) | result development, with the development_changed hook (Q8) |
| `eotg_frontier_debug_readout_effect` | character: the debug readout toasts (§V) |
| `eotg_frontier_set_founder_effect` (`FOUNDER`) | sets the founder |
| `eotg_frontier_set_sponsor_effect` (`SPONSOR`) | sets or replaces the sponsor and its back-reference; the sponsor_changed hook |
| `eotg_frontier_clear_sponsor_effect` | removes the sponsor; the sponsor_changed hook |
| `eotg_frontier_drop_sponsor_effect` | removes the sponsor quietly (settle and abandon fire their own hooks) |
| `eotg_frontier_add_progress_effect` (`AMOUNT`) | Establishment 0–100, milestones, stage modifier; the progressed hook |
| `eotg_frontier_milestone_effect` | +1 development at 33 and 66, once each; the development_changed hook |
| `eotg_frontier_update_tier_modifier_effect` | the one stage modifier |
| `eotg_frontier_add_strain_effect` (`CAUSE`) | strain +1 (0–8); records the cause |
| `eotg_frontier_ease_strain_effect` | strain −1 |
| `eotg_frontier_tick_effect` | the yearly tick (§6.1) |
| `eotg_frontier_check_sponsor_effect` | fallback: a dead sponsor still set → Sponsor Lapse; a sponsor who is now the holder → dropped, no strain. The heir hand-off is `resolve_pending_heir` (on_death + next tick, §V) |
| `eotg_frontier_sponsor_pay_effect` | the yearly payment, or Sponsor Lapse |
| `eotg_frontier_event_roll_effect` | the flavor roll; sets the event cooldown |
| `eotg_frontier_find_sponsor_candidate_effect` | the liege, else an ally (AI, can sponsor) |
| `eotg_frontier_complete_effect` | the type result rows (if/else_if on the type), then settle |
| `eotg_frontier_build_holding_effect` (`HOLDING`) | a new System in an open slot, given to the holder; else +1 development, +10 control |
| `eotg_frontier_create_leader_effect` | Settlement: the settlers' leader (template `eotg_frontier_settler_leader_template`) |
| `eotg_frontier_settle_effect` | ends the Frontier: the completed and settled hooks, history, `New Settlement` |
| `eotg_frontier_clear_project_effect` | removes the project variables |
| `eotg_frontier_abandon_effect` (`FAILED`) | → abandoned, with traces; the failed (if `FAILED`) and abandoned hooks |
| `eotg_frontier_restart_effect` | .005 b/c: half the Establishment, strain 2 |

### 3.3 Scripted triggers (`common/scripted_triggers/eotg_frontier_triggers.txt`), as built
| Key | Scope | True when |
|---|---|---|
| `eotg_frontier_is_unsettled` / `_is_frontier` / `_is_abandoned` | county | the state flag |
| `eotg_frontier_can_establish` | county | unsettled or abandoned, and the capital is not occupied |
| `eotg_frontier_admin_eligible` | county | can establish, and the holder is a duke or above or this is not their capital Region |
| `eotg_frontier_has_valid_founder` | county | the founder is alive, adult, free, and the holder or in the holder's realm |
| `eotg_frontier_has_valid_sponsor` | county | the sponsor exists and is alive |
| `eotg_frontier_completion_met` | county | Establishment ≥ 100, and the type's development and control floors |
| `eotg_frontier_holds_frontier` / `_holds_establishable` | character | holds such a Region |
| `eotg_frontier_is_sponsor` | character | has the back-reference `eotg_frontier_sponsoring` |
| `eotg_frontier_can_sponsor` | character | landed, count+, gold ≥ 2 payments, sponsors none |
| `eotg_frontier_ai_would_sponsor` | character | AI, can sponsor, gold ≥ 4 payments (§V) |
| `eotg_frontier_ai_room` | global | fewer than `eotg_frontier_ai_cap_value` Regions in the active list (§V) |

### 3.4 Script values (`common/script_values/eotg_frontier_values.txt`)
| Key | Value |
|---|---|
| `eotg_frontier_establish_cost_value` | `medium_gold_value` (E20) |
| `eotg_frontier_invest_cost_value` | `minor_gold_value` |
| `eotg_frontier_sponsor_payment_value` | `minor_gold_value`, but from the sponsor's scope |
| `eotg_frontier_base_rate_value` | the type's base gain per year (§5.2) |
| `eotg_frontier_dev_bonus_value` | development_level / 5, capped at 4 |
| `eotg_frontier_control_bonus_value` | +2 at control ≥ 80, 0 at 40–79, −3 below 40 |
| `eotg_frontier_founder_bonus_value` | the founder's type skill / 4, capped at 5; 0 if the founder is dead or absent |
| `eotg_frontier_sponsor_bonus_value` | 6 when `eotg_frontier_sponsor_paid` is set |
| `eotg_frontier_trace_bonus_value` | the resettle head start, 10 × attempts, capped at 30 (§6.6) |
| `eotg_frontier_yearly_gain_value` | the sum of the above, floored at 0 |
| `eotg_frontier_min_dev_value`, `eotg_frontier_min_control_value` | the type's completion floors (§5.2) |
| `eotg_frontier_ai_cap_value` | 8 |

### 3.5 Decisions (`common/decisions/eotg_frontier_decisions.txt`)
| Key | Taker | Does |
|---|---|---|
| `eotg_decision_frontier_establish` | the holder of an establishable county | pays the cost and fires `eotg_frontier.001` |
| `eotg_decision_frontier_invest` | the holder of a frontier | gold → progress (one per county per year) |
| `eotg_decision_frontier_sponsor` | a ruler who can sponsor | fires `eotg_frontier.010`, the pick of frontiers to back |
| `eotg_decision_frontier_withdraw` | a current sponsor | clears the sponsorship, +1 strain, toast to the holder |
| `eotg_decision_frontier_abandon` | the holder of a frontier | abandons, with cause `voluntary` |
| `eotg_decision_frontier_debug_mark_unsettled` | debug only | marks the taker's capital county Unsettled |
| `eotg_decision_frontier_debug_tick` | debug only | runs the tick on the taker's frontier counties now, ignoring the cooldown |

### 3.6 On_actions (`common/on_action/eotg_frontier_on_actions.txt`)
| Key | Kind |
|---|---|
| `yearly_playable_pulse` → `eotg_on_yearly_frontier_tick` | vanilla hook, extended additively |
| `eotg_frontier_on_project_started`, `_on_project_progressed`, `_on_project_completed`, `_on_project_failed`, `_on_abandoned`, `_on_sponsor_changed`, `_on_development_changed`, `_on_settled` | **integration hooks** (§7), defined empty |

### 3.7 Events (`events/eotg_frontier_events.txt`, namespace `eotg_frontier`): see §9

---

## 4. Founder, Sponsor, Political Owner (design §5–7)

They are three separate things, stored separately.

| Role | Stored | Set by | Changes without touching the others |
|---|---|---|---|
| **Founder** | `var:eotg_frontier_founder` on the county | .001 (start); .002's *Without a Founder* variant, or the tick for AI (replacement) | yes |
| **Sponsor** | `var:eotg_frontier_sponsor` on the county | .003 (an accepted offer); withdraw, death and lapse clear it | yes |
| **Political owner** | not stored: `holder` of the county | normal CK3 | yes |

**Founder rules:**
- The founder **does not** become the ruler (design §5).
- The founder may be the holder, a courtier or a knight.
- They supply the skill input (§6.2): the type's skill (§5.1).

### 4.1 Founder validity (ruling Q2: no founder-death event)
The yearly tick (`eotg_frontier_tick_effect`, step 1) tests `eotg_frontier_has_valid_founder` on the Region.
- **An invalid founder** (dead, imprisoned, a child, or gone from the holder's realm) gives strain +1 with cause `no_founder`, every tick until replaced.
- **A player holder** replaces the founder in the .002 variant *The Frontier Without a Founder*, which the event roll takes ahead of the ordinary complication while the founder is invalid.
- **An AI holder** replaces the founder in the tick: their best candidate (the holder or a courtier, by the type's skill).
- **No hook fires on a founder change**, since the brief has none (open question).

### 4.2 Sponsor validity and change
**In the tick:**
- **A dead sponsor** (§V, E2): `on_death` (`eotg_frontier_on_sponsor_death`) stores their `primary_heir` as `eotg_frontier_pending_heir` and clears the sponsor (`…_on_sponsor_changed`). At the Region's next tick the heir becomes the sponsor when alive, able to sponsor and not the holder: fire `…_on_sponsor_changed` with `scope:eotg_frontier_old_sponsor`, and toast the holder.
- **Otherwise** strain +1 with cause `sponsor_lapsed` (no lapse if a new backer was found meanwhile, or if the heir now holds the Region).
- **A sponsor who becomes the holder** is dropped with no strain: sponsor and holder are never collapsed (§R).

**The sponsor-change flow** (design §6–7):
1. A would-be sponsor (player decision, or the AI through the tick) **offers**.
2. The county holder **accepts or refuses** in `eotg_frontier.003`.
3. Accepting replaces any current sponsor (the old one gets a toast) and fires `…_on_sponsor_changed`.

**Sponsorship gives the sponsor nothing beyond the arrangement:** no claim, no liege relationship, no ownership, and never the result (§R).

### 4.3 The yearly sponsor payment (tick step 3)
- **If the sponsor is alive and can afford it:** they pay `eotg_frontier_sponsor_payment_value` gold, which goes into the project (it is spent; the holder doesn't receive it). Set `eotg_frontier_sponsor_paid` for 360 days.
- **If they can't pay:** the sponsorship **lapses**. Clear the sponsor, strain +1, and toast both parties.
- **Owner question Q5:** should the money go to the project, as here, or to the holder?

---

## 5. Project types as data (design §4.1, §21)

**How "data" is done:**
- **One generic engine:** start, tick, complete, abandon.
- **Types are rows** in four `switch` tables keyed on `var:eotg_frontier_type`:
  - eligibility (`eotg_frontier_can_establish`, plus `eotg_frontier_admin_eligible` for Administrative);
  - rate (`eotg_frontier_base_rate_value`);
  - floors (`eotg_frontier_min_dev_value` / `_min_control_value`);
  - result (`eotg_frontier_complete_effect`, which dispatches to one small effect per type).
- **Adding a type** means adding a row to each table, an option in .001 and loc. No core change.
- **Why `switch`, not effect names built from parameters:** keys like `eotg_frontier_complete_$TYPE$_effect` would need the engine to substitute parameters inside identifiers. That is UNVERIFIED (§16 V14). If it holds, the dispatch could become one line.

### 5.1 Eligibility and inputs
Every type needs the county to be establishable (§3.3). Extra eligibility is deliberately light in Phase 1. Traits (design §10) are Phase 2.

| Type | Extra eligibility (Phase 1) | Founder skill input | Base rate / yr |
|---|---|---|---|
| Settlement | none | stewardship | 12 |
| Trade | none | stewardship | 11 |
| Mining | none | stewardship | 11 |
| Military | none | martial | 10 |
| Religious | none (faith-neutral: reads no faith keys) | learning | 10 |
| Research | none | learning | 9 |
| Administrative | the county's holder is duke-tier or above, or the county is not their capital county | stewardship | 10 |

Also part of the yearly gain (§6.2): development, county control, the sponsor payment and the resettle trace bonus. Gold investment comes through the Invest decision (+10 progress, at most once a year).

### 5.2 Completion requirements
For all types: progress ≥ 100. The two milestones give +2 development on the way.

| Type | min development_level | min county_control |
|---|---|---|
| Settlement | 2 | 40 |
| Trade | 3 | 50 |
| Mining | 2 | 50 |
| Military | 2 | 70 |
| Religious | 2 | 50 |
| Research | 3 | 50 |
| Administrative | 3 | 80 |

**Pacing:**
- A typical yearly gain is (base 9–12 + development 0–2 + control 0–2 + founder 2–4 + sponsor 0–6) × 0.5, about **6–13 a year** (§V, pacing doubled).
- **Unsponsored: about 10–16 years. Sponsored: about 8–10.** Investing shortens both.
- If the floors aren't met, progress holds at 100 and the tick keeps running (strain rules still apply) until they are.
- **Owner question Q4:** confirm the pacing target.

### 5.3 Completion results (normal CK3 terms)
Every type: the settled transition (§6.5), plus its row below.
- "Holding" means `eotg_frontier_build_holding_effect` on the first empty barony slot (E12). **If there is no empty slot**, the holding line is replaced by +1 development and +10 control.
- **Holding names in player text** follow the glossary: Port (city), Bastion (castle), Sanctum (temple).

| Type | Result |
|---|---|
| Settlement | Holding `city_holding` (a Port), +1 development. **A local character is created** (E13): the settlers' first leader, age 25–45, the county holder's culture and faith *by scope* (`culture = root.culture`, as the patron envoy, E13), as a courtier of the holder. The new System stays with the holder (§R). |
| Trade | Holding `city_holding`, +1 development; `eotg_frontier_mod_new_settlement` with a tax line |
| Mining | +2 development; `eotg_frontier_mod_new_settlement` with a tax line. **No holding**: the mine is the county's existing capital plus the modifier text. |
| Military | Holding `castle_holding` (a Bastion), +15 control |
| Religious | Holding `church_holding` (a Sanctum), +1 development |
| Research | +2 development; the modifier carries a development growth line. The founder gains learning +1 (`add_learning_skill`, invariant 7). |
| Administrative | Control set to 100 (`change_county_control = 100`, E8), +1 development; the modifier carries a control growth line |

`eotg_frontier_mod_new_settlement` (10 years) is one modifier: development growth +, and a small tax +. The type-specific flavor is in its description. **Owner question Q6:** one modifier per type, or one shared?

---

## 6. Progression, completion, failure (design §8, §12)

### 6.1 The yearly tick: `yearly_playable_pulse` → `eotg_on_yearly_frontier_tick`
Root is a playable character. Effect:

```
every_held_title = {                         # confirmed (V13)
    limit = {
        tier = tier_county
        eotg_frontier_is_frontier = yes
        OR = {                                   # cooldown authority (inv. 4; §V Q9)
            NOT = { has_variable = eotg_frontier_tick_year }
            current_year > var:eotg_frontier_tick_year   # vanilla orientation
        }
    }
    set_variable = { name = eotg_frontier_tick_year  value = current_year }
    eotg_frontier_tick_effect = yes
}
```

`eotg_frontier_tick_effect` runs on the county:
1. **Strain causes** (design §12), each +1, applied through `eotg_frontier_add_strain_effect`:
   - no valid founder (`eotg_frontier_has_valid_founder`, §4.1; ruling Q2);
   - county_control < 40;
   - the county's capital province is occupied (UNVERIFIED trigger, §16 V11);
   - the holder is at war **and** the strain from war has not fired this tick (one war point, however many wars).
   - **If no cause applied,** strain −1 (floor 0).
2. **Sponsor validity and payment** (§4.2, §4.3).
3. **Gain:** `eotg_frontier_add_progress_effect = { AMOUNT = eotg_frontier_yearly_gain_value }`. Milestones at 33 and 66 each pay +1 development once, and fire `…_on_development_changed`. Then update the tier modifier.
4. **Resolve**, in order. The first match wins:
   1. `eotg_frontier_completion_met` → `trigger_event = eotg_frontier.004` to the holder, AI or player. The AI chooses by `ai_chance`, which is fewer code paths than a separate AI resolution. Up to 8 AI frontiers make the cost negligible.
   2. strain ≥ `eotg_frontier_strain_fail_value` (8) → `trigger_event = eotg_frontier.005` to the holder, AI or player. The `ai_chance` values follow §6.6's AI order.
   3. Otherwise the **event roll**, gated by `NOT = { has_variable = eotg_frontier_event_cd }`. The event roll is the **only** place that sets `eotg_frontier_event_cd` (3 years, owner decision). Event triggers never read it (lesson 5). The roll is a `random_list`:
      - 30: `.002` (complication, or its *Without a Founder* variant while the founder is invalid; a player holder only);
      - 20: `.003` (sponsor offer). Only when there is no sponsor, a candidate sponsor exists (§8.4), and the holder is not AI. AI–AI offers resolve in script with no event.
      - 50: nothing.

### 6.2 Hidden state and how it's surfaced
- **Progress and strain are never shown as numbers** (design §8). No tooltip prints them.
- **Display:** one county modifier, showing the tier:
  - `eotg_frontier_mod_outpost` (progress 0–32): tax −50%, levies −50%, control growth −;
  - `eotg_frontier_mod_foothold` (33–65): tax −25%, levies −25%;
  - `eotg_frontier_mod_established` (66–99): tax −10%, development growth +.
  - Their descriptions say in words how far along it is.
- **Strain shows only through events and descriptions:** .002's desc varies by strain band.
- **The decision tooltips** (Invest, Abandon) name the type, founder and sponsor, and the tier in words.
- **Resettle head start:** a project started on an abandoned county starts at `eotg_frontier_trace_bonus_value` (design §3.4: resource knowledge, abandoned infrastructure).

### 6.3 Strain
Strain is an integer from 0 to 4, hidden. Its causes are the tick list (§6.1) plus event outcomes. At 4 the project fails, so failure is **contextual**, not a random roll (design §12): every point of strain has a named cause, and .005's desc names the dominant one.
- **Tracking the cause:** the latest strain cause is kept in `eotg_frontier_last_cause` (§2.4).

### 6.4 Flavor event cadence
- **Cooldown:** at most one flavor event per county every 3 years (about 4–5 per typical project), with `eotg_frontier_event_cd` as the cooldown authority (§6.1).
- **Not affected:** completion and failure are resolution events, outside the cooldown.

### 6.5 Completion → Settled (design §3.3)
`eotg_frontier_complete_effect` runs the type's result (§5.3), then `eotg_frontier_settle_effect`:
- **Removes** the tier modifier and every `eotg_frontier_*` state variable (state, type, progress, strain, founder, sponsor, paid, milestone, event_cd, last_cause, invested).
- **Removes** the county from `eotg_frontier_active` and from the founder's and sponsor's lists.
- **Sets** `eotg_frontier_history = flag:settled` and adds `eotg_frontier_mod_new_settlement` (10 years).
- **Keeps** `eotg_frontier_attempts` and `eotg_frontier_former_type` as history.
- **Fires** `…_on_project_completed`, then `…_on_settled`.

After that the county is a normal county. No Frontier code reads it again. The `eotg_frontier_history` flag exists only for future systems.

### 6.6 Failure and abandonment (design §3.4, §12)
**`eotg_frontier.005` *The Frontier Falters*** offers (contextual, design §12 "a failed project may"):
- **(a) Abandon:** `eotg_frontier_abandon_effect = { CAUSE = failed }`.
- **(b) Continue under a new founder:** costs `minor_gold_value`; strain → 4; progress × 0.5; the founder is replaced by the best candidate.
- **(c) Scale back to Settlement:** strain → 4; progress × 0.5; the type re-picked from the ones eligible. Shown only if another type is eligible.
- **(d) Hand it to the sponsor's care:** only with a living sponsor who can pay twice; strain → 2; the sponsor pays a double payment. Design §12: "transfer sponsorship".

**AI resolution, no event:** (d) if possible; else (b) if gold ≥ 2 × minor; else (a).

**Abandonment** (`eotg_frontier_abandon_effect`, from .005, the Abandon decision or the debug flow):
- `state = flag:abandoned`, `attempts +1`, `former_type = type`.
- Clear the founder, sponsor, progress, strain and lists.
- −1 development if milestone ≥ 1 ("lose infrastructure").
- Add `eotg_frontier_mod_abandoned_works` (10 years: the ruins of the attempt, a small tax line, a description). The `abandoned` state then stays, so the county shows as resettlable.
- **Fire** `…_on_project_failed` (only when `CAUSE` is `failed`), then `…_on_abandoned`.

**Resettle:** Establish works on `abandoned` exactly as on `unsettled`, with the trace head start (§6.2). The `unsettled` modifier is not re-added.

---

## 7. Integration hooks (design §14)

All eight are custom on_actions, defined **empty** in `eotg_frontier_on_actions.txt` so that later systems can extend them additively. Phase 1 puts nothing in them.

**How they're fired:** `trigger_event = { on_action = <hook> }` (E17, UNVERIFIED).
- **Root:** the county's **holder**, a character. Custom on_actions fired by `trigger_event` need a character root (E17). The brief's "root = county" becomes a saved scope.
- **Saved scopes:** each hook gets `scope:eotg_frontier_county` (the county title), `scope:eotg_frontier_founder` and `scope:eotg_frontier_sponsor` (when they exist), via `eotg_frontier_save_hook_scopes_effect`.

| Hook | Fired from | Extra scopes |
|---|---|---|
| `eotg_frontier_on_project_started` | `eotg_frontier_start_effect` | — |
| `eotg_frontier_on_project_progressed` | `eotg_frontier_add_progress_effect`, when gain > 0 | — |
| `eotg_frontier_on_project_completed` | the settle effect, before the variables are cleared | — |
| `eotg_frontier_on_project_failed` | the abandon effect with `CAUSE = failed` | — |
| `eotg_frontier_on_abandoned` | the abandon effect (every cause) | — |
| `eotg_frontier_on_sponsor_changed` | the set/clear sponsor effects | `scope:eotg_frontier_old_sponsor` when there was one |
| `eotg_frontier_on_development_changed` | the milestone effect, and the result effects that change development | — |
| `eotg_frontier_on_settled` | the settle effect, after the variables are cleared | — |

**Fallback if E17 fails:** call scripted effects with an empty body (`eotg_frontier_hook_started_effect = yes`), which future systems override. That is a weaker pattern: it needs a file override, not additive extension.

---

## 8. Player and AI entry points

### 8.1 Establish Frontier: `eotg_decision_frontier_establish`
- **`is_shown`:** `eotg_frontier_holds_establishable = yes`.
- **`is_valid`:** gold ≥ cost (the engine blocks an unaffordable `cost`, E15); not at war (Q7).
- **`cost`:** gold `eotg_frontier_establish_cost_value`.
- **Effect:**
  - Picks the target county: the taker's establishable county with the highest development, as `scope:eotg_frontier_county`. With several, .001 has an option to look at the next one (§9).
  - Picks the founder candidate: the taker, or their courtier or knight with the highest **stewardship** when that beats the taker's own (`scope:eotg_frontier_candidate`). .001 can switch it to "lead it yourself".
  - Fires `eotg_frontier.001`.
- **Alternative (option 8b):** a character interaction with title targeting (`target_type = title`, as vanilla's grant and revoke title interactions) would let the player click the exact county. Its 1.20 shape is UNVERIFIED (§16 V16). Keep 8a for Phase 1.

### 8.2 Invest: `eotg_decision_frontier_invest`
- **Shown** to a holder of a frontier. **Cost:** `eotg_frontier_invest_cost_value`.
- **Effect:** the target is the taker's frontier county that has no `eotg_frontier_invested` (§2.4), highest progress first. +5 progress (§V).
- **Q3:** keep this decision, or move investment into event options?

### 8.3 Sponsor, Withdraw, Abandon
- **Sponsor (`eotg_decision_frontier_sponsor`):** shown when `eotg_frontier_can_sponsor = yes` and some active frontier is held by **someone else**. Fires `.010`, which lists up to 3 frontiers via `ordered_in_global_list` (E5), ranked by the holder's opinion of the taker and then by distance (the distance trigger is UNVERIFIED, §16 V17). Picking one sends `.003` to that county's holder.
- **Withdraw (`eotg_decision_frontier_withdraw`):** shown to a sponsor (`eotg_frontier_is_sponsor`). Clears the one sponsorship they hold (no event), strain +1 with cause Sponsor Lapse, and a toast to the holder.
- **Abandon (`eotg_decision_frontier_abandon`):** shown to a holder of a frontier. Confirmation text plus `eotg_frontier_abandon_effect = { CAUSE = voluntary }` on the chosen county (the same "highest development first" pick). No event.

### 8.4 AI weights (plausible, not spammy)
| Decision | `ai_check_interval_by_tier` (months) | `ai_potential` | `ai_will_do` |
|---|---|---|---|
| Establish | barony 0, county 60, duchy 48, kingdom 48, empire 48, hegemony 48 | holds an establishable county; `eotg_frontier_ai_room = yes`; holds no active frontier | base 10; +10 stewardship ≥ 12; +10 ambitious; +5 diligent; −10 lazy / content; ×0 at war or gold < 2 × cost |
| Invest | county 24, others 24 (barony 0) | holds a frontier; gold ≥ 3 × cost | base 20; +20 if strain ≥ 2 (read in script, never shown) |
| Sponsor | county 0, duchy 60, kingdom 36, empire 36, hegemony 36 | `eotg_frontier_can_sponsor`; gold ≥ 4 × payment; sponsors none | base 5; +10 generous; +5 ambitious; ×0 if greedy |
| Withdraw | all tiers 24 (barony 0) | is a sponsor | base 0; +50 if gold < 2 × payment; +20 at war |
| Abandon | all tiers 36 (barony 0) | holds a frontier | base 0; +30 if strain ≥ 3 and gold < minor |

**Global throttle:** at most `eotg_frontier_ai_cap_value` = 8 active frontiers (read through the global list), and at most one per AI ruler. AI never uses the debug decisions.

**AI–AI sponsor offers** (tick step 4.iii, only when the holder is AI): a candidate sponsor is the holder's liege, else a `random_ally` (E24). They must pass `eotg_frontier_can_sponsor` and the Sponsor ai_potential. The holder accepts when its opinion of the candidate ≥ 0.

### 8.5 Debug only: `eotg_decision_frontier_debug_mark_unsettled`, `…_debug_tick`
**Gating options:**

| Option | How | Notes |
|---|---|---|
| **A** (recommended) | `is_shown = { debug_only = yes }` | E16, M |
| B | a game rule `eotg_frontier_debug` (off by default) | needs a game-rule file; has_game_rule is already used by the mod |
| C | shown only to `is_ai = no` while a character flag set from the console is held | always works; less clean |

**Mark unsettled:** effect `capital_county = { eotg_frontier_mark_unsettled_effect = { DEV_LOSS = 0 } }`.

**Tick:** for every held frontier county, run the tick now (the calendar-year marker is not set, so the normal tick still runs that year).

**Readout (§V):** `eotg_decision_frontier_debug_readout` toasts progress, strain and the floors for each held Frontier.

**Testing a non-capital county:** use the console: `effect title:<c_key> = { eotg_frontier_mark_unsettled_effect = { DEV_LOSS = 0 } }`. Vanilla keys are fine at the console; they are never in script.

---

## 9. Phase 1 events (namespace `eotg_frontier`). **Count: 6 (ruling Q2).**

Every event moves or reads Establishment (progress) or its pressure (strain), as invariant 5 requires.

| ID | Title (draft) | Fired by | Root | Options | Couples |
|---|---|---|---|---|---|
| `.001` | *An Opportunity Here* (start) | `eotg_decision_frontier_establish` | the taker; `scope:eotg_frontier_county`, `scope:eotg_frontier_candidate` | One option per **type** (7; the Administrative option also needs `eotg_frontier_admin_eligible`), each starting the project with the candidate as founder. **"Not now"** refunds the cost. | **sets** progress (0, or the trace bonus); the start hook |
| `.002` | *A Hard Year* (complication) / *The Frontier Without a Founder* (variant) | tick event roll (player holders) | the holder; `scope:eotg_frontier_county` | **Complication:** **(a)** "Ship in supplies": `minor_gold_value`, strain −1. **(b)** "Push through": progress +8, strain +1 (cause `hardship`). **(c)** [has a sponsor] "Call on the backer": the sponsor makes one extra payment, strain −1. **Without a Founder** (the founder is invalid): **(d)** "Appoint [eotg_frontier_candidate.GetName]": founder = the best candidate. **(e)** "Lead it yourself": founder = root. **(f)** "Let them manage alone": no founder; strain stays. The desc varies by strain band (0–1, 2, 3+). | moves strain or progress; sets the founder |
| `.003` | *An Offer of Backing* (sponsor offer) | tick event roll (an AI candidate offers to a player holder), or `.010` (a player offers to any holder) | the holder; `scope:eotg_frontier_sponsor` = the offerer; `scope:eotg_frontier_county` | **(a)** Accept: set the sponsor; progress +5 (the first shipment). **(b)** Refuse. AI chance: by opinion of the offerer. | sets the sponsor; moves progress |
| `.004` | *No Longer a Frontier* (completion) | tick resolve | the holder | The new System stays with the holder (§R). The options reward the founder (ruling Q12): **(a)** "A purse for [founder]": the holder pays `minor_gold_value`, which goes to the founder. **(b)** "Honor them publicly": the founder gains prestige, the holder a little. **(c)** "The work is its own reward": nothing. **(a)** and **(b)** are shown only when the founder is valid and is not the holder. Every option runs completion → settled. Desc variant per type. | completes Establishment (progress → Settled) |
| `.005` | *The Frontier Falters* (failure) | tick resolve (strain 8) | the holder | §6.6 a–d. The desc names `eotg_frontier_last_cause`. | resets or ends progress; strain |
| `.010` | *Whom to Back* (Sponsor pick) | `eotg_decision_frontier_sponsor` | the taker | Up to 3 options, one per offered county (`scope:eotg_frontier_offer_1..3`), each sending `.003` to that holder. Plus Cancel. | reads progress (the desc names each county's stage in words) |

**Why .010 is an event:** decisions can't take a county target (E15). If option 8b (title interaction) is verified, .010 goes away.

**AI holders** get .001, .004, .005 and .003 (from player offers), and pick by `ai_chance`. They never get .002, and never get .003 from AI offers, which resolve in script.

## 10. Loc surface (`localization/english/eotg_frontier_l_english.yml`), as built: 118 keys
UTF-8 with BOM, bare `[x.GetName]`, gendered pronouns for single characters, ~~US English~~ Canadian English (supersedes US spelling: owner ruling 2026-10-04, loc commit 4168bb8), no em dashes. Glossary words (ruling Q1): **Region** (county), **System** (barony or holding), **Port**, **Bastion**, **Sanctum**.
- **Events:**
  - `.001`–`.005` and `.010`: `.t`, `.desc`, option keys `.a`–`.h`;
  - variants: `.001.desc_resettle`; `.002.t_no_founder`; `.002.desc_low/_mid/_high/_no_founder`; `.003.desc_replace`; `.004.desc_<type>` ×7; `.005.desc_<cause>` ×6;
  - option tooltips: `.001.start_tt`, `.002.ease_tt/_push_tt/_founder_tt/_f_tt`, `.003.accept_tt/_refuse_tt`, `.004.complete_tt`, `.005.abandon_tt/_restart_tt/_sponsor_tt`, `.010.offer_tt`.
- **Decisions:** 7 × `<key>`, `_desc`, `_confirm`, plus the custom tooltips `_gold_tt`, `_peace_tt`, `_effect_tt`, `_ready_tt` and `_valid_tt`. Raw variables never reach a requirement line (eotg_lint L006).
- **Modifiers:** 7 × `<key>`, `_desc`.
- **Toasts:** `eotg_frontier_toast_sponsor_inherited`, `_lapsed`, `_withdrew`, `_replaced`.
- **Appended descs** (after the opener) start with `\n\n` (round-4 lint L013d).
- **Vocabulary (§R lore):**
  - **Use:** star systems, stations, settlers, survey, supply runs, berths; foundation, expedition, venture, outpost.
  - **Never:** "charter" in the sense of a higher authority, a named faction, the Void, "village", "manor", "peasants", "barony", "holding slot".

## 11. File placement (new files only)
| File | Contents |
|---|---|
| `common/scripted_effects/eotg_frontier_effects.txt` | §3.2 |
| `common/scripted_triggers/eotg_frontier_triggers.txt` | §3.3 |
| `common/script_values/eotg_frontier_values.txt` | §3.4 |
| `common/modifiers/eotg_frontier_modifiers.txt` | §3.1 modifiers |
| `common/scripted_character_templates/eotg_frontier_templates.txt` | the settlers' leader (§5.3) |
| `common/decisions/eotg_frontier_decisions.txt` | §3.5 |
| `common/on_action/eotg_frontier_on_actions.txt` | §3.6 |
| `events/eotg_frontier_events.txt` | §9 |
| `localization/english/eotg_frontier_l_english.yml` | §10 |
| `docs/specs/frontier_v1_test_plan.md` | the in-game checklist (in `docs/specs/`: this work may only add `frontier_v1_*` files there) |

- **Not created:** no `replace_path`, no `descriptor.mod` edits, no gfx (modifiers use vanilla icons such as `county_modifier_development_positive`; their existence is UNVERIFIED, V18).
- **Not touched:** no `eotg_augmentation_*` file.

---

## 12. Definition of done (Phase 1)
1. **Lint clean:** `eotg_lint` shows no new findings in `eotg_frontier_*` files (L001 prefix, L004 hooks, L005, L006, L007, L009 reachability, L010 loc, L013 style, L014 unused loc). `check_all` passes. `gen_test_recipes.py` emits recipes for every `eotg_frontier.*` event.
2. **Debug entry point:** on the vanilla map, with `-debug_mode`, the debug decision marks the capital county Unsettled. The county shows `eotg_frontier_mod_unsettled`. Establish appears.
3. **Each of the 7 types completes:**
   - every county variable is cleared;
   - the right holding exists where an empty slot did, otherwise the development and control fallback applies;
   - `eotg_frontier_mod_new_settlement` is present;
   - no Frontier decision is shown for that county again.
4. **Failure:** strain 8 → .005; each branch behaves as §6.6; Abandoned → Establish works again with the head start; `abandoned_works` is present; attempts +1.
5. **Founder and sponsor validity:** killing or imprisoning the founder → strain +1 (No Founder) each tick, and the .002 *Without a Founder* variant offers a replacement. Killing a sponsor → at the next tick it passes to their heir, or lapses with +1 strain (Sponsor Lapse).
6. **Owner change** (grant the county away): the frontier continues under the new holder; the founder and sponsor are unchanged, and the founder stays valid when the new holder is their vassal (Q3); there is no double tick that year.
7. **AI behaviour (10-year observer run):** active frontiers stay ≤ 8; no AI ruler has more than one; at least one AI frontier starts and resolves.
8. **Standalone:** nothing reads any `eotg_aug*` or other EotG system (grep). No title, province, culture or faith keys in script (grep for `title:`, `province:`, `culture:`, `faith:`: 0 hits).
9. **No numbers:** no tooltip shows a progress or strain number.

---

## 13. Phase 2+ (listed, not built)
- **Content:**
  - Frontier traits as county modifiers (Rich Resources, Ancient Ruins, Strategic, Hostile, Remote, Anomalous: design §10), feeding the rate and eligibility tables;
  - more positive and negative events (design §11);
  - infrastructure modifiers (design §9);
  - discoveries;
  - per-type result modifiers;
  - a sponsor opinion modifier;
  - a founder-change hook.
- **Holdings:** possibly a minimal "outpost" holding type (option 2.3b), or the great-project surface (option 2.2C, D6).
- **Setup:**
  - an exploration stub: a decision that reveals or enables Unsettled (design §13);
  - the cartographer marks Unsettled counties on the real map through `eotg_frontier_mark_unsettled_effect` (D3).
- **Phases 3–4 (design §22):** integrations (Corporations, Religion, Trade, Mercenaries, Exploration); Greater Drift sponsorship, rival settlement and the boom, all through the §7 hooks and the sponsor and rate inputs, with no core changes.

## 14. Deferrals
- **D1:** Frontier traits (Phase 2).
- **D2:** any opinion modifier (Phase 2, Q10).
- **D3:** marking Unsettled on the real map (after Gate 1; cartographer, one effect call per county; how history sets title variables is UNVERIFIED, V19).
- **D4:** a custom holding type (Phase 2+).
- **D5:** a founder-change hook (Q8).
- **D6:** the great-projects surface (needs E21 gating answered).
- **D7:** exploration states: known, unknown, partially explored (design §13).

## 15. Lore and canon questions (**answered by the owner 2026-10-04: see §R**; kept for the record)
- **L1. Settlers at 866.** Who are the people who go out to a frontier in 866 AG? The Titan Exodus is ongoing (REVIEW_866), with refugee fleets "continuing to arrive in settled space". Can Settlement loc imply Exodus arrivals as settlers? Or must it stay generic ("settlers", "families from the inner systems")?
- **L2. Ruins and remnants.** Abandoned traces are the *project's own* ruins (stations, berths). May an Unsettled county's descriptions mention older ruins: Second Era wreckage, or Grip-era remnants (the Grip is 866 years past, living history)? Or is that Phase 2 trait territory, with its own canon review?
- **L3. Sponsorship register.** With no authority above the polity (LAW AT 866), is a sponsorship anything more than a private arrangement between a backer and a holder? Proposed wording: "backing", "underwriting", "a supply contract under [holder]'s law". Are words like "charter" or "licence" acceptable, or do they imply a higher authority?
- **L4. "New Cauldron" in the brief** is only an example. The bookmark design has New Cauldron founded in 131 AG, and REVIEW_866 lists "No state augmentation programmes (New Cauldron, 1610)". Confirm that no 866 faction is named anywhere in Frontier text. The current spec names none.
- **L5. The Research type.** The design mentions "anomalous" opportunities. The Void's influence is unexplained at 866, and the cybernetic voice is not Void-related (ERRATA). Should Research text avoid the Void entirely in Phase 1?
- **L6. Vocabulary.** Are "station", "outpost", "beacon", "berth" and "survey" in register for 866 space infrastructure (the cybernetics-at-866 tech ceiling: hand-fitted parts, no self-repair)? Are there terms to avoid?
- **L7. Religious type, faith-neutral.** Is "mission" acceptable for every faith family?

## 16. Verification list for the local session (eotg-vanilla-scout against vanilla 1.20.0.3). **Still open; tracked in [`frontier_v1_open_questions.md`](frontier_v1_open_questions.md). V3 (character lists) no longer applies, and V21 now asks whether `primary_heir` of a **dead** character is readable from the yearly tick; see §R.**
1. **(E4)** Do `set_variable`, `has_variable`, `var:x`, `change_variable` and `remove_variable` work on a **landed_title** scope? Do title variables persist when the holder changes? Give a vanilla example.
2. **(E5)** Exact names and shapes: `add_to_global_variable_list`, `remove_list_global_variable`, `every_in_global_list`, `ordered_in_global_list` (with `order_by`, `max`), and a list-size trigger (`global_variable_list_size`?). Can a global list hold title scopes?
3. **(E6)** Can a character variable list (`add_to_variable_list` / `every_in_list` / `remove_list_variable`) hold landed_title scopes?
4. **(E7)** `add_county_modifier = { modifier = x years = n }`, `remove_county_modifier`, `has_county_modifier` on a county title in 1.20. What `icon =` keys suit county modifiers?
5. **(E9)** Does `change_development_level` exist in 1.20 on a county? Is there `change_development_progress`?
6. **(E10)** Triggers `development_level >= n` and `county_control >= n` on a county title.
7. **(E11, E25)** Province triggers `has_holding = yes/no`, `has_holding_type = x`. The county → provinces iterators (`every_county_province` / `random_county_province`?). `title_province`. Is the county's `capital_province` stable?
8. **(E12)** **The key one.** Can script build a holding in an empty barony slot (`set_holding_type = city_holding` on the province)? Which effect does vanilla use (Found a City? nomad or admin holdings in 1.20)? Who holds the new barony title afterwards? Is there a building-time or "under construction" mechanic to use instead?
9. **(E14)** The exact 1.20 shape for granting a barony to a character from script (`create_title_and_vassal_change` / `change_title_holder` / `resolve_title_and_vassal_change`).
10. **(E16)** Is `debug_only = yes` valid in a decision `is_shown`? Which vanilla debug decisions use it?
11. **(V11)** A trigger for "this county or its capital province is occupied" (`is_occupied` on province?).
12. **(E17)** Does `trigger_event = { on_action = x }` fire a custom on_action with root and saved scopes intact? Can root be a title?
13. **(E18)** `every_held_title` with `tier = tier_county`. Does `yearly_playable_pulse` fire for every county holder (all playable characters), once a year each?
14. **(V14)** Are scripted-effect parameters substituted inside identifiers (`eotg_frontier_complete_$TYPE$_effect = yes`)? Is `switch = { trigger = var:x  flag:a = { } }` valid with flag values?
15. **(E24)** `random_ally`, `random_neighboring_top_liege_realm_owner` (or the 1.20 equivalents) on a character.
16. **(V16)** 1.20 character interactions with `target_type = title` (the grant/revoke shape): could a player pick the exact county for Establish or Sponsor?
17. **(V17)** A distance trigger or order_by value between a character and a county or province (`squared_distance`?).
18. **(V18)** Vanilla county-modifier icon keys (development and control positive/negative).
19. **(V19)** Can `history/titles/` set a title variable at a date, for D3? Or must an on_game_start effect do it?
20. **(E21)** Is `common/great_projects/` gated by a DLC in 1.20 (`has_dlc_feature`)? For D6 only.
21. **(E2)** In `on_death`, is the dying character's variable list still readable? Is `primary_heir` valid there?
22. **(E20)** Are `minor_gold_value` and `medium_gold_value` evaluated in the root character's scope when used in a county-scope effect? Or must they be read through `holder`?

## 17. Questions for the owner (**Q1, Q2 and Q12 answered, see §R; the rest are open in [`frontier_v1_open_questions.md`](frontier_v1_open_questions.md)**)
- **Q1. The word.** The glossary says county = "Region" and barony = "System". This task says a star system is a county. Which word do players see for a Frontier county? Option (i), Region, keeps the glossary: "the Region of X is a Frontier", and the stations go into its empty Systems. Option (ii), System, overrides the glossary for this feature. (i) is recommended.
- **Q2. The event count:** 6 required (.001–.005, .010) plus .006 optional. Approve, cut .006 (the death handling then runs automatically with a toast), or add more? Adding means Phase 2.
- **Q3. Invest:** a decision (proposed), or only event options?
- **Q4. Pacing:** ~~about 5–8 years unsponsored and 4–5 sponsored~~ **doubled by the owner: 10–16 and 8–10** (§V).
- **Q5. Sponsor money:** spent on the project (proposed), or paid to the holder?
- **Q6. One shared "New Settlement" modifier** with type text, or one per type (+7 modifiers)?
- **Q7. War:** may Establish be taken while at war? (Proposed: no. War adds strain anyway.)
- **Q8. A founder-change hook:** should the brief's eight hooks gain `eotg_frontier_on_founder_changed`?
- **Q9. Withdraw:** from every sponsorship at once (proposed), or one at a time (needs a pick event)?
- **Q10. Opinion modifiers** between sponsor and holder: Phase 1 or Phase 2 (proposed: Phase 2)?
- **Q11. The AI cap of 8** active frontiers on the map, at most one per ruler. On the vanilla map, nothing is Unsettled until the debug decision marks it, so AI frontiers only appear in counties marked that way. Is that acceptable for Phase 1 testing?
- **Q12. Who gets the new holding on completion:** the holder by default, with optional grants in .004 (proposed). Or should the founder get it automatically when they're unlanded (the "Local Ruler: House Veyra" example in design §7)?

---

### HANDOFF
- status: partial. Phase 1 is built on the owner's rulings (§R) and the defaults in `frontier_v1_open_questions.md`, and is unverified in game.
- next: eotg-vanilla-scout (open questions §B) → eotg-qa (Tiger, PX) → human (`frontier_v1_test_plan.md` §0 first)
- ask: verify the engine list in `frontier_v1_open_questions.md` §B, starting with V1, V8 and V12; their binding fallbacks are in §R. Run Tiger and PX on the eotg_frontier_* files, then hand the owner the test plan.
- files: §11
- needs-loc: none (118 keys written; localizer review welcome)
- needs-lore: none open (§R)
- needs-human: the open questions file §A (Q3–Q16); the test plan
