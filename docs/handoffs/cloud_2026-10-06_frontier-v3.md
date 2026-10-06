### HANDOFF (cloud session, unvalidated)
- **branch:** `claude/frontier-v3-cloud`, from `v2-space-map` @ `17c6e1a`. **Do NOT merge**: the local session verifies (Tiger, PX, eotg-vanilla-scout on spec §15, lore) and the owner reviews.
- **status:** done (static, unvalidated: no game files, Tiger or PX here).
- **summary:** Frontier Phase 3a, built additively on Phases 1–2.
  - **Exploration:** a Region state Unknown → Partial → Known (absent = Known). A new "Send an Expedition" decision and .042, and the hook `eotg_frontier_on_explored`.
  - **Mercenaries:** .040 offers an escort that counters Dangerous, or a captain as the Sponsor of a Military project.
  - **Religious organizations:** .041 offers a head of faith or a holy order as the Sponsor, or a blessing; a Religious completion adds piety and fervour.
  - **Corporations and trade:** documented hooks only, no content.
- **commits:**
  - `021360c` spec and test plan;
  - `0a9b5ee` part 1, exploration (and the vanilla sub-mod's Unknown marking);
  - `db57f3c` part 2, mercenaries;
  - `de98c89` part 3, religious organizations;
  - `b4fb354` part 4, corporation and trade hooks;
  - then this handoff.
- **files:**
  - `common/{decisions,modifiers,on_action,script_values,scripted_effects,scripted_triggers}/eotg_frontier_*`;
  - `events/eotg_frontier_events.txt`;
  - `localization/english/eotg_frontier_l_english.yml`;
  - `docs/specs/frontier_v3.md`, `docs/specs/frontier_v3_test_plan.md`;
  - `docs/test_submods/frontier_vanilla/{README.md, common/on_action/eotg_test_frontier_vanilla_on_actions.txt}`;
  - `docs/qa/generated/{console_recipes.md, spec_conformance.md}` (regenerated).
- **static checks run here:**
  - eotg_lint: `total: 0 finding(s), 0 new (vs baseline)`;
  - check_all: `summary: 14 pass, 0 fail, 7 skipped`;
  - spec_conformance: frontier_v3 has 54 ids, **0 missing**;
  - every Frontier file and the sub-mod's on_action file parse, with exactly one BOM (all writes went through `docs/tools/textio.py`);
  - no title, province, character, culture, faith or religion keys in mod script.

**Phase 1/2 identifiers changed** (spec §3.6, each additive):
| Identifier | Change |
|---|---|
| `eotg_frontier_can_establish` | Unknown guard |
| `eotg_frontier_can_survey` | Unknown guard |
| `eotg_frontier_danger_strains` | the escort counters Dangerous |
| `eotg_frontier_clear_infra_effect` | the escort ends with the project |
| `eotg_frontier_flavor_pick_effect` | two pool entries and their searches; still one roll |
| `eotg_frontier_yearly_gain_value` | the trade hook, 0 by default |
| `eotg_frontier_complete_effect` | the Religious row adds piety and fervour |

**New events** (3 of the allowed 6):
| Event | Title | Fired by |
|---|---|---|
| `eotg_frontier.040` | Blades for Hire | pool |
| `eotg_frontier.041` | A Faithful Offer | pool |
| `eotg_frontier.042` | The Expedition Returns | Send an Expedition |

Options are in spec §9. **Prompts per typical project stay at about 5**: same single roll, same 50% chance and 3-year cooldown, and .042 is player-initiated.

- **unverified-vanilla:**
  - `common/scripted_triggers/eotg_frontier_triggers.txt:272`: the mercenary company government flag is `government_is_mercenary` (§15 1).
  - `common/scripted_triggers/eotg_frontier_triggers.txt:280`: the holy order government flag is `government_is_holy_order` (§15 2).
  - `common/scripted_effects/eotg_frontier_effects.txt:1410`: `random_independent_ruler` reaches mercenary captains (§15 3).
  - `common/scripted_effects/eotg_frontier_effects.txt:1429`: `faith.religious_head` with `exists`; `random_independent_ruler` reaches holy order leaders; `faith = scope:x.faith` (§15 3–5).
  - `events/eotg_frontier_events.txt:2284`: a saved scope value (`scope:eotg_frontier_fee`) as the gold amount in `remove_short_term_gold` / `add_gold` (§15 8).
  - In game:
    - a captain or faith leader paying the yearly sponsor gold, and what happens when the company disbands (§15 6);
    - `eotg_frontier_explored` surviving save/reload and a holder change (§15 7; test plan §0.1).
- **needs-local-validation:** Tiger + PX on the `eotg_frontier_*` files, `events/eotg_frontier_events.txt`, the loc file, and `docs/test_submods/frontier_vanilla/`.
- **needs-loc:** none. 42 new keys are written (316 → 358).
- **needs-lore:**
  - .040 and .041 against LAW AT 866: the captain, head of faith or holy order gains no claim, say or authority, and the tooltips say so.
  - "Unexplored Region" and the expedition text: time-neutral, no Void.
  - .041 is faith-neutral: "the head of your faith", "a holy order of your faith".
- **needs-human (spec §16):**
  - **Q3-1:** an Unknown Region is also Unsettled. Keep?
  - **Q3-2:** a mercenary captain as Founder? This needs the founder rule widened (deferred D3-1).
  - **Q3-3:** escort costs medium gold for 5 years.
  - **Q3-4:** AI-to-AI mercenary and faith backing (not built).
  - **Q3-5:** a dead head of faith's backing goes to their primary heir, not the next head.
- **art wanted (spec §14):**
  - a decision picture for Send an Expedition;
  - county-modifier icons for Unexplored Region, Partly Explored Region and Mercenary Escort;
  - an expedition event background.

  Vanilla `decision_realm.dds`, the vanilla icons and `theme = realm` are used for now.
- **taskboard:**
  - **CB-37 (Frontier in-game test):** add `frontier_v3_test_plan.md` after the v1/v2 plans.
  - **Proposed new item:** "Frontier Phase 3a: local verification (spec §15) and owner questions Q3-1..5".
