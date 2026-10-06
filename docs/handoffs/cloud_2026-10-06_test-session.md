# Handoff: consolidated in-game test plan, plus tool and housekeeping fixes

### HANDOFF (cloud session, unvalidated)
- **branch:** `claude/test-session-cloud`, from `origin/v2-space-map` @ `e481957` (Phase 3a merged). **Do NOT merge**: the local orchestrator reviews and merges.
- **status:** done.
- **summary:**
  - **A.** `docs/qa/IN_GAME_SESSION_PLAN.md`: every pending in-game check in three sittings (engine, then cybernetics, then Frontier P1 → P2 → P3a). It has console lines, expected results, tick boxes (140), save points, time notes, a "what to send back" section and a dedupe appendix. Each check cites its source and id. Unclaimed Regions has a marked placeholder (§U). `HOW_TO_TEST_IN_GAME.md` links to the plan.
  - **B.** Five small fixes (below).
- **commits:**
  - `2c17da0` B1–B5;
  - `fe85b31` the plan;
  - this handoff (the commit after `fe85b31`).
- **validation (static):**
  - eotg_lint: 0 findings;
  - unit tests: all OK, 222 (218 before, plus 4 new);
  - check_all: 14 pass, 0 fail, 7 skipped (Tiger, PX and the game are local-only).

## B. The fixes, and the choices made
1. **`docs/tools/tests/test_eotg_lint.py`:18.** The raw U+FEFF literal is now the escape `"\ufeff"`, so textio can rewrite the file. The tests are unchanged and pass. The file was rewritten through textio, which proves the point.
2. **`docs/tools/gen_seller_names.py`.** A new `same_content()` compares bytes with CRLF normalised to LF. `--check` and the "unchanged, leave it alone" skip both use it, so a `core.autocrlf=true` checkout is no longer STALE, while a real content change still is. Tests:
   - `test_check_ignores_crlf_line_endings` turns the generated files to CRLF and expects "current"; it then adds a name and expects STALE;
   - `test_same_content`.
3. **`docs/tools/px_event_report.py`: option chosen, exclude `docs/`.** Loc coverage now skips entries under `docs/`, as well as the frozen v1 tree (`OUTSIDE_MOD`, matched on the first path component relative to the checkout).
   - **Why not add the keys instead:** both missing keys live in sub-mods that never ship. Those load as separate mods with their own loc. The observer builds its keys at runtime (`debug_log = eotg_obs_$KEY$`), so PX can't resolve them. Adding them to the test-map or observer loc would be guessing which two keys PX meant; I couldn't run PX here. And it would leave the report open to the next docs/ sub-mod.
   - The report already skipped `OLD PROJECT VERSION` for the same reason.
   - Tests: `test_docs_and_v1_tree_are_outside_the_mod`, which covers relative, absolute and Windows-backslash paths, and checks that `docsish/` is *not* excluded; and `test_outside_mod`.
4. **`events/eotg_augmentation_fracture.txt`, fracture.004 option `e`.** Its trigger is now `has_trait = callous` plus `OR = { exists = scope:eotg_victim_dead  exists = scope:eotg_victim }`: the same `exists` gate as option c, widened to either victim.
   - "Fill the empty places" fits the dead and the wounded alike. The brief said "nobody was killed or wounded".
   - In-game check: plan C5-8.
5. **`common/defines/eotg_space_map_defines.txt`.** One BOM was added through textio. The script asserted that the new bytes equal `BOM + old bytes`, so nothing else changed (987 → 990 bytes).

## Not verified (no game here)
- **The plan's console lines** are copied from the source plans and HTT. A few are new, and none of these was run:
  - the character-switch command (I wrote "`play <id>` may work; otherwise `help`");
  - giving yourself a second county with `effect title:c_arborea = { change_title_holder = { holder = root } }` (marked unverified in the plan, with a fallback);
  - E-11's repeated `increase_wounds_effect = { REASON = attacked }` from the console.
- **Character ids on the test map** come from `docs/test_map/README.md` (900001 Aurelian, 900007 Melitta, 900008 Nikephoros). Orsocorre I's holdings in 1066 aren't known here, so the plan covers the one-county case.
- **B3:** I couldn't run PX, so I couldn't confirm which two keys it reported. Any eotg_ key under `docs/` is now excluded.

- **needs-local-validation:** Tiger and PX on `events/eotg_augmentation_fracture.txt` and `common/defines/eotg_space_map_defines.txt` (PX's missing-bom finding should be gone). Run `px_event_report` once to confirm the two `docs/` keys are no longer reported.
- **needs-loc:** none.
- **needs-lore:** none.
- **needs-human:** run the plan.
- **taskboard:**
  - **CB-19** (the defines BOM) is done by B5; move it to Done.
  - **CB-01, CB-02, CB-03 and CB-21** are marked blocked on B-DESCRIPTOR / B-TEMPMAP, but they run on the vanilla map now. Consider moving them to waiting-human and pointing them to the plan (sitting 2).
  - Point **CB-31, CB-34, CB-35 and CB-37 to CB-43** to `docs/qa/IN_GAME_SESSION_PLAN.md`.
  - When Unclaimed Regions merges, fill the plan's §U from that branch's handoff (V-U1 to V-U15), and move Frontier play to Corsica (Sardinia will be released).
