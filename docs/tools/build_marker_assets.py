"""Build the galactic province markers: one mesh and one colour per HOLDING TYPE.

The marker is a holo-projector plinth with a glowing emblem floating above it. Each holding type
has its own mesh (build_marker_mesh.py): the shared plinth, that type's emblem, and a beam
fitted to it. This script writes the .asset that textures them, and the building overrides that
make every holding draw its own.

The plinth is dark brushed metal with glowing trim lines in the holding's colour. The metal is
authored in PhotoCraft (docs/art/marker_plinth/eotg_plinth_metal.png, made by
docs/tools/build_plinth_material.py). The trims are composited here, because they must sit
exactly on the plinth's ledges, and those UV rows come from make_marker_obj.py's profile.

Colour says what KIND of holding this is - castle, city, temple, tribal, nomad - not who owns
it. So there is no `governments` filter: each holding's primary building simply names the mesh
for its own type. That also means the colour survives conquest, and survives a holding upgrade,
because every level of every primary building points at the same entry.

Holding graphics come from more places than is obvious, and all of them have to be covered or
medieval geometry keeps showing up:

  5 files with `assets = { asset = ... }`   castle, city, temple, temple citadel, tribal
  00_nomad_buildings.txt, bare `asset = `   nomad and herder camps
  99_background_graphics_buildings.txt      the WALLS ringing every holding, and - because the
                                            wall meshes carry the ground decal in a decal_plane
                                            sub-mesh - the patch of dirt underneath. Pointing
                                            these at western_walls_00_mesh, vanilla's own empty
                                            "no walls" mesh, removes both.

Special and legendary buildings also carry assets, but they are placed by history and this mod
places none yet. When it does, they will need the same treatment.

Usage:  python docs/tools/build_marker_assets.py <mod root>
"""
from __future__ import annotations

import os
import re
import sys

import numpy as np
from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_terrain_materials import save_dds_dxt5

REL = os.path.join("gfx", "models", "buildings", "eotg_markers")
SIZE = 128
MESH = "eotg_marker_%s.mesh"      # per holding type, from build_marker_mesh.py
SHAPE = "eotg_markerShape"

# snap_to_terrain, not a new name. A NEW Effect declared in a shader file does not register - the
# lookup falls through to a default and the material is never created, so the mesh draws nothing.
# The mod's pdxmesh.shader adds EOTG_MARKER to this existing effect instead.
SHADER = "snap_to_terrain"
# The beam slot alone. Opaque geometry cannot look like light, so this is the one vanilla effect
# that both snaps to terrain and blends - see make_beam_obj.py for the full reasoning.
BEAM_SHADER = "snap_to_terrain_alpha_to_coverage"

# The beam's .obj gives v = 0 at the aperture and v = 1 at the crown, and .obj puts v = 0 at the
# BOTTOM of the image. If the fade ever comes out upside down - dense at the emblem, thin at the
# plinth - this is the single switch to flip; nothing else needs to change.
BEAM_V_FLIP = False
BEAM_WHITEN = 0.30      # how far the beam's hue is pushed toward white. Light IS paler than the
                        # thing it projects, but only up to a point: at 0.55 the cone came out a
                        # pale cream that, over a dark map, read as more stone on top of the
                        # plinth. Keeping most of the holding's hue is what makes it read as a
                        # beam belonging to the emblem above it.
BEAM_FALLOFF = 1.5      # exponent on the fade from aperture to the model
BEAM_FOOT = 0.14        # the ramp IN at the aperture. Without it the beam starts at full alpha on
                        # a hard geometric edge, which from above is a bright ring sitting on the
                        # stone. Both ends of the beam now reach zero, so it has no visible rim
                        # from any angle.
BEAM_SCANLINES = 7      # faint rings up the beam. The hologram tell, and cheap. 22 of them over
                        # a gap this short is finer than the screen can resolve, and unresolved
                        # banding just reads as noise.
BEAM_SCAN_DEPTH = 0.16

# The palette (owner, 2026-10-20): castle red, city blue, temple yellow, tribal green, nomad a
# fifth hue (violet). A variant takes a lighter tint of its parent, so the temple citadel is pale
# yellow. The herder, the nomad's pastoral form, is almost off-white with a faint violet cast
# (owner: "very pale, almost off-white"). City is a true blue rather
# than the old cyan, so it cannot be mistaken for tribal green on a dark map.
HOLDINGS = [
    ("castle",         (226,  70,  62)),
    ("city",           ( 66, 136, 255)),
    ("temple",         (240, 204,  56)),
    ("temple_citadel", (250, 228, 138)),
    ("tribal",         ( 85, 185, 107)),
    ("nomad",          (167, 124, 255)),
    ("herder",         (238, 232, 246)),
]

# The construction cage (see SCAFFOLD below): amber, because no holding type uses it. Its
# alpha is the texture's share of the beam effect's opacity, and that effect multiplies it by
# a view fade and a 0.45 gain, so 1.0 here still draws see-through.
CONSTRUCTION_RGB = (255, 162, 48)

# Sites (build_marker_mesh.py SITES): one cool cyan for the gatherings and the camp, magenta for
# the hazards. Neither is a holding colour.
GATHERING_RGB = (110, 225, 240)
HAZARD_RGB = (236, 72, 196)
SITES = [("feast", GATHERING_RGB), ("hunt", GATHERING_RGB), ("tournament", GATHERING_RGB),
         ("wedding", GATHERING_RGB), ("camp", GATHERING_RGB), ("quarantine", HAZARD_RGB),
         ("decon", HAZARD_RGB), ("purge", HAZARD_RGB)]

# Vanilla entity files replaced by path; each defines one pdxmesh and one entity, and nothing
# else, so a same-path file with just the entity is a clean swap (scouted 2026-10-20).
#   activities: map_entity in common/activities/activity_types/*.txt; feast also serves funeral,
#               gruesome festival, tour and witch ritual
#   epidemics:  started by epidemic_model_* in gfx/models/_city_entities.asset
ACTIVITY_OVERRIDES = [
    ("gfx/models/buildings/events/%ss/building_%s_%s_01.asset" % (act, cul, act),
     "building_%s_%s_01_entity" % (cul, act), "eotg_site_%s_mesh" % act, "")
    for act in ("feast", "hunt", "tournament", "wedding")
    for cul in ("western", "mena", "indian")]
EPIDEMIC_OVERRIDES = [
    ("gfx/models/buildings/events/disease/fp4_burial_mass_01_a.asset",
     "fp4_burial_mass_01_a_entity", "eotg_site_quarantine_mesh", ""),
    ("gfx/models/buildings/events/disease/fp4_healers_camp_01_a.asset",
     "fp4_healers_camp_01_a_entity", "eotg_site_decon_mesh", ""),
    # the pyre keeps vanilla's fire: the attached `pyre` entity runs particle city/pyre_01
    ("gfx/models/buildings/events/disease/fp4_pyre_01_a.asset",
     "fp4_pyre_01_a_entity", "eotg_site_purge_mesh",
     '\tlocator = { name = "pyre_01" position = { 0 .3 0 } }\n'
     '\tattach = { "pyre_01" = "pyre" }\n'),
]

# The adventurer camp borrowed the HUNT entity (00_domicile_types.txt camp map_entity), so the
# camp and the hunt looked the same. It gets its own entity, and the domicile file is copied
# with only the camp's map_entity blocks replaced; nothing in a domicile type merges by field.
CAMP_ENTITY = "eotg_adventurer_camp_entity"
DOMICILE_TYPES = os.path.join("common", "domiciles", "types", "00_domicile_types.txt")

# The holy-site landmark: vanilla's two cathedral meshes, replaced by path. Their mesh NAMES
# stay, because holy_site_pagan_grand_temple_01 / holy_site_other_grand_temple_01 (the only
# fallbacks a mod religion can get) and the mod's stripped special.txt map objects name them.
MONOLITH_OVERRIDES = [
    ("gfx/models/buildings/special/building_special_cathedral_pagan.asset",
     "building_special_cathedral_pagan_mesh", "building_special_cathedral_pagan_entity"),
    ("gfx/models/buildings/special/building_special_cathedral_generic.asset",
     "building_special_cathedral_generic_mesh", "building_special_cathedral_generic_entity"),
]
MONOLITH_BODY_RGB = (72, 78, 94)   # dark, but a step above the map so its outline holds
MONOLITH_GLOW_RGB = (150, 240, 220)

# Siege projectiles. The boulder is skinned to a two-bone skeleton that its flight animation
# drives, and obj_to_pdxmesh writes no skins, so the MESH stays; the three western engines'
# boulder and the cannonball become plasma balls by texture alone. The file is copied whole, because the cannon
# and ballista projectiles live in it too.
PROJECTILES = os.path.join("gfx", "models", "effects", "_siege_weapons_projectiles.asset")
PLASMA_RGB = (215, 248, 255)
CONSTRUCTION_ALPHA = 1.0

# Which holding type each primary building belongs to. Longest prefix wins, so temple_citadel_
# must be tested before temple_.
BUILDING_HOLDING = [
    ("temple_citadel_", "temple_citadel"),
    ("castle_",         "castle"),
    ("city_",           "city"),
    ("temple_",         "temple"),
    ("tribe_",          "tribal"),
    ("nomadic_camp_",   "nomad"),
    ("herder_camp_",    "herder"),
]

HOLDING_FILES = ("00_castle_buildings.txt", "00_city_buildings.txt", "00_temple_buildings.txt",
                 "temple_citadel_buildings.txt", "00_tribal_buildings.txt",
                 "00_nomad_buildings.txt")
WALLS_FILE = "99_background_graphics_buildings.txt"
EMPTY_WALL_MESH = "western_walls_00_mesh"

GAME = r"D:\SteamLibrary\steamapps\common\Crusader Kings III\game"

# Vanilla's scaffold, replaced by path. Same entity name, locator and states as vanilla
# (gfx/models/mapitems/scaffolding/scaffolding_a.asset). The engine draws it AT THE HOLDING'S
# LOCATOR, around the holding model (vanilla's is a 4.7 x 6.3 x 5.0 cage centred on the
# origin), so the mesh is a translucent wireframe cage that encloses the marker.
SCAFFOLD = os.path.join("gfx", "models", "mapitems", "scaffolding", "scaffolding_a.asset")
SCAFFOLD_ASSET = """\ufeff# MOD(eotg) GENERATED by docs/tools/build_marker_assets.py - do not hand-edit.
# Replaces vanilla's wooden scaffold with a translucent amber wireframe cage, drawn around
# the holding's own marker while something is under construction. The entity, its locator and
# its states match vanilla; only the mesh changes.

entity = {
	name = "construction"
	pdxmesh = "eotg_construction_mesh"

	locator = { name = part1 }

	default_state = "idle"
	state = { name = "idle" state_time = 5 looping = no
		event = { time = 0 node = "part1" particle = "city/construction_dust_looping" trigger_once = yes sound = { soundeffect = "event:/SFX/VFX/vfx_construction_ongoing" } }
	}

	state = { name = "complete" state_time = 5 looping = no
		event = { time = 0 node = "part1" particle = "city/construction_dust_end" trigger_once = yes}
	}
}
"""


def find_block(text, start):
    """Index just past the matching close brace for the block opening at `start`."""
    depth = 0
    i = start
    while i < len(text):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return i + 1
        i += 1
    raise ValueError("unbalanced braces")


def holding_of(key):
    for prefix, holding in BUILDING_HOLDING:
        if key.startswith(prefix):
            return holding
    return None


def strip_assets(block):
    """Remove every asset declaration from a building block, in either spelling.

    Returns (block_without_assets, illustration, soundeffect). The illustration and sound are
    carried out because they are per-asset in vanilla, and dropping them silently costs the
    holding its picture in the UI and its ambient audio - a regression that is invisible on the
    map and only shows up when you click the holding.
    """
    illustration = soundeffect = None
    fallback_illu = fallback_snd = None
    while True:
        # Any indent, not just one tab. Vanilla temple_03 closes its `assets = { }` early, which
        # leaves four dharmic-temple `asset` entries at the building's top level indented by two
        # tabs. A one-tab pattern skipped them, and dharmic provinces kept vanilla temples.
        m = re.search(r"\n\t+(assets|asset)\s*=\s*\{", block)
        if not m:
            break
        end = find_block(block, block.index("{", m.end() - 1))
        chunk = block[m.start():end]

        # Prefer a base-game asset. Vanilla lists DLC variants first, so taking the first match
        # gives castles a Norse illustration and Norse ambience for every culture. An asset with
        # no requires_dlc_flag is the one everyone sees.
        for am in re.finditer(r"\n\t+asset\s*=\s*\{", chunk):
            aend = find_block(chunk, chunk.index("{", am.end() - 1))
            entry = chunk[am.start():aend]
            dlc = "requires_dlc_flag" in entry
            im = re.search(r"illustration\s*=\s*(\S+)", entry)
            sm = re.search(r"soundeffect\s*=\s*\{", entry)
            snd = None
            if sm:
                send = find_block(entry, entry.index("{", sm.end() - 1))
                snd = entry[sm.start():send]
            if im and fallback_illu is None:
                fallback_illu = im.group(1)
            if snd and fallback_snd is None:
                fallback_snd = snd
            if not dlc:
                if im and illustration is None:
                    illustration = im.group(1)
                if snd and soundeffect is None:
                    soundeffect = snd
        block = block[:m.start()] + block[end:]
    return block, illustration or fallback_illu, soundeffect or fallback_snd


def asset_block(mesh_name, illustration, soundeffect):
    out = ["\n\tassets = {", "\t\tasset = {", "\t\t\ttype = pdxmesh",
           '\t\t\tname = "%s"' % mesh_name]
    if illustration:
        out.append("\t\t\tillustration = %s" % illustration)
    if soundeffect:
        out.append("\t\t\t" + soundeffect)
    out += ["\t\t}", "\t}"]
    return "\n".join(out)


def override_file(src, outdir, pick_mesh, header_note):
    """Copy every building that declares an asset, with our asset swapped in.

    Buildings merge by key, so emitting only the ones that define a model leaves every other
    vanilla building untouched. Everything else in the block is copied verbatim, including
    is_enabled, so gameplay and the wall-selection logic are unchanged - only what is drawn
    changes.
    """
    txt = open(src, encoding="utf-8-sig").read()

    # `@name = value` reader variables are FILE-scoped, so a copied building referring to
    # @holding_illustration_india resolves to nothing unless the definition travels with it.
    defs = re.findall(r"^@[A-Za-z_][A-Za-z0-9_]*\s*=\s*[^\n]+$", txt, re.M)

    kept, names = [], []
    for m in re.finditer(r"^([a-z0-9_]+)\s*=\s*\{", txt, re.M):
        key = m.group(1)
        end = find_block(txt, txt.index("{", m.start()))
        block = txt[m.start():end]
        if not re.search(r"\n\t(assets|asset)\s*=\s*\{", block):
            continue
        mesh_name = pick_mesh(key)
        if mesh_name is None:
            continue
        stripped, illu, snd = strip_assets(block)
        close = stripped.rindex("}")
        newblock = stripped[:close].rstrip() + "\n" + asset_block(mesh_name, illu, snd) + "\n}"
        kept.append(newblock)
        names.append(key)

    if not kept:
        return []
    out = os.path.join(outdir, "eotg_" + os.path.basename(src))
    header = ("\ufeff# MOD(eotg) GENERATED by docs/tools/build_marker_assets.py - do not "
              "hand-edit.\n# " + header_note + "\n# Vanilla definitions are copied verbatim with "
              "ONLY the asset declarations replaced,\n# so gameplay is untouched. Buildings merge "
              "by key, so every other building in the\n# vanilla file is left alone.\n\n")
    if defs:
        header += "\n".join(defs) + "\n\n"
    open(out, "w", encoding="utf-8", newline="\n").write(header + "\n\n".join(kept) + "\n")
    return names


def flat(rgb):
    a = np.zeros((SIZE, SIZE, 4), np.uint8)
    a[..., 0], a[..., 1], a[..., 2] = rgb
    a[..., 3] = 255
    return Image.fromarray(a, "RGBA")


def beam_texture(rgb):
    """A vertical alpha ramp in the holding's hue, for the projector beam.

    Everything that varies ALONG the beam lives here rather than in the shader, because it is the
    same for every camera angle and a texture is the cheaper place to put it. The shader only adds
    what the texture cannot know: the fade across the beam, which depends on where you are
    standing.
    """
    v = np.linspace(0.0, 1.0, SIZE)          # 0 = aperture, 1 = crown
    if not BEAM_V_FLIP:
        v = v[::-1]                          # .obj v = 0 is the BOTTOM row of the image
    # Zero at the aperture, peak just above it, zero again at the model. The top end matters most:
    # the beam now ENDS at the emblem's base, so alpha reaching 0 there means the light simply
    # runs out rather than being clipped by the end of the geometry.
    foot = np.clip(v / BEAM_FOOT, 0.0, 1.0)
    foot = foot * foot * (3.0 - 2.0 * foot)          # smoothstep, so the ramp has no corner
    a = foot * (1.0 - v) ** BEAM_FALLOFF
    # Rings, not a smooth wash. A perfectly even cone reads as glass; banding reads as projection.
    a *= 1.0 - BEAM_SCAN_DEPTH * (0.5 + 0.5 * np.cos(v * BEAM_SCANLINES * 2.0 * np.pi))

    col = np.array(rgb, np.float64)
    col = col + (255.0 - col) * BEAM_WHITEN

    img = np.zeros((SIZE, SIZE, 4), np.uint8)
    img[..., :3] = np.clip(col, 0, 255).astype(np.uint8)
    img[..., 3] = np.clip(a * 255.0, 0, 255).astype(np.uint8)[:, None]
    return Image.fromarray(img, "RGBA")


# ---------------------------------------------------------------- the plinth

PLINTH_SIZE = 512
PLINTH_METAL = os.path.join("docs", "art", "marker_plinth", "eotg_plinth_metal.png")
TRIM_WHITEN = 0.18               # trims a touch paler than the emblem: light, not paint
TRIM_PX = 5                      # band width in texels at 512; under 4 aliases out at mid zoom
BEAM_R0_OF_PEDESTAL = 0.55       # build_marker_mesh.py: the aperture is this share of the top

# Where each trim sits, as indices into make_marker_obj.py's profile points. All four sit where
# the profile already has an edge, so they read as built in:
#   foot      a band round the base wall (points a -> b), a ground light that outlines it
#   rim       the outermost point of the top, which outlines the top
#   top       the top face (points a -> b, radius falling to 0); the aperture ring sits on it at
#             the beam's base radius: the projector's lens
#   conduits  vertical lines up the neck (points a -> b); the holding plinth only
TRIMS = {
    "chess": dict(foot=(1, 2), rim=9, top=(10, 11), conduits=(5, 8)),    # holding plinth
    "disc": dict(foot=(1, 2), rim=4, top=(4, 5), conduits=None),         # site puck
}


def profile_v(profile):
    """The V coordinate of each profile point, exactly as make_marker_obj.py assigns it
    (arc length along the profile, normalised)."""
    from make_marker_obj import PROFILES
    prof = PROFILES[profile]
    lengths = [0.0]
    for a, b in zip(prof, prof[1:]):
        lengths.append(lengths[-1] + float(np.hypot(b[0] - a[0], b[1] - a[1])))
    return prof, [x / lengths[-1] for x in lengths]


def plinth_trim_mask(profile="chess"):
    """1 on the trim lines, 0 elsewhere, in the plinth's UV space (see TRIMS).
    .obj puts v = 0 at the BOTTOM of the image, so row = (1 - v) * size."""
    prof, v = profile_v(profile)
    spec = TRIMS[profile]
    n = PLINTH_SIZE
    rows = np.arange(n)[:, None].astype(np.float64)
    cols = np.arange(n)[None, :].astype(np.float64)
    mask = np.zeros((n, n))

    def row_of(vv):
        return (1.0 - vv) * (n - 1)

    def hband(vv, px=TRIM_PX):
        d = np.abs(rows - row_of(vv))
        return np.clip(px / 2.0 + 0.5 - d, 0.0, 1.0) * np.ones((1, n))

    a, b = spec["foot"]
    mask = np.maximum(mask, hband((v[a] + v[b]) / 2, TRIM_PX + 2))
    mask = np.maximum(mask, hband(v[spec["rim"]]))
    # The aperture: the beam's base radius is BEAM_R0_OF_PEDESTAL of the top's outer radius
    aperture = BEAM_R0_OF_PEDESTAL * prof[spec["rim"]][0]
    a, b = spec["top"]
    (r0, _), (r1, _) = prof[a], prof[b]
    t = (r0 - aperture) / (r0 - r1)
    mask = np.maximum(mask, hband(v[a] + t * (v[b] - v[a]), TRIM_PX - 1))
    if spec["conduits"]:
        a, b = spec["conduits"]
        lo, hi = row_of(v[b]), row_of(v[a])
        on_neck = ((rows >= lo) & (rows <= hi)).astype(np.float64)
        for k in range(6):
            u = (k + 0.5) / 6.0
            d = np.abs(cols - u * (n - 1))
            mask = np.maximum(mask, on_neck * np.clip((TRIM_PX - 1) / 2.0 + 0.5 - d, 0.0, 1.0))
    return mask


def plinth_metal(mod_root):
    """The PhotoCraft metal, made seamless around the plinth.

    U wraps once round the lathe, so the image's left and right edges meet on the model. A motion
    blur does not wrap, so the raw texture shows a seam there: about 3.5 times the
    column-to-column difference anywhere else. Cross-fading each edge into the opposite one
    removes it."""
    src = os.path.join(mod_root, PLINTH_METAL)
    if not os.path.exists(src):
        sys.exit("missing %s - run docs/tools/build_plinth_material.py" % src)
    img = Image.open(src).convert("RGB").resize((PLINTH_SIZE, PLINTH_SIZE), Image.LANCZOS)
    a = np.asarray(img, np.float64)
    w = 48
    rolled = np.roll(a, PLINTH_SIZE // 2, axis=1)
    ramp = np.ones(PLINTH_SIZE)
    ramp[:w] = np.linspace(0.0, 1.0, w)
    ramp[-w:] = np.linspace(1.0, 0.0, w)
    return a * ramp[None, :, None] + rolled * (1.0 - ramp[None, :, None])


def plinth_diffuse(metal, trim, rgb):
    col = np.array(rgb, np.float64)
    col = col + (255.0 - col) * TRIM_WHITEN
    out = metal * (1.0 - trim[..., None]) + col[None, None, :] * trim[..., None]
    img = np.zeros((PLINTH_SIZE, PLINTH_SIZE, 4), np.uint8)
    img[..., :3] = np.clip(out, 0, 255).astype(np.uint8)
    img[..., 3] = 255
    return Image.fromarray(img, "RGBA")


def write_entity_override(mod_root, rel, body):
    path = os.path.join(mod_root, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    head = ("\ufeff# MOD(eotg) GENERATED by docs/tools/build_marker_assets.py - do not hand-edit.\n"
            "# Replaces vanilla %s by path: same names, a space-setting mesh.\n\n" % rel)
    open(path, "w", encoding="utf-8", newline="\n").write(head + body)


def write_camp_domicile(mod_root):
    """Copy vanilla's domicile types with only the camp's map_entity blocks swapped for one
    shorthand line naming the camp's own entity."""
    src = os.path.join(GAME, DOMICILE_TYPES)
    raw = open(src, "rb").read()
    bom = raw.startswith(b"\xef\xbb\xbf")
    text = raw.decode("utf-8-sig")
    start = text.index("camp = {")
    end = find_block(text, text.index("{", start))
    camp = text[start:end]
    spans = []
    for m in re.finditer(r"\n\t+map_entity\s*=\s*\{", camp):
        spans.append((m.start(), find_block(camp, camp.index("{", m.end() - 1))))
    if not spans:
        sys.exit("no map_entity in vanilla camp - the domicile file has changed")
    new_camp = (camp[:spans[0][0]]
                + "\n\t# MOD(eotg): the camp has its own marker. Vanilla borrowed the hunt"
                  " activity's entity,\n\t# so a camp and a hunt looked the same.\n"
                  # vanilla's live-owner trigger stays: a dead adventurer's camp shows nothing
                  "\tmap_entity = {\n\t\ttrigger = {\n\t\t\towner ?= { is_alive = yes }\n\t\t}\n"
                  "\t\treference = \"%s\"\n\t}" % CAMP_ENTITY
                + camp[spans[-1][1]:])
    out = text[:start] + new_camp + text[end:]
    head = ("# MOD(eotg) GENERATED by docs/tools/build_marker_assets.py - do not hand-edit.\n"
            "# Vanilla's file with ONLY the camp's map_entity changed. Regenerate after a game\n"
            "# patch rather than editing.\n")
    path = os.path.join(mod_root, DOMICILE_TYPES)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8-sig" if bom else "utf-8", newline="\n").write(head + out)


def write_projectiles(mod_root):
    text = open(os.path.join(GAME, PROJECTILES), encoding="utf-8-sig").read()
    n = text.count('texture_diffuse = "projectile_diffuse.dds"')
    # the three western boulders and the cannonball share it; the ballista bolt has its own
    if n != 4:
        sys.exit("expected the boulder texture 4 times in %s, found %d" % (PROJECTILES, n))
    text = text.replace('texture_diffuse = "projectile_diffuse.dds"',
                        'texture_diffuse = "eotg_projectile_plasma_diffuse.dds"')
    head = ("# MOD(eotg) GENERATED by docs/tools/build_marker_assets.py - do not hand-edit.\n"
            "# Vanilla's file; the boulders and the cannonball take a plasma texture. The meshes and\n"
            "# their flight animations are vanilla (they are skinned; obj_to_pdxmesh writes no\n"
            "# skins).\n")
    path = os.path.join(mod_root, PROJECTILES)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, "w", encoding="utf-8", newline="\n").write(head + text)
    save_dds_dxt5(flat(PLASMA_RGB), os.path.join(os.path.dirname(path),
                                                  "eotg_projectile_plasma_diffuse.dds"))


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    mod_root = sys.argv[1]
    outdir = os.path.join(mod_root, REL)
    os.makedirs(outdir, exist_ok=True)
    missing = [n for n, _ in HOLDINGS if not os.path.exists(os.path.join(outdir, MESH % n))]
    if missing:
        sys.exit("missing %s - run build_marker_mesh.py first"
                 % ", ".join(MESH % n for n in missing))

    # Slot 1 glows because its properties map has r = 1; EOTG_MARKER multiplies its emissive and
    # rim by Properties.r. Slot 0's map has r = 1 only on the trim lines, so the plinth lights as
    # plain metal with glowing trims. That is what lets all slots share one effect - and they
    # must, because the effect carries the terrain snap and a slot without it would sit at sea
    # level.
    glow = np.zeros((SIZE, SIZE, 4), np.uint8)
    glow[..., 0] = 255
    glow[..., 3] = 255
    save_dds_dxt5(Image.fromarray(glow, "RGBA"), os.path.join(outdir, "eotg_marker_glow_properties.dds"))
    trim = plinth_trim_mask()
    props = np.zeros((PLINTH_SIZE, PLINTH_SIZE, 4), np.uint8)
    props[..., 0] = np.clip(trim * 255.0, 0, 255).astype(np.uint8)
    props[..., 3] = 255
    save_dds_dxt5(Image.fromarray(props, "RGBA"),
                  os.path.join(outdir, "eotg_marker_plinth_properties.dds"))
    metal = plinth_metal(mod_root)
    # the stone the plinth used to be; nothing references it any more
    stale = os.path.join(outdir, "eotg_marker_stone_diffuse.dds")
    if os.path.exists(stale):
        os.remove(stale)

    lines = ["\ufeff# MOD(eotg) GENERATED by docs/tools/build_marker_assets.py - do not hand-edit.",
             "# One mesh per HOLDING TYPE, three material slots: 0 the projector plinth (metal,",
             "# trims glowing in the holding's colour), 1 that type's glowing emblem, 2 the beam",
             "# that makes the emblem read as something the plinth casts.",
             "# The silhouette and the colour both say what kind of holding it is.",
             ""]
    for name, rgb in HOLDINGS:
        tex = "eotg_marker_%s_diffuse.dds" % name
        save_dds_dxt5(flat(rgb), os.path.join(outdir, tex))
        plinth_tex = "eotg_marker_%s_plinth_diffuse.dds" % name
        save_dds_dxt5(plinth_diffuse(metal, trim, rgb), os.path.join(outdir, plinth_tex))
        beam_tex = "eotg_marker_%s_beam.dds" % name
        save_dds_dxt5(beam_texture(rgb), os.path.join(outdir, beam_tex))
        lines += [
            "pdxmesh = {",
            '\tname = "eotg_marker_%s_mesh"' % name,
            '\tfile = "%s"' % (MESH % name),
            "",
            "\tmeshsettings = {",
            '\t\tname = "%s"' % SHAPE,
            "\t\tindex = 0",
            '\t\ttexture_diffuse = "%s"' % plinth_tex,
            '\t\ttexture_normal = "nonormal.dds"',
            '\t\ttexture_specular = "eotg_marker_plinth_properties.dds"',
            '\t\tshader = "%s"' % SHADER,
            "\t}",
            "\tmeshsettings = {",
            '\t\tname = "%s"' % SHAPE,
            "\t\tindex = 1",
            '\t\ttexture_diffuse = "%s"' % tex,
            '\t\ttexture_normal = "nonormal.dds"',
            '\t\ttexture_specular = "eotg_marker_glow_properties.dds"',
            '\t\tshader = "%s"' % SHADER,
            "\t}",
            # Slot 2 shares the emblem's properties map, so Properties.r is 1 and the beam counts
            # as a marker surface; what makes it behave differently is the effect, not the mask.
            "\tmeshsettings = {",
            '\t\tname = "%s"' % SHAPE,
            "\t\tindex = 2",
            '\t\ttexture_diffuse = "%s"' % beam_tex,
            '\t\ttexture_normal = "nonormal.dds"',
            '\t\ttexture_specular = "eotg_marker_glow_properties.dds"',
            '\t\tshader = "%s"' % BEAM_SHADER,
            "\t}",
            "}",
            "",
        ]
    # the construction cage: one slot, on the beam's blending effect
    if not os.path.exists(os.path.join(outdir, "eotg_construction.mesh")):
        sys.exit("eotg_construction.mesh is missing - run build_marker_mesh.py first")
    cage = np.zeros((SIZE, SIZE, 4), np.uint8)
    cage[..., :3] = CONSTRUCTION_RGB
    cage[..., 3] = int(round(255 * CONSTRUCTION_ALPHA))
    save_dds_dxt5(Image.fromarray(cage, "RGBA"),
                  os.path.join(outdir, "eotg_construction_diffuse.dds"))
    lines += [
        "# The construction cage, drawn around a holding's marker while something is being",
        "# built (entity `construction`, gfx/models/mapitems/scaffolding/scaffolding_a.asset).",
        "pdxmesh = {",
        '\tname = "eotg_construction_mesh"',
        '\tfile = "eotg_construction.mesh"',
        "",
        "\tmeshsettings = {",
        '\t\tname = "eotg_constructionShape"',
        "\t\tindex = 0",
        '\t\ttexture_diffuse = "eotg_construction_diffuse.dds"',
        '\t\ttexture_normal = "nonormal.dds"',
        '\t\ttexture_specular = "eotg_marker_glow_properties.dds"',
        '\t\tshader = "%s"' % BEAM_SHADER,
        "\t}",
        "}",
        "",
    ]
    # sites: puck + glyph + beam, textured like a holding marker but on the puck's trim mask
    puck_trim = plinth_trim_mask("disc")
    props = np.zeros((PLINTH_SIZE, PLINTH_SIZE, 4), np.uint8)
    props[..., 0] = np.clip(puck_trim * 255.0, 0, 255).astype(np.uint8)
    props[..., 3] = 255
    save_dds_dxt5(Image.fromarray(props, "RGBA"),
                  os.path.join(outdir, "eotg_site_puck_properties.dds"))
    lines += ["# Sites: activity sites, the adventurer camp and epidemic sites, on the low puck.", ""]
    for name, rgb in SITES:
        if not os.path.exists(os.path.join(outdir, "eotg_site_%s.mesh" % name)):
            sys.exit("eotg_site_%s.mesh is missing - run build_marker_mesh.py first" % name)
        puck_tex = "eotg_site_%s_puck_diffuse.dds" % name
        glyph_tex = "eotg_site_%s_diffuse.dds" % name
        beam_tex = "eotg_site_%s_beam.dds" % name
        save_dds_dxt5(plinth_diffuse(metal, puck_trim, rgb), os.path.join(outdir, puck_tex))
        save_dds_dxt5(flat(rgb), os.path.join(outdir, glyph_tex))
        save_dds_dxt5(beam_texture(rgb), os.path.join(outdir, beam_tex))
        lines += ["pdxmesh = {", '\tname = "eotg_site_%s_mesh"' % name,
                  '\tfile = "eotg_site_%s.mesh"' % name, ""]
        for idx, diff, spec, shader in (
                (0, puck_tex, "eotg_site_puck_properties.dds", SHADER),
                (1, glyph_tex, "eotg_marker_glow_properties.dds", SHADER),
                (2, beam_tex, "eotg_marker_glow_properties.dds", BEAM_SHADER)):
            lines += ["\tmeshsettings = {", '\t\tname = "%s"' % SHAPE, "\t\tindex = %d" % idx,
                      '\t\ttexture_diffuse = "%s"' % diff, '\t\ttexture_normal = "nonormal.dds"',
                      '\t\ttexture_specular = "%s"' % spec, '\t\tshader = "%s"' % shader, "\t}"]
        lines += ["}", ""]
    lines += ["# The adventurer camp (common/domiciles/types/00_domicile_types.txt, camp map_entity)",
              "entity = {", '\tname = "%s"' % CAMP_ENTITY, '\tpdxmesh = "eotg_site_camp_mesh"', "}",
              ""]
    path = os.path.join(outdir, "eotg_markers.asset")
    open(path, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
    print("wrote %s" % path)
    for name, rgb in HOLDINGS:
        print("  %-15s rgb%s" % (name, rgb))

    print("\noverriding holding buildings (colour by holding type):")
    bdir = os.path.join(mod_root, "common", "buildings")
    os.makedirs(bdir, exist_ok=True)
    total = 0
    for fn in HOLDING_FILES:
        src = os.path.join(GAME, "common", "buildings", fn)
        if not os.path.exists(src):
            print("  skipped, not in this install: %s" % fn)
            continue
        names = override_file(
            src, bdir,
            lambda k: ("eotg_marker_%s_mesh" % holding_of(k)) if holding_of(k) else None,
            "Every level of every primary building points at the same entry, so the marker "
            "does not change on upgrade.")
        total += len(names)
        print("  %-36s %d  %s" % ("eotg_" + fn, len(names), ", ".join(names)))
    print("  %d primary buildings now draw the marker" % total)

    # The construction site. The engine draws the entity named `construction` while a holding
    # is being built; no script references it. Overriding the vanilla file by path is what
    # guarantees the swap, since a second entity of the same name would only be a duplicate.
    # The vanilla dust particle and construction sound stay; only the mesh changes.
    scaffold = os.path.join(mod_root, SCAFFOLD)
    os.makedirs(os.path.dirname(scaffold), exist_ok=True)
    open(scaffold, "w", encoding="utf-8", newline="\n").write(SCAFFOLD_ASSET)
    print("\nconstruction site: %s -> eotg_construction_mesh" % SCAFFOLD)

    print("\nsites (entity files replaced by path):")
    for rel, entity, mesh, extra in ACTIVITY_OVERRIDES + EPIDEMIC_OVERRIDES:
        if not os.path.exists(os.path.join(GAME, rel)):
            sys.exit("vanilla file moved or gone: %s" % rel)
        write_entity_override(mod_root, rel,
                              "entity = {\n\tname = \"%s\"\n\tpdxmesh = \"%s\"\n%s}\n"
                              % (entity, mesh, extra))
        print("  %-62s %s" % (rel, mesh))

    write_camp_domicile(mod_root)
    print("\nadventurer camp: %s -> %s" % (DOMICILE_TYPES, CAMP_ENTITY))

    print("\nholy-site landmark:")
    sdir = os.path.join(mod_root, "gfx", "models", "buildings", "special")
    if not os.path.exists(os.path.join(sdir, "eotg_precursor_monolith.mesh")):
        sys.exit("eotg_precursor_monolith.mesh is missing - run build_marker_mesh.py first")
    save_dds_dxt5(flat(MONOLITH_BODY_RGB), os.path.join(sdir, "eotg_monolith_body_diffuse.dds"))
    save_dds_dxt5(flat(MONOLITH_GLOW_RGB), os.path.join(sdir, "eotg_monolith_glow_diffuse.dds"))
    for rel, mesh, entity in MONOLITH_OVERRIDES:
        if not os.path.exists(os.path.join(GAME, rel)):
            sys.exit("vanilla file moved or gone: %s" % rel)
        body = ("pdxmesh = {\n\tname = \"%s\"\n\tfile = \"eotg_precursor_monolith.mesh\"\n\n"
                % mesh)
        for idx, diff, spec in ((0, "eotg_monolith_body_diffuse.dds", "noproperties.dds"),
                                (1, "eotg_monolith_glow_diffuse.dds",
                                 "eotg_marker_glow_properties.dds")):
            body += ("\tmeshsettings = {\n\t\tname = \"eotg_precursor_monolithShape\"\n"
                     "\t\tindex = %d\n\t\ttexture_diffuse = \"%s\"\n"
                     "\t\ttexture_normal = \"nonormal.dds\"\n\t\ttexture_specular = \"%s\"\n"
                     "\t\tshader = \"%s\"\n\t}\n" % (idx, diff, spec, SHADER))
        body += "}\n\nentity = {\n\tname = \"%s\"\n\tpdxmesh = \"%s\"\n}\n" % (entity, mesh)
        write_entity_override(mod_root, rel, body)
        print("  %-62s eotg_precursor_monolith.mesh" % rel)

    print("\nsiege projectiles:")
    write_projectiles(mod_root)
    print("  %s: boulders and cannonball textured as plasma" % PROJECTILES)

    print("\nremoving the walls and the dirt patch under them:")
    src = os.path.join(GAME, "common", "buildings", WALLS_FILE)
    if os.path.exists(src):
        names = override_file(
            src, bdir, lambda k: EMPTY_WALL_MESH,
            "Walls off. The wall meshes carry the holding's ground decal in a decal_plane "
            "sub-mesh,\n# so pointing them at vanilla's empty western_walls_00_mesh removes the "
            "dirt patch too.\n# is_enabled is left exactly as vanilla wrote it; only the mesh "
            "changes.")
        print("  %-36s %d  %s" % ("eotg_" + WALLS_FILE, len(names), ", ".join(names)))


if __name__ == "__main__":
    main()
