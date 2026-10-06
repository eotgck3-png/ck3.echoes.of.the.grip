# Spec: Unclaimed Regions (Frontier, "Option B")

**Author:** eotg-architect, 2026-10-06. **Status: design approved by the owner 2026-10-06 (see §D). Batches 1 and 2 built on branch `claude/frontier-unclaimed-cloud` (cloud, static, unvalidated); NOT merged. Build notes and deviations: §20.** Owner decision 2026-10-06, "Option B": Unsettled space has **no ruler**. The engine still needs a holder for every county, so each unclaimed county is held by a **passive placeholder**, which stands for the scattered people living there and is not a ruler. A ruler must **claim** the county before Establishing a Frontier there. An abandoned Frontier goes back to unclaimed. Unclaimed space is hard on armies passing through. Impassable or void provinces that are not counties stay scenery.

**Supersedes:** [`frontier_v1.md`](frontier_v1.md) §2.3 option (a), *for unclaimed counties only*. Phase 1's owned-county Unsettled path (`eotg_frontier_mark_unsettled_effect` on a county someone already holds) stays as it is, as a separate case (§6.3).

**Inputs:** the research in [`research/unclaimed_regions_vanilla_2026-10-06.md`](research/unclaimed_regions_vanilla_2026-10-06.md) (cited as *R§n*); [`docs/design/frontier_systems.md`](../design/frontier_systems.md) §3, §12, §13; [`frontier_v1.md`](frontier_v1.md) §R, §V, §2.5, §4; [`frontier_v2.md`](frontier_v2.md) §V; Phase 3a on `origin/claude/frontier-v3-cloud:docs/specs/frontier_v3.md` (unmerged). Vanilla is 1.20.0.3, `G` = the game root. I re-checked every vanilla citation below against the installed files during this session. Where I went beyond the research, the line says **(new)**.

**Size (proposed):** 1 government, 1 trait, 1 character template, 1 county modifier, 1 character interaction, 2 debug decisions, about 10 scripted effects, 6 triggers, 5 script values, 4 additive vanilla hooks, 2 Frontier-hook listeners, 2 new empty hooks, **1 key-level vanilla trigger override**, and about 30 loc keys. **No events, no gfx.** Two batches (§13).

---

## D. Owner decisions (2026-10-06). These bind and override §19's open questions and §15's placeholders.

The owner accepted every orchestrator recommendation ("follow your recommendations").

- **UQ1, playability.** Accept the risk with this spec's mitigations. Batch 1 probes whether placeholders are
  playable. If they are, add the trigger override that keeps placeholders out of vanilla yearly events, plus the
  lobby warning. Do NOT override vanilla `herder_government`.
- **UQ2, war immunity.** Use our own flag `eotg_government_is_unclaimed` plus the key-level override of
  `herders_and_tributary_constraints` (§4.4). Do NOT reuse `government_is_herder`: vanilla
  `mpo_retrieve_land_from_herder_interaction` would let the AI take unclaimed land without our pacing.
- **UQ3, authoring.** One history seed (`eotg_unclaimed_seed`), split at game start into one placeholder per county.
- **UQ5, release.** A capital county stays with its holder on abandonment. Both failed and voluntary abandonment
  release a claimed county back to unclaimed.
- **UQ7, attrition.** `supply_limit_mult_for_others = -0.5` on the government, plus `supply_limit_mult = -0.25` on
  Phase 1's Unsettled modifier for owned counties. Tune after playtesting.
- **UQ4, UQ6, UQ8, UQ10, UQ11.** The spec's own defaults.
- **UQ9, names (lore).** Placeholders keep random names from their culture (real people, not "nobodies"). A fixed
  pattern, if one is ever needed, is "the Unsworn of [county]".
- **Names (lore-keeper, UL2 and UL3):**
  - the status and modifier is **"Unclaimed Region"**;
  - the people and trait `eotg_unclaimed_folk` are **"the Unsworn"**;
  - the interaction is **"Raise Your Colours"**, not "Stake a Claim". CK3's [claim|E] concept means a claim
    pressed in war, and this interaction leaves none. The keys can stay `eotg_unclaimed_*`.
  - Interaction description: "Pay for the crews, the guns and the flag, and this Region is yours for as long as
    you can hold it. Nobody else has to agree, and nobody is obliged to respect it."
- **UL1, culture and faith.** Placeholders copy the county's culture and faith by scope (no neutral culture).
  The cartographer picks real drifter peoples from the briefs (e.g. Uvreki, Tangentine). Which counties start
  unclaimed is a vault question; never guess it.
- **Text rules (ERRATA LAW AT 866):**
  - never say a claim is filed, registered, recognized, licensed or chartered, or that others must respect it;
  - write "Region" (a county), not "system", for the claimed unit;
  - keep "Council" and "Frontier Guard" out of this system's text;
  - don't present unclaimed space as where the Titan Exodus lands;
  - the Myr is a war zone at 866, not empty land.
- **No ERRATA entry is added for now;** the premise is recorded here instead. The lore-keeper's draft
  ("UNCLAIMED SPACE AT 866") is available if the owner wants it in canon later.

---

## 1. Purpose and gate

- **The loop this adds:** *Unclaimed* → **Claim** → owned Unsettled → (Phase 1) Establish → Frontier → Settled. If the Frontier is abandoned, the county is **released** back to Unclaimed and keeps its Abandoned traces.
- **Unclaimed is a political status, not a Frontier state.** A county that is Unclaimed is always Unsettled (or Abandoned) in Phase 1's terms, but an Unsettled county is not necessarily Unclaimed: Phase 1's owned Unsettled counties stay owned.
- **Gate:** Gate 3 (Systems). This is a **mod-exclusive system**, built and tested against the temporary map and the vanilla test sub-mod before Gate 1 closes (`docs/agent_workflow.md` §5 rule 2). **It is not blocked.** It must stay map-agnostic: mod script names no title, province, character, culture or faith key. Which counties *start* unclaimed is history data, which is the cartographer's job at Gate 1 (§10).
- **Standalone with respect to the rest of the mod:** it needs Frontier Phase 1 (`eotg_frontier_mark_unsettled_effect`, the `eotg_frontier_on_abandoned` / `_on_settled` hooks). It does not need Phases 2 or 3a, and reads no cybernetics state.

---

## 2. Signature resource

**The county title variable `eotg_unclaimed_county` (value `yes`). If it is present, the county is Unclaimed.** It is the one fact the system turns on:
- **set** only by `eotg_unclaimed_release_effect` (game start, abandonment, debug);
- **removed** only by `eotg_unclaimed_on_claimed_effect` (whatever moved the title);
- **read** by the claim interaction (`is_shown`), the yearly sweep, the Phase 1 establish guard, the debug readout and the title-gain catch-all.

The placeholder character is a *consequence* of the variable. It is never the source of truth: a placeholder can die or be replaced, and the county stays Unclaimed.

A second, permanent-until-settled county variable, **`eotg_unclaimed_claimed`**, records that a county came out of unclaimed space. Only counties that carry it go back to Unclaimed on abandonment (§6).

**There are no flavour events in this system** (the owner decides on event expansion). Every effect listed in §3.3 moves or reads `eotg_unclaimed_county`.

---

## 3. Identifier table

All identifiers are new and carry the `eotg_` prefix. There are **no landed titles**. **There is no event namespace** (no events).

### 3.1 Data objects
| Type | Key | Notes |
|---|---|---|
| government | `eotg_unclaimed_government` | §4 |
| government flag | `eotg_government_is_unclaimed` | the identity flag; read by the war override and `eotg_is_unclaimed_holder` |
| trait | `eotg_unclaimed_folk` | blockers: marriage, children, inheritance (§5.4); it also marks a placeholder that has lost its land |
| character template | `eotg_unclaimed_holder_template` | §5.2; also the government's `generated_character_template` |
| history character | `eotg_unclaimed_seed` | **cartographer**, one per map (§5.1, §10). It is not in mod script; script finds it by government. |
| county modifier | `eotg_unclaimed_mod_unclaimed` | "Unclaimed Region": display and explanation; the fallback attrition line (§7) |
| title variable | `eotg_unclaimed_county` | **signature** (§2) |
| title variable | `eotg_unclaimed_claimed` | came from unclaimed; cleared on Settled or on release (§6) |
| global variable list | `eotg_unclaimed_counties` | every Unclaimed county; the sweep and the readout iterate it |
| global variable | `eotg_unclaimed_ai_gap` | timed (`eotg_unclaimed_ai_gap_days_value`): the worldwide AI claim throttle (§8.4) |
| saved scopes | `eotg_unclaimed_target` (county), `eotg_unclaimed_new_holder`, `eotg_unclaimed_old_holder`, `eotg_unclaimed_claimant`, `eotg_unclaimed_change` | internal; `_target`, `_claimant` and `_old_holder` are also the hook scopes (§9.3) |

### 3.2 Scripted triggers (`common/scripted_triggers/eotg_unclaimed_triggers.txt`)
| Key | Scope | True when |
|---|---|---|
| `eotg_is_unclaimed_folk` | character | `has_trait = eotg_unclaimed_folk` (landed or not) |
| `eotg_is_unclaimed_holder` | character | `government_has_flag = eotg_government_is_unclaimed`. **This is the shared exclusion trigger that every mod pulse and event entry uses** (§5.5). |
| `eotg_unclaimed_is_unclaimed` | county | `has_variable = eotg_unclaimed_county` |
| `eotg_unclaimed_in_reach` | county, `$ACTOR$` | the actor can claim this county (§8.2) |
| `eotg_unclaimed_can_claim` | character (actor) | landed, count or above, adult, free, not an unclaimed holder (§8.2) |
| `eotg_unclaimed_ai_may_claim` | character (AI actor) | §8.4 throttle |

### 3.3 Scripted effects (`common/scripted_effects/eotg_unclaimed_effects.txt`)
| Key | Scope | Does |
|---|---|---|
| `eotg_unclaimed_release_effect` | county | **The single entry point that makes a county Unclaimed** (game start, abandonment, debug, test sub-mods). Creates a placeholder (`_create_holder_effect`) and moves the title to it. Then: sets `eotg_unclaimed_county`, adds the county to the list, calls `eotg_frontier_mark_unsettled_effect` (which does nothing on an Abandoned county, so it stays resettlable), sets the neutral colour, adds `eotg_unclaimed_mod_unclaimed`, removes `eotg_unclaimed_claimed`, and fires `eotg_unclaimed_on_released` |
| `eotg_unclaimed_create_holder_effect` | county | Creates the placeholder: the MPO pattern (§4.6), with culture, faith and rite **taken from the county by scope**. Moves the county with `type = granted`, `add_claim_on_loss = no`. Then `change_government = eotg_unclaimed_government`, with the independence guard copied from MPO. Saves `scope:eotg_unclaimed_new_holder` |
| `eotg_unclaimed_on_claimed_effect` | county, `CLAIMANT`, `OLD` | Bookkeeping after **any** transfer out of unclaimed (§8.5): removes `eotg_unclaimed_county` and the list entry, sets `eotg_unclaimed_claimed`, removes `eotg_unclaimed_mod_unclaimed`, recolours, vanishes OLD (`_vanish_effect`), and fires `eotg_unclaimed_on_claimed` |
| `eotg_unclaimed_claim_effect` | character (actor), `TARGET` | The interaction's `on_accept`: pays gold and prestige, then moves TARGET to the actor (`type = granted`, `add_claim_on_loss = no`). The bookkeeping runs from `on_title_gain`, not from here (§8.5) |
| `eotg_unclaimed_vanish_effect` | character | If the character is folk and holds no landed title: `death = { death_reason = death_vanished }` |
| `eotg_unclaimed_on_holder_death_effect` | character (dying) | Every county the dying placeholder holds gets a new placeholder (§5.3) |
| `eotg_unclaimed_game_start_effect` | none | Splits the seed's holdings: one placeholder per county, then vanishes the seed (§5.1) |
| `eotg_unclaimed_sweep_effect` | none | The yearly safety net (§5.3, §8.5) |
| `eotg_unclaimed_set_neutral_colour_effect` | county | `set_title_color = { 88 92 100 }`. **The only place in script with the neutral colour literal** (§7.1) |
| `eotg_unclaimed_set_claimed_colour_effect` | county, `CLAIMANT` | Recolours on claim (§7.2) |
| `eotg_unclaimed_debug_readout_effect` | character | Toasts the probe results (§12, V-U1) |

### 3.4 Script values (`common/script_values/eotg_unclaimed_values.txt`)
| Key | Value | Notes |
|---|---|---|
| `eotg_unclaimed_claim_gold_value` | `minor_gold_value` | the actor's scope (Phase 1 E20) |
| `eotg_unclaimed_claim_prestige_value` | `minor_prestige_value` (75) | as vanilla `mpo_retrieve_land_from_herder_interaction` |
| `eotg_unclaimed_reach_value` | `squared_distance_medium` (62500) | non-adjacent reach (§8.2); a map knob |
| `eotg_unclaimed_ai_gap_days_value` | 180 | at most about 2 AI claims a year, worldwide |
| `eotg_unclaimed_ai_hold_cap_value` | 2 | an AI may hold at most this many counties that are still `eotg_unclaimed_claimed` (claimed but not settled) |

### 3.5 Interaction, decisions, hooks
| Type | Key | Notes |
|---|---|---|
| character interaction | `eotg_unclaimed_claim_interaction` | "Stake a Claim" (working name; localizer and lore-keeper). Recipient = a placeholder (§8) |
| decision (debug) | `eotg_decision_unclaimed_debug_release` | `debug_only = yes`. Releases the taker's least-developed held county that is not their capital |
| decision (debug) | `eotg_decision_unclaimed_debug_readout` | `debug_only = yes`. The probe readout (V-U1, V-U3) |
| on_action (vanilla, additive) | `on_game_start` → `eotg_unclaimed_on_game_start` | §5.1 |
| on_action (vanilla, additive) | `on_title_gain` → `eotg_unclaimed_on_title_gain` | the catch-all (§8.5) |
| on_action (vanilla, additive) | `on_death` → `eotg_unclaimed_on_death` | §5.3 |
| on_action (vanilla, additive) | `yearly_global_pulse` → `eotg_unclaimed_on_yearly_sweep` | §5.3, §8.5 |
| on_action (Frontier hook, additive) | `eotg_frontier_on_abandoned` → `eotg_unclaimed_on_frontier_abandoned` | §6.1 |
| on_action (Frontier hook, additive) | `eotg_frontier_on_settled` → `eotg_unclaimed_on_frontier_settled` | §6.2 |
| on_action (new hook, empty) | `eotg_unclaimed_on_claimed`, `eotg_unclaimed_on_released` | for later systems; root = the new holder; scopes in §9.3 |
| **vanilla key override** | `herders_and_tributary_constraints` | §4.3. In `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt` |
| vanilla key override (**conditional**) | `basic_is_valid_for_yearly_events_trigger` | only if V-U1 finds placeholders playable (§4.5 M2) |

### 3.6 Phase 1 identifiers touched (additive; each with its reason)
| Key | Change | Reason |
|---|---|---|
| `eotg_frontier_can_establish` | add `NOT = { has_variable = eotg_unclaimed_county }` | defence in depth: placeholders can't take decisions anyway, but the rule is "gate on role at every tier" |
| `eotg_frontier_mod_unsettled` | add `supply_limit_mult = -0.25` (**owner question UQ7**) | owned Unsettled counties also slow armies (§7.3) |
| `eotg_decision_frontier_abandon`, `eotg_frontier.005` option (a) | add a custom tooltip `eotg_unclaimed_abandon_returns_tt`, shown only when the Region has `eotg_unclaimed_claimed` | the player must see that abandoning gives the Region up |

Nothing else in Phases 1–3a changes. The release and settle logic attaches to the existing **hooks**, as design §14 intends.

---

## 4. The placeholder government: `eotg_unclaimed_government`

### 4.1 Definition (shape: vanilla `herder_government`, `G/common/governments/00_government_types.txt:733-792`)
```
eotg_unclaimed_government = {
    generated_character_template = eotg_unclaimed_holder_template
    government_rules = {
        court_generate_spouses = no
        council = no
        create_cadet_branches = no
        rulers_should_have_dynasty = no
        inherit_from_dynastic_government = no   # fenced off, as holy orders and mercenaries are (:327-400)
        legitimacy = no
        use_title_tier_modifiers = no
        deny_powerful_vassal = yes
        buildings = no
        allow_accolades = no
        dynasty_named_realms = no
    }
    court_generate_commanders = no
    character_modifier = {
        knight_limit = -100          # herder
        county_opinion_add = 100     # herder: no revolts against nobody
        monthly_income_mult = -10    # herder: no treasury, so no MAA
        levy_size = -1               # (new) no levies in military-strength sums
    }
    primary_holding = castle_holding
    valid_holdings = { city_holding church_holding tribal_holding }
    can_get_government = { has_trait = eotg_unclaimed_folk }   # (new) see 4.2
    ai = {
        use_lifestyle = no  arrange_marriage = no  use_goals = no  use_decisions = no
        use_scripted_guis = no  use_legends = no  perform_religious_reformation = no
        use_great_projects = no
    }
    flags = { eotg_government_is_unclaimed  cannot_be_vassal_or_liege }
    supply_limit_mult_for_others = -0.5     # §7
    color = { 88 92 100 }                   # the government map mode; same neutral as §7.1
}
```
- **Not set:** `mechanic_type`, `is_mechanic_type_default`, `uses_county_fertility`, `replenishes_county_fertility`, `fallback`, `vassal_contract_group`, `royal_court`.
  - **Why no mechanic_type or fertility:** they bring herd and fertility behaviour, and vanilla's no-MPO conversion (`G/common/on_action/game_start.txt:1249-1263`) turns `herder_government` into tribal. That conversion matches only `has_government = herder_government`, so a custom government is safe from it (R§1).
  - **Why no vassal contract:** the flag `cannot_be_vassal_or_liege` means a placeholder is never a liege or a vassal.
- **`fallback` is left unset.** Vanilla priorities start at 1 (`:16, :110, :480, :830`), so the default 0 is assumed to mean "not a fallback". V-U10 checks this.
- **Holdings:** castle is the primary holding, and every vanilla settled type is valid, so whatever capital the cartographer authors is legal. `buildings = no` stops construction. A custom "camp" holding is deferral UD4.
- **Tiger and PX don't validate 1.20 government fields** (R risk 8). QA checks this block by hand against `G/common/governments/_governments.info` and `herder_government`.

### 4.2 `can_get_government` (new)
The engine assigns governments when a character is landed. Vanilla guards holy orders with `can_get_government` "to prevent barons holding temple baronies from randomly getting holy order gov type" (`00_government_types.txt:436-441`). Gating on the trait means only placeholders can get this government. The template adds the trait, and so do the creation effects, **before** `change_government`. V-U10 checks that the gate doesn't block the scripted `change_government`.

### 4.3 War immunity: **recommendation: our own flag, plus a key-level override of `herders_and_tributary_constraints`**

| | **A. Reuse `government_is_herder`** | **B. Own flag + override the trigger (recommended)** |
|---|---|---|
| War immunity | free: the trigger already blocks herder defenders (`00_war_and_peace_triggers.txt:1144-1160`); 17 CB groups call it (R§2) | the trigger gains our flag on the defender side **and on the attacker side** (placeholders never declare war) |
| Vanilla overrides | none | **one key-level override** (a non-additive replacement; pitfalls entry in §4.4) |
| Side effects | the flag is read in **88 vanilla files**. Wanted: commoner clothing (`00_clothing_triggers.txt:1739, 1812, 1922`), alliance blocks (`00_alliance.txt:1794, 1808`), and exclusion from some yearly and religion sweeps (`yearly_on_actions.txt:2507`, `religion_on_actions.txt:1316, 1360`). **Unwanted (new):** vanilla **`mpo_retrieve_land_from_herder_interaction`** (`09_mpo_interactions.txt:7426`) is shown on *any* recipient with the herder flag. It is a second, vanilla claim path that costs only prestige. Its AI (`ai_will_do` +25 for any non-nomad with `massive_gold_value`, `ai_frequency_by_tier` duchy+ 4 months, targets `neighboring_rulers`) **would grab unclaimed space with none of our pacing caps**. Also the herder branches in revoke-title and grant rules, and MPO migration and coronation events. | none outside the trigger |
| Gate 2 risk | every future mod government that reads herder logic inherits the confusion | none |

**Why B:** the retrieve-land interaction turns the herder flag from "mostly harmless" into a pacing bug. Suppressing it would need a second override, of an interaction this time. B costs one 50-line trigger copy.

**Gaps that remain under either option (accepted):**
- **`independence` (CB group, `00_casus_belli_groups.txt:150`):** it needs a liege–vassal pair, and `cannot_be_vassal_or_liege` means a placeholder is never in one. Moot.
- **`migration` (`:171`):** `can_only_start_via_script`, fired only by MPO nomad events. The mod has no nomads. **Revisit if Gate 2 adds a nomad government.**
- **Raids** are not CB wars. Whether raiders can raid unclaimed counties is deferred (UD6).
- **Fabricated claims** on unclaimed counties are possible (the chancellor) but useless, since every claim CB is blocked. They are not suppressed.

**Vassalization and offers:** the flag `cannot_be_vassal_or_liege` (as on mercenary and holy order, `00_government_types.txt:348, 388, 431`) is checked by vassalize and offer (`00_character_interactions.txt:55, 577`), grant titles (`00_grant_titles_interaction.txt:33`), tributary interactions (`00_tributary_interactions.txt:273, 904, 4483`) and tributarize (`00_tributarize.txt:20-30`) (R§2).

### 4.4 Pitfalls entry (the orchestrator adds this to `docs/pitfalls.md` when the override ships)
> **N. A key-level override of a vanilla scripted trigger: `herders_and_tributary_constraints`.**
> **What:** `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt` redefines a vanilla key. It is a verbatim copy of `G/common/scripted_triggers/00_war_and_peace_triggers.txt` `herders_and_tributary_constraints` (1.20.0.3) plus two lines, each marked `# EOTG`: our flag in the defender `NOR`, and an attacker check. **It is a non-additive replacement.** Vanilla changes to that trigger are silently lost.
> **Confirm it loads:** `logs/database_conflicts.log` must show `Overriding entry 'herders_and_tributary_constraints'` naming our file. The same log already lists the mod's building overrides. If it is absent, the key-level override didn't take, and the fallback is a full copy of the vanilla file under its own name (which is worse).
> **Prevent:** after every CK3 update, diff the copied block against vanilla (§2's override sweep). The header of the file lists every overridden key and the vanilla version it was copied from.

### 4.5 Playability: **the top risk**
**What the evidence says (new):**
- The "Is unplayable" label is tied to the flags `government_is_republic`, `government_is_mercenary`, `government_is_holy_order` and `government_is_herder` (`G/localization/english/government_l_english.yml:272, 280, 281, 285`).
- **Republic has no `mechanic_type`** (`00_government_types.txt:64-92`) and is still unplayable. So unplayability does not come from `mechanic_type`.
- The four unplayable governments are hard-coded engine keys: every one is listed in `NGovernment.GOVERNMENT_TYPES` (`G/common/defines/00_defines.txt:550-573`), and the herder block says "This is referenced in code".
- **Inference: a custom government is most likely *playable*.** Its holder would then pass `is_playable_character`, get `yearly_playable_pulse`, and could be clicked in the lobby's free pick.

**Plan:** build A as specified, and probe it in Batch 1 (V-U1, through the debug readout). If the holder is playable, apply these mitigations:
- **M1. Mod pulses:** every mod on_action entry that runs on playable characters, everyone, or the dead adds `eotg_is_unclaimed_holder = no` (or `eotg_is_unclaimed_folk = no`). Batch 2 audits these (§9.2). **This is needed whatever V-U1 shows**, because `random_yearly_everyone_pulse` and `on_death` reach unplayable characters too.
- **M2. Vanilla yearly events:** a second key-level override, of `basic_is_valid_for_yearly_events_trigger` (`G/common/scripted_triggers/00_available_for_events_triggers.txt:802-816`), adding `NOT = { government_has_flag = eotg_government_is_unclaimed }`. Same file and same pitfalls entry. **Only if V-U1 says playable.**
- **M3. Lobby pick:** an additive `on_game_start_after_lobby` check that toasts any player who picked a placeholder: "No one rules here; choose a ruler" (`eotg_unclaimed_toast_unplayable`; not built until V-U1 says playable, §20). Bookmarks never list placeholders. **The toast does not stop the player from playing that character. This is a known limitation, owner question UQ1.**
- **The alternative if M1–M3 are not acceptable:** override vanilla `herder_government` itself, by key, to strip fertility, herd and `mechanic_type` while keeping the engine's unplayable key. That breaks the MPO no-DLC conversion (placeholders become tribal without MPO), anything MPO expects of herders, and the default herder government. **Not recommended**, listed only so the owner sees the whole choice (UQ1).

### 4.6 Vanilla precedent for creating a placeholder
The creation pattern is `G/common/scripted_effects/09_dlc_mpo_scripted_effects.txt:6650-6710`, which makes a herder for each county:
1. `create_character` with `template`, `dynasty = none`, `location = <county>.title_province`, and `culture`, `faith` and `rite` all `= <county>.<x>`.
2. `create_title_and_vassal_change { type = granted  add_claim_on_loss = no }`.
3. `change_title_holder`, then `resolve_title_and_vassal_change`.
4. `change_government`.
5. If `is_independent_ruler = no`: `type = independency` and `becomes_independent`.

**One deviation:** use `change_title_holder`, not `_include_vassals`. A released county's other baronies may be held by the old holder's vassals, and moving them would make the placeholder a liege, which its flag forbids. Those baronies stay where they are (§6.1).

---

## 5. Placeholder characters

### 5.1 Created at game start from one history seed (recommended)
| Option | How | For | Against |
|---|---|---|---|
| **(S) Seed + split (recommended)** | The cartographer authors **one** history character `eotg_unclaimed_seed` (any culture and faith key) and, for each county that starts unclaimed, `866.1.1 = { holder = eotg_unclaimed_seed  government = eotg_unclaimed_government }` (the `k_angara.txt:15-16` pattern). On `on_game_start`, `eotg_unclaimed_game_start_effect` runs `every_ruler` with our government flag. For every county a ruler holds, **unless** that ruler is folk and holds exactly one county, it calls `eotg_unclaimed_release_effect`. Then it vanishes the landless seed. | one history character per map; **culture, faith and name come from the county by scope (map-agnostic)**; "which counties are unclaimed" is plain history data; Phase 1's Unsettled marking comes for free | one runtime transfer per county at start (vanilla MPO does the same at runtime) |
| (H) One history character per county | vanilla's own herder pattern (264 `government = herder_government` lines) | no runtime transfer | hundreds of hand-made characters, each needing culture and faith keys that must match its county; a lore burden; not map-agnostic |

**(S) also accepts (H)'s output.** A history character that already has the trait and holds one county is left alone. The cartographer can hand-author a named community where the lore wants one.

- **`on_game_start` runs before the lobby** (vanilla: `on_game_start_after_lobby` is "like on_game_start, except it is called once the host … exits the lobby", `game_start.txt:2509`). So the split is done before anyone picks a character.
- **One placeholder per county, never shared.** A shared holder makes a single realm across scattered counties: one map label stretched over the gaps, summed levies and realm size in AI evaluation, one death moving every county at once, and domain-limit penalties. One per county avoids all of that, at the cost of N characters (vanilla carries 264 herders).

### 5.2 Template `eotg_unclaimed_holder_template` (shape: `G/common/scripted_character_templates/09_mpo_character_templates.txt:2`, `herder_character`)
- `age = { 30 55 }`, `gender_female_chance = 50`, `dynasty = none`, `random_traits = no`, `trait = eotg_unclaimed_folk`.
- `culture = this.culture`, `faith = this.faith`, `rite = this.rite`. The creation effect also passes them explicitly from the county (§4.6), as MPO does.
- **No culture, faith or name keys.** The **name** is the culture's ordinary random name. A fixed name (for example "the Scattered") is owner question UQ9.

### 5.3 Death and replacement
- **Primary path:** an additive `on_death` handler. Root is "just about to die" (`G/common/on_action/death.txt:1`). If `eotg_is_unclaimed_holder = yes`, `eotg_unclaimed_on_holder_death_effect` runs `eotg_unclaimed_create_holder_effect` on each county the dying placeholder holds, while it still holds them. V-U8 checks that a transfer inside `on_death` works.
- **Fallback (if V-U8 fails):** the engine's own succession. The trait blocks children and dynasty, so the engine generates a successor, and the government's `generated_character_template` makes it folk. `eotg_unclaimed_on_title_gain` then *adopts* a folk receiver who doesn't have our government (`change_government`). A **non-folk** receiver of a folk-held unclaimed county gets the claim bookkeeping (§8.5) and **no** auto-conversion: script never turns a real character into a placeholder.
- **Yearly sweep** (`yearly_global_pulse`, which runs every 1 January with no root, `yearly_on_actions.txt:1-3`), iterating `eotg_unclaimed_counties`:
  - (a) a county in the list whose holder is not an unclaimed holder → run the claim bookkeeping;
  - (b) a county in the list without the variable → remove it from the list;
  - (c) every folk character who is alive and holds no land → vanish.
  - This is a safety net. The direct paths should leave it nothing to do, and the debug readout reports what it found.

### 5.4 Trait `eotg_unclaimed_folk` (shape: `G/common/traits/00_traits.txt:6896-6899`, the blocker lines)
- `flag = can_not_marry`, `can_have_children = no`, `inheritance_blocker = all`, `claim_inheritance_blocker = all`;
- `shown_in_ruler_designer = no`, `shown_in_encyclopedia = no`;
- `icon` = an existing vanilla trait icon path until art arrives (§14).
- **Why:** a placeholder must never marry into a real dynasty, have heirs, or inherit real titles. `ai.arrange_marriage = no` only stops the placeholder itself from proposing (R§2).

### 5.5 Event and pulse safety
- **The shared exclusion trigger is `eotg_is_unclaimed_holder`.** Mod code that must also skip a placeholder that has lost its land uses `eotg_is_unclaimed_folk`.
- **Vanilla yearly events** go through `basic_is_valid_for_yearly_events_trigger`, which requires `is_playable_character = yes`. If V-U1 finds placeholders unplayable, that already excludes them; otherwise M2 applies.
- **Mod entry points to guard** (Batch 2, the scripter confirms the exact list): in `common/on_action/eotg_augmentation_on_actions.txt`, `yearly_playable_pulse` (:81), `on_death` (:95), `random_yearly_everyone_pulse` (:107), `on_game_start_after_lobby` (:150) and their `eotg_on_*` children; in `common/on_action/eotg_frontier_on_actions.txt`, `yearly_playable_pulse` (:10). Add the guard in the custom on_action's `trigger`, never as a top-level `trigger` on a vanilla hook (invariant 4).
- **Hooks this system adds:** `on_title_gain` and `on_death` fire for every character in the game. Each handler's **first** check is the cheap one: `scope:title = { has_variable = eotg_unclaimed_county }`, or `eotg_is_unclaimed_holder = yes`.

---

## 6. Release on abandonment, and owned Unsettled counties

### 6.1 An abandoned Frontier returns to Unclaimed
- **This attaches to Phase 1's hook, not to Phase 1's code.** `eotg_frontier_on_abandoned` already fires from `eotg_frontier_abandon_effect`, with root the holder and `scope:eotg_frontier_county` set (`frontier_v1.md` §7). `eotg_unclaimed_on_frontier_abandoned` listens to it.
- **Effect:** if the county has `eotg_unclaimed_claimed` **and is not the holder's capital county**, run `eotg_unclaimed_release_effect`. The county keeps its Abandoned state and traces (attempts, `abandoned_works`, the salvage record, revealed traits), so it is resettlable after the next claim (design §3.4). Then toast the former holder (`eotg_unclaimed_toast_released`).
- **The capital exception (recommended, UQ5):** releasing a capital would leave a one-county ruler landless. A capital Region stays with its holder, Abandoned, as in Phase 1.
- **Baronies:** only the county title and its capital barony move (V-U5). Any other barony in the county that someone holds stays with them.
- **Failed and voluntary abandonment** behave the same (UQ5).
- **Dependency:** V12 in Phase 1 (scopes reach custom on_actions). If it fails, Phase 1's fallback (empty scripted effects that get overridden) applies, and this listener becomes a one-line call at the end of `eotg_frontier_abandon_effect` (a Phase 1 edit, recorded in §3.6).

### 6.2 Settled clears the history
`eotg_unclaimed_on_frontier_settled` removes `eotg_unclaimed_claimed`. A settled county is ordinary land and never goes back to unclaimed.

### 6.3 Counties a ruler simply holds that are marked Unsettled
**These are unchanged.** `eotg_frontier_mark_unsettled_effect` on a held county (debug, the Corsica test, the cartographer's D3 marking) does not release it. Without `eotg_unclaimed_claimed`, abandonment keeps the county with its holder, as in Phase 1. The only new thing they get is the optional attrition line on the Unsettled modifier (§7.3, UQ7).

### 6.4 A claimed county that is never established
It stays with its claimant, Unsettled, with no time limit. A lapse after N years is deferred (UD3, UQ11).

---

## 7. Map colour and attrition

### 7.1 Neutral colour
- **Realms map mode is engine-driven** (`G/gfx/map/map_modes/map_modes.txt:276-277`, `color_mode = realms`). R§4 infers that it colours by the top liege's primary title, so an independent one-county placeholder shows its **county title's colour**.
- **The cartographer** gives every county that starts unclaimed `color = { 88 92 100 }` in `common/landed_titles/`. This is a desaturated slate. **The final pick belongs to the human, in game** (UQ8).
- **Script:** `eotg_unclaimed_set_neutral_colour_effect` is the only place the literal appears in script. It is called by every release. If the colour changes, it changes in that effect and in the cartographer's landed_titles block.
- **Neighbouring placeholders share the colour,** so unclaimed space reads as one grey expanse. The engine still draws realm borders between them (cosmetic, accepted).

### 7.2 Recolouring on claim
`eotg_unclaimed_set_claimed_colour_effect`:
- `set_color_from_title = <claimant>.primary_title`. Precedent: `01_puppet_interactions.txt:1938`, `00_major_decisions_scripted_effects_3.txt:233`.
- While the county is inside the claimant's realm, the map shows the realm's colour anyway. The recolour only matters if the county later becomes someone's independent primary title, and then it won't show slate grey.
- `set_title_color` (precedent: `00_major_decisions_scripted_effects.txt:254`) is only proven on an empire title. **V-U6: county scope, and persistence through save and reload.**

### 7.3 Attrition: armies that are not the owner's

| Where | Mechanism | Value | Who it hits |
|---|---|---|---|
| **Unclaimed counties (primary)** | `supply_limit_mult_for_others` on `eotg_unclaimed_government`. The .info: "Army owners of different government type have this multiplier applied to the supply limit" (`_governments.info:434-438`) | **−0.5**, vanilla's tribal and wanua value (`00_government_types.txt:199, 272`) | every army except a placeholder's, and placeholders have none. Since nobody can attack a placeholder, in practice this means every army **marching through** unclaimed space |
| Unclaimed counties (**fallback**, only if V-U3 shows the government knob doesn't apply) | a `supply_limit_mult = -0.5` line in `eotg_unclaimed_mod_unclaimed` | −0.5 | everyone in the county (symmetric) |
| **Owned Unsettled counties** (UQ7) | a `supply_limit_mult = -0.25` line in Phase 1's `eotg_frontier_mod_unsettled` | −0.25 | everyone, but a defender in their own realm gets `SUPPLY_OWN_REALM` +15% or `SUPPLY_OWN_SUB_REALM` +30% (`00_defines.txt:657-658`), **so it still falls harder on attackers** |

- **They add up:** an unclaimed county also carries the Unsettled modifier, so wild space is −0.75 and owned Unsettled space is −0.25. That gradient is the intent: the wilderness is harder than a claimed edge. If the owner wants a flat −0.5 in unclaimed space, set the government knob to −0.25.
- **The floor:** `MINIMUM_SUPPLY_LIMIT = 1000` (`00_defines.txt:659`). Supply starts to drain only above the limit, and attrition starts at supply 0 (`:662-680`). **Armies under 1,000 men never starve, and low-development unclaimed counties are often near the floor already.** The penalty bites only on large armies, which is the right shape for "a host can't live off empty space". V-U3 tests it with a 3,000+ army.
- **Not used:** `hostile_county_attrition`. It is a character modifier on the army owner (`G/common/modifier_definition_formats/00_definitions.txt:2191`), and nothing shows it working on a county.

---

## 8. Claiming

### 8.1 A character interaction, not a decision
- **Precedent:** `mpo_retrieve_land_from_herder_interaction` (`G/common/character_interactions/09_mpo_interactions.txt:7426`). That is vanilla's own "take land from someone who holds it without ruling it". It takes neighbour reach, a prestige cost, `auto_accept` for a landed actor, AI `ai_targets = neighboring_rulers`, and `ai_frequency_by_tier`.
- **Why an interaction:** the placeholder *is* the county's handle. The player clicks the grey county, then its holder, then "Stake a Claim". A decision can't target a county (Phase 1 E15). One placeholder holds one county, so there is no title picker: the target is `scope:recipient.capital_county`.
- **Deviations:** our cost, our cooldown and our AI throttle. We pay in `on_accept` and check affordability in `is_valid_showing_failures_only`, which follows both vanilla's interaction and the mod's interaction rule (`eotg_augmentation_interactions.txt` header).

### 8.2 Who can claim
- **`is_shown`:** `scope:recipient` passes `eotg_is_unclaimed_holder`, and its capital county passes `eotg_unclaimed_is_unclaimed`.
- **The actor** (`eotg_unclaimed_can_claim`): `is_landed = yes`, `highest_held_title_tier >= tier_county`, adult, not imprisoned, and not a placeholder. Vassals may claim: the county joins their domain and so their liege's realm.
- **Reach** (`eotg_unclaimed_in_reach`, county scope, `$ACTOR$`), either of:
  - (a) **adjacency:** `$ACTOR$ = { any_sub_realm_county = { any_neighboring_county = { this = <target> } } }`. This is the MPO precedent's own test (`09_mpo_interactions.txt`, the `is_valid_showing_failures_only` of the interaction at :7426);
  - (b) **distance:** `"$ACTOR$.capital_province.squared_distance(<target>.title_province)" <= eotg_unclaimed_reach_value`. The syntax precedent is `00_fp3_interactions.txt:918`. This reaches across void or sea lanes on a space map.
- **Not in Batch 2:** landless adventurers (vanilla lets them claim from their domicile), and a fleet or travel requirement. Both are UD1 and UQ4.
- **Unknown Regions (Phase 3a): claimable** (recommended, UQ6).
  - Phase 3a's **Send an Expedition** is a holder's decision, so if Unknown blocked claiming, nobody could ever explore an unclaimed Unknown Region.
  - The claimant explores after claiming, and Phase 3a's own gate still stops Establish until the Region is explored.
  - This needs no change to Phase 3a and no read of its variable, so it works whether or not 3a is merged.

### 8.3 Cost, cooldown, transfer
- **Cost:** `eotg_unclaimed_claim_gold_value` (minor gold) plus `eotg_unclaimed_claim_prestige_value` (minor prestige), paid in `on_accept`. Together with Phase 1's Establish (medium gold), a Frontier on new ground costs about minor + medium gold and minor prestige.
- **Cooldown:** `cooldown = { years = 5 }`, **per actor** (`_character_interactions.info:199`).
  - This is the interaction's own gate, not an event cooldown.
  - It deviates from the cybernetics rule of `cooldown_against_recipient` only, because the recipient changes every time: each claim vanishes its placeholder.
- **Transfer:** `type = granted`, `add_claim_on_loss = no`. This is the MPO creation pattern (R§5). It gives no "conquered" penalties and leaves the vanished placeholder no claim.
  - `usurped` or `conquest` would suggest a seizure. Under LAW AT 866, a claim is asserted under the claimant's own law, not won from anyone.
- **The placeholder vanishes:** `death = { death_reason = death_vanished }` (precedent: `G/common/factions/00_nomadic_faction.txt:383`). It runs only **after** the county has moved, so the `on_death` replacement finds nothing to replace.
- **Frontier tie-in:**
  - Claiming does **not** start a Frontier and does **not** re-mark the county: it is already Unsettled or Abandoned from its release.
  - **Establish needs the claim by construction,** because Phase 1's decision only offers counties the taker holds. The guard in §3.6 is defence in depth.
  - The `on_accept` tooltip says "You may now Establish a Frontier here", and it warns about the release rule (`eotg_unclaimed_claim_effect_tt`, `_returns_tt`).

### 8.4 AI pacing (plausible, not a land rush)
| Field | Value |
|---|---|
| `ai_targets` | `ai_recipients = neighboring_rulers`, `max = 5` (vanilla precedent). V-U14 checks that placeholders count as neighbouring rulers. The distance branch (b) is for players only. |
| `ai_frequency_by_tier` | barony 0, county 36, duchy 24, kingdom 24, empire 24, hegemony 24 (months) |
| `is_available` for AI (`eotg_unclaimed_ai_may_claim`) | not at war; gold ≥ 3 × the claim cost; `domain_size < domain_limit`; holds fewer than `eotg_unclaimed_ai_hold_cap_value` (2) counties with `eotg_unclaimed_claimed`; **no global `eotg_unclaimed_ai_gap`** |
| `ai_will_do` | base 10; +10 ambitious; +10 stewardship ≥ 12; −10 content; −10 lazy; ×0 at war |
| `on_accept` (AI actor) | sets the global `eotg_unclaimed_ai_gap` for `eotg_unclaimed_ai_gap_days_value` (180) days |

- **Effect on the map:** at most about 2 AI claims a year worldwide, whatever the map size. A large unclaimed region fills over generations, not in a decade.
- **Players are not throttled** beyond the 5-year cooldown and the cost.
- **Phase 1's AI cap** (8 active Frontiers, 1 per ruler) then decides how many of those claims become projects.

### 8.5 One bookkeeping path for every transfer: the `on_title_gain` catch-all
- **Hook:** `on_title_gain` (`G/common/on_action/title_on_actions.txt:229-233`: root is the new holder, with `scope:title` and `scope:previous_holder`).
- **Handler:** `eotg_unclaimed_on_title_gain`. If `scope:title` has `eotg_unclaimed_county` and root is **not** folk, it runs `eotg_unclaimed_on_claimed_effect = { CLAIMANT = root  OLD = scope:previous_holder }`.
- **Why one path:** the interaction, a vanilla event that moves titles, a console `change_title_holder` or any future system all end in the same state, and the interaction itself does no bookkeeping. **V-U9:** `on_title_gain` fires for scripted transfers. The yearly sweep catches anything this misses.

---

## 9. Wiring

### 9.1 Hooks
| Hook | Kind | Root | Handler's first check | Fires |
|---|---|---|---|---|
| `on_game_start` | vanilla, `on_actions = { }` | none | — | `eotg_unclaimed_game_start_effect` |
| `on_title_gain` | vanilla, additive | new holder | `scope:title = { has_variable = eotg_unclaimed_county }` | §8.5 |
| `on_death` | vanilla, additive | dying character | `eotg_is_unclaimed_holder = yes` | §5.3 |
| `yearly_global_pulse` | vanilla, additive | none | — | `eotg_unclaimed_sweep_effect` |
| `eotg_frontier_on_abandoned` | Frontier hook, additive | the Region's holder | `scope:eotg_frontier_county = { has_variable = eotg_unclaimed_claimed }` | §6.1 |
| `eotg_frontier_on_settled` | Frontier hook, additive | the holder | same | §6.2 |
| `on_game_start_after_lobby` | vanilla, additive, **only if V-U1 says playable** | none | `every_player` with `eotg_is_unclaimed_holder` | M3 toast |

- **No cooldown is duplicated in any trigger.** The interaction's `cooldown`, the AI gap variable and the sweep's yearly cadence are each the single authority for their own pacing.
- **Tiers:** placeholders are counts, and role triggers gate every tier (the interaction's `ai_frequency_by_tier` covers county to hegemony).

### 9.2 Guards added to existing mod pulses (Batch 2)
§5.5's list: `eotg_is_unclaimed_folk = no` in the trigger of each custom child on_action that a vanilla pulse reaches, in `eotg_augmentation_on_actions.txt` and `eotg_frontier_on_actions.txt`. The scripter records the exact touch points in the handoff.

### 9.3 New hooks for later systems
- `eotg_unclaimed_on_claimed`: root = the claimant; `scope:eotg_unclaimed_target`, `scope:eotg_unclaimed_old_holder`.
- `eotg_unclaimed_on_released`: root = the new placeholder; `scope:eotg_unclaimed_target`, plus `scope:eotg_unclaimed_old_holder` when the county had a real holder.
- Both are defined empty and fired through `trigger_event = { on_action = … }`, as Phase 1's hooks are. Later candidates: corporations claiming for a backer, exploration revealing claimable space.

---

## 10. Gate 1: what the cartographer must do (map-specific; nothing here is mod script)

1. **Choose which counties start unclaimed,** from the region briefs. Where a brief doesn't say, the question goes to the vault through `eotg-intake` (`intake/.../QUESTIONS.md`), never a guess.
2. **The seed character:** `history/characters/`, key `eotg_unclaimed_seed`, with any culture, faith and birth date. It is vanished at start.
3. **Title history:** for each unclaimed county, `866.1.1 = { holder = eotg_unclaimed_seed  government = eotg_unclaimed_government }`, or the bookmark's own date if it differs.
4. **landed_titles:** `color = { 88 92 100 }` on each unclaimed county, or the colour the human picks (UQ8).
5. **Holdings:** the capital barony gets a holding (castle by default); the other baronies get `holding = none`. Low development (Phase 1 D3).
6. **No Unsettled marking is needed** for these counties: the split calls Phase 1's marking itself.
   - Phase 3a's Unknown marking, if it merges, stays the cartographer's call through `eotg_frontier_mark_unknown_effect`.
   - An optional second seed for "unclaimed and Unknown" is deferral UD5.
7. **Impassable or void provinces** that aren't counties: unchanged, scenery only.
8. **The bookmark** lists no placeholder.

---

## 11. Test setups (both are sub-mods in `docs/`, never shipped)

### 11.1 The vanilla sub-mod (Corsica and Sardinia), `docs/test_submods/frontier_vanilla/` (scripter; vanilla title keys are allowed there)
- **Sardinia** (`c_cagliari`, `c_arborea`, `c_gallura`, `c_logudoro`, `c_tortoli`): `eotg_unclaimed_release_effect = yes` instead of marking Unsettled. That gives five Unclaimed Regions, neutral grey, held by placeholders. Their 867 holders become unlanded; note this in the README.
- **Corsica** (`c_ajaccio`, `c_bastia`, `c_vecchio`): unchanged, owned Unsettled. That tests §6.3, and gives a neighbour across the strait who can claim Sardinia (reach (a) or (b)).
- **This needs no landed_titles change.** The release sets the colour at runtime, which also tests V-U6.

### 11.2 The test map, `docs/test_map/` (cartographer)
- Add `eotg_unclaimed_seed` to `history/characters/eotg_test_map_characters.txt`.
- In `history/titles/eotg_test_map_titles.txt`, reassign **2–3 neighbouring counties** to it, with `government = eotg_unclaimed_government`. Choose counties that are not used in `docs/qa/cybernetics_test_plan.md` §1c or the Frontier test plans, and that border at least two realms (so there are competing claimants).
- Give them the neutral colour in `common/landed_titles/00_landed_titles.txt`.
- This exercises the real Gate 1 path (S), which the vanilla sub-mod does not.

### 11.3 Anywhere
- The debug decision `eotg_decision_unclaimed_debug_release` releases a non-capital county.
- From the console: `effect title:<c_key> = { eotg_unclaimed_release_effect = yes }`. Keys are fine at the console.

---

## 12. Verification list for the local session (in game, with `-debug_mode`; vanilla-scout for the static items)
1. **V-U1 Playability:** `eotg_decision_unclaimed_debug_readout` toasts whether a placeholder passes `is_playable_character`. Also check the lobby: can a placeholder be picked in free pick? **This decides M2 and M3 (§4.5).**
2. **V-U2 War immunity:**
   - `database_conflicts.log` shows the `herders_and_tributary_constraints` override;
   - give yourself a claim on an unclaimed county (`add_claim` at the console): no CB is offered;
   - no placeholder ever declares war (20-year observer run).
3. **V-U3 Attrition:** park a 3,000+ army in an unclaimed county and compare its supply limit with the same county after claiming it. The difference should be the −0.5 (the government knob) plus −0.25 (Unsettled, if UQ7 is approved). If no difference shows, switch to the fallback line (§7.3).
4. **V-U4 History seed:** on the test map, `government =` in title history sets the seed's government, and the split leaves one placeholder per county with the county's culture and faith. The seed is gone.
5. **V-U5 Capital barony:** `change_title_holder` on the county carries its capital barony. If not, move it explicitly.
6. **V-U6 Colour:** `set_title_color` and `set_color_from_title` on a **county** change the realms map. Both survive save and reload, and so does the history colour.
7. **V-U7 Vanish:** `death_vanished` removes the old placeholder without death notifications to players.
8. **V-U8 Death:** kill a placeholder (console). Its county passes to a new placeholder through `on_death`. If not, check the fallback in §5.3.
9. **V-U9 Catch-all:** `on_title_gain` fires for a console `change_title_holder` and the bookkeeping runs.
10. **V-U10 Government gate:** `can_get_government` on the trait doesn't block the scripted `change_government`, and the unset `fallback` doesn't make this a fallback government (no random count ever ends up with it).
11. **V-U11 Trait blockers:** the marriage interactions refuse a placeholder, and holding the county is unaffected by `inheritance_blocker`.
12. **V-U12 Realm name:** whether `eotg_unclaimed_government_realm` (as vanilla `herder_government_realm: "Pastureland"`) appears anywhere on the map or in the realm name.
13. **V-U13 Persistence:** after save and reload, `eotg_unclaimed_county`, `eotg_unclaimed_claimed` and the list survive (as Phase 1 V1).
14. **V-U14 AI targets:** AI rulers bordering placeholders do claim, within the throttle, in a 20-year observer run.
15. **V-U15 Abandon:** abandon a claimed Frontier. The county goes back to grey, Unclaimed and Abandoned with traces. A Corsica (owned) abandonment stays with its holder.

---

## 13. Build batches

**Batch 1: core and probes (eotg-scripter; the cartographer does §11.2 in parallel)**
- The government, trait, template, triggers, effects (everything except `_claim_effect`), the county modifier, the four vanilla hooks and the trigger override.
- Both debug decisions and the vanilla sub-mod change (§11.1).
- Loc for all of these.
- **Exit:** V-U1 to V-U13 run in game. V-U1's answer decides whether Batch 2 includes M2 and M3.

**Batch 2: claiming and Frontier tie-ins (eotg-scripter)**
- The interaction, the AI throttle, the Frontier hook listeners, and the §3.6 Phase 1 touches.
- The §9.2 pulse guards; M2 and M3 if V-U1 needs them.
- **Exit:** V-U14 and V-U15, and the definition of done.

---

## 14. Loc surface (`localization/english/eotg_unclaimed_l_english.yml`; UTF-8 with exactly one BOM, Canadian English, bare `[x.GetName]`)
- **Government:** `eotg_unclaimed_government` ("Unclaimed"), `_adjective`, `_realm` ("Unclaimed Region"), `_desc`, `_with_icon`. The icon is vanilla `@government_type_herder!` until art arrives. Also the flag line `eotg_government_is_unclaimed` (it shows in the government tooltip, as vanilla's flag lines do, `government_l_english.yml:272-285`).
- **Trait:** `trait_eotg_unclaimed_folk`, `trait_eotg_unclaimed_folk_desc`.
- **Modifier:** `eotg_unclaimed_mod_unclaimed`, `eotg_unclaimed_mod_unclaimed_desc`.
- **Interaction:**
  - `eotg_unclaimed_claim_interaction`, `_desc`;
  - tooltips `eotg_unclaimed_claim_reach_tt`, `_gold_tt`, `_prestige_tt`, `_effect_tt`, `_returns_tt`;
  - **any requirement line shows words, never raw variables.**
- **Toasts:** `eotg_unclaimed_toast_claimed`, `eotg_unclaimed_toast_released`, and conditionally `eotg_unclaimed_toast_unplayable` (not built until V-U1 says playable, §20).
- **Debug decisions:** 2 × (`<key>`, `_desc`, `_confirm`), plus `eotg_unclaimed_debug_playable_tt` / `_unplayable_tt` and `eotg_unclaimed_debug_counts_tt`.
- **Phase 1:** `eotg_unclaimed_abandon_returns_tt`.
- **No `replace/` overrides needed.**
  - The placeholder still shows the vanilla rank "Count". Renaming the rank per government is deferred (UD7).
  - The overridden trigger's tooltip key `is_a_herder_defender_tt` stays vanilla text ("herders can't fight"). The localizer can add our own `custom_tooltip` key inside the override (`eotg_unclaimed_defender_tt`), since we own that copy. Not built: the override ships inert until the local session pastes vanilla's body (§20).
- **Glossary:** county = **Region**. Use "unclaimed" and "claim". **Never** "charter", "registry", "wasteland" (it's lived in), "peasants", "human" (multi-species), or any named faction.

---

## 15. Lore constraints (route to eotg-lore-keeper: UL1–UL3)
- **LAW AT 866** (`docs/lore/REVIEW_866.md`, draft errata): there is no authority above the polity. **A claim is asserted under the claimant's own law and recognized by no one else.** No text may imply a registry, a grant from above, or a recognized title to empty space. That is why the transfer type is `granted` and the wording is "stake a claim".
- **Who lives there:** the placeholder is "the scattered people" (owner). Frontier §R allows Exodus arrivals and their descendants (ongoing since 131 AG), prospectors and isolated communities. Text stays time-neutral, as in all of Frontier (`frontier_v1.md` §V).
- **Culture and faith** come from the county by scope. **UL1:** is it canon-safe that unclaimed space carries a culture and faith (the province's) at 866, or should the briefs mark some unclaimed space as mixed?
- **UL2:** the player-facing term: "Unclaimed Region" or another word in the setting's register (vault question if no brief settles it).
- **UL3:** the interaction name ("Stake a Claim").

---

## 16. Definition of done
1. Tiger and PX are clean on every `eotg_unclaimed_*` file, apart from the known-benign list. The government block has been checked by hand against `_governments.info` and `herder_government` (Tiger can't).
2. `database_conflicts.log` shows exactly **one** new override (`herders_and_tributary_constraints`), or two if M2 ships, and the pitfalls entry (§4.4) is in `docs/pitfalls.md`.
3. **Map-agnostic:** `grep -nE 'title:|province:|culture:|faith:|character:'` over the system's `common/` files returns nothing. Keys appear only in the two test sub-mods and in the cartographer's history.
4. **On the test map, at start:** every seeded county has its own placeholder with the county's culture and faith; the seed is gone; the counties are grey, Unsettled and carry `eotg_unclaimed_mod_unclaimed`; and the list size equals the number of seeded counties.
5. **Claiming:** the interaction shows only on placeholders that are in reach. It charges gold and prestige, and the county moves. The colour changes, the old placeholder is gone, the variable is cleared, and Establish becomes available.
6. **Immunity:** with a claim on an unclaimed county, no CB is offered against it, and no placeholder declares war in a 20-year run.
7. **Attrition:** V-U3 shows the knob, or the fallback is in place.
8. **Death:** a killed placeholder's county is held by a new placeholder by the next sweep at the latest.
9. **Abandonment:** V-U15 passes for both a claimed and an owned county.
10. **AI, 20-year observer run:** AI claims stay at or under about 2 a year; no AI holds more than 2 claimed, unsettled counties; the sweep reports **0** leftover folk characters.
11. **Persistence:** markers, list and colours survive save and reload.
12. **`signature`:** every effect in §3.3 sets, removes or reads `eotg_unclaimed_county` (grep).

---

## 17. Deferred
- **UD1:** claiming by landless adventurers, and a fleet or travel requirement for distant claims. Needs a fleet or travel design and the adventurer question.
- **UD2:** surveying or exploring an unclaimed Region **before** claiming it. Phase 2's Survey and Phase 3a's Expedition are holder-only; widening them is a later Frontier phase.
- **UD3:** an unestablished claim lapsing back to unclaimed after N years (UQ11).
- **UD4:** a custom "camp" holding for unclaimed capitals (Phase 1 option 2.3b; needs gfx).
- **UD5:** a second seed for "unclaimed and Unknown" at start (needs Phase 3a merged).
- **UD6:** raiding unclaimed counties (needs Gate 2 raider governments).
- **UD7:** a rank name for placeholders instead of "Count" (a loc or `replace/` design).
- **UD8:** neighbour notifications when someone claims next to you; an opinion modifier for contested claims.

## 18. Art wanted (none built)
- A **government icon** `government_type_eotg_unclaimed` (text icon and government UI); until then the herder icon.
- A **trait icon** for `eotg_unclaimed_folk` (it is hidden from the designer, but shows on the character).
- An **interaction icon** for Stake a Claim; until then a vanilla interaction icon chosen by the scripter.
- A **county-modifier icon** for Unclaimed Region; until then a vanilla `county_modifier_*` icon.
- Optional: a generic **coat of arms** for unclaimed counties.

---

## 19. Owner questions
- **UQ1 (top): playability.** If V-U1 shows placeholders are playable, accept mitigations M1–M3 (a second vanilla trigger override, plus a lobby toast that can't actually stop a player picking one)? Or repurpose vanilla `herder_government` by key override (not recommended, §4.5)?
- **UQ2: war immunity.** Own flag plus one key-level trigger override (recommended), or reuse `government_is_herder` and live with vanilla's "Retrieve Land" interaction as an unthrottled second claim path for the AI?
- **UQ3: authoring.** One history seed split at game start (recommended), or hand-authored history characters per county? (S) accepts both.
- **UQ4: reach.** Adjacency **or** within `squared_distance_medium` of the claimant's capital? Should landless adventurers ever claim?
- **UQ5: release rules.** Should a capital Region stay with its holder when abandoned (recommended)? Should failed and voluntary abandonment both release?
- **UQ6: Unknown Regions claimable** before exploring (recommended), at the same cost?
- **UQ7: attrition.** −0.5 on unclaimed space (the government knob); should owned Unsettled counties also get −0.25 (symmetric, but softened for defenders by the own-realm supply bonus)?
- **UQ8: the neutral colour.** `{ 88 92 100 }`, or your pick in game.
- **UQ9: placeholder names.** Random names from the county's culture (recommended), or one fixed name for every placeholder?
- **UQ10: AI pacing.** About 2 AI claims a year worldwide, and at most 2 claimed-but-unsettled counties per AI ruler?
- **UQ11:** should a claim that is never established lapse back after N years?

---

## 20. Build notes (cloud session, 2026-10-06; static, unvalidated)
Batch 1 and Batch 2 are built on `claude/frontier-unclaimed-cloud` (from Frontier Phase 3a round 2, `dc02666`). Handoff: `docs/handoffs/cloud_2026-10-06_frontier-unclaimed.md`.

**Deviations from this spec, and why:**
1. **The `herders_and_tributary_constraints` override ships INERT** (`common/scripted_triggers/eotg_vanilla_overrides_triggers.txt`, commented out). The cloud session has no game files, and a key-level override must be a verbatim copy; a reconstruction would silently change 17 CB groups. The file carries the frame, the two `# EOTG` lines and the paste steps. **Until the local session pastes vanilla's body, there is no war immunity (V-U2 fails by design).** `eotg_unclaimed_defender_tt` waits with it (not built).
2. **M2 and M3 are not built** (`basic_is_valid_for_yearly_events_trigger` override, `eotg_unclaimed_toast_unplayable`): §4.5 makes both conditional on V-U1. The probe (`eotg_decision_unclaimed_debug_readout`) answers it. **M1 is built** (the pulse guards, §9.2).
3. **Expedition targeting is widened now** (owner instruction for this build; this spec's UD2 had left it for a later phase). `eotg_frontier_can_target_expedition` and `eotg_frontier_pick_expedition_target_effect` (`frontier_v3.md` §4.1) also allow an explorable Unclaimed Region within the actor's reach (`eotg_unclaimed_in_reach`), after the actor's own Regions. Survey stays holder-only.
4. **The capital barony is moved explicitly** with the county, when the old county holder held it (creation and claim). If V-U5 shows the engine already does this, the extra move is a no-op.
5. **A history placeholder holding exactly one county is adopted**, not replaced (§5.1 "(S) also accepts (H)'s output"). A seed being split carries the character flag `eotg_unclaimed_splitting`, so it is never adopted; every county it held gets its own placeholder.
6. **The seed must carry the trait `eotg_unclaimed_folk`** in its history (added to §10 step 2's needs): `can_get_government` reads it, and without it history's `government =` may fall back.
7. **New identifiers beyond §3:**
   - the trigger `eotg_unclaimed_would_release` (county; shared by the release listener and the Phase 1 abandon tooltips);
   - the effect `eotg_unclaimed_on_abandoned_effect` (the listener's body);
   - the script value `eotg_unclaimed_ai_gold_floor_value` (3 × the claim gold);
   - the loc keys `eotg_unclaimed_claim_returns_tt` (§14's `_returns_tt`), `eotg_unclaimed_debug_none_tt` and `eotg_decision_unclaimed_debug_release_valid_tt`;
   - the character flag `eotg_unclaimed_splitting`;
   - the global variable `eotg_unclaimed_sweep_fixed` (what the last sweep fixed; the readout shows it);
   - the saved scopes `eotg_unclaimed_previous`, `_former`, `_stray`, `_stray_holder`, `_probe` and `_debug_reader`.
8. **Names:** the trait shows as "Unsworn" (one person; the people are "the Unsworn"). The interaction is "Raise Your Colours" (§D), and its key stays `eotg_unclaimed_claim_interaction`.
9. **Interaction category:** `interaction_category_diplomacy` (UNVERIFIED-VANILLA). The icon is the mod's existing placeholder `icon_personal`.
10. **Placeholders and Phase 3a hooks:** an expedition to an Unclaimed Region fires `eotg_frontier_on_explored` with root = the placeholder, because Frontier hooks fire on the county holder. Listeners must not assume a real ruler there.
11. **Test map:** c_aphion_seam and c_helios_shoal start unclaimed. They are adjacent, between them they border both big realms, and neither is anyone's only county. c_aphion_seam was listed among the development-10 counties for cybernetics §1c, but no ruler's gate read it.
12. **eotg_lint:** a `governments` loc naming convention (`{key}`, `_adjective`, `_realm`, `_desc`, `_with_icon`), marked unverified, so L014 sees the government's loc.

---

### HANDOFF
- status: done
- next: eotg-scripter (Batch 1, §13), with eotg-cartographer for §11.2 in parallel; eotg-lore-keeper for UL1–UL3
- ask: build Batch 1 of `docs/specs/frontier_unclaimed_regions.md` (government, trait, template, triggers, effects except claim, modifier, the four vanilla hooks, the `herders_and_tributary_constraints` key override, two debug decisions, the vanilla sub-mod change), then hand V-U1 to V-U13 to the human through QA. The cartographer adds the seed and 2–3 unclaimed counties to the test map.
- files: docs/specs/frontier_unclaimed_regions.md
- needs-loc: §14 (about 30 keys) once Batch 1 lands
- needs-lore: UL1 culture and faith in unclaimed space at 866; UL2 the player-facing term; UL3 the interaction name
- needs-human: UQ1–UQ11 (UQ1 after V-U1); the in-game checks V-U1–V-U15; the pitfalls entry in §4.4 goes in when the override ships (orchestrator)
