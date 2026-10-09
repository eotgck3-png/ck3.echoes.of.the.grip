# B12 loc worklist: Frontier (`events/eotg_frontier_events.txt`)

Event quality P3, batch B12 (`docs/specs/event_quality_v1.md` §13.3). The script half is done. This list is for eotg-localizer. Loc file: `localization/english/eotg_frontier_l_english.yml`.

## Script changes that affect text

- **W5 (re-gating): no change.** No option in the file is gated on a root personality trait (0 before, 0 after). The only gated options are two skill checks: 001.f (`learning`) and 032.c (`diplomacy`). With 2 gated options, the file is below the §13.1 step 6 threshold of 5, so no education or tier gate is needed. **No option is reframed, and no option key needs new text.**
- **W6 (portraits):** `triggered_animation` reactions were added to root's portrait in all 19 visible events, plus explicit-scope reactions on six right portraits (003, 030, 031, 033, 040, 041). These are portrait-only and need no loc.

## L018: time-of-day words (must fix)

A galaxy has no shared clock (§8, GQF-002). Change only the time word; keep the rest of the sentence.

| Key | Current | The replacement must stay true to |
|---|---|---|
| `eotg_frontier.004.desc_military` | "...the approaches to the Region are watched day and night." | Shown at completion for a Military project (desc variant after `.004.desc`). It says the garrison is permanent and the approaches are watched **without a break**. Use a clock-free phrase such as "watched without a break" or "watched every hour of every shift". Don't use "around the clock" (it implies a planetary day). Keep the leading `\n\n`. |
| `eotg_frontier.036.desc` | "The crew chief wants to start cutting tomorrow." | A Rich Seam. The tension is **speed against knowledge**: the crew chief wants to cut **at once**, and the surveyors want to know how far the seam runs first. Options: a "Survey it properly first." (costs gold, reveals the Rich Resources trait, +2 progress) and b "Start cutting. We need it now." (+4 progress, plus strain). Use "at once", "on the next shift" or "before the survey is done". The urgency must survive, because option b depends on it. |

## W1: second person in desc keys (rule 13 grep)

`\byou\b|\byour\b` in this batch's event desc keys, outside quoted speech. Root narrates, so change you/your to I/me/my/mine and keep everything else.

| Key | Phrase(s) | Note |
|---|---|---|
| `eotg_frontier.001.desc_self` | "You have looked over the surveys yourself" | → "I have looked over the surveys myself". "we build first" stays (rule 6: the ruler's own "we"). Shown only when root is the founder. |
| `eotg_frontier.010.desc` | "Whichever you choose ... take your money" | → I / my. |
| `eotg_frontier.031.desc` | "The Region is yours, under your law" | → "mine, under my law". LAW AT 866 must stay explicit: the backing never came with a say. |
| `eotg_frontier.032.desc_liege` | "As your liege" | → "As my liege". Shown only when root has a liege. |
| `eotg_frontier.033.desc` | "waiting to hear from you" | → "from me". |
| `eotg_frontier.041.desc_head` | "who leads your faith", "the Region stays yours" | → my / mine. Stay faith-neutral, and keep "no claim, no say, no authority". |
| `eotg_frontier.041.desc_order` | "a holy order of your faith", "the Region stays yours" | Same as desc_head. |

**Keep as they are (rule 5):**
- `eotg_frontier.031.a` ("Your money buys no say in it."): root is speaking to the sponsor.
- The short tooltip `eotg_frontier.037.a_tt` ("bring you some renown") is allowed. First person is preferred.
- Decision and modifier keys are out of W1 scope. They follow the vanilla decision-UI voice.

## Checks for the localizer

- Read each change against every desc variant the event can show. For example, 004's type variants are combined with `desc_built_much`, `desc_studied` and `desc_hard_won`.
- Re-run `python docs/tools/eotg_lint.py --baseline docs/tools/eotg_lint_baseline.json`. L018 should drop to 0.
