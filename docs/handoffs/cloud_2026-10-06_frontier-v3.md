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

---

## Round 2 (2026-10-06)

### HANDOFF (cloud session, unvalidated)
- **branch:** `claude/frontier-v3-cloud`, with `origin/v2-space-map` @ `86eb121` merged in (`41ea2a7`). **Do NOT merge.**
- **status:** done (static; no Tiger, PX or game here).
- **summary:**
  - **Fixes:**
    - settling clears the exploration state, and Send an Expedition takes Survey's gate (S2);
    - .042 files the charts at Known through `eotg_frontier_file_survey_effect` in both options, so an active Frontier never gets survey data;
    - .040's escort is only for a Dangerous non-Military project and is paid with `pay_short_term_gold`. Its pool entry rolls only where (a) or (b) can apply, so the event never offers only "nothing";
    - holy order leaders are found through `random_faith_holy_order`, and `eotg_frontier_is_holy_order_leader` is retired;
    - companies at war with the holder are excluded;
    - `eotg_frontier_offer_backing_effect` documents that callers own their pacing, and refuses the holder as sponsor;
    - loc per the lore-keeper: *Guns for Hire*, the .040 desc and tooltip, and `eotg_frontier_mod_unknown_desc`.
  - **Owner decisions (spec §16):**
    - Q3-4: the AI accepts company and faith backers in `eotg_frontier_event_roll_effect`, with no event;
    - Q3-5: a faith backer's backing passes to the faith's next head or the order's next leader (spec §6.1), never their personal heir;
    - the cartographer note: no Unknown cores.
  - **Unclaimed prep:**
    - all expedition targeting goes through `eotg_frontier_can_target_expedition` and `eotg_frontier_pick_expedition_target_effect`, unchanged in behaviour (spec §4.1 says how Unclaimed widens them);
    - spec §17 lists every Phase 3a assumption of a real, playable holder;
    - no government, placeholder or claiming logic.
- **commits:**
  - `41ea2a7` the merge of `v2-space-map` (86eb121);
  - `6ed0eab` script and loc;
  - `1a8251d` spec, test plan and generated reports;
  - this handoff (the commit after `1a8251d`).
- **validation:**
  - eotg_lint: 0 findings;
  - check_all: 14 pass, 0 fail, 7 skipped (local tools);
  - spec_conformance: frontier_v3 has 0 missing, 76 present and 4 exempt (the Unclaimed ids, not built, and the retired trigger);
  - the loc file has one BOM.
- **unverified-vanilla:** `common/scripted_effects/eotg_frontier_effects.txt:1563`: a character variable holding a faith or a holy order, copied to a county variable and read back as a scope (spec §15 item 9). Items 6 and 7 stay in game.
- **needs-local-validation:** Tiger + PX on the Frontier files. In game, test plan §1.5–1.6 (filing on a Frontier; settling clears exploration), §0.2.3 (the holy-order search), §2.5 (a company disbands), §2.6 (AI backers) and §3.2 (a faith backer dies).
- **needs-loc:** none. One new key, `eotg_frontier_toast_faith_backer_succeeded`.
- **needs-lore:**
  - the new toast ("…passes to the one who now leads the faithful in their place");
  - the .040 tooltip ("while it does, the Region's dangers no longer slow the work").
  - The .040 desc is the lore-keeper's text verbatim. Its "guards for the convoys and, if the venture is a military one, money behind it as well" now reads on a Military project, where the escort isn't offered. Confirm that's acceptable, or give a variant for that case.
- **needs-human:** none new.
- **taskboard:** CB-37 also covers `frontier_v3_test_plan.md`'s round 2 steps; Q3-1..5 are answered.
