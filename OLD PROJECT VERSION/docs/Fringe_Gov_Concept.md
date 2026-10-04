# Fringe Government Design Document (CK3 Mod Implementation)

## Overview

The **Fringe Government** is a custom Crusader Kings III government type designed for unstable frontier realms built around raiding, temporary alliances, charismatic warlords, and cyclical collapse.

The intended gameplay fantasy is:

* rapid military expansion
* unstable internal politics
* decentralized authority
* powerful subordinate captains
* succession crises
* splintering realms
* eventual reform into more stable systems

This government should naturally create:

* temporary large empires
* civil wars
* breakaway states
* internal betrayal
* recurring cycles of conquest and collapse

The government is intentionally unstable and should not be sustainable long-term without reform.

---

# Core Design Goals

## Intended Gameplay Loop

1. Expand aggressively
2. Reward warfare and raiding
3. Punish long-term peace
4. Increase instability with realm growth
5. Trigger internal fragmentation
6. Force player toward reform or repeated collapse

---

# Government Definition

## Government Name

`fringe_government`

---

## Government Fantasy

Fringe realms are loose coalitions of:

* raiders
* pirates
* scavenger clans
* outlaw fleets
* mercenary bands
* frontier warlords

They are held together through:

* fear
* loot
* military success
* personal loyalty

NOT through:

* bureaucracy
* law
* institutions

---

# CK3 Implementation Notes

The following mechanics are designed around what is realistically possible in CK3 scripting.

The design avoids systems that would require engine-level hardcoding.

---

# Government Mechanics

# 1. Grip System

## Purpose

Represents central authority over captains and subordinate warlords.

Since CK3 does not support custom government authority systems directly, Grip should be implemented using:

* character modifiers
* realm modifiers
* scripted values
* yearly pulse events

---

## Grip States

### High Grip

Modifier effects:

* reduced faction military power
* increased vassal opinion
* reduced liberty faction chance
* increased control growth

### Medium Grip

No major effects.

### Low Grip

Modifier effects:

* increased faction creation
* increased independence faction strength
* reduced vassal opinion
* increased hostile scheme power against ruler
* reduced taxes
* reduced levies

---

## Grip Gain Sources

| Action                      | Suggested Effect |
| --------------------------- | ---------------- |
| Winning wars                | increase Grip    |
| Successful raids            | increase Grip    |
| Executing rebels            | increase Grip    |
| Holding feasts for captains | increase Grip    |
| Conquering territory        | small increase   |

---

## Grip Loss Sources

| Action                | Suggested Effect |
| --------------------- | ---------------- |
| Long periods of peace | lose Grip        |
| Losing wars           | lose Grip        |
| Debt                  | lose Grip        |
| Large realm size      | passive decay    |
| Failed raids          | lose Grip        |
| Low prestige          | lose Grip        |

---

## Implementation

Recommended implementation:

* hidden variable tracked on ruler
* yearly maintenance event adjusts value
* modifiers applied dynamically depending on thresholds

Example thresholds:

* 80+ = High Grip
* 40–79 = Stable Grip
* below 40 = Low Grip

---

# 2. Captain System

## Purpose

Fringe vassals are semi-independent captains rather than traditional nobles.

This should primarily be represented through:

* opinion modifiers
* events
* faction pressure

---

## Captain Expectations

Captains expect:

* warfare
* loot
* rewards
* territory grants

Failure to satisfy them increases revolt risk.

---

## Recommended Mechanics

### During Peace

Apply:

* negative vassal opinion
* increased faction desire

---

### After Successful Raids

Apply:

* positive opinion modifier
* reduced faction pressure

---

### Captain Rivalries

Random events generate:

* rivalries
* duels
* murder schemes
* internal conflicts

---

# 3. Peace Decay Mechanic

## Purpose

Fringe realms should destabilize during extended peace.

---

## Implementation

Yearly check:

If ruler has:

* no wars
* no raids
* peace longer than X years

Apply:

* prestige loss
* Grip loss
* vassal opinion penalties

---

## Suggested Thresholds

| Peace Duration | Effect             |
| -------------- | ------------------ |
| 2 years        | small unrest       |
| 5 years        | major unrest       |
| 10 years       | severe instability |

---

# 4. Overextension System

## Purpose

Large Fringe realms should become unstable automatically.

---

## Implementation

Based on:

* realm size
* number of vassals
* distance penalties

---

## Effects

Large realms receive:

* Grip decay
* increased faction strength
* reduced vassal opinion

---

## Suggested Scaling

| Realm Size | Effect             |
| ---------- | ------------------ |
| Small      | no penalty         |
| Medium     | minor instability  |
| Large      | strong instability |
| Massive    | severe instability |

---

# 5. Succession Instability

## Purpose

Succession should be dangerous.

---

## CK3 Limitation

Cannot dynamically split realms outside succession laws easily.

Instead use:

* succession events
* claimant factions
* liberty factions
* independence revolts

---

## Recommended Mechanics

On ruler death:

Chance to trigger:

* independence factions
* pretender uprisings
* captain rebellions

---

## Additional Effects

New ruler may receive:

* temporary low Grip
* short reign penalties amplified

---

# Government Bonuses

## Advantages

| Modifier                      | Effect    |
| ----------------------------- | --------- |
| Raid efficiency               | increased |
| Army maintenance during raids | reduced   |
| Prestige from battles         | increased |
| Conquest CB cost              | reduced   |
| Levy reinforcement            | increased |

---

## Disadvantages

| Modifier             | Effect    |
| -------------------- | --------- |
| Development growth   | reduced   |
| Control growth       | reduced   |
| Vassal factionalism  | increased |
| Succession stability | reduced   |
| Tax income           | unstable  |

---

# Casus Belli

# CB: Frontier Raid

## Purpose

Raid neighboring realms for gold/prestige.

---

## Outcomes

If successful:

* gain gold
* gain prestige
* gain Grip

If failed:

* lose prestige
* lose Grip

---

# CB: Seize Territory

Low-cost conquest CB.

Restricted to neighboring rulers.

---

# CB: Punitive Raid

Target ruler who insulted or rivaled Fringe ruler.

Rewards:

* prestige
* fear modifier
* ransom opportunities

---

# Decisions

# Decision: Distribute the Spoils

## Requirements

* recently completed raid or war
* sufficient gold

---

## Effects

### Positive

* increase Grip
* increase vassal opinion
* reduce faction pressure

### Negative

* lose gold

---

# Decision: Rule Through Fear

## Effects

### Positive

* increase Grip
* reduced faction power

### Negative

* increased murder scheme chance
* tyranny gain
* opinion penalties for compassionate characters

---

# Decision: Call the Warbands

## Effects

### Positive

* temporary levy increase
* knight effectiveness increase

### Negative

* reduced income
* county control penalties

---

# Decision: Raid the Frontier

## Effects

Creates temporary modifier:

* raid bonuses
* movement bonuses

---

# Decision: Suppress Breakaway Captains

## Outcomes

### Peaceful Suppression

* reduced revolt risk
* cost gold/prestige

### Violent Suppression

* possible rebellion
* possible execution events

---

# Major Decision: Forge a Unified Fringe

## Purpose

Late-game temporary stabilization.

---

## Requirements

* large realm
* high prestige
* high dread
* high Grip

---

## Effects

### Positive

* reduced faction pressure
* conquest bonuses
* vassal fear increase

### Negative

* severe succession crisis on death
* increased claimant faction power after ruler death

---

# Reformation System

## Purpose

Transition Fringe realms into stable governments.

---

# Reform Path 1: Cartel State

## Fantasy

Raiders evolve into organized criminal syndicates.

---

## Effects

### Gains

* stronger economy
* corruption mechanics
* extortion bonuses

### Losses

* weaker raiding bonuses

---

## Suggested Government Conversion

Convert to:

* clan variant
* republic-style hybrid if available

---

# Reform Path 2: PMC State

## Fantasy

Warlords become professional military contractors.

---

## Effects

### Gains

* stronger men-at-arms
* contract income
* improved succession stability

### Losses

* weaker raid economy

---

# Reform Path 3: Corporate Frontier State

## Fantasy

Frontier raiders evolve into exploitative industrial rulers.

---

## Effects

### Gains

* development bonuses
* tax bonuses

### Losses

* reduced military aggression bonuses

---

# Reform Path 4: Feudalization

## Fantasy

Warlords become legitimate rulers.

---

## Effects

### Gains

* stable succession
* long-term growth

### Losses

* raid-focused gameplay

---

# Reform Crisis

## Purpose

Reforming should create resistance.

---

## Possible Outcomes

* traditionalist revolt
* captain rebellion
* splinter realms
* assassination attempts

---

# Event Chains

# Captain Event Chain

## Event: The Captains Demand Their Share

### Trigger

After successful war or raid.

---

## Choices

### Share Generously

Effects:

* gain vassal opinion
* gain Grip
* lose gold

---

### Keep Most for Yourself

Effects:

* gain gold
* lose Grip
* increase faction pressure

---

### Favor One Captain

Effects:

* one captain gains opinion
* others lose opinion
* rivalry chance

---

# Event: A Captain Refuses Orders

## Trigger

Low Grip or low opinion captain.

---

## Choices

### Tolerate

Effects:

* lose Grip

---

### Public Punishment

Effects:

* gain dread
* rebellion chance

---

### Attempt Assassination

Effects:

* murder scheme event chain

---

# Event: Mutiny in the Void

## Trigger

Very low Grip.

---

## Outcomes

* rebel faction forms
* captain gains troops
* possible independence war

---

# Succession Events

# Event: Who Commands the Fleet?

## Trigger

Ruler death.

---

## Outcomes

* claimant factions
* captain alliances
* temporary chaos modifier

---

# Event: The Outer Clans Break Away

## Trigger

Large realm succession.

---

## Outcomes

* independence factions created
* border vassals gain disloyalty modifiers

---

# Collapse Events

# Event: Loot Riots

## Trigger

Low gold after wars.

---

## Effects

* county control loss
* development loss
* popular opinion penalties

---

# Event: Blood Feud

## Trigger

Captain rivalries.

---

## Outcomes

* duels
* murders
* internal wars

---

# Raid Events

# Event: The Great Plunder

## Trigger

Major successful raid.

---

## Effects

* large prestige gain
* temporary vassal happiness
* future greed modifier

---

# Event: Raid Gone Wrong

## Trigger

Failed raid.

---

## Effects

* prestige loss
* captain dissatisfaction
* Grip loss

---

# AI Behavior

## AI Goals

Fringe rulers should:

* raid frequently
* expand aggressively
* overextend often
* collapse periodically

---

## AI Weights

Increase:

* war declaration tendency
* raid targeting

Decrease:

* peaceful development behavior

---

# Intended Emergent Outcomes

The system should naturally generate:

* pirate kingdoms
* unstable empires
* civil wars
* splinter states
* mercenary breakaways
* criminal proto-states

---

# Final Design Philosophy

The Fringe Government should always feel unstable.

Players should constantly feel:

> "I can conquer this region — but can I survive holding it?"

The ideal outcome is cyclical instability rather than permanent dominance.
