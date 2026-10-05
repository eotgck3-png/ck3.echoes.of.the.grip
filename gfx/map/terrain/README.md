# Terrain

> **Status corrected 2026-10-04.** This file opened by saying the terrain work was "paused, on hold
> and not shipped" and that the folder held only `flat_maps/flatmap.dds`. That has been untrue
> since the terrain pass resumed in late September: `materials.settings`, `detail_index.tga`,
> `detail_intensity.tga`, `colormap.dds`, the nine `eotg_structure_*.dds` bakes, the masks and the
> `pdxterrain.shader` override are all present and shipping. The history below is kept because the
> round-1 diagnosis is still the reason the textures look the way they do.

## Rebuilding the shipped art — READ THIS FIRST

The two generators below rewrite their outputs **unconditionally**, and the arguments that produced
the shipped files are **not the defaults**. Running either with defaults silently replaces the
map's look with something different. These are the exact commands, verified byte-identical against
the tracked files on 2026-10-04 (9/9 structure bakes, and the colormap):

```
python docs/tools/build_terrain_hybrid.py <root> --source "C:/Users/river/Downloads/spectralbaron_seamless_repeating_futuristic_smoked_carbon-glass_138c75b4-2b72-472a-b618-4aa25d6ec2a8.png"
python docs/tools/build_colormap.py       <root> --level 132
```

The `--source` image lives in `Downloads`, outside the repo, alongside the six other candidates
evaluated on 10-01/10-02. **It is the single point of failure for the structure bakes** — if it is
ever deleted they become genuinely irreproducible, which is why the bakes and the colormap are
tracked via `.gitignore` exceptions. See `docs/pitfalls.md` section 13.

`docs/test_map/build_terrain.py` is the safe pattern for pointing a generator anywhere near this
folder: it refuses an `--out` inside the main mod's `gfx/` and checksums these ten files before and
after.

## Why round 1 was paused
Round 1 of generated textures failed a structural constraint: terrain is minified ~5-9 source
pixels per screen pixel, so pinpoint stars baked into a texture sparkle and crawl. Measured local
contrast 1.20 and peak/mean 13.1 against vanilla terrain's 0.06 and 0.3. See
`docs/terrain_texture_brief.md` for the full diagnosis and the spec for round 2.

## What was preserved from round 1
- **Tools** — `build_terrain_index.py` and `build_colormap.py` are still the live path (with
  `build_terrain_hybrid.py`). `build_terrain_materials.py` and `import_terrain_textures.py` are
  round-1 and must not be invoked directly — see above. The importer's `--check` is still the
  written-down form of the structural limits, which is why it is kept.
- **Docs** — `docs/terrain_scheme.md` (canonical names), `docs/terrain_texture_brief.md` (the round-2
  spec), `docs/terrain_materials.md` (how CK3 layers terrain), `docs/asset_manifest.md`.
- **The removed files themselves** — moved, not deleted, to
  `Documents/Paradox Interactive/Crusader Kings III/mod/_eotg_terrain_backup_20260925/` (445 MB).

## Rebuilding everything, in order

    python docs/tools/build_terrain_hybrid.py <root> --source <image>   # see READ THIS FIRST above
    python docs/tools/build_terrain_index.py  <root>                    # detail_index + detail_intensity
    python docs/tools/build_colormap.py       <root> --level 132

### Do not run `build_terrain_materials.py` directly

It is **superseded**, along with `import_terrain_textures.py`, by `build_terrain_hybrid.py`, and
running it against the shipped folder causes a failure that is worse than a crash because it
renders a wrong map in silence.

`build_terrain_hybrid.py` writes `materials.settings` **and** `gfx/FX/eotg_terrain_params.fxh` in
the *same run*, deliberately. Material ids are **positional** in `materials.settings`, and the
`.fxh` is a lookup table keyed off that exact ordering — its own generated header says "both files
are written by the same run, so they cannot drift apart". `build_terrain_materials.py` writes
`materials.settings` and never touches the `.fxh`.

So running it alone rewrites the ordering while the lookup table keeps the old one, and every
terrain then reads some *other* terrain's tint, star density and effect. Nothing errors. The map
just renders wrong, and because the `.fxh` is gitignored, `git status` reports nothing either.

**Keep the file, though — it is not dead code.** Five other tools import helpers from it
(`save_dds_dxt5`, `save_dds_uncompressed`, `fbm`, `norm01`, `write_material`, `TERRAINS`,
`EDGES`), including `build_colormap.py`, `build_marker_assets.py` and `build_terrain_hybrid.py`
itself. It is a library now, not an entry point.
