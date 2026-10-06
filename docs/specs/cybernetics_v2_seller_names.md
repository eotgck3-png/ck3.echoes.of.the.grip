# Cybernetics v2: named sellers (CB-42)

**Index:** [cybernetics_v2.md](cybernetics_v2.md). Index §1 rules 1–12 and the §5 lore register apply. The lore-keeper ruled on §8.1 and §8.3 on 2026-10-05. Its rulings are folded in below, and index §5 item 3 and balance §5 item 5 now carry the amended text.
**Status:** spec, 2026-10-05. **Owner of the request:** the human (approved; taskboard CB-42).
**Sequence:** ~~lore-keeper (§8.1 ruling + names brief)~~ done 2026-10-05 → scripter (generator, rolls, wiring) → localizer (starting names into the owner file, 23 host-line rewrites) → lore-keeper (names check) → QA → orchestrator commits.
**Blocked on:** the tier-options batch (`cybernetics_v2_tier_options.md`) being committed first. It edits the same loc file and `events/eotg_augmentation_tier2.txt`, including tier2.014.

---

## 1. Purpose & gate

Cybernetics events now say "a clinic", "a vendor" or "the syndicate". With this change they name the seller: a made-up **company** for sanctioned clinics and licit vendors, and a made-up **gang** for back-street work. The Patron's syndicate is named too, from a list of **canon** syndicates (owner ruling, 2026-10-05). Each name is drawn from one owner-editable file. It starts with 12 companies, 12 gangs and 1 syndicate (Pill Mob). The name is rolled once per encounter and kept wherever the story continues. This is **flavour on existing events only**. It adds no events and no options, changes no option effects, and touches no tooltips that describe mechanics.

**Gate:** cybernetics is a mod-exclusive system (CLAUDE.md, 2026-10-02), so this can be built now, before Gate 1. Nothing here references a title, province, character, culture or faith. Region- or culture-specific name pools wait for the real map (§10).

**Recommendation in one line:** store every roll as a **character variable holding a flag** and read it with **non-random customizable localization** (the vanilla captive-animal pattern). Generate the custom loc, the roll effects and the name loc from **one plain list file**, `cybernetics_seller_names.txt` at the repo root, with `docs/tools/gen_seller_names.py`. That tool has a `--check` mode wired into `check_all.py` (option **(b)**). The Patron's syndicate is named once per story from a third list, `[syndicates]`, of canon names that the owner maintains (§5.4).

## 2. Signature resource

This spec adds no events, so it adds no flavour event that could fail invariant 5. Every host listed in §5.1 already reads or moves the cybernetics resource (`eotg_fracture_risk`, the `eotg_cybernetics` tier, or both), and that stays as it is.

The value this system defines is the **seller roll**: a character variable holding a flag (`flag:eotg_aug_co_<id>` or `flag:eotg_aug_gang_<id>`). A host either **rolls it in `immediate`** or is a listed **continuation that only reads it**. No other event may read a seller variable. Without that rule, an unrelated event would show a seller from an earlier encounter.

## 3. Identifier table

All new keys carry `eotg_`. There are no landed titles. "Gen" means the key is written by the generator and nobody edits it by hand.

| Identifier | Type | Exact name | Owner |
|---|---|---|---|
| Owner list file | data file (not loaded by the game) | `cybernetics_seller_names.txt` (repo root) | human (localizer drafts the first 24) |
| Generator | Python tool | `docs/tools/gen_seller_names.py` | scripter |
| Generator tests | unittest | `docs/tools/tests/test_gen_seller_names.py` | scripter |
| Company flag value | flag | `flag:eotg_aug_co_<id>` | gen |
| Gang flag value | flag | `flag:eotg_aug_gang_<id>` | gen |
| Syndicate flag value | flag | `flag:eotg_aug_syn_<id>` | gen |
| Company name loc | loc key | `eotg_aug_seller_co_<id>` | gen |
| Gang name loc | loc key | `eotg_aug_seller_gang_<id>` (value is `the <Name>`) | gen |
| Syndicate name loc | loc key | `eotg_aug_seller_syn_<id>` (value is the name exactly as the owner wrote it, §4.1) | gen |
| Fallback loc | loc keys | `eotg_aug_seller_fallback_company`, `_gang`, `_vendor_careful`, `_vendor_bold`, `_clinic_of_record` `_syndicate`, `_rival_syndicate` | gen (text fixed in §7.3) |
| Custom loc: this encounter's company | customizable_localization | `eotg_aug_cl_company` | gen |
| Custom loc: this encounter's gang | customizable_localization | `eotg_aug_cl_gang` | gen |
| Custom loc: careful vendor | customizable_localization | `eotg_aug_cl_vendor_careful` | gen |
| Custom loc: bold vendor | customizable_localization | `eotg_aug_cl_vendor_bold` | gen |
| Custom loc: clinic of record | customizable_localization | `eotg_aug_cl_clinic_of_record` | gen |
| Custom loc: the Patron's syndicate | customizable_localization | `eotg_aug_cl_syndicate`, `eotg_aug_cl_syndicate_offer`, `eotg_aug_cl_rival_syndicate` | gen |
| Roll a company into a variable | scripted effect, param `VAR` | `eotg_aug_roll_company_effect` | gen |
| Roll a company, excluding one | scripted effect, params `VAR`, `EXCLUDE` | `eotg_aug_roll_company_except_effect` | gen |
| Roll a gang into a variable | scripted effect, param `VAR` | `eotg_aug_roll_gang_effect` | gen |
| Roll a syndicate | scripted effects | `eotg_aug_roll_syndicate_effect`, `eotg_aug_roll_syndicate_except_effect` | gen |
| Roll both vendors | scripted effect | `eotg_aug_roll_vendors_effect` | scripter (hand-written) |
| Record the clinic | scripted effect | `eotg_aug_record_clinic_effect` | scripter (hand-written) |
| This encounter's company | character variable (flag) | `eotg_aug_seller_company` | scripter |
| This encounter's gang | character variable (flag) | `eotg_aug_seller_gang` (on root; on `scope:eotg_copycat` in tier1.018) | scripter |
| Careful vendor | character variable (flag) | `eotg_aug_vendor_careful` | scripter |
| Bold vendor | character variable (flag) | `eotg_aug_vendor_bold` | scripter |
| Clinic of record | character variable (flag) | `eotg_aug_clinic_of_record` | scripter |
| Offered syndicate | character variable (flag) | `eotg_patron_syndicate_passthrough` (same naming as the existing `eotg_patron_envoy_passthrough`) | scripter |
| Patron's syndicate | story variable (flag) | `eotg_syndicate` on `eotg_story_aug_patron` | scripter |
| Rival syndicate | character variable (flag) | `eotg_aug_rival_syndicate` | scripter |
| Rival exclusion (copy of the story's syndicate) | character variable (flag) | `eotg_aug_rival_exclude` | scripter |
| Syndicate-list never list | JSON key in an existing file | `"syndicate_never"` in `docs/tools/eotg_lint_register.json` | scripter (terms from §8.3) |
| Syndicate-list warning list | JSON key in an existing file | `"syndicate_warn"` in `docs/tools/eotg_lint_register.json` | scripter (terms from §8.3) |
| L012 exemption for generated syndicate keys | JSON key in an existing file | `"exempt_key_regex": "^eotg_aug_seller_syn_"` in `docs/tools/eotg_lint_register.json` | scripter |
| Bold-firmware desc with the name | loc key (modifier custom desc) | `eotg_mod_aug_bold_firmware_vendor_desc` | localizer |
| Name-only never list | JSON key in an existing file | `"name_never"` in `docs/tools/eotg_lint_register.json` | scripter (terms from §8.3) |
| Per-list banned name words | JSON key in an existing file | `"name_banned_words"` in `docs/tools/eotg_lint_register.json` | scripter (terms from §8.3) |

`<id>` is derived from the name (§4.2). Name lists, icons, CoAs and holy sites: the 24 starting names are owned above. There are no icons, CoAs or holy sites.

## 4. File placement

| Path | What | Written by |
|---|---|---|
| `cybernetics_seller_names.txt` | the owner's list (§4.1) | human / localizer |
| `common/customizable_localization/eotg_aug_seller_names.txt` | the custom loc keys of §3, one `text` per name plus a fallback | gen |
| `common/scripted_effects/eotg_aug_seller_roll_effects.txt` | the roll effects | gen |
| `localization/english/eotg_aug_seller_names_l_english.yml` | the name keys and fallback keys | gen (through `textio.write_text(..., bom=True)`) |
| `common/scripted_effects/eotg_augmentation_effects.txt` | `eotg_aug_roll_vendors_effect`, `eotg_aug_record_clinic_effect` | scripter |
| `events/eotg_augmentation_{initiation,tier1,tier2}.txt` | rolls in `immediate`, clinic-of-record sets, modifier `desc =` | scripter |
| `localization/english/eotg_augmentation_l_english.yml` | the 23 host-line rewrites (§7.1), `eotg_mod_aug_bold_firmware_vendor_desc` | localizer |
| `docs/tools/check_all.py` | one more `--check` entry | scripter |
| `docs/tools/eotg_lint.py`, `eotg_lint.md` | custom-loc awareness for L010/L014 (§4.3) | scripter |

`common/customizable_localization/` is a new folder for the mod. Add it to the placement table in CLAUDE.md when it lands (orchestrator). It needs no `replace_path`.

The list file goes at the **root** so the owner can find it. The game ignores unknown root files. The generated files each open with a comment saying "GENERATED. Edit `cybernetics_seller_names.txt` and run `python docs/tools/gen_seller_names.py`."

### 4.1 Owner-file recommendation: option (b)

Adding one name by hand would mean touching about eight places: a loc key, five custom loc entries (company names appear in four keys), and two or three `random_list` entries. That breaks the "one file" promise, and a header listing eight edit sites (option (a)) would be wrong the first time a key is added. **Option (b)**: the owner edits one list and runs one command. Nobody maintains a count, because the tool counts and prints it every run.

**Exact format** (UTF-8, BOM optional, read with `textio.read_text`):

```
# ============================================================
#  CYBERNETICS SELLER NAMES  (Echoes of the Grip)
# ============================================================
#  The companies and gangs that sell implants in cybernetics events.
#
#  TO ADD A NAME
#    1. Put it on its own line under [companies], [gangs] or
#       [syndicates].
#    2. Run:   python docs/tools/gen_seller_names.py
#       It tells you how many names each list has, or what is wrong.
#    That is all. No other file needs editing.
#
#  RULES
#    Companies: local firms that fit and service implants. Singular,
#      no "the": Merrow & Tallis Surgical. They fit, service and
#      sell implants; they never make them. Not Corp, Co., Inc.,
#      Holdings, Industries, Works, Labs, or anything galactic.
#    Gangs: back-street crews. Plural, and NO "the" at the start.
#      The game adds it: write Low Wires, it prints "the Low Wires".
#    Syndicates: CANON groups from the setting, not invented ones.
#      This is the Patron's syndicate. Write the name exactly as it
#      is printed mid-sentence, with "the" only if canon uses
#      one: the Pill Mob, Samulo's Tieflings. One name is enough.
#      The tool rejects authorities, planar names, post-866 groups
#      and Nikios, and warns about P&D, Calix and the Black Cogs
#      Consortium (your call).
#    Up to 32 characters. Letters, digits, spaces, & ' . - only.
#    Companies and gangs: Canadian spelling, and made up: no real
#      brands, no real gangs, no canon groups.
#    Never use a name on the never-name list in
#      docs/specs/cybernetics_v2_seller_names.md section 8.3.
#      The tool rejects most of them for you.
#
#  RENAMING OR DELETING
#    Allowed. A story already running in a saved game that used
#    the old name will show generic wording ("a sanctioned
#    clinic", "the syndicate") until that story ends.
#    Adding names never changes a story already running.
#
#  Lines starting with # are ignored. Blank lines are ignored.
# ============================================================

[companies]
<12 names>

[gangs]
<12 names>

[syndicates]
the Pill Mob
```

**Parsing rules:**
- `[companies]`, `[gangs]` and `[syndicates]` are the only section headers.
- One name per line. Surrounding whitespace is trimmed, and anything after a `#` on a name line is dropped.
- A name before the first header is an error, and so is an unknown header.

### 4.2 Generator `docs/tools/gen_seller_names.py`

Standard library only, following the pattern of `gen_test_recipes.py` / `spec_conformance.py`.

```
python docs/tools/gen_seller_names.py [--root CHECKOUT] [--check]
```

**id derivation:**
1. NFKD-fold to ASCII.
2. Lowercase, and turn `&` into `and`.
3. Turn every run of non-alphanumeric characters into `_`, then strip leading and trailing `_`.
4. Cap at 40 characters.

Example: `Merrow & Tallis Surgical` becomes `merrow_and_tallis_surgical`. For syndicates, a leading `the ` is dropped before the id is derived, so `the Pill Mob` becomes `pill_mob`. The id is not written in the list, so renaming a name changes its id (§4.1 header explains what that does).

**Validation** (reports the list file and line number, exits 1):
- **List size:** `[companies]` needs at least 2 names, because tier2.013 needs two distinct vendors. `[gangs]` needs at least 1. `[syndicates]` needs at least 1. With a single syndicate the rival roll finds nothing and patron.006.d reads "a rival syndicate" (§5.4).
- **Duplicates:** a duplicate name (case-insensitive) or a duplicate id is an error. So is an empty id.
- **Length:** at most 32 characters.
- **Characters:** only letters (including accented ones), digits, space, `&`, `'`, `.` and `-` are allowed. So `"`, `[`, `]`, `$`, `#`, `|`, `§`, `{`, `}`, `=`, `—` and `–` are rejected.
- **Articles:** a gang name that starts with `the ` is rejected with the message "drop 'the'; the game adds it". A syndicate name is printed **exactly as written**, with the article only if canon uses one (`the Pill Mob`, `Samulo's Tieflings`). The tool never adds or changes an article in that list. `|U` capitalizes it at a sentence start.
- **Never-names and banned words, companies and gangs:** every `error` regex in `docs/tools/eotg_lint_register.json`, plus the new `name_never` list (§8.3), is checked against each name. So are the per-list word bans of §8.3 (`name_banned_words` in the same JSON, with keys `all`, `companies`, `gangs`). Matching is whole-word and case-insensitive. Plurals are listed explicitly, and the leading-word bans (`Red`, `Black`) are anchored. Every rule in §8.3 that a regex can express is enforced here (lore-keeper ruling 5). The rest go to the lore-keeper's sign-off.
- **Syndicates are checked differently** (lore-keeper ruling, 2026-10-05). They are canon names, so these do **not** apply to `[syndicates]`: the register never-names, `name_never`, the suffix and word bans, the 'the is built in' rule and the invented-name requirement. Apostrophes are allowed in every list. What does apply: **hard rejects** from `syndicate_never` (exit 1) and **warnings** from `syndicate_warn` (printed, exit 0; the owner decides), both in §8.3, plus the format rules (32 characters, the character set, no duplicates). So `the Pill Mob` passes in `[syndicates]` and still fails in `[gangs]`. One name in two lists is an error.

**Outputs** (deterministic: list order is kept, `\n` line endings, written through `textio.write_text(path, text, bom=True)`, so there is exactly one BOM, L016):

1. **Custom loc file.** Each key below gets one `text` per name in its list, in list order, plus a final `fallback = yes` text. All keys are `type = character`. No key has `random_valid`. The triggers are `var:<VAR> ?= flag:<flag>` (the vanilla form, §6).

   | key | list | reads |
   |---|---|---|
   | `eotg_aug_cl_company` | companies | `var:eotg_aug_seller_company` |
   | `eotg_aug_cl_gang` | gangs | `var:eotg_aug_seller_gang` |
   | `eotg_aug_cl_vendor_careful` | companies | `var:eotg_aug_vendor_careful` |
   | `eotg_aug_cl_vendor_bold` | companies | `var:eotg_aug_vendor_bold` |
   | `eotg_aug_cl_clinic_of_record` | companies | `var:eotg_aug_clinic_of_record` |
   | `eotg_aug_cl_syndicate_offer` | syndicates | `var:eotg_patron_syndicate_passthrough` |
   | `eotg_aug_cl_syndicate` | syndicates | `any_owned_story = { story_type = eotg_story_aug_patron  var:eotg_syndicate ?= flag:<flag> }` |
   | `eotg_aug_cl_rival_syndicate` | syndicates | `var:eotg_aug_rival_syndicate` |

   The key-to-variable table is a constant in the generator. `PATRON_NAMED = True` (owner ruling, 2026-10-05), so the syndicate rows are always emitted. The constant stays in the generator as a switch for turning the naming off again.

2. **Roll effects file.** One `random_list` per effect, with one `1 = { ... }` entry per name.
   - Each entry is `set_variable = { name = $VAR$  value = flag:<flag> }`.
   - In the `_except` variants, each entry also carries `trigger = { NOT = { var:$EXCLUDE$ ?= flag:<flag> } }`.
   - Shape: vanilla `random_list` entries with `trigger`, `events/story_cycles/story_cycle_pet_animal_events.txt:108-200`.

3. **Name loc file.** It opens with `l_english:`. It holds one key per name and the fallback keys from §7.3:
   - companies: `eotg_aug_seller_co_<id>:0 "<Name>"`;
   - gangs: `eotg_aug_seller_gang_<id>:0 "the <Name>"`;
   - syndicates: `eotg_aug_seller_syn_<id>:0 "<Name as written>"` (for example `"the Pill Mob"`).

   The header comment repeats the counts.

**Default run:** validates, writes the three files, and prints `companies: 12  gangs: 12  syndicates: 1` and the three paths.

**`--check`:** validates, renders all three outputs in memory and compares their bytes with the files on disk. It exits 0 and prints the counts when they match. When they don't, it exits 1 and names each stale file, with the line "run: python docs/tools/gen_seller_names.py". A validation error also exits 1. It never writes.

**check_all wiring:** add `("gen_seller_names", "cybernetics_seller_names.txt")` to the tuple loop at `docs/tools/check_all.py:224`. The loop already calls `[PY, tool.py, "--root", root, "--check"]` and skips the check when the presence path is missing. Update the module docstring list at `check_all.py:14-17`.

**Tests** (`test_gen_seller_names.py`, using `_testutil`):
- parse and validate each error class;
- id derivation, including `&`, accents and collisions;
- the output is byte-stable across two runs;
- `--check` fails after a list edit and passes after regeneration;
- the output has exactly one BOM per file;
- a gang name starting with "the" is rejected;
- a register never-name is rejected.

### 4.3 Lint follow-ups (scripter, same batch)

`eotg_lint.py` does not read `common/customizable_localization/` today. Without these two changes, every generated name key trips **L014** (defined, never referenced), and a mistyped `Custom('...')` passes **L010**:
- **L014:** treat every `localization_key = X` inside `common/customizable_localization/*.txt` as a reference to `X`.
- **L010:** a `Custom('eotg_...')` call in loc must name a key defined at the top level of `common/customizable_localization/`. Every `localization_key` there must be defined in loc.
- Document both in `eotg_lint.md`. **L012** needs no change: name keys start `eotg_aug_`, so they are already scanned for never-names. That double-checks the generator.

## 5. Wiring

There are no new on_actions or events, and no cooldowns to place. Every host keeps its current caller and trigger. Rolls go in `immediate` inside `hidden_effect`. A variable set in `immediate` is in place before the desc and the options render, and nothing re-rolls it while the window is open. That stability is why there is **no `random_valid` anywhere** (it re-picks on every evaluation).

### 5.1 Host classification

The grep `clinic|vendor|syndicate` (case-insensitive) over `localization/english/eotg_augmentation_l_english.yml` returns **75 lines** (working tree of 2026-10-05). Each is classified below, plus 1 non-hit that continues a named story (tier1.018). Line numbers drift, so the keys are what count.

**Named: company list**

| Key(s) | Line | Storage / roll |
|---|---|---|
| `eotg_aug_init.001.desc` | 102 | `eotg_aug_roll_company_effect = { VAR = eotg_aug_seller_company }` in a new `immediate` |
| `eotg_aug_init.002.desc` | 110 | same, new `immediate` |
| `eotg_aug_init.006.desc`, `.desc_congenital` | 359, 1733 | same, added to the existing `immediate` (`initiation.txt:743`). The plural "the clinics here" stays generic; "a/the technician" gets "from [company]" |
| `eotg_aug_init.018.desc`, `.a` | 456–457 | company roll in a new `immediate` (with the gang roll below) |
| `eotg_aug_tier1.002.desc`, `.desc_sought` | 148–149 | `immediate`: if `has_variable = eotg_aug_clinic_of_record`, `set_variable = { name = eotg_aug_seller_company  value = var:eotg_aug_clinic_of_record }`; otherwise roll. *The clinic that fitted you comes back with the next model.* |
| `eotg_aug_tier1.019.desc_worse`, `.desc_dead` | 1036–1037 | `immediate`: the same "record, else roll" as tier1.002, on root. The clinic that treats the copycat is your clinic. |
| `eotg_aug_tier2.013.desc`, `.a`, `.b` | 1141–1143 | `immediate`: `eotg_aug_roll_vendors_effect` when `NOT = { has_variable = eotg_aug_vendor_careful }` |
| `eotg_aug_tier2.014.desc_played`, `.desc_waited`, `.a`, `.b` | 1152–1153 (+ .a/.b, not grep hits) | **read only** (continuation of .013). No roll. |
| `eotg_mod_aug_bold_firmware_desc` → new `eotg_mod_aug_bold_firmware_vendor_desc` | 1396 | `desc = eotg_mod_aug_bold_firmware_vendor_desc` added to both `add_character_modifier` calls (`tier2.txt:1914`, `:2034`). The old `_desc` stays as the engine default. |
| `eotg_decision_aug_pursue_next_stage_desc` | 887 | **read only**, `eotg_aug_cl_clinic_of_record` with its fallback |

**Named: gang list**

| Key(s) | Line | Storage / roll |
|---|---|---|
| `eotg_aug_init.004.desc` | 124 | `eotg_aug_roll_gang_effect = { VAR = eotg_aug_seller_gang }` in a new `immediate`. "The sanctioned clinics are two systems behind" stays generic. |
| `eotg_aug_init.010.desc` | 393 | same, new `immediate`. "what the sanctioned clinics charge" stays generic. |
| `eotg_aug_init.018.desc`, `.b` | 456, 458 | gang roll in the same `immediate` as the company |
| `eotg_aug_init.011.desc_discovered` | 402 | **read only**, a continuation of init.010 (a, c, d) and init.018.b (`initiation.txt:1466,1513,1548,2689`). Nothing that can fire between them rolls a gang into root's variable. Init gang hosts require `eotg_is_augmented_any = no`, and tier1.018 writes to the copycat (next row). |
| `eotg_aug_tier1.018.desc` (non-hit: "a back-room operator") | 1026 | rolled **on the copycat**: inside the existing `scope:eotg_copycat = { }` block, `eotg_aug_roll_gang_effect = { VAR = eotg_aug_seller_gang }`. Loc reads `[eotg_copycat.Custom('eotg_aug_cl_gang')]`. Root's gang variable is untouched. |

**Clinic of record.** It is set by `eotg_aug_record_clinic_effect`:

```
if = { limit = { has_variable = eotg_aug_seller_company }
       set_variable = { name = eotg_aug_clinic_of_record  value = var:eotg_aug_seller_company } }
```

Call it inside the existing `hidden_effect`, next to the procedure call, in **every option of a named-company host whose procedure call has `PROVIDER = clinic`**:
- init.001 a, d, e;
- init.002 a;
- init.006 a, and any other clinic option there;
- init.018 a;
- tier1.002 a.

The scripter enumerates the exact list by grepping `PROVIDER = clinic` inside those events. It does **not** go into `eotg_aug_procedure_effect`, which stays as built. The clinic of record is never removed: excision or full removal leaves it, and a later clinic install overwrites it. **Amended 2026-10-06 (kingpin spec, lore review item 6):** a **seizure** is the one other permitted overwrite. When a ruler seizes a front clinic (`eotg_aug_kingpin.076`, [cybernetics_v2_kingpin.md](cybernetics_v2_kingpin.md) L17), the seized company becomes the clinic of record. Nothing else removes or overwrites it; the kingpin story's other endings leave it alone.

**Stays generic, and why**

| Lines | Keys | Reason |
|---|---|---|
| 109, 1150–1151 | `init.002.t`, `tier2.014.t` and its comment | Titles stay short and stable |
| 1145–1146, 1685 | `tier2.013.c.success/.failure`, `init.007.a.success` | Duel-outcome tooltips. Keep the ripple out of effect text (request). |
| 448 | `init.017.desc` | False hit ("clinical") |
| 469, 471 | Seek Augmentation desc / tooltip | Shown **before** any event, so nothing has been rolled yet. The plural "the clinics, sanctioned and otherwise" is correct as generic. |
| 1795, 1800, 1834, 1836, 2035, 2205, 2206 | `proc.001`, `proc.003`, `proc.005`, `tamper.004` "The clinic." etc. | The provider *type* in the procedure system (request: stays generic) |
| 1908, 1909, 1911, 1948 | `eotg_aug_send_clinic*`, `EOTG_AUG_AI_CLINIC` | Provider widget / AI reason text |
| 2050, 2053, 2063 | realm law effects, `eotg_aug_clinic_closed_tt` | Law text is about clinics as a class |
| 2199 | `self_repair_no_provider_tt` | Tooltip |
| 1463, 1469, 1601–1606 | section comment, `patron.001.t`, Patron modifiers (`eotg_mod_aug_patron_clause*`, `_throttle`) | Titles and modifier descs stay generic. The lien desc must never name the syndicate (U1). |
| 1479–1535, 1737, 1751–1752, 1785–1793, 2178, 2180 | the Patron chain and its init.018 entry | **Named at first mention per desc**: the table in §5.4 lists which keys. Later mentions, `.tt` keys and outcome lines stay "the syndicate". |

**Count, companies and gangs:** 21 distinct hit lines named (17 company lines and 4 gang lines; line 456 carries both lists) and 1 non-hit named (tier1.018), for 23 rewritten keys (§7.1). The Patron lines are counted in §5.4.

### 5.2 Vendors (tier2.013 / .014)

`eotg_aug_roll_vendors_effect` (hand-written):

```
eotg_aug_roll_vendors_effect = {
    eotg_aug_roll_company_except_effect = { VAR = eotg_aug_vendor_careful  EXCLUDE = eotg_aug_vendor_bold }
    eotg_aug_roll_company_except_effect = { VAR = eotg_aug_vendor_bold  EXCLUDE = eotg_aug_vendor_careful }
}
```

The two vendors are always distinct, and the generator guarantees at least 2 companies. **The bold vendor draws from companies**, for these reasons:
- The bold option is lawful in the mechanics: no `eotg_mod_illegal_implants`, no `backstreet` provider, and no realm-law crime.
- A gang vendor would contradict the License law text "Back-street implant work is a crime" (line 2053).
- It is firmware, a product, not a back-street procedure.

"More power now and fewer questions" fits a less careful firm.

tier2.013 is once per character (`eotg_flag_aug_vendor_done`, set in `eotg_on_yearly_aug_tier2_check`). That makes the variables effectively permanent, which the bold-firmware modifier desc needs: it is shown for as long as the modifier lasts. tier2.014 reads them without rolling. An old save that had .013 fire before this change shows the fallback wording (§7.3).

### 5.3 Rolled once: summary

| Variable | Set when | Read by | Can be overwritten by |
|---|---|---|---|
| `eotg_aug_seller_company` (root) | `immediate` of init.001/.002/.006/.018, tier1.002, tier1.019 | the same event | the next company host's `immediate` only |
| `eotg_aug_seller_gang` (root) | `immediate` of init.004/.010/.018 | the same event, init.011 | the next init gang host (impossible once augmented) |
| `eotg_aug_seller_gang` (copycat) | tier1.018 `immediate` | tier1.018 | nothing |
| `eotg_aug_vendor_careful` / `_bold` | tier2.013 `immediate`, once | .013, .014, the modifier desc | nothing (.013 is once per life) |
| `eotg_aug_clinic_of_record` | clinic options of named-company hosts; a seizure (kingpin L17, 2026-10-06) | tier1.002, tier1.019, the Pursue decision desc | the next clinic install, or a seizure |

### 5.4 The Patron syndicate: named from canon (owner ruling, 2026-10-05)

The owner's ruling, verbatim: "Name it from a list, there are many canon syndicates in the setting. Add 'Pill Mob' as the first and only entry, I will populate the list later." The generator ships with `PATRON_NAMED = True`.

1. **List.** There is a third list, `[syndicates]`, containing **canon** syndicates only. The owner maintains it, and it starts with exactly one entry, `the Pill Mob`. It is separate from `[gangs]`, so the Patron never coincides with an invented back-street crew.
2. **One name for the whole story.**
   - **Offer.** Roll `eotg_aug_roll_syndicate_effect = { VAR = eotg_patron_syndicate_passthrough }`, unless that variable is already set, in two places:
     - init.018 `immediate`, when e's gate holds (`eotg_aug_has_patron = no`, no `eotg_flag_aug_had_patron`);
     - patron.001 `immediate`.

     A declined offer keeps the passthrough, so the same syndicate offers again.
   - **Accept.** `eotg_story_aug_patron.on_setup` copies `story_owner.var:eotg_patron_syndicate_passthrough` into the story variable `eotg_syndicate`, then removes the passthrough. It is placed next to the existing envoy and terms passthrough (`common/story_cycles/eotg_augmentation_stories.txt:486-498`) and uses the same var-to-var copy (vanilla `00_animal_effects.txt:395-398`).
   - **Read.**
     - Pre-story texts (init.018 `.desc_syndicate`, `.e`; patron.001) use `eotg_aug_cl_syndicate_offer`, which reads the passthrough.
     - patron.002–.009 use `eotg_aug_cl_syndicate`, which reads `any_owned_story`'s `var:eotg_syndicate`.
3. **How far the name reaches.** I checked this against the story file. The name holds through:
   - patron.001–.006;
   - .007 (a new envoy, inside the same story);
   - .008 (*The Paper*);
   - .009 (*The Collector*).

   A betrayal with no implants does not end the story. It **parks** it at a dormant stage and sets `eotg_paper_sold` (`eotg_augmentation_stories.txt:480-482`; `events/eotg_augmentation_patron.txt:987-993`). The tick then fires .009, so `var:eotg_syndicate` is still there for the collector. The story ends on the owner's death (`on_owner_death = { end_story = yes }`, `eotg_augmentation_stories.txt:531-532`) and is never inherited, so no text after the story needs the name. The envoy and the collector are characters, not name carriers: their lines say "the syndicate envoy" and "the collector" around the first-mention name.
4. **Rival** (patron.006.d, `.d.success`, `.d.failure`). Roll in patron.006 `immediate`:

   ```
   set_variable = { name = eotg_aug_rival_exclude  value = scope:eotg_patron_story.var:eotg_syndicate }
   eotg_aug_roll_syndicate_except_effect = { VAR = eotg_aug_rival_syndicate  EXCLUDE = eotg_aug_rival_exclude }
   ```

   The first line is a var-to-var copy, as in vanilla `hunt_events.txt:4405`. With **one** syndicate in the list, every entry is excluded, so `random_list` picks nothing, `eotg_aug_rival_syndicate` stays unset, and the text reads the fallback "a rival syndicate", which is today's wording. With two or more, the rival is a different canon syndicate. `.d.failure` ("The old syndicate finds out first.") stays generic.
5. **When the owner adds entries later:**
   - New entries only enter **future** rolls.
   - A rolled flag is stored in a variable, so running stories, offers already made (the passthrough) and rivals already rolled keep their syndicate.
   - With a single entry, every Patron story is the Pill Mob. Variety starts with the second entry, and the rival with it.
   - Renaming or deleting an entry turns the stories that used it to "the syndicate" (fallback) until they end. Nothing else breaks.
6. **Loc: name at first mention per desc, "the syndicate" / "the syndicate envoy" afterwards.** Every rewrite still reads correctly with the fallback "the syndicate".

   | Key | First mention |
   |---|---|
   | `eotg_aug_init.018.desc_syndicate` | "…An envoy from [ROOT.Char.Custom('eotg_aug_cl_syndicate_offer')] offers to cover the cost…" |
   | `eotg_aug_init.018.e` | "[syndicate_offer\|U] will pay." |
   | `eotg_aug_patron.001.desc` | "An envoy from [syndicate_offer] has asked for a private audience…" |
   | `eotg_aug_patron.002.desc`, `.003.desc`, `.004.desc`, `.005.desc`, `.005.desc_no_heir` | "The envoy from [syndicate]…", or the first "the syndicate" becomes the name |
   | `eotg_aug_patron.006.desc_betrayal`, `_settlement`, `_writeoff` and their `_absent` forms | the first "The syndicate…" |
   | `eotg_aug_patron.006.d` | "Sell them to [ROOT.Char.Custom('eotg_aug_cl_rival_syndicate')]." |
   | `eotg_aug_patron.006.d.success` | "[rival\|U] pays, and the old one does not find out." |
   | `eotg_aug_patron.007.desc`, `.008.desc`, `.009.desc` | the first "The syndicate…" |

   These stay generic:
   - `.e.tt`;
   - all `.tt` keys, success and failure lines other than `.006.d.success`;
   - the option names;
   - `eotg_aug_patron_paper_sold_tt`;
   - the modifiers;
   - every `.009 c` line.

   That makes 19 rewritten Patron keys. The localizer confirms the exact count against the file.

   **Binding loc guardrails** (lore-keeper, 2026-10-05):
   - **B1. The Patron's loc never imports Pill Mob canon.**
     - Banned: Red Pills, Dr. Pill, Pillwake, Shadow Cartel, Flesh Pledge, souls, psychic essence, "otherworldly", and any drug or addiction.
     - The Patron stays purely commercial and cybernetic, and never touches the Void or the voice register.
     - The name reaches loc **only** through the generated custom loc; it is never typed by hand. Whichever canon syndicate the list holds, the lines must read true for every entry.
   - **B2. No real-world mafia vocabulary:** Don, capo, consigliere, omertà, made man, "the Family" as an organization, fedoras, tommy guns. `patron.005.t` "The Family Clause" stays.
   - **B3. Name at the first mention, then "the syndicate".** Never put `'s` after the name function: write "the syndicate's…" or "… from [syndicate]".
7. **Reprisal P7 and U1 still bind.**
   - P7 matters more now, because the Pill Mob's Flesh Pledge puts soul-binding in canon. The syndicate's name never appears in a sentence with P7's ownership words: "theirs", "the syndicate's again", "back in their hands", "on their schedule", "serviced by them", "under contract", "owned", "obedience", "loyalty", "bound", "leash", or anything about who holds the firmware (`cybernetics_v2_reprisal.md:304`).
   - The lien desc `eotg_mod_aug_patron_clause_final_desc` never names the syndicate (U1). No Patron modifier desc does.
   - The Pale Hand and white-glove ban still holds for imagery.
8. **The canon cost no longer applies.** The lore-keeper's note (an invented name would rule out the Patron being one of the real 866 players) is moot: the names are canon now. The opposite holds instead. The Patron **is** one of the canon syndicates in the list, so the list's chronology is canon-sensitive. A group that only exists after 866 doesn't belong in it (§8.3).
9. **Canon edits applied** (2026-10-05). The Patron rule now reads "Named once per story from the owner's `[syndicates]` list of canon syndicates; 'the syndicate' / 'the syndicate envoy' on later mentions." in:
   - index §5 item 3 (Pill Mob comes off the never-name list for the generated syndicate name only; in hand-written loc, Pill Mob, Pillwake, Red Pills and Dr. Pill stay banned) and item 7;
   - balance §5 item 5;
   - phase5 §2;
   - new_beats §8;
   - procedures (Gate line and §8);
   - reprisal §8.

   The scripter updates the header comment at `events/eotg_augmentation_patron.txt:21-24`.

## 6. Vanilla precedent

| Need | Vanilla | Citation |
|---|---|---|
| Custom loc picks a text from a **character variable holding a flag**, no `random_valid` | `GetAnimalTypeCaptive`, `type = all`, `trigger = { var:captive_animal_type ?= flag:lion }` | `common/customizable_localization/04_ep2_hunt_custom_loc.txt:413-418` |
| …and that variable is set once by an effect | `set_variable = { name = captive_animal_type  value = scope:activity.var:animal_type  years = 5 }` | `events/activities/hunt_activity/hunt_events.txt:4403-4406` |
| A **modifier desc** that reads that variable through `ROOT.Char.Custom` | `add_character_modifier = { modifier = hunt_captive_beast_modifier  years = 5  desc = hunt_captive_beast_modifier_custom_desc }`; loc `[ROOT.Char.Custom('GetAnimalTypeCaptive')]` | `hunt_events.txt:4409-4413`; `localization/english/modifiers/activity_hunt_modifiers_l_english.yml:154` |
| A **story's** name stored once as a flag variable and read by custom loc | `CatStoryName`: `var:story_cycle_cat_name = flag:cat_name_gyb`, rolled by a `random_list` of `set_variable` entries with `trigger` | `common/customizable_localization/00_pet_custom_loc.txt:48-100`; roll at `events/story_cycles/story_cycle_pet_animal_events.txt:108-200` |
| Copying a flag variable to another holder | `transfer_cat_story_cycle_to_effect`: `value = $STORY$.var:story_cycle_cat_name` | `common/scripted_effects/00_animal_effects.txt:395-398` |
| An event-scoped flag read by custom loc (considered, not chosen) | `BG_CounterSkill_*`: `scope:bg_skill_a = flag:diplomacy`, set by `save_scope_value_as` | `00_board_game_custom_loc.txt:5-30`; `00_board_game_effects.txt:72-99` |
| `fallback = yes` text | `wakename_wake` | `common/customizable_localization/00_activity_loc.txt:468-471` |
| A rolled number stored as a variable | `set_variable = { name = root_dice_1  value = { integer_range = { min = 3 max = 18 } } }` | `events/activities/tournaments/ep2_locale_events.txt:1045-1053` |
| `ROOT.Char.Custom` in a decision desc | `hire_physician_decision_desc` | vanilla `localization/english` (grep the key) |

**Why variables, not saved scope values or numbers:**
- **Not saved scopes.** A saved scope dies with the event chain, and the bold-firmware modifier desc and the Pursue decision desc run outside any event. Variables serve all hosts with one mechanism, the captive-animal one, which vanilla also uses in modifier descs.
- **Not integer indices.** Deleting a middle name would silently shift every later name in running saves. With flags, a deleted or renamed name falls back to generic wording instead of showing the wrong one.

## 7. Loc surface

Rules: bare scope names (`[eotg_copycat.Custom(...)]`), `[ROOT.Char.Custom(...)]` for root, as vanilla and as the mod already does (`[ROOT.Char.GetHerHis]`). One definition per key. L010–L016 must pass.

**Grammar contract.** Every name function returns a **complete noun phrase** with no article needed: companies are singular and bare, gangs are plural with "the" built in, fallbacks are full phrases. So:
- use `|U` at the start of a sentence;
- **never attach `'s`** to a name function (names can end in s); write "the report from [X]";
- only gang lines take a plural verb, and only company lines a singular one.

### 7.1 Host lines rewritten (23 existing keys, localizer)

These are proposed drafts, kept in the current register. The localizer finalizes them. The voice follows the list: company lines stay clinical and commercial (representative, proposal, waiting list, warranty), and gang lines stay street (cheap, fast, no questions).

| Key | Draft (changed part) |
|---|---|
| `eotg_aug_init.001.desc` | "A representative from [ROOT.Char.Custom('eotg_aug_cl_company')] is already here…" |
| `eotg_aug_init.002.desc` | "A representative from [company] arrives at court with a carefully worded proposal…" |
| `eotg_aug_init.004.desc` | "…a field technician who works for [gang], with unlicensed hardware and no medical certification…" |
| `eotg_aug_init.006.desc` | "…A technician from [company] has laid the specifications on the table." |
| `eotg_aug_init.006.desc_congenital` | "…The technician from [company] is careful to say what the contract covers…" |
| `eotg_aug_init.010.desc` | "[gang\|U] run a clinic with no name and no certificate on the wall. They work cheap…" |
| `eotg_aug_init.011.desc_discovered` | "Word has got out. Someone saw the incision, or saw you leave [gang], or paid to know…" |
| `eotg_aug_init.018.desc` | "…[company\|U], with records and a waiting list. [gang\|U], with neither. And a closed door…" |
| `eotg_aug_init.018.a` | "[company\|U], a sanctioned clinic." |
| `eotg_aug_init.018.b` | "[gang\|U], in the back streets." |
| `eotg_aug_tier1.002.desc` | "The newest model from [company] has arrived in the capital…" |
| `eotg_aug_tier1.002.desc_sought` | "You sent for [company], and the technician came…" |
| `eotg_aug_tier1.018.desc` | "…went to [eotg_copycat.Custom('eotg_aug_cl_gang')] for the same…" |
| `eotg_aug_tier1.019.desc_worse` | "…failing in ways [company] cannot name…" |
| `eotg_aug_tier1.019.desc_dead` | "The report from [company] is short and clinical…" |
| `eotg_aug_tier2.013.desc` | "Two vendors have heard you are in the market. [careful\|U] offers tested hardware… [bold\|U] offers more power now and fewer questions…" |
| `eotg_aug_tier2.013.a` / `.b` | "[careful\|U]: the careful offer." / "[bold\|U]: the bold offer." |
| `eotg_aug_tier2.014.desc_played` | "[careful\|U] and [bold] are back, each with a sharper offer…" |
| `eotg_aug_tier2.014.desc_waited` | "…The warranty from [careful] has shortened. The firmware from [bold] has matured…" |
| `eotg_aug_tier2.014.a` / `.b` | "The new offer from [careful]." / "The new offer from [bold]." |
| `eotg_decision_aug_pursue_next_stage_desc` | "…and [ROOT.Char.Custom('eotg_aug_cl_clinic_of_record')] will book you whenever you send word." |

`tier2.014.d` (tier-options batch, "Read their faces through the overlay while they haggle.") stays as it is. "their" already means the vendors.

### 7.2 New keys

- `eotg_mod_aug_bold_firmware_vendor_desc` (localizer): "The firmware from [ROOT.Char.Custom('eotg_aug_cl_vendor_bold')] is aggressive and lightly tested. It buys reaction speed the implant was never meant to produce."
- Generated name keys `eotg_aug_seller_co_<id>` (12) and `eotg_aug_seller_gang_<id>` (12), plus the fallbacks in §7.3.

### 7.3 Fallback text (fixed in the generator)

| Key | Text | Reads as |
|---|---|---|
| `eotg_aug_seller_fallback_company` | `a sanctioned clinic` | "A representative from a sanctioned clinic" |
| `eotg_aug_seller_fallback_gang` | `back-street operators` | "Back-street operators run a clinic" (plural, like gang names) |
| `eotg_aug_seller_fallback_vendor_careful` | `the careful vendor` | "The careful vendor offers tested hardware" |
| `eotg_aug_seller_fallback_vendor_bold` | `the bold vendor` | "The firmware from the bold vendor" |
| `eotg_aug_seller_fallback_clinic_of_record` | `a sanctioned clinic` | the Pursue desc as it reads today |
| `eotg_aug_seller_fallback_syndicate` | `the syndicate` | today's wording |
| `eotg_aug_seller_fallback_rival_syndicate` | `a rival syndicate` | today's wording |

Option names (init.018.a/.b, tier2.013/.014 a/b) can read awkwardly on fallback, for example "A sanctioned clinic, a sanctioned clinic." That happens only on a cold console fire or an old save. Rolls happen in the same event, so live play never shows it. This is accepted.

### 7.4 Voice variants: zero runtime branches

The request allows light voice variants. None are needed at runtime: **no host slot ever draws from both lists**. init.018 shows one of each in fixed positions, and the vendors are both companies. So the register is decided per host when the line is written (§7.1), and no custom loc branch or alternate desc key is added. If a later host does mix lists in one slot, the place to add a variant is a `parent`/`suffix` custom loc pair (format in `reference/common/customizable_localization/_custom_loc.info`), not a second desc.

No vanilla string needs a `replace/` override.

## 8. Lore constraints

### 8.1 Seller naming vs the licensing rule (ruled 2026-10-05)

1. **Firms may be named (confirmed).** Index §5 item 3 now opens with this binding text: "Licensing is always local, and the licensing authority is never named: no court, regulator, registry or licensing body appears in text. Sellers (clinics, fitters, dealers and back-street crews) may be named from the CB-42 lists (`cybernetics_v2_seller_names.md`). 'Sanctioned' always means sanctioned under the realm's own law." Balance §5 item 5 now reads: "The Pursue decision names the clinic of record, or reads 'a sanctioned clinic' when there is none." init.018.a keeps "a sanctioned clinic" after the name (§7.1).
2. **Compatible with P&D's 866 monopoly, on one condition** (`REVIEW_866.md:33`). **Companies fit, service and deal in hardware; they never make it.**
   - No loc line may say that a vendor built or designed hardware. "The firmware from [bold] has matured" (tier2.014) stays, and so do the warranty and "tested hardware" lines.
   - The localizer re-reads every §7.1 draft against this.
   - Manufacturing words are banned in company names (§8.3).
3. **The salvage buyer stays unnamed (confirmed)** (`cybernetics_v2_interactions.md:841`). No gang name may evoke salvage (word bans in §8.3).
4. **The bold vendor draws from companies (confirmed)** (§5.2).

### 8.2 Patron

**Reversed by the owner, 2026-10-05.** The Patron's syndicate is "Named once per story from the owner's `[syndicates]` list of canon syndicates; 'the syndicate' / 'the syndicate envoy' on later mentions." This is now the text in the index, balance, phase5, new_beats, procedures and reprisal specs (§5.4 item 9). The licensing authority is still never named (§8.1). Reprisal P7 and U1 still bind (§5.4 item 7).

### 8.3 Names brief (localizer drafts, lore-keeper checks)

**Counts and setting:**
- 12 companies and 12 gangs, all invented.
- 866 AG: implants are common and commercial (`REVIEW_866.md:33`).
- Licensing is local, so companies are **local firms**: a practice, a fitting house, a dealer. They are not a state programme and not a galactic megacorp.
- **Companies fit, service and deal in hardware; they never make it.**
- Nothing in any list may imply reach beyond one realm.

**Company names:**
- Small, local and commercial. Singular, used with no article.
- Fine: invented surname partnerships, a trade word.
- Banned words (generator): Corp, Co., Inc, Ltd, Holdings, Industries, Group, plus the manufacturing words Works, Foundry, Fabrication(s), Manufactory, Dynamics and Labs.
- Header example: **Merrow & Tallis Surgical** ("Vane" collides with canon).

**Gang names:**
- Plural street names that read naturally after "the". Header example: **Low Wires**.
- Banned words (generator): Mob, Cartel, Market, Contract, Saint(s), Angel(s), Apostle(s), Sinner(s), and "Black" as the first word.
- No salvage words (generator): scrap, salvage, concrete, slate, ash.
- No real-world gang or organized-crime names (no Triad, Yakuza, Bratva, cartel names, motorcycle clubs).

**Banned words in every list** (generator, whole word, case-insensitive):
- System(s): the reflavor glossary uses County→System.
- Titan, Exodus, Grip, Stellar, Galactic, Interstellar.
- Pale, Bone, Shard, Rift, Hollow, Silent, Eye, Wake.
- Pact, Directive, Corps, Network, Clan(s).
- "Red" as the first word.

**Never-name list** (index §5.2/§5.3/§5.7). The generator enforces it from the L012 register plus the new `name_never` list.
- **`name_never`, single terms:** Tribunal, Helix, Pale Hand, Consortium, Compact, Continuity, Rooks, League, Corp, Co., Inc, Xerxes.
- **`name_never`, organizations** (lore-keeper, 2026-10-05): Black Cogs, Chains of Greed, Jade Pact, Iron Pact, Stellar Compact, Ashen Compact, Scaled Compact, Forged Compact, Slate Syndicate, Titanium Directive, Enforcer Corps, Specter Drones, Council of Executives, Pump & Dump, New Cauldron, Voidspire.
- **Already in the register:** Blackstar, Shadow Market(s), Black Contract(s), Blackline, P&D, Calix, Pill Mob, Pillwake, Red Pills, Concrete Cartel, Acathea, Codex, Archivist(s), Conclave, Carrigore, Trauma Team, Galactic League, "galactic", "interstellar regulation".
- **Not machine-checkable (lore-keeper):** any canon faction, nation, house or company in `docs/lore/` or `intake/`.

**Culture-neutral:**
- No real-world national or ethnic name forms, and no species-marked forms. Use plain invented surnames and trade words.
- Per-culture pools stay deferred (§10).

**Imagery and register:**
- No hand, glove or white-glove imagery in any list (the Pale Hand rule, applied broadly).
- No Void, whisper, Orrin, "the Eye" or demon register.
- No monotheistic words.
- **No Nikios Khanate** names and no khanate or steppe-khan flavour (CLAUDE.md invariant 9).
- Multi-species: no human-only markers ("Mankind", "Human").

**Spelling and form:**
- Canadian English. The generated loc runs through L013b, so "Center", "Armor" or "Color" in a name is caught.
- At most 32 characters, using only the characters in §4.2.

**Sign-off:** the lore-keeper checks the 24 starting names against the `intake/regions/myr_clusters/` culture, dynasty and ruler briefs, as well as against `docs/lore/` (§9 item 9).

**Syndicates (owner-entered canon names; lore-keeper ruling, 2026-10-05).**
- **Seed entry:** `the Pill Mob`.
- **Form:** the owner enters each name in its exact printed form, with the article only if canon uses one (`Samulo's Tieflings` takes none).
- **Dropped for this list only:**
  - the never-name / L012 check;
  - the suffix and word bans;
  - the "the is built in" rule;
  - the invented-name requirement;
  - culture-neutral spelling;
  - the Patron-specific bans (Consortium, Compact, Continuity, Rooks, Pact, Combine, Directive, Hand, "Syndicate" in the name).

  Apostrophes are allowed.
- **Hard rejects, `syndicate_never` (generator, exit 1):**
  - Helix, Pale Hand;
  - the authorities: Acathea, Codex, Archivist(s), Conclave, Tribunal, League, Galactic;
  - New Cauldron;
  - post-866 entities: Slate Syndicate, Broken Ledger, Ashen Compact;
  - planar names: Orrin, Kyros, the Eye, Void, Carrigore;
  - Nikios;
  - Trauma Team.
- **Format rules, still enforced:** 32 characters, the character set, no duplicates (within and across lists).
- **Warn but allow, `syndicate_warn` (generator prints, exit 0; the owner decides):** P&D, Calix, Black Cogs Consortium.
- **Not machine-checkable (advisory review by the lore-keeper when entries are added):** the group exists as a syndicate by 866, and its canon does not contradict the chain (for example remote-kill hardware, index §5.3). The loc guardrails B1–B3 (§5.4 item 6) keep any entry's other canon out of the text.
- **Lint:** L012 skips the generated `eotg_aug_seller_syn_*` keys (`exempt_key_regex`) and stays on all hand-written loc. Host lines call `Custom()`, which L012 strips before matching, so a canon name reaches the player only through the generated keys.

## 9. Definition of done

1. **Classification holds.** Every line in §5.1's "named" tables calls a `eotg_aug_cl_*` function. A diff shows every "stays generic" key byte-identical to before, including the Patron modifier descs and every `.009 c` line.
2. **No re-roll between desc and options.** No `eotg_aug_cl_*` key has `random_valid`, and every one reads a `var:` (grep). In game: for each rolling host, fire it from the console (`event eotg_aug_init.018` etc., `docs/qa/HOW_TO_TEST_IN_GAME.md` §2). The company and gang in the desc must match the names in options a/b, and must not change after hovering every option, closing and reopening tooltips, or switching the time speed.
3. **The story keeps its seller:**
   - **tier2.013 → .014:** take .013.c (on success) or .013.e. When .014 fires, it names the same careful and bold vendors as .013, and they are two different companies.
   - **Bold firmware:** after .013.b or .014.b, the bold-firmware modifier tooltip names the bold vendor.
   - **init.010 → init.011:** the `desc_discovered` gang is the init.010 gang (force it with the discovered branch).
   - **Clinic of record:** after a clinic install in init.001/.002/.006/.018, tier1.002 and the Pursue decision desc name that same clinic.
4. **Cold fires read correctly.** tier2.014 fired cold shows "the careful vendor" / "the bold vendor". The Pursue decision desc with no record shows "a sanctioned clinic". No raw keys and no empty brackets appear.
5. **Owner-file round trip:**
   - (a) add a 13th company and a 13th gang to `cybernetics_seller_names.txt`;
   - (b) `python docs/tools/check_all.py --only gen_seller_names` fails with "stale";
   - (c) `python docs/tools/gen_seller_names.py` prints `companies: 13  gangs: 13`;
   - (d) `check_all` passes;
   - (e) the custom loc file has 13 company texts in each of the four company keys plus a fallback, and each roll effect has 13 entries;
   - (f) in game, `effect = { set_variable = { name = eotg_aug_clinic_of_record value = flag:eotg_aug_co_<new_id> } }` makes the Pursue decision desc show the new name;
   - (g) delete the name again, regenerate, and the same desc shows "a sanctioned clinic".
6. **`--check` rejects bad input:**
   - a duplicate;
   - an id collision;
   - a gang starting with "the";
   - "Pill Mob" under `[gangs]` (register; the same name passes under `[syndicates]`), "Helix" and "the Codex" under `[syndicates]` (`syndicate_never`, exit 1), "P&D" under `[syndicates]` (a warning, exit 0), "Samulo's Tieflings" under `[syndicates]` (passes, apostrophe allowed), "Helix Surgical" (`name_never`), "Blackstar Fittings" (register), "Tallis Works" (company word ban), "Scrap Kings" (gang salvage ban), "Red Lanterns" (leading Red), "Low Saints" (gang word ban);
   - a `"` in a name;
   - one company only;
   - an empty `[syndicates]`.

   Each case exits 1 and names the list file line.
7. **Lint, BOM, Tiger, PX:**
   - eotg_lint L010–L016 pass. There are no L014 warnings on generated keys (§4.3), and L016 sees exactly one BOM in each generated file.
   - Tiger is clean except the known-benign list in CLAUDE.md.
   - The PX LSP and vocab checks are clean, and `px_event_report` shows no new unreachable events.
8. **No behaviour change:**
   - **Events and options:** the event count and option count are unchanged.
   - **Effect diffs:** limited to the new `immediate` rolls, the `eotg_aug_record_clinic_effect` calls, and the two modifier `desc =` lines.
   - **Built behaviour:** the procedure roll, providers, `eotg_aug_has_surgeon_for`, the booking guard, realm law and clinic gating, and the Patron paper and story all diff to nothing.
   - **Generated reports:** `spec_conformance --check` and `gen_test_recipes --check` pass after regenerating.
9. **Names approved:** the lore-keeper signs off the 24 starting names against §8.3, the `intake/regions/myr_clusters/` culture, dynasty and ruler briefs, and `docs/lore/`. The owner has been shown the file (CB-42 next step).
10. **Patron name across the story.**
   - Accept patron.001: the name in .001 is the name in .002–.007.
   - Force the betrayal with no implants: the story parks, and .009 names the same syndicate.
   - With only `the Pill Mob` in the list, patron.006.d reads "a rival syndicate".
   - Add a second canon syndicate and regenerate: in an already-running story the name doesn't change, and a new story's .006.d names the other syndicate.
   - No sentence carrying the name contains a P7 ownership word (grep), and `eotg_mod_aug_patron_clause_final_desc` is unchanged.

## 10. Deferred

| Item | Why |
|---|---|
| Patron modifier descs (`eotg_mod_aug_patron_clause*`, `_throttle`) | Keeps the ripple small. The lien desc never gets the name (U1), and the others could take a `desc =` later using the bold-firmware pattern. |
| Region weighting of the `[syndicates]` list | Waits for the real map (lore-keeper, 2026-10-05) |
| Filling `[syndicates]` beyond Pill Mob | The owner's task ("I will populate the list later"). The lore-keeper reviews additions. |
| "Technician" and "surgeon" lines (init.003, init.007, tier1.007, tier1.021, tier2.003, end.001, the maintenance decision) | Not seller-generic hits. Adding them is new scope. A follow-up can reuse `eotg_aug_cl_clinic_of_record`. |
| The salvage buyer | Canon: stays unnamed (`interactions.md:841`) |
| Duel-outcome, tooltip and law text | Effect text stays generic (request) |
| Per-name voice or weights | Each host has a fixed list, so per-name voice isn't needed (§7.4). Weights are always 1. |
| Region-, culture- or faith-specific name pools | Would depend on the map, culture and faith. Mod-exclusive rule; revisit after Gate 1. |
| Clinic of record passing to the heir | New behaviour. The heir meets their own sellers. |
| Explicit stable ids in the list file | Simpler for the owner. The cost is generic wording in a running story after a rename (stated in the file header). |

---

### HANDOFF
- status: done
- next: eotg-scripter
- ask: Build §4–§5 of docs/specs/cybernetics_v2_seller_names.md, including the §5.4 Patron naming (PATRON_NAMED = True, [syndicates] = the Pill Mob), syndicate_never / syndicate_warn, the L012 exemption, and B1–B3 for the localizer. Then the localizer does the 23 + 19 rewrites and drafts the 24 invented names, and the lore-keeper signs off.
- files: docs/specs/cybernetics_v2_seller_names.md, docs/specs/cybernetics_v2.md, docs/specs/cybernetics_v2_balance.md, docs/specs/cybernetics_v2_phase5.md, docs/specs/cybernetics_v2_new_beats.md, docs/specs/cybernetics_v2_procedures.md, docs/specs/cybernetics_v2_reprisal.md
- needs-loc: 23 seller keys (§7.1), 19 Patron first-mention keys (§5.4 item 6), eotg_mod_aug_bold_firmware_vendor_desc, 12 company + 12 gang names
- needs-lore: sign-off of the 24 invented names; advisory review of future [syndicates] additions
- needs-human: none (Q3/Q4 defaults taken: list at the repo root; generic fallback on rename/delete)
