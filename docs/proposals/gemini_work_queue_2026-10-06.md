# Gemini work queues (2026-10-06): long-form and unattended

The orchestrator (Claude) may be unavailable for several hours. Each queue below runs **top to bottom without waiting for input**.

**Rules for every task:**
- Write only to the output path named for that task. Never edit `.txt`, `.yml`, `.gui` or `.dds` files, or any file that is not one of your own outputs.
- After saving each output, re-open it and confirm it is not empty. Append its line count to `docs/proposals/gemini_queue_log.md` (writer) or `docs/qa/geminiqa/queue_log.md` (QA): one line per task, giving the task id, the output path, the line count, and the start and finish times.
- If you cannot write files, put the whole output in your reply and continue.
- **Report only checks you actually ran.** If you didn't run a check, write "not checked".
- If a task is blocked (a file it needs is missing), log the reason, skip it, and go on to the next.
- Don't wait for approval between tasks. Don't redo a finished task unless its output file is empty.

---

## Queue W: Gemini (writer)

All writing tasks follow `docs/proposals/gemini_rewrite_feedback_2026-10-06.md` §2–§4. Before W1, read `docs/proposals/kingpin_fragments_r1_apply_instructions.md`: it lists the mistakes from your last draft, and none of them may recur.

The shared rules for W1–W4:
- **Voice:** the implant forecasts and logs its own user only.
- **Speech:** single quotes for speech; never `\"`.
- **No eye implants.**
- **Pronouns:** never "they" for one person; `|U` when a line starts with a pronoun function.
- **Placeholders:** never `[scope:`.
- **Truth:** every line must be true on every path that shows it.
- **Spelling:** Canadian English.

### W1. Fracturing Inheritance: all event text
Follow `docs/proposals/gemini_brief_inherit_text_2026-10-06.md` exactly. Output: `docs/proposals/inherit_text_gemini_r1.md` (about 226 keys).

### W2. Fracturing Inheritance: self-review
Re-read your W1 output against: the brief's §3 rules, spec `docs/specs/cybernetics_v2_fracturing_inheritance.md` §7 and §7.1, and the error classes in `kingpin_fragments_r1_apply_instructions.md`.

Output: `docs/proposals/inherit_text_gemini_r1_selfreview.md`, a table with key | problem | corrected text. **Do not edit the W1 file.** Corrections go in this table only. End the file with a count of the keys you changed and the keys you left alone.

### W3. Neurofractured Kingpin: everything except the fragments
Source: spec `docs/specs/cybernetics_v2_kingpin.md`. Read §5.2 (variation), §5.4.2 (the visible leverage panel), §5.8 (the node and leaf tables), §7 (the loc surface, incl. §7.2 key list), §7.3 (voice and register), §7.4 (binding wording fixes and banned list) and §8.

Write:
- every event's `.t` title;
- every option, including the per-kind variants `.e_crew` and so on;
- the duel `.success` and `.failure` tooltips;
- the leverage tooltips "deepens" and "loosens";
- the story-panel strings, and the three band names: "A favour owed", "Deep in their pocket", "They own the room";
- the descs for events that are **not** in the fragment draft: .004, .007, .008, .009, .011, .013, .014, .015, .030–.039, .040, .050;
- every ending desc .060–.076, with its per-kind aftermath lines where §5.8 asks for them;
- the 15 modifiers, plus each one's `_desc`;
- the opinion keys and the debug decision keys.

Fixed titles and fixed lines from §7.4 must be used verbatim. Read each option's effects in §5.8 before writing it.

Output: `docs/proposals/kingpin_text_gemini_r1.md`. Split it into sections by event. Under each event, add a short truth note covering the entry paths and why the text holds on each. You may write it in several saves; append to the same file.

### W4. Neurofractured Kingpin: self-review
As W2, for W3. Also check that no line duplicates a fragment from `kingpin_fragments_gemini_r1.md` or its apply instructions. Output: `docs/proposals/kingpin_text_gemini_r1_selfreview.md`.

### W5. Shipped cybernetics: a sweep for time-of-day and stock phrases (proposals only)
Read `localization/english/eotg_augmentation_l_english.yml` and look for:
- time-of-day words: dawn, morning, today, tonight, night, overnight, sunrise, evening;
- "half a second" beyond the four kept on purpose (see `docs/qa/variety_pass_2026-10-07.md`);
- any remaining medieval or clockwork words from feedback §3.

For each hit, give the key, the current text and a proposed replacement, written to be true for the event (read the event in `events/eotg_augmentation_*.txt`).

Output: `docs/proposals/cyber_loc_sweep_gemini_r1.md`.

### W6. Done
Append "QUEUE W COMPLETE" to the log, with a one-paragraph summary.

---

## Queue Q: GeminiQA (independent, read-only reviewer)

Every QA task follows the reporting format in `docs/qa/geminiqa_brief_2026-10-06.md` §3: IDs, severity, path:line, evidence, rule, fix, confidence, and `NEEDS-VANILLA-CHECK` where it applies. Use a fresh ID prefix for each task, so IDs never collide.

### Q1. Shipped cybernetics audit
Follow `docs/qa/geminiqa_brief_2026-10-06.md` exactly. Output: `docs/qa/geminiqa/cybernetics_audit_r1.md`. ID prefix: `GQA-`.

### Q2. Frontier and Unclaimed Regions audit
Scope:
- files matching `eotg_frontier*` and `eotg_unclaimed*` under `events/`, `common/` and `localization/english/`;
- the specs: `docs/specs/frontier_*.md`, including `frontier_unclaimed_regions.md` (its §D holds the owner decisions);
- the override `common/scripted_triggers/eotg_vanilla_overrides_triggers.txt`. Its diff from vanilla must be exactly two lines; see `docs/pitfalls.md` §16.

Use the same categories as the cybernetics audit. Output: `docs/qa/geminiqa/frontier_audit_r1.md`. ID prefix: `GQF-`.

### Q3. Spec-to-build conformance
For every spec in `docs/specs/` whose system is built (cybernetics_v2*.md and frontier*.md, **not** the kingpin or fracturing_inheritance specs):
- list each identifier, event, option, modifier and effect the spec promises;
- say whether the build has it and whether it behaves as specified;
- report the divergences: missing, extra, or different behaviour.

Output: `docs/qa/geminiqa/spec_conformance_r1.md`. ID prefix: `GQS-`.

### Q4. Cross-check of the writer's drafts
When the writer's outputs exist (W1–W4: `docs/proposals/inherit_text_gemini_r1*.md`, `kingpin_text_gemini_r1*.md`), review them against their specs. If an output is not there yet, do Q5 first and come back.

Check:
- truth against the option effects in §5.3 and §5.8;
- the binding wording in §7.1 and §7.4;
- placeholders and scope names that exist in the spec;
- banned words, voice and pronouns.

**Verify the writer's claimed checks.**

Output: `docs/qa/geminiqa/draft_review_r1.md`. ID prefix: `GQD-`.

### Q5. Pitfalls regression scan
Read `docs/pitfalls.md` and the CLAUDE.md invariants. For each entry, search the repo, excluding `OLD PROJECT VERSION/`, for new instances of that mistake. Some patterns to start with:
- `eotg_[ekdcb]_` title keys;
- `[scope:` in localization;
- top-level `effect =` or `trigger =` blocks on vanilla on_actions;
- events that nothing fires;
- `GetHeir` on a character;
- `hidden_trigger`;
- skill effects without `_skill`;
- a `replace_path` for a folder the mod doesn't ship;
- loc files without a BOM. You can't see bytes: report this one as "not checked" unless your tools can read them.

Output: `docs/qa/geminiqa/pitfalls_scan_r1.md`. ID prefix: `GQP-`.

### Q6. Done
Append "QUEUE Q COMPLETE" to the log, with the total findings by severity across Q1–Q5.
