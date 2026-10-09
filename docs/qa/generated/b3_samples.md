# B3 samples: tier3 loc (W1 + W4 + W5 reframes)

File: `localization/english/eotg_augmentation_l_english.yml`, `eotg_aug_tier3.*` keys. 100 keys touched across the first pass and the review pass. Scorecard for `eotg_augmentation_tier3.txt` (24 events): voice 87.5 / 0.0 / 12.5 (first / second / neutral), dialogue 45.8%, `#EMP` 0%, L017 new findings 0 against baseline.

**1. eotg_aug_tier3.013.desc (first person plus a finder line, W1 + W4)**
- Before: "[finder] found you in the lower corridor while it was empty, standing at a sealed door with one hand on the lock. Your eyes were open. You did not respond to your name for almost a minute, and you have no idea how you came to be there."
- After: "[finder] found me in the lower corridor while it was empty, standing at a sealed door with one hand on the lock. My eyes were open. "You did not know your own name," [finder] tells me. "Not for almost a minute." I have no idea how I came to be there."

**2. eotg_aug_tier3.019.desc (rule 12: the implant no longer "is in favour", plus a delegate line)**
- Before: "Your hands are not steady enough for everything on your desk. [delegate] has offered to carry some of it. The implant rates the offer favourably and has already built a table of what to hand over. For once it is in favour of someone else deciding."
- After: "My hands are not steady enough for everything on my desk. [delegate] steps forward. "Let me carry some of it," [delegate] says. The implant rates the offer favourably and has already built a table of what to hand over. For once the figures point toward someone else deciding."

**3. eotg_aug_tier3.012.desc_known (rule 12: the second self no longer asks)**
- Before: "You have noticed this before, the second self that finishes your sentences. It has never asked for anything. It is asking now, and it will take a reply."
- After: "I have noticed this before, the second self that finishes my sentences. Until now it only ran ahead. This time the thought ends in a question, and the question is waiting for a reply."

**4. eotg_aug_tier3.005.e (rule 12: the machine does not command)**
- Before: "Let the machine command from the rear."
- After: "Command from the rear, and follow the forecast."

## Reframes (same keys; 18 options plus 005.e)
001.e (martial) "Burn the reflex off in drill, on the practice posts." / 002.d (duchy+) "Present the new face to the court as the face of the seat." / 003.d (stewardship) "Put the night hours through the accounts." / 003.e (duchy+) "Clear tomorrow's business, and lie there anyway." / 004.e (intrigue) "Read the room past the count, and take [suspect]." / 005.d (martial) "Place myself where the plan breaks, at the head of the charge." / 006.d (duchy+) "From the seat, convene an inquiry into my own fitness." / 009.e (duchy+) "Stand behind the order. It went out under my seal." / 010.d (learning) "Read the readout, and run it right up to its tolerance." / 010.e (duchy+) "Halt the court, and shut it all down. Now." / 012.d (intrigue) "Test the thought for a plant before I act on it." / 013.e (duchy+) "Make the night watch account for the door." / 014.e (duchy+) "Call [claimant] a liar from the seat, and hold no inquiry." / 017.e (duchy+) "Order the guard out, and arrest them all." / 019.c (stewardship) "Delegate everything: who carries what, and how it reports back." / 020.d (diplomacy) "Tell [intervener] plainly that I am frightened, and agree to the downgrade." / 020.f (intrigue) "Demand to know whose hand is behind this visit, and refuse." / 023.d (martial) "Take the plan, and lead the point of contact myself."

## Notes for the reviewer
- Speakers (11 of 24 events): 003 (unattributed "the watch officer", since the script saves no scope), 004 (desc_suspect fragment only), 006, 007, 009, 013 (main desc; desc_alone has none), 014, 015 (both variants), 019, 020, 021. Reported speech in 006, 014, 020 and 021 became one direct line each.
- Neutral (3): 004, 023, 024. After review 003, 007, 008 and 015 are first person, because root is never narrated neutrally through body parts (that is the Seamless register, rules 1, 7, 13). No event is second person. First-person events carry I/me/my in every desc variant (rule 13).
- Rule 12 flags fixed: 005.e, 012.desc_known, 019.desc. Also softened: 004.desc_suspect ("has been waiting for [her] to move" now a flag that has not cleared), 010.desc ("the system wants to throttle itself" now a throttle flag), 012.desc ("waiting on a response"), 023.desc ("recommends a plan"), 024.desc_overreach ("issued a correction ... does not apologize"), 024.desc_inconclusive.
- Speech true for any speaker: 003 "Are you well?", 004 "Is something wrong?", 006 "With respect, we must ask whether you are still fit to rule." (the spokesperson may be any vassal), 007 "You feel it too." (both are Overclocked), 009 "It is done, as you ordered." (an adult courtier), 014 "I have the dates.", 015 "As agreed." / "Shall we begin?", 019 "Let me carry some of it." (chancellor or spouse), 020 "Take some of it out now, while you can still choose." (spouse or heir), 021 "I carried out your order in good faith ...".
- 014.e "Call [claimant] a liar" reads the same whether the claimant is honest or exploiting the gap (the script does not read the truth flag).
- 004.e names `[eotg_suspect]`, which the option's trigger guarantees exists. 020.d and 020.f name `[eotg_intervener]`, which the event always saves.
- The titles (e.g. 011.t "The Feast You Didn't Eat") and the toasts were not touched.
- Review pass (lore + QA): 006.desc no longer says "three of my most senior vassals" (now "a delegation of my vassals"). Time-of-day words are gone from the tier3 keys (grep for night, dawn, morning, today, tonight, tomorrow, evening, sunrise and overnight returns 0): 003.c/d/e/f, 013.e. 012.d now reads "Treat the thought as an unverified report, and check it before I act." 015 alliance and rivalry are first person with one spoken line each that does not restate the narration. 007.desc, 008.desc, 003.desc, 013.desc and 014.desc follow the lore text. 004.e is "Watch [suspect] myself, then have [suspect] taken." 011.t is now "The Feast I Didn't Eat" (the only title touched). 014.b toasts are first person.
