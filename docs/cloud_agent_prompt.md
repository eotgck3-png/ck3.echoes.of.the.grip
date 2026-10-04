# Cloud agent prompt (template)

Paste everything below the line into a cloud Claude Code session that only has GitHub access. Replace §6 with one bounded task. Kept current by the local orchestrator.

---

You are working on **Echoes of the Grip**, a Crusader Kings III total-conversion mod (original sci-fi/fantasy galaxy, 866 AG bookmark), in the GitHub repo `eotgck3-png/ck3.echoes.of.the.grip`.

## 0. Branch: read this first
- Work from branch **`v2-space-map`**, NOT `main`. `main` is the frozen v1 tree and is wrong for everything. The branch `claude/great-pasteur-klj6z4` was built on v1 too, so ignore it.
- Create your own branch from `v2-space-map` (e.g. `claude/<task-slug>`), commit there and push. Do **not** merge or open a PR into `main` or `v2-space-map`. The local orchestrator session reviews, validates and merges.
- If `v2-space-map` is missing or its `CLAUDE.md` does not mention "v2", stop and report it. Don't work on `main`.

## 1. What you can't do, and what to do about it
This repo is normally driven by a Claude Code session on the owner's Windows machine. That session can see things you can't. You have **no** access to:

| Missing | Consequence for you |
|---|---|
| The installed CK3 game files (`D:/SteamLibrary/.../Crusader Kings III/game/`) | You can't check vanilla syntax, on_action names, effect/trigger names, scopes or file shapes against the game. |
| ck3-tiger (`C:/Users/river/tools/...`) and the PX Toolkit scripts in `docs/tools/px_*` (they need VS Code + local vanilla) | You can't validate anything. Don't try to run them, and don't claim anything "passes". |
| The `ck3-modding` skill (installed user-wide on that machine, not in the repo) | Not loaded. If you have web access, the same skill is public at `github.com/Sililex/ck3-claude-skill`; clone it into a temp dir (outside the repo) and read its topic files and `reference/common/<folder>/*.info`. |
| Running the game | No in-game checks of any kind. |
| Local paths in docs and agent files (`C:/Users/river/...`, `D:/...`) | They don't exist for you. Treat those instructions as "the local session does this". |

So:
1. **Repo-internal evidence comes first.** It is valid evidence: existing working v2 script in `common/`, `events/` and `localization/`; specs in `docs/specs/`; `docs/pitfalls.md`; `OLD VERSION CATALOG.md`. Copy shapes from v2 files that already exist before inventing anything.
2. **Next, the public `ck3-modding` skill**, if you can fetch it. Last resort: `OLD PROJECT VERSION/docs/CK3_Modding_Complete_Reference_v1_19.md`. It is known to be wrong about loc: it teaches `[scope:x.GetName]`, but the correct form is bare `[x.GetName]`.
3. **Don't guess engine facts.** Some claims rest on vanilla behaviour you couldn't check: an effect or trigger name, an on_action's name or when it fires, a field's validity, a scope's type. Mark each one in code with `# UNVERIFIED-VANILLA: <what to check>` and list it in your handoff (§5). The local session will check them against the game and Tiger.
4. Prefer tasks that don't depend on vanilla at all: specs, design docs, loc text, refactors of existing mod script into already-proven shapes, consistency audits, taskboard hygiene.

## 2. Read before doing anything (in this order)
1. `CLAUDE.md`. Its invariants are binding. Ignore its Tiger/PX command blocks, which are local-only.
2. `circlebackTaskboard.md`: open items, blockers and pending human decisions. Don't do work it marks `blocked` or `waiting-human`.
3. `docs/agent_workflow.md`: gates, ownership and pipelines. Gate 1 (a world that loads) is still open. Don't build Gate 2–4 content, except mod-exclusive systems that don't reference specific titles, provinces, characters, cultures or faiths (cybernetics is one).
4. `docs/pitfalls.md` and `OLD VERSION CATALOG.md` §4, the lessons v1 paid for.
5. The relevant spec in `docs/specs/` for your task.

## 3. Invariants (summary; `CLAUDE.md` wins on conflict)
- `eotg_` prefix on every identifier. Landed titles are tier-first instead (`k_eotg_x`, never `eotg_k_x`). `grep -rnE 'eotg_[ekdcb]_'` must stay empty.
- Events go in `events/`. Each must be fired by something. Vanilla on_actions are extended additively only (`on_actions = { }` / `events = { }`). Cooldowns live in the on_action.
- Every flavor event reads or moves its system's signature resource.
- Loc goes in `localization/english/*_l_english.yml`: **UTF-8 with BOM**, bare `[x.GetName]`, one definition per key across the whole tree. Write the BOM explicitly and check it with `head -c3 file | xxd`, which should show `efbb bf`.
- Skill effects take the `_skill` suffix (`add_intrigue_skill`). The real yearly hook is `yearly_playable_pulse`; `on_yearly_playable` is dead.
- Nikios Khanate content is deferred. Don't build it.
- New events, options or beats beyond an approved spec are the owner's call. Propose them, don't build them.
- Canon: `OLD PROJECT VERSION/docs/SETTING LORE` (its ERRATA block overrides the body). Don't settle open canon questions (see taskboard "Decisions for the human"). Flag them.

## 4. Agents
`.claude/agents/eotg-*.md` define role agents (architect, cartographer, scripter, localizer, qa, lore-keeper, vanilla-scout, intake). You can use them, keeping the ownership split (makers don't sign off their own work). But **`eotg-vanilla-scout` can't work here**: it needs game files. Any "QA pass" you run is static review only, and must be labelled "static, unvalidated".

## 5. Finish with a handoff file
Commit `docs/handoffs/cloud_<YYYY-MM-DD>_<task-slug>.md` to your branch, containing:
```
### HANDOFF (cloud session, unvalidated)
- branch: <name>
- status: done | partial | blocked
- summary: <2–4 lines>
- files: <paths touched>
- unverified-vanilla: <each # UNVERIFIED-VANILLA item, as file:line — what to check>
- needs-local-validation: Tiger + PX on <paths>
- needs-loc: <keys, or none>
- needs-lore: <questions, or none>
- needs-human: <decisions, or none>
- taskboard: <CB items this touches / new items to add>
```
Don't edit `circlebackTaskboard.md` or the gate board in `docs/agent_workflow.md` §6; the local orchestrator owns both. Put proposed changes in the handoff instead.

## 6. Your task
<<TASK GOES HERE: one bounded item, e.g. a CB-## from the taskboard, with the spec or files it concerns>>
