# CLAUDE.md — Echoes of the Grip (v2)

CK3 1.19 total-conversion mod, original sci-fi/fantasy galaxy, primary bookmark **866 AG**. This is the second iteration. The first lives, frozen, in `OLD PROJECT VERSION/`; read `OLD VERSION CATALOG.md` before touching anything — it says what to lift, what to rewrite, and the twelve lessons v1 paid for.

## Work is done through agents
Eight subagents in `.claude/agents/` split the work by ownership; `docs/agent_workflow.md` is the protocol (gates, pipelines, handoff block). Read it before dispatching. Short version:

| Need | Agent |
|---|---|
| Design a system / decide identifiers | `eotg-architect` (writes `docs/specs/` only) |
| Titles, provinces, map, history, bookmarks, descriptor | `eotg-cartographer` (Gate 1 owner) |
| Events, effects, governments, on_actions, cultures, religions | `eotg-scripter` |
| Localization | `eotg-localizer` |
| Tiger run, audits, review — read-only | `eotg-qa` |
| Canon check, names — read-only | `eotg-lore-keeper` |
| "How does vanilla do X" — read-only | `eotg-vanilla-scout` |
| Turn the lore briefs for a region into a build order; send questions to the vault | `eotg-intake` (writes `docs/specs/regions/` only) |

The main session orchestrates, relays handoffs, updates the gate board in `docs/agent_workflow.md` §6 and the loose-ends board in **`circlebackTaskboard.md`** (read it at session start; deferred items, blockers and human decisions live there, with usage rules at the top), and is the only thing that commits. Nothing in Gates 2–4 is built while Gate 1 (a world that loads) is open — except **mod-exclusive systems** (decided 2026-10-02), which are built and tested against a **temporary map** until the real one lands. Cybernetics (augmentation) is the first. The **PMC, Corporation, Cartel and Gob-Corp governments** are also exempt (owner, 2026-10-08). They are tested on the British Isles test sub-mod (`docs/test_submods/british_isles`) and specced in `docs/specs/governments_v2.md`. Such systems must not depend on specific titles, provinces, characters, cultures or faiths, so they survive the map swap.

## World data comes through `intake/`
The setting arrives as Markdown **briefs** per region (`intake/regions/<region>/`, shared material in `intake/setting/`), written from the Obsidian lore vault by an external Gemini agent against `intake/templates/`. They are reference for agents to read, not input for a program: `eotg-intake` turns a region folder into a build order in `docs/specs/regions/`, and the cartographer / scripter / localizer author the script from the briefs and that order. Facts the briefs do not settle go back to the vault as questions, never into script as guesses. The mod ships its **own `map_data/`** (decided 2026-09-21); province ids come from the mod's `definition.csv`.

## Invariants
1. **`eotg_` prefix on every identifier** — namespaces, effects, triggers, flags, variables, decisions, traits, modifiers, cultures, faiths, dynasties, governments, on_actions, story cycles, MAA, bookmarks. Collisions are silent.
2. **Landed titles are the one exception: tier-first.** `e_eotg_x`, `k_eotg_x`, `d_eotg_x`, `c_eotg_x`, `b_eotg_x`. CK3 reads tier from the first two characters; the v1 form `eotg_e_x` produced 318 unparseable titles. `grep -rnE 'eotg_[ekdcb]_'` must always be empty.
3. Every barony has `province =`. Never `replace_path` a folder the mod does not ship.
4. Events live in `events/`, are always fired by something, and extend vanilla on_actions **additively** (`on_actions = { }`, `events = { }`) — never top-level `effect = {}` / `trigger = {}` on a vanilla hook. Cooldown authority lives in the on_action, not duplicated in the event trigger.
5. Every flavor event reads or moves its system's signature resource. No vignettes.
6. Loc: `localization/english/*_l_english.yml`, **UTF-8 with BOM**, bare `[x.GetName]` (never `[scope:x]`), one definition per key across the tree including `replace/`.
7. Skill effects take `_skill` (`add_intrigue_skill`). Shared opinion modifiers carry no government prefix.
8. Makers do not sign off their own work; QA and lore-keeper do not fix.
9. Nikios Khanate content is deferred — do not build it.

## File placement
Use the table in `OLD PROJECT VERSION/CLAUDE.md` (written for 1.19: `common/religion/religion_types/`, `common/bookmarks/bookmarks/`, etc.). **Except religion, which 1.20 split** (2026-10-04): religions go in `religion_types/` with `religion_details = { }`; faiths go in `common/religion/faith_types/` (`faith_details`, list-form `tenets`/`doctrines`); optional `rite_types/`; families take `tenet_background_icon`. v1 religions are the old shape and need a port, not a copy (`docs/qa/v1_lift_readiness_cloud.md` §6). Add `map_data/` and `common/dynasties/` to it, plus `common/story_cycles/`, `common/deathreasons/`, `common/scripted_character_templates/` and `common/script_values/` (cybernetics v2, 2026-10-03; shapes per vanilla, cited in `docs/specs/cybernetics_v2.md`), plus `common/character_interactions/`, `common/schemes/scheme_types/`, `common/law_groups/`, `common/laws/` (1.20 splits law groups from laws; laws carry `law_group_type`) `common/court_positions/types/` and `common/culture/innovations/` (cybernetics content specs, 2026-10-04; shapes cited in `docs/specs/cybernetics_v2_interactions.md` and `cybernetics_v2_realm.md`), plus `common/customizable_localization/` (2026-10-05), plus `common/governments/`, `common/subject_contracts/contracts/`, `common/subject_contracts/groups/`, `common/flavorization/` and `gfx/interface/icons/government_types/` (governments v2, 2026-10-08; shapes in `docs/specs/governments_v2.md`). The seller-name files in it are **generated** from `cybernetics_seller_names.txt` by `docs/tools/gen_seller_names.py`, so never hand-edit them. In-game testing how-to: `docs/qa/HOW_TO_TEST_IN_GAME.md`.

## Validation
Black map, neon borders, or errors in files the mod does not touch: see `docs/pitfalls.md` first — all three have known causes.

Tiger 1.17.0 against CK3 1.19. From the Bash tool:
```bash
"/c/Users/river/tools/ck3-tiger-windows-v1.17.0/ck3-tiger.exe" --game "D:/SteamLibrary/steamapps/common/Crusader Kings III/game" "echoes_of_the_grip.mod"
```
Known benign (Tiger predates the 1.19 religion folder rename): ~48 faith/religion-path lookups, ~24 culture lookups, 2 `error(filename)` on the religion folders. Do not "fix" those. Everything else is real. **This exemption covers only lookups into vanilla's religion folders.** Tiger 1.17 doesn't understand the 1.20 religion schema at all, so once the mod ships its own religions or faiths, a clean Tiger run proves nothing about them. Check every ported religion and faith against the vanilla `.info` files and a vanilla example by hand (eotg-vanilla-scout). Write Tiger logs to the scratchpad, not the repo.

**Note (2026-10-03, updated 2026-10-04):** the installed game is now 1.20.0.3 "Crozier", and Tiger 1.17 targets 1.18.3. These are version noise inside vanilla files, so don't "fix" them:
- **About 48 errors in `20_health_effects.txt`** (`change_spiritual_fulfillment` ×36, `has_personal_tenet_flag` ×12), reached through `increase_wounds_effect`. The count grows with the number of call sites.
- **The vanilla trigger override** `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt` (2026-10-06): 17 `strict-scopes` warnings, "herders_and_tributary_constraints expects scope:attacker to be set", one per CB group. The engine sets that scope; see pitfalls §16.
- **`rite` as an unknown field** in `create_character` and in character templates. Tiger 1.17 predates 1.20 rites; vanilla's `herder_character` uses the same field.
- **The `execute_prisoner_effect` / `imprison_character_effect` path into vanilla `00_prison_effects.txt`** (2026-10-08, kingpin): `stress_and_fulfillment_impact`, the situation parameter `the_christian_church_clerical_violence_less_consequential`, plus the same `rite` / `change_spiritual_fulfillment` / `has_personal_tenet_flag` / `check_rite` strict-scopes family. These are 1.20 tokens that Tiger 1.17 doesn't know.
- **Story-cycle fields `visible`, `icon`, `background`, `visualization`** (`eotg_aug_kingpin_story.txt`). They're documented in vanilla `_story_cycles.info` and used by `book_translation_story_cycle.txt`.
- **The decision county-picker widget** (`eotg_frontier_decisions.txt`, 2026-10-08). Tiger reports `error(choice)` on `controller = select_scope_object`, and unknown-field on `setup_items`, `default_item`, `is_item_valid` and `ai_select_item`, five per widget. These are documented in vanilla `_decisions.info:305-350`.
- **`missing-item` on the `eotg_aug_policy_*` laws.** Tiger can't parse the 1.20 law-group split.
- ~~PX vocab `use_great_projects`~~ is NOT benign (2026-10-08). The 1.20 parser rejects it ("Unexpected token" in error.log) even though `_governments.info:630` documents it, so the field was removed. Lesson: a field that appears only in `.info` and in no vanilla file is not proof the game accepts it.
- **Errors from the kinslayer path** (`add_kinslayer_trait_or_nothing_effect` → `00_secret_effects` / `00_religious_triggers`): `knows_doctrine` / `add_known_doctrine` (about 14), `rite` / `rite_has_parameter` (about 28), and strict-scopes warnings that `check_rite` / `check_rite_liege` are unset. Vanilla sets those scopes itself with `save_temporary_scope_as` (`00_religious_triggers.txt:389,397`).

A new descriptor must say `supported_version="1.20.*"`. `echoes_of_the_grip.mod` at the repo root is the Tiger descriptor. The game loads the repo directly: `Documents/Paradox Interactive/Crusader Kings III/mod/eotg_stellar_rivers` is a directory junction to it (2026-10-04), so the working tree, including uncommitted edits, is what the game runs.

**PX Toolkit checks** run alongside Tiger on every script or loc change. They come from the VS Code extension `jdeffner.px-toolkit`, and each catches things the others miss:
```bash
# language server: braces, missing values, BOM/loc-file format, dangling event ids, required loc (~10 s once vanilla is cached)
ELECTRON_RUN_AS_NODE=1 "/c/Users/river/AppData/Local/Programs/Microsoft VS Code/Code.exe" docs/tools/px_lsp_diagnostics.js common events localization
# engine vocabulary: unknown effects/triggers/modifiers, undefined traits/modifiers/events, dead vanilla hooks
python docs/tools/px_vocab_check.py common events
# PX's Event Graph + loc coverage as JSON, then reachability (invariant 4) and missing eotg_ loc
ELECTRON_RUN_AS_NODE=1 "/c/Users/river/AppData/Local/Programs/Microsoft VS Code/Code.exe" docs/tools/px_lsp_diagnostics.js events --request=eventGraph --request=locCoverage --out=<scratchpad>
python docs/tools/px_event_report.py <scratchpad>
```
Neither checks scope (e.g. `add_gold` inside `capital_county`); Tiger does. Known-benign PX findings: `missing-required-loc` on `building_walls_*` (vanilla has no loc for them either).

## Reference sources, in precedence order
0. **`docs/pitfalls.md`** — repeated issues and their confirm-before-you-change steps. Read it BEFORE debugging any visual or shader problem; every entry is something this project has got wrong more than once. Add to it whenever something costs more than one attempt.
1. **`CLAUDE.md` invariants and the v1 lessons** (`OLD VERSION CATALOG.md` §4) — these encode failures this project actually paid for. They win over any external reference.
2. **Vanilla game files** — `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`. Copy the shape of the vanilla equivalent before writing anything new. `eotg-vanilla-scout` exists for this.
3. **The `ck3-modding` skill** — installed at `C:/Users/river/.claude/skills/ck3-modding/` (from github.com/Sililex/ck3-claude-skill). Topic files (`scopes.md`, `effects.md`, `triggers.md`, `events.md`, `governments.md`, `religions.md`, `cultures.md`, `history.md`, `bookmarks.md`, and more) plus `reference/common/<folder>/*.info` field specs covering 97 folders. Agents reach it via the Skill tool or by reading the file directly — reading one file is usually cheaper than loading the whole skill. **Gaps:** no `map_data/` coverage (definition.csv, provinces.png, default.map, heightmaps, positions.txt) and no `common/dynasties` spec — use vanilla for those.
4. **`OLD PROJECT VERSION/docs/CK3_Modding_Complete_Reference_v1_19.md`** — last resort. It teaches `[scope:x.GetName]` in loc, which is wrong; the skill gets it right.

If a lower source contradicts a higher one, follow the higher and report the contradiction rather than silently picking.

## Canon
`OLD PROJECT VERSION/docs/SETTING LORE` ERRATA block first, then the **dated** entries in the `docs/lore/` histories (only what exists by 866 AG), then `866_bookmark_design.md`, then the SETTING LORE body (human ruling, 2026-10-04). Start from `docs/lore/REVIEW_866.md`, the digest of what holds at 866. The undated "Nation in 851" summaries in `Third era Nations.md` often describe later states, so never cite them over a dated entry. 866 AG: the Grip was 866 years ago and is living history; the Titan Exodus is ongoing; the Myr Cluster Wars ignited 850 AG; no Galactic League yet.

## Reference material in the old tree
- `docs/CK3_Modding_Complete_Reference_v1_19.md` — 1,770-line syntax reference. Known error: it teaches `[scope:x.GetName]` in loc.
- `docs/closed_alpha_checklist.md`, `system_depth_audit.md`, `government_robustness_plan.md` — why v1 failed, per system.
- `docs/title_hierarchy.md` — the intended title tree with province ids; never applied. Source draft for Gate 1.
