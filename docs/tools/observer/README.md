# EotG Observer: logging sub-mod for the 50-year run

This is the tool for **CB-20** on `circlebackTaskboard.md`: the observer run in `docs/specs/cybernetics_v2_balance.md` §9.2. It logs the 12 measurements listed there, plus the five interaction counters of `docs/specs/cybernetics_v2_interactions.md` §9 item 10 and the four realm counters of `docs/specs/cybernetics_v2_realm.md` §4.9, so the cybernetics pacing can be judged against the targets you set (HQ2). It changes no gameplay.

**These sources are versioned here, but the main mod never loads them.** CK3 only reads its known folders at the mod root, and this folder is under `docs/`. A build step creates the installable sub-mod **outside** the repo.

---

## 1. What it is

**Sources in this folder:**

| File | Role |
|---|---|
| `common/on_action/eotg_observer_on_actions.txt`, `common/scripted_effects/eotg_observer_effects.txt` | Observer logic: a year marker every 1 January; a census at game start and every 10 years; a yearly check of the Pursue gold gate; a line when a Neurofractured or Seamless ruler dies. |
| `localization/english/eotg_observer_l_english.yml` | Reference copy of the log text. The build regenerates it. |
| `descriptor.mod`, `eotg_observer_submod.mod` | The sub-mod's descriptor and its launcher file. The launcher depends on **"Echoes of the Grip"**. |
| `tools/build_observer.py` | Builds the installable sub-mod. |
| `tools/parse_observer_log.py` | Turns the logs into the §9.2 report, plus sections [13] (interactions) and [14] (realm). |

**What the build adds.** Logging needs hooks inside six main-mod files: the augmentation effects, on_actions, decisions and stories, plus the character interactions (`common/character_interactions/eotg_augmentation_interactions.txt`: Examine and Tamper start, on the click) and the tamper outcome events (`events/eotg_augmentation_tamper.txt`: tamper.001's success, failure and discovery). Offer, Demand and Salvage are hooked in their scripted effects; the realm counters add a hook in `eotg_aug_contraband_effect`, one on the cascade (with a technician), one in Demand's crime-refusal branch, and law and technician lines in the census and the initiation log (the observer's own effects). So the build writes **overlay copies** of those six files into the output folder, with one-line hooks, each tagged `# eotg_obs`.
- CK3 loads the sub-mod after the main mod, so the overlays replace the originals.
- Every hook sits inside `hidden_effect`. The hooks only write `debug_log` lines, a counter (`eotg_obs_tick`), and two flags only the observer reads (`eotg_obs_sought`, `eotg_obs_pursued`).
- The build checks that deleting every tagged line gives back the main-mod file byte for byte.
- The overlays are generated, never stored here. Two duplicate sets of cybernetics definitions in the repo would confuse searches and checks.

> **Rebuild every time the main mod changes.** A stale overlay runs old gameplay code. `--check` (below) tells you if it is stale.

---

## 2. Install

1. **Make sure the main mod has a launcher entry.**
   - The repo has no `descriptor.mod` yet (taskboard B-DESCRIPTOR).
   - If your CK3 launcher doesn't already list the mod as **Echoes of the Grip**, create `Documents/Paradox Interactive/Crusader Kings III/mod/echoes_of_the_grip.mod` containing:
     ```
     version="0.1"
     name="Echoes of the Grip"
     supported_version="1.20.*"
     path="C:/Users/river/Documents/GitHub/ck3.echoes.of.the.grip"
     ```
   - Put **no** `replace_path` lines in it. The main mod ships none of the folders v1 replaced; copying v1's lines would empty the world.
   - If you name the mod something else, edit `dependencies` in both `.mod` files in this folder to match.
2. **Build the sub-mod straight into the CK3 mod folder.** From the repo root:
   ```
   python docs/tools/observer/tools/build_observer.py --out "C:/Users/river/Documents/Paradox Interactive/Crusader Kings III/mod/eotg_observer_submod"
   ```
   - This creates the `eotg_observer_submod/` folder and puts `eotg_observer_submod.mod` beside it, where the launcher looks.
   - It prints the number of hook lines per file and fails loudly if a main-mod anchor has moved.
   - It refuses an `--out` inside the repo.
3. **Check it is current** (also do this before every run):
   ```
   python docs/tools/observer/tools/build_observer.py --out "<same folder>" --check
   ```
   It prints `overlays up to date`, or `STALE` with the file name. If it says STALE, rebuild.
4. **Make a playset in the launcher.** Enable **Echoes of the Grip**, then **EotG Observer**, in that order (the dependency enforces it). Enable no other mods.

---

## 3. Run the 50-year observer

1. **Launch with debug mode.** In Steam → CK3 → Properties → Launch options, add `-debug_mode`. The `observe` console command needs it. It doesn't change the simulation rules.
2. **Start a new game** on the temporary map and pick any character. Closing the lobby fires the year-0 census.
3. **Start observing.** Open the console (`` ` ``) and type `observe`, then set speed 5.
4. **Let it run 50 game years.** Saving at years 10, 20, 30, 40 and 50, or turning on yearly autosave, helps spot checks; the parser doesn't need saves.
5. **Save the log.** Copy `Documents/Paradox Interactive/Crusader Kings III/logs/debug.log` somewhere safe as `run1_debug.log` **before** starting another game; the game overwrites logs on launch.
6. **Repeat** for **3 seeds** in total (each new game is a new seed): `run2_debug.log`, `run3_debug.log`.
7. **Time it (measurement 12).** Note the real-world clock at in-game years 40 and 50. For a comparison, do one vanilla observe run without any mods and note the same times. Vanilla is a different map, so read that comparison as indicative only.

**Where output lands:** `debug.log`. Every observer line contains `EOTG_OBS`, in the form `EOTG_OBS <key> y=<game year> id=<character id>`. Also glance at `error.log` for anything mentioning `eotg_obs` or `eotg_observer`; there should be nothing.

---

## 4. Read it off

```
python docs/tools/observer/tools/parse_observer_log.py run1_debug.log run2_debug.log run3_debug.log --start-year 866
```

The report has one section per §9.2 measurement. **The headline check is item 1 against HQ2.**

| § | Measurement | Target |
|---|---|---|
| **1** | **Census: share of AI count+ rulers at each tier, by title tier** | **HQ2 at year 30: 25–40% augmented, and ≥ 15% of those at Overclocked, Neurofractured or Seamless** |
| 2 | Flows per decade: initiations (random vs Seek), tier-ups (Pursue vs offer), regressions, cascades, endgames, non-ruler cascades | — |
| 3 | Years from initiation to Enhanced and to Overclocked (AI) | median 18–28 years to Overclocked |
| 4 | Decision use per decade and per 10 eligible rulers; regression share of Overclocked exits | every decision used at least once; regression 35–65% |
| 5 | Knights by tier; non-ruler breakdowns; years from augmentation to breakdown | median 15–25 years |
| 6 | Yearly-list events per ruler-year, by tier | Overclocked ≤ 0.5 (plus the Countdown); Neurofractured ≤ 0.4 |
| 7 | Gold gate: share of rulers who are eligible to progress but can't pay | above 70% means cost is the bottleneck |
| 8 | Capital development ≥ 10 / 15 / 20 / 35 at each census | sets the development gates |
| 9 | Neurofractured span (cascade to end), share on Sedation, Sedation courses at the end | — |
| 10 | Countdown stage hits; stage 3 seen in Countdowns that reach stage 4 | ≥ 60% |
| 11 | Heir's Arc, Patron, Retinue: starts and ends | — |
| 12 | Game days per real minute, years 40–50 | flag a drop over 10% |
| 13 | Interactions per decade (interactions spec §9 item 10): Offer installs (landed / unlanded), Demand removals, Examinations, Tamper starts / successes / failures / discoveries at execution, Salvages (and deaths on the table) | judged against HQ2 with [1]; any non-zero count answers engine check (c) |
| 14 | Realm (realm spec §4.9): count+ rulers by governing Augmentation law and technicians employed at each census; initiations per 10 governed rulers by law; contraband crimes and refused-lawful-order refusals per decade; Overclocked → cascade median with and without a technician | judged against HQ2 with [1]; the law levers should roughly cancel |

**How some figures are approximated:**
- **Per-ruler-year rates (4, 6):** each decade is divided by the mean of the two censuses around it.
- **Event volume (6):** counts the five yearly lists only; chain stages and story events are excluded (the Countdown is in item 10).
- **Pursue vs random offer (2):** a random offer taken within a year of a declined Pursue counts as Pursue (rare).
- **Arc ends (11):** ends caused by the owner's death are shown in brackets.

**Raw keys in the log:** if a line shows `eotg_obs_<key>` instead of `EOTG_OBS <key>`, the text didn't resolve; the parser accepts both.

---

## 5. After the run

Hand the report to the architect (taskboard CB-20). Per §9.2, tune **only**:
- the script values in `common/script_values/eotg_augmentation_values.txt`;
- the AI "nothing" factors (`is_ai`);
- the `ai_will_do` numbers.

Change one set at a time, rebuild the sub-mod, and rerun.

## If the log is empty

- The playset must list both mods, with the observer loaded second.
- The game must be launched with `-debug_mode`.
- `--check` must report `overlays up to date`.
- Search `error.log` for `eotg_observer`.
