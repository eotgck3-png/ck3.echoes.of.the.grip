### HANDOFF (cloud session; Frontier v1 fix pass, not run in game)
- **branch:** `claude/frontier-v1-cloud`, rebased onto `origin/v2-space-map` @ `4300d0c`, fixes in `a823fa1`. Pushed with `--force-with-lease` because of the rebase.
- **status:** done. Every MUST and SHOULD item in `docs/specs/frontier_v1_verification.md` §1–§3 is applied, as are the §2 Notes, the test-plan fixes, the approved debug readout and the owner's §4 decisions.
- **validation (sandbox):**
  - **Lint:** `eotg_lint` with the base's baseline gives **0 findings, 0 new** (round 4's L013 and L014 included).
  - **check_all:** **12 pass, 0 fail, 7 skipped** (local-only tools). The two generated reports were regenerated for the 6 Frontier events, because the base's copies were current without them:
    - `console_recipes.md`: 175 events;
    - `spec_conformance.md`: unchanged spec set; the Frontier definitions now appear under "named in no spec", because the base tool reads only cybernetics specs.
  - **Unit tests:** all OK.
  - **spec_conformance on `docs/specs/frontier_v1*.md`:** every identifier in the spec's as-built tables exists in script. The remaining "missing" ids are deliberate:
    - the `eotg_k_cauldron` contradiction note;
    - the fallback name `eotg_frontier_hook_started_effect`;
    - the game-rule option `eotg_frontier_debug`;
    - the "no `eotg_aug`" grep;
    - the declined `eotg_frontier_on_founder_changed`;
    - in the verification file (not mine), the names it reports as replaced.
  - **gen_test_recipes:** FIX 9 (title scopes, order-aware reads) is in round 5, which is not merged. Run read-only from that branch, the Frontier rows are usable, e.g. .005: "needs scope:eotg_frontier_county, saved by effect eotg_frontier_tick_effect", `effect <county> = { … }` lines, and the debug-decision pointer. Regenerate after round 5 merges.
  - All 8 Frontier files parse with no errors and carry their BOM.
- **markers:**
  - **Confirmed items** (V1, V2, V4–V8, V10–V15, V18, V19, V23, V24) lost their UNVERIFIED-VANILLA marker, with a citation where useful.
  - **`# TEST-IN-GAME`:** V1 (persistence), V8 (the barony and its holder), V12 (scopes reach the hooks). All three are in `frontier_v1_test_plan.md` §0.1–0.3.
  - **New UNVERIFIED-VANILLA** (small; marked):
    - `current_year` as a value (Q9 marker, `eotg_frontier_on_actions.txt:24`);
    - `development_level` / `county_control` read as script values (`eotg_frontier_values.txt:111`);
    - `MakeScope.Var().GetValue` in the debug toast (`eotg_frontier_l_english.yml:149`).
- **needs-human:**
  1. Run `frontier_v1_test_plan.md` §0 first, in debug mode.
  2. Then the rest of the plan.
- **one judgment call to confirm:** the 2-year flavor-event cooldown is **unchanged** under the doubled pacing. Each project now sees about twice the events, but each +1 hardship weighs half as much on the 0–8 scale, so strain from events stays proportionate. To keep events per project constant instead, set `years = 4` in `eotg_frontier_event_roll_effect`.

## Item table

Line numbers are for the pushed files. `L` = `localization/english/eotg_frontier_l_english.yml`, `E` = `events/eotg_frontier_events.txt`, `F` = `common/scripted_effects/eotg_frontier_effects.txt`, `T` = `…scripted_triggers/eotg_frontier_triggers.txt`, `V` = `…script_values/eotg_frontier_values.txt`, `D` = `…decisions/eotg_frontier_decisions.txt`, `O` = `…on_action/eotg_frontier_on_actions.txt`, `M` = `…modifiers/eotg_frontier_modifiers.txt`.

### §1 Lore
| ID | Done | How | Where |
|---|---|---|---|
| N1 | done | Sponsor desc: "no claim and no say, only a part in whether the venture succeeds" | L:17 |
| N2 | done | `new_settlement_desc` and `.004.desc` reworded; the Region is never annexed | L:53, L:101 |
| P1 | done | `.003.desc_replace`: "Accepting would end that arrangement." | L:95 |
| I1 | done | `.001.desc` split into an opener plus `first_valid` `_other`/`_self`; `.001.start_self_tt` via `eotg_frontier_start_tooltip_effect` | E:46, L:63-65, L:76, F:34 |
| I2 | done | Settlement, trade, military and religious completion lines are true with or without a new holding | L:102-107 |
| I3 | done | `.002.c`, `.005.d`, `.005.sponsor_tt`: the backer pays by arrangement | L:85, L:123, L:127 |
| I4 | done | `.005.desc_low_control` | L:116 |
| I5 | done | `.004.desc_mining` | L:104 |
| I6 | done | `.010.desc` | L:129 |
| R1 | done | `.004.a` "Pay … well, for all of it." | L:109 |
| R2 | done | `eotg_frontier_mod_unsettled_desc` | L:41 |
| R3 | done (owner: apply) | `.003.desc` credit and loss line | L:94 |
| S1 | done (owner: apply) | `.002.t` "A Hard Year"; the modifier renamed `eotg_frontier_mod_hard_year` (key, loc, event) | L:77, M:66-68, E:320 |
| S2 | not applied (owner) | The Exodus is era-specific; all Frontier text is time-neutral (standing rule) | — |

### §2 QA
| ID | Done | How | Where |
|---|---|---|---|
| Q-B1 (1) | done | Every .001 type option checks `eotg_frontier_can_establish`, and every .002–.005 option that changes a Region checks `eotg_frontier_is_frontier`. Start, complete, abandon and restart are guarded by a state `limit`. .002, .004 and .005 get a "The moment has passed" option, shown only when the Region has left the Frontier state, so an open event is never stuck. | E:59 (and every type option), E:410 / .004 / .005 fallback options, F:105, F:542, F:712, F:744, L:144 |
| Q-B1 (2) | done | `eotg_frontier_active_count` and `eotg_frontier_count_effect` removed. `eotg_frontier_ai_room` reads `any_in_global_list = { variable = eotg_frontier_active count >= cap }` | T:130, F:130 |
| Q1 | done | `_tooltip` loc for all 7 decisions (8 with the readout) | L:4 onward (one per decision) |
| Q2 | done | `save_hook_scopes` clears absent founder and sponsor. `find_sponsor_candidate` clears first. `old_sponsor` is cleared at the start of `set_sponsor`, `clear_sponsor` and `tick_effect`. `_holder`, `_heir_sponsor`, `_lapsed_sponsor`, `_sponsor_candidate` and `_new_barony` are temporary. | F:47, F:518, F:142, F:351-354 |
| Q3 | done (ruling) | Founder valid if alive, adult and free, and any of: is the holder; employer or vassal-or-below of the holder; the holder is vassal-or-below of the founder. Spec §V and the test plan §0.1 updated. | T:59 |
| Q4 | done (ruling) | (a) Floor = `min(type floor, var:eotg_frontier_dev_reachable)`, recorded at start as starting development + milestone development not yet granted. (b) `eotg_frontier_mod_waiting_development` / `_waiting_control` replace the stage modifier at full progress, plus `eotg_decision_frontier_invest_waiting_tt`. | V:55, V:76, F:105, F:280, M:43, D:160, L:48-51 |
| Q5 | done (ruling) | Permanent `eotg_frontier_dev_granted` (0–2); `eotg_frontier_grant_milestone_dev_effect` grants each level once per Region; Abandon keeps its −1 | F:264, F:712 |
| Q6 | done | `establish_effect_tt` says "your most developed Region that is open for settlement" | L:8 |
| Q7 | done | .010 desc has a stage line per offer (early, mid, late), 9 keys | E:807, L:130-138 |
| Q8 | done | `progressed` fires only when progress rose. `development_changed` fires only from `raise_dev` / milestones / the build fallback (Military with a holding: none). `settled` and `abandoned` (and `failed`) go through `eotg_frontier_trigger_hook_effect`, with the scopes saved before the clear. | F:227, F:590, F:80, F:669, F:712 |
| Q9 | done (ruling) | Calendar-year marker `eotg_frontier_tick_year = current_year` replaces the 300-day `eotg_frontier_ticked` | O:18 |
| Note: hard_season comment | done | The comment now says option b | M:66 |
| Note: test-plan path | done | `docs/specs/frontier_v1_test_plan.md` | D:351 |
| Note: `valid_tt` | done | "Your capital Region is not Unsettled, a Frontier or abandoned already" | L:35 |
| Note: AI-to-AI 4× gate | done | `eotg_frontier_ai_would_sponsor` (AI, can sponsor, gold ≥ 4 payments), used for every candidate | T:142, F:525 |
| Note: title change scope | done | `create_title_and_vassal_change` / `resolve` at character scope (`scope:eotg_frontier_holder`), the barony's `change_title_holder` inside; marked TEST-IN-GAME (V8) | F:605 |
| Note: .001 third person | done | = I1 | E:46 |
| Test plan §0.4-5 | done | Kill the founder before the grant; the Q3 rule is explained | test plan §0.1 |
| Test plan §1 | done | The console line for other Regions; "finish or abandon one Region before marking the next" | test plan §1 |
| Test plan §4.2 | done | AI liege or ally setup (`effect liege = { add_gold = 3000 }`) and the conditions it must meet | test plan §4.2 |
| Readout | done (approved) | `eotg_decision_frontier_debug_readout` (`debug_only`) → `eotg_frontier_debug_readout_effect`: one toast per held Frontier with progress, strain, development and control against the floors | D:436, F:765, L:146-150 |

### §3 Engine
| ID | Done | How | Where |
|---|---|---|---|
| E1 | done | `barony_cannot_construct_holding = no` in both the `any_county_province` check and the `random_county_province` pick; the guarded grant is kept | F:605 |
| E2 | done | Additive `on_death` → `eotg_frontier_on_sponsor_death` → `eotg_frontier_on_sponsor_death_effect` (hand-off to `primary_heir`); the yearly tick keeps only the lapse fallback | O:45-58, F:196, F:416 |
| E3 | checked | Gold values are only read in character scopes (`var:eotg_frontier_sponsor = { … }`, decisions, `eotg_frontier_ai_would_sponsor`); no fix moved one | — |
| E4 | done | The test plan says debug mode is required for the `(Debug)` decisions | test plan header |
| E5 | done | The fallback (empty per-hook scripted effects) is documented at `eotg_frontier_fire_hook_effect` and in the on_actions header | F:64-70, O:72 |
| E6 | done | Markers updated (see the markers note above) | all Frontier files |
| In-game tests 1–3 | done | `frontier_v1_test_plan.md` §0.1 (V1), §0.2 (V8), §0.3 (V12) | test plan §0 |

### §4 Owner decisions
| Decision | Done | How | Where |
|---|---|---|---|
| Q3–Q16 defaults accepted | done | Recorded | `frontier_v1_open_questions.md` §A |
| Pacing doubled (10–16 / 8–10 years) | done | The yearly gain sum × `eotg_frontier_pace_value` (0.5). One-off gains halved: Invest +5, push through +4, accepted backing +3, AI-to-AI backing +3. | V:184, V:194, D:166, E (.002 b, .003 a), F:518-535 |
| Strain, failure and abandon rescaled | done | Strain 0–8, failure at `eotg_frontier_strain_fail_value` (8). .002 bands 4 and 6. AI Invest ≥ 4, Abandon ≥ 6. Restart sets 4, the backer branch 2. Per-cause +1 and quiet −1 unchanged, so failure is proportionate. | V:202, F:336, E:675, D:185, D:336 |
| S1, R3 apply; S2 not | done | See §1 | — |
| Time-neutral text | done | Checked: no era, faction, date or "season" in Frontier loc | L |
| Orchestrator rulings Q3, Q4, Q5, Q9 | done | See §2. `frontier_v1.md` §V and `frontier_v1_open_questions.md` §A2 match. | specs |

## Follow-up pass (after the local re-QA), 2026-10-04

Branch `claude/frontier-v1-cloud` (A–C). Tools (D) are on a **new branch `claude/tools-round6-cloud`**, stacked on `claude/tools-round5-cloud` because two of the files it touches are round 5's. Merge it after round 5.

**Validation:**
- **Frontier branch:**
  - eotg_lint: 0 findings, 0 new.
  - check_all: 12 pass, 0 fail, 7 skipped. `spec_conformance.md` was regenerated for the three new effects.
  - Unit tests OK.
  - All 8 Frontier files parse and carry their BOM.
- **Tools branch:**
  - 149 tests OK on LF and on CRLF (autocrlf clone).
  - check_all: 12 pass, 0 fail, 7 skipped.
  - eotg_lint: 0 new (vs baseline).

| ID | Done | How | Where |
|---|---|---|---|
| A1 | done | Marker → citation (game_start.txt:987-991, title_on_actions.txt:103). The comparison is flipped to `current_year > var:eotg_frontier_tick_year`, and the `NOT has_variable` guard is kept in the OR | O:24-27, O:36 |
| A2 | done | Marker → citation (03_dlc_fp2_script_values.txt:88-91, 00_county_control_values.txt:127, 09_mpo_wars.txt:1335) | V:111-113 |
| A3 | done | Marker → citation (coronation_activity_l_english.yml:675, 817). Checked: the readout sets the four `eotg_frontier_debug_*` variables on the county inside `every_held_title`, saves that county as `eotg_frontier_county`, then sends the toast, so the loc reads the same scope after the variables are set | L:149, F:834-852 |
| B | done | `years = 3` at all four `eotg_frontier_event_cd` sets. Spec pacing note: about 4–5 events per typical project. The spec variable table, §6.1 and §6.4 are updated. The test plan only clears the cooldown and assumed no length; its pacing line now states 3 years | F:529-574, spec:37, 233, 497, 518; test plan:20 |
| C1 | done | .005 options a–d also require `var:eotg_frontier_strain >= eotg_frontier_strain_fail_value`. The fallback is `NOT = { AND = { is_frontier, strain >= fail } }` | E:704, 722, 744, 764; E:791-801 |
| C2 | done | The heir is never made sponsor if they are the holder (`NOT = { this = scope:eotg_frontier_holder }`). This sits in the next-tick hand-off, because per C3 the hand-off now happens there. `eotg_frontier_check_sponsor_effect` drops a sponsor who `= holder`, with no strain. An heir who already holds the Region is dropped with no strain as well (C2's "inherits the Region" case) | F:240, F:254, F:477-501 |
| C3 | done | `on_death`: `eotg_frontier_on_sponsor_death_effect` sets `eotg_frontier_pending_heir` = `primary_heir` and `eotg_frontier_pending_from` = the dead backer (used for the lapse toast and as the pending marker), then clears the sponsor (fires `sponsor_changed`). The next tick runs `eotg_frontier_resolve_pending_heir_effect`: if the heir is alive, `can_sponsor` (which includes "backs nothing") and not the holder, they become the sponsor (fires `sponsor_changed`, toast); else lapse (strain +1, toast). If a new backer was found in between, there is no lapse. The pending variables are removed either way, and also when the project ends | F:191-278, F:440, F:775; O:45-48; spec:51, 99, 231, 278-280, 382-385; test plan §4.4; open questions:43 |
| C4 | done | "Too many hard years in a row." | L:120 |
| C5 | done | The spec §3.2 rows for `check_sponsor` / `on_sponsor_death` / the new effects describe the on_death + next-tick flow | spec:278-280, 294 |
| D1 | done | `px_event_report.py --root` (default: its own repo) supplies the variable whitelist. check_all passes it through `px_event_report_cmd(out, root)`. The CLI moved to argparse (same positional `<dir>` and `--all-loc`) and calls `utf8_console` (FIX 8) | tools: px_event_report.py:26-28, 36, 50, 127-136; check_all.py:164-166, 179; tests/test_px_event_report.py |
| D2 | done (see note) | Cause: temp-dir cleanup on Windows. `shutil.rmtree` and `TemporaryDirectory` raise PermissionError [WinError 5/32] while Defender or the indexer holds a file that was just written, so a test that passed fails at random, on Windows only. New `tests/_testutil.py` provides `rmtree` (retries with backoff, clears read-only, leaks rather than fails) and `tempdir()`. Every test file uses them | tools: tests/_testutil.py; all tests/test_*.py; tests/test_testutil.py |

**D2 note:**
- **Not reproduced here:** the failure did not reproduce in this session: 20 runs with different `PYTHONHASHSEED` values and 12 runs in parallel all passed.
- **Other causes ruled out:**
  - Set and dict ordering (seeded runs).
  - Shared fixed paths (parallel runs).
  - Open file handles (none in the tools).
  - Time-dependent output (none).
- **What's left:** the Windows lock on temp-dir cleanup was the one cause left.
- **Another way the same tests could fail:** the four `Real*Current` / `RealRepoBaseline` tests check the live working tree. They fail on purpose while `docs/qa/generated/` is stale. For example, the in-progress local batch shares those files, and a failure there would look like a flake.
- **If it recurs:** send the failing test names and the traceback.
