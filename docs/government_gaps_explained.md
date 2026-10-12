# The four governments: what's missing, in plain terms

**For:** the owner. **Written:** 2026-10-11, by eotg-architect.
**Covers:** PMC, Corporation, Cartel and Trade Oligarchy (Gob-Corp internally).
**Based on:** the government template (`docs/specs/government_template.md`) and the five QA reports of 2026-10-11. File-level evidence is listed at the end.

---

## 1. The short version

All four governments are **playable reskins of feudal**. You can pick a ruler, and on paper the dynasty carries on after they die. Each has its own name, colour, ranks, knight term, vassal numbers and a few character bonuses. That is what the first build phase (G1) set out to do.

A distinct government gives you a different daily job: its own number to watch and spend, a different deal with your vassals, inheritance that matches the fiction, and a way in and out during play. None of the four has that yet. The Cartel comes closest, through vanilla's tribute system.

| Design question | PMC | Corporation | Cartel | Trade Oligarchy |
|---|---|---|---|---|
| Q1. What do you *do*? | Missing: you conquer and inherit, like feudal | Missing | Partial: you can offer tributary status (borrowed from vanilla) | Missing |
| Q2. Signature resource | Missing: "standing" is named but not built | Missing: "board influence" is named but not built | Partial: uses vanilla dread, but nothing Cartel-specific feeds it or spends it | Missing: "market share" is named but not built |
| Q3. Vassal relationship | Partial: own terms, feudal shape | Partial | Partial | Partial |
| Q4. Succession | Partial: oldest child inherits, under a name that says rank is earned | Contradicts the fiction: a board, but oldest child inherits | Partial: oldest child, called "Council Succession" | Contradicts the fiction: "no single head", but oldest child inherits |
| Q5. Getting in and out | Missing: test-only switches | Missing | Missing | Missing |
| Q6. AI behaviour | Partial: vanilla defaults | Partial | Partial: vanilla tribute AI | Partial |
| Q7. What you see on screen | Partial: name, ranks, colour; placeholder icon | Partial | Partial: dread already has vanilla UI | Partial |

---

## 2. What makes a government feel distinct

Paradox only builds a new government mechanic when the **core action** differs from feudal's "conquer land, then pass it to your heir". If a ruler still conquers and inherits, a new label and some bonuses are enough: a reskin, which is a legitimate build. If the fiction says the ruler does something else, the mechanics must say so too, or the player is playing feudal under another name.

The vanilla examples, as a player meets them:

- **Feudal: contracts.** Your relationship with each vassal is a negotiated deal over tax and levies, with special rights you can trade. Conquest and inheritance are the game.
- **Clan: house unity.** Your family's cohesion is a meter. Vassals pay by their opinion of you, not by contract. Keeping the house together is the job.
- **Nomad: herd and obedience.** Your wealth is livestock, your vassals stay loyal only while obedient, and you move when the pasture runs out.
- **Administrative: influence.** Land comes with an office and goes when you lose the office, but your house is permanent. You play politics for influence to hold governorships and climb toward the throne.
- **Mandala: radiance.** You grow by pulling neighbours in as tributaries through prestige and devotion, not mainly by war.

Each has a verb that isn't "conquer", a number measuring how well you do it, a vassal model built around that number, and a screen where you watch it move.

---

## 3. The gaps all four share

### 3.1 No signature resource

**What's missing.** Three of the four have a reserved name for their number (PMC standing, Corporation board influence, Trade Oligarchy market share), but no part of the game uses any of them yet. The Cartel uses vanilla dread, which every ruler already has.

**Why it matters.** There is nothing particular to the government to gain, spend or lose. It also blocks events: every flavour event must move or read its system's resource (the rule v1's do-nothing events taught us), so G2 events have nothing to attach to yet.

**What closing it involves.** The template's default: a scripted 0–100 number on each ruler, changed only through one capped effect, set up on gaining the government and cleared on leaving it. You'd see it without custom interface work, through a character modifier that scales with the number (in the character window, with a tooltip) and a story-cycle counter showing the value. A top-bar readout is an optional later upgrade.

### 3.2 No core action of their own

**What's missing.** Apart from the Cartel's borrowed tribute offer, the only government-specific decisions are debug switches. A PMC sells no force, a Corporation makes no deals, and Trade Princes don't compete for market share.

**Why it matters.** This is the difference between "feudal with different numbers" and a new way to play. The descriptions promise things no mechanic delivers: directors scheming for the board's favour, power bought and counted, rank earned in the field.

**What closing it involves.** At least one top-ruler decision and one vassal decision per government, each moving the resource: PMC "take a contract" and "deliver", Corporation "deals", Cartel decisions that spend dread. They're gated on the government's flag, so they don't depend on any title or map. Any that fire new events need your approval.

### 3.3 No way to adopt or leave the government

**What's missing.** There's no in-game decision to become a PMC, Corporation, Cartel or Trade Oligarchy, and none to leave one. Nothing has been decided about what happens if a ruler loses all their land or is conquered by another government.

**Why it matters.** Vanilla changes governments through decisions (tribal to feudal, adopting mandala). Without them, these governments exist only where history puts them, and a player can never grow into one.

**What closing it involves.** An entry decision and an exit decision per government, following vanilla's conversion decisions, including what happens to the resource on the way in and out. The spec already plans a PMC-to-Corporation evolution, much as tribal grows into feudal.

### 3.4 Vassal terms shaped like feudal ones

**What's missing.** Each government has its own vassal contract with its own names and numbers. Underneath, though, each is feudal's two sliders (tax and levies), copied level by level. None of the governments has a third obligation, a government-specific opinion of the liege, or a bonus that applies only to the top ruler.

**Why it matters.** Vassal relations are where a government's character shows daily. Today a Cartel boss and a Corporation director bargain exactly as a feudal count does.

**What closing it involves.** Three levels: feudal sliders with new numbers (all four have this); an obligation that reads the resource, as vanilla's tribal contract scales with the liege's prestige; or a different kind of subject. G2 plans a third obligation each (board seat, enforcement rights, field commission), with something that reads it.

### 3.5 Succession that contradicts the fiction

**What's missing.** All four use "oldest child inherits everything":

| Government | Law name | What the fiction says |
|---|---|---|
| PMC | Command Succession | rank is earned by results in the field |
| Corporation | Executive Succession | run by a board |
| Cartel | Council Succession | a council of bosses |
| Trade Oligarchy | Charter Succession | no single head |

**Why it matters.** Succession is when the player feels the government most. A "board" that always hands the company to the CEO's eldest child is a hereditary monarchy.

**What closing it involves.** Either accept single heir for now and rename the laws so they stop promising otherwise, or have G2 build elective laws (board vote, wealth-weighted vote, takeover, command pick), with electors limited to the dynasty or house so the player's game doesn't end. This is CB-53 and needs your ruling.

### 3.6 Thin AI and grant settings

**What's missing.** The AI has vanilla's default behaviour plus weights on laws and contracts. Nothing tells the AI how to grant land to vassals of these governments, or which other governments they may grant to. Feudal can create clergy vassals under theocratic or ecclesiastical government; these four can't.

**Why it matters.** It shows only decades in, when AI realms drift, churn laws or go bankrupt. Once a resource exists, the AI must also know how to earn and spend it.

**What closing it involves.** The grant fields, plus an AI weight on each new decision that reads the resource, built alongside each resource.

### 3.7 Reachable only by picking on the map

**What's missing.** No bookmark character starts with these governments, and vanilla's ruler designer only ever makes tribal, clan or feudal rulers. The test sub-mod's history places one realm of each, and picking that ruler is the only way in.

**Why it matters.** Fine for testing. In a real campaign, a player who doesn't pick one of those rulers never meets these governments unless entry decisions (3.3) exist.

**What closing it involves.** Entry decisions do most of the work. Bookmark entries wait for the real map (Gate 1).

---

## 4. Government by government

### PMC

**Intended feel.** A military state run as a business: a command hierarchy that sells force, earning income and reputation outside its own realm. Knights are Operators.

**What differs from feudal today.**
- Vassals pay little tax but owe a lot of troops: 5% tax at the standard level against feudal's 10%, and 35% levies against feudal's 25%.
- +2 knights and +15% knight effectiveness.
- −10% men-at-arms upkeep and −20% mercenary hiring cost.
- Twice as many commanders at court.
- No regnal numbers, and realms are named for the title rather than the dynasty.
- No feudal partition and no feudal special contracts.

**Specific gaps.** Nothing sells force. Standing doesn't exist. Feudal's option to create clergy vassals was not carried over.

**The one change that would matter most.** Standing, plus a contract loop: take a contract at the top, deliver it at vassal tier, and standing rises or falls with the result. First check whether vanilla's adventurer contract system can be offered to a landed ruler before building a substitute.

### Corporation

**Intended feel.** A company state run by a board: polished at the top, cut-throat below, with directors scheming for favour and a board playing a slow game of influence.

**What differs from feudal today.**
- Cities, not castles, are the main holding.
- +5% income, +1 diplomacy, −10% building cost, −15% levies.
- Vassals pay more tax but owe fewer troops: 15% tax and 10% levies at standard.
- No regnal numbers, and realms are named for the title.

**Specific gaps.**
- No board influence.
- Single-heir succession for a board-run state.
- **City leak risk.** Vanilla's republic is the only other city-based government, and like these, it sets no condition on who can receive it. If the engine assigns governments to newly landed rulers by their main holding, city baronies anywhere on the map could become Corporation (or Trade Oligarchy). Nobody knows yet. The 50-year test has to count city baronies *outside* the test realms, and a guard is already drafted if they turn up.
- A playable city-based government is untried in vanilla, so it's also unproven whether holding castles alongside cities works smoothly.

**The one change that would matter most.** Board influence that works as a currency, with a deal decision at each tier, followed by a board election as succession.

### Cartel

**Intended feel.** An organized syndicate grown into a state. A council of bosses rules through fear, keeps neighbours on a payment schedule, and the top is always under threat from within. It grows by tribute, not raids.

**What differs from feudal today.**
- It can offer tributary status to independent neighbours, and tributary land counts toward creating titles.
- +2 intrigue, −2 diplomacy.
- +25% dread gained, and +25% dread decay.
- Its own tax curve, rising to 30% at the steepest level.
- The levy obligation is now called the "Turf Levy", so it no longer clashes with real tributaries (fixed in CB-55).

**Specific gaps.**
- **Dread and tribute don't connect.** The tribute offer costs *piety*, not dread. The AI weighs mandala radiance, piety, military threat, tier and faith; nothing reads dread. A Cartel starts with a large penalty and none of the mandala bonuses, so expect few acceptances.
- **Tribute lapses every generation.** The arrangement ends when the overlord dies; the heir must pay piety and ask again at the same poor odds, so the network may never build up. The script confirms the lapse; the in-game test will measure how much it hurts.
- **The +25% dread decay is effectively a penalty.** Vanilla treats *slower* decay as the bonus. Faster decay makes a Cartel ruler's fear fade sooner: weaker, not more Cartel-like.
- Nothing models "the top is always under threat". There's no military identity beyond dread.

**The one change that would matter most.** Couple dread to tribute: a Cartel-only tribute offer that costs or scales with dread instead of piety, plus at least one decision that spends dread (collecting early, making an example of a vassal). Revisit the decay figure at the same time.

### Trade Oligarchy (Gob-Corp)

**Intended feel.** Fifty Trade Princes bound by a shared charter, competing for market share, with no single head. The top rank is First Prince, first among equals. Internal politics are as dangerous as war.

**What differs from feudal today.**
- City-based, like the Corporation.
- +10% income, −1 diplomacy, −10% levies, −10% men-at-arms upkeep.
- Vassals pay 12.5% tax and 15% levies at standard.
- No regnal numbers; own ranks.

**Specific gaps.**
- No market share.
- Single-heir succession for "no single head". Allowing a royal court and always having one First Prince reinforce the single head.
- The same city leak risk as the Corporation.
- The −1 diplomacy works against a bargaining fiction (a tuning note).

**The one change that would matter most.** Market share as the resource, ideally fed by the Frontier trade network, followed by a wealth-weighted vote for succession.

---

## 5. Shared risks: handled and still open

**Handled since the assessment.**
- **The inheritance law trap** (CB-55, done). An heir who moved up a tier could keep the dead ruler's succession law unchecked. A PMC count who inherited a partition realm, for example, would have kept partition for good. A check on title gain now restores the government's own law. CB-55 also renamed the Cartel levy, filled in Unsworn's missing text, added a check that keeps the government lists in step with vanilla, and corrected stale comments.
- **Art.** The four icons are still copies of vanilla icons (mercenary, administrative, clan, republic), so the Cartel reads as Clan in the character window, for instance. Real icons are now being wired in through a new art-conversion tool. That's status, not a design gap.

**Still open.**
- **Unsworn playability (CB-54, ruled).** A player can pick an Unsworn placeholder, a dead end. Your ruling: if a small key-level override works (test T14), block it with a game-over message; if only a full-file override works, leave it playable with a warning toast until Gate 1.
- **In-game proof (CB-49, not yet run).** Every "playable" verdict is a static reading. Nobody has yet picked these rulers, killed them and watched the heir carry on. This is the biggest unknown.
- **The city-barony leak test.** Part of CB-49's 50-year run: count Corporation and Trade Oligarchy rulers outside the test realms.

---

## 6. Decisions only you can make

1. **CB-53: succession versus fiction.** Accept single heir as debt and rename the laws, or have G2 build elective laws (board, vote, takeover, command).
2. **The Cartel's empire rank name.** It currently reads "Cartel", the same word as the government. The candidates are **"Combine"** or **"Hegemony"**. "Syndicate" is out, because the setting's syndicates are canon groups that this government must not be read as.
3. **Influence or a scripted resource.** Vanilla influence could stand in for, say, board influence. But outside the administrative government it gets no top-bar readout, only the character window and ledger, and nobody knows whether spending it works. The default is a scripted resource. If you want influence, it needs a test first (T11).
4. **The order of the G2 design pass.** The recommendation is to **start with the Cartel**. It has the most vanilla machinery to build on, and its fix (coupling dread to tribute) is the clearest.

---

## 7. Suggested roadmap

Each milestone can be approved on its own.

| # | Milestone | What you'd see when it's done | Needs from you |
|---|---|---|---|
| M0 | **Run CB-49** (in-game checks) | Proof that each government is playable, heirs keep it, and it doesn't leak to city baronies | A play session on the British Isles sub-mod |
| M1 | **Rulings** | Succession direction set, Cartel empire name chosen, influence question settled | Decisions 1–3 above |
| M2 | **Cartel G2** | Tribute paid in dread; decisions that spend dread; dread decay retuned; entry and exit decisions; grant and AI settings | Approval of any new events |
| M3 | **PMC G2** | Standing on screen; take-a-contract / deliver loop; adopt-PMC and exit decisions | As M2 |
| M4 | **Corporation G2** | Board influence on screen; deal decisions; entry and exit | As M2 |
| M5 | **Trade Oligarchy G2** | Market share on screen, tied to the Frontier trade network; entry and exit | As M2 |
| M6 | **Depth** | Elective successions (if ruled), third vassal obligations, v1 events lifted only where they move the resource | Approval per event batch |
| M7 | **Breadth** | Government-specific wars and schemes, the PMC-to-Corporation evolution, links to cybernetics and the Frontier | Approval per item |

M2 to M5 each follow the same steps: the resource and its display first, then one top-tier and one vassal-tier decision, then entry and exit, then AI and grants.

---

## 8. Where the evidence is

- **The standard:** `docs/specs/government_template.md`. §1 covers playability, §2 the design questions Q1–Q7, §3 the build surfaces, §6 the gap table, §8 the influence and display answers, and §9 the assessment, with the recommended order in §9.6.
- **The intent:** `docs/specs/governments_v2.md`. §2 covers resources, §5.1–5.4 each government, §6 contract numbers, §14 the G2 outline and §15 what was deferred.
- **The QA reports:** `docs/qa/government_assessment_2026-10-11/`, which contains `pmc.md`, `corporation.md`, `cartel.md`, `gobcorp.md` and `shared_infra.md`.
- **The taskboard:** `circlebackTaskboard.md` entries CB-49 (in-game checks), CB-53 (succession), CB-54 (Unsworn) and CB-55 (fixes done, commit f57e151).
