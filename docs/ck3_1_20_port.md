# CK3 1.20 "Crozier" Port Tracker

Tracks the work of moving Echoes of the Grip from CK3 1.19 "Scribe" to 1.20.0.2 "Crozier".

**Sources used:**
- Vanilla 1.20.0.2 game files: `common/governments/_governments.info`, `00_government_types.txt`,
  `02_theocratic_government_types.txt`, `common/law_groups/00_realm_law_groups.txt`,
  `common/scripted_triggers/00_law_triggers.txt`, `common/scripted_rules/01_grant_title_rules.txt`.
  These were diffed against 1.19.0.3 using the
  [skonester/ck3-mod-base](https://github.com/skonester/ck3-mod-base) mirror of the vanilla files.
- That repo's community migration guide, `1.20.0.2.md`. This is **not** official Paradox
  documentation. Every claim below was checked against the vanilla files.

**Tiger caveat:** the newest Tiger release (1.19.0) still validates against CK3 1.19. It does
not know about `possible_grant_vassal_governments`, `grant_vassal_ai_will_do`,
`government_has_mechanic`, `royal_court = landed`, faith_types, law_groups and so on. Expect
false positives on 1.20-only syntax until Tiger is updated.

---

## Status

| Area | Status | Notes |
|---|---|---|
| Governments (`common/governments/`) | ✅ Audited: no changes required | See below |
| Subject contracts (`common/subject_contracts/`) | ✅ Audited: no changes required | `.info` files unchanged between 1.19 and 1.20 |
| Council positions / tasks | ✅ Audited: no changes required | `.info` files unchanged between 1.19 and 1.20 |
| Government-related script (`has_government`, `change_government`) | ✅ No changes required | All targets still exist |
| Religions (`common/religion/religion_types/`) | ❌ **Blocking**: needs restructure | 11 `faiths = { }` blocks. Faiths nested in religions are no longer read in 1.20 |
| Religion families | ❌ Needs update | `doctrine_background_icon` → `tenet_background_icon` inside `religion_details` |
| `stress_impact` blocks (193 uses) | ⚠️ Optional | Still valid. `stress_and_fulfillment_impact` is the new form |
| `descriptor.mod` `supported_version` | ⏳ Pending | Bump to `"1.20.*"` once religion is ported |
| Laws (`common/laws/`) | ✅ N/A | The mod defines no laws |

---

## Governments: audit results

### What changed in 1.20

| 1.19 | 1.20 |
|---|---|
| `government_rules = { religious = yes }` | Removed. Use `mechanic_type = theocracy` |
| `government_rules = { administrative = yes }` | Removed. Use `mechanic_type = administrative` |
| (none) | `is_mechanic_type_default = yes`: one per mechanic type. Vanilla already provides every default |
| (none) | `possible_grant_vassal_governments = { ... }` + `grant_vassal_ai_will_do`: Grant Titles government picker |
| (none) | New government rules `treasury_vassal_development` and `add_religious_subordinates_for_treasury` |
| `royal_court = none / any / top_liege` | Adds `landed` |
| `theocracy_government` in `00_government_types.txt` | Moved to `02_theocratic_government_types.txt`. New `ecclesiastical_government` |
| Realm laws nested in groups | Law groups are separate (`common/law_groups/`) and gated by `required_government_flag` |

### Why the EOTG governments need no changes

1. **No removed rules.** None of the seven governments uses `religious` or `administrative`.
   Every rule we set (`create_cadet_branches`, `rulers_should_have_dynasty`,
   `dynasty_named_realms`, `legitimacy`) is unchanged.
2. **`mechanic_type` is optional.** `_governments.info` says *"Not all governments must specify
   one."* Vanilla `republic_government` and `tribal_government` set none. In vanilla script,
   `government_has_mechanic` only checks `administrative` and `theocracy`, and none of ours are
   either. Adding `mechanic_type = feudal` would bring no script-visible benefit and could pull
   in undocumented engine behaviour, so it is left unset.
3. **Law gating behaves as before.** Crown Authority is now gated by
   `required_government_flag = { government_uses_crown_authority }`. In 1.19 the same flag was
   checked through `realm_law_use_crown_authority` in each law's `can_keep`. None of our
   governments had the flag in 1.19, so none had Crown Authority, and that stays true in 1.20.
   Tribal, church and the bureaucracy authorities use new flags that we also don't set.
4. **Raiding is unchanged.** `government_can_raid_rule` (Cartel) is still the raid flag in
   vanilla 1.20 (tribal, wanua, nomad).
5. **Modifiers are valid.** Every `character_modifier` key we use is still defined. The 1.20
   removals are faith-creation costs and five Islamic-school opinion modifiers, none of which we use.
6. **Holdings are unchanged.** `castle_holding` and `city_holding` keep their keys.
7. **`change_government` targets all exist.** Fringe reforms target `eotg_cartel_government`,
   `eotg_pmc_government`, `eotg_gobcorp_government` and vanilla `feudal_government`. PMC
   restructuring targets `eotg_corporation_government`.

### Optional 1.20 features (design decisions, not done)

- **Crown Authority for Elven Monarchy.** The design doc calls it "mechanically closest to
  vanilla feudal". Adding `government_uses_crown_authority` to its `flags` would give it the
  Crown Authority law track. This changes behaviour, so it needs a design decision.
- **Theocratic grants.** `possible_grant_vassal_governments = { theocracy_government }` would
  let a ruler hand counties to theocratic vassals. Vanilla's `is_grant_government_valid` only
  allows this when both rulers' Rite has `doctrine_theocracy_temporal`. That fits the
  Thae'Viriel / Eternal King faiths, but it should wait until the religion port is done.
- **Flag-based checks.** Vanilla 1.20 keeps moving from `has_government = X` to
  `government_has_flag = ...` (e.g. tributary contracts). Our scripted triggers could check
  `eotg_government_is_*` flags instead, which makes them moddable. This isn't required.

---

## Next up: religion port (blocking)

### Inventory (`common/religion/religion_types/eotg_religions.txt`)

11 religions, 12 faiths, 2 families. All `doctrine_*` keys used still exist in 1.20 `doctrine_types`.
No `tenet_*` keys, holy sites, religious-head titles, traits, icons or localization blocks are defined.

| Religion | Family | Faith(s) | Head / theocracy | Used in history |
|---|---|---|---|---|
| `eotg_religion_elross` | divine_order | `eotg_faith_elross_canonical` | temporal head, temporal theocracy | 3 chars |
| `eotg_religion_commerce` | titan_worship | `eotg_faith_commerce` | none, lay clergy | 3 chars |
| `eotg_religion_coldiron` | divine_order | `eotg_faith_coldiron` | temporal head, temporal theocracy | 4 chars |
| `eotg_religion_stampede` | titan_worship | `eotg_faith_stampede` | none, lay clergy | unused |
| `eotg_religion_ancestor_veneration` | titan_worship | `eotg_faith_ancestor_veneration` | none, lay clergy | unused |
| `eotg_religion_void_reverence` | titan_worship | `eotg_faith_void_cult` | none, lay clergy | unused |
| `eotg_religion_firstlight` | divine_order | `eotg_faith_firstlight` | spiritual head, temporal theocracy | 4 chars + bookmark |
| `eotg_religion_survivalism` | titan_worship | `eotg_faith_industrial_survivalism` | none, lay clergy | 2 chars |
| `eotg_religion_secular_codes` | titan_worship | `eotg_faith_secular_contract`, `eotg_faith_civic_secular` | none, lay clergy | 3 + 1 chars |
| `eotg_religion_forge_tradition` | titan_worship | `eotg_faith_forge_tradition` | none, lay clergy | 1 char |
| `eotg_religion_deep_warren` | titan_worship | `eotg_faith_deep_warren` | spiritual head, lay clergy | 2 chars |

### Required work

1. **Faiths** → `common/religion/faith_types/eotg_faiths.txt`: top-level entries with
   `faith_details = { religion = ... color = ... }`. With no `main_rite`, the engine creates a
   dynamic Rite with the same key, so existing faith keys keep working.
2. **Religions** → wrap `family` in `religion_details = { }` and delete the `faiths = { }` blocks.
   Religion-level `doctrine = ...` lines stay where they are.
3. **Families** (`eotg_religion_families.txt`) → `doctrine_background_icon = core_tenet_banner_*.dds`
   becomes `tenet_background_icon` (+ `_heretical_` / `_neutral_` / `_unknown_` variants, as in
   vanilla `rf_abrahamic`). Consider adding `hostility_doctrine` (e.g. `abrahamic_hostility_doctrine`),
   which vanilla families set and ours never have.
4. **`descriptor.mod` replace_path (crash risk).** In 1.19, vanilla faiths lived inside
   `religion_types`, which we already replace. In 1.20 they live in folders we do **not** replace,
   so 102 vanilla faiths, their Rites and 17 faith-history files would load pointing at religions
   that no longer exist. Add:
   `common/religion/faith_types`, `common/religion/rite_types`, `history/faiths`.
   Check whether `common/religion/rite_names` and `rite_icons` reference vanilla rites too.
5. **Character history** uses `religion = faith:eotg_faith_x`. The 1.20 `_characters.info`
   documents `faith = <key>` (or `rite = <key>`), with `religion = <faith>` as a compatibility
   form. Switch to `faith = eotg_faith_x`. The `faith:` prefix is not the documented history syntax.
6. **Religious heads.** Elross and Coldiron (temporal head) and Firstlight and Deep Warren
   (spiritual head) have head doctrines but no `religious_head` title. Unchanged from 1.19, but
   worth fixing during the port.
