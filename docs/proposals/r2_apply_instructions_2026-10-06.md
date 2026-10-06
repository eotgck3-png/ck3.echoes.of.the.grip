# Applying rewrite round 2: merged review instructions (2026-10-06)

**For:** eotg-localizer. **Source:** `cybernetics_events_rewrite_proposals_r2.md` (Gemini, round 2).
**Reviews merged here:** QA (rules and truth) and lore-keeper (canon and voice).
**Owner ruling:** apply round 2 with these edits; no round 3; "station" becomes the character's seat (below).

## Precedence
1. **Truth against the script (QA) is non-negotiable.** A line must be true on every path that shows it, and an
   option's text must match its effects.
2. **Canon and voice (lore) next.** Where the two reviews give different wording for the same key, write a line
   that satisfies BOTH: QA's facts in the lore-keeper's register.
3. **Revert to the SHIPPED line** wherever the lore-keeper says "revert", or where round 2 only padded a shipped
   option. Don't apply round 2's §4 "Dynamic substance" section at all: it is out of scope and misreads the events.

## Global rules
- **"station", "deck", "docking ring", "station logs", "station memory" and similar** must not assume a station.
  Use the character's seat: `[ROOT.Char.Custom('eotg_court_seat')]` (or `[x.Custom('eotg_court_seat')]` for
  another scope), which renders the mod's holding name in lowercase (bastion, port, sanctum, …; "court" as the
  fallback). Use the exact usage string the scripter reports, and check that it reads naturally ("your bastion").
  Where a seat isn't needed, use residence, court, quarters, the docks.
- **No singular they/their** for one person (proc.002.desc_salvaged, tier3.003.desc).
- **No body-location assumptions:** collar, armrest, cuff, fitted hands, seam in the side (where avoidable),
  surrounding muscle.
- **Banned in this content:**
  - "breach" (Neurofractured) and "whispers";
  - "mortal";
  - "registry", "magistrate", "citizen";
  - "diagnostic" used for reading people (diagnostics read hardware);
  - "title" where it isn't literally a title (use "name" or "place").
- **The implant forecasts and logs only.** It never regulates heart, pulse or body (tier2.001), never reads minds,
  and never "sees through their thoughts".
- **Break up round 2's new stock phrases:**
  - "your quarters" (6 events): keep at most 2;
  - "the court watches / looks upon": vary it;
  - "Nobody…" (the swapped crutch): vary it;
  - "the clinic fitter" opening every proc.002 variant: use "the fitter", since the provider varies;
  - "takes the chair": vary it;
  - fracture.020: at most two variants end on a spoken quote (false_arrested and false_executed).
- Keep Canadian spelling and the `\n\n` openers on the init.020 desc lines. Replace the one em dash
  (tier1.019.desc_recovered) with a comma.
- Keep `.t` titles as shipped (round 2 left them unchanged).

## Per event (QA's exact text where given; lore suggestions where QA had none)
- **tier1.019.** desc_dead: last sentence becomes "The file is closed, and the docket waits for your seal." No
  "fitted hands", no kin "at the threshold". desc_recovered: "The new housing shows at the seams: unpainted,
  scarred, and paid for on [eotg_copycat.GetHerHis] own account." desc_worse: trim the melodrama ("The sick-bay
  hatch stays shut, and the people who pass it have stopped pretending not to listen."). Keep `.a` and `.b`.
- **tier3.018.**
  - desc_attempt: "…struck in the transit corridor, and the blade found you before the guards did. The warning had
    sat in your log for months, marked unread." Nobody subdues the attacker.
  - desc_unknown: the last sentence becomes "When [eotg_conspirator.GetSheHe] attends audience,
    [eotg_conspirator.GetHerHis] face gives nothing away, and you cannot tell whether you uncovered an assassin or
    imagined one."
  - desc_true: "The inquiry is complete, and the implant was right. [eotg_conspirator.GetFirstName] was plotting,
    and the intercepted messages are in the record. The court says you saw it coming. You know only that the
    pattern matched."
  - desc_false: no "diagnostic", no "whispers". The last sentence becomes "The cleared logs are on file, and they
    are not kind to your judgment."
  - desc_quiet and the options are fine.
- **fracture.020.**
  - desc_false_arrested: "The inquiry is finished, and the cell is still sealed. [eotg_accused.GetName] was
    innocent; the flagged conspiracy was sensor noise. 'Your implant made a pattern out of me, and I am paying for
    it in the cells,' [eotg_accused.GetSheHe] says when told. The court has seen the cleared docket, and the
    injustice is plain."
  - desc_false_spared: "[eotg_accused.GetSheHe] tells you," with no magistrate. Use "record", never "station
    memory".
  - desc_true_spared: "…and [eotg_accused.GetSheHe] still walks free. Nothing came of it, and the record holds both
    facts." (no taunt)
  - desc_true: "record", not "registry"; "trust the next flag a little more", not "citizen".
  - desc_false_executed: drop "in the reclamation bay"; keep the kin quote.
  - `.c_spared` stays "It was right; I was not."
- **fracture.004.**
  - desc: keep the shipped irony and make it truthful. "There will be an official account. It will speak of a loss
    of control in the audience chamber. It will not resemble what the witnesses saw." Concrete overclocked-hardware
    detail (coolant hiss, hot casings, guards backing away) may follow, but must never recast your violence as an
    equipment fault. No "breach". "Terror" at most once across desc and desc_none.
  - desc_killed: "…whose hand it was" (killer = root).
  - desc_wounded: delete "the surge"; "[eotg_victim.GetName] survived, and remembers whose hand it was."
  - `.b`: revert to shipped.
  - `.e`: "fill the empty places".
- **init.012.** Apply, but trim the padding ("bloodied clamps…", "scent of antiseptic hangs thick", "the core is
  yours now") down to the spoken verdict.
- **proc.002.**
  - desc_repair_fault: "The faulty component was unsealed and reworked some weeks ago. The fitter runs a probe
    along the freshly closed housing and reads the result at the panel, and the tissue around the port is still
    stiff and tender to the touch."
  - desc_upgrade: "The upgraded component has been in place for some weeks now. A diagnostic lead runs from your
    interface port to the panel, and the readings scroll past as the fitter watches. The new housing carries more
    mass than the original, and the body is still adjusting to it."
  - desc_removal: "The component has been out for some weeks now. The fitter lifts the dressing to inspect the empty
    recess where the casing once sat. The severed leads have been capped, and the area is numb and strangely light
    without the heat it used to carry."
  - desc_repair: "The repair has had some weeks to settle. The fitter connects a test lead to the port and waits
    for the readout."
  - desc_salvaged: the last sentence becomes "Whoever closed the seam did it fast, and the cuts came close to things
    that were not hardware."
  - desc_refit: "The fitter…"; keep the self-repair fact.
  - Options: revert to shipped ("It is done." / "It will have to do." / "Sweat it out.").
- **retinue.002.** QA's desc: "Word has spread from the barracks, and [eotg_cand_a.GetFirstName] has come to ask
  for an implant. [eotg_cand_a.GetSheHe|U] makes the case cleanly: [eotg_cand_a.GetSheHe] is the strongest you
  have, and means to stay that way when others are fitted. [eotg_cand_a.GetSheHe|U] does not ask what it costs."
  Optional `.e`: "Both of you, at my expense and with care."
- **retinue.001.** QA's desc (no invented injury; "as others have been"; keep the barracks-envy beat).
- **heir.007.**
  - desc_dead: "along with the place".
  - desc_displaced: "…[eotg_heir.GetFirstName] does, and knows how the change was made.
    [eotg_heir.GetSheHe|U] sits where the last heir sat, and does not ask why." (no registry, no neck, no cliché)
  - `.b`: revert to "Then you know what I am."
- **tier2.018.** desc_estranged: "share quarters and a name". desc_reconciled: "…no longer flinches when your hand
  finds [eotg_aug_spouse.GetHerHis]." `.c` stays neutral.
- **end.030.**
  - "your title" becomes "your name".
  - The ending becomes "[ROOT.Char.GetPrimaryTitle.GetHeir.GetFirstName] stands in the doorway with the padded lock-bars and says
    softly, 'It is only a formality.' The restraints are a formality that no one believes is a formality."
  - No "palace".
- **init.020.** Apply. Optional: "weighing who is fit for the table". Optional `.d`: revert to shipped.
- **tier1.003.** desc: "…ultimately direct: [eotg_concerned_vassal.GetSheHe] wants to understand what
  [eotg_concerned_vassal.GetHerHis] liege has become, and whether the oaths [eotg_concerned_vassal.GetSheHe] swore
  still bind the same person." (no collar, no flicker, no "machine-bound"). `.c`: revert to "Show
  [eotg_concerned_vassal.GetHerHim] what I can do."
- **tier1.004.** desc first sentence: "[eotg_petitioning_knight.GetTitledFirstName] has watched what your implant
  does in boarding drills." (no "mortal", no superhero register)
- **tier3.002.** Apply. Optional `.e`: revert to "Cover the mirrors."
- **tier3.003.** desc: "Three days without sleep. The implant reports that the body does not need it. The readout
  may be right; that is the problem. The watch officer arriving for the shift change startles at your
  motionless posture…" (no singular they; no "station cargo manifests"). `.d`: "Then put the hours to use."
- **tier2.001.** No pulse or body regulation; use "…The implant had already logged it, filed it, and forecast your
  answer. The feeling came after, late, like a message routed the long way." `.d`: "Sit with my family until the
  feeling arrives." `.e`: revert to "Good."
- **tier1.001.** Apply; cut "with a sharp crack of metal".
- **patron.007.** Apply; cut "across the sector".
- **end.011.**
  - `.c`: "Seal the docks. No one leaves without my word."
  - desc_none: keep the shipped line plus the stake, "…the way people watch a machine that is working correctly,
    waiting for the moment it stops." (no "station")
  - desc_named: fine.


**Correction (2026-10-06):** characters have no `GetHeir` loc function; titles do. Use `[ROOT.Char.GetPrimaryTitle.GetHeir.GetFirstName]` (Tiger flagged the old form).
