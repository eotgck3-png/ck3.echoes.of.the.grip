# B11 samples: Neurofractured Kingpin batch A loc (W1 + W3 + W4 + reframes)

File: `localization/english/eotg_aug_kingpin_l_english.yml`, `eotg_aug_kingpin.*` batch A keys. 122 keys rewritten, 26 toast titles present (16 new in this pass). Scorecard for `eotg_augmentation_kingpin.txt` (42 events): voice 76.2 / 0.0 / 23.8 (first / second / neutral), dialogue 42.9% (was 35.7 / 45.2 / 19.0 and 14.3%).

**1. eotg_aug_kingpin.001.desc_reporter plus the band and kind fragments (W1 + W4, rule 13)**
- Before: "[reporter] brings the report in person, and waits while you read it." / crew: "...across the stacks and the shuttered market level." / band_flicker: "The tells are still small: a hand that moves before the decision does, a step taken a moment early."
- After: "[reporter] brings the report in person, and waits while I read it. "I would not have carried this up if it could wait," [reporter] says." / crew: "...across the stacks and the shuttered market level of my capital." / band_flicker: "...a step taken a moment early. I would miss them if I were not looking."
- The reporter line is true for a spymaster or a marshal and adds no fact. Every fragment that joins in sequence now carries I, me or my, so any kind, method and band pairing still reads. The band fragments are shared with .010 and .012 and were written to read after a hideout or a fire as well as a report.

**2. eotg_aug_kingpin.007.desc (W1 + W4: the informant speaks)**
- Before: "Your agents bring word of a quiet leak. [informant] has been passing your household routines and patrol rosters down to [kp]'s people... Nobody had thought to look until now."
- After: "My agents bring word of a quiet leak, and they bring [informant] with it. [informant] has been passing my household routines and patrol rosters down to [kp]'s people... Nobody had thought to look until now. "I only copied what I was handed," [informant] says."
- The line is a defence, true for a willing spy and a coerced one, and does not restate the leak. It adds no implant talk.

**3. eotg_aug_kingpin.005.c_infiltration and its tooltip (reframe to intrigue, W1)**
- Before: option "Give [lieutenant] a post, and watch every move." / tooltip "[lieutenant] joins your household, and you know exactly whom [lieutenant] reports to."
- After: option "Give [lieutenant] a post, and read everything [lieutenant] touches." / tooltip "[lieutenant] joins my household, and I know exactly whom [lieutenant] reports to."
- The option now names the spymaster's craft (reading what the plant handles), which is what the education_intrigue gate tests. Light touch: the effect (unmasked, household post, leverage up) is unchanged.

**4. eotg_aug_kingpin.011.desc (W1 + W4: the boss's order, no implant talk)**
- Before: "Your guards assemble at the blast doors... Below, [kp]'s people have thrown barricades across the transit hubs, and the corridors echo with shouting as the assault begins. Whatever happens next, it happens level by level, door by door."
- After: "My guards assemble at the blast doors... as the assault begins. [kp] gives the order and it is repeated down the line: "Hold the hubs. Make the guard come to us." Whatever happens next, it happens level by level, door by door."
- The order is relayed, so the line needs no physical presence and no volume (a cold-mind boss still gives it). It names no kind noun, so it holds for crew, syndicate, front and hired.

## W3 toast titles (16, no numbers, no organization noun, no band or leverage words)
- .005 c_blackmail: "The File Cut the Other Way" / "The Move Was Seen Coming".
- .006 c_purge: "Talked Down" / "The Talk Went Nowhere".
- .007 b: "The Informant Now Reports to Me" / "The Informant Would Not Turn".
- .010 a: "Taken Alive" / "Broke Through the Guard" (true when the boss stood in the audience chamber). .010 b: "Taken Quietly" / "The Quiet Arrest Was Blown".
- .011 a: "The Sweep Found Its Target" / "The Lower Levels Held" (fits both the Break and the Arrangement that follow).
- .015 a: "The Audit Found Enough" / "The Audit Turned Up Nothing".
- .068 a: "Cut Down in the Lower Levels" / "Lost in the Lower Levels" (an ending of a massacre, no triumph).

## Reframes
- .006 b_cold (stewardship): "Send back an invoice of my own." became "Answer with my own ledger, line for line."
- .008 c (duchy authority): "Send the guard into the lower levels." became "Command the guard into the lower levels."; its tooltip is "My guards go into the lower levels to break the demand by force."

## Notes for the reviewers
- First person (18 events): .001 to .007, .009 to .013, .015, .040, .061, .069, .070, .073. Neutral (9): .008, .014, .060, .062, .068, .071, .074, .075, .076. Second person in a main desc: 0 events (rule 5 limits it to letters, speech and short option lines, so the "about 5%" bucket is empty, as in B10). Second person remains only inside speech and in unchanged option lines.
- The first-person leaves (.061, .069, .070, .073) rewrote their shared `desc_end_*` fragments to "By the end, I saw..." so rule 13 holds. .060, .062, .068 and .071 to .076 keep the old third-person end fragments (neutral events).
- W4 speakers added (12): .001 reporter (not desc_none), .004 courier, .007 informant, .010 boss (audience arrest only), .011 boss's relayed order, .012 victim (only where one exists), .014 the watch captain, .015 clinic attendant, .040 messenger, .061 boss at the trial, .069 boss (the batch A `desc` only), .070 boss. Existing speakers kept: .002, .003 (noclaim), .005, .006, .009. Batch B untouched. No line has the implant as a speaker or an agent. The mind lines in .002, .005 and .006 are the fixed §5.2.4 / §7.3 wordings and forecast only the boss.
- Skipped on purpose: .008 (a written demand), .013 (the boss is silent under guard), .060, .062, .068, .071, .073, .076 (the boss would contradict the narration or restate it).
- Two lint L011 hits (they/them in speech naming one character) were fixed by rewording the .011 and .014 lines.
- Modifier and opinion descriptions are unchanged (second person, outside this pass).

## Review fixes applied (lore conditional pass, QA fix-first)
- .012: `desc_victim` is now for adult victims ("Nobody warned us," ... tells me); new key `desc_victim_young` ("...is brought to me wounded.", no speech).
- .070: "lead" is a leash, so the line is now "Then I will not pull on it."
- .001 band fragments now hold at a distance (hosted also by .034 and .039): storm is reported ("a danger to anyone near [her]. The reports no longer soften it."), flicker adds "as far as I can judge", fracture ends "I no longer doubt any of it."
- .073 `desc_end_*` use "the reports I read" instead of "I saw" (the boss is not seen in person on several paths). .061, .069 and .070 keep "I saw".
- Toasts and outcomes: .015 failure "The Vault Stayed Shut" with "turns my auditors out"; .007 success "The Informant Was Turned" with first-person b.success and b.failure; .009 "watched [kp] change since the implant went in"; .010 audience "the order has barely left my mouth"; .040 flicker reworded.
- Rechecked: scorecard kingpin row still 42.9% dialogue (18 of 42), 76.2 / 0.0 / 23.8 voice; no events lost speech, because the fixes changed lines and did not remove any. Lint baseline clean, PX only the 6 known warnings, BOM single, no `\"`, no odd quotes, no duplicate keys, no time-of-day words.
