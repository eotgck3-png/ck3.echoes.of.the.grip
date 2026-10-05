# Spec: Cybernetic Augmentation, from four traits to one XP track

**Author:** eotg-architect, 2026-10-02; amended 2026-10-03 with the human's decisions
**Status:** ready for the scripter
**Requested by:** the human. Convert the three tier traits to the vanilla Blademaster model: one trait with a level track.
**Scope:** a rework of the system lifted 2026-10-02 (static QA PASS, never played). No new events; the count stays at 31. Beats, cooldowns, pacing and on_action wiring stay as they are, except where this spec says otherwise.

---

## 0. Decisions (all resolved 2026-10-03)

| # | Question | Resolution |
|---|---|---|
| Q1 | Should the visible XP replace the hidden `eotg_fracture_risk`? | **Resolved 2026-10-03: kept separate.** XP is the tier state (visible). `eotg_fracture_risk` stays the hidden signature resource. The maintenance tooltip loses its number and is reworded in "The static quiets" style. "Static" is augmentation-only vocabulary. Rationale in §2.3. |
| Q2 | Should XP fill within a tier? | **Resolved 2026-10-03: thresholds only.** XP is set to exactly 0 / 50 / 100 at tier changes and never moves in between. There is no drift, no in-band cap, no readiness gate, and no XP nudge from event options. Today's pacing is unchanged. |
| Q3 | How many icons? | **Resolved 2026-10-03: 2.** `eotg_cybernetics.dds` (track) and `eotg_neurofractured.dds`. |
| Q4 | v1 Overclocked lost Enhanced's health and scheme defence. Keep that? | **Resolved 2026-10-03.** Overclocked **keeps** the scheme defence: `enemy_hostile_scheme_phase_duration_add` delta at level 100 is 0, total 5. Overclocked **loses** the +0.5 health; lore-keeper confirmed this is intentional. |
| Q5 | `eotg_aug_init.005` peer condition | **Decided:** a peer at any track level counts. Neurofractured peers are excluded. |
| Names | Track label and timed modifiers | **Resolved 2026-10-03.** Track label "Integration". Modifiers `eotg_mod_aug_affect_dampened` ("Affect Dampened") and `eotg_mod_aug_running_hot` ("Running Hot"). |

---

## 1. Purpose & gate

Replace `eotg_augmented` → `eotg_enhanced` → `eotg_overclocked` (all three superseded and removed from script) with one trait, **`eotg_cybernetics`**. Today the three traits are swapped in and out with `remove_trait`/`add_trait`. The new trait has a single level track whose XP bands are the three tiers. Its displayed name and description switch by XP, as vanilla `lifestyle_blademaster` does. `eotg_neurofractured` stays a separate trait.

The rework also fixes three QA findings:
- timed modifiers that collide with the permanent synergy keys;
- positive icons on the Neurofracture distortion modifiers;
- knights who are augmented but get no synergy modifier.

**Gate 3 (Systems).** Not blocked. `docs/agent_workflow.md` §5 rule 2 (decided 2026-10-02) allows mod-exclusive systems to be built against the temporary map, cybernetics first. §8 confirms this design is map-agnostic.

---

## 2. Signature resource, tier state, and how they move

### 2.1 Two numbers, one signature

| Role | Identifier | Visible? | Values | Who moves it |
|---|---|---|---|---|
| **Signature resource** (invariant 5) | character variable `eotg_fracture_risk` | **hidden** | 0–100 | Unchanged from today. Initiation sets it, flavor options move it, the Overclocked pulse accumulates it, the cascade resets it, and the Neurofractured pulse reads it as episode pressure. |
| **Tier state** | trait XP on `eotg_cybernetics` (single shorthand track, named after the trait) | visible (bar in the trait tooltip) | exactly 0, 50 or 100 | `eotg_aug_set_integration_effect` only |

The signature resource does not change. QA audit 8 keeps its current rule: a flavor event couples if at least one option moves `eotg_fracture_risk` **or** changes tier. Changing tier now means calling `eotg_aug_set_integration_effect`, or adding/removing the trait. That replaces today's "adds or swaps a tier trait", which is how `eotg_aug_tier1.002`, `eotg_aug_tier2.003` (a) and `eotg_aug_tier1.004` passed static QA.

### 2.2 XP values and progression rules

| Level | XP | Display name |
|---|---|---|
| 1 | 0 | Augmented |
| 2 | 50 | Enhanced |
| 3 | 100 | Overclocked |

The thresholds (50 and 100) are vanilla's (`lifestyle_blademaster`).

**Rules (binding):**

1. **XP holds exactly 0, 50 or 100.** Nothing moves it between tiers.
2. **Only one effect changes XP.** `eotg_aug_set_integration_effect = { XP = n }` sets XP to an exact value and refreshes the synergy modifier. Its callers:
   - the two upgrade events (`tier1.002.a` → 50; `tier2.003.a` and `.c` → 100);
   - the two regression decisions (Partial Removal → 0; Downgrade Protocol → 50).

   The cascade removes the trait, which discards its XP. No other `add_trait_xp` on `eotg_cybernetics` may exist anywhere.
3. **Initiation adds the trait at XP 0.** This is the engine default for a newly added track trait, so no initiation option touches XP. `eotg_aug_init.004`'s black-market start keeps its `eotg_fracture_risk = 10` difference.
4. **The progression gates are unchanged.** `eotg_can_progress_to_enhanced` / `_overclocked` keep:
   - the suppress-flag check;
   - the `capital_county.development_level` checks (20 / 35);
   - the on_action's gold conditions.

   Only the tier test inside them changes (§5.2). Pacing is identical to today.
5. **No decay.** Do not use `monthly_track_xp_degradation`. It takes one `min` for the whole track, so it would slide Overclocked characters into a lower tier without:
   - a regression event or decision;
   - `eotg_mod_oc_regression_recovery`;
   - a synergy refresh.

   Vanilla Blademaster has no degradation either.

### 2.3 Why XP does not replace `eotg_fracture_risk` (Q1 rationale)

- **They measure different things.** Maintenance (`eotg_decision_maintenance_protocol`, `tier1.001.b`, `tier3.004.b`) lowers risk. If risk were XP, maintenance would drop the character a tier.
- **Risk outlives the track.** After the cascade the character holds `eotg_neurofractured`, which has no track. `eotg_fracture_risk` keeps running as episode pressure. XP disappears when `eotg_cybernetics` is removed.
- **Risk builds where XP is already at the top.** The whole tier-3 loop runs at XP 100.
- **Hidden is the design intent.** Both the v1 doc and the on_action header say the risk is hidden. A qualitative hint is listed under Deferred.

---

## 3. Identifier table

All keys are `eotg_`-prefixed. No landed titles are involved.

### 3.1 Added

| Type | Key | File | Owner | Notes |
|---|---|---|---|---|
| trait | `eotg_cybernetics` | `common/traits/eotg_augmentation_traits.txt` | scripter | §4.1 |
| scripted trigger | `eotg_is_aug_tier1` | `common/scripted_triggers/eotg_augmentation_triggers.txt` | scripter | `has_trait = eotg_cybernetics` AND NOT `has_trait_xp = { trait = eotg_cybernetics value >= 50 }` |
| scripted trigger | `eotg_is_aug_tier2` | same | scripter | has trait AND xp ≥ 50 AND NOT xp ≥ 100 |
| scripted trigger | `eotg_is_aug_tier3` | same | scripter | has trait AND xp ≥ 100 |
| scripted effect | `eotg_aug_initiate_effect` | `common/scripted_effects/eotg_augmentation_effects.txt` | scripter | `add_trait = eotg_cybernetics` + `eotg_aug_refresh_synergy_effect = yes`. Used for rulers **and knights**. |
| scripted effect | `eotg_aug_set_integration_effect` (param `$XP$`) | same | scripter | The only effect that changes tier; §4.3 |
| scripted effect | `eotg_aug_clear_synergy_effect` | same | scripter | Removes all 15 `eotg_mod_{aug,enh,oc}_*_bonus` |
| scripted effect | `eotg_aug_refresh_synergy_effect` | same | scripter | Clears, then applies the current tier's synergy by `highest_skill` |
| static modifier | `eotg_mod_aug_affect_dampened` | `common/modifiers/eotg_augmentation_modifiers.txt` | scripter | `icon = intrigue_positive`, `intrigue = 2`. Timed. Replaces the timed reuse of `eotg_mod_enh_intrigue_bonus` (QA a). |
| static modifier | `eotg_mod_aug_running_hot` | same | scripter | `icon = martial_positive`, `martial = 3`, `stress_gain_mult = 0.1`. Timed. Replaces the timed reuse of `eotg_mod_oc_martial_bonus` (QA a). |
| icon | `gfx/interface/icons/traits/eotg_cybernetics.dds` | `gfx/` | **human (art)** | QA reports it as art debt, not an error |
| icon | `gfx/interface/icons/traits/eotg_neurofractured.dds` | `gfx/` | **human (art)** | same |

### 3.2 Removed

| Type | Key | Replaced by |
|---|---|---|
| trait | `eotg_augmented` | superseded by `eotg_cybernetics` at XP 0 |
| trait | `eotg_enhanced` | superseded by `eotg_cybernetics` at XP 50 |
| trait | `eotg_overclocked` | superseded by `eotg_cybernetics` at XP 100 |
| scripted effect | `eotg_apply_edu_synergy_augmented` | superseded by `eotg_aug_refresh_synergy_effect`, called by `eotg_aug_initiate_effect` and `eotg_aug_set_integration_effect` |
| scripted effect | `eotg_apply_edu_synergy_enhanced` | superseded (same) |
| scripted effect | `eotg_apply_edu_synergy_overclocked` | superseded (same) |

No `trait_conversion.lookup` entry. No saves exist, and adding an entry would mean overriding vanilla's lookup file.

### 3.3 Kept

These keep their key and meaning:
- `eotg_neurofractured` (body edited, §4.2), `eotg_fracture_risk`, `eotg_add_fracture_risk`.
- `eotg_trigger_neurofracture`, `eotg_apply_neurofracture_distortion` and `eotg_clean_all_aug_modifiers` (bodies edited).
- `eotg_aug_heal_wounds_effect`.
- `eotg_is_augmented_any`, `eotg_can_progress_to_enhanced` / `_overclocked` and `eotg_neurofracture_threshold_met` (bodies edited).
- `eotg_can_receive_augmented`, `eotg_ai_wants_augmentation`.
- The 15 synergy modifiers and the 5 distortion modifiers (icons edited).
- `eotg_mod_implant_calibrated`, `eotg_mod_illegal_implants`, `eotg_mod_oc_regression_recovery`, `eotg_mod_withdrawn_from_court`.
- The 4 opinion modifiers, 3 decisions, all flags (including `eotg_flag_suppress_progression`, whose behaviour is unchanged), the 5 custom on_actions, and all 31 event ids and namespaces.

---

## 4. Definitions

### 4.1 `eotg_cybernetics`: the track trait

The shape is copied from `lifestyle_blademaster` (`game/common/traits/00_traits.txt:1178`).

**Track levels stack.** Every threshold the character has reached applies on top of the trait's base modifiers. The evidence is `tourney_participant`'s `foot` track (`00_traits.txt:16476–16490`): level 100 leaves out modifiers that 65 grants, which only makes sense if the levels add up. So the track columns below are **deltas**. They are chosen so the totals match today's three traits, with the Q4 change applied.

| Modifier | Base (= Augmented total) | `track` 50 (delta) | `track` 100 (delta) | Enhanced total | Overclocked total |
|---|---|---|---|---|---|
| `prowess` | 2 | +2 | +4 | 4 | 8 |
| `health` | 0.5 | 0 | −0.5 | 0.5 | 0 |
| `stress_gain_mult` | 0.1 | +0.1 | +0.2 | 0.2 | 0.4 |
| `attraction_opinion` | −5 | −10 | −15 | −15 | −30 |
| `enemy_hostile_scheme_phase_duration_add` | 0 | +5 | **0** | 5 | **5** (Q4) |
| `diplomacy` | 0 | −2 | −3 | −2 | −5 |
| `fertility` | 0 | −0.2 | −0.2 | −0.2 | −0.4 |
| `dread_gain_mult` | 0 | 0 | +0.3 | 0 | 0.3 |
| `knight_effectiveness_mult` | 0 | 0 | +0.1 | 0 | 0.1 |
| `ai_honor` | −1 | 0 | −1 | −1 | −2 |
| `ai_energy` | 2 | +1 | +1 | 3 | 4 |
| `ai_zeal` | −1 | −1 | −1 | −2 | −3 |

Leave zero-delta cells out of the script. Their absence is what carries the stacked value forward.

`ai_*` keys are modifiers: vanilla puts `ai_energy` in a static modifier (`common/modifiers/00_martial_lifestyle_modifiers.txt:221`). `_traits.info` reads any unrecognised key inside a track level as a modifier, so they are valid at track levels.

Other fields:
- `category = health`. Vanilla `infirm` (`00_traits.txt:6039`) is a health-category trait with tracks.
- `icon = eotg_cybernetics.dds`
- `opposites = { eotg_neurofractured }`
- `ruler_designer_cost = 20`
- `track = { 50 = {...} 100 = {...} }`. This is the shorthand single track, named `eotg_cybernetics`.
- No `monthly_track_xp_degradation`.
- `name = { first_valid = { ... } }`, as in blademaster:
  - `triggered_desc` with `exists = this` + `has_trait_xp = { trait = eotg_cybernetics value >= 100 }` → `trait_eotg_cybernetics_3`;
  - the same at `>= 50` → `trait_eotg_cybernetics_2`;
  - fallback `desc = trait_eotg_cybernetics_1`.
- `desc = { first_valid = { ... } }`, as in blademaster:
  - first, `NOT = { exists = this }` → `trait_eotg_cybernetics_1_desc`;
  - `>= 100` → `trait_eotg_cybernetics_3_character_desc`;
  - `>= 50` → `trait_eotg_cybernetics_2_character_desc`;
  - fallback `trait_eotg_cybernetics_1_character_desc`.

  The `NOT exists = this` guard must come first. `_traits.info` warns that there may be no root.

### 4.2 `eotg_neurofractured`: separate failure state

Neurofractured is a terminal, irreversible failure state with its own event pool, not a fourth level. Its modifiers are unchanged. Edits:
- `opposites = { eotg_cybernetics }`
- add `icon = eotg_neurofractured.dds`
- add `shown_in_ruler_designer = no`. Today it costs 0 in the ruler designer, which makes it a free +14 prowess.

### 4.3 Effects

Read XP as a value with `"has_trait_xp(eotg_cybernetics)"`. Precedents: the skill's `triggers.md:205`, and `game/common/scripted_effects/00_commander_effects.txt:617–623`. Guard `add_trait_xp` with `has_trait` (`00_accolades_scripted_effects.txt:6524–6537`). Negative `add_trait_xp` values, needed for regression, appear in vanilla at `00_interaction_effects.txt:4201–4205`.

- **`eotg_aug_set_integration_effect = { XP = n }`** (n ∈ {0, 50, 100}): if `has_trait = eotg_cybernetics`, run `add_trait_xp = { trait = eotg_cybernetics value = { value = $XP$ subtract = "has_trait_xp(eotg_cybernetics)" } }`, then `eotg_aug_refresh_synergy_effect = yes`.
- **`eotg_aug_clear_synergy_effect`**: the 15 `remove_character_modifier` lines.
- **`eotg_aug_refresh_synergy_effect`**: run `eotg_aug_clear_synergy_effect = yes`, then:
  - `if eotg_is_aug_tier3` → OC set;
  - `else_if eotg_is_aug_tier2` → ENH set;
  - `else_if eotg_is_aug_tier1` → AUG set.

  Each set uses the same `highest_skill` ladder and martial fallback as today. It applies nothing to Neurofractured or unaugmented characters.
- **`eotg_aug_initiate_effect`**: `add_trait = eotg_cybernetics`, then `eotg_aug_refresh_synergy_effect = yes`.

The engine has no on_action for a track level change; `traits_on_actions.txt` has only `on_trait_gained` / `on_trait_lost`. That is why the synergy refresh lives inside `eotg_aug_set_integration_effect`, and why nothing else may change tier.

### 4.4 Modifier decisions

| Effect today | Goes to | Why |
|---|---|---|
| Fixed stats of the 3 tier traits | **track levels** (§4.1) | They are static per tier. |
| Tier synergy (15 keys) | **stays a character modifier**, applied by `eotg_aug_refresh_synergy_effect` | It depends on `highest_skill`. Track levels accept only static modifiers plus `culture_modifier` / `faith_modifier`. |
| Neurofracture distortion (5 keys) | stays a character modifier | NF has no track, and the distortion depends on skill. |
| Calibrated / illegal implants / regression recovery / withdrawn | stay | They are timed or event-specific. |
| Timed intrigue bonus in tier2.001.a / tier2.006.a | `eotg_mod_aug_affect_dampened` | **QA (a).** Adding a modifier the character already holds permanently, with `years =`, refreshes or overwrites that instance instead of stacking. Separate key, same value (intrigue +2). |
| Timed martial bonus in tier3.003.b / tier3.005.a | `eotg_mod_aug_running_hot` | **QA (a)**, same mechanism. Same values (martial +3, stress_gain_mult +0.1). |
| NF distortion icons | `martial_negative`, `stewardship_negative`, `intrigue_negative`, `learning_negative`, `diplomacy_negative` | **QA (b).** All five `.dds` files exist in `game/gfx/interface/icons/modifiers/`. |
| Knights augmented via init.002.c and tier1.004.a | `eotg_aug_initiate_effect` in the knight's scope; the knight pick requires `eotg_is_augmented_any = no` | **QA knight gap.** Without the filter, `add_trait` can silently do nothing on an already-augmented knight, or clash with `opposites` on a Neurofractured one. |

`eotg_clean_all_aug_modifiers` gets the two new keys. It has no caller today, and that stays as is.

---

## 5. File placement and rewrite table

No new folders are needed. Touched files:
- `common/{traits,scripted_triggers,scripted_effects,modifiers,decisions,on_action}/eotg_augmentation_*.txt`
- `events/eotg_augmentation_{initiation,tier1,tier2,tier3}.txt`
- `localization/english/eotg_augmentation_l_english.yml`

`events/eotg_augmentation_fracture.txt` needs **no** change.

Line numbers are as of the 2026-10-02 lift. The table is exhaustive for:
- every `has_trait` / `add_trait` / `remove_trait` on the four augmentation traits;
- every `eotg_apply_edu_synergy_*` call;
- every timed reuse of a synergy key.

**No event option gains an XP call.** The only XP changes are the band-crossing rows below.

### 5.1 `common/traits/eotg_augmentation_traits.txt`

| Line | Today | Replacement |
|---|---|---|
| 2–5 | header describing the 3-trait chain | header: XP takes exactly 0/50/100; deltas stack; only `eotg_aug_set_integration_effect` changes XP |
| 8–23 (superseded) | `eotg_augmented = {…}` | delete; replaced by `eotg_cybernetics` (§4.1) |
| 25–43 (superseded) | `eotg_enhanced = {…}` | delete |
| 45–63 (superseded) | `eotg_overclocked = {…}` | delete |
| 78 (superseded) | `opposites = { eotg_augmented eotg_enhanced eotg_overclocked }` | `opposites = { eotg_cybernetics }`, plus `icon` and `shown_in_ruler_designer = no` (§4.2) |

### 5.2 `common/scripted_triggers/eotg_augmentation_triggers.txt`

| Line | Today | Replacement |
|---|---|---|
| 7–12 (superseded) | `OR = { has_trait = eotg_augmented … eotg_neurofractured }` | `OR = { has_trait = eotg_cybernetics  has_trait = eotg_neurofractured }` |
| 31 (superseded) | `has_trait = eotg_augmented` | `eotg_is_aug_tier1 = yes` (no XP condition) |
| 41 (superseded) | `has_trait = eotg_enhanced` | `eotg_is_aug_tier2 = yes` (no XP condition) |
| 51 (superseded) | `has_trait = eotg_overclocked` | `eotg_is_aug_tier3 = yes` |
| new | n/a | `eotg_is_aug_tier1/2/3` (§3.1) |

### 5.3 `common/scripted_effects/eotg_augmentation_effects.txt`

| Line | Today | Replacement |
|---|---|---|
| 5–36 (superseded) | `eotg_apply_edu_synergy_augmented` | delete |
| 38–74 (superseded) | `eotg_apply_edu_synergy_enhanced` | delete |
| 76–112 (superseded) | `eotg_apply_edu_synergy_overclocked` | delete |
| new | n/a | `eotg_aug_clear_synergy_effect`, `eotg_aug_refresh_synergy_effect`, `eotg_aug_initiate_effect`, `eotg_aug_set_integration_effect` (§4.3) |
| 116–120 | 5× `remove_character_modifier = eotg_mod_oc_*_bonus` | `eotg_aug_clear_synergy_effect = yes` |
| 148–173 | `eotg_clean_all_aug_modifiers` | add removes for `eotg_mod_aug_affect_dampened` and `eotg_mod_aug_running_hot` |
| 187 (superseded) | `remove_trait = eotg_overclocked` | `remove_trait = eotg_cybernetics` |
| 188 | `add_trait = eotg_neurofractured` | unchanged |

### 5.4 `common/modifiers/eotg_augmentation_modifiers.txt`

| Line | Today | Replacement |
|---|---|---|
| 101 | `icon = martial_positive` | `icon = martial_negative` |
| 107 | `icon = stewardship_positive` | `icon = stewardship_negative` |
| 113 | `icon = intrigue_positive` | `icon = intrigue_negative` |
| 119 | `icon = learning_positive` | `icon = learning_negative` |
| 125 | `icon = diplomacy_positive` | `icon = diplomacy_negative` |
| new | n/a | `eotg_mod_aug_affect_dampened`, `eotg_mod_aug_running_hot` (§3.1) |

### 5.5 `common/decisions/eotg_augmentation_decisions.txt`

| Line | Today | Replacement |
|---|---|---|
| 4–5 | header | "Enhanced → Augmented (XP to 0)", "Overclocked → Enhanced (XP to 50)" |
| 16 (superseded) | `has_trait = eotg_enhanced` | `eotg_is_aug_tier2 = yes` |
| 31–32 (superseded) | `remove_trait = eotg_enhanced` / `add_trait = eotg_augmented` | `eotg_aug_set_integration_effect = { XP = 0 }` |
| 33–38 (superseded) | `eotg_apply_edu_synergy_augmented = yes` + 5× remove `eotg_mod_enh_*` | delete |
| 62 (superseded) | `has_trait = eotg_overclocked` | `eotg_is_aug_tier3 = yes` |
| 77–78 (superseded) | `remove_trait = eotg_overclocked` / `add_trait = eotg_enhanced` | `eotg_aug_set_integration_effect = { XP = 50 }` |
| 79–84 (superseded) | `eotg_apply_edu_synergy_enhanced = yes` + 5× remove `eotg_mod_oc_*` | delete |
| 85 | `eotg_mod_oc_regression_recovery` | unchanged |
| 110–114 (superseded) | `OR = { has_trait = eotg_augmented / eotg_enhanced / eotg_overclocked }` | `has_trait = eotg_cybernetics` |
| 132 (superseded) | `limit = { has_trait = eotg_overclocked }` | `limit = { eotg_is_aug_tier3 = yes }` |
| 141 (superseded) | `has_trait = eotg_overclocked` | `eotg_is_aug_tier3 = yes` |
| 147 (superseded) | `modifier = { add = 30  has_trait = eotg_overclocked }` | `modifier = { add = 30  eotg_is_aug_tier3 = yes }` |

### 5.6 `common/on_action/eotg_augmentation_on_actions.txt`

| Line | Today | Replacement |
|---|---|---|
| 1–32 | header | add one line: the tier is the XP on `eotg_cybernetics` (0/50/100), read through `eotg_is_aug_tier1/2/3`. Everything else unchanged. |
| 104 (superseded) | `any_vassal = { has_trait = eotg_augmented }` | `any_vassal = { has_trait = eotg_cybernetics }` (Q5) |
| 105 (superseded) | `any_courtier = { is_alive = yes  has_trait = eotg_augmented }` | `… has_trait = eotg_cybernetics }` |
| 124 (superseded) | `has_trait = eotg_augmented` | `eotg_is_aug_tier1 = yes` |
| 136 (superseded) | `has_trait = eotg_augmented` | `eotg_is_aug_tier1 = yes` |
| 156 | `trigger = { any_knight = { is_alive = yes } }` | `trigger = { any_knight = { is_alive = yes  eotg_is_augmented_any = no } }` |
| 183 (superseded) | `has_trait = eotg_enhanced` | `eotg_is_aug_tier2 = yes` |
| 235 (superseded) | `limit = { has_trait = eotg_overclocked }` | `limit = { eotg_is_aug_tier3 = yes }` |
| 307 (superseded) | `any_vassal = { is_alive = yes  has_trait = eotg_overclocked }` | `… eotg_is_aug_tier3 = yes }` |
| 308 (superseded) | `any_courtier = { is_alive = yes  has_trait = eotg_overclocked }` | `… eotg_is_aug_tier3 = yes }` |
| 330 | `has_trait = eotg_neurofractured` | unchanged |

### 5.7 `events/eotg_augmentation_initiation.txt`

| Line | Today | Replacement |
|---|---|---|
| 14 | header "adds a tier trait" | "adds `eotg_cybernetics` at XP 0" |
| 38 + 40 (superseded) | `add_trait = eotg_augmented` … `eotg_apply_edu_synergy_augmented = yes` | `eotg_aug_initiate_effect = yes` (keep line 39, heal wounds, and the risk set) |
| 113 + 114 | same pair | `eotg_aug_initiate_effect = yes` |
| 149 | `trigger = { any_knight = { is_alive = yes } }` | `… is_alive = yes  eotg_is_augmented_any = no …` |
| 151 | `limit = { is_alive = yes }` | `limit = { is_alive = yes  eotg_is_augmented_any = no }` |
| 152 (superseded) | `add_trait = eotg_augmented` (knight) | `eotg_aug_initiate_effect = yes` (knight synergy fix) |
| 181 + 182 | same pair | `eotg_aug_initiate_effect = yes` |
| 234 + 237 | same pair | `eotg_aug_initiate_effect = yes` (keep line 235, illegal implants, and line 236, heal wounds) |
| 293 (superseded) | `any_vassal = { has_trait = eotg_augmented }` | `… has_trait = eotg_cybernetics …` |
| 294 (superseded) | `any_courtier = { is_alive = yes  has_trait = eotg_augmented }` | `… has_trait = eotg_cybernetics …` |
| 301 (superseded) | `limit = { any_vassal = { has_trait = eotg_augmented } }` | `… eotg_cybernetics …` |
| 303 (superseded) | `limit = { has_trait = eotg_augmented }` | `limit = { has_trait = eotg_cybernetics }` |
| 309 (superseded) | `limit = { is_alive = yes  has_trait = eotg_augmented }` | `… has_trait = eotg_cybernetics }` |
| 319 + 320 | same pair | `eotg_aug_initiate_effect = yes` |

### 5.8 `events/eotg_augmentation_tier1.txt`

| Line | Today | Replacement |
|---|---|---|
| 96–98 (002.a) (superseded) | `remove_trait = eotg_augmented` / `add_trait = eotg_enhanced` / `eotg_apply_edu_synergy_enhanced = yes` | `eotg_aug_set_integration_effect = { XP = 50 }` |
| 241–243 | `trigger = { any_knight = { is_alive = yes } }` | `… is_alive = yes  eotg_is_augmented_any = no …` (matches on_action line 156) |
| 248 | `limit = { is_alive = yes }` | `limit = { is_alive = yes  eotg_is_augmented_any = no }` |
| 258 (superseded) | `add_trait = eotg_augmented` (knight) | `eotg_aug_initiate_effect = yes` (knight synergy fix) |

### 5.9 `events/eotg_augmentation_tier2.txt`

| Line | Today | Replacement |
|---|---|---|
| 38 (001.a) | `modifier = eotg_mod_enh_intrigue_bonus  years = 3` | `modifier = eotg_mod_aug_affect_dampened  years = 3` (QA a) |
| 139–141 (003.a) (superseded) | `remove_trait = eotg_enhanced` / `add_trait = eotg_overclocked` / `eotg_apply_edu_synergy_overclocked = yes` | `eotg_aug_set_integration_effect = { XP = 100 }` |
| 181–183 (003.c) | same three lines | `eotg_aug_set_integration_effect = { XP = 100 }` (keep the risk +5 on line 180) |
| 369 (006.a) | `modifier = eotg_mod_enh_intrigue_bonus  years = 2` | `modifier = eotg_mod_aug_affect_dampened  years = 2` (QA a) |

### 5.10 `events/eotg_augmentation_tier3.txt`

| Line | Today | Replacement |
|---|---|---|
| 176 (003.b) | `modifier = eotg_mod_oc_martial_bonus  years = 2` | `modifier = eotg_mod_aug_running_hot  years = 2` (QA a) |
| 285 (005.a) | `modifier = eotg_mod_oc_martial_bonus  years = 1` | `modifier = eotg_mod_aug_running_hot  years = 1` (QA a) |
| 411 (superseded) | `any_vassal = { is_alive = yes  has_trait = eotg_overclocked }` | `… eotg_is_aug_tier3 = yes …` |
| 412 (superseded) | `any_courtier = { is_alive = yes  has_trait = eotg_overclocked }` | `… eotg_is_aug_tier3 = yes …` |
| 428 (superseded) | `limit = { any_vassal = { is_alive = yes  has_trait = eotg_overclocked } }` | `… eotg_is_aug_tier3 = yes …` |
| 430 (superseded) | `limit = { is_alive = yes  has_trait = eotg_overclocked }` | `limit = { is_alive = yes  eotg_is_aug_tier3 = yes }` |
| 436 (superseded) | `limit = { is_alive = yes  has_trait = eotg_overclocked }` | `limit = { is_alive = yes  eotg_is_aug_tier3 = yes }` |

---

## 6. Wiring and vanilla precedent

**Wiring is unchanged.** `yearly_playable_pulse` (additive) fires the five `eotg_on_yearly_aug_*` on_actions. Cooldown flags are set and checked only there.

The event-trigger edits in §5.7, §5.8 and §5.10 are world-state guards. Each one mirrors its on_action branch trigger exactly, which lesson 5 allows. No on_action gains a new line beyond those rewrites.

Knights augmented by events are not count+, so the yearly pulse never fires for them. They stay at XP 0, the same reach as today.

| Need | Vanilla precedent | Used for |
|---|---|---|
| One trait with a track and per-level name/desc | `game/common/traits/00_traits.txt:1178` `lifestyle_blademaster` | §4.1 |
| Track levels stack | `00_traits.txt:16476–16490` `tourney_participant` `foot` | §4.1 delta table |
| Health-category trait with tracks | `00_traits.txt:6039` `infirm` | `category = health` |
| Reading XP as a value | `00_commander_effects.txt:617–623`; skill `triggers.md:205` | §4.3 |
| Guarding `add_trait_xp` with `has_trait` | `00_accolades_scripted_effects.txt:6524–6537` | §4.3 |
| Negative `add_trait_xp` | `00_interaction_effects.txt:4201–4205` | regression to 0 / 50 |
| Old tier traits mapped onto a track | `trait_conversion.lookup` | not followed (no saves) |
| Loc shape | `game/localization/english/traits_l_english.yml:139–147, 1258, 1303–1304` | §7 |

Field names were checked against `ck3-modding/reference/common/traits/_traits.info`: `track`, `name`/`desc`/`icon` blocks, `shown_in_ruler_designer`, `opposites`, `category = health`.

---

## 7. Loc surface (`localization/english/eotg_augmentation_l_english.yml`, owner eotg-localizer)

UTF-8 with BOM, one definition per key, no `replace/` overrides.

**Removed (6; superseded, deliberately absent):** `trait_eotg_augmented`, `trait_eotg_augmented_desc`, `trait_eotg_enhanced`, `trait_eotg_enhanced_desc`, `trait_eotg_overclocked`, `trait_eotg_overclocked_desc`.

**Added (track trait, 10):**

| Key | Content |
|---|---|
| `trait_eotg_cybernetics` | Generic name, shown where no character exists: "Cybernetic Augmentation" |
| `trait_eotg_cybernetics_1` | "Augmented" |
| `trait_eotg_cybernetics_2` | "Enhanced" |
| `trait_eotg_cybernetics_3` | "Overclocked" |
| `trait_eotg_cybernetics_1_desc` | Reuse the text of the old `trait_eotg_augmented_desc` (that key is superseded) |
| `trait_eotg_cybernetics_1_character_desc` | Reuse the old Augmented desc. If you add the character's name, use the vanilla trait-tooltip form `[ROOT.GetCharacter.GetFirstNameNoTooltip]` (`traits_l_english.yml:141`), never `[scope:x]`. |
| `trait_eotg_cybernetics_2_character_desc` | Reuse the old Enhanced desc |
| `trait_eotg_cybernetics_3_character_desc` | Reuse the old Overclocked desc |
| `trait_track_eotg_cybernetics` | "Integration" |
| `trait_track_eotg_cybernetics_desc` | One line on how deeply the implants are wired in |

Do not add `trait_eotg_cybernetics_2_desc` / `_3_desc` (not built, on purpose). They can never be shown, and vanilla comments out its own equivalents.

**Added (modifiers, 4):**
- `eotg_mod_aug_affect_dampened` "Affect Dampened", plus `eotg_mod_aug_affect_dampened_desc`
- `eotg_mod_aug_running_hot` "Running Hot", plus `eotg_mod_aug_running_hot_desc`

Both descs should read as temporary states.

**Kept, text revised:**
- `eotg_decision_partial_removal_tooltip`: Integration falls to Augmented, and the tier synergy is replaced.
- `eotg_decision_overclock_regression_tooltip`: Integration falls to Enhanced; withdrawal lasts 5 years.
- `eotg_decision_maintenance_protocol_tooltip`: no number and no word "risk". Use "static" wording that the lore-keeper has approved, e.g. "Applies Calibrated Systems for 3 years. If Overclocked, the static quiets." "Static" is augmentation-only vocabulary; do not reuse it in other systems' loc.

**Unchanged:** `trait_eotg_neurofractured` (+`_desc`) and all other modifier, opinion and event keys.

---

## 8. Lore constraints and map-agnostic check

- Canon (`SETTING LORE` lines ~114, 305, 464, 565, 631) establishes only that cybernetic augmentation exists and is developing. Level names carry over from v1.
- Lore-keeper approved, 2026-10-03:
  - the track label "Integration";
  - "Affect Dampened" and "Running Hot";
  - "static" as augmentation-only vocabulary;
  - Overclocked's health loss as intentional.
- **Map-agnostic: confirmed.** The design references no title, province, character, culture or faith. The only things it reads from the world are:
  - `capital_county.development_level` (unchanged);
  - vanilla personality traits;
  - relationship scopes;
  - the mod's own flags and variables.
- The v1 culture-reaction table stays deferred.

---

## 9. Definition of done (QA-testable)

1. `grep -rnE 'eotg_(augmented|enhanced|overclocked)\b' common events localization` returns nothing.
2. `grep -rn 'eotg_apply_edu_synergy_' common events` returns nothing.
3. `grep -rnE 'eotg_mod_(enh_intrigue|oc_martial)_bonus +years' events` returns nothing.
4. The five `eotg_mod_nf_*_distortion` modifiers use `*_negative` icons.
5. `add_trait_xp` appears **only** inside `eotg_aug_set_integration_effect`, under a `has_trait = eotg_cybernetics` guard. Every call site passes `XP = 0`, `50` or `100`: tier1.002.a, tier2.003.a, tier2.003.c and the two decisions. No `monthly_track_xp_degradation` anywhere.
6. All 31 events are reachable from the same on_action branches, with the same gates as before (QA reachability audit).
7. Resource coupling (QA audit 8): the set of passing events is unchanged from the 2026-10-02 PASS.
8. Both knight paths (init.002.c and tier1.004.a) call `eotg_aug_initiate_effect`, and both knight picks exclude augmented knights.
9. Tiger 1.17.0 clean except the known-benign list. In particular, no `unknown trait`, `unknown modifier`, missing-loc or unknown-field reports in `eotg_augmentation_*` files.
10. Every key in §7 "Added" is defined once, the BOM is present, and there is no `[scope:`. The 6 removed keys are gone.
11. **Human, in game:**
    - Console `add_trait eotg_cybernetics` on a count → the tooltip reads "Augmented", shows an "Integration" bar, and gives +2 prowess.
    - Add 50 XP → "Enhanced", prowess +4, diplomacy −2, enemy scheme phase +5.
    - Add 50 more → "Overclocked", prowess +8, enemy scheme phase still +5, no health bonus.
    - Neurofractured does not appear in the ruler designer.
    - Partial Removal on an Enhanced ruler → "Augmented" at XP 0, with exactly one `eotg_mod_aug_*_bonus` active.

---

## 10. Deferred

| Item | Why |
|---|---|
| XP that moves within a tier (drift, option nudges, readiness gates) | Rejected by the human 2026-10-03 (Q2). This was the architect's original proposal; the design is recorded in git history if it is ever revisited. |
| Per-level track icons | Q3: 2 icons. Possible later with the `tourney_participant` icon block. |
| A qualitative hint that shows the risk | Keeps the risk hidden (Q1). Needs its own design call. |
| `trait_conversion.lookup` | No saves exist. |
| An `on_trait_gained` hook for synergy | Revisit when history characters start with the trait (after Gate 1), because history `trait =` lines bypass `eotg_aug_initiate_effect`. |
| History characters starting at a given level | Needs Gate 1 characters, then `add_trait_xp` in a history effect. |
| Culture/religion reaction table | Blocked by the map-agnostic rule. |
| Callers for `eotg_clean_all_aug_modifiers` | No full-removal path exists. |
| Building gates, Nikios interaction | Post-beta; Nikios is deferred by the owner. |

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Implement `docs/specs/cybernetics_track.md` §4–§5 from the rewrite table (thresholds-only XP, `eotg_aug_set_integration_effect` as the only path for changing tier); then eotg-localizer does §7.
- files: docs/specs/cybernetics_track.md
- needs-loc: trait_eotg_cybernetics, trait_eotg_cybernetics_1/_2/_3, trait_eotg_cybernetics_1_desc, trait_eotg_cybernetics_1/_2/_3_character_desc, trait_track_eotg_cybernetics(+_desc), eotg_mod_aug_affect_dampened(+_desc), eotg_mod_aug_running_hot(+_desc); revise eotg_decision_partial_removal_tooltip, eotg_decision_overclock_regression_tooltip, eotg_decision_maintenance_protocol_tooltip; remove trait_eotg_{augmented,enhanced,overclocked}(+_desc)
- needs-lore: none
- needs-human: supply eotg_cybernetics.dds and eotg_neurofractured.dds; in-game check §9 item 11 after implementation
