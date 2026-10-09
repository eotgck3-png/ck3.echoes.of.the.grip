# B6 samples: initiation loc (W1 + W4 + W5 reframes)

File: `localization/english/eotg_augmentation_l_english.yml`, `eotg_aug_init.*` keys (the prefix is `eotg_aug_init`, not `eotg_aug_initiation`). 61 keys rewritten. Scorecard for `eotg_augmentation_initiation.txt` (20 events): voice 90.0 / 0.0 / 10.0 (first / second / neutral), dialogue 60.0%, `#EMP` 0%, lint 0 new against baseline.

**1. eotg_aug_init.006.desc (first person plus a technician line, W1 + W4)**
- Before: "The old injury is still the first thing anyone notices about you. The clinics here do not patch. They replace. A technician from [company] has laid the specifications on the table."
- After: "The old injury is still the first thing anyone notices about me. A technician from [company] has laid the specifications on the table. "We do not patch," the technician says. "We replace.""

**2. eotg_aug_init.003.desc (no neutral narration through body parts, plus a technician line)**
- Before: "The years have done what war could not. The hands that once commanded armies are slower now. A technician has sought you out with a solution, for a price."
- After: "The years have done what war could not. My hands, which once commanded armies, are slower now. A technician has sought me out. "I can buy back the years," the technician says, "for a price.""

**3. eotg_aug_init.017.d (address-neutral: shown under desc and desc_self)**
- Before: "I trust your hands."
- After: "I trust the hands doing this."

**4. eotg_aug_init.003.d (re-gated: duchy+, authority; was "I will not grow old in front of them.")**
- After: "My court will not watch me grow old. Fit more."

## Reframes (12)
001.d (martial) "I know what the next wound costs. Armour me past it." / 001.e (diplomacy) "Tell the camp flesh was only ever a first draft, and let them repeat it." / 003.d (duchy+) above / 004.d (duchy+) "I command this host. I will lead it to the end as I am." / 005.e (intrigue) "Press [peer] on where the hardware came from, until it comes out." / 006.e (martial, loss-neutral so it holds for sight, eye and limb) "Build it for the field, not to match the old one." / 007.e (learning) "Run it past its rating. I know how far it will go." / 010.c (intrigue) "Do it, and arrange it so nothing traces back to me." / 013.d (stewardship, sound-neutral for desc_fractured) "Put them to open auction for the best price, and let it be known." / 014.d (diplomacy) "Keep [child] talking and calm through every hour of it." / 016.e (duchy+, works with a named rival and with desc_no_rival) "Let them learn to fear the seat." / 017.e (intrigue, hidden under desc_self) "Who stands to profit from this proposal?"

## Notes for the reviewer
- Speakers: unnamed in 001 (representative), 003, 004, 006, 007 (technician or surgeon), 013 (the dead parent's physician); named in 005 (peer, a vassal or courtier), 016 (rival), 017 (physician; desc_self has none). 012 keeps its two existing surgeon lines, each now in a first-person desc. 014 has the staying physician. Every line is true for any holder of the scope: nothing assumes kinship, rank or acquaintance.
- Neutral (2): 002 and 010, which have no root in the narration. Nothing is narrated neutrally through body parts: 003, 007, 008 and 011 are first person ("My hands", "my incision", "my nervous system").
- Time-of-day words: none in the initiation keys (grep for night, dawn, morning, today, tonight, tomorrow, evening, sunrise and overnight returns 0).
- Titles touched: 013.t "My [Mother/Father]'s Hardware" and 018.t "The Offer I Sought" (the only two with "you").
- 011 variants all carry I/me/my; the severe-outcome lines use "my arm", "one of my eyes" and "my sight".
- Rule 12: no implant, model or forecast acts as an agent in these keys. 017.e asks who profits from the proposal; it does not accuse the implant.
- The kept personality gates (001.c, 002.d, 003.e, ...) were not changed.
