# Feasibility: custom races, ancestry-based inheritance and heritage groups

2026-10-25. Research by four read-only investigations:
- vanilla heritage pillars;
- vanilla inheritance mechanics;
- the repo and lore;
- an observational survey of other mods (technique only, never a source; §11).

Game: CK3 **1.20.1.1**. G = `D:/SteamLibrary/steamapps/common/Crusader Kings III/game`. **V** = verified in vanilla files, **I** = inferred, **T** = needs an in-game test. Nothing has been built.

## The idea

- Custom races, each with its own heritage(s).
- Races **don't hybridize**: every character is exactly one race.
- A child's race is a **% chance based on ancestry**, so a long-mixed lineage can throw either race.
- **Heritage groups** gather the cultures of one race, so race-specific events can target a whole group.

## Verdict

**Feasible.** The engine gives us every building block. None of it is a vanilla feature, so each piece is our own script.

| Piece | Vanilla support | How |
|---|---|---|
| Heritage groups | None built in (**V**: no heritage or language family exists in 1.20.1.1) | A custom **parameter** on each heritage pillar, read with `has_cultural_parameter` (**I**, **T1**) |
| One race per character | Genetic traits can't do it (**V**) | Mutually exclusive, non-genetic **race traits** |
| Ancestry-weighted roll | None | **Ancestry-share variables** plus a weighted roll at birth |
| Race-specific events | Vanilla already gates on heritage (**V**) | Trigger on the race trait, the heritage group, or both |
| No cross-race hybrid cultures | Hybridization runs through overridable scripted triggers (**V**) | Override the hybrid check to refuse cross-group pairs |
| Race appearance | Trait-driven portrait modifiers exist (**V**) | Trait portrait modifiers plus culture ethnicities |

## 1. Heritage groups

- **Vanilla has no group above heritage.**
  - Heritages are `type = heritage` pillars in `G/common/culture/pillars/00_heritage.txt`.
  - `(heritage|language)_(family|group)` matches nothing in vanilla.
  - Vanilla "groups" are ad hoc OR lists, e.g. `00_combat_traditions.txt:245-246`.
- **Our route: a group parameter on each heritage pillar.**
  - Give every heritage pillar of a race a parameter, e.g. `parameters = { eotg_heritage_group_elven = yes }`.
  - Then a check reads `culture = { has_cultural_parameter = eotg_heritage_group_elven }`.
  - **Why it should work:** `_pillars.info` says pillars share the cultural-trait structure, and `_cultural_traits.info:61-66` documents `parameters`. Vanilla already uses parameters on its ethos and martial-custom pillars.
  - **Not yet proven on a heritage pillar (T1).** If it fails, fall back to a scripted trigger per group that lists its heritages, which is vanilla's own idiom.
- **Wrap each group in a scripted trigger,** e.g. `eotg_is_heritage_group_elven = yes`, so events never name heritages directly. This keeps the event layer map-agnostic.

## 2. Races as traits, chosen by ancestry

**Why traits, not heritage alone.** Heritage belongs to the **culture**, and a character's culture can change: by conversion, by marriage, or by moving courts. If race lived only in culture, a Myr raised at a human court would "become human" (§11). A **trait** stays with the person. Heritage groups still describe which cultures belong to which race. A character's race and their culture's group can then differ, which is intended: an elf born into a human culture.

**Why not genetic traits** (**V**, `_traits.info:86-90, 126-128`):
- Genetic traits inherit per trait: 100% from an active parent, 50% from an inactive one.
- They can't take `inherit_chance`.
- They can't force "exactly one of N", or weight by ancestry.
- `opposites` stops a character holding two of them, but doesn't choose which one.

**The design** (scripted; every hook exists, **V**):
1. **Race traits.** One non-genetic trait per race, e.g. `eotg_race_human` and `eotg_race_elf`. They are mutual `opposites` and share a `group`, so `has_trait = <group>` means "has any race".
2. **Ancestry shares.** Each character stores one variable per race, e.g. `var:eotg_race_share_elf = 0.25`. The shares sum to 1.
3. **At birth,** in an additive `on_birth_child` hook (invariant 4):
   - Scopes: `scope:child`, `scope:mother` and `scope:real_father` (**V**, `child_birth_on_actions.txt:855-860`). Use `on_birth_child`, not `on_birth_mother`, which skips historical pregnancies (:9-11).
   - Set each share on the child to the average of the mother's and the real father's (vanilla variable math, **V**).
   - Roll one race weighted by those shares, using `random_list` with `modifier = { add = … }` weights (**I**).
   - Add that race's trait. The child keeps the full share profile, so a quarter-elf lineage carries forward even when it rolls human.
4. **Engine-generated characters** (pool, guests, court populator, mercenaries, script):
   - `on_character_created` fires for all of them, with `scope:creation_reason` (**V**, `character_created_on_actions.txt:1-17`).
   - Assign a race and set shares to 100% of the culture's group.
   - This is the gap trait-based race mods kept patching (§11).
5. **History and bookmark characters.** Set race and shares at game start, either from their culture group or from history. Test whether `on_character_created` also fires for history and ruler-designer characters (T2).
6. **Missing data.** If either parent has no shares (an old save or an edge case), treat that parent as 100% of their race trait.

**Cost:** one effect per birth and no global loops, so this is cheap.

## 3. Race-specific events

- **By person:** gate on the race trait, `has_trait = eotg_race_elf`.
- **By culture:** gate on the heritage group for culture-level content, such as an elven court, an elven realm or a Shoal's population, with `culture = { has_cultural_parameter = … }`. County and province scopes can read culture too.
- **Combined:** for example, an elf ruling a human realm.
- **Vanilla precedent (V):** `coronation_events_1.txt:9623-9635` uses `has_cultural_pillar = heritage_chinese` and similar. `culture_emergence_events.txt:35,137` uses `has_same_culture_heritage`.
- **Invariant 5 applies:** every flavour event moves its system's resource. Race events need a resource of their own, or have to ride on an existing system.

## 4. Keeping races and cultures from mixing

| Route | Block it? | How |
|---|---|---|
| Hybrid cultures | Yes | Override `is_valid_for_hybridising_trigger` (`00_cultural_triggers.txt:473-477`). It is wrapped by `can_hybridize_culture_trigger` (:517) and the scripted rule `can_hybridize_culture` (`00_rules.txt:899-904`). The AI path is a code trigger (`00_culture_interactions.txt:141-152`) that likely routes through the same rule (**I**, **T3**). |
| Divergent cultures | Yes | Use `is_shown` on our heritage pillars to limit the choice to the same group. |
| Event-created hybrids | Yes, in our own script | `create_hybrid_culture` bypasses the UI check, so our events must test the group first. |
| Children | Already handled | The roll gives one race. |
| Fertility between races (optional) | Partly | `can_have_children_with` is an overridable scripted trigger (`00_marriage_triggers.txt:66-68`), and trait fertility modifiers exist. No pair-based conception block found. |
| Marriage between races (optional) | Yes | `could_marry_character_trigger` and `can_marry_common_trigger` are overridable, and marriage `ai_will_do` can weigh by trait. |

## 5. Appearance

- **Trait portrait modifiers (V).** `gfx/portraits/trait_portrait_modifiers/` takes `traits = { … }` and `dna_modifiers` (`_trait_modifier.info:1-17`). `portrait_modifiers` can gate morphs and accessories on a trait (`00_animation_expressions.txt:42-66`, `has_trait = dwarf`). So a race trait can drive ears, skin and build.
- **Culture ethnicities** set the base look for characters generated in that culture.
- **Children's DNA blends from both parents** (**V**, genes `blend_range`). A race overlay sits on top of the blend. Whether that looks right, or a separate body is needed (a new portrait type, or an inheritable race morph gene, §11), is an art question.
- **Your near-complete race:** I couldn't find it in the repo, the mod folders, the Desktop or Downloads. Where it is decides how much of the portrait work is already done.

## 6. Canon tension: canon has hybrids

| Hybrid | Source |
|---|---|
| Xerxes is half elf, half human | SETTING LORE errata |
| The Old Xerxes population is half-elven | `MYR_CLUSTER_WARS_866_THEATRE.md:170-177` |
| Half-Orcs are a playable race | `SETTING LORE:578-590` |
| Half-giants | `D7D_CAMPAIGN_ARCHIVE_CATALOG.md:189` |

Options:
1. **Half-races are their own races,** e.g. a "half-elf" race with its own heritage group. A human × elf pairing could add a share of it.
2. **Canon exceptions only.** Named characters and existing populations keep their half-race; new births never produce one.
3. **Revise the canon.**

## 7. Map-agnostic rule and timing

- **The race mechanics can be built now.** Traits, shares, the birth roll, the creation hook, the hybrid block and the portrait hooks use no title, culture or faith key. They can be built and tested on the temporary map with test races, as was done for cybernetics and the governments.
- **The heritage groups have to wait.** They need real heritages and cultures, which are blocked by B-CULTURES (Gate 1/2). The intake briefs mark every culture "Human", and Q-C1 is still open with the vault.
- **This would unblock two parked items:**
  - CB-17, cybernetics culture reactions, which asks for "pillars, not culture keys";
  - CB-48, the knight term by culture.

## 8. In-game proofs before building at scale

| ID | What | Why |
|---|---|---|
| T1 | A custom `parameters` entry on a heritage pillar is readable with `has_cultural_parameter` | The heritage-group mechanism (the fallback is OR-list triggers) |
| T2 | `on_character_created` fires for ruler-designer and history characters | Whether game start needs its own pass |
| T3 | AI culture hybridization respects the overridden scripted rule | Whether cross-race hybrid cultures can be fully blocked |
| T4 | A race trait added in `on_birth_child` shows on the first portrait, and the order relative to the engine's genetic roll | Whether race looks apply from birth |

## 9. Decisions for you

1. **Canon hybrids:** option 1, 2 or 3 in §6?
2. **Where is the near-complete race?**
3. **Fertility and marriage between races:** allow freely, discourage (AI weights), or forbid?
4. **Race resource:** do race events get their own resource, or ride on existing systems?
5. **Timing:** build the mechanics now on the temporary map, or wait for Gate 1/2 cultures?

## 10. Suggested build order, once ruled

1. **Proofs.** Run T1 to T4 in one small test sub-mod with two test races.
2. **Spec (eotg-architect).** Race traits, the share schema, the birth and creation hooks, the hybrid block, the portrait hooks and save handling.
3. **Mechanics batch.** Map-agnostic. Build it, then QA.
4. **Heritage groups.** Build them with the Gate 1/2 cultures, from the intake briefs (answer Q-C1 first).
5. **Race events.** Propose them to you first (the owner rule on new events), then build.

## 11. What existing overhaul mods do (observational only)

Owner rule: other mods may be studied for technique, never used as sources or precedent, and never copied. Every mechanism below has to be confirmed in vanilla before we use it.

Three installed mods implement races: *Warcraft: Guardians of Azeroth Reforged 2*, *LotR: Realms in Exile* and *Elder Kings 2*. Godherja, AGOT, After the End and its sci-fi submod have no race layer.

### Their strategies

| Strategy | Who | Strength | Weakness |
|---|---|---|---|
| **Race = the culture's heritage.** Custom heritage parameters (e.g. an "elven heritage" flag plus an umbrella "heritage group" flag), read by scripted `is_<race>` triggers. | LotR | Generated characters always get the right race, because they inherit culture. Grouping is one parameter check. | Race moves with culture, so they **lock culture conversion** across races and **divorce cross-race marriages** that slip through. |
| **Race = a trait,** one per race in a shared trait group, with family flags (e.g. "elven family"). | Warcraft | Race stays with the person through any culture change. | Needs many re-entry hooks (guest arrival, joining a court, rank-up) to give traits to generated characters. Their own comments call it the most CPU-heavy part of the mod. |
| **Three layers.** Heritage parameter for species, character flags for races that can't interbreed, and a **culture variable** holding the species, copied to new cultures on `on_culture_created`. | EK2 | Hybrid and divergent cultures keep the right species automatically. | The most moving parts. |

### How they handle inheritance

- **Warcraft:** a hidden `on_birth_child` event rolls 50/50 to copy one parent's race trait, so a child is always one whole race and never a blend. Appearance comes from an **inheritable race morph gene**, which ethnicities pin per race.
- **LotR:** race simply follows the culture vanilla gives the child, because cross-race marriages are blocked.
- **EK2:** non-interbreeding races are copied when either parent has them. Lifespan traits combine from both parents by tiered rules, which is the closest any of them comes to blending.
- **None of them tracks ancestry percentages.** Our share-and-roll design (§2) has no precedent in these mods.

### Fertility and marriage

- **LotR:** racial fertility, fertile years and life expectancy sit in the heritage pillar's `character_modifier`. An `on_marriage` fallback breaks up cross-race matches.
- **Warcraft:** fertility sits on the trait. A sexual-compatibility trigger is driven by a **game rule** (unrestricted / distant-interracial / off), plus a whitelist of humanoid families.
- **EK2:** a race-compatibility trigger is used in marriage interactions and in pool and guest selection. An incompatible pregnancy is ended (`end_pregnancy`).

### Grouping and targeting

- **LotR:** umbrella heritage parameters, plus pair triggers ("same race as…").
- **Warcraft:** family trait flags (`has_trait_with_flag`).
- **EK2:** the species culture variable, propagated to new cultures.

### Pitfalls they work around, and the lessons for us

1. **Two of them override vanilla on_action files in place** (birth and title on_actions), and EK2 comments out vanilla pregnancy events. That breaks our invariant 4. **Use additive hooks only.**
2. **Trait-based race goes missing on generated characters.** Warcraft patches this from many hooks. **Use the single `on_character_created` hook** (§2.4), and check its coverage with T2.
3. **Culture-based race drifts with conversion.** LotR locks conversion to prevent it. **Keep race on the trait** and use heritage only for grouping. That avoids the lock, and an elf can live in a human culture.
4. **Immortals and ruler-designer characters** need special cases (EK2's lifespan code). **Plan for edge cases** in the spec: designer characters, adopted children, characters spawned from history.
5. **Cost.** Warcraft's repeated re-checks are expensive. **Run once per birth or creation,** with no recurring loops.

### Techniques to confirm in vanilla for our design

- Custom heritage `parameters` (T1).
- Trait `group` with `has_trait = <group>`.
- `has_trait_with_flag` for race families.
- `on_character_created` with `creation_reason`.
- `on_culture_created`, to keep new cultures in the right group.
- Inheritable morph genes with ethnicity pinning, for race bodies.
- A game rule for cross-race fertility, to fit our INT5 rules pattern.
