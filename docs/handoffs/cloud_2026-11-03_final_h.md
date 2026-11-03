# Handoff: final queue H (cloud, 2026-11-03)

Branch `claude/final-h-cloud`: cut from origin/claude/void-corruption-v2-cloud (e02389d), merged origin/claude/mechanics-sim-cloud (f602a72); origin/v2-space-map (4a6191e) was already contained. No game script or loc in the main mod was changed.

## H1: test-harness cases for the G2 governments and the Void

### HANDOFF (cloud session, unvalidated)
- branch: `claude/final-h-cloud`
- status: done
- summary: 16 new harness decisions and 25 hidden events in `docs/tools/gen_test_harness.py` (39 tests, 49 events in all), regenerated into `docs/test_submods/test_harness/`; README test list updated with spec ids.
  - G2: GP1/GC1/GT1 (writer → story counter, modifier re-applied, clamp; V-P2/3, V-CO2/3, V-TO2/3).
  - GP2: battle feed values +2/−3 (V-P6; the hook itself is a LOOK).
  - GC2a/GC2b → GC2c: Court the Board bracket (V-CO8 and the erosion fix, including the already-eroded guard path).
  - GT2a → GT2b: Corner the Market bracket (V-TO7, including the once-a-year guard on a pre-marked Prince).
  - GE1/GE2: election band edges as LOOK (V-CO13, V-TO13).
  - Void: VD1 exposure bands (V-V3), VD2 the Hollowing through the real yearly pulse with the cooldown set by the on_action (V-V8, V-V17), VD3 depth bands and the +4 drift (V-V9–V-V12), VD4 the Voidwalker courtier, −6 accrual and the Ward decision (V-V13), VD5 the Insight guard (V-V16).
  - Lessons followed: nothing kills or deposes (VD2 warns that 0030.c steps down; the player chooses), every unmet setup logs SKIP, each PASS reads something downstream of the setup (story counter, band modifiers, accrual value, decision availability) or is a LOOK, baselines read first with exact deltas and restored, every `eotg_test_*` variable cleared in the final step.
- files: `docs/tools/gen_test_harness.py`; `docs/test_submods/test_harness/**` (regenerated, byte-stable on a second run); `docs/qa/TEST_HARNESS.md`; this handoff.
- unverified-vanilla:
  - `gen_test_harness.py` GC2a/GT2a: `is_decision_on_cooldown = <decision>` as a character trigger.
  - VD3: `has_opinion_modifier = { modifier target }`.
  - VD5 and the existing CY1: skills read as values (`value = diplomacy add = martial …`).
  - VD4: `can_execute_decision` for a decision with a gold cost (AL4 uses it already).
  - All tests: `save_scope_value_as` with a `{ value subtract }` block passed on as `AMOUNT = scope:x` into the writers (their `save_scope_value_as` / `change_variable` take a value).
- needs-local-validation: Tiger and PX over `docs/test_submods/test_harness/` (with the main mod), then the session: GP1, GP2, GE1/GE2 as Raoul/Hoël/Bertrand; GC2 as Konan (reload between a and b); GT2 needs two Trade Oligarchy vassals (V-TO9); VD1, VD4, VD5 on any ruler; VD2 → answer 0030 → VD3 on a throwaway save.
- needs-loc: none (harness loc is generated).
- needs-lore: none.
- needs-human: none.
- taskboard: none.

## H2: the Void in the simulation

Not started.
