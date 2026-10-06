# Writing brief: Neurofractured Kingpin, variable description fragments (Gemini, round 1)

**For:** the external Gemini writing agent. **Date:** 2026-10-06.
**Deliver to:** `docs/proposals/kingpin_fragments_gemini_r1.md`, and nowhere else. **Never edit `.yml` or `.txt` files.**
The project's localizer applies your drafts after the lore-keeper and QA review them.

## 0. Read first (in this order)
1. `docs/proposals/gemini_rewrite_feedback_2026-10-06.md`, §2 (the setting), §3 (banned words and replacements), §4 (rules for the text). **All of it applies here.**
2. `docs/specs/cybernetics_v2_kingpin.md`: §5.2 (the four variation axes), §5.8 node table (what each event does), §7.1 (how fragments assemble), §7.3 (voice and register), §7.4 (banned words and fixed wordings for this chain), §8 (lore constraints).

If this brief and the spec disagree, the spec wins. Tell us where they disagree.

## 1. What this is
"The Neurofractured Kingpin" is an event chain. A criminal organization's leader near the player's capital goes Neurofractured: an implant failure that makes the person unstable. The **owner's main requirement** is that each organization feels different, not copy-pasted. Key event descriptions are therefore **built from 2–3 independent fragments**, one per variation axis, joined in sequence. Your job is to write those fragments. **No options and no titles.** Those come later, once the script exists.

The four axes (spec §5.2):
- **Kind:**
  - **crew**: a street crew; protection and debt in the underlevels; stacks, stairwells, a shuttered market level. The name is plural.
  - **syndicate**: a syndicate's local business; contraband and unvetted implants through the docks; a cargo hulk, bonded warehouses, "the customs desk that waves them through". The name is singular. It appears only when the player already owes this syndicate (the Patron).
  - **front**: a licit fitting clinic that keeps every client's logs and sells what it learns. It services and deals, and never manufactures hardware. Consulting rooms, the records vault, the back rooms behind recovery. The name is singular, with no article.
  - **hired**: a hired crew between contracts; muscle and boarding crews; disciplined, loyal to whoever pays next; a barracks ship, a rented hangar, the drill floor. The name is plural.
- **Method:** violence, bribery, blackmail, infiltration.
- **Mind** (how the Neurofracture shows):
  - **purge** (paranoid, wrathful): the implant forecasts the leader's *own* suspicion and violence before the leader feels it.
  - **grandeur** (arrogant, ambitious): the overlay never shows the leader hesitating, and the leader reads that as a mandate.
  - **forecast** (eccentric, calm): the leader does what the implant shows they are about to do, and says so.
  - **cold** (callous, diligent): flattened affect; looks at the floor when spoken to; prices everything.
- **Band** (how far gone the leader is): **flicker** (early, small tells), **fracture** (open episodes), **storm** (near the end, dangerous to everyone near).

## 2. The fragments to write

Key form: `eotg_aug_kingpin.<event>.<fragment>`. These names are **provisional**; the scripter may rename them, and the localizer maps your drafts onto the final keys.

| Event | What happens there (spec §5.8) | Fragments (one line each) |
|---|---|---|
| **.001 Word From Below** | Someone reports to the player that the leader of an organization has gone unstable. The reporter is `eotg_kp_reporter` (spymaster, else marshal), or a described, unscoped "captain of the dock watch" in `.desc_none`. | **A, the kind:** `.desc_crew`, `.desc_syndicate`, `.desc_syndicate_patron` (the player's own Patron's syndicate), `.desc_front`, `.desc_hired`. **B, the method:** `.desc_m_violence`, `.desc_m_bribery`, `.desc_m_blackmail`, `.desc_m_infiltration`. **C, the band:** `.desc_band_flicker`, `.desc_band_fracture`, `.desc_band_storm`. |
| **.002 The Audience** | The leader comes to the player's audience chamber. | **A, the mind:** `.desc_purge` (names a lieutenant the leader had killed; scope `eotg_kp_lieutenant`), `.desc_grandeur`, `.desc_forecast`, `.desc_cold`. **B, the kind** (one line: what they brought into the room): `.desc_k_crew`, `.desc_k_syndicate`, `.desc_k_front`, `.desc_k_hired`. **C, the band:** `.desc_band_flicker`, `.desc_band_fracture`, `.desc_band_storm`. |
| **.003 The Offer** | The leader proposes a partnership. | **A, the kind** (the offer itself): `.desc_crew`, `.desc_syndicate`, `.desc_front`, `.desc_hired`. **B, the player's position:** `.desc_vassal` (the leader hints the player could take the liege's seat), `.desc_independent` (hints at a neighbour's seat), `.desc_noclaim` (no seat on offer, only partnership). |
| **.005 The Errand** | The leader asks for a favour. | One per method: `.desc_violence` (someone who crossed the leader, a courtier, scope `eotg_kp_errand_target`), `.desc_bribery` (a cargo, waved through), `.desc_blackmail` (a file on a named person, scope `eotg_kp_errand_target`), `.desc_infiltration` (seat the leader's person at your court). |
| **.006 The Episode** | The fracture shows openly. | One per mind: `.desc_purge` (wants `eotg_kp_purge_target` handed over before doing it; use the fixed line in spec §7.3), `.desc_grandeur` (wants a public seat at your table), `.desc_forecast` (warns you about itself; fixed line in §7.3), `.desc_cold` (the itemized cost of your patience). |
| **.010 The Arrest** | Guards go to take the leader. | One per kind (where it happens): `.desc_crew` (the stacks), `.desc_syndicate` (a cargo hulk), `.desc_front` (the clinic's back rooms), `.desc_hired` (a barracks ship; they fight back as a unit). |
| **.012 Retaliation** | The organization strikes back. | One per kind: `.desc_crew` (arson; a victim may be named, scope `eotg_kp_victim`, with a fallback `.desc_crew_none` without one), `.desc_syndicate` ("your guard was bought"), `.desc_front` (they threaten to publish client logs), `.desc_hired` (open fighting on the drill floor; victim and fallback as for crew). |
| **.033 The War Below** | A war is on, and the organization offers or demands something. | One per kind: `.desc_crew` (raids on the enemy's stores), `.desc_syndicate` (an enemy officer for sale), `.desc_front` (a file on an enemy councillor), `.desc_hired` (the crew wants a raise). |
| **Endings** | Shared band lines for every ending: how far gone the leader was by the end. | `.desc_end_flicker`, `.desc_end_fracture`, `.desc_end_storm` (write them once, generic to every ending, naming only the leader). |

That is about 55 fragments.

## 3. Rules special to this chain (on top of the feedback file)
- **Fragment length:** fragment A about 30–50 words, fragments B and C 12–30 words each. An assembled desc should stay within about 45–80 words. Every fragment after the first starts with `\n\n`.
- **Every fragment must read correctly next to every partner it can be joined with.** Test each A against each B in your head. No fragment may assume another fragment's content: "the bodies" in B can't refer back to something only crew-A mentions.
- **Naming the organization:** only in per-kind fragments, with these placeholders exactly:
  - crew / hired: `[eotg_kp.Custom('eotg_aug_cl_gang')]` (plural: "the Cut Lines are…");
  - syndicate: `[eotg_kp.Custom('eotg_aug_cl_syndicate_offer')]` (singular);
  - front: `[eotg_kp.Custom('eotg_aug_cl_company')]` (singular, no article).

  Never put `'s` after a Custom() call. Lines shared across kinds name only the leader.
- **The leader:** `[eotg_kp.GetFirstName]`, `[eotg_kp.GetSheHe]`, `[eotg_kp.GetHerHis]`, `[eotg_kp.GetHerHim]`. The leader is a woman about half the time, so never write "he" or "his".
- **What to call the leader in prose:** crew "the boss"; syndicate "the syndicate's boss here"; front "the director"; hired "the captain". **Never "kingpin"** in any desc.
- **The player:** "you". The liege is `[ROOT.Char.GetLiege.GetFirstName]`.
- **Voice:** the leader's implant forecasts and logs **only the leader**. It never predicts the player, plots or the future of the realm; never "says", "speaks", "whispers" or "answers". The leader speaks; the implant *has the leader doing*, *runs the leader forward*, *shows*. The fixed lines in spec §5.2.4 and §7.3 are binding: use them as written where they fit.
- **Banned in this chain** (spec §7.4, plus feedback §3): warrant, police, officers (as law), law enforcement, authorities, law-and-order, puppet, strings, "owns you", clean house, today, tonight, dawn, morning, decks (say "the lower levels" / "the underlevels"), hang, gallows, noose, neural copies, station, human, Void, mafia vocabulary (Don, capo, consigliere, "the Family"), and medieval crime words (brigand, thieves' guild, footpad).
- **No invented people.** Use only the scopes named above. Unscoped people are described by role, with no gender ("one of the dock hands", "a runner").
- **Make the four kinds sound different.** The crew talks about streets, debt and who owes whom; the syndicate about cargo, margins and what clears customs; the front about files, records and what clients said under sedation; the hired crew about contracts, retainers and pay. The organizations are different businesses, so write them that way.
- Canadian spelling.

## 4. In-voice samples (target register)
- "The boss has stopped collecting. [eotg_kp.GetSheHe|U] sends the debts back paid, in someone else's blood, with a note of the date."
- "It had me reaching for [eotg_kp_lieutenant.GetFirstName] a day before I knew I'd stopped trusting [eotg_kp_lieutenant.GetHerHim]. It's been right about me every time." (fixed line, purge)
- "[eotg_kp.GetFirstName] looks at the floor when spoken to, and replies with prices." (fixed line, cold)

## 5. Format of your delivery
- One section per event. Each line is ` key:0 "text"`, with no `l_english:` header and no literal newlines inside quotes.
- After each event, add a short **pairing check**: list any A+B combination you think reads awkwardly.
- At the end, a word-frequency note: the five words or phrases you used most across all fragments, so we can catch new crutches.
- Don't claim checks you haven't done.
