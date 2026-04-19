# Echoes of the Grip — CK3 Total Conversion Mod

> *"And so the Titan's hand gripped the veil, pulling creation into chaos."*

**Echoes of the Grip** is a total conversion mod for Crusader Kings III set in the Third Era — the age that began when Orrin, Titan of the Void, tore through the fabric of reality and merged the First and Second Material Planes in the cataclysm known as **Orrin's Grip (0 AG)**.

The mod places players into the fractured galaxy that emerged from that catastrophe: weakened gods, freed titans, scattered civilizations struggling to rebuild, and the looming shadow of Orrin and Yu's war reshaping the cosmos.

---

## Setting

The Third Era begins at **0 AG** — the moment of Orrin's Grip. The game's primary bookmark opens at **866 AG**, a pivotal mid-era moment where the galaxy is simultaneously rebuilding and fracturing again.

### 866 AG — The State of the Galaxy

**866 AG is a world in flux:**

- The **Titan Exodus** (begun 131 AG) is still ongoing — the last refugees of the Titanworld continue trickling into galactic space
- The **Myr Cluster Wars** have just ignited (850 AG) — New Cauldron, the Gob-Ogre Trade League, the Coldiron Caliphate, and the Elrossi Imperium are all beginning to circle the resource-rich Myr Clusters
- **New Cauldron** is 735 years into its democracy, a thriving mercenary republic built from the literal ruins of Orrin's Grip's capital city
- The **Nikios Khanate** just weathered the War of Broken Hooves (800 AG) — the centaur clans are bruised, consolidating under a new Khan
- The **Shatter Stance** Hobgoblins are scattered in bitter exile across the Devoid Systems, not yet unified under the Ironshard Concord
- No **Galactic League of States** exists yet — it won't form until 1650 AG, leaving the galaxy a true multipolar free-for-all

Key playable powers at 866 AG:
- **New Cauldron** — democratic mercenary republic, early Myr Cluster ambitions
- **The Elrossi Imperium** — holy, martial, expanding faith across the galaxy
- **The Gob-Ogre Trade League** — corporate empire, fifty Trade Princes, early Myr aggression
- **The Coldiron Caliphate** — faith-driven expansionists pressing into the Clusters
- **The Nikios Khanate** — recovering centaur mercenary power in Savage Space
- **Angelia** — Aasimar holy nation in the Border Systems, repelling Carrigore raids
- **The Broken Daimyos** — feuding star-city-states in their pre-Sengoku fragmentation

---

## Mod Prefix

All mod-specific identifiers use the prefix **`eotg_`** without exception.

This applies to: event namespaces, scripted effects, scripted triggers, flags, variables, decisions, traits, modifiers, cultures, religions, titles, and dynasty names.

> **Why this matters:** CK3 namespace collisions between mods are completely silent — no error is ever logged. Discipline here prevents invisible bugs.

---

## Target Version

| Field | Value |
|---|---|
| CK3 Version | `1.19.*` (Scribe) |
| Mod Version | `0.1.0` |
| Bookmark | `866 AG` — Titan Exodus era, Myr Cluster Wars igniting |
| Status | 🚧 Early Scaffolding |

---

## Repository Structure

```
echoes_of_the_grip/
├── echoes_of_the_grip.mod        ← Install this in your mod folder
├── descriptor.mod            ← Auto-used by CK3; identical but without path=
├── common/
│   ├── buildings/            ← Holding upgrades
│   ├── casus_belli_types/    ← War justifications
│   ├── character_interactions/
│   ├── coat_of_arms/
│   ├── culture/
│   │   ├── cultures/         ← eotg_ culture definitions
│   │   ├── innovations/      ← Tech tree nodes
│   │   └── pillars/          ← Ethos, heritage, language
│   ├── customizable_localization/
│   ├── decisions/            ← Player decisions
│   ├── dynasty_legacies/
│   ├── flavorization/        ← Culture/religion title name overrides (additive)
│   ├── governments/
│   ├── laws/
│   ├── men_at_arms_types/
│   ├── modifiers/            ← Static modifier definitions
│   ├── on_action/            ← Event hook registrations
│   ├── opinion_modifiers/
│   ├── religion/
│   │   ├── religions/        ← eotg_ faith/religion definitions
│   │   ├── doctrines/
│   │   └── fervor_modifiers/
│   ├── scripted_effects/     ← Reusable effect macros (eotg_se_*)
│   ├── scripted_modifiers/
│   ├── scripted_triggers/    ← Reusable trigger macros (eotg_st_*)
│   ├── script_values/        ← Computed numeric values
│   ├── story_cycles/         ← Persistent narrative structures (1.19)
│   ├── struggle/             ← Regional struggle definitions
│   └── traits/               ← eotg_ trait definitions
├── events/                   ← ALL event files live here (NOT in common/)
├── gfx/
│   ├── portraits/
│   └── interface/illustrations/
├── gui/scripted_widgets/
├── history/
│   ├── characters/           ← Starting characters per bookmark
│   ├── titles/               ← Title ownership at 1851 AG
│   └── provinces/            ← Province culture/religion/holding
├── localization/
│   └── english/
│       ├── *_l_english.yml   ← UTF-8 BOM required
│       └── replace/          ← Vanilla loc key overrides
├── music/
└── docs/                     ← Design docs, lore references, notes
```

---

## Critical Development Rules

### Events
- Events live in `events/` at the root — **never** in `common/events/` (that path does not exist in CK3).
- Events **do not auto-fire**. Every event must be called from an `on_action`, decision, interaction, or another event.
- All event namespaces must be prefixed: `eotg_`.

### Localization
- All `.yml` files must be **UTF-8 with BOM**. Files without BOM fail silently.
- Filename must end in `_l_english.yml`.
- Format: one space before each key, strings in double quotes, version counter always `:0`.

### on_action
- `on_action` `effect =` blocks **overwrite**, not append. Never add `effect = {}` directly to a vanilla on_action.
- Chain custom behaviour via `on_actions = {}` inside a custom on_action instead.

### Compatibility
- `flavorization/`, `scripted_triggers/`, `scripted_effects/`, `modifiers/`, and `localization/` are **additive** — new files sit alongside vanilla safely.
- Everything else (traits, decisions, buildings, etc.) uses **full-file override** if the same path exists in vanilla. Prefer single-object override (redefine just the key) over duplicating entire vanilla files.

---

## Tooling

| Tool | Purpose |
|---|---|
| [CK3 Tiger](https://github.com/amtep/ck3tiger) | Static validator — run before every test session |
| VSCode + CWTools | Autocomplete, scope tooltips |
| VSCode + Paradox Highlight | Syntax highlighting |
| WinMerge / KDiff3 | Diff vanilla overrides after each CK3 patch |

Run CK3 with `-debug_mode` and `-develop` flags during development.  
Check `Documents/Paradox Interactive/Crusader Kings III/logs/error.log` every session.

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for coding standards, branch conventions, and the review process.

---

## Lore & Design Documents

Internal lore docs are stored in `docs/`. These are the canonical sources for world history, nations, and characters — all scripted content should be consistent with them.

---

## License

TBD — mod assets and lore are original intellectual property of the project authors.
