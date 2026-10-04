# Spec: Cybernetics v2 — self-repairing machinery (a researchable advance, and the hardware it unlocks)

**Author:** eotg-architect, 2026-10-04
**Authorised by:** the human, 2026-10-04 (relayed by the coordinator): *"make self-repairing machinery a research option that unlocks a much more expensive augmentation reducing the need for calibration."*
**Index:** [cybernetics_v2.md](cybernetics_v2.md). Index §1 rules 1–12 and the §5 lore register apply to everything here.
**Builds on, does not re-spec:**
- [cybernetics_v2_procedures.md](cybernetics_v2_procedures.md): the shared roll (`eotg_aug_procedure_effect`, params `PATIENT` / `PROVIDER` / `PROCEDURE` / `SURGEON`), `eotg_aug_save_surgeon_effect`, the pricing helpers, proc.002 *After the Procedure*.
- [cybernetics_v2_realm.md](cybernetics_v2_realm.md): `eotg_aug_clinic_open`, `eotg_aug_has_surgeon_access`, `eotg_aug_surgeon_is_technician`, `eotg_aug_opt_technician`, the conditional `eotg_aug_price_mult_physician`, and the technician's Overclocked accrual rows (§3.2 row for `eotg_on_yearly_aug_overclocked_check`).
- [cybernetics_v2_procedures_lore.md](cybernetics_v2_procedures_lore.md): the 866 tech ceiling (lore N1).
**Also binding:** [cybernetics_v2_balance.md](cybernetics_v2_balance.md) (HQ1 / HQ2, §9.2 observer run); the SETTING LORE ERRATA entry **CYBERNETICS AT 866** (2026-10-04).

**Build position.** Last in the cybernetics queue: **procedures → interactions → realm → reprisal → this spec.** It reads triggers, values and option shapes that only exist once procedures and realm are built (§4.7). It shares files with reprisal (effects, loc), so it lands after it.

**Size.**
- **1 new event** (`eotg_aug_proc.005`). Below the 2-event flag; no further yes needed.
- 1 new culture innovation (the mod's first file in `common/culture/innovations/`, which is a **new folder** for the placement table).
- 1 new decision, 1 new static modifier, 2 new script values.
- 1 new desc line on proc.002. Small edits to 2 decisions, 2 on_actions and 1 effect.
- About 20 loc keys.
- No new trait, opinion, story cycle, on_action, namespace, death reason, character template or law. Icons reuse existing art (§3.1); bespoke innovation art is optional human debt.

---

## 0. Corrections to the brief (found in the current script)

| Brief says | Script says | Consequence here |
|---|---|---|
| The Calibrated Systems modifier is `eotg_mod_aug_calibrated` | The key is **`eotg_mod_implant_calibrated`** (`common/modifiers/eotg_augmentation_modifiers.txt`; loc "Calibrated Systems"). It carries `stress_gain_mult = -0.15`, `health = 0.3`. | This spec uses the real key. |
| Calibration slows risk | **It does not.** Nothing reads `eotg_mod_implant_calibrated` in any accrual. The only risk effect of calibration is the **one-off −8 at Overclocked** in `eotg_decision_maintenance_protocol`'s effect (−12 in Consult the Physician; the realm spec makes Maintenance −12 with a technician). | "Calibrations last longer" alone would buy stress and health, not stability. The package in §4.3 pairs it with an accrual change so the hardware does what its name says. |
| The Maintenance cooldown | `eotg_flag_maintenance_cooldown`, 3 years, **set in the decision effect** and read in its `is_valid` / `ai_potential`. Decision-owned (index §1 rule 5). | Not shortened and not removed (§4.3, "Rejected"). |

---

## 1. Purpose & gate

**Self-repairing machinery** is not in existence at 866 AG, but a culture's scholars can develop it (ERRATA, CYBERNETICS AT 866). Here it is a **culture innovation**: a culture researches it as it researches any other advance in CK3. Once the culture has it, an augmented character of that culture can pay for a **refit**. This is a procedure on the existing machinery (provider choice, shared roll, reveal), not a new tier. The refit lets calibration last longer, and slows the wear that drives Overclocked hardware toward the cascade. It does not touch the mind: stress, paranoia, war and everything after the cascade run exactly as before.

**Gate 3 (Systems), built against the temporary map** (`docs/agent_workflow.md` §5 rule 2; the mod-exclusive exception in `CLAUDE.md`). **Not blocked**, but it is built **after** the four specs ahead of it in the queue.
- **Map-agnostic.** No culture, title, province, character or faith keys. The innovation has no `potential`, no `region` and no heritage asset, so every culture can research it, vanilla cultures on the test map included.
- **One coupling to Gate 1** (recorded in §10 and for the taskboard): the innovation is placed by **era**. The era a culture holds at 866 is set by the mod's culture history, which Gate 1 builds from the briefs. §4.1 states the rule that survives that change.

**Not built, by canon (ERRATA):** remote-kill or wearer-termination, state programmes or subsidies, mind upload, datavaults, AI secretariats. None of them appears here, even as flavor. The innovation is **a culture's scholars advancing**, not a state programme. Nothing is funded, mandated or issued by a realm.

---

## 2. Signature resource

| Resource | How this system couples |
|---|---|
| **`eotg_fracture_risk`** (hidden, 0–100), unchanged | **The refit moves it at once.** Deep work adds risk +2 / +4 / +6 at Augmented / Enhanced / Overclocked (the repair scale from procedures §4.2 step 3, minus the Neurofractured step: a Neurofractured character cannot be refitted). A complication on the roll adds +10. **The fitted hardware then changes its yearly accrual** at Overclocked (§4.3). |
| **tier** | Read: the refit is offered at tiers 1–3 only (`has_trait = eotg_cybernetics`), and its desc reads tier 3. |
| **Marker:** `eotg_mod_aug_self_repair` (permanent static modifier) | The state this system adds. It is read by the accrual value, the two calibration decisions and the decision's own `is_shown`. It is **visible** on the character sheet; it carries no number about risk. |

**Coupling (invariant 5 / index §1 rule 4):**
- proc.005 a and b move risk (the fit) and lead to a tier-keyed procedure.
- proc.005 c is the decline (as proc.001.d and proc.003.d; index §1 rule 6 allows a no-op decline).
- proc.002's new `desc_refit` is a chain stage of a procedure that moves risk.

**Why a modifier and not a flag or variable.** The player paid three years' income for it and must be able to see it. A modifier is the vanilla way to show a lasting bodily state with a description, and `has_character_modifier` is a cheap read. A flag (the `eotg_flag_aug_hidden_flaw` pattern) is right for a secret; this is not one. It needs no new art (§3.1).

---

## 3. Identifier table

All keys carry the `eotg_` prefix. No landed titles. Loc keys use the dot form for events (index §0); the innovation uses the vanilla key-as-loc form (`_culture_innovations.info:11`).

### 3.1 New

| Type | Key | Where | Owner |
|---|---|---|---|
| culture innovation | `eotg_innovation_self_repairing_machinery` | `common/culture/innovations/eotg_innovations.txt` (**new folder for the mod**; additive, no `replace_path`) | scripter |
| innovation flag | `eotg_cybernetic_innovation` (`flag =`; **not** `global_regular` / `early_medieval_era_regular`, §4.1) | same file | scripter |
| innovation icon | stopgap `gfx/interface/icons/culture_innovations/innovation_misc_inventions.dds` (vanilla, the `@misc_inventions` icon used by `innovation_armilary_sphere`, `00_early_medieval_innovations.txt:30, :413`) | same file | scripter (stopgap); **human** if bespoke art is wanted (not blocking) |
| decision | `eotg_decision_aug_self_repair` | `common/decisions/eotg_augmentation_decisions.txt` | scripter |
| decision picture | placeholder: `gfx/interface/illustrations/decisions/eotg_decision_maintenance_protocol.dds` (the Seek decision already reuses it) | same | scripter; human if bespoke |
| event | `eotg_aug_proc.005` *Within Tolerance* (lore-keeper's name) | `events/eotg_augmentation_procedures.txt` | scripter |
| static modifier | `eotg_mod_aug_self_repair` (`icon = eotg_implant_calibrated`, the existing mod icon; `health = 0.1`) | `common/modifiers/eotg_augmentation_modifiers.txt` | scripter |
| scripted effect | `eotg_aug_self_repair_fit_effect` (no params; patient scope: adds the modifier, then the tier-scaled risk in `hidden_effect`) | `common/scripted_effects/eotg_augmentation_effects.txt` | scripter |
| scripted trigger | `eotg_aug_can_self_repair` (culture has the innovation; `has_trait = eotg_cybernetics`; NOT the modifier) | `common/scripted_triggers/eotg_augmentation_triggers.txt` | scripter |
| script value | `eotg_aug_self_repair_price_value` (= `massive_gold_value` × 2) | `common/script_values/eotg_augmentation_values.txt` | scripter |
| script value | `eotg_aug_oc_wear_relief_value` (≤ 0; sum of the three wear-relief rows, no cap, down to −9; §4.3) | values file | scripter |
| saved scope value (event chain) | `eotg_proc_refit` (`yes`; read by proc.002's opener) | proc.005 options | scripter |

### 3.2 Changed (key kept)

| Key | Change | § |
|---|---|---|
| `eotg_on_yearly_aug_overclocked_check` | The vendor-safe row (−3) and the realm technician row (−2 / −3) are **replaced** by one call: `eotg_add_fracture_risk = { AMOUNT = eotg_aug_oc_wear_relief_value }`. The vendor-bold row (+3) stays separate. All other rows unchanged. | 4.3 |
| `eotg_on_yearly_aug_nonruler_check` | Step 3, the Overclocked accrual (base 10, +6 at stress level 2+): one row, `has_character_modifier = eotg_mod_aug_self_repair` → −3. | 4.3 |
| `eotg_decision_maintenance_protocol` | Calibration lasts **5 years** with the modifier (else 3). Cooldown flag unchanged at 3 years. `ai_will_do` gains `modifier = { add = -10  has_character_modifier = eotg_mod_aug_self_repair  eotg_is_aug_tier3 = no }`. | 4.3 |
| `eotg_decision_consult_physician` | Calibration lasts **7 years** with the modifier (else 5). | 4.3 |
| `eotg_clean_all_aug_modifiers` | One guarded line: remove `eotg_mod_aug_self_repair`. That clears it on a full exit (`eotg_aug_remove_all_effect`) and at Total Integration (`eotg_aug_total_integration_effect`), the effect's only two callers. | 4.5 |
| proc.002 *After the Procedure* | One new opener, `desc_refit`, **first** in its opener `first_valid`, when `exists = scope:eotg_proc_refit`. | 4.4 |
| realm spec §3.2, technician accrual row | **Location only:** its two values (−2 / −3) move unchanged into `eotg_aug_oc_wear_relief_value`. No change to its numbers; the realm spec's −6 best case stands (human, 2026-10-04). | 4.3 |

**Reused, not new:** `eotg_aug_procedure_effect`, `eotg_aug_save_surgeon_effect`, `eotg_aug_pay_procedure_effect`, `eotg_aug_can_afford_procedure`, `eotg_aug_price_mult_physician`, `eotg_aug_stress_surgery_effect`, `eotg_add_fracture_risk`, `eotg_aug_clinic_open`, `eotg_aug_has_surgeon_access`, `eotg_aug_surgeon_is_technician`, the loc key `eotg_aug_opt_technician`, `eotg_aug_clinic_closed_tt`, `eotg_is_aug_tier1/2/3`, `eotg_aug_has_countdown`.

---

## 4. Wiring

### 4.1 The innovation (research)

**Engine facts** (vanilla 1.20.0.3, under `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`):

| Fact | Evidence |
|---|---|
| An innovation names one era (`culture_era`), one group (`culture_group_military` / `culture_group_civic`), a head-of-culture skill for fascination (`skill`, default learning), an `icon`, optional `potential` (hidden if false) and `can_progress` (shown but stalled if false), optional `flag`s, and `unlock_*` / `custom` tooltip lines. **`unlock_decision` is tooltip-only**: the decision must gate itself. | `common/culture/innovations/_culture_innovations.info:14-30, 75-79, 100-114` |
| **There is no per-innovation cost or progress field.** The only levers are era placement, `can_progress`, `region`, and the AI weights. | same file (full field list) |
| Era years: tribal 0, early medieval **900**, high medieval **1050**, late medieval 1200. The year is when the era *starts receiving base spread*; a culture then needs at least 8 of its current era's innovations plus era progress to join it. | `common/culture/eras/00_culture_eras.txt:2-7, 39-40, 83-84`; `_culture_eras.info:2`; `common/defines/00_defines.txt:1194-1196` (`MINIMUM_INNOVATIONS_TO_NEXT_ERA = 8`, `ERA_PROGRESS_GAIN_BASE_MONTHLY = 0.1`) |
| At the vanilla 867 start, almost every culture is in the **tribal** era. Most join early medieval at the **950** history entry. | e.g. `history/cultures/greek.txt:3-24` (867 innovations, `join_era = culture_era_early_medieval` at `950.1.1`); 22 of the files with an early-medieval `join_era` place it at 950, 1 at 866 |
| **Ahead-of-time research exists.** A culture can progress an innovation from a later era, with progress divided by 5 per era behind. Each ahead-of-time innovation a culture holds divides further gains by 2 (exponential). | `00_defines.txt:1230-1233` (`INNOVATION_PROGRESS_DIVIDE_FACTOR_IF_ERA_BEHIND = 5`, `…_PER_AHEAD_OF_TIME_TECH = 2`) |
| Vanilla stops the **AI** from fascinating a future-era innovation with `ai_weight_for_fascination` × 0 until the culture is in that era. In this block root is the culture and `scope:character` is the culture head. | `00_early_medieval_innovations.txt:58-68` (`innovation_battlements`); `_culture_innovations.info:45-50` |
| Spread: a neighbouring culture that has it adds +40 to the monthly progress chance. Fascination adds 10 plus a skill bonus. | `00_defines.txt:1206-1221` |
| Other script tests a culture with `culture = { has_innovation = x }` from character scope; `liege.culture ?= { … }` when the liege's culture matters. | `common/buildings/00_city_buildings.txt:459-461`; `common/decisions/30_activity_decisions.txt:767-768`; `common/court_positions/types/00_court_positions.txt:5949-5950` (`scope:liege.culture ?= { has_innovation = fp3_innovation_mural_sextant }`) |
| A future-era `can_progress` prerequisite: `can_progress = { has_innovation = innovation_fire_medicine }`. | `common/culture/innovations/tgp_innovations.txt:151-153` |
| Grant by effect (tests, console): `add_innovation = x` in culture scope. | `events/decisions_events/roman_restoration_events.txt:2575-2584` |
| There is **no** on_action for "innovation discovered". The culture hooks are `yearly_culture_pulse`, `three_yearly_culture_pulse`, `on_culture_era_changed`, and others not relevant. | `common/on_action/culture_on_actions.txt:5, 15, 24` |

**Gating options.** The brief asks for the advance to be realistic for 866: not instant, not trivially early, and not locked to a hard 975 date that a normal playthrough never reaches.

| | Placement | When the AI world gets it | When a determined player gets it | Verdict |
|---|---|---|---|---|
| **A. Late era** | `culture_era = culture_era_high_medieval` | Not before the culture joins high medieval (base spread from 1050; vanilla pacing ~1100). | Ahead of time from a tribal culture at ÷10 (two eras behind). Over a century. | Canon-safe, but the human would not see it in a normal playthrough. **Not recommended.** |
| **B. Mid era, cost through ahead-of-time** | `culture_era = culture_era_early_medieval`; no `can_progress`; AI fascination × 0 until in era | After the culture joins early medieval (spread from 900; vanilla history joins most at 950): **roughly 940–1000 AG**, which brackets canon's 975. Spread then carries it to neighbours. | From day one, by fascinating it ahead of time at ÷5, and paying vanilla's ahead-of-time penalty on later research. **About 5T**, where T is an in-era fascination (to be measured on the test map; §9). | **Recommended; decided by the human 2026-10-04.** |
| **C. Mid era with a prerequisite** | as B, plus `can_progress = { has_cultural_era_or_later = culture_era_early_medieval }` | As B. | Only after the culture joins the era: as the AI, plus T. | The fallback if B proves too fast in testing (one line). |

**Decided: B** (human, 2026-10-04; the architect's recommendation). Price `massive_gold_value` × 2 decided the same day.
- It is the vanilla cost lever. CK3 has no "expensive innovation" field. What it has is research ahead of your era: slow (÷5), and taxing (later ahead-of-time progress halves).
- The AI follows the vanilla pattern, so the world gets the advance around canon's date. A player who wants it can buy it early with research priority. That fits "a culture's scholars advancing".
- It needs no prerequisite on a vanilla innovation key. v2 may ship its own innovations later, and a `has_innovation = innovation_x` prerequisite would then break silently.

**Rule that survives Gate 1** (for the taskboard): *the innovation sits exactly one era above the era the mod's cultures hold at 866.* If the mod's culture history puts its 866 cultures in `culture_era_early_medieval` (a spacefaring setting might), move it to `culture_era_high_medieval`, and its AI × 0 test with it. If v2 replaces the eras, re-point both keys. Nothing else changes.

**Definition** (shape: `innovation_armilary_sphere`, `00_early_medieval_innovations.txt:409-433`, plus `unlock_decision` from `.info:105-106`):

```
eotg_innovation_self_repairing_machinery = {
    skill = learning                          # a culture's scholars (fascination uses the head's learning)
    group = culture_group_civic
    culture_era = culture_era_early_medieval  # option B; see the Gate 1 rule above
    icon = "gfx/interface/icons/culture_innovations/innovation_misc_inventions.dds"   # stopgap

    unlock_decision = eotg_decision_aug_self_repair            # tooltip only (.info:105)
    custom = eotg_innovation_self_repairing_machinery_custom

    flag = eotg_cybernetic_innovation        # NOT global_regular / *_era_regular (below)

    ai_weight_for_fascination = {
        value = 50                            # half a normal innovation's 100: the AI does not race for it
        if = { limit = { NOT = { has_cultural_era_or_later = culture_era_early_medieval } }  multiply = 0 }
        if = { limit = { scope:character ?= { eotg_is_augmented_any = yes } }  multiply = 2 }   # an augmented head of culture favours it
    }
}
```

- **No `potential`, `can_progress`, `region` or `asset`:** available to every culture (map-agnostic).
- **No modifiers.** The innovation itself changes nothing until someone pays for a refit. That keeps it from altering vanilla balance on the test map.
- **Why only a mod flag.** `global_regular` is read by vanilla's "all innovations" achievement (`common/achievements/standard_achievements.txt:923`, `has_all_innovations = { with_flag = global_regular }`). The era flags are for the same bookkeeping. The mod has no use for either.
- **Era governments.** The early medieval era is `invalid_for_government` for tribal, nomad, herder and wanua (`00_culture_eras.txt:8-11`). That limits era and innovation *modifiers*. This innovation has none, and its decision tests `has_innovation` directly, so a tribal ruler on the test map can still use it. That is accepted: v2's governments are `eotg_*`.

### 4.2 Who may have it fitted: the patient's own culture

`eotg_aug_can_self_repair` tests `culture = { has_innovation = eotg_innovation_self_repairing_machinery }` on **the patient**.

**Why not the realm head's culture.**
- Vanilla keys what a character can *use* to that character's (or the holding's) culture. Buildings use `culture = { has_innovation }` (`00_city_buildings.txt:459-461`), and `unlock_maa` follows culture.
- `liege.culture` is used where the **liege provides** the thing: the court position's employer, a petition to the liege (`00_court_positions.txt:5949`; `30_activity_decisions.txt:767-768`, which tests both, joined by AND).
- Here the patient buys the hardware. The patient is usually the ruler, so the two tests rarely differ.
- Reaching through the liege would let a courtier of a backward culture buy what their own scholars never made, with no fiction for it.

**Deferred:** buying the hardware from a foreign culture that has it (§10).

### 4.3 What the hardware does (the package), and its pacing

**Fiction (binding for the localizer; lore review S1, S6).**
- The hardware **measures its own wear** and corrects it (S6: never "notices" or "senses").
- It re-zeroes its tolerances, re-seats a contact that has worked loose, routes around a failed path, and logs the part it will need replaced.
- **It cannot make a part, and it does not order one. A worn part is still replaced by hand** (S1). It only puts off the day a part is needed.
- It is machinery: no swarm, no growth, no replication, no agency, no voice. Say nothing about arcana either way (lore Q3).
- It **does not fix the mind**. A self-repairing implant stays in tolerance; the person wearing it does not.

**The package:**

| # | Effect | Where | Tiers |
|---|---|---|---|
| 1 | **Calibration lasts longer.** Maintenance gives Calibrated Systems for **5 years** (was 3); Consult the Physician for **7** (was 5). Cooldowns unchanged (Maintenance 3 years, Consult 3 years). | the two decisions | Augmented, Enhanced, Overclocked |
| 2 | **Slower wear at Overclocked.** **−3 a year** on accrual, through `eotg_aug_oc_wear_relief_value`. It **stacks fully** with the vendor-safe firmware (−3) and the Implant Technician (−2 / −3): **no cap** (human, 2026-10-04). Full stack: −9 a year. | Overclocked check; −3 in the non-ruler check | Overclocked |
| 3 | **Nothing else.** The stress rows (+8 / +16 / +24), paranoid (+12), war (+10), vendor-bold (+3), the hidden-flaw row (+4), the Countdown, the cascade threshold (80), Neurofractured drift and the terminal are all untouched. | — | — |

```
eotg_aug_oc_wear_relief_value = {             # character scope (the ruler)
    value = 0
    if = { limit = { has_character_flag = eotg_flag_aug_vendor_safe }  subtract = 3 }
    # realm §3.2 technician rows, moved here verbatim (−3 at aptitude >= 4, else −2)
    if = { limit = { has_character_modifier = eotg_mod_aug_self_repair }  subtract = 3 }
    # no min: the rows stack fully (human, 2026-10-04)
}
```
- Script value as the `AMOUNT` operand: the mod's own `eotg_aug_nf_drift_value` (vanilla `common/scripted_effects/00_laamp_effects.txt:1247`).
- **Why one value, with no cap.** It keeps the three wear rows in one place for the observer run, and makes a cap a one-line change if the human later wants one (vanilla `min` in a script value: `common/script_values/01_dynamic_values.txt`, every `*_gold_value`). The realm spec's rows and values are unchanged; they only move here.

**Rejected, with reasons:**
- **Shortening the Maintenance cooldown.** It makes the ruler calibrate *more* often, the opposite of the brief. At Overclocked it would also turn Maintenance's one-off −8 (−12 with a technician) into a bigger lever.
- **Removing the cooldown.** Unbounded −8s. That trivialises Overclocked.
- *(A shared −5 ceiling on the three wear rows was proposed and **not taken**: human decision 2026-10-04, no cap. Its consequence is stated in the pacing below.)*

**Neurofractured is not trivialised. By construction:**
- Maintenance and Consult are shown only with `eotg_cybernetics`, which the cascade removes (`eotg_trigger_neurofracture`). So package item 1 cannot reach a Neurofractured character.
- The relief value is read only in the Overclocked branches.
- The modifier stays on a Neurofractured character (no clean-up runs at the cascade) and does nothing but `health = 0.1`. Its desc says so ("it stays in tolerance; you do not").

**Pacing against HQ1 / HQ2.** Cascade at risk 80, Maintenance taken whenever its 3-year cooldown allows (−8 each), no technician:

| Overclocked ruler | Pulses to the cascade today | With self-repair | Change |
|---|---|---|---|
| calm (+12) | 9 (7 with no Maintenance) | 14 (9 with no Maintenance; 12 when calibrating every 5 years, as the longer modifier invites) | +3 to +5 years |
| stress level 1 (+20) | 5 | 6 | +1 |
| at war, calm (+22) | 5 | 6 | +1 |
| stress level 2 (+28) | 4 | 4 | none |
| stress level 3 (+36) | 3 | 3 | none |

**The uncapped best case: full stack** (vendor-safe −3, excellent technician −3, self-repair −3 = **−9 a year**; Maintenance −12 with the technician, every 3 years):

| Overclocked ruler | Realm spec's best case today (−6) | Full stack (−9) | Change |
|---|---|---|---|
| calm (+12 → net 3 a year) | 42 pulses | **never, while Maintenance is kept up**: +9 over three years against −12, so risk sits near 0. With no Maintenance at all: 27 pulses. | the cascade leaves the reign |
| stress level 1 (+20 → 11) | 9 | 12 | +3 |
| at war, calm (+22 → 13) | 8 | 9 | +1 |
| stress level 2 (+28 → 19) | 5 | 6 | +1 |
| stress level 3 (+36 → 27) | 4 | 4 | none |

Self-repair with only one of the other two (−6) is exactly the realm spec's current best case: 42 calm pulses with the technician's Maintenance, 24 with plain Maintenance.

**Stated plainly.** A fully equipped, calm, peaceful, non-paranoid Overclocked ruler who keeps Maintenance up **does not cascade, and does not reach the Countdown's threshold (50)**. Their Overclocked state is stable for as long as those conditions hold. It ends only through stress, war, paranoia, the hidden flaw (+4), vendor-bold, or events that move risk directly. This was already nearly true under the realm spec (42 pulses); self-repair makes it fully true. The cost of the full stack:
- one Bidding War outcome (vendor-safe);
- an excellent technician's salary;
- about three years' income for the refit (§4.4);
- Maintenance every 3 years;
- staying calm.

**What still holds:**
- Neurofractured, its drift and the terminal outcome are unchanged.
- Stressed and warring rulers still cascade within a reign.
- The AI rarely assembles all three pieces.

The observer run (below) measures how often it does.

**Effect on the targets:**
- **HQ1** (minimum 10 years initiation → Overclocked): untouched. The refit is not a tier change and moves no time floor.
- **HQ2** (25–40% augmented, ≥ 15% Overclocked or beyond, at year 30): **untouched at its checkpoint**. Under option B, no AI culture fascinates the innovation before it joins the early medieval era (spread from 900), so no AI ruler is fitted at year 30 (896 AG). Later, the refit costs about three years' income (§4.4), so it is a minority purchase among count+ rulers whose culture has it. Expected effect: the Overclocked share rises slightly, and that rise is what HQ2's "≥ 15%" band wants. The cascade rate falls among calm fitted rulers, to zero for the calm fully equipped ones (above).
- **"One terminal per 10 Neurofractured rulers per decade":** untouched (Neurofractured is not affected).
- **Observer run (balance §9.2) gains two counters per decade:** (1) cultures with the innovation, and AI rulers fitted; (2) the Overclocked→cascade median for fitted and unfitted rulers. Add a third counter: AI Overclocked rulers holding all three wear rows, and how many of them cascaded. **Tuning knobs, if the human wants them later:** the self-repair row (−3 → −2), or a `min` on `eotg_aug_oc_wear_relief_value`. Each is one number.

### 4.4 The refit: decision and provider event

**`eotg_decision_aug_self_repair`** (shape: `eotg_decision_seek_augmentation`; vanilla `common/decisions/00_lifestyle_decisions.txt:342`, a decision with no cost that fires a paying hub event):

| Field | Value |
|---|---|
| `picture` | placeholder, the Maintenance Protocol art (§3.1) |
| `selection_tooltip` | `eotg_decision_aug_self_repair_selection_tt` |
| `ai_check_interval_by_tier` | barony 0, county 0, duchy 36, kingdom 24, empire 24, hegemony 24 (Seek's: counts are offered, they never seek; balance §5.2/§5.3) |
| `is_shown` | `eotg_aug_can_self_repair = yes` |
| `is_valid` | `custom_description = { text = eotg_decision_aug_self_repair_no_provider_tt  OR = { eotg_aug_clinic_open = yes  eotg_aug_has_surgeon_access = yes } }`. Gold floor at the cheapest provider: `OR = { eotg_aug_can_afford_procedure = { BASE = eotg_aug_self_repair_price_value  MULT = 1 }  AND = { eotg_aug_has_surgeon_access = yes  eotg_aug_can_afford_procedure = { BASE = eotg_aug_self_repair_price_value  MULT = eotg_aug_price_mult_physician } } }` |
| `cooldown` | `{ years = 1 }` (decision-owned, index §1 rule 5; covers "Not yet") |
| `effect` | `custom_tooltip = eotg_decision_aug_self_repair_tooltip`; `trigger_event = eotg_aug_proc.005` |
| `ai_potential` | `eotg_aug_can_self_repair = yes`; `short_term_gold >= { value = eotg_aug_self_repair_price_value  multiply = eotg_aug_price_mult_physician }` |
| `ai_will_do` | base 5; +25 `eotg_is_aug_tier3 = yes`; +20 `eotg_aug_has_countdown = yes`; +10 diligent; +10 `education_learning_3` or better; −15 greedy; −10 lazy |

**`eotg_aug_self_repair_price_value`** = `massive_gold_value` × 2. That is about 36 months of income (vanilla `massive_income_multiplier_value = 18`, `00_basic_values.txt:455`): 3× the Overclocked upgrade (`major_gold_value`, 12 months) and 6× the Enhanced upgrade (`medium_gold_value`). Physician / technician routes pay it × `eotg_aug_price_mult_physician` (0.75, or 0.6 with a technician, realm §3.2).

**No back streets and no self-surgery.** The hardware comes from the scholars' workshops, and fitting it takes a team. No cheap copy exists yet. This also means the severe tail and death on the table **cannot** happen on this procedure: the clinic and physician columns weigh them 0 (procedures §4.2, DoD 5).

#### proc.005 *Within Tolerance*
- `character_event`, `events/eotg_augmentation_procedures.txt`, namespace `eotg_aug_proc`.
- **Fired by:** `eotg_decision_aug_self_repair` only.
- **Trigger** (world-state guard; no cooldown read): `eotg_aug_can_self_repair = yes`.
- **Immediate:** `eotg_aug_save_surgeon_effect = yes`.
- **Desc:** base, plus `desc_overclocked` (`eotg_is_aug_tier3 = yes`: the deepest hardware wears fastest, and this is what it is for), plus `desc_surgeon` (`eotg_aug_has_surgeon_access = yes`).
- **Paid options run, in order:**
  1. `eotg_aug_pay_procedure_effect = { BASE = eotg_aug_self_repair_price_value  MULT = … }`;
  2. `eotg_aug_self_repair_fit_effect = yes` (adds the modifier: shown by the engine; then risk +2 / +4 / +6 by tier in `hidden_effect`);
  3. `save_scope_value_as = { name = eotg_proc_refit  value = yes }`;
  4. `hidden_effect = { eotg_aug_procedure_effect = { PATIENT = root  PROVIDER = …  PROCEDURE = upgrade  SURGEON = … } }`;
  5. `custom_tooltip = eotg_aug_proc.005.tt`;
  6. `eotg_aug_stress_surgery_effect = yes` (one stress helper per paid option, as proc.003).
- **Why `PROCEDURE = upgrade`.** A fifth procedure literal would touch every `upgrade` row in the roll and the apply effect. The refit *is* deep work on fitted hardware, so the upgrade rows apply as they stand: infection and rejection ×2, rejection reads as "complication" (risk +10, infection 1 year). Only the proc.002 opener differs, through `scope:eotg_proc_refit` (saved scope values travel with `trigger_event`, procedures §4.1 rule 2).
- **The fit applies on the click,** as the Overclocked upgrade's XP does in tier2.003. The roll's outcome (a complication or an infection; *discovered* under a Ban, realm §3.2) is applied at the reveal as usual. A clean or flawed outcome is silent (procedures §4.1 rule 3).

| Opt | Text intent | Trigger | Provider / price | ai_chance |
|---|---|---|---|---|
| a | "The clinic." | `eotg_aug_clinic_open = yes`; afford ×1. `show_as_unavailable = { eotg_aug_clinic_open = no }` with `eotg_aug_clinic_closed_tt` (realm §3.2, vanilla `tournament_events.txt:4496`) | clinic ×1, `SURGEON = root` | 40; +20 diligent; +10 craven; −20 greedy |
| b | "My own physician." / name variant `eotg_aug_opt_technician` when `eotg_aug_surgeon_is_technician = yes` (realm §3.2) | `eotg_aug_has_surgeon_access = yes`; afford × `eotg_aug_price_mult_physician` | physician × that mult, `SURGEON = scope:eotg_proc_surgeon` | 40; +20 trusting; +10 diligent |
| c | "Not yet." | — | — | 15; +20 greedy; +10 content |

No trait-gated option. This is a purchase point like proc.001, and index §1 rule 6 allows 0–2. A trait option would add loc for no new decision.

### 4.5 Lifecycle of the modifier

| Event in the character's life | Modifier | Why |
|---|---|---|
| Partial removal, Overclock regression | **kept** | The refit services the hardware that stays. Neither path calls `eotg_clean_all_aug_modifiers`. |
| Cascade to Neurofractured | **kept, inert** | §4.3: no reader at Neurofractured. |
| Full exit (Remove Implants, Excision, Rejection, nr.006, retinue reversal) | **removed** | `eotg_aug_remove_all_effect` → `eotg_clean_all_aug_modifiers`. It came out with the rest. A later re-entry pays again. |
| Total Integration | **removed** | `eotg_aug_total_integration_effect` → `eotg_clean_all_aug_modifiers`. Seamless has no risk to slow. |
| **proc.004 *A Part Replaced*** | **unchanged** | Lore N1 (rationale restated by U3): self-repairing machinery makes no part, so the Seamless repair is ordered parts and booked technicians, **even if the culture has the innovation**. No desc variant. |

**Not affected by the refit:** the syndicate's firmware throttle (reprisal), a tamper (`eotg_flag_aug_sabotaged`, interactions), the hidden flaw (`eotg_flag_aug_hidden_flaw`, thread T6), infections. Each is a fault that someone made or bought, not wear.

### 4.6 On_actions

No new on_action. The two accrual edits sit inside existing custom on_actions on `yearly_playable_pulse` (index §2). The decision is player- or AI-clicked. proc.005 is fired only by the decision, and proc.002 only by `eotg_aug_procedure_effect`. Cooldown authority: the decision's `cooldown` block, nowhere else.

### 4.7 Dependencies on unbuilt specs (why this is last)

| Needs | From | If it slips |
|---|---|---|
| `eotg_aug_procedure_effect`, `eotg_aug_save_surgeon_effect`, pricing helpers, proc.002, `events/eotg_augmentation_procedures.txt` | procedures | **Hard dependency.** Do not build this spec first. |
| `eotg_aug_clinic_open`, `eotg_aug_has_surgeon_access`, `eotg_aug_surgeon_is_technician`, `eotg_aug_opt_technician`, `eotg_aug_clinic_closed_tt`, conditional `eotg_aug_price_mult_physician`, the technician accrual rows | realm | **Hard dependency** in the order given. Only if the human reorders the queue: use `eotg_has_physician_access` in place of surgeon access, drop the clinic gate and its unavailable state, and leave the technician line out of the relief value. Record that as a follow-up for when realm lands. |
| (nothing) | interactions, reprisal | Order only: shared files. |

---

## 5. File placement

| Path | What |
|---|---|
| `common/culture/innovations/eotg_innovations.txt` | **new file, new folder for the mod**: `eotg_innovation_self_repairing_machinery`. UTF-8 with BOM (as vanilla's). **No `replace_path`** (vanilla innovations stay). The orchestrator adds `common/culture/innovations/` to the `CLAUDE.md` placement table. |
| `common/decisions/eotg_augmentation_decisions.txt` | the new decision; Maintenance and Consult edits |
| `events/eotg_augmentation_procedures.txt` | proc.005; proc.002 opener |
| `common/modifiers/eotg_augmentation_modifiers.txt` | `eotg_mod_aug_self_repair` |
| `common/scripted_effects/eotg_augmentation_effects.txt` | `eotg_aug_self_repair_fit_effect`; the clean-up line |
| `common/scripted_triggers/eotg_augmentation_triggers.txt` | `eotg_aug_can_self_repair` |
| `common/script_values/eotg_augmentation_values.txt` | `eotg_aug_self_repair_price_value`, `eotg_aug_oc_wear_relief_value` |
| `common/on_action/eotg_augmentation_on_actions.txt` | the two accrual edits; the header's resource notes |
| `localization/english/eotg_augmentation_l_english.yml` | §7 (the innovation keys may live here; one definition per key) |

---

## 6. Vanilla precedent

All under `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/`.

| Mechanism | File:line | Used for |
|---|---|---|
| Innovation fields; `unlock_decision` is tooltip-only; key-as-loc plus `_desc` | `common/culture/innovations/_culture_innovations.info:11-30, 75-79, 100-114` | §4.1 |
| A learning, civic, early-medieval innovation with no regional gate | `common/culture/innovations/00_early_medieval_innovations.txt:409-433` (`innovation_armilary_sphere`) | the definition's shape and icon |
| AI fascination × 0 until the culture is in the era | `00_early_medieval_innovations.txt:58-68` | `ai_weight_for_fascination` |
| A `can_progress` prerequisite on a later-era innovation | `common/culture/innovations/tgp_innovations.txt:151-153` | option C |
| Era years and the era gate | `common/culture/eras/00_culture_eras.txt:2-11, 39-44, 83-88`; `_culture_eras.info:2, 12` | the gating options |
| Ahead-of-time and fascination defines | `common/defines/00_defines.txt:1194-1233` | the gating options; §9 |
| Vanilla cultures at 867 are tribal; most join early medieval in 950 | `history/cultures/greek.txt:3-24` | option B's timing |
| `culture = { has_innovation }` from character scope; the liege variant | `common/buildings/00_city_buildings.txt:459-461`; `common/decisions/30_activity_decisions.txt:767-768`; `common/court_positions/types/00_court_positions.txt:5949-5950` | §4.2 |
| `add_innovation` in culture scope | `events/decisions_events/roman_restoration_events.txt:2575-2584` | tests (§9) |
| The flag the vanilla achievement counts | `common/achievements/standard_achievements.txt:923` | the mod-only flag |
| Gold scale | `common/script_values/01_dynamic_values.txt:93-192`; `00_basic_values.txt:454-455` | the price |
| A decision with no cost that fires a paying event | `common/decisions/00_lifestyle_decisions.txt:342` | the decision |
| `min` in a script value; a script value as an effect operand | `01_dynamic_values.txt` (every `*_gold_value`); `common/scripted_effects/00_laamp_effects.txt:1247` | `eotg_aug_oc_wear_relief_value` |
| Unavailable option with a reason | `events/activities/tournaments/tournament_events.txt:4496` (via realm §3.2) | proc.005.a |

---

## 7. Loc surface (eotg-localizer)

**Binding renderings:** [cybernetics_v2_self_repair_lore.md](cybernetics_v2_self_repair_lore.md) (eotg-lore-keeper, 2026-10-04, approved with S1–S7). Where it gives a rendering, the localizer uses it, polishing only within the rules below. The briefs in the table are a fallback.

**Names (fixed by the review):**
- innovation: **"Self-Repairing Machinery"**;
- decision: **"Commission Self-Repairing Hardware"**;
- modifier: **"Self-Repairing Hardware"**;
- proc.005: **"Within Tolerance"**.

**General rules:**
- index §5 items 1–8, plus the never-name list (index §5.3 and its extensions in the procedures, realm and reprisal lore files);
- US spelling; bare `[x.GetName]`; appended lines start with `\n\n`;
- **no number, and no "risk", "odds" or "chance"** in any tooltip or desc (the hidden rule). The engine's own modifier tooltip shows `health`; nothing else is quantified.

**The hardware's register.** With the hardware as subject, never:
- **S1.** fabricate, print, build or make (a part), order, requisition, send for, copy, replicate. It never makes or orders a part.
- **S6.** notices, senses, heals, feels, knows, alive, living, instinct, organic. It **measures** its wear.
- **Q3.** grows, learns, wants, decides. The passive "How it goes is decided on the table" is allowed. Say nothing about arcana either way.
- No swarm, nanite(s) or colony. No voice or speaker in the hardware.

**S2: the log.** Its record is read **at the panel, by hands**. Never "alert", "message", "notifies", "tells you", "reports to you", or an overlay readout.

**S3: whose scholars.**
- The innovation's `_desc` and `_custom` are descriptive with no possessive, so they read true before the research is done.
- "Our scholars" appears only in decision and event text.
- Never "the realm's", the court's or the ruler's scholars.
- Never "programme", "state", "decree", "subsidy" or "issued".

**S4: date-free.** Never:
- the Gnomish Technocracy, Gnomes as the inventors, the year 975, any named nation, school or authority;
- first, "the first to", "before anyone", "ahead of its time", "only we", secret;
- "new age", "new era", renaissance, "golden age", "rogue scholars", "from across the galaxy";
- Council of Innovation, Technarch, technomagic, Core Purity Doctrine.

**S7: no promises.** Loc may say calibration holds longer and the hardware stays in tolerance. Never safer, protects, prevents, "slows the cascade", fracture, or "a longer life".

Also: the banned list of index §5.2.

| Keys | Count | Brief (fallback; the lore file's renderings bind) |
|---|---|---|
| `eotg_innovation_self_repairing_machinery`, `_desc` | 2 | "Self-Repairing Machinery". Desc: mechanisms that measure their own wear and correct it; they cannot make a part. No possessive (S3). |
| `eotg_innovation_self_repairing_machinery_custom` | 1 | "Augmented characters of this culture can have self-repairing hardware fitted." |
| `eotg_decision_aug_self_repair`, `_desc`, `_tooltip`, `_confirm`, `_selection_tt`, `_no_provider_tt` | 6 | "Commission Self-Repairing Hardware". Desc: our scholars' hardware keeps itself in tolerance; calibrating less often; the price is ruinous. |
| `eotg_mod_aug_self_repair`, `_desc` | 2 | "Self-Repairing Hardware". Desc: it measures its own wear and holds its calibration longer; you are another matter. |
| `eotg_aug_proc.005.t`, `.desc`, `.desc_overclocked`, `.desc_surgeon`, `.a`, `.b`, `.c`, `.tt` | 8 | .t "Within Tolerance". .a "The clinic." .b "My own physician." (the technician variant reuses `eotg_aug_opt_technician`). .c "Not yet." |
| `eotg_aug_proc.002.desc_refit` | 1 | Its record, read at the panel, already shows the first fault it found and corrected (S2). |
| **Total** | **20 new, 0 revised** | |

No vanilla string needs a `replace/` override. The Maintenance and Consult tooltips are unchanged: the engine shows the modifier's new duration itself.

---

## 8. Lore constraints

**Lore review: done** (eotg-lore-keeper, 2026-10-04, [cybernetics_v2_self_repair_lore.md](cybernetics_v2_self_repair_lore.md)). Approved with must-fixes S1–S7, all folded in (§4.3, §7, §9, §10).

- **ERRATA, CYBERNETICS AT 866 (2026-10-04; sub-bullet refined by the review):**
  - Self-repairing machinery does not exist at 866. It is researchable by a culture's scholars, and only then can its hardware be fitted.
  - A self-repairing unit adjusts, re-seats, reroutes and records. **It never makes a part.**
  - This spec gates the hardware on the innovation. Nothing exists before it.
- **S5: nothing has it at 866.1.1.**
  - No `history/cultures` grant of the innovation.
  - No bookmark or history character carries the modifier (DoD 2).
  - Note for the cartographer at Gate 1: **CB-36**.
- **Future tech not built:** remote kill (Blackstar, 1300), state programmes (New Cauldron, 1610), uploads, datavaults, secretariats (c. 1825). None is here. The innovation is not a programme (§1).
- **Tech ceiling** (procedures lore (c)): no self-replicating repair. **Ruled (Q1):** "self-repairing" stands, and "replicating" is banned in loc.
- **Procedures lore N1:** its rationale is restated by U3 in [cybernetics_v2_procedures_lore.md](cybernetics_v2_procedures_lore.md). proc.004 is ordered parts either way.
- **Never name** the Gnomish Technocracy or the Mechanized Renaissance, nor the index §5.3 implant players (S4).
- **Culture gate accepted (U1):** the scholars belong to a culture. There is no liege read.
- **Voice register** (index §5.1–2): the hardware has no voice and gives the voice nothing new. A Neurofractured character's modifier desc must not suggest the hardware is fighting, helping or answering them.
- **Seamless:** A Part Replaced (proc.004) is separate and unchanged. The modifier is removed at Total Integration (U2).
- **Multi-species:** "self", never "humanity" (index §5.5).
- **Alternate timing (Q4):** a culture reaching the advance before 975 is alternate history, not a contradiction, provided nothing has it at 866.1.1 (S5). The loc is date-free and culture-agnostic (S3, S4).
- **Nikios Khanate:** not touched.

---

## 9. Definition of done

0. **Tiger, `px_lsp_diagnostics.js`, `px_vocab_check.py`** clean on the touched files, except the `CLAUDE.md` known-benign list.
   - Tiger 1.17 targets 1.18.3. Check any finding on the innovation file against `_culture_innovations.info` and `00_early_medieval_innovations.txt` before treating it as real.
1. **Reachability (PX event graph):** proc.005 from `eotg_decision_aug_self_repair`. proc.002 (with `desc_refit`) from `eotg_aug_procedure_effect`.
2. **Gating:**
   - `grep -rn "eotg_innovation_self_repairing_machinery" common` finds only the innovation, `eotg_aug_can_self_repair`, and the decision's `unlock_decision` line;
   - `eotg_aug_can_self_repair` is the only `has_innovation` test;
   - **S5:** `grep -rn "eotg_innovation_self_repairing_machinery\|eotg_mod_aug_self_repair" history common/bookmarks` returns nothing;
   - no culture, title, faith or province key anywhere in the change.
3. **Cooldown authority:** the decision's `cooldown = { years = 1 }` is the only cooldown. proc.005's trigger reads no flag. `eotg_flag_maintenance_cooldown` is still 3 years.
4. **Package bounds:**
   - `eotg_mod_aug_self_repair` is read only in `eotg_aug_oc_wear_relief_value`, the non-ruler Overclocked row, Maintenance, Consult, `eotg_aug_can_self_repair`, and the clean-up line;
   - no Neurofractured or Seamless event or on_action reads it;
   - `eotg_aug_oc_wear_relief_value` has **no** `min` (no cap, human 2026-10-04);
   - the Overclocked check has no separate vendor-safe or technician row left;
   - the technician values are the realm spec's, unchanged.
5. **Severe tail:** proc.005 calls the roll only with `PROVIDER = clinic` or `physician`.
6. **Coupling (QA audit 8):** proc.005 a/b call `eotg_aug_self_repair_fit_effect` (risk) and the roll.
7. **Hidden rule:** no new tooltip or desc contains a number or "risk", "odds" or "chance". All risk moves are in `hidden_effect`.
8. **Loc:**
   - all §7 keys exist exactly once, with BOM and no `[scope:`;
   - **S4 grep:** `grep -rniE "gnom|technocra|technarch|renaissance|golden age|council of innovation|technomag|975|replicat|nanite|swarm|before anyone|ahead of its time|the first to"` over the new keys is empty;
   - a reviewer reads the 20 keys against the S1, S2, S6 and S7 word lists in §7. Those lists have hardware-as-subject conditions, so they are not grep-clean.
9. **Human, in game (temporary map, vanilla cultures):**
   - The culture window lists the innovation in the civic group, early medieval column, for any culture. Its tooltip shows the decision unlock and the custom line.
   - **Engine check:** from a tribal-era culture at the start, the player can choose it as the **fascination** (ahead of time), and it shows progress. Note the rate the UI shows, and the rate for an in-era innovation (T). If the ahead-of-time choice is not offered, report it: option B then behaves like C.
   - Console (player scope) `effect = { culture = { add_innovation = eotg_innovation_self_repairing_machinery } }`. Then the decision appears for an augmented character, and not for an unaugmented, Neurofractured or Seamless one. It disappears once fitted.
   - Clinic route: gold drops by the full price and the modifier appears. Reload until a bad outcome: proc.002 opens with `desc_refit`. Physician route: cheaper price. With a technician (after realm) the option reads "My implant technician."
   - Under a Ban (realm): the clinic option is greyed with its reason. With no physician or technician, the decision is invalid with `_no_provider_tt`.
   - Maintenance, with the modifier: Calibrated Systems for 5 years. Consult: 7.
   - Overclocked, calm, fitted (`var:eotg_fracture_risk` before and after the yearly pulse):
     - no vendor flag, no technician: rises 9 a year (12 unfitted);
     - with vendor-safe as well: 6;
     - with vendor-safe and an excellent technician: 3.
   - Remove Implants: the modifier is gone. Total Integration: the modifier is gone, and A Part Replaced still reads as before.
10. **Observer run (balance §9.2):** the three counters in §4.3 are recorded.

---

## 10. Deferred

- **Option C's prerequisite and option A's era.** Not built (the human picked B, 2026-10-04); one line each if testing shows B too fast or too slow.
- **A cap on stacked Overclocked relief.** Not built (human, 2026-10-04). If the observer run shows fully equipped AI rulers never cascading, a `min` on `eotg_aug_oc_wear_relief_value` is a one-line change (§4.3).
- **Gate 1 coupling (taskboard CB-36):**
  - Move the innovation one era up if the mod's 866 cultures start in the early medieval era, and re-point the era keys if v2 replaces the eras (§4.1 rule).
  - **S5:** the cartographer's `history/cultures` must not grant the innovation, and no bookmark or history character may carry `eotg_mod_aug_self_repair` (DoD 2 grep).
- **Buying from a foreign culture** (a patient whose culture lacks the innovation, buying from one that has it, at a premium). Cut: it needs a cross-culture provider scope, and the fiction of traders and imports needs a lore pass.
- **Back-street copies** once the advance has spread. Cut: a cheap, unreliable copy is a good later beat, but it reopens the severe tail and needs its own weights.
- **Offering the refit to others** (the interactions spec's Offer Augmentation) and **Borrow Their Technician** fitting it. The roll already takes `PATIENT`, so this is an option row later.
- **Curing the hidden flaw, a tamper or the syndicate's throttle by refit.** Cut on purpose (§4.5): each is a fault someone made or bought, and each belongs to a story thread (T6, interactions, reprisal).
- **An announcement event when the culture discovers it.** Vanilla has no hook for it (§4.1) and already notifies discoveries. A yearly culture-pulse poll would be a vignette.
- **Bespoke art** for the innovation icon, the modifier icon and the decision picture. Stopgaps are named (§3.1). Human debt; not blocking.
- **The other future techs** (remote kill, programmes, uploads): canon says not at 866. Not built.

---

### HANDOFF
- status: done
- next: eotg-scripter (when the queue reaches it: after procedures → interactions → realm → reprisal)
- ask: Build docs/specs/cybernetics_v2_self_repair.md §3–§5: option B gating; price massive_gold_value × 2; the wear-relief value with NO cap; the realm technician values unchanged. Run the three validators, then hand §7 to eotg-localizer, who uses docs/specs/cybernetics_v2_self_repair_lore.md renderings. Then eotg-qa runs §9.
- files: docs/specs/cybernetics_v2_self_repair.md (S1–S7, names, human decisions folded in); docs/specs/cybernetics_v2_procedures_lore.md (N1 rationale restated, U3)
- needs-loc (20, §7; binding renderings in docs/specs/cybernetics_v2_self_repair_lore.md): eotg_innovation_self_repairing_machinery (+_desc, _custom); eotg_decision_aug_self_repair (+_desc, _tooltip, _confirm, _selection_tt, _no_provider_tt); eotg_mod_aug_self_repair (+_desc); eotg_aug_proc.005.t/.desc/.desc_overclocked/.desc_surgeon/.a/.b/.c/.tt; eotg_aug_proc.002.desc_refit
- needs-lore: none (review done; S1–S7 folded in)
- needs-human: (a) acknowledge §4.3's stated consequence of no cap: a calm, fully equipped Overclocked ruler who keeps Maintenance up never cascades and never reaches the Countdown; (b) the orchestrator adds `common/culture/innovations/` to the CLAUDE.md placement table; (c) the §9 item 9 in-game checks, especially whether a later-era innovation can be chosen as the fascination
