# Handoff: Unclaimed Regions (Frontier), Batches 1 and 2

### HANDOFF (cloud session, unvalidated)
- **branch:** `claude/frontier-unclaimed-cloud`.
  - Branched from `origin/claude/frontier-v3-cloud` @ `dc02666` (Frontier Phase 3a round 2), **not** from `v2-space-map`, because it needs 3a's `eotg_frontier_can_target_expedition`.
  - `v2-space-map` moved to `b3371a0` (cybernetics only) while I worked, but it does not contain Phase 3a yet, so I did not merge it.
  - **Do NOT merge.** Merge Phase 3a into `v2-space-map` first, then this branch.
- **status:** done (static, unvalidated: no game files, Tiger or PX here). **One blocker for V-U2:** the war-immunity override ships inert (below).
- **summary:** spec `docs/specs/frontier_unclaimed_regions.md` (owner decisions §D bind), built in its two batches. Deviations are in §20 of the spec and repeated below.
  - **Batch 1:**
    - the placeholder government, the "Unsworn" trait and template;
    - the release, create, claim-bookkeeping, vanish, death and sweep effects;
    - the game-start split of the history seed;
    - the colour effects and attrition (government knob plus Phase 1's Unsettled modifier);
    - the probe and release debug decisions;
    - the override file (inert);
    - both test setups.
  - **Batch 2:**
    - *Raise Your Colours* with reach, cost, cooldown and the AI throttle;
    - return to unclaimed on abandonment, and the settle clear;
    - the Phase 1 guards and tooltips;
    - the M1 pulse guards;
    - expedition widening and the `frontier_v3.md` §17 adaptations;
    - the .040 Military desc.
- **commits:**
  - `b253b6a` Batch 1;
  - `f273a5f` Batch 2;
  - this handoff (the commit after `f273a5f`).
- **validation (static):**
  - `eotg_lint`: 0 findings;
  - `check_all`: 14 pass, 0 fail, 7 skipped (Tiger, PX and the game are local-only);
  - `spec_conformance`: **frontier_unclaimed_regions: 0 missing** (90 present, 2 referenced only, 3 exempt); frontier_v3: 0 missing;
  - every new file has exactly one BOM;
  - the map-agnostic grep (`title:|province:|culture:|faith:|character:`) over the system's `common/` files is empty;
  - `grep -rnE 'eotg_[ekdcb]_'` is empty.
- **files:**
  - **new:**
    - `common/governments/eotg_unclaimed_government.txt`
    - `common/traits/eotg_unclaimed_traits.txt`
    - `common/scripted_character_templates/eotg_unclaimed_templates.txt`
    - `common/modifiers/eotg_unclaimed_modifiers.txt`
    - `common/script_values/eotg_unclaimed_values.txt`
    - `common/scripted_triggers/eotg_unclaimed_triggers.txt`
    - `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt`
    - `common/scripted_effects/eotg_unclaimed_effects.txt`
    - `common/on_action/eotg_unclaimed_on_actions.txt`
    - `common/decisions/eotg_unclaimed_decisions.txt`
    - `common/character_interactions/eotg_unclaimed_interactions.txt`
    - `localization/english/eotg_unclaimed_l_english.yml`
  - **changed:**
    - `common/modifiers/eotg_frontier_modifiers.txt` (Unsettled −0.25 supply)
    - `common/scripted_triggers/eotg_frontier_triggers.txt`
    - `common/scripted_effects/eotg_frontier_effects.txt`
    - `common/decisions/eotg_frontier_decisions.txt`
    - `common/on_action/eotg_frontier_on_actions.txt`
    - `common/on_action/eotg_augmentation_on_actions.txt` (guards only)
    - `events/eotg_frontier_events.txt`
    - `localization/english/eotg_frontier_l_english.yml`
  - **test setups:**
    - `docs/test_submods/frontier_vanilla/` (on_action, README)
    - `docs/test_map/` (characters, titles, landed_titles, README)
  - **docs:**
    - `docs/specs/frontier_unclaimed_regions.md` (status, §20)
    - `docs/specs/frontier_v3.md` (§4.1, §17)
    - `docs/tools/eotg_lint_loc_conventions.json` and `eotg_lint.md` (a `governments` naming convention)
    - `docs/qa/generated/*` (regenerated)

## The war-immunity override ships INERT (read first)
`common/scripted_triggers/eotg_vanilla_overrides_triggers.txt` holds the header, the paste steps and the two `# EOTG` lines, **all commented out**.
- A key-level override must be a **verbatim** copy of vanilla's `herders_and_tributary_constraints` (`00_war_and_peace_triggers.txt:1144-1160`, 1.20.0.3). There are no game files here, and a public copy couldn't be found. A copy rebuilt from memory would silently change the 17 CB groups that call the trigger.
- **Local session:** paste vanilla's body, add the defender line beside `government_is_herder` and the attacker line, uncomment, then check `database_conflicts.log` and V-U2. Until then nothing stops a CB war on a placeholder, so **V-U2 fails by design**.
- **Pitfalls entry text** (spec §4.4; the orchestrator adds it to `docs/pitfalls.md` once the override is live):

> **N. A key-level override of a vanilla scripted trigger: `herders_and_tributary_constraints`.**
> **What:** `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt` redefines a vanilla key. It is a verbatim copy of `G/common/scripted_triggers/00_war_and_peace_triggers.txt` `herders_and_tributary_constraints` (1.20.0.3) plus two lines, each marked `# EOTG`: our flag in the defender `NOR`, and an attacker check. **It is a non-additive replacement.** Vanilla changes to that trigger are silently lost.
> **Confirm it loads:** `logs/database_conflicts.log` must show `Overriding entry 'herders_and_tributary_constraints'` naming our file. The same log already lists the mod's building overrides. If it is absent, the key-level override didn't take, and the fallback is a full copy of the vanilla file under its own name (which is worse).
> **Prevent:** after every CK3 update, diff the copied block against vanilla (§2's override sweep). The header of the file lists every overridden key and the vanilla version it was copied from.

## unverified-vanilla (every `# UNVERIFIED-VANILLA` marker this build added)
**Playability, colour, attrition and the override (the four the brief singled out):**
- `common/governments/eotg_unclaimed_government.txt:24`: **playability (V-U1).** A custom government with no `mechanic_type` is probably *playable* (spec §4.5's inference). The probe decision answers it. If playable, build M2 (a second key override, `basic_is_valid_for_yearly_events_trigger`) and M3 (the lobby toast).
- `common/scripted_effects/eotg_unclaimed_effects.txt:347` and `:357`: **map colour (V-U6).** `set_title_color` and `set_color_from_title` on a **county** title change the realms map, and persist through save and reload. Vanilla has only proven them on an empire title.
- `common/governments/eotg_unclaimed_government.txt:89`: **attrition semantics (V-U3).** `supply_limit_mult_for_others` hits an army standing in the placeholder's county. The `.info` only says "army owners of different government type". The fallback is the commented line in `eotg_unclaimed_mod_unclaimed`.
- `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt:31`: **the trigger override** (above; blocking V-U2).

**The rest:**
- `common/governments/eotg_unclaimed_government.txt:17`: every government field exists in 1.20.0.3 (Tiger and PX don't check them). Check by hand against `_governments.info` and `herder_government`.
- `common/governments/eotg_unclaimed_government.txt:21` (V-U10): an unset `fallback` isn't a fallback, and `can_get_government` on the trait doesn't block the scripted `change_government`.
- `common/scripted_effects/eotg_unclaimed_effects.txt:106`: `create_character` in a **county title** scope, with `dynasty = none` and `rite = <county>.rite` (the MPO shape). The mod's own calls all run in a character scope.
- `common/scripted_effects/eotg_unclaimed_effects.txt:109`: `becomes_independent = { change = … }` with `type = independency`.
- `common/scripted_effects/eotg_unclaimed_effects.txt:230` (V-U8): a title transfer inside `on_death` works.
- `common/scripted_effects/eotg_unclaimed_effects.txt:254`: `every_ruler` reaches independent counts (the seed).
- `common/scripted_effects/eotg_unclaimed_effects.txt:33`: `is_target_in_global_variable_list` (name/target).
- `common/on_action/eotg_unclaimed_on_actions.txt:30` (V-U9): `on_title_gain` fires for scripted `change_title_holder`.
- `common/on_action/eotg_unclaimed_on_actions.txt:83`: `yearly_global_pulse` is the live hook name (pitfalls §12).
- `common/scripted_triggers/eotg_unclaimed_triggers.txt:37`:
  - `any_neighboring_county` from a county scope;
  - `target_is_liege_or_above`;
  - `this.title_province` inside the `squared_distance()` string.
- `common/scripted_triggers/eotg_unclaimed_triggers.txt:72`: `domain_size < domain_limit`.
- `common/script_values/eotg_unclaimed_values.txt:16`: `squared_distance_medium` exists.
- `common/scripted_character_templates/eotg_unclaimed_templates.txt:11`: `culture = this.culture` / `faith = this.faith` in a template.
- `common/traits/eotg_unclaimed_traits.txt:15`: `celibate.dds` exists as a vanilla trait icon.
- `common/character_interactions/eotg_unclaimed_interactions.txt:23`: `interaction_category_diplomacy`.
- `common/character_interactions/eotg_unclaimed_interactions.txt:94` (V-U14): placeholders count as `neighboring_rulers`.
- `common/scripted_effects/eotg_frontier_effects.txt:1756`: `ordered_in_global_list` with `limit` and `order_by`.
- Unmarked, but standard and worth a glance: `set_global_variable` with `days =` (the AI gap), and `add_prestige` with a negative value block.

## In-game verification list (spec §12), updated for what was built
Setup: `-debug_mode`. **Test map:** c_aphion_seam and c_helios_shoal start unclaimed. **Vanilla map:** load the sub-mod, and Sardinia's 5 counties are released at start. Corsica stays owned-Unsettled. Anywhere: **(Debug) Release a Region to the Unsworn**, or `effect title:<c_key> = { eotg_unclaimed_release_effect = yes }`.
1. **V-U1 Playability:** take **(Debug) Unclaimed Regions Readout**. The first toast says "IS playable" or "is NOT playable". Also try picking an Unsworn holder in the lobby's free pick. **This decides M2 and M3**, which are not built.
2. **V-U2 War immunity:** **blocked** until the override is pasted in (above). Then:
   - check `database_conflicts.log`;
   - `add_claim` on an unclaimed county gives no CB;
   - in a 20-year observer run, no placeholder declares war.
3. **V-U3 Attrition:** park a 3,000+ army in an unclaimed county, then claim it and compare the supply limit. Expect −0.5 (the government) plus −0.25 (the Unsettled modifier, now built). If the government part doesn't show, uncomment the fallback line in `eotg_unclaimed_mod_unclaimed`.
4. **V-U4 History seed (test map):**
   - the seed `eotg_unclaimed_seed` gets `eotg_unclaimed_government` from title history (it carries the trait, which `can_get_government` needs);
   - at start each county has its own Unsworn holder, with the county's culture and faith;
   - the seed is gone;
   - the readout counts 2 Regions and 2 Unsworn.
5. **V-U5 Capital barony:** the script now moves it explicitly when the old holder held it. Check that the placeholder (or the claimant) holds the capital barony, and that nothing errors if the engine had already moved it.
6. **V-U6 Colour:**
   - released counties turn slate `{ 88 92 100 }`; on the test map the history colour is already slate;
   - a claimed one takes the claimant's primary title colour;
   - both survive save and reload.
7. **V-U7 Vanish:** after a claim the old placeholder is gone, with no death notification to players. The readout's "Unsworn alive" drops by one.
8. **V-U8 Death:** kill a placeholder (`effect character:<id> = { death = { death_reason = death_natural_causes } }`). The county passes to a new Unsworn holder at once (`on_death`), or by the next 1 January (the sweep). The readout's "fixed by the last yearly sweep" is 0 if `on_death` worked.
9. **V-U9 Catch-all:** `effect title:<unclaimed c_key> = { change_title_holder = { holder = character:<your id> } }` from the console. The county loses `Unclaimed Region`, recolours, and you get the "colours now fly" toast.
10. **V-U10 Government gate:** placeholders get the government, and no ordinary count ever ends up with it (observer run).
11. **V-U11 Trait blockers:** marriage interactions refuse an Unsworn holder, and holding the county is unaffected.
12. **V-U12 Realm name:** does "Unclaimed Region" (`eotg_unclaimed_government_realm`) show on the map or in the realm name?
13. **V-U13 Persistence:** `eotg_unclaimed_county`, `eotg_unclaimed_claimed`, the list (readout count) and the colours survive save and reload.
14. **V-U14 AI targets:**
    - in a 20-year observer run, AI rulers next to placeholders claim with *Raise Your Colours*;
    - at most about 2 a year worldwide (the 180-day gap);
    - no AI holds more than 2 claimed, unsettled Regions.
15. **V-U15 Abandon:**
    - claim a Sardinian Region from Corsica, mark nothing (it's already Unsettled), Establish, then abandon. The decision and .005 (a) show "Abandoning the Frontier gives it up"; the Region goes back to grey, Unclaimed and Abandoned, keeping its traces, and a toast says so;
    - a Corsican (owned, never claimed) abandonment stays with its holder;
    - a claimed **capital** Region stays, Abandoned.

**New checks for this build:**
- **Raise Your Colours:**
  - it shows only on Unsworn holders whose Region is unclaimed;
  - it greys out with the reasons in words (reach, gold, standing);
  - it charges minor gold and minor prestige on accept, with a 5-year cooldown per actor;
  - *Establish a Frontier* becomes available for that Region.
- **Expedition to unclaimed space:** mark a Sardinian Region Unknown (c_tortoli already is). From Corsica, **Send an Expedition** offers it if it is in reach: own Regions first, then unclaimed. Filing the charts at Known gives the Region survey data for whoever claims it.
- **Placeholders stay out of mod content:** no cybernetics or Frontier events or offers ever reach an Unsworn character (`error.log` lines with `eotg_is_unclaimed`).
- **.040 on a Military Frontier:** the desc offers only money behind the venture, with no convoy guards.

## Deviations from the spec (also in its §20)
1. The override ships inert (above).
2. M2 and M3 are not built: the spec makes them conditional on V-U1. M1 (the pulse guards) is built: the five yearly augmentation checks, the non-ruler, former and seamless checks, both augmentation death hooks, the Frontier yearly tick and the Frontier sponsor-death hook all skip `eotg_is_unclaimed_folk = yes`. **Not guarded:**
   - `eotg_on_game_start_aug_init` (no root);
   - `on_birth_child` (placeholders have no children);
   - the combat and activity hooks (placeholders have no armies, knights or activities);
   - `on_trait_gained`.
3. Expedition targeting is widened now, as this brief asked (the spec's UD2 had it later).
4. The capital barony is moved explicitly (a no-op if the engine already does it).
5. A one-county history placeholder is adopted. A seed being split is flagged `eotg_unclaimed_splitting`, so it is never adopted.
6. The seed must carry `eotg_unclaimed_folk` (add to the cartographer's §10 step 2).
7. New identifiers beyond §3 (listed in spec §20 item 7), among them:
   - `eotg_unclaimed_would_release`;
   - `eotg_unclaimed_on_abandoned_effect`;
   - `eotg_unclaimed_ai_gold_floor_value`;
   - `eotg_unclaimed_sweep_fixed`.
8. "Unsworn" is the trait's display name (one person); the people are "the Unsworn". The interaction key stays `eotg_unclaimed_claim_interaction`.
9. Expeditions into unclaimed space fire `eotg_frontier_on_explored` with root = the placeholder, because Frontier hooks fire on the county holder.
10. Test-map counties: c_aphion_seam and c_helios_shoal. They are adjacent (computed from `provinces.png`), border both big realms, and neither is anyone's only county. c_aphion_seam was in the cybernetics §1c development-10 list, but no ruler's gate read it.

## Also done (Phase 3a, small)
.040's desc is now a `first_valid` with a Military variant, `eotg_frontier.040.desc_military`. It offers only money behind the venture and keeps the lore-keeper's wording otherwise.

- **needs-local-validation:** Tiger + PX on every file listed above, plus the hand check of the government block against `_governments.info` and `herder_government` (Tiger doesn't know 1.20 government fields).
- **needs-loc:** none; 33 keys are written in `eotg_unclaimed_l_english.yml`, plus `eotg_frontier.040.desc_military`. The localizer may later add `eotg_unclaimed_defender_tt` inside the override once it is live.
- **needs-lore:**
  - the new loc: the government desc and flag line, "Unsworn", the modifier desc, the interaction tooltips, the release toast and the abandon warning;
  - .040's Military desc.
- **needs-human:**
  - V-U1's answer (M2 and M3);
  - UQ8 (the colour) in game;
  - whether to accept placeholder-rooted `eotg_frontier_on_explored` hooks.
- **taskboard:**
  - **new item:** "Unclaimed Regions: paste the vanilla `herders_and_tributary_constraints` body into the override (blocks V-U2), add pitfalls entry N";
  - **new item:** "Unclaimed Regions: in-game V-U1..V-U15";
  - **new item:** "Cartographer §10: the seed carries `eotg_unclaimed_folk`";
  - the merge order is Phase 3a, then this branch.
