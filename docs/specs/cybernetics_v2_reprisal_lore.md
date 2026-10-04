# Lore review: cybernetics_v2_reprisal.md (binding for script and loc)

**eotg-lore-keeper, 2026-10-04.** Approved, with seven must-fix items (P1–P7). The mechanics hold:
- the reprisal is a person, a sum, a lien and agents;
- nothing acts at a distance;
- no authority sits above the polity;
- nothing exceeds CYBERNETICS AT 866.

## Must-fix
- **P1.** The §8 tone quote is the **Black Cogs Consortium's "Chains of Greed", 1130** (`docs/lore/Third era Nations.md:723-730`), not Blackstar.
  - Cite it as a post-866 tone model only.
  - Add "Black Cogs" and "Chains of Greed" to the never-name line.
  - "Enforcers" never reaches loc.
- **P2.** Two of the three `_absent` descs have no courier, so the §5.2 note is wrong. Option .006.f refuses the message, not a messenger: **"Burn the terms. Send no answer."**
- **P3.** `paper_sold_tt` never says "reach". The throttle is a local absence (servicing stopped).
- **P4.** .009.d is not an expulsion: **"There is no debt. We are done."** The collector chooses to stay.
- **P5.** .009.e.failure: the collector's people stop the seizure, and the collector stays.
- **P6.** Gendered pronouns for the collector. Plural "their people" (the crew) stays.
- **P7. .009.c is a sale of stock against the debt.** The paper came with a case of the syndicate's stock, made to this ruler's measure, and the ruler takes it at the paper's price.
  - **Never write:** "theirs", "the syndicate's again", "back in their hands", "on their schedule", "serviced by them", "under contract", "owned", "obedience", "loyalty", "bound", "leash", or anything about who holds the firmware.
  - Script comments follow the same rule.

## Rulings
- **Title:** *The Collector*.
- **Selling the debt fits 866.**
  - The collector *holds* the paper as property. Never "lawful", "rightful", "claim", "title to the debt", "bounty", "assigned", and nothing on the realm-lore apparatus list.
  - The collector is a local buyer (root culture and faith). No foreign or galactic framing.
- **Enforcement by vanilla murder scheme: approved.** In-world, the paper is worth more as an example than as a sum. Loc never says "murder".
- **Collector as a guest: approved.** Seizing a guest costs tyranny: that is the hospitality breach.
- **U1. Lien recipient:** holder-neutral, decided under the human's "proceed with recommendations". Revise `eotg_mod_aug_patron_clause_final_desc` to: "A permanent share of the revenues goes to whoever holds the paper, in exchange for the debt being closed. It is paid every month, and it will be paid for as long as there are revenues." The name "Syndicate Lien" stays.
- **QA grep additions:** `bounty|lawful|rightful|black cogs|chains of greed`, plus `\breach` over paper_sold_tt, .009.desc and the .d.tt / .e* keys.

## Renderings
The localizer may polish these. No numbers, and no "risk", "odds" or "chance". Appended lines start with `\n\n`.

**Patron option and tooltip**
- `eotg_aug_patron.006.f` "Burn the terms. Send no answer."
- `eotg_aug_patron_paper_sold_tt` "None of the syndicate's hardware is left in you to stop servicing. It will sell your paper to someone who collects in person."

**patron.009 *The Collector***
- `.t` "The Collector"
- `.desc` "The syndicate has sold your paper. [eotg_patron_collector.GetName] holds it now, and has come to your residence as a guest to say so. [eotg_patron_collector.GetSheHe|U] brings the original terms, and under them, in the syndicate's hand, an account of how you broke them. The paper came with a case of the syndicate's stock, made to your measure, and that has come too. [eotg_patron_collector.GetHerHis|U] people wait outside. No threat is spoken. [eotg_patron_collector.GetSheHe|U] names the sum, and then the alternatives."
- `.desc_envoy_dead` "\n\n[eotg_patron_collector.GetSheHe|U] asks after [eotg_patron_envoy.GetName] once, and does not ask again."
- Options:
  - `.a` "Pay what the paper says."
  - `.b` "Sign the lien on my revenues."
  - `.c` "Take the hardware against the debt."
  - `.d` "There is no debt. We are done."
  - `.d.tt` "[eotg_patron_collector.GetName] takes the answer without argument, and stays on as your guest. [eotg_patron_collector.GetHerHis|U] people are patient."
  - `.e` "Seize the collector, and the paper."
  - `.e.success` "[eotg_patron_collector.GetName] is taken before [eotg_patron_collector.GetHerHis] people can move. The paper burns."
  - `.e.failure` "[eotg_patron_collector.GetHerHis|U] people are at the door before your guards are. Nobody draws, and nobody is taken. [eotg_patron_collector.GetName] stays on as your guest, and keeps the paper."
