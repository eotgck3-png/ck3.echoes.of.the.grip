# Event writing review against vanilla (2026-10-05)

Read-only triage of all 194 eotg_ events (192 visible) against 10,255 parsed vanilla 1.20 events.
Desc word counts are taken after resolving loc, with `[...]` counted as one word. For multi-variant
descs, "min" is the shortest path and "max" the longest. **Nothing is copied from vanilla:** the
highest 6-gram overlap with any vanilla event is a single stock phrase.

## Baselines

| Set | n | desc p25 / median / p75 | options (mean) | words per option (median) | options with a custom tooltip |
|---|---|---|---|---|---|
| Vanilla, all visible | 9,060 | 42 / 58 / 76 | 2.55 | 6 | 25% |
| Vanilla court (left + right portrait) | 5,412 | 47 / 63 / 80 | 2.79 | 6 | 25% |
| Vanilla solo | 3,648 | 36 / 52 / 69 | 2.21 | 6 | 24% |
| Vanilla decision follow-ups | 576 | 47 / 64 / 80 | 2.19 | 6 | 29% |
| **Mod, all** | 192 | 39 / 46 / 57 | **4.59** | **4** | **14%** |
| Mod court | 102 | 42 / 47 / 58 | 4.74 | 4 | 13% |

### Findings
- **Descs are short, but not badly so.** The mod's median (46) sits near the vanilla court p25. 66 of 192
  events fall below their category's p25 even on their longest variant.
- **Options are the bigger gap.**
  - 131 of 192 events have 5 or more options, against 8% in vanilla.
  - Options are terse: a median of 4 words against vanilla's 6.
  - Few carry tooltips: 14% against vanilla's 25%.
  - 36 events have no option longer than 4 words.
- **There is a fixed template.** 98 events have exactly two trait-gated options plus two or three ungated
  ones.
- **The prose is clipped.** The mean sentence is 10.4 words against vanilla's 13.5, and 30% of sentences
  are 6 words or fewer against 20% in vanilla. Applied everywhere, that rhythm makes many events read alike.
- **Characters go unnamed.** In 18% of mod court events the longest desc names no character, against 3% in
  vanilla ("A vassal requests…", "Someone must go first…").
- **Length is a filter, not a verdict.** "First of the Iron" (retinue.001) is 48 words, right at the court
  p25; its problem is substance: no stake, no reason given, and options that are labels.
- **Frontier (16 events) is in better shape:** 6.1 words per option and a median desc of 48 words. Most
  of the problems are in augmentation and fracture.

## Ranked rewrite candidates

| Event | Title | Desc words (min–max) | Options | Problem | Rewrite should add |
|---|---|---|---|---|---|
| eotg_aug_tier1.019 | Copycat: Their Fate | 22–29 | 1 ("I see.") | the only option is a dismissal | what the fate costs you; one reaction to choose |
| eotg_aug_tier3.018 | The Plot: The Truth | 26–35 | 2 | thin payoff to a chain; reads as a report | the confrontation, and what the court now believes |
| eotg_fracture.020 | What the Record Shows | 29–45 | 2 | all six variants open "The inquiry is finished…"; same structure as tier3.018 | varied openings; the wronged party's voice |
| eotg_fracture.004 | The Court Massacre | 13–40 | 5 | 13 words for a massacre on the shortest path | the aftermath, the witnesses, a named survivor |
| eotg_aug_init.012 | The Body Decides | 16–23 | 2 ("So be it.") | flat outcome | the surgeon's verdict in their own words |
| eotg_aug_proc.002 | After the Procedure | 17–49 | 3 | the base text is one sentence | a per-procedure opening with a person in it |
| eotg_aug_retinue.002 | More Step Forward | 24–45 | 5 ("Both." / "Neither.") | terse options; repeats retinue.001 | why these two; options in the ruler's voice |
| eotg_aug_retinue.001 | First of the Iron | 48 | 5 | no reason, cost or character beat | a named motive, the price, the other knights' view |
| eotg_aug_heir.007 | The Next in Line | 16–37 | 5 | the 16-word variant | a scene for the short variant |
| eotg_aug_tier2.018 | Resolution | 35–41 | 2 | terse option; reuses tier2.014's opening | an option fitting each variant |
| eotg_aug_end.030 | Into Restraints | 34 | 2 | a climax in 34 words; the heir unnamed | the heir present and speaking |
| eotg_aug_init.020 | Choosing the Volunteer | 23 | 5 | no named actors; reads as a menu | one line per candidate |
| eotg_aug_tier1.003 | An Uncomfortable Question | 23 | 5 | an anonymous vassal; no stake | a named vassal and their fear |
| eotg_aug_tier1.004 | The Knight's Request | 29 | 5 | same beat as retinue.001 and .002 | merge with them, or differentiate |
| eotg_aug_tier3.002 | The Mirror | 20 | 5 ("Perfect.") | an abstract vignette | a witness, or a consequence |
| eotg_aug_tier3.003 | Sleepless | 23 | 6 | thin; ends on an aphorism | what the hours were spent on, and who noticed |
| eotg_aug_tier2.001 | Emotional Delay | 25 | 5 ("Good.") | "someone said something" | a named person and the real moment |
| eotg_aug_tier1.001 | Phantom Sensation | 30 | 5 | generic | a concrete sensation, a court moment |
| eotg_aug_patron.007 | A New Envoy | 31 | 3 | the fifth envoy opening | the envoy's character; a hint of the last one's fate |
| eotg_aug_end.011 | The Empty Hall | 30–32 | 3 | terse options | name one departure that hurts |

Fine as short beats (toast-like): proc.004, end.010, end.042, fracture.0001, tier1.017. Only their
"Continue." could be in-voice.

## Similarity clusters
1. **Procedure outcome lines.** proc.002 and tier1.022 share 5 outcome lines verbatim, and their bodies
   near-duplicate each other. init.011's desc_discovered echoes "Word has got out…".
2. **Hardware grades.** int.002 and realm.001 share the grade lines (Jaccard 0.56). act.001 and act.003
   reuse "Your law prohibits augmentation…".
3. **A volunteer asks for implants.** tier1.004, retinue.001 and retinue.002 are the same beat three times.
4. **Inquiry verdicts.** tier3.018 and fracture.020 have the same chain shape.
5. **Envoy invoices.** patron.002–.007: five of them open "The envoy (from X)…".
6. **The provider menu.** proc.001/.003/.005, tamper.004, tier1.002 and init.018 all offer "The clinic." /
   "My own physician." / "Someone cheaper." / "Not yet.".
7. **Trait-pair templates.**
   - honest/deceitful: fracture.005, fracture.015, tier1.003, tier2.009;
   - paranoid/trusting: fracture.012, fracture.019, tier2.012;
   - brave/craven: tier3.005, tier3.023.
   Paranoid gates 29 options in total.
8. **"Half a second before you."** fracture.010/.017/.022/.026/.027, tier1.017, tier2.003/.020 and tier3.012/.022.

## Stock phrases (count of events)
"No one …" 32 · "the hardware" 26 · "the work" (as surgery) 25 · "the body" as subject 20 · quiet/quietly 19 ·
"half a second" 10 · "X has come to…" 9 · "It is not …" 8 · "Word has got out/spread" 5 ·
"you do not remember" 5 · "the readings stutter/drift" 5.

Repeated options: "Ignore it." 7 · "Not yet." 7 · "My own physician." 7 · "Refuse." 6 · "Continue." 4 · "No." 4 ·
"Arrest X." 4 · "Execute X." 4 · "The clinic." 4 · "Someone cheaper." 4 · "The moment has passed." 3 · "Good." 3.

Openings: 30 desc variants start "X has…", 11 start "The implant…" and 10 start "The hardware…".

## Caveats
- Option names set inside `text = { first_valid }` blocks were not resolved and count as 0 words, so the
  average option length is slightly understated.
- Option counts include trait-gated options a player may not see. Ungated options average 1.94 per event
  against vanilla's 1.59.
