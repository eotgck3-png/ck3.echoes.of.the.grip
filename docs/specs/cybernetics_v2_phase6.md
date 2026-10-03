# Cybernetics v2 — Phase 6: the non-ruler lifecycle

Index: [cybernetics_v2.md](cybernetics_v2.md). Rules in index §1 apply. Needs Phase 0. Reads, but does not need, Phase 5's retinue flags.

**Purpose & gate.** Gate 3. Not blocked.

Today, augmented knights and courtiers are frozen at Augmented forever (audit §1.7i; content gaps §2.8), and v1 design intent #3 is unmet: *"rulers, knights, generals and courtiers take part"*. This phase lets them:
- progress;
- break;
- reach their **liege** as events: "your champion attacked a guard".

It also makes tier3.007 *Two Machines*, init.005 *A Familiar Change*, fracture.024 *The Familiar Change* and init.019 *The Arms Race* reachable through courtiers, not just landed peers.

**Signature resource.** Each non-ruler carries their own `eotg_fracture_risk`, which accrues at tier 3, cascades at 80, and drifts once fractured. Every liege-facing event moves the **champion's** risk or changes their tier.

---

## 1. Wiring

`random_yearly_everyone_pulse`: verified, PX `on_actions.log:2123`; `game/common/on_action/yearly_on_actions.txt:3172` ("once a year for all characters, at a random point"). Extended additively:
```
random_yearly_everyone_pulse = { on_actions = { eotg_on_yearly_aug_nonruler_check } }
```

**`eotg_on_yearly_aug_nonruler_check`.** Root is the non-ruler. The hook fires for **every** character, so the trigger is ordered cheapest-first:
```
trigger = {
    OR = { has_trait = eotg_cybernetics  has_trait = eotg_neurofractured  is_knight = yes }
    highest_held_title_tier < tier_county
    is_alive = yes
    is_adult = yes
    exists = employer
    employer = { highest_held_title_tier >= tier_county }
}
```
`employer` is a vanilla event target ("Get employer of scoped character", PX `event_targets.log`). In the effect, save `employer` as `scope:eotg_nr_liege`.

Effect order:

| Step | Applies to | Effect |
|---|---|---|
| 1. NR-01 offer | `is_knight = yes`, `eotg_is_augmented_any = no`, and the liege has `eotg_cybernetics`, or ≥1 augmented knight, or `eotg_flag_aug_want_more` | 3%: fire **nr.001** to the liege (cooldown below) |
| 2. Progression | `eotg_is_aug_tier1/2` | 4% a year (8% if `eotg_flag_aug_iron_retinue` **and** the liege has `eotg_flag_aug_retinue_permanent`): `eotg_aug_set_integration_effect = { XP = 50 / 100 }`. Silent; nr.002 reports it. |
| 3. Accrual | `eotg_is_aug_tier3` | `eotg_add_fracture_risk`: +6, +6 more at `stress_level >= 2`. If risk ≥ 80 → `eotg_aug_nr_cascade_effect` (§2), which fires **nr.006** to the liege and ignores cooldown. |
| 4. Drift | `has_trait = eotg_neurofractured` | +6 a year |
| 5. Liege event | NOT `eotg_flag_aug_nr_cooldown` **on the liege** | one `random_list`, then the flag is set on the liege (`years = 1`) |

The step-5 list, with the trigger on the champion:

| Weight | Trigger | Event |
|---|---|---|
| 10 | `is_knight = yes`, tier 1–2 | nr.002 *Your Champion's New Edge* |
| 15 | tier 2–3, risk ≥ 30 | nr.003 *Something Is Wrong With Them* |
| 20 | tier 3 with risk ≥ 60, or Neurofractured | nr.004 *The Champion's Mistake* |
| 10 | `is_knight = no`, tier 2+ | nr.005 *The Familiar Change* |
| 100 | — | nothing |

Weights ×1.5 for `eotg_flag_aug_iron_retinue` characters (`modifier = { factor = 1.5 … }`).

Before firing, `save_scope_as = eotg_champion`, then `scope:eotg_nr_liege = { trigger_event = { id = … days = { 1 30 } } }`. Saved scopes travel with the triggered event. The cooldown flag lives on the liege, in this on_action only.

The liege's own `yearly_playable_pulse` on_actions are untouched. Non-rulers never enter `eotg_on_yearly_aug_*`, because those hooks only fire for count+ characters.

## 2. Effect

**`eotg_aug_nr_cascade_effect`** (`common/scripted_effects/eotg_augmentation_effects.txt`). The ruler-side `eotg_trigger_neurofracture` fires fracture.0001, a ruler event, so it is **not** reused for non-rulers:
```
remove_trait = eotg_cybernetics
add_trait = eotg_neurofractured
eotg_apply_neurofracture_distortion = yes
set_variable = { name = eotg_fracture_risk  value = 0 }
save_scope_as = eotg_champion
employer = { trigger_event = { id = eotg_aug_nr.006  days = { 1 7 } } }
```

## 3. Events (`events/eotg_augmentation_nonruler.txt`, namespace `eotg_aug_nr`)

Root is the liege. `scope:eotg_champion` is the non-ruler. Every event's `trigger` is `exists = scope:eotg_champion` plus `scope:eotg_champion = { is_alive = yes }`, which is a world-state guard. Risk moves are on the champion unless stated.

**nr.001 The Champion Volunteers (NR-01).**
- **a** "Granted." `minor_gold_value`. The champion runs `eotg_aug_initiate_effect` (risk 0).
- **b** "Denied." The champion gets unease.
- **c** "Granted, if they pay for it." Install at no cost; the champion gets unease.
- **d [generous]** "At my expense, and properly." Install + `eotg_mod_implant_calibrated` 3 years. `medium_gold_value`.
- **e [paranoid]** "Why do you want to be stronger than me?" The champion gets fear.

**nr.002 Your Champion's New Edge (NR-02).** The desc names their new tier.
- **a** "Reward them." `minor_gold_value`. Admiration. Risk +3.
- **b** "Keep an eye on them." —
- **c** "Front line, every battle." +50 prestige for root. Risk +8.
- **d [ambitious]** "I want more of them." The liege gets `eotg_flag_aug_want_more` 5 years, which raises nr.001's base chance to 6% and the Arms Race weight ×1.5.
- **e [craven]** "Keep them beside me." Admiration. Risk −3.

**nr.003 Something Is Wrong With Them (NR-03).**
- **a** "Pay for their maintenance." `minor_gold_value`. Risk −10.
- **b** "Relieve them of duty." Disgust. Risk −5.
- **c** "Ignore it." Risk +5.
- **d [compassionate]** "Sit with them." Reassured. Risk −8.
- **e [callous]** "Work them until it breaks." +25 prestige. Risk +10.

**nr.004 The Champion's Mistake (NR-04).** `immediate`: `eotg_aug_pick_victim_effect = { NAME = eotg_victim  FAMILY_FACTOR = 0.05 }` in the liege's scope (root = liege, so the picker's `root` exclusions are right). Exclude the champion with a wrapper limit. The victim is wounded (`REASON = attacked`). No victim: "they attacked a door, a bulkhead, themselves", and the champion gets `wounded_1`.
- **a** "Imprison them." `imprison = { target = scope:eotg_champion  type = dungeon }`. Helper tyranny. Risk −5.
- **b** "Pay off the victim." `minor_gold_value`. Risk +5.
- **c** "Restrain them, and have them treated." `medium_gold_value`. Risk −10.
- **d [just]** "A trial." +50 prestige; then as a.
- **e [sadistic]** "Let them finish." `scope:eotg_victim = { death = { death_reason = death_murder  killer = scope:eotg_champion } }`. +20 dread. Helper murder (sadistic loses stress). Risk +5.

Options a–d carry helper wound for the liege: their champion, their responsibility.

**nr.005 The Familiar Change (NR-05).** `immediate`: `scope:eotg_champion = { eotg_aug_scramble_personality_effect = yes }` (Phase 3a effect). **If Phase 3a has not shipped,** use `add_trait = paranoid` when they are not `trusting` and not already paranoid. The desc names what changed.
- **a** "Talk to them." Risk −5.
- **b** "Send them away." `move_to_pool`.
- **c** "Watch." Risk +3.
- **d [compassionate]** "They're still in there." Reassured. Risk −8.
- **e [paranoid]** "Lock them in their rooms." `imprison` house arrest. Risk −3.

**nr.006 The Broken Champion (NR-06).** Fired by `eotg_aug_nr_cascade_effect`, outside the cooldown.
- **a** "Restrain them." `imprison` house arrest. Risk −10.
- **b** "Cut it out of them." `medium_gold_value`. `random_list`: 30 death (`death_treatment`, −15 if `eotg_has_physician_access`); 70 `eotg_aug_remove_all_effect`, plus 30% `maimed`. Tier exit.
- **c** "Protect them." Admiration. Risk +5. They stay: a Neurofractured knight with +14 prowess.
- **d** "Execute them." `death_execution`, killer root. Helper murder.
- **e [compassionate]** "I'll care for them myself." As c, + reassured. Risk −5.
- **f [callous]** "Point them at the enemy." Risk +10. Root gets lesson martial.

## 4. Loc (≈ 40 keys)
- 6 events × ~6 keys;
- nr.004 no-victim variant;
- nr.005 trait-change variant (generic, plus the vanilla trait-gain tooltip);
- nr.002 tier-name variants (2).

## 5. Definition of done
0. **Validation, all three clean** on the phase's files, except the known-benign items listed in `CLAUDE.md` §Validation: Tiger 1.17.0 (scratch descriptor), `docs/tools/px_lsp_diagnostics.js` (PX language server, headless) and `docs/tools/px_vocab_check.py` (engine vocabulary + dead hooks). Tiger is the only one of the three that checks scope.
1. `random_yearly_everyone_pulse` is extended only via `on_actions = { eotg_on_yearly_aug_nonruler_check }`. The trigger's first line is the cheap trait/knight `OR`.
2. The liege cooldown flag is set only in the on_action. No `eotg_aug_nr` event checks it.
3. Non-rulers never call `eotg_trigger_neurofracture`.
4. QA reachability: tier3.007 and fracture.024 are now reachable through courtiers, not only landed peers.
5. **Human, in game:** a count with an augmented knight sees progression within ~10–20 years, or immediately via console (`add_trait_xp` on the knight). An Overclocked knight with risk 85 produces nr.006 within a year.
