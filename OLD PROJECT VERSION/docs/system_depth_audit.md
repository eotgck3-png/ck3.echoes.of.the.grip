# System & Government Depth Audit — Echoes of the Grip

Audit: 2026-08-28, `main` @ 08f143e. Companion to `closed_alpha_checklist.md`.
Measures **content depth**, not wiring correctness. Assumes Gate 1/2 blockers get fixed.

---

## Governments at a glance

| Government | Events | Decis | Effects | Trigs | Values | Signature resource | Unique assets |
|---|---:|---:|---:|---:|---:|---|---|
| **Fringe** | 35 | 9 | 10 | 10 | 4 | `fringe_grip`, `fringe_peace_years` | — |
| **Corporation** | 33 | 2 | 8 | 9 | 3 | `board_influence` | interaction, scheme, CB, market cycle |
| **PMC** | 32 | 4 | 6 | 9 | 2 | `pmc_extension_count`, `pmc_contract_client` | council position + 3 tasks |
| **New Cauldron** | 28 | 8 | 6 | 12 | 5 | `nc_senate_support`, `nc_rally_bonus`, `nc_term_count` | — |
| **Cartel** | 27 | 4 | 11 | 11 | 5 | *none* — flags + vanilla dread | — |
| **Gob-Corp** | 27 | **1** | 6 | 7 | 5 | `vote_weight`, `total_votes`, `election_weight` | market cycle (shared) |
| **Elven Monarchy** | **24** | 2 | **6** | 11 | 4 | *none* — isolationism modifier | — |

Event counts include each government's flavor set (~19 each), which inflates them — see *Cross-cutting* below.

---

## Ranked: most lacking first

### 1. Elven Monarchy — thinnest government in the mod
- 24 events, but `eotg_elven_court.0002` and `.0003` are **orphans that can never fire** → 22 live.
- Only 2 decisions (`decree_court_purity`, `cultural_appeal`) and 6 scripted effects — the fewest of both.
- **No tracked resource.** "Isolationism scales with ruler tier" is a yearly modifier refresh, not a mechanic the player pushes against. Nothing to spend, bank, or lose.
- Succession — the Eternal Court ratification that defines the government — is a single event (`elven_court.0001`) plus two effects (`court_confirmed_bonus` / `_penalty`).
- **Its biggest asset is switched off.** `events/eotg_expulsion_events.txt` is 1,212 lines and 6 events of Elven cultural-displacement chain, fully written and internally chained. `eotg_expulsion.0001` is called from nowhere; the file's own header says *"Fires from: Wire eotg_expulsion.0001 to a yearly elven ruler on_action"* and it never was.
- **Cheapest fix in the audit:** one `on_action` hook nearly doubles this government's content.

### 2. Gob-Corp — a voting system with nothing to vote on
- **1 decision** (`gobcorp_no_confidence_vote`), against Fringe's 9 and New Cauldron's 8.
- 6 effects, 7 triggers, and **1 on_action hook** (`yearly_gobcorp_flavor`) — the only government whose sole hook is its flavor pulse. Nothing checks vote weight, Trade Prince standing, or Director-General vulnerability on a timer.
- Three vote variables (`vote_weight`, `total_votes`, `election_weight`) and 5 vote events exist, but no decision lets a Trade Prince *build* weight — the player is a passenger.
- The "50 Trade Princes" identity rests entirely on `eotg_market_faction_cycle`, which is shared with Corporation and Cartel and is not Gob-Corp-specific.

### 3. Cartel — good machinery, no currency
- Genuinely well-built underneath: 11 effects, 11 triggers, a real 4-rank hierarchy (`street_lord` → `underboss` → `boss` → `grand_underlord`), a loyalty-tax cycle, shakedown/hostile-takeover factions, paranoia.
- But **no tracked variable of its own.** Dread is the stated currency of power and it is vanilla dread — the government adds `dread_decay_add = 0.5` and otherwise leans on flags and modifiers. There is no Cartel-specific number the player watches.
- No unique interaction, scheme or CB, despite being the mod's crime-state archetype where all three would be obvious.

### 4. PMC — well-equipped, shallow contract layer
- The only government with council content (1 position, 3 tasks), and 6 on_action hooks — the most of any.
- But the contract system that names the government is **4 events** and **2 script values**, the fewest values in the table. `pmc_extension_count` and `pmc_contract_client` are the whole model.
- 6 scripted effects for a government whose loop is supposed to be negotiate → serve → renew → be discarded.

### 5. New Cauldron — strong, but elections are simulated
- Deep on paper: 8 decisions, 12 triggers, 5 values, 3 tracked variables, 5 on_action hooks.
- The presidency is **flag-driven, not a succession law**. There is no `common/succession_election/`; `eotg_on_death_nc_president` hands the title to a flagged Vice President via an event firing at `days = 1`. It works, but term limits, campaigns and the Senate all sit outside CK3's own election UI, so the player gets no native feedback.
- No unique interaction, scheme or CB for a democracy whose politics is the point.

### 6. Corporation — best-equipped, fewest player levers
- The only government with a character interaction, a scheme (`eotg_sabotage_rival`) and a casus belli (`eotg_boardroom_war`), plus 9 board events and the market faction cycle.
- **Only 2 decisions.** Board Influence is depleted by decisions per the design, and there are two of them.

### 7. Fringe — deepest, and the template everything else was cut from
- 9 decisions including 4 reform paths (feudal / cartel / corporation / PMC), 35 events, a decaying `fringe_grip` with a `fringe_peace_years` collapse timer. The one government whose signature resource is actually driven by its own events.
- Gap: no unique interaction, scheme or CB — its raiding identity leans on vanilla raid mechanics plus one `on_raid_action_start` hook.

---

## Non-government systems

| System | Content | Verdict |
|---|---|---|
| **Cybernetic augmentation** | 31 events (5 files), 4 traits, 3 decisions, 5 hooks, 8 modifiers, full loc | **Complete.** Implementation *exceeds* `docs/eotg_cybernetic_augmentation_system.md` — the doc specifies 15 events, 31 shipped. Needs icons only. |
| **Myr Cluster Wars** | 9 events, 5 phases, 6 catalysts (all 6 wired via `eotg_se_myr_catalyst`), 3 hooks, 1 CB, 1 interaction, 1 ending decision | **Mechanically sound.** Blocked only on `regions = {}` and zero loc — both already in the alpha checklist. Content depth is fine for alpha. |
| **Titan Exodus** | 10 events, 6 modifiers, 1 hook, 1 trigger, 2 variables | **Functional but thin.** No decisions, no traits, no depletion curve — an Exodus "still ongoing" after 735 years fires at the same rate in 866 as in 1200. Refugees carry `refugee_culture`/`refugee_faith` but never form a culture, faith or faction. |
| **Orrin's Grip / The Weight of 866** | 3 events, 1 story cycle | **Thin for what it is.** The mod's founding cataclysm gets a 3-event framing sequence that ends itself after a year and grants 100 prestige. No later callbacks, no anniversary beats, no interaction with the `eotg_grip_survivor` trait. |
| **Void corruption** | 15 events, 2 new traits, 3 decisions, 9 modifiers, 5 opinions, 5 hooks, full loc | **Built out 2026-08-29** (was: empty stub, 0 events, bare `# TODO` hook). Signature resource is `eotg_void_exposure` (0–100), surfaced on the character sheet via three swapped band modifiers. Four stages: Whispers → the Bargain → Void-touched → Hollowed, with `eotg_void_defiant` as the resist path. 28 of 52 options are gated on education, age, trait, faith or wealth; `eotg_se_void_edu_insight` pays out a different permanent modifier per education. Every event moves the signature resource. Needs 2 trait icons only. |
| **Expulsion chain** | 6 events, 1,212 lines — **unreachable** | Largest event file in the mod. Entry point `eotg_expulsion.0001` is called from nowhere. See Elven Monarchy above. |
| **Market faction cycle** | 1 story cycle, `market_share` + `faction_role` | Shared by Corporation / Cartel / Gob-Corp. Works, but doing triple duty as three governments' factional identity. |

---

## Cross-cutting findings

### The flavor layer is decoupled wallpaper
~135 events (41% of the corpus) live in the seven `*_expanded_events.txt` files. They are competently built — real triggers, cooldown flags, `ai_chance` weights, three differentiated options each — but structurally flat:

- **Exactly 3 options, every event.** No 2-option dilemmas, no 4+ branches.
- **Zero chaining.** Not one flavor event triggers a follow-up (`trigger_event` refs to `*_flavor.*`: 0 across all seven sets).
- **They never touch the government's signature resource.** All six tracked variables — `nc_senate_support`, `board_influence`, `fringe_grip`, `vote_weight`, `nc_rally_bonus`, `pmc_extension_count` — have **zero references** in any expanded flavor file. Those resources move only via the small system event sets and the yearly hooks.

Net effect: a player spends most of their event time on vignettes that pay out prestige, dread, skill and opinion while the mechanic that defines their government moves independently. Coupling even a third of the flavor layer to the signature resources would do more for each government's identity than new events would.

### Opinion-modifier namespace leakage
`eotg_fringe_fear_rule_resentment`, `eotg_fringe_public_punishment`, `eotg_fringe_reform_resentment`, `eotg_fringe_spoils_distributed` and `eotg_pmc_loyalty_restored` are used across the New Cauldron, PMC, Cartel, Gob-Corp and Corporation flavor files. Display names are generic ("Ruled by Fear", "Loyalty Restored"), so **nothing is broken or visibly wrong in-game** — but the `eotg_fringe_` prefix on a modifier six governments use is misleading, and suggests the expanded files were cut from a Fringe/PMC template. Worth re-homing to a shared `eotg_shared_*` namespace before more content is written against them.

---

## Recommended order of work

1. **Wire `eotg_expulsion.0001`** — one on_action hook, unlocks 1,212 lines and rescues the weakest government. Highest content-per-effort ratio in the mod.
2. ~~**Give the Void some events**~~ — **DONE 2026-08-29.** Built as a four-stage exposure system rather than a flavor set, so it also answers the "no tracked resource" finding for a mod-exclusive system. Lore basis corrected against `docs/SETTING LORE` mid-build: the Void is **Orrin the Eye's prison**, not a Titan domain, and the live cause is the 850–866 AG **Planar Rift Re-activation** (Grip scars never healed, seals weakening). Malvrick's hunted **Voidwalkers** supply the only real ward, which makes warding a political liability rather than a free cleanse.
3. **Gob-Corp decisions** — 1 is not enough to make voting playable; it needs ways to build and spend vote weight.
4. **Couple flavor events to signature resources** — a pass across the seven expanded files, not new content.
5. **Elven Monarchy resource** — give isolationism a number the player pushes against, and fix the two orphan court events.
6. **Cartel currency** — either a tracked Dread-adjacent variable or an explicit decision that its existing 11 effects feed.
7. **Exodus depletion + Orrin's Grip callbacks** — both are setting-defining and both currently fire once and stop mattering.
