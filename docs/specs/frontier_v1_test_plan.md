# Frontier Systems v1: in-game test checklist

**For:** the owner, playing the vanilla map with only Echoes of the Grip enabled.
**Setup:** follow [`docs/qa/HOW_TO_TEST_IN_GAME.md`](../qa/HOW_TO_TEST_IN_GAME.md) §1 (debug mode, one playset, restart after the batch is committed). Console conventions are its §2.
**Why this is hand-written:** `gen_test_recipes.py` can't produce usable Frontier recipes. Every Frontier event needs `scope:eotg_frontier_county`, which the console can't supply. So you drive the system with the two debug decisions plus a few console lines, and the events arrive on their own.

**What to look at:** the Region's modifiers (hover the county). Progress and strain are hidden by design, so the stage modifier is the readout:
- `Unsettled Region`: marked, nothing started;
- `Frontier: Outpost`, `Frontier: Foothold`, `Frontier: Nearly Settled`: the three stages;
- `New Settlement`: completed;
- `Abandoned Works`: given up.

Console lines below use `capital_county`, your capital Region. For another Region, replace `capital_county` with `title:<county key>`. Vanilla keys are fine at the console; they are never in script.

---

## 0. The engine check that decides the architecture (spec §16 V1, owner's test)
Do this first. If any step fails, stop and report it: the state store then moves to a story cycle.
1. Take **(Debug) Mark Capital Region Unsettled**. The capital Region shows `Unsettled Region`.
2. Take **Establish a Frontier** and pick any type in *An Opportunity Here*. The Region shows `Frontier: Outpost`.
3. **Save, quit to menu, reload.** It still shows `Frontier: Outpost`.
4. **Change the holder:** grant the Region to a vassal with the normal Grant Title interaction. The modifier stays on the Region.
5. **Kill the founder.** Hover them for their id, then `kill <id>`. If that isn't available: `effect = { character:<id> = { death = { death_reason = death_murder } } }`. Then have the Region's holder take **(Debug) Run the Frontier Year** (or let a year pass). The Frontier is still there; the founder now counts as missing (§4).
6. **Report:** did the Frontier survive steps 3–5?

## 1. Start every type (7)
For each type: mark a fresh Region Unsettled, Establish, and pick that option in .001.
- **The Administrative option** ("Bring it into proper order") appears only if you are a duke or above, or the Region isn't your capital Region.
- **"Not now"** costs nothing, and the Region stays Unsettled.
- **Check:** the cost (a medium amount of gold) is taken when a type is picked; the Region shows `Frontier: Outpost`.

## 2. Progress and completion
1. Run **(Debug) Run the Frontier Year** a few times. The stage moves Outpost → Foothold → Nearly Settled, and the Region gains development at the first two stage changes.
2. **To force completion:**
   - `effect capital_county = { set_variable = { name = eotg_frontier_progress value = 100 } }`
   - `effect capital_county = { change_development_level = 3 change_county_control = 100 }` (the type's floors)
   - **(Debug) Run the Frontier Year**
3. **Check:**
   - *No Longer a Frontier* appears, with the type's line.
   - The options reward the founder: a purse or public honor. Neither appears when you are the founder.
   - Afterwards: `New Settlement` replaces the stage modifier; no Frontier decision shows for this Region; Establish isn't offered there again.
4. **Holdings** (spec §5.3):
   - Settlement and Trade add a **Port**, Military a **Bastion**, Religious a **Sanctum**, in a free slot of the Region. **The new System is yours, the current holder's, never the founder's.**
   - With no free slot, the Region gains development and control instead.
   - **Report whether a holding was created**, and who holds the new System (spec §16 V8).
5. **Settlement** also adds a settlers' leader to your court. **Research** gives the founder +1 learning. **Administrative** sets control to 100.

## 3. Strain, failure, abandonment
1. **Strain causes:** each adds pressure in a yearly tick.
   - **War:** be at war.
   - **Low Control:** `effect capital_county = { change_county_control = -100 }`.
   - **No Founder:** imprison or kill the founder.
   - **Occupation:** let an enemy occupy the capital.
   - **Sponsor Lapse:** §4.
2. **To force failure:**
   - `effect capital_county = { set_variable = { name = eotg_frontier_strain value = 4 } }`, with at least one cause present (e.g. kill the founder). A quiet year would ease it back down.
   - **(Debug) Run the Frontier Year**.
   - *The Frontier Falters* appears, and its text names the cause.
3. **The four branches:**
   - **Let it go:** the Region shows `Abandoned Works` and loses one development if the Frontier had reached Foothold.
   - **New hands:** costs a small amount of gold; the stage may drop.
   - **Scale it back:** not shown for Settlement; the type becomes Settlement.
   - **Ask our backer for more:** only with a backer who can pay double.
4. **Abandon decision:** **Abandon a Frontier** abandons your most troubled Frontier at once.
5. **Resettle:**
   - Establish again on the abandoned Region. *An Opportunity Here* mentions the earlier attempt.
   - The new Frontier starts with a head start: it reaches Foothold sooner.
   - Each abandonment adds to the head start, up to three.

## 4. Founder and sponsor
1. **Founder gone** (ruling Q2: no death event): with the founder dead or imprisoned, clear the event cooldown with `effect capital_county = { remove_variable = eotg_frontier_event_cd }`, then run the debug year.
   - *The Frontier Without a Founder* offers: appoint a courtier, lead it yourself, or let them manage.
   - Strain keeps building until someone is appointed.
2. **A backer offers (AI → you):** let years pass, or clear the cooldown and run the debug year a few times. *An Offer of Backing* comes from your liege or an ally. Accepting shows a jump in the stage. The backer pays every year.
3. **You back someone (you → AI):**
   - Make an AI Region a Frontier from the console:
     - `effect title:<c_key> = { eotg_frontier_mark_unsettled_effect = yes }`
     - `effect title:<c_key> = { eotg_frontier_start_effect = { TYPE = trade FOUNDER = title:<c_key>.holder } }`
   - Take **Back a Frontier** → *Whom to Back* lists it → the AI holder answers.
   - Afterwards **Withdraw Your Backing** appears; taking it ends the backing.
4. **The backer dies:** kill the sponsor, then run the debug year (as the Region's holder). If their heir is landed and has gold, the heir carries the backing (a toast says so). Otherwise the backing lapses (toast, more strain).
5. **Owner change:** grant a Frontier Region to a vassal. The Frontier continues under them, with the founder and backer unchanged. It is not ticked twice that year.

## 5. AI (let it run 10+ years, observer if wanted)
- Mark several AI Regions Unsettled from the console (§4 step 3, first line).
- **Expect:**
  - at most 8 active Frontiers on the map;
  - no AI ruler with more than one;
  - some AI Frontiers start, and some complete or are abandoned;
  - AI backers appear now and then.

## 6. Throughout
- **No tooltip ever shows** a progress or strain number.
- **No player text says** "barony", "holding slot", "county", "charter", or names a faction.
- **error.log:** send every line containing `eotg_frontier`. Unknown-effect or unknown-trigger errors there answer the spec §16 verification list directly.
