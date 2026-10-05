# Cybernetics v2: tier options, lore pass record

**Reviewer:** eotg-lore-keeper, 2026-10-05, read-only pass on `cybernetics_v2_tier_options.md` §7. Recorded here by the orchestrator so the binding texts live in the repo.

**Verdict:** no rejects, and no canon contradiction in any option concept. The renderings below override §7.

## Binding renderings (must change)
| Key | Rendering | Reason |
|---|---|---|
| `eotg_aug_act.001.f` | "Units above tolerance are barred. The rest may compete." | "Ride" brought the horse back (index §5 item 6). |
| `eotg_aug_tier2.014.d` | "Read their faces through the overlay while they haggle." | Reading a vendor's margins implies remote or networked reach, above the tech ceiling (procedures lore (c)). The overlay reads the person in front of you. |
| `eotg_aug_tier2.016.d` | "Recalibrate the response curves by hand, from my own logs." | "Rebuild the parameters from my logs" read as restoring the mind from a backup, which the ceiling bans. |
| `eotg_aug_act.002.f` | "Take the throttle off the reflexes." | Index §5 item 8: "answers" becomes "replies" or "responds". Also, letting the reflexes answer gave the hardware the voice's agency in a line from before the voice. |

## Adopted rewordings
- `eotg_aug_act.004.g`: "It is only a first fitting. Let them feel it work." The implant is fitted in the wrist and cannot be handed round.
- `eotg_aug_nr.003.g`: "Maintenance scheduled. Fault logged." It ends on the thing logged.

## Brief corrections
- **`eotg_aug_act.004.f`** stays as "Let it finish my sentences." Its brief: your mouth, your words, your phrasing, a half-second ahead of you. No second voice is ever heard, the guests hear only you, and the model never addresses them as itself. Any later text built on this row must not show the model speaking to guests.
- **Strike §5.2 per-row note 2** ("the ban on 'answers' does not apply"). Index §5 item 8 applies regardless.

## Seamless resource
- `eotg_aug_residue` as the Seamless signature is canon-consistent (procedures lore (a)). Seamless rows carry no stress.
- **Pacing (orchestrator ruling).** Residue only runs 0–3 and the host events recur, so draining it would make Flicker (end.042) and `desc_residue_high` unreachable. The ruling:
  - Rows that move another character's risk do not also lower residue. These are act.001.f and nr.003.g.
  - The residue-only row, act.003.g, is gated on `var:eotg_aug_residue >= 1`.

## Tech ceiling
After the rewordings above, none of the 16 concepts implies self-repair, remote kill, state programmes, upload or networking. Overlays, unthrottled reflexes, local thermal reading and personal diagnostic logs are all already established in shipped loc.
