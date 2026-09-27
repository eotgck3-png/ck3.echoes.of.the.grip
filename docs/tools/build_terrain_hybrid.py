"""
Hybrid terrain: a few shared structure textures + per-terrain identity in the shader.

Why this shape. Terrain is minified ~5-9 source pixels per screen pixel, so anything with pinpoint
highlights sparkles no matter how it is processed (measured local contrast 1.20 and peak/mean 13.1
on a starfield, against vanilla terrain's 0.06 / 0.3). Smooth low-frequency cloud minifies cleanly.
So the textures carry only *smooth greyscale structure*, shared across every terrain, and each
terrain's identity - colour, how much structure shows, star density - is applied per pixel by
pdxterrain.shader, which reads the material index out of DetailIndexTexture.

Consequences:
  * 3 textures to get right instead of 26.
  * Retuning a terrain is a number in the table below, not another art round.
  * Stars are generated in the shader, band-limited per camera distance, so they never alias.

This writes three things that must stay in sync, which is why one script emits all of them:
  gfx/map/terrain/eotg_structure_{a,b,c}_*.dds   the shared structure textures
  gfx/map/terrain/materials.settings             every terrain material, pointed at one of them
  gfx/FX/eotg_terrain_params.fxh                 index -> (tint, structure amount, stars) for the shader

Material indices are positional in materials.settings, so the generated .fxh is keyed off the same
ordering that wrote the file. Never hand-edit either one.

Usage:  python build_terrain_hybrid.py <mod root> [--source <image for structure A>]
"""
import os, sys, struct
import numpy as np
from PIL import Image, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_terrain_materials import save_dds_uncompressed, fbm, norm01

SIZE = 512
STRUCTURES = ("eotg_structure_a", "eotg_structure_b", "eotg_structure_c")
SOURCE_ZOOMS = (1.0, 1.7, 2.6)   # used only with --source

hx = lambda s: tuple(int(s[i:i + 2], 16) / 255 for i in (1, 3, 5))

# Tints are pushed away from grey before being written into the shader table. The structure
# textures are greyscale and the colormap soft-lights toward neutral, so a tint that looks right
# as a swatch ends up washed out on screen.
TINT_SATURATION = 1.45

def tint_rgb(hexstr):
    r, g, b = hx(hexstr)
    grey = 0.2126 * r + 0.7152 * g + 0.0722 * b
    return tuple(min(1.0, max(0.0, grey + (c - grey) * TINT_SATURATION)) for c in (r, g, b))

# terrain -> (pretty, tint, structure, tile_factor, structure_amount, star_density, star_bright, modifier)
#   tint            multiplies the greyscale structure; this is the terrain's identity
#   structure       which shared texture (0=a smooth broad, 1=b finer, 2=c very smooth)
#   tile_factor     world tiling; also varies apparent scale between terrains sharing a texture
#   structure_amount how strongly the cloud shows, 0 = flat tint, 1 = full
#   star_density    0..1, scales the procedural star field
#   star_bright     0..1
#   fx              name of an entry in FX below, or "none". An effect is a KIND (a shape-making
#                   primitive that lives in pdxterrain.shader) plus PARAMETERS (which live here).
#                   Reusing a kind with new numbers costs nothing in the shader; only a genuinely
#                   new shape does. That is what makes adding terrains later cheap.
#
#   legacy note: this column used to be a bare int that was BOTH the effect and its identity, so
#   every new effect meant editing the shader in four places. See docs/terrain_materials.md.
#   old modifier ids, for reference when reading git history:
#                   0 none
#                   1 lensing rings   teal, EOTG_MOD_LENS_*      (Anomaly Fields)
#                   2 crystalline     ice shards, MOD_CRYSTAL_*  (Frozen Cluster)
#                   3 flares          orange, MOD_FLARE_*        (Volatile Cluster)
#                   4 gas             MOD_GAS_*, tints from the terrain rather than its own colour
#                                     (Nebula Barrier AND Nebula Wilds - the only shared slot)
#                   5 strata          MOD_STRATA_*               (Layered Cluster)
#                   Slots are packed as ModA.xyzw = kinds 1..4 and ModB.xyzw = kinds 5..8, so
#                   there is room for three more kinds before the packing has to grow.

# Effect presets. kind: 1 shard (Voronoi ridge), 2 splat (rotated gaussians), 3 rings (lens, whose
# parameters stay in the shader because they are read at a neighbouring anchor), 4 bands (warped
# sine field), 5 filament (ridged warped noise).
#   color   None = tint the effect with the terrain's own colour
#   scale   cell size for 1/2/3, noise scale for 4/5
#   p, q    kind-specific, documented beside each kind in pdxterrain.shader. NOTE these are
#           overloaded per kind - q[0] is a warp scale for kinds 4/5, a density gain for kind 6,
#           and an INVERT FLAG for kind 2. Check which kind you are editing before touching q.
#   height  (lo, hi, floor) in 0..1 heightmap units - effect strength ramps from `floor` at lo to
#           full at hi. (0,0,0) disables it. Use for things that care how HIGH the ground is.
#   slope   (lo, hi, floor) on local ruggedness - the height gradient, normalised by
#           EOTG_GRAD_GAIN in the shader. Use for things that care how BROKEN the ground is.
#           Costs 4 height taps when enabled, so leave it (0,0,0) unless it earns its place.
#   q[2:4]  for kind 4 only: (altitude frequency, altitude amount). amount 1 makes the bands
#           iso-elevation lines, so the field traces the landform - see docs/terrain_materials.md.
#           frequency is how many bands across the full 0..1 height range.
#
# All height- and slope-derived numbers are provisional: map_data/ has no heightmap yet, so these
# are being tuned against the VANILLA map and will need redoing once the real one exists.
FX = {
 "none":     dict(kind=0, color=None,      gain=0.00, dark=1.00, scale=1.0,
                  p=(0,0,0,0), q=(0,0,0,0), height=(0,0,0)),
 # Frozen Cluster: ice shards gathered into floes, not an even honeycomb.
 "crystal":  dict(kind=1, color="#b8e6ff", gain=0.40, dark=0.38, scale=9.0,
                  p=(0.20, 0.038, 0.35, 0.0), q=(0,0,0,0), height=(0.08, 0.30, 0.45)),
 # Volatile Cluster: stellar flares, sparse and elongated.
 "flare":    dict(kind=2, color="#ff9e42", gain=0.85, dark=0.72, scale=14.0,
                  p=(5.2, 0.30, 0.82, 0.6), q=(0,0,0,0), height=(0,0,0)),
 # Anomaly Fields: lensing rings. Parameters live in the shader; this only selects the kind.
 "lens":     dict(kind=3, color=None,      gain=0.00, dark=1.00, scale=0.0,
                  p=(0,0,0,0), q=(0,0,0,0), height=(0,0,0)),
 # Nebula Barrier: a dense gas wall, TIED TO ALTITUDE. It thickens over high ground and thins in
 # the passes, so the chokepoints read as gaps you could actually move through. Tune the (lo, hi)
 # band against your own heightmap - these are a first guess at where sea level and ridgeline sit.
 "gaswall":  dict(kind=4, color=None,      gain=0.22, dark=0.72, scale=0.055,
                  p=(1.0, 0.35, 2.2, 2.8), q=(0.5, 0.70, 30.0, 0.30), height=(0.12, 0.34, 0.45)),
 # Layered Cluster: flat-topped strata with navigable corridors between them.
 # Layered Cluster. grain was 0, which selects the flat-topped smoothstep branch in
 # EotgFxBands: hard-edged bright bands with dark corridors between them, reported twice as an
 # "inverse oreo". Switching grain on moves it to the noise-modulated branch, so the layering is
 # broken up along its length instead of being a clean stripe, and the contrast is way down
 # (dark 0.26 -> 0.74 means the gaps no longer punch to a quarter brightness).
 # Layered Cluster: "pronounced variations in navigational elevation". The bands now follow
 # ALTITUDE rather than running across the map in world space, so the layering is drawn by the
 # landform - which is the whole concept, and it is the one terrain actually named for it. Higher
 # band frequency than the mountains use, because this terrain spans a much smaller height range.
 # Grain stays on: flat-topped altitude bands would just be hard contour lines, the same failure
 # the gas wall had. The slope gate keeps it off ground with no relief to layer.
 "strata":   dict(kind=4, color=None,      gain=0.20, dark=0.74, scale=0.060,
                  p=(0.0, 1.0, 1.25, 2.4), q=(0.35, 0.70, 165.0, 0.80),
                  height=(0,0,0), slope=(0.15, 0.60, 0.55)),
 # Broken Cluster: scattered debris. The concept is DISCRETE chunks, so this needs the sprite
 # kind - a continuous noise field can only ever produce mottle, which is what it did before.
 # The earlier choice of a noise field was made to save cost and had it backwards: EotgFbm is 3
 # octaves x 4 hashes = 36 hashes, while the 3x3 sprite loop rejects most cells on their first
 # hash and comes to about 17. The right primitive is also the cheaper one. Measured identical
 # crawl (0.0061) with higher local contrast, which is wanted here - debris should read as chunks.
 # Round (length ~ width) and small, unlike the long sparse flares that share this kind.
 # SHAPE is what separates debris from stars, not brightness. The first version was 1.17:1 -
 # round - with a 0.35 cross term, which draws a perpendicular streak: that is a plus sign, which
 # is how you draw a star. It read as hills simply having more stars than everything else.
 # Elongated shards at 4:1 with no cross cannot be confused with a point of light, and the sprite
 # already rotates per anchor so they lie at every angle. Dimmer too, since stars are the bright
 # thing on this map and debris should not compete.
 # Two things separate debris from stars, and shape is NOT one of them: the shards were 0.95
 # world units long against a star radius of 0.52-2.21, so a 4:1 aspect amounted to a pixel or
 # two of elongation and still read as a dot.
 #   SIZE     3.5 world units, several times a star, so the shape is actually resolvable.
 #   POLARITY q[0]=1 inverts the field so the chips are DARK and the gaps lit. A star is a bright
 #            point by definition; something darker than its background cannot be mistaken for
 #            one. Measured feature/background luminance 1.24 -> 0.74.
 # gain is 0 deliberately: with the field inverted, any additive term would light the GAPS.
 "debris":   dict(kind=2, color=None,      gain=0.00, dark=0.55, scale=12.0,
                  p=(3.50, 1.10, 0.30, 0.00), q=(1, 0, 0, 0), height=(0,0,0),
                  slope=(0.15, 0.60, 0.45)),
 # Barren Barrier: the dust equivalent of the gas wall - same kind, drier and darker, and tied to
 # altitude for the same reason: the passes have to stay readable.
 "dustwall": dict(kind=4, color=None,      gain=0.20, dark=0.76, scale=0.045,
                  p=(1.0, 0.60, 1.8, 2.2), q=(0.45, 0.70, 30.0, 0.40), height=(0.10, 0.30, 0.45)),
 # Nebula Barrier: a dense nebula that behaves like a volume rather than a decal - its layers
 # parallax against the camera and it thickens at grazing angles. Every number here was settled in
 # docs/tools/preview_terrain_fx.py against the real heightmap; q[0] (density gain) is the critical
 # one and must stay near 0.55, because above ~0.6 the field saturates and loses both its cloud
 # structure and its parallax at the same time.
 #   p = (layer altitude, parallax, opacity, puff)   q = (density gain, graze max, emit thresh, churn)
 "nebula":   dict(kind=6, color=None,      gain=0.26, dark=0.45, scale=0.055,
                  p=(26.0, 1.0, 0.85, 0.80), q=(0.55, 2.1, 0.55, 0.15),
                  height=(0.10, 0.34, 0.45)),
 # Barren Barrier, and every impassable province on the map. Same volumetric kind as Nebula
 # Barrier but choked: higher opacity, a darker floor so it genuinely obscures, and almost no
 # emission - nothing is alight in here. Gain stays near 0.6 for the same reason as the nebula:
 # push it higher and the field saturates into a flat wash.
 "nebula_dead": dict(kind=6, color=None,     gain=0.24, dark=0.34, scale=0.048,
                  p=(22.0, 1.0, 0.92, 0.85), q=(0.62, 1.9, 0.80, 0.10),
                  height=(0.0, 0.0, 0.0)),
 # Nebula Wilds: a tangled thicket of filaments. Warm, fine, and braided rather than banded -
 # the whole point is that it must not read as the Barrier's gas.
 "filament": dict(kind=5, color="#e07898", gain=0.26, dark=0.55, scale=0.065,
                  p=(1.5, 0.55, 2.2, 0.4), q=(0.6, 0, 0, 0), height=(0,0,0)),

 # --- the pale blue-grey trio -------------------------------------------------------------
 # forest #90a0b8, steppe #8ea8ae and taiga #8fc0e0 are the three closest pairs on the whole
 # map: forest/steppe 10.3, taiga/steppe 11.2, taiga/forest 11.6. Their hues are hemmed in by
 # the rest of the palette and cannot be pushed much further apart without colliding with
 # something else, so they are separated by SHAPE instead - which CIEDE2000 cannot measure and
 # the eye reads first. Taiga already has hard crystal shards; these two take the other two
 # textures a cloud can have.

 # Dense Cluster: unresolved haze BETWEEN the stars. Its star_density is already 1.00, so what
 # it lacks is not more points but something continuous behind them. Same kind as the Barrier
 # at a third of the gain and a much larger scale, so it reads as depth rather than as wall.
 "haze":     dict(kind=6, color="#a8c0d8", gain=0.09, dark=0.80, scale=0.028,
                  p=(18.0, 1.0, 0.70, 0.55), q=(0.40, 1.6, 0.45, 0.10), height=(0,0,0)),

 # Frontier Reach: thin drifting strands, the opposite of forest's glow. Scale stays inside the
 # 0.055-0.075 band the Wilds filament had to be dragged back into - at 0.16 it flooded the map
 # pink. Gain is a third of Wilds' and the colour is near-neutral, so the two do not converge:
 # Wilds is a hot tangled thicket, Frontier is a few cold threads across emptiness.
 "strands":  dict(kind=5, color="#b6c6cc", gain=0.10, dark=0.82, scale=0.058,
                  p=(1.1, 0.40, 1.7, 0.25), q=(0.55, 0, 0, 0), height=(0,0,0)),

 # Arid Reach: sparse dust motes. Same sprite kind as debris and flares, but small, dim and
 # warm - debris is 3.50 long and dark-polarity, flares are 5.2 long and bright orange. These
 # are round, a third the size, and barely above the tint.
 # Swept for coverage against the aliasing gates: at the first numbers it covered only 2.6% of
 # ground, about as sparse as the flares, which is invisible across the large flat areas this
 # terrain occupies. These give 9.4% - between flares and debris' 16.3% - at lc 0.025 and peak
 # 0.232, both far inside the gates.
 "dust":     dict(kind=2, color="#c8a878", gain=0.30, dark=0.88, scale=13.0,
                  p=(1.60, 1.25, 0.12, 0.0), q=(0, 0, 0, 0), height=(0,0,0)),
}

# Hypsometric ramp, per terrain: the tint shifts toward ALT colour as altitude rises.
#   terrain -> (high-altitude colour, (lo, hi, amount))   amount 0 / absent = flat, no ramp
# This is how height becomes legible from colour rather than only from the lighting. Terrains that
# are meant to read as flat regions should NOT have one; it is for landforms.
# Star colour temperature per terrain: 0 = amber, 0.5 = white, 1 = blue-white. Each star jitters
# around its terrain's value, so this is a bias rather than a fixed colour. These follow what
# docs/terrain_texture_prompts.md already says about each region - "dim blue stars" for Frozen
# Cluster, "warm golden stars" for Fertile Reach and Sanctuary Systems, "pale stars" for Frontier
# Reach - none of which was true while every star on the map was the same white.
STAR_TEMP = {
 "plains": 0.50, "hills": 0.45, "desert": 0.62, "mountains": 0.55,
 "taiga": 0.88, "drylands": 0.32, "forest": 0.58, "steppe": 0.66,
 "jungle": 0.30, "desert_mountains": 0.38, "wetlands": 0.70,
 "farmlands": 0.14, "floodplains": 0.20, "oasis": 0.12, "terraced_hills": 0.52,
}

# How much world-space procedural noise to mix into the tiled detail, per terrain. The detail
# texture repeats tile_factor times across the map; on a big terrain with nothing else in it that
# repeat reads as wallpaper (the Sahara was the clear case). Noise cannot repeat, so mixing it in
# breaks the grid. Costs 2 FBM where it is non-zero, so it is spent on the large empty terrains
# and left off the ones whose own detail already hides the tile.
TILEBREAK = {
 # Measured: mixing linearly, autocorrelation at the tile period falls 0.999 -> 0.46 -> 0.10
 # as the mix goes 0.0 -> 0.6 -> 0.8, so anything under about 0.65 still reads as a grid.
 "desert": 0.85, "plains": 0.78, "drylands": 0.78, "steppe": 0.75,
 "desert_mountains": 0.70, "hills": 0.62, "forest": 0.55, "taiga": 0.55,
}

# Relief shading strength per terrain, 0 = flat. This is the main cue for landform shape; give it
# to terrains that ARE a landform and leave it off for ones meant to read as open regions, or the
# whole map turns into a relief chart.
SHADE = {
 "mountains": 0.55, "desert_mountains": 0.45, "hills": 0.33,
 "taiga": 0.28, "terraced_hills": 0.30,
}

ALT = {
 # Nebula Barrier: deep violet in the valleys climbing to a pale, lit crown on the peaks. With the
 # altitude banding on the gas as well, the range shows its own relief instead of being a wash.
 # Peaks go DENSER, not paler. The first version ramped toward a light lavender and nearly
 # doubled peak luminance (0.298 -> 0.569), which read as the effect petering out and the colour
 # changing at altitude. Height legibility is carried by the nebula and the hillshade now, so this
 # only has to add a little depth: gas pooling thicker on the summits.
 # Peaks shift HUE rather than lightness: the body is violet at 257 deg, the summits magenta at
 # 290, so the densest gas reads as hotter. Lightening instead (the first attempt) nearly doubled
 # peak luminance and looked like the effect petering out into grey; darkening (the second) made
 # them barely distinguishable. 1.2x luminance with a hue shift is the version that reads.
 "mountains":        ("#a03fb4", (0.15, 0.50, 0.55)),
 # Barren Barrier: dust catches the light higher up, but stays drab.
 "desert_mountains": ("#9a5030", (0.11, 0.38, 0.50)),
 # Frozen Cluster: ice whitens with altitude.
 "taiga":            ("#c4e2f5", (0.10, 0.34, 0.45)),
 # Broken Cluster: high rubble is bare and lighter than the fill between it.
 # Hills had a ramp to warm tan at altitude, added back when every terrain needed height
 # legibility. It is the source of the tan patches appearing inside mountain ranges, and tan is
 # the one earth colour on a violet map. Relief shading carries hills' form on its own now.
 # (kept here, disabled, because the entry documents why it should not come back)
 # "hills":          ("#998c7c", (0.10, 0.32, 0.30)),
}

TERRAINS = {
 # Palette is spread deliberately: 15 terrains were crowded into 3 hue families (5 cool greys,
 # 3 tans, 3 golds) and collided in pairs. Run docs/tools/check_terrain_distinctness.py after any
 # edit here - it reads this table and will tell you which pairs you just merged.
 "plains":          ("Open Cluster",       "#6a7290", 0, 337, 0.55, 0.48, 0.60, "none"),  # the baseline everything else is read against
 "hills":           ("Broken Cluster",     "#85796a", 1, 520, 0.85, 0.48, 0.55, "debris"),  # warm stone-grey; kept well clear of plains, which it borders constantly
 "desert":          ("Barren Reach",       "#3f4a62", 2, 260, 0.35, 0.08, 0.45, "none"),  # cold near-black void
 # Barrier vs Wilds must not converge: they were 4 of 7 axes apart and read as the same purple
 # cloud in game. Barrier = a solid cold WALL (big, flat, starless); Wilds = a warm tangled
 # THICKET (fine, lumpy, stars showing through). See docs/terrain_scheme.md.
 # star_density 0.02 -> 0.22, star_bright 0.30 -> 0.38: a few stars showing THROUGH the
 # barrier, so it reads as dense cloud you can just see past rather than an opaque wall.
 # Still far below Wilds (0.55), which is the terrain Barrier must not converge with, and
 # below plains (0.48) so it stays the emptier of the two. Impassable mountains are NOT
 # affected: build_terrain_index forces every impassable province into desert_mountains.
 "mountains":       ("Nebula Barrier",     "#5c3f9e", 0, 150, 0.65, 0.22, 0.38, "nebula"),
 "taiga":           ("Frozen Cluster",     "#8fc0e0", 1, 430, 0.80, 0.48, 0.65, "crystal"),
 "drylands":        ("Arid Reach",         "#a8874a", 2, 380, 0.60, 0.26, 0.45, "dust"),  # saturated ochre dust
 "forest":          ("Dense Cluster",      "#90a0b8", 0, 600, 0.55, 1.00, 0.75, "haze"),
 "steppe":          ("Frontier Reach",     "#8ea8ae", 2, 300, 0.40, 0.18, 0.50, "strands"),  # pale cyan-grey, emptier than plains
 "jungle":          ("Nebula Wilds",       "#d05c86", 1, 420, 1.00, 0.55, 0.45, "filament"),
 "desert_mountains":("Barren Barrier",     "#6b3a32", 0, 220, 0.90, 0.08, 0.35, "nebula_dead"),  # ALSO the wastelands: build_terrain_index forces every impassable province here. Burnt rust, not grey.
 "wetlands":        ("Anomaly Fields",     "#3fbfb0", 1, 350, 0.70, 0.48, 0.60, "lens"),
 "farmlands":       ("Fertile Reach",      "#ffc861", 0, 450, 0.65, 1.00, 0.90, "none"),
 "floodplains":     ("Volatile Cluster",   "#e08a45", 2, 400, 0.70, 0.72, 0.85, "flare"),
 "oasis":           ("Sanctuary Systems",  "#fff2e4", 1, 500, 0.55, 1.00, 0.95, "none"),  # near-white cream: the brightest thing on the map, a visible sanctuary
 "terraced_hills":  ("Layered Cluster",    "#5d7f8a", 2, 300, 0.75, 0.72, 0.55, "strata"),  # muted slate-teal; the earlier olive green won the distinctness metric but was the one earth colour on a violet/teal/gold map
}
EDGES = [("eotg_edge_01", "#8a4ad0", 0, 420, 0.80, 0.35, 0.60, "none"),
         ("eotg_edge_02", "#e0b060", 1, 420, 0.80, 0.35, 0.60, "none")]
DYNAMIC = ["drought", "drought_cracks", "flood", "summer_grass", "winter_effect"]


# The structure textures must stay LOW CONTRAST. Stretching a source to full range (norm01) is
# wrong here: a dark cloud image whose brightest wisp is 0.36 gets pushed to 0.80, which reads as
# snow and makes the tiling obvious. Map percentiles instead, so outliers clip rather than stretch.
STRUCT_LO, STRUCT_HI = 0.40, 0.62      # where p2 and p98 land
STRUCT_CLIP = (0.33, 0.70)


def normalise_structure(a):
    lo, hi = np.percentile(a, 2), np.percentile(a, 98)
    a = STRUCT_LO + (STRUCT_HI - STRUCT_LO) * (a - lo) / (hi - lo + 1e-6)
    return np.clip(a, *STRUCT_CLIP)


def make_seamless(a):
    """Offset-and-blend per axis, so opposite edges become neighbours and the tile closes."""
    h, w = a.shape
    for axis, n in ((1, w), (0, h)):
        t = np.arange(n, dtype=np.float32) / n
        m = 0.5 * (1.0 - np.cos(2.0 * np.pi * t))
        m = m.reshape((1, n) if axis == 1 else (n, 1))
        a = a * m + np.roll(a, n // 2, axis=axis) * (1.0 - m)
    return a


def smooth_structure(size, seed, base, octaves, soften):
    """Greyscale cloud. Deliberately low local contrast - that is the whole point."""
    rng = np.random.default_rng(seed)
    a = norm01(fbm(size, octaves, base, rng=rng))
    a = np.asarray(Image.fromarray((a * 255).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(soften)), dtype=np.float32) / 255.0
    return normalise_structure(a)


# Background level and peak for line-mode. The peak may reach white because the bright
# set is a thin network: measured local_contrast 0.208 against the 0.35 shimmer limit.
LINE_BG, LINE_PEAK, LINE_CLIP_LO = 0.36, 1.00, 0.28


def normalise_lines(a):
    """For sources whose signal is a sparse bright line network rather than a cloud."""
    lo, hi = np.percentile(a, 50), np.percentile(a, 99.5)
    out = LINE_BG + (a - lo) * (LINE_PEAK - LINE_BG) / max(hi - lo, 1e-6)
    return np.clip(out, LINE_CLIP_LO, 1.0)


def from_source(path, size, seamless=True, zoom=1.0, lines=True):
    """zoom > 1 crops tighter before resizing, which widens the source's features."""
    im = Image.open(path).convert("L")
    w, h = im.size
    s = int(min(w, h) / max(zoom, 1e-3))
    s = max(8, min(s, min(w, h)))
    im = im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((size, size), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float32) / 255.0
    a = normalise_lines(a) if lines else normalise_structure(a)
    if seamless:
        a = make_seamless(a)
    return a


def write_structure(outdir, name, grey):
    s = grey.shape[0]
    d = np.zeros((s, s, 4), np.uint8)
    for c in range(3):
        d[..., c] = np.clip(grey * 255, 0, 255)
    d[..., 3] = np.clip(grey * 255, 0, 255)          # alpha = height, drives the 4-way blend
    save_dds_uncompressed(Image.fromarray(d, "RGBA"), os.path.join(outdir, f"{name}_diffuse.dds"))
    # normal from the structure, DXT5nm / RRxG packing
    hpad = np.pad(grey, 1, mode="wrap")
    gx = (hpad[1:-1, 2:] - hpad[1:-1, :-2]) * 0.5
    gy = (hpad[2:, 1:-1] - hpad[:-2, 1:-1]) * 0.5
    nx, ny = -gx * 6.0, -gy * 6.0
    ln = np.sqrt(nx * nx + ny * ny + 1.0)
    nx, ny = nx / ln, ny / ln
    n = np.zeros((s, s, 4), np.uint8)
    n[..., 0] = n[..., 1] = np.clip((nx * 0.5 + 0.5) * 255, 0, 255)
    n[..., 2] = 255
    n[..., 3] = np.clip((-ny * 0.5 + 0.5) * 255, 0, 255)
    save_dds_uncompressed(Image.fromarray(n, "RGBA"), os.path.join(outdir, f"{name}_normal.dds"))
    p = np.zeros((s, s, 4), np.uint8)
    p[..., 1] = 40          # specular
    p[..., 2] = 0           # metalness
    p[..., 3] = 220         # roughness
    save_dds_uncompressed(Image.fromarray(p, "RGBA"), os.path.join(outdir, f"{name}_properties.dds"))


def main():
    root = sys.argv[1]
    source = sys.argv[sys.argv.index("--source") + 1] if "--source" in sys.argv else None
    # Two content types need different normalisation: a thin bright network (a grid) keeps
    # its peaks, a broad cloud must be clamped or it reads as snow. Default is line-mode.
    lines_mode = "--cloud" not in sys.argv
    outdir = os.path.join(root, "gfx", "map", "terrain")
    fxdir = os.path.join(root, "gfx", "FX")
    os.makedirs(outdir, exist_ok=True); os.makedirs(fxdir, exist_ok=True)
    os.makedirs(os.path.join(outdir, "masks"), exist_ok=True)

    # --- the three shared structure textures -------------------------------------------------
    greys = []
    if source:
        # One source across all three slots, at three zooms, so terrains still differ.
        for name, z in zip(STRUCTURES, SOURCE_ZOOMS):
            greys.append(from_source(source, SIZE, zoom=z, lines=lines_mode))
            print(f"  {name[5:]} <- {os.path.basename(source)}  "
                  f"(zoom {z:g}x, {'line' if lines_mode else 'cloud'}-mode)")
    else:
        greys.append(smooth_structure(SIZE, 11, 3, 6, 1.5)); print("  structure_a  procedural (broad)")
        greys.append(smooth_structure(SIZE, 23, 5, 6, 1.2)); print("  structure_b  procedural (finer)")
        greys.append(smooth_structure(SIZE, 37, 2, 5, 2.4)); print("  structure_c  procedural (very smooth)")
    for name, g in zip(STRUCTURES, greys):
        write_structure(outdir, name, g)

    # --- materials.settings ------------------------------------------------------------------
    entries = []        # (id, structure_index, tile, params...)
    L = ["# MOD(eotg) generated by docs/tools/build_terrain_hybrid.py - do not hand-edit.",
         "# Every terrain material points at one of three SHARED structure textures; the terrain's",
         "# colour, structure amount and star density are applied by pdxterrain.shader, which reads",
         "# the material index from DetailIndexTexture. See gfx/FX/eotg_terrain_params.fxh.",
         "", "{",
         "\t# Dynamic materials - positional index, DO NOT REORDER. Effects are disabled in the",
         "\t# shaders, so these never draw; they point at structure A purely to stay array-consistent."]
    for dyn in DYNAMIC:
        L += ["\t{", f'\t\tname     = "{dyn}"', '\t\tdiffuse  = "eotg_structure_a_diffuse.dds"',
              '\t\tnormal   = "eotg_structure_a_normal.dds"', '\t\tmaterial = "eotg_structure_a_properties.dds"',
              f'\t\tmask     = "masks/{dyn}_mask.png"', f'\t\tid       = "{dyn}"', "\t}"]
        entries.append((dyn, 0, None, "#000000", 0.0, 0.0, 0.0, "none"))
    L += ["", "\t# EotG terrains"]
    def emit(mid, pretty, tint, st, tile, amt, sd, sb, mod):
        s = STRUCTURES[st]
        L.extend(["\t{", f'\t\tname     = "{mid}"', f'\t\tdiffuse  = "{s}_diffuse.dds"',
                  f'\t\tnormal   = "{s}_normal.dds"', f'\t\tmaterial = "{s}_properties.dds"',
                  f'\t\tmask     = "masks/{mid}_mask.png"', f'\t\tid       = "{mid}"',
                  f"\t\ttile_factor = {tile}", f"\t\t# {pretty}", "\t}"])
        entries.append((mid, st, tile, tint, amt, sd, sb, mod))
    for terr, (pretty, tint, st, tile, amt, sd, sb, mod) in TERRAINS.items():
        emit(f"eotg_{terr}_01", pretty, tint, st, tile, amt, sd, sb, mod)
    for mid, tint, st, tile, amt, sd, sb, mod in EDGES:
        emit(mid, "System Edge", tint, st, tile, amt, sd, sb, mod)
    L += ["}", "", "# unmasked textures (vanilla ships this block empty; the parser requires it)", "{", "}", ""]
    with open(os.path.join(outdir, "materials.settings"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L))

    # --- the shader's lookup table, keyed off the ordering just written ----------------------
    n = len(entries)
    F = ["# MOD(eotg) GENERATED by docs/tools/build_terrain_hybrid.py - do not hand-edit.",
         "# Index -> terrain appearance. Indices are positional in materials.settings, and both",
         "# files are written by the same run, so they cannot drift apart.", "",
         "PixelShader = {", "\tCode", "\t[[",
         f"\t\tstatic const int EOTG_TERRAIN_COUNT = {n};", ""]
    def arr(name, typ, vals):
        F.append(f"\t\tstatic const {typ} {name}[{n}] = {{")
        F.append("\t\t\t" + ", ".join(vals))
        F.append("\t\t};")
    arr("EOTG_TINT", "float3", [f"float3( {tint_rgb(e[3])[0]:.3f}f, {tint_rgb(e[3])[1]:.3f}f, {tint_rgb(e[3])[2]:.3f}f )" for e in entries])
    arr("EOTG_STRUCTURE_AMOUNT", "float", [f"{e[4]:.2f}f" for e in entries])
    arr("EOTG_STAR_DENSITY", "float", [f"{e[5]:.2f}f" for e in entries])
    arr("EOTG_STAR_BRIGHT", "float", [f"{e[6]:.2f}f" for e in entries])
    def fx(e):
        return FX.get(e[7], FX["none"])
    def f4(v):
        return f"float4( {v[0]:.4f}f, {v[1]:.4f}f, {v[2]:.4f}f, {v[3]:.4f}f )"
    def alt(e):
        return ALT.get(e[0].replace("eotg_", "").rsplit("_01", 1)[0], (None, (0, 0, 0)))
    arr("EOTG_STAR_TEMP", "float", [
        f"{STAR_TEMP.get(e[0].replace('eotg_', '').rsplit('_01', 1)[0], 0.50):.2f}f" for e in entries])
    arr("EOTG_TILEBREAK", "float", [
        f"{TILEBREAK.get(e[0].replace('eotg_', '').rsplit('_01', 1)[0], 0.0):.3f}f" for e in entries])
    arr("EOTG_SHADE", "float", [
        f"{SHADE.get(e[0].replace('eotg_', '').rsplit('_01', 1)[0], 0.0):.3f}f" for e in entries])
    arr("EOTG_ALT_TINT", "float3", [
        (lambda c: f"float3( {c[0]:.3f}f, {c[1]:.3f}f, {c[2]:.3f}f )")(
            tint_rgb(alt(e)[0]) if alt(e)[0] else (0.0, 0.0, 0.0)) for e in entries])
    arr("EOTG_ALT_BAND", "float3", [
        (lambda v: f"float3( {v[0]:.3f}f, {v[1]:.3f}f, {v[2]:.3f}f )")(alt(e)[1]) for e in entries])
    arr("EOTG_FX_KIND", "int", [f"{fx(e)['kind']}" for e in entries])
    arr("EOTG_FX_COLOR", "float3", [
        (lambda c: f"float3( {c[0]:.3f}f, {c[1]:.3f}f, {c[2]:.3f}f )")(hx(fx(e)["color"]) if fx(e)["color"] else (0.0, 0.0, 0.0))
        for e in entries])
    arr("EOTG_FX_USETINT", "float", [f"{0.0 if fx(e)['color'] else 1.0:.1f}f" for e in entries])
    arr("EOTG_FX_GAIN", "float", [f"{fx(e)['gain']:.3f}f" for e in entries])
    arr("EOTG_FX_DARK", "float", [f"{fx(e)['dark']:.3f}f" for e in entries])
    arr("EOTG_FX_SCALE", "float", [f"{fx(e)['scale']:.5f}f" for e in entries])
    arr("EOTG_FX_P", "float4", [f4(fx(e)["p"]) for e in entries])
    arr("EOTG_FX_Q", "float4", [f4(fx(e)["q"]) for e in entries])
    arr("EOTG_FX_SLOPE", "float3", [
        (lambda v: f"float3( {v[0]:.3f}f, {v[1]:.3f}f, {v[2]:.3f}f )")(fx(e).get("slope", (0, 0, 0)))
        for e in entries])
    arr("EOTG_FX_HEIGHT", "float3", [
        (lambda h: f"float3( {h[0]:.3f}f, {h[1]:.3f}f, {h[2]:.3f}f )")(fx(e)["height"]) for e in entries])
    F += ["", "\t]]", "}", ""]
    with open(os.path.join(fxdir, "eotg_terrain_params.fxh"), "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(F))

    # dummy masks so materials.settings' references resolve
    blank = Image.new("L", (64, 64), 0)
    for e in entries:
        blank.save(os.path.join(outdir, "masks", f"{e[0]}_mask.png"))

    print(f"\nmaterials.settings: {n} entries ({n - len(DYNAMIC)} terrain + {len(DYNAMIC)} dynamic)")
    print(f"eotg_terrain_params.fxh: {n}-entry lookup table")
    print(f"structure textures: {len(STRUCTURES)} x 3 files")


if __name__ == "__main__":
    main()
