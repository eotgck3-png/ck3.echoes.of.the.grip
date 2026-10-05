# TEST MAP: not mod content.
"""Install the EotG Test Map sub-mod into the CK3 mod folder.

    python docs/test_map/install.py --out "C:/Users/<you>/Documents/Paradox Interactive/Crusader Kings III/mod/eotg_test_map"

What it does:
  1. Copies the sub-mod (this folder, minus the tooling and docs) into --out, replacing any earlier install.
  2. Puts the terrain textures in <out>/gfx/map/terrain:
       - copies docs/test_map/gfx/map/terrain/* if they exist and are not older than their inputs;
       - otherwise runs docs/test_map/build_terrain.py --out <out>/gfx/map/terrain (if the script exists);
       - otherwise warns: the map loads, but with the main mod's / vanilla terrain textures.
  3. Writes the launcher file <out>.mod (next to the folder) with path= set to --out.

It refuses to write inside the repository. Stdlib only.
"""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
TERRAIN_REL = Path("gfx/map/terrain")

# Files and folders in docs/test_map that are tooling or docs, not sub-mod content.
SKIP_TOP = {"install.py", "build_terrain.py", "README.md", "MAPEDITOR_STEPS.md", "eotg_test_map.mod", "__pycache__"}
# Inputs the terrain textures are generated from; a texture older than any of these is stale.
TERRAIN_INPUTS = [HERE / "build_terrain.py", HERE / "map_data/provinces.png", HERE / "map_data/heightmap.png",
                  HERE / "common/province_terrain/00_province_terrain.txt"]

NAME = "EotG Test Map"


def is_inside(child: Path, parent: Path) -> bool:
    try:
        child.relative_to(parent)
        return True
    except ValueError:
        return False


def copy_submod(out: Path) -> None:
    if out.exists():
        desc = out / "descriptor.mod"
        if not desc.is_file() or f'name="{NAME}"' not in desc.read_text(encoding="utf-8", errors="replace"):
            sys.exit(f"refusing to replace {out}: it exists and is not an earlier {NAME} install")
        shutil.rmtree(out)
    out.mkdir(parents=True)
    for item in HERE.iterdir():
        if item.name in SKIP_TOP:
            continue
        dest = out / item.name
        if item.is_dir():
            # terrain textures are handled separately (generated, gitignored)
            ignore = None
            if item.name == "gfx":
                def ignore(d, names):
                    return [n for n in names if Path(d).resolve() == (HERE / "gfx/map").resolve() and n == "terrain"]
            shutil.copytree(item, dest, ignore=ignore)
        else:
            shutil.copy2(item, dest)


def terrain_files(folder: Path):
    if not folder.is_dir():
        return []
    return [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in (".tga", ".dds", ".png")]


def place_terrain(out: Path) -> str:
    local = HERE / TERRAIN_REL
    dest = out / TERRAIN_REL
    files = terrain_files(local)
    newest_input = max((p.stat().st_mtime for p in TERRAIN_INPUTS if p.exists()), default=0)
    fresh = bool(files) and min(p.stat().st_mtime for p in files) >= newest_input
    if fresh:
        dest.mkdir(parents=True, exist_ok=True)
        for p in files:
            shutil.copy2(p, dest / p.name)
        return f"copied {len(files)} terrain texture(s) from {local}"
    builder = HERE / "build_terrain.py"
    if builder.is_file():
        dest.mkdir(parents=True, exist_ok=True)
        why = "stale" if files else "missing"
        print(f"terrain textures {why}; running build_terrain.py (this can take a while)...")
        subprocess.run([sys.executable, str(builder), "--out", str(dest)], check=True)
        return f"built terrain textures into {dest} ({why} locally)"
    return ("WARNING: no terrain textures installed (none in docs/test_map/gfx/map/terrain and no build_terrain.py). "
            "The map loads, but with inherited terrain textures.")


def write_launcher(out: Path) -> Path:
    launcher = out.parent / f"{out.name}.mod"
    text = (out / "descriptor.mod").read_text(encoding="utf-8")
    lines = [ln for ln in text.splitlines() if not ln.startswith("path=")]
    lines.append(f'path="{out.as_posix()}"')
    launcher.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return launcher


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="destination folder, e.g. <CK3 user dir>/mod/eotg_test_map")
    args = ap.parse_args()
    out = Path(os.path.abspath(args.out))
    for target in (out, out.parent / f"{out.name}.mod"):
        if is_inside(target.resolve(), REPO) or is_inside(target, REPO):
            sys.exit(f"refusing to write inside the repository: {target}")
    if out.parent.name.lower() != "mod":
        print(f"note: {out.parent} is not a folder named 'mod'; the launcher only scans <CK3 user dir>/mod")
    copy_submod(out)
    print(f"copied sub-mod to {out}")
    print(place_terrain(out))
    print(f"wrote launcher {write_launcher(out)}")
    print('Playset order: "Echoes of the Grip", then "EotG Test Map".')


if __name__ == "__main__":
    main()
