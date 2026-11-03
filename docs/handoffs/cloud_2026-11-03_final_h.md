# Handoff: final queue H (cloud, 2026-11-03)

Branch `claude/final-h-cloud`: cut from origin/claude/void-corruption-v2-cloud (e02389d), merged origin/claude/mechanics-sim-cloud (f602a72); origin/v2-space-map (4a6191e) was already contained. No game script or loc in the main mod was changed.

## H1: test-harness cases for the G2 governments and the Void

### HANDOFF (cloud session, unvalidated)
- branch: `claude/final-h-cloud`
- status: done
- summary: 16 new harness decisions and 25 hidden events in `docs/tools/gen_test_harness.py` (39 tests, 49 events in all), regenerated into `docs/test_submods/test_harness/`; README test list updated with spec ids.
  - G2: GP1/GC1/GT1 (writer → story counter, modifier re-applied, clamp; V-P2/3, V-CO2/3, V-TO2/3).
  - GP2: battle feed values +2/−3 (V-P6; the hook itself is a LOOK).
  - GC2a/GC2b → GC2c: Court the Board bracket (V-CO8 and the erosion fix, including the already-eroded guard path).
  - GT2a → GT2b: Corner the Market bracket (V-TO7, including the once-a-year guard on a pre-marked Prince).
  - GE1/GE2: election band edges as LOOK (V-CO13, V-TO13).
  - Void: VD1 exposure bands (V-V3), VD2 the Hollowing through the real yearly pulse with the cooldown set by the on_action (V-V8, V-V17), VD3 depth bands and the +4 drift (V-V9–V-V12), VD4 the Voidwalker courtier, −6 accrual and the Ward decision (V-V13), VD5 the Insight guard (V-V16).
  - Lessons followed: nothing kills or deposes (VD2 warns that 0030.c steps down; the player chooses), every unmet setup logs SKIP, each PASS reads something downstream of the setup (story counter, band modifiers, accrual value, decision availability) or is a LOOK, baselines read first with exact deltas, every `eotg_test_*` variable cleared in the final step. **Correction (local validation, 2026-11-03):** not everything is restored. GP1/GC1/GT1, GP2, GE1/GE2, VD1 and VD3 restore their value; VD2 leaves the ruler Hollowed, VD4 leaves a Voidwalker at court, VD5 leaves +4 skill and an Insight modifier, and GC2b / GT2a leave the real 1-year guards (`eotg_corp_board_eroded` on the liege, `eotg_gobcorp_cornered` on a Prince). `docs/qa/TEST_HARNESS.md` now lists what each test leaves and a suggested order; use a throwaway save.
  - Local fixes (eotg-scripter, 2026-11-03, after eotg-qa): VD5.1 compared two `{ }` blocks (a parse error; now stored in `eotg_test_after` first); VD2 SKIPs when a Voidwalker is at court (VD4 leaves one, which made VD2.1 a false pass); GT2B.2/.3 FAIL lines carry their sub-step numbers.
- files: `docs/tools/gen_test_harness.py`; `docs/test_submods/test_harness/**` (regenerated, byte-stable on a second run); `docs/qa/TEST_HARNESS.md`; this handoff.
- unverified-vanilla:
  - `gen_test_harness.py` GC2a/GT2a: `is_decision_on_cooldown = <decision>` as a character trigger.
  - VD3: `has_opinion_modifier = { modifier target }`.
  - VD5 and the existing CY1: skills read as values (`value = diplomacy add = martial …`).
  - VD4: `can_execute_decision` for a decision with a gold cost (AL4 uses it already).
  - All tests: `save_scope_value_as` with a `{ value subtract }` block passed on as `AMOUNT = scope:x` into the writers (their `save_scope_value_as` / `change_variable` take a value).
- needs-local-validation: Tiger and PX over `docs/test_submods/test_harness/` (with the main mod), then the session: GP1, GP2, GE1/GE2 as Raoul/Hoël/Bertrand; GC2 as Konan (reload between a and b); GT2 needs two Trade Oligarchy vassals (V-TO9); VD1, VD5 on any ruler; VD2 → answer 0030 → VD3 on a throwaway save; VD4 last or from a reload (its Voidwalker makes VD2 SKIP).
- needs-loc: none (harness loc is generated).
- needs-lore: none.
- needs-human: none.
- taskboard: none.

## H2: the Void in the simulation

Not started.

## H2a: simulation model fixes (corrects M1)

### HANDOFF (cloud session, unvalidated)
- branch: `claude/final-h-cloud` (merged origin/v2-space-map at 295ea5a first: the Void post-merge fixes and lore loc)
- status: done
- summary: The nine local-audit items are applied and the full grid rerun (`run_all.py --checks --hostile`, about 3 minutes here, about 6.5 minutes locally).
  - (1) Per-owner war state in `common.World` (`v_at_war`, vassal own wars about 3% of years), used by every vassal path: the Trade Oligarchy tick, the Corporation results tick, Cartel Lean on the Locals, and PMC Deliver Results. **M1 flips:** vassal Princes hold 55–57 against the First Prince's 23–28. The First Prince's feed turns negative above a 20% war share (sweep: 54.6 at 10%, 10.0 at 30%), and non-dynasts would win 32–37% of elections without the dynasty rule.
  - (2) The cybernetics development sample is conditioned on ≥ 10: a pushing player reaches Overclocked in 34.0% of installs (P4: 50.7%), and cascade deaths go from 9.4% to 14.5% under P4.
  - (3) The Cartel walk-off is measured over 10 years: P5 takes it from 0.436 to 0.218 with 4 vassals, and from 0.146 to 0.043 with 16.
  - (4) A note sits beside H1: only the top's direct vassals erode the CEO (`eotg_corporation_decisions.txt:152-158`), so read the 4–8 director rows.
  - (5) `--checks`, `--hostile` and `--only` flags; the runtime and dependencies are in REPORT and README.
  - (6) P6 is marked not simulated (the gold proxy runs about 2× vanilla, which has a floor of 50).
  - (7) The patch carries the loc for P1, P2, P3 and P6 (plus P5's existing line). `git apply --check` passes on the merged tree.
  - (8) `results.json` is gitignored and untracked.
  - (9) A recommendation table sits at the top of REPORT. **Take now:** P5 and P1. **Owner call:** P2-cap, a once-a-year cap on Deliver Results, simulated beside P2 (AI 16 vassals: 59.8 → 56.2 against P2's 42.8; full pressure years at 100: 77.8% → 57.0%). **Hold:** P2, P3, P4 and P6, each with its reason.
  - Also: L2's hostile-world numbers now come from the code (1.2% / 4.3% / 9.2% abandonment for Settlement / Research / Administrative). The first run's 10% / 25% did not reproduce and are withdrawn.
- files: `docs/tools/sim/{common.py,run_all.py,report_tables.py,exploit_scan.py,README.md}`, `docs/tools/sim/models/{cartel,corporation,cybernetics,gobcorp,pmc}.py`, `docs/qa/mechanics_sim_2026-11-03/{REPORT.md,exploit_scan.md,proposed_tuning.patch,.gitignore,chart_*.png}`; `results.json` removed from the index.
- unverified-vanilla: `00_basic_values.txt:82` (the medium gold floor of 50) is quoted from the local audit; I couldn't read vanilla here.
- needs-local-validation: rerun `python docs/tools/sim/run_all.py --checks --hostile` and compare REPORT. Run `git apply --check docs/qa/mechanics_sim_2026-11-03/proposed_tuning.patch`.
- needs-loc: the patch's loc lines (P1, P2, P3, P6) need a localizer read before anything is applied.
- needs-lore: none.
- needs-human: the REPORT recommendation table: take P5 and P1; decide the P2 shape (cap or value); decide M1 (is a First Prince out-shared by vassals intended?).
- taskboard: CB-66 can move from "model fix pending" to "recommendations ready".

## H2b: the Void in the simulation

### HANDOFF (cloud session, unvalidated)
- branch: `claude/final-h-cloud`
- status: done
- summary: `docs/tools/sim/models/void.py` reads the merged Void script through `pdx_read`:
  - the accrual block (`eotg_void_values.txt:11-43`, Voidwalker −6 at `:35`);
  - Hollowing start 25 and drift +4 (`:46-53`);
  - the contact chance 4 player / 1 AI from its `is_ai` branch (`:60-66`);
  - the stage triggers as written;
  - the band thresholds (25/50/75 and 50/85) from the refresh effects;
  - every slot of `eotg_on_yearly_void_check` (chance or weight, and the cooldown it sets);
  - every option of the 15 events, with the `eotg_void_*` scripted effects inlined.

  It follows the on_action's order (accrual, forced Hollowing, one roll by stage, then the Voidwalker only if nothing fired), and the 0004 gate is read from the script. Outputs:
  - **The Q5 contact sweep** (0.5/1/2/4% plus the default; 10/25/50 years): within 50 years, the default leaves 86.6% of player seats contacted and 13.4% ever Touched, against 40.3% and 4.6% for AI seats.
  - **Stage timings:** contact to Touched takes a median of 28–29 years; Touched to Hollowed takes 4. With a Voidwalker seated at contact, Touched falls to 0.3%.
  - **0004's yield:** 0.50 Voidwalkers per 100 seat-years, about two thirds of them unseated.

  REPORT gets a "Void" section:
  - **VH1:** the Touched stage is a 4-year sprint behind a 5-year cooldown, so stage-C events fire 0.038 per 100 seat-years. **V1** (Touched term +6 → +2) takes that to 0.211, with Touched lasting 6 years.
  - **VM1:** the Voidwalker arrives too late. **V2** (0004 roll 12 → 25) doubles arrivals.
  - **VL1:** keep the Q5 default.
  - **VL2:** the −6 term is not a lever.
  - **VL3:** the exploit scan is clean.

  V1 and V2 are in `proposed_tuning.patch` (not applied; `git apply --check` passes). `exploit_scan.py` now walks `eotg_void_*` scripted effects inline (so it sees the shared ward cooldown) and adds a Void table. There is one chart, `chart_void.png`. The recommendation table gains V1 (take now), V2 (owner call) and Q5 (keep).
- files: `docs/tools/sim/models/void.py` (new), `docs/tools/sim/{run_all.py,report_tables.py,exploit_scan.py,README.md}`, `docs/qa/mechanics_sim_2026-11-03/{REPORT.md,exploit_scan.md,proposed_tuning.patch,chart_void.png}`.
- unverified-vanilla: none new. The model reads only mod script; the option-availability and choice rules are ASSUMPTIONs listed in REPORT Appendix C.
- needs-local-validation:
  - run `python docs/tools/sim/run_all.py --checks --hostile` (or `--only void` for this part) and compare REPORT's Void section;
  - run `git apply --check` on the patch;
  - in game, the harness VD tests plus 10 years as a Touched ruler (count stage-C events).
- needs-loc: none (V1 and V2 change no player text; `docs/specs/void_corruption_v2.md` §3.3's accrual table would need +6 → +2 if V1 is taken).
- needs-lore: none.
- needs-human: V1 (recommended), V2 (do you want Voidwalkers about twice as common?), Q5 (keep 4/1).
- taskboard: CB-65 Q5 now has data; V1 and V2 belong beside it.
