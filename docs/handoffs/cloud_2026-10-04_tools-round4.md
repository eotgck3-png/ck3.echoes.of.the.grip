### HANDOFF (cloud session; validated in the sandbox, not on Windows or against game files)
- **branch:** `claude/tools-round4-cloud` (from `origin/v2-space-map` @ `33f27a4`)
- **status:** done (FIX 7, L013, L014, `gen_test_recipes.py`, `spec_conformance.py`, check_all wiring)
- **summary:**
  - **FIX 7, port check under `check_all --root`:** `port_religions_1_20.py` now writes the `--src` path relative to the checkout that **contains** `--src`. It finds that checkout by walking up to the folder holding `OLD PROJECT VERSION/` or `.git`. It used to be relative to the tool's own repo.
    - Running `--check` from another checkout now gives byte-identical output.
    - Its stdout prints the absolute source path.
    - The live-`common/` guard covers both repos.
    - **New tests:** one copies the tool into checkout A, puts the sources and staging in checkout B, and asserts "current" through a subprocess. A second runs `check_all --root B` and expects PASS. Both fail on the old tool and pass on the new one.
  - **L013, loc house style (WARNING), with data in `docs/tools/eotg_lint_style.json`.** The message starts with the sub-rule id.
    - **L013a:** an em or en dash.
    - **L013b:** British spelling. Whole words, case-insensitive, matched on visible text. It uses the seed list, a few more `-our` words and every `-ise/-isation` form. An `-ise` word is skipped when its base form is in `ise_exceptions` (about 70 words: rise, wise, noise, promise…). Literal `exceptions` (`Tide-Crowned`) are blanked out first.
    - **L013c:** a double space, or leading or trailing whitespace.
    - **L013d:** an appended desc that doesn't start with `\n\n`. "Appended" is read from the structure: a `triggered_desc`'s desc, or a plain `desc = key`, that is a direct child of an event's `desc = { }` block and not its first segment.
      - `first_valid` / `random_valid` alternatives that open the block are not required to start with `\n\n`.
      - A `first_valid` that follows the opener, a nested desc block, or a key used in two roles is **skipped** and listed under `"skipped": {"L013d": [...]}` in `--json`.
  - **L014, unused `eotg_` loc keys (WARNING).** A key containing `eotg_` that nothing references. A reference is any of:
    - a script literal (any key or value in `common/` or `events/`, quoted or not), or a word in a `gfx/**/*.gui`;
    - `$KEY$` or `Localize('KEY')` in loc;
    - an engine naming convention from `docs/tools/eotg_lint_loc_conventions.json`. These start from what L010 already implies (decision, trait including leveled and track keys, modifier, opinion), plus interactions, scheme_types, laws, law_groups, court positions, deathreasons, story_cycles and buildings. Each folder entry has a `verified` flag.
  - **`gen_test_recipes.py` (top priority) writes `docs/qa/generated/console_recipes.md`.** It covers 163 events, grouped under the test plan §4 headings plus Procedures. It has a summary table, a "how to use" header pointing to HOW_TO_TEST_IN_GAME.md, and a "generated, do not edit" banner. Each row gives:
    - **FIRE COLD:** *yes*, *after setup*, or **no**. A **no** lists exactly what is missing:
      - a saved scope not created in the event's own immediate or options (scopes saved by scripted effects called there count as created), with who saves it;
      - a running story the trigger needs, with who creates it;
      - a story variable;
      - a flag, or a state variable in the trigger, that another definition sets, with who sets it.
      - `duel_value` read inside a `duel` doesn't count, because the duel sets it.
    - **SETUP:** console lines in the HOW_TO §2 form.
      - `has_trait` becomes `add_trait` / `remove_trait`.
      - Tier comes from the scripted trigger's own `has_trait_xp` (it expands `eotg_is_aug_tier*` and every scripted trigger), and becomes `effect eotg_aug_initiate_effect = yes` then `effect add_trait_xp = { … value = 0|50|100 }`.
      - Variable thresholds become `effect set_variable`, flags `effect add_character_flag`, gold `effect add_gold`, `stress_level` `effect add_stress`, skills `effect add_<skill>_skill`.
      - Everything else becomes a plain-English note: "must be at war", "needs a vassal who/which: opinion of you < -30", "needs your spymaster who/which: not you", and so on.
      - A second line, *for realistic content*, holds the requirements common to every firing path (the on_action `limit` and `random_list` entry `trigger` chain), e.g. the tier the yearly pulse requires.
    - **FIRE:** `event <id>`. When the script fires it inside a scope switch (`every_knight`, `scope:eotg_nr_liege`…), it becomes `event <id> <character id>` plus who.
    - **FIRED BY:** taken from the shared graph. On_actions show their hook chain (`yearly_playable_pulse → eotg_on_yearly_aug_tier1_check`), and events show the option. Hidden events carry "hidden: runs silently, check its effects".
    - **LIVE ROUTE** (for **no** only): the shortest upstream chain, preferring a decision root, else a pulse. A flag or variable that must exist first is named before the chain.
    - **Options:** `--check` (CRLF-tolerant), `--event <id>`, `--json`.
  - **Shared event graph:** `eotg_lint.fire_sites(mod)` returns `{event: [FireSite]}`. L009 now uses it too; its semantics are unchanged and the baseline is identical. No second parser.
  - **`spec_conformance.py` writes `docs/qa/generated/spec_conformance.md`.**
    - It extracts every backticked `eotg_` id and event id from each `docs/specs/cybernetics_v2*.md`.
    - **Classification:** from the table's Type column, wherever that column sits (Type|Key and Key|Type both work); else the heading; else the id's shape; else where the script defines it; else `unknown`.
    - **Expanded:** `{a,b}` braces and `` `x_low` / `_high` `` suffix shorthand. Shorthand is resolved against the script; unresolved ones are listed and not counted.
    - **Skipped:** prefixes (`eotg_story_aug_`), placeholders (`_X_`), file paths and code blocks.
    - **Status:** present, referenced only, or missing.
    - **Built:** a spec is built if any of its new events exists. New events are the event rows in its "New" section's Key column, excluding "new option on an existing event"; with no New section, every event it names. `*_lore.md` follows its parent spec.
    - **Exempt:** any line with deferred, rejected, superseded or not built.
    - **Also lists** script definitions that no spec names.
    - **Options:** `--check`, `--json`, `--specs`.
  - **Wiring:**
    - `check_all.py` runs `gen_test_recipes --check` and `spec_conformance --check` with `--root`. They FAIL only on a stale file and show their counts in the detail line. They are skipped when the target checkout has no generated file.
    - `docs/tools/qa/README.md` has a new "Generated QA reports" section.
    - `eotg_lint.md` covers L013, L014 and the shared graph.
- **files:**
  - **Modified:**
    - `docs/tools/port_religions_1_20.py`, `eotg_lint.py`, `eotg_lint.md`, `check_all.py`, `qa/README.md`;
    - `tests/test_port_religions.py`, `tests/test_eotg_lint.py`, `tests/test_check_all.py`.
  - **New:**
    - tools and data: `docs/tools/eotg_lint_style.json`, `eotg_lint_loc_conventions.json`, `gen_test_recipes.py`, `spec_conformance.py`;
    - tests: `tests/test_gen_test_recipes.py`, `tests/test_spec_conformance.py`;
    - generated output: `docs/qa/generated/console_recipes.md`, `docs/qa/generated/spec_conformance.md`;
    - this handoff.
  - `eotg_lint_baseline.json` was regenerated and is unchanged.
- **validation:**
  - **Unit tests:** `python -m unittest discover -s docs/tools/tests` gives **120 OK**, both on this LF checkout and on a fresh `git clone -c core.autocrlf=true` of the branch, where every text file is CRLF.
  - **`check_all.py` in the LF repo:** 12 pass, 0 fail, 7 skipped. The skips are px_vocab, px_lsp, px_event_report and Tiger (need a local install) plus the 3 interactive QA scripts.
    ```
    eotg_lint (vs baseline)        PASS  total: 14 finding(s), 0 new (vs baseline)
    unit tests (docs/tools/tests)  PASS  OK
    port_religions_1_20 --check    PASS  port output is current
    gen_test_recipes --check       PASS  console recipes are current: 163 events, 39 fire cold, 63 after setup, 61 need a route
    spec_conformance --check       PASS  spec conformance report is current: 20 spec(s), 14 built, 3 missing id(s) in built specs
    ```
  - **Inside the CRLF clone:** the same, 12 pass, 0 fail, 7 skipped.
  - **`check_all.py --root <CRLF clone>`, run from this checkout:** 12 pass, 0 fail, 7 skipped. The port check passes cross-checkout, which is the FIX 7 acceptance.
- **baseline per rule (current tree):**

  | Rule | Count |
  |---|---|
  | L000 | 0 |
  | L001 | 0 |
  | L002 | 0 |
  | L003 | 0 |
  | L004 | 0 |
  | L005 | 0 |
  | L006 | 0 |
  | L007 | 0 |
  | L008 | 0 |
  | L009 | 0 |
  | L010 | 0 |
  | L011 | 0 (3 allowlisted) |
  | L012 | 14 WARNING, 0 ERROR (unchanged from round 3) |
  | L013 | **0** |
  | L014 | **0** |

  **Total: 14, all in the baseline.**
- **L013 and L014 findings for triage: none.**
  - **L013:** no dashes, British spellings or stray spaces in `eotg_*.yml`. L013d checked 34 appended descs and all start with `\n\n`. It skipped 108 keys, all inside a `first_valid` that follows the opener (end.001, heir.004, init.006, proc.002, the fracture voice bands…). All 108 happen to start with `\n\n` as well.
  - **L014:** all 1,576 keys containing `eotg_` are reached by script, a convention or `$KEY$`. The 60 decision `_desc`/`_confirm` and modifier `_desc` keys are reached only by convention.
- **recipe totals:** 163 events.
  - **Fire cold:** 39.
  - **After setup:** 63. The event's own trigger needs console lines or arrangements.
  - **No:** 61. These need a saved scope, a running story or play-created state.

  | Group | Events | Cold | Setup | No |
  |---|---|---|---|---|
  | Initiation | 20 | 8 | 9 | 3 |
  | Augmented | 22 | 6 | 12 | 4 |
  | Enhanced | 21 | 5 | 9 | 7 |
  | Overclocked | 24 | 6 | 12 | 6 |
  | Countdown | 6 | 1 | 3 | 2 |
  | Neurofractured | 29 | 11 | 8 | 10 |
  | Heir's Arc | 6 | 0 | 0 | 6 |
  | Endgames | 11 | 1 | 8 | 2 |
  | Patron | 8 | 1 | 0 | 7 |
  | Iron Retinue | 5 | 0 | 0 | 5 |
  | Non-ruler | 6 | 0 | 0 | 6 |
  | Procedures | 5 | 0 | 2 | 3 |

  (The same table is at the top of `console_recipes.md`.)

  **Three sample rows** (the `--event` form):
  ```
  eotg_aug_tier1.005  Weight of Silence
  fire cold:  yes
  for realistic content:
    effect eotg_aug_initiate_effect = yes
  fire:       event eotg_aug_tier1.005
  fired by:   on_action yearly_playable_pulse → eotg_on_yearly_aug_tier1_check

  eotg_aug_init.009  The Cynic's Argument
  fire cold:  after setup
  setup:
    # must not be augmented (if you are: `effect eotg_aug_remove_all_effect = yes`)
    add_trait cynical
    effect add_learning_skill = 12
  fire:       event eotg_aug_init.009

  eotg_aug_patron.002  Repayment
  fire cold:  NO
    - needs story eotg_story_aug_patron running (created by effect eotg_aug_patron_accept_effect)
  fire:       event eotg_aug_patron.002
  fired by:   story eotg_story_aug_patron
  live route: decision eotg_decision_seek_augmentation → event eotg_aug_init.018 option e →
              event eotg_aug_patron.001 option a → effect eotg_aug_patron_accept_effect →
              story eotg_story_aug_patron → this event; then let time run
  ```
- **conformance gaps in built specs (3).** All three are spec wording, not script gaps; read the cited line before acting.
  - **`cybernetics_v2_balance.md:792`, `eotg_fracture.011.desc_misled`:** the line says "minus `eotg_fracture.011.desc_misled`", i.e. the key was removed on purpose. *Architect:* the word "minus" isn't on the exempt list. Either reword it ("removed") or leave it as a known hit.
  - **`cybernetics_v2_procedures.md:24`, `eotg_mod_aug_illegal_implants`:** this is the "Gaps doc says" column of a corrections table. The spec itself says the real key is `eotg_mod_illegal_implants`. It's a false positive by design.
  - **`cybernetics_v2_procedures.md:359`, `eotg_alley_outcome`:** "Every `scope:eotg_alley_outcome` becomes `scope:eotg_proc_outcome`". The old name is gone, as specified. It's a false positive by design.
  - **Unbuilt specs:**
    - `interactions` and `interactions_lore`: 81 missing.
    - `realm` and `realm_lore`: 76 missing and 1 exempt.
    - `reprisal` and `reprisal_lore`: 14 missing; `eotg_aug_patron.009` doesn't exist yet.
  - **In script but named by no spec:** 134 definitions. By kind: 50 saved scopes, 28 effects, 20 modifiers, 12 flags, 8 events, 7 variables, 6 triggers, 3 namespaces.
    - The 8 events are countdown.002/.003, patron.007, retinue.002/.004, tier1.014/.019 and tier3.018. The specs likely refer to them as ranges or by title.
    - The 20 modifiers are mostly the per-skill tier bonuses (`eotg_mod_aug_*_bonus`, `eotg_mod_enh_*`, `eotg_mod_oc_*`, `eotg_mod_nf_*_distortion`).
    - This list is for the architect. It is not a defect list.
- **unverified-vanilla:**
  - **L013d:** that the engine concatenates the children of `desc = { }` in order with no separator. The `\n\n` convention matches the mod's own loc, but wasn't checked against vanilla.
  - **L014:** the conventions marked `"verified": false`: deathreason `_killer`/`_unknown`; interaction `_extra_icon`; scheme `_action`/`_name`/`_success_desc`…; law `_effects`; court position `court_position_<x>`; story_cycles; buildings. A wrong pattern can only hide a dead key; it can't invent one.
  - **Recipes:**
    - whether the console `event` command evaluates the event's `trigger`. The recipe assumes it does, hence "after setup" and "no" for story-gated events;
    - whether `add_trait eotg_neurofractured` from the console is enough to test Neurofractured events. The recipe takes `has_trait` literally.
- **needs-human:**
  - **Story events.** The recipes disagree with test plan §4's Console column on 15 story events: heir.001/.003/.004, fracture.005, patron.003–.007 and retinue.001–.005. The plan says `event <id>` works. The script's own `trigger` needs `any_owned_story = { story_type = … }`, so the recipe says **no**, with the live route.
    - One in-game try settles the UNVERIFIED point above: `event eotg_aug_patron.003` with no patron story.
  - **`duel_value`.** The plan marks 6 events "via parent (needs `duel_value`)": init.016, tier1.010, tier1.016, tier2.005, tier2.015 and fracture.017. In script, `duel_value` is read only inside the event's own `duel` block, which sets it. The recipes call them fire-cold or after-setup.
  - **The 3 spec wording items above (architect).**
- **taskboard (proposed):**
  - "human: test one story event cold (`event eotg_aug_patron.003` without a patron) to settle whether the console checks event triggers. Then correct `cybernetics_test_plan.md` §4 Console or the recipe assumption."
  - "orchestrator: from now on, re-run `python docs/tools/gen_test_recipes.py` and `spec_conformance.py` after each event or spec batch. `check_all` FAILs when they are stale."
  - "architect: the 3 conformance wording items. Optionally, mention the 134 unnamed definitions in the spec index."
