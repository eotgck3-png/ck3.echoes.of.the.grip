# Owner decisions: researched answers (2026-11-03)

Every open mechanics decision, each with a suggested answer. Five research tracks compared each question with vanilla CK3 1.20.1.1 (the precedent, cited file:line in the track files) and with the overhaul mods installed on this machine: Elder Kings 2, LotR: Realms in Exile, Godherja, A Game of Thrones, After the End (+ Sci-Fi) and The Fallen Eagle. **The mods are technique only.** No answer rests on a mod (project rule). Where a number matters, it was checked with the repo's sim (`docs/tools/sim/`, plus the what-if drivers in `docs/tools/sim/whatif/`, seed 20261103).

**How to answer:** reply "accept all", or list item IDs with your call. Nothing here is applied yet. Canon and vault questions are listed at the end and not answered.

Track files (full evidence for each item):
- [A: PMC and Cartel](A_pmc_cartel.md)
- [B: Corporation and Trade Oligarchy](B_corp_trade.md)
- [C: Void and cybernetics](C_void_cyber.md)
- [D: Grip Legacies](D_legacies.md)
- [E: Races](E_races.md)

Confidence: **H** high, **M** medium, **L** low.

---

## 1. Take now: high confidence, small value changes

| ID | Decision | Suggested answer | Conf. | Vanilla basis |
|---|---|---|---|---|
| A-P5 | Cartel succession grace | **3 → 5 years** (walk-offs after succession 0.436 → 0.218). An heir needs about 53 months to rebuild dread 20 | H | timed tribute protection, `tributary_has_been_reasserted_recently` |
| B-P1 | Court the Board erosion | **−5 → −2**, keeping both once-a-year caps. Runs stuck at 0 go from 52% to 0%. Two loc lines | H | `minor_unity_loss`, the clan-unity yearly step |
| C-V1 | Void Touched events almost never fire | **Option A: the 0010/0011 cooldown 5 → 2 years.** Stage C goes 0.038 → 0.238 per 100 seat-years; Touched stays about 4 years | H | stress keeps a separate cooldown per level |
| C-CD | Cooldown timing (with V1) | Write Void cooldowns one day short, `days = 729`, not `years = 2`. Otherwise a cooldown can still be live on the pulse day, and 2 years behaves like 3 | M | stress cooldown 1824 days, `00_stress_values.txt:77` |
| C-P4 | Lower the Overclocked gate to 15? | **No, hold at 20.** 15 equals the Enhanced gate and raises cascade deaths by half. If you want more Overclocked, use 18 | H | — |

## 2. Government design calls

| ID | Decision | Suggested answer | Conf. |
|---|---|---|---|
| A-P2 | PMC Standing grows with vassal count | **A once-a-year cap per liege on Deliver Results, keeping +5.** No value cut: 16 AI vassals settle at 59.8, inside the spec's own 40–70 band. Vanilla caps the total, not each share (dynasty prestige: 0.02 a month each, capped at 2) | M-H |
| A-flag | Cartel Lean on the Locals also gives the liege an uncapped +5 | The same cap, as a lower-priority follow-up | M |
| A-P6 | PMC contract pay | **`(standing / 50 + 0.5) × medium_gold_value`, `min = 50`.** Vanilla pays contracts 50 × the employer's tier. Today's flat formula overpays counts and underpays kings. Not simulated | M |
| A-OQ1–9 | PMC owner questions | Accept as specced: 75% inheritance, Recruit sink, visible story, starts 40/20, AI adoption off until V-G11. Defer PMC → Corporation, but fix its shape now (standing ≥ 60, 200 prestige, board influence = 20 + 0.5 × standing). No events yet | H/M |
| B-TO | Princes out-share the First Prince (55–57 vs 23–28) | **Half feature, half bug.** A Prince stronger than the ruler is fine; vanilla elections weight that. The gap is driven by how often the First Prince fights. **Fix with "charter dues":** while at least one partner Prince is at peace, the First Prince loses 2, not 4, per war year. The AI First Prince then settles at 45–50 against partners at 57–59, and the result is the same with 1 or 16 partners. Reject P3 | M |
| B-TO-OQ9 | Seat electors by market share? | **Yes (reverses the spec default),** with gold as the tie-break. Vanilla seats electors by whatever the election measures | M |
| B-CO-OQ10 | Corporation needs a Port capital? | **No.** A castle capital is valid under the Corporation's holdings | H |
| B-TO-OQ11 | Trade Oligarchy diplomacy −1 → +1 | **Yes** (no vanilla precedent for a skill modifier on a government; design call) | M |
| B-rest | Remaining Corporation and Trade Oligarchy OQs | Accept as built, including both once-a-year caps (Corporation OQ3, Trade Oligarchy OQ10). Events deferred; build Corporation E3 and Trade Oligarchy E4 first when you open them | H |

## 3. Void Corruption (CB-65)

| ID | Decision | Suggested answer | Conf. |
|---|---|---|---|
| C-Q1 | Mod-exclusive? | **Yes.** It has no map, faith or title keys | H |
| C-Q2 | How a Void cult is keyed, mechanically | **A parameter `eotg_void_cult` granted by a mod tenet, read as `rite = { rite_has_parameter = eotg_void_cult }`.** In 1.20 tenets sit on rites, and vanilla's witchcraft gate does the same. The lift plan's `has_doctrine = tenet_*` form is wrong for 1.20. Needs `common/religion/tenet_types/` added to CLAUDE.md placement | H |
| C-Q4 | Do the devout dislike a Voidwalker? | **Yes, mildly:** zealous −10 and piety costs (vanilla zealous −10; a known witch −15). Later make it faith-dependent with CB-12 | M |
| C-Q5 | Contact rate | **4% for players; AI by tier, 2% kingdom+, 1% duchy, 0.5% county** (vanilla's AI `chance_of_no_event` 30/70/95). The flat 4/1 now in script is an acceptable fallback | M |
| C-Q6 | Stage-D end state | **Depth 100 adds `incapable` (a regent takes over) through a message, as vanilla dementia does**, and the stage-D roll skips incapable rulers. About 35% of the Hollowed reach it, a median of 19 years in. Fallback: the plateau | M |
| C-V2 | Voidwalkers too rare | **0004 chance 12% → 25%, together with V1.** Voidwalkers 0.50 → 0.97 per 100 seat-years; ever Hollowed 26.4% → 22.5% | M |

## 4. Grip Legacies (CB-67)

The research found three gaps in the cloud's Legacies sim (D §0). It fixes them in its own runs, and the numbers below are the corrected ones. The repo model `docs/tools/sim/models/legacies.py` still needs the same three fixes.

| ID | Decision | Suggested answer | Conf. |
|---|---|---|---|
| D-Q7 | Mod-exclusive? | **Yes**, with four guards: a map-key grep, testing on the British Isles test sub-mod plus harness cases, deferrals recorded on the taskboard, and the D-Q9 cap | H |
| D-Q4 | Exodus re-entry | **Drop the path now, with no stub.** On re-entry, the Exodus pulse calls the Legacies discovery effect at 10%, the way pilgrimages call `create_legend_seed` | H |
| D-Q8 | Integrity drain | **−1 a year on Extracted only** (vanilla artifacts: −1 a year in use, 0 on display). 16.9% of sites reach 0, at a median of 69 years | H |
| D-Q9 | Seeding density | **Keep 3%.** Add a **global cap at 6% of counties** (vanilla's `laamps_tally` pattern). Past the cap, an empty survey only gives the 0004 vignette. Don't halve 0002.a; that only cuts yield 5%. The real risk is AI surveys seeding new sites | M-H |
| D-Q10 | Rival-claim gate | **Gate 25, floor 25** (about 0.11 per site-century, landing on the roughly 7% of "loud" sites). Lower to gate 20 if you want more claims | M |
| D-0105 | Dynasty gate on 0105 | **Adopt it** (vanilla's own test, negated). Sealed ends at 34%; the remaining push towards Sealed is option 0105.c "reseal", which is your call | H |

## 5. Races

| ID | Decision | Suggested answer | Conf. |
|---|---|---|---|
| E-D1 | Half-races | **Default `as_own_race`.** Under `off`, canon's half-elven people (Old Xerxes) die out within a generation. A blend factor keeps your "% chance" rule: elf × human → half-elf 50%, elf 25%, human 25%. Heritage groups only for canon half-race peoples. **This conflicts with your earlier "races don't hybridize", so it's yours to rule** | M |
| E-D2 | Half-race fertility under a future `forbidden` | Fertile within a race family and across registered pairings; the pairing table is the compatibility table. Override `can_have_children_with`; never block marriage | M-H |
| E-D3 | Fertility default and race modifiers | **Keep `free`.** Put modifiers on the race traits within vanilla's bands: fertility ±0.2, health ±0.25, life expectancy ±10. Human 0; elf −0.2 fertility / +10 life expectancy / +5 fertile years; dwarf −0.1 / +0.25 health / +5; orc +0.1 / +0.25 / −5; ogre −0.2 / −0.25 health. The full table is in E | H (structure), L-M (values) |
| E-D4 | Race resource | **None new:** cultural acceptance is the race system's signature resource. Add `same_opinion = 10` to the race traits | M |
| E-D5 | Default race | **Human, and human heritages must carry `eotg_heritage_group_human`**; otherwise the hybrid block leaks | H |
| E-D6 | Race in the ruler designer | **Yes**, with vanilla-rate costs. Re-roll designer children from their parents after the lobby | M-H |
| E-D7 | Pairing order | Keep it, half-elf first | H |
| E-bug | Spec §8.1 sketch for `forbidden` | Ending a pregnancy in the same on_action leaves a stray `pregnant` trait. When it's built, fire a hidden event a day later and use vanilla's `end_pregnancy` + `pregnancy_cleanup_effect` | H |

---

## 6. Not answered here: canon and vault questions

- **Void:** who carries `eotg_grip_survivor`; who "the Marked" are; which of the Grip-Touched faith's three tenets gives way to the new Void tenet.
- **Legacies:** "Confluence" (renamed to "the Grip" by default); the fourth family's name (default Hellshard); whether a hell can keep an administration; the ERAS errata, the Grip at 0 AG (in the spec's amendment block, for you to approve).
- **Races** (E's closing list):
  - The kit's race list lacks the Half-Orcs in canon's playable list.
  - Half-giant parentage, and whether Zandrov exists at 866.
  - Old Xerxes: a half-elf culture, or a human-group culture of half-elves?
  - Is any race near-immortal?
  - Does any sub-race differ in body from its family?

## 7. Follow-ups whatever you decide

- Fix the three Legacies sim gaps in `docs/tools/sim/models/legacies.py` (D §0: S1 drain → 0104, S2 marker floor, S3 AI survey seeding).
- Add `common/religion/tenet_types/` to the CLAUDE.md file-placement list (C-Q2).
- The `proposed_tuning.patch` P6 hunk needs `min = 50` (A-P6). The V1 hunk is superseded by option A. P3 is superseded by charter dues.
