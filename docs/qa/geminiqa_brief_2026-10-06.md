# GeminiQA brief: in-depth audit of the shipped cybernetics system (round 1)

**For:** GeminiQA, an external Gemini agent working as an independent QA reviewer. **Date:** 2026-10-06.
**Deliver to:** `docs/qa/geminiqa/cybernetics_audit_r1.md`, and nowhere else.
**READ-ONLY.** Do not edit, create or delete any other file. In particular, never touch `.txt`, `.yml`, `.gui` or `.dds` files: a past outside edit broke the file encoding. You report problems; the project's own agents fix them.

## 0. The project
Echoes of the Grip is a total-conversion mod for Crusader Kings III 1.20, set in an original space-faring galaxy at 866 AG. Read these first:
1. `CLAUDE.md`: the invariants, file placement, and known-benign tool output. Don't report anything on the known-benign list.
2. `docs/specs/cybernetics_v2.md`: the cybernetics system's index spec. Its §5 holds the lore rules.
3. `docs/proposals/gemini_rewrite_feedback_2026-10-06.md` §2–§4: the setting, the banned words and the rules for text.
4. `OLD PROJECT VERSION/docs/SETTING LORE`: read only the ERRATA block at the top (CYBERNETIC VOICE, LAW AT 866, CYBERNETICS AT 866).
5. `docs/pitfalls.md`: mistakes this project has already made.

**Vanilla game files are not in the repo.** Where a finding depends on how vanilla CK3 behaves, mark it `NEEDS-VANILLA-CHECK` and say what to look up. Don't assert engine behaviour as fact.

## 1. Scope
The shipped cybernetics (augmentation) system:
- `events/eotg_augmentation_*.txt`, **except** `eotg_augmentation_kingpin.txt` and any `eotg_augmentation_inherit.txt`, which are being built right now;
- the `common/` files they use: scripted effects and triggers, on_actions, story cycles, modifiers, opinion modifiers, traits, script values, character interactions, decisions, laws, court positions, character templates and customizable localization (grep for `eotg_aug` and `eotg_fracture`);
- `localization/english/eotg_augmentation_l_english.yml` and the other `eotg_aug*` loc files.

## 2. What to look for
Our own tools already catch syntax, unknown effects, missing loc keys, BOM and encoding problems, and scope type errors. **Don't spend effort there.** Look for what tools miss:

1. **Text that lies.**
   - An option's text promises something its effects don't do, or hides a major effect.
   - A desc is false on one of the paths that shows it. Check `first_valid` and `triggered_desc` ordering, fallbacks, and which events fire the event.
   - A desc names someone who may not exist on that path.
2. **Logic and state.**
   - Flags or variables that are set but never read, or read but never set.
   - Variables never cleared, so they leak into a later run or a later ruler.
   - `random_list` branches whose weights can all be zero.
   - Triggers that make an event or option impossible.
   - Effects that run on the wrong character: root versus scope, liege versus heir.
   - Chains that can stall with no follow-up event.
   - Double-firing: two on_actions or events that can both start the same chain.
3. **Reachability and pacing.**
   - Events nothing fires.
   - Options that are never available.
   - Cooldowns that conflict.
   - Chains a player could hit far too often, or never.
   - The signature resource: every flavour event must read or move `eotg_fracture_risk` or the system's stated resource (invariant 5). List any that don't.
4. **Balance and player experience.**
   - Options with an obvious best choice.
   - Costs out of proportion to rewards.
   - Death or ruin with no warning.
   - Places where the player can't tell what a choice will do.
5. **Lore and voice**, with exact line references:
   - the implant doing more than forecast and log its user;
   - medieval or clockwork vocabulary; banned words;
   - singular "they" for one person; an assumed gender for an unscoped person;
   - "human" as the default people;
   - institutions above the realm.
6. **Inconsistency across events:**
   - the same thing named differently;
   - numbers that disagree between a tooltip and the effect;
   - modifiers whose desc doesn't match their values.

## 3. How to report
For each finding:
- **ID:** GQA-001, GQA-002, and so on.
- **Severity:**
  - **BLOCKER:** crash, broken chain, or text that lies about a death or a major cost.
  - **MAJOR:** wrong behaviour or false text.
  - **MINOR:** polish.
  - **NOTE:** a question, not a defect.
- **Location:** `path:line`. Name the event id and the loc key.
- **Evidence:** a short verbatim quote of the relevant lines.
- **Why it's wrong:** cite the rule, spec section or the contradicting line.
- **Suggested fix:** one or two sentences. For text, give the exact replacement.
- **Confidence:** high / medium / low. Add `NEEDS-VANILLA-CHECK` where it applies.

Order: BLOCKER first, then by file. End with:
- a summary table (counts by severity and by category 1–6);
- a list of the files you read in full and the files you only skimmed;
- **the checks you actually performed.** Don't claim any check you didn't run. An earlier Gemini report claimed an "automated script" test that never happened, and that cost trust. Saying "not checked" is fine.

Quality over quantity: 30 solid findings beat 150 guesses. If you're unsure, say so and mark the finding NOTE.

After saving, re-open `docs/qa/geminiqa/cybernetics_audit_r1.md` and confirm it isn't empty. Report its line count and the number of findings. If you cannot write files, paste the whole report into your reply.
