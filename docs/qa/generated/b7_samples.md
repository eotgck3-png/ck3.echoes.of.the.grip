# B7 samples: countdown, endgame, heir loc (W1 + W4 + W5 reframes + Seamless fixes)

File: `localization/english/eotg_augmentation_l_english.yml`, prefixes `eotg_aug_countdown.*`, `eotg_aug_end.*`, `eotg_aug_heir.*`. Refreshed from the current loc after the lore and QA fixes.

Scorecard rows (voice first / second / neutral, dialogue):
- countdown (6 events): 100 / 0 / 0, 50.0%.
- endgame (11): 36.4 / 27.3 / 36.4, 45.5%. The 27.3% second person is end.002, end.009 and end.010 (W7 set pieces, descs left alone). The 36.4% neutral is the four Seamless events (011, 040, 041, 042), exempt from the first-person floor. The four remaining events (001, 020, 030, 031) are all first person.
- heir (5): 60 / 20 / 20, 60%. The second person is heir.005.desc (W7); the neutral is heir.004 (see below).
- Lint against baseline: 0 new.

**1. Seamless fixes (applied as given in section 13.3; the root reference is the dynamic term)**
- heir.004.desc_seamless: "They address the chair. There is no one else in it to address."
- end.041.desc_residue_high: "Halfway through, the head tilts the way it once did for listening. [resigner] stops, looks at the chair, and starts again more slowly. The tilt is logged."
- end.041.desc_residue_low: "[resigner] finishes. Nothing in the face at the head of the table has moved, and [she] did not expect it to. Filed."
- end.011.desc and .desc_named: "...the quiet in the [ROOT.Char.Custom('eotg_court_seat')] became unbearable..." end.011.desc_none: "They watch the chair the way people watch a machine that is working correctly..."
- A grep of the Seamless keys for I, me, my, we and our shows no narration hit. The option end.011.c is now "Seal the docks. No departures without clearance.", with no "my" either.

**2. heir.004 (shown to Seamless owners too, so its main desc is neutral)**
- Before: "The decision is made. You can see it in how [heir] holds [herself]..."
- After: "The decision is made. It shows in how [heir] holds [herself]: the question is settled, and only the method remains." The ally, usurp and kill fragments say "beside the seat", "the incident log", "came to kill". The premonition and silent fragments stay first person (they never show to a Seamless owner).

**3. countdown.002.desc_voice (rule 12: the model no longer "offers"; ending per lore)**
- After: "...The gap is flagged for reconciliation, pending my word. I cannot tell whether accepting it would be a repair or a surrender."

**4. end.031.desc (the old ruler speaks)**
- After: "[old] knows my step in the corridor. "[ROOT.Char.GetFirstName]," [old] says through the door, before I have spoken: the forecast, still running ahead."

**5. countdown.004 (two keys, pending the scripter's branch)**
- `.desc_asks` (living victim aged 4+): the earlier text with the victim's "Why?".
- `.desc` (fallback, speech-free): "[victim] is on the floor, my hand is open, and the room is very still. I remember none of the strike. I remember the clarity before it, the sense that one clean motion would settle everything, and then the floor."

**6. end.001.d.tt (checked against the effect: maiming has weight 0 on this option, so only death and a clean outcome remain)**
- After: "The surgeons begin, with me awake. If I live, I live whole, and I will see all of it."

## Reframes (10, the count in the worklist table; its heading says 11)
countdown.001.e (duchy+) "Not now. The realm's business comes before the maintenance table, and the calendar is mine to set." / countdown.002.d (intrigue) "Ask who was near me in those days and who gains, and seize the likeliest." / countdown.003.d (diplomacy) "Draw the account out of those who were at the table, without making it an inquest." / countdown.004.e (learning) "Tend [victim] myself while [she] heals." / end.001.d (duchy+) "Awake, and at my order. I want to watch them take it out." / heir.001.e (intrigue) "Read the concern for what it is: a move on my seat." / heir.003.d (duchy+) "Then convene a hearing on my fitness, and let it judge me." / heir.004.ally_b (duchy+) "Not on these terms. I refuse it on my own standing." / heir.005.b (learning, option text only) "By law and by faith, it was murder." / heir.007.e (duchy+) "By the right of my seat, put [heir] under watch."

## Notes for the reviewer
- W7 desc keys untouched: end.002, end.009, end.010 and heir.005.
- Time-of-day words: none in these families (grep returns 0).
- Speakers: victim (countdown.004.desc_asks), courtier (005, 006), lead surgeon (end.001), councillor (end.020), heir (heir.001, .003, .007), the old ruler (end.031), the resigner (end.041, Seamless: quotes may say "you").
