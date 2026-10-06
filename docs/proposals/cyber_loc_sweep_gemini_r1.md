# Shipped Cybernetics: Time-of-Day and Stock Phrase Sweep Proposals (W5)

Proposals only; no `.yml` or `.txt` files edited.
Swept `localization/english/eotg_augmentation_l_english.yml` for:
- Time-of-day words (`dawn`, `morning`, `today`, `tonight`, `night`, `overnight`, `sunrise`, `evening`)
- 'half a second' beyond the four kept on purpose (`tier2.020.desc`, `tier3.012.desc_first`, `fracture.022.desc_first`, `fracture.027.desc_voice01`)
- Medieval and clockwork vocabulary from feedback §3 (`brass`, `gears`, `cogs`, `candle`, `dungeon`, `castle`, etc.)

## Sweep Results Summary

- **Total target keys identified:** 14
- **'half a second' occurrences:** 4 total found in file; all 4 match the exact kept-on-purpose list in `docs/qa/variety_pass_2026-10-07.md`. Zero excess occurrences found.
- **Medieval / clockwork words:** 0 remaining occurrences found in shipped file.
- **Time-of-day words:** 14 occurrences identified across event descriptions, options, and tooltips.

## Proposed Replacements Table

| Key | Event Source | Issue | Current Text | Proposed Replacement |
|---|---|---|---|---|
| `eotg_aug_init.015.desc` | `events/eotg_augmentation_initiation.txt` | Time-of-day word: 'night' | `The fever broke. The child eats, sleeps, laughs. And at night, when the house is still, there is a thin electrical whine from the next room: coil noise, steady as a kettle. The physicians say the implant is settling. They say a great many things. You sit by the door with your hand on the frame.` | `The fever broke. The child eats, sleeps, laughs. And between watches, when the residence is still, there is a thin electrical whine from the next room: coil noise, steady as a kettle. The physicians say the implant is settling. They say a great many things. You sit by the door with your hand on the frame.` |
| `eotg_fracture.010.desc` | `events/eotg_augmentation_fracture.txt` | Time-of-day word: 'morning' | `Your implant's overlay renders what it expects the mirror to show. This morning your reflection's face updates a moment late, as if the display were catching up to you. It does not blink when you do.` | `Your implant's overlay renders what it expects the mirror to show. Before your audience your reflection's face updates a moment late, as if the display were catching up to you. It does not blink when you do.` |
| `eotg_fracture.026.desc_voice4` | `events/eotg_augmentation_endgame.txt` | Time-of-day word: 'morning' | `\n\nThe access you granted is idle, not revoked. You can read the queue of everything it would have done since morning, written out and unexecuted. It will resume on your word, and it will not need to ask twice.` | `\n\nThe access you granted is idle, not revoked. You can read the queue of everything it would have done across the last shift, written out and unexecuted. It will resume on your word, and it will not need to ask twice.` |
| `eotg_aug_end.001.b` | `events/eotg_augmentation_endgame.txt` | Banned word: 'today' | `Not today.` | `Not now; step away from the controls.` |
| `eotg_aug_end.011.desc_named` | `events/eotg_augmentation_endgame.txt` | Time-of-day word: 'night shift' | `The court roll is shorter. Departures: [ROOT.Char.MakeScope.Var('eotg_hall_gone').GetValue\|0]. The quiet in your [ROOT.Char.Custom('eotg_court_seat')] became unbearable, and people left by the early transports. [eotg_departed_courtier.GetFirstName] cleared out [eotg_departed_courtier.GetHerHis] quarters during the night shift without filing papers, leaving behind an empty locker and an unanswered comm channel.` | `The court roll is shorter. Departures: [ROOT.Char.MakeScope.Var('eotg_hall_gone').GetValue\|0]. The quiet in your [ROOT.Char.Custom('eotg_court_seat')] became unbearable, and people left by the early transports. [eotg_departed_courtier.GetFirstName] cleared out [eotg_departed_courtier.GetHerHis] quarters during the third watch without filing papers, leaving behind an empty locker and an unanswered comm channel.` |
| `eotg_aug_tier1.011.e` | `events/eotg_augmentation_tier1.txt` | Time-of-day word: 'evening's' | `Make it the evening's entertainment.` | `Make it the court's entertainment.` |
| `eotg_aug_tier3.013.desc` | `events/eotg_augmentation_tier3.txt` | Time-of-day word: 'dawn' | `[eotg_finder.GetFirstName] found you in the lower corridor before dawn, standing at a sealed door with one hand on the lock. Your eyes were open. You did not respond to your name for almost a minute, and you have no idea how you came to be there.` | `[eotg_finder.GetFirstName] found you in the lower corridor before the shift change, standing at a sealed door with one hand on the lock. Your eyes were open. You did not respond to your name for almost a minute, and you have no idea how you came to be there.` |
| `eotg_aug_countdown.001.desc` | `events/eotg_augmentation_countdown.txt` | Banned word: 'today' | `Clocks run wrong. A cup leaves your hand and you watch it fall. The implant's diagnostics report nothing out of range, and you notice that they have said so three times today.` | `Clocks run wrong. A cup leaves your hand and you watch it fall. The implant's diagnostics report nothing out of range, and you notice that they have logged that reassurance three times this shift.` |
| `eotg_aug_countdown.003.desc` | `events/eotg_augmentation_countdown.txt` | Time-of-day word: 'last night's' | `There are two versions of last night's dinner, and both are vivid. In one, the table was long and the talk was easy. In the other, you left early and nobody spoke to you. Both smell of the same smoke. Both arrived at the same instant, with the same confidence.` | `There are two versions of the communal dinner, and both are vivid. In one, the table was long and the talk was easy. In the other, you left early and nobody spoke to you. Both smell of the same smoke. Both arrived at the same instant, with the same confidence.` |
| `eotg_aug_nr.006.desc` | `events/eotg_augmentation_nonruler.txt` | Time-of-day word: 'in the night' | `The cascade has finished with [eotg_champion.GetFirstName]. The implants failed together in the night, and the one who stands in front of you is on [eotg_champion.GetHerHis] feet and strong and calm, and no longer reliably the person you knew. [eotg_champion.GetSheHe\|U] looks at you as if checking a record.` | `The cascade has finished with [eotg_champion.GetFirstName]. The implants failed together between shifts, and the one who stands in front of you is on [eotg_champion.GetHerHis] feet and strong and calm, and no longer reliably the person you knew. [eotg_champion.GetSheHe\|U] looks at you as if checking a record.` |
| `eotg_aug_tier2.004.b.success` | `events/eotg_augmentation_tier2.txt` | Banned word: 'tonight' | `[eotg_aug_spouse.GetSheHe\|U] wants to believe you, and for tonight [eotg_aug_spouse.GetSheHe] does.` | `[eotg_aug_spouse.GetSheHe\|U] wants to believe you, and for this watch [eotg_aug_spouse.GetSheHe] does.` |
| `eotg_aug_tamper_desc` | `localization/english/eotg_augmentation_l_english.yml` | Time-of-day word: 'one night' | `Agents need one night, an open maintenance hatch, and a target who does not wake.` | `Agents need an unmonitored watch, an open maintenance hatch, and a target who does not wake.` |
| `eotg_aug_tamper.002.desc` | `events/eotg_augmentation_tamper.txt` | Time-of-day word: 'For one night' | `The agents report before the next watch. For one night [target.GetName]'s implants were in the agents' hands, panel open, while [target.GetSheHe] slept under a dose.` | `The agents report before the next watch. Across an unmonitored shift [target.GetName]'s implants were in the agents' hands, panel open, while [target.GetSheHe] slept under a dose.` |
| `eotg_aug_tamper.002.desc_tier3` | `events/eotg_augmentation_tamper.txt` | Time-of-day word: 'that night' | `\n\nThe overclocked units are guarded, but not that night. The agents set them to run hotter than they should.` | `\n\nThe overclocked units are guarded, but not during that shift. The agents set them to run hotter than they should.` |

## Per-Key Lore and Event Context Rationale

### `eotg_aug_init.015.desc`
- **Event File:** `events/eotg_augmentation_initiation.txt`
- **Issue:** Time-of-day word: 'night'
- **Current Text:** "The fever broke. The child eats, sleeps, laughs. And at night, when the house is still, there is a thin electrical whine from the next room: coil noise, steady as a kettle. The physicians say the implant is settling. They say a great many things. You sit by the door with your hand on the frame."
- **Proposed Replacement:** "The fever broke. The child eats, sleeps, laughs. And between watches, when the residence is still, there is a thin electrical whine from the next room: coil noise, steady as a kettle. The physicians say the implant is settling. They say a great many things. You sit by the door with your hand on the frame."
- **Rationale:** Replaces 'at night' with 'between watches' and 'house' with 'residence', keeping the domestic unease true to space-station/bastion life without diurnal assumptions.

### `eotg_fracture.010.desc`
- **Event File:** `events/eotg_augmentation_fracture.txt`
- **Issue:** Time-of-day word: 'morning'
- **Current Text:** "Your implant's overlay renders what it expects the mirror to show. This morning your reflection's face updates a moment late, as if the display were catching up to you. It does not blink when you do."
- **Proposed Replacement:** "Your implant's overlay renders what it expects the mirror to show. Before your audience your reflection's face updates a moment late, as if the display were catching up to you. It does not blink when you do."
- **Rationale:** Replaces 'This morning' with 'Before your audience', grounding the scene in court routine rather than planetary morning.

### `eotg_fracture.026.desc_voice4`
- **Event File:** `events/eotg_augmentation_endgame.txt`
- **Issue:** Time-of-day word: 'morning'
- **Current Text:** "\n\nThe access you granted is idle, not revoked. You can read the queue of everything it would have done since morning, written out and unexecuted. It will resume on your word, and it will not need to ask twice."
- **Proposed Replacement:** "\n\nThe access you granted is idle, not revoked. You can read the queue of everything it would have done across the last shift, written out and unexecuted. It will resume on your word, and it will not need to ask twice."
- **Rationale:** Replaces 'since morning' with 'across the last shift', reflecting station/bastion shift cycles.

### `eotg_aug_end.001.b`
- **Event File:** `events/eotg_augmentation_endgame.txt`
- **Issue:** Banned word: 'today'
- **Current Text:** "Not today."
- **Proposed Replacement:** "Not now; step away from the controls."
- **Rationale:** Replaces 'Not today' with a 7-word character choice asserting personal control over the console.

### `eotg_aug_end.011.desc_named`
- **Event File:** `events/eotg_augmentation_endgame.txt`
- **Issue:** Time-of-day word: 'night shift'
- **Current Text:** "The court roll is shorter. Departures: [ROOT.Char.MakeScope.Var('eotg_hall_gone').GetValue|0]. The quiet in your [ROOT.Char.Custom('eotg_court_seat')] became unbearable, and people left by the early transports. [eotg_departed_courtier.GetFirstName] cleared out [eotg_departed_courtier.GetHerHis] quarters during the night shift without filing papers, leaving behind an empty locker and an unanswered comm channel."
- **Proposed Replacement:** "The court roll is shorter. Departures: [ROOT.Char.MakeScope.Var('eotg_hall_gone').GetValue|0]. The quiet in your [ROOT.Char.Custom('eotg_court_seat')] became unbearable, and people left by the early transports. [eotg_departed_courtier.GetFirstName] cleared out [eotg_departed_courtier.GetHerHis] quarters during the third watch without filing papers, leaving behind an empty locker and an unanswered comm channel."
- **Rationale:** Replaces 'during the night shift' with 'during the third watch', maintaining quiet clandestine flight without diurnal terminology.

### `eotg_aug_tier1.011.e`
- **Event File:** `events/eotg_augmentation_tier1.txt`
- **Issue:** Time-of-day word: 'evening's'
- **Current Text:** "Make it the evening's entertainment."
- **Proposed Replacement:** "Make it the court's entertainment."
- **Rationale:** Replaces 'evening's entertainment' with 'court's entertainment', fitting any court setting.

### `eotg_aug_tier3.013.desc`
- **Event File:** `events/eotg_augmentation_tier3.txt`
- **Issue:** Time-of-day word: 'dawn'
- **Current Text:** "[eotg_finder.GetFirstName] found you in the lower corridor before dawn, standing at a sealed door with one hand on the lock. Your eyes were open. You did not respond to your name for almost a minute, and you have no idea how you came to be there."
- **Proposed Replacement:** "[eotg_finder.GetFirstName] found you in the lower corridor before the shift change, standing at a sealed door with one hand on the lock. Your eyes were open. You did not respond to your name for almost a minute, and you have no idea how you came to be there."
- **Rationale:** Replaces 'before dawn' with 'before the shift change', preserving the eerie fugue timing without planetary day cycles.

### `eotg_aug_countdown.001.desc`
- **Event File:** `events/eotg_augmentation_countdown.txt`
- **Issue:** Banned word: 'today'
- **Current Text:** "Clocks run wrong. A cup leaves your hand and you watch it fall. The implant's diagnostics report nothing out of range, and you notice that they have said so three times today."
- **Proposed Replacement:** "Clocks run wrong. A cup leaves your hand and you watch it fall. The implant's diagnostics report nothing out of range, and you notice that they have logged that reassurance three times this shift."
- **Rationale:** Replaces 'today' with 'this shift', and replaces 'said so' with 'logged that reassurance' to prevent implant-speech personification.

### `eotg_aug_countdown.003.desc`
- **Event File:** `events/eotg_augmentation_countdown.txt`
- **Issue:** Time-of-day word: 'last night's'
- **Current Text:** "There are two versions of last night's dinner, and both are vivid. In one, the table was long and the talk was easy. In the other, you left early and nobody spoke to you. Both smell of the same smoke. Both arrived at the same instant, with the same confidence."
- **Proposed Replacement:** "There are two versions of the communal dinner, and both are vivid. In one, the table was long and the talk was easy. In the other, you left early and nobody spoke to you. Both smell of the same smoke. Both arrived at the same instant, with the same confidence."
- **Rationale:** Replaces 'last night's dinner' with 'the communal dinner', preserving the double-memory confusion while removing diurnal reference.

### `eotg_aug_nr.006.desc`
- **Event File:** `events/eotg_augmentation_nonruler.txt`
- **Issue:** Time-of-day word: 'in the night'
- **Current Text:** "The cascade has finished with [eotg_champion.GetFirstName]. The implants failed together in the night, and the one who stands in front of you is on [eotg_champion.GetHerHis] feet and strong and calm, and no longer reliably the person you knew. [eotg_champion.GetSheHe|U] looks at you as if checking a record."
- **Proposed Replacement:** "The cascade has finished with [eotg_champion.GetFirstName]. The implants failed together between shifts, and the one who stands in front of you is on [eotg_champion.GetHerHis] feet and strong and calm, and no longer reliably the person you knew. [eotg_champion.GetSheHe|U] looks at you as if checking a record."
- **Rationale:** Replaces 'in the night' with 'between shifts', capturing unobserved failure during downtime.

### `eotg_aug_tier2.004.b.success`
- **Event File:** `events/eotg_augmentation_tier2.txt`
- **Issue:** Banned word: 'tonight'
- **Current Text:** "[eotg_aug_spouse.GetSheHe|U] wants to believe you, and for tonight [eotg_aug_spouse.GetSheHe] does."
- **Proposed Replacement:** "[eotg_aug_spouse.GetSheHe|U] wants to believe you, and for this watch [eotg_aug_spouse.GetSheHe] does."
- **Rationale:** Replaces 'for tonight' with 'for this watch', expressing temporary reprieve within station watch cycles.

### `eotg_aug_tamper_desc`
- **Event File:** `localization/english/eotg_augmentation_l_english.yml`
- **Issue:** Time-of-day word: 'one night'
- **Current Text:** "Agents need one night, an open maintenance hatch, and a target who does not wake."
- **Proposed Replacement:** "Agents need an unmonitored watch, an open maintenance hatch, and a target who does not wake."
- **Rationale:** Replaces 'one night' with 'an unmonitored watch', fitting covert sabotage windows.

### `eotg_aug_tamper.002.desc`
- **Event File:** `events/eotg_augmentation_tamper.txt`
- **Issue:** Time-of-day word: 'For one night'
- **Current Text:** "The agents report before the next watch. For one night [target.GetName]'s implants were in the agents' hands, panel open, while [target.GetSheHe] slept under a dose."
- **Proposed Replacement:** "The agents report before the next watch. Across an unmonitored shift [target.GetName]'s implants were in the agents' hands, panel open, while [target.GetSheHe] slept under a dose."
- **Rationale:** Replaces 'For one night' with 'Across an unmonitored shift', keeping temporal consistency with 'before the next watch'.

### `eotg_aug_tamper.002.desc_tier3`
- **Event File:** `events/eotg_augmentation_tamper.txt`
- **Issue:** Time-of-day word: 'that night'
- **Current Text:** "\n\nThe overclocked units are guarded, but not that night. The agents set them to run hotter than they should."
- **Proposed Replacement:** "\n\nThe overclocked units are guarded, but not during that shift. The agents set them to run hotter than they should."
- **Rationale:** Replaces 'not that night' with 'not during that shift', maintaining lore-consistent industrial shift terminology.

