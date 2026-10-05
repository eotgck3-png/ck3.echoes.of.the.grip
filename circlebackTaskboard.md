# Circleback Taskboard

Things we deliberately left for later. For each one, what it is waiting on, who can move it, and what to do when it is unblocked.

This board is **not** the gate board in `docs/agent_workflow.md` §6. The gate board tracks whole gates. This board tracks individual loose ends: decisions we deferred, checks we couldn't run yet, art we're waiting on, fixes parked until something else exists.

---

## How to use this file

**When to read it**
- Read it at the start of every session, after `CLAUDE.md`, before choosing work.
- Read it whenever a blocker clears (a map lands, art arrives, a decision is made). Search this file for that blocker's ID, e.g. `B-DESCRIPTOR`. Every item it was holding up is now workable.

**Who updates it**
- **The orchestrator** (the main Claude Code session) adds, updates and closes items, the same way it keeps the gate board.
- **Subagents** don't edit this file. If an agent defers something, it puts it in its HANDOFF block, and the orchestrator copies it here.
- **The human** can edit it freely: answer a decision inline, or mark something done.

**Adding an item**
1. Give it the next free ID in its section: `CB-<number>`. IDs are never reused.
2. Fill every field: what, why it's parked, blocked by, owner, next step, refs.
3. If the blocker is shared by several items, give it an entry in **Blockers** (`B-<NAME>`) and link to that, so it doesn't get repeated.

**Updating an item**
- Change the status and date. Don't delete history; add to it.
- If the next step changes, rewrite it. The next step must always describe the very next action, not the whole plan.

**Closing an item**
- Move it to **Done** at the bottom, add one line saying how it was resolved, and give the date.
- Close a blocker only when everything it was holding is either closed or re-blocked by something else.

**Status values**
- `blocked`: can't move until its blocker clears.
- `waiting-human`: needs a decision, art or an in-game check from you.
- `ready`: unblocked; any session can pick it up.
- `parked`: deliberately deferred by decision. Revisit at the trigger named in "next step".

**Owner values:** `human`, `orchestrator`, or an agent name (`eotg-scripter`, `eotg-localizer`, `eotg-architect`, `eotg-qa`, `eotg-lore-keeper`, `eotg-cartographer`). This is who acts next, not who wrote it.

---

## Blockers

These are shared conditions. Clearing one unblocks every item that names it.

| ID | Blocker | Clears when | Holding |
|---|---|---|---|
| ~~**B-DESCRIPTOR**~~ | **Cleared 2026-10-04** (39b8bda): `descriptor.mod` + `echoes_of_the_grip.mod` at the repo root, "Echoes of the Grip", 1.20.*, no `replace_path`. | — | — |
| **B-TEMPMAP** | **In progress 2026-10-04:** the test map is built as the sub-mod EotG Test Map (`docs/test_map/`, 06b1eb2). It still needs the human's `-mapeditor` heightmap pass (`docs/test_map/MAPEDITOR_STEPS.md`), then a first load. | Clears when the human reaches the 866 test bookmark with the map rendering. | CB-01, CB-02, CB-03, CB-20, CB-21 |
| **B-FAITHS** | No faiths or religions exist in v2 yet (Gate 1 / intake work). | Religions are lifted or built from the briefs. | CB-12 |
| **B-CULTURES** | No cultures exist in v2 yet. | Cultures are lifted or built from the briefs. | CB-17 |
| **B-ART** | Art is human-supplied. | You drop files in (e.g. `C:\Users\river\Downloads\assets`); the orchestrator converts them to vanilla formats. | CB-04, CB-05 |

---

## Testing and verification

### CB-01: Play-test cybernetics v2 in game
- **Status:** blocked (2026-10-03)
- **What:** all 33 in-game checks in `docs/qa/cybernetics_test_plan.md` §3. Static QA passed on every phase, but nothing has been played yet.
- **Blocked by:** B-DESCRIPTOR, B-TEMPMAP
- **Owner:** human (then eotg-qa triages anything found)
- **Next step:** load a save on the temporary map and work through §3 using the console toolkit in §2. Report failures with the event ID and a screenshot or error.log line.
- **Refs:** `docs/qa/cybernetics_test_plan.md`, `docs/specs/cybernetics_v2.md`

### CB-02: Q7, does Containment Regency persist?
- **Status:** blocked (2026-10-03)
- **What:** the vanilla `designate_diarch` + `try_start_diarchy = regency` path is built. It is unverified whether the engine ends a regency early when the liege is a capable adult. A fallback exists but is commented out: add vanilla `isolating_modifier` for the regency's duration.
- **Blocked by:** B-DESCRIPTOR, B-TEMPMAP
- **Owner:** human → eotg-scripter
- **Next step:** test plan item 11. If the regency ends early, have eotg-scripter uncomment the fallback in `eotg_aug_start_containment_regency_effect` (`common/scripted_effects/eotg_augmentation_effects.txt`).
- **Refs:** spec phase 3 §2, Q7 in `docs/specs/cybernetics_v2.md` §0

### CB-03: In-game checks from the earlier cybernetics passes
- **Status:** blocked (2026-10-03)
- **What:**
  - Confirm that the XP track levels **stack**: Augmented +2, Enhanced +4, Overclocked +8 prowess. Vanilla implies stacking, but the docs don't say it.
  - Confirm that no tooltip ever shows a fracture-risk number.
  - Confirm that error.log has no unset-scope or portrait errors from `eotg_` events.
- **Blocked by:** B-DESCRIPTOR, B-TEMPMAP
- **Owner:** human
- **Next step:** do these alongside CB-01, using `add_trait eotg_cybernetics` and then `effect add_trait_xp = { trait = eotg_cybernetics value = 50 }`.
- **Refs:** `docs/specs/cybernetics_track.md` §9

### CB-20: 50-year observer run (QA round 2)
- **Status:** blocked (2026-10-04)
- **What:** let the game run 50 years in observer mode on the temporary map. Count augmented rulers by tier, how many reach Overclocked and Neurofractured, and how many die in a cascade. This settles round 2's top design issues (progression speed, AI uptake, everyone stuck at Augmented) before any pacing number is tuned.
- **Blocked by:** B-DESCRIPTOR, B-TEMPMAP
- **Owner:** human → eotg-architect
- **Next step:** a logging sub-mod is built for this, in `docs/tools/observer/` (2026-10-04). Its build script writes the installable sub-mod outside the repo with `--out`. Follow its `README.md`:
  1. Create the main-mod launcher.
  2. Run `tools/build_observer.py`.
  3. Copy it into the CK3 mod folder.
  4. Launch with `-debug_mode`.
  5. Type `observe`, then run 50 years at speed 5. Do 3 seeds.
  6. Run `tools/parse_observer_log.py` on each `debug.log`.

  Judge the results against HQ2: 25–40% of AI count+ rulers augmented by year 30, and at least 15% of those at Overclocked or beyond. Hand the report to the architect. Ask the orchestrator to move the sub-mod somewhere permanent first if the scratchpad may be cleared.
- **Refs:** `docs/qa/cybernetics_qa_round2.md` §4.3, §6.1

### CB-21: QA round 2 in-game checks
- **Status:** blocked (2026-10-04)
- **What:** round 2 §6 items 2–7:
  - **Regency (M15):** the containment regency is still active after 2–3 months on a healthy adult.
  - **Heir event (H3):** who sees heir.005 after the restructure.
  - **Error log (H4):** no range error after init.019.c and retinue.004.a with 1–2 knights.
  - **Excision (M2):** an excision death gives no survival event.
  - **Cascade (M1):** next year's risk starts at about 8 after a cascade.
  - **Display:** the trait tooltip shows Augmented, Enhanced and Overclocked with the Integration bar, and end.011 shows a whole number.
- **Blocked by:** B-DESCRIPTOR, B-TEMPMAP
- **Owner:** human
- **Next step:** run these alongside CB-01.

### CB-23: Augmented landed barons get no yearly content
- **Status:** parked (2026-10-04)
- **What:** the ruler checks run for county tier and up, and the non-ruler checks for employed knights and courtiers. A landed baron fits neither, so an augmented baron never progresses or gets events. Not a bug, but a design gap.
- **Trigger to revisit:** if baron-tier play matters for the setting.
- **Owner:** eotg-architect

---

## Art

### CB-04: Seamless trait icon
- **Status:** waiting-human (2026-10-03)
- **What:** `gfx/interface/icons/traits/eotg_total_integration.dds`, for the Seamless (Total Integration) endgame trait. It's 120 × 120, uncompressed 32-bit with alpha, no mipmaps. No vanilla stand-in, because it would look like an existing trait. Tiger shows one expected `missing-file` warning until then.
- **Blocked by:** B-ART
- **Owner:** human
- **Next step:** supply a PNG. The orchestrator converts it, matching the other two trait icons, which have a textured backdrop. **Tone (2026-10-04):** match vanilla trait icons, e.g. blademaster: mean saturation ≈0.32 and brightness ≈0.33 over opaque pixels. The two shipped icons were toned down to this in 43ec7d7, and new icons get the same treatment on conversion. **Size:** the teal backdrop square is 92 px at x 14–105, y 15–106 on the 120 px canvas, matching blademaster (fc86da0).
- **Refs:** test plan §5

### CB-05: Nine placeholder decision illustrations
- **Status:** waiting-human (2026-10-03), optional
- **What:** these decisions use existing art, marked `PLACEHOLDER` in `common/decisions/eotg_augmentation_decisions.txt`: Seek Augmentation, Remove Implants, Consult a Physician, Augment a Courtier, Accept Restraints, Begin a Sedation Regimen, Appoint a Warden, Hand Over the Controls, Cut It Out. They're 1100 × 440 and stored as DXT1.
- **Blocked by:** B-ART
- **Owner:** human
- **Next step:** the test plan §5 lists a suggested subject for each. When art arrives, the orchestrator converts it, and eotg-scripter swaps the `reference` and removes the `PLACEHOLDER` comment.
- **Refs:** test plan §5

---

## Decisions for the human

### CB-28: Open Helix questions (follow-up to the CB-06 ruling)
- **Status:** waiting-human (2026-10-04)
- **What:** the ruling is in SETTING LORE's ERRATA: a remnant that is active and growing, holding 3 counties in different duchies. These points are still open:
  1. Which duchies or region? The never-applied v1 draft `title_hierarchy.md:163-185, 251-257` gives Helix whole duchies. **The cartographer must not lift it as written.**
  2. Is any of the 3 counties on or near Xerxes? (Clayd's arc is "The Ghosts Beneath Xerxes".)
  3. Its government type. v1 had a corporation government.
  4. Who leads it? Does Clayd Kestrel-Vire hold all 3 counties, or do vassals or rivals hold some?
  5. Are the Pale Hand ties still only suspected? The lore-keeper reads it that way.
- **Settled:** the cybernetics syndicate stays unnamed, under the map-agnostic rule and `cybernetics_v2.md:227`. Once a Helix title exists, the human could choose a gated "Helix envoy" variant; that would be new content.
- **Owner:** human → intake (vault questions) → eotg-cartographer
- **Next step:** answer here or in the Helix region brief.

### CB-32: Canon rulings from the docs/lore review
- **Status:** waiting-human (2026-10-04)
- **What:** the precedence ruling and errata are done (2026-10-04): docs/lore's dated entries win, Yu is freed, and LAW AT 866 is pasted. That resolved most of the 16 contradictions. Seven small points remain, where the sources are silent or disagree with each other. They're listed in `docs/lore/REVIEW_866.md` under "Still open".
- **Owner:** human
- **Next step:** settled 2026-10-04 except the Vaelorin/Xerxes question (see `docs/lore/REVIEW_866.md`). Answer that one when convenient.

### CB-08: Glossary ruling on medieval game terms
- **Status:** waiting-human (2026-10-03)
- **What:** cybernetics text uses vanilla UI terms: court, courtier, vassal, knight, household, gold, liege. The interim ruling keeps terms that match the game UI the player sees. A real decision would go in the reflavor glossary and `localization/english/replace/`.
- **Owner:** human → eotg-localizer
- **Next step:** decide which terms get renamed (e.g. knight → ?, gold → ?). If any are renamed, the localizer updates the glossary and the `replace/` layer, and greps the cybernetics loc for them.
- **Refs:** `OLD PROJECT VERSION/docs/localization_crusade.md`

## Parked until something else exists

### CB-10: v1 systems still on the dead yearly hook
- **Status:** parked (2026-10-02)
- **What:** v1's `eotg_legacy_on_actions.txt` and the hub `eotg_on_actions.txt` (government flavor) extend `on_yearly_playable`. That name only appears in vanilla `.info` prose; the real hook is `yearly_playable_pulse`. None of those v1 events ever fired.
- **Trigger to revisit:** when Confluence Legacies or the government flavor are lifted (Gate 2/3).
- **Owner:** eotg-scripter (at lift time)
- **Next step:** rewire to `yearly_playable_pulse`. `python docs/tools/px_vocab_check.py` flags the dead hook automatically.
- **Refs:** `OLD VERSION CATALOG.md` §4 lesson 13, `docs/pitfalls.md` §12

### CB-11: Void Corruption system, not yet lifted
- **Status:** parked (2026-10-03)
- **What:** the v1 Void system is next in line for a lift (catalog §5). It must stay distinct from cybernetics: the Void is external and heard at the edge of hearing, while the cybernetic voice is internal. Both systems can sit on one character, so their text must never blur.
- **Trigger to revisit:** when the human picks the next system.
- **Owner:** eotg-scripter + eotg-localizer, then eotg-lore-keeper
- **Next step:** Pipeline B lift. Rewire its hook (CB-10 applies), and run the PX tools and Tiger.
- **Refs:** catalog §2.3, memory "Void Corruption system"

### CB-12: Zealous vs Industrial Survivalism
- **Status:** blocked (2026-10-03)
- **What:** zealous characters are scripted to dislike implants: the stress helpers, A Tithe for Purity, the refusal options. Canon faith Industrial Survivalism holds machinery sacred (`866_religions:227-233`), so a zealous Creedwright reacts backwards. Kept faith-neutral for now; a gate based on faith doctrine is deferred.
- **Blocked by:** B-FAITHS
- **Owner:** eotg-architect → eotg-scripter
- **Next step:** once faiths exist, the architect designs a doctrine or tenet check (not a hard-coded faith key) that inverts the zealous reactions for machine-sacred faiths.
- **Refs:** `docs/specs/cybernetics_v2.md` §10 deferrals

### CB-13: Deferred cybernetics features
- **Status:** parked (2026-10-03)
- **What:** these were decided as out of scope for v2.
  - **The Clinic arc** (Q10): building-adjacent, so it waits for building gates.
  - **A qualitative hint of the hidden risk** for the player, e.g. a trait-desc line. The Countdown story carries this narratively for now.
  - **Visible story-cycle panels**, which would need art.
  - **3 track icons instead of 1.** The engine can switch a trait's icon by XP level (vanilla `tourney_participant`).
- **Trigger to revisit:** after the CB-01 play-test shows whether players can read the system.
- **Owner:** human (scope call) → eotg-architect
- **Refs:** `docs/specs/cybernetics_v2.md` §10, `docs/specs/cybernetics_track.md` §10

### CB-14: Event ideas raised by QA (your call; not built)
- **Status:** waiting-human (2026-10-03)
- **What:** expanding events beyond an approved proposal is the human's call. QA suggested:
  - A Patron beat for an owner who has had the implants removed ("the syndicate still holds the paper").
  - A Retinue knight-cascade beat linking the Iron Retinue to The Broken Champion.
  - A "declined" follow-up for offers you keep refusing (The Prosthetic, The Neural Bridge).
  - A follow-up when a chosen retainer resents being augmented (init.020).
  - Event beats for the two regression decisions, which today are decision-only.
- **Owner:** human
- **Next step:** say which (if any) to build. The architect specs them, then the usual pipeline runs.

### CB-15: Small script loose ends
- **Status:** parked (2026-10-03)
- **What:**
  - `eotg_flag_aug_containment_regency` is set and cleared but never read.
  - `eotg_flag_aug_trusted_delegate` (Phase 4) isn't wired into Containment Regency as an optional bonus.
  - `eotg_flag_aug_trusted_delegate` shows as "set but never used" in error.log. Keep it: it's a reserved optional read (phase4 spec ~l.429). The warning is expected until it's wired in.
  - Pre-v2 events use unprefixed saved-scope names (`aug_peer`, `aug_spouse`, `concerned_vassal`, `confessor`, `other_machine`, `petitioning_knight`, `watching_heir`). These are event-local, not global, so it's cosmetic.
- **Trigger to revisit:** the next time those events are edited.
- **Owner:** eotg-scripter

### CB-17: Culture reactions to augmentation
- **Status:** blocked (2026-10-03)
- **What:** v1's design had per-culture reactions to augmented rulers. They were deferred because they would reference culture keys, which breaks the temporary-map rule.
- **Blocked by:** B-CULTURES (and the real map)
- **Owner:** eotg-architect
- **Next step:** spec it using culture traditions or pillars rather than hard-coded culture keys, if possible.

---

### CB-31: In-game checks for the 2026-10-04 cybernetics batch (eca9b9c)
- **Status:** waiting-human (2026-10-04)
- **What:** these were found or fixed after the human's play-test screenshots, and need confirming in game:
  1. Decision-list hovers read as plain text: Remove Implants, Maintenance, Consult Physician.
  2. Seek Augmentation:
     - requirement lines are ticked text, with no raw flag names;
     - no "You lose…" lines;
     - the physician line appears only when you have a physician.
  3. init.018 *The Offer You Sought*: the syndicate paragraph and option e's tooltip appear only when you have no Patron.
  4. Pursue: the requirement lines read correctly, and only synergy modifiers you hold are listed.
  5. Maintenance and Consult Physician: "the static quiets" shows only at Overclocked, and "lose" lines only for modifiers you hold.
  6. Remove Implants and Excision list only modifiers you hold. The throttle shows only if you are throttled.
  7. Total Integration lists only the traits you actually have.
  8. fracture.006.b and tier3.006 show no opinion-removal lines when nothing is held.
  9. The 9 new `.tt` option tooltips show their text.
  10. tier2.011.c's success shows "Trimmed Levy Plan" (+5% tax, no opinion change).
  11. fracture.018.a's toast names the forgotten person.
  12. fracture.020: sparing a real traitor shows `desc_true_spared` and "It was right. I was not.", with no prestige.
  13. The trait's Integration line is on its own paragraph, and (1) and (2) match the track.
  14. Patron with the envoy absent:
      - .006 shows the `_absent` text, with no portrait and no options c or e;
      - when d fails, nobody dies; an augmented owner gets the throttle and the risk.
  15. Patron with the envoy present:
      - options c and e kill the envoy;
      - at demand 2, if the envoy is the only possible critic, .005 fires instead.
  16. error.log is clean after a few story ticks.
- **Owner:** human → orchestrator (route failures to the Cybernetics session)
- **Next step:** play-check during normal testing. Screenshots are enough.

### CB-33: Vanilla scheme agent names and generic scheme loc are medieval
- **Status:** parked (2026-10-04)
- **What:** the Tamper scheme (interactions spec) reuses vanilla agent roles, which show as "Physic", "Smith", "Footpad" and so on in the agent slots. It also reuses the generic `intrigue_scheme_ongoing.1001` ("servant…", "a few coins…"). This affects every scheme in the mod, not only Tamper.
- **Trigger to revisit:** the vanilla reflavor / `replace/` pass (CB-08 glossary).
- **Owner:** eotg-localizer
- **Next step:** reflavor them through `localization/english/replace/` (e.g. Technician, Fitter, Sneak) when the glossary is decided.

### CB-34: In-game checks for G9 (7d79ff2) and the new beats (db0c550)
- **Status:** waiting-human (2026-10-04)
- **What, G9 trait depth:**
  1. Each of the 8 trait options shows with its trait icon. Use console `add_trait`, then fire the host event.
  2. tier2.004.e: Reassured or Unease depending on whether the spouse is chaste, and .017 follows 180–365 days later.
  3. tier3.010.f: Dulled Senses for 2 years.
  4. tier3.021.d: Falsely Accused, +10 dread, and one arbitrary stress line.
  5. nr.004.f: the champion is Reassured, and a victim gets Disgust only if one exists.
  6. The helper rows appear: impatient, gluttonous and temperate on reject options; fickle on neglect options.
  7. Three gated options showing at once don't overflow the window.
- **What, new beats:**
  1. Round 2: after a round-1 kill, heir.007 shows desc_executed with the dead predecessor's portrait, and option a is gendered.
  2. Round-2 heir.003 and heir.004 show desc_successor. The story ends after round 2's heir.004, and there is no third heir.007.
  3. patron.008 fires once after full removal; options a and b behave as specced.
  4. Once per life: no second patron.001 for 10+ years after settling, and init.018 shows no syndicate line or option e.
  5. The throttle tooltip shows after a betrayal.
  6. Opinion names in the breakdown, including the ruler's own opinion of another Overclocked character after tier3.007.a ("Admiration").
  7. Gendered pronouns read right with a female and a male champion and heir.
- **Owner:** human → orchestrator
- **Next step:** check alongside CB-31 during normal play.

### CB-35: In-game checks for the Procedures batch (G2/G3)
- **Status:** waiting-human (2026-10-04)
- **What:** `docs/specs/cybernetics_v2_procedures.md` §9 item 11 is the full list (Seek and Clinic rolls, Pursue g/f, Remove Implants → proc.001/.002, injuries → proc.003/.004, proc.020, Seamless Ledger/Resignation/Flicker). Also check:
  1. The end.041 resigner is never the spouse or close family, and the end.041.c toast shows.
  2. A booked removal blocks a second booking. The decisions show "No procedure is already booked".
  3. A ruler who is their own physician gets no option b in proc.001/.003, only e (self).
  4. **Engine Q1:** does a wound pushed to rank 3 by `increase_wounds_no_death_effect` fire `on_trait_gained` for `wounded_3`? If not, proc.003 misses wound-ranked injuries. Report to the scripter.
  5. **Engine Q2:** starting characters with a listed trait get no proc.003 on day 1. Deferred until `history/` exists.
- **Owner:** human → orchestrator
- **Next step:** check alongside CB-31 and CB-34.

### CB-36: Self-repair innovation era depends on Gate 1 culture eras
- **Status:** blocked (2026-10-04)
- **What:** the self-repairing machinery innovation (`docs/specs/cybernetics_v2_self_repair.md` §4.1) sits one era above whatever era the mod's own cultures hold at 866. Vanilla cultures are tribal at 867 (so early medieval for testing). When Gate 1 sets the mod's culture eras, the innovation's era must move to match.
- **Blocked by:** B-CULTURES
- **Owner:** eotg-architect → eotg-scripter
- **Next step:** when cultures exist, re-place the innovation per the §4.1 rule.

### CB-37: Frontier Systems Phase 1: in-game test
- **Status:** waiting-human (2026-10-04)
- **What:** merged in ef514e8 after three local verification passes (`docs/specs/frontier_v1_verification.md`). The in-game plan is `docs/specs/frontier_v1_test_plan.md`. **Run section 0 first** (V1 county-variable persistence, V8 holding in an empty slot, V12 saved scopes reaching the hooks). It works on the vanilla map via the debug decisions, or on the test map (24 counties with empty slots; see docs/test_map/README.md).
- **Owner:** human -> orchestrator (route failures to the cloud agent)
- **Next step:** after section 0 passes, run the rest of the plan. Phase 2 content is the owner's call.

### CB-38: In-game checks for the Interactions batch (G4/G5/G8)
- **Status:** waiting-human (2026-10-04)
- **What:** `docs/specs/cybernetics_v2_interactions.md` §9 item 12 is the full list: Offer, Demand, Examine, Tamper (each agent package, execute, discovery, invalidation) and Salvage (rough ×20, physician, kin death → kinslayer, the prisoner stays imprisoned, int.002 a/b/c). Also check:
  1. **Engine (a):** the Tamper preparations window (`scheme_critical_moments.0002`) opens at phase completion, and "execute" fires tamper.001. Vanilla settles this on paper (steal_back_artifact).
  2. **Engine (b):** int.002's outcome lines match what actually happened on the table (`scope:eotg_proc_outcome` saved inside `hidden_effect`).
  3. Ticking two providers on Offer or Demand disables the send button.
  4. A back-street fault repair that comes out maimed leaves the fault in place: Examine still shows desc_tampered.
  5. **Engine (c):** does the AI use the interactions? Read section [13] of the observer report (rebuild the sub-mod first; it now overlays 6 files). This feeds into CB-20.
- **Art debt:** 6 placeholder interaction/scheme icons (Examine uses `plague`).
- **Later (not blocking):** fault repairs and injury repairs share the variable `eotg_aug_repair_injury`. If an injury lands during a pending fault repair, the reveal repairs the injury instead of the fault.
- **Owner:** human → orchestrator
- **Next step:** check alongside CB-31, CB-34 and CB-35.

### CB-39: In-game checks for the Realm batch (G7/G10/G6)
- **Status:** waiting-human (2026-10-04)
- **What:** `docs/specs/cybernetics_v2_realm.md` §9 item 12 is the full list:
  - **the law:** shows in My Realm, its cost and cooldown, the vassal lock, inheritance, and reverting to Tolerated;
  - **a Ban:** clinics closed, discovery leading to realm.001, the Demand crime line and "Refused a Lawful Order";
  - **the Implant Technician:** hire, the "My implant technician." option, cheaper Maintenance, and invalidation under a vassal's Ban;
  - **Borrow Their Technician;**
  - **activities act.001–.006:** tournaments need Tours & Tournaments; pilgrimages need holy sites.

  Also check:
  1. **Engine (h):** under a Ban, Offer and Demand open with no provider preselected and the clinic option shown as unavailable.
  2. **Engine (a):** the child `on_actions` under vanilla activity hooks fire, and the parent's trigger gates them.
  3. **Engine (c):** the second `realm_law` group renders in My Realm alongside Crown Authority.
  4. **Engine (g):** an unlanded courtier reads their employer's law through `top_liege`.
  5. **Observer:** read report section [14] for HQ2. Rebuild the sub-mod first; it now has the realm counters.
- **Tiger:** 1.17 reports about 68 errors on the 1.20 law split (`law_group_type`, "law not defined"). QA matched the shape to vanilla 1.20 `00_realm_law_groups.txt` / `00_realm_laws.txt`, so treat these as noise until a 1.20-aware Tiger exists (CB-18).
- **Art debt:** 4 law icons, the Implant Technician court-position icon, and the Borrow interaction icon (placeholder `plague`).
- **Notes (not blocking):**
  - Self-surgery under a Ban has no discovery chance.
  - A Seamless liege's AI never hires a technician.
  - Borrow's AI only targets war allies.
- **Owner:** human → orchestrator
- **Next step:** check alongside CB-38.

### CB-40: In-game checks for the Reprisal batch (the paper is sold)
- **Status:** waiting-human (2026-10-04)
- **What:** `docs/specs/cybernetics_v2_reprisal.md` §9 item 9 is the full list:
  - **case a:** envoy murdered → .009 with desc_envoy_dead;
  - **case b:** .006 f with the throttle for an augmented owner; .006 f then .009 for an owner with no implants;
  - **case c:** a deceitful owner's d fails;
  - **.009 c:** back at tier 1, with no lien;
  - **.009 d:** the murder scheme shows in the scheme list or console, and vanilla discovery names the collector;
  - **.009 e:** the collector becomes a prisoner, with the tyranny tooltip; on failure, the collector stays as a guest who owns the scheme.

  Also check:
  1. **Engine (a):** does a guest created by `create_character` + `add_visiting_courtier` actually progress and execute the murder scheme? Vanilla `allow`/`valid` permit it on paper.
  2. **Engine (b):** can the `remove_short_term_gold` fallback take a ruler into debt?
  3. **Observer:** read report section [15]. Rebuild the sub-mod first; it now has 7 overlays.
- **Known deferral (spec §10):** .009 c, like patron.008 c, ignores a realm Ban.
- **Owner:** human → orchestrator
- **Next step:** check alongside CB-38 and CB-39.

### CB-41: In-game checks for the Self-repair batch
- **Status:** waiting-human (2026-10-04)
- **What:** `docs/specs/cybernetics_v2_self_repair.md` §9 item 9 is the full list:
  - the culture window shows Self-Repairing Machinery (civic group, early medieval column);
  - a tribal culture can pick it as an ahead-of-time fascination (note the rate shown in the UI);
  - after granting it by console, the decision appears for tiers 1–3 only and disappears once fitted;
  - the clinic, physician and "My implant technician." routes all work;
  - the clinic is greyed out under a Ban;
  - calibration lasts 5 years after Maintenance and 7 years after Consult;
  - Overclocked accrual is 11 / 8 / 5 depending on how much is stacked;
  - the modifier is removed on a full exit and at Total Integration.

  Also check:
  1. **Engine (a):** how fast the ahead-of-time research actually goes. The defines say it is allowed: ÷5 per era behind, and halved for each ahead-of-time innovation already held.
  2. **Engine (d):** tribal rulers on the test map can still use it. The early medieval era is invalid for tribal governments, but that only limits engine-applied innovation effects, and this innovation has none.
  3. **Observer:** read report section [16]. Rebuild the sub-mod first.
- **Art debt:** the innovation icon, the modifier icon and the decision picture are stopgaps.
- **Note:** a refit roll uses up the sabotage flag, as every roll does, so it lifts a tampering's ×1.5 penalty. The Tampered modifier stays.
- **Related:** CB-36 (move the innovation's era at Gate 1; S5: nothing in history or bookmarks may grant it).
- **Owner:** human → orchestrator
- **Next step:** check alongside CB-38 to CB-40.

## Tooling and environment

### CB-18: Game is 1.20.0.3; the tools target older versions
- **Status:** waiting-human (2026-10-03)
- **What:**
  - **Tiger** 1.17 targets 1.18.3. It reports 1.20 tokens inside vanilla `20_health_effects.txt` as errors (known-benign, documented in `CLAUDE.md`).
  - **PX Toolkit's** bundled `script_docs` engine dump is also older than 1.20.
  - **`CLAUDE.md`** still says "CK3 1.19" in places.
- **Owner:** human (download or run in game) → orchestrator
- **Next step:**
  1. Check for a newer ck3-tiger release that targets 1.20, and update the path in `CLAUDE.md`.
  2. In game, run the console command `script_docs` (and `DumpDataTypes`) to generate a 1.20 dump. Point PX at it with the `px.logsPath` setting, and update `docs/tools/px_vocab_check.py` to read it.
  3. The orchestrator then updates the version references in `CLAUDE.md`.

### CB-19: Space-map defines file has no BOM
- **Status:** waiting-human (2026-10-03)
- **What:** PX's language server flags `common/defines/eotg_space_map_defines.txt` as not UTF-8 with BOM. Vanilla defines files have a BOM. It's your space-map work, so it was left untouched.
- **Owner:** human (or say "fix it")
- **Next step:** re-save it as UTF-8 with BOM. The orchestrator can do this on request; the content doesn't change.

---

## Done

| ID | Item | Resolved | Date |
|---|---|---|---|
| CB-25 | Loc broken by the scope rename | Fixed by the localizer in the round-2 pass. The 10 strings now use `eotg_aug_spouse` / `eotg_other_machine`, and the 3 missing keys (`eotg_fracture.011.f`, `.020.d`, `eotg_aug_tier3.014.a.tt`) were added. QA confirmed 0 missing loc and no `unknown datafunction` | 2026-10-04 |
| CB-22 | Balance amendment, from QA round 2's design issues | Built and QA-passed: Parts B1 and B2 (`docs/specs/cybernetics_v2_balance.md`) and the round-2 bug and text fixes. Further pacing tuning waits for CB-20, and then touches only the script values, the AI weights and `ai_will_do` | 2026-10-04 |
| — | Q8: build The Sickly Child (child augmentation) | Human accepted all v2 recommendations; lore-keeper confirmed the drafted tone | 2026-10-03 |
| — | Cybernetics trait icons, 3 decision pictures, 4 modifier icons | Delivered and converted to vanilla formats | 2026-10-03 |
| CB-06 | Helix at 866 AG | Ruling: a remnant that is active and growing, with 3 counties in different duchies. Lore-keeper ERRATA pasted into SETTING LORE. Open points are in CB-28 | 2026-10-04 |
| CB-07 | Cybernetic voice errata | Approved by the human, pasted into SETTING LORE | 2026-10-04 |
| CB-09 | Commit the cybernetics work | 2e6cef2 (round 2 + balance B1/B2), pushed | 2026-10-04 |
| CB-30 | Marker model questions | Human: keep the 7 colours for now (placeholders); every model sits on the shared plinth; leave the `map-presentation-good` tag at 69b1f5f | 2026-10-04 |
| CB-29 | Junction the game's mod folder to the repo | `mod/eotg_stellar_rivers` is now a junction to the repo. The launcher file `eotg_stellar_rivers.mod` was renamed to "Echoes of the Grip" (Total Conversion, 1.20.*). Old folder kept as `mod/eotg_stellar_rivers_backup_20261004` (with the old `.mod` as `.mod.bak`); delete it once the game is confirmed loading. Before switching, a full diff showed: 4 settings files differed only by a BOM (kept the repo versions, which match vanilla); the lane ramp and the table_styles BOM were committed; 12 gitignored generated textures (colormap, 5 holding decals, 6 structure textures, the newer 10-01 bakes) were copied into the working tree. **Uncommitted working-tree edits are now live in game.** | 2026-10-04 |
| CB-26 | Architect rulings on the conformance audit | `docs/specs/cybernetics_v2_conformance_rulings.md` (d223f1a); work items W1–W6 built in eca9b9c | 2026-10-04 |
| CB-27 | Conformance bug fixes M7/M8 | Built and QA-passed, eca9b9c; in-game checks in CB-31 | 2026-10-04 |
| CB-16 | Superseded notes on the 4 pre-v2 cybernetics QA docs | Done by cloud session (CB-24) | 2026-10-04 |
| CB-24 | Cloud conformance audit | Merged from `claude/focused-dirac-ixo81h`. Verified locally: 12/12 MEDIUM confirmed and 5 vanilla claims settled (report §6). Follow-ups are CB-25 to CB-27. | 2026-10-04 |
