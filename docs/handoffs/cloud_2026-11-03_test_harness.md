# In-game test harness (cloud, 2026-11-03)

Brief (Part E): turn the backlog of in-game checks into one-click debug decisions, with automatic PASS/FAIL where
script can read the result and LOOK lines for visual checks, plus a README cross-referenced to the session plan.

### HANDOFF (cloud session, unvalidated)
- branch: claude/test-harness-cloud (from v2-space-map at aeb1f10)
- status: done
- summary:
  - **23 debug-only decisions,** each named "(Test) <ID>: …", with **24 hidden assertion events**
    (namespace `eotg_test`). They cover every area the brief named:
    - **cybernetics:** the tier ladder with the prowess stacking check, the Neurofractured and Seamless end
      states, the Cascade threshold, the track AI values (LOOK), and wound rank 3 and the repair hook;
    - **Frontier:** start (military, settlement, religious), forced completion with the E-12 / FX-2 / G-2 LOOKs,
      the progress and strain clamps, save/reload persistence (a two-step test), exploration;
    - **governments:** the Cartel schedule start and walk-off, the elective candidate rule (dynasty), the Cartel
      resource core;
    - **alerts:** breaking strain, founderless, establish-ready, calibration lapsed;
    - **game rules:** all five rules logged, and a FAIL for any rule that reads no known setting;
    - **investigation items:** SI V8, T1, F3 and F8 as setups. The rest are in the README's "manual" table, with
      the reason each stays manual.
  - **Setup uses only the systems' own effects:**
    - `eotg_aug_initiate_effect`, `eotg_aug_set_integration_effect`;
    - `eotg_frontier_start_effect`, `eotg_frontier_tick_effect`, `eotg_frontier_add_progress_effect`,
      `eotg_frontier_add_strain_effect`, `eotg_frontier_mark_unknown_effect`;
    - `eotg_cartel_change_dread_effect`, `eotg_cartel_start_schedule_effect`, `eotg_cartel_walk_off_effect`.
  - **Assertions read only the systems' own triggers and values.**
  - **Logging.** Every line is `EOTG_TEST <id> START|PASS|FAIL|LOOK|INFO|SKIP|DONE: …` via `debug_log`, with
    plain-text strings. A failed precondition logs SKIP and changes nothing.
  - **Kept out of normal play:**
    - every decision is `debug_only = yes`, `should_create_alert = { always = no }`,
      `ai_potential = { always = no }`, with the gating copied from the shipped debug decisions;
    - every event is `hidden = yes` and fired only by a harness decision (invariant 4).
  - **Everything is generated** by `docs/tools/gen_test_harness.py`. The headers say "never hand-edit".
  - **`docs/qa/TEST_HARNESS.md`** covers enabling debug mode, the playsets, the tag table, the grep commands,
    each test with its plan ids (IGSP, SI, V-C, V-SU, INT1), the suggested order, the manual-only checks, and
    how to extend it.
  - **Not covered:** the PMC, Corporation and Trade Oligarchy G2 resources. They live on the unmerged branch
    `claude/governments-g2-three-cloud`; add them when it merges.
- files (moved 2026-11-03 at local validation into the test sub-mod `docs/test_submods/test_harness/`,
  "EotG Test: In-Game Test Harness"; test content never ships):
  - `docs/test_submods/test_harness/descriptor.mod`, `README.md`
  - `docs/test_submods/test_harness/common/decisions/eotg_test_harness_decisions.txt`
  - `docs/test_submods/test_harness/events/eotg_test_harness.txt`
  - `docs/test_submods/test_harness/localization/english/eotg_test_harness_l_english.yml` (93 keys; one BOM each, checked)
  - `docs/tools/gen_test_harness.py`
  - `docs/qa/TEST_HARNESS.md`
  - this handoff
- unverified-vanilla:
  - `common/decisions/eotg_test_harness_decisions.txt:47` — `value = prowess` read as a value (as `dread` is in
    `eotg_cartel_values.txt`). If it is rejected, the CY1 prowess checks fail loudly; the tier checks still
    stand.
  - `common/decisions/eotg_test_harness_decisions.txt:761` — `random_neighboring_top_liege_realm_owner`, the
    random form of the `any_` iterator v2 already uses. If it is unknown, GV1 logs SKIP.
  - `events/eotg_test_harness.txt:11` — `debug_log` writes its literal string to `logs/debug.log` (corrected
    from `game.log` at local validation).
  - Scopes saved before `trigger_event = { days = N }` reach the delayed event. The mod's own chains rely on it
    (`eotg_aug_heir.006`), so this is low risk.
- needs-local-validation: Tiger + PX on `common/decisions/eotg_test_harness_decisions.txt`,
  `events/eotg_test_harness.txt` and `localization/english/eotg_test_harness_l_english.yml`. Expect no new
  benign families. `eotg_lint` gave 0 new findings, and brace balance was checked.
  - First in-game smoke test: GR1 (no setup), then CY1. Every `START` should be followed by its `DONE`.
- needs-loc: localizer review of the 93 test-decision keys (testing text, low priority).
- needs-lore: none (debug text only).
- needs-human:
  - Run the harness alongside `IN_GAME_SESSION_PLAN.md` and send back every `EOTG_TEST … FAIL` line with the
    LOOK observations.
  - ~~Owner choice: main mod or sub-mod~~ Decided: a test sub-mod (test content never ships). Done at local
    validation, 2026-11-03.
- taskboard: (orchestrator to copy)
  - New item: "Run the test harness (`docs/qa/TEST_HARNESS.md`) with the session plan; harness smoke test GR1 +
    CY1 first".
  - New item: "Add PMC/Corporation/Trade Oligarchy G2 tests to `gen_test_harness.py` when
    `claude/governments-g2-three-cloud` merges".
