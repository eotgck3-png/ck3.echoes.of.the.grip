# EotG Test: Frontier on Corsica and Sardinia (sub-mod)

**Test only, never shipped.** Lets you test Frontier on the **vanilla map** with the main mod's shaders and cybernetics.
At game start it marks Corsica's 3 counties Unsettled (c_ajaccio, c_bastia, c_vecchio; still owned) and **releases
Sardinia's counties as Unclaimed Regions** (Unclaimed Regions, `docs/specs/frontier_unclaimed_regions.md` §11.1): each
released county gets its own Unsworn placeholder with the county's culture and faith, turns neutral grey, and is
Unsettled. A Corsican count across the strait can claim them with *Raise Your Colours*. Two Regions, c_vecchio and
c_tortoli, also start **Unknown** (Frontier Phase 3a exploration; `docs/specs/frontier_v3_test_plan.md`). Nothing else
changes.

**What actually releases (frontier_v4.md A7.1, 2026-10-11).** The release effect never takes a real ruler's capital
Region, so each Sardinian judge keeps his capital county and nobody ends up landless. At the 867 start the five counties
belong to two judges (vanilla `history/titles/k_sardinia.txt`):

| Judge | Counties | Released |
|---|---|---|
| Gobleno (235092) | c_cagliari, c_arborea, c_tortoli | the two that are not his capital |
| Arzocco (75000) | c_gallura, c_logudoro | the one that is not his capital |

So **3 of the 5 counties become Unclaimed**. The engine picks each judge's capital at history load (probably c_cagliari
for Gobleno), so check the map on the first start (in-game check U2): each judge still holds one county. If c_tortoli is
Gobleno's capital it stays his, still Unknown (owned-Unknown exploration).

**What to look at for frontier_v4 batch 2 (2026-10-11).** Each row is a §10 check; the spec has the pass conditions.
- **A1, Local Ruler (needs V8 first).** A Corsican count is normally feudal, seated in a castle. Finish a Settlement, Trade or
  Religious Frontier there (the debug tick decision, plus console `add_county_modifier` or progress as the frontier test
  plan does). The new System should go to a vassal of yours: the founder when they are your landless courtier (.004
  names them), else the settlers' leader, a new factor (Trade) or the mission elder, with a republic or theocracy
  government. A Military Frontier's castle stays yours. Repeat with the founder killed, imprisoned, or yourself as
  founder: the created figure should hold it.
- **A7.3, Raise Your Colours as a decision.** From a Corsican count: the decision should list exactly the Unclaimed
  Sardinian Regions in reach, default to the most developed, and after one claim block a second for 5 years on both
  the decision and the character interaction.
- **A7.4.** Declare war on a Sardinian Unsworn holder: the CB list should say why you can't (`eotg_unclaimed_defender_tt`).
- **A8.** Hover Invest, Build and Abandon on a Corsican Frontier: pace, time and strain lines in words, with no digits;
  a cause line once strain is high.

Install: the game's `Documents/Paradox Interactive/Crusader Kings III/mod/eotg_test_frontier_vanilla` is a **directory
junction** to this folder (2026-10-11), so edits here are live. Do not copy the folder. To recreate the link (cmd):
`mklink /J "<mod folder>\eotg_test_frontier_vanilla" "<repo>\docs\test_submods\frontier_vanilla"`, with
`mod/eotg_test_frontier_vanilla.mod` holding this descriptor plus `path="<that folder>"`.
Playset: **Echoes of the Grip**, then this sub-mod. **Not** the EotG Test Map (that replaces the vanilla map).
It only runs on a new game (on_game_start), not on a loaded save.
