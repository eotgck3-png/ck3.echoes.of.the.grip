# E. Race framework: suggested answers to the open owner decisions (D1–D7)

2026-11-03. Read-only research for the owner. It covers `docs/specs/races_framework_v1.md` §11 (D1–D7) and
`docs/proposals/race_and_heritage_groups_feasibility.md` (§6, §11). Nothing in the repo was changed.

**Abbreviations used below**
- **G** = `D:/SteamLibrary/steamapps/common/Crusader Kings III/game` (1.20.1.1). It is the only precedent cited.
- **W** = `D:/SteamLibrary/steamapps/workshop/content/1158310`. Mods there are observed for technique only. They
  are never cited as precedent and never copied.
- **Spec** = `docs/specs/races_framework_v1.md`. **Feas** = the feasibility proposal.

**Race families used throughout:**

| Family flag | Races |
|---|---|
| `eotg_race_family_human` | human (the suggested default race) |
| `eotg_race_family_elf` | elf, moon elf, dusk elf, drow, and half-elf as a half-race |
| `eotg_race_family_orc` | orc, orog, deep orc |
| `eotg_race_family_goblinoid` | goblin, hobgoblin, stardust hobgoblin |
| `eotg_race_family_dwarf` | dwarf, duergar |
| `eotg_race_family_giantkin` | ogre/giantkin, and half-giant as a half-race |
| `eotg_race_family_minotaur` | minotaur |

---

## 0. What the four mods do (extends Feas §11; observational only)

Feas §11 already covers the high-level strategies: LotR puts race on heritage, Warcraft on a trait, and EK2 uses
three layers. This table adds what §11 lacks: the exact handling of each topic the owner asked about.

| Topic | LotR: Realms in Exile (2291024373) | Elder Kings 2 (2887120253) | Godherja (2326030123) | AGOT (2962333032) |
|---|---|---|---|---|
| **Cross-race fertility** | **Blocked unless same race.**<br>• `lotr_children_with_allowed` requires `same_race` (`common/scripted_triggers/lotr_scripted_triggers/lotr_marriage_triggers.txt:3-35`).<br>• Hidden `pregnancy.8001` ends a failed pregnancy with `end_pregnancy` + `pregnancy_cleanup_effect`, then re-fires the vanilla pregnancy events itself (`events/pregnancy_events.txt:1783-1806`). That needs an in-place edit of the vanilla `on_pregnancy_mother` (`common/on_action/child_birth_on_actions.txt:1160`). | **Blacklist, not whitelist.**<br>• `ek_race_compatible_trigger` (`common/scripted_triggers/ek_race_triggers.txt:1-75`) blocks only 7 species (khajiit, argonian, lilmothiit, imga, goblinken, daedra, giant) from breeding outside their kind. Everyone else (men and mer) is `always = yes`.<br>• Checked in marriage `is_valid` (`00_marriage_interactions.txt:750, :1811`), the pool-marriage on_action (`yearly_on_actions.txt:3275`) and guest selection.<br>• `ek_race.0100` ends a pregnancy (`end_pregnancy` + `pregnancy_cleanup_effect`). `ek_race.0101/0102` stillbirth any leftover child at birth (`events/ek_race_events/ek_race_events.txt`). Both are wired by editing vanilla on_actions in place. | No race layer. | No race layer.<br>• Dragons are characters with `can_have_children = no` and `fertility = 0.0` on the trait (`common/traits/00_agot_dragon_traits.txt`, the `dragon` block). |
| **Half-races** | None as a race.<br>• The only canon hybrid marriage (Aragorn × Arwen) is a **named-character carve-out** in `lotr_children_with_allowed` (`:8-33`). That is "canon exceptions only" in practice. | No half-race trait.<br>• Half-elven peoples (e.g. Bretons) are ordinary **cultures** in the men/mer pool, with no species flag. | None. | None.<br>• "Dragonblood" ancestry is a **genealogy walk**, not a stored share: `agot_has_dragonblood_heritage` checks `real_father` / `real_mother` chains 2–3 generations deep, with the depth set by a game rule (`common/scripted_triggers/00_agot_dragon_triggers.txt:489-549`; `common/game_rules/00_agot_game_rules.txt:101-104`). |
| **Default race** | **Human is the fallback.**<br>• `is_human` carries the comment "all other races and species should be added here" (`lotr_race_triggers.txt:278`). | **No flag means compatible with all.**<br>• `race_traits_effect` flags only the 7 exceptions; everyone else needs no data. | n/a | **Human is the default.**<br>• `is_human = { NOT = { has_trait = dragon } ... }` (`common/scripted_triggers/00_agot_character_triggers.txt:1`). |
| **Race in the ruler designer** | Race comes from **culture**, which the player picks.<br>• Race-like traits are hidden: `doom_sundered` has `shown_in_ruler_designer = no` (`common/traits/00_lotr_traits.txt:2141-2150`).<br>• The blood tiers are buyable: `blood_of_numenor_1..10`, cost 20→200 (`00_lotr_traits.txt:630, 946`). | Race flags come from **culture** in the setup effect.<br>• Lifespan traits are hidden: `shown_in_ruler_designer = no` (`common/traits/ek_misc_traits.txt:455, 488, 521, 554, 829`).<br>• Designer characters are special-cased with `is_from_ruler_designer` (`common/scripted_effects/ek_race_effects.txt` `lifespan_traits_effect`). | Magic potency is a buyable genetic trait group, `magic_good_1..10`, cost 100→800 (`common/traits/godherja/GH_magic_traits.txt:5-60, 311-353`). | The `dragon` trait has `shown_in_ruler_designer = no`. |
| **Race modifiers (fertility, health, lifespan)** | On the **heritage pillar's `character_modifier`** (`common/culture/pillars/00_heritage.txt`):<br>• elves: `life_expectancy = 28000`, `years_of_fertility = 13000`, `health = 10` (:281-321);<br>• dwarves: life 170–190, `fertility = -0.2`, `health = 0.5`, `negate_health_penalty_add = 7` (:1103-1290);<br>• orcs: life 120; goblins: `fertility = 0.5` (:821-894);<br>• hobbits: life +30, fertility +0.25 (:262-267);<br>• Drúedain: life −25 (:206-209);<br>• **humans: none.** | On a **separate lifespan trait group**, `lifespan_1..6`:<br>• life 60 / 110 / 160 / 260, then immortal;<br>• fertility −0.1 per tier, from −0.1 down to −0.6 (`ek_misc_traits.txt:443-838`);<br>• assigned from heritage parameters `heritage_lifespan_N`;<br>• inherited from both parents by weighted `random_list` (90/10, 60/40; `ek_race_effects.txt:513+`). | No race modifiers. | `dragon`: `health = 5`. Vanilla `giant`, unchanged: `health = -0.25`. |
| **Race-specific resource** | **Blood of Númenor**, a 10-tier trait:<br>• fertility −0.05→−0.25 and life +20→+200 per tier;<br>• re-derived at birth from **both parents' tiers** with a `random_list` (`events/lotr_events/lotr_blood_of_numenor_event.txt:135-240`).<br>• This is the closest any of the four comes to our share-and-roll design. | Species variable on the **culture**, propagated on `on_culture_created` (`common/on_action/ek_hybridization_on_actions.txt:1-30`). Not a spendable resource. | **Magic** (spell resource and magic potency traits).<br>• Social reaction through `triggered_opinion` keyed on a parameter (`magic_illegal` / `magic_shunned` / `magic_supreme`; `GH_magic_traits.txt:28-41`). | **Dragons** themselves, plus dragonblood ancestry. |

**Lessons for D1–D7:**
1. **Out-of-band lifespans.** Both race mods scale lifespan far beyond vanilla (+200 to +28 000 years). Neither has
   to keep a medieval succession loop moving. We do (D3).
2. **Pregnancy blocks were wired by in-place on_action edits.** Both blocking mods also call
   `pregnancy_cleanup_effect` after `end_pregnancy`. Vanilla does the same (D2).
3. **Nobody exposes race in the designer.** Every mod hides race-like traits. Race comes from the culture pick (D6).
4. **The default race is human, or "no data".** That holds in every mod that has a default (D5).
5. **Canon hybrids are handled as exceptions.** LotR carves out named characters; EK2 treats half-peoples as
   cultures (D1).

---

## D1. Canon hybrids

### 1. Question
Are half-races their own race (rule `as_own_race`), canon exceptions only (rule `off`, today's default), or does the
canon get revised? Do half-races get heritage groups and cultures?

### 2. Vanilla comparables
- **There is nothing above heritage.** Vanilla has no heritage family or group (Feas §1). Its groupings are ad-hoc OR
  lists (`G/common/culture/traditions/00_combat_traditions.txt:245-246`).
- **Heritage pillars carry no `parameters` and no `character_modifier`** (`G/common/culture/pillars/00_heritage.txt`
  has 0 `character_modifier` blocks). A half-race heritage would be a mod-only construct either way.
- **Hybrid cultures are vanilla's "half" mechanism, at culture level.**
  - The gate is `is_valid_for_hybridising_trigger` (`G/common/scripted_triggers/00_cultural_triggers.txt:473-514`).
  - It needs `cultural_acceptance >= hybridization_threshold_value` (:524).
  - Spec §6 blocks hybrids between cultures of different race groups.

### 3. Mod techniques
- **LotR** has no half-race. Its one canon hybrid line is a named-character exception
  (`lotr_marriage_triggers.txt:8-33`).
- **EK2** models half-peoples as ordinary cultures with no species data.
- **No mod** gives a half-race its own heritage group.

### 4. Suggested answer
**Make `as_own_race` the default rule setting.** Keep `off` as a lobby option.

**Why:**
1. **Canon has self-sustaining half-race *populations*, not only individuals.**
   - The Half-Elf citizens of Old Xerxes (`docs/lore/MYR_CLUSTER_WARS_866_THEATRE.md:170-177`; 866 AG theatre
     dossier).
   - The half-giant Star Tsars of Zandrov (`docs/lore/D7D_CAMPAIGN_ARCHIVE_CATALOG.md:189`).
   - Under `off`, two half-elves can only have elf or human children (birth step 3 *splits* the HALF share, Spec §9).
     A canon half-elven people would dissolve within one generation, and only the pool would refill it.
2. **`as_own_race` still obeys the owner's rule.** Races don't blend: every child is exactly one race, rolled from
   ancestry. The half-race is simply another race in the roll.
3. **`off` remains available** for players who want strict canon-exceptions play. Named characters such as Xerxes
   keep their trait under either setting.

**Optional softening** (it keeps the owner's "% chance" feel for first-generation crosses):
- Today, pure elf × pure human always gives 100% half-elf. The merge is deterministic.
- Add a blend factor *k* (suggest 0.5): HALF += 2·min·*k*.
- Pure elf × pure human would then give half-elf 50%, elf 25%, human 25%. Later generations converge the same way.

**Heritage groups and cultures for half-races:**
- **Give a half-race a heritage group only where canon names a half-race *people*.**
  - Half-elf: **yes**, for the Old Xerxes culture.
  - Half-giant: **pending** the canon check below.
  - Every other half-race character lives in a parent race's culture, and needs nothing.
- **Make the hybrid block family- and pairing-aware.** As built, it refuses hybrids between the half-elf group and
  both the elf and the human groups, because they are different groups. It also refuses hybrids between moon-elf
  and dusk-elf cultures.

  The suggested rule: hybridization is refused only when the two groups belong to **different families and no
  pairing links them**. So:
  - half-elf ↔ elf is allowed (same family);
  - half-elf ↔ human is allowed (the pairing links them);
  - elf ↔ orc is still refused.

### 5. Confidence
**Medium.** The mechanics recommendation is firm. The default depends on canon (below).

**Canon dependencies** (noted here, not settled):
- **(a) The kit's race list and SETTING LORE disagree.**
  - SETTING LORE's playable list (`OLD PROJECT VERSION/docs/SETTING LORE:578-590`) names Half-Orcs, tieflings,
    gnolls, ratfolk and dragonborn. The kit has none of them.
  - The kit adds goblins, orcs, ogres, minotaurs and duergar, which that list doesn't name.
  - Is Half-Orc a kit race? Spec §9.3 still uses half-orc as its example.
- **(b) Half-giant parentage:** human × ogre/giantkin, or human × something else?
- **(c) The D7D catalogue isn't dated.** It is not a dated `docs/lore` history, so the canon-precedence rule ranks
  the Zandrov half-giant realm below dated entries. Lore-keeper should confirm it exists at 866.
- **(d) Is the Old Xerxes populace a culture of its own, or a human-group culture with half-elf characters?**

### 6. Script change
1. **Game rule default.** In `common/game_rules/eotg_game_rules.txt`, set the default of `eotg_race_half_races`
   (line 90) to `eotg_race_half_races_as_own_race`. Keep both settings.
2. **Optional blend factor.** In `common/scripted_effects/eotg_race_effects.txt`, `eotg_race_pair_op_merge_effect`
   (:385-407): change `multiply = 2` to `multiply = $FACTOR$`, then add the remainder back to A and B as
   (min − min·FACTOR) each.
   - Pass `FACTOR` from `eotg_race_for_each_pairing_effect` with a default of 2, or add a third rule setting
     `as_own_race_partial`.
   - Update the B-tests in `docs/test_submods/races/README.md`.
3. **Family-aware hybrid block.**
   - Add a registry trigger `eotg_race_cultures_related = { A B }` to the pack (an 11th registry key). Its body is
     an OR over families plus one clause per pairing.
   - Change `eotg_race_cultures_can_hybridize` (`common/scripted_triggers/eotg_race_triggers.txt:87`) to refuse only
     when the cultures are `eotg_race_cultures_in_different_groups` **and not** `eotg_race_cultures_related`.
   - Add a main-mod stub of `always = no` with inert parameter references (Spec §4.1).
4. **Race pack.** Register `half_elf` (and `half_giant` once canon allows) as grouped races, with
   `eotg_heritage_group_half_elf` on the Old Xerxes heritage.
5. **Spec.** Rewrite Spec §9 and §11 D1 as resolved.

---

## D2. Half-race fertility under `forbidden`, and the compatibility table

### 1. Question
Under a future `forbidden` setting, may a half-elf have children with an elf or a human? Today `forbidden` would treat
every pair of different traits as cross-race. Should compatibility come from a table keyed on race families
(`eotg_race_family_*`)?

### 2. Vanilla comparables
- **Conception chance is the average of the two parents' fertility**, multiplied by a constant
  (`G/common/defines/00_defines.txt:374`, `FERTILITY_CHANCE_MULTIPLIER`).
  - The only pair-based multipliers are code-side family ones (:429-431).
  - **No scriptable pair-based conception block exists.** A trait's `can_have_children = no` (`_traits.info:84`;
    `incapable` `00_traits.txt:6397`, `celibate` :8717) is per character, not per pair.
- **`can_have_children_with` is the vanilla scripted pair check** (`G/common/scripted_triggers/00_marriage_triggers.txt:66-68`).
  It holds only `sex_opposite_of`. Vanilla AI reads it to decide whether a match is "about fertility and genetic
  traits":
  - `G/common/character_interactions/00_marriage_interactions.txt:2620, :2630, :2656, :2684, :3225`;
  - `G/common/on_action/yearly_on_actions.txt:3242, :3254` (pool marriage);
  - `G/events/interaction_events/marriage_interaction_events.txt:844-876`.

  Overriding it makes vanilla AI stop valuing incompatible matches for heirs, with no further edits.
- **Termination.** `on_pregnancy_mother` (`G/common/on_action/child_birth_on_actions.txt:1500-1520`) fires at reveal.
  Vanilla ends a pregnancy with the pair `end_pregnancy = yes` + `pregnancy_cleanup_effect = yes`
  (`G/events/pregnancy_events.txt:806-807`; the cleanup is defined at
  `G/common/scripted_effects/00_pregnancy_effects.txt:265`).
- **Ordering hazard.** `pregnancy.1001` fires from the same on_action and calls `add_trait = pregnant` without
  checking that a pregnancy still exists (`G/events/pregnancy_events.txt:155-164`).
  - If our termination runs first, the mother keeps a stray `pregnant` trait.
  - Spec §8.1's sketch (`end_pregnancy` only, same tick) would hit this.

### 3. Mod techniques
- **EK2: blacklist.** Only listed species are exclusive; everything else is compatible. Its trigger is used in
  marriage validity, pool marriage and guest pools, and it terminates the pregnancy plus stillbirths leftovers.
- **LotR: whitelist** (same race only), plus named exceptions.
- **Both** call `pregnancy_cleanup_effect` after `end_pregnancy`, and both edit vanilla on_actions in place. That
  breaks our invariant 4.

### 4. Suggested answer
**Under `forbidden`, a half-race is fully fertile with both of its parent races and with its own kind.**

**Compatibility comes from two sources, both already in the race pack:**
1. **Same family is compatible.** Moon elf × drow, orc × orog, and hobgoblin × stardust hobgoblin can all breed.
2. **The pairing table is also the compatibility table.** If `half_elf = elf + human` is registered, then:
   - elf × human is compatible (canon says it happens);
   - half-elf × elf and half-elf × human are compatible.

Everything else is infertile under `forbidden`: elf × orc, human × minotaur, dwarf × goblin, and so on. No third
table is needed.

**Rename the setting's meaning to "compatible only".** Keep the reserved key `eotg_race_crossbreeding_forbidden`
(Spec §8) and change only its description. This is EK2's shape (default compatible, families exclusive) derived from
our own data. Keep `free` as the default (D3).

**Marriage under `forbidden`:**
- **Don't block it.** Canon marriages across races exist (Xerxes' parents), and a sterile marriage is ordinary
  vanilla (`can_have_children = no` traits still marry).
- **Override `can_have_children_with` instead.** The vanilla AI then deprioritizes those matches through its
  existing fertility logic (call sites above).

### 5. Confidence
**Medium-high** for the rule shape. **Medium** for the termination timing, which needs an in-game test (see the
script change).

### 6. Script change
1. **Compatibility trigger.** Add a 12th registry key in the pack, `eotg_race_can_interbreed = { TARGET }`. Its body
   is an OR of:
   - one `AND = { has_trait_with_flag = eotg_race_family_<f>  $TARGET$ = { has_trait_with_flag = eotg_race_family_<f> } }`
     per family;
   - one clause per pairing (A↔B, HALF↔A, HALF↔B, both directions).

   The main-mod stub is `always = yes`, so with no pack everything stays compatible.
2. **Override `can_have_children_with` by key** in a new file, `common/scripted_triggers/eotg_race_vanilla_overrides_marriage_triggers.txt`:
   - copy the vanilla body (`00_marriage_triggers.txt:66-68`) and add one `# EOTG` clause:
     `trigger_if = { limit = { has_game_rule = eotg_race_crossbreeding_forbidden } eotg_race_can_interbreed = { TARGET = $CHARACTER$ } }`;
   - put it on the re-copy list (pitfalls §16).
3. **Replace Spec §8.1's same-tick sketch.** `eotg_race_on_pregnancy_mother` should only
   `trigger_event = { id = eotg_race.0001 days = 1 }` when the pair can't interbreed. That event is hidden; its
   `immediate` runs `end_pregnancy = yes` and `pregnancy_cleanup_effect = yes` (the vanilla pair,
   `pregnancy_events.txt:806-807`).
   - The one-day delay lets `pregnancy.1001` add `pregnant` first, so the cleanup removes it.
   - The player may see a pregnancy announcement followed by a quiet loss. Decide on a toast when building.
4. **Add test B6** to `docs/test_submods/races/README.md`: a forced cross-family pregnancy ends, and no `pregnant`
   trait remains.
5. **Re-add the setting.** Put `eotg_race_crossbreeding_forbidden` back in `common/game_rules/eotg_game_rules.txt`,
   with loc, **only together with** items 1–3 (Spec §8, the orchestrator ruling).

---

## D3. Fertility default, and race modifiers on the trait

### 1. Question
Should the cross-breeding default stay `free`, or become `discouraged`? Should race traits carry fertility, health or
lifespan modifiers, and with what values?

### 2. Vanilla comparables

**The scale** (`G/common/defines/00_defines.txt`):
- `BASE_FERTILITY = 0.5` and `BASE_HEALTH = 5.0` (:149-150).
- Fertility is averaged across the couple and multiplied by 4.75 to give a monthly conception percentage
  (:374, `FERTILITY_CHANCE_MULTIPLIER`).
- Characters start dying below health 3 (:334).
- `life_expectancy` is in years. Its concept text says a high value "will make characters visibly age slower"
  (`G/localization/english/game_concepts_l_english.yml:534`).

**Fertility on vanilla traits** (`G/common/traits/00_traits.txt`):
| Value | Traits |
|---|---|
| ±0.1 | `beauty_good_1` :7209 / `beauty_bad_1` :7077 |
| ±0.2 | `beauty_good_2` :7251 / `beauty_bad_2` :7123; `family_first` :974; `seducer` :1716 |
| ±0.25 | `lustful` :2267 / `chaste` :2313 |
| ±0.3 | `beauty_good_3` :7311 / `beauty_bad_3` :7173 |
| ±0.5 | `fecund` :7990 / `infertile` :8669; `inbred` −0.5 :8331 |

**Health on vanilla traits:**
| Value | Traits |
|---|---|
| ±0.25 | `physique_good_1` :7811 / `physique_bad_1` :7677; `temperate` :2409; `athletic` :5305; `pure_blooded` :7963 |
| ±0.5 | `physique_good_2` :7860 / `physique_bad_2` :7720; `strong` :8020 |
| ±1 | `physique_good_3` :7909 / `physique_bad_3` :7768 |
| −0.25 | **`giant` :8287**, the only vanilla "body type" trait with a health term |

**Lifespan (`life_expectancy`) in vanilla:**
| Value | Source |
|---|---|
| +5 | `fecund` `00_traits.txt:7991`, which also has `years_of_fertility = 5` :7992 |
| −3 … −10 | `fragile_bones` tiers, `00_traits.txt:6322-6374` |
| +5 | `blood_legacy_5`, `G/common/dynasty_perks/00_dynasty_perks.txt:68` |
| +5 | `tradition_cultivation`, `G/common/culture/traditions/tgp_traditions.txt:2119` |
| +10 | the strongest: the FP1 high-king modifiers, `G/common/modifiers/01_dlc_fp1_modifiers.txt:10, :19` |

**Where body modifiers live in vanilla:** the body-type traits put their modifiers **on the trait**:
- `dwarf` `00_traits.txt:8234-8270` (prowess −4, `same_opinion = 20`);
- `giant` :8274-8320 (prowess +6, health −0.25).

Vanilla heritages carry none (D1 §2).

**Crossbreeding rule defaults:** vanilla rule defaults are the "historical/normal" setting, and the deviations are
opt-in. Examples: `same_sex_marriage` default → accepted (`G/common/game_rules/00_game_rules.txt:320-335`);
`hybrid_culture_ai_restrictions` (:619-639).

### 3. Mod techniques
- **LotR** puts race modifiers on the heritage, with extreme values (elves `life_expectancy = 28000`, `health = 10`).
- **EK2** uses a separate lifespan trait group of 60–260 years, with a fertility penalty that grows with lifespan
  (−0.1 per tier).
- **The pattern both share** (longer life means lower fertility) is good design. **Their magnitudes don't suit a
  succession game:** vanilla's whole range is ±10 years.

### 4. Suggested answer

**(a) The default stays `free`.**
- Canon has cross-race children: Xerxes, the half-elven Old Xerxes, half-orcs and half-giants (Feas §6).
- The owner's own model ("child gets a % chance by ancestry") assumes mixed couples have children.
- `discouraged` (AI marriage × 0.1, Spec §8.2) can come later as a lobby option. It shouldn't be the default.

**(b) Race modifiers go on the race trait,** like vanilla `dwarf` and `giant`, not on the heritage. Race stays with
the person (Feas §2, "why traits").

**(c) Every value stays inside one vanilla tier-1 or tier-2 genetic step,** so ordinary genetics (beauty, physique,
fecund) still decides individuals. The caps:
- fertility within **±0.2** (the `beauty_*_2` band);
- health within **±0.25** (`physique_*_1`, `giant`);
- `life_expectancy` within **±10** (the vanilla maximum);
- `years_of_fertility` **+5** at most (`fecund`).

**(d) Sub-races share their family's values.** Differences inside a family are canon and flavour, not stats, until
lore says otherwise.

**Suggested values:**

| Race(s) | `fertility` | `health` | `life_expectancy` | `years_of_fertility` | Justification (vanilla anchor) |
|---|---|---|---|---|---|
| human (default) | 0 | 0 | 0 | 0 | The defines are tuned for humans (`00_defines.txt:149-150`). The baseline must not move |
| elf, moon elf, dusk elf, drow | −0.2 | 0 | +10 | +5 | Long life at vanilla's ceiling (`01_dlc_fp1_modifiers.txt:10`). Fertility down by the `beauty_bad_2` step (:7123), with a longer fertile window like `fecund` (:7992). The net is fewer children over a longer span |
| half-elf | −0.1 | 0 | +5 | 0 | The midpoint of elf and human. +5 years matches `fecund` / `blood_legacy_5` |
| dwarf, duergar | −0.1 | +0.25 | +5 | 0 | Hardy (`physique_good_1` :7811, `temperate` :2409), long-lived (+5), slow-breeding (`beauty_bad_1` step) |
| orc, orog, deep orc | +0.1 | +0.25 | −5 | 0 | Robust against illness (+0.25) but short-lived (half of `fragile_bones`' worst tier, :6374). Breeds a little fast (`beauty_good_1` step) |
| goblin | +0.2 | 0 | −5 | 0 | Fastest breeder (`family_first` / `seducer` step, :974 / :1716); short-lived |
| hobgoblin, stardust hobgoblin | +0.1 | 0 | 0 | 0 | Between goblin and human |
| ogre/giantkin | −0.2 | −0.25 | 0 | 0 | Mirrors vanilla `giant` health −0.25 (:8287). Large bodies breed slowly |
| half-giant | −0.1 | 0 | 0 | 0 | The midpoint of giantkin and human |
| minotaur | −0.1 | +0.25 | 0 | 0 | A hardy body (`physique_good_1` step); slow breeder |

**How this plays with the engine:**
- Couple fertility is averaged (`00_defines.txt:374`). An elf × human pair conceives at −0.1, and an orc × elf pair
  at −0.05. Mixed couples land between their parents, which is coherent under `free`.
- Prowess, opinions and combat terms are **not** in scope here. Vanilla shows they are possible (`dwarf` prowess
  −4, `giant` +6). They are a separate owner call.

### 5. Confidence
- **High:** `free` as the default; modifiers on the trait; the vanilla-band caps.
- **Low-medium:** the exact per-race numbers. They are a balancing proposal, and canon may move them.

**Canon dependencies** (not settled):
- **(a) Lifespans.** The 866 digest names no racial lifespans (`docs/lore/REVIEW_866.md` mentions no race).
  - If canon has elves who personally remember the Grip ("living history", CLAUDE.md "Canon"), +10 is far too
    small. That would need a separate immortality/longevity design (vanilla `immortal = yes`, `_traits.info`).
  - Lore-keeper should rule before the numbers are fixed.
- **(b) Do drow, duergar, deep orcs or the stardust hobgoblin differ from their family** (e.g. a Void link)?

### 6. Script change
1. **Main mod.** `common/traits/eotg_race_traits.txt`: replace the template comment "Gameplay … None in v1" (line
   ~57) with the four allowed fields and their caps:
   - `fertility` ±0.2;
   - `health` ±0.25;
   - `life_expectancy` ±10;
   - `years_of_fertility` ≤ +5;

   and cite the vanilla anchors above.
2. **Race pack.** Put each trait's values from the table on its `eotg_race_<race>` trait. The human trait carries
   none.
3. **No change** to `eotg_race_crossbreeding`: `free` stays the default and stays the only setting until D2 is built.
4. **Spec §11 D3:** record the table and the caps.

---

## D4. A race resource, or riding on existing systems

### 1. Question
Invariant 5 says every flavour event reads or moves its system's signature resource. Do race events get their own
resource, or do they ride on existing systems?

### 2. Vanilla comparables

**Cultural acceptance is vanilla's own currency for contact between peoples.**
- Its concept text: "Primarily, it affects how much opinion is reduced between Characters of different Cultures. It
  also affects county opinion, and the cost of forming a hybrid culture"
  (`G/localization/english/game_concepts_l_english.yml:1328`).
- Vanilla moves it from events and pulse actions with `change_cultural_acceptance`. For example, a wedding moves it
  in both directions between the spouses' cultures (`G/common/activities/pulse_actions/wedding_pulse_actions.txt:178-195`).
  Other sites: `pilgrimage_actions.txt:817`, `journey_actions.txt:398`.
- Vanilla reads it in the hybridization gate (`G/common/scripted_triggers/00_cultural_triggers.txt:524`), the trigger
  our Spec §6 already overrides.

**Trait-level social reaction is built in, and needs no events:**
- `same_opinion` / `opposite_opinion` (`G/common/traits/_traits.info:144-148`);
- vanilla `dwarf` has `same_opinion = 20` (`00_traits.txt:8257`), and so does `giant` (:8301);
- personality opposites use `opposite_opinion = -10` (:2272).

**Vanilla has no per-ancestry resource.** The nearest is the dynasty legacy track `blood_legacy_track`
(`G/common/dynasty_legacies/99_legacies.txt:21`).

### 3. Mod techniques
- **LotR**'s race "resource" is a 10-tier ancestry trait (Blood of Númenor), re-derived at each birth.
- **Godherja** uses magic potency traits with `triggered_opinion` keyed on cultural or faith parameters.
- **AGOT** uses dragons plus a genealogy walk.
- **Not one of them builds a new spendable race currency.**

### 4. Suggested answer
**Don't build a new resource. Race events ride on two things:**

1. **Cultural acceptance is the signature resource.** Race flavour events move acceptance between the cultures of
   different heritage groups, or read it.
   - It is a real vanilla quantity with a gameplay effect: opinion between different-culture characters, and county
     opinion.
   - It already sits on the trigger our hybrid block overrides.
   - It is map-agnostic: it is read through `culture` scopes, never through keys.
   - Our block refuses cross-race hybrid cultures whatever the acceptance, so acceptance stays meaningful without
     reopening hybridization.
2. **The ancestry shares** (`eotg_race_share_of`, `eotg_race_share_at_least`; Spec §7) are the read-only input that
   picks *which* events fire: a quarter-elf heir, a half-race court. Shares are fixed at birth and must never be
   "moved" by events.

**Add a small passive reaction on the traits:**
- `same_opinion = 10`, half of vanilla `dwarf`'s 20, on every race trait.
- **No `opposite_opinion`.** Every race lists every other race in `opposites` (Spec §2.1), so it would apply
  blanket friction between every cross-race pair, half-elf vs. elf included.
- Racial attitudes, if wanted later, belong in faith or culture parameters through `triggered_opinion`
  (`_traits.info:151-159`), not on the base trait.

### 5. Confidence
**Medium.** The owner may want race content tied to a mod system instead, e.g. Void Corruption for drow or
duergar. That remains possible because events may read a second system. But invariant 5 needs one signature
resource, and acceptance fits it best.

### 6. Script change
1. **Spec §7 / §11 D4.** Name cultural acceptance as the race system's signature resource, and the shares as its
   read-only selector.
2. **New helper** in `common/scripted_effects/eotg_race_effects.txt`:
   `eotg_race_change_acceptance_effect = { A = <culture> B = <culture> VALUE = <script value> DESC = <loc> }`.
   It wraps a two-way `change_cultural_acceptance`, as vanilla does at `wedding_pulse_actions.txt:184-195`.
   - Use vanilla's own acceptance values (e.g. `miniscule_positive_culture_acceptance`); verify the value file with
     vanilla-scout.
   - `eotg-qa`'s reachability check should require every `eotg_race` event to call it, or to read
     `cultural_acceptance`.
3. **Race pack:** add `same_opinion = 10` to every race trait. The template comment gets a "no `opposite_opinion`"
   rule.
4. **No race event is built** until the owner approves specific events (the owner rule on new events).

---

## D5. The default race

### 1. Question
Which race does a raceless parent or an ungrouped culture count as?

### 2. Vanilla comparables
- **Vanilla's baseline body is the absence of a body trait.**
  - `dwarf` and `giant` are deviations from it (`G/common/traits/00_traits.txt:8234`, :8274), each the other's
    `opposites`.
  - Every define is tuned for that baseline (`BASE_FERTILITY`, `BASE_HEALTH`, `00_defines.txt:149-150`; health and
    aging :326-338).
- **Vanilla's generated-character ranges assume it too** (`RANDOM_CHARACTER_*_FERTILITY/HEALTH`, :110-115).

### 3. Mod techniques
- **LotR:** human is the catch-all (`lotr_race_triggers.txt:278`).
- **AGOT:** human means "not a dragon".
- **EK2:** "no flag" means the compatible majority.
- All three converge on **human as the default**.

### 4. Suggested answer
**Human is the default race, and it carries zero modifiers** (D3). This keeps vanilla's balance exact for the
majority.

**Also make human a *grouped* race:** every human heritage carries `eotg_heritage_group_human`.
- **The reason:** Spec §6 lets an *ungrouped* culture hybridize freely with anything. If human cultures relied only on
  the default, human × elf hybrid cultures would slip through the block.
- **The default then only catches** truly ungrouped cultures (test cultures, unfinished regions, vanilla leftovers)
  and raceless parents.

### 5. Confidence
**High.**

**Canon dependency:** SETTING LORE lists humans first ("diverse cultures, adaptable", `SETTING LORE:580`). The intake
briefs mark every culture "Human" (Feas §7), so today's data agrees.

### 6. Script change
1. **Race pack.** `eotg_race_default_race_effect = { eotg_race_op_$OP$_effect = { RACE = human } }`.
2. Also list `human` in `eotg_race_for_each_grouped_race_effect`, `eotg_race_cultures_in_different_groups` and the
   human heritages' `parameters` (Spec §4.3, steps 2–4 and 6).
3. **No main-mod change.**

---

## D6. Race in the ruler designer

### 1. Question
May players pick race in the ruler designer? Today the traits say `shown_in_ruler_designer = no`, and race comes
from culture.

### 2. Vanilla comparables

**What `.info` documents:**
- `shown_in_ruler_designer = yes/no` defaults to **yes** (`G/common/traits/_traits.info:104`).
- `ruler_designer_cost = int` defaults to 0 (:189).

**What the designer UI does** (`G/gui/window_ruler_designer.gui`):
- It lists non-education, non-personality traits through `GetOtherRulerDesignerTraits` (:1161).
- Each is filtered with `Trait.ShowInRulerDesigner` and gated by `RulerDesignerWindow.CanPickTrait`, with a tooltip
  `CanPickTraitDesc` (:3791-3798).
- **There is no "must pick exactly one" control.** A player can pick no race.
- **Opposites in the designer:** vanilla shows `dwarf` and `giant`, which are mutual `opposites`
  (`00_traits.txt:8243-8245`), at costs 0 and 20 (:8259, :8308). That is the precedent for mutually exclusive body
  traits in the designer. That `CanPickTrait` enforces `opposites` is inferred from this, and needs an in-game check.

**Vanilla pricing:**
| Trait | Cost | Notes |
|---|---|---|
| `physique_good_1` | 60 | `00_traits.txt:7826` (health +0.25, plus prowess) |
| `fecund` | 50 | :7999 |
| `infertile` | **0** | :8674, despite −0.5 fertility, so vanilla doesn't charge for fertility penalties |
| `physique_bad_1` | −15 | :7685 |
| `inbred` | −30 | :8339 |

The ironman cap is 400 points (`00_defines.txt:1558`).

**Designer characters at start:** `is_from_ruler_designer` is a vanilla trigger (`G/common/on_action/game_start.txt:4648`),
and `on_game_start_after_lobby` (:2553) runs after the designer.

### 3. Mod techniques
- **All four mods keep race-like traits out of the designer:**
  - LotR: `doom_sundered`;
  - EK2: the lifespan traits;
  - AGOT: `dragon`.
- **LotR and EK2 derive race from the culture the player picks.**
- **Only purchasable *grades*** (Númenor blood, Godherja magic) are sold, at rising cost.

### 4. Suggested answer
**Yes. Show the race traits in the designer** (`shown_in_ruler_designer = yes`).
- **Why:** our race is deliberately *not* culture (Feas §2), and an elf ruling a human culture is an intended case.
  Hiding race would make that case impossible for players.
- **Picking no race is fine.** The after-lobby pass then assigns one from the culture, as today.

**Price race by its net modifiers, using vanilla's rates:**
- about **+10 per +5 years** of `life_expectancy` (`fecund`: 50 for +5 years plus +0.5 fertility);
- about **+20 per +0.25 health** (half of `physique_good_1`'s 60, which also buys prowess);
- **fertility unpriced**, as `infertile` = 0.

| Race | Suggested cost |
|---|---|
| human | 0 |
| elf family | 20 |
| half-elf | 10 |
| dwarf family | 30 |
| orc family | 10 |
| goblin | −10 |
| hobgoblin family | 0 |
| ogre/giantkin | −20 |
| half-giant | 0 |
| minotaur | 20 |

**Half-races in the designer:** shown under `as_own_race` (D1). Under `off` they should be canon exceptions only,
which needs a designer-side condition the trait can't express. Showing them under both settings is the simple
choice. Accept it, or make it an owner call.

**Fix the designer family.** A designer ruler picked as an elf in a human culture gets designer-generated children
and a spouse (the designer adds them; its point multipliers are `GENERATED_SONS_MULTIPLIER`, `GENERATED_DAUGHTERS_MULTIPLIER` and `GENERATED_SPOUSE`, `00_defines.txt:1562-1564`). The culture route would make them
human, so their race wouldn't follow the parents. Re-roll the children from the parents.

### 5. Confidence
- **Medium-high** to show race.
- **Medium** on the costs, which are balance proposals.
- **Two in-game checks:**
  - that the designer refuses two race traits at once (`opposites`);
  - whether designer-generated relatives count as `is_from_ruler_designer`.

### 6. Script change
1. **Main mod:** `common/traits/eotg_race_traits.txt`, template.
   - Change `shown_in_ruler_designer = no` to `yes`.
   - Add a `ruler_designer_cost = <per table>` line.
   - Update the rules comment (:29-31).
2. **Main mod:** `common/scripted_effects/eotg_race_effects.txt`, `eotg_race_game_start_effect` (:114). In the
   after-lobby run only, before the culture pass:
   - `every_ruler = { limit = { is_from_ruler_designer = yes } every_child = { limit = { is_from_ruler_designer = yes } … } }`
     (or every child under 16; check which flag the generated children carry);
   - remove the child's race and run `eotg_race_birth_effect = { MOTHER = real_mother FATHER = real_father }`.

   The after-lobby call needs a parameter, or a separate `eotg_race_after_lobby_effect`, so `on_game_start` doesn't
   run it.
3. **Race pack:** the per-race costs.
4. **Tests:**
   - **D6a:** design an elf in a human culture with generated children; the children roll from their parents.
   - **D6b:** two race traits can't be picked together.

---

## D7. Pairing order for a shared parent race

### 1. Question
When two pairings share a parent race, which pairing claims the shared share first? Spec §9.3 says listed order
today.

### 2. Vanilla comparables
- None. Vanilla has no multi-race inheritance.
- **`random_list` and the effect order are deterministic per script order.** That is the only ordering vanilla
  offers here (Spec §12 U2: `G/events/dlc/bp2/bp2_hostage_system.txt:968-969`).

### 3. Mod techniques
- None of the four tracks shares, so none faces this.
- LotR's Númenor tiers and EK2's lifespans resolve two-parent combinations with **explicit fixed tables**, not
  dynamic allocation.

### 4. Suggested answer

**This is rarer than §9.3 suggests:**
- **Under `off`, order never matters.** Split is independent per HALF.
- **Under `as_own_race`, A and B never coexist in one profile after merging.** A conflict needs three raw races in one
  child, with the shared race scarcer than the two claims combined.
  - Example: elf .4, giantkin .4, human .2, where both half-elf and half-giant want human.
  - When human covers both claims (elf .25, giantkin .25, human .5), order makes no difference.
- **With today's kit** (half-elf, half-giant; no half-orc), it needs an elf × giantkin parent crossed with humans.

**The suggestion:**
1. **Keep listed order, and fix it by rule:** pairings are listed in descending canon prominence, so **half-elf
   first**, then half-giant. Write that rule into Spec §4.3 step 7 so packs follow it.
2. **Optional fairness upgrade, only if a third pairing on human arrives** (e.g. half-orc): allocate the shared race
   **proportionally** to the claims.

### 5. Confidence
**High.** The impact is low, and the canon-order rule is cheap.

**Canon dependency:** whether Half-Orc becomes a kit race (D1 canon note (a)). That is what would make proportional
allocation worth building.

### 6. Script change
1. **Spec §9.3 and §4.3 step 7:** "pairings are listed in canon-prominence order: half-elf, half-giant[, half-orc]".
2. **Race pack:** `eotg_race_for_each_pairing_effect` lists `half_elf` before `half_giant`.
3. **Optional, later.** A `merge_proportional` op in `eotg_race_effects.txt`:
   - a first pass sums each shared race's claims into local variables;
   - a second pass scales each min(A,B) by shared ÷ total claims when the claims exceed the share.

   Add test B6p for elf .4 / giantkin .4 / human .2.

---

## Canon questions to route to eotg-lore-keeper (none are settled here)
1. **Race list.** Does the kit's list (no Half-Orc, tiefling, gnoll, ratfolk or dragonborn; adds goblin, orc, ogre,
   minotaur, duergar) supersede SETTING LORE:578-590? (D1, D7)
2. **Half-giant.** What is its parentage, and does the Zandrov half-giant realm (D7D catalogue :189, undated) exist
   at 866? (D1)
3. **Old Xerxes.** Is it a half-elf *culture*, or a human-group culture whose people are half-elves? (D1)
4. **Lifespans.** Are any races near-immortal, e.g. elves who witnessed the Grip? That decides whether D3's ±10
   band holds. (D3)
5. **Sub-races.** Do any sub-races differ from their family in body (drow, duergar, deep orc, stardust hobgoblin)? (D3)
