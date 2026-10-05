# Frontier Systems v1: in-game test checklist

**For:** the owner, playing the vanilla map with only Echoes of the Grip enabled.

**Setup:** follow [`docs/qa/HOW_TO_TEST_IN_GAME.md`](../qa/HOW_TO_TEST_IN_GAME.md) §1 (one playset, restart after the batch is committed). Console conventions are its §2.
- **Debug mode is required.** Every `(Debug)` decision here is gated by `debug_only = yes` and shows **only** when the game runs with `-debug_mode` (verification E4).

**Why the recipes are hand-written:** every Frontier event needs `scope:eotg_frontier_county`, which the console can't supply. You drive the system with the debug decisions plus a few console lines, and the events arrive on their own.
- `docs/qa/generated/console_recipes.md` lists the Frontier events too once tools round 5 is merged. Its lines show `<county>` where you type `capital_county` or `title:<c_key>`.

**What to look at.** The stage modifier on the Region (hover the county):
- `Unsettled Region`: marked, nothing started;
- `Frontier: Outpost`, `Frontier: Foothold`, `Frontier: Nearly Settled`: the three stages;
- `Frontier: Waiting on Development` / `Waiting on Control`: full progress, but a completion floor is unmet;
- `New Settlement`: completed;
- `Abandoned Works`: given up.

**The hidden numbers:** take **(Debug) Frontier Readout**. It shows a toast per Frontier you hold, with progress (/100), strain (/8), and development and control against their completion floors. The toast ends "Floors met." or "Waiting on a floor."

**Pacing (owner decision):** about 10–16 years to Settled unsponsored, 8–10 sponsored. Strain fails a project at 8. Flavor events come at most once every **3 years** per Region (about 4–5 per project at most); to see one sooner, clear the cooldown as in §4 step 1.

Console lines below use `capital_county`, your capital Region. For another Region, replace `capital_county` with `title:<county key>`. Vanilla keys are fine at the console; they are never in script.

---

## 0. Engine checks that decide the architecture (TEST-IN-GAME)
Do these first. If any fails, stop and report it.

### 0.1 A county variable survives save, reload and a holder change (V1)
If this fails, the state store moves to a story cycle.
1. Take **(Debug) Mark Capital Region Unsettled**. The capital Region shows `Unsettled Region`.
2. Take **Establish a Frontier** and pick any type in *An Opportunity Here*. The Region shows `Frontier: Outpost`.
3. **Save, quit to menu, reload.** It still shows `Frontier: Outpost`; the **Readout** shows the same numbers as before.
4. **Kill the founder FIRST** (verification test-plan fix: do it before the grant).
   - Hover them for their id, then `kill <id>`.
   - If `kill` isn't available: `effect = { character:<id> = { death = { death_reason = death_murder } } }`.
5. **Now change the holder:** grant the Region to a vassal with the normal Grant Title interaction. The modifier stays on the Region.
6. Let the year end (the debug year is the holder's decision, so it isn't yours any more). The Frontier is still there, and its strain rose by one (No Founder). The new holder's Readout shows it; or re-grant the Region to yourself and take the Readout.
7. **Report:** did the Frontier survive steps 3–6?

**Founder rule** (verification Q3): granting the Region away does **not** invalidate a living founder who granted it. The new holder is their vassal, so the founder stays valid. To see that, repeat step 5 without step 4: no strain is added.

### 0.2 Building a holding in an empty slot (V8)
1. Pick a Region that has a free holding slot. Mark it, and establish a **Settlement**, **Trade**, **Military** or **Religious** Frontier.
2. Force completion (§2.2).
3. **Report:**
   - Does a new Port, Bastion or Sanctum appear in a free slot?
   - Is it held by the Region's holder?
   - If no holding appears, does the Region get +1 development and +10 control instead?

### 0.3 Scopes reach the custom hooks (V12)
Nothing in Frontier listens to the hooks yet, so there is nothing visible to check. Send any `error.log` line that mentions `eotg_frontier_on_` (an unset scope there means the hooks need their empty-effect fallback).

---

## 1. Start every type (7)
**One Region at a time.** The debug decision marks only your **capital** Region, and only while it has no Frontier state. **Finish or abandon one Region before marking the next.**

To mark any other Region (one you hold), use: `effect title:<c_key> = { eotg_frontier_mark_unsettled_effect = yes }`.

For each type: mark a fresh Region Unsettled, Establish, and pick that option in .001.
- **The founder:** when a courtier out-stewards you, *An Opportunity Here* names them. Otherwise it says you looked over the surveys yourself.
- **The Administrative option** ("Bring it into proper order") appears only if you are a duke or above, or the Region isn't your capital Region.
- **"Not now"** costs nothing, and the Region stays Unsettled.
- **Check:** the cost (a medium amount of gold) is taken when a type is picked; the Region shows `Frontier: Outpost`.
- **Double-start guard:** take Establish twice before answering the first event. The second event's type options are hidden once the Region has started.

## 2. Progress and completion
1. Run **(Debug) Run the Frontier Year** several times, checking the Readout. Progress rises about 6–13 a year.
   - The stage moves Outpost → Foothold → Nearly Settled, and the Region gains development at the first two stage changes, **once per Region ever**.
   - A resettled Region that already got its milestone development gets none again.
2. **To force completion:**
   - `effect capital_county = { set_variable = { name = eotg_frontier_progress value = 100 } }`
   - **(Debug) Run the Frontier Year**.
   - If the stage becomes `Waiting on Development` or `Waiting on Control`, the Readout shows which floor is missing. Raise it: `effect capital_county = { change_development_level = 3 }` or `effect capital_county = { change_county_control = 100 }`. Then run the year again.
   - The development floor is never more than the Region's development at start plus the milestone development still to come.
3. **Check:**
   - *No Longer a Frontier* appears, with the type's line.
   - The options reward the founder: pay them well, or honor them publicly. Neither appears when you are the founder.
   - Afterwards: `New Settlement` replaces the stage modifier; no Frontier decision shows for this Region; Establish isn't offered there again.
4. **Holdings:** see §0.2. **The new System is the current holder's, never the founder's.**
5. **Settlement** also adds a settlers' leader to your court. **Research** gives the founder +1 learning. **Administrative** sets control to 100.

## 3. Strain, failure, abandonment
1. **Strain causes:** each adds one point in a yearly tick (watch it in the Readout). A year with none removes one.
   - **War:** be at war.
   - **Low Control:** `effect capital_county = { change_county_control = -100 }`.
   - **No Founder:** imprison or kill the founder.
   - **Occupation:** let an enemy occupy the capital.
   - **Sponsor Lapse:** §4.
2. **To force failure:**
   - `effect capital_county = { set_variable = { name = eotg_frontier_strain value = 8 } }`, with at least one cause present (e.g. kill the founder). A quiet year would ease it back down.
   - **(Debug) Run the Frontier Year**.
   - *The Frontier Falters* appears, and its text names the cause.
3. **The four branches:**
   - **Let it go:** the Region shows `Abandoned Works` and loses one development if the Frontier had reached Foothold.
   - **New hands:** costs a small amount of gold; half the progress stays; strain drops to 4.
   - **Scale it back:** not shown for Settlement; the type becomes Settlement.
   - **Call on our backer:** only with a backer who can pay double; strain drops to 2.
4. **Abandon decision:** **Abandon a Frontier** abandons your most troubled Frontier at once.
5. **Left open:** with *The Frontier Falters* open, take **Abandon a Frontier**. The open event now offers only "The moment has passed", and nothing happens twice.
6. **Resettle:**
   - Establish again on the abandoned Region. *An Opportunity Here* mentions the earlier attempt.
   - The new Frontier starts with a head start (Readout: progress 10 per earlier attempt, up to 30).

## 4. Founder and sponsor
1. **Founder gone** (ruling Q2: no death event): with the founder dead or imprisoned, clear the event cooldown with `effect capital_county = { remove_variable = eotg_frontier_event_cd }`, then run the debug year.
   - *The Frontier Without a Founder* offers: appoint a courtier, lead it yourself, or let them manage. "Push through" is offered too: it is each event's ungated fallback (error.log, first launch), so the event can never open with nothing to pick.
   - **Fallbacks:** in every Frontier event at least one option has no trigger. With an event left open after the Region stopped being a Frontier, "Push through" (.002) or "The work is its own reward" (.004) does nothing; "The moment has passed" shows as well.
   - Strain keeps building until someone is appointed.
2. **A backer offers (AI → you).** The offer comes from your **liege** or an **ally** who is AI, holds a county or more, has gold for four payments, and backs no other Frontier.
   - **Setup:** be a vassal, then `effect liege = { add_gold = 3000 }`. Or have an ally and give them gold the same way through `character:<id>`.
   - Clear the cooldown (step 1), then run the debug year a few times.
   - *An Offer of Backing* says the backer shares the credit if it succeeds, and the loss if it fails. Accepting raises progress a little, and the backer pays every year.
3. **You back someone (you → AI):**
   - Make an AI Region a Frontier from the console:
     - `effect title:<c_key> = { eotg_frontier_mark_unsettled_effect = yes }`
     - `effect title:<c_key> = { eotg_frontier_start_effect = { TYPE = trade FOUNDER = title:<c_key>.holder } }`
   - Take **Back a Frontier** → *Whom to Back* lists it with its stage in words → the AI holder answers.
   - Afterwards **Withdraw Your Backing** appears; taking it ends the backing.
4. **The backer dies:** kill the sponsor. Nothing shows at the moment of death (the backing is cleared; the heir is noted on the Region).
   - **At the next year** (run the debug year): if their primary heir is alive, landed, has gold, backs nothing and does not hold the Region, the heir carries the backing, and a toast says so.
   - **Otherwise:** the backing lapses at that year (toast, strain +1).
   - **Heir holds the Region** (e.g. you hold the Region and the backer was your parent, with you as primary heir): no backer and **no** strain.
   - **Sponsor becomes the holder:** grant the Frontier Region to its backer, then run the year. The backing ends with no strain.
5. **Owner change:** grant a Frontier Region to a vassal. The Frontier continues under them, with the founder and backer unchanged. **Exactly one tick per calendar year:** note the progress (Readout), grant the Region away mid-year, let the year turn, re-grant it, and read again. Progress rose by one year's gain, not two. (The debug year ignores this marker on purpose, so use natural time here.)

## 5. AI (let it run 10+ years, observer if wanted)
- Mark several AI Regions Unsettled from the console (§4 step 3, first line).
- **Expect:**
  - at most 8 active Frontiers on the map;
  - no AI ruler with more than one;
  - some AI Frontiers start, and some complete or are abandoned (slowly: the pacing is 10–16 years);
  - AI backers appear now and then.

## 6. Throughout
- **No tooltip ever shows** a progress or strain number. The debug Readout is the one exception, and it's debug-only.
- **No player text says** "barony", "holding slot", "county", "charter", "season", names a faction, or names an era.
- **error.log:** send every line containing `eotg_frontier`.
