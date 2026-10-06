# Cybernetics fix batch (orchestrator, 2026-10-05)

Source: the owner's first in-game playtest, docs/qa/loc_bug_hunt_2026-10-05.md, and two owner rulings.

## A. Localization bugs (pink "(BUG: …)" text): see docs/qa/loc_bug_hunt_2026-10-05.md
1. **Class 1: add 7 NOT_ keys, written as the failure state.**
   - NOT_eotg_aug_clinic_closed_tt (confirmed in game; 16 sites)
   - NOT_eotg_aug_send_physician_valid_tt
   - NOT_eotg_aug_policy_cooldown_tt
   - NOT_eotg_aug_send_one_provider_tt
   - NOT_eotg_can_receive_augmented_suppressed_tt
   - NOT_eotg_decision_aug_removal_booked_tt
   - NOT_eotg_aug_borrow_none_held_tt
2. **Class 2: fix the 8 visible sites.**
   - Self-Repair: `NOT = { this = $PATIENT$ }` becomes `this != $PATIENT$` (triggers:610,616,622,626).
   - Self-Repair: is_alive (triggers:565). Restructure decisions:1064-1071 as trigger_if (clinic open) /
     trigger_else, or use hidden_trigger.
   - Augment a Retainer: any_knight (decisions:540) becomes custom_description with a new key.
   - is_alive at triggers:60 and 221 goes inside hidden_trigger.
   - interactions:1564: short_term_gold becomes gold >= minor_gold_value.
   - tier2:377: any_prisoner becomes custom_description + its NOT_ key.
   - procedures:125,238: has_variable goes inside hidden_trigger.
3. **Others.**
   - effects:3029: the toast title uses a paragraph key (eotg_aug_act.003.c.hot); give it a short title key.
   - eotg_flag_aug_trusted_delegate (set at tier3:2741,2807) is read nowhere. Wire up a reader or drop it;
     the architect decides.
   - Leave the latent sites (no show_as_unavailable) and vanilla's own failures alone.

## B. Owner ruling: removal decisions, one step per stage
- **Augmented:** Remove the Implants (safe full removal), unchanged.
- **Enhanced:** Partial Implant Removal ONLY. Remove tier 2 from eotg_decision_aug_excision's is_shown.
- **Overclocked:** Initiate Downgrade Protocol, plus Cut It Out as the last resort.
- **Neurofractured:** Cut It Out.

Reword Cut It Out's desc and tooltip so its danger and finality are unmistakable (it can kill; everything
comes out; major gold), and so it clearly differs from Remove the Implants, whose desc currently reads almost
the same. Update the specs (phase3 decision table, balance §5.2) and anything that points Enhanced characters
to Excision.

## C. Owner request: "Pursue the Next Stage" wording
"The last work has settled" (eotg_decision_aug_pursue_next_stage_settling_tt) is really the 5-year
eotg_flag_aug_settling timer. Make it explicit, keeping the theme:
- the requirement reads "Your last procedure was at least 5 years ago";
- the decision desc gains one sentence: "Each procedure needs five years to settle before the body will take
  another."
- Apply the same to any other tooltip that names the settling gate.

## Not in this batch
The event-writing rewrite (docs/qa/event_writing_review_2026-10-05.md) waits on the owner's go-ahead.
