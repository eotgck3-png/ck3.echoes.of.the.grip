# Cyberware portraits: shipping spec

> **Owner rulings (2026-11-03):** git LFS approved (binaries `.mesh`/`.dds` only; LFS set up in the main checkout: `git lfs install --local`, root `.gitattributes`). Prosthesis flags are **kept** on full augmentation removal. SH1 setup done by the orchestrator.

**Status:** spec, 2026-11-03 (eotg-architect). Owner approved shipping the finished set (2026-11-03 dispatch).
**Source set:** MCP asset workspace `C:/Users/river/MCP`, which is outside this repo. The source files are:
- `staging/cyberware/CATALOG.md` (21 items, QA verdict SHIP-READY 2026-10-26, §8);
- `staging/cyberware/eotg_wiring/EOTG_WIRING_PROPOSAL.md`;
- `staging/cyberware/eotg_wiring/eotg_cyberware_portrait_modifiers_draft.txt` (2,438 lines, sha256 `d5c6242a0dc8b0029979bf016c3ef2a2905154cfe4993f36e903f9f0df83f879` after the SH4 none-weight fix, 2026-11-03);
- `staging/cyberware/BRIEF.md` and `ENGINE_NOTES.md` (vanilla-scout, 2026-10-26).

**Game:** CK3 1.20.1.1.

All line numbers below were re-checked on 2026-11-03 against HEAD `97c3c8a`. The proposal's numbers still hold, except where this spec says otherwise.

---

## 1. Purpose & gate

This spec puts EotG cybernetics on the character portrait. A character's implants show their tier, their end state (Neurofractured or Seamless) and their finish (clinic or back-street). A set of crew and faction wearables (earpiece, visor, rebreather, collar, harness, badge, Cartel Mark) shows by role and by government.

The work has four parts:
- import 2,803 generated files from the MCP workspace;
- add a small set of character flags to the existing augmentation effects;
- add one scripted-trigger file;
- generate two portrait-modifier files from the MCP wiring draft.

**Gate:** this is part of the cybernetics system, so it is **mod-exclusive and exempt from Gate 1** (decided 2026-10-02). The wearables read only the government identity flags of PMC, Corporation, Gob-Corp and Cartel, which are also exempt (2026-10-08). They also read vanilla court positions and one EotG court position. Nothing references a title, province, character, culture or faith. The race-shape triggers stay `always = no` placeholders until races exist (§3, §10). **The work is not blocked.**

## 2. Signature resource

The system has no resource of its own. **It renders the cybernetics state, and every portrait entry reads part of it:**

- **Tier:** two new flags, `eotg_aug_tier_enhanced` and `eotg_aug_tier_overclocked`. They mirror the `eotg_cybernetics` track (XP 50 and 100) and stay through Neurofractured and Seamless.
- **End state:** the traits `eotg_neurofractured` and `eotg_total_integration`.
- **Finish:** `eotg_aug_backstreet_fitted`.
- **Focus:** `var:eotg_aug_focus`.
- **Prostheses:** `eotg_aug_prosthetic_eye`, `_arm` and `_leg`.

There are **no events** in this system. The DoD check is the reverse of the usual one: every entry in file B reads at least one of these, and nothing outside §5's setter sites writes them.

## 3. Identifier table

### 3.1 New script identifiers (EotG side)

| Key | Type | Owner | Notes |
|---|---|---|---|
| `eotg_aug_tier_enhanced` | character flag (permanent) | scripter | Set while the track XP is 50 or more (Enhanced **or higher**). Kept through Neurofractured and Seamless. |
| `eotg_aug_tier_overclocked` | character flag (permanent) | scripter | Set while the track XP is 100. Kept through Neurofractured and Seamless. |
| `eotg_aug_backstreet_fitted` | character flag (permanent) | scripter | The character holds back-street hardware. |
| `eotg_aug_prosthetic_eye` | character flag (permanent) | scripter | A lost eye, or sight, was replaced by an optic. |
| `eotg_aug_prosthetic_arm` | character flag (permanent) | scripter | A lost arm was replaced (limb frame over the arm). |
| `eotg_aug_prosthetic_leg` | character flag (permanent) | scripter | A lost leg was replaced (actuator leg plus the vanilla stump morph). |
| `eotg_aug_portrait_tier_sync_effect` | scripted effect | scripter | Keeps the two tier flags in step with the track (§5.2). |
| `eotg_portrait_aug_enhanced_trigger`, `eotg_portrait_aug_overclocked_trigger` | scripted triggers | scripter | **Changed from the draft:** they read the tier flags, not `has_trait_xp` (§5.4). |
| `eotg_portrait_prosthetic_eye_trigger`, `_arm_trigger`, `_leg_trigger` | scripted triggers | scripter | **New, not in the draft.** Flag AND the matching loss trait not held again (§5.4). |
| `eotg_portrait_shows_optic_trigger`, `eotg_portrait_shows_lattice_trigger`, `eotg_wear_earpiece_role_trigger`, `eotg_portrait_cartel_affiliated_trigger` | scripted triggers | scripter | As in draft section A, with the one edit in §5.4. |
| `eotg_portrait_bull_head_trigger`, `_small_frame_`, `_large_frame_`, `_elf_ears_`, `_orc_ears_`, `_goblin_ears_`, `_chad_orc_ears_`, `_tusked_` (all `_trigger`) | scripted triggers | scripter | `always = no` placeholders. `eotg_portrait_human_ears_trigger` is derived from them, as drafted. |
| 11 trait-portrait-modifier groups `eotg_cyber_{eye,cranial,temple,cheek,heatsink,dressing,patch,spine,chest,arm,leg}_portrait` | trait portrait modifier groups | generated (§4.4) | From draft section B. |
| 8 portrait-modifier groups `eotg_wear_{ear,headgear,face,collar,harness,badge,face_mark,brow}_game` | portrait modifier groups (`usage = game`) | generated (§4.4) | From draft section C. |

**Not created:** `eotg_aug_last_xp`. The flag route (proposal §7, recommended by QA) makes it unnecessary, because the tier flags survive `remove_trait = eotg_cybernetics`. It must not appear anywhere in the tree (DoD 7).

### 3.2 Imported identifiers (generated in MCP; never hand-edited here)

| Kind | Count | Pattern |
|---|---|---|
| Accessory genes | **19** (11 head, 8 body) | `eotg_cyber_<slot>`, `eotg_wear_<slot>` |
| Morph (decal) gene | 1 | `eotg_wear_face_mark` |
| Gene templates | 198 (189 accessory, 9 decal), plus one `_none` per gene | `eotg_<item>[_profile]_<side>_<finish>[_race]` |
| Accessories | 378 | `eotg_<item>[_profile]_<m\|f>_<side>_<finish>[_race]` |
| Entities and meshes | 21 `.asset` files | `eotg_<item>*` |
| Barbershop groups | 19, `interface_position` 20–38 | `eotg_custom_cyber_*`, `eotg_custom_wear_*` |
| Loc keys | 259 | 251 `PORTRAIT_MODIFIER_eotg_*` and 8 bare gene names `eotg_*` |

**Catalogue correction:** `CATALOG.md` §1 and §4.1 say 18 accessory genes and 18 accessory files. The files define **19 of each** (12 `eotg_cyber_*`, 7 `eotg_wear_*`), counted 2026-11-03. Use 19.

**Prefix exceptions forced by the engine** (documented here so lint triage does not "fix" them):
- the container keys `special_genes`, `accessory_genes` and `morph_genes`;
- the vanilla null template `empty`;
- the loc-key form `PORTRAIT_MODIFIER_<group>_<entry>`, whose group and entry parts both carry `eotg_`.

The landed-title grep `eotg_[ekdcb]_` matches nothing in any imported file (checked 2026-11-03).

### 3.3 Name lists, CoAs, icons
None needed. The Cartel Mark sigils and the badge marks are unnamed abstract art (lore rulings, BRIEF.md).

## 4. File placement

### 4.1 Binary assets in git: recommendation **git LFS, scoped to the portrait binaries**

**Facts (measured 2026-11-03):**
- **Size:** 2,775 binary-folder files, 610,578,109 bytes (582.3 MiB). That is 2,585 `.mesh`, 169 `.dds` and 21 `.asset`.
- **Largest single file:** 1,398,256 bytes (a 1024² BC3 DDS). This is far below GitHub's 50 MB warning and 100 MB rejection limits, so file size is not the problem.
- **Compression:** `gzip -6` of the set is 216,838,006 bytes. A plain commit would grow the pack by about **207 MiB per full version**, against today's 29.8 MiB pack: a 7× larger repo on the first import. Each rebuild in MCP rewrites every mesh it touches, so each re-sync of a rebuilt item adds its full compressed size again, forever.
- **The MCP workspace is not a git repository** (`git rev-parse` fails there), and nothing else backs it up. The builders are Blender-driven and "rebuild from scratch on every install" (CATALOG §5). Byte-for-byte reproducibility has never been tested, unlike the terrain and marker tools that `.gitignore` relies on, whose sources are tracked here.
- **git-lfs 3.7.1 is installed**, and the global `filter.lfs.*` config is present. But the repo has **no `.gitattributes`** and **no LFS hooks** in `.git/hooks`. Without the `pre-push` hook, a push sends pointers but not objects.
- The game loads the working tree through the junction. After an LFS checkout the working tree holds the real files, so the game is unaffected.

**Options weighed:**

| Option | Verdict |
|---|---|
| Commit as-is | Works within every GitHub hard limit. But it bloats history by about 207 MiB per version, and every cloud-session clone pays that cost. **Fallback** if LFS is refused. |
| **Git LFS** for `*.mesh` / `*.dds` under the two portrait folders | **Recommended.** History stays small (about 0.35 MB of pointers). GitHub holds an off-machine copy, which the MCP workspace lacks. The `.asset` and script files stay plain text, so they diff and Tiger reads them. Cost: LFS storage and bandwidth quota (**owner question**, §10). |
| Gitignore the binaries; MCP is the source; copy step plus checksums | **Rejected.** The repo would hold nothing but a manifest, and the only copy of 582 MiB of finished art would sit on one unversioned disk whose builders are not proven reproducible. The `.gitignore` precedent (terrain, markers) applies only to outputs whose sources are tracked in this repo. |
| Split (text in git, binaries ignored) | Has the same backup flaw as the gitignore option. Rejected. |

**SH1 setup** (the orchestrator does this, since it is the only committer):
1. Run `git lfs install --local` in the main checkout. Confirm that `.git/hooks/pre-push` now exists.
2. Create the root `.gitattributes` **before** the first `git add` of any portrait file, or the files land in plain history:
   ```
   # Portrait cyberware binaries (docs/specs/cyberware_portraits_ship.md §4.1): git LFS
   gfx/models/portraits/eotg_cyberware/**/*.mesh   filter=lfs diff=lfs merge=lfs -text
   gfx/models/portraits/eotg_cyberware/**/*.dds    filter=lfs diff=lfs merge=lfs -text
   gfx/models/portraits/decals/eotg_face_mark/*.dds filter=lfs diff=lfs merge=lfs -text
   # Imported generated text: byte-exact (core.autocrlf is true on this machine), so the manifest hashes hold on every checkout
   gfx/models/portraits/eotg_cyberware/**/*.asset  -text
   common/genes/eotg_*.txt                          -text
   gfx/portraits/accessories/eotg_*.txt             -text
   gfx/portraits/portrait_modifiers/eotg_cyber_*_custom.txt  -text
   gfx/portraits/portrait_modifiers/eotg_wear_face_mark_custom.txt -text
   localization/english/eotg_cyber_*_l_english.yml  -text
   localization/english/eotg_wear_face_mark_l_english.yml -text
   ```
   `-text` turns off line-ending conversion only; `git diff` still works on these files.
3. Confirm the setup: `git check-attr filter -- gfx/models/portraits/eotg_cyberware/optic/eotg_optic_m_l.mesh` prints `lfs`, and `git check-ignore` matches no portrait path. The current `.gitignore` has no rule that touches `gfx/models/portraits/` or `gfx/portraits/`.
4. Add to `docs/cloud_agent_prompt.md`: cloud sessions clone with `GIT_LFS_SKIP_SMUDGE=1`. Portrait binaries there are pointer files; never commit under `gfx/models/portraits/`, and never run the game or portrait QA from a cloud checkout.

### 4.2 Copy plan (source → destination, same relative path)

Source root `C:/Users/river/MCP/ck3_mod/`; destination is the repo root. **Allowlist; nothing else is copied.**

| # | Source (relative) | Files | Kind |
|---|---|---|---|
| 1 | `gfx/models/portraits/eotg_cyberware/**` (20 folders: actuator_leg, chest_housing, corp_badge, crew_collar, dressing, earpiece, face_mark, fitter_harness, heatsink, lattice, limb_frame, optic, panel, patch, rebreather, ring, scorched_actuator, spinal_housing, visor, wrist_servo) | 2,765 (2,585 `.mesh`, 159 `.dds`, 21 `.asset`) | binary (LFS) and `.asset` text |
| 2 | `gfx/models/portraits/decals/eotg_face_mark/*.dds` | 10 | binary (LFS) |
| 3 | `common/genes/eotg_cyber_head_genes.txt`, `eotg_cyber_body_genes.txt`, `eotg_wear_face_mark_genes.txt` | 3 | script |
| 4 | `gfx/portraits/accessories/eotg_cyber_*.txt` (12), `eotg_wear_*.txt` (7) | 19 | script |
| 5 | `gfx/portraits/portrait_modifiers/eotg_cyber_head_custom.txt`, `eotg_cyber_body_custom.txt`, `eotg_wear_face_mark_custom.txt` | 3 | script (barbershop) |
| 6 | `localization/english/eotg_cyber_head_l_english.yml`, `eotg_cyber_body_l_english.yml`, `eotg_wear_face_mark_l_english.yml` | 3 | loc |
| | **Total** | **2,803** | |

**Hard denylist.** The tool refuses these even if a glob would match:
- `descriptor.mod`;
- any **race-kit** path or non-`eotg_` file containing `chad_orc` (amended 2026-11-03: the 30 `eotg_*_chad_orc*.mesh` cyberware variants ship, because three `.asset` files reference them; see `docs/tools/sync_cyberware.py:27-31`);
- `gfx/models/portraits/{male_head,female_head,textures}/` (the race kit overrides vanilla `male_head.asset` / `female_head.asset`; copying them would replace every head in the game);
- `gfx/models/portraits/decals/chad_orc/`;
- `common/ethnicities/`, `gfx/coat_of_arms/`, `gui/`, `interface/`;
- any file whose basename does not start with `eotg_`.

Nothing from `staging/` is copied, including `retired/`, previews and `.npz`. **Close the game before running `copy`:** the junction means the copy writes into the live mod.

### 4.3 Sync tool: `docs/tools/sync_cyberware.py`

The tool uses the standard library only (`argparse`, `hashlib`, `json`, `pathlib`, `shutil`). It follows the `--check` convention of `docs/tools/gen_seller_names.py`. The scripter writes it in SH1.

```
python docs/tools/sync_cyberware.py plan   [--src C:/Users/river/MCP]   # dry run: added / changed / removed / unchanged, totals; exit 0
python docs/tools/sync_cyberware.py copy   [--src ...]                  # copy the allowlist, generate B and C (§4.4), write the manifest
python docs/tools/sync_cyberware.py verify [--report PATH]              # hash the working tree against the manifest; needs no MCP
python docs/tools/sync_cyberware.py copy --check                        # copy nothing; exit 1 if anything would change (stale import)
```

**Rules:**
- **Refuse to run** unless `--dst` (default: the repo root above `docs/tools/`) contains `echoes_of_the_grip.mod`, and unless `--src/ck3_mod/descriptor.mod` exists (a sanity check that this is the MCP workspace).
- **Allowlist and denylist** as in §4.2. Any file found under an allowlisted folder that breaks the `eotg_` basename rule, or whose extension is not `.mesh`, `.dds`, `.asset`, `.txt` or `.yml`, stops the run with exit 1. Nothing is skipped silently.
- **Removals:** `copy` deletes a destination file only if it is listed in the **previous** manifest and no longer exists in the source (for example a mesh a builder retired). It never touches a file that is not in the manifest.
- **Pre-copy checks** (exit 1 on failure):
  - every `.yml` starts with the UTF-8 BOM and has `l_english:` on its first line;
  - no imported loc key is defined anywhere else under `localization/` (including `replace/`);
  - no file is 100 MB or larger; files of 50 MB or more produce a warning.
- **Manifest:** `docs/tools/cyberware_manifest.json` (tracked). It records:
  - `tool_version`, `source_root` and `generated_at`;
  - `catalog_sha256` (MCP `CATALOG.md`) and `draft_sha256` (the wiring draft);
  - per file: `dst`, `src`, `bytes`, `sha256`, and `kind` (`lfs` / `text` / `generated`);
  - totals per kind.
- **`verify`:**
  - re-hashes every manifest file in the working tree;
  - reports missing, changed and extra `eotg_` files in the managed folders;
  - **detects LFS pointer files**: under 1 KB and beginning `version https://git-lfs`. The game would try to load these as meshes. This is how a skip-smudge checkout is caught.
  - exits 1 on any finding;
  - with `--report`, writes a plain-text checksum report: one line per file, then the totals. Write the report to the scratchpad, not the repo.
- **Draft drift:** `plan` and `copy --check` warn when the MCP draft's sha256 differs from the manifest's `draft_sha256`. That means B and C must be regenerated (`copy` does both in one run).

### 4.4 Generated wiring files B and C

`copy` extracts **section B** and **section C** from the MCP draft into:
- `gfx/portraits/trait_portrait_modifiers/eotg_cyber_trait_modifiers.txt` (section B, 11 groups);
- `gfx/portraits/portrait_modifiers/eotg_wear_game.txt` (section C, 8 groups, `usage = game`, `priority = 7`).

**Exactly three textual substitutions are applied to section B and nothing else.** Each is a whole-token match, and each count must equal the count measured on 2026-11-03, or the run stops:

| From | To | Count in B |
|---|---|---|
| `has_character_flag = eotg_aug_prosthetic_eye` | `eotg_portrait_prosthetic_eye_trigger = yes` | 10 (the 11th is in section A) |
| `has_character_flag = eotg_aug_prosthetic_arm` | `eotg_portrait_prosthetic_arm_trigger = yes` | 15 |
| `has_character_flag = eotg_aug_prosthetic_leg` | `eotg_portrait_prosthetic_leg_trigger = yes` | 9 |

Per-section counts, verified 2026-11-03 (draft lines 86–1849 are B, 1850–2438 are C):
- eye: A 1, B 10, C 0;
- arm: B 15;
- leg: B 9.

Section C is copied without changes. Each output file starts with a BOM and this header:

```
# GENERATED by docs/tools/sync_cyberware.py from MCP eotg_cyberware_portrait_modifiers_draft.txt
# (draft sha256 <hash>). Do not hand-edit: change MCP staging/cyberware/work/gen_wiring_draft.py and re-sync.
```

**Section A is not generated.** It becomes the scripter-owned `common/scripted_triggers/eotg_portrait_triggers.txt`, because the tier triggers diverge from the draft (§5.4).

### 4.5 Ownership of the new folders

`gfx/` has no owner in `docs/agent_workflow.md` §1. The proposal:
- **eotg-scripter** owns `gfx/portraits/` and `gfx/models/portraits/`, as imported generated content plus the tool;
- **eotg-localizer** reviews the three imported `.yml` files but does not edit them, since they are generated.

The orchestrator records this in §1.

### 4.6 Additions to CLAUDE.md "File placement" (the orchestrator edits CLAUDE.md)

Append this to the list:

> plus `common/genes/`, `gfx/portraits/accessories/`, `gfx/portraits/portrait_modifiers/`, `gfx/portraits/trait_portrait_modifiers/` and `gfx/models/portraits/` (decals in `gfx/models/portraits/decals/`) (cyberware portraits, 2026-11-03; `docs/specs/cyberware_portraits_ship.md`). The `eotg_cyber_*` / `eotg_wear_*` files there, the 20 model folders and the face-mark decals are **imported** from the MCP workspace by `docs/tools/sync_cyberware.py`; the two wiring files are **generated** by it. Never hand-edit any of them. The binaries are git LFS (`.gitattributes`).

Also add one line under Validation: run `python docs/tools/sync_cyberware.py verify` before any in-game portrait test.

## 5. Wiring

There are no on_actions, events or cooldowns. Portrait modifiers are evaluated by the engine. The flags are set inside existing effects, so they reach every tier and every role: rulers, knights, courtiers and children (a child sees nothing until adulthood, because of the adult gate).

### 5.1 `eotg_aug_backstreet_fitted`: set once, at the shared roll

**Deviation from the proposal, with the reason.** The proposal sets the flag in `eotg_aug_procedure_effect` (`:2528`). But six back-street installs call `eotg_aug_procedure_roll_effect` **directly** and never pass through it:
- `eotg_aug_offer_install_effect` (`common/scripted_effects/eotg_augmentation_effects.txt:2774`);
- `events/eotg_augmentation_initiation.txt:1731`, `:1783`, `:1822` and `:3176`;
- `events/eotg_augmentation_interactions.txt:425`.

The roll is the one point every fitting passes through. That includes `eotg_aug_procedure_roll_booked_effect` (`:2382`).

- **Set:** in `eotg_aug_procedure_roll_effect` (`:2088`), inside the `$PATIENT$ = { … }` block, **between the sponsor block (ending `:2359`) and the death block (`:2360-2363`)**:
  ```
  # Cyberware portraits §5.1: back-street hardware stays visible (patch, khaki casings, amber)
  if = {
      limit = {
          scope:eotg_proc_provider = flag:backstreet
          NOT = { scope:eotg_proc_kind = flag:removal }
          NOT = { scope:eotg_proc_outcome = flag:death }
          eotg_is_augmented_any = yes
      }
      hidden_effect = { add_character_flag = eotg_aug_backstreet_fitted }
  }
  ```
  - **Install, upgrade and repair** all count: each fits a back-street part. Removal does not.
  - `eotg_is_augmented_any` is safe at that point, because every install path adds the trait before the roll touches risk (`:290-297`).
  - A rejected install ends in `eotg_aug_remove_all_effect` through init.012, which clears the flag.
- **Clear:** in `eotg_aug_remove_all_effect` (`:480`), next to the other flag removals (`:493-496`). The flag clears on every exit: Remove Implants, Excision, Rejection, nr.006 and retinue reversal all funnel through it. See `:470-479` and `:1646-1660`.
- **A later clinic refit does not clear it.** The back-street casing and scar stay in the body. This is the drafted behaviour and answers owner decision 7.1-1, unless the owner overrules it.

### 5.2 Tier flags: one effect, two call sites

The new effect goes in `common/scripted_effects/eotg_augmentation_effects.txt`, directly after `eotg_aug_set_integration_effect`:

```
# Cyberware portraits §5.2: the portrait tier flags mirror the eotg_cybernetics
# track (XP 0/50/100). They are read by eotg_portrait_aug_*_trigger and are
# deliberately NOT touched by the Neurofracture or Total Integration effects, so
# the last tier survives the track's removal. Cleared only in
# eotg_aug_remove_all_effect.
# Callers: eotg_aug_initiate_effect, eotg_aug_set_integration_effect.
eotg_aug_portrait_tier_sync_effect = {
    if = {
        limit = { has_trait = eotg_cybernetics }
        hidden_effect = {
            if = {
                limit = { OR = { eotg_is_aug_tier2 = yes  eotg_is_aug_tier3 = yes } }
                add_character_flag = eotg_aug_tier_enhanced
            }
            else = { remove_character_flag = eotg_aug_tier_enhanced }
            if = {
                limit = { eotg_is_aug_tier3 = yes }
                add_character_flag = eotg_aug_tier_overclocked
            }
            else = { remove_character_flag = eotg_aug_tier_overclocked }
        }
    }
}
```

**Call sites:**
- `eotg_aug_set_integration_effect` (`:158`): insert `eotg_aug_portrait_tier_sync_effect = yes` between `add_trait_xp` (ending `:177`) and `eotg_aug_refresh_synergy_effect` (`:178`). This is the **only** writer of track XP in the tree (grep `add_trait_xp`: one hit, `:171`), so every promotion and regression (partial removal to XP 0, downgrade to XP 50, `:2581` and `:2593`) passes through it.
- `eotg_aug_initiate_effect` (`:130`): insert the same call after `add_trait = eotg_cybernetics` (`:144`). On a re-initiation, this keeps flags from a stale earlier state off an XP-0 track.

**Clear:** in `eotg_aug_remove_all_effect`, add `remove_character_flag = eotg_aug_tier_enhanced` and `remove_character_flag = eotg_aug_tier_overclocked` next to `:493-496`.

**No change** at these sites, by design, because the flags must outlive the track:
- `eotg_trigger_neurofracture` (`:314-315`);
- `eotg_aug_nr_cascade_effect` (`:1672-1673`);
- `eotg_aug_total_integration_effect` (`:1138-1140`).

**Engine note.** The tier triggers read `has_trait_xp` immediately after `add_trait_xp` in the same effect. The in-game walk (§9.2 T2) confirms that the value is already updated at that point. If it is not, pass the target tier in as a parameter instead.

### 5.3 Prosthesis flags: eight setter sites, no automatic clear

Each flag is set **inside the guarded block that actually removes the loss trait**, wrapped in `hidden_effect`. That is the repo pattern for hidden state (`:2677-2680`).

| Flag | `eotg_aug_restore_loss_effect` (`:555`) | `eotg_aug_repair_injury_effect` (`:2626`) |
|---|---|---|
| `eotg_aug_prosthetic_eye` | `blind` branch `:558`; `one_eyed` branch `:570` | `one_eyed` `:2653`; `blind` `:2660` |
| `eotg_aug_prosthetic_leg` | `one_legged` `:562` | `one_legged` `:2646` |
| `eotg_aug_prosthetic_arm` | `maimed` `:566` | `maimed` `:2635` |

The callers of `restore_loss` are `eotg_aug_offer_install_effect` (`:2761`) and `events/eotg_augmentation_initiation.txt:905`, `:966` and `:1030`. The repair callers are `eotg_aug_procedure_apply_effect` and proc.004. No other site in `common/` or `events/` removes these four traits (grep, 2026-11-03).

**What happens when the loss trait comes back.** Vanilla and EotG re-add these traits in many places:
- EotG adds `maimed` at `:1312` (excision), `:3932` (inheritance excision), `events/eotg_augmentation_nonruler.txt:1208` and the apply effect `:2485-2508`;
- vanilla adds them in battles, duels and torture.

There is no clean hook for every one of those. So **the guard lives in the portrait triggers, not at the add sites** (§5.4): a prosthesis entry is skipped while the matching loss trait is held. The vanilla stump, eye patch, blindfold or missing-arm morph then shows, and the arm group falls through to its `maimed` (right-arm) entries. A later repair sets the flag again, which is harmless.

**Full exit:** the default is to **keep** the prosthesis flags in `eotg_aug_remove_all_effect`. That effect does not give the loss trait back. The limb is mechanically whole, so the prosthesis must still be drawn on it. The draft's plain prosthesis entries require no augmentation trait, so they keep showing. This is owner decision 7.1-4 (§10). If the owner rules "clear", add three `remove_character_flag` lines in `remove_all`.

**Side effect of keeping them:** `eotg_aug_backstreet_fitted` clears on exit, so a kept back-street prosthesis is redrawn with the clinic finish. This is accepted as minor (§10).

### 5.4 `common/scripted_triggers/eotg_portrait_triggers.txt` (new; from draft section A)

The scripter copies draft section A (draft lines 31-84) with these changes:
1. **The tier triggers become flags:**
   ```
   eotg_portrait_aug_enhanced_trigger = { has_character_flag = eotg_aug_tier_enhanced }
   eotg_portrait_aug_overclocked_trigger = { has_character_flag = eotg_aug_tier_overclocked }
   ```
   The draft's `has_trait_xp` and `eotg_aug_last_xp` lines (draft `:32-43`) are dropped.
2. **New prosthesis guards:**
   ```
   eotg_portrait_prosthetic_eye_trigger = {
       has_character_flag = eotg_aug_prosthetic_eye
       NOT = { has_trait = one_eyed }
       NOT = { has_trait = blind }
   }
   eotg_portrait_prosthetic_arm_trigger = {
       has_character_flag = eotg_aug_prosthetic_arm
       NOT = { has_trait = maimed }
   }
   eotg_portrait_prosthetic_leg_trigger = {
       has_character_flag = eotg_aug_prosthetic_leg
       NOT = { has_trait = one_legged }
   }
   ```
3. **In `eotg_portrait_shows_optic_trigger`**, `NOT = { has_character_flag = eotg_aug_prosthetic_eye }` (draft `:48`) becomes `eotg_portrait_prosthetic_eye_trigger = no`.
4. The file starts with a BOM and a header citing this spec. The race placeholders stay `always = no`, with the draft's comments kept; they list which kits each trigger will cover.

`eotg_is_augmented_any` already exists (`common/scripted_triggers/eotg_augmentation_triggers.txt:7`), as do `eotg_is_aug_tier2` and `eotg_is_aug_tier3` (`:41`, `:56`). The government flags exist: `eotg_cartel_government.txt:86`, `eotg_corporation_government.txt:56`, `eotg_gobcorp_government.txt:57` and `eotg_pmc_government.txt:57`. So does the court position (`common/court_positions/types/eotg_augmentation_court_positions.txt:20`). The reserved family flag `eotg_government_is_corporate` is **not** used until G2 releases it.

### 5.5 Drafted behaviours adopted as defaults

These are the drafted defaults for the open owner decisions in CATALOG §7.1. They are recorded here, and each changes with one line if the owner rules otherwise.

| # | Decision | Default |
|---|---|---|
| 2 | Neurofractured hardware finish | Keeps its fitted finish. |
| 3 | Augmented with no focus | A wrist servo shows. |
| 5 | The `worn` earpiece, visor and rebreather finishes | Barbershop only. |
| 6 | Actuator leg | Trait route only, no barbershop entry. The engine forces this: the stump morph can't ride a barbershop pick. |
| 7 | Hobgoblin and Chad Orc variants | Moot until races exist. |

## 6. Vanilla precedent

All paths are relative to `game/`.

- **Trait portrait modifier groups:** `gfx/portraits/trait_portrait_modifiers/_trait_modifier.info`. "The first that is valid will be applied"; `base` also applies the base entry's modifiers, which is why the draft uses no `base`; `root may be set as a character so exists check it`, which is why every entry has `exists = root`.
- **Loss traits:** `00_trait_modifiers.txt`:
  - `maimed` (`:852`, morph `gene_maimed_left_arm`);
  - `one_legged` (`:876`, morph `gene_one_legged` `no_left_leg` plus the wooden leg on `special_legwear`; our leg entries reuse the same morph);
  - `blind` / `one_eyed` (`:1963-2013`).
- **Flag-keyed portrait entries:** `temporarily_blind` (`:1985-1990`, `has_character_flag = temporarily_blinded`) and `temporarily_one_eyed` (`:2007-2012`, `has_character_flag = wears_fake_eye_patch`). These are the precedent for keying on flags instead of `has_trait_xp`. Vanilla reads `has_trait_xp` in a portrait context only in `portrait_animations/animations.txt:537-551`, never in modifiers (proposal §7).
- **Adult gate in the barbershop:** `gfx/portraits/portrait_modifiers/01_hairstyles_base.txt:1592-1601` (`is_valid_custom` with `trigger_if = { limit = { exists = root } … }`). The ruler designer has no root and falls to `trigger_else`.
- **`usage = game` weighted groups by government:** `01_cloaks_base.txt:58` (`government_has_flag`), `05_headgear_situational.txt` and `06_makeup.txt` (priority 6; ours use 7).
- **Accessory genes:** `common/genes/08_genes_special_visual_traits.txt:1274-1320`.
- **Asset, mesh and texture formats** (BC3 for all three maps, RRxG normal): ENGINE_NOTES.md (vanilla-scout, 2026-10-26).
- **Deviations:** none from vanilla. The deviations from the MCP proposal are listed in §5.1, §5.3 and §5.4.

## 7. Loc surface

- **New keys: none.** Flags, triggers and portrait modifiers carry no player-facing text.
- **Imported keys:** 259 in 3 files. Checked 2026-11-03:
  - all three files start with `EF BB BF` (BOM) and are in `localization/english/`;
  - no key is duplicated within the files;
  - **0 collide** with any key in the current `localization/` tree, `replace/` included;
  - every key carries `eotg_` (251 inside `PORTRAIT_MODIFIER_eotg_*`, 8 bare gene names).
- **The localizer reviews but does not edit** (the files are regenerated by MCP regen). The review covers:
  - Canadian English;
  - the reflavor glossary (no "barony", "county" or "knight" wording);
  - the label "broad orc ear", flagged in CATALOG §3.9, which ships only once race gates open.
  
  Any fix goes back to the MCP manifests, then regen, then a re-sync.
- **`replace/` overrides needed:** none.

## 8. Lore constraints

From BRIEF.md (lore-keeper rulings 2026-10-26, binding) and the wiring proposal's rulings (a)–(c):
- **Hardware, not magic.** Hand-fitted casings, seals, ports, leads and screws. No brass, clockwork, Void imagery, kill collars, state insignia, datavault sockets, living sheen, or glowing eyes.
- **Clinic work** reads cyan/white; **back-street work** reads amber, with mismatched casings. Heat shows as dull orange-red on fins only. Violet and black are reserved for the Void.
- **The tier ladder:**
  - Augmented: one or two small units;
  - Enhanced: panels, partial frame, cranial port;
  - Overclocked: heat sinks;
  - Neurofractured: dark optic, sedation dressing; strain, never horror;
  - Seamless: shows only the flush optic, limb frame and leg (ruling c).
- **The back-street patch never shows at Seamless** through a game route (ruling a). It is barbershop only.
- **The Cartel Mark never names or depicts a syndicate; the corporate badge names no company.**
- **866 AG:** PMCs, Corporations, Gob-Corps and Cartels exist as governments. Nothing here dates past 866.

**Routed to eotg-lore-keeper** (not blocking SH1–SH3):
- Should a **self** or **physician** fitting draw the back-street finish? The default is no: only `PROVIDER = backstreet` sets the flag.
- Should **kingpins**, who are created Neurofractured (`common/scripted_effects/eotg_aug_kingpin_effects.txt:50`), carry tier or back-street flags by organisation kind? The default is none, so a kingpin shows only the Neurofractured items that need no tier: the sedation dressing (and the patch, only if back-street). This is deferred (§10).

## 9. Definition of done

1. `python docs/tools/sync_cyberware.py verify` exits 0. The manifest lists **2,803** files (2,754 `lfs`, 49 `text`), plus the 2 `generated` wiring files, and the working tree holds no LFS pointer files.
2. `git lfs ls-files | wc -l` = **2,754** (2,585 `.mesh` + 169 `.dds`). `git ls-files gfx/models/portraits/eotg_cyberware | grep -c '\.asset$'` = 21 (plain git). `.git/hooks/pre-push` exists. After the push, GitHub shows "Stored with Git LFS" on a sampled `.mesh`.
3. **Nothing from the denylist is in the tree.** `ls gfx/models/portraits` shows only `eotg_cyberware` and `decals`, and `ls gfx/models/portraits/decals` shows only `eotg_face_mark`. `git ls-files | grep -E 'male_head|female_head|ethnicities'` is empty, and every `chad_orc` hit is an `eotg_` cyberware mesh under `eotg_cyberware/`.
4. **Tiger** (1.17 command in CLAUDE.md, log in the scratchpad) shows **no new finding** in any imported or new file beyond the known-benign list. Record the before and after totals; the MCP baseline had 0 findings from cyberware. **PX LSP** and `px_vocab_check.py common events` are clean on `eotg_portrait_triggers.txt` and the edited effects file. `eotg_lint.py` findings on the engine-forced keys of §3.2 go to an allowlist with a comment citing this spec; no key is renamed.
5. **Grep checks:**
   - `eotg_aug_backstreet_fitted` is set in exactly 1 place (`eotg_aug_procedure_roll_effect`) and cleared in exactly 1 (`eotg_aug_remove_all_effect`);
   - `eotg_aug_tier_enhanced` / `_overclocked` are written only in `eotg_aug_portrait_tier_sync_effect` and `eotg_aug_remove_all_effect`;
   - each `eotg_aug_prosthetic_*` flag is set only at the §5.3 sites (eye 4, leg 2, arm 2).
6. **Every entry in B reads the state.** Each of its 11 groups is keyed on at least one of: the three aug traits, a tier trigger, `var:eotg_aug_focus`, `eotg_aug_backstreet_fitted` or a prosthesis trigger. Every entry in B carries `is_adult = yes`, and every weighted entry in C carries the child `factor = 0`. The generator's checks still hold: 0 entries are missing these.
7. **What must be absent:**
   - `grep -rn 'eotg_aug_last_xp'` over `common events gfx` is empty;
   - `has_trait_xp` does not occur under `gfx/portraits/` or in `eotg_portrait_triggers.txt`;
   - `grep -rnE 'eotg_[ekdcb]_'` stays empty.
8. `sync_cyberware.py copy --check` exits 0 straight after a sync, and B and C carry the draft hash that the manifest records.
9. The **human** confirms the in-game tests in §9.2.

### 9.1 Batches

| Batch | Agent | Contents | Gate to the next |
|---|---|---|---|
| **SH1: import and tool** | orchestrator (LFS setup, `.gitattributes`, CLAUDE.md, agent_workflow §1, cloud prompt) then eotg-scripter (`docs/tools/sync_cyberware.py`, run `copy`, manifest) | §4.1–4.4, §4.6. B and C are generated, but they reference triggers that do not exist yet, so **SH1 and SH3 must land in the same commit** or B and C must stay out of the tree until SH3. Recommended: the SH1 commit holds the binaries, the imported script, the loc and the tool, with `copy --no-wiring` (a flag the tool supports). | `verify` exits 0; Tiger shows no new findings; the human sees 19 barbershop groups (T1). |
| **SH2: flags and setters** | eotg-scripter | §5.1–5.3: `eotg_aug_portrait_tier_sync_effect`, 2 call sites, 1 back-street setter, 8 prosthesis setters, 3 flag clears in `remove_all`. | PX and Tiger clean; DoD 5. |
| **SH3: portrait wiring** | eotg-scripter | §5.4 trigger file; `sync_cyberware.py copy` (with wiring) generates B and C. | DoD 6–8. |
| **SH4: QA** | eotg-qa (read-only), eotg-localizer (loc review §7), then the human | Full DoD 1–8; diff review against this spec; then the in-game walk in §9.2. | Human sign-off. |

### 9.2 In-game tests (human; `docs/qa/HOW_TO_TEST_IN_GAME.md`)

Run `sync_cyberware.py verify` first. Use console `effect = { … }` on the played character, in a full-length view where legs matter.

- **T1 (SH1):**
  - The barbershop shows 19 groups at positions 20–38, every name localized, and no leg group.
  - Only base variants are listed.
  - On a child, no hardware is offered (`is_valid_custom`), and the ruler designer still works.
- **T2, the tier walk (SH3):**
  1. `eotg_aug_initiate_effect = yes`, then set `var:eotg_aug_focus` to `flag:senses`. Expected: an optic on the right eye.
  2. `eotg_aug_set_integration_effect = { XP = 50 }`. Expected: the panel, ring, lattice and spine appear **without reloading**. If they don't, the portrait-refresh question in §10 is live.
  3. `XP = 100`. Expected: heat sinks and the overclocked chest.
  4. `eotg_trigger_neurofracture = yes`. Expected: dark optic, left-temple dressing, heat sinks kept, ring gone.
  5. `eotg_aug_total_integration_effect = yes`. Expected: only the Seamless optic, frame and leg remain.
- **T3, finish:** a back-street install through the back-street interaction. Expected: the patch on the right jaw, khaki casings and amber indicators. Then a clinic upgrade. Expected: the patch stays.
- **T4, prostheses:**
  - Give `one_legged`, then run `eotg_aug_restore_loss_effect = yes`. Expected: the actuator leg plus the stump morph in the full-length view.
  - `add_trait = one_legged` again. Expected: the vanilla wooden leg only, with no double leg.
  - Repeat for `maimed` (frame on the left arm; on re-loss, hardware goes to the right arm) and for `one_eyed` (left optic; on re-loss, the vanilla patch only).
- **T5, wearables:**
  - A PMC courtier gets the visor or issue collar at the expected rate.
  - The court physician gets the medic harness, and the Implant Technician the fitter's harness.
  - Cartel vassals carry the Mark. The brow stud is absent while the optic shows.
  - The rebreather never appears together with the patch.
- **T6, carried QA items:** see §10.
- **T7, exit:** `eotg_aug_remove_all_effect = yes`. Expected: every implant is gone, the prosthesis stays (default), and the tier and back-street flags are cleared (`has_character_flag` in the console).

## 10. Deferred, carried and open

**Owner questions:**
1. **The LFS quota.** Check GitHub Settings → Billing → Git LFS. The set needs about 0.6 GiB of storage per full version, plus every rebuilt item re-synced. Every smudging clone downloads about 0.6 GiB of bandwidth. If the quota is too small, the fallback is a plain commit (§4.1); it is never the gitignore option.
2. **Prosthesis flags on full exit:** kept (the default, §5.3) or cleared?

Owner decisions 7.1-1, -2, -3, -5, -6 and -7 take the defaults in §5.1 and §5.5 unless overruled.

**QA open items carried to the in-game pass (T6):**
- **Cloaks against nape and chest hardware.** Cloaks and fur mantles set no hide tag, so they may cover or clip the spinal housing, the chest housing and the collar (CATALOG §3.12, §3.17; 12–14 of 22–24 cloak outfits cover the chest). Possible fix: a custom hide tag set by the builder in MCP.
- **Legs show only in full-length views.** The actuator leg is invisible in head-and-shoulders portraits. That is accepted; test in the character-sheet full view. The socket and cuff overlap the stump by 17–33 % in bind space (`leg/fit_report.json`): check whether that reads as an intended tuck-in.
- **The adult gate via `is_valid_custom`.** Confirm that it hides barbershop entries on a child and doesn't break the ruler designer. The body meshes have no infant shapes, so a child must never draw hardware.
- **Decal resolution.** The 9 face-mark diffuse maps are 1024² (1.3 MiB each). Cutting them to 512 saves about 10 MiB if the sigil stays legible at portrait size. Judge in game, and change it in MCP (`make_cyber_face_mark.py`), not here.
- **Portrait refresh on a flag change:** unverified (T2 step 2). Vanilla's `temporarily_one_eyed` relies on the same mechanism.
- **Rebreather against the patch.** For now the rebreather is factored to 0 for back-street fitted characters. The cleaner fix is a custom hide tag (proposal §4), which is an MCP builder change.
- **Clipping to watch:** the goblin earpiece and collar, and the rebreather's tusk clearance (CATALOG §2.3). These matter only once races exist.

**Deferred:**
- **Race gates.** The 105 race-specific templates ship inert. Opening them takes:
  - real race triggers (culture, heritage or race trait; portraits can't read DNA) replacing the `always = no` placeholders;
  - an MCP `RACE_GATES` regen and a re-sync.
  
  This is blocked on the race system (`97c3c8a` proposal). The 152 ear-race blendshape meshes (12.8 MiB) stay inert until the race kits ship.
- **Kingpin finish and tier** (§8, needs-lore).
- **A back-street prosthesis keeps its finish after a full exit:** would need a per-prosthesis finish flag. Minor; cut.
- **The family flag `eotg_government_is_corporate`** for the badge, collar and visor. Waits on G2 releasing it.
- **Faith tokens:** deferred until the faiths exist (BRIEF.md).

---

### HANDOFF
- status: done
- next: eotg-scripter (after the orchestrator does SH1 setup steps 1–4 of §4.1 and the CLAUDE.md / agent_workflow edits of §4.5–4.6)
- ask: Build SH1 (write `docs/tools/sync_cyberware.py` and run `copy --no-wiring`), then SH2 (§5.1–5.3 flags and setters), then SH3 (§5.4 trigger file plus `copy` with wiring) from `docs/specs/cyberware_portraits_ship.md`.
- files: docs/specs/cyberware_portraits_ship.md
- needs-loc: none new; eotg-localizer reviews the 3 imported `.yml` files read-only (§7)
- needs-lore: whether self or physician fittings draw the back-street finish; whether kingpins carry tier or back-street flags by organisation kind (§8)
- needs-human: approve git LFS and confirm the GitHub LFS quota; decide whether prosthesis flags are kept or cleared on full exit; then run the in-game walk T1–T7 (§9.2)
