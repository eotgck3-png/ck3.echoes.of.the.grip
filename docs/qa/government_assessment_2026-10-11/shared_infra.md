## QA report: shared government infrastructure + Unsworn, 2026-10-11
Tiger: 436 errors / 250 warnings / 40 tips (whole mod). Government files: 124 findings, **0 real**. Log: `scratchpad/govassess/tiger_govassess.txt` (ANSI-stripped copy: `tiger_clean.txt`)
PX LSP: 6 findings, all `building_walls_*` (known benign). PX vocab: 0. eotg_lint: 0 new. `eotg_[ekdcb]_` grep: empty. Loc BOMs: all present.

### Scorecard
| Area | Verdict | Evidence | Standard |
|---|---|---|---|
| GOVERNMENT_TYPES (main) | MEETS | `common/defines/eotg_government_defines.txt:20-45`: the 20 vanilla keys match `00_defines.txt:550-573` verbatim, plus the 5 mod keys | P6, §5.1.4 |
| GOVERNMENT_TYPES (sub-mod) | MEETS | `zz_eotg_test_bi_government_defines.txt:13-40` = main list + offmap. Nothing masked today. No other mod or vanilla file sets the array | P6 |
| Succession laws (shape) | MEETS | `eotg_government_succession_laws.txt:25-151` mirrors `single_heir_succession_law` (`00_succession_laws.txt:249-347`). `flag = advanced_succession_law` matches vanilla. Its readers are mostly title-law checks; the one realm-law check is at `holy_order_events.txt:2308` | §3.5 |
| Succession safety net | PARTIAL | covers only `on_game_start` and `on_government_change` (`eotg_government_on_actions.txt:10-51`). Tier-up inheritance and mid-game landing are not covered (G1, G2) | §3.5 |
| Contracts | MEETS (min) | groups `groups/eotg_government_contract_groups.txt:17-55`; trees copy `feudal.txt:128-190` by position | §3.3 |
| Knight term | MEETS | `eotg_knight_culture.txt:26-58`: 4 terms + `knight_default` fallback; children match vanilla `:91-123`; 4×8 loc keys present | §3.21 |
| Flavourization | MEETS | 92 entries = 23 per government (5 title, 10 vassal, 8 top at priority 61); all have `top_liege = no`; all 92 loc keys present; no tier words | §3.18 |
| Loc (4 governments) | MEETS | every §3.16 key defined exactly once, engine modifier names included; laws `<law>/_subname/_effects`; groups `/_desc` | §3.16 |
| Unsworn block | PARTIAL | `eotg_unclaimed_government.txt`: guard `can_get_government` (trait) :63-65, not sticky, no fallback; playable (B1); no succession law (G3); loc gaps (G4) | P0, P3, P7 |
| British Isles sub-mod | PARTIAL | placement correct: PMC `k_france.txt` (d_valois), Corporation `k_brittany`, Cartel `k_leon` (+d_asturias, c_pravia), Gob-Corp `k_burgundy` (d_provence). README is stale (P3); T4 and T10 are not covered | §4.4, §5.2 |

### BLOCKERS
None at S1. Nothing here stops a commit. The item below blocks **sign-off of Unsworn against §1**:
- **B1 [S2] Unsworn is playable, and the outcome is undefined.** No P0 entry exists (`common/scripted_rules/` is absent). Each placeholder holds a county, so it passes `is_playable_character` (`00_available_for_events_triggers.txt:964-980`) and the rule's catch-all (`00_rules.txt:237-247`).
  - **What a player who picks one gets:** income ×-10 (`:51`), no council, no buildings, no knights.
  - **No wars:** the CB override bars an Unsworn attacker (`eotg_vanilla_overrides_triggers.txt:37`).
  - **On death:** `eotg_unclaimed_on_death` hands every county to new placeholders *before* death (`eotg_unclaimed_on_actions.txt:73-80`; `eotg_unclaimed_effects.txt:156`). The player inherits nothing, and with `rulers_should_have_dynasty = no` the game is over [inferred]. If V-U8 fails, the player continues as a generated folk heir instead.
  - **Becoming Unsworn mid-game is not possible** for a real character. Every `change_government` call is folk-gated (`effects:59-62, 327-331`; `on_actions:47-51`) and `can_get_government` needs the trait. The lobby pick is the only path.
  - M1 guards exist. M2 and M3 are unbuilt, waiting on V-U1. Owner: architect (template §6.2 option a/b), after V-U1 and T14.

### GAPS
- **G1 The safety net misses tier-up inheritance.** `_laws.info:300-303`: an heir who goes up a tier "gets the laws of the dead ruler" and the conditions are not checked. Two cases:
  - A PMC count who inherits a feudal or tribal kingdom gets that ruler's law.
  - `confederate_partition_succession_law` has `potential` true for our flags (`00_succession_laws.txt:71-80`) and `can_keep` always yes for non-Japanese governments (`:5-14`), so it is **kept forever**, and nothing fires `on_government_change`.

  Fix: add an additive `on_title_gain` entry (trigger: own flag and missing own law) → `eotg_gov_ensure_succession_law_effect`. Owner: scripter.
- **G2 The default-law risk is mis-stated.** The file header (`:18-20`) blames partition, but partition needs `government_is_feudal`. The real pre-emptors are `single_heir_succession_law` (index 3; `should_start_with` is culture only, `:290-297`) and `single_heir_succession_law_youngest` (index 5; **no** `should_start_with`, `:395+`). Both sit before index 50, so a ruler landed mid-game without a government-change event depends on V-G10. Correct the comment and add a test. Owner: scripter.
- **G3 Unsworn has no succession law.** No vanilla order law's `can_have` passes for it, so the engine default (likely youngest) applies and its `can_keep` then fails. Succession is scripted, so the effect is cosmetic or churn ("Anarchy" display risk, P3). Record the decision in the spec, or give it a placeholder law. Owner: architect.
- **G4 Unsworn loc gaps:** `eotg_unclaimed_government_filter_option`, `_filter_option_desc` and `_vassals_label` are missing. Vanilla herder defines all three. Owner: localizer.
- **G5 The two GOVERNMENT_TYPES copies have no drift guard.** The sub-mod's `zz_` copy wins [engine, unverified load order]. A key added only to the main file would be masked during sub-mod tests. Add an eotg_lint rule that diffs the two lists, plus a check of the vanilla 20. Owner: scripter/orchestrator.
- **G6 T-list coverage:** V-G1–V-G20 cover T1–T3, T5–T9. Missing:
  - T4 (erosion through a feudal relative);
  - T10 (save compatibility);
  - T3 with a female or minor heir;
  - tier-up law inheritance (G1).

### POLISH
- Other mods are cited as precedent, against the owner rule of 2026-10-11 (Appendix A): `eotg_government_defines.txt:11` (After the End) and `eotg_knight_culture.txt:8-9` (TFE). Replace them with vanilla citations. Owner: scripter.
- `has_government = feudal_government` in a debug-only decision (`eotg_government_debug_decisions.txt:155`) breaks §5.1.5 in letter only.
- Sub-mod README §Mod governments (`README.md:113-131`) says the keys are "not defined yet" and the default is `off`, but `gen_history.py:56` has `'on'`. The line-14 summary still says "feudal stand-ins". Owner: cartographer.
- The 40 Tiger tips ask for `<level>_desc` on contract levels. Vanilla feudal levels have none either, so this is optional. The obligations header (`:14`) lists `_desc` as required; align it.
- No `modifier_definition_formats` for our 5 governments. Vanilla also omits herder, mandala, meritocratic and steppe_admin, and the mod never uses the generated modifiers. Harmless.
- **Template contradiction:** §3.6 says castle-primary + city-valid "appears nowhere in vanilla", but administrative has exactly that (`00_government_types.txt:482-483`), as do celestial (:832-833) and steppe_admin (:1137-1138). Report to the architect.
- Unsworn has no `required_county_holdings`. Herder sets it (`:762`).

### Tiger triage (government files)
| File | Count | Category | Verdict |
|---|---|---|---|
| `laws/eotg_government_succession_laws.txt` | 69 | unknown-field 20, duplicate-item 16, exact-duplicate 15, missing-loc on `potential`/`can_have`/... 18 | **Benign.** This is the 1.20 law-group parse family: Tiger reads each law as a group, and `eotg_augmentation_laws.txt` shows the identical pattern |
| `scripted_effects/eotg_government_effects.txt:19-49` | 8 | missing-item "law not defined" | Benign, same family (CLAUDE.md lists it only for `eotg_aug_policy_*`) |
| `governments/*.txt` (all 5) | 5 | unknown-field `allow_accolades` | Benign. Vanilla-only field (`00_government_types.txt:11`; template §4.6) |
| `subject_contracts/contracts/eotg_government_obligations.txt` | 40 | tips: suggest `_desc` loc | Note, not a bug (vanilla has none) |
| `eotg_unclaimed_templates.txt:24`, `eotg_unclaimed_effects.txt:121` | 2 | unknown-field `rite` | Benign (CLAUDE.md `rite` family) |
| contract groups, flavourization, knight culture, government defines, government loc, government on_actions, government triggers | 0 | none | Clean |

Ask for the orchestrator: add the government succession laws and `allow_accolades` to the known-benign list in CLAUDE.md, so the next QA pass doesn't re-triage them.

### Top 3 recommendations
1. **Extend the succession net to `on_title_gain`** (G1/G2) before G2 builds on the four. It closes the confederate-partition trap and the youngest/primogeniture default, and costs one additive on_action.
2. **Decide Unsworn's playability now** (B1): run V-U1 and T14. If the key-level override in `zz_eotg_rules.txt` works, add the GAME_OVER entry; otherwise record option (b) on the taskboard. Settle G3 (no law) in the same spec pass.
3. **Lint the two GOVERNMENT_TYPES copies against each other and against vanilla's 20** (G5). It is the only define in the mod that silently breaks on a CK3 patch.

### In-game tests needed (human, British Isles sub-mod)
- error.log: no "preregistered modifier type"; `database_conflicts.log` shows `KnightCulture` from `eotg_knight_culture.txt` (V-G1).
- Pick an Unsworn placeholder in the lobby: is the pick allowed? Then `kill` it: game over, or does play continue as folk? (V-U1, B1)
- `kill` a PMC count whose heir also holds a feudal kingdom elsewhere (or console-grant): record the heir's law after tier-up (G1).
- Grant a county to a courtier of each realm: record the new vassal's government **and succession law** (V-G10 + G2).
- T3 with a female heir and with a minor heir; T4 erosion; T10 save and reload.
- Unsworn's realm screen: which succession law shows, and is there an "Anarchy" label (G3)?

### Audits run: 1, 2 (prefix in shared files), 5, 6 (sub-mod `replace_path` history/titles is generated and gitignored, OK), 7, 9 (all 5 governments appear in sub-mod `history/titles`), 10. Skipped: 3, 4, 8 (no events in scope).
### Verdict: PASS (pending in-game) for the shared layer. The Unsworn sign-off is FAIL until B1 has an owner decision. The shared layer is clean on every static check, and its two real gaps (G1/G2) are reachable only through inheritance edge cases.
