# B4+B5 fracture: loc worklist from the W5 re-gating (eotg-scripter → eotg-localizer)

Source: `events/eotg_augmentation_fracture.txt`, all events .001–.029, W5/W6 per
`docs/specs/event_quality_v1.md` §13.1. Option keys and effects are unchanged. Only
the gate moved, so each line below must now read as its new axis (§13.1 step 7).
Voice: Neurofractured full first person (§12.1 rule 7). Check every desc branch
listed. The localizer writes no new keys. Every key here already exists.

## Re-axed options (text must change)

| Key | Current text | Old gate | New gate | What the new text must convey | Desc branches to read against |
|---|---|---|---|---|---|
| `eotg_fracture.002.e` | "Tend them with my own hands." | compassionate | education_learning | Hands-on medical competence: I dress the wound properly because I know how (physician's knowledge), not out of warmth alone. Must still work when only the dead victim exists or there's no victim at all: the option shows on every path. Avoid "them" referring to a living patient unless conditional, or keep it general ("the hurt"). | `.desc_wounded`, `.desc_none`, `.desc_killed` (stacked) |
| `eotg_fracture.004.c` | "Bury them with honours." | zealous | education_learning (still requires a dead victim) | That I know the rites owed to the dead and perform them correctly. Learned and ceremonial, not pious fervour. **W7 set piece:** option text only; desc keys belong to W7. | `.desc_killed` (+ `.desc_wounded` stacked) |
| `eotg_fracture.004.e` | "Fill the empty places by the next watch." | callous | tier ≥ duchy (still requires a victim) | Authority: I appoint replacements to the posts by right, before the next watch. A lord's order, not callousness. The current text already leans that way, so a light touch may suffice. **W7 set piece:** option text only. | `.desc_killed`, `.desc_wounded` |
| `eotg_fracture.005.e` | "It was a seizure. Nothing more." | deceitful | education_intrigue | A crafted cover story built from what the heir actually saw: an intriguer's precise lie, not a reflexive one. It is still a lie, and the 50/50 believed/doubted toasts stand. | `.desc` (single) |
| `eotg_fracture.006.e` | "Bring [eotg_warrant_vassal.GetHerHim] to my table." | gregarious | education_diplomacy | Diplomatic skill: I talk the filer round at table (the duel is diplomacy). Negotiation, not conviviality. | `.desc_faction`, `.desc_discontent`, `.desc_circulated` |
| `eotg_fracture.007.d` | "Sell them." | greedy | education_stewardship | A steward's trade: I price the plans and find the buyer. Competence rather than appetite. | `.desc` |
| `eotg_fracture.008.d` | "Say [eotg_named.GetHerHis] real name until it sticks." | compassionate | education_diplomacy | Patient, skilled repair of the moment with the person: I talk them back to their name. It must fit both the heir and the spouse. | `.desc_dead_name`, `.desc_designation` (the designation path has no dead name to correct) |
| `eotg_fracture.009.e` | "Log every minute from now on." | diligent | education_stewardship | Ledger discipline: a minute-by-minute account of my own day, kept as a steward keeps books. The current text already fits. Light touch or none. | `.desc`, `.desc_misled` (misled path: the minutes say I sat in council; the log must not contradict that framing) |
| `eotg_fracture.010.d` | "Bless the glass." | zealous | education_learning | I know the rite of blessing and say it correctly. Learned practice, not fervour. No invocation of a power acting on the glass (lore §8 item 6). | `.desc` + `.desc_saw_mirror` + all four `[voice]` branches |
| `eotg_fracture.011.e` | "You heard nothing." | deceitful | education_intrigue | An intriguer leaning on a witness until they agree they saw nothing. Practised pressure, not a fib. | `.desc_witness` only (the option is hidden on the misled/no-witness path) |
| `eotg_fracture.012.e` | "An impostor." | paranoid | education_intrigue | A spymaster's reflex: treat the face as a cover and question it as one. It is still wrong (fear opinion, risk +5). | `.desc` |
| `eotg_fracture.013.d` | "Stake the treasury on it." | eccentric | education_stewardship (gold gate kept) | A steward's calculated stake placed through the treasury's own instruments on the forecast. Not a whim. | `.desc` |
| `eotg_fracture.014.e` | "Then I am wrong. Help me." | humble | education_learning | Method: I doubt the instrument and test the overlay against the wall's plans, out loud and with help. Scholar's self-correction rather than humility. | `.desc` |
| `eotg_fracture.015.d` | "Send it with a note: "I don't remember writing this."" | honest | education_diplomacy | A skilful covering note that disarms whatever the letter says. Candour used as diplomacy. Must work for all three letter kinds, including the misled path where the letter I read is not the one I send. | `.desc_confession`, `.desc_threat`, `.desc_devotion` (any can be the misled one) |
| `eotg_fracture.016.e` | "Pay [eotg_victim.GetHerHis] family restitution." | just | tier ≥ duchy (victim + gold gates kept) | Lordly justice: I set and pay a blood-price from the seat, by right. | `.desc` (the option needs a victim, so `.desc_own` never shows with it) |
| `eotg_fracture.017.e` | "No device speaks for me." | zealous | tier ≥ duchy | Sovereign standing: nothing speaks in my name. It refuses on authority, not faith. The current text already fits, so a light touch or none. It still carries the hidden 15% override. | `.desc` + all four `[voice]` branches (at voice 4 "speaks for me" must still parse) |
| `eotg_fracture.018.d` | "I refuse to wake up as someone else." | stubborn | education_martial | Drilled discipline: I hold the position under fire by technique, like a soldier holding a line. Not mere refusal. | `.desc` |
| `eotg_fracture.019.d` | "[eotg_accused.GetHerHis\|U] family too." | paranoid | tier ≥ duchy | A lord's order to take the whole house into the cells. The authority to do it is the point. | `.desc` |
| `eotg_fracture.023.e` | "Wait for the scouts." | calm | education_martial (peace only, kept) | A commander's discipline: hold the muster until the scouts report. The current text already fits. Light touch or none. | `.desc_peace` only |
| `eotg_fracture.024.d` | "Sit with [eotg_changed.GetHerHim]. We both know what this is." | compassionate | education_learning | Physician's recognition: I know these symptoms in another implant and talk them through it. Knowledge first, warmth second. "We" is fine here (two people, not the implant's plural), but check it against §12.1 rule 7. | `.desc` |
| `eotg_fracture.025.d` | "[eotg_keeper.GetSheHe\|U] has planned this for months." | paranoid | tier ≥ duchy | Authority: I order my guards to take the keeper into custody. The effect is the hold, so the text must say I order it, not only that I suspect it. | `.desc` |
| `eotg_fracture.027.c` | "Fight it." | brave | education_martial | Fighting the cascade channel by channel, as a drilled soldier fights a line. **W7 set piece:** option text only. The addendum lists `.a`–`.d` as unchanged, so this re-axe is the one B5 text change W7 inherits. | `.desc` + `.desc_premonition` + four `[voice]` branches |

## Re-gated but text locked (no change)

| Key | Old gate | New gate | Note |
|---|---|---|---|
| `eotg_fracture.022.d` "We are more than any one ruler." | arrogant | tier ≥ duchy | §13.3 L-2: "the options are unchanged". The line already reads as the majestic plural, so no edit. Flag to lore-keeper if they disagree. |

## Desc path assumptions changed

- **fracture.004:** a new static `lower_center_portrait` shows a witness courtier (`scope:eotg_witness`) who is neither hurt nor jailed. W7's new `.desc` text ("The guards will not look at me...") must not contradict an onlooker in frame. No key change.
- No other desc branch conditions changed. The re-axed options keep their existing extra guards (victim, gold, peace, witness).

## Kept personality options (no text change; stress row added, §13.1 step 5)

`007.e` generous, `009.d` paranoid, `012.d` trusting, `013.e` patient, `016.d` callous,
`019.e` trusting, `022.e` humble, `024.e` paranoid, `026.e` zealous, `027.d` stubborn,
`029.b` humble.
