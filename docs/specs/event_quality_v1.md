# Spec: Event quality v1 (presentation, voice, craft)

**Author:** eotg-architect, 2026-10-08
**Input:** [`docs/qa/event_quality_vs_vanilla_2026-10-08.md`](../qa/event_quality_vs_vanilla_2026-10-08.md) (the "report", commit d14188c). The three owner decisions at its top supersede its findings 2–4. This spec turns its "Suggested order" into work items W1–W11.
**Owner rulings in force:**
- **R1 (voice).** The narration mix is about 60% first person (root narrates), about 35% neutral or third person, and about 5% second person (letters, short option and outcome lines).
- **R2 (trait gates).** Trait depth stays. Gates vary by personality, education (`education_*`, `skill =` icon) and title tier. Don't stack several personality traits on one event. There is no option cap.
- **R3 (quotes): RULED.** The owner confirmed it on 2026-10-08, relayed by the orchestrator. Dialogue uses vanilla's straight double quotes inside the string, unescaped (§12.2), with `#EMP …#!` for stress. This **reverses** the single-quote house style; §12.4 lists every document that must change.
- **Q1, Q2, Q3: RULED** 2026-10-09 (owner: "follow recommendations"; relayed by the orchestrator). Q1: the quote conversion runs now. Q2: W7 and the NEW half of W9 are approved. Q3: the Seamless fade is staged once, at the threshold only, as a record and not a speaker. Details in §16.
- **L-1: ANSWERED** by eotg-lore-keeper 2026-10-09. Seamless has no first person; Neurofractured is full first person. Folded into §8, §12.1 rule 7 and `cybernetics_v2_procedures_lore.md` §(c).
- **Voice baseline (2026-10-09).** The ported `eotg_event_quality.py` measures **74% second person** on the main desc keys. The report's 52% could not be reproduced and appears to be a hand count. The orchestrator accepts 74% as the "before" figure and keeps this spec's classifier (§15).

**State read:** the working tree on `v2-space-map` at d14188c, plus vanilla 1.20.0.3. Counts marked *(re-measured)* come from this session's scratch scripts on the current tree, not from the report.

**Rewrite or new content.** The owner's rule still applies: new events, options and beats need the owner's approval (memory "event expansion is the user's call"). Every work item is classed:
- **REWRITE:** changes to existing events, options and text. These are dispatchable.
- **NEW:** new content. It needs owner approval first (§16).

---

## 1. Purpose & gate

The mod's events work in logic but read and look medieval and samey. Every event shows a vanilla throne room or torchlit study. Narration drifted to second person, characters rarely speak, many events read as "pick your personality", and outcomes land silently. This spec sets the rules and the work order that bring the 249 non-hidden mod events to vanilla's craft baseline using **vanilla assets only**. Art (item 10) and the 1.20 stress-block form (item 11) are parked.

**Gate.** This is quality work on **mod-exclusive systems** (cybernetics, Frontier), so it is exempt from the Gate 1 block, the same basis as `loc_dynamic_terms_ruling.md`. It references no title, province, culture or faith. One caveat feeds into §14: vanilla background keys resolve by the root's culture and government, and the mod has no cultures yet. That is why §14 uses mod-owned background keys.

**Ownership** follows `loc_dynamic_terms_ruling.md`. Cybernetics files belong to the Cybernetics Modding session and Frontier files to whoever holds Frontier, both routed through the orchestrator. Agents named below act in that session's context.

---

## 2. Signature resource

There is no game resource here. The **signature measure is the event-quality scorecard**: the per-file metrics from `docs/tools/eotg_event_quality.py` (W0b, §15). Every work item names the scorecard columns it must move, and QA judges each item by the before/after scorecard.

**Invariant 5 is protected, not served.** No rewrite may remove or weaken an existing read or move of a system resource: `eotg_fracture_risk`, tier, `eotg_aug_voice`, kingpin and Frontier variables. QA proves this with `docs/tools/qa/risk_moves.py` and `option_outcomes.py` (§9).

---

## 3. Identifier table

| Key | Type | Owner | Notes |
|---|---|---|---|
| `eotg_bg_corridor_night` | event background | eotg-scripter | §14.1 (vanilla image `corridor.dds`) |
| `eotg_bg_private_quarters` | event background | eotg-scripter | `bedchamber.dds` |
| `eotg_bg_clinic` | event background | eotg-scripter | `study_physician.dds` |
| `eotg_bg_holding_cell` | event background | eotg-scripter | `dungeon.dds` |
| `eotg_bg_council` | event background | eotg-scripter | `councilchamber.dds` |
| `eotg_bg_underlevel_night` | event background | eotg-scripter | `alley.dds` |
| `eotg_bg_underlevel_day` | event background | eotg-scripter | `alley_day.dds` |
| `eotg_bg_office` | event background | eotg-scripter | `study.dds` |
| `eotg_bg_battlefield` | event background | eotg-scripter | `battlefield.dds` |
| `eotg_bg_field_camp` | event background | eotg-scripter | `genericcamp.dds` |
| `eotg_bg_command_tent` | event background | eotg-scripter | `ep3_military_tent.dds` |
| `eotg_bg_vault` | event background | eotg-scripter | `fp4_catacombs.dds` |
| `eotg_bg_cavern` | event background | eotg-scripter | `fp3_cave.dds` |
| `eotg_bg_barren_world` | event background | eotg-scripter | `drylands.dds` |
| `eotg_bg_riot` | event background | eotg-scripter | `raid_burning.dds`; on probation, see §14.1 |
| `<event_id>.toast`, `<event_id>.toast_<variant>` | loc keys | eotg-localizer | W3; same form as vanilla `ep3_story_cycle_admin_eunuch.toast` |
| `<event_id>.msg`, `<event_id>.msg_<variant>` | loc keys | eotg-localizer | W3, `send_interface_message` titles |
| `<desc_key>_v2`, `<desc_key>_v3` | loc keys | eotg-localizer | W8 `random_valid` openings |
| `<event_id>.opening` | loc key | eotg-localizer | W9 letter conversions |
| `eotg_aug_cl_*` (new entries) | customizable loc | eotg-scripter (`common/`), eotg-localizer (text) | W8; extends the existing family |
| `docs/tools/eotg_event_quality.py` | tool | orchestrator (tooling session) | W0b |
| `docs/tools/eotg_quote_convert.py` | tool | orchestrator (tooling session) | W0e |
| eotg_lint `L013e` quote style, `L015` missing background, `L017` stacked personality gates | lint rules | orchestrator (tooling session) | Provisional numbers; the tool owner may renumber |

There are no new namespaces, events, flags, variables or modifiers. Icons: none. Fullscreen `queue_icon` art is deferred (§10).

---

## 4. File placement

| What | Path |
|---|---|
| Background database (new folder for the mod) | `common/event_backgrounds/eotg_event_backgrounds.txt`. **The orchestrator adds `common/event_backgrounds/` to the CLAUDE.md placement list** (precedent: vanilla splits the folder over `01_event_backgrounds.txt` and `activity_backgrounds.txt`). |
| Event edits | `events/eotg_augmentation_*.txt`, `events/eotg_frontier_events.txt` (no new files) |
| Loc | the existing files: `localization/english/eotg_augmentation_l_english.yml`, `eotg_aug_inherit_l_english.yml`, `eotg_aug_kingpin_l_english.yml`, `eotg_frontier_l_english.yml` (UTF-8 BOM) |
| Customizable loc (W8) | `common/customizable_localization/eotg_augmentation_*.txt` (existing family) |
| Tools | `docs/tools/eotg_event_quality.py`, `docs/tools/eotg_quote_convert.py`, tests in `docs/tools/tests/` |
| Generated scorecard | `docs/qa/generated/event_quality.md` + `.json` (same convention as the other generated reports, with `--check`) |
| Gemini drafts (optional) | `docs/proposals/voice_rewrite_gemini_<batch>.md` |

---

## 5. Wiring

**No on_action changes.** Every item edits events that are already fired. Rules carried from v1:
- Re-gating changes **option** triggers only. Never add an event-level `trigger = {}`, and never touch cooldowns; cooldown authority stays in the on_action.
- Letter conversions (W9) keep the event id and every `trigger_event` caller. Only `type`, `sender`, `opening` and the window change.
- Tier gates use `highest_held_title_tier` on root. The augmentation events fire on `yearly_playable_pulse`, which includes landless characters (`loc_dynamic_terms_ruling.md` §0.5). A tier gate simply hides the option from them, which is safe. Desc text must still not call `GetCapitalLocation` unguarded.

---

## 6. Vanilla precedent (verified in 1.20.0.3 this session)

| Technique | Vanilla file:line |
|---|---|
| `override_background = { reference = estate }` | `events/dlc/ep3/ep3_admin_events.txt:436` |
| Field shape for override_background, effect_2d, sound | `events/_events.info:251-275` |
| Background database entry (`background = { trigger reference environment ambience }`) | `common/event_backgrounds/_event_backgrounds.info:1-40` |
| 2D effect keys: `smoke`, `fog`, `flies`, `legend_glow` | `common/event_2d_effects/event_2d_effects.txt`; use at `events/activities/coronation_activity/coronation_events.txt:1426` |
| Trait option pairing: `trigger = { has_trait = shy }`, `trait = shy`, stress entry for that trait | `events/dlc/ep2/wedding_events/ep2_wedding_events_ewan.txt:3759-3778` |
| Skill icon on option: `skill = intrigue` | `events/dlc/bp3/bp3_survey_events.txt:1093-1095`; field doc `_events.info:208` |
| Education gate by group: `has_trait = education_intrigue` | `events/dlc/ep3/ep3_story_cycle_admin_eunuch_events.txt:2740` (68 uses for intrigue across `events/`) |
| Tier condition | `highest_held_title_tier >= tier_duchy`, `events/councillor_task_events/chancellor_task_events.txt:2026` |
| Trait-variant option name (one option, text keyed to a trait) | `events/dlc/ep3/ep3_admin_events.txt:512-523` |
| Trait-keyed portrait reactions | `events/dlc/ep3/ep3_camp_temperament_events.txt:317-352` |
| Toast `send_interface_toast = { type = event_toast_effect_bad title left_icon right_icon }` | `events/dlc/ep3/ep3_story_cycle_admin_eunuch_events.txt:748-754`. Types are defined in `common/messages/00_messages.txt:102-149` (`event_toast_effect_good/neutral/bad`, `send_interface_message_good/bad`). |
| `send_interface_message` to another player | `events/dlc/ep3/ep3_admin_events.txt:653-659` |
| `play_music_cue` in `immediate` | `events/birth_events.txt:2756-2757`; cue keys `music/in_game/music.txt` (`mx_cue_death`:275, `mx_cue_murder`:372, `mx_cue_prison`:261, `mx_cue_illness`:365, `mx_cue_stress`:358) |
| `add_internal_flag = dangerous` / `special` | 84 and 187 uses across `events/` |
| Letter event (`type = letter_event`, `opening`, `sender`, `after`) | `events/dlc/bp2/bp2_hostage_system.txt:675-760` |
| Anonymous letter | `window = anonymous_letter_event`, `events/dlc/ep3/ep3_contract_events.txt:8598` |
| Fullscreen set piece (needs `queue_icon`) | `events/dlc/ce1/legend_ending_events.txt:10-53` |
| `big_event_window` for major beats | `_events.info:19`; `events/bookmark_events.txt` |
| Inner dialogue quotes | §12.2 |

**Deviation, stated.** Vanilla references its background keys directly. This spec routes through mod-owned `eotg_bg_*` keys pointing at vanilla images (§14), for three reasons:
1. The mod has no cultures yet, and vanilla keys switch image by culture and government. The tribal, nomadic and landless-adventurer branches turn `council_chamber` into a tent (`01_event_backgrounds.txt:1426-1756`), and the mod's Unclaimed holder is herder-style.
2. Mod keys resolve the same way everywhere.
3. The art track (W10) then replaces one `reference =` per key, and every event updates with no per-event work.

---

## 7. Loc surface

| Work item | Keys | Estimate |
|---|---|---|
| W1/W4 voice and dialogue | Existing desc keys, text replaced, keys unchanged | **about 430** second-person desc keys *(re-measured; the report's "about 360" counted a narrower set)*, plus any option lines the batch touches |
| W0e quotes | Existing keys with `'…'` speech, converted | **40** *(re-measured: inherit 19, kingpin 11, augmentation 10)*, plus manual-review hits |
| W5 re-gating | Existing option keys, text replaced to fit the new axis | about 130 *(re-measured: 117 events gate 2+ personality traits, 13 of them gate 3)* |
| W3 toasts and messages | New `<event_id>.toast*`, `.msg*` | about 120 toasts, about 15 messages (estimate) |
| W8 variety | New `<desc_key>_v2/_v3` openers; new `eotg_aug_cl_*` text | about 40 events × 2, plus about 30 vocabulary entries |
| W9 letters | New `<event_id>.opening` | 1 per converted event |
| W7 set pieces (NEW) | Lengthened desc text on 6 events | after approval |

**`replace/`:** none. No vanilla string needs an override.

**eotg_lint L014** (loc key conventions) must accept the `.toast`, `.msg` and `.opening` suffixes and `_v2`/`_v3`. The tooling owner updates `eotg_lint_loc_conventions.json` in W0c.

---

## 8. Lore constraints

- **Cybernetics register** (`cybernetics_v2.md` §5 rules 1–8) binds every rewritten line:
  - the voice is internal, "you, a half-second early";
  - the banned list;
  - licensing is never named;
  - no monotheistic invocations;
  - "self", not "humanity";
  - the medieval-leak substitutions.
- The **Seamless and Neurofractured registers** were restated for first-person narration by the lore-keeper (L-1, 2026-10-09) in `cybernetics_v2_procedures_lore.md` §(c), which binds. Seamless has no first person ("Seamless ends the self", SETTING LORE ERRATA :76-77; `cybernetics_v2.md` Q9 :42); Neurofractured is full first person. The working form is §12.1 rule 7. The batches no longer skip these keys.
- The Kingpin (`cybernetics_v2_kingpin.md` §7.4) and Inheritance (`cybernetics_v2_fracturing_inheritance.md` §7.1) lore wording tables still bind word for word. Only the quote characters change.
- **No time-of-day words** in cybernetics text (GQF-002; still open project-wide in CB-47). §14 avoids "night" and "day" in mod key *names* for that reason. The images themselves are lighting only.
- **Backgrounds:**
  - No religious building is used, because faiths vary: no `temple*`, church, cathedral or `holy_site*` keys.
  - No throne room or courtyard, by owner direction.
  - No image tied to a real place: no `ep3_constantinople*`, `hagia_sophia` or `holy_site_jerusalem`.
- **Canadian English and no dashes** (eotg_lint L013a/b). A rewrite may not reintroduce a word the dynamic-terms ruling made dynamic.
- Uncertain canon (for example, what a Frontier sponsor's courier looks like) goes to eotg-lore-keeper, never into text as a guess.

---

## 9. Definition of done

These are end-state targets, measured by `eotg_event_quality.py` on the 249-event corpus. Each work item also has its own DoD (§11).
1. **Background:** `override_background` is set on every non-hidden event except the 6 activity events and the 13 "keep" events in §14.2 (230 of 249). Any event added to the keep list later needs a reason in its batch report. Every reference is an `eotg_bg_*` key.
2. **Voice** (main desc key per event): first person ≥ 50%, second person ≤ 10%, the rest neutral. The aim is about 60/35/5. The "before" figure is **74% second person** (the ported scorecard, 2026-10-09). **Seamless keys are exempt from the first-person floor**: they are excluded from the first-person denominator and counted only against the second-person ceiling, so the metric never pushes a writer back to "I" (§12.1 rule 7). A Seamless key is one whose text is gated on `eotg_total_integration` or belongs to the threshold set (end.009 Seamless outcome, end.010, fracture.027); the scorecard takes the list from a pinned set in its tests, not from a regex.
3. **Dialogue** in ≥ 40% of events, against 8% today. 0 keys with `'…'` speech, and 0 keys with escaped `\"`.
4. **Gates:** 0 events with 2+ options gated on root's personality traits, except owner-approved lint allows. Each file with ≥ 5 gated options has ≥ 1 education gate and ≥ 1 tier gate. **No personality trait's gated count** in `docs/tools/qa/trait_coverage.py` falls below min(its 2026-10-08 count, 3). Every kept personality option has the full pairing (icon, trigger, stress entry).
5. **Outcomes:** ≥ 0.5 toasts per event, and ≥ 15 options flagged `dangerous` or `special`.
6. **Portraits:** `triggered_animation` ≥ 0.3 per event, and ≥ 80 distinct animations.
7. **Resource safety:** `risk_moves.py` totals per file are unchanged, except where an item's batch report lists a change approved through the orchestrator. `event_graph.py` shows no new orphans.
8. **Tooling:**
   - Tiger is clean except the known-benign list in CLAUDE.md.
   - PX LSP and vocab: no new findings.
   - eotg_lint: no new findings against the baseline.
   - `loc_mechanical.py`: clean under its updated quote rule.
9. **In game** (human, CB-44 session): one event from each `eotg_bg_*` key renders, and one converted dialogue line renders with its quotes visible.

---

## 10. Deferred

| Item | Why | Re-open when |
|---|---|---|
| W10 sci-fi backgrounds, themes, outfits, fullscreen splash plates and `queue_icon` | Needs art (B-ART). The report recommends backgrounds come first when art starts. | Art starts: replace each `eotg_bg_*` `reference`, then consider `common/event_themes/eotg_*`. |
| W11 `stress_impact` → `stress_and_fulfillment_impact` (310 blocks) | Tiger 1.17 doesn't know the new form; the old form still works (vanilla keeps 174 uses). | CB-18 clears (Tiger for 1.20); then one mechanical pass. |
| `window = fullscreen_event` for the endgames | Vanilla's fullscreen plates are period paintings, and `queue_icon` needs a splash icon. W7 uses `big_event_window` now. | W10 art. |
| Court events (`type = court_event`) | Royal Court is DLC-gated and needs a fallback; low gain. | Owner asks. |
| `outfit_tags` other than `nightgown` | Vanilla outfits are period clothing. | W10 (implant portrait track). |
| Option cap | R2 removed it. | Never, unless the owner reopens it. |

---

## 11. Work order

The phases run in order. Items inside a phase can run in parallel if they touch different files.

| Phase | Items | Starts when |
|---|---|---|
| **P0** rules and tooling | W0a–W0e (W1's rules, scorecard, lint, quote pilot, quote converter) | now |
| **P1** backgrounds | W2 | after W0b, which takes the "before" scorecard |
| **P2** outcomes and sound | W3 | after P1, or in parallel on other files |
| **P3** per-file sweep | W1 (voice), W4 (dialogue), W5 (re-gating), W6 (portraits), W0e apply | after the **current cybernetics loc batches**: the dynamic-terms ruling applied, and CB-46 Kingpin batch B localized. Batch order is in §13.3. |
| **P4** variety | W8 | per file, after that file's P3 batch |
| **P5** set pieces (NEW, approved 2026-10-09) | W7 | after the architect's W7 addendum; the six events' P3 batch (B4/B5/B7) first |
| **P6** letters | W9 (REWRITE and NEW parts, both approved 2026-10-09) | after P3 for the file |
| parked | W10, W11 | §10 |

New text written in the meantime follows §12 from the day it is dispatched. That includes CB-46 batch B, which is drafted against the old rules. Batch B's loc is written in the new voice and quote form, so it never needs a second pass.

### W0a: Rules into the binding docs (report item 1, the rules half). REWRITE
- **Scope:** §12 of this spec is the binding voice and quote text. Update every document in §12.4 to point to it or to match it.
- **Files:** those in §12.4 (`docs/` only), plus `.claude/agents/eotg-localizer.md` (a one-line pointer; configuration, so the orchestrator and owner apply it).
- **Owner:** orchestrator.
- **Precedent:** report "Owner decisions".
- **DoD:** `grep -rniE "single quote|' for speech|never \`\\\\\"\`"` over `docs/proposals docs/specs docs/qa .claude/agents` returns only historical records annotated "superseded 2026-10-08".
- **Risk:** low. A missed brief means a Gemini or cloud draft arrives in the old style, which W0e catches.

### W0b: Port the measurement script into `docs/tools/eotg_event_quality.py`. REWRITE (tooling)
- **Scope:** Port the loc-review session's `evq.py`. It lives in a temp scratchpad (`…/88c59e56-…/scratchpad/evq/evq.py`, 86 lines) and **may be deleted**, so port it first. Add the metrics the report computed by hand; §15 has the full list. Output `docs/qa/generated/event_quality.{md,json}`, with `--check` and a `--vanilla` switch so the vanilla baseline can be re-run.
- **Owner:** orchestrator (tooling session); eotg-qa runs it.
- **Precedent:** the other generated reports in `docs/tools/qa/README.md`.
- **DoD:**
  - On the d14188c tree it reproduces the report's mod column within ±2 points: background 0%, dialogue 8%, trait icons 31%, toasts 0.12. **Voice is the exception:** the port measures 74% second person, against the report's 52%, which was not reproducible (a hand count). The orchestrator accepted 74% as the "before" figure on 2026-10-09; the classifier stays as §15 defines it.
  - It is committed with the "before" scorecard.
  - It is added to `check_all.py`.
- **Risk:** the regex-based voice and dialogue detection is ±5 points (report caveat). Pin the classifier in tests so that drift is visible.

### W0c: Lint and checker updates. REWRITE (tooling)
- **Scope:**
  - **L013e** quote style:
    - ERROR on an escaped `\"` in a mod loc value;
    - WARN on a `'…'` speech pair (same detector as W0e);
    - ERROR on a trailing comment after the closing quote that contains `"`.
  - **L015:** WARN when a non-hidden, non-activity mod event has no `override_background`.
  - **L017** *(proposed as L016; renumbered 2026-10-08 because L016 is the BOM rule)*: WARN when an event has 2+ options gated on root personality traits. Exempt with `# eotg_lint: allow L017 <reason>`.
  - **Invert `docs/tools/qa/loc_mechanical.py:57-58`.** It currently prints `INNERQUOTE` for every unescaped inner `"`, the very form vanilla uses. Change it to flag `\"` and odd quote counts instead.
  - L014 conventions get the new suffixes (§7).
- **Owner:** orchestrator (tooling session).
- **DoD:**
  - Tests in `docs/tools/tests/test_eotg_lint.py` cover each new rule, including the vanilla line forms in §12.2.
  - Today's tree produces the expected L015/L017 counts (243/117 ±2; L015 skips the "keep" list once W2 records it as allows), and the baseline is regenerated on purpose.
- **Risk:** the L017 personality-trait set must come from vanilla `00_traits.txt` (`category = personality`), not a hand list.

### W0d: Quote pilot. REWRITE
- **Scope:** Convert **one** key by hand, `eotg_aug_heir.003.desc` (§12.3 example 3).
- **Owner:** eotg-localizer; then eotg-qa runs Tiger, PX LSP, `loc_mechanical.py` and eotg_lint; then a human views it in game.
- **Precedent:** §12.2.
- **DoD:**
  - The tools report no new finding on the key.
  - In game, heir.003 shows `"Step aside,"` with visible straight quotes, and the rest of the desc after the second inner quote renders.
- **Risk:** this proves the parser behaviour in the mod's own context (PX's parser in particular is unproven) before the mass conversion.

### W0e: Convert existing single-quoted speech: a separate, scripted, reviewable pass. REWRITE
- **Status (Q1 RULED 2026-10-09):** run now. eotg-localizer is applying it in order: the W0d pilot, then the 40 AUTO keys, then the 13 REVIEW items by hand.
- **Scope:** Every mod loc file in `localization/`, using `docs/tools/eotg_quote_convert.py`. Design:
  - **Dry-run by default.** It prints a unified diff per file, an `AUTO` count and a `REVIEW` list, and writes nothing. `--apply` writes. It keeps the BOM, line endings, key, `:0` version and any trailing comment byte for byte.
  - **Parsing.** Value = from the first `"` after `key:N ` to the last `"` before an optional `# comment`. The same greedy rule vanilla's lines need (§12.2).
  - **Masked before detection:**
    - `[ … ]` data functions, so `Custom('X')` and `GetCouncillorPosition( 'councillor_steward' )` are never touched;
    - `$KEY$` references;
    - `#FMT` / `#!` tokens;
    - literal `\n`.
  - **A `'` is never a delimiter** when it has a letter or digit on **both** sides (`don't`, `Konan's`, `it's`). Such a `'` is skipped outright.
  - **Opener:** a `'` at value start, or after whitespace, `\n`, `(` or `:`, and followed by a non-space.
  - **AUTO closer:** a `'` immediately preceded by `[.,!?]` and followed by end, whitespace, `\n` or `[,.;:)]`. Only an opener and AUTO-closer pair on the same paragraph, with no masked region inside it, converts automatically.
  - **Goes to the REVIEW list, never converted:**
    - a closer preceded by a letter, as in a quoted single word (`'we'` in fracture.022) or a possessive plural (`the soldiers' mess`);
    - an unpaired opener;
    - a pair spanning `\n\n`;
    - any `'` that starts a word, such as `'em`.
  - **Converts to** an unescaped `"`. Never `\"`.
  - **Post-check per changed value:** the inner `"` count is even, there is no `\"`, and no `'` delimiter is left inside a converted span.
  - **Tests** use fixtures: `Konan's`, `don't`, `the soldiers' quarters`, `Custom('KnightCulture')`, `'we'`, speech at value start (vanilla `tournament_events.9004.desc` shape), speech at value end (`hold_court.7000.desc` shape), and nested speech across `\n\n`.
- **Owner:**
  - the orchestrator (tooling session) writes the script and tests;
  - eotg-localizer runs the dry-run, hand-resolves the REVIEW list and applies;
  - eotg-qa reviews the diff.
- **Sequencing:**
  - Run it once after W0d and before P3, so P3 starts from double quotes.
  - Re-run it per P3 batch for any stragglers.
  - Gemini and cloud drafts written with `\"` (for example `docs/proposals/kingpin_text_gemini_r1.md`) are converted to an unescaped `"` when they are applied, never to `'`.
- **DoD:**
  - The dry-run diff is attached to the QA report.
  - After apply: 0 `'…'` speech pairs (L013e), 0 `\"`, and every REVIEW item resolved by hand and listed in the batch report.
  - The per-key text, apart from the quote characters, is byte-identical to before, which the script asserts.
- **Risk:** possessive plurals and single-word mentions. Both are routed to REVIEW by construction. Speech **inside** a `[...]` function argument is never converted.

### W1: Voice rewrite (report item 1, the text half). REWRITE
- **Scope:** about 430 second-person desc keys, in batches by event file (§13.3), following the §12.1 rubric. Seamless and Neurofractured keys are in scope from 2026-10-09 under §12.1 rule 7 (L-1 answered). The threshold keys (end.009 Seamless outcome, end.010, fracture.027) are written with W7, not in their batch.
- **Owner:** eotg-localizer writes; eotg-lore-keeper reviews each batch; eotg-qa runs the scorecard and loc checks.
- **Precedent:** vanilla first-person narration ("As I am exploring the grounds…", `tournament_activity_oltner_l_english.yml:11`).
- **DoD per batch:**
  - The file's first-person share in the main desc ≥ 50%, and second person ≤ 10% outside letters. **Seamless keys are exempt from the first-person floor** (§9 item 2); they must instead carry no I/me/my/we/our in narration (a batch-report grep).
  - Neurofractured keys pass the §12.1 rule 7 banned list (no second speaker, no quoted implant lines, no "the voice", no possession framing, no Void lexicon or Carrigore).
  - No banned or register term (L012).
  - L011 pronoun checks pass.
  - The lore-keeper signs off.
- **Risk:**
  - Tone loss: second person served the dissociation. §12.1 keeps that effect through "I" against the forecast "we" in the ruler's own mouth.
  - Pronoun slips: "you" left in narration. The batch report greps for it.
  - Batches collide with other loc work, so only one batch per loc file is in flight at a time.
- **Gemini queue (optional):** the drafts are raw material only (memory: GeminiQA was 39% false, and Gemini drifts medieval). If one is used:
  - the brief must embed §12.1 with its examples, the §8 constraints, the banned-word table, the dynamic-terms ruling and a "script-truth" rule (never change `[functions]`);
  - output goes to `docs/proposals/voice_rewrite_gemini_<batch>.md`;
  - the localizer authors the final text.

### W2: Backgrounds and 2D effects (report item 2). REWRITE
- **Scope:** create `common/event_backgrounds/eotg_event_backgrounds.txt` with the 15 keys in §14.1, then set `override_background` (and `override_effect_2d` where listed) on every event per §14.2.
- **Owner:** eotg-scripter. Kingpin events go after CB-46 batch B, or inside it.
- **Precedent:** §6.
- **DoD:**
  - §9 item 1.
  - Every `eotg_bg_*` key exists and is used at least once.
  - Each entry carries `reference`, `environment` and `ambience` copied from the cited vanilla line, with no `trigger`.
  - L015 shows 0 findings.
  - The CB-44 in-game spot check is done.
- **Risk:**
  - `raid_burning.dds` may read too medieval. It is on probation: if it does, swap to `eotg_bg_underlevel_night` + `smoke`.
  - Ambience strings name castle rooms; they are audio only and harmless, and the art track may drop them.

### W3: Outcome surfacing: toasts, messages, flags, music (report item 3, plus the music half of item 7). REWRITE
- **Scope:**
  - **Toasts:** a `send_interface_toast` on every **delayed or rolled outcome**: each `random_list` or `duel` branch, each follow-up event's resolving option, each Frontier stage change and each syndicate move. Use `event_toast_effect_good`, `_neutral` or `_bad` by the outcome's direction for root, with `left_icon = root` and `right_icon` = the other party when one exists. Toast titles say what happened, never a number, odds or "risk" (cybernetics rendering rules).
  - **`send_interface_message`** to an affected **other** character when they may be a player: the heir in heir and inherit events, the vassal hit by a policy, the champion in `nr.*`.
  - **Flags:**
    - `add_internal_flag = dangerous` on options that can kill or imprison root, start a cascade, or hand over control. Examples: awake excision (procedures), end.009's handover options, executing on a flag (fracture.020), kingpin crackdown branches.
    - `special` on rare opportunities (once per life, or gated by a rare state).
  - **Music:** `play_music_cue` in `immediate`:
    - `mx_cue_death` on cascade deaths and executions;
    - `mx_cue_murder` on heir.005;
    - `mx_cue_prison` on end.030, end.031 and kingpin.013;
    - `mx_cue_illness` on tier1.013–.015.

    At most one cue per event.
- **Owner:** eotg-scripter; eotg-localizer writes the toast and message titles.
- **Precedent:** §6.
- **DoD:**
  - §9 item 5.
  - Every hidden-meter outcome (fracture risk, countdown) has a toast that names the visible consequence only.
  - Tiger clean.
  - No toast fires from an AI-only path. Guard with `is_ai = no` where the vanilla pattern does, or rely on toasts being player-only.
- **Risk:**
  - Toast spam on yearly flavour. A toast goes only on outcomes, never on the opening beat.
  - A toast that leaks hidden numbers. QA greps the toast loc against the rendering rules.

### W4: One line of NPC dialogue per eligible event (report item 4). REWRITE
- **Scope:** every event whose desc features a named NPC who speaks: vassals, envoys, physicians, the heir, the spouse, the delegation, kingpin bosses, Frontier backers. Give them one line of direct speech in vanilla quotes (§12.2), done inside the same P3 batch as W1.
- **Owner:** eotg-localizer, with eotg-lore-keeper for voice.
- **Precedent:** `hold_court_events_james_l_english.yml:3`.
- **DoD:** §9 item 3, per batch: dialogue in ≥ 40% of the file's events wherever the file has ≥ 40% NPC events. Kingpin and inherit should go well above.
- **Risk:** the voice register. NPCs never voice the implant, and the implant's voice lines are not "dialogue" (rule 1).

### W5: Re-gating (report item 5, superseded by R2). REWRITE
- **Scope:** about 117 events. Apply the §13 rubric in the same P3 batch as W1, because re-axed options need new text.
- **Owner:** eotg-scripter (triggers, icons, stress, `ai_chance`), then eotg-localizer (text), then eotg-qa.
- **Precedent:** §6 rows 4–7.
- **DoD:** §9 item 4. Each batch report lists every option re-axed, folded or kept, with the trait coverage before and after.
- **Risk:**
  - Breaking G9. The eight G9 options are protected (§13.1).
  - Losing a resource move when folding. Folding is only allowed for options with no distinct resource move (§13.1 step 3c).

### W6: Portrait pass (report item 6). REWRITE
- **Scope:** in the same P3 batch, for each event:
  - root gets `triggered_animation` reactions keyed to traits (paranoid → `paranoia`; wrathful or callous → `anger`; compassionate → `crying`), with the current animation kept as the fallback;
  - NPCs get role animations (`physician`, `spymaster`, `chancellor`, `throne_room_bow_1`, `threatening`, `beg`);
  - a lower portrait is added for witnesses (heir.005, tier3.006, fracture.004);
  - `outfit_tags = { nightgown }` in tier3.003 and tier3.013;
  - `hide_info = yes` for anonymous syndicate couriers.

  All the named animations exist in `gfx/portraits/portrait_animations/animations.txt` (checked this session).
- **Owner:** eotg-scripter.
- **Precedent:** `ep3_camp_temperament_events.txt:317-352`.
- **DoD:** §9 item 6. Tiger shows no unknown-animation errors.
- **Risk:** low. A lower portrait needs its scope to exist, so guard it with `exists`.

### W7: Endgame set pieces. NEW, APPROVED (Q2 RULED 2026-10-09)
- **Q3 (RULED 2026-10-09):** the Seamless threshold fade is staged here and nowhere else: the end.009 Seamless outcome, end.010 and, optionally, fracture.027. The text turns into the **log register** (§12.1 rule 7); it is a record, not a speaker.
- **Scope:** fracture.027 The Cascade, end.009 Hand Over the Controls, end.010 There Is No Static, fracture.004 The Court Massacre, heir.005 What Must Be Done, end.002 Silence. For each:
  - `window = big_event_window` now; fullscreen waits for art (§10);
  - longer text, 90–140 words in 2–3 `\n\n` paragraphs;
  - an `override_effect_2d`;
  - a music cue (W3 has already put the death and murder cues on some of these).
- **Owner:** eotg-architect writes a short addendum after approval; then scripter, localizer, lore and QA.
- **Precedent:** `legend_ending_events.txt:10-53`; `_events.info:19`.
- **DoD:** after approval. The six events reach the vanilla 90th-percentile length (≥ 85 words).
- **Risk:** "longer text" adds beats. The addendum lists each added sentence for the lore-keeper.

### W8: Variety: `random_valid` openings and Custom loc (report item 8). REWRITE (text variants, no new beats)
- **Scope:**
  - Repeatable tier flavour events, those whose on_action can fire them more than once per character, get 2–3 opening variants via `random_valid`.
  - New `eotg_aug_cl_*` entries add vocabulary: implant slang, clinic nouns, a "static" vocabulary.
  - Vanilla relation and address functions are used in text: `Custom2('RelationToMe', …)`, `FormOfAddressForLiege`.
  - Paragraphs break at the beat with `\n\n`.
- **Owner:** eotg-localizer, with eotg-scripter for the `desc = { random_valid = { } }` blocks and the customizable-loc entries.
- **Precedent:** `random_valid` is in 3% of vanilla DLC events; customizable loc follows `common/customizable_localization/00_councillor_custom_loc.txt`.
- **DoD:** `random_valid` ≥ 10% of events; Custom loc ≥ 20%; paragraphing ≥ 60%.
- **Risk:** a variant that drifts in meaning. Every variant must carry the same facts as the original opener.

### W9: Letter conversions (report item 9). Mixed
- **REWRITE:** whole events whose entire content already is a letter.
  - Frontier.003 *An Offer of Backing* and frontier.030 *A Rival Backer* become `type = letter_event` with `sender` = the backer and an `opening`.
  - patron.009 *The Collector* (if its desc is entirely the debt-sale notice; the scripter checks) and patron.008 *The Paper* use `window = anonymous_letter_event` if the sender is the unsigned syndicate.
- **NEW** (APPROVED, Q2 RULED 2026-10-09):
  - patron.006's `*_absent` variant ("A courier brings the final account, sealed") is a desc variant inside a character event. Making it a letter means splitting off a new event.
  - Unsigned syndicate notes as separate beats.
- **Owner:** eotg-scripter, then eotg-localizer (the `opening` text is in the sender's second-person voice, the R1 5% bucket).
- **Precedent:** `bp2_hostage_system.txt:675-760`; `ep3_contract_events.txt:8598`.
- **DoD:**
  - The converted events have `sender` and `opening`.
  - Every `trigger_event` caller is unchanged (`event_graph.py`).
  - The letter count in the scorecard is ≥ 3.
- **Risk:** a letter needs a sender who is alive and exists. Each conversion needs a fallback to `character_event`, or a sender guarantee.

### W10 and W11: parked (§10).

---

## 12. House rules: voice and quotes (binding on all loc text from 2026-10-08)

### 12.1 Voice rubric (R1)
1. **The narrator is root**, whoever root is: the ruler, the heir in heir events, the liege in `nr.*`. Main desc openers are **first person, present tense**, as most mod text already is. Map you → I or me, your → my, yourself → myself, and fix verb agreement ("you are" → "I am").
2. **Generic "you"** ("you can't tell where it starts") becomes neutral ("there is no telling where it starts"). Don't use "one".
3. **Appended fragments** (`triggered_desc` additions about the court, NPCs or consequences) are **neutral or third person**. When they refer to root, they use me and my.
4. **Root's name** in narration, `[ROOT.Char.GetFirstName]`, becomes "I" unless an NPC is saying it.
5. **Second person is allowed only in:**
   - letters (the sender to the reader);
   - NPC speech inside quotes;
   - short option or outcome lines where vanilla also uses it.
6. **The forecast "we".** First person makes the implant's intrusions sharper: the narrator's "I" against the "we" that the forecast puts in the ruler's own mouth (fracture.022) is the effect that replaces second person's dissociation. The "we" is always the ruler's spoken word or an option line, never a line the model says. Keep every existing "we" line; don't add new ones (that is a beat). (L-2, eotg-lore-keeper 2026-10-09.)
7. **Seamless and Neurofractured** (L-1 answered by eotg-lore-keeper 2026-10-09; Q3 RULED; binding source `cybernetics_v2_procedures_lore.md` §(c)).
   - **Seamless has no first person.** "Seamless ends the self" (SETTING LORE ERRATA :76-77; `cybernetics_v2.md` Q9 :42). In steady state:
     - narration is neutral and log-like, with no narrating subject: no I, me, my, we or our;
     - "you" becomes a neutral referent ("the body", "the chair", "the hand", "the [court seat]") or the passive;
     - lines are short declaratives; residue lines end logged, filed or pruned (procedures_lore ruling (a));
     - the court still speaks and feels, and quotes may say "you";
     - options are imperative or a bare acknowledgement.
     - Exemplars: `end.042.desc`, `end.040`.
   - **The threshold fade (Q3)** is staged once, at the threshold only: the end.009 Seamless outcome, end.010 and, optionally, fracture.027 (all W7). The text turns into log entries: timestamps, "logged", "filed", "Next item". The log never says I or we and never addresses anyone, and the "I" never returns afterwards. Call it the **log register**, never "the implant's voice". Sample: "I can see the forecast for the next thought. I am reading it. Reading complete. Next item."
   - **Neurofractured is full first person**: a degrading self.
     - *Allowed:* gaps and missing time; the forecast running ahead (a known sentence end, ready answers with a confidence figure, a forecast filed as memory); hearing one's own words late; overlay text that labels me; motor pre-emption as granted and logged access; unreliable narration set against the log; feelings.
     - *Banned:* a second speaker (no "it tells me / says / answers", no quoted implant lines, no addressing the implant); "hearing the voice"; possession framing; the Void lexicon and Carrigore; giving the implant wants or decisions.
   - **Rule 6 and the second-speaker ban (L-2, answered 2026-10-09).** fracture.022's "we" lines are the ruler's own speech, so they are not a second speaker. They are kept. B5 converts them to first person like any other key.
   - **Scorecard:** Seamless keys are exempt from the first-person floor (§9 item 2, W1 DoD).
8. **Options** are first person or imperative ("Let them watch.", "I will speak to them myself."), as today.
9. **Length** keeps the existing band unless the event is a W7 set piece. Break paragraphs at the beat with `\n\n`.
10. **Unchanged:** Canadian English, no dashes, the register and banned lists, and dynamic terms.

### 12.2 Quote form (R3, RULED): verified in vanilla 1.20.0.3
- **Form:** an **unescaped** straight double quote inside the loc string: `key:0 "Narration. "Speech," [x.GetSheHe] says."`
  - CK3's loc reader takes the value as running to the **last** `"` on the line, so inner quotes need no escape.
  - In vanilla `localization/english/`, **8,677** lines carry more than two unescaped quotes, against **89** lines using `\"` (the coronation oath lines). The unescaped form is the standard.
- **Cited lines:**
  1. `localization/english/event_localization/hold_court_events/hold_court_events_james_l_english.yml:3`, `hold_court.7000.desc`. Mid-string speech that ends the value: `…?""`.
  2. `localization/english/activities/tournament_activity_oltner_l_english.yml:11`, `tournament_events.9001.desc`. Speech with `#EMP [liegeless_knight.GetHouse.GetMotto]!#!` inside the quotes.
  3. `localization/english/activities/tournament_activity_oltner_l_english.yml:43`, `tournament_events.9004.desc:0 ""Go, #EMP [falconer_1.Custom('GetBirdName')|U]#!, go faster!" I hear…`. Speech that **opens** the value.
- **Stress:** `#EMP …#!` around the stressed word or phrase, at most once per event (vanilla is at 14%). Example: `"It closed #EMP before#! I decided."`
- **Never** `\"` (mod rule, for one form only; it parses but is the minority form), and never a `"` in a trailing `# comment` on a loc line.
- **Single words mentioned or quoted** also use `"` ("I said "we"."). Apostrophes stay `'`.
- **The parser fact is inferred** from the vanilla corpus, not documented anywhere. W0d proves it in the mod's own context (Tiger, PX, game) before W0e runs.

### 12.3 Worked examples (current text → target)
1. **First person, fracture.016.desc.**
   - Before: "You wake with blood on your sleeve. It is dry. The cuff is stiff with it, and the implant's log for the past few hours is a clean, blank line."
   - After: "I wake with blood on my sleeve. It is dry. The cuff is stiff with it, and the implant's log for the past few hours is a clean, blank line."
2. **First person plus a W4 line, tier3.013.desc.**
   - Before: "[eotg_finder.GetFirstName] found you in the lower corridor … Your eyes were open. You did not respond to your name for almost a minute, and you have no idea how you came to be there."
   - After: "[eotg_finder.GetFirstName] found me in the lower corridor while it was empty, standing at a sealed door with one hand on the lock. My eyes were open.\n\n"You did not know your own name," [eotg_finder.GetSheHe] tells me. "Not for almost a minute." I have no idea how I came to be there."
3. **Quote conversion and voice, heir.003.desc (the W0d pilot).** As a loc line:
   ` eotg_aug_heir.003.desc:0 "The incident logs, a signed statement from my physician and a date: [eotg_heir.GetFirstName] has brought all three. [eotg_heir.GetSheHe|U] is not shouting. "Step aside," [eotg_heir.GetSheHe] says, "or I will make you." It is a prepared sentence. [eotg_heir.GetSheHe|U] rehearsed it, and it still cost [eotg_heir.GetHerHim] to say."`
4. **The model's "we", fracture.022.desc.**
   - After: "I said "we". I was giving an order, in my own voice, and the word came out as if it had always been there: "We will not be moving the fleet." The order stood uncorrected. Someone at the table looked up."
5. **Already neutral: no change.** tier2.002.desc ("The youngest ones flinch now…") stays as it is. Neutral narration is the 35% bucket.
6. **Allowed second person, a W9 letter opening:** "[ROOT.Char.GetFirstName], the account is closed. You will not hear from us again."

### 12.4 Documents and rules to update (owner confirmed R3; nothing may still say "single quotes")
| # | Where | Today | Change | Who |
|---|---|---|---|---|
| 1 | `docs/proposals/kingpin_fragments_r1_apply_instructions.md:22` (G1) | "Write speech in single quotes, never `\"`" | Superseded note: speech in unescaped `"` (event_quality_v1 §12.2). The batch B drafts' `\"` convert to `"`. | orchestrator |
| 2 | `docs/proposals/gemini_brief_inherit_text_2026-10-06.md:43` | "Speech goes in single quotes ('…'), never `\"`" | Same note | orchestrator |
| 3 | `docs/proposals/gemini_work_queue_2026-10-06.md:21` (the Gemini queue **template**, per memory) | "single quotes for speech; never `\"`" | Rewrite the rule. Add §12.1 voice. | orchestrator |
| 4 | `docs/proposals/gemini_rewrite_feedback_2026-10-06.md` §3 "In-voice samples" (lines 72-74) | samples written `"'The leads took…'"` | Re-quote the samples in `"…"` form. Add a voice line: "narrate in first person". | orchestrator |
| 5 | `docs/specs/cybernetics_v2_kingpin.md` §7.4 and `docs/specs/cybernetics_v2_fracturing_inheritance.md` §7.1 (lore wording) | approved lines are given between Markdown `"…"`; **no single-quote mandate found** | Add a one-line note at each section head: "Speech in these lines is rendered with inner `"` (event_quality_v1 §12.2); first person per §12.1." The wording itself is unchanged. | eotg-architect (next pass on those specs) |
| 6 | `docs/specs/cybernetics_v2_procedures_lore.md` §(c) Seamless register | written for second person | **Done 2026-10-09.** Restated for first person per L-1; N5's heir.004 line marked superseded. | eotg-lore-keeper → architect |
| 7 | `docs/qa/variety_pass_2026-10-07.md:212` (QA checklist "no embedded double quote is used") | treats an inner `"` as a defect | Annotate "superseded 2026-10-08". Future checklists check for "no `\"`, no `'…'` speech". | orchestrator |
| 8 | `docs/tools/qa/loc_mechanical.py:57-58` | prints `INNERQUOTE` for every unescaped inner `"` | Invert (W0c) | tooling |
| 9 | eotg_lint | **no rule enforces quotes today** (L013a–d are dashes, spelling, whitespace, `\n\n`) | Add L013e (W0c); document it in `eotg_lint.md` | tooling |
| 10 | `.claude/agents/eotg-localizer.md` | silent on voice and quotes | One-line pointer to §12. Configuration change, owner-approved. | orchestrator |
| 11 | The report's finding 3 recommendation ("keep second person") | superseded | The report's header already says so. No edit. | none |
| 12 | Memory `feedback_event_voice_house_style.md` | already states R1–R3 (updated by the loc-review session; indexed in MEMORY.md) | No change. Memory `feedback_gemini_writing_briefs.md` has no quote rule. | none |

---

## 13. Re-gating rubric (R2)

**Definition.** A *personality gate* is an option whose `trigger` requires **root** to have a `category = personality` trait (vanilla `common/traits/00_traits.txt`). Gates on another character's trait, such as tier2.004.e's chaste spouse, don't count.

**Today** *(re-measured)*:
- events by number of personality gates: 0 in 70 events, 1 in 62, 2 in 104, 3 in 13;
- 305 personality-gated options;
- 31 education or skill options;
- **0 tier-gated options**.

### 13.1 Per-event procedure
1. **Inventory** the event's gated options with their axis (W0b scorecard, `--event`).
2. **Keep at most one personality-gated option.** Choose in this order:
   - (a) a **G9 option** (`cybernetics_v2_trait_depth.md` §5.1; the eight are protected and never re-gated);
   - (b) the trait with the **thinnest coverage**: `trait_coverage.py` "gated" ≤ 3 is protected (on 2026-10-08: lustful, chaste, gluttonous, temperate, patient, impatient, content, arbitrary);
   - (c) the trait the option's text most depends on.
3. **Re-axis each other personality option:**
   - (a) **Competence-flavoured** (knowing how: a ledger, a diagnosis, a tactical read, rhetoric) → **education gate**:
     - `trigger = { has_trait = education_<skill> }` and `skill = <skill>`;
     - no `trait =` icon;
     - `ai_chance` modifiers switch to the education trait.
   - (b) **Authority-flavoured** (commanding, ceremony, adjourning, calling on vassals or levies) → **tier gate**:
     - `trigger = { highest_held_title_tier >= tier_duchy }` for lord-scale actions, `>= tier_kingdom` for realm-scale actions;
     - never gate on `tier_county` alone, which is every landed ruler;
     - no icon.
   - (c) **Neither, and no distinct resource move** → **fold.** Retire the option. Its trait survives on the closest situational option as:
     - a `name = { trigger = { has_trait = X } text = … }` variant (vanilla `ep3_admin_events.txt:512-523`);
     - that trait's stress entry;
     - an `ai_chance` modifier.

     An option **with** a distinct resource move must be re-axed (a or b), never folded.
4. **The trait's stress entry** moves with the trait. If the re-axed option no longer fits the trait, keep the trait's stress row as a *response* on the option that does (vanilla keys stress to traits on ungated options too).
5. **Pair the kept personality option the vanilla way:** `trait =` icon, `has_trait` trigger and a stress entry for that trait (`ep2_wedding_events_ewan.txt:3759-3778`). Add whichever piece is missing.
6. **Spread per file:**
   - no single education skill holds more than 50% of a file's education gates;
   - every file with ≥ 5 gated options ends with ≥ 1 education gate and ≥ 1 tier gate.
7. **Text.** The localizer rewrites the re-axed option's text so it reads as that axis. The key stays the same. Effects don't change, apart from `ai_chance`.
8. **Coverage floor:** no trait's gated count falls below min(its 2026-10-08 count, 3) (§9 item 4).

### 13.2 Worked example: tier1.005 *Weight of Silence*
Today it has three personality gates: d [shy], e [gregarious], f [gluttonous, G9].
- **f stays.** It is a G9 option, and gluttonous has 3 gates (protected).
- **e "Make it theatre." becomes an education gate.** It is about rhetoric, so it is competence: `has_trait = education_diplomacy`, `skill = diplomacy`. New text: "Turn the pause into ceremony, and make them wait on my word." Prestige +100, dread +5 and risk +5 are unchanged. The `gregarious` stress row moves to option b ("Make light of it."), which is gregarious-shaped.
- **d "Leave the hall." becomes a tier gate.** Exiting by right is authority: `highest_held_title_tier >= tier_duchy`. New text: "Adjourn. The gathering is mine to end." Its effects (prestige −50, risk +2) are unchanged. `shy` keeps its stress loss as a response on d, ungated; shy's gate count goes from 6 to 5.
- **Result:** one personality gate, one education gate and one tier gate, the same option count, no resource move lost. That is three different players who see a special answer.

### 13.3 Batch order (P3; each batch = W1 + W4 + W5 + W6 for one file set)
After the current cybernetics loc batches (the dynamic-terms ruling applied; CB-46 batch B localized). Counts are second-person desc keys and stacked events *(re-measured)*.

| Batch | Files | 2nd-person keys | Events with 2+ personality gates | Note |
|---|---|---|---|---|
| B1 | tier1 | 38 | 13 | Most-seen content. Pilot for the rubric; review before B2. |
| B2 | tier2 | 36 | 16 | |
| B3 | tier3 | 46 | 17 | Seamless keys in scope under §12.1 rule 7 (no first person; exempt from the first-person floor) |
| B4 | fracture .001–.014 | about 33 | about 11 | Neurofractured keys in scope: full first person, §12.1 rule 7 allowed/banned lists |
| B5 | fracture .015–.029 | about 34 | about 11 | L-2 answered 2026-10-09: fracture.022 is in scope, with the lore-approved text below; fracture.027 is W7 |
| B6 | initiation | 29 | 11 | |
| B7 | countdown, endgame, heir | 40 | 10 | W7 set pieces (approved) are written with W7, not here; carries the four Seamless shipped-text fixes below |
| B8 | patron, procedures, tamper, interactions, realm | 42 | 7 | patron letters are W9 |
| B9 | retinue, nonruler, activities | 29 | 15 | activities keep their activity backgrounds |
| B10 | inherit | 40 | 3 | 19 keys of `'…'` speech, already converted by W0e |
| B11 | kingpin | 54 | 3 | after CB-46; batch B is already written in the new voice |
| B12 | frontier | 9 | 0 | Frontier owner; mostly neutral already, so a light pass |

**fracture.022 first-person text (L-2, lore-approved 2026-10-09; eotg-localizer items in batch B5).** `eotg_fracture.022.desc` stays as in §12.3 example 4 (approved); the options are unchanged.

| Key | Text |
|---|---|
| `eotg_fracture.022.desc_first` | "\n\nThis is the first time I have caught it. The word did not feel like a slip. It felt like the more accurate pronoun, applied half a second before I chose it." |
| `eotg_fracture.022.desc_known` | "\n\nI saw it coming. The model has been treating my decisions as joint for some time, and I have been letting it. Now the grammar has caught up in public." |

**Seamless shipped-text fixes (L-1, 2026-10-09; eotg-localizer items in batch B7).** Existing keys whose shipped text breaks the no-first-person register. Lore-keeper wording, applied as given:

| Key | New text (or replacement) |
|---|---|
| `eotg_aug_heir.004.desc_seamless` | "\n\nThey address the chair. There is no one else in it to address." (supersedes procedures_lore N5) |
| `eotg_aug_end.041.desc_residue_high` | "...the head tilts the way it once did for listening." |
| `eotg_aug_end.041.desc_residue_low` | "Nothing in the face at the head of the table has moved." |
| `eotg_aug_end.011.desc`, `.desc_named` | the root reference becomes "the [court seat]" (the dynamic council-seat term per the dynamic-terms ruling) |
| `eotg_aug_end.011.desc_none` | "...watch the chair." |

The localizer fits the end.041 and end.011 phrases into the existing sentences without adding beats; each residue line still ends logged, filed or pruned (procedures_lore ruling (a)).

---

## 14. Background mapping

### 14.1 The mod's background keys (W2)
Each key is one `background = { reference environment ambience }` block, copied from the cited vanilla fallback entry in `common/event_backgrounds/01_event_backgrounds.txt`, with **no trigger**. Every `.dds` was checked to exist under `gfx/interface/illustrations/event_scenes/`.

| Key | Vanilla key (fallback image) | 01_ line | environment | Scene class |
|---|---|---|---|---|
| `eotg_bg_corridor_night` | `corridor_night` (`corridor.dds`) | 1251 | `environment_event_corridor` | wandering, missing persons, sleepwalking, discoveries, the door, plots |
| `eotg_bg_private_quarters` | `bedchamber` (`bedchamber.dds`) | 8016 | `environment_event_bedchamber` | waking, sleeplessness, private episodes, mirror, spouse alone |
| `eotg_bg_clinic` | `physicians_study` (`study_physician.dds`) | 8830 | `environment_event_study_physician` | licensed surgery, physicians, rejection, recovery |
| `eotg_bg_holding_cell` | `dungeon` (`dungeon.dds`) | 3065 | `environment_event_dungeon` | restraints, locked wing, custody, wards |
| `eotg_bg_council` | `council_chamber` (`councilchamber.dds`) | 1749 | `environment_council` | delegations, warrants, council, succession politics, petitions, audiences |
| `eotg_bg_underlevel_night` | `alley_night` (`alley.dds`) | 299 | `environment_event_alley` | back-street clinics, syndicate, kingpin, couriers, errands |
| `eotg_bg_underlevel_day` | `alley_day` (`alley_day.dds`) | 407 | `environment_event_alley_day` | vendors, contraband, street trade |
| `eotg_bg_office` | `study` (`study.dds`) | 8232 | `environment_event_study` | ledgers, contracts, reports, audits, records |
| `eotg_bg_battlefield` | `battlefield` (`battlefield.dds`) | 465 | `environment_event_battlefield` | combat, engagements, cascades in the field |
| `eotg_bg_field_camp` | `army_camp` (`genericcamp.dds`) | 10031 | `environment_event_genericcamp` | Frontier camps, retinue drill, bouts |
| `eotg_bg_command_tent` | `ep3_military_tent` (`ep3_military_tent.dds`) | 451 | `environment_ep3_military_tent_interior` | war councils, campaign orders |
| `eotg_bg_vault` | `ce1_catacombs` (`fp4_catacombs.dds`) | 15648 | `environment_ce1_catacombs` | the quiet room, aftermath of death, ruins |
| `eotg_bg_cavern` | `fp3_cave` (`fp3_cave.dds`) | 10793 | `environment_event_sittingroom` | Frontier finds, seams |
| `eotg_bg_barren_world` | `drylands` (`drylands.dds`) | 3351 | `environment_event_desert` | Frontier surveys, supply runs |
| `eotg_bg_riot` | `burning_building` (`raid_burning.dds`) | 7550 | `environment_ep3_constantinople_on_fire` | crackdowns, regions falling (on probation, see W2) |

The ambience string is copied from the line after `environment` at the cited vanilla line.

**Rejected, with reasons:**
- every `throne_room*`, `courtyard*` and `feast*` key (owner direction);
- `temple*`, `church` and `holy_site*` (faiths vary);
- `gallows` (medieval);
- `docks` (sailing ships);
- `tavern` and `market` (period trade);
- `armory` (racks of swords);
- `ep3_constantinople*` (a real place);
- `tgp_examination_room` (the Chinese examination hall);
- `terrain` and `wilderness` (they need a location or scope and pick vanilla landscapes by terrain).

### 14.2 Event → background (W2 default; the scripter reads each desc and may move an event to another class, listing the move in the batch report)
Legend: **CN** corridor_night, **PQ** private_quarters, **CL** clinic, **HC** holding_cell, **CO** council, **UN** underlevel_night, **UD** underlevel_day, **OF** office, **BF** battlefield, **FC** field_camp, **CT** command_tent, **VA** vault, **CV** cavern, **BW** barren_world, **RI** riot. `+smoke`, `+fog` and `+flies` mean `override_effect_2d`. **keep** means no override: family, love, marriage and friendly themes resolve to vanilla's relaxing or sitting rooms, which are acceptable until art.

- **activities** 001–006: keep (activity locales)
- **countdown:** 001 PQ · 002 CN+fog · 003 PQ · 004 CN · 005 keep · 006 PQ
- **endgame:** 001 CL · 002 CL · 009 PQ · 010 PQ+fog · 011 CO · 020 CO · 030 HC · 031 HC · 040 OF · 041 CO · 042 PQ
- **fracture:** 001 BF+smoke · 002 BF+smoke · 003 PQ · 004 CO+smoke · 005 CN · 006 CO · 007 OF · 008 keep · 009 CN+fog · 010 PQ · 011 PQ · 012 keep · 013 PQ+fog · 014 CN · 015 OF · 016 PQ · 017 PQ · 018 PQ+fog · 019 OF · 020 OF · 021 CN · 022 CO · 023 CT · 024 CO · 025 CO · 026 PQ · 027 PQ+smoke · 028 PQ · 029 PQ
- **heir:** 001 keep · 003 CO · 004 CO · 005 CN · 007 keep
- **inherit:** 001 OF · 002 keep · 003 CL · 004 CN · 005 CO · 006 keep · 007 keep · 008 HC · 009 CN · 010 CL · 011 UN · 012 UN · 013 CO · 014 CO · 015 UN · 016 OF · 017 CN+smoke · 018 CO · 019 VA · 020 CN · 021 CL · 022 keep · 023 HC · 024 CL · 025 CO · 026 CO · 027 VA
- **initiation:** 001 BF · 002 UD · 003 PQ · 004 BF+smoke · 005 CL · 006 CL · 007 CL · 008 PQ · 009 OF · 010 UN · 011 PQ · 012 CL · 013 VA · 014 CL · 015 keep · 016 FC · 017 CL · 018 OF · 019 CT · 020 FC
- **interactions:** 001 CL · 002 CL
- **kingpin:** 001 UN · 002 CO · 003 UN · 004 OF · 005 UN · 006 CN · 007 UN · 008 OF · 009 UN · 010 HC · 011 RI+smoke · 012 UN+smoke · 013 HC · 014 UN+flies · 015 OF · 040 CO · 060 HC · 061 UD · 062 OF · 068 CN · 069 CO · 070 CO · 071 RI+smoke · 073 OF · 074 UN · 075 CN · 076 UD
- **nonruler:** 001 FC · 002 FC · 003 CN · 004 CN · 005 PQ · 006 VA
- **patron:** 001 OF · 002 OF · 003 OF · 004 UN · 005 OF · 006 CO · 007 CO · 008 OF · 009 UN
- **procedures:** 001 CL · 002 CL · 003 UD · 004 CL · 005 CL · 020 PQ
- **realm:** 001 UD
- **retinue:** 001 FC · 002 FC · 003 FC · 004 FC · 005 CO
- **tamper:** 002 UN · 003 UN · 004 CL
- **tier1:** 001 PQ · 002 CL · 003 CO · 004 CO · 005 CO · 006 BF · 007 PQ · 008 CL · 009 PQ · 010 FC · 011 CO · 012 CO · 013 CL · 014 CL · 015 CL · 016 FC · 017 FC · 018 CL · 019 CL · 020 PQ · 021 CL · 022 CL
- **tier2:** 001 CO · 002 keep · 003 CL · 004 PQ · 005 CO · 006 CO · 007 OF · 008 VA · 009 OF · 010 keep · 011 OF · 012 CO · 013 OF · 014 UD · 015 CN · 016 CL · 017 PQ · 018 PQ · 019 OF · 020 PQ · 021 OF
- **tier3:** 001 CO · 002 PQ · 003 PQ · 004 PQ+fog · 005 BF · 006 CO · 007 CN · 008 PQ · 009 CT · 010 PQ+smoke · 011 CO · 012 PQ · 013 CN · 014 OF · 015 FC · 016 PQ+fog · 017 CN · 018 CO · 019 CO · 020 keep · 021 CT · 022 CL+fog · 023 CT · 024 BF+smoke
- **frontier:** 001 CO · 002 OF · 003 OF · 004 CO · 005 FC · 010 CO · 020 BW · 021 FC · 030 OF · 031 CO · 032 OF · 033 FC · 034 BW · 035 CV · 036 CV · 037 VA · 040 UD · 041 CO · 042 FC

That is 230 events overridden and 19 kept: the 6 activity events plus 13 family, love and friendly scenes. The 13 non-activity keeps are the whole exception list for §9 item 1.

---

## 15. QA gates and the scorecard tool

**Porting `evq.py`.** Keep its parsing: comment strip, brace blocks, non-hidden filter, desc key resolution through loc. Per event, add:
- `override_background` key(s);
- `override_effect_2d`;
- `window`;
- letter type, `sender` and `opening`;
- `send_interface_toast`, `send_interface_message` and `play_music_cue` counts (including inside `after` and options);
- `add_internal_flag` value;
- `triggered_animation` count and distinct animation set;
- `outfit_tags`;
- `random_valid`;
- `Custom(`/`Custom2(` in the desc text;
- `#EMP`;
- `\n\n`.

**Voice classifier** on the main desc key:
- strip speech first: `"…"` pairs inside the value, `\"…\"` and legacy `'…'`;
- strip `[…]`;
- count first-person (I, me, my, mine, myself) against second-person (you, your, yours, yourself) words outside speech;
- label `1st` / `2nd` / `neutral`. Pin it with tests.

**Gate axes per option:**
- personality (from vanilla `00_traits.txt` `category = personality`, root only);
- education or `skill =`;
- `highest_held_title_tier` in the option `trigger`;
- other.

**Per-event:** personality-gate count, which feeds L017.

**Output and flags:**
- per-file and total tables, with the vanilla-DLC column from `--vanilla`;
- `--event <id>` for a single event's breakdown (used in §13.1 step 1);
- `--check` for staleness.

**Per-phase gate:** each phase's QA report attaches the scorecard diff (before → after) for the files it touched. QA fails a batch when any §9 target the batch owns is missed and the batch report does not explain it.

**Always run (CLAUDE.md):**
- Tiger, with the log to the scratchpad;
- PX LSP and vocab;
- eotg_lint against the baseline;
- `loc_mechanical.py`;
- `trait_coverage.py`, `risk_moves.py`, `option_outcomes.py` and `event_graph.py` before and after.

---

## 16. Owner and lore questions (few)
- **Q1 (owner): RULED 2026-10-09.** Run the quote conversion now. *(Asked: should W0a/W0e run ahead of the voice rewrite? Recommendation was yes.)* eotg-localizer is applying it: the W0d pilot, then the 40 AUTO keys, then the 13 REVIEW items by hand (W0e status line).
- **Q2 (owner, approval of NEW content): RULED 2026-10-09, approved.**
  - W7: the six endgame set pieces (`big_event_window` now, 90–140 words, effect and music; fullscreen later with art).
  - The NEW half of W9: the patron.006 absent-variant letter and the separate unsigned syndicate notes.
- **Q3 (owner, tone): RULED 2026-10-09.** The Seamless fade is staged **once, at the threshold only** (the end.009 Seamless outcome, end.010, optionally fracture.027), framed as a record (the log register), not a speaker. Steady-state Seamless text has no first person (§12.1 rule 7).
- **L-1 (lore-keeper): ANSWERED 2026-10-09.** Folded into §12.1 rule 7 and `cybernetics_v2_procedures_lore.md` §(c); the four shipped-text fixes are batch B7 items (§13.3).
- **L-2 (lore-keeper): ANSWERED 2026-10-09.** Keep fracture.022's "we" lines: they are the ruler's own spoken word, not a second speaker. Folded into §12.1 rules 6 and 7; the B5 text is in §13.3. Nothing in B5 is held.
- **Voice baseline (orchestrator, settled 2026-10-09).** 74% second person from the ported scorecard is the "before" figure; the report's 52% is not reproducible. The classifier in §15 stands.

---

### HANDOFF
- status: done (spec updated with the 2026-10-09 rulings; no open owner questions)
- next: orchestrator → eotg-scripter for **W2** (backgrounds and 2D effects, §11 P1 and §14). W2 needs no owner input: W0b's "before" scorecard exists and §14 fixes the key set and the event mapping.
- ask: Create the `eotg_bg_*` background keys in `common/event_backgrounds/` per §14.1 and set `override_background` on the 230 events in §14.2 (keep list of 19 stays); report any class moves in the batch report. Then eotg-qa takes the scorecard before/after and runs Tiger, PX and lint.
- files: docs/specs/event_quality_v1.md, docs/specs/cybernetics_v2_procedures_lore.md
- needs-loc: W0d/W0e already in flight with eotg-localizer; the four Seamless shipped-text fixes are queued in batch B7 (§13.3)
- needs-lore: W7 addendum review once written (L-1 and L-2 answered 2026-10-09)
- needs-human: CB-44 in-game checks for W0d and W2 (`common/event_backgrounds/` is already in the CLAUDE.md placement list)
