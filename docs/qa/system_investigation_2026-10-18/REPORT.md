# System investigation, 2026-10-18

Six read-only reviews of the mod's systems against each other and against vanilla CK3 **1.20.1.1**. Scope:
- cybernetics core;
- cybernetics' social and realm layer;
- Frontier Systems with Unclaimed Regions;
- the seams between systems;
- a shape comparison with vanilla;
- a survey of vanilla systems the mod could plug into.

The governments were assessed separately on 2026-10-11 (`docs/qa/government_assessment_2026-10-11/`). Items already on `circlebackTaskboard.md` are left out.

**Bottom line:** no crash paths, no invariant breaks, and on_action layering, shared identifiers and pulse performance are clean. There are about 40 behaviour gaps:
- 1 HIGH: the Ban has two routes that skip it.
- 9 MED.
- the rest LOW.

Most are missing guards: a state that changes during a delay, or an edge case such as an imprisoned ruler, a vassal-held county, or a child heir. A smaller group needs a design ruling. The integration survey found two cheap, low-risk wins that need no art: decision alerts and encyclopedia entries.

Confidence labels: **C** = confirmed by reading the code (the orchestrator re-checked S3 and C1 itself), **L** = likely, **G** = needs an in-game check.

Owner codes in the Owner column:
- **scr** = eotg-scripter
- **loc** = eotg-localizer
- **arch** = eotg-architect
- **human** = the owner

---

## 1. Fix now: mechanical, no design needed

These follow a vanilla precedent or an existing house rule.

| ID | Sev | Conf | Finding | Where | Fix | Owner |
|---|---|---|---|---|---|---|
| C1 | MED | C | Imprisoned and incapable rulers still get the full cybernetics pools and story beats, e.g. Court Massacre against their own court from an enemy dungeon. Vanilla filters both (`00_available_for_events_triggers.txt:802-810`). | `common/on_action/eotg_augmentation_on_actions.txt:182-184, 896-898, 1201-1203, 1898-1903`; story ticks in `eotg_augmentation_stories.txt` | Gate the **event branches**, not the risk/drift accrual (hardware wears either way), on `is_imprisoned = no` and `is_incapable = no`. Gate the Countdown and Heir's Arc effect_groups too. | scr |
| C2 | MED | C | About 25 tier events fire 1–30 days after the roll and don't re-check the tier. A cascade, removal or downgrade during the delay shows an Overclocked event to a Neurofractured, Enhanced or unaugmented character. The Countdown's tier3.020 can land after the pulse's cascade. | tier1 .003/.004/.006/.009/.010/.012; tier2 .002/.004/.005/.007/.011/.012/.015; tier3 .005/.006/.007/.009/.012/.014/.017/.019/.020/.023 | Add `eotg_is_aug_tierN = yes` to each trigger. This is a world-state guard, as the B13 Neurofractured guards were, not a cooldown. | scr |
| S3 | MED | C | The AI flips License ↔ Favor every 10 years and pays prestige each time. Each law scores 0 while held, so the alternative always wins (for an augmented, non-zealous, diligent/just and ambitious/cynical ruler). | `common/laws/eotg_augmentation_laws.txt:131, 248` | Score absolutely, without self-exclusion (vanilla `00_realm_laws.txt:2576-2645`). | scr |
| X1 | MED | L | The non-ruler pulse fires liege events (nr.001–.005, including nr.004's murder) on an **Unsworn** employer. | `eotg_augmentation_on_actions.txt:1516-1532` | Add `employer = { eotg_is_unclaimed_holder = no }`. | scr |
| X3 | MED | G | Government succession setup runs on `on_game_start`, before the lobby, so a ruler-designer character may start without its law. Cybernetics moved to `on_game_start_after_lobby` for this reason (`:153-160`). | `common/on_action/eotg_government_on_actions.txt:10-14` | Also register it after the lobby (it's safe to run twice). Add a designer check to CB-49. | scr, human |
| F1 | MED | L | War strain misses a **vassal's** Frontier when the liege is at war and enemy armies stand in the Region. It only starts once the county is occupied, which falls short of spec A4.1. | `common/scripted_triggers/eotg_frontier_triggers.txt:314-327` | Test the war state and army owner against `top_liege` as well as the holder (vanilla `governance_on_actions.txt:1038-1039`). | scr |
| F3 | MED | C (G for engine) | A Local Ruler ignores the faith's clergy gender and the realm's gender law. Templates are a flat 50% female. | `common/scripted_character_templates/eotg_frontier_templates.txt:16,63`; `eotg_frontier_triggers.txt:98-127`; `eotg_frontier_effects.txt:1473-1530` | Use `root_faith_clergy_gender_female_chance` (vanilla `00_court_character_templates.txt:31`) and the vanilla grant triggers (`00_scripted_triggers.txt:342-383`) in `founder_can_rule`. | scr |
| S5 | MED | L | The Kingpin story passes to a **child** heir, though starting it needs an adult. | `common/story_cycles/eotg_aug_kingpin_story.txt:160-187` | Add `is_adult` to the handover; end the story otherwise. | scr |
| F4/F5 | LOW | C | .001's options, and .004/.005, don't re-check `holder ?= root`. A county lost while the window is open still costs the old holder or completes for them. | `events/eotg_frontier_events.txt:78-269, 834, 1070` | House rule: `holder ?= root` in the options or trigger. | scr |
| F7 | LOW | C | `.003`'s Seamless guard also blocks **AI** holders and still uses up the Sponsor decision's cooldown. | `eotg_frontier_events.txt:634`; `eotg_frontier_decisions.txt:348` | Apply the guard to players only. Rule 7 is about text a player sees. | scr |
| X5 | LOW | C | A PMC is never picked as the Frontier "mercenary backer" (it needs `government_is_mercenary`). | `eotg_frontier_triggers.txt:432-434` | Also accept the PMC government flag. | scr |
| C5 | LOW | C | While the back-alley retry flag is held, the whole initiation list is skipped. In years when the 50% retry roll fails, nothing fires. | `eotg_augmentation_on_actions.txt:188-200` | Make the retry an `if`, not the head of an `else_if` chain. | scr |
| C11 | LOW | C | Excision's `is_valid` demands the full clinic price though option e costs 0.4x, and "Not today" uses up the 5-year cooldown. | `common/decisions/…:855-857`; `events/eotg_augmentation_endgame.txt:148-165` | Check the cheapest cost; refund or skip the cooldown on b. | scr |
| S10 | LOW | C | int.001 doesn't re-check that the saved surgeon is alive or employed after its 3–10-day delay, and gives no fail toast. | `events/eotg_augmentation_interactions.txt:83-88` | Re-check, plus `on_trigger_fail`. | scr |
| S12 | LOW | C | Two Admiration opinions never expire: a non-decaying modifier with no duration. | `events/eotg_augmentation_activities.txt:176, 498` | Add `years =`. | scr |
| S6 | LOW | C | Tamper: no toast when the target is imprisoned (vanilla abduct `:278-316`); a target who reaches Seamless gets the "removed" text; no `is_hostage = no`. | `common/schemes/scheme_types/eotg_augmentation_schemes.txt:100-112, 307-357` | Follow abduct's invalidation branches. | scr, loc |
| S11 | LOW | C | Examine has no `notification_text`, so an AI-sent Examine shows the generic text. | `common/character_interactions/eotg_augmentation_interactions.txt:897-901` | Add one. | loc |
| V1 | LOW | C | The stale "UNVERIFIED-VANILLA: interaction_category_diplomacy" comment. It is vanilla (`00_adoption.txt:5`). | `common/character_interactions/eotg_unclaimed_interactions.txt:29` | Delete the comment. | scr |

## 2. Needs a ruling first

The architect proposes a rule, and the owner approves the ones marked **human**.

| ID | Sev | Finding | Where | Options |
|---|---|---|---|---|
| **S1** | **HIGH** | **The Ban doesn't stop retainer or knight installs.** The augment-retainer decision (init.020) and the yearly knight volunteer (nr.001) call `eotg_aug_initiate_effect` directly: no provider, roll, discovery or contraband. This is the main AI uptake path, so the Ban barely reduces augmentation. | `eotg_augmentation_effects.txt:731-735`; init.020; nr.001; decisions `:519-583` | Route these through the procedure roll with a provider, or at least run the contraband check under a Ban. Lower their weights under a Ban. (arch) |
| S2 | MED | **The physician operates at a distance.** The physician send option and Examine work on a spouse abroad or a relative at another court. Vanilla's only physician-operates interaction needs the recipient to be a courtier or guest and `is_available` (`06_ep3_interactions.txt:4461-4476`). This also breaks lore I6, "physical and local". | interactions `:67-74, 142-156, 476-483, 557-571, 912-924` | Require presence and `is_available` for the physician and Examine; clinics and back streets stay remote. (arch) |
| S4 | MED | **A liege prosecutes their own gift.** A discovered Offer under a Ban gives the actor-liege a crime reason against the patient they chose to augment. | effects `:2627, 2652 → 2336 → 2976-2995` | Skip the liege's reason when the liege is the actor. (arch) |
| F2 | MED | **Sponsorship survives war, loss and prison.** A sponsor keeps paying a conqueror and gets the completion reward. .010 offers enemy Frontiers too. | `eotg_frontier_triggers.txt:130-133`; events `:1499-1529`; decisions `:426-436` | Lapse it on holder change, or on war with the holder, imprisonment or landlessness; filter .010. (arch) |
| X2 | MED | **Kingpin under a Cartel.** No government gate, so the crime boss gets "a criminal boss moves in". The kingpin's dread beats get the Cartel's +25% gain, and once Cartel G2 C2 lands they would feed tribute retention without anyone designing that. | `common/scripted_triggers/eotg_aug_kingpin_triggers.txt:19-35` | Gate, tilt or accept, **before Cartel C2**. Add to CB-57. (arch, human) |
| C3 | LOW-MED | **The Intervention is a repeatable risk drain.** Only a refusal blocks it, so an accepted one returns every pulse, and the Countdown can fire it twice a year. | on_actions `:1143-1155`; stories `:462` | Add a cooldown flag on acceptance. (arch) |
| C4 | LOW-MED | **The inherit-tree lock never expires.** The guards read `eotg_inh_heir`; the spec's 6-year safety flag is written but never read. No live leak today, but any missed close bars the ruler from both arcs for life. | effects `:3187`; on_actions `:985, 1235, 1943` | Read the 6-year flag as expiry. (arch) |
| C6 | LOW | **A deposed Neurofractured ex-ruler drifts to 100** with no terminal event. Abdication sets the restraint modifier but not the flag. | effects `:1273-1288`; on_actions `:1641` | Set the flag, or give the drift an end state. (arch) |
| C7 | LOW | **The Heir's Arc closes for good** after any landless tick, which can happen under 1.20 admin rotation or a short adventurer stint. | Heir's Arc first branch | Pause it instead of closing. (arch, G) |
| C8/C9 | LOW | **Child rulers progress through tier 3 and the Countdown.** Knights skip the "settling" floor and can go from tier 1 to tier 3 in two pulses. | `eotg_can_progress_to_*`; on_actions `:1527, 1580-1595` | Add `is_adult` for rulers; apply the settling flag to non-rulers. (arch) |
| C10 | LOW | **`eotg_flag_aug_iron_retinue` outlives the retinue,** so knights who left keep a +5 progress bonus. | effects `:1509, 1546` | Clear the flag on leaving the court or on the owner's death. (scr) |
| F8/X6 | LOW | **Local Rulers always get vanilla republic or theocracy,** even under a PMC, Corporation, Cartel or Trade Oligarchy liege. Deferred as frontier_v4 D4-4, but it was missing from the taskboard. | `eotg_frontier_effects.txt:1136-1170, 1452-1530` | Pick a government by the liege's flag, once G2 defines vassal-tier governments. (arch) |
| P1 | design | **The four governments drop `government_is_feudal`,** so vanilla content that keys on it (370 readers) is blind to them. | `common/governments/eotg_pmc_government.txt` etc. | Keep them distinct (the current choice), or set the flag on some to gain feudal content. (human) |
| S7, S8, S9, S13 | LOW | The Ban's opinion hit only reaches direct vassals and courtiers. Realm splits reset to Tolerate (G). Demand Removal can't use a clinic under a Ban. The Patron debt dies with its owner. | laws `:60-67`; law group `:23-28`; interactions `:543-556`; stories `:520-551` | Design notes; accept or adjust. (arch) |

## 3. Add to the in-game session plan (`docs/qa/IN_GAME_SESSION_PLAN.md`)

- **F1:** strain on a vassal's Frontier while enemy armies are inside, before occupation.
- **F3:** a Religious completion under a male-only clergy faith: check the theocrat's gender and error.log.
- **F6:** completion while the county is occupied (a holding appearing mid-war).
- **F8:** a Local Ruler's contract under a mod-government liege.
- **X3:** design a character over Raoul (PMC); after unpausing, `eotg_pmc_succession_law` is shown.
- **X4:** cybernetics tier events on a landless adventurer (camp).
- **X7:** an independent Unsworn AI passing the Ban or Favor law.
- **S8:** the cybernetics law of a kingdom that breaks free.
- **T1:** whether per-level `ai_*` values inside the trait's track blocks apply (`common/traits/eotg_augmentation_traits.txt:34-60`).
- **V8:** whether `set_holding_type` creates the barony holder (`eotg_frontier_effects.txt:1376`).
- **M1 (rare, LOW, L):** vanilla's `migration` CB group skips `herders_and_tributary_constraints`, so nomad migration could target Unsworn. Matters only if nomads are present.

## 4. Divergences from vanilla, judged acceptable

- **Frontier is not a great project or a situation.** Great projects are per province, owned by the top liege and DLC-gated. Situations are bound to a region and would break the map-agnostic rule. This was rejected in frontier_v1 §155/195 and still holds. If a progress bar is wanted later, vanilla's nearest analogue is pam's Cathedral contribution (`01_pam_projects.txt:617-632`).
- **Augmentation trait `category = health`.** The one vanilla reader (`pam_decision_events.txt:1167`) also needs `lowers_health`, which our traits don't have, so the only effect is where the trait sits in the UI. The orchestrator checked this.
- **Story cycles, interactions, schemes and the court position** carry vanilla's key sets. The picker widget copies pam faithfully, and every Frontier decision has `ai_check_interval_by_tier`, `ai_potential` and `ai_will_do`.
- **Unsworn vs herder:** the omissions are deliberate. The vanilla trigger override still matches 1.20.1.1 byte for byte.
- **Clean across systems:**
  - on_action layering is additive only, and no child depends on order;
  - no shared identifiers between systems;
  - no recurring `every_living_character`/`every_county` loop in any pulse;
  - save compatibility: two retired county variables, both harmless leftovers.

## 5. Vanilla integration opportunities (ranked)

| Rank | Hook | Gain | Cost and risk | Art |
|---|---|---|---|---|
| 1 | **Decision alerts:** `should_create_alert` on our decisions (`_decisions.info:277`), surfaced by vanilla `action_take_decision` (`common/important_actions/00_action_take_decision_or_interaction.txt:5-45`). Custom `common/important_actions/` entries for "a Frontier is claimable" or "an augmentation offer is open" (pattern `00_title_actions.txt:2-40`). | A top-bar alert; players find the systems | Low; no DLC gate; 4 loc keys per custom action | none (reuse icons) |
| 2 | **Game concepts** (`common/game_concepts/`, `_game_concepts.info`): Augmentation, Seamless, Frontier, Region strain, Unsworn, and the four governments, with `parent`/`alias`. | Linkable tooltips and encyclopedia pages; replaces hand-written explainers | Near zero; pure data, map-agnostic | optional |
| 3 | **Secrets and hooks:** an `eotg_secret_illegal_augmentation` secret type (`00_secret_types.txt`) for procedures under a Ban; vanilla blackmail hooks (`00_hook_types.txt:2-11`) for the kingpin. | Discovery, blackmail interaction, exposure and scandal for free; also gives S1 and S4 a vanilla-shaped answer | Low; check the `.info` fields | none |
| 4 | **Memories** (`common/character_memory_types/`, `create_character_memory`) for the big beats: initiation, the threshold, Frontier completion. | The vanilla past-events UI; hooks for later flavour | 3 perspective loc keys per type | none |
| 5 | **Game rules** (`common/game_rules/`, template `conquerors_frequency` `00_game_rules.txt:130-175`): cybernetics frequency, Frontier difficulty. | Free options UI; owner and testers can tune | Frozen at game start, so add them early; confirm `has_game_rule` | none |
| 6 | **Men-at-arms** for augmented troops (`can_recruit` gated by a government flag or the self-repair innovation). | AI recruitment and a UI list entry | New balance surface | unit art |
| 7 | **Court amenity** "clinic" category (`common/court_amenities/`). | Court-screen UI and a gold sink; could carry rejection-risk modifiers | Royal Court DLC gating unconfirmed; check the UI | optional |
| 8 | **Legends** for completed Frontiers (`common/legends/`). | A spreading prestige narrative | Legends of the Dead DLC-gated; `use_legends` AI flag | legend icons |
| 9 | Dynasty legacy track for augmentation dynasties | Dynasty identity | Adds a track to every dynasty's UI; legacy files crash on scripted triggers | track and perk icons |
| — | **Not recommended:** situations (map-bound), epidemics for rejection (wrong model, needs an overlay). | | | |

Not assessed: activity types, artifacts, accolades, travel, struggles, lifestyle perks, council tasks, and the 1.20 tax jurisdictions, confederations and domiciles (for the governments, check `governments_v2.md` first).

## 6. Suggested order

1. **Fix batch I1 (scripter, then QA):** all of §1. Mostly guards, plus the law AI rescoring; no new content or loc except S6/S11. Best done **before the next in-game sitting**, because the play-test would hit C1, C2 and S3.
2. **Architect ruling pass:** §2 S1, S2, S4, F2, C3, C4 and C6 to C9, with secrets (§5 rank 3) considered as the vehicle for S1/S4. Then the owner approves.
3. **Owner calls:** X2 (kingpin × Cartel, added to CB-57) and P1 (the feudal flag).
4. **Integration batch, owner's pick:** ranks 1 and 2 are cheap, art-free and map-agnostic. Ranks 3 to 5 next.
5. **Add §3 to the in-game session plan.**
