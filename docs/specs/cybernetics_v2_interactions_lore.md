# Lore review: cybernetics_v2_interactions.md (binding for script and loc)

**eotg-lore-keeper, 2026-10-04.** Approved, with seven must-fix items (I1–I7). The mechanics break no canon:
- nothing acts at a distance;
- no authority sits above the polity;
- no named implant players;
- Nikios is untouched.

## Must-fix
- **I1.** Retitle tamper.004 to **"A Fault in the Hardware"**. The old title, "Something in the Hardware", implied a presence inside it.
- **I2.** tamper.004 shows bodily and hardware symptoms only: the overlay stutters, a sensor drifts, a limb responds late. No forecast arriving. Use "responds", never "answers".
- **I3.** `eotg_aug_proc.outcome_repair_failed` must be injury-neutral: "\n\nThe repair did not take. The part sits where it was fitted and does nothing, and nothing is better than it was." This supersedes the line in the procedures lore file.
- **I4. Salvage register.**
  - Never harvest, reap, farm, "strip for parts", or scrap/wreck applied to the person.
  - No gore past init.012 ("the socket is empty and raw").
  - Removed hardware carries nothing of its wearer: no memory, replay or connection, and never "someone else wears it now".
- **I5. Tracing uses physical evidence only:** tool marks, a replaced seal, a bribed technician who talks, who had access. At most, the implant's own record of a change made at its panel. Never a connection log, a signal path, or a network trace.
- **I6. Tampering.**
  - "A dose" is a sedative for the sleeper, never an agent that acts on the hardware (no nanites).
  - Firmware is changed only by hand at an open panel.
  - The QA grep adds `hack|virus|upload|network|harvest`.
- **I7.** `cybernetics_v2.md` thread T2: "Remote Throttle" becomes "the firmware throttle".

## Rulings
- **Seamless exclusions.** Excluding Seamless characters from Demand Removal, Tamper and Examine is upheld. At 866 tech, no surgeon can find where Seamless hardware ends and the body begins.
- **Salvage of Seamless prisoners.** The human decides. Lore recommends option A, exclude. Option B (forced death) is not recommended.
- **Salvage tone at 866:** approved. Keep the trade unnamed: the buyer is only "a dealer" or "someone who asks no questions". The prose is clinical; the cruelty is the actor's choice.
- **Healthy children.** The human decides. Lore recommends adults only: init.014 says the procedure is "never done on the very young".
- **Titles:**
  - Approved: *The Physician's Report*, *What Came Out*, *The Work Is Done*, *Hands Withdrawn*, *Offer Augmentation*, *Have Them Examined*, *Tamper with Implants*.
  - Change: *Demand Implant Removal* (bare "Removal" reads as removal from office) and *Salvage Implants* (bare "Salvage" reads as rescue).
  - Opinion `_salvaged_me` becomes **"Cut Out My Implants"**.
- **Throttle desc** (the shipped modifier): "The syndicate's technicians wrote a throttle into the firmware at installation, held off by a renewal they entered at each servicing. The servicing has stopped, and the throttle has engaged. It is set low, and it has not been found. The body feels the limit as stress and weakness." The trigger is a local absence, not a remote signal.
- **Gendered N1–N3** in new_beats: ratified (see new_beats §11).
- **Noted for later (CB board):** vanilla scheme agent names ("Physic", "Smith", "Footpad") and the generic scheme-ongoing loc are medieval leaks. They affect every scheme in the mod and belong to the vanilla reflavor pass.

## Renderings
The localizer may polish these. No numbers, and no "risk", "odds" or "chance". Appended lines start with `\n\n`.

**Interactions**
- **Offer Augmentation:** "Offer Augmentation"
  - _desc "Pay for their first implants, and choose whose hands do the fitting."
  - _notification "[actor.GetName] offers to pay for implants, fitted by hands of [actor.GetHerHis] choosing."
- **Demand Implant Removal:** "Demand Implant Removal"
  - _desc "Order them to have every implant taken out. You pay, and you choose whose hands do it."
  - _notification "[actor.GetName] demands that your implants come out."
- **Have Them Examined:** "Have Them Examined"
  - _desc "Have your physician look over their hardware and report what is found."
- **Tamper with Implants:** "Tamper with Implants"
- **Salvage Implants:** "Salvage Implants"
  - _desc "Have the prisoner's implants cut out, for their value. The prisoner's comfort is not the point."

**Send options**
- heading "Whose hands"
- clinic "A sanctioned clinic"
  - _tt "A team, a table and records. The full price."
- physician "My own physician"
  - _tt "Your physician does the work, for less than a clinic charges."
- backstreet "The back streets"
  - _tt "Cheap, quick and unvetted. No one keeps a record."
- rough "Whoever is at hand"
  - _tt "It costs nothing, and no one takes care with what else comes out."

**Tamper start**
- approved_tt "You can start a scheme to tamper with [recipient.GetName]'s implants."
- notification "Scheme started: Tamper with Implants"
- agent_focus tooltips: vanilla `start_abduct.tt.*` format.

**Toasts and tooltips**
- offer_accepted "[recipient.GetName] Accepts the Implants"
- offer_declined "[recipient.GetName] Declines the Implants"
- demand_accepted "[recipient.GetName] Agrees to the Removal"
- demand_declined "[recipient.GetName] Refuses the Removal"
- examine_declined "[recipient.GetName] Will Not Be Examined"
- demand_removal_effect_tt "Every implant comes out. How it goes is decided on the table."
- salvage_effect_tt "The hardware comes out. What else comes with it is decided on the table."
- tamper_foiled "Hands on My Hardware", body "[owner.GetName]'s agents were caught at your implants."

**`ai_accept` descs**
- LIEGE "Their liege's wish"
- AMBITIOUS "Ambitious"
- CYNICAL "Cynical"
- BRAVE "Brave"
- GREEDY "Greedy"
- LOSS "Wants what was lost restored"
- CRAVEN "Craven"
- CONTENT "Content"
- PARANOID "Paranoid"
- HUMBLE "Humble"
- ZEALOUS "Zealous"
- FORMER "Has had implants taken out before"
- CLINIC "A sanctioned clinic does the work"
- PHYSICIAN "A physician does the work"
- BACKSTREET "Back-street hands"
- TIER_AUGMENTED "Only lightly augmented"
- TIER_ENHANCED "Enhanced"
- TIER_OVERCLOCKED "Overclocked"
- STUBBORN "Stubborn"
- ARROGANT "Arrogant"
- STRESS "Under strain"
- COUNTDOWN "Their hardware is failing"
- ILLEGAL "Black-market implants"
- TRUSTING "Trusting"
- DECEITFUL "Deceitful"

**Scheme**
- name "Tamper with Implants"
- _action "Tampering with Implants"
- _desc_general "Get hands on a target's hardware while no one is watching, and leave it worse than it was fitted."
- _desc "Agents need one night, an open maintenance hatch, and a target who does not wake."
- SUCCESS_DESC "The target's hardware is left with a fault. It misbehaves, and whoever opens it next will find the work harder."
- DISCOVERY_DESC "If the target learns whose hands it was, they gain a reason to imprison you."
- Invalidation:
  - invalidated_title "Tampering Abandoned"
  - _dead "[target.GetName] is dead. There is no one left to work on."
  - _removed "[target.GetName]'s hardware is out of reach: taken out, or integrated past anything the agents could open."
- Success-chance modifiers:
  - TARGET_PHYSICIAN "A physician checks their hardware"
  - TARGET_ILLEGAL "Back-street hardware, no seals on the panels"
  - TARGET_HARDENED "Overclocked hardware is watched"
  - TARGET_FRACTURED "Restrained or sedated, and handled by wardens"
  - OWNER_KNOWS "Knows how this hardware is fitted"

**Opinions**
- forced_procedure "Forced Procedure"
- demanded_removal "Demanded Implant Removal"
- salvaged_me "Cut Out My Implants"
- salvaged_family_member "Cut Out a Relative's Implants"
- tampered "Tampered with My Implants"

**int.001 *The Physician's Report***
- .desc "The examination is finished. The report on [eotg_examined.GetName]'s hardware is short and plain."
- Band lines:
  - .desc_fractured "\n\nThe hardware is unstable. The readings will not hold still long enough to be written down."
  - .desc_oc_bad "\n\nThe overclocked units are running hot, and have been for some time."
  - .desc_oc_ok "\n\nThe overclocked units run hot, but within tolerance."
  - .desc_stable "\n\nEverything is within tolerance. The fittings are clean."
- Appended lines:
  - .desc_flaw "\n\nOne unit is not what it was sold as. The part is cheaper than its casing claims, and it will not last."
  - .desc_tampered "\n\nSomeone has had a panel open. The seals have been replaced, and the calibration is not as it was fitted."
  - .desc_infection "\n\nThe tissue around the fittings is inflamed, and there is debris in it that should have come out."
  - .desc_illegal "\n\nIt is back-street work: no maker's marks, no records, fittings filed to size."
- Options:
  - .a "Treat what you can."
  - .b "Fix the fault."
  - .c "Note it."
  - .d "Trace the tampering."
  - .e "Let me do it myself."
- .b.tt "The fault is opened up and reworked. How it goes is decided on the table."
- .d.success "Tool marks, a replaced seal, and a technician who talked. It leads to [eotg_saboteur.GetName]."
- .d.failure "The trail goes cold. Whoever opened the panel left nothing to follow."

**int.002 *What Came Out***
- .desc "The hardware taken from [recipient.GetName] has been cleaned and laid out on a tray. It is yours to do with as you like."
- Tier lines:
  - .desc_augmented "\n\nFirst-tier work: a handful of units on standard fittings. Worth something, not much."
  - .desc_enhanced "\n\nA full set of enhancements, well kept. A dealer would pay properly for it."
  - .desc_overclocked "\n\nOverclocked hardware, scorched along the heat sinks and still worth a great deal. Few can afford to buy it new."
  - .desc_fractured "\n\nOverclocked hardware, worn past its limits. The casings are scored and the cabling is fused in places. It still sells."
- Outcome lines:
  - .desc_died "\n\n[recipient.GetName] did not survive the table. The hardware came out anyway."
  - .desc_maimed "\n\nIt did not come out cleanly. [recipient.GetName] lost more on the table than the hardware."
  - .desc_fragments "\n\nNot all of it came out. What is left in [recipient.GetName] will stay there."
- Options:
  - .a "Sell it to a dealer."
  - .b "Have it fitted to me."
  - .c "Keep it for spare parts."
  - .d "Destroy it."
  - .e "Take it apart. Learn how it was made."

**tamper.002 *The Work Is Done***
- .desc "The agents report before dawn. For one night [target.GetName]'s hardware was in their hands, panel open, while [target.GetSheHe] slept under a dose."
- Tier lines:
  - .desc_tier1 "\n\nThere was little to reach: a few first-tier units. They loosened what they could."
  - .desc_tier2 "\n\nThe enhancements were all within reach. They set the calibration a little wrong and left the seals looking whole."
  - .desc_tier3 "\n\nThe overclocked units are guarded, but not that night. The agents set them to run hotter than they should."
  - .desc_fractured "\n\nThe hardware was already failing. No one will be able to say how much of what follows was their doing."
- .desc_discovered "\n\nThey were not careful enough. Someone saw them leave."
- Options:
  - .a "Quietly done."
  - .b "Let them know whose hands."

**tamper.003 *Hands Withdrawn***
- .desc "The agents never got the panel open. They were interrupted, or lost their nerve, and came back with nothing done."
- .desc_tier3 "\n\nOverclocked hardware is watched. Someone was always awake beside it."
- .desc_discovered "\n\nWorse, they were seen. [target.GetName] will know who sent them."
- Options:
  - .a "Let it go."
  - .b "Again."

**tamper.004 *A Fault in the Hardware***
- .desc "The hardware misbehaves. The overlay stutters at its edges, and a limb responds a beat late."
- Tier lines:
  - .desc_aug "\n\nIt is small: a sensor that drifts, a grip that slips. Small enough to ignore, for now."
  - .desc_enh "\n\nThe enhancements are out of step with each other. Reflexes fire in the wrong order."
  - .desc_oc "\n\nThe overclocked units run hotter than they should, and the cooling cannot keep up."
  - .desc_nf "\n\nThe hardware was already unstable. It is worse now, and no one can say what was done to it."
- .desc_unknown "\n\nThe seals on one panel are new. Someone had their hands on it while you slept."
- .desc_known "\n\n[owner.GetName]'s people opened the panel while you slept, and made sure you would know it."
- Options:
  - .a "The clinic."
  - .b "My own physician."
  - .c "Someone cheaper."
  - .d "Live with it."
  - .e "Find the hands."
- .tt "The fault is opened up and reworked. How it goes is decided on the table."
- .e.success "A bribed technician and a door left unlocked. The trail ends at [owner.GetName]."
- .e.failure "Whoever it was left nothing to follow."

**Procedures amendments**
- proc.002.desc_salvaged "The hardware has been out for some weeks now. It was cut out for its value, not for your sake, and the incisions show it."
- proc.002.desc_repair_fault "The faulty hardware was opened and reworked some weeks ago."
- proc.020.desc_salvaged "\n\nIt was cut out of you for its value. The reflex reaches for it anyway."
