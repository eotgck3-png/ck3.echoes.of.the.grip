### HANDOFF (cloud session; validated in the sandbox, not on Windows or against game files)
- **branch:** `claude/lint-rules-round3-cloud` (from `origin/v2-space-map` @ `43057db`)
- **status:** done (FIX 2, 3, 4 and 5, plus the new rules L011 and L012)
- **summary:**
  - **FIX 2, L007:** narrowed to options whose effects are **only deferred**: `trigger_event`, `create_story`, `start_scheme`, or containers and scripted effects holding only those. Scope saves may accompany them. Hidden-resource moves (risk, variables, flags, voice) are never flagged.
    - On the tree at `2e6cef2` it reports the init.018.e bug (`trigger_event = { … days = 1 }` only), plus end.020.d, init.011.d, tier1.014.a and tier3.016.a. All five are fixed in the current tree.
  - **FIX 3, L006:** only `is_valid` and `is_valid_showing_failures_only` are checked now; `is_shown` is ignored.
  - **FIX 4, suppression:** `# eotg_lint: allow L007[,L005] <reason>` works on the finding's line or the line above, in `.txt` and `.yml` files. If the reason or the rule id is missing, or the id is unknown, that becomes an L000 finding and suppresses nothing.
  - **FIX 5, check_all.py:**
    - `--root CHECKOUT` lints and QAs another checkout with this copy's tools: the linter gets `--root`, the QA scripts get the root, and `px_vocab_check` gets `EOTG_MOD_ROOT`. px_lsp uses the target's own copy, Tiger runs with cwd = the target, and port `--check` uses the target's v1 sources and staging, skipping if absent.
    - The Tiger log goes to `$EOTG_LOG_DIR`, else the system temp dir. It is never written inside the target or tool repo; if the env var points inside one, it falls back to temp with a note. The path is printed.
  - **L011 (new):** in `eotg_*.yml`, a value with exactly one named character scope and they/them/their/themself/theirs, and no gendered loc function, is a WARNING. Keys go in the allowlist `docs/tools/eotg_lint_pronoun_allowlist.txt`.
  - **L012 (new):** the cybernetics never-names are ERRORs and the register words WARNINGs (they list the key), all as data in `docs/tools/eotg_lint_register.json`. The data comes from `cybernetics_v2.md` §5 items 2–3 and the interactions and realm lore DoD greps. It is checked only on `eotg_aug_*`, `eotg_fracture*`, `eotg_mod_aug*`, `eotg_decision_aug*` and `eotg_opinion_aug*` values.
  - `eotg_lint.md` documents all of the above, including the L011 and L012 false positives.
- **baseline per rule (current tree):**

  | Rule | Count |
  |---|---|
  | L000 | 0 |
  | L001 | 0 |
  | L002 | 0 |
  | L003 | 0 |
  | L004 | 0 |
  | L005 | 0 |
  | L006 | **0** (was 4, all `is_shown`) |
  | L007 | **0** (was 24, all hidden-resource moves) |
  | L008 | 0 |
  | L009 | 0 |
  | L010 | 0 |
  | L011 | **0** (3 hits, all plural "they", allowlisted with reasons: fracture.002.desc_killed, init.020.a, fracture.006.desc_discontent) |
  | L012 | **14 WARNING, 0 ERROR**: "warrant" ×6 (fracture.006 *The Warrant*), "program" ×4 (Iron Retinue / init.019.b), "encourage" ×2 (init.001.desc, tier2.020.b), "answers" ×2 (tier2.004.desc, heir.007.desc_dead). These are human triage items. |

  **Total: 14, all in the baseline.**
- **files:**
  - `docs/tools/eotg_lint.py`, `eotg_lint.md`, `eotg_lint_baseline.json`
  - `eotg_lint_register.json` (new), `eotg_lint_pronoun_allowlist.txt` (new)
  - `check_all.py`
  - `tests/test_eotg_lint.py`, `tests/test_check_all.py`
  - this handoff
- **validation:**
  - `python -m unittest discover -s docs/tools/tests` → **87 OK**, on both an LF checkout and a `core.autocrlf=true` checkout.
  - `check_all.py` → 10 pass, 0 fail, 7 skipped (local-only tools and the interactive QA scripts).
  - `check_all.py --root "OLD PROJECT VERSION"` lints that checkout (1,493 findings, as expected) and skips its port check.
- **unverified-vanilla:** that `trigger_event` with `days` prints no tooltip line (L007).
- **needs-human:** triage the 14 L012 warnings. Rewording or adding `# eotg_lint: allow L012 <reason>` is the localizer's call; the linter does not edit loc.
- **taskboard (proposed):** "localizer: triage eotg_lint L012 register warnings (14)".
