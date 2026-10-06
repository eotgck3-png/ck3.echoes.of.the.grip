# In-game session plan (all pending checks, one place)

**For:** the owner, testing with `-debug_mode`. **Written:** 2026-10-06, against `v2-space-map` at `e481957` (Frontier Phase 3a merged) plus the tools branch `claude/test-session-cloud`.

This plan gathers every check still waiting for a human into **three sittings**:
1. engine checks first;
2. then cybernetics;
3. then Frontier, Phase 1 → 2 → 3a.

Overlapping checks are merged, and each says where it came from, so a failure can be routed. It replaces nothing: the source files keep their detail, and this is the order to run them in.

**Sources** (cited after each check as *src:*):

| Short | File |
|---|---|
| **F1** | `docs/specs/frontier_v1_test_plan.md` (CB-37) |
| **F2** | `docs/specs/frontier_v2_test_plan.md` |
| **F3** | `docs/specs/frontier_v3_test_plan.md` |
| **CTP** | `docs/qa/cybernetics_test_plan.md` §3 (CB-01) |
| **CB-nn** | `circlebackTaskboard.md` item |
| **LBH** | `docs/qa/loc_bug_hunt_2026-10-05.md` |
| **FIX** | `docs/handoffs/orchestrator_2026-10-05_cyber-fix-batch.md` (built in `87a5811`) |
| **REC** | `docs/qa/generated/console_recipes.md` (per-event setup lines) |
| **HTT** | `docs/qa/HOW_TO_TEST_IN_GAME.md` |
| **PROC / INT / REALM / REP / SELF / TOPT** | `docs/specs/cybernetics_v2_{procedures,interactions,realm,reprisal,self_repair,tier_options}.md` §9 (CB-35, CB-38, CB-39, CB-40, CB-41, CB-43) |

**How to use it:**
- Tick `[ ]` → `[x]` as you go, or write **FAIL** and the check id (e.g. `E-3 FAIL`).
- **Save often:** each group says which save to start from, so a failure never costs a restart.
- At the end, send what §S asks for.

> **Not every taskboard "blocked" item is still blocked.** CB-01, CB-02, CB-03 and CB-21 are listed as *blocked* on the descriptor and the test map. The descriptor exists now (the junction, CB-29), and cybernetics runs on the vanilla map. So they are included here (sitting 2). CB-20, the 50-year observer run, is optional (§C13).

---

## §0 Setup (once)

### 0.1 Playsets: make two, never both sub-mods at once
| Playset | Mods, in this order | Used for |
|---|---|---|
| **A: vanilla map** | **Echoes of the Grip**, then **EotG Test: Frontier on Corsica and Sardinia** | sittings 1 and 3 (Frontier), and cybernetics if you prefer the vanilla map |
| **B: test map** | **Echoes of the Grip**, then **EotG Test Map** | cybernetics (sitting 2): built for it (`docs/test_map/README.md` "Cybernetics") |

- Install the Corsica/Sardinia sub-mod as its README says (`docs/test_submods/frontier_vanilla/README.md`). Install the test map with `python docs/test_map/install.py --out "<…>/mod/eotg_test_map"`, and **re-run it after any change in `docs/test_map/`**.
- **Never** load the test map and the Corsica/Sardinia sub-mod together: the test map replaces the vanilla map.
- **The observer sub-mod** (`docs/tools/observer/`) only goes in for the optional §C13 run.
- **Test map caveat:** its heightmap is still the vanilla fallback until `MAPEDITOR_STEPS.md` is done (B-TEMPMAP), so terrain looks wrong. Script works. If playset B won't load, run sitting 2 on playset A as any king with vassals (see 0.4).

### 0.2 Launch options
- **`-debug_mode`**: required. Every `(Debug)` decision is `debug_only`, and debug mode also shows character and event ids. Steam: Properties → Launch Options. Paradox launcher: Game settings → Launch options.
- **Never `-mapeditor`** for play: picking a bookmark with it crashes after "Setup powerful vassals" (`docs/test_map/README.md`).
- **Before you start, ask the orchestrator "is the tree clean?"** The game runs the repo working tree through the junction (HTT §1). Restart the game after any commit; script and loc load at startup.

### 0.3 Recommended start (playset A)
**1066 bookmark → Orsocorre I, Judge of Cagliari** (Sardinia).

What the sub-mod does on a new game (it only runs on a **new** game, never on a loaded save):
- marks 8 counties Unsettled:
  - Corsica: `c_ajaccio`, `c_bastia`, `c_vecchio`;
  - Sardinia: `c_cagliari` (your capital), `c_arborea`, `c_gallura`, `c_logudoro`, `c_tortoli`;
- marks **`c_vecchio` and `c_tortoli` Unknown** as well.

**Do this first, then save as `S0_start`:**
- [ ] **0-1** Hover `c_cagliari`: it shows `Unsettled Region`. Hover `c_tortoli`: `Unsettled Region` and `Unexplored Region`. *src: F3 intro; sub-mod README*
- Note your own character id, and the ids of the holders of `c_arborea` and `c_tortoli`. Hover a character to see its id. You'll need these for grants and backers.

**If you hold only one county** (you need a second Region to grant away in E-1 and F1-4.5): give yourself a neighbouring one from the console. Neither line below is verified in game, so if both error, play a ruler with two or more counties:
- `effect title:c_arborea = { change_title_holder = { holder = root } }`, or
- the vanilla debug command for titles (type `help` and look for a title-granting command).

### 0.4 Console basics (HTT §2)
- Open the console with the key below Esc.
- Commands act on **your** character unless an id is given.
- The command to switch which character you play is **not verified**. `play <id>` may work; otherwise `help` lists it. You need it to move between rulers in one save.
- For a Region other than your capital, `title:<c_key>` replaces `capital_county` in every Frontier line.
- **"Run the debug year"** means **(Debug) Run the Frontier Year**. It runs one Frontier tick at once, with no waiting.
- **"Let N years pass"** means speed 5, unpaused, for N in-game years. Yearly checks fire on each ruler's **own** date, so allow a little over N.

---

## Sitting 1: engine checks (playset A, Orsocorre, about 1½ hours)

These decide whether the architecture holds. **If any E-check fails, stop and send §S before going on**: later checks may depend on it. Start from `S0_start`.

### E1 Frontier state survives save, reload and a holder change
- [ ] **E-1** *src: F1 §0.1 (V1), CB-37*
  1. Your capital is already Unsettled. Take **Establish a Frontier** → *An Opportunity Here* → any type. The Region shows `Frontier: Outpost`.
  2. **(Debug) Frontier Readout**: note progress and strain.
  3. **Save, quit to menu, reload.** Still `Frontier: Outpost`, and the Readout shows the same numbers.
  4. **Kill the founder first.** Get their id (hover), then `kill <id>`, or `effect = { character:<id> = { death = { death_reason = death_murder } } }`.
  5. Grant **a non-capital Frontier Region** to a vassal with Grant Title. For that, Establish on your second county from 0.3 instead, with `title:<c_key>` in the console lines. The stage modifier stays on the Region.
  6. Let the year turn (the vassal is the holder now). The Frontier is still there, and strain rose by 1 (No Founder).
  - **Expect:** steps 3–6 keep the Frontier. **Founder rule:** repeat step 5 *without* step 4, and no strain is added.
- [ ] **E-2** County **modifiers** survive save and reload and a holder change. *src: F2 §0.1*
  1. `effect title:<c_key> = { add_county_modifier = eotg_frontier_trait_remote }` on a running Frontier.
  2. Take **Build Frontier Infrastructure** once.
  3. Save and reload, then grant the Region away and back. Both modifiers are still there.
  4. Run the debug year: the Readout's progress still counts them. Remote without a Beacon gains about 1 a year less.
- [ ] **E-3** The exploration variable persists. *src: F3 §0.1 (spec §15 item 7)*
  1. `effect title:c_tortoli = { eotg_frontier_mark_unknown_effect = yes }`. It is already Unknown on this save, so just hover it: `Unexplored Region`.
  2. Save and reload: still there.
  3. If you hold `c_tortoli`, grant it away and back; otherwise skip this step. Still there.

### E2 A holding appears in an empty slot
- [ ] **E-4** *src: F1 §0.2 (V8)*
  1. On a Region with a free holding slot (most Sardinian counties have one), establish a **Settlement**, **Trade**, **Military** or **Religious** Frontier.
  2. Force completion: `effect title:<c_key> = { set_variable = { name = eotg_frontier_progress value = 100 } }`, then run the debug year. If it says *Waiting on Development* or *Control*:
     - `effect title:<c_key> = { change_development_level = 3 }`, or
     - `effect title:<c_key> = { change_county_control = 100 }`,
     then run the debug year again.
  - **Expect:** *No Longer a Frontier*, then a new Port, Bastion or Sanctum in a free slot, **held by the Region's holder, never the founder**. If no holding appears: +1 development and +10 control instead. **Report which.**

### E3 Hooks receive their scopes
- [ ] **E-5** *src: F1 §0.3 (V12), F2 §6, F3 §1.4*
  - Nothing listens to the Frontier hooks yet, so there is nothing to see.
  - After E-1 to E-4, send every `error.log` line containing `eotg_frontier_on_` (§S). An unset-scope line there means the hooks need their fallback.

### E4 `clamp_variable` holds progress and strain in range
- [ ] **E-6** *src: F2 §0.2*
  - Event `.035` gives +4 progress, `.036` +1 strain, `.034` −3 progress. To fire one on a Region: `effect title:<c_key> = { save_scope_as = eotg_frontier_county holder = { trigger_event = eotg_frontier.035 } }`.
  1. `effect title:<c_key> = { set_variable = { name = eotg_frontier_progress value = 98 } }` → fire .035 → **Strip it for parts** → the Readout shows **100**, not 102.
  2. Strain to 8, fire .036 → **Work it now** → strain **8**, not 9.
  3. Progress to 1, fire .034 → **Make do** → progress **0**, not −2.

### E5 Finding captains and faith leaders
*src: F3 §0.2 (spec §15 items 1–5, confirmed statically in round 2; this is the in-game half)*
- [ ] **E-7** Make a Frontier Military: `effect title:<c_key> = { set_variable = { name = eotg_frontier_type value = flag:military } }`. Fire `.040` as above. *Guns for Hire* shows a captain's portrait and name. If the right portrait is empty, send the `error.log` lines with `government_is_mercenary`.
- [ ] **E-8** Set the type to `flag:religious` and fire `.041`. Report whether it names **your head of faith** or **a holy order's leader**. Orsocorre is Catholic, so the head of faith is the easy case.
- [ ] **E-9** The holy-order path: you need a ruler whose faith has **no head** but has a holy order. Use the character-switch command to such a ruler (or create an order with vanilla's decision first), then fire `.041` on a Religious Frontier of theirs.
  - The portrait is the order's leader, and the desc is the *holy order* variant.
  - Send `error.log` lines with `random_faith_holy_order`, `religious_head` or `eotg_frontier_backs_for`.

### E6 Quick cybernetics engine checks (any character, any save)
- [ ] **E-10** The XP track **stacks**. *src: CB-03*
  1. `effect eotg_aug_initiate_effect = yes` → prowess +2 on the character sheet.
  2. `effect add_trait_xp = { trait = eotg_cybernetics value = 50 }` → **+4** in total.
  3. `… value = 100` → **+8** in total.
- [ ] **E-11** Wounds and `on_trait_gained`. *src: CB-35 Engine Q1, PROC §4.9*
  - As an Enhanced ruler, push a wound to rank 3 (repeated `effect increase_wounds_effect = { REASON = attacked }`).
  - Report: does **proc.003** come within 30 days? If not, proc.003 misses wound-ranked injuries, and the scripter needs to know.

**Save as `S1_engine_done`** (playset A).

---
## Sitting 2: cybernetics (playset B as Emperor Aurelian, or playset A as a king with vassals; about 3 hours)

**Who to play.** You need vassals, knights, a spouse, children, an heir, a court physician and a prisoner.
- **Playset B: Emperor Aurelian Vaskar** (900001, lead 1). He has all of them:
  - Melitta (900007) is a physician candidate; appoint her;
  - Nikephoros (900008) is in his prison;
  - Lysias (17) is his heir;
  - he has 3 dukes and 4 counts as vassals.
- **Playset A:** any king with vassals; switch to him with the character-switch command (0.4).
- **Capital development 10+** is the initiation gate (CTP §1c). Aurelian's capital is at 15. On playset A, check yours, and if needed: `effect capital_county = { change_development_level = 10 }`.

**Fresh save first: `S2_clean`**, unaugmented. Every group below says what to reload.
- Console setup per stage (HTT §2, TOPT §11): Augmented, Enhanced, Overclocked, Neurofractured, Seamless.
- **Every event's exact setup lines are in REC.** Look one up with `python docs/tools/gen_test_recipes.py --event <id>`.
- Firing an event cold with no setup can show blank names. That is expected (HTT §2), not a bug.

### C1 Entry, decisions and tooltips (from `S2_clean`)
- [ ] **C1-1** The decision list hovers read as plain text, with no `eotg_flag_…` and no "(BUG: …)" pink text. *src: CB-31 items 1, 2; LBH Class 1/2; FIX A*
  - Seek Augmentation: ticked requirement lines; no "You lose…" lines; the physician line only when you have a physician.
- [ ] **C1-2** Seek Augmentation → init.018 *The Offer You Sought*. *src: CB-31 item 3, CB-34 new beats 4, CB-42*
  - The syndicate paragraph and option e's tooltip show only when you have never had a Patron.
  - The clinic of record is named.
- [ ] **C1-3** Every Seek path installs. *src: CTP 7; PROC §11*
  - **Clinic:** 20 tries with reloads → almost all silent.
  - **Back streets:** 20 tries → init.011 with mixed outcomes, at least one severe or a death across the set.
  - init.010 → init.011 show **the same gang** name. *src: CB-42*
- [ ] **C1-4** A `maimed` count is offered The Prosthetic, and accepting removes `maimed`. *src: CTP 6*
  - Set up with `add_trait maimed`, then let 1–2 years pass, or fire `event eotg_aug_init.006`.
- [ ] **C1-5** Trait options at entry: a brave, a craven and a cynical ruler each see different options on `event eotg_aug_init.001` and `.004`. Use `add_trait` / `remove_trait` between fires. *src: CTP 4*
- [ ] **C1-6** **Under a Ban** (pass it in C10 first, or come back here): clinic options are greyed with **"Augmentation is prohibited in the realm"**, not pink "BUG" text. *src: LBH Class 1 (confirmed site, NOT_eotg_aug_clinic_closed_tt); FIX A1*

### C2 Augmented (`effect eotg_aug_initiate_effect = yes`, then save `S2_aug`)
- [ ] **C2-1** Maintenance, Consult Physician and Remove Implants:
  - their hovers list only modifiers you hold;
  - "the static quiets" shows only at Overclocked;
  - the throttle line shows only if you are throttled.

  *src: CB-31 items 5, 6*
- [ ] **C2-2** Hover the cybernetics trait. *src: CB-31 item 13; CB-21 display*
  - The Integration line is its own paragraph.
  - The (1)/(2) markers match the track.
  - The tooltip shows Augmented / Enhanced / Overclocked with the Integration bar.
- [ ] **C2-3** G9 trait options, each with its trait icon and stress line. *src: CB-34 G9 1, 6; HTT §3*

  | Trait | Fire |
  |---|---|
  | gluttonous | `event eotg_aug_tier1.005` |
  | impatient | `event eotg_aug_tier1.007` |
  - Helper rows also show: impatient, gluttonous and temperate on reject options; fickle on neglect options.
- [ ] **C2-4** The First Upgrade chain: tier1.002 → tier1.021 asks what to change → tier1.022 installs Enhanced at stage 3. *src: CTP 17*
  - The clinic is named in tier1.002 and in the Pursue decision's desc. *src: CB-42*
- [ ] **C2-5** Pursue the Next Stage: *src: CB-31 item 4; FIX C*
  - requirements read correctly;
  - only synergy modifiers you hold are listed;
  - the settling line reads **"Your last change of stage was at least 5 years ago"**.
- [ ] **C2-6** Pursue at Augmented: *src: PROC §11*
  - option g → tier1.022 reveals an outcome;
  - option f with a learning-16 physician → mostly clean.
- [ ] **C2-7** Remove Implants → proc.001. Use the back streets until **Fragments** → proc.002 → Consult the Physician is visible and clears it. *src: PROC §11*
  - **Removal ladder (owner ruling):** at Augmented only *Remove the Implants* is offered, never Cut It Out. *src: FIX B*
- [ ] **C2-8** Leave the system entirely. 1–3 years later proc.020 fires **once**, and zealous vassals show "Reassured". *src: PROC §11*
- [ ] **C2-9** Kill an augmented parent (augment a parent by console, then kill them) → the heir gets **A Parent's Hardware** within about 2 years. *src: CTP 8*
- [ ] **C2-10** tier1.019 (Copycat): the new option **b** costs minor gold, gives "Reassured" to the copycat (or to kin at court if the copycat died), and is greyed when you can't afford it. *src: commit aa2bb5d*

### C3 Enhanced (`effect add_trait_xp = { trait = eotg_cybernetics value = 50 }`, then save `S2_enh`)
- [ ] **C3-1** The removal ladder: Enhanced offers **Partial Implant Removal only**. **No Cut It Out.** Cut It Out's text reads as the deadly last resort (it can kill; everything comes out; major gold), clearly unlike Remove the Implants. *src: FIX B*
- [ ] **C3-2** `add_trait chaste` → `event eotg_aug_tier2.004` → option **e**: "Reassured" or "Unease", depending on whether the spouse is chaste. tier2.017 follows 180–365 days later. *src: CB-34 G9 1, 2*
- [ ] **C3-3** `add_trait fickle` → `event eotg_aug_tier2.020`: the option shows with its icon. *src: CB-34 G9 1*
- [ ] **C3-4** `event eotg_aug_tier2.011` → option c's success shows **Trimmed Levy Plan** (+5% tax, no opinion change). *src: CB-31 item 10*
- [ ] **C3-5** `event eotg_aug_tier2.013` → `.014` show **the same two different vendors**, and the bold-firmware modifier names the bold vendor. *src: CB-42*
- [ ] **C3-6** A child born to an Enhanced parent → *Absent at the Birth* within 3 days. *src: CTP 18*
  - Have your spouse pregnant, or let time run.
- [ ] **C3-7** tier2.016 (after a Tamper, C9): option **d** is absent in the culprit outcome, and removes Tampered in the malfunction outcome. *src: TOPT §11, CB-43*
- [ ] **C3-8** An injury: `add_trait one_legged` → proc.003 within 30 days. A second injury within 3 years gives nothing. *src: PROC §11*
  - **A ruler who is their own physician:** no option b in proc.001/.003, only e (self). *src: CB-35 item 3*
- [ ] **C3-9** A booked removal blocks a second booking. The decisions read **"No procedure is already booked"**. *src: CB-35 item 2*
- [ ] **C3-10** `event eotg_aug_tier2.001` (*Emotional Delay*): when you have a spouse, kin or a free adult courtier, the desc names one of them (no blank names). *src: commit aa2bb5d*

### C4 Overclocked (`… value = 100`, then save `S2_oc`)
- [ ] **C4-1** At stress 0, Overclocked does not cascade before the 7th yearly check (let about 7 years pass, or check the risk at the console). After `add_stress 250`, the cascade comes within 3 checks. *src: CTP 1*
- [ ] **C4-2** Downgrade Protocol can be taken at stress 0. Its tooltip shows scaled gold and **no risk number**. *src: CTP 3*
  - **Cut It Out is offered** at Overclocked. *src: FIX B*
- [ ] **C4-3** The Countdown story:
  - `effect set_variable = { name = eotg_fracture_risk value = 55 }` → Minor Anomalies within about 5 months;
  - raise it to 76 → Violence comes next (skipping stages) and names its victim;
  - downgrade with the halved risk under 50 → The Quiet fires **once**, and the Countdown stops.

  *src: CTP 22–24*
- [ ] **C4-4** Trait options on these events, each with its trait icon. *src: CB-34 G9 1, 3, 4*

  | Trait | Fire | Expect |
  |---|---|---|
  | lustful | `event eotg_aug_tier3.003` | the option shows with its trait icon |
  | temperate | `event eotg_aug_tier3.010` | option f gives **Dulled Senses for 2 years** |
  | arbitrary | `event eotg_aug_tier3.021` | option d gives **Falsely Accused**, +10 dread, one arbitrary stress line |
  - tier3.021 is via its parent; the setup is in REC.
- [ ] **C4-5** tier3.006.e: *src: TOPT §11; CB-43*
  - with `eotg_fracture_risk` at **10**, the result is the *clean* toast;
  - at **50**, the *strained* toast;
  - the option tooltip never shows the condition.
- [ ] **C4-6** tier3.006 shows no opinion-removal lines when nothing is held. *src: CB-31 item 8*
- [ ] **C4-7** tier3.014.b's result appears as a **toast after the click**, not on hover. *src: CTP 21*
- [ ] **C4-8** First Contact (tier3.012) fires only **once** per character. *src: CTP 19*
- [ ] **C4-9** The Plot: the reveal (tier3.018) comes **4–8 months** after the accusation. *src: CTP 20*
- [ ] **C4-10** `event eotg_aug_tier3.007` → option a → your opinion breakdown of the other Overclocked character shows **"Admiration"**, and the opinion names read right. *src: CB-34 new beats 6*
- [ ] **C4-11** Violent Impulse (tier3.001) names its victim. With an empty court, it shows the "no one was near" text and no portrait error. *src: CTP 5*

### C5 Neurofractured (`add_trait eotg_neurofractured`, then save `S2_nf`)
- [ ] **C5-1** A Neurofractured count who makes no choices reaches the 30+ band in about 3–4 years. *src: CTP 2*
- [ ] **C5-2** The pool shifts with the risk. *src: CTP 9*
  - Set `eotg_fracture_risk` to **10, 45 and 70** in turn, letting 1–2 years pass at each.
  - Expect Flicker events (wrong names, the mirror), then Fracture (blood on the sleeve), then Storm (the Warrant, regency, the Massacre).
- [ ] **C5-3** A Warrant creates a liberty faction or adds discontent. *src: CTP 10*
- [ ] **C5-4** **ENGINE: Containment Regency lasts a full year** and is still active after 2–3 months on a healthy adult. Start it with `event eotg_fracture.025`, then let a year pass. If the engine ends it early, report it: the scripter has a fallback ready. *src: CTP 11, CB-02 (Q7), CB-21 (M15)*
- [ ] **C5-5** Scrambled swaps a personality trait visibly. *src: CTP 12, CB-31 item 11*
  - `event eotg_fracture.018` → option a's toast names the forgotten person.
- [ ] **C5-6** `event eotg_fracture.019` → .020: sparing a real traitor shows `desc_true_spared` and "It was right. I was not.", with no prestige. *src: CB-31 item 12*
- [ ] **C5-7** fracture.006.b shows no opinion-removal lines when nothing is held. *src: CB-31 item 8*
- [ ] **C5-8** **New gate (this branch):** The Court Massacre (fracture.004), as a **callous** ruler (`add_trait callous`). *src: this branch, B4*
  - **Fill the empty places by the next watch** (option e) shows **only when someone was killed or wounded**.
  - On a run with no victim (an empty court), it does not show; zealous option c doesn't either.
- [ ] **C5-9** Risk **96** → The Cascade. *src: CTP 13; CB-21 (M1)*
  - Next year's risk starts at about **8** after a cascade.
- [ ] **C5-10** Excision can kill, and can also free the character. An excision **death** gives no survival event. *src: CTP 14, CB-21 (M2)*
- [ ] **C5-11** **The Heir's Arc** (primary heir 14+; start with `event eotg_aug_heir.001`). *src: CTP 16; CB-34 new beats 1, 2, 7; HTT §3*
  - **Round 1:** at heir.004 take the kill option.
  - **Round 2:** make another character your heir and let 1–2 years pass. heir.007 *The Next in Line* shows `desc_executed` with the dead predecessor's portrait, and option a is gendered. Then heir.003 and heir.004 show `desc_successor`.
  - The story **ends** after round 2's heir.004: no third heir.007, and a finished arc never restarts.
  - Read once with a **female** and once with a **male** heir: the pronouns are right.
- [ ] **C5-12** **Who sees heir.005** after the restructure: note who gets it. *src: CB-21 (H3)*

### C6 Seamless (`add_trait eotg_total_integration`, then `effect set_variable = { name = eotg_aug_residue value = 3 }`; save `S2_seam`)
- [ ] **C6-1** Seamless strips personality and stops the episodes, and the court thins out. *src: CTP 15; CB-31 item 7*
  - Total Integration's tooltip listed only the traits you actually had.
- [ ] **C6-2** end.011 *The Empty Hall*: *src: CB-21 display; commit aa2bb5d*
  - shows a whole number;
  - names the most notable courtier who left (`desc_named`).
- [ ] **C6-3** `add_trait blind` → proc.004, and the trait is gone. *src: PROC §11*
- [ ] **C6-4** Over 10 years: *src: PROC §11*
  - Ledger, Resignation and Flicker appear; after three residue moves, no more Flicker;
  - heir.004 with a Seamless owner shows `desc_seamless`, not `desc_silent` or `desc_premonition`;
  - an adult heir with no arc gets heir.004;
  - the end.041 resigner is never the spouse or close family, and the end.041.c toast shows (CB-35 item 1).
- [ ] **C6-5** The Seamless trait icon shows (no checkerboard). Also on act.001.f, act.003.g and nr.003.g. *src: CB-43 art; CB-04*

### C7 Patron and Reprisal (from `S2_clean`: Seek → init.018 → option e; save `S2_patron`)
- [ ] **C7-1** Accept the Patron. *src: CTP 25; CB-42*
  - The envoy arrives with your culture and faith.
  - Repayment comes in 2–3 years (3–4 if you read every clause).
  - Three refusals bring the Final Demand early.
  - The syndicate's **name** holds from .001 to .007, and through .009 when the story is parked. .006.d reads "a rival syndicate".
  - `error.log` shows no `random_list` errors when patron.006 fires.
- [ ] **C7-2** **Envoy present:** options c and e of .006 kill the envoy. At demand 2, if the envoy is the only possible critic, .005 fires instead. *src: CB-31 item 15*
- [ ] **C7-3** **Envoy absent** (kill them by id): *src: CB-31 item 14*
  - .006 shows the `_absent` text, with no portrait and no options c or e;
  - when d fails, nobody dies; an augmented owner gets the throttle and the risk.
- [ ] **C7-4** Remove Implants during a Patron debt: the debt continues, the clause stays, and only non-hardware options show. *src: CTP 26*
  - **The Paper:** patron.008 fires **once** after full removal; options a and b behave as specced (CB-34 new beats 3).
- [ ] **C7-5** **Once per life:** after settling, take Seek Augmentation for 10+ years. There is never a second patron.001, and init.018 shows no syndicate line or option e. *src: CB-34 new beats 4; HTT §3*
- [ ] **C7-6** The throttle tooltip shows after a betrayal. *src: CB-34 new beats 5*
- [ ] **C7-7** Reprisal (the paper is sold). Each case is set up in REP §9; reload `S2_patron` between cases. *src: CB-40; REP §9*
  - **case a:** the envoy is murdered at .006 c → .009 at the next tick, with `desc_envoy_dead`;
  - **case b:** an augmented owner, the envoy console-killed, grievance 3 → .006 `_absent` shows a, b, f (and d if deceitful). Taking f gives the throttle and the story ends. With no implants: no throttle, and .009 at the next tick;
  - **case c:** a deceitful owner with no implants and the envoy absent: .006 d fails (reload until it does) → .009;
  - **.009 c:** back at tier 1, with no lien, and the story is gone;
  - **.009 d:** the collector stays as a guest with a murder scheme against you; vanilla discovery names the collector;
  - **.009 e:** on success the collector is in your prison, with the tyranny tooltip; on failure, a guest who owns the scheme.
  - **ENGINE (a):** does that guest's murder scheme actually progress and execute?
  - **ENGINE (b):** can the `remove_short_term_gold` fallback put a ruler into debt?

### C8 Knights, the Retinue and non-rulers (from `S2_clean`)
- [ ] **C8-1** Augment two knights through **Augment a Courtier**. The Retinue starts, and *More Step Forward* follows within 1–2 years. *src: CTP 27*
  - **One** knight → the Retinue starts at phase 1, and *First of the Iron* arrives within 1–2 years, naming the volunteer (CTP 32).
- [ ] **C8-2** An augmented knight progresses within 10–20 years, or at once with `effect character:<knight id> = { add_trait_xp = { trait = eotg_cybernetics value = 50 } }`. *src: CTP 28, 33*
  - *Your Champion's New Edge* fires that year with the matching Enhanced or Overclocked line.
- [ ] **C8-3** An Overclocked knight at risk 85 (`effect character:<id> = { set_variable = { name = eotg_fracture_risk value = 85 } }`) → *The Broken Champion* within a year, and no other non-ruler event that year. *src: CTP 29*
- [ ] **C8-4** At most **one** non-ruler event a year per liege. *src: CTP 30*
  - An imprisoned champion never gets *The Champion's Mistake*.
  - The Arms Race never fires while a Retinue runs (CTP 31).
- [ ] **C8-5** `add_trait forgiving`, then fire `event eotg_aug_nr.004 <knight id>` (on a knight, not yourself). *src: CB-34 G9 5*
  - Option f: the champion is Reassured.
  - A victim gets Disgust **only if one exists**.
- [ ] **C8-6** No range error in `error.log` after init.019.c and retinue.004.a with 1–2 knights. *src: CB-21 (H4)*

### C9 Interactions (CB-38; INT §9 item 12; from `S2_aug` with courtiers)
- [ ] **C9-1** **Offer Augmentation:** *src: INT §12*
  - to an unaugmented courtier via the clinic: a silent install, and gratitude;
  - to a one-legged courtier: the leg is restored;
  - to a zealous one: the send button is blocked, and the AI breakdown says why;
  - via the back streets: init.011 on the recipient 6–18 months later.
  - **Ticking two providers disables the send button** (CB-38 item 3), with readable text, not pink "BUG" text (LBH, `NOT_eotg_aug_send_one_provider_tt`).
  - With no physician, the physician send option reads as text (LBH, `NOT_eotg_aug_send_physician_valid_tt`).
- [ ] **C9-2** **Demand Removal** on an Enhanced vassal: *src: INT §12; LBH*
  - accepted or refused by the shown odds;
  - accepted: the vassal is out;
  - refused: "Demanded Removal";
  - with a strong hook: auto-accept, and "Forced Procedure";
  - with a removal already booked, the failure text reads (LBH, `NOT_eotg_decision_aug_removal_booked_tt`).
- [ ] **C9-3** **Examine** a tier-3 spouse → int.001 with a band line. "Fix the fault" on a flawed patient → proc.002 shows the fault-repair opener. *src: INT §12*
  - A back-street fault repair that comes out **maimed** leaves the fault: Examine still shows `desc_tampered` (CB-38 item 4).
- [ ] **C9-4** **Tamper**, with each agent package: *src: INT §12; CB-38 Engine (a)*
  - the slots fill;
  - **ENGINE:** the vanilla preparations window (`scheme_critical_moments.0002`) opens at phase completion, and "execute" fires tamper.001 → tamper.002 → tamper.004 on the target, with the Tampered modifier;
  - the target's next procedure is worse;
  - failing with discovery gives the target the opinion and a toast;
  - the scheme invalidates when the target leaves the system.
- [ ] **C9-5** **Salvage** from an augmented prisoner (Nikephoros on the test map; augment him first). *src: INT §12; CB-38 Engine (b)*
  - The rough way, about 20 reloads: mixed outcomes, Fragments common, at least one severe.
  - With a physician: mostly clean.
  - Kin dying on the table → kinslayer.
  - The prisoner stays imprisoned.
  - int.002 a, b and c each work, **and its outcome lines match what happened on the table** (ENGINE b).

### C10 Realm: the law, the Ban, the Technician (CB-39; REALM §9 item 12; as an independent ruler)
- [ ] **C10-1** **The law:** *src: REALM §12; CB-39 Engine (c)*
  - the **Augmentation** group shows in My Realm alongside Crown Authority (ENGINE c);
  - pass each law: it costs, and then shows the cooldown tooltip as text, not pink "BUG" text (LBH, `NOT_eotg_aug_policy_cooldown_tt`);
  - a vassal sees it locked, with the liege tooltip;
  - an heir inherits it;
  - a ruler who becomes a vassal reverts to Tolerated within a month;
  - missing law icons show as a blank, not a crash.
- [ ] **C10-2** **The Ban:** *src: REALM §12; CB-39 Engine (h)*
  - zealous vassals show the law's opinion line; augmented vassals show "Outlawed";
  - Seek → init.018 shows the clinic unavailable;
  - back streets, 20 reloads: some are "discovered", and you (the liege) get realm.001;
  - Demand Removal shows the crime line; a refusal gives "Defied the Law", with imprison available;
  - **ENGINE (h):** Offer and Demand open with no provider preselected and the clinic shown as unavailable.
  - Then go back and do **C1-6**.
- [ ] **C10-3** **The Implant Technician:** *src: REALM §12; CB-39 Engine (g)*
  - an augmented ruler sees the court position, and can hire one;
  - the aptitude breakdown shows the augmented line;
  - procedure options read **"My implant technician."**;
  - Maintenance costs half;
  - under a vassal's Ban, the position invalidates;
  - **ENGINE (g):** an unlanded courtier reads their employer's law through `top_liege`.
- [ ] **C10-4** **Borrow Their Technician** from an ally who has one: procedure options offer the technician for a year. *src: REALM §12; LBH (`NOT_eotg_aug_borrow_none_held_tt`)*
  - The "already lent" failure reads as text.
- [ ] **C10-5** **Activities** need DLC: tournaments need Tours & Tournaments; pilgrimages need holy sites, so they wait for Gate 1 faiths. Record them as waiting, not failed. *src: REALM §12 (Engine a, b, d); CB-39*
  - A tournament with an augmented knight → act.001. Bar the knight → they withdraw (no empty vanilla 0800 window).
  - Compete augmented → act.002, and the score moves.
  - Feast → act.004. Hunt → act.005.
  - **ENGINE (a):** the child on_actions under vanilla activity hooks fire, and the parent's trigger gates them.
  - act.002, act.004 and nr.003 fit **five options without scrolling** (CB-34 G9 7, CB-43).
  - A just-Enhanced host sees act.003 **e, not f** (CB-43).

### C11 Self-repair (CB-41; SELF §9 item 9)
- [ ] **C11-1** The culture window lists **Self-Repairing Machinery** in the civic group, early medieval column, with its custom line. *src: SELF §9*
  - **ENGINE (a), the ahead-of-time rate:** a tribal-era culture can choose it as the **fascination**. Note the rate the UI shows, and an in-era innovation's rate.
- [ ] **C11-2** Grant it: `effect = { culture = { add_innovation = eotg_innovation_self_repairing_machinery } }`. *src: SELF §9; LBH Class 2 (Self-Repair, confirmed sites)*
  - The decision shows for augmented tiers 1–3 only, not for unaugmented, Neurofractured or Seamless characters, and disappears once fitted.
  - Its requirement lines read as text, with no pink "BUG" text.
- [ ] **C11-3** The routes: *src: SELF §9*
  - **clinic:** the full price, and the modifier appears. Reload until a bad outcome: proc.002 opens with `desc_refit`;
  - **physician:** cheaper;
  - **technician:** reads "My implant technician.";
  - under a Ban, the clinic is greyed with its reason;
  - with no provider, the decision is invalid with `_no_provider_tt`;
  - with gold for the clinic but not the surgeon: invalid (the gold floor).
- [ ] **C11-4** Calibration lasts 5 years after Maintenance, and 7 after Consult. *src: SELF §9*
- [ ] **C11-5** Overclocked, calm and fitted: risk rises **11** a year; **8** with vendor-safe; **5** with vendor-safe and an excellent technician. *src: SELF §9*
  - Read `var:eotg_fracture_risk` before and after the yearly pulse.
- [ ] **C11-6** Remove Implants and Total Integration both remove the modifier. *src: SELF §9*
  - *A Part Replaced* reads as before.
- [ ] **C11-7** ENGINE (d): tribal rulers can still use it. *src: CB-41 Engine (d)*

### C12 Read-through of the rewritten events (`b3371a0`, `aa2bb5d`; new since the owner's first play-test)
- [ ] **C12-1** Fire each and read it (setup lines in REC):
  - init.012, init.020
  - tier1.001, .003, .004, .019
  - tier2.001, .018
  - tier3.002, .003, .018
  - fracture.004, .020
  - heir.007
  - patron.007
  - retinue.001, .002
  - proc.002
  - end.011, .030

  **Expect:**
  - named actors where the event has one, and no blank names;
  - "your seat" names your capital holding (new custom loc `eotg_court_seat`: bastion, port, sanctum, clanhold; a stopgap word, or "court");
  - no medieval or clockwork words.

  Screenshot anything that reads wrong. *src: commits b3371a0, aa2bb5d*
- [ ] **C12-2** init.020: the desc lists only candidates who exist (no blank names). *src: commit aa2bb5d*

### C13 (optional) The 50-year observer run
- [ ] **C13-1** Follow `docs/tools/observer/README.md`: *src: CB-20, CB-38 Engine (c), CB-39, CB-40, CB-41*
  1. build the sub-mod with `tools/build_observer.py`, and add it to a playset with Echoes of the Grip;
  2. `observe`, then 50 years at speed 5. Do 3 seeds if you can;
  3. run `tools/parse_observer_log.py` on each `debug.log`.
  - Send sections [13]–[16]: does the AI use the interactions, the realm law and self-repair?
  - Send the tier counts, to judge against HQ2: 25–40% of AI count+ rulers augmented by year 30, and at least 15% of those Overclocked or beyond.

### C-T Throughout cybernetics
- [ ] **C-T1** **No tooltip ever shows a fracture-risk number.** *src: CTP "Throughout", CB-03*
- [ ] **C-T2** **No pink "(BUG: …)" text** anywhere (LBH's 7 Class 1 keys and 8 Class 2 sites, fixed in `87a5811`). *src: LBH, FIX A*
  - After the sitting, run the `Trigger Localization` grep (§S).
  - The confirmed sites to look at:
    - clinic options under a Ban;
    - Self-Repair's is_valid;
    - Augment a Courtier's is_valid;
    - tier2.003's greyed prisoner option.
- [ ] **C-T3** The act.003 toasts have **short titles**, not a paragraph (`eotg_aug_act.003.c.hot`). *src: LBH Other; FIX A3*
- [ ] **C-T4** Seller names: in each named event, the desc and the options match, and stay the same while you hover. Cold fires read the generic fallbacks. *src: CB-42*
- [ ] **C-T5** `error.log`: no unset-scope or portrait errors from `eotg_` events, and the story ticks are clean. *src: CTP; CB-03; CB-31 item 16*

**Save as `S2_done`.**

---
## Sitting 3: Frontier, Phase 1 → 2 → 3a (playset A, Orsocorre; about 3 hours)

Start from **`S0_start`**, not from S1: E-checks left Regions in odd states.

**Reading the Regions** (hover the county): *src: F1 intro*
- the stages:
  - `Unsettled Region`;
  - `Frontier: Outpost` / `Foothold` / `Nearly Settled`;
  - `Frontier: Waiting on Development` / `Waiting on Control`;
  - `New Settlement`;
  - `Abandoned Works`;
- Phase 2 traits and infrastructure as county modifiers;
- the Phase 3a exploration modifiers, `Unexplored Region` and `Partly Explored Region`.

**The hidden numbers:** **(Debug) Frontier Readout**.

**Fire any Frontier event on one Region:**
```
effect title:<c_key> = { save_scope_as = eotg_frontier_county  holder = { trigger_event = eotg_frontier.0NN } }
```
**Clear the flavour cooldown:** `effect title:<c_key> = { remove_variable = eotg_frontier_event_cd }`.

Already covered in sitting 1, so don't repeat them here: F1 §0 (E-1, E-4, E-5), F2 §0 (E-2, E-6) and F3 §0 (E-3, E-7, E-8, E-9).

### F-P1 Phase 1 (F1 §1–§6; CB-37)
- [ ] **F1-1** Start every type (7). Mark a fresh Region, Establish, and pick that option in .001. *src: F1 §1*
  - **Mark a Region:** `effect title:<c_key> = { eotg_frontier_mark_unsettled_effect = yes }`. Sardinia's Regions are already marked.
  - **One Region at a time:** finish or abandon a Region before marking the next.
  - The **founder** is a courtier who out-stewards you; otherwise "you looked over the surveys yourself".
  - **Administrative** shows only if you are a duke or above, or the Region isn't your capital.
  - **"Not now"** costs nothing.
  - The cost (medium gold) is taken when a type is picked. The Region shows `Frontier: Outpost`.
  - **Double-start guard:** take Establish twice before answering. The second event's type options are hidden.
- [ ] **F1-2** Progress: run the debug year several times. *src: F1 §2.1*
  - About 6–13 progress a year.
  - Outpost → Foothold → Nearly Settled, with development at the first two stage changes, **once per Region ever**.
  - A resettled Region gets no milestone development again.
- [ ] **F1-3** Completion (force it as in E-4). *src: F1 §2.2–2.5*
  - The development floor is never above the start development plus the milestone development still to come.
  - *No Longer a Frontier* has the type's line. The founder options (pay them well, honour them) show only when you aren't the founder.
  - Afterwards, `New Settlement`: no Frontier decision for the Region, and Establish isn't offered again.
  - **Settlement** adds a settlers' leader to your court; **Research** gives the founder +1 learning; **Administrative** sets control to 100.
- [ ] **F1-4** Strain, one point per cause per yearly tick (Readout); a year with none removes one. The causes: *src: F1 §3.1*
  - **War;**
  - **Low Control:** `effect title:<c_key> = { change_county_control = -100 }`;
  - **No Founder:** imprison or kill them;
  - **Occupation;**
  - **Sponsor Lapse:** F1-8.
- [ ] **F1-5** Failure: set strain to 8 with a cause present (`effect title:<c_key> = { set_variable = { name = eotg_frontier_strain value = 8 } }`), then run the debug year → *The Frontier Falters* names the cause. *src: F1 §3.2–3.6*
  - **Let it go:** `Abandoned Works`, and −1 development if the Frontier had reached Foothold.
  - **New hands:** small gold; half the progress stays; strain 4.
  - **Scale it back:** not shown for Settlement; the type becomes Settlement.
  - **Call on our backer:** only with a backer who can pay double; strain 2.
  - **Abandon a Frontier** abandons the most troubled at once. With *Falters* left open, only "The moment has passed" is offered.
  - **Resettle:** *An Opportunity Here* mentions the earlier attempt, and progress starts 10 ahead per attempt (up to 30).
- [ ] **F1-6** Founder gone (no death event): clear the cooldown, then run the debug year → *The Frontier Without a Founder*. *src: F1 §4.1*
  - It offers: appoint a courtier, lead it yourself, let them manage, and "Push through".
  - Strain builds until someone is appointed.
  - **Every event's ungated fallback:** an event left open after the Region stopped being a Frontier does nothing, and "The moment has passed" shows.
- [ ] **F1-7** **A backer offers** (AI → you). *src: F1 §4.2*
  - Be a vassal with a rich liege (`effect liege = { add_gold = 3000 }`), or have an ally with gold.
  - Clear the cooldown and run the debug year a few times → *An Offer of Backing*: the backer shares the credit if it succeeds and the loss if it fails. Accepting gives a little progress, and they pay yearly.
  - Orsocorre is independent, so use an ally, or the corporation-style hook in F3-10.
- [ ] **F1-8** **You back someone** (you → AI). *src: F1 §4.3*
  1. `effect title:c_arborea = { eotg_frontier_start_effect = { TYPE = trade FOUNDER = title:c_arborea.holder } }`. It is already Unsettled.
  2. **Back a Frontier** → *Whom to Back* shows its stage in words → the AI answers.
  3. **Withdraw Your Backing** then appears and works.
- [ ] **F1-9** **The backer dies.** Kill the sponsor → nothing shows at the moment of death. At the next debug year: *src: F1 §4.4*
  - if the heir is alive, landed, has gold, backs nothing and doesn't hold the Region → the heir carries the backing, with a toast;
  - otherwise the backing lapses (toast, strain +1);
  - if the heir holds the Region: no backer and **no** strain;
  - if the sponsor becomes the holder (grant them the Region): the backing ends with no strain.
- [ ] **F1-10** **Exactly one tick per calendar year.** *src: F1 §4.5*
  1. Note progress.
  2. Grant the Region away mid-year.
  3. Let the year turn **in natural time** (the debug year ignores this marker).
  4. Re-grant it and read again: one year's gain, not two.
- [ ] **F1-11** The AI: mark several AI Regions, then let **10+ years** pass at speed 5. *src: F1 §5*
  - At most 8 active Frontiers, and no AI ruler with more than one.
  - Some start, and some complete or are abandoned (slowly).
  - AI backers appear now and then.

**Save `S3_p1`.**

### F-P2 Phase 2 (F2 §1–§9)
- [ ] **F2-1** **Survey reveals a trait.** On an Unsettled Region, take **Survey a Region** → *Survey Report* names the trait, and the Region shows it. *src: F2 §1.1*
  - **File the report** → Establish there: the Readout starts at 5 (+10 per earlier abandonment).
  - **Send them deeper** (gold) → a second trait, never a third.
  - No Survey of that Region again for 5 years, or once it has two traits.
- [ ] **F2-2** Establishing a fresh, never-surveyed Region reveals one trait, with a toast. A Region never has both `Habitable` and `Hostile Environment`. *src: F2 §1.2–1.3*
- [ ] **F2-3** Trait effects (give one with `effect title:<c_key> = { add_county_modifier = eotg_frontier_trait_<x> }`, then Readout and the debug year): *src: F2 §1.5*
  - **Rich Resources + Mining:** about +1.5 a year. **Hostile** or **Remote:** about −1.
  - **Strategic Location:** control floor +10. **Remote:** −10. **Ancient Infrastructure:** development floor −1.
  - **Dangerous:** below the control floor, +strain each year (.005 names "The Region was never safe..."). A Garrison Post or a Military project stops it.
  - **Hostile Environment:** a quiet year no longer eases strain. An Orbital Station restores that.
- [ ] **F2-4** Abandoning keeps the traits. *src: F2 §1.6*
- [ ] **F2-5** **Build Frontier Infrastructure.** *src: F2 §2*
  - *What to Build* lists only what fits:
    - Habitat, Orbital Station and Navigation Beacon always;
    - **Trade Station** for Trade, or a Valuable Trade Route;
    - **Mining Complex** for Mining, or Rich Resources;
    - **Research Facility** for Research, Anomalous, or Ancient Ruins;
    - **Mission** for Religious;
    - **Garrison Post** for Military, Strategic Location, or Dangerous.
  - The cost (medium gold) is paid on the pick.
  - One build a year per Region; one piece before Foothold, two from Foothold (`… eotg_frontier_progress value = 40`).
  - Speed: about +0.5 a year per piece, +1.5 for a fitting one.
  - Abandoning loses the infrastructure and keeps the traits.
- [ ] **F2-6** Types. *src: F2 §3*
  - In *An Opportunity Here*:
    - the garrison option needs, and costs, a little prestige;
    - the mission needs a little piety;
    - research needs decent learning in you or the candidate. To see it greyed out: `effect = { add_learning_skill = -20 }`.
  - **Military ignores war:** no War strain.
  - **Administrative's Low Control line is 50:** at control 45 it strains, and a Settlement doesn't.
  - **The inputs:** Settlement at control 60+, Trade with a paying backer, Mining at high development, a high-martial Military holder, a pious Religious holder, and a high-stewardship Administrative holder each gain a little more.
- [ ] **F2-7** Settling (give the Region a trait and two pieces of infrastructure first). After *No Longer a Frontier*: *src: F2 §4*
  - every `eotg_frontier_trait_*` and `_infra_*` modifier is gone;
  - the matching legacy shows for 25 years;
  - extra development (at most +3), and +10 control from an Orbital Station;
  - the type's figure: Military, a commander; Religious, a mission elder; Administrative, a Region official; Settlement, the settlers' leader. Each has your culture and faith.
- [ ] **F2-8** The events (fire each with the line above, on a Region that meets its conditions): *src: F2 §5*

  | Event | Needs | Check |
  |---|---|---|
  | .030 *A Rival Backer* | a backer, and a liege or ally who could back | **Take the new terms:** the old backer's opinion drops ("Dropped as a Frontier's Backer"), with a toast. **Keep faith:** opinion up, strain −1 |
  | .031 *The Backer Wants a Say* | a backer who is not you | no option gives a say, and each tooltip says so. **The Region is mine:** opinion down, strain +1 |
  | .032 *Terms Demanded* | Foothold+ | as a vassal count: the liege variant (*Talk him round* / *Talk her round*). As independent (Orsocorre): the settlers' variant → `Settlers' Terms` for 10 years |
  | .033 *A Quarrel in the Camps* | a founder who is not you | **Back the founder:** progress +3, strain +1. **Side with the settlers:** strain −1, progress −2, and the founder resents it |
  | .034 *A Supply Run Lost* | — | the desc adds a line for Remote or Dangerous |
  | .035 *What the Crews Found* | trait room | no known ruins → ruins → `Ancient Ruins`. Known ruins → a derelict → `Ancient Infrastructure`. **Strip it:** +4, no trait |
  | .036 *A Rich Seam* | trait room, no Rich Resources | **Survey it:** `Rich Resources`, +2. **Work it now:** +4, strain +1 |

  - Every event has an always-clickable option, including on a Region that's no longer a Frontier.
- [ ] **F2-9** Natural frequency: leave one Frontier **15 years** with no console. About 3 flavour events, never two within 3 years. *src: F2 §5; F3 §5*
  - Some may be *Guns for Hire* or *A Faithful Offer* (F3).
- [ ] **F2-10** Expansion B. *src: F2 §9*
  - **B1:** an uncountered Hostile, Remote or Dangerous Region adds a line to *A Hard Year*. *No Longer a Frontier* adds lines for two pieces of infrastructure, studied ruins or anomalies, or a hard Region.
  - **B3:** .035 → **Study them properly** → *What the Ruins Held* 1–2 years later, if the Region is still a Frontier. Both options raise progress, and sharing gives prestige.
  - **B2 salvage:** build, abandon, Establish again → *An Opportunity Here* mentions what's standing, and +5 progress per piece left behind (on top of the 10 per attempt).
- [ ] **F2-11** The AI, over 10+ years: some AI surveys, infrastructure (more where it counters a bad trait), traits on AI Frontiers, and AI completions. Still at most 8 active. *src: F2 §7*

**Save `S3_p2`.**

### F-P3a Phase 3a (F3 §1–§5)
- [ ] **F3-1** **Unknown blocks** Establish and Survey (`c_tortoli` is Unknown). Neither decision offers it. *src: F3 §1.1*
- [ ] **F3-2** **Send an Expedition** (minor gold) → *The Expedition Returns*. *src: F3 §1.2*
  - The Region is now `Partly Explored Region` with **one trait**.
  - The decision is unavailable for that Region for a year.
  - Partial allows Establish and Survey.
- [ ] **F3-3** Again (next year, or `effect title:c_tortoli = { remove_variable = eotg_frontier_expedition_sent }`) → fully charted: `Partly Explored` is gone, and a second trait if there was room. *src: F3 §1.3*
  - **File the charts** at Known: the next project starts 5 ahead.
  - **Send them straight back out** (from Partial, with gold): Known in one report.
- [ ] **F3-4** **Filing on a running Frontier** (round 2): Unknown → explore once → Establish → explore again → **File the charts** gives **+2 progress now**, not survey data. *src: F3 §1.5*
- [ ] **F3-5** **Settling clears exploration** (round 2). *src: F3 §1.6*
  - Establish in a **Partial** Region and force completion → `Partly Explored Region` is gone, and Send an Expedition doesn't offer it.
  - A Region marked only Unsettled behaves exactly as in Phase 2 (F3 §1.7).
- [ ] **F3-6** **Escort** (Dangerous, not Military): *src: F3 §2.1, §2.4*
  1. A Settlement Frontier with `eotg_frontier_trait_dangerous`, and control −100 → the debug year adds Danger strain.
  2. Fire .040 → **Hire them to guard the convoys**: your gold drops by the fee, and **the captain's gold rises by the same amount** (hover them before and after); `Mercenary Escort`; strain −1; no more Danger strain.
  - The option is gone while the escort lasts.
  - It is **not offered on a Military Frontier.**
  - A company at war with you is never offered.
  - The escort ends with the project.
- [ ] **F3-7** **Backing** (Military, no backer) → **Let the company back the venture**: the captain is the backer, progress +3, and no Sponsor Lapse while they have gold. *src: F3 §2.2, §2.3*
  - A Settlement without Dangerous, or a Military project with a backer: .040 never comes naturally, and fired cold only **We will hold it ourselves** is clickable.
  - **.040's desc on a Military project** offers money behind the venture only, with **no convoy guards** (Military desc variant; added on the Unclaimed branch, so check it after that merge).
- [ ] **F3-8** **The captain's company disbands** (round 2). Make a captain the backer, then let the company disband (play on, or ask the orchestrator for vanilla's disband effect). *src: F3 §2.5*
  - Report whether the captain keeps paying, whether the backing lapses (toast), or whether `error.log` shows `eotg_frontier_sponsor` errors.
- [ ] **F3-9** **Religious organizations:** fire .041. *src: F3 §3*
  - **Accept the backing** (no backer yet): the head of faith, or an order's leader, backs it; progress +3; the tooltip says no claim, no say and no authority.
  - **Blessing:** minor piety, progress +2.
  - **Stands on its own:** nothing.
  - **A faith backer dies** (round 2): kill your head of faith (`effect character:<id> = { death = { death_reason = death_natural_causes } }`). At the next debug year, the **new** head backs it, with a toast, **not** the dead head's heir. If they can't back, it lapses. The same applies to an order's leader.
  - **Completion:** minor piety, and fervour rises a little (the faith view's fervour breakdown names "A Frontier mission became a settlement").
  - The text never names a faith or order.
- [ ] **F3-10** **Hooks:** *src: F3 §4*
  - **Trade:** `effect title:<c_key> = { eotg_frontier_set_trade_network_effect = { AMOUNT = 4 } }` on a Trade Frontier → +2 a year. No change on other types.
  - **Corporation-style offer:** `effect title:<c_key> = { eotg_frontier_offer_backing_effect = { SPONSOR = character:<landed count id> } }` → *An Offer of Backing* names them.
- [ ] **F3-11** **AI, Q3-4** (with F2-11's 10+ years): AI Military and Religious Frontiers sometimes gain a company or faith backer, with no event. *src: F3 §2.6*

### F-T Throughout Frontier
- [ ] **F-T1** **No number** in any Frontier tooltip or desc; the debug Readout is the exception. *src: F1 §6; F2 §8; F3 §5*
- [ ] **F-T2** No player text says "barony", "holding slot", "county", "charter", "season", a faction, an era or the Void. Canadian spelling (colour, honour, defence, travelled). *src: F1 §6; F2 §8; F3 §5*
- [ ] **F-T3** `error.log`: every `eotg_frontier` line. *src: F1 §6; F2 §8; F3 §5*
  - Above all the Phase 2 `UNVERIFIED-VANILLA` items: `piety_level`, `county_opinion_add`, the script-value comparisons in `eotg_frontier_triggers.txt`, and `change_development_level` with a script value.
  - **Known benign:** "Flag habitat/mission/… set but never used" (the infrastructure hook payload; LBH "Other").

**Save `S3_done`.**

---

## §U Unclaimed Regions (added after merge)
**Placeholder.** Unclaimed Regions (`docs/specs/frontier_unclaimed_regions.md`) is built on its own branch, which is not on `v2-space-map` yet.

When it merges, its in-game list goes here: V-U1 to V-U15, from that branch's handoff `docs/handoffs/cloud_2026-10-06_frontier-unclaimed.md`. Two changes will apply then:
- the Corsica/Sardinia sub-mod will **release Sardinia as unclaimed**, so sitting 3 moves Frontier play to Corsica;
- **V-U1** (whether the Unsworn holders are playable) belongs in sitting 1, as an engine check.

**Don't test Unclaimed from this plan until this section is filled in.**

---

## §S What to send back

After each sitting, send the orchestrator:
1. **The ids that failed** (e.g. `E-3`, `C5-8`, `F2-5`), each with **one line**: what you expected and what you saw. Ticked boxes need no comment.
2. **Screenshots** of each failure: the event window or tooltip, with the debug event id visible if you can.
3. **`error.log`**, from `Documents/Paradox Interactive/Crusader Kings III/logs/error.log`. The game rewrites it each launch, so copy it **before** restarting.
   - **The loc failures (pink "BUG" text)**, with file:line:
     - Git Bash: `grep -A2 "Trigger Localization" error.log`
     - PowerShell: `Select-String -Path error.log -Pattern "Trigger Localization" -Context 0,2`
   - **Every mod line:**
     - Git Bash: `grep -n "eotg" error.log`
     - PowerShell: `Select-String -Path error.log -Pattern "eotg"`
   - Or simply send the whole file.
4. **Engine answers in words**, whatever the outcome: E-4 (which holding, or the fallback), E-8 and E-9 (who was found), E-11, C5-4 (the regency), C7-7 ENGINE a/b, C9-4/C9-5 ENGINE, C10 ENGINE a/c/g/h, C11 ENGINE a/d, F3-8.
5. **Optional:** the save you were in when something failed, and for C13 the observer reports.

**Known noise to ignore in error.log** (CLAUDE.md "Validation"):
- about 48 lines in vanilla `20_health_effects.txt` (`change_spiritual_fulfillment`, `has_personal_tenet_flag`);
- the kinslayer-path lines (`knows_doctrine`, `rite`, `check_rite` unset);
- "Flag habitat/mission/… set but never used".

Lines in vanilla files with no `eotg` in them are usually version noise. Send them anyway if unsure.

---

## Appendix: merged checks (dedupe record)
| Merged into | Also covers |
|---|---|
| E-1 | F1 §0.1 (V1), CB-37 §0 |
| E-4 | F1 §0.2 (V8), F1 §2.4 |
| E-5 | F1 §0.3 (V12), F2 §6 hooks, F3 §1.4 hook |
| C1-1 | CB-31 items 1–2, LBH Class 1/2 (decisions), FIX A |
| C2-2 | CB-31 item 13, CB-21 display (trait tooltip) |
| C2-3, C3-2, C3-3, C4-4, C8-5 | CB-34 G9 1–6, HTT §3 table |
| C5-4 | CTP 11, CB-02 (Q7), CB-21 (M15), CTP §6 item 4 |
| C5-9, C5-10 | CTP 13–14, CB-21 (M1, M2) |
| C5-11 | CTP 16, CB-34 new beats 1, 2, 7, HTT §3 Heir's Arc |
| C6-5 | CB-04 (Seamless icon), CB-43 art |
| C7-1 to C7-5 | CTP 25–26, CB-31 items 14–15, CB-34 new beats 3–5, CB-42 Patron, HTT §3 Paper and once per life |
| C10-5 (five options) | CB-34 G9 7, CB-43 |
| C-T1 | CTP "Throughout", CB-03 |
| C-T2 | LBH (all), FIX A, CB-31 item 9 (the 9 `.tt` tooltips show text) |
| C-T5 | CTP "Throughout", CB-03, CB-31 item 16 |
| F2-9 | F2 §5 frequency, F3 §5 prompts |
| F-T1 to F-T3 | F1 §6, F2 §8, F3 §5 |
