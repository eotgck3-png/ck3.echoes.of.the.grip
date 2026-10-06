# Localization bug hunt: pink "(BUG: …)" text in the UI (2026-10-05)

Static sweep of all eotg_ content (cybernetics, Frontier P1 and P2). **Verdict: FAIL.** Class 1 has 7 keys across
29 sites (1 confirmed in game); Class 2 has 9 visible sites (3 confirmed); Class 3 has 0.

**These failures do reach error.log.** They appear under `Trigger Localization (dynamic|database)`, with file:line.
After a play session, run `grep -A2 "Trigger Localization" error.log` to confirm fixes.

## Class 1: a failing custom_description in failure-style UI with no NOT_ key
Failure-style UI shows a failing `custom_description` by its negative key (`NOT_<key>` or `not_<key>_<persp>`).
There is no NOT anywhere in the script for this to happen. The contexts:
- interaction `is_valid_showing_failures_only`;
- `send_option` is_valid;
- law `can_pass`;
- options with `show_as_unavailable`.

Vanilla supplies a NOT_ form for nearly all of these (for example 595 of 601 custom_description keys in failures-only
blocks). Two contexts are NOT affected: decision `is_valid`, which lists every requirement with its positive key,
and `custom_tooltip`, which is never negated.

**Fix:** add these keys, each written as the failure state:

| Key to add | Sites | Where it shows |
|---|---|---|
| NOT_eotg_aug_clinic_closed_tt (confirmed) | init.txt:2697; procedures.txt:121,234,556,669,940; tamper.txt:338; tier1.txt:191,285,313; tier2.txt:320,372,407; interactions:136,551,1567 | greyed clinic options under a Ban; clinic send options |
| NOT_eotg_aug_send_physician_valid_tt | interactions:151,566,1428 | physician send option (no physician) |
| NOT_eotg_aug_policy_cooldown_tt | laws:41,107,153,224 | law can_pass during the cooldown |
| NOT_eotg_aug_send_one_provider_tt | interactions:78,494 | Offer / Demand Removal |
| NOT_eotg_can_receive_augmented_suppressed_tt | triggers:62,454 | Offer Augmentation, target waiting |
| NOT_eotg_decision_aug_removal_booked_tt | interactions:489 | Demand Removal |
| NOT_eotg_aug_borrow_none_held_tt | interactions:1560 | Borrow Technician |

Optional (they render positively today, so they aren't broken): NOT_ keys for 12 decision is_valid custom_descriptions.

## Class 2: vanilla trigger localization failing in a perspective

| site | UI | failing trigger | fix |
|---|---|---|---|
| triggers:610,616,622,626 (eotg_aug_has_surgeon_for), via decisions:1067-1069 (confirmed) | Self-Repair is_valid | `NOT = { this = $PATIENT$ }` | `this != $PATIENT$` |
| triggers:565 (eotg_aug_borrowed_technician_valid) (confirmed) | Self-Repair is_valid | is_alive (global-only loc) | restructure decisions:1064-1071 as trigger_if (clinic open) / trigger_else; or hidden_trigger |
| decisions:540 (confirmed) | Augment a Retainer is_valid | any_knight has no loc | custom_description with a new key |
| triggers:60 (eotg_can_receive_augmented) | Seek Augmentation is_valid | is_alive, first person | hidden_trigger |
| triggers:221 (eotg_aug_keeper_candidate) | Appoint Warden is_valid | is_alive, third person | hidden_trigger |
| interactions:1564 | Borrow Technician | short_term_gold has no loc (probable) | gold >= minor_gold_value |
| tier2.txt:377 | tier2.003.c greyed | any_prisoner has no loc | custom_description + its NOT_ key |
| procedures.txt:125,238 (low) | proc.001.a/f | has_variable has no NOT_ loc | hidden_trigger |

**Latent (66 lines):** the same patterns sit in option triggers without `show_as_unavailable`, so they never render.
They are listed in the agent report and only matter if `show_as_unavailable` is added later. Examples: has_trait_xp
in eotg_is_aug_tier1/2/3, is_alive and `NOT this` in Frontier triggers.

## Class 3: missing or broken keys
None. All 2,155 explicit references resolve; auto-generated keys exist; BOMs are correct; no `[scope:`.

## Other
- `eotg_aug_act.003.c.hot` (a full paragraph) is used as a toast **title** (effects:3029). Route to localizer/scripter.
- The error.log line "Flag habitat/mission/… set but never used" is benign: the Frontier infrastructure flag is the
  payload for the empty hook eotg_frontier_on_infrastructure_built, so it is unread by design.
- `eotg_flag_aug_trusted_delegate` (tier3.txt:2741,2807) is genuinely dead: nothing reads it. The architect should
  wire up a reader or drop it.
- False positives (not bugs): exists and debug_only; is_available_quick; currently_being_tortured; tamper allow
  lines under is_ai; is_shown/potential blocks; vanilla is_available_adult and can_start_scheme, which fail the same
  way in vanilla.
