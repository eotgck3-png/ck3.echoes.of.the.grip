# Cybernetics — Test Plan, Requirements and Art

**Date:** 2026-10-03.

**State:**
- Cybernetics v2 Phases 0–6 are built.
- Static QA passed on every phase: Tiger, the PX language server, the PX vocab check and the PX event graph.
- Every line of text passed lore review.
- **Nothing has been played yet.**

**Specs:** [cybernetics_track.md](../specs/cybernetics_track.md), [cybernetics_v2.md](../specs/cybernetics_v2.md) and its phase files.

**Contents:** 1 Requirements · 2 Console toolkit · 3 In-game test list · 4 Every event · 5 Art · 6 Open decisions

---

## 1. Requirements

### 1a. To run at all

| Requirement | Status | Why it matters |
|---|---|---|
| A mod descriptor (`descriptor.mod` + `echoes_of_the_grip.mod`) | **Missing** (Gate 0) | The launcher cannot load the mod without one. Every static check so far used a scratch descriptor. |
| The temporary map | Pending (yours) | The system is map-agnostic, but it needs the characters and conditions in §1c to exist. |
| Game version | 1.20.0.3 installed | Tiger 1.17 targets 1.18.3. It reports `has_personal_tenet_flag` / `change_spiritual_fulfillment` errors inside vanilla `20_health_effects.txt`; these are version noise. |
| Art | 1 icon missing (see §5) | The trait shows a blank icon. Nothing breaks. |

### 1b. How a character moves through the system

**Who it runs for.** Rulers of **county tier and up**. Their checks run through vanilla `yearly_playable_pulse`, once a year on each ruler's own date. Knights and courtiers have a slower lifecycle of their own (see Non-rulers below), and events about them go to their liege.

**Getting in (Initiation).** A character can be offered augmentation when all of these hold:
- they are an adult;
- they are not already augmented;
- no suppression flag is set on them;
- their **capital county has development 10 or higher**.

Once a year, one weighted roll picks at most one offer from the ones that fit:
- **Injury and disability:** a wound (with peace and war versions), a lost limb or eye, or being infirm or incapable. These lead to The Prosthetic and The Neural Bridge.
- **Wealth:** a syndicate offer. Ambitious or greedy characters who are short of gold can get the Patron instead.
- **Other circumstances:** being 50+ with low prowess, an augmented peer at court, a court physician, a cynical and learned outlook, or a duel loss.
- **Family:** an augmented parent's death (A Parent's Hardware), or a sick child (The Sickly Child, which runs on its own 5-year clock).
- **Two augmented knights at court** (The Arms Race).

Declining The Prosthetic or The Neural Bridge makes that offer much rarer for 10 years.

**Or skip the wait** with the **Seek Augmentation** decision: any eligible adult, a tiny gold cost, a 3-year cooldown. It offers four routes: a sanctioned clinic, the back streets, your own physician, or a syndicate.

**The tiers.** One trait, "Cybernetic Augmentation", with an Integration track:

| Tier | Integration | How you get there | Feel |
|---|---|---|---|
| Augmented | 0 | any install | useful, seductive |
| Enhanced | 50 | The First Upgrade chain (tier1.002 → .021 → .022); costs `medium_gold_value` | becoming part of you |
| Overclocked | 100 | The Next Stage (tier2.003); costs `major_gold_value`, or test it on a prisoner | something is wrong |
| Neurofractured | separate trait | the Neural Cascade (see the hidden number below) | you don't control this |
| Seamless | separate trait | an endgame (see Endgames) | nothing left to argue |

Integration only ever sits at 0, 50 or 100. It changes only at these steps or through the regression decisions.

**The hidden number (fracture risk).** It is never shown, and it only matters from Overclocked onwards.
- **How it rises:** each year at Overclocked it goes up by **12, plus 8 per stress level, plus 12 if paranoid, plus 10 at war**.
- **What happens at 80:** the **Neural Cascade** fires and the character becomes Neurofractured. A calm ruler lasts about 7 years at Overclocked; a highly stressed one about 3.
- **How the player learns about it:** only through event choices and the story. **The Countdown** story starts at 50 (40 with a hidden implant flaw) and escalates: minor anomalies, then lost time, then contradictory memories, then violence, then intervention.
- **Ways to slow or stop it:**
  - Maintenance Protocol (calibration; it also removes black-market implants).
  - Consult a Physician.
  - The Downgrade decision, which steps down to Enhanced and halves the risk.
  - Partial Removal (Enhanced to Augmented).
  - Remove Implants (Augmented to none).

**Neurofractured: pressure bands.** After the cascade, the same hidden number becomes "pressure".
- **How it moves:** +8 a year, plus 4 more per stress level. Sedation lowers it by 6 a year, Restraints by 4.
- **Which events it brings:**
  - **Flicker (under 30):** small and eerie. Wrong names, lost hours, the mirror, the door.
  - **Fracture (30–59):** violence and lost time. Blood on the sleeve, the false traitor, the missing courtier.
  - **Storm (60+):** the realm reacts. The Warrant (a real liberty or independence faction), Containment Regency (a vanilla regency), the Massacre.
  - **95+:** The Cascade, where the implant decides: death, Seamless, a free excision, abdication, or it passes.
- **The Heir's Arc** runs once per ruler. The heir watches, fears, confronts, then allies, usurps or tries to kill.

**Endgames.**
- **Excision:** surgery, reached through a decision or events. It can kill. Survivors lose everything cybernetic and may be left maimed.
- **Seamless (Total Integration):** reached through Hand Over the Controls, which needs Storm pressure plus either a late voice stage or permission from an event. It wipes personality traits and relationships, stops the episodes, and the court leaves.
- **Death in a neural cascade:** one possible result of The Cascade.
- **Abdication or restraints:** needs a primary heir. The old ruler lives on, confined.

**Decisions at a glance.**

| Decision | Shown when | Cost / cooldown |
|---|---|---|
| Seek Augmentation | adult, not augmented (valid when eligible and holding tiny gold) | 3 years |
| Maintenance Protocol | has the trait | `minor_gold_value` (×0.75 with a physician) |
| Consult a Physician | has the trait + physician access | `minor_gold_value` (×0.5 if you are a physician), 3 years |
| Augment a Courtier | has the trait + a willing knight or courtier | 2 years |
| Remove Implants | Augmented | `medium_gold_value` |
| Partial Removal | Enhanced | `medium_gold_value` (−25% at stress level 2+ or after an Intervention) |
| Downgrade Protocol | Overclocked | `major_gold_value` (same discount); halves risk |
| Accept Restraints / Begin a Sedation Regimen | Neurofractured | minor / medium gold |
| Appoint a Warden | Neurofractured, no diarchy, eligible for vanilla diarchy | 5 years |
| Hand Over the Controls | Neurofractured, Storm pressure, voice stage 3+ or permission | — |
| Cut It Out (Excision) | Overclocked or Neurofractured, and can afford it (not Enhanced: owner ruling 2026-10-05, one removal step per stage) | 5 years |

**Story cycles.** The player never sees these directly; they pace events in the background.
- **The Countdown** (Overclocked).
- **The Patron:** a syndicate pays for your implant, then calls in favours for years. The debt survives removing the implants.
- **The Iron Retinue:** augmenting knights becomes a program.
- **The Heir's Arc** (Neurofractured).

**Non-rulers.** Augmented knights and courtiers:
- progress slowly: 4% a year, 8% for Iron Retinue knights;
- build up risk at Overclocked, and can cascade on their own;
- generate at most one event a year for their liege. The events are The Champion Volunteers, New Edge, Something Is Wrong, The Champion's Mistake, The Familiar Change and The Broken Champion.

### 1c. What the temporary map needs for a full test

- **Count-tier or higher rulers whose capital county is at development 10+.** Without that development, nobody is ever offered augmentation (`eotg_can_receive_augmented`). **This is the requirement that can silently block everything.**
- **Courtiers and knights.** These drive the Arms Race, the Retinue, the non-ruler events, and supply victims and witnesses.
- **A court physician** for the physician paths.
- **Vassals** for the Warrant and the opinion events.
- **A spouse, children and a primary heir** for the Heir's Arc, Absent at the Birth, abdication and The Sickly Child.
- **A war** for Desperation Protocol and the Clarity Campaign.
- **A prisoner** for "Test it on a prisoner".
- **A government that allows vanilla diarchy**, for Appoint a Warden and Containment Regency.
- **Characters with varied personality traits.** About 40 options appear only for a specific trait.

---

## 2. Console toolkit

Select the character first, then use:
- **Fire an event:** `event <id>`. The "Console" column in §4 says which events can be fired directly.
- **Augment:** `effect eotg_aug_initiate_effect = yes`, or `add_trait eotg_cybernetics`.
- **Change tier:** `effect add_trait_xp = { trait = eotg_cybernetics value = 50 }`.
- **Set the hidden risk or pressure:** `effect set_variable = { name = eotg_fracture_risk value = 55 }`.
- **Add stress:** `add_stress 250`.

Then let the game run. The yearly checks fire on each ruler's own date.

---

## 3. In-game test list

These come from the QA passes and are in build order. Tick them off as you go.

**Core (Phase 0)**
1. An Overclocked count at stress 0 does not cascade before the 7th yearly check. After `add_stress 250`, the cascade comes within 3 checks.
2. A Neurofractured count who makes no choices reaches the 30+ band in about 3–4 years.
3. Downgrade Protocol can be taken at stress 0. Its tooltip shows scaled gold and no risk number.

**Trait options (Phase 1)**
4. A brave, a craven and a cynical ruler each see different options on init.001 and init.004.
5. Violent Impulse (tier3.001) names its victim. With an empty court it shows the "no one was near" text and no portrait error.

**Entry (Phase 2)**
6. A `maimed` count is offered The Prosthetic, and accepting removes `maimed`.
7. Seek Augmentation appears for an unaugmented count, and every one of its paths installs.
8. Killing an augmented parent gives the heir A Parent's Hardware within about 2 years.

**Neurofractured (Phase 3)**
9. Set risk to 10, 45 and 70 on a Neurofractured count. The event pool shifts each time.
10. A Warrant creates a liberty faction or adds discontent.
11. **Containment Regency lasts a full year.** If the engine ends it early, tell me; a fallback is ready (Q7).
12. Scrambled visibly swaps a personality trait.
13. Risk 96 fires The Cascade.
14. Excision can kill, and it can also free the character.
15. Seamless strips personality and stops the episodes, and the court thins out.
16. A finished Heir's Arc never restarts for the same ruler.

**Tiers (Phase 4)**
17. The First Upgrade asks what to change (tier1.021) and installs Enhanced at stage 3 (tier1.022).
18. A child born to an Enhanced parent fires Absent at the Birth within 3 days.
19. First Contact fires only once per character.
20. The Plot's reveal (tier3.018) arrives 4–8 months after the accusation.
21. tier3.014.b's result appears as a toast after the click, not on hover.

**Story arcs (Phase 5)**
22. An Overclocked count at risk 55 gets Minor Anomalies within about 5 months.
23. Raise that count to 76. Violence arrives next (skipping stages) and names its victim.
24. Downgrade with the halved risk under 50. The Quiet fires **once** and the Countdown stops.
25. Accept a patron:
    - the envoy arrives with your culture and faith;
    - Repayment comes in 2–3 years (3–4 if you read every clause);
    - three refusals bring the Final Demand early.
26. Remove Implants during a Patron debt. The debt continues, the clause stays, and only the non-hardware options show.
27. Augment two knights through Augment a Courtier. The Retinue starts, and More Step Forward follows within 1–2 years.

**Non-rulers (Phase 6)**
28. A count with an augmented knight sees that knight progress within 10–20 years, or right away with `add_trait_xp` on the knight.
29. An Overclocked knight at risk 85 produces The Broken Champion within a year, and no other non-ruler event that year.
30. Each liege gets at most one non-ruler event a year.
31. An imprisoned champion never gets The Champion's Mistake, and the Arms Race never fires while a Retinue runs.
32. Augmenting a single knight starts the Retinue at phase 1. "First of the Iron" arrives within 1–2 years and names the volunteer.
33. When a knight progresses, "Your Champion's New Edge" fires that year with the matching Enhanced or Overclocked line.

**Throughout:**
- No tooltip ever shows a fracture-risk number.
- error.log has no unset-scope or portrait errors from `eotg_` events.

---

## 4. Every event (152)

- **Fired by:** what triggers the event in play.
- **Console:** where the event can be fired directly on a selected character, this gives the command.
- **Via parent:** the event reads scopes handed over by an earlier event. Fire the event listed under "Fired by" instead.

### Initiation

| Event | Title | Fired by | Console |
|---|---|---|---|
| `eotg_aug_init.001` | The Cost of Survival | yearly initiation | `event eotg_aug_init.001` |
| `eotg_aug_init.002` | A Corporate Offer | yearly initiation | `event eotg_aug_init.002` |
| `eotg_aug_init.003` | Aging Hands | yearly initiation | `event eotg_aug_init.003` |
| `eotg_aug_init.004` | Desperation Protocol | yearly initiation | `event eotg_aug_init.004` |
| `eotg_aug_init.005` | A Familiar Change | yearly initiation | `event eotg_aug_init.005` |
| `eotg_aug_init.006` | The Prosthetic | yearly initiation | `event eotg_aug_init.006` |
| `eotg_aug_init.007` | The Neural Bridge | yearly initiation | `event eotg_aug_init.007` |
| `eotg_aug_init.008` | The Bridge Settles | event eotg_aug_init.007 | `event eotg_aug_init.008` |
| `eotg_aug_init.009` | The Cynic's Argument | yearly initiation | `event eotg_aug_init.009` |
| `eotg_aug_init.010` | Back-Alley Surgery | yearly initiation | `event eotg_aug_init.010` |
| `eotg_aug_init.011` | The Scar Itches | event eotg_aug_init.010, event eotg_aug_init.018 | `event eotg_aug_init.011` |
| `eotg_aug_init.012` | The Body Decides | event eotg_aug_init.011 | `event eotg_aug_init.012` |
| `eotg_aug_init.013` | A Parent's Hardware | yearly initiation | `event eotg_aug_init.013` |
| `eotg_aug_init.014` | The Sickly Child | yearly initiation | `event eotg_aug_init.014` |
| `eotg_aug_init.015` | The Child Who Hums | event eotg_aug_init.014 | via parent (needs `eotg_sick_child`) |
| `eotg_aug_init.016` | The Duel Shame | yearly initiation | via parent (needs `duel_value`) |
| `eotg_aug_init.017` | The Physician's Proposal | yearly initiation | `event eotg_aug_init.017` |
| `eotg_aug_init.018` | The Offer You Sought | decision: seek_augmentation | `event eotg_aug_init.018` |
| `eotg_aug_init.019` | The Arms Race | yearly initiation | `event eotg_aug_init.019` |
| `eotg_aug_init.020` | Choosing the Volunteer | decision: augment_retainer | `event eotg_aug_init.020` |

### Augmented

| Event | Title | Fired by | Console |
|---|---|---|---|
| `eotg_aug_tier1.001` | Phantom Sensation | yearly tier1 | `event eotg_aug_tier1.001` |
| `eotg_aug_tier1.002` | The Upgrade | yearly tier1 | `event eotg_aug_tier1.002` |
| `eotg_aug_tier1.003` | An Uncomfortable Question | yearly tier1 | `event eotg_aug_tier1.003` |
| `eotg_aug_tier1.004` | The Knight's Request | yearly tier1 | `event eotg_aug_tier1.004` |
| `eotg_aug_tier1.005` | Weight of Silence | yearly tier1 | `event eotg_aug_tier1.005` |
| `eotg_aug_tier1.006` | The Faster Hand | yearly tier1 | `event eotg_aug_tier1.006` |
| `eotg_aug_tier1.007` | Firmware Itch | yearly tier1 | `event eotg_aug_tier1.007` |
| `eotg_aug_tier1.008` | Dulled Palate | yearly tier1 | `event eotg_aug_tier1.008` |
| `eotg_aug_tier1.009` | A Lover's Touch | yearly tier1 | `event eotg_aug_tier1.009` |
| `eotg_aug_tier1.010` | The Training Yard | yearly tier1 | via parent (needs `duel_value`) |
| `eotg_aug_tier1.011` | The Stare | yearly tier1 | `event eotg_aug_tier1.011` |
| `eotg_aug_tier1.012` | A Tithe for Purity | yearly tier1 | `event eotg_aug_tier1.012` |
| `eotg_aug_tier1.013` | Rejection: Fever | yearly tier1 | `event eotg_aug_tier1.013` |
| `eotg_aug_tier1.014` | Rejection: Crisis | event eotg_aug_tier1.013 | `event eotg_aug_tier1.014` |
| `eotg_aug_tier1.015` | Rejection: Outcome | event eotg_aug_tier1.014 | `event eotg_aug_tier1.015` |
| `eotg_aug_tier1.016` | The Challenge | yearly tier1 | via parent (needs `duel_value`) |
| `eotg_aug_tier1.017` | The Bout | event eotg_aug_tier1.016 | via parent (needs `duel_value`, `eotg_challenger`) |
| `eotg_aug_tier1.018` | Copycat | yearly tier1 | `event eotg_aug_tier1.018` |
| `eotg_aug_tier1.019` | Copycat: Their Fate | event eotg_aug_tier1.018 | via parent (needs `eotg_copycat`) |
| `eotg_aug_tier1.020` | Something Is Missing | yearly tier1 | `event eotg_aug_tier1.020` |
| `eotg_aug_tier1.021` | What Will You Change? | event eotg_aug_tier1.002 | `event eotg_aug_tier1.021` |
| `eotg_aug_tier1.022` | Installation | event eotg_aug_tier1.021 | `event eotg_aug_tier1.022` |

### Enhanced

| Event | Title | Fired by | Console |
|---|---|---|---|
| `eotg_aug_tier2.001` | Emotional Delay | yearly tier2 | `event eotg_aug_tier2.001` |
| `eotg_aug_tier2.002` | Children Fear Me | yearly tier2 | `event eotg_aug_tier2.002` |
| `eotg_aug_tier2.003` | The Next Stage | yearly tier2 | `event eotg_aug_tier2.003` |
| `eotg_aug_tier2.004` | The Space Between Us | yearly tier2 | `event eotg_aug_tier2.004` |
| `eotg_aug_tier2.005` | The Spiritual Advisor's Warning | yearly tier2 | via parent (needs `duel_value`) |
| `eotg_aug_tier2.006` | Cold Detachment | yearly tier2 | `event eotg_aug_tier2.006` |
| `eotg_aug_tier2.007` | Numbers, Not Faces | yearly tier2 | `event eotg_aug_tier2.007` |
| `eotg_aug_tier2.008` | The Late Grief | yearly tier2 | `event eotg_aug_tier2.008` |
| `eotg_aug_tier2.009` | Perfect Recall | yearly tier2 | `event eotg_aug_tier2.009` |
| `eotg_aug_tier2.010` | Absent at the Birth | hook: birth_aug_parent | via parent (needs `eotg_newborn`) |
| `eotg_aug_tier2.011` | Market Ledger | yearly tier2 | `event eotg_aug_tier2.011` |
| `eotg_aug_tier2.012` | Trust Protocol | yearly tier2 | `event eotg_aug_tier2.012` |
| `eotg_aug_tier2.013` | The Bidding War | yearly tier2 | `event eotg_aug_tier2.013` |
| `eotg_aug_tier2.014` | The Vendors Return | event eotg_aug_tier2.013 | via parent (needs `eotg_vendor_return`) |
| `eotg_aug_tier2.015` | Tampering | yearly tier2 | via parent (needs `duel_value`) |
| `eotg_aug_tier2.016` | What Was Done | event eotg_aug_tier2.015 | via parent (needs `eotg_tamper_trace`, `eotg_tamperer`) |
| `eotg_aug_tier2.017` | Confrontation | event eotg_aug_tier2.004 | via parent (needs `aug_spouse`) |
| `eotg_aug_tier2.018` | Resolution | event eotg_aug_tier2.017 | via parent (needs `aug_spouse`) |
| `eotg_aug_tier2.019` | The Cold Calculation | yearly tier2 | `event eotg_aug_tier2.019` |
| `eotg_aug_tier2.020` | The Second Self | yearly tier2 | `event eotg_aug_tier2.020` |
| `eotg_aug_tier2.021` | The Report Was Wrong | event eotg_aug_tier2.012 | via parent (needs `eotg_flagged`) |

### Overclocked

| Event | Title | Fired by | Console |
|---|---|---|---|
| `eotg_aug_tier3.001` | Violent Impulse | yearly overclocked | via parent (needs `eotg_victim`) |
| `eotg_aug_tier3.002` | The Mirror | yearly overclocked | `event eotg_aug_tier3.002` |
| `eotg_aug_tier3.003` | Sleepless | yearly overclocked | `event eotg_aug_tier3.003` |
| `eotg_aug_tier3.004` | Signal Noise | yearly overclocked | via parent (needs `eotg_suspect`) |
| `eotg_aug_tier3.005` | Clarity | yearly overclocked | `event eotg_aug_tier3.005` |
| `eotg_aug_tier3.006` | The Delegation | yearly overclocked | `event eotg_aug_tier3.006` |
| `eotg_aug_tier3.007` | Two Machines | yearly overclocked | `event eotg_aug_tier3.007` |
| `eotg_aug_tier3.008` | Tremor | yearly overclocked | `event eotg_aug_tier3.008` |
| `eotg_aug_tier3.009` | Phantom Orders | yearly overclocked | `event eotg_aug_tier3.009` |
| `eotg_aug_tier3.010` | Heat Spike | yearly overclocked | `event eotg_aug_tier3.010` |
| `eotg_aug_tier3.011` | The Feast You Didn't Eat | yearly overclocked | `event eotg_aug_tier3.011` |
| `eotg_aug_tier3.012` | First Contact | yearly overclocked | `event eotg_aug_tier3.012` |
| `eotg_aug_tier3.013` | Sleepwalker | yearly overclocked | `event eotg_aug_tier3.013` |
| `eotg_aug_tier3.014` | The Missing Conversation | yearly overclocked | `event eotg_aug_tier3.014` |
| `eotg_aug_tier3.015` | Two Machines: The Next Meeting | event eotg_aug_tier3.007 | via parent (needs `duel_value`, `eotg_machines_bond`, `other_machine`) |
| `eotg_aug_tier3.016` | The Bleed | yearly overclocked | `event eotg_aug_tier3.016` |
| `eotg_aug_tier3.017` | The Plot | yearly overclocked | via parent (needs `eotg_second_suspect`) |
| `eotg_aug_tier3.018` | The Plot: The Truth | event eotg_aug_tier3.017 | via parent (needs `eotg_conspirator`, `eotg_plot_action`, `eotg_plot_learned`) |
| `eotg_aug_tier3.019` | The Delegation, Revisited | yearly overclocked | `event eotg_aug_tier3.019` |
| `eotg_aug_tier3.020` | The Intervention | event eotg_aug_countdown.005, yearly overclocked, story: countdown | `event eotg_aug_tier3.020` |
| `eotg_aug_tier3.021` | The Other Order | event eotg_aug_tier3.019 | via parent (needs `eotg_delegate`) |
| `eotg_aug_tier3.022` | The Bleed: Outcome | event eotg_aug_tier3.016 | `event eotg_aug_tier3.022` |
| `eotg_aug_tier3.023` | The Clarity Campaign | yearly overclocked | `event eotg_aug_tier3.023` |
| `eotg_aug_tier3.024` | The Engagement | event eotg_aug_tier3.023 | `event eotg_aug_tier3.024` |

### Countdown (story)

| Event | Title | Fired by | Console |
|---|---|---|---|
| `eotg_aug_countdown.001` | Minor Anomalies | story: countdown | `event eotg_aug_countdown.001` |
| `eotg_aug_countdown.002` | Lost Time | story: countdown | via parent (needs `eotg_suspect`) |
| `eotg_aug_countdown.003` | Contradictory Memories | story: countdown | `event eotg_aug_countdown.003` |
| `eotg_aug_countdown.004` | Violence | story: countdown | via parent (needs `eotg_victim`) |
| `eotg_aug_countdown.005` | No One Asks Any More | story: countdown | `event eotg_aug_countdown.005` |
| `eotg_aug_countdown.006` | The Quiet | decision: overclock_regression, story: countdown | `event eotg_aug_countdown.006` |

### Neurofractured

| Event | Title | Fired by | Console |
|---|---|---|---|
| `eotg_fracture.0001` | Neural Cascade | effect: trigger_neurofracture | via parent (needs `eotg_victim`) |
| `eotg_fracture.002` | Containment Failure | yearly neurofractured | via parent (needs `eotg_victim`, `eotg_victim_dead`, `eotg_victim_extra`) |
| `eotg_fracture.003` | Lucid Moment | yearly neurofractured | `event eotg_fracture.003` |
| `eotg_fracture.004` | The Court Massacre | yearly neurofractured | via parent (needs `eotg_victim`, `eotg_victim_dead`) |
| `eotg_fracture.005` | What the Heir Saw | story: heir_arc | `event eotg_fracture.005` |
| `eotg_fracture.006` | The Warrant | yearly neurofractured | via parent (needs `duel_value`, `eotg_warrant_result`) |
| `eotg_fracture.007` | Dead Reckoning | yearly neurofractured | `event eotg_fracture.007` |
| `eotg_fracture.008` | Wrong Name | yearly neurofractured | `event eotg_fracture.008` |
| `eotg_fracture.009` | Lost Hour | yearly neurofractured | via parent (needs `eotg_victim`) |
| `eotg_fracture.010` | The Mirror Doesn't Blink | yearly neurofractured | `event eotg_fracture.010` |
| `eotg_fracture.011` | Conversations With No One | yearly neurofractured | via parent (needs `eotg_witness`) |
| `eotg_fracture.012` | The Familiar Stranger | yearly neurofractured | `event eotg_fracture.012` |
| `eotg_fracture.013` | Memory of Tomorrow | yearly neurofractured | `event eotg_fracture.013` |
| `eotg_fracture.014` | The Door | yearly neurofractured | `event eotg_fracture.014` |
| `eotg_fracture.015` | The Unsent Letter | yearly neurofractured | `event eotg_fracture.015` |
| `eotg_fracture.016` | Blood on the Sleeve | yearly neurofractured | via parent (needs `eotg_victim`) |
| `eotg_fracture.017` | Terms of Access | yearly neurofractured | via parent (needs `duel_value`) |
| `eotg_fracture.018` | Scrambled | yearly neurofractured | `event eotg_fracture.018` |
| `eotg_fracture.019` | The Flagged Name | yearly neurofractured | `event eotg_fracture.019` |
| `eotg_fracture.020` | What the Record Shows | event eotg_fracture.019 | via parent (needs `eotg_accused`) |
| `eotg_fracture.021` | The Missing Courtier | yearly neurofractured | via parent (needs `eotg_missing`) |
| `eotg_fracture.022` | We | yearly neurofractured | `event eotg_fracture.022` |
| `eotg_fracture.023` | The Wrong War | yearly neurofractured | `event eotg_fracture.023` |
| `eotg_fracture.024` | The Familiar Change | yearly neurofractured | `event eotg_fracture.024` |
| `eotg_fracture.025` | Containment Regency | yearly neurofractured | `event eotg_fracture.025` |
| `eotg_fracture.026` | The Last Lucid Moment | yearly neurofractured | `event eotg_fracture.026` |
| `eotg_fracture.027` | The Cascade | yearly neurofractured | `event eotg_fracture.027` |
| `eotg_fracture.028` | The Terms | event eotg_fracture.017 | `event eotg_fracture.028` |
| `eotg_fracture.029` | It Passes | event eotg_fracture.027 | via parent (needs `eotg_victim`, `eotg_victim_2`) |

### Heir's Arc (story)

| Event | Title | Fired by | Console |
|---|---|---|---|
| `eotg_aug_heir.001` | Concern | story: heir_arc | `event eotg_aug_heir.001` |
| `eotg_aug_heir.003` | The Heir's Warning | story: heir_arc | `event eotg_aug_heir.003` |
| `eotg_aug_heir.004` | The Heir's Choice | story: heir_arc | `event eotg_aug_heir.004` |
| `eotg_aug_heir.005` | What Must Be Done | event eotg_aug_heir.004 | via parent (needs `eotg_parent_ruler`) |

### Endgames

| Event | Title | Fired by | Console |
|---|---|---|---|
| `eotg_aug_end.001` | The Surgeons | decision: aug_excision, event eotg_aug_end.031, event eotg_fracture.007 … | `event eotg_aug_end.001` |
| `eotg_aug_end.002` | Silence | effect: aug_excision_surgery_effect | via parent (needs `eotg_excision_outcome`) |
| `eotg_aug_end.009` | Hand Over the Controls | decision: aug_embrace_cascade | `event eotg_aug_end.009` |
| `eotg_aug_end.010` | There Is No Static | effect: aug_total_integration_effect | `event eotg_aug_end.010` |
| `eotg_aug_end.011` | The Empty Hall | event eotg_aug_end.010 | `event eotg_aug_end.011` |
| `eotg_aug_end.020` | Appoint a Warden | decision: aug_appoint_warden | `event eotg_aug_end.020` |
| `eotg_aug_end.030` | Into Restraints | event eotg_aug_end.020, event eotg_fracture.027 | `event eotg_aug_end.030` |
| `eotg_aug_end.031` | The Locked Wing | effect: aug_abdicate_effect | via parent (needs `eotg_old_ruler`) |

### Patron (story)

| Event | Title | Fired by | Console |
|---|---|---|---|
| `eotg_aug_patron.001` | The Syndicate's Offer | event eotg_aug_init.018, yearly initiation | `event eotg_aug_patron.001` |
| `eotg_aug_patron.002` | Repayment | story: patron | via parent (needs `duel_value`) |
| `eotg_aug_patron.003` | Exclusivity | story: patron | `event eotg_aug_patron.003` |
| `eotg_aug_patron.004` | The Errand | story: patron | `event eotg_aug_patron.004` |
| `eotg_aug_patron.005` | The Family Clause | story: patron | `event eotg_aug_patron.005` |
| `eotg_aug_patron.006` | The Final Demand | story: patron | `event eotg_aug_patron.006` |
| `eotg_aug_patron.007` | A New Envoy | story: patron | `event eotg_aug_patron.007` |

### Iron Retinue (story)

| Event | Title | Fired by | Console |
|---|---|---|---|
| `eotg_aug_retinue.001` | First of the Iron | story: retinue | `event eotg_aug_retinue.001` |
| `eotg_aug_retinue.002` | More Step Forward | story: retinue | `event eotg_aug_retinue.002` |
| `eotg_aug_retinue.003` | The Iron Ranks | story: retinue | `event eotg_aug_retinue.003` |
| `eotg_aug_retinue.004` | Resentment in the Ranks | story: retinue | `event eotg_aug_retinue.004` |
| `eotg_aug_retinue.005` | What the Program Becomes | story: retinue | `event eotg_aug_retinue.005` |

### Non-ruler lifecycle

| Event | Title | Fired by | Console |
|---|---|---|---|
| `eotg_aug_nr.001` | The Champion Volunteers | yearly nonruler | via parent (needs `eotg_champion`) |
| `eotg_aug_nr.002` | Your Champion's New Edge | yearly nonruler | via parent (needs `eotg_champion`) |
| `eotg_aug_nr.003` | Something Is Wrong | yearly nonruler | via parent (needs `eotg_champion`) |
| `eotg_aug_nr.004` | The Champion's Mistake | yearly nonruler | via parent (needs `eotg_champion`, `eotg_victim`) |
| `eotg_aug_nr.005` | The Familiar Change | yearly nonruler | via parent (needs `eotg_champion`) |
| `eotg_aug_nr.006` | The Broken Champion | effect: aug_nr_cascade_effect | via parent (needs `eotg_champion`) |

---

## 5. Art

**Missing, and no placeholder possible:**

| File | For | Size / format |
|---|---|---|
| `gfx/interface/icons/traits/eotg_total_integration.dds` | the **Seamless** trait (the Total Integration endgame) | 120 × 120, uncompressed 32-bit with alpha, no mipmaps (same as the other two trait icons) |

No vanilla trait icon is used as a stand-in, because it would make Seamless look like an existing vanilla trait.

**Using vanilla art as a placeholder.** These work now; replace them when you have art. All decision illustrations are 1100 × 440, DXT1, no mipmaps, in `gfx/interface/illustrations/decisions/`.

| Decision | Placeholder | Suggested subject for the real art |
|---|---|---|
| Seek Augmentation | vanilla `decision_smith.dds` | a clinic consultation, hardware laid out on a cloth |
| Remove Implants | mod `eotg_decision_partial_removal.dds` | hardware lifted out, the empty sockets |
| Consult a Physician | vanilla `decision_physician.dds` | a physician reading an implant's diagnostics |
| Augment a Courtier | vanilla `decision_knight_kneeling.dds` | a knight on the table, the ruler watching |
| Accept Restraints | vanilla `decision_prison.dds` | a locked residence wing, a guard at the door |
| Begin a Sedation Regimen | vanilla `decision_physician.dds` | a dosing schedule in a dimmed room |
| Appoint a Warden | vanilla `decision_realm.dds` | the ruler handing over a seal or access key |
| Hand Over the Controls | vanilla `decision_misc.dds` | a figure and a console, the line between them gone |
| Cut It Out (Excision) | vanilla `decision_physician.dds` | the excision table, surgeons in masks |

Each placeholder is marked `PLACEHOLDER` in a comment in `common/decisions/eotg_augmentation_decisions.txt`.

**Already custom** (delivered 2026-10-03):
- **Trait icons:** Cybernetic Augmentation and Neurofractured.
- **Decision illustrations:** Partial Removal, Downgrade Protocol and Maintenance Protocol.
- **Modifier icons:** the implant bonuses (mind and body), Calibrated Systems and Regression Recovery.

Event backgrounds all use vanilla event themes. They suit the content and don't need replacing.

---

## 6. Open decisions for you (none of them block testing)

1. **Helix at 866 AG:** active, or a remnant? Canon contradicts itself. The syndicate stays unnamed until you decide. The lore-keeper drafted errata text for both answers.
2. **The cybernetic "voice" errata:** approve adding it to SETTING LORE's ERRATA block. It records that the voice is technological and never the Void.
3. **Industrial Survivalism vs zealous characters:** zealous characters currently dislike implants, which inverts that faith. This is accepted as a known gap until the faiths exist in v2; a fix based on faith doctrine is deferred.
4. **Q7, Containment Regency:** confirm in game (test 11).
