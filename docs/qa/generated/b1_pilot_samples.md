# B1 pilot samples: tier1 loc (W1 + W4)

File: `localization/english/eotg_augmentation_l_english.yml`, `eotg_aug_tier1.*` keys. 47 lines changed. Scorecard for `eotg_augmentation_tier1.txt` (22 events): voice 68.2 / 0.0 / 31.8 (first / second / neutral), dialogue 45.5%, `#EMP` 0%.

## Descs

**1. eotg_aug_tier1.001.desc (first person, plain conversion)**
- Before: "...The cup in your hand dents, and the room goes quiet mid-petition as councillors watch you pry your own fingers loose."
- After: "...The cup in my hand dents, and the room goes quiet mid-petition as the councillors watch me pry my own fingers loose."

**2. eotg_aug_tier1.007.desc (neutral, no "you", the implant no longer "wants")**
- Before: "An update is due, and the implant wants it. It says so the way a bad tooth does: a low, patient insistence behind everything else you are trying to think about. ..."
- After: "An update is due, and the notice will not leave the mind alone. It sits the way a bad tooth does: a low, patient insistence behind every other thought. The technicians have a window open this week. It will not stay open."

**3. eotg_aug_tier1.021.desc_reassured (re-framed: an expert's questions, not fear; neutral)**
- Before: "The surgeon has told you three times that it is safe. You notice that you needed to hear it each time."
- After: "Every risk was put to the surgeon until the replies came without a pause. They held. The margins are still being turned over."

## Options

**4. eotg_aug_tier1.005.d (re-gated: duchy authority; was "Leave the hall.")**
- After: "Adjourn. The gathering is mine to end."

**5. eotg_aug_tier1.003.e (re-gated: intrigue; was "There is nothing to tell; I am unchanged.")**
- After: "Deflect, and read what [eotg_concerned_vassal.GetSheHe] came here fishing for."

## Dialogue

**6. eotg_aug_tier1.010.desc (sparring partner, W4)**
- Before: "...You did not choose the last two exchanges. The implant did, and you followed it faster than your intent could. The drill floor has stopped moving. Nobody applauds, because nobody is sure whose win it was."
- After: "...I did not choose the last two exchanges. The forecast ran ahead of me, and my hand moved before I did. The drill floor has stopped moving. "Was that you?" [eotg_sparring_partner.GetSheHe] asks from the floor. Nobody applauds, because nobody is sure."

## Notes for the reviewer

- Speakers: 003, 004, 009, 010, 012 (main desc), 016, 017 (all four outcome lines), 018, 019 (recovered and worse), 021. Ten of 22 events. The implant never speaks; 019 worse is a voice heard through the hatch.
- Appended fragments (015, 017, 019, 022) keep "me" where they refer to root; 019 and 021 are neutral.
- 004.e and 018.e keep their existing text (both already fit the reframe).
- `.success`, `.failure` and `.tt` outcome lines were not touched (short outcome lines, second person allowed under §12.1 rule 5).
- Removed "the new hardware" in 022.desc_clean ("the new implant"). Avoided "answers" (L012 register) in 021.desc_reassured.
- 021 speech ("What you choose now...") stays true on both paths: the reassured fragment follows it.

- Post-review (lore and QA): 017 desc, desc_victory, desc_narrow, desc_defeat and desc_severe are now path-neutral so they hold after 016.d (implant switched off).
