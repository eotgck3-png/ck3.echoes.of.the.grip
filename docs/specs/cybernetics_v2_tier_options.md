# Spec: Cybernetics v2: hardware-state options on existing events

**Author:** eotg-architect, 2026-10-05
**Authorised by:** the human approved this on 2026-10-05; the orchestrating session relayed it: *"have cybernetics give new options in events based on traits — a round of expanding on choices in events that seem to have few options. Avoid doing this in chains where it would drastically change a story cycle."* The approval covers **new options on existing `events/eotg_augmentation_*.txt` events only. No new events.**
**Builds on:** [cybernetics_v2.md](cybernetics_v2.md) (the index: §1 rules 3–11, the §5 register and never-name lists bind every row), [cybernetics_v2_phase0.md](cybernetics_v2_phase0.md) §2.4 (stress helpers), [cybernetics_v2_trait_depth.md](cybernetics_v2_trait_depth.md) (G9: the trait-option shape this copies), [cybernetics_v2_procedures.md](cybernetics_v2_procedures.md) §2 and [cybernetics_v2_procedures_lore.md](cybernetics_v2_procedures_lore.md) (Seamless resource and register).
**State read:** `v2-space-map` at `3c0686c` plus the working tree (only `docs/pitfalls.md` modified). Event ids, option letters and option counts are as they stand there.

---

## 1. Purpose & gate

No cybernetics event has an option gated on the character's augmentation state. The survey (§1.1) found **zero** such options among the 803 options in 178 events. The only one that comes close is proc.002.c, which checks `eotg_is_augmented_any` as a guard. The tier pools give each tier its own events, so this goes unnoticed inside them. It shows in three places:
- the **thin events**, with 1–3 visible options, where an augmented character facing the problem has no option their hardware changes;
- the **cross-state events**: activities, the non-ruler pool, chain stages that land after a tier change. These fire for characters at different states, but every state gets the same options;
- **Seamless and Neurofractured characters** meeting ordinary events, with no option in their register.

This spec adds **16 options to 11 existing events**. Each option is gated on a hardware state: Augmented, Enhanced or higher, Overclocked, Neurofractured (with a voice stage), or Seamless. Most also need a personality trait. Each one shows either the hardware solving the problem at a cost, or the implant tempting the character.

**Gate 3 (Systems).** Cybernetics is a mod-exclusive system, built against the temporary map (`docs/agent_workflow.md` §5 rule 2). **Not blocked.** No row references a title, province, character, culture or faith.

### 1.1 Survey (Step 1)

**Method.**
- Ran `docs/tools/qa/short_events.py`, `trait_coverage.py`, `option_outcomes.py` and `option_ai_weights.py --prefix eotg_aug_act.00`.
- Ran a scratch survey over `aug_parse.load_events`. Per event it counted options, ungated options, personality-gated options, and options whose `trigger` reads a hardware state (`eotg_is_aug_tier*`, `eotg_neurofractured`, `eotg_total_integration`, `eotg_aug_voice`, `eotg_aug_focus`, pressure bands). It also recorded the event-trigger tiers and the on_action pool tiers.
- Read `docs/qa/generated/console_recipes.md` for firing context.
- Then read every candidate in full.

**Headline numbers** (`trait_coverage.py`): 178 events and 803 options. Events by option count: 0 options: 2, 1: 8, 2: 13, 3: 13, 4: 16, 5: 95, 6: 27, 7: 3, 8: 1. **Options gated on hardware state: 0.** Personality-gated options: 298.

**Events with ≤ 3 options** (hidden events left out), with what this spec does with each:

| Event | Opts | Disposition |
|---|---|---|
| tier2.016 *What Was Done* | 3 (1 visible in 3 of 4 outcomes) | **chosen** |
| tier2.021 *The Report Was Wrong* | 2 | **chosen** |
| tier2.014 *The Vendors Return* | 3, all ungated | **chosen** |
| tier3.019 *Lighter Hands* | 3 | **chosen** |
| fracture.029 *It Passes* | 2 | **chosen** (borderline: see §5.3) |
| tier2.018 *Resolution* | 2 | excluded: an Heir's Arc seed (index T3) |
| tier3.018 *The Plot: The Truth* | 2 | skipped: an outcome stage with a merged fallback option; the plot variables decide everything |
| tier3.024 *The Engagement* | 2 | skipped: an outcome notification (index rule 6, CB-26 S12); a real hardware option needs a battle beat (§10, suggestion H1) |
| tier3.022, tier1.017, tier1.019 | 1 | skipped: outcome notifications |
| tier1.014, tier1.015 | 3, 2 | skipped: rejection chain outcome roll (built behaviour) |
| tier1.022 *Installation*, init.008, init.012 | 2–3 | skipped: procedure and bridge outcomes (built behaviour: the procedure roll) |
| proc.002, proc.004, proc.005 | 3, 1, 3 | skipped: procedure flow (the roll, `eotg_aug_has_surgeon_for`, booking guard, clinic-closed gating) |
| tamper.002, tamper.003 | 2 | skipped: Tamper scheme outcomes (interactions spec) |
| fracture.020 *What the Record Shows* | 2 | skipped: the chain end clears the accusation variables in every option, and a voice option needs a follow-up beat (§10, H2) |
| fracture.0001, fracture.028 | 1 | excluded: the cascade transition notice and the Terms of Access grant notice |
| end.002, end.010, end.011 | 3, 1, 3 | excluded: chain stages of endgame transitions (endgame file header) |
| end.009, end.030 | 3, 2 | excluded: endgame transitions |
| end.041, end.042 | 3, 1 | skipped: Seamless-only, so every option is already in the logging register |
| countdown.005, countdown.006 | 3, 2 | excluded: the Countdown |
| patron.007 | 3 | excluded: the Patron |

**Events with no option that reflects the acting character's hardware.** That is every event, by the gate count. Most 5–6-option tier events still have *universal* options that act through the hardware: "Let the optics track it", "Throttle it down", "Execute the plan". Those are saturated, and adding to them would overflow the window. The real gap is the events where the acting character's hardware never comes into it:
- the **activity events**: act.001 and act.003 for the host; act.002 and act.004 for an Overclocked or Neurofractured guest, who gets a desc variant but no option;
- **nr.003**, where the liege's own hardware is irrelevant;
- the thin chain stages above;
- **tier3.006**, where the question is literally your fitness to rule.

**Ranking** (thinness = most options an augmented character sees today; fit = how natural a hardware option is):

| Rank | Event | Visible today | Fit | Why |
|---|---|---|---|---|
| 1 | tier2.016 *What Was Done* | 1 (non-culprit outcomes) | high | A firmware audit with no author. Enhanced hardware can be rebuilt by hand. |
| 2 | tier2.021 *The Report Was Wrong* | 2 | high | The model was wrong in a way you can check. Either retrain it or let it flag harder. |
| 3 | tier2.014 *The Vendors Return* | 3, flat | high | Two firmware offers. The overlay can read margins. |
| 4 | tier3.019 *Lighter Hands* | 2–3 | high | The desc already says the implant "has built a table". The temptation is to let it run the desk. |
| 5 | fracture.029 *It Passes* | 1–2 | high | Post-cascade recovery. The model offers to schedule it, a voice moment. |
| 6 | act.003 *Foul Play?* | 3–5 | high | An Enhanced or Seamless host can read the casing from the seat. |
| 7 | nr.003 *Something Is Wrong* | 3–4 | high | A liege who has lived these symptoms, or a Seamless liege who logs them. |
| 8 | act.004 *A Hum at the Table* | 3–4 | med-high | Neurofractured has a desc variant and no option; a first fitting is plain enough to hand round. |
| 9 | act.002 *Past Spec* | 3–4 | med-high | Overclocked and Neurofractured have desc variants and no option. |
| 10 | tier3.006 *The Delegation* | 3–4 | med-high | "Are you still fit to rule?" The logs can answer. |
| 11 | act.001 *The Rules of the Field* | 3–4 | med | A Seamless host rules on the entrants by tolerance. |

**Considered and left out** (not excluded by the brief):
- act.005 already shows 5 at once (brave + lifestyle_hunter).
- act.006 is a faith reaction. The zealous-versus-Industrial-Survivalism deferral (index §5) applies.
- nr.001, nr.005, nr.006 and realm.001 have 5–6 visible.
- int.001 and int.002 run the interactions roll.
- tier2.010 seeds the Heir's Arc (`eotg_flag_aug_absent_at_birth`).
- tier3.007 and tier3.015 already set the bond and run the Two Machines chain, and are hardware-centric.
- tier3.016 has 4 options and is already hardware-saturated.
- The initiation events: the root is usually unaugmented.

### 1.2 Excluded by the brief (Step 2)

| Excluded | Ids | Reason |
|---|---|---|
| The Countdown | countdown.001–.006 | story cycle |
| The Patron | patron.001–.009 (incl. .008 *The Paper*, .009) | story cycle; Patron paper is built behaviour |
| The Heir's Arc | heir.001–.007; plus tier2.010, tier2.018, tier3.020 (seeds, index T3) | story cycle and its seeds |
| The Iron Retinue | retinue.001–.005 | story cycle |
| Endgame transitions | end.001, .002, .009, .010, .011, .020, .030, .031 | change tier or state, or are stages of a change (endgame file header) |
| Frontier | all `eotg_frontier*` | out of scope |
| Options that set story variables or stages | any event whose options start, end or advance a story or set its stage variable | none chosen here sets one (§9 item 7 checks) |

**Purely local exception used:** none from the list above. fracture.029 is not on the list, but it sits in the cascade flow; see §5.3.

---

## 2. Signature resource

**`eotg_fracture_risk`** (character variable 0–100, hidden, index §1 rule 3), plus tier through `eotg_aug_set_integration_effect`. **At Seamless the resource is `eotg_aug_residue`** (hidden integer 0–3; it only falls). The reason: `eotg_add_fracture_risk` is a no-op at Seamless by design (`common/scripted_effects/eotg_augmentation_effects.txt:271-284`, guard `NOT = { has_trait = eotg_total_integration }`). Residue is the lore-approved Seamless signature (procedures spec §2; lore ruling (a)). **The brief says "risk or tier"; this is the one stated deviation, and it is forced.** A Seamless row that moved risk would move nothing.

Every one of the 16 rows moves a signature resource, always inside `hidden_effect`:
- **13 rows** move `eotg_fracture_risk` on root.
- **1 row** (nr.003.f) moves it on both root and `scope:eotg_champion`.
- **3 Seamless rows** move residue −1 (hidden, clamped at 0). Two of them (act.001.f, nr.003.g) also move other characters' risk.
- **No row changes tier.**

Direction follows index rule 4:
- below Overclocked, root moves are all **+**;
- the only **−** moves are on other characters (champion, entrants), as nr.003.a and nr.003.d already do.

No row shows a number. Loc never says "risk", "odds" or "chance" and carries no digits (Q1).

---

## 3. Identifier table

**No new scripted effects, triggers, modifiers, opinions, flags, variables, traits or icons.** Every key the rows use already exists and was checked in the tree:

| Key | Type | Defined in |
|---|---|---|
| `eotg_is_aug_tier1` / `_tier2` / `_tier3` | scripted triggers | `common/scripted_triggers/eotg_augmentation_triggers.txt:16,28,42` |
| `eotg_neurofractured`, `eotg_total_integration`, `eotg_cybernetics` | traits (gate and icon) | `common/traits/eotg_augmentation_traits.txt:16,129,164` |
| `eotg_aug_voice` | char var 0–5 | set by `eotg_aug_voice_advance_effect` (never lowered) |
| `eotg_aug_residue` | char var 0–3 | set by `eotg_aug_total_integration_effect` (`eotg_augmentation_effects.txt:1117`) |
| `eotg_aug_pressure_flicker` | scripted trigger (band) | triggers file :115 |
| `eotg_add_fracture_risk` | scripted effect (`AMOUNT`) | effects file :271 |
| `eotg_aug_act003_examine_effect` | scripted effect | effects file :3010 |
| `eotg_aug_act004_reactions_effect` | scripted effect | effects file :3051 |
| `eotg_aug_act_withdraw_effect` (`HOST`) | scripted effect | effects file :2978 |
| `eotg_aug_tournament_entrant` | scripted trigger | triggers file :634 |
| `eotg_aug_stress_embrace_effect` | stress helper | Phase 0 §2.4 |
| `eotg_mod_implant_calibrated`, `eotg_mod_aug_lesson_learning`, `eotg_mod_aug_lesson_intrigue`, `eotg_mod_aug_overheated`, `eotg_mod_aug_optimised_levies`, `eotg_mod_aug_tampered` | static modifiers | `common/modifiers/eotg_augmentation_modifiers.txt` |
| `eotg_opinion_aug_reassured`, `_unease`, `_fear`, `_falsely_accused` | opinion modifiers | `common/opinion_modifiers/eotg_augmentation_opinions.txt` |
| `eotg_flag_aug_vendor_safe` / `_bold` | char flags | tier2.013 / .014 |
| `scope:activity`, `scope:eotg_aug_accused`, `scope:eotg_aug_accuser`, `scope:eotg_champion`, `scope:eotg_tamper_outcome`, `scope:eotg_flagged`, `scope:eotg_delegation_leader` | saved scopes | the host events or their firing chain |

**Identifier conventions for this batch.**
- **Option names** use the host event's existing dot form (index "Decided here"): `eotg_aug_act.002.f`, `eotg_aug_tier2.021.c`, `eotg_fracture.029.c`. The letter is the **next free letter** in each event.
- **Sub-keys** (toasts, tooltips) append to the option key, as the file already does (`eotg_aug_act.003.c.hot`, `eotg_aug_end.041.c.stays`): `eotg_aug_tier3.006.e.tt`, `.e.clean`, `.e.strained`.

**New option keys (16) and sub-keys (3):**

| Event | New option(s) | Gate (short) |
|---|---|---|
| `eotg_aug_act.001` *The Rules of the Field* | **f** | Seamless |
| `eotg_aug_act.002` *Past Spec* | **f**, **g** | Overclocked + wrathful; Neurofractured, voice ≥ 2 |
| `eotg_aug_act.003` *Foul Play?* | **f**, **g** | Enhanced+ and diligent, not just; Seamless, not just |
| `eotg_aug_act.004` *A Hum at the Table* | **f**, **g** | Neurofractured, voice ≥ 2; Augmented + trusting |
| `eotg_aug_nr.003` *Something Is Wrong* | **f**, **g** | Enhanced+; Seamless |
| `eotg_aug_tier2.014` *The Vendors Return* | **d** | Enhanced+ and greedy |
| `eotg_aug_tier2.016` *What Was Done* | **d** | Enhanced+ and diligent, outcome not culprit |
| `eotg_aug_tier2.021` *The Report Was Wrong* | **c**, **d** | Enhanced+ and paranoid; Enhanced+ and just |
| `eotg_aug_tier3.006` *The Delegation* | **e** (+ `.e.tt`, `.e.clean`, `.e.strained`) | Overclocked + honest |
| `eotg_aug_tier3.019` *Lighter Hands* | **d** | Overclocked + lazy |
| `eotg_fracture.029` *It Passes* | **c** | Neurofractured, voice ≥ 3 |

**Traits checked** in `game/common/traits/00_traits.txt` (index rule 10): wrathful :2707, diligent :2613, greedy :2464, paranoid :4003, just :3803, honest :3242, lazy :2566, trusting :4085, compassionate :4143. None is a childhood trait. `curious` and `pensive` are not used.

**Owners:** scripter (16 options), localizer (19 keys), and the human for the Seamless icon (existing art debt `gfx/interface/icons/traits/eotg_total_integration.dds`, §10). No CoAs, name lists or holy sites. CB-42 (named sellers) will later touch tier2.014's vendor wording. Row 10's loc says "the vendors" so it can take a name.

---

## 4. File placement

| File | Change |
|---|---|
| `events/eotg_augmentation_activities.txt` | act.001.f; act.002.f, .g; act.003.f, .g; act.004.f, .g |
| `events/eotg_augmentation_nonruler.txt` | nr.003.f, .g |
| `events/eotg_augmentation_tier2.txt` | tier2.014.d; tier2.016.d; tier2.021.c, .d |
| `events/eotg_augmentation_tier3.txt` | tier3.006.e; tier3.019.d |
| `events/eotg_augmentation_fracture.txt` | fracture.029.c |
| `common/modifiers/eotg_augmentation_modifiers.txt` | `# Caller(s):` comment updates only: `eotg_mod_aug_overheated` (+act.002.f), `eotg_mod_aug_optimised_levies` (+tier3.019.d), `eotg_mod_aug_tampered` (+tier2.016.d removal) |
| `localization/english/eotg_augmentation_l_english.yml` | 19 keys (§7) |

Each new option goes **after the host event's last existing option**. It carries the file's usual one-line comment: `# [<gate>] "Text." why`. **No other file changes.** In particular: no on_action, event `trigger`, `immediate` or desc changes, and no change to existing options.

---

## 5. Wiring

### 5.0 Firing (unchanged)

No on_action, branch, weight, cooldown or chain-delay changes. Every host is already fired:

| Host | Fired by | States that can reach it |
|---|---|---|
| act.001 | `eotg_on_tournament_opening_aug` (`common/on_action/eotg_augmentation_on_actions.txt:2019`) | host in any state, including Seamless and unaugmented |
| act.002 | `eotg_on_tournament_contest_aug` (:2039) | Augmented, Enhanced, Overclocked, Neurofractured (not Seamless) |
| act.003 | `eotg_on_tournament_active_aug` (:2061), player host | host in any state |
| act.004 | `eotg_on_feast_aug` (:2092), player | Augmented–Neurofractured (not Seamless) |
| nr.003 | `eotg_on_yearly_aug_nonruler_check` (:1475), on `scope:eotg_nr_liege` | liege in any state |
| tier2.014 | tier2.013 a/c (`events/eotg_augmentation_tier2.txt:1869,1910`) | `eotg_cybernetics` (Enhanced, or Overclocked if upgraded in the gap) |
| tier2.016 | tier2.015 a/c/d (:2063,2088,2124) | as above |
| tier2.021 | tier2.012 b/e (:1668,1723) | Enhanced, Overclocked, or Neurofractured by then |
| tier3.006, tier3.019 | `eotg_on_yearly_aug_overclocked_check` (:864) | Overclocked |
| fracture.029 | fracture.027 a–d, end.009 a/c (`console_recipes.md` row 187) | Neurofractured |

**Cooldown authority** stays in those on_actions and chains (index §1 rule 5). No row sets or reads a cooldown flag, and no row's `trigger` reads anything but world state: traits, tier, voice, outcome scopes, gold.

### 5.1 Shared option shape

```
option = {
    name = eotg_aug_<event>.<letter>
    trigger = {
        <hardware gate>                    # from the table below
        has_trait = <personality>          # rows that have one
        <extra guard>                      # rows that list one
    }
    trait = <personality>                  # rows that have one: first icon
    trait = <hardware trait>               # eotg_cybernetics | eotg_neurofractured | eotg_total_integration
    ...effects (row)...
    hidden_effect = { <signature move (row)> }
    <stress (row)>
    ai_chance = {
        base = 30
        modifier = { add = <30|20>  has_trait = <primary> }
        modifier = { add = 10  has_trait = <secondary> }
    }
}
```

**Hardware gates** (the existing tier triggers; reuse, do not redefine):

| Gate | Trigger body |
|---|---|
| **H-AUG** (Augmented) | `eotg_is_aug_tier1 = yes` |
| **H-ENH+** (Enhanced or Overclocked) | `OR = { eotg_is_aug_tier2 = yes  eotg_is_aug_tier3 = yes }` |
| **H-OC** (Overclocked) | `eotg_is_aug_tier3 = yes` |
| **H-NF(v)** (Neurofractured, voice stage v) | `has_trait = eotg_neurofractured  has_variable = eotg_aug_voice  var:eotg_aug_voice >= v` (the fracture file's idiom, e.g. `events/eotg_augmentation_fracture.txt:1575-1590`) |
| **H-SEAM** (Seamless) | `has_trait = eotg_total_integration` |

**Why the tier gate is written even where the host fires at one tier.** tier2.014, .016 and .021, and tier3.006 and .019, are chain stages or pool events that land days to months after the roll. The ruler may have upgraded, regressed or cascaded by then. QA round 2 re-checks tier in chain stages for the same reason (tier3.015, tier3.021 triggers). The gate also tells the reader and the icon *which hardware* unlocks the option.

**Icons.** A row with a personality trait shows that trait's icon first and the hardware trait second. Vanilla puts two `trait =` lines on one option at `game/events/dlc/fp2/fp2_struggle_events.txt:2360-2361`, and the mod does the same at `eotg_aug_end.040.d`. A hardware-only row shows the hardware trait alone. The Seamless icon is existing art debt (see §10).

**`ai_chance`.** Base 30, inside the index's 10–40 range. The primary modifier is +30 when the row's gate includes that trait (the G9 shape) and +20 on hardware-only rows. Every row has a secondary +10. Each row therefore has ≥ 2 trait modifiers (index rule 6).

**Stress.** Personality rows use an inline `stress_impact = { <trait> = minor_stress_impact_loss }`, as every G9 row does. Rows that lean into the machine also call `eotg_aug_stress_embrace_effect`, the Phase 0 helper for exactly that. **No row adds an inline line for impatient, gluttonous, temperate or fickle** (trait-depth §5.2). **Seamless rows carry no stress line.** That follows the end.040 and end.041 precedent and the trait's `stress_gain_mult = -0.75`, and it keeps the register rule that the ruler does not feel.

**Signature moves.** Risk: `eotg_add_fracture_risk = { AMOUNT = N }` inside `hidden_effect`, the activities file's pattern. Residue: copy the end.040.b block verbatim:
`if = { limit = { has_variable = eotg_aug_residue }  change_variable = { name = eotg_aug_residue  add = -1 }  clamp_variable = { name = eotg_aug_residue  min = 0  max = 3 } }` inside `hidden_effect`.

### 5.2 The sixteen options

Risk sizes follow the existing scales; each row cites a comparable option already in the tree.

| # | Option | Gate (+ extra guard) | `trait =` | Effects (script-level, in order) | Signature move (comparable) | `ai_chance` (base 30) | Stress |
|---|---|---|---|---|---|---|---|
| 1 | **act.001.f** | H-SEAM | `eotg_total_integration` | `involved_activity = { every_attending_character = { limit = { eotg_aug_tournament_entrant = yes  OR = { eotg_is_aug_tier3 = yes  has_trait = eotg_neurofractured } }  eotg_aug_act_withdraw_effect = { HOST = root } } }`, then `involved_activity = { every_attending_character = { limit = { eotg_aug_tournament_entrant = yes  OR = { eotg_is_aug_tier1 = yes  eotg_is_aug_tier2 = yes } }  hidden_effect = { eotg_add_fracture_risk = { AMOUNT = 3 } } } }`. **No** zealous-unease loop (unlike a/d): the ruling is by tolerance, not by faith. | residue −1 (end.040.b); entrants who ride +3 (act.001.a) | +20 just, +10 diligent | none (Seamless) |
| 2 | **act.002.f** | H-OC + wrathful | `wrathful`, `eotg_cybernetics` | `activity_tournament_change_contestant_score_effect = { SCORE = increase_major }` · `add_character_modifier = { modifier = eotg_mod_aug_overheated  years = 1 }` (the reflex layer runs unthrottled: health −0.5) · **no** 25% "seen" roll | root +8 (above act.002.a's OC branch +6; equal to its NF branch +8) | +30 wrathful, +10 brave | inline `wrathful` loss · `eotg_aug_stress_embrace_effect` |
| 3 | **act.002.g** | H-NF(2) | `eotg_neurofractured` | `activity_tournament_change_contestant_score_effect = { SCORE = increase_major }` · **no** "seen" roll (the model times every exchange inside the rules' tolerance) | root +10 (act.002.a NF +8, plus the handover) | +20 ambitious, +10 arrogant | `eotg_aug_stress_embrace_effect` |
| 4 | **act.003.f** | H-ENH+ + diligent; `NOT = { has_trait = just }` | `diligent`, `eotg_cybernetics` | `eotg_aug_act003_examine_effect = yes` (the same verdict as c/e, told by toast; the toasts never say who examined) · no surgeon needed | root +2 (act.005.a tier 1–2 +2) | +30 diligent, +10 paranoid | inline `diligent` loss |
| 5 | **act.003.g** | H-SEAM; `NOT = { has_trait = just }` | `eotg_total_integration` | `eotg_aug_act003_examine_effect = yes` | residue −1 (end.040.b) | +20 just, +10 diligent | none (Seamless) |
| 6 | **act.004.f** | H-NF(2) | `eotg_neurofractured` | `add_prestige = minor_prestige_value` · `eotg_aug_act004_reactions_effect = yes` | root +6 (act.004.d +4, plus the handover) | +20 gregarious, +10 arrogant | `eotg_aug_stress_embrace_effect` |
| 7 | **act.004.g** | H-AUG + trusting | `trusting`, `eotg_cybernetics` | `add_prestige = minor_prestige_value` · **no** reactions effect (it is handed round close up, not shown to the hall) | root +2 (act.005.a +2) | +30 trusting, +10 gregarious | inline `trusting` loss |
| 8 | **nr.003.f** | H-ENH+ | `eotg_cybernetics` | `scope:eotg_champion = { add_opinion = { modifier = eotg_opinion_aug_reassured  target = root  years = 5 } }` | champion −10 (nr.003.a −10, here with no gold); root +3, the ruler's own maintenance slot given up (act.004.a +3) | +20 compassionate, +10 generous | inline `compassionate = minor_stress_impact_loss  callous = minor_stress_impact_gain` |
| 9 | **nr.003.g** | H-SEAM; `gold >= minor_gold_value` | `eotg_total_integration` | `remove_short_term_gold = minor_gold_value` · `scope:eotg_champion = { add_character_modifier = { modifier = eotg_mod_implant_calibrated  years = 1 }  add_opinion = { modifier = eotg_opinion_aug_unease  target = root  years = 5 } }` | champion −12 (nr.003.a −10, plus calibration); residue −1 | +20 diligent, +10 callous | none (Seamless) |
| 10 | **tier2.014.d** | H-ENH+ + greedy | `greedy`, `eotg_cybernetics` | `remove_character_flag = eotg_flag_aug_vendor_bold` · `add_character_flag = eotg_flag_aug_vendor_safe` · `add_gold = medium_gold_value` (a gives `minor_`; the overlay finds the margin) | root +3 (tier2.014.b +3) | +30 greedy, +10 diligent | inline `greedy` loss |
| 11 | **tier2.016.d** | H-ENH+ + diligent; `NOT = { scope:eotg_tamper_outcome = flag:culprit }` | `diligent`, `eotg_cybernetics` | `if = { limit = { has_character_modifier = eotg_mod_aug_tampered }  remove_character_modifier = eotg_mod_aug_tampered }` · `add_character_modifier = { modifier = eotg_mod_aug_lesson_learning  years = 5 }` | root +4 (tier1.007.f +4: firmware work without the technicians' preparation) | +30 diligent, +10 paranoid | inline `diligent` loss |
| 12 | **tier2.021.c** | H-ENH+ + paranoid | `paranoid`, `eotg_cybernetics` | `add_character_modifier = { modifier = eotg_mod_aug_lesson_intrigue  years = 5 }` · `scope:eotg_flagged` keeps the falsely-accused opinion and stays held if held | root +6 (tier2.021.b +5, one step further) | +30 paranoid, +10 callous | inline `paranoid` loss · `eotg_aug_stress_embrace_effect` |
| 13 | **tier2.021.d** | H-ENH+ + just | `just`, `eotg_cybernetics` | `scope:eotg_flagged = { … }` exactly as option a (release if held by root; remove `eotg_opinion_aug_falsely_accused` if present; add `eotg_opinion_aug_reassured` 5y) · `add_character_modifier = { modifier = eotg_mod_implant_calibrated  years = 1 }` · `add_prestige = { value = minor_prestige_value  multiply = -1 }` (the correction is made before the court) | root +3 (tier2.021.a +2, plus retraining) | +30 just, +10 honest | inline `just` loss |
| 14 | **tier3.006.e** | H-OC + honest | `honest`, `eotg_cybernetics` | `custom_tooltip = eotg_aug_tier3.006.e.tt` · `hidden_effect = { if = { limit = { eotg_aug_pressure_flicker = yes }` → every vassal with `opinion(root) < -20`: remove `eotg_opinion_aug_fear` and `_unease` if present, add `eotg_opinion_aug_reassured` 5y; toast `eotg_aug_tier3.006.e.clean` (left_icon `scope:eotg_delegation_leader`) `} else = {` → the same vassals add `eotg_opinion_aug_unease` 5y; `add_prestige = { value = minor_prestige_value  multiply = -1 }`; toast `eotg_aug_tier3.006.e.strained` `} }` | root +3 (tier3.021.a +3). **Reads the band** inside `hidden_effect`, so the tooltip never shows the condition (the `eotg_aug_act003_examine_effect` / end.041.c toast pattern) | +30 honest, +10 just | inline `honest` loss |
| 15 | **tier3.019.d** | H-OC + lazy | `lazy`, `eotg_cybernetics` | `add_character_modifier = { modifier = eotg_mod_aug_optimised_levies  years = 3 }` (tier2.011.a's implant-optimised desk: tax up, vassals cooler) · **does not** fire tier3.021 and sets no delegate flag (as b) | root +8 (tier3.019.b failure +8) | +30 lazy, +10 content | inline `lazy` loss · `eotg_aug_stress_embrace_effect` |
| 16 | **fracture.029.c** | H-NF(3) | `eotg_neurofractured` | `stress_impact = { base = medium_stress_impact_loss }` (the model takes the shaking off you) | root +8 (act.002.a NF +8; the mirror of .029.b's −5) | +20 content, +10 craven | the base relief above · `eotg_aug_stress_embrace_effect` |

**Per-row notes.**
- **2 (act.002.f).** Wrathful's vanilla opposite is calm, which none of the existing gated options uses. "Reflexes" is the Overclocked ruler's own word, not voice text, so the §5.2 ban on "answers" does not apply. The localizer may still choose "take it" (§7).
- **3 / 6 / 16 (Neurofractured rows).** None of them calls `eotg_aug_voice_advance_effect`. Voice stages belong to the T1 beats only. A voice gate below the threshold just hides the row.
- **4 / 5 (act.003).** Both exclude `just`, because e already runs the same examination for a just host. With that exclusion, e, f and g never show together (§5.4).
- **8 vs nr.003.d.** d (compassionate) gives −8 and costs nothing. f gives −10 and costs the ruler +3. a gives −10 and costs gold. Nothing here is a free win over a universal option.
- **11 (tier2.016.d).** In the malfunction outcome it removes the year of relearning. In the risk and nothing outcomes the lesson is what it pays. The culprit outcome keeps its own b/c.
- **13 (tier2.021.d).** For a just ruler this is the better deal than a, which is allowed (index rule 6, amended 2026-10-03). a stays the honest option and still has its point (no prestige cost).
- **14 (tier3.006.e).** The just option d can show alongside, giving 5 at most. The honest gamble reads a band the player cannot see. That is the hidden-risk rule working as intended: prose and toasts react to the band, and nothing quantifies it.
- **15 (tier3.019.d).** Tech ceiling: the implant is not networked into the treasury or the realm's records (procedures lore (c)). The fiction is that **the ruler's hands do the work in the order the model sets**, without reading it. The levy modifier is the result.

### 5.3 Borderline: fracture.029

fracture.029 is the survival branch after a cascade or a stalled handover (fired by fracture.027 a–d and end.009 a/c). It is **not** in the brief's exclusion list:
- it changes no tier or state (it stays Neurofractured);
- its options set no story variable;
- row 16 moves only risk and stress.

It *is* in the endgame flow, though, and the brief says to prefer skipping such events. **Recommendation: keep it.** It is the thinnest choice event a Neurofractured ruler meets (one universal option), and it is the clearest voice moment outside the T1 beats. **If the orchestrator reads it as endgame, drop row 16 and nothing else changes.** The batch is then 15 options in 10 events, still inside the 12–20 target.

### 5.4 Visible-option check (≤ 5 at once)

The cap comes from vanilla practice and CB-34 item 7. Counts are the most options visible at once *after* this batch.

| Host | Always | Conditionally gated | New | Most visible at once |
|---|---|---|---|---|
| act.001 | a, b, c | d cynical / e zealous (vanilla opposites) | f Seamless | **5** |
| act.002 | a, b, c | d deceitful / e honest (opposites) | f Overclocked / g Neurofractured (mutually exclusive traits) | **5** |
| act.003 | a, b, d | c (surgeon access); e just | f (not just, Enhanced+) / g (not just, Seamless) | **5** (e, f and g are mutually exclusive) |
| act.004 | a, b, c | d gregarious / e shy (opposites) | f Neurofractured / g Augmented (exclusive) | **5** |
| nr.003 | b, c (+ a with gold) | d compassionate / e callous (opposites) | f Enhanced+ / g Seamless (exclusive) | **5** |
| tier2.014 | a, b, c | — | d | **4** |
| tier2.016 | a | b / c (culprit only; held vs not held) | d (not culprit) | **2** |
| tier2.021 | a, b | — | c paranoid, d just | **4** |
| tier3.006 | a, b, c | d just | e honest | **5** |
| tier3.019 | b (+ a with a delegate) | c humble | d lazy | **4** |
| fracture.029 | a | b humble | c | **3** |

No host goes above 5. The G9 hosts (tier1.005, tier1.007, tier2.004, tier2.020, tier3.003, tier3.010, tier3.021, nr.004) are **not touched**.

---

## 6. Vanilla precedent

| Pattern | Source | Used for |
|---|---|---|
| Trait-gated option, `trigger` + `trait` icon | index §1 rule 6; G9 rows (trait-depth §5.1) | all 16 |
| Two icons on one option | `game/events/dlc/fp2/fp2_struggle_events.txt:2360-2361`; mod `eotg_aug_end.040.d` | the 11 personality + hardware rows |
| Verdict told by toast after the click, hidden branch | `game/events/activities/hunt_activity/jb_hunt_events.txt:2375` (hunt.8540, cited at `eotg_augmentation_effects.txt:3007`); mod end.041.c | tier3.006.e |
| Excluding a trait to avoid a duplicate option | the mod's G9 practice of avoiding stacked same-effect options; vanilla opposite pairs that never co-show | act.003.f, .g (`NOT just`) |
| Seamless options carry no stress | mod end.040 / end.041; `eotg_total_integration` `stress_gain_mult = -0.75` | rows 1, 5, 9 |

**Deviation:** the three Seamless rows move residue, not risk (§2, forced by the risk effect's guard). Nothing else deviates.

---

## 7. Loc surface (eotg-localizer)

File: `localization/english/eotg_augmentation_l_english.yml`, UTF-8 BOM, dot form, one definition each. Place each key under its event's block, after the last existing option key. The text below is a proposal; the localizer owns the final wording within §8. **No `replace/` override and no vanilla string change.**

| Key | Proposed text | Speaker / register / brief |
|---|---|---|
| `eotg_aug_act.001.f` | "Units above tolerance are barred. The rest may ride." | Seamless ruler. Logging register: short declaratives, often passive, no feeling. A ruling by rating, not by faith. |
| `eotg_aug_act.002.f` | "Let the reflexes answer." | Overclocked ruler. Stop throttling the reflex layer. "Take it" is an acceptable alternative ending. Not voice text. |
| `eotg_aug_act.002.g` | "Run the schedule it has already drafted." | Neurofractured ruler, **voice register**: the model has planned the next exchanges half a second ahead. "It" is the model of you. Nothing speaks, answers or whispers. |
| `eotg_aug_act.003.f` | "Run the heat readings through the overlay." | Enhanced host. The overlay reads the casing from the seat. |
| `eotg_aug_act.003.g` | "Casing temperatures noted. A ruling follows." | Seamless host, logging register. |
| `eotg_aug_act.004.f` | "Let it finish my sentences." | Neurofractured guest, **voice register**: the model of you replies to the guests a half-second early, in your own voice. Internal, never external. |
| `eotg_aug_act.004.g` | "It is only a first fitting. Let them hold it." | Augmented guest. The hardware is plain enough to hand round. |
| `eotg_aug_nr.003.f` | "I know these symptoms. Take my maintenance slot." | Enhanced+ liege. Pronoun-neutral as written. If it names the champion, use `[eotg_champion.GetHerHim]`. |
| `eotg_aug_nr.003.g` | "Fault logged. Maintenance is scheduled." | Seamless liege, logging register. The champion is treated as equipment; the unease is the court's feeling, not the ruler's. |
| `eotg_aug_tier2.014.d` | "Run their margins through the overlay." | Enhanced, greedy. "Their" means the vendors. CB-42 may later name them. |
| `eotg_aug_tier2.016.d` | "Rebuild the parameters from my own logs." | Enhanced, diligent. Personal device logs only, not networked. |
| `eotg_aug_tier2.021.c` | "Lower the threshold. Let it flag more." | Enhanced, paranoid. The temptation: trust the machine over people. |
| `eotg_aug_tier2.021.d` | "Correct the model, and say so before the court." | Enhanced, just. |
| `eotg_aug_tier3.006.e` | "Hand them my diagnostic logs." | Overclocked, honest. |
| `eotg_aug_tier3.006.e.tt` | "The delegation reads the logs. Its verdict follows." | Option tooltip. No band, no number. |
| `eotg_aug_tier3.006.e.clean` | "[eotg_delegation_leader.GetName] reads the logs twice and finds nothing to fear. The delegation leaves reassured." | Toast. Gendered pronouns via `[eotg_delegation_leader.GetSheHe]` if used. |
| `eotg_aug_tier3.006.e.strained` | "The logs show a system running close to its limits. [eotg_delegation_leader.GetName] reads them in silence, and the delegation leaves more worried than it came." | Toast. Prose may react to the band (index rule 3), but must not quantify it. |
| `eotg_aug_tier3.019.d` | "Work through its table. Don't read it." | Overclocked, lazy. The ruler's hands do the work in the model's order. **Not** "let the implant run the treasury" (tech ceiling). |
| `eotg_fracture.029.c` | "Let it schedule the recovery." | Neurofractured, voice ≥ 3, **voice register**: the model forecasts and schedules. It is "us", a half-second early. |

**19 keys** (16 option keys, 1 tooltip, 2 toasts). Bare `[x.GetName]`, never `[scope:x]`.

---

## 8. Lore constraints

- **Voice register** (index §5 item 1; SETTING LORE ERRATA "CYBERNETIC 'VOICE'", 2026-10-03), for rows 3, 6 and 16. The voice is the implant's predictive model of its user, running ahead. It is internal. It logs, schedules, forecasts and requests access. It is **never** external, never whispering, never "answers" or "speaks from" anywhere, and is never the Eye.
- **Banned in the Neurofractured rows** (index §5 item 2): Void, Orrin, Kyros, the Eye, breach, rift, tear, whisper, "at the edge of hearing", hollow, silent speaker, answers, speaks from, prison, possess/possession, demon, pact, abyss, frenzy, "grip" as a metaphor, Carrigore.
- **Seamless register** (procedures lore (c), ruling (a)), for rows 1, 5 and 9:
  - logging or report voice: short declaratives, often passive;
  - "you" may be the subject of a bodily action or a decision outcome, never of a feeling;
  - the court may feel, the ruler may not;
  - any residue-flavoured line ends with the thing logged, filed or pruned;
  - never preference, hesitation, longing, regret, "the old self", or anything returning.
- **Tech ceiling** (ERRATA "CYBERNETICS AT 866", 2026-10-04):
  - no self-repair: no row references it, so no `eotg_aug_can_self_repair` gate is needed;
  - no remote-kill;
  - no state programme;
  - no upload, backup or datavault;
  - the implant is not networked into the treasury or records (row 15's fiction, row 11's "own logs").
- **Licensing is local and unnamed** (index §5 item 3). No row names an authority, and none uses the never-name list: Blackstar, Shadow Markets, Black Contract(s), Blackline, P&D, Calix, Pill Mob / Pillwake / Red Pills, Concrete Cartel, Acathea, the Codex, Archivists, Conclave, Tribunal, "Trauma Team", Helix, or "galactic"/"League".
- **No monotheistic invocations; "self"/"personhood", never "humanity"** (index §5 items 4–5).
- **Medieval leaks** (index §5 item 6): no palace, masons, scribes or horses. "Hall", "court" and "table" are already in the host events.
- **Gendered pronouns** through the loc functions (`GetSheHe`, `GetHerHim`, `GetHerHis`). **Canadian English**: favour, honour, centre, defence, -ize (apologize, recognize), as the file already does.
- **Map-agnostic** (index rule 9). Faith reactions only through existing helpers (act.004's reactions effect); no row adds a faith or culture read.
- **Nothing here is uncertain canon.** The lore-keeper's routine pass over the 19 lines applies (§9 item 10).

---

## 9. Definition of done

0. **Validation, all three clean** on the touched files, except the known-benign items in `CLAUDE.md` §Validation: Tiger 1.17.0, `docs/tools/px_lsp_diagnostics.js common events localization`, and `python docs/tools/px_vocab_check.py common events`. Tiger is the only scope check. `involved_activity` (act.001, act.002), `scope:activity` (act.004), and `scope:eotg_champion`, `scope:eotg_flagged`, `scope:eotg_delegation_leader` blocks are character or activity scope as used by the host's existing options.
1. **Count.** `grep -cE '^\s*trait = eotg_(cybernetics|neurofractured|total_integration)\s*$' events/eotg_augmentation_*.txt`, summed, returns **16**; today it returns **0**. The 16 `name =` lines of §3 each exist exactly once.
2. **Shape.** Each row has:
   - its §5.2 hardware gate in `trigger`, using the existing tier triggers only (no new trigger keys: `git diff common/scripted_triggers/` is empty);
   - the personality `has_trait` where the row has one, plus the listed extra guard;
   - the `trait =` lines in the §5.1 order;
   - `ai_chance` with `base = 30` and exactly the two modifiers of §5.2.
3. **Signature (invariant 5).**
   - Each of rows 2–4, 6–8 and 10–16 calls `eotg_add_fracture_risk` with the §5.2 amount inside `hidden_effect`. Row 8 calls it twice: on root, and inside `scope:eotg_champion`.
   - Rows 1, 5 and 9 contain the end.040.b residue block inside `hidden_effect`.
   - Rows 1 and 9 also move other characters' risk as listed.
   - No row calls `eotg_aug_set_integration_effect`, `eotg_aug_voice_advance_effect` or `eotg_aug_remove_all_effect`.
4. **Hidden risk.**
   - tier3.006.e reads `eotg_aug_pressure_flicker` only inside `hidden_effect`.
   - In the 19 new loc lines, `grep -nE '\b(risk|odds|chance)\b|[0-9]'` returns nothing.
   - No `basic_counter` or `visible = yes` is added anywhere.
5. **Visible-option cap.** For each of the 11 hosts, the most options visible at once matches §5.4 (≤ 5). QA verifies this with a scratch script that enumerates trait combinations, treating vanilla opposites (cynical/zealous, deceitful/honest, gregarious/shy, compassionate/callous) and the hardware traits (`opposites` in `eotg_augmentation_traits.txt`) as exclusive.
6. **No firing or trigger change.** `git diff common/on_action/` is empty. No hunk touches any event's `trigger`, `immediate`, `desc` or existing option.
7. **Excluded set untouched.** `git diff` shows no hunk in:
   - `events/eotg_augmentation_{countdown,patron,heir,retinue,endgame,procedures,interactions,tamper,realm,initiation}.txt`;
   - any `eotg_frontier*` file;
   - tier2.010, tier2.018, tier3.020;
   - the G9 hosts.
   No new option calls `create_story`, `end_story`, or sets a story stage variable.
8. **Built behaviour intact.**
   - No row calls `eotg_aug_procedure_effect`, `eotg_aug_pay_procedure_effect` or `eotg_aug_save_surgeon_effect`.
   - No row reads `eotg_aug_has_surgeon_for`, `eotg_aug_clinic_open`, `eotg_aug_under_policy` or `eotg_aug_removal_kind`.
   - Rows 4 and 5 call only `eotg_aug_act003_examine_effect`.
9. **Loc mechanical.** The 19 keys of §7 each exist once in the tree. The BOM is intact, there is no `[scope:`, and `python docs/tools/qa/loc_mechanical.py` reports no new missing or duplicate key. PX `locCoverage` reports no missing `eotg_` key.
10. **Register greps.**
    - In the rows 3, 6 and 16 loc lines, `grep -niE 'void|orrin|kyros|\beye\b|breach|rift|whisper|edge of hearing|hollow|answers|speaks from|prison|possess|demon|pact|abyss|frenzy|\bgrip\b|carrigore'` returns nothing.
    - In all 19 lines, `grep -niE 'humanity|\bhuman\b|god forgive|thank god|galactic|league|blackstar|helix|trauma team'` returns nothing.
    - Lore-keeper routine pass: no must-fix.
11. **Human, in game (temporary map).** Set up through the console lines in `docs/qa/generated/console_recipes.md`:
    - Enhanced: `effect eotg_aug_initiate_effect = yes`, then `effect add_trait_xp = { trait = eotg_cybernetics value = 50 }`. Overclocked: the same with `value = 100`.
    - Neurofractured: `add_trait eotg_neurofractured`, then `effect set_variable = { name = eotg_aug_voice value = 3 }`.
    - Seamless: `add_trait eotg_total_integration`, then `effect set_variable = { name = eotg_aug_residue value = 3 }`.

    Then check:
    - Each row appears only in its state, with both icons where listed. The Seamless rows show the placeholder icon until the art lands.
    - tier3.006.e: with `eotg_fracture_risk` at 10, the result is the *clean* toast; at 50, the *strained* toast. The option tooltip never shows the condition.
    - tier2.016.d is absent in the culprit outcome. In the malfunction outcome it removes Tampered.
    - act.003 with a just Enhanced host shows e and not f.
    - Five options at once in act.002, act.004 and nr.003 fit the window without scrolling (CB-34 item 7).

---

## 10. Deferred

| Item | Why |
|---|---|
| The Seamless option icon | `trait = eotg_total_integration` points at the existing art debt `gfx/interface/icons/traits/eotg_total_integration.dds`. The trait definition already accepts the missing icon. If the human would rather the option show no icon until the art lands, the scripter drops that one line from rows 1, 5 and 9. The trigger still gates. |
| A second Augmented-tier row | Only act.004.g gates on Augmented. Few cross-state events give a first fitting something distinct to do, and the tier1 pool events are saturated. Revisit if suggestion H4 is approved. |
| act.005 / act.006 hardware rows | act.005 already shows 5. act.006 is a faith reaction, and the zealous-versus-Industrial-Survivalism deferral (index §5) holds until v2 has faiths. |
| tier3.016 *The Bleed* [diligent, "sort the warnings"] | A decent fit, but the event already has 4 hardware options and fires .022. Keep it for a later pass. |
| Phase 0 §2.4 / trait-depth tables | Unchanged: no helper body changes in this batch. |
| CB-42 seller names in tier2.014.d | Once CB-42 lands, the localizer may swap "their" for the vendor name functions. That is not a mechanic change. |

### 10.1 Suggestions for the human (each would need a NEW event; not specced)

- **H1. tier3.024 *The Engagement*.** An Overclocked, wrathful "close the gap myself" after an overreach needs a counterstroke battle beat, with war state and casualties. As an option on the outcome notice it would be an escape hatch from the outcome.
- **H2. fracture.020 *What the Record Shows*.** A voice option, "let it amend the file", only means something if a later beat finds the altered record (an heir or a councillor reading it). Without that beat it is a free pass on tyranny already applied.
- **H3. nr.005 / nr.006, liege and champion.** An augmented liege calibrating a changed or broken champion side by side wants its own scene. Both events already show 5–6 options, and any machine-to-machine framing must stay under the tech ceiling (no networked implants).
- **H4. An Augmented-tier social beat.** For example, a guest at court asks to hold the first-fitted hand. It would give tier 1 its own cross-state moment; today only act.004.g has one.

### 10.2 Questions

- **For the orchestrator:** row 16 (fracture.029.c) is the one borderline inclusion (§5.3). Keep it, or drop it to make 15 options in 10 events?
- **For the human:** accept the placeholder Seamless icon on rows 1, 5 and 9, or show no icon until the art lands (§10)?
- **No canon question.** The voice, Seamless and tech-ceiling constraints are all settled by the ERRATA and the procedures lore rulings.

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Add the 16 options of §5.2 to their 11 host events (shape §5.1, gates are the existing tier triggers, risk/residue moves in hidden_effect), update the three modifier caller comments, touch nothing else (§9 items 6–8), then run the three validators.
- files: docs/specs/cybernetics_v2_tier_options.md
- needs-loc: eotg_aug_act.001.f, eotg_aug_act.002.f, eotg_aug_act.002.g, eotg_aug_act.003.f, eotg_aug_act.003.g, eotg_aug_act.004.f, eotg_aug_act.004.g, eotg_aug_nr.003.f, eotg_aug_nr.003.g, eotg_aug_tier2.014.d, eotg_aug_tier2.016.d, eotg_aug_tier2.021.c, eotg_aug_tier2.021.d, eotg_aug_tier3.006.e, eotg_aug_tier3.006.e.tt, eotg_aug_tier3.006.e.clean, eotg_aug_tier3.006.e.strained, eotg_aug_tier3.019.d, eotg_fracture.029.c (proposed text and register in §7)
- needs-lore: routine pass on the 19 lines, especially the voice-register rows (act.002.g, act.004.f, fracture.029.c) and the Seamless rows (act.001.f, act.003.g, nr.003.g)
- needs-human: §9 item 11 in-game checks; Seamless placeholder icon on rows 1/5/9 (keep or drop the line); orchestrator call on fracture.029.c (§5.3); suggestions H1–H4 (§10.1) are for the human's yes/no, not for building
