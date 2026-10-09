# B9 samples: retinue, nonruler and activities loc (W1 + W4 + W5 reframes)

File: `localization/english/eotg_augmentation_l_english.yml`, prefixes `eotg_aug_retinue.*`, `eotg_aug_nr.*`, `eotg_aug_act.*` (plus the one `eotg_aug_tier2.018.desc_estranged` fix). 62 keys rewritten.

Scorecard rows (voice first / second / neutral, dialogue):
- retinue (5 events): 60.0 / 0.0 / 40.0, dialogue 60.0%.
- nonruler (6 events): 66.7 / 0.0 / 33.3, dialogue 50.0%.
- activities (6 events): 100.0 / 0.0 / 0.0, dialogue 66.7%. Activity backgrounds and themes untouched (background share stays 0%, as before).
- Lint against baseline: 0 new; L018 fell from 4 to 3.

**1. eotg_aug_nr.005.desc (liege is root, so "I" is the liege; the non-ruler speaks)**
- Before: "[champion] has changed, in a way you cannot point at. ... [She] says the right words in a slightly wrong order, and you have known [her] too long to miss it."
- After: "[champion] has changed, in a way I cannot point at. The same face, the same voice, the same service, and something in how [she] weighs things is different. "It is as you say," [she] says, a half-beat late, and I have known [her] too long to miss it." (No "my liege": the champion can be a courtier, a knight or kin.)

**2. eotg_aug_act.003.desc (accuser line, first person judge)**
- Before: "Between bouts, [accuser] seeks you out. [She] says [accused] wins with implants, not skill: a strike too fast for any arm, and a casing hot to the touch after every bout."
- After: "Between bouts, [accuser] seeks me out. "[accused] wins with implants, not skill," [she] says. "A strike too fast for any arm, and a casing hot to the touch after every bout.""

**3. eotg_aug_act.001.desc_ban (my law, and the reframed d must not claim a lawful sanction)**
- Before: "Your law prohibits augmentation. On your field, that is reason enough."
- After: "My law prohibits augmentation. On my field, that is reason enough." The option d reads "Reorder the tournament around them, and let my rank carry it." It names rank, never law.

**4. eotg_aug_act.002.f (works for a board game and for a physical bout)**
- Before: "Take the throttle off the reflexes."
- After: "Trust my trained reflexes, and take the throttle off."

## Reframes (17)
retinue.001.d (duchy+) "As head of this household, I order two fitted at once." / retinue.002.d (stewardship) "Fit both, and let them repay the cost from their pay." / retinue.003.e (intrigue) "Set my own eyes among the ranks." / retinue.004.e (duchy+) "Send the most resentful from my court. It is mine to order." / nr.001.e (intrigue) "Question [champion] on the motive behind it, and read the reply." / nr.002.d (duchy+) "Let my household field more of them." / nr.003.e (martial) "Keep [champion] on the roster, and drill through the fault." / nr.004.d (duchy+, no wronged party assumed) "Try [champion] in a court under my own authority." / nr.004.e (intrigue) "Stand back and let it end, then write that the hardware did it." / nr.005.e (duchy+) "By my order, confine [champion] to [her] rooms." / nr.006.f (martial) "Spend [champion] on the enemy line, as a commander spends a reserve." / act.001.d (duchy+) above / act.002.d (intrigue) "Run it where no marshal can read it, and let them call it skill." / act.002.f above / act.003.f (learning) "Run the casing heat through the overlay, and read it as evidence." / act.004.g (learning) "Hand the fitting round, and show how it seats and works, close up." / act.006.e (duchy+) "Cut the pilgrimage short. The realm calls."

## Notes for the reviewer
- Speakers: retinue 001 (volunteer), 002 (cand_a), 004 (unattributed knight, "one of them"); nr 001, 003, 005 (the champion); act 001 (senior marshal), 003 (accuser), 004 (a guest), 006 (a keeper). Lines assume no kinship, rank or acquaintance. Reported speech became direct only where it added the speaker's own claim.
- The "every eye" tic in act.004.desc_host was rewritten ("the hall keeps finding its way back to the head of the table").
- Neutral: retinue 003 and 004, nr 002 and 004 (root is not in the narration). In the nonruler fragments the root references that remain use "me" (nr.002.desc_overclocked "Whatever [she] is for me", nr.004.desc_none "cannot tell me").
- Titles touched: nr.002.t ("My [knight]'s New Edge"). The nr.*.msg_* lines are addressed to the non-ruler recipient, so their second person is correct and they were not changed.
- Time-of-day words: none in these key families (grep returns 0). tier2.018.desc_estranged now reads "Good day," instead of the morning greeting.
- Rule 12: nothing in these keys has the implant, overlay or model as an agent with a banned verb. act.002.g ("Run the schedule it has already drafted.") and retinue.003.desc_voice (the overlay tagging) were left as flags and tags.
