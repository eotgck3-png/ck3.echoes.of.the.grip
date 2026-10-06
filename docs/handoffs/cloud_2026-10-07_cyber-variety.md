# Handoff: cybernetics writing variety pass (event-writing review, tier 2)

### HANDOFF (cloud session, unvalidated)
- **branch:** `claude/cyber-variety-cloud`, from `origin/v2-space-map` @ `d6805f6`. **Do NOT merge:** the local orchestrator reviews and merges.
- **status:** done.
- **summary:** a text-only variety pass on `localization/english/eotg_augmentation_l_english.yml`. 190 keys were reworded; no keys were added or removed. The 20 events rewritten in `b3371a0` and every `.txt` file are untouched.
  - **Stock phrases** are cut to a third or less: "No one" 35 → 7, "the hardware" 36 → 1, "the work" 19 → 0, "the body" 20 → 3, quiet 32 → 9, "half a second" 11 → 4.
  - **Openings:** "X has…" 29 → 5, "The implant…" 13 → 1, "The hardware…" 8 → 0. The 5 left are all in excluded events.
  - **Repeated options** now have their own voice, matched to their effects and trait gates. The provider menu stays verbatim, as the exception allows.
  - **Canon lines are kept on purpose**, with the reasons in the report.
- **commits:**
  - `cc9d61e` the yml;
  - `a032532` the report, `docs/qa/variety_pass_2026-10-07.md`;
  - this handoff (the commit after `a032532`).
- **validation (static):**
  - eotg_lint: 0 findings, 0 new;
  - unit tests: OK (222);
  - check_all: 14 pass, 0 fail, 7 skipped (Tiger, PX and the game are local-only);
  - the self-check script on all 190 changed lines found 0 banned words, 0 `[scope:` forms, 0 quotes, 0 opener mismatches, 0 descs over 80 words and 0 new scopes;
  - all 46 they/them/their hits were read by hand, and every one has a plural referent.

  The script's output is in the report.
- **files:**
  - `localization/english/eotg_augmentation_l_english.yml`
  - `docs/qa/variety_pass_2026-10-07.md`
  - this file
- **unverified-vanilla:** none. No script was touched.
- **What I couldn't verify** (no game here):
  - how the new lines render: wrapping, and the five-option windows. The new options are 4–9 words, so act.002, act.004 and nr.003 should be re-checked against session plan C10-5;
  - that every changed line reads true *in play*. I checked each option against its block in `events/eotg_augmentation_*.txt` and kept each desc's facts, but saw nothing on screen;
  - the custom-loc seller names inside changed lines (init.010.desc, tier1.018.desc, patron.*) are unchanged placeholders, but weren't rendered.
- **needs-local-validation:**
  - Tiger + PX on `localization/english/eotg_augmentation_l_english.yml`: the language server's loc checks, and `px_event_report` loc coverage, which should be unchanged since no keys changed;
  - after a play session, `grep -A2 "Trigger Localization" error.log`.
- **needs-loc:** none (this is loc).
- **needs-lore:** a read of the changed lines. These are the ones with new wording, not just phrase swaps:
  - the options: tier1.012.b/.e, tier1.016.b, tier1.018.b, tier2.012.c, tier2.017.e, tier3.012.b, tier3.017.d, tier3.020.b, fracture.013.c, fracture.018.d, fracture.021.e, fracture.025.b, fracture.027.d, patron.002.b/.003.b/.004.b/.009.c, end.010.a, end.020.e, end.031.d, end.042.a, proc.004.a, retinue.003.b, retinue.005.a, countdown.001.c, countdown.005.a, act.001.e;
  - the reworked descs: tier1.012, tier2.019, tier3.004, fracture.023 (both), patron.009, heir.003/.004.
- **needs-human:** none.
- **taskboard:** the event-writing review's tier 2 (stock phrases, openings, repeated options) is done; the report records what is left. Suggested follow-ups, for the owner's call:
  - **the similarity clusters this pass didn't target:** the hardware-grade lines shared by int.002 and realm.001, and "Your law prohibits augmentation…" in act.001 and act.003;
  - **the replacement words that rose slightly:** "casing(s)" 11 → 16 and "tissue" 7 → 11. Watch them in the next pass.
