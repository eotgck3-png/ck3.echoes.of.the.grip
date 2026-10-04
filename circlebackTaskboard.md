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
| **B-DESCRIPTOR** | No mod descriptor (`descriptor.mod` + `echoes_of_the_grip.mod`) at the repo root, the Gate 0 item. The launcher can't load the mod; Tiger only runs with a scratch descriptor. | The cartographer writes both files. Per `CLAUDE.md`, `replace_path` only for folders the mod actually ships. | CB-01, CB-02, CB-03 |
| **B-TEMPMAP** | The temporary map isn't in yet. Systems are map-agnostic, but in-game tests need rulers, courts and conditions to exist. | The human brings it in. Check `docs/qa/cybernetics_test_plan.md` §1c against it, especially **capital county development 10+**. | CB-01, CB-02, CB-03 |
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
- **Next step:** a logging sub-mod is built for this (2026-10-04), kept outside the repo in this session's scratchpad: `eotg_observer_submod/`. Follow its `README.md`:
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
- **Next step:** supply a PNG. The orchestrator converts it, matching the other two trait icons, which have a textured backdrop.
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

### CB-06: Helix Corporation at 866 AG, active or remnant?
- **Status:** waiting-human (2026-10-03)
- **What:** canon contradicts itself. `SETTING LORE:302-306` says it's "active and growing"; `Bookmark-Characters:51`, `EOTG_Events_Characters:593` and `866_religions:232` say it's a remnant. Until you rule, the cybernetics syndicate stays unnamed.
- **Owner:** human → eotg-lore-keeper
- **Next step:** pick one. The lore-keeper's two drafted ERRATA texts (one for remnant, one for "active but splintered") are in its first cybernetics review. Ask the orchestrator to reproduce them. Then paste the chosen one into the ERRATA block of `OLD PROJECT VERSION/docs/SETTING LORE`.
- **Refs:** lore-keeper reviews, 2026-10-02/03

### CB-07: The cybernetic "voice" errata
- **Status:** waiting-human (2026-10-03)
- **What:** add a canon note that the implant's "voice" is technological (the implant's predictive model of its user) and has no connection to the Void, Orrin or Kyros. The rule already binds all text through `docs/specs/cybernetics_v2.md` §5; this would put it in canon too.
- **Owner:** human
- **Next step:** approve, then paste into SETTING LORE's ERRATA block. Draft text:
  ```
  - CYBERNETIC "VOICE" (2026-10-03): Deeply integrated augmentation users
    report a second perspective — the implant's predictive model of its user,
    running ahead of them. It is TECHNOLOGICAL. It has no connection to the
    Void, Orrin, Kyros, or any planar entity, and in-world text never frames it
    as possession, a pact, or a whisper. It is not what "speaks from the empty
    Void"; that remains unexplained.
  ```

### CB-08: Glossary ruling on medieval game terms
- **Status:** waiting-human (2026-10-03)
- **What:** cybernetics text uses vanilla UI terms: court, courtier, vassal, knight, household, gold, liege. The interim ruling keeps terms that match the game UI the player sees. A real decision would go in the reflavor glossary and `localization/english/replace/`.
- **Owner:** human → eotg-localizer
- **Next step:** decide which terms get renamed (e.g. knight → ?, gold → ?). If any are renamed, the localizer updates the glossary and the `replace/` layer, and greps the cybernetics loc for them.
- **Refs:** `OLD PROJECT VERSION/docs/localization_crusade.md`

### CB-09: Commit the cybernetics work
- **Status:** waiting-human (2026-10-03)
- **What:** none of the cybernetics work is committed: v1 lift, track conversion, art, v2 Phases 0–6, the PX tools, and the docs. It sits in the working tree alongside your uncommitted map and marker changes, so it needs a selective commit.
- **Owner:** human → orchestrator
- **Next step:** say "commit cybernetics". The orchestrator stages only the cybernetics paths:
  - `common/*/eotg_augmentation_*`, `common/story_cycles/`, `common/deathreasons/`, `common/scripted_character_templates/`
  - `events/eotg_augmentation_*`, `localization/`
  - `gfx/interface/icons/{traits,modifiers}/eotg_*`, `gfx/interface/illustrations/decisions/eotg_*`
  - `docs/specs/cybernetics_*`, `docs/qa/`
  - `docs/tools/px_*`, this file, and the `CLAUDE.md`, `agent_workflow.md` and catalog edits
  
  It leaves your map, marker and shader files unstaged.

---

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

### CB-26: Architect: ratify or reject the conformance deviations
- **Status:** ready (2026-10-04)
- **What:** the conformance report, `docs/qa/cybernetics_spec_conformance_cloud.md`, covers M1–M6, M9–M12, L1, L4, L6–L12, L14–L24 and S1–S19. Most are commented "final QA" or "orchestrator ruling" deviations that were never written back into the specs. Also: titles retitled in 5a97355 (init.002, init.005, tier2.005, fracture.024) now drift from the spec names.
- **Owner:** eotg-architect
- **Next step:** one pass. CB-22 has settled (2026-10-04), so this can be dispatched as soon as the round-2 and balance work is committed. Until then the two would touch the same files. Read §6 first: L3 is moot, and the line numbers are stale.

### CB-27: Scripter: conformance bug fixes
- **Status:** blocked on CB-26 for M1 and M2 (2026-10-04); M7 and M8 are ready once the round-2 edits land
- **What:**
  - **M8:** exclude the patron envoy from `eotg_aug_patron_critic_candidate` and the patron.004 pick.
  - **M7:** guard patron.006's portrait and descs against a dead envoy, and decide what happens to an envoy who has left court.
  - **After rulings:** M1 (penalty text vs modifier), M2, M10, L2, L5 and L13.
- **Owner:** eotg-scripter (eotg-localizer for any text)
- **Next step:** dispatch after the round-2 session commits, to avoid edit collisions.

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
| CB-16 | Superseded notes on the 4 pre-v2 cybernetics QA docs | Done by cloud session (CB-24) | 2026-10-04 |
| CB-24 | Cloud conformance audit | Merged from `claude/focused-dirac-ixo81h`. Verified locally: 12/12 MEDIUM confirmed and 5 vanilla claims settled (report §6). Follow-ups are CB-25 to CB-27. | 2026-10-04 |
