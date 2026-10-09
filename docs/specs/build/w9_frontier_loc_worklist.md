# W9 frontier letters: loc worklist (eotg-localizer)

Source: `docs/specs/event_quality_v1.md` W9 (REWRITE half). Script: `events/eotg_frontier_events.txt`, eotg_frontier.003 and .030, now `type = letter_event` (eotg-scripter, 2026-10-09, uncommitted).
File: `localization/english/eotg_frontier_l_english.yml` (UTF-8 BOM). Canadian English, no dashes, bare `[x.GetName]`, speech in vanilla double quotes.

**Voice (§12.1 R1 rule 5):** a letter is written by the sender to the ruler, so second person ("you") is allowed in the opening and the desc. The B12 first-person text (commit 5ffab0c) narrates the offer from root's side. It must become the sender's own letter. The sender's portrait is the only one shown. The ruler's name in the letter is `[ROOT.Char.GetFirstName]` or `[ROOT.Char.GetTitledFirstName]`.

## New keys

| Key | Sender | Must convey |
|---|---|---|
| `eotg_frontier.003.opening` | `eotg_frontier_sponsor` | The salutation line of a letter from the prospective backer to the ruler, e.g. addressing `[ROOT.Char.GetTitledFirstName]`. One short line, like vanilla `*.opening` keys. No offer content here. |
| `eotg_frontier.030.opening` | `eotg_frontier_rival` | The salutation line of a letter from the rival backer to the ruler. One short line. It may hint at a business proposal but must not name the current backer. |

## Existing keys to rewrite (same key, new text in the sender's voice)

| Key | Facts that must survive |
|---|---|
| `eotg_frontier.003.desc` | The sender has heard of the work in `[eotg_frontier_county.GetName]`. They offer regular shipments of money and supplies for as long as the Frontier needs them. No claim is attached. They share the credit if it succeeds and the loss if it fails (keep this as the sender's own words; it is no longer reported speech, so drop the "says" frame). |
| `eotg_frontier.003.desc_replace` | Appended paragraph, shown when the Frontier already has a backer. The sender acknowledges the Frontier already has one, and that accepting would end that arrangement. Starts with `\n\n`. |
| `eotg_frontier.030.desc` | The sender has watched the work in `[eotg_frontier_county.GetName]`. They offer better terms than `[eotg_frontier_sponsor.GetFirstName]`: the first shipment at once, then yearly on the same schedule. Accepting ends the arrangement with `[eotg_frontier_sponsor.GetFirstName]`, who will not take it kindly. Neither backer gains a claim on the Region either way (LAW AT 866; the sender can state it as a reassurance). |

## Unchanged
`.t`, the option names (`.003.a/.b`, `.030.a/.b`) and the tooltips (`.003.accept_tt`, `.003.refuse_tt`, `.030.a_tt`) stay as they are: options are root's replies. `.t` is kept in script though the letter window shows no title (vanilla letter events carry none).
