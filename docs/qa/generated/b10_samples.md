# B10 samples: A Fracturing Inheritance loc (W1 + W4 + reframes)

File: `localization/english/eotg_aug_inherit_l_english.yml`, `eotg_aug_inherit.*` keys. 79 keys changed, none added or removed. Scorecard for `eotg_augmentation_inherit.txt` (27 events): voice 63.0 / 0.0 / 37.0 (first / second / neutral), dialogue 63.0%, `#EMP` 0%.

## 1. Reframe, option .001.e (authority, convening the council by right)
- Before: "The succession comes first. Call the council."
- After: "The succession is mine to settle. Convene the council."
- Reads under all 4 profiles, 5 bonds and both sources: it names no report content.

## 2. Reframe, option .009.d (martial: set the guard and the ground, then wait)
- Before: "Let it come to me, then." / tooltip "You stand ready for whatever comes."
- After: "Set the guard, choose the ground, and wait." / tooltip "The guard is set on ground you chose. Whatever comes will find it ready."
- Fits kill_ruler, massacre, next_two and self: it says nothing about what is coming.

## 3. Voice and rule 14 on an existing speaker, eotg_aug_inherit.002.desc_rage
- Before: "[heir] will not sit. [heir] walks the length of the room and back, working a hand that has split at the knuckles. "It closed before I decided," [heir] says. "I watched it do it." A dented cup sits on the table between you, where it was thrown."
- After: "[heir] will not sit. I watch [heir] walk the length of the room and back, working a hand that has split at the knuckles. A dented cup sits on the table where it was thrown. "My hand closed before I decided," [heir] says. "I watched it close.""
- Why: the narrator is the ruler (I). The speaker's "it" could read as the implant acting, so it now names the hand (rule 14). The closing sensory sentence moved ahead of the speech.

## 4. W4 dialogue, eotg_aug_inherit.026.desc_warden (root is the heir; the old ruler speaks)
- Before: "You hold the [seat], and [old ruler] holds the controls. Every paper crosses [old ruler]'s desk before it reaches yours, and the staff still bring questions to the older hand first. You have the title. The routine has not caught up. You may keep that arrangement or end it, and the staff are watching which you choose."
- After: "I hold the [seat], and [old ruler] holds the controls. Every paper crosses [old ruler]'s desk before it reaches mine, and the staff still bring questions to the older hand first. "Ask me when you need to. Don't ask me when you don't," [old ruler] says, and slides the day's first paper across to me. I have the title. The routine has not caught up. I may keep that arrangement or end it, and the staff are watching which I choose."
- The line adds advice and does not restate the desk routine. It is true whoever the old ruler is: no kinship or rank assumed.

## Notes for the reviewer
- First person (17 events): .001, .002, .003, .006, .007, .009, .010, .012, .014, .015, .017, .018, .020, .024, .025, .026, .027. Every desc key and appended fragment in them carries I, me or my outside speech. .025 and .026 are told by the heir.
- Neutral (10 events): .004, .005, .008, .011, .013, .016, .019, .021, .022, .023. .004 and .019 are unchanged; their narration already held no "you".
- Second person in descs: 0 events. Spec §12.1 rule 5 limits second person to letters, speech and short option lines, so the "about 5%" bucket is left empty.
- New speakers: heir in .011, .012, .013 (accept and violent), .014, .016 (both descs), .020, .022 (both), .023 (both), .024; second in .027 (both); old ruler in .026 (both). Existing speakers (.002, .003, .006, .007, .015, .018) kept. In .002, .003, .006, .015 and .018 the closing sensory sentence after the speech moved ahead of it or was folded in.
- Skipped, optional-scope speakers: .001, .004, .005, .008, .009, .010, .017, .021, .025. No generic unattributed line added.
- Lore: L12 (.019) untouched and still found, not shown. .016 child fragment untouched (one plain sentence). The heir's ledger certainty in .016, .025 and .002 is belief ("It was settled before I wrote the first name"). No "tonight". The cells and "lay to rest" untouched.
- The implant never speaks or acts. The two grep hits for "wants" and "chooses" are the heir (.001) and councillors (.005).
- .016 lines: "Asked why, [heir] says only..." implies the heir can be questioned before options a, b and c. It is stated as a plain event, not custody.
