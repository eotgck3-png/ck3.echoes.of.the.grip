# Spec: Void Corruption v2 (a port of v1's Void, with fixes)

**Author:** cloud session, 2026-11-03 (orchestrator brief, Part G). **Status:** built, unvalidated. Next: Tiger + PX locally, then eotg-lore-keeper (§8, the loc), then owner rulings (§11).
**Sources:** `docs/qa/v1_lift_readiness_cloud.md` §2 "V." and §6; `OLD VERSION CATALOG.md` §2.3 and §4; v1 `OLD PROJECT VERSION/events/eotg_void_*.txt`, `OLD PROJECT VERSION/common/*/eotg_void_*`, the hub block in `OLD PROJECT VERSION/common/on_action/eotg_on_actions.txt:74-84`, `eotg_traits.txt:10-40`, `eotg_modifiers.txt:7-14`, and `localization/english/eotg_void_l_english.yml`.
**Canon:** SETTING LORE ERRATA (ORRIN 2026-08-29; CYBERNETIC "VOICE" 2026-10-03; YU 2026-10-04) and `docs/lore/REVIEW_866.md:35,64`.
**Supersedes, where they differ:** the proposal `docs/specs/void_lift_plan_cloud.md` (2026-10-04). Its §3(d) recommended "the trait is the resource" for stage D and §3(e) left Voidwalkers open; the orchestrator rulings R8 and R4 below decide both. Its open questions 2, 4, 5, 6, 8 and 9 are answered by R4, §8.1 (the text says "the scar" and never "the seal"), R4 (no Elrossi, no hunt spans), R7 and R8.
**Scope:** the 15 v1 events and their options, the v1 decisions, traits, modifiers and opinions. **No new events and no new options.** New script objects are limited to what the rulings require: the stage-D variable and its two band modifiers, the Voidwalker template, and helper effects.

---

## 0. Kind of build

**A mod-exclusive system, port with fixes.** Void Corruption depends on no title, province, culture or faith (the faith check is one inert trigger, R3), so it survives the map swap. Like cybernetics, it can be built before Gate 1 closes; the owner still has to designate it mod-exclusive (`v1_lift_readiness_cloud.md` §6 correction 3, owner question Q1).

The core verb: **an outside pressure accumulates on a ruler; the ruler pushes it back (wards, piety, a Voidwalker) or trades with it (insight, dread), until it either recedes or finishes passing through them.**

---

## 1. Purpose & gate

- **Purpose.** The v1 system was complete on paper and never ran (it sat on the dead `on_yearly_playable` hook). v2 makes it run, fixes the six HIGH rows of the readiness audit, and brings the text into canon and the v2 voice rules.
- **Gate.** Mod-exclusive exemption (CLAUDE.md, decided 2026-10-02). Pending the owner's designation (Q1).

---

## 2. Signature resources

| Variable | Range | Stage | Writer (the only one) | Readers |
|---|---|---|---|---|
| `eotg_void_exposure` | 0–100 | A–C, pinned at 100 in D | `eotg_void_change_exposure_effect` | stage triggers, bands, on_action, decisions |
| `eotg_void_hollowing_depth` | 0–100 | D only | `eotg_void_change_hollowing_depth_effect` | depth bands, the 0031/0032 pool weights |

Both writers create the variable at 0 if missing, clamp to 0–100, and refresh their band. Every AMOUNT is a literal or a named script value (`eotg_void_values.txt`); an inline `{ }` block is not valid as `$AMOUNT$`.

---

## 3. Stages and the state machine

### 3.1 Exposure bands (single owner: `eotg_void_refresh_band_effect`)

| Exposure | Band modifier | Loc name |
|---|---|---|
| 0–24 | none | |
| 25–49 | `eotg_mod_void_whispers` | Void Whispers |
| 50–74 | `eotg_mod_void_pressure` | Void Pressure |
| 75–100 | `eotg_mod_void_saturation` | Void Saturation |

The Hollowed carry no exposure band. "Pressure" stays a Void word; cybernetics keeps "static" (R7).

### 3.2 Stages

```
            seed (0001, 0024.a heir, Commune)
                 |
   [0] unseeded --+--> [A] exposure >= 25, no trait: whispers 0002 / 0003
                         |
                         v
                  [B] exposure >= 50, not Defiant: the Bargain 0010
                         |  a: accept ------------------------------+
                         |  b: refuse -> Void-Defiant (-25, ward 10y)|
                         |  c/d: stay in B, exposure up            |
                         v                                         |
                  [B!] exposure >= 75, Defiant or not: Taken Anyway 0011 (forced Touched)
                                                                   |
                                                                   v
                  [C] Void-Touched: 0020-0025 (one roll a year)
                         |
                         | exposure reaches 100 (accrual +6/yr while Touched)
                         v
                  [D] Hollowed (0030, forced): exposure pinned at 100,
                      depth starts at 25, drifts +4/yr; 0031 / 0032
```

- **Wards** (decisions, 0001.a, 0004.b, 0011.b, 0021.a on the child, 0022.a) cut exposure and run `eotg_mod_void_warded`; a new ward replaces a running one.
- **Defiance** removes the Bargain (stage B) but not Taken Anyway (B!). v1's comment said otherwise; the behaviour was always this, and 0011's text is written for it.

### 3.3 Yearly accrual (`eotg_void_yearly_accrual_value`, v1's terms, written once)

Applies to `eotg_void_susceptible` (landed, not Hollowed, and one of: Grip Survivor, Touched, cult faith, a Touched character near, seeded).

| Term | Amount |
|---|---|
| base | +2 |
| `eotg_grip_survivor` | +3 |
| cult faith (inert, R3) | +5 |
| a Touched courtier, vassal or spouse | +4 |
| Touched | +6 |
| stress 200+ | +4 |
| lunatic or possessed | +4 |
| age 60+ | +2 |
| Void-Defiant | −4 |
| warded | −5 |
| learning education | −3 |
| a Voidwalker at court | −6 |
| piety level 3+, not cult | −3 |

v1 called the change effect up to 13 times a year, each refreshing the band; v2 sums and writes once.

### 3.4 Stage D: Hollowing depth (R8)

- Starts at `eotg_void_hollowing_start_value` (25) inside `eotg_void_become_hollowed_effect`.
- Drifts `eotg_void_hollowing_drift_value` (+4) a year in the on_action.
- Every option of 0030, 0031 and 0032 moves it: the "power" options deepen it (+5 to +15), the "presence" options pull it back (−5 to −20).
- **Bands:** `eotg_mod_void_hollow_far` (50+, "Far Off": opinion −5, dread baseline +5), `eotg_mod_void_hollow_quiet` (85+, "Gone Quiet": opinion −10, dread baseline +10, stress gain −25%).
- **Pool tilt:** 0031 weight 45, +20 at depth 50+; 0032 weight 15, +15 below 50. Being far gone makes the court adapt; being near makes moments of being come back.

### 3.5 The yearly on_action (`eotg_on_yearly_void_check`, on `yearly_playable_pulse`)

1. accrual (exposure), then depth drift;
2. the Hollowing, forced, ignoring the cooldown (as v1);
3. one roll by stage: D (0031/0032) › C (0020–0025, triggered `random_list`) › B! (0011, 75%) › B (0010, 50%) › A (0002 40 / 0003 35 / nothing 25) › contact (0001, 4%, unseeded only);
4. the Voidwalker at the gate (0004, 12%) only if step 3 fired nothing.

**Cooldown authority** is the on_action alone: each branch sets `eotg_flag_void_event_cooldown` at fire time for v1's per-event duration (0001 3y, 0002 3y, 0003 4y, 0004 5y, 0010 5y, 0011 5y, 0020 3y, 0021 4y, 0022 3y, 0023 4y, 0024 5y, 0025 3y, 0030 5y, 0031 3y, 0032 6y). v1 set it in each event's immediate, days later, so 0004 could fire in the same pulse as a whisper.

---

## 4. Identifier table

### 4.1 Script objects

| v2 identifier | Type | v1 name (plain text) | Change |
|---|---|---|---|
| `eotg_on_yearly_void_check` | on_action | on_yearly_void_check + 5 sub-hooks | one effect, `yearly_playable_pulse` (R1) |
| `eotg_void_change_exposure_effect` | effect | se_void_add_exposure | single writer |
| `eotg_void_change_hollowing_depth_effect` | effect | none | NEW (R8) |
| `eotg_void_refresh_band_effect` | effect | se_void_refresh_band | guarded adds; Hollowed carry none |
| `eotg_void_refresh_depth_band_effect` | effect | none | NEW (R8) |
| `eotg_void_remove_modifier_effect` | effect | none | NEW helper (lint L005) |
| `eotg_void_seed_effect` | effect | se_void_seed | through the writer |
| `eotg_void_become_touched_effect` | effect | se_void_become_touched | aura guarded |
| `eotg_void_become_defiant_effect` | effect | se_void_become_defiant | ward replaced, not stacked |
| `eotg_void_become_hollowed_effect` | effect | se_void_become_hollowed | exposure through the writer; depth starts |
| `eotg_void_insight_effect` | effect | se_void_edu_insight | one Insight per character (guard) |
| `eotg_void_add_ward_effect` | effect | none | NEW helper, `$YEARS$` |
| `eotg_void_warding_rite_effect` | effect | se_void_ward | |
| `eotg_void_voidwalker_ward_effect` | effect | inline in the v1 decision | |
| `eotg_void_create_voidwalker_effect` | effect | none | NEW (R5) |
| `eotg_void_shelter_voidwalker_effect` | effect | se_void_shelter_voidwalker | seats the courtier (bug fix) |
| `eotg_void_step_down_effect` | effect | none | NEW (R9, 0030.c) |
| `eotg_void_is_cult_faith` | trigger | st_void_venerates | `always = no` (R3) |
| `eotg_void_has_exposure` | trigger | st_void_has_exposure | |
| `eotg_void_near_touched` | trigger | st_void_near_touched | |
| `eotg_void_susceptible` | trigger | st_void_susceptible | |
| `eotg_void_has_voidwalker` | trigger | st_void_has_voidwalker | |
| `eotg_void_whisper_stage` | trigger | st_void_whisper_stage | |
| `eotg_void_bargain_ready` | trigger | st_void_bargain_ready | |
| `eotg_void_saturated` | trigger | st_void_saturated | comment fixed |
| `eotg_void_hollowing_ready` | trigger | st_void_hollowing_ready | |
| `eotg_void_can_be_warded` | trigger | st_void_can_be_warded | comment fixed |
| `eotg_void_event_ready` | trigger | st_void_event_ready | read by the on_action only |
| `eotg_void_has_any_insight` | trigger | none | NEW (guard) |
| `eotg_void_yearly_accrual_value` | script value | se_void_yearly_accrual | summed |
| `eotg_void_hollowing_start_value` | script value | none | NEW (R8) |
| `eotg_void_hollowing_drift_value` | script value | none | NEW (R8) |
| `eotg_grip_survivor` | trait | same | lifted (R2), inert |
| `eotg_void_touched` | trait | same | |
| `eotg_void_defiant` | trait | same | |
| `eotg_void_hollowed` | trait | same | |
| `eotg_mod_void_whispers` | modifier | same | |
| `eotg_mod_void_pressure` | modifier | same | name kept (R7) |
| `eotg_mod_void_saturation` | modifier | same | |
| `eotg_mod_void_hollow_far` | modifier | none | NEW (R8) |
| `eotg_mod_void_hollow_quiet` | modifier | none | NEW (R8) |
| `eotg_mod_void_warded` | modifier | same | |
| `eotg_mod_void_aura` | modifier | same | desc added |
| `eotg_mod_void_deep_charts` | modifier | same | |
| `eotg_mod_void_unseen_step` | modifier | same | |
| `eotg_mod_void_cold_hand` | modifier | same | |
| `eotg_mod_void_long_ledger` | modifier | same | |
| `eotg_mod_void_borrowed_voice` | modifier | same | |
| `eotg_opinion_void_unreachable` | opinion | opinion_void_revulsion | renamed (R10) |
| `eotg_opinion_void_shelters_voidwalker` | opinion | opinion_void_harbors_heretic | renamed (R4) |
| `eotg_opinion_void_unease` | opinion | same | |
| `eotg_opinion_void_kinship` | opinion | same | belief-framed name (R6) |
| `eotg_opinion_void_defiance_respect` | opinion | same | neutral name (R6) |
| `eotg_decision_void_warding_rite` | decision | same | v2 shape |
| `eotg_decision_void_voidwalker_ward` | decision | same | now reachable |
| `eotg_decision_void_commune` | decision | same | inert (cult); `cooldown` block |
| `eotg_void_voidwalker_template` | character template | none | NEW (R5) |
| `eotg_flag_void_seeded` | flag | same | |
| `eotg_flag_void_voidwalker` | flag | same | on the courtier now |
| `eotg_flag_void_event_cooldown` | flag | same | set in the on_action only |
| `eotg_flag_void_ward_cooldown` | flag | same | shared by two decisions |
| `eotg_void_voidwalker` | saved scope | none | 0004 |
| `eotg_void_child` | saved scope | void_child | prefixed |
| `eotg_void_confessor` | saved scope | void_confessor | prefixed |
| `eotg_void_vassal` | saved scope | void_vassal | prefixed |
| `eotg_void_successor` | saved scope | none | step-down |

### 4.2 Not lifted (pruned)

flag_void_bargain_offered (set, never read); flag_void_commune_cooldown (the decision's `cooldown` block replaces it); st_is_void_hollowed, st_void_rift_contact, st_void_resists (no callers); the trait flags flag_void_corruption, flag_void_defiance, flag_grip_bloodline (no readers); se_void_init_exposure (folded into the writer); se_apply_void_corruption and se_remove_void_corruption (v1 `eotg_scripted_effects.txt:10-26`; no callers; bypassed the state machine).

### 4.3 Events

Namespace `eotg_void`. Files: `events/eotg_void_whispers.txt` (0001–0004, 0010, 0011), `events/eotg_void_touched_events.txt` (0020–0025), `events/eotg_void_hollowing.txt` (0030–0032). All 15 are fired by `eotg_on_yearly_void_check`. The fate of every option is in the handoff (`docs/handoffs/cloud_2026-11-03_void_corruption.md`).

---

## 5. Rulings built to

Each is **default (orchestrator, 2026-11-03), pending owner**.

- **R1 Hook.** `yearly_playable_pulse`, in `common/on_action/eotg_void_on_actions.txt`, additive. Cooldowns live in the on_action.
- **R2 `eotg_grip_survivor`.** Lifted with the Void. The bloodline branches stay inert until Gate 1 places bearers.
- **R3 Cult faith.** All 23 call sites route through `eotg_void_is_cult_faith` (`always = no`, commented). The cult desc variants, 0001.c's cult path, 0022.b, 0030.a and the Commune decision are inert until the owner rules (Q2).
- **R4 Voidwalkers.** A warrior order of the Malvrick Orders that contains and handles Void and Rift relics; not worshippers, not heretics, not hunted at 866 (REVIEW_866.md:64 outranks the SETTING LORE body's hunts).
- **R5 Voidwalker bug.** 0004 creates the Voidwalker from `eotg_void_voidwalker_template` (shape of `eotg_pmc_operator_template`), flagged; option a seats them. The flag is on the courtier, which is what `eotg_void_has_voidwalker` reads.
- **R6 Orrin.** Narration never states that Orrin is sealed or that the Void is his reach. Cult claims are framed as belief ("the Marked believe", "my faith teaches"). The opinion names are "Believes Them Eye-Marked" and "Respects Their Resolve".
- **R7 Pressure.** The Void keeps "pressure"; cybernetics keeps "static". Band names kept.
- **R8 Stage D.** `eotg_void_hollowing_depth` (0–100) with its own clamped writer; 0031 and 0032 move it; every 0030–0032 option touches depth.
- **R9 Overpromising options.**
  - 0030.c made real: `eotg_void_step_down_effect`, `depose = yes` plus the player hand-off, copied from `eotg_aug_abdicate_effect` (`eotg_augmentation_effects.txt:1386-1404`, which cites vanilla `stress_threshold_events.txt:16775` and `tgp_dynastic_cycle_decisions.txt:2155-2170`).
  - 0021.c reworded ("Keep them away from me for now"): no vanilla or v2 effect fosters a child to a chosen far court in one call.
  - 0022.c reworded ("Have them dragged from the hall"): the effect is dread, piety and an opinion, so the text now says humiliation, not silencing.
  - 0004.d made honest: the Voidwalker now exists, so the option kills them (`death` shape of `eotg_augmentation_kingpin.txt:1135-1138`).
- **R10 Register and the MED/LOW rows.** The Void is external (floor, scar, cold, edge of hearing), never the character's interior language. Saved scopes prefixed; "866 years" removed; Insights guarded; `se_apply/remove` not lifted; unused identifiers pruned; `eotg_mod_void_aura_desc` added; defiance comment fixed; Canadian English; "a Tuesday" gone; the "Hollowed" opinion renamed "Unreachable"; icons are vanilla placeholders listed in §9.

---

## 6. Decisions

| Decision | Shown | Cost | Effect | Cadence |
|---|---|---|---|---|
| `eotg_decision_void_warding_rite` | can be warded, not cult | 200 piety | exposure −20, ward 8y | shared ward flag, 10y |
| `eotg_decision_void_voidwalker_ward` | a Voidwalker at court, not Hollowed | 100 gold | exposure −35, ward 10y, piety −150, zealous courtiers −10 opinion | shared ward flag, 8y |
| `eotg_decision_void_commune` | cult (inert), not Hollowed | 150 piety | seed, Insight, exposure +20, stress | `cooldown` 10y |

---

## 7. Loc surface

File: `localization/english/eotg_void_l_english.yml` (UTF-8 with BOM), 146 keys:
- 8 trait keys (`trait_eotg_<key>` and `_desc`, as `eotg_augmentation_traits.txt`; v1 defined both forms);
- 24 modifier keys (12 modifiers, name and `_desc`);
- 5 opinion names;
- 13 decision keys (3 × name, desc, tooltip, confirm; one shared cooldown tooltip);
- 96 event keys (15 titles, 25 descs and desc variants, 56 options).

**Voice:** first person for the main descs (event_quality_v1 §12.1), with neutral or third-person descs where the court is the subject (0003.desc, 0004, 0022.desc, 0025, 0031) and in trait, modifier and opinion text; second person only in NPC speech and in decision text (as the Cartel decisions). One NPC line at most per desc, straight double quotes, `#EMP` once (0022). Knights through `Custom('KnightCulturePluralNoTooltipLowercase')`. No dashes, no time-of-day words (lint L018), no medieval drift ("flogged", "astronomers in the tower", "fence", "duchy" replaced).

---

## 8. Lore constraints (for eotg-lore-keeper)

1. The Void's present influence is unexplained (ERRATA ORRIN; REVIEW_866.md:35). The text never names what speaks; 0010 says "I do not know what it is".
2. The Void register must never touch the cybernetic voice (ERRATA CYBERNETIC "VOICE"). The cybernetic second perspective is internal and technological; the Void comes from outside.
3. Voidwalkers (R4): 0004 now says "a sworn blade of the Malvrick Orders, one of those who go where the Void has left a mark and carry away what should not be left lying there". The devout's dislike ("Keeps a Voidwalker", the piety costs) is kept from v1 and reframed as discomfort with a Malvrick blade at the table. **Check:** is that dislike canon at 866 (Q4)?
4. The Rift is a separate plane and is not mentioned.
5. "Second Era route-charts" (0023, Deep Charts): the Second Era is the age before the Grip (REVIEW_866.md:27). v1 called them Voidwalker notation; v2 drops that.

---

## 9. Art (B-ART; vanilla placeholders now)

| Object | Placeholder |
|---|---|
| traits `eotg_grip_survivor`, `eotg_void_touched`, `eotg_void_defiant`, `eotg_void_hollowed` | `brave.dds`, `paranoid.dds`, `stubborn.dds`, `callous.dds` (UNVERIFIED-VANILLA paths) |
| exposure and depth bands, aura | modifier icon `stress_negative` |
| warded | `health_positive` |
| Insights | `learning_positive`, `intrigue_positive`, `martial_positive`, `stewardship_positive`, `diplomacy_positive` |
| 3 decisions | `gfx/interface/illustrations/decisions/decision_misc.dds` |

---

## 10. Test list (V-V1…)

Each can become a test-harness decision later.

| ID | Setup | Expect |
|---|---|---|
| V-V1 | Fresh ruler, no Void state; run 25 pulses | 0001 fires about once in 25 years (4%); never twice within 3 years |
| V-V2 | Seed, exposure 0 | accrual +2 a year (base) and `eotg_void_exposure` exists |
| V-V3 | Set exposure 24 → change +1 | Void Whispers appears; only one band modifier at any time |
| V-V4 | Exposure 50, not Defiant | 0010 can fire; Defiant ruler at 50–74 never sees 0010 |
| V-V5 | 0010.b | Void-Defiant, exposure −25, warded 10y, one ward modifier |
| V-V6 | Defiant at 75 | 0011 can fire and makes them Touched (Defiant removed) |
| V-V7 | Touched, at war | 0020 is eligible; not at war, never 0020 |
| V-V8 | Touched, exposure 100 | 0030 fires within the pulse even with the cooldown flag set |
| V-V9 | After 0030 | Hollowed; exposure 100; no exposure band; depth 25; every courtier has "Unreachable" |
| V-V10 | Hollowed, 10 pulses, no choices | depth 65; "Far Off" band from 50 |
| V-V11 | Depth 90 | "Gone Quiet" band; 0031 weight 65 against 0032 15 |
| V-V12 | 0032.d at depth 30 | depth 10, no band |
| V-V13 | 0004.a | the Voidwalker is a courtier with `eotg_flag_void_voidwalker`; the Voidwalker Ward decision shows; accrual −6; 0004 no longer rolls |
| V-V14 | 0004.d | the Voidwalker is dead, killed by root |
| V-V15 | 0030.c, player with an AI heir | the player plays the heir; the old ruler is deposed |
| V-V16 | Insight twice (0010.c, then 0023.a) | +2 skill both times; one Insight modifier only |
| V-V17 | Two Void events in one pulse | impossible: 0004 never fires in a pulse where step 3 fired |
| V-V18 | Any cult path | never shown while `eotg_void_is_cult_faith` is `always = no` |
| V-V19 | Warding Rite then Voidwalker Ward | the second is blocked by the shared flag |
| V-V20 | Loc | every key resolves; no `[scope:`; no Orrin-as-fact line |

---

## 11. Owner questions (each with a recommended default)

- **Q1 Mod-exclusive designation.** Designate Void Corruption mod-exclusive so it can be merged before Gate 1? **Default: yes** (it depends on no map data).
- **Q2 What is a Void cult in v2?** **Default:** keep `eotg_void_is_cult_faith` at `always = no` until faiths exist, then key it on a doctrine or tenet (as CB-12), never a faith key.
- **Q3 Who bears `eotg_grip_survivor` at 866?** **Default:** Gate 1 history assigns it to a handful of old dynasties; until then nobody has it.
- **Q4 Do the devout dislike a Voidwalker at court?** **Default:** yes, mildly (kept from v1: −10 opinion from zealous courtiers, piety costs), framed as discomfort, not heresy. Lore-keeper to confirm.
- **Q5 Contact rate for AI rulers.** 4% a year for every unseeded playable character gives every realm the Void within a generation. **Default:** keep v1's rate for the player test; consider `is_ai = no` or a lower AI rate after the first in-game test.
- **Q6 Stage-D end state.** Depth 100 has no terminal event (no new events allowed). **Default:** none; the "Gone Quiet" band is the end state.
