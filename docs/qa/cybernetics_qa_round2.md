# Cybernetics — QA Round 2 (after the v2 expansion)

**Date:** 2026-10-03 · **State reviewed:** the working tree after cybernetics v2 Phases 0–6 (`docs/specs/cybernetics_v2.md`). That is 152 events in 11 files, 4 story cycles, 4 endgames, 13 decisions and about 26,000 lines.
**Focus (as asked):**
1. Does it fit into CK3?
2. Is the localization coherent?
3. Does it deliver the goal of bringing cybernetics to CK3?

**Method:**
- Tiger 1.17 run against the whole mod. The game is now 1.20.0.3 and Tiger warns that it targets 1.18.3.
- Seven read-only reviewers:
  - CK3 engine fit, ×4, split by file: `common/` and wiring; initiation, tier 1 and tier 2; Overclocked and Neurofractured; the arcs, endgames and non-ruler events.
  - Localization coherence.
  - Canon and tone.
  - Design/goal fit, with event-graph parsing and Monte-Carlo pacing.
- I re-checked every HIGH finding and the headline claims against the files myself. Those carry **✔ verified** below. Everything else is the reviewer's claim, checked against vanilla citations they supplied.

---

## 0. Verdict

| Question | Verdict |
|---|---|
| **Fits into CK3 (engine)** | **Yes, with a short fix list.** Tiger reports nothing in any cybernetics file except one missing icon (`eotg_total_integration.dds`, known art debt). All 152 events are reachable, with 0 orphans and 0 undefined ids. Every effect, trigger, scope link, hook, theme, animation, death reason, story-cycle field, faction and diarchy call was found in vanilla 1.20 in the same shape. No blockers. 4 HIGH logic bugs. |
| **Localization coherent** | **Yes. Mechanically clean; a handful of coherence fixes.** BOM present, 1,334 keys, 0 missing, 0 duplicates, 0 unused, no `[scope:`, every `[x.Func]` traced to a saved scope, and nothing quantifies the hidden risk. Canon passes with no new proper nouns. The voice is consistent from first beat to last. The fixes are vocabulary ("pressure"), three naming collisions, and some text that promises more than the effect delivers. |
| **Brings cybernetics to CK3** | **Mostly, as a design.** It uses CK3's own machinery throughout: a track trait, stress level as the visible proxy for the hidden risk, story cycles, real factions, regency, duels and vanilla trait reactivity. It exceeds every content target and gates options on all 36 personality traits. **The biggest gap is pacing:** progression takes decades, the AI barely uses the decision layer, and the likely world has many Augmented rulers and almost no Overclocked or Neurofractured ones. That is the half of the system where most of the goals are actually delivered. |

---

## 1. Must fix (HIGH)

| # | Where | Problem | Fix | Owner |
|---|---|---|---|---|
| H1 ✔ | `events/eotg_augmentation_fracture.txt` ~2737–2758, fracture.020 (The Plot reveal) | Every false accusation gives the accused and family −30 "falsely accused" for 10 years in `immediate`, **including when the ruler only watched or explicitly spared them** (019.e already gave +15 reassured). In those cases only the fallback option is valid, and its false branch ("I was right anyway.") adds tyranny, lie stress and risk. The ruler who chose correctly is punished, contradicting `desc_false_spared` ("you were right to"). | Limit the opinion to `arrested` / `executed` (watched gets unease at most). Give watched and spared their own fallback: "So I was right not to." with no tyranny and risk −5. | scripter + localizer |
| H2 ✔ | `events/eotg_augmentation_retinue.txt:726-730`; on_action ~280; `initiation.txt:2559/2589/2690`; effects ~1212 | **The Iron Retinue restarts after it ends.** .005 ends the story but records nothing, and every start path checks only `eotg_aug_has_retinue = no`. With 2+ augmented knights left, init.019 re-arms and the Program loops, even after "Stop recruiting". | Set a permanent `eotg_flag_aug_retinue_done` in .005 `after`, and check it in all three start paths. | scripter |
| H3 ✔ (timing) | `events/eotg_augmentation_heir.txt:513-518` | heir.005 "What Must Be Done" is sent to the heir 3–7 days out, **while the heir is still AI**. The AI picks the option and the ruler dies in its `immediate`, so the player never sees the scene. Its desc ("Your hands are steady") is written for the player. | Kill the ruler in a hidden event first, then send heir.005 to the heir after succession, when they are the player. Confirm in game. | scripter |
| H4 ✔ | `initiation.txt:2671-2677` (init.019.c), `retinue.txt:523-529` (retinue.004.a) | `ordered_knight` with `max = 3` and **no `check_range_bounds = no`**. No file in the system uses that flag. With 1–2 knights, which is the usual case, the engine logs a range error. `max` is an inclusive index, so it also reaches up to 4 knights while the cost charges for 3. In retinue.004.a, gold may be charged and the installs skipped. Vanilla pairs the two: `feast_tsagaan_sar_events.txt:1215-1217`. | `max = 2` and `check_range_bounds = no` at both sites. | scripter |

---

## 2. Should fix (MEDIUM): engine and logic

| # | Where | Problem | Fix |
|---|---|---|---|
| M1 ✔ | on_action NF check ~975–1019, with `eotg_trigger_neurofracture` (effects ~252) | **The cascade pulse also gets a year of Neurofractured drift (+8 to +20), and the Heir's Arc can start the same day.** The cascade runs inside the Overclocked check, and the NF check runs later in the same pulse. The 11-month cooldown blocks only the roll. | Gate drift and arc creation on `NOT = { has_character_flag = eotg_flag_nf_event_cooldown }`, or set a 1-day "cascaded this pulse" flag. |
| M2 | effects ~1028–1037 (Excision) | After a `random_list` whose branch kills the patient, the code checks `is_alive = yes`. If death processing is deferred, a patient who died on the table gets the survival event and prestige. PLAUSIBLE. | Test `exists = scope:eotg_excision_outcome`, which only the survival branches save. |
| M3 | tier2.017/.018/.021, tier1.017 (and other delayed stages) | Delayed stages call `eotg_add_fracture_risk` without checking the ruler is still augmented. If they left the system in between, the risk variable is recreated, which breaks the remove-all promise. | Add `eotg_is_augmented_any = yes` to the helper's own limit. One change covers every caller. |
| M4 | fracture.002.c, tier3.001.c, tier3.015.e, tier3.017.b, fracture.019.c | **Deliberate killings of family carry no kinslayer.** Vanilla adds it in script (`add_kinslayer_trait_or_nothing_effect`, `00_secret_effects.txt:433`), not in code. The victim picker can choose family (0.05, or 0.25 in Storm), and `random_vassal` in tier3.017 / fracture.019 is unfiltered. | Add the vanilla effect to the deliberate options. Leaving the involuntary episodes without it is a design call; document it. |
| M5 | fracture.006.a/.c, .019.a/.d, .024.c, .025.d, tier2.015.d | Bare `imprison` means no tyranny and no family fallout. tier3 uses vanilla `imprison_character_effect`, so the two halves of the system disagree, and 019.a jails a landed vassal for free. Separately, **tier3.006.a counts tyranny twice** (wrapper plus a manual +15). | Use the vanilla wrapper everywhere and drop the manual tyranny where the wrapper is used. |
| M6 | tier3.017.b, fracture.019.c | Executing a free vassal costs almost nothing up front: 20 dread or nothing, with tyranny arriving only later if the accusation was false. | Add 15–20 tyranny now, or imprison first and execute in the follow-up. |
| M7 | tier3.014.a | The tooltip gives away the hidden truth: "Trust them." shows a gold loss only when the envoy is exploiting you, which is what option b exists to find out. | Wrap it in `hidden_effect` with a neutral custom tooltip. |
| M8 ✔ | fracture.011 a/b/c/e | All options show when the desc says "No one else was there", and c charges gold with no one to pay. | Add `trigger = { exists = scope:eotg_witness }`, or add no-witness variants. |
| M9 | nonruler.txt (all 6 triggers) | Only `is_alive` is checked on the champion. If they left court during the 1–30 day delay, options imprison or pay for a stranger. | Add `scope:eotg_champion = { is_courtier_of = root }`. |
| M10 | triggers ~304–311 | `eotg_aug_patron_critic_candidate` has no `is_adult`, so the Patron can ask you to murder a child. | Add `is_adult = yes`. |
| M11 | endgame ~384–393 (end.011.a "Hire replacements") | Hires no one, and costs major gold with no gold gate (debt). | Create courtiers from a vanilla template and gate on gold, or reword the option. |
| M12 | stories ~394–402 (Patron) | Envoys are never cleaned up. Each .007 adds another permanent courtier. | In `on_end`, move a living envoy to the pool. |
| M13 | effects ~1275–1284 | A non-ruler cascade doesn't end the Countdown, so a landless Overclocked ex-ruler who cascades still gets countdown.006 "The Quiet". | Call `eotg_aug_end_countdown_effect` from the non-ruler cascade, and add a Neurofractured guard to .006. |
| M14 | tier2.001.a, tier2.006.a | Free timed +2 intrigue with no cost. It beats option b for most characters (spec §1 rule 6). | Add +2/+3 risk, which also strengthens resource coupling. |
| M15 | Containment Regency (fracture.025) | It may be refused or ended early on a capable adult liege. Spec Q7 is still open. | **In-game check** before any change. |

**Low-priority items (one batch for the scripter):**
- **Missing re-checks:**
  - tier3.024 has no trigger (add the tier and at-war check).
  - tier3.015 and tier3.021 don't re-check root's tier.
  - tier2.008 and init.013 dereference a variable without a guard or a desc fallback.
- **Gold:**
  - These spend gold with no `gold >=` gate: fracture.011.c, .013.d, .014.a, .016.e, .021.a, tier3.009.a, tier3.014.a.
  - Gold paid before a chain stage that can fail is lost (tier1.002 → .021, init.007 → .008).
- **Trait guards:** tier3.004.a adds `paranoid` to a possibly `trusting` ruler. fracture.005.c guards only against `compassionate`, not `sadistic`.
- **Wrong or unwanted effects:**
  - fracture.002.c uses `death_murder` for an execution; it should be `death_execution`.
  - fracture.018.c's double scramble can undo itself.
  - Warrant `create_faction` can conscript a multiplayer player vassal; vanilla filters `is_ai = yes`.
- **Retinue and Embrace:**
  - Retinue phase 1 can stall forever with no candidate.
  - Total Integration strips the Retinue modifier while the Program runs.
  - Stories keep running on a deposed owner.
  - Embrace the Cascade has no cooldown.
- **Unflagged victims:** the tier1.018 copycat uses a bare `random_courtier`, and the tier1.010.a sparring partner is never flagged.
- **Install paths:**
  - init.002.c installs on a knight with no stress helper, unlike init.017.c.
  - A ruler-designer pick of `eotg_cybernetics` (cost 20) skips the install effect: no synergy, no risk variable.
- **Leftover flags:** `eotg_flag_aug_hidden_flaw` survives Remove Implants.
- **Other:**
  - The Countdown can start and end in the same pulse.
  - `eotg_aug_is_nonruler` is never used.
  - Augmented landed barons get no yearly content: they are neither count+ nor employed.
  - 7 saved scopes lack the `eotg_` prefix: `watching_heir`, `aug_peer`, `concerned_vassal`, `petitioning_knight`, `aug_spouse`, `confessor`, `other_machine`.
  - Optional performance guard on `eotg_on_death_aug_grief`. Performance is otherwise fine: the cheap trait check comes first on the everyone-pulse, and nothing runs monthly.

---

## 3. Localization

### 3.1 Mechanical: clean
- UTF-8 BOM, `l_english:`, 1,334 well-formed lines, no tabs or stray quotes.
- **0 missing** of 1,168 referenced keys, plus every implied key (decisions ×4, modifiers ×2, opinions, traits, death reason, track label).
- **0 duplicates.** It is the only `.yml` under `localization/` and there is no `replace/`.
- **0 unused**, apart from the two track keys the engine reads automatically.
- No `[scope:`. One `[ROOT.Char.MakeScope.Var(...).GetValue]` (end.011), a valid vanilla form. Consider `|0`.
- All 92 `[x.Func]` references trace to a `save_scope_as` in the event or upstream in the chain. Option names that contain a scope are guarded with `exists`.
- Singular "they" is used throughout. No hardcoded he/she.
- **Hidden-risk rule holds:** no numbers, no "risk +n". The approved "the static quiets" wording is present.

### 3.2 Coherence fixes
| Sev | Issue | Lines | Fix |
|---|---|---|---|
| HIGH (cheap) ✔ | **"Pressure" as player vocabulary for the hidden resource.** The Void system's v1 loc uses "Void Pressure" / "the pressure recedes". That file is frozen in `OLD PROJECT VERSION/` and not yet in v2, so this is a **future** collision, but the spec's rule is that the two registers never blur. The tiers also use "static" for the same resource, so the player sees two words for one thing. | 347, 726, 854, 857, 858, 881 | Use "the static" (already approved and augmentation-only) everywhere. Add the errata line from the canon review to SETTING LORE. |
| MED | init.002 "A Corporate Offer" and "syndicate representative" in init.001/.002 collide with the Patron's unnamed "syndicate". The Patron naming rule also bans "Corp". | 101, 108–109 | Retitle, and call generic sellers "clinic" / "vendor". |
| MED | Three events titled "(A/The) Familiar Change": init.005, fracture.024, nr.005. tier3.019 "The Delegation, Revisited" is not a sequel to tier3.006. | 129, 673, 1620 | Retitle, e.g. nr.005 "Not Quite Them", tier3.019 "Lighter Hands". |
| MED ✔ | tier2.003 says "The next tier of modification is not reversible", but the Downgrade Protocol and tier3.020 reverse it. | 202 | "does not come out cleanly" |
| MED | tier2.005: "spiritual advisor" in the desc, "confessor" in the outcomes. "Confessor" is also faith-specific. | 216–224 | Use "advisor" throughout. |
| LOW ✔ | Wording rules: "Reflexes are inhuman" (multi-species rule), "too much grip" (the cataclysm's name), "It watches you" (banned voice phrase). | 56, 130, 169 | Reword. |
| LOW | Tier register slips: tier1.008 *Dulled Palate* and tier1.020 *Something Is Missing* are Enhanced-style affect loss sitting in tier 1. Three "one clear hour" events (fracture.003/.007/.026). | — | Move them or soften. Vary the third clear hour. |
| LOW | Mixed option point of view (second-person options among first-person and imperative), narration inside an option (fracture.003.c), "anymore"/"any more", "catalogued" in American text, lower-case "the overclocked", a fragment friend reason (tier3.015), "Containment Regency" vs "Warden" never connected, two decisions sharing a closing sentence. | various | Style pass. |
| note | The Void's v1 text ("in your own interior language") drifts onto augmentation's ground, not the reverse. Fix it when Void is lifted. | v1 void loc | Route to the architect when Void is lifted. |

### 3.3 Text that promises more than it does
- **Medium:** fracture.011 (witness options with no witness; see M8).
- **Low:**
  - tier2.012.b "Take their access keys": the spymaster keeps the seat.
  - tier3.007.d "Recruit them": no one joins.
  - fracture.004.d "Hand myself to the court's judgment": no judgment happens.
  - nr.004.b and countdown.004.a "Pay off the victim/family": no opinion change for them.
  - nr.004.c "Restrain them, and have them treated": no restraint.
  - nr.003.b "Relieve them of duty": they stay a knight.
  - nr.001.c and retinue.002.d "they pay for it": no gold leaves the knight.
  - retinue.002.b "The stronger one" shows with only one candidate.
  - end.011.a (M11).
- **Verified as matching (36 of 46 sampled):** every arrest imprisons, every kill uses the right death reason, every release fixes opinion, and all 12 decision tooltips match their durations and effects.

### 3.4 Canon and tone
- **No contradiction.** No Void, Orrin, Grip, Exodus, Myr, League, Nikios, Helix, dates, faiths, cultures or titles. The syndicate stays unnamed, and no vault approval is needed.
- **Tone holds together.** Feudal frame plus transactional tech: invoices, warranties, firmware.
- **Neurofractured is a genuinely different register** (logs, designations, "we", permissions). The canon review called it the strongest writing in the file.
- **The voice keeps its tells across all six beats.** It never whispers and never "comes from" anywhere.
- **Sensitive content handled with restraint:** the Sickly Child, the suicide option, the sadistic "Let them finish". One wording tweak: init.014 "The experimental procedure" → "The back-street version".

---

## 4. Does it bring cybernetics to CK3?

### 4.1 Scorecard (goals from `cybernetics_system_overview.md` §4)
| Goal | Status | Evidence |
|---|---|---|
| Power outpaces stability | Met, **inverted at the top** | The tier stats escalate. But Seamless (Total Integration) gives +20 prowess, +4 to four skills and −75% stress, and Embrace → end.009 a/c grants it **with no roll**. |
| Terminal stakes | Met, **but can be paused** | 4 endgames, all reachable. The terminal arrives in about 5–12 years. But calm drift +8 minus Sedation (−6) and Restraints (−4) is **−2 a year**, so Neurofractured can be held indefinitely. |
| Everyone takes part, AI included | Partly | About 55–80% of eligible AI rulers augment within 20 years, but only about 6–10% reach Overclocked within 40 years. 10 of 13 decisions are effectively unused by the AI. Non-rulers progress 4% a year. |
| The tier arc reads | Partly | The prose differs by tier. 99 of 152 events share the same 5-option template. |
| Robust, varied events | Met on volume and size, **partly on outcomes** | 152 events and 670 options: 75 single-screen, 51 chain heads or stages, 22 driven by story cycles, 4 fired by decisions. **91% of options have fixed outcomes.** |
| Neurofractured is a different extreme | Partly | The scaffolding is different: drift, 3 band pools, terminal, decisions, Warrant, Regency, Heir's Arc. The events are shaped like Overclocked ones. "The implant decides" appears in only 2 NF events, and the "plot that isn't real" pattern also exists at Overclocked. |
| Wide trait coverage | **Met** for personality traits | All 36 are gated, stressed and AI-weighted at least once. Thin: chaste, fickle, impatient, lustful, gluttonous, temperate (1–2 options each). Coping traits and congenital traits are unused, and `lifestyle_mystic` is named in the spec but unused. |
| Hidden risk; XP at thresholds only; map-agnostic; cooldowns owned by on_actions; coupling | Met | No counters. 10 XP call sites, all 0/50/100. No title, culture or faith keys. |

### 4.2 Content delivered
| Stage | Events | Target (gaps §3) |
|---|---|---|
| Initiation | 20 | ~11 ✔ |
| Augmented | 22 | ~12 ✔ |
| Enhanced | 21 | ~12 ✔ |
| Overclocked | 24, plus the 6-stage Countdown | ~14 ✔ |
| Neurofractured | 29 (bands: Flicker 9, Fracture 10, Storm 7), plus the 4-stage Heir's Arc and 8 endgame events | ~25 ✔ |
| Arcs | Patron 7, Retinue 5, Non-ruler 6 | 3 large arcs ✔ (Clinic deferred, Q10) |

Decisions: 13 against a target of about 11. Story cycles: 4.

### 4.3 Design issues, ranked
1. **Progression is a lottery, and the expansion diluted it. ✔ (weights verified)** The Upgrade is one weight-30 branch among 15 tier-1 branches (about 275) plus 150 for "nothing", behind a 2-year cooldown. That is roughly 8% per eligible roll. Simulated median for a player who **always accepts**: about 32–44 years from initiation to Overclocked, and longer for the AI. Roughly 71 of 152 events (Overclocked, Countdown, Neurofractured, Heir, endgames) sit behind that wait, and no decision lets the player pursue the next stage. **Fix:** a "Pursue the Next Stage" decision (minimum years at tier, gold and dev gates) that fires tier1.002 / tier2.003. Or move progression into its own roll whose odds grow with time at tier.
2. **The AI's decision layer is inert.** `ai_check_interval = 120` with `ai_will_do` 3–15 means about 0.3–1.5% a year. The AI almost never regresses, so AI Overclocked rulers almost always cascade, and Excision, Warden, Embrace and Augment Retainer never happen. **Fix:** `ai_check_interval_by_tier` at 12–36 months (vanilla uses it 412 times), with conditional `ai_will_do` (e.g. regression 50+ while the Countdown runs at stress level 2+).
3. **Wide spread, shallow depth.** The physician branch is nearly universal, and so are back-alley (low gold) and aging (50+). The Augmented tier is almost free. Likely world: everyone Augmented, no one Overclocked. **Fix:** a 50-year observer test, vanilla-style AI throttles (`yearly_on_actions.txt:3022-3030`), and an ongoing cost at Augmented.
4. **Neurofractured events look like Overclocked events.** **Fix:** turn 6–8 Fracture/Storm events into forced or hidden-override events, with override odds rising by band. Add misleading desc variants in Flicker. Drop the third universal option in Storm.
5. **Neurofractured can be paused, and Seamless is a guaranteed win.** **Fix:** give Sedation tolerance on renewal. Make Embrace a weighted roll (death, a Storm episode or Seamless), or give Seamless an ongoing realm cost.
6. **Outcomes are fixed (91%).** **Fix:** in each of the 23 chain heads, make one universal option a skill- or trait-weighted roll (vanilla duel and skill-check pattern).
7. **The non-ruler lifecycle is too slow to see.** At 4% a year, a knight augmented at 20 typically breaks after 45+ years. **Fix:** about 10% a year, battle accrual, and a faster track for retinue knights.
8. **Patron and Retinue are side piles, and one seed goes nowhere.** Neither arc references tier, Neurofractured or the voice. `eotg_flag_aug_child_patient` (the Sickly Child) is set and never read. The Heir's Arc starts only at Neurofractured, the rarest state given issue 1. **Fix:** make the Patron and the Retinue react to tier and Neurofractured. Read `child_patient` in the Heir's Arc and the non-ruler weights. Allow Heir's Arc seeds from Overclocked.
9. **The vanilla stress and mental-health layer is ignored.** Overclocked (+40% stress) and Neurofractured (+60%) will hit vanilla mental breaks and coping traits, but no event reads drunkard, flagellant, reclusive, irritable, lunatic or possessed. Congenital hooks are missing (beauty next to −50 attraction; clubfooted or hunchbacked for the Prosthetic). **Fix:** coping and lunatic options in the Flicker and Fracture pools, and congenital hooks in the Prosthetic and Training Yard.
10. **Pacing and AI cost at the top.** Augmented and Enhanced are fine at about 0.35–0.4 events a year. Overclocked runs about 1.5–2.5 a year with the Countdown, and Neurofractured plus its arcs about 2–3 a year. That suits a crisis, but there is **no AI throttle**, and under issue 3 most AI rulers roll these lists. Countdown stage 3 spans a 5-point band that accrual (12+) usually jumps. **Fix:** AI-only nothing-weights, and widen stage 3 to 68–76.

---

## 5. Earlier audit findings: status
**Fixed:**
- the free prisoner upgrade (now scaled cost);
- tier3.006.b / fracture.006.b "recovery" (now removes fear and unease and adds +15 reassured);
- tier3.006.a arrest (vanilla wrapper; double tyranny noted in M5);
- tier3.007.a mutual opinion;
- fracture.002.c (only this episode's flagged victims);
- named, weighted victims via the picker;
- `curious` removed;
- opinion durations;
- the B2 stress cliff (graded accrual, fixed threshold of 80);
- B1 Neurofractured drift;
- B3 regression gates;
- B4 cooldowns;
- B5 scaled gold;
- B6 lesson modifiers in place of permanent skill.

---

## 6. In-game checks (human, temporary map)
1. **A 50-year observer run.** Count augmented rulers by tier and the Overclocked, Neurofractured and cascade deaths. This settles issues 1–3.
2. **Containment Regency** on a healthy adult (025.a/.c/.e): still active after 2–3 months, with the swing held (M15 / Q7).
3. **heir.005:** who sees it when the player is the ruler (H3).
4. **The error log** after init.019.c and retinue.004.a with 1–2 knights (H4).
5. **Excision death:** no survival event follows (M2).
6. **The cascade year:** the next year's risk starts at 8, not 16+ (M1).
7. **Trait tooltip:** reads Augmented/Enhanced/Overclocked with the "Integration" bar. end.011 shows a whole number. The tier3.015 friend reason reads correctly.

## 7. Suggested order
1. **Scripter batch A:** H1–H4, M1–M3, M8–M10. Small, mechanical, and nothing here needs a design call.
2. **Localizer batch:** "pressure" → "static", the retitles, advisor/confessor, the wording fixes (§3.2), and the over-promising option text (§3.3), either reworded or handed to the scripter to make real.
3. **Architect calls,** then scripter: progression lever (issue 1), AI decision layer (2), AI throttle and Augmented cost (3, 10), the Seamless and Sedation balance (5), kinslayer policy (M4), imprisonment consistency (M5/M6).
4. **The observer run** (§6.1) before tuning any pacing numbers.
5. **Content passes:** Neurofractured agency (4), outcome rolls (6), thread links (8), coping and congenital hooks (9), the non-ruler rate (7).

The reviewers' analysis scripts (event graph, trait coverage, Monte-Carlo pacing) are in this session's scratchpad. The Tiger logs are `tiger2.log` / `tiger2_clean.log` there.
