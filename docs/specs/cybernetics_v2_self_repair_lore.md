# Lore review: cybernetics_v2_self_repair.md (binding for script and loc)

**eotg-lore-keeper, 2026-10-04.** Approved, with seven must-fix items (S1–S7). The mechanics hold:
- the innovation gates the hardware;
- nothing has it at 866;
- it is not a programme;
- no named players;
- Neurofractured, Seamless and proc.004 are untouched.

## Rulings
- **Q1.** "Self-repairing" (ERRATA) stands, and "replicating" is banned. The procedures-lore ceiling "no self-replicating repair" still binds. **A self-repairing unit adjusts, re-seats, reroutes and records. It never makes a part.** Worn or lost parts are replaced by hand, and proc.004 is unchanged. (The ERRATA sub-bullet was refined to match, 2026-10-04.)
- **Q3. Register.** Mundane machinery, and say nothing about arcana either way. "Grows, learns, wants, decides" are banned with the hardware as the subject. The passive "How it goes is decided on the table" is allowed.
- **Q4.** A culture reaching it before 975 is alternate history, not a contradiction, provided nothing has it on 866.1.1 (S5). The loc is date-free and culture-agnostic.
- **Human design decisions (2026-10-04):**
  - gating option **B** (early medieval era);
  - price `massive_gold_value` × 2;
  - **no cap** on stacked Overclocked relief (self-repair + firmware + Technician stack fully; the realm spec keeps its −6).
- **U1.** Culture gate accepted: the scholars belong to a culture (ERRATA now says "a culture's scholars"). No liege read.
- **U2.** Removing the modifier at Total Integration stands, as specced.
- **U3.** Procedures-lore N1 rationale restated: "Self-repairing machinery does not exist at 866; it is researchable, and once researched it still makes no part. proc.004 is ordered parts either way."

## Must-fix
- **S1.** It never makes or orders a part. §4.3 adds: "It cannot make a part, and it does not order one. A worn part is still replaced by hand." "Logs the part it will need replaced" stays.
  - Banned with the hardware as subject: fabricate, print, build/make (a part), order, requisition, send for, copy, replicate.
- **S2.** Its log is read at the panel, by hands. Never alert, message, notifies, tells you, reports to you, or an overlay readout.
- **S3.** The innovation's `_desc` and `_custom` are descriptive with no possessive, so they read true before research. "Our scholars" only in decision and event text. Never "the realm's", court's or ruler's scholars.
- **S4.** Date-free. Never:
  - first, "the first to", "before anyone", "ahead of its time", "only we", secret;
  - "new age", "new era", renaissance, "golden age", "rogue scholars", "from across the galaxy";
  - Council of Innovation, Technarch, technomagic, Core Purity Doctrine.
  - DoD item 8 grep: `gnom|technocra|technarch|renaissance|golden age|council of innovation|technomag|975|replicat|nanite|swarm|before anyone|ahead of its time|the first to`.
- **S5.** Nothing at 866 has it. No `history/cultures` grant, no bookmark or history character carries the modifier.
  - DoD item 2: `grep -rn "eotg_innovation_self_repairing_machinery\|eotg_mod_aug_self_repair" history common/bookmarks` returns nothing.
  - Note for the cartographer at Gate 1 (CB-36).
- **S6.** "measures its own wear", not "notices" or "senses". Banned with the hardware as subject: heals, feels, knows, alive, living, instinct, organic.
- **S7.** The hidden rule covers promises. Loc may say calibration holds longer and the hardware stays in tolerance. Never safer, protects, prevents, "slows the cascade", fracture, or "a longer life".

## Names
- Innovation: **"Self-Repairing Machinery"**
- Decision: **"Commission Self-Repairing Hardware"**
- Modifier: **"Self-Repairing Hardware"**
- proc.005: **"Within Tolerance"**

## Renderings
The localizer may polish these. No numbers, and no "risk", "odds" or "chance". Appended lines start with `\n\n`.

**Innovation**
- `eotg_innovation_self_repairing_machinery` "Self-Repairing Machinery"
- `_desc` "Mechanisms that measure their own wear and correct it: tolerances re-zeroed, a loose contact re-seated, a failed path routed around, and the worn part recorded for the next pair of hands. They cannot make a part. They only put off the day one is needed."
- `_custom` "Augmented characters of this culture can have self-repairing hardware fitted."

**Decision**
- `eotg_decision_aug_self_repair` "Commission Self-Repairing Hardware"
- `_desc` "Our scholars have built machinery that keeps itself in tolerance. Fitted into the implants you already carry, it would mean calibrating them less often. The work is deep, and the price is ruinous."
- `_tooltip` "Have your implants refitted with self-repairing hardware. Choose who performs it."
- `_confirm` "Arrange the refit."
- `_selection_tt` "Have your implants refitted with hardware that keeps itself in tolerance."
- `_no_provider_tt` "No clinic will do this work for you here, and there is no one at your court who can."

**Modifier**
- `eotg_mod_aug_self_repair` "Self-Repairing Hardware"
- `_desc` "The implants measure their own wear and correct it, and hold their calibration longer. They keep themselves in tolerance. You are another matter."

**proc.005 "Within Tolerance"**
- `.t` "Within Tolerance"
- `.desc` "Our scholars' hardware is ready for fitting: units that measure their own wear and correct it between calibrations. It keeps the machinery true. It does nothing for the one wearing it. The work goes deep into what you already carry, and the price is ruinous."
- `.desc_overclocked` "\n\nThe overclocked units wear fastest of all. This is the hardware the refit was made for."
- `.desc_surgeon` "\n\nSomeone at your court knows this hardware well enough to fit it, for less than the clinic asks."
- Options:
  - `.a` "The clinic."
  - `.b` "My own physician." (the technician variant reuses `eotg_aug_opt_technician`)
  - `.c` "Not yet."
- `.tt` "The refit begins. How it goes is decided on the table."

**proc.002 addition**
- `eotg_aug_proc.002.desc_refit` "The new hardware has been in for some weeks now. Read at the panel, its record already shows the first fault it found and corrected."
