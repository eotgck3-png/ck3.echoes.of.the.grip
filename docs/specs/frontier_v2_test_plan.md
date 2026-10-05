# Frontier Systems v2: in-game test checklist

**For:** the owner. Run Phase 1's plan (`frontier_v1_test_plan.md`) §0 first if it hasn't passed yet; everything here builds on it.

**Setup:**
- **Debug mode is required** (`-debug_mode`), as in Phase 1.
- **Test map** (`docs/test_map/README.md`): play **Duke Sveinn Wyvar** (lead 3) or any count. The best Regions to mark are ones with **empty Systems**: `c_emberscar` (Sveinn's domain), `c_reogladra` (development 3, for the floors), `c_warpmire` (3), `c_muth` (4). Avoid `c_kronos`, `c_graveshelf`, `c_skeldscar`, `c_wyveris`, which have no empty slot.
- **Vanilla map:** everything below works on your capital with the debug decisions, as in Phase 1.

**Console conventions:**
- Mark a Region: `effect title:c_emberscar = { eotg_frontier_mark_unsettled_effect = yes }`.
- Lines below use `title:c_emberscar`; use your own Region's key, or `capital_county`.
- **Fire one event on one Region** (every new event works this way; it finds its own backer, rival, founder or liege):
  `effect title:c_emberscar = { save_scope_as = eotg_frontier_county  holder = { trigger_event = eotg_frontier.030 } }`
- **Clear the flavor cooldown:** `effect title:c_emberscar = { remove_variable = eotg_frontier_event_cd }`.
- **The hidden numbers:** **(Debug) Frontier Readout**, as in Phase 1. Traits and infrastructure show as county modifiers on the Region.

---

## 0. Engine checks (TEST-IN-GAME; spec §15 item 4)
### 0.1 A county modifier survives a holder change
1. Mark a Region Unsettled and give it a trait: `effect title:c_emberscar = { add_county_modifier = eotg_frontier_trait_remote }`. Establish a Frontier there and build one piece of infrastructure.
2. **Save, quit to menu, reload.** The trait and the infrastructure modifier are still on the Region.
3. Grant the Region to a vassal (Grant Title). Hover the Region: both modifiers are still there.
4. Re-grant it to yourself (or play on), run **(Debug) Run the Frontier Year**: the Readout's progress still counts them (a Remote Region without a Beacon gains about 1 a year less).
5. **Report:** did the modifiers survive steps 2 and 3?

### 0.2 `clamp_variable` holds progress and strain in range
1. `effect title:c_emberscar = { set_variable = { name = eotg_frontier_progress value = 98 } }`, then fire .035 and choose **Strip it for parts** (+4): the Readout shows 100, not 102.
2. `effect title:c_emberscar = { set_variable = { name = eotg_frontier_strain value = 8 } }`, then fire .036 and choose **Work it now** (strain +1): the Readout shows strain 8, not 9.
3. Set progress to 1 and fire .034, choosing **Make do** (−3): progress shows 0, not −2.
4. **Report:** any value outside 0–100 (progress) or 0–8 (strain).

---

## 1. Traits (spec §5)
1. **Survey reveals a trait.** Mark a Region Unsettled, take **Survey a Region**. *Survey Report* names what was found, and the Region shows the trait modifier (e.g. `Remote`).
   - **File the report:** the Region now has survey data. Establish there: the Readout shows progress 5 at the start (10 more per earlier abandonment).
   - **Send them deeper** (gold): a second trait, never a third (at most two).
   - Survey is not offered for that Region again for 5 years, nor once it has two traits.
2. **Establish reveals one** if nothing is known: mark a fresh Region, Establish straight away. A toast says the first expedition reported back, and one trait appears.
3. **Exclusive pair:** a Region never has both `Habitable` and `Hostile Environment`.
4. **Give a trait directly** (to test its effect): `effect title:c_emberscar = { add_county_modifier = eotg_frontier_trait_dangerous }` (any `eotg_frontier_trait_*`).
5. **Effects** (Readout, then **(Debug) Run the Frontier Year**):
   - **Speed:** a Rich Resources Mining project gains about 1.5 a year more than without; Hostile or Remote, about 1 a year less.
   - **Requirements:** Strategic Location raises the control floor by 10, Remote lowers it by 10, Ancient Infrastructure lowers the development floor by 1 (the Readout shows the floors).
   - **Dangerous:** with control below the project's own control floor (the Readout shows it; `effect title:c_emberscar = { change_county_control = -100 }`), each year adds strain; at or above the floor, it doesn't; .005 then names the cause ("The Region was never safe..."). A Garrison Post, or a Military project, stops it.
   - **Hostile Environment:** a year with no strain cause no longer eases strain. An Orbital Station restores that.
6. **Abandon keeps the traits:** abandon the Frontier; the trait modifiers stay on the Region.

## 2. Infrastructure (spec §4)
1. In a Frontier, take **Build Frontier Infrastructure**. *What to Build* lists only what fits: Habitat, Orbital Station and Navigation Beacon always; Trade Station for Trade or a Valuable Trade Route; Mining Complex for Mining or Rich Resources; Research Facility for Research, Anomalous or Ancient Ruins; Mission for Religious; Garrison Post for Military, Strategic Location or Dangerous.
2. The cost (medium gold) is paid on the pick; the Region shows `Frontier ...` infrastructure modifier.
3. **Limits:** the decision is unavailable again this year for that Region; only one piece before Foothold, two from Foothold (`effect title:c_emberscar = { set_variable = { name = eotg_frontier_progress value = 40 } }`).
4. **Speed:** each piece adds about 0.5 a year, a fitting one about 1.5 (Readout before and after a debug year).
5. **Abandon loses it:** the infrastructure modifiers go; the traits stay.

## 3. Types (spec §6)
1. **Requirements in *An Opportunity Here*:** the garrison option needs and costs a little prestige, the mission a little piety; the research option needs decent learning (vanilla's `decent_skill_rating`) in you or the founder candidate. To see it greyed out, lower both: `effect = { add_learning_skill = -20 }` for you, and the same on the candidate through `character:<id>`.
2. **Military ignores war:** start a Military Frontier, declare a war; no War strain (Readout). Any other type takes it.
3. **Administrative's Low Control line is 50:** an Administrative Frontier at control 45 takes Low Control strain; a Settlement at 45 doesn't.
4. **Inputs:** a Settlement at control ≥ 60, a Trade project with a paying backer, a Mining project at high development, a Military holder with high martial, a Religious holder with piety, an Administrative holder with high stewardship each gain a little more a year.

## 4. Settling (spec §7)
1. Force completion as in Phase 1 §2.2 (progress 100, floors met, a debug year). Before that, give the Region a trait and two pieces of infrastructure.
2. **Check after *No Longer a Frontier*:**
   - every `eotg_frontier_trait_*` and `eotg_frontier_infra_*` modifier is gone;
   - the matching legacy is there for 25 years (`Frontier Legacy: Trade / Industry / Defence / Learning / Faith`);
   - extra development from Habitat, Navigation Beacon, Habitable, Rich Resources or Ancient Infrastructure (at most +3); +10 control from an Orbital Station;
   - **Military:** a new commander at your court; **Religious:** a mission elder; **Administrative:** a Region official; **Settlement:** the settlers' leader (Phase 1). Each has your culture and faith.

## 5. Events (spec §9)
Fire each with the console line above, on a Frontier that meets its conditions:

| Event | Needs | Check |
|---|---|---|
| .030 *A Rival Backer* | a backer, and a liege or ally who could back it | **Take the new terms:** the rival backs it, the old backer's opinion of you drops ("Dropped as a Frontier's Backer") and gets a toast. **Keep faith:** opinion up, strain −1 |
| .031 *The Backer Wants a Say* | a backer who is not you | no option gives the backer a say; each says so in its tooltip. **The Region is mine:** opinion down, strain +1 |
| .032 *Terms Demanded* | a Frontier from Foothold | **as a count under a liege:** the liege's variant (pay the share, or refuse and be resented; with diplomacy, *Talk him round* or *Talk her round*); **as an independent ruler:** the settlers' variant (grant: `Settlers' Terms` for 10 years) |
| .033 *A Quarrel in the Camps* | a founder who is not you | **Back the founder:** progress +3, strain +1. **Side with the settlers:** strain −1, progress −2, the founder resents it |
| .034 *A Supply Run Lost* | — | the desc adds a line for Remote or Dangerous |
| .035 *What the Crews Found* | trait room | **without known ruins:** ruins; study them → `Ancient Ruins`. **With known ruins:** a derelict; restore it → `Ancient Infrastructure`. **Strip it:** progress +4, no trait |
| .036 *A Rich Seam* | trait room, no Rich Resources yet | **Survey it** → `Rich Resources`, progress +2. **Work it now:** progress +4, strain +1 |

- **Every event has an option you can always click**, including when fired on a Region that is no longer a Frontier (which then does nothing).
- **Natural frequency:** leave a Frontier running 15 years (no console). Expect about 3 flavor events, never two within 3 years of each other.

## 6. Hooks (spec §10)
Nothing listens to them yet. Send any `error.log` line mentioning `eotg_frontier_on_discovery` or `eotg_frontier_on_infrastructure_built`.

## 7. AI (10+ years, observer if wanted)
- Mark several AI Regions Unsettled. **Expect:** some AI surveys, some AI infrastructure (more often where it counters a bad trait), traits appearing on AI Frontiers, and AI completions with the new results. Still at most 8 active Frontiers.

## 8. Throughout
- **No number** in any Phase 2 tooltip or desc.
- **No player text** says "barony", "holding slot", "county", "charter", "season", names a faction, an era, or the Void.
- **Canadian spelling** (colour, honour, defence, travelled).
- **error.log:** send every line containing `eotg_frontier`, especially from the Phase 2 lines marked `UNVERIFIED-VANILLA` (spec §15): `piety_level`, `county_opinion_add`, the script-value comparisons in `eotg_frontier_triggers.txt`, and `change_development_level` with a script value.

## 9. Expansion (spec §B; each part can be dropped on its own)
- **B1:** with a Hostile, Remote or Dangerous trait and no counter, *A Hard Year* adds a line about it. *No Longer a Frontier* adds a line for two pieces of infrastructure, studied ruins or anomalies, or a hard Region.
- **B3:** fire .035 on a Region without known ruins and choose **Study them properly**. One to two years later (or speed up time), *What the Ruins Held* arrives if the Region is still a Frontier. Both options raise progress; sharing also gives prestige.
- **B2 salvage:** build infrastructure in a Frontier, then **Abandon a Frontier**. Establish there again: *An Opportunity Here* mentions what is still standing, and the Readout shows 5 more progress per piece left behind (on top of the 10 per earlier attempt).
