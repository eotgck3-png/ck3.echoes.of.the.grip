# Cybernetics QA scripts

Read-only analysis scripts used in the cybernetics QA rounds (`docs/qa/cybernetics_qa_round2.md`). They count and cross-reference; they are not validators, and Tiger stays the authority on syntax.

**Run** from the repo root with Python 3, no extra packages: `python docs/tools/qa/<script>.py [root]`. `root` is the mod repo root and defaults to the current directory. Inputs are always `events/eotg_augmentation_*.txt`, `common/*/eotg_augmentation_*.txt` and/or `localization/english/eotg_augmentation_l_english.yml`, unless noted. Nothing is written to disk.

| Script | Checks | Run | Inputs |
|---|---|---|---|
| `aug_parse.py` | Shared helpers (event and loc loaders, comment strip). `load` delegates to `docs/tools/pdx_parse.py`. Not run directly. | — | — |
| `trait_coverage.py` | Per-file event and option stats, plus each of the 36 personality traits as option gate, stress response, AI weight and any mention; non-personality traits used. | `python docs/tools/qa/trait_coverage.py` | events, common |
| `event_graph.py` | What fires each event (single / chain head / chain stage / story / decision), orphans, and fired-but-undefined ids. | `python docs/tools/qa/event_graph.py [--list]` | events, common |
| `option_outcomes.py` | Each option's outcome class (fixed / flat roll / weighted roll / duel / conditional), and follow-ups per file including 30+ day delays. | `python docs/tools/qa/option_outcomes.py` | events |
| `risk_moves.py` | Options that move `eotg_fracture_risk` at top level, per file: count, sign and mean/min/max amount. | `python docs/tools/qa/risk_moves.py` | events |
| `loc_mechanical.py` | Loc file BOM, line shape, duplicates (file and tree), missing explicit and implied keys, unused keys, unresolved `$KEY$`. | `python docs/tools/qa/loc_mechanical.py` | loc, events, common, all of `localization/` |
| `loc_scope_refs.py` | Loc `[scope.Func]` references whose event never saves that scope. These are candidates, since the scope may be saved upstream in a chain. | `python docs/tools/qa/loc_scope_refs.py` | loc, events, common |
| `show_option.py` | Prints an option's script by loc key, with `ai_chance` stripped, for comparing text against effect. | `python docs/tools/qa/show_option.py --key eotg_fracture.011.c` | events |
| `option_ai_weights.py` | AI weights, trait gate and flagged effects per option for an event-id prefix. | `python docs/tools/qa/option_ai_weights.py --prefix eotg_aug_init --effects eotg_aug_initiate_effect` | events |
| `progression_sim.py` | Monte-Carlo of years until a tier's progression event fires and is accepted. Weights are passed as arguments, read off the on_action `random_list`. | `python docs/tools/qa/progression_sim.py --total 240 --prog 30 --nothing 150 --cooldown 2` | none; uses its arguments |

**Known limits.**
- Parsing is delegated to `docs/tools/pdx_parse.py` (2026-10-04), which also handles `@` values, inline math, tagged colour blocks, BOM and CRLF; `aug_parse.load` keeps its tuple shape, and every script's output was verified unchanged.
- `event_graph.py` reads `trigger_event` calls only, not on_action `events = {}` lists. This system uses `trigger_event` throughout.
- `loc_mechanical.py` lists `set_variable` / `save_scope_value_as` `name =` arguments as "missing". These are false positives.
