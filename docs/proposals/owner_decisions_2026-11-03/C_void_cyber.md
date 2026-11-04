# Decisions C: Void Corruption (Q1, Q2, Q4, Q5, Q6, V1, V2) and cybernetics P4

**Date:** 2026-11-03. **Status:** suggestions for the owner. Nothing in the repo was changed.
**Sources:**
- Vanilla CK3 1.20.1.1 at `D:/SteamLibrary/steamapps/common/Crusader Kings III/game` (abbreviated `V:`). This is the precedent.
- Six workshop overhauls, used for technique only. They are never precedent and nothing was copied from them.
- The spec `docs/specs/void_corruption_v2.md` §11 and the sim report `docs/qa/mechanics_sim_2026-11-03/REPORT.md`.
- The Void script (`common/*/eotg_void_*`, `events/eotg_void_*`) and the cybernetics values and triggers.

**New sim runs.** Some numbers are new what-ifs. I ran them with the repo's own models (`docs/tools/sim/models/void.py`, `cybernetics.py`): 10,000 seats, seed 20261103, player seat at 4% contact, 100 years, unless stated otherwise.
- The drivers are `docs/tools/sim/whatif/void_cyber_variants.py` and `void_cyber_variants2.py` (their JSON output is regenerated, not kept).
- The base case reproduces the REPORT exactly: stage C 0.038, Touched 4 years, Overclocked 34.0% / 5.5%.

Q3 (who carries `eotg_grip_survivor`) is left to canon and the vault, as asked.

---

## Cross-cutting finding: a flag set "for N years" is checked on the day it expires

**What happens now.** `yearly_playable_pulse` fires once a year per character (`V:common/on_action/yearly_on_actions.txt:979-981`). Every Void cooldown is `add_character_flag = { ... years = N }`, set during that pulse (`common/on_action/eotg_void_on_actions.txt:48-185`). So the flag expires on the same day as the pulse N years later. Whether it still blocks that pulse depends on the engine's order of operations.

**What vanilla does.** Vanilla sidesteps this on purpose:
- `stress_threshold_cooldown_duration = 1824 # 1 day less than 5 years` (`V:common/script_values/00_stress_values.txt:77-78`);
- the note "for the cooldown duration - 1 days" (`V:common/scripted_effects/00_stress_effects.txt:56-63`).

**Why it matters.** The sim treats "N years" as ready at pulse T+N. If the engine instead sees the flag at T+N, every Void cooldown runs a year longer. The V1 numbers would then shift (option A at "2 years" behaves like the 3-year row below: 0.173, not 0.238).

**Suggestion.** Write the cooldowns as days minus one, `days = 1824` for 5 years and `days = 729` for 2. Or name them in `eotg_void_values.txt` as vanilla does. This is a mechanical change to the 16 `add_character_flag` lines in the on_action; no design changes. Confidence: high that vanilla does this deliberately. The engine's order on the boundary day is UNVERIFIED; test V-V1 or V-V17 would show it.

---

## Q1. Should Void Corruption be designated mod-exclusive?

1. **Question.** Can the Void merge and be tested on the temporary map before Gate 1?
2. **Vanilla comparables.** None; this is a project-process call. The test is CLAUDE.md's rule that a mod-exclusive system has no title, province, culture, faith or character dependencies.
3. **Check performed.**
   - Grepping the Void script for `title:`, `culture:`, `faith:`, `religion`, `province:` and `dynasty:` finds nothing.
   - Its only outside keys are vanilla traits: personalities, `education_*`, `lunatic_*`/`possessed_*`, `zealous`.
   - The two world-dependent hooks are both inert by design: `eotg_void_is_cult_faith = always = no` (`common/scripted_triggers/eotg_void_triggers.txt:21-23`) and `eotg_grip_survivor`, which nobody carries.
4. **Suggested answer.** **Yes, designate it.** Same terms as cybernetics: it is tested on the temporary map, and the cult and bloodline branches stay inert until B-FAITHS and Gate 1 land.
5. **Confidence.** High.
6. **Script change.** None. Add "Void Corruption" to the mod-exclusive list in CLAUDE.md and update CB-65 (orchestrator).

---

## Q2. What is a Void cult in v2, and how do we key it without a faith key?

1. **Question.** `eotg_void_is_cult_faith` gates 25 call sites (counted with `grep`; the spec says 23). How should it detect a cult once faiths exist, using a doctrine or tenet rather than `faith:eotg_faith_void_cult`?

2. **Vanilla comparables (1.20.1.1).**
   - **1.20 moved tenets onto rites.** Across `common` and `events`, vanilla uses:
     - `has_doctrine = tenet_*`: **0** times;
     - `rite_has_tenet`: 1,181;
     - `rite_has_doctrine`: 1,867;
     - `rite_has_parameter`: 1,603;
     - `has_doctrine_parameter`: 764.
     So the lift plan's example `faith = { has_doctrine = tenet_esotericism }` (`docs/specs/void_lift_plan_cloud.md:290`) is not the 1.20 form. Its folder `common/religion/doctrines/` (`:291`) does not exist either; tenets live in `V:common/religion/tenet_types/`.
   - **Tenets are meant for this.** "Faith tenets are what defines how a faith works. All unique faith mechanics are tied to tenets, rather than involving hardcoding" (`V:common/religion/tenet_types/_tenet_types.info:3`).
   - **Vanilla gates behaviour on a parameter, not on a key.** The witch secret's shunned and criminal triggers read `rite = { rite_has_parameter = witchcraft_shunned }` and `... witchcraft_illegal }`, on the owner and on `any_liege_or_above` (`V:common/scripted_triggers/00_secret_type_triggers.txt:383-399`). The `witch` trait's opinion is also keyed on the parameter (`V:common/traits/00_traits.txt:12632-12641`).
   - **How a tenet declares a parameter.** `tenet_esotericism` has `parameters = { tenet_esotericism_mystic_education ... }` (`V:common/religion/tenet_types/00_tenet_types.txt:2112, 2185-2191`).
   - **The invisible marker doctrine (the alternative).**
     - Defined at `special_doctrine_is_western_christian_faith = { ... visible = no  parameters = { is_western_christian_faith } }` (`V:common/religion/doctrine_types/40_doctrines_special.txt:457-466`).
     - Its group is `category = not_creatable` (`V:common/religion/doctrine_group_types/00_doctrine_group_types.txt:187-193`), and that category is `visible = no` (`V:common/religion/doctrine_category_types/00_doctrine_category_types.txt:23-26`).
     - It is listed in the faith's own `doctrines` (`V:common/religion/faith_types/00_faith_types.txt:922-929`).
     - It is read as `rite = { rite_has_doctrine = special_doctrine_is_western_christian_faith }` (`V:common/activities/activity_types/ecumenical_council.txt:1388-1396`). That shows a rite sees the faith's own doctrines.
   - **A mixed check.** `rite = { rite_has_tenet = tenet_tax_nonbelievers }` and `faith = { has_doctrine = special_doctrine_jizya }` appear side by side (`V:common/achievements/fp3_achievements.txt:26-27`).
   - Vanilla uses invisible markers for **classification** (portraits, council rules) and tenets or parameters for **mechanics**.

3. **Mod techniques (observational).**
   - **Invisible marker doctrines.** A Game of Thrones tags cult faiths with `visible = no` marker doctrines checked with `has_doctrine`.
   - **Doctrine or rite parameters.** Elder Kings 2 keys vampirism on rite doctrines and parameters, `rite_has_parameter = vampirism_shunned/criminal`, including a liege check. After the End uses `has_doctrine_parameter = dark_covens_active`.
   - **Faith keys.** Godherja and LotR key on `faith:` or `religion:` directly. That is exactly what the map-agnostic rule forbids.

4. **Suggested answer.** Key the cult on a **parameter, `eotg_void_cult`**, granted by **a mod tenet, `eotg_tenet_void_communion`**. Read it from the character's rite:
   ```
   eotg_void_is_cult_faith = {
       rite = { rite_has_parameter = eotg_void_cult }
   }
   ```
   Keep `always = no` until the first religion with this tenet ships (B-FAITHS).

   **Why a tenet and not the invisible marker:**
   - It is visible, so a player can see what makes their faith a Void cult.
   - It can be adopted on reformation, so cults can emerge in play. That fits canon's "clandestine covens endure".
   - Any faith or rite can carry it, so it is map-agnostic.

   **Why a parameter and not `rite_has_tenet`:** a later heresy rite or special doctrine can also grant `eotg_void_cult` without touching the 25 call sites. This is the witchcraft pattern.

   **Do not** key on the brief's vanilla tenets (esotericism, sacred destruction, human sacrifice). Vanilla faiths carry them too, so unrelated faiths would become Void cults.

   **Vault question.** Canon has to say which tenet the Grip-Touched faith (`eotg_faith_void_cult`, `intake/setting/religion_void_reverence.md:54-62`) gives up for it. A faith carries three tenets; tenet 1, "Esotericism… forbidden void philosophy", is the closest fit. The lore-keeper must also confirm that "the Marked" are this faith's believers (CB-65).

5. **Confidence.** High for the mechanism (vanilla 1.20 forms with a 1,600-use precedent). Medium for the tenet-versus-marker choice, which is a design call.

6. **Script change (when B-FAITHS lands; nothing now).**
   - **New file** `common/religion/tenet_types/eotg_void_tenets.txt`. Shape: copy a vanilla tenet (`00_tenet_types.txt:2112-2202`): icon, `piety_cost`, `parameters = { eotg_void_cult }`. The `_tenet_types.info` fields are for eotg-vanilla-scout to confirm.
     - `common/religion/tenet_types/` is **not in the CLAUDE.md file-placement list**, so add it.
     - Tiger 1.17 cannot validate it (the CLAUDE.md religion caveat), so check it by hand.
   - **Trigger body** at `common/scripted_triggers/eotg_void_triggers.txt:21-23` as above. All 25 sites already route through it.
   - **Loc:** `eotg_tenet_void_communion_name` / `_desc`.
   - **Sibling:** CB-12's machine-sacred inversion can use the same pattern, e.g. a parameter `eotg_machine_sacred` on a tenet.

---

## Q4. Do the devout dislike a Voidwalker at court?

1. **Question.** Should we keep v1's −10 opinion from zealous courtiers and the piety costs? 0004.a costs −100 piety, and the Voidwalker Ward decision costs −150 piety plus zealous −10 (`events/eotg_void_whispers.txt:288-296`, `common/decisions/eotg_void_decisions.txt:95-98`).

2. **Vanilla comparables.**
   - `zealous`: `opposite_opinion = -10`, `opinion_of_different_faith = -35` (`V:common/traits/00_traits.txt:3947-3949`). So −10 is vanilla's "temperament clash" scale.
   - A known witch, where witchcraft is shunned: `witchcraft_intolerant = { opinion = -15 }` (`V:common/opinion_modifiers/00_doctrinal_crime_opinions.txt:32-35`). Where it is criminal: `witchcraft_crime = -15` plus imprisonment and execution reasons (`:25-30`).
   - Both are keyed on rite parameters, never on a blanket "devout" (`V:common/traits/00_traits.txt:12632-12641`).
   - Piety scale: `medium_piety_value = 100`, `major_piety_value = 250` (`V:common/script_values/00_basic_values.txt:1133-1134`).

3. **Mod techniques.** Elder Kings 2 splits a condition's social cost by faith stance: a secret if shunned or criminal, open otherwise. A Game of Thrones gates its healers on a faith parameter.

4. **Suggested answer.** **Yes, mildly. Keep −10 for 10 years and the piety costs.**
   - −10 sits below vanilla's known-witch −15 and carries no crime reasons, which reads as "discomfort, not heresy" (ruling R4).
   - The −100 and −150 piety are about vanilla `medium_piety_value`. When that code is next touched, write them as `medium_piety_loss` rather than raw numbers.
   - **Later (with Q2):** make the zealous reaction depend on the faith, like CB-12. ERRATA YU says Yu blesses Malvrick's orders, so a faith that honours those orders should not resent their blade.
   - **Lore-keeper:** confirm that the dislike is canon at 866. REVIEW_866:64 makes the Orders open and not heretical.

5. **Confidence.** Medium-high on the numbers. The canon point is still for the lore-keeper.

6. **Script change.** None now. Later, wrap the two `every_courtier = { limit = { has_trait = zealous } ...` blocks with a faith-parameter check (`NOT = { rite = { rite_has_parameter = eotg_honours_malvrick_orders } }`), in the same pass as CB-12.

---

## Q5. Contact rate for AI rulers

1. **Question.** Keep 4% a year for players and 1% for the AI (`common/script_values/eotg_void_values.txt:60-66`)?

2. **Vanilla comparables.**
   - **Vanilla scales by tier, not just player versus AI.** `random_yearly_playable_pulse` adds `chance_of_no_event` for the AI: 30 at kingdom+, 70 at duchy, 95 at county (`V:common/on_action/yearly_on_actions.txt:3038-3059`). The AI therefore gets ×0.7, ×0.3 and ×0.05 of the player's flavour rate.
   - **Rare onset for dark conditions.**
     - Lunatic and possessed onset: weight 5 each (`V:common/on_action/yearly_on_actions.txt:3545-3549`).
     - Witch first contact (trait_specific.4001, "an old tome"): weight 50 (`:3553`).
     - All three sit inside `on_yearly_events`, which itself has `chance_to_happen = 25` and a 200 weight of "no event" (`:3467-3470`).
     - Each onset sets a 10-year re-roll flag (`V:events/trait_specific_events/trait_specific_events.txt:281-285` for lunatic).
   - **Epidemics: rare start, fast spread.**
     - Outbreak per province per year: base 0.0005–0.12% (`V:common/script_values/06_ce1_epidemics_values.txt:14-19`).
     - Inside an outbreak, the monthly infection chance per character is 10 + 10 to 40 (`:1668-1705`; "Monthly chance", `V:common/epidemics/_epidemics.info:37-42`).
   - **Secret faiths and witchcraft spread by relationship, not by roll.** Guardian to ward at 15 (`V:common/on_action/childhood_on_actions.txt:175-181`). Instant if both are AI and part of a coven or zealous (`V:events/witch_events.txt:18-50`, `V:events/secret_faith_events.txt:13-50`).
   - **Discovery.** A spymaster's chance to find a secret = intrigue × 5, max 95 (`V:common/script_values/99_spymaster_values.txt:486-497`).

3. **Mod techniques.**
   - Elder Kings 2: county spread on the quarterly pulse at about 5% plus modifiers, only next to an affected county, then self-blocked for 10 years. A game rule multiplies it by ×0.5, ×2 or ×4.
   - Elder Kings 2 also spreads character to character on purpose, through a scheme.
   - The Fallen Eagle (a vanilla heresy copy): monthly per faith at 25%, mostly suppressed by fervour.
   - Godherja: fog spreads on a 120-day tick.
   - Pattern: rare spontaneous contact; spread through adjacency or relationships; a cap after spread.

4. **Suggested answer.** **Keep 4% for players, and split the AI's 1% by tier in vanilla's shape: kingdom+ 2%, duchy 1%, county 0.5%.**
   - The sim says the rates scale almost linearly (`REPORT.md:250-256`). On 50-year seats:
     - kings at 2%: about 64% contacted, 8% Touched;
     - dukes at 1%: 40%, 4.6%;
     - counts at 0.5%: 23%, 2.5%.
   - So the Void shows up where the player looks (rival kings and dukes), and stays rare among the many counts.
   - The flat 4/1 is an acceptable fallback; the sim's "keep" stands either way.
   - Spread between characters already exists, by vanilla's relational logic. A Touched courtier, vassal or spouse adds +4 accrual (`eotg_void_values.txt:15`), so no contact-by-proximity roll is needed.

5. **Confidence.** Medium. The tier split is a refinement with clear vanilla shape; the 4/1 core is simulated.

6. **Script change.** `common/script_values/eotg_void_values.txt:60-66`:
   ```
   eotg_void_contact_chance_value = {
       value = 4
       if = {
           limit = { is_ai = yes }
           value = 0.5
           if = { limit = { highest_held_title_tier >= tier_duchy }    value = 1 }
           if = { limit = { highest_held_title_tier >= tier_kingdom }  value = 2 }
       }
   }
   ```
   - Decimal chances are valid in `random`: `chance = 0.05` (`V:common/on_action/travel_on_actions.txt:606`) and `chance = 0.75` (`V:events/councillor_task_events/councillor_spouse_events/councillor_spouse_intrigue_events.txt:103`).
   - Update the comment and the spec §11 Q5 numbers.

---

## Q6. What happens at the end of stage D (depth 100)?

1. **Question.** Depth 100 has no terminal event, and the spec allows no new events. Should "Gone Quiet" (85+) stay the end state?

2. **Vanilla comparables.**
   - **Dementia is the same 0–100 meter, and it ends.** `withering_mind` has a trait XP track with bands at 25, 50, 75 and 100 (`V:common/traits/00_traits.txt:6124, 6151-6185`).
     - It advances on the yearly health pulse through `send_interface_message` alone, with no event: +50, +8, +4 or +1 by weighted roll (`V:common/on_action/health_on_actions.txt:118-235`).
     - At 100: `add_trait = incapable` (`:236-241`).
   - **`incapable` hands the ruler to a regent.** `regency_for_personal_reasons_trigger` includes `is_incapable = yes` (`V:common/scripted_triggers/00_diarchy_scripted_triggers.txt:181-193`).
     - The trait: `incapacitating = yes`, all skills ×0, `dread_baseline_add = -25` (`V:common/traits/00_traits.txt:6381-6410`).
     - The vanilla helper is `upgrade_infirm_to_incapable_effect` (`V:common/scripted_effects/20_health_effects.txt:4249-4258`).
   - **Stress does not plateau either.** 400 resets to 300 with a forced break (`V:events/stress_events/stress_threshold_events.txt:326-358`). The level-3 pool can end in `death_stress` (`:14875-14931`).
   - **Lunacy and possession never end.** They are persistent conditions with ongoing events, each on a 10-year per-event flag (`V:events/trait_specific_events/trait_specific_ongoing_events.txt:40-57`). That is the "plateau" model.
   - **Vanilla yearly flavour excludes the incapable.** `basic_is_valid_for_yearly_events_trigger` has `incapable = no` (`V:common/scripted_triggers/00_available_for_events_triggers.txt:802-807`).

3. **Mod techniques.**
   - Elder Kings 2 ends vampirism in a permanent trait swap.
   - LotR's ring chain runs out by itself after about 4 trait swaps.
   - Godherja stacks mutation traits, with thresholds that rise each time.
   - A Game of Thrones' greyscale has no terminal state.
   - None of them uses a hard plateau with the meter still running.

4. **Suggested answer.** **Make depth 100 terminal through the dementia path. No new event.**
   - The first time a Hollowed ruler's depth reaches 100, apply vanilla `incapable` with a single interface message. A regent takes over: the Void "finishes passing through them". `incapable`'s −25 dread replaces the Gone Quiet +10, which reads as a court that no longer fears someone who is not there.
   - It stays avoidable. In the sim (new run), only **34–36% of Hollowed rulers ever reach depth 100**, at a median of **19 years after the Hollowing**, because the 0030–0032 "presence" options pull depth back. Step Down (0030.c) also remains.
   - Make it one-way, as vanilla never removes dementia's `incapable`.
   - Add `is_incapable = no` to the stage-D roll, following vanilla's yearly-event gate.
   - If the owner prefers the lunacy model, the spec's default (Gone Quiet as a plateau) is the fallback. In that case, stop the +4 drift at 100: there is nothing left to drift toward.

5. **Confidence.** Medium. The vanilla shape is exact, but whether the Hollowing should end in incapacity is a design and canon call, and the lore-keeper should see the message text.

6. **Script change.** In `common/on_action/eotg_void_on_actions.txt`, right after the depth drift at `:40-43`:
   ```
   if = {
       limit = {
           has_trait = eotg_void_hollowed
           var:eotg_void_hollowing_depth >= 100
           NOT = { has_trait = incapable }
       }
       send_interface_message = {
           type = msg_health_change                 # vanilla type, health_on_actions.txt:228
           title = eotg_void_gone_message_title
           left_icon = root
           upgrade_infirm_to_incapable_effect = yes # vanilla 20_health_effects.txt:4249
       }
   }
   ```
   - Add `is_incapable = no` to the stage-D branch's limit (`:60-61`).
   - One loc key: `eotg_void_gone_message_title`. External register; for example, "Gone quiet: [ROOT.Char.GetName] no longer answers."
   - Add test V-V21: depth 99 → +4 → `incapable`, a regent seated, and 0031/0032 no longer roll.

---

## V1. Touched-stage events: option A (cooldown 5 → 2) or option B (Touched accrual +6 → +2)?

1. **Question.** All six stage-C events together fire about 0.04 per 100 seat-years. Which lever should fix it?

2. **Vanilla comparables.**
   - **Cooldowns are per stage, and reaching a higher stage is not blocked by a lower stage's cooldown.**
     - Stress uses three flags, `stress_threshold_event_1/2/3_cooldown`, each set for 1,824 days (`V:common/scripted_effects/00_stress_effects.txt:57-80`).
     - The break dispatcher fires a level-N break whenever the level-N flag is clear, even if lower-level flags are set (`V:events/stress_events/stress_threshold_events.txt:62-76`).
     - On reaching a new level, the break follows 3 days later (`V:common/on_action/stress_on_actions.txt:34-43`).
     - Here, the Bargain's 5-year cooldown blocks the very stage it opened. That is the opposite of vanilla's shape.
   - **Rhythm of an ongoing dark condition.**
     - Angry ghosts: one roll every 60–365 days at 50% (`V:common/story_cycles/bp1_story_cycle_visited_by_angry_ghosts.txt:14-27`).
     - Plague witch hunt: 365–600 days at 50% (`V:common/story_cycles/ce1_story_cycle_plague_witch_hunt.txt:43-72`).
     - So about one event every 1–2.5 years while the condition lasts.
   - **The stage's length is a separate dial.** Dementia's meter speed sets how long each band lasts (`V:common/on_action/health_on_actions.txt:118-235`). It is not used to fix event cadence.

3. **Mod techniques.**
   - Godherja's shade-plague story shortens its interval as the threat nears: 2–4 months, then 1–2 months, then 21–37 days.
   - LotR re-queues its next step 12–18 months after each event.
   - Pattern: cadence is set by the event timer, and stage length is a separate dial.

4. **Suggested answer.** **Option A: set the cooldown that 0010 and 0011 set to 2 years (as `days = 729`). Keep the Touched accrual at +6.**

   | Case (player, 4%, 100 y) | Stage C / 100 seat-yr | Stage C per Touched ruler | Touched, median yr | Ever Touched | Ever Hollowed | 0010 per seeded ruler |
   |---|---|---|---|---|---|---|
   | As scripted | 0.038 | 0.12 | 4 | 30.9% | 26.4% | 0.57 |
   | **A: 0010/0011 → 2 y** | **0.238** | **0.76** | **4** | 31.2% | 25.5% | 0.59 |
   | A at 3 y (what "2 years" becomes if the flag survives its last day) | 0.173 | 0.56 | 4 | 30.7% | 25.6% | — |
   | Vanilla-literal per-stage: entering Touched sets 1 y | 0.289–0.314 | 0.95–1.03 | 4 | 30.4% | 25.2% | 0.56 |
   | B: Touched +2 | 0.211 | 0.68 | 6 | 30.9% | 22.8% | — |
   | A + B | 0.391 | 1.29 | 6 | 30.2% | 21.6% | — |

   **Why A:**
   - It removes the actual constraint and leaves the Hollowing's threat and the Touched length unchanged.
   - It matches vanilla's per-stage cooldown shape.
   - The worry that the Bargain would be re-offered more often does not hold up. 0010 fires 0.59 times per seeded ruler, against 0.57, because almost every Bargain ends in Touched or Defiant.

   **Why not B:** B is a balance change disguised as a pacing fix. It cuts the Hollowing rate by 14% and stretches Touched by half, while A alone already gives more events than B.

   **Optional, later.** For a full Touched ruler's arc of about one stage-C event, use the per-stage-flag version: a separate `eotg_flag_void_touched_cooldown` read only by the stage-C branch, like vanilla's per-level flags. That is a restructure, not a value change, so it is not proposed now.

5. **Confidence.** High that A beats B. Medium on 2 against 1 year; both are defensible.

6. **Script change.**
   - `common/on_action/eotg_void_on_actions.txt:127` (0011) and `:137` (0010): `add_character_flag = { flag = eotg_flag_void_event_cooldown  days = 729 }`.
   - Update the cooldown table in the header comment (`:21-23`) and spec §3.5.
   - This needs a new hunk, because the sim patch only carries V1-as-B.

---

## V2. The Voidwalker is rare. Should 0004 go from 12% to 25%?

1. **Question.** 0.46–0.50 Voidwalkers per 100 seat-years, of whom about 29% are seated. Should Voidwalkers be more common?

2. **Vanilla comparables.**
   - **Vanilla's counter-role for a dark condition is on hand, not a rare visitor.** The possessed treatment event needs only a court chaplain or a clergy courtier of the same faith (`V:events/trait_specific_events/trait_specific_ongoing_events.txt:1413-1440`, trigger at `:1425-1440`). The depressed get "Your court physician tries to treat you" (`V:common/on_action/yearly_on_actions.txt:3638`).
   - **Holy orders reach courts often.** "Military Order suggests you send them a child" has weight 200, against 5 for lunatic onset, in the same pool (`V:common/on_action/yearly_on_actions.txt:3609`).

3. **Mod techniques.**
   - LotR's hunter (the Nazgûl) returns every 9–12 months and escalates with each failure.
   - Elder Kings 2 has no hunter. Its counter is a cure timer that races the transformation timer.
   - Pattern: when a counter-role exists, it is frequent enough to matter.

4. **Suggested answer.** **Take V2 at 25%, together with V1-A.**

   | Case (player, 4%, 100 y) | Voidwalkers / 100 seat-yr | Ever Touched | Ever Hollowed | Stage C / 100 seat-yr |
   |---|---|---|---|---|
   | As scripted | 0.50 | 30.9% | 26.4% | 0.038 |
   | V2 alone | 0.94 | 28.8% | 24.3% | 0.033 |
   | A + V2 at 20% | 0.83 | 29.5% | 24.6% | 0.215 |
   | **A + V2 at 25%** | **0.97** | **27.4%** | **22.5%** | **0.196** |

   - Canon supports it. At 866 the Orders are open, and the Voidwalkers are "those who go where the Void has left a mark" (REVIEW_866:64; spec §8.3). It is natural that they turn up at marked courts.
   - The world stays sparse. An AI seat at 1% sees about 0.2 → 0.4 per 100 seat-years.
   - Leave the exposure gate (≥ 20, `:179`) alone, as the REPORT advises.

5. **Confidence.** Medium. The number is simulated; whether Voidwalkers should be twice as visible is a design and canon call.

6. **Script change.** `common/on_action/eotg_void_on_actions.txt:184`: `chance = 25`.

---

## P4. Overclocked development gate, 20 → 15?

1. **Question.** Should the Overclocked gate (`eotg_aug_dev_gate_overclocked`, `common/script_values/eotg_augmentation_values.txt:25-27`) drop to 15, the same as the Enhanced gate (`:22-24`)?

2. **Vanilla comparables.**
   - **Vanilla's stepped thresholds always rise strictly:**
     - stress 100/200/300/400 (`V:common/script_values/00_stress_values.txt:20-23`);
     - epidemic infection levels 10/50/80 (`V:common/epidemics/00_epidemics.txt:148-172`);
     - dementia bands 25/50/75/100 (`V:common/traits/00_traits.txt:6151-6185`).
   - A gate equal to the one before it is no gate.
   - **Development gates in vanilla decisions:** `convert_to_feudalism_development_requirement` = 10 (`V:common/script_values/50_major_decision_values.txt:25-26`), and 30 for the university decisions (`V:common/decisions/80_major_decisions.txt:1861-1939`).

3. **Mod techniques.** Godherja raises each mutation threshold by multiplying it by the mutation count. The pattern is to escalate gates, not flatten them.

4. **Suggested answer.** **Hold at 20 until the real map lands.** If the owner wants more Overclocked now, use **18, not 15** (new runs, 4 vassals):

   | Gate | Pushing player reaches OC | OC within 20 y | Cascade deaths | AI reaches OC |
   |---|---|---|---|---|
   | 20 (now) | 34.0% | 26.1% | 9.4% | 5.5% |
   | 18 | 41.1% | 32.0% | 11.8% | 6.8% |
   | 17 | 45.5% | 35.8% | 12.8% | 7.2% |
   | 15 (P4) | 50.7% | 41.8% | 14.5% | 7.5% |

   **Why:**
   - At 15, development stops being a separate step; only time and gold remain.
   - It raises cascade deaths by half.
   - It barely helps the AI (5.5% → 7.5%). The AI's shortfall against HQ2 (≥ 15% at Overclocked or beyond) comes from `ai_will_do` and the tier-2 ×0.5 prudence, not from development. So P4 does not fix the target it is aimed at.
   - The spec already marks the gates as provisional to the real map (`docs/specs/cybernetics_v2_balance.md:202-205`).

5. **Confidence.** High on "not 15". Medium on 18 as the interim value.

6. **Script change.** None (hold). If the owner chooses the interim value: `eotg_augmentation_values.txt:26`, `value = 18`. The Enhanced gate stays 15.

---

## Summary

1. Q1: designate the Void mod-exclusive. It has no map, faith or title keys; the cult and bloodline branches stay inert.
2. Q2: in 1.20, tenets live on rites (0 vanilla `has_doctrine = tenet_*`). Key the cult on parameter `eotg_void_cult` from a mod tenet in `common/religion/tenet_types/`, read with `rite = { rite_has_parameter = eotg_void_cult }`.
3. Q4: keep the zealous −10 (vanilla zealous `opposite_opinion` −10, below the known-witch −15) and the piety costs. Make it faith-dependent later, with CB-12.
4. Q5: keep 4% for players; split the AI by tier in vanilla's chance_of_no_event shape: kingdom+ 2%, duchy 1%, county 0.5%.
5. Q6: make depth 100 terminal like dementia (vanilla `withering_mind` → `incapable` → regency), with a message and no new event. Only about 35% of the Hollowed reach it, at a median 19 years.
6. V1: option A. 0010/0011 cooldown 5 → 2 years (`days = 729`): stage C 0.038 → 0.238 per 100 seat-years, Touched stays 4 years. B trims Hollowings and stretches Touched.
7. Cross-cutting: vanilla sets cooldowns one day short (1824 days) so they clear on the pulse day. Convert the Void's `years = N` flags, or A behaves like 3 years (0.173).
8. V2: take 25% with A. Voidwalkers 0.50 → 0.97 per 100 seat-years, Hollowed 26.4% → 22.5%. Vanilla's counter-roles (chaplain, physician) are on hand, not rare.
9. P4: hold at 20. Dropping to 15 erases the Enhanced/Overclocked step and raises cascade deaths by half, and the AI barely moves (5.5 → 7.5%). Interim 18 if wanted.
10. The new sim runs use the repo's models with the same seed and reproduce the REPORT base. Drivers: `docs/tools/sim/whatif/void_cyber_variants*.py`.
