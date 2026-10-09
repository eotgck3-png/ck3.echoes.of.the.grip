# B2 samples: tier2 loc (W1 + W4 + W5 reframes)

File: `localization/english/eotg_augmentation_l_english.yml`, `eotg_aug_tier2.*` keys. 64 keys rewritten. Scorecard for `eotg_augmentation_tier2.txt` (21 events): voice 66.7 / 0.0 / 33.3 (first / second / neutral), dialogue 47.6%, `#EMP` 0%.

**1. eotg_aug_tier2.004.desc (first person plus a spouse line, W1 + W4)**
- Before: "For weeks your [wife/husband], [name], has said very little. ... the questions are specific: when did you stop reaching for [her] first? When did the warmth go out of your hands? You have answers. They are very precise. That is, apparently, the problem."
- After: "For weeks my [wife/husband], [name], has said very little. This time [she] says a great deal, and the questions are specific. [She] wants to know when I stopped reaching for [her] first. "When did the warmth go out of your hands?" [she] asks. I have answers. They are very precise. That is, apparently, the problem."

**2. eotg_aug_tier2.012.desc (spymaster line, seat by GetCouncillorPosition, true on every desc variant)**
- Before: "Your [spymaster], [name], is flagged. The implant cross-referenced ... It does not say what [she] is guilty of."
- After: "My [spymaster], [name], stands across the table, flagged. The implant cross-referenced ... It does not say what [she] is guilty of. "Is there a problem?" [she] asks." The senses_true and senses_false fragments become "I read the room the way the implant reads it ..." and both keep working after the line.

**3. eotg_aug_tier2.020.e (reframe: the model is never a person or a speaker)**
- Before: "At last, someone who understands."
- After: "Trust the forecast. It has not once misread me."

**4. eotg_aug_tier2.003.desc_voice (rule 12: no "wants")**
- Before: "The second self has read the proposal already. It wants this too. It has priced the cost in the same terms you would have, a beat before you did."
- After: "The model of me has run the proposal already. The cost is priced in the same terms I would have used, a beat before I used them, and my answer is forecast as yes."

## Reframes (same keys)
001.d "Keep my family close and talking until the feeling catches up." / 002.d "Win the frightened youngest back with patience." / 003.d "Order the combat-rated install, with no safety margin." / 004.d "Rebuild the old warmth from study, and perform it." / 006.e "Find the dampener in the firmware, and strip it out." / 007.d "Rule the case by the realm's law, from the seat." / 008.e "Run the record down to the hand that did it, and let them know." / 009.e "Cross-check every lie in the archive, with a light touch." / 010.d "Stay, and hold the room steady for the other parent." / 011.d "Tighten the tax cycle past the model's figure." / 012.e "Arrest [her] on my own authority." / 013.d "Make both suppliers pay for the contract." / 017.e "No. I rule from this seat, and it does not bend, even for you." / 019.e "Read the projection to the last line, and act on it." / 019.f "Convene the council, and put it before them." / 020.d "Question the model's forecasts until I know how it predicts me." / 020.e above / 021.d "Find where the model went wrong, correct it, and say so before the court."

## Notes for the reviewer
- Speakers (10 of 21 events): 001 (desc_speaker only), 004, 005, 007, 010 (unattributed "someone murmurs", because eotg_other_parent is optional), 012, 016 (desc_culprit only), 017, 018 (all three variants), 021. 011 skipped: its only candidate speaker lives in a random_list tooltip line.
- Neutral (7): 002, 008, 009, 011, 014, 015, 019. No event is second person. Rule 13 fragments in first-person events carry I/me/my.
- Implant agency removed: 003.desc_voice ("wants"), 008 ("held it back" now the dampening), 011 ("came back with a proposal"), 012.d ("than it" now "than the figure"), 015 ("admits the ranking is weak" now the log marks it), 019 ("solution" and "files its objection"), 021 ("defended with a confidence"), 020.desc_nerves ("has used the time").
- Speech lines are true for any speaker: 001 "Did you hear me?", 012 "Is there a problem?", 016 "Hear me before you decide.", 017 "Something changes. I am not asking.", 021 "I will not forget how this was done." (both 012 paths accuse).
- Outcome lines converted to first person: 004.b, 005.e, 013.c.failure, 019.c. 011.c lines now say "The [steward]" (neutral).
