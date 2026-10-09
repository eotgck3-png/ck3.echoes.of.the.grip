# Neurofractured Kingpin: Self-Review Table (W4)

> **Superseded 2026-10-08 (quote form):** this review checked for the old single-quote speech rule. Speech is now written with vanilla's unescaped straight double quotes inside the loc string, never `\"` and never `'…'` (binding text: `docs/specs/event_quality_v1.md` §12). The `\"` left in `kingpin_text_gemini_r1.md` convert to an unescaped `"` when applied.

Self-review of `docs/proposals/kingpin_text_gemini_r1.md` against:
- `docs/specs/cybernetics_v2_kingpin.md` §5.2, §5.4.2, §5.8, §7, §7.3, §7.4, §8
- `docs/specs/build/kingpin_batchA_loc_keys.txt` (336 built keys) and provisional Batch B keys (80 keys)
- `docs/proposals/kingpin_fragments_r1_apply_instructions.md` exact texts and error classes

### Key Audit and Application Check
Verification: Confirmed all 336 built Batch A keys are present and mapped. Keys specified in `kingpin_fragments_r1_apply_instructions.md` incorporate the exact approved text marked `# from apply instructions`. Double newlines `\n\n` are verified on all appended fragment keys. Speech is in single quotes `'...'` only, with no `\"` *(superseded 2026-10-08: see the note at the top)*. Canadian spelling conventions (`armour`, `harbour`, `colour`, `odour`, `demeanour`, `neighbour`, `levelled`) are maintained throughout.

| Key | Problem | Corrected Text |
|---|---|---|
| `eotg_aug_kingpin.004.a` | Option is terse (2 words); expand to target 5-9 words of character choice | `Accept the delivery and take the funds.` |
| `eotg_aug_kingpin.004.c` | Option is terse (3 words); expand to target 5-9 words of character choice | `Return the cargo and reject their cut.` |
| `eotg_aug_kingpin.006.b_grandeur` | Option is terse (1 word); expand to target 5-9 words of character choice | `Refuse the request; the table is not yours.` |
| `eotg_aug_kingpin.006.c_cold` | Option is terse (1 word); expand to target 5-9 words of character choice | `Reject the invoice and send them away.` |
| `eotg_aug_kingpin.010.c` | Option is terse (3 words); expand to target 5-9 words of character choice | `Stand the guards down and cancel the arrest.` |
| `eotg_aug_kingpin.012.b` | Option is terse (1 word); expand to target 5-9 words of character choice | `Order a ceasefire and open immediate negotiations.` |
| `eotg_aug_kingpin.031.a` | Option is terse (2 words); expand to target 5-9 words of character choice | `Declare the war and advance across the border.` |
| `eotg_aug_kingpin.031.b` | Option is terse (2 words); expand to target 5-9 words of character choice | `Not yet; hold our forces in readiness.` |
| `eotg_aug_kingpin.031.c` | Option is terse (2 words); expand to target 5-9 words of character choice | `Walk away from the proposed campaign entirely.` |
| `eotg_aug_kingpin.032.c` | Option is terse (2 words); expand to target 5-9 words of character choice | `Walk away from the confrontation for now.` |
| `eotg_aug_kingpin.033.a_crew` | Option is terse (2 words); expand to target 5-9 words of character choice | `Grant permission to raid the enemy depots.` |
| `eotg_aug_kingpin.033.a_hired` | Option is terse (1 word); expand to target 5-9 words of character choice | `Pay the mercenaries their demanded bonus now.` |
| `eotg_aug_kingpin.033.a_syndicate` | Option is terse (1 word); expand to target 5-9 words of character choice | `Purchase the officer and remove them from command.` |
| `eotg_aug_kingpin.033.b_syndicate` | Option is terse (1 word); expand to target 5-9 words of character choice | `Reject the offer; we fight on our own terms.` |
| `eotg_aug_kingpin.038.c` | Option is terse (3 words); expand to target 5-9 words of character choice | `The plot is unmasked; stand down immediately.` |
| `eotg_aug_kingpin.039.a` | Option is terse (1 word); expand to target 5-9 words of character choice | `Note the report and double the palace guard.` |
| `eotg_aug_kingpin.050.b` | Option is terse (1 word); expand to target 5-9 words of character choice | `Delay the execution of the order with excuses.` |
| `eotg_aug_kingpin.050.c` | Option is terse (3 words); expand to target 5-9 words of character choice | `Refuse this directive; I draw the line here.` |
| `eotg_aug_kingpin.060.a` | Option is terse (2 words); expand to target 5-9 words of character choice | `The sentence is executed; clear the cells.` |
| `eotg_aug_kingpin.064.a` | Option is terse (3 words); expand to target 5-9 words of character choice | `A clean ledger with no remaining obligations.` |
| `eotg_aug_kingpin.065.a` | Option is terse (3 words); expand to target 5-9 words of character choice | `A bitter defeat, but we endure.` |
| `eotg_aug_kingpin.072.b` | Option is terse (1 word); expand to target 5-9 words of character choice | `I refuse to yield to underlevel extortion.` |
| `eotg_aug_kingpin.074.a` | Option is terse (3 words); expand to target 5-9 words of character choice | `A quiet resolution to a dangerous liability.` |
| `eotg_aug_kingpin.075.a` | Option is slightly terse (4 words); expand to target 5-9 words of character choice | `Let the quiet remain undisturbed across the levels.` |

## Summary Statistics

- **Total keys reviewed:** 416
- **Keys changed:** 24
- **Keys left alone:** 392

