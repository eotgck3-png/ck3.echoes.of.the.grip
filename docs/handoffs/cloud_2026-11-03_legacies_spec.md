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
  - **§8 canon:** under the ERAS rule the "Second Era" *is* pre-Grip, so it stays. "Eight centuries" becomes "nearly nine centuries". "The Confluence" becomes "the Grip". "Hell" becomes "another plane" ("Planar Pocket"). Every flagged line is listed with its file:line. The register is physical and archaeological; the voice mix follows R1.
  - **§9** has tests V-L1 to V-L18. **§10** has owner questions Q2, Q3, Q4, Q7, Q8, Q9 and Q10, each with a default. **§11** lists the pitch's unbuilt beats, which need owner approval.
- files: `docs/specs/legacies_v2.md`, this handoff.
- unverified-vanilla:
  - `every_county` in a game-start on_action (§4.1);
  - `random_pool_character` with `province =` (§5.2, LOW-2);
  - `increase_wounds_effect` REASON keys other than `attacked` (LOW-1);
  - the event themes `martial`, `stewardship`, `diplomacy`, `intrigue`, `learning`, `faith` and `realm` (lifted from v1).
- needs-local-validation: none yet (no script). After the build: Tiger and PX, then V-L1 to V-L18.
- needs-loc: the full conversion of 127 keys (second person to first, dashes, Canadian spelling); the flagged lines are drafted in Appendix A.
- needs-lore: §8.1. Confirm with the vault that the Second Era is pre-Grip, and send "Confluence" and the Hell/plane wording there.
- needs-human: Q7 (mod-exclusive), Q2 (names), Q3 (dating), Q4 (Exodus), Q9 (density), Q8 (passive drain), Q10 (weighting).
- taskboard (for the orchestrator to add; I didn't edit it):
  - "Legacies: re-add bookmark seeding of named sites (v1 had 7 history characters) after Gate 1".
  - "Legacies: re-add the Exodus-haven discovery path when Titan Exodus is lifted".
