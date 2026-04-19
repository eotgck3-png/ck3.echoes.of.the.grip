# ECHOES OF THE GRIP
## Government Systems Design & Architecture Document — Version 2

**Mod Prefix:** `eotg_`
**CK3 Version Target:** 1.19 "Scribe"
**Status:** Pre-Production — Closed Beta Scope
**Governments:** Gob-Corp | Corporation | Cartel | Elven Monarchy | PMC | New Cauldron Democracy

---

## Table of Contents

1. [Shared Architecture](#1-shared-architecture)
2. [Gob-Corp Government](#2-gob-corp-government)
3. [Corporation Government](#3-corporation-government)
4. [Cartel Government](#4-cartel-government)
5. [Elven Monarchy Government](#5-elven-monarchy-government)
6. [PMC Government](#6-pmc-government)
7. [New Cauldron Democracy](#7-new-cauldron-democracy)
8. [Implementation Order](#8-implementation-order)

---

## 1. Shared Architecture

All government systems are built on two shared foundations that must be implemented before any individual government file is written.

### 1.1 Mod Prefix & Naming Convention

Every mod-specific identifier is prefixed with `eotg_`. Namespace collisions in CK3 are completely silent and produce no error log entry. Discipline here is non-negotiable.

| Path | Purpose |
|---|---|
| `common/governments/eotg_[name]_government.txt` | Government files |
| `common/subject_contract_groups/eotg_[name]_contracts.txt` | Subject contract groups |
| `common/story_cycles/eotg_[name]_cycle.txt` | Story cycles |
| `common/scripted_effects/eotg_[name]_effects.txt` | Scripted effects |
| `common/scripted_triggers/eotg_[name]_triggers.txt` | Scripted triggers |
| `common/decisions/eotg_[name]_decisions.txt` | Decisions |
| `events/eotg_[name]_events.txt` | Events |
| `localization/english/eotg_[name]_l_english.yml` | Localization |
| `common/customizable_localization/eotg_[topic].txt` | Customizable loc functions |

### 1.2 Shared Localization Architecture

All dynamic name resolution is handled through customizable localization functions defined in `common/customizable_localization/`. The `.yml` files call these functions and never change as new governments are added — only the function files grow. Always put the vanilla-safe fallback block last in every function.

| Function | Resolves |
|---|---|
| `eotg_GetHoldingTypeName` | Castle rename per government |
| `eotg_GetVassalTierOneName` | County-tier title flavor |
| `eotg_GetVassalTierTwoName` | Duchy-tier title flavor |
| `eotg_GetVassalTierThreeName` | Kingdom-tier title flavor |
| `eotg_GetRulerTitle` | Empire-tier ruler title |
| `eotg_GetRealmName` | Realm name flavor |
| `eotg_GetSuccessionEventFlavor` | Succession event flavor text |
| `eotg_GetFactionName` | Dynamic faction name from leader house + government suffix |

### 1.3 Unified Market Faction Story Cycle

A single story cycle — `eotg_market_faction_cycle` — handles all corporate-flavored vassal faction tracking regardless of government type. Activates on powerful vassals. Tracks three variables:

| Variable | Purpose |
|---|---|
| `eotg_market_share` | Accumulates monthly per government type via branched scripted effects |
| `eotg_faction_allegiance` | Character reference to current dominant faction leader |
| `eotg_faction_role` | 0 = independent, 1 = member, 2 = leader |

Faction leaders receive **1.5x** the base gold multiplier versus members. Government-specific market share logic branches inside the cycle — the cycle itself is universal. One cycle per powerful vassal in memory regardless of how many government types exist.

---

## 2. Gob-Corp Government

**Key:** `eotg_gobcorp_government`
**Nations:** Gob-Ogre Trade League
**Identity:** Victorian Industrial Oligarchy

The goblin-and-ogre flavor of corporate governance. Built around 50 Trade Princes, their factional market competition, and the precarious authority of the Director-General. Internal politics are as dangerous as external wars. Distinct from the human Corporation government.

### 2.1 Title Hierarchy

| CK3 Rank | Title | Notes |
|---|---|---|
| Barony | Corporate Holding | Localization rename via `eotg_GetHoldingTypeName` |
| County | Trade Prince | Core vassal tier. The 50 Trade Princes operate here |
| Duchy | Trade Prince (Senior) | Regional monopoly holder. Same title flavor, higher rank |
| Kingdom | Merchant Lord | Regional bloc leader |
| Empire | Director-General | Figurehead and supreme authority. Elected for life |

### 2.2 Subject Contract Group: `eotg_gobcorp_contracts`

| Obligation | Description |
|---|---|
| Market Tithe | Replaces standard taxes. Three levels: Minimum Contribution, Standard Yield, Full Extraction. Output scales with vassal opinion (clan-adjacent). Higher extraction tanks opinion and faction loyalty |
| Corporate Security Levy | Replaces standard levies. Low by default — military is a corporate expense |
| Seat on the Board | Rights checkbox. Grants council position flag. Increases vote weight in No Confidence calculation. Increases faction loyalty |

### 2.3 Market Faction System

Implemented via `eotg_market_faction_cycle`. Market share accumulates based on gold income and realm size. Dominant faction named dynamically from leading Prince's house name + `Combine` suffix via `eotg_GetFactionName`. Periodic gold bonuses to all members. Faction leader receives 1.5x multiplier.

### 2.4 Succession: Wealth-Prestige Election

Elected for life by Merchant Lords and powerful Trade Princes. Candidate weighting: gold held + prestige + Board Seat status modifier. Families cycle through the title as market fortunes shift — intentional and lore-accurate.

### 2.5 Vote of No Confidence

| Step | Description |
|---|---|
| Step 1 | Decision fires when DG prestige falls below threshold OR `eotg_gobcorp_dg_instability` modifier is active |
| Step 2 | Vote weight calculated per vassal: gold + prestige + opinion + Board Seat modifier |
| Step 3 | If weighted votes reach 90% of theoretical maximum, vote passes |
| Step 4 | DG event: Step Down Gracefully or Refuse |
| Step 5a | Graceful exit: prestige + gold payout + `eotg_honorable_exit` trait |
| Step 5b | Refusal triggers `eotg_boardroom_war` CB — targeted title war for DG title only |
| Immunity | Win the war → permanent `eotg_survived_vote` flag. No further votes ever |

### 2.6 Files Required

| Folder | File |
|---|---|
| `common/governments/` | `eotg_gobcorp_government.txt` |
| `common/subject_contract_groups/` | `eotg_gobcorp_contracts.txt` |
| `common/laws/` | `eotg_gobcorp_laws.txt` |
| `common/story_cycles/` | `eotg_market_faction_cycle.txt` (shared) |
| `common/scripted_effects/` | `eotg_gobcorp_effects.txt` |
| `common/scripted_triggers/` | `eotg_gobcorp_triggers.txt` |
| `common/script_values/` | `eotg_gobcorp_values.txt` |
| `common/decisions/` | `eotg_gobcorp_decisions.txt` |
| `common/casus_belli_types/` | `eotg_boardroom_war.txt` |
| `events/` | `eotg_gobcorp_vote_events.txt`, `eotg_gobcorp_faction_events.txt` |
| `localization/english/` | `eotg_gobcorp_l_english.yml` |

---

## 3. Corporation Government

**Key:** `eotg_corporation_government`
**Nations:** P&D Co, Helix Corp remnants, human corporate minor nations
**Identity:** Cyberpunk Corporate Oligarchy

Human-nation corporate governance inspired by Cyberpunk 2077 corporate aesthetics — sleek, ruthless, omnipresent but polished at the top. Mechanically distinct from Gob-Corp: cleaner board structure, fewer but more powerful vassal nodes, higher external diplomatic capability. P&D Company is the primary example — infamous for monopolies, forced labor, exploitation, economic colonization, and occasional humanitarian PR stunts.

### 3.1 Title Hierarchy

| CK3 Rank | Title | Notes |
|---|---|---|
| Barony | Corporate Holding | Renamed via `eotg_GetHoldingTypeName` |
| County | Account Director | Cutthroat bottom tier. Primary Sabotage Rival scheme users |
| Duchy | Operations Chief | Middle management. Bridges the cutthroat floor and polished top |
| Kingdom | Regional Director | Board-eligible tier. Only vassals with Board seats |
| Empire | CEO | Supreme authority. Elected by Board of Regional Directors |

### 3.2 Two-Tier Identity

Cutthroat at the bottom, intrigue-diplomacy-stewardship focused at the top. Account Directors and Operations Chiefs scheme against each other using the Sabotage Rival scheme. Regional Directors and the CEO play a slow Board Influence game. The transition between tiers is the core political experience.

### 3.3 Sabotage Rival Scheme

| Parameter | Value |
|---|---|
| File | `common/scheme_types/eotg_sabotage_rival.txt` |
| Type | Hostile — has secrecy, can be discovered |
| Primary skill | Intrigue (schemer), Stewardship (target resistance) |
| Agents | Up to 3 — Account Directors or Operations Chiefs in same realm |
| `is_valid` | Both characters have `eotg_corporation_government`. Both are vassals of same liege |
| `on_success` | Applies `eotg_corporate_undermined`: -15% monthly income, -10 vassal opinion, -10% prestige gain. Duration: 3 years. Stackable |
| `on_discovered` | Schemer takes prestige hit. Target gains a hook on schemer |

### 3.4 Board Influence System

`eotg_board_influence` is a character variable on the CEO. Decays monthly. Spent by major decisions (war declaration, succession law changes, etc.). Earned through successful diplomacy events, granting Board Seat obligations, and completing certain schemes. Running out unlocks the Corporate Vote of No Confidence decision for powerful vassals.

Board consists exclusively of Regional Directors.

### 3.5 Succession: Surface Election with Hidden Manipulation

Surface election weighted by stewardship + gold among Regional Directors. Hidden layer: **Corporate Interference** decision available before election fires. CEO-elect spends gold and intrigue to plant a modifier suppressing a rival candidate's vote weight. Discoverable only via Sabotage Rival scheme during the election window. Very P&D Co energy.

### 3.6 Hostile Acquisition

| Stage | Description |
|---|---|
| Initiator | Regional Director to Regional Director character interaction |
| Cost | Gold threshold scaled to target's realm size |
| Accept | Target paid out in gold. Title transfers peacefully |
| Refuse | Triggers `eotg_proxy_war` CB — costs both sides gold rather than levies. Winner takes disputed title |

### 3.7 Files Required

| Folder | File |
|---|---|
| `common/governments/` | `eotg_corporation_government.txt` |
| `common/scheme_types/` | `eotg_sabotage_rival.txt` |
| `common/subject_contract_groups/` | `eotg_corporation_contracts.txt` |
| `common/modifiers/` | `eotg_corporation_modifiers.txt` |
| `common/scripted_effects/` | `eotg_corporation_effects.txt` |
| `common/scripted_triggers/` | `eotg_corporation_triggers.txt` |
| `common/script_values/` | `eotg_corporation_values.txt` |
| `common/casus_belli_types/` | `eotg_proxy_war.txt` |
| `events/` | `eotg_corporation_scheme_events.txt`, `eotg_corporation_board_events.txt` |

---

## 4. Cartel Government

**Key:** `eotg_cartel_government`
**Nations:** Slate Syndicate, criminal nations
**Identity:** Paranoid Survival, Brutal Expansion, Raiding

Represents nations that are criminal enterprises that achieved statehood — primarily the Slate Syndicate, evolved from the ruins of the Concrete Cartel. Dread replaces gold as the primary currency of power. Internal politics are violent rather than procedural. The Grand Underlord is always under threat from within.

### 4.1 Title Hierarchy

| CK3 Rank | Title | Notes |
|---|---|---|
| Barony | Den | Renamed via `eotg_GetHoldingTypeName` |
| County | Street Lord | Local crime lord controlling a territory |
| Duchy | Underboss | Regional cartel leader |
| Kingdom | Boss | Major faction head |
| Empire | Grand Underlord | Supreme criminal authority |

### 4.2 Dread System

Leans heavily into vanilla CK3 dread with modified thresholds. Dread decays **faster than vanilla**. Replenished by Loyalty Tax collection and raiding victories. A dedicated building line nullifies the faster decay rate when maxed out — long-term infrastructure goal rewarding patient play alongside the aggressive raiding treadmill.

### 4.3 Loyalty Tax

Periodic flat demand from the Grand Underlord to all Syndicate Bosses. Demand scales with title rank and number of titles held. Paying maintains dread. Refusing bleeds dread and feeds faction mechanics. This is the treadmill that keeps the Grand Underlord constantly active.

### 4.4 Raiding

Tribal raiding system reflavored with criminal aesthetics. **No distance restriction** — any target, anywhere. Consistent with Slate Syndicate lore of raiding Belinore's shipping lanes across galactic distances. Raiding victories replenish dread.

### 4.5 Faction System

All four factions run simultaneously. Each Syndicate Boss can only join **one faction at a time** — they commit to an angle of attack. Factions operate independently of each other.

| Faction | Demand | Escalation on Refusal |
|---|---|---|
| The Shakedown Faction | Reduce Loyalty Tax rate permanently | Economic standoff — collective withholding of next Loyalty Tax payment, dread bleeds until resolved within a time window |
| The Hostile Takeover Faction | Faction leader's own claim to Grand Underlord title | Civil war for Grand Underlord title only |
| The Defection Faction | Peaceful release to flip territory to rival nation | Defecting bosses invite neighboring power to annex them, triggering external war |
| The Purge Demand Faction | Elimination of a specific Boss (chosen by faction leader from: most powerful Boss, highest dread Boss, or worst opinion Boss) | Faction backs the target Boss instead, flipping the power dynamic |

### 4.6 Succession

Violent. The Hostile Takeover Faction is the primary succession mechanism. No formal election. Grand Underlord is deposed through violence or dies and the strongest claimant takes power.

---

## 5. Elven Monarchy Government

**Key:** `eotg_elven_monarchy_government`
**Nations:** Thae'Viriel Cohorts, Ado'Quor, Sin'Dal Sovranty, Lord Protector's Court, Q'Xorlarrin Domain, elven minors
**Identity:** Divine-Right Isolationist Monarchy

Broad government type used by multiple elven nations — from small 1-3 province proud holdouts to Thae'Viriel's galaxy-spanning Cohorts. Gro'May's power comes from his religious title (Eternal King) rather than his government tier. Mechanically closest to vanilla feudal but with significant isolationism, non-elven second-class mechanics, and the Eternal Court confirmation system.

### 5.1 Title Hierarchy

| CK3 Rank | Title | Notes |
|---|---|---|
| Barony | Star Hold | Renamed via `eotg_GetHoldingTypeName` |
| County | Star Warden | Local elven lord |
| Duchy | Celestial Lord | Regional elven noble |
| Kingdom | Eternal Regent | Senior vassal in the Eternal Court structure |
| Empire | Starborn Sovereign | Political emperor title. Separate from Gro'May's religious Eternal King title |

### 5.2 Isolationism Scaling

Negative opinion impact on other heritage groups scales with ruler's title rank. Implemented as `eotg_elven_isolationism_penalty` script value reading `highest_held_title_tier`. **Outward only** — the elven ruler looks down on outsiders, not the reverse. A county-tier elven lord is merely snobbish; a Starborn Sovereign actively repels galactic diplomacy.

### 5.3 Non-Elven Second-Class Mechanics

| Mechanic | Description |
|---|---|
| Council exclusion | Non-elven characters cannot hold council positions under Elven Monarchy rulers |
| Heir exclusion | Non-elven characters cannot be heirs to Elven Monarchy titles |
| Revolt risk scaling | Scales with proportion of non-elven holdings — small conquest manageable, half-non-elven empire becomes genuinely unstable |

### 5.4 Eternal Court Confirmation

On succession, the heir requires ratification from powerful vassals. Outcome determined by number of powerful vassals with positive opinion of heir + length of previous ruler's reign.

| Outcome | Condition | Effect |
|---|---|---|
| Confirmed with bonus | High vassal support + long reign | Heir receives large legitimacy and prestige bonus |
| Confirmed with penalty | Low vassal support | Heir takes power with legitimacy penalty |
| Regency fires | Mixed support | Court deliberates, regency period while outcome resolves |
| Succession crisis | Hostile Court | Rival claimant backed by dissenting Court members |

### 5.5 Cultural Loyalty System

Gro'May can call on small elven minor nations diplomatically regardless of faith. Cultural loyalty transcends religious divides — elven solidarity is deeper than theology. Elven minors are fiercely independent and expansionist but respond to Gro'May's diplomatic calls.

### 5.6 Succession & Laws

Strict primogeniture with Eternal Court ratification layer on top. Legitimacy uses vanilla CK3 legitimacy system. Starlit Concord mechanics are **post-beta scope**.

---

## 6. PMC Government

**Key:** `eotg_pmc_government`
**Nations:** Multiple races and cultures galaxy-wide
**Identity:** Proto-Corporate Military State

The PMC government is to the Corporation government what Tribal is to Feudal — a foundational, military-focused proto-corporate state that can evolve into a full Corporation over time. Generic enough to work across multiple races and cultures. Knights are called **Operators**.

### 6.1 Title Hierarchy

| CK3 Rank | Title | Notes |
|---|---|---|
| Barony | Garrison | Renamed via `eotg_GetHoldingTypeName` |
| County | Contractor | Ground-level operational territory holder |
| Duchy | Field Director | Regional operational command |
| Kingdom | Executive Commander | Senior strategic leadership |
| Empire | Contractor-General | Top of the PMC structure. Distinct from Gob-Corp's Director-General |
| Knights | Operators | PMC knight equivalent |

### 6.2 Contract War System

Primary unique mechanic. When a nearby ruler with positive relations enters a war, a pulse event offers the Contractor-General a contract at one of three tiers:

| Tier | Reward | Restriction |
|---|---|---|
| Minor Contract | Small gold and prestige | None |
| Standard Contract | Meaningful gold and prestige | None |
| Exclusive Contract | Large gold and prestige | Locks out other contracts AND prevents Contractor-General from declaring offensive wars for contract duration |

**Controversy:** Applies `eotg_pmc_controversy` modifier — reduces opinion in holdings proportional to contract tier. Monthly chance to fire revolt event in counties above controversy threshold. Controversy ripples to **vassal holdings AND to the contract client's lands**. Client receives notification event with option to terminate early at prestige cost.

**Council recommendation events:** Council members fire recommendation events for contracts. Accepting a recommendation grants a small bonus (e.g. Marshal recommending Standard Contract → martial opinion boost).

### 6.3 Council — Modified Positions

Court Chaplain is replaced by **Logistics Officer** (Stewardship skill).

| Task | Effect |
|---|---|
| Manage Supply Lines | Reduces army maintenance cost |
| Secure Resources | Boosts gold income from domain |
| Audit Contracts | Reduces controversy from active contracts |

### 6.4 Loss of Command Deposition

| Stage | Description |
|---|---|
| Trigger | Powerful vassals collectively withdraw forces from Contractor-General's command |
| Window | One year to buy back loyalty via gold or prestige concessions |
| Extensions | Additional time purchasable. Each extension costs progressively more gold |
| Ally intervention | Positive-relationship vassals have a chance to fire events buying more time |
| Expiry | Most powerful Executive Commander becomes acting Contractor-General automatically. No war needed |

### 6.5 PMC to Corporation Evolution

| Requirement | Description |
|---|---|
| Gold threshold | Accumulated corporate wealth |
| Prestige threshold | Military success and reputation |
| Land holding | Minimum realm size |
| Title rank | Must hold at least one kingdom tier title |

On transition: Major decision fires. **Player receives text input event** to rename the title — their Corporation's name. AI defaults to previous primary title name. Government switches to `eotg_corporation_government`.

---

## 7. New Cauldron Democracy

**Key:** `eotg_new_cauldron_government`
**Nations:** New Cauldron (exclusive — not a template for other nations)
**Identity:** Mercenary-Origin Democratic Republic

Unique government exclusive to New Cauldron, built around their specific political history. Democratic foundations since 131 AG. First President: Mikey the Great. US-inspired structure of constituent States electing a President. The 7th Mercenary Legion is a semi-autonomous military arm in the Myr Clusters; its full political status is resolved through the Myr Cluster struggle system (discussed separately, post-beta scope).

### 7.1 Title Hierarchy

| CK3 Rank | Title | Notes |
|---|---|---|
| Barony | District | Renamed via `eotg_GetHoldingTypeName` |
| County | Governor | Elected or appointed regional administrator |
| Duchy | Senator | Senate seat if direct vassal of President title |
| Kingdom | State | Constituent kingdom. One Senate representative per State |
| Empire | President | Elected by constituent States. 15-year terms, two-term limit |

### 7.2 Senate System

**Composition:** One representative per Kingdom-tier State + direct duchy-level vassals of the President title. Senate operates independently while President governs — President loses their Senate seat for the duration of their presidency.

| Mechanic | Description |
|---|---|
| Senate Veto | Major decisions go to Senate vote. Hostile Senate can block entirely. President can override at significant legitimacy cost |
| War declaration | Offensive wars require Senate majority vote. Defensive wars are automatic |
| Emergency Powers | Once per term decision. Bypasses Senate for one offensive war. High legitimacy cost. Senate notified via event — cannot stop it but react with opinion penalties |
| Vote buying | Senators can be bought with gold. Discovery hits legitimacy AND triggers Senate censure event |

### 7.3 Presidential Election

**Normal cycle:** Last two years of a term trigger the campaign phase.

**Mid-term death:** Special event announcing the President's death fires to all realm characters, then campaign phase triggers as normal.

Candidate weighting: stewardship + gold. Two-term limit strictly enforced.

### 7.4 Campaign Decisions

| Decision | Mechanic |
|---|---|
| Make Campaign Promise | No cost now. Creates timed obligation after election. Breaking it has opinion consequences |
| Rally the Districts | Costs gold. Boosts vote weight in specific regions |
| Attack Rival's Record | Intrigue-based. Damages rival candidate's vote weight. Risk of scandal |
| Public Address | Costs prestige. Realm-wide event. High diplomacy = broad vote weight boost. Low diplomacy = backfires and boosts rival |
| Forge Alliance | Transparent deal — offer rival kingdom holder a post-election council position for their Senate vote. Publicly visible, rivals can counter-offer |

### 7.5 Vice President

Runner-up in the Presidential election becomes Vice President. Purely a succession safety net — no mechanical function during normal governance. If Vice President inherits mid-term due to President's death, they receive a **30-year opinion bonus** from other rulers of the same culture, representing the galaxy rallying around New Cauldron in mourning. They serve only until a new election is concluded.

### 7.6 Former President Modifier

When a President's term ends and they return to their State title, they receive `eotg_former_president`:

- Elevated Senate influence
- Opinion boost with other rulers
- Income boost

Former Presidents become genuine kingmakers in subsequent elections.

### 7.7 Lore Anchors

| Reference | Detail |
|---|---|
| Founded | 131 AG. First President: Mikey the Great |
| Elections | Every five years since founding (15-year terms in gameplay) |
| Mercenary Legions | Dominated by the Brass Concord by 1370 AG |
| Vault Stance | Elite multi-racial force. Opened to non-humans 1020 AG |
| 7th Mercenary Legion | Semi-autonomous in Myr Clusters. Political status resolved via Myr Cluster struggle — post-beta scope |
| Irreligious | Secular stance reflected through culture, not government mechanics |

---

## 8. Implementation Order

| Phase | Government | Notes |
|---|---|---|
| Phase 0 — Foundations | Shared systems | `eotg_market_faction_cycle` + all customizable localization function stubs. Nothing else written until these exist |
| Phase 1 | Gob-Corp | First complete government. Establishes contract group, vote chain, and faction cycle template |
| Phase 2 | Elven Monarchy | Lowest complexity. Good momentum builder after Gob-Corp |
| Phase 3 | PMC | Contract War system, Loss of Command, Logistics Officer. Establishes evolution pathway to Corporation |
| Phase 4 | Corporation | Builds on PMC evolution foundation. Sabotage Rival scheme, Board Influence, Hostile Acquisition |
| Phase 5 | Cartel | Four-faction system, Loyalty Tax, raiding, dread building line |
| Phase 6 | New Cauldron Democracy | Most complex. Presidential election, Senate system, campaign decisions, Vice President chain |
| Post-Beta | Nikios Khanate | Separate unique government. Design spec not yet written |
| Post-Beta | 7th Mercenary Legion | Resolved through Myr Cluster struggle system |

### 8.1 CK3 Tiger Validation

Run CK3 Tiger after every file addition. Check `database_conflicts.log` after each government addition to confirm no vanilla overrides are being lost to load order. Do not let validation errors accumulate across sessions.

### 8.2 Version Target

CK3 1.19 "Scribe" (open beta, March 2026). Subject contract group API renamed from "vassal contracts" in 1.12 — verify all contract group references match 1.19 vanilla file structure. Regenerate `script_docs` after every major patch.

### 8.3 Governments NOT in Closed Beta

- `eotg_corporation_government` is reachable via PMC evolution but not independently assigned to any starting nation in the closed beta
- Nikios Khanate government is post-beta scope
- New Cauldron Democracy should be implemented last — most complex government in the mod

---

*Echoes of the Grip — Government Systems Design Document v2*
*`eotg_` prefix | CK3 1.19 target | 6 governments + 2 post-beta*
