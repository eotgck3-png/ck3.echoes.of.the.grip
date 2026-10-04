### HANDOFF (cloud session; built without game files, Tiger or PX: nothing here has been run in game)
- **branch:** `claude/frontier-v1-cloud`, rebased onto `origin/v2-space-map` @ `bf7b3b8`
- **status:** partial. Phase 1 is built on the owner's rulings and the documented defaults. The engine verification is the next step.
- **basis:**
  - The owner answered Q1, Q2, Q12 and the lore questions (2026-10-04). They're recorded in spec §R.
  - The questions still open are listed, with the default built for each and where to change it, in `docs/specs/frontier_v1_open_questions.md`.
  - The owner hasn't sent a formal "Stage 2 approved". The owner's 2026-10-04 answers were taken as the go-ahead. The build follows §R, and where §R is silent, the recommended defaults.
- **summary:**
  - **The state lives on the Region (county title)** as variables: state, type, progress 0–100, strain 0–4, founder, sponsor, traces. The player sees one stage modifier, never numbers.
    - The political owner is the live county holder. Founder and sponsor are separate variables, and the new System always goes to the holder (Q12).
    - The only character-side data is the sponsor's back-reference `eotg_frontier_sponsoring`, so Withdraw can find its Region (spec §B.6).
  - **Unsettled** is data set by one effect, `eotg_frontier_mark_unsettled_effect`, called from a debug decision (`debug_only = yes`). It is map-agnostic: no title, province, culture, faith or character keys (grep: 0).
  - **The yearly tick** runs on `yearly_playable_pulse`, added in our own file.
    - Its cooldown authority is a 300-day variable on the Region, and the flavor-event cooldown is another, set only by the roll.
    - **Named strain causes:** No Founder, Low Control, Occupation, War and Sponsor Lapse, plus Hardship from an event choice (open Q13). A quiet year eases strain. Failure is never a random roll.
  - **Seven project types** are rows in if/else_if tables (rate, floors, result).
    - **Completion:** a Port, Bastion or Sanctum in an open slot (else development and control), plus development, control, the settlers' leader (Settlement), and `New Settlement` for 10 years.
    - **Abandoned** is resettlable: an attempts count, the former type, `Abandoned Works` for 10 years, and a head start of 10 per earlier attempt, up to 30.
  - **The 8 integration hooks** are custom on_actions, defined empty. They fire with root = the holder plus `scope:eotg_frontier_county`, `_founder` and `_sponsor`. Nothing names another system.
  - **6 events** (owner ruling):
    - .001 start;
    - .002 complication / *The Frontier Without a Founder*;
    - .003 sponsor offer;
    - .004 completion (rewards the founder, never with the holding);
    - .005 failure (abandon / new hands / scale back / lean on the backer);
    - .010 sponsor pick.
  - **Decisions:** Establish, Invest, Back a Frontier, Withdraw, Abandon, plus 2 debug decisions (mark capital Unsettled, run the Frontier year).
  - **AI:** a cap of 8 active, at most one per ruler.
  - **Loc:** 118 keys. Region/System wording; no charter, no factions, no Void.
- **files (all new except the spec):**
  - `common/scripted_effects/eotg_frontier_effects.txt`, `common/scripted_triggers/eotg_frontier_triggers.txt`, `common/script_values/eotg_frontier_values.txt`, `common/modifiers/eotg_frontier_modifiers.txt`;
  - `common/decisions/eotg_frontier_decisions.txt`, `common/on_action/eotg_frontier_on_actions.txt`, `common/scripted_character_templates/eotg_frontier_templates.txt`;
  - `events/eotg_frontier_events.txt`, `localization/english/eotg_frontier_l_english.yml`;
  - `docs/specs/frontier_v1.md` (§R rulings, §B build notes, identifier tables as built), `docs/specs/frontier_v1_open_questions.md`, `docs/specs/frontier_v1_test_plan.md`; this handoff.
  - **Not touched:** any `eotg_augmentation_*` file, gfx, the map, `descriptor.mod`, `replace_path`.
- **validation (sandbox):**
  - All 8 script and loc files parse with `pdx_parse` with no errors, and all carry a BOM.
  - `eotg_lint` with this tree's baseline: **0 new findings**. Three L011 hits were reworded (a false positive: the Region is a title, and "they" meant the settlers), not suppressed.
  - **Round-4 lint** (`claude/tools-round4-cloud`, run against this tree): **0** findings on L009, L010, L011, L013 and L014. L013d skips 13 keys in .004 and .005, by design; all 13 start with `\n\n`.
  - `check_all.py`: 10 pass, 0 fail, 7 skipped (local-only tools).
  - Spec conformance (round-4 tool on `frontier_v1.md`): every identifier in the as-built tables exists in script. The "missing" ids left are fallback or hypothetical names, the noted `eotg_k_cauldron` contradiction, and the "no `eotg_aug`" grep line.
- **gen_test_recipes on Frontier:** it runs (169 events with the cybernetics set), but its Frontier recipes are not usable. They're replaced by the hand-written `docs/specs/frontier_v1_test_plan.md`. Two tool limits showed up:
  1. It counts a scope saved inside an option's scripted effect as "provided" for the event's own trigger and desc. So .002–.005 show "fire cold: yes" although they need `scope:eotg_frontier_county`.
  2. It reads conditions inside a `scope:x = { }` switch in a scripted-effect context as the root's.

  Worth a tools follow-up.
- **unverified-vanilla:** every use is commented `# UNVERIFIED-VANILLA` in the files. The full list, with fallbacks, is open questions §B.
  - **The three that decide the architecture:**
    - **V1:** variables on a county title, through save/reload and a holder change. The test plan §0 is the owner's own test. Fallback: a story cycle, never the founder.
    - **V8:** `set_holding_type` on an empty slot, and who holds the new barony. Fallback: development and control.
    - **V12:** `trigger_event = { on_action = x }` with scopes. Fallback: empty scripted effects.
  - **Others:** `debug_only`; the global list over titles; `ordered_in_global_list`; `every_held_title` / `any_county_province` / `title_province` / `barony`; `is_occupied`; `random_ally`; `primary_heir` of a dead character; the county modifier keys and icons; `theme = realm`; the decision picture path; `prev` inside `var:x = { }`; the title-change shape.
- **source contradictions:**
  - The v1_19 reference teaches a story-cycle shape (`start_story` / `on_monthly`) that the mod's verified v2 script doesn't use.
  - `OLD PROJECT VERSION/CONTRIBUTING.md` shows `eotg_k_x` title keys, against invariant 2.
  - Higher sources were followed in both cases.
- **needs-lore:** none open (owner answers in spec §R). A localizer or lore-keeper read of the 118 keys is welcome.
- **needs-human:**
  1. Run `docs/specs/frontier_v1_test_plan.md` §0 (the V1 test) first.
  2. Then the rest of the plan.
  3. Answer the open questions file §A (Q3–Q16).
- **next:** orchestrator → eotg-vanilla-scout on open questions §B → eotg-qa (Tiger and PX on the `eotg_frontier_*` files; `error.log` lines with `eotg_frontier`) → human test plan → merge.
