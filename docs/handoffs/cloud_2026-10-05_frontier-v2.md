### HANDOFF (cloud session; Frontier Systems Phase 2, not run in game, DO NOT MERGE)
- **branch:** `claude/frontier-v2-cloud`, from `origin/v2-space-map` @ `3c0686c`. **Not merged**, as the owner asked. The local session verifies first (Tiger, PX, vanilla-scout on spec §15, a lore pass), then the owner reviews.
- **commits:**
  - `d998734` Phase 2 A (A1–A6), with the spec and the test plan;
  - `6b1a4d9` expansion B1;
  - `6589ed8` expansion B2;
  - `19a9744` expansion B3;
  - this handoff.

  Each B commit can be reverted on its own.
- **spec:** `docs/specs/frontier_v2.md`. **test plan:** `docs/specs/frontier_v2_test_plan.md`. Phase 1's spec, rulings and owner decisions are unchanged and still bind.

## Validation (sandbox)
- **eotg_lint:** `total: 0 finding(s), 0 new (vs baseline)`. That covers L001–L016, including L011 (they/them), L013b (Canadian spelling) and L016 (one BOM).
- **check_all:** `summary: 13 pass, 0 fail, 7 skipped` (the 7 are local-only: Tiger, PX, VS Code, and interactive qa scripts).
- **spec_conformance:** frontier_v2 shows **0 missing**; every id in the spec is in script. The report covers 28 specs, 26 built, 0 missing ids in built specs.
- **gen_test_recipes:** regenerated (194 events). The rows for .020–.037 are usable: each names `scope:eotg_frontier_county` and the setup line. Each new flavor event also re-derives its own scopes in `immediate`, so the one console line in test plan §0 fires any of them.
- **Files:** all 10 Frontier files parse with no errors and hold exactly one BOM, at byte 0. Every write went through `docs/tools/textio.py`.
- **Ungated options:** every new event has at least one option with no trigger, and it guards its own effects.
- **No map keys:** a grep for `title:`, `province:`, `culture:`, `faith:` and `eotg_aug` in Frontier script finds nothing.

## Summary by section

**A1. Project types made distinct** (spec §6). Still one engine with data rows keyed on the type.
- **Requirements:** Military costs minor prestige, Religious minor piety. Research needs decent learning in you or the founder candidate. Administrative's Low Control line is 50, not 40.
- **Inputs:** a new `eotg_frontier_type_input_value`, each row from a normal CK3 source:
  - Settlement: control ≥ 60;
  - Trade: the backer's payment;
  - Mining: development;
  - Military: the holder's martial;
  - Religious: the holder's piety level;
  - Administrative: the holder's stewardship.
- **Military** takes no War strain.
- **Results:** see A6.

**A2. Infrastructure** (spec §4). 8 county modifiers: Habitat, Orbital Station, Navigation Beacon, Trade Station, Mining Complex, Research Facility, Mission, Garrison Post.
- **Why not buildings:** vanilla buildings need an icon, a 3D asset and an illustration, which is `gfx/` work.
- **Building:** a new decision, *Build Frontier Infrastructure*, leads to .021 *What to Build*. Each piece costs medium gold. One slot at the start, two from Foothold, one build a year.
- **Effect while a Frontier:** +1 yearly input each (+3 where it fits the type). Three counter a bad trait: Orbital Station → Hostile, Beacon → Remote, Garrison Post → Dangerous.
- **On settling:** each turns into development, control or a 25-year legacy.
- **On abandonment:** lost (but see B2).

**A3. Traits** (spec §5). 10 county modifiers: Rich Resources, Valuable Trade Route, Strategic Location, Habitable, Ancient Ruins, Ancient Infrastructure, Anomalous, Hostile Environment, Remote, Dangerous.
- **Limits:** at most 2 per Region; Habitable and Hostile exclude each other.
- **What they change:** speed (`eotg_frontier_trait_rate_value`), floors (Strategic +10 control, Remote −10, Ancient Infrastructure −1 development), risk, rewards on settling, and event weights.
- **Risk:**
  - **Dangerous** adds a new named strain cause, **Danger**, while control is below 60. .005 names it.
  - **Hostile** stops a quiet year from easing strain.
  - Strain is still never a dice roll.
- **Persistence:** traits survive abandonment (knowledge of the place) and are removed on settling, after their value is paid out.

**A4. Discoveries** (spec §8).
- **Survey:** a new decision, *Survey a Region* (minor gold; once per Region per 5 years), leads to .020 *Survey Report*, which reveals a trait.
  - **Before a project:** the filed report is a head start (+5) for the next project.
  - **During a project:** progress +2.
  - "Send them deeper" pays again for a second trait.
- **Establish** reveals one trait when nothing is known yet.
- **Exploration hook:** the public `eotg_frontier_reveal_trait_effect` (callable on any county) and the new hook `eotg_frontier_on_discovery` (with `scope:eotg_frontier_discovered` = the trait's flag). Exploration itself is not built.

**A5. Events** (spec §9). Seven flavor events (.030–.036) share Phase 1's one roll: the same 50% chance in an eligible year and the same 3-year cooldown, now from a weighted pool that reads traits and infrastructure.
- **Budget:** a typical project still sees about **5 prompts in total**, inside the 4–6 budget.
- **LAW AT 866:**
  - In .031 the backer asks for a say. No option gives one, and each option's tooltip says so.
  - In .032, the "local ruler" who demands concessions is the settlers or the holder's own liege, both inside the realm.

**A6. Better settlement outcomes** (spec §7). After the type row and before the settle step, `eotg_frontier_settle_rewards_effect` turns traits and infrastructure into normal CK3 results:
- **Development:** +1 per source, at most +3.
- **Control:** +10 from an Orbital Station.
- **25-year legacies:** Trade, Industry, Defence, Learning, Faith (only modifier keys already in use).
- **Characters:** Military gets a garrison commander, Religious a mission elder, Administrative a Region official, each with the holder's culture and faith by scope.

**B. Expansion** (spec §B; separate commits, accept or drop each):
- **B1 (`6b1a4d9`):** .002's complication names an uncountered bad trait, and .004 names what the Frontier leaves behind. Desc lines only.
- **B2 (`6589ed8`):** salvage. An abandoned Region records its lost infrastructure, and the next project starts 5 ahead per piece. .001 says so.
- **B3 (`19a9744`):** .037 *What the Ruins Held*, one to two years after choosing to study ruins in .035. It adds a prompt only after that choice.

## New events
| ID | Title | Fired by |
|---|---|---|
| `eotg_frontier.020` | Survey Report | decision Survey a Region |
| `eotg_frontier.021` | What to Build | decision Build Frontier Infrastructure |
| `eotg_frontier.030` | A Rival Backer | the yearly roll (pool) |
| `eotg_frontier.031` | The Backer Wants a Say | the yearly roll |
| `eotg_frontier.032` | Terms Demanded | the yearly roll |
| `eotg_frontier.033` | A Quarrel in the Camps | the yearly roll |
| `eotg_frontier.034` | A Supply Run Lost | the yearly roll |
| `eotg_frontier.035` | What the Crews Found | the yearly roll |
| `eotg_frontier.036` | A Rich Seam | the yearly roll |
| `eotg_frontier.037` | What the Ruins Held (B3) | .035 option a, after 365–730 days |

Phase 1 events changed:
- **.001:** type requirements, AI chances that follow the known traits, and the `desc_known` and `desc_salvage` (B2) lines.
- **.002:** trait lines (B1).
- **.004:** legacy lines (B1).
- **.005:** `desc_danger`.

## Loc
- **Phase 2 A:** **153 new keys** (149 → 302).
- **Expansion:** +13 (B1 6, B2 1, B3 6).
- **Total:** **315** in `eotg_frontier_l_english.yml`.

Canadian English, gendered pronouns, no dashes. No Void, charter, "human", era or named power. The cybernetics never-name list was checked by hand.

## UNVERIFIED-VANILLA (spec §15; marked in script)
1. `piety_level >= n` as a character trigger. `eotg_frontier_type_input_value`, Religious row.
2. `county_opinion_add` in a static county modifier. `eotg_frontier_mod_legacy_faith` and `eotg_frontier_mod_concessions`; the mod's buildings use the key inside their county modifier.
3. `add_county_modifier = $TRAIT$` with a whole-token parameter. Low risk: Phase 1's `HOOK = $HOOK$` and `flag:$TYPE$` are the precedent.
4. **TEST-IN-GAME:** a county modifier added to an Unsettled Region survives a holder change.
5. **The one most worth checking:** a script value on the **left** of a trigger comparison (`eotg_frontier_trait_count_value < eotg_frontier_trait_max_value` and similar). Phase 1 only put script values on the right.
   - **Where:** marked in `eotg_frontier_triggers.txt`.
   - **Fallback:** `calc_true_if`, or a count variable.
6. `change_development_level = <script value>` (`eotg_frontier_settle_rewards_effect`).

Engine use that has a precedent in the mod's verified script, so it is not flagged:
- `random_list` entries with `modifier = { add }`;
- `save_scope_value_as` with a flag;
- `add_opinion … years`;
- `minor_piety_value`, `minor_prestige_value`, `decent_skill_rating`;
- `create_character` with a template.

## Questions for the owner (spec §16)
- **Q2-1. Traits after settling:** removed (as built: the Frontier is temporary, and their value is paid out as results), or kept as permanent descriptors on the Region?
- **Q2-2. Infrastructure cost:** medium gold each, at most two. Too cheap, or too dear?
- **Q2-3. Negative reveals:** about 30% of reveals are bad news (Hostile, Remote, Dangerous). Keep that rate, or weight reveals toward good news?
- **Q2-4. Type costs:** Military costs minor prestige and Religious minor piety to start. Keep, or switch to gold like the other types?
- **Q2-5. .032's liege variant:** a vassal's liege asks for a share of the vassal's Frontier. Keep it, or make .032 settlers-only?
- **Q2-6. New courtiers:** three new types of courtier on completion (commander, elder, official). Keep them, or only Settlement's leader, as in Phase 1?
- **Expansion:** accept or drop B1, B2 and B3 individually.

## Test-plan additions
`docs/specs/frontier_v2_test_plan.md`, usable on the test map (`c_emberscar`, `c_reogladra`, `c_warpmire` and `c_muth` have empty Systems).

| Section | Covers |
|---|---|
| §0 | a console line that fires any new event on any Region, and one that clears the cooldown |
| §1 | traits: survey, establish, exclusivity, each effect, persistence |
| §2 | infrastructure: offers, limits, speed, loss |
| §3 | type requirements and inputs |
| §4 | settling results |
| §5 | one row per new event |
| §6 | hooks |
| §7 | AI |
| §8 | throughout checks |
| §9 | the expansion |

## needs
- **eotg-vanilla-scout:** spec §15 items 1–3, 5 and 6.
- **eotg-qa:** Tiger and PX on the `eotg_frontier_*` files.
- **eotg-lore-keeper:** the Phase 2 loc. Points to check:
  - the ruins and anomaly lines (no Void, ruins never dated);
  - .031 against LAW AT 866;
  - the "Frontier Legacy" names.
- **owner:** the Q2 questions, then the test plan.
