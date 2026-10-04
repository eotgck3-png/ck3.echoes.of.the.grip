# Spec: Cybernetics v2 — procedures, providers and repairs (G1), Seamless life (G2), former augmentation (G3)

**Author:** eotg-architect, 2026-10-04
**Authorised by:** the human, 2026-10-04 (relayed by the coordinator): Part 1 (procedures, providers, repairs), G2 (Seamless ongoing life) and G3 (a marker for former augmentation, with aftermath), all from [`docs/qa/cybernetics_content_gaps_v2.md`](../qa/cybernetics_content_gaps_v2.md).
**Index:** [cybernetics_v2.md](cybernetics_v2.md). Index §1 rules 1–12 and the §5 lore register apply to everything here.
**Also binding:** [cybernetics_v2_balance.md](cybernetics_v2_balance.md) (HQ1/HQ2 pacing), [cybernetics_v2_conformance_rulings.md](cybernetics_v2_conformance_rulings.md), [cybernetics_v2_new_beats.md](cybernetics_v2_new_beats.md) (patron.008 and the removal state).
**Checked against:** the working tree on `v2-space-map` after `82defbd`, including the Cybernetics session's uncommitted batch (tooltip guards, W1–W6, M7/M8), which is QA-passed for script. This spec builds on that batch and changes none of it. Line numbers are left out on purpose: existing events and options are referenced **by id and option letter** (index §1 rule 12).

**Size.**
- **8 new events:** 4 for Part 1, 1 for G3 and 3 for G2.
- 1 new namespace, 1 new event file, 3 new custom on_actions (one of them on a new vanilla hook), 1 new modifier.
- About 13 new scripted effects, triggers and script values; 3 new variables and 5 new flags.
- About 115 loc keys.
- The gaps doc estimated 12–15 events (Part 1 ~5, G3 3–4, G2 4–6). **This spec comes in below that. Nothing needs a further yes from the human for event count.**

---

## 0. Corrections to the gaps doc (found in the current script)

The rest of this spec relies on these. None of them changes the approved direction.

| Gaps doc says | Script says | Consequence here |
|---|---|---|
| The discovered modifier is `eotg_mod_aug_illegal_implants` | The key is **`eotg_mod_illegal_implants`** (`common/modifiers/eotg_augmentation_modifiers.txt`) | This spec uses the real key. |
| The upgrade to Enhanced has "none" from the procedure | tier1.022 already rolls clean 70 / complication 30 (+15 clean with physician access or the chain edge; +10 complication with strain). A complication means risk +10 and a 1-year infection. | That roll is **replaced** by the shared roll (§4.3). Its complication becomes the upgrade form of *rejection*, and its two descs are kept. |
| "Desperation and the craven back-alley variant feed the same `init.011` roll" | Only init.010 (a, c, d) and init.018.b fire init.011. init.004 (desperation) installs directly, with risk 10/15 and the illegal-implants modifier. | init.004 is mapped to the back-street provider (§4.5). Its existing illegal modifier switches off the *discovered* outcome. |
| "Outcome descs on … `tier2.014`" | tier2.014 *The Vendors Return* is the Bidding War's second stage. It is not an installation. | The Overclocked upgrade happens on the click in tier2.003, and its outcome is reported by the new proc.002 (§4.4). |
| Consult the Physician removes Fragments | `eotg_decision_consult_physician` has `is_shown = { has_trait = eotg_cybernetics … }`, so a character who has left the system cannot see it | It is widened (§4.8). |

---

## 1. Purpose & gate

**Part 1.**
- Every procedure (install, both upgrades, every removal, repairs) offers a provider: a clinic, the character's own physician, or the back streets.
- One shared roll sets the outcome odds.
- The severe tail (maiming, an eye, blindness, death on the table) exists only in the back streets, and it is rare.
- An augmented character who suffers a real injury can have it repaired.

**G3.** Leaving the system leaves a permanent marker and one aftermath beat.

**G2.** Seamless gets a small yearly pool, coupled to a new resource, because `eotg_fracture_risk` is removed at Total Integration.

**Gate 3 (Systems), built against the temporary map** (`docs/agent_workflow.md` §5 rule 2; the mod-exclusive-system exception in `CLAUDE.md`). **Not blocked.**
- Map-agnostic: no title, province, character, culture or faith keys.
- The syndicate stays unnamed.
- Faith reactions go only through `zealous` / `cynical` and piety.

---

## 2. Signature resource

| State | Resource | Notes |
|---|---|---|
| Augmented / Enhanced / Overclocked / Neurofractured | **`eotg_fracture_risk`** (hidden, 0–100), unchanged, plus **tier** (track XP 0/50/100, moved only by `eotg_aug_set_integration_effect`) | Procedures move risk (§4.2 table) and change tier. A repair always adds risk, scaled by tier. Every risk move is in `hidden_effect`. Nothing quantifies it (index §1 rule 3). |
| **Seamless** (`eotg_total_integration`) | **NEW `eotg_aug_residue`** (hidden character variable, integer 0–3) | **Why a new resource.** `eotg_add_fracture_risk` is a no-op at Seamless by design, and the voice is fixed at 5. Residue counts the *habits and reflexes the integration has not yet optimised away*. It is **not** a person: the voice-5 line ("There is no one left for it to speak to") stays true. **It only falls**, so it works as the state's clock. It is set to 3 by `eotg_aug_total_integration_effect`. **Read by:** the Flicker's eligibility; desc bands in every Seamless event; the size of the Ledger windfall; A Part Replaced's desc. **Moved by:** one option in each G2 choice event, and the Flicker itself. **Never shown** (the same hidden rule as risk). **Approved by the lore-keeper (2026-10-04, ruling (a))**, with its register constraint (§7). |
| **Former** (left the system) | **tier** (the way back in), plus the read-only marker **`eotg_aug_former`** | A former character has no risk, and nothing may recreate it (QA round 2 M3). The aftermath event couples by offering the way back in, which is a tier change: index §1 rule 4, "or changes tier". Its desc reads the marker. |

**Coupling (invariant 5 / index §1 rule 4) for each new event:**
- proc.001: tier change on every paid option.
- proc.002 and proc.004: chain stages of a procedure. They also move risk (upgrade complication, infection c, repair risk) or read residue.
- proc.003: every paid option moves risk.
- proc.020: options c and d lead into an install (tier), and the desc reads the marker.
- end.040–.042: each moves or reads residue.

---

## 3. Identifier table

All keys carry the `eotg_` prefix. No landed titles. Loc keys use the dot form (index §0, "Loc key form").

### 3.1 New

| Type | Key | Where | Owner | Part |
|---|---|---|---|---|
| namespace | `eotg_aug_proc` | `events/eotg_augmentation_procedures.txt` (**new file**) | scripter | 1, G3 |
| event | `eotg_aug_proc.001` *Who Takes It Out?* | procedures file | scripter | 1 |
| event | `eotg_aug_proc.002` *After the Procedure* | procedures file | scripter | 1 |
| event | `eotg_aug_proc.003` *Spare Parts* | procedures file | scripter | 1 |
| event | `eotg_aug_proc.004` *A Part Replaced* (lore N1; working title was *Self-Mending*) | procedures file | scripter | 1 / G2 |
| event | `eotg_aug_proc.020` *Phantom Static* | procedures file | scripter | G3 |
| event | `eotg_aug_end.040` *The Ledger Balances* | `events/eotg_augmentation_endgame.txt` | scripter | G2 |
| event | `eotg_aug_end.041` *A Resignation* | endgame file | scripter | G2 |
| event | `eotg_aug_end.042` *A Flicker* | endgame file | scripter | G2 |
| scripted effect | `eotg_aug_procedure_roll_effect` (params `PATIENT`, `PROVIDER`, `PROCEDURE`, `SURGEON`) | `common/scripted_effects/eotg_augmentation_effects.txt` | scripter | 1 |
| scripted effect | `eotg_aug_procedure_roll_booked_effect` (params `PATIENT`, `PROCEDURE`, `SURGEON`; provider read from `scope:eotg_proc_provider`) | effects | scripter | 1 |
| scripted effect | `eotg_aug_procedure_apply_effect` (no params; runs in the patient's scope) | effects | scripter | 1 |
| scripted effect | `eotg_aug_procedure_effect` (params as the roll; roll, then report or apply) | effects | scripter | 1 |
| scripted effect | `eotg_aug_save_surgeon_effect` (no params; saves `scope:eotg_proc_surgeon`) | effects | scripter | 1 |
| scripted effect | `eotg_aug_pay_procedure_effect` (params `BASE`, `MULT`) | effects | scripter | 1 |
| scripted effect | `eotg_aug_removal_perform_effect` (no params; reads `var:eotg_aug_removal_kind`) | effects | scripter | 1 |
| scripted effect | `eotg_aug_repair_injury_effect` (no params; reads `var:eotg_aug_repair_injury`) | effects | scripter | 1 |
| scripted effect | `eotg_aug_mark_former_effect` | effects | scripter | G3 |
| scripted trigger | `eotg_aug_can_afford_procedure` (params `BASE`, `MULT`) | `common/scripted_triggers/eotg_augmentation_triggers.txt` | scripter | 1 |
| scripted trigger | `eotg_aug_has_repair_injury` (the trait named by `var:eotg_aug_repair_injury` is still held) | triggers | scripter | 1 |
| script value | `eotg_aug_proc_bad_factor` | `common/script_values/eotg_augmentation_values.txt` | scripter | 1 |
| script values | `eotg_aug_price_mult_physician` (0.75), `eotg_aug_price_mult_self` (0.25), `eotg_aug_price_mult_backstreet_upgrade` (0.5), `eotg_aug_price_mult_backstreet_removal` (0.4), `eotg_aug_price_mult_backstreet_repair` (0.5) | values file | scripter | 1 |
| script value | `eotg_aug_removal_base_value` (clinic price by removal kind, with the B3 discount) | values file | scripter | 1 |
| script value | `eotg_aug_seamless_windfall_value` | values file | scripter | G2 |
| static modifier | `eotg_mod_aug_fragments` (`icon = health_negative`, `health = -0.25`, `stress_gain_mult = 0.05`; applied for 5 years) | `common/modifiers/eotg_augmentation_modifiers.txt` | scripter | 1 |
| custom on_action | `eotg_on_trait_gained_aug_repair` | `common/on_action/eotg_augmentation_on_actions.txt` | scripter | 1 |
| custom on_action | `eotg_on_yearly_aug_former_check` | on_actions | scripter | G3 |
| custom on_action | `eotg_on_yearly_aug_seamless_check` | on_actions | scripter | G2 |
| character variable (permanent) | `eotg_aug_former` = `flag:removed` / `flag:excised` / `flag:rejected` (`flag:salvaged` is reserved for G8) | `eotg_aug_mark_former_effect`, then the callers override it | scripter | G3 |
| character variable (permanent, 0–3) | `eotg_aug_residue` | `eotg_aug_total_integration_effect` | scripter | G2 |
| character variable (timed, 30 days) | `eotg_aug_removal_kind` = `flag:partial` / `flag:downgrade` / `flag:full` | the three removal decisions | scripter | 1 |
| character variable (timed, 365 days) | `eotg_aug_repair_injury` = `flag:wounded` / `flag:maimed` / `flag:one_legged` / `flag:one_eyed` / `flag:blind` / `flag:disfigured` | `eotg_on_trait_gained_aug_repair` | scripter | 1 |
| character flag (timed, 3 years) | `eotg_flag_aug_repair_cooldown` | **set only in** `eotg_on_trait_gained_aug_repair` | scripter | 1 |
| character flag (timed, 30 days) | `eotg_flag_aug_procedure_injury` (this injury came from a procedure, so no repair offer follows) | `eotg_aug_procedure_apply_effect`, before a severe trait is added; read only by the repair on_action | scripter | 1 |
| character flag (one-shot, consumed by the roll) | `eotg_flag_aug_proc_under` ("put me under") | set by the craven options before the roll; cleared by the roll | scripter | 1 |
| character flags | `eotg_flag_aug_former_settling` (1 year), `eotg_flag_aug_phantom_done` (permanent until the next exit) | `eotg_aug_mark_former_effect`; the former on_action | scripter | G3 |
| character flag (timed, 2 years) | `eotg_flag_aug_seamless_cooldown` | **set only in** `eotg_on_yearly_aug_seamless_check` | scripter | G2 |
| saved scope values (event chain) | `eotg_proc_outcome`, `eotg_proc_provider`, `eotg_proc_kind`; saved scopes `eotg_proc_patient`, `eotg_proc_surgeon` | the roll effects | scripter | 1 |

**Reused, not new:**
- `eotg_opinion_aug_reassured` (+15) for the zealous welcome (G3).
- `eotg_opinion_aug_unease` (−10) for the Ledger's cuts (G2).
- `eotg_mod_aug_infection`, `eotg_mod_aug_clean_install`, `eotg_mod_illegal_implants`, `eotg_flag_aug_hidden_flaw`, `eotg_flag_aug_chain_edge` / `_strain`, `eotg_flag_aug_backalley_discreet`, `eotg_flag_aug_vendor_safe` / `_bold`.
- Vanilla: `death_treatment`, the traits in §6, and `recently_maimed_modifier` through `apply_maimed_trait_and_modifier_effect`.

**No new trait, opinion, story cycle, decision, death reason or icon.** Event art uses existing themes.

### 3.2 Changed (key kept)

| Key | Change | § |
|---|---|---|
| `eotg_aug_pay_upgrade_effect` | gains a param `MULT` (escrow and charge are both multiplied); all callers updated | 4.6 |
| `eotg_aug_can_afford_upgrade` | gains a param `MULT`; callers tier1.002 (a, d, e) pass `MULT = 1`, the Pursue decision passes the back-street multiplier | 4.6 |
| `eotg_aug_excision_surgery_effect` | gains params `MAIMED_BASE` (callers a/c/d pass 30) and `PHYSICIAN` (a/c/d pass `yes`) | 4.7 |
| `eotg_aug_excision_effect` | after `eotg_aug_remove_all_effect`: `set_variable = { name = eotg_aug_former  value = flag:excised }` | G3 |
| `eotg_aug_remove_all_effect` | calls `eotg_aug_mark_former_effect` last; `remove_variable = eotg_aug_residue` | G3, G2 |
| `eotg_clean_all_aug_modifiers` | removes `eotg_mod_aug_fragments` (guarded, as the batch's tooltip pattern) | 4.2 |
| `eotg_aug_total_integration_effect` | in its `hidden_effect`: `set_variable = { name = eotg_aug_residue  value = 3 }` | G2 |
| `eotg_aug_heir.004` (desc only; lore N5) | `desc_premonition`'s `triggered_desc` trigger gains `NOT = { has_trait = eotg_total_integration }`. The `first_valid` fallback `desc_silent` becomes a `triggered_desc` with the same `NOT` trigger. A new appended `triggered_desc = { trigger = { has_trait = eotg_total_integration }  desc = eotg_aug_heir.004.desc_seamless }` follows the `first_valid`. Options and logic are unchanged; this is not a new beat. | G2 |
| `eotg_decision_partial_removal`, `_overclock_regression`, `_remove_implants` | no `cost`. A gold floor in `is_valid` at the back-street price. The effect sets `eotg_aug_removal_kind` and fires proc.001. The old effect body moves into `eotg_aug_removal_perform_effect`. | 4.6 |
| `eotg_decision_consult_physician` | `is_shown` / `ai_potential` also pass for an unaugmented character holding `eotg_mod_aug_fragments`; the effect removes Fragments | 4.8 |
| `eotg_decision_aug_pursue_next_stage` | the `is_valid` gold floor becomes the back-street price (the cheapest path, as Seek does) | 4.6 |
| init.010 (a, c, d), init.018 (a, b, c), init.011, init.012, tier1.002, tier1.021, tier1.022, tier2.003, end.001, init.006, and the install offers in §4.5 | see §4 | 4 |
| `eotg_on_yearly_aug_initiation_check` | The Prosthetic branch: `factor = 2` when `has_variable = eotg_aug_former` | G3 |
| `yearly_playable_pulse` block (mod file) | adds `eotg_on_yearly_aug_former_check`, `eotg_on_yearly_aug_seamless_check` | G2, G3 |
| `on_trait_gained` (new vanilla hook for the mod, additive) | `on_actions = { eotg_on_trait_gained_aug_repair }` | 4.9 |

---

## 4. Wiring

### 4.1 Architecture: roll at the table, apply at the reveal

Three rules settle when the dice are thrown and when the result lands:

1. **The roll runs on a click**: an option, or an option's `after` block, at the moment the surgery narratively happens. It is never in an `immediate`.
   - Death on the table is applied **inside the roll**, as Excision already does (end.001 options → `eotg_aug_excision_surgery_effect`). A root that dies in an `immediate` is not a pattern this mod has proved.
2. **The roll decides; the reveal applies.** `eotg_aug_procedure_roll_effect` saves the outcome as a scope value. Every other consequence (modifiers, flags, traits, risk from complications) is applied by `eotg_aug_procedure_apply_effect` in the reveal event's `immediate`, so nothing shows on the character sheet before the event that explains it.
   - Saved scopes travel with `trigger_event`. The mod already relies on this: end.001 → end.002 (`scope:eotg_excision_outcome`) and tier2.013 → .014 (`scope:eotg_vendor_return`).
3. **Reveal routing.**
   - Install outcomes are revealed by **init.011** *The Scar Itches*, which already reads as provider-neutral.
   - The Enhanced upgrade is revealed by **tier1.022** (its own stage).
   - Everything else goes to **proc.002**.
   - Excision keeps end.002.
   - A reputable procedure whose outcome is plain (clean or hidden flaw) shows **no** report: it is applied silently. Repairs always report, because the result is the payoff.

```
# Shape of the public entry point (scripter writes the real body)
eotg_aug_procedure_effect = {
    eotg_aug_procedure_roll_effect = { PATIENT = $PATIENT$  PROVIDER = $PROVIDER$  PROCEDURE = $PROCEDURE$  SURGEON = $SURGEON$ }
    if = { limit = { NOT = { scope:eotg_proc_outcome = flag:death } }
        if = { limit = { scope:eotg_proc_kind = flag:repair }                       # always report
            $PATIENT$ = { trigger_event = { id = eotg_aug_proc.002  days = { 14 45 } } } }
        else_if = { limit = { OR = { scope:eotg_proc_outcome = flag:clean  scope:eotg_proc_outcome = flag:flaw } }
            $PATIENT$ = { eotg_aug_procedure_apply_effect = yes } }                 # silent
        else_if = { limit = { scope:eotg_proc_kind = flag:install }
            $PATIENT$ = { trigger_event = { id = eotg_aug_init.011  days = { 30 90 } } } }
        else = { $PATIENT$ = { trigger_event = { id = eotg_aug_proc.002  days = { 14 45 } } } }
    }
}
```
Callers wrap it in `hidden_effect` (the hidden-risk rule) and add a `custom_tooltip` that says the outcome is decided on the table (the end.001.tt precedent).

**G4/G8 hooks.** The roll takes `PATIENT` and `SURGEON` as scopes and `PROVIDER` / `PROCEDURE` as literals. A later interaction can operate on a spouse, a vassal or a prisoner with the liege's physician as surgeon, and needs no change to this effect. The reveal goes to `$PATIENT$`.

### 4.2 The shared roll: `eotg_aug_procedure_roll_effect`

**Params:**
- `PATIENT` (scope);
- `PROVIDER` = `clinic` | `physician` | `self` | `backstreet`;
- `PROCEDURE` = `install` | `upgrade` | `removal` | `repair`;
- `SURGEON` (scope). For `physician`, use `scope:eotg_proc_surgeon` from `eotg_aug_save_surgeon_effect`. For `self`, use the patient. Clinic and back streets ignore it, so pass the patient.

**Body, in order:**
1. `save_scope_as` eotg_proc_patient / eotg_proc_surgeon. `save_scope_value_as = { name = eotg_proc_provider  value = flag:$PROVIDER$ }` and the same for `eotg_proc_kind`. Precedent: `flag:$PARAM$` in `20_health_effects.txt:1102-1105`, and `00_scheme_scripted_effects.txt:713-718`.
2. `$PATIENT$ = { random_list = { … } }`, with weights in **units of 0.5%** (each provider's column sums to 200).
   - Every entry has base `0` and gets its column through `modifier = { add = N  scope:eotg_proc_provider = flag:x }`. This is the vanilla shape at `00_scheme_scripted_effects.txt:722-740`: base-0 entries, `add = $PARAM$`, and `factor = <script value>` at :738.
   - Each entry saves `eotg_proc_outcome`.
3. Procedure-kind risk (all in `hidden_effect`; `eotg_add_fracture_risk` is already a no-op for formers and Seamless):
   - **repair:** +2 Augmented / +4 Enhanced / +6 Overclocked / +8 Neurofractured;
   - **back streets on upgrade or repair:** +3 more.
4. If the outcome is `flag:death`: `death = { death_reason = death_treatment }` (vanilla `00_event_deaths.txt:214`, "died due to a botched treatment").
5. Clear the one-shot modifier flags: `eotg_flag_aug_proc_under`, `eotg_flag_aug_backalley_discreet`, and `eotg_aug_clear_chain_flags_effect`.

`eotg_aug_procedure_roll_booked_effect` is an if-ladder over `scope:eotg_proc_provider` that calls the roll with the matching literal. It is for a stage where the provider was chosen earlier in the chain (tier1.021).

**Weight table (per 200 = 100%):**

| Outcome (`flag:`) | Clinic | Physician / self | Back streets | Applied at the reveal (`eotg_aug_procedure_apply_effect`) |
|---|---|---|---|---|
| `clean` | 190 | 180 | 129 | repair: `eotg_aug_repair_injury_effect` |
| `excellent` | 2 | 4 | 6 | install/upgrade: `eotg_mod_aug_clean_install` 10 y; repair: injury removed and `clean_install` 5 y; removal: removes `eotg_mod_aug_removal_withdrawal` if held |
| `infection` | 6 | 10 | 20 | `eotg_mod_aug_infection` (install 2 y, otherwise 1 y); repair: injury also removed |
| `flaw` | 0 | 2 | 16 | `eotg_flag_aug_hidden_flaw` (repair: injury also removed). **Reported as clean** (spec §6.3, thread T6). |
| `rejection` | 2 | 4 | 12 | **install:** nothing here; init.011 d/e lead to init.012 (unchanged). **upgrade, "complication":** risk +10, infection 1 y. **removal, "fragments":** `eotg_mod_aug_fragments` 5 y. **repair, "failed":** injury stays, risk +5. |
| `discovered` | 0 | 0 | 10 | `eotg_mod_illegal_implants`; repair: injury also removed |
| `maimed` | 0 | 0 | 2 | flag `eotg_flag_aug_procedure_injury` 30 d; `apply_maimed_trait_and_modifier_effect`; `increase_wounds_no_death_effect = { REASON = treatment }` |
| `one_eyed` | 0 | 0 | 2 | as maimed, with `add_trait_force_tooltip = one_eyed` (vanilla `maimed_in_battle_effect` shape) |
| `blind` | 0 | 0 | 2 | as maimed: remove `one_eyed` if held, then `add_trait = blind` (guarded as `coronation_events_1.txt:8719-8726`) |
| `death` | 0 | 0 | 1 | applied **in the roll** (step 4); no reveal |
| **Bad total** | **4%** | **8%** | **32.5%**, of which severe is 3.5% (death 0.5%) | |

These are the gaps doc's bands. Back streets: clean 64.5, infection 10, flaw 8, rejection 6, discovered 5, maimed 1, eye 1, blind 1, death 0.5.

**Modifiers:**
- **All bad entries** (infection, flaw, rejection, discovered, maimed, one_eyed, blind, death) take `modifier = { factor = eotg_aug_proc_bad_factor }`.
- Entry-specific:
  - **infection:** ×2 on upgrade (deeper work); ×1.5 on upgrade with `eotg_flag_aug_vendor_bold`; +20 with `eotg_flag_aug_chain_strain` (this replaces init.011's strain +10 and tier1.022's +10, at the new scale).
  - **rejection:** ×2 on upgrade.
  - **flaw:** factor 0 on removal, or if the patient already has the flag.
  - **discovered:** factor 0 on removal, with `eotg_flag_aug_backalley_discreet`, or if the patient already has `eotg_mod_illegal_implants`.
  - **maimed / one_eyed / blind:** ×2 with `eotg_flag_aug_proc_under`. Factor 0 if the trait is already held (one_eyed is also 0 when blind).
  - **death:** factor 0 on **repair**. ×2 with `eotg_flag_aug_proc_under`.
  - **excellent:** ×2 on upgrade with `vendor_bold`.

**`eotg_aug_proc_bad_factor`** (script value, `value = 1`, then `multiply` steps). The stepped skill factors are vanilla `risky_wound_treatment_effect`'s shape (`20_health_effects.txt:2368-2420`):

| Condition | × |
|---|---|
| provider physician or self, and `scope:eotg_proc_surgeon.learning < medium_skill_rating` (10) | 1.25 |
| … learning ≥ `decent_skill_rating` (12) | 0.8 |
| … learning ≥ `high_skill_rating` (15) | 0.6 (in place of 0.8) |
| … surgeon has `lifestyle_physician` | 0.8 |
| provider `self` (operating on yourself) | 1.5 |
| `eotg_flag_aug_chain_edge` (replaces "clean +15") | 0.6 |
| upgrade with `eotg_flag_aug_vendor_safe` (the Bidding War folds in here) | 0.75 |
| patient `eotg_neurofractured` ("unstable") | 1.5 |
| `min = 0.2` | |

A physician at learning 16 with the physician lifestyle runs at about 4% bad, the gaps doc's "max 96" ceiling. A poor physician (learning < 10) runs at about 10%.

**`eotg_aug_save_surgeon_effect`:** if the patient `employs_court_position = court_physician_court_position`, save `court_position:court_physician_court_position` as `eotg_proc_surgeon` (as end.001's immediate does); otherwise save the patient. Vanilla's own helper is `save_court_physician_as_effect` (`20_health_effects.txt:1539`). It is not reused, because it adds a `court_owner` hop and an `is_physically_able` filter that `eotg_has_physician_access` does not mirror.

### 4.3 Pacing against HQ1 and HQ2 (why the numbers above are safe)

| Change | Old | New | Effect on the balance targets |
|---|---|---|---|
| Back-alley install, bad outcome | ~60% (rejection 15%; ≈ 9–10% of jobs end out of the system) | 32.5% (rejection 6%; ≈ 3.5% out of the system; death 0.5%) | Slightly more installs stay augmented. Back-alley is a minority of AI installs (one option of 4–5 in init.010 and init.018), so the HQ2 census (25–40% augmented at year 30) moves by about +1 point at most. The observer run (balance §9.2) measures it. |
| Enhanced upgrade, complication (risk +10) | 30% (15–45) | clinic ≈ 8%, physician ≈ 14%, back streets ≈ 42% after the ×2 upgrade modifiers | Mean risk on entering Overclocked falls by about 2 points at a clinic. Calm Overclocked accrual is 12–15 a year to a threshold of 80, so the cascade comes about 0.2 pulses later. That is within noise for HQ2's "≥ 15% Overclocked / Neurofractured / Seamless". The back street's risk +3 and its 42% complication give the cheap path a real cost. |
| Upgrade price | clinic only | back streets at 50% | Gold-poor AI counts, the failure case named in balance §5.1, can now progress. This **helps** HQ2's top band. |
| Time | — | no new waits or gates | **HQ1 is untouched.** The 5-year settle flag is the only floor. Procedures can delay (death, or rejection out of the system) but never speed up. |
| Repairs | none | +2 to +8 risk, about once or twice a reign | Pushes an injured ruler slightly toward the cascade. That is intended (invariant 5), and too rare to move HQ2. |

### 4.4 New events (Part 1)

All are `character_event`, in `events/eotg_augmentation_procedures.txt`, namespace `eotg_aug_proc`.
- Every option has an `ai_chance` with at least 2 trait modifiers (index §1 rule 6, as amended by L9).
- **One stress helper per option** (index §1 rule 6; CB-26 M2):
  - **proc.003**'s paid options run `eotg_aug_stress_surgery_effect`.
  - **proc.001**'s paid options run **no** surgery helper. Their stress comes from `eotg_aug_removal_perform_effect`, which carries each decision's original stress unchanged: the reject helper for a full removal, `medium_stress_impact_loss` for partial and downgrade.
- **G9 overlap** (`docs/specs/cybernetics_v2_trait_depth.md` §5.2, being built): impatient, gluttonous and temperate join `eotg_aug_stress_reject_effect`, and fickle joins `eotg_aug_stress_neglect_effect`.
  - Every option here that calls those helpers (proc.001 full removal through the perform effect, proc.003.d, end.001.e, and proc.002.c / init.011.c via neglect) picks up the new rows automatically.
  - **No option in this spec may add its own `stress_impact` line for impatient, gluttonous, temperate or fickle.** The only extra lines written here are content and ambitious (proc.020.a), ambitious (proc.001.d) and zealous (proc.020.e, proc.001.f). None of them is a G9 trait.

#### proc.001 *Who Takes It Out?* (removal provider)
- **Fired by:** `eotg_decision_partial_removal`, `eotg_decision_overclock_regression`, `eotg_decision_remove_implants` (`trigger_event` in the decision effect, as Seek fires init.018).
- **Trigger** (world-state guard): `has_variable = eotg_aug_removal_kind`, plus the tier matching the kind (partial ↔ `eotg_is_aug_tier2`, downgrade ↔ `eotg_is_aug_tier3`, full ↔ `eotg_is_aug_tier1`).
- **Desc:** base, plus one line per kind (`desc_partial` / `desc_downgrade` / `desc_full`), plus `desc_physician` if `eotg_has_physician_access`.
- **Immediate:** `eotg_aug_save_surgeon_effect`.
- **Paid options** run, in order:
  1. `eotg_aug_pay_procedure_effect = { BASE = eotg_aug_removal_base_value  MULT = … }`;
  2. `eotg_aug_removal_perform_effect`;
  3. `hidden_effect = { eotg_aug_procedure_effect = { PATIENT = root  PROVIDER = …  PROCEDURE = removal  SURGEON = … } }`;
  4. `custom_tooltip = eotg_aug_proc.001.tt`.
- **All options** end with `remove_variable = eotg_aug_removal_kind` (in `after`).

| Opt | Text intent | Trigger | Provider / price | Extra | ai_chance |
|---|---|---|---|---|---|
| a | "The clinic." | `eotg_aug_can_afford_procedure = { BASE = eotg_aug_removal_base_value  MULT = 1 }` | clinic ×1 | — | 40; +20 diligent; +10 craven; −20 greedy |
| b | "My own physician." | physician access; afford ×0.75 | physician ×0.75 | — | 40; +20 trusting; +10 diligent |
| c | "Someone cheaper." | afford ×0.4 | backstreet ×0.4 | — | 20; +20 greedy; +10 deceitful; −20 craven |
| d | "Not yet." | — | — | the minor ambitious stress line | 10; +20 ambitious; +10 stubborn |
| e [lifestyle_physician] | "I'll guide their hands myself." | `has_trait = lifestyle_physician`; NOT blind; afford ×0.25 | **self** ×0.25, `SURGEON = root` | — | 30; +30 lifestyle_physician; +10 arrogant |
| f [zealous], full removal only | "Every piece. I want none of it left." | zealous; kind = full; afford ×1 | clinic ×1 | +50 piety | 30; +30 zealous; +10 humble |

**`eotg_aug_removal_perform_effect`** moves the three decisions' current effect bodies, unchanged, into one if-ladder on `var:eotg_aug_removal_kind`:
- **partial:** XP 0, unmask congenital, medium stress loss, tooltip `eotg_decision_partial_removal_tooltip`;
- **downgrade:** halve risk, XP 50, the Countdown end block, `eotg_mod_oc_regression_recovery` 5 y, remove the intervention discount, unmask congenital, medium stress loss, its tooltip;
- **full:** `eotg_aug_remove_all_effect`, `eotg_mod_aug_removal_withdrawal` 3 y, `eotg_aug_stress_reject_effect`.

`eotg_aug_removal_base_value`:
- partial: `medium_gold_value`;
- downgrade: `major_gold_value`;
- full: `medium_gold_value`;
- ×0.75 when `stress_level >= 2` or the intervention discount applies (partial and downgrade only, as today; B3).

**Coupling:** a/b/c/e/f change tier.

#### proc.002 *After the Procedure* (outcome report)
- **Fired by:** `eotg_aug_procedure_effect`, for every non-install procedure with a reportable outcome, and for every repair. 14–45 days.
- **Trigger:** `is_alive = yes`. Nothing else: it is a chain stage, and the patient may have left the system.
- **Immediate:** `eotg_aug_procedure_apply_effect = yes`.
- **Desc:**
  - an opener by kind (`desc_upgrade` / `desc_removal` / `desc_repair`);
  - then a `first_valid` on `scope:eotg_proc_outcome` and kind: `outcome_excellent`, `outcome_infection`, `outcome_complication` (upgrade rejection), `outcome_fragments` (removal rejection), `outcome_repair_failed` (repair rejection), `outcome_discovered`, `outcome_maimed`, `outcome_one_eyed`, `outcome_blind`, and fallback `outcome_clean` (clean and flaw);
  - plus `desc_repair_residue` for a Seamless patient… (not reachable: Seamless repairs use proc.004; listed only so QA does not look for it).
- **Options (outcome stage, index §1 rule 6 / S12: one to three):**

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "It is done." / name variant `a_grim` "It will have to do." on bad outcomes | — | — | 30; +10 content; +10 lazy |
| b | "Fetch a physician." | outcome infection or fragments; physician access or `gold >= minor_gold_value` | as init.011.b: free with access, else `minor_gold_value`; removes infection / fragments if held | 40; +20 diligent; +20 craven; −20 greedy |
| c | "Sweat it out." | outcome infection; `eotg_is_augmented_any = yes` | as init.011.c: risk +5, 25% `ill`, neglect helper | 20; +20 stubborn; +20 greedy |

#### proc.003 *Spare Parts* (repair offer)
- **Fired by:** `eotg_on_trait_gained_aug_repair` (§4.9) for a non-Seamless augmented patient. 7–30 days.
- **Trigger:** `eotg_is_augmented_any = yes`, NOT `eotg_total_integration`, `eotg_aug_has_repair_injury = yes`.
- **Immediate:** `eotg_aug_save_surgeon_effect`.
- **Desc:**
  - base;
  - a `first_valid` on the injury (`desc_wounded`, `desc_maimed`, `desc_one_legged`, `desc_one_eyed`, `desc_blind`, `desc_disfigured`);
  - `desc_fractured` when Neurofractured ("No clinic will touch it": clinics refuse a patient whose implant is unstable);
  - `desc_physician` when there is physician access.
- **Paid options:** pay at medium base, then `hidden_effect = { eotg_aug_procedure_effect = { … PROCEDURE = repair … } }`, then `custom_tooltip = eotg_aug_proc.003.tt`.

| Opt | Text intent | Trigger | Provider / price (base `medium_gold_value`) | Extra | ai_chance |
|---|---|---|---|---|---|
| a | "The clinic." | NOT `eotg_neurofractured`; afford ×1 | clinic | — | 40; +20 diligent; +10 just; −20 greedy |
| b | "My own physician." | physician access; afford ×0.75 | physician | — | 40; +20 trusting; +10 diligent |
| c | "The back streets." | afford ×0.5 | backstreet | — | 25; +20 greedy; +10 deceitful; −20 craven |
| d | "Live with it." | — | — | `eotg_aug_stress_reject_effect`; `if zealous: add_piety = 25`. No risk move: the repair did not happen. | 20; +20 content; +20 zealous; −10 ambitious |
| e [lifestyle_physician] | "Hand me the tools." | NOT blind; afford ×0.25 | **self**, `SURGEON = root` | — | 30; +30 lifestyle_physician; +10 brave |
| f [cynical] | "Improve it while you're in there." | NOT `eotg_neurofractured`; afford ×1 | clinic | `eotg_mod_aug_lesson_prowess` 5 y; risk +5 (hidden) | 30; +30 cynical; +10 ambitious |

**Neurofractured** (gaps F call 3): **no episode on the table.** Clinics refuse, the physician and the back streets roll at ×1.5 bad, and pressure +8. An episode fired here would bypass `eotg_flag_nf_event_cooldown`, which the band pools own (lesson 5). The Neurofractured variant is a desc plus the hidden clinic option, **not a separate event**.

**Coupling:** a/b/c/e/f move risk inside the roll (repair scaling).

#### proc.004 *A Part Replaced* (Seamless repair; lore N1)
- **Fired by:** `eotg_on_trait_gained_aug_repair` for a Seamless patient. 7–30 days.
- **Trigger:** `has_trait = eotg_total_integration`, `eotg_aug_has_repair_injury = yes`.
- **Immediate:** `eotg_aug_repair_injury_effect`. No roll, no gold, no risk (risk is a no-op here by design).
- **Fiction (lore N1):** this is **not** self-repairing machinery, which is beyond 866 AG's tech level. The system logs the injury, orders the part against the existing fittings and books the technicians itself, and the cost was already budgeted. The mechanic is unchanged: no roll, no gold, no risk.
- **Desc:** base, plus `desc_residue` when `var:eotg_aug_residue >= 1` (the old expression of pain was logged). Binding wording is in the lore file.
- **One option:** a "Continue." (ai_chance base 100; a one-option notification, so the trait-modifier minimum does not apply, per S12).
- **Coupling:** reads residue.

### 4.5 Install paths

| Path | Change |
|---|---|
| **init.018 a** (clinic), **c** (physician) | After `eotg_aug_initiate_effect` and the risk set: `eotg_aug_save_surgeon_effect` (c), then `hidden_effect = { eotg_aug_procedure_effect = { PATIENT = root  PROVIDER = clinic/physician  PROCEDURE = install  SURGEON = … } }`, plus `custom_tooltip = eotg_aug_proc.install_tt`. Keep `eotg_mod_implant_calibrated`. |
| **init.018 b**, **init.010 a, c, d** (back streets; always revealed at init.011, 180–540 days) | Before the existing `trigger_event` to init.011: `hidden_effect = { eotg_aug_procedure_roll_effect = { PATIENT = root  PROVIDER = backstreet  PROCEDURE = install  SURGEON = root } }`. **Order in init.010.a:** the duel (which sets edge or strain) comes first, then the roll. **init.010.d** [craven] sets `eotg_flag_aug_proc_under` before the roll. **init.010.c** keeps setting the discreet flag before the roll. If the outcome is death, the trigger to init.011 is skipped (`if = { limit = { NOT = { scope:eotg_proc_outcome = flag:death } } … }`). |
| **init.011** | `immediate`: the whole `random_list` and its flag clean-up are **replaced** by `eotg_aug_procedure_apply_effect = yes`. Every `scope:eotg_alley_outcome` becomes `scope:eotg_proc_outcome`. The existing five descs stay. **New descs:** `desc_maimed`, `desc_one_eyed`, `desc_blind`, placed first in the `first_valid`. Pain animation on those too. Options a–f are unchanged; a's grim name also covers the three severe outcomes. |
| **init.012** | In the `lost` branch, after `eotg_aug_remove_all_effect`: `set_variable = { name = eotg_aug_former  value = flag:rejected }`. Same in **tier1.015**'s remove-all branch. |
| **Other install offers** (ruler self-installs; one hidden call to `eotg_aug_procedure_effect` per option, after the install lines; provider by fiction) | **clinic:** init.001 a, d, e · init.002 a · init.003 a, d · init.005 a, d · init.006 a, e, f · init.009 a, d · init.016 a, e · init.019 a, d · init.020 d (if it installs on root; scripter confirms). **physician** (with `eotg_aug_save_surgeon_effect`): init.006 c · init.017 a, d. **backstreet:** init.002 d · init.004 a, e (their existing illegal modifier and hidden flaw switch the matching outcomes off). |
| **Not rolled** (own outcome logic, or another patient, which is G4 scope) | init.007/.008 (the Bridge's settle stage), init.013 (a parent's hardware: own flaw), init.014/.015 (the child arc), init.017 c, init.002 c, tier1.004, tier1.015 b, tier1.018, patron and heir installs, `eotg_aug_retainer_install_effect`, `eotg_aug_child_install_effect`, the nr.* lifecycle. |

**What Was Taken (G3, no event).** init.006 gets an appended `triggered_desc` `eotg_aug_init.006.desc_former` (`var:eotg_aug_former ?= flag:excised`): the surgeons who took the hardware took this too. The initiation check's Prosthetic branch gets `modifier = { factor = 2  has_variable = eotg_aug_former }`.

### 4.6 Upgrades and pricing

**Pricing helpers.**
- `eotg_aug_can_afford_procedure = { BASE  MULT }` → `gold >= { value = $BASE$  multiply = $MULT$ }`.
- `eotg_aug_pay_procedure_effect` → `remove_short_term_gold` with the same value.
- Shape: the mod's `eotg_aug_patron_can_pay` / `eotg_aug_patron_pay_effect` (`{ BASE  MULT }`), QA-passed.

**tier1.002 (Enhanced; the provider is chosen here, the surgery happens at .021).**
- Each paying option saves `save_scope_value_as = { name = eotg_proc_provider  value = flag:… }`.
- a, d and e: clinic. They use `eotg_aug_pay_upgrade_effect = { MULT = 1 }` and `eotg_aug_can_afford_upgrade = { MULT = 1 }`.
- New options:

| Opt | Text intent | Trigger | Provider | ai_chance |
|---|---|---|---|---|
| f | "My own physician." | physician access; `eotg_aug_can_afford_upgrade = { MULT = eotg_aug_price_mult_physician }` | physician | 35; +20 trusting; +10 diligent; ×0.1 rule n/a (follow-through) |
| g | "Someone cheaper." | `eotg_aug_can_afford_upgrade = { MULT = eotg_aug_price_mult_backstreet_upgrade }` | backstreet | 20; +20 greedy; +10 ambitious; −20 craven |

Both fire tier1.021 as a does. g does not get a's stewardship duel: you are not vetting anyone.

**tier1.021:** `after` gains, before its `trigger_event`:
1. `eotg_aug_save_surgeon_effect`;
2. `hidden_effect = { eotg_aug_procedure_roll_booked_effect = { PATIENT = root  PROCEDURE = upgrade  SURGEON = scope:eotg_proc_surgeon } }`;
3. if the outcome is death, skip the trigger to .022.

The focus choice is the consent at the table.

**tier1.022:**
- `immediate`: its `random_list`, the physician/edge/strain modifiers and the `if` on complication are **replaced** by `eotg_aug_procedure_apply_effect = yes`. The flag removals and escrow clean-up stay.
- Desc mapping: `desc_complication` (existing) for `flag:infection`. **New** `desc_rejection` for `flag:rejection` (risk +10 and infection: the body fights the new hardware). Shared lines `eotg_aug_proc.outcome_excellent / _discovered / _maimed / _one_eyed / _blind`. `desc_clean` stays the fallback.
- Both options still set XP 50: the tier change stands on every outcome except death.

**tier2.003 (Overclocked; the surgery happens on the click).**
- a, c and d are clinic. After their XP line: `hidden_effect = { eotg_aug_procedure_effect = { PATIENT = root  PROVIDER = clinic  PROCEDURE = upgrade  SURGEON = root } }`.
- New options:

| Opt | Text intent | Trigger | Provider / price (`major_gold_value`) | ai_chance |
|---|---|---|---|---|
| f | "My own physician." | physician access; afford ×0.75 | physician | 35; +20 trusting; +10 diligent |
| g | "Someone cheaper." | afford ×0.5 | backstreet | 20; +20 greedy; +10 ambitious; −20 craven |

  Both: pay, XP 100, the roll as above, the surgery helper.
- Neither f nor g gets the sought-flag 0.1 factor (they are follow-throughs; balance §5.1 item 3).
- The **Bidding War** is folded in through the roll (`vendor_safe` bad ×0.75; `vendor_bold` infection ×1.5, excellent ×2). tier2.013/.014 are not edited.

**Pursue the Next Stage:** the `is_valid` gold floor becomes `eotg_aug_can_afford_upgrade = { MULT = eotg_aug_price_mult_backstreet_upgrade }` (tier 1) and `gold >= { value = major_gold_value  multiply = eotg_aug_price_mult_backstreet_upgrade }` (tier 2). This is the cheapest path, as Seek's floor is. **It amends balance §5.1's "mirror option a" note:** the decision still never shows an event the ruler cannot act on, since back streets is always offered.

**Removal decisions** (all three):
- Delete `cost`.
- `is_valid = { eotg_aug_can_afford_procedure = { BASE = eotg_aug_removal_base_value  MULT = eotg_aug_price_mult_backstreet_removal } }` (the Seek shape: "the hub charges per path"). The script value reads `var:eotg_aug_removal_kind`, which is unset when `is_valid` is evaluated. So each decision instead writes its literal base (`medium_gold_value` / `major_gold_value`, with the 0.75 discount `if`) into the trigger's `BASE`.
- `effect = { set_variable = { name = eotg_aug_removal_kind  value = flag:…  days = 30 }  custom_tooltip = <existing tooltip key>  trigger_event = eotg_aug_proc.001 }`.
- `ai_potential` adds `short_term_gold >=` the back-street price.
- Ruling L1 ("cost alone, no gold in is_valid") is superseded for these three, for the same reason Seek has no cost: a decision cost would charge twice.

### 4.7 Excision (end.001)

`eotg_aug_excision_surgery_effect` gains two params:
- `MAIMED_BASE` replaces the literal 30;
- `PHYSICIAN` gates both physician modifiers (death −15, clean +15) with `always = $PHYSICIAN$`.

a, c and d pass `MAIMED_BASE = 30  PHYSICIAN = yes`.

**New option e "Not their table. Somewhere cheaper."**

| Field | Value |
|---|---|
| trigger | NOT `eotg_flag_aug_excision_free` (the surgeons are already in the room); `eotg_aug_can_afford_procedure = { BASE = major_gold_value  MULT = eotg_aug_price_mult_backstreet_removal }` |
| effect | pay ×0.4 (ignores the promised-treatment half; the promise was to the real surgeons); `custom_tooltip = eotg_aug_end.001.tt`; `hidden_effect = { eotg_aug_excision_surgery_effect = { DEATH_BASE = 25  BRAVE = no  MAIMED_BASE = 40  PHYSICIAN = no } }`; `eotg_aug_stress_reject_effect` |
| ai_chance | 15; +20 greedy; +10 brave; −20 craven |

This is the gaps doc's back-street table: death +10, maimed +10.

**The physician's −15 does not apply in the back street** (upheld by the lore-keeper, 2026-10-04). Thread T5's premise is "your physician stays at the table" (`desc_physician`), and that table is the sanctioned one. Where the gaps doc said the physician "keeps its −15", this spec reads it as "the clinic options keep it". Only the human can reverse it now, with one param.

Survivors still go through `eotg_aug_excision_effect`, which now marks `flag:excised`.

### 4.8 Consult the Physician (Fragments)

- `is_shown` and `ai_potential` become `OR = { has_trait = eotg_cybernetics  AND = { eotg_is_augmented_any = no  has_character_modifier = eotg_mod_aug_fragments } }`, plus physician access.
- The effect gains a guarded `remove_character_modifier = eotg_mod_aug_fragments`.
- The calibration modifier is wrapped in `if = { limit = { has_trait = eotg_cybernetics } }`, so a former character is not "calibrated".

### 4.9 Repairs: `on_trait_gained`

```
on_trait_gained = { on_actions = { eotg_on_trait_gained_aug_repair } }      # additive (invariant 4)

eotg_on_trait_gained_aug_repair = {
    trigger = {
        is_alive = yes
        eotg_is_augmented_any = yes
        OR = { is_ai = no  highest_held_title_tier >= tier_county }
        OR = {
            scope:trait = trait:wounded_3   scope:trait = trait:maimed     scope:trait = trait:one_legged
            scope:trait = trait:one_eyed    scope:trait = trait:blind      scope:trait = trait:disfigured
        }
        NOT = { has_character_flag = eotg_flag_aug_repair_cooldown }     # cooldown authority: here only
        NOT = { has_character_flag = eotg_flag_aug_procedure_injury }    # a procedure's own injury
    }
    effect = {
        add_character_flag = { flag = eotg_flag_aug_repair_cooldown  years = 3 }
        # map scope:trait -> set_variable eotg_aug_repair_injury = flag:<x> (days = 365), one if per trait
        if = { limit = { has_trait = eotg_total_integration }  trigger_event = { id = eotg_aug_proc.004  days = { 7 30 } } }
        else = { trigger_event = { id = eotg_aug_proc.003  days = { 7 30 } } }
    }
}
```

- **wounded_2 is excluded** (gaps F call 2), as is wounded_1.
  - wounded_2 is a routine battle outcome (`maimed_in_battle_effect` and the combat wound effects add it), and vanilla's own wound treatment covers it (`decide_who_picks_wound_treatment_effect`, `20_health_effects.txt:3730`).
  - The cybernetic repair is for permanent losses and near-death wounds. That keeps it to "once or twice a reign".
- **`eotg_aug_repair_injury_effect`:**
  - `flag:wounded` → `eotg_aug_heal_wounds_effect`;
  - otherwise remove the named trait if it is held; for `maimed`, also remove `recently_maimed_modifier` if held;
  - then `remove_variable = eotg_aug_repair_injury`.
- **`eotg_aug_has_repair_injury`:** wounded → `has_trait_rank = { trait = wounded  rank = 3 }` (or `has_trait = wounded_3`); otherwise `has_trait = <the named trait>`.
- **In-game check (engine fact not settled by vanilla):** whether `change_trait_rank` (used by `increase_wounds_no_death_effect`) fires `on_trait_gained` for `wounded_3`. No vanilla on_trait_gained handler tests a wounded rank. If it does not fire, wounded_3 repairs simply never offer. That is acceptable, and lost body parts are unaffected. No fallback script is built.
- Characters who start with these traits at history load: the check also confirms the hook does not fire for them. If it does, add `NOT = { has_game_started… }`. Do not guess the guard until then.

### 4.10 G3: the former marker and its aftermath

**`eotg_aug_mark_former_effect`** is called last in `eotg_aug_remove_all_effect`, so every exit gets it: Remove Implants, Excision, Rejection, nr.006, and the retinue reversal.
1. `set_variable = { name = eotg_aug_former  value = flag:removed }`. Excision, init.012 and tier1.015 then overwrite it with `flag:excised` / `flag:rejected`.
2. `add_character_flag = { flag = eotg_flag_aug_former_settling  years = 1 }`; `remove_character_flag = eotg_flag_aug_phantom_done`. Each exit gets its own aftermath.
3. **Welcome back** (no event). If the character is landed (`is_landed = yes`): `every_vassal` and `every_courtier`, limited to `has_trait = zealous`, get `add_opinion = { modifier = eotg_opinion_aug_reassured  target = root  years = 5 }`. Cynical ones get nothing ("don't warm").

**Why a variable, not a trait.**
- A trait needs an icon (human art debt) and would show on every character sheet and in AI opinion. That is a public stigma the design does not ask for.
- A flag cannot record *how* the character left, which the aftermath desc and G8's future `flag:salvaged` need.
- Vanilla records history states as variables holding flags (`set_variable … value = flag:$X$`, `00_scheme_scripted_effects.txt:729-732`).
- The variable is **permanent and kept on re-installation** ("has been out before"), so later content can read relapse.

**Fit with patron.008 (new_beats §5.2).**
- patron.008's entry tests `eotg_is_augmented_any = no` and is unchanged.
- The marker is set in the same effect that removes the trait, so it is always present when the paper is served. Phantom Static waits at least 1 year (the settling flag), and the Patron tick normally serves the paper first.
- If the owner relapses through Phantom Static before the paper comes, the paper never fires. The demand sequence continues, which is new_beats' stated behaviour for re-installs.
- patron.008.c and Phantom Static's relapse are **different routes back** (the syndicate's technicians, or the ruler's own choice of provider through init.018). They do not need to exclude each other.

**`eotg_on_yearly_aug_former_check`** (on `yearly_playable_pulse`):
- limit: `has_variable = eotg_aug_former`, `eotg_is_augmented_any = no`, NOT `eotg_flag_aug_former_settling`, NOT `eotg_flag_aug_phantom_done`;
- effect: `random = { chance = 35  add_character_flag = eotg_flag_aug_phantom_done  trigger_event = { id = eotg_aug_proc.020  days = { 1 60 } } }`.

#### proc.020 *Phantom Static*
- **Trigger** (world-state guard, mirrors the on_action): `eotg_is_augmented_any = no`, `has_variable = eotg_aug_former`.
- **Desc:**
  - base: a reflex reaches for an overlay that isn't there; the half-second early is gone;
  - a `first_valid` on the marker (`desc_excised` / `desc_rejected` / fallback `desc_removed`);
  - `desc_fragments` when holding `eotg_mod_aug_fragments`.

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "It will fade." | — | stress: content minor loss, ambitious minor gain | 30; +20 content; +10 patient |
| b | "See my physician." | physician access | medium stress loss; remove `eotg_mod_aug_fragments` / `eotg_mod_aug_infection` if held | 30; +20 diligent; +10 craven |
| c | "Call the clinic." | `eotg_can_receive_augmented = yes`; NOT `eotg_mod_aug_excision_recovery`; `gold >= tiny_gold_value` | `custom_tooltip = eotg_aug_proc.020.c.tt`; `trigger_event = eotg_aug_init.018` (the provider hub charges) | 20; +20 ambitious; +10 cynical; −30 zealous |
| d | "Replace what was taken." | `eotg_has_physical_loss = yes`; NOT excision recovery | `trigger_event = eotg_aug_init.006` | 30; +20 brave; +10 ambitious |
| e [zealous] | "As I was made." | zealous | +50 piety; zealous minor stress loss | 30; +30 zealous; +10 humble |

- **Coupling:** c and d lead into an install (tier). The desc reads the marker.
- init.018's own trigger and init.006's install guard re-check eligibility on arrival.

### 4.11 G2: Seamless ongoing life

**`eotg_on_yearly_aug_seamless_check`** (on `yearly_playable_pulse`, added after the Neurofractured check):

```
trigger = { has_trait = eotg_total_integration }
effect = { if = { limit = { NOT = { has_character_flag = eotg_flag_aug_seamless_cooldown } }
  random_list = {
    30 = { add_character_flag = { flag = eotg_flag_aug_seamless_cooldown  years = 2 }  trigger_event = { id = eotg_aug_end.040  days = { 1 30 } } }
    25 = { trigger = { any_councillor = { is_landed = no  NOT = { this = root } } }
           add_character_flag = { … years = 2 }  trigger_event = { id = eotg_aug_end.041  days = { 1 30 } } }
    10 = { trigger = { var:eotg_aug_residue ?= { >= 1 } }   # scripter: use the mod's `?=` idiom for a missing var
           add_character_flag = { … years = 2 }  trigger_event = { id = eotg_aug_end.042  days = { 1 30 } } }
    20 = { trigger = { eotg_aug_has_heir_arc = no  NOT = { has_character_flag = eotg_flag_aug_heir_arc_done }
                       primary_heir ?= { is_alive = yes  is_adult = yes } }
           add_character_flag = { … years = 2 }
           # start eotg_story_aug_heir_arc exactly as the Overclocked check does (balance §5.8a),
           # then random_owned_story = { limit = { story_type = eotg_story_aug_heir_arc }  set_variable = { name = eotg_stage  value = 3 } }
           # -- the same jump eotg_aug_total_integration_effect makes: the next tick fires heir.004 (the Choice) }
    100 = { # nothing; AI-only factors as the NF lists (balance §5.10a): count x2.5, duke x1.75, king+ x1.25
    }
  } } }
```

**"The heir confronts what's in the chair"** is **heir.004**, reused through the arc. It is not a new event. heir.004 gets the Seamless-owner desc from lore N5 (§3.2). M11 holds: the arc runs once per ruler, plus at most the one reprise from new_beats. The done flag gates it.

#### end.040 *The Ledger Balances*
- **Trigger:** `has_trait = eotg_total_integration`.
- **Desc:** base, plus `desc_residue_high` (`var:eotg_aug_residue >= 2`: a hesitation over one line, the pardons budget, and then it is cut) or `desc_residue_low` (no hesitation at all).
- **`eotg_aug_seamless_windfall_value`:** `medium_gold_value`, multiplied by `(1 + 0.5 × (3 − residue))`. The less is left, the cleaner the books.

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "Bank the surplus." | — | `add_gold = minor_gold_value` | 30; +10 education_stewardship_3; +10 education_learning_3 |
| b | "Cut what does not pay." | — | `add_gold = eotg_aug_seamless_windfall_value`; `every_vassal = { add_opinion = { modifier = eotg_opinion_aug_unease  target = root  years = 5 } }`; **residue −1** (hidden, clamped at 0) | 30; +20 education_stewardship_4; +10 education_intrigue_3 |
| c | "Return it to the realm." | — | `add_prestige = 150`; no gold | 30; +10 education_diplomacy_3; +10 education_martial_3 |
| d [education_stewardship_4 or _5] | "Rebalance every ledger." | `trait = education_stewardship_4` (icon) | as b without the opinion; **residue −1** | 30; +30 education_stewardship_4; +20 education_stewardship_5 |

#### end.041 *A Resignation*
- **Trigger:** Seamless; `any_councillor = { is_landed = no  NOT = { this = root } }`.
- **Immediate:** `random_councillor = { limit = { is_landed = no  NOT = { this = root } }  save_scope_as = eotg_resigner }`. This is a chosen target, not an episode victim (index rule 7, CB-26 L4). Named in loc, with a portrait.
- **Desc:** the councillor resigns because the work is correct and no one is there. Residue band line as end.040 (`desc_residue_high` / `_low`).

| Opt | Text intent | Effect | ai_chance |
|---|---|---|---|
| a | "Accept it." | `scope:eotg_resigner = { move_to_pool = yes }` (verified in index §2) | 30; +10 education_diplomacy_3; +10 education_learning_3 |
| b | "Order them to stay." | `add_dread = 15`; `scope:eotg_resigner = { add_opinion = { modifier = eotg_opinion_aug_unease  target = root  years = 5 } }`; **residue −1** | 30; +20 education_martial_3; +10 education_intrigue_3 |
| c | "Ask them why." | `if residue >= 1`: they stay; `scope:eotg_resigner = { add_opinion = { modifier = eotg_opinion_aug_admiration  target = root  years = 5 } }`; **residue −1** (answering costs something). `else`: no answer is possible; they leave (`move_to_pool`). Branch toasts `.c.stays` / `.c.leaves` (the hunt.8540 toast pattern used at tier3.014.b). | 30; +20 education_diplomacy_4; +10 education_learning_4 |

**`random_councillor` / `any_councillor`:** the scripter confirms both in PX `effects.log` / `triggers.log` (character scope) before building. If either is missing, use `random_courtier` with `limit = { is_councillor = yes }`.

#### end.042 *A Flicker*
- **Trigger:** Seamless and `var:eotg_aug_residue >= 1`.
- **Immediate:** `change_variable` residue −1 (hidden, clamped at 0).
- **Desc:** `desc` (a reflex surfaces: a hand reaches for someone who left; it is logged and filed), plus `desc_last` appended when residue is now 0 ("It does not happen again").
- **One option:** a "Continue." (the gaps doc's "one option, no choice"; S12). **Lore N2:** the reflex is a routine that fires at a scheduled hour and is logged as redundant and pruned. It never reaches for a person.
- **Coupling:** moves and reads residue.

**Seamless characters have no personality traits** (`eotg_aug_total_integration_effect` removes all 36). So their trait options and `ai_chance` modifiers use education traits (`00_traits.txt:208, 234, 368, 394, 549, 774, 816` and siblings). That is the only trait family a Seamless ruler is guaranteed to keep. Stress helpers are omitted for the same reason.

---

## 5. File placement

| Path | What |
|---|---|
| `events/eotg_augmentation_procedures.txt` | **new**: namespace `eotg_aug_proc`; proc.001–.004, .020. Header in the style of the other files (fires-from map, resource line). UTF-8 with BOM, as the siblings. |
| `events/eotg_augmentation_endgame.txt` | end.040–.042; edit end.001 (e), header |
| `events/eotg_augmentation_initiation.txt` | init.010, .011, .012, .018, .006 desc, the §4.5 install offers |
| `events/eotg_augmentation_tier1.txt` | tier1.002, .015 (marker), .021, .022 |
| `events/eotg_augmentation_tier2.txt` | tier2.003 |
| `common/scripted_effects/eotg_augmentation_effects.txt` | §3.1 effects; §3.2 changes |
| `common/scripted_triggers/eotg_augmentation_triggers.txt` | `eotg_aug_can_afford_procedure`, `eotg_aug_has_repair_injury`; `eotg_aug_can_afford_upgrade` param |
| `common/script_values/eotg_augmentation_values.txt` | §3.1 values |
| `common/modifiers/eotg_augmentation_modifiers.txt` | `eotg_mod_aug_fragments` |
| `common/decisions/eotg_augmentation_decisions.txt` | the three removal decisions, Consult, Pursue |
| `common/on_action/eotg_augmentation_on_actions.txt` | `on_trait_gained` block; three custom on_actions; header cooldown list gains `eotg_flag_aug_repair_cooldown`, `eotg_flag_aug_seamless_cooldown`, `eotg_flag_aug_phantom_done` |
| `localization/english/eotg_augmentation_l_english.yml` | §7 |

No new folder. No `replace_path`. `on_trait_gained` is a vanilla hook, extended additively.

---

## 6. Vanilla precedent

All under `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`.

| Mechanism | File:line | Used for |
|---|---|---|
| `on_trait_gained`: root = character, `scope:trait`; test `scope:trait = trait:x` | `common/on_action/traits_on_actions.txt:6`, `:13` | §4.9 |
| `flag:$PARAM$` into a saved scope value | `common/scripted_effects/20_health_effects.txt:1102-1105` | roll step 1 |
| Base-0 `random_list` entries driven by `modifier = { add = $PARAM$ }`, `scope:x = flag:y` tests, `factor = <script value>` | `common/scripted_effects/00_scheme_scripted_effects.txt:692-745` (factor :738; value `00_scheme_values.txt:704`) | roll body, `eotg_aug_proc_bad_factor` |
| Physician-skill stepped odds, critical success/failure | `20_health_effects.txt:2368-2420` (`risky_wound_treatment_effect`) | bad factor |
| Court physician as a saved scope | `20_health_effects.txt:1539` (`save_court_physician_as_effect`); the mod's end.001 immediate | `eotg_aug_save_surgeon_effect` |
| Wound step without death / with death | `20_health_effects.txt:1101` (`increase_wounds_no_death_effect`), `:1332` (`increase_wounds_effect`) | severe outcomes (the no-death form, so death odds stay exactly the death weight) |
| Loss trait plus a wound in one outcome | `20_health_effects.txt:1355-1395` (`maimed_in_battle_effect`, `add_trait_force_tooltip`) | one_eyed |
| Maimed with its modifier | `20_health_effects.txt:1398` (`apply_maimed_trait_and_modifier_effect`); `common/modifiers/00_event_modifiers.txt:225` | maimed |
| Guarded `add_trait = blind` | `events/activities/coronation_activity/coronation_events_1.txt:8719-8726` | blind |
| Death reason | `common/deathreasons/00_event_deaths.txt:214` (`death_treatment`; loc "died due to a botched treatment") | death on the table |
| Traits used | `common/traits/00_traits.txt`: `wounded_1/2/3` :5771/:5807/:5847 (group `wounded`, levels 1–3), `maimed` :5886, `one_eyed` :5930, `one_legged` :5966, `disfigured` :6002, `blind` :7039, `lifestyle_physician` :2059, `education_*` :11–868 | throughout |
| Wound treatment that already covers routine wounds | `20_health_effects.txt:3730` (`decide_who_picks_wound_treatment_effect`) | wounded_2 excluded |
| Decision with no cost that fires a paying hub event | `common/decisions/00_lifestyle_decisions.txt:342` (`commission_epic_decision`); the mod's Seek decision | removal decisions |

**Tiger:** the severe outcomes reach `increase_wounds_no_death_effect`, so the 16 known-benign 1.20 errors in vanilla `20_health_effects.txt` (`CLAUDE.md` §Validation) will also appear on this path. They are not new findings.

---

## 7. Loc surface (eotg-localizer)

**Binding renderings:** [cybernetics_v2_procedures_lore.md](cybernetics_v2_procedures_lore.md) (eotg-lore-keeper, 2026-10-04). It gives the exact text for the keys below, plus must-fixes N1–N5 and the residue register. Where it gives a rendering, the localizer uses it verbatim. The briefs in this section are fallback guidance only.

Rules:
- index §5, items 1–8;
- US spelling (balance §8);
- bare `[x.GetName]`;
- appended desc lines start with `\n\n`;
- **no tooltip quantifies risk or odds** (the hidden rule; duel-style percentages appear nowhere here);
- back-alley register as init.010–.012;
- **no named clinic, no named syndicate, no named authority**.

**Licensing wording, kept neutral on purpose.** The lore-keeper's `docs/lore/` check (2026-10-04) confirms that licensing is local and unnamed at 866. The neutral wording below stands, and survives either reading.
- All new text says "the clinic", "a clinic that keeps records", "the back streets", "someone cheaper".
- It **neither names nor characterizes** whoever sanctions a clinic: no "local", "your law's", "licensed by", "galactic" or "registered".
- Then neither outcome of the lore check forces a rewrite. (The existing "A sanctioned clinic." in init.018.a is not touched here.)

**No vanilla string needs a `replace/` override.**

| Keys | Count |
|---|---|
| `eotg_aug_proc.001.t`, `.desc`, `.desc_partial`, `.desc_downgrade`, `.desc_full`, `.desc_physician`, `.a`–`.f`, `.tt` | 13 |
| `eotg_aug_proc.002.t`, `.desc_upgrade`, `.desc_removal`, `.desc_repair`, `.a`, `.a_grim`, `.b`, `.c` | 8 |
| shared outcome lines `eotg_aug_proc.outcome_clean`, `_excellent`, `_infection`, `_complication`, `_fragments`, `_repair_failed`, `_discovered`, `_maimed`, `_one_eyed`, `_blind` (used by proc.002 and tier1.022) | 10 |
| `eotg_aug_proc.install_tt` (on every rolled install option: "How it took will be known when the incision heals.") | 1 |
| `eotg_aug_proc.003.t`, `.desc`, `.desc_wounded`, `.desc_maimed`, `.desc_one_legged`, `.desc_one_eyed`, `.desc_blind`, `.desc_disfigured`, `.desc_fractured`, `.desc_physician`, `.a`–`.f`, `.tt` | 17 |
| `eotg_aug_proc.004.t` ("A Part Replaced"), `.desc`, `.desc_residue`, `.a` | 4 |
| `eotg_aug_heir.004.desc_seamless` (lore N5, exact text in the lore file) | 1 |
| `eotg_aug_proc.020.t`, `.desc`, `.desc_removed`, `.desc_excised`, `.desc_rejected`, `.desc_fragments`, `.a`–`.e`, `.c.tt` | 12 |
| `eotg_aug_init.011.desc_maimed`, `.desc_one_eyed`, `.desc_blind` | 3 |
| `eotg_aug_init.006.desc_former` | 1 |
| `eotg_aug_tier1.002.f`, `.g` · `eotg_aug_tier1.022.desc_rejection` · `eotg_aug_tier2.003.f`, `.g` | 5 |
| `eotg_aug_end.001.e` | 1 |
| `eotg_aug_end.040.t`, `.desc`, `.desc_residue_high`, `.desc_residue_low`, `.a`–`.d` | 8 |
| `eotg_aug_end.041.t`, `.desc`, `.desc_residue_high`, `.desc_residue_low`, `.a`–`.c`, `.c.stays`, `.c.leaves` | 9 |
| `eotg_aug_end.042.t`, `.desc`, `.desc_last`, `.a` | 4 |
| `eotg_mod_aug_fragments`, `eotg_mod_aug_fragments_desc` | 2 |
| **revised** (existing keys): `eotg_decision_partial_removal_tooltip`, `eotg_decision_overclock_regression_tooltip` (now "Choose who performs it"), `eotg_decision_remove_implants_tooltip` (exists, loc line 1747), `eotg_decision_consult_physician_selection_tt` (mentions fragments) | 4 revised |
| **Total** | **~102 new** (the lore file's ~101, plus `heir.004.desc_seamless` from N5), **4 revised** |

**Briefs:**
- **proc.001:** desc_full is the last hardware out. desc_downgrade is "the overclock comes off; the rest stays". f [zealous] is faith-neutral ("as I was made"; index §5 deferral note).
- **Severe outcome lines** (`outcome_maimed / _one_eyed / _blind`, init.011's three): factual and medical, with no gore beyond init.012's level. Blindness is the optic interface failing on the table.
- **outcome_fragments:** "they missed some". Wire and splinters left in. Never "the implant is still there".
- **proc.003.desc_fractured:** clinics refuse a patient whose hardware is unstable. Neurofractured register (index §5 items 1–2: internal, never external, no banned words).
- **proc.004 and end.040–.042** are **Seamless register**. There is no voice, and "There is no one left" stays true.
  - **Residue register** (lore ruling (a)). **Allowed:** motor patterns, facial reflexes, standing instructions, schedules, and the court's perception of them. **Never:** preference, hesitation, longing, regret, felt recognition, memory as an experience, a "spark", soul, humanity or "the old self", or anything returning or growing.
  - **Every residue line ends with the thing logged, filed or pruned.**
  - N3: end.040 `desc_residue_high` is a standing instruction older than the integration, flagged and cut. It is not mercy.
  - N4: end.041 `.c.stays` is written from the councillor's perception only.
  - end.042's one option is "Continue." (end.010's wording; a separate key).
- **end.041:** the councillor is named (`[eotg_resigner.GetName]`). Medieval leaks per index §5.6.
- **proc.020:** the reflex reaching for an absent overlay. Must not use "whisper", "voice", "static that speaks", or anything external (the Void register is the opposite). The title *Phantom Static* is a working name for the lore-keeper.
- **Titles (approved, lore ruling (b)):** *Who Takes It Out?*, *After the Procedure*, *Spare Parts*, *A Part Replaced* (N1), *Phantom Static*, *The Ledger Balances*, *A Resignation*, *A Flicker*.

---

## 8. Lore constraints

- **866 AG** (`CLAUDE.md` §Canon). Cybernetics is still developing (SETTING LORE): reputable clinics exist and are not perfect (4%), and cheap work is dangerous.
- **No Galactic League.** No authority above the polity. Provider wording stays neutral (§7). The `docs/lore/` review confirms licensing is local and unnamed at 866.
- **Tech level (lore N1):** nothing here repairs itself. Self-repairing machinery is post-866 (975, the Gnomish Mechanized Renaissance), so the Seamless repair is ordered parts and booked technicians.
- **The syndicate stays unnamed.** Nothing here names it. patron.008 is untouched.
- **Voice register** (index §5.1–2): the voice appears in none of these events. Seamless has no voice (`eotg_aug_voice = 5`). Former characters have no voice.
- **Lore review: done** (eotg-lore-keeper, 2026-10-04, [cybernetics_v2_procedures_lore.md](cybernetics_v2_procedures_lore.md)). Approved with must-fixes N1–N5, all folded in:
  - N1: proc.004 retitled *A Part Replaced*, with the ordered-part fiction (§3.1, §4.4, §7).
  - N2–N4: residue wording (§7).
  - N5: heir.004 Seamless desc (§3.2, §7).
  - Residue is **approved** with its register constraint. The earlier fallback (drop end.042) is withdrawn.
  - All titles are approved.
  - The back-street Excision physician ruling (§4.7) is **upheld**.
- **Nikios Khanate:** not touched.

---

## 9. Definition of done

0. **Tiger, `px_lsp_diagnostics.js` and `px_vocab_check.py` clean** on the touched files, except the `CLAUDE.md` known-benign list (including the 16 `20_health_effects.txt` errors reached through the wound effects).
1. **Reachability (PX event graph):**
   - proc.001 from the three removal decisions;
   - proc.002 from `eotg_aug_procedure_effect`;
   - proc.003 and proc.004 from `eotg_on_trait_gained_aug_repair`;
   - proc.020 from `eotg_on_yearly_aug_former_check`;
   - end.040–.042 from `eotg_on_yearly_aug_seamless_check`;
   - init.011 additionally from `eotg_aug_procedure_effect`.

   Nothing is fired by nothing.
2. **Cooldown authority:** `grep -n eotg_flag_aug_repair_cooldown` and `eotg_flag_aug_seamless_cooldown` find `add_character_flag` **only** in `common/on_action/eotg_augmentation_on_actions.txt`. No event `trigger` reads either flag, or `eotg_flag_aug_phantom_done`.
3. **One roll:** outcome odds appear only in `eotg_aug_procedure_roll_effect` (and Excision's own effect). `grep -n random_list` in init.011's immediate and tier1.022's immediate returns nothing.
4. **No roll in an `immediate`:** every call to `eotg_aug_procedure_roll_effect`, `_booked_effect` or `eotg_aug_procedure_effect` sits in an option or an `after` block.
5. **Severe tail only in the back streets:** with the provider pinned to clinic, physician or self, none of maimed / one_eyed / blind / death / discovered can be selected (weights 0 before factors). Death weight is 0 for `repair`.
6. **Coupling (QA audit 8):**
   - every paid option of proc.001 and proc.003 changes tier or moves risk;
   - proc.002 and proc.004 are chain stages that move risk or read residue;
   - proc.020 c/d lead into an install;
   - end.040 b/d, end.041 b/c and end.042 move residue, and every G2 desc reads it.
6b. **Stress helpers:**
   - No option in proc.001 calls both the surgery helper and (through `eotg_aug_removal_perform_effect`) the reject helper.
   - No option in this spec writes a `stress_impact` line for impatient, gluttonous, temperate or fickle. Those come only through the G9 rows in the reject and neglect helpers.
7. **Hidden rule:** no new tooltip, toast or desc contains a number or the words "risk", "odds" or "chance". All risk and residue moves are in `hidden_effect`.
8. **No recreated risk:** for a former character, `eotg_fracture_risk` never reappears after proc.002 (Fragments / infection) or proc.020 a/b/e.
9. `grep -rn "eotg_aug_former" common events`: it is set in `eotg_aug_mark_former_effect` and overridden only in `eotg_aug_excision_effect`, init.012 and tier1.015.
10. **Loc:** all §7 keys exist exactly once, with BOM and no `[scope:`. No new string names or characterizes a licensing authority.
11. **Human, in game (temporary map):**
    - Seek → back streets, 20 times with console reloads. You should see init.011 with mixed outcomes and at least one severe or death across the set. Clinic, 20 times: almost all silent.
    - Pursue the Next Stage at Augmented, take g → tier1.022 reveals an outcome. Take f with a learning-16 physician → mostly clean.
    - Remove Implants → proc.001. Back streets until Fragments → proc.002 → Consult the Physician is visible and clears it.
    - An Enhanced ruler, console `add_trait = one_legged` → proc.003 within 30 days. A second injury within 3 years → nothing. Seamless (console Total Integration), `add_trait = blind` → proc.004, and the trait is gone.
    - **Engine check (§4.9):** a wound pushed to rank 3 by `increase_wounds_no_death_effect` does / does not fire `on_trait_gained`. Starting characters with a listed trait do not get proc.003 on day 1.
    - Leave the system; 1–3 years later proc.020 fires once. Zealous vassals show "Reassured".
    - Seamless for 10 years: Ledger / Resignation / Flicker appear. heir.004 with a Seamless owner shows `desc_seamless` and neither `desc_silent` nor `desc_premonition`. After three residue moves, no Flicker fires again. An adult heir with no arc gets heir.004.

---

## 10. Deferred

- **G4–G10** (interactions, Tamper scheme, activities, the edict, Salvage, thin traits, the Implant Technician). Not specced. **Hooks left:**
  - the roll takes `PATIENT`, `SURGEON` and literal `PROVIDER` / `PROCEDURE`;
  - the reveal goes to `$PATIENT$`;
  - `eotg_aug_former` reserves `flag:salvaged` (G8);
  - `eotg_aug_proc_bad_factor` is the place a G10 technician or a G7 licence edict would add a line.
- **Episodes on the operating table for Neurofractured patients** (gaps F3). Cut: it would bypass the band pools' cooldown authority. Revisit only as a band-pool entry.
- **A repair for the unaugmented.** Not needed: The Prosthetic (init.006) already serves them, and now gets a former desc and a ×2 weight.
- **Rolls for installs on other characters** (knights, children, the Bridge, the parent's hardware, patron and heir installs). Cut: their own outcome logic stands, or they are G4 scope.
- **A fourth G2 event (the court that left).** end.011 already plays it at Total Integration. A recurring version would repeat it.
- **wounded_2 repairs.** Cut for rarity (§4.9). A one-line change in the on_action if wanted later.
- **Relapse-aware text** (init.018 or init.006 variants for "you have done this before"). The marker supports it. Not written, to hold loc down.
- **Physician bonus in the back-street Excision.** Off by ruling (§4.7). One param flips it.

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Build docs/specs/cybernetics_v2_procedures.md §3–§5 on top of the uncommitted QA-passed batch and the G9 stress rows (trait_depth §5.2). This includes the lore N5 desc-only change on heir.004 (§3.2). Run the three validators, then hand §7 to eotg-localizer, who uses docs/specs/cybernetics_v2_procedures_lore.md renderings verbatim. Then eotg-qa runs §9.
- files: docs/specs/cybernetics_v2_procedures.md; binding loc renderings in docs/specs/cybernetics_v2_procedures_lore.md
- new events (8): eotg_aug_proc.001 Who Takes It Out? (the three removal decisions); eotg_aug_proc.002 After the Procedure (eotg_aug_procedure_effect); eotg_aug_proc.003 Spare Parts (on_trait_gained → eotg_on_trait_gained_aug_repair); eotg_aug_proc.004 A Part Replaced (same hook, Seamless); eotg_aug_proc.020 Phantom Static (eotg_on_yearly_aug_former_check); eotg_aug_end.040 The Ledger Balances, eotg_aug_end.041 A Resignation, eotg_aug_end.042 A Flicker (eotg_on_yearly_aug_seamless_check). Below the gaps doc's 12–15 estimate.
- needs-loc (~102 new, 4 revised; §7): eotg_aug_proc.001.* (13), eotg_aug_proc.002.* (8), eotg_aug_proc.outcome_* (10), eotg_aug_proc.install_tt, eotg_aug_proc.003.* (17), eotg_aug_proc.004.* (4), eotg_aug_proc.020.* (12), eotg_aug_init.011.desc_maimed/_one_eyed/_blind, eotg_aug_init.006.desc_former, eotg_aug_tier1.002.f/.g, eotg_aug_tier1.022.desc_rejection, eotg_aug_tier2.003.f/.g, eotg_aug_end.001.e, eotg_aug_end.040.* (8), eotg_aug_end.041.* (9), eotg_aug_end.042.* (4), eotg_aug_heir.004.desc_seamless, eotg_mod_aug_fragments(+_desc); revised: eotg_decision_partial_removal_tooltip, eotg_decision_overclock_regression_tooltip, eotg_decision_remove_implants_tooltip, eotg_decision_consult_physician_selection_tt
- needs-lore: none (review done; N1–N5 folded in)
- needs-human: §9 item 11 in-game checks, including the engine check that on_trait_gained fires on a wound rank change (§4.9)
