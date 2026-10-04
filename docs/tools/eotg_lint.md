# eotg_lint: static linter for Echoes of the Grip

`docs/tools/eotg_lint.py` is a fast static check, written in plain Python 3 with only the standard library. It catches the mistakes this project has made more than once. It runs in under a second on the whole mod. It **complements** Tiger and the PX Toolkit and does not replace them: it doesn't check scopes or engine vocabulary. It checks project invariants and the tooltip and loc patterns that Tiger accepts but that look wrong in game.

## Usage

```bash
python docs/tools/eotg_lint.py                                   # every rule, whole mod
python docs/tools/eotg_lint.py --baseline docs/tools/eotg_lint_baseline.json   # only NEW findings fail
python docs/tools/eotg_lint.py events/ --rule L005,L007          # filter by path and rule
python docs/tools/eotg_lint.py --json out.json                   # machine-readable
python docs/tools/eotg_lint.py --write-baseline docs/tools/eotg_lint_baseline.json  # accept current
```

- **Paths filter reporting only.** The whole tree is always loaded, because L003, L009 and L010 are cross-file.
- **Exit status** is `1` when any finding is not covered by `--baseline`, or, with no baseline, when there is any finding at all. Otherwise it is `0`.
- **Baseline matching** uses (rule, file, message) and counts duplicates. It ignores line numbers, so edits elsewhere in a file don't break it.
- **Output** is one line per finding, `file:line: SEVERITY RULE message`, then a summary table.
- **Root:** `--root` points at a different mod root. The default is the repo containing the script. This also works on `OLD PROJECT VERSION/`.

## Supporting files

| File | Purpose |
|---|---|
| `docs/tools/pdx_parse.py` | The shared Paradox-script parser, with line numbers. `docs/tools/qa/aug_parse.py` now delegates to it; all QA script output was verified byte-identical. |
| `docs/tools/eotg_lint_baseline.json` | The accepted current findings. Regenerate it only on purpose. |
| `docs/tools/eotg_lint_loc_allowlist.txt` | Vanilla loc keys the mod borrows on purpose (L010). |
| `docs/tools/tests/test_eotg_lint.py`, `test_pdx_parse.py` | Fixture tests: one hit and one non-hit for every rule. Run `python -m unittest discover -s docs/tools/tests`. |

## Rules

### L000 — script file does not parse (WARNING)
The file has unbalanced braces, an operator with no key, or a key with no value. The parser keeps going and reports the line. Tiger is the authority on syntax; this rule only makes sure no file is skipped silently.

### L001 — `eotg_` prefix on mod-defined identifiers (ERROR)
**Checked:**
- event `namespace`s;
- top-level keys in `common/` `scripted_effects`, `scripted_triggers`, `modifiers`, `opinion_modifiers`, `decisions`, `traits`, `story_cycles`, `script_values`, `deathreasons` and `scripted_character_templates`;
- custom on_actions, meaning a top-level on_action key that something lists in `on_actions = { }` or names in `on_action = x`;
- flags set by `add_*flag` / `set_*flag`;
- variables set by `set_variable`, `set_global_variable` and `add_to_(global_)variable_list`.

**Exempt:**
- landed titles, which are tier-first instead (L002);
- `@` constants;
- `$PARAM$` names;
- `common/buildings` and similar vanilla-override folders, whose keys are vanilla keys.

**Why:** CK3 merges every mod and vanilla definition by key, and a collision is silent: the later file wins with no error (CLAUDE.md invariant 1).

**Not checked:** saved-scope names and `set_local_variable`. Both are effect-local, so they can't collide across files.

### L002 — `eotg_[ekdcb]_` anywhere (ERROR)
Same regex as CLAUDE.md invariant 2. It scans every text file under `common/`, `events/`, `history/`, `localization/`, `map_data/` and `gfx/`, comments included.

**Why:** CK3 reads a title's tier from its first two characters. v1's `eotg_e_x` form produced 318 titles the game could not parse.

### L003 — localization files (ERROR)
For every `localization/**/*.yml`, including `replace/`:
- it must start with a UTF-8 BOM;
- its first non-comment line must be `l_<language>:`, taken from the `_l_<language>.yml` filename;
- it must not contain `[scope:`;
- each key is defined **once per language across the whole tree**. The second and later definitions are reported, naming the first.

**Why:**
- A file without a BOM fails to load, with no error.
- `[scope:x.GetName]` is wrong; loc uses bare `[x.GetName]`.
- A duplicated key means one of the two strings is silently lost.

All of these are CLAUDE.md invariant 6. Run on v1 it reports the 166 `replace/` duplicates the lift audit counted, plus 3 header/BOM-type findings.

**UNVERIFIED-VANILLA:** the order in which the engine resolves duplicates between `replace/` and normal loc.

### L004 — dead or non-additive vanilla on_action hook (ERROR)
Two checks:
- A top-level `on_yearly_playable` in `common/on_action`. It appears only in vanilla `.info` prose and never fires; the real hook is `yearly_playable_pulse` (pitfalls §12, catalog lesson 13).
- A top-level `effect = { }` or `trigger = { }` inside a **non-`eotg_`** on_action (a vanilla hook). It replaces vanilla's block instead of adding to it (CLAUDE.md invariant 4). Extend vanilla hooks only with `on_actions = { }` / `events = { }`.

On v1 it flags all three dead hooks: hub, legacy and augmentation (CB-10).

### L005 — unguarded removal on a visible path (WARNING)
`remove_character_modifier = X`, `remove_trait = X` or `remove_opinion = { modifier = X }` that is not guarded by either of these:
- an ancestor with a `limit` that checks `has_character_modifier = X` / `has_trait = X` / `has_opinion_modifier = { modifier = X }`. This covers `if`, `else_if` and list builders like `every_vassal`, as well as a `random_list` entry's `trigger`;
- an ancestor `hidden_effect`, `custom_tooltip` or `custom_description`.

**Visible paths:** event options (not in `hidden = yes` events), decision `effect`, scripted effects (they may be called from an option), and interaction `on_accept` / `on_send` / `on_auto_accept`.

**Why:** a tooltip lists every removal whether or not the character has the modifier or trait. This exact pattern gave an in-game tooltip with about 16 "You lose …" lines. Run against the tree before commit `eca9b9c`, the rule reports 113 such removals. The current tree has 0.

**UNVERIFIED-VANILLA:**
- that `immediate`, `after`, on_action and story-cycle effects never reach a tooltip;
- that `custom_tooltip = { text = … effects }` hides the effects' own lines;
- that `random_list` entries whose `trigger` fails are left out of the tooltip.

### L006 — raw flag or variable shown as a decision requirement (WARNING)
`has_character_flag`, `has_variable` or `has_global_variable` (including under `NOT`, `OR` and so on) directly in a decision's `is_valid`, `is_valid_showing_failures_only` or `is_shown`, and not inside `custom_description` or `custom_tooltip`.

**Why:** the requirement list renders the raw key ("You do not have the eotg_flag_… flag"). Before `eca9b9c` it caught `eotg_flag_maintenance_cooldown` in `is_valid`.

**UNVERIFIED-VANILLA:** whether `is_shown` failures ever render. Normally a failed `is_shown` hides the decision, so the 4 current `is_shown` findings are low priority. They are kept in the baseline in case the debug or decision-list view shows them.

### L007 — event option with only silent effects and no tooltip (WARNING)
An option, in an event with **two or more** options and not `hidden = yes`, that does have effects, but every one of them is silent, and nothing in the option is a `custom_tooltip` / `custom_description` / `show_as_tooltip` / toast.

**What counts as silent:**
- `trigger_event`, `hidden_effect`;
- flag and variable sets and removals;
- `save_scope_as` / `save_scope_value_as`;
- story calls;
- containers (`if`, `random_list`, `scope:x = { }`, `every_*`…) whose contents are all silent;
- mod scripted effects whose body is all silent, resolved recursively.

**Why:** the option's tooltip renders empty, so it looks the same as a "do nothing" option even when it changes hidden state or advances a chain.

**Exempt:** single-option events (a lone "OK" that continues a chain), because there is nothing to tell apart.

**UNVERIFIED-VANILLA:** that variable and flag effects never print a tooltip line, and that `trigger_event` prints none either.

### L008 — skill effect without `_skill` (ERROR)
`add_diplomacy`, `add_martial`, `add_stewardship`, `add_intrigue`, `add_learning` and `add_prowess` as effect keys. The real effects are `add_<skill>_skill` (CLAUDE.md invariant 7, catalog lesson 9). The bare names are unknown, and the engine drops them.

### L009 — event defined but never fired (WARNING)
An event is counted as fired by any reference to its id outside its own body:
- `trigger_event = id` or `{ id = … }`;
- on_action `events`, `random_events` and `first_valid` lists;
- story-cycle effects, decisions, interactions, schemes and scripted effects.

An event that only fires itself counts as unfired.

**Why:** events never fire on their own (CLAUDE.md invariant 4). An orphan is dead content.

**Limit:** references from GUI or code-side hooks are not seen.

### L010 — loc key referenced but not defined (ERROR)
**Keys checked:**
- event `title`, `desc` and option `name`, including keys inside `first_valid`, `triggered_desc` and `random_valid`;
- decision `title` / `desc` / `selection_tooltip` / `confirm_text` when written, otherwise the implied `<key>` and `<key>_desc`;
- trait `name` / `desc` when written, otherwise the implied `trait_<key>` and `trait_<key>_desc`;
- static modifier `<key>` and `<key>_desc`.

**Lookup:** keys are looked up across all `localization/**/*_l_english.yml`, plus `docs/tools/eotg_lint_loc_allowlist.txt` for vanilla keys the mod borrows on purpose.

**Skipped:** values containing spaces, `[`, `$` or `@`, which are inline text or parameters.

**UNVERIFIED-VANILLA:**
- which implied keys the engine actually requires: decision `_tooltip` / `_confirm` are not checked, and modifier `_desc` is checked;
- whether a trait with no `name` falls back to `trait_<key>` or `<key>` (v1 defined both).

## Current baseline (2026-10-04, tree at `27d2e46`)
| Rule | Count | What |
|---|---|---|
| L006 | 4 | `is_shown` flag/variable checks in the Restraints, Sedation and Embrace the Cascade decisions |
| L007 | 24 | silent-only options. Most are options whose only effect is `eotg_add_fracture_risk` (a variable change, by design hidden). Others: the tier1.021 focus choice, patron grievance options, retinue/init chain options |

Every other rule is at 0 on the current tree.

**Cross-checks:**
- On `OLD PROJECT VERSION/` the linter reports 1,426 findings: L002 1,009, L003 169, L004 3, L005 129, L006 19, L007 9, L010 88. These match the lift audit's counts.
- On the tree before commit `eca9b9c` it reports L005 113, L006 5, L007 32.
