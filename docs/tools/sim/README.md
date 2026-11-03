# Mechanics simulation

A Monte Carlo harness that models the mod's resource economies and progression systems
**from the actual script**, so a tuning change is measured by rerunning it. Built
2026-11-03 (Part F). It never changes game script. The report lives in
`docs/qa/mechanics_sim_2026-11-03/REPORT.md`.

## Rerun it

```bash
pip install numpy matplotlib          # once; the only dependencies (Python 3.10+)
python docs/tools/sim/run_all.py --checks --hostile   # every number in REPORT.md (about 6.5 min locally)
python docs/tools/sim/run_all.py --runs 500           # quick look (about 25 s)
python docs/tools/sim/run_all.py --only void          # one part: gov, cyber, frontier, proposals, void
python docs/tools/sim/exploit_scan.py --md out.md     # static exploit scan
```

- `run_all.py` writes `results.json` and one PNG chart per system into
  `docs/qa/mechanics_sim_2026-11-03/` (or `--out DIR`). The full run with `--checks --hostile`
  takes about 6.5 minutes on the local machine (about 3 minutes on the 4-core cloud container).
  `results.json` is gitignored: it is deterministic from the seed.
- `--checks` adds the 2,000-run side checks REPORT quotes and the Trade Oligarchy war-share
  sweep; `--hostile` adds the Frontier hostile-world variant (REPORT L2). `--only` limits the
  run to some parts (the charts are drawn only for a full grid; `results.json` holds what ran).
- The seed is fixed, so two runs of the same tree give the same numbers. **Rerun after any
  tuning change:** every model reads its numbers from the script at start.

## How it is built

| File | What |
|---|---|
| `pdx_read.py` | The script reader. It wraps `docs/tools/pdx_parse.py` and **evaluates** script values, scripted triggers, decision costs, cooldowns, `ai_check_interval_by_tier`, `ai_potential`, `ai_will_do`, story `effect_group` intervals, `random_list` weights, and the literal amounts passed to a change effect, all against numpy arrays (one element per simulated ruler). Vanilla named values it can't read come from `VANILLA_DEFAULTS` (each one an ASSUMPTION). Unresolved names evaluate to 0 or false and are logged. `Script.overrides` gives what-if tuning without touching a file. |
| `common.py` | World assumptions (wars, gold, mortality, traits, realm shapes), the AI policy (`annual_take`: `ai_will_do` per check, converted to a yearly chance), and the statistics (quantiles, time at the clamps, equilibrium, settle year, 20-year runaway/dead streaks). Every number here is registered with `assume()`. |
| `models/*.py` | One model per system. Each cites the files it reads in its docstring. |
| `models/void.py` | Void Corruption (H2b): reads the accrual block, the contact chance (`is_ai` branch), the band thresholds, every slot of the yearly on_action and every option of the 15 events; contact-rate sweep, stage timings, 0004 yield and the V1–V3 what-ifs (`void.term.<trigger>` and `void.slot.<event>.chance` overrides). |
| `exploit_scan.py` | The static scan: per action, its cost, cooldown (including timed flag or variable guards), AI reachability and net resource gain a year. It walks `eotg_void_*` scripted effects inline, reads Void exposure as a cost, and flags F1 (net positive, no cooldown), F2 (entry/exit loops), F3 (AI can never choose) and F4 (repeatable monthly). |
| `run_all.py` | The grid, the proposals' before/after reruns (`PROPOSALS`), the charts and `results.json`. |

**Two policies:**
- `ai` follows each decision's `ai_will_do` and `ai_check_interval` as written;
- `greedy` is a player at the top (vassals stay AI): it takes every action that raises its resource as soon as it is valid and affordable, and never spends the resource on a sink;
- `greedy_all` makes every ruler in the realm greedy, an upper bound on pressure (for example, every director courting the board at once).

**War state is per owner:** the top and each vassal have their own war process (a vassal is not at war because its liege is; `eotg_frontier_triggers.txt:383-386`).

**Realm sizes:** 1, 4, 8 and 16 vassals of the same government. 1 and 4 sit under a duke; 8 and 16 under a king, a quarter of them dukes.

## Add a system

1. Write `models/<system>.py` with `run(R, size, policy, runs, years, seed)` returning arrays and counts.
2. Read every mod number through `R`:
   - `R.num('<script value>', ctx)`;
   - `R.decision('<key>')`, then `R.ai_will_do(...)`, `R.cost_value(...)`, `d['cooldown_years']`;
   - `R.effect_group_intervals('<story>')`;
   - `R.change_calls(node, '<change effect>')`;
   - `R.random_list_entries(...)`.
3. Every number you can't read from the script goes through `common.assume(key, value, why)`, so it reaches the report's ASSUMPTION list.
4. Add the system to `run_all.py` (the grid and, if needed, a chart), then rerun.
5. Check the reader's unresolved names: `pdx_read.assumptions_used()` keys starting `unresolved:`. Each is a trigger or value the model has not supplied, and it silently evaluated to 0 or false.

## Known limits

- **Not the engine.** Wars, battles, gold, deaths, opinions and vanilla AI voting are proxies (ASSUMPTIONs). Comparing tunings within the sim is more reliable than any absolute number.
- **Yearly steps.** Cartel dread decays monthly; everything else is yearly. The AI decision chance per year is derived from the per-check chance and the check interval.
- **No events except where a system's outcome table is itself an event.** These are the Frontier falter (`eotg_frontier.005`) and the cybernetics terminal (`eotg_fracture.027`). Flavour pools are a mean ASSUMPTION.
