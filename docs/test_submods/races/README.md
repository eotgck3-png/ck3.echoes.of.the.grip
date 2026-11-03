# EotG Test: Race Framework (sub-mod)

**Test only, never shipped.** Proves the race mechanics framework (`docs/specs/races_framework_v1.md`) with two
test races, `eotg_race_test_a` and `eotg_race_test_b`, plus one test half-race, `eotg_race_test_half_ab`. It fills
the main mod's race registry by redefining its keys. Without this sub-mod, the framework is switched off and does
nothing.

Nothing here has been run. The cloud session that wrote it had no game, no Tiger and no PX. Every engine fact it
could not check is marked `UNVERIFIED-VANILLA` in the files, and listed in the spec §12.

## What it adds

| File | What |
|---|---|
| `common/traits/eotg_test_race_traits.txt` | The three test race traits, written to the main mod's template |
| `common/culture/pillars/eotg_test_race_pillars.txt` | Two test heritages carrying `eotg_heritage_group_test_a` / `_b` and `eotg_heritage_grouped`, and one test language |
| `common/culture/cultures/eotg_test_race_cultures.txt` | `eotg_test_culture_a` and `eotg_test_culture_b`. No province or character uses them |
| `common/scripted_effects/zz_eotg_test_race_registry_effects.txt`, `common/scripted_triggers/zz_eotg_test_race_registry_triggers.txt` | The registry: switches the framework on; test_a is the default race; test_half_ab is born of test_a × test_b |
| `common/decisions/eotg_test_race_decisions.txt`, `common/scripted_effects/eotg_test_race_debug_effects.txt`, `common/scripted_character_templates/eotg_test_race_templates.txt` | The debug decision **(Debug) Run the Race Framework Test** |
| `common/on_action/eotg_test_race_on_actions.txt` | Logs a real test birth (B5), and the T2 probe |
| `localization/english/eotg_test_races_l_english.yml` | Loc for all of the above (UTF-8 BOM) |

## Install

Same pattern as `docs/test_submods/frontier_vanilla`: make a directory junction from the game's mod folder to
this folder (cmd), and a `mod/eotg_test_races.mod` holding this descriptor plus `path="<that folder>"`:

```
mklink /J "<mod folder>\eotg_test_races" "<repo>\docs\test_submods\races"
```

**Playset:** Echoes of the Grip, then this sub-mod (it must load after the main mod: its registry keys override
the main mod's). Any map the main mod loads on will do. The British Isles test sub-mod also works under it.
**Launch with `-debug_mode`**, because the decision is `debug_only`. Start a **new game**: the game-start pass and
the T2 probe run only on a new game.

**Reading results:** every line this sub-mod writes starts with `EOTG_RACE`. They go to
`Documents/Paradox Interactive/Crusader Kings III/logs/game.log`:

```bash
grep EOTG_RACE game.log
```

If a line shows raw `[...]` text instead of a name or a number, then `debug_log` doesn't evaluate data functions
(UNVERIFIED-VANILLA). The yes/no lines still work. Hover the characters in debug mode to read their variables.

## Before anything: load checks

- **S0.** `error.log` has no `eotg_race` or `eotg_test` errors. In particular, look for:
  - `Unknown effect eotg_race_op_`, or a literal `$OP$`, `$RACE$`, `$A$` or `$TARGET$`. Any of these means
    parameter substitution inside identifiers fails (spec §12, U1). Stop and report: the registry design needs it.
  - errors on `culture:eotg_test_culture_a`. This means a culture that nothing uses doesn't exist at game start
    (U13). Fallback: set one county to the test culture in history, or by console, then rerun.
  - unknown `ethos_stoic`, `martial_custom_equal`, `head_determination_domain`, `name_list_roman`, `western_*_gfx`
    or `caucasian_northern`. These vanilla keys were copied from v1 unchecked. Replace them with keys from a
    vanilla culture.
- **S1.** `logs/database_conflicts.log` shows `Overriding entry` for each of the 7 registry keys:
  - `eotg_race_for_each_race_effect`, `eotg_race_default_race_effect`, `eotg_race_for_each_pairing_effect` and
    `eotg_race_roll_effect`;
  - `eotg_race_framework_active`, `eotg_race_same_as` and `eotg_race_cultures_in_different_groups`.

  Each must name a `zz_eotg_test_race_*` file.

## In-game proofs T1–T4 (feasibility report §8)

| ID | What | How | Pass |
|---|---|---|---|
| **T1** | A custom `parameters` entry on a heritage pillar is readable with `has_cultural_parameter` | Run the decision | Log: `T1 PASS: culture A reads eotg_heritage_group_test_a`, and no `T1 FAIL` line. Also `H3 PASS` ×2. If it fails, switch `eotg_is_heritage_group` and `eotg_race_culture_is_grouped` to OR lists of `has_cultural_pillar` (spec §5.4) |
| **T2** | `on_character_created` fires for history and ruler-designer characters | New game, reach the map; for the designer half, start with a ruler-designer character | Log, at game start: `T2: on_character_created fired before on_game_start` or `... did NOT fire ...`. After the lobby: `T2: player ... passed through` or `... did NOT pass through`. **Either answer is fine**, because the game-start pass covers both. Record the answer in the spec §5.3 |
| **T3** | AI culture hybridization respects the overridden scripted rule | **Only after a local session completes stub 1** in `common/scripted_triggers/eotg_race_vanilla_overrides_triggers.txt`. Put test culture A and test culture B side by side (two counties by console, each with a ruler of that culture), then watch the AI for a few decades, or try the hybridize interaction as the player | The player's UI refuses A+B with the tooltip of our clause, and no A+B hybrid ever appears. A hybrid of A and an ungrouped vanilla culture is still allowed |
| **T4** | A race trait added in `on_birth_child` shows on the first portrait; order against the engine's genetic roll | **Needs a trait portrait modifier.** None ships (no gfx). Locally, copy any vanilla trait portrait modifier, key it on `eotg_race_test_b`, and make it obvious (e.g. a large morph). Then let B5's pregnancy come to term | Open the newborn the day it's born: if the B-race modifier shows on a test_b child at once, race looks apply from birth. If it shows only after a reload or later, record that; the fix is on the art side (spec §10) |

## Framework checks

Run **(Debug) Run the Race Framework Test** from the decisions panel. It adds about 32 characters to your court.

**Creation hook (C1–C2)**

- **C1.** Log: `spawned adult ... (eotg_test_race_man_a)` followed by `race = test_a`. Same for `woman_a`, and
  `woman_b` with `race = test_b`. This is the culture route through `on_character_created`, and it needs T1. If
  you see `NO RACE: on_character_created did not assign one`, the creation hook isn't firing for
  `create_character`, or its root isn't the new character (U6).
- **C2.** `man_none` was spawned in **your** culture, which is ungrouped. It must show `race = test_a`, because the
  documented fallback gives the default race. Then it's stripped of its race for B3.
- **G1.** At game start, every existing character got a race. Hover a few: all should have Test Race A, the
  default, because no vanilla culture is grouped. The after-lobby probe logs `G1: player has a race after the lobby`.
  A `G1 FAIL` line there can mean only that the probe ran before the framework's pass. Re-check by hovering.

**Helpers (H1–H3)**

- **H1.** `same_as(man_a, woman_a) = yes` and `same_as(man_a, woman_b) = no`, both PASS.
- **H2.** `crossbreeding_allows(man_a, woman_b)`: `yes` under rule *Free* and *Discouraged*, `no` under *Forbidden*.
  This checks only our trigger. Nothing calls it until the stubs are completed.
- **H3.** Culture A and culture B may not hybridize; culture A and your ungrouped culture may.

**Birth roll (B1–B5).** Run the decision once under each value of the **Half-Races** game rule. The expected values
are under each scenario label in the log.

| Scenario | Rule *Off* (default) | Rule *A Race of Their Own* |
|---|---|---|
| **B1** woman_b × man_a (8 children) | every child `share test_a = 0.500`, `share test_b = 0.500`; roughly half `race = test_a`, half `race = test_b`. Never `test_half_ab` | every child `race = test_half_ab`, `pure (implicit profile)` |
| **B2** woman_a × a B1 child (8) | `test_a = 0.750`, `test_b = 0.250`; about 6 in 8 roll test_a | `test_a = 0.500`, `test_half_ab = 0.500` |
| **B3** woman_b × man_none (no race, so counts as test_a) (8) | `test_a = 0.500`, `test_b = 0.500` | every child `race = test_half_ab` |
| **B4** woman_a × man_a (4) | `pure (implicit profile)`, `race = test_a`, no share lines | same |
| **B5** real pregnancy, woman_b by man_a | about 9 months later: `real birth: ...` with the B1 values | B1 values for this rule |

- **Roll weighting.** Counts of 8 are small. For a better check, run the decision 3–4 times under rule *Off*, and
  count B2's test_a rolls: about 75% means the `random_list` weights work (U2/U3). If **every** child in B1 rolls
  the same race, the `local_var` weights aren't being read inside `random_list` (U3).
- **Shares sum to 1.** In every child line, the shares add up to 1.000 (±0.001).
- **B5 hook order.** If the real-birth log says `no race yet`, the sub-mod's report hook ran before the
  framework's. Hover the newborn: it must have a race trait and, under rule *Off*, `eotg_race_share_test_a` and
  `_test_b` at 0.5.
- **Crossbreeding rule.** Under *Forbidden*, B1–B3 still roll, because the simulation calls the birth effect
  directly and the stubs are inert. Only H2 changes.

## Not tested here

- The hybrid block (T3) and the marriage/fertility block (*Forbidden*) stay inert until a local session completes
  the stubs in `common/scripted_triggers/eotg_race_vanilla_overrides_triggers.txt`.
- The *Discouraged* AI marriage weight isn't wired yet (`common/scripted_modifiers/eotg_race_modifiers.txt`).
- Old saves: the framework never needs a migration. A character without shares counts as 100% of its trait, and a
  character without a trait counts as the default race at its children's birth. But characters in a save started
  before the sub-mod get a race only when they're next created or born, because the game-start pass runs only on
  a new game.
