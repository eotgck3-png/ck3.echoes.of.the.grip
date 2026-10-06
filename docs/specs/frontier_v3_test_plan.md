# Frontier Systems v3 (Phase 3a): in-game test checklist

**For:** the owner. Phases 1 and 2 first (`frontier_v1_test_plan.md` §0, `frontier_v2_test_plan.md` §0). Everything here builds on them.

**Two ways to play it (both work):**
- **Test map** (`docs/test_map/README.md`): play **Duke Sveinn Wyvar** (lead 3). Regions with empty Systems: `c_emberscar` (his domain), `c_reogladra`, `c_warpmire`, `c_muth`. Mark Regions from the console (below).
- **Vanilla map** with the sub-mod `docs/test_submods/frontier_vanilla` (Corsica and Sardinia). On a new game it marks 8 counties Unsettled, and now **two of them Unknown**: `c_vecchio` (Corsica) and `c_tortoli` (Sardinia). Play their holder, or any count, and use the console on any of the 8.

**Setup:** `-debug_mode`, as in Phases 1 and 2.

**Console conventions** (the key below is `c_emberscar`; on the vanilla map use `c_vecchio`, `c_tortoli` or another of the 8):
- Mark Unsettled: `effect title:c_emberscar = { eotg_frontier_mark_unsettled_effect = yes }`
- **Mark Unknown:** `effect title:c_emberscar = { eotg_frontier_mark_unknown_effect = yes }` (or the debug decision **(Debug) Mark Capital Region Unknown** for your capital)
- **Fire an event on a Region:** `effect title:c_emberscar = { save_scope_as = eotg_frontier_county  holder = { trigger_event = eotg_frontier.040 } }` (.041 the same). Each finds its own captain or faith backer.
- **Give a trait:** `effect title:c_emberscar = { add_county_modifier = eotg_frontier_trait_dangerous }`
- **Set the type** of a running Frontier: `effect title:c_emberscar = { set_variable = { name = eotg_frontier_type value = flag:military } }`
- **The hidden numbers:** **(Debug) Frontier Readout**.

---

## 0. Engine checks (spec §15)
### 0.1 The exploration variable persists (TEST-IN-GAME, §15 7)
1. Mark a Region Unknown. Hover it: `Unexplored Region`.
2. Save, quit, reload: still `Unexplored Region`.
3. Grant it to a vassal and back: still there.
4. **Report** if it vanished.

### 0.2 Finding captains and faith leaders (§15 1–5)
1. On a Military Frontier, fire .040. **Report:** does *Blades for Hire* show a captain's portrait and name? (If the right portrait is empty, no captain was found: send the `error.log` lines with `eotg_frontier_find_company_effect` or `government_is_mercenary`.)
2. On a Religious Frontier, fire .041. **Report:** does it name your head of faith (if your faith has one), or a holy order's leader? Which one? (Vanilla map, a Catholic or Orthodox count is the easy case; on the test map, the Empire's faith.)
3. Send every `error.log` line mentioning `government_is_holy_order`, `religious_head` or `random_independent_ruler`.

---

## 1. Exploration (spec §4)
1. **Unknown blocks Establish and Survey:** mark a Region Unknown (vanilla: `c_vecchio` already is). *Establish a Frontier* and *Survey a Region* don't offer it (if it is your only open Region, the decisions don't show at all).
2. **Send an Expedition** appears. Take it (minor gold).
   - *The Expedition Returns* says the Region is now partly explored; the Region shows `Partly Explored Region` and **one trait**.
   - The decision is unavailable for that Region for a year.
   - **Partial** allows Establish and Survey.
3. Next year (or `effect title:c_emberscar = { remove_variable = eotg_frontier_expedition_sent }`), take it again: the report says the Region is fully charted; `Partly Explored Region` is gone; a second trait if there was room.
   - **File the charts** at Known: the next project there starts 5 ahead (Readout).
   - **Send them straight back out** (from Partial, with gold): goes to Known in one report.
4. **Hook:** send any `error.log` line mentioning `eotg_frontier_on_explored`.
5. **Old Regions:** a Region marked only Unsettled (no Unknown) behaves exactly as in Phase 2: Establish and Survey offered, no exploration modifier.

## 2. Mercenaries (spec §5)
1. **Escort:** start a Frontier in a Region with `Dangerous`, set control low (`effect title:c_emberscar = { change_county_control = -100 }`), and run the debug year: strain rises (Danger). Fire .040, choose **Hire them to guard the convoys** (medium gold): the Region shows `Mercenary Escort`, strain −1, and the next debug years add no Danger strain. The option is gone while an escort is there.
2. **Backing (Military only, no backer):** on a Military Frontier with no backer, choose **Let the company back the venture**: the captain is the backer (hover the Region in .010's list, or check that **Withdraw** isn't yours); progress +3. Next debug year: no Sponsor Lapse while the captain has gold.
3. **Not for others:** on a Settlement Frontier without Dangerous, .040 never comes up naturally (the pool skips it); fired from the console, only **We will hold it ourselves** is clickable.
4. **Settle or abandon:** the escort modifier goes with the project.

## 3. Religious organizations (spec §6)
1. On a Religious Frontier, fire .041:
   - **Accept the backing** (no backer yet): the head of faith (or holy order leader) backs it; progress +3. The tooltip says they gain no claim, no say, no authority.
   - **Ask only for a blessing:** minor piety for you; progress +2.
   - **The mission stands on its own:** nothing.
2. **Completion:** force a Religious Frontier to complete (Phase 1 §2.2). You gain minor piety, and your faith's fervour rises a little (faith view; the fervour breakdown names "A Frontier mission became a settlement").
3. **Never names a faith:** the text says "the head of your faith" or "a holy order", never a faith or order name.

## 4. Hooks (spec §7)
1. **Trade network:** on a Trade Frontier: `effect title:c_emberscar = { eotg_frontier_set_trade_network_effect = { AMOUNT = 4 } }`. Readout, debug year: progress rises 2 more than before. On a non-Trade Frontier: no change.
2. **Corporation-style offer:** `effect title:c_emberscar = { eotg_frontier_offer_backing_effect = { SPONSOR = character:<id> } }` with a landed count's id (hover them). *An Offer of Backing* arrives for the holder, naming that character.

## 5. Throughout
- **Prompts:** let a Frontier run 15 years with no console: still about 3 flavour events (Phase 2), now sometimes *Blades for Hire* or *A Faithful Offer*.
- **No number** in any tooltip; no faith, order or company name; no "charter", season or Void; Canadian spelling.
- **error.log:** every line containing `eotg_frontier`.
