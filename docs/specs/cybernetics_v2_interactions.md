# Spec: Cybernetics v2 — character interactions (G4), the tampering scheme (G5), prisoner Salvage (G8)

**Author:** eotg-architect, 2026-10-04
**Authorised by:** the human, 2026-10-04 (relayed by the coordinator): G4 (character interactions), G5 (the "sabotage their implants" hostile scheme) and G8 (prisoner Salvage), all from [`docs/qa/cybernetics_content_gaps_v2.md`](../qa/cybernetics_content_gaps_v2.md) Part 2.
**Index:** [cybernetics_v2.md](cybernetics_v2.md). Index §1 rules 1–12 and the §5 lore register (with today's never-name extension) apply to everything here.
**Builds on:** [cybernetics_v2_procedures.md](cybernetics_v2_procedures.md) (committed, in lore review). This spec **uses** its roll (`eotg_aug_procedure_roll_effect` / `eotg_aug_procedure_effect`, params `PATIENT`, `PROVIDER`, `PROCEDURE`, `SURGEON`), its pricing helpers, `eotg_aug_save_surgeon_effect`, `eotg_aug_removal_perform_effect`, `eotg_aug_repair_injury_effect`, proc.002 and proc.020, and the reserved `eotg_aug_former = flag:salvaged`. It does **not** re-spec the roll. §3.2 lists five small additive amendments to the procedures spec's not-yet-built pieces.
**Lore review:** approved 2026-10-04 with must-fixes I1–I7, all folded in below. The verdict and its loc renderings are in [cybernetics_v2_interactions_lore.md](cybernetics_v2_interactions_lore.md), which is **binding** for script and loc (§7, §8).
**Also binding:** [cybernetics_v2_balance.md](cybernetics_v2_balance.md) (HQ1 pacing, HQ2 world targets, §9.2 observer run), [cybernetics_v2_trait_depth.md](cybernetics_v2_trait_depth.md) §5.2 (G9 stress rows), [cybernetics_v2_new_beats.md](cybernetics_v2_new_beats.md) (patron.008 fires after any exit), [`docs/lore/REVIEW_866.md`](../lore/REVIEW_866.md).

**Size.**
- **6 new events** (5 visible, 1 hidden): 2 interaction follow-ups, 4 scheme outcome stages. **Below the ~10 flag; no further yes needed.**
- 5 character interactions, 1 scheme type, 1 custom on_action (scheme ongoing).
- 2 new namespaces, 2 new event files, 2 new script folders (`common/character_interactions/`, `common/schemes/scheme_types/`).
- 5 new opinion modifiers. No new trait, static modifier, decision, story cycle, death reason or icon (icons are vanilla placeholders, §3.1).
- About 145 loc keys (§7).

**Build order.** After the procedures spec is built and QA'd. Everything here calls its effects.

---

## 0. Engine facts this spec rests on (verified; vanilla wins over the `.info`)

All paths under `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`.

| Fact | Evidence |
|---|---|
| A hostile scheme is started by an interaction with `scheme = <type>`, `category = interaction_category_hostile`, four exclusive agent-package `send_option`s, and `begin_scheme_with_agents_effect` in `on_accept` | `common/character_interactions/00_scheme_interactions.txt:251-509` (`start_abduct`); helper `common/scripted_effects/00_scheme_scripted_effects.txt:16270` |
| Scheme completion runs `on_phase_completed` → a prep effect that saves `follow_up_event = event_id:<x>` and fires the shared preparations window `scheme_critical_moments.0002`; the player's "execute" option calls `trigger_event = { saved_event_id = scope:follow_up_event }` | `00_scheme_scripted_effects.txt:11884-11898` (`steal_back_artifact_scheme_prep_effect`); `events/scheme_events/scheme_critical_moments_events.txt:197-220` (`saved_event_id` at :219), :570 (`.0002`) |
| The result event is hidden, rolls `scope:scheme.scheme_success_chance`, and routes to success / failure | `scheme_critical_moments_events.txt:1630-1661` (`.1111`, Steal Back Artifact) |
| An end-of-scheme discovery roll is `100 − scheme_secrecy` | `scheme_critical_moments_events.txt:1394-1407` (`.1071`, Fabricate Claim) |
| Mid-scheme discovery is vanilla's monthly breach system, generic for every hostile scheme (fallback descs exist) | `00_scheme_scripted_effects.txt:57` (`hostile_scheme_monthly_discovery_chance_effect`); `events/scheme_events/hostile_scheme_discovery_events.txt` (`.2001` has `desc = hostile_scheme_discovery.2001.fallback`) |
| Outcome events end the scheme with `scope:scheme = { end_scheme = yes }`, or retry with `reset_failed_scheme_effect` | `events/scheme_events/steal_back_artifact_scheme/steal_back_artifact_outcome_events.txt:64-66`; `events/scheme_events/adbuct_scheme/abduct_outcome_events.txt:491-520`; effect `00_scheme_scripted_effects.txt:665` |
| The 1.20 scheme field set (agents, `phases_per_agent_charge`, `base_maximum_success`, `success_desc`, `discovery_desc`) | `common/schemes/scheme_types/steal_back_artifact_scheme.txt:1-276`, `abduct_scheme.txt:1-338` |
| Vanilla agent types usable here: `agent_physic` (learning, success), `agent_smith` (stewardship/prowess, success), `agent_infiltrator` (speed), `agent_footpad` (speed), `agent_lookout` (secrecy), `agent_decoy` (secrecy) | `common/schemes/agent_types/agent_types.txt:2249, 2376, 3800, 3911, 4857, 5064` |
| An interaction needing acceptance can only be sent to an AI that will accept; the AI evaluates every send-option combination and uses the highest `ai_will_do` | `common/character_interactions/_character_interactions.info:744-745`, `:589` |
| `ai_frequency_by_tier` needs every tier, `0` = never | `_character_interactions.info:552-560` |
| Weak hook: `+50` acceptance (`scope:hook ?= yes`, desc `SCHEME_WEAK_HOOK_USED`); strong hook: `auto_accept` with `custom_description = spending_hook` | `common/scripted_modifiers/00_religion_scripted_modifiers.txt:72-76`; `00_religious_interactions.txt:236-245` |
| A prisoner-maiming interaction: `category = interaction_category_prison`, `is_imprisoned_by`, auto-accept, `ai_recipients = prisoners`, dread by victim rank, `$VERB$_me` / `$VERB$_family_member` opinions, **no scripted tyranny, no kinslayer** | `00_prison_interactions.txt:8150-8344` (`blind_interaction`); `common/scripted_effects/00_interaction_effects.txt:487-554` (dread :530-552), `:92-160` (opinion effect) |
| An opinion that grants a lawful imprisonment reason: `imprisonment_reason = yes` | `common/opinion_modifiers/00_crime_and_prison_opinions.txt:459-465` (`blinded_me`) |
| Kinslayer is script-applied, and vanilla applies it to a victim already dead | `00_secret_effects.txt:433`; `events/diarchy_events/diarchy_events.txt:11370-11383` |
| An interaction that operates on a family member needs the actor's court physician and fires a follow-up event to the actor | `06_ep3_interactions.txt:4461-4464` (`employs_court_position = court_physician_court_position`), `:4613` |
| Every trigger and effect named here exists in character scope (PX `triggers.log` / `effects.log`): `is_knight_of`, `is_courtier_of`, `is_vassal_of`, `is_spouse_of`, `is_close_family_of`, `is_imprisoned_by`, `has_usable_hook`, `has_strong_hook`, `can_start_scheme`, `use_hook`, `start_scheme`, `end_scheme`, `expose_scheme`, `add_dread`, `reverse_add_opinion`, `send_interface_toast`, `death` | PX 0.5.0 `script_docs` |

**The installed `.info` is behind vanilla on schemes.** `common/schemes/scheme_types/_schemes.info:64` names `base_maximum_success_chance`; every 1.20 scheme uses `base_maximum_success` (`abduct_scheme.txt:20`, `steal_back_artifact_scheme.txt:19`). The `.info` also omits `desc`, `success_desc`, `discovery_desc` and `phases_per_agent_charge`. **Vanilla files win** (precedence: vanilla > skill). The skill's copy of `_schemes.info` matches the installed one.

---

## 1. Purpose & gate

The system is rich in events about yourself and has no levers over other people (gaps doc Part 2 headline). This spec adds them:
- **G4.** Three interactions: **Offer Augmentation** (to a spouse, family member, courtier or vassal), **Demand Implant Removal** (from a vassal, courtier, spouse or family member), **Have Them Examined** (your physician looks at someone's hardware).
- **G5.** A hostile scheme, **Tamper with Implants**. Agents get physical access to the target's hardware. Success raises risk by tier, leaves a visible fault, and makes the target's **next procedure roll** worse until it is repaired.
- **G8.** A prisoner interaction, **Salvage Implants**. The prisoner's implants are cut out through the procedure roll, so the prisoner can die or be maimed, and Fragments are likely. Dread, opinion and kinslayer follow vanilla's prisoner-maiming shape. The salvaged hardware can be sold, fitted, or destroyed.

**Gate 3 (Systems), built against the temporary map** (`docs/agent_workflow.md` §5 rule 2; the mod-exclusive-system exception in `CLAUDE.md`). **Not blocked.**
- Map-agnostic: no title, province, character, culture or faith keys. Relations go through scope tests (`is_vassal_of`, `is_courtier_of`, …) only.
- Faith reactions only through `zealous` / `cynical` and piety (index §1 rule 9).

---

## 2. Signature resource

Unchanged: **`eotg_fracture_risk`** (hidden, 0–100; pressure for Neurofractured) plus **tier** (track XP 0/50/100). For a character who leaves, the read-only **`eotg_aug_former`** marker.

| Lever | How it couples |
|---|---|
| Offer Augmentation | Changes the recipient's tier (unaugmented → Augmented) through the procedure roll. |
| Demand Removal, Salvage | Changes tier (→ out of the system) through the roll; marks `eotg_aug_former` (`flag:removed` / `flag:salvaged`). |
| Have Them Examined → int.001 | Desc reads the recipient's band and faults; options move risk (treatment, or a repair roll). |
| Tamper scheme → tamper.004 | Moves the target's risk by tier; sets the fault flag the procedure roll reads. tamper.002/.003 read the target's tier in their descs. |
| Salvage → int.002 | Options change the actor's tier or move risk; desc reads the tier the hardware came from. |

**The procedure roll is the shared mechanic** (the human's G5 ask: "using fracture risk, tier and the procedure roll"):
- Every surgery here (install, removal, repair, salvage) goes through `eotg_aug_procedure_effect` / `_roll_effect`.
- A successful tampering sets `eotg_flag_aug_sabotaged`, which multiplies the target's **next** roll's bad outcomes (×1.5 on `eotg_aug_proc_bad_factor`). That is the extension point the procedures spec reserved (§10 there).

Hidden-risk rule (index §1 rule 3): no tooltip, toast, desc or scheme modifier quantifies risk. The scheme's **success chance** is vanilla UI and is not the signature resource.

---

## 3. Identifier table

All keys carry `eotg_`. No landed titles.

### 3.1 New

| Type | Key | Where | Owner |
|---|---|---|---|
| character interaction | `eotg_aug_offer_augmentation_interaction` | `common/character_interactions/eotg_augmentation_interactions.txt` (**new folder**) | scripter |
| character interaction | `eotg_aug_demand_removal_interaction` | same | scripter |
| character interaction | `eotg_aug_examine_interaction` | same | scripter |
| character interaction | `eotg_aug_start_tamper_interaction` | same | scripter |
| character interaction | `eotg_aug_salvage_interaction` | same | scripter |
| scheme type | `eotg_aug_tamper` | `common/schemes/scheme_types/eotg_augmentation_schemes.txt` (**new folder**) | scripter |
| namespace | `eotg_aug_int` | `events/eotg_augmentation_interactions.txt` (**new file**) | scripter |
| namespace | `eotg_aug_tamper` | `events/eotg_augmentation_tamper.txt` (**new file**) | scripter |
| event | `eotg_aug_int.001` *The Physician's Report* | interactions event file | scripter |
| event | `eotg_aug_int.002` *What Came Out* | interactions event file | scripter |
| event (hidden) | `eotg_aug_tamper.001` (result roll) | tamper event file | scripter |
| event | `eotg_aug_tamper.002` *The Work Is Done* (owner, success) | tamper event file | scripter |
| event | `eotg_aug_tamper.003` *Hands Withdrawn* (owner, failure) | tamper event file | scripter |
| event | `eotg_aug_tamper.004` *A Fault in the Hardware* (target) | tamper event file | scripter |
| custom on_action | `eotg_aug_tamper_ongoing` | `common/on_action/eotg_augmentation_on_actions.txt` | scripter |
| scripted effect | `eotg_aug_offer_install_effect` (param `PROVIDER` = clinic / physician / backstreet) | `common/scripted_effects/eotg_augmentation_effects.txt` | scripter |
| scripted effect | `eotg_aug_demand_removal_effect` (param `PROVIDER`) | effects | scripter |
| scripted effect | `eotg_aug_salvage_effect` (param `PROVIDER` = physician / backstreet) | effects | scripter |
| scripted effect | `eotg_aug_salvage_actor_effect` (stress helper plus vanilla dread tiers) | effects | scripter |
| scripted effect | `eotg_aug_sabotage_apply_effect` (target scope) | effects | scripter |
| scripted effect | `eotg_aug_tamper_prep_effect` (scheme scope) | effects | scripter |
| scripted trigger | `eotg_aug_offer_candidate` | `common/scripted_triggers/eotg_augmentation_triggers.txt` | scripter |
| scripted trigger | `eotg_aug_in_charge_of` (param `ACTOR`: courtier, vassal, spouse or close family of `$ACTOR$`) | triggers | scripter |
| scripted trigger | `eotg_aug_tamper_target` (`eotg_is_augmented_any = yes`, NOT `eotg_total_integration`) | triggers | scripter |
| scripted trigger | `eotg_aug_has_fault` (`eotg_flag_aug_hidden_flaw` OR `eotg_flag_aug_sabotaged`) | triggers | scripter |
| script value | `eotg_aug_salvage_sale_value` (reads `scope:eotg_salvage_tier`) | `common/script_values/eotg_augmentation_values.txt` | scripter |
| opinion modifier | `eotg_opinion_aug_forced_procedure` (−30, decaying, 20 years) | `common/opinion_modifiers/eotg_augmentation_opinions.txt` | scripter |
| opinion modifier | `eotg_opinion_aug_demanded_removal` (−10; applied with `years = 5`) | opinions | scripter |
| opinion modifier | `eotg_opinion_aug_salvaged_me` (−50, decaying, 50 years, `imprisonment_reason = yes`; displayed "Cut Out My Implants") | opinions | scripter |
| opinion modifier | `eotg_opinion_aug_salvaged_family_member` (−20, decaying, 20 years) | opinions | scripter |
| opinion modifier | `eotg_opinion_aug_tampered` (−40, decaying, 30 years, `imprisonment_reason = yes`) | opinions | scripter |
| character flag (timed, 5 years) | `eotg_flag_aug_sabotaged` | `eotg_aug_sabotage_apply_effect`; read by `eotg_aug_proc_bad_factor`; consumed by the roll; removed by a fault repair | scripter |
| character flag (one-shot) | `eotg_flag_aug_proc_salvage` | set by `eotg_aug_salvage_effect` before the roll; consumed by the roll | scripter |
| character variable (timed, 10 years) | `eotg_aug_sabotaged_by` → the scheme owner | `eotg_aug_sabotage_apply_effect`; read by int.001.d | scripter |
| variable value (reserved, now used) | `eotg_aug_former = flag:salvaged` | `eotg_aug_salvage_effect` | scripter |
| variable value (new) | `eotg_aug_repair_injury = flag:fault` | int.001.b, tamper.004 a/b/c | scripter |
| saved scope values | `eotg_proc_fault`, `eotg_proc_salvage`, `eotg_salvage_tier`, `eotg_tamper_signed`, `scheme_successful` / `scheme_discovered` (vanilla names, local); saved scopes `eotg_examined`, `eotg_saboteur`, `owner`, `target`, `scheme` (vanilla names, local) | the effects and events above | scripter |
| interaction send-option flags | `eotg_aug_provider_clinic`, `eotg_aug_provider_physician`, `eotg_aug_provider_backstreet` (Offer, Demand, Salvage) | interactions | scripter |
| icons (placeholders, vanilla files) | interactions: `icon_personal` (Offer), `demand_obedience` (Demand), `learning` (Examine), `icon_scheme_steal_back_artifact` (start Tamper), `blind` (Salvage); scheme `icon_scheme_hostile` | vanilla `gfx/interface/icons/character_interactions/`, `…/scheme_types/` | human (bespoke art later; recorded as art debt) |

**One deliberate exception to "prefix everything":** the Tamper interaction's agent-package flags keep vanilla's names `agent_focus_balance / _success / _speed / _secrecy`. They are scope values local to one interaction (they cannot collide), and keeping them lets the four option labels use vanilla's existing loc. Everything global is prefixed.

**Reused, not new:** `eotg_mod_aug_tampered` (prowess −2, diplomacy −2), `eotg_mod_aug_infection`, `eotg_mod_aug_fragments` (procedures), `eotg_mod_aug_clean_install`, `eotg_mod_implant_calibrated`, `eotg_mod_aug_removal_withdrawal`, `eotg_mod_aug_lesson_learning`, `eotg_opinion_aug_grateful_patient` (+20), `eotg_opinion_aug_reassured` (+15), the nine stress helpers, `eotg_aug_try_start_countdown_effect`, `eotg_aug_restore_loss_effect`, `eotg_aug_initiate_effect`, `eotg_aug_remove_all_effect`. Procedures: `eotg_aug_procedure_effect`, `_roll_effect`, `eotg_aug_save_surgeon_effect`, `eotg_aug_pay_procedure_effect`, `eotg_aug_can_afford_procedure`, `eotg_aug_removal_perform_effect`, `eotg_aug_repair_injury_effect`, `eotg_aug_price_mult_*`. Vanilla: `begin_scheme_with_agents_effect`, `reset_failed_scheme_effect`, `hostile_scheme_monthly_discovery_chance_effect`, `torture_blind_castrate_disfigure_opinion_effect`, `add_kinslayer_trait_or_nothing_effect`, `suppress_scheme_follow_up_event_till_input_given_effect`, `cap_schemes_and_fire_reminders_effect`, `purge_ai_scheme_slots_effect`, `add_scheme_starting_opportunities_intrigue_effect`.

### 3.2 Amendments to the procedures spec (additive; that spec is not built yet, so the scripter builds them together)

| Piece | Amendment | Why |
|---|---|---|
| `eotg_aug_proc_bad_factor` | one more row: patient has `eotg_flag_aug_sabotaged` → ×1.5 | G5's hold on the roll (the reserved extension point, procedures §10) |
| `eotg_aug_procedure_roll_effect` | patient has `eotg_flag_aug_proc_salvage`: **rejection** ×5, **maimed / one_eyed / blind** ×2, **death** ×3. Step 5 (clear one-shots) also removes `eotg_flag_aug_proc_salvage` and `eotg_flag_aug_sabotaged`. | Salvage is unwilling, restrained surgery done for the parts, not the patient. "Fragments likely" (gaps G8). Severe weights stay 0 at physician and clinic before factors, so procedures DoD 5 still holds. |
| `eotg_aug_repair_injury_effect` | new branch `flag:fault` → remove `eotg_flag_aug_hidden_flaw`, `eotg_flag_aug_sabotaged`, `eotg_mod_aug_tampered` (each guarded) | A repair roll can now fix a fault, not only an injury |
| proc.002 desc | two openers placed **before** the kind openers in its `first_valid`: `desc_salvaged` (`exists = scope:eotg_proc_salvage`) and `desc_repair_fault` (`exists = scope:eotg_proc_fault`) | The report reads right for a salvaged prisoner and for a fault repair. `desc_repair` and `outcome_repair_failed` must be written injury-neutral (§7). |
| proc.020 desc | `desc_salvaged` added to the marker `first_valid` (`var:eotg_aug_former ?= flag:salvaged`) | Uses the reserved value |

**Salvage odds** with the amendment (weights per 200, removal):

| Outcome | Back streets (×salvage) | Physician (×salvage; bad factor 1) |
|---|---|---|
| clean | 129 (56%) | 180 (84%) |
| excellent | 6 (3%) | 4 (2%) |
| infection | 20 (9%) | 10 (5%) |
| fragments (rejection) | 60 (26%) | 20 (9%) |
| maimed / one_eyed / blind | 12 (5%) | 0 |
| death | 3 (1.3%) | 0 |

The physician is the safe choice and needs one. The rough way is free and dangerous. A Neurofractured prisoner adds the roll's existing ×1.5 to every bad row (the roll runs **before** the trait is removed, §4.5).

---

## 4. Wiring

### 4.0 Shared rules for all five interactions

- **Scopes.** Use `scope:actor` and `scope:recipient` (the shape of `ask_for_conversion_courtier_interaction`, `00_religious_interactions.txt:158-505`). Puppet actors (`scope:puppet_or_actor`) are not supported. That is deliberate and recorded in §10.
- **The roll runs on a click.** An interaction's `on_accept` is the click (the recipient accepting, or the actor sending on auto-accept). This satisfies procedures §4.1 rule 1. Every roll call sits inside `hidden_effect`, followed by a `custom_tooltip`. No tooltip quantifies odds.
- **Payment.** The actor pays in `on_accept` with `eotg_aug_pay_procedure_effect` inside `scope:actor`. Affordability is checked in `is_valid_showing_failures_only` with `eotg_aug_can_afford_procedure`, per provider flag.
  - **Not** the vanilla `cost = { gold = … }` block. `cost` is charged on send (`_character_interactions.info:484-487`), so a player recipient's refusal would still cost the actor.
  - The procedures spec's helpers keep one price scale.
- **The surgeon.** For `physician`, run `scope:actor = { eotg_aug_save_surgeon_effect = yes }`. In the actor's scope it saves the actor's court physician, or the actor if they are themselves a `lifestyle_physician` (the effect's fallback is "this"). The send option's `is_valid` is `scope:actor = { eotg_has_physician_access = yes }`.
- **Provider send options** (Offer, Demand, Salvage), exclusive (`send_options_exclusive = yes`, `00_scheme_interactions.txt:368`):

```
send_option = { flag = eotg_aug_provider_clinic      localization = eotg_aug_send_clinic      current_description = eotg_aug_send_clinic_tt      starts_enabled = { always = yes } }
send_option = { flag = eotg_aug_provider_physician   localization = eotg_aug_send_physician   current_description = eotg_aug_send_physician_tt
                is_valid = { scope:actor = { eotg_has_physician_access = yes } } }
send_option = { flag = eotg_aug_provider_backstreet  localization = eotg_aug_send_backstreet  current_description = eotg_aug_send_backstreet_tt }
```
  Salvage has no clinic (§4.5) and labels its back-street option `eotg_aug_send_rough`.
- **Hooks** (Offer, Demand). These copy `ask_for_conversion_courtier_interaction`:
  - the send option: `flag = hook`, `localization = SCHEME_HOOK`, `is_valid = { scope:actor = { has_usable_hook = scope:recipient } }` (:362-378);
  - the extra icon (:375-378);
  - a strong hook means `auto_accept` (:236-245);
  - `use_hook` in `on_accept` (:264-280);
  - the AI's "use a hook only if needed" `add = -1` (:404-407);
  - a weak hook adds +50 (`00_religion_scripted_modifiers.txt:72-76`).
  - A hook-forced acceptance gives the recipient `eotg_opinion_aug_forced_procedure` toward the actor. It replaces the willing-acceptance opinion.
- **Opinion in `ai_accept`:** `opinion_modifier = { who = scope:recipient  opinion_target = scope:actor  multiplier = 0.5  desc = AI_OPINION_REASON }` (`00_alliance.txt:626-631`).
- **Every `ai_accept` modifier carries a `desc`.** Keys are in §7 (`EOTG_AUG_AI_*`), and vanilla keys are reused where they exist.
- **Stress:** the actor's stress uses the mod helpers (index §1 rule 6), always inside `scope:actor = { }`. No interaction writes its own `stress_impact` line for impatient, gluttonous, temperate or fickle (trait-depth §5.2).

### 4.1 Offer Augmentation — `eotg_aug_offer_augmentation_interaction`

| Field | Value | Precedent |
|---|---|---|
| `category` / `icon` / `interface_priority` | `interaction_category_friendly` / `icon_personal` / 40 | `00_character_interaction_categories.txt:25` |
| `desc` | `eotg_aug_offer_augmentation_interaction_desc` | |
| `notification_text` | `eotg_aug_offer_augmentation_interaction_notification` | `00_religious_interactions.txt:516` |
| `is_available` | `is_adult = yes`, `is_imprisoned = no`; AI only: `OR = { eotg_is_augmented_any = yes  has_trait = ambitious  has_trait = cynical }`, NOT `zealous` | `.info:570-573`; `00_artifact_interactions.txt:2828-2847` |
| `is_shown` | `scope:recipient != scope:actor`; `scope:recipient = { eotg_aug_in_charge_of = { ACTOR = scope:actor } }`; `scope:recipient = { eotg_is_augmented_any = no  is_imprisoned = no }` | |
| `is_valid_showing_failures_only` | `scope:recipient = { eotg_aug_offer_candidate = yes }`; afford by flag: clinic `minor_gold_value` ×1, physician ×`eotg_aug_price_mult_physician`, back streets `tiny_gold_value` | |
| `cooldown_against_recipient` | `{ years = 5 }` | `00_religious_interactions.txt:213` (15 for conversion) |
| `ai_min_reply_days` / `ai_max_reply_days` | 1 / 5 | :247-248 |
| `auto_accept` | strong-hook `custom_description` only | :236-245 |
| `on_accept` | `eotg_aug_offer_install_effect = { PROVIDER = … }` (an if-ladder on the three flags); hook use; opinion; actor toast `eotg_aug_offer_accepted_toast` | |
| `on_decline` | actor toast `eotg_aug_offer_declined_toast`. **No opinion penalty:** it was a gift. | |

**`eotg_aug_offer_candidate`** (recipient scope):
- `is_adult = yes`, `is_alive = yes`, `eotg_is_augmented_any = no`;
- NOT `eotg_flag_suppress_progression`;
- NOT `has_character_modifier = eotg_mod_aug_excision_recovery`;
- `trigger_if = { limit = { is_landed = yes }  eotg_can_receive_augmented = yes }`. A landed recipient meets the ruler development gate, as every other ruler install does. That keeps HQ2's development gating.

**`eotg_aug_in_charge_of = { ACTOR }`:** `OR = { is_courtier_of = $ACTOR$  is_vassal_of = $ACTOR$  is_spouse_of = $ACTOR$  is_close_family_of = $ACTOR$ }`.

**`eotg_aug_offer_install_effect = { PROVIDER }`** mirrors init.018's three paths with `PATIENT = scope:recipient` (procedures §4.5):
1. Pay (actor): clinic `minor_gold_value`; physician `minor_gold_value` × `eotg_aug_price_mult_physician`; back streets `tiny_gold_value`. The base is `minor_gold_value` because that is the existing price for installing on someone else (init.020 a/b/c). Seek's `medium` is the ruler's own.
2. `scope:recipient = { eotg_aug_initiate_effect = yes }`. If `eotg_has_physical_loss = yes`: `eotg_aug_restore_loss_effect = yes`. The offer doubles as a prosthetic, as in The Prosthetic (init.006).
3. Clinic or physician:
   - `eotg_mod_implant_calibrated` (2 or 3 years);
   - for the physician, `scope:actor = { eotg_aug_save_surgeon_effect = yes }`;
   - `hidden_effect = { eotg_aug_procedure_effect = { PATIENT = scope:recipient  PROVIDER = $PROVIDER$  PROCEDURE = install  SURGEON = scope:eotg_proc_surgeon (physician) / scope:recipient (clinic) } }`;
   - `custom_tooltip = eotg_aug_proc.install_tt`.
4. Back streets:
   - `scope:recipient = { hidden_effect = { set_variable = { name = eotg_fracture_risk  value = 5 } } }`;
   - `hidden_effect = { eotg_aug_procedure_roll_effect = { PATIENT = scope:recipient  PROVIDER = backstreet  PROCEDURE = install  SURGEON = scope:recipient } }`;
   - unless `scope:eotg_proc_outcome = flag:death`, `scope:recipient = { trigger_event = { id = eotg_aug_init.011  days = { 180 540 } } }`.
5. Opinion: willing → `eotg_opinion_aug_grateful_patient`, 10 years (as `eotg_aug_retainer_install_effect`); hook-forced → `eotg_opinion_aug_forced_procedure`.

The reveal goes to the recipient (init.011 or silent), per the procedures routing. init.011's options use the patient's own gold and traits, so they work for a courtier. A recipient who dies on the table dies inside the roll, and the actor sees the vanilla death notice.

**`ai_accept`** (recipient's view):

| Modifier | add | desc key |
|---|---|---|
| base | 0 | |
| `scope:recipient` is a courtier or vassal of the actor | +25 | `EOTG_AUG_AI_LIEGE` |
| opinion ×0.5 | ± | `AI_OPINION_REASON` (vanilla) |
| ambitious / cynical / brave / greedy | +30 / +20 / +10 / +10 | `EOTG_AUG_AI_AMBITIOUS` / `_CYNICAL` / `_BRAVE` / `_GREEDY` |
| `eotg_has_physical_loss = yes` | +40 | `EOTG_AUG_AI_LOSS` |
| craven / content / paranoid / humble | −30 / −20 / −15 / −15 | `EOTG_AUG_AI_CRAVEN` / `_CONTENT` / `_PARANOID` / `_HUMBLE` |
| zealous | −100 | `EOTG_AUG_AI_ZEALOUS` |
| `has_variable = eotg_aug_former` | −20 | `EOTG_AUG_AI_FORMER` |
| provider clinic / physician / back streets | +10 / +5 / −25 | `EOTG_AUG_AI_CLINIC` / `_PHYSICIAN` / `_BACKSTREET` |
| weak hook | +50 | `SCHEME_WEAK_HOOK_USED` (vanilla) |

**AI sending** (HQ2: §4.7):
- `ai_targets`: `spouses`; `vassals` (`max = 10`); `family` (`max = 5`). `ai_target_quick_trigger = { adult = yes }`.
  - **Courtiers and knights are left to the AI's `eotg_decision_augment_retainer`**, which already covers them (balance §5.2). The two levers do not double-dip.
- `ai_frequency_by_tier`: barony 0 / county 0 / duchy 60 / kingdom 36 / empire 36 / hegemony 36.
- `ai_will_do`:
  - base 0;
  - +20 actor `eotg_is_augmented_any`, +10 ambitious, +10 cynical;
  - +25 recipient `eotg_has_physical_loss` (+10 more if the actor is compassionate);
  - +15 recipient is the primary heir;
  - flag back streets −15 (+20 greedy), physician +5;
  - hook `add = -1`;
  - `factor = 0.1` recipient `is_landed = yes` (the HQ2 throttle);
  - `factor = 0` actor `short_term_gold` below the chosen price.

### 4.2 Demand Removal — `eotg_aug_demand_removal_interaction`

| Field | Value | Precedent |
|---|---|---|
| `category` / `icon` | `interaction_category_vassal` / `demand_obedience` | |
| `popup_on_receive` / `pause_on_receive` | yes / yes | `00_religious_interactions.txt:511-512` |
| `is_shown` | `scope:recipient = { has_trait = eotg_cybernetics  eotg_aug_in_charge_of = { ACTOR = scope:actor }  is_imprisoned = no }`. Tiers 1–3 only. **Neurofractured is excluded:** its exit is Excision (`eotg_decision_aug_excision`), deliberately dangerous. **Seamless is excluded** (lore ruling, upheld): at 866 tech no surgeon can find where Seamless hardware ends and the body begins, so there is nothing a removal could take out. | |
| `is_valid_showing_failures_only` | afford by flag: base `medium_gold_value` (the full-removal clinic price, procedures `eotg_aug_removal_base_value`); multipliers 1 / `eotg_aug_price_mult_physician` / `eotg_aug_price_mult_backstreet_removal` | |
| `cooldown_against_recipient` | `{ years = 10 }` | demand_conversion: 15 (:544) |
| `auto_accept` | strong hook | |
| `on_accept` | `eotg_aug_demand_removal_effect = { PROVIDER = … }`; hook use; opinion; actor toast `eotg_aug_demand_accepted_toast` | |
| `on_decline` | recipient `add_opinion = { modifier = eotg_opinion_aug_demanded_removal  target = scope:actor  years = 5 }`; actor toast `eotg_aug_demand_declined_toast` | `00_religious_interactions.txt:667-672` (demanded_my_conversion −10) |

**`eotg_aug_demand_removal_effect = { PROVIDER }`.** Same order as proc.001: pay, perform, roll.
1. `scope:actor = { eotg_aug_pay_procedure_effect = { BASE = medium_gold_value  MULT = … } }`.
2. Physician: `scope:actor = { eotg_aug_save_surgeon_effect = yes }`.
3. `scope:recipient = { set_variable = { name = eotg_aug_removal_kind  value = flag:full  days = 30 }  eotg_aug_removal_perform_effect = yes }`. That is the remove-all, withdrawal for 3 years and the reject stress, **on the recipient**. `eotg_aug_mark_former_effect` sets `flag:removed`.
4. `hidden_effect = { eotg_aug_procedure_effect = { PATIENT = scope:recipient  PROVIDER = $PROVIDER$  PROCEDURE = removal  SURGEON = … } }`; `custom_tooltip = eotg_aug_demand_removal_effect_tt`.
5. `scope:recipient = { remove_variable = eotg_aug_removal_kind }`.
6. Opinion:
   - hook-forced → `eotg_opinion_aug_forced_procedure`;
   - willing and zealous → `eotg_opinion_aug_reassured`, 5 years;
   - otherwise none.
7. Actor stress: a hook-forced demand runs `eotg_aug_stress_tyranny_effect`; a willing one runs none.

**Refusal penalty: opinion only, by decision.** Vanilla makes refusing a demand a **crime** only when a law says so (`refusing_conversion_is_crime_trigger`, `00_religious_interactions.txt:651-666`, `illegal_resisted_conversion_opinion` via `reverse_add_opinion`). Here the equivalent law is G7's Augmentation Edict (ban). Until G7 exists, a refusal costs the refuser −10 opinion toward the actor and nothing more. The `reverse_add_opinion` crime line is G7's hook (§10).

**`ai_accept`** (recipient):

| Modifier | add | desc key |
|---|---|---|
| base | −10 | |
| courtier or vassal of the actor | +50 | `EOTG_AUG_AI_LIEGE` |
| opinion ×0.5 | ± | `AI_OPINION_REASON` |
| tier: Augmented / Enhanced / Overclocked | +10 / −20 / −40 | `EOTG_AUG_AI_TIER_AUGMENTED` / `_ENHANCED` / `_OVERCLOCKED` |
| zealous / content / craven | +30 / +15 / +10 | `EOTG_AUG_AI_ZEALOUS` / `_CONTENT` / `_CRAVEN` |
| ambitious / cynical / stubborn / arrogant | −30 / −20 / −20 / −10 | `EOTG_AUG_AI_AMBITIOUS` / `_CYNICAL` / `_STUBBORN` / `_ARROGANT` |
| `stress_level >= 2` | +20 | `EOTG_AUG_AI_STRESS` |
| `eotg_aug_has_countdown = yes` | +25 | `EOTG_AUG_AI_COUNTDOWN` |
| `eotg_mod_illegal_implants` | +10 | `EOTG_AUG_AI_ILLEGAL` |
| provider clinic / physician / back streets | +10 / +5 / −30 | `EOTG_AUG_AI_CLINIC` / `_PHYSICIAN` / `_BACKSTREET` |
| weak hook | +50 | `SCHEME_WEAK_HOOK_USED` |

The same desc key is used whichever direction the number points. The sign tells the player which way it pushes, so `EOTG_AUG_AI_ZEALOUS` reads "Zealous" in both interactions.

**AI sending:**
- `ai_targets`: `vassals` (`max = 10`), `spouses`, `courtiers` (`chance = 0.25`). Quick trigger `adult = yes`.
- `ai_frequency_by_tier`: 0 / 0 / 60 / 36 / 36 / 36.
- `ai_will_do`:
  - base 0;
  - +25 zealous;
  - +20 recipient `eotg_is_aug_tier3` with the Countdown running;
  - +15 recipient is the spouse or primary heir and tier 3;
  - provider back streets −20, physician +5;
  - hook `add = -1`;
  - `factor = 0` actor `eotg_is_augmented_any`;
  - `factor = 0` actor cynical;
  - `factor = 0` cannot afford.

### 4.3 Have Them Examined — `eotg_aug_examine_interaction`

| Field | Value |
|---|---|
| `category` / `icon` | `interaction_category_friendly` / `learning` |
| `is_available` | `eotg_has_physician_access = yes` (actor-only state belongs in `is_available`, `.info:570-573`) |
| `is_shown` | `scope:recipient != scope:actor`; recipient `eotg_aug_tamper_target = yes` (augmented, not Seamless; lore ruling: at 866 tech no one can tell where Seamless hardware ends and the body begins, so there is no hardware to examine apart from the body); recipient `OR = { eotg_aug_in_charge_of = { ACTOR = scope:actor }  is_imprisoned_by = scope:actor }` |
| `cooldown_against_recipient` | `{ years = 2 }` |
| `auto_accept` | `OR = { scope:recipient = { is_courtier_of = scope:actor }  scope:recipient = { is_imprisoned_by = scope:actor } }`. Your own household and your prisoners do not get a say. |
| `on_accept` | `scope:recipient = { save_scope_as = eotg_examined }`; `scope:actor = { eotg_aug_save_surgeon_effect = yes  trigger_event = { id = eotg_aug_int.001  days = { 3 10 } } }` |
| `on_decline` | actor toast `eotg_aug_examine_declined_toast` |

Precedent: the actor's physician, then an actor follow-up event (`06_ep3_interactions.txt:4461-4464`, `:4613`).

**`ai_accept`** (vassals, spouses and family at other courts):

| Modifier | add | desc key |
|---|---|---|
| base | 25 | |
| opinion ×0.5 | ± | `AI_OPINION_REASON` |
| trusting / paranoid / deceitful | +20 / −40 / −10 | `EOTG_AUG_AI_TRUSTING` / `_PARANOID` / `_DECEITFUL` |
| `stress_level >= 2` | +15 | `EOTG_AUG_AI_STRESS` |
| `eotg_aug_has_countdown = yes` | +20 | `EOTG_AUG_AI_COUNTDOWN` |
| `eotg_mod_illegal_implants` | −20 | `EOTG_AUG_AI_ILLEGAL` |

**AI sending:**
- `ai_targets`: `spouses`, `family` (`max = 5`), `vassals` (`max = 10`).
- `ai_frequency_by_tier`: 0 / 0 / 60 / 36 / 36 / 36.
- `ai_will_do`:
  - base 0;
  - +40 recipient tier 3 or Neurofractured;
  - +20 recipient holds infection, fragments or `eotg_mod_aug_tampered`;
  - +20 recipient `eotg_aug_has_fault`;
  - +10 actor diligent;
  - `factor = 0` when the recipient is tiers 1–2 with none of those.

### 4.4 Tamper with Implants — scheme `eotg_aug_tamper` and `eotg_aug_start_tamper_interaction`

#### 4.4.1 The scheme type

Shape: `steal_back_artifact_scheme.txt` (hostile, character target, agents, a single result), with `abduct_scheme.txt`'s location penalties.

```
eotg_aug_tamper = {
    skill = intrigue
    desc = eotg_aug_tamper_desc_general
    success_desc = "EOTG_AUG_TAMPER_SUCCESS_DESC"
    discovery_desc = "EOTG_AUG_TAMPER_DISCOVERY_DESC"
    icon = icon_scheme_hostile                                         # placeholder
    illustration = "gfx/interface/illustrations/event_scenes/corridor.dds"
    category = hostile
    target_type = character
    is_secret = yes
    maximum_breaches = 5
    cooldown = { years = 10 }                                          # abduct :13, steal_back :12
    speed_per_skill_point = t2_spsp_owner_value                        # abduct :16-21 (tier-2 difficulty)
    speed_per_target_skill_point = t2_spsp_target_value
    base_progress_goal = t2_base_phase_length_value
    maximum_secrecy = 85
    base_maximum_success = t2_base_max_success_value
    phases_per_agent_charge = 1
    success_chance_growth_per_skill_point = t2_scgpsp_value
    allow = { … }          # below
    valid = { … }          # below
    agent_leave_threshold = -25
    agent_join_chance = { base = 0  ai_agent_join_chance_basic_suite_modifier = yes  ai_agent_join_chance_hostile_grievous_modifier = yes }
    agent_groups_owner_perspective = { courtiers guests scripted_relations puppets }
    agent_groups_target_character_perspective = { courtiers vassals }
    valid_agent = { is_valid_agent_standard_trigger = yes }
    odds_prediction = { add = hostile_scheme_base_odds_prediction_target_is_char_value  add = odds_skill_contribution_intrigue_value
                        add = agent_groups_owner_perspective_value  add = agent_groups_target_character_perspective_value  min = 0 }
    base_success_chance = { … }   # below
    base_secrecy = { add = secrecy_base_value  add = countermeasure_apply_secrecy_maluses_value }
    on_start = { … }  on_phase_completed = { … }  on_hud_click = { … }  on_semiyearly = { … }  on_monthly = { … }  on_invalidated = { … }
}
```
The vanilla script values and scripted modifiers named here exist: `common/script_values/00_scheme_values.txt:397-428, 589, 2159, 2602, 2667, 2784, 3170`; `common/scripted_modifiers/00_scheme_scripted_modifiers.txt`.

**`allow`** (copy `steal_back_artifact_scheme.txt:24-69`):
- owner: `is_adult = yes`, `is_imprisoned = no`;
- `scope:target = { is_adult = yes  is_imprisoned = no  eotg_aug_tamper_target = yes }`;
- AI blockers, verbatim in shape:
  - no AI tampering with a target whose opinion of the owner is above 50;
  - not friends unless greedy or deceitful;
  - **anti-spam:** an AI may not start one against a player who already has an `eotg_aug_tamper` scheme targeting them (`steal_back_artifact_scheme.txt:57-66`).

**`valid`** (`abduct_scheme.txt:44-82` shape):
- owner `is_incapable = no`;
- `scope:target = { is_alive = yes  is_imprisoned = no  exists = location  in_diplomatic_range = scope:owner  eotg_aug_tamper_target = yes }`;
- the `no_scheming_allowed_var` block (:75-81).

A target who leaves the system, or reaches Seamless, invalidates the scheme. The Seamless exclusion is upheld by lore: at 866 tech no one can find where Seamless hardware ends and the body begins, so there is no panel to open.

**`base_success_chance`.** Vanilla core first: `scheme_type_skill_success_chance_modifier = { SKILL = INTRIGUE }`, `hostile_scheme_base_chance_modifier = yes`, `apply_calculated_scheme_success_chance_adjustments_modifier = yes` (`abduct_scheme.txt:106-113`). Then:

| Modifier | add | desc | Why |
|---|---|---|---|
| target foreign ruler / foreign subject / ruler in the same realm (`first_valid`) | −40 / −20 / −20 | `sway_foreign_target` / `sway_foreign_target` / `FABRICATE_HOOK_RULER_TARGET` (vanilla) | Half of abduct's (:131-156): you need hands on hardware, not the whole body |
| at war with the target / with their liege (`first_valid`) | −500 / −350 / −250 | `SCHEME_AT_WAR` / `SCHEME_AT_WAR_WITH_LIEGE` (vanilla) | abduct :158-189, verbatim |
| target `eotg_has_physician_access` | −10 | `EOTG_AUG_TAMPER_TARGET_PHYSICIAN` | someone checks the hardware |
| target `eotg_mod_illegal_implants` | +15 | `EOTG_AUG_TAMPER_TARGET_ILLEGAL` | cheap back-street hardware, no security |
| target `eotg_is_aug_tier3` | −10 | `EOTG_AUG_TAMPER_TARGET_HARDENED` | clinic-grade overclock is guarded |
| target `eotg_neurofractured` | +15 | `EOTG_AUG_TAMPER_TARGET_FRACTURED` | unstable, and often restrained or sedated by keepers |
| owner `eotg_is_augmented_any` or `lifestyle_physician` | +10 | `EOTG_AUG_TAMPER_OWNER_KNOWS` | knows the hardware |

**Agents** (vanilla types; `agent_types.txt` lines in §0):

| Package flag | Slots |
|---|---|
| `agent_focus_balance` (also the `on_start` fallback) | `agent_physic`, `agent_smith`, `agent_infiltrator`, `agent_footpad`, `agent_lookout` |
| `agent_focus_success` | `agent_physic`, `agent_physic`, `agent_smith`, `agent_infiltrator`, `agent_lookout` |
| `agent_focus_speed` | `agent_infiltrator`, `agent_infiltrator`, `agent_footpad`, `agent_physic`, `agent_lookout` |
| `agent_focus_secrecy` | `agent_lookout`, `agent_lookout`, `agent_decoy`, `agent_physic`, `agent_infiltrator` |

The physic and the smith are the "hands". Every package has at least one hand.

**On-actions** (copy `steal_back_artifact_scheme.txt:170-275`):
- `on_start`: `set_variable = { name = apply_countermeasures  value = flag:calculating }`; `add_scheme_starting_opportunities_intrigue_effect = yes`; the fallback agent slots when `agents_added` is absent.
- `on_phase_completed`: `suppress_scheme_follow_up_event_till_input_given_effect = yes`, `eotg_aug_tamper_prep_effect = yes`, `cap_schemes_and_fire_reminders_effect = yes`.
- `on_hud_click`: `eotg_aug_tamper_prep_effect = yes`.
- `on_semiyearly`: for AI owners, `eotg_aug_tamper_prep_effect = yes`, then `purge_ai_scheme_slots_effect = yes`.
- `on_monthly`:
  - save `scheme` / `owner` / `target`;
  - `hostile_scheme_monthly_discovery_chance_effect = yes`;
  - unless `scope:discovery_event_happening`, `scheme_owner = { trigger_event = { on_action = eotg_aug_tamper_ongoing  days = { 1 15 } } }`.
- `on_invalidated`: owner toasts `eotg_aug_tamper_invalidated_title` with `eotg_aug_tamper_invalidated_dead` (target died) or `eotg_aug_tamper_invalidated_removed` (target left the system or reached Seamless). Plus vanilla's `scheme_target_not_in_diplomatic_range` text.

**`eotg_aug_tamper_prep_effect`** (shape `00_scheme_scripted_effects.txt:11884-11898`):
```
save_scope_as = scheme
save_scope_value_as = { name = follow_up_event  value = event_id:eotg_aug_tamper.001 }
if = { limit = { NOT = { exists = scope:suppress_next_event } }  scheme_owner = { trigger_event = scheme_critical_moments.0002 } }
```
The shared preparations window (`.0002`) is vanilla's. The mod adds nothing to it.

**`eotg_aug_tamper_ongoing`** (copy `common/on_action/schemes/steal_back_artifact_on_actions.txt:70-87`): `trigger = { is_travelling = no }`; `random_events = { 100 = 0  2 = intrigue_scheme_ongoing.1001  3 = agent_events.9801 }`. Both are vanilla's generic scheme events, which have fallback descs for unknown scheme types (`intrigue_scheme_ongoing_events.txt:16`; `agent_events.txt:5011`). It is a custom on_action fired by the scheme, so no vanilla hook is extended.

#### 4.4.2 The start interaction — `eotg_aug_start_tamper_interaction`

Shape: `start_abduct` (`00_scheme_interactions.txt:251-509`) for the body, `start_stealing_back_artifact` (`00_artifact_interactions.txt:2813-3330`) for the AI.

| Field | Value |
|---|---|
| `icon` / `category` / `interface_priority` / `send_name` | `icon_scheme_steal_back_artifact` / `interaction_category_hostile` / 70 / `START_SCHEME` |
| `scheme` / `ignores_pending_interaction_block` | `eotg_aug_tamper` / yes |
| `is_available` (AI only) | `intrigue >= low_skill_rating`; no running `murder`, `abduct` or `eotg_aug_tamper` scheme; `is_imprisoned = no` (`00_artifact_interactions.txt:2828-2847`) |
| `is_shown` | `scope:recipient != scope:actor`; NOT `scope:recipient = { is_imprisoned_by = scope:actor }`; `scope:recipient = { eotg_aug_tamper_target = yes }`. The multiplayer murder game rules block (`00_scheme_interactions.txt:293-319`) is copied too: tampering is a hostile scheme against a player. |
| `is_valid_showing_failures_only` | `can_start_scheme = { type = eotg_aug_tamper  target_character = scope:recipient }`; `scope:recipient = { NOT = { has_strong_hook = scope:actor } }` (:322-350) |
| `desc` | `triggered_desc` → `eotg_aug_start_tamper_approved_tt` when `can_start_scheme` (:352-364) |
| send options | `options_heading = schemes.t.agent_packages` (vanilla); four exclusive packages, `current_description = eotg_aug_start_tamper.tt.agent_focus_*` (:366-389) |
| `on_accept` | `scope:actor = { eotg_aug_stress_wound_effect = yes }` (stress on start, as vanilla abduct :405-415 and steal_back :3033-3040); a toast `eotg_aug_start_tamper_notification` that runs `begin_scheme_with_agents_effect = { SCHEME_TYPE = eotg_aug_tamper  TARGET_TYPE = target_character  TARGET_SCOPE = scope:recipient  AGENT_1..5 = … }` per package (:416-490) |
| `auto_accept` | yes |

**AI** (copy `00_artifact_interactions.txt:3237-3330`):
- `ai_target_quick_trigger = { adult = yes }`.
- `ai_targets`: `scripted_relations`; `liege`; `neighboring_rulers` + `peer_vassals` (`max = 10`); `family` (`max = 10`); `vassals` (`max = 10`).
- `ai_frequency_by_tier`: barony 0 / county 144 / duchy 72 / kingdom 36 / empire 36 / hegemony 36.
- `ai_will_do`:
  - base −30;
  - `ai_boldness` ×−1; `ai_vengefulness` if > 0; `ai_compassion` ×−0.25;
  - rival +60, nemesis +150;
  - **added:** +15 cynical; +10 zealous (hates the machine); +20 the actor is augmented and the recipient is at a higher tier (envy: tier 3 or NF over the actor's tier 1–2);
  - `factor = 0` when the actor's opinion of the recipient is ≥ `medium_positive_opinion` (unless `ai_greed` is high), and for friends or lovers (:3312-3330).

#### 4.4.3 Outcome flow

```
scheme_critical_moments.0002 (vanilla) --execute--> eotg_aug_tamper.001 (hidden)
   success --> owner: tamper.002 (1 day) --option--> target: tamper.004 (3-14 days)
   failure --> owner: tamper.003 (1 day);  if discovered: target gets the opinion + a toast
```

**tamper.001 (hidden).** Shape `scheme_critical_moments.1111` (:1630-1661) plus the discovery roll of `.1071` (:1394-1407).
- `immediate`:
  - `scope:scheme = { scheme_owner = { save_scope_as = owner }  scheme_target_character = { save_scope_as = target } }`;
  - success roll `random = { chance = scope:scheme.scheme_success_chance  save_scope_value_as = { name = scheme_successful  value = yes } }`;
  - discovery roll `random = { chance = { value = 100  subtract = scope:scheme.scheme_secrecy }  save_scope_value_as = { name = scheme_discovered  value = yes } }`.
- Success: `scope:owner = { trigger_event = { id = eotg_aug_tamper.002  days = 1 } }`. Also `mandala_trickster_increment_successful_schemes_effect = yes`, as vanilla (:1648).
- Failure: `scope:owner = { trigger_event = { id = eotg_aug_tamper.003  days = 1 } }`. If `scheme_discovered`: `scope:target = { add_opinion = { modifier = eotg_opinion_aug_tampered  target = scope:owner } }` and a toast to the target, `eotg_aug_tamper_foiled_toast` (`left_icon = scope:owner`).

**tamper.002 *The Work Is Done*** (owner; `window = scheme_successful_event`, widget `event_window_widget_scheme`, theme `generic_intrigue_scheme`; `steal_back_artifact_outcome_events.txt:11-33`).
- Desc: base (agents had the hardware in their hands for a night), plus a target-tier line (`desc_tier1` / `_tier2` / `_tier3` / `_fractured`: what the hands could reach), plus `desc_discovered` when `scheme_discovered`.
- Portraits: left owner, lower right target.
- Options (outcome stage, S12: two):

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "Quietly done." | — | `scope:scheme = { end_scheme = yes }`; `scope:target = { trigger_event = { id = eotg_aug_tamper.004  days = { 3 14 } } }` | 50; +20 deceitful; +10 patient |
| b [sadistic] | "Let them know whose hands." | `has_trait = sadistic`; `trait = sadistic` | `save_scope_value_as = { name = eotg_tamper_signed  value = yes }`; `add_dread = minor_dread_gain`; `eotg_aug_stress_cruelty_effect = yes`; end the scheme; fire .004 as in a | 30; +40 sadistic; +10 arrogant |

  .004 is fired from the option, not from .001, so b can sign the deed (saved scopes are captured when `trigger_event` runs). `scope:scheme` has ended by the time .004 fires, so .004 reads only `owner`, `target`, `scheme_discovered` and `eotg_tamper_signed`.

**tamper.003 *Hands Withdrawn*** (owner; `window = scheme_failed_event`; abduct 4001's two options, `abduct_outcome_events.txt:491-520`).
- Desc: base, plus `desc_tier3` when the target is tier 3 or NF (the hardware was watched), plus `desc_discovered`.

| Opt | Text intent | Effect | ai_chance |
|---|---|---|---|
| a | "Let it go." | `scope:scheme = { end_scheme = yes }`; `stress_impact = { stubborn = medium_stress_impact_gain }` (vanilla :496-498) | 50; +20 craven; +10 content |
| b | "Again." | `custom_tooltip = restart_scheme_tt` (vanilla); `scope:scheme = { reset_failed_scheme_effect = yes }` | 10; +200 stubborn (vanilla :513-518); +20 vengeful |

**tamper.004 *A Fault in the Hardware*** (target; retitled by lore I1, because the old title implied a presence inside the hardware). This is the reveal: the consequences land here (procedures §4.1 rule 2).
- **Trigger:** `is_alive = yes`, `eotg_aug_tamper_target = yes`. A target who has left since gets nothing: there is no hardware to fail.
- **Immediate:** `eotg_aug_save_surgeon_effect = yes`; `eotg_aug_sabotage_apply_effect = yes`; if `OR = { exists = scope:scheme_discovered  exists = scope:eotg_tamper_signed }`, `add_opinion = { modifier = eotg_opinion_aug_tampered  target = scope:owner }`.
- **Desc:**
  - base: the hardware misbehaves. Bodily and hardware symptoms only (lore I2): the overlay stutters, a sensor drifts, a limb **responds** late. Never a forecast, and never "answers";
  - a tier line (`desc_aug` / `_enh` / `_oc` / `_nf`);
  - `desc_known` (names `[owner.GetName]`) when discovered or signed, else `desc_unknown` (someone had their hands on it).
- **Portraits:** left root (`paranoia`); right owner when known.

**`eotg_aug_sabotage_apply_effect`** (target scope; `scope:owner` saved):
```
hidden_effect = {
    if tier 1: eotg_add_fracture_risk = { AMOUNT = 8 }      # tier2.016's tampering is +10; scaled by tier
    else_if tier 2: 12   else_if tier 3: 16   else_if eotg_neurofractured: 20 (pressure)
    set_variable = { name = eotg_aug_sabotaged_by  value = scope:owner  years = 10 }
    if = { limit = { eotg_is_aug_tier3 = yes  OR = { var:eotg_fracture_risk >= 50  AND = { var:eotg_fracture_risk >= 40  has_character_flag = eotg_flag_aug_hidden_flaw } } }
           eotg_aug_try_start_countdown_effect = yes }      # same threshold as the OC check's start; patron betrayal precedent
}
add_character_modifier = { modifier = eotg_mod_aug_tampered  years = 2 }
random = { chance = 50  add_character_modifier = { modifier = eotg_mod_aug_infection  years = 1 } }
add_character_flag = { flag = eotg_flag_aug_sabotaged  years = 5 }
```
No episode is fired. Episodes belong to the band pools' cooldown authority (lesson 5; procedures §4.4 made the same call for the operating table).

**Options** (Spare Parts shape, procedures proc.003). Every paid option:
1. pays at base `medium_gold_value`;
2. sets `set_variable = { name = eotg_aug_repair_injury  value = flag:fault  days = 365 }` and `save_scope_value_as = { name = eotg_proc_fault  value = yes }`;
3. runs `hidden_effect = { eotg_aug_procedure_effect = { PATIENT = root  PROVIDER = …  PROCEDURE = repair  SURGEON = … } }`;
4. ends with `custom_tooltip = eotg_aug_tamper.004.tt`.

A fault repair adds the repair risk (+2 to +8 by tier, back streets +3), and the sabotaged flag it is clearing makes **this** roll ×1.5 bad. Fixing sabotaged hardware is harder than fixing it clean. A clean, excellent, infection, flaw or discovered outcome runs `eotg_aug_repair_injury_effect` (`flag:fault`) and clears the fault. Rejection ("failed") leaves it and adds risk +5.

| Opt | Text intent | Trigger | Provider / price | Extra | ai_chance |
|---|---|---|---|---|---|
| a | "The clinic." | NOT `eotg_neurofractured`; afford ×1 | clinic | — | 40; +20 diligent; +10 craven; −20 greedy |
| b | "My own physician." | `eotg_has_physician_access`; afford × `eotg_aug_price_mult_physician` | physician, `SURGEON = scope:eotg_proc_surgeon` | — | 40; +20 trusting; +10 diligent |
| c | "Someone cheaper." | afford × `eotg_aug_price_mult_backstreet_repair` | backstreet | — | 25; +20 greedy; +10 deceitful; −20 craven |
| d | "Live with it." | — | — | `eotg_aug_stress_neglect_effect = yes`. The fault stays (2-year modifier, 5-year flag). | 20; +20 lazy; +10 stubborn |
| e [paranoid] | "Find the hands." (physical evidence only, lore I5; §7) | `has_trait = paranoid`; NOT known (no `scheme_discovered`, no `eotg_tamper_signed`); `scope:owner ?= { is_alive = yes }` | — | intrigue `duel` vs `scope:owner` (tier2.015.a shape, `compare_modifier` ×2.5); success: `add_opinion = { modifier = eotg_opinion_aug_tampered  target = scope:owner }`, toast `.e.success`; failure: toast `.e.failure` | 30; +30 paranoid; +10 vengeful |

**Coupling:** the immediate moves risk; a/b/c move risk inside the roll; the desc reads the tier.

**Discovery summary** (what the target learns, and how):

| Path | Who learns | Mechanism |
|---|---|---|
| Monthly breaches during the scheme | the target's spymaster, then the target | vanilla `hostile_scheme_discovery.*` (generic) |
| Execution roll (`100 − secrecy`), success | the target, at tamper.004 | `eotg_opinion_aug_tampered` toward the owner, with `imprisonment_reason = yes`: a lawful arrest, the vanilla way (`blinded_me` shape) |
| Execution roll, failure | the target | the same opinion plus a toast |
| Owner signs it (tamper.002.b) | the target | the same opinion, and the desc names the owner |
| Target's paranoid trace (tamper.004.e), or an examination (int.001.d) | the target, or the examining liege | intrigue duel; the same opinion |

No court, tribunal or authority above the realm is involved (lore). The crime is answered by the victim's own power to imprison.

### 4.5 Salvage — `eotg_aug_salvage_interaction`

Shape: `blind_interaction` (`00_prison_interactions.txt:8150-8344`).

| Field | Value |
|---|---|
| `category` / `icon` / `interface_priority` | `interaction_category_prison` / `blind` / 30 |
| `desc` | `eotg_aug_salvage_interaction_desc` |
| `is_shown` | `scope:actor = { is_adult = yes }`; `scope:recipient = { is_imprisoned_by = scope:actor  eotg_aug_tamper_target = yes }`. **Seamless is excluded** for now (option A, lore's recommendation). **Open human decision** (§8 ruling 2): A, exclude; or B, allow it with death on the table forced. Build A. B would be a later change to `is_shown` and `eotg_aug_salvage_effect`. |
| `is_valid_showing_failures_only` | recipient NOT `is_being_tortured`, NOT `is_currently_being_purged` (vanilla `custom_description` keys `currently_being_tortured`, `is_currently_being_purged_tt`; :8175-8194) |
| `is_highlighted` | actor sadistic, or rival of the recipient (:8196-8213, minus the cultural lines) |
| send options | physician (needs access, `localization = eotg_aug_send_physician`) / rough (`flag = eotg_aug_provider_backstreet`, `localization = eotg_aug_send_rough`, `starts_enabled`) |
| `on_accept` | see below |
| `auto_accept` | yes |

**`on_accept`:**
1. `eotg_aug_salvage_actor_effect = yes`:
   - `scope:actor = { eotg_aug_stress_wound_effect = yes }`;
   - dread tiers copied from `00_interaction_effects.txt:530-552`: spouse, close family or kingdom+ → `major_dread_gain`; duke or count → `medium_dread_gain`; else `minor_dread_gain`.
2. `torture_blind_castrate_disfigure_opinion_effect = { VERB = eotg_opinion_aug_salvaged }` (vanilla `00_interaction_effects.txt:92-160`). It builds `eotg_opinion_aug_salvaged_me` on the prisoner and `eotg_opinion_aug_salvaged_family_member` on their spouse and close family, exactly as blinding does.
3. `eotg_aug_salvage_effect = { PROVIDER = physician | backstreet }`.
4. `scope:actor = { trigger_event = { id = eotg_aug_int.002  days = { 7 14 } } }`.

**`eotg_aug_salvage_effect = { PROVIDER }`.** The roll comes **first**, so a death on the table ends it with the trait still on the corpse, and the Neurofractured ×1.5 applies.
```
scope:recipient = {
    save_scope_value_as = { name = eotg_salvage_tier  value = flag:augmented|enhanced|overclocked|fractured }   # if-ladder on the tier triggers
    save_scope_value_as = { name = eotg_proc_salvage  value = yes }
    add_character_flag = eotg_flag_aug_proc_salvage
}
(physician) scope:actor = { eotg_aug_save_surgeon_effect = yes }
hidden_effect = { eotg_aug_procedure_effect = { PATIENT = scope:recipient  PROVIDER = $PROVIDER$  PROCEDURE = removal
                                               SURGEON = scope:eotg_proc_surgeon (physician) / scope:recipient (backstreet) } }
custom_tooltip = eotg_aug_salvage_effect_tt
if = { limit = { NOT = { scope:eotg_proc_outcome = flag:death } }
    scope:recipient = {
        eotg_aug_remove_all_effect = yes                                          # marks flag:removed ...
        set_variable = { name = eotg_aug_former  value = flag:salvaged }          # ... overridden (procedures §4.10 rule)
        add_character_modifier = { modifier = eotg_mod_aug_removal_withdrawal  years = 3 }
        add_stress = major_stress_gain                                            # vanilla value; 06_ep3_interactions.txt:4585
    }
}
else = {
    scope:actor = { add_kinslayer_trait_or_nothing_effect = { VICTIM = scope:recipient }  eotg_aug_stress_murder_effect = yes }
}
```

**Fallout, ruled:**
- **Dread:** vanilla's maiming tiers.
- **Opinion:** vanilla's maiming shape. The prisoner's opinion carries `imprisonment_reason = yes`, as `blinded_me` does.
- **Kinslayer: only on a death.** Blinding or castrating kin adds none in vanilla. A death on the table is the actor's act on a prisoner they chose to cut open, so it is treated as an execution. `add_kinslayer_trait_or_nothing_effect` decides family and dynasty itself (`00_secret_effects.txt:433`), and vanilla calls it on a victim already dead (`diarchy_events.txt:11370-11383`). This applies balance §10's M4 policy: deliberate acts take kinslayer.
- **Tyranny: none scripted.** Vanilla's prisoner maiming scripts none (`00_prison_interactions.txt:7827-7925`, `:8215-8288`). The prisoner is already held. Round 2 M5 concerns imprisoning, which does not happen here.
- **Fragments:** about 26% on the rough path, 9% with a physician (§3.2). They are applied at the prisoner's proc.002 reveal.
- **The prisoner stays imprisoned.** Unlike blinding, there is no release (`:8225-8230`). Salvage is not a punishment that ends custody.
- The new_beats patron.008 and Phantom Static fire later for a salvaged playable character, as for any exit. That is intended.

**AI** (`blind_interaction` :8290-8343):
- `ai_targets = { ai_recipients = prisoners }`.
- `ai_frequency_by_tier`: barony 0 / county 144 / duchy 48 / kingdom 36 / empire 12 / hegemony 12.
- `ai_will_do`:
  - base −20;
  - +20 sadistic, +20 greedy, +15 cynical, +10 zealous (rip it out);
  - `ai_compassion = tiny_chance_impact_negative_ai_value` (vanilla);
  - opinion ×−0.25;
  - +20 recipient tier 3 or NF (the valuable hardware);
  - +15 the actor is augmented, or `eotg_can_receive_augmented`;
  - physician flag +10 when the actor is compassionate;
  - `factor = 0.25` recipient close family.

### 4.6 The two interaction events

All `character_event`, in `events/eotg_augmentation_interactions.txt`, namespace `eotg_aug_int`. Index §1 rule 6 applies: three universal options plus 1–2 trait-gated ones, every `ai_chance` with ≥ 2 trait modifiers, morally loaded options using a stress helper.

#### int.001 *The Physician's Report*
- **Fired by:** `eotg_aug_examine_interaction` `on_accept`, 3–10 days.
- **Trigger:** `scope:eotg_examined ?= { is_alive = yes  eotg_aug_tamper_target = yes }`.
- **Portraits:** left root; right `scope:eotg_examined`; lower left `scope:eotg_proc_surgeon` when they are not root.
- **Desc:**
  - base;
  - a `first_valid` on the examined: `desc_fractured` (NF), `desc_oc_bad` (tier 3 and `eotg_aug_pressure_flicker = no`, i.e. risk ≥ 30), `desc_oc_ok` (tier 3), fallback `desc_stable`;
  - appended when true: `desc_flaw` (hidden flaw), `desc_tampered` (`eotg_flag_aug_sabotaged`), `desc_infection` (infection or fragments), `desc_illegal` (`eotg_mod_illegal_implants`).
  - **Prose only, no numbers** (hidden rule).

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "Treat what you can." | examined holds infection, fragments or `eotg_mod_aug_tampered`, OR is tier 3 / NF; `gold >= minor_gold_value` | pay `minor_gold_value`; on the examined: remove infection, fragments and tampered (guarded); hidden risk −5 if tier 3 or NF; `eotg_opinion_aug_grateful_patient` 10 years | 40; +20 diligent; +20 compassionate |
| b | "Fix the fault." | examined `eotg_aug_has_fault = yes`; afford `medium_gold_value` × `eotg_aug_price_mult_physician` | pay; on the examined `eotg_aug_repair_injury = flag:fault` (365 days); `save_scope_value_as eotg_proc_fault`; `hidden_effect = { eotg_aug_procedure_effect = { PATIENT = scope:eotg_examined  PROVIDER = physician  PROCEDURE = repair  SURGEON = scope:eotg_proc_surgeon } }`; `custom_tooltip = eotg_aug_int.001.b.tt` | 30; +20 diligent; +10 paranoid; −20 greedy |
| c | "Note it." | — | `eotg_aug_stress_neglect_effect = yes` | 20; +20 lazy; +10 content |
| d | "Trace the tampering." (physical evidence only, lore I5; §7) | `scope:eotg_examined.var:eotg_aug_sabotaged_by ?= { is_alive = yes }` (save as `eotg_saboteur` in the immediate) | intrigue `duel` vs `scope:eotg_saboteur` (×2.5); success: the examined **and** root `add_opinion = { modifier = eotg_opinion_aug_tampered  target = scope:eotg_saboteur }`, toast `.d.success`; failure: toast `.d.failure` | 30; +20 paranoid; +10 vengeful |
| e [lifestyle_physician] | "Let me do it myself." | `has_trait = lifestyle_physician`, NOT blind; the same state trigger as a | as a, but free, plus `eotg_mod_aug_lesson_learning` 5 years | 30; +30 lifestyle_physician; +10 diligent |

**Coupling:** the desc reads the band; a and e move risk at tier 3 / NF; b moves risk through the roll.

#### int.002 *What Came Out*
- **Fired by:** `eotg_aug_salvage_interaction` `on_accept`, 7–14 days. Saved: `recipient`, `eotg_salvage_tier`, `eotg_proc_outcome`, `eotg_proc_salvage`.
- **Trigger:** `is_alive = yes`.
- **Portraits:** left root; right `scope:recipient` (`override_imprisonment_visuals = yes` if alive, as `prison_events.txt:618-622`).
- **Desc:**
  - base;
  - a tier line from `scope:eotg_salvage_tier` (`desc_augmented` / `_enhanced` / `_overclocked` / `_fractured`);
  - an outcome line (`first_valid`): `desc_died` (death), `desc_maimed` (maimed, one_eyed or blind), `desc_fragments` (rejection), fallback none.

| Opt | Text intent | Trigger | Effect | ai_chance |
|---|---|---|---|---|
| a | "Sell it." | — | `add_gold = eotg_aug_salvage_sale_value` | 30; +20 greedy; +10 cynical |
| b | "Fit it to me." | `eotg_can_receive_augmented = yes`; `gold >= tiny_gold_value` | pay `tiny_gold_value`; `eotg_aug_initiate_effect = yes`; hidden risk set to 5; 50% `eotg_flag_aug_hidden_flaw` (used hardware; thread T6). With physician access: `eotg_aug_save_surgeon_effect`, then `eotg_aug_procedure_effect` (physician, install), `custom_tooltip = eotg_aug_proc.install_tt`. Without: `eotg_aug_procedure_roll_effect` (backstreet, install), then init.011 in 180–540 days unless death. Then `eotg_aug_stress_surgery_effect = yes`. **Tier 1 only**, whatever the hardware came from (HQ1: no skipping tiers). | 30; +20 ambitious; +10 cynical; `factor = 0` zealous |
| c | "Keep it for spare parts." | `has_trait = eotg_cybernetics` | `eotg_mod_aug_clean_install` 5 years; hidden risk +3; 25% `eotg_flag_aug_hidden_flaw` | 30; +20 diligent; +10 greedy |
| d | "Destroy it." | — | `add_piety = minor_piety_gain`; `eotg_aug_stress_reject_effect = yes` | 20; +30 zealous; +10 humble |
| e [cynical] | "Take it apart. Learn." | `has_trait = cynical` | `eotg_mod_aug_lesson_learning` 5 years; if augmented, hidden risk +2 | 30; +30 cynical; +10 education_learning_3 |

**`eotg_aug_salvage_sale_value`** (actor scope): `flag:augmented` → `minor_gold_value`; `flag:enhanced` → `medium_gold_value`; `flag:overclocked` / `flag:fractured` → `medium_gold_value` × 1.5. The buyer is never named (§8).

**Coupling:** b changes tier; c and e move risk; the desc reads the tier the hardware came from.

### 4.7 AI against the HQ2 world targets

HQ2 (balance §0): at game year 30, **25–40%** of AI count-tier-and-above rulers are augmented; of those, **≥ 15%** are Overclocked, Neurofractured or Seamless; **≥ 1 terminal outcome per 10 Neurofractured rulers per decade**.

| Lever | Pushes | Design guard | Expected effect at year 30 (first guess; the observer run decides) |
|---|---|---|---|
| Offer (AI) | augmented share **up** | counts never send; landed recipients ×0.1; landed recipients must pass the ruler development gate; courtiers and knights are left to the retainer decision; actor must be augmented, ambitious or cynical | ≤ +2 points. Estimate: one duke+ check every 3–5 years × about 5% will-do on a landed target × about 40% acceptance ≈ 1 landed conversion per 20–30 duke+ ruler-decades. |
| Demand Removal (AI) | augmented share **down** | zealous, unaugmented, non-cynical lieges only; targets tier 1 most easily | ≈ −1 to −2 points. It roughly cancels Offer, which is the intent: the world splits by temperament. |
| Examine (AI) | slower cascades | duke+; only for tier 3 / NF kin and spouses, or real faults | Small. It trims the cascade rate among the AI's own family. It is offset by Tamper. |
| Tamper (AI) | **top band up** (risk +8 to +20, Countdown starts) | rival-gated (vanilla steal-back weights); anti-spam versus players; Seamless excluded | Supports "≥ 15% at the top" and the terminal rate. It is rare, because rivals are rare. |
| Salvage (AI) | augmented share slightly **down** | prisoners only; vanilla blinding frequencies | ≈ −0.5 point (augmented rulers taken in war). |

**Tuning rule (balance §9.2):** change only `ai_will_do` numbers, the `factor` throttles and the frequencies. Do not change content. **The observer run gains five counters** (§9 item 10).

---

## 5. File placement

| Path | What |
|---|---|
| `common/character_interactions/eotg_augmentation_interactions.txt` | **new folder and file**: the five interactions |
| `common/schemes/scheme_types/eotg_augmentation_schemes.txt` | **new folder and file**: `eotg_aug_tamper`. Vanilla `agent_types` and `pulse_actions` are used, not extended. |
| `events/eotg_augmentation_interactions.txt` | **new**: namespace `eotg_aug_int`; int.001, int.002. Header in the style of the siblings (fires-from map, resource line). UTF-8 with BOM. |
| `events/eotg_augmentation_tamper.txt` | **new**: namespace `eotg_aug_tamper`; .001–.004 |
| `common/scripted_effects/eotg_augmentation_effects.txt` | §3.1 effects; the §3.2 roll and repair amendments |
| `common/scripted_triggers/eotg_augmentation_triggers.txt` | §3.1 triggers |
| `common/script_values/eotg_augmentation_values.txt` | `eotg_aug_salvage_sale_value`; the bad-factor row (§3.2) |
| `common/opinion_modifiers/eotg_augmentation_opinions.txt` | the five opinions |
| `common/on_action/eotg_augmentation_on_actions.txt` | `eotg_aug_tamper_ongoing` (custom; no vanilla hook touched) |
| `events/eotg_augmentation_procedures.txt` | proc.002 and proc.020 desc lines (§3.2) |
| `localization/english/eotg_augmentation_l_english.yml` | §7 |

**No `replace_path`. No vanilla file overridden.** The orchestrator adds `common/character_interactions/` and `common/schemes/scheme_types/` to the `CLAUDE.md` placement table (both exist in the v1 tree, so it is the same layout).

---

## 6. Vanilla precedent (consolidated)

| Mechanism | File:line | Used for |
|---|---|---|
| Courtier interaction with `ai_accept`, hook send option, strong-hook auto-accept, `cooldown_against_recipient`, reply days, AI hook economy | `common/character_interactions/00_religious_interactions.txt:158-505` | Offer, Demand, Examine |
| Demand with popup, pause, and a −10 decline opinion; refusal as crime only under law | `00_religious_interactions.txt:508-778` (:511-512, :651-672) | Demand |
| Opinion and weak-hook acceptance modifiers | `common/scripted_modifiers/00_religion_scripted_modifiers.txt:26-41, 72-76`; `00_alliance.txt:626-631` | all `ai_accept` |
| Physician-gated operation on kin, with an actor follow-up | `06_ep3_interactions.txt:4400-4660` (:4461-4464, :4613) | Examine, Offer (physician) |
| Hostile scheme start with agent packages | `00_scheme_interactions.txt:251-509` | Tamper start |
| Hostile scheme AI (targets, frequency, personality, rival weights, friendly zero) | `00_artifact_interactions.txt:2828-2847, 3237-3330` | Tamper AI |
| Scheme type (hostile, character target, single result) | `common/schemes/scheme_types/steal_back_artifact_scheme.txt:1-276` | `eotg_aug_tamper` |
| Location and war penalties | `abduct_scheme.txt:131-189` | Tamper success chance |
| Prep → preparations window → saved follow-up event | `00_scheme_scripted_effects.txt:11884-11898`; `scheme_critical_moments_events.txt:197-220, 570` | Tamper prep |
| Hidden success roll / discovery roll | `scheme_critical_moments_events.txt:1630-1661`, `:1394-1407` | tamper.001 |
| Success / failure outcome windows; abandon or retry | `steal_back_artifact_outcome_events.txt:11-149`; `abduct_outcome_events.txt:440-520` | tamper.002/.003 |
| Ongoing events via a custom on_action | `common/on_action/schemes/steal_back_artifact_on_actions.txt:70-87` | `eotg_aug_tamper_ongoing` |
| Monthly discovery and breaches | `00_scheme_scripted_effects.txt:57-230`; `events/scheme_events/hostile_scheme_discovery_events.txt` | Tamper discovery |
| Prisoner maiming (shown, valid, accept, AI, frequency) | `00_prison_interactions.txt:8150-8344` | Salvage |
| Maiming dread tiers; `$VERB$` opinion builder | `common/scripted_effects/00_interaction_effects.txt:530-552, 92-160` | Salvage |
| Maiming opinions with `imprisonment_reason` | `common/opinion_modifiers/00_crime_and_prison_opinions.txt:453-465` | `eotg_opinion_aug_salvaged_*`, `eotg_opinion_aug_tampered` |
| Kinslayer after death | `00_secret_effects.txt:433`; `events/diarchy_events/diarchy_events.txt:11370-11383` | Salvage death |
| Victim stress on forced surgery | `06_ep3_interactions.txt:4585` (`add_stress = major_stress_gain`) | Salvage |
| Interaction categories | `common/character_interaction_categories/00_character_interaction_categories.txt:25, 46, 53, 74` | all |

**Deviations, with reasons:**
- **Payment is in `on_accept`, not `cost`** (§4.0): one price scale with the procedures spec, and no charge on a player's refusal.
- **No house-relation damage** on Salvage. Vanilla blinding calls `change_house_relation_effect` with `scope:dummy_gender` (:8277-8287), a DLC-feature path this spec does not need. It is recorded in §10.
- **Salvage keeps the prisoner** (blinding releases): explained in §4.5.

**Tiger:** Salvage and the repair rolls reach `increase_wounds_no_death_effect`, so the 16 known-benign 1.20 errors in vanilla `20_health_effects.txt` will appear on these paths too (`CLAUDE.md` §Validation). Tiger 1.17 targets 1.18.3. If it flags 1.20 scheme fields (`phases_per_agent_charge`, `base_maximum_success`, agent packages), check the field against vanilla `steal_back_artifact_scheme.txt` before treating it as real.

---

## 7. Loc surface (eotg-localizer)

Rules:
- index §5 items 1–8 and today's never-name extension;
- US spelling;
- bare `[x.GetName]`;
- appended desc lines start with `\n\n`;
- **no tooltip, toast or desc quantifies risk or odds**. The scheme's vanilla success-chance UI is not ours.

**The renderings in [cybernetics_v2_interactions_lore.md](cybernetics_v2_interactions_lore.md) §Renderings are binding.** The localizer may polish them within the rules below, but does not rewrite them. Display names follow that file: *Offer Augmentation*, *Demand Implant Removal* (bare "Removal" reads as removal from office), *Have Them Examined*, *Tamper with Implants*, *Salvage Implants* (bare "Salvage" reads as rescue).

**Pronouns:** the mod's loc uses gendered pronouns for scoped single characters (human request, 2026-10-04): `[x.GetSheHe]` and its siblings, never singular "they". Some renderings say "their" or "they" of one character (for example `EOTG_AUG_AI_LIEGE`, `_COUNTDOWN`, `EOTG_AUG_TAMPER_TARGET_PHYSICIAN`, `EOTG_AUG_TAMPER_DISCOVERY_DESC`, the Offer and Demand `_desc`). The localizer genders them when a scope is available in that string. Where none is (some engine-drawn descs), it rephrases to avoid the pronoun.

**Register for the tampering (binding, lore review):** physical and local. Agents with hands: someone at the maintenance hatch, a bribed technician, a panel opened while the target slept.
- **"A dose" is a sedative for the sleeper** (lore I6). It never acts on the hardware: no nanites, nothing in the bloodstream that reaches the implants.
- **Firmware is changed only by hand, at an open panel** (I6).
- **Never** "signal", "transmit", "remote", "from afar", "kill switch", "override code", "shut down", "terminate", "brick", "hack", "virus", "upload", "network". Remote implant control is Blackstar technology of 1300.
- The voice register (index §5.1–2) does not appear.

**Tracing (int.001.d, tamper.004.e; lore I5):** physical evidence only: tool marks, a replaced seal, a bribed technician who talks, who had access. At most, the implant's own record of a change made at its panel. Never a connection log, a signal path or a network trace.

**Salvage register (Salvage Implants, int.002, proc.002 and proc.020 `desc_salvaged`; lore I4):**
- Never "harvest", "reap", "farm", "strip for parts", or "scrap" / "wreck" applied to the person.
- No gore past init.012's level ("the socket is empty and raw").
- Removed hardware carries nothing of its wearer: no memory, replay or connection, and never "someone else wears it now".

No vanilla string needs a `replace/` override. Vanilla keys reused as-is: `START_SCHEME`, `SCHEME_HOOK`, `SCHEME_WEAK_HOOK_USED`, `AI_OPINION_REASON`, `schemes.t.agent_packages`, `agent_focus_*`, `restart_scheme_tt`, `sway_foreign_target`, `FABRICATE_HOOK_RULER_TARGET`, `SCHEME_AT_WAR`, `SCHEME_AT_WAR_WITH_LIEGE`, `currently_being_tortured`, `is_currently_being_purged_tt`, `scheme_target_not_in_diplomatic_range`.

| Keys | Count |
|---|---|
| **Interactions:** `eotg_aug_offer_augmentation_interaction`, `_desc`, `_notification`; `eotg_aug_demand_removal_interaction`, `_desc`, `_notification`; `eotg_aug_examine_interaction`, `_desc`; `eotg_aug_start_tamper_interaction`; `eotg_aug_salvage_interaction`, `_desc` | 11 |
| **Send options:** `eotg_aug_send_provider_heading`, `eotg_aug_send_clinic` (+`_tt`), `eotg_aug_send_physician` (+`_tt`), `eotg_aug_send_backstreet` (+`_tt`), `eotg_aug_send_rough` (+`_tt`) | 9 |
| **Tamper start:** `eotg_aug_start_tamper_approved_tt`, `eotg_aug_start_tamper_notification`, `eotg_aug_start_tamper.tt.agent_focus_balance / _success / _speed / _secrecy` (vanilla list format, `start_abduct.tt.*`) | 6 |
| **Toasts and effect tooltips:** `eotg_aug_offer_accepted_toast`, `eotg_aug_offer_declined_toast`, `eotg_aug_demand_accepted_toast`, `eotg_aug_demand_declined_toast`, `eotg_aug_examine_declined_toast`, `eotg_aug_demand_removal_effect_tt`, `eotg_aug_salvage_effect_tt`, `eotg_aug_tamper_foiled_toast` | 8 |
| **`ai_accept` descs:** `EOTG_AUG_AI_LIEGE`, `_AMBITIOUS`, `_CYNICAL`, `_BRAVE`, `_GREEDY`, `_LOSS`, `_CRAVEN`, `_CONTENT`, `_PARANOID`, `_HUMBLE`, `_ZEALOUS`, `_FORMER`, `_CLINIC`, `_PHYSICIAN`, `_BACKSTREET`, `_TIER_AUGMENTED`, `_TIER_ENHANCED`, `_TIER_OVERCLOCKED`, `_STUBBORN`, `_ARROGANT`, `_STRESS`, `_COUNTDOWN`, `_ILLEGAL`, `_TRUSTING`, `_DECEITFUL` | 25 |
| **Scheme:** `eotg_aug_tamper`, `eotg_aug_tamper_action`, `eotg_aug_tamper_desc`, `eotg_aug_tamper_desc_general`, `EOTG_AUG_TAMPER_SUCCESS_DESC`, `EOTG_AUG_TAMPER_DISCOVERY_DESC`, `eotg_aug_tamper_invalidated_title`, `eotg_aug_tamper_invalidated_dead`, `eotg_aug_tamper_invalidated_removed`, `EOTG_AUG_TAMPER_TARGET_PHYSICIAN`, `_TARGET_ILLEGAL`, `_TARGET_HARDENED`, `_TARGET_FRACTURED`, `_OWNER_KNOWS` | 14 |
| **Engine-generated scheme modifier names**, only if PX `missing-required-loc` asks for them (vanilla has them for its schemes): `eotg_aug_tamper_scheme_phase_duration_add`, `eotg_aug_tamper_enemy_scheme_phase_duration_add` (vanilla form at `steal_back_artifact_scheme_phase_duration_add`) | (2) |
| **Opinions:** `eotg_opinion_aug_forced_procedure`, `_demanded_removal`, `_salvaged_me`, `_salvaged_family_member`, `_tampered` | 5 |
| `eotg_aug_int.001.t`, `.desc`, `.desc_fractured`, `.desc_oc_bad`, `.desc_oc_ok`, `.desc_stable`, `.desc_flaw`, `.desc_tampered`, `.desc_infection`, `.desc_illegal`, `.a`–`.e`, `.b.tt`, `.d.success`, `.d.failure` | 18 |
| `eotg_aug_int.002.t`, `.desc`, `.desc_augmented`, `.desc_enhanced`, `.desc_overclocked`, `.desc_fractured`, `.desc_died`, `.desc_maimed`, `.desc_fragments`, `.a`–`.e` | 14 |
| `eotg_aug_tamper.002.t`, `.desc`, `.desc_tier1`, `.desc_tier2`, `.desc_tier3`, `.desc_fractured`, `.desc_discovered`, `.a`, `.b` | 9 |
| `eotg_aug_tamper.003.t`, `.desc`, `.desc_tier3`, `.desc_discovered`, `.a`, `.b` | 6 |
| `eotg_aug_tamper.004.t`, `.desc`, `.desc_aug`, `.desc_enh`, `.desc_oc`, `.desc_nf`, `.desc_known`, `.desc_unknown`, `.a`–`.e`, `.tt`, `.e.success`, `.e.failure` | 16 |
| **Procedures amendments:** `eotg_aug_proc.002.desc_salvaged`, `eotg_aug_proc.002.desc_repair_fault`, `eotg_aug_proc.020.desc_salvaged` | 3 |
| **Total** | **~144 (+2 conditional)** |

**Briefs:**
- **Offer:** a gift, in the transactional tone of the existing system. The physician and clinic tooltips say who does the work, never who licenses it (the procedures spec's neutral-licensing rule). The back-street tooltip: cheap, unvetted.
- **Demand Removal:** the liege's own will, no law cited. Zealous lines are faith-neutral ("as you were made").
- **int.001:** a physician's plain report. Bands as prose ("running hot", "within tolerance", "unstable"). `desc_tampered`: "someone has had a panel open". `desc_illegal`: back-street work, unnamed.
- **Salvage and int.002:** clinical and cold, no gore past init.012's level. The buyer of salvage is "a dealer" or "someone who asks no questions". **Never the Concrete Cartel**, or any named salvage trade. `desc_died`: they did not survive the table, and the hardware came out anyway.
- **tamper.004 *A Fault in the Hardware*:** bodily and hardware symptoms only (lore I2): the overlay stutters, a sensor drifts, a limb **responds** late. No forecast, and never "answers". `desc_unknown`: new seals; someone had their hands on it. `desc_known` names `[owner.GetName]`.
- **proc.002 `desc_repair` and `outcome_repair_failed`** (procedures loc) **must read injury-neutral**, because a fault repair also lands there. Binding text (lore I3, also updated in [cybernetics_v2_procedures_lore.md](cybernetics_v2_procedures_lore.md)): `eotg_aug_proc.outcome_repair_failed` = "\n\nThe repair did not take. The part sits where it was fitted and does nothing, and nothing is better than it was."
- **Titles (ratified by lore):** *The Physician's Report*, *What Came Out*, *The Work Is Done*, *Hands Withdrawn*, *A Fault in the Hardware* (I1); the interactions *Offer Augmentation*, *Demand Implant Removal*, *Have Them Examined*, *Salvage Implants*; the scheme *Tamper with Implants*; the opinion `eotg_opinion_aug_salvaged_me` "Cut Out My Implants".

---

## 8. Lore constraints

- **866 AG**, cybernetics common and commercial (`REVIEW_866.md`, "Augmentation trade"). Salvage exists as a trade at 866, but **it is never named** (the Concrete Cartel is on the never-name list).
- **No remote control of implants** (Blackstar, 1300). Tampering is physical and local, enforced by the loc register (§7) and by the mechanic: agents need access, location penalties apply, and nothing acts at a distance.
- **No supranational authority** (LAW AT 866). Demand Removal is the liege's own will. Discovery is answered by the victim's own power to imprison (`imprisonment_reason`). No court, tribunal or licensing body is named or implied.
- **Never name the implant players** (index §5.3, extended today): Blackstar, Shadow Markets, Black Contract(s), Blackline, P&D, Calix, Pill Mob / Pillwake / Red Pills, Concrete Cartel, "Trauma Team".
- **Nikios Khanate:** not touched.
- **Lore rulings (2026-10-04, [cybernetics_v2_interactions_lore.md](cybernetics_v2_interactions_lore.md)):**
  1. **Seamless exclusions from Demand Implant Removal, Tamper and Examine: upheld.** The reason, to be kept in the trigger comments: at 866 tech no surgeon can find where Seamless hardware ends and the body begins. There is no panel to open, nothing to take out, and nothing to examine apart from the body.
  2. **Salvage of Seamless prisoners: open human decision.** Option A, exclude (lore's recommendation, and what this spec builds now). Option B, allow it with death on the table forced; lore does not recommend it.
  3. **Salvage tone at 866: approved.** The trade stays unnamed: the buyer is only "a dealer" or "someone who asks no questions". The prose is clinical, and the cruelty is the actor's choice. Register in §7 (I4).
  4. **Titles:** ratified, with *Demand Implant Removal*, *Salvage Implants*, *A Fault in the Hardware* and "Cut Out My Implants" (§7).
  5. **Throttle wording (shipped loc, outside this spec's build):** `eotg_mod_aug_patron_throttle_desc` takes the lore file's text ("The syndicate's technicians wrote a throttle into the firmware at installation, … The body feels the limit as stress and weakness."). The trigger is a local absence (the servicing stopped), never a remote signal. This is a localizer task. The index's thread T2 now says "the firmware throttle" (I7).
  6. **Noted for later:** vanilla scheme agent names ("Physic", "Smith", "Footpad") and the generic scheme-ongoing loc are medieval leaks. They affect every scheme in the mod and belong to the vanilla reflavor pass, not to this spec.

---

## 9. Definition of done

0. **Tiger, `px_lsp_diagnostics.js` and `px_vocab_check.py` clean** on the touched files, except the `CLAUDE.md` known-benign list (including the 16 `20_health_effects.txt` errors). Tiger findings on 1.20 scheme fields are checked against vanilla `steal_back_artifact_scheme.txt` first (§6).
1. **Reachability (PX event graph):**
   - int.001 from `eotg_aug_examine_interaction`;
   - int.002 from `eotg_aug_salvage_interaction`;
   - tamper.001 from `eotg_aug_tamper_prep_effect` (saved `follow_up_event`; the PX graph may not follow `saved_event_id`, so QA confirms by grep);
   - tamper.002/.003 from tamper.001; tamper.004 from tamper.002 a/b.
   - No event is fired by nothing.
2. **Cooldown authority:** no event `trigger` checks a cooldown. Interaction cooldowns are `cooldown_against_recipient` only. The scheme's is `cooldown = { years = 10 }`.
3. **Roll discipline:** every call to `eotg_aug_procedure_effect` / `_roll_effect` sits in an interaction `on_accept` or an event option, inside `hidden_effect`, followed by a `custom_tooltip`. None in an `immediate`. `grep -n random_list` in the new event files returns only tamper.004's and int.001's duel blocks, if any; no outcome odds outside the roll.
4. **Severe tail only in the back streets:** with the provider pinned to clinic or physician, Salvage, Offer, Demand and fault repairs can never select maimed / one_eyed / blind / death. Death weight stays 0 for every `repair`.
5. **Coupling (QA audit 8):**
   - int.001 a/b/e and int.002 b/c/e move risk or tier;
   - int.001's desc reads the band and int.002's reads the tier;
   - tamper.004's immediate moves risk;
   - tamper.002/.003 descs read the target's tier;
   - tamper.001 is hidden plumbing.
6. **Hidden rule:** no new tooltip, toast, desc or `ai_accept` desc contains a number, or the words "risk", "odds" or "chance", about the signature resource. Every risk move is in `hidden_effect`.
7. **Map-agnostic:** `grep -nE "title:|culture:|faith:|character:[0-9]" common/character_interactions common/schemes events/eotg_augmentation_interactions.txt events/eotg_augmentation_tamper.txt` returns nothing.
8. **Identifiers:** every new global key starts `eotg_` (except the documented `agent_focus_*` local flags and vanilla `scheme_successful` / `scheme_discovered` scope values). `grep -rnE 'eotg_[ekdcb]_'` stays empty.
9. **Lore register:** `grep -niE "remote|signal|transmit|from afar|kill.?switch|override code|shut ?down|terminate|brick|hack|virus|upload|network|harvest|\breap|strip for parts|nanite|blackstar|concrete cartel|p&d|calix|pill ?mob|pillwake|trauma team"` over the new loc keys returns nothing. (`hack|virus|upload|network|harvest` were added by lore I6; `reap|strip for parts|nanite` come from I4 and I6.) Also: tamper.004's loc contains neither "forecast" nor "answer" (I2), and `eotg_aug_proc.outcome_repair_failed` matches the I3 text exactly.
10. **Observer run** (balance §9.2) **adds five counters** per decade: Offer installs (landed / unlanded), Demand removals, Examinations, Tamper starts / successes / discoveries, Salvages (and deaths on the table). Judged against HQ2 (§4.7).
11. **Loc:** all §7 keys exist exactly once, with BOM and no `[scope:`.
12. **Human, in game (temporary map):**
    - **Offer:** to an unaugmented courtier with a clinic (silent install, gratitude); to a one-legged courtier (leg restored); to a zealous one (the send button is blocked, and the AI breakdown shows the reason); through the back streets (init.011 on the recipient 6–18 months later).
    - **Demand Removal:** on an Enhanced vassal → accepted or refused by the shown odds. When accepted, the vassal is out (former `flag:removed`, withdrawal). When refused, the vassal shows "Demanded Removal". With a strong hook → auto-accept and "Forced Procedure".
    - **Examine:** a tier-3 spouse → int.001 with a band line. "Fix the fault" on a flawed patient → proc.002 shows the fault-repair opener.
    - **Tamper:** start it with each agent package. Confirm the slots fill and the vanilla preparations window opens at phase completion. Execute → tamper.002, then tamper.004 on the target with the tampered modifier, and the target's next procedure is worse (repeat to sample). Fail with discovery → the target gets the opinion and a toast. The scheme invalidates when the target leaves the system.
    - **Salvage:** an augmented prisoner, the rough way, about 20 reloads. Expect mixed outcomes with Fragments common, and at least one severe. With a physician, mostly clean. Kin dies on the table → kinslayer. The prisoner stays imprisoned. int.002 a/b/c each work.
    - **Engine checks (not settled by vanilla):**
      - (a) the PX event graph or Tiger accepts `trigger_event = { saved_event_id = scope:follow_up_event }` reaching tamper.001;
      - (b) `scope:eotg_proc_outcome` saved inside the roll is readable later in the same `on_accept` (the procedures roll's own pattern) and in int.002;
      - (c) AI actually sends Offer, Demand, Examine and Tamper in an observer run (any non-zero count).

---

## 10. Deferred

| Item | Why |
|---|---|
| **Offer to children** | **Pending the human.** The Sickly Child arc (init.014, Q8) already covers a sick child under a tone ruling. A healthy-child augmentation is a new moral beat. **Lore recommends adults only**, citing init.014's own line that the procedure is "never done on the very young". Until the human rules, `is_adult = yes` stays in `eotg_aug_offer_candidate`. |
| **Lend Your Surgeon** (gaps G4, optional) | It is the court-position problem (G10, the Implant Technician). Borrowing another court's physician needs a cross-court surgeon scope that G10 would define once. |
| **Higher ransom for augmented prisoners** (gaps G8) | Vanilla computes ransom in its own script values. Changing it means overriding a vanilla file, which this project avoids (collisions are silent, and one-definition rules apply). Revisit if vanilla exposes a hook. |
| **Refusal as a crime** (Demand Removal) | Belongs to G7's Augmentation Edict (ban), as vanilla gates refusal-crime on law. The hook: `on_decline` gains `reverse_add_opinion` with an `imprisonment_reason` opinion when the actor's realm holds the ban flag. |
| **House-relation damage on Salvage** | Vanilla's call uses a DLC-feature scope (`scope:dummy_gender`, `00_prison_interactions.txt:8277-8287`). It is not needed for the system. |
| **Puppet actors** (`scope:puppet_or_actor`) | A 1.20 DLC mechanic. The interactions use `scope:actor` like the courtier conversion precedent. |
| **Rolls for init.020 / the retainer hub and other installs on others** | Unchanged from the procedures deferral. The Offer interaction rolls; the decision hub keeps its own logic. Unify later if QA finds the two inconsistent in play. |
| **A Tamper "method" choice** (abduct-style method events) | Six events is the lean target. One method, scaled by tier, carries the system. |
| **Episodes as a sabotage result** | Lesson 5: episodes belong to the band pools' cooldown authority (the same call as the procedures spec's operating table). |
| **Dedicated icons** for the five interactions and the scheme | Vanilla placeholders now (§3.1). Art debt for the human, alongside the Seamless trait icon. |
| **A scheme odds-prediction term for the mod's modifiers** | The vanilla prediction is an approximation. Our ±10/15 lines are left out of it rather than adding a misc script value. Add one if players find the prediction misleading. |

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Build docs/specs/cybernetics_v2_interactions.md §3–§5 (including the §3.2 procedures amendments) after the procedures spec lands. The lore review is folded in (I1–I7). Salvage Implants builds option A (Seamless excluded) until the human decides. Then eotg-localizer: §7, with docs/specs/cybernetics_v2_interactions_lore.md §Renderings binding, the gendered-pronoun rule, the I3 text for eotg_aug_proc.outcome_repair_failed, and the rewrite of the shipped eotg_mod_aug_patron_throttle_desc (§8 ruling 5). Then eotg-qa (§9, with item 9's extended grep).
- files: docs/specs/cybernetics_v2_interactions.md; docs/specs/cybernetics_v2_interactions_lore.md (binding renderings); docs/specs/cybernetics_v2_procedures_lore.md (I3 line)
- new events (6; below the ~10 flag): eotg_aug_int.001 The Physician's Report (eotg_aug_examine_interaction on_accept); eotg_aug_int.002 What Came Out (eotg_aug_salvage_interaction on_accept); eotg_aug_tamper.001 hidden result (eotg_aug_tamper_prep_effect → vanilla scheme_critical_moments.0002 → saved follow_up_event); eotg_aug_tamper.002 The Work Is Done and eotg_aug_tamper.003 Hands Withdrawn (both from tamper.001); eotg_aug_tamper.004 A Fault in the Hardware (tamper.002 a/b, on the target). Also 5 interactions, 1 scheme type (eotg_aug_tamper), 1 custom on_action (eotg_aug_tamper_ongoing).
- needs-loc (~144, +2 conditional, §7): as listed in §7; the lore file's renderings are binding.
- needs-lore: none open (I1–I7 folded in)
- needs-human: Salvage of Seamless prisoners, option A (exclude, built) or B (forced death) (§8 ruling 2); offering augmentation to healthy children (§10; lore recommends adults only); the §9 item 12 in-game checks, including engine checks (a)–(c); the observer run's five new counters (§9 item 10); placeholder icons as art debt; the orchestrator adds common/character_interactions/ and common/schemes/scheme_types/ to the CLAUDE.md placement table, and the vanilla scheme-agent-name leak (§8 ruling 6) to the circleback board
