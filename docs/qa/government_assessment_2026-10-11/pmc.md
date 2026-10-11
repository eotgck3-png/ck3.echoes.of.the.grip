## QA assessment: PMC government (eotg_pmc_government), 2026-10-11
Static tools (no Tiger, per brief): PX LSP `common localization` = 6 warnings, all known-benign `building_walls_*` missing-loc; `px_vocab_check common` = 0; `eotg_lint --baseline` = 0 new. Logs are in `scratchpad/govassess/pmc_{px_lsp,vocab,lint}.txt`.
`G/` = vanilla game root. GT = `G/common/governments/00_government_types.txt`.

### Scorecard
| Area | Verdict | Evidence | Std |
|---|---|---|---|
| P0 blacklist | MEETS | Only vanilla flags are settled/domain_limit/crown_authority (`eotg_pmc_government.txt:56-61`). The blacklist rejects republic/mercenary/holy_order plus DLC-gated admin/theocracy/adventurer (`G/common/scripted_rules/00_rules.txt:157-217`). The mod ships no `scripted_rules/`. | §1 P0, P9 |
| P1 dynastic | MEETS | `pmc:24-25` (feudal GT:7-8) | P1 |
| P2 inherit default | MEETS | unset | P2 |
| P3 succession law | MEETS (static) | `eotg_government_succession_laws.txt:25-55` has potential/can_have/can_keep/should_start_with on the identity flag. Safety net: `eotg_government_effects.txt:14-23`, hooked additively at `eotg_government_on_actions.txt:10-22`. Vanilla single heir is blocked for this government (`00_law_triggers.txt:371-397`). Gender laws carry no government gate (`00_succession_laws.txt:2024+`). | P3, §3.5 |
| P4 playable character | MEETS | The test ruler is a duke (`k_france.txt:200-203`), which passes `is_playable_character` (`00_available_for_events_triggers.txt:964-980`). | P4 |
| P5 heir keeps it | MEETS (static) | `pmc:29-30` (admin GT:458/462) | P5 |
| P6 GOVERNMENT_TYPES | MEETS | The vanilla 20 are byte-identical after whitespace strip (diff vs `00_defines.txt:552-571`). The key is at `eotg_government_defines.txt:42` and in the sub-mod copy at `:35`. | P6, §3.20 |
| P7 can_get_government / leakage | PARTIAL | Deliberately unset (`pmc:13`). No `fallback` (correct). No grant fields (below). Leakage is untested (V-G11). | P7 |
| P8 reachability | PARTIAL | Map pick only, through sub-mod history. The sub-mod bookmark lists 5 vanilla-government characters (`00_bookmarks.txt:22-90`). The ruler designer can't reach it, and there is no adoption decision. | P8 |
| P10 DLC | MEETS | No DLC-gated rule or mechanic | P10 |
| Q1 core verb | FAILS | Nothing sells force. The government is modifiers only (`pmc:45-50`). | §2 Q1 |
| Q2 signature resource | FAILS | `eotg_pmc_standing` is reserved (`governments_v2.md:31,71`). Zero hits in `common/`, `events/` and `localization/`. | Q2, §3.11, inv. 5 |
| Q3 vassal model | PARTIAL | Own group (`groups/...:17-25`), but feudal-shaped trees with different numbers | Q3, §3.3 |
| Q4 succession fit | PARTIAL | Oldest-child single heir, labelled "Command Succession" (loc `:62-64`). The desc says "rank is earned by results in the field" (`:5`). | Q4 |
| Q5 entry/exit | FAILS | Debug only (`eotg_government_debug_decisions.txt:10-38`) | Q5 |
| Q6 AI | PARTIAL | `use_legends` only (`pmc:52-54`). Laws and contract levels do have AI weights. | Q6, §3.14 |
| Q7 UI | PARTIAL | Free surfaces only. Placeholder icon and borrowed text icon. | Q7 |
| §3.1 block fields | MEETS | Every field has a vanilla `.txt` call site: cadet/dynasty/legitimacy/accolades GT:7-11; dynasty_named_realms GT:454; base_on_landed GT:458; sticky GT:462; regnal GT:816; royal_court GT:14; holdings GT:18-20; contract_group GT:22; court_generate_commanders GT:335/373/416; use_legends GT:25; realm_mask GT:60-61. No field is `.info`-only. All four modifiers exist in vanilla blocks (GT:509-514, 594; `01_japan_government_types.txt:122`). | §3.1, §4.6 |
| §3.2 flags | MEETS | Identity flag read by the law, the effect, the knight trigger and the decision. No `government_is_feudal`. | §3.2 |
| §3.3 contracts | MEETS (min) | `eotg_government_obligations.txt:19-145` has 5 chained levels, levy-tree values copied by position, and the flags `obligation_high_taxes/levies` | §3.3 |
| §3.4 law groups | MEETS (min) | crown_authority requires the flag (`00_realm_law_groups.txt:2`), which the PMC carries | §3.4 |
| §3.6 holdings | MEETS | Castle shape, verbatim from GT:18-20 | §3.6 |
| §3.7 MAA/knights | PARTIAL | Modifiers only. No gated MAA. | §3.7 |
| §3.8 decisions/interactions/CBs | FAILS (full) / MEETS (min) | Debug decisions only | §3.8 |
| §3.13 character_modifier | MEETS | `pmc:45-50`. No `top_liege_character_modifier`. | §3.13 |
| §3.14 AI/grants | PARTIAL | No `possible_grant_vassal_governments` (feudal grants theocracy/ecclesiastical, GT:40) and no `grant_vassal_ai_will_do` | §3.14 |
| §3.15 resource GUI | N-A | There is no resource to show | §3.15 |
| §3.16 loc | MEETS | 1 BOM, no `[scope:`. Name/adj/realm/desc/with_icon/filter/obligations/vassals_label/6 engine modifiers at `:2-16`; law `:62-64`; contracts `:74-95`; group `:306-307`; flavour `:162-184`; knight `:254-261`; debug `:286-289`. GAME_OVER keys are N-A because the government is playable. | §3.16 |
| Icon | PARTIAL | Placeholder copy of mercenary (`government_types/README.txt`) | §3.16 |
| Text icon | PARTIAL | Borrowed `@government_type_mercenary!`, which exists (`G/gui/texticons.gui:4756`) | §3.17 |
| Flavourization | MEETS | 23 entries (`eotg_government_flavorization.txt:23+`). Rules placement matches vanilla (`00_title_holders.txt:3415-3426`, `_flavourization.info:165-209`). | §3.18 |
| on_actions | PARTIAL | Succession net only. No resource init or teardown (none exists). | §3.19 |
| Knight term | MEETS | `eotg_knight_culture.txt:29-34` plus the trigger at `eotg_government_triggers.txt:10-18` | §3.21 |
| Map-agnostic | MEETS | No title, culture or faith key in G1 files. Title-key audit is empty. | §4.2 |

### BLOCKERS
None found by static review. Nothing visible statically stops a PMC ruler being picked or the dynasty continuing. Every playability "MEETS" above is unproven in game, because CB-49 is still `waiting-human`.

### GAPS
1. **[S2] No core verb, no resource (Q1/Q2/§3.11).** By the template's own §2 rule this is a feudal reskin. Mechanically it differs from feudal only in these ways:
   - it lacks `government_is_feudal`, so there are no partition laws, feudal special/coinage/fortification contracts or feudal-gated events;
   - tax is 0.05 vs 0.10 at standard and levies 0.35 vs 0.25 (`obligations.txt:31,95` vs `G/.../feudal.txt:158`, `00_goverment_values.txt:75-79`);
   - +2 knights, +15% knight effectiveness, -10% MAA maintenance and -20% mercenary cost;
   - commanders x2, no regnal numbers, title-named realms.
   This matches the G1 scope (`governments_v2.md` §1), but it fails §6.1 PMC items 1-2. Owner: eotg-architect, then eotg-scripter.
2. **[S2] No entry or exit path (Q5/P8).** Without the sub-mod history, a player cannot reach the PMC. Owner: architect.
3. **[S3] Grants (§3.14).** Feudal's `possible_grant_vassal_governments = { theocracy_government ecclesiastical_government }` (GT:40) was not carried over, so a PMC liege has no clergy-government option in the county-or-higher grant picker (`_governments.info:674-681`). Owner: scripter.
4. **[S3] Succession safety net covers game start and government change only.** A courtier newly landed by a PMC liege (V-G10) relies on the engine firing `on_government_change`, or on the default-law pick skipping partition (`laws.txt:21-22` UNVERIFIED). Check this in T5. If it fails, add a net on `on_title_gain`.
5. **[S3] `opinion_of_liege`, `top_liege_character_modifier`, own MAA: missing.** These are deferred (`governments_v2.md` §15).
6. **Spec divergence.**
   - `KnightCulture` children are redefined (`eotg_knight_culture.txt:60+`), while spec §10 says "not redefined". The change is harmless, but the spec should be amended.
   - The flags omit feudal's `may_elevate_co_monarch` (GT:31; read by `00_diarchy_scripted_triggers.txt`), with no recorded reason. Owner: architect to rule.

### POLISH
- The owner rule (2026-10-11) says other mods are never cited, but two files cite one: `eotg_government_defines.txt:11` (After the End) and `eotg_knight_culture.txt:8-9` (TFE). Owner: scripter.
- `eotg_knight_culture.txt:18` says "PENDING OWNER", but OQ1 is RULED (`governments_v2.md:681`).
- `has_government = feudal_government` appears at `eotg_government_debug_decisions.txt:155` (§5.1.5). It is debug-only, so this is a note.
- Fiction mismatch: "Command Succession / Oldest Child Inherits", while the desc says rank is earned by results. Loc owner: eotg-localizer, or keep it and log the debt (Q4).

### Fiction fit
The spec defines the PMC as "a command hierarchy that sells force ... income and standing earned outside the realm" (`governments_v2.md:133`, robustness 0.2). The PMC as built does none of that:
- no contracts sold, no external income, no standing;
- succession is dynastic primogeniture.

The military flavour is present: Operators, more and better knights, cheaper MAA and mercenaries, commanders, and the rank ladder. G1 explicitly accepts this (`governments_v2.md:17-19`), so judged against the full standard the fit is PARTIAL.

### Top 3 recommendations
1. **Run the CB-49 PMC slice first:** V-G1, V-G3, V-G4, V-G9 (`kill` Raoul), V-G10 and V-G11. P3, P5 and P7 are all "met (static)" only. Owner: human.
2. **G2 P1 for the PMC:**
   - `eotg_pmc_standing` with one clamped `eotg_pmc_change_standing_effect`;
   - init and teardown in `eotg_gov_on_game_start` / `_on_government_change`;
   - the §3.15 default display (scaled modifier plus story-cycle `basic_counter`);
   - a top-tier "take a contract" and a vassal-tier "deliver" decision that move standing;
   - a feudal-to-PMC adoption decision and an exit decision.
   Owner: architect spec, then scripter.
3. **Add the grant fields** (`possible_grant_vassal_governments` as feudal GT:40). Decide the §5.6 `can_get_government` guard only after V-G11. If T5 shows newly landed PMC vassals on an invalid law, extend the net to `on_title_gain`.

### Unverifiable without in-game test (British Isles sub-mod, `-debug_mode`)
- **T1/V-G3.** Pick Raoul (40406) on the map. Expect no "Is unplayable" and no GAME_OVER tooltip, and the government not remapped at start.
- **T2/V-G1.** error.log has no "preregistered modifier type" for `eotg_pmc_government` and no "Unexpected token" from `eotg_pmc_government.txt`. `database_conflicts.log` shows `KnightCulture` (+ children) overridden.
- **T3/V-G4/V-G9.**
  - The realm screen shows "Command Succession" with a named heir, and Primogeniture is unavailable.
  - `kill` Raoul: the heir is in the dynasty, PMC, has the law, and play continues.
  - Repeat with a minor or female heir.
- **T4.** Make a landed feudal relative the heir and record the resulting government (erosion).
- **T5/V-G6/V-G10.**
  - The contract window shows Contractor Fees / Operational Levies plus 3 rights, with loc.
  - Grant a county to a courtier and record their government **and their succession law** (GAP 4).
- **T6/V-G16.** Debug "Become a PMC" on William adds the law. "Become feudal" drops it.
- **T7/V-G11 and T8/V-G12.** 50-year observer run: PMC only in Valois and its grants or conquests; solvent; no law churn.
- **T9/V-G7/V-G8/V-G18.**
  - "Contractor-General Raoul", vassals "Contractor".
  - Knights tab says Operator(s).
  - Olive map colour.
  - Mercenary placeholder icon.
- **V-G14.** Accolades are available.
- **V-G20.** Record the government of city barons.
- **T10.** A save survives a reload.

### Verdict: PASS (pending in-game) as a playable reskin; FAIL against the distinct-government standard (Q1, Q2, Q5).
