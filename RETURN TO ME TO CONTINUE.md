# RETURN TO ME TO CONTINUE

Parked on 2026-10-20. When you come back, answer the decisions below (a word each is enough) and say "continue". I'll pick up from here.

Full report: [`docs/qa/system_investigation_2026-10-18/REPORT.md`](docs/qa/system_investigation_2026-10-18/REPORT.md). The taskboard entry is **CB-60** in `circlebackTaskboard.md`.

---

## Status 2026-10-20: picked up

**Owner rulings:**

| Item | Ruling |
|---|---|
| 1. Fix batch I1 | Go |
| 2. Kingpin under a Cartel (X2) | **Make it rarer** |
| 3. Feudal flag (P1) | **Keep distinct** |
| 4. Integrations | Alerts and encyclopedia pages first; memories and game rules specced |
| 5. Architect ruling pass | Go |
| Holding tiers | **Keep the brief, no D** (closed) |
| CB-59 | **Seamless text variants** for .001/.010/.020/.021/.037/.042 |
| CB-57 | **Accept all** (C1 building) |
| CB-58 | **Simple fabricators allowed** |
| CB-53 | **Build elective laws** |
| CB-52 | **Regained traits are surface** (closed) |

**DONE 2026-10-20 (all committed and pushed, QA and lore passed; nothing tested in game yet):**

| Item | Commits |
|---|---|
| Fix batches I1a and I1b | 170de01, 7866c66 |
| Design rulings I2a/I2b/I2d, CB-51 (both versions, gated), S11 | 99aea16 |
| I2 follow-ups (I2f) | 94c01af |
| I2c sponsorship lapse | 023492e |
| CB-59 Seamless variants and CB-58 printers | 7866c66 |
| Cartel G2 C1 to C5 | 9292c06, d7a052a, 95ea754, 34325c5; C5 full-system review DONE |
| Elective succession (CB-53) | e04660b |
| Region → **Shoal**, loc and vanilla UI | 2a6fad2, c2c947d |
| Region → Shoal, specs and test plan | 46fa4b8 |
| Integrations: Frontier alerts, encyclopedia, memories and game rules, cybernetics alert | 20ebad9, b8044c3, ccc5d69, ffe965e |
| Lint conventions for convention-named loc | 1876510, 0ecc292 |

**What's left waits on you:** the in-game test sitting.
- `docs/qa/IN_GAME_SESSION_PLAN.md`, which has the investigation checks;
- Cartel V-C1 to V-C20 and V-IR23;
- elective succession V-SU0 to V-SU14 (V-SU1: does a realm-law election work at all?);
- alerts 6a to 6f;
- memories and rules T-M and T-R;
- V-IR checks;
- markers CB-61.

**Optional:** paste the SIMPLE FABRICATION errata line into SETTING LORE. It is on the taskboard at CB-58, and now also allows weapons and hull plate.

## Where we stopped: the system investigation (2026-10-18)

Six read-only reviews found about **40 gaps**. None of them crashes the game or breaks an invariant.

**What is clean:**
- on_action layering is additive only.
- No system reads another system's variables by accident.
- No pulse loops over every character or county.
- Old saves stay safe.
- Where we differ from vanilla, it was deliberate and still holds. Example: Frontier is not a vanilla great project, because those are per province and DLC-gated.

### Bugs a play-test would hit (report §1, 18 mechanical fixes)

- **C1:** A ruler in an enemy dungeon still gets cybernetics events, including Court Massacre against their own court.
- **C2:** About 25 tier events fire 1 to 30 days after they're rolled and never re-check the tier. A ruler who just fell to Neurofractured can still get an Overclocked event.
- **S3:** The AI flips its augmentation law License ↔ Favor every 10 years and pays prestige each time. Each law scores 0 while it's held.
- **Smaller items:**
  - Unsworn placeholders get cybernetics liege events (X1).
  - A ruler-designer character may start without their government's succession law (X3).
  - A vassal's Frontier takes no war strain until occupied (F1).
  - A completed Frontier's new ruler ignores clergy-gender and realm gender laws (F3).
  - The kingpin story passes to a child heir (S5).

### Needs a design ruling (report §2, architect first)

- **S1 (the one HIGH):** The Ban doesn't cover retainer or knight installs, which is how the AI mostly augments. In practice the law barely does anything.
- **S2:** The court surgeon can operate on people who aren't at your court.
- **S4:** A liege can be handed a crime reason against someone they chose to augment.
- **F2:** A sponsor keeps paying for a Frontier after an enemy takes it.
- Smaller design notes (C3, C4, C6 to C10, S7 to S9, S13) are in the report.

### Vanilla integration (report §5, ranked)

1. **Top-bar alerts** for Frontier and augmentation opportunities. Cheap, no art.
2. **Encyclopedia pages** (game concepts) for Augmentation, Frontier, Unsworn and the four governments. Cheap, no art.
3. **Secrets and blackmail** for illegal augmentation. These would also fix S1 and S4 the vanilla way.
4. **Memories, game rules,** and later **men-at-arms, a clinic court amenity, Frontier legends.**

---

## Decisions I need from you

1. **Fix batch I1:** may I run the 18 report §1 fixes (mostly missing guards, plus rescoring the law AI) before your next in-game test session? *Recommended: yes.*
2. **Kingpin under the Cartel (X2):** the kingpin story has no government check. A Cartel ruler, who is the crime boss, gets "a criminal boss moves in", and once Cartel G2 lands its dread gains would feed tribute. **Block it, make it rarer, or accept it?** (It's also CB-57 question 8.)
3. **The feudal flag (P1):** our four governments drop vanilla's `government_is_feudal`, so about 370 vanilla checks for feudal rulers never see them. **Keep them distinct, or give some of them the flag?**
4. **Integrations:** which ones do you want? *Recommended: start with top-bar alerts and encyclopedia pages.*
5. **Architect ruling pass on report §2:** go ahead in parallel with the fix batch? *Recommended: yes.*

## Also waiting: holding tier progression (2026-10-20)

The verdict is in [`docs/proposals/holding_tier_progression_feasibility.md`](docs/proposals/holding_tier_progression_feasibility.md). It is feasible but not recommended as written:
- 3D holdings vanish at zoom step 9 of 35, so tiers can't read from far out.
- The proposal conflicts with the governing brief's rule of 7 meshes and no modelled tiers.
- It has several factual errors.

**Decisions:**
- **Keep the brief, or amend it?**
- **Test option D?** One file that keeps all markers visible further out.
- **If you want tiers:** option B, size-only tiers.

## Older decisions still open (the taskboard has details)

| Item | Question |
|---|---|
| CB-57 | The Cartel G2 design: 7 questions plus X2 above. Building waits on the answers. |
| CB-58 | Fabricators or printers at 866: keep the ban, or allow simple ones? |
| CB-59 | 6 decision-fired Frontier events still show first-person text to Seamless rulers: hide them, or give them Seamless text? Also confirm my .004/.005 ruling. |
| CB-53 | Government succession vs. the governments' fiction: rename the laws, or build elective laws? |
| CB-51, CB-52 | nr.004.e cover-up text; whether Seamless characters can regain personality traits. |

## In-game checks waiting on you

- **CB-44:** the test-session plan, `docs/qa/IN_GAME_SESSION_PLAN.md`.
- **CB-49:** the governments.
- **The Frontier checks:** `docs/specs/frontier_v5.md` §10.
- **T14:** gates Frontier batch 3, the Unsworn lobby block.
- **New from the investigation:** report §3. These get added to the session plan when we continue.
