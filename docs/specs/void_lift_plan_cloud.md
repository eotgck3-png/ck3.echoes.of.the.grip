# Void Corruption: v1 → v2 lift plan (cloud)

> **Orchestrator note (2026-10-04):** written before the canon precedence ruling. The dated `docs/lore/` entries now outrank the SETTING LORE body (see `docs/lore/REVIEW_866.md`). Re-check canon claims here against that digest before acting on them. This is a proposal, not a ruling.


> **This is a proposal for eotg-architect, not a ruling.** It is static and unvalidated: it came from a cloud session with no Tiger, no PX, no game files and nothing run in game. Engine behavior I could not check is marked `UNVERIFIED-VANILLA`.
>
> **Date:** 2026-10-04. **Builds on:** `docs/qa/v1_lift_readiness_cloud.md` §2 "V. Void Corruption" (lines 73–108), X1 (`:54-57`), the SE row (`:221-223`, `:231`), and `circlebackTaskboard.md` CB-10, CB-11, CB-12 and B-FAITHS.
>
> **Not opened, by instruction:** anything named augmentation or cybernetics, `gfx/` and `map_data/`. The cybernetics text rules used in §4 are the ones quoted in the dispatch from `docs/specs/cybernetics_v2.md` §5, plus SETTING LORE ERRATA `:10-16` (ORRIN THE EYE) and `:25-30` (CYBERNETIC "VOICE").
>
> Paths are under `OLD PROJECT VERSION/` unless they start with a v2 path. I re-read every cited line for this plan.

## 0. Gate and status

- **Pipeline:** B, lift from v1 (`docs/agent_workflow.md:85-91`). The system breaks catalog lessons 13 (dead hook) and 6 (resource coupling in 0031/0032), and it hard-codes a faith key. Under Pipeline B's own rule (`:91`), that means it needs the architect pass this plan asks for.
- **Gate:** Gate 3 (`docs/agent_workflow.md:65-67`), and Gate 1 is still open. It can only be built now if it is classed as **mod-exclusive** (CLAUDE.md, decided 2026-10-02; `agent_workflow.md:141` rule 2). That class requires no reference to specific titles, provinces, characters, cultures or faiths.
- **What the script couples to today:**
  - **One faith key:** `eotg_religion_void_reverence` (`common/scripted_triggers/eotg_void_triggers.txt:50-52`). This blocks on B-FAITHS and breaks the map-agnostic rule.
  - **One mod trait from a shared file:** `eotg_grip_survivor` (`common/traits/eotg_traits.txt:10`). This is fine once its owner is decided (§3a).
  - **No titles, provinces or history characters** in script.
- **What the text names:** canon entities Elrossi (loc `:85,88,124`) and Malvrick (`:45,85`). That is text, not script, so it does not break the map-agnostic rule. It does tie the text to canon (§6).
- **→ human/architect call:**
  1. Is Void mod-exclusive, so it can be built on the temporary map?
  2. If yes, the cult branch must be stubbed per §3b before the lift.

  In script, nothing else ties Void to a map.

**Corrections to the audit (re-verified):**
- **The Void on_action file already exists in v1.** `common/on_action/eotg_void_on_actions.txt` (190 lines) defines the 5 sub-hooks. Only the parent `eotg_on_yearly_void_check` (`eotg_on_actions.txt:76-84`) and its registration on the dead hook (`:11-13`, Void entry at `:13`) live in the hub.
- **The cult gate has 23 call sites, not 11.** There are 17 gating sites and 6 `ai_chance` sites (§3b).
- **SETTING LORE line numbers have moved.** The audit's Voidwalker citations "SETTING LORE `:127,218`" are now `:144` and `:235`. The ERRATA block grew by 17 lines; today `:127` is "Religious orthodoxies solidifying" and `:218` is "Pale Hand CONSPIRACY…".

---

## 1. Target layout

| v1 source | v2 target | What moves / changes |
|---|---|---|
| `events/eotg_void_whispers.txt` (0001–0004, 0010, 0011) | `events/eotg_void_whispers.txt` | Whole file; namespace `eotg_void`. Fixes in §2 (0004 bug, 0010.c re-fire, stub). |
| `events/eotg_void_touched_events.txt` (0020–0025) | `events/eotg_void_touched_events.txt` | Whole file. Rename the saved scopes (§2 step 5). 0021.c and 0022.c get a fix or a reword. |
| `events/eotg_void_hollowing.txt` (0030–0032) | `events/eotg_void_hollowing.txt` | Whole file. 0030.c gets a fix or a reword. The 0031/0032 resource coupling depends on §3d. |
| `common/on_action/eotg_void_on_actions.txt` (5 sub-hooks) | `common/on_action/eotg_void_on_actions.txt` | Whole file, **plus** the parent block moved in from the hub (`eotg_on_actions.txt:76-84`), **plus** a new additive registration in this file and never in a hub: `yearly_playable_pulse = { on_actions = { eotg_on_yearly_void_check } }`. Rewrite the header comment at `:4-6`, which says the parent lives in the hub. |
| `common/on_action/eotg_on_actions.txt:11-13` (`on_yearly_playable`, Void entry) and `:73-84` | — (extracted) | Only `eotg_on_yearly_void_check` is taken. The rest of the hub stays in v1 (governments, Myr, Exodus). |
| `common/decisions/eotg_void_decisions.txt` | `common/decisions/eotg_void_decisions.txt` | Whole file. The commune decision is gated by the cult stub. |
| `common/modifiers/eotg_void_modifiers.txt` | `common/modifiers/eotg_void_modifiers.txt` | Whole file, plus `eotg_mod_void_aura` extracted from `eotg_modifiers.txt:7-14`. Rename `eotg_mod_void_pressure` if §3c says so. |
| `common/opinion_modifiers/eotg_void_opinions.txt` | `common/opinion_modifiers/eotg_void_opinions.txt` | Whole file, plus a proposed `eotg_opinion_void_reassured` (§2 step 5d). |
| `common/scripted_effects/eotg_void_effects.txt` | `common/scripted_effects/eotg_void_effects.txt` | Whole file. Fix the shelter effect and add the insight guard. |
| `common/scripted_triggers/eotg_void_triggers.txt` | `common/scripted_triggers/eotg_void_triggers.txt` | Stub `eotg_st_void_venerates` (§3b). Prune 3 triggers (§2 step 6). Fix the comments. |
| `common/traits/eotg_void_traits.txt` (defiant, hollowed) | `common/traits/eotg_void_traits.txt` | Plus `eotg_void_touched` extracted from `eotg_traits.txt:25-40`. |
| `common/traits/eotg_traits.txt:7-23` (`eotg_grip_survivor`) | **per §3a** (recommended: `common/traits/eotg_setting_traits.txt`) | Owner decision first. |
| — | **new** `common/scripted_character_templates/eotg_void_templates.txt` | Voidwalker template (§2 step 7a, option 1). The folder already exists in v2. |
| `localization/english/eotg_void_l_english.yml` (177 lines) | `localization/english/eotg_void_l_english.yml` | Whole file, UTF-8 BOM. §4 rewrites. Add `eotg_void_touched` loc (`eotg_l_english.yml:7-9`), `eotg_mod_void_aura` (`:12`) and a new `eotg_mod_void_aura_desc`. |
| `localization/english/eotg_l_english.yml:3-5` (`eotg_grip_survivor`) | follows §3a (e.g. `eotg_setting_l_english.yml`) | Its desc needs the lore pass in §4. |
| **Not lifted** | — | `eotg_se_apply_void_corruption` and `eotg_se_remove_void_corruption` (`eotg_scripted_effects.txt:7-26`): no callers, and they bypass the exposure state machine. `eotg_se_grant_grip_heritage` (`:28-36`) and `eotg_st_is_grip_survivor` (`eotg_scripted_triggers.txt:7-11`): no callers. `eotg_st_is_void_touched` (`:13-17`): no callers (comment ref only, `eotg_void_triggers.txt:18`). `eotg_st_is_third_era_ruler` (`:19-25`): TODO stub, not Void. `eotg_mod_grip_resilience` (`eotg_modifiers.txt:16-23`, loc `eotg_l_english.yml:13`): no users, not Void. The dead triggers and flags in §2 step 6. |

---

## 2. Ordered work list

**Step 0. Rulings.** Owner: architect, then human. Rule on §3 (a)–(e) and §0 (mod-exclusive).
- Steps 1–6 and 7a–7e can start before the rulings land. Each depends on a ruling only where noted.
- 7f and §4 loc wait for (c), (d) and (e).

**Step 1. Copy the system.** Owner: scripter.
- Copy the 3 event files and the 7 `common/*/eotg_void_*` files to the v2 paths in §1, unchanged.
- Run the Pipeline B audit: prefix, no title refs, resource coupling, cooldown authority.
- Cooldown authority already lives in the on_action (`eotg_st_void_event_ready`, `eotg_void_triggers.txt:157-159`). No event `trigger` re-checks `eotg_flag_void_event_cooldown` (I checked all 15). Lesson 5 holds.

**Step 2. Rewire the hook (CB-10, X1, lesson 13).** Owner: scripter. File: `common/on_action/eotg_void_on_actions.txt`.
- Add this, verbatim from `eotg_on_actions.txt:76-84`:
  ```
  eotg_on_yearly_void_check = {
      on_actions = {
          eotg_on_yearly_void_accrual
          eotg_on_yearly_void_contact
          eotg_on_yearly_void_whispers
          eotg_on_yearly_void_touched
          eotg_on_yearly_void_hollowed
      }
  }
  yearly_playable_pulse = {
      on_actions = { eotg_on_yearly_void_check }
  }
  ```
- Never use `on_yearly_playable`.
- Never give a vanilla hook a top-level `effect = {}`.
- **Order is load-bearing.** Accrual must run before the stage gates (`eotg_void_on_actions.txt:8-10`; hub comment `:74-75`). Whether a list of on_actions runs in order is `UNVERIFIED-VANILLA` (audit §4.5).
  - **If it does not:** call `eotg_se_void_yearly_accrual` from an `effect` in `eotg_on_yearly_void_check` and keep only the 4 event sub-hooks in its `on_actions`. Whether an on_action's `effect` runs before its `on_actions` is itself `UNVERIFIED-VANILLA`. vanilla-scout decides.

**Step 3. Extract from shared files.** Owner: scripter, except the loc (localizer).
- `eotg_traits.txt:25-40` (`eotg_void_touched`) → `common/traits/eotg_void_traits.txt`. Rewrite the comment at `:26-27`, which says "Orrin's remnants".
- `eotg_modifiers.txt:7-14` (`eotg_mod_void_aura`) → `common/modifiers/eotg_void_modifiers.txt`. Update the header comment at `eotg_void_modifiers.txt:7`.
- Loc `eotg_l_english.yml:7-9` and `:12` → `eotg_void_l_english.yml`.
- `eotg_grip_survivor` (`eotg_traits.txt:7-23`; loc `eotg_l_english.yml:3-5`) goes wherever §3a says.

**Step 4. Script-comment canon pass.** Owner: scripter, then lore-keeper.
- These comments state Orrin as fact. Reword them to say "the influence is unexplained; the cult and some Voidwalkers attribute it to Orrin":
  - `eotg_void_effects.txt:5-8`
  - `eotg_void_triggers.txt:6-13`, `:32-33`
  - `eotg_void_whispers.txt:13-14`, `:78`, `:409-410`
  - `eotg_void_traits.txt:7`, `:15`
  - `eotg_void_opinions.txt:34-35`
  - `eotg_void_decisions.txt:113-116`
  - `eotg_traits.txt:8`, `:26`
- Fix the comments that do not match the behavior:
  - `eotg_void_triggers.txt:105-106` says Defiant characters are asked again "until the ward lapses". The trigger checks the **trait** (`:112`), which never lapses, so a Defiant character is never offered the Bargain again.
  - `eotg_void_triggers.txt:144-145` says you cannot ward "past saturation". The trigger (`:146-151`) has no saturation check.
  - `eotg_void_hollowing.txt:76` says 0030.c is "always available", but it is gated on `primary_heir` (`:79-82`).
  - `eotg_void_touched_events.txt:544` says 0025.c is "always available", but it is gated on `gold >= 150` (`:547`).

**Step 5. Renames.**
- **(a) Saved scopes (invariant 1).** Owner: scripter. All in `events/eotg_void_touched_events.txt`:
  - `void_child` → `eotg_void_child` (`:126,138,153,184`)
  - `void_confessor` → `eotg_void_confessor` (`:232,244,256,273,285`)
  - `void_vassal` → `eotg_void_vassal` (`:489,501,515,533,549,563`)

  No loc string uses these scopes (checked).
- **(b) `eotg_mod_void_pressure`, if §3c renames it.** Owner: scripter + localizer. Sites: `eotg_void_modifiers.txt:23`; `eotg_void_effects.txt:41,50,199`; loc `:15-16`. Example key: `eotg_mod_void_undertow`.
- **(c) Opinion names "Marked by the Eye" / "Refused the Eye".** Owner: localizer. Loc `:36-37` → §4.
- **(d) Split `eotg_opinion_void_defiance_respect`.** Owner: scripter + localizer.
  - **Problem:** its "Refused the Eye" label is applied at 11 sites, and only 2 of them are an actual refusal: `eotg_void_whispers.txt:490` (0010.b) and `eotg_void_touched_events.txt:257` (0022.a).
  - **The other 9 are generic reassurance:**
    - `eotg_void_touched_events.txt:427` (0024.a heir), `:516` (0025.a), `:550` (0025.c bought silence)
    - `eotg_void_hollowing.txt:85` (0030.c), `:164` (0031.b), `:178` (0031.c), `:241` (0032.a), `:257` (0032.b)
  - **Proposal:** add `eotg_opinion_void_reassured` (+10, 10 years) to `eotg_void_opinions.txt` and use it at those 9 sites. Keep `defiance_respect` for the two refusals.
- **(e) "Hollowed" name clash.** Owner: localizer. The trait (loc `:7,9`) and the opinion `eotg_opinion_void_revulsion` (loc `:33`) are both shown as "Hollowed". Rename the opinion (§4). The key can stay.
- **(f) "The Borrowed Voice"** (`eotg_mod_void_borrowed_voice`, loc `:29-30`). Owner: localizer. "Voice" is the cybernetics term (ERRATA `:25-30`). Rename the display name (§4). The key can stay, or become `eotg_mod_void_unseen_advocate`.

**Step 6. Prune.** Owner: scripter. Each item below is defined or set and never read. I grepped the whole v1 tree.

| Identifier | Where | Status |
|---|---|---|
| flag `eotg_flag_void_bargain_offered` | `eotg_void_whispers.txt:440` | Set, never read. Prune, or reuse per step 7d. |
| trait flag `eotg_flag_void_defiance` | `eotg_void_traits.txt:29` (file line; shown as 114 in the concatenated read) | Never read. |
| trait flag `eotg_flag_void_corruption` | `eotg_traits.txt:39`; `eotg_void_traits.txt:54` | Never read; shared by touched and hollowed. |
| trait flag `eotg_flag_grip_bloodline` | `eotg_traits.txt:22` | Never read (goes with §3a). |
| trigger `eotg_st_is_void_hollowed` | `eotg_void_triggers.txt:66-68` | No callers. |
| trigger `eotg_st_void_rift_contact` | `eotg_void_triggers.txt:83-85` | No callers. |
| trigger `eotg_st_void_resists` | `eotg_void_triggers.txt:136-141` | No callers. |
| `eotg_st_is_void_touched`, `eotg_st_is_grip_survivor`, `eotg_se_grant_grip_heritage`, `eotg_se_apply/remove_void_corruption`, `eotg_mod_grip_resilience` | shared files (§1) | Not lifted. |

**Step 7. Bug fixes.** Owner: scripter, unless noted.

**7a. Voidwalker flag on the wrong character (HIGH).**
- **The bug:** `eotg_se_void_shelter_voidwalker` (`eotg_void_effects.txt:69-71`) runs `add_character_flag = eotg_flag_void_voidwalker` on the **ruler**. `eotg_st_void_has_voidwalker` (`eotg_void_triggers.txt:74-79`) looks for the flag on `any_courtier`.
- **The effects today:**
  - the Voidwalker Ward decision (`eotg_void_decisions.txt:69-72`) is never shown;
  - the −6 accrual (`eotg_void_effects.txt:147-150`) never applies;
  - the on_action gate `eotg_st_void_has_voidwalker = no` (`eotg_void_on_actions.txt:101`) never closes, so event 0004 can fire again at a 12% yearly chance after its 5-year cooldown. Each time, option .a costs −100 piety (`eotg_void_whispers.txt:337`) and hits zealous courtiers' opinion again.
- **Option 1 (recommended):** make the Voidwalker a real courtier.
  - New `common/scripted_character_templates/eotg_void_templates.txt` with `eotg_void_voidwalker_template`:
    - female, to match loc `:85-89`;
    - adult age range;
    - learning-leaning skills;
    - **no hard-coded culture or faith**: take them from the ruler or leave them to the template default, for map-agnosticism. Once faiths exist, revisit giving her the Malvrick or cult faith (§3e).
  - Shelter effect:
    ```
    eotg_se_void_shelter_voidwalker = {
        create_character = {
            template = eotg_void_voidwalker_template
            location = root.capital_province
            employer = root
            save_scope_as = eotg_voidwalker
        }
        scope:eotg_voidwalker = { add_character_flag = eotg_flag_void_voidwalker }
    }
    ```
  - **UNVERIFIED-VANILLA:** the `create_character` field names (`template`, `location`, `employer`, `save_scope_as` inside `create_character`); `root.capital_province`; and the template file shape. vanilla-scout should copy a vanilla template plus its call site.
  - Knock-on effects:
    - the decision becomes visible;
    - −6 accrual applies;
    - 0004 stops firing while she lives.
    - If she dies or leaves court, the shelter is lost and 0004 can offer again. That reads as intended.
    - Decision text `:44-47` ("the heretic under your roof") becomes literally true.
- **Option 2:** check the flag on root (`eotg_st_void_has_voidwalker = { has_character_flag = eotg_flag_void_voidwalker }`).
  - Trivial, but the shelter is permanent and has no person behind it.
  - The decision loc then over-promises a person.
  - 0004 never repeats.

**7b. Insight stacking (MED).**
- `eotg_se_void_edu_insight` (`eotg_void_effects.txt:215-245`) adds +2 base skill (always stacks) and a permanent modifier (stack or refresh is `UNVERIFIED-VANILLA`, audit §4.6).
- **It is called 7 times:**
  - decision commune (`eotg_void_decisions.txt:143`), every 10 years;
  - 0010.a (`eotg_void_whispers.txt:448`), 0010.c (`:511`), 0011.a (`:569`), 0011.c (`:594`);
  - 0023.a (`eotg_void_touched_events.txt:345`), which can come up every eligible year;
  - 0024.b (`:440`).
- 0030.b also adds `eotg_mod_void_unseen_step` directly (`eotg_void_hollowing.txt:72`).
- **Fix:** guard each branch on its own modifier being absent, e.g. `limit = { has_education_learning_trigger = yes NOT = { has_character_modifier = eotg_mod_void_deep_charts } }`. If it is already present, fall through to a small non-stacking payout (e.g. `add_prestige = 50`) or nothing.
- **Note on the `else` branch** (`:241-244`): with no matching education, the character gets `cold_hand`, the same modifier as martial. The modifier guard covers both.
- Guard 0030.b the same way.

**7c. Double-queue window (MED, proposal).**
- **The gap:** the cooldown flag is set in each event's `immediate`, which runs when the event fires, 1–60 days after the queue. During one pulse, more than one sub-hook can queue an event. Examples:
  - 0004 is an independent `if` (`eotg_void_on_actions.txt:97-109`) next to the 0010/0011/0002/0003 chain;
  - a non-seeded `eotg_grip_survivor` at 25+ exposure can draw 0001 and 0002 in the same year.
- **Fix:** each on_action that calls `trigger_event` also sets a short `add_character_flag = { flag = eotg_flag_void_event_queued days = 90 }`, and `eotg_st_void_event_ready` checks that flag as well. Cooldown authority stays in the on_action (invariant 4), and event triggers still do not re-check it.

**7d. 0010 re-fire (0104-style).**
- **The loop:** after 0010.c ("refuse but keep") or 0010.d, the character is neither Touched nor Defiant, so `eotg_st_void_bargain_ready` stays true. 0010 then comes back every ≥5 years at 50%, and .c can be taken again, granting insight each time.
- This is by design for .d ("defers", `:523`). It is not by design for .c.
- **Fix:** .c sets `eotg_flag_void_insight_stolen` and is hidden when that flag is present. Either reuse the dead `eotg_flag_void_bargain_offered` slot for this or prune it.
- Other repeaters I checked, all acceptable:
  - 0024 repeats every 5 years at 60+; .a gives +1 learning each time, harmless.
  - 0011 and 0030 fire once (the stage changes).
  - 0001 fires once (every option seeds the flag).

**7e. Shared ward cooldown (LOW).**
- Both ward decisions set the same `eotg_flag_void_ward_cooldown`: 10 years at `eotg_void_effects.txt:254` and 8 years at `eotg_void_decisions.txt:88`. So each locks out the other.
- The tooltips (`:43,47`) do not say so.
- **Fix:** split the flags, or say it in the tooltips.

**7f. Over-promising options (MED).** Owner: scripter + localizer. Make each real, or reword it.
- **0030.c "Abdicate"** (`eotg_void_hollowing.txt:77-94`; loc `:159`): it gives piety, heir opinion and stress loss, and does not abdicate.
  - *Real:* `depose = yes` or a vanilla abdication effect, `UNVERIFIED-VANILLA`. Also add a guard so the Hollowed character keeps the trait as a courtier.
  - *Reword:* §4. **Recommend the reword** unless vanilla-scout confirms a clean abdication effect.
- **0021.c "Send them to be fostered"** (`eotg_void_touched_events.txt:182-194`; loc `:120`): only an opinion and −3 exposure.
  - *Real:* move the child to another court, or set a guardian. The effect names are `UNVERIFIED-VANILLA`.
  - **Recommend the reword** (§4).
- **0022.c "Have them silenced. Tonight, and permanently."** (`:280-299`; loc `:128`): +25 dread, −100 piety and an opinion. Nobody is silenced.
  - *Real:* `imprison` the confessor (`UNVERIFIED-VANILLA`).
  - **Recommend the reword** (§4) to a public rebuke, which matches the dread and opinion it already gives.

**7g. Cult stub (§3b).** Owner: scripter. Applies whichever option the architect picks.

**7h. 0011.b ward (LOW, design note).** 0011's `immediate` runs `eotg_se_void_become_touched`, which removes `eotg_mod_void_warded` (`eotg_void_effects.txt:174`). Option .b then re-adds it for 5 years (`eotg_void_whispers.txt:584`). That contradicts "the ward is spent" (`eotg_void_effects.txt:164`). It is harmless, but the architect should confirm it is intended.

**Step 8. Loc lift.** Owner: localizer.
- Copy `eotg_void_l_english.yml` and add the extracted keys (step 3), with UTF-8 BOM and the `l_english:` header.
- Apply §4.
- Add `eotg_mod_void_aura_desc` (missing in v1: grep found 0 hits).
- Add loc for any new keys: `eotg_opinion_void_reassured`, and the renamed modifier if (c).
- One definition per key across the tree.

**Step 9. Canon and register review.** Owner: lore-keeper.
- Review §4 against ERRATA `:10-16` and `:25-30`.
- Cross-check that no Void string uses the cybernetic register (interior, predictive, "half-second early").
- QA cross-checks the reverse, that no cybernetics text uses Void words. That needs the cybernetics loc, which this session may not open.

**Step 10. Validation (local session).** Owner: QA, read-only.
1. `python docs/tools/px_vocab_check.py common events`: there must be no dead-hook finding (pitfalls §12), and `yearly_playable_pulse` must be recognized.
2. `ELECTRON_RUN_AS_NODE=1 ".../Code.exe" docs/tools/px_lsp_diagnostics.js common events localization`: braces, BOM, loc format, dangling event ids, required loc.
3. Run `px_lsp_diagnostics.js events --request=eventGraph --request=locCoverage --out=<scratchpad>`, then `python docs/tools/px_event_report.py <scratchpad>`. All 15 `eotg_void.*` events must be reachable from `yearly_playable_pulse`, and there must be no missing `eotg_` loc.
4. Run Tiger with the root `echoes_of_the_grip.mod` (B-DESCRIPTOR is now cleared). First check that its `path=` (`C:/Users/river/Documents/GitHub/ck3.echoes.of.the.grip`) is the working copy. Write logs to the scratchpad, and ignore the known-benign religion/culture and `20_health_effects` noise. Scope checks matter here (e.g. `primary_heir = { … }`, `scope:eotg_voidwalker`).
5. These greps must all come back empty:
   - `grep -rnE 'eotg_[ekdcb]_'`
   - `grep -rn 'on_yearly_playable\b' common`
   - `grep -rn 'save_scope_as = void_' events`
   - `grep -rn 'eotg_religion_void_reverence' common events` (after the stub)
   - `grep -niE 'interior language|own thought|own voice' localization/english/eotg_void_l_english.yml`
6. Human, in game on the temporary map: seed exposure via console (`UNVERIFIED-VANILLA` console syntax), then check that 0004.a creates the courtier, that the Voidwalker Ward appears, and that 0004 does not recur.

---

## 3. Architect calls

### (a) Who owns `eotg_grip_survivor`

**Who uses it in v1:**
- **Void:** `eotg_void_effects.txt:89-92` (+3 accrual); `eotg_void_triggers.txt:40` (susceptibility); `eotg_void_whispers.txt:134-137` and `:424-427` (bloodline descs, loc `:65,95`).
- **Orrin's Grip opening story:** `events/eotg_story_orrins_grip.txt:21,38`.
- **History characters:** `history/characters/eotg_characters_866.txt:35,74`.
- **Bookmark design:** `docs/866_bookmark_design.md:111` ("bloodline heritage, not personal experience").
- **Shared helpers with no callers:** `eotg_se_grant_grip_heritage` and `eotg_st_is_grip_survivor`.

| Option | Pros | Cons |
|---|---|---|
| 1. Lift it with Void (`eotg_void_traits.txt`) | One commit; no new shared file. | Wrong owner: it is a setting-wide heritage marker that history and the Grip story will assign. Void would end up owning Gate 1 data. |
| 2. Shared `common/traits/eotg_setting_traits.txt` (+ `eotg_setting_l_english.yml`), trait only, owned by architect/scripter | Right ownership. History and the Grip story can use it later without touching Void. | A new shared file (the v1 hub problem). Keep it to setting-wide traits only. Its desc needs a lore pass (§4, `eotg_l_english.yml:5`). |
| 3. Cut the bloodline branches (4 script sites + 2 descs) | No dependency at all. | Loses two of the best descs. Anyway, on the temporary map nobody holds the trait, so the branches are inert, not broken. |

**Recommendation: option 2.** Ship the trait definition and loc only, with no assignment. Void keeps its 4 references. They do nothing until Gate 1 history assigns the trait, which suits the map-agnostic rule.

### (b) Gating the cult branch without a faith key

The current gate is `eotg_st_void_venerates = { faith = { religion_tag = eotg_religion_void_reverence } }` (`eotg_void_triggers.txt:50-52`). `religion_tag` is `UNVERIFIED-VANILLA`.

**All 23 sites:**
- **Gating (17):**
  - `eotg_void_effects.txt:95` (+5 accrual), `:155` (piety resistance)
  - `eotg_void_decisions.txt:26` (Warding Rite hidden for cult), `:125` (Commune shown)
  - `eotg_void_triggers.txt:42` (susceptibility)
  - `eotg_void_whispers.txt:84` (0001.c), `:131` (0002 desc), `:421` (0010 desc), `:453`/`:460` (0010.a opinions), `:580` (0011.b)
  - `eotg_void_hollowing.txt:32` (0030 desc), `:54` (0030.a), `:60` (0030.a kin)
  - `eotg_void_touched_events.txt:220` (0022 desc), `:252` (0022.a), `:270` (0022.b)
- **ai_chance (6):** `eotg_void_whispers.txt:97, 347, 382, 471, 497, 603`.

| Option | Pros | Cons |
|---|---|---|
| 1. Vanilla doctrine/tenet check (CB-12 style), e.g. `faith = { has_doctrine = tenet_esotericism }` | No new content. | Vanilla tenets are too broad: every esoteric faith would become a Void cult. Still needs B-FAITHS. |
| 2. Mod tenet `eotg_tenet_void_veneration` (`common/religion/doctrines/`, `UNVERIFIED-VANILLA` shape), checked with `has_doctrine` | Precise, map-agnostic, and any faith can carry it. Matches the CB-12 direction. | Needs the religion folders and a test faith; touches B-FAITHS work. |
| 3. Personal trait or flag (e.g. hidden trait `eotg_void_votary`) | Faith-independent, and fits canon "remnant cults persist in secret" (SETTING LORE `:403`). Testable on the temporary map. | Nothing sets it yet; it needs an entry path (0004 or 0001.c). It changes the design from a faith to a secret allegiance (architect and lore call). |
| 4. `eotg_st_void_venerates = { always = no }` with `# STOPGAP: B-FAITHS` | Zero risk. Lifts all code intact. Unblocks the lift now. | The cult branch is dormant. |

With option 4: the "= no" sites always pass; 0030.a and 0022.b are never offered, and 0030.d, 0022.c and 0022.d remain, so there is no soft-lock; the commune decision is hidden.

**Recommendation:** option 4 now, then option 2 when B-FAITHS clears. Record it as a CB-12 sibling on the taskboard. Ask the architect whether option 3 (the secret-allegiance design) is wanted alongside it.

### (c) "Pressure" vs "static"

**Facts:**
- v1 Void uses "Void Pressure" (loc `:15`) and "The pressure recedes" (`:20`); key `eotg_mod_void_pressure`.
- The audit (`:93`) records that QA round 2 moved cybernetics off "pressure"; cybernetics now uses "the static" (per dispatch).
- The Cartel has `eotg_cartel_defiance_pressure` (audit `:231`).

| Option | Pros | Cons |
|---|---|---|
| 1. Void keeps "Pressure" (rule: "pressure" is Void's) | No change. | Generic English word, and it overlaps the Cartel resource. It also invites drift back into other systems' text. |
| 2. Rename the band: **"Void Undertow"** (alternatives: "Void Pull", "Void Draw", "Void Tide") | Unique and external: something pulling from outside. It fits v1's own water imagery ("a voice heard through deep water" `:63`; "the way water finds the low ground" `:103`). | 4 script sites plus 2 loc keys. Before adopting, grep the cybernetics loc for the word; that file is off-limits to this session. |
| 3. Neutral term ("Deepening Exposure") | No collision. | Flat. It loses the band's character. |

**Recommendation:** option 2 ("Undertow"), renaming the key as well (`eotg_mod_void_undertow`), plus the `:20` rewrite in §4.

### (d) The resource after Hollowing

**Facts:**
- `eotg_se_void_become_hollowed` pins exposure at 100 (`eotg_void_effects.txt:201`).
- Accrual stops, because `eotg_st_void_susceptible` excludes the Hollowed (`eotg_void_triggers.txt:38`).
- 0031 and 0032 (`eotg_void_hollowing.txt:116-187`, `:196-291`) read only the trait and never move exposure. They are the only invariant-5 failures: every other event moves exposure in at least one option, and 0030 sets it.
- 17 of 56 options leave exposure untouched (recounted): 0001.b, 0002.b, 0002.d, 0003.c, 0010.a, 0025.c, all four 0030 options, all three 0031 options, and all four 0032 options. Invariant 5 is per event, though, not per option.

| Option | Pros | Cons |
|---|---|---|
| 1. Ruling: in stage D the trait is the resource | Cheapest; it lifts now. 0031/0032 move dread and opinion, which is the cost the trait describes. | It bends invariant 5 by ruling; QA audit 8 would need the exception written down. |
| 2. New stage-D variable, e.g. `eotg_void_lucidity` (0–100): 0031 lowers it, 0032 options raise it, and it sets 0032's weight | Makes 0032 "buy back standing" (`:10-13`) legible, and keeps the invariant honest. | New resource, band and loc. That is design work, not a lift. |
| 3. Couple to exposure (0032 options −5 to −10, 0031 +5; 0032 weight read from exposure < 100) | No new variable. | Exposure has no meaning past 100 or once Hollowed; nothing else reads it. It is a fake coupling. |

**Recommendation:** option 1 now, written into the spec as an explicit exception. Add a taskboard deferral for option 2 if play-testing shows 0031/0032 feel inert.

### (e) Voidwalkers: worshippers or wardens

**The canon body text:**
- `SETTING LORE:144`: "Voidwalkers (Malvrick sect): Secret society forming around void worship".
- `:235`: Malvrick "Darkness, Void, Secrets | Voidwalkers (mostly destroyed)".
- `:270`: "Voidwalker Remnants: Malvrick worship continues underground".
- `:398-403`: the hunts, 200–700 AG.

**v1 instead casts them as wardens:**
- `eotg_void_triggers.txt:10-16`;
- loc `:85` ("her order spent four hundred years learning to close these things");
- the decision at `:44-47`.

**Context:** the v1 Void Reverence religion has Malvrick as its high god (`common/religion/religion_types/eotg_religions.txt:930,961`). Its comment says it venerates "Carrigore and the Void" (`:929`), and `866_religions:130-134` says the faith "venerates the breach itself". That is a three-way identity question (§6). This is in the canon dossier, so it is not decided here.

**How the plan branches on each answer:**
- **Worship.** The mechanics stay: the ward still works, as a votary's craft. The text changes:
  - 0004.desc `:85` becomes "learning to keep these things" (keeper, not closer);
  - the decision desc `:45` frames the ward as a rite of the Void's own faithful;
  - in 0004.a, the sheltered Voidwalker may later become the cult's entry path (§3b option 3);
  - the template faith follows the Malvrick or cult faith once B-FAITHS clears.
- **Warden.** Keep the v1 text, but this needs an ERRATA entry to override `:144`/`:270`. The template takes the ruler's faith or a neutral one.
- **Both (my suggestion to the lore-keeper).** They revere the Void and, for that reason, guard its thin places against misuse, as priests keeping a shrine shut. Only `:85` and `:45` change wording, and the mechanics are untouched.

---

## 4. Loc drafts

All lines are in `localization/english/eotg_void_l_english.yml` unless marked `eotg_l_english.yml`. I re-read every line and key. Current text is verbatim, trimmed with … where long. Proposals use American spelling, keep the Void **external** (at the edge of hearing, from an unnamed source), name Orrin only as a belief, and drop the hard-coded year count. The v1 strings have no `[…]` functions to preserve.

| Line | Key | Current (verbatim) | Proposed |
|---|---|---|---|
| 4, 6 | `eotg_void_defiant_desc`, `trait_eotg_void_defiant_desc` | "This character was offered something through the weakening seal, and gave it back. Voidwalker doctrine holds that what is refused cannot be taken twice." | "This character was offered something from beyond the scar, and gave it back. Voidwalker doctrine holds that what is refused cannot be taken twice." |
| 15 | `eotg_mod_void_pressure` (→ `eotg_mod_void_undertow` per §3c) | "Void Pressure" | "Void Undertow" |
| 16 | `eotg_mod_void_pressure_desc` (→ `_undertow_desc`) | "The whispers have opinions now, and a preference for solitude. It has become easier to keep secrets than company." | Text unchanged; only the key is renamed. |
| 20 | `eotg_mod_void_warded_desc` | "Sigils drawn correctly, in the old order, by someone who understood why the order mattered. The pressure recedes while the ward holds." | "Sigils drawn correctly, in the old order, by someone who understood why the order mattered. The sound at the edge of hearing falls back while the ward holds." |
| 28 | `eotg_mod_void_long_ledger_desc` | "…across spans longer than a life, and settle favourably." | "Accounts settle themselves across spans longer than a life, and settle favorably." |
| 29 | `eotg_mod_void_borrowed_voice` | "The Borrowed Voice" | "The Unseen Advocate" |
| 30 | `eotg_mod_void_borrowed_voice_desc` | "People agree first and wonder why afterward. Something else is doing part of the talking, and it is very good at it." | "People agree first and wonder why afterward. When this character speaks, listeners swear someone else in the room was agreeing, just at the edge of hearing." |
| 33 | `eotg_opinion_void_revulsion` | "Hollowed" | "A Hollow Throne" |
| 34 | `eotg_opinion_void_harbors_heretic` | "Harbours Heretics" | "Harbors Heretics" |
| 36 | `eotg_opinion_void_kinship` | "Marked by the Eye" | "Void Kinship" |
| 37 | `eotg_opinion_void_defiance_respect` | "Refused the Eye" | "Refused the Void" (2 sites only, per step 5d) |
| new | `eotg_opinion_void_reassured` | — | "Reassured" |
| 41 | `eotg_decision_void_warding_rite_desc` | "…It is also not a hanging offence." | "Every faith that survived the Grip kept some form of ward against the scars, half-remembered and expensive to perform properly. It is weaker than what the Voidwalkers knew. It is also not a hanging offense." |
| 48 | `eotg_decision_void_commune` | "Commune with the Eye" | "Commune with the Void" |
| 49 | `eotg_decision_void_commune_desc` | "The seal is thin here, and thinning. What waits behind it has never once been generous, but it has always been willing to trade — and it pays in exactly the currency you were taught to count." | "The scar is thin here, and thinning. Your faith says something waits on the far side; it has never said what, and your priests stopped agreeing long ago. Whatever it is has never once been generous, but it has always been willing to trade — and it pays in exactly the currency you were taught to count." |
| 63 (LOW) | `eotg_void.0002.desc` | "It began as a fault in the foundations, which is what you told the mason, who found no fault. …" | "It began as a fault in the foundations, which is what you told the builders, who found no fault. It is beneath the floor of your own chambers and nowhere else, and it keeps no rhythm that a pump or a settling stone would keep.\n\nIt is closest to a voice heard through deep water. It has been three weeks. You have started leaving a lamp burning." (Only "mason" changes; it is a medieval leak.) |
| 64 (optional; already framed as belief) | `eotg_void.0002.desc_cult` | "…Your faith teaches that Orrin the Eye speaks to those he intends to use, and that being used by a god is the nearest thing to grace this cosmos still offers. …" | "The priests would call this a summons and be right to. It is beneath the floor of your own chambers and nowhere else, patient as a tide, and it has been three weeks.\n\nYour faith teaches that what speaks from the empty prison speaks only to those it means to use — your elders still argue over whether it is Orrin the Eye or something he left behind — and that being used by it is the nearest thing to grace this cosmos still offers. You find that you are not frightened. You find that this frightens you." (Waits on the cult-identity ruling, §6.) |
| 65 | `eotg_void.0002.desc_bloodline` | "…Eight hundred and sixty-six years is not long enough, it turns out, for a bloodline to finish falling through a hole." | "Your family has a word for this that appears in no dictionary, passed down with the estate and the debts. Nobody ever explained it. Everyone always knew.\n\nIt is beneath the floor of your chambers and nowhere else, and it is speaking in the cadence your grandmother used when she thought the room was empty. All the centuries since the Grip have not been long enough, it turns out, for a bloodline to finish falling through a hole." |
| 85 | `eotg_void.0004.desc` | "…Harbouring her is a capital matter in every realm that matters." | Change "Harbouring" to "Harboring". Under §3e "worship" or "both", also change "learning to close these things" to "learning to keep these things shut". |
| 88 (lore check) | `eotg_void.0004.c` | "Hand her to the Elrossi. They have been waiting five hundred years." | "Hand her to the Elrossi. They have been waiting a long time for her kind." ("Five hundred years" does not fit the 200–700 AG hunts at 866 AG.) |
| 93 | `eotg_void.0010.desc` | "It does not come as a voice this time. It comes as a certainty arriving fully formed in your own interior language, the way your own thoughts arrive, which is precisely how you know it is not one.\n\nThe offer is not complicated. There is a great deal on the other side of the seal that has had eight hundred and sixty-six years and nothing whatever to do, …" | "It does not come as a voice this time. It comes from the far side of the room, at the very edge of hearing, and it is still there when you turn to face it and nothing is.\n\nThe offer is not complicated. Whatever waits beyond the scar has had a very long time and nothing whatever to do, and it is willing to lend a portion of that attention to your affairs. It will make you better at the one thing you were raised to be good at. It is specific about this. It knows what that thing is.\n\nIt asks for nothing you would miss immediately. That is the part you cannot stop turning over." |
| 94 | `eotg_void.0010.desc_cult` | "It comes the way your faith always promised it would: not as a voice but as a certainty, arriving in your own interior language, indistinguishable from your own thought except that you did not think it.\n\nOrrin the Eye is sealed and cannot act, and this is what the sealed do — they lend. A portion of eight hundred and sixty-six years of undivided attention, …" | "It comes the way your faith always promised it would: not as a voice in the room but as something just past the edge of hearing, patient, from no direction you can point to.\n\nYour priests have argued for centuries over what speaks from the empty prison. Some still name it Orrin the Eye; others say the Eye is long gone and something else stayed behind. Tonight the argument seems very small. Whatever it is, it lends, and it is turning a portion of its long, undivided attention on your affairs, sharpening the one thing you were raised to be good at. Your priests have described this moment your whole life. None of them mentioned that it would be courteous.\n\nIt asks for nothing you would miss immediately. Your faith says that is because there is nothing worth keeping that you would miss immediately." |
| 95 | `eotg_void.0010.desc_bloodline` | "It arrives in your own interior language, fully formed, indistinguishable from your own thought — and it is using the family word. …" | "It comes up through the floor, at the very edge of hearing, and it is using the family word. The one from the estate papers that nobody ever defined.\n\nThe offer is not complicated, and it is not new. It has been made to your line before. You understand, with a clarity you would rather not have, that the reason your family has the word at all is that someone once accepted, and that the reason it was never explained is that they had nothing good to report.\n\nIt will make you better at the one thing you were raised to be good at. It asks for nothing you would miss immediately. It is patient in the specific way of something that has done this before and is prepared to do it again." |
| 103 | `eotg_void.0011.desc` | "…The seal is thin here. It has been getting thinner since long before you were born, …" | "You understand, somewhere around the third hour, that you have been treating this as a negotiation with two parties in it.\n\nThe scar is thin here. It has been getting thinner since long before you were born, and your refusal, however sincerely meant, was never load-bearing. Nothing is asking now. The cold goes through the middle of you and keeps going, unhurried, the way water finds the low ground.\n\nWhat is left to decide is only how you are standing when it finishes." |
| 110 | `eotg_void.0020.desc` | "…In the field the thing in you is not a burden at all; it is the most useful instrument you have ever been handed, and every single person who fights beside you now knows it exists." | "The line breaks in front of you and you cannot account for it. You did nothing. You raised no weapon and gave no order — you simply looked along the enemy front, and the men there stopped being willing.\n\nYour own knights saw it happen. Two of them have not met your eye since. In the field the thing that follows you is not a burden at all; it is the most useful instrument you have ever been handed, and every single person who fights beside you now knows it is there." |
| 120 (if not made real) | `eotg_void.0021.c` | "Send them to be fostered somewhere far from here." | "Keep them away from your table, and from you." |
| 125 | `eotg_void.0022.desc_cult` | "…and then they name it correctly, as favour. … They say the realm has been waiting eight hundred and sixty-six years for a ruler the seal recognises, …" | "Your confessor has been building to this for a year and delivers it in open court, in the full voice, so that no one can later claim they were not there.\n\nThey name the condition — and then they name it correctly, as favor. They say the Eye does not lend its attention to the unworthy and does not lend it twice. They say the realm has waited since the Grip for a ruler the Void would recognize, and that the ordinary faiths call this corruption because the ordinary faiths were not offered anything.\n\nThey kneel. Half the hall kneels with them. You had not previously known the count." ("The Eye" stays because a character is speaking, which counts as belief under the ERRATA.) |
| 128 (if not made real) | `eotg_void.0022.c` | "Have them silenced. Tonight, and permanently." | "Rebuke them before the court, harshly enough that no one repeats it." |
| 140 | `eotg_void.0024.desc` | "…a great deal of that was not entirely you.\n\n…the thing that has been lending you its attention does not appear to have noticed, … and will still be here afterward looking for somewhere to put itself. …" | "You have carried this longer than most people carry a marriage, and the arrangement has been, in its way, honest. It took what it took. It gave what it promised. You have ruled a long time and ruled well, and a great deal of that was done with something standing just past the edge of hearing, lending its attention.\n\nWhat has changed is the arithmetic. There is less ahead than behind now, and the thing at the edge of hearing does not appear to have noticed, or does not appear to care, and will still be out there afterward, looking for somewhere else to lend itself.\n\nThe question is no longer what it wants from you. It is what you intend to leave behind, and to whom." |
| 155 | `eotg_void.0030.desc` | "There is no moment. … and instead there is a Tuesday. … You watch yourself construct a reassuring answer out of nothing at all and deliver it in your own voice, and you note, from somewhere behind your own eyes, that it works." | "There is no moment. That is the thing nobody warns about — you keep waiting for the moment, and instead there is an ordinary working day.\n\nYou hold court. You rule competently, more competently than you ever have. You settle three disputes that had been running for years and you settle them correctly, and at no point during any of it do you want anything, or mind anything, or find any of it to be happening to you.\n\nAfterward your steward asks whether you are well. You give a reassuring answer, made out of nothing at all, and it works. Nothing in you minds that it works. Somewhere at the edge of hearing, past the far wall, something has gone quiet in the way a thing goes quiet when it is finished." |
| 156 | `eotg_void.0030.desc_cult` | "…Your steward asks whether you are well. You watch yourself assemble a reassuring answer out of nothing at all, and deliver it, and note from behind your own eyes that it works. …" | "There is no moment, and your faith did warn you of that. The scriptures are specific: the Eye does not arrive, it finishes.\n\nYou hold court. You rule better than you ever have — three disputes settled correctly that had run for years — and at no point do you want anything, or mind anything, or find any of it to be happening to you. This is the state your order has spent five centuries describing as the end of the noise.\n\nYour steward asks whether you are well. You give a reassuring answer, made out of nothing at all, and it works, and nothing in you minds. Past the edge of hearing, the noise your order promised would end has ended. The scriptures did not mention what the quiet would sound like. You suspect the ones who got this far stopped writing." |
| 159 | `eotg_void.0030.c` | "Abdicate now, while the decision is still recognisably yours." | If made real: "Abdicate now, while the decision is still recognizably yours." If reworded (recommended): "Name your heir before the court, while the choice is still recognizably yours." |
| new | `eotg_mod_void_aura_desc` | — (missing) | "The air near this character sits a degree too cold, and something just past the edge of hearing seems to follow them from room to room. Prayer comes harder in their company." |
| `eotg_l_english.yml:5` (with §3a) | `eotg_grip_survivor_desc` | "This character's bloodline traces back to those who endured the horrors of Orrin's Grip — the tunnel through the hells that shattered the Second Material Plane. …" | "This character's bloodline traces back to those who lived through the Grip. The family carries a resilience nobody chose, and an old unease nobody ever quite explains." (This drops "Orrin's Grip", which SETTING LORE `:117,365` uses for a *different* ~131–180 AG event, and drops "tunnel through the hells". Lore-keeper should confirm.) |

**Other spelling fixes and a check:**
- **British spellings fixed above:** `:28`, `:34`, `:41`, `:85`, `:125` (×2), `:159`. A grep of the file found no others.
- **Left alone, but lore-keeper should confirm:** `:45` ("hunted across five centuries", which fits 200–700 AG); `:85` ("between the second and seventh centuries", "four hundred years"); `:156` ("five centuries", the order's own history); "Elrossi" at `:85,88,124` (§6).

---

## 5. UNVERIFIED-VANILLA (for vanilla-scout)

1. `yearly_playable_pulse`. This one is checked: pitfalls §12 cites vanilla `yearly_on_actions.txt:973`. What is unverified is whether a list of `on_actions` runs in the listed order, and whether an on_action's `effect` runs before its `on_actions`.
2. `create_character` fields (`template`, `location`, `employer`, `save_scope_as`), the shape of a `scripted_character_templates` entry (gender, age, skills, culture/faith inheritance), and `root.capital_province`.
3. `faith = { religion_tag = … }`; `has_doctrine` for a mod tenet; the shape of a mod tenet in `common/religion/doctrines/`.
4. Whether `add_character_modifier` without a duration stacks or refreshes.
5. Abdication (`depose`, or a vanilla abdicate effect), fostering / guardian effects, `imprison`.
6. Event themes `corruption`, `disaster`, `dread`, `secret`, `mental_health`, `war`, `family`, `faith`, `learning`, `vassal`. Animations `disbelief`, `scheme`, `paranoia`, `personality_bold`, `personality_rational`, `personality_cynical`, `grief`, `fear`, `shock`.
7. Modifier and trait keys: `advantage`, `max_hostile_schemes_add`, `monthly_lifestyle_xp_gain_mult`, `dread_baseline_add`, `attraction_opinion`, `fertility`.
8. Traits and triggers: `lunatic_1`, `lunatic_genetic`, `possessed_1`, `possessed_genetic`; `has_education_*_trigger`; `piety_level`; `stress >= 200`; `every_knight`; `primary_heir`; `random_child`; `remove_short_term_gold`; `clamp_variable`; `trigger` inside a `random_list` entry.
9. Decisions: whether `<key>_confirm` loc is picked up by default (v1 has no `confirm_text`); `is_valid_showing_failures_only`; `cost = { piety = }`; the `picture = { reference = "gfx/interface/illustrations/decisions/decision_misc.dds" }` path.
10. Which trait name loc key the engine reads, `trait_<key>` or `<key>`. v1 defines both (`:3-10`; `eotg_l_english.yml:7-8`).
11. Console syntax for seeding `eotg_void_exposure` in the play-test.

## 6. Open questions (human / lore-keeper)

1. Is Void mod-exclusive, so it can be built on the temporary map before Gate 1 (§0)?
2. Voidwalkers: worshippers (SETTING LORE `:144,270`), wardens (v1), or both (§3e)?
3. Who does the Void cult revere? Malvrick (v1 religion `eotg_religions.txt:930,961`), "Carrigore and the Void" (`:929`), "the breach itself" (`866_religions:132`), or Orrin (loc `:64`, as belief)?
4. Is "the seal" acceptable as a neutral in-world word for the Void boundary, or is it retired with the "sealed Orrin" framing? The §4 drafts use "the scar".
5. Should the Void text name the Elrossi as the hunters (`:85,88,124`)? An Elrossi ruler gets "Hand her to the Elrossi".
6. "Five hundred years" (`:88`) and "four hundred years" (`:85`): what are the canon spans for the Voidwalker hunts?
7. `eotg_grip_survivor_desc`: does the trait refer to The Grip (~1,000 years before 866) or "Orrin's Grip Emergence" (~131–180 AG, SETTING LORE `:117,365`)? This ties to audit §3 Q1, the Grip date.
8. Band name "Void Undertow": approve, or pick another (§3c)? The orchestrator should grep the cybernetics loc for the word first.
9. Is stage D's trait-as-resource exception to invariant 5 acceptable (§3d)?
10. The v2 map docs call the sea "Deep Void" (`docs/terrain_conversions.md:102`). If that reaches player-visible loc, does it collide with the canon Void (cf. audit `:246`, "Voidfarers")?
11. Should the Voidwalker be female and lone, as the loc describes, with template faith left open until B-FAITHS?

---

## 7. Orchestrator review notes (cloud)
- **Spot-checked** against the v1 sources:
  - `eotg_st_void_venerates`: 24 grep hits, which is 1 definition plus 23 uses;
  - the two ward-cooldown durations (10 years at `eotg_void_effects.txt:254`, 8 years at `eotg_void_decisions.txt:88`);
  - the Voidwalker flag mismatch;
  - the 0010 desc text.
- **Loc drafts still need a lore-keeper pass** (step 9).
  - The 0020.desc draft keeps v1's "the men there stopped being willing". Under the multi-species rule (cybernetics_v2 §5 item 5), consider "the soldiers there".
  - "five centuries" in the 0030.desc_cult draft is carried over from v1, and waits on open question 6.
- **Links to the canon dossier** (`docs/specs/canon_decisions_cloud.md`):
  - open question 2 (Voidwalkers) is dossier §5;
  - open question 7 (Grip vs Orrin's Grip) is dossier §1.

## 8. Handoff
### HANDOFF (cloud session, unvalidated)
- **branch:** `claude/canon-void-glossary-cloud`
- **status:** done (proposal; nothing ruled)
- **files:** `docs/specs/void_lift_plan_cloud.md`
- **unverified-vanilla:** §5 (11 items).
- **needs-local-validation:** step 10, once built.
- **needs-loc:** §4 drafts, after rulings (c) and (e).
- **needs-lore:** step 9; open questions 2–7.
- **needs-human:** open question 1 (is Void mod-exclusive?) and the §3 rulings via the architect.
- **taskboard (proposed):**
  - CB-11 next step: "architect rules on void_lift_plan_cloud.md §3";
  - a CB-12 sibling for the Void cult gate (option 2 after B-FAITHS);
  - a deferral for a stage-D variable (§3d option 2).
