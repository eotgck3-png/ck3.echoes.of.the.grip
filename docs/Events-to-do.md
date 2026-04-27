# Fringe Government Event Design Document

## Phase 1 — Functional + Core Flavor Events

### Target: ~50 Events

### Purpose: Establish instability loop, captain politics, succession collapse, and raiding identity

---

# EVENT CATEGORY — GRIP SYSTEM

These events reinforce the central instability mechanic.

---

## Event: The Grip Weakens

### Trigger

* Low Grip threshold reached
* realm size above medium threshold

### Description

Rumors spread that the ruler is losing control. Captains begin ignoring orders and withholding tribute.

### Outcomes

#### Tighten Discipline

* gain small Grip
* gain dread
* vassal opinion penalty
* compassionate characters lose stress

#### Let Them Squabble

* lose Grip
* reduced immediate faction pressure
* chance for captain rivalry events

#### Buy Their Loyalty

* lose gold
* gain captain opinion
* small Grip gain

### Relevant Traits

* wrathful
* arbitrary
* greedy
* compassionate

### Modifiers

* `eotg_fringe_cracking_authority`
* `eotg_fringe_bought_loyalty`

---

## Event: The Captains Smell Weakness

### Trigger

* ruler loses major war
* low prestige

### Description

Several captains openly question leadership.

### Outcomes

#### Public Execution

* gain dread
* gain Grip
* rebellion chance

#### Challenge Them Personally

* duel event chain
* martial characters gain advantage

#### Ignore the Insults

* lose prestige
* faction strength increases

---

# EVENT CATEGORY — RAID PRESSURE

---

## Event: The Fringe Hungers

### Trigger

* no raid or war for 3 years

### Description

The captains grow restless. Loot stores run dry.

### Outcomes

#### Promise Future Glory

* temporary delay modifier
* future penalty if no war begins

#### Launch Immediate Raid

* gain raid target modifier
* forced war preparation cost

#### Tighten Rations

* county unrest
* development penalty

### Modifiers

* `eotg_fringe_restless_captains`
* `eotg_fringe_promised_glory`

---

## Event: Raiders Desert the Cause

### Trigger

* prolonged peace
* low gold

### Description

Warbands abandon the ruler in search of richer opportunities.

### Outcomes

#### Pay Them to Stay

* lose gold
* retain levies

#### Let Them Leave

* levy reduction
* lower upkeep temporarily

#### Threaten Execution

* gain dread
* mutiny risk

---

# EVENT CATEGORY — CAPTAIN POLITICS

---

## Event: The Captains Demand Their Share

### Trigger

* successful raid
* successful conquest war

### Description

Captains demand division of spoils.

### Outcomes

#### Divide the Loot Equally

* gain captain opinion
* lose gold
* gain Grip

#### Favor Loyal Captains

* chosen captain gains opinion
* rival captains lose opinion

#### Keep the Best for Yourself

* gain gold
* lose Grip
* faction progress increases

---

## Event: A Captain Refuses Orders

### Trigger

* low opinion captain
* low Grip

### Description

A captain openly disobeys military orders.

### Outcomes

#### Make an Example of Them

* imprisonment attempt
* rebellion chance

#### Negotiate

* hook exchange
* lose prestige

#### Ignore the Defiance

* lose Grip
* captain gains influence modifier

---

## Event: Blood Feud Among Captains

### Trigger

* two rival captains
* large realm

### Description

Two captains begin violent conflict over territory and loot.

### Outcomes

#### Force Peace

* diplomacy challenge
* both captains dislike ruler

#### Support One Side

* chosen captain loyalty increase
* rival gains rebellion chance

#### Let Them Fight

* county damage chance
* weaker captain may die

---

# EVENT CATEGORY — SUCCESSION CHAOS

---

## Event: Who Commands the Fleet?

### Trigger

* ruler death

### Description

Captains gather to decide who controls the realm.

### Outcomes

#### Rally Behind the Heir

* legitimacy challenge
* requires high diplomacy/prestige

#### Buy Captain Support

* lose gold
* reduce succession factions

#### Rule Through Fear

* gain dread
* assassination risk increases

### Modifiers

* `eotg_fringe_succession_crisis`

---

## Event: The Outer Clans Break Away

### Trigger

* succession
* large realm size

### Description

Peripheral captains refuse to recognize new leadership.

### Outcomes

#### Accept Their Departure

* vassals become independent peacefully

#### Crush the Rebels

* rebellion war

#### Offer Greater Autonomy

* reduced taxes
* reduced faction hostility

---

## Event: The Heir Is Challenged

### Trigger

* ambitious captain exists
* succession period

### Description

A captain claims the heir is weak.

### Outcomes

#### Duel the Challenger

* prowess duel

#### Assassinate Them Quietly

* intrigue challenge

#### Buy Their Loyalty

* expensive gold payment

---

# EVENT CATEGORY — OVEREXTENSION

---

## Event: The Realm Fractures

### Trigger

* very large realm
* low Grip

### Description

Communication collapses across distant territories.

### Outcomes

#### Abandon Remote Holdings

* release distant vassals

#### Centralize Power

* massive opinion penalties
* temporary Grip increase

#### Delegate Authority

* strong vassal empowerment

---

## Event: Supply Lines Collapse

### Trigger

* large war
* distant territories

### Description

Logistics fail across the frontier.

### Outcomes

#### Divert Resources

* lose gold
* army supply bonus

#### Let Local Captains Handle It

* captain power increase

#### Push Forward Anyway

* army attrition increase

---

# EVENT CATEGORY — MUTINY & REBELLION

---

## Event: Mutiny in the Void

### Trigger

* extremely low Grip

### Description

A fleet commander attempts to seize ships and defect.

### Outcomes

#### Crush the Mutiny

* military challenge
* gain dread

#### Negotiate Amnesty

* lose prestige
* avoid revolt

#### Let Them Leave

* splinter realm created

---

## Event: The Warbands Riot

### Trigger

* unpaid armies
* low gold

### Description

Warriors riot over unpaid spoils.

### Outcomes

#### Pay Them

* lose gold

#### Use Force

* casualties
* gain dread

#### Blame the Captains

* captain opinion penalties

---

# EVENT CATEGORY — RAID EVENTS

---

## Event: The Great Plunder

### Trigger

* highly successful raid

### Description

The raid yields extraordinary wealth.

### Outcomes

#### Celebrate Publicly

* prestige gain
* vassal opinion increase

#### Secretly Hoard the Wealth

* gain large gold
* lose Grip

#### Reward the Captains

* strong captain loyalty boost

### Modifier

* `eotg_fringe_great_plunder`

---

## Event: Raid Gone Wrong

### Trigger

* failed raid

### Description

The raid collapses into disaster.

### Outcomes

#### Blame the Scouts

* random captain loses opinion

#### Accept Responsibility

* gain small legitimacy
* lose prestige

#### Demand Another Raid Immediately

* army exhaustion

---

## Event: Refugees Join the Fringe

### Trigger

* neighboring war
* successful raid nearby

### Description

Refugees offer themselves to the ruler.

### Outcomes

#### Accept Them

* levy increase
* development strain

#### Enslave Them

* gold gain
* tyranny gain

#### Turn Them Away

* no gain

---

# EVENT CATEGORY — REFORMATION

---

## Event: The Raiders Grow Fat

### Trigger

* long successful reign
* high wealth

### Description

Some captains prefer profit over endless war.

### Outcomes

#### Begin Cartel Reforms

* unlock reform chain

#### Maintain the Old Ways

* gain captain approval

#### Secretly Prepare Reforms

* intrigue-based hidden progress

---

## Event: Discipline Over Chaos

### Trigger

* high martial ruler
* strong army

### Description

Veteran commanders demand professionalism.

### Outcomes

#### Begin PMC Reforms

* unlock PMC transition

#### Reject Professionalization

* traditionalist approval

---

## Event: The Old Ways Die Hard

### Trigger

* reform attempt

### Description

Traditional captains resist centralization.

### Outcomes

#### Suppress the Traditionalists

* rebellion chance

#### Compromise

* weaker reform bonuses

#### Abandon Reform

* stability restored temporarily

---

# EVENT CATEGORY — RARE FLAVOR EVENTS

---

## Event: A Warlord of Legend Emerges

### Trigger

* extremely successful captain

### Description

A captain becomes wildly popular among warbands.

### Outcomes

#### Promote Them

* strong knight bonus
* future rival risk

#### Suppress Their Fame

* opinion penalty

#### Bind Them Through Marriage

* alliance modifier

---

## Event: Songs of the Fringe

### Trigger

* multiple successful wars

### Description

Stories spread across the frontier of the ruler’s victories.

### Outcomes

#### Embrace the Legend

* prestige gain

#### Encourage Fear Instead

* dread gain

---

## Event: The Ghost Fleet

### Trigger

* failed mutiny
* lost fleet

### Description

Rumors spread that lost raiders still haunt the frontier.

### Outcomes

#### Exploit the Fear

* dread gain

#### Investigate the Rumors

* possible treasure event chain

#### Ignore the Stories

* no effect
# Fringe Government Event Design Document

## Phase 2 — Reinforcement + Escalation Events

### Purpose: Deepen instability loops, create emergent storytelling, reinforce long-term collapse cycles

---

# EVENT CATEGORY — CAPTAIN POWER BLOCS

These events create internal political ecosystems between captains.

---

## Event: A Captain Builds Their Own Following

### Trigger

* powerful captain
* high prestige captain
* long reign under same ruler

### Description

A captain gathers loyal warriors and subordinate officers around themselves rather than the ruler.

### Outcomes

#### Demand Loyalty Oaths

* intrigue challenge
* captain opinion penalty
* possible rebellion

#### Allow the Growth

* captain gains power modifier
* reduced immediate unrest

#### Grant Them Territory

* strong loyalty gain
* future independence risk

### Modifiers

* `eotg_fringe_personal_following`
* `eotg_fringe_captain_entrenched`

---

## Event: Secret Talks Between Captains

### Trigger

* low Grip
* multiple dissatisfied captains

### Description

Rumors spread that captains are secretly meeting without the ruler’s approval.

### Outcomes

#### Send Spies

* intrigue challenge
* possible hooks discovered

#### Publicly Accuse Them

* gain dread
* opinion penalties

#### Ignore the Rumors

* faction strength increase

---

## Event: The Captains Form a Coalition

### Trigger

* multiple strong factions
* low ruler prestige

### Description

Several captains temporarily unite against central authority.

### Outcomes

#### Divide Them with Bribes

* lose large gold
* coalition weakened

#### Arrest Their Leaders

* high rebellion chance

#### Promise Future Spoils

* temporary loyalty increase
* future expectation modifier

---

# EVENT CATEGORY — BREAKAWAY REALMS

---

## Event: A Captain Declares Independence

### Trigger

* low Grip
* distant vassal
* weak ruler

### Description

A captain declares their territory sovereign from the realm.

### Outcomes

#### Accept the Split

* peaceful independence

#### Crush the Traitor

* war declared

#### Offer Recognition in Exchange for Tribute

* tributary relationship

---

## Event: The Frontier Slips Away

### Trigger

* overextension
* low control in distant territories

### Description

Remote territories no longer obey central authority.

### Outcomes

#### Abandon the Frontier

* lose counties

#### Send Enforcers

* gold cost
* revolt chance

#### Grant Local Autonomy

* reduced taxes
* reduced unrest

---

## Event: Rival Fringe Realm Emerges

### Trigger

* splinter rebellion succeeds

### Description

A rival ruler claims to represent the true future of the Fringe.

### Outcomes

#### Prepare for War

* martial bonus modifier

#### Seek Alliance

* diplomacy challenge

#### Assassinate Their Leader

* intrigue event chain

---

# EVENT CATEGORY — FEAR & DREAD

---

## Event: Public Execution Broadcast

### Trigger

* imprisoned rival
* high dread ruler

### Description

The ruler stages a brutal execution to terrify captains and subjects alike.

### Outcomes

#### Make It Spectacular

* large dread gain
* diplomacy penalties

#### Quiet Execution

* small dread gain
* less opinion penalty

#### Spare Them Publicly

* compassionate approval
* lose dread

### Modifiers

* `eotg_fringe_public_terror`

---

## Event: Fear Turns to Hatred

### Trigger

* extremely high dread

### Description

The realm obeys, but whispers of assassination spread everywhere.

### Outcomes

#### Increase Personal Guard

* gold upkeep increase

#### Ignore the Threats

* assassination chance increases

#### Purge Suspected Conspirators

* tyranny gain
* random deaths

---

# EVENT CATEGORY — RAID ESCALATION

---

## Event: A Rich Trade Route Is Exposed

### Trigger

* neighboring wealthy realm
* high intrigue scout

### Description

Scouts discover an exposed trade route ripe for plunder.

### Outcomes

#### Launch Immediate Raid

* raid bonus modifier

#### Sell the Information

* gold gain

#### Share with Captains

* captain loyalty increase

---

## Event: Raiders Bring Back Strange Relics

### Trigger

* successful distant raid

### Description

Raiders return with mysterious artifacts from the frontier.

### Outcomes

#### Sell Them

* gold gain

#### Keep Them

* artifact chance

#### Let the Captains Divide Them

* opinion gain

---

## Event: Civilian Massacre During Raid

### Trigger

* wrathful or sadistic ruler
* aggressive raid outcome

### Description

The raid becomes a massacre.

### Outcomes

#### Encourage Terror

* dread gain
* diplomacy penalty

#### Punish the Raiders

* captain opinion penalty

#### Deny Responsibility

* intrigue coverup chance

---

# EVENT CATEGORY — SUCCESSION DISASTERS

---

## Event: The Dead Ruler's Favorite Captain

### Trigger

* ruler death
* strong captain relationship with previous ruler

### Description

A favored captain claims the ruler intended them to guide succession.

### Outcomes

#### Accept Their Support

* gain captain backing
* heir legitimacy weakened

#### Reject Them

* rebellion risk

#### Offer Shared Rule

* temporary stability modifier
* future power struggle risk

---

## Event: The Fleets Choose Sides

### Trigger

* succession crisis
* multiple heirs

### Description

Different fleets swear loyalty to different claimants.

### Outcomes

#### Rally the Largest Fleet

* military advantage

#### Seek Peaceful Settlement

* realm split outcome

#### Assassinate Rival Heir

* intrigue chain

---

## Event: The Succession War Begins

### Trigger

* failed succession stabilization

### Description

The captains abandon negotiation. War erupts.

### Outcomes

#### Fight for Unity

* war bonuses

#### Negotiate Partition

* realm divided peacefully

#### Flee with Loyalists

* adventurer-style exile setup

---

# EVENT CATEGORY — REFORMATION PRESSURE

---

## Event: Merchants Gain Influence

### Trigger

* high gold economy
* reduced raiding frequency

### Description

Traders and financiers gain influence over captains.

### Outcomes

#### Embrace Commerce

* Cartel reform progress

#### Suppress Merchant Influence

* captain approval

#### Exploit Both Sides

* temporary bonuses
* corruption modifier

---

## Event: Veterans Demand Structure

### Trigger

* large standing army
* disciplined ruler

### Description

Experienced commanders push for permanent organization.

### Outcomes

#### Establish Military Doctrine

* PMC reform progress

#### Reject Professionalism

* traditionalist loyalty

---

## Event: Young Captains Reject Tradition

### Trigger

* reform underway

### Description

A younger generation believes the old raider culture is dying.

### Outcomes

#### Support the Young Captains

* reform acceleration

#### Side with Traditionalists

* reform slowed
* stability gain

---

# EVENT CATEGORY — CULTURAL FRINGE EVENTS

---

## Event: Frontier Festival

### Trigger

* recent victory
* high prestige

### Description

Warbands gather in celebration.

### Outcomes

#### Hold Grand Celebrations

* prestige gain
* captain loyalty increase

#### Recruit New Raiders

* levy growth

#### Use Festival for Political Deals

* hook generation chance

---

## Event: Tales of the Old Frontier

### Trigger

* old ruler
* peaceful moment

### Description

Veteran raiders tell stories of past conquests and betrayals.

### Outcomes

#### Inspire the Young

* martial lifestyle experience

#### Reminisce on Lost Glory

* melancholy modifier

#### Call for New Conquests

* raid preparation modifier

---

## Event: A Child Raised by Raiders

### Trigger

* young heir
* martial education

### Description

The heir grows among violent warbands.

### Outcomes

#### Encourage Ruthlessness

* possible sadistic/wrathful traits

#### Teach Leadership

* diplomacy/martial bonuses

#### Shield Them from Violence

* compassionate traits possible

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: The Great Unifier

### Trigger

* extremely successful ruler
* high prestige
* large realm

### Description

Some begin calling the ruler the one destined to unite the Fringe forever.

### Outcomes

#### Embrace the Myth

* huge prestige gain
* stronger factions after death

#### Reject the Worship

* modest legitimacy gain

#### Use the Myth for Conquest

* conquest CB bonuses

### Modifier

* `eotg_fringe_great_unifier`

---

## Event: Prophecy of Collapse

### Trigger

* enormous realm
* low Grip

### Description

Rumors spread that the realm is doomed to fracture.

### Outcomes

#### Silence the Prophets

* dread gain

#### Ignore the Warnings

* stress loss for cynical rulers

#### Prepare for Collapse

* succession stabilization modifier

---

## Event: The Last Great Raid

### Trigger

* old ruler
* nearing death
* high prestige

### Description

The ruler considers leading one final legendary raid.

### Outcomes

#### Lead the Raid Personally

* high risk/high reward chain

#### Send the Heir Instead

* heir gains prestige or injury

#### Retire from War

* captain disappointment modifier
# Fringe Government Event Design Document

## Phase 3 — Deep Flavor, Emergent Narratives, and Rare Story Events

### Purpose: Make Fringe realms feel alive, mythic, unstable, and culturally distinct

These events are not strictly necessary for mechanics, but they are what make players remember a campaign.

---

# EVENT CATEGORY — LEGENDARY CAPTAINS

---

## Event: The Butcher of the Frontier

### Trigger

* captain with high dread
* many raid victories
* sadistic or wrathful traits

### Description

Stories spread of a captain who leaves burning worlds and mass graves behind them.

### Outcomes

#### Reward Their Brutality

* captain loyalty increase
* dread gain
* diplomacy penalties

#### Publicly Condemn Them

* lose dread
* captain rivalry created

#### Secretly Use Their Reputation

* intrigue bonus
* hidden terror modifier

### Modifiers

* `eotg_fringe_butcher_reputation`

---

## Event: The Captain Loved by the Warbands

### Trigger

* high popularity captain
* charismatic traits

### Description

Warriors cheer louder for the captain than for the ruler.

### Outcomes

#### Elevate Them

* strong military bonus
* future succession threat

#### Undermine Their Reputation

* intrigue scheme opportunity

#### Bind Them by Marriage

* alliance modifier

---

## Event: The Disappearing Captain

### Trigger

* captain disappears mysteriously

### Description

A powerful captain vanishes without explanation.

### Outcomes

#### Investigate

* possible intrigue chain

#### Blame Rivals

* rivalry escalation

#### Seize Their Assets

* gold gain
* captain unrest

---

# EVENT CATEGORY — FRONTIER MYTHS

---

## Event: The Ghost Signal

### Trigger

* deep frontier territory
* low development systems

### Description

A repeating signal echoes from abandoned space.

### Outcomes

#### Investigate the Source

* possible treasure chain
* danger chance

#### Claim It Is Haunted

* dread gain

#### Sell the Coordinates

* gold gain

---

## Event: The Graveyard Fleet

### Trigger

* failed war
* destroyed fleets

### Description

Drifting wrecks from old battles fill a forgotten sector.

### Outcomes

#### Salvage the Ruins

* gold gain

#### Honor the Dead

* prestige gain

#### Recruit Survivors

* levy reinforcement

---

## Event: Songs of the Fallen Warlord

### Trigger

* famous ruler death

### Description

Raiders sing of the ruler’s victories and betrayals.

### Outcomes

#### Encourage the Legend

* dynasty prestige gain

#### Rewrite the Story

* legitimacy gain

#### Ban the Songs

* captain opinion penalty

---

# EVENT CATEGORY — WARBAND CULTURE

---

## Event: Trial by Combat

### Trigger

* dispute between captains

### Description

Warriors demand the conflict be resolved through combat.

### Outcomes

#### Allow the Duel

* possible death/injury

#### Forbid It

* lose prestige

#### Rig the Outcome

* intrigue risk

---

## Event: Feast of Plunder

### Trigger

* successful raid

### Description

Captured goods are displayed during a massive celebration.

### Outcomes

#### Share Everything

* captain loyalty boost

#### Reserve the Best Goods

* gold gain
* greed resentment modifier

#### Use It to Recruit

* levy gain

---

## Event: Raiders Fight Over Slaves

### Trigger

* post-raid event

### Description

Warbands argue violently over captives.

### Outcomes

#### Divide Them Fairly

* stability increase

#### Favor Elite Captains

* loyalty shift

#### Sell Them Immediately

* gold gain

---

# EVENT CATEGORY — PARANOIA & BETRAYAL

---

## Event: Poison in the Cup

### Trigger

* high intrigue realm
* many rivals

### Description

Someone attempts to poison the ruler during a feast.

### Outcomes

#### Execute the Suspects

* dread gain

#### Secret Investigation

* intrigue chain

#### Public Forgiveness

* diplomacy gain
* weakness perception

---

## Event: The Heir Plots Too Soon

### Trigger

* ambitious heir
* aging ruler

### Description

Rumors suggest the heir grows impatient.

### Outcomes

#### Confront the Heir

* relationship shift

#### Ignore the Rumors

* assassination risk

#### Remove Them from Succession

* succession crisis risk

---

## Event: A Captain Sells Secrets

### Trigger

* neighboring rival realm

### Description

A captain secretly provides information to enemies.

### Outcomes

#### Public Execution

* dread gain

#### Blackmail Them Instead

* strong hook gained

#### Cover It Up

* intrigue bonus

---

# EVENT CATEGORY — FRINGE CHILDREN & SUCCESSORS

---

## Event: Raised Among Raiders

### Trigger

* child education

### Description

A child spends their youth among violent warbands.

### Outcomes

#### Teach Ruthlessness

Possible traits:

* wrathful
* sadistic
* ambitious

#### Teach Leadership

Possible traits:

* strategist
* brave
* gregarious

#### Teach Survival

Possible traits:

* paranoid
* cautious
* patient

---

## Event: Child of the Frontier

### Trigger

* heir born during war

### Description

The child is born while the realm burns around them.

### Outcomes

#### Declare Them Blessed by War

* prestige gain

#### Hide Them Away

* safety modifier

#### Raise Them Publicly

* captain approval

---

## Event: Heir of Many Captains

### Trigger

* child educated by multiple captains

### Description

Different captains shape the heir’s worldview.

### Outcomes

#### Encourage Unity

* diplomacy education bonus

#### Encourage Competition

* intrigue/martial bonus

#### Let the Captains Fight for Influence

* future rivalries

---

# EVENT CATEGORY — COLLAPSE & APOCALYPSE EVENTS

---

## Event: The Great Fragmentation

### Trigger

* massive realm
* catastrophic low Grip
* succession crisis

### Description

The realm tears itself apart as captains declare sovereignty simultaneously.

### Outcomes

#### Fight for Every System

* massive civil war

#### Accept Controlled Fragmentation

* multiple peaceful releases

#### Retreat to the Core Territories

* realm contraction modifier

### Modifier

* `eotg_fringe_fragmentation`

---

## Event: The Captains Crown a Pretender

### Trigger

* weak ruler
* low legitimacy

### Description

A coalition of captains backs a rival claimant.

### Outcomes

#### Duel the Pretender

* combat event

#### Negotiate Power Sharing

* autonomy increase

#### Declare Total War

* faction war begins

---

## Event: The Realm Consumes Itself

### Trigger

* multiple simultaneous rebellions

### Description

Warbands burn worlds while captains slaughter each other openly.

### Outcomes

#### Restore Order Through Terror

* massive dread gain
* development destruction

#### Seek Negotiated Peace

* prestige loss
* rebellion reduction

#### Flee the Capital

* exile-style chain

---

# EVENT CATEGORY — REFORMATION MASTER EVENTS

These are transition-defining narrative events.

---

## Event: The Future of the Fringe

### Trigger

* reform decision started

### Description

The ruler gathers captains to decide the future of the realm.

### Outcomes

#### We Become a Cartel

* unlock cartel transition

#### We Become a Military State

* unlock PMC transition

#### We Remain Free

* reform canceled
* traditionalist loyalty

---

## Event: Traditionalist Revolt

### Trigger

* reform progress high

### Description

Old captains reject civilization and centralized rule.

### Outcomes

#### Crush the Old Guard

* reform progress increases
* rebellion war

#### Compromise with Them

* weaker reform outcome

#### Abandon Reform

* gain stability temporarily

---

## Event: The End of the Raider Age

### Trigger

* successful reform completion

### Description

The old raider banners are lowered as the realm transforms into something new.

### Outcomes

#### Honor the Old Ways

* veteran captain opinion gain

#### Erase the Past

* modernization bonuses

#### Preserve Raider Traditions

* hybrid modifiers

### Modifiers

* `eotg_fringe_old_blood`
* `eotg_fringe_modernized_state`

---

# EVENT CATEGORY — ULTRA RARE LEGEND EVENTS

---

## Event: The Warlord Who Would Not Die

### Trigger

* ruler survives many assassination attempts
* old ruler
* high prestige

### Description

Stories claim the ruler cannot be killed.

### Outcomes

#### Encourage the Myth

* dread gain

#### Laugh at the Stories

* diplomacy gain

#### Secretly Manipulate the Legend

* intrigue bonus

---

## Event: The Last Captain Loyal to the Old Realm

### Trigger

* realm collapse aftermath

### Description

One ancient captain still swears loyalty to the fallen ruler.

### Outcomes

#### Reward Their Loyalty

* strong knight bonus

#### Distrust Their Intentions

* intrigue chain

#### Retire Them Honorably

* prestige gain

---

## Event: The Frontier Remembers

### Trigger

* former Fringe ruler dies after reforming government

### Description

Old raiders gather one final time to remember the chaotic age of conquest.

### Outcomes

#### Celebrate the Legacy

* dynasty prestige

#### Condemn the Violence

* legitimacy gain

#### Call for a Return to the Old Ways

* possible restoration faction modifier
# Fringe Government Event Design Document

## Phase 4 — System Events, Dynamic Reactions, and AI Reinforcement

### Purpose: Ensure the government behaves dynamically across AI realms and sustains long campaigns

These events reinforce cyclical instability and keep AI Fringe realms from becoming static blobs.

---

# EVENT CATEGORY — AI STABILITY PRESSURE

These events primarily exist to help AI realms self-destruct naturally.

---

## Event: The Captains Grow Impatient

### Trigger

* AI ruler
* peace longer than 4 years
* medium or low Grip

### Description

Captains pressure the ruler to seek conquest.

### Outcomes

#### Launch Border Raid

* AI prioritizes nearby weak target

#### Promise Future Expansion

* temporary stability

#### Refuse the Demands

* faction pressure increase

### AI Weighting

Aggressive rulers heavily favor raids.

---

## Event: The Frontier Overstretches

### Trigger

* AI realm size above threshold

### Description

The ruler struggles to maintain control over distant territories.

### Outcomes

#### Delegate Authority

* stronger vassals

#### Tighten Control

* opinion penalties

#### Abandon Remote Holdings

* release weak territories

---

## Event: The Captains Challenge Weak Leadership

### Trigger

* AI ruler low martial
* low prestige

### Description

Captains begin openly questioning leadership competence.

### Outcomes

#### Promote Strong Captains

* vassal empowerment

#### Rule Through Fear

* dread increase

#### Ignore Them

* rebellion risk

---

# EVENT CATEGORY — FACTION ESCALATION

These events escalate faction pressure before wars occur.

---

## Event: Secret Meetings in the Outer Systems

### Trigger

* independence faction nearing threshold

### Description

Faction members gather secretly to discuss rebellion.

### Outcomes

#### Send Agents

* chance to weaken faction

#### Threaten the Leaders

* dread increase
* possible escalation

#### Pretend Ignorance

* intrigue bonus for rebels

---

## Event: The Captains Demand Concessions

### Trigger

* liberty faction active

### Description

Captains demand autonomy and reduced obligations.

### Outcomes

#### Grant Concessions

* reduced taxes
* faction weakened

#### Refuse Completely

* faction strength increases

#### Negotiate

* temporary compromise modifier

---

## Event: A Captain Defects to the Enemy

### Trigger

* external war
* disloyal captain

### Description

A captain secretly joins the enemy during wartime.

### Outcomes

#### Execute Their Family

* dread gain

#### Attempt Reconciliation

* diplomacy challenge

#### Publicly Denounce Them

* prestige effect

---

# EVENT CATEGORY — FRINGE DIPLOMACY

Fringe realms should feel feared and unstable diplomatically.

---

## Event: A Neighbor Seeks Protection

### Trigger

* weak neighboring ruler
* powerful Fringe realm nearby

### Description

A frightened ruler offers tribute for protection.

### Outcomes

#### Accept Tribute

* gold income
* tributary modifier

#### Demand Full Submission

* conquest opportunity

#### Mock Their Fear

* dread gain

---

## Event: Frontier Mercenaries Offer Service

### Trigger

* ongoing wars
* wealthy ruler

### Description

Independent warbands offer temporary service.

### Outcomes

#### Hire Them

* temporary troops

#### Turn Them Away

* no effect

#### Absorb Them Into the Realm

* captain creation chance

---

## Event: Diplomats Fear the Frontier Court

### Trigger

* high dread ruler

### Description

Foreign envoys are terrified by the ruler’s court.

### Outcomes

#### Exploit Their Fear

* diplomacy advantage

#### Offer Hospitality

* legitimacy gain

#### Intimidate Them Further

* dread increase

---

# EVENT CATEGORY — INTERNAL ECONOMIC CHAOS

---

## Event: Loot Floods the Markets

### Trigger

* multiple successful raids

### Description

Massive quantities of stolen goods destabilize local economies.

### Outcomes

#### Sell Everything Quickly

* gold gain
* inflation modifier

#### Regulate Distribution

* stability bonus

#### Let Captains Handle It

* captain wealth increase

### Modifier

* `eotg_fringe_loot_flood`

---

## Event: Smugglers Gain Influence

### Trigger

* wealthy captains
* large realm

### Description

Smuggling networks grow powerful within the realm.

### Outcomes

#### Work With Them

* gold increase

#### Suppress Smuggling

* captain anger

#### Tax Their Operations

* mixed effects

---

## Event: The Captains Hoard Wealth

### Trigger

* unequal loot distribution

### Description

Some captains become vastly wealthier than others.

### Outcomes

#### Redistribute Wealth

* loyalty increase
* wealthy captain anger

#### Ignore the Imbalance

* rivalry growth

#### Seize Their Assets

* tyranny gain

---

# EVENT CATEGORY — CULTURAL DEGENERATION

These reinforce the idea that long-term Fringe existence damages society.

---

## Event: Children Raised for War

### Trigger

* long continuous wars

### Description

An entire generation grows up knowing only violence.

### Outcomes

#### Encourage Warrior Culture

* levy bonuses

#### Try to Civilize Them

* captain opinion penalties

#### Exploit Their Aggression

* raid bonuses

---

## Event: Frontier Brutality Normalized

### Trigger

* very high dread realm

### Description

Cruelty becomes accepted throughout society.

### Outcomes

#### Encourage Fear

* dread increase

#### Restore Order

* stress for cruel rulers

#### Ignore the Situation

* cultural decay modifier

---

## Event: Veterans Cannot Adapt to Peace

### Trigger

* long peace after many wars

### Description

Experienced warriors struggle with peace.

### Outcomes

#### Send Them to Raid

* raid preparation bonus

#### Retire Them

* gold cost

#### Use Them as Enforcers

* control growth bonus

---

# EVENT CATEGORY — RULER PERSONAL EVENTS

---

## Event: Sleepless from Betrayal

### Trigger

* many rivals
* failed assassination attempts

### Description

The ruler becomes obsessed with betrayal.

### Outcomes

#### Trust Nobody

* intrigue gain
* diplomacy loss

#### Lean on Loyal Captains

* friendship chance

#### Descend into Paranoia

* possible paranoid trait

---

## Event: The Weight of Endless War

### Trigger

* many wars fought

### Description

Years of violence wear down the ruler.

### Outcomes

#### Push Forward

* martial bonus
* stress gain

#### Seek Rest

* temporary peace modifier

#### Become Numb to Violence

* possible callous traits

---

## Event: Dreams of Empire

### Trigger

* large realm
* ambitious ruler

### Description

The ruler dreams of permanently uniting the Fringe.

### Outcomes

#### Pursue the Dream

* conquest bonuses

#### Accept Reality

* stewardship gain

#### Begin Reform Plans

* reform progress

---

# EVENT CATEGORY — ENDGAME COLLAPSE EVENTS

These ensure massive Fringe empires eventually destabilize.

---

## Event: Too Many Captains

### Trigger

* extremely large vassal count

### Description

The ruler can no longer manage competing captains.

### Outcomes

#### Create Regional Warlords

* powerful vassal creation

#### Purge Lesser Captains

* tyranny gain

#### Allow Informal Autonomy

* tax reduction

---

## Event: The Empire Cracks

### Trigger

* massive realm
* succession instability
* low Grip

### Description

The realm begins fracturing faster than it can be controlled.

### Outcomes

#### Hold the Core Systems

* controlled fragmentation

#### Fight Everywhere

* massive war exhaustion

#### Retreat and Rebuild

* lose territory
* stability gain

---

## Event: The Captains Divide the Realm

### Trigger

* catastrophic succession

### Description

Captains informally partition the empire among themselves.

### Outcomes

#### Resist the Partition

* huge civil war

#### Negotiate Borders

* realm split peacefully

#### Flee with Loyalists

* adventurer-style survival setup

---

# EVENT CATEGORY — FINAL LEGACY EVENTS

---

## Event: The Frontier King

### Trigger

* legendary ruler dies

### Description

Stories spread across the galaxy of the ruler who nearly united the Fringe.

### Outcomes

#### Eternal Legacy

* dynasty prestige

#### Mythologized Tyrant

* dread legacy modifier

#### Forgotten Conqueror

* small prestige only

---

## Event: Return to the Fringe

### Trigger

* reformed state destabilizes

### Description

Old captains whisper that civilization has made the realm weak.

### Outcomes

#### Embrace Stability

* reform strengthened

#### Return to Raider Ways

* possible government regression

#### Compromise

* hybrid modifier

---

## Event: The Frontier Never Dies

### Trigger

* long-running Fringe culture survives collapse

### Description

Even after collapse, new captains rise from the ashes.

### Outcomes

#### The Cycle Continues

* new adventurer captains spawn

#### Attempt to End the Cycle

* legitimacy challenge

#### Celebrate the Chaos

* cultural prestige gain
# Fringe Government Event Design Document

## Phase 5 — Decisions, Decision Event Chains, and Government Transition Systems

### Purpose: Tie mechanics together through major player-facing choices

These events support major decisions and create meaningful consequences for rulers attempting to stabilize or exploit the Fringe.

---

# DECISION CHAIN — DISTRIBUTE THE SPOILS

## Decision: `eotg_fringe_distribute_spoils`

### Requirements

* completed raid or offensive war within last 2 years
* minimum gold threshold
* not bankrupt

### Immediate Effects

* spend gold
* gain Grip
* reduce faction pressure

### Follow-Up Event

---

## Event: Spoils Divided Among the Captains

### Description

The ruler gathers captains to distribute loot and rewards.

### Outcomes

#### Equal Shares for All

* broad opinion increase
* moderate Grip gain

#### Reward the Most Loyal

* selected captain gains strong loyalty
* rivals gain resentment modifier

#### Keep the Finest Treasures

* gain artifact chance
* lose Grip

### Modifiers

* `eotg_fringe_generous_distribution`
* `eotg_fringe_unfair_distribution`

---

# DECISION CHAIN — RULE THROUGH FEAR

## Decision: `eotg_fringe_rule_through_fear`

### Requirements

* high dread ruler OR wrathful/sadistic traits

### Immediate Effects

* gain dread
* short-term Grip increase

### Follow-Up Event

---

## Event: Terror in the Court

### Description

The ruler stages a brutal display to intimidate captains.

### Outcomes

#### Public Execution

* major dread gain
* diplomacy penalties

#### Torture Prisoners Publicly

* sadistic rulers gain stress loss
* compassionate rulers gain stress

#### Spare One Prisoner

* legitimacy gain
* smaller dread gain

### Modifiers

* `eotg_fringe_reign_of_terror`

---

# DECISION CHAIN — CALL THE WARBANDS

## Decision: `eotg_fringe_call_warbands`

### Requirements

* offensive war possible
* not recently called

### Immediate Effects

* temporary levy increase
* army maintenance increase

### Follow-Up Event

---

## Event: The Warbands Gather

### Description

Warriors flood toward the ruler’s banners.

### Outcomes

#### Promise Riches

* stronger levy bonus
* future unrest if no war succeeds

#### Promise Glory

* prestige bonus
* morale increase

#### Force Conscription

* control penalties

### Modifiers

* `eotg_fringe_mobilized_warbands`

---

# DECISION CHAIN — FORGE A UNIFIED FRINGE

This is a major mid-to-late game stabilization decision.

---

## Decision: `eotg_forge_unified_fringe`

### Requirements

* empire-tier ruler
* high prestige
* high dread
* large realm
* high Grip

### Immediate Effects

* temporary stabilization
* faction suppression
* legitimacy gain

### Hidden Effect

Massively worsens future succession crisis severity.

---

## Event: The Great Gathering

### Description

Captains gather from across the realm to hear the ruler proclaim unity.

### Outcomes

#### Promise Eternal Conquest

* conquest bonuses

#### Promise Stability

* reform support increases

#### Rule Through Fear

* dread increase

### Modifiers

* `eotg_fringe_unifier`

---

## Event: Some Captains Refuse Unity

### Trigger

* after unification attempt

### Description

Traditional captains reject centralized authority.

### Outcomes

#### Crush the Dissidents

* rebellion war

#### Bribe Them

* gold cost

#### Allow Limited Autonomy

* weaker centralization bonus

---

# DECISION CHAIN — BEGIN CARTEL REFORMATION

---

## Decision: `eotg_fringe_begin_cartel_reform`

### Requirements

* high gold income
* reduced raid reliance
* stable realm

### Immediate Effects

* unlock reform events
* traditionalist unrest

---

## Event: Merchants Demand Stability

### Description

Trade interests push for institutional organization.

### Outcomes

#### Empower the Merchants

* reform progress increase

#### Keep Captains Dominant

* reform slowed

#### Balance Both Sides

* mixed modifiers

---

## Event: Smugglers Become Executives

### Description

Former raiders transition into organized criminal elites.

### Outcomes

#### Encourage the Transition

* cartel conversion progress

#### Resist the Change

* captain approval

---

## Event: Traditional Captains Revolt

### Trigger

* high reform progress

### Description

Old raiders accuse the ruler of weakness.

### Outcomes

#### Crush the Old Guard

* rebellion war
* reform progress

#### Compromise

* hybrid government modifier

#### Cancel Reform

* stability restored temporarily

---

# DECISION CHAIN — BEGIN PMC REFORMATION

---

## Decision: `eotg_fringe_begin_pmc_reform`

### Requirements

* strong men-at-arms
* high martial ruler
* organized military structure

### Immediate Effects

* discipline modifiers
* captain unrest

---

## Event: Veteran Officers Demand Structure

### Description

Experienced commanders demand permanent organization.

### Outcomes

#### Establish Officer Corps

* PMC progress

#### Maintain Warband Traditions

* captain approval

#### Create Hybrid Structure

* weaker reform bonuses

---

## Event: The Free Captains Resist Discipline

### Description

Independent captains reject military hierarchy.

### Outcomes

#### Enforce Discipline

* rebellion chance

#### Grant Special Privileges

* reduced unrest

#### Allow Semi-Autonomy

* weaker PMC bonuses

---

## Event: Birth of the Contractor State

### Trigger

* successful PMC reform

### Description

The chaotic warbands reorganize into a disciplined military state.

### Outcomes

#### Fully Embrace Professionalism

* convert government

#### Preserve Raider Traditions

* hybrid modifier

### Modifiers

* `eotg_fringe_professionalized`

---

# DECISION CHAIN — SUPPRESS BREAKAWAY CAPTAINS

---

## Decision: `eotg_fringe_suppress_breakaway`

### Requirements

* disloyal powerful vassal
* low opinion

---

## Event: The Breakaway Captain Defies You

### Description

A captain openly resists central authority.

### Outcomes

#### Offer Amnesty

* reduced hostility

#### Demand Submission

* possible duel

#### Send Assassins

* intrigue event chain

#### Launch Immediate Assault

* rebellion war

---

# DECISION CHAIN — RETREAT TO THE CORE

Emergency stabilization decision.

---

## Decision: `eotg_fringe_retreat_to_core`

### Requirements

* massive instability
* multiple active factions
* low Grip

### Immediate Effects

* voluntarily release distant territories
* major stability boost

---

## Event: Abandoning the Frontier

### Description

The ruler withdraws from distant territories to preserve the core realm.

### Outcomes

#### Preserve the Heartland

* stability increase

#### Leave Scorched Worlds Behind

* dread gain

#### Appoint Independent Allies

* tributary creation chance

---

# DECISION CHAIN — DECLARE THE GREAT RAID

Legendary high-risk conquest decision.

---

## Decision: `eotg_fringe_great_raid`

### Requirements

* high prestige
* strong armies
* major target nearby

### Immediate Effects

* raid bonuses
* army morale increase

### Risk

Failure causes catastrophic instability.

---

## Event: Preparations for the Great Raid

### Description

The realm prepares for an enormous campaign.

### Outcomes

#### Promise Riches Beyond Imagination

* morale increase

#### Promise Immortality Through Glory

* prestige bonus

#### Force Participation

* control penalties

---

## Event: Triumph of the Great Raid

### Trigger

* successful war

### Outcomes

#### Legendary Victory

* massive prestige
* Grip increase

#### Reward the Captains Generously

* loyalty bonuses

#### Claim Everything Personally

* huge gold gain
* future instability

---

## Event: Disaster of the Great Raid

### Trigger

* failed campaign

### Outcomes

#### The Captains Turn Against You

* faction surge

#### The Armies Desert

* levy collapse

#### Blame the Generals

* rivalry chains

### Modifiers

* `eotg_fringe_failed_great_raid`

---

# DECISION CHAIN — NAME A SUCCESSOR

Attempt to stabilize succession manually.

---

## Decision: `eotg_fringe_name_successor`

### Requirements

* aging ruler
* high prestige

### Immediate Effects

* chosen heir gains support modifier

### Risk

Other captains may oppose decision.

---

## Event: The Captains Debate the Successor

### Description

The captains react to the ruler’s chosen heir.

### Outcomes

#### Force Acceptance

* dread gain

#### Negotiate Support

* gold cost

#### Allow Debate

* diplomacy challenge

---

## Event: Rival Claimants Emerge

### Trigger

* weak chosen heir

### Description

Other captains back rival candidates.

### Outcomes

#### Buy Their Loyalty

* expensive

#### Prepare for Succession War

* military modifiers

#### Assassinate Rivals

* intrigue chain

---

Add a path for Fringe government to feudalize

---

# Gob-Corp Government Event Design Document

## Phase 1 — Functional + Core Flavor Events

### Target: ~40 Events for Beta Functionality

### Purpose: Establish corporate oligarchy gameplay, factional board politics, market competition, and Vote of No Confidence instability

Government Reference: `eotg_gobcorp_government` 

---

# CORE GOVERNMENT FANTASY

The Gob-Corp Government is not a stable corporation.

It is:

* corrupt industrial oligarchy
* faction-ridden trade empire
* unstable alliance of Trade Princes
* profit-driven political machine

The Director-General survives through:

* political maneuvering
* board alliances
* bribery
* economic dominance
* fear of instability

The core gameplay loop is:

1. Expand economic influence
2. Empower Trade Princes
3. Compete for market dominance
4. Survive internal corporate sabotage
5. Avoid Vote of No Confidence
6. Manipulate factional politics

---

# EVENT CATEGORY — MARKET FACTIONS

These reinforce the market faction system.

---

## Event: A Combine Gains Dominance

### Trigger

* faction market share threshold reached

### Description

One Trade Combine begins economically dominating the realm.

### Outcomes

#### Support the Dominant Combine

* faction leader opinion gain
* gold bonus
* rival faction hostility

#### Secretly Fund Rivals

* weaker factions gain power
* intrigue gain

#### Regulate Their Expansion

* stability increase
* dominant faction anger

### Modifiers

* `eotg_gobcorp_market_monopoly`
* `eotg_gobcorp_faction_favoritism`

---

## Event: Market Manipulation Allegations

### Trigger

* powerful faction leader
* high greed characters

### Description

Accusations spread that a Trade Prince manipulates prices and trade flow.

### Outcomes

#### Ignore the Allegations

* gold increase
* legitimacy penalty

#### Launch Investigation

* intrigue challenge

#### Publicly Support the Prince

* faction loyalty gain
* rival anger

---

## Event: Rival Combines Clash

### Trigger

* two powerful factions

### Description

Trade wars erupt between competing combines.

### Outcomes

#### Mediate the Dispute

* diplomacy challenge

#### Side with One Combine

* one faction strengthened

#### Exploit the Conflict

* gain gold
* instability increase

---

# EVENT CATEGORY — TRADE PRINCE POLITICS

---

## Event: A Trade Prince Demands Board Representation

### Trigger

* powerful vassal
* high gold income

### Description

A wealthy Trade Prince demands greater influence in corporate governance.

### Outcomes

#### Grant Board Seat

* loyalty increase
* vote influence increase

#### Refuse Them

* faction hostility

#### Offer Temporary Privileges

* temporary loyalty modifier

### Modifiers

* `eotg_gobcorp_board_member`

---

## Event: Industrial Rivalry Escalates

### Trigger

* rival Trade Princes

### Description

Two Trade Princes sabotage each other’s operations.

### Outcomes

#### Allow Competition

* economic growth
* instability increase

#### Intervene Directly

* opinion penalties

#### Secretly Encourage One Side

* hook generation chance

---

## Event: A Prince Hoards Wealth

### Trigger

* extremely wealthy vassal

### Description

A Trade Prince accumulates enormous economic power.

### Outcomes

#### Tax Their Holdings

* gold gain
* loyalty loss

#### Ignore Their Growth

* future faction threat

#### Force Shared Investment

* realm development bonus

---

# EVENT CATEGORY — VOTE OF NO CONFIDENCE

This is the defining mechanic chain.

---

## Event: Whispers in the Boardroom

### Trigger

* low prestige Director-General
* instability modifier active

### Description

Board members quietly discuss removing the Director-General.

### Outcomes

#### Bribe the Board

* gold cost
* reduce vote momentum

#### Threaten Dissidents

* dread gain
* scandal risk

#### Ignore the Rumors

* no immediate effect

---

## Event: The Vote Is Called

### Trigger

* confidence threshold reached

### Description

The Board formally calls a Vote of No Confidence.

### Outcomes

#### Campaign for Support

* diplomacy challenge

#### Buy Votes

* large gold cost

#### Prepare for Refusal

* unlock conflict preparation modifier

---

## Event: Board Members Choose Sides

### Trigger

* active vote chain

### Description

Trade Princes publicly declare support or opposition.

### Outcomes

#### Promise Reforms

* gain temporary support

#### Offer Board Privileges

* loyalty shifts

#### Threaten Economic Retaliation

* dread increase

---

## Event: The Vote Passes

### Trigger

* failed confidence defense

### Description

The Board votes to remove the Director-General.

### Outcomes

#### Step Down Gracefully

* honorable exit modifier
* prestige retained

#### Refuse the Decision

* unlock Boardroom War

---

## Event: The Director-General Refuses

### Trigger

* refusal outcome chosen

### Description

The Director-General rejects the Board’s authority.

### Outcomes

#### Mobilize Loyal Princes

* civil conflict preparation

#### Attempt Last-Minute Negotiation

* diplomacy challenge

#### Purge Dissidents

* tyranny increase

---

## Event: Boardroom War Begins

### Trigger

* refusal path

### Description

Corporate civil war erupts across the realm.

### Outcomes

#### Fight for Authority

* war bonuses

#### Seek Settlement

* possible negotiated abdication

---

# EVENT CATEGORY — ECONOMIC INSTABILITY

---

## Event: Industrial Accident

### Trigger

* industrial holdings
* low stewardship ruler

### Description

A catastrophic accident kills workers and disrupts production.

### Outcomes

#### Compensate the Victims

* gold loss
* legitimacy gain

#### Cover It Up

* intrigue challenge

#### Blame Local Managers

* opinion penalties

### Modifiers

* `eotg_gobcorp_factory_disaster`

---

## Event: Worker Unrest

### Trigger

* high taxation
* poor conditions

### Description

Workers protest exploitative labor conditions.

### Outcomes

#### Increase Wages

* gold loss
* unrest reduced

#### Hire Security Forces

* dread increase

#### Ignore the Protest

* revolt risk

---

## Event: Smuggling Through Corporate Ports

### Trigger

* corrupt vassals
* high trade activity

### Description

Illegal goods move through corporate shipping networks.

### Outcomes

#### Profit from Smuggling

* gold gain

#### Crack Down

* intrigue challenge

#### Partner with Smugglers

* corruption modifier

---

# EVENT CATEGORY — BOARD INTRIGUE

---

## Event: Secret Shareholder Alliance

### Trigger

* multiple dissatisfied board members

### Description

Several powerful Trade Princes form a hidden alliance.

### Outcomes

#### Infiltrate the Alliance

* intrigue opportunity

#### Offer Concessions

* loyalty gain

#### Publicly Expose Them

* scandal event chance

---

## Event: Blackmail Material Acquired

### Trigger

* intrigue focus
* rival board member

### Description

Evidence of corruption or illegal dealings is uncovered.

### Outcomes

#### Use It Quietly

* strong hook

#### Public Scandal

* target legitimacy loss

#### Sell the Information

* gold gain

---

## Event: A Prince Funds Assassins

### Trigger

* strong rivalry

### Description

Rumors suggest a Trade Prince hired killers against rivals.

### Outcomes

#### Investigate

* intrigue chain

#### Ignore It

* future violence escalation

#### Secretly Approve

* dread increase

---

# EVENT CATEGORY — CORPORATE CULTURE

---

## Event: Lavish Board Banquet

### Trigger

* prosperous economy

### Description

The elite gather for extravagant celebration.

### Outcomes

#### Impress the Board

* diplomacy bonus

#### Make Secret Deals

* hook opportunities

#### Display Wealth Excessively

* worker unrest chance

---

## Event: Young Executive Prodigy

### Trigger

* talented child character

### Description

A young heir displays remarkable economic talent.

### Outcomes

#### Mentor Them Personally

* stewardship growth

#### Push Them Ruthlessly

* stress risk

#### Exploit Their Talent

* short-term bonuses

---

## Event: Corporate Propaganda Campaign

### Trigger

* legitimacy loss

### Description

Massive propaganda efforts attempt to restore public trust.

### Outcomes

#### Honest Messaging

* modest legitimacy gain

#### Aggressive Propaganda

* stronger short-term gain
* scandal risk later

#### Attack Rivals Instead

* rival legitimacy damage

---

# EVENT CATEGORY — SUCCESSION EVENTS

---

## Event: Election Season Begins

### Trigger

* aging Director-General
* succession approaching

### Description

Trade Princes begin maneuvering for the next election.

### Outcomes

#### Endorse a Successor

* influence successor support

#### Stay Neutral

* legitimacy gain

#### Secretly Manipulate the Vote

* intrigue opportunities

---

## Event: Corporate Dynasty Rivalries

### Trigger

* election period

### Description

Major corporate families intensify their political struggle.

### Outcomes

#### Back One Dynasty

* faction alignment

#### Balance the Families

* diplomacy challenge

#### Exploit Their Rivalry

* intrigue gain

---

## Event: The New Director-General Takes Power

### Trigger

* succession completed

### Description

The Board recognizes the new Director-General.

### Outcomes

#### Promise Stability

* legitimacy gain

#### Reward Loyal Supporters

* faction shifts

#### Purge Opposition

* dread increase
# Gob-Corp Government Event Design Document

## Phase 2 — Reinforcement, Corporate Warfare, and Industrial Political Chaos

### Purpose: Expand boardroom politics, economic warfare, corruption ecosystems, and internal oligarch instability

---

# EVENT CATEGORY — TRADE COMBINE POWER STRUGGLES

---

## Event: A Combine Attempts Monopoly Control

### Trigger

* dominant faction extremely powerful
* weak Director-General

### Description

A Trade Combine attempts to dominate an entire sector of the economy.

### Outcomes

#### Allow the Monopoly

* large gold increase
* rival faction unrest

#### Break Their Control

* stewardship challenge
* possible economic slowdown

#### Secretly Profit from It

* corruption modifier
* personal wealth gain

### Modifiers

* `eotg_gobcorp_sector_monopoly`
* `eotg_gobcorp_market_corruption`

---

## Event: Combine Sabotage Operations

### Trigger

* strong faction rivalry

### Description

Factories, cargo routes, and industrial assets are mysteriously sabotaged.

### Outcomes

#### Investigate the Sabotage

* intrigue challenge

#### Blame Rival Combine

* faction hostility increases

#### Cover Up the Damage

* temporary stability
* future scandal risk

---

## Event: Illegal Price Fixing Ring

### Trigger

* greedy faction leaders
* prosperous economy

### Description

Several Trade Princes secretly manipulate prices together.

### Outcomes

#### Join the Scheme

* major gold gain
* legitimacy penalty

#### Expose the Ring

* faction anger
* legitimacy gain

#### Demand a Cut

* gold gain
* corruption modifier

---

# EVENT CATEGORY — INDUSTRIAL WORKER CRISES

These make the realm feel industrial and unstable.

---

## Event: Factory Workers Riot

### Trigger

* high extraction contracts
* poor county conditions

### Description

Workers riot over deadly conditions and brutal labor demands.

### Outcomes

#### Send Corporate Security

* dread gain
* revolt suppression

#### Negotiate with Workers

* gold cost
* unrest reduction

#### Ignore the Riots

* development damage

### Modifiers

* `eotg_gobcorp_worker_unrest`

---

## Event: Child Labor Scandal

### Trigger

* exploitative rulers
* low legitimacy

### Description

Reports spread that children are dying in dangerous factories.

### Outcomes

#### Ban the Practice

* economic penalty
* legitimacy gain

#### Deny Everything

* intrigue challenge

#### Continue Quietly

* gold bonus
* scandal risk

---

## Event: Toxic Industrial Spill

### Trigger

* industrial development
* low stewardship

### Description

Industrial chemicals poison nearby districts.

### Outcomes

#### Clean the Damage

* major gold cost

#### Hide the Disaster

* intrigue challenge

#### Blame a Rival Prince

* rivalry escalation

---

# EVENT CATEGORY — BOARDROOM CONSPIRACIES

---

## Event: Secret Meeting of the Board

### Trigger

* unstable government
* multiple hostile vassals

### Description

Board members secretly gather without informing the Director-General.

### Outcomes

#### Spy on the Meeting

* hook chance

#### Interrupt the Gathering

* opinion penalties

#### Pretend Ignorance

* future conspiracy risk

---

## Event: Corporate Blackmail Files

### Trigger

* intrigue-heavy character

### Description

Sensitive financial records are discovered.

### Outcomes

#### Use the Files

* strong hook

#### Leak the Documents

* target legitimacy damage

#### Destroy the Evidence

* stress reduction for honest rulers

---

## Event: Assassination by Accounting

### Trigger

* strong rivalry

### Description

A rival manipulates contracts and finances to ruin a Trade Prince completely.

### Outcomes

#### Protect the Victim

* loyalty gain

#### Allow the Ruin

* rival weakened

#### Exploit Both Sides

* gold gain

---

# EVENT CATEGORY — CORPORATE SECURITY & PARAMILITARIES

---

## Event: Security Forces Brutalize Workers

### Trigger

* high dread
* worker unrest

### Description

Corporate security massacres protesting workers.

### Outcomes

#### Approve the Violence

* dread gain
* legitimacy loss

#### Punish the Officers

* legitimacy gain
* security loyalty loss

#### Cover It Up

* intrigue challenge

---

## Event: Private Militias Clash

### Trigger

* rival Trade Princes

### Description

Corporate militias fight openly in industrial districts.

### Outcomes

#### Support One Side

* faction shift

#### Send Peacekeepers

* gold cost

#### Let Them Bleed Each Other

* reduced rival strength

---

## Event: A Security Chief Gains Influence

### Trigger

* strong marshal equivalent

### Description

Corporate security leadership becomes politically powerful.

### Outcomes

#### Promote Them

* military bonus
* future coup risk

#### Limit Their Power

* opinion penalty

#### Use Them Against Rivals

* intrigue bonus

---

# EVENT CATEGORY — ECONOMIC BOOMS & CRASHES

---

## Event: Sudden Economic Boom

### Trigger

* prosperous trade network

### Description

Trade profits surge across the realm.

### Outcomes

#### Invest in Expansion

* development gain

#### Reward Loyal Princes

* faction loyalty gain

#### Hoard the Wealth

* personal treasury increase

### Modifier

* `eotg_gobcorp_market_boom`

---

## Event: Market Collapse

### Trigger

* failed investments
* instability

### Description

Panic spreads through corporate markets.

### Outcomes

#### Bail Out the Combines

* major gold cost

#### Let Weak Companies Die

* faction reshuffling

#### Blame Foreign Rivals

* diplomacy penalties

### Modifier

* `eotg_gobcorp_market_crash`

---

## Event: Counterfeit Trade Certificates

### Trigger

* corruption high

### Description

Fake trade contracts flood the market.

### Outcomes

#### Crack Down Aggressively

* intrigue challenge

#### Secretly Profit

* corruption gain

#### Ignore the Problem

* economy penalty

---

# EVENT CATEGORY — SUCCESSION MANIPULATION

---

## Event: Vote Buying Before Election

### Trigger

* active succession cycle

### Description

Trade Princes openly trade favors and wealth for votes.

### Outcomes

#### Participate Aggressively

* gold cost
* election advantage

#### Publicly Condemn Corruption

* legitimacy gain

#### Secretly Manipulate Votes

* intrigue opportunity

---

## Event: A Candidate Is Exposed

### Trigger

* election cycle

### Description

Damaging information emerges about a candidate.

### Outcomes

#### Exploit the Scandal

* rival vote reduction

#### Defend the Candidate

* alliance opportunity

#### Fabricate Worse Evidence

* intrigue risk

---

## Event: Boardroom Coup Rumors

### Trigger

* weak Director-General
* ambitious board members

### Description

Rumors spread of an organized political takeover attempt.

### Outcomes

#### Purge Suspects

* tyranny increase

#### Bribe Loyalists

* gold cost

#### Prepare for Conflict

* military readiness modifier

---

# EVENT CATEGORY — CORPORATE CULTURE & EXCESS

---

## Event: Executive Luxury Scandal

### Trigger

* poor economy
* wealthy ruler

### Description

The elite indulge in massive luxury while workers suffer.

### Outcomes

#### Defend Elite Privilege

* noble loyalty gain
* unrest increase

#### Public Charity Campaign

* legitimacy gain
* gold cost

#### Hide the Excess

* intrigue challenge

---

## Event: Industrial Innovation Competition

### Trigger

* high stewardship rulers

### Description

Trade Princes compete to develop profitable innovations.

### Outcomes

#### Fund the Competition

* development growth

#### Rig the Outcome

* intrigue gain

#### Sell the Innovation Abroad

* gold gain

---

## Event: The Director-General's Public Address

### Trigger

* legitimacy concerns

### Description

The ruler addresses the realm directly.

### Outcomes

#### Promise Reform

* legitimacy gain

#### Threaten Dissidents

* dread gain

#### Celebrate Prosperity

* economic confidence bonus

---

# EVENT CATEGORY — INTERNAL CORPORATE DECAY

---

## Event: Corruption Becomes Systemic

### Trigger

* high corruption modifiers

### Description

Bribery and corruption infect every level of governance.

### Outcomes

#### Attempt Reform

* stability gain
* elite anger

#### Accept Corruption

* gold gain
* legitimacy decay

#### Weaponize the Corruption

* intrigue bonuses

---

## Event: Trade Princes Ignore Central Authority

### Trigger

* weak Director-General

### Description

Powerful Trade Princes increasingly act independently.

### Outcomes

#### Reassert Authority

* conflict risk

#### Grant More Freedom

* autonomy increase

#### Secretly Divide Them

* intrigue opportunity

---

## Event: The Board Loses Faith

### Trigger

* multiple failures
* low legitimacy

### Description

Even loyal board members begin doubting leadership.

### Outcomes

#### Promise Radical Reform

* temporary stability

#### Rule Through Fear

* dread gain

#### Prepare for No Confidence Vote

* defensive modifier

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: The Golden Director-General

### Trigger

* extremely successful reign

### Description

The ruler becomes legendary for economic success.

### Outcomes

#### Embrace the Legend

* massive prestige gain

#### Share Credit with the Board

* loyalty increase

#### Consolidate Power

* succession danger later

### Modifier

* `eotg_gobcorp_golden_age`

---

## Event: The Corporate Civil War

### Trigger

* failed Vote of No Confidence
* multiple hostile factions

### Description

The corporate oligarchy collapses into open warfare.

### Outcomes

#### Crush the Opposition

* war bonuses

#### Negotiate Division

* realm split possibility

#### Flee with Loyalists

* exile chain possibility

---

## Event: The Market Remembers

### Trigger

* famous Director-General death

### Description

Trade Princes recount the ruler’s triumphs and betrayals.

### Outcomes

#### Celebrate Their Legacy

* dynasty prestige

#### Rewrite Their History

* legitimacy gain

#### Blame Them for Current Problems

* successor advantage modifier
# Gob-Corp Government Event Design Document

## Phase 3 — Decision Chains, Economic Control Systems, and Advanced Political Crises

### Purpose: Tie government mechanics into active player choices and create long-term oligarch gameplay loops

---

# DECISION CHAIN — CALL A BOARD SUMMIT

## Decision: `eotg_gobcorp_call_board_summit`

### Requirements

* not recently used
* minimum number of powerful vassals
* realm stability below threshold OR active faction tension

### Immediate Effects

* temporary faction pause
* begins summit event chain

---

## Event: The Board Gathers

### Description

Trade Princes gather to negotiate the future of the realm.

### Outcomes

#### Negotiate Compromises

* faction hostility reduced
* reduced authority temporarily

#### Demand Absolute Loyalty

* dread gain
* faction escalation risk

#### Play the Factions Against Each Other

* intrigue challenge
* hook opportunities

### Modifiers

* `eotg_gobcorp_board_summit`

---

## Event: Secret Deals During the Summit

### Trigger

* intrigue characters present

### Description

Private negotiations occur behind closed doors.

### Outcomes

#### Spy on the Negotiations

* possible hooks

#### Join the Secret Deals

* corruption gain
* alliance opportunities

#### Publicly Expose Corruption

* legitimacy gain
* elite anger

---

## Event: Summit Ends in Chaos

### Trigger

* failed diplomacy outcomes

### Description

The summit collapses into accusations and threats.

### Outcomes

#### Threaten the Board

* dread gain

#### Offer Economic Concessions

* gold cost

#### Walk Out in Anger

* no confidence momentum increase

---

# DECISION CHAIN — MANIPULATE THE MARKET

## Decision: `eotg_gobcorp_manipulate_market`

### Requirements

* high stewardship OR intrigue
* prosperous economy

### Immediate Effects

* temporary economic boost
* risk of scandal

---

## Event: Artificial Market Boom

### Description

The government artificially inflates market confidence.

### Outcomes

#### Push Aggressive Growth

* large short-term gold gain
* future crash risk

#### Moderate Expansion

* stable smaller gains

#### Secret Insider Trading

* personal gold gain
* corruption modifier

### Modifier

* `eotg_gobcorp_market_speculation`

---

## Event: Investors Panic

### Trigger

* failed manipulation

### Description

Confidence collapses after suspicious market behavior.

### Outcomes

#### Bail Out the Economy

* major gold cost

#### Sacrifice Smaller Combines

* faction reshuffling

#### Blame Foreign Rivals

* diplomacy penalties

---

# DECISION CHAIN — BUY BOARD LOYALTY

## Decision: `eotg_gobcorp_buy_board_loyalty`

### Requirements

* sufficient gold
* unstable board relations

### Immediate Effects

* improved board opinion
* hidden corruption increase

---

## Event: Gifts to the Board

### Description

Lavish gifts and favors are distributed to powerful Trade Princes.

### Outcomes

#### Extravagant Bribes

* strong loyalty increase
* corruption growth

#### Subtle Incentives

* modest opinion gains

#### Threaten Instead of Paying

* dread gain
* possible backlash

---

## Event: Bribery Scandal Leaks

### Trigger

* intrigue failure chance

### Description

Evidence of bribery reaches the public.

### Outcomes

#### Deny Everything

* intrigue challenge

#### Sacrifice a Trade Prince

* target loses power

#### Admit Corruption Openly

* legitimacy damage
* elite loyalty gain

---

# DECISION CHAIN — CORPORATE PURGE

## Decision: `eotg_gobcorp_corporate_purge`

### Requirements

* high dread
* active faction threats

### Immediate Effects

* attempt to weaken factions
* legitimacy risk

---

## Event: Executives Disappear Overnight

### Description

Corporate officials vanish as the purge begins.

### Outcomes

#### Continue the Purge

* faction suppression
* dread gain

#### Target Only Rivals

* intrigue-focused outcome

#### Halt the Purge

* stability partially restored

### Modifiers

* `eotg_gobcorp_purge`

---

## Event: Fear Spreads Through the Board

### Trigger

* purge active

### Description

Trade Princes become terrified of being targeted next.

### Outcomes

#### Encourage Fear

* dread increase

#### Offer Safety to Loyalists

* faction loyalty gain

#### Secretly Prepare More Arrests

* intrigue advantage

---

# DECISION CHAIN — EXPAND CORPORATE HOLDINGS

## Decision: `eotg_gobcorp_expand_holdings`

### Requirements

* strong economy
* development threshold

### Immediate Effects

* investment costs
* growth modifiers

---

## Event: New Industrial Expansion

### Description

Massive industrial construction begins.

### Outcomes

#### Focus on Production

* tax growth

#### Focus on Infrastructure

* development growth

#### Exploit Cheap Labor

* faster growth
* unrest increase

---

## Event: Construction Corruption

### Trigger

* corrupt officials

### Description

Funds disappear during expansion projects.

### Outcomes

#### Investigate Corruption

* stewardship challenge

#### Ignore the Losses

* corruption increase

#### Profit Personally

* gold gain

---

# DECISION CHAIN — PREPARE SUCCESSOR

## Decision: `eotg_gobcorp_prepare_successor`

### Requirements

* aging Director-General
* eligible heir/candidate exists

### Immediate Effects

* chosen candidate gains support modifier

---

## Event: The Chosen Executive

### Description

The ruler quietly promotes a favored successor.

### Outcomes

#### Public Endorsement

* strong support gain
* rival hostility

#### Secret Promotion

* intrigue bonus

#### Test Multiple Candidates

* flexibility modifier

---

## Event: Rival Princes Resist the Successor

### Trigger

* succession tension

### Description

Trade Princes oppose the chosen candidate.

### Outcomes

#### Buy Their Support

* gold cost

#### Threaten Them

* dread gain

#### Divide the Opposition

* intrigue challenge

---

# DECISION CHAIN — SUPPRESS A COMBINE

## Decision: `eotg_gobcorp_suppress_combine`

### Requirements

* dominant faction too powerful

### Immediate Effects

* faction targeted
* economic risk

---

## Event: Government Investigation Begins

### Description

Officials investigate a powerful Combine.

### Outcomes

#### Seize Their Assets

* gold gain
* rebellion risk

#### Fine Them Heavily

* gold gain
* moderate anger

#### Force Leadership Changes

* faction reshuffling

---

## Event: The Combine Fights Back

### Trigger

* suppression resisted

### Description

The targeted Combine retaliates economically and politically.

### Outcomes

#### Escalate the Conflict

* civil conflict risk

#### Negotiate Settlement

* compromise outcome

#### Publicly Humiliate Them

* prestige gain
* future revenge modifier

---

# DECISION CHAIN — DECLARE CORPORATE EMERGENCY

Emergency anti-collapse decision.

---

## Decision: `eotg_gobcorp_corporate_emergency`

### Requirements

* active no confidence threat
* multiple factions
* economic instability

### Immediate Effects

* temporary emergency powers
* legitimacy penalty

---

## Event: Emergency Powers Invoked

### Description

The Director-General declares extraordinary authority.

### Outcomes

#### Seize Full Control

* major authority gain
* tyranny increase

#### Temporary Emergency Measures

* moderate stability

#### Blame External Enemies

* diplomatic penalties

### Modifiers

* `eotg_gobcorp_emergency_powers`

---

## Event: The Board Questions Emergency Rule

### Trigger

* emergency powers active

### Description

Board members fear dictatorship.

### Outcomes

#### Promise Temporary Measures

* legitimacy gain

#### Threaten the Board

* dread gain

#### Arrest Dissidents

* faction escalation

---

# DECISION CHAIN — ENGINEER A MARKET CRASH

Dark high-risk intrigue option.

---

## Decision: `eotg_gobcorp_engineer_crash`

### Requirements

* intrigue-focused ruler
* rival combine powerful

### Immediate Effects

* destabilizes target faction

---

## Event: Financial Panic Spreads

### Description

Markets collapse around targeted rivals.

### Outcomes

#### Profit from the Collapse

* massive gold gain

#### Absorb Rival Assets

* faction power increase

#### Hide Your Involvement

* intrigue challenge

---

## Event: The Crash Escapes Control

### Trigger

* failed manipulation

### Description

Economic collapse spreads across the realm.

### Outcomes

#### Emergency Intervention

* massive gold cost

#### Sacrifice Smaller Princes

* faction reshuffling

#### Let the Weak Die

* severe instability

---

# Corporation Government Event Design Document

## Phase 1 — Functional + Core Flavor Events

### Target: ~50 Events for Beta Functionality

### Purpose: Establish cyberpunk corporate politics, executive sabotage, board manipulation, and hostile acquisition gameplay

Government Reference: `eotg_corporation_government` 

---

# CORE GOVERNMENT FANTASY

Unlike Gob-Corp chaos, Corporation Government is:

* sleek
* professional
* predatory
* hyper-capitalist
* paranoid
* image-conscious

The lower ranks are ruthless corporate climbers.

The upper ranks are cold strategic manipulators.

The government fantasy is:

> “Smile publicly. Destroy rivals privately.”

Core gameplay loop:

1. sabotage rivals
2. manipulate the board
3. maintain corporate image
4. dominate markets
5. absorb weaker rivals
6. survive executive conspiracies

---

# EVENT CATEGORY — SABOTAGE RIVAL SYSTEM

This is the defining mechanic chain.

---

## Event: Financial Irregularities Detected

### Trigger

* sabotage scheme succeeds

### Description

Evidence emerges that a rival executive’s division suffers unexplained financial losses.

### Outcomes

#### Leak the Information

* target legitimacy loss

#### Blackmail the Executive

* strong hook

#### Quietly Profit from Their Collapse

* gold gain

### Modifiers

* `eotg_corporation_financial_sabotage`

---

## Event: Internal Systems Breach

### Trigger

* sabotage scheme success

### Description

Corporate infrastructure mysteriously fails across rival holdings.

### Outcomes

#### Escalate the Sabotage

* additional target penalties

#### Pretend Sympathy

* diplomacy gain

#### Blame Foreign Competitors

* external tension modifier

---

## Event: Sabotage Discovered

### Trigger

* sabotage scheme exposed

### Description

Evidence points back to the schemer.

### Outcomes

#### Deny Everything

* intrigue challenge

#### Sacrifice a Subordinate

* opinion penalties to subordinate

#### Publicly Threaten the Accuser

* dread gain

### Modifiers

* `eotg_corporation_exposed_schemer`

---

# EVENT CATEGORY — BOARD INFLUENCE

---

## Event: Board Members Demand Favors

### Trigger

* low board influence

### Description

Regional Directors demand concessions in exchange for support.

### Outcomes

#### Grant Concessions

* board influence gain

#### Promise Future Rewards

* temporary support

#### Refuse Them

* no confidence pressure increases

---

## Event: A Director Questions Leadership

### Trigger

* low legitimacy CEO

### Description

A powerful Regional Director publicly criticizes leadership.

### Outcomes

#### Public Debate

* diplomacy challenge

#### Secret Blackmail

* intrigue challenge

#### Remove Them Quietly

* assassination/sabotage chain

---

## Event: Board Influence Drains Away

### Trigger

* failed wars
* economic downturn

### Description

Confidence in executive leadership erodes.

### Outcomes

#### Launch PR Campaign

* legitimacy gain
* gold cost

#### Offer Executive Contracts

* board loyalty increase

#### Threaten Dissenters

* dread gain

---

# EVENT CATEGORY — HOSTILE ACQUISITIONS

---

## Event: Acquisition Proposal Sent

### Trigger

* hostile acquisition attempt

### Description

A rival receives an offer to surrender assets peacefully.

### Outcomes

#### Accept the Offer

* peaceful transfer

#### Negotiate Better Terms

* diplomacy challenge

#### Reject the Acquisition

* proxy war risk

---

## Event: Shareholders Demand Expansion

### Trigger

* prosperous economy

### Description

Investors demand aggressive growth.

### Outcomes

#### Pursue Acquisitions

* acquisition bonuses

#### Focus on Stability

* development bonus

#### Manipulate Investor Expectations

* intrigue modifier

---

## Event: Corporate Merger Disaster

### Trigger

* failed acquisition

### Description

A merger spirals into chaos and inefficiency.

### Outcomes

#### Force Integration

* control penalties

#### Sell Off Assets

* partial recovery

#### Blame Former Leadership

* legitimacy shift

---

# EVENT CATEGORY — EXECUTIVE WARFARE

---

## Event: Executive Assassination Rumors

### Trigger

* strong rivalries

### Description

Rumors spread that executives hire killers against competitors.

### Outcomes

#### Investigate Quietly

* intrigue challenge

#### Ignore the Rumors

* future violence escalation

#### Weaponize the Rumors

* target legitimacy damage

---

## Event: Corporate Espionage Leak

### Trigger

* intrigue-heavy rulers

### Description

Sensitive internal documents leak publicly.

### Outcomes

#### Suppress the Leak

* intrigue challenge

#### Blame Rivals

* diplomatic tension

#### Exploit the Leak

* weaken rival factions

---

## Event: Security Division Expands Power

### Trigger

* high militarization

### Description

Corporate security gains growing political influence.

### Outcomes

#### Empower Security Forces

* military bonuses
* authoritarian drift

#### Restrict Their Power

* security anger

#### Use Them Against Rivals

* intrigue gain

---

# EVENT CATEGORY — PUBLIC IMAGE & PR

This government must maintain image.

---

## Event: Public Relations Crisis

### Trigger

* scandals
* worker deaths
* sabotage exposure

### Description

Public trust in the corporation collapses.

### Outcomes

#### Massive PR Campaign

* legitimacy gain
* gold cost

#### Suppress the News

* intrigue challenge

#### Blame Rogue Employees

* minor recovery

### Modifiers

* `eotg_corporation_pr_crisis`

---

## Event: Executive Charity Event

### Trigger

* prosperous ruler

### Description

The corporation publicly funds humanitarian projects.

### Outcomes

#### Genuine Charity

* legitimacy gain

#### Hidden Profit Scheme

* gold gain

#### Pure Propaganda

* short-term legitimacy only

---

## Event: Media Manipulation Operation

### Trigger

* intrigue ruler

### Description

Executives manipulate public narratives.

### Outcomes

#### Attack Rivals Publicly

* rival legitimacy damage

#### Promote Corporate Unity

* faction stability

#### Spread Fear

* dread gain

---

# EVENT CATEGORY — LOWER EXECUTIVE CUTTHROAT POLITICS

These reinforce Account Director brutality.

---

## Event: Promotion by Betrayal

### Trigger

* ambitious lower executive

### Description

An executive sabotages coworkers for advancement.

### Outcomes

#### Reward Ruthlessness

* intrigue gain

#### Punish Them

* legitimacy gain

#### Secretly Encourage It

* corruption increase

---

## Event: Data Theft Between Divisions

### Trigger

* rivalry between vassals

### Description

Confidential information is stolen internally.

### Outcomes

#### Punish Both Sides

* authority gain

#### Support One Division

* faction alignment shift

#### Sell the Data Externally

* gold gain

---

## Event: Executive Burnout

### Trigger

* long intrigue conflicts

### Description

An executive collapses under stress.

### Outcomes

#### Replace Them

* efficiency restored

#### Exploit Their Weakness

* hook gain

#### Support Recovery

* opinion gain

---

# EVENT CATEGORY — SUCCESSION & CEO ELECTIONS

---

## Event: The Succession Race Begins

### Trigger

* aging CEO

### Description

Executives begin maneuvering for leadership.

### Outcomes

#### Endorse a Candidate

* succession influence

#### Secretly Sabotage Rivals

* intrigue opportunities

#### Public Neutrality

* legitimacy gain

---

## Event: Corporate Interference Operation

### Trigger

* succession period

### Description

Executives secretly manipulate vote systems.

### Outcomes

#### Rig the Election

* election advantage
* scandal risk

#### Blackmail Directors

* hooks gained

#### Spread False Information

* intrigue challenge

---

## Event: Election Scandal Erupts

### Trigger

* interference exposed

### Description

Evidence emerges of election manipulation.

### Outcomes

#### Deny Everything

* intrigue challenge

#### Sacrifice Executives

* damage containment

#### Double Down

* legitimacy collapse risk

---

## Event: The New CEO Ascends

### Trigger

* election complete

### Description

The corporation welcomes new leadership.

### Outcomes

#### Promise Stability

* legitimacy gain

#### Reward Loyal Directors

* faction support

#### Purge Opposition

* dread increase

---

# EVENT CATEGORY — CORPORATE ECONOMIC PRESSURE

---

## Event: Investor Panic

### Trigger

* economic instability

### Description

Major investors fear collapse.

### Outcomes

#### Reassure Investors

* diplomacy challenge

#### Hide the Numbers

* intrigue challenge

#### Sacrifice Smaller Divisions

* faction losses

---

## Event: Hostile Market Competition

### Trigger

* strong rival corporation nearby

### Description

Aggressive economic warfare erupts.

### Outcomes

#### Compete Aggressively

* growth bonus

#### Sabotage Competitors

* intrigue risk

#### Negotiate Agreements

* diplomacy outcome

---

## Event: Corporate Overexpansion

### Trigger

* massive realm growth

### Description

The corporation struggles to manage distant assets.

### Outcomes

#### Decentralize Operations

* vassal empowerment

#### Centralize Everything

* unrest increase

#### Sell Remote Holdings

* gold recovery

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: The Perfect Executive

### Trigger

* highly successful CEO

### Description

The CEO becomes legendary for ruthless competence.

### Outcomes

#### Build Personality Cult

* authority gain

#### Strengthen the Institution

* stability gain

#### Exploit the Reputation

* diplomacy bonuses

### Modifier

* `eotg_corporation_perfect_executive`

---

## Event: Executive Civil War

### Trigger

* failed succession
* severe board division

### Description

Corporate divisions openly wage war.

### Outcomes

#### Crush Rival Executives

* war bonuses

#### Negotiate Division

* realm split possibility

#### Escape With Loyal Assets

* exile-style survival chain

---

## Event: The Corporation Becomes a Machine

### Trigger

* long stable reign

### Description

The corporation grows cold, efficient, and impersonal.

### Outcomes

#### Embrace Efficiency

* economic bonuses

#### Preserve Human Relationships

* diplomacy bonuses

#### Exploit Workers Harder

* profit gain
* unrest growth

# Corporation Government Event Design Document

## Phase 2 — Advanced Executive Intrigue, Information Warfare, and Corporate Control Systems

### Purpose: Expand sabotage ecosystems, executive paranoia, hostile acquisitions, and authoritarian corporate evolution

---

# EVENT CATEGORY — INFORMATION WARFARE

This government should weaponize information constantly.

---

## Event: A Director Leaks Confidential Data

### Trigger

* rival executive
* active intrigue schemes

### Description

Confidential internal documents appear on public networks.

### Outcomes

#### Trace the Leak

* intrigue challenge

#### Fabricate a Different Culprit

* redirect scandal

#### Use the Leak Against Rivals

* legitimacy damage to target

### Modifiers

* `eotg_corporation_data_breach`

---

## Event: Internal Surveillance Expansion

### Trigger

* paranoid ruler
* high intrigue focus

### Description

Executives propose expanding employee surveillance systems.

### Outcomes

#### Approve Full Surveillance

* scheme resistance increase
* legitimacy penalty

#### Limited Monitoring

* moderate bonuses

#### Reject the Proposal

* liberty-minded opinion gain

---

## Event: False Information Campaign

### Trigger

* active rivalry

### Description

Executives spread false narratives about competitors.

### Outcomes

#### Massive Disinformation Push

* target legitimacy damage

#### Subtle Rumor Campaign

* intrigue bonus

#### Forge Documents

* high risk/high reward

---

# EVENT CATEGORY — EXECUTIVE PARANOIA

---

## Event: Nobody Trusts the Board

### Trigger

* multiple rivalries
* exposed conspiracies

### Description

Executives suspect everyone around them.

### Outcomes

#### Encourage Internal Competition

* intrigue growth

#### Attempt Reconciliation

* diplomacy challenge

#### Purge Potential Rivals

* dread increase

---

## Event: Security Audit Finds Irregularities

### Trigger

* corruption high

### Description

Internal audits uncover suspicious executive behavior.

### Outcomes

#### Launch Investigations

* intrigue chain

#### Bury the Findings

* corruption increase

#### Use Findings for Blackmail

* hooks gained

---

## Event: An Executive Disappears

### Trigger

* failed intrigue schemes

### Description

A major executive vanishes without explanation.

### Outcomes

#### Investigate Thoroughly

* reveal conspiracy chance

#### Quietly Replace Them

* stability preserved

#### Exploit the Fear

* dread gain

---

# EVENT CATEGORY — HOSTILE ACQUISITION ESCALATION

---

## Event: Proxy Acquisition Attempt

### Trigger

* acquisition plans active

### Description

Executives secretly acquire influence within rival structures.

### Outcomes

#### Bribe Rival Directors

* acquisition progress

#### Manipulate Shareholders

* intrigue challenge

#### Sabotage Their Economy First

* target instability

---

## Event: Rival Corporation Resists Buyout

### Trigger

* failed acquisition

### Description

A rival corporation publicly resists takeover attempts.

### Outcomes

#### Escalate Economic Pressure

* economic warfare modifier

#### Offer Better Terms

* diplomacy challenge

#### Destroy Their Reputation

* PR attack chain

---

## Event: Absorbing Rival Assets

### Trigger

* successful acquisition

### Description

The corporation absorbs rival infrastructure and staff.

### Outcomes

#### Integrate Everything Quickly

* instability risk

#### Gradual Integration

* slower bonuses

#### Purge Rival Leadership

* dread gain

---

# EVENT CATEGORY — CORPORATE AUTHORITARIANISM

This government should slowly drift toward dystopian control.

---

## Event: Employees Fear the Corporation

### Trigger

* high dread
* surveillance active

### Description

Workers and lower executives live in fear.

### Outcomes

#### Encourage Fear

* productivity bonus
* legitimacy loss

#### Ease Restrictions

* reduced unrest

#### Use Fear Selectively

* mixed effects

### Modifiers

* `eotg_corporation_fear_state`

---

## Event: Executive Loyalty Oaths

### Trigger

* unstable board

### Description

Executives are ordered to publicly swear loyalty.

### Outcomes

#### Mandatory Oaths

* authority gain
* resentment increase

#### Voluntary Ceremony

* diplomacy gain

#### Secret Loyalty Testing

* intrigue bonus

---

## Event: The Corporation Controls the Media

### Trigger

* powerful realm
* high intrigue

### Description

Media networks become extensions of corporate propaganda.

### Outcomes

#### Full Narrative Control

* legitimacy manipulation

#### Controlled Press Partnerships

* softer influence

#### Weaponize Fear Campaigns

* dread gain

---

# EVENT CATEGORY — EXECUTIVE CLASS DECADENCE

---

## Event: Executive Luxury Excess

### Trigger

* prosperous corporation
* low public approval

### Description

Executives indulge in absurd luxury while workers struggle.

### Outcomes

#### Celebrate Wealth Publicly

* elite loyalty gain
* unrest increase

#### Hide the Excess

* intrigue challenge

#### Public Philanthropy Campaign

* legitimacy gain

---

## Event: Corporate Narcotics Culture

### Trigger

* decadent elite culture

### Description

Executives rely on stimulants and designer narcotics.

### Outcomes

#### Ignore the Problem

* productivity bonus
* health risks

#### Crack Down

* elite anger

#### Profit from the Trade

* gold gain

---

## Event: Detached Executive Leadership

### Trigger

* extremely large corporation

### Description

Leadership becomes isolated from ordinary citizens and workers.

### Outcomes

#### Maintain Distance

* efficiency gain
* legitimacy loss

#### Public Outreach Campaign

* legitimacy gain

#### Manipulate Public Perception

* intrigue bonus

---

# EVENT CATEGORY — INTERNAL DIVISIONAL WARFARE

---

## Event: Departments Sabotage Each Other

### Trigger

* rival executive divisions

### Description

Corporate divisions undermine each other’s operations.

### Outcomes

#### Punish Everyone

* authority gain

#### Encourage Competition

* productivity gain
* instability increase

#### Secretly Favor One Side

* faction shifts

---

## Event: A Regional Director Goes Rogue

### Trigger

* weak central authority

### Description

A Regional Director ignores executive orders entirely.

### Outcomes

#### Remove Them

* rebellion risk

#### Negotiate Autonomy

* weaker authority

#### Use Assassins

* intrigue chain

---

## Event: Internal Corporate Spy Ring

### Trigger

* paranoia high

### Description

Executives discover widespread espionage inside the corporation.

### Outcomes

#### Expand Counterintelligence

* scheme defense increase

#### Turn Spies Into Double Agents

* intrigue opportunities

#### Publicly Reveal the Ring

* instability increase

---

# EVENT CATEGORY — SUCCESSION CHAOS

Unlike Gob-Corp elections, this is colder and more manipulative.

---

## Event: Executive Succession War Begins

### Trigger

* weak succession
* multiple ambitious candidates

### Description

Executives begin covert warfare for control of the corporation.

### Outcomes

#### Support a Candidate Publicly

* alliance shift

#### Secretly Manipulate Everyone

* intrigue gain

#### Prepare for Violence

* military readiness modifier

---

## Event: Vote Manipulation Network

### Trigger

* succession cycle

### Description

Executives create networks to manipulate board votes.

### Outcomes

#### Buy Directors

* gold cost

#### Blackmail Executives

* hooks gained

#### Forge Corporate Records

* intrigue risk

---

## Event: The Board Splits Completely

### Trigger

* failed succession stabilization

### Description

The executive board fractures into hostile blocs.

### Outcomes

#### Force Unity

* dread increase

#### Negotiate Division

* possible peaceful split

#### Prepare for Corporate War

* military bonuses

---

# EVENT CATEGORY — ECONOMIC COLLAPSE & CONTROL

---

## Event: The Numbers Were False

### Trigger

* corruption high
* economic downturn

### Description

Financial reports were manipulated for years.

### Outcomes

#### Reveal the Truth

* legitimacy damage
* future recovery bonus

#### Continue the Lie

* temporary stability

#### Blame Executives Below You

* scapegoat modifier

---

## Event: Automated Systems Fail

### Trigger

* overreliance on automation

### Description

Critical automated infrastructure malfunctions catastrophically.

### Outcomes

#### Emergency Repairs

* gold cost

#### Shift Blame to Engineers

* legitimacy risk

#### Replace Human Staff Entirely

* productivity modifier

---

## Event: Investor Revolt

### Trigger

* repeated failures

### Description

Major investors demand executive restructuring.

### Outcomes

#### Accept Oversight

* reduced authority

#### Resist Investor Pressure

* no confidence escalation

#### Manipulate Investor Reports

* intrigue challenge

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: The Invisible CEO

### Trigger

* intrigue-focused successful ruler

### Description

The CEO rarely appears publicly, ruling entirely through networks and intermediaries.

### Outcomes

#### Embrace the Mystery

* intrigue gain

#### Return to Public Leadership

* legitimacy gain

#### Weaponize Uncertainty

* dread gain

### Modifier

* `eotg_corporation_shadow_ceo`

---

## Event: Corporate State Ascendant

### Trigger

* massive successful realm

### Description

The corporation becomes more powerful than governments themselves.

### Outcomes

#### Fully Corporate Society

* economic bonuses
* liberty penalties

#### Maintain Corporate Balance

* stability gain

#### Militarize Corporate Authority

* authoritarian modifiers

---

## Event: Humanity as a Product

### Trigger

* extreme dystopian development

### Description

Executives begin openly treating citizens purely as economic assets.

### Outcomes

#### Maximize Efficiency

* massive productivity gains
* legitimacy collapse risk

#### Preserve Public Morale

* softer bonuses

#### Create Synthetic Consumer Culture

* hybrid modifiers

# Corporation Government Event Design Document

## Phase 3 — Decision Chains, Corporate Emergency Systems, and Endgame Executive Control

### Purpose: Create active strategic gameplay loops for corporate rulers and support authoritarian megacorporation evolution

---

# DECISION CHAIN — LAUNCH SABOTAGE OPERATION

## Decision: `eotg_corporation_launch_sabotage`

### Requirements

* target rival exists
* intrigue threshold met
* sufficient operational funds

### Immediate Effects

* begins sabotage operation chain
* target receives hidden destabilization modifier

---

## Event: Corporate Operatives Deployed

### Description

Special operatives infiltrate rival infrastructure and executive circles.

### Outcomes

#### Target Financial Systems

* economic damage to rival

#### Target Public Reputation

* legitimacy damage

#### Target Internal Leadership

* assassination/scheme bonuses

### Modifiers

* `eotg_corporation_active_sabotage`

---

## Event: Sabotage Escalates

### Trigger

* successful sabotage progress

### Description

The operation begins seriously destabilizing the target.

### Outcomes

#### Push Further

* stronger damage
* exposure risk increases

#### Maintain Current Pressure

* stable moderate damage

#### Pull Back Quietly

* preserve secrecy

---

## Event: Operatives Exposed

### Trigger

* failed sabotage secrecy

### Description

Evidence links the corporation to covert attacks.

### Outcomes

#### Deny Involvement

* intrigue challenge

#### Sacrifice the Operatives

* legitimacy preservation

#### Threaten Retaliation

* dread gain

---

# DECISION CHAIN — HOSTILE ACQUISITION CAMPAIGN

## Decision: `eotg_corporation_hostile_acquisition`

### Requirements

* wealthy corporation
* weaker target exists

### Immediate Effects

* acquisition pressure modifier on target

---

## Event: Acquisition Teams Mobilized

### Description

Corporate negotiators and agents pressure the target corporation.

### Outcomes

#### Aggressive Buyout Strategy

* faster acquisition progress
* instability risk

#### Gradual Economic Pressure

* slower but safer progress

#### Secretly Destabilize the Target

* sabotage synergy bonus

---

## Event: Rival Shareholders Resist

### Trigger

* target resistance high

### Description

Investors resist the acquisition effort.

### Outcomes

#### Increase the Offer

* gold cost

#### Blackmail Shareholders

* intrigue challenge

#### Threaten Economic Ruin

* dread increase

---

## Event: Corporate Absorption Complete

### Trigger

* successful acquisition

### Description

The rival corporation is fully absorbed.

### Outcomes

#### Integrate Their Leadership

* stability bonus

#### Purge Their Executives

* dread gain

#### Strip Their Assets

* massive gold gain
* instability risk

### Modifiers

* `eotg_corporation_absorbed_competitor`

---

# DECISION CHAIN — CORPORATE MEDIA CAMPAIGN

## Decision: `eotg_corporation_media_campaign`

### Requirements

* legitimacy problems OR upcoming succession/election

### Immediate Effects

* starts PR manipulation chain

---

## Event: Narrative Engineering Begins

### Description

Corporate media divisions begin reshaping public perception.

### Outcomes

#### Promote Corporate Unity

* legitimacy gain

#### Smear Rivals

* target legitimacy damage

#### Manufacture Fear

* dread increase

### Modifiers

* `eotg_corporation_media_control`

---

## Event: Investigative Journalists Dig Deeper

### Trigger

* aggressive propaganda used

### Description

Independent reporters investigate suspicious narratives.

### Outcomes

#### Silence the Journalists

* intrigue challenge

#### Buy Their Loyalty

* gold cost

#### Publicly Debate Them

* diplomacy challenge

---

## Event: Propaganda Backfires

### Trigger

* failed campaign

### Description

The public reacts negatively to manipulative messaging.

### Outcomes

#### Double Down

* short-term recovery
* future legitimacy risk

#### Admit Mistakes

* modest legitimacy recovery

#### Blame Rogue Executives

* scapegoat modifier

---

# DECISION CHAIN — EXECUTIVE PURGE

## Decision: `eotg_corporation_executive_purge`

### Requirements

* active conspiracies OR low board loyalty
* high dread OR intrigue

### Immediate Effects

* begins purge chain

---

## Event: Executives Summoned for Review

### Description

Executives are interrogated regarding loyalty and competence.

### Outcomes

#### Remove Suspected Rivals

* faction suppression

#### Quietly Blackmail Them

* hooks gained

#### Public Trials

* dread gain
* legitimacy risk

### Modifiers

* `eotg_corporation_internal_purge`

---

## Event: Fear Sweeps the Corporation

### Trigger

* purge active

### Description

Executives fear becoming the next target.

### Outcomes

#### Encourage Fear

* authority gain

#### Offer Protection to Loyalists

* faction loyalty increase

#### Expand Surveillance Further

* scheme defense gain

---

## Event: Purge Creates Power Vacuum

### Trigger

* purge too large

### Description

Too many executives were removed too quickly.

### Outcomes

#### Promote Loyal Incompetents

* stability penalty

#### Recruit New Talent

* gold cost

#### Centralize Authority Personally

* stress gain
* authority gain

---

# DECISION CHAIN — DECLARE CORPORATE SECURITY EMERGENCY

Emergency anti-collapse system.

---

## Decision: `eotg_corporation_security_emergency`

### Requirements

* multiple active threats
* severe instability

### Immediate Effects

* emergency powers activated

---

## Event: Security Forces Deployed Everywhere

### Description

Corporate security floods streets, factories, and executive districts.

### Outcomes

#### Total Security State

* revolt suppression
* legitimacy damage

#### Temporary Emergency

* moderate stabilization

#### Quiet Operations Only

* intrigue bonuses

### Modifiers

* `eotg_corporation_security_lockdown`

---

## Event: Executives Fear Dictatorship

### Trigger

* emergency active

### Description

Board members fear the CEO seeks permanent emergency powers.

### Outcomes

#### Promise Restoration of Normalcy

* legitimacy gain

#### Threaten the Board

* dread gain

#### Arrest Dissidents

* faction escalation risk

---

# DECISION CHAIN — AUTOMATE THE WORKFORCE

Dystopian economic optimization chain.

---

## Decision: `eotg_corporation_automate_workforce`

### Requirements

* advanced economy
* sufficient wealth

### Immediate Effects

* productivity increase
* worker unrest risk

---

## Event: Massive Automation Initiative

### Description

Machines replace enormous numbers of workers.

### Outcomes

#### Full Automation

* huge tax bonus
* unrest increase

#### Partial Automation

* balanced modifiers

#### Human Oversight Programs

* softer bonuses

### Modifiers

* `eotg_corporation_mass_automation`

---

## Event: Displaced Workers Organize

### Trigger

* automation unrest

### Description

Former workers organize resistance movements.

### Outcomes

#### Suppress Organizers

* dread gain

#### Offer Minimal Compensation

* gold cost

#### Ignore Them

* revolt risk

---

## Event: Machines Begin Replacing Executives

### Trigger

* extreme automation path

### Description

Some propose algorithmic governance systems.

### Outcomes

#### Trust the Algorithms

* efficiency bonuses
* diplomacy penalties

#### Maintain Human Leadership

* legitimacy gain

#### Hybrid Executive Systems

* balanced modifiers

---

# DECISION CHAIN — ENGINEER EXECUTIVE SUCCESSION

## Decision: `eotg_corporation_engineer_succession`

### Requirements

* aging CEO
* succession instability possible

### Immediate Effects

* succession manipulation modifier

---

## Event: The Preferred Candidate

### Description

Executives begin backing the CEO’s chosen successor.

### Outcomes

#### Public Support Campaign

* legitimacy bonus

#### Secret Vote Manipulation

* intrigue gain

#### Threaten Opposition Directors

* dread gain

---

## Event: Rival Candidates Fight Dirty

### Trigger

* active succession struggle

### Description

Candidates sabotage each other relentlessly.

### Outcomes

#### Encourage Competition

* instability increase

#### Force Unity

* authority challenge

#### Secretly Manipulate Everyone

* intrigue bonuses

---

## Event: The Succession Crisis Explodes

### Trigger

* failed succession stabilization

### Description

The corporation fractures during the transition of power.

### Outcomes

#### Emergency Executive Rule

* temporary authority

#### Negotiate Division of Assets

* peaceful split option

#### Executive Civil War

* open conflict

---

# DECISION CHAIN — BECOME A CORPORATE STATE

Endgame transformation path.

---

## Decision: `eotg_corporation_become_corporate_state`

### Requirements

* enormous realm
* high legitimacy
* strong security apparatus

### Immediate Effects

* transition chain begins

---

## Event: Government and Corporation Become One

### Description

Corporate authority fully replaces traditional governance.

### Outcomes

#### Total Corporate Rule

* authoritarian bonuses

#### Managed Corporate Citizenship

* stability focus

#### Profit Above All

* extreme economic bonuses
* unrest risks

### Modifiers

* `eotg_corporation_corporate_state`

---

## Event: Citizens Become Consumers

### Trigger

* transformation completed

### Description

The line between citizen and customer disappears entirely.

### Outcomes

#### Fully Embrace Consumer Society

* economic bonuses

#### Preserve Civic Structures

* legitimacy gain

#### Weaponize Consumer Dependency

* control bonuses

---

# FINAL DESIGN NOTE

Corporation Government now supports:

* executive sabotage gameplay
* hostile acquisitions
* propaganda warfare
* board manipulation
* executive purges
* surveillance states
* automated dystopian economics
* succession manipulation
* corporate authoritarianism
* megacorporation transformation systems

This creates a fully distinct gameplay identity from Gob-Corp:

| Gob-Corp                | Corporation                 |
| ----------------------- | --------------------------- |
| chaotic oligarchs       | cold technocratic predators |
| unstable trade combines | disciplined megacorps       |
| loud corruption         | hidden corruption           |
| open board conflict     | covert executive warfare    |
| industrial chaos        | controlled dystopia         |
| factional instability   | paranoid authoritarianism   |

# Cartel Government Event Design Document

## Phase 1 — Functional + Core Flavor Events

### Target: ~50 Events for Beta Functionality

### Purpose: Establish criminal empire gameplay, fear-based loyalty, brutal enforcement, and unstable underworld politics

Government Reference: `eotg_cartel_government` 

---

# CORE GOVERNMENT FANTASY

Cartel Governments are criminal states masquerading as legitimate powers.

They survive through:

* fear
* extortion
* smuggling
* intimidation
* assassinations
* personal loyalty networks

Unlike Fringe governments:

* Cartels are more organized
* more economically focused
* more politically manipulative

Unlike Corporations:

* Cartels rely on fear and criminal influence
* not public legitimacy

Core gameplay loop:

1. expand criminal influence
2. maintain loyalty through fear and rewards
3. suppress rivals brutally
4. dominate smuggling routes
5. prevent betrayals
6. survive internal gang wars

---

# EVENT CATEGORY — FEAR & LOYALTY

This is the defining mechanic ecosystem.

---

## Event: Loyalty Bought with Blood

### Trigger

* recently crushed rebellion
* high dread ruler

### Description

Subordinates become loyal after witnessing brutal punishment.

### Outcomes

#### Publicly Display the Bodies

* dread gain
* loyalty increase
* diplomacy penalties

#### Quiet Executions

* moderate fear gain

#### Spare One Survivor

* legitimacy gain among softer characters

### Modifiers

* `eotg_cartel_rule_of_fear`

---

## Event: Fear Turns Into Hatred

### Trigger

* extremely high dread

### Description

Subordinates obey, but secretly dream of betrayal.

### Outcomes

#### Increase Security

* gold upkeep increase

#### Purge Suspected Traitors

* faction suppression
* tyranny gain

#### Ignore the Tension

* assassination risk increase

---

## Event: A Lieutenant Demands Respect

### Trigger

* powerful vassal
* low opinion

### Description

A lieutenant feels underappreciated and insulted.

### Outcomes

#### Reward Them

* loyalty increase

#### Threaten Them

* dread gain
* rebellion risk

#### Humiliate Them Publicly

* rivalry created

---

# EVENT CATEGORY — SMUGGLING NETWORKS

---

## Event: Smuggling Route Discovered

### Trigger

* successful trade operation

### Description

A lucrative illegal trade route is uncovered.

### Outcomes

#### Exploit It Aggressively

* gold gain
* exposure risk

#### Keep It Secret

* smaller safer profits

#### Share Profits with Lieutenants

* loyalty increase

### Modifiers

* `eotg_cartel_smuggling_network`

---

## Event: Authorities Interfere with Smuggling

### Trigger

* rival government pressure

### Description

Local authorities attempt to disrupt operations.

### Outcomes

#### Bribe Officials

* gold cost

#### Assassinate the Investigators

* dread gain
* exposure risk

#### Relocate Operations

* temporary losses

---

## Event: Smugglers Skim Profits

### Trigger

* corrupt subordinates

### Description

Smugglers secretly steal from cartel profits.

### Outcomes

#### Brutal Punishment

* dread gain

#### Quiet Blackmail

* hook gain

#### Ignore Minor Theft

* small loyalty gain

---

# EVENT CATEGORY — CARTEL INTERNAL POLITICS

---

## Event: Rival Crews Clash

### Trigger

* rival vassals

### Description

Two criminal crews fight over territory and profits.

### Outcomes

#### Back One Crew

* loyalty shift

#### Force Peace

* diplomacy challenge

#### Let Them Kill Each Other

* reduced rival strength

---

## Event: A Lieutenant Builds Private Armies

### Trigger

* powerful lieutenant
* weak ruler

### Description

A subordinate secretly builds independent forces.

### Outcomes

#### Demand Disarmament

* rebellion risk

#### Allow It for Now

* future danger modifier

#### Secretly Sabotage Them

* intrigue opportunity

---

## Event: Informants Spread Through the Cartel

### Trigger

* instability
* rival governments nearby

### Description

Rumors spread that informants infiltrate operations.

### Outcomes

#### Launch Internal Investigation

* intrigue challenge

#### Torture Suspects

* dread gain

#### Ignore the Rumors

* future betrayal risk

---

# EVENT CATEGORY — CRIMINAL OPERATIONS

---

## Event: Protection Racket Expands

### Trigger

* prosperous territory

### Description

Businesses are forced to pay for “protection.”

### Outcomes

#### Expand Aggressively

* gold gain
* unrest increase

#### Keep Demands Moderate

* stable income

#### Use Violence Selectively

* dread increase

### Modifiers

* `eotg_cartel_protection_racket`

---

## Event: Illegal Trade Boom

### Trigger

* successful criminal economy

### Description

Illegal trade floods cartel markets.

### Outcomes

#### Flood the Market

* huge gold gain
* instability risk

#### Control Distribution

* stable profits

#### Restrict Supply for Higher Prices

* intrigue economy bonus

---

## Event: A Drug Operation Goes Wrong

### Trigger

* illegal production chains

### Description

A dangerous shipment causes deaths and chaos.

### Outcomes

#### Cover It Up

* intrigue challenge

#### Eliminate Witnesses

* dread gain

#### Blame Rivals

* rivalry escalation

---

# EVENT CATEGORY — ENFORCEMENT & VIOLENCE

---

## Event: Public Execution in the Streets

### Trigger

* betrayal punished

### Description

A traitor is executed publicly as a warning.

### Outcomes

#### Brutal Display

* major dread gain

#### Quick Execution

* moderate fear gain

#### Spare Them Publicly

* legitimacy gain
* weakness perception

---

## Event: Enforcers Become Too Violent

### Trigger

* high dread
* brutal ruler

### Description

Cartel enforcers terrorize civilians excessively.

### Outcomes

#### Encourage Terror

* control gain
* legitimacy loss

#### Restrain the Enforcers

* loyalty penalty

#### Secretly Profit from Chaos

* corruption gain

---

## Event: Assassins Request Approval

### Trigger

* intrigue ruler

### Description

Professional killers request permission for high-profile assassinations.

### Outcomes

#### Approve the Hit

* target removal chance

#### Delay the Operation

* intrigue modifier

#### Reject the Assassination

* diplomacy gain

---

# EVENT CATEGORY — SUCCESSION & BETRAYAL

Cartels should suffer dangerous transitions.

---

## Event: Lieutenants Prepare for Succession

### Trigger

* aging ruler

### Description

Subordinates begin preparing for power struggles.

### Outcomes

#### Name a Successor

* succession influence

#### Encourage Competition

* stronger future ruler
* instability increase

#### Secretly Eliminate Rivals

* intrigue opportunities

---

## Event: The Boss Is Dead

### Trigger

* ruler death

### Description

The cartel leadership fractures after the ruler’s death.

### Outcomes

#### Rally Loyalists

* military advantage

#### Negotiate Power Sharing

* temporary stability

#### Begin Purges Immediately

* dread gain
* civil war risk

---

## Event: Betrayal at the Funeral

### Trigger

* succession instability

### Description

Violence erupts during funeral ceremonies.

### Outcomes

#### Fight Immediately

* combat chain

#### Escape the Ambush

* survival event

#### Negotiate Temporary Peace

* unstable truce modifier

---

# EVENT CATEGORY — UNDERWORLD CULTURE

---

## Event: Criminal Legends Spread

### Trigger

* successful long reign

### Description

Stories spread of the ruler’s brutality and cunning.

### Outcomes

#### Encourage the Myth

* dread gain

#### Build a Public Persona

* legitimacy gain

#### Remain Hidden

* intrigue bonuses

---

## Event: Feast of the Underworld

### Trigger

* prosperous criminal operations

### Description

Lieutenants gather for lavish criminal celebrations.

### Outcomes

#### Reward Loyal Lieutenants

* loyalty increase

#### Conduct Secret Deals

* hooks gained

#### Show Excessive Wealth

* unrest increase

---

## Event: Children Raised in Crime

### Trigger

* criminal dynasty

### Description

Young heirs grow up surrounded by cartel violence.

### Outcomes

#### Teach Ruthlessness

* cruel traits possible

#### Teach Leadership

* diplomacy/martial bonuses

#### Shield Them from Violence

* compassionate traits possible

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: The Untouchable Boss

### Trigger

* long successful reign
* many failed assassination attempts

### Description

The ruler gains a legendary reputation for surviving everything.

### Outcomes

#### Embrace the Fear

* dread gain

#### Build a Public Legend

* prestige gain

#### Rule from the Shadows

* intrigue bonuses

### Modifier

* `eotg_cartel_untouchable`

---

## Event: Cartel War Erupts

### Trigger

* major faction conflict

### Description

Multiple crews and lieutenants openly wage war.

### Outcomes

#### Crush the Rivals

* war bonuses

#### Negotiate Territories

* temporary peace

#### Flee and Rebuild

* exile-style survival chain

---

## Event: The Underworld Remembers

### Trigger

* famous ruler death

### Description

Criminals across the galaxy speak of the ruler’s reign.

### Outcomes

#### Fearful Legacy

* dynasty dread modifier

#### Respected Legacy

* prestige gain

#### Bloody Legacy

* successor instability modifier
# Cartel Government Event Design Document

## Phase 2 — Criminal Empire Expansion, Internal Betrayals, and Underworld Control Systems

### Purpose: Expand cartel ecosystem into a living criminal underworld full of paranoia, gang wars, corruption, and shadow economies

---

# EVENT CATEGORY — GANG WARFARE

---

## Event: Territory Dispute Escalates

### Trigger

* rival lieutenants
* overlapping profitable territories

### Description

Two crews violently contest control of profitable districts.

### Outcomes

#### Support One Side

* chosen lieutenant loyalty gain
* rival hatred increases

#### Force a Settlement

* diplomacy challenge

#### Let the Violence Continue

* both weakened
* unrest increase

### Modifiers

* `eotg_cartel_turf_war`

---

## Event: Street War Engulfs the District

### Trigger

* unresolved gang conflict

### Description

Violence spreads through civilian areas as crews fight openly.

### Outcomes

#### Deploy Enforcers

* control restored
* dread gain

#### Allow the Bloodshed

* rival weakening
* development damage

#### Secretly Arm One Side

* intrigue advantage

---

## Event: A Crew Refuses Tribute

### Trigger

* weak ruler
* powerful lieutenant

### Description

A crew openly refuses to pay its expected tribute.

### Outcomes

#### Crush Them Publicly

* rebellion risk
* dread gain

#### Negotiate New Terms

* reduced income
* temporary peace

#### Secretly Assassinate Their Leader

* intrigue chain

---

# EVENT CATEGORY — BETRAYAL & INFORMANTS

---

## Event: An Informant Is Found

### Trigger

* paranoia events
* failed secrecy

### Description

A suspected informant is captured by cartel enforcers.

### Outcomes

#### Torture Them Publicly

* dread gain

#### Interrogate Quietly

* intrigue information chance

#### Kill Them Immediately

* fear increase
* lost intelligence opportunity

---

## Event: False Informant Accusation

### Trigger

* paranoid ruler

### Description

An innocent lieutenant is accused of betrayal.

### Outcomes

#### Execute Them Anyway

* dread gain
* loyalty fear increase

#### Investigate Carefully

* intrigue challenge

#### Publicly Apologize

* legitimacy gain
* weakness perception

---

## Event: Double Agent Within the Cartel

### Trigger

* active rival realm
* intrigue failure risk

### Description

A trusted operative secretly works for enemies.

### Outcomes

#### Feed Them False Information

* counter-intrigue bonus

#### Eliminate Them Quietly

* secrecy preserved

#### Turn Them Into Triple Agent

* high-risk intrigue chain

---

# EVENT CATEGORY — SHADOW ECONOMY

---

## Event: Black Market Boom

### Trigger

* strong criminal economy

### Description

Illegal markets explode in profitability.

### Outcomes

#### Expand Operations

* gold gain
* instability increase

#### Centralize Control

* stable profits

#### Let Lieutenants Compete

* faction rivalry increase

### Modifiers

* `eotg_cartel_black_market_expansion`

---

## Event: Counterfeit Goods Flood the Market

### Trigger

* corrupt operations

### Description

Fake products undermine cartel operations.

### Outcomes

#### Crack Down Hard

* gold cost
* legitimacy gain

#### Secretly Profit from Counterfeits

* gold gain

#### Blame Rivals

* rivalry escalation

---

## Event: Smuggling Empire Expands Too Fast

### Trigger

* large criminal network

### Description

Rapid expansion creates organizational chaos.

### Outcomes

#### Appoint Regional Smuggling Bosses

* decentralization

#### Centralize Operations

* unrest increase

#### Allow Informal Expansion

* corruption growth

---

# EVENT CATEGORY — ENFORCER SYSTEMS

---

## Event: Enforcer Captain Gains Fame

### Trigger

* successful suppression actions

### Description

A feared enforcer becomes famous throughout the underworld.

### Outcomes

#### Promote Them

* stronger enforcement bonuses
* future coup risk

#### Keep Them Controlled

* loyalty penalty

#### Use Them Against Rivals

* intrigue bonus

### Modifiers

* `eotg_cartel_feared_enforcer`

---

## Event: Enforcers Demand More Freedom

### Trigger

* strong security faction

### Description

Cartel enforcers demand autonomy to handle threats “properly.”

### Outcomes

#### Grant Expanded Authority

* control bonuses
* legitimacy loss

#### Restrict Their Actions

* enforcer anger

#### Secretly Encourage Brutality

* dread increase

---

## Event: Rogue Enforcers

### Trigger

* weak oversight

### Description

Enforcers abuse power for personal profit.

### Outcomes

#### Punish Them

* legitimacy gain

#### Ignore It

* corruption increase

#### Profit Alongside Them

* gold gain

---

# EVENT CATEGORY — CARTEL FAMILY DYNASTIES

---

## Event: Family Rivalry Intensifies

### Trigger

* powerful dynasties

### Description

Two cartel bloodlines deepen their hatred.

### Outcomes

#### Mediate Peace

* diplomacy challenge

#### Support One Family

* faction shift

#### Secretly Escalate the Conflict

* weakened rivals

---

## Event: Marriage Between Crime Families

### Trigger

* alliance opportunity

### Description

A marriage could unite rival criminal dynasties.

### Outcomes

#### Approve the Marriage

* alliance gain

#### Sabotage the Union

* rivalry continues

#### Use Marriage for Manipulation

* intrigue bonus

---

## Event: The Heir Is Too Soft

### Trigger

* compassionate heir
* brutal cartel culture

### Description

Lieutenants doubt the heir’s ability to rule through fear.

### Outcomes

#### Harden the Heir

* cruel trait chance

#### Defend Their Compassion

* legitimacy gain

#### Replace the Heir Quietly

* succession instability risk

---

# EVENT CATEGORY — POLITICAL CORRUPTION

Cartels should infect surrounding governments.

---

## Event: Officials Accept Bribes

### Trigger

* strong corruption network

### Description

Government officials secretly work for the cartel.

### Outcomes

#### Expand the Corruption

* influence gain

#### Blackmail the Officials

* hooks gained

#### Eliminate Loose Ends

* intrigue gain

---

## Event: Politician Threatens the Cartel

### Trigger

* anti-cartel neighboring ruler

### Description

A politician publicly promises to destroy cartel influence.

### Outcomes

#### Assassinate Them

* intrigue chain

#### Bribe Them

* gold cost

#### Public Intimidation Campaign

* dread increase

---

## Event: Cartel Influence Reaches the Courts

### Trigger

* long corruption campaign

### Description

Judges and legal systems become compromised.

### Outcomes

#### Fully Corrupt the Courts

* crime suppression reduction

#### Use Selective Corruption

* balanced bonuses

#### Hide the Corruption Carefully

* intrigue gain

---

# EVENT CATEGORY — NARCOTICS & VICE ECONOMIES

---

## Event: New Designer Drug Emerges

### Trigger

* criminal innovation

### Description

A highly addictive narcotic floods the streets.

### Outcomes

#### Mass Distribution

* huge gold gain
* instability increase

#### Controlled Distribution

* stable profits

#### Restrict the Trade

* legitimacy gain

### Modifiers

* `eotg_cartel_drug_epidemic`

---

## Event: Addiction Crisis

### Trigger

* prolonged narcotics trade

### Description

Communities collapse under addiction and crime.

### Outcomes

#### Ignore the Crisis

* continued profits

#### Fund Recovery Programs

* legitimacy gain

#### Exploit the Addiction

* stronger control modifier

---

## Event: Rival Cartels Poison Supply Chains

### Trigger

* cartel rivalry

### Description

Contaminated narcotics spread panic.

### Outcomes

#### Retaliate Brutally

* rivalry escalation

#### Quietly Recall Product

* gold loss

#### Blame Competitors Publicly

* propaganda effect

---

# EVENT CATEGORY — INTERNAL PARANOIA

---

## Event: Nobody Sleeps Safely

### Trigger

* extreme paranoia
* many rivals

### Description

Fear and betrayal infect every level of leadership.

### Outcomes

#### Increase Personal Security

* gold upkeep

#### Trust Nobody

* intrigue gain
* diplomacy loss

#### Hold Loyalty Gatherings

* temporary unity

---

## Event: The Boss Sees Betrayal Everywhere

### Trigger

* paranoid trait
* assassination attempts

### Description

The ruler suspects everyone.

### Outcomes

#### Launch Purges

* faction suppression

#### Withdraw into Isolation

* diplomacy penalties

#### Use Fear Strategically

* intrigue gain

---

## Event: Trusted Lieutenant Vanishes

### Trigger

* intrigue-heavy environment

### Description

A loyal subordinate disappears mysteriously.

### Outcomes

#### Investigate Aggressively

* intrigue chain

#### Replace Them Immediately

* stability preserved

#### Blame Rivals

* war justification

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: The Criminal Empire Peaks

### Trigger

* massive cartel realm
* extremely wealthy ruler

### Description

The cartel dominates trade, crime, and fear across entire sectors.

### Outcomes

#### Rule Through Terror

* dread bonuses

#### Rule Through Wealth

* economic bonuses

#### Attempt Legitimization

* reform path unlock

### Modifier

* `eotg_cartel_empire_of_crime`

---

## Event: The Great Betrayal

### Trigger

* low loyalty across multiple lieutenants

### Description

Several trusted lieutenants betray the ruler simultaneously.

### Outcomes

#### Fight for Survival

* civil war bonuses

#### Escape with Loyalists

* exile chain

#### Negotiate Division

* realm fragmentation

---

## Event: The Underworld Never Dies

### Trigger

* cartel collapse

### Description

Even after collapse, criminal networks survive underground.

### Outcomes

#### New Crews Rise

* adventurer criminal factions spawn

#### Crack Down Completely

* expensive suppression effort

#### Secretly Maintain Old Networks

* hidden criminal modifiers
# Cartel Government Event Design Document

## Phase 3 — Decision Chains, Criminal State Evolution, and Endgame Underworld Control

### Purpose: Create active cartel gameplay loops focused on fear, criminal economies, intimidation, and criminal empire management

---

# DECISION CHAIN — EXPAND SMUGGLING NETWORK

## Decision: `eotg_cartel_expand_smuggling`

### Requirements

* active trade routes
* sufficient gold investment
* no recent crackdown failure

### Immediate Effects

* begins smuggling expansion chain
* increased criminal income potential

---

## Event: Smuggling Routes Expand

### Description

Cartel operatives establish new illegal trade corridors.

### Outcomes

#### Aggressive Expansion

* large gold increase
* detection risk rises

#### Careful Expansion

* stable moderate income

#### Let Lieutenants Control Routes

* lieutenant loyalty gain
* decentralization risk

### Modifiers

* `eotg_cartel_expanded_routes`

---

## Event: Border Officials Become Suspicious

### Trigger

* rapid smuggling growth

### Description

Authorities begin noticing unusual cargo movement.

### Outcomes

#### Bribe Officials

* gold cost

#### Assassinate Investigators

* intrigue risk

#### Relocate Smuggling Routes

* temporary losses

---

## Event: Smuggling Network Exposed

### Trigger

* failed secrecy

### Description

Evidence of cartel smuggling operations becomes public.

### Outcomes

#### Destroy the Evidence

* intrigue challenge

#### Silence Witnesses

* dread gain

#### Blame Independent Criminals

* legitimacy mitigation

---

# DECISION CHAIN — ORDER A HIGH-PROFILE HIT

## Decision: `eotg_cartel_order_hit`

### Requirements

* rival exists
* sufficient intrigue or assassin network

### Immediate Effects

* begins assassination chain

---

## Event: Assassins Receive the Contract

### Description

Professional killers prepare to eliminate the target.

### Outcomes

#### Fast and Brutal

* higher success chance
* exposure risk

#### Quiet Elimination

* lower exposure risk

#### Make It a Public Message

* dread gain if successful

### Modifiers

* `eotg_cartel_active_hit`

---

## Event: The Hit Goes Wrong

### Trigger

* failed assassination

### Description

The operation spirals into chaos.

### Outcomes

#### Eliminate Witnesses

* intrigue challenge

#### Blame Rivals

* rivalry escalation

#### Abandon the Operation

* prestige loss

---

## Event: Fear Spreads After the Hit

### Trigger

* successful assassination

### Description

Enemies become terrified after the killing.

### Outcomes

#### Exploit the Fear

* loyalty gain

#### Demand Tribute

* economic pressure bonus

#### Threaten More Targets

* dread increase

---

# DECISION CHAIN — HOLD A FEAST OF LOYALTY

Cartel version of a feast.

---

## Decision: `eotg_cartel_loyalty_feast`

### Requirements

* enough gold
* no active major rebellion

### Immediate Effects

* begins loyalty gathering chain

---

## Event: The Underworld Gathers

### Description

Lieutenants and criminal elites gather in luxury and paranoia.

### Outcomes

#### Reward Loyal Lieutenants

* opinion increases

#### Conduct Secret Negotiations

* hooks gained

#### Display Brutal Power

* dread gain

### Modifiers

* `eotg_cartel_loyalty_feast`

---

## Event: A Lieutenant Insults Another

### Trigger

* rival lieutenants present

### Description

Tensions erupt during the gathering.

### Outcomes

#### Force Peace

* diplomacy challenge

#### Encourage the Rivalry

* future instability

#### Allow a Duel

* injury/death risk

---

## Event: Poisoned Drinks

### Trigger

* many rivals
* intrigue-heavy realm

### Description

Someone attempts murder during the feast.

### Outcomes

#### Investigate Quietly

* intrigue chain

#### Public Executions

* dread gain

#### Blame a Rival Crew

* gang war escalation

---

# DECISION CHAIN — CORRUPT LOCAL AUTHORITIES

## Decision: `eotg_cartel_corrupt_authorities`

### Requirements

* sufficient wealth
* nearby non-cartel rulers or officials

### Immediate Effects

* corruption network expansion

---

## Event: Officials Accept Payment

### Description

Local authorities begin secretly serving cartel interests.

### Outcomes

#### Expand the Corruption Network

* influence gain

#### Blackmail the Officials

* hooks gained

#### Keep Corruption Hidden

* intrigue bonus

### Modifiers

* `eotg_cartel_corrupt_officials`

---

## Event: Honest Officials Resist

### Trigger

* corruption expansion resistance

### Description

Certain officials refuse cartel influence.

### Outcomes

#### Assassinate Them

* dread gain

#### Bribe Them Again

* gold cost

#### Destroy Their Reputation

* intrigue challenge

---

## Event: Anti-Corruption Investigation Begins

### Trigger

* corruption exposed

### Description

Authorities begin investigating cartel influence.

### Outcomes

#### Infiltrate the Investigation

* intrigue opportunity

#### Eliminate Investigators

* exposure risk

#### Temporarily Reduce Operations

* income reduction

---

# DECISION CHAIN — BRUTALIZE A RIVAL CREW

## Decision: `eotg_cartel_brutalize_rivals`

### Requirements

* rival faction exists
* high dread OR martial ruler

### Immediate Effects

* intimidation campaign begins

---

## Event: Cartel Enforcers Strike

### Description

Violence erupts against rival operations.

### Outcomes

#### Maximum Brutality

* dread gain
* escalation risk

#### Precise Elimination

* targeted suppression

#### Send a Warning Instead

* smaller effect
* lower risk

### Modifiers

* `eotg_cartel_terror_campaign`

---

## Event: Civilians Caught in Violence

### Trigger

* brutal tactics used

### Description

Collateral damage spreads fear and outrage.

### Outcomes

#### Ignore the Deaths

* dread gain

#### Pay Compensation

* legitimacy gain
* gold cost

#### Blame Rivals

* propaganda opportunity

---

## Event: Rivals Seek Revenge

### Trigger

* surviving rivals

### Description

Enemies prepare retaliation attacks.

### Outcomes

#### Prepare Ambushes

* military readiness

#### Negotiate Truce

* temporary peace

#### Escalate Further

* major gang war risk

---

# DECISION CHAIN — CONSOLIDATE THE UNDERWORLD

Mid-to-late game stabilization decision.

---

## Decision: `eotg_cartel_consolidate_underworld`

### Requirements

* large cartel realm
* high dread
* strong economy

### Immediate Effects

* criminal authority increase
* lieutenant unrest risk

---

## Event: The Boss Demands Total Loyalty

### Description

The ruler demands complete obedience from all crews.

### Outcomes

#### Rule Through Terror

* authority gain

#### Rule Through Wealth

* loyalty increase

#### Offer Shared Profits

* reduced unrest

### Modifiers

* `eotg_cartel_consolidated_underworld`

---

## Event: Independent Crews Resist Control

### Trigger

* consolidation attempt

### Description

Some criminal groups reject centralization.

### Outcomes

#### Crush Them

* rebellion war

#### Buy Their Loyalty

* gold cost

#### Grant Limited Independence

* weaker authority

---

## Event: The Cartel Becomes an Empire

### Trigger

* successful consolidation

### Description

The cartel evolves into a vast criminal state.

### Outcomes

#### Embrace Criminal Rule

* dread bonuses

#### Seek Legitimacy

* reform opportunities

#### Hide Behind Front Businesses

* intrigue/economic hybrid bonuses

---

# DECISION CHAIN — LEGITIMIZE THE CARTEL

Reformation pathway.

---

## Decision: `eotg_cartel_legitimize_rule`

### Requirements

* stable realm
* high wealth
* reduced instability

### Immediate Effects

* reform chain begins

---

## Event: Public Faces Replace Gang Leaders

### Description

Executives and officials replace open criminals.

### Outcomes

#### Fully Legitimize Operations

* reform progress

#### Maintain Secret Criminal Networks

* hidden bonuses

#### Reject Legitimization

* traditionalist loyalty

---

## Event: Old Enforcers Resist Civilization

### Trigger

* reform progress

### Description

Violent veterans reject attempts to civilize the cartel.

### Outcomes

#### Suppress the Old Guard

* rebellion risk

#### Preserve Criminal Traditions

* hybrid modifiers

#### Abandon Reform

* temporary stability

---

## Event: Birth of a Criminal State

### Trigger

* reform completed

### Description

The cartel transforms into a semi-legitimate power structure.

### Outcomes

#### Corporate Criminal State

* transition path

#### Political Crime Syndicate

* corruption bonuses

#### Hidden Shadow Government

* intrigue bonuses

### Modifiers

* `eotg_cartel_shadow_state`

---

# FINAL DESIGN NOTE

Cartel Government now supports:

* fear-based governance
* gang warfare
* criminal economies
* corruption networks
* assassination systems
* smuggling empires
* underworld politics
* violent succession crises
* cartel consolidation systems
* criminal legitimization reform paths

This creates a strong gameplay distinction:

| Fringe                | Cartel                       |
| --------------------- | ---------------------------- |
| unstable raider chaos | organized criminal hierarchy |
| conquest-driven       | profit-driven                |
| temporary warlords    | entrenched crime bosses      |
| open violence         | strategic intimidation       |
| splinter clans        | criminal families            |
| collapse cycles       | paranoia & betrayal cycles   |

# PMC Government Event Design Document

## Phase 1 — Functional + Core Flavor Events

### Target: ~40–50 Events for Beta Functionality

### Purpose: Establish contract warfare gameplay, disciplined military hierarchy, operator loyalty systems, and militarized corporate-state identity

Government Reference: `eotg_pmc_government` 

---

# CORE GOVERNMENT FANTASY

PMC Governments are militarized contractor states.

They are:

* disciplined
* transactional
* militaristic
* profit-driven
* professional
* politically dangerous

Unlike Fringe governments:

* PMCs value discipline over chaos

Unlike Cartels:

* PMCs enforce order and contracts

Unlike Corporations:

* PMCs derive legitimacy from military effectiveness

Core gameplay loop:

1. secure military contracts
2. maintain operator loyalty
3. preserve discipline
4. avoid rogue commanders
5. profit from conflict
6. balance professionalism with greed

---

# EVENT CATEGORY — CONTRACT SYSTEM

This is the defining gameplay loop.

---

## Event: A New Contract Offer Arrives

### Trigger

* peace period
* neighboring conflict exists

### Description

A foreign power offers payment for military services.

### Outcomes

#### Accept the Contract

* gold income
* war obligations

#### Negotiate Better Terms

* diplomacy challenge

#### Reject the Offer

* no effect
* operator disappointment chance

### Modifiers

* `eotg_pmc_active_contract`

---

## Event: Contract Payment Delayed

### Trigger

* active contract
* unreliable employer

### Description

The client delays promised payment.

### Outcomes

#### Demand Immediate Payment

* diplomacy escalation

#### Continue Operations

* operator unrest risk

#### Seize Assets as Compensation

* war escalation risk

---

## Event: Contract Terms Violated

### Trigger

* client betrayal

### Description

The employer violates the agreement.

### Outcomes

#### Enforce the Contract Militarily

* war justification

#### Negotiate Settlement

* diplomacy outcome

#### Abandon the Contract

* prestige loss
* legitimacy gain

---

# EVENT CATEGORY — OPERATOR LOYALTY

Operators replace traditional feudal loyalty.

---

## Event: Operators Demand Better Pay

### Trigger

* low gold
* prolonged campaigns

### Description

Operators complain about compensation.

### Outcomes

#### Increase Pay

* gold loss
* loyalty increase

#### Promise Future Bonuses

* temporary stability

#### Threaten Discipline

* dread gain
* mutiny risk

### Modifiers

* `eotg_pmc_operator_discontent`

---

## Event: Veteran Operators Question Leadership

### Trigger

* weak ruler
* failed campaign

### Description

Experienced soldiers criticize command decisions.

### Outcomes

#### Listen to Their Concerns

* legitimacy gain

#### Punish Dissidents

* dread gain

#### Replace Senior Officers

* instability risk

---

## Event: Elite Unit Gains Fame

### Trigger

* successful battles

### Description

A PMC unit becomes legendary among operators.

### Outcomes

#### Reward the Unit

* military bonus

#### Use Them for Propaganda

* legitimacy gain

#### Keep Them Under Control

* reduced coup risk

### Modifiers

* `eotg_pmc_elite_unit`

---

# EVENT CATEGORY — DISCIPLINE & MILITARY CULTURE

---

## Event: Breakdown of Discipline

### Trigger

* prolonged war
* low morale

### Description

Operators ignore command structures.

### Outcomes

#### Brutal Discipline Measures

* control restored
* dread gain

#### Reform Training Standards

* long-term stability

#### Ignore the Problem

* future mutiny risk

---

## Event: Battlefield Looting

### Trigger

* victorious campaign

### Description

Operators loot conquered territory without authorization.

### Outcomes

#### Allow the Looting

* operator loyalty gain
* legitimacy loss

#### Punish the Looters

* discipline gain
* operator anger

#### Organize Controlled Looting

* balanced outcome

---

## Event: Officers Compete for Influence

### Trigger

* multiple powerful commanders

### Description

Senior officers form competing military blocs.

### Outcomes

#### Balance Their Influence

* diplomacy challenge

#### Favor One Commander

* factional shift

#### Rotate Command Positions

* stability gain
* resentment risk

---

# EVENT CATEGORY — CONTRACT WARFARE

---

## Event: Mission Objectives Escalate

### Trigger

* active contract war

### Description

The client demands expanded military operations.

### Outcomes

#### Accept Expanded Objectives

* more rewards
* greater risks

#### Refuse Expansion

* client anger

#### Demand Additional Payment

* diplomacy challenge

---

## Event: Civilian Casualties During Operations

### Trigger

* brutal military actions

### Description

PMC operations kill civilians.

### Outcomes

#### Suppress the Reports

* intrigue challenge

#### Publicly Regret the Incident

* legitimacy gain

#### Justify the Violence

* dread gain

---

## Event: Operators Commit Atrocities

### Trigger

* low discipline
* brutal commanders

### Description

Operators commit unauthorized war crimes.

### Outcomes

#### Punish the Guilty

* legitimacy gain

#### Cover It Up

* intrigue bonus

#### Encourage Fear Tactics

* dread gain

---

# EVENT CATEGORY — INTERNAL POWER STRUGGLES

---

## Event: A Commander Builds Personal Loyalty

### Trigger

* successful commander
* long campaigns

### Description

Operators become loyal to a commander over the state.

### Outcomes

#### Promote the Commander

* military bonuses
* coup risk

#### Reassign Them

* loyalty penalties

#### Secretly Undermine Them

* intrigue opportunity

---

## Event: Mercenary Faction Forms

### Trigger

* operator unrest

### Description

Operators organize around shared grievances.

### Outcomes

#### Negotiate with Them

* stability gain

#### Suppress the Movement

* rebellion risk

#### Buy Their Loyalty

* gold cost

---

## Event: Officer Coup Rumors Spread

### Trigger

* weak ruler
* powerful military leadership

### Description

Rumors spread that officers plan a takeover.

### Outcomes

#### Investigate Quietly

* intrigue chain

#### Purge Suspected Officers

* dread gain

#### Increase Loyalist Presence

* security bonus

---

# EVENT CATEGORY — PMC ECONOMICS

---

## Event: War Profits Surge

### Trigger

* multiple active contracts

### Description

Military contracts generate enormous profits.

### Outcomes

#### Reinvest into Military Expansion

* army bonuses

#### Reward Operators

* loyalty gain

#### Enrich Leadership

* personal gold gain

### Modifiers

* `eotg_pmc_war_profits`

---

## Event: Lack of Contracts Hurts Revenue

### Trigger

* prolonged peace

### Description

Without conflict, PMC finances weaken.

### Outcomes

#### Seek New Wars

* contract search modifier

#### Downsize Forces

* army reduction

#### Manufacture Instability Abroad

* intrigue opportunities

---

## Event: Arms Smuggling Opportunities

### Trigger

* nearby wars

### Description

Weapons can be sold secretly to conflict zones.

### Outcomes

#### Sell to Everyone

* huge profits
* diplomatic risks

#### Sell Selectively

* stable income

#### Refuse Illegal Sales

* legitimacy gain

---

# EVENT CATEGORY — PROPAGANDA & REPUTATION

---

## Event: Recruitment Campaign

### Trigger

* manpower shortages

### Description

The PMC launches recruitment propaganda.

### Outcomes

#### Glorify Warfare

* levy growth

#### Promise Wealth

* operator attraction bonus

#### Emphasize Professionalism

* discipline gain

### Modifiers

* `eotg_pmc_recruitment_campaign`

---

## Event: Reputation for Professionalism

### Trigger

* disciplined operations

### Description

Clients praise the PMC’s efficiency.

### Outcomes

#### Build Prestige

* legitimacy gain

#### Increase Contract Prices

* gold bonuses

#### Exploit Reputation Aggressively

* greed modifier

---

## Event: Reputation Damaged by Scandal

### Trigger

* exposed atrocities
* failed operations

### Description

Public confidence collapses.

### Outcomes

#### Launch PR Defense

* gold cost

#### Blame Rogue Operators

* stability gain

#### Ignore Public Opinion

* dread gain

---

# EVENT CATEGORY — SUCCESSION & COMMAND TRANSITION

---

## Event: Operators Debate the Successor

### Trigger

* aging ruler

### Description

Military leadership debates future command.

### Outcomes

#### Endorse a Successor

* succession influence

#### Allow Open Competition

* instability increase

#### Secretly Remove Rivals

* intrigue opportunities

---

## Event: Command Transition Crisis

### Trigger

* succession instability

### Description

Operators split loyalty between competing commanders.

### Outcomes

#### Rally Loyal Units

* military advantage

#### Negotiate Power Sharing

* temporary stability

#### Prepare for Civil Conflict

* war readiness bonus

---

## Event: The New Commander Takes Control

### Trigger

* successful succession

### Description

The new leader assumes command.

### Outcomes

#### Promise Discipline

* stability gain

#### Reward Loyal Officers

* military loyalty gain

#### Purge Opposition

* dread increase

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: The Legendary Commander

### Trigger

* extremely successful ruler

### Description

The commander becomes a legendary military figure.

### Outcomes

#### Build Cult of Leadership

* authority gain

#### Strengthen Institutional Discipline

* stability gain

#### Inspire Expansion

* conquest bonuses

### Modifier

* `eotg_pmc_legendary_commander`

---

## Event: PMC Civil War

### Trigger

* failed succession
* officer factions

### Description

Military divisions openly fight for control.

### Outcomes

#### Crush Rival Commanders

* war bonuses

#### Negotiate Military Partition

* realm split option

#### Retreat With Loyal Units

* exile survival chain

---

## Event: Endless War Doctrine

### Trigger

* highly militarized state

### Description

The PMC becomes dependent on perpetual warfare.

### Outcomes

#### Embrace Endless Conflict

* war bonuses
* peace penalties

#### Seek Stability

* economic bonuses

#### Manipulate Foreign Wars

* intrigue warfare bonuses

# PMC Government Event Design Document

## Phase 2 — Military Politics, Contractor Corruption, and Warlordization Systems

### Purpose: Expand PMC gameplay into officer rivalries, military-industrial corruption, contract manipulation, and dangerous militarized state evolution

---

# EVENT CATEGORY — OFFICER POLITICS

---

## Event: Rival Officers Form Cliques

### Trigger

* multiple powerful commanders
* prolonged campaigns

### Description

Senior officers form competing political circles inside the PMC.

### Outcomes

#### Balance the Cliques

* diplomacy challenge

#### Favor One Group

* military faction alignment

#### Break Up the Cliques

* officer resentment

### Modifiers

* `eotg_pmc_officer_cliques`

---

## Event: Junior Officers Demand Advancement

### Trigger

* stagnant command structure

### Description

Younger officers believe leadership positions are monopolized by veterans.

### Outcomes

#### Promote Rising Officers

* loyalty gain
* veteran anger

#### Maintain Seniority

* stability among veterans

#### Encourage Competition

* intrigue rivalry growth

---

## Event: Officer Duel Over Honor

### Trigger

* martial culture
* rival commanders

### Description

Two officers challenge each other over insults and battlefield disagreements.

### Outcomes

#### Allow the Duel

* injury/death risk

#### Forbid It

* discipline gain
* resentment risk

#### Manipulate the Outcome

* intrigue opportunity

---

# EVENT CATEGORY — CONTRACT MANIPULATION

---

## Event: A Client Wants Dirty Work

### Trigger

* active contract

### Description

A client secretly requests illegal military actions.

### Outcomes

#### Accept the Mission

* huge gold gain
* legitimacy risk

#### Refuse the Request

* professionalism gain

#### Blackmail the Client

* hooks gained

### Modifiers

* `eotg_pmc_black_contract`

---

## Event: Competing Contracts Create Conflict

### Trigger

* multiple simultaneous contracts

### Description

Two clients demand incompatible operations.

### Outcomes

#### Prioritize the Highest Bidder

* gold gain
* client anger

#### Attempt Balance

* diplomacy challenge

#### Secretly Manipulate Both Clients

* intrigue opportunities

---

## Event: Contract Fraud Discovered

### Trigger

* corrupt operations

### Description

Evidence emerges that officers falsified combat reports for profit.

### Outcomes

#### Punish the Officers

* legitimacy gain

#### Hide the Fraud

* intrigue bonus

#### Profit from the Scheme

* gold gain
* corruption modifier

---

# EVENT CATEGORY — PMC CORRUPTION

---

## Event: Officers Sell Military Supplies

### Trigger

* corrupt commanders

### Description

Weapons and equipment disappear into black markets.

### Outcomes

#### Crack Down Hard

* discipline gain

#### Ignore Minor Corruption

* stability maintained

#### Secretly Profit

* gold gain

---

## Event: Ghost Soldiers on Payroll

### Trigger

* high corruption

### Description

Fake soldiers exist only on payroll records.

### Outcomes

#### Investigate the Fraud

* stewardship challenge

#### Continue the Scheme

* gold savings
* military weakness risk

#### Blame Logistics Officers

* scapegoat modifier

---

## Event: Mercenary Kickback Networks

### Trigger

* wealthy officers

### Description

Commanders profit personally from contract negotiations.

### Outcomes

#### Allow the Practice

* officer loyalty gain
* corruption increase

#### Restrict Kickbacks

* legitimacy gain
* officer anger

#### Use It to Control Officers

* hooks gained

---

# EVENT CATEGORY — WARTIME ESCALATION

---

## Event: Operators Demand War Bonuses

### Trigger

* successful campaign

### Description

Operators demand extra compensation after dangerous missions.

### Outcomes

#### Pay Bonuses

* loyalty gain

#### Promise Future Rewards

* temporary calm

#### Refuse the Demands

* mutiny risk

---

## Event: Battlefield Reputation Grows

### Trigger

* repeated victories

### Description

The PMC gains a terrifying military reputation.

### Outcomes

#### Market the Reputation

* contract value increase

#### Encourage Fear

* dread gain

#### Maintain Professional Image

* legitimacy gain

### Modifiers

* `eotg_pmc_battlefield_reputation`

---

## Event: Endless Deployment Exhaustion

### Trigger

* prolonged warfare

### Description

Operators grow exhausted from nonstop campaigns.

### Outcomes

#### Rotate Troops

* gold cost
* morale recovery

#### Push Them Harder

* temporary military bonus
* future unrest

#### Recruit Replacements

* levy reinforcement

---

# EVENT CATEGORY — MILITARY INDUSTRIAL COMPLEX

---

## Event: Weapons Manufacturers Gain Influence

### Trigger

* strong war economy

### Description

Arms producers begin influencing military decisions.

### Outcomes

#### Partner with Manufacturers

* military bonuses

#### Regulate Their Influence

* legitimacy gain

#### Let Them Drive Expansion

* aggressive war bonuses

---

## Event: Experimental Weapons Proposal

### Trigger

* advanced military industry

### Description

Engineers propose dangerous experimental weapon systems.

### Outcomes

#### Fund Development

* military innovation bonus

#### Reject Unsafe Weapons

* professionalism gain

#### Test Them Secretly

* intrigue bonuses

---

## Event: The Economy Depends on War

### Trigger

* prolonged militarized economy

### Description

Peace threatens financial collapse.

### Outcomes

#### Encourage Foreign Wars

* intrigue warfare bonus

#### Diversify the Economy

* long-term stability

#### Embrace Permanent Conflict

* war economy modifier

### Modifiers

* `eotg_pmc_war_economy`

---

# EVENT CATEGORY — ROGUE COMMANDERS

---

## Event: A Commander Ignores Orders

### Trigger

* powerful commander
* weak ruler

### Description

A field commander refuses operational directives.

### Outcomes

#### Court Martial Them

* rebellion risk

#### Negotiate Compliance

* temporary loyalty

#### Secretly Assassinate Them

* intrigue chain

---

## Event: Rogue Battalion Emerges

### Trigger

* severe instability

### Description

An armed battalion acts independently from central command.

### Outcomes

#### Crush the Battalion

* military confrontation

#### Offer Amnesty

* reintegration chance

#### Let Them Operate Independently

* future warlord risk

---

## Event: Operators Follow Their Commander, Not the State

### Trigger

* charismatic commander

### Description

Troops become personally loyal to officers instead of institutions.

### Outcomes

#### Strengthen Institutional Identity

* discipline gain

#### Reward the Commander

* military bonuses
* coup risk

#### Rotate Units Frequently

* stability gain
* morale penalty

---

# EVENT CATEGORY — PMC PROPAGANDA

---

## Event: Recruitment Through Heroism

### Trigger

* successful campaigns

### Description

Propaganda glorifies elite operators.

### Outcomes

#### Heroic Marketing

* recruitment bonus

#### Fear-Based Recruitment

* dread gain

#### Professional Discipline Messaging

* discipline gain

---

## Event: Scandalous War Footage Leaks

### Trigger

* atrocities exposed

### Description

Disturbing battlefield footage spreads publicly.

### Outcomes

#### Suppress the Footage

* intrigue challenge

#### Blame Rogue Units

* legitimacy mitigation

#### Justify the Violence

* dread gain

---

## Event: Veterans Become Celebrities

### Trigger

* famous operators

### Description

Certain soldiers become public icons.

### Outcomes

#### Use Them for Recruitment

* recruitment growth

#### Keep Them Away from Politics

* reduced populism risk

#### Encourage Their Fame

* future political danger

---

# EVENT CATEGORY — SUCCESSION & COMMAND STRUGGLES

---

## Event: Officers Back Rival Heirs

### Trigger

* succession instability

### Description

Military officers divide their loyalties among competing successors.

### Outcomes

#### Consolidate Loyal Officers

* military advantage

#### Negotiate Unity

* diplomacy challenge

#### Purge Rival Supporters

* dread gain

---

## Event: The Succession Conference Fails

### Trigger

* failed succession negotiations

### Description

Command leadership cannot agree on succession.

### Outcomes

#### Force a Decision

* legitimacy risk

#### Split Operational Commands

* partial partition

#### Prepare for Military Conflict

* civil war bonuses

---

## Event: Coup During Transition

### Trigger

* weak successor

### Description

Military officers attempt to seize control during transition.

### Outcomes

#### Crush the Coup

* authority gain

#### Negotiate with Coup Leaders

* temporary stability

#### Flee With Loyal Forces

* exile chain

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: The Professional Army State

### Trigger

* extremely disciplined PMC realm

### Description

The PMC evolves into a fully militarized state apparatus.

### Outcomes

#### Institutional Military Rule

* stability bonuses

#### Officer Aristocracy

* powerful commander bonuses

#### Endless Military Expansion

* conquest bonuses

### Modifier

* `eotg_pmc_military_state`

---

## Event: The Warlord Commander

### Trigger

* rogue commander success

### Description

A commander becomes dangerously popular and independent.

### Outcomes

#### Integrate Them Into Leadership

* stability chance

#### Destroy Them

* civil war risk

#### Grant Semi-Autonomy

* future fragmentation risk

---

## Event: Peace Is Bad for Business

### Trigger

* long peace period

### Description

Executives and officers fear peace more than war.

### Outcomes

#### Manufacture Conflict Abroad

* intrigue warfare bonuses

#### Seek Civilian Contracts

* economic diversification

#### Accept Economic Decline

* stability gain

# PMC Government Event Design Document

## Phase 3 — Decision Chains, Militarized State Evolution, and Contract Empire Systems

### Purpose: Create active strategic PMC gameplay centered on contracts, discipline, military politics, and war-economy survival

---

# DECISION CHAIN — NEGOTIATE A MAJOR CONTRACT

## Decision: `eotg_pmc_negotiate_contract`

### Requirements

* nearby war OR unstable neighboring realm
* sufficient military strength
* not already overloaded with contracts

### Immediate Effects

* begins contract negotiation chain

---

## Event: Contract Negotiations Begin

### Description

Representatives from a foreign power negotiate terms for military support.

### Outcomes

#### Demand Maximum Payment

* larger rewards
* higher client tension

#### Offer Competitive Pricing

* easier acceptance
* smaller profits

#### Add Hidden Clauses

* intrigue opportunities

### Modifiers

* `eotg_pmc_contract_negotiation`

---

## Event: Client Attempts to Manipulate Terms

### Trigger

* difficult client

### Description

The client attempts to alter the agreement in their favor.

### Outcomes

#### Resist Firmly

* professionalism gain

#### Accept Modified Terms

* contract stability

#### Secretly Prepare Leverage

* hooks gained

---

## Event: Contract Signed

### Trigger

* successful negotiations

### Description

The agreement is finalized and operators mobilize.

### Outcomes

#### Begin Immediate Deployment

* military readiness bonus

#### Demand Advance Payment

* upfront gold gain

#### Publicize the Agreement

* legitimacy gain

---

# DECISION CHAIN — ENFORCE DISCIPLINE

## Decision: `eotg_pmc_enforce_discipline`

### Requirements

* low morale OR rising corruption
* active operator unrest

### Immediate Effects

* begins discipline crackdown chain

---

## Event: Military Discipline Hearings

### Description

Operators accused of misconduct face military judgment.

### Outcomes

#### Harsh Punishments

* discipline gain
* operator fear increase

#### Professional Reforms

* long-term stability

#### Selective Punishment

* intrigue manipulation opportunities

### Modifiers

* `eotg_pmc_discipline_campaign`

---

## Event: Operators Resist Crackdowns

### Trigger

* harsh measures used

### Description

Operators resent increasingly strict command policies.

### Outcomes

#### Double Down

* discipline gain
* mutiny risk

#### Ease Restrictions

* morale recovery

#### Reward Loyal Units

* stability gain

---

## Event: Discipline Restored

### Trigger

* successful crackdown

### Description

Order and professionalism return to the ranks.

### Outcomes

#### Strengthened Chain of Command

* military bonuses

#### Institutional Reform

* long-term discipline modifier

#### Publicize the Reforms

* legitimacy gain

---

# DECISION CHAIN — EXPAND OPERATOR RECRUITMENT

## Decision: `eotg_pmc_expand_recruitment`

### Requirements

* manpower shortages OR expansion goals

### Immediate Effects

* recruitment campaign begins

---

## Event: Recruitment Offices Open

### Description

The PMC aggressively recruits new operators.

### Outcomes

#### Recruit Veterans

* elite troop quality

#### Recruit Desperate Civilians

* larger manpower pool
* lower discipline

#### Recruit Foreign Specialists

* unique bonuses
* loyalty concerns

### Modifiers

* `eotg_pmc_recruitment_drive`

---

## Event: Recruitment Propaganda Escalates

### Trigger

* aggressive recruitment path

### Description

Massive propaganda glorifies military service.

### Outcomes

#### Promise Wealth

* recruitment growth

#### Promise Glory

* morale bonuses

#### Promise Stability

* discipline growth

---

## Event: Criminals Join the Ranks

### Trigger

* low standards recruitment

### Description

Dangerous individuals enter the operator corps.

### Outcomes

#### Use Them Aggressively

* military bonuses
* discipline risk

#### Purge the Worst Recruits

* professionalism gain

#### Turn Them Into Black Ops Units

* intrigue bonuses

---

# DECISION CHAIN — COURT THE ARMS INDUSTRY

## Decision: `eotg_pmc_court_arms_industry`

### Requirements

* large military economy
* active wars

### Immediate Effects

* military industry influence rises

---

## Event: Arms Manufacturers Lobby Leadership

### Description

Weapons companies seek influence over PMC policy.

### Outcomes

#### Grant Contracts Generously

* military bonuses
* corruption increase

#### Maintain Oversight

* legitimacy gain

#### Use Competition Between Manufacturers

* economic gains

### Modifiers

* `eotg_pmc_arms_lobby`

---

## Event: Experimental Weapons Demonstration

### Trigger

* advanced military investment

### Description

Manufacturers demonstrate dangerous new weapons.

### Outcomes

#### Mass Production

* military power increase

#### Limited Testing

* controlled bonuses

#### Reject the Weapons

* professionalism gain

---

## Event: Corruption in Procurement Contracts

### Trigger

* corruption high

### Description

Military procurement becomes riddled with bribery.

### Outcomes

#### Investigate the Corruption

* stewardship challenge

#### Ignore the Corruption

* officer loyalty gain

#### Profit Personally

* gold gain

---

# DECISION CHAIN — REMOVE A ROGUE COMMANDER

## Decision: `eotg_pmc_remove_commander`

### Requirements

* disloyal commander
* evidence of insubordination

### Immediate Effects

* begins confrontation chain

---

## Event: Commander Summoned to Headquarters

### Description

A dangerous commander is ordered to answer for disobedience.

### Outcomes

#### Court Martial Them

* rebellion risk

#### Offer Retirement

* peaceful resolution chance

#### Arrange an Accident

* intrigue operation

### Modifiers

* `eotg_pmc_command_crisis`

---

## Event: Loyal Operators Defend the Commander

### Trigger

* commander highly popular

### Description

Operators resist attempts to remove their leader.

### Outcomes

#### Threaten the Troops

* dread gain

#### Negotiate Quietly

* stability chance

#### Prepare for Armed Resistance

* civil conflict risk

---

## Event: The Commander Revolts

### Trigger

* failed removal attempt

### Description

The commander openly rebels.

### Outcomes

#### Crush the Revolt

* military bonuses

#### Negotiate Reintegration

* temporary autonomy

#### Retreat to Loyal Territory

* fragmentation possibility

---

# DECISION CHAIN — CREATE BLACK OPERATIONS DIVISION

## Decision: `eotg_pmc_black_ops_division`

### Requirements

* intrigue investment
* elite operators available

### Immediate Effects

* unlock covert military actions

---

## Event: Special Operations Program Begins

### Description

Elite covert units begin secret operations.

### Outcomes

#### Focus on Assassinations

* intrigue bonuses

#### Focus on Sabotage

* enemy destabilization

#### Focus on Counterinsurgency

* control bonuses

### Modifiers

* `eotg_pmc_black_operations`

---

## Event: Black Ops Atrocities Revealed

### Trigger

* covert failure

### Description

Disturbing details emerge about covert missions.

### Outcomes

#### Deny Everything

* intrigue challenge

#### Eliminate Witnesses

* dread gain

#### Blame Rogue Units

* legitimacy mitigation

---

## Event: Black Ops Gain Too Much Power

### Trigger

* prolonged black ops activity

### Description

Covert units begin operating independently.

### Outcomes

#### Bring Them Under Control

* conflict risk

#### Expand Their Authority

* intrigue bonuses
* coup risk

#### Secretly Use Them Politically

* internal manipulation bonuses

---

# DECISION CHAIN — DECLARE MARTIAL CORPORATE RULE

Late-game transformation path.

---

## Decision: `eotg_pmc_martial_rule`

### Requirements

* enormous PMC realm
* high military authority
* strong discipline

### Immediate Effects

* militarized state transformation begins

---

## Event: Civil Administration Replaced

### Description

Military leadership replaces civilian governance structures.

### Outcomes

#### Full Military Governance

* authority bonuses

#### Controlled Military Oversight

* balanced stability

#### Permanent War Administration

* conquest bonuses

### Modifiers

* `eotg_pmc_martial_state`

---

## Event: Officers Become Nobility

### Trigger

* transformation progresses

### Description

Military command evolves into hereditary elite leadership.

### Outcomes

#### Formalize Officer Aristocracy

* strong commanders

#### Preserve Meritocracy

* discipline bonuses

#### Balance Both Systems

* hybrid modifiers

---

## Event: The State Exists for War

### Trigger

* transformation completed

### Description

The PMC fully evolves into a militarized war-state.

### Outcomes

#### Endless Expansion

* military bonuses

#### Controlled Militarism

* stability bonuses

#### Military Economy Dominance

* economic war bonuses

---

# FINAL DESIGN NOTE

PMC Government now supports:

* contract warfare gameplay
* officer faction politics
* discipline systems
* military corruption
* rogue commander crises
* war economy mechanics
* covert military operations
* militarized succession struggles
* military-industrial influence
* transformation into martial war-state

This strongly differentiates PMC from the other governments:

| Fringe                         | PMC                          |
| ------------------------------ | ---------------------------- |
| chaotic warbands               | disciplined operators        |
| loyalty through charisma       | loyalty through contracts    |
| collapse through fragmentation | collapse through coups       |
| raiding culture                | professional warfare culture |

| Corporation              | PMC                       |
| ------------------------ | ------------------------- |
| covert executive warfare | direct military hierarchy |
| profit through markets   | profit through war        |
| board manipulation       | officer politics          |
| PR image                 | battlefield reputation    |

# Elven Monarchy Government Event Design Document

## Phase 1 — Functional + Core Flavor Events

### Target: ~40–50 Events for Beta Functionality

### Purpose: Establish isolationist aristocracy, Eternal Court politics, racial hierarchy tensions, and succession legitimacy struggles

Government Reference: `eotg_elven_monarchy_government` 

---

# CORE GOVERNMENT FANTASY

The Elven Monarchy is:

* ancient
* aristocratic
* isolationist
* proud
* ritualized
* culturally supremacist

This is not a chaotic government.

Its instability comes from:

* succession legitimacy
* aristocratic stagnation
* cultural arrogance
* suppression of non-elven populations
* Eternal Court politics

Core gameplay loop:

1. preserve elven supremacy
2. manage the Eternal Court
3. suppress unrest among outsiders
4. maintain legitimacy through tradition
5. balance isolationism vs diplomacy
6. survive succession confirmation crises

---

# EVENT CATEGORY — ETERNAL COURT POLITICS

This is the defining mechanic ecosystem.

---

## Event: The Eternal Court Convenes

### Trigger

* major political issue
* succession tension
* legitimacy concerns

### Description

The Eternal Court gathers to deliberate on matters of the realm.

### Outcomes

#### Respect Ancient Traditions

* legitimacy gain
* slower reforms

#### Manipulate the Court

* intrigue opportunities

#### Pressure the Regents

* dread gain
* court resentment

### Modifiers

* `eotg_elven_court_session`

---

## Event: A Celestial Lord Questions the Heir

### Trigger

* succession approaching
* weak heir legitimacy

### Description

A powerful noble publicly questions whether the heir is worthy.

### Outcomes

#### Defend the Heir Publicly

* diplomacy challenge

#### Silence the Critic

* dread gain

#### Offer Concessions

* noble loyalty gain

---

## Event: Court Factions Form

### Trigger

* multiple powerful vassals

### Description

Noble blocs form competing political circles within the Eternal Court.

### Outcomes

#### Balance the Factions

* diplomacy challenge

#### Support One Bloc

* faction loyalty gain

#### Undermine All Factions

* intrigue opportunities

---

# EVENT CATEGORY — ISOLATIONISM

---

## Event: Foreign Envoys Arrive

### Trigger

* diplomacy interaction
* nearby foreign rulers

### Description

Foreign envoys request cooperation and diplomacy.

### Outcomes

#### Treat Them with Respect

* diplomacy gain

#### Openly Mock Them

* prestige gain among elves
* diplomacy penalties

#### Refuse to Meet Them

* isolationism increase

### Modifiers

* `eotg_elven_isolationist_posture`

---

## Event: Elven Purists Demand Separation

### Trigger

* many non-elven subjects

### Description

Traditionalists demand stricter separation from outsiders.

### Outcomes

#### Enforce Segregation

* elven loyalty gain
* non-elven unrest

#### Moderate the Policy

* stability gain

#### Reject the Purists

* court anger

---

## Event: Outsider Customs Spread

### Trigger

* multicultural holdings

### Description

Foreign traditions begin influencing local culture.

### Outcomes

#### Suppress the Influence

* control gain

#### Tolerate Limited Exchange

* development gain

#### Secretly Embrace Innovation

* intrigue/stewardship bonuses

---

# EVENT CATEGORY — NON-ELVEN SUBJECTS

This supports the second-class subject mechanics.

---

## Event: Non-Elven Unrest Grows

### Trigger

* high non-elven population
* harsh policies

### Description

Outsider populations grow resentful of discrimination.

### Outcomes

#### Brutally Suppress Them

* dread gain

#### Ease Restrictions

* stability gain
* noble anger

#### Ignore the Problem

* revolt risk

### Modifiers

* `eotg_elven_subject_unrest`

---

## Event: A Non-Elven Official Shows Talent

### Trigger

* talented outsider character

### Description

An outsider demonstrates exceptional ability despite restrictions.

### Outcomes

#### Secretly Use Their Skills

* stewardship/intrigue bonus

#### Publicly Reward Them

* noble anger
* outsider loyalty gain

#### Reject Their Advancement

* stability among nobles

---

## Event: Mixed Communities Form

### Trigger

* long multicultural rule

### Description

Elves and outsiders increasingly live together.

### Outcomes

#### Separate Them

* control gain

#### Tolerate the Communities

* development gain
* purist anger

#### Encourage Assimilation

* hybrid cultural pressure

---

# EVENT CATEGORY — SUCCESSION & CONFIRMATION

The most important instability mechanic.

---

## Event: The Heir Awaits Judgment

### Trigger

* ruler death
* succession begins

### Description

The Eternal Court prepares to judge the heir.

### Outcomes

#### Appeal to Tradition

* legitimacy gain chance

#### Bribe Influential Regents

* gold cost

#### Threaten Dissenters

* dread gain

---

## Event: The Eternal Court Debates

### Trigger

* succession confirmation

### Description

The Court argues over whether the heir should rule.

### Outcomes

#### Accept the Heir

* normal succession

#### Demand Concessions

* weaker authority

#### Support a Rival Claimant

* succession crisis

---

## Event: Regency Proposed

### Trigger

* weak heir
* divided court

### Description

Some nobles demand a regency instead of full inheritance.

### Outcomes

#### Accept Regency

* temporary stability

#### Refuse the Proposal

* legitimacy risk

#### Eliminate Opposition Quietly

* intrigue opportunities

---

## Event: Court Schism Over Succession

### Trigger

* hostile court outcome

### Description

The Eternal Court fractures over succession legitimacy.

### Outcomes

#### Negotiate Unity

* diplomacy challenge

#### Crush Rival Claimants

* civil war risk

#### Divide Court Privileges

* temporary peace

---

# EVENT CATEGORY — ELVEN ARISTOCRACY

---

## Event: Noble Bloodline Dispute

### Trigger

* rival noble houses

### Description

Ancient noble families dispute lineage claims.

### Outcomes

#### Support One Bloodline

* faction alignment

#### Demand Proof

* intrigue challenge

#### Ignore the Dispute

* future rivalry escalation

---

## Event: Aristocrats Reject Reform

### Trigger

* modernization attempts

### Description

Traditional nobles resist administrative changes.

### Outcomes

#### Push Reforms Anyway

* development gains
* noble anger

#### Compromise Carefully

* moderate stability

#### Preserve Tradition

* legitimacy gain

---

## Event: A Celestial Lord Grows Too Powerful

### Trigger

* strong vassal

### Description

A noble accumulates dangerous influence.

### Outcomes

#### Limit Their Authority

* rebellion risk

#### Bind Them by Marriage

* alliance gain

#### Use Them Against Rivals

* intrigue opportunities

---

# EVENT CATEGORY — CULTURAL SUPREMACY

---

## Event: Ancient Elven Superiority Debates

### Trigger

* isolationist rulers

### Description

Court scholars argue that elves are destined to rule lesser peoples.

### Outcomes

#### Promote the Doctrine

* elven loyalty gain
* diplomacy penalties

#### Moderate the Extremism

* stability gain

#### Reject the Doctrine

* traditionalist anger

---

## Event: Outsider Ambassador Humiliated

### Trigger

* diplomatic visit

### Description

A foreign diplomat is insulted publicly by nobles.

### Outcomes

#### Encourage the Humiliation

* prestige among isolationists

#### Apologize Diplomatically

* diplomacy gain

#### Punish the Noble Responsible

* noble anger

---

## Event: Ancient Traditions Revived

### Trigger

* long reign
* high legitimacy

### Description

Ancient ceremonial practices return to prominence.

### Outcomes

#### Fully Restore the Rituals

* legitimacy gain

#### Adapt Them for Modern Times

* balanced bonuses

#### Ignore the Old Ways

* noble disapproval

---

# EVENT CATEGORY — CULTURAL LOYALTY SYSTEM

---

## Event: Minor Elven Realm Requests Guidance

### Trigger

* nearby elven minor

### Description

A smaller elven realm seeks support from the monarchy.

### Outcomes

#### Offer Protection

* alliance opportunity

#### Demand Loyalty

* influence gain

#### Ignore Their Request

* prestige loss

---

## Event: Elven Solidarity Against Outsiders

### Trigger

* foreign threats

### Description

Elven realms discuss unified cultural defense.

### Outcomes

#### Promote Unity

* diplomacy bonuses with elves

#### Exploit the Fear

* authority gain

#### Refuse Cooperation

* isolationism gain

---

## Event: Religious Differences Cause Tension

### Trigger

* differing elven faiths

### Description

Elven rulers argue over faith while sharing cultural identity.

### Outcomes

#### Emphasize Shared Heritage

* cultural unity gain

#### Exploit Religious Division

* intrigue opportunities

#### Demand Orthodoxy

* unrest risk

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: The Eternal King’s Shadow

### Trigger

* extremely prestigious ruler

### Description

Some whisper the ruler approaches the greatness of ancient Eternal Kings.

### Outcomes

#### Embrace the Myth

* legitimacy gain

#### Reject Divine Comparisons

* diplomacy gain

#### Use the Myth Politically

* authority gain

### Modifiers

* `eotg_elven_royal_myth`

---

## Event: The Court Fractures

### Trigger

* failed succession
* multiple hostile nobles

### Description

The Eternal Court collapses into open political warfare.

### Outcomes

#### Crush the Dissidents

* civil war bonuses

#### Negotiate Court Privileges

* temporary peace

#### Retreat to Loyal Territories

* fragmentation risk

---

## Event: The Old Ways Fade

### Trigger

* modernization pressure
* multicultural influence

### Description

Ancient elven traditions weaken under modern pressures.

### Outcomes

#### Preserve Tradition at All Costs

* legitimacy gain
* development penalties

#### Adapt Carefully

* balanced modernization

#### Embrace Change

* innovation bonuses
* noble unrest
# Elven Monarchy Government Event Design Document

## Phase 2 — Court Intrigue, Cultural Decay, and Aristocratic Power Systems

### Purpose: Expand Eternal Court politics, noble conspiracies, racial hierarchy tensions, and isolationist decline mechanics

---

# EVENT CATEGORY — ETERNAL COURT INTRIGUE

---

## Event: Secret Alliances Within the Court

### Trigger

* rival noble factions
* unstable succession period

### Description

Noble houses secretly negotiate alliances against rivals.

### Outcomes

#### Expose the Conspiracy

* intrigue challenge

#### Join the Alliance Secretly

* faction benefits

#### Manipulate Both Sides

* hooks gained

### Modifiers

* `eotg_elven_hidden_court_pact`

---

## Event: Ancient Rivalries Rekindled

### Trigger

* noble house disputes

### Description

Old grudges between noble bloodlines erupt again.

### Outcomes

#### Mediate Peace

* diplomacy gain

#### Encourage the Rivalry

* weaken both houses

#### Publicly Support One House

* faction loyalty shift

---

## Event: A Regent Publicly Defies the Throne

### Trigger

* weak ruler
* strong Eternal Regent

### Description

A powerful noble openly ignores royal authority.

### Outcomes

#### Demand Submission

* rebellion risk

#### Negotiate Privileges

* reduced authority

#### Quiet Assassination Plot

* intrigue chain

---

# EVENT CATEGORY — ISOLATIONIST RADICALIZATION

---

## Event: Isolationist Scholars Gain Influence

### Trigger

* high isolationism

### Description

Court philosophers argue outsiders corrupt civilization itself.

### Outcomes

#### Promote Their Ideas

* noble loyalty gain
* diplomacy penalties

#### Restrict Their Influence

* moderate stability

#### Secretly Fund Them

* intrigue bonuses

### Modifiers

* `eotg_elven_radical_isolationism`

---

## Event: Trade With Outsiders Debated

### Trigger

* economic pressures

### Description

Merchants argue foreign trade is necessary for prosperity.

### Outcomes

#### Restrict Trade

* isolationism gain
* economic penalty

#### Controlled Trade Access

* balanced bonuses

#### Expand Foreign Trade

* development gain
* noble anger

---

## Event: Foreign Artifacts Enter the Court

### Trigger

* diplomacy/trade events

### Description

Exotic foreign creations fascinate younger nobles.

### Outcomes

#### Ban the Artifacts

* traditionalist approval

#### Study Them Secretly

* innovation bonuses

#### Display Them Publicly

* cultural tension

---

# EVENT CATEGORY — OUTSIDER RESISTANCE

---

## Event: Secret Meetings Among Outsiders

### Trigger

* high non-elven unrest

### Description

Non-elven populations organize quietly against discrimination.

### Outcomes

#### Brutal Crackdowns

* dread gain

#### Infiltrate Their Groups

* intrigue opportunities

#### Offer Limited Rights

* unrest reduction

### Modifiers

* `eotg_elven_underground_resistance`

---

## Event: An Outsider Revolt Leader Emerges

### Trigger

* prolonged oppression

### Description

A charismatic outsider inspires resistance movements.

### Outcomes

#### Assassinate the Leader

* intrigue chain

#### Crush the Movement Militarily

* revolt suppression

#### Negotiate Reforms

* stability gain

---

## Event: Elven Soldiers Refuse Brutality

### Trigger

* harsh oppression policies

### Description

Some elven warriors question excessive cruelty.

### Outcomes

#### Demand Obedience

* dread gain

#### Moderate Policies

* military loyalty gain

#### Replace the Officers

* instability risk

---

# EVENT CATEGORY — ARISTOCRATIC DECAY

---

## Event: Noble Decadence Spreads

### Trigger

* long peace
* wealthy aristocracy

### Description

The nobility grows decadent and detached from reality.

### Outcomes

#### Encourage Luxury

* noble loyalty gain
* military weakness risk

#### Demand Discipline

* aristocrat anger

#### Ignore the Decay

* future instability

### Modifiers

* `eotg_elven_noble_decay`

---

## Event: Ancient Bloodline Obsession

### Trigger

* strong aristocratic traditions

### Description

Nobles obsess over increasingly narrow bloodline purity.

### Outcomes

#### Encourage Purity Traditions

* noble approval
* heir risks

#### Quietly Discourage Extremes

* stability gain

#### Publicly Reject the Practice

* legitimacy risk

---

## Event: Young Nobles Embrace Dangerous Ideas

### Trigger

* modernization pressure

### Description

Younger aristocrats question ancient traditions.

### Outcomes

#### Suppress Radical Ideas

* control gain

#### Allow Debate

* innovation growth

#### Secretly Support Reformists

* intrigue opportunities

---

# EVENT CATEGORY — SUCCESSION MANIPULATION

---

## Event: Court Members Demand Concessions

### Trigger

* succession uncertainty

### Description

Regents demand privileges before supporting succession.

### Outcomes

#### Grant Concessions

* succession support

#### Refuse Demands

* legitimacy risk

#### Secretly Blackmail Them

* hooks gained

---

## Event: Rival Claimant Gains Court Support

### Trigger

* weak heir

### Description

A rival claimant gathers backing from powerful nobles.

### Outcomes

#### Discredit the Rival

* intrigue challenge

#### Negotiate Shared Power

* temporary stability

#### Prepare for Civil Conflict

* military readiness

---

## Event: Succession Deliberations Drag On

### Trigger

* divided Eternal Court

### Description

The Court delays confirmation endlessly.

### Outcomes

#### Force Immediate Decision

* legitimacy risk

#### Allow Deliberation

* regency extension

#### Secretly Remove Opponents

* intrigue escalation

---

# EVENT CATEGORY — CULTURAL SUPERIORITY SYSTEMS

---

## Event: Elven Histories Rewritten

### Trigger

* supremacist ideology

### Description

Scholars alter history to glorify elven civilization.

### Outcomes

#### Promote the Revised History

* legitimacy gain

#### Preserve Accurate Records

* diplomacy gain

#### Use History as Propaganda

* authority bonuses

---

## Event: Outsider Servants Humiliated

### Trigger

* arrogant nobles

### Description

Nobles publicly degrade outsider servants and officials.

### Outcomes

#### Encourage the Behavior

* noble approval
* unrest increase

#### Quietly Condemn It

* stability gain

#### Punish the Nobles

* aristocratic anger

---

## Event: Debate Over Outsider Assimilation

### Trigger

* long multicultural rule

### Description

Some argue outsiders can never truly join elven civilization.

### Outcomes

#### Reject Assimilation Entirely

* isolationism increase

#### Controlled Assimilation

* moderate stability

#### Encourage Integration

* noble unrest

---

# EVENT CATEGORY — CULTURAL LOYALTY & ELVEN UNITY

---

## Event: Call for Elven Unity

### Trigger

* external threats
* fragmented elven realms

### Description

Messengers urge elven rulers to stand together.

### Outcomes

#### Rally the Elven Realms

* diplomacy bonuses

#### Demand Submission

* authority gain

#### Ignore the Appeals

* prestige loss

---

## Event: Minor Realm Refuses Guidance

### Trigger

* proud elven minor realm

### Description

A smaller elven ruler rejects outside influence.

### Outcomes

#### Respect Their Independence

* diplomacy gain

#### Pressure Them Politically

* influence growth

#### Threaten Intervention

* conflict risk

---

## Event: Shared Heritage Celebrations

### Trigger

* peaceful relations between elven realms

### Description

Elven rulers celebrate ancient shared traditions.

### Outcomes

#### Expand Cultural Ties

* diplomacy gain

#### Use Celebrations Politically

* legitimacy bonuses

#### Exclude Rival Houses

* faction tension

---

# EVENT CATEGORY — MILITARY & SUPREMACY

---

## Event: Elite Elven Guard Demands Privilege

### Trigger

* elite military units

### Description

Prestigious warriors demand greater status.

### Outcomes

#### Grant Privileges

* military loyalty gain

#### Refuse Their Demands

* military anger

#### Use Rival Units Against Them

* intrigue opportunities

---

## Event: Non-Elven Auxiliaries Distrusted

### Trigger

* outsider military units

### Description

Elven commanders distrust non-elven soldiers.

### Outcomes

#### Remove Them from Service

* military reduction

#### Restrict Their Roles

* moderate stability

#### Reward Loyal Auxiliaries

* outsider loyalty gain

---

## Event: Ancient War Doctrine Revived

### Trigger

* militaristic ruler

### Description

Ancient elven military philosophies return.

### Outcomes

#### Embrace Traditional Warfare

* military bonuses

#### Adapt Old Doctrines

* balanced improvements

#### Reject Outdated Methods

* noble military anger

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: The Eternal Court Splits the Realm

### Trigger

* catastrophic succession crisis

### Description

The Court considers dividing the realm between rival claimants.

### Outcomes

#### Accept Partition

* peaceful fragmentation

#### Reject Division

* civil war escalation

#### Eliminate Rival Claimants

* intrigue bloodbath

---

## Event: The Isolationist Dream

### Trigger

* extreme isolationism success

### Description

The realm nearly severs itself completely from foreign influence.

### Outcomes

#### Total Isolation

* strong internal stability
* diplomatic collapse

#### Controlled Isolation

* balanced modifiers

#### Reopen Limited Relations

* diplomacy recovery

### Modifier

* `eotg_elven_closed_realm`

---

## Event: Twilight of the Ancient Houses

### Trigger

* modernization + weak traditions

### Description

The old aristocratic order begins collapsing.

### Outcomes

#### Preserve the Ancient Houses

* legitimacy gain
* development penalties

#### Reform the Aristocracy

* modernization bonuses

#### Let the Old Order Die

* noble rebellion risk
# Elven Monarchy Government Event Design Document

## Phase 3 — Decision Chains, Aristocratic Authority Systems, and Late-Stage Civilizational Decline

### Purpose: Create active gameplay loops for isolationism, noble control, succession legitimacy, and preservation of ancient civilization

---

# DECISION CHAIN — CONVENE THE ETERNAL COURT

## Decision: `eotg_elven_convene_eternal_court`

### Requirements

* succession concerns OR legitimacy loss OR major noble tensions

### Immediate Effects

* Eternal Court session begins
* noble political activity increases

---

## Event: The Court Assembles

### Description

Ancient nobles gather beneath ceremonial banners to debate the future of the realm.

### Outcomes

#### Respect Every Tradition

* legitimacy gain
* reform slowdown

#### Quietly Manipulate the Debate

* intrigue bonuses

#### Dominate the Court by Authority

* dread gain
* noble resentment

### Modifiers

* `eotg_elven_grand_court_session`

---

## Event: Noble Houses Form Temporary Alliances

### Trigger

* active court session

### Description

Political blocs emerge among rival houses.

### Outcomes

#### Encourage Balance

* diplomacy gains

#### Support a Bloc

* faction loyalty shift

#### Secretly Divide the Alliances

* hooks gained

---

## Event: Court Session Ends in Deadlock

### Trigger

* failed negotiations

### Description

The Court cannot agree on critical matters.

### Outcomes

#### Force a Decision

* legitimacy risk

#### Delay Action

* stability loss

#### Quietly Remove Opponents

* intrigue escalation

---

# DECISION CHAIN — ENFORCE ELVEN SUPREMACY

## Decision: `eotg_elven_enforce_supremacy`

### Requirements

* large outsider population
* noble pressure high

### Immediate Effects

* outsider unrest increases
* elven noble approval rises

---

## Event: New Restrictions Imposed

### Description

The monarchy introduces stricter laws separating elves from outsiders.

### Outcomes

#### Harsh Segregation

* noble loyalty gain
* unrest increase

#### Moderate Restrictions

* balanced modifiers

#### Symbolic Measures Only

* smaller stability changes

### Modifiers

* `eotg_elven_supremacist_policy`

---

## Event: Outsider Resistance Organizes

### Trigger

* harsh enforcement

### Description

Oppressed populations begin coordinated resistance.

### Outcomes

#### Brutal Suppression

* dread gain

#### Infiltrate the Resistance

* intrigue opportunities

#### Offer Limited Concessions

* unrest reduction

---

## Event: Young Elves Question the Policies

### Trigger

* modernization pressure

### Description

Some younger nobles challenge supremacist ideology.

### Outcomes

#### Silence the Reformists

* control gain

#### Allow Controlled Debate

* innovation gain

#### Secretly Encourage Reform

* intrigue bonuses

---

# DECISION CHAIN — SEAL THE REALM

Extreme isolationist pathway.

---

## Decision: `eotg_elven_seal_realm`

### Requirements

* high isolationism
* strong internal stability

### Immediate Effects

* diplomacy penalties
* internal stability bonuses

---

## Event: Borders Begin to Close

### Description

Foreign trade and travel restrictions tighten dramatically.

### Outcomes

#### Full Isolation

* strong internal control
* economic penalties

#### Controlled Isolation

* balanced outcome

#### Secret Exceptions for Trusted Traders

* intrigue/economic bonuses

### Modifiers

* `eotg_elven_closed_borders`

---

## Event: Merchants Protest Isolation

### Trigger

* trade restrictions

### Description

Merchant groups warn the realm will stagnate.

### Outcomes

#### Ignore Their Complaints

* noble approval gain

#### Allow Limited Trade

* stability increase

#### Suppress Merchant Opposition

* dread gain

---

## Event: Foreign Powers Grow Suspicious

### Trigger

* long isolation period

### Description

Neighbors fear what occurs behind sealed borders.

### Outcomes

#### Exploit the Fear

* diplomacy intimidation bonus

#### Reassure Neighbors

* diplomacy recovery

#### Ignore Foreign Concerns

* isolationism gain

---

# DECISION CHAIN — CONFIRM THE HEIR

Core succession stabilization system.

---

## Decision: `eotg_elven_confirm_heir`

### Requirements

* designated heir exists
* ruler aging OR legitimacy concerns

### Immediate Effects

* confirmation debate begins

---

## Event: The Heir Presented to the Court

### Description

The heir stands before the Eternal Court for judgment.

### Outcomes

#### Emphasize Noble Bloodline

* legitimacy gain

#### Emphasize Competence

* military/stewardship support

#### Threaten Dissenters

* dread gain

### Modifiers

* `eotg_elven_heir_confirmation`

---

## Event: Regents Demand Concessions

### Trigger

* divided court

### Description

Powerful nobles demand privileges before supporting succession.

### Outcomes

#### Grant Privileges

* succession stability

#### Refuse Completely

* legitimacy danger

#### Secretly Blackmail Regents

* hooks gained

---

## Event: Rival Claimant Challenges the Heir

### Trigger

* weak confirmation support

### Description

Another noble asserts superior claim.

### Outcomes

#### Duel of Legitimacy

* diplomacy challenge

#### Arrange Their Elimination

* intrigue chain

#### Prepare for Succession War

* military readiness

---

# DECISION CHAIN — RESTORE ANCIENT TRADITIONS

Traditionalist path.

---

## Decision: `eotg_elven_restore_traditions`

### Requirements

* high legitimacy
* traditionalist support

### Immediate Effects

* ancient ritual revival begins

---

## Event: Forgotten Rituals Return

### Description

Old ceremonies and customs return to court life.

### Outcomes

#### Full Restoration

* legitimacy gain

#### Adapt Rituals to Modernity

* balanced bonuses

#### Use Rituals Politically

* authority gain

### Modifiers

* `eotg_elven_restored_rituals`

---

## Event: Reformists Mock the Traditions

### Trigger

* modernization factions exist

### Description

Some nobles see the rituals as outdated theater.

### Outcomes

#### Punish the Reformists

* noble loyalty gain

#### Tolerate Dissent

* innovation bonuses

#### Secretly Use Reformists

* intrigue opportunities

---

## Event: Ancient Ceremony Goes Wrong

### Trigger

* failed restoration chain

### Description

A ceremonial disaster embarrasses the monarchy.

### Outcomes

#### Blame Sabotage

* intrigue escalation

#### Publicly Accept Failure

* legitimacy loss

#### Suppress News of the Failure

* intrigue challenge

---

# DECISION CHAIN — PURGE A NOBLE HOUSE

Authoritarian stabilization tool.

---

## Decision: `eotg_elven_purge_house`

### Requirements

* disloyal noble house
* evidence or fabricated accusations

### Immediate Effects

* purge investigation begins

---

## Event: Charges Against the House

### Description

The monarchy accuses a noble house of treason or corruption.

### Outcomes

#### Public Trial

* legitimacy gain
* faction escalation risk

#### Quiet Assassinations

* intrigue bonus

#### Seize Their Holdings Immediately

* gold gain
* rebellion risk

### Modifiers

* `eotg_elven_house_purge`

---

## Event: Noble Allies Rally to the Accused

### Trigger

* strong noble alliances

### Description

Other houses defend the targeted family.

### Outcomes

#### Expand the Purge

* dread gain

#### Negotiate Compromise

* temporary peace

#### Divide the Nobility

* intrigue opportunities

---

## Event: The House Falls

### Trigger

* successful purge

### Description

An ancient noble bloodline collapses.

### Outcomes

#### Redistribute Their Lands

* vassal loyalty shifts

#### Absorb Everything into Crown Authority

* authority gain

#### Install Loyal Puppet Nobles

* stability increase

---

# DECISION CHAIN — GUIDE THE YOUNG NOBILITY

Modernization vs stagnation path.

---

## Decision: `eotg_elven_guide_young_nobles`

### Requirements

* young reformist nobles exist

### Immediate Effects

* ideological shaping begins

---

## Event: Young Aristocrats Debate the Future

### Description

The next generation argues over the destiny of elven civilization.

### Outcomes

#### Teach Ancient Supremacy

* traditionalist loyalty

#### Encourage Controlled Reform

* balanced modernization

#### Promote Radical Modernization

* innovation growth
* noble unrest

### Modifiers

* `eotg_elven_noble_education`

---

## Event: Radical Young Nobles Form Secret Circles

### Trigger

* reform pressure high

### Description

Young aristocrats organize around dangerous ideas.

### Outcomes

#### Crush the Circles

* control gain

#### Infiltrate Them

* intrigue opportunities

#### Quietly Support Them

* future reform path bonuses

---

## Event: The New Generation Takes Influence

### Trigger

* successful guidance path

### Description

A new political generation rises within the Court.

### Outcomes

#### Traditionalist Generation

* legitimacy bonuses

#### Balanced Generation

* stability bonuses

#### Reformist Generation

* modernization bonuses

---

# DECISION CHAIN — DECLARE THE ETERNAL REALM

Late-game ideological transformation.

---

## Decision: `eotg_elven_eternal_realm`

### Requirements

* massive realm
* high legitimacy
* strong noble control

### Immediate Effects

* ideological transformation begins

---

## Event: The Realm Proclaims Eternal Destiny

### Description

The monarchy declares the realm the rightful eternal civilization.

### Outcomes

#### Absolute Elven Supremacy

* authority bonuses

#### Enlightened Eternal Order

* stability bonuses

#### Isolationist Eternal Kingdom

* internal control bonuses

### Modifiers

* `eotg_elven_eternal_realm`

---

## Event: Foreigners Fear the Eternal Realm

### Trigger

* transformation progresses

### Description

Other powers grow fearful of the monarchy’s ideology.

### Outcomes

#### Exploit Their Fear

* diplomacy intimidation

#### Reassure Foreign Powers

* diplomacy recovery

#### Ignore Foreign Reactions

* isolationism gain

---

## Event: The Realm Rejects Change Forever

### Trigger

* extreme traditionalist outcome

### Description

The monarchy fully commits to preserving ancient civilization unchanged.

### Outcomes

#### Eternal Stability

* legitimacy bonuses

#### Cultural Stagnation

* development penalties

#### Sacred Isolation

* strong internal unity
* diplomatic collapse

---

# FINAL DESIGN NOTE

Elven Monarchy now supports:

* Eternal Court politics
* succession legitimacy crises
* noble faction management
* isolationism systems
* outsider oppression mechanics
* aristocratic decay
* ideological supremacy systems
* noble purges
* reform vs stagnation struggles
* civilizational preservation gameplay

Strong thematic identity:

| Elven Monarchy               | Corporation                |
| ---------------------------- | -------------------------- |
| ancient aristocracy          | modern executive oligarchy |
| legitimacy through tradition | legitimacy through success |
| court politics               | board politics             |
| cultural purity              | economic efficiency        |
| isolationism                 | expansionist capitalism    |

| Elven Monarchy        | Fringe              |
| --------------------- | ------------------- |
| rigid hierarchy       | chaotic warbands    |
| ancient rituals       | frontier survival   |
| succession legitimacy | succession violence |
| stagnation            | instability         |
# New Cauldron Democracy Government Event Design Document

## Phase 1 — Functional + Core Flavor Events

### Target: ~60 Events for Beta Functionality

### Purpose: Establish senate politics, presidential elections, campaign systems, legitimacy crises, and democratic instability

Government Reference: `eotg_new_cauldron_government` 

---

# CORE GOVERNMENT FANTASY

The New Cauldron Democracy is:

* ambitious
* ideological
* politically fractured
* bureaucratic
* militarized
* democratic but corruptible

Unlike the other governments:

* legitimacy comes from elections and institutions
* instability comes from political paralysis and factionalism
* rulers must maintain coalitions instead of fear alone

Core gameplay loop:

1. win elections
2. manage Senate support
3. pass legislation and war votes
4. balance promises vs reality
5. survive scandals
6. prevent democratic collapse

---

# EVENT CATEGORY — SENATE POLITICS

This is the defining mechanic ecosystem.

---

## Event: Senate Debate Turns Hostile

### Trigger

* controversial legislation
* low Senate support

### Description

Senators openly attack presidential leadership during debate.

### Outcomes

#### Negotiate Compromise

* Senate support gain

#### Publicly Shame Opponents

* dread-style political pressure
* legitimacy risk

#### Delay the Vote

* stability loss

### Modifiers

* `eotg_nc_senate_gridlock`

---

## Event: Senator Demands Concessions

### Trigger

* important Senate vote pending

### Description

A Senator demands political favors in exchange for support.

### Outcomes

#### Offer a Council Position

* Senate support gain

#### Promise Future Funding

* future obligation modifier

#### Refuse the Demand

* vote opposition increases

---

## Event: Regional Bloc Forms in Senate

### Trigger

* several allied States

### Description

Multiple Senators unite into a voting bloc.

### Outcomes

#### Court the Bloc

* diplomacy challenge

#### Divide the Coalition

* intrigue opportunity

#### Ignore Them

* bloc influence grows

---

# EVENT CATEGORY — PRESIDENTIAL ELECTIONS

Core government mechanic.

---

## Event: Campaign Season Begins

### Trigger

* final years of presidential term

### Description

Candidates begin campaigning across the republic.

### Outcomes

#### Campaign Aggressively

* vote weight gain
* gold cost

#### Focus on Elite Support

* Senate influence gain

#### Focus on Public Messaging

* legitimacy boost

### Modifiers

* `eotg_nc_campaign_season`

---

## Event: A Rival Candidate Gains Momentum

### Trigger

* strong rival candidate

### Description

A political rival surges in popularity.

### Outcomes

#### Attack Their Record

* intrigue challenge

#### Debate Publicly

* diplomacy challenge

#### Spread Quiet Rumors

* scandal risk

---

## Event: Campaign Promise Made

### Trigger

* campaign decision

### Description

The candidate publicly promises future reforms.

### Outcomes

#### Promise Economic Reform

* economic support gain

#### Promise Military Expansion

* military support gain

#### Promise Anti-Corruption Measures

* legitimacy gain

### Hidden Effect

Broken promises later create legitimacy penalties.

---

## Event: Election Day

### Trigger

* election resolution

### Description

Votes are counted across the republic.

### Outcomes

#### Clear Victory

* legitimacy bonus

#### Narrow Victory

* instability risk

#### Contested Election

* Senate crisis chain

---

# EVENT CATEGORY — VOTE BUYING & CORRUPTION

---

## Event: Senators Accept Bribes

### Trigger

* vote buying attempt

### Description

Several Senators quietly accept political payments.

### Outcomes

#### Expand the Bribery

* vote support gain
* corruption risk

#### Keep It Limited

* smaller gains

#### Record Their Corruption

* hooks gained

### Modifiers

* `eotg_nc_senate_corruption`

---

## Event: Vote Buying Exposed

### Trigger

* bribery discovered

### Description

Evidence of corruption spreads publicly.

### Outcomes

#### Deny Everything

* intrigue challenge

#### Sacrifice a Senator

* legitimacy recovery

#### Admit Political Reality

* elite approval
* legitimacy loss

---

## Event: Anti-Corruption Movement Rises

### Trigger

* corruption high

### Description

Reformers demand sweeping political changes.

### Outcomes

#### Support Reform

* legitimacy gain
* elite anger

#### Suppress Reformers

* dread-style pressure

#### Manipulate the Movement

* intrigue bonuses

---

# EVENT CATEGORY — WAR & SENATE AUTHORITY

---

## Event: Senate Refuses War Authorization

### Trigger

* offensive war request denied

### Description

The Senate rejects military action.

### Outcomes

#### Respect the Decision

* legitimacy gain

#### Pressure Senators

* political hostility

#### Consider Emergency Powers

* unlock escalation chain

---

## Event: Emergency Powers Declared

### Trigger

* emergency powers decision

### Description

The President bypasses Senate authority.

### Outcomes

#### Limited Emergency Measures

* temporary war authorization

#### Full Executive Override

* large legitimacy penalty

#### Promise Temporary Use

* smaller penalties

### Modifiers

* `eotg_nc_emergency_powers`

---

## Event: Senators Outraged by Executive Overreach

### Trigger

* emergency powers active

### Description

Many Senators fear authoritarianism.

### Outcomes

#### Reassure the Senate

* diplomacy challenge

#### Threaten Political Enemies

* dread increase

#### Arrest Extremists

* legitimacy risk

---

# EVENT CATEGORY — STATES & REGIONAL POLITICS

---

## Event: A State Threatens Secession

### Trigger

* low legitimacy
* angry State ruler

### Description

A State government threatens withdrawal from the republic.

### Outcomes

#### Negotiate Autonomy

* stability gain

#### Threaten Federal Intervention

* rebellion risk

#### Offer Political Concessions

* Senate shifts

---

## Event: Governors Defy Federal Policy

### Trigger

* weak President

### Description

Regional Governors ignore presidential directives.

### Outcomes

#### Enforce Federal Authority

* legitimacy challenge

#### Allow Regional Flexibility

* stability gain

#### Secretly Undermine the Governors

* intrigue opportunities

---

## Event: Regional Economic Dispute

### Trigger

* uneven development

### Description

States accuse each other of unfair economic treatment.

### Outcomes

#### Mediate Fairly

* diplomacy gain

#### Favor Strategic States

* faction support gain

#### Ignore the Conflict

* regional anger

---

# EVENT CATEGORY — PUBLIC OPINION & MEDIA

---

## Event: Public Approval Falls

### Trigger

* failed wars
* scandals
* economic decline

### Description

Citizens lose confidence in leadership.

### Outcomes

#### Public Address

* diplomacy challenge

#### Blame Political Rivals

* intrigue gain

#### Promise Sweeping Reform

* temporary legitimacy gain

### Modifiers

* `eotg_nc_public_discontent`

---

## Event: Investigative Journalists Publish Scandal

### Trigger

* corruption or intrigue failures

### Description

Journalists uncover damaging political information.

### Outcomes

#### Suppress the Story

* intrigue challenge

#### Publicly Respond

* diplomacy challenge

#### Destroy the Journalists’ Reputation

* scandal escalation risk

---

## Event: Patriotic Unity Movement Emerges

### Trigger

* external threats

### Description

Citizens rally around national identity.

### Outcomes

#### Encourage Unity

* legitimacy gain

#### Weaponize Patriotism

* war support gain

#### Moderate the Movement

* stability bonus

---

# EVENT CATEGORY — SUCCESSION & MIDTERM CRISIS

---

## Event: The President Dies in Office

### Trigger

* ruler death during term

### Description

The republic mourns the President’s death.

### Outcomes

#### Vice President Assumes Office

* stability bonus

#### Senate Demands Immediate Election

* instability risk

#### Political Chaos Erupts

* succession crisis

### Modifiers

* `eotg_nc_national_mourning`

---

## Event: Vice President Faces Distrust

### Trigger

* VP succession

### Description

Some politicians question the legitimacy of succession.

### Outcomes

#### Rally Public Support

* legitimacy gain

#### Negotiate with Senate

* Senate support gain

#### Use Emergency Authority

* political backlash risk

---

## Event: Former President Becomes Kingmaker

### Trigger

* former president alive

### Description

A former President influences the next election heavily.

### Outcomes

#### Seek Their Endorsement

* campaign bonuses

#### Undermine Their Influence

* intrigue opportunity

#### Build Coalition Together

* alliance bonus

---

# EVENT CATEGORY — IDEOLOGICAL POLITICS

---

## Event: Debate Over Federal Authority

### Trigger

* strong States
* weak presidency

### Description

Politicians argue over centralized power.

### Outcomes

#### Strengthen Federal Government

* authority gain

#### Protect State Rights

* State loyalty gain

#### Seek Compromise

* balanced modifiers

---

## Event: Militarists Gain Influence

### Trigger

* active wars
* PMC influence

### Description

Hardliners demand stronger military policies.

### Outcomes

#### Support Militarization

* military bonuses

#### Resist Militarists

* legitimacy gain

#### Use Militarists Politically

* Senate shifts

---

## Event: Civil Rights Debate

### Trigger

* multicultural tensions

### Description

Politicians argue over equal treatment policies.

### Outcomes

#### Expand Rights

* legitimacy gain
* conservative anger

#### Maintain Current Policies

* stability

#### Restrict Rights

* unrest risk

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: Constitutional Crisis

### Trigger

* contested election
* emergency powers abuse
* severe Senate hostility

### Description

The republic faces a legitimacy crisis over constitutional authority.

### Outcomes

#### Respect Constitutional Limits

* legitimacy gain

#### Expand Presidential Authority

* authoritarian drift

#### Let the Senate Decide

* instability risk

---

## Event: The Republic Stands United

### Trigger

* highly successful presidency

### Description

Political factions temporarily unite behind the republic.

### Outcomes

#### Strengthen Institutions

* stability bonus

#### Build Presidential Legacy

* prestige gain

#### Push Major Reforms

* reform opportunity

### Modifier

* `eotg_nc_republic_united`

---

## Event: Democracy Begins to Fail

### Trigger

* extreme corruption
* repeated crises

### Description

Citizens begin losing faith in democratic governance itself.

### Outcomes

#### Restore Trust

* difficult reform path

#### Exploit the Chaos

* authoritarian bonuses

#### Let the System Rot

* fragmentation risk
# New Cauldron Democracy Government Event Design Document

## Phase 2 — Senate Corruption, Campaign Warfare, and Democratic Fragmentation

### Purpose: Expand political maneuvering, campaign systems, factional democracy, and institutional decay mechanics

---

# EVENT CATEGORY — SENATE FACTIONALISM

---

## Event: Senate Coalition Collapses

### Trigger

* unstable political alliance
* failed legislation

### Description

A fragile coalition fractures during negotiations.

### Outcomes

#### Rebuild the Coalition

* diplomacy challenge

#### Punish Defectors

* political hostility increase

#### Form a New Coalition

* faction shift

### Modifiers

* `eotg_nc_broken_coalition`

---

## Event: Senators Trade Favors

### Trigger

* major vote approaching

### Description

Political backroom deals spread through the Senate.

### Outcomes

#### Participate in the Deals

* vote support gain
* corruption increase

#### Expose the Corruption

* legitimacy gain

#### Manipulate Both Sides

* hooks gained

---

## Event: Independent Senators Refuse Alignment

### Trigger

* fractured Senate

### Description

Several Senators reject major political blocs.

### Outcomes

#### Court Their Support

* diplomacy challenge

#### Bribe Them Quietly

* corruption risk

#### Threaten Political Isolation

* opinion penalties

---

# EVENT CATEGORY — CAMPAIGN WARFARE

---

## Event: Smear Campaign Begins

### Trigger

* aggressive election strategy

### Description

Political operatives launch attacks against rival candidates.

### Outcomes

#### Use Real Scandals

* legitimacy-safe attack

#### Fabricate Evidence

* intrigue bonuses
* exposure risk

#### Publicly Distance Yourself

* diplomacy gain

### Modifiers

* `eotg_nc_smear_campaign`

---

## Event: Campaign Rally Turns Violent

### Trigger

* tense election season

### Description

Supporters clash during a public event.

### Outcomes

#### Calm the Crowd

* diplomacy gain

#### Blame Rival Agitators

* political hostility gain

#### Encourage the Chaos

* instability increase

---

## Event: Secret Donors Offer Support

### Trigger

* election campaign active

### Description

Wealthy interests offer campaign financing.

### Outcomes

#### Accept the Funding

* campaign strength gain
* future obligations

#### Refuse the Money

* legitimacy gain

#### Secretly Blackmail the Donors

* hooks gained

---

# EVENT CATEGORY — POLITICAL SCANDALS

---

## Event: Private Communications Leak

### Trigger

* intrigue failure
* rival sabotage

### Description

Damaging private messages become public.

### Outcomes

#### Deny Authenticity

* intrigue challenge

#### Apologize Publicly

* legitimacy mitigation

#### Leak Rival Information Too

* scandal escalation

### Modifiers

* `eotg_nc_scandal_cycle`

---

## Event: Family Corruption Allegations

### Trigger

* wealthy ruling family

### Description

Accusations spread that relatives profit from political office.

### Outcomes

#### Launch Investigation

* legitimacy gain

#### Protect the Family

* corruption increase

#### Sacrifice a Relative Politically

* stability recovery

---

## Event: Senate Ethics Investigation

### Trigger

* repeated corruption scandals

### Description

A Senate committee investigates misconduct.

### Outcomes

#### Cooperate Fully

* legitimacy gain

#### Obstruct the Investigation

* intrigue bonuses
* major risk

#### Manipulate the Committee

* political influence gain

---

# EVENT CATEGORY — FEDERAL VS STATE POWER

---

## Event: State Leaders Challenge Federal Authority

### Trigger

* low federal legitimacy

### Description

Powerful States publicly resist national authority.

### Outcomes

#### Assert Federal Supremacy

* authority gain
* rebellion risk

#### Negotiate State Privileges

* stability gain

#### Secretly Divide the States

* intrigue opportunity

---

## Event: State Militia Refuses Orders

### Trigger

* military tensions

### Description

Regional forces refuse federal deployment.

### Outcomes

#### Force Compliance

* civil conflict risk

#### Allow Temporary Refusal

* weakness perception

#### Replace Regional Leadership

* instability risk

---

## Event: Wealthier States Demand More Influence

### Trigger

* unequal economy

### Description

Powerful States argue they deserve greater political power.

### Outcomes

#### Expand Their Influence

* elite support gain

#### Preserve Equal Representation

* legitimacy gain

#### Manipulate the Rivalries

* intrigue opportunities

---

# EVENT CATEGORY — PRESIDENTIAL AUTHORITY

---

## Event: Executive Orders Expand

### Trigger

* weak Senate support

### Description

The President increasingly governs through executive action.

### Outcomes

#### Expand Executive Power

* authority gain
* Senate anger

#### Use Limited Orders

* balanced stability

#### Return Power to Senate

* legitimacy gain

### Modifiers

* `eotg_nc_executive_expansion`

---

## Event: Senate Threatens Censure

### Trigger

* controversial presidency

### Description

Opponents seek formal condemnation of presidential conduct.

### Outcomes

#### Negotiate with Moderates

* diplomacy challenge

#### Attack the Senate Publicly

* political escalation

#### Offer Political Concessions

* support recovery

---

## Event: Presidential Inner Circle Gains Influence

### Trigger

* long presidency

### Description

Close advisors dominate decision-making.

### Outcomes

#### Empower Trusted Advisors

* governance bonuses

#### Rotate Advisors Frequently

* stability gain

#### Allow Factional Competition

* intrigue growth

---

# EVENT CATEGORY — MEDIA & PUBLIC CONTROL

---

## Event: Media Empire Backs a Candidate

### Trigger

* election period

### Description

A powerful media organization endorses a political figure.

### Outcomes

#### Accept the Support

* campaign boost

#### Keep Distance Publicly

* legitimacy gain

#### Secretly Manipulate Coverage

* intrigue bonuses

---

## Event: Public Protests Spread

### Trigger

* low legitimacy
* scandal or war fatigue

### Description

Large demonstrations erupt across major districts.

### Outcomes

#### Address the Public

* diplomacy challenge

#### Suppress the Demonstrations

* dread gain

#### Ignore the Protesters

* unrest growth

### Modifiers

* `eotg_nc_mass_protests`

---

## Event: Propaganda Campaign Begins

### Trigger

* falling approval

### Description

The administration launches mass messaging campaigns.

### Outcomes

#### Patriotic Messaging

* legitimacy gain

#### Fear-Based Messaging

* authority gain

#### Reformist Messaging

* moderate stability

---

# EVENT CATEGORY — MILITARY & DEMOCRACY

---

## Event: Generals Enter Politics

### Trigger

* prolonged wars

### Description

Military leaders gain political ambitions.

### Outcomes

#### Encourage Their Participation

* military support gain

#### Keep Military Separate

* legitimacy gain

#### Use Them as Political Allies

* faction bonuses

---

## Event: Veterans Demand Representation

### Trigger

* major wars ended

### Description

Veterans demand political recognition and reform.

### Outcomes

#### Expand Veteran Benefits

* loyalty gain

#### Ignore the Veterans

* unrest increase

#### Use Veterans Politically

* election bonuses

---

## Event: Military Loyalty Questioned

### Trigger

* constitutional crisis

### Description

Politicians fear military leaders may ignore civilian authority.

### Outcomes

#### Reinforce Civilian Oversight

* legitimacy gain

#### Reward Military Leadership

* military loyalty gain

#### Purge Dangerous Officers

* instability risk

---

# EVENT CATEGORY — ELECTION NIGHT CRISES

---

## Event: Election Fraud Accusations

### Trigger

* close election

### Description

Candidates accuse each other of manipulating votes.

### Outcomes

#### Demand Recounts

* legitimacy challenge

#### Reject the Accusations

* stability risk

#### Secretly Manipulate Results

* intrigue escalation

---

## Event: Senate Refuses Election Outcome

### Trigger

* highly contested election

### Description

Some Senators reject the declared winner.

### Outcomes

#### Negotiate Recognition

* diplomacy challenge

#### Pressure the Senate

* political escalation

#### Threaten Emergency Powers

* legitimacy collapse risk

---

## Event: Riots After the Election

### Trigger

* extreme polarization

### Description

Violence spreads after election results are announced.

### Outcomes

#### Call for Unity

* diplomacy gain

#### Deploy Security Forces

* control gain

#### Blame Political Rivals

* faction escalation

---

# EVENT CATEGORY — DEMOCRATIC IDEOLOGY

---

## Event: Debate Over the Republic’s Future

### Trigger

* repeated instability

### Description

Politicians debate whether the republic still works.

### Outcomes

#### Defend Democracy

* legitimacy gain

#### Advocate Strong Executive Rule

* authority bonuses

#### Demand Constitutional Reform

* reform chain unlock

---

## Event: Populist Movement Emerges

### Trigger

* public dissatisfaction

### Description

A charismatic populist gains mass support.

### Outcomes

#### Embrace the Movement

* public support gain
* elite anger

#### Resist Populism

* institutional support gain

#### Manipulate the Populists

* intrigue bonuses

---

## Event: Political Extremists Enter Senate

### Trigger

* instability high

### Description

Radical factions gain political representation.

### Outcomes

#### Isolate the Extremists

* stability gain

#### Cooperate Temporarily

* short-term support

#### Exploit Them Against Rivals

* long-term instability

---

# EVENT CATEGORY — RARE HIGH-IMPACT EVENTS

---

## Event: Senate Walkout

### Trigger

* severe political polarization

### Description

A large group of Senators abandons proceedings entirely.

### Outcomes

#### Negotiate Their Return

* diplomacy challenge

#### Govern Without Them

* legitimacy crisis

#### Arrest the Leaders

* authoritarian escalation

---

## Event: The Republic Nearly Breaks

### Trigger

* simultaneous crises

### Description

The democratic system teeters on collapse.

### Outcomes

#### National Unity Government

* temporary stability

#### Presidential Emergency Rule

* authoritarian path

#### Fragmentation of the Republic

* secession risks

---

## Event: A Golden Age of Democracy

### Trigger

* highly successful administration

### Description

The republic experiences unusual political unity and prosperity.

### Outcomes

#### Strengthen Institutions

* stability bonuses

#### Expand Federal Authority

* authority gain

#### Decentralize Power Peacefully

* State loyalty bonuses

### Modifier

* `eotg_nc_democratic_golden_age`
# New Cauldron Democracy Government Event Design Document

## Phase 3 — Decision Chains, Constitutional Power Struggles, and Democratic Endgame Systems

### Purpose: Create active democratic gameplay loops around elections, Senate negotiation, institutional survival, and authoritarian drift

---

# DECISION CHAIN — BUILD A SENATE COALITION

## Decision: `eotg_nc_build_coalition`

### Requirements

* low Senate support
* important legislation or war vote pending

### Immediate Effects

* coalition negotiations begin

---

## Event: Coalition Negotiations Begin

### Description

Political factions gather to negotiate support for the administration.

### Outcomes

#### Offer Policy Concessions

* Senate support gain

#### Offer Political Appointments

* loyalty modifiers

#### Pressure Moderate Senators

* political hostility risk

### Modifiers

* `eotg_nc_coalition_negotiations`

---

## Event: Coalition Members Demand More

### Trigger

* unstable coalition

### Description

Supporting Senators demand additional favors.

### Outcomes

#### Grant More Concessions

* coalition stability

#### Refuse Their Demands

* coalition fracture risk

#### Secretly Divide Coalition Leaders

* intrigue opportunities

---

## Event: Coalition Secured

### Trigger

* successful negotiations

### Description

A governing coalition formally supports the administration.

### Outcomes

#### Stable Governing Majority

* Senate bonuses

#### Fragile Alliance

* temporary stability only

#### Corrupt Coalition Network

* corruption growth
* strong legislative power

---

# DECISION CHAIN — LAUNCH PRESIDENTIAL CAMPAIGN

## Decision: `eotg_nc_launch_campaign`

### Requirements

* election approaching

### Immediate Effects

* campaign season begins

---

## Event: Campaign Headquarters Mobilized

### Description

Strategists, donors, and organizers begin national campaigning.

### Outcomes

#### Grassroots Campaign

* public support gain

#### Elite Donor Campaign

* financial advantages

#### Aggressive Attack Campaign

* intrigue bonuses

### Modifiers

* `eotg_nc_active_campaign`

---

## Event: Debate Performance Shapes Election

### Trigger

* active campaign

### Description

Candidates face each other before the public.

### Outcomes

#### Inspire the Public

* legitimacy gain

#### Humiliate Opponents

* rival support reduction

#### Manipulate Media Coverage

* intrigue advantage

---

## Event: Campaign Exhaustion Sets In

### Trigger

* prolonged election cycle

### Description

Candidates and staff become exhausted and desperate.

### Outcomes

#### Push Harder

* campaign strength increase
* scandal risk

#### Slow the Campaign

* reduced momentum

#### Delegate Operations

* advisor influence increases

---

# DECISION CHAIN — PASS MAJOR LEGISLATION

## Decision: `eotg_nc_pass_legislation`

### Requirements

* Senate support threshold

### Immediate Effects

* legislative battle begins

---

## Event: Senate Committees Debate the Bill

### Description

Committees reshape and weaken legislation.

### Outcomes

#### Accept Amendments

* easier passage

#### Fight for Original Bill

* political conflict

#### Secretly Bribe Committee Leaders

* intrigue opportunities

### Modifiers

* `eotg_nc_legislative_battle`

---

## Event: Public Pressure Builds

### Trigger

* controversial legislation

### Description

Citizens pressure Senators over the proposal.

### Outcomes

#### Mobilize Public Support

* vote pressure increase

#### Ignore Public Opinion

* legitimacy loss

#### Manipulate Public Messaging

* propaganda bonuses

---

## Event: The Vote Decides Everything

### Trigger

* final Senate vote

### Description

The Senate votes on the legislation.

### Outcomes

#### Bill Passes Cleanly

* legitimacy gain

#### Narrow Passage

* political resentment

#### Catastrophic Failure

* coalition collapse risk

---

# DECISION CHAIN — DECLARE EXECUTIVE EMERGENCY

Authoritarian drift system.

---

## Decision: `eotg_nc_executive_emergency`

### Requirements

* national crisis
* low stability OR active war

### Immediate Effects

* emergency powers activated

---

## Event: Emergency Powers Announced

### Description

The President temporarily bypasses constitutional limitations.

### Outcomes

#### Limited Emergency Rule

* moderate authority increase

#### Full Executive Control

* major legitimacy loss

#### Promise Immediate Restoration

* softer penalties

### Modifiers

* `eotg_nc_emergency_government`

---

## Event: Senate Resistance Grows

### Trigger

* emergency powers active

### Description

Opposition Senators fear dictatorship.

### Outcomes

#### Negotiate Limits

* stability gain

#### Threaten Opposition

* dread-style pressure

#### Arrest Conspirators

* authoritarian escalation

---

## Event: Citizens Fear Tyranny

### Trigger

* prolonged emergency powers

### Description

Public trust in democracy weakens.

### Outcomes

#### Restore Constitutional Order

* legitimacy recovery

#### Expand Emergency Authority

* authoritarian path progress

#### Distract the Public

* propaganda effects

---

# DECISION CHAIN — INVESTIGATE CORRUPTION

Anti-corruption reform system.

---

## Decision: `eotg_nc_investigate_corruption`

### Requirements

* corruption above threshold

### Immediate Effects

* investigation chain begins

---

## Event: Investigators Uncover Networks

### Description

Massive political corruption is revealed.

### Outcomes

#### Prosecute the Corrupt

* legitimacy gain
* elite anger

#### Protect Political Allies

* corruption persists

#### Use Evidence for Blackmail

* hooks gained

### Modifiers

* `eotg_nc_anti_corruption_probe`

---

## Event: Powerful Senators Resist Investigation

### Trigger

* corruption tied to elites

### Description

Influential politicians attempt to sabotage investigations.

### Outcomes

#### Expand the Investigation

* political conflict

#### Compromise with Elites

* reduced reform impact

#### Secretly Remove Evidence

* intrigue bonuses

---

## Event: Public Trust Begins to Recover

### Trigger

* successful reforms

### Description

Citizens regain confidence in institutions.

### Outcomes

#### Strengthen Institutions

* stability bonuses

#### Expand Reform Agenda

* reform momentum

#### Declare Victory Early

* smaller gains

---

# DECISION CHAIN — FEDERALIZE THE REPUBLIC

Centralization path.

---

## Decision: `eotg_nc_federalize_republic`

### Requirements

* strong presidency
* weak State resistance

### Immediate Effects

* federal authority expansion begins

---

## Event: States Resist Centralization

### Description

Regional governments fear loss of autonomy.

### Outcomes

#### Force Centralization

* authority gain
* rebellion risk

#### Negotiate Compromise

* slower progress

#### Buy State Loyalty

* gold cost

### Modifiers

* `eotg_nc_federal_expansion`

---

## Event: Senate Debates National Authority

### Trigger

* federalization active

### Description

Senators argue over the future of the republic.

### Outcomes

#### Strengthen Federal Institutions

* stability gain

#### Preserve State Rights

* decentralization pressure

#### Manipulate the Debate

* intrigue opportunities

---

## Event: National Bureaucracy Expands

### Trigger

* successful centralization

### Description

Federal administration grows dramatically.

### Outcomes

#### Efficient Bureaucracy

* governance bonuses

#### Corrupt Bureaucratic Networks

* corruption growth

#### Militarized Administration

* authority bonuses

---

# DECISION CHAIN — APPEAL TO THE PUBLIC

Mass legitimacy system.

---

## Decision: `eotg_nc_appeal_public`

### Requirements

* low approval OR election approaching

### Immediate Effects

* public campaign begins

---

## Event: National Address Broadcast

### Description

The President speaks directly to the republic.

### Outcomes

#### Inspirational Speech

* legitimacy gain

#### Fear-Based Messaging

* authority gain

#### Reformist Vision

* public optimism

### Modifiers

* `eotg_nc_public_campaign`

---

## Event: Public Reaction Divides

### Trigger

* controversial messaging

### Description

Citizens respond very differently to the speech.

### Outcomes

#### Embrace Polarization

* loyalist support gain

#### Moderate the Message

* stability increase

#### Attack Critics

* political escalation

---

## Event: Massive Public Demonstrations

### Trigger

* failed appeal

### Description

Huge demonstrations erupt nationwide.

### Outcomes

#### Meet Protest Leaders

* diplomacy challenge

#### Deploy Security Forces

* unrest suppression

#### Ignore the Demonstrations

* instability increase

---

# DECISION CHAIN — REFORM THE CONSTITUTION

Late-game transformation system.

---

## Decision: `eotg_nc_reform_constitution`

### Requirements

* severe instability OR major legitimacy mandate

### Immediate Effects

* constitutional convention begins

---

## Event: Constitutional Convention Opens

### Description

Delegates gather to redefine the republic.

### Outcomes

#### Strengthen Democracy

* legitimacy bonuses

#### Strengthen Executive Power

* authoritarian drift

#### Redesign Federal Structure

* State relationship changes

### Modifiers

* `eotg_nc_constitutional_convention`

---

## Event: Delegates Turn Against Each Other

### Trigger

* polarized politics

### Description

Convention debates become vicious and unstable.

### Outcomes

#### Force Consensus

* legitimacy risk

#### Allow Open Debate

* instability increase

#### Secretly Manipulate Delegates

* intrigue opportunities

---

## Event: Birth of the New Republic

### Trigger

* successful reform

### Description

A transformed political system emerges.

### Outcomes

#### Democratic Renewal

* stability bonuses

#### Strong Presidential Republic

* authority bonuses

#### Fragmented Compromise Republic

* mixed modifiers

---

# FINAL DESIGN NOTE

New Cauldron Democracy now supports:

* Senate coalition politics
* election campaigns
* legislation battles
* corruption investigations
* public opinion systems
* federal vs state conflicts
* emergency powers
* constitutional crises
* democratic reform systems
* authoritarian drift paths

Strong thematic identity:

| New Cauldron Democracy | Corporation         |
| ---------------------- | ------------------- |
| elected leadership     | executive oligarchy |
| Senate coalitions      | board manipulation  |
| public legitimacy      | profit legitimacy   |
| constitutional crises  | corporate coups     |

| New Cauldron Democracy | Elven Monarchy          |
| ---------------------- | ----------------------- |
| evolving institutions  | ancient tradition       |
| public elections       | aristocratic succession |
| ideological pluralism  | cultural hierarchy      |
| federal politics       | noble court politics    |

---------------------------------------------------------

# Supplemental Government Event Expansion Pack

## Additional Event Ecosystems to Fix Missing Gameplay Gaps

### Purpose

These events directly address missing gameplay systems identified in the government assessment.

Format optimized for Claude Code implementation planning.

---

# 1. FRINGE GOVERNMENT — SURVIVAL & CLAN CULTURE EXPANSION

---

# EVENT CATEGORY — FRONTIER SURVIVAL

---

## Event: Fuel Reserves Run Dry

### Description

Critical fuel reserves are nearly exhausted after extended raids and migration.

### Relevant Traits

* Greedy
* Temperate
* Reckless
* Paranoid

### Choices

#### Seize Fuel by Force

* immediate raid opportunity
* nearby rulers angered
* martial prestige gain

#### Ration the Reserves

* army effectiveness penalty
* stability gain

#### Abandon Heavy Equipment

* lose military bonuses
* migration speed increase

### Outcomes

Modifier:

* `eotg_fringe_fuel_shortage`

---

## Event: The Hungry Camps

### Description

Food shortages spread through the migrating camps.

### Relevant Traits

* Compassionate
* Callous
* Generous
* Sadistic

### Choices

#### Feed the Warriors First

* military morale gain
* civilian unrest

#### Equal Distribution

* stability gain
* army morale penalty

#### Raid Nearby Settlements

* loot gain
* neighboring hostility

---

## Event: Ship Graveyard Salvage

### Description

Scavengers discover ancient wreckage filled with salvageable materials.

### Relevant Traits

* Greedy
* Brave
* Diligent

### Choices

#### Strip Everything Valuable

* gold gain

#### Preserve Useful Technology

* innovation modifier

#### Fight Over the Salvage

* clan rivalry escalation

---

# EVENT CATEGORY — WARBAND CULTURE

---

## Event: Feast of Victorious Raiders

### Description

Warriors gather after successful raids to celebrate conquest.

### Relevant Traits

* Gregarious
* Wrathful
* Ambitious

### Choices

#### Reward the Greatest Warriors

* knight loyalty gain

#### Glorify the Clan

* prestige gain

#### Humiliate Weak Fighters

* dread gain

---

## Event: Blood Feud Rekindled

### Description

Ancient clan grievances erupt again.

### Relevant Traits

* Vengeful
* Forgiving
* Arbitrary

### Choices

#### Demand Revenge

* rivalry war chain

#### Negotiate Compensation

* diplomacy gain

#### Ignore the Insult

* prestige loss

---

## Event: Trial by Combat for Leadership

### Description

Warriors demand disputes be settled through combat.

### Relevant Traits

* Brave
* Craven
* Wrathful

### Choices

#### Fight Personally

* prestige gain
* injury risk

#### Appoint a Champion

* knight interaction

#### Refuse the Duel

* legitimacy loss

---

# 2. GOB-CORP GOVERNMENT — LABOR & MARKET CHAOS EXPANSION

---

# EVENT CATEGORY — WORKER UNREST

---

## Event: Goblin Workers Riot

### Description

Factory workers riot over impossible quotas and deadly working conditions.

### Relevant Traits

* Greedy
* Compassionate
* Sadistic

### Choices

#### Crush the Riot

* dread gain
* production restored

#### Improve Conditions Slightly

* gold cost
* stability gain

#### Promise Bonuses You Cannot Afford

* temporary calm
* future unrest

### Outcomes

Modifier:

* `eotg_gobcorp_worker_riots`

---

## Event: Unsafe Machinery Explosion

### Description

A poorly maintained industrial complex explodes catastrophically.

### Relevant Traits

* Lazy
* Diligent
* Callous

### Choices

#### Cover Up the Disaster

* intrigue challenge

#### Pay Compensation

* gold cost
* legitimacy gain

#### Blame the Workers

* productivity maintained
* unrest gain

---

## Event: Workers Sabotage Production

### Description

Disgruntled workers intentionally damage production lines.

### Relevant Traits

* Paranoid
* Wrathful
* Calm

### Choices

#### Execute the Saboteurs

* dread gain

#### Investigate Management Abuse

* stability gain

#### Replace Workers Entirely

* production disruption

---

# EVENT CATEGORY — MARKET CHAOS

---

## Event: Speculative Bubble Forms

### Description

Executives inflate absurd market expectations.

### Relevant Traits

* Greedy
* Arbitrary
* Temperate

### Choices

#### Push the Bubble Higher

* temporary massive profits

#### Quietly Sell Assets

* personal gold gain

#### Warn Investors

* legitimacy gain

---

## Event: Market Collapse Panic

### Description

A financial bubble bursts violently.

### Relevant Traits

* Calm
* Paranoid
* Greedy

### Choices

#### Bail Out Major Investors

* stability gain
* gold loss

#### Let the Market Burn

* chaos increases

#### Blame Rival Corporations

* intrigue opportunity

---

## Event: Insider Trading Scandal

### Description

Executives secretly manipulated markets for profit.

### Relevant Traits

* Deceitful
* Honest
* Arbitrary

### Choices

#### Punish Executives

* legitimacy gain

#### Join the Scheme

* gold gain

#### Destroy the Evidence

* intrigue challenge

---

# 3. CORPORATION GOVERNMENT — BUREAUCRACY & WORKER ALIENATION

---

# EVENT CATEGORY — BUREAUCRATIC DYSTOPIA

---

## Event: Compliance Review Paralysis

### Description

Corporate bureaucracy delays critical decisions endlessly.

### Relevant Traits

* Diligent
* Lazy
* Patient

### Choices

#### Expand Oversight Further

* safety gain
* efficiency loss

#### Remove Bureaucratic Layers

* efficiency gain
* scandal risk

#### Ignore the Delays

* future crisis risk

---

## Event: Endless Paperwork Crisis

### Description

Executives drown in administrative complexity.

### Relevant Traits

* Stressed
* Diligent
* Impatient

### Choices

#### Hire More Administrators

* gold cost

#### Automate Administration

* efficiency gain

#### Force Longer Work Hours

* burnout risk

---

# EVENT CATEGORY — WORKER ALIENATION

---

## Event: Workers Collapse from Exhaustion

### Description

Employees suffer mass burnout after extreme productivity demands.

### Relevant Traits

* Compassionate
* Callous
* Ambitious

### Choices

#### Reduce Workloads

* productivity loss
* stability gain

#### Push Harder

* short-term production gain

#### Replace Exhausted Workers

* unrest gain

---

## Event: Automation Protest Movement

### Description

Workers protest mass replacement by automated systems.

### Relevant Traits

* Cynical
* Compassionate
* Greedy

### Choices

#### Suppress the Protest

* dread gain

#### Slow Automation

* stability gain

#### Accelerate Replacement

* economic gain
* unrest growth

---

# 4. CARTEL GOVERNMENT — SHADOW GOVERNANCE SYSTEMS

---

# EVENT CATEGORY — SHADOW JUSTICE

---

## Event: Civilians Ask the Cartel for Justice

### Description

Locals seek cartel intervention against corrupt officials.

### Relevant Traits

* Just
* Arbitrary
* Sadistic

### Choices

#### Deliver Brutal Justice

* local loyalty gain
* dread gain

#### Exploit Both Sides

* gold gain

#### Refuse Involvement

* legitimacy loss

---

## Event: Cartel Charity Distribution

### Description

The cartel distributes food and medicine to poor districts.

### Relevant Traits

* Generous
* Cynical
* Compassionate

### Choices

#### Genuine Aid

* civilian loyalty gain

#### Demand Loyalty in Return

* control gain

#### Use Aid for Propaganda

* prestige gain

---

# EVENT CATEGORY — NARCOTICS COLLAPSE

---

## Event: Overdose Epidemic

### Description

Mass addiction deaths destabilize controlled districts.

### Relevant Traits

* Compassionate
* Greedy
* Callous

### Choices

#### Continue Distribution

* gold gain

#### Restrict Supply

* stability gain

#### Blame Rival Suppliers

* intrigue escalation

---

# 5. ELVEN MONARCHY — IMMORTALITY & CIVILIZATIONAL DECLINE

---

# EVENT CATEGORY — IMMORTAL MEMORY

---

## Event: The King Remembers the Insult

### Description

The ruler still remembers an insult from centuries ago.

### Relevant Traits

* Vengeful
* Forgiving
* Arrogant

### Choices

#### Renew the Feud

* rivalry escalation

#### Finally Let Go

* stress loss

#### Secretly Manipulate Descendants

* intrigue bonuses

---

## Event: Ancient Ruler Detached from Reality

### Description

The ruler struggles to understand modern generations.

### Relevant Traits

* Stubborn
* Wise
* Cynical

### Choices

#### Ignore Modern Concerns

* legitimacy loss

#### Listen to Younger Nobles

* innovation gain

#### Retreat into Tradition

* noble approval gain

---

# EVENT CATEGORY — CIVILIZATIONAL DECAY

---

## Event: Empty Noble Halls

### Description

Ancient palaces grow silent as noble families shrink.

### Relevant Traits

* Melancholic
* Content
* Ambitious

### Choices

#### Preserve the Empty Traditions

* legitimacy gain

#### Invite New Bloodlines

* noble anger

#### Abandon Old Estates

* economic recovery

---

## Event: Declining Birth Rates

### Description

The aristocracy quietly fears demographic collapse.

### Relevant Traits

* Family Focus
* Ambitious
* Calm

### Choices

#### Encourage Noble Families

* fertility bonuses

#### Ignore the Problem

* long-term decline

#### Relax Bloodline Restrictions

* traditionalist anger

---

# 6. PMC GOVERNMENT — HUMAN COST OF WAR

---

# EVENT CATEGORY — VETERAN TRAUMA

---

## Event: Operators Cannot Sleep

### Description

Veterans suffer psychological collapse after endless warfare.

### Relevant Traits

* Compassionate
* Callous
* Brave

### Choices

#### Fund Recovery Programs

* gold cost
* stability gain

#### Ignore Their Weakness

* discipline preserved
* future unrest

#### Use Drugs to Maintain Performance

* temporary military bonuses

---

## Event: Violent Veteran Incident

### Description

Traumatized operators lash out violently in civilian districts.

### Relevant Traits

* Wrathful
* Calm
* Sadistic

### Choices

#### Arrest the Veterans

* discipline gain

#### Protect Them Publicly

* operator loyalty gain

#### Cover Up the Incident

* intrigue challenge

---

# EVENT CATEGORY — CONTRACTOR CULTURE

---

## Event: Camp Followers Exploit Soldiers

### Description

Civilian contractors profit from desperate operators.

### Relevant Traits

* Greedy
* Just
* Cynical

### Choices

#### Regulate the Camps

* legitimacy gain

#### Ignore Exploitation

* gold gain

#### Let Officers Profit Too

* corruption increase

---

# 7. NEW CAULDRON DEMOCRACY — PARTIES & JUDICIAL SYSTEMS

---

# EVENT CATEGORY — POLITICAL PARTIES

---

## Event: Party Convention Erupts into Chaos

### Description

Delegates fight over party leadership and policy direction.

### Relevant Traits

* Gregarious
* Wrathful
* Calm

### Choices

#### Unite the Delegates

* party stability gain

#### Support a Radical Faction

* polarization increase

#### Manipulate the Convention

* intrigue bonuses

---

## Event: Party Schism Threatens Elections

### Description

Internal divisions threaten electoral collapse.

### Relevant Traits

* Diplomatic
* Arbitrary
* Ambitious

### Choices

#### Negotiate Unity

* stability gain

#### Purge Dissidents

* legitimacy risk

#### Accept the Split

* faction fragmentation

---

# EVENT CATEGORY — JUDICIAL POWER

---

## Event: Supreme Court Challenges Executive Authority

### Description

The judiciary rules against executive actions.

### Relevant Traits

* Arbitrary
* Just
* Wrathful

### Choices

#### Respect the Ruling

* legitimacy gain

#### Attack the Court Publicly

* authoritarian drift

#### Pressure the Judges

* intrigue escalation

---

## Event: Judicial Appointment Battle

### Description

Political factions fight over court appointments.

### Relevant Traits

* Ambitious
* Patient
* Cynical

### Choices

#### Appoint Loyal Judges

* authority gain

#### Appoint Independent Judges

* legitimacy gain

#### Secretly Blackmail Candidates

* hooks gained

---

# EVENT CATEGORY — CIVILIAN MOVEMENTS

---

## Event: Student Protest Movement

### Description

Young activists demand sweeping reforms.

### Relevant Traits

* Compassionate
* Cynical
* Calm

### Choices

#### Support the Protesters

* reform momentum

#### Suppress Demonstrations

* unrest gain

#### Manipulate the Movement

* intrigue bonuses

---

## Event: Massive Labor Strike

### Description

Workers organize nationwide strikes against economic conditions.

### Relevant Traits

* Greedy
* Just
* Arbitrary

### Choices

#### Negotiate with Unions

* stability gain

#### Break the Strike

* economic disruption

#### Divide the Workers

* intrigue opportunity

# Supplemental Government Event Expansion Pack — Phase 2

## Advanced Missing Systems & Long-Term Emergent Gameplay

### Purpose

These events deepen long-term replayability, AI instability behavior, social ecosystems, and late-game narrative pressure.

---

# 1. FRINGE GOVERNMENT — MIGRATION & COLLAPSE PRESSURE

---

# EVENT CATEGORY — MIGRATION CHAOS

---

## Event: The Warband Wants to Move Again

### Description

Restless warriors demand migration toward richer territories.

### Relevant Traits

* Ambitious
* Content
* Wrathful

### Choices

#### Follow the Warband

* migration bonuses
* instability increase

#### Refuse to Move

* morale loss

#### Split the Clan

* realm fragmentation risk

### Outcomes

Modifier:

* `eotg_fringe_restless_warband`

---

## Event: Refugees Join the Camps

### Description

Desperate survivors beg to join the migrating clans.

### Relevant Traits

* Compassionate
* Xenophobic
* Greedy

### Choices

#### Accept Them

* manpower gain
* supply strain

#### Enslave the Refugees

* gold gain
* unrest risk

#### Turn Them Away

* prestige loss

---

## Event: Warlords Demand Independent Territory

### Description

Sub-commanders demand permanent control over conquered regions.

### Relevant Traits

* Ambitious
* Arbitrary
* Gregarious

### Choices

#### Grant Autonomy

* fragmentation pressure

#### Refuse Them

* rebellion risk

#### Encourage Rivalries Between Warlords

* intrigue bonuses

---

# EVENT CATEGORY — RAIDER SPIRITUALISM

---

## Event: Prophecy of Endless Raiding

### Description

Mystics claim the clan is destined to conquer endlessly.

### Relevant Traits

* Zealous
* Cynical
* Ambitious

### Choices

#### Embrace the Prophecy

* conquest bonuses

#### Exploit It Politically

* authority gain

#### Suppress the Prophets

* unrest increase

---

## Event: Spirits of the Fallen Warriors

### Description

Veterans claim the dead haunt the camps.

### Relevant Traits

* Brave
* Paranoid
* Compassionate

### Choices

#### Honor the Dead

* morale gain

#### Ignore Superstition

* stability risk

#### Use Fear to Control Warriors

* dread gain

---

# 2. GOB-CORP — INDUSTRIAL INSANITY

---

# EVENT CATEGORY — CORPORATE MAD SCIENCE

---

## Event: Experimental Product Catastrophe

### Description

A wildly unsafe product kills consumers across multiple markets.

### Relevant Traits

* Greedy
* Callous
* Diligent

### Choices

#### Recall the Product

* gold loss
* legitimacy gain

#### Deny Responsibility

* intrigue challenge

#### Sell Remaining Inventory Anyway

* huge short-term profits

### Outcomes

Modifier:

* `eotg_gobcorp_product_disaster`

---

## Event: Inventor Creates Something Horrifying

### Description

A goblin engineer unveils unstable but profitable technology.

### Relevant Traits

* Curious
* Arbitrary
* Greedy

### Choices

#### Mass Produce It

* economic bonuses
* disaster risk

#### Restrict Development

* stability gain

#### Sell It Abroad

* foreign instability chain

---

# EVENT CATEGORY — INDUSTRIAL HELL

---

## Event: Factory District Becomes Unlivable

### Description

Industrial pollution destroys entire urban districts.

### Relevant Traits

* Cynical
* Compassionate
* Lazy

### Choices

#### Ignore the Pollution

* productivity gain

#### Relocate Workers

* gold cost

#### Blame Competitors

* propaganda opportunity

---

## Event: Child Labor Profits Surge

### Description

Executives propose expanding child labor practices.

### Relevant Traits

* Sadistic
* Greedy
* Compassionate

### Choices

#### Expand Labor Exploitation

* productivity increase

#### Restrict the Practice

* legitimacy gain

#### Hide the Practice Carefully

* intrigue bonuses

---

# 3. CORPORATION — AI DYSTOPIA & SOCIAL COLLAPSE

---

# EVENT CATEGORY — MACHINE GOVERNANCE

---

## Event: Predictive Algorithm Recommends Purges

### Description

Corporate AI systems identify “potentially disloyal” employees.

### Relevant Traits

* Paranoid
* Rational
* Compassionate

### Choices

#### Trust the Algorithm

* scheme resistance gain
* unrest risk

#### Investigate Manually

* slower stability gain

#### Ignore the Recommendations

* future sabotage risk

### Outcomes

Modifier:

* `eotg_corporation_algorithmic_control`

---

## Event: AI Denies Essential Services

### Description

Automated systems cut support to entire populations deemed inefficient.

### Relevant Traits

* Callous
* Just
* Arbitrary

### Choices

#### Maintain Efficiency Standards

* economic gain

#### Override the System

* legitimacy gain

#### Hide the Decision

* intrigue challenge

---

# EVENT CATEGORY — CORPORATE SOCIAL DECAY

---

## Event: Citizens Forget Life Outside Corporate Rule

### Description

Entire generations grow up fully dependent on the corporation.

### Relevant Traits

* Ambitious
* Cynical
* Compassionate

### Choices

#### Encourage Dependency

* control bonuses

#### Promote Civic Identity

* legitimacy gain

#### Manipulate Dependency

* intrigue bonuses

---

## Event: Suicide Rates Rise in Corporate Zones

### Description

Despair spreads among exhausted workers.

### Relevant Traits

* Compassionate
* Callous
* Cynical

### Choices

#### Improve Conditions

* productivity loss
* stability gain

#### Launch Wellness Propaganda

* temporary stability

#### Ignore the Crisis

* future unrest

---

# 4. CARTEL — SHADOW STATE EVOLUTION

---

# EVENT CATEGORY — CRIMINAL GOVERNANCE

---

## Event: Entire Neighborhood Loyal to the Cartel

### Description

Local civilians trust cartel authority more than official governments.

### Relevant Traits

* Gregarious
* Cynical
* Arbitrary

### Choices

#### Protect the Neighborhood

* civilian loyalty gain

#### Exploit Their Dependence

* gold gain

#### Recruit Local Militias

* security bonuses

### Outcomes

Modifier:

* `eotg_cartel_shadow_community`

---

## Event: Cartel Judges Settle Disputes

### Description

Citizens increasingly rely on cartel arbitration instead of courts.

### Relevant Traits

* Just
* Arbitrary
* Sadistic

### Choices

#### Deliver Fair Judgments

* legitimacy gain

#### Favor Loyalists

* loyalty bonuses

#### Sell Verdicts for Profit

* corruption increase

---

# EVENT CATEGORY — CRIMINAL DECAY

---

## Event: Addiction Devastates Loyal Districts

### Description

Communities collapse under widespread narcotics abuse.

### Relevant Traits

* Compassionate
* Greedy
* Cynical

### Choices

#### Restrict Supply

* stability gain

#### Continue Profits

* gold gain

#### Militarize the District

* control gain

---

## Event: Children Raised by the Cartel

### Description

Young people increasingly idolize cartel culture.

### Relevant Traits

* Gregarious
* Sadistic
* Compassionate

### Choices

#### Encourage Recruitment

* manpower gain

#### Build Community Programs

* stability gain

#### Weaponize Youth Gangs

* unrest suppression

---

# 5. ELVEN MONARCHY — IMMORTAL DECAY & CULTURAL MELANCHOLY

---

# EVENT CATEGORY — IMMORTAL STAGNATION

---

## Event: The Nobles Have Discussed This for Centuries

### Description

Court debates repeat endlessly with no resolution.

### Relevant Traits

* Patient
* Stubborn
* Cynical

### Choices

#### Continue Deliberation

* stability gain
* reform slowdown

#### Force Action

* noble anger

#### Manipulate Endless Debate

* intrigue bonuses

### Outcomes

Modifier:

* `eotg_elven_eternal_deliberation`

---

## Event: Ancient Noble Refuses to Forget

### Description

A centuries-old noble still refuses reconciliation over ancient betrayal.

### Relevant Traits

* Vengeful
* Forgiving
* Arrogant

### Choices

#### Support Their Revenge

* faction escalation

#### Demand Reconciliation

* diplomacy challenge

#### Exploit Their Hatred

* intrigue gain

---

# EVENT CATEGORY — CULTURAL MELANCHOLY

---

## Event: Songs of a Dying Civilization

### Description

Artists mourn the slow fading of ancient elven greatness.

### Relevant Traits

* Melancholic
* Poet
* Cynical

### Choices

#### Celebrate the Old Ways

* legitimacy gain

#### Inspire Renewal

* innovation gain

#### Suppress Defeatism

* control gain

---

## Event: The Last Great Sculptor Dies

### Description

An irreplaceable master artist dies without students.

### Relevant Traits

* Learning Education
* Compassionate
* Arrogant

### Choices

#### Preserve Their Works

* prestige gain

#### Fund New Artists

* cultural renewal

#### Ignore Artistic Decline

* cultural decay grows

---

# 6. PMC — WAR ADDICTION & MILITARY SOCIETY

---

# EVENT CATEGORY — WAR ADDICTION

---

## Event: Operators Cannot Adapt to Peace

### Description

Veterans become unstable during prolonged peace.

### Relevant Traits

* Wrathful
* Calm
* Brave

### Choices

#### Find New Contracts

* war pressure increases

#### Expand Civilian Roles

* stability gain

#### Ignore the Problem

* unrest risk

### Outcomes

Modifier:

* `eotg_pmc_peace_instability`

---

## Event: Officers Secretly Provoke Border Conflict

### Description

Military leaders engineer incidents to restart warfare.

### Relevant Traits

* Ambitious
* Deceitful
* Cynical

### Choices

#### Approve Their Actions

* war opportunities

#### Punish the Officers

* discipline gain

#### Use the Conflict Politically

* authority gain

---

# EVENT CATEGORY — MILITARY CIVILIZATION

---

## Event: Children Raised in Military Academies

### Description

PMC culture reshapes childhood into military preparation.

### Relevant Traits

* Ambitious
* Callous
* Diligent

### Choices

#### Expand Academy Systems

* military quality gain

#### Moderate Militarization

* balanced stability

#### Encourage Civilian Education

* military anger

---

## Event: Operators Worship Legendary Commanders

### Description

Soldiers idolize military heroes more than institutions.

### Relevant Traits

* Ambitious
* Gregarious
* Arrogant

### Choices

#### Build Personality Cults

* loyalty gain
* coup risk

#### Emphasize Institutional Loyalty

* stability gain

#### Use Heroes for Recruitment

* manpower bonuses

---

# 7. NEW CAULDRON DEMOCRACY — PARTY MACHINES & MASS MOVEMENTS

---

# EVENT CATEGORY — PARTY MACHINES

---

## Event: Party Boss Controls the Delegates

### Description

A powerful political boss manipulates convention delegates.

### Relevant Traits

* Deceitful
* Gregarious
* Ambitious

### Choices

#### Work with the Boss

* campaign support gain

#### Break Their Influence

* political war begins

#### Secretly Blackmail Them

* hooks gained

### Outcomes

Modifier:

* `eotg_nc_party_machine`

---

## Event: Party Loyalists Demand Purges

### Description

Activists demand ideological purity inside the party.

### Relevant Traits

* Zealous
* Cynical
* Arbitrary

### Choices

#### Purge Moderates

* polarization increases

#### Preserve Coalition Unity

* stability gain

#### Manipulate the Factions

* intrigue bonuses

---

# EVENT CATEGORY — JUDICIAL CRISIS

---

## Event: Supreme Court Deadlock

### Description

The judiciary cannot decide a critical constitutional issue.

### Relevant Traits

* Patient
* Arbitrary
* Calm

### Choices

#### Respect Judicial Limits

* legitimacy gain

#### Pressure the Court

* authoritarian drift

#### Circumvent the Judiciary

* constitutional crisis risk

---

## Event: Judges Accused of Corruption

### Description

Evidence emerges that powerful judges accepted bribes.

### Relevant Traits

* Honest
* Deceitful
* Cynical

### Choices

#### Launch Investigations

* legitimacy gain

#### Protect Friendly Judges

* corruption growth

#### Use Scandal Against Rivals

* political advantage

---

# EVENT CATEGORY — MASS POLITICAL MOVEMENTS

---

## Event: Anti-War Demonstrations Sweep the Republic

### Description

Massive protests erupt against military intervention.

### Relevant Traits

* Compassionate
* Wrathful
* Calm

### Choices

#### Withdraw Support for War

* peace support gain

#### Crush the Demonstrations

* unrest increase

#### Manipulate Patriotism

* polarization growth

---

## Event: Radical Student Movement Emerges

### Description

Universities become centers of revolutionary politics.

### Relevant Traits

* Cynical
* Curious
* Zealous

### Choices

#### Allow Open Debate

* innovation gain

#### Suppress Radical Organizers

* unrest gain

#### Infiltrate the Movement

* intrigue bonuses


# Supplemental Government Event Expansion Pack — Phase 3

## Endgame Collapse Systems, Societal Transformation, and Emergent Disaster Chains

### Purpose

These systems create late-game pressure, emergent realm transformation, and AI instability patterns that keep governments dynamic over long campaigns.

---

# 1. FRINGE GOVERNMENT — TOTAL FRAGMENTATION & NOMADIC DESTINY

---

# EVENT CATEGORY — FRAGMENTATION CRISIS

---

## Event: The Clans No Longer Obey

### Description

Major warbands openly reject central leadership authority.

### Relevant Traits

* Arbitrary
* Wrathful
* Gregarious

### Choices

#### Crush the Dissidents

* civil war risk

#### Grant Clan Independence

* realm fragmentation

#### Let the Strongest Rule

* succession violence chain

### Outcomes

Modifier:

* `eotg_fringe_clan_breakdown`

---

## Event: The Great Splintering

### Description

Entire clans begin abandoning the greater confederation.

### Relevant Traits

* Ambitious
* Cynical
* Brave

### Choices

#### Hold the Confederation Together

* legitimacy challenge

#### Accept the Fragmentation

* peaceful breakup chance

#### Lead the Strongest Survivors

* elite warband bonuses

---

# EVENT CATEGORY — NOMADIC DESTINY

---

## Event: A New Frontier Is Discovered

### Description

Scouts discover distant vulnerable territories rich with opportunity.

### Relevant Traits

* Ambitious
* Brave
* Greedy

### Choices

#### Begin the Great Migration

* migration bonuses

#### Raid Instead of Settling

* loot bonuses

#### Ignore the Discovery

* prestige loss

---

## Event: Settlers vs Raiders

### Description

Some clans wish to settle permanently while others demand endless conquest.

### Relevant Traits

* Content
* Ambitious
* Stubborn

### Choices

#### Embrace Settlement

* stability gain
* reformation progress

#### Preserve Raider Traditions

* military bonuses

#### Split the Confederation

* faction split

---

# 2. GOB-CORP — ECONOMIC APOCALYPSE

---

# EVENT CATEGORY — TOTAL MARKET INSANITY

---

## Event: Hyper-Speculation Frenzy

### Description

Markets become completely detached from reality.

### Relevant Traits

* Greedy
* Lunatic
* Arbitrary

### Choices

#### Exploit the Frenzy

* enormous profits
* crash risk

#### Quietly Withdraw Assets

* personal gold gain

#### Attempt Regulation

* elite anger

### Outcomes

Modifier:

* `eotg_gobcorp_market_mania`

---

## Event: Shareholders Riot

### Description

Investors panic after catastrophic losses.

### Relevant Traits

* Wrathful
* Greedy
* Calm

### Choices

#### Promise Recovery

* temporary stability

#### Blame Rival Firms

* hostility increase

#### Sacrifice Executives

* legitimacy recovery

---

# EVENT CATEGORY — INDUSTRIAL COLLAPSE

---

## Event: Entire Factory Arcology Fails

### Description

A gigantic industrial district collapses due to neglect and greed.

### Relevant Traits

* Lazy
* Diligent
* Callous

### Choices

#### Evacuate Survivors

* gold cost

#### Continue Production Anyway

* productivity gain
* death toll increases

#### Hide the Scale of the Disaster

* intrigue challenge

---

## Event: Workers Form Armed Unions

### Description

Labor groups organize militant resistance.

### Relevant Traits

* Arbitrary
* Wrathful
* Compassionate

### Choices

#### Negotiate with Them

* stability gain

#### Hire Mercenaries

* violent suppression

#### Divide the Union Leaders

* intrigue bonuses

---

# 3. CORPORATION — TOTAL CORPORATE DYSTOPIA

---

# EVENT CATEGORY — MACHINE TYRANNY

---

## Event: Algorithmic Social Ranking

### Description

Corporate AI systems begin ranking citizens by economic value.

### Relevant Traits

* Rational
* Callous
* Compassionate

### Choices

#### Fully Implement Rankings

* efficiency bonuses

#### Limit the System

* legitimacy gain

#### Secretly Manipulate Rankings

* intrigue opportunities

### Outcomes

Modifier:

* `eotg_corporation_social_scoring`

---

## Event: AI Predicts Civil Unrest

### Description

Algorithms identify populations likely to rebel.

### Relevant Traits

* Paranoid
* Calm
* Arbitrary

### Choices

#### Preemptive Crackdowns

* control gain

#### Improve Conditions

* stability gain

#### Manipulate the Population

* propaganda bonuses

---

# EVENT CATEGORY — HUMAN COLLAPSE

---

## Event: Corporate Citizens Lose Purpose

### Description

Workers feel spiritually empty under endless corporate existence.

### Relevant Traits

* Cynical
* Compassionate
* Ambitious

### Choices

#### Increase Entertainment Consumption

* stability gain

#### Promote Corporate Identity

* control bonuses

#### Ignore the Crisis

* future unrest

---

## Event: Executive Class Detached from Humanity

### Description

Corporate elites no longer understand ordinary people.

### Relevant Traits

* Arrogant
* Cynical
* Compassionate

### Choices

#### Preserve Elite Isolation

* efficiency gain

#### Force Executive Exposure to Reality

* legitimacy gain

#### Weaponize Class Division

* authority gain

---

# 4. CARTEL — CRIMINAL STATE ENTRENCHMENT

---

# EVENT CATEGORY — CRIMINAL SOCIETY

---

## Event: Children Dream of Becoming Enforcers

### Description

Cartel culture dominates youth identity.

### Relevant Traits

* Gregarious
* Cynical
* Compassionate

### Choices

#### Encourage Recruitment

* manpower gain

#### Build Alternative Opportunities

* stability gain

#### Militarize Youth Crews

* unrest suppression

### Outcomes

Modifier:

* `eotg_cartel_criminal_generation`

---

## Event: Citizens Fear the Cartel More Than Government

### Description

Official authority becomes meaningless in cartel-controlled regions.

### Relevant Traits

* Arbitrary
* Sadistic
* Just

### Choices

#### Replace Government Entirely

* control bonuses

#### Maintain Front Institutions

* legitimacy gain

#### Rule Through Fear Openly

* dread gain

---

# EVENT CATEGORY — CRIMINAL PARANOIA

---

## Event: Trusted Lieutenant Secretly Builds Escape Network

### Description

A major lieutenant prepares for betrayal and escape.

### Relevant Traits

* Paranoid
* Cynical
* Ambitious

### Choices

#### Eliminate Them Quietly

* intrigue gain

#### Pretend Ignorance

* future betrayal risk

#### Turn Them Into Double Agent

* intrigue bonuses

---

## Event: The Cartel Devours Itself

### Description

Violence between crews spirals out of control.

### Relevant Traits

* Wrathful
* Arbitrary
* Calm

### Choices

#### Brutal Purges

* authority gain

#### Negotiate Territory Division

* temporary peace

#### Let the Weak Die

* rival destruction

---

# 5. ELVEN MONARCHY — TWILIGHT OF IMMORTAL CIVILIZATION

---

# EVENT CATEGORY — CIVILIZATIONAL EXHAUSTION

---

## Event: The Young No Longer Believe

### Description

Young elves quietly reject ancient traditions.

### Relevant Traits

* Stubborn
* Cynical
* Curious

### Choices

#### Crush Dissident Thought

* control gain

#### Reform the Traditions

* innovation gain

#### Ignore the Youth

* future instability

### Outcomes

Modifier:

* `eotg_elven_generational_decline`

---

## Event: The Court Feels Empty

### Description

Ancient ceremonies continue, but fewer nobles truly care.

### Relevant Traits

* Melancholic
* Content
* Arrogant

### Choices

#### Preserve Ritual Anyway

* legitimacy gain

#### Modernize the Court

* stability gain

#### End Ancient Ceremonies

* traditionalist anger

---

# EVENT CATEGORY — IMMORTAL MADNESS

---

## Event: A Noble Cannot Forget the Past

### Description

A centuries-old aristocrat descends into obsession over ancient grievances.

### Relevant Traits

* Vengeful
* Lunatic
* Paranoid

### Choices

#### Support Their Crusade

* faction escalation

#### Force Retirement

* noble anger

#### Exploit Their Obsession

* intrigue bonuses

---

## Event: Eternal Life Breeds Detachment

### Description

Immortal elites increasingly see mortal lives as meaningless.

### Relevant Traits

* Arrogant
* Compassionate
* Cynical

### Choices

#### Embrace Elven Superiority

* noble loyalty gain

#### Encourage Empathy

* legitimacy gain

#### Isolate the Nobility Further

* isolationism gain

---

# 6. PMC — THE PERMANENT WAR MACHINE

---

# EVENT CATEGORY — WAR STATE COLLAPSE

---

## Event: Officers Profit from Endless War

### Description

Military leaders sabotage peace negotiations for profit.

### Relevant Traits

* Greedy
* Ambitious
* Cynical

### Choices

#### Encourage Continued War

* military bonuses

#### Punish Corrupt Officers

* discipline gain

#### Secretly Profit Alongside Them

* gold gain

### Outcomes

Modifier:

* `eotg_pmc_perpetual_conflict`

---

## Event: Soldiers Lose Ability to Live as Civilians

### Description

Veterans cannot adapt to peaceful society.

### Relevant Traits

* Brave
* Wrathful
* Calm

### Choices

#### Expand Veteran Programs

* stability gain

#### Redirect Them Into Security Forces

* control bonuses

#### Ignore the Crisis

* unrest increase

---

# EVENT CATEGORY — MILITARY CULT EXTREMISM

---

## Event: Operators Worship War Itself

### Description

A dangerous warrior ideology spreads through the ranks.

### Relevant Traits

* Zealous
* Wrathful
* Brave

### Choices

#### Encourage Militarism

* combat bonuses

#### Reinforce Professionalism

* discipline gain

#### Purge Extremists

* instability risk

---

## Event: Children Raised for Endless Conflict

### Description

Entire generations grow up expecting permanent warfare.

### Relevant Traits

* Ambitious
* Callous
* Compassionate

### Choices

#### Expand Militarized Education

* army quality gain

#### Reintroduce Civilian Values

* stability gain

#### Exploit Militarized Youth

* manpower bonuses

---

# 7. NEW CAULDRON DEMOCRACY — DEMOCRATIC DECAY & MASS POLARIZATION

---

# EVENT CATEGORY — POLITICAL RADICALIZATION

---

## Event: Citizens Stop Trusting Elections

### Description

Large populations believe elections are fundamentally corrupt.

### Relevant Traits

* Cynical
* Honest
* Arbitrary

### Choices

#### Reform Election Systems

* legitimacy gain

#### Suppress Dissidents

* unrest increase

#### Exploit Distrust Politically

* polarization growth

### Outcomes

Modifier:

* `eotg_nc_electoral_crisis`

---

## Event: Extremist Militias Form

### Description

Political radicals organize armed movements.

### Relevant Traits

* Wrathful
* Calm
* Zealous

### Choices

#### Ban the Militias

* rebellion risk

#### Secretly Support Allies

* intrigue bonuses

#### Integrate Them into Politics

* instability gain

---

# EVENT CATEGORY — DEMOCRATIC EXHAUSTION

---

## Event: Citizens Grow Tired of Politics

### Description

Public apathy spreads after endless political crises.

### Relevant Traits

* Cynical
* Gregarious
* Calm

### Choices

#### Encourage Civic Participation

* legitimacy gain

#### Exploit Public Apathy

* authority gain

#### Distract the Population

* stability bonuses

---

## Event: Calls for a Strong Leader Grow

### Description

Many citizens demand decisive leadership over democracy.

### Relevant Traits

* Ambitious
* Arbitrary
* Just

### Choices

#### Defend Democratic Institutions

* legitimacy gain

#### Expand Executive Authority

* authoritarian drift

#### Manipulate Public Fear

* political control bonuses
