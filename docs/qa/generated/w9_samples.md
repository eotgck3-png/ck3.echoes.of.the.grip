# W9 samples: patron letters

File: `localization/english/eotg_augmentation_l_english.yml`. 4 new keys (`eotg_aug_patron.010.t`, `.desc_writeoff`, `.desc_betrayal`, `.desc_settlement`) and 3 converted keys (`eotg_aug_patron.006.*_absent`). Worklist: `docs/specs/build/w9_loc_worklist.md`. Patron scorecard row after W9: 10 events, voice 90 / 0 / 10 (first / second / neutral; the neutral is the letter, whose body is the sender's second person and counts under the letter exception), dialogue 70%. Lint against baseline: 0 new.

**1. eotg_aug_patron.010 (the unsigned letter; second person is the sender's, the corporate "we" is not the forecast "we")**
- .t: "The Final Account"
- The salutation is folded into each body (no `opening` key): every body starts "[ROOT.Char.GetFirstName], the account is closed." and a paragraph break.
- .desc_writeoff (owner Neurofractured, write-off flag): "We have reviewed your account. We do not service broken units, and the hardware in you is no longer worth servicing. What you owe is due now."
- .desc_betrayal (grievance 3+): "We kept a ledger of your refusals. These terms are final. We were never buying the implant. We were buying you, and you have stopped being for sale."
- .desc_settlement (demand 4+): "On our side, nothing remains but to settle. The terms enclosed are generous. Settle the account, and you will not hear from us again."

**2. eotg_aug_patron.006.desc_writeoff_absent (in-flight fallback, now a character event in first person)**
- Before: "The message arrives sealed... [syndicate] has reviewed your account and closed it. The terms are brief: the syndicate does not service broken units, and what you owe is due now."
- After: "The message arrives sealed, with no courier waiting for an answer. [syndicate] has reviewed my account and closed it. The terms are brief: the syndicate does not service broken units, and what I owe is due now."

**3. The other two converted fallbacks**
- desc_betrayal_absent: "...A ledger of my refusals, and it is closed. The terms are final and written without heat: they were never buying the implant. They were buying me, and I have stopped being for sale."
- desc_settlement_absent: "A courier brings me the final account, sealed. [syndicate] has closed it on its side, and would like to settle with me..."

## Notes for the reviewer
- The letter bodies carry no narration, no signature and no sender name; the syndicate speaks as "we". There is no I, me or my in the five keys, and the salutation opens each body.
- Each body is true on its path: writeoff shows for the write-off flag, betrayal for grievance 3+, settlement otherwise. All four reused options (.006.a, .b, .d, .f) answer a letter; "Settle the account, and you will not hear from us again" is conditional, so it holds on every path.
- The three `_absent` keys now carry I, me or my and no second person.
- Frontier .003 and .030: the spec lists them for conversion, but the script half has not landed (no `opening` or `letter_event` in `events/eotg_frontier_events.txt`, and no worklist rows), so no frontier loc was changed. They are ready for a follow-up when the scripter converts them.
- No time-of-day words in the patron.006 and patron.010 keys (grep returns 0).
