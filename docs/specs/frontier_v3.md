# Spec: Frontier Systems v3 (Phase 3a: Exploration, Mercenaries, Religious organizations; hooks for Corporations and Trade)

**Author:** cloud agent (architect role), 2026-10-06. **Status: built on branch `claude/frontier-v3-cloud`; NOT merged.** The local session verifies (Tiger, PX, eotg-vanilla-scout on §15, lore) and the owner reviews before anything lands.

**Source of intent:** [`docs/design/frontier_systems.md`](../design/frontier_systems.md) §13 (Exploration), §14 (hooks), §15 (future integration), §22 Phase 3. Phases 1 and 2 are [`frontier_v1.md`](frontier_v1.md) and [`frontier_v2.md`](frontier_v2.md); their §R and §V rulings bind. **This phase is additive:** it uses the existing hooks, sponsor effects, data rows and the single yearly roll. Every Phase 1/2 identifier it touches is listed in §3.6 with the reason.

**Round 2 (2026-10-06):** the local verification's fixes and the owner's answers to Q3-1–Q3-5 are in (§16), with expedition targeting prepared for Unclaimed Regions (§4.1, §17). Lines that changed say "round 2".

**Written without game files, Tiger or PX** (`docs/cloud_agent_prompt.md` §1). Engine facts carry a confidence (§1); anything not shown by the mod's own verified script is marked `# UNVERIFIED-VANILLA` in script and listed in §15.

**Size (as built):** 3 new events (.040, .041, .042; the cap was 6), 2 decisions (1 player, 1 debug), 3 county modifiers, 1 new integration hook, about 50 loc keys (51 after round 2). No gfx, no GUI, no story cycles.

---

## 0. Rules (Phase 1/2 rules, plus)
- **Map-agnostic:** no title, province, character, culture, faith, religion or doctrine key in mod script. Faith is read only as `holder.faith`, its head (`religious_head`) and leaders of that faith.
- **LAW AT 866:** a mercenary captain, a head of faith or a holy order that backs or guards a Frontier gains no claim, no say and no law authority. The holder owns the Region. Every option that makes one a backer says so in its tooltip.
- **No named factions, bodies or companies** in text ("a mercenary company", "the head of your faith", "a holy order"). No Void imagery, no "charter", no seasons. Canadian English; gendered pronouns for single scoped characters.
- **Pacing:** the ×0.5 pace, the halved one-off gains and the 3-year cooldown stand. The two new flavour events join `eotg_frontier_flavor_pick_effect`'s pool; there is still **one** yearly roll.

---

## 1. Engine facts

| # | Fact | Source | Conf. |
|---|---|---|---|
| G1 | `faith = { change_fervor = { value = trivial_fervor_gain desc = <loc key> } }` | `common/buildings/eotg_00_temple_buildings.txt:178-190` (vanilla shape, Tiger-clean) | H |
| G2 | `government_has_flag = <flag>` as a character trigger | `common/buildings/eotg_99_background_graphics_buildings.txt:27` | H |
| G3 | The mercenary company government carries the flag `government_is_mercenary` | skill `reference/common/governments/_governments.info:116` | **H** (confirmed, round 2) |
| G4 | The holy order government carries the flag `government_is_holy_order` | by analogy with G3; skill `_governments.info:321` names a `holy_order` government type | **H** (confirmed, round 2) |
| G5 | `random_independent_ruler = { limit = { … } }` | v1 script; with `government_is_mercenary`, vanilla `martial_authority_events.txt:73-85` | **H** (confirmed, round 2) |
| G6 | Mercenary captains and holy order leaders are independent rulers, so G5 finds them | general knowledge; for captains, the precedent in G5. Holy order leaders are now found through the faith instead (G10) | **H** for captains (round 2) |
| G7 | `faith.religious_head` (a character, may not exist) | skill `SKILL.md:59` (`primary_heir.faith.religious_head`) | **H** (confirmed, round 2) |
| G8 | `faith = scope:x.faith` (two characters share a faith) | general knowledge | **H** (confirmed, round 2) |
| G10 | `faith = { random_faith_holy_order = { limit = { leader = { … } } leader = { … } } }` | the local verification (round 2) | H |
| G11 | `pay_short_term_gold = { target = <character> gold = <value> }` | the local verification (round 2) | H |
| G9 | `add_piety`, `minor_piety_value`, `random_list` with `modifier`, `save_scope_value_as` flags, `trigger_event` | Phases 1–2 (verified) | H |

---

## 2. Data model (new state, on the county title unless noted)

| Key | Kind | Meaning |
|---|---|---|
| `eotg_frontier_explored` | variable: `flag:unknown` / `flag:partial`; **absent = Known** | The Region's exploration state (§4). Old saves and maps have none, so every existing Region is Known, which is "Known but Unsettled" as today. |
| `eotg_frontier_expedition_sent` | variable, yes, timed 1 year | One expedition a year per Region (the decision's own gate, not an event cooldown). |
| `eotg_frontier_trade_network_bonus` | variable, a number | **Hook:** a future trade system writes it through `eotg_frontier_set_trade_network_effect`; a Trade Frontier adds it to its yearly input (§7). Never set by Frontier itself. |
| `eotg_frontier_mod_merc_escort` | county modifier, 5 years | A mercenary escort guards the Region: Dangerous adds no strain (§5). |
| `eotg_frontier_backs_for_faith` | **character** variable: a faith | Round 2 (Q3-5): set on a head of faith who backs a Frontier; the faith whose next head inherits the backing. Removed whenever the character starts backing anew (`eotg_frontier_set_sponsor_effect`). |
| `eotg_frontier_backs_for_order` | **character** variable: a holy order | The same for a holy order's leader; the order whose next leader inherits it. |
| `eotg_frontier_pending_faith` / `eotg_frontier_pending_order` | variables | Round 2: the dead faith backer's tie, copied at death, resolved at the Region's next tick (§6.1), then removed with Phase 1's pending variables. |

Saved scopes: `eotg_frontier_exploration` (flag value: what an expedition reached, `flag:partial` or `flag:known`; for the hook and .042's desc), `eotg_frontier_company` (a mercenary captain, .040), `eotg_frontier_faith_backer` (a head of faith or holy order leader, .041), `eotg_frontier_faith_backer_kind` (`flag:head` / `flag:order`); internal: `eotg_frontier_fee` (.040's escort fee, fixed once), `eotg_frontier_believer` (the holder, while finding a faith backer).

---

## 3. New identifiers

### 3.1 Modifiers
| Type | Key | Notes |
|---|---|---|
| static modifier | `eotg_frontier_mod_unknown` | "Unexplored Region": shown while Unknown |
| static modifier | `eotg_frontier_mod_partial` | "Partly Explored Region": shown while Partial |
| static modifier | `eotg_frontier_mod_merc_escort` | "Mercenary Escort", 5 years (§5) |

### 3.2 Scripted effects (county scope unless noted)
| Type | Key | Does |
|---|---|---|
| scripted effect | `eotg_frontier_mark_unknown_effect` | **the cartographer's entry point** for Unknown, parallel to `eotg_frontier_mark_unsettled_effect`: marks the Region Unsettled (if it has no state) and Unknown |
| scripted effect | `eotg_frontier_explore_step_effect` | one step: Unknown → Partial → Known; reveals a trait each step (Phase 2's `eotg_frontier_reveal_trait_effect`); fires `eotg_frontier_on_explored` |
| scripted effect | `eotg_frontier_find_company_effect` | saves `scope:eotg_frontier_company`: a mercenary captain who could back the Frontier |
| scripted effect | `eotg_frontier_find_faith_backer_effect` | saves `scope:eotg_frontier_faith_backer`: the holder's head of faith, else the leader of a holy order of the holder's faith (searched through the faith, G10), who could back it; also `scope:eotg_frontier_backer_faith` or `scope:eotg_frontier_faith_order` |
| scripted effect | `eotg_frontier_set_faith_backer_effect` | round 2: makes `scope:eotg_frontier_faith_backer` the Sponsor and records their tie (`eotg_frontier_backs_for_faith` / `_order`) for Q3-5 |
| scripted effect | `eotg_frontier_resolve_faith_successor_effect` | round 2 (Q3-5): a dead faith backer's backing passes to the faith's head now (`scope:eotg_frontier_successor`) or the order's leader now, if they can back and don't hold the Region; else it lapses |
| scripted effect | `eotg_frontier_clear_exploration_effect` | round 2: removes `eotg_frontier_explored` and both exploration modifiers (at settle) |
| scripted effect | `eotg_frontier_pick_expedition_target_effect` | round 2 (`ACTOR`): **the one expedition target pick** (§4.1); saves `scope:eotg_frontier_county` |
| scripted effect | `eotg_frontier_faith_settle_effect` | a Religious completion: piety for the holder, fervour for the holder's faith |
| scripted effect | `eotg_frontier_offer_backing_effect` | **hook** (`SPONSOR`): any system offers backing; the holder answers in Phase 1's .003 (§7) |
| scripted effect | `eotg_frontier_set_trade_network_effect` | **hook** (`AMOUNT`): a trade system sets the Region's trade input (§7) |

### 3.3 Scripted triggers
| Type | Key | True when |
|---|---|---|
| scripted trigger | `eotg_frontier_is_unknown` | county: `flag:unknown` |
| scripted trigger | `eotg_frontier_is_partial` | county: `flag:partial` |
| scripted trigger | `eotg_frontier_can_explore` | county: Unknown or Partial, no expedition this year, and (round 2) Unsettled, a Frontier or Abandoned (Survey's gate) |
| scripted trigger | `eotg_frontier_can_target_expedition` | round 2, county (`ACTOR`): **the one expedition targeting rule** (§4.1): `eotg_frontier_can_explore`, and held by `$ACTOR$` |
| scripted trigger | `eotg_frontier_holds_explorable` | character: has a Region `eotg_frontier_can_target_expedition` allows |
| scripted trigger | `eotg_frontier_can_back` | character: alive, backs nothing yet, gold for two payments (the backer test for captains and faith leaders, who may hold no county) |
| scripted trigger | `eotg_frontier_is_company_captain` | character: leads a mercenary company (G3) |
| scripted trigger | `eotg_frontier_is_holy_order_leader` | superseded in round 2 and removed: holy order leaders are found through the faith (G10) |

### 3.4 Script values
| Type | Key | Value |
|---|---|---|
| script value | `eotg_frontier_explore_cost_value` | `minor_gold_value` (character scope) |
| script value | `eotg_frontier_escort_cost_value` | `medium_gold_value` (character scope) |
| script value | `eotg_frontier_trade_network_value` | **hook:** `var:eotg_frontier_trade_network_bonus` on a Trade Frontier, else 0 |

### 3.5 Decisions, hooks, events
| Type | Key | Notes |
|---|---|---|
| decision | `eotg_decision_frontier_explore` | Send an Expedition → .042 (§4) |
| decision | `eotg_decision_frontier_debug_mark_unknown` | debug only: marks the capital Region Unknown |
| loc key | `eotg_frontier_toast_faith_backer_succeeded` | round 2: the toast when a faith backer's successor takes up the backing |
| on_action | `eotg_frontier_on_explored` | integration hook: a Region's exploration state advanced |
| event | `eotg_frontier.040` | *Guns for Hire* (§5) |
| event | `eotg_frontier.041` | *A Faithful Offer* (§6) |
| event | `eotg_frontier.042` | *The Expedition Returns* (§4) |

### 3.6 Phase 1/2 identifiers changed (additive; each with its reason)
| Key | Change | Reason |
|---|---|---|
| `eotg_frontier_can_establish` | adds `eotg_frontier_is_unknown = no` | Unknown Regions can't be Established until explored (scope item 1) |
| `eotg_frontier_can_survey` | adds `eotg_frontier_is_unknown = no` | nor Surveyed |
| `eotg_frontier_danger_strains` | adds "no mercenary escort" | the escort counters Dangerous alongside the Garrison Post (item 2) |
| `eotg_frontier_clear_infra_effect` | also removes the escort | an escort ends with the project (settle or abandon) |
| `eotg_frontier_flavor_pick_effect` | two pool entries (.040, .041) and their searches | the single yearly roll (owner rule) |
| `eotg_frontier_yearly_gain_value` | adds `eotg_frontier_trade_network_value` (0 by default) | the trade hook (item 4) |
| `eotg_frontier_complete_effect` | the Religious row also runs `eotg_frontier_faith_settle_effect` | item 3: completion ties into the faith |
| `eotg_frontier_settle_effect` | round 2: also runs `eotg_frontier_clear_exploration_effect` | a settled Region carries no exploration state (S2) |
| `eotg_frontier_set_sponsor_effect` | round 2: removes the new sponsor's `eotg_frontier_backs_for_faith` / `_order` | a fresh backing starts with no faith tie; `eotg_frontier_set_faith_backer_effect` sets it after |
| `eotg_frontier_on_sponsor_death_effect` | round 2: a faith backer's tie goes to `eotg_frontier_pending_faith` / `_order` instead of `eotg_frontier_pending_heir` | Q3-5 |
| `eotg_frontier_resolve_pending_heir_effect` | round 2: first branch calls `eotg_frontier_resolve_faith_successor_effect` | Q3-5 |
| `eotg_frontier_clear_pending_heir_effect` | round 2: also removes the two new pending variables | Q3-5 |
| `eotg_frontier_event_roll_effect` | round 2: an AI holder accepts a company or faith backer in script (§11) | Q3-4 |
| `eotg_frontier_flavor_pick_effect` | round 2: .040's entry only where (a) or (b) can apply | no prompt with only the "nothing" option |
| `eotg_decision_frontier_explore` | round 2: its effect calls `eotg_frontier_pick_expedition_target_effect` | §4.1 |

Nothing else in Phases 1–2 changes. No Phase 1/2 event or loc key is edited.

---

## 4. Exploration (design §13; Phase 2 deferral D2-2)

**States:** Unknown → Partially explored → Known. Stored in `eotg_frontier_explored`; **absent = Known**. A state only: no fog of war, no map hiding, no GUI.

**What Unknown blocks:** Establish and Survey (`eotg_frontier_can_establish`, `eotg_frontier_can_survey`). Partial allows both; exploring further still pays (a trait each step, the charts filed as a survey at Known).

**Where exploring applies (round 2):** only in a Region that is Unsettled, a Frontier or Abandoned, the same gate as Survey. **Settling clears exploration** (`eotg_frontier_clear_exploration_effect` in `eotg_frontier_settle_effect`): a settled Region has no exploration variable and no Unknown or Partial modifier, so Send an Expedition is hidden for it.

**Marking:** `eotg_frontier_mark_unknown_effect` is the one entry point, for the cartographer after Gate 1 and for test sub-mods. **An Unknown Region is also Unsettled**: the effect calls `eotg_frontier_mark_unsettled_effect` first (owner question Q3-1). It does nothing to a Region that is already a Frontier, Abandoned or settled-with-history (it only acts when the Region has no Frontier state, or is Unsettled).

**The action: a new decision, "Send an Expedition" (`eotg_decision_frontier_explore`), not a Survey extension. Why:**
- Survey's gates don't fit: it needs trait room and runs once in 5 years; exploring an Unknown Region needs neither.
- Exploration is the hook a future Exploration system replaces or extends; one decision and one effect (`eotg_frontier_explore_step_effect`) give it a clean seam.
- Survey stays exactly as Phase 2 built it.

**The decision:** shown to a holder of an Unknown or Partial Region (`eotg_frontier_holds_explorable`). Cost: `eotg_frontier_explore_cost_value` (minor gold). One expedition a year per Region. It picks the target through `eotg_frontier_pick_expedition_target_effect` (Unknown first, else Partial; then the most developed), marks the year, and fires .042.

**.042 *The Expedition Returns*** (player-initiated, so not part of the prompt budget). `immediate` runs one step:
- Unknown → **Partial**: a trait is revealed.
- Partial → **Known**: a trait is revealed (if there is room), and the variable is removed.
- Fires `eotg_frontier_on_explored` (`scope:eotg_frontier_exploration` = `flag:partial` / `flag:known`).

Options:
- **(a, ungated) "File the charts."** At Known: Phase 2's `eotg_frontier_file_survey_effect` (round 2): +2 progress on a running Frontier, survey data (the +5 head start) otherwise. **Never survey data on an active Frontier.** At Partial: nothing more (`eotg_frontier.042.a_partial_tt`).
- **(b) "Send them straight back out."** Still Partial, gold for another expedition: pays, takes the second step now (→ Known), and runs `eotg_frontier_file_survey_effect` as (a) does.

**AI:** potential holds an explorable Region and gold ≥ 3 × the cost; will do base 10. AI holders explore their own Unknown Regions, then can Establish there as usual.

### 4.1 Expedition targeting (round 2; prepared for Unclaimed Regions)
**Every** expedition target goes through two identifiers, and nothing else decides it:
- `eotg_frontier_can_target_expedition = { ACTOR = <character> }` (county scope): may `ACTOR` send an expedition here? `eotg_frontier_holds_explorable` and the pick both use it.
- `eotg_frontier_pick_expedition_target_effect = { ACTOR = <character> }`: chooses the Region and saves `scope:eotg_frontier_county`. The decision calls it.

**Today:** `eotg_frontier_can_explore = yes` and `holder = $ACTOR$`, and the pick iterates `$ACTOR$`'s held county titles. This is the Phase 3a behaviour unchanged.

**How the Unclaimed Regions build widens it** (`frontier_unclaimed_regions.md` §8.2; that spec deferred it as UD2, and the owner asked for it in its Batch 2. **Built** on `claude/frontier-unclaimed-cloud`, unmerged; steps 1–3 as written, `eotg_frontier_holds_explorable` also reads the Unclaimed list, and the decision is never shown to a placeholder):
1. The trigger becomes `eotg_frontier_can_explore = yes` AND (`holder = $ACTOR$` OR (`eotg_unclaimed_is_unclaimed = yes` AND `eotg_unclaimed_in_reach = { ACTOR = $ACTOR$ }`)): the actor's own Regions, plus unclaimed Regions **within reach**, adjacency to the actor's sub-realm or distance from the actor's capital, exactly as that spec's §8.2 defines reach.
2. The pick adds a second pass over unclaimed counties in reach (the reach test's own iterator), after the actor's own Regions, with the same Unknown-first order.
3. .042 is fired to the actor, not the county holder; its options already act on `scope:eotg_frontier_county` and pay from root. Nothing else in §4 changes.
4. Exploring an unclaimed Region gives no claim and no say over it (LAW AT 866); claiming stays the Unclaimed interaction's job.

---

## 5. Mercenary organizations (design §15)

**Entry chosen: one new pool event, .040 *Guns for Hire* (retitled in round 2), offering both the escort and the backing.** Why not the others:
- **The .001 founder pick:** a Founder must be the holder, in the holder's realm, or the holder's liege (Phase 1 Q3 ruling). A captain is none of these, so every tick would add No Founder strain. Making a captain a valid founder means changing the founder rule, which Phase 3a doesn't do (owner question Q3-2).
- **The Sponsor-offer flow (.003):** its accept option requires `eotg_frontier_can_sponsor` (a landed count or above), which a captain isn't. .040 instead checks the new, narrower `eotg_frontier_can_back` and calls the same `eotg_frontier_set_sponsor_effect`, so payments, lapse, withdrawal and the hooks all work unchanged.

**.040 *Guns for Hire*:** pool weight 10, only for a **Military** project with no backer, or a **Dangerous** Region of any other project with no escort (round 2), and only when `eotg_frontier_find_company_effect` found a captain (`eotg_frontier_is_company_captain` + `eotg_frontier_can_back`, and not at war with the holder, round 2). Options:
- **(a) (Dangerous, not Military; round 2) "Hire them to guard the convoys."** `eotg_frontier_escort_cost_value` (medium gold, owner Q3-3), paid to the captain with `pay_short_term_gold` (G11): `eotg_frontier_mod_merc_escort` for 5 years, strain −1. While it lasts, Dangerous adds no strain. Not if one is already there. A Military project already ignores Danger, so the escort is never offered there and its tooltip is true on every path.
- **(b) (Military only, no backer yet) "Let the company back the venture."** The captain becomes the Sponsor (they pay the yearly payment from their own gold), progress +3. Tooltip: no claim, no say.
- **(c, ungated) "We will hold it ourselves."** Nothing.

**Death or lapse:** the captain is an ordinary Sponsor. On their death Phase 1's hand-off looks at their primary heir, who will usually not be landed, so the backing lapses as for anyone else. **If the company disbands** while the captain lives, the captain stays the Sponsor and keeps paying from their own gold until they can't (Sponsor Lapse); in-game check in the test plan §2.

**Founder:** no mercenary Founders for now (owner Q3-2); revisit after in-game testing of Phases 1–3.

---

## 6. Religious organizations (design §15), faith-neutral

**Who:** the holder's **head of faith** (`holder.faith.religious_head`, if it exists and is not the holder), else the **leader of a holy order of the holder's faith**, found through the faith (round 2, G10: `faith = { random_faith_holy_order = { limit = { leader = { eotg_frontier_can_back = yes } } … } }`). Found by `eotg_frontier_find_faith_backer_effect`; both must pass `eotg_frontier_can_back`. No faith, religion or doctrine key is ever named.

**.041 *A Faithful Offer*:** pool weight 10, only for a **Religious** project with a faith backer found. The desc varies by `eotg_frontier_faith_backer_kind` (head or order). Options:
- **(a) (no backer yet) "Accept the backing."** The faith backer becomes the Sponsor through `eotg_frontier_set_faith_backer_effect` (round 2), progress +3. Tooltip: no claim, no say, no authority over the Region.
- **(b) "Ask only for a blessing."** The holder gains minor piety; progress +2.
- **(c, ungated) "The mission stands on its own."** Nothing.

### 6.1 When a faith backer dies (owner Q3-5, round 2)
The backing passes to the faith's **next head**, or the order's **next leader**, never to the dead backer's personal heir:
1. `eotg_frontier_set_faith_backer_effect` records the tie on the backer: `eotg_frontier_backs_for_faith` (a head) or `eotg_frontier_backs_for_order` (an order leader).
2. At death, `eotg_frontier_on_sponsor_death_effect` copies it to the Region (`eotg_frontier_pending_faith` / `_order`) in place of `eotg_frontier_pending_heir`.
3. At the next tick, `eotg_frontier_resolve_faith_successor_effect` reads the faith's `religious_head` (or the order's `leader`) **now**. If they pass `eotg_frontier_can_back` and don't hold the Region, they become the Sponsor, the tie moves to them, and the holder gets `eotg_frontier_toast_faith_backer_succeeded`. Otherwise the backing lapses (Sponsor Lapse strain and Phase 1's lapse toast).
4. The successor gains no claim, no say and no authority (LAW AT 866).

**Completion ties to the faith** (`eotg_frontier_faith_settle_effect`, in the Religious row of `eotg_frontier_complete_effect`): the holder gains minor piety, and the holder's faith gains `trivial_fervor_gain` fervour (G1), with the desc key `eotg_frontier_fervor_mission_settled`.

---

## 7. Corporations and trade networks: hooks only (how a future system plugs in)

No corporation or trade system exists; these are **empty, documented entry points**. Frontier never names the future system.

**A corporation as a Sponsor:**
1. Its representative is a character. Call, on the Frontier's county: `eotg_frontier_offer_backing_effect = { SPONSOR = <that character> }`. That saves the scopes and sends Phase 1's .003 *An Offer of Backing* to the holder, who accepts or refuses as for any backer.
2. .003 accepts only an `eotg_frontier_can_sponsor` backer (landed count or above). A corporation led by an unlanded character either becomes landed, or calls `eotg_frontier_set_sponsor_effect = { SPONSOR = <character> }` directly after its own consent flow. Both effects fire `eotg_frontier_on_sponsor_changed`.
3. Payments, lapse, withdrawal and the death hand-off then work as for any backer. The corporation gains no claim and no say (LAW AT 866).

**A trade network feeding Trade Frontiers:**
1. Call `eotg_frontier_set_trade_network_effect = { AMOUNT = n }` on the county (n ≥ 0, pre-pace like every input; +2 means +1 progress a year).
2. `eotg_frontier_trade_network_value` adds it to the yearly gain of a **Trade** Frontier only; it is 0 everywhere else and whenever the variable is absent. Set `AMOUNT = 0` to switch it off.
3. Listen to `eotg_frontier_on_project_progressed` / `_completed` to react.

**Exploration** (built here, §4) is the third: call `eotg_frontier_mark_unknown_effect`, `eotg_frontier_explore_step_effect` or Phase 2's `eotg_frontier_reveal_trait_effect`, and listen to `eotg_frontier_on_explored` / `eotg_frontier_on_discovery`.

---

## 8. Hooks (design §14)
| Hook | Fired from | Extra scopes |
|---|---|---|
| `eotg_frontier_on_explored` | `eotg_frontier_explore_step_effect` | `scope:eotg_frontier_exploration` (`flag:partial` / `flag:known`) |

Defined empty in `eotg_frontier_on_actions.txt`, extended additively, fired through Phase 1's `eotg_frontier_fire_hook_effect`.

---

## 9. Events (all three; owner review list)

| ID | Title | Fired by | Options (the always-available one in **bold**) | Couples |
|---|---|---|---|---|
| `eotg_frontier.040` | *Guns for Hire* | the yearly roll's pool: Military project with no backer, or Dangerous Region of another project with no escort; a captain found | (a) Dangerous, not Military: hire an escort (medium gold to the captain; 5 years; strain −1); (b) Military, no backer: the company backs it (progress +3); **(c) hold it ourselves** | strain / progress |
| `eotg_frontier.041` | *A Faithful Offer* | the pool: Religious project, a faith backer found | (a) no backer: accept the backing (progress +3); (b) a blessing (minor piety, progress +2); **(c) the mission stands on its own** | progress |
| `eotg_frontier.042` | *The Expedition Returns* | decision Send an Expedition | **(a) file the charts** (at Known: +2 progress on a Frontier, else survey data); (b) send them straight back out (gold; → Known; filed the same way) | the head start (progress) |

**Prompts per typical project:** unchanged at **about 5** (Phase 2 §9.1). .040 and .041 only widen the pool; the 50% chance and the 3-year cooldown decide how many flavour events come. .042 is player-initiated, like Survey and Build. A player who explores an Unknown Region sees one or two .042 reports before the project starts, by choice.

---

## 10. Loc surface
`localization/english/eotg_frontier_l_english.yml`, Canadian English. New: **42 keys** (316 → 358): exploration 22 (2 modifiers, 2 decisions, .042), mercenaries 10 (1 modifier, .040), religious organizations 10 (.041, 1 fervour desc). The hooks add none.

## 11. AI
| Decision | Interval | ai_potential | ai_will_do |
|---|---|---|---|
| Send an Expedition | county 60, duchy+ 48 (barony 0) | holds an explorable Region; gold ≥ 3 × the cost | base 10; +10 learning ≥ 12 |

AI holders still get no flavour events, so .040 and .041 are player-only. **AI holders accept mercenary and faith backers in script, with no event** (owner Q3-4, round 2), in `eotg_frontier_event_roll_effect`, like Phase 1's AI-to-AI offers: an AI holder of a Military or Religious Frontier with no backer and no flavour cooldown has a 20% chance a year to take a company (Military) or a faith backer (Religious) as Sponsor, progress +3, and the 3-year cooldown.

## 12. Definition of done
1. eotg_lint 0 in Frontier files; check_all passes; spec_conformance shows **0 missing ids for frontier_v3**.
2. Every new event is fired, has an always-available option that guards its own effects, and moves progress or strain.
3. Through `frontier_v3_test_plan.md`, on the test map and on the vanilla sub-mod: Unknown blocks Establish and Survey; an expedition moves Unknown → Partial → Known with a trait each step and fires the hook; .040's escort stops Danger strain and its backing makes a captain the Sponsor; .041 makes a head of faith or holy order leader the Sponsor or blesses the project; a Religious completion adds piety and fervour; the trade hook adds to a Trade Frontier only.
4. Old saves and maps: a Region with no `eotg_frontier_explored` behaves exactly as in Phase 2.

## 13. Deferrals
- **D3-1:** a captain as **Founder** (needs the founder rule widened). Deferred by the owner (Q3-2) until Phases 1–3 are tested in game.
- **D3-2:** AI-to-AI mercenary and faith backing: built in round 2 (§11), no longer deferred.
- **D3-5:** exploring Regions the actor doesn't hold (Unclaimed Regions UD2): prepared in §4.1, not built.
- **D3-3:** Unknown hiding anything on the map (fog of war, names): GUI and map work.
- **D3-4:** Corporations and trade networks themselves (Phase 3b or later); only their hooks exist.

## 14. Art wanted (none built; vanilla icons and the decision picture `decision_realm.dds` are used)
- A decision picture for **Send an Expedition** (a survey ship leaving a station).
- County-modifier icons for **Unexplored Region**, **Partly Explored Region** and **Mercenary Escort** (now `county_modifier_development_negative` / `_control_positive`).
- An event background for the expedition's return (now `theme = realm`).

## 15. Verification list for the local session (eotg-vanilla-scout, vanilla 1.20.0.3)
**Round 2:** items 1–5 and 8 are confirmed by the local session. Item 2's trigger was then removed (holy order leaders are found through the faith, G10). Item 8's fallback is not needed: .040 (a) pays with `pay_short_term_gold` (G11). Items 6, 7 and 9 stay open (in game).

1. **(G3)** The mercenary company government's flag is `government_is_mercenary`, readable with `government_has_flag` (`eotg_frontier_is_company_captain`).
2. **(G4)** The holy order government's flag name (`government_is_holy_order`?) (`eotg_frontier_is_holy_order_leader`, superseded in round 2).
3. **(G6)** `random_independent_ruler` reaches mercenary captains and holy order leaders (`eotg_frontier_find_company_effect`, `eotg_frontier_find_faith_backer_effect`). If not, which iterator does (`random_ruler`, `random_living_character`)?
4. **(G7)** `faith.religious_head` from a character's faith, and `exists =` on it (`eotg_frontier_find_faith_backer_effect`).
5. **(G8)** `faith = scope:x.faith` comparing two characters' faiths.
6. A mercenary captain or holy order leader as `var:eotg_frontier_sponsor`: does `remove_short_term_gold` take their gold each year (`eotg_frontier_sponsor_pay_effect`)? Do they lose it when the company is disbanded? (In game.)
7. TEST-IN-GAME: `eotg_frontier_explored` on a county title survives save/reload and a holder change (as V1 did).
8. A saved scope value as a gold amount: `remove_short_term_gold = scope:eotg_frontier_fee` / `add_gold = scope:eotg_frontier_fee` in .040 (a). Fallback: `remove_short_term_gold = eotg_frontier_escort_cost_value` and no payment to the captain.
9. Round 2: a **character** variable holding a faith (`eotg_frontier_backs_for_faith`) or a holy order (`eotg_frontier_backs_for_order`), copied to a county variable at death and read back as a scope (`var:eotg_frontier_pending_faith = { religious_head ?= { … } }`, `var:eotg_frontier_pending_order = { leader ?= { … } }`). Marked `UNVERIFIED-VANILLA` in `eotg_frontier_set_faith_backer_effect`. Also: what the order variable holds if the order is disbanded before the next tick (the `?=` guards should make it lapse).

## 16. Owner decisions (2026-10-06, round 2)
- **Q3-1. Yes:** Unknown implies Unsettled (as built).
- **Q3-2. No** mercenary Founders for now; revisit after in-game testing of Phases 1–3 (D3-1).
- **Q3-3. Keep** the escort at medium gold for 5 years.
- **Q3-4. Yes:** AI holders accept mercenary and faith backers, resolved in script with no events, like the AI–AI sponsor offers (§11; built in round 2).
- **Q3-5.** When a head of faith (or an order's leader) backing a Frontier dies, the backing passes to the **next** head of faith (or the order's next leader) if they can back; otherwise it lapses (Sponsor Lapse). Never to their personal heir (§6.1; built in round 2).
- **For the cartographer:** never mark long-settled cores Unknown. Unknown is for fringe and border Regions.

## 17. Unclaimed Regions impact (round 2; `frontier_unclaimed_regions.md`, approved, not built)
Every place in Phase 3a that assumes the county's holder is a real, playable ruler. When counties can be held by an Unclaimed placeholder, each needs a look. Phase 3a itself adds no government, placeholder or claiming logic.

**Adapted by the Unclaimed Regions build** (`claude/frontier-unclaimed-cloud`, unmerged):
- expedition targeting: widened (§4.1);
- `eotg_decision_frontier_explore`: `is_shown` excludes placeholders (`eotg_is_unclaimed_holder = no`);
- `eotg_frontier_event_roll_effect`, AI block: the holder must not be a placeholder;
- `eotg_frontier_offer_backing_effect`: never for a placeholder-held county;
- `eotg_frontier_can_establish`: never while Unclaimed;
- the yearly Frontier tick and the sponsor-death on_action: skip Unsworn characters.

The other rows need no change, for the reasons the table gives.

| Where | Assumes | What Unclaimed needs |
|---|---|---|
| `eotg_frontier_can_target_expedition`, `eotg_frontier_pick_expedition_target_effect`, `eotg_frontier_holds_explorable`, `eotg_decision_frontier_explore` | the explorer holds the Region | widen per §4.1 (Regions within reach); until then a placeholder could see the decision, so its `is_shown` should exclude placeholders (`eotg_is_unclaimed_holder`, not built yet) when that trigger exists |
| `eotg_frontier.042` | fired to the holder, who pays | fire to the actor (§4.1 step 3) |
| `eotg_frontier.040`, `.041` (`eotg_frontier_flavor_pick_effect`) | `holder = { trigger_event }`: the holder decides and pays | none while unclaimed counties can't be Frontiers (Unclaimed §6: establishing needs a claim first); add a placeholder guard if that ever changes |
| `eotg_frontier_find_company_effect` | `is_at_war_with` the holder | a placeholder is never at war (war immunity, Unclaimed §4.3), so the test holds |
| `eotg_frontier_find_faith_backer_effect` | `holder.faith`: the holder's faith is the one that backs | a placeholder copies the county's faith (UL1), so it would find a backer; guard if an unclaimed Frontier is ever allowed |
| `eotg_frontier_event_roll_effect`, AI block | `holder = { is_ai = yes }` means an AI ruler choosing a backer | exclude placeholders, which are AI, so they never take backers |
| `eotg_frontier_resolve_faith_successor_effect`, `eotg_frontier_resolve_pending_heir_effect` | the successor or heir is compared with the holder, and the toast goes to the holder | if a Frontier is released to Unclaimed (Unclaimed §6.1, abandonment) these don't run (no Frontier); no change expected |
| `eotg_frontier_offer_backing_effect` | `holder = { trigger_event = eotg_frontier.003 }` and `NOT = { holder = $SPONSOR$ }` | callers own their pacing; a caller must not offer backing for an unclaimed county |
| `eotg_frontier_mark_unknown_effect` | Unknown implies Unsettled (Q3-1) for a held county | Unclaimed §8.2 makes Unknown Regions claimable; marking still works, since the variable lives on the title, not the holder |
| `eotg_frontier_can_establish`, `eotg_frontier_can_survey` | the holder acts | Survey stays holder-only (Unclaimed UD2); Establish already needs a claim |
| `eotg_frontier_faith_settle_effect` | the holder's piety and faith | runs only at completion, by a real holder |

---

### HANDOFF
See `docs/handoffs/cloud_2026-10-06_frontier-v3.md`.
