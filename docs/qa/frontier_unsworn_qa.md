# Frontier Systems and the Unsworn Government — QA Assessment

**Date:** 2026-10-11 · **State reviewed:** working tree on `v2-space-map` at `0abde1d` (CK3 is now **1.20.0.4**; Tiger 1.17 targets 1.18.3).
**Scope:**
- **Frontier Systems:** `events/eotg_frontier_events.txt`, `common/*/eotg_frontier_*.txt`, `localization/english/eotg_frontier_l_english.yml`, and the test sub-mod `docs/test_submods/frontier_vanilla`.
- **The Unsworn government / Unclaimed Regions:** `common/governments/eotg_unclaimed_government.txt`, `common/*/eotg_unclaimed_*.txt`, the vanilla trigger override, and `localization/english/eotg_unclaimed_l_english.yml`.

**Measured against:**
- the design brief `docs/design/frontier_systems.md`;
- specs `frontier_v1–v3.md` and `frontier_unclaimed_regions.md`;
- the earlier GeminiQA audit `docs/qa/geminiqa/frontier_audit_r1.md`.

**Method:**
- **Tiger and PX:** a Tiger run and the PX vocabulary check, plus PX language-server passes by the reviewers.
- **Six read-only reviewers:**
  - CK3 engine fit, ×3: the Frontier non-event script and wiring, the Frontier events, the Unsworn government;
  - localization;
  - canon and tone;
  - design fit, with a pacing Monte Carlo and an event census.
- **My own checks:** every HIGH finding and the headline claims, re-checked against the files. These are marked **✔ verified**.

---

## 0. Verdict

| Question | Verdict |
|---|---|
| **Fits CK3 (engine)** | **Yes.** Tiger has **no real findings** in any Frontier or Unsworn file. Every hit is on the known-benign list (county-picker widget ×30, the trigger-override strict-scopes ×17, `rite` ×2), plus `allow_accolades`, which vanilla uses in its own governments and which should be **added to CLAUDE.md's benign list**. The PX vocabulary check found 0 findings; the PX language server found 0 diagnostics. All 19 Frontier events are reachable, with no orphans. The trigger override is **byte-identical to vanilla** apart from its two marked lines. **No blockers.** |
| **Localization coherent** | **Yes. Mechanically clean**, with a few text-versus-effect fixes. BOM, line shape, 0 missing / 0 duplicate / 0 unused keys, every scope reference saved, Canadian spelling, no hard-coded "knight", voice mix within the event-quality target. Canon is **clear**, with no new proper nouns needing vault approval. Fixes: "pressure" vocabulary, four lines that promise what the script doesn't do, and one conquest phrasing. |
| **Works as a CK3 system** | **Sound architecture, thin life around the loop.** State lives on county titles, results hand off to vanilla (development, control, holdings, courtiers, piety), all 8 design hooks exist, and the Unsworn placeholder copies vanilla's own herder pattern. A Frontier settles in **6–16 years**, which fits the design target and CK3's timescale. **Gaps:** the AI barely establishes Frontiers and gets no Frontier events. Player events are rare, fixed-outcome and indifferent to personality. A completed Frontier can hand its ruler a holding that produces nothing (H1). **Almost nothing has been checked in game:** 1 of 142 boxes in the session plan is ticked. |

---

## 1. Must fix (HIGH)

| # | Where | Problem | Fix | Owner |
|---|---|---|---|---|
| **H1** ✔ | `common/scripted_effects/eotg_frontier_effects.txt` ~760–790 (completion results) and `eotg_frontier_build_holding_effect` ~838–875 | **Settled holdings can be dead weight.** Settlement and Trade create a **city** barony and Religious a **church** barony, and give it **directly to the county holder**. Feudal, Cartel and PMC rulers may only hold castles and temple-citadels (vanilla `00_government_types.txt:18-19`; mod `eotg_cartel/pmc_government.txt`). Vanilla's rule then applies: "Due to being the wrong holding type… the holding produces no levies or taxes" (`holdings_l_english.yml:36`). The main reward of three of seven project types does nothing for most rulers. | When the holding type isn't valid for the holder, create a vassal: the settlers' leader as mayor (city), or an elder as bishop (church). That is vanilla's own shape, and it also delivers design §7's "Local Ruler ≠ Political Owner". Confirm who ends up holding the barony with in-game check V8. | architect → scripter |
| **H2** ✔ | `Documents/Paradox Interactive/Crusader Kings III/mod/eotg_test_frontier_vanilla/` | **The installed Frontier test sub-mod is a stale copy** from 2026-10-05, not a link to the repo. Its on_action differs from `docs/test_submods/frontier_vanilla`: it marks all 8 Corsica/Sardinia counties Unsettled, where the repo version releases Sardinia to the Unsworn and marks two counties Unknown. An in-game test today **does not exercise Unclaimed Regions or exploration**, and would give false results. | Replace the folder with a directory junction to the repo folder, as the main mod already is, and change the README's "copy this folder" instruction. | main session |
| **H3** | Unsworn placeholders (`eotg_unclaimed_government.txt`) | **The placeholders are probably playable**, and the mitigations for that aren't built. ✔ Vanilla's `basic_is_valid_for_yearly_events_trigger` (`00_available_for_events_triggers.txt:802-816`) gates only on `is_playable_character`, and nothing in the custom government makes a character unplayable. If in-game check V-U1 confirms it: every placeholder gets vanilla yearly events, and a player can pick one in the lobby. The mod's own pulses are already guarded (M1, re-verified). | **Run V-U1 first.** If playable, build spec mitigations M2 (a second key-level override keeping placeholders out of vanilla yearly events, same file and pitfalls §16 procedure) and M3 (lobby warning). | human → scripter |

---

## 2. Should fix (MEDIUM)

### Frontier
| # | Where | Problem | Fix |
|---|---|---|---|
| F1 ✔ | `eotg_frontier_on_actions.txt:35-46`, `eotg_frontier_effects.txt:642-660` | **No per-ruler cap, and events arrive in bursts.** The cooldown is per county (3 years, then a 50% roll), so each Frontier gets about one event every 4 years. All held Frontiers tick inside one loop in the same yearly pulse, so a player with 8 Frontiers gets about 2 events a year, and with 20 about 5, **on the same day**. The AI is capped (8 on the map, 1 per ruler); players aren't. | Allow one flavour roll per ruler per pulse, and/or fire with `days = { 1 120 }`. The events already re-check their state in their triggers. |
| F2 | `events/eotg_frontier_events.txt:914-989` (.005) | **The AI doesn't follow the spec's failure order.** The spec (`frontier_v1.md:538`) says "d if possible; else b if gold ≥ 2×minor; else a". The script uses flat weights, so the AI takes d only ~55% of the time and ~11% picks c, which isn't in the order at all. b is gated at 1× instead of 2×. | `modifier = { factor = 0 }` gates (vanilla `ep3_admin_events.txt:133,166`), or the architect updates the spec. |
| F3 ✔ | `eotg_frontier_decisions.txt:324-365` | "Back a Frontier" has **no cooldown**, so an AI refusal is only a re-roll. | `cooldown = { years = 1 }`, or a "recently refused" county variable. |
| F4 | `eotg_frontier_effects.txt:514-519` | **The AI auto-founder doesn't check validity.** A child or imprisoned AI holder becomes the founder every year, never counts as valid, and takes +1 "no founder" strain a year with no easing, failing the project at 8 with no other cause. | Limit to an adult, unimprisoned holder; otherwise use the best adult courtier. |
| F5 | founder death, .002/.005 routing | **A player whose founder dies may be unable to name a new one for up to 3 years**, while "no founder" strain builds. The only routes are .002, reached through the cooldown-gated roll, and .005. | Let a founder's death clear the cooldown, or add an "Appoint a Founder" decision. |
| F6 | `eotg_frontier_effects.txt:1639` | A stored holy order is read as a hard scope. Faith-valued variables have vanilla precedent; holy-order-valued ones don't, and the order may be disbanded in between. | Use `?=` and fall through to the lapse branch. |
| F7 | `eotg_frontier_effects.txt:530-537` | **War strain is blunt.** Any war the holder is in, including a distant ally's call, adds +1 strain a year, and a quiet year doesn't follow it. Eight war years fail any non-Military project, and CK3's AI is often at war. | Add strain only when the county is occupied or has hostile armies in it, or when the holder is war leader or defender. |
| F8 | `.040`, `.021.h` vs `.034` weights | The "danger countered" tooltips over-claim. A mercenary escort or garrison doesn't lower the raider event's +10 weight for a Dangerous Region, unlike the beacon's −5 for a Remote one. | Add `modifier = { add = -5 … }` for the escort and garrison modifiers, or soften the tooltips. |

### Unsworn / Unclaimed
| # | Where | Problem | Fix |
|---|---|---|---|
| U1 | `eotg_unclaimed_effects.txt:454-475` (claim), `:135-153` (create) | Only the county and its **capital** barony move. If a placeholder also holds a non-capital barony (hand-authored history, or a missed "holding = none"), it survives as an independent, war-immune, un-vassalizable Unsworn baron inside the claimant's county: a permanent enclave. | Move every barony in the county held by the old placeholder, and add a yearly-sweep rule: an Unsworn holder whose capital county isn't Unclaimed vanishes. The cartographer keeps §10.5 (non-capital baronies `holding = none`). |
| U2 ✔ | `eotg_unclaimed_effects.txt:35` (`eotg_unclaimed_release_effect`) | **No guard against releasing a real ruler's capital or only county.** The capital rule (UQ5) lives only in the separate `eotg_unclaimed_would_release` trigger. The Frontier test sub-mod releases the Sardinian judges' counties, which probably include their capitals, so the judges would end up landless while their vassals stay. | Skip `holder.capital_county` when the holder isn't Unsworn, or document the precondition. In the test, check no judge ends up landless. |

---

## 3. Low priority (one batch)

**Frontier**
- **Development loss:** abandoning costs −1 development even when this attempt granted none, so resettle/abandon cycles drain development. This is a ruling ("Abandon keeps its −1"); the architect should confirm it.
- **Gold lost in .004.a:** root pays `minor_gold_value` at its own scale and the founder receives it at the founder's scale. Save the value first.
- **Hard-coded prestige in .004.b:** `add_prestige = 100/25` should use the script values.
- **Spec drift:** spec §6.6(c) says the project type is re-picked; the code forces settlement. The spec is stale.
- **The explore decision's trigger** scans every Unclaimed county with a distance test each time the panel refreshes. Watch it once the real map lands.
- **Modularity runs the wrong way:** 17 live Unclaimed references sit inside Frontier's core files, so Frontier can't load without them. Route them through one seam file, or record the coupling as accepted in the spec (design §2.1).
- **Expected noise:** the two public hook effects (`offer_backing`, `set_trade_network`) have no callers by design, which explains the one "used but never set" line in error.log.
- **A skipped tick** when a Region changes holder mid-year. Accepted by verification Q9.

**Unsworn**
- **Order of operations:** `change_government` runs before `becomes_independent`. The government has no vassal contract group, so the order should be swapped to avoid "no contract" lines in error.log.
- **Corporate government flash:** releasing a county from a PMC, Corporation, Gob-Corp or Cartel holder gives the new placeholder that government for a moment, because of `use_as_base_on_landed`. Test one corporate abandonment (V-U15).
- **Sweep cost:** the yearly sweep walks `every_living_character`. Track Unsworn holders in a global list instead.
- **Placeholder lifecycle:** placeholders age and die. Watch for death-notification spam (V-U8).
- **Hook ordering:** the test sub-mod's release and the main split both hook `on_game_start` in no fixed order. Harmless while the hook is empty.
- **Placeholder AI:** it can still run schemes and activities, the same gap herders have.
- **Real map:** the main `history/` has no `eotg_unclaimed_seed` yet, so the system is inert until Gate 1. The seed must carry the trait.
- **Blocked-war message:** a declaration blocked against an Unsworn holder shows auto-generated trigger text. Spec §14's `eotg_unclaimed_defender_tt` was never built, so nothing points the player to "Raise Your Colours".

---

## 4. Localization and canon

### 4.1 Mechanical: clean
- Both files start with one BOM and the `l_english:` header; all 361 + 43 key lines are well-formed. Speech uses vanilla double quotes, with no escaped quotes or single-quote speech.
- **0 missing keys:** every referenced key resolves, and all implied keys exist (14 decisions ×4, 37 modifiers ×2, opinions, trait, government name/adjective/realm/desc/with-icon plus flag line, interaction).
- **0 duplicates** across `localization/`, and 0 collisions with vanilla keys. **0 unused keys.**
- **0 `[scope:`**, and all 12 scope names used in loc are saved in script. Data functions are vanilla's.
- **Style rules met:** no hard-coded "knight", Canadian spelling throughout, no em or en dashes.
- **Event quality:** the narration voice mix is 63/26/11, inside the 60/35/5 target; dialogue appears in 42% of events.

### 4.2 Text that promises what the script doesn't do
| Sev | Key | Text says | Script does | Fix |
|---|---|---|---|---|
| HIGH ✔ | `eotg_decision_frontier_abandon_desc` (frontier:29) | "What was built stays where it stands" | Clears all infrastructure; −1 development if a milestone was reached; only a salvage record survives | "Most of what was built is lost, but its ruins remain…" (line 32's tooltip already says this) |
| MED | claim tooltip (unclaimed:45) | "You may now Establish a Frontier here." | Establishing is blocked while the Region is still Unknown | Add "once it has been explored", or make the line conditional |
| MED ✔ | `.040.desc_military` (frontier:360) | "[county] is being taken by force… A contract buys the company's guns and its ships" | A Military Frontier is a garrison in your own Region, and the only real option has the company **backing** you (paying you) | Reword to the backing frame. Both the localization and canon reviewers flagged it: conquest contradicts the Unsworn premise. |
| MED | `.030.desc` (frontier:265) | The rival backer offers "better terms" | Mechanics identical to the current sponsor; the line also contradicts itself, and the sponsor's name repeats 4 times | Pitch "a fresh start" or "more reliable"; use pronouns |
| LOW | `.031.a_tt`, `.031.c`, `.032.a`, `.032.b` (liege variant), `.035.a_tt` | "slows the work", "first returns", "a content camp works harder", "the settlers feel it", "pauses" | Strain only; immediate gold; tax modifier, no progress; no terms were offered; −2 progress | Reword (details in the localization review) |

### 4.3 Coherence and canon
- **"Pressure" is the player word for Frontier strain** ✔ (frontier:93, 96, 132, 290, 365). It's the same collision cybernetics was moved off: v1's Void uses "Void Pressure". **Use "strain"**, which matches the script variable. Keep line 83's literal "pressure seal". The architect should rule on who owns "pressure" alongside the Void lift plan §3c.
- **"Frontier Legacy: Trade/Industry/…"** collides with vanilla dynasty Legacies and the mod's Confluence Legacies. Suggest **"Frontier Roots: …"**; avoid "Heritage" (vanilla's culture pillar).
- **The Unsettled modifier** says "No permanent settlement has taken hold here yet", but the Unsworn live there. Suggest "Nothing here has grown past scattered households and stations yet…".
- **The claim prestige tooltip:** "make it stick" can read as others accepting the claim, which LAW AT 866 forbids. Suggest "…for crews to sail under your flag."
- **Casing and terms:** "abandoned"/"Abandoned"; the debug "Unknown" vs the player-facing "Unexplored Region"; `eotg_unclaimed_government_with_icon` hard-codes "Unsworn" (vanilla uses `$herder_government$`).
- **Canon: clear.** No text says a claim is filed, registered, recognized, licensed or chartered. No Council, Frontier Guard, League, Exodus, Myr or Grip. Unclaimed space isn't framed as empty. The technology level fits 866. No new organization, place or person needs vault approval. **Tone reads as space-age settlement** (crews, stations, convoys, surveys), not medieval. Frontier and Unsworn text agree, and nothing touches the cybernetics register.
- **GeminiQA GQF-001 ("Systems" in the government description): not a bug. Close it.** The real reflavor glossary (`OLD PROJECT VERSION/docs/localization_crusade.md`) is **Barony→System, County→Region**, and the text calls the claimed unit "Region" correctly. One reviewer cited "County→System" from a stale memory note; I have corrected that memory note. GQF-002 and GQF-003 are fixed; GQF-004 and GQF-005 still pass.

---

## 5. Does it work as a CK3 system?

### 5.1 Design coverage (`docs/design/frontier_systems.md`)
| § | Feature | Status |
|---|---|---|
| 3 | Unsettled → Frontier → Settled → Abandoned | Built. Real-map marking of owned counties deferred. |
| 3.1, 13 | Explore / survey / expedition (Unknown → Partial → Known) | Built |
| 4.1 | 7 project types | Built (all 7). **Results partial:** no vanilla buildings are placed, and Research has no technology or innovation output. |
| 5 | Founder | Partial: picked automatically (best steward, or the taker); no choice of adventurer, dynasty member or merchant |
| 6, 7 | Sponsor; founder ≠ sponsor ≠ owner | Built. The sponsor only converts gold into progress. |
| 8, 9 | Hidden development from CK3 inputs; infrastructure (8 pieces) | Built |
| 10 | Traits (10/10) | Built; at most 2 known per Region |
| 11 | Events | **Partial:** 19 events, 71 options |
| 12 | Failure (strain 0–8) | Mostly built |
| 14 | Hooks (8/8, plus 5 extra) | Built; only `on_abandoned` and `on_settled` have consumers (Unsworn) |

### 5.2 The player loop and pacing
- **Start:** find a grey county and use **Raise Your Colours** on its Unsworn holder (minor gold plus 75 prestige, 5-year cooldown, the county must be in reach). Then **Establish** (medium gold, not while at war) and pick one of 7 types.
- **During the project:** Invest yearly, Build infrastructure (at most 1 a year), Survey every 5 years, Expedition yearly, Abandon.
- **Time to Settled** (2,000-run Monte Carlo, development 1, control 100, founder stewardship 10):

| Type | Bare | Sponsored | Invest every year | Sponsor + invest + build |
|---|---|---|---|---|
| Settlement | 12 y | 9 | 8 | 6 |
| Trade, Mining, Military, Admin | 14 | 9–10 | 8 | 6 |
| Religious | 15 | 10 | 9 | 6 |
| Research | 16 | 11 | 9 | 7 |

  That's on the owner's target of 10–16 unsponsored and 8–10 sponsored.
- **Events:** about 1 every 4 years per Frontier: 3 per bare project, **1.5 per fully funded one. Funding the project removes its story.**
- **Legibility:** the stage modifiers, milestone toasts, county-picker widgets and the grey Unclaimed colour are good. But **nothing shows what drives progress, how far along a project is, or its strain**, except .002's description bands. The claim is an interaction on a placeholder character, so nothing points the player to it.
- **Sponsor economics:** investing yourself gives +5 per minor gold; a sponsor gives +3 per minor gold paid, and gets nothing back but opinion.

### 5.3 The AI
- **Claiming:** a worldwide 180-day gap caps AI claims at **2 a year**, and each AI holds at most 2 claimed, unsettled counties. No runaway: the 161 Unsworn counties in the British Isles test would take 80+ years to fill.
- **Establishing:** checked every 48–60 months at a 10–35% chance, and only with gold ≥ 2× medium. The **mean wait after a claim is about 11–50 years (typically 25–35)**. One Frontier per AI, 8 active across the map.
- **Throughput:** at most about 0.5–0.7 settled a year against 2 claims a year. **Claimed but never-established counties pile up** until every border AI hits its cap of 2. The claim counts forever, because the lapse rule (UD3) is deferred.
- **No events for the AI:** AI holders get no Frontier flavour events, only scripted sponsor offers.
- **Net:** leans to **inertia, not runaway**. The galaxy "building itself" (design §23) will mostly happen only where the player acts.

### 5.4 Design issues, ranked
1. **AI participation (biggest gap).** Raise the Establish weight to 40–60 when the AI holds a claimed Unsettled county, with a 24-month interval and a 1× gold gate. Scale the map-wide cap with the number of Unclaimed counties. Gate AI claims on affording claim plus Establish, or build UD3 (an AI claim lapses after N years).
2. **H1** (dead holdings). See §1.
3. **Nothing confirmed in game.** V-U1 (playability), V-U14 (whether placeholders count as neighbouring rulers, which decides whether AI claims happen at all), V8 (holding creation) and V12 (scopes reaching hooks) decide H1, H3 and the Unsworn listeners. **Run plan §U sitting 1 before any new content**, after fixing H2.
4. **Events are thin and fixed** *(new events are your call)*. 11 events in the flavour pool; all 71 options have fixed outcomes; **0 trait-gated options, 0 `stress_impact`**. Only 14 of 36 personality traits appear, and only in AI weights. Design §11: positive 3 of 7, negative 3 of 8 (disease, hostile inhabitants, collapse, shortage are missing; raiders exist only as description lines), political 3 of 6. **Cheap first step, no new events:** add `stress_impact` and skill-weighted rolls to existing options.
5. **War strain is blunt** (F7).
6. **Legibility and sponsor value.** Put the year's inputs in the Invest and Build tooltips as qualitative bands ("about N years remain", "under strain"). Raise the sponsor's input. Give the sponsor a completion reward.
7. **Claiming is hard to discover.** Add a "Raise Your Colours" decision using the same county-picker widget as Explore (`eotg_frontier_decisions.txt:970-976` already lists in-reach Unclaimed counties). Keep the interaction.
8. **Modularity** (see §3).
9. **Unsworn base-game risks:** see H3 and the Unsworn items in §3. Watch them in a 20-year observer run.
10. **Founder choice** is automatic (design §5 wants adventurers, dynasty members and merchants as candidates), and research projects yield no technology.

---

## 6. In-game checks (human), in order
0. **Fix H2 first** (link the test sub-mod), or nothing below is trustworthy.
1. **V-U1** — can a placeholder be played or picked in the lobby? Decides H3.
2. **V8** — which character holds the barony created at completion? Is a city or church holding dead for a feudal holder? (H1)
3. **V-U14** — do placeholders count as neighbouring rulers, so that AI claims happen?
4. **V-U9 / V-U8** — does `on_title_gain` fire on scripted transfers, and can titles transfer inside `on_death`?
5. **Frontier pacing:** hold 3+ Frontiers, run the debug tick a few times, and count same-day events (F1).
6. **A blocked war** against an Unsworn holder: read the tooltip (§3).
7. **A release from a corporate holder** (V-U15), and a release of a Sardinian judge's county: does the judge end up landless? (U2)
8. **Error log** after a faith-backer or holy-order succession (F6).

## 7. Suggested order and owners
1. **Main session:** H2 (link the test sub-mod), and add `allow_accolades` to CLAUDE.md's benign list.
2. **Human:** the in-game sitting (§6 items 1–4).
3. **Architect:** H1 (vassal-holder rule), AI participation (§5.4 #1), F1, F2, F5, F7, the "pressure" ruling, and the Legacy rename.
4. **Scripter:** F3, F4, F6, F8, U1, U2, then H3 mitigations if V-U1 says playable, then the low batch.
5. **Localizer:** §4.2 and §4.3.
6. **Content (your call):** stress responses and outcome rolls on existing events first; new events for the §11 gaps later.

The reviewers' scripts (event census, pacing Monte Carlo, localization checker) and the Tiger and PX logs are in this session's scratchpad, which is temporary.
