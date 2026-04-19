# Contributing to Echoes of the Grip

Thank you for contributing! This document covers the conventions that keep the mod consistent and maintainable.

---

## Prefix Rule — Non-Negotiable

Every mod-specific identifier **must** be prefixed with `eotg_`.

This includes:
- Event namespaces: `eotg_orrin_grip`, `eotg_titan_exodus`, etc.
- Scripted effects: `eotg_se_apply_void_corruption`
- Scripted triggers: `eotg_st_is_void_touched`
- Flags: `eotg_flag_grip_survivor`
- Variables: `eotg_var_void_exposure`
- Decisions: `eotg_decision_consult_titan_lore`
- Traits: `eotg_void_touched`, `eotg_grip_survivor`
- Modifiers: `eotg_mod_void_aura`
- Cultures: `eotg_culture_elrossi`
- Religions/Faiths: `eotg_faith_elross`
- Title keys: `eotg_k_cauldron`, `eotg_e_elrossi_imperium`
- Dynasty keys: `eotg_dynasty_benthi`

> Namespace collisions in CK3 are **completely silent** — no error is logged. Two mods defining `is_powerful_ruler` will silently overwrite each other.

---

## Branch Conventions

| Branch | Purpose |
|---|---|
| `main` | Stable, tested releases only |
| `dev` | Integration branch — all PRs target here |
| `feature/<name>` | New systems (e.g. `feature/void-corruption-traits`) |
| `nation/<name>` | Nation/history work (e.g. `nation/elrossi-imperium`) |
| `event/<chain-name>` | Event chain work (e.g. `event/titan-exodus-chain`) |
| `fix/<description>` | Bug fixes |

---

## File Placement Rules

| Content | Location |
|---|---|
| All events | `events/` (**not** `common/events/` — that path does not exist) |
| Scripted effects | `common/scripted_effects/` |
| Scripted triggers | `common/scripted_triggers/` |
| Static modifiers | `common/modifiers/` |
| Traits | `common/traits/` |
| Cultures | `common/culture/cultures/` |
| Religions | `common/religion/religions/` |
| Doctrines | `common/religion/doctrines/` |
| Localization | `localization/english/*_l_english.yml` |
| Vanilla loc overrides | `localization/english/replace/` |
| History characters | `history/characters/` |
| History titles | `history/titles/` |

---

## Localization Requirements

- All `.yml` files **must** be saved as **UTF-8 with BOM**. Files without BOM fail silently on some systems.
- Filename must end in `_l_english.yml`.
- Format:

```yaml
l_english:
 eotg_my_key:0 "Display text here."
 eotg_my_key_desc:0 "A longer description with [ROOT.GetFirstName] inline."
```

- One space before each key. No extra indentation.
- Version counter is always `:0`.
- Never hardcode player-visible text in script files — always use a loc key.

---

## Event Writing Standards

```pdx
# events/eotg_example.txt
namespace = eotg_example

# ── eotg_example.0001 ─────────────────────────────────────────────────────────
# Fires from: on_action / decision / another event
# Scope: character (the affected ruler)
eotg_example.0001 = {
    type = character_event
    title = eotg_example.0001.t
    desc = eotg_example.0001.desc
    theme = void        # or appropriate theme

    trigger = {
        # Conditions that must be true for this event to fire
    }

    option = {
        name = eotg_example.0001.a
        # effects
    }
}
```

- Every event file gets a header comment: what it covers, what calls it, what scope it expects.
- Each event gets a comment block listing its ID, trigger source, and scope.
- Never use `MTTH` — CK3 has no MTTH system. All events must be explicitly called.

---

## on_action Rules

- **Never** add `effect = {}` directly to a vanilla `on_action` — this silently overwrites the vanilla effect.
- Chain custom behaviour via `on_actions = { eotg_my_on_action }` inside a new custom on_action file instead.

---

## Before You Open a PR

1. Run **CK3 Tiger** on the mod and resolve all errors and warnings.
2. Boot the game with `-debug_mode -develop` and verify your changes load without `error.log` entries.
3. Check `database_conflicts.log` if you touched any vanilla-adjacent files.
4. Update `localization/english/` for any new keys you added.
5. Update this CONTRIBUTING.md or README.md if you've added a new system.

---

## Lore Consistency

All scripted content must be consistent with the canonical lore documents in `docs/`.  
If you're unsure about a historical detail, check the Events timeline (`docs/events_timeline.md`) or the Nations compendium (`docs/nations_compendium.md`) before scripting.

Key dates to know:
- `0 AG` — Orrin's Grip; the cataclysm that ends the Second Era
- `131 AG` — The Titan Exodus begins
- `1851 AG` — The main gameplay bookmark

---

## Questions?

Open a GitHub Discussion or ping in the project Discord (link TBD).
