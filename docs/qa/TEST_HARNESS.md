# In-game test harness

**One click per check.** Each harness decision sets up the scenario for one pending in-game check, using the systems' own effects. Where the result can be read in script, a hidden event checks it a day or so later and writes **PASS** or **FAIL** to `logs/debug.log`. Checks that need eyes (portraits, the top bar, tooltips) write **LOOK** lines that say what to look at.

Built 2026-11-03 by a cloud session; Tiger and PX checked locally the same day. **Nothing here has run in the game yet** (handoff: `docs/handoffs/cloud_2026-11-03_test_harness.md`).

**Test content never ships.** The harness is its own sub-mod, **EotG Test: In-Game Test Harness**, in `docs/test_submods/test_harness/`. The main mod carries none of it.

| File (under `docs/test_submods/test_harness/`) | What |
|---|---|
| `descriptor.mod` | The sub-mod descriptor; depends on **Echoes of the Grip** |
| `common/decisions/eotg_test_harness_decisions.txt` | 39 decisions, all `debug_only = yes` |
| `events/eotg_test_harness.txt` | 49 hidden assertion events (namespace `eotg_test`), fired only by those decisions |
| `localization/english/eotg_test_harness_l_english.yml` | Decision text |
| `README.md` | A pointer to this guide |

**`docs/tools/gen_test_harness.py` generates every file in that folder.** Never hand-edit them: change the generator, then run `python docs/tools/gen_test_harness.py`. The output is deterministic, so a second run changes nothing.

---

## 1. Enable it

1. **Install the sub-mod once.** Make a directory junction from the game's mod folder to the sub-mod folder (cmd), the same pattern as the other test sub-mods:
   ```
   mklink /J "<mod folder>\eotg_test_harness" "<repo>\docs\test_submods\test_harness"
   ```
   Then write `<mod folder>\eotg_test_harness.mod`: a copy of `docs/test_submods/test_harness/descriptor.mod` plus `path="<mod folder>/eotg_test_harness"`. The mod folder is `Documents/Paradox Interactive/Crusader Kings III/mod`. Re-run the generator after any change to it; the junction makes the result live.
2. **Launch with `-debug_mode`** (Steam: Properties → Launch Options; Paradox launcher: Game settings → Launch options; HTT §0.2). Without it the harness decisions don't exist.
3. Use the playsets from `docs/qa/IN_GAME_SESSION_PLAN.md` §0.1, and **add the harness last in both**. It must load after **Echoes of the Grip**:
   - **A**: Echoes of the Grip, then the Corsica/Sardinia sub-mod, then the harness. For cybernetics, Frontier, the alerts and the game rules.
   - **C**: Echoes of the Grip, then the British Isles sub-mod, then the harness. For the government tests.
4. **Use a throwaway save.** The decisions change it for good: they add traits, set Frontier state, add payers and change dread. Save before each group, as the session plan does.
5. Open the **Decisions** tab. Every harness decision is named **"(Test) <ID>: …"**.

## 2. Read the results

Every line the harness writes starts with `EOTG_TEST`. `debug_log` writes to `debug.log`, not `game.log`:

```
Documents/Paradox Interactive/Crusader Kings III/logs/debug.log
```

From the Bash tool, or Git Bash, in that `logs` folder:

```bash
grep "EOTG_TEST" debug.log
```

To see only problems:

```bash
grep -E "EOTG_TEST .* (FAIL|SKIP)" debug.log
```

| Tag | Meaning |
|---|---|
| `START` | The decision ran. |
| `PASS` | A scripted check held. |
| `FAIL: <what>` | A scripted check failed. The text names the condition. **Send these back** with the test id. |
| `LOOK: <what>` | Look at the game now. Record what you saw against the session-plan check named in §3. A numbered LOOK (`AL4.1`, `CY3.2`) replaces a check that script could only answer by restating its own setup. |
| `INFO` | A value worth recording (the game-rule settings). |
| `SKIP: <why>` | A precondition wasn't met; the text says what to run first. Nothing was changed. |
| `DONE` | The test's last step ran. A missing `DONE` after a `START` means an event never fired: check `error.log` for `eotg_test`. |

Sub-steps are numbered: `CY1.4` is the fourth check of CY1.

Also check `error.log` for `eotg_test`, which means a harness bug. Any other mod line found during a test is a real finding for that system.

## 3. The tests

**Plan ids:** `IGSP` refers to `docs/qa/IN_GAME_SESSION_PLAN.md`; `SI` to `docs/qa/system_investigation_2026-10-18/REPORT.md` §3; `V-C` to the Cartel spec §13; `V-SU` to the succession spec; `INT1` to `docs/specs/integration_v1.md` §4.2. **Auto** means the result is checked in script.

### Cybernetics (playset A, any landed ruler)

| Id | Decision | Plan ids | Auto | What it does |
|---|---|---|---|---|
| **CY1** | Tier Ladder | IGSP E-10, C2, C3, C4 | yes | Initiates, then XP 50, then XP 100, a day apart (through `eotg_aug_set_integration_effect`, the only XP writer). Checks tier 1/2/3 and prowess base +2/+4/+8 (does the track stack). Start unaugmented. |
| **CY2** | Neurofractured End State | IGSP C5 | yes | SKIPs unless you have `eotg_cybernetics` (otherwise the check proves nothing). Adds `eotg_neurofractured`; checks it replaced `eotg_cybernetics`. |
| **CY3** | Seamless End State | IGSP C6 | yes, then LOOK | Adds `eotg_total_integration` and 3 residue; checks the trait. The Frontier flavour exclusion is a LOOK (CY3.2): its trigger only reads the trait. |
| **CY4** | Neural Cascade at the Threshold | IGSP C4 | yes | As an Overclocked ruler: risk 80, then runs the real yearly pulse once (`eotg_on_yearly_aug_overclocked_check`). Checks that the Cascade made you Neurofractured (cybernetics trait gone) and reset the risk to 0. The cascade event `eotg_fracture.0001` follows. |
| **CY5** | Track AI Values on a Courtier | IGSP E-13, SI T1 | LOOK | Picks an unaugmented adult AI courtier and raises them a tier every 3 days. Hover them and note energy, honour and zeal at each LOOK line. |
| **CY6** | Wound Rank 3 and the Repair Offer | IGSP E-11 | yes | As an augmented ruler: clears the **real** repair cooldown flag `eotg_flag_aug_repair_cooldown` (the one the repair hook sets for 3 years), then raises your wound up to rank 3. Each `increase_wounds_effect` call is guarded by "not yet `wounded_3`", because vanilla kills a character it wounds at rank 3 (`20_health_effects.txt:1342-1351`). It can't stop at rank 2: the repair hook fires on `wounded_3` only. Checks `wounded_3` and that `on_trait_gained` queued the repair (`eotg_aug_repair_injury = flag:wounded`). LOOK: proc.003 within 30 days. Vanilla's own `wounded_3` health events still follow, so stay on a throwaway save. |

**Suggested order:** CY1 (save) → CY6 → CY4. Reload the CY1 save → CY2. Reload → CY3. CY4 ends Overclocked (the Cascade), so it comes after CY6. CY5 works on a courtier at any time.

### Frontier (playset A, Giovanni or any ruler; all on the capital Shoal)

| Id | Decision | Plan ids | Auto | What it does |
|---|---|---|---|---|
| **FR1a / b / c** | Start a Military / Settlement / Religious Frontier | IGSP E-1 (step 1), E-4, E-12, FX-2 and G-2 setups | yes | Marks the capital Unsettled and starts a Frontier of that type with you as founder (`eotg_frontier_start_effect`, the real path). Checks the state, the type and the founder. SKIPs if a Frontier already runs in your realm, or if the capital is Unknown. |
| **FR2** | Force Frontier Completion | IGSP E-4, E-12 (SI V8), FX-2, G-2 | yes, then LOOK | Progress 100, development +5, control 100, one Frontier year (`eotg_frontier_tick_effect`). **Answer the completion event as soon as it appears:** the check runs 7 days later and fails if the Frontier is still open. Checks it completed and cleared. LOOKs by type: Military → who holds the new Bastion's barony (E-12); Religious → the Sanctum holder's gender (FX-2) and government (G-2); Settlement → which holding and holder (E-4, G-2). |
| **FR3** | Progress and Strain Clamps | IGSP E-6 | yes | 98 + 4 → 100; strain 8 + 1 → 8; 1 − 3 → 0, through the real change effects, a day apart. |
| **FR4a → FR4b** | Mark, then Check Persistence | IGSP E-1 (steps 2-3), E-2 | yes | FR4a adds the Remote trait and records progress. **Save, quit to menu, reload**, then FR4b checks the Frontier, the progress and the modifier survived. |
| **FR5** | Mark the Capital Unexplored | IGSP E-3 | yes | SKIPs while a Frontier runs on the capital, or if it is Abandoned or already has an exploration state. `eotg_frontier_mark_unknown_effect`; checks `eotg_frontier_is_unknown`. Then ends with `eotg_frontier_clear_exploration_effect` and checks the capital is Known again, so it isn't left Unknown (it stays Unsettled). The tooltip is session-plan check 0-1. |

**Suggested order:**
- FR1a → FR3 → FR4a (save, reload) → FR4b → FR2.
- Then FR1c → FR2 (FX-2; reload and repeat 4–6 times, counting the genders).
- As Raoul (PMC, playset C): FR1b → FR2 for G-2.

### Governments and the Cartel (playset C, British Isles)

| Id | Decision | Plan ids | Auto | What it does |
|---|---|---|---|---|
| **GV1** | Cartel Payment Schedule | V-C4, V-C19 | yes | As an independent Cartel ruler (Alfonso, or **(Debug) Become a Cartel**): records the baseline, then +40 dread through the Cartel's change effect. Puts one independent neighbour on the schedule (`eotg_cartel_start_schedule_effect`, the interaction's own effect). Checks the contract group, the payer count, and that the baseline rose by exactly 4. SKIPs at the cap of 40. **It calls the effect, not the interaction,** so it skips the interaction's `can_have_tributaries_trigger` (crown authority 1+) and its other validity checks; whether the interaction is available is a manual check. |
| **GV2** | Cartel Walk-Off | V-C12 | yes | Runs `eotg_cartel_walk_off_effect` once; checks exactly one payer left. LOOK: the toast and the baseline. |
| **GV3** | Elective Candidate Rule | V-SU3, V-SU9 | yes, then LOOK | As a Corporation, Trade Oligarchy or Cartel ruler: the projected successor (`primary_heir`) is of your dynasty (owner ruling: candidates by dynasty; electors unrestricted). LOOK: the vote window. |
| **GV4** | Cartel Resource Core | V-C2 | yes | The Payment Schedule story and modifier exist on a landed Cartel ruler. |

**The tribute lifecycle in full:** GV4 → GV1 (repeat for more payers) → GV2. Then `kill` the ruler for V-C11 (manual: the heir keeps the payers and has the 3-year grace).

### PMC, Corporation and Trade Oligarchy G2 resources (playset C, British Isles)

Added 2026-11-03 (final H1; `docs/handoffs/cloud_2026-11-03_final_h.md`). Spec ids are each spec's §12 (`governments_v2_g2_pmc.md`, `_corporation.md`, `_gobcorp.md`). GP1, GC1, GT1, GP2 and GE1/GE2 read a baseline first and restore it. The two brackets do not: they leave the real 1-year guard variables in the save (below). **Use a throwaway save**, and reload it between brackets.

| Id | Decision | Spec ids | Auto | What it does |
|---|---|---|---|---|
| **GP1 / GC1 / GT1** | Resource Follows a Change (PMC standing / board influence / market share) | V-P2, V-P3 / V-CO2, V-CO3 / V-TO2, V-TO3 | yes, then LOOK | Moves the value +10 (−10 above 90) through its only writer, then +120. Checks the exact delta, that the story counter (written by the sync effect) mirrors the value, that the scaled modifier is still present (the writer re-applies it), and the clamp at 100. Restores the baseline. LOOK (x.4): the modifier's numbers match the new value. |
| **GP2** | PMC Battle Feed Values | V-P6 | yes, then LOOK | Applies `eotg_pmc_battle_won_value` then `eotg_pmc_battle_lost_value` through the writer: exactly +2, then −3. SKIPs within 3 of a clamp. The combat hook needs a combat side a decision cannot build: LOOK GP2.3, fight a battle as war leader. |
| **GC2a / GC2b → GC2c** | Court the Board: record, then check | V-CO8; the 2026-11-03 erosion fix | yes | Play a Corporation **vassal** (Konan). GC2a records your influence, the projected value and your liege's influence and erosion state; GC2b first marks the liege eroded this year (the decision's own guard). **Then take the real Court the Board**, and GC2c the next day: your influence is the projection; the liege lost exactly 5 only if not already eroded and your projection was above theirs, and is then marked; otherwise the liege lost nothing. Reload between GC2a and GC2b (5-year cooldown). **Leaves:** GC2b, and any courting that erodes, leaves the real guard `eotg_corp_board_eroded` on your liege for 1 year. |
| **GT2a → GT2b** | Corner the Market: record, then check | V-TO7 | yes | As the top Trade Oligarch with Trade Oligarchy vassals (V-TO9). GT2a records every Prince's share and marks one as already cornered this year (when there are two or more). **Then take the real Corner the Market**, and GT2b: your share +15; every Prince not yet cornered −5 exactly and now marked; the pre-marked Prince untouched (drained at most once a year). **Leaves:** GT2a leaves the real guard `eotg_gobcorp_cornered` on one Prince for 1 year (and Corner the Market marks the rest); reload before a second run. |
| **GE1 / GE2** | Election Bands (Corporation / Trade Oligarchy) | V-CO13 / V-TO13 | LOOK | Moves your value to each vote band edge (one below band 1, then each band), a day apart, through the writer, and says what the succession tooltip should show. Vote strength cannot be read in script. Restores the value. |

**Suggested order (throwaway save; save first):** GP1, GC1, GT1, GP2, GE1/GE2 (they restore); then GC2a → Court the Board → GC2c; reload; GC2b → Court the Board → GC2c; reload; GT2a → Corner the Market → GT2b.

### Void Corruption (any playset; throwaway save)

Spec ids are `docs/specs/void_corruption_v2.md` §10.

| Id | Decision | Spec ids | Auto | What it does |
|---|---|---|---|---|
| **VD1** | Void Exposure Bands | V-V3 | yes | Not Hollowed. Drives exposure to 24, 25, 50, 75 through `eotg_void_change_exposure_effect`, a day apart; checks exactly one band (none / Whispers / Pressure / Saturation) each time, then restores the baseline and checks the band follows it. |
| **VD2** | The Hollowing Through the Yearly Pulse | V-V8, V-V17 | yes, then LOOK | Touched + exposure 100 through the system's effects; clears the Void cooldown; runs the real `eotg_on_yearly_void_check` once. Checks the **on_action** set the cooldown flag (no event sets it). The Hollowing event follows: answer it (option c steps you down), then VD3. SKIPs if a Voidwalker is at court (VD4 leaves one: with it, a Touched ruler's accrual can go negative, the Hollowing never fires, and VD2.1 would pass for the wrong reason). **Leaves:** the ruler Hollowed, for good. |
| **VD3** | Hollowing Depth Bands and Drift | V-V9, V-V10, V-V11, V-V12 | yes | Hollowed only. Checks Touched gone, exposure 100, no exposure band, the court's Unreachable opinion. Drives depth to 50 (Far Off only), 85 (Gone Quiet only), 10 (none), then runs the yearly pulse once: depth exactly 14 (+4 drift). Restores depth. |
| **VD4** | The Voidwalker at Court | V-V13 | yes, then LOOK | Creates and seats a Voidwalker with option a's own effects. Checks the flag is on a courtier, the yearly accrual value fell by exactly 6, and `can_execute_decision` for the Voidwalker Ward (SKIP when Hollowed, short of 100 gold or on the ward cooldown). **Leaves:** the Voidwalker at your court for good (and VD2 then SKIPs). |
| **VD5** | One Insight per Character | V-V16 | yes, then LOOK | Runs `eotg_void_insight_effect` twice: the six-skill total rises by exactly 4, an Insight is held; LOOK: only one copy listed. **Leaves:** +4 skill and one Insight modifier, for good (VD5 then SKIPs). |

**Suggested order (throwaway save; save first):** VD1 (restores exposure), VD5, then VD2 → answer The Hollowing → VD3; reload the save from before VD2, then VD4. VD4 must come last, or from a reload: its Voidwalker makes VD2 SKIP, and VD4.3 SKIPs on a Hollowed ruler.

Not automated: V-V1 (contact odds; the sim covers it), V-V2/V-V4–V-V7 (random event rolls), V-V14 and V-V15 (they kill or depose, which the harness never does), V-V18–V-V20 (static: Tiger, PX, grep).

### Alerts (INT1; playset A)

| Id | Decision | Auto | What it does |
|---|---|---|---|
| **AL1** | Frontier at Breaking Strain | yes, then LOOK | Strain 6 on the capital Frontier; checks `eotg_frontier_strain_is_breaking`. LOOK: the top-bar alert. |
| **AL2** | Frontier Without a Founder | yes, then LOOK | Removes the founder record; checks `eotg_frontier_has_valid_founder = no`. LOOK: the alert and its click. |
| **AL3** | A Frontier Can Be Established | yes, then LOOK | SKIPs if a Frontier runs in your realm (the alert is off by design then) or the capital is Unknown. Marks the capital Unsettled; checks `eotg_frontier_establish_alertable`. LOOK: the alert opens Establish a Frontier. |
| **AL4** | Implant Calibration Lapsed | LOOK | Removes `eotg_mod_implant_calibrated`. The alert should show only when Maintenance Protocol can be taken: the AL4.1 LOOK line says which case you are in. |

The Unclaimed *Raise Your Colours* alert needs an Unclaimed neighbour (the Sardinia sub-mod setup): look for it in §U of the session plan.

### Game rules (any playset)

| Id | Decision | Auto | What it does |
|---|---|---|---|
| **GR1** | Read the Game Rules | yes | Logs the active setting of every mod rule (`eotg_aug_event_frequency`, `eotg_aug_ai_uptake`, `eotg_frontier_difficulty`, `eotg_race_half_races`, `eotg_race_crossbreeding`) as INFO. It FAILs a rule that reads no known setting, which is how a renamed setting key would show. `eotg_race_crossbreeding` defines only `eotg_race_crossbreeding_free` for now; add settings to `RULES` in the generator when the rule gains them. Start games with different lobby settings and compare. |

## 4. Checks the harness does not automate (manual, by design)

| Plan id | Why it stays manual |
|---|---|
| IGSP G-1 (SI X3), designer over Raoul | Happens in the lobby, before any decision exists. |
| IGSP G-3 (SI X4), tier events on a landless adventurer | Needs a camp character from the bookmark. CY1 can do the tier setup once you play him. |
| IGSP FX-1 (SI F1), FX-3 (SI F6), war and occupation | Needs an enemy army in the Shoal. FR1a and FR2 set up the Frontier side. |
| IGSP C10-6 (SI X7), C10-7 (SI S8), the cybernetics law on Unsworn and on a breakaway realm | AI behaviour and realm splits over time. |
| IGSP V-U16 (SI M1), nomad migration | An observer run with *Khans of the Steppe*. |
| IGSP E-1 steps 4–6, E-2 step 3, holder changes | Need Grant Title by hand. FR4a/FR4b cover the save-and-reload half. |
| Everything a LOOK line names | Portraits, the top bar and tooltips can't be read in script. |

## 5. Extending it

Add a `T(...)` call in `docs/tools/gen_test_harness.py`: id, key suffix, name, description, plan ids, the decision's setup effect, and the assertion events. Then re-run the generator; it writes to `docs/test_submods/test_harness/` (pass another folder as the first argument to write elsewhere).

Rules:
- use only the systems' own effects and triggers;
- every event stays hidden and is fired only by a harness decision (invariant 4);
- every decision stays `debug_only`;
- harness content stays in the sub-mod, never in the main mod;
- a PASS must check something the setup did not write directly; otherwise make it a LOOK;
- log lines start `EOTG_TEST <id> <TAG>:` and contain no `"` or `[`.
