# CLAUDE.md — Echoes of the Grip

This file is read automatically by Claude Code at the start of every session.
Read it fully before doing any work on this mod.

---

## What This Project Is

**Echoes of the Grip** is a CK3 total conversion mod set in an original sci-fi/fantasy galaxy.
The primary gameplay bookmark is **866 AG** (After the Grip).

### Essential reading before writing any code
- `docs/CK3_Modding_Complete_Reference_v1_19.md` — all CK3 1.19 scripting rules, syntax, and gotchas
- `docs/866_bookmark_design.md` — canonical lore, nation states, and scripting priorities for the 866 AG bookmark
- `docs/governments.md` — government types designed for this mod (if present)
- `CONTRIBUTING.md` — coding conventions, branch naming, and PR checklist

---

## The One Rule That Cannot Be Broken

**Every single mod-specific identifier must be prefixed with `eotg_`.**

This applies to: event namespaces, scripted effects, scripted triggers, flags, variables,
decisions, traits, modifiers, cultures, religions, titles, dynasties, on_actions, story cycles,
men-at-arms types, buildings, laws, governments, and bookmark keys.

CK3 namespace collisions are completely silent — no error is ever logged.
Two identifiers with the same name will overwrite each other with zero warning.

---

## File Placement Rules

| What | Where |
|---|---|
| All event files | `events/` — **never** `common/events/` (that path does not exist in CK3) |
| Scripted effects | `common/scripted_effects/` |
| Scripted triggers | `common/scripted_triggers/` |
| Static modifiers | `common/modifiers/` |
| Traits | `common/traits/` |
| Cultures | `common/culture/cultures/` |
| Religions & faiths | `common/religion/religion_types/` (CK3 1.19 — **not** `religions/`) |
| Religion families | `common/religion/religion_family_types/` |
| Holy sites | `common/religion/holy_site_types/` |
| Doctrines | `common/religion/doctrine_types/` |
| Governments | `common/governments/` |
| Laws | `common/laws/` |
| Bookmark definition | `common/bookmarks/bookmarks/` (nested subfolder in 1.19) |
| Landed titles | `common/landed_titles/` |
| Localization | `localization/english/*_l_english.yml` |
| Vanilla loc overrides | `localization/english/replace/` |
| History characters | `history/characters/` |
| History titles | `history/titles/` |
| History provinces | `history/provinces/` |
| Design documents | `docs/` |

---

## Localization Rules

- All `.yml` files **must** be saved as **UTF-8 with BOM** — files without BOM fail silently
- Filename must end in `_l_english.yml`
- One space before each key, strings in double quotes, version counter always `:0`
- Never hardcode any player-visible text in script — always use a loc key
- Every new identifier needs a corresponding loc key

---

## Critical Scripting Rules

### Events
- Events do NOT auto-fire — every event must be explicitly called from an on_action,
  decision, interaction, story cycle, or another event
- Never add `effect = {}` directly to a vanilla on_action — it silently overwrites vanilla
- Chain custom behaviour via `on_actions = { eotg_my_action }` in a custom on_action instead

### on_action merging
- `events`, `random_events`, and `on_actions` sub-blocks are **additive**
- `effect = {}` and `trigger = {}` at the top level of an on_action **overwrite** vanilla — never use these on vanilla on_actions

### Scope discipline
- Always know what scope you are in before writing triggers or effects
- Use `save_scope_as` and `scope:name` for named scopes across event options
- Common scopes: `root`, `scope:actor`, `scope:recipient`, `scope:hook_target`

---

## Validation — Run CK3 Tiger Before Every Test

Tiger is located at:
```
C:\Users\river\tools\ck3-tiger-windows-v1.17.0\ck3-tiger.exe
```

CK3 vanilla files are at:
```
D:\SteamLibrary\steamapps\common\Crusader Kings III\game
```

To validate the mod, run from PowerShell:
```powershell
& "C:\Users\river\tools\ck3-tiger-windows-v1.17.0\ck3-tiger.exe" `
  --game "D:\SteamLibrary\steamapps\common\Crusader Kings III\game" `
  "c:\Users\river\Documents\GitHub\ck3.echoes.of.the.grip"
```

Tiger catches: missing loc keys, invalid scope usage, undefined references, syntax errors,
and bad trigger/effect combinations. Fix all errors and warnings before committing.

When Tiger output is pasted into this chat, fix all listed issues before moving on.

---

## Vanilla Reference

Before writing any new system, check how vanilla CK3 does it:
```
D:\SteamLibrary\steamapps\common\Crusader Kings III\game\common\
D:\SteamLibrary\steamapps\common\Crusader Kings III\game\events\
```

Study the vanilla pattern first. Deviate only when the mod specifically requires it.

---

## 866 AG — Quick Context

- Orrin's Grip (the cataclysm) was **866 years ago** — living history, not myth
- The Titan Exodus from the Titanworld is **still ongoing**
- The Myr Cluster Wars **just ignited** (850 AG) — early phase only
- **No Galactic League of States** exists yet (forms 1650 AG)
- New Cauldron is a **735-year-old democracy** built from the ruins of Orrin's Grip's capital city
- The Nikios Khanate just recovered from the **War of Broken Hooves** (~800–840 AG)

Full nation-by-nation breakdown: `docs/866_bookmark_design.md`

---

## Workflow for Every Task

1. Read the relevant section of `docs/CK3_Modding_Complete_Reference_v1_19.md` before writing
2. Check vanilla CK3 files for the pattern you're implementing
3. Write code with `eotg_` prefix on everything
4. Add localization keys for every new identifier
5. Run Tiger and fix all errors
6. Commit with a descriptive message

---

## Branch Naming

| Branch | Use |
|---|---|
| `main` | Stable only |
| `dev` | Integration — all PRs target here |
| `feature/<name>` | New systems |
| `nation/<name>` | Nation/history work |
| `event/<chain>` | Event chains |
| `fix/<description>` | Bug fixes |
