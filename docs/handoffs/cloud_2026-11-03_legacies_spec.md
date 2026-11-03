# Handoff: Confluence Legacies v2, the lift spec (cloud, 2026-11-03, H3)

Spec: `docs/specs/legacies_v2.md`. This is a spec and audit only: no game script, events or loc were written. The owner hasn't ruled Legacies mod-exclusive (Q7).

### HANDOFF (cloud session, unvalidated)
- branch: `claude/legacies-spec-cloud` (cut from origin/v2-space-map at 295ea5a)
- status: done (base spec). The deepening (Appendix A loc drafts, Appendix B sim) follows in the sections below.
- summary: The spec has the same shape as the Void spec.
  - **§2 state machine.** Six county variables. Family is written once by seeding. Condition, integrity and attention each get one clamped writer; v1 had a second condition writer inside make-known. The site cooldown is renamed `eotg_legacy_site_cd`. The section also gives the bands and the condition-to-modifier table.
  - **§3 hooks.** `yearly_playable_pulse`, `on_title_gain` and `on_game_start_after_lobby`, each confirmed by existing v2 on_actions. Cooldowns are set only at firing points; v1 set them in about 30 event options.
  - **§4 map-agnostic.** Seeding is per county (`eotg_legacy_seed_chance_value` = 3) instead of 7 history characters plus 30% of rulers. The Titan Exodus path is dropped. Both have taskboard notes for the human.
  - **§5.1 performance.** `every_held_title` with `tier = tier_county` replaces `every_sub_realm_county`, as the Frontier tick does (`eotg_frontier_on_actions.txt:35`).
  - **§5.2 every MED and LOW audit row** has a concrete design, plus three new findings: 0102.b is empty; the loc keys move to the Void form; the survey picks through `random_held_title`.
  - **§6 identifier table**, v1 → v2.
  - **§7 fate table:** 16 events, 62 options (32 fixed, 30 lifted, none dropped).
  - **§8 canon:** under the ERAS rule the "Second Era" *is* pre-Grip, so it stays. "Eight centuries" is dropped with no replacement figure: the text says "since the Grip" (local review, 2026-11-03). "The Confluence" becomes "the Grip". "Hell" becomes "a shard of one of the hells", and the family is "Hellshard", pending the vault (local review; this replaces the cloud draft's "another plane" / "Planar Pocket"). Every flagged line is listed with its file:line. The register is physical and archaeological; the voice mix follows R1.
  - **§9** has tests V-L1 to V-L23 (the local review added V-L22 and V-L23). **§10** has owner questions Q2, Q3, Q4, Q7, Q8, Q9 and Q10, each with a default. **§11** lists the pitch's unbuilt beats, which need owner approval.
- files: `docs/specs/legacies_v2.md`, this handoff.
- unverified-vanilla: none since the local review (2026-11-03). All of these were verified against vanilla; the citations are in the spec's amendment block and §4.1, §5.2 and §7:
  - `every_county`;
  - `random_pool_character` with `province =`;
  - the wound effect, now `increase_wounds_no_death_effect`;
  - the event themes.
- needs-local-validation: none yet (no script). After the build: Tiger and PX, then V-L1 to V-L23.
- needs-loc: the full conversion of 127 keys (second person to first, dashes, Canadian spelling); the flagged lines are drafted in Appendix A.
- needs-lore: §8.1. Confirm with the vault that the Second Era is pre-Grip, and send "Confluence" and the Hell/plane wording there.
- needs-human: Q7 (mod-exclusive), Q2 (names), Q3 (dating), Q4 (Exodus), Q9 (density), Q8 (passive drain), Q10 (weighting).
- taskboard (for the orchestrator to add; I didn't edit it):
  - "Legacies: re-add bookmark seeding of named sites (v1 had 7 history characters) after Gate 1".
  - "Legacies: re-add the Exodus-haven discovery path when Titan Exodus is lifted".

## Deepening (a): Appendix A, replacement loc

### HANDOFF (cloud session, unvalidated)
- branch: `claude/legacies-spec-cloud`
- status: done
- summary: The spec's Appendix A gives exact replacement strings, under the v2 keys, for every flagged line:
  - the decision name, desc and tooltip;
  - the descs of 0002, 0010, 0020, 0021 (with one heir speech line), 0030 and 0040, plus 0040's title, and option 0021.b;
  - the modifier names and descs.

  The rules applied: first person in the main descs, no dashes, Canadian spelling, "the Grip", bare `[x.GetName]`. The local review (2026-11-03) replaced "nearly nine centuries" with "since the Grip", "another plane" with "a shard of one of the hells", and "county" with "Shoal". The block is BOM-free markdown; the BOM goes on at build time. The other 100-odd keys are left for the voice, dash and spelling conversion at build time.
- files: `docs/specs/legacies_v2.md` (Appendix A).
- needs-lore: the four checks listed under Appendix A.
- needs-loc: the full 127-key conversion at build time.

## Deepening (b): the Legacies sim, Appendix B

### HANDOFF (cloud session, unvalidated)
- branch: `claude/legacies-spec-cloud`
- status: done
- summary: `docs/tools/sim/models/legacies.py` reads the **v1** files through `pdx_read.py` (`Script(repo='OLD PROJECT VERSION')`): option weights, gates and amounts, condition and direct integrity writes, `random_list` branches, follow-ups, the survey's AI weight and fallback, the pulse's decay, chances and cooldowns, and the seed weights. It models the v2 design. I copied `pdx_read.py`, `common.py` and `models/__init__.py` unchanged from `claude/final-h-cloud`, so the branches merge clean. Output: `docs/qa/mechanics_sim_2026-11-03/legacies_v2_sim.md`. The findings revise the spec:
  - **B2 / NEW-5:** 0105 fires at every succession and ratchets 63% of sites into Sealed. Gate it on a dynasty change: Sealed falls to 26%.
  - **B3 / Q8:** integrity never reaches 0 from play. Default: −1 a year on Extracted.
  - **B4 / Q10:** the rival claim (0101) never fires. Default: gate 25 plus an attention floor at 25.
  - **B5 / Q9:** survey seeding gives a player about 4 new sites a century.
  - **NEW-4:** 0104 writes integrity directly; route it through the writer.
- files: `docs/tools/sim/models/legacies.py` (new); `docs/tools/sim/{pdx_read.py,common.py,models/__init__.py}` (copied, identical to `claude/final-h-cloud`); `docs/qa/mechanics_sim_2026-11-03/legacies_v2_sim.md`; the spec (§5.2 NEW-4 and NEW-5, §7, §10, §12, Appendix B).
- unverified-vanilla: none. The local review (2026-11-03) replaced NEW-5's compare with vanilla's form, `title_on_actions.txt:474-475`.
- needs-local-validation: rerun `python docs/tools/sim/models/legacies.py` and compare with the md file.
- needs-human: the revised Q8, Q9 and Q10 defaults, and NEW-5.
