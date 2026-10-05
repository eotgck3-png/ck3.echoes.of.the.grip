# Repacking the test map's heightmap — steps for the human

The test map ships `map_data/heightmap.png` but **not** the three files CK3 actually loads from it.
`default.map` says `topology = "heightmap.heightmap"`, and that file does not exist yet. Only a
running game can produce it, so this is the one part of the test map nobody can do offline.

**Nothing in `docs/tools` can do this.** It was checked: no tool in this repo packs a heightmap.

Steps marked **VERIFY** are ones that could not be confirmed from the game files — CK3's map-editor
UI is compiled into the executable, not in `localization/` or `gui/`, so the menu paths below are
from general Paradox practice and need checking against what is actually on screen. Everything not
marked VERIFY was confirmed against vanilla's own files.

---

## What is actually missing, and why

`heightmap.heightmap` is **not** image data. It is a ~293-byte text descriptor. Vanilla's reads:

```
heightmap_file="map_data/packed_heightmap.png"
indirection_file="map_data/indirection_heightmap.png"
original_heightmap_size={ 18432 9216 }
tile_size=65
should_wrap_x=no
level_offsets={ { 0 0 } { 0 1397 } { 0 3129 } { 0 3690 } { 0 3861 } }
max_compress_level=4
empty_tile_offset={ 225 39 }
```

The real artifacts are the two files it points at:

| file | vanilla | what it is |
|---|---|---|
| `packed_heightmap.png` | 3185×4061, 16-bit | an atlas of deduplicated height tiles, at 5 compression levels |
| `indirection_heightmap.png` | 288×144, RGBA | one pixel per tile, saying where that tile sits in the atlas |

`level_offsets` and `empty_tile_offset` are **outputs** of the packing — they record where each
level landed inside the atlas. That is why the descriptor cannot be hand-written: the numbers are
only known once the packing has happened, and whatever does the packing writes the descriptor too.

The tiling maths does work for this map. Stride is `tile_size - 1` = 64, and 8192 / 64 = 128,
4096 / 64 = 64, both whole numbers, so the indirection image would be 128×64.

---

## Before you start

1. The test map must be **installed as a sub-mod** — the cartographer's `install.py` does this.
   The editor edits the installed copy, not this repo folder.
2. Enable both in one playset: **Echoes of the Grip** + **EotG Test Map**. The test map must load
   *after* the main mod so its `map_data` wins.
3. **Back up `docs/test_map/map_data/heightmap.png` first.** The editor can rewrite the source
   heightmap, not just the packed files, and this one came from CK3Gen and is not regenerable here.

> ⚠️ **The main mod folder is a directory junction to this repo.** Anything the editor writes into
> `mod/eotg_stellar_rivers` lands directly in your working tree. Check `git status` after the
> session and revert anything you did not intend — in particular `gfx/map/terrain/colormap.dds` and
> the nine `eotg_structure_*.dds` files, which are tracked and **irreproducible** (see
> `docs/pitfalls.md` §13).

## 1. Launch with the map editor

Add the launch option `-mapeditor`. Either:

- Steam → CK3 → Properties → General → Launch Options: `-mapeditor`, then launch normally; **or**
- run the executable directly: `ck3.exe -mapeditor`

**VERIFY:** whether the Paradox launcher passes the flag through, or whether it has to go on the
exe directly. If the game boots to the normal main menu, the flag did not take.

**VERIFY:** whether the editor needs the playset selected in the launcher first, or offers its own
mod picker on load.

## 2. Repack the heightmap

**VERIFY — this whole step.** The expected shape of it is a heightmap or terrain panel with an
explicit repack/pack action, something like *Map* → *Heightmap* → **Repack heightmap**. Look for
wording containing "repack" or "pack". Some versions do the repack automatically when the map is
saved after a heightmap change.

If no repack action can be found, the fallback is to make a trivial edit to the heightmap in the
editor and save, which forces a repack.

## 3. Let it write `positions.txt` too

`positions.txt` is also missing and is also an editor output — it holds the per-province positions
for name text, unit stacks, buildings and sieges. The same session should produce it.

**VERIFY:** whether this is automatic on save or a separate action (often *Map* → *Generate
positions*, or similar).

## 4. Find what it wrote and copy it back

The editor writes into the **installed** mod folder, not this repo.

**VERIFY** the exact output location. Expected:
`Documents/Paradox Interactive/Crusader Kings III/mod/<test map folder>/map_data/`

Copy these four back into `docs/test_map/map_data/`:

```
heightmap.heightmap
packed_heightmap.png
indirection_heightmap.png
positions.txt
```

Then sanity-check the descriptor before committing — `original_heightmap_size` should read
`{ 8192 4096 }`, and `tile_size` should be `65`. If `original_heightmap_size` says anything else,
the editor repacked a different heightmap than the one intended.

---

## Watch-for list

- **`nodes.dat`** — vanilla ships one and the test map has none. It is not known whether CK3
  regenerates it, requires it, or ignores it for a mod map. If the map fails to load and the
  heightmap is demonstrably fine, this is the next thing to suspect. **VERIFY.**
- **Heightmap aspect ratio.** Vanilla's heightmap is exactly **2×** its `provinces.png` in both
  dimensions (18432×9216 over 9216×4608). This map's is **1:1** (8192×4096 over 8192×4096). The
  tiling still divides cleanly, so this may be fine — but it is the only structural difference from
  the one known-good example, so suspect it first if the editor rejects or mangles the heightmap.
- **Province ids.** `definition.csv` holds ids 1–102: land 1–89, `sea_zones` 90–101,
  `impassable_seas` 102. That matches `default.map` and is internally consistent — no action, but
  if the editor renumbers anything, this is what it should still look like afterwards.
- **16-bit is correct.** `heightmap.png` is `I;16`, and so is vanilla's. Do not let anything
  convert it to 8-bit.

## After the repack

The terrain textures for this map (`detail_index.tga`, `detail_intensity.tga`, `colormap.dds` at
8192×4096 / 4096×2048) are already generated under `docs/test_map/gfx/map/terrain/`. They were
built against this map's own `provinces.png`, so the first load should show terrain rather than a
black or garbled map. If terrain is wrong *after* a successful heightmap repack, that is a separate
problem from this document — start at `docs/pitfalls.md`.
