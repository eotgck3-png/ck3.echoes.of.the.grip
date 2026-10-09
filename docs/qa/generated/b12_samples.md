# B12 samples: frontier loc (L018 + W1 + W4)

File: `localization/english/eotg_frontier_l_english.yml`, `eotg_frontier.*` desc keys (it holds all the event keys). 34 keys touched, all desc keys; no option, tt, decision, modifier or title key changed. Scorecard for `eotg_frontier_events.txt` (19 events): voice 73.7 / 0.0 / 26.3 (first / second / neutral), dialogue 52.6%, `#EMP` 0%. Lint 0 findings against baseline (L018 0). PX LSP: 0 diagnostics. Duplicate keys 0. BOM present.

**1. eotg_frontier.036.desc (L018 "tomorrow" gone, urgency kept, W4 crew chief)**
- Before: "A survey crew in [county] has struck a seam richer than anything on the charts. The crew chief wants to start cutting tomorrow. The surveyors want to know how far it runs first."
- After: "A survey crew in [county] has struck a seam richer than anything on the charts. The crew chief wants to start cutting at once. "Every shift we spend waiting is ore we are not moving," the crew chief tells me. The surveyors want to know how far it runs first."

**2. eotg_frontier.004.desc_military (L018 "day and night" gone)**
- Before: "The garrison has dug in for good, and the approaches to the Region are watched day and night."
- After: "The garrison has dug in for good, and the approaches to the Region are watched without a break."

**3. eotg_frontier.031.desc (W1 + W4, law at 866 explicit)**
- Before: "...and now wants a voice in how the Region is run: who is appointed, what is built, where the money goes. That is not [her] to have. The Region is yours, under your law and nobody else's..."
- After: "[sponsor] has paid for a good part of the work in [county], and has come to ask for more than credit. "Who is appointed, what is built, where the money goes," [she] says. "I should be asked." That is not [her] to have. The Region is mine, under my law and nobody else's, and the backing never came with a say. ..."

**4. eotg_frontier.033.desc (W1 + W4)**
- Before: "[founder] wants the crews ... working longer shifts until the next stage is done. ... Both sides are waiting to hear from you."
- After: "[founder] wants the crews in [county] on longer shifts. "The next stage is close," [she] says. "Longer shifts will finish it." The crews say they are already working all the hours there are, ... Both sides are waiting to hear from me."

**5. eotg_frontier.005.desc_low_control (second person in a fragment, event moved to first person)**
- Before: "Your officials never had much hold out here, and the settlers stopped looking to them."
- After: "My officials never had much hold out here, and the settlers stopped looking to them."

## Notes for the reviewer
- W1: the seven worklist keys are first person (001.desc_self, 010.desc, 031.desc, 032.desc_liege, 033.desc, 041.desc_head, 041.desc_order). One further catch outside the worklist: 005.desc_low_control ("Your officials"). Left as the worklist said: 031.a, 037.a_tt. Also untouched, as tt/option lines under rule 5: 001.start_self_tt ("with you leading the work"), 010.offer_tt ("Your offer").
- First-person events (14 of 19): 001, 003, 005, 010, 021, 030, 031, 032, 033, 035, 036, 037, 040, 041. Every desc variant of these carries I/me/my (rule 13), except the nine 010.desc_offer_* list lines, which are list entries and stay neutral.
- Neutral (5): 002, 004, 020, 034, 042 (no speaker or only a generic report; the only edit was 004.desc_military). Dialogue (10 of 19, 52.6%): 001 (desc_other), 003, 030, 031, 032 (both variants), 033, 035 (both variants), 036, 040 (two variants), 041 (head and order). The 40% target was reachable.
- Speech true for any speaker: 001 "Name the first project, and I will lead it." (candidate is the best steward at court or the taker, so an adult); 003 "If the Frontier succeeds, I share the credit. If it fails, I share the loss." (any ruler); 030 "I will ask for less than [sponsor] does, and pay on the same schedule." (any ruler); 031 "Who is appointed, what is built, where the money goes. I should be asked."; 032 settlers: the unnamed lead spokesperson, liege "I will take my share when the first returns come in."; 033 "The next stage is close. Longer shifts will finish it."; 035 and 036: the unnamed crew chief, no pronoun used; 040 "Convoy guards, for a fee." / "I will put the company's money behind the venture."; 041 "The faithful out there should not stand alone."
- Rule 12: no implant appears in the frontier file, so it does not apply.
- Terms kept: Region, Frontier, System, backer. No "knight". Canadian spelling (honour, defence).
- 005: "I should have seen it sooner" (desc_no_founder) and "I sent too many lightly guarded convoys" (desc_danger) put some blame on the ruler. Check against the frontier spec.

## W9: letters (eotg_frontier.003 and .030)
Both events are `letter_event`s now, so the text is the sender's own letter to the ruler (second person allowed). 2 keys added (`.003.opening`, `.030.opening`), 3 rewritten (`.003.desc`, `.003.desc_replace`, `.030.desc`). Options, tooltips and titles untouched. No time words. Lint 0 against baseline (both L010 cleared), PX 0 diagnostics, duplicate keys 0, BOM present, LF endings.

- eotg_frontier.003.opening: "To [ROOT.Char.GetTitledFirstName],"
- eotg_frontier.003.desc: "News of the work in [county] has reached me, and I would like to help pay for it: regular shipments of money and supplies, for as long as the Frontier needs the help. The first shipment can leave as soon as you agree.\n\nI ask for no claim on the Region and no say in how it is run, and none comes with my help. If the Frontier succeeds, I will share the credit. If it fails, I will share the loss."
- eotg_frontier.003.desc_replace: "\n\nI understand the Frontier already has a backer. If you accept my offer, that arrangement ends."
- eotg_frontier.030.opening: "To [ROOT.Char.GetTitledFirstName], on a matter of business,"
- eotg_frontier.030.desc: "I have been watching the work in [county], and I offer better terms than [sponsor] does. I can send the first shipment at once, and pay every year after, on the same schedule as [sponsor].\n\nI know that taking my offer ends your arrangement with [sponsor], who will not take it kindly. Neither of us would gain any claim on the Region either way, and neither would have a say in how it is run."

Notes: the .003 letter says "none comes with my help" so it holds for any sender; "as soon as you agree" matches accept_tt (first shipment at once). The .003 letter has no sign-off because desc_replace is appended after it; the sender's portrait names the writer. The .030 opening does not name the current backer. Sender's gender is never referenced.
