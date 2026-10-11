# Spec: Government requirements template (CK3 1.20)

**Author:** eotg-architect, 2026-10-11. **Status:** reference template. It is not a build order, so nothing in it is built directly.
**Audience:** architect, scripter, localizer and QA, and the owner when designing the next government.
**Use:** answer §2 before anything else. Work through §3 surface by surface, apply the §4 overlay, and run §5. Copy §7 into the new government's spec (`docs/specs/<gov>.md`) and fill it in. §6 checks the four existing governments against the template.

**Sources and abbreviations.**
- `V/` is the vanilla game root, `D:/SteamLibrary/steamapps/common/Crusader Kings III/game/` (installed 1.20.0.3).
- `GT` is `V/common/governments/00_government_types.txt`, `JT` is `01_japan_government_types.txt`, `TT` is `02_theocratic_government_types.txt`, and `GI` is `V/common/governments/_governments.info` (772 lines, read in full).
- Research notes from 2026-10-11 are in the session scratchpad (`govresearch/01`–`04`). Every vanilla citation below comes from them or from a direct read.
- **[inferred]** marks a conclusion the files don't state. **[engine, unverified]** marks behaviour that lives in the executable and needs an in-game check. **[web]** marks a claim from dev diaries or the wiki rather than from game files.

**Precedence conflicts found while writing this** (higher source wins, so they are reported here rather than silently resolved):
- The ck3-modding skill's `governments.md` shows the pre-1.15 shape: rules at top level and a `vassal_contract = { }` list. Its `reference/common/governments/_governments.info` has 735 lines and no `possible_grant_vassal_governments` or `grant_vassal_ai_will_do`, so it predates 1.20. **Use vanilla `GI` and `GT`.** This was already reported in `governments_v2.md` §5.5.
- `GI:488-498` still documents `vassal_contract = { }` (the old list form) pointing at `common/vassal_contracts/`. Vanilla 1.20 uses `vassal_contract_group` (`GT:22`) and `common/subject_contracts/`. `.info` is wrong in both directions: it documents fields the parser rejects (`use_great_projects`, `GI:630`, pitfalls lesson) and omits fields vanilla uses (`vassal_contract_group`, `tax_slot_type`, `allow_accolades` at `GT:11`, `realm_mask_offset`/`_scale` at `GT:60-61`, `max_dread` at `GT:665`). **Rule: a field is usable when a vanilla `.txt` uses it. `.info` alone proves nothing.**

---

## 1. What "playable" means in practice

A government is playable when a human can pick a ruler of it at game start and keep playing after that ruler dies.

**Correction (2026-10-11).** The research said there was no script-visible playable switch (research 01 §2). That was wrong. **The gate is the scripted rule `is_character_allowed_to_be_player`** (`V/common/scripted_rules/00_rules.txt:151-249`). It is a **blacklist of government flags**, and each entry fails with a `GAME_OVER_CANNOT_PLAY_*` text (loc in `V/localization/english/gui/ingame_main_l_english.yml:83-89`). Inside `trigger_if = { limit = { scope:will_override_government = no } }` (`:152-155`), so it is skipped entirely when the engine will override the government, it blocks the following:
- `government_is_republic` (`:157-160`), `government_is_mercenary` (`:162-165`) and `government_is_holy_order` (`:167-170`), always;
- `government_is_administrative` without the `admin_gov` DLC feature (`:172-180`);
- ecclesiastical and theocracy without `by_god_alone` (`:182-199`);
- without `roads_to_power`: landless adventurers, barons, and the catch-all `is_playable_character` (`:201-217`);
- landless Japanese-government and theocracy rulers without a domicile (`:219-235`, `GAME_OVER_CANNOT_PLAY_ESTATELESS`, unless they hold a `clerical_elector_title`).

Otherwise the catch-all applies (`:237-247`): `is_playable_character = yes`, or a non-ruler who passes `is_valid_for_laampdom`, and in both cases no `declined_become_laamp` flag.

**So a mod government is playable by default** if it carries none of those flags and its rulers pass `is_playable_character` (P4). Republic is unplayable because of the blacklist entry at `:157-160`, **not only** because it lacks dynasty rules. The "Is unplayable" flag labels (P9) are the loc side of the same list.

### 1.1 Hard requirements

| # | Requirement | What to set | Evidence | Engine-side / unverified |
|---|---|---|---|---|
| P0 | **Not on the playable blacklist**, or deliberately on it | Playable: carry none of `government_is_republic`, `_mercenary`, `_holy_order`. Avoid `_administrative`, `_ecclesiastical`, `_theocracy` and `_landless_adventurer`, which are DLC-conditional. **Unplayable on purpose:** add a `custom_description = { text = "GAME_OVER_CANNOT_PLAY_<X>" NOT = { government_has_flag = eotg_government_is_<gov> } }` entry. | `V/common/scripted_rules/00_rules.txt:151-249` (above) | **Making a government unplayable needs an override of `is_character_allowed_to_be_player`.** The safe form is the same path, `common/scripted_rules/00_rules.txt`, which replaces the whole vanilla file. That is a compatibility cost, and the file must be re-diffed every patch (`docs/pitfalls.md` §2). **UNVERIFIED:** whether a same-key rule in a separately named file (e.g. `zz_eotg_rules.txt`) overrides the key or duplicates it. There is no `_scripted_rules.info` in vanilla or in the skill. Project precedent: a key-level override works for scripted triggers (`docs/pitfalls.md` §16). Check it with `logs/database_conflicts.log` and test T14 before relying on it. |
| P1 | **Dynastic rulers**, so the heir is in the player's dynasty and play continues | `government_rules = { rulers_should_have_dynasty = yes  create_cadet_branches = yes }` | Default is `no` (`GI:30-33`). Feudal `GT:7-8`, clan `GT:98`, admin `GT:453`. Every playable landed vanilla government sets it. Republic (`GT:64-70`), mercenary (`GT:329`) and herder (`GT:745`) don't. Republic and mercenary are *blocked* by the P0 blacklist (`00_rules.txt:157-165`); the missing dynasty rule is a second reason, not the gate. | The wiki says "non-dynastic governments … are not playable", and a random character inherits [web, research 04 §3]. Whether a dynastic player whose heir falls outside the dynasty gets game over is the engine's succession behaviour, and T3 checks it. |
| P2 | **Leave `inherit_from_dynastic_government` at its default (`yes`)** unless you are building a full heir channel | don't set it | `GI:164-173`: "Many non-dynastic governments are unplayable, so it prevents game over." Republic, theocracy, ecclesiastical, mercenary and both holy orders set `no`. | **Caveat:** `no` puts the government in the non-dynastic group, whose rulers can't inherit from dynastic ones. Theocracy only became playable in 1.20 after Paradox added designated heirs, clerical succession, a conclave and "Establish a Dynasty" [web, research 04 §3]. **Caveat on `yes` [inferred]:** a ruler of another dynastic government can inherit this government's titles and keep their own government. `use_as_base_on_landed` (P5) only fires on a ruler's *first* title. Expect realms to erode to feudal through cousins, and test it (§5, T4). |
| P3 | **A valid succession law** for every ruler of the government | own `succession_order_laws` law (§3.5) | Vanilla order laws whitelist government flags (`V/common/scripted_triggers/00_law_triggers.txt:268-280, 343-397, 589-591, 641-670`). A new government qualifies for none of them. | A custom law that never applied fell back to "Agnatic" and the government displayed as "Anarchy" [web, research 04 §4]. |
| P4 | **`is_playable_character`** must be true for its rulers | a title above barony, or a domicile, or `landless_playable = yes` | `V/common/scripted_triggers/00_available_for_events_triggers.txt:964-980`: `is_ruler`, then a domicile, or `highest_held_title_tier > tier_barony` (landed), or a theocracy-flag government. `landless_playable` (`GI:61-66`) **needs the DLC flag `landless_playable`**. | `is_playable_character` is the catch-all inside the P0 rule (`00_rules.txt:216, 245`). The blacklist itself is script (P0), not engine. |
| P5 | **The heir keeps the government** | `use_as_base_on_landed = yes`, `sticky_government = yes` | `GI:73-77`, `GI:148-151`; admin `GT:458, 462`; nomad `GT:642-647`. `use_as_base_on_rank_up` (`GI:79-83`) also spreads it upward to conquerors, so leave it unset unless that is wanted (`governments_v2.md` §5.0). | Test it with a death and a `kill` (§5, T3). |
| P6 | **A `NGovernment.GOVERNMENT_TYPES` entry** | the mod's define file lists **all 20 vanilla keys verbatim** plus the new key | `V/common/defines/00_defines.txt:550-573`. **An array define replaces vanilla's list, it does not merge** (`docs/pitfalls.md` §2, "Define arrays replace"). The engine pre-registers `<g>_vassal_opinion`, `<g>_opinion`, `<g>_tax/levy_contribution_add/_mult` only for listed governments. Without the entry you get 12 "Could not find the preregistered modifier type" errors. | Two copies must stay in step: `common/defines/eotg_government_defines.txt` and the test sub-mod's `docs/test_submods/british_isles/common/defines/zz_eotg_test_bi_government_defines.txt`. Re-copy the vanilla 20 after every CK3 patch. |
| P7 | **`can_get_government` and a fallback story** | either a guard (`GI:358-368`) or a recorded decision not to have one, plus a known exit government | `can_get_government` is checked "when landed" (`GI:358-368`). If nothing passes, the `fallback` order is used (`GI:348-356`): feudal 1, clan 2, administrative and celestial 3. Guard shapes: mandala `GT:949-957` (liege-or-independent), monastic holy order `GT:439-443` (title-based). | **The trade-off:** a guard risks an heir failing it at succession and dropping to feudal. No guard risks leakage, meaning the engine hands the government to unrelated newly landed rulers [engine, unverified]. **Never set `fallback` on a mod government**, or it becomes a default for empty counties. `assign_new_government_effect` (`V/common/scripted_effects/00_government_effects.txt:75-199`) does not check playability (comment at `:158`). |
| P8 | **Reachability: bookmark and ruler designer** | a bookmark `character = { government = <key> }` entry, or a decision path from a reachable government | Bookmarks set `government =` per character (`V/common/bookmarks/bookmarks/00_bookmarks.txt:1196` ecclesiastical). The ruler designer only ever assigns tribal, clan or feudal (`V/common/on_action/ruler_designer.txt:147-161`). The bookmark and designer GUIs branch on government only for display. | Without either, a player reaches the government only by picking its ruler on the map, or through an in-game adoption decision. Whether the bookmark screen remaps an "unplayable" government at start (Herder → Nomadic, [web]) is **[engine, unverified]**. Test it (§5, T1). |
| P9 | **Never carry an "unplayable" identity flag** | omit `government_is_republic`, `government_is_mercenary`, `government_is_holy_order`, `government_is_herder` | Their loc labels read "Is unplayable" (`V/localization/english/government_l_english.yml:272, 280, 281, 285`). Republic, mercenary and holy order are the P0 blacklist entries. | `government_is_herder` carries the label but **is not on the P0 blacklist**. Whatever keeps herders off the player list lies elsewhere [unverified]. Don't carry it either. |
| P10 | **DLC independence** | don't rely on rules that need a DLC flag | `landless_playable` (`GI:64`) and `mechanic_type = administrative` (`GI:330`, `admin_gov`) are DLC-gated. Vanilla DLC governments gate `can_get_government` on `has_*_dlc_trigger` (`GT:301, 669, 1228`). | A player without the DLC loses the mechanic silently [inferred]. |

### 1.2 What playability does *not* require
- `mechanic_type`. Republic (`GT:64-92`) and japan_feudal (`JT:97-182`) set none. The project's `eotg_unclaimed_government` loads without one; whether a playable one is *played* correctly is CB-49 / V-G3.
- A domicile, a situation, a unique currency or a custom GUI. Those are what make a government *distinct* (§2). They aren't what makes it *playable*.

---

## 2. Design questions to answer before building

**The rule.** A government earns new mechanics only when its **core verb differs from feudal's "conquer land, then inherit it"**. This is Paradox's pattern [web]: DD148 says admin "you will have to engage in politics" because land is temporary and the house is permanent; DD174 says a cyclical fall needs a cyclical rise; DD176 says Mandala expansion relies on alternatives to war (research 04 §2). If the verb is the same as feudal's, the right build is a **feudal reskin**: flags, rank names, a `character_modifier` and flavour. It doesn't need a new resource or vassal model. Say which kind you are building, in writing, before §3.

Answer each question in the §7 form.

### Q1. What is the core verb?
One sentence: "A ruler of X spends their time ___ to get ___." Vanilla examples (research 04 §1):
- tribal raids and wins battles for prestige;
- clan manages tax jurisdictions and House Unity;
- admin plays politics for influence;
- nomad keeps subjects obedient and migrates;
- mandala radiates to pull tributaries;
- adventurer takes contracts and moves the camp.

If the answer is "conquers and inherits, with a different flavour", stop here and build a reskin.

### Q2. What is the signature resource, and is it an engine currency or a scripted one?
Every post-1.13 government has one, usually walled off from gold (research 04 §2). The project requires one per system (invariant 5): every flavour event moves or reads it.

| Option | What you get | Cost and risk | Evidence |
|---|---|---|---|
| **Piety, prestige, dread** (universal) | Already in the UI, AI-aware, with level tables; costs use `piety =` / `prestige =` | Not distinct. Every ruler has it. It works as the resource only if the government changes how it is *gained or spent* (modifiers, costs, `currency_levels_cap`). | `currency_levels_cap` (`GI:568-579`) can only lower the caps for piety, prestige, influence and merit. Mandala sets piety 8 (`GT:1087`). |
| **Influence** | Existing UI and effects (`change_influence`, cost key `influence =`, modifiers `monthly_influence(_mult)`) | It is switched on by the capability flag `government_has_influence` (interactions 78, activities 58, great projects 27, buildings 16 hits). Its gain rates are coded for admin (`V/common/defines/00_defines.txt:318-320`). **Every vanilla government with the flag is `mechanic_type = administrative`, and the top-bar widget is gated on the mechanic, not the flag** (`V/gui/hud.gui:7025`). A non-admin government with the flag would show influence in the character window and ledger only. Gain through `monthly_influence` is likely; spending and admin features are unknown (§8.1, test T11). | research 02 §0, §6; §8.1 |
| **Merit, treasury, obedience** | Engine currencies with UI | Turning on `merit = yes`, `treasury = yes` (`GI:112-125`) or `obedience = yes` (`GI:137-141`) brings in the administrative stack: budgets, salary laws, `replace_gold_cost_by_treasury`. Vanilla uses them only with `mechanic_type = administrative` or nomad. [inferred] Expect half-working UI without the rest of the stack. | research 03 §6-7, §9 |
| **Herd, provisions** | Engine currencies | **They exist only inside a domicile** with `herd = yes` / `provisions = yes`, and are changed by `domicile = { change_herd / change_provisions }` (`V/common/scripted_effects/00_faction_effects.txt:1125-1126`, `00_activity_effects.txt:2814-2815`). That means a domicile (§3.9). | research 03 §1, §3 |
| **Radiance** | — | **Closed.** It uses the rule `radiance = yes` plus `mandala_radiance_value`, marked "USED IN CODE, DO NOT RENAME" (`V/common/script_values/tgp_mandala_values.txt:485`). It can't be re-pointed. | research 03 §4 |
| **Scripted pseudo-currency** (variable plus script value) | Full design freedom; map-agnostic; no DLC | **No caps or level tables come with it.** It needs clamping in one change effect and an AI that reads it in `ai_will_do`. **Display needs no GUI file:** a scaled character modifier shows the live value in the character window and its tooltip (`V/common/modifiers/00_court_position_modifiers.txt:138-141`), and a visible story cycle shows it as a `basic_counter` (§3.15, §8.4). | research 03 §10; §8.4 |

**Recommendation, the project default:** a **scripted pseudo-currency shown through a scaled character modifier plus a story-cycle `basic_counter`**, with no `gui/` files (§3.15). Pick an engine currency only if its meaning genuinely matches, and prove it with a debug-decision probe first (influence: T11).

### Q3. What is the vassal relationship?
Paradox gives every distinct government a distinct vassal model (research 04 §2):
- contracts (feudal);
- tax jurisdictions (clan);
- appointed governors (admin);
- obedience and tributaries (nomad);
- tributaries over vassals (mandala).

Choose one of three:
- (a) **feudal-shaped tax and levy trees with your own numbers.** This is the minimum. It is *not* distinct.
- (b) **a contract whose obligation reads your resource**, e.g. the tribal shape that scales with liege prestige (`V/common/subject_contracts/contracts/tribal.txt:1`).
- (c) **a different subject type**: tributaries via `ask_for_tribute` (`GI:264-270`), or appointment (admin only, `GI:463-486`).

Also decide `opinion_of_liege` (`GI:516-530`), which is a per-government opinion term.

### Q4. What is the succession model?
- **Dynastic single heir or partition** is cheap and safe, and is the reuse path.
- **Elective** uses a title succession law plus `common/succession_election/`. Shape: `V/common/laws/01_title_succession_laws.txt:2-34`, `feudal_elective_succession_law`. The electors must be dynasty members or the player risks game over [inferred from P1].
- **Appointment** is admin-mechanic only (`00_law_triggers.txt:641-670`).

**The identity test:** if the fiction says "a board elects" or "no single head", single-heir inheritance contradicts it. Record that as a debt if you ship it anyway.

### Q5. What are the entry and exit transitions?
"Governments can only be changed via decisions" [web, research 04 §2]. Name:
- **The entry.** A decision that runs `change_government` (precedents: `convert_to_tribalism_decision` at `V/common/decisions/80_major_decisions.txt:473`, change at `:514`; `pam_convert_to_theocracy_decision` at `pam_decisions.txt:426`, change at `:569`; mandala at `tgp_east_asia_decisions.txt:57`). Grants to vassals are the other route (§3.14).
- **The exit.** A decision back to a vanilla or mod government (`convert_whole_realm_to_feudalism_decision` at `80_major_decisions.txt:348`; `mandala_adopt_clan_government_decision`; `return_to_the_steppe_decision` at `tgp_steppe_decisions.txt:243`, which refunds and tears down the government's assets).
- **The forced exit.** What happens on losing all land, dropping below a tier, or conquest by another government. Admin reverts to feudal below king tier [web].
- **What converts.** For the resource on entry and exit, follow the herd → treasury refund precedent: `nomad_convert_herds_to_treasury_or_gold_special_troops_effect`, used by `tgp_steppe_decisions.txt:1-210`.

### Q6. What does the AI do?
"Most AI/army behaviour is hardcoded" (skill `SKILL.md`, "What Script Can and Cannot Do"). The levers are:
- the `ai = { }` toggles (`GI:593-634`);
- `ai_will_do` on every law, decision, interaction and contract level;
- `grant_vassal_ai_will_do` (`GI:683-701`);
- `ai_ruler_desired_*_titles` (`GI:656-672`);
- contract `ai_liege_desire` / `ai_subject_desire`.

State how the AI gains the resource, how it spends it, and how it avoids bankruptcy and law churn. There is no per-government AI folder (research 02 §7).

### Q7. Where does the player see it (the UI surface)?
List every screen where the government shows. Free surfaces (§3.15): the name, icon, map colour, laws, contract window and rank names. **The resource display defaults to the no-GUI path**: a scaled modifier plus a story-cycle counter (§3.15). A persistent HUD readout is the opt-in upgrade through `gui/scripted_widgets/`. A government tab or a `hud.gui` change is new GUI work and needs an owner decision.

---

## 3. Build checklist, by surface

Each item lists what to supply, the path, the vanilla precedent, and the **minimum** ("min") and **full** versions. A **playable reskin** is every "min". A **distinct government** adds the "full" column wherever §2 said the verb differs.

### 3.1 The government block
**Path:** `common/governments/eotg_<gov>_government.txt`, one government per file (precedent: `eotg_pmc_government.txt`).

| Field | Closed set? | Min | Full | Precedent |
|---|---|---|---|---|
| `government_rules = { }` booleans | **Closed.** Only the `GI:13-309` keys, plus vanilla-used extras such as `allow_accolades` (`GT:11`). No new rules can be made. | P1, P2, P5 rules, `legitimacy = yes` (`GI:46-49`; v1 `no` silently inerted `add_legitimacy`) | add a rule only for a reused mechanic, e.g. `ask_for_tribute` (`GI:264-270`, mandala `GT:934`), `deny_powerful_vassal` (`GI:186-190`), `disable_regnal_numbers` (`GI:300-303`, celestial `GT:816`) | feudal `GT:5-62` |
| `mechanic_type`, `is_mechanic_type_default` | **Closed:** feudal, mercenary, holy_order, clan, theocracy, administrative, landless_adventurer, herder, nomad, mandala (`GI:311-346`). One default per type. | unset (republic, japan_feudal) | only to buy a coded mechanic, accepting its whole stack. `administrative` needs the `admin_gov` DLC flag (`GI:330`). | research 03 §9 |
| `primary_holding`, `valid_holdings`, `required_county_holdings` | Open keys from `common/holdings/` | copy a vanilla shape verbatim (§3.6) | own holding type (out of scope; map-wide) | `GI:382-400`; feudal `GT:18-20`, republic `GT:65-67` |
| `vassal_contract_group` | key into `common/subject_contracts/groups/` | own group (§3.3) | same | feudal `GT:22` |
| `royal_court` | **Closed enum:** none, any, top_liege, landed (`GI:447-455`) | `any` | — | feudal `GT:14` |
| `main_administrative_tier`, `min_appointment_tier`, `minimum_provincial_maa_tier`, `title_maa_setup` | **Closed enums.** Admin only (`GI:463-486`). | unset | admin mechanic only | admin `GT:455-470` |
| `house_unity`, `tax_slot_type`, `domicile_type` | keys into their databases (§3.9, §3.12) | unset | as designed | clan `GT:95-185`; `GI:500-513` |
| `currency_levels_cap` | **Closed keys:** piety, prestige, influence, merit; can only lower (`GI:568-579`) | unset | if the resource is one of the four | mandala `GT:1087`, celestial `GT:911` |
| `character_modifier`, `top_liege_character_modifier` | generic modifiers only (`GI:721-733`) | §3.13 | §3.13 | tribal `GT:213-228`, admin `GT:490-520` |
| `opinion_of_liege` (+ `_desc`), `opinion_of_suzerain`, `opinion_of_overlord` | script value | unset | the vassal model's opinion hook | `GI:516-566`; clan uses `opinion_of_liege` (research 02 §6) |
| `ai = { }`, `grant_vassal_ai_will_do`, `possible_grant_vassal_governments`, `ai_ruler_desired_*`, `ai_can_reassign_council_positions` | `ai` keys **closed** (`GI:593-634`; **`use_great_projects` rejected by the 1.20 parser**) | §3.14 | §3.14 | feudal `GT:24-26, 40-43` |
| `can_get_government`, `fallback`, `can_move_realm_capital` | trigger, int, trigger | §1 P7 | §1 P7 | `GI:348-380` |
| `court_generate_commanders`, `court_generate_spouses` (rule), `generated_character_template`, `supply_limit_mult_for_others`, `prestige_opinion_override`, `compatible_government_type_succession`, `blocked_subject_courts`, `max_dread` | various | unset | only with a stated reason | `GI:402-461, 581-586`; `max_dread` nomad `GT:665` (vanilla-only field) |
| `primary_heritages`, `preferred_religions` | culture/religion keys | **never** (project: map-agnostic, §4) | — | clan `GT:95-185` |
| `flags = { }` | **Open strings** (`GI:711-718`) | §3.2 | §3.2 | — |
| `color`, `realm_mask_offset`, `realm_mask_scale` | — | distinct from every vanilla colour (v1's Cartel copied tribal's) | — | feudal `GT:59-61` |

### 3.2 Flags: identity versus capability
Vanilla's own comment says "use flags instead of has_government for moddability" (`GT:25`, `GT:588`). `has_government` appears in only small numbers in vanilla, while `government_has_flag` appears in the hundreds (research 02 §0).

- **Identity flag (always):** `eotg_government_is_<gov>`. Every mod trigger reads it, never `has_government`. Each identity flag must be read by at least one trigger (no dead flags, robustness plan F5).
- **Family flag (optional):** e.g. `eotg_government_is_corporate`. Only with a named consumer.
- **Vanilla identity flags: never.** Above all `government_is_feudal`, which vanilla reads 369 times in 93 files: carrying it makes the government feudal in everything but name (`governments_v2.md` §5.0). Also never the four "unplayable" flags (P9).
- **Vanilla capability flags.** Opt in for each mechanic you want. Hit counts are from research 02 §0.

| Capability flag | Unlocks | Hits / where |
|---|---|---|
| `government_is_settled` | settled-ruler perks and effects | lifestyle_perks 13, scripted_effects 6 |
| `government_uses_domain_limit` | domain-limit perks; the mod's Unclaimed AI throttle reads it | lifestyle_perks 4 |
| `government_uses_crown_authority` | **the crown-authority law group** (`V/common/law_groups/00_realm_law_groups.txt:2`). Without it a ruler can never change succession law (`can_change_succession_laws` from crown authority 2, `00_realm_laws.txt:147`), and has no tributaries (`can_have_tributaries`, CA 1, `:64`) | load-bearing (`governments_v2.md` §5.0) |
| `government_uses_tribal_authority` | the tribal-authority law group (`00_realm_law_groups.txt:9`); wanua reuses it | `00_law_triggers.txt:193` |
| `government_has_influence` | the influence UI, interactions and buildings (Q2 caveat) | interactions 78, activities 58, great_projects 27, buildings 16 |
| `government_has_treasury`, `government_uses_salary_budget`, `government_uses_military_budget` | treasury budget laws | law_groups 3; laws 21 each |
| `government_uses_imperial_bureaucracy` | the imperial bureaucracy law group (`00_realm_law_groups.txt:29`) | law_groups 3 |
| `government_uses_administrative_house_aspirations` | admin house powers | house_aspirations 13 |
| `government_uses_admin_province_obligations` | admin province obligations | interactions 4 |
| `government_can_raid_rule` | raiding (tribal; v1 rejected it for the Cartel) | — |
| `cannot_be_vassal_or_liege` | fences the ruler out of all subject relations (mercenary `GT:344`, adventurer `GT:619`, Unclaimed) | — |

Flags read by the GUI are a fixed set (§3.15). A new mod flag gets no GUI.

### 3.3 The contract group and contracts
**Paths:** `common/subject_contracts/groups/eotg_<…>_contract_groups.txt`, `common/subject_contracts/contracts/eotg_<…>_obligations.txt`. **Spec:** `V/common/subject_contracts/contracts/_subject_contracts.info`.

- **Min:** one group with a tax tree and a levy tree, each with 5 levels chained by `parent`. Copy `subject_opinion`, `ai_liege_desire`, `ai_subject_desire`, `score` and `flag` by position from `feudal_government_levies` (`V/common/subject_contracts/contracts/feudal.txt:128-190`). Add the generic rights `war_declaration_rights`, `council_rights` and `title_revocation_rights` (`special_contracts.txt:476-580`). **Don't copy feudal's tax tree logic:** its AI desire branches on `government_is_feudal` (`feudal.txt:29-115`). Group shape: `V/common/subject_contracts/groups/subject_contract_groups.txt:1-15`.
- **Full:** at least one obligation that reads or moves the signature resource, with a consumer for its flag. Other options:
  - the tribal-style single non-negotiable level scaled by a liege value (`contracts/tribal.txt:1`);
  - a third obligation;
  - `modify_contract_layout` (`clan`, `admin`; assumed **closed** [inferred]).
- **Excluded by default:** `special_contract`, `fortification_rights`, `coinage_rights` (`government_is_feudal` ×10), `succession_rights` (needs confederate partition, `special_contracts.txt:443-446`), and the faith- and nomad-specific rights.
- **Gotchas:**
  - Per-government tax and levy modifiers (`<g>_government_tax_contribution_*`) are code-generated only for governments in `GOVERNMENT_TYPES` (P6). Vanilla declares feudal's and clan's in `V/common/modifier_definition_formats/00_government_definitions.txt:5-36, 142-176`.
  - The modify-contract interactions show for any government except admin and nomad (`V/common/character_interactions/00_modifiy_vassal_contract.txt:15-24, 327-337`).
  - **Tributary contracts are picked by the suzerain's government in a hard-coded branch list.** A mod government falls to the final `else`, `tributary_subjugated` (`V/common/scripted_effects/00_interaction_effects.txt:2981-2986`; `subject_contract_groups.txt:103-115`, `suzerain_heir_succession = no`). An own tributary group needs a key-level override of that effect (see `docs/pitfalls.md` §16 for the procedure).
- **Loc:** group `<grp>`, `<grp>_desc`; each contract; each level `<level>` and `<level>_short` (§3.16).

### 3.4 Realm law groups
- **Min:** reuse the crown-authority group through `government_uses_crown_authority` (§3.2).
- **Full:** an own law group gated by `required_government_flag = eotg_government_is_<gov>`, if the government has a policy axis. Precedents: `camp_purpose` (`00_realm_law_groups.txt:22-26`, laws `00_realm_laws.txt:801-1363`), `nomadic_authority` (`:35-37`), `mandala_decree` (`:50-53`).
- **Paths:** `common/law_groups/`, `common/laws/`. 1.20 laws carry `law_group_type` (CLAUDE.md placement).
- Every law needs `ai_will_do`. A missing trigger stops the AI picking one law [web, research 04 §4].

### 3.5 The succession gap
**The problem.** Vanilla succession laws whitelist government flags, so a new government gets none of them:
- partition and high partition need feudal, clan or japan_feudal (`00_law_triggers.txt:268-280`);
- single heir needs the culture innovation **and** a feudal, clan, admin, merit or japan_feudal government (`:343-397`);
- city succession needs `government_is_republic` (`:589-591`);
- appointment needs the admin mechanic (`:641-670`).

Title succession laws list feudal, clan and tribal (`V/common/laws/01_title_succession_laws.txt:7, 42-43, 79-81, 113-115, 147-149, 187-189`).

**The two ways out.**
- (a) **Own law(s)** in the vanilla group `succession_order_laws` (`V/common/law_groups/00_succession_law_groups.txt:1`), with `potential`/`can_have`/`can_keep`/`should_start_with` on the identity flag. Shape: `single_heir_succession_law`, `V/common/laws/00_succession_laws.txt:249-347`; built example: `common/laws/eotg_government_succession_laws.txt:25`.
- (b) **Carry a vanilla flag** the laws accept. Rejected for `government_is_feudal` (§3.2).

**Required with (a): a safety net.** The default law is "the first law in definition order whose `should_start_with` is true" (`V/common/laws/_laws.info:300-308`), so a vanilla law may be picked first. Add an additive `on_game_start` and `on_government_change` hook that runs `add_realm_law_skip_effects = <own law>` when the ruler lacks it. Vanilla forces laws the same way (`V/common/on_action/game_start.txt:2503`). Built example: `common/on_action/eotg_government_on_actions.txt:10-51`, `common/scripted_effects/eotg_government_effects.txt:14`.

**Min:** one order law per government. **Full:** an elective or distinct title succession law (Q4) plus `common/succession_election/`, with the gender law left vanilla. Clan's unity-stage laws (`V/common/house_unities/00_house_unities.txt:41-151`) are the precedent for succession tied to a resource.

### 3.6 Holdings and buildings
- **Min:** copy a vanilla shape verbatim.
  - **Castle shape:** feudal `GT:18-20`.
  - **City shape:** republic `GT:65-67`. **A playable city-primary government is untested in vanilla** (republic is blocked by the P0 blacklist). Check it in game (V-G17).
  - Never invent a mixed combination. v1's castle-primary plus city-valid appears nowhere in vanilla.
- Holding types: `V/common/holdings/00_holdings.txt` (castle `:2`, tribal `:55`, city `:84`).
- **Buildings** are gated by triggers inside each building, not by a government field:
  - `building_requirement_tribal` (`V/common/scripted_triggers/00_building_requirement_triggers.txt:5-13`);
  - admin buildings (`00_admin_buildings.txt:5-20`);
  - `government_has_influence` parameters (16 in `00_standard_economy_buildings.txt`);
  - `character_government_modifier` blocks (28 in `00_temple_buildings.txt`).
  - Castle, city and church buildings work for any government that isn't excluded.
- **Full:** government-gated buildings or a `character_government_modifier` keyed on the identity flag. **`buildings = no`** (`GI:278-282`) only for passive governments.

### 3.7 Men-at-arms, levies and knights
- Rules:
  - `regiments_prestige_as_gold` (`GI:35-39`, tribal `GT:190`);
  - `subject_men_at_arms` (`GI:153-156`; MAA types require `government_allows = subject_men_at_arms`, `V/common/men_at_arms_types/00_maa_types.txt:45, 94, 150, 214, 268`);
  - `use_maa_maintenance` (`GI:192-196`);
  - `conditional_maa_refill` (`GI:85-92`, performance warning).
- Admin title MAA comes only with the admin mechanic (`GT:455-470`).
- **Knights: there is no government gate**, only modifiers (`knight_limit`, `knight_effectiveness_mult`) (research 02 §4).
- **Min:** `character_modifier` lines such as `levy_size`, `men_at_arms_maintenance` and `knight_limit`.
- **Full:** a government-gated MAA type (`common/men_at_arms_types/`, trigger on the identity flag), or a resource-paid MAA rule if an engine currency fits (Q2).

### 3.8 Decisions, interactions and CBs
- **Gating:** the capability or identity flag in `is_shown`/`is_valid`. Nothing in vanilla is gated by the government key itself (research 02 §5).
- **Min:** none, plus debug decisions (`debug_only = yes`) for testing conversion in and out. Built example: `common/decisions/eotg_government_debug_decisions.txt:10-139`.
- **Full:**
  - one **entry** and one **exit** decision (Q5);
  - at least one **vassal-tier** and one **top-tier** decision that moves the resource (role-ladder rule, v1 lesson 4);
  - the interactions that express the core verb (admin: Bribe Officials, Force Abdication; mandala: Coerce Tributary; research 04 §2);
  - CBs only if the verb is a kind of war.
- Precedent files:
  - tribal: `00_tribal_interactions.txt:92, 233`;
  - clan: `00_unity_decisions.txt`;
  - admin: `dlc_decisions/ep_3/06_ep3_admin_decisions.txt:724, 1314`, CBs `07_ep3_admin_cbs.txt:354, 1629`.
- Paths: `common/decisions/`, `common/character_interactions/`, `common/casus_belli_types/`. Confirm the last one is in the CLAUDE.md placement table before use.

### 3.9 Domicile (optional)
- **Path:** `common/domiciles/types/` and `common/domiciles/buildings/` (not yet in the CLAUDE.md placement list). Field `domicile_type` (`GI:508-513`).
- Vanilla types: camp (`00_domicile_types.txt:1`), estate (`:1032`), yurt (`:1955`), east_asian_estate (`:2101`), japanese_manor (`10_tgp_japan_domicile_types.txt:1`).
- **Open:** the type key, slots and buildings. **Closed:** the resource booleans (only `herd`, `provisions`, `culture_and_faith`).
- **GUI (answered, §8.3):** `gui/window_domicile.gui` tests the government **by name** only to pick the Asian or Western art set:
  - frame `:283/:295`;
  - header `:377/:445`;
  - the other pairs `:549/:558`, `:646/:654`, `:2119/:2127`.

  **An unlisted government falls into the Western branch** and takes its icon, illustration and name from its domicile type, so the window doesn't break. A mod government with `mechanic_type = nomad` gets mixed chrome, because `:283` checks the mechanic while `:377+` check the name. The Asian frame would need a `window_domicile.gui` override, so don't aim for it.
- **Pitfall:** when a domicile is created by `create_nomad_title`, its line of succession is reported to appear for a custom government only if the government has `uses_county_fertility = yes` (forum bug report, §8.3). Test succession in any created domicile (T13).
- A new domicile type needs its own `icon`, `illustration` and `map_pin_texture` (shape: camp, `00_domicile_types.txt:1`; spec `_domicile_types.info`).
- Recommend a domicile only when the core verb is "move" or "estate" (Q1), or when herd or provisions is the chosen currency.

### 3.10 Situation (optional)
- **Path:** `common/situation/situations/`. **Spec:** `_situations.info`.
- Phases, participant groups and `on_*` effects are open data.
- The `window =` enum is **closed** (situation, the_great_steppe, silk_road, dynastic_cycle, the_christian_church; vanilla uses `christian_church` at `pam_christian_situation.txt:10`, a `.info` discrepancy). `gui_window_name` can point at any widget. Precedent: `the_great_steppe.txt:9-14`.
- Use it only for a region-wide, multi-ruler process. It needs region keys, so it **conflicts with map-agnostic** (§4) until Gate 1. Defer it.

### 3.11 The currency
- **Engine currency:** the effects are `change_merit` (`V/common/scripted_effects/00_casus_belli_effects.txt:103`, guarded by `government_allows = merit`), `change_influence`, `add_treasury` / `add_treasury_or_gold`, and `domicile = { change_herd / change_provisions }`. The flows are modifiers (`monthly_merit`, `monthly_influence`, `domicile_monthly_herd_add`, …). The cost keys are `influence =`, `merit =`, `treasury =`, `herd =` (`V/common/scripted_costs/00_costs.txt:700+`) (research 03 §0).
- **Scripted currency (project default):**
  - a character variable `eotg_<gov>_<resource>`, set on every ruler of the government at every tier;
  - **one** change effect, `eotg_<gov>_change_<resource>_effect`, that clamps the value (no other code writes it);
  - a script value for derived numbers;
  - display through the §3.15 default: a scaled character modifier plus a story-cycle `basic_counter`;
  - `ai_will_do` terms that read it;
  - initialization in `eotg_gov_on_game_start` and `on_government_change`;
  - teardown on exit.
- **Min:** the variable, the change effect, the init and teardown hooks, and the scaled modifier (display layer 1, §3.15).
- **Full:** at least two sources and two sinks the player chooses between, a level or band ladder, and a read in a contract or law.

### 3.12 House unity, tax slots and house aspirations (only if used)
- **`house_unity = <key>`** (`GI:500-505`): clan `GT:95-185` → `V/common/house_unities/00_house_unities.txt:1`. Stages carry `on_start`, parameters and `succession_law_flag`.
- **`tax_slot_type`:** clan only, `V/common/tax_slots/types/00_tax_slot_types.txt:3`. **Not in `GI`**, so it is a vanilla-only field. It also forces a tax-collector contract (`contracts/clan.txt:1`) and `modify_contract_layout = clan`.
- **House aspirations:**
  - the rule `house_aspirations` (`GI:215-219`);
  - admin: the flag `government_uses_administrative_house_aspirations` with data in `V/common/house_aspirations/00_admin_house_powers.txt`;
  - mandala: aspects in `tgp_mandala_devaraja_aspects.txt`.
- Each of these brings a code-driven UI built for its vanilla government. Treat them as **full-only** and **probe first**. None of the three folders is in the CLAUDE.md placement list yet.

### 3.13 `character_modifier`
- `character_modifier` and `top_liege_character_modifier` (`GI:636-645`) accept **generic modifiers only**, or ones generated from schemes, holdings, lifestyles and regions. Modifiers generated by other governments, MAA types, cultures or terrain aren't allowed (`GI:721-733`).
- **Min:** 2–4 lines that express identity without becoming the identity (balance check in V-G12).
- **Full:** a `top_liege_character_modifier` for the independent ruler (tribal `GT:213-228`).

### 3.14 The AI block and grants
- **`ai = { }`:** only `use_lifestyle`, `arrange_marriage`, `use_goals`, `use_decisions`, `use_scripted_guis`, `use_legends`, `perform_religious_reformation` (`GI:593-628`). **Never `use_great_projects`**: the 1.20 parser rejects it even though `GI:630` documents it (CLAUDE.md, 2026-10-08).
- **Grants:**
  - `possible_grant_vassal_governments` (`GI:674-681`) is set on the *liege's* government and lists what it may grant;
  - `grant_vassal_ai_will_do` (`GI:683-701`) is set on the *granted* government;
  - precedents: feudal `GT:40-43`, nomad `GT:725`.
  - Without these, what government a newly landed vassal gets is engine-chosen (V-G10, [engine, unverified]).
- **Min:** `use_legends = yes` and `ai_will_do` on every own law and contract level.
- **Full:** `grant_vassal_ai_will_do`, `ai_ruler_desired_*_titles` if the government shouldn't hoard titles, and resource-aware `ai_will_do` on every decision.
- **Accept** that war, army and most diplomacy AI is hard-coded (skill `SKILL.md`).

### 3.15 GUI
- **Free with no GUI file:**
  - the name and icon in the character and realm windows;
  - the map-mode colour (`color`, `realm_mask_*`);
  - the law window;
  - the contract modify window, through `modify_contract_layout` or the default;
  - rank names (flavourization, §3.18);
  - modifiers in the character window (research 02 §8).
- **Not free:**
  - `HasGovernmentFlag` branches in GUI read only vanilla flags (`government_has_influence`, `_has_treasury`, `_is_tribal`, `_is_theocracy`, `_is_ecclesiastical`, `_is_herder`, `_is_mandala`);
  - `IsAdministrativeRuler` drives the admin-only windows (`window_government_administration.gui`, `window_admin_vassal_detail.gui`, `window_title_appointment.gui`, `window_treasury_budget_change.gui`);
  - `window_domicile.gui` branches by government name, cosmetically (§3.9);
  - the top-bar influence widget keys on `HasMechanic('administrative')` (`V/gui/hud.gui:7025`);
  - radiance's HUD button binds to engine data (`Character.GetRadianceBreakdown`, `V/gui/hud.gui:3507-3540`), not to a script value, so it isn't a pattern to copy.
- **Displaying a scripted resource: the ladder, least invasive first.** Use as many layers as the design needs, from the top down.
  - **The default is layers 1 + 4, with no `gui/` files.** This settles the "the mod ships no `gui/` folder" question with a default.
  - Layer 5 is the opt-in upgrade and needs an owner decision.

| # | Layer | How | Precedent | Cost |
|---|---|---|---|---|
| 1 | **Scaled character modifier** (default) | A static modifier, added on entry, carrying `scale = { value = <script value> desc = <loc> display_mode = scaled }`. The character window's modifier row and its tooltip show the live value. | `V/common/modifiers/00_court_position_modifiers.txt:138-141`, `00_diarchy_modifiers.txt:159` | None beyond one modifier, one script value and one icon (modifier art, 60 × 60). |
| 2 | **Loc that prints the value** | `[GetPlayer.MakeScope.Var('eotg_<gov>_<res>').GetValue\|0]` or `[Character.MakeScope.Var(...)]` in decision descs and tooltips. A decision whose desc shows the value and its thresholds works as a pseudo-panel. `ScriptValue` in loc is global only (`EmptyScope.ScriptValue`). | `V/localization/english/activities/coronation_activity_l_english.yml:675-677, 705`; `modifiers/modifiers_l_english.yml:1368` | None |
| 3 | **Customizable loc bands** | Text per band ("Strong", "Shaky") in `common/customizable_localization/`, read from the variable | Already in this mod's placement table | None |
| 4 | **Visible story cycle with a `basic_counter`** (default) | One `visible = yes` story per ruler of the government, with `visualization = { basic_counter = { variable … min max label } }`. **The variable must live on the story scope**, so either the change effect writes the story's copy or the story is the sole owner of the value. | `_story_cycles.info:23, 58-110`; `V/common/story_cycles/book_translation_story_cycle.txt:2, 10-14`. This mod's `common/story_cycles/eotg_aug_kingpin_story.txt:46-55` already uses `visible`, `icon`, `background` and `visualization`. | Low. Tiger reports the 1.20 story fields, which are known benign (CLAUDE.md). |
| 5 | **`gui/scripted_widgets/`** (opt-in) | A text file mapping `gui/eotg_<x>.gui = eotg_<widget>`. The engine creates the widget at map load without editing any vanilla `.gui`, and "multiple mods can load their own widgets". Pair it with a `common/scripted_guis/` entry for visibility (the government gate). | `V/gui/scripted_widgets/_scripted_widgets.info`; wiki https://ck3.paradoxwikis.com/Interface | Medium: new `gui/` and `scripted_guis/` placement entries, widget art, and a risk of overlapping the outliner. |
| 6 | **`hud.gui` / `window_character.gui` override** (last resort) | Override the file or inject a type | Wiki Interface page | High: a wholesale override of vanilla UI, re-diffed every patch (`docs/pitfalls.md` §2) |

- Vanilla `scripted_gui` examples are only visibility and validity gates (`V/common/scripted_guis/pam_scripted_guis.txt:2-8`). None shows a value, so layer 5 is new ground for this project.

### 3.16 Loc keys (full list)
**Path:** `localization/english/eotg_<gov>_l_english.yml`, UTF-8 with exactly one BOM, Canadian English, bare `[x.GetName]`. Key shapes copy `V/localization/english/government_l_english.yml` (feudal `:2-7`).

| Key | Note |
|---|---|
| `<g>`, `<g>_adjective`, `<g>_realm`, `<g>_desc` | name, adjective, realm noun, 2–4 sentence desc naming no nation |
| `<g>_with_icon` | `@government_type_<…>! $<g>$` (§3.17) |
| `<g>_filter_option`, `<g>_filter_option_desc` | character finder |
| `<g>_obligations`, `<g>_vassals_label` | contract UI |
| `<g>_vassal_opinion`, `<g>_opinion`, `<g>_tax_contribution_add`, `<g>_tax_contribution_mult`, `<g>_levy_contribution_add`, `<g>_levy_contribution_mult` | **engine-generated modifier names** (exist only with P6) |
| flag labels `<flag>` | only if a flag is shown in tooltips (vanilla `:272-285`) |
| `GAME_OVER_CANNOT_PLAY_<X>`, `NOT_GAME_OVER_CANNOT_PLAY_<X>` | **only for a deliberately unplayable government** (P0). Shape: `V/localization/english/gui/ingame_main_l_english.yml:83-84` (`"Cannot play [republics\|E]"`, and the `NOT_` key as `"$GAME_OVER_CANNOT_PLAY_REPUBLIC$"`). The key itself carries no `eotg_` prefix by vanilla convention; use `<X>` = `EOTG_<GOV>`. |
| `opinion_of_liege_desc` text | if §3.1 sets it |
| per law: `<law>`, `<law>_subname`, `<law>_effects` | shape `succession_laws_l_english.yml:14-16` |
| per contract group: `<grp>`, `<grp>_desc` | |
| per contract: `<contract>`; per level `<level>`, `<level>_short` | shape `feudal_government_levies` |
| flavourization keys (§3.18) | one per entry |
| knight term keys (§3.21) | 8 per term |
| decisions, interactions, the scaled resource modifier (`<mod>`, `<mod>_desc`, the `scale.desc` key), the story-cycle counter label, events | `_t`/`_desc`/`_a` per project convention; `eotg_<ns>_NNNN_*` |

**Icon:**
- `gfx/interface/icons/government_types/<g>.dds`, 70 × 70 with transparency;
- **a small painted object**, usually headgear, about 60% of the square, with a soft dark outline (art check 2026-10-11, `C:/Users/river/Desktop/EotG_Art_Needed.md` §5);
- until the art lands, a copied vanilla icon is the placeholder (`gfx/interface/icons/government_types/README.txt`);
- a **missing** file renders blank (the Unsworn icon today).

### 3.17 Text icons
- Vanilla defines them in `gui/texticons.gui` (admin `:4647`) as `government_type_<x>`.
- **Min:** reuse a vanilla text icon in `<g>_with_icon` (precedent: `@government_type_herder!` for Unclaimed). Confirm the icon key exists.
- **Full (answered, §8.2):** an own text icon in **the mod's own `gui/eotg_texticons.gui`**, holding only `texticon = { }` blocks.
  - Vanilla already splits text icons across several files (`texticons.gui`, `texticons_legitimacy.gui`, `texticons_religion.gui`), so the engine merges them.
  - **Never name a mod file `texticons.gui`.** The same path replaces vanilla's whole file.
  - Copy the shape of `V/gui/texticons.gui:4704-4711`:
    `texticon = { icon = government_type_eotg_<gov> iconsize = { texture = "gfx/interface/icons/government_types/eotg_<gov>_government.dds" size = { 28 28 } offset = { 0 6 } fontsize = 16 } }`
  - `<g>_with_icon` then uses `@government_type_eotg_<gov>!`. Per the art check, the same 70 × 70 image serves.
  - `gui/` needs a placement-table entry. Never `replace_path` `gui/`. Confirm in game (T12).

### 3.18 Flavourization
- **Path:** `common/flavorization/eotg_<…>_flavorization.txt`. **Shape:** `V/common/flavorization/00_title_holders.txt` (`count_feudal_male` `:8518-8525`, `county_feudal` `:8534-8539`, republic `top_liege = no` `:3415-3426`, admin `priority = 50` `:10419-10428`). Field spec: skill `reference/common/flavorization/_flavourization.info`.
- **Min:**
  - title rank (5 tiers);
  - vassal rank (5 tiers × 2 genders, `only_vassals = yes`);
  - top rank (county to empire × 2, `only_independent = yes`, priority one above).
  - All entries need `governments = { <g> }`, `flavourization_rules = { top_liege = no }` (the character's own government counts), priority ≥ 60, and no `name_lists` or `heritages`.
- **Full:** domicile and contract flavourization (`01_domicile.txt`, `02_vassal_contracts.txt`).
- **Glossary guard:** no rank word may be a tier word (System, Region, Sector, Expanse, Cluster).

### 3.19 on_actions
- **Additive only** (invariant 4). Hooks:
  - `on_government_change`, root = character, `scope:old_government` (`V/common/on_action/government_on_actions.txt:4`);
  - `on_game_start` (`game_start.txt`);
  - `on_liege_government_change` (`ep3_on_actions.txt:214`).
- **Min:** extend the shared `eotg_gov_on_game_start` / `eotg_gov_on_government_change` (`common/on_action/eotg_government_on_actions.txt:24, 43`) with a branch per government: the succession safety net plus resource init and teardown. Teardown reads `scope:old_government`.
- **Full:** pulse content on `yearly_playable_pulse` (**not** `on_yearly_playable`, `docs/pitfalls.md` §12), one mod on_action per government:
  - Section A: any tier, role trigger;
  - Section B: top tier;
  - **the cooldown lives in the on_action only.**

### 3.20 The defines entry
Covered by P6. Add the key to **both** define files in the same commit, and re-diff vanilla's 20 against ours after every CK3 patch.

### 3.21 The knight term (project rule CB-48: never hard-code "knight")
- The term comes from the key-level override of `KnightCulture` in `common/customizable_localization/eotg_knight_culture.txt`, one `text = { trigger = { eotg_gov_knight_realm_is_<gov> = yes } … }` per government before the `knight_default` fallback.
- The trigger lives in `common/scripted_triggers/eotg_government_triggers.txt`. It is the ruler's own flag, or an unlanded character's employer's.
- Vanilla's 7 children inherit through `parent =` (`V/common/customizable_localization/00_knight_culture.txt:91-123`), so only the parent is redefined.
- **Loc:** 8 keys per term (`<term>`, `_plural`, `_no_tooltip`, `_no_tooltip_plural`, `_no_tooltip_lowercase`, `_no_tooltip_lowercase_plural`, `_no_tooltip_lowercase_plural_possessive`, `_no_tooltip_lowercase_adjective`). Shapes: `knight_culture_l_english.yml:30-31, 67-70, 96-97`.
- **All mod text** uses `Custom('KnightCulture…')` on the realm owner.
- **The term is an owner ruling.** Check that it doesn't collide with vanilla concepts (agent) or canon organizations (Enforcer).

---

## 4. Project rules overlay

1. **Prefix.** Every key is `eotg_` (invariant 1): `eotg_<gov>_government`, `eotg_government_is_<gov>`, `eotg_<gov>_vassal`, `eotg_<gov>_succession_law`, `eotg_knight_<term>`, `eotg_<gov>_<resource>`. Landed titles are never involved (`grep -rnE 'eotg_[ekdcb]_'` stays empty).
2. **Map-agnostic.** No title, province, culture, faith or character key in any government file. No `primary_heritages` or `preferred_religions`. No region-bound situation before Gate 1. The CLAUDE.md exemption for the PMC, Corporation, Cartel and Gob-Corp governments rests on this, and a new government only gets the same exemption if the owner grants it.
3. **No vanilla-key dependencies in triggers.** Read identity and capability flags, never `has_government = <vanilla>` or culture or faith keys. Vanilla `KnightCulture` blocks that name real-world cultures are dropped for the same reason.
4. **Testing.** Assignment goes in history data in the British Isles sub-mod (`docs/test_submods/british_isles/isles_assignments.csv`, cartographer). Bookmarks there need vanilla portraits, so the default is to pick on the map. Test setups are generated, validated and installed for the owner (memory, "hands-off setup").
5. **Tiger and PX:**
   - Tiger 1.17 and PX don't validate 1.20 government fields. **QA checks every government block by hand** against `GI` and a vanilla call site.
   - Known noise (CLAUDE.md): the `missing-item` on 1.20 law-group laws (shown for `eotg_aug_policy_*`; expect the same for new law groups), and the `rite` / `change_spiritual_fulfillment` / prison and kinslayer path families.
   - Write Tiger logs to the scratchpad.
6. **"A field only in `.info` is not proof."** Every field needs a vanilla `.txt` call site or an error.log-clean in-game load (`use_great_projects` lesson). The reverse also holds: vanilla-only fields (`vassal_contract_group`, `tax_slot_type`, `allow_accolades`, `max_dread`) are valid even though `GI` omits them.
7. **Signature resource rule.** No flavour event ships that neither moves nor reads the resource (invariant 5, v1 lesson). New events need owner approval (memory, "event expansion").
8. **Lore.** Precedence ERRATA → dated `docs/lore` → `866_bookmark_design.md` → SETTING LORE body. `NATIONS_AT_866_AG.md` is non-canon. Government text names no nation or person. Apply the B2 banned-vocabulary list where relevant. Canadian English.
9. **Placement.** Folders this template names that are **not** yet in the CLAUDE.md placement list (`common/domiciles/`, `common/house_unities/`, `common/tax_slots/`, `common/house_aspirations/`, `common/situation/`, `common/succession_election/`, `common/men_at_arms_types/`, `common/scripted_guis/`, `gui/`) need an orchestrator entry before first use. Never `replace_path` any of them.
10. **Save compatibility.** Treat any change to a shipped government's key, flags, contract group or laws as save-breaking (project practice; other mods are observational only and are not cited, owner rule 2026-10-11). Note it in the commit and taskboard.

---

## 5. Validation and test plan

### 5.1 Static (eotg-qa)
1. Tiger is clean except the CLAUDE.md known-benign list.
2. `px_lsp_diagnostics.js common events localization` is clean. `px_vocab_check.py common events` is clean, and it must flag no unknown on_action hooks. The PX `eventGraph` + `locCoverage` report shows no missing `eotg_` loc and no unreachable event.
3. **Hand check** of every government block against `GI` and the cited vanilla lines (§3.1 table), field by field. Every field has a vanilla call site.
4. The new key is present in **both** `GOVERNMENT_TYPES` copies, and the vanilla 20 there match the installed `00_defines.txt:550-573`.
5. The identity flag is read by at least one trigger. No `has_government` in mod script. No title, culture or faith keys (`grep`).
6. The loc file has exactly one BOM and no `[scope:`, and every §3.16 key is defined once across the tree, `replace/` included.
7. Every own law, contract level and decision has `ai_will_do`.
8. **The playable blacklist:** `grep -n "government_is_" common/governments/eotg_<gov>_government.txt` shows none of the P0 flags outside comments. A government meant to be unplayable has its `GAME_OVER_CANNOT_PLAY_*` entry and its two loc keys.

### 5.2 In game (human, `-debug_mode`, British Isles sub-mod)
| ID | Check | Pass |
|---|---|---|
| T1 | **Bookmark or map start.** The ruler can be picked and played. No `GAME_OVER_CANNOT_PLAY_*` tooltip appears and the lobby doesn't say "Is unplayable". The start doesn't remap the government. | yes |
| T2 | **Load.** error.log has nothing from the new files: no "preregistered modifier type", no "Unexpected token". `database_conflicts.log` shows only the intended key overrides (`KnightCulture`, any `pitfalls.md` §16 trigger). | yes |
| T3 | **Succession across a death.** `kill` the ruler. The heir is in the dynasty, keeps the government, has the own succession law, and play continues. Repeat with a female or minor heir under the vanilla gender law. | yes |
| T4 | **Erosion.** Give a title of this government to a landed feudal relative (`kill` the ruler with that relative as heir) and record the government of the result. | recorded |
| T5 | **AI vassals.** Vassals show the government's contract trees with loc. An AI liege changes a level within 20 years. Granting a county to a courtier: record the new vassal's government. | yes / recorded |
| T6 | **Conversion in and out.** Debug decisions turn a feudal ruler into the government and back. The law is added on entry and dropped on exit (`can_keep`). The resource is initialized on entry and cleared on exit. No orphan modifiers remain. | yes |
| T7 | **Leakage.** After a 50-year observer run, the government map mode shows it only in seeded realms and their grants or conquests. If not, build the P7 guard. | yes |
| T8 | **50-year AI health.** No ruler without a valid succession law, no permanent bankruptcy, no law churn. The resource stays inside its clamp and moves both ways. | yes |
| T9 | **Surfaces.** Rank names (independent top rank at any tier), the knight term in the Knights tab and in lowercase, plural and possessive lines, the map colour, the icon, the text icon, and the resource display. | yes |
| T10 | **Save compatibility.** Save in year 1, load the save after a no-op rebuild, and confirm the government, law and resource survive. After any change to the government definition, record whether old saves load. | yes / recorded |
| T11 | **Influence on a non-admin government** (only if Q2 picks influence). Give a test government `government_has_influence`, no administrative `mechanic_type`, and a `monthly_influence = 1` modifier. After 3 months, record: (a) the top bar (expected absent, `hud.gui:7025`); (b) the character-window influence row; (c) the influence value in the character debug view; (d) whether `change_influence` and `influence >= X` work and an influence-cost interaction is usable; (e) error.log. | Recorded. Influence is usable only if (b)–(d) pass. |
| T12 | **Custom text icon.** Ship `gui/eotg_texticons.gui` with one `government_type_eotg_<gov>` block and use it in `<g>_with_icon`. It renders in the character window and in a tooltip; vanilla `@gold_icon!` and `@government_type_feudal!` still render; error.log has no texticon line. | yes |
| T14 | **Unplayable on purpose** (only if P0 adds an entry). Try to pick a ruler of the government: the pick is refused with the `GAME_OVER_CANNOT_PLAY_<X>` text. `database_conflicts.log` shows which file won `is_character_allowed_to_be_player`, which settles the same-key-in-another-file question. Every vanilla blacklist entry still applies: a republic is still refused. | yes |
| T13 | **Resource display and domicile** (where used). The scaled modifier shows the live value and moves when the change effect runs, and the story-cycle `basic_counter` matches it. If a domicile is used: the window opens in the Western frame with the type's icon and illustration, and the domicile shows a line of succession after the holder dies. | yes |

---

## 6. Gap check: the four governments against this template

Sources: the files under `common/` (line numbers below), `governments_v2.md`, and CB-49 (in-game checks still waiting on the human). "Met (untested)" means it is built and its in-game check hasn't run yet. Column order follows the request.

| Requirement | PMC | Corporation | Cartel | Gob-Corp (Trade Oligarchy) |
|---|---|---|---|---|
| P0 not on the playable blacklist (`V/common/scripted_rules/00_rules.txt:151-249`) | met: the only vanilla flag is `government_is_settled` (`pmc:58`) | met (`corp:58`; `government_is_republic` appears only in a comment, `:14`) | met (`cartel:68`) | met (`gobcorp:59`; republic only in a comment, `:15`) |
| P1 dynastic rules | met, `eotg_pmc_government.txt:24-25` | met, `eotg_corporation_government.txt:25-26` | met, `eotg_cartel_government.txt:35-36` | met, `eotg_gobcorp_government.txt:25-26` |
| P2 `inherit_from_dynastic_government` default | met (unset) | met (unset) | met (unset) | met (unset) |
| P3 valid succession law | met (untested V-G4), `common/laws/eotg_government_succession_laws.txt:25` | met (untested), `:57` | met (untested), `:121` | met (untested), `:89` |
| P5 heir keeps government | met (untested V-G9), `pmc:29-30` | met (untested; Konan test), `corp:30-31` | met (untested), `cartel:40-41` | met (untested), `gobcorp:30-31` |
| P6 `GOVERNMENT_TYPES` | met, `common/defines/eotg_government_defines.txt:42` (+ sub-mod copy) | met, `:43` | met, `:45` | met, `:44` |
| P7 `can_get_government` / fallback | partial: deliberately unset, leakage untested (V-G11); guard drafted in `governments_v2.md` §5.6 | partial: same | partial: same | partial: same |
| P8 bookmark / ruler designer | missing: map pick only (`governments_v2.md` §12); sub-mod bookmarks list none | missing | missing | missing |
| T1 played in game | unverified (CB-49) | unverified; city shape V-G17 | unverified | unverified; city shape V-G17 |
| Identity flag, no vanilla identity flag | met, `pmc:57` | met, `corp:56-57` (+ reserved family flag) | met, `cartel:67` | met, `gobcorp:57-58` |
| Capability flags (settled, domain limit, crown authority) | met, `pmc:58-60` | met, `corp:58-60` | met, `cartel:68-71` | met, `gobcorp:59-61` |
| Q1 distinct core verb | **missing**: modifiers only (`pmc:43-50`); nothing sells force | **missing** | partial: tribute via `ask_for_tribute` (`cartel:42-43`) | **missing** |
| Q2 / §3.11 signature resource | **missing**: `eotg_pmc_standing` reserved, not built (`governments_v2.md` §2) | **missing**: `eotg_corp_board_influence` reserved | partial: vanilla dread with gain and decay modifiers (`cartel:58-59`), no unique sink | **missing**: `eotg_gobcorp_market_share` reserved |
| Q3 / §3.3 distinct vassal model | partial: own group (`groups/eotg_government_contract_groups.txt:17`), feudal levy-tree shape | partial, `:27` | partial, `:47`; tributaries are vanilla `tributary_subjugated` (lapse on death) | partial, `:37` |
| `opinion_of_liege` | missing (deferred, `governments_v2.md` §15) | missing | missing | missing |
| Q4 succession fits identity | partial: single heir (command succession is G2) | **conflict**: dynastic single heir for a board-run state | partial: fits "top under threat" loosely | **conflict**: single heir for "no single head" |
| Q5 entry / exit transitions | missing: debug decisions only (`common/decisions/eotg_government_debug_decisions.txt:10`) | missing (`:42`) | missing (`:106`) | missing (`:74`) |
| §3.4 realm laws | met (min): crown authority; no own group | met (min) | met (min) | met (min) |
| §3.6 holdings | met: castle shape `pmc:37-39` | met (untested): city shape `corp:38-40` | met: castle `cartel:49-51` | met (untested): city `gobcorp:38-40` |
| §3.7 MAA / levies / knights | partial: `knight_limit`, MAA maintenance, merc cost, commanders (`pmc:43-50`) | partial: `levy_size` (`corp:48`) | missing: no military identity beyond dread | partial: MAA maintenance (`gobcorp:47-48`) |
| §3.8 decisions / interactions / CBs | missing | missing | partial: vanilla Offer Tributary Status (piety cost) | missing |
| §3.13 `character_modifier` | met `pmc:45-50` | met `corp:44-49` | met `cartel:55-60` | met `gobcorp:44-49` |
| `top_liege_character_modifier` | missing (optional) | missing | missing | missing |
| §3.14 AI block / grants | partial: `use_legends` only (`pmc:52-54`); no `grant_vassal_ai_will_do` / `possible_grant_vassal_governments` | partial (`corp:51-53`) | partial (`cartel:62-64`) | partial (`gobcorp:51-54`) |
| §3.15 resource UI | missing (no resource) | missing | partial: dread's vanilla UI | missing |
| §3.16 loc | met, `localization/english/eotg_government_l_english.yml:2-16` | met, `:17-31` | met, `:47-61` | met, `:32-46` |
| §3.16 icon | partial: vanilla mercenary copy (`gfx/interface/icons/government_types/README.txt`) | partial: admin copy | partial: clan copy | partial: republic copy |
| §3.17 text icon | partial: borrowed `@government_type_mercenary!` (loc `:6`) | partial: borrowed admin (`:21`) | partial: borrowed clan (`:51`) | partial: borrowed republic (`:36`) |
| §3.18 flavourization | met, `common/flavorization/eotg_government_flavorization.txt:27` ff. | met, `:313` ff. | met, `:885` ff. | met, `:599` ff. |
| §3.19 `on_government_change` | met, `common/on_action/eotg_government_on_actions.txt:18-22, 43-51` (succession only; no resource init) | met (same) | met (same) | met (same) |
| §3.21 knight term | met, `common/customizable_localization/eotg_knight_culture.txt:31` (Operator) | met, `:37` (Specialist) | met, `:49` (Brute) | met, `:43` (Strongarm) |
| Map colour distinct | met (V-G18 pending), `pmc:64` | met, `corp:64` | met, `cartel:75` | met, `gobcorp:65` |

### 6.1 Top gaps per government (what stops each from feeling distinct and playable)

All four are **playable reskins of feudal** by this template's definition. The G1 scope intended exactly that, and `governments_v2.md` §1 says so. The gaps below are what G2 must close. Recommendations only; nothing here is built.

**PMC**
1. **No core verb.** Nothing a player does sells force. Recommendation: a contract loop as the G2 P1 decision pair: a top-tier "take a contract" decision and a vassal-tier "deliver" decision that move `eotg_pmc_standing`. Have eotg-vanilla-scout check whether the landless-adventurer `common/task_contracts/` system can be offered to a landed government before scripting a substitute [inferred].
2. **No resource**, so invariant 5 has nothing to bind G2 events to. Build the variable and change effect first (G2 P1).
3. **The vassal model is feudal with lower tax.** Recommendation: a third obligation, "field commission", whose flag a decision reads.
4. **No entry path.** Add the PMC → Corporation evolution decision (`governments_v2.md` §14.1 P3) and a feudal → PMC adoption decision.

**Corporation**
1. **Succession contradicts the fiction.** A board-run state passes by single-heir inheritance. Recommendation: the G2 P2 elective title law, with electors limited to the ruler's dynasty and house (P1-safe), and board influence as vote weight.
2. **No resource.** Influence on a non-admin government gets no top-bar widget (§8.1), so it isn't "UI for free". Recommendation: the scripted `eotg_corp_board_influence` with the §3.15 default display. Run T11 only if the owner still wants vanilla influence.
3. **No core verb or decisions** ("deals"). Recommendation: one vassal-tier and one top-tier decision that move `eotg_corp_board_influence`.
4. The city-primary shape is unverified (V-G17).

**Cartel** (the closest to distinct)
1. **Dread has no sink unique to the Cartel.** Recommendation: G2 decisions that spend dread, e.g. collect tribute early or make an example of a vassal, so dread is spent as well as gained.
2. **Tribute lapses on the ruler's death** (`tributary_subjugated`, `suzerain_heir_succession = no`). Accepted for G1. If the V-G12 churn is bad, add an own tributary group plus an override of the `00_interaction_effects.txt:2981-2986` branch.
3. **"The top is always under threat" has no mechanic.** Recommendation: a takeover title succession or a Cartel faction (`governments_v2.md` §14.1 P2/P3).
4. **No military identity.** Optional.

**Gob-Corp (Trade Oligarchy)**
1. **Succession contradicts "no single head".** Recommendation: a wealth-weighted elective law, with market share as vote weight (G2 P2).
2. **No resource.** `eotg_gobcorp_market_share` is reserved and unbuilt. Its natural consumer is the Frontier trade network.
3. **No core verb.** Competing for market share needs decisions against other Princes (a CB or a scheme, G2 P3).
4. The city-primary shape is unverified (V-G17).

**Cross-cutting:**
- none of the four has entry or exit decisions, `grant_vassal_ai_will_do`, `opinion_of_liege` or real art;
- the whole in-game V-G list (CB-49) is still unrun, so every "met" for P3, P5 and T1 is unproven;
- no resource display exists yet. The §3.15 default (a scaled modifier plus a story-cycle counter) needs no GUI, so G2 P1 can start without a GUI decision.

### 6.2 Gap outside the four: Unsworn (`eotg_unclaimed_government`) is playable
- **Finding.** Unsworn carries `eotg_government_is_unclaimed` and `cannot_be_vassal_or_liege` (`common/governments/eotg_unclaimed_government.txt:77-83`), and neither is on the P0 blacklist. Each placeholder holds a county, so it passes `is_playable_character` (`V/common/scripted_triggers/00_available_for_events_triggers.txt:964-980`). **A player can therefore pick an Unsworn placeholder.**
- **Why it matters.** It has `rulers_should_have_dynasty = no` and `inherit_from_dynastic_government = no` (`:35-38`). It is a passive stand-in, "not a ruler" (`:3-4`), with no council, no buildings and `monthly_income_mult = -10`. Playing one is a dead end, and its death likely ends the game, because the heir is non-dynastic [inferred].
- **Options:**
  - (a) **Add a GAME_OVER entry.** Override `is_character_allowed_to_be_player` with `custom_description = { text = "GAME_OVER_CANNOT_PLAY_EOTG_UNCLAIMED" NOT = { government_has_flag = eotg_government_is_unclaimed } }`, plus two loc keys (§3.16). Cost: a full-file override of `common/scripted_rules/00_rules.txt` (P0), or an UNVERIFIED key-level override in a separate file.
  - (b) **Accept it.** Record it as known behaviour and rely on the map lens showing these counties as unclaimed.
- **Recommendation: (a), after T14 settles whether a key-level override in `zz_eotg_rules.txt` works.** If it does, the cost is one small file. If only the full-file override works, take (b) until Gate 1 and record it on the taskboard. Re-copying a 250-line rules file each patch is not worth it for a test-map edge case.
- **Owner:** architect (here) → scripter → QA (T14). Unsworn's spec is `docs/specs/frontier_unclaimed_regions.md`.

---

## 7. Fill-in template (copy into `docs/specs/<gov>.md`)

```
# Spec: <Display name> government (eotg_<gov>_government)
Author / date / status:
Gate: <2 by default | mod-exclusive exemption granted by owner on <date>>   Blocked by Gate 1? <yes/no, why>

## 0. Kind of build (§2 rule)
[ ] Playable reskin (verb = conquer and inherit)   [ ] Distinct government (verb differs; complete Q1-Q7)
Playable? (§1 P0)  [ ] yes: no blacklisted flag   [ ] no, on purpose: GAME_OVER_CANNOT_PLAY_<X> entry + override of 00_rules.txt (T14)

## 1. Purpose & gate
One paragraph. Fiction in one sentence; who holds it at 866 (cite dated lore, never NATIONS_AT_866_AG.md).

## 2. Design answers
Q1 core verb:            "A ruler of X spends their time ___ to get ___."
Q2 signature resource:   key ______  type [scripted var | piety | prestige | dread | influence* | other*]  range __
                         sources: 1.__ 2.__   sinks: 1.__ 2.__   (*probe first: influence = T11)
                         display (§3.15 ladder): [x] 1 scaled modifier  [x] 4 story-cycle basic_counter  [ ] 2 loc  [ ] 3 bands  [ ] 5 scripted_widget*  (*owner decision)
Q3 vassal model:         [feudal-shaped trees | resource-reading obligation | tributaries | other]  opinion_of_liege? __
Q4 succession:           [own single heir | own partition | elective (electors: __) ]  fits fiction? __
Q5 entry:  ______  exit: ______  forced exit (land loss / tier drop / conquest): ______  resource on exit: ______
Q6 AI:     gains resource by __; spends by __; grant weight __; bankruptcy guard __
Q7 UI:     free surfaces used: __ ; text icon: [borrowed @government_type___! | own in gui/eotg_texticons.gui]
           new GUI beyond the default? [no | scripted_widget, owner decision ref __]

## 3. Identifier table
| Type | Key | Owner |
| government | eotg_<gov>_government | scripter |
| identity flag | eotg_government_is_<gov> | scripter |
| capability flags (vanilla) | government_is_settled, government_uses_domain_limit, government_uses_crown_authority, __ | scripter |
| contract group | eotg_<gov>_vassal | scripter |
| contracts / levels | eotg_<gov>_<tax>, eotg_<gov>_<levy>, <contract>_{none,low,standard,high,extortionate} | scripter |
| succession law(s) | eotg_<gov>_succession_law | scripter |
| law group (opt.) | eotg_<gov>_<axis> | scripter |
| resource variable / change effect | eotg_<gov>_<res> / eotg_<gov>_change_<res>_effect | scripter |
| resource display | modifier eotg_<gov>_<res>_display (scaled) + script value eotg_<gov>_<res>_value; story cycle eotg_<gov>_<res>_story (basic_counter) | scripter / localizer / human art (modifier icon) |
| role triggers | eotg_<gov>_role_top, _county, _duchy, _kingdom | scripter |
| knight trigger / term | eotg_gov_knight_realm_is_<gov> / eotg_knight_<term> (owner ruling) | scripter / localizer |
| flavourization | eotg_<tier>_<gov>, eotg_<gov>_<tier>_<gender>, eotg_<gov>_top_<tier>_<gender> | scripter / localizer |
| decisions | entry __, exit __, vassal-tier __, top-tier __, debug eotg_decision_gov_debug_become_<gov> | scripter |
| event namespace | eotg_<ns> | scripter |
| icon / text icon | gfx/interface/icons/government_types/eotg_<gov>_government.dds (70x70) / government_type_eotg_<gov> | human art / orchestrator |

## 4. File placement   (paths per §3; new folders flagged for CLAUDE.md: __)

## 5. Government block   (field | value | vanilla call site file:line | why) - every field has a call site

## 6. Wiring
on_game_start / on_government_change branches: succession net, resource init, resource teardown.
Pulse: yearly_playable_pulse -> eotg_<gov>_pulse (Section A any tier + role trigger; Section B top). Cooldown here only.
GOVERNMENT_TYPES: both define files.

## 7. Vanilla precedent   (closest vanilla government and why; deviations with reasons)

## 8. Loc surface   (§3.16 list filled; replace/ overrides: none expected)

## 9. Lore constraints   (canon facts, names banned, Canadian English, B2 list if criminal)

## 10. Definition of done
Static §5.1 items 1-7.  In game T1-T10 (+ T11-T13 where used) with expected results.  Resource moves in >= N events/decisions.
Gap table row for this government (§6 columns) all "met" or "deferred with reason".

## 11. Deferred   (item | why | trigger to revisit)

### HANDOFF
- status / next / ask / files / needs-loc / needs-lore / needs-human
```

---

## 8. Engine questions: answers (2026-10-11)

Sources:
- `govresearch/05_engine_questions_web.md` (web);
- `govresearch/06_engine_questions_files.md` (vanilla files).

Online coverage of all four questions is thin. No wiki page, forum thread or mod repo addresses them directly, so the vanilla files are the main evidence. Confidence levels: **confirmed** (read in vanilla files), **likely** (strong indirect evidence), **unknown** (needs the in-game test named).

### 8.1 Does influence work on a government without `mechanic_type = administrative`?
| Part | Answer | Confidence | Evidence |
|---|---|---|---|
| Vanilla precedent | None. All five governments with `government_has_influence` are `mechanic_type = administrative`. | confirmed | `GT:530` (admin, mechanic `:550`), `:884` (celestial, `:824`), `:1199` (steppe_admin, `:1132`), `:1329` (meritocratic, `:1265`), `JT:72` (japan_administrative, `:21`). Mandala and japan_feudal have no influence flag (`GT:1069-1081`, `JT:156-165`). |
| Top-bar (HUD) widget | **Hidden.** It is gated on the mechanic, not the flag. | confirmed | `V/gui/hud.gui:7022-7025`: `visible = "[GetPlayer.GetGovernment.HasMechanic( 'administrative' )]"` |
| Character window, ledger | Shown. These are gated on the flag. | confirmed | `V/gui/window_character.gui:5570, 5576`; `V/gui/window_ledger.gui:6621` (`HasGovernmentFlag( 'government_has_influence' )`) |
| Script checks | They work. About 60 interaction, CB and activity uses read the flag; buildings use `parameter = government_has_influence`. | confirmed (they read the flag) | `V/common/buildings/00_standard_economy_buildings.txt:3453` onward |
| Monthly gain through `monthly_influence` | Probably accrues. It is a generic modifier (`V/common/modifiers/00_artifact_modifiers.txt:197`). | likely | research 05 §1 |
| Spending; admin features (governorships, influence-cost interactions, influence AI) | Not known. | unknown | Web sources treat influence as admin-only: https://gamerant.com/ck3-roads-to-power-use-administrative-government-type-guide/, https://ck3.paradoxwikis.com/Meritocratic. No mod found doing it; the nearest is the Way of Crowns changelog (excerpt), https://steamcommunity.com/sharedfiles/filedetails/changelog/2975514448 |

**Consequence for the template:** influence is not "UI for free". A non-admin government loses the top-bar readout, and restoring it means a `hud.gui` override. Q2 therefore defaults to a scripted currency. **The settling test is T11.**

### 8.2 Can the mod add its own government text icons?
- **Answer:** yes, in **the mod's own `gui/eotg_texticons.gui`**, holding only `texticon = { }` blocks. **Never name a file `texticons.gui`**: the same path replaces vanilla's whole file.
- **Confidence: likely.** The vanilla evidence is strong, but no mod file was seen online.
- **Evidence:**
  - Vanilla spreads identical `texticon` blocks across six files (`gui/texticons.gui`, `texticons_legitimacy.gui`, `texticons_religion.gui`, `gui/shared/texticons_religion.gui`, `texticons_trigger.gui`, `texticons_ui.gui`), which implies the engine merges them.
  - Shape to copy: `V/gui/texticons.gui:4704-4711` (`government_type_herder`, size `{ 28 28 }`, offset `{ 0 6 }`, fontsize 16). It is used as `@government_type_herder!` (`V/localization/english/government_l_english.yml:761`).
  - There is no `common/` mechanism and no `_texticons.info`.
  - Web: https://ck3.paradoxwikis.com/Localization (the `@icon!` syntax). A texticon frame-count mismatch logs an error at startup (excerpt): https://steamcommunity.com/sharedfiles/filedetails/comments/2785112407
- **Settling test:** T12.

### 8.3 How does `window_domicile.gui` handle a government it doesn't name?
- **Answer:** it falls back to the **Western** frame, header and controls. The name branches only pick the Asian or Western art set. Icon, illustration and name come from the domicile type (`Domicile.GetType.GetIcon` `:66`, `GetIllustration` `:876`, `GetName` `:722`).
- **Confidence: confirmed** by reading vanilla; not yet seen in game.
- **Evidence:**
  - `V/gui/window_domicile.gui`: frame `:283/:295`, header `:377/:445`, control pairs `:549/:558`, `:646/:654`, `:2119/:2127`.
  - Each branch has a `Not(Or(...))` complement, so a frame is always visible.
  - Mixed chrome for a mod government with `mechanic_type = nomad`: `:283` uses `IsNomad`, while `:377+` use `IsType('nomad_government')`.
  - Domicile assets are picked by type (Roads to Power modding dev diary, excerpt): https://admin-forum.paradoxplaza.com/forum/developer-diary/dev-diary-156-modding-achievements.1702728
- **Pitfall (likely):** a domicile created by `create_nomad_title` reportedly gets a line of succession only when the custom government has `uses_county_fertility = yes` (forum bug report, excerpt): https://admin-forum.paradoxplaza.com/forum/threads/the-create_nomad_title-effect-fails-to-create-a-domicile-line-of-succession-with-government-types-other-than-nomad_government.1889778
- **Settling test:** T13 (domicile part).

### 8.4 How can a scripted resource be shown without a custom GUI?
- **Answer:** the §3.15 ladder. The default is a **scaled character modifier** plus a **visible story cycle with a `basic_counter`**. `gui/scripted_widgets/` is the opt-in upgrade, and a `hud.gui` override is the last resort.
- **Confidence: confirmed** for each mechanism (vanilla precedent). No consensus online on what mods do. How prominently a story cycle displays is unknown, and T13 settles it.
- **Evidence:**
  - Scaled modifier: `V/common/modifiers/00_court_position_modifiers.txt:138-141`, `00_diarchy_modifiers.txt:159`.
  - Loc reading a variable: `coronation_activity_l_english.yml:675-677, 705`. Global `ScriptValue`: `modifiers_l_english.yml:1368`. No vanilla modifier or trait desc prints a per-character numeric variable; the numeric cases are decision and trigger tooltips.
  - Story cycle: `_story_cycles.info:23, 58-110`; `book_translation_story_cycle.txt:2, 10-14`. The variable lives on the story scope. Mod precedent: `common/story_cycles/eotg_aug_kingpin_story.txt:46-55`.
  - Scripted widgets: `V/gui/scripted_widgets/_scripted_widgets.info` ("multiple mods can load their own widgets") and https://ck3.paradoxwikis.com/Interface. Overlap risk with other widgets (excerpt): https://steamcommunity.com/workshop/filedetails/discussion/2829316015/3838801919855095394
  - Radiance can't be copied: its HUD binds to engine data (`V/gui/hud.gui:3507-3540`), and `mandala_radiance_value` is "USED IN CODE" (`tgp_mandala_values.txt:483-485`).
- **Decision recorded by this template:** the "the mod ships no `gui/` folder" owner question has a default answer (layers 1 + 4, no `gui/`). Adding `gui/` (text icons, scripted widgets) is opt-in per government and needs a placement-table entry.

---

### HANDOFF
- status: done
- next: none (orchestrator). The template is reference material. The engine questions are answered in §8, and the remaining unknowns are in-game tests T11–T13. Next for the four governments: an architect G2 spec built on the §3.15 default display.
- ask: Record `docs/specs/government_template.md` as the required starting point for any new government spec. Run CB-49 (V-G1–V-G20) before G2 builds on the four.
- files: docs/specs/government_template.md
- needs-loc: none
- needs-lore: none
- needs-human: CB-49 in-game checks; T14 (scripted-rule override: key-level vs full file) before the §6.2 Unsworn decision. Owner decisions: (1) settled by default (§3.15: a scaled modifier plus a story-cycle counter, no `gui/`); a `gui/scripted_widgets/` readout and `gui/eotg_texticons.gui` are opt-in and need placement entries; (2) whether the Corporation and Trade Oligarchy accept dynastic single-heir succession until G2 elective laws land; (3) the orchestrator adds the §4 item 9 folders to the CLAUDE.md placement list when first used.

### 8.5 Vassal-contract window and government names (2026-10-11, verified in vanilla)
- `gui/interaction_modify_vassal_window.gui` hard-codes government names in a few places, and all of them are cosmetic:
  - background art: `FeudalVassalBackground` at :1381 for `feudal_government`, and `NonFeudalVassalBackground` at :1400 for everything that is not nomad, feudal or administrative. Further name-specific art at :1418-1472;
  - wording: feudal versus non-feudal text at :572/:576 and :625/:629;
  - the "obligation only once" note at :914, shown only for feudal or administrative vassals.
- Which panel section shows is chosen by the contract layout (`HasModifyContractLayout('default' | 'clan' | 'admin' | 'eastern_admin')`, :95-143), not by the government name.
- **Effect on our governments:** their vassals get the non-feudal background and the generic wording. Negotiation works through the contract group. No override is needed. Only change the window if a custom `modify_contract_layout` is ever introduced; that is a wholesale override of a vanilla GUI file, with the compatibility cost that brings.
- `government_is_administrative` has **no reader in vanilla `gui/`** (grep, 2026-10-11). The claim that the engine checks that flag for the estate or noble-family UI is UNVERIFIED. It came from an observational source and is not relied on.
