# CK3 Modding Reference — Authoritative Guide for Version 1.19 "Scribe"

> **Purpose:** This document is a complete, authoritative reference for writing CK3 mod script at version 1.19. It is structured for use as a system prompt or working reference. All information has been verified against official Paradox documentation, community forum archives, OldEnt's trigger/effect logs, and the 1.19 "Scribe" open beta (released March 27, 2026).
>
> **Critical rule for all generated code:** Always prefix every mod-specific name with a unique mod tag (e.g., `mymod_`). This applies to event namespaces, scripted effects, scripted triggers, flags, variables, decisions, traits, and modifiers. Namespace collisions between mods are completely silent — no error is logged.

---

## TABLE OF CONTENTS

1. [Cardinal Rules](#1-cardinal-rules)
2. [Environment & Tooling](#2-environment--tooling)
3. [Mod Structure](#3-mod-structure)
4. [The Scripting Language](#4-the-scripting-language)
5. [Scopes](#5-scopes)
6. [Triggers](#6-triggers)
7. [Effects](#7-effects)
8. [Events](#8-events)
9. [Decisions](#9-decisions)
10. [Character Interactions](#10-character-interactions)
11. [On Actions](#11-on-actions)
12. [Story Cycles](#12-story-cycles)
13. [Scripted Effects, Triggers & Values](#13-scripted-effects-triggers--values)
14. [Traits](#14-traits)
15. [Modifiers](#15-modifiers)
16. [History Files](#16-history-files)
17. [Localization](#17-localization)
18. [Override Rules & Compatibility](#18-override-rules--compatibility)
19. [Common Folder Reference](#19-common-folder-reference)
20. [Debugging](#20-debugging)
21. [Expert Tips & Gotchas](#21-expert-tips--gotchas)
22. [1.19 "Scribe" Modding Impact](#22-119-scribe-modding-impact)
23. [Key Resources](#23-key-resources)

---

## 1. Cardinal Rules

- **Never edit base game files.** Files under `steamapps/common/Crusader Kings III/game/` are wiped on every update. All work lives in a dedicated mod folder.
- **Read `error.log` every session.** Located at `Documents/Paradox Interactive/Crusader Kings III/logs/error.log`. Silent errors compound.
- **Prefer single-object override to full file replacement.** Duplicating an entire vanilla file causes unnecessary incompatibility with other mods and future patches.
- **Events do not auto-fire.** CK3 has no MTTH system. Every event must be explicitly called from an on_action, decision, interaction, or another event. If your event never fires, the first question is: what calls it?
- **Your namespace is global and sacred.** `mymod_` prefixes everything. Two mods defining a scripted trigger named `is_powerful_ruler` will silently overwrite each other. No error is logged.
- **`on_action` `effect =` blocks overwrite, not append.** Only `events`, `random_events`, and `on_actions` sub-blocks merge additively. Adding `effect = {}` directly to a vanilla on_action silently discards the vanilla effect. Chain a custom on_action via `on_actions = {}` instead.
- **Version control from day one.** Commit after every working state. Use WinMerge or KDiff3 to diff overridden vanilla files after each patch.

### What Is and Is Not Moddable
**Via script:** events, decisions, on_actions, traits, cultures, religions, laws, buildings, titles, character interactions, modifiers, map data, GUI, localization, history files, activities, struggles, schemes, men-at-arms, dynasty legacies, story cycles, accolades, artifacts.
**Hardcoded:** core AI army logic, most pathfinding, engine rendering, fundamental game loop timing.
**Since 1.9:** Achievements no longer disabled by mods. Ironman saves unaffected.

---

## 2. Environment & Tooling

### Launch Flags
Add to Steam launch options or shortcut target:

| Flag | Effect |
|---|---|
| `-debug_mode` | Dev tooltips, console access, character debug shortcuts |
| `-develop` | Hot-reloads script files on save (GUI/map need restart) |
| `-mapeditor` | Opens the map editor |
| `-nographics` | Headless; starts observer mode |
| `-random_seed=42` | Fixed RNG seed (requires `-debug_mode`) |
| `-continuelastsave` | Auto-loads last save on launch |
| `-save_every=10` | Auto-saves every 10 years without overwriting autosaves |

### Essential Console Commands
```
script_docs           # Dumps triggers.log, effects.log, scopes.log, modifiers.log → logs/
release_mode          # Toggles live error tracker overlay in-game
charinfo              # Debug overlay on portraits (shows character IDs)
bypass_requirements   # Toggle: ignore all is_valid/cost checks for decisions/interactions
effect add_gold = 100     # Run an effect on the player character
trigger is_adult = yes    # Evaluate a trigger; returns true/false
run my_test.txt           # Execute a .txt file from Documents/.../CK3/run/ as raw script
```

> **Regenerate `script_docs` after every major patch.** The wiki trigger/effect lists go stale.

### Debug Click Shortcuts (requires `-debug_mode`)
- `Ctrl+click` — switch to character
- `Alt+click` — kill character instantly
- `Ctrl+Alt+click` — open in Explorer (live effects/triggers)

### Recommended Editors

| Editor | Key Extensions |
|---|---|
| **VSCode** (recommended) | CK3 Tiger (validator), CWTools (autocomplete + scope tooltips), Paradox Highlight |
| **Sublime Text** | CK3 Tools (official Paradox extension) |
| **Notepad++** | Set language to Perl |
| **IntelliJ IDEA** | Paradox Language Support plugin |

### CK3 Tiger — Run Before Every Test
CK3 Tiger is a static validator that catches scope errors, missing loc keys, invalid trigger/effect combinations, and undefined references before you launch the game. It catches ~80% of common errors in seconds.
- https://github.com/amtep/ck3tiger (standalone + VSCode extension)

### Hot-Loading Limits
`-develop` hot-reloads most script. But: saved scopes in open events do NOT update on hot-load; new localization keys require restart; large structural changes (new on_actions, file additions) need a clean boot. Phantom bugs from broken hot-load states are common — restart before extended debugging.

---

## 3. Mod Structure

### File Locations

| Path | Purpose |
|---|---|
| `Documents/Paradox Interactive/Crusader Kings III/mod/` | Local mods (Windows) |
| `~/.local/share/Paradox Interactive/Crusader Kings III/mod/` | Local mods (Linux) |
| `steamapps/common/Crusader Kings III/game/` | Vanilla files — READ ONLY |

### The `.mod` File
```pdx
version="1.0"
tags={ "Gameplay" }
name="My Mod Name"
supported_version="1.19.*"
path="mod/my_mod"
```
The `descriptor.mod` inside the mod folder is identical but omits `path=`. Update `supported_version` after every major patch.

### Folder Tree
```
my_mod/
├── common/
│   ├── buildings/
│   ├── casus_belli_types/
│   ├── character_interactions/
│   ├── coat_of_arms/coat_of_arms/
│   ├── culture/
│   │   ├── cultures/
│   │   ├── innovations/
│   │   └── pillars/
│   ├── customizable_localization/
│   ├── decisions/
│   ├── dynasty_legacies/
│   ├── flavorization/
│   ├── game_rules/
│   ├── governments/
│   ├── holdings/
│   ├── laws/
│   ├── men_at_arms_types/
│   ├── modifiers/
│   ├── on_action/
│   ├── opinion_modifiers/
│   ├── religion/
│   │   ├── religions/
│   │   ├── doctrines/
│   │   └── fervor_modifiers/
│   ├── scheme_types/
│   ├── script_values/
│   ├── scripted_effects/
│   ├── scripted_modifiers/
│   ├── scripted_triggers/
│   ├── story_cycles/
│   ├── struggle/
│   ├── traits/
│   └── titled_opinions/
├── events/          ← ALL event files go here — NOT in common/
├── gfx/
│   ├── portraits/portrait_modifiers/
│   └── interface/illustrations/
├── gui/
│   └── scripted_widgets/    ← Additive GUI panel registrations (safe)
├── history/
│   ├── characters/
│   ├── titles/
│   └── provinces/
├── localization/
│   └── english/
│       ├── *_l_english.yml
│       └── replace/         ← Overrides for vanilla loc keys
└── music/
```

> **Critical:** Events live in `events/` at the root. There is no `common/events/` in CK3.

---

## 4. The Scripting Language

CK3 uses "Jomini script" — a declarative, data-driven language. You describe what should happen and under what conditions, not sequential execution steps.

### Syntax
```pdx
# Comment

key = value                       # Simple pair
key = { block }                   # Block form
age >= 18                         # Numeric comparison
gold != 0
primary_heir = primary_spouse     # Scope equality (same object?)

# Safe existence check (?= operator)
capital_county ?= title:c_byzantion
# Equivalent to: exists = capital_county  +  capital_county = title:c_byzantion
# Also works as a block navigator:
scope:patron ?= { add_gold = 50 } # Skips cleanly if scope:patron is unset
```

### Database Key Access
```pdx
title:k_france       faith:catholic      religion:christianity
character:12345      culture:french      trait:brave
dynasty:1038
```

### Logic Blocks
```pdx
# AND (default — all must be true)
trigger = { is_adult = yes  is_ai = no }

OR = { has_trait = brave  has_trait = bold }
NOT = { has_trait = craven }      # Use with single child for clarity
NAND = { ... }   NOR = { ... }   # Also valid

# Conditional EFFECTS (not triggers!)
if = {
    limit = { is_adult = yes }
    add_gold = 100
}
else_if = { limit = { age >= 14 }  add_gold = 50 }
else = { add_gold = 10 }

# Conditional TRIGGERS (not effects!)
trigger_if = { limit = { is_ai = no }  is_independent_ruler = yes }
trigger_else = { gold >= 200 }
```

> **`if/else` are effects. `trigger_if/trigger_else` are triggers.** Using the wrong one in the wrong block is a silent failure — the block is skipped. CK3 Tiger catches this.

### Script Value Arithmetic
```pdx
# In common/script_values/
mymod_reward = {
    base = 50           # Starting value (0 if omitted)
    add = stewardship   # Add skill value
    multiply = 2        # Applied to running total (order matters)
    min = 100
    max = 1000
    if = { limit = { has_trait = greedy }  multiply = 0.5 }
}
add_gold = mymod_reward  # Use anywhere a number is expected
```

### Variables
```pdx
set_variable = { name = counter value = 0 }
change_variable = { name = counter add = 1 }
var:counter >= 5                          # Trigger check
exists = var:counter                      # Existence check
remove_variable = counter
set_variable = { name = buff value = yes years = 5 }  # Auto-expires

# Scoping
set_global_variable = { name = mymod_world_flag value = yes }
exists = global_var:mymod_world_flag

set_local_variable = { name = temp value = 42 }  # Current block only, fastest
local_var:temp >= 10
```

---

## 5. Scopes

A scope is the current game entity that effects act upon and triggers check. Every effect and trigger executes *within* a scope.

### Core Scope Types
| Scope | Represents |
|---|---|
| `character` | A person |
| `title` / `landed_title` | A title (barony → empire) |
| `province` | A map province |
| `faith` | A specific denomination (Catholic, Sunni) |
| `religion` | A faith group (Christianity, Islam) |
| `culture` | A culture |
| `dynasty` / `house` | Dynasty or cadet house |
| `war` / `faction` / `scheme` | Active conflict/scheme |
| `activity` / `struggle` | Activity or regional struggle |
| `army` / `combat` | Army/combat engagement |
| `none` | Null — always check `exists =` before navigating |

> **`faith` ≠ `religion`.** `faith` is the denomination (Catholic); `religion` is the group (Christianity). Character checks use `faith`. To check faith's group: `faith = { religion = religion:christianity }`.

### Scope Navigation
```pdx
# Character → related objects
liege              top_liege          employer
father             mother             real_father
primary_heir       primary_spouse
capital_county     capital_province
dynasty            house              faith            culture

# Title navigation
title:k_france.holder           # Current holder
title:k_france.previous_holder
title:c_paris.county

# Cross-scope
scope:saved_char.capital_county
```

### Keywords
| Keyword | Meaning |
|---|---|
| `root` | Scope at start of event/decision/interaction |
| `this` | Current scope (mainly useful in iterators) |
| `prev` | Previous scope in nesting stack |
| `scope:name` | Named saved scope |

### Saving Scopes
```pdx
save_scope_as = my_target                          # Persists for event lifetime
scope:my_target = { add_gold = 100 }               # Re-enter saved scope
save_temporary_scope_as = temp_target              # Exists in current block only
save_scope_value_as = { name = amount value = 500 } # Save a number
clear_saved_scope = my_target                      # Clean up when done
```

> **Premade scopes in interactions:** `scope:actor` (initiator), `scope:recipient` (target). In on_actions: check comments in `common/on_action/00_on_actions.txt`.

### List Iteration

**Prefix meanings:** `every_` (effect, all matching) · `any_` (trigger, ≥1 match) · `random_` (effect, 1 weighted) · `ordered_` (effect, sorted)

```pdx
# All matching — effect
every_vassal = { limit = { is_adult = yes }  add_prestige = 50 }

# At least one — trigger
any_vassal = { limit = { is_adult = yes }  gold >= 500 }

# Count — trigger
any_vassal = { limit = { is_adult = yes }  count >= 3 }

# Sorted selection
ordered_vassal = { order_by = gold  position = 0  max = 1  save_scope_as = richest }

# Weighted random
random_vassal = {
    limit = { is_adult = yes }
    weight = { base = 1  modifier = { add = 10  has_trait = ambitious } }
    save_scope_as = chosen
}

# Geographic/realm iteration
every_county_in_region = { region = world_europe_west  limit = { ... }  ... }
every_sub_realm_county = { limit = { ... }  ... }         # All realm counties recursively
every_directly_owned_province = { limit = { ... }  ... }  # Only personally held
every_in_de_facto_hierarchy = { limit = { tier = tier_county }  ... }
every_close_or_extended_family_member = { limit = { is_alive = yes }  ... }
every_powerful_vassal = { ... }  # Only top vassals — much cheaper than every_vassal
```

---

## 6. Triggers

Triggers return true/false. Used in `trigger = {}`, `limit = {}`, `is_shown = {}`, `is_valid = {}`, `any_` list iterators.

### Common Triggers
```pdx
# State
is_adult = yes          is_alive = yes         is_ai = yes
is_player_character = yes                      is_imprisoned = yes
is_landed = yes         is_independent_ruler = yes   is_ruler = yes
is_at_war = yes         is_incapable = yes     has_character_flag = my_flag

# Traits
has_trait = brave
has_trait_xp = { trait = knight  track = chivalry  value >= 50 }

# Skills
diplomacy >= 15    martial >= 10    stewardship >= 12
intrigue >= 8      learning >= 10   prowess >= 15

# Title tier — CORRECT syntax
highest_held_title_tier >= tier_king      # tier_baron/county/duchy/kingdom/empire
highest_held_title_tier = tier_emperor

# Relations
is_vassal_of = scope:liege
is_close_family_of = scope:other
is_spouse_of = scope:char
is_allied_to = scope:char
is_at_war_with = scope:enemy

# Titles
holds_title = title:k_france
title:k_france.holder = root

# Faith/Culture
faith = faith:catholic
culture = culture:french
faith = { religion = religion:christianity }
has_cultural_tradition = tradition:tradition_fp1_longboats

# Resources
gold >= 100    prestige >= 500    piety >= 200    stress >= 50

# Misc
age >= 18      exists = father    has_government = feudal_government
```

> **Government keys changed in 1.12+.** Always verify `government = ` keys against `common/governments/`.

### Scripted Triggers
Defined in `common/scripted_triggers/`. Additive — new definitions are added alongside existing ones.
```pdx
# Definition
mymod_is_eligible = {
    is_adult = yes   is_alive = yes   prowess >= 15
    OR = { has_trait = brave  has_trait = ambitious }
    NOT = { is_imprisoned = yes }
}

# Usage — always = yes or = no, never bare
trigger = { mymod_is_eligible = yes }
```

---

## 7. Effects

Effects modify game state. Used in `immediate = {}`, `option = {}`, `effect = {}`, `after = {}`, and interaction blocks.

### Common Effects
```pdx
# Resources
add_gold = 100
remove_short_term_gold = 50    # Debts below 0
add_prestige = 200   add_piety = 100   add_piety_level = 1
add_stress = 10      remove_stress = 20    add_health = 1

# Traits
add_trait = brave    remove_trait = craven
add_trait_xp = { trait = knight  track = chivalry  value = 100 }

# Opinion (TYPE C — see Modifiers section for disambiguation)
add_opinion = { target = scope:liege  modifier = grateful_opinion  years = 5 }
remove_opinion = { target = scope:liege  modifier = grateful_opinion }

# Titles
give_title = { title = title:c_paris  recipient = scope:char }
remove_title = { holder = root  title = title:c_paris }

# Imprisonment/Death
imprison = { target = scope:prisoner  type = dungeon }   # dungeon | house_arrest
release_from_prison = scope:prisoner
kill_character = scope:char

# Create character
create_character = {
    location = title:c_paris.title_province
    age = 25    gender = male
    faith = faith:catholic    culture = culture:french
    save_scope_as = new_char
}

# Modifiers
add_character_modifier = { modifier = mymod_blessed  years = 10 }
remove_character_modifier = mymod_blessed

# Events
trigger_event = { id = mymod.0001  days = 7 }
trigger_event = { id = mymod.0001  days = { 5 15 } }   # Random range
trigger_event = { id = mymod.0001  delayed = yes }       # Next tick, ASAP

# Flags
set_character_flag = { flag = my_flag  years = 5 }
set_character_flag = my_flag    # Permanent
remove_character_flag = my_flag
```

### Tooltip Control — Always Use These
```pdx
# Suppress tooltip for internal bookkeeping
hidden_effect = {
    set_character_flag = tracking_flag
    add_stress = 10     # Player won't see this in option tooltip
}

# Show custom text instead of raw mechanics
custom_tooltip = mymod_effect_description_key
# Follow with actual effects, often in hidden_effect

# Full wrapper — replaces ALL tooltip text with one custom line
custom_description = {
    text = mymod_grant_power_tooltip
    subject = scope:target
    add_prestige = 500   add_trait = brave   # Run silently
}

# Show effects in tooltip even if they fire later via a follow-up event
show_as_tooltip = { add_gold = 100 }
```

> **`hidden_effect` is not optional polish.** Without it, every flag set and tracking variable modified clutters the player's option tooltip with mechanical noise.
> **`cost =` deducts automatically.** Never also manually `add_gold = -200` in the effect block — that double-charges the player.

### Control Flow Effects
```pdx
# switch — branch on a single trigger (replaces long if/else_if chains)
# Note: trigger_switch from CK2 does NOT exist. Use switch.
switch = {
    on_trigger = has_trait
    brave = { add_prestige = 200 }
    craven = { add_stress = 50 }
    fallback = { add_prestige = 50 }   # Required — always include fallback
}

# random — percentage chance
random = {
    chance = 25
    modifier = { add = 15  has_trait = lucky }
    add_prestige = 200
}

# random_list — pick ONE weighted outcome
random_list = {
    50 = { add_gold = 200 }
    25 = { add_trait = brave  add_prestige = 500 }
    25 = {
        trigger = { is_adult = yes }   # Excluded from pool if false
        add_stress = 30
    }
}
# Weights are relative, not percentages. Pool excludes entries with false triggers.

# while — loop until condition is false (max 1000 iterations)
while = { limit = { var:counter < 5 }  change_variable = { name = counter  add = 1 } }
while = { count = 3  add_prestige = 100 }   # Fixed iterations
```

### Personality-Reactive Stress
```pdx
# Always prefer stress_impact over bare add_stress for personality-driven options
stress_impact = {
    base = minor_stress_impact_gain     # Always applied
    brave = minor_stress_impact_loss    # Brave chars lose stress instead
    craven = major_stress_impact_gain   # Craven chars suffer more
    greedy = medium_stress_impact_gain
}
# Constants: no_stress_impact, minor/medium/major/massive_stress_impact_gain/loss
```

### Skill-Based Outcomes
```pdx
# duel — the standard system for skill-scaled weighted outcomes
duel = {
    skill = martial
    target = scope:opponent
    # scope:duel_value = actor_skill - opponent_skill (typically -20 to +20)
    # scope:duel_target = opponent character

    50 = {  # Victory — weight up when actor wins (duel_value positive)
        compare_modifier = { value = scope:duel_value  multiplier = 0.5 }
        add_prestige = 500
    }
    50 = {  # Defeat — weight up when opponent wins (duel_value negative)
        compare_modifier = { value = scope:duel_value  multiplier = -0.5 }
        add_stress = 30
    }
}
# Using 0.5 on win and -0.5 on loss creates a linear 0–100% probability gradient.
```

### Notifications
```pdx
send_interface_message = {
    type = default_message_type
    title = mymod_title_key
    desc = mymod_desc_key
    left_icon = scope:character
    right_icon = title:k_france
    goto = title:k_france        # Adds navigation button
    add_prestige = 100           # Optional effects
}

send_interface_toast = {
    type = default_message_type
    title = mymod_toast_key
    left_icon = root
}
```

### Character Memories
```pdx
create_character_memory = {
    type = mymod_battle_memory   # Defined in common/character_memory_types/
    participants = { enemy = scope:foe  ally = scope:knight }
    duration = { years = 10 }    # Omit for permanent
}
has_character_memory_type = mymod_battle_memory   # Trigger
every_memory = { limit = { has_memory_type = mymod_battle_memory }  ... }
```

### Opinion Value Capture
```pdx
save_opinion_value_as = { name = vassal_loyalty  target = scope:vassal }
if = { limit = { scope:vassal_loyalty >= 50 }  add_prestige = 300 }
```

---

## 8. Events

All event files live in `events/` at the mod root. Each file has one namespace.

### Full Anatomy
```pdx
namespace = mymod   # Global — unique per mod, prefix with mod tag

mymod.0001 = {
    type = character_event   # See event types below
    hidden = no              # hidden = yes: fires silently, no popup window
    cooldown = { years = 5 } # Auto-manages re-fire blocking (replaces manual flag guards)

    title = mymod_0001_title

    # desc patterns — always use first_valid
    desc = {
        first_valid = {
            triggered_desc = { trigger = { has_trait = brave }  desc = mymod_desc_brave }
            triggered_desc = { trigger = { has_trait = craven }  desc = mymod_desc_craven }
            desc = mymod_desc_default   # Bare desc = always valid; put last as fallback
        }
        # random_valid = { ... }  — picks randomly from all true entries
    }

    theme = war   # Controls background art

    # Portraits: left_portrait, right_portrait, lower_left_portrait, lower_right_portrait
    left_portrait = {
        character = root
        triggered_animation = {        # first_valid-style animation selection
            trigger = { has_trait = brave }
            animation = aggressive_sword
        }
        animation = personality_rational   # Fallback
    }
    right_portrait = {
        character = scope:antagonist
        animation = anger
        # outfit_tags = { soldier_outfit }
    }

    # Guard — event cancels silently if this becomes false before firing
    trigger = {
        is_adult = yes
        is_at_war = yes
        NOT = { has_character_flag = mymod_war_fired }
    }

    # Runs before player sees the event
    immediate = {
        set_character_flag = mymod_war_fired
        random_war_enemy = {
            limit = { is_alive = yes }
            save_scope_as = antagonist
        }
    }

    # Options
    option = {
        name = mymod_opt_a
        trigger = { gold >= 100 }   # Option hidden if false (not greyed out)
        add_gold = -100
        add_prestige = 200
        custom_tooltip = mymod_opt_a_tooltip
        hidden_effect = { set_character_flag = mymod_chose_fight }
        add_internal_flag = special         # Yellow highlight (no gameplay effect)
        # add_internal_flag = dangerous     # Red highlight
        highlight_portrait = scope:antagonist
        skill = martial                      # Flavor skill icon
        ai_chance = {
            base = 60
            modifier = { add = 20   has_trait = greedy }
            modifier = { add = -30  gold < 100 }
        }
    }

    option = {
        name = mymod_opt_b
        stress_impact = {
            base = minor_stress_impact_gain
            brave = minor_stress_impact_loss
        }
        show_as_tooltip = { add_gold = 50 }
        hidden_effect = { trigger_event = { id = mymod.0002  days = 7 } }
        ai_chance = { base = 40 }
    }

    # Fallback — shown only if no other options pass their triggers
    option = {
        name = mymod_opt_fallback
        trigger = { always = no }
        fallback = yes
        add_stress = 5
    }

    # Runs after any option is chosen
    after = {
        hidden_effect = { }
    }
}
```

### Event Types
| Type | Scope | Notes |
|---|---|---|
| `character_event` | character | Standard popup |
| `court_event` | character | Player's court setting |
| `province_event` | province | Province scope |
| `letter_event` | character | Letter/scroll visual |
| `fullscreen_event` | character | Full-screen art takeover |
| `activity_event` | character | During activities |
| `duel_event` | character | Provides `scope:duel_value`, `scope:duel_target` |
| `empty` | none | No root scope — for pure effect events |

### Event Themes
`war`, `diplomacy`, `intrigue`, `learning`, `stewardship`, `faith`, `marriage`, `pregnancy`, `illness`, `death`, `travel`, `activity`, `default`

> Check `gfx/interface/illustrations/event_scenes/` in vanilla for complete list.

---

## 9. Decisions

Defined in `common/decisions/`. Appear in the character decision panel.

```pdx
mymod_my_decision = {
    picture = "gfx/interface/illustrations/decisions/decision_misc.dds"
    major = yes              # major decisions panel; no = minor list
    ai_check_interval = 60   # Months between AI evaluations

    is_shown = {             # When to show at all
        is_adult = yes
        is_landed = yes
    }

    is_valid = {             # When it can be taken (greyed out if false)
        gold >= 200
        prestige >= 500
        NOT = { has_character_flag = mymod_took_decision }
    }

    is_valid_showing_failures_only = {
        gold >= 200
        prestige >= 500
    }

    cost = {                 # Auto-deducts AND displays in tooltip
        gold = 200           # Do NOT also manually deduct in effect block
        prestige = 500
    }

    effect = {
        set_character_flag = mymod_took_decision
        trigger_event = { id = mymod.2001 }
        custom_tooltip = mymod_decision_tooltip
    }

    ai_potential = { always = yes }
    ai_will_do = {
        base = 10
        modifier = { add = 40   has_trait = ambitious }
        modifier = { add = -10  gold < 300 }
    }
}
```

---

## 10. Character Interactions

Defined in `common/character_interactions/`. Right-click actions between two characters. Always use `scope:actor` (initiator) and `scope:recipient` (target) — never `root`.

```pdx
mymod_pledge_alliance = {
    category = interaction_category_diplomacy
    icon = icon_alliance

    is_shown = {
        scope:actor = { is_landed = yes }
        scope:recipient = { is_landed = yes }
        NOT = { scope:actor = { is_allied_to = scope:recipient } }
    }

    can_send = {
        scope:actor = { gold >= 50 }
        scope:recipient = { is_adult = yes }
    }

    can_send_showing_failures_only = {
        scope:actor = { gold >= 50 }
    }

    send_cost = { gold = 50 }

    auto_accept = no

    on_accept = {
        scope:actor = { add_prestige = 100 }
        scope:recipient = { add_prestige = 100 }
    }

    on_decline = {
        scope:actor = {
            add_opinion = { target = scope:recipient  modifier = disrespected_opinion }
        }
    }

    ai_potential = { scope:actor = { is_ai = yes } }
    ai_will_do = {
        base = 10
        modifier = { add = 30  scope:actor = { has_trait = gregarious } }
    }
    ai_accept = {
        base = 0
        modifier = {
            add = 30
            scope:recipient = { opinion = { target = scope:actor  value >= 30 } }
        }
    }
}

run_interaction = {
    interaction = mymod_pledge_alliance
    actor = root
    recipient = scope:target
    send_threshold = accept
    execute_threshold = maybe
}
```

---

## 11. On Actions

Defined in `common/on_action/`. **Partially additive** — read this table before writing anything here.

### What IS and IS NOT Additive
| Field in an on_action block | Behaviour |
|---|---|
| `events = { }` | **Additive** — your events appended |
| `random_events = { }` | **Additive** — entries appended |
| `on_actions = { }` | **Additive** — your chains appended |
| `effect = { }` | **OVERWRITES** — only one kept per on_action |
| `trigger = { }` | **OVERWRITES** — same as effect |

**The correct pattern for adding effects:**
```pdx
on_death = {
    on_actions = { mymod_on_death_handler }
}

mymod_on_death_handler = {
    effect = {
        every_close_family_member = { add_stress = 10 }
    }
}
```

### Recommended Pulses for Mod Events

| On Action | Fires For | Notes |
|---|---|---|
| `random_yearly_playable_pulse` | Count+ playable chars, once/year, staggered | **Best default for mod events** |
| `random_5_year_pulse` | Per character, ~every 5 years | For infrequent heavy checks |
| `quarterly_playable_pulse` | Playable chars, every 3 months | More frequent but still targeted |
| `on_yearly_pulse` | Every living character | Expensive — use sparingly |
| `on_monthly_pulse` | Every living character, monthly | Very expensive — avoid for events |

```pdx
random_yearly_playable_pulse = {
    on_actions = { mymod_yearly_handler }
}

mymod_yearly_handler = {
    random_events = {
        100 = mymod.3001
        50 = mymod.3002
        10 = { event = mymod.3003  weight_multiplier = { base = 1  modifier = { add = 2  has_trait = ambitious } } }
        0 = mymod.3004
    }
}
```

### Other Common Hooks
```pdx
on_death = { on_actions = { mymod_death_handler } }
on_birthday = { events = { mymod.3005 } }
on_war_ended_victory = { events = { mymod.3006 } }
on_title_gain = { events = { mymod.3007 } }
on_birth = { events = { mymod.3008 } }
on_game_start_after_lobby = { on_actions = { mymod_startup } }
```

---

## 12. Story Cycles

Persistent multi-stage narrative structures. Defined in `common/story_cycles/`.

```pdx
mymod_quest = {
    on_setup = {
        set_variable = { name = mymod_quest_stage  value = 1 }
        trigger_event = { id = mymod_story.0001 }
    }

    on_monthly = {
        events = { mymod_story.0002 }
    }

    should_end = {
        OR = {
            has_character_flag = mymod_quest_complete
            NOT = { is_alive = yes }
        }
    }

    on_end = {
        if = {
            limit = { has_character_flag = mymod_quest_complete }
            add_prestige = 500
        }
    }
}

start_story = { story_cycle = mymod_quest }
end_story = yes
story = { set_variable = { name = quest_stage  value = 2 } }
```

---

## 13. Scripted Effects, Triggers & Values

### Scripted Effects
```pdx
mymod_reward = {
    add_gold = 200
    add_prestige = 100
    add_trait = content
}
mymod_reward = yes

mymod_transfer_gold = {
    $GIVER$ = { save_scope_as = giver }
    $RECEIVER$ = { save_scope_as = receiver }
    save_scope_value_as = { name = amount  value = $AMOUNT$ }
    scope:giver = { remove_short_term_gold = scope:amount }
    scope:receiver = { add_gold = scope:amount }
    clear_saved_scope = giver
    clear_saved_scope = receiver
}
mymod_transfer_gold = { GIVER = root  RECEIVER = scope:ally  AMOUNT = 500 }
```

### Scripted Triggers
```pdx
mymod_is_eligible = {
    is_adult = yes   is_alive = yes   prowess >= 15
    OR = { has_trait = brave  has_trait = ambitious }
}
trigger = { mymod_is_eligible = yes }
```

### Scripted Values
```pdx
mymod_battle_reward = {
    base = 10
    add = { value = martial  multiply = 0.5 }
    if = { limit = { has_trait = brilliant_strategist }  add = 25 }
    min = 5   max = 500
}
add_prestige = mymod_battle_reward
```

---

## 14. Traits

```pdx
mymod_blessed = {
    category = virtue

    character_modifier = {
        monthly_piety_gain_mult = 0.1
        diplomacy = 2
        health = 0.5
    }

    opposites = { craven  zealous }

    track = {
        id = devotion
        xp_per_level = 100
        level_bonus = {
            character_modifier = { monthly_piety_gain_mult = 0.1 }
        }
    }

    is_valid = { NOT = { has_trait = zealous } }

    ai_honor = 1    ai_energy = 0    ai_zeal = 2
    ruler_designer_cost = 10
}
```

> **Note on 1.19:** `infirm` is now the first tier of a tiered Elder Trait system. New traits: `faltering_heart`, `fragile_bones`, `clouded_eyes`, `withering_mind`. Check vanilla before using `has_trait = infirm` as a terminal condition.

---

## 15. Modifiers

> ⚠️ **"Modifier" refers to three unrelated things in CK3.**
>
> | Type | What | Where | How |
> |---|---|---|---|
> | **Static modifier** | Named stat bundle | `common/modifiers/` | `add_character_modifier = { modifier = key }` |
> | **Weight modifier** | Inline weight adjustment | Inside `random`, `ai_will_do` | `modifier = { add = X  condition }` |
> | **Opinion modifier** | Named opinion change | `common/opinion_modifiers/` | `add_opinion = { modifier = key  target = X }` |

### Static Modifiers
```pdx
mymod_war_hardened = {
    icon = martial_positive
    martial = 3
    prowess = 2
    monthly_prestige_gain_mult = 0.1
    tax_mult = -0.1
}

add_character_modifier = { modifier = mymod_war_hardened  years = 5 }
add_county_modifier = { modifier = mymod_prosperous  years = 10 }
remove_character_modifier = mymod_war_hardened
has_character_modifier = mymod_war_hardened
```

### Opinion Modifiers
```pdx
add_opinion = { modifier = grateful_opinion  target = scope:helper  years = 5 }
add_opinion = { modifier = eternal_debt_opinion  target = scope:creditor }
remove_opinion = { modifier = grateful_opinion  target = scope:helper }
```

---

## 16. History Files

### Character History
```pdx
12345 = {
    name = "Harald"
    dynasty = dynasty:1038
    religion = faith:norse_pagan
    culture = culture:norse
    father = 12340   mother = 12341

    867.1.1 = { birth = yes }
    885.3.15 = {
        add_trait = brave
        give_title = { title = title:k_norway }
    }
    900.1.1 = { death = { death_reason = death_combat  killer = 12350 } }
}
```

### Title History
```pdx
k_england = {
    867.1.1 = {
        holder = 12400
        government = feudal_government
        succession_laws = { confederate_partition_succession_law }
    }
    1066.10.14 = { holder = 12500 }
}
```

### Province History
```pdx
1 = {
    culture = culture:english
    religion = faith:catholic
    holding = castle_holding
}
```

---

## 17. Localization

### File Rules
- Location: `localization/english/`
- Filename: must end in `_l_english.yml`
- Encoding: **UTF-8 with BOM** — mandatory. Files without BOM fail silently.
- Override vanilla keys: place files in `localization/english/replace/`

### YAML Format
```yaml
l_english:
 mymod_title:0 "A Crisis of War"
 mymod_desc:0 "The enemy stands at the gates, and [ROOT.GetFirstName] must decide."
 mymod_opt_a:0 "Spend gold to bolster the defenses"
```

### Formatting Codes
```
[ROOT.GetFirstName]       [ROOT.GetFullName]        [ROOT.GetTitledFirstName]
[ROOT.GetHerHis]          [ROOT.GetSheHe]            [ROOT.GetHerHim]
[scope:char.GetFirstName]
[ROOT.GetFirstName|U]     # Uppercase first letter
£gold£  £prestige£  £piety£  £stress£  £martial£  £diplomacy£
#bold text#
```

### Flavorization
```pdx
mymod_king_french = {
    type = character
    gender = male
    special = holder
    tier = kingdom
    priority = 110
    cultures = { french }
}
```

### Customizable Localization
```pdx
mymod_ruler_title = {
    type = character
    text = {
        trigger = { is_female = yes  highest_held_title_tier = tier_kingdom }
        localization_key = mymod_ruler_queen
    }
    text = {
        trigger = { is_female = no  highest_held_title_tier = tier_kingdom }
        localization_key = mymod_ruler_king
    }
    text = { localization_key = mymod_ruler_default }
}
```

---

## 18. Override Rules & Compatibility

| System | Behaviour |
|---|---|
| `events/` namespace entries | Additive |
| `common/on_action/` events/random_events/on_actions | Additive |
| `common/on_action/` effect/trigger keys | **Overwrites** |
| `common/scripted_triggers/` | Additive |
| `common/scripted_effects/` | Additive |
| `common/script_values/` | Additive |
| `common/modifiers/` | Additive |
| `localization/` keys | Additive |
| `common/defines/` | Per-key override |
| Everything else | **Full file override if same path** |

### Compatibility Practices
- Prefix everything.
- Override single objects, not whole files.
- After each patch: run CK3 Tiger, diff vanilla overrides, regenerate `script_docs`.

---

## 19. Common Folder Reference

| Folder | Contents |
|---|---|
| `common/buildings/` | Holding building upgrades |
| `common/casus_belli_types/` | War justification types |
| `common/character_interactions/` | Right-click interactions |
| `common/coat_of_arms/` | CoA definitions |
| `common/culture/cultures/` | Culture definitions |
| `common/culture/innovations/` | Cultural innovations |
| `common/culture/pillars/` | Ethos, heritage, language pillars |
| `common/customizable_localization/` | Dynamic in-text conditionals |
| `common/decisions/` | Character decisions |
| `common/defines/` | Global numeric constants |
| `common/dynasty_legacies/` | Dynasty perk trees |
| `common/flavorization/` | Culture/religion-based title names |
| `common/governments/` | Government type definitions |
| `common/laws/` | Succession and realm laws |
| `common/men_at_arms_types/` | Regiment type definitions |
| `common/modifiers/` | Static modifier definitions |
| `common/on_action/` | Event hook definitions |
| `common/opinion_modifiers/` | Opinion modifier definitions |
| `common/religion/doctrines/` | Doctrine definitions |
| `common/religion/religions/` | Religion and faith definitions |
| `common/script_values/` | Computed numeric values |
| `common/scripted_effects/` | Reusable effect macros |
| `common/scripted_triggers/` | Reusable trigger macros |
| `common/story_cycles/` | Persistent narrative structures |
| `common/struggle/` | Regional struggle definitions |
| `common/traits/` | Trait definitions |
| `events/` | **All event files** |
| `gfx/interface/` | UI textures and icons (.dds) |
| `gfx/portraits/` | Portrait asset definitions |
| `gui/scripted_widgets/` | **Additive** mod GUI panels |
| `history/characters/` | Starting characters per bookmark |
| `history/titles/` | Title ownership per date |
| `history/provinces/` | Province starting data |
| `localization/english/` | English text strings |
| `localization/english/replace/` | Vanilla loc key overrides |
| `map_data/` | Province IDs, terrain, rivers |
| `music/` | Music track definitions |

---

## 20. Debugging

### Error Log
`Documents/Paradox Interactive/Crusader Kings III/logs/error.log` — overwritten on launch. Check immediately when something breaks.

```
[error] Could not find type <X>        → Undefined key reference
[error] Unexpected token               → Syntax error / mismatched brace
[error] Script error in <file>:<line>  → Go directly to that line
[error] Invalid scope                  → Effect/trigger on wrong scope type
[warning] Missing localization key     → Raw key shown in game
```

### Script Documentation Logs
Run `script_docs` in-game console. Generates in `logs/`: `triggers.log`, `effects.log`, `modifiers.log`, `scopes.log`. **Regenerate after every major patch.**

### Debug Effects
```pdx
debug_log = "mymod: reached branch A"
debug_log_scopes = yes
debug_trigger_event = { id = mymod.0001 }
```

### Common Mistakes

| Symptom | Cause | Fix |
|---|---|---|
| Event never fires | Nothing calls it | Check "what calls it?" |
| Option missing | Option `trigger` fails | Check scope; test in console |
| Localization raw key | Not UTF-8+BOM; wrong filename | Re-save with BOM |
| Game crash on load | Brace mismatch | Run CK3 Tiger |
| `effect = {}` does nothing | Overwritten by vanilla | Chain via `on_actions = {}` |
| Double cost deducted | Both `cost` and manual deduction | Remove manual deduction |
| `switch` silently skips | No `fallback` | Always include `fallback` |

---

## 21. Expert Tips & Gotchas

- **`immediate` fires for AI too.** Wrap player-only code: `if = { limit = { is_player_character = yes } ... }`
- **`trigger = {}` on an event is a re-evaluation guard.** If it becomes false before the event fires, the event is silently cancelled.
- **`after` does not run if the event is force-closed.**
- **Opinion modifiers require a definition.** Invented keys in `add_opinion` silently do nothing.
- **Always `exists =` before navigating unset scopes.** `father`, `liege`, `spouse` can be unset.
- **Flags vs variables.** Flags = fast boolean. Variables = numeric/expiring. Use flags for on/off tracking.
- **`random_events` weights are not percentages.** Weight 0 disables an entry.
- **`.dds` format matters.** UI icons: DXT1. Portrait modifiers: DXT5. Wrong format = black boxes.
- **`gui/` overrides break every patch.** Use `gui/scripted_widgets/` for new panels instead.
- **`every_living_character` causes late-game freezes.** Use scoped alternatives.
- **`on_monthly_pulse` fires for every character.** Use `random_yearly_playable_pulse` by default.
- **Namespace collisions are completely silent.** Prefix everything.

---

## 22. 1.19 "Scribe" Modding Impact

### Breaking Changes
- **Domain limit** no longer from Stewardship — now from Education trait tiers.
- **`infirm` trait** reworked into tiered Elder Trait system. New traits: `faltering_heart`, `fragile_bones`, `clouded_eyes`, `withering_mind`.
- **Accolades system** completely reworked — old primary/secondary model replaced.
- **Event frequency drastically reduced.** Travel events: 1-in-5 → 1-in-20. Coming of Age: now only heirs and oldest children.
- **Event Nameplates UI overlay added.** Mods overriding core event GUI files may conflict.

### New Systems Available
- **Stories system** — UI-visible tracker in Situations tab for long-running chains.
- **Tiered Elder Traits** — new canonical pattern for degrading traits.
- **Knight Permissions** — new scripted filter for knight eligibility.
- **`PatternColorOverrides` increased to 64** (from 16).

---

## 23. Key Resources

### Official Documentation
- CK3 Wiki — Event Modding: https://ck3.paradoxwikis.com/Event_modding
- CK3 Wiki — Scripting: https://ck3.paradoxwikis.com/Scripting
- CK3 Wiki — Effects: https://ck3.paradoxwikis.com/Effects
- CK3 Wiki — Triggers: https://ck3.paradoxwikis.com/Triggers
- CK3 Wiki — Scopes: https://ck3.paradoxwikis.com/Scopes
- CK3 Wiki — Mod Structure: https://ck3.paradoxwikis.com/Mod_structure
- CK3 Wiki — Localization: https://ck3.paradoxwikis.com/Localization
- CK3 Wiki — Story Cycles: https://ck3.paradoxwikis.com/Story_cycles_modding

### Tools
- CK3 Tiger (validator): https://github.com/amtep/ck3tiger
- CK3 Tiger VSCode Extension: https://marketplace.visualstudio.com/items?itemName=unlomtrois.ck3tiger-for-vscode
- CWTools VSCode Extension: https://marketplace.visualstudio.com/items?itemName=tboby.cwtools-vscode
- WinMerge: https://winmerge.org/

### Community
- OldEnt Trigger/Effect History: https://github.com/OldEnt/crusader-kings-3-triggers-modifiers-effects-event-scopes-targets-on-actions-code-revisions-list
- CK3 Modding Discord: https://discord.com/invite/apEvxDZ
- Paradox Forums — CK3 User Mods: https://forum.paradoxplaza.com/forum/forums/crusader-kings-iii-user-mods.1080/

---

*Targets CK3 version 1.19 "Scribe". After any major patch: regenerate `script_docs`, re-run CK3 Tiger, diff all vanilla overrides.*
