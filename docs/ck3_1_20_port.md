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

Religion is the one high-risk area. In 1.20 a faith nested inside a religion's `faiths = { }`
block is not loaded at all, so every character, title and trigger that references an EOTG
faith breaks. Required work:

1. Move each faith to `common/religion/faith_types/` as a top-level entry with
   `faith_details = { religion = <religion_key> ... }`.
2. Wrap religion-level `family`, `graphical_faith`, `piety_icon_group` and icons in
   `religion_details = { }`.
3. Add the new faith folders (and the rite folder, once its name is checked against 1.20
   vanilla) to `replace_path` in `descriptor.mod` if vanilla faiths should not load.
4. EOTG religions use no `tenet_*` keys. The `doctrine_*` keys still need to be checked against
   1.20 `doctrine_types`.
