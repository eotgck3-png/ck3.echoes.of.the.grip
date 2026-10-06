# EotG Test: Frontier on Corsica and Sardinia (sub-mod)

**Test only, never shipped.** Lets you test Frontier on the **vanilla map** with the main mod's shaders and cybernetics.
At game start it marks Corsica's 3 counties Unsettled (c_ajaccio, c_bastia, c_vecchio; still owned) and **releases
Sardinia's 5 as Unclaimed Regions** (c_cagliari, c_arborea, c_gallura, c_logudoro, c_tortoli; Unclaimed Regions,
`docs/specs/frontier_unclaimed_regions.md` §11.1): each gets its own Unsworn placeholder with the county's culture and
faith, turns neutral grey, and is Unsettled. **Sardinia's 867 holders lose those counties** (those who held only
Sardinian land become unlanded). A Corsican count across the strait can claim them with *Raise Your Colours*. Two
Regions, c_vecchio and c_tortoli, also start **Unknown** (Frontier Phase 3a exploration;
`docs/specs/frontier_v3_test_plan.md`). Nothing else changes.

Install: copy this folder to `Documents/Paradox Interactive/Crusader Kings III/mod/eotg_test_frontier_vanilla`, and write
`mod/eotg_test_frontier_vanilla.mod` with this descriptor plus `path="<that folder>"`.
Playset: **Echoes of the Grip**, then this sub-mod. **Not** the EotG Test Map (that replaces the vanilla map).
It only runs on a new game (on_game_start), not on a loaded save.
