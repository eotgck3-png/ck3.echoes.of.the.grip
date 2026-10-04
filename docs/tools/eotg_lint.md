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
| `docs/tools/eotg_lint_pronoun_allowlist.txt` | Loc keys where they/them is plural (L011), each with a reason. |
| `docs/tools/eotg_lint_register.json` | The cybernetics never-name and register terms (L012), as data. |
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
`has_character_flag`, `has_variable` or `has_global_variable` (including under `NOT`, `OR` and so on) directly in a decision's `is_valid` or `is_valid_showing_failures_only`, and not inside `custom_description` or `custom_tooltip`.

**Why:** the requirement list renders the raw key ("You do not have the eotg_flag_… flag"). Before `eca9b9c` it caught `eotg_flag_maintenance_cooldown` in `is_valid`.

**`is_shown` is not checked** (FIX 3, 2026-10-04). A decision whose `is_shown` fails is hidden entirely, so a raw flag there never renders.

### L007 — option whose only consequence is deferred (WARNING)
An option, in an event with **two or more** options and not `hidden = yes`, whose effects are **only deferred**, with nothing in the option being a `custom_tooltip` / `custom_description` / `show_as_tooltip` / toast.

**Deferred** means:
- `trigger_event`, `create_story` or `start_scheme`;
- a container (`if`, `hidden_effect`, `random_list` entry, `scope:x = { }`, `every_*`…) holding only deferred effects;
- a mod scripted effect whose body is only deferred effects, resolved recursively.

Scope saves (`save_scope_as`, `save_scope_value_as` and the temporary forms) are neutral and may accompany them.

**Why:** the consequence arrives later and invisibly, so the option looks identical to "do nothing". The motivating bug was `eotg_aug_init.018.e`, whose only effect was `trigger_event = { id = … days = 1 }` and which looked the same as "Not yet." The rule reports it, and four similar options, on the tree at `2e6cef2`.

**Deliberately not flagged** (FIX 2, 2026-10-04):
- Options that only move **hidden resources**: `eotg_add_fracture_risk`, variables, flags, voice advances. The hidden-risk design keeps those silent on purpose.
- An option that moves a hidden resource **and** fires an event, because it has a non-deferred effect.

**Exempt:** single-option events, such as a lone "OK" continuing a chain.

**UNVERIFIED-VANILLA:** that `trigger_event` with `days` prints no tooltip line.

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

### L011 — single named character referred to as they/them (WARNING)
House rule (owner, 2026-10-04): a single scoped character gets gendered pronouns via loc functions.

**What it flags:** in `localization/**/eotg_*.yml`, a value that:
- references **exactly one** character scope by name (`[x.GetName]`, `[x.GetFirstName]`, `[ROOT.Char.GetName]`, `GetTitledFirstName`, `GetFullName`, …);
- uses they / them / their / themself / theirs in its visible text;
- has no gendered function (`[x.GetSheHe]`, `GetHerHim`, `GetHerHis`, `GetHerselfHimself`, …).

**False positives are expected.** Plural "they" is legitimate: a group, the court, the faction's members, the syndicate, or "the others" in the same sentence as one named character. Triage each hit. If it is plural, add the key to `docs/tools/eotg_lint_pronoun_allowlist.txt` with the reason. All three hits on the current tree were plural and are allowlisted.

**Missed by design:**
- values naming two or more characters, where "they" is ambiguous;
- values that name nobody;
- non-`eotg_` files.

### L012 — cybernetics never-names and register (ERROR / WARNING)
The rules are data, in `docs/tools/eotg_lint_register.json`, encoded from:
- `docs/specs/cybernetics_v2.md` §5 items 2–3;
- the `hack|virus|upload|network|harvest` grep in `docs/specs/cybernetics_v2_interactions_lore.md`;
- the `telemetry|warrant|magistrat|inspector|registry|encourag|sponsor|patronag` grep in `docs/specs/cybernetics_v2_realm_lore.md`.

**Scope:** only loc keys starting `eotg_aug_`, `eotg_fracture`, `eotg_mod_aug`, `eotg_decision_aug` or `eotg_opinion_aug`. Matching is on the **visible text**: `[functions]`, `$keys$` and `#formatting` are removed first.

**ERROR (never-names):**
- Blackstar, Shadow Market(s), Black Contract(s), Blackline, P&D, Calix, Pill Mob, Pillwake, Red Pills, Concrete Cartel;
- Acathea, Codex, Archivist(s) as a capitalised proper noun, Conclave, Carrigore, Trauma Team, Galactic League;
- "galactic", "interstellar regulation".

**WARNING (listing the key, for human triage):**
- whisper, "edge of hearing", "speaks from", possess(ion), demon, pact, abyss;
- "the Eye", Orrin, Kyros, Void, rift, breach, "answers" (the verb);
- remote, hack, virus, upload, network, harvest, telemetry;
- warrant, magistrate, inspector, registry, encourage, sponsor, patronage, programme/program.

**Known noisy terms** (WARNING by design):
- "warrant" hits fracture.006 *The Warrant*, a vassal faction.
- "program" hits the Iron Retinue's *Program*.
- "answers" also matches the noun.
- "Archivist" at the start of a sentence matches even when it isn't a proper noun.

Edit the JSON, not the code, when the rules change. Each entry has `term`, `regex`, `case` (true means case-sensitive) and `source`.

## Inline suppression
To silence one finding, put this on the finding's line or on the line directly before it:

```
# eotg_lint: allow L007 the follow-up event's own option explains the cost
```

- **Several rules:** `allow L005,L007 reason`.
- **A reason is required.** An allow without a reason is itself an **L000** finding, and it suppresses nothing. So is an allow with no rule id or with an unknown id.
- **Where it works:** script (`.txt`) and loc (`.yml`) files alike. For L007, the finding's line is the `option = {` line.
- **Suppression vs baseline:** use suppression for a deliberate, reviewed exception that should stay quiet forever. Use the baseline for known debt that should be fixed later.

## Current baseline (2026-10-04, tree at `43057db`)
| Rule | Count | What |
|---|---|---|
| L012 | 14 | All WARNING (register triage), 0 never-name ERRORs. The hits are "warrant" ×6 (fracture.006 *The Warrant*), "program" ×4 (the Iron Retinue's Program, init.019.b), "encourage" ×2, "answers" ×2. |

Every other rule is at 0:
- **L007:** the 24 earlier hits were hidden-resource moves; it is now narrowed to deferred-only options (FIX 2).
- **L006:** the 4 earlier hits were all in `is_shown` (FIX 3).
- **L011:** 3 hits, all plural "they", so allowlisted.

**Cross-checks:**
- On `OLD PROJECT VERSION/` the linter reports L002 1,009, L003 169, L004 3, L005 129 and L010 88.
- On the tree at `2e6cef2`, L007 reports the init.018.e bug.
