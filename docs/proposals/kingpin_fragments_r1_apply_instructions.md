# Applying the Kingpin fragments (Gemini round 1): review and apply instructions (2026-10-06)

> **Superseded 2026-10-08 (quote form and voice):** speech is written with vanilla's **unescaped straight double quotes** inside the loc string (`key:0 "Narration. "Speech," [x.GetSheHe] says."`), stress with `#EMP …#!` (at most once per event), never `\"` and never `'…'` for speech; narration is first person per `docs/specs/event_quality_v1.md` §12.1. Binding text: `docs/specs/event_quality_v1.md` §12. Any `\"` in a draft converts to an unescaped `"` when applied, never to `'`.

**For:** eotg-localizer, when writing `localization/english/eotg_aug_kingpin_l_english.yml` after the Kingpin batch A build.
**Source:** `kingpin_fragments_gemini_r1.md` (57 keys; the 58th `:0 "` line is in the self-check table, not a key).
**Review:** lore-keeper, 2026-10-06. **Verdict:** ACCEPT WITH EDITS. 11 fragments pass unchanged; 42 need the edits below. Keys follow the final names in the scripter's key list; map them where the build renamed anything.

**Pass unchanged (apart from G1 quotes where they hold speech):**
- .001: `m_blackmail`, `band_storm`
- .002: `cold`, `k_syndicate`, `k_front`, `band_fracture`
- .003: `crew`
- .012: `crew`, `crew_none`
- .033: `hired`
- `desc_end_fracture`

## Orchestrator rulings (structural; also sent to the scripter)
- **G2. The .001 reporter line comes first.** Order: `desc_reporter` / `desc_none`, then kind A, method B, band C. Every .001 kind A therefore starts with `\n\n`. Budget: reporter 14 words or fewer, A 32 or fewer, B 19 or fewer, C 19 or fewer, for about 80 words in total.
- **U1. Band lines.** .005 and .006 reuse the .002 band keys; .010 and .012 reuse the .001 band keys. There are no new band keys.
- **U2. .003 `desc_independent`** covers both seat targets, with no gating. Use the wording below.
- **U3. Currency.** Avoid currency nouns ("credit chips", "chits", "hard currency"), because canon has no unit.

## Global edits
- **G1.** ~~Write speech in single quotes, never `\"`~~ (shipped style: `eotg_augmentation_l_english.yml:413-414`). *(superseded 2026-10-08: see the note at the top)* Speech now goes in unescaped `"`; batch B's `\"` convert to `"`.
- **G3. No eye implant.** No "optical iris", "optic flutter", "optical feed" or "optical jitter".
- Canadian spelling: "levelled", not "leveled".
- The front's signature is the recovery logs: what clients said under sedation. Cut "telemetry" down to one use at most.

## Per-key fixes (exact text)
| Key | Fix |
|---|---|
| .001.desc_reporter | `[eotg_kp_reporter.GetFirstName] brings the report in person, and waits while you read it.` |
| .001.desc_none | `The captain of the dock watch brings the report up from the underlevels, and waits by the door.` |
| .001.desc_crew | `\n\n[eotg_kp.Custom('eotg_aug_cl_gang')] collect debts across the stacks and the shuttered market level. Their boss, [eotg_kp.GetFirstName], has lately started collecting twice from people who already paid.` |
| .001.desc_syndicate | `\n\nUnvetted crates unload from a hulk into bonded warehouses and clear the customs desk that waves them through. [eotg_kp.Custom('eotg_aug_cl_syndicate_offer')] moves the cargo, but the syndicate's boss here, [eotg_kp.GetFirstName], has started missing hand-offs.` |
| .001.desc_syndicate_patron | `\n\nUnvetted crates for [eotg_kp.Custom('eotg_aug_cl_syndicate_offer')], the syndicate you already owe, unload from a hulk past the customs desk that waves them through. The syndicate's boss here, [eotg_kp.GetFirstName], has started missing hand-offs.` |
| .001.desc_front | `\n\n[eotg_kp.Custom('eotg_aug_cl_company')] fits and services implants in its consulting rooms, and keeps every client's logs in a vault behind recovery. Lately the logs have been selling. The director, [eotg_kp.GetFirstName], has begun to slip.` |
| .001.desc_hired | `\n\n[eotg_kp.Custom('eotg_aug_cl_gang')] are between contracts on the drill floor of a barracks ship, with pay in hand and nowhere to spend it. Their captain, [eotg_kp.GetFirstName], has begun giving the squads contradictory orders.` |
| .001.desc_m_violence | `\n\nBefore the shift ended, two runners turned up broken in a service conduit, and the report gives no reason.` |
| .001.desc_m_bribery | `\n\nTwo of your clerks have cleared debts their pay could never cover. Neither will say who paid.` |
| .001.desc_m_infiltration | `\n\nThe report ends with names: porters, attendants and dock hands, all passing word below for months.` |
| .001.desc_band_flicker | `\n\nThe tells are still small: a hand that moves before the decision does, a step taken a moment early.` |
| .001.desc_band_fracture | Gemini's text, with "leveled" changed to "levelled". |
| .002.desc_forecast | `[eotg_kp.GetFirstName] takes the seat across from you. [eotg_kp.GetSheHe\|U] starts to rise before [eotg_kp.GetSheHe] has decided to, sits again, and apologizes for the habit. 'Sorry,' [eotg_kp.GetSheHe] mutters, rubbing [eotg_kp.GetHerHis] temple. 'It ran ahead of me again. I'll let you finish.'` |
| .002.desc_k_crew | `\n\n[eotg_kp.GetSheHe\|U] drops a cracked debt slate on the table between you, every name on it marked paid, overdue or gone.` |
| .002.desc_k_hired | `\n\n[eotg_kp.GetSheHe\|U] has come in boarding armour, and lays the last contract on the table: paid in full, nothing signed since.` |
| .002.desc_band_flicker | `\n\nOne hand moves a moment before the rest of [eotg_kp.GetHerHim], but [eotg_kp.GetHerHis] posture stays under control.` |
| .002.desc_band_storm | `\n\nHeat shimmers off the port at the base of [eotg_kp.GetHerHis] skull. [eotg_kp.GetHerHis\|U] fingers spasm against [eotg_kp.GetHerHis] sidearm, and your guards shift closer.` |
| .002 grandeur / purge | Apply G1 only. |
| .003.desc_syndicate | Gemini's text, with "unrolls" changed to "opens". |
| .003.desc_front | Gemini's text, with "taps the locked folder." changed to "sets a locked folder on the table." |
| .003.desc_hired | Gemini's text, with "for your personal banner" changed to "for your own guard". |
| .003.desc_independent | `\n\n'Your borders could grow,' [eotg_kp.GetFirstName] suggests. 'Back me, and a seat near you could be yours before the year is out.'` |
| .003 vassal / noclaim | Apply G1 only. |
| .005.desc_violence | Gemini's text, with "the boss says flatly" changed to "[eotg_kp.GetSheHe] says flatly", plus G1. |
| .005.desc_bribery | `[eotg_kp.GetFirstName] lays an uninspected cargo manifest on the table. 'A transport from the outer route is sitting at the docks,' [eotg_kp.GetSheHe] says. 'Have your customs desk wave it through with the seals unbroken, and your cut is paid before the next shift.'` |
| .005.desc_blackmail | `[eotg_kp.GetFirstName] sets a file on the table, labelled with one name: [eotg_kp_errand_target.GetFirstName]. 'Logs, debts, a few things said in a recovery bay,' [eotg_kp.GetSheHe] murmurs. 'Use it or burn it. Either way, we understand each other better.'` |
| .005.desc_infiltration | `[eotg_kp.GetFirstName] glances toward the door. 'One of my people needs a post in your household,' [eotg_kp.GetSheHe] says. 'Something quiet, with access to the lower transit corridors. You'll find the arrangement useful.'` |
| .006.desc_purge | Gemini's text, with "[eotg_kp.GetHerHis] optical feed glowing an angry amber" changed to "[eotg_kp.GetHerHis] jaw locked tight". Keep the fixed line; apply G1. |
| .006.desc_grandeur | `[eotg_kp.GetFirstName] steps into your audience unannounced and asks for a seat at your table, in public. 'Everyone below already knows my name,' [eotg_kp.GetSheHe] declares before your attendants. 'It is time your court said it out loud.'` |
| .006.desc_forecast | `[eotg_kp.GetFirstName] stops you in the corridor, unhurried, and waits until you are listening. 'Every time it runs me forward, I end up on the other side of you,' [eotg_kp.GetSheHe] says. 'I wanted you to hear that from me.'` |
| .006.desc_cold | Gemini's text, with "from the deck" changed to "from the floor" and "drones in an unvarying monotone" changed to "says, without inflection". |
| .010.desc_crew | `Your guards have traced the boss, [eotg_kp.GetFirstName], to the stacks: three flights down a rusted stairwell, behind the shuttered market level, where every landing has a lookout and every lookout owes [eotg_kp.Custom('eotg_aug_cl_gang')] money.` |
| .010.desc_syndicate | `Your guards have traced the syndicate's boss here, [eotg_kp.GetFirstName], to a cargo hulk moored off the docks. The bonded holds are stacked with crates that never went near the customs desk, and the hands aboard keep odd hours.` |
| .010.desc_front | `Your guards have mapped the back rooms of [eotg_kp.Custom('eotg_aug_cl_company')]: consulting rooms in front, recovery behind them, and past recovery the records vault, where the director, [eotg_kp.GetFirstName], works late among the client files.` |
| .010.desc_hired | `Your guards have found [eotg_kp.GetFirstName] aboard a barracks ship in a rented hangar. [eotg_kp.Custom('eotg_aug_cl_gang')] drill there every shift, armed and in step, and their captain is never far from them. If it comes to a fight, they will fight as one.` |
| .012.desc_syndicate | `The guards you posted at the docks have been bought. The customs desk waved a transport through an hour early, and your own watch stood aside while the contraband cleared. The duty roster shows nothing out of place.` |
| .012.desc_front | `A courier brings one page from the records vault of [eotg_kp.Custom('eotg_aug_cl_company')]: a recovery log, transcribed word for word, of what one of your courtiers said under sedation. Every file like it goes public unless you back down.` |
| .012.desc_hired | `[eotg_kp.Custom('eotg_aug_cl_gang')] come off the drill floor in boarding order and push into the corridors below your residence. In the crossfire, [eotg_kp_victim.GetFirstName] is hit and badly wounded before your guards hold them at the blast doors.` |
| .012.desc_hired_none | `[eotg_kp.Custom('eotg_aug_cl_gang')] come off the drill floor in boarding order and push into the corridors below your residence. Volley fire drives your guards back, level by level, until the blast doors close between them.` |
| .033.desc_crew | `With the war on, [eotg_kp.Custom('eotg_aug_cl_gang')] have found the enemy's stores: fuel and munitions in depots below the enemy's own lower levels, guarded by people who owe the crew money. The boss wants to raid them, and wants you to look the other way.` |
| .033.desc_syndicate | `The war has slowed every lane but the docks. [eotg_kp.Custom('eotg_aug_cl_syndicate_offer')] has an enemy officer in a bonded warehouse, caught slipping through customs with the wrong papers. For a price, the syndicate's boss here will make sure the officer never reaches the enemy's lines again.` |
| .033.desc_front | `The war has made the records vault of [eotg_kp.Custom('eotg_aug_cl_company')] worth more than its fittings. An enemy councillor was once a client there, and the director, [eotg_kp.GetFirstName], has the recovery logs: what the councillor said under sedation, word for word. The file is yours, if you want it.` |
| desc_end_flicker | `\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it.` |
| desc_end_storm | `\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next.` |

Any fragment not listed takes Gemini's text with G1 applied. Before writing, check every line against the built events: it must be true on every path that shows it. Lines in .012 must hold on all three entry paths (.003 d, a .010 failure, a .015 failure). Ending band lines must hold on every leaf.

## For a Gemini round 2 (if any)
Do not claim checks that weren't run: Gemini's "automated script" pairing check and its Canadian-spelling list were both false.
