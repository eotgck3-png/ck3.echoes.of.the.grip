# B6 (initiation): localizer worklist for the W5 re-gating

Source: `events/eotg_augmentation_initiation.txt`, re-gated under `docs/specs/event_quality_v1.md` §13.1 (2026-10-09, eotg-scripter).
Loc file: `localization/english/eotg_augmentation_l_english.yml`.

Every key below **stays the same**; only the text changes so the option reads as its new axis (§13.1 step 7). The effects are unchanged. Apply the §12.1 voice rules (first person, implant-agency verbs) as for the rest of the B6 W1 pass. Check each new line against **every** desc variant listed (B1 lesson 7).

No W6 (portrait) change adds or moves a loc key. No desc path changed in this batch.

## Re-axed options (12)

| Key | Old gate | New gate | Current text | What the new text must convey | Desc variants to check |
|---|---|---|---|---|---|
| `eotg_aug_init.001.d` | craven | education_martial | "Anything, so I never feel that again." | A soldier's read: I know what the next wound costs, so armour me past it; more hardware than this wound needs (risk 5). Fear can stay as subtext, but the voice is competence, not panic. | `.desc` only |
| `eotg_aug_init.001.e` | cynical | education_diplomacy | "Flesh was only ever a first draft." | Rhetoric: a line said aloud for the camp to repeat (prestige +50, piety −50 for saying it). The phrase can survive if it reads as a deliberate speech. | `.desc` only |
| `eotg_aug_init.003.d` | arrogant | tier ≥ duchy | "I will not grow old in front of them." | Authority: the seat cannot be seen to weaken before the court or vassals; more hardware for it (prestige +100, risk 5). "Them" should read as the court or vassals. | `.desc` only |
| `eotg_aug_init.004.d` | brave | tier ≥ duchy | "I will finish this war as I am." | Authority: refusing in front of the host, as its commander, and leading it to the end unaltered (piety +100, prestige +75). | `.desc` only |
| `eotg_aug_init.005.e` | paranoid | education_intrigue | "What did they put inside you?" | Tradecraft: questioning the peer about the hardware's provenance until it comes out; refusal and watching (intrigue lesson, peer unease). Suspicion is now method, not fear. | `.desc` only |
| `eotg_aug_init.006.e` | cynical | education_martial | "Make it better than the original." | A fighter's specification: build the limb for the field, not to match the old one (prowess lesson, risk 5). Never "cure" (lore M6: hardware compensates). | `.desc` + every loss line (`desc_blind`, `desc_one_legged`, `desc_maimed`, `desc_one_eyed`), `desc_former`. Not shown with `desc_congenital` (e needs a physical loss). "Limb" is wrong for blind / one-eyed: keep it loss-neutral or name "it". |
| `eotg_aug_init.007.e` | ambitious | education_learning | "Run it at full current." | A scholar's read of the bridge's rating: I know how far past the rated current it can be pushed (risk 40; two lessons on success). | `.desc` only |
| `eotg_aug_init.010.c` | deceitful | education_intrigue | "Do it, and keep my name out of it." | Tradecraft: arranging a procedure that cannot be traced (discreet flag: no discovered outcome later). Current text already nearly fits; make the arranging explicit. | `.desc` only |
| `eotg_aug_init.013.d` | greedy | education_stewardship | "Sell them to the highest bidder, and let it be known." | A steward's open auction for the best price (gold x1.5, prestige −50 for doing it publicly). | `.desc` and `.desc_fractured`: with the fractured line the hardware is known to have broken the parent; the auction text must not claim it is sound. |
| `eotg_aug_init.014.d` | compassionate | education_diplomacy | "Sit with [eotg_sick_child.GetHerHim] through every hour of it." | A diplomat's patience: keeping the frightened child talking through the procedure (child opinion +, as a). Same precedent as tier2.002.d in B2. Keep the `GetHerHim` reference. | `.desc` only |
| `eotg_aug_init.016.e` | arrogant | tier ≥ duchy | "They will regret it." | Authority: answering the shame with fear of the seat (dread +10, risk 5). | `.desc` (rival named) **and** `.desc_no_rival` (no rival; "they" = the people who saw). Text must work in both. |
| `eotg_aug_init.017.e` | paranoid | education_intrigue | "And who paid you to suggest it?" | A spymaster's question: who profits from this proposal (intrigue lesson, physician unease). | `.desc` only (hidden when the ruler is the physician, `desc_self`). |

## Kept personality gates whose text is unchanged

001.c, 002.d, 003.e, 004.e, 005.d, 006.d, 007.d, 008.c, 009.d, 010.d, 011.f, 012.b, 013.e, 014.e, 015.d, 016.d, 017.d, 019.d, 020.d. These keep the gate. Some gained a stress row or trait icon (001.c: content/humble icons and rows; 002.d greedy; 017.d trusting; 020.d callous), but none needs new text.

## Pre-existing issue found in the desc-variant check (not caused by B6)

- `eotg_aug_init.017.d` "I trust your hands." is shown under `desc_self` as well (its trigger does not exclude `scope:eotg_physician = root`). With the ruler as their own physician, "your hands" has no addressee. Options: (a) the localizer makes the line address-neutral, or (b) eotg-scripter adds a `name = { trigger = { scope:eotg_physician = root } text = eotg_aug_init.017.d_self }` variant and the localizer writes that key. This batch made no change. The orchestrator decides.
