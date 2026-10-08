# GeminiQA r1 verification (eotg-qa, 2026-10-08)

**Scope:** `docs/qa/geminiqa/` cybernetics_audit_r1, frontier_audit_r1, spec_conformance_r1 and pitfalls_scan_r1, 32 findings. Findings were located by key or by the quoted text, because GeminiQA's line numbers are unreliable. `draft_review_r1` (it reviewed a stale draft) and `build_qa_inherit_kingpinA_r1` (covered by eotg-qa's own build QA) are out of scope.

**Totals:**
- CONFIRMED: 19 (10 actionable, 9 PASS or no-action notes).
- CONFIRMED-ALT: 4.
- REJECTED: 9.
- NEEDS-INGAME: 0.

**False positives:** 9 of the 23 defect claims (39%). Four of the real findings misquoted the text.

**Recurring GeminiQA errors:**
- quoting text that isn't in the file;
- applying the Gemini writing-brief bans to the whole project, and stretching them ("throne", "clocks", "scroll" used as a verb, "tomorrow");
- citing pitfalls sections that don't say what it claims;
- reporting spec gaps the specs already document.

| id | verdict | evidence | fix | owner |
|---|---|---|---|---|
| GQA-001 | REJECTED | `docs/qa/loc_bug_hunt_2026-10-05.md:17-19` (confirmed in game): a decision's `is_valid` shows the positive key. `NOT_` is shown only in failures-only UI (Demand Removal, `interactions.txt:488-491`, where `recipient` exists). Vanilla uses `[recipient.…]` in `NOT_` keys too. | none | – |
| GQA-002 | CONFIRMED | `tamper.txt:155-158`: only `.002.b` saves `eotg_tamper_signed`. `scheme_discovered` comes from a random roll in `.001` (`:57`). Both show `desc_known` (`:282-292`), so "made sure you would know it" is false on the `.002.a` + discovered path. | Split the `first_valid`: signed → `desc_known`; discovered only → a new `desc_known_discovered`. | scripter + localizer |
| GQA-003 | CONFIRMED (the option is **.017.b**, not .d) | `tier3.txt:2324-2356` `.017.b` kills the conspirator. False + executed falls through to `desc_false` (loc:1350), which never mentions the death. The silent opinion and tyranny effects are at `tier3.txt:2603-2628`. Precedent: `eotg_fracture.020.desc_false_executed`. | Add a `triggered_desc` before true/false: `eotg_plot_truth = flag:false` + `eotg_plot_action = flag:executed` → `eotg_aug_tier3.018.desc_false_executed`. Optionally add a tooltip on `.018.c`. | scripter + localizer |
| GQA-004 | CONFIRMED (already CB-15) | `effects.txt:1006` sets `eotg_flag_aug_containment_regency`; it is cleared at :466 and :1120 and never read. It is specced (`phase3.md:137`). | Leave it parked under CB-15. | architect to rule |
| GQA-005 | CONFIRMED | loc:62 "Processing is flawless" ("flawless" is banned, feedback:63) | "Processing runs without pause." | localizer |
| GQA-006 | REJECTED | loc:1814 "the readings scroll past" uses "scroll" as a verb. The text GeminiQA quoted doesn't exist. | none | – |
| GQA-007 | CONFIRMED | loc:537 "This morning" | "This watch" | localizer |
| GQA-008 | CONFIRMED-ALT | loc:714 reads "since morning" | "…since the shift began" | localizer |
| GQA-009 | CONFIRMED | loc:1281 "before dawn" | "before the shift change" | localizer |
| GQA-010 | CONFIRMED | loc:756 "wants the throne" (architect flag, `new_beats.md:409`) | "[eotg_heir.GetSheHe\|U] wants your seat." | localizer |
| GQA-011 | CONFIRMED | loc:1437 "last night's dinner" | "the last shared meal" | localizer |
| GQA-012 | CONFIRMED-ALT | loc:433 reads "And at night, when the house is still" | "And between watches, when the house is still, …" | localizer |
| GQA-013 | CONFIRMED | loc:973 "the evening's entertainment" | "Make it the court's entertainment." | localizer |
| GQA-014 | CONFIRMED-ALT | loc:1701 ends "…and for tonight [x] does." | "…and for now [eotg_aug_spouse.GetSheHe] does." | localizer |
| GQA-015 | CONFIRMED (low) | loc:807 "Not today." | "Not yet." | localizer |
| GQA-016 | CONFIRMED-ALT | loc:1418: keep "Clocks run wrong" (a clock isn't clockwork); the problem is "three times today" | "three times this shift" | localizer |
| GQA-017 | CONFIRMED (no action) | proc.004 reads `eotg_aug_residue`; fired at `on_actions.txt:1840` | none | – |
| GQA-018 | CONFIRMED (no action) | proc.020 reads `var:eotg_aug_former`; fired at `on_actions.txt:1867` | none | – |
| GQF-001 | REJECTED | The rule (`frontier_unclaimed_regions.md:43`) is "Region, not system, **for the claimed unit**". "Its Systems" are the baronies (glossary: Barony = System, County = Region). | none | – |
| GQF-002 | REJECTED (owner call) | `frontier_l_english.yml:106` "day and night". No time-word rule covers Frontier text. | Optional, only if the owner extends the rule project-wide. | owner |
| GQF-003 | REJECTED | `frontier_l_english.yml:304` "tomorrow" is on no banned list. | none | – |
| GQF-004 | CONFIRMED (PASS) | The override's diff from vanilla is exactly two `# EOTG` lines. | none | – |
| GQF-005 | CONFIRMED (PASS) | No title/province/culture/faith/character keys in the 19 frontier and unclaimed files. | none | – |
| GQS-001 | REJECTED | Already recorded as dropped (`cybernetics_v2_phase5.md:303`). | none | – |
| GQS-002 | REJECTED | Already documented (`cybernetics_v2_realm.md:117`). | none | – |
| GQS-003 | REJECTED | Already struck through (`cybernetics_v2_phase4.md:429`, :437). | none | – |
| GQS-004 | CONFIRMED (no action) | CLI and wildcard prose (`tier_options.md:24-25`). | Optional: make `spec_conformance.py` skip them. | – |
| GQS-005 | CONFIRMED (no action) | Build note documented (`frontier_unclaimed_regions.md:577`). | none | – |
| GQP-001 | REJECTED | The cited pitfalls section doesn't cover GetHeir. `GetPrimaryTitle.GetHeir` is a vanilla chain (`laws_l_english.yml:56`). | Optional hardening: save `primary_heir` as a scope in end.030. | – |
| GQP-002 | CONFIRMED (PASS) | Exactly one BOM in each of the five yml files. | none | – |
| GQP-003 | CONFIRMED (PASS) | No top-level effect or trigger on vanilla on_actions. | none | – |
| GQP-004 | CONFIRMED (PASS) | All 197 non-new event ids are referenced. | none | – |

**Routing:**
- **Scripter, then localizer:** GQA-002 and GQA-003.
- **Localizer:** GQA-005, 007–016. Batch them with the W5 sweep (`docs/proposals/cyber_loc_sweep_gemini_r1.md`), which overlaps.
- **Owner:** GQF-002, whether the time-word rule should apply project-wide.
