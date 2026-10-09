# Spec: Cybernetics v2: The Neurofractured Kingpin

**Author:** eotg-architect, 2026-10-06.
**Requested by:** the owner, relayed by the orchestrator, 2026-10-06. The owner's request in brief: a criminal organization's leader has gone Neurofractured and may become a problem. Branch events let the character collaborate with the kingpin, back the kingpin to claim the character's **liege's** title for later rewards, cause a civil war, and reach "a dozen other outcomes that range from good to bad, from meagre execution of the kingpin to the character becoming a localized crisis". The target is 12 or more distinct final outcomes.
**Owner addition (binding, 2026-10-06):** the organization must feel different each time. The spec rolls a stored **organization profile** and a **kingpin mind** at entry. The profile changes which middle events can fire, which options appear, the odds and the outcomes, and some leaves are reachable only through certain profiles. Each profile has its own desc variants at the key beats (§5.2).
**Index:** [cybernetics_v2.md](cybernetics_v2.md). Index §1 rules 1–12 and the §5 lore register apply to every line of this spec unless this file says otherwise.
**Builds on:** the Patron story ([phase5](cybernetics_v2_phase5.md) §2, [reprisal](cybernetics_v2_reprisal.md)), the named sellers ([seller_names](cybernetics_v2_seller_names.md)), Neurofractured mode ([phase3](cybernetics_v2_phase3.md)), the balance amendments ([balance](cybernetics_v2_balance.md)), the writing review (`docs/qa/event_writing_review_2026-10-05.md`) and the rewrite feedback (`docs/proposals/gemini_rewrite_feedback_2026-10-06.md` §2–§4).
**Lore review (2026-10-06): changes required, applied in this revision** (the lore-keeper's ruling, relayed by the orchestrator; binding wording in §7.4).
**Owner answers (2026-10-06):** §11 Q2–Q6 ruled and folded in: the story passes to the heir (§5.4.1), entry is 2% a year (§5.3), empire-tier claims stay open, L12 stays vanilla independence, and leverage is **visible as three bands** (§2, §5.4.2).
**Sequence:** architect (this file) → lore-keeper (canon review, §8 questions) → scripter (batch A, then batch B, see the handoff) → localizer → QA → orchestrator commits.

---

## 1. Purpose & gate

Somebody runs the lower levels of your capital: a crew, a syndicate's local business, a clinic that is really a front, or a hired crew between contracts. Their boss has gone Neurofractured. The boss's implant now runs a model of them slightly ahead of them, and they have started to act on it. The story asks what a ruler does with a dangerous, useful, failing person who controls the crime under their seat:
- execute them cheaply;
- clean the streets properly;
- take their money;
- take their guns into a war against your own liege;
- let them do it for you;
- or end up as the thing they hold.

Each run rolls an organization profile and a kingpin mind, so two runs don't play the same (§5.2).

**Gate:** 3 (Systems). Cybernetics is a mod-exclusive system, built and tested against the temporary map (CLAUDE.md, 2026-10-02; `docs/agent_workflow.md` §5 rule 2). **Not blocked.** The design is map-agnostic: it names no title, province, character, culture or faith key. Every title comes from a scope (`liege.primary_title`, a held county, a neighbour's primary title). The kingpin inherits `root.culture` and `root.faith` by scope (index §1 rule 9).

**Size:** 42 events (25 nodes including the heir notification, 17 leaves), 1 story cycle, 2 character templates, 1 custom on_action, 10 character/county modifiers, 6 opinion modifiers, 1 script value file, about 14 scripted effects and 8 scripted triggers, 1 debug decision, and about 420 loc keys. It is built in **two batches** (handoff): A is entry, collaboration, the law path and the non-war leaves; B is the claim path, the wars and the crisis stage.

---

## 2. Signature resource

**The kingpin's `eotg_fracture_risk`**, read as Neurofractured episode pressure. It is the existing cybernetics variable, on an augmented character (index §1 rule 4: "on root **or a saved augmented character**"). The kingpin holds `eotg_neurofractured`, so `eotg_add_fracture_risk` works on them unchanged. The bands are the existing triggers, run on `scope:eotg_kp`: `eotg_aug_pressure_flicker` / `_fracture` / `_storm`.

- **Start:** rolled by mind (§5.2.3): 15–45.
- **Drift:** each yearly tick adds `eotg_aug_kp_drift_value` (§5.6): base +6, purge mind +4, crew kind +2, during a war stage +6, and −4 for each calm option taken since the last tick (counted in `eotg_kp_calmed`, reset on tick), with a floor of 2. From 30, a calm run reaches Storm (60) in about 4 years and the terminal (95) in about 8 to 10.
- **Terminal at ≥ 95:** the tick resolves the story at once, to The Break (massacre, L9) or The Fracture Finishes It (cascade death, L16), §5.5 T1.
- **Hidden:** the kingpin's fracture risk has no number, bar or counter, ever (index §1 rule 3). Prose reads its band. (Leverage, below, is the one visible value, as bands.)

**Coupling rule (invariant 5, binding on every event in this spec):** every event either moves the kingpin's pressure in at least one option (`scope:eotg_kp = { eotg_add_fracture_risk = { AMOUNT = N } }`) **or** reads the band in a `triggered_desc`. Leaves read it in their desc, and the ending text differs by band. The per-event column in §5.8 says which.

**Secondary state (story variable, not the signature): `eotg_kp_leverage`, 0–100**, the organization's hold on you. Taking money, running errands and staying quiet raise it. Refusals, unmasking an informant and evidence lower it. It selects between collaboration's endings (§5.5 T4) and decides whether the crisis closes on you (T2). **Visible as three bands, never as a number** (owner ruling Q6, 2026-10-06; §5.4.2): 1 "A favour owed" (0–40), 2 "Deep in their pocket" (41–79), 3 "They own the room" (80–100). The band thresholds are the tree's own thresholds (T4 ≤ 40, T2 ≥ 80), so the band the player sees tells them which endings are near. The kingpin's fracture risk stays hidden.

The root's own risk moves only where the root's own implant is in the scene (the Neurofractured-root option in .002 and .072, §5.8). Nothing here creates risk on an unaugmented root (`eotg_add_fracture_risk` already guards that).

---

## 3. Identifier table

All keys carry `eotg_`. There are no landed titles. Loc key form: the index's dot form (`eotg_aug_kingpin.001.t / .desc_* / .a`), not `_NNNN_t`. Index §0 "Decided here" binds the cybernetics namespaces to the dot form. The owner's brief named the namespace `eotg_aug_kingpin`, and the keys follow it.

| Identifier | Type | Exact name | Owner |
|---|---|---|---|
| Namespace | event namespace | `eotg_aug_kingpin` | scripter |
| Events (nodes) | character_event | `eotg_aug_kingpin.001`–`.015`, `.030`–`.034`, `.036`, `.038`, `.039`, `.040` (the heir's notification), `.050` | scripter |
| Events (leaves) | character_event | `eotg_aug_kingpin.060`–`.076` | scripter |
| Story cycle | story_cycle | `eotg_story_aug_kingpin` (`visible = yes`, §5.4.2) | scripter |
| Leverage band | story variable (int 1–3) | `eotg_kp_leverage_band` (written only by `eotg_aug_kp_leverage_effect`; read by the story's `basic_counter` and the custom loc) | scripter |
| Leverage band name | customizable_localization (`type = all`, run on the story) | `eotg_aug_kp_cl_leverage_band` (texts `eotg_aug_kp_band_1` / `_2` / `_3`; fallback `_1`) | scripter |
| Inherited marker | story variable (bare, one-shot) | `eotg_kp_inherited` (set in `on_owner_death`, read by .040's desc and removed in its `after`) | scripter |
| Leaf guard | story variable (bare) | `eotg_kp_resolving` (set in the `immediate` of every leaf and of .036; `on_owner_death` ends the story instead of passing it on) | scripter |
| Custom on_action | on_action | `eotg_on_yearly_aug_kingpin_check` | scripter |
| Kingpin template | scripted_character_template | `eotg_aug_kingpin_template` (age 32–58; `gender_female_chance = 50`; **no** personality traits; `random_traits_list` count 1 from `education_intrigue_3`, `education_martial_3`, `education_stewardship_2`; `random_traits = no`; martial 10–16, intrigue 10–16, stewardship 6–12, prowess 10–16) | scripter |
| Lieutenant template | scripted_character_template | `eotg_aug_kp_lieutenant_template` (age 25–45; 50% female; one of `ambitious`, `deceitful`, `craven`, `honest`; intrigue 8–12) | scripter |
| Kingpin marker | character flag | `eotg_flag_aug_kingpin` | scripter |
| Watched kingpin (L11 b) | character flag | `eotg_flag_aug_kingpin_watched` (10 years) | scripter |
| Grudge (L14 b) | character flag | `eotg_flag_aug_kingpin_grudge` (seed, read by nothing yet) | scripter |
| Once per life | character flag | `eotg_flag_aug_had_kingpin` | scripter |
| Entry cooldown | character flag | `eotg_flag_aug_kingpin_cooldown` (10 years; on_action only) | scripter |
| Passthrough | character variable | `eotg_kp_passthrough` (root → story) | scripter |
| Profile | character variables on the kingpin (flags) | `eotg_kp_kind` (`crew`/`syndicate`/`front`/`hired`), `eotg_kp_method` (`violence`/`bribery`/`blackmail`/`infiltration`), `eotg_kp_reach` (`local`/`wide`), `eotg_kp_mind` (`purge`/`grandeur`/`forecast`/`cold`) | scripter |
| Organization name | character variables on the kingpin (existing names, existing generated effects) | `eotg_aug_seller_gang` (crew, hired), `eotg_aug_seller_company` (front), `eotg_patron_syndicate_passthrough` (syndicate) | scripter (rolls), gen (effects/custom loc unchanged) |
| Front exclusion | character variable on the kingpin (flag), transient | `eotg_kp_exclude_company` | scripter |
| Debug overrides | character variables on root | `eotg_kp_force_kind`, `_method`, `_reach`, `_mind` | scripter |
| Story variables | story variables | §5.4 table (`eotg_kp`, `eotg_kp_stage`, `eotg_kp_path`, `eotg_kp_leverage`, `eotg_kp_refusals`, `eotg_kp_years`, `eotg_kp_war_years`, `eotg_kp_calmed`, `eotg_kp_target`, `eotg_kp_opponent`, `eotg_kp_rival`, `eotg_kp_informant`, `eotg_kp_informant_unmasked`, `eotg_kp_playing`, `eotg_kp_forewarned`, `eotg_kp_evidence`, `eotg_kp_spiral_done`) | scripter |
| Saved scopes | event scopes | `eotg_kp`, `eotg_kp_story`, `eotg_kp_target`, `eotg_kp_opponent`, `eotg_kp_rival`, `eotg_kp_informant`, `eotg_kp_lieutenant`, `eotg_kp_errand_target`, `eotg_kp_purge_target`, `eotg_kp_county`, `eotg_kp_reporter`, `eotg_kp_victim`, `eotg_kp_victim_2`, `eotg_kp_war`, `eotg_patron_story` (reused) | scripter |
| Scripted effects | scripted_effect | `eotg_aug_kp_start_effect`, `eotg_aug_kp_roll_profile_effect`, `eotg_aug_kp_roll_name_effect`, `eotg_aug_kp_add_mind_traits_effect`, `eotg_aug_kp_leverage_effect` (param `AMOUNT`, clamps 0–100, then writes `eotg_kp_leverage_band`), `eotg_aug_kp_inherit_effect` (§5.4.1), `eotg_aug_kp_refuse_effect` (refusals +1, kp +`$RISK$`), `eotg_aug_kp_calm_effect` (kp −`$RISK$`, calmed +1), `eotg_aug_kp_set_stage_effect` (param `STAGE`), `eotg_aug_kp_raise_claimant_effect` (params `CLAIMANT`), `eotg_aug_kp_war_support_effect`, `eotg_aug_kp_seize_county_effect`, `eotg_aug_kp_grant_county_effect`, `eotg_aug_kp_end_effect`, `eotg_aug_kp_save_scopes_effect` (every event's `immediate` opener) | scripter |
| Scripted triggers | scripted_trigger | `eotg_aug_kp_can_start`, `eotg_aug_kp_root_is_vassal`, `eotg_aug_kp_root_is_independent`, `eotg_aug_kp_liege_claim_possible`, `eotg_aug_kp_neighbour_target`, `eotg_aug_kp_vassal_seat_target`, `eotg_aug_kp_seizable_county` (county: held by root, not the capital, tier county), `eotg_aug_kp_errand_target`, `eotg_aug_kp_purge_target`, `eotg_aug_kp_informant_candidate`, `eotg_aug_kp_is` (params `AXIS`, `VALUE`: `scope:eotg_kp.var:eotg_kp_$AXIS$ ?= flag:$VALUE$`) | scripter |
| Script values | script_value | `eotg_aug_kp_drift_value`, `eotg_aug_kp_arrest_value`, `eotg_aug_kp_levies_value` | scripter |
| Character modifiers | static modifier | `eotg_mod_aug_kp_arrangement` (`domain_tax_mult = 0.08`, `county_opinion_add = -5`), `eotg_mod_aug_kp_hired_guns` (`levy_size = 0.15`; vanilla shape `common/modifiers/00_activity_hold_court_modifiers.txt:29`, `levy_size = 0.2`), `eotg_mod_aug_kp_network` (`domain_tax_mult = 0.15`, `vassal_opinion = -5`, `enemy_hostile_scheme_success_chance_add = -10`), `eotg_mod_aug_kp_exposed` (`vassal_opinion = -10`, `general_opinion = -5`), `eotg_mod_aug_kp_kept` (`stress_gain_mult = 0.25`, `dread_gain_mult = 0.5`, `tyranny_gain_mult = 0.25`, `vassal_opinion = -15`), `eotg_mod_aug_kp_tribute` (`domain_tax_mult = -0.1`), `eotg_mod_aug_kp_informants` (`enemy_hostile_scheme_success_chance_add = -10`), `eotg_mod_aug_kp_seized_clinic` (`domain_tax_mult = 0.05`) | scripter (keys verified in PX `modifiers.log`, 2026-10-06) |
| County modifiers | static modifier | `eotg_mod_aug_kp_arson` (`monthly_county_control_decline_add`), `eotg_mod_aug_kp_lockdown` (`monthly_county_control_growth_add = 0.3`, `development_growth_factor = -0.2`), `eotg_mod_aug_kp_loose_ends` (`monthly_county_control_decline_add`), `eotg_mod_aug_kp_streets_cleared` (`monthly_county_control_growth_add = 0.3`, `county_opinion_add = 5`), `eotg_mod_aug_kp_crisis` (`development_growth_factor = -0.25`, `county_opinion_add = -10`, `levy_reinforcement_rate = -0.2`), `eotg_mod_aug_kp_burned_levels` (`development_growth_factor = -0.3`, `levy_size = -0.2`), `eotg_mod_aug_kp_massacre` (`county_opinion_add = -15`, `development_growth_factor = -0.2`) | scripter (first-guess values; QA tunes) |
| Opinion modifiers | opinion_modifier | `eotg_opinion_aug_kp_order` (+10, 10 y), `eotg_opinion_aug_kp_kingmaker` (+50, 20 y, decaying), `eotg_opinion_aug_kp_conspired` (−30, 10 y), `eotg_opinion_aug_kp_harboured` (−20, 10 y), `eotg_opinion_aug_kp_raised_criminal` (−10, 10 y), `eotg_opinion_aug_kp_warned` (+20, 10 y) | scripter. System-scoped (index §1 rule 1), not shared with any government. |
| Army name | loc key | `eotg_aug_kp_army_name` | localizer |
| Toasts | loc keys | `eotg_aug_kingpin_toast_gone`, `eotg_aug_kingpin_toast_dead` | localizer |
| Story panel loc | loc keys | `eotg_story_aug_kingpin` (name), `eotg_story_aug_kingpin_info` (custom string), `eotg_story_aug_kingpin_kp_label`, `eotg_story_aug_kingpin_band_label`, `_band_min_label`, `_band_max_label`, `eotg_aug_kp_band_1` / `_2` / `_3` | localizer |
| Debug decision | decision | `eotg_decision_aug_debug_kingpin` (`debug_only = yes`; runs the start effect with the force variables; precedent `common/decisions/eotg_unclaimed_decisions.txt:9`) | scripter |
| Name lists, CoAs, holy sites, icons | — | **None new.** Names come from the existing seller lists (`cybernetics_seller_names.txt`, owner), and characters from the culture's name list. The landed kingpin (L4, L10, L12) uses the existing title's CoA. The event themes are vanilla (`intrigue`, `stewardship_wealth_focus`, `war`, `dread`, `realm`); no art debt. | — |

No new trait, death reason, decision art, law, government or MAA.

## 4. File placement

| Path | What | Written by |
|---|---|---|
| `events/eotg_augmentation_kingpin.txt` | 42 events, with the namespace header in the Patron file's form (callers, cooldown authority, resource, naming) | scripter |
| `common/story_cycles/eotg_aug_kingpin_story.txt` | `eotg_story_aug_kingpin` | scripter |
| `common/on_action/eotg_aug_kingpin_on_actions.txt` | the `yearly_playable_pulse` extension and the custom on_action | scripter |
| `common/on_action/eotg_augmentation_on_actions.txt` | **E1**, one trigger line | scripter |
| `common/scripted_character_templates/eotg_augmentation_templates.txt` | append the two templates | scripter |
| `common/scripted_effects/eotg_aug_kingpin_effects.txt` | effects (§3) | scripter |
| `common/scripted_triggers/eotg_aug_kingpin_triggers.txt` | triggers (§3) | scripter |
| `common/script_values/eotg_aug_kingpin_values.txt` | values (§5.6) | scripter |
| `common/customizable_localization/eotg_aug_kingpin_custom_loc.txt` | the band-name custom loc (hand-written; **not** one of the generated seller-name files) | scripter |
| `common/modifiers/eotg_aug_kingpin_modifiers.txt` | 15 modifiers | scripter |
| `common/opinion_modifiers/eotg_aug_kingpin_opinions.txt` | 6 opinions | scripter |
| `common/decisions/eotg_aug_kingpin_decisions.txt` | the debug decision | scripter |
| `localization/english/eotg_aug_kingpin_l_english.yml` | **all** keys of §7.2, including the story-panel keys, UTF-8 with BOM | localizer |

Every folder already exists in the mod. No `replace_path`. **The seller generator, its list and its generated files do not change.**

---

## 5. Wiring

### 5.1 Who the player is, and who the kingpin is

#### 5.1.1 The player (root)

- **Eligible:** landed, `highest_held_title_tier >= tier_county`, adult, not imprisoned, `eotg_is_unclaimed_folk = no`, and not a landless adventurer (`NOT = { government_has_flag = government_is_landless_adventurer }`). The capital must be developed enough for implants to be traded there (`capital_county.development_level >= 10`, the same floor as `eotg_can_receive_augmented`).
- **Role** (`eotg_aug_kp_root_is_vassal` / `_is_independent`, §3):
  - **Vassal:** `is_independent_ruler = no` and `exists = liege`. The liege-claim branches (.003 b/c → .030) are open.
  - **Independent:** `is_independent_ruler = yes`. Fallback branches replace the liege claim:
    - **.031 The Neighbour's Seat:** back the kingpin's claim on a neighbouring independent ruler's primary title (`random_neighboring_top_liege_realm_owner`, PX `effects.log:8138`; `top_liege = this` is implied for an independent root). Vanilla `claim_cb` with `claimant =`.
    - **.032 The Vassal's Seat:** hand the kingpin a landed vassal's primary title by decree. This is the independent ruler's **civil war**: the angriest remaining vassal raises a faction against you (§5.8 .032).
  - Neither is available → the claim options are hidden, and the rest of the tree runs.
- **Tiers:** counts through emperors. The same role gates apply at every tier (CLAUDE.md "not empire-only"). An emperor's realm is big, so the claim war is long (the spiral, L7, is likelier). That is the intended texture, not a bug.

#### 5.1.2 The kingpin (`scope:eotg_kp`, story variable `eotg_kp`)

- **Created, not picked.** The kingpin is new to the world, and their organization never existed before this story. Picking an existing courtier would make the "lower levels" a court member, and no vanilla character is a crime boss. Template `eotg_aug_kingpin_template` (§3), created in `eotg_aug_kp_start_effect`, which follows the Patron's envoy shape: `create_character = { template = … location = root.capital_province culture = root.culture faith = root.faith save_scope_as = eotg_kp }` (precedent `eotg_aug_patron.009`, `events/eotg_augmentation_patron.txt:1377-1383`; vanilla `events/story_cycles/ep3_story_cycle_el_cid.txt:1406-1409`).
- **Neurofractured on creation:** `add_trait = eotg_neurofractured`, `eotg_apply_neurofracture_distortion = yes`, `set_variable = { name = eotg_fracture_risk value = <mind start> }`. Never `eotg_trigger_neurofracture`: it fires a ruler event and opens the ruler cooldown. Same reasoning as `eotg_aug_nr_cascade_effect`.
- **Personality:** the template rolls **no** personality traits. The mind (§5.2.3) adds exactly two, which never conflict. One more comes from a list that excludes the mind's opposites: three in total, the vanilla cap.
- **Flag:** `eotg_flag_aug_kingpin` (permanent while the story runs, removed in `on_end`). It keeps the kingpin out of `eotg_on_yearly_aug_nonruler_check` (§5.3 edit E1), so the story's tick is the only drift.
- **Courtier status by stage** (the story checks it in maintenance, §5.5 M0):

| Stage | Where the kingpin is | Why |
|---|---|---|
| `open`, `collab`, `kept` | **Pool character at root's capital province** (no employer) | They run the lower levels; they are not your courtier. Vanilla creates pool characters with `location =` and no employer (el_cid precedent above). |
| custody (.013) | root's prisoner (`imprison_character_effect`, vanilla `00_prison_effects.txt:1644`) | |
| `pending`, `war` (claim path) | **root's courtier** (`add_courtier`). In the vassal "back the kingpin" path and the independent "neighbour" path, they are the claimant in your court, as vanilla claimants are. | A claimant faction or `claim_cb` needs a claimant that the attacker can field. |
| leaves | as the leaf says: dead, landed (L4, L10, L12), your courtier (L11), the liege's courtier (L6, L8), or the pool (L14) | |

- **Risk to check (V-K1):** an AI may invite a pool character to its court. The maintenance check M0 resolves it: if the kingpin's employer exists and is neither root nor (in custody) root's prison, the story ends silently through `on_end` with a toast (`eotg_aug_kingpin_toast_gone`). If the in-game check shows this happens often, the fallback is to keep the kingpin as root's guest (`add_visiting_courtier`, the Collector precedent `eotg_augmentation_patron.txt:1384`) and re-add them on the tick. The scripter builds the pool version. QA reports the observer count.

#### 5.1.3 Exclusivity and the Patron

| Situation at entry | Rule |
|---|---|
| Root owns `eotg_story_aug_kingpin` | No entry (on_action trigger). One kingpin at a time. |
| Root has `eotg_flag_aug_had_kingpin` | No entry. **Once per life** (set in `on_setup`; precedent `eotg_flag_aug_had_patron`, `eotg_augmentation_stories.txt` patron `on_setup`). |
| **Root owns a Patron story** (`eotg_aug_has_patron = yes`) | Entry weight ×2. **The kind is forced to `syndicate`, and the syndicate is the Patron's own:** `scope:eotg_kp = { set_variable = { name = eotg_patron_syndicate_passthrough value = scope:eotg_patron_story.var:eotg_syndicate } }` (var-to-var copy, vanilla `00_animal_effects.txt:395-398`). If the story has no `eotg_syndicate` (an old save), it rolls. The kingpin is **that syndicate's local boss in your realm**, never its head (§8 L3). .001 gains option d "Ask the envoy to deal with [kp]" (needs `eotg_aug_patron_envoy_present = yes`), which leads to L15. Its cost is one Patron demand step (`eotg_aug_patron_demand_effect`, scope `eotg_patron_story` saved in .001 `immediate`). **Nothing else in the Patron story changes.** Its tick, demands and endings run as built. |
| Patron story ends while the kingpin story runs | Nothing. The kingpin keeps the copied syndicate name: it is on the kingpin, not on the Patron story. |
| Countdown, Heir's Arc, Retinue running | No interaction. Both stories can tick in the same year; the kingpin's tick fires at most one event a year (§5.7). |
| Root is Neurofractured | Allowed. .002.d and .072.c open (the root's own implant in the scene). The kingpin's text never uses the voice-register lines reserved for the root's implant. |

### 5.2 Variation (owner addition)

At entry, `eotg_aug_kp_roll_profile_effect` stores four things **on the kingpin** as character variables holding flags, the same mechanism as the seller names. A fifth thing, the organization's **name**, is rolled through the existing seller-name effects into the variable that fits the kind. Debug overrides: root variables `eotg_kp_force_kind`, `_method`, `_reach`, `_mind`. If one is present, it wins over the roll and is removed (§9.1).

#### 5.2.1 Kind (`var:eotg_kp_kind`): what the organization *is*

| Kind flag | Kind | Named from (existing seller system) | Trade | Where they hole up (desc texture) |
|---|---|---|---|---|
| `flag:crew` | **A street crew** | `[gangs]`: `eotg_aug_roll_gang_effect = { VAR = eotg_aug_seller_gang }` on the kingpin → `[eotg_kp.Custom('eotg_aug_cl_gang')]` (plural, "the Cut Lines") | protection and debt collection in the underlevels | the stacks, stairwells, a shuttered market level |
| `flag:syndicate` | **A syndicate's local business** | `[syndicates]` (canon): `eotg_aug_roll_syndicate_effect = { VAR = eotg_patron_syndicate_passthrough }` on the kingpin, or copied from the Patron (§5.1.3) → `[eotg_kp.Custom('eotg_aug_cl_syndicate_offer')]` | contraband cargo and unvetted implants through the docks | a cargo hulk, bonded warehouses, the customs desk that waves them through |
| `flag:front` | **A clinic that is a front** | `[companies]`: `eotg_aug_roll_company_effect = { VAR = eotg_aug_seller_company }` on the kingpin → `[eotg_kp.Custom('eotg_aug_cl_company')]` (singular, no article) | a licit fitting house that keeps every client's logs and sells what it learns. It **services and deals**; it never makes hardware (seller spec §8.1.2) | consulting rooms, the records vault, the back rooms behind recovery |
| `flag:hired` | **A hired crew between contracts** | `[gangs]` (as crew) | muscle and boarding crews for hire; guns kept on retainer. They answer to a contract, not to a street: disciplined, mobile, loyal to whoever pays next | a barracks ship, a rented hangar, the drill floor |

**Why these four:** each has a different way of hurting you. Each gives the tree a different lever:
- the crew: the streets;
- the syndicate: money;
- the front: files;
- the hired crew: guns.

Each is named from the list that fits it, so no new names are invented (owner rule). **Salvage is not a trade:** the salvage buyer stays unnamed in canon (`cybernetics_v2_interactions.md:841`), and gang names carry no salvage words.

**Kind weights at entry:** crew 30, syndicate 0, front 25, hired 20. **A syndicate-kind kingpin exists only with a Patron** (ruling: index §5 item 3, `cybernetics_v2.md:211`: the generated syndicate name is for the Patron's syndicate only). A Patron forces `syndicate`. Without a Patron the syndicate weight is 0, and it stays 0 when more syndicates are added unless that index rule changes. Consequence: L15's "without a Patron" branch is **dead** while the rule holds (kept so the leaf survives a future ruling). Under a realm **Ban** law (`eotg_aug_under_policy = { LAW = ban }`), crew ×1.5 (the back streets). Under a **License**, front ×1.5 (the licit cover).

**The front-kind roll excludes root's clinic of record** (lore review item 6): before rolling, copy root's record onto the kingpin (`set_variable = { name = eotg_kp_exclude_company  value = root.var:eotg_aug_clinic_of_record }`, only if root has one), run `eotg_aug_roll_company_except_effect = { VAR = eotg_aug_seller_company  EXCLUDE = eotg_kp_exclude_company }`, then remove the exclusion variable. Your own clinic is never the front.

**Pronoun and grammar contract:** gang names are plural, and company and syndicate names are singular (seller spec §7). Every line that names the organization is a **per-kind** variant, so each variant fixes its own verb agreement. Lines shared across kinds name only the kingpin (`[eotg_kp.GetFirstName]`, `[eotg_kp.GetFirstNamePossessive]`), never the organization. Never write `'s` after a `Custom()` call.

#### 5.2.2 Method (`var:eotg_kp_method`) and reach (`var:eotg_kp_reach`)

Method is rolled with weights that depend on the kind:

| Method | crew | syndicate | front | hired | What it unlocks |
|---|---|---|---|---|---|
| `flag:violence` | 60 | 10 | 0 | 70 | .008 Protection Bill weight ×2; .005 is the "remove someone" errand; arrest failure leads to the Region seizure (.071) more often |
| `flag:bribery` | 15 | 50 | 15 | 20 | .004 The Ledger; .003 option "The Cut"; .012 resolves as "your guard was bought" |
| `flag:blackmail` | 15 | 20 | 50 | 0 | .005 is the "a file on someone" errand; .003 front option "your liege's file"; the own-claim path costs no leverage (the claim is forged from their files) |
| `flag:infiltration` | 10 | 20 | 35 | 10 | .007 The Informant can fire; arrest rolls −10 until the informant is unmasked; .005 is the "seat my person at your court" errand |

Reach is `flag:local` (60) or `flag:wide` (40), and syndicates roll wide at 60:
- **wide:** arrest rolls −10; .009 The Lieutenant weight ×2; gold amounts one step up (minor → medium); war levies ×1.5;
- **local:** the Region seizure (.071) needs `local` or Storm, because they hold ground they know.

#### 5.2.3 Mind (`var:eotg_kp_mind`): how the Neurofracture shows

| Mind | Traits added | Start pressure | Drift | What the implant does to them (text; voice rules §7.3) | Mechanical lean |
|---|---|---|---|---|---|
| `flag:purge` | `paranoid`, `wrathful` | 35–45 | +4 | The implant forecasts the kingpin's **own** suspicion and violence before they feel it: it has them reaching for a lieutenant a day before they know they have stopped trusting that lieutenant. It never flags other people. They act on the forecast, and lieutenants vanish. | .006 purge variant; massacre (L9) odds ×1.5; betrayal (L8) ×1.25; .034 Turned Guns opens without low leverage |
| `flag:grandeur` | `arrogant`, `ambitious` | 25–35 | +0 | The overlay never shows them hesitating any more, and they read that as a mandate. They want to be seen. | .006 grandeur variant (public honours); the "back the kingpin" option gets ai_chance +20 for the kingpin's side; L4 rewards ×1.5, paid in public |
| `flag:forecast` | `eccentric`, `calm` | 20–35 | +0 | The implant's model of them runs slightly ahead, and they have stopped arguing with it. They do what it shows them about to do, and they say so. A forecast of **themselves**, never of plots or of you. | .006 forecast variant: they **warn you about themselves** (sets `eotg_kp_forewarned`, which halves L8's costs) |
| `flag:cold` | `callous`, `diligent` | 15–30 | −2 | Affect flattened. The implant runs them so evenly that nothing reaches the face: they look at the floor when spoken to, and price everything. | .006 cold variant (itemized costs); the Neighbour's Seat and Vassal's Seat wars go better (+1 levy step); massacre odds ×0.5 |

**Mind weights by kind** (crew/syndicate/front/hired): purge 45/20/15/15, grandeur 20/35/20/15, forecast 25/20/25/25, cold 10/25/40/45. Crew leans purge (a street boss who turns on his own); hired leans cold (a captain who prices the job).

**Third trait:** one of `greedy`, `deceitful`, `vengeful`, `stubborn`, `impatient`, `cynical`, filtered against the mind's two traits by `NOT = { has_trait = <opposite> }`. Vanilla `random_traits_list` cannot filter, so this list is an `add_trait` `random_list` in the start effect, with a trigger on each entry (precedent: the seller roll effects' `random_list` with `trigger`).

#### 5.2.4 The matrix: profile × events, options and outcomes

`●` = only this profile; `▲` = weighted up; `▼` = weighted down; `–` = absent.

| | crew | syndicate | front | hired |
|---|---|---|---|---|
| **.001 opening desc** | bodies, protection money, a stairwell | a cargo that never clears customs | a client list, a fitting gone wrong on purpose | a crew back from a contract with nowhere to spend it |
| **.001 kind option** | "Pay them to keep their boss quiet." → collab ● | (Patron only) "Ask the envoy…" → L15 ● | "Audit the clinic's client records." → .015 ● | "Buy out their next contract." → collab, `eotg_mod_aug_kp_hired_guns` ● |
| **.003 kind option** | "Keep the stacks quiet, and we talk again." | "Take your cut and look away." (gold now) | (vassal) "Your files on [liege]. Now." (root gets a weak blackmail hook on the liege) | "I'll keep your guns on retainer." (`eotg_mod_aug_kp_hired_guns`) |
| **Collab middles** | .008 ▲▲, .005 (violence) ▲, .006 | .004 ●▲, .009 ▲, .005 (bribery) | .005 (blackmail) ▲, .007 ▲ (infiltration), .009 | .008 ▲, .006, .005 (violence) |
| **.010 where the arrest happens** | the stacks | a cargo hulk | the clinic's back rooms | a barracks ship (martial −10) |
| **.012 Retaliation** | arson and a named victim; fall-back-to-the-depots option → .071 ● | "your guard was bought": back to .003 at leverage +15 | they publish client files → L8 ● | open fighting on the drill floor; "Pay their next contract elsewhere." → .073 ● |
| **.013 custody kind option** | – | "Hand [kp] to the syndicate." → L15 ● | "Seize the clinic and its records." → L17 ● | – |
| **War support (.030/.031/.032)** | small levies | gold for mercenaries (`add_gold`, scaled) | the liege's allies are leaned on (weak hooks on 1–2 of the liege's vassals) | large levies (`spawn_army`); .034 Turned Guns can fire ● |
| **.033 The War Below** | raids on the enemy's stores | buys an enemy officer | a councillor's file | the crew wants a raise |
| **Exclusive leaves** | L12 The Region Falls | L15 The Syndicate Settles It | L17 The Clinic Changes Hands | .034 Turned Guns → L6; .012 contract buy-out → L14 |
| **Drift** | +2 (the streets wear on a boss) | +0 | +0 | +0 (contract discipline) |
| **Arrest roll** | ±0 | ±0 | ±0 | martial −10 (they fight back as a unit) |
| **Leaf odds** | L9 Break ▲, L12 ▲ | L3 Network ▲, L14 Arrangement ▲ | L8 Turns ▲ (exposure), L3 ▲ | L7 Spiral ▲, L9 ▲, L6 ▲ (turned guns) |
| **L16 aftermath** | streets restless (county control −) | an unclaimed cargo (gold) | the clinic closes | idle guns (levy +) |

| | violence | bribery | blackmail | infiltration |
|---|---|---|---|---|
| .005 The Errand variant | "someone who crossed me": a named courtier dies or is warned | "a cargo, waved through" | "a file on [target]": root gains a weak hook on a named vassal or the liege | "seat my person at your court": a lieutenant joins your court |
| Arrest modifier | ±0 | ±0 | ±0 | −10 until the informant is unmasked |
| .012 resolution | harm and seizure | the bought guard | exposure | they knew you were coming (+refusal) |

| | purge | grandeur | forecast | cold |
|---|---|---|---|---|
| .002 audience desc | names a lieutenant [kp.GetSheHe] had killed: "It had me reaching for [lieutenant] a day before I knew I'd stopped trusting [lieutenant.GetHerHim]. It's been right about me every time." | arrives with an entourage, sits before being asked | starts to rise before [kp.GetSheHe] has decided to, sits again, and apologizes for the habit | looks at the floor when spoken to |
| .006 The Episode | "It has me going for [target]. Give [target.GetHerHim] to me, or it will be me who does it." | "a seat at your table, in public" | "Every time it runs me forward, I end up on the other side of you. I wanted you to hear that from me." | "the itemized cost of your patience" |
| .072 The Hold Closes | "or I start with yours" | "kneel where they can see it" | "It already has me shaking your hand. It is usually right about me." | "your options, priced" |
| Ending lean | L9 ▲, L8 ▲ | L4 ▲ (rewards ×1.5) | L8 softened | L9 ▼, wars ▲ |

**Pacing check on variety:** 4 kinds × 4 methods (12 non-zero combinations) × 2 reaches × 4 minds = **96 profiles**. .001, .002, .003, .010, .012 and the leaves each assemble their desc from **two or three independent per-axis fragments** (§7.1), so the same event reads differently along every axis it touches. No desc is one generic text with a name swapped in.

### 5.3 Entry and the on_action

New file `common/on_action/eotg_aug_kingpin_on_actions.txt`:

```
yearly_playable_pulse = { on_actions = { eotg_on_yearly_aug_kingpin_check } }   # additive (invariant 4)

eotg_on_yearly_aug_kingpin_check = {
    trigger = {
        eotg_is_unclaimed_folk = no
        eotg_aug_kp_can_start = yes          # §5.1.1 eligibility, no story, no had-flag
        NOT = { has_character_flag = eotg_flag_aug_kingpin_cooldown }
    }
    effect = {
        random_list = {
            2 = {                             # fire (owner ruling Q3, 2026-10-06: 2%, was 4%)
                modifier = { factor = 2     eotg_aug_has_patron = yes }
                modifier = { factor = 1.5   eotg_is_augmented_any = yes }
                modifier = { factor = 1.5   eotg_aug_under_policy = { LAW = ban } }
                modifier = { factor = 1.5   has_character_modifier = eotg_mod_illegal_implants }
                modifier = { factor = 1.25  OR = { any_courtier = { eotg_is_augmented_any = yes } any_vassal = { eotg_is_augmented_any = yes } } }
                modifier = { factor = 0.25  is_ai = yes }
                add_character_flag = { flag = eotg_flag_aug_kingpin_cooldown  years = 10 }
                trigger_event = { id = eotg_aug_kingpin.001  days = { 1 30 } }
            }
            98 = { }                          # nothing
        }
    }
}
```

- **Cooldown authority is here only** (invariant 4, lesson 5). `.001`'s `trigger` mirrors world state (`eotg_aug_kp_can_start = yes`) and reads no flag. The 10-year cooldown matters only if a story ends before `on_setup` sets the once-per-life flag (a cold cancel). It is also the AI pacing floor.
- **Expected frequency (owner ruling Q3, 2026-10-06):** base 2% a year, so a player with no multipliers sees it about once in 50 years. With all the multipliers (Patron, augmented, Ban, illegal implants, augmented court: ×12.7, about 24% a year) about once in 4–5 years, but the once-per-life flag and the 10-year cooldown cap it. Typical play lands at about once or twice per campaign. AI ×0.25.
- **Story creation:** `.001` `immediate` runs `eotg_aug_kp_start_effect`. It creates the kingpin, rolls the profile (§5.2), and runs `create_story = eotg_story_aug_kingpin` with the kingpin passed through `root.var:eotg_kp_passthrough` (Patron envoy pattern, `eotg_augmentation_stories.txt` patron `on_setup`). `on_setup` copies it into `var:eotg_kp`, removes the passthrough, and sets `eotg_flag_aug_had_kingpin`.

**Edit E1 (existing file, one line):** add `NOT = { has_character_flag = eotg_flag_aug_kingpin }` to the `trigger` of `eotg_on_yearly_aug_nonruler_check` (`common/on_action/eotg_augmentation_on_actions.txt:1505`). This is needed only while the kingpin is root's courtier in the claim stages. No other existing file changes, apart from the template append (§3).

### 5.4 Story cycle `eotg_story_aug_kingpin`

New file `common/story_cycles/eotg_aug_kingpin_story.txt`. Shape: the Patron story (`eotg_augmentation_stories.txt`), plus a monthly maintenance group (vanilla `common/story_cycles/fp3_story_cycle_zanj_rebellion.txt:17-31`, `days = 1` maintenance group). Invisible (vanilla default; no counters).

| Story variable | Type | Meaning |
|---|---|---|
| `eotg_kp` | character | the kingpin |
| `eotg_kp_stage` | flag | `flag:open` (met or ignored, nothing agreed), `flag:collab`, `flag:custody`, `flag:pending` (faction raised, no war), `flag:war`, `flag:kept` |
| `eotg_kp_path` | flag | `flag:own` / `flag:back_kp` (vassal), `flag:neighbour` / `flag:vassal_seat` (independent); unset outside the claim path |
| `eotg_kp_leverage` | int 0–100 | §2. Start 20. Clamped. |
| `eotg_kp_refusals` | int | refusals since the last resolution; reset by .003 b-talk and by .036 |
| `eotg_kp_years` | int | ticks in `collab` or `kept` |
| `eotg_kp_war_years` | int | ticks in `war` |
| `eotg_kp_calmed` | int | calm options since the last tick (drift relief, §2) |
| `eotg_kp_target` | landed title | the claimed title |
| `eotg_kp_opponent` | character | who the war is against (the old liege, the neighbour, or the faction leader) |
| `eotg_kp_rival` | character | .031/.032's named rival (the neighbour or the vassal) |
| `eotg_kp_informant` | character | infiltration's planted courtier |
| `eotg_kp_playing` | bare | .002.c: root played along. Read: arrest +15, .009 better terms. |
| `eotg_kp_forewarned` | bare | .006 forecast c. Read: L8 costs halved. |
| `eotg_kp_evidence` | int | .004.b and .009.a; each point is +10 on arrest and audit rolls (max +30) |
| `eotg_kp_spiral_done` | bare | one-shot guard for .066 |
| `eotg_kp_leverage_band` | int 1–3 | the visible band (§5.4.2); written only by `eotg_aug_kp_leverage_effect` |
| `eotg_kp_inherited` | bare | set in `on_owner_death`; .040 reads it |
| `eotg_kp_resolving` | bare | set by every leaf and .036; blocks inheritance |

**`on_end`:** remove `eotg_flag_aug_kingpin` from a living kingpin. If the kingpin is alive, unlanded, not imprisoned, and not root's or the liege's courtier by a leaf's choice, `move_to_pool = yes` (Patron `on_end` precedent). Remove `eotg_mod_aug_kp_arrangement` and `eotg_mod_aug_kp_kept` from the owner if held. The crisis **county** modifier keeps its timer.

**`on_owner_death` (owner ruling Q2, 2026-10-06): the story passes to the heir.** Vanilla shape, `common/story_cycles/ce1_story_cycle_black_death.txt:18-30`:

```
on_owner_death = {
    if = {
        limit = {
            exists = story_owner.player_heir
            exists = var:eotg_kp
            var:eotg_kp = { is_alive = yes }
            NOT = { exists = var:eotg_kp_resolving }
            NOT = { story_owner.player_heir = var:eotg_kp }
        }
        eotg_aug_kp_inherit_effect = yes        # carry-over table below, run before the hand-off
        make_story_owner = story_owner.player_heir
        story_owner = { trigger_event = { id = eotg_aug_kingpin.040  days = { 3 10 } } }
    }
    else = { end_story = yes }
}
```

The scripter confirms whether `story_owner` already points to the heir after `make_story_owner` (vanilla stops there, so it never needed to know). If it does not, the heir is saved as `scope:eotg_kp_heir` before the hand-off and the event is fired on that (V-K8).

#### 5.4.1 What carries over to the heir

| Thing | Carries? | Rule |
|---|---|---|
| The kingpin, the profile, the organization's name | yes | They are on the kingpin. |
| `eotg_kp_leverage` | yes, **−10** (floor 0) | The debt is the house's, but a new face buys a little room. The band is recomputed through `eotg_aug_kp_leverage_effect`. |
| `eotg_kp_evidence`, `eotg_kp_years`, `eotg_kp_informant` | yes | Records, history and a planted courtier don't die with the ruler. |
| `eotg_kp_refusals`, `eotg_kp_calmed`, `eotg_kp_playing`, `eotg_kp_forewarned` | **reset** | Personal: they belonged to the dead ruler. |
| stage `open`, `collab` | yes | |
| stage `custody` | yes | Vanilla passes prisoners to the heir. If the kingpin was freed by the succession, M2-style check: stage becomes `open`. |
| stage `kept` | yes | The crisis outlives the ruler. The heir gets `eotg_mod_aug_kp_kept`, and the kingpin `add_hook = { type = strong_blackmail_hook  target = <heir> }` (the files outlive the ruler; hooks don't transfer by themselves). |
| stage `pending` | **reset to `collab`** | The faction was the dead ruler's. Unset `eotg_kp_path` and `eotg_kp_target`; vanilla handles the faction itself. |
| stage `war`, path `own` | **reset to `collab`** | The claimant died, so vanilla `claimant_faction_war` invalidates (`should_invalidate`: the special character must be alive). Unset the path. M3 never resolves it, so no false loss. |
| stage `war`, other paths | yes | The kingpin is the claimant and still alive. The war follows **vanilla war inheritance**; the story keeps `eotg_kp_opponent`, and M3 resolves whenever the heir is no longer at war with the opponent (won, lost, or not inherited at all, which M3 treats as lost: .065). V-K8 confirms what vanilla does with a faction war whose leader dies. |
| `eotg_mod_aug_kp_arrangement`, `_hired_guns`, `_informants` (character modifiers on the dead) | re-applied to the heir with the remaining years only if the stage is `collab` or `kept` | Modifiers die with the character. |
| County modifiers | stay | They are on the counties, which pass to the heir anyway. |
| `eotg_flag_aug_had_kingpin` | set on the heir | An inherited story is the heir's one per life. |

**.040 The Inheritance** (notification on the heir; signature: desc reads the band). Desc: a base line, then one fragment by stage (`.desc_open` / `_collab` / `_custody` / `_kept` / `_war`) and one band line. Example beat: "[kp.GetFirstName] sends no condolences. [kp.GetSheHe|U] sends the ledger." One option, **a** "Then [kp.GetFirstName] deals with me now." plus, only in `collab` or `kept`, **b** "Send word: the arrangement stands." (leverage +5, kp −3, calmed +1) and **c** "Send word: it ended with the funeral." (refusals +1, kp +5). Shape: vanilla inheritance notifications are one-option (`events/story_cycles/` "inherited" letters); the two extra options follow index §1 rule 6 (outcome stages may have one or two options) only where the stage gives the heir something to decide.

#### 5.4.2 Visible story (owner ruling Q6, 2026-10-06)

Index §1 rule 3 makes story cycles invisible **to hide fracture risk**. This story is the one exception, by owner ruling, because what it shows is leverage, not risk. The amendment is recorded in the index (`cybernetics_v2.md` §1 rule 3). Shape: `common/story_cycles/_story_cycles.info` (`visible`, `icon`, `background`, `visualization`), with the precedents `bp2_story_cycle_foreign_raised_reformer.txt:3-33` (`custom_string_key` plus a 0–3 `basic_counter`) and `book_translation_story_cycle.txt:2-19`.

```
eotg_story_aug_kingpin = {
    visible = yes
    icon = { reference = "gfx/interface/icons/story_cycles/story_icon_palace_politics.dds" }   # vanilla; no art debt
    background = { reference = "gfx/interface/illustrations/event_scenes/alley.dds" }         # vanilla; see the note below
    visualization = {
        custom_string_key = "eotg_story_aug_kingpin_info"
        character = { variable_name = "eotg_kp"  label = "eotg_story_aug_kingpin_kp_label" }
        basic_counter = {
            variable_name = "eotg_kp_leverage_band"
            min = 1  max = 3
            label = "eotg_story_aug_kingpin_band_label"
            min_label = "eotg_story_aug_kingpin_band_min_label"   # "A favour owed"
            max_label = "eotg_story_aug_kingpin_band_max_label"   # "They own the room"
        }
    }
    ...
}
```

- **Bands, not numbers.** The counter reads `eotg_kp_leverage_band` (1–3), never `eotg_kp_leverage`. `eotg_aug_kp_leverage_effect` changes and clamps leverage, then writes the band: 1 if ≤ 40, 2 if 41–79, 3 if ≥ 80. Nothing else writes the band.
- **The band's name** comes from the custom loc `eotg_aug_kp_cl_leverage_band` (`type = all`, triggers `var:eotg_kp_leverage_band = 1/2/3`; vanilla `Story.Custom` precedent: `00_pet_custom_loc.txt:1917` `CatStoryNameAll`, used as `[Story.Custom('CatStoryNameAll')]` in `story_cycles_l_english.yml:16`).
- **`eotg_story_aug_kingpin_info`** (the custom string, `Story` scope) names the organization, the band, and what moves it, in plain words with no numbers: "[Story.Custom('eotg_aug_kp_cl_leverage_band')]. Taking their money, doing their errands and keeping their secrets deepen it. Refusing them, turning their people and gathering evidence loosen it." The organization's name is on the kingpin, so the string uses `[Story.MakeScope.Var('eotg_kp').Char.GetFirstName]` (vanilla form, `story_cycles_l_english.yml:70`) and a fixed noun, not the seller custom loc (that runs on a character).
- **Not shown:** the kingpin's fracture risk, the stage, the path, any count.
- **Background note:** if the mod reskins vanilla event scenes for space, the scripter swaps `alley.dds` for the mod's equivalent; otherwise the vanilla file stands. No new art.

### 5.5 The tick (cooldown authority for every chain stage)

**Maintenance group, `months = 1`, first_valid** (watchers; they fire nothing on a normal month):

| # | Trigger | Effect |
|---|---|---|
| M0 | the kingpin's employer exists and is not root, while the stage is `open`, `collab` or `kept` (§5.1.2 V-K1) | toast `eotg_aug_kingpin_toast_gone`, `end_story` |
| M1 | the owner is not landed, or is imprisoned by anyone but the kingpin's side | `end_story` (silent) |
| M2 | the kingpin is dead and the stage is not `war` (any death not made by this story's own leaves, which end the story themselves) | toast `eotg_aug_kingpin_toast_dead` (reads nothing; it is not an event), `end_story` |
| M3 | stage `war` and `NOT = { story_owner = { is_at_war_with = var:eotg_kp_opponent } }` | resolve (table below), then the leaf event in 1–5 days |
| M4 | stage `war`, `var:eotg_kp_war_years >= 3` **or** (the kingpin is in Storm **and** mind purge), and no `eotg_kp_spiral_done` | set `eotg_kp_spiral_done`; fire .066 |

**M3 war resolution:**

| path | `eotg_kp_target.holder` | Leaf |
|---|---|---|
| `back_kp` | = the kingpin | .063 Kingmaker (vassal variant) |
| `own` | = the owner | .036 The Partner's Price |
| `neighbour` | = the kingpin | .063 Kingmaker (independent variant) |
| `vassal_seat` | the owner still holds their primary title **and** the kingpin still holds the seat | .069 A Seat Under You ("kept by force" desc) |
| `vassal_seat` | otherwise | .066 Every Level Burning (`eotg_kp_spiral_done` ignored) |
| any other case (lost, white peace, invalidated because the claimant died) | | .065 Sold to the Winner, or the toast and `end_story` if the kingpin is dead |

**Yearly tick, `years = 1`, first_valid, in this order:**

0. **Always first (a non-exclusive `effect` before the first_valid):**
   - drift: `var:eotg_kp = { eotg_add_fracture_risk = { AMOUNT = eotg_aug_kp_drift_value } }`, then reset `eotg_kp_calmed`;
   - `eotg_kp_years` +1 in `collab` or `kept`; `eotg_kp_war_years` +1 in `war`.

| # | Trigger | Fires | Notes |
|---|---|---|---|
| T1 | the kingpin's `eotg_fracture_risk >= 95` | `random_list`: .068 The Break, weight 40 (×1.5 purge, ×1.5 crew or hired, ×0.5 cold); .075 The Fracture Finishes It, weight 60 | In any stage except `custody`. In `war`, .068's war variant is used. |
| T2 | stage `collab` or `open`, leverage ≥ 80, kingpin Fracture or Storm | .072 The Hold Closes | the crisis gate |
| T3 | stage `collab`, refusals ≥ 2 | `random = { chance = 50` (×1.25 purge, ×1.25 grandeur) `}` → .067 The Turn | |
| T4 | stage `collab`, `eotg_kp_years >= 6` | leverage ≤ 40 and (kind syndicate or front, or the kingpin in Storm): .062 The Trade Is Yours (a cascade death ends the deal); leverage ≤ 40 otherwise: .073; leverage 41–79: .073 A Standing Arrangement | the natural end of a long deal |
| T5 | stage `open` | `random = { chance = 60 }` → .014 Bodies on the Docks | neglect escalates |
| T6 | stage `collab` | middle pool (§5.7) | |
| T7 | stage `kept` | `random = { chance = 70 }` → .050 The Orders; if leverage < 40, .073 instead (you have bought your way to a truce) | |
| T8 | stage `war` | `random_list`: .033 The War Below 60; .034 Turned Guns 25 (`hired` only, and leverage < 30 or mind purge); nothing 40 | |
| T9 | stage `pending` | .038 Now or Never | |

### 5.6 Script values (`common/script_values/eotg_aug_kingpin_values.txt`)

| Value | Formula |
|---|---|
| `eotg_aug_kp_drift_value` | 6; +4 if mind purge; −2 if mind cold; +2 if kind crew; +6 if stage war; − 4 × `eotg_kp_calmed`; min 2. Run in story scope, reading `var:eotg_kp.var:…`. |
| `eotg_aug_kp_arrest_value` | the bonus for .010/.011 rolls: + 10 × `eotg_kp_evidence` (max 30); +15 `eotg_kp_playing`; +20 the audience arrest (.002.b); −10 reach wide; −10 method infiltration with the informant not unmasked; −10 kind hired (martial only) |
| `eotg_aug_kp_levies_value` | `spawn_army` levies for the kind: crew 0.1, hired 0.35, others 0 × root's `max_military_strength` (V-K4: confirm that the value exists as a script value, else use `realm_size` × a constant); ×1.5 reach wide; +1 step for mind cold |

### 5.7 The middle pool (T6), and the AI

```
random_list = {
    20 = { trigger = { kind syndicate OR method bribery }   modifier = { factor = 2 kind syndicate }   → .004 }
    25 = { → .005 (the errand variant comes from method) }
    25 = { → .006 (the variant comes from mind)   modifier = { factor = 1.5  the kingpin in Fracture or Storm } }
    20 = { trigger = { method infiltration  NOT = { exists = var:eotg_kp_informant_unmasked } } → .007 }
    20 = { trigger = { kind crew OR kind hired OR method violence }   modifier = { factor = 2  method violence } → .008 }
    10 = { modifier = { factor = 2  reach wide } → .009 }
    30 = { modifier = { factor = 3  is_ai = yes } }           # nothing
}
```

- **At most one story event a year** from the yearly tick. Maintenance fires only the war-end resolution and the spiral, both one-shot.
- **AI owners:** the AI ×3 nothing-weight in T6 and T8. Every option has `ai_chance` (index §1 rule 6): base 30 by default, a refusal or no-op as low as 10, the option an offer exists to sell up to 40, and at least two trait modifiers each. **Claim options:** base 5, `add = 15` ambitious, `add = 10` (deceitful or arrogant), `factor = 0` if `is_at_war = yes`, `factor = 0.25` if the target title's tier is above root's highest tier + 1 (a count does not usually try for an empire).
- **AI vassal, player liege:** when an AI owner's claim path starts its war (.030 a or .038 a) against a **player** opponent, `.039 Word From the Docks` fires on the opponent (`is_ai = no`). It is a notification that reads the kingpin's band. This is the only player-visible face of an AI's story.

### 5.8 The tree

Delays are in days unless marked. "→" is `trigger_event` on root, unless a stage change hands control to the tick ("tick"). Every option has an `ai_chance` per §5.7; the column lists base and modifiers only where they deviate from base 30 with two trait modifiers.

```
                              yearly_playable_pulse
                                       |
                    eotg_on_yearly_aug_kingpin_check (2%, cooldown here)
                                       |
                              .001 Word From Below ─────────────────────────────┐
           ┌─────────────┬────────────┼─────────────────┬──────────────────────┐ │
        a meet       b arrest     c leave it   d [Patron] envoy   e [front] audit │
           |             |            | (open)          |               |       │
     .002 Audience     .010        tick T5 →.014       L15 .074       .015 Audit  │
     /    |     \     Arrest        a→.010 b→.002        ┌──────────────┘   │     │
  a hear b guards c play                c ignore again    success→.013  fail→.012  │
    |      → .010   (playing)            (Storm crew: .071)                       │
  .003 The Offer <──────────────────────────────────────── .012 b "Negotiate" ────┘
   ├ a collaborate ──────────────► stage collab ─ tick T6 ─► .004 .005 .006 .007 .008 .009
   ├ e kind offer ───────────────► stage collab (variant)          │        │
   ├ d refuse ──► .012 Retaliation (kind)                           T2 ► .072 The Hold Closes
   ├ b [vassal] own claim ─┐                                        │       ├ a submit → stage kept ─ T7 ► .050 Orders
   ├ c [vassal] back kp ───┴► .030 The Claim                        │       │      (exit: L9/L16 at T1, L14 at leverage<40)
   ├ b'[indep] neighbour ───► .031 The Neighbour's Seat             │       ├ b resist → .068 L9 / .067 L8
   └ c'[indep] vassal seat ─► .032 The Vassal's Seat                │       └ c [NF root] → kept (+root risk)
                                                                    T3 ► .067 L8   T4 ► .062 L3 / .073 L14
 .030 / .031 / .032 ── a strike → stage war ─ T8 ► .033 / .034 ; M4 ► .066 L7
                    └─ b wait → stage pending ─ T9 ► .038 Now or Never ─ a strike / b disband (→collab)
                    └─ c walk away → refusals+1, leverage+20 (→ collab)
 war ends (M3) ─► back_kp/neighbour won: .063 L4 · own won: .036 The Partner's Price ─ a→.069 L10, b→.070 L11, c roll→.064 L5 / .067 L8, d→.067 L8
              └─► vassal_seat held: .069 L10 · lost / white peace: .065 L6 · vassal_seat lost: .066 L7
 .010 Arrest ─ success → .013 In Custody ─ a .060 L1 · b .061 L2 · c .070 L11 · d .069 L10 · e[front] .076 L17 · f[syndicate] .074 L15
            └ failure → .012 Retaliation ─ a fight → .011 Crackdown (success → .013; failure → .068 L9 in Storm, else .073 L14)
                                         ├ b negotiate → .003 (leverage +15)
                                         ├ c [crew] fall back to the depots → .071 L12
                                         ├ c‴[hired] buy out the contract → .073 L14
                                         ├ c'[front] let them publish → .067 L8
                                         └ c''[syndicate] pay the guard's price → stage open
 T1 (pressure ≥ 95) ─► .068 The Break L9  or  .075 The Fracture Finishes It L16
```

#### Node table

| Event | Title (working) | Fired by | Options → next (delay) | Signature |
|---|---|---|---|---|
| **.001** | Word From Below | on_action | **a** "Bring [kp] to me. Quietly." → .002 (5–15). ai 40, +ambitious, +greedy, −just. **b** "Arrest [kp] before the next shift." → .010 (3–10). +just, +wrathful, −craven. **c** "A quarrel in the underlevels. Leave it." stage `open`, kp +5. ai 20, +lazy, +content. **d** [Patron and envoy present; kind syndicate] "Ask the envoy to deal with [kp]." → .074 (10–30); Patron demand +1. **e** [front] "Audit [company]'s client records." → .015 (10–20). **f** [crew] "Pay them to keep their boss quiet." `remove_short_term_gold = minor_gold_value`, leverage +15, stage `collab`, kp −3, `eotg_kp_calmed` +1. **f′** [hired] "Buy out their next contract." `remove_short_term_gold = medium_gold_value`, root `eotg_mod_aug_kp_hired_guns` 5 years, leverage +10, stage `collab`, kp −3, calmed +1. | desc reads band (opening line by band); c and f move it |
| **.002** | The Audience | .001 a, .014 b | **a** "Say what you came to say." → .003 (1). **b** "Guards. Now." → .010 (1); `add_prestige = -minor_prestige_value`. The text frames it as root breaking his own word in front of his own court (he granted the audience); the loss stays small; the arrest value +20. +wrathful, +paranoid. **c** [deceitful or schemer] "Smile. Agree. Remember all of it." → .003 (1); sets `eotg_kp_playing`. **d** [root `eotg_neurofractured`] "Does yours run ahead of you too?" → .003 (1); kp −5, root `eotg_add_fracture_risk = 5`, leverage −10. | desc by mind and band; d moves both |
| **.003** | The Offer | .002, .012 b | **a** "We can work together." stage `collab`; leverage +10; mutual `major_crime_accomplice_hook` (each on the other); kp −5, calmed +1. ai 30, +greedy, +ambitious, −just, −honest. **b** [vassal; `eotg_aug_kp_liege_claim_possible`] "Put me in [liege]'s seat." `path = own` → .030 (5–10); leverage +20, except +0 when the method is blackmail ("they forge it from their files"). **c** [vassal; same] "Take the seat yourself. I'll hold the door." `path = back_kp` → .030 (5–10); leverage +10. **b′** [independent; `eotg_aug_kp_neighbour_target`] "Take [rival]'s seat. My guns, your name." → .031 (5–10). **c′** [independent; `eotg_aug_kp_vassal_seat_target`] "[rival]'s seat could be yours." → .032 (5–10). **d** "No. Get out." refusals +1; kp +5; `random_list` 70 (crew or hired) / 40 (others): → .012 (30–90), else stage `open`. ai 30, +just, +brave. **e (kind):** crew "Keep the stacks quiet, and we talk again." (collab, leverage +5, kp −3); syndicate (or bribery) "Take your cut and look away." (collab, `add_gold = minor_gold_value`, `eotg_mod_aug_kp_arrangement`, leverage +15); front [vassal] "Your files on [liege]. Now." (collab, root `add_hook = { type = weak_blackmail_hook target = liege }`, leverage +20); hired "I'll keep your guns on retainer." (collab, `eotg_mod_aug_kp_hired_guns` 5 years, leverage +10). Max 5 visible. | every option moves kp except b/c (desc reads band) |
| **.004** | The Ledger | T6 (syndicate or bribery) | **a** "Take it." `add_gold = medium_gold_value` (wide: major), leverage +10, kp −3, calmed +1. **b** "Take half. Log every credit." `add_gold = minor_gold_value`, leverage +5, evidence +1. +diligent, +just. **c** "Send it back." refusals +1, kp +5. **d** [greedy] "Ask what the other half buys." gold medium ×1.5, leverage +15. | moves |
| **.005** | The Errand | T6 | Variant by method (desc and options). **violence:** a named target (`eotg_aug_kp_errand_target`, a chosen target per index rule 7: an adult courtier who is not root's close family or spouse) — **a** "Look away." The target dies (`death_murder`, killer the kingpin, 10–30 days later); leverage +15; kp −5; `eotg_aug_stress_murder_effect`. **b** "Warn [target]." refusals +1; target +20 opinion (vanilla `grateful_opinion` or `eotg_opinion_aug_kp_warned`); kp +5. **c** "Arrest the ones sent to do it." → .010 (5); refusals +1. **blackmail:** a file on a named target (the liege for a vassal; else the vassal with the most powerful realm) — **a** "Keep the file." root `add_hook = { type = weak_blackmail_hook target = … }`, leverage +10. **b** "Burn it." refusals +1, kp +5. **c** "Use it on [kp] instead." intrigue duel vs the kingpin: success leverage −15, evidence +1; failure leverage +10, kp +5. **infiltration:** **a** "Give them a post." A lieutenant (template) joins root's court as `eotg_kp_informant`; leverage +15. **b** "No posts for them." refusals +1, kp +5. **c** [paranoid or schemer] "Give them a post. Watch them." as a, plus `eotg_kp_informant_unmasked`, leverage +5. **bribery:** **a** "Wave it through." gold minor, leverage +10. **b** "Inspect the cargo." refusals +1, `stress_impact = { just = minor_stress_impact_loss  honest = minor_stress_impact_loss }`, kp +5. **c** [just] "Seize it." gold minor, refusals +1, kp +10. | moves |
| **.006** | The Episode | T6 | Variant by mind. **purge:** the implant has the kingpin going for one of yours (a chosen target, `eotg_aug_kp_purge_target`), and the kingpin asks for the target before doing it himself: **a** "Take [target], then." `imprison_character_effect` on the target with root as imprisoner, tyranny per vanilla, leverage +10, kp −10, `eotg_aug_stress_cruelty_effect`. **b** "No one of mine." refusals +1, kp +10. **c** "Sit down. Talk me through it." diplomacy vs `medium_skill_rating`: kp −10, calmed +1 / kp +5. **grandeur:** **a** "A seat at my table, then." `add_prestige = -minor_prestige_value`, leverage +10, kp −10. **b** "No." kp +10. **c** [arrogant] "Mock the request in front of the court." dread +5, kp +15, refusals +1. **forecast:** **a** "Thank you for the warning." kp +5. **b** "My physician will see you." `remove_short_term_gold = minor_gold_value`, kp −15 (−20 with `eotg_has_physician_access`), calmed +1. **c** "Then I'll plan for it." sets `eotg_kp_forewarned`, kp +5. **cold:** **a** "Pay the itemized cost." gold minor, leverage +5, kp −5. **b** [callous] "Send back an invoice of my own." dread +10, kp −5. **c** "No." kp +5. | moves |
| **.007** | The Informant | T6 (infiltration) | The informant is the planted lieutenant if one exists, else a chosen courtier (`eotg_aug_kp_informant_candidate`). **a** "Arrest [informant]." imprison; leverage −15; sets `eotg_kp_informant_unmasked`; kp +5. **b** "Turn [informant]." intrigue duel vs the informant: success leverage −20, evidence +1, unmasked; failure leverage +10, kp +5. **c** "Let [informant] be." leverage +5, kp −3. | moves |
| **.008** | The Protection Bill | T6 (crew, hired, or violence) | **a** "Pay it." `remove_short_term_gold = minor_gold_value` (wide: medium); leverage +10; kp −3, calmed +1. **b** "Not one credit." refusals +1; capital `add_county_modifier = { modifier = eotg_mod_aug_kp_arson years = 2 }`; kp +5. **c** [brave or wrathful] "Send the guard into the stacks." → .011 (5–10). | moves |
| **.009** | The Lieutenant | T6, or T5 at 20% | A lieutenant (`eotg_aug_kp_lieutenant_template`, saved `eotg_kp_lieutenant`) offers the kingpin. **a** "Tell me everything." evidence +2; → .010 (10–20). **b** "Warn [kp]." leverage −10; the lieutenant dies 10–20 days later (`death_murder`, killer the kingpin); kp −5; `eotg_aug_stress_cruelty_effect`. **c** "I never heard this." The lieutenant leaves (`death_disappearance` if root is purge-known, else pool); kp +5. | moves |
| **.010** | The Arrest | .001 b, .002 b, .005 c, .009 a, .014 a | Desc by kind (where) and band. **a** "Take [kp] alive." `duel = { skill = martial target = scope:eotg_kp … }` with `eotg_aug_kp_arrest_value` → success: `imprison_character_effect`, stage `custody`, → .013 (1); failure: → .012 (5–15), kp +10. **b** "Quietly, while [kp.GetSheHe] sleeps." intrigue duel, the same branches. **c** "Call it off." refusals +1, kp +5, stage `open`. | moves |
| **.011** | The Crackdown | .008 c, .012 a | **a** "Every level. Every door." `remove_short_term_gold = medium_gold_value`, dread +10, martial vs `high_skill_rating` + the arrest value: success → .013; failure → .068 if kp Storm, else .073 (exhausted truce). **b** "Lock the underlevels down." capital `eotg_mod_aug_kp_lockdown` 2 years (control growth +, development growth −), kp +5, stage `open`. **c** "Stand the guard down." refusals +1, kp +5. | moves |
| **.012** | Retaliation | .003 d, .010 failure, .015 failure | Desc by kind (§5.2.4). **a** "Fight for every level." → .011 (5). **b** "Talk." → .003 (5); leverage +15; refusals reset. **c** [crew; `eotg_aug_kp_seizable_county`] "Let them fall back to [county]." → .071 (5). **c‴** [hired] "Pay their next contract elsewhere." `remove_short_term_gold = medium_gold_value`, kp −3 → .073 (5) (contract desc variant). **c′** [front] "Let them publish." → .067 (5). **c″** [syndicate] "Pay what my guards were paid." `remove_short_term_gold = medium_gold_value`, leverage −5, stage `open`. Crew and hired, before the options: in `immediate`, 50% a picked victim (`eotg_aug_pick_victim_effect`, wounded) named in desc. | desc reads band; a/b/c route; c″ and the victim move kp (+5) |
| **.013** | In Custody | .010 or .011 success, .015 success | The kingpin is root's prisoner. **a** "Execute [kp]. Now." → .060 (1). ai +wrathful, +impatient. **b** "A public trial, then every level cleared." `remove_short_term_gold = medium_gold_value` → .061 (30–60). +just, +diligent. **c** "More use alive. Inside my court." → .070 (1). +schemer, +ambitious. **d** [`eotg_aug_kp_seizable_county`] "Give [kp] a Region to keep quiet." → .069 (1). **e** [front] "Seize the clinic and its records." → .076 (1). **f** [syndicate] "Hand [kp] to the syndicate." → .074 (5–15). Max 5 visible (d, e and f are mutually exclusive by kind except d). | desc reads band (the cell readings line) |
| **.014** | Bodies on the Docks | T5 | **a** "Now we act." → .010 (3–10). **b** "Bring [kp] in." → .002 (5–15). **c** "Not my quarrel." kp +8; if kind crew **and** kp Storm **and** `eotg_aug_kp_seizable_county`: 30% → .071 (30–60). | moves |
| **.015** | The Audit | .001 e | **a** "Audit everything." stewardship vs the kingpin's intrigue, + 10 × evidence: success → imprison, stage `custody`, → .013 (5); failure → .012 (10–20), kp +5. **b** "Buy the records quietly." `remove_short_term_gold = medium_gold_value`, leverage −10, evidence +2, stage `collab`. **c** "Leave the records sealed." kp +5, stage `open`. | moves |
| **.030** | The Claim | .003 b / c | `immediate`: save `eotg_kp_target = liege.primary_title`, `eotg_kp_opponent = liege`. Grant the claimant (root for `own`, the kingpin for `back_kp`) `add_pressed_claim = scope:eotg_kp_target`. For `back_kp`, `add_courtier = scope:eotg_kp` on root. Set `root.var:claiming_title = scope:eotg_kp_target` (vanilla needs it for `can_create_faction`, see below). **a** "Raise the faction. Strike now." `show_as_unavailable` unless `can_create_faction = { type = claimant_faction target = liege }`. Runs `eotg_aug_kp_raise_claimant_effect` (vanilla `00_vassal_interactions.txt:1548-1597`: `create_faction`, then `joined_faction = { set_special_character = <claimant>  set_special_title = scope:eotg_kp_target }`, the `claimant_factions` variable list, `remove_variable = claiming_title`), then `joined_faction = { faction_start_war = {} }` (vanilla `events/factions/faction_demands.txt:396`), then war support by kind (§5.2.4: `spawn_army` with `eotg_aug_kp_levies_value`, or `add_gold`, or weak hooks). Stage `war`; kp +5. Fires .039 on a player opponent. **b** "Gather support first." The same faction effect, without the war. Stage `pending`. **c** "Walk away from it." `remove_claim` on the granted claim; `remove_variable = claiming_title`; the kingpin back to the pool; refusals +1, leverage +20; stage `collab`. | moves |
| **.031** | The Neighbour's Seat | .003 b′ | `immediate`: save the rival (`eotg_aug_kp_neighbour_target`, the weakest neighbouring independent ruler with a primary title of tier ≥ county), `eotg_kp_target = rival.primary_title`, the opponent = the rival; `add_courtier = scope:eotg_kp`; kingpin `add_pressed_claim`. **a** "Declare it." `start_war = { cb = claim_cb  target = scope:eotg_kp_rival  claimant = scope:eotg_kp  target_title = scope:eotg_kp_target }` (V-K3: `claim_cb` with `claimant` and `target_title`; vanilla `00_claim.txt` reads `scope:claimant`), then war support by kind. Stage `war`; kp +5. **b** "Not yet." stage `collab`, leverage +10; the kingpin back to the pool. **c** "Walk away." remove the claim; refusals +1; leverage +20. | moves |
| **.032** | The Vassal's Seat | .003 c′ | The rival is the target vassal (`eotg_aug_kp_vassal_seat_target`: landed, not root's close family, primary title tier ≥ county and below root's tier). **a** "Revoke it by decree." Zanj precedent (`events/dlc/fp3/fp3_story_cycle_zanj_rebellion_events.txt:414-470`), with type `revoked`: the title goes to the kingpin through `create_title_and_vassal_change` and `change_title_holder`; `add_tyranny = 40`; the dispossessed gets −50 opinion (vanilla `revoked_title` opinion). Then the angriest remaining landed vassal (lowest opinion of root; may be the dispossessed if still landed) runs `create_faction = { type = liberty_faction target = root }` and `joined_faction = { faction_start_war = {} }`: chance 100 (method violence or kind hired), else 60. War → stage `war`, `path = vassal_seat`, the opponent = the faction leader. No war → .069 (5). kp +5. **b** "Buy [rival] out." `remove_short_term_gold = major_gold_value`; the same transfer without tyranny; the dispossessed +10 opinion (compensated); → .069 (5). **c** "Walk away." refusals +1. | moves |
| **.033** | The War Below | T8 | Variant by kind. **crew:** "raid their stores" — **a** "Let them." dread +10, kp +5. **b** "Keep them on the front." kp −3. **syndicate:** "an enemy officer for sale" — **a** "Buy." `remove_short_term_gold = medium_gold_value`; the opponent loses a random knight to the pool (V-K6), or −20 opinion of the opponent toward their marshal. **b** "No." kp +3. **front:** "a councillor's file" — **a** root `add_hook = { type = weak_blackmail_hook target = <opponent's councillor> }`, kp +3. **b** "Burn it." kp +3. **hired:** "the crew wants a raise" — **a** "Pay." `remove_short_term_gold = medium_gold_value`, leverage +5. **b** "Not mid-war." leverage −10, kp +5. Each variant also has **c** [the kingpin in Storm] "Keep [kp] away from the line." calmed +1, kp −5, levies −10% (no new army). | moves |
| **.034** | Turned Guns | T8 (hired) | The crew turns on you. **a** "Outbid the other side." `remove_short_term_gold = major_gold_value`, kp +5. **b** "Let them go." The opponent gets `spawn_army` with `eotg_aug_kp_levies_value`; the kingpin moves to the opponent's court (`add_courtier`); the claimant faction invalidates if the kingpin was the claimant (vanilla `should_invalidate`). **c** [brave] "Meet them at the hangar first." prowess duel vs the kingpin: success, the kingpin dies (`death_battle`) and the war goes on; failure, root `increase_wounds_effect` and b's effects. | moves |
| **.036** | The Partner's Price | M3 (`own` won) | root now holds the liege's title. **a** "A Region of your own." → .069 (1). **b** "A seat at my court." → .070 (1). **c** "Loose ends." intrigue duel vs the kingpin: success → .064 (1); failure → .067 (5–10). **d** "You've been paid enough." → .067 (10–30). | desc reads band |
| **.038** | Now or Never | T9 | **a** "Strike." `faction_start_war` + war support; stage `war`; kp +5. **b** "Disband it." destroy the faction; refusals +1, leverage +10; stage `collab`. Before the options: 20% the liege learns (`immediate`) → only option **c** "Then it's done." → .067. | moves |
| **.039** | Word From the Docks | .030 a, .038 a on a player opponent | Notification on the player liege. **a** "Noted." **b** "Put a bounty on [kp]." `remove_short_term_gold = minor_gold_value`; kp +5 (the hunt). | desc reads band; b moves |
| **.050** | The Orders | T7 (kept) | Variant by mind and method (four order types: a squeeze, a name, a march, a show). **a** "Do as [kp] says." tyranny +10 (or the squeeze's gold), dread +10, kp −5, leverage +5. **b** "Stall." kp +10, leverage −10. **c** "Not this one." refusals +1; if refusals ≥ 2 → .068 (Storm) or .067 (otherwise), 10–30 days. The four order types are acts root performs: the squeeze (gold), the name (an arrest root orders), the march (**a show of force root stages himself**, a parade of his own levies; never the kingpin's implant acting on root), the show (public honours). Root NF: **d** "Do what mine already has me doing." as a, plus root risk +5, leverage −5. | moves |

#### Leaf table (17 endings)

Every leaf ends the story (`random_owned_story = { limit = { story_type = eotg_story_aug_kingpin } end_story = yes }` in its options' `after`, or in `immediate` for single-option leaves) and reads the band in its desc.

| # | Event | Ending | Reachable from | Profile gate | Mechanics |
|---|---|---|---|---|---|
| **L1** | **.060** | **A Quick Ending.** The meagre ending: a short hearing, a shorter walk to the cells' end. Nobody sings about it. The text says "the order" and "the arrest": never a warrant, never hanging. | .013 a | — | `execute_prisoner_effect = { VICTIM = scope:eotg_kp  EXECUTIONER = root }` (vanilla `00_prison_effects.txt:413`; it computes the tyranny and opinion). `add_prestige = minor_prestige_value`; `add_dread = 5`. The capital gets `eotg_mod_aug_kp_loose_ends` for 2 years (control growth −; the organization splinters). One option "It's done." or [compassionate] "Give [kp.GetHerHim] proper rites." (piety minor, stress loss). |
| **L2** | **.061** | **The Streets Go Quiet.** Order restored: a trial under your own law, every level cleared. | .013 b | — | Gold already paid in .013 b. **a** "Execute [kp]." (vanilla effect as L1) or **b** "The cells, for life." (the kingpin stays imprisoned; flag removed). Both: `add_prestige = medium_prestige_value`; capital `eotg_mod_aug_kp_streets_cleared` 10 years; every vassal `add_opinion = { modifier = eotg_opinion_aug_kp_order target = root }` (+10, 10 years). |
| **L3** | **.062** | **The Trade Is Yours.** A long, quiet deal ends with the kingpin's cascade, and their business is now yours. Profitable and corrupting. | T4 | ▲ syndicate, front | The kingpin dies (`death = { death_reason = eotg_death_cascade }`). `add_gold = major_gold_value`. **a** "Keep it running." `eotg_mod_aug_kp_network` 20 years (domain tax +, vassal opinion −). **b** "Burn the ledgers." every vassal `eotg_opinion_aug_kp_order` (+10, 10 years), no modifier. **c** [greedy] "Expand it." the modifier + `add_tyranny = 15`; greedy stress loss. |
| **L4** | **.063** | **Kingmaker.** The kingpin won, and remembers friends. | M3 (`back_kp`, `neighbour`) | ▲ grandeur | **Vassal:** the kingpin now holds the old liege's title and is root's liege. Rewards: `add_gold = major_gold_value` (×1.5 grandeur); a non-capital county from the kingpin's demesne if one exists (`create_title_and_vassal_change = { type = granted }` → root), else a second gold major; the kingpin `add_opinion = { modifier = eotg_opinion_aug_kp_kingmaker target = root }` (+50, 20 years); mutual `major_crime_accomplice_hook`. **Purge mind:** 30% he pays half and keeps a `strong_blackmail_hook` on root instead of the mutual hook (desc variant). **Independent:** the kingpin is root's vassal holding the conquered title, with the same opinion and hook; `add_prestige = major_prestige_value`. From here the existing Neurofractured ruler content runs on the landed kingpin (`eotg_on_yearly_aug_neurofractured_check`): a Neurofractured liege, or a Neurofractured vassal, is the long tail. **Syndicate kind (lore review item 1, text only):** the boss acts for himself and breaks with the syndicate, which fits the fracture; no line implies the syndicate's head knows or cares, and none uses the Flesh Pledge, souls or "loyalty". |
| **L5** | **.064** | **Before the Bill Came.** You took the liege's seat and had your partner killed before the bill came. | .036 c success | — | The kingpin dies (`death_murder`, killer root); `add_secret = { type = secret_murder target = scope:eotg_kp }` (vanilla secret, V-K5); `add_dread = 10`; `add_gold = minor_gold_value` (seized funds). |
| **L6** | **.065** | **Sold to the Winner.** The war is lost, and the kingpin has sold you to the winner. Betrayal on a loss. | M3 (lost, white peace), .034 b → loss | ▲ hired | **Vassal:** the kingpin moves to the old liege's court (`add_courtier`); the liege `add_hook = { type = strong_blackmail_hook target = root }`; `remove_short_term_gold = medium_gold_value` (the kingpin's fee, taken); root `eotg_mod_aug_kp_exposed` 10 years. **Independent:** the kingpin moves to the rival's court; the rival `add_pressed_claim` on a random non-capital county of root's (none: gold medium instead). Vanilla's own war-loss effects (imprisonment, truce) apply first. |
| **L7** | **.066** | **Every Level Burning.** The civil war spirals: nobody wins, and the lower levels of both realms burn. | M4; M3 (`vassal_seat` lost) | ▲ hired, purge | **a** "End it. Any terms." `end_war = white_peace` on the war (V-K7: `random_character_war` with the opponent, `end_war`); the kingpin dies in the fighting (`death_battle`) at 50%. **b** "Burn it all down." `add_dread = 30`; `add_tyranny = 20`; the war continues; kp +10. Both: root's capital and the opponent's capital get `eotg_mod_aug_kp_burned_levels` 10 years. The story ends; vanilla resolves the war (a later M3 does not fire). |
| **L8** | **.067** | **The Turn.** (Retitled: "kingpin" never appears in a line a syndicate-kind story can show, §7.4.) Outside a war, the kingpin sells you. | T3; .003 refusal chain; .012 c′; .036 c fail / d; .038 c; .050 c; .072 b | ▲ front, purge, grandeur | **Vassal:** the liege `add_hook = { type = strong_blackmail_hook target = root }`; the liege `add_opinion = { eotg_opinion_aug_kp_conspired target = root }` (−30, 10 years); `eotg_mod_aug_kp_exposed` 10 years; the kingpin moves to the liege's court. **Independent ("causing a civil war"):** the kingpin arms your angriest vassal: `create_faction = { type = liberty_faction target = root }` and `faction_start_war` (crew, hired or violence), else the same with no war (it builds). **Front:** client files published, `add_prestige = -medium_prestige_value`. **Options:** **a** "Let it land." **b** "Pay [kp] to soften it." `remove_short_term_gold = major_gold_value`, halves the opinion hit and removes the exposed modifier. **c** [vengeful] "Hunt [kp] down." intrigue duel vs the kingpin: success, the kingpin dies (`death_murder`); either way dread +10. `eotg_kp_forewarned` halves every cost. |
| **L9** | **.068** | **The Break.** The kingpin's fracture breaks into a massacre in the lower levels, and at your court if the boss came up to the residence. | T1, .011 fail (Storm), .050 c, .072 b | ▲ crew, hired, purge; ▼ cold | `immediate`: 1–2 victims picked by `eotg_aug_pick_victim_effect` / `_second_` on root's court (index rule 7: the implant's violence, not the ruler's choice; FAMILY_FACTOR 0.25). Victims die `death_murder`, killer the kingpin. Capital `eotg_mod_aug_kp_massacre` 10 years. **a** "Hunt [kp] down. Now." martial duel: success, the kingpin dies (`death_battle`); failure, the kingpin is gone (`death_vanished`). **b** "Seal the lower levels and count the dead." `add_dread = 10`; the kingpin dies in the sealing (`death_vanished`). **c** [compassionate] "Go down there yourself." stress gain medium; the vassal opinion hit is halved. If stage `collab` or `kept`: every vassal `eotg_opinion_aug_kp_harboured` (−20, 10 years). War variant: also ends the faction (`destroy_faction`). |
| **L10** | **.069** | **A Seat Under You.** The kingpin becomes your landed vassal. | .013 d, .032 a/b, .036 a, M3 (`vassal_seat` held) | — | Grant a non-capital county from root's demesne (`eotg_aug_kp_seizable_county`, `create_title_and_vassal_change = { type = granted }`). In .032 they already hold the seat, so only the opinion lines run. Every vassal `eotg_opinion_aug_kp_raised_criminal` (−10, 10 years); the kingpin +30 opinion (vanilla `granted_title`); root keeps or gains `major_crime_accomplice_hook` on the kingpin. Released from prison if held. From here the existing Neurofractured ruler pipeline runs on them. Syndicate kind: a text-only break with the syndicate, as in L4. |
| **L11** | **.070** | **Brought Inside.** The kingpin becomes your courtier, on a short lead. | .013 c, .036 b | — | Release from prison if held; `add_courtier`; remove the flag (the non-ruler pipeline takes over); root `add_hook = { type = major_crime_accomplice_hook target = scope:eotg_kp }`; root `eotg_mod_aug_kp_informants` 10 years (`enemy_hostile_scheme_success_chance_add = -10`). **a** "Keep [kp] close." **b** [paranoid] "Keep [kp] closer: a post where I can see [kp.GetHerHim]." (`eotg_flag_aug_kingpin_watched` for 10 years; the kingpin's own risk −10). |
| **L12** | **.071** | **The Region Falls.** The crew falls back to the Region where it keeps its depots and holds it, or the county is ceded in a negotiated surrender. Never a crew conquering systems. | .012 c, .014 c | **crew only** | Zanj independency pattern (`fp3_story_cycle_zanj_rebellion_events.txt:414-470`): `create_title_and_vassal_change = { type = independency  add_claim_on_loss = no }`; the seized county (`eotg_aug_kp_seizable_county`) → the kingpin via `change_title_holder`; the kingpin `becomes_independent`. **No truce** (unlike the Zanj): root `add_pressed_claim` on the county, so it can be taken back with vanilla `claim_cb`. `add_prestige = -medium_prestige_value`. The organization's name stays on the kingpin for any later text. **Not** the Unclaimed release (§10). |
| **L13** | **.072** | **The Hold Closes.** The localized crisis: the kingpin stops asking. | T2 | ▲ syndicate, front (leverage builds faster) | **a** "Do as [kp.GetSheHe] says." stage `kept`: root `eotg_mod_aug_kp_kept` (character, while kept: stress gain +, dread gain +, tyranny gain +, vassal opinion −15), the capital `eotg_mod_aug_kp_crisis` 10 years (development growth −, county opinion −10, levy reinforcement −); the kingpin `add_hook = { type = strong_blackmail_hook target = root }`. Then T7 runs .050 The Orders every year or so: tyranny and dread climb, vassal opinion falls, and vanilla factions do the rest. That is the dread/tyranny spiral. **Exit:** T1 (the kingpin's terminal → L9 or L16, and `on_end` removes `_kept`), or leverage < 40 at T7 → L14. **b** "No." → .068 if Storm and (purge, crew or hired), else .067 (5–15). **c** [root `eotg_neurofractured`] "Do what mine already has me doing." as a, plus root risk +10 and kp −10. The kingpin's implant never acts on root: the hold is hooks, money and fear. |
| **L14** | **.073** | **A Standing Arrangement.** The extortion stalemate: you pay, they keep the streets quiet, neither of you moves. | T4, T7, .011 a failure | ▲ syndicate | Root `eotg_mod_aug_kp_tribute` 10 years (domain tax −, county control growth +). The kingpin stays in the pool; the flag is removed. **a** "It's cheaper than a war." **b** [just] "Until I find a way." (stress gain minor; `eotg_flag_aug_kingpin_grudge`, read by nothing yet; it is a seed, §10). |
| **L15** | **.074** | **The Syndicate Settles It.** The syndicate removes its own failing boss, and you owe them for the quiet. | .001 d (Patron), .013 f | **syndicate only** | The kingpin dies (`death_disappearance`). **With a Patron story:** `eotg_aug_patron_demand_effect` (one demand step nearer), desc variant. **Without one:** `add_gold = minor_gold_value` (they pay for the quiet). **Dead branch** while the syndicate kind is Patron-only (§5.2.1); kept for a future ruling. |
| **L16** | **.075** | **The Fracture Finishes It.** The kingpin's cascade ends the story before anyone else does. The neglect ending. | T1 | — | The kingpin dies (`death = { death_reason = eotg_death_cascade }`). The aftermath varies by kind: crew, capital `eotg_mod_aug_kp_loose_ends` 2 years; syndicate, `add_gold = minor_gold_value` (an unclaimed cargo); front: the record is **left alone** (seller spec: only an install or a seizure overwrites it), and only the desc changes (the clinic's doors are shut). The front is never root's clinic of record anyway (§5.2.1 exclusion); hired, root `eotg_mod_aug_kp_hired_guns` 5 years (idle guns). |
| **L17** | **.076** | **The Clinic Changes Hands.** You seize the front, and its clinic is yours now, under your law. | .013 e | **front only** | `add_gold = medium_gold_value`; **the seized company becomes root's clinic of record:** `set_variable = { name = eotg_aug_clinic_of_record value = scope:eotg_kp.var:eotg_aug_seller_company }`, so the Pursue decision names it. This is a permitted overwrite, **seizure** (seller spec §5.1 "Clinic of record", amended 2026-10-06); root `eotg_mod_aug_kp_seized_clinic` 20 years (domain tax +5%). **a** "Execute [kp]." (as L1, without the loose-ends modifier) or **b** "Let [kp] run the clinic for me now." (the kingpin becomes a courtier, as L11 without the hook). |

**Leaf count:** 17. **Profile-exclusive:** L12 (crew, hired), L15 (syndicate), L17 (front), and the .034 route into L6 (hired). **Role-dependent variants:** L4, L6 and L8 (vassal and independent). Every leaf is reachable from at least two parents, except L5 (.036), L12 (two parents but gated), L15 (two parents) and L17 (.013 only).

#### War support by kind (`eotg_aug_kp_war_support_effect`, run after any war start)

| Kind | Effect |
|---|---|
| crew | `spawn_army = { levies = eotg_aug_kp_levies_value  location = root.capital_province  inheritable = no  name = eotg_aug_kp_army_name  war = <the war> }` (small) |
| hired | the same, large; plus `eotg_mod_aug_kp_hired_guns` for the war's span |
| syndicate | `add_gold = medium_gold_value` (major if wide): mercenaries are root's own call |
| front | root `add_hook = { type = weak_blackmail_hook target = X }` on 1–2 of the opponent's vassals (`random_vassal` on the opponent, those with the highest military) |

The `war =` argument needs the war scope. After `faction_start_war` / `start_war`, find it with `random_character_war = { limit = { primary_defender = scope:eotg_kp_opponent } save_scope_as = eotg_kp_war }` (V-K7). Vanilla `spawn_army` (PX `effects.log:9774`): without `war` it "will not be spawned" if not at war, and root is at war by then.

---

## 6. Vanilla precedent

| Need | Vanilla (G = game root) | Used for |
|---|---|---|
| Story with a created antagonist, maintenance group, the story-owned character variable | `common/story_cycles/fp3_story_cycle_zanj_rebellion.txt:1-31`; in-mod `eotg_story_aug_patron` | §5.4 |
| Created character at the ruler's location, culture and faith by scope | `events/story_cycles/ep3_story_cycle_el_cid.txt:1406-1409` | §5.1.2 |
| A claimant faction for a chosen claimant and title | `common/character_interactions/00_vassal_interactions.txt:1548-1597` (`claiming_title` variable → `create_faction` → `set_special_character` / `set_special_title`) | .030 |
| A faction's war started by script | `events/factions/faction_demands.txt:396` (`scope:faction = { faction_start_war = {} }`) | .030, .032, .038, L8 |
| The claimant war and its victory hand-off | `common/casus_belli_types/00_civil_war.txt:956-1040` (`claimant_faction_war`, `on_claimant_faction_war_win_common`, `should_invalidate`) | M3 |
| Pressing a courtier's claim abroad | `common/casus_belli_types/00_claim.txt` (`claim_cb`, `scope:claimant`) | .031 |
| Seizing a county into an independent realm | `events/dlc/fp3/fp3_story_cycle_zanj_rebellion_events.txt:414-470` (`create_title_and_vassal_change = { type = independency }`, `change_title_holder`, `becomes_independent`) | L12, .032 |
| Execution with tyranny and opinion | `common/scripted_effects/00_prison_effects.txt:413` `execute_prisoner_effect` | L1, L2, L17 |
| Imprisonment with consequences | `00_prison_effects.txt:1644` `imprison_character_effect` | .006, .007, .010 |
| Hooks | `common/hook_types/`: `weak_blackmail_hook`, `strong_blackmail_hook`, `major_crime_accomplice_hook` (strong) | .003, .005, L4, L6, L8, L11, L13 |
| Death reasons | `common/deathreasons/00_event_deaths.txt`: `death_execution`, `death_murder`, `death_disappearance`, `death_vanished`, `death_battle`; in-mod `eotg_death_cascade` | leaves |
| Duel against a person, and against a fixed rating | `events/activities/chariot_race_activity/chariot_ongoing_events_jp.txt:195`; `chariot_race_events.txt:1947` (balance §5.6) | .010, .015, .034, .036, .005 |
| Composite desc (fixed part plus `first_valid`) | in-mod `eotg_fracture.0001` | §7.1 |
| Character variable holding a flag, read by custom loc on another character | in-mod tier1.018 (gang rolled on the copycat; seller spec §5.1); vanilla `04_ep2_hunt_custom_loc.txt:413-418` | §5.2.1 |
| Spawned army in a war | PX `effects.log:9774` `spawn_army`; vanilla `events/factions/faction_demands.txt:1855-1857` (spawn after `faction_start_war`) | war support |
| Debug-only decision | in-mod `common/decisions/eotg_unclaimed_decisions.txt:9` | §9.1 |

**Deviations, with reasons:**
1. **The kingpin is a pool character rather than a guest.** The Collector precedent is a guest, but the Collector stays a matter of days. A guest wanders off over years, while a pool character stays where it was created unless invited. V-K1 tests the invite risk.
2. **No truce after L12,** unlike the Zanj. The point of a seized Region is that you can take it back.
3. **The claim war bypasses the faction's power threshold** (the option starts the war directly, as vanilla's own scripted faction wars do). The player chose to strike before the faction was strong. That is the risk, and L6/L7 are its price.

---

## 7. Loc surface

**Rules:** bare scopes (`[eotg_kp.GetFirstName]`, `[eotg_kp.Custom('eotg_aug_cl_gang')]`, `[ROOT.Char.GetLiege.GetFirstName]`, never `[scope:`); one definition per key; Canadian spelling; descs 45–80 words; options 5–9 words, in the ruler's voice (writing review). For one person, use pronoun functions, never "they". Never `'s` after `Custom()`.

### 7.1 Desc assembly: per-axis fragments, not name swaps

A key beat's desc is `desc = { <fragment A first_valid>  <fragment B first_valid>  [<band line first_valid>] }`, the composition used by `eotg_fracture.0001` (`desc` + `first_valid`). Each fragment is true on every path that shows it, and each starts with `\n\n` if it follows another (lint rule, rewrite feedback §6).

| Event | Fragment A | Fragment B | Fragment C |
|---|---|---|---|
| .001 | `.desc_crew` / `_syndicate` / `_front` / `_hired` (with `_syndicate_patron` first when a Patron exists) | `.desc_m_violence` / `_bribery` / `_blackmail` / `_infiltration` | `.desc_band_flicker` / `_fracture` / `_storm` |
| .002 | `.desc_purge` / `_grandeur` / `_forecast` / `_cold` | `.desc_k_crew` … `_hired` (one line: what they brought into the room) | band line |
| .003 | `.desc_crew` … `_hired` (the offer) | `.desc_vassal` / `.desc_independent` / `.desc_noclaim` | — |
| .005 | `.desc_violence` / `_blackmail` / `_infiltration` / `_bribery` | — | band |
| .006 | `.desc_purge` … `_cold` | — | band |
| .010, .012 | per kind | — | band |
| .033, .050 | per kind / per mind and method | — | — |
| .060–.076 | the ending line | per kind (aftermath) where §5.8 says so | band (`.desc_end_flicker` / `_fracture` / `_storm`: how far gone the kingpin was) |

### 7.2 Key list (localizer)

- **Per event:** `.t`, every option `.a`–`.f` (and `.b2` etc. where a kind/role variant replaces an option: write them `.e_crew`, `.e_syndicate`, `.e_front`, `.e_hired`, `.f_hired` (.001), `.c_hired` (.012), `.b_indep`, `.c_indep`), and duel `.success` / `.failure` tooltips (index balance §5.6 form).
- **Descs:** as §7.1, plus `.desc_war` (.068), `.desc_patron` (.074), `.desc_indep` (.063, .065, .067), `.desc_purge_half` (.063), `.desc_held` (.069 from M3), `.desc_lost` (.066 from M3), `.desc_contract` (.073 from .012 c‴), `.desc_discovered` (.038), `.desc_none` fallbacks wherever a scope may be absent (the reporter in .001, the victims in .012 and .068, a county in .012 and .014).
- **Tooltips:** `eotg_aug_kingpin.<id>.<opt>.tt` where an option's effect is hidden (leverage changes are numberless: each option that moves leverage shows one of two shared tooltips, `eotg_aug_kp_leverage_up_tt` "[kp.GetFirstName]'s hold on you deepens." or `eotg_aug_kp_leverage_down_tt` "[kp.GetFirstName]'s hold on you loosens.", and the story panel shows the band), plus the toasts.
- **Story panel:** `eotg_story_aug_kingpin`, `_info`, `_kp_label`, `_band_label`, `_band_min_label`, `_band_max_label`, `eotg_aug_kp_band_1` "A favour owed", `_2` "Deep in their pocket", `_3` "They own the room" (owner wording; checked against §7.4: it is about the room, not "owns you"), `eotg_aug_kp_leverage_up_tt`, `_down_tt`.
- **.040:** `.t`, `.desc`, `.desc_open` / `_collab` / `_custody` / `_kept` / `_war`, band lines, `.a`–`.c`.
- **Modifiers:** `<key>` and `<key>_desc` for all 15. **Opinions:** 6 keys. **Decision:** `eotg_decision_aug_debug_kingpin`, `_desc`, `_tooltip`, `_confirm`. **Army:** `eotg_aug_kp_army_name`.
- **Estimate:** about 440 keys. The scripter hands the localizer the exact list from the built file (the dangling-key check in `px_lsp_diagnostics.js`).
- **Vanilla strings:** none need a `replace/` override. Faction, war and CB text is vanilla's and reads correctly with mod titles. Vanilla `claimant_faction_war` names are medieval-neutral; CB-33 (scheme agent names) is unrelated.

### 7.3 Text plan (beats only; the localizer writes)

**Named actors in every scene** (writing review: 18% of mod court events name nobody):
- the kingpin, always;
- the reporter in .001 (your spymaster, else your marshal, else a guard captain described but not scoped: "the captain of the dock watch");
- the lieutenant (.009), the informant (.007), the errand and purge targets (.005, .006);
- the liege in the vassal path;
- the rival in .031/.032;
- the victims in .012 and .068.

**The kingpin's Neurofractured voice:** it is the kingpin's *own* implant, heard through what the kingpin says and does, never as a voice in root's head. It follows index §5 item 1: it logs, schedules, forecasts the **wearer**, and requests access. Per mind:
- **purge** (the implant forecasts the kingpin's own suspicion and violence; it never flags other people): "It had me reaching for [lieutenant] a day before I knew I'd stopped trusting [lieutenant.GetHerHim]. It's been right about me every time." At .006: "It has me going for [target]. Give [target.GetHerHim] to me, or it will be me who does it." No hand-written names: use a scope, or "my second".
- **grandeur:** "It doesn't show me hesitating any more. You'd be surprised how much that's worth in a room."
- **forecast:** "Sorry. It ran ahead of me again. I'll let you finish." At .006: "Every time it runs me forward, I end up on the other side of you. I wanted you to hear that from me." At .072: "It already has me shaking your hand. It is usually right about me." At .002 (narration): [kp.GetSheHe] starts to rise before [kp.GetSheHe] has decided to, sits again, and apologizes for the habit.
- **cold** (narration, not speech): [kp.GetFirstName] looks at the floor when spoken to, and replies with prices.

**Never:** prophecy of plots, of the future of the realm, or of other people's choices (the forecast is of the kingpin, a moment ahead). Never "whisper", "it speaks", "answers", Void, Orrin, the Eye, breach, rift, hollow, or "grip" as a metaphor (index §5 item 2).

**Register** (rewrite feedback §2–§3):
- Places: the lower levels / the underlevels (the umbrella term: true on stations, ships and colony worlds alike), the stacks, the docks, cargo bays, a cargo hulk, a bonded warehouse, the drill floor, a hangar, the cells, the audience chamber, the residence. Never "decks" as the umbrella.
- Things: work lights, the panel, coil whine, sutures, a sedative.
- **Never:** dungeon, castle, throne room, tavern, guild, scroll, seal and ring, knight-as-rank, "by morning", seasons, or a medieval crime vocabulary ("brigand", "thieves' guild", "footpads").
- No real-world mafia vocabulary (seller spec B2: Don, capo, consigliere, made man, "the Family", fedoras).
- **"Kingpin" appears only in the system name and the event-title family, never in prose and never in any line a syndicate-kind story can show.** Prose uses the per-kind noun: crew "boss"; syndicate "the syndicate's boss here"; front "the director"; hired "the captain". Shared lines use the kingpin's name.

**LAW AT 866:**
- The trial in .013 b / L2 is held **under your own law**, in your court.
- In the vassal path, the liege's law is the liege's own.
- No galactic court, no extradition, no "authorities" above the realm.
- "Sanctioned" means sanctioned under the realm's own law.
- The front's crime is that it keeps and sells its clients' logs and fits unvetted hardware. No licensing body is named or implied (index §5 item 3).

**Time-neutral:** "before the next shift", "weeks later", "a year of quiet".

**Multi-species:** "people", "personhood", never "humanity".

**"True on every path":**
- .003's role fragment shows only when the option it describes is visible: `.desc_vassal` requires `eotg_aug_kp_liege_claim_possible`, otherwise `.desc_noclaim`.
- A leaf's aftermath line must not promise a death that a later option decides (L9's "a" and "b" both end the kingpin's story, but only "a" can kill on screen).
- .060 says nothing about the organization's fate beyond "splinters".

### 7.4 Lore wording fixes (lore review 2026-10-06; binding on the localizer)

*(Note 2026-10-08: speech in these lines is rendered with inner unescaped `"` (event_quality_v1 §12.2); narration is first person per §12.1. The approved wording itself is unchanged.)*

**Banned in every line of this chain** (in addition to index §5 item 2 and seller spec B1/B2):
- warrant, police, officers (as law), law enforcement, authorities, law-and-order;
- puppet, strings, "owns you", clean house;
- "kingpin" in any line a syndicate-kind story can show (and in prose generally, §7.3);
- "says" for the implant (the kingpin says; the implant *has them* doing, *runs them forward*, *shows*);
- today, tonight;
- decks (as the umbrella; use the lower levels / the underlevels);
- hang, gallows, noose;
- neural copies.

**Fixed wordings:**
- .013 a: "Execute [kp]. Now."
- The syndicate kind's place: "the customs desk that waves them through".
- L1 compassionate option: "Give [kp.GetHerHim] proper rites."
- L1 desc: "the order", "the arrest"; never a warrant.
- L9: the massacre reaches your court only because the boss "came up to the residence".
- L12: the crew falls back to the Region where it keeps its depots, or the Region is ceded in a negotiated surrender. Never a crew conquering systems.
- L13 and .050: never imply that the kingpin's implant acts on root. The hold is hooks, money and fear. The .050 "march" is a show of force that root stages with his own levies. .050 d and .072 c read "Do what mine already has me doing."
- Retitles: .033 "The War Below"; .036 "The Partner's Price"; L5 "Before the Bill Came"; L6 "Sold to the Winner"; L7 "Every Level Burning"; L8 "The Turn"; L15 "The Syndicate Settles It"; the purge line in .072 "or I start with yours".
- Voice lines: as §5.2.4 and §7.3, verbatim intent. No hand-written personal names ("my second", or a scope).
- Syndicate-kind landed outcomes (L4, L10, the claim wars): the boss acts for himself and breaks with the syndicate. No line implies the syndicate's head knows or cares; no Flesh Pledge, souls or "loyalty".

---

## 8. Lore constraints

**Canon that bounds this system** (ERRATA first, then dated `docs/lore/` entries, then the bookmark design; human ruling, 2026-10-04):
- **L1. LAW AT 866** (SETTING LORE ERRATA): no authority above the polity. The trial, the order, the arrest and the crackdown run under the realm's own law. No extradition and no "authorities".
- **L2. CYBERNETICS AT 866** (ERRATA): implants are common, commercial and imperfect, fitted and repaired by clinics and back-street surgeons. The front **services and deals**; it never manufactures (seller spec §8.1.2). No self-repairing hardware (it is a researchable advance), and nothing in this chain implies it.
- **L3. The Pill Mob is canon, and its head is canon** (`docs/lore/Third era Nations.md:4024-4032`: Dr. Pill, "rose from death", "eternal ruler", "immortal kingpin"; "a 1920s–1930s mafia aesthetic"). When the kind is `syndicate` and the list returns the Pill Mob, **the kingpin is a local boss of that syndicate's business in your realm, never its head**. The text never touches resurrection, immortality or the mafia aesthetic. Seller spec B1 (no Red Pills, Dr. Pill, Pillwake, Shadow Cartel, Flesh Pledge, souls, drugs or addiction) and B2 (no mafia vocabulary) bind **every** line of this chain, not only the syndicate lines. **KQ1 ruled:** syndicate kind is Patron-only (index §5 item 3, `cybernetics_v2.md:211`). Landed syndicate outcomes (L4, L10, the claim wars) are text-only breaks: the boss acts for himself and leaves the syndicate.
- **L4. Reprisal P7** (`cybernetics_v2_reprisal.md:304`): the syndicate's name never shares a sentence with an ownership word ("theirs", "owned", "loyalty", "bound", "leash", "under contract"…). This applies to the syndicate kind here, as in the Patron.
- **L5. Voice register** (index §5 item 1; ERRATA "CYBERNETIC VOICE"): the implant forecasts its wearer, slightly ahead. The kingpin's implant never forecasts *other* people or events months away. **KQ2 ruled (lore review, 2026-10-06):** every mind forecasts the kingpin only, as reframed in §7.3. Purge forecasts the kingpin's own suspicion and violence and never flags other people; forecast's lines are "Every time it runs me forward…" and "It already has me shaking your hand…". The implant never "says".
- **L6. Never-names** (index §5 item 3; seller spec §8.3): the organization is named **only** through `Custom()`. No hand-written org name, no named authority, no Blackstar, Shadow Markets, Black Contract, Concrete Cartel and so on. **No salvage trade** (`interactions.md:841`).
- **L7. 866 AG:** the Myr Cluster Wars ignited in 850. A civil war in a Myr realm reads as one more war in a war zone, not as a first breach of peace. No Galactic League. The Titan Exodus is ongoing: no line presents the people of the underlevels as Exodus refugees (an Unclaimed Regions rule, applied here for consistency).
- **L8. No Nikios** (CLAUDE.md invariant 9): no khanate or steppe flavour, and no tribute CB.
- **L9. Multi-species, faith-neutral:** no monotheistic invocations (index §5 item 4). The zealous reactions are faith-neutral.

**Lore-keeper questions (ruled 2026-10-06; kept for the record):**
- **KQ1.** With only `the Pill Mob` in `[syndicates]`, every syndicate-kind kingpin is a Pill Mob local boss. Is a local boss of the Pill Mob, Neurofractured, in an arbitrary 866 realm canon-safe? Or should the syndicate kind be **disabled** while the list has one entry (weight 0 unless `eotg_aug_has_patron = yes`)? **Ruled:** Patron-only (index §5 item 3, `cybernetics_v2.md:211`).
- **KQ2.** The forecast mind's lines (§7.3). **Ruled:** reframed; see L5.
- **KQ3.** "Kingpin" as an in-world word. The owner used it, and canon uses it of Dr. Pill. Should the prose say "boss" and leave "kingpin" only in the event-title family? **Ruled:** the title family only, never in syndicate-kind lines; per-kind nouns in prose (§7.3).

---

## 9. Definition of done

0. **Tiger, `px_lsp_diagnostics.js` and `px_vocab_check.py` are clean** on the new and touched files, except the known-benign list (CLAUDE.md §Validation). Tiger is the scope check: `faction_start_war` in faction scope; `set_special_character` in faction scope; `add_hook` in character scope with the target; `create_title_and_vassal_change` + `becomes_independent`.
1. **Reachability:** `px_event_report.py` shows all 42 events reachable (.040 from the story's `on_owner_death`). `.001` from the on_action; every node and leaf from a node, the story tick or maintenance. No event is fired by nothing.
2. **Cooldown authority:** `grep -n "eotg_flag_aug_kingpin_cooldown" events/` returns nothing. No event `trigger` reads a flag. `.001`'s trigger is `eotg_aug_kp_can_start = yes` only.
3. **Signature coupling (QA audit 8):** every one of the 42 events moves the kingpin's `eotg_fracture_risk` in ≥ 1 option, or reads `eotg_aug_pressure_*` on `scope:eotg_kp` in a `triggered_desc`. ≥ 30 events **move** it.
4. **Visibility (owner ruling Q6):** `eotg_story_aug_kingpin` is the only `visible = yes` story in the mod, and its only `basic_counter` reads `eotg_kp_leverage_band` (min 1, max 3). Nothing shows `eotg_fracture_risk` or raw `eotg_kp_leverage` (grep: no `basic_counter` on either; no digits next to those words in loc). `eotg_kp_leverage_band` is written only inside `eotg_aug_kp_leverage_effect`. In game: the story panel shows the kingpin, the band name, and the explanation, and the band changes after .004 a (deepen) and .007 a (loosen).
4a. **Inheritance (owner ruling Q2):** kill the owner mid-story (`kill` on yourself with a heir; or the console death effect) in `collab`, `kept` and `war` (path `back_kp`): the heir owns the story, .040 fires with the right stage fragment, leverage is down one step's worth (or the same band), refusals are 0, and in `kept` the heir has `eotg_mod_aug_kp_kept` and is hooked by the kingpin. In `war` path `own` and in `pending`, the heir's stage is `collab`. With the kingpin dead, or with a leaf event pending, the story ends instead.
5. **Map-agnostic:** `grep -nE "title:[ekdcb]_|c_[a-z]|culture:|faith:|character:" ` over the new files returns nothing outside comments.
6. **Profile variety:** a 100-start observer run (`docs/tools/observer`, or `eotg_decision_aug_debug_kingpin` ×100 in one session) shows all 4 kinds, all 4 minds and all 4 methods. Each exclusive leaf (L12, L15, L17) is reachable only with its kind (QA reads the option triggers).
7. **Leaves:** each of the 17 leaves is reached at least once by the console recipes (§9.1) and ends the story (`any_owned_story` false afterwards). It applies the §5.8 mechanics, verified on the character sheet: the modifier, the hook, the title holder, or the death and its reason.
8. **Wars:**
   - a vassal player's .030 a raises a claimant faction (the Factions tab shows the kingpin or root as claimant, and the liege's title) and starts `claimant_faction_war`;
   - winning with `back_kp` makes the kingpin the liege, and .063 pays out;
   - losing fires .065;
   - an independent player's .031 a starts `claim_cb` for the kingpin, and .032 a starts a liberty war against root.
9. **Seller names:** the organization's name renders in .001 for every kind, and is the same in every later event of that story. With a Patron, it equals the Patron's syndicate. A cold console fire shows the seller fallback text, not a raw key.
10. **E1:** while the kingpin is root's courtier (claim stages), `eotg_aug_nr.*` never fires for them.
11. **Loc:** every key exists once, with BOM. No `[scope:`. `eotg_lint` L010–L016 pass. No banned word from §7.3, index §5 item 2 or seller spec B1/B2 (L012 register).
12. **Human, in game:** the §9.1 recipes; plus one natural run (speed 5, an augmented count under a Ban with a Patron) that sees `.001` within about 6 years.

### 9.1 Console recipes (per leaf)

**Start** (forcing the profile):
```
effect = { set_variable = { name = eotg_kp_force_kind value = flag:front } set_variable = { name = eotg_kp_force_mind value = flag:purge } }
event eotg_aug_kingpin.001
```
Or take the debug decision. **Shorthand** used below: `S{…}` = `effect = { random_owned_story = { limit = { story_type = eotg_story_aug_kingpin } … } }`; `KP{…}` = `S{ var:eotg_kp = { … } }`.

| Leaf | Recipe |
|---|---|
| L1 .060 | start any → .001 b → .010 a (`yesmen` does not apply to duels; raise martial with `add_martial_skill = 20` first) → .013 a |
| L2 .061 | as L1 → .013 b; wait 30–60 days |
| L3 .062 | kind syndicate → .001 a → .002 a → .003 a; `S{ set_variable = { name = eotg_kp_years value = 6 } set_variable = { name = eotg_kp_leverage value = 30 } }`; wait for the yearly tick (or `KP{ set_variable = { name = eotg_fracture_risk value = 70 } }` to also meet the Storm branch) |
| L4 .063 | vassal; → .003 c → .030 a. As the faction leader, win the war with the console (`win`, or white-peace-proof: occupy and force the war score to 100). M3 fires .063 within a month. Independent: → .003 b′ → .031 a → `win` |
| L5 .064 | vassal; .003 b → .030 a → `win` → .036 c with `add_intrigue_skill = 20` |
| L6 .065 | vassal; .003 c → .030 a → `lose` (or surrender in the war window) |
| L7 .066 | as L6 but `S{ set_variable = { name = eotg_kp_war_years value = 3 } }`; wait a month |
| L8 .067 | → .003 a; `S{ set_variable = { name = eotg_kp_refusals value = 2 } }`; wait for the tick. Independent variant: an independent root with vassals |
| L9 .068 | any collab; `KP{ set_variable = { name = eotg_fracture_risk value = 96 } }`, force mind purge; wait for the tick (40–60% massacre; repeat the start if .075 rolls) |
| L10 .069 | root with ≥ 2 counties → .001 b → .010 → .013 d |
| L11 .070 | → .013 c |
| L12 .071 | kind crew, root with ≥ 2 counties → .003 d → .012 c |
| L13 .072 | collab; `S{ set_variable = { name = eotg_kp_leverage value = 85 } }`, `KP{ set_variable = { name = eotg_fracture_risk value = 40 } }`; wait for the tick → .072 a. Check `_kept` and `_crisis`, then wait for .050 |
| L14 .073 | collab; `S{ set_variable = { name = eotg_kp_years value = 6 } set_variable = { name = eotg_kp_leverage value = 55 } }`; tick |
| L15 .074 | kind syndicate (or a Patron: run init.018 e first) → .001 d, or .013 f |
| L16 .075 | `KP{ set_variable = { name = eotg_fracture_risk value = 96 } }`, force mind cold; tick (repeat if .068 rolls) |
| L17 .076 | kind front → .001 e → .015 a (with `add_stewardship_skill = 20`) → .013 e. Then check that the Pursue decision names the seized company |

**V-checks (in game, human):**
- **V-K8:** after `make_story_owner` inside `on_owner_death`, does `story_owner` point to the heir? And what does vanilla do with a claimant faction war whose leader (the dead owner) is not the claimant?
- **V-K1:** does an AI ever invite the pool kingpin? (Observer run.)
- **V-K2:** does `can_create_faction` pass for a vassal with `claiming_title` set and a pressed claim?
- **V-K3:** `claim_cb` with `claimant = <courtier>` and `target_title =`.
- **V-K4:** `max_military_strength` as a script value.
- **V-K5:** `add_secret = { type = secret_murder target = … }`.
- **V-K6:** removing an enemy knight from script.
- **V-K7:** finding the war scope after `faction_start_war` / `start_war`, and `end_war = white_peace`.

Each failed check has a fallback in the cited row (V-K8: fire .040 on a scope saved before the hand-off; treat a war the heir did not inherit as lost, as M3 already does). The scripter records which one was used.

---

## 10. Deferred

| Item | Why |
|---|---|
| **The Unclaimed Regions release for L12** (`eotg_unclaimed_release_effect` when the seizing kingpin dies without heirs) | It is map-agnostic, but it makes Unclaimed a by-product of crime, and the Unclaimed placeholders are "the Unsworn", not a gang. A gang is a ruler, not nobody. The seizure uses vanilla independency instead. Owner question Q5. |
| The landless-adventurer kingpin (a 1.20 camp with followers) | DLC-dependent (Roads to Power) and a government the mod does not own. The pool character covers the role. |
| A playable kingpin (become the boss) | A new government or a landless-ruler path; out of scope. |
| MAA for hired crews | The mod has no MAA lift yet. Levies only. |
| The L14 grudge payoff (`eotg_flag_aug_kingpin_grudge`) | A seed for a later beat. Event expansion is the owner's call (memory: feedback_event_expansion_deferred_to_user). |
| Region-, culture- or faith-specific organizations | They need the real map (seller spec §10). |
| A second kingpin per life | One per life, until play shows whether players want more. Owner question Q3. |
| Cross-system: a Countdown or Heir's Arc beat reading the kingpin | Keeps other stories untouched (owner brief: "don't drastically alter other story cycles"). |

---

## 11. Owner questions

- **Q1. Pill Mob (KQ1). Settled by ruling:** syndicate kind is Patron-only (index §5 item 3, `cybernetics_v2.md:211`). L15's "without a Patron" branch is dead while that holds.
- **Q2. Inheritance. Ruled 2026-10-06: the story passes to the heir** if the kingpin is alive and no leaf is resolving (vanilla `on_owner_death` shape, `ce1_story_cycle_black_death.txt:18-30`). Reason: the crisis is the house's, not one ruler's, and a debt that dies with the debtor would make the kept stage escapable by dying. Built in §5.4.1 (carry-over) and .040.
- **Q3. Frequency. Ruled 2026-10-06: 2% a year at base** (was 4%), multipliers, 10-year cooldown and once per life unchanged. Reason: about once or twice per campaign keeps it an event, not a fixture (§5.3).
- **Q4. Empire-tier claims. Ruled 2026-10-06: allowed, as specced.** Reason: vanilla's claimant faction targets the direct liege at any tier (`create_claimant_faction_against_interaction`, `00_vassal_interactions.txt:1367`); the AI stays discouraged by its `ai_chance` (§5.7).
- **Q5. L12. Ruled 2026-10-06: vanilla independence, as specced,** the boss holding the whole Region as one ruler; not the Unclaimed release. Reason: a crew is a ruler, not "the Unsworn" (§10).
- **Q6. Leverage visibility. Ruled 2026-10-06: visible as three bands,** not hidden; the exact number stays hidden. Reason: leverage is the player's lever, not a hidden risk, and the bands map to the tree's own thresholds. Built in §2 and §5.4.2 (visible story, `basic_counter` on a 1–3 band variable, band-name custom loc, explanatory string).

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Build batch A of docs/specs/cybernetics_v2_kingpin.md (.001–.015, .060–.062, .068–.071, .073–.076, the story without the war stages, the on_action, E1, the templates, the debug decision), then batch B (.030–.039, .050, .063–.067, .072, the war stages, M3/M4). Apply the lore review as written (§5.2.1 syndicate Patron-only and the front exclusion, §5.2.3–§5.2.4 minds, §7.3–§7.4) and the owner rulings (§11: 2% entry, heir inheritance §5.4.1 and .040 in batch A, the visible banded story §5.4.2).
- files: docs/specs/cybernetics_v2_kingpin.md, docs/specs/cybernetics_v2_seller_names.md (seizure amendment, §5.1 and §5.3)
- needs-loc: about 440 keys in localization/english/eotg_aug_kingpin_l_english.yml (§7.1–§7.4), after the scripter's build gives the exact list
- needs-lore: none blocking (KQ1–KQ3 ruled 2026-10-06); sign-off of the drafted loc against §7.4
- needs-human: none open in §11 (all ruled 2026-10-06); V-K1–V-K8 in-game checks after batch A/B
