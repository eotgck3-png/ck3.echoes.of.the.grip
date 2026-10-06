# Neurofractured Kingpin: Non-Fragment Event Text and Interface Strings (Gemini, Round 1)

Draft for `localization/english/eotg_aug_kingpin_l_english.yml`. Text only; no `.yml` or `.txt` edits.
Follows `docs/specs/cybernetics_v2_kingpin.md` §5.2, §5.4.2, §5.8, §7, §7.3, §7.4, §8.

## eotg_aug_kingpin.001

 eotg_aug_kingpin.001.t:0 "Word From Below"
 eotg_aug_kingpin.001.a:0 "Bring [eotg_kp.GetFirstName] to me. Quietly."
 eotg_aug_kingpin.001.b:0 "Arrest [eotg_kp.GetFirstName] before the next shift."
 eotg_aug_kingpin.001.c:0 "A quarrel in the underlevels. Leave it."
 eotg_aug_kingpin.001.d:0 "Ask the envoy to deal with [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.001.e:0 "Audit [eotg_kp.Custom('eotg_aug_cl_company')]'s client records."
 eotg_aug_kingpin.001.f_crew:0 "Pay them to keep their boss quiet."
 eotg_aug_kingpin.001.f_hired:0 "Buy out their next contract."

**Truth note:** Fired by yearly pulse on_action. Options branch into audience (.002), arrest (.010), open neglect, patron envoy (.074), audit (.015), or bribery/collaboration. Holds for any starting realm.

## eotg_aug_kingpin.002

 eotg_aug_kingpin.002.t:0 "The Audience"
 eotg_aug_kingpin.002.a:0 "Say what you came to say."
 eotg_aug_kingpin.002.b:0 "Guards. Now."
 eotg_aug_kingpin.002.c:0 "Smile. Agree. Remember all of it."
 eotg_aug_kingpin.002.d:0 "Does yours run ahead of you too?"

**Truth note:** Fired from .001.a or .014.b. Boss comes to private audience. Options provide dialogue, arrest, deceptive delay, or augmented recognition. Holds across all minds.

## eotg_aug_kingpin.003

 eotg_aug_kingpin.003.t:0 "The Offer"
 eotg_aug_kingpin.003.a:0 "We can work together."
 eotg_aug_kingpin.003.b:0 "Put me in [ROOT.Char.GetLiege.GetFirstName]'s seat."
 eotg_aug_kingpin.003.c:0 "Take the seat yourself. I'll hold the door."
 eotg_aug_kingpin.003.b_indep:0 "Take [eotg_kp_rival.GetFirstName]'s seat. My guns, your name."
 eotg_aug_kingpin.003.c_indep:0 "[eotg_kp_rival.GetFirstName]'s seat could be yours."
 eotg_aug_kingpin.003.d:0 "No. Get out."
 eotg_aug_kingpin.003.e_crew:0 "Keep the stacks quiet, and we talk again."
 eotg_aug_kingpin.003.e_syndicate:0 "Take your cut and look away."
 eotg_aug_kingpin.003.e_front:0 "Your files on [ROOT.Char.GetLiege.GetFirstName]. Now."
 eotg_aug_kingpin.003.e_hired:0 "I'll keep your guns on retainer."

**Truth note:** Fired from .002 or .012.b negotiation. Options offer partnership, claim support (vassal or independent), refusal, or profile-specific arrangements. Holds on all entry routes.

## eotg_aug_kingpin.004

 eotg_aug_kingpin.004.t:0 "The Ledger"
 eotg_aug_kingpin.004.desc:0 "A courier brings a sealed ledger and an uninspected cargo pouch to your chambers. Every entry records off-the-books transactions through the lower transit corridors, accompanied by a sizeable share set aside specifically for your seal."
 eotg_aug_kingpin.004.a:0 "Take it."
 eotg_aug_kingpin.004.b:0 "Take half. Log every credit."
 eotg_aug_kingpin.004.c:0 "Send it back."
 eotg_aug_kingpin.004.d:0 "Ask what the other half buys."

**Truth note:** Triggered in stage collab during yearly pulse T6 for syndicate kind or bribery method. Courier delivers underlevel revenues and ledger. Holds whether quiet arrangement or active collaboration.

## eotg_aug_kingpin.005

 eotg_aug_kingpin.005.t:0 "The Errand"
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

**Truth note:** Triggered in stage collab during yearly pulse T6. Variant options by method (violence, blackmail, infiltration, bribery). Holds across all kinds.

## eotg_aug_kingpin.006

 eotg_aug_kingpin.006.t:0 "The Episode"
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

**Truth note:** Triggered in stage collab during yearly pulse T6. Options vary by mind (purge, grandeur, forecast, cold). Holds across all organization kinds.

## eotg_aug_kingpin.007

 eotg_aug_kingpin.007.t:0 "The Informant"
 eotg_aug_kingpin.007.desc:0 "Your agents bring word of a hidden link: [eotg_kp_informant.GetFirstName] has been quietly passing household routines and patrol rosters down into the underlevels. The informant was caught copying schedule slates near the lower transit passages."
 eotg_aug_kingpin.007.a:0 "Arrest [eotg_kp_informant.GetFirstName]."
 eotg_aug_kingpin.007.b:0 "Turn [eotg_kp_informant.GetFirstName]."
 eotg_aug_kingpin.007.c:0 "Let [eotg_kp_informant.GetFirstName] be."

**Truth note:** Fired in stage collab T6 when method is infiltration and informant not unmasked. Informs ruler of breach. Holds whether informant is planted lieutenant or courtier.

## eotg_aug_kingpin.008

 eotg_aug_kingpin.008.t:0 "The Protection Bill"
 eotg_aug_kingpin.008.desc:0 "A message slate arrives from the lower levels, itemizing the costs of keeping the docks and lower corridors undisturbed. The demand is blunt: pay the maintenance levy, or watch fuel lines and warehouse depots succumb to mysterious accidents."
 eotg_aug_kingpin.008.a:0 "Pay it."
 eotg_aug_kingpin.008.b:0 "Not one credit."
 eotg_aug_kingpin.008.c:0 "Send the guard into the stacks."

**Truth note:** Fired in stage collab T6 for crew, hired, or violence method. Organization demands tribute for quiet. Holds on all qualifying profiles.

## eotg_aug_kingpin.009

 eotg_aug_kingpin.009.t:0 "The Lieutenant"
 eotg_aug_kingpin.009.desc:0 "[eotg_kp_lieutenant.GetTitledFirstName] requests a secret audience away from prying eyes. The lieutenant claims [eotg_kp.GetFirstName]'s neurological episodes have turned unpredictable and dangerous, offering full access to the hideout in exchange for immunity and safety."
 eotg_aug_kingpin.009.a:0 "Tell me everything."
 eotg_aug_kingpin.009.b:0 "Warn [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.009.c:0 "I never heard this."

**Truth note:** Fired in stage collab T6 (or T5 20%). Lieutenant offers to betray boss. Holds whether ruler collaborates or seeks evidence.

## eotg_aug_kingpin.010

 eotg_aug_kingpin.010.t:0 "The Arrest"
 eotg_aug_kingpin.010.a:0 "Take [eotg_kp.GetFirstName] alive."
 eotg_aug_kingpin.010.b:0 "Quietly, while [eotg_kp.GetSheHe] sleeps."
 eotg_aug_kingpin.010.c:0 "Call it off."

**Truth note:** Fired from .001.b, .002.b, .005.c, .009.a, .014.a. Ruler attempts to arrest boss. Martial/intrigue duel or calling off. Holds on all entry paths.

## eotg_aug_kingpin.011

 eotg_aug_kingpin.011.t:0 "The Crackdown"
 eotg_aug_kingpin.011.desc:0 "Your guards assemble at the blast doors leading into the underlevels, weapons drawn and riot shields locked. Down below, the barricades have gone up across the transit hubs, and the corridors echo with shouts as the assault begins."
 eotg_aug_kingpin.011.a:0 "Every level. Every door."
 eotg_aug_kingpin.011.b:0 "Lock the underlevels down."
 eotg_aug_kingpin.011.c:0 "Stand the guard down."

**Truth note:** Fired from .008.c or .012.a. Full security operation launched against underlevels. Holds across all combat branches.

## eotg_aug_kingpin.012

 eotg_aug_kingpin.012.t:0 "Retaliation"
 eotg_aug_kingpin.012.a:0 "Fight for every level."
 eotg_aug_kingpin.012.b:0 "Talk."
 eotg_aug_kingpin.012.c_crew:0 "Let them fall back to [eotg_kp_county.GetNameNoTier]."
 eotg_aug_kingpin.012.c_hired:0 "Pay their next contract elsewhere."
 eotg_aug_kingpin.012.c_front:0 "Let them publish."
 eotg_aug_kingpin.012.c_syndicate:0 "Pay what my guards were paid."

**Truth note:** Fired upon failed arrest (.010), failed audit (.015), or refusal (.003.d). Retaliation variants branch by kind. Holds on all entry routes.

## eotg_aug_kingpin.013

 eotg_aug_kingpin.013.t:0 "In Custody"
 eotg_aug_kingpin.013.desc:0 "[eotg_kp.GetFirstName] sits in the high-security holding cells, secured by magnetic clamps and heavy restraints. The diagnostic monitors at [eotg_kp.GetHerHis] temple pulse unevenly, but the prisoner remains silent under guard."
 eotg_aug_kingpin.013.a:0 "Execute [eotg_kp.GetFirstName]. Now."
 eotg_aug_kingpin.013.b:0 "A public trial, then every level cleared."
 eotg_aug_kingpin.013.c:0 "More use alive. Inside my court."
 eotg_aug_kingpin.013.d:0 "Give [eotg_kp.GetFirstName] a Region to keep quiet."
 eotg_aug_kingpin.013.e:0 "Seize the clinic and its records."
 eotg_aug_kingpin.013.f:0 "Hand [eotg_kp.GetFirstName] to the syndicate."

**Truth note:** Fired when boss is captured in .010, .011, or .015. Sentences branch to leaves L1, L2, L10, L11, L15, L17. Holds across all capture origins.

## eotg_aug_kingpin.014

 eotg_aug_kingpin.014.t:0 "Bodies on the Docks"
 eotg_aug_kingpin.014.desc:0 "Neglecting the underlevels has taken a bloody toll. Dock watchmen report a trail of casualties across the cargo bays: rival runners and unaligned porters beaten or slain without restraint as [eotg_kp.GetFirstName]'s faction tightens its control over transit."
 eotg_aug_kingpin.014.a:0 "Now we act."
 eotg_aug_kingpin.014.b:0 "Bring [eotg_kp.GetFirstName] in."
 eotg_aug_kingpin.014.c:0 "Not my quarrel."

**Truth note:** Fired in stage open during yearly pulse T5. Neglected underlevels erupt in violence. Holds whether crew, syndicate, or hired gang.

## eotg_aug_kingpin.015

 eotg_aug_kingpin.015.t:0 "The Audit"
 eotg_aug_kingpin.015.desc:0 "Your inspectors arrive at the premises of [eotg_kp.Custom('eotg_aug_cl_company')], demanding unhindered access to the consultation vaults and client ledger files. The front's attendants stall for time while couriers scramble behind locked security partitions."
 eotg_aug_kingpin.015.a:0 "Audit everything."
 eotg_aug_kingpin.015.b:0 "Buy the records quietly."
 eotg_aug_kingpin.015.c:0 "Leave the records sealed."

**Truth note:** Fired from .001.e for front kind. Inspectors audit clinic records. Stewardship duel rolls success (.013) or failure (.012). Holds for front kind.

## eotg_aug_kingpin.030

 eotg_aug_kingpin.030.t:0 "The Claim"
 eotg_aug_kingpin.030.desc:0 "The opportunity has arrived to challenge [eotg_kp_opponent.GetTitledFirstName] for the title of [eotg_kp_target.GetNameNoTier]. The claimant faction stands prepared to declare open rebellion, backed by armed squads and covert support from the lower levels."
 eotg_aug_kingpin.030.a:0 "Raise the faction. Strike now."
 eotg_aug_kingpin.030.b:0 "Gather support first."
 eotg_aug_kingpin.030.c:0 "Walk away from it."

**Truth note:** Fired from .003.b or .003.c for vassal ruler. Faction raised against liege for liege title. Holds whether ruler claims title or backs kingpin.

## eotg_aug_kingpin.031

 eotg_aug_kingpin.031.t:0 "The Neighbour's Seat"
 eotg_aug_kingpin.031.desc:0 "Across the border, [eotg_kp_rival.GetTitledFirstName] rules [eotg_kp_target.GetNameNoTier] with vulnerable borders and distracted guards. [eotg_kp.GetFirstName] proposes a sudden military strike: your banners will march, and the conquered domain will be placed in trusted hands."
 eotg_aug_kingpin.031.a:0 "Declare it."
 eotg_aug_kingpin.031.b:0 "Not yet."
 eotg_aug_kingpin.031.c:0 "Walk away."

**Truth note:** Fired from .003.b' for independent ruler against neighbouring rival. Starts claim war. Holds across all independent realms.

## eotg_aug_kingpin.032

 eotg_aug_kingpin.032.t:0 "The Vassal's Seat"
 eotg_aug_kingpin.032.desc:0 "Tension within your realm offers a chance to reorder authority. [eotg_kp_rival.GetTitledFirstName] holds [eotg_kp_target.GetNameNoTier], but [eotg_kp.GetFirstName] urges you to revoke the seat by decree or buy out the title to install a hardened commander."
 eotg_aug_kingpin.032.a:0 "Revoke it by decree."
 eotg_aug_kingpin.032.b:0 "Buy [eotg_kp_rival.GetFirstName] out."
 eotg_aug_kingpin.032.c:0 "Walk away."

**Truth note:** Fired from .003.c' for independent ruler with targeted vassal. Revoke or buy out seat. Holds whether ruler uses force or gold.

## eotg_aug_kingpin.033

 eotg_aug_kingpin.033.t:0 "The War Below"
 eotg_aug_kingpin.033.a_crew:0 "Let them."
 eotg_aug_kingpin.033.b_crew:0 "Keep them on the front."
 eotg_aug_kingpin.033.a_syndicate:0 "Buy."
 eotg_aug_kingpin.033.b_syndicate:0 "No."
 eotg_aug_kingpin.033.a_front:0 "Take the councillor's file."
 eotg_aug_kingpin.033.b_front:0 "Burn it."
 eotg_aug_kingpin.033.a_hired:0 "Pay."
 eotg_aug_kingpin.033.b_hired:0 "Not mid-war."
 eotg_aug_kingpin.033.c:0 "Keep [eotg_kp.GetFirstName] away from the line."

**Truth note:** Fired during stage war T8. Mid-war events by kind. Holds on all active war fronts.

## eotg_aug_kingpin.034

 eotg_aug_kingpin.034.t:0 "Turned Guns"
 eotg_aug_kingpin.034.desc:0 "Alarming reports arrive from the front lines. The hired fighters have broken contract discipline: [eotg_kp.GetFirstName] has opened secret negotiations with the enemy, threatening to switch sides in the middle of battle unless a massive sum is paid immediately."
 eotg_aug_kingpin.034.a:0 "Outbid the other side."
 eotg_aug_kingpin.034.b:0 "Let them go."
 eotg_aug_kingpin.034.c:0 "Meet them at the hangar first."

**Truth note:** Fired during war T8 for hired kind. Hired crew threatens betrayal. Holds for hired kind during active war.

## eotg_aug_kingpin.036

 eotg_aug_kingpin.036.t:0 "The Partner's Price"
 eotg_aug_kingpin.036.desc:0 "The war is won and the title is yours, but [eotg_kp.GetFirstName] stands before your court expecting payment. The alliance that placed you upon the seat now demands its reward, and the partner will not be dismissed with empty thanks."
 eotg_aug_kingpin.036.a:0 "A Region of your own."
 eotg_aug_kingpin.036.b:0 "A seat at my court."
 eotg_aug_kingpin.036.c:0 "Loose ends."
 eotg_aug_kingpin.036.d:0 "You've been paid enough."

**Truth note:** Fired upon winning claimant war for own claim. Boss demands payment. Holds whether ruler rewards, betrays, or denies partner.

## eotg_aug_kingpin.038

 eotg_aug_kingpin.038.t:0 "Now or Never"
 eotg_aug_kingpin.038.desc:0 "The claimant faction has reached its limit of patience. The conspirators cannot remain hidden much longer without betrayal or exposure. It is time to launch the rebellion against [eotg_kp_opponent.GetTitledFirstName] or disband the network entirely."
 eotg_aug_kingpin.038.desc_discovered:0 "Disaster has struck before the strike could launch. Agents loyal to [eotg_kp_opponent.GetTitledFirstName] uncovered the conspiracy, capturing couriers and forcing the faction into open exposure."
 eotg_aug_kingpin.038.a:0 "Strike."
 eotg_aug_kingpin.038.b:0 "Disband it."
 eotg_aug_kingpin.038.c:0 "Then it's done."

**Truth note:** Fired during stage pending T9. Faction must strike or disband. Holds across all pending claimant factions.

## eotg_aug_kingpin.039

 eotg_aug_kingpin.039.t:0 "Word From the Docks"
 eotg_aug_kingpin.039.desc:0 "Word reaches your council that an insurgent faction has risen in the realm, supported by [eotg_kp.GetFirstName] and armed contingents from the lower levels. The rebels intend to press a claim against your rightful rule."
 eotg_aug_kingpin.039.a:0 "Noted."
 eotg_aug_kingpin.039.b:0 "Put a bounty on [eotg_kp.GetFirstName]."

**Truth note:** Fired on player liege when AI vassal starts claim war. Notification event. Holds on all player lieges facing kingpin rebellion.

## eotg_aug_kingpin.040

 eotg_aug_kingpin.040.t:0 "The Inherited Hold"
 eotg_aug_kingpin.040.desc:0 "Upon succeeding to the realm, you find private records detailing an ongoing entanglement with [eotg_kp.GetFirstName]. Your predecessor left debts, secret compacts, and covert arrangements that now demand your attention."
 eotg_aug_kingpin.040.desc_open:0 "\n\nThe lower levels remain in unsettled neglect, with [eotg_kp.GetFirstName]'s network operating beyond official supervision."
 eotg_aug_kingpin.040.desc_collab:0 "\n\nA web of collaborative kickbacks and mutual obligations binds your treasury directly to the underlevel organization."
 eotg_aug_kingpin.040.desc_custody:0 "\n\n[eotg_kp.GetFirstName] remains held in your high-security cells, awaiting your personal decree regarding final sentence."
 eotg_aug_kingpin.040.desc_kept:0 "\n\nThe organization holds deep leverage over the bench, expecting ongoing subservience and regular concessions."
 eotg_aug_kingpin.040.desc_war:0 "\n\nAn active rebellion burns in the realm, initiated in partnership with [eotg_kp.GetFirstName]'s armed contingents."
 eotg_aug_kingpin.040.a:0 "Acknowledge the arrangement."
 eotg_aug_kingpin.040.b:0 "Repudiate the agreement."
 eotg_aug_kingpin.040.c:0 "Order the guards to find [eotg_kp.GetFirstName]."

**Truth note:** Fired on heir via on_owner_death when predecessor dies during active kingpin story. Desc variants reflect preceding stage (open, collab, custody, kept, war). Holds for all inherited stories.

## eotg_aug_kingpin.050

 eotg_aug_kingpin.050.t:0 "The Orders"
 eotg_aug_kingpin.050.desc:0 "[eotg_kp.GetFirstName] sends formal demands directly to your desk. No longer asking as a petitioner, the boss requires realm resources and authority to be deployed for the organization's objectives."
 eotg_aug_kingpin.050.a:0 "Do as [eotg_kp.GetFirstName] says."
 eotg_aug_kingpin.050.b:0 "Stall."
 eotg_aug_kingpin.050.c:0 "Not this one."
 eotg_aug_kingpin.050.d:0 "Do what mine already has me doing."

**Truth note:** Fired in stage kept T7. Boss demands realm compliance (squeeze, name, march, show). Options reflect submission, stall, refusal, or augmented resonance. Holds on all kept stages.

## eotg_aug_kingpin.060

 eotg_aug_kingpin.060.t:0 "A Quick Ending"
 eotg_aug_kingpin.060.desc:0 "The hearing is brief and held behind closed doors. Under your personal order, [eotg_kp.GetFirstName] is escorted to the far corridor of the cells. The sentence is carried out without ceremony or delay, and the lower levels are left without a head."
 eotg_aug_kingpin.060.a:0 "It's done."
 eotg_aug_kingpin.060.b:0 "Give [eotg_kp.GetHerHim] proper rites."

**Truth note:** L1: A Quick Ending. Reached from .013.a. Execution under ruler's personal order. Holds for any kind.

## eotg_aug_kingpin.061

 eotg_aug_kingpin.061.t:0 "The Streets Go Quiet"
 eotg_aug_kingpin.061.desc:0 "The public trial concludes under the realm's own law. Evidence compiled by your clerks is read aloud, and sentence is pronounced from your bench. Systematic sweeps clear every transit corridor, restoring unbroken order across the lower levels."
 eotg_aug_kingpin.061.a:0 "Execute [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.061.b:0 "The cells, for life."

**Truth note:** L2: The Streets Go Quiet. Reached from .013.b. Public trial under realm law. Holds for any kind.

## eotg_aug_kingpin.062

 eotg_aug_kingpin.062.t:0 "The Network Is Yours"
 eotg_aug_kingpin.062.desc:0 "Years of quiet cooperation come to an end with a sudden medical report. [eotg_kp.GetFirstName] suffered fatal neural cascade in private quarters. With the boss gone and every ledger already in your hands, the entire organization passes smoothly to your control."
 eotg_aug_kingpin.062.a:0 "Keep it running."
 eotg_aug_kingpin.062.b:0 "Burn the ledgers."
 eotg_aug_kingpin.062.c:0 "Expand it."

**Truth note:** L3: The Network Is Yours. Reached from T4 (syndicate/front). Boss dies of neural cascade, leaving network to ruler. Holds for long deals.

## eotg_aug_kingpin.063

 eotg_aug_kingpin.063.t:0 "Kingmaker"
 eotg_aug_kingpin.063.desc:0 "The war ends in complete victory. [eotg_kp.GetFirstName] ascends to the seat of [eotg_kp_target.GetNameNoTier], casting aside former syndicate ties to rule in [eotg_kp.GetHerHis] own right. The new liege grants generous rewards and honours the alliance that won the realm."
 eotg_aug_kingpin.063.desc_indep:0 "\n\nThe campaign is won, and [eotg_kp.GetFirstName] kneels before your bench as your newly installed vassal in [eotg_kp_target.GetNameNoTier]. The conquered domain is secured, and your court celebrates a bold expansion."
 eotg_aug_kingpin.063.desc_purge_half:0 "\n\nThe victory is complete, but [eotg_kp.GetFirstName]'s paranoia runs deep. The new ruler withholds half the promised reward, keeping records and leverage over you instead of equal fellowship."
 eotg_aug_kingpin.063.a:0 "Long may the new order endure."

**Truth note:** L4: Kingmaker. Reached from M3 victory (back_kp, neighbour). Kingpin takes conquered seat. Holds for vassal and independent variants.

## eotg_aug_kingpin.064

 eotg_aug_kingpin.064.t:0 "Before the Bill Came"
 eotg_aug_kingpin.064.desc:0 "The title is won, but true security requires that dangerous partners never present their bill. Before [eotg_kp.GetFirstName] could claim a share of the realm, loyal agents moved in the shadows. The former partner perished quietly, leaving no claims behind."
 eotg_aug_kingpin.064.a:0 "A clean ledger."

**Truth note:** L5: Before the Bill Came (§7.4 retitle). Reached from .036.c success. Ruler murders partner after winning title. Holds for own-claim victory.

## eotg_aug_kingpin.065

 eotg_aug_kingpin.065.t:0 "Sold to the Winner"
 eotg_aug_kingpin.065.desc:0 "The campaign has collapsed in ruin. Rather than sharing your defeat, [eotg_kp.GetFirstName] took every piece of correspondence and switched allegiance to the victor. Your enemy now holds your secrets, while your treasury pays the bitter price of betrayal."
 eotg_aug_kingpin.065.desc_indep:0 "\n\nAcross the border, [eotg_kp_rival.GetTitledFirstName] welcomes [eotg_kp.GetFirstName] into court, pressing fresh claims against your territories backed by your former partner's intelligence."
 eotg_aug_kingpin.065.a:0 "A bitter defeat."

**Truth note:** L6: Sold to the Winner (§7.4 retitle). Reached from M3 loss or white peace. Boss defects to victor with secrets. Holds for lost claim wars.

## eotg_aug_kingpin.066

 eotg_aug_kingpin.066.t:0 "Every Level Burning"
 eotg_aug_kingpin.066.desc:0 "The conflict has degenerated into a brutal war of attrition. Neither side can achieve victory, and the lower levels of both domains burn with continuous sabotage and skirmishes. Smoke hangs in the ventilation ducts as the realm bleeds."
 eotg_aug_kingpin.066.desc_lost:0 "\n\nThe contested seat was destroyed in the fighting, leaving only charred bulkheads and ruined corridors in place of dynastic authority."
 eotg_aug_kingpin.066.a:0 "End it. Any terms."
 eotg_aug_kingpin.066.b:0 "Burn it all down."

**Truth note:** L7: Every Level Burning (§7.4 retitle). Reached from M4 spiral or lost vassal seat. Long civil war burns lower levels. Holds for prolonged war.

## eotg_aug_kingpin.067

 eotg_aug_kingpin.067.t:0 "The Turn"
 eotg_aug_kingpin.067.desc:0 "[eotg_kp.GetFirstName] has turned against you. Every covert secret, every uninspected shipment, and every private communication has been delivered to your rivals or public heralds. The realm reels as your vulnerabilities are laid bare before your peers."
 eotg_aug_kingpin.067.desc_indep:0 "\n\nArmed dissidents in your outlying settlements rally around the leaked slates, preparing open rebellion against your rule."
 eotg_aug_kingpin.067.a:0 "Let it land."
 eotg_aug_kingpin.067.b:0 "Pay [eotg_kp.GetFirstName] to soften it."
 eotg_aug_kingpin.067.c:0 "Hunt [eotg_kp.GetFirstName] down."

**Truth note:** L8: The Turn (§7.4 retitle). Reached from T3, refusal chain, or betrayal. Boss leaks secrets or starts faction. Holds across all non-war betrayals.

## eotg_aug_kingpin.068

 eotg_aug_kingpin.068.t:0 "The Break"
 eotg_aug_kingpin.068.desc:0 "The final collapse arrived with sudden, catastrophic violence. [eotg_kp.GetFirstName]'s neurological restraints gave way entirely. Coming up to the residence in a blind frenzy, the boss tore through corridors, leaving bodies and wreckage in the residence before retreating below."
 eotg_aug_kingpin.068.desc_none:0 "\n\nThough no courtiers fell, several service attendants were wounded before the household guard forced the assailant back into the stairwells."
 eotg_aug_kingpin.068.desc_war:0 "\n\nThe violence erupted across both the frontline encampments and the command staff, shattering the rebellion in a single bloody night."
 eotg_aug_kingpin.068.a:0 "Hunt [eotg_kp.GetFirstName] down. Now."
 eotg_aug_kingpin.068.b:0 "Seal the lower levels and count the dead."
 eotg_aug_kingpin.068.c:0 "Go down there yourself."

**Truth note:** L9: The Break. Reached from T1, .011 failure (Storm), or resistance. Boss has violent psychotic outbreak coming up to residence. Holds for violent collapse.

## eotg_aug_kingpin.069

 eotg_aug_kingpin.069.t:0 "A Seat Under You"
 eotg_aug_kingpin.069.desc:0 "The long dispute is resolved by formal enfeoffment. [eotg_kp.GetFirstName] is granted a landed domain of the realm, trading shadowy control of the underlevels for the duties of a recognized vassal. The court murmurs at the appointment, but the streets are pacified."
 eotg_aug_kingpin.069.desc_held:0 "\n\nHaving defended the seat by force of arms during the recent conflict, the new vassal's hold upon the territory is undisputed."
 eotg_aug_kingpin.069.a:0 "Welcome my newest vassal."

**Truth note:** L10: A Seat Under You. Reached from .013.d, .032.a/b, .036.a, M3 held. Boss enfeoffed as landed vassal. Holds across all grant routes.

## eotg_aug_kingpin.070

 eotg_aug_kingpin.070.t:0 "Brought Inside"
 eotg_aug_kingpin.070.desc:0 "Realizing that [eotg_kp.GetFirstName] is too capable to execute and too dangerous to leave outside, you bring the former criminal into your household. Assigned a discreet post within your personal retinue, [eotg_kp.GetSheHe] now directs [eotg_kp.GetHerHis] talents in your service."
 eotg_aug_kingpin.070.a:0 "Keep [eotg_kp.GetFirstName] close."
 eotg_aug_kingpin.070.b:0 "Keep [eotg_kp.GetFirstName] closer: a post where I can see [eotg_kp.GetHerHim]."

**Truth note:** L11: Brought Inside. Reached from .013.c or .036.b. Boss recruited into ruler's household as courtier. Holds for recruitment paths.

## eotg_aug_kingpin.071

 eotg_aug_kingpin.071.t:0 "The Region Falls"
 eotg_aug_kingpin.071.desc:0 "Pushed beyond accommodation, the crew withdrew into the depots of the region where they keep their munitions. Fortifying the transit stations and declaring their own rule, they have severed ties with your court, leaving the domain entirely beyond your immediate reach."
 eotg_aug_kingpin.071.a:0 "A wound that will be answered."

**Truth note:** L12: The Region Falls. Reached from .012.c or .014.c (crew only). Crew falls back to depots and seizes region. Holds for crew independence.

## eotg_aug_kingpin.072

 eotg_aug_kingpin.072.t:0 "The Hold Closes"
 eotg_aug_kingpin.072.desc:0 "The balance of power has completely shifted. [eotg_kp.GetFirstName] enters your private audience without guards or summons, setting down a list of realm directives. With enough leverage and evidence to destroy your rule, the boss no longer asks for favours."
 eotg_aug_kingpin.072.a:0 "Do as [eotg_kp.GetSheHe] says."
 eotg_aug_kingpin.072.b:0 "No."
 eotg_aug_kingpin.072.c:0 "Do what mine already has me doing."

**Truth note:** L13: The Hold Closes. Reached from T2 (leverage >= 80, fracture/storm). Boss imposes complete dominance. Holds for crisis entry.

## eotg_aug_kingpin.073

 eotg_aug_kingpin.073.t:0 "A Standing Arrangement"
 eotg_aug_kingpin.073.desc:0 "Neither side could achieve a decisive advantage, leading to a weary compromise. A regular allocation of realm revenues flows down into the underlevels, and in return the organization ensures that violence and unrest remain strictly suppressed."
 eotg_aug_kingpin.073.desc_contract:0 "\n\nA renewed service contract formalizes the financial understanding, setting exact figures for each month of peace."
 eotg_aug_kingpin.073.a:0 "It's cheaper than a war."
 eotg_aug_kingpin.073.b:0 "Until I find a way."

**Truth note:** L14: A Standing Arrangement. Reached from T4, T7, .011 failure. Extortion stalemate where tribute buys quiet. Holds for stable truce.

## eotg_aug_kingpin.074

 eotg_aug_kingpin.074.t:0 "The Syndicate Settles It"
 eotg_aug_kingpin.074.desc:0 "The syndicate has resolved its internal liability. Unwilling to let [eotg_kp.GetFirstName]'s neurological instability jeopardize wider operations, quiet enforcers arrived from the outer transit routes. The former boss was removed without a trace, leaving the docks quiet once more."
 eotg_aug_kingpin.074.desc_patron:0 "\n\nThe patron's envoy confirms that the account is marked settled, though the ledger of personal obligations between you remains open."
 eotg_aug_kingpin.074.a:0 "A quiet resolution."

**Truth note:** L15: The Syndicate Settles It (§7.4 retitle). Reached from .001.d or .013.f (syndicate only). Syndicate cleans up boss. Holds for syndicate removal.

## eotg_aug_kingpin.075

 eotg_aug_kingpin.075.t:0 "The Fracture Finishes It"
 eotg_aug_kingpin.075.desc:0 "Without intervention or sudden violence, the failing implant simply burned out its host. Attendants found [eotg_kp.GetFirstName] lifeless in private quarters, the cranial port cold and dark after a fatal neurological cascade. The organization splinters in silence."
 eotg_aug_kingpin.075.a:0 "Let the quiet remain."

**Truth note:** L16: The Fracture Finishes It. Reached from T1 (pressure >= 95). Boss dies of unassisted cascade. Holds for natural termination.

## eotg_aug_kingpin.076

 eotg_aug_kingpin.076.t:0 "The Clinic Changes Hands"
 eotg_aug_kingpin.076.desc:0 "Under your direct authority, the surgical rooms and records vaults of [eotg_kp.Custom('eotg_aug_cl_company')] have been seized. Its diagnostic archives now belong to your court, providing your household with a fully operational clinic under your own law."
 eotg_aug_kingpin.076.a:0 "Execute [eotg_kp.GetFirstName]."
 eotg_aug_kingpin.076.b:0 "Let [eotg_kp.GetFirstName] run the clinic for me now."

**Truth note:** L17: The Clinic Changes Hands. Reached from .013.e (front only). Front clinic seized and operated under realm law. Holds for front seizure.

## Tooltips and Combat Outcomes

 eotg_aug_kp.duel_arrest.success:0 "You successfully subdue [eotg_kp.GetFirstName] and secure [eotg_kp.GetHerHim] in restraints."
 eotg_aug_kp.duel_arrest.failure:0 "[eotg_kp.GetFirstName] breaks through your guard and escapes into the corridors."
 eotg_aug_kp.duel_blackmail.success:0 "You turn the incriminating records against [eotg_kp.GetFirstName]."
 eotg_aug_kp.duel_blackmail.failure:0 "[eotg_kp.GetFirstName] outmanoeuvres your agents and deepens [eotg_kp.GetHerHis] advantage."
 eotg_aug_kp.duel_turn.success:0 "You persuade [eotg_kp_informant.GetFirstName] to serve as your double agent."
 eotg_aug_kp.duel_turn.failure:0 "[eotg_kp_informant.GetFirstName] refuses your overtures and warns the organization."
 eotg_aug_kp.duel_hangar.success:0 "You defeat [eotg_kp.GetFirstName] in combat and prevent the hired force from turning."
 eotg_aug_kp.duel_hangar.failure:0 "[eotg_kp.GetFirstName] overpowers you, and the mercenaries defect to the enemy."
 eotg_aug_kp.duel_hunt.success:0 "Your hunters corner [eotg_kp.GetFirstName] and strike [eotg_kp.GetHerHim] down."
 eotg_aug_kp.duel_hunt.failure:0 "[eotg_kp.GetFirstName] evades your agents and slips away into the underlevels."
 eotg_aug_kp.duel_loose_ends.success:0 "You eliminate [eotg_kp.GetFirstName] before [eotg_kp.GetSheHe] can demand payment."
 eotg_aug_kp.duel_loose_ends.failure:0 "[eotg_kp.GetFirstName] anticipates the strike and retaliates against your rule."
 eotg_aug_kp_leverage_up_tt:0 "[eotg_kp.GetFirstName]'s hold on you deepens."
 eotg_aug_kp_leverage_down_tt:0 "[eotg_kp.GetFirstName]'s hold on you loosens."
 eotg_aug_kingpin_toast_gone:0 "Underlevel Boss Departed"
 eotg_aug_kingpin_toast_dead:0 "Underlevel Boss Deceased"
 eotg_aug_kp_army_name:0 "Underlevel Cohort"

**Truth note:** Valid across all relevant UI contexts and state checks.

## Story Panel Loc

 eotg_story_aug_kingpin:0 "The Neurofractured Boss"
 eotg_story_aug_kingpin_info:0 "[Story.Custom('eotg_aug_kp_cl_leverage_band')]. Taking their money, doing their errands and keeping their secrets deepen it. Refusing them, turning their people and gathering evidence loosen it."
 eotg_story_aug_kingpin_kp_label:0 "Local Figure:"
 eotg_story_aug_kingpin_band_label:0 "Current Standing:"
 eotg_story_aug_kingpin_band_min_label:0 "Loose"
 eotg_story_aug_kingpin_band_max_label:0 "Tight"
 eotg_aug_kp_band_1:0 "A favour owed"
 eotg_aug_kp_band_2:0 "Deep in their pocket"
 eotg_aug_kp_band_3:0 "They own the room"

**Truth note:** Valid across all relevant UI contexts and state checks.

## Modifiers

 eotg_mod_aug_kp_arrangement:0 "Underlevel Arrangement"
 eotg_mod_aug_kp_arrangement_desc:0 "A quiet understanding with the lower transit networks yields revenue at the cost of local trust."
 eotg_mod_aug_kp_hired_guns:0 "Hired Guns"
 eotg_mod_aug_kp_hired_guns_desc:0 "A detachment of hardened fighters has been retained to bolster realm defence."
 eotg_mod_aug_kp_network:0 "Criminal Network"
 eotg_mod_aug_kp_network_desc:0 "Extensive illicit operations channel tax revenues into your treasury while shielding you from rival schemes."
 eotg_mod_aug_kp_exposed:0 "Compromised Standing"
 eotg_mod_aug_kp_exposed_desc:0 "Damaging secrets and compromised records have eroded your authority and invited vassal suspicion."
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
 eotg_mod_aug_kp_crisis:0 "Underlevel Crisis"
 eotg_mod_aug_kp_crisis_desc:0 "Entrenched criminal dominance has suppressed trade, drained recruitment, and alarmed the population."
 eotg_mod_aug_kp_burned_levels:0 "Burned Transit Levels"
 eotg_mod_aug_kp_burned_levels_desc:0 "Devastating civil conflict has wrecked lower infrastructure, crippling development and levies."
 eotg_mod_aug_kp_massacre:0 "Massacre Aftermath"
 eotg_mod_aug_kp_massacre_desc:0 "A horrific violent outbreak has left the populace traumatized and damaged realm development."

**Truth note:** Valid across all relevant UI contexts and state checks.

## Opinions

 eotg_opinion_aug_kp_order:0 "Restored Order"
 eotg_opinion_aug_kp_kingmaker:0 "Kingmaker"
 eotg_opinion_aug_kp_conspired:0 "Conspired with Criminals"
 eotg_opinion_aug_kp_harboured:0 "Harboured Unstable Elements"
 eotg_opinion_aug_kp_raised_criminal:0 "Enfeoffed Underlevel Boss"
 eotg_opinion_aug_kp_warned:0 "Warned of Threat"

**Truth note:** Valid across all relevant UI contexts and state checks.

## Debug Decision

 eotg_decision_aug_debug_kingpin:0 "Debug: Trigger Kingpin Story"
 eotg_decision_aug_debug_kingpin_desc:0 "Force-starts the Neurofractured Kingpin story cycle for testing purposes."
 eotg_decision_aug_debug_kingpin_tooltip:0 "Begins the kingpin event sequence."
 eotg_decision_aug_debug_kingpin_confirm:0 "Initiate Story"

**Truth note:** Valid across all relevant UI contexts and state checks.

