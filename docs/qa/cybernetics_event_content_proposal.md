# Cybernetics — Proposed Event & Story-Cycle Content

**Date:** 2026-10-03  
**Basis:** `cybernetics_content_gaps.md` and `cybernetics_system_overview.md`

## Purpose

This document turns the identified Cybernetics content gaps into a concrete proposed event and story-cycle list.

The goal is not simply to add more one-screen events. The expanded content should make Cybernetics feel like a character arc with escalating consequences while preserving the current system rules:

- Integration only changes at 0 / 50 / 100.
- Fracture risk remains hidden.
- The system remains map-agnostic.
- Events use vanilla traits/mechanics and `eotg_` identifiers.
- Flavor events should read or move `eotg_fracture_risk`, or change tier.
- Cooldown authority remains in on_actions.
- Neurofracture should be a fundamentally different mode rather than simply a stronger Overclocked tier.

The proposed structure targets approximately **80 events**, with a mixture of small events, medium chains, large story cycles, and a dedicated non-ruler lifecycle.

---

# 1. Overall Event Structure

| Stage | Existing | New target | Final target |
|---|---:|---:|---:|
| Initiation | 5 | +6 | **11** |
| Augmented | 6 | +6 | **12** |
| Enhanced | 6 | +6 | **12** |
| Overclocked | 7 | +7 | **14** |
| Neurofractured | 7 | +18 | **25** |
| Cross-stage / lifecycle | — | +6 | **6** |
| **Total** | **31** | **~49** | **~80** |

The important distinction is that the additional content should not consist entirely of independent popups. Medium and large chains should connect events into recognizable character arcs.

---

# 2. Initiation — 11 Events

### Narrative purpose

**"Why would I voluntarily put this thing inside myself?"**

Initiation should become a deliberate entry into the system rather than something that happens only when a random offer appears.

The current system already has hooks for wounds, wealth, old age, desperation and augmented peers. The major missing hook is replacement of physical losses.

---

## I-01 — The Prosthetic

**Size:** S/M  
**Hook:** `maimed`, `one_legged`, `one_eyed`, `blind`

The flagship initiation event.

### Core choices

- Accept the implant.
- Refuse and remain disabled.
- Seek conventional treatment.

### Special behavior

- Successful augmentation removes the relevant physical-loss trait.
- Court physician access reduces cost/risk.
- Zealous characters can receive a stronger moral objection.
- Cynical characters can receive a more accepting option.

---

## I-02 — The Neural Bridge

**Size:** M  
**Hook:** `infirm` / `incapable`

A physician proposes an experimental neural implant as a last resort.

### Stage 1
Decide whether to undergo the procedure.

### Stage 2
Months later, roll for:

- Successful integration.
- Partial rejection.
- Complication.

The starting fracture risk should be comparatively high.

---

## I-03 — The Cynic's Argument

**Size:** S  
**Hook:** `cynical`, high Learning

The character actively seeks augmentation rather than being offered it.

Potential personality-specific approaches:

- Cynical — reject the idea that flesh is sacred.
- Zealous — demand a justification compatible with faith/piety.
- Ambitious — focus on increased power.
- Curious — pursue the experimental option.

This should be a major personality-reactivity event.

---

## I-04 — Back-Alley Surgery

**Size:** M, 3 stages  
**Hook:** low gold / at war / `deceitful`

A cheap provider offers augmentation.

### Stage 1
Accept the inexpensive procedure.

### Stage 2 — 6–18 months later

Roll for:

- Clean installation.
- Infection.
- Rejection.
- Hidden flaw.
- Illegal implant.
- Unexpectedly excellent result.

### Stage 3
Deal with the consequences.

This is a natural entry point for `eotg_mod_illegal_implants`.

---

## I-05 — The Patron

**Size:** L — story cycle

A wealthy patron offers to pay for augmentation.

At first it appears to be charity.

Eventually:

> "We need a small favour."

Possible escalating demands:

1. Financial repayment.
2. Political favour.
3. Family/hostage favour.
4. Military assistance.
5. Final demand.

The player can:

- Continue cooperating.
- Refuse.
- Renegotiate.
- Betray the patron.

This becomes one of the system's major multi-year arcs.

---

## I-06 — A Parent's Hardware

**Size:** M  
**Hook:** augmented parent has died

The character inherits old implants.

The implants are functional and powerful, but were designed for someone else.

Choices:

- Install them.
- Sell them.
- Destroy them.
- Preserve them.

Installation is cheaper but begins with elevated fracture risk.

---

## I-07 — The Sickly Child

**Size:** M  
**Hook:** child is `ill` / `infirm`

A child can potentially be saved with augmentation.

Possible choices:

- Save the child through augmentation.
- Refuse and accept the risk.
- Attempt an experimental procedure.
- Delay.

The child remains augmented as they grow up, creating future lifecycle content.

---

## I-08 — The Duel Shame

**Size:** S  
**Hook:** failed duel / low Prowess

Someone demonstrates that the character's physical ability is inadequate.

Potential reactions:

- Brave — accept another challenge.
- Craven — embrace augmentation.
- Proud — angry refusal.
- Ambitious — become interested in augmentation.

---

## I-09 — The Arms Race

**Size:** M  
**Hook:** augmented knight/courtier

One augmented warrior becomes two.

Then more.

The ruler eventually has to decide whether to:

- Improve existing warriors.
- Improve themselves.
- Start an augmentation programme.

This naturally feeds into **The Iron Retinue**.

---

## I-10 — The Physician's Proposal

**Size:** S  
**Hook:** `lifestyle_physician`

The physician proactively proposes augmentation.

The physician should become an active participant in the system rather than merely a numerical modifier.

---

## I-11 — The Offer You Sought

**Size:** S  
**Hook:** **Seek Augmentation** decision

This is the cleanest player-controlled entry point.

The player explicitly decides:

> "I want this."

---

# 3. Augmented — 12 Events

### Narrative purpose

**"This is incredible. Why would I ever stop?"**

Augmented should feel socially legible, personally seductive, and useful.

---

## Small Events

### A-01 — Firmware Itch

**Traits:** diligent / lazy

The implant requires maintenance.

- Diligent characters maintain it personally.
- Lazy characters can ignore it.
- Neglect can increase fracture risk.

---

### A-02 — Dulled Palate

**Traits:** gluttonous / temperate

Food no longer tastes quite right.

- Gluttonous characters become frustrated.
- Temperate characters may barely care.

---

### A-03 — A Lover's Touch

**Traits:** lustful / chaste

A romantic partner hesitates to touch the character's augmentation.

Potential effects:

- Attraction opinion.
- Stress.
- Relationship development.

---

### A-04 — The Training Yard

**Traits:** brave / craven  
**Hook:** `lifestyle_blademaster`

The implant makes the character faster and more effective.

The machine may now outperform its owner.

This can lead into **The Challenge**.

---

### A-05 — The Stare

**Traits:** shy / gregarious

People stare at the augmentation.

- Shy characters experience stress.
- Gregarious characters may turn the attention into a spectacle.

---

### A-06 — A Tithe for Purity

**Traits:** zealous / cynical

A pious courtier asks the character to repent.

Faith reactions should remain generic through:

- `zealous`
- `cynical`
- piety

rather than named faith dependencies.

---

## Medium Events

### A-07 — Rejection

**Size:** M

#### Stage 1
Fever.

#### Stage 2
Crisis.

#### Stage 3
Roll for:

- Recovery.
- Implant failure → back to unaugmented + `wounded_1`.
- Recovery with increased fracture risk.

This establishes that augmentation can actually be lost.

---

### A-08 — The Challenge

**Size:** M

A rival knight challenges the augmented character.

Use a Prowess check.

Possible outcomes:

- Victory → prestige.
- Narrow victory → stress/risk.
- Defeat → humiliation.
- Severe failure → injury.

---

### A-09 — Copycat

**Size:** M

A vassal or courtier obtains a botched black-market implant.

They ask for help.

Choices:

- Pay for treatment.
- Refuse.
- Exploit their desperation.
- Remove them from court.

This also helps establish non-ruler augmentation.

---

### A-10 — The Iron Retinue

**Size:** L — story cycle

The ruler begins augmenting knights.

#### Phase 1
First successful retainer.

#### Phase 2
More knights request augmentation.

#### Phase 3
The ruler develops an augmented elite.

#### Phase 4
Non-augmented warriors become resentful.

#### Phase 5
The player decides whether to:

- Continue.
- Stop.
- Reverse the programme.
- Make augmentation a privilege.

This is the primary bridge into the non-ruler lifecycle.

---

### A-11 — Something Is Missing

**Hook:** `curious`

The character realizes they can no longer remember what a particular sensation felt like.

A curious character becomes fascinated rather than frightened.

Dangerous option:

> "What else can I replace?"

This increases fracture risk.

---

### A-12 — The First Upgrade

**Existing progression event, expanded**

Turn the Augmented → Enhanced transition into a short sequence.

#### Stage 1
Why upgrade?

#### Stage 2
What part of yourself should change?

#### Stage 3
Installation.

Personality traits influence the framing and potential risk.

---

# 4. Enhanced — 12 Events

### Narrative purpose

**"This isn't something I wear anymore. This is becoming part of who I am."**

Enhanced should feel invasive and psychologically consequential.

---

## Small Events

### E-01 — Numbers, Not Faces

**Traits:** just / arbitrary

The implant makes a difficult decision easier by reducing people to numbers and probabilities.

The character must decide whether to accept that logic.

---

### E-02 — The Late Grief

**Traits:** forgiving / vengeful

Emotion arrives late.

A death occurred months ago, but only now does grief or anger arrive.

---

### E-03 — Perfect Recall

**Traits:** honest / deceitful

The implant remembers everything.

- Honest character embraces perfect memory.
- Deceitful character looks for ways to exploit it.

---

### E-04 — Absent at the Birth

**Hook:** `on_birth_child`

The character is physically present for their child's birth but emotionally detached.

This should establish a recurring family consequence.

---

### E-05 — Market Ledger

**Traits:** greedy / generous

The implant identifies economic inefficiencies.

- Greedy characters can exploit them.
- Generous characters can reject the recommendations.

---

### E-06 — Trust Protocol

**Traits:** trusting / paranoid

The implant begins flagging suspicious behavior.

The dangerous part:

**Some warnings are wrong.**

This establishes unreliable information before Overclocked.

---

## Medium Events

### E-07 — The Bidding War

**Size:** M

Two augmentation providers compete for the character's next upgrade.

Provider A:

- Safer.
- Less powerful.

Provider B:

- More powerful.
- Higher future risk.

The choice affects the future risk/event curve without changing Integration.

---

### E-08 — Tampering

**Size:** M

Someone attempts to interfere with the implant.

Use an Intrigue check.

Possible outcomes:

- Identify the culprit.
- Temporary malfunction.
- Increased fracture risk.
- Failure to realize anything happened.

---

### E-09 — The Space Between Us

**Size:** M/L

Expand the existing spouse event into three stages.

#### Stage 1 — Concern
The spouse notices emotional detachment.

#### Stage 2 — Confrontation
The spouse demands change.

#### Stage 3 — Resolution

Possible endings:

- Reconciliation.
- Estrangement.
- Divorce.

---

### E-10 — The Cold Calculation

**Traits:** compassionate/just vs cynical/ambitious

The implant provides a mathematically optimal solution to a difficult decision.

The character must decide whether efficiency outweighs morality.

---

### E-11 — The Second Self

**Hook:** elevated fracture risk

The character begins speaking to the implant as though it were a separate entity.

Possible reactions:

- Reject the thought.
- Encourage it.
- Become fascinated.

This is the conceptual bridge to Overclocked.

---

### E-12 — The Next Stage

**Existing progression event, expanded**

The final seductive step.

By this point the character has become dependent enough that removing augmentation feels like losing part of themselves.

---

# 5. Overclocked — 14 Events

### Narrative purpose

**"Something inside me is starting to make decisions."**

Overclocked is the countdown tier.

The content should increasingly undermine the player's confidence in what their character actually knows or remembers.

---

## Small Events

### O-01 — Tremor

**Traits:** patient / impatient

A tiny involuntary movement appears.

- Patient character waits.
- Impatient character attempts self-repair.

---

### O-02 — Phantom Orders

**Traits:** calm / wrathful

The character gives an order and later doesn't remember deciding to give it.

---

### O-03 — Heat Spike

The implant overheats.

Choices:

- Pay for maintenance.
- Push through.
- Shut it down temporarily.

---

### O-04 — The Feast You Didn't Eat

**Traits:** gluttonous / temperate

Everyone remembers the character eating at a feast.

The character does not.

---

### O-05 — First Contact

The implant "speaks."

It may not literally be a voice, but the character experiences a thought that does not feel like their own.

This becomes a recurring motif.

---

### O-06 — Sleepwalker

The court discovers the character somewhere they should not be.

They don't remember getting there.

---

### O-07 — The Missing Conversation

Someone claims they had an important conversation with the ruler.

The ruler remembers nothing.

Choices:

- Trust them.
- Investigate.
- Pretend to remember.

---

## Medium Events

### O-08 — Two Machines

**Size:** M

Another Overclocked character appears.

Possible relationships:

- Alliance.
- Rivalry.
- Duel.
- Mutual escalation.

---

### O-09 — The Plot

**Size:** M

The implant identifies a supposed conspirator.

The information appears convincing.

Choices:

- Arrest.
- Execute.
- Secret investigation.
- Ignore.

Months later, a follow-up reveals the truth.

The information should frequently be wrong.

---

### O-10 — The Bleed

**Size:** M

A sudden fracture-risk spike occurs.

Possible results:

- Early cascade.
- Survival with permanent scarring.
- Survival with unusual insight.

---

### O-11 — The Intervention

**Size:** M

Spouse or heir asks the ruler to regress.

Personality changes the response:

- Compassionate → listen.
- Stubborn → reject.
- Paranoid → suspect manipulation.
- Ambitious → refuse to surrender power.

This should connect directly to the regression decision.

---

### O-12 — The Delegation, Revisited

The ruler delegates authority because they are becoming unreliable.

Later, another character claims that the ruler gave a completely different order.

This can feed into the eventual containment/regency arc.

---

## Large Events

### O-13 — Countdown

**Size:** L — story cycle  
**Hook:** elevated hidden fracture risk

The story begins when the character is approaching the danger zone.

Instead of showing a numerical risk value, increasingly ominous events communicate the hidden state.

#### Stage 1
Minor anomalies.

#### Stage 2
Lost time.

#### Stage 3
Contradictory memories.

#### Stage 4
Violence.

#### Stage 5
Intervention.

#### Ending
- Regression.
- Neurofracture.

This preserves the current rule that fracture risk remains hidden.

---

### O-14 — The Clarity Campaign

**Hook:** at war

The implant insists that one decisive strategy will end the conflict.

Choices:

- Follow it.
- Reject it.
- Delay.

Potential effects:

- War outcome.
- Stress.
- Fracture risk.

This gives Overclocked a genuine realm-scale consequence before Neurofracture.

---

# 6. Neurofractured — 25 Events

### Narrative purpose

**"I don't control this anymore."**

Neurofractured should not simply be Overclocked with worse numbers.

It should introduce:

- Unreliable perception.
- Hidden/random outcomes.
- Identity erosion.
- Loss of player agency.
- Named victims.
- Family consequences.
- Realm reactions.
- Endgame states.

The events should be divided into three hidden pressure bands.

---

# 6.1 Flicker — Risk 0–29

### N-F01 — Wrong Name

The character calls their heir or spouse by the name of a dead person.

---

### N-F02 — Lost Hour

An entire hour disappears from the character's memory.

---

### N-F03 — The Mirror Doesn't Blink

The character becomes convinced that their reflection moved incorrectly.

---

### N-F04 — Conversations With No One

A courtier discovers the ruler speaking alone.

---

### N-F05 — The Familiar Stranger

A trusted person suddenly feels completely unfamiliar.

---

### N-F06 — Memory of Tomorrow

The character remembers an event that has not happened yet.

---

### N-F07 — The Door

The character insists that a door exists where there isn't one.

---

### N-F08 — The Unsent Letter

The character discovers a letter in their handwriting that they do not remember writing.

---

# 6.2 Fracture — Risk 30–59

### N-F09 — Containment Breach

Expand the existing event.

Someone is injured because of the character's actions.

---

### N-F10 — Blood on the Sleeve

The character discovers blood on their clothing.

They don't know whose it is.

Use `eotg_aug_pick_victim_effect` to select a victim.

Family should be possible but rare.

---

### N-F11 — The Voice Bargains

The implant offers something:

> **Power in exchange for control.**

The player chooses an apparent option, but the actual result can be determined by a hidden roll.

---

### N-F12 — Scrambled

A personality trait changes to its opposite.

Examples:

- brave → craven
- trusting → paranoid
- patient → impatient
- compassionate → callous
- honest → deceitful

This begins identity erosion.

---

### N-F13 — The False Traitor

The implant identifies someone as a traitor.

They are innocent.

A later event reveals the truth.

---

### N-F14 — The Missing Courtier

A courtier disappears.

The ruler believes they ordered it.

Nobody else remembers such an order.

---

### N-F15 — The Second Voice

The character starts referring to the implant as **"we."**

---

### N-F16 — The Wrong War

The character believes a war is occurring when it isn't, or believes an enemy has surrendered when they haven't.

---

### N-F17 — The Familiar Change

An augmented courtier begins behaving differently.

The ruler believes they are the only person who notices.

This connects the non-ruler lifecycle to the ruler's Neurofracture story.

---

### N-F18 — The Heir's Warning

The heir confronts the ruler.

This begins the Heir's Arc.

---

# 6.3 Cascade Storm — Risk 60+

### N-F19 — The Warrant

A vanilla political mechanism reacts to the ruler's behavior.

A faction or appropriate vanilla CB/war mechanism becomes involved.

Neurofracture finally becomes a realm problem.

---

### N-F20 — Containment Regency

The spouse or heir attempts to take control.

Use the vanilla diarchy/regency framework where appropriate.

---

### N-F21 — The Massacre

Expand the existing event into the signature catastrophic Neurofracture event.

Do not always kill random characters.

Victims should be deliberately selected and saved/named where possible:

- Guard.
- Courtier.
- Knight.
- Vassal.
- Rarely family.

---

### N-F22 — The Heir's Choice

Final stage of the Heir's Arc.

The heir chooses:

- **Ally** — protect the ruler.
- **Usurp** — remove the ruler from power.
- **Kill** — end the threat.

---

### N-F23 — The Last Lucid Moment

The ruler briefly understands what has happened.

This should be rare and powerful.

Possible choices:

- Ask for help.
- Beg the heir to act.
- Embrace the implant.
- Attempt Excision.

---

### N-F24 — The Cascade

The actual terminal event.

The player should not necessarily receive a conventional choice menu.

The implant determines what happens.

Potential results:

- Violence.
- Death.
- Total Integration.
- Excision opportunity.
- Abdication.

---

### N-F25 — Dead Reckoning

The ruler attempts to reconstruct what happened.

This can lead directly into:

- Excision.
- Total Integration.
- Death.
- Restraints/Abdication.

---

# 7. Neurofractured Endgames

The four endings should be destination states rather than ordinary isolated events.

---

## Ending A — Excision

High-risk surgery removes the augmentation.

Possible outcomes:

- Death.
- Survival.
- Survival with `maimed`.

On success:

- Remove all cybernetic integration.
- Remove associated modifiers.
- Return to unaugmented.
- Apply appropriate recovery/withdrawal effects.

This provides a real caller for `eotg_clean_all_aug_modifiers`.

---

## Ending B — Total Integration

**Requirement:** high pressure + deliberate embrace of the Cascade.

The character becomes something qualitatively different.

Potential effects:

- Personality traits removed.
- Massive skill increase.
- Diplomacy heavily damaged.
- Court opinion collapses.
- Unique Total Integration trait.
- Permanent Neurofracture.

This is the "power at the cost of humanity" ending.

---

## Ending C — Death by Cascade

Risk reaches its terminal state.

Use the dedicated:

`eotg_death_cascade`

death reason.

---

## Ending D — Restraints / Abdication

The character voluntarily gives up active power.

They remain alive but are effectively removed from active rulership.

This provides an escape that does not require surgery.

---

# 8. Non-Ruler Lifecycle — 6 Events

The original design goal explicitly includes knights, generals and courtiers, but the current system does not give non-rulers a full lifecycle.

These events should be driven by `random_yearly_everyone_pulse`, filtered to augmented non-playable characters.

---

## NR-01 — The Champion Volunteers

A knight asks to be augmented.

The liege decides whether to authorize/support it.

---

## NR-02 — Your Champion's New Edge

The liege observes an augmented knight becoming unusually effective.

Potentially positive at first.

---

## NR-03 — Something Is Wrong With Him

The knight begins displaying behavioral symptoms.

---

## NR-04 — The Champion's Mistake

The knight attacks someone they should not have.

The event fires to the liege:

> **"Your champion attacked a guard."**

---

## NR-05 — The Familiar Change

A courtier's personality begins changing.

The ruler gets involved.

---

## NR-06 — The Broken Champion

A non-ruler reaches Neurofracture.

The liege chooses whether to:

- Restrain them.
- Remove implants.
- Protect them.
- Execute them.
- Ignore them.

---

# 9. Major Story Cycles

Not every medium/large event should have equal importance. Three arcs should serve as the system's signature stories.

---

## 9.1 The Patron

**Stages:** Initiation → Augmented → Enhanced

The character enters Cybernetics because somebody else pays for it.

Eventually:

> **They weren't buying the implant. They were buying you.**

The arc creates a long-term social obligation and makes the initial augmentation consequential.

---

## 9.2 The Countdown

**Stages:** Overclocked → Neurofractured

This is the primary personal horror arc.

The player never sees a raw number such as:

`Risk = 63`

Instead they experience:

**Minor anomalies → lost time → false memories → paranoia → violence → intervention → collapse.**

The hidden fracture-risk rule is therefore communicated through narrative rather than UI.

---

## 9.3 The Heir's Arc

**Stage:** Neurofractured

This is the major realm/family consequence.

### Stage 1 — Concern
The heir notices something is wrong.

### Stage 2 — Fear
The heir witnesses an episode.

### Stage 3 — Confrontation
The heir tries to intervene.

### Stage 4 — Decision

The heir chooses:

- Ally.
- Usurp.
- Kill.

This ensures Neurofracture affects the dynasty rather than ending with the ruler's personal event.

---

# 10. Personality Trait Coverage

The expanded content should deliberately cover a broad range of personality traits.

| Trait | Cybernetics expression |
|---|---|
| Brave | Challenge / intervention |
| Craven | Avoidance / augmentation |
| Calm | Phantom Orders |
| Wrathful | Violent Impulse |
| Patient | Tremor |
| Impatient | Self-repair |
| Diligent | Maintenance |
| Lazy | Neglect |
| Ambitious | Power seeking |
| Content | Resistance |
| Greedy | Patron / Market Ledger |
| Generous | Sickly Child / Copycat |
| Zealous | Purity |
| Cynical | Seeking augmentation |
| Just | Numbers, Not Faces |
| Arbitrary | Numbers, Not Faces |
| Compassionate | Sickly Child |
| Callous | Cold Calculation |
| Honest | Perfect Recall |
| Deceitful | Back-Alley Surgery / Perfect Recall |
| Trusting | Trust Protocol |
| Paranoid | False Traitor |
| Shy | The Stare |
| Gregarious | The Stare |
| Lustful | Lover's Touch |
| Chaste | Lover's Touch |
| Forgiving | Late Grief |
| Vengeful | Late Grief |
| Gluttonous | Dulled Palate / Feast You Didn't Eat |
| Temperate | Dulled Palate / Feast You Didn't Eat |
| Curious | Something Is Missing |
| Pensive | Second Self |

The purpose is not to give every trait a token option. Traits should change the **way the character experiences the cybernetics narrative**.

---

# 11. Stage-by-Stage Narrative Identity

The four tiers should have different types of stories rather than simply escalating the numbers.

## Augmented

### "This is useful."

Focus:

- Novelty.
- Social reaction.
- Performance.
- Seduction.
- Maintenance.

---

## Enhanced

### "This is becoming part of me."

Focus:

- Relationships.
- Emotional change.
- Dependence.
- Efficiency.
- Identity.

---

## Overclocked

### "Something is wrong."

Focus:

- Paranoia.
- Malfunction.
- Unreliable information.
- Loss of control.
- Impending catastrophe.

---

## Neurofractured

### "I don't control this anymore."

Focus:

- Unreliable perception.
- Forced/random outcomes.
- Identity erosion.
- Named casualties.
- Family.
- Regency.
- Political consequences.
- Irreversible endings.

---

# 12. Final Design Principle

The expanded system should not feel like:

> **"There are now 80 cybernetics popups."**

It should feel like:

### Initiation
**Why did I do this?**

↓

### Augmented
**This is amazing.**

↓

### Enhanced
**I can't imagine going back.**

↓

### Overclocked
**Something is happening to me.**

↓

### Neurofractured
**Something is controlling me.**

↓

### Endgame
**What remains of me?**

This structure turns the existing mechanical system into a coherent Cybernetics character arc while retaining its current Integration thresholds, hidden fracture-risk design, map independence, and escalating tier identity.
