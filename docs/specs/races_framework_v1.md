# Race mechanics framework v1 (as built)

2026-11-03. Cloud session, then a local fix pass the same day after QA (verdict FIX FIRST): Tiger, PX and the
vanilla checks in §12 ran locally; nothing has run in game yet. Design source:
`docs/proposals/race_and_heritage_groups_feasibility.md` (§2–§5, §8). Owner decision: build the mechanics now,
map-agnostic, ahead of the real races. Handoff: `docs/handoffs/cloud_2026-11-03_race_mechanics_framework.md`.

## 1. Summary

- **Every character is exactly one race.** Race is a non-genetic trait, `eotg_race_<race>`.
- **Ancestry is tracked as shares.** `var:eotg_race_share_<race>`, from 0 to 1, summing to 1.
- **The birth roll.** At birth, the child's shares are the average of its parents'. One race is rolled, weighted by
  those shares.
- **Engine-created characters** take the race of their culture's **heritage group**, which is a custom parameter on
  the heritage pillar.
- **Data-driven.** The races are listed in one registry, so adding a race is a small, documented block (§4.3).
- **The main mod registers no races,** so the framework is switched off and does nothing until a race pack fills the
  registry. Two packs exist or are planned:
  - the test sub-mod `docs/test_submods/races/` (two test races and a test half-race);
  - later, the real race kit, whose art is built elsewhere.
- **Map-agnostic.** No title, province, culture or faith key appears in the main mod.

## 2. Files and identifiers

### Main mod

| File | Holds |
|---|---|
| `common/traits/eotg_race_traits.txt` | **Comments only**: the per-race trait template (§2.1) |
| `common/scripted_triggers/eotg_race_triggers.txt` | Generic triggers: `eotg_race_is`, `eotg_race_share_at_least`, `eotg_is_heritage_group`, `eotg_race_cultures_can_hybridize`, `eotg_race_is_cross_race_with` |
| `common/scripted_triggers/eotg_race_registry_triggers.txt` | Registry, trigger half: `eotg_race_framework_active`, `eotg_race_has_any_race`, `eotg_race_culture_is_grouped`, `eotg_race_same_as`, `eotg_race_cultures_in_different_groups` (all `always = no` stubs) |
| `common/scripted_effects/eotg_race_effects.txt` | Generic effects: helpers, the birth roll, the culture route, the game-start pass, the per-race and per-pairing ops |
| `common/scripted_effects/eotg_race_registry_effects.txt` | Registry, effect half: `eotg_race_for_each_race_effect`, `eotg_race_for_each_grouped_race_effect`, `eotg_race_default_race_effect`, `eotg_race_for_each_pairing_effect`, `eotg_race_roll_effect` (inert stubs) |
| `common/on_action/eotg_race_on_actions.txt` | Additive hooks on `on_birth_child`, `on_character_created`, `on_game_start` and `on_game_start_after_lobby`, plus custom on_actions `eotg_race_on_birth_child`, `eotg_race_on_character_created` and `eotg_race_on_game_start` |
| `common/scripted_triggers/eotg_race_vanilla_overrides_triggers.txt` | **Active key-level override** of vanilla `is_valid_for_hybridising_trigger`, plus one `# EOTG` clause (§6) |
| `common/game_rules/eotg_game_rules.txt` | `eotg_race_half_races`, `eotg_race_crossbreeding` (appended; the second has only `free`, §8) |
| `localization/english/eotg_game_rules_l_english.yml` | Rule loc (appended; BOM kept) |
| `docs/specs/races_framework_v1_portrait_example.txt` | Commented portrait-hook example (§10). Not loaded |

### Identifiers

| Kind | Name | Meaning |
|---|---|---|
| Trait | `eotg_race_<race>` | The race trait. Belongs to a race pack |
| Trait group | `eotg_race` | Every race trait carries `group = eotg_race` |
| Trait flag | `eotg_race_family_<family>` | Race family, e.g. every elf race |
| Character variable | `eotg_race_shares` | Boolean: the character has an explicit share profile |
| Character variable | `eotg_race_share_<race>` | That race's share, 0..1. Absent means 0 |
| Cultural parameter | `eotg_heritage_group_<race>` | On a heritage pillar: the culture belongs to that race's group |
| Cultural parameter | `eotg_heritage_grouped` | On a heritage pillar: the culture belongs to *some* race group |
| Game rules | `eotg_race_half_races` (`_off`, `_as_own_race`); `eotg_race_crossbreeding` (`_free` only for now; `_discouraged` and `_forbidden` are reserved, §8) | §8, §9 |
| Temporary scope value | `eotg_race_stub_<op>` | Inert: only inside the main-mod registry stubs' `if = { limit = { always = no } }`, a branch that never runs |
| Local variables | `eotg_race_acc`, `eotg_race_total`, `eotg_race_w_<race>`, `eotg_race_pair`, `eotg_race_pure`, `eotg_race_share_result` | Effect-local, never stored |
| Saved scopes | `eotg_race_parent_a`, `eotg_race_parent_b`, `eotg_race_report_char` | Birth roll; debug report |

`<race>` is always the race **suffix** (`elf`, `moon_elf`, `half_elf`), never the trait key.

### 2.1 Race traits

Template and rules: `common/traits/eotg_race_traits.txt`. Every race trait:
- has `group = eotg_race`;
- lists every other race in `opposites`;
- carries race-family `flag =` entries, `physical = yes` and `shown_in_ruler_designer = no`;
- has an icon placeholder;
- has **no** `genetic`, `inherit_chance`, `birth` or `random_creation`, so the engine never hands one out.

Loc keys: `trait_eotg_race_<race>`, `_desc`, and `TRAIT_FLAG_DESC_<flag>`.

## 3. Ancestry shares

### 3.1 The rule

Every character has a share profile over the registered races, summing to 1.

### 3.2 Storage: explicit or implicit

- **Explicit.** The character holds `eotg_race_shares`, and `var:eotg_race_share_<race>` for each non-zero share.
- **Implicit.** No `eotg_race_shares` means a share of **1 in the race of its race trait**, and 0 elsewhere.

**Pure characters store nothing.** After the birth roll, a child whose rolled race holds ≥ 0.999 of its profile has
its variables dropped. Engine-created and game-start characters are always implicit.

This differs from the literal brief, which said "shares at 100%". The semantics are identical, and the save carries
no variables for the great majority of characters. Every reader honours the rule:
- `eotg_race_share_of`;
- `eotg_race_share_at_least`;
- `eotg_race_add_parent_share_effect`.

Never read `var:eotg_race_share_*` directly.

### 3.3 Precision

Shares halve with each generation. A share below the engine's smallest fixed-point step (expected 0.001;
UNVERIFIED) rounds to 0, so a lone ancestor fades out after about ten generations. Rounding can also leave a sum
of 0.999. The roll doesn't need an exact sum, and compaction uses 0.999 as its threshold.

## 4. The registry

### 4.1 How it works

The registry is the only place races are named. It is ten keys in two files. The main mod defines them as inert
stubs, and a race pack **redefines them by key** in a differently named file that loads later. The test sub-mod
uses `zz_eotg_test_race_registry_*.txt`. Never reuse the main mod's filename: the same path replaces the whole
file.

The effect keys dispatch by literal parameter replacement:

```
eotg_race_for_each_race_effect = {             # in the pack
    eotg_race_op_$OP$_effect = { RACE = elf }
    eotg_race_op_$OP$_effect = { RACE = human }
}
# eotg_race_for_each_race_effect = { OP = inherit } then runs
#   eotg_race_op_inherit_effect = { RACE = elf }, then = { RACE = human }
```

All the per-race logic lives in `eotg_race_op_<op>_effect` in the main mod's `eotg_race_effects.txt`, written once,
generically.

**Main-mod stubs.** Each stub is `always = no` (triggers) or empty (effects), plus an inert reference to every
parameter it is called with: `$TARGET$ = { always = no }`, or
`if = { limit = { always = no } save_temporary_scope_value_as = { name = eotg_race_stub_$OP$ value = yes } }`.
Without it, Tiger reports `error(macro)` "does not need macro arguments" at every call site.

Two keys moved into the registry in the fix pass, because their real bodies name things that only a pack
defines. Both were load errors in the main mod alone:
- `eotg_race_has_any_race`, whose body is `has_trait = eotg_race`, a trait group that no main-mod trait carries;
- `eotg_race_culture_is_grouped`, whose body is `has_cultural_parameter = eotg_heritage_grouped`, which no main-mod
  pillar defines.

### 4.2 The ten keys

| Key | Pack content |
|---|---|
| `eotg_race_framework_active` | `always = yes` |
| `eotg_race_has_any_race` | `has_trait = eotg_race` |
| `eotg_race_culture_is_grouped` | `has_cultural_parameter = eotg_heritage_grouped` |
| `eotg_race_for_each_race_effect` | One `eotg_race_op_$OP$_effect = { RACE = <race> }` line per race, half-races included |
| `eotg_race_for_each_grouped_race_effect` | The same line, for **grouped races only**: races whose heritage pillars carry `eotg_heritage_group_<race>`. Read by the culture route. Don't list a half-race that has no heritage of its own: its parameter is defined nowhere |
| `eotg_race_default_race_effect` | One such line for the **default race**, or empty. The default is the race of a parent with no race trait, and of a character whose culture is ungrouped |
| `eotg_race_for_each_pairing_effect` | One `eotg_race_pair_op_$OP$_effect = { HALF = h A = a B = b }` line per half-race pairing |
| `eotg_race_roll_effect` | One `random_list` with one entry per race: `0 = { modifier = { add = local_var:eotg_race_w_<race> } add_trait = eotg_race_<race> }` |
| `eotg_race_same_as` | `OR` with one `AND = { has_trait = eotg_race_<race> $TARGET$ = { has_trait = eotg_race_<race> } }` per race |
| `eotg_race_cultures_in_different_groups` | `OR` with one `AND = { $A$ = { eotg_is_heritage_group = { RACE = <race> } } $B$ = { NOT = { eotg_is_heritage_group = { RACE = <race> } } } }` per **grouped** race |

### 4.3 Adding a race `<race>`, step by step

1. **Trait.** Copy the template in `common/traits/eotg_race_traits.txt` into the pack's traits file as
   `eotg_race_<race>`. Add `eotg_race_<race>` to the `opposites` of every existing race trait in that file.
2. **Registry, effects file.** Add one line to `eotg_race_for_each_race_effect`, and one entry to
   `eotg_race_roll_effect`. If the race has heritage pillars (step 4), also add one line to
   `eotg_race_for_each_grouped_race_effect`.
3. **Registry, triggers file.** Add one line to `eotg_race_same_as`. If the race is grouped, also add one line to
   `eotg_race_cultures_in_different_groups`. `eotg_race_has_any_race` and `eotg_race_culture_is_grouped` are set
   once per pack, not per race.
4. **Heritage.** On each of the race's heritage pillars, add
   `parameters = { eotg_heritage_group_<race> = yes  eotg_heritage_grouped = yes }`.
5. **Loc.** Add to the pack's loc file:
   - `trait_eotg_race_<race>`, `trait_eotg_race_<race>_desc`;
   - any new `TRAIT_FLAG_DESC_eotg_race_family_<family>`;
   - `culture_parameter_eotg_heritage_group_<race>` (key form unverified).
6. **Optional: default race.** If it's the default race, put its line in `eotg_race_default_race_effect`; there is
   exactly one default.
7. **Optional: half-race.** If it's a half-race of `<a>` and `<b>`, also add
   `eotg_race_pair_op_$OP$_effect = { HALF = <race> A = <a> B = <b> }` to `eotg_race_for_each_pairing_effect`.
8. **Optional: event sugar.** A per-race wrapper such as
   `eotg_is_heritage_group_<race> = { eotg_is_heritage_group = { RACE = <race> } }`.

That makes three files plus loc. No generic file changes.

## 5. Hooks

All hooks are additive (invariant 4). Each custom on_action checks `eotg_race_framework_active` first. No event
fires and there is no cooldown: everything runs once per birth, creation or game start.

### 5.1 Birth: `on_birth_child` → `eotg_race_birth_effect`

`scope:child` runs `eotg_race_birth_effect = { MOTHER = scope:mother FATHER = scope:real_father }`. The hook is
`on_birth_child`, not `on_birth_mother`, per feasibility §2.3. A missing parent is replaced by the other one; with
both missing, the child takes the culture route.

1. **Reset.** Remove any race trait and share profile. `on_character_created` may have run first and given a race
   from culture.
2. **Average.** For each race, the child's share is (mother's + real father's) ÷ 2, where a parent's share is:
   - its explicit share, if it has a profile;
   - else 1 if it has that race's trait, else 0.

   The default race also gets 1 from each parent with **no race trait and no profile**. The child then holds
   `eotg_race_shares`.
3. **Half-races.** Set by the game rule (§9).
4. **Roll.** Weight = share × 1000, held in local variables. One `random_list` runs if the total is above 0. If
   nothing could be rolled, the child takes the culture route.
5. **Compaction.** If the rolled race's share is ≥ 0.999, drop the profile (implicit storage).

The child keeps the full profile, so a quarter-elf line carries forward even when it rolls human (feasibility §2.3).

### 5.2 Creation: `on_character_created` → `eotg_race_assign_from_culture_effect`

This runs only for a character with **no** race. Fallback chain:
1. **Grouped culture:** the first grouped race (`eotg_race_for_each_grouped_race_effect`) whose group holds the
   culture.
2. **Otherwise** (no culture, an ungrouped culture, or no match): the default race.
3. **No default registered:** no race. Every reader treats "no race" as neutral.

The character gets the implicit profile. `scope:creation_reason` isn't read.

### 5.3 Game start: `on_game_start` and `on_game_start_after_lobby` → `eotg_race_game_start_effect`

`every_living_character` with no race goes through the culture route. The second hook catches ruler-designer
characters, as `eotg_cartel_on_actions.txt` does. The pass is idempotent, and a history file may set a race
directly with `trait = eotg_race_<race>`.

**T2 is open:** does `on_character_created` already cover history and designer characters? This pass makes the
answer irrelevant. The test sub-mod logs it; record the result here.

### 5.4 Heritage groups (§5 of the brief)

The group mechanism is the custom pillar parameter. It is **plausible but unproven, and test T1 is still needed**
(§12 U5). Readers:
- `eotg_is_heritage_group = { RACE = x }` (culture scope);
- `eotg_race_culture_is_grouped` (culture scope).

**Fallback if T1 fails:** rewrite only those two triggers as OR lists of `has_cultural_pillar = <heritage>`. That
is vanilla's idiom (`00_combat_traditions.txt:245-246`). No caller changes.

The main mod defines no heritages or cultures. The test sub-mod defines `eotg_heritage_test_a` / `_b` and
`eotg_test_culture_a` / `_b`.

## 6. Hybrid-culture block

`eotg_race_cultures_can_hybridize = { A B }` is true unless:
- both cultures are grouped (`eotg_heritage_grouped`);
- **and** they sit in different groups (`eotg_race_cultures_in_different_groups`).

Documented fallback: an ungrouped culture hybridizes freely, and so does everything while no race is registered.

`eotg_race_vanilla_overrides_triggers.txt` overrides vanilla's `is_valid_for_hybridising_trigger` by key. It takes
the parameters `$CHARACTER$` and `$CULTURE$`, and is copied programmatically from `00_cultural_triggers.txt:473-514`
at 1.20.1.1, then diffed. The only added line, marked `# EOTG`, is a top-level child of the body:

```
eotg_race_cultures_can_hybridize = { A = $CHARACTER$.culture B = $CULTURE$ }   # EOTG
```

- **Scope.** It reads only what vanilla itself reads unguarded (`$CHARACTER$.culture` at :508).
- **Callers.** The trigger is wrapped by `can_hybridize_culture_trigger` (:517-527) and by the scripted rule
  `can_hybridize_culture` (`00_rules.txt:899-904`), so the UI and every wrapper inherit the clause.
- **Main mod alone.** With no race registered the clause is always true, so vanilla behaviour is unchanged.
- **Tooltip.** There is no custom tooltip yet, so a refusal shows the trigger's breakdown. A `custom_description`
  with a loc key is a possible polish.
- **Maintenance.** Re-copy after every CK3 update (pitfalls §2).

Test: **T3**.

Our own future events must test `eotg_race_cultures_can_hybridize` before any `create_hybrid_culture`, because that
effect bypasses the UI check (feasibility §4). Not yet built: an `is_shown` limit on divergence to heritages of the
same group (feasibility §4, "Divergent cultures"). It needs the scope of pillar `is_shown`, which wasn't verified.

## 7. Helpers for future race events

| Helper | Kind, scope | Use |
|---|---|---|
| `eotg_race_is = { RACE = x }` | trigger, character | Is of race x (trait) |
| `eotg_race_same_as = { TARGET = scope:y }` | trigger, character | Same race trait as y |
| `eotg_race_share_of = { RACE = x }` | effect, character | Writes the share (0..1) into `local_var:eotg_race_share_result` |
| `eotg_race_share_at_least = { RACE = x VALUE = 0.25 }` | trigger, character | Share threshold |
| `eotg_race_has_any_race` | trigger, character | Has any race (a registry key; `always = no` in the main mod) |
| `eotg_race_is_cross_race_with = { TARGET = scope:y }` | trigger, character | Both have a race, and the races differ |
| `eotg_is_heritage_group = { RACE = x }` | trigger, culture | Culture is in x's group |
| `eotg_race_set_effect = { RACE = x }` | effect, character | Make a character a pure x (history fix-ups, spawns) |

`eotg_race_share_of` is an **effect**, not a value: script values take no parameters. For a pure comparison use
`eotg_race_share_at_least`.

No race events are built. Invariant 5 needs a race resource first; see §11, D4.

## 8. Fertility and marriage between races: rule `eotg_race_crossbreeding`

**Orchestrator ruling (2026-11-03, pending the owner's fertility decision D3): only `free` ships.** The cloud build
also offered `discouraged` and `forbidden`, but nothing implemented either:
- `forbidden` promised "cannot have children", but `can_have_children_with` doesn't gate conception;
- `discouraged` was never wired.

Both settings and their loc were removed. The rule stays, with its one setting, so that it can grow. These went
with them:
- the commented-out marriage-trigger stubs;
- `eotg_race_crossbreeding_allows`;
- `eotg_race_modifiers.txt` (`eotg_race_crossbreeding_ai_marriage_modifier`).

A rule with a single setting has no vanilla precedent (§12 U19). Confirm in the lobby that it shows and loads.

| Setting | Effect | State |
|---|---|---|
| `free` (**default**) | No restriction | Done |
| `discouraged` | AI marriage weight × 0.1 for cross-race pairs | Reserved key, not built |
| `forbidden` | No cross-race children | Reserved key, not built |

"Cross-race" means `eotg_race_is_cross_race_with`: both characters have a race, and the traits differ. A
half-race differs from both of its parent races (D2).

### 8.1 How `forbidden` is to be built

1. Add an additive hook on vanilla `on_pregnancy_mother` (`G/common/on_action/child_birth_on_actions.txt:1504`)
   with `on_actions = { eotg_race_on_pregnancy_mother }`.
2. In that custom on_action, end a cross-race pregnancy with `end_pregnancy = yes`, vanilla's own termination
   effect (`G/common/scripted_effects/00_pregnancy_effects.txt:340`):

```
eotg_race_on_pregnancy_mother = {
    trigger = {
        eotg_race_framework_active = yes
        has_game_rule = eotg_race_crossbreeding_forbidden
    }
    effect = {
        # scope:real_father is the biological father; scope:father is only the assumed one
        # (vanilla header, child_birth_on_actions.txt:1500-1503)
        if = {
            limit = { eotg_race_is_cross_race_with = { TARGET = scope:real_father } }
            end_pregnancy = yes
        }
    }
}
```

The hook fires when the pregnancy is **revealed**, not at conception (vanilla header, :1500), so the player may see
the pregnancy announced before it ends. `on_pregnancy_father` (:1537) fires at the same point, so it doesn't help.
Decide when building whether that is acceptable or needs a notification. Whether `forbidden` should also block marriage is a separate owner question (D2, D3). If it should, find vanilla's
marriage-eligibility trigger and override it per pitfalls §16, as §6 does.

### 8.2 How `discouraged` is to be built

Vanilla's AI marriage acceptance is the scripted modifier `marriage_ai_accept_modifier`
(`G/common/scripted_modifiers/00_marriage_scripted_modifiers.txt:1512-2798`). It is called at
`G/common/character_interactions/00_marriage_interactions.txt:836` and `:1697`.

1. Override it by key in a differently named file, such as `eotg_vanilla_overrides_modifiers.txt`.
2. Copy the whole block programmatically, add one `# EOTG` modifier, and diff against vanilla (pitfalls §16):

```
modifier = {   # EOTG
    factor = 0.1
    has_game_rule = eotg_race_crossbreeding_discouraged
    <the recipient> = { eotg_race_is_cross_race_with = { TARGET = <the proposed spouse> } }
}
```

Use that block's own scope names for the two parties. The removed `eotg_race_crossbreeding_ai_marriage_modifier`
had this body. `elopment_ai_accept_modifier` (:2800) says it "should copy marriage_ai_accept_modifier on relevant
points", so decide whether elopement gets the clause too.

When either setting is built, add it back to `eotg_game_rules.txt` with the same key, and its loc
(`setting_eotg_race_crossbreeding_<x>` and `_desc`) to `eotg_game_rules_l_english.yml`.

## 9. Half-races: rule `eotg_race_half_races`

Canon ruling pending: Xerxes is half-elf, Half-Orcs exist (feasibility §6). A half-race is always registered as an
ordinary race, with its own trait, share and line in the roll. The pairing table (`eotg_race_for_each_pairing_effect`)
says which two races produce it. The rule decides what birth step 3 does with it.

| Setting | Step 3 | Result |
|---|---|---|
| `off` (**default**) | **split**: any inherited HALF share is moved half to A and half to B | No child is ever born HALF. Existing half-race characters keep their trait (canon exceptions, feasibility §6 option 2) |
| `as_own_race` | **merge**: amount = min(A, B); A −= amount; B −= amount; HALF += 2 × amount | Pure A × pure B gives 100% HALF. A × HALF gives A .5 / HALF .5. A quarter-A child of a B parent (A .125, B .875) gives HALF .25 / B .75. A and B never coexist in one profile (feasibility §6 option 1) |

**§9.3 Order.** Pairings that share a race (half-elf = elf + human, half-orc = orc + human) are applied in listed
order, so with mixed elf + orc + human ancestry the first pairing takes the human share. It's harmless for
two-race lines; the owner may want a rule.

## 10. Portraits

The race trait drives appearance. `gfx/portraits/trait_portrait_modifiers/` takes `traits = { }` and
`dna_modifiers`, and `portrait_modifiers` can gate on `has_trait`. Culture ethnicities set the base look.

There's a commented example in `docs/specs/races_framework_v1_portrait_example.txt`. **No gfx ships.** **T4** checks
whether a trait added in `on_birth_child` shows on the first portrait. If it doesn't, the fix belongs on the art side
(an inheritable race morph gene pinned by ethnicity), not in the roll.

## 11. Open owner decisions

- **D1. Canon hybrids** (feasibility §6): own race, canon exceptions only, or revised canon? The rule implements
  the first two as `as_own_race` / `off`, default `off`. Do half-races also get heritage groups and cultures?
- **D2. Half-race fertility:** under `forbidden`, may a half-elf marry an elf or a human? Today they can't, because
  the races differ. A compatibility table (race families via `eotg_race_family_*`) is the obvious extension.
- **D3. Fertility default.** `free` for now. Should the default be `discouraged`? Should races carry fertility,
  health or lifespan modifiers on the trait, as LotR does on the heritage (feasibility §11)?
- **D4. Race resource for future events** (invariant 5): a race resource of its own, or ride on existing systems?
  No race event is built until this is decided.
- **D5. Default race.** Which race does a raceless parent or an ungrouped culture count as? Presumably human. The
  real race kit sets it in its registry.
- **D6. Ruler designer.** May players pick race in the designer? Today `shown_in_ruler_designer = no`, and the race
  comes from culture.
- **D7. Pairing order** for shared parent races (§9.3).
- **D8. `forbidden` and `discouraged` were removed (resolved 2026-11-03).** By orchestrator ruling, pending D3,
  only `free` ships until one of them is built (§8.1, §8.2). Their keys are reserved.

## 12. UNVERIFIED-VANILLA list, with verdicts

QA (2026-11-03) and the fix pass checked these items against vanilla 1.20.1.1. Each **Verified** item has lost its
`# UNVERIFIED-VANILLA` marker in script, and the comment there cites the vanilla file and line instead.

| ID | Claim | Verdict | Evidence, or the check still needed |
|---|---|---|---|
| U1 | `$PARAM$` works inside an effect name and an identifier (`eotg_race_op_$OP$_effect`, `eotg_race_share_$RACE$`) | **Verified** | `10_dlc_tgp_scripted_effects.txt:238` (`great_project_contribution_completion_reward_$LEVEL$_effect`); `00_education_effects.txt:361` (`has_$SKILL$_..._trigger`) |
| U2 | A `random_list` entry with base weight 0 plus `modifier = { add = X }`; a zero-weight entry is never picked | **Verified** | `events/dlc/bp2/bp2_hostage_system.txt:968-969` (`0 = { modifier = { add = var:hook_chance } ...`) |
| U3 | `local_var:` is readable inside a `random_list` modifier | Plausible | Vanilla reads a `var:` there (U2). B1: the children are not all one race |
| U4 | `has_trait = <group>` matches any trait in the group | **Verified** | `00_education_triggers.txt:325` (`has_trait = education_martial`, a group). Now in the registry (§4.1) |
| U5 | Custom `parameters` on a heritage pillar, read by `has_cultural_parameter` | Plausible; **T1 still needed** | `_cultural_traits.info`. Vanilla uses parameters on ethos and martial pillars only |
| U6 | `on_character_created` root is the new character, and its culture is set | **Verified** | `character_created_on_actions.txt:4`: "Root is the newly created character" |
| U7 | A scripted effect or trigger may be called with a parameter its body never uses | **Fails in Tiger** (`error(macro)`) | Fixed: the stubs reference each parameter inertly (§4.1) |
| U8 | `debug_log` evaluates `[..]` data functions; `$RACE$` is replaced inside a quoted string | **No vanilla precedent** | Test-only output. Read the log text |
| U9 | `category` may be omitted on a trait | **Verified** | `00_traits.txt:8234` (`dwarf`) and `:8274` (`giant`) have none |
| U10 | `has_trait_with_flag` exists | **Verified** | `00_available_for_events_triggers.txt:18` |
| U11 | Variables survive a character's death (the skill says no) | Open | A posthumous test birth |
| U12 | Fixed-point step 0.001 | Open | Shares after about ten generations |
| U13 | A culture that no province or character uses exists as `culture:<key>` | Open | S0 |
| U14 | The v1 vanilla culture keys (ethos, martial custom, head determination, name list, gfx, ethnicity) | **Fixed** | `caucasian_northern` doesn't exist. It is now `caucasian_northern_blond` (`common/ethnicities/01_ethnicities_caucasian.txt:244`). The other keys were found in vanilla culture files |
| U15 | `audio_parameter = european`; a direct colour on a language | Open | Vanilla pillars |
| U16 | `while = { count = N }`, `make_pregnant = { father = x }`, a fixed template `age` | **Verified** | `00_administrative_effects.txt:427-428`; `ep1_fund_inspiration_events.txt:19911`; `00_mongol_templates.txt:51` |
| U17 | Loc key forms `<pillar>_name`, `_collective_noun`, `culture_parameter_<param>` | **Verified** | `cultural_heritages_l_english.yml:3-4`; `cultural_innovations_l_english.yml:15` |
| U18 | The vanilla trigger bodies for the overrides, and the marriage block for `discouraged` | **Resolved** | The hybrid override is copied from `00_cultural_triggers.txt:473-514` (§6). The marriage stubs were removed; the `discouraged` site is in §8.2 |
| U19 | A game rule with a single setting shows and loads | **No vanilla precedent** (new) | Every vanilla rule has two or more settings. Check the lobby |

## 13. Tests

All in `docs/test_submods/races/README.md`:
- **S0–S1:** load and override checks.
- **T1–T4:** the feasibility proofs.
- **C1–C2, G1:** the creation hook and the game-start pass.
- **H1–H3:** the helpers.
- **B1–B5:** the birth roll under both half-race settings, including one real pregnancy through the hook.

T4 needs local work first: adding a test portrait modifier. T3 can run now, because the hybrid override is
active.
