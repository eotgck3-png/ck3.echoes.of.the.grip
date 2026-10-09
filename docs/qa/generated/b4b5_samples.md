# B4+B5 samples: fracture loc (W1 + W4 + W5 reframes)

File: `localization/english/eotg_augmentation_l_english.yml`, `eotg_fracture.*` keys. 116 keys rewritten. Scorecard for `eotg_augmentation_fracture.txt` (29 events): voice 93.1 / 6.9 / 0.0 (first / second / neutral), dialogue 48.3%, `#EMP` 0%. The 6.9% second person is the two W7 set pieces (fracture.004 and .027 descs), left alone by instruction. Lint against baseline: 0 new; L018 fell from 3 to 2.

**1. eotg_fracture.008.desc (Neurofractured first person, plus a speaker who is any heir or spouse)**
- Before: "You greet [named] and the word that leaves your mouth is not [her] name. You hear it a moment after you say it. [She] hears it at once."
- After: "I greet [named] and the word that leaves my mouth is not [her] name. I hear it a moment after I say it. "That is not my name," [she] says."

**2. eotg_fracture.017.desc (rule 12: the model no longer wants; rule 7: no second speaker)**
- Before: "A request opens across your thoughts, formatted like an access prompt. The implant's model asks for wider access to act ahead of you. It lists what it wants: ..."
- After: "A request opens across my thoughts, formatted like an access prompt. The implant's model flags wider access to act ahead of me, and lists it: motor pre-emption, scheduling of my attention, first call on decisions made in a crisis. Its reasons are attached. The reasons are good."

**3. eotg_fracture.022.desc_first and .desc_known (lore-approved text, applied exactly; options unchanged)**
- desc_first: "This is the first time I have caught it. The word did not feel like a slip. It felt like the more accurate pronoun, applied half a second before I chose it."
- desc_known: "I saw it coming. The model has been treating my decisions as joint for some time, and I have been letting it. Now the grammar has caught up in public."

**4. eotg_fracture.013.t (L018: no time-of-day word)**
- Before: "Memory of Tomorrow". After: "A Memory Out of Order".

## Reframes (21 of 23 written; 022.d locked, 027.c done as option text only)
002.e "Tend whoever is hurt, as I was taught." / 004.c "Perform the rites owed to the dead, and perform them correctly." / 004.e "Name replacements to the empty posts before the next watch. It is mine to order." / 005.e "Tell it as a seizure, built from what [heir] actually saw." / 006.e "Bring [vassal] to my table, and talk [vassal] round." / 007.d "Price the plans, and find the buyer." / 008.d "Talk [named] back to [named] name, patiently." / 010.d "Say the rite of blessing over the glass, word for word." / 011.e "Press [witness] until [witness] agrees [witness] heard nothing." / 012.e "Treat the face as a cover, and question it as one." / 013.d "Back the forecast with a calculated stake from the treasury." / 014.e "Test the overlay against the wall's plans, aloud, with help." / 015.d "Send it with a disarming note: "I don't remember writing this."" / 016.e "Set a blood-price from the seat, and pay [victim]'s family." / 017.e "No device speaks in my name. I hold this seat." / 018.d "Hold my position by drill, as a soldier holds a line." / 019.d "Take [accused] whole house into the cells. I will have it so." / 023.e "Hold the muster until the scouts report." / 024.d "Sit with [changed]. I know these symptoms, and I can talk [changed] through them." / 025.d "Order [keeper] taken into custody. This was planned for months." / 027.c "Fight it channel by channel, as a drilled soldier fights a line." (009.e was already a fit and is unchanged.)

## Notes for the reviewer
- Speakers (12 of 29 events): 002 (wounded victim), 005 (heir), 006 (warrant vassal, faction branch), 008 (heir or spouse), 011 (witness), 012 (friend, lover or spouse), 014 (work crew foreman), 021 (a corridor guard), 023 (senior marshal, peace branch), 024 (the changed courtier), 025 (keeper, spouse or heir), plus the kin and the accused already speaking in 020. No line assumes rank, kinship or acquaintance, and none is the implant. Dialogue reached 48.3%, so the target was reachable under rule 7.
- Rule 7 and 12 edits: no quoted implant line and no implant "asks", "wants" or "decides". 002 ("It does not particularly care" is now a log with no correction), 006.c ("Let the implant decide" is now "Leave the matter to the model's forecast."), 017.d (no longer addresses the implant: "Set the price of access before I grant it."), 027.tt and 028.desc.
- 006.c avoids the register word "warrant" (new L012 hit otherwise).
- W7 left alone: fracture.004 descs, fracture.027 descs.
- Time-of-day words: the grep over the fracture keys returns only a comment line. 013.t is retitled.
- Left as is: 015.b.reveal_* now say "the letter I read"; 023.f and .f_war keep "the rest of you", which is an address to others and an option line.
