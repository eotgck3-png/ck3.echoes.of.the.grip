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

The main session orchestrates, relays handoffs, updates the gate board in `docs/agent_workflow.md` §6, and is the only thing that commits. Nothing in Gates 2–4 is built while Gate 1 (a world that loads) is open.

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
Use the table in `OLD PROJECT VERSION/CLAUDE.md` — it is still correct for 1.19 (`common/religion/religion_types/`, `common/bookmarks/bookmarks/`, etc.). Add `map_data/` and `common/dynasties/` to it.

## Validation
Tiger 1.17.0 against CK3 1.19. From the Bash tool:
```bash
"/c/Users/river/tools/ck3-tiger-windows-v1.17.0/ck3-tiger.exe" --game "D:/SteamLibrary/steamapps/common/Crusader Kings III/game" "echoes_of_the_grip.mod"
```
Known benign (Tiger predates the 1.19 religion folder rename): ~48 faith/religion-path lookups, ~24 culture lookups, 2 `error(filename)` on the religion folders. Do not "fix" those. Everything else is real. Write Tiger logs to the scratchpad, not the repo.

## Reference sources, in precedence order
1. **`CLAUDE.md` invariants and the v1 lessons** (`OLD VERSION CATALOG.md` §4) — these encode failures this project actually paid for. They win over any external reference.
2. **Vanilla game files** — `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`. Copy the shape of the vanilla equivalent before writing anything new. `eotg-vanilla-scout` exists for this.
3. **The `ck3-modding` skill** — installed at `C:/Users/river/.claude/skills/ck3-modding/` (from github.com/Sililex/ck3-claude-skill). Topic files (`scopes.md`, `effects.md`, `triggers.md`, `events.md`, `governments.md`, `religions.md`, `cultures.md`, `history.md`, `bookmarks.md`, and more) plus `reference/common/<folder>/*.info` field specs covering 97 folders. Agents reach it via the Skill tool or by reading the file directly — reading one file is usually cheaper than loading the whole skill. **Gaps:** no `map_data/` coverage (definition.csv, provinces.png, default.map, heightmaps, positions.txt) and no `common/dynasties` spec — use vanilla for those.
4. **`OLD PROJECT VERSION/docs/CK3_Modding_Complete_Reference_v1_19.md`** — last resort. It teaches `[scope:x.GetName]` in loc, which is wrong; the skill gets it right.

If a lower source contradicts a higher one, follow the higher and report the contradiction rather than silently picking.

## Canon
`OLD PROJECT VERSION/docs/SETTING LORE` (ERRATA block at the top overrides the body) and `866_bookmark_design.md`. 866 AG: the Grip was 866 years ago and is living history; the Titan Exodus is ongoing; the Myr Cluster Wars ignited 850 AG; no Galactic League yet.

## Reference material in the old tree
- `docs/CK3_Modding_Complete_Reference_v1_19.md` — 1,770-line syntax reference. Known error: it teaches `[scope:x.GetName]` in loc.
- `docs/closed_alpha_checklist.md`, `system_depth_audit.md`, `government_robustness_plan.md` — why v1 failed, per system.
- `docs/title_hierarchy.md` — the intended title tree with province ids; never applied. Source draft for Gate 1.
