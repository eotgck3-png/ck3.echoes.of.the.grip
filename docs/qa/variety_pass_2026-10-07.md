# Cybernetics writing variety pass (event-writing review, tier 2), 2026-10-07

**Branch:** `claude/cyber-variety-cloud` (from `v2-space-map` @ `d6805f6`). **Text only:** `localization/english/eotg_augmentation_l_english.yml`, **190 keys reworded**, no keys added or removed, no `.txt` touched. The 20 events rewritten in `b3371a0` (the review's ranked rewrite table) are untouched, and every count below separates them out.

**Static, unvalidated:** written in a cloud session without the game. Every changed option was checked against its option block in `events/eotg_augmentation_*.txt` (effects and trait gate), and every changed desc keeps the facts of the line it replaced, so it stays true on the paths that showed the old line.

## How the counts were taken

- **Scope:** every key of a cybernetics event (`eotg_aug_<group>.NNN…` and `eotg_fracture.NNN…`) in `eotg_augmentation_l_english.yml`, titles (`.t`) excluded. **All** = every such event; **in scope** = without the 20 excluded events.
- **Phrases:** case-insensitive regexes, counted as occurrences, with the number of distinct events in brackets. `"the work"` counts every "the work" (all of them were surgery or a job); `"the body"` counts every "the body".
- **Openings:** desc variants (keys `…desc*`, a leading `\n\n` ignored). **"X has…"** = the desc opens with a named placeholder followed by "has" (`[x.GetFirstName] has…`, `[x.GetName], your spymaster, has…`), which reproduces the review's figure (29 against its 30). The broader "any subject of up to three words + has" count is also given.
- **Options:** exact text of option keys.
- The review's own numbers ("No one" 32, "the hardware" 26 …) counted events, across a slightly different key set; the *before* column here is measured on `d6805f6` with this script, so before and after are like for like.

## Stock phrases

| Phrase | Before, all | After, all | Before, in scope | After, in scope |
|---|---|---|---|---|
| "No one…" | 35 (28) | 7 (5) | 31 (26) | 3 (3) |
| "the hardware" | 36 (24) | 1 (1) | 35 (23) | 0 (0) |
| "the work" (surgery) | 19 (14) | 0 (0) | 19 (14) | 0 (0) |
| "the body" (subject) | 20 (17) | 3 (3) | 18 (15) | 1 (1) |
| quiet/quietly | 32 (21) | 9 (7) | 25 (15) | 2 (1) |
| "half a second" | 11 (10) | 4 (4) | 11 (10) | 4 (4) |
| "X has come to…" | 10 (10) | 3 (3) | 7 (7) | 0 (0) |
| "It is not…" | 9 (7) | 4 (2) | 8 (6) | 3 (1) |
| "Word has got out/spread" | 2 (2) | 1 (1) | 1 (1) | 0 (0) |
| "you do not remember" | 4 (4) | 2 (2) | 4 (4) | 2 (2) |
| "the readings stutter/drift" | 2 (2) | 2 (2) | 1 (1) | 1 (1) |

## Openings (desc variants)

| Opening | Before, all | After, all | Before, in scope | After, in scope |
|---|---|---|---|---|
| X has… | 29 | 5 | 24 | 0 |
| The implant… | 13 | 1 | 12 | 0 |
| The hardware… | 8 | 0 | 8 | 0 |
| (broad) any subject + has | 60 | 35 | 49 | 24 |

No opening pattern now starts more than 8 descs. The 5 remaining "X has…" openings are all in the excluded events.

## Repeated options

| Option text | Before, all | After, all | Before, in scope | After, in scope |
|---|---|---|---|---|
| Ignore it. | 7 | 1 | 6 | 0 |
| Not yet. | 7 | 5 | 6 | 4 |
| My own physician. | 7 | 7 | 7 | 7 |
| Refuse. | 6 | 0 | 6 | 0 |
| Continue. | 4 | 0 | 4 | 0 |
| No. | 4 | 0 | 4 | 0 |
| Good. | 3 | 1 | 2 | 0 |
| The clinic. | 4 | 4 | 4 | 4 |
| Someone cheaper. | 4 | 4 | 4 | 4 |
| The moment has passed. | 0 | 0 | 0 | 0 |

- **The provider menu stays verbatim** ("The clinic." / "My own physician." / "Someone cheaper." / "Not yet." in tier1.002, init.018, proc.001, proc.003, proc.005, tamper.004 and tier2.003): the brief's exception allows it, and keeping it identical keeps it recognizable. In scope, the remaining "Not yet." (4) and "My own physician." (7) are all menu entries; the fifth "Not yet." is `eotg_aug_retinue.001.b`, in an excluded event. Every non-menu "Not yet." (init.017.b, fracture.027.d) has its own text now.
- The remaining "Ignore it." and "Good." are in excluded events.

## Replacement crutches checked

Words the rewrite leaned on, counted over all cybernetics events. "the implants" first rose from 8 to 18; a second pass varied it back down.

| Word | Before | After |
|---|---|---|
| the implants | 8 | 10 |
| flesh | 10 | 13 |
| tissue | 7 | 11 |
| casing(s) | 11 | 16 |
| a beat | 1 | 3 |
| nobody | 20 | 19 |
| parts | 2 | 7 |
| procedure | 1 | 4 |

No changed line repeats another changed line's text.

## Lines left alone on purpose

- `eotg_aug_end.010.desc`: "There is no voice now. There is no one left for it to speak to." is the Seamless voice-5 line fixed by `cybernetics_v2.md` §5 item 8.
- `eotg_aug_end.009.desc`: "afterward there is no one left to make another": the terms of Hand Over the Controls. That no one is left is the point of the event.
- `eotg_aug_end.041.desc`: "reporting to a room with no one in it": the resigner's complaint is the event.
- `eotg_aug_end.042.desc`: "the body turns toward the door": Seamless, after the self is gone. "the body" is deliberate there (its "No one is there" was changed).
- `eotg_aug_tier2.020.desc`: "half a second early": The Second Self introduces the voice, the canon forecast. Its "It is not another person" was changed.
- `eotg_aug_tier3.012.desc_first`: "half a second": First Contact, the voice's first request (its "You do not remember" was changed).
- `eotg_fracture.022.desc_first`: "half a second": the 'we' pronoun arrives ahead of the choice; the forecast is the content.
- `eotg_fracture.027.desc_voice01`: "half a second early is arriving earlier now: a full second, then three": the Cascade is the forecast's lead running away.
- `eotg_aug_end.002.a / .c`: "It's quiet." / "Quiet. At last." in *Silence* (after Excision): the word is the event's subject. Its desc lost its "It is quiet."
- `eotg_fracture.015.b.reveal_*`: "It is not the letter you read." ×3: three parallel outcome toasts, of which only one ever shows; the refrain is deliberate.
- `eotg_aug_tier3.009.desc`: "You do not remember giving it": the premise of Phantom Orders.
- `eotg_fracture.027.desc_premonition`: "What you do not remember is the ending": the forecast-stored-as-memory canon (§5 item 2).
- `eotg_aug_tier1.022.desc_complication`: "the readings stutter": only one in scope; the review's cluster was proc.002 (excluded).
- `Provider menu`: See above.

## Fixed in passing (lines that were being changed anyway)

- Banned words: "dawn" (tamper.002.desc), "tick" (act.006.desc_hot), "By morning" (fracture.026.a.success); "night" removed from fracture.026.desc.
- Singular they for one unscoped person: tier3.004.desc ("their chair"), tier2.006.desc ("their replacement"), patron.001.desc (the envoy, "They bring"), init.002.desc (the representative, "They call it"), fracture.023.desc_war (the envoy, "They are confused"), fracture.021.desc ("no one will say they saw").
- Body-location: tier3.001.desc ("The body was already moving" → you).

## Keys changed, by event

- **act.001**: `desc`, `desc_many`, `e`
- **act.002**: `desc`, `desc_physical`, `desc_hot`, `e`
- **act.003**: `desc`, `c.hot`, `c.clean`, `c.tt`
- **act.005**: `desc`
- **act.006**: `desc_hot`
- **countdown.001**: `c`
- **countdown.005**: `a`
- **countdown.006**: `desc`
- **end.001**: `desc`, `desc_odds_poor`, `desc_free`
- **end.002**: `desc`, `desc_maimed`
- **end.010**: `a`
- **end.020**: `e`
- **end.031**: `d`, `a.success`
- **end.041**: `c.leaves`
- **end.042**: `desc`, `a`
- **fracture.002**: `desc`, `desc_none`
- **fracture.003**: `desc`
- **fracture.006**: `desc_faction`, `desc_circulated`
- **fracture.009**: `desc`
- **fracture.010**: `desc_voice01`
- **fracture.013**: `desc`, `c`
- **fracture.014**: `desc`
- **fracture.017**: `desc_voice01`, `desc_voice3`
- **fracture.018**: `d`
- **fracture.019**: `desc`
- **fracture.021**: `desc`, `e`
- **fracture.022**: `desc`
- **fracture.023**: `desc_peace`, `desc_war`
- **fracture.024**: `desc`
- **fracture.025**: `desc`, `b`
- **fracture.026**: `desc`, `desc_voice01`, `desc_voice3`, `a.success`
- **fracture.027**: `d`
- **fracture.029**: `desc`, `desc_embrace`, `desc_none`
- **heir.001**: `desc_overclocked`, `desc_patient`
- **heir.003**: `desc`, `desc_successor`
- **heir.004**: `desc`, `desc_ally`, `desc_silent`, `silent_a`, `desc_successor`
- **heir.005**: `desc`
- **init.002**: `desc`, `a`
- **init.006**: `desc_former`
- **init.008**: `desc_success`
- **init.009**: `desc`, `desc_zealot`
- **init.010**: `desc`, `c`, `a.success`, `a.failure`
- **init.011**: `desc_rejection`, `desc_discovered`, `a`, `d.tt`, `desc_one_eyed`
- **init.014**: `desc`
- **init.015**: `desc`, `d`
- **init.017**: `desc`, `b`
- **int.001**: `desc_fractured`
- **int.002**: `desc`, `desc_died`, `desc_maimed`
- **nr.001**: `desc`
- **nr.002**: `desc`, `desc_enhanced`, `desc_overclocked`
- **nr.003**: `desc`, `b`, `c`
- **nr.005**: `desc`
- **nr.006**: `b.survive`
- **patron.001**: `desc`
- **patron.002**: `desc`, `b`
- **patron.003**: `desc`, `b`
- **patron.004**: `b`
- **patron.006**: `desc_writeoff_absent`
- **patron.008**: `desc`
- **patron.009**: `desc`, `c`
- **proc.001**: `desc`, `desc_full`, `desc_physician`, `tt`
- **proc.003**: `desc`, `desc_physician`
- **proc.004**: `desc`, `a`
- **proc.005**: `desc`, `desc_overclocked`
- **proc.020**: `desc`, `desc_rejected`
- **realm.001**: `desc_nf`
- **retinue.003**: `desc`, `b`
- **retinue.005**: `a`
- **tamper.002**: `desc`, `desc_fractured`, `a`
- **tamper.004**: `desc`, `desc_nf`
- **tier1.006**: `desc`
- **tier1.007**: `desc`
- **tier1.010**: `desc`, `g`
- **tier1.012**: `desc`, `desc_conscience`, `b`, `e`
- **tier1.013**: `desc`
- **tier1.015**: `desc`, `desc_failed`, `desc_scarred`
- **tier1.016**: `desc`, `b`
- **tier1.017**: `desc`
- **tier1.018**: `desc`, `b`, `c.success`, `c.failure`
- **tier1.022**: `desc`, `desc_rejection`
- **tier2.003**: `desc_nerves`, `desc_voice`
- **tier2.004**: `desc`
- **tier2.005**: `desc`
- **tier2.006**: `desc`
- **tier2.007**: `desc`
- **tier2.009**: `desc`
- **tier2.011**: `desc`, `b`
- **tier2.012**: `desc`, `a`, `c`, `a.success`
- **tier2.015**: `desc`
- **tier2.017**: `desc`, `e`
- **tier2.019**: `desc`, `b`, `c.success`
- **tier2.020**: `desc`
- **tier3.001**: `desc`, `desc_none`
- **tier3.004**: `desc`, `desc_none`
- **tier3.008**: `desc`
- **tier3.012**: `desc_first`, `b`
- **tier3.015**: `desc_alliance`, `desc_rivalry`
- **tier3.017**: `desc`, `d`
- **tier3.019**: `b.success`
- **tier3.020**: `desc`, `b`
- **tier3.021**: `desc`
- **tier3.022**: `desc_scarring`, `desc_insight`

(190 keys in 102 events.) The before and after text of each is in the commit diff: `git show cc9d61e -- localization/english/eotg_augmentation_l_english.yml`.

## Self-check (run on every changed line)

The script checks:
- the banned list: feedback §3, r2 "Global rules", the brief's additions (station, breach, mortal, registry, magistrate, whispers, citizen, human, royal), and the voice and Neurofractured list in `cybernetics_v2.md` §5;
- that no `[scope:` form is used;
- that no embedded double quote is used;
- that `\n\n` openers match the old line;
- that descs are at most 80 words;
- that every placeholder scope already appears in that event's loc;
- and it lists every they/them/their for a manual read.

```
changed lines checked: 190
  eotg_aug_act.001.e                            THEY?      them
  eotg_aug_act.002.desc_hot                     THEY?      They
  eotg_aug_act.002.desc_physical                THEY?      their
  eotg_aug_act.006.desc_hot                     THEY?      they
  eotg_aug_countdown.005.a                      THEY?      them
  eotg_aug_countdown.005.a                      THEY?      their
  eotg_aug_end.001.desc                         THEY?      They
  eotg_aug_end.001.desc                         THEY?      them
  eotg_aug_end.001.desc                         THEY?      them
  eotg_aug_end.001.desc                         THEY?      them
  eotg_aug_end.002.desc_maimed                  THEY?      they
  eotg_aug_heir.001.desc_patient                THEY?      they
  eotg_aug_init.006.desc_former                 THEY?      them
  eotg_aug_init.009.desc_zealot                 THEY?      They
  eotg_aug_init.010.a.failure                   THEY?      they
  eotg_aug_init.010.desc                        THEY?      They
  eotg_aug_init.010.desc                        THEY?      they
  eotg_aug_init.010.desc                        THEY?      they
  eotg_aug_init.010.desc                        THEY?      their
  eotg_aug_init.014.desc                        THEY?      them
  eotg_aug_init.015.desc                        THEY?      They
  eotg_aug_nr.001.desc                          THEY?      them
  eotg_aug_nr.002.desc                          THEY?      their
  eotg_aug_patron.009.desc                      THEY?      them
  eotg_aug_patron.009.desc                      THEY?      them
  eotg_aug_proc.001.desc                        THEY?      they
  eotg_aug_proc.001.desc_full                   THEY?      them
  eotg_aug_proc.003.desc                        THEY?      them
  eotg_aug_proc.005.desc                        THEY?      their
  eotg_aug_proc.020.desc                        THEY?      them
  eotg_aug_retinue.003.b                        THEY?      them
  eotg_aug_retinue.003.desc                     THEY?      them
  eotg_aug_retinue.003.desc                     THEY?      they
  eotg_aug_retinue.003.desc                     THEY?      They
  eotg_aug_retinue.003.desc                     THEY?      they
  eotg_aug_retinue.003.desc                     THEY?      their
  eotg_aug_retinue.003.desc                     THEY?      them
  eotg_aug_retinue.005.a                        THEY?      They
  eotg_aug_tier1.006.desc                       THEY?      them
  eotg_aug_tier1.006.desc                       THEY?      they
  eotg_aug_tier2.004.desc                       THEY?      They
  eotg_aug_tier2.009.desc                       THEY?      their
  eotg_aug_tier3.020.b                          THEY?      they
  eotg_fracture.013.desc                        THEY?      they
  eotg_fracture.013.desc                        THEY?      their
  eotg_fracture.023.desc_war                    THEY?      their
findings: 46
```

**Result:** 0 banned words, 0 scope-form, 0 quotes, 0 opener mismatches, 0 over 80 words, 0 new scopes. The 46 they/them/their lines were each read by hand, and every one has a plural referent: surgeons, the gang, entrants, casings, parts, heat sinks, the Ranks, the court, soldiers, implants, stairs, other people, the enemy. The two shipped lines of that kind kept from the old text are fracture.013.desc ("what they did with their hands", the people in the remembered conversation) and fracture.023.desc_war ("their surrender", the enemy side). `eotg_lint` L011 (one named character as they) reports 0 new.

## Validation

- `eotg_lint` vs baseline: 0 findings, 0 new.
- Unit tests: OK (222).
- `check_all`: 14 pass, 0 fail, 7 skipped (Tiger, PX and the game are local-only).
- The yml has exactly one BOM and LF line endings, as before; written through `docs/tools/textio.py`.
