# W9 patron letters: localizer worklist

Source: `docs/specs/event_quality_v1.md` W9 (REWRITE and NEW halves, owner-approved Q2 2026-10-09), §12.1 rule 5 (second person allowed in letters), §12.3 example 6 (letter opening), §12.5 (Seamless). Script half landed 2026-10-09 (eotg-scripter).
Loc file: `localization/english/eotg_augmentation_l_english.yml`. `replace/`: none.

## What the script did

- **New event `eotg_aug_patron.010` *The Final Account*.** The Final Demand (.006) as the syndicate's **unsigned** note: `type = character_event`, `window = anonymous_letter_event` (vanilla `ep3_contract_events.txt:8596-8600`), `opening = { desc = … }` (vanilla `bp2_hostage_system.txt:677`). There is no sender, because the syndicate signs nothing and the anonymous window has no sender portrait (`_events.info:18`). The story tick now fires .010 instead of .006 when the envoy is dead or has left court. Its options are .006 a, b, d and f, with unchanged mechanics, and they **reuse .006's option keys**.
- **patron.006** keeps its three `*_absent` descs and option f as the in-flight fallback, for an envoy who dies or leaves in the 1–30 days between the tick and the event. The fallback is a character event, so the narration is first person (§12.1 rule 1), not a letter.
- **patron.008 and patron.009 stay character events.** The spec's conditions for converting them are not met: .008 fires only while the envoy is at court, and .009's collector arrives in person. Their keys are unchanged.

## Voice for the letter (.010)

- The body is the syndicate writing to the ruler: second person to the reader ("you", "your") and the syndicate as "we" or "us" (§12.1 rule 5, the R1 5% bucket). This corporate "we" is the sender's. It is not the forecast "we" of rule 6, which remains banned as a new line.
- It is unsigned. Don't name a person or sign off. The syndicate's name may appear only through `[ROOT.Char.Custom('eotg_aug_cl_syndicate')]`, and it is optional here because the letter speaks as "we".
- The register is the envoy's: polite, unhurried, final. Follow the house rules: no dashes, Canadian English, no Helix, Pale Hand, white-glove imagery or authorities (file header, CB-42).
- No narration. Nothing like "the message arrives sealed" goes in a letter body, because the window already is the letter.
- `[x.GetName]` bare form only.

## New keys (5)

| # | Key | Draft / intent | Notes |
|---|---|---|---|
| 1 | `eotg_aug_patron.010.t` | "The Final Account" | The anonymous window does not draw the title (vanilla uses a debug title); it still shows in the event log. |
| 2 | `eotg_aug_patron.010.opening` | "[ROOT.Char.GetFirstName], the account is closed." | From §12.3 example 6, first sentence. It must fit all three bodies, and all three close the account. |
| 3 | `eotg_aug_patron.010.desc_writeoff` | Intent of `.006.desc_writeoff_absent` as the letter body: "We have reviewed your account. We do not service broken units, and the hardware in you no longer meets our terms. What you owe is due now." | Shown when the owner is Neurofractured (write-off flag). Don't say "Neurofractured". "Broken units" is the shipped phrase. |
| 4 | `eotg_aug_patron.010.desc_betrayal` | Intent of `.006.desc_betrayal`: "We have kept a ledger of your refusals, and it is closed. These terms are final. We were never buying the implant. We were buying you, and you have stopped being for sale." | Grievance 3+. Keep the shipped line "We were never buying the implant…", now as the letter's own words with no quote marks. |
| 5 | `eotg_aug_patron.010.desc_settlement` | Intent of `.006.desc_settlement_absent`: "Your account is closed on our side, and we would like to settle. The terms enclosed are generous. Settle them, and you will not hear from us again." | Demand 4+. The second clause is from §12.3 example 6. "You will not hear from us again" is literally untrue after options d (failure) and f for an owner with no implants, where the paper is sold and the collector comes (.009). That irony is intended. If lore objects, drop the clause. |

Read each body against the four options shown: .006.a "Sign over the revenues.", .006.b "Buy them out.", .006.d "Sell them to [rival].", .006.f "Burn the terms. Send no answer." All four answer a letter, and f is now always visible there.

## Changed keys: patron.006 fallback narration (3)

These were left in second person by B8 for W9 (`b8_samples.md:34`). They now show only when the envoy is lost in flight. Convert them to first person (§12.1 rules 1 and 13: every desc key carries I, me or my). Keep the facts.

| # | Key | Today | Target |
|---|---|---|---|
| 6 | `eotg_aug_patron.006.desc_betrayal_absent` | "…a ledger of your refusals… They were buying you, and you have stopped being for sale." | "The message comes without the usual courtesy, sealed and unsigned. [ROOT.Char.Custom('eotg_aug_cl_syndicate')\|U] has kept a ledger of my refusals, and it is closed. The terms are final and written without heat: they were never buying the implant. They were buying me, and I have stopped being for sale." |
| 7 | `eotg_aug_patron.006.desc_writeoff_absent` | "…reviewed your account… what you owe is due now." | "The message arrives sealed, with no courier waiting for an answer. [ROOT.Char.Custom('eotg_aug_cl_syndicate')\|U] has reviewed my account and closed it. The terms are brief: the syndicate does not service broken units, and what I owe is due now." |
| 8 | `eotg_aug_patron.006.desc_settlement_absent` | Neutral, with no I, me or my (fails rule 13) | "A courier brings me the final account, sealed. [ROOT.Char.Custom('eotg_aug_cl_syndicate')\|U] has closed it on its side, and would like to settle with me. The terms are generous and the tone is relaxed, like that of someone who has already collected what they came for." |

(`\|U` in the table is a Markdown escape; the loc line is `|U`.)

## Reused, unchanged (listed so nobody duplicates them)

`eotg_aug_patron.006.a`, `.b`, `.d`, `.d.success`, `.d.failure`, `.f`, `.toast_d_success`, `.toast_d_failure`; `eotg_aug_patron_paper_sold_tt` (through `eotg_aug_patron_betray_effect`). Every patron.008 and patron.009 key is unchanged.

## Checks after writing

- `\byou\b` appears in keys 6–8 only inside quoted speech (there is none).
- Keys 2–5: there is no I, me or my, and the sender is "we" or "us".
- UTF-8 with BOM, one definition per key.
