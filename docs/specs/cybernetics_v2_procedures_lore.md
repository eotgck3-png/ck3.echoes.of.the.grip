# Lore review: cybernetics_v2_procedures.md (binding for script and loc)

**eotg-lore-keeper, 2026-10-04.** Approved, with five must-fix items (N1–N5). Checked against:
- the SETTING LORE ERRATA (SOURCE PRECEDENCE, YU, LAW AT 866);
- `docs/lore/REVIEW_866.md`;
- `docs/specs/cybernetics_v2.md` §5.

No never-name violations, no remote-kill, no state programmes. The neutral clinic wording stands: under LAW AT 866, licensing is local and unnamed.

## Must-fix
- **N1. proc.004 is over the 866 tech level.** Self-repairing machinery belongs to the Gnomish Mechanized Renaissance, 975 (`Third era Nations.md:4241-4242`).
  - Keep the mechanic: no roll, no gold, no risk.
  - Change the fiction: the system orders the part and books the technicians itself, and the cost was already budgeted.
  - **Retitle it "A Part Replaced".**
- **N2. end.042.** The motion must not reach for a person (that would be longing). It's a routine that fires at a scheduled hour, then is logged as redundant and pruned.
- **N3. end.040 `desc_residue_high`.** No hesitation over mercy. The line is kept by a standing instruction older than the integration, then flagged and cut.
- **N4. end.041 `.c.stays`.** Write it from the councillor's perception ("They believe someone asked it"). Narration never says the ruler felt, meant or wanted anything.
- **N5. heir.004 with a Seamless owner.**
  - Gate `eotg_aug_heir.004.desc_silent` and `eotg_aug_heir.004.desc_premonition` with `NOT = { has_trait = eotg_total_integration }`.
  - Add the appended `eotg_aug_heir.004.desc_seamless`: "\n\nThey address the chair, not you. They have understood there is no difference left to make."
  - This is a desc-only change, not a new beat.
- **Not lore:** `eotg_decision_remove_implants_tooltip` already exists (loc line 1747), so it's a REVISED key, not a new one. That makes ~101 new keys and 4 revised.

## Rulings
- **(a) Residue: approved, with a register constraint.**
  - **Allowed:** motor patterns, facial reflexes, standing instructions, schedules, and the court's perception of them.
  - **Never:** preference, hesitation, longing, regret, felt recognition, memory as an experience, a "spark", soul, humanity or "the old self", or anything returning or growing.
  - **Every residue line ends with the thing logged, filed or pruned.**
- **(b) Titles:** all approved except proc.004, which becomes *A Part Replaced*.
- **(c) Register.**
  - **Seamless:** the logging or report voice. Short declaratives, often passive. "You" may be the subject of a bodily action or a decision outcome, never of a feeling. The court may feel things; the ruler may not.
  - **Tech ceiling:** no upload, backup, copy or transfer of the mind; no datavault or secretariat; the implant is not networked into the treasury or the realm's records; no self-replicating repair.
  - **Phantom Static:** internal and bodily only. No signal arriving, no "someone/something", no whisper or voice. The full §5.2 banned list applies.
- **(d) Back-street Excision: `PHYSICIAN = no` is upheld.** Option e's text and tooltip never mention the physician.
- **Discovery:** keep "word has got out". No arrest, and no authority.

## Renderings
The localizer may polish these. Rules:
- No numbers, and no "risk", "odds" or "chance".
- Appended lines start with `\n\n`.
- All proc.002 outcome lines are appended after the opener.

**proc.001**
- .t "Who Takes It Out?"
- .desc "The decision is made. What is left is whose hands do the work. The clinic has a table, a team and a price. Cheaper hands can be found, and they will not ask to see a record."
- .desc_partial "\n\nThe deeper work comes out. The first implants stay where they are."
- .desc_downgrade "\n\nThe overclock comes off. The rest stays."
- .desc_full "\n\nAll of it: the last of the hardware, and the cabling threaded through you to reach it."
- .desc_physician "\n\nYour physician knows this hardware, and has offered to do the work for less."
- .a "The clinic."
- .b "My own physician."
- .c "Someone cheaper."
- .d "Not yet."
- .e "I'll guide their hands myself."
- .f "Every piece. I want none of it left."
- .tt "The work begins. How it goes is decided on the table."

**proc.002**
- .t "After the Procedure"
- .desc_upgrade "The new hardware has been in for some weeks now."
- .desc_removal "The hardware has been out for some weeks now."
- .desc_repair "The repair has had some weeks to settle."
- .a "It is done."
- .a_grim "It will have to do."
- .b "Fetch a physician."
- .c "Sweat it out."

**`eotg_aug_proc.outcome_*`** (all appended)
- clean "\n\nNothing hurts that should not. The readings are steady." This also serves `flaw`, so it must hint at nothing.
- excellent "\n\nIt took better than anyone had a right to expect. The incision is already a fine line."
- infection "\n\nThe incision is hot and swollen, and a fever is building under it."
- complication "\n\nThe body is fighting the new hardware. The incision weeps and the readings stutter. The surgeon says it will hold. It will also hurt."
- fragments "\n\nThey missed some. Wire and splinters of casing are still in the tissue, and the body knows it before the scans do."
- repair_failed "\n\nThe repair did not take. The part sits where it was fitted and does nothing, and the injury is as it was."
- discovered "\n\nWord has got out. Someone saw the work, or the place it was done, or paid to know."
- maimed "\n\nSomething was cut on the table that was not hardware. The use of the limb has not come back."
- one_eyed "\n\nAn optic line was severed on the table. One eye has stayed dark."
- blind "\n\nThe optic interface failed on the table, and it took your sight with it. Nothing the surgeon tried brought it back."

**Install tooltip:** `eotg_aug_proc.install_tt` "How it took will be known when the incision heals."

**proc.003**
- .t "Spare Parts"
- .desc "A body does not recover from this kind of injury on its own. The hardware already in you has standard fittings, and replacements are in stock somewhere. What remains is who fits them, and for how much."
- .desc_wounded "\n\nThe wound is deep and has not closed. Grafted tissue and a support frame would have you upright in weeks."
- .desc_maimed "\n\nThe hand and arm are past saving. A frame and a sensor lattice could replace them."
- .desc_one_legged "\n\nThe leg is gone. An actuator limb would take the sockets your implants already use."
- .desc_one_eyed "\n\nThe eye is gone. An optical unit would close the gap."
- .desc_blind "\n\nThe sight is gone. The optical units exist, and the interface for them is already in you."
- .desc_disfigured "\n\nThe damage is to the face. Synthetic tissue over a new frame would rebuild it, close enough that few would know."
- .desc_fractured "\n\nNo clinic will touch it. Their technicians read the diagnostics on your hardware and decline. Others are less particular."
- .desc_physician "\n\nYour physician has looked at the injury and the hardware both, and could do the fitting for less."
- .a "The clinic."
- .b "My own physician."
- .c "The back streets."
- .d "Live with it."
- .e "Hand me the tools."
- .f "Improve it while you're in there."
- .tt "The fitting begins. How well it takes is decided on the table."

**proc.004 (N1)**
- .t "A Part Replaced"
- .desc "The injury is logged within the hour. Replacement parts are ordered against the existing fittings, the technicians are scheduled, and the work is finished within the month. The cost was already in the budget. Nothing else changes."
- .desc_residue "\n\nWhen it happened, the face made the old expression of pain. The expression was logged. It has not recurred."
- .a "Continue."

**proc.020**
- .t "Phantom Static"
- .desc "A reflex reaches for an overlay that is not there. You look at a face, and no name surfaces beside it. You start down the stairs, and nothing counts them. The half-second early is gone, and the body has not finished learning that."
- .desc_removed "\n\nYou had it taken out, and you would do it again. The reflex does not care."
- .desc_excised "\n\nThe surgeons took all of it, and some of what had grown around it. The reflex reaches into the gap."
- .desc_rejected "\n\nYour body threw the hardware out. It still reaches for what it threw out."
- .desc_fragments "\n\nNow and then the fragments left in catch: a sting along the old line of the cabling, then nothing."
- .a "It will fade."
- .b "See my physician."
- .c "Put it back."
- .d "Replace what was lost."
- .e "As I was made."
- .c.tt "Send word for an installation. Whoever replies will name their price."

**init.011 / init.006 additions**
- init.011.desc_maimed "Weeks on, the incision has closed. Something was cut on the table that should not have been, and the arm has not worked since."
- init.011.desc_one_eyed "Weeks on, the incision has closed. An optic line was cut in the work, and one eye has stayed dark."
- init.011.desc_blind "Weeks on, the incision has closed. The optic interface failed on the table, and your sight went with it."
- init.006.desc_former "\n\nThe surgeons who took the hardware out took this with it."

**tier1, tier2 and end.001 additions**
- tier1.002.f and tier2.003.f "My own physician."
- tier1.002.g and tier2.003.g "Someone cheaper."
- tier1.022.desc_rejection "\n\nThe body is fighting the new hardware. The incision weeps, a fever comes and goes, and the readings will not settle. It will hold. It will also hurt for a while."
- end.001.e "Not their table. Somewhere cheaper."

**end.040**
- .t "The Ledger Balances"
- .desc "The treasury accounts are read in one sitting, end to end. Every line is costed against what it returns. The surplus is found, and it is larger than the treasury staff projected."
- .desc_residue_high (N3) "\n\nOne line is carried forward a cycle longer than the rest: the pardons budget, kept by a standing instruction older than the integration. Then it is flagged as unjustified, like the others."
- .desc_residue_low "\n\nNothing is carried forward out of habit. There is no habit left to carry it."
- .a "Bank the surplus."
- .b "Cut what does not pay."
- .c "Return it to the realm."
- .d "Rebalance every ledger."

**end.041**
- .t "A Resignation"
- .desc "[eotg_resigner.GetName] asks to be released from the council. Their work has been reviewed, and it is correct. Every recommendation was taken. That is the problem, they say: they have been reporting to a room with no one in it."
- .desc_residue_high "\n\nHalfway through, your head tilts the way it used to when you were listening. They stop, look at you, and start again more slowly."
- .desc_residue_low "\n\nThey finish. Nothing in your face has moved, and they did not expect it to."
- .a "Accept it."
- .b "Order them to stay."
- .c "Ask them why."
- .c.stays (N4) "[eotg_resigner.GetName] hears the old question in the old words, and stays. They believe someone asked it."
- .c.leaves "The question is put correctly. [eotg_resigner.GetName] hears no one asking it, and goes."

**end.042 (N2)**
- .t "A Flicker"
- .desc "At the hour the court once gathered, the body turns toward the door and a hand lifts in greeting. No one is there to be greeted. The motion is logged as redundant and pruned."
- .desc_last "\n\nIt does not happen again."
- .a "Continue." This is a separate key from end.010.a.

**Modifier**
- eotg_mod_aug_fragments "Implant Fragments"
- _desc "Wire and splinters of casing left in the tissue by a careless removal. They ache, and they slow the healing."

**Decision tooltips** (all revised; none is new)
- partial "Integration falls back to Augmented. Choose who performs it."
- overclock_regression "Integration falls to Enhanced. Some of the damage remains. Choose who performs it."
- remove_implants "Have every implant taken out. Choose who performs it."
- consult_physician_selection_tt "Have your physician look over the implants, or what a removal left behind."
- Optional: a guarded alternative to "The static quiets." for former characters: "The fragments come out."
