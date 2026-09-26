# Confluence Legacies — System Pitch

## Premise

Orrin's Grip did not merely destroy the Second Era. It forced worlds, stations,
territories, and planes of existence together into the Third Era's strange
geography. This violent fusion is known as **the Confluence**.

Every inhabited system may therefore contain layers that do not belong together:

- a buried district from an unrelated Second Era planet;
- the surviving machinery of a civilization with no living descendants;
- an orbital habitat embedded in a mountain range;
- a sealed fragment of one of Hell's many layers, now mistaken for an ordinary
  badland or mine;
- a shrine, archive, palace, or battlefield whose original star is long gone.

The world is not a clean frontier. It is an inheritance assembled from wreckage.
The player does not simply develop territory; they decide what to do with the
past already buried inside it.

## Terms

- **The Confluence:** the historical and scholarly term for the forced fusion
  of Second Era places during Orrin's Grip.
- **Confluence Legacies:** the gameplay system—what rulers discover, claim,
  exploit, preserve, or seal from that inheritance.
- **World-Seams:** physical places where incompatible fragments of worlds are
  fused together.
- **Orrin's Scars:** fearful or religious language for dangerous World-Seams,
  especially those marked by Void influence.

## Design Goal

Make individual counties feel like **systems with histories**, rather than
interchangeable landed parcels. The system should create discovery, ownership
disputes, cultural friction, and long-tail consequences for a realm.

It is deliberately not a generic archaeology minigame. A relic site should
matter because of what the ruler does with it:

- preserve it and gain legitimacy, learning, or a new local community;
- exploit it for money, soldiers, or infrastructure;
- conceal or destroy it to prevent religious, dynastic, or Void-related danger;
- claim its heritage and invite a rival to contest that claim.

## CK3 Shape

### County-level site traits

Give selected counties one persistent **Confluence Legacy** modifier or flag. A
site is revealed at game start for famous locations, or discovered through a
decision/event chain. It supplies a small always-on identity effect and unlocks
the appropriate event pool.

Suggested site families:

| Site family | What it represents | Baseline gameplay identity |
|---|---|---|
| **Buried Metropolis** | Fused ruins of a vanished city-world | Development, salvage, urban unrest |
| **Relic Works** | Foundry, reactor, shipyard, or industrial complex | Income, building speed, industrial accidents |
| **Archive Fragment** | Library, data-vault, memory palace, or diplomatic record | Learning, claims, secrets, cultural prestige |
| **Lost Court** | Palace, embassy, command bunker, or refugee government | Claimants, legitimacy, court politics |
| **Pilgrim Scar** | A site marked by a god, saint, Titan, or planar breach | Piety, conversion, faith conflict |
| **Hell Pocket** | A sealed but living fragment of an infernal layer | Rare rewards, corruption, monsters/raids, religious crisis |
| **War Graveyard** | A battlefield, fleet wreck, or weapons cache | Men-at-arms support, dread, veterans, dangerous arms races |
| **Ecological Graft** | Incompatible biospheres fused together | Development and supplies, disease, unusual local culture |

Only a minority of counties need a site. The intent is for discoveries to be
memorable and geographically meaningful, not for every holding to generate a
constant event.

### Legacy lifecycle

A Confluence Legacy must not be a one-time cache. Each known Legacy has a
simple visible **condition** and a mostly hidden **attention** value. These are
enough to make the same place produce different stories over a campaign without
requiring a new interface.

| Condition | Meaning | Typical next pressure |
|---|---|---|
| **Dormant** | Known only to a few, or still buried | Survey, construction, refugees, or war can expose it |
| **Exposed** | Opened, but no durable policy has been chosen | Local opportunists, scholars, and rivals compete to define it |
| **Governed** | Recovered, chartered, sanctified, or safely integrated | Produces a persistent benefit and recurring obligations |
| **Extracted** | Being mined, stripped, or militarized | Produces immediate value while integrity declines |
| **Sealed** | Contained, forbidden, or formally abandoned | Safe for now; cults, smugglers, or a later breach can challenge the seal |
| **Unstable** | Damaged, contested, or actively changing | Disaster, succession crisis, breach, or exceptional reward is possible |

**Attention** rises when a ruler publicizes, militarizes, exploits, or claims a
Legacy. It falls through secrecy, diplomacy, successful integration, and time.
At low attention a Legacy is a local matter; at high attention it can pull in a
neighbour, faith head, mercenary company, claimant, refugee group, or powerful
vassal. This turns success into a new kind of vulnerability instead of a final
reward.

Use only two lightweight tracked values per important site:

- **Integrity** — how much of the Legacy remains. Exploitation, war, and bad
  outcomes reduce it; patient recovery and investment restore it. At zero the
  site is exhausted, transformed, or catastrophically altered.
- **Attention** — who has heard of it and wants a say. Public acts and visible
  wealth raise it; secrecy and recognized charters lower it.

The player should always see the condition and broad attention band in the
county modifier tooltip: *Obscure*, *Rumoured*, *Contested*, or *Renowned*.
Exact numbers may remain hidden.

### Sources of motion

The yearly survey is only one entry point. Legacies should enter play when the
world changes around them:

- a county changes hands, is raided, or is occupied in a major war;
- control or development crosses a threshold;
- a ruler begins a building project, faces debt, or needs troops;
- a Titan Exodus fleet arrives with a map, key, claimant, or survivor;
- a character dies, inherits the county, starts a scheme, or returns from war;
- a struggle phase changes, especially in the Myr Clusters;
- an Unstable World-Seam shifts after a cooldown.

Each site should have a cooldown after a major event—normally two to five
years—unless it is Unstable. This preserves a sense of a living world without
turning every county into event spam.

### Discovery and stewardship

Use a character decision such as **Survey Confluence Legacies** or a council task
such as **Survey Ruined Infrastructure**. The task targets a county in the
domain and, over time, can:

1. reveal a hidden site;
2. improve understanding of a known site;
3. trigger a consequence event;
4. exhaust a site for immediate gain; or
5. establish a lasting institution around it.

Stewardship and Learning should be the primary skills. Martial and Intrigue
should offer distinct approaches—secure a dangerous site or quietly strip it
before rivals learn it exists.

This gives peaceful rulers a meaningful campaign action without making the
system passive. A ruler must choose whether a discovery becomes a public asset,
a private extraction project, or a secret.

## The Core Choice: Recover, Exploit, Seal, or Claim

Every substantial discovery should offer some version of these four responses.

| Response | Immediate reward | Longer consequence |
|---|---|---|
| **Recover** | Development, control, cultural acceptance, prestige | Creates a durable local institution or a new community with expectations |
| **Exploit** | Gold, men-at-arms equipment, a temporary military/economic modifier | Site degradation, worker unrest, accidents, rival attention |
| **Seal** | Removes a danger, gains faith approval or safety | Loses access to rewards; secret cults, smugglers, or a future breach remain possible |
| **Claim** | Legitimacy, prestige, a claim, or diplomatic leverage | Invites competing claimants, faith objections, or a succession dispute |

The response should reflect personality. Compassionate rulers protect displaced
populations; greedy rulers strip vaults; zealous rulers sanctify or destroy;
ambitious rulers claim a dead civilization's authority.

Every answer should also change the site's lifecycle. Recover generally moves a
Legacy toward **Governed**; Exploit toward **Extracted** and higher Attention;
Seal toward **Sealed** but leaves a future breach hook; Claim makes it
**Renowned** and attracts political competitors. The system is dynamic when a
choice changes the next question, not merely the reward.

## Event Material

### Event structure

Legacies should run in short, consequential chains rather than isolated
treasure-popups:

1. **Discovery:** a survey, construction project, war, refugee arrival, or
   county-control event reveals the Legacy.
2. **Disposition:** the ruler chooses to Recover, Exploit, Seal, or Claim it.
3. **Reckoning:** the choice produces a result after weeks, months, or years.
   This is where chance, skill, and political opposition matter.
4. **Inheritance:** a successful or failed disposition leaves a lasting county
   feature, character relationship, claimant, secret, or future event hook.

### Dynamism rules

The system should follow these rules in implementation:

1. **A Legacy remembers.** Its condition, integrity, attention, charter,
   claimant, and unresolved obligation survive a ruler's death and a county's
   transfer. A conqueror inherits the problem as well as the reward.
2. **Every public reward creates an audience.** A prominent discovery should
   select at least one interested actor from the local ruler, powerful vassals,
   neighbouring rulers, same-culture characters, same-faith characters,
   refugees, corporations/PMCs, or criminal groups.
3. **The interested actor acts.** They ask for a concession, offer a bargain,
   start a scheme, fund a rival expedition, demand recognition, or prepare a
   war/raid. They must be more than flavour text in the ruler's event window.
4. **Rulers can change the Legacy, not solve it forever.** Extraction trades
   integrity for value; recovery trades immediate profit for obligations; a
   seal can fail; a charter can be disputed; a restored community can become a
   political constituency.
5. **The county changes the wider game.** A recovered archive may create a
   claim, a relic works may affect a contract, and a Hell Pocket may become a
   faith problem. Results should propagate to characters, factions, diplomacy,
   wars, or another system.
6. **The event pool reacts to history.** Do not repeat the discovery event once
   a site is known. Dispatch later events from its condition, attention,
   integrity, previous disposition, owner government, and the personalities of
   interested characters.

No result should be completely random. Choices show an **outcome category** in
their tooltip—favourable, uncertain, or dangerous—and relevant skill,
education, traits, councillors, and site condition shift the odds. Players can
choose danger for a better reward; they should not lose a developed county to a
surprise die roll.

### Option gates: personality, education, and ability

Every major event retains **at least two, preferably three, broadly available
options**. Gated options express *how* a ruler governs, rather than merely
giving the best result to a single build. No player should be left with a
single meaningful answer because their ruler lacks the relevant trait,
education, skill, councillor, or artifact.

| Gate | Example exclusive response | Usual benefit | Usual cost or risk |
|---|---|---|---|
| **Compassionate / Just** | Protect an enclave; honour the dead polity's law | acceptance, opinion, legitimacy | gold cost, stronger local expectations |
| **Greedy / Callous** | Strip a vault; sell relic rights; compel survivors into service | gold, construction, levy reward | unrest, site depletion, stress for compassionate rulers |
| **Ambitious / Arrogant** | Claim a dead world's mandate | prestige, legitimacy, claim/CB | rival claimant or powerful-vassal opposition |
| **Zealous** | Consecrate or purge a spiritual Legacy | piety, faith opinion, reduced breach risk | faith hostility, lost secular reward |
| **Cynical** | Publicly sanctify a site while secretly auctioning access | gold and a secret/hook | exposure scandal, stress for honest rulers |
| **Brave / Wrathful** | Personally lead a breach or purge | martial prestige, fast resolution | injury, death, collateral damage |
| **Patient / Temperate** | Stabilize the site over time | safest persistent outcome | delayed reward; a rival may intervene |
| **Martial education** | Secure, drill, or dismantle a war relic | regiment/defence reward | arms race or militarized vassal |
| **Stewardship education** | Audit and concession a relic works | income, building, control reward | corruption or worker unrest |
| **Intrigue education** | Conceal the discovery or sell it through intermediaries | secrets, hooks, illicit income | blackmail, criminal foothold |
| **Diplomacy education** | Convene descendants, faiths, and neighbours | acceptance, alliances, legitimacy | concessions and reduced direct profit |
| **Learning education** | Interpret an archive, contain a breach, or restore a rite | knowledge, piety, safe recovery | slow resolution; dangerous revelation |

Education gates should normally require an education trait at level 2 or higher.
Level 4 education, a relevant councillor with 15+ skill, or a ruler skill of
16+ can upgrade an uncertain result to favourable or suppress the worst branch.
Exceptional thresholds—20+ skill, a renowned courtier, or a fitting artifact—can
unlock a special answer rather than simply increasing numbers.

### 1. Survey events — discovery is contested

#### The Map That Contradicts the Sky

A survey team finds a Second Era star chart whose route network cannot match
the present heavens. It points to an apparently empty location in the county.

- **Fund a full excavation** — costs gold; 55% chance to reveal an Archive
  Fragment or Buried Metropolis, 25% chance of an ordinary salvage cache, and
  20% chance that the map was deliberately false or dangerous.
- **Commission a cautious local survey** — modest gold and a slower outcome;
  likely to reveal only a minor cache, but cannot trigger the dangerous branch.
- **File the chart under seal** — no immediate reward; lowers Attention and
  creates a future discovery hook when a ruler, refugee, or courtier produces
  a reason to revisit it.
- **[Learning education 2+] Recalculate the old heavens** — a slower, safer
  route; a skilled Learning ruler can identify whether the chart is a World-Seam
  distortion, gaining lifestyle experience and avoiding the false-map result.
- **[Greedy] Sell the coordinates** — immediate gold; a neighbouring ruler,
  corporation, or cartel may gain the site first and acquire a claim to it.
- **[Paranoid] Burn the chart** — no reward, but blocks a later dangerous
  discovery in exchange for stress relief or dread.

#### The Surveyors Have Stopped Reporting

An expedition falls silent below an exposed seam.

- **Send the county garrison** — costs gold and briefly weakens local control;
  a middling chance to save the surveyors or recover their notes.
- **Hire independent salvage crews** — a gold-for-chance response; success
  reveals a site, failure raises Attention by letting outsiders learn of it.
- **Close the breach and record the loss** — no rescue and a popular-opinion
  penalty, but the site becomes Sealed and cannot worsen for several years.
- **[Brave or Martial education 2+] Lead a relief force** — high chance of
  rescuing an excellent courtier or recovering a weapons cache; low chance of
  injury or the ruler gaining a traumatic/stress modifier.
- **[Compassionate] Pay for a careful recovery** — gold cost, high chance of
  saving the team and gaining local opinion.
- **[Callous] Mark them lost and continue** — avoids cost; 35% chance that
  survivors return as hostile witnesses, lowering county control.
- **[Intrigue education 3+] Learn why they stopped** — discovers sabotage by a
  vassal, rival, or criminal network, enabling a hook or imprisonment attempt.

#### The Boundary Moves Overnight

A World-Seam shifts and exposes a new district while swallowing part of a
settlement.

- Emergency resettlement protects control and popular opinion but costs gold.
- Claim the exposed works for the domain gives a major discovery chance but
  risks development loss if the seam shifts again.
- Mark the district as forbidden ground: prevents a follow-up disaster and
  lowers Attention, but leaves the Legacy Dormant and sacrifices development.
- **[Stewardship 16+]** stabilise the site: a strong long-term county modifier,
  but no immediate payout.
- **[Zealous]** declare the movement an omen: piety and fervour, with a chance
  that another faith considers the proclamation blasphemous.

### 2. Buried Metropolis events — the district that should not be there

An intact civic district is found beneath a county. Its architecture, language,
and star charts belong to a world from the other side of the former galaxy.

#### The Street of Foreign Suns

- **Restore it as a living district** — development and a county modifier.
  After one to three years, descendants or cultural enthusiasts petition for
  protected status. A diplomatic ruler can turn them into a loyal enclave;
  refusing them creates resentment.
- **Open it under a temporary public authority** — modest control and
  legitimacy; after a year, the ruler chooses whether to charter, recover, or
  close the district with better information.
- **Cordon and catalogue the ruins** — low cost and no immediate payout; keeps
  Integrity intact while lowering Attention and creates an archive follow-up.
- **[Stewardship education 2+] Issue rebuilding concessions** — gold and
  construction speed; a 30% chance of contractor corruption that can be
  investigated, ignored, or used for blackmail.
- **[Greedy] Sell the fabric of the old city** — large immediate gold and a
  small development loss; may deplete the Legacy permanently.
- **[Ambitious] Declare it a national monument** — prestige and legitimacy;
  one eligible neighbouring ruler may receive an event claiming the district
  was stolen from their ancestors.

#### The Unfinished Evacuation

The metropolis still contains evacuation records naming families who never
reached safety.

- **Place the register in the public archive** — a small legitimacy reward;
  the information may create a claimant later, but no character is immediately
  favoured.
- **Let local families search it privately** — improves popular opinion and
  has a modest chance to create a grateful courtier or a disputed inheritance.
- **Hold the register pending verification** — buys time and lowers the chance
  of a false claim, at the cost of prestige and growing local frustration.
- **[Compassionate or Just] Publish the names** — acceptance and popular
  opinion; a courtier or vassal may discover a lost ancestor and gain a claim.
- **[Intrigue education 2+] Alter the register before publication** — creates a
  hook on the affected character if undiscovered; exposure causes a legitimacy
  scandal.
- **[Callous] Use the names to locate abandoned assets** — gold, with a chance
  of awakening a claimant faction in the county.

### 3. Archive Fragment events — the court in the vault

An archive contains a preserved legal register, genealogy, and succession
protocol for a dead Second Era polity. These events should produce political
facts: claims, hooks, secrets, and contested authority.

#### The Court in the Vault

- **Seal and catalogue the archive** — safe, slow, and preserves Integrity;
  gains a small Learning reward and starts a later interpretation event.
- **Employ neutral archivists** — costs gold for a moderate chance of a useful
  claim, secret, or artifact; a poor result produces only a local modifier.
- **Open the records to the realm** — grants prestige and raises Attention,
  inviting one interested house to make a request or counterclaim.
- **[Learning education 2+] Restore the archive's chain of custody** — gains
  Learning experience, legitimacy, and a safe archive modifier. At 18+ Learning
  there is a chance to recover a unique artifact or historical claim.
- **[Diplomacy education 2+] Invite interested houses to witness the opening**
  — lowers the chance of a claimant crisis and may create an alliance or truce,
  but the ruler cannot monopolize the records.
- **[Ambitious] Adopt the dead polity's mandate** — prestige and a one-use CB
  or title claim; a powerful vassal can reject the invented continuity.
- **[Cynical / Intrigue education 3+] Copy only the useful records** — gains
  secrets and hooks; 40% chance a scholar learns of the omission and becomes a
  blackmailer.

#### The Archive Names an Heir

The records establish that a living courtier, vassal, foreign ruler, or refugee
has a plausible connection to the dead court.

- Recognize the heir as a client or vassal: an opinion and legitimacy gain,
  with a future succession problem.
- Support the heir abroad: a hook, alliance, or proxy-war pretext.
- **[Just] Publish the finding regardless of cost** — major stress relief and
  legitimacy; strongly empowers the heir.
- **[Arbitrary] Suppress it** — secure short-term control; the record can later
  escape through a courtier, producing a harsher scandal.

#### The Memory That Refuses to Be Read

An archive contains living or semi-living memory architecture.

- **Assign a supervised scholar team** — costs gold; a moderate chance to
  gain Learning experience or a useful secret, with a small chance of stress
  or an Unstable result.
- **Keep the memory isolated** — establishes a safe quarantine modifier and
  delays the question, though it can attract future smugglers or cultists.
- **Destroy its active core** — permanently removes the danger and reduces
  Integrity to zero; grants a small control reward but no knowledge.
- **[Learning 16+]** communicate safely, gaining a scholar/secret/innovation
  progress reward.
- **[Brave]** enter it personally, with a high reward and a low but serious
  chance of stress, a mental trait, or Void exposure.
- **[Paranoid]** isolate it, gaining a safe quarantine modifier and a delayed
  chance for smugglers or cultists to seek it out.

### 4. Relic Works events — industry without an owner

#### The Foundry Still Burns

A buried industrial complex can produce something useful, but its safety
systems were designed for a population and environment that no longer exist.

- **Reopen one production line under guard** — modest income with a modest
  accident chance; it reveals whether the site can sustain a larger project.
- **Dismantle it for materials** — safe gold and construction supplies, while
  reducing Integrity and ending the chance of a permanent relic works.
- **Mothball the complex** — no current profit; keeps Integrity high and lowers
  Attention until a later ruler, war, or shortage gives reason to reopen it.
- **[Stewardship education 2+] Recommission under audited concessions** —
  income and a relic-foundry building; outcome chance scales with Stewardship
  and the steward's skill.
- **[Martial education 2+] Convert it to armaments** — a temporary regiment or
  men-at-arms modifier; powerful vassals gain an arms-race opinion modifier.
- **[Greedy] Run it at full output** — immediate gold with a substantial chance
  of fire, workers' unrest, or permanent site depletion.
- **[Temperate / Patient] Bring it online slowly** — no early gold, but the
  best chance of a permanent building and no disaster branch.

#### The Concession War

Two vassals, corporations, or foreign patrons offer competing terms for a
Relic Works concession.

- Grant an exclusive concession for gold and a political backer.
- Divide access for smaller rewards but lower faction pressure.
- **[Diplomacy education 3+] Negotiate a public charter** — requires a Senate,
  board, or vassal vote where appropriate; grants legitimacy and control.
- **[Intrigue education 2+] Sell each side false assurances** — gains hooks and
  gold; a discovery produces a hostile scheme or faction.

### 5. War Graveyard events — the war machine wakes

#### The Arsenal Beneath the Field

A Relic Works or War Graveyard yields a functioning Second Era weapons system.

- Refit it for the realm: temporary men-at-arms effectiveness or a regiment
  unlock. The chance of a safe refit is higher for Martial education and high
  prowess/martial councillors.
- Sell access to a PMC or corporation: gold and a contract relationship;
  25% chance the buyer later uses the weapons against the realm or its ally.
- Dismantle it: a safe development/building reward, but no military legacy.
- Entrust it to a vassal: opinion and military support now; that vassal gains a
  persistent power modifier and may become a future rival.

#### The Dead Fleet's Oath

Recovered records show that a legendary unit was betrayed by the ruler's
political ancestors.

- **Hold a memorial without assigning blame** — modest prestige and local
  opinion; the hidden grievance remains but does not immediately escalate.
- **Archive the record as disputed history** — little immediate reward; lowers
  Attention and creates a future historian or claimant event.
- **Invite the unit's descendants to negotiate** — costs gold or a concession,
  but may end the grievance or reveal that they seek a political claim.
- **[Honest or Just] Admit the betrayal** — improves relations with the unit's
  cultural descendants and removes a hidden grievance; costs prestige now.
- **[Ambitious] Claim the unit's glory** — prestige and martial lifestyle
  experience; a historian, courtier, or rival can expose the lie.
- **[Zealous] Consecrate the wreckage** — piety and a pilgrimage/holy-site-like
  local modifier, but destroys the military reward.

### 6. Hell Pocket events — a fragment of Hell has a tax code

A Hell Pocket is not only a monster nest. It may contain a functioning infernal
market, a disciplined garrison, a bound bureaucracy, or a population that has
survived there for centuries.

#### The Infernal Ledger

- **Bargain** — receive gold, soldiers, or secrets; accept a timed obligation
  that returns as a future event. Default success is uncertain, not guaranteed.
- **Quarantine the market** — gold cost and no infernal reward; lowers breach
  risk while leaving a Sealed site that could later tempt smugglers.
- **Order the gate closed by force** — a martial-strength-weighted chance to
  destroy the market safely; failure makes the pocket Unstable and causes
  immediate local damage.
- **[Stewardship education 3+] Audit the bargain** — reduces the obligation or
  identifies a loophole. Failure creates a more demanding debt.
- **[Cynical] Offer someone else's concession** — shifts the cost to a vassal
  or rival; creates a secret and a strong exposure event.
- **[Zealous] Reject the ledger as blasphemy** — piety and faith approval; may
  provoke an immediate breach or destroy the market safely depending on martial
  strength and the realm priest's Learning.

#### The Gate Wants a Warden

The pocket can be contained only if a living character accepts a long-term role.

- Ask a loyal courtier or knight: they gain a unique modifier and may become a
  heroic, corrupted, or resentful figure.
- **[Brave] Take the burden yourself** — rare, powerful realm protection and
  major prestige; injury, stress, fertility, or health risk.
- **[Callous] Compel a prisoner** — no willing-candidate requirement; dread and
  short-term safety, with a high chance of a vengeful return.
- Seal the gate permanently: costly, safe, and narratively final.
- Fund a rotating watch: a modest recurring cost preserves the seal without
  sacrificing the site, but creates a future Warden politics event.

### 7. Living Legacy events — the people below the ruins

Surveyors discover a surviving community adapted to a sealed fragment for
centuries. They may have a distinct faith, culture, body, or political custom.

#### The People Below the Ruins

- **Recognize them provisionally** — small acceptance and a delayed request for
  a charter; neither immediate autonomy nor exploitation is committed to.
- **Resettle willing families across the county** — modest development and
  control gain, with a chance that cultural friction increases later.
- **Keep the settlement isolated** — avoids a realm-wide issue and lowers
  Attention, but leaves the community distrustful and the county underdeveloped.
- **[Compassionate] Protect them as a community** — gains acceptance and a
  county-development bonus after a delay; their elders later ask for legal
  recognition.
- **[Diplomacy education 2+] Negotiate a local charter** — creates a loyal
  enclave modifier, a courtier, or a low-tier vassal; the community expects
  autonomy in future crises.
- **[Greedy or Callous] Compel service** — levies or income now; a chance of
  revolt, flight, or an Exodus-style raider follow-up.
- **[Zealous] Demand conversion** — success chance depends on faith hostility
  and the realm priest; failure creates a secret cult or religious faction.
- **[Arbitrary] Expel them** — removes local friction but launches a possible
  refugee, raid, or foreign condemnation event.

#### The Child of Two Worlds

A prominent member of the enclave has ancestry—or a body—shaped by two fused
world fragments. They become an exceptional courtier, a marriage prospect, or
a political symbol.

- Educate and sponsor them: gain a talented character and community loyalty.
- Give them a minor court appointment: a modest skill/opinion reward that keeps
  them close, with a chance they become a useful political intermediary.
- Send them as an honoured envoy: improves relations with a suitable neighbour
  or enclave, but they may build an independent power base away from court.
- **[Paranoid] Keep them under watch** — a hook and scheme resistance, but a
  chance they become a resentful rival.
- **[Ambitious] Bind them to the dynasty by marriage** — legitimacy with the
  enclave, but cultural/faith objections and difficult inheritance politics.

### 8. Ecological Graft events — a living world that does not agree with itself

#### The Forest Eats the Bulkhead

An alien biosphere is consuming an old habitat, creating valuable medicines,
food, and biological hazards.

- **Cordon the advancing graft** — costs gold and prevents the immediate
  disease branch, but provides no income and leaves the site Dormant.
- **Permit a limited local harvest** — small income and popular opinion with a
  low depletion risk; a later event determines whether the ecosystem adapts.
- **Burn back the perimeter** — protects existing holdings and control but
  reduces Integrity and may destroy a rare resource.
- **[Learning education 2+] Establish a controlled preserve** — health and
  development reward; a rare chance of a valuable biological artifact.
- **[Stewardship education 2+] Harvest it under quotas** — income with a
  manageable depletion risk.
- **[Greedy] Strip the graft bare** — large gold; high disease, famine, or
  control-loss risk.
- **[Mystic / Zealous] Treat it as a living holy place** — piety and faith
  support; a materialist or industrial vassal may oppose the restriction.

### 9. Political aftermath events — inheritance never stays buried

These events fire months or years after any major Legacy disposition. They turn
a county outcome into character politics. The selection should be driven by the
site's condition and attention, not by a fixed sequence.

- **The rival's archaeologist:** a neighbour asserts ownership of a recovered
  Legacy. Most likely at *Contested* or *Renowned* attention. Negotiate, pay
  compensation, expose their weak evidence, or prepare for a claim war.
- **The concession's beneficiaries:** a vassal, board member, or Trade Prince
  has become too rich from an Extracted site. Tax them, demand a vote,
  nationalize the works, or accept their growing influence.
- **The legacy at succession:** a new ruler inherits a site agreement they did
  not make. Honour it for legitimacy, renegotiate at political cost, or break
  it and face factions, raids, or a client breaking away.
- **The cult beneath the monument:** an apparently safe restoration has become
  a focus for an alien faith, a Void cult, or a movement for local autonomy.
  More likely if a Sealed or Governed spiritual site has low integrity.
  Investigate and tolerate it, prohibit public rites, or fund an orthodox local
  institution; trait and faith options may offer stronger variants.
- **The veteran's claim:** a commander who secured a War Graveyard now argues
  that they, not the ruler, embody the site's military inheritance. Grant an
  honour without land, appoint them to a restricted command, or dismiss their
  claim and accept the resulting opinion/faction risk.
- **The seam changes hands:** conquest, inheritance, or a revolt transfers the
  county. The new holder must recognize the old charter, strip the former
  beneficiary, or re-seal the site—each choice changes the former holder's
  opinion and can create a claim, truce, raid, or faction.
- **The quiet site becomes famous:** an event, artifact, courtier, or refugee
  raises Attention from *Rumoured* to *Contested*. Select a new interested
  actor and give them an active response rather than simply a notification:
  publicly recognize their interest, buy them off with a concession, or deny
  the connection and lower Attention at a legitimacy cost.
- **The exhausted Legacy:** an Extracted site reaches zero Integrity. It may
  become an abandoned ruin, collapse into an Unstable World-Seam, reveal a
  deeper layer, or leave an angry workforce and no more profit. Abandon the
  works, finance a safe conversion of the ruins, or gamble on reaching the
  deeper layer; the latter may have gated expert variants.

These aftermaths are where Legacy content becomes generational CK3 drama. A
good discovery should still have the ability to matter when the original ruler
is dead.

## Rewards

The reward palette should be broad enough that each discovery is tempting, but
not so strong that surveying becomes the only optimal activity.

### Immediate rewards

- gold, prestige, piety, legitimacy, or lifestyle experience;
- county control/development and temporary construction or tax modifiers;
- artifacts, secrets, hooks, and claim opportunities;
- a temporary men-at-arms or knight effectiveness modifier;
- a skilled courtier, engineer, commander, scholar, or refugee claimant.

### Persistent rewards

- a specialized county building such as a salvaged shipyard, archive sanctuary,
  relic foundry, pilgrimage scar, or fortified quarantine;
- a local culture/faith acceptance modifier;
- a recurring court position, council task, or decision;
- access to a distinctive regiment, artifact pool, or contract type;
- a new vassal, client, holy order, mercenary company, or minority enclave.

### Costs and failure states

- control loss, development damage, disease, fire, or planar breach;
- a hostile faith or cultural faction;
- a claimant whose legitimacy is strengthened by the discovery;
- a rival who covets the site, creating a CB or hostile scheme opportunity;
- corruption, stress, or Void exposure for characters who excavate too deeply;
- site depletion, so extraction has a visible price.

## How Governments Should Read the Same Legacy Differently

The same discovery should reinforce each polity's identity rather than require
separate site systems.

| Government | Natural response to a Confluence Legacy |
|---|---|
| **New Cauldron** | Senate inquiry, public works, heritage protections, or emergency appropriation |
| **Gob-Corp / Corporation** | concession rights, shareholder fights, proprietary archives, and private security |
| **Cartel** | smuggling routes, illicit relic markets, protection rackets, and compromised officials |
| **PMC** | secure the site for a client, sell access, or use it to strengthen the company |
| **Fringe** | loot it, make it a warlord's seat, or lose control of it to a captain |
| **Elven Monarchy** | preserve, purify, claim ancestry, or reject contamination from alien layers |
| **Theocratic realms** | sanctify, regulate, weaponize, or purge sites according to doctrine |

This is also a clean way to connect currently separate signature resources:
corporations may spend Board Influence to secure a concession; Fringe rulers
gain or lose Grip based on distributing salvage; New Cauldron asks for Senate
support before a major appropriation; Cartels turn an excavation into an
underworld monopoly.

## Relation to Other Major Systems

### Titan Exodus

Refugee fleets can identify sites from their lost homelands, arrive with a key
to open a vault, or claim that a newly discovered district belongs to them.
Sheltering refugees can therefore unlock genuine local growth rather than a
generic development bonus.

### Myr Cluster Wars

The struggle's stakes become more concrete when contested counties contain
specific Second Era assets: a Helix archive, an industrial relic, a sacred
scar, or a half-buried command network. Control of a county then changes more
than a border color.

### Void Echoes

Confluence Legacies can be a major source of Void exposure, but not every strange
remnant is Void-tainted. Keep Hell, lost civilizations, divine scars, and
ordinary industrial wreckage distinct. The setting becomes richer when the
player cannot solve every anomaly with a single "corruption" label.

### Culture and faith

Use sites to produce cultural and religious politics: who owns the memory of a
dead civilization, who may interpret its records, and whether its survivors
belong in the present realm. This is more thematically useful than making every
site a technology cache.

## Scope Recommendation

### First playable version

- 8–12 hand-placed famous sites, primarily in the Myr Clusters and major
  bookmark powers;
- 4 site families: Buried Metropolis, Archive Fragment, Relic Works, Hell
  Pocket;
- one survey decision and at least **three short event chains per family**:
  discovery, disposition, and a delayed reckoning or political aftermath;
- one shared aftermath pool for claimants, concessions, succession disputes,
  and cults—so a resolved county event can still shape the next generation;
- one persistent county modifier/building outcome per family;
- condition flags plus Integrity and Attention for every hand-placed site;
- ownership-transfer and succession events for any site with a charter,
  concession, claimant, or high Attention;
- a limited chance for newly surveyed counties to reveal a hidden site.

### Later expansion

- government-specific variants and contracts;
- artifacts and dedicated men-at-arms tied to selected major sites;
- a map layer or iconography for known sites;
- dynamic region events: a seam shift, a salvage boom, a cult migration, or a
  relic arms race that affects several related counties at once;
- site inheritance, where rulers and claimants fight over discoveries made by
  earlier generations;
- region-specific site tables so the Myr Clusters, Devoid Systems, Coldiron
  space, and the Border Systems do not all produce the same ruins.

## Guiding Rule

Every Confluence Legacy should answer two questions:

1. **What impossible piece of the Second Era is here?**
2. **What political problem does possessing it create now?**

If the answer to the second question is only "the ruler receives gold," the
site needs another consequence.
