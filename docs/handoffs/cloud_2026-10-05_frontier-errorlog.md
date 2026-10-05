### HANDOFF (cloud session; Frontier error.log notes from the owner's first launch, not run in game)
- **branch:** `claude/frontier-errorlog-cloud`, from `origin/v2-space-map` @ `a06544f`. Frontier files and their docs only. Item (c) is a tools fix; it is on `claude/tools-round7-cloud`.
- **validation (sandbox):**
  - eotg_lint: 0 findings, 0 new.
  - check_all: 11 pass, 1 fail, 7 skipped. The fail is the unit tests: main's 2 known L013 tests (`test_b_british`, `test_b_clean_and_exceptions`), which round 7 fixes.
  - All 8 Frontier script files parse.
  - Every Frontier file has exactly **one** BOM, counted byte by byte (the edits went through round 7's `textio`).
  - Every Frontier event has at least one option with no trigger.
  - `spec_conformance.md` is regenerated for the spec edits. It conflicts with round 7's copy only as a generated file: regenerate after merging both.

| Item | Done | How | Where |
|---|---|---|---|
| (a) debug vars ×4 | done (read) | `eotg_frontier_debug_floor_dev`, `_floor_control`, `_dev`, `_control` are now also read **in script**: the readout compares them to pick the toast, "Floors met." or "Waiting on a floor." (new key `eotg_frontier_debug_readout_toast_waiting`). It is a real use and needs no new engine feature. I did not use `MakeScope.ScriptValue` in loc, which would remove the variables but can't be verified here | common/scripted_effects/eotg_frontier_effects.txt:850; L:151 |
| (a) `eotg_frontier_former_type` | done (dropped) | Nothing read it, and the spec had no reader for it. The traces are `attempts` (the head start) and `dev_granted` | common/scripted_effects/eotg_frontier_effects.txt:790; spec §2.4 (struck through, "superseded"), §6.6 |
| (a) `eotg_frontier_history` | done (dropped) | The spec said "read by nothing; a hook for future systems". A future system listens to `eotg_frontier_on_settled` instead | common/scripted_effects/eotg_frontier_effects.txt:739; spec §2.4, §6.5 |
| (b) .002 | done | **"Push through" (b) is now the ungated fallback.** Its effects and tooltip sit in `if = { limit = { eotg_frontier_is_frontier = yes } }`. **Design change to confirm:** the *Without a Founder* variant now offers "Push through" too. "The moment has passed" is kept | E:315; spec §9 .002 row; test plan §4.1 |
| (b) .004 | done | **"The work is its own reward" (c) is now ungated.** `eotg_frontier_complete_effect` already guards itself; the tooltip moved inside a guard. Nothing else changes, because (c) was already offered whenever the Region was a Frontier | E:613 |
| (c) `eotg_frontier_active` | done (exempt, tools) | It is the global variable list of active Frontiers, not loc. px_event_report's whitelist didn't read `add_to_global_variable_list` or `variable = x` | `claude/tools-round7-cloud`, `px_event_report.py` |

- **Other options considered for (b):**
  - Ungating "The moment has passed" would show that text while the moment is still live, and would offer a free way out of every complication.
  - A new neutral .002 option would need new loc and a balance decision.

  Say if you would rather keep "Push through" out of the founder variant. The alternative is a new ungated "Let it run its course" option (strain +1 while still a Frontier).
