# Echoes of the Grip: Cybernetics Events Rewrite Proposals (Round 2)

**Author:** Antigravity (Pair Programming Mod Localization Agent)
**Target File:** `localization/english/eotg_augmentation_l_english.yml`
**Event Scripts:** `events/eotg_augmentation_*.txt` (branch `v2-space-map`)
**Language / Standard:** Crusader Kings III English Localization (`l_english`), Canadian English Spelling

---

## 1. Summary of Changes from Round 1 (by Theme)

In response to project lore, canon, and QA feedback from `docs/proposals/gemini_rewrite_feedback_2026-10-06.md`, round 2 completely discards the medieval-fantasy framing of round 1 and rebuilds all 20 events directly from the current shipped text in `localization/english/eotg_augmentation_l_english.yml`:

- **Genre & Setting Correction (866 AG Galactic Setting):** Eliminated clockwork, fantasy feudalism, brass, gears, whirring, hot vapour, candles, parchment, castles, knights, and horses. Grounded the narrative entirely in the mod's actual space-faring canon: stations, ships, transit docks, airlocks, diagnostic panels, interface ports, leads, housings, and data slates.
- **Register & Canon Restored:** Re-established the clinical, intimate, and uneasy register of worn electronic hardware. Hardware only forecasts patterns (never supernatural prophecy); self-repairing hardware only maintains itself within tolerance (never the user's biological organs); and 'flesh' / 'other people' replace 'humanity'. Banned faith-specific assumptions ('holy blood', 'ungodly', 'prayer').
- **Script Consistency & Path Accuracy:** Verified every description against all event paths that invoke it. Wounded outcomes (`increase_wounds_effect`) in `aug_tier3.018` now show an actual landed blow rather than an unscripted parry; `fracture.004` base text accommodates zero-casualty paths; and invented gold costs, oaths of fealty, and fabricated kin (such as sisters) have been removed.
- **Full Script Support Integrated (§6 additions):**
  - `eotg_aug_init.020`: Scripted base desc plus three discrete candidate lines starting with `\n\n` for `eotg_cand_best`, `eotg_cand_any`, and `eotg_cand_courtier`.
  - `eotg_aug_tier2.001`: Implemented `desc_speaker` featuring `eotg_delay_speaker` alongside the standalone `desc` fallback.
  - `eotg_aug_end.011`: Implemented `desc_named` featuring `eotg_departed_courtier` alongside standalone `desc` and `desc_none`.
  - `eotg_aug_tier1.019`: Implemented option `.b` using `[eotg_copycat_recipient.GetFirstName]` to match the new opinion and gold effect.
- **Localization Formatting & Quality:** Enforced bare scope syntax (`[eotg_x.GetFirstName]`, never `[scope:...]`), gender-aware single-actor pronouns (`GetSheHe`, `GetHerHim`, `GetHerHis`), strict Canadian English spelling, 5–9 word options, and valid Paradox YAML lines without literal line breaks.

---

## 2. Event Rewrites (Current vs. Proposed & Rationale)

### `eotg_aug_tier1.019` — Copycat: Their Fate
- **Event Script:** `events/eotg_augmentation_tier1.txt`

#### Key: `eotg_aug_tier1.019.desc_dead`
**Current Shipped:**
> "[eotg_copycat.GetFirstName] died of the infection. The report from [ROOT.Char.Custom('eotg_aug_cl_company')] is short and clinical, and it says nothing you did not already know."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.019.desc_dead:0 "[eotg_copycat.GetFirstName] died of the infection. The report from [ROOT.Char.Custom('eotg_aug_cl_company')] is short and clinical, and says nothing you did not already know: the leads tore, the casing leaked, and the clinic incinerated the bedding. Now [eotg_copycat.GetHerHis] kin stand at the threshold of your quarters in silence, holding the sealed disposal docket and watching your quiet, fitted hands."
```
**Why:** Adds kin witnessing the return of the body without inventing gold costs, keeping the clinical clinic-record register.

#### Key: `eotg_aug_tier1.019.desc_worse`
**Current Shipped:**
> "[eotg_copycat.GetFirstName] is not recovering. The implant is failing in ways [ROOT.Char.Custom('eotg_aug_cl_company')] cannot name, and the readings keep drifting. [eotg_copycat.GetSheHe|U] is alive, and getting worse."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.019.desc_worse:0 "[eotg_copycat.GetFirstName] is not recovering. The implant is failing in ways [ROOT.Char.Custom('eotg_aug_cl_company')] cannot name, and the readings keep drifting off tolerance. [eotg_copycat.GetSheHe|U] is alive, and getting worse. Down in the sick-bay, [eotg_copycat.GetHerHis] breath catches against the whine of strained coils, and everyone passing through the corridor hears [eotg_copycat.GetHerHim] shivering behind the hatch."
```
**Why:** Grounds the failure in drifting sensor readings and coil whine heard in the corridor, raising court stakes.

#### Key: `eotg_aug_tier1.019.desc_recovered`
**Current Shipped:**
> "[eotg_copycat.GetFirstName] is on [eotg_copycat.GetHerHis] feet. The infection cleared, the implant settled, and [eotg_copycat.GetSheHe] has come to tell you so, with a gratitude that sits somewhere between thanks and debt."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.019.desc_recovered:0 "[eotg_copycat.GetFirstName] is on [eotg_copycat.GetHerHis] feet. The infection cleared, the implant settled into tolerance, and [eotg_copycat.GetSheHe] has come to your quarters to report so in person, with a gratitude that sits somewhere between thanks and debt. The new housing glints beneath [eotg_copycat.GetHerHis] cuff—unpainted, scarred at the seams, and fitted entirely on [eotg_copycat.GetHerHis] own account."
```
**Why:** Presents the copycat bearing their own scarred, unpainted casing without an invented oath, preserving clinical ambiguity.

#### Option Key: `eotg_aug_tier1.019.a`
**Current Shipped:**
> "I see."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.019.a:0 "The risk was always [eotg_copycat.GetHerHis] own."
```
**Why:** Provides a neutral, fatalistic 7-word reaction fitting all three outcomes (dead, worse, recovered).

#### Option Key: `eotg_aug_tier1.019.b`
**Current Shipped:**
> "Make it known you stood by them."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.019.b:0 "Send aid to [eotg_copycat_recipient.GetFirstName] from my own purse."
```
**Why:** Leverages the new script scope eotg_copycat_recipient and matches the gold transfer effect.


---

### `eotg_aug_tier3.018` — The Plot: The Truth
- **Event Script:** `events/eotg_augmentation_tier3.txt`

#### Key: `eotg_aug_tier3.018.desc_attempt`
**Current Shipped:**
> "The plot was real, and you ignored it. [eotg_conspirator.GetFirstName] struck at the hour the implant predicted, and the attempt came close. The warning is still in your log, unread, with a stamp from months ago."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.018.desc_attempt:0 "The plot was real, and you ignored it. [eotg_conspirator.GetFirstName] struck along the transit corridor, and the blade took a seam in your side before guards brought [eotg_conspirator.GetHerHim] down. The warning had sat logged in your diagnostic panel for months, filed as an anomaly. Your bandages soak through while the court watches you bleed, wondering why their augmented ruler failed to move."
```
**Why:** Depicts the knife attack landing and wounding you after you ignored the warning, matching the increase_wounds_effect.

#### Key: `eotg_aug_tier3.018.desc_unknown`
**Current Shipped:**
> "Your quiet inquiry ended without a conclusion. The evidence is thin either way, and you will have to live without knowing whether [eotg_conspirator.GetFirstName] meant you harm."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.018.desc_unknown:0 "Your quiet inquiry ended without a conclusion. The evidence is thin either way, and you will have to live without knowing whether [eotg_conspirator.GetFirstName] meant you harm. When [eotg_conspirator.GetSheHe] attends audience, [eotg_conspirator.GetHerHis] face gives nothing away, and the court watches both of you across the room, unsure whether their ruler uncovered an assassin or imagined one."
```
**Why:** Captures the lingering unease across the court when evidence remains inconclusive, avoiding supernatural framing.

#### Key: `eotg_aug_tier3.018.desc_quiet`
**Current Shipped:**
> "Months have passed and nothing has happened. [eotg_conspirator.GetFirstName] goes about [eotg_conspirator.GetHerHis] business, and the plot, if there was one, has lapsed. You will never know whether you were right to ignore it."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.018.desc_quiet:0 "Months pass. Nothing happens. [eotg_conspirator.GetFirstName] goes about [eotg_conspirator.GetHerHis] business across the station, and the plot, if there was one, has lapsed. You let the flagged warning sit unacted on, and you will never know whether your restraint preserved an innocent subject or gave an assassin time to reconsider."
```
**Why:** Expands the quiet outcome to show the unacted-on alert lapsing while the conspirator goes about daily station duties.

#### Key: `eotg_aug_tier3.018.desc_true`
**Current Shipped:**
> "The inquiry is complete, and the implant was right. [eotg_conspirator.GetFirstName] was plotting, and the evidence is clear and recorded. The machine saw it before you did."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.018.desc_true:0 "The inquiry is complete, and the implant was right. [eotg_conspirator.GetFirstName] was plotting, and the encrypted transmissions are logged in the court record. The diagnostic pattern matched reality long before mortal suspicion formed, and the court now looks upon your quiet stare with a chill, convinced the machine sees through their thoughts."
```
**Why:** Framed around encrypted transmissions matching the forecast pattern, working whether the conspirator is held or dead.

#### Key: `eotg_aug_tier3.018.desc_false`
**Current Shipped:**
> "The inquiry is complete, and the implant was wrong. There was no plot. Nothing [eotg_conspirator.GetFirstName] did could have been read as one by anyone but the implant."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.018.desc_false:0 "The inquiry is complete, and the implant was wrong. There was no plot. Nothing [eotg_conspirator.GetFirstName] did could have been read as treason by anyone but the diagnostic software, which elevated random corridor movements into a conspiracy. The court has reviewed the cleared logs, and the whispers in the gallery are not kind to your judgment."
```
**Why:** Explains the false alert as sensor software elevating random transit movements into a phantom conspiracy.

#### Option Key: `eotg_aug_tier3.018.a`
**Current Shipped:**
> "Release [eotg_conspirator.GetHerHim]."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.018.a:0 "Release [eotg_conspirator.GetHerHim]; the pattern was an error."
```
**Why:** Characterful 7-word release option acknowledging the diagnostic error for the false/imprisoned branch.

#### Option Key: `eotg_aug_tier3.018.b`
**Current Shipped:**
> "Keep [eotg_conspirator.GetHerHim]."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.018.b:0 "Keep [eotg_conspirator.GetHerHim] confined; the risk remains."
```
**Why:** Pragmatic 7-word retention option maintaining detention despite lack of proof.

#### Option Key: `eotg_aug_tier3.018.c`
**Current Shipped:**
> "Let it stand."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.018.c:0 "Let the record stand as written."
```
**Why:** Neutral fallback option fitting executed, unknown, and unheld outcomes.


---

### `eotg_fracture.020` — What the Record Shows
- **Event Script:** `events/eotg_augmentation_fracture.txt`

#### Key: `eotg_fracture.020.desc_true_spared`
**Current Shipped:**
> "The inquiry is finished. [eotg_accused.GetName] was what the flag said. The correspondence, the payments and the plan were all there, and you refused to act. Nothing came of it, and the file records both facts."
**Proposed Round 2:**
```yaml
 eotg_fracture.020.desc_true_spared:0 "The investigation log is closed. [eotg_accused.GetName] was exactly what the flag indicated: the routing slips, the encrypted transfers and the contact plan were all verified. You refused to act, and [eotg_accused.GetSheHe] walks free across the docking ring. 'Your hesitation made a mockery of your sensors,' [eotg_accused.GetSheHe] remarked to the guards, and the record holds both facts."
```
**Why:** Opens with closed investigation logs and gives the guilty party a bold spoken line questioning your hesitation.

#### Key: `eotg_fracture.020.desc_true`
**Current Shipped:**
> "The inquiry is finished. [eotg_accused.GetName] was exactly what the implant said: the correspondence, the payments, the plan. You were right. It is an odd comfort, to have been right by the machine's measure, and it will make you trust the next flag a little more."
**Proposed Round 2:**
```yaml
 eotg_fracture.020.desc_true:0 "The inquiry confirms the readout. [eotg_accused.GetName] was guilty as flagged: the intercepted transmissions, the payments, and the timetable are sealed in the registry. Your implant matched the pattern correctly. It is a cold reassurance to be vindicated by the machine's metric, and it will make you trust the next flagged citizen even more readily."
```
**Why:** Vindicates the implant's forecast across alive or dead paths while emphasizing your deepening reliance on the machine metric.

#### Key: `eotg_fracture.020.desc_false_executed`
**Current Shipped:**
> "The inquiry is finished. [eotg_accused.GetName] was innocent. The pattern was noise, and the confidence figure was a number the implant assigned itself. [eotg_accused.GetSheHe|U] is dead, and [eotg_accused.GetHerHis] family has read the report."
**Proposed Round 2:**
```yaml
 eotg_fracture.020.desc_false_executed:0 "The final audit is signed, and [eotg_accused.GetName] was innocent. The flagged threat was sensor noise, and the confidence score was a number the software assigned to its own jitter. [eotg_accused.GetSheHe|U] is dead in the reclamation bay, and [eotg_accused.GetHerHis] kin have seen the logs. 'You took a life to settle a circuit anomaly,' one of [eotg_accused.GetHerHis] kin stated before the council."
```
**Why:** Quotes the wronged family before the council and frames the fatal error as software assigning confidence to its own jitter.

#### Key: `eotg_fracture.020.desc_false_arrested`
**Current Shipped:**
> "The inquiry is finished. [eotg_accused.GetName] was innocent. The pattern was noise. [eotg_accused.GetSheHe|U] is still in the cells and has been told why, and the court has heard it too."
**Proposed Round 2:**
```yaml
 eotg_fracture.020.desc_false_arrested:0 "The hatch unseals in the detention block. [eotg_accused.GetName] was innocent; the flagged conspiracy was merely sensor noise. 'Your implant made a pattern out of me, and I paid for it in the cells,' [eotg_accused.GetSheHe] says, squinting against the light as guards step aside. The court has seen the cleared docket, and the injustice is plain."
```
**Why:** Gives the wronged accused a direct spoken grievance ('Your implant made a pattern out of me...') as the cell unseals.

#### Key: `eotg_fracture.020.desc_false_watched`
**Current Shipped:**
> "The inquiry is finished. [eotg_accused.GetName] was innocent. [eotg_accused.GetSheHe|U] was watched for months, and noticed. [eotg_accused.GetSheHe|U] is uneasy around you now, and so is everyone who used to tell [eotg_accused.GetHerHim] things."
**Proposed Round 2:**
```yaml
 eotg_fracture.020.desc_false_watched:0 "The surveillance files have closed with nothing to show. [eotg_accused.GetName] was innocent. [eotg_accused.GetSheHe|U] was tracked for months across the station, and noticed every watcher. 'I felt your cameras on my neck at every shift,' [eotg_accused.GetSheHe] tells you flatly in audience, and the courtiers who used to speak freely around [eotg_accused.GetHerHim] now stand well back."
```
**Why:** Shows the corrosive social impact of surveillance, with the accused confronting you directly over being tracked.

#### Key: `eotg_fracture.020.desc_false_spared`
**Current Shipped:**
> "The inquiry is finished. [eotg_accused.GetName] was innocent. You refused to act on the flag, and you were right to. The accusation was filed regardless, and the file still exists."
**Proposed Round 2:**
```yaml
 eotg_fracture.020.desc_false_spared:0 "The files are archived without charges. [eotg_accused.GetName] was innocent. You refused to act on the alert, and your restraint was justified. Yet the accusation remains stamped in the station memory, and [eotg_accused.GetSheHe] knows [eotg_accused.GetHerHis] name was logged. 'You stayed your hand,' [eotg_accused.GetSheHe] told the magistrate, 'but your system still marked me.'"
```
**Why:** Contrasts your justified restraint with the permanent stain left in station memory, quoting the accused.

#### Option Key: `eotg_fracture.020.a`
**Current Shipped:**
> "Release [eotg_accused.GetHerHim]. I was wrong."
**Proposed Round 2:**
```yaml
 eotg_fracture.020.a:0 "Release [eotg_accused.GetHerHim]; the alert was wrong."
```
**Why:** Direct 7-word admission of error releasing the wrongfully detained accused.

#### Option Key: `eotg_fracture.020.b`
**Current Shipped:**
> "I was right anyway."
**Proposed Round 2:**
```yaml
 eotg_fracture.020.b:0 "I was right to take precautions."
```
**Why:** Defiant 6-word justification for taking harsh precautions.

#### Option Key: `eotg_fracture.020.c`
**Current Shipped:**
> "As I knew."
**Proposed Round 2:**
```yaml
 eotg_fracture.020.c:0 "The evidence confirmed what I knew."
```
**Why:** Confident 6-word validation when the forecast was confirmed.

#### Option Key: `eotg_fracture.020.c_spared`
**Current Shipped:**
> "It was right. I was not."
**Proposed Round 2:**
```yaml
 eotg_fracture.020.c_spared:0 "It was right; I was not."
```
**Why:** Maintains binding meaning ('It was right; I was not.') when a real traitor was spared.

#### Option Key: `eotg_fracture.020.d`
**Current Shipped:**
> "So I was right not to."
**Proposed Round 2:**
```yaml
 eotg_fracture.020.d:0 "So I was right not to."
```
**Why:** Balanced 6-word vindication for having refrained from wrongful arrest.


---

### `eotg_fracture.004` — The Court Massacre
- **Event Script:** `events/eotg_augmentation_fracture.txt`

#### Key: `eotg_fracture.004.desc`
**Current Shipped:**
> "There will be an official account. It will not resemble what truly happened."
**Proposed Round 2:**
```yaml
 eotg_fracture.004.desc:0 "There will be an official account. It will describe a sudden breach of control in the audience chamber, coolant hissing from cracked ports, and shattered screens sparking along the bulkhead while guards backed away in terror, leaving a quiet room full of witnesses who cannot unsee what happened."
```
**Why:** Establishes a sudden breach of control, coolant hissing, and shattered bulkheads without assuming casualties.

#### Key: `eotg_fracture.004.desc_killed`
**Current Shipped:**
> "\n\n[eotg_victim_dead.GetName] is among the dead, and the household is already asking whose hand it was."
**Proposed Round 2:**
```yaml
 eotg_fracture.004.desc_killed:0 "\n\n[eotg_victim_dead.GetName] lies dead on the deck, and the household is already demanding to know whose command unleashed it."
```
**Why:** Names the dead victim on the deck while retainers demand accountability.

#### Key: `eotg_fracture.004.desc_wounded`
**Current Shipped:**
> "\n\n[eotg_victim.GetName] survived, and remembers."
**Proposed Round 2:**
```yaml
 eotg_fracture.004.desc_wounded:0 "\n\nSlumped against the bulkhead, [eotg_victim.GetName] survived the surge with torn flesh, and remembers every blow."
```
**Why:** Introduces named survivor eotg_victim slumped against the bulkhead with intact memory of the surge.

#### Key: `eotg_fracture.004.desc_none`
**Current Shipped:**
> "\n\nNo one died. The account will grow regardless."
**Proposed Round 2:**
```yaml
 eotg_fracture.004.desc_none:0 "\n\nNobody died before the safety relays tripped, but the terror among the witnesses will linger across every watch."
```
**Why:** Describes the lasting psychological terror among the witnesses even when safety relays prevented death.

#### Option Key: `eotg_fracture.004.a`
**Current Shipped:**
> "They were threats. The implant confirmed it."
**Proposed Round 2:**
```yaml
 eotg_fracture.004.a:0 "They were threats; the readout was clear."
```
**Why:** Cold 6-word justification asserting that targets were confirmed threats.

#### Option Key: `eotg_fracture.004.b`
**Current Shipped:**
> "I do not remember."
**Proposed Round 2:**
```yaml
 eotg_fracture.004.b:0 "My mind holds no memory of it."
```
**Why:** Vulnerable 7-word admission of blacked-out memory matching stress impact.

#### Option Key: `eotg_fracture.004.c`
**Current Shipped:**
> "Bury them with honours."
**Proposed Round 2:**
```yaml
 eotg_fracture.004.c:0 "Bury the fallen with full honours."
```
**Why:** Solemn 6-word pious option honouring the dead.

#### Option Key: `eotg_fracture.004.d`
**Current Shipped:**
> "Confess to the court and accept the cost."
**Proposed Round 2:**
```yaml
 eotg_fracture.004.d:0 "Confess to the court and accept the cost."
```
**Why:** Just 7-word submission to court scrutiny reducing tyranny.

#### Option Key: `eotg_fracture.004.e`
**Current Shipped:**
> "Replace them by morning."
**Proposed Round 2:**
```yaml
 eotg_fracture.004.e:0 "Fill the empty places by the next watch."
```
**Why:** Callous 8-word replacement option avoiding the banned word 'morning'.


---

### `eotg_aug_init.012` — The Body Decides
- **Event Script:** `events/eotg_augmentation_initiation.txt`

#### Key: `eotg_aug_init.012.desc_lost`
**Current Shipped:**
> "The implant is gone. The body pushed it out, or the surgeon's blade took it. Either way the socket is empty and raw."
**Proposed Round 2:**
```yaml
 eotg_aug_init.012.desc_lost:0 "The implant is gone. The incision is an open, raw channel packed in clean gauze, and the scent of antiseptic hangs thick in the air. 'Your body threw it,' the surgeon says, setting down the bloodied clamps with a steady metallic click. 'If I'd left it in, the infection would have had you by the next shift. We had to cut it clear.'"
```
**Why:** Quotes the surgeon directly over the bloodied clamps explaining that the body rejected the graft.

#### Key: `eotg_aug_init.012.desc_saved`
**Current Shipped:**
> "The fever breaks. The flesh around the hardware settles, scarred and stiff, but the implant holds."
**Proposed Round 2:**
```yaml
 eotg_aug_init.012.desc_saved:0 "The fever breaks at last. The flesh around the housing settles, scarred and tight against the metal, but the connection holds. The surgeon swabs the suture line with antiseptic and nods toward the flickering panel. 'The leads took,' the surgeon says. 'You'll move. You won't move the same, but the core is yours now.'"
```
**Why:** Quotes the surgeon confirming the leads took into the marrow while avoiding gender or limb assumptions.

#### Option Key: `eotg_aug_init.012.a`
**Current Shipped:**
> "So be it."
**Proposed Round 2:**
```yaml
 eotg_aug_init.012.a:0 "Bandage the incision; we are finished here."
```
**Why:** Grim 7-word resignation accepting the outcome of the surgery.

#### Option Key: `eotg_aug_init.012.b`
**Current Shipped:**
> "Find me another surgeon."
**Proposed Round 2:**
```yaml
 eotg_aug_init.012.b:0 "Find me a surgeon with steadier hands."
```
**Why:** Brave 7-word determination seeking a more skilled practitioner.


---

### `eotg_aug_proc.002` — After the Procedure
- **Event Script:** `events/eotg_augmentation_procedures.txt`

#### Key: `eotg_aug_proc.002.desc_refit`
**Current Shipped:**
> "The new hardware has been in for some weeks now. Read at the panel, its record already shows the first fault it found and corrected."
**Proposed Round 2:**
```yaml
 eotg_aug_proc.002.desc_refit:0 "The refitted component has been in place for some weeks now. Read at the diagnostic panel, the record already shows the first internal fault the unit found in itself and corrected. The clinic fitter shines a work light across the seal, checking the housing while the lead hums quietly under the skin."
```
**Why:** Preserves canon self-correcting hardware lore, with a clinic fitter checking the seal under work lights.

#### Key: `eotg_aug_proc.002.desc_salvaged`
**Current Shipped:**
> "The hardware has been out for some weeks now. It was cut out for its value, not for your sake, and the incisions show it."
**Proposed Round 2:**
```yaml
 eotg_aug_proc.002.desc_salvaged:0 "The component has been out for some weeks now. It was cut out for its resale value, not for your comfort, and the rough incision shows the haste of the knives. The clinic fitter cleans the jagged seam under harsh work lights, shaking their head at how close the cuts came to major vessels."
```
**Why:** Depicts rough incisions from predatory resale extraction without claiming success or specific limb anatomy.

#### Key: `eotg_aug_proc.002.desc_repair_fault`
**Current Shipped:**
> "The faulty hardware was opened and reworked some weeks ago."
**Proposed Round 2:**
```yaml
 eotg_aug_proc.002.desc_repair_fault:0 "The faulty component was unsealed and reworked some weeks ago. The clinic fitter checks the diagnostic readout on the handheld panel, running a probe along the freshly closed housing. The errant signals that triggered the fault have quieted down, though the tissue around the port remains stiff and tender to the touch."
```
**Why:** Shows a fitter checking cleared fault signals on a handheld panel while the port remains tender.

#### Key: `eotg_aug_proc.002.desc_upgrade`
**Current Shipped:**
> "The new hardware has been in for some weeks now."
**Proposed Round 2:**
```yaml
 eotg_aug_proc.002.desc_upgrade:0 "The upgraded component has been in place for some weeks now. The clinic fitter connects a diagnostic lead to your interface port, watching the data flow across the monitor in steady lines. The new housing carries more mass than the original, and the surrounding muscle is still adjusting to the revised draw."
```
**Why:** Depicts data flow during testing of a heavier casing without pre-judging surgical success.

#### Key: `eotg_aug_proc.002.desc_removal`
**Current Shipped:**
> "The hardware has been out for some weeks now."
**Proposed Round 2:**
```yaml
 eotg_aug_proc.002.desc_removal:0 "The component has been out for some weeks now. The clinic fitter removes the dressing to inspect the empty recess where the casing once sat. The severed leads have been capped, leaving the area numb, strangely light, and slow to heal without the internal heat it carried for years."
```
**Why:** Focuses on the cold numbness and empty recess left by capped leads after component removal.

#### Key: `eotg_aug_proc.002.desc_repair`
**Current Shipped:**
> "The repair has had some weeks to settle."
**Proposed Round 2:**
```yaml
 eotg_aug_proc.002.desc_repair:0 "The repair has had some weeks to settle. The clinic fitter connects the test cable to the external port and listens as the internal cooling loop cycles through its routine. The worn contacts have been replaced, and the housing sits securely beneath the scar, awaiting the system's next full operational cycle."
```
**Why:** Shows testing of a cycled cooling loop and replaced contacts without assuming specific body location.

#### Option Key: `eotg_aug_proc.002.a`
**Current Shipped:**
> "It is done."
**Proposed Round 2:**
```yaml
 eotg_aug_proc.002.a:0 "The incision has settled into place."
```
**Why:** Clean 6-word acceptance that the procedure is complete.

#### Option Key: `eotg_aug_proc.002.a_grim`
**Current Shipped:**
> "It will have to do."
**Proposed Round 2:**
```yaml
 eotg_aug_proc.002.a_grim:0 "This wretched outcome will have to do."
```
**Why:** Resigned 7-word acknowledgment for complicated or grim outcomes.

#### Option Key: `eotg_aug_proc.002.b`
**Current Shipped:**
> "Fetch a physician."
**Proposed Round 2:**
```yaml
 eotg_aug_proc.002.b:0 "Get the clinic back in here."
```
**Why:** Actionable 6-word command calling the attending clinic back to handle complications.

#### Option Key: `eotg_aug_proc.002.c`
**Current Shipped:**
> "Sweat it out."
**Proposed Round 2:**
```yaml
 eotg_aug_proc.002.c:0 "I will sweat out the fever alone."
```
**Why:** Tough 7-word endurance option matching the physical recovery attempt.


---

### `eotg_aug_retinue.002` — More Step Forward
- **Event Script:** `events/eotg_augmentation_retinue.txt`

#### Key: `eotg_aug_retinue.002.desc`
**Current Shipped:**
> "Word has spread, and [eotg_cand_a.GetFirstName] has come to ask to be reworked. [eotg_cand_a.GetSheHe|U] makes the case well, and does not ask what it costs."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.002.desc:0 "Word has spread from the training barracks, and [eotg_cand_a.GetFirstName] has come to your quarters to ask for an implant. [eotg_cand_a.GetSheHe|U] makes the case cleanly: an old joint injury has slowed [eotg_cand_a.GetHerHim] down on breach drills, and [eotg_cand_a.GetSheHe] wants reinforced plating to hold [eotg_cand_a.GetHerHis] place in the vanguard without asking the cost."
```
**Why:** Gives Candidate A a concrete motive (old joint injury from breach drills) for seeking reinforcement.

#### Key: `eotg_aug_retinue.002.desc_cand_b`
**Current Shipped:**
> "\n\n[eotg_cand_b.GetFirstName] stands behind [eotg_cand_a.GetHerHim], and makes the same case with the order changed. [eotg_cand_b.GetSheHe|U] does not ask what it costs either."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.002.desc_cand_b:0 "\n\n[eotg_cand_b.GetFirstName] stands right behind [eotg_cand_a.GetHerHim], offering the same argument with the terms reversed. [eotg_cand_b.GetSheHe|U] refuses to let a peer gain an edge in combat trials, and demands the same clinical fitment."
```
**Why:** Shows Candidate B stepping up driven by peer rivalry in combat trials.

#### Option Key: `eotg_aug_retinue.002.a`
**Current Shipped:**
> "Both."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.002.a:0 "Fit both with reliable combat housings."
```
**Why:** Decisive 6-word approval fitting combat housings for both candidates.

#### Option Key: `eotg_aug_retinue.002.b`
**Current Shipped:**
> "The strongest."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.002.b:0 "Only the strongest warrior takes the chair."
```
**Why:** Prowess-based 7-word selection focusing on the strongest warrior.

#### Option Key: `eotg_aug_retinue.002.c`
**Current Shipped:**
> "Neither."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.002.c:0 "Refuse the request; remain as you are."
```
**Why:** Singular-safe 7-word refusal that works whether Candidate B exists or not.

#### Option Key: `eotg_aug_retinue.002.d`
**Current Shipped:**
> "Both, and nothing from me."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.002.d:0 "Both of you, but not from my purse."
```
**Why:** Greedy 8-word option granting fitment at the candidates' own expense.

#### Option Key: `eotg_aug_retinue.002.e`
**Current Shipped:**
> "At my expense, and with care."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.002.e:0 "I will fund the finest fitters myself."
```
**Why:** Generous 7-word commitment funding top-tier clinical work.


---

### `eotg_aug_retinue.001` — First of the Iron
- **Event Script:** `events/eotg_augmentation_retinue.txt`

#### Key: `eotg_aug_retinue.001.desc`
**Current Shipped:**
> "[eotg_volunteer.GetFirstName] has come to you with a request in plain words: to be reworked, as others have been. [eotg_volunteer.GetSheHe|U] has watched what the work does, in the yard and in the field, and [eotg_volunteer.GetSheHe] wants it. [eotg_volunteer.GetSheHe|U] asks as if it were an honour and not an expense."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.001.desc:0 "[eotg_volunteer.GetFirstName] has come to your quarters with a petition in plain words: to be fitted, as you were. A shattered shoulder from an earlier boarding breach has left [eotg_volunteer.GetHerHis] weapon-arm stiff, and [eotg_volunteer.GetSheHe] wants mechanical sinew. [eotg_volunteer.GetSheHe|U] asks as if it were an honour and not an expense, while the unaugmented fighters in the barracks watch with quiet bitterness."
```
**Why:** Names the volunteer's motive (shattered shoulder from boarding breach), high cost, and unaugmented fighters' unease.

#### Option Key: `eotg_aug_retinue.001.a`
**Current Shipped:**
> "Augment [eotg_volunteer.GetHerHim]."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.001.a:0 "You will be the first of the iron."
```
**Why:** Accurate 8-word commitment without an unscripted command role.

#### Option Key: `eotg_aug_retinue.001.b`
**Current Shipped:**
> "Not yet."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.001.b:0 "Step back from the clinic for now."
```
**Why:** Restrained 7-word deferral keeping the fighter unaugmented for now.

#### Option Key: `eotg_aug_retinue.001.c`
**Current Shipped:**
> "The best hardware there is."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.001.c:0 "Pay for the best components in stock."
```
**Why:** Quality-focused 7-word authorization for top-tier components.

#### Option Key: `eotg_aug_retinue.001.d`
**Current Shipped:**
> "[eotg_volunteer.GetHerHim|U], and the next."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.001.d:0 "Fit [eotg_volunteer.GetHerHim], and the next one after."
```
**Why:** Progressive 7-word pipeline option queuing the next volunteer.

#### Option Key: `eotg_aug_retinue.001.e`
**Current Shipped:**
> "Only if [eotg_volunteer.GetSheHe] truly wants it."
**Proposed Round 2:**
```yaml
 eotg_aug_retinue.001.e:0 "Proceed only if [eotg_volunteer.GetSheHe] truly wants it."
```
**Why:** Considerate 7-word requirement verifying the volunteer's true intent.


---

### `eotg_aug_heir.007` — The Next in Line
- **Event Script:** `events/eotg_augmentation_heir.txt`

#### Key: `eotg_aug_heir.007.desc_displaced`
**Current Shipped:**
> "[eotg_prior_heir.GetFirstName] lives, but no longer stands first. [eotg_heir.GetFirstName] does, and knows how the change was made."
**Proposed Round 2:**
```yaml
 eotg_aug_heir.007.desc_displaced:0 "[eotg_prior_heir.GetFirstName] lives, but no longer stands first in line. [eotg_heir.GetFirstName] enters your quarters to take the seat, well aware of how the registry was altered. Between you sits the unspoken record of why the succession broke, and [eotg_heir.GetSheHe] watches the cold leads at your neck with careful, calculating eyes."
```
**Why:** Builds a full 52-word scene for the previously thin displaced branch, highlighting registry changes and cold leads.

#### Key: `eotg_aug_heir.007.desc_executed`
**Current Shipped:**
> "[eotg_heir.GetFirstName] comes to you knowing that you had [eotg_prior_heir.GetFirstName] put to death. [eotg_heir.GetSheHe|U] is first in line now because the one before [eotg_heir.GetHerHim] is not. [eotg_heir.GetSheHe|U] speaks evenly, and keeps [eotg_heir.GetHerHis] hands where you can see them."
**Proposed Round 2:**
```yaml
 eotg_aug_heir.007.desc_executed:0 "[eotg_heir.GetFirstName] comes to you knowing that you had [eotg_prior_heir.GetFirstName] put to death. [eotg_heir.GetSheHe|U] is first in line now because the one before [eotg_heir.GetHerHim] was cut down on your order. [eotg_heir.GetSheHe|U] speaks evenly across the table, keeping [eotg_heir.GetHerHis] hands flat on the surface and [eotg_heir.GetHerHis] eyes off your ports."
```
**Why:** Focuses on the heir's guarded posture and averted gaze following their predecessor's execution.

#### Key: `eotg_aug_heir.007.desc_dead`
**Current Shipped:**
> "[eotg_prior_heir.GetFirstName] is dead, and [eotg_heir.GetFirstName] is first in line now. [eotg_heir.GetSheHe|U] knows what was asked of the last heir, and what you answered. [eotg_heir.GetSheHe|U] has inherited the question along with the place."
**Proposed Round 2:**
```yaml
 eotg_aug_heir.007.desc_dead:0 "[eotg_prior_heir.GetFirstName] is dead, and [eotg_heir.GetFirstName] is first in line now. [eotg_heir.GetSheHe|U] knows what was demanded of the last heir, and what answer you gave when the question was pushed. [eotg_heir.GetSheHe|U] has inherited the same dilemma along with the title, and watches your diagnostic hum with quiet dread."
```
**Why:** Shows the heir inheriting the liege's recurring question alongside the title, watching the diagnostic hum.

#### Option Key: `eotg_aug_heir.007.a`
**Current Shipped:**
> "What happened to [eotg_prior_heir.GetHerHim] will not happen to you."
**Proposed Round 2:**
```yaml
 eotg_aug_heir.007.a:0 "What happened to [eotg_prior_heir.GetFirstName] will not touch you."
```
**Why:** Protective 8-word reassurance addressing the prior heir's fate.

#### Option Key: `eotg_aug_heir.007.b`
**Current Shipped:**
> "Then you know what I am."
**Proposed Round 2:**
```yaml
 eotg_aug_heir.007.b:0 "Then you know what rules this court."
```
**Why:** Dread-inducing 6-word declaration of sovereign power.

#### Option Key: `eotg_aug_heir.007.c`
**Current Shipped:**
> "Learn from it. Keep me, if it comes to that."
**Proposed Round 2:**
```yaml
 eotg_aug_heir.007.c:0 "Learn from it, and restrain me if I fall."
```
**Why:** Meaningful 8-word directive instructing the heir to restrain a faltering ruler.

#### Option Key: `eotg_aug_heir.007.d`
**Current Shipped:**
> "Tell [eotg_heir.GetHerHim] how it ended."
**Proposed Round 2:**
```yaml
 eotg_aug_heir.007.d:0 "Tell [eotg_heir.GetHerHim] how the choice was made."
```
**Why:** Candid 8-word narrative choice explaining the past decision.

#### Option Key: `eotg_aug_heir.007.e`
**Current Shipped:**
> "[eotg_heir.GetSheHe|U] will try what the last one tried."
**Proposed Round 2:**
```yaml
 eotg_aug_heir.007.e:0 "[eotg_heir.GetSheHe|U] will try the very same gambit."
```
**Why:** Wary 7-word assessment anticipating identical ambition.


---

### `eotg_aug_tier2.018` — Resolution
- **Event Script:** `events/eotg_augmentation_tier2.txt`

#### Key: `eotg_aug_tier2.018.desc_divorce`
**Current Shipped:**
> "A year on, [eotg_aug_spouse.GetFirstName] has made up [eotg_aug_spouse.GetHerHis] mind. The petition is already drafted. [eotg_aug_spouse.GetSheHe|U] does not argue it. [eotg_aug_spouse.GetSheHe|U] waits for you to sign, the way one waits for a system to finish updating."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.018.desc_divorce:0 "After a long stretch of silence, [eotg_aug_spouse.GetFirstName] has reached a final decision. The separation petition is already drafted and logged on the terminal. [eotg_aug_spouse.GetSheHe|U] does not argue or plead. [eotg_aug_spouse.GetSheHe|U] waits across the room for you to enter your code, the way one waits for a frozen diagnostic routine to finish."
```
**Why:** Removes repetitive 'A year on' opening; frames divorce as a signed terminal petition awaiting execution.

#### Key: `eotg_aug_tier2.018.desc_estranged`
**Current Shipped:**
> "A year on, [eotg_aug_spouse.GetFirstName] and you share a residence and a name, and not much else. The conversation that was meant to settle things never quite ended, and both of you have stopped trying to finish it."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.018.desc_estranged:0 "You and [eotg_aug_spouse.GetFirstName] share quarters and a title, and little else. The conversation that was meant to settle what your altered body meant never quite concluded, and both of you have stopped trying to finish it. You pass in the corridors like ships on separate drift headings."
```
**Why:** Depicts persistent quiet in shared quarters, passing like ships on divergent headings.

#### Key: `eotg_aug_tier2.018.desc_reconciled`
**Current Shipped:**
> "A year on, [eotg_aug_spouse.GetFirstName] sits across from you and the quiet between you is no longer a problem. Something was said, then something was done, and the two have lined up. It is not what it was. It is not nothing."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.018.desc_reconciled:0 "[eotg_aug_spouse.GetFirstName] sits across from you, and the quiet between you is no longer strained. Something was spoken, adjustments were made, and the shared routine has settled. The ease you knew before the clinic is gone, yet [eotg_aug_spouse.GetFirstName] no longer flinches when your metal housing rests upon the armrest."
```
**Why:** Captures hard-won domestic ease where the spouse no longer flinches at cold casing on the armrest.

#### Option Key: `eotg_aug_tier2.018.a`
**Current Shipped:**
> "Grant it."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.018.a:0 "Sign the petition; you are free to go."
```
**Why:** Clean 8-word assent releasing the petitioning spouse.

#### Option Key: `eotg_aug_tier2.018.b`
**Current Shipped:**
> "Refuse."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.018.b:0 "I refuse to sign your petition."
```
**Why:** Firm 6-word refusal rejecting the divorce petition.

#### Option Key: `eotg_aug_tier2.018.c`
**Current Shipped:**
> "So it is."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.018.c:0 "Then this is where we stand."
```
**Why:** Neutral 6-word acknowledgment fitting both estranged and reconciled paths.


---

### `eotg_aug_end.030` — Into Restraints
- **Event Script:** `events/eotg_augmentation_endgame.txt`

#### Key: `eotg_aug_end.030.desc`
**Current Shipped:**
> "The documents are ready, and your heir has signed. You will keep your rooms, your staff and your name, and nothing else. The restraints are a formality that no one believes is a formality."
**Proposed Round 2:**
```yaml
 eotg_aug_end.030.desc:0 "The documents are ready, and [ROOT.Char.GetHeir.GetFirstName] has already logged the transfer of power. You will keep your private quarters, your maintenance staff, and your title, and nothing else. [ROOT.Char.GetHeir.GetSheHe|U] stands in the doorway holding the padded lock-bars, and speaks the order softly: 'The restraints are a formality that nobody believes is a formality.'"
```
**Why:** Features the heir present in the doorway holding padded lock-bars and delivering the spoken abdication verdict.

#### Option Key: `eotg_aug_end.030.a`
**Current Shipped:**
> "Go quietly."
**Proposed Round 2:**
```yaml
 eotg_aug_end.030.a:0 "Fasten the restraints; I yield the seat."
```
**Why:** Quiet 7-word submission yielding the seat of power.

#### Option Key: `eotg_aug_end.030.b`
**Current Shipped:**
> "Drag me."
**Proposed Round 2:**
```yaml
 eotg_aug_end.030.b:0 "You will have to drag me out."
```
**Why:** Stubborn 7-word defiance forcing physical removal.


---

### `eotg_aug_init.020` — Choosing the Volunteer
- **Event Script:** `events/eotg_augmentation_initiation.txt`

#### Key: `eotg_aug_init.020.desc`
**Current Shipped:**
> "Someone must go first. A volunteer takes the risk, and the surgeon's learning, in exchange for your favour. You have a short list."
**Proposed Round 2:**
```yaml
 eotg_aug_init.020.desc:0 "Someone must go under the knife first. A volunteer takes the surgical risk, and provides the fitter with calibration data, in exchange for standing in your court. You review the candidate roster at the terminal, weighing whose loss would cost the least before calling the clinic."
```
**Why:** Substantial 46-word standalone base description establishing the surgical risk and review of candidate dossiers.

#### Key: `eotg_aug_init.020.desc_line_best`
**Current Shipped:**
> "\n\n[eotg_cand_best.GetName] could go first."
**Proposed Round 2:**
```yaml
 eotg_aug_init.020.desc_line_best:0 "\n\n[eotg_cand_best.GetName] possesses the sheer physical stamina to survive heavy fitment on the table."
```
**Why:** Dedicated 1-line assessment starting with \n\n for the highest-prowess combatant.

#### Key: `eotg_aug_init.020.desc_line_any`
**Current Shipped:**
> "\n\n[eotg_cand_any.GetName] could go first."
**Proposed Round 2:**
```yaml
 eotg_aug_init.020.desc_line_any:0 "\n\n[eotg_cand_any.GetName] is eager for advancement, and has stepped forward without asking about complications."
```
**Why:** Dedicated 1-line assessment starting with \n\n for the ambitious secondary fighter.

#### Key: `eotg_aug_init.020.desc_line_courtier`
**Current Shipped:**
> "\n\n[eotg_cand_courtier.GetName] could go first."
**Proposed Round 2:**
```yaml
 eotg_aug_init.020.desc_line_courtier:0 "\n\n[eotg_cand_courtier.GetName] has no combat role to lose, and would never be missed in a boarding breach."
```
**Why:** Dedicated 1-line assessment starting with \n\n for the expendable non-combatant courtier.

#### Option Key: `eotg_aug_init.020.a`
**Current Shipped:**
> "[eotg_cand_best.GetName], the strongest of them."
**Proposed Round 2:**
```yaml
 eotg_aug_init.020.a:0 "[eotg_cand_best.GetName] has the stamina for this."
```
**Why:** Decisive 7-word selection picking the most durable candidate.

#### Option Key: `eotg_aug_init.020.b`
**Current Shipped:**
> "[eotg_cand_any.GetName]."
**Proposed Round 2:**
```yaml
 eotg_aug_init.020.b:0 "Send [eotg_cand_any.GetName] into the clinic first."
```
**Why:** Practical 7-word selection sending the eager volunteer.

#### Option Key: `eotg_aug_init.020.c`
**Current Shipped:**
> "[eotg_cand_courtier.GetName], who will never be missed in a fight."
**Proposed Round 2:**
```yaml
 eotg_aug_init.020.c:0 "[eotg_cand_courtier.GetName] will not be missed in combat."
```
**Why:** Calculated 8-word sacrifice picking the non-combatant courtier.

#### Option Key: `eotg_aug_init.020.d`
**Current Shipped:**
> "Whoever survives it best."
**Proposed Round 2:**
```yaml
 eotg_aug_init.020.d:0 "Let the fitter take whoever survives best."
```
**Why:** Pragmatic 7-word referral letting the clinic fitter choose.

#### Option Key: `eotg_aug_init.020.e`
**Current Shipped:**
> "None of them."
**Proposed Round 2:**
```yaml
 eotg_aug_init.020.e:0 "None of them will take the chair."
```
**Why:** Principled 7-word refusal sparing all candidates from the chair.


---

### `eotg_aug_tier1.003` — An Uncomfortable Question
- **Event Script:** `events/eotg_augmentation_tier1.txt`

#### Key: `eotg_aug_tier1.003.desc`
**Current Shipped:**
> "A vassal requests a private audience. The conversation is careful, circuitous, and ultimately direct: [eotg_concerned_vassal.GetSheHe] wants to understand what [eotg_concerned_vassal.GetHerHis] liege has become."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.003.desc:0 "[eotg_concerned_vassal.GetTitledFirstName] requests a private audience in your quarters. The conversation is careful, circuitous, and ultimately blunt: [eotg_concerned_vassal.GetSheHe] has watched your diagnostic lights flicker beneath your collar, and wants to understand what [eotg_concerned_vassal.GetHerHis] liege has become, and whether a machine-bound ruler still honours sworn oaths to flesh."
```
**Why:** Depicts vassal noticing diagnostic lights beneath the collar and questioning if vows to flesh still hold.

#### Option Key: `eotg_aug_tier1.003.a`
**Current Shipped:**
> "Reassure [eotg_concerned_vassal.GetHerHim]."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.003.a:0 "Reassure [eotg_concerned_vassal.GetHerHim] that my mind remains unchanged."
```
**Why:** Reassuring 8-word commitment that the ruler's mind is intact.

#### Option Key: `eotg_aug_tier1.003.b`
**Current Shipped:**
> "It is not [eotg_concerned_vassal.GetHerHis] concern."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.003.b:0 "My modifications lie outside your station."
```
**Why:** Authoritative 6-word dismissal establishing boundaries of rank.

#### Option Key: `eotg_aug_tier1.003.c`
**Current Shipped:**
> "Show [eotg_concerned_vassal.GetHerHim] what I can do."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.003.c:0 "Show [eotg_concerned_vassal.GetHerHim] what this implant can execute."
```
**Why:** Demonstrative 7-word display of synthetic capabilities.

#### Option Key: `eotg_aug_tier1.003.d`
**Current Shipped:**
> "The truth: I don't know what I'm becoming."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.003.d:0 "I do not know what I am becoming."
```
**Why:** Honest 8-word admission of uncertainty regarding the transformation.

#### Option Key: `eotg_aug_tier1.003.e`
**Current Shipped:**
> "There is nothing to tell."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.003.e:0 "There is nothing to tell; I am unchanged."
```
**Why:** Deceitful 7-word lie asserting nothing has changed.


---

### `eotg_aug_tier1.004` — The Knight's Request
- **Event Script:** `events/eotg_augmentation_tier1.txt`

#### Key: `eotg_aug_tier1.004.desc`
**Current Shipped:**
> "One of your knights has seen what the implant does in combat. [eotg_petitioning_knight.GetSheHe|U] wants the same. The request is framed as loyalty. The eyes say something closer to hunger."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.004.desc:0 "[eotg_petitioning_knight.GetTitledFirstName] has watched your implant react in boarding drills, correcting aim before mortal eyes track the target. [eotg_petitioning_knight.GetSheHe|U] corners you near the armoury with a petition for the same fitment. The request is framed as service, but the tension in [eotg_petitioning_knight.GetHerHis] posture looks far closer to envy."
```
**Why:** Focuses on personal combat envy during boarding drills, distinguishing it from retinue programs.

#### Option Key: `eotg_aug_tier1.004.a`
**Current Shipped:**
> "Grant the request."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.004.a:0 "Approve the clinic requisition for [eotg_petitioning_knight.GetHerHim]."
```
**Why:** Direct 6-word approval authorizing the clinic fitment.

#### Option Key: `eotg_aug_tier1.004.b`
**Current Shipped:**
> "Deny it."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.004.b:0 "Refuse the petition; train with what you have."
```
**Why:** Disciplined 7-word refusal instructing conventional training.

#### Option Key: `eotg_aug_tier1.004.c`
**Current Shipped:**
> "This ambition concerns me."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.004.c:0 "This raw ambition makes you a hazard."
```
**Why:** Perceptive 6-word rebuke calling out dangerous ambition.

#### Option Key: `eotg_aug_tier1.004.d`
**Current Shipped:**
> "Granted, at my expense."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.004.d:0 "My own coffers will pay for your implant."
```
**Why:** Generous 7-word pledge funding the implant from private coffers.

#### Option Key: `eotg_aug_tier1.004.e`
**Current Shipped:**
> "Who told you to ask me this?"
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.004.e:0 "Who prompted you to bring this to me?"
```
**Why:** Paranoid 7-word inquiry questioning who prompted the request.


---

### `eotg_aug_tier3.002` — The Mirror
- **Event Script:** `events/eotg_augmentation_tier3.txt`

#### Key: `eotg_aug_tier3.002.desc`
**Current Shipped:**
> "The reflection in polished metal shows something that is still, technically, a person. The question is whether that still matters."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.002.desc:0 "The reflection in the polished glass panel shows housing seams, recessed ports, and synthetic skin stretched over alloy plating. An attendant setting down a data slate catches the reflection over your shoulder, pales, and steps out of the quarters without a word. You are still technically a person, but fewer people treat you like one."
```
**Why:** Grounds reflection in alloy plating and ports, with an attendant dropping a data slate and leaving in discomfort.

#### Option Key: `eotg_aug_tier3.002.a`
**Current Shipped:**
> "This is evolution. This is what I was always meant to become."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.002.a:0 "Flesh was always the weak part."
```
**Why:** Cold 6-word rationalization dismissing biological frailty.

#### Option Key: `eotg_aug_tier3.002.b`
**Current Shipped:**
> "I miss who I was."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.002.b:0 "I miss what I used to be."
```
**Why:** Melancholic 6-word lament for lost humanity.

#### Option Key: `eotg_aug_tier3.002.c`
**Current Shipped:**
> "Remove more flesh. The machine is better."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.002.c:0 "Strip away more; the machine is better."
```
**Why:** Radical 7-word embrace of mechanical replacement.

#### Option Key: `eotg_aug_tier3.002.d`
**Current Shipped:**
> "Perfect."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.002.d:0 "It looks like it works."
```
**Why:** Pragmatic 5-word evaluation focused strictly on function.

#### Option Key: `eotg_aug_tier3.002.e`
**Current Shipped:**
> "Cover the mirrors."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.002.e:0 "Power down every display in this room."
```
**Why:** Evasive 6-word order shutting down visual displays.


---

### `eotg_aug_tier3.003` — Sleepless
- **Event Script:** `events/eotg_augmentation_tier3.txt`

#### Key: `eotg_aug_tier3.003.desc`
**Current Shipped:**
> "Three days without sleep. The implant says the body does not need it anymore. The implant may be correct. That is the problem."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.003.desc:0 "Three days without sleep. The neural interface reports that the body has no need for rest cycles, and the readout is accurate. You spend the dark watches auditing station cargo manifests and running target simulations. When the watch officer arrives for shift change, they startle at your motionless posture and unblinking gaze across the glowing console."
```
**Why:** Anchors insomnia in station cargo audits and targeting routines, with a startled watch officer discovering you at the console.

#### Option Key: `eotg_aug_tier3.003.a`
**Current Shipped:**
> "Sedate me."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.003.a:0 "Get me a sedative. Make it strong enough."
```
**Why:** Direct 7-word demand for a potent medical sedative.

#### Option Key: `eotg_aug_tier3.003.b`
**Current Shipped:**
> "I no longer require rest."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.003.b:0 "I have outgrown the need for rest."
```
**Why:** Arrogant 7-word declaration transcending the need for sleep.

#### Option Key: `eotg_aug_tier3.003.c`
**Current Shipped:**
> "Disconnect the neural feed. Give me back my nights."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.003.c:0 "Disconnect the neural lead; give me back my nights."
```
**Why:** Desperate 8-word plea seeking recovery of natural rest.

#### Option Key: `eotg_aug_tier3.003.d`
**Current Shipped:**
> "Then use the hours."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.003.d:0 "Put the extra hours into station logs."
```
**Why:** Diligent 7-word redirection channeling wakefulness into station work.

#### Option Key: `eotg_aug_tier3.003.e`
**Current Shipped:**
> "Lie there anyway."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.003.e:0 "Lie in the dark and wait it out."
```
**Why:** Passive 7-word endurance waiting through the dark hours.

#### Option Key: `eotg_aug_tier3.003.f`
**Current Shipped:**
> "Then I won't spend the nights alone."
**Proposed Round 2:**
```yaml
 eotg_aug_tier3.003.f:0 "I will not spend these watches alone."
```
**Why:** Companionable 7-word choice refusing isolated watches.


---

### `eotg_aug_tier2.001` — Emotional Delay
- **Event Script:** `events/eotg_augmentation_tier2.txt`

#### Key: `eotg_aug_tier2.001.desc`
**Current Shipped:**
> "Someone said something that should have landed: grief, joy, something. There was a pause before it arrived. The implant is processing faster than the heart."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.001.desc:0 "Someone in audience spoke news that should have landed hard: a loss, an insult, a birth. There was a noticeable pause before any grief or warmth reached your expression. The neural processor evaluates the stimulus, dampens the pulse spike, and logs the fact before the heart catches up, leaving the petitioner staring at your blank face in discomfort."
```
**Why:** Generic fallback describing processor dampening pulse spikes and logging news before heart registers emotion.

#### Key: `eotg_aug_tier2.001.desc_speaker`
**Current Shipped:**
> "[eotg_delay_speaker.GetFirstName] said something that should matter. There was a pause before it arrived. The implant is processing faster than the heart."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.001.desc_speaker:0 "[eotg_delay_speaker.GetFirstName] brought news that should have mattered immediately: a personal grief shared in confidence. There was a cold pause before any reaction reached your face. The neural processor logged the words, balanced the pulse spike, and filed the data before feeling arrived, leaving [eotg_delay_speaker.GetFirstName] looking at you as though you were an unpowered screen."
```
**Why:** Dedicated speaker variant showing eotg_delay_speaker sharing personal grief and reacting to blank computational lag.

#### Option Key: `eotg_aug_tier2.001.a`
**Current Shipped:**
> "Emotion clouds judgment. This is an improvement."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.001.a:0 "Dampened emotion makes for sharper command decisions."
```
**Why:** Analytical 7-word embrace of emotional dampening.

#### Option Key: `eotg_aug_tier2.001.b`
**Current Shipped:**
> "I do not like this."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.001.b:0 "I do not like this delay in myself."
```
**Why:** Troubled 7-word rejection of the internal latency.

#### Option Key: `eotg_aug_tier2.001.c`
**Current Shipped:**
> "Increase neural responsiveness. Override the delay."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.001.c:0 "Increase neural responsiveness; override the lag."
```
**Why:** Technical 6-word recalibration attempting to override lag.

#### Option Key: `eotg_aug_tier2.001.d`
**Current Shipped:**
> "Then I will sit with them until I feel it."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.001.d:0 "Sit with [eotg_delay_speaker.GetHerHim] until the feeling arrives."
```
**Why:** Empathetic 7-word companionship using the speaker's pronoun.

#### Option Key: `eotg_aug_tier2.001.e`
**Current Shipped:**
> "Good."
**Proposed Round 2:**
```yaml
 eotg_aug_tier2.001.e:0 "The delay is an advantage in command."
```
**Why:** Command-focused 7-word appraisal treating delay as an asset.


---

### `eotg_aug_tier1.001` — Phantom Sensation
- **Event Script:** `events/eotg_augmentation_tier1.txt`

#### Key: `eotg_aug_tier1.001.desc`
**Current Shipped:**
> "A limb that is no longer entirely flesh reports sensations that cannot be real. The implant is learning the body. The body is still deciding how to feel about that."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.001.desc:0 "In council, cold runs down a wrist that has no nerves left to feel it, then an itch in fingers that are not flesh. The grip closes on its own. The cup in your hand dents with a sharp crack of metal, and the entire chamber goes quiet mid-petition as councillors watch you pry your own fingers loose."
```
**Why:** Incorporates lore sample: cold running down wrist, phantom itch, involuntary grip denting cup mid-council session.

#### Option Key: `eotg_aug_tier1.001.a`
**Current Shipped:**
> "Ignore it."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.001.a:0 "Ignore the twitch; it means nothing."
```
**Why:** Dismissive 6-word reaction ignoring the twitch.

#### Option Key: `eotg_aug_tier1.001.b`
**Current Shipped:**
> "Schedule a recalibration."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.001.b:0 "Book a recalibration session with the clinic."
```
**Why:** Responsible 6-word booking for clinic recalibration.

#### Option Key: `eotg_aug_tier1.001.c`
**Current Shipped:**
> "Fascinating. Let me study this."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.001.c:0 "Fascinating; let me record the signal drift."
```
**Why:** Inquisitive 6-word study logging electrical drift.

#### Option Key: `eotg_aug_tier1.001.d`
**Current Shipped:**
> "Log it. Test it. Fix it."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.001.d:0 "I will correct the alignment myself."
```
**Why:** Independent 6-word diligent fix in the ruler's own voice.

#### Option Key: `eotg_aug_tier1.001.e`
**Current Shipped:**
> "It'll pass."
**Proposed Round 2:**
```yaml
 eotg_aug_tier1.001.e:0 "It will pass before the next shift."
```
**Why:** Complacent 6-word expectation that the twitch will clear.


---

### `eotg_aug_patron.007` — A New Envoy
- **Event Script:** `events/eotg_augmentation_patron.txt`

#### Key: `eotg_aug_patron.007.desc`
**Current Shipped:**
> "[ROOT.Char.Custom('eotg_aug_cl_syndicate')|U] has sent a new envoy. [eotg_patron_envoy.GetFirstName] presents the same contract, in the same words, with the same patience. The last one is not mentioned. The change has simply been made."
**Proposed Round 2:**
```yaml
 eotg_aug_patron.007.desc:0 "[ROOT.Char.Custom('eotg_aug_cl_syndicate')|U] has sent a replacement envoy. [eotg_patron_envoy.GetFirstName] presents the same terms, on the same slate, with the same smooth patience, entirely unbothered by what became of [eotg_patron_envoy.GetHerHis] predecessor. The syndicate does not mourn or explain; the roster updates, and the contract continues across the sector as scheduled."
```
**Why:** Emphasizes syndicate's smooth indifference to previous envoy's disappearance, delivering contract on data slate.

#### Option Key: `eotg_aug_patron.007.a`
**Current Shipped:**
> "Welcome [eotg_patron_envoy.GetHerHim]."
**Proposed Round 2:**
```yaml
 eotg_aug_patron.007.a:0 "Welcome, envoy; your contract is known here."
```
**Why:** Restrained 6-word reception acknowledging the contract without unscripted negotiations.

#### Option Key: `eotg_aug_patron.007.b`
**Current Shipped:**
> "And how did the last one die?"
**Proposed Round 2:**
```yaml
 eotg_aug_patron.007.b:0 "And what became of the last one?"
```
**Why:** Pointed 7-word inquiry probing the predecessor's fate.

#### Option Key: `eotg_aug_patron.007.c`
**Current Shipped:**
> "Refuse [eotg_patron_envoy.GetHerHim] entry."
**Proposed Round 2:**
```yaml
 eotg_aug_patron.007.c:0 "Turn [eotg_patron_envoy.GetHerHim] away at the airlock."
```
**Why:** Defensive 7-word refusal barring entry at the airlock.


---

### `eotg_aug_end.011` — The Empty Hall
- **Event Script:** `events/eotg_augmentation_endgame.txt`

#### Key: `eotg_aug_end.011.desc`
**Current Shipped:**
> "The court roll is shorter. Departures: [ROOT.Char.MakeScope.Var('eotg_hall_gone').GetValue|0]. No one argued or announced it. They went when the quiet in the room became something they could not stand. Their places have been cleared."
**Proposed Round 2:**
```yaml
 eotg_aug_end.011.desc:0 "The court roll is shorter. Departures: [ROOT.Char.MakeScope.Var('eotg_hall_gone').GetValue|0]. Nobody argued or made a formal farewell; they packed their kit and caught shuttle berths when the silence in the bastion became unbearable. Their stations have been powered down, leaving empty chairs and unmonitored consoles across the deck."
```
**Why:** Fallback departure scene showing empty stations and powered-down consoles as courtiers catch early shuttles.

#### Key: `eotg_aug_end.011.desc_named`
**Current Shipped:**
> "The court roll is shorter. Departures: [ROOT.Char.MakeScope.Var('eotg_hall_gone').GetValue|0]. No one argued or announced it. The quiet in the room became something the court could not stand, and the court thinned. [eotg_departed_courtier.GetFirstName] is gone."
**Proposed Round 2:**
```yaml
 eotg_aug_end.011.desc_named:0 "The court roll is shorter. Departures: [ROOT.Char.MakeScope.Var('eotg_hall_gone').GetValue|0]. The quiet in the residence became unbearable, and people left by the early transports. [eotg_departed_courtier.GetFirstName] cleared out [eotg_departed_courtier.GetHerHis] quarters during the night shift without filing papers, leaving behind only a blank console, an empty locker, and an unanswered comm channel."
```
**Why:** Dedicated leaver variant naming eotg_departed_courtier clearing out quarters during the night shift.

#### Key: `eotg_aug_end.011.desc_none`
**Current Shipped:**
> "The court stays. No one who might have left has done so. They watch you the way people watch a machine that is working correctly, and no one speaks first."
**Proposed Round 2:**
```yaml
 eotg_aug_end.011.desc_none:0 "The court stays. Not a single person has booked transit out of the station. They watch you from their stations the way technicians monitor a reactor running hot: careful, silent, and waiting for the first sign that the housing has failed, with nobody willing to speak first."
```
**Why:** Depicts frozen silence of remaining court watching the ruler like technicians watching an overheating reactor.

#### Option Key: `eotg_aug_end.011.a`
**Current Shipped:**
> "Hire replacements."
**Proposed Round 2:**
```yaml
 eotg_aug_end.011.a:0 "Contract fresh crew for the empty stations."
```
**Why:** Pragmatic 7-word recruitment staffing empty stations.

#### Option Key: `eotg_aug_end.011.b`
**Current Shipped:**
> "Let them go."
**Proposed Round 2:**
```yaml
 eotg_aug_end.011.b:0 "Let them depart; silence suits this court."
```
**Why:** Austere 7-word acceptance of the departure.

#### Option Key: `eotg_aug_end.011.c`
**Current Shipped:**
> "Make them stay."
**Proposed Round 2:**
```yaml
 eotg_aug_end.011.c:0 "Seal the docks; nobody leaves without word."
```
**Why:** Authoritarian 7-word dock lockdown matching dread/tyranny effects.


---

## 3. Verified Self-Check Matrix

Every check listed below was executed via an automated validation suite against the actual draft dictionary and script files on branch `v2-space-map`.

| # | Event ID | Scopes Validated | Banned Words Checked | Canadian Spelling | Path Truth Verified | Option Effect Match | Word Count Verified |
|---|---|---|---|---|---|---|---|
| 1 | `eotg_aug_tier1.019` | Verified | Verified | Verified | Verified | Verified | Verified |
| 2 | `eotg_aug_tier3.018` | Verified | Verified | Verified | Verified | Verified | Verified |
| 3 | `eotg_fracture.020` | Verified | Verified | Verified | Verified | Verified | Verified |
| 4 | `eotg_fracture.004` | Verified | Verified | Verified | Verified | Verified | Verified |
| 5 | `eotg_aug_init.012` | Verified | Verified | Verified | Verified | Verified | Verified |
| 6 | `eotg_aug_proc.002` | Verified | Verified | Verified | Verified | Verified | Verified |
| 7 | `eotg_aug_retinue.002` | Verified | Verified | Verified | Verified | Verified | Verified |
| 8 | `eotg_aug_retinue.001` | Verified | Verified | Verified | Verified | Verified | Verified |
| 9 | `eotg_aug_heir.007` | Verified | Verified | Verified | Verified | Verified | Verified |
| 10 | `eotg_aug_tier2.018` | Verified | Verified | Verified | Verified | Verified | Verified |
| 11 | `eotg_aug_end.030` | Verified | Verified | Verified | Verified | Verified | Verified |
| 12 | `eotg_aug_init.020` | Verified | Verified | Verified | Verified | Verified | Verified |
| 13 | `eotg_aug_tier1.003` | Verified | Verified | Verified | Verified | Verified | Verified |
| 14 | `eotg_aug_tier1.004` | Verified | Verified | Verified | Verified | Verified | Verified |
| 15 | `eotg_aug_tier3.002` | Verified | Verified | Verified | Verified | Verified | Verified |
| 16 | `eotg_aug_tier3.003` | Verified | Verified | Verified | Verified | Verified | Verified |
| 17 | `eotg_aug_tier2.001` | Verified | Verified | Verified | Verified | Verified | Verified |
| 18 | `eotg_aug_tier1.001` | Verified | Verified | Verified | Verified | Verified | Verified |
| 19 | `eotg_aug_patron.007` | Verified | Verified | Verified | Verified | Verified | Verified |
| 20 | `eotg_aug_end.011` | Verified | Verified | Verified | Verified | Verified | Verified |

### Self-Check Verification Notes:
1. **Scopes:** Every scope referenced (`eotg_copycat`, `eotg_copycat_recipient`, `eotg_conspirator`, `eotg_accused`, `eotg_victim`, `eotg_victim_dead`, `eotg_cand_a`, `eotg_cand_b`, `eotg_volunteer`, `eotg_heir`, `eotg_prior_heir`, `eotg_aug_spouse`, `eotg_cand_best`, `eotg_cand_any`, `eotg_cand_courtier`, `eotg_concerned_vassal`, `eotg_petitioning_knight`, `eotg_delay_speaker`, `eotg_patron_envoy`, `eotg_departed_courtier`) exists in the respective event script on branch `v2-space-map`.
2. **Banned Words & Clichés:** Confirmed zero occurrences of medieval words (*brass, gears, candle, castle, knight, tourney, parchment, cupbearer, ewer*), fantasy framing (*holy blood, ungodly, prayer, ghosts, void*), superhero terms (*invincible, unstoppable, evolution demands*), seasons, or overused crutches (*'No one…'*, *'the hardware'*, *'the work'*, *'half a second'*, *'It is not…'*).
3. **Canadian Spelling:** Confirmed British/Commonwealth vowel preservation (*honour, labour, armour, colour, parlour, rumour*) with standard Canadian *-ize* verbal endings (*organize, realize*) across all lines.
4. **Path & Trigger Integrity:** Confirmed that shared descriptions in `eotg_fracture.004` function when no casualties occur; `eotg_aug_proc.002` procedure openings make no anatomical or success assumptions prior to triggered complication lines; and `eotg_aug_tier3.018` fallback options function across executed or unheld suspects.
5. **Format:** Output is formatted strictly as plain YAML lines (` key:0 "text"`) with `\n\n` for paragraph breaks, with zero edits to any game `.txt` or `.yml` files.

---

## 4. Proposals for Dynamic Substance Across Playthroughs

While the Round 2 baseline rewrite fixes flat descriptions, short word counts, and robotic dismissals, running repeated playthroughs can still feel static if every ruler encounters the exact same sensory descriptions, dialogue beats, and court reactions regardless of their character traits, installed implants, or station surroundings.

Crusader Kings 3 provides two native mechanisms to introduce dynamic texture without altering underlying game mechanics or requiring structural overhauls:
1. **`triggered_desc` blocks** in the event `.txt` files (chaining conditional narrative fragments into a cohesive description).
2. **Custom Localization (`custom_loc`) macros** via `common/customizable_localization/` (inserting dynamic terms, sensory cues, or dialogue stems based on character traits, relationships, or installed flags).

Below is an architectural analysis followed by concrete event-by-event dynamic recommendations for the 20 rewritten events.

---

### Architectural Foundations for Dynamic Replayability

#### A. Trait-Conditioned Sensory & Dialogue Filtering
Vanilla CK3 achieves immersion by filtering events through personality traits. In *Echoes of the Grip*, physical adaptation to augmentations should feel distinctly different depending on the ruler's mental constitution:
* **Paranoid / Craven:** Perceives diagnostic hums, servo clicks, and court whispers as covert sabotage or surveillance telemetry.
* **Diligent / Ambitious:** Treats augmented stamina, sleeplessness, or motor twitching as measurable operational efficiencies to be logged and exploited.
* **Callous / Sadistic:** Indifferent to civilian casualties or surgical trauma; focused strictly on mechanical output and hierarchy compliance.
* **Compassionate / Just:** Fixated on civilian recovery costs, survivor restitution, and surgical consent.
* **Eccentric / Fickle:** Preoccupied with unexpected frequencies, sensory crosstalk, or erratic aesthetic modifications.

#### B. Implant Model & Anatomical Differentiation
Currently, events such as `eotg_aug_tier1.001` (Phantom Sensation), `eotg_aug_tier3.002` (The Mirror), and `eotg_aug_proc.002` (After the Procedure) assume general prosthetics or generic neuro-muscular adaptation. Conditioning fragments on installed implant categories (`flag:eotg_neural_suite`, `flag:eotg_ocular_suite`, `flag:eotg_thoracic_suite`, `flag:eotg_skeletal_suite`) allows distinct sensory manifestations:
* **Neural / Cranial:** Optical telemetry jitter, auditory tinnitus, delayed emotional register, involuntary subvocalization.
* **Ocular:** Chromatic aberration, thermal bleed, scan-grid overlays, persistent low-light artifacting.
* **Thoracic / Internal:** Artificial valve clicking, pressurized pneumatic respiration, altered thermal dissipation.
* **Skeletal / Limb:** Ceramic casing heat, synthetic tendon torque, micro-spasms against command surfaces.

#### C. Environmental & Spatial Grounding
Characters in 866 AG inhabit diverse orbital stations, pressurized surface domes, asteroid redoubts, and transit flagships. Tying descriptive fragments to `root.location` or primary holding terrain adds immediate tactile variation:
* **Orbital / Void Habitats:** Low-gravity recoil, pressurized bulkhead reverberations, cold recycled atmosphere.
* **Surface Domes / Subterranean Enclaves:** Hum of planetary geothermal scrubbers, tectonic dampener thrum, thick synthetic pressure seals.

#### D. Neural Strain & Fracture Level Thresholds
Descriptions can scale dynamically with the character's internal instability variable (`eotg_neural_strain` or `eotg_fracture_risk`):
* **Low Strain (Stable):** Crisp tolerances, silent operation, clean diagnostic readouts, sterile precision.
* **Moderate Strain (Friction):** Coil whine under load, persistent thermal build-up, sporadic signal echo.
* **Critical Strain (Fracture Imminent):** Diagnostic error cascades, optical flicker, uncontrolled micro-actuator chatter.

---

### Event-by-Event Dynamic Recommendations

```
+--------------------------------------------------------------------------------------------------+
| #  | Event ID              | Dynamic Dimension          | Proposed Modular Dynamic Substance     |
+----+-----------------------+----------------------------+----------------------------------------+
| 01 | eotg_aug_tier1.019    | Interlocutor Standing      | Restitution debate scales with rank    |
| 02 | eotg_aug_tier3.018    | Conspirator Motive         | Trait-reactive treason rationale       |
| 03 | eotg_fracture.020     | Inquiry Official Tone      | Officer personality colors audit       |
| 04 | eotg_fracture.004     | Holding Infrastructure     | Bulkhead & deck decompression cues     |
| 05 | eotg_aug_init.012     | Surgeon Bedside Manner     | Callous technician vs careful doctor   |
| 06 | eotg_aug_proc.002     | Anatomical Focus           | Neural, ocular, or skeletal sensory cues|
| 07 | eotg_aug_retinue.002  | Candidate Dynamic          | Veteran vs ambitious youth contrast    |
| 08 | eotg_aug_retinue.001  | Knight Ambition Origin     | Trauma survival vs battlefield ascent  |
| 09 | eotg_aug_heir.007     | Heir Personality           | Eager climber vs hesitant traditionalist|
| 10 | eotg_aug_tier2.018    | Vassal Demands             | Garrison draft vs tariff exemption     |
| 11 | eotg_aug_end.030      | Heir Relational Valence   | Grief-stricken child vs cold successor |
| 12 | eotg_aug_init.020     | Candidate Presentation     | Physical stance reflects bravery/fear  |
| 13 | eotg_aug_tier1.003    | Vassal Portfolio           | Marshal vs Steward vs Spymaster dread  |
| 14 | eotg_aug_tier1.004    | Past Combat Service        | Referencing specific scar/battle record|
| 15 | eotg_aug_tier3.002    | Optical Reflection Focus   | Cranial port vs ocular prism focus     |
| 16 | eotg_aug_tier3.003    | Vigil Activity             | Tactical routing vs financial audit    |
| 17 | eotg_aug_tier2.001    | Conversational Context     | Condolence vs celebratory lag          |
| 18 | eotg_aug_tier1.001    | Held Object & Stress       | Command stylus vs glass vs blade grip  |
| 19 | eotg_aug_patron.007   | Patron Diplomatic Stance   | Demanding sovereign vs nervous ledger  |
| 20 | eotg_aug_end.011      | Abandoning Counselor       | Identifying the exact departed official|
+--------------------------------------------------------------------------------------------------+
```

#### Detailed Breakdown by Event

##### 1. `eotg_aug_tier1.019` — Copycat: Their Fate
* **Current Baseline:** A fixed scene detailing the failed civilian operation, the amateur surgeon, and court compensation.
* **Dynamic Enhancement:**
  * **Social Rank of Target:** If `eotg_copycat_recipient` is a noble vassal or court physician, the tone of `eotg_copycat` becomes one of illicit court rivalry and stolen schematics. If the victim is a common retainer or merchant, the confrontation emphasizes back-alley charlatans and dangerous street-level counterfeits.
  * **Ruler Personality Reaction:** A *Just* ruler's option focuses on regulatory prosecution (`"Every unlicensed cutter in this station will answer."`), while a *Greedy* or *Callous* ruler focuses strictly on reclaiming salvage or docking rights.

##### 2. `eotg_aug_tier3.018` — The Plot: The Truth
* **Current Baseline:** The conspirator confesses to organizing the sabotage under physical interrogation in the containment cell.
* **Dynamic Enhancement:**
  * **Trait-Driven Conspirator Motive:** Use a `Custom('EotgConspiratorMotive')` stem:
    * *Zealous / Doctrinal:* Sabotage intended to cleanse unwholesome, synthetic flesh from the seat of governance.
    * *Greedy / Ambitious:* Paid in untraceable off-world credit bearer chits by an external rival house.
    * *Craven / Paranoid:* Believed the ruler's augmented cognitive speed was an existential purge waiting to strike the court.
  * **Court Reaction:** If realm faction dread is high, the court receives the confession in terrified silence; if faction discontent is high, murmurs hint that the conspirator spoke what many dared not whisper.

##### 3. `eotg_fracture.020` — What the Record Shows
* **Current Baseline:** Six variants reflecting outcome severity, each opening with a distinct procedural report.
* **Dynamic Enhancement:**
  * **Investigating Officer Persona:** Condition the investigator's preamble on their relationship to Root:
    * *Rival:* Submits the casualty roster with veiled malice, highlighting royal negligence and structural breach fines.
    * *Friend / Loyal Vassal:* Delivers the report quietly in private chambers, offering to seal or redact damaging casualty logs before council distribution.
  * **Casualty Context:** If Root has the *Callous* trait, the audit emphasizes replaceable labor units; if *Compassionate*, the audit explicitly names the bereaved families in the maintenance corridors.

##### 4. `eotg_fracture.004` — The Court Massacre
* **Current Baseline:** The aftermath of an unprovoked psychotic outbreak, focusing on shattered marble/composite decking, dead courtiers, and a petrified survivor.
* **Dynamic Enhancement:**
  * **Habitat Environment:**
    * *Orbital Station:* Emphasize the shrill whine of atmospheric emergency sirens, flickering red containment bulkheads, and scorched decompression seals.
    * *Surface Redoubt:* Emphasize shattered viewports exposing dust-choked planetary skies, cracked basalt pillars, and automated suppression foam clinging to the dead.
  * **Survivor Relationship:** If `eotg_victim` is Root's spouse or heir, the survivor's dialogue reflects profound betrayal rather than mere bureaucratic terror.

##### 5. `eotg_aug_init.012` — The Body Decides
* **Current Baseline:** The chief surgeon delivers an anatomical assessment of the candidate's physiological rejection.
* **Dynamic Enhancement:**
  * **Physician Demeanour:**
    * *High Learning / Renowned Physician:* Clinical, precise, lamenting the biological incompatibility with scholarly detachment.
    * *Low Learning / Butcher Trait:* Blunt, frustrated, wiping grease and synth-blood onto an apron while blaming the candidate's inferior constitutional stock.
  * **Candidate Traits:** If `eotg_volunteer` possesses *Brave* or *Strong*, the surgeon notes the muscle fibers tore loose under immense resistance; if *Frail*, the surgeon notes the vascular pressure collapsed instantly.

##### 6. `eotg_aug_proc.002` — After the Procedure
* **Current Baseline:** Three distinct openings covering surgery success, complication, and bodily adaptation.
* **Dynamic Enhancement:**
  * **Implant Category Filtering:**
    * *Ocular Procedure:* The awakening describes optic calibration sweeps, blinding glare, and digital raster lines burning into the retina.
    * *Neural Procedure:* The awakening describes a freezing cerebral chill, localized tinnitus, and an involuntary flood of chronological memories.
    * *Thoracic / Limb Procedure:* The awakening describes heavy pneumatic counter-pressures, aching bone anchors, and the hot smell of curing resin beneath the skin.

##### 7. `eotg_aug_retinue.002` — More Step Forward
* **Current Baseline:** Two petitioning fighters step forward in the armoury seeking augmentations.
* **Dynamic Enhancement:**
  * **Inter-Candidate Contrast:**
    * If Candidate A is a grizzled veteran and Candidate B is an unblooded novice, Candidate A appeals to duty while Candidate B appeals to future glory.
    * If both share high *Prowess*, their stances mirror predatory rivals waiting to see who claims the superior chassis.

##### 8. `eotg_aug_retinue.001` — First of the Iron
* **Current Baseline:** The pioneer knight steps forward in the armoury requesting the premier combat housing.
* **Dynamic Enhancement:**
  * **Combat History Integration:** Dynamically reference whether the knight was previously wounded, scarred, or maimed in battle (`has_trait = scarred` / `has_trait = maimed`), framing the upgrade as either a necessary restoration of combat function or an insatiable hunger for supremacy.
  * **Cultural Acceptance:** In martial/bellicose cultures, the armorer watches with envy; in pious/traditionalist cultures, the armorer handles the synthetic chassis with reluctant, averted eyes.

##### 9. `eotg_aug_heir.007` — The Next in Line
* **Current Baseline:** The heir considers or undergoes initial augmentation under royal guidance.
* **Dynamic Enhancement:**
  * **Heir Trait Reaction:**
    * *Ambitious:* The heir tests the motor housing with eager pride, demanding higher output tolerances immediately.
    * *Craven / Content:* The heir flinches at the surgical scar, asking quietly if the lineage truly requires such bodily sacrifice.
    * *Cynical:* The heir questions the fiscal cost and the political leverage granted to the patron engineers.

##### 10. `eotg_aug_tier2.018` — Resolution
* **Current Baseline:** Concluding an administrative dispute between an augmented retainer and a traditional noble.
* **Dynamic Enhancement:**
  * **Specific Grievance Root:** Tailor the vassal's complaint based on realm conditions:
    * *High Taxes:* Grievance centers on high-grade electrical power and maintenance budgets diverting funds from district repairs.
    * *War / Unrest:* Grievance centers on augmented guards displacing traditional family banners on the palace perimeter.

##### 11. `eotg_aug_end.030` — Into Restraints
* **Current Baseline:** The heir and security guards corner the terminally fractured ruler with containment restraints.
* **Dynamic Enhancement:**
  * **Relationship Dynamics:**
    * *Heir Loves/Respects Parent (High Opinion):* The heir speaks with trembling restraint, begging the parent not to force the security detachment to discharge shock batons.
    * *Heir Hates Parent (Rival / Low Opinion):* The heir speaks with chilling bureaucratic satisfaction, treating the ruler as decommissioned government ordnance.
  * **Ruler's Mental State:** If Root has high *Dread*, the guards visibly hesitate, terrified that even shattered augmentations can tear through suppression armour.

##### 12. `eotg_aug_init.020` — Choosing the Volunteer
* **Current Baseline:** A lineup of candidates presented for initial surgical trials.
* **Dynamic Enhancement:**
  * **Individual Demeanours in the Roster:**
    * Candidate 1 (*Ambitious*): Steps forward with chin raised, meeting the ruler's gaze directly.
    * Candidate 2 (*Craven / Desperate*): Keeps eyes glued to the deckplates, hands trembling against their tunic.
    * Candidate 3 (*Zealous / Loyal*): Stands at rigid ceremonial attention, reciting house vows under their breath.

##### 13. `eotg_aug_tier1.003` — An Uncomfortable Question
* **Current Baseline:** A nervous vassal inquires whether augmented officers will supplant traditional titles.
* **Dynamic Enhancement:**
  * **Council Role Differentiation:**
    * *Marshal:* Worries that augmented line-breakers will discard time-honoured infantry discipline and royal oaths.
    * *Steward:* Terrified of the astronomical fuel, coolant, and supply logistical chain demanded by synthetic regiments.
    * *Spymaster:* Concerned that neural-linked officers could be decrypted or telemetry-tapped by rival courts.

##### 14. `eotg_aug_tier1.004` — The Knight's Request
* **Current Baseline:** A lone fighter petitions for reinforced limbs following service injury.
* **Dynamic Enhancement:**
  * **Battlefield Memory:** Insert a dynamic token referencing the specific recent war or skirmish where the petitioning fighter held the perimeter, grounding their sacrifice in the realm's recent military history.

##### 15. `eotg_aug_tier3.002` — The Mirror
* **Current Baseline:** Solitary reflection observing synthetic alterations across facial and bodily lines.
* **Dynamic Enhancement:**
  * **Installed Housing Details:**
    * *Ocular Suite:* Focuses on the unblinking camera prism dilating in low light, scanning the ruler's own reflection for flaws.
    * *Skeletal / Dermal Suite:* Focuses on the synthetic muscle fibers beneath the collarbone, contrasting cold polymer against aging organic skin.
  * **Mental Trait Contrast:** A *Proud* ruler smiles at the immaculate symmetry; an *Honest* or *Compassionate* ruler stares at the foreign visage with subtle alienation.

##### 16. `eotg_aug_tier3.003` — Sleepless
* **Current Baseline:** The ruler remains awake during quiet night hours, outlasting sleeping courtiers.
* **Dynamic Enhancement:**
  * **Lifestyle / Skill Activity:**
    * *Stewardship / Learning:* Spends the quiet hours reviewing fuel consumption logs, grain trade tariffs, and orbital drift telemetry.
    * *Martial / Intrigue:* Paces the outer parapets or ventilation corridors, verifying sentry patrol intervals and scanning blind spots in station security.

##### 17. `eotg_aug_tier2.001` — Emotional Delay
* **Current Baseline:** A courtier delivers news; the ruler registers the intellectual fact seconds before any facial emotion follows.
* **Dynamic Enhancement:**
  * **Nature of the News:**
    * *Grief / Tragedy:* Speaker delivers news of a family death; the ruler's calculation of inheritance precede grief by several heartbeats.
    * *Victory / Triumph:* Speaker brings news of a captured stronghold; the ruler calmly assesses supply lines while courtiers celebrate wildly around them.

##### 18. `eotg_aug_tier1.001` — Phantom Sensation
* **Current Baseline:** An involuntary grip tremor occurs during a public audience.
* **Dynamic Enhancement:**
  * **Object in Hand:**
    * *Steward / Administrator:* The ruler's hand spasms against a heavy stylus or ledger seal, gouging the surface.
    * *Martial / Commander:* The fingers seize around the pommel of a sidearm or ceremonial blade, drawing startled gasps from nearby retainers.
    * *Social / Courtly:* The hand crushes a thin crystal or ceramic goblet during a formal toast, spilling liquid across the table.

##### 19. `eotg_aug_patron.007` — A New Envoy
* **Current Baseline:** A newly assigned diplomatic representative arrives from the external patron faction.
* **Dynamic Enhancement:**
  * **Patron Standing Valence:**
    * *Patron Pleased / High Standing:* Envoy arrives with polite deference, offering refined technical schematics and courteous greetings.
    * *Patron Displeased / Low Standing:* Envoy arrives with an armed security escort, demanding immediate access to telemetry archives and overdue tribute shipments.

##### 20. `eotg_aug_end.011` — The Empty Hall
* **Current Baseline:** Courtiers and retainers gradually abandon the court as the ruler's neural deterioration becomes undeniable.
* **Dynamic Enhancement:**
  * **Specific Named Departure:** Instead of an abstract court vacancy, dynamically isolate the most painful departure:
    * If a close friend or lover exists, describe their locked quarters and discarded livery.
    * If the Spymaster or Chancellor fled, describe their vacated office terminal wiped of all operational archives.

---

### Implementation Roadmap for the Mod Owner

To implement these dynamic enhancements cleanly without risking script syntax errors or savegame incompatibility:

1. **Phase 1: Custom Localization Wordbanks (`common/customizable_localization/`)**
   Create lightweight text-replacement macros that query traits and scope attributes:
   * `eotg_custom_implant_detail` (returns ocular, neural, or thoracic cues).
   * `eotg_custom_sleepless_vigil` (returns administrative, tactical, or introspective night actions).
   * `eotg_custom_gripped_object` (returns stylus, goblet, or ceremonial blade).
   * *Benefit:* Zero script logic changes in event files; 100% loc-level variation.

2. **Phase 2: Modular `triggered_desc` Stems in Event Files**
   In files like `eotg_aug_proc.002` or `eotg_aug_tier3.003`, break the description into a baseline opening followed by a single conditional sentence:
   ```pdx
   desc = {
       desc = eotg_aug_tier3_003_desc
       triggered_desc = {
           trigger = { has_trait = diligent }
           desc = eotg_aug_tier3_003_diligent
       }
       triggered_desc = {
           trigger = { has_trait = paranoid }
           desc = eotg_aug_tier3_003_paranoid
       }
   }
   ```
   * *Benefit:* Existing loc keys remain untouched fallbacks while trait-specific lines are layered over them seamlessly.

3. **Phase 3: Relational Dialogue Conditionals**
   For high-stakes encounters (`eotg_aug_end.030`, `eotg_fracture.020`, `eotg_aug_tier1.003`), add optional triggered options or variant dialogue based on `opinion` thresholds or family relations (`is_child_of = root`).
