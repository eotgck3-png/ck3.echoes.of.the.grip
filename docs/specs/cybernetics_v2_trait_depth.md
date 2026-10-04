# Spec: Cybernetics v2 — thin-trait depth (G9)

**Author:** eotg-architect, 2026-10-04
**Authorised by:** the human approved G9 of [`docs/qa/cybernetics_content_gaps_v2.md`](../qa/cybernetics_content_gaps_v2.md) on 2026-10-04 (relayed by the coordinator). The approval covers **trait-gated options on existing events only. No new events.**
**Builds on:** [cybernetics_v2.md](cybernetics_v2.md) (the index; §1 rules 4, 5, 6, 9, 10, 11 and the §5 register bind every line here), [cybernetics_v2_phase0.md](cybernetics_v2_phase0.md) §2.4 (stress helpers), [cybernetics_v2_balance.md](cybernetics_v2_balance.md) §10 (where this item was deferred).
**State read:** the working tree on `v2-space-map` after `82defbd`, including the uncommitted, QA-passed Cybernetics batch. That batch was committed as `eca9b9c`, and this spec was re-checked against `eca9b9c` on 2026-10-04. No `eca9b9c` hunk falls inside any of the eight host events. Helper bodies, caller counts (37 reject, 18 neglect), on_action lines and modifier keys match. Event ids and option letters are as they stand there.

---

## 1. Purpose & gate

Six vanilla personality traits have only one or two trait-gated options across the 153 cybernetics events: chaste, fickle, impatient (1 each), lustful, gluttonous and temperate (2 each). Forgiving and arbitrary have one each. This spec adds **one trait-gated option per trait, eight in total**, each on an existing choice event. It also decides which Phase 0 stress helper, if any, each of the six thin traits joins, based on vanilla co-occurrence.

**Gate 3 (Systems).** Cybernetics is a mod-exclusive system and is built against the temporary map (index header; `docs/agent_workflow.md` §5 rule 2). **Not blocked.** Nothing here references a title, province, character, culture or faith (index §1 rule 9).

**Avoided on purpose.** A parallel spec in progress (procedures, providers and repairs: gaps v2 Part 1) changes these, so this spec touches none of them:
- `eotg_aug_init.018` and `init.010`, `init.011`, `init.012`;
- `tier1.002`, `tier1.021`, `tier1.022`;
- `tier2.003`, `tier2.013`, `tier2.014`;
- `end.001`;
- the rejection chain `tier1.013`–`.015`;
- every upgrade, removal or repair decision: Seek, Pursue the Next Stage, Remove Implants, Excision, Partial Removal, Downgrade Protocol, Consult the Physician.

The helper edits in §5.2 change a shared effect body, not those events. The providers spec author still needs to know, because new callers it adds will inherit the new rows.

---

## 2. Signature resource

**`eotg_fracture_risk`** (character variable, 0–100, hidden: index §1 rule 3), plus tier through `eotg_aug_set_integration_effect`.

Each of the eight new options calls `eotg_add_fracture_risk`: seven on root, and one (nr.004.f) on the saved augmented character `scope:eotg_champion`, as index §1 rule 4 allows. None changes tier. Direction follows rule 4:
- below Overclocked, all moves are **+** (tier1.005.f, tier1.007.f, tier2.004.e, tier2.020.f);
- at Overclocked, one option is a **−** move (tier3.010.f, temperate), and it pays for the cut with a modifier;
- the non-ruler option moves the champion's risk **+**.

No option shows a number (Q1).

---

## 3. Identifier table

**No new identifiers.** Every key below already exists in the tree and was checked there.

| Key | Type | Defined in | Used by |
|---|---|---|---|
| `eotg_add_fracture_risk` | scripted effect (param `AMOUNT`) | `common/scripted_effects/eotg_augmentation_effects.txt` | all 8 |
| `eotg_aug_stress_reject_effect` | scripted effect | same | gains 3 rows (§5.2) |
| `eotg_aug_stress_neglect_effect` | scripted effect | same | gains 1 row (§5.2) |
| `eotg_aug_stress_tyranny_effect` | scripted effect | same | tier3.021.d |
| `eotg_aug_voice_advance_effect` | scripted effect (param `STAGE`) | same | tier2.020.f (as every .020 option) |
| `eotg_mod_implant_calibrated` | static modifier | `common/modifiers/eotg_augmentation_modifiers.txt` | tier1.007.f |
| `eotg_mod_aug_dulled_senses` | static modifier | same | tier3.010.f (update its `# Caller:` comment) |
| `eotg_opinion_aug_reassured` (+15, timed) | opinion modifier | `common/opinion_modifiers/eotg_augmentation_opinions.txt` | tier2.004.e, nr.004.f (update its caller comment) |
| `eotg_opinion_aug_unease` (−10) | opinion modifier | same | tier2.004.e |
| `eotg_opinion_aug_disgust` (−20) | opinion modifier | same | nr.004.f |
| `eotg_opinion_aug_falsely_accused` (−30, applied `years = 10`) | opinion modifier | same | tier3.021.d (update its caller comment) |
| `eotg_aug_marriage_strain` | character variable | tier2.004 / .017 / .018 | tier2.004.e |
| `scope:eotg_aug_spouse`, `scope:eotg_delegate`, `scope:eotg_champion`, `scope:eotg_victim` | saved scopes | the host events' `immediate` or the chain | as named |

**New option keys** (option names, dot form per the index "Decided here" ruling; the letter is the next free one in each event):

| Event | New option | Trait |
|---|---|---|
| `eotg_aug_tier1.005` Weight of Silence | **f** | gluttonous |
| `eotg_aug_tier1.007` Firmware Itch | **f** | impatient |
| `eotg_aug_tier2.004` The Space Between Us | **e** | chaste |
| `eotg_aug_tier2.020` The Second Self | **f** | fickle |
| `eotg_aug_tier3.003` Sleepless | **f** | lustful |
| `eotg_aug_tier3.010` Heat Spike | **f** | temperate |
| `eotg_aug_tier3.021` The Other Order | **d** | arbitrary |
| `eotg_aug_nr.004` The Champion's Mistake | **f** | forgiving |

Every trait key was checked in `game/common/traits/00_traits.txt` (index rule 10):

| Trait | Line |
|---|---|
| lustful | 2251 |
| chaste | 2307 |
| gluttonous | 2361 |
| temperate | 2403 |
| impatient | 2961 |
| arbitrary | 3750 |
| fickle | 4386 |
| forgiving | 4561 |

None is a childhood trait.

No icons, CoAs or name lists are needed. `trait = X` uses vanilla trait icons.

---

## 4. File placement

| File | Change |
|---|---|
| `events/eotg_augmentation_tier1.txt` | add tier1.005.f, tier1.007.f |
| `events/eotg_augmentation_tier2.txt` | add tier2.004.e, tier2.020.f |
| `events/eotg_augmentation_tier3.txt` | add tier3.003.f, tier3.010.f, tier3.021.d |
| `events/eotg_augmentation_nonruler.txt` | add nr.004.f |
| `common/scripted_effects/eotg_augmentation_effects.txt` | 4 new rows in two helpers (§5.2) |
| `common/modifiers/eotg_augmentation_modifiers.txt` | caller comment on `eotg_mod_aug_dulled_senses` only |
| `common/opinion_modifiers/eotg_augmentation_opinions.txt` | caller comments on `_reassured`, `_falsely_accused` only |
| `localization/english/eotg_augmentation_l_english.yml` | 8 option keys (§7) |

Each new option goes **after the host event's last existing option**, with the file's usual one-line comment above it (`# [trait] "Text."` and a short why).

---

## 5. Wiring

### 5.0 Firing (unchanged)
No on_action, branch, weight or cooldown changes. The options become reachable as soon as their host events are, and every host is already fired:

| Host | Fired by | Tier |
|---|---|---|
| tier1.005, tier1.007 | `eotg_on_yearly_aug_tier1_check` (`common/on_action/eotg_augmentation_on_actions.txt:486`; branches at :530, :542) | Augmented |
| tier2.004, tier2.020 | `eotg_on_yearly_aug_tier2_check` (:661; branches at :693, :789) | Enhanced |
| tier3.003, tier3.010 | `eotg_on_yearly_aug_overclocked_check` (:802; branches at :917, :972) | Overclocked |
| tier3.021 | chain stage from tier3.019 a/c (`events/eotg_augmentation_tier3.txt` `trigger_event … days = { 180 360 }`) | Overclocked |
| nr.004 | `eotg_on_yearly_aug_nonruler_check` (:1412; branch at :1583) | non-ruler (augmented champion) |

**Cooldown authority** stays in those on_actions and chains (index §1 rule 5). No new option sets or reads a cooldown flag, and no event `trigger` changes.

### 5.1 The eight options

**Shared shape** (index §1 rule 6), for all eight:
```
option = {
    name = eotg_aug_<event>.<letter>
    trigger = { has_trait = <trait> }      # plus any extra guard listed below
    trait = <trait>
    ...effects...
    ai_chance = {
        base = 30
        modifier = { add = 30  has_trait = <trait> }
        modifier = { add = 10  has_trait = <secondary> }
    }
}
```
This is the file's existing gated-option pattern (e.g. tier1.005.d/.e, tier3.010.d/.e). It meets the index requirements of base 30 inside the 10–40 range and at least two trait modifiers.

| # | Option | Trait / extra guard | Effects (in order) | Stress | `ai_chance` secondary | Why this home |
|---|---|---|---|---|---|---|
| 1 | **tier1.005.f** "Reach for the platter." | gluttonous | `eotg_add_fracture_risk = { AMOUNT = 3 }` · no prestige change | inline `stress_impact = { gluttonous = minor_stress_impact_loss }` | `content` +10 | The pause happens at a formal gathering, where food is on the table. Gluttonous covers the processing gap by eating, so the court reads appetite, not malfunction. It avoids the −25 prestige that a and b pay. Hiding the symptom is what lets it grow (+3, the same figure as a). |
| 2 | **tier1.007.f** "Now. Not this week. Now." | impatient | `add_character_modifier = { modifier = eotg_mod_implant_calibrated  years = 1 }` · `eotg_add_fracture_risk = { AMOUNT = 4 }` | inline `stress_impact = { impatient = minor_stress_impact_loss }` | `arrogant` +10 | The desc is a window the ruler has to wait for. Impatient won't wait: the update goes in now, mid-court, without the technicians' preparation. Compared with a, it is free and calibrates for the same year, but it costs +4 risk. Compared with c, it is certain but carries risk. Neither universal option is made pointless (rule 6). |
| 3 | **tier2.004.e** "We were never held together by hands." | chaste | `if = { limit = { scope:eotg_aug_spouse = { has_trait = chaste } }` → spouse `add_opinion = { modifier = eotg_opinion_aug_reassured  target = root  years = 5 }`, `set_variable = { name = eotg_aug_marriage_strain  value = 0 } }` `else` → spouse `add_opinion = { modifier = eotg_opinion_aug_unease  target = root  years = 5 }`, `set_variable = { name = eotg_aug_marriage_strain  value = 1 } }` · `add_piety = 50` · `eotg_add_fracture_risk = { AMOUNT = 2 }` · `trigger_event = { id = eotg_aug_tier2.017  days = { 180 365 } }` (**required**: every .004 option fires stage 2) | inline `stress_impact = { chaste = minor_stress_impact_loss }` | `zealous` +10 | The spouse asks when the warmth left the ruler's hands. A chaste ruler answers that touch was never the bond. A chaste spouse agrees (strain 0). Anyone else hears an evasion (strain 1, the same as option b's denial). The implant's affect channel is left as it is (+2). This seeds the existing Confrontation → Resolution chain and needs no new beats. |
| 4 | **tier2.020.f** "Let it guess. I will have changed my mind." | fickle | `eotg_aug_voice_advance_effect = { STAGE = 1 }` (**required**: every .020 option advances to stage 1, thread T1) · `eotg_add_fracture_risk = { AMOUNT = 5 }` | inline `stress_impact = { fickle = minor_stress_impact_loss }` | `eccentric` +10 | The event is the implant's model of you running half a second ahead. A fickle mind is the one self that model cannot pin down, so it has to keep re-learning (+5, between c's 4 and b's 6). This is the strongest natural fit outside the excluded regression decisions (§1). |
| 5 | **tier3.003.f** "Then I won't spend them alone." | lustful | `eotg_add_fracture_risk = { AMOUNT = 10 }` | inline `stress_impact = { lustful = minor_stress_impact_loss }` | `gregarious` +10 | The implant says the body no longer needs sleep. Lustful fills the nights with company instead of work. It mirrors d (diligent, +10) at the same risk, trading d's gold for stress relief. Tone precedent: vanilla's lustful coping line `stress_threshold.2301.desc.lustful` (`localization/english/event_localization/stress_events/stress_threshold_events_1_l_english.yml:140`). The option text stays at that register, with nothing explicit. |
| 6 | **tier3.010.f** "Run it at half, and keep it there." | temperate | `add_character_modifier = { modifier = eotg_mod_aug_dulled_senses  years = 2 }` · `eotg_add_fracture_risk = { AMOUNT = -8 }` | inline `stress_impact = { temperate = minor_stress_impact_loss }` | `patient` +10 | Temperate chooses the sustainable setting, not the full shutdown (c: −10 and −50 prestige; e: −12 and −100 prestige). It takes less risk off, pays no prestige, and accepts two dulled years. This is the one − move, and it sits at Overclocked as rule 4 requires. |
| 7 | **tier3.021.d** "It was their hand. It is their fault." | arbitrary | `scope:eotg_delegate = { add_opinion = { modifier = eotg_opinion_aug_falsely_accused  target = root  years = 10 } }` · `add_dread = 10` · `eotg_add_fracture_risk = { AMOUNT = 5 }` · **does not read** `scope:eotg_order_truth` | `eotg_aug_stress_tyranny_effect = yes` (already carries `arbitrary = minor_stress_impact_loss`; no inline row, so there is no double relief) | `callous` +10 | The event has 3 universal options and no gated one. Arbitrary blames the delegate whatever the logs would show; that indifference to the truth is the trait. It is harsher than b (falsely accused −30 for 10 years instead of disgust −20 for 5) and buys dread. The opinion is always "falsely accused" because the delegate always believes they acted on your order (desc: "carried it out in good faith"). |
| 8 | **nr.004.f** "They did not choose this. Let it go." | forgiving (the event trigger already guarantees the champion is free) | `scope:eotg_champion = { add_opinion = { modifier = eotg_opinion_aug_reassured  target = root  years = 5 }  eotg_add_fracture_risk = { AMOUNT = 5 } }` · `if = { limit = { exists = scope:eotg_victim  scope:eotg_victim = { is_alive = yes } }  scope:eotg_victim = { add_opinion = { modifier = eotg_opinion_aug_disgust  target = root  years = 5 } } }` | inline `stress_impact = { forgiving = minor_stress_impact_loss  just = minor_stress_impact_gain }`, **no** `eotg_aug_stress_wound_effect` (see note) | `compassionate` +10 | The desc says outright "the champion did not mean it". Forgiving lets it pass: no prison, no treatment, so the champion's risk climbs (+5, as b). The victim, if alive, resents it. |

**Note on 8 (helper omission).** Every other nr.004 option calls `eotg_aug_stress_wound_effect`. That helper gives `forgiving = minor_stress_impact_gain`, which would cancel this option's own relief. This is the case conformance ruling **M10** already ratified for nr.004.d (`docs/specs/cybernetics_v2_conformance_rulings.md:35`): a trait option omits a helper whose row for that trait would cancel the option's relief. The inline block follows the vanilla mercy shape in `events/court_events/court_events_general.txt:1246–1250` (court.0111.b: vengeful and wrathful gain, forgiving loss). Vengeful is the vanilla opposite of forgiving, so it is never present here and is dropped. `just` gains because nothing was judged.

**Rule-6 visibility check** (most gated options visible at once):
- tier1.005: shy and gregarious are opposites, so at most 2 show.
- tier1.007: diligent and lazy are opposites, so at most 2.
- tier2.004: deceitful + chaste, at most 2.
- tier3.003: diligent and lazy are opposites, so at most 2.
- tier3.010: brave and craven are opposites, so at most 2.
- tier3.021: 1.
- tier2.020 and nr.004 can show **3** for a rare combination:
  - tier2.020: eccentric + shy + fickle;
  - nr.004: just + sadistic + forgiving.

  This is accepted on the precedent of balance §5.9, which let tier1.010 reach 8 options with about 4 visible. No universal option loses its point.

### 5.2 Stress helpers: which trait joins which

**Method.** The vanilla trait definitions in `00_traits.txt` carry no per-trait stress triggers; stress lives in each event's `stress_impact` block. So "the vanilla definition" was read as **how vanilla's own stress blocks pair each trait with the traits our helpers already contain**.

1. A script scanned every `stress_impact` and `stress_and_fulfillment_impact` block under `game/events` and `game/common` (the 1.20 install). The 1.20 rename to `stress_and_fulfillment_impact` is cosmetic: plain `stress_impact` still appears 187 times in 1.20 vanilla, and the mod keeps it.
2. A block counted as "matching" a helper when at least 2 of the helper's rows appear in it with the same sign, and none with the opposite sign.
3. A trait joins a helper only when that helper clearly leads the field for one sign of the trait. Otherwise it stays inline-only.

| Trait | Vanilla blocks (gain / loss) | Strongest helper match | **Decision** | Evidence (vanilla option, file:line) |
|---|---|---|---|---|
| **impatient** | 448 / 139 | gain ↔ **reject**: 45 blocks, 5× the next helper | **Join `eotg_aug_stress_reject_effect`: `impatient = minor_stress_impact_gain`.** Restraint and refusal are waiting. | hunt.8070.b "Just wait" (`events/activities/hunt_activity/jb_hunt_events.txt:1288`: impatient gain, patient and humble loss); pilgrimage.2006.b (`events/activities/pilgrimage_activity/pilgrimage_events.txt:3330`: impatient gain, patient and humble loss) |
| **temperate** | 180 / 68 | loss ↔ **reject**: 13, every other helper ≤ 2 | **Join `eotg_aug_stress_reject_effect`: `temperate = minor_stress_impact_loss`.** Taking less is relief. | ep3_laamp_flavor.0030.c "glad I'm free of that life" (`events/dlc/ep3/ep3_laamp_flavor.txt:602`: temperate, content, humble loss); az_debate.0002.d "cultivation without grasping" (`events/activities/debate_activity/az_debate_events.txt:575`: temperate and humble loss, ambitious gain). Gain is spread across all helpers (≤ 10%): no gain row. |
| **gluttonous** | 101 / 87 | gain ↔ **reject**: 10, every other helper ≤ 2 | **Join `eotg_aug_stress_reject_effect`: `gluttonous = minor_stress_impact_gain`.** Denial chafes. This is temperate's mirror, as vanilla pairs them. | legend_spread_events.5065.b "I will do better" (`events/dlc/ce1/legend_spread_events_nick.txt:2802`: gluttonous and cynical gain, temperate and zealous loss); `events/dlc/ep2/wedding_events/ep2_wedding_events.txt:7396` (gluttonous and arrogant gain, temperate and humble loss). Loss has no helper signal (≤ 4): no loss row. |
| **fickle** | 199 / 89 | loss ↔ **neglect**: 14 (reject 13, but in **mixed** blocks) | **Join `eotg_aug_stress_neglect_effect`: `fickle = minor_stress_impact_loss`.** Dropping a routine is relief. | bp2_adult_education.1010.c "opt-out" (`events/dlc/bp2/bp2_adult_education_activity_events.txt:1475`: diligent and ambitious gain, fickle and lazy loss); epidemic_events.5000.e "Don't be ridiculous" (`events/dlc/ce1/epidemic_events.txt:6119`: diligent gain, lazy and fickle loss). Reject is not used: its rows (ambitious gain) contradict the fickle-loss blocks about as often as they agree. |
| **lustful** | 209 / 159 | none: best 13 of 209 (wound, inherited from compassionate rows) and 10 of 159 (tyranny) | **No helper.** Lustful's vanilla stress is about intimacy, which no helper models. Inline only. | (absence) |
| **chaste** | 241 / 58 | none: best 15 of 241 (cruelty); loss ↔ reject 5 of 58, all in lust-specific blocks (`events/activities/pilgrimage_activity/pilgrimage_events.txt:8032`) | **No helper.** Chastity's stress is about sexual conduct, not refusing the machine. Inline only. | (absence) |
| forgiving | — | already in wound (minor gain), murder (medium gain), cruelty (minor gain) | **No change.** | Phase 0 §2.4 |
| arbitrary | — | already in tyranny (minor loss); trait has `stress_gain_mult = -0.5` (`00_traits.txt:3759`) | **No change.** | Phase 0 §2.4 |

**Resulting helper bodies** (new rows marked `# G9`):
```
eotg_aug_stress_reject_effect = {
    stress_impact = {
        ambitious = minor_stress_impact_gain
        arrogant = minor_stress_impact_gain
        cynical = minor_stress_impact_gain
        impatient = minor_stress_impact_gain    # G9
        gluttonous = minor_stress_impact_gain   # G9
        content = minor_stress_impact_loss
        zealous = minor_stress_impact_loss
        humble = minor_stress_impact_loss
        temperate = minor_stress_impact_loss    # G9
    }
}
eotg_aug_stress_neglect_effect = {
    stress_impact = {
        diligent = minor_stress_impact_gain
        paranoid = minor_stress_impact_gain
        lazy = minor_stress_impact_loss
        fickle = minor_stress_impact_loss       # G9
    }
}
```

**Blast radius.**
- `eotg_aug_stress_reject_effect` has 37 callers and `eotg_aug_stress_neglect_effect` has 18 (grep of `events/` and `common/decisions/`, current tree). The new rows reach all of them. That is the purpose: these traits react wherever the ruler refuses or neglects the machine.
- None of those caller options also has an inline row for impatient, temperate, gluttonous or fickle, so nothing double-counts (checked by script).
- The tier1.008.e / tier3.011.e temperate options and the tier3.008.e impatient option do not call these helpers, so they are unaffected.
- Callers in the excluded set (end.001.a, the removal decisions) also inherit the rows. The providers spec author should know, but the event files themselves are not touched.
- Also update the Phase 0 §2.4 table (`docs/specs/cybernetics_v2_phase0.md`) with the four rows. That is the orchestrator's or architect's doc edit, not the scripter's; listed in the handoff.

**Scale.** All rows are `minor`, matching the other non-headline rows of each helper and vanilla's predominant magnitude in the cited blocks.

---

## 6. Vanilla precedent

| Pattern | Vanilla | Used for |
|---|---|---|
| Trait-gated option, `trigger` + `trait` | index §1 rule 6 (from vanilla practice); the file's own tier1.005.d/.e, tier3.010.d/.e | all 8 |
| Mercy option stress (forgiving loss, vengeful/wrathful gain) | `events/court_events/court_events_general.txt:1246–1250` (court.0111.b) | nr.004.f |
| Waiting stresses impatient | `events/activities/hunt_activity/jb_hunt_events.txt:1288` (hunt.8070.b) | reject + impatient |
| Restraint relieves temperate, chafes gluttonous | `events/dlc/ce1/legend_spread_events_nick.txt:2802`; `events/dlc/ep3/ep3_laamp_flavor.txt:602` | reject + temperate / gluttonous |
| Opting out relieves fickle (with lazy) | `events/dlc/bp2/bp2_adult_education_activity_events.txt:1475`; `events/dlc/ce1/epidemic_events.txt:6119` | neglect + fickle |
| Lustful coping register | `localization/english/event_localization/stress_events/stress_threshold_events_1_l_english.yml:140` | tier3.003.f tone |
| Helper omitted when it cancels the option's own trait relief | conformance ruling M10 (`docs/specs/cybernetics_v2_conformance_rulings.md:35`) | nr.004.f |

**No deviation.** The one judgement call is tier3.021.d reading no truth flag. It is the trait's point, not a departure from vanilla.

---

## 7. Loc surface (eotg-localizer)

`localization/english/eotg_augmentation_l_english.yml`, UTF-8 BOM, dot form, one definition each. Place each key under its event's block, after the last existing option key. Proposed text; the localizer owns the final wording within §8.

| Key | Proposed text |
|---|---|
| `eotg_aug_tier1.005.f` | "Reach for the platter." |
| `eotg_aug_tier1.007.f` | "Now. Not this week. Now." |
| `eotg_aug_tier2.004.e` | "We were never held together by hands." |
| `eotg_aug_tier2.020.f` | "Let it guess. I will have changed my mind." |
| `eotg_aug_tier3.003.f` | "Then I won't spend them alone." |
| `eotg_aug_tier3.010.f` | "Run it at half, and keep it there." |
| `eotg_aug_tier3.021.d` | "It was their hand. It is their fault." |
| `eotg_aug_nr.004.f` | "They did not choose this. Let it go." |

**8 keys. No `custom_tooltip`, `triggered_desc` or `replace/` override is needed.**
- tier2.004.e's spouse branch shows through the engine's normal effect tooltip.
- No vanilla string changes.
- None of these lines may name a number for risk (Q1).

---

## 8. Lore constraints

- **Index §5 register applies to every line.** These eight are the ruler's own words, never the voice. tier2.020.f is about the voice, so it must not make the model external: "it" is the model of you, and nothing "answers", "whispers" or "speaks from" anywhere (§5 items 1–2). The proposed line refers to it as something that guesses, which is within the register.
- **No monotheistic invocation** (§5 item 4). tier2.004.e's piety comes from the effect, not from a prayer in the text.
- **"Self"/"personhood", never "humanity"** (§5 item 5). No line uses either.
- **Medieval leaks** (§5 item 6): "platter" and "hall" are already used in the existing tier1.005 and tier1.008 text; keep the existing register. No masons, palace, scribes or horses.
- **tier3.003.f stays non-explicit.** That is the tone of vanilla's own stress-coping lines (§6), and the content fires for every culture.
- **Zealous stays faith-neutral** (index §5, "Deferred: zealous vs Industrial Survivalism"). tier2.004.e uses zealous only as an `ai_chance` weight.
- Nothing here is uncertain canon. **No lore-keeper question.** The lore-keeper's normal pass over new loc applies.

---

## 9. Definition of done

0. **Validation, all three clean** on the touched files, except the known-benign items in `CLAUDE.md` §Validation (Tiger 1.17.0 with the scratch descriptor; `docs/tools/px_lsp_diagnostics.js`; `docs/tools/px_vocab_check.py`). Tiger is the only check of scope: `scope:eotg_delegate`, `scope:eotg_champion`, `scope:eotg_victim` and `scope:eotg_aug_spouse` blocks are character scope.
1. **Count.** `grep -nE "trait = (chaste|fickle|impatient|lustful|gluttonous|temperate|forgiving|arbitrary)\b" events/*.txt` (lines without `has_trait`) returns **chaste 2, fickle 2, impatient 2, lustful 3, gluttonous 3, temperate 3, forgiving 2, arbitrary 2** (today 1/1/1/2/2/2/1/1).
2. **Shape.** Each of the 8 options has `trigger = { has_trait = X … }` and `trait = X` with the same X, and `ai_chance` with `base = 30` and exactly the two trait modifiers of §5.1.
3. **Signature (invariant 5).** Each of the 8 calls `eotg_add_fracture_risk` with the §5.1 amount: 7 on root, nr.004.f inside `scope:eotg_champion`. QA audit 8 passes on the 8 host events.
4. **Required carry-overs.** tier2.004.e fires `eotg_aug_tier2.017` (`days = { 180 365 }`) and sets `eotg_aug_marriage_strain` to 0 or 1. tier2.020.f calls `eotg_aug_voice_advance_effect = { STAGE = 1 }`.
5. **Helpers.** `eotg_aug_stress_reject_effect` contains `impatient` gain, `gluttonous` gain and `temperate` loss. `eotg_aug_stress_neglect_effect` contains `fickle` loss. No other helper changes.
6. **No double relief.** tier3.021.d has no inline `arbitrary` row. nr.004.f does not call `eotg_aug_stress_wound_effect`.
7. **No firing change.** `git diff common/on_action/` is empty. No event `trigger = {}` changes.
8. **Excluded events untouched.** `git diff` shows no hunk inside init.010/.011/.012/.018, tier1.002/.013–.015/.021/.022, tier2.003/.013/.014, end.001, or `common/decisions/`.
9. **Loc.** The 8 keys of §7 each exist once in the tree, BOM intact, no `[scope:`. PX `locCoverage` reports no missing `eotg_` key.
10. **Human, in game (temporary map):**
    - console `add_trait gluttonous` on an Augmented ruler, then `event eotg_aug_tier1.005`: option f shows with the gluttonous icon;
    - repeat for each trait and host (impatient tier1.007; chaste tier2.004 while married; fickle tier2.020 with voice < 1; lustful tier3.003; temperate tier3.010);
    - tier2.004.e with a chaste spouse vs. a non-chaste spouse produces Reassured vs. Augmentation Unease;
    - picking "Reject the thought" (tier2.020.a) as an impatient ruler shows a stress gain line for impatient.

---

## 10. Deferred

| Item | Why |
|---|---|
| A second option each for chaste, fickle and impatient (they end at 2, the others at 3) | The approval is one per trait. Revisit with `docs/tools/qa/trait_coverage.py` after the observer run. |
| fickle in Partial Removal / Downgrade (the gaps doc's suggestion) | Removal decisions are changed by the providers spec in progress (§1). Once that lands, a fickle "change of heart" cancel option on the new "Who Takes It Out?" event is the natural follow-up. |
| impatient in Pursue the Next Stage (the gaps doc's suggestion) | Same reason. tier1.007 took it instead. |
| The gaps doc's other homes (A Lover's Touch, Dulled Palate, The Feast You Didn't Eat, Tremor) | **Already used.** tier1.009 holds lustful.d / chaste.e, tier1.008 and tier3.011 hold gluttonous.d / temperate.e, and tier3.008 holds impatient.e. The second and third options went to the next-best events instead. |
| tier3.006 The Delegation [arbitrary] | A good fit, but tier3.021 had no gated option at all and needed one more. Keep for a later pass. |
| A real lover or fertility effect on tier3.003.f (`had_sex_with_effect`) | It needs a partner picker and pregnancy handling: a new beat in all but name. Event expansion is the human's call. |
| Universal options that move no risk (e.g. tier1.005.b, tier1.007.a/.d, tier3.003.a, tier2.020.a) | They are legal under index rule 4, which applies per event. This spec's "every option moves risk" applies to its own eight options only. Noted for the next conformance pass; not changed here. |
| Updating `docs/specs/cybernetics_v2_phase0.md` §2.4 with the four helper rows | It is a doc edit outside this file. The architect does it on the coordinator's word, after the scripter lands §5.2, so the table never disagrees with the tree. |

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Add the 8 trait-gated options of §5.1 to their existing host events and the 4 helper rows of §5.2, without touching on_actions, event triggers or any event excluded in §1, then run the three validators.
- files: docs/specs/cybernetics_v2_trait_depth.md
- needs-loc: eotg_aug_tier1.005.f, eotg_aug_tier1.007.f, eotg_aug_tier2.004.e, eotg_aug_tier2.020.f, eotg_aug_tier3.003.f, eotg_aug_tier3.010.f, eotg_aug_tier3.021.d, eotg_aug_nr.004.f (proposed text in §7)
- needs-lore: none (routine pass on the 8 lines against index §5)
- needs-human: §9 item 10 in-game checks on the temporary map; tell the providers-spec author that reject/neglect helper rows change (§5.2 blast radius)
