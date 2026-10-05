# Lore review: cybernetics_v2_realm.md (binding for script and loc)

**eotg-lore-keeper, 2026-10-04.** Approved, with eight must-fix items (R1–R8), all in wording. The mechanics hold:
- every law is set by the head of the realm, and nothing sits above it (LAW AT 866);
- no named implant players;
- Favor provides nothing;
- nothing acts at a distance.

## Must-fix
- **R1. A vassal reads "the law of your realm", not "your law".** The policy belongs to the top liege.
  - Every `desc_ban` / `desc_license` in act.001, act.003 and realm.001 gets two variants:
    - root `is_independent_ruler = yes` → "Your law …";
    - otherwise → "The law of your realm …" (or `[ROOT.Char.GetTopLiege.GetName]`'s law).
  - These are desc variants, not new beats, and add about 5 keys.
  - The §7 line becomes: "never anyone's law but the realm's own, as set by the ruler at its head."
- **R2. Never an unqualified "the law".** Allowed forms: "your law", "your realm's law", "the law of your realm".
  - realm.001.e becomes "The realm's law holds, for everyone."
  - The `defied_law` opinion becomes "Refused a Lawful Order".
- **R3.** `eotg_aug_policy_set_by_liege_tt` becomes "Set by the ruler at the head of your realm, for all of it."
- **R4. act.002 is retitled "Past Spec".** "Running Hot" is already the shipped modifier `eotg_mod_aug_running_hot`.
- **R5. act.006.d becomes "Keep the full vigil."**
  - "Pray" assumes a god, and "bear it" takes a doctrine stance; both are out.
  - "keepers of the site" becomes "those who tend the site" (to avoid Acathea's Sentinel Keepers).
  - "after the climb" becomes "after the long approach".
- **R6. Foul play is proven only by physical evidence** (I5): a strike too fast for an arm, heat coming off a casing, scorched heat sinks; a hands-on look.
  - Never scan logs, telemetry, a signal, a jammer, a relay, "hacked", or anyone controlling the hardware.
  - `.c.hot` and `.c.clean` never say who examined, because option e reaches them too.
- **R7. The act.004 hum is audible hardware:** a servo tick, coil whine. Never "at the edge of hearing" or faint "from somewhere".
- **R8. A lent technician does not move.** Only a variable is set. Say "will see to your implants for a year"; never travel or joining your court.
- **DoD grep additions:** `telemetry|jamm|relay|hack|authorit|warrant|magistrat|inspector|registry|encourag|sponsor|patronag`.

## Rulings
- **Q1. Arrest: approved, inside LAW AT 866.** The boundary loc must respect:
  1. The arrest is made by the subject's own liege, inside the realm, under that realm's own law, which the ruler at the head of the realm set.
  2. **No apparatus.** Never authorities, enforcers, inspectors, magistrates, tribunals (judicial), warrants, registries, permits or permit offices, certification, regulation(s), or a named licensing body. "Your court" as a household is fine. A licence is held "under your law".
  3. Discovery is hearsay only: "word has got out" or "word has reached you". No investigation, records, scans or implant register.
  4. Under Tolerate or Favor, and for the independent lawmaker themselves: no arrest, and no authority (the earlier ruling).
  5. The law never reaches outside the realm. No extradition, no foreign warrant.
  6. A Ban never "created or fed" the black market. The back streets are simply what is left under it.
  - **Amendment to `cybernetics_v2_procedures_lore.md`, Discovery:** "Keep 'word has got out'. With no law in force (Tolerate, Favor, or an independent patient), no arrest and no authority. Under the patient's realm's own Ban or License (`cybernetics_v2_realm.md` §4.2), the patient's liege may arrest under that law. See the realm lore boundary."
- **Q2. Favor: keep it, four laws.** Open regard is a personal stance, not provision.
  - Its mechanics are approved: more offers, +15 Offer acceptance, back-street discovery ×0.5.
  - Never "encourage", "promote", "sponsor", "support", "invest", "programme/program", "patron" or "patronage".
  - `_effects` never implies the ruler pays, supplies or arranges anything.
- **Register.**
  - **Tournaments** (canon: Angelia's divine tournaments).
    - Allowed: the field, the bout, the arena, the marshal, the stands, the trial grounds.
    - Banned: lists, joust, tilt, lance, horse, squire.
  - **Pilgrimage.**
    - Faith-neutral: no god-name, doctrine, pray, bless or sacrament.
    - Say "the holy site". Use Sanctum if a building is needed.
  - **Hunts:** "the quarry" and "the trail" only. No Earth animals, no hounds, no mounts.

## Names (picked)
- **Law group:** "Augmentation".
- **Laws:**
  - Ban: "Augmentation Prohibited"
  - License: "Augmentation Licensed"
  - Tolerate: "Augmentation Tolerated"
  - Favor: "Augmentation Favoured"
- **Court position:** "Implant Technician".
- **Interaction:** "Borrow Their Technician" (replaces "Lend Your Surgeon").
- **Events:**
  - act.001 "The Rules of the Field"
  - act.002 "Past Spec"
  - act.003 "Foul Play?"
  - act.004 "A Hum at the Table"
  - act.005 "Quarry in the Overlay"
  - act.006 "At the Holy Site"
  - realm.001 "Contraband Hardware"
- **Opinions:**
  - contraband "Unlawful Implants"
  - defied_law "Refused a Lawful Order"
  - outlawed "Outlawed My Implants"
  - barred "Barred Me from the Field"

## Renderings
The localizer may polish these. No numbers, and no "risk", "odds" or "chance". Appended lines start with `\n\n`. `/v` marks the vassal variant (R1).

**Laws**
- **ban** "Augmentation Prohibited"
  - _effects "Augmentation is prohibited in your realm.\nNo sanctioned clinic operates in your realm.\nImplant work on anyone living under your law is a crime, and its discovery gives their liege reason to imprison them.\nRefusing your order to remove implants is a crime.\nAugmented vassals and courtiers resent it."
  - _desc "No hands in your realm may fit an implant."
- **license** "Augmentation Licensed"
  - _effects "Only implant work by sanctioned hands is lawful in your realm.\nSanctioned clinics are vetted under your law.\nBack-street implant work is a crime.\nRefusing your order to remove unlawful implants is a crime."
  - _desc "Implants are lawful in your realm if the right hands fit them."
- **tolerate** "Augmentation Tolerated"
  - _effects "Your law says nothing on augmentation."
  - _desc "What anyone has fitted is their own affair."
- **favor** "Augmentation Favoured"
  - _effects "You hold the augmented in open regard at your court.\nOffers of implant work come more readily.\nFewer look closely at back-street work."
  - _desc "Your court makes no secret of whose company it prefers."
- cooldown_tt "The Augmentation law has not been changed recently" (synced 2026-10-04 to the shipped `eotg_aug_policy_cooldown_tt`; it is a `custom_description` that renders as a met/unmet condition, so the shipped form stands)
- set_by_liege_tt "Set by the ruler at the head of your realm, for all of it."
- clinic_closed_tt "No sanctioned clinic operates where augmentation is prohibited."

**AI and Demand amendments**
- REFUSAL_IS_CRIME "Refusing would break their realm's law"
- BANNED "Prohibited in their realm"
- FAVORED "Favoured in the realm" (shipped wording; Canadian spelling, 4168bb8)
- demand_removal_crime_desc "\n\nUnder the law of your realm, refusing this order is a crime."
- demand_crime_toast "[recipient.GetName] Refuses a Lawful Order". Body: "Refusing was a crime under your realm's law. You have reason to imprison [recipient.GetHerHim]."

**Implant Technician**
- name "Implant Technician"
- _desc "A specialist in fitting and servicing implants, kept at court."
- employer_desc "Operates on you and those in your care, more safely and more cheaply than a physician. Services your implants by hand, and keeps overclocked hardware running cooler."
- aptitude_augmented "Wears hardware of their own, and knows how it fails."
- aptitude_former "Has had implants taken out, and knows how they come out."
- banned_tt "Augmentation is prohibited in your realm."
- opt_technician "My implant technician."

**Borrow Their Technician**
- _desc "Ask for the services of their Implant Technician for a year, for a fee."
- _notification "[actor.GetName] asks for your Implant Technician's services for a year, for a fee."
- accepted toast "[recipient.GetName] Lends Their Technician". Body: "[eotg_lent_technician.GetName] will see to your implants for a year."
- declined toast "[recipient.GetName] Keeps Their Technician"
- AI descs:
  - ALLIED "Allied"
  - FAMILY "Family"
  - GENEROUS "Generous"
  - NEEDS_TECHNICIAN "Needs their technician themselves"

**act.001 "The Rules of the Field"**
- .desc "The marshals have come to you before the first bout. Some of the entrants carry hardware: limbs on actuators, optics behind the eyes. The rules of the field were written for flesh, and never imagined it."
- .desc_many "\n\nIt is not one entrant. [eotg_aug_entrant.GetName] is only the most obvious."
- .desc_entrant_oc "\n\n[eotg_aug_entrant.GetName] is overclocked. The casings are scorched along the heat sinks, and the stands can see it."
- .desc_entrant_nf "\n\n[eotg_aug_entrant.GetName]'s hardware is unstable. A hand twitches on the rail, and those beside [eotg_aug_entrant.GetHerHim] keep a step back."
- .desc_ban "\n\nYour law prohibits augmentation. On your field, that is reason enough."
  - /v "\n\nThe law of your realm prohibits augmentation. On a field in that realm, that is reason enough."
- Options a–e as briefed in the spec.
- barred_toast "Barred from the Field". Body: "The host has barred augmented entrants. You will not compete."

**act.002 "Past Spec"**
- .desc "The bout is close. The hardware could give more than the rules of the field expect."
- .desc_physical "\n\nPush the actuators past their rating, and the body will move before anyone else on the field can."
- .desc_board "\n\nThe overlay has already played the next three moves. Only your hand is waiting."
- .desc_hot "\n\nThe hardware is already warm. It has been running close to its limit for some time."
- .desc_ban "\n\nAugmentation is prohibited in the host's realm. Anything you do with it here will be noticed."
- .a.seen "Someone in the stands saw the heat shimmer off your casing. Word has reached the host."

**act.003 "Foul Play?"**
- .desc "[eotg_aug_accuser.GetName] has come to you between bouts. [eotg_aug_accuser.GetSheHe|U] says [eotg_aug_accused.GetName] wins with hardware, not skill: a strike too fast for any arm, and a casing hot to the touch after every bout."
- .desc_hot "\n\nEven from your seat, the heat coming off [eotg_aug_accused.GetName]'s casing is plain to see."
- .desc_ban "\n\nYour law prohibits augmentation. Whatever the field's rules say, your realm's say more." (with a /v variant)
- .desc_license "\n\nYour law allows implants fitted by sanctioned hands, and no others. Nobody has yet asked whose hands fitted these." (with a /v variant)
- .b "I see no foul play."
- .c.hot "Up close, the casing is scorched and the heat sinks are still warm from the bout. The hardware was run past spec. [eotg_aug_accused.GetName] is withdrawn from the field."
- .c.clean "Up close, the hardware is cool and within its rating. The accusation does not stand."

**act.004 "A Hum at the Table"**
- .desc "The servo in your wrist ticks as you lift the cup. Nobody hears it over the talk, until somebody does. Now the guests nearest you are watching your hand, not your face."
- .desc_host "\n\nIt is your feast. Every eye in the hall finds its way back to the head of the table."
- .desc_oc "\n\nThe overclocked units run warm, and their coil whine carries further than a servo's tick."
- .desc_nf "\n\nThe hand does not quite stop when you set the cup down. The guests nearest you have stopped talking."

**act.005 "Quarry in the Overlay"**
- .desc "The optics pick out a trail no one else in the party can see: a bent stem, a warm track, a heat trace fading in the cover."
- .desc_senses "\n\nYour senses read the trail truer still. The quarry's path hangs in the overlay, a step ahead of it."
- .desc_hum "\n\nThe quarry hears the coil whine before it sees you."

**act.006 "At the Holy Site"**
- .desc "Those who tend the site look at your hardware before they look at you. Nobody bars the way. Nobody steps aside, either."
- .desc_hot "\n\nAfter the long approach, the hardware is warm to the touch, and the heat sinks tick as they cool."
- .d "Keep the full vigil."

**realm.001 "Contraband Hardware"**
- .desc "Word has reached you: [eotg_contraband_subject.GetName] has had implant work done that your realm's law does not allow."
- .desc_ban "\n\nYour law prohibits augmentation, and [eotg_contraband_subject.GetSheHe] lives under it."
  - /v "\n\nThe law of your realm prohibits augmentation, and [eotg_contraband_subject.GetSheHe] lives under it."
- .desc_license "\n\nYour law allows implant work by sanctioned hands only. These hands were not." (with a /v variant)
- Tier lines:
  - .desc_aug "\n\nFirst-tier work: a handful of units on standard fittings."
  - .desc_enh "\n\nA full set of enhancements, recently fitted."
  - .desc_oc "\n\nOverclocked hardware. Whoever fitted it knew exactly what they were doing."
  - .desc_nf "\n\nThe hardware was already unstable. Whoever touched it last has made it no better."
- .desc_courtier "\n\n[eotg_contraband_subject.GetSheHe|U] lives under your roof."
- Options:
  - .a "Arrest them." (if guards appear: "your guards", not "wardens")
  - .b "Have it taken out."
  - .c "A fine will do."
  - .d "Look the other way."
  - .e "The realm's law holds, for everyone."
  - .f "A fine. A large one."

## Open (canon silent; optional vault questions)
- **866 hunt fauna.** Keep "the quarry" generic until region briefs name species.
- **Who tends holy sites.** Keep "those who tend the site" until faith loc exists after Gate 1.
