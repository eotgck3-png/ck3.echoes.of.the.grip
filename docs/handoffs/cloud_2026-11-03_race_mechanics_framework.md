# Race mechanics framework v1 (cloud, 2026-11-03)

Brief: build the race mechanics now, map-agnostic and data-driven, ahead of the real races. Design source:
`docs/proposals/race_and_heritage_groups_feasibility.md` §2–§5. As-built spec: `docs/specs/races_framework_v1.md`.
The test sub-mod is `docs/test_submods/races/`.

### HANDOFF (cloud session, unvalidated)
- branch: claude/race-mechanics-framework-cloud (from v2-space-map)
- status: done. All ten brief items are present. Items 6 and 8 are deliberately inert stubs that need vanilla
  bodies, and the `discouraged` weight is written but not wired; both are listed below.
- summary:
  - **Races.** A race is a non-genetic trait, `eotg_race_<race>`, in trait group `eotg_race`.
  - **Ancestry shares.** `var:eotg_race_share_<race>` holds the shares; `eotg_race_shares` marks an explicit profile.
    Pure characters store nothing: an implicit share of 1 in the trait's race (spec §3.2). This is a deliberate
    reading of "shares at 100%": same semantics, no save bloat.
  - **The birth roll** sits in an additive `on_birth_child` hook. It averages the parents' shares, applies the
    half-race rule, rolls one `random_list` weighted by share × 1000, then compacts pure children. Fallbacks:
    - a parent with no shares counts as 100% of its trait;
    - a parent with no trait counts as the default race;
    - a missing parent is replaced by the other one.
  - **Engine-created characters.** `on_character_created` gives the race from the culture's heritage group
    (custom pillar parameter `eotg_heritage_group_<race>`, plus the umbrella parameter `eotg_heritage_grouped`).
    Ungrouped cultures fall back to the default race. A game-start pass runs on `on_game_start` and on
    `on_game_start_after_lobby`.
  - **One registry.** All per-race data sits in 7 registry keys across 2 files. The generic logic is written once
    as `eotg_race_op_<op>_effect = { RACE }`, dispatched by literal `$OP$` replacement. Adding a race means:
    - a trait block (and its key added to the other races' `opposites`);
    - 2 registry lines in the effects file and 2 in the triggers file;
    - the heritage parameters;
    - loc.

    Spec §4.3 has the checklist.
  - **The main mod registers no races,** so `eotg_race_framework_active = no` and every hook is a no-op. The test
    sub-mod switches it on with `eotg_race_test_a` (the default), `eotg_race_test_b` and the half-race fixture
    `eotg_race_test_half_ab`.
  - **Game rules:**
    - `eotg_race_half_races`: `off` (default) splits inherited half-race shares back into the parent races;
      `as_own_race` merges min(A, B) into the half-race;
    - `eotg_race_crossbreeding`: `free` (default), `discouraged` or `forbidden`.
  - **Helpers:** `eotg_race_is`, `eotg_race_same_as`, `eotg_race_share_of` (an effect writing a local var, since
    script values take no parameters), `eotg_race_share_at_least`, `eotg_race_set_effect`.
  - **Hybrid block.** `eotg_race_cultures_can_hybridize` is active. Its vanilla override is a commented-out stub.
  - **No events or options were added,** and no gfx.
- files:
  - new, main mod:
    - `common/traits/eotg_race_traits.txt` (comment-only template)
    - `common/scripted_triggers/eotg_race_triggers.txt`
    - `common/scripted_triggers/eotg_race_registry_triggers.txt`
    - `common/scripted_triggers/eotg_race_vanilla_overrides_triggers.txt` (all commented out)
    - `common/scripted_effects/eotg_race_effects.txt`
    - `common/scripted_effects/eotg_race_registry_effects.txt`
    - `common/scripted_modifiers/eotg_race_modifiers.txt`
    - `common/on_action/eotg_race_on_actions.txt`
  - edited, main mod:
    - `common/game_rules/eotg_game_rules.txt` (2 rules appended; read-site header updated)
    - `localization/english/eotg_game_rules_l_english.yml` (12 keys appended; BOM checked `ef bb bf`)
  - new, docs:
    - `docs/specs/races_framework_v1.md`
    - `docs/specs/races_framework_v1_portrait_example.txt`
    - `docs/handoffs/cloud_2026-11-03_race_mechanics_framework.md`
  - new, test sub-mod `docs/test_submods/races/`:
    - `descriptor.mod` (`supported_version="1.20.*"`)
    - `README.md`
    - `common/traits/eotg_test_race_traits.txt`
    - `common/culture/pillars/eotg_test_race_pillars.txt`
    - `common/culture/cultures/eotg_test_race_cultures.txt`
    - `common/scripted_effects/zz_eotg_test_race_registry_effects.txt`
    - `common/scripted_effects/eotg_test_race_debug_effects.txt`
    - `common/scripted_triggers/zz_eotg_test_race_registry_triggers.txt`
    - `common/scripted_character_templates/eotg_test_race_templates.txt`
    - `common/decisions/eotg_test_race_decisions.txt`
    - `common/on_action/eotg_test_race_on_actions.txt`
    - `localization/english/eotg_test_races_l_english.yml` (BOM)
- unverified-vanilla: (file:line — what to check; full table in spec §12)
  - `common/scripted_effects/eotg_race_effects.txt:12` — U1: `$PARAM$` inside an effect name
    (`eotg_race_op_$OP$_effect`) and inside identifiers (`eotg_race_share_$RACE$`). **Load-bearing for the whole
    registry.**
  - `common/scripted_effects/eotg_race_effects.txt:28` — U3: `local_var:` readable inside a `random_list`
    modifier. Also: `change_(local_)variable` with `multiply` / `subtract`.
  - `common/scripted_effects/eotg_race_effects.txt:137` — U11: a dead parent's variables (a posthumous birth
    falls back to the father's trait).
  - `common/scripted_effects/eotg_race_effects.txt:141` — U12: fixed-point step (expected 0.001).
  - `common/scripted_effects/eotg_race_effects.txt:357` — U8: `debug_log` evaluates `[..]` data functions;
    `$RACE$` is replaced inside a quoted string.
  - `common/scripted_effects/eotg_race_registry_effects.txt:14` — U7: a stub called with an unused parameter.
  - `common/scripted_effects/eotg_race_registry_effects.txt:58` — U2: a `random_list` entry with weight 0 plus
    `modifier = { add = local_var }`; a zero-weight entry is never picked.
  - `common/scripted_triggers/eotg_race_triggers.txt:25` — U4: `has_trait = eotg_race` (a trait-group key).
  - `common/scripted_triggers/eotg_race_triggers.txt:61` — U5 / T1: a custom `parameters` entry on a heritage
    pillar, read with `has_cultural_parameter`.
  - `common/scripted_triggers/eotg_race_registry_triggers.txt:31` — U7, trigger form.
  - `common/scripted_triggers/eotg_race_vanilla_overrides_triggers.txt:5` — U18: the bodies, ranges and scope
    names for:
    - `is_valid_for_hybridising_trigger` (`00_cultural_triggers.txt:473-477`);
    - `can_have_children_with` (`00_marriage_triggers.txt:66-68`);
    - `could_marry_character_trigger` (location not cited).
  - `common/scripted_modifiers/eotg_race_modifiers.txt:15` — U18: which marriage-interaction block takes the
    `discouraged` modifier, and its scope names.
  - `common/on_action/eotg_race_on_actions.txt:24` — U6: `on_character_created` root is the new character, with
    its culture already set.
  - `common/traits/eotg_race_traits.txt:26` — U10: `has_trait_with_flag`.
  - `common/traits/eotg_race_traits.txt:40` — U9: trait `category` omitted (compare vanilla `giant` / `dwarf`).
  - `docs/test_submods/races/common/culture/pillars/eotg_test_race_pillars.txt:4,7` — U5; U15:
    `audio_parameter = european` and a direct language colour.
  - `docs/test_submods/races/common/culture/cultures/eotg_test_race_cultures.txt:4,8` — U14: the v1 vanilla
    culture keys; U13: an unused culture exists as `culture:<key>`.
  - `docs/test_submods/races/common/scripted_effects/eotg_test_race_debug_effects.txt:9` — U16:
    `while = { count }` and `make_pregnant`.
  - `docs/test_submods/races/common/scripted_character_templates/eotg_test_race_templates.txt:17` — U16: template
    `age = 0`.
  - `docs/test_submods/races/localization/english/eotg_test_races_l_english.yml:3` — U17: the pillar and
    cultural-parameter loc key forms.
  - `docs/specs/races_framework_v1_portrait_example.txt:14` — every portrait field (example only, not loaded).
- needs-local-validation: Tiger + PX on:
  - `common/scripted_triggers/eotg_race_*.txt`
  - `common/scripted_effects/eotg_race_*.txt`
  - `common/on_action/eotg_race_on_actions.txt`
  - `common/scripted_modifiers/eotg_race_modifiers.txt`
  - `common/traits/eotg_race_traits.txt`
  - `common/game_rules/eotg_game_rules.txt`
  - `localization/english/eotg_game_rules_l_english.yml`

  And separately on `docs/test_submods/races/` loaded over the main mod. Expect Tiger noise on the
  `$OP$`-dispatched effect names, which it may not expand. Only `docs/tools/eotg_lint.py` was run here:
  - the main mod: 0 new findings against the baseline;
  - the sub-mod as its own root: 16 L014 "defined but never referenced" on engine-convention keys
    (culture/pillar/parameter loc, `TRAIT_FLAG_DESC_`). The lint's convention table doesn't cover those.
- needs-loc: none missing. eotg-localizer should review:
  - the 12 game-rule keys;
  - the sub-mod loc (test-only wording).

  Note: `setting_eotg_race_crossbreeding_forbidden_desc` promises a block that is inert until stubs 2 and 3 are
  completed.
- needs-lore:
  - **Canon hybrids** (feasibility §6, spec D1). The default `off` implements "canon exceptions only"; confirm it,
    or switch the default to `as_own_race`.
  - Do half-races get heritage groups and cultures of their own?
  - The default race (spec D5): presumably human.
- needs-human:
  - **Owner decisions** (spec §11):
    - D2: half-race fertility under `forbidden`;
    - D3: the fertility default, and whether races carry fertility or lifespan modifiers;
    - D4: a race resource for future events (invariant 5);
    - D6: race in the ruler designer;
    - D7: the order of pairings that share a parent race.
  - **Local session:**
    - complete stubs 1–3 in `eotg_race_vanilla_overrides_triggers.txt`, following the steps in its header and
      pitfalls §16;
    - wire `eotg_race_crossbreeding_ai_marriage_modifier` into vanilla's marriage interaction;
    - or hide `forbidden` and `discouraged` until both are done.
  - **In game** (sub-mod README): S0–S1, T1–T4, C1–C2, G1, H1–H3, B1–B5. Run U1 first: if parameter
    substitution in names fails, the registry dispatch has to be rewritten as explicit per-op lists. That is
    mechanical, but it touches both registry files.
- taskboard: (orchestrator to copy; not edited here)
  - **New item:** "Race framework v1: in-game proofs T1–T4 and the U-list (spec §12) on the races test sub-mod".
    Owner human; blocked by nothing (the sub-mod runs on any map).
  - **New item:** "Complete the race vanilla-override stubs 1–3 and wire the discouraged weight". Owner: local
    session (eotg-scripter + eotg-vanilla-scout).
  - **Owner decisions D1–D7.** D1 and D3 restate feasibility §9 decisions 1 and 3; D4 restates decision 4.
  - **Heritage groups for the real cultures** stay blocked by B-CULTURES. When cultures land, each race heritage
    gets the two parameters (spec §4.3 step 4). This may unblock CB-17 and CB-48 (feasibility §7).
  - **Proposed later, not built:**
    - a divergence `is_shown` limit on race heritages (spec §6);
    - an `on_culture_created` check that new cultures keep their group (feasibility §11);
    - race events, after D4.
