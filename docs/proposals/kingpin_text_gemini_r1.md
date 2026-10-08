# Neurofractured Kingpin: Localization Proposals (Gemini Round 1)

Draft for `localization/english/eotg_aug_kingpin_l_english.yml`. Text only; no `.yml` or `.txt` edits.
Follows `docs/specs/cybernetics_v2_kingpin.md` §5.2, §5.4.2, §5.8, §7, §7.3, §7.4, §8, and built script keys `docs/specs/build/kingpin_batchA_loc_keys.txt`.

# BATCH A, built script keys (336 keys)

## eotg_aug_kingpin.001

 eotg_aug_kingpin.001.t:0 "Word From Below"
 eotg_aug_kingpin.001.desc_reporter:0 "[eotg_kp_reporter.GetFirstName] brings the report in person, and waits while you read it." # from apply instructions
 eotg_aug_kingpin.001.desc_none:0 "The captain of the dock watch brings the report up from the underlevels, and waits by the door." # from apply instructions
 eotg_aug_kingpin.001.desc_syndicate_patron:0 "\n\nUnvetted crates for [eotg_kp.Custom('eotg_aug_cl_syndicate_offer')], the syndicate you already owe, unload from a hulk past the customs desk that waves them through. The syndicate's boss here, [eotg_kp.GetFirstName], has started missing hand-offs." # from apply instructions
 eotg_aug_kingpin.001.desc_crew:0 "\n\n[eotg_kp.Custom('eotg_aug_cl_gang')] collect debts across the stacks and the shuttered market level. Their boss, [eotg_kp.GetFirstName], has lately started collecting twice from people who already paid." # from apply instructions
 eotg_aug_kingpin.001.desc_syndicate:0 "\n\nUnvetted crates unload from a hulk into bonded warehouses and clear the customs desk that waves them through. [eotg_kp.Custom('eotg_aug_cl_syndicate_offer')] moves the cargo, but the syndicate's boss here, [eotg_kp.GetFirstName], has started missing hand-offs." # from apply instructions
 eotg_aug_kingpin.001.desc_front:0 "\n\n[eotg_kp.Custom('eotg_aug_cl_company')] fits and services implants in its consulting rooms, and keeps every client's logs in a vault behind recovery. Lately the logs have been selling. The director, [eotg_kp.GetFirstName], has begun to slip." # from apply instructions
 eotg_aug_kingpin.001.desc_hired:0 "\n\n[eotg_kp.Custom('eotg_aug_cl_gang')] are between contracts on the drill floor of a barracks ship, with pay in hand and nowhere to spend it. Their captain, [eotg_kp.GetFirstName], has begun giving the squads contradictory orders." # from apply instructions
 eotg_aug_kingpin.001.desc_m_violence:0 "\n\nBefore the shift ended, two runners turned up broken in a service conduit, and the report gives no reason." # from apply instructions
 eotg_aug_kingpin.001.desc_m_bribery:0 "\n\nTwo of your clerks have cleared debts their pay could never cover. Neither will say who paid." # from apply instructions
 eotg_aug_kingpin.001.desc_m_blackmail:0 "\n\nA sealed dossier was produced. Personal telemetry logs were quoted line by line until resistance stopped entirely."
 eotg_aug_kingpin.001.desc_m_infiltration:0 "\n\nThe report ends with names: porters, attendants and dock hands, all passing word below for months." # from apply instructions
 eotg_aug_kingpin.001.desc_band_storm:0 "\n\nHeat shimmers off the port at the base of [eotg_kp.GetHerHis] skull. [eotg_kp.GetHerHis\" # from apply instructions
 eotg_aug_kingpin.001.desc_band_fracture:0 "\n\nGemini's text, with "leveled" changed to "levelled"." # from apply instructions
 eotg_aug_kingpin.001.desc_band_flicker:0 "\n\nThe tells are still small: a hand that moves before the decision does, a step taken a moment early." # from apply instructions
 eotg_aug_kingpin.001.a:0 "Bring [eotg_kp.GetFirstName] to me. Quietly."
 eotg_aug_kingpin.001.b:0 "Arrest [eotg_kp.GetFirstName] before the next shift."
 eotg_aug_kingpin.001.c:0 "A quarrel in the underlevels. Leave it."
 eotg_aug_kingpin.001.d:0 "Ask the envoy to deal with [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.001.e:0 "Audit [eotg_kp.Custom('eotg_aug_cl_company')]'s client records."
 eotg_aug_kingpin.001.f:0 "Pay them to keep their boss quiet."
 eotg_aug_kingpin.001.f_hired:0 "Buy out their next contract."
 eotg_aug_kingpin.001.a.tt:0 "You summon [eotg_kp.GetFirstName] to a private audience."
 eotg_aug_kingpin.001.b.tt:0 "You order the guard to take [eotg_kp.GetFirstName] into custody immediately."
 eotg_aug_kingpin.001.d.tt:0 "You request the patron's envoy to handle [eotg_kp.GetFirstName] on your behalf."
 eotg_aug_kingpin.001.e.tt:0 "You send inspectors to examine the clinic's books and client files."

**Truth note:** Fired by yearly pulse on_action. Options branch into audience (.002), arrest (.010), open neglect, patron envoy (.074), audit (.015), or bribery/collaboration. Holds for any starting realm.

## eotg_aug_kingpin.002

 eotg_aug_kingpin.002.t:0 "The Audience"
 eotg_aug_kingpin.002.desc_purge:0 "[eotg_kp.GetFirstName] enters your audience chamber with tense strides, [eotg_kp.GetHerHis] gaze checking every doorway. \"It had me reaching for [eotg_kp_lieutenant.GetFirstName] a day before I knew I'd stopped trusting [eotg_kp_lieutenant.GetHerHim],\" [eotg_kp.GetSheHe] says quietly. \"It's been right about me every time.\""
 eotg_aug_kingpin.002.desc_grandeur:0 "[eotg_kp.GetFirstName] arrives with an entourage and sits before being invited, spreading [eotg_kp.GetHerHis] arms wide across the chair. \"It doesn't show me hesitating any more,\" [eotg_kp.GetSheHe] remarks with a sharp smile. \"You'd be surprised how much that's worth in a room.\""
 eotg_aug_kingpin.002.desc_forecast:0 "[eotg_kp.GetFirstName] takes the seat across from you. [eotg_kp.GetSheHe\" # from apply instructions
 eotg_aug_kingpin.002.desc_cold:0 "[eotg_kp.GetFirstName] enters without ceremony. [eotg_kp.GetSheHe|U] looks at the floor when spoken to, and replies with prices. Every gesture is flattened, stripped of hesitation or fear, as if the living person were merely an invoice waiting for settlement."
 eotg_aug_kingpin.002.desc_k_crew:0 "\n\n[eotg_kp.GetSheHe\" # from apply instructions
 eotg_aug_kingpin.002.desc_k_syndicate:0 "\n\n[eotg_kp.GetSheHe|U] sets down a customs clearance seal and a manifest of unvetted shipments, stamped and counter-signed."
 eotg_aug_kingpin.002.desc_k_front:0 "\n\n[eotg_kp.GetSheHe|U] places a locked diagnostic slate on the table, its display listing encrypted recovery room files."
 eotg_aug_kingpin.002.desc_k_hired:0 "\n\n[eotg_kp.GetSheHe\" # from apply instructions
 eotg_aug_kingpin.002.desc_band_storm:0 "\n\nHeat shimmers off the port at the base of [eotg_kp.GetHerHis] skull. [eotg_kp.GetHerHis\" # from apply instructions
 eotg_aug_kingpin.002.desc_band_fracture:0 "\n\nActuator clicks twitch along [eotg_kp.GetHerHis] collar. [eotg_kp.GetSheHe|U] blinks against sudden visual distortion before continuing."
 eotg_aug_kingpin.002.desc_band_flicker:0 "\n\nOne hand moves a moment before the rest of [eotg_kp.GetHerHim], but [eotg_kp.GetHerHis] posture stays under control." # from apply instructions
 eotg_aug_kingpin.002.a:0 "Say what you came to say."
 eotg_aug_kingpin.002.b:0 "Guards. Now."
 eotg_aug_kingpin.002.c:0 "Smile. Agree. Remember all of it."
 eotg_aug_kingpin.002.d:0 "Does yours run ahead of you too?"
 eotg_aug_kingpin.002.a.tt:0 "Hear the boss's proposal."
 eotg_aug_kingpin.002.b.tt:0 "Call the guards and attempt an immediate arrest."
 eotg_aug_kingpin.002.c.tt:0 "Feign agreement while studying [eotg_kp.GetFirstName]'s weaknesses."

**Truth note:** Fired from .001.a or .014.b. Boss comes to private audience. Options provide dialogue, arrest, deceptive delay, or augmented recognition. Holds across all minds.

## eotg_aug_kingpin.003

 eotg_aug_kingpin.003.t:0 "The Offer"
 eotg_aug_kingpin.003.desc_crew:0 "[eotg_kp.GetFirstName] leans forward across the table. [eotg_kp.Custom('eotg_aug_cl_gang')] can ensure the underlevels stay manageable, running protection and suppressing street unrest for a steady share of domain revenue and freedom from patrol harassment."
 eotg_aug_kingpin.003.desc_syndicate:0 "Gemini's text, with "unrolls" changed to "opens"." # from apply instructions
 eotg_aug_kingpin.003.desc_front:0 "Gemini's text, with "taps the locked folder." changed to "sets a locked folder on the table."" # from apply instructions
 eotg_aug_kingpin.003.desc_hired:0 "Gemini's text, with "for your personal banner" changed to "for your own guard"." # from apply instructions
 eotg_aug_kingpin.003.desc_noclaim:0 "\n\n\"A simple, quiet arrangement,\" [eotg_kp.GetFirstName] concludes. \"You take your share of the margin, and the lower levels run without friction.\""
 eotg_aug_kingpin.003.a:0 "We can work together."
 eotg_aug_kingpin.003.d:0 "No. Get out."
 eotg_aug_kingpin.003.e_crew:0 "Keep the stacks quiet, and we talk again."
 eotg_aug_kingpin.003.e_syndicate:0 "Take your cut and look away."
 eotg_aug_kingpin.003.e_front:0 "Your files on [ROOT.Char.GetLiege.GetFirstName]. Now."
 eotg_aug_kingpin.003.e_hired:0 "I'll keep your guns on retainer."
 eotg_aug_kingpin.003.d.tt:0 "Reject [eotg_kp.GetFirstName]'s terms entirely."

**Truth note:** Fired from .002 or .012.b negotiation. Options offer partnership, claim support, refusal, or profile-specific arrangements. Holds on all entry routes.

## eotg_aug_kingpin.004

 eotg_aug_kingpin.004.t:0 "The Ledger"
 eotg_aug_kingpin.004.desc:0 "A courier brings a sealed ledger and an uninspected cargo pouch to your chambers. Every entry records off-the-books transactions through the lower transit corridors, accompanied by a sizeable share set aside specifically for your seal."
 eotg_aug_kingpin.004.a:0 "Take it."
 eotg_aug_kingpin.004.b:0 "Take half. Log every credit."
 eotg_aug_kingpin.004.c:0 "Send it back."
 eotg_aug_kingpin.004.d:0 "Ask what the other half buys."
 eotg_aug_kingpin.004.b.tt:0 "Accept only a registered portion of the proceeds."

**Truth note:** Triggered in stage collab during yearly pulse T6 for syndicate kind or bribery method. Courier delivers underlevel revenues and ledger. Holds whether quiet arrangement or active collaboration.

## eotg_aug_kingpin.005

 eotg_aug_kingpin.005.t:0 "The Errand"
 eotg_aug_kingpin.005.desc_violence:0 "Gemini's text, with "the boss says flatly" changed to "[eotg_kp.GetSheHe] says flatly", plus G1." # from apply instructions
 eotg_aug_kingpin.005.desc_blackmail:0 "[eotg_kp.GetFirstName] sets a file on the table, labelled with one name: [eotg_kp_errand_target.GetFirstName]. 'Logs, debts, a few things said in a recovery bay,' [eotg_kp.GetSheHe] murmurs. 'Use it or burn it. Either way, we understand each other better.'" # from apply instructions
 eotg_aug_kingpin.005.desc_infiltration:0 "[eotg_kp.GetFirstName] glances toward the door. 'One of my people needs a post in your household,' [eotg_kp.GetSheHe] says. 'Something quiet, with access to the lower transit corridors. You'll find the arrangement useful.'" # from apply instructions
 eotg_aug_kingpin.005.desc_bribery:0 "[eotg_kp.GetFirstName] lays an uninspected cargo manifest on the table. 'A transport from the outer route is sitting at the docks,' [eotg_kp.GetSheHe] says. 'Have your customs desk wave it through with the seals unbroken, and your cut is paid before the next shift.'" # from apply instructions
 eotg_aug_kingpin.005.a_violence:0 "Look away."
 eotg_aug_kingpin.005.b_violence:0 "Warn [eotg_kp_errand_target.GetFirstName]."
 eotg_aug_kingpin.005.c_violence:0 "Arrest the ones sent to do it."
 eotg_aug_kingpin.005.a_blackmail:0 "Keep the file."
 eotg_aug_kingpin.005.b_blackmail:0 "Burn it."
 eotg_aug_kingpin.005.c_blackmail:0 "Use it on [eotg_kp.GetFirstName] instead."
 eotg_aug_kingpin.005.a_infiltration:0 "Give them a post."
 eotg_aug_kingpin.005.b_infiltration:0 "No posts for them."
 eotg_aug_kingpin.005.c_infiltration:0 "Give them a post. Watch them."
 eotg_aug_kingpin.005.a_bribery:0 "Wave it through."
 eotg_aug_kingpin.005.b_bribery:0 "Inspect the cargo."
 eotg_aug_kingpin.005.c_bribery:0 "Seize it."
 eotg_aug_kingpin.005.c_violence.tt:0 "Dispatch the guard to apprehend the attack squad before they strike."
 eotg_aug_kingpin.005.c_blackmail.success:0 "You turn the incriminating records against [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.005.c_blackmail.failure:0 "[eotg_kp.GetFirstName] outmanoeuvres your agents and deepens [eotg_kp.GetHerHis] advantage."
 eotg_aug_kingpin.005.c_infiltration.tt:0 "Place [eotg_kp_lieutenant.GetFirstName] under close watch within your household."

**Truth note:** Triggered in stage collab during yearly pulse T6. Variant options by method (violence, blackmail, infiltration, bribery). Holds across all kinds.

## eotg_aug_kingpin.006

 eotg_aug_kingpin.006.t:0 "The Episode"
 eotg_aug_kingpin.006.desc_purge:0 "Gemini's text, with "[eotg_kp.GetHerHis] optical feed glowing an angry amber" changed to "[eotg_kp.GetHerHis] jaw locked tight". Keep the fixed line; apply G1." # from apply instructions
 eotg_aug_kingpin.006.desc_grandeur:0 "[eotg_kp.GetFirstName] steps into your audience unannounced and asks for a seat at your table, in public. 'Everyone below already knows my name,' [eotg_kp.GetSheHe] declares before your attendants. 'It is time your court said it out loud.'" # from apply instructions
 eotg_aug_kingpin.006.desc_forecast:0 "[eotg_kp.GetFirstName] stops you in the corridor, unhurried, and waits until you are listening. 'Every time it runs me forward, I end up on the other side of you,' [eotg_kp.GetSheHe] says. 'I wanted you to hear that from me.'" # from apply instructions
 eotg_aug_kingpin.006.desc_cold:0 "Gemini's text, with "from the deck" changed to "from the floor" and "drones in an unvarying monotone" changed to "says, without inflection"." # from apply instructions
 eotg_aug_kingpin.006.a_purge:0 "Take [eotg_kp_purge_target.GetFirstName], then."
 eotg_aug_kingpin.006.b_purge:0 "No one of mine."
 eotg_aug_kingpin.006.c_purge:0 "Sit down. Talk me through it."
 eotg_aug_kingpin.006.a_grandeur:0 "A seat at my table, then."
 eotg_aug_kingpin.006.b_grandeur:0 "No."
 eotg_aug_kingpin.006.c_grandeur:0 "Mock the request in front of the court."
 eotg_aug_kingpin.006.a_forecast:0 "Thank you for the warning."
 eotg_aug_kingpin.006.b_forecast:0 "My physician will see you."
 eotg_aug_kingpin.006.c_forecast:0 "Then I'll plan for it."
 eotg_aug_kingpin.006.a_cold:0 "Pay the itemized cost."
 eotg_aug_kingpin.006.b_cold:0 "Send back an invoice of my own."
 eotg_aug_kingpin.006.c_cold:0 "No."
 eotg_aug_kingpin.006.c_purge.success:0 "You calm [eotg_kp.GetFirstName] and avert bloodshed."
 eotg_aug_kingpin.006.c_purge.failure:0 "[eotg_kp.GetFirstName]'s paranoia boils over, demanding concessions."
 eotg_aug_kingpin.006.c_forecast.tt:0 "Adjust your household security in anticipation of [eotg_kp.GetFirstName]'s predicted actions."

**Truth note:** Triggered in stage collab during yearly pulse T6. Options vary by mind (purge, grandeur, forecast, cold). Holds across all organization kinds.

## eotg_aug_kingpin.007

 eotg_aug_kingpin.007.t:0 "The Informant"
 eotg_aug_kingpin.007.desc:0 "Your agents bring word of a hidden link: [eotg_kp_informant.GetFirstName] has been quietly passing household routines and patrol rosters down into the underlevels. The informant was caught copying schedule slates near the lower transit passages."
 eotg_aug_kingpin.007.a:0 "Arrest [eotg_kp_informant.GetFirstName]."
 eotg_aug_kingpin.007.b:0 "Turn [eotg_kp_informant.GetFirstName]."
 eotg_aug_kingpin.007.c:0 "Let [eotg_kp_informant.GetFirstName] be."
 eotg_aug_kingpin.007.b.success:0 "You persuade [eotg_kp_informant.GetFirstName] to report on the underlevels for you."
 eotg_aug_kingpin.007.b.failure:0 "[eotg_kp_informant.GetFirstName] refuses your offer and alerts [eotg_kp.GetFirstName]."

**Truth note:** Fired in stage collab T6 when method is infiltration and informant not unmasked. Informs ruler of breach. Holds whether informant is planted lieutenant or courtier.

## eotg_aug_kingpin.008

 eotg_aug_kingpin.008.t:0 "The Protection Bill"
 eotg_aug_kingpin.008.desc:0 "A message slate arrives from the lower levels, itemizing the costs of keeping the docks and lower corridors undisturbed. The demand is blunt: pay the maintenance levy, or watch fuel lines and warehouse depots succumb to mysterious accidents."
 eotg_aug_kingpin.008.a:0 "Pay it."
 eotg_aug_kingpin.008.b:0 "Not one credit."
 eotg_aug_kingpin.008.c:0 "Send the guard into the stacks."
 eotg_aug_kingpin.008.c.tt:0 "Send the guard into the lower levels to shut down the extortion ring."

**Truth note:** Fired in stage collab T6 for crew kind or violence method. Demands maintenance levy. Holds whether ruler pays, denies, or cracks down.

## eotg_aug_kingpin.009

 eotg_aug_kingpin.009.t:0 "The Lieutenant"
 eotg_aug_kingpin.009.desc:0 "[eotg_kp_lieutenant.GetTitledFirstName] requests a secret audience away from prying eyes. The lieutenant claims [eotg_kp.GetFirstName]'s neurological episodes have turned unpredictable and dangerous, offering full access to the hideout in exchange for immunity and safety."
 eotg_aug_kingpin.009.a:0 "Tell me everything."
 eotg_aug_kingpin.009.b:0 "Warn [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.009.c:0 "I never heard this."
 eotg_aug_kingpin.009.a.tt:0 "Act on the lieutenant's intelligence to capture [eotg_kp.GetFirstName]."

**Truth note:** Fired in stage collab T6 (or T5 20%). Lieutenant offers to betray boss. Holds whether ruler collaborates or seeks evidence.

## eotg_aug_kingpin.010

 eotg_aug_kingpin.010.t:0 "The Arrest"
 eotg_aug_kingpin.010.desc_crew:0 "Your guards have traced the boss, [eotg_kp.GetFirstName], to the stacks: three flights down a rusted stairwell, behind the shuttered market level, where every landing has a lookout and every lookout owes [eotg_kp.Custom('eotg_aug_cl_gang')] money." # from apply instructions
 eotg_aug_kingpin.010.desc_syndicate:0 "Your guards have traced the syndicate's boss here, [eotg_kp.GetFirstName], to a cargo hulk moored off the docks. The bonded holds are stacked with crates that never went near the customs desk, and the hands aboard keep odd hours." # from apply instructions
 eotg_aug_kingpin.010.desc_front:0 "Your guards have mapped the back rooms of [eotg_kp.Custom('eotg_aug_cl_company')]: consulting rooms in front, recovery behind them, and past recovery the records vault, where the director, [eotg_kp.GetFirstName], works late among the client files." # from apply instructions
 eotg_aug_kingpin.010.desc_hired:0 "Your guards have found [eotg_kp.GetFirstName] aboard a barracks ship in a rented hangar. [eotg_kp.Custom('eotg_aug_cl_gang')] drill there every shift, armed and in step, and their captain is never far from them. If it comes to a fight, they will fight as one." # from apply instructions
 eotg_aug_kingpin.010.a:0 "Take [eotg_kp.GetFirstName] alive."
 eotg_aug_kingpin.010.b:0 "Quietly, while [eotg_kp.GetSheHe] sleeps."
 eotg_aug_kingpin.010.c:0 "Call it off."
 eotg_aug_kingpin.010.a.success:0 "You overpower [eotg_kp.GetFirstName] and take [eotg_kp.GetHerHim] into custody."
 eotg_aug_kingpin.010.a.failure:0 "[eotg_kp.GetFirstName] fights [eotg_kp.GetHerHis] way past the guards and flees below."
 eotg_aug_kingpin.010.b.success:0 "Your agents take [eotg_kp.GetFirstName] in [eotg_kp.GetHerHis] sleep without alarm."
 eotg_aug_kingpin.010.b.failure:0 "[eotg_kp.GetFirstName] awakens in time and slips away into the lower levels."

**Truth note:** Fired from .001.b, .002.b, .005.c, .009.a, .014.a. Ruler attempts to arrest boss. Martial/intrigue duel or calling off. Holds on all entry paths.

## eotg_aug_kingpin.011

 eotg_aug_kingpin.011.t:0 "The Crackdown"
 eotg_aug_kingpin.011.desc:0 "Your guards assemble at the blast doors leading into the underlevels, weapons drawn and riot shields locked. Down below, the barricades have gone up across the transit hubs, and the corridors echo with shouts as the assault begins."
 eotg_aug_kingpin.011.a:0 "Every level. Every door."
 eotg_aug_kingpin.011.b:0 "Lock the underlevels down."
 eotg_aug_kingpin.011.c:0 "Stand the guard down."
 eotg_aug_kingpin.011.a.success:0 "The guard clears the transit hubs and brings [eotg_kp.GetFirstName] in in irons."
 eotg_aug_kingpin.011.a.failure:0 "The assault falters against heavy barricades, and [eotg_kp.GetFirstName] holds the stacks."

**Truth note:** Fired from .008.c or .012.a. Full security operation launched against underlevels. Holds across all combat branches.

## eotg_aug_kingpin.012

 eotg_aug_kingpin.012.t:0 "Retaliation"
 eotg_aug_kingpin.012.desc_crew:0 "Smoke fills the lower levels as incendiary charges detonate along the market stacks. Amidst the chaos, [eotg_kp_victim.GetFirstName] was caught in the corridor and badly beaten, left bleeding against the bulkhead as a deliberate warning from the street."
 eotg_aug_kingpin.012.desc_syndicate:0 "The guards you posted at the docks have been bought. The customs desk waved a transport through an hour early, and your own watch stood aside while the contraband cleared. The duty roster shows nothing out of place." # from apply instructions
 eotg_aug_kingpin.012.desc_front:0 "A courier brings one page from the records vault of [eotg_kp.Custom('eotg_aug_cl_company')]: a recovery log, transcribed word for word, of what one of your courtiers said under sedation. Every file like it goes public unless you back down." # from apply instructions
 eotg_aug_kingpin.012.desc_hired:0 "[eotg_kp.Custom('eotg_aug_cl_gang')] come off the drill floor in boarding order and push into the corridors below your residence. In the crossfire, [eotg_kp_victim.GetFirstName] is hit and badly wounded before your guards hold them at the blast doors." # from apply instructions
 eotg_aug_kingpin.012.desc_victim:0 "\n\nIn the crossfire, [eotg_kp_victim.GetFirstName] was struck down and badly wounded by stray fire."
 eotg_aug_kingpin.012.desc_none:0 "\n\nThough no courtiers were harmed, the sudden violence sent panic through the residence corridors."
 eotg_aug_kingpin.012.a:0 "Fight for every level."
 eotg_aug_kingpin.012.b:0 "Talk."
 eotg_aug_kingpin.012.c:0 "Let them fall back to [eotg_kp_county.GetNameNoTier]."
 eotg_aug_kingpin.012.c_hired:0 "Pay their next contract elsewhere."
 eotg_aug_kingpin.012.c_syndicate:0 "Pay what my guards were paid."
 eotg_aug_kingpin.012.a.tt:0 "Deploy the guard in force to crush the retaliation."
 eotg_aug_kingpin.012.c.tt:0 "Concede the border region to let the crew withdraw."

**Truth note:** Fired upon failed arrest (.010), failed audit (.015), or refusal (.003.d). Retaliation variants branch by kind. Holds on all entry routes.

## eotg_aug_kingpin.013

 eotg_aug_kingpin.013.t:0 "In Custody"
 eotg_aug_kingpin.013.desc:0 "[eotg_kp.GetFirstName] sits in the high-security holding cells, secured by magnetic clamps and heavy restraints. The diagnostic monitors at [eotg_kp.GetHerHis] temple pulse unevenly, but the prisoner remains silent under guard."
 eotg_aug_kingpin.013.desc_band_storm:0 "\n\nHeat shimmers off the port at the base of [eotg_kp.GetHerHis] skull. [eotg_kp.GetHerHis\" # from apply instructions
 eotg_aug_kingpin.013.desc_band_fracture:0 "\n\nActuator clicks twitch along [eotg_kp.GetHerHis] collar. [eotg_kp.GetSheHe|U] blinks against sudden visual distortion before continuing."
 eotg_aug_kingpin.013.desc_band_flicker:0 "\n\nOne hand moves a moment before the rest of [eotg_kp.GetHerHim], but [eotg_kp.GetHerHis] posture stays under control." # from apply instructions
 eotg_aug_kingpin.013.a:0 "Execute [eotg_kp.GetFirstName]. Now."
 eotg_aug_kingpin.013.b:0 "A public trial, then every level cleared."
 eotg_aug_kingpin.013.c:0 "More use alive. Inside my court."
 eotg_aug_kingpin.013.d:0 "Give [eotg_kp.GetFirstName] a Region to keep quiet."
 eotg_aug_kingpin.013.e:0 "Seize the clinic and its records."
 eotg_aug_kingpin.013.f:0 "Hand [eotg_kp.GetFirstName] to the syndicate."
 eotg_aug_kingpin.013.a.tt:0 "Order an immediate summary execution."
 eotg_aug_kingpin.013.c.tt:0 "Offer [eotg_kp.GetFirstName] a place within your household retinue."
 eotg_aug_kingpin.013.d.tt:0 "Enfeoff [eotg_kp.GetFirstName] with a landed region in exchange for quiet."
 eotg_aug_kingpin.013.e.tt:0 "Seize the front's facilities and client records for realm use."
 eotg_aug_kingpin.013.f.tt:0 "Hand [eotg_kp.GetFirstName] over to the syndicate to settle your account."

**Truth note:** Fired when boss is captured in .010, .011, or .015. Sentences branch to leaves L1, L2, L10, L11, L15, L17. Holds across all capture origins.

## eotg_aug_kingpin.014

 eotg_aug_kingpin.014.t:0 "Bodies on the Docks"
 eotg_aug_kingpin.014.desc:0 "Neglecting the underlevels has taken a bloody toll. Dock watchmen report a trail of casualties across the cargo bays: rival runners and unaligned porters beaten or slain without restraint as [eotg_kp.GetFirstName]'s faction tightens its control over transit."
 eotg_aug_kingpin.014.desc_county:0 "\n\nWord from [eotg_kp_county.GetNameNoTier] indicates the local garrisons were bypassed entirely as armed runners took over cargo transit."
 eotg_aug_kingpin.014.desc_none:0 "\n\nThe violence remains concentrated around the central docks, leaving outer settlements uncertain."
 eotg_aug_kingpin.014.a:0 "Now we act."
 eotg_aug_kingpin.014.b:0 "Bring [eotg_kp.GetFirstName] in."
 eotg_aug_kingpin.014.c:0 "Not my quarrel."
 eotg_aug_kingpin.014.a.tt:0 "Send the guard into the docks to arrest [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.014.b.tt:0 "Summon [eotg_kp.GetFirstName] to discuss terms before violence spreads."

**Truth note:** Fired in stage open during yearly pulse T5. Neglected underlevels erupt in violence. Holds whether crew, syndicate, or hired gang.

## eotg_aug_kingpin.015

 eotg_aug_kingpin.015.t:0 "The Audit"
 eotg_aug_kingpin.015.desc:0 "Your inspectors arrive at the premises of [eotg_kp.Custom('eotg_aug_cl_company')], demanding unhindered access to the consultation vaults and client ledger files. The front's attendants stall for time while couriers scramble behind locked security partitions."
 eotg_aug_kingpin.015.a:0 "Audit everything."
 eotg_aug_kingpin.015.b:0 "Buy the records quietly."
 eotg_aug_kingpin.015.c:0 "Leave the records sealed."
 eotg_aug_kingpin.015.a.success:0 "Inspectors uncover the illicit client files and secure [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.015.a.failure:0 "[eotg_kp.GetFirstName] locks the vaults and drives the inspectors out."
 eotg_aug_kingpin.015.b.tt:0 "Pay for the records to keep your household safe from exposure."

**Truth note:** Fired from .001.e for front kind. Inspectors audit clinic records. Stewardship duel rolls success (.013) or failure (.012). Holds for front kind.

## eotg_aug_kingpin.040

 eotg_aug_kingpin.040.t:0 "The Inherited Hold"
 eotg_aug_kingpin.040.desc:0 "Upon succeeding to the realm, you find private records detailing an ongoing entanglement with [eotg_kp.GetFirstName]. Your predecessor left debts, secret compacts, and covert arrangements that now demand your attention."
 eotg_aug_kingpin.040.desc_collab:0 "\n\nA web of collaborative kickbacks and mutual obligations binds your treasury directly to the underlevel organization."
 eotg_aug_kingpin.040.desc_custody:0 "\n\n[eotg_kp.GetFirstName] remains held in your high-security cells, awaiting your personal decree regarding final sentence."
 eotg_aug_kingpin.040.desc_kept:0 "\n\nThe organization holds deep leverage over the bench, expecting ongoing subservience and regular concessions."
 eotg_aug_kingpin.040.desc_war:0 "\n\nAn active rebellion burns in the realm, initiated in partnership with [eotg_kp.GetFirstName]'s armed contingents."
 eotg_aug_kingpin.040.desc_open:0 "\n\nThe lower levels remain in unsettled neglect, with [eotg_kp.GetFirstName]'s network operating beyond official supervision."
 eotg_aug_kingpin.040.desc_band_storm:0 "\n\nHeat shimmers off the port at the base of [eotg_kp.GetHerHis] skull. [eotg_kp.GetHerHis\" # from apply instructions
 eotg_aug_kingpin.040.desc_band_fracture:0 "\n\nActuator clicks twitch along [eotg_kp.GetHerHis] collar. [eotg_kp.GetSheHe|U] blinks against sudden visual distortion before continuing."
 eotg_aug_kingpin.040.desc_band_flicker:0 "\n\nOne hand moves a moment before the rest of [eotg_kp.GetHerHim], but [eotg_kp.GetHerHis] posture stays under control." # from apply instructions
 eotg_aug_kingpin.040.a:0 "Acknowledge the arrangement."
 eotg_aug_kingpin.040.b:0 "Repudiate the agreement."
 eotg_aug_kingpin.040.c:0 "Order the guards to find [eotg_kp.GetFirstName]."

**Truth note:** Fired on heir via on_owner_death when predecessor dies during active kingpin story. Desc variants reflect preceding stage (open, collab, custody, kept, war). Holds for all inherited stories.

## eotg_aug_kingpin.060

 eotg_aug_kingpin.060.t:0 "A Quick Ending"
 eotg_aug_kingpin.060.desc:0 "The hearing is brief and held behind closed doors. Under your personal order, [eotg_kp.GetFirstName] is escorted to the far corridor of the cells. The sentence is carried out without ceremony or delay, and the lower levels are left without a head."
 eotg_aug_kingpin.060.desc_end_storm:0 "\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next." # from apply instructions
 eotg_aug_kingpin.060.desc_end_fracture:0 "\n\nBy the end, [eotg_kp.GetFirstName] suffered violent motor spasms and sensory distortion, the neurofracture tearing through every calculated thought."
 eotg_aug_kingpin.060.desc_end_flicker:0 "\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it." # from apply instructions
 eotg_aug_kingpin.060.a:0 "It's done."
 eotg_aug_kingpin.060.b:0 "Give [eotg_kp.GetHerHim] proper rites."

**Truth note:** L1: A Quick Ending. Reached from .013.a. Execution under ruler's personal order. Holds for any kind.

## eotg_aug_kingpin.061

 eotg_aug_kingpin.061.t:0 "The Streets Go Quiet"
 eotg_aug_kingpin.061.desc:0 "The public trial concludes under the realm's own law. Evidence compiled by your clerks is read aloud, and sentence is pronounced from your bench. Systematic sweeps clear every transit corridor, restoring unbroken order across the lower levels."
 eotg_aug_kingpin.061.desc_end_storm:0 "\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next." # from apply instructions
 eotg_aug_kingpin.061.desc_end_fracture:0 "\n\nBy the end, [eotg_kp.GetFirstName] suffered violent motor spasms and sensory distortion, the neurofracture tearing through every calculated thought."
 eotg_aug_kingpin.061.desc_end_flicker:0 "\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it." # from apply instructions
 eotg_aug_kingpin.061.a:0 "Execute [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.061.b:0 "The cells, for life."

**Truth note:** L2: The Streets Go Quiet. Reached from .013.b. Public trial under realm law. Holds for any kind.

## eotg_aug_kingpin.062

 eotg_aug_kingpin.062.t:0 "The Network Is Yours"
 eotg_aug_kingpin.062.desc:0 "Years of quiet cooperation come to an end with a sudden medical report. [eotg_kp.GetFirstName] suffered fatal neural cascade in private quarters. With the boss gone and every ledger already in your hands, the entire organization passes smoothly to your control."
 eotg_aug_kingpin.062.desc_end_storm:0 "\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next." # from apply instructions
 eotg_aug_kingpin.062.desc_end_fracture:0 "\n\nBy the end, [eotg_kp.GetFirstName] suffered violent motor spasms and sensory distortion, the neurofracture tearing through every calculated thought."
 eotg_aug_kingpin.062.desc_end_flicker:0 "\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it." # from apply instructions
 eotg_aug_kingpin.062.a:0 "Keep it running."
 eotg_aug_kingpin.062.b:0 "Burn the ledgers."
 eotg_aug_kingpin.062.c:0 "Expand it."

**Truth note:** L3: The Network Is Yours. Reached from T4 (syndicate/front). Boss dies of neural cascade, leaving network to ruler. Holds for long deals.

## eotg_aug_kingpin.068

 eotg_aug_kingpin.068.t:0 "The Break"
 eotg_aug_kingpin.068.desc:0 "The final collapse arrived with sudden, catastrophic violence. [eotg_kp.GetFirstName]'s neurological restraints gave way entirely. Coming up to the residence in a blind frenzy, the boss tore through corridors, leaving bodies and wreckage in the residence before retreating below."
 eotg_aug_kingpin.068.desc_victims:0 "\n\nBoth [eotg_kp_victim.GetFirstName] and [eotg_kp_victim_2.GetFirstName] fell before the household guard could drive the attacker back."
 eotg_aug_kingpin.068.desc_victim:0 "\n\n[eotg_kp_victim.GetFirstName] was badly wounded before the household guard could drive the attacker back."
 eotg_aug_kingpin.068.desc_none:0 "\n\nThough no courtiers fell, several service attendants were wounded before the household guard forced the assailant back into the stairwells."
 eotg_aug_kingpin.068.desc_end_storm:0 "\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next." # from apply instructions
 eotg_aug_kingpin.068.desc_end_fracture:0 "\n\nBy the end, [eotg_kp.GetFirstName] suffered violent motor spasms and sensory distortion, the neurofracture tearing through every calculated thought."
 eotg_aug_kingpin.068.desc_end_flicker:0 "\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it." # from apply instructions
 eotg_aug_kingpin.068.a:0 "Hunt [eotg_kp.GetFirstName] down. Now."
 eotg_aug_kingpin.068.b:0 "Seal the lower levels and count the dead."
 eotg_aug_kingpin.068.c:0 "Go down there yourself."
 eotg_aug_kingpin.068.a.success:0 "You corner and cut down [eotg_kp.GetFirstName] before more harm is done."
 eotg_aug_kingpin.068.a.failure:0 "[eotg_kp.GetFirstName] wounds your fighters before perishing in the melee."

**Truth note:** L9: The Break. Reached from T1, .011 failure (Storm), or resistance. Boss has violent psychotic outbreak coming up to residence. Holds for violent collapse.

## eotg_aug_kingpin.069

 eotg_aug_kingpin.069.t:0 "A Seat Under You"
 eotg_aug_kingpin.069.desc:0 "The long dispute is resolved by formal enfeoffment. [eotg_kp.GetFirstName] is granted a landed domain of the realm, trading shadowy control of the underlevels for the duties of a recognized vassal. The court murmurs at the appointment, but the streets are pacified."
 eotg_aug_kingpin.069.desc_end_storm:0 "\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next." # from apply instructions
 eotg_aug_kingpin.069.desc_end_fracture:0 "\n\nBy the end, [eotg_kp.GetFirstName] suffered violent motor spasms and sensory distortion, the neurofracture tearing through every calculated thought."
 eotg_aug_kingpin.069.desc_end_flicker:0 "\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it." # from apply instructions
 eotg_aug_kingpin.069.a:0 "Welcome my newest vassal."

**Truth note:** L10: A Seat Under You. Reached from .013.d, .032.a/b, .036.a, M3 held. Boss enfeoffed as landed vassal. Holds across all grant routes.

## eotg_aug_kingpin.070

 eotg_aug_kingpin.070.t:0 "Brought Inside"
 eotg_aug_kingpin.070.desc:0 "Realizing that [eotg_kp.GetFirstName] is too capable to execute and too dangerous to leave outside, you bring the former criminal into your household. Assigned a discreet post within your personal retinue, [eotg_kp.GetSheHe] now directs [eotg_kp.GetHerHis] talents in your service."
 eotg_aug_kingpin.070.desc_end_storm:0 "\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next." # from apply instructions
 eotg_aug_kingpin.070.desc_end_fracture:0 "\n\nBy the end, [eotg_kp.GetFirstName] suffered violent motor spasms and sensory distortion, the neurofracture tearing through every calculated thought."
 eotg_aug_kingpin.070.desc_end_flicker:0 "\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it." # from apply instructions
 eotg_aug_kingpin.070.a:0 "Keep [eotg_kp.GetFirstName] close."
 eotg_aug_kingpin.070.b:0 "Keep [eotg_kp.GetFirstName] closer: a post where I can see [eotg_kp.GetHerHim]."

**Truth note:** L11: Brought Inside. Reached from .013.c or .036.b. Boss recruited into ruler's household as courtier. Holds for recruitment paths.

## eotg_aug_kingpin.071

 eotg_aug_kingpin.071.t:0 "The Region Falls"
 eotg_aug_kingpin.071.desc:0 "Pushed beyond accommodation, the crew withdrew into the depots of the region where they keep their munitions. Fortifying the transit stations and declaring their own rule, they have severed ties with your court, leaving the domain entirely beyond your immediate reach."
 eotg_aug_kingpin.071.desc_end_storm:0 "\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next." # from apply instructions
 eotg_aug_kingpin.071.desc_end_fracture:0 "\n\nBy the end, [eotg_kp.GetFirstName] suffered violent motor spasms and sensory distortion, the neurofracture tearing through every calculated thought."
 eotg_aug_kingpin.071.desc_end_flicker:0 "\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it." # from apply instructions
 eotg_aug_kingpin.071.a:0 "A wound that will be answered."

**Truth note:** L12: The Region Falls. Reached from .012.c or .014.c (crew only). Crew falls back to depots and seizes region. Holds for crew independence.

## eotg_aug_kingpin.073

 eotg_aug_kingpin.073.t:0 "A Standing Arrangement"
 eotg_aug_kingpin.073.desc:0 "Neither side could achieve a decisive advantage, leading to a weary compromise. A regular allocation of realm revenues flows down into the underlevels, and in return the organization ensures that violence and unrest remain strictly suppressed."
 eotg_aug_kingpin.073.desc_contract:0 "\n\nA renewed service contract formalizes the financial understanding, setting exact figures for each month of peace."
 eotg_aug_kingpin.073.desc_end_storm:0 "\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next." # from apply instructions
 eotg_aug_kingpin.073.desc_end_fracture:0 "\n\nBy the end, [eotg_kp.GetFirstName] suffered violent motor spasms and sensory distortion, the neurofracture tearing through every calculated thought."
 eotg_aug_kingpin.073.desc_end_flicker:0 "\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it." # from apply instructions
 eotg_aug_kingpin.073.a:0 "It's cheaper than a war."
 eotg_aug_kingpin.073.b:0 "Until I find a way."

**Truth note:** L14: A Standing Arrangement. Reached from T4, T7, .011 failure. Extortion stalemate where tribute buys quiet. Holds for stable truce.

## eotg_aug_kingpin.074

 eotg_aug_kingpin.074.t:0 "The Syndicate Settles It"
 eotg_aug_kingpin.074.desc:0 "The syndicate has resolved its internal liability. Unwilling to let [eotg_kp.GetFirstName]'s neurological instability jeopardize wider operations, quiet enforcers arrived from the outer transit routes. The former boss was removed without a trace, leaving the docks quiet once more."
 eotg_aug_kingpin.074.desc_patron:0 "\n\nThe patron's envoy confirms that the account is marked settled, though the ledger of personal obligations between you remains open."
 eotg_aug_kingpin.074.desc_end_storm:0 "\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next." # from apply instructions
 eotg_aug_kingpin.074.desc_end_fracture:0 "\n\nBy the end, [eotg_kp.GetFirstName] suffered violent motor spasms and sensory distortion, the neurofracture tearing through every calculated thought."
 eotg_aug_kingpin.074.desc_end_flicker:0 "\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it." # from apply instructions
 eotg_aug_kingpin.074.a:0 "A quiet resolution."
 eotg_aug_kingpin.074.a.tt:0 "The envoy confirms your debt to the syndicate is reduced."

**Truth note:** L15: The Syndicate Settles It (retitled). Reached from .001.d or .013.f (syndicate only). Syndicate cleans up boss. Holds for syndicate removal.

## eotg_aug_kingpin.075

 eotg_aug_kingpin.075.t:0 "The Fracture Finishes It"
 eotg_aug_kingpin.075.desc:0 "Without intervention or sudden violence, the failing implant simply burned out its host. Attendants found [eotg_kp.GetFirstName] lifeless in private quarters, the cranial port cold and dark after a fatal neurological cascade. The organization splinters in silence."
 eotg_aug_kingpin.075.desc_crew:0 "\n\nWith the boss gone, the crew splinters into squabbling gangs across the stacks, fighting over remaining caches."
 eotg_aug_kingpin.075.desc_syndicate:0 "\n\nThe syndicate quietly closes the local ledger, recalling its remaining cargo tenders and writing off the operation."
 eotg_aug_kingpin.075.desc_front:0 "\n\nWithout direction, the consulting rooms shutter their doors and client files are quietly abandoned in the records vault."
 eotg_aug_kingpin.075.desc_hired:0 "\n\nThe mercenaries break formation and disperse across the starport, seeking individual berths on outgoing transports."
 eotg_aug_kingpin.075.desc_end_storm:0 "\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next." # from apply instructions
 eotg_aug_kingpin.075.desc_end_fracture:0 "\n\nBy the end, [eotg_kp.GetFirstName] suffered violent motor spasms and sensory distortion, the neurofracture tearing through every calculated thought."
 eotg_aug_kingpin.075.desc_end_flicker:0 "\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it." # from apply instructions
 eotg_aug_kingpin.075.a:0 "Let the quiet remain."

**Truth note:** L16: The Fracture Finishes It. Reached from T1 (pressure >= 95). Boss dies of unassisted cascade. Holds for natural termination.

## eotg_aug_kingpin.076

 eotg_aug_kingpin.076.t:0 "The Clinic Changes Hands"
 eotg_aug_kingpin.076.desc:0 "Under your direct authority, the surgical rooms and records vaults of [eotg_kp.Custom('eotg_aug_cl_company')] have been seized. Its diagnostic archives now belong to your court, providing your household with a fully operational clinic under your own law."
 eotg_aug_kingpin.076.desc_end_storm:0 "\n\nBy the end, the casing at the base of [eotg_kp.GetHerHis] skull ran hot to the touch, and [eotg_kp.GetFirstName] lost whole conversations between one sentence and the next." # from apply instructions
 eotg_aug_kingpin.076.desc_end_fracture:0 "\n\nBy the end, [eotg_kp.GetFirstName] suffered violent motor spasms and sensory distortion, the neurofracture tearing through every calculated thought."
 eotg_aug_kingpin.076.desc_end_flicker:0 "\n\nBy the end, [eotg_kp.GetFirstName] still hid it well: only a reflex that fired a moment early, and a step taken before the decision to take it." # from apply instructions
 eotg_aug_kingpin.076.a:0 "Execute [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.076.b:0 "Let [eotg_kp.GetFirstName] run the clinic for me now."

**Truth note:** L17: The Clinic Changes Hands. Reached from .013.e (front only). Front clinic seized and operated under realm law. Holds for front seizure.

## Debug Decision

 eotg_decision_aug_debug_kingpin:0 "Debug: Trigger Kingpin Story"
 eotg_decision_aug_debug_kingpin_desc:0 "Force-starts the Neurofractured Kingpin story cycle for testing purposes."
 eotg_decision_aug_debug_kingpin_tooltip:0 "Begins the kingpin event sequence."
 eotg_decision_aug_debug_kingpin_confirm:0 "Initiate Story"

**Truth note:** Valid across all relevant UI contexts and state checks.

## Modifiers

 eotg_mod_aug_kp_arrangement:0 "Underlevel Arrangement"
 eotg_mod_aug_kp_arrangement_desc:0 "A quiet understanding with the lower transit networks yields revenue at the cost of local trust."
 eotg_mod_aug_kp_hired_guns:0 "Hired Guns"
 eotg_mod_aug_kp_hired_guns_desc:0 "A detachment of hardened fighters has been retained to bolster realm defence."
 eotg_mod_aug_kp_network:0 "Criminal Network"
 eotg_mod_aug_kp_network_desc:0 "Extensive illicit operations channel tax revenues into your treasury while shielding you from rival schemes."
 eotg_mod_aug_kp_kept:0 "Under Their Hold"
 eotg_mod_aug_kp_kept_desc:0 "Blackmail and mounting pressure from the underlevels force you into harsh, erratic governance."
 eotg_mod_aug_kp_tribute:0 "Extorted Realm"
 eotg_mod_aug_kp_tribute_desc:0 "Regular tribute payments flow into the lower levels to maintain fragile civil peace."
 eotg_mod_aug_kp_informants:0 "Underlevel Informants"
 eotg_mod_aug_kp_informants_desc:0 "Turned contacts in the lower corridors provide early warning against hostile plots."
 eotg_mod_aug_kp_seized_clinic:0 "Seized Medical Facility"
 eotg_mod_aug_kp_seized_clinic_desc:0 "A former front has been converted into a legitimate realm clinic, generating steady revenue."
 eotg_mod_aug_kp_arson:0 "Transit Arson"
 eotg_mod_aug_kp_arson_desc:0 "Retaliatory sabotage and arson have disrupted storage depots and damaged local control."
 eotg_mod_aug_kp_lockdown:0 "Corridor Lockdown"
 eotg_mod_aug_kp_lockdown_desc:0 "Heavy barriers and strict patrols contain transit unrest at the expense of commercial growth."
 eotg_mod_aug_kp_loose_ends:0 "Splintered Gangs"
 eotg_mod_aug_kp_loose_ends_desc:0 "The elimination of leadership has sparked chaotic infighting among surviving underlevel crews."
 eotg_mod_aug_kp_streets_cleared:0 "Streets Cleared"
 eotg_mod_aug_kp_streets_cleared_desc:0 "Rigorous enforcement of realm law has restored civic order and earned vassal approval."
 eotg_mod_aug_kp_massacre:0 "Massacre Aftermath"
 eotg_mod_aug_kp_massacre_desc:0 "A horrific violent outbreak has left the populace traumatized and damaged realm development."

**Truth note:** Valid across all relevant UI contexts and state checks.

## Opinions

 eotg_opinion_aug_kp_order:0 "Restored Order"
 eotg_opinion_aug_kp_harboured:0 "Harboured Unstable Elements"
 eotg_opinion_aug_kp_raised_criminal:0 "Enfeoffed Underlevel Boss"
 eotg_opinion_aug_kp_warned:0 "Warned of Threat"

**Truth note:** Valid across all relevant UI contexts and state checks.

## Story Panel and Leverage Loc

 eotg_aug_kp_leverage_up_tt:0 "[eotg_kp.GetFirstName]'s hold on you deepens."
 eotg_aug_kp_leverage_down_tt:0 "[eotg_kp.GetFirstName]'s hold on you loosens."
 eotg_aug_kp_band_3:0 "They own the room"
 eotg_aug_kp_band_2:0 "Deep in their pocket"
 eotg_aug_kp_band_1:0 "A favour owed"
 eotg_story_aug_kingpin_info:0 "[Story.Custom('eotg_aug_kp_cl_leverage_band')]. Taking their money, doing their errands and keeping their secrets deepen it. Refusing them, turning their people and gathering evidence loosen it."
 eotg_story_aug_kingpin_kp_label:0 "Local Figure:"
 eotg_story_aug_kingpin_band_label:0 "Current Standing:"
 eotg_story_aug_kingpin_band_min_label:0 "Loose"
 eotg_story_aug_kingpin_band_max_label:0 "Tight"
 eotg_story_aug_kingpin:0 "The Neurofractured Boss"

**Truth note:** Valid across all relevant UI contexts and state checks.

## Toasts

 eotg_aug_kingpin_toast_dead:0 "Underlevel Boss Deceased"
 eotg_aug_kingpin_toast_gone:0 "Underlevel Boss Departed"

**Truth note:** Valid across all relevant UI contexts and state checks.

# BATCH B, provisional keys from spec §7

Provisional keys and text for Batch B events (.030–.039, .050, .063–.067, .072), drafted per spec §7.

## eotg_aug_kingpin.030

 eotg_aug_kingpin.030.a:0 "Raise the faction. Strike now."
 eotg_aug_kingpin.030.b:0 "Gather support first."
 eotg_aug_kingpin.030.c:0 "Walk away from it."
 eotg_aug_kingpin.030.desc:0 "The opportunity has arrived to challenge [eotg_kp_opponent.GetTitledFirstName] for the title of [eotg_kp_target.GetNameNoTier]. The claimant faction stands prepared to declare open rebellion, backed by armed squads and covert support from the lower levels."
 eotg_aug_kingpin.030.t:0 "The Claim"

**Truth note:** Fired from .003.b or .003.c for vassal ruler. Faction raised against liege for liege title. Holds whether ruler claims title or backs kingpin.

## eotg_aug_kingpin.031

 eotg_aug_kingpin.031.a:0 "Declare it."
 eotg_aug_kingpin.031.b:0 "Not yet."
 eotg_aug_kingpin.031.c:0 "Walk away."
 eotg_aug_kingpin.031.desc:0 "Across the border, [eotg_kp_rival.GetTitledFirstName] rules [eotg_kp_target.GetNameNoTier] with vulnerable borders and distracted guards. [eotg_kp.GetFirstName] proposes a sudden military strike: your banners will march, and the conquered domain will be placed in trusted hands."
 eotg_aug_kingpin.031.t:0 "The Neighbour's Seat"

**Truth note:** Fired from .003.b' for independent ruler against neighbouring rival. Starts claim war. Holds across all independent realms.

## eotg_aug_kingpin.032

 eotg_aug_kingpin.032.a:0 "Revoke it by decree."
 eotg_aug_kingpin.032.b:0 "Buy [eotg_kp_rival.GetFirstName] out."
 eotg_aug_kingpin.032.c:0 "Walk away."
 eotg_aug_kingpin.032.desc:0 "Tension within your realm offers a chance to reorder authority. [eotg_kp_rival.GetTitledFirstName] holds [eotg_kp_target.GetNameNoTier], but [eotg_kp.GetFirstName] urges you to revoke the seat by decree or buy out the title to install a hardened commander."
 eotg_aug_kingpin.032.t:0 "The Vassal's Seat"

**Truth note:** Fired from .003.c' for independent ruler with targeted vassal. Revoke or buy out seat. Holds whether ruler uses force or gold.

## eotg_aug_kingpin.033

 eotg_aug_kingpin.033.a_crew:0 "Let them."
 eotg_aug_kingpin.033.a_front:0 "Take the councillor's file."
 eotg_aug_kingpin.033.a_hired:0 "Pay."
 eotg_aug_kingpin.033.a_syndicate:0 "Buy."
 eotg_aug_kingpin.033.b_crew:0 "Keep them on the front."
 eotg_aug_kingpin.033.b_front:0 "Burn it."
 eotg_aug_kingpin.033.b_hired:0 "Not mid-war."
 eotg_aug_kingpin.033.b_syndicate:0 "No."
 eotg_aug_kingpin.033.c:0 "Keep [eotg_kp.GetFirstName] away from the line."
 eotg_aug_kingpin.033.t:0 "The War Below"

**Truth note:** Fired during war pulse T8. Profile opportunities during conflict. Holds across crew, syndicate, front, hired profiles.

## eotg_aug_kingpin.034

 eotg_aug_kingpin.034.a:0 "Outbid the other side."
 eotg_aug_kingpin.034.b:0 "Let them go."
 eotg_aug_kingpin.034.c:0 "Meet them at the hangar first."
 eotg_aug_kingpin.034.desc:0 "Alarming reports arrive from the front lines. The hired fighters have broken contract discipline: [eotg_kp.GetFirstName] has opened secret negotiations with the enemy, threatening to switch sides in the middle of battle unless a massive sum is paid immediately."
 eotg_aug_kingpin.034.t:0 "Turned Guns"

**Truth note:** Fired during war T8 for hired kind. Hired crew threatens betrayal. Holds for hired kind during active war.

## eotg_aug_kingpin.036

 eotg_aug_kingpin.036.a:0 "A Region of your own."
 eotg_aug_kingpin.036.b:0 "A seat at my court."
 eotg_aug_kingpin.036.c:0 "Loose ends."
 eotg_aug_kingpin.036.d:0 "You've been paid enough."
 eotg_aug_kingpin.036.desc:0 "The war is won and the title is yours, but [eotg_kp.GetFirstName] stands before your court expecting payment. The alliance that placed you upon the seat now demands its reward, and the partner will not be dismissed with empty thanks."
 eotg_aug_kingpin.036.t:0 "The Partner's Price"

**Truth note:** Fired upon winning claimant war for own claim. Boss demands payment. Holds whether ruler rewards, betrays, or denies partner.

## eotg_aug_kingpin.038

 eotg_aug_kingpin.038.a:0 "Strike."
 eotg_aug_kingpin.038.b:0 "Disband it."
 eotg_aug_kingpin.038.c:0 "Then it's done."
 eotg_aug_kingpin.038.desc:0 "The claimant faction has reached its limit of patience. The conspirators cannot remain hidden much longer without betrayal or exposure. It is time to launch the rebellion against [eotg_kp_opponent.GetTitledFirstName] or disband the network entirely."
 eotg_aug_kingpin.038.desc_discovered:0 "Disaster has struck before the strike could launch. Agents loyal to [eotg_kp_opponent.GetTitledFirstName] uncovered the conspiracy, capturing couriers and forcing the faction into open exposure."
 eotg_aug_kingpin.038.t:0 "Now or Never"

**Truth note:** Fired during stage pending T9. Faction must strike or disband. Holds across all pending claimant factions.

## eotg_aug_kingpin.039

 eotg_aug_kingpin.039.a:0 "Noted."
 eotg_aug_kingpin.039.b:0 "Put a bounty on [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.039.desc:0 "Word reaches your council that an insurgent faction has risen in the realm, supported by [eotg_kp.GetFirstName] and armed contingents from the lower levels. The rebels intend to press a claim against your rightful rule."
 eotg_aug_kingpin.039.t:0 "Word From the Docks"

**Truth note:** Fired on player liege when AI vassal starts claim war. Notification event. Holds on all player lieges facing kingpin rebellion.

## eotg_aug_kingpin.050

 eotg_aug_kingpin.050.a:0 "Do as [eotg_kp.GetFirstName] says."
 eotg_aug_kingpin.050.b:0 "Stall."
 eotg_aug_kingpin.050.c:0 "Not this one."
 eotg_aug_kingpin.050.d:0 "Do what mine already has me doing."
 eotg_aug_kingpin.050.desc:0 "[eotg_kp.GetFirstName] sends formal demands directly to your desk. No longer asking as a petitioner, the boss requires realm resources and authority to be deployed for the organization's objectives."
 eotg_aug_kingpin.050.t:0 "The Orders"

**Truth note:** Fired in stage kept T7. Boss demands realm compliance (squeeze, name, march, show). Options reflect submission, stall, refusal, or augmented resonance. Holds on all kept stages.

## eotg_aug_kingpin.063

 eotg_aug_kingpin.063.a:0 "Long may the new order endure."
 eotg_aug_kingpin.063.desc:0 "The war ends in complete victory. [eotg_kp.GetFirstName] ascends to the seat of [eotg_kp_target.GetNameNoTier], casting aside former syndicate ties to rule in [eotg_kp.GetHerHis] own right. The new liege grants generous rewards and honours the alliance that won the realm."
 eotg_aug_kingpin.063.desc_indep:0 "\n\nThe campaign is won, and [eotg_kp.GetFirstName] kneels before your bench as your newly installed vassal in [eotg_kp_target.GetNameNoTier]. The conquered domain is secured, and your court celebrates a bold expansion."
 eotg_aug_kingpin.063.desc_purge_half:0 "\n\nThe victory is complete, but [eotg_kp.GetFirstName]'s paranoia runs deep. The new ruler withholds half the promised reward, keeping records and leverage over you instead of equal fellowship."
 eotg_aug_kingpin.063.t:0 "Kingmaker"

**Truth note:** L4: The Liege's Seat. Reached upon winning claimant war for player's own claim. Boss rewarded or purged. Holds for own-claim victory.

## eotg_aug_kingpin.064

 eotg_aug_kingpin.064.a:0 "A clean ledger."
 eotg_aug_kingpin.064.desc:0 "The title is won, but true security requires that dangerous partners never present their bill. Before [eotg_kp.GetFirstName] could claim a share of the realm, loyal agents moved in the shadows. The former partner perished quietly, leaving no claims behind."
 eotg_aug_kingpin.064.t:0 "Before the Bill Came"

**Truth note:** L5: The Partner's Seat. Reached upon winning claimant war for boss's claim. Boss installed as independent ruler. Holds for boss-claim victory.

## eotg_aug_kingpin.065

 eotg_aug_kingpin.065.a:0 "A bitter defeat."
 eotg_aug_kingpin.065.desc:0 "The campaign has collapsed in ruin. Rather than sharing your defeat, [eotg_kp.GetFirstName] took every piece of correspondence and switched allegiance to the victor. Your enemy now holds your secrets, while your treasury pays the bitter price of betrayal."
 eotg_aug_kingpin.065.desc_indep:0 "\n\nAcross the border, [eotg_kp_rival.GetTitledFirstName] welcomes [eotg_kp.GetFirstName] into court, pressing fresh claims against your territories backed by your former partner's intelligence."
 eotg_aug_kingpin.065.t:0 "Sold to the Winner"

**Truth note:** L6: The Neighbour's Seat Won. Reached upon winning claim war against neighbour. Boss enfeoffed with conquered seat. Holds for external conquest.

## eotg_aug_kingpin.066

 eotg_aug_kingpin.066.a:0 "End it. Any terms."
 eotg_aug_kingpin.066.b:0 "Burn it all down."
 eotg_aug_kingpin.066.desc:0 "The conflict has degenerated into a brutal war of attrition. Neither side can achieve victory, and the lower levels of both domains burn with continuous sabotage and skirmishes. Smoke hangs in the ventilation ducts as the realm bleeds."
 eotg_aug_kingpin.066.desc_lost:0 "\n\nThe contested seat was destroyed in the fighting, leaving only charred bulkheads and ruined corridors in place of dynastic authority."
 eotg_aug_kingpin.066.t:0 "Every Level Burning"

**Truth note:** L7: Defeat. Reached upon losing claimant war. Player imprisoned or stripped of titles; boss flees or executed. Holds for war defeat.

## eotg_aug_kingpin.067

 eotg_aug_kingpin.067.a:0 "Let it land."
 eotg_aug_kingpin.067.b:0 "Pay [eotg_kp.GetFirstName] to soften it."
 eotg_aug_kingpin.067.c:0 "Hunt [eotg_kp.GetFirstName] down."
 eotg_aug_kingpin.067.desc:0 "[eotg_kp.GetFirstName] has turned against you. Every covert secret, every uninspected shipment, and every private communication has been delivered to your rivals or public heralds. The realm reels as your vulnerabilities are laid bare before your peers."
 eotg_aug_kingpin.067.desc_indep:0 "\n\nArmed dissidents in your outlying settlements rally around the leaked slates, preparing open rebellion against your rule."
 eotg_aug_kingpin.067.t:0 "The Turn"

**Truth note:** L8: The Turn. Reached from failed pending stage T9 or betrayal. Boss leaks secrets and finances rebellion. Holds for leak crisis.

## eotg_aug_kingpin.072

 eotg_aug_kingpin.072.a:0 "Do as [eotg_kp.GetSheHe] says."
 eotg_aug_kingpin.072.b:0 "No."
 eotg_aug_kingpin.072.c:0 "Do what mine already has me doing."
 eotg_aug_kingpin.072.desc:0 "The balance of power has completely shifted. [eotg_kp.GetFirstName] enters your private audience without guards or summons, setting down a list of realm directives. With enough leverage and evidence to destroy your rule, the boss no longer asks for favours."
 eotg_aug_kingpin.072.t:0 "The Hold Closes"

**Truth note:** L13: The Hold Closes. Reached from T2 (leverage >= 80, fracture/storm). Boss imposes complete dominance. Holds for crisis entry.

