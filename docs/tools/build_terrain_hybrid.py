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
 # Frozen Cluster is the Pleiades: an open cluster that has drifted into a cold dust cloud.
 # Kind 7, built for this, because a Voronoi can only read as filled cells or as a net and both
 # were rejected - the primitive was the problem, not its numbers.
 #
 # Two mechanics, both from the real object. STRIAE run parallel on one heading, because the
 # dust grains are combed into alignment by the interstellar magnetic field; that is what keeps
 # them clear of steppe's randomly-oriented strands and terraced_hills' altitude bands. And the
 # nebula is a REFLECTION nebula, so it only glows where starlight reaches it: the halos sit on
 # this terrain's own star anchors, and the striae are modulated by that same glow.
 #
 # Measured before shipping. Halo radius and the fraction of stars bright enough to light the
 # dust both matter more than gain: at radius 0.55 with every star lit, the halos overlapped and
 # covered 94% of the ground, which is a flat wash with no cluster in it. At 0.30 and 0.55 the
 # coverage is 17% and it reads as knots with dark between them. Colour #eaf4ff sits dE 17.1
 # from the taiga tint - the old crystal blue was 9.5, closer than the dust that turned out
 # invisible. lc 0.052, inside the gates.
 # SECOND PASS, after the first shipped as a lattice of dots. Two mistakes, one cause.
 #
 # The striae were at a 2.86 world-unit period, which is a hatch rather than a wisp, and the
 # halos at 55% of anchors with a 2.5-unit radius made a dense dot field that swamped them. The
 # result read as spotty, which is the opposite of the reference. The cause was scoring the
 # effect with metrics instead of LOOKING at it: lc 0.052 passed the gates while the field was
 # a dot lattice, because a regular pattern of soft blobs has low local contrast. The harness
 # also warns in its own docstring that world-units-per-pixel is the one genuine unknown and
 # that --wpp sweeps it, and that sweep was not run.
 #
 # Now streak-led: period 24 world units, warp more than doubled so they meander instead of
 # ruling, and the halos rare (12% of anchors) and wide (7.6 units) so they brighten stretches
 # of the striae rather than punching dots through them. Rendered and looked at across
 # wpp 0.5/1/2 - it stays wisps at all three - and lc 0.021-0.052 with crawl 0.0.
 # THIRD PASS. The streaks were right in character but wrong in weight: broad bright bands
 # ruling the whole terrain, with visible square patches through them. The squares were the
 # warp - one octave of value noise sampled on an axis-aligned grid, which at this low a
 # frequency shows its own grid. The shader now sums a second, finer, ROTATED octave, which
 # breaks the alignment. Stria power 2.6 -> 4.5 for a thinner wisp, gain and stria gain down.
 # Rendered and compared side by side rather than scored: lit area 8.7% -> 3.4%.
 # Frozen Cluster is on "none" as a RESTING STATE, not as a decision. Seven attempts were
 # rejected - honeycomb, fracture net, dot lattice, all-over weave, ruled lines, contour rings,
 # ice shards - so it is parked plain rather than left wearing the last thing tried.
 #
 # It is not undefended without one. Its two closest neighbours, forest at dE 11.6 and steppe
 # at 11.2, both HAVE effects, so "this one is plain" is itself the distinguishing feature, and
 # it keeps the highest star density of the three (0.48) plus the palest tint on that side of
 # the palette. The global contour overlay now gives every terrain some structure as well.
 #
 # Frozen Cluster, seventh attempt, and a change of primitive rather than another tuning
 # pass. The Pleiades effect below is kept but unused - six rounds on it produced a honeycomb,
 # a net, a dot lattice, an all-over weave, ruled lines and then contour rings, and each fix
 # traded one artifact for another. That is a sign the primitive is fighting the brief.
 #
 # ICE SHARDS instead: discrete elongated splinters, kind 2. Three reasons.
 #   * Kind 2's nearest other user is dE 31.8 away, so there is no convergence risk at all -
 #     unlike kinds 5 and 6, which taiga cannot touch because steppe and forest sit at 11.2
 #     and 11.6.
 #   * It is the ONE kind the preview harness models faithfully, so it can be verified end to
 #     end instead of eyeballed. Everything that went wrong with the Pleiades effect went wrong
 #     in a kind with no CPU model.
 #   * Discrete splinters are not something any other terrain does.
 # Length 6.0 against a star radius under 1.7 keeps them clear of the stars - size is what
 # separates a shard from a star, which the debris effect had to learn three times.
 # Rendered sparse-to-dense before choosing: coverage 2.4%, lc 0.020, peak 0.341.
 # Frozen Cluster: pack ice. AREAS, not lines or points - a noise field thresholded into
 # plates with soft edges and a varying interior. Every other effect on the map is lines,
 # points, rings or bands, so this cannot be confused with any of them even though taiga's two
 # nearest neighbours sit only dE 11.2 and 11.6 away in colour.
 #
 # Thresholds are in EotgFbmRot's RAW range - roughly 0 to 0.84, mean 0.475 - derived by
 # measuring the function rather than assuming 0..1. At 0.600/0.070 the plates cover about 13%,
 # which is drifts on clean ground; the first prototype sat at 48% and read as camouflage.
 "packice":  dict(kind=8, color="#eaf4ff", gain=0.32, dark=0.88, scale=0.032,
                  p=(0.600, 0.070, 0.30, 0.0), q=(0,0,0,0), height=(0,0,0)),

 "iceshard": dict(kind=2, color="#eaf4ff", gain=0.65, dark=0.70, scale=34.0,
                  p=(6.00, 0.75, 0.50, 0.25), q=(0, 0, 0, 0), height=(0,0,0)),

 # UNUSED. Kept because it is a lot of measured work and may be wanted for another terrain.
 # FIFTH PASS, and the first one that started by comparing taiga against the terrains that
 # had already been approved instead of tuning it in isolation. Forest haze runs at gain 0.09
 # and steppe strands at 0.10; taiga was at 0.62, six times either, which is why it read as
 # loud next to terrains that read as atmosphere. Gain 0.62 -> 0.30, and the striae floor in
 # the shader 0.18 -> 0.08 so the ground between lit patches goes quiet rather than carrying a
 # weave across the whole terrain. Rendered at three gains side by side: 0.62 is an all-over
 # texture, 0.20 is invisible, 0.30 is nebulosity gathered into patches.
 "pleiades": dict(kind=7, color="#eaf4ff", gain=0.30, dark=0.72, scale=0.24,
                  p=(1.00, 1.45, 0.70, 0.95), q=(0.15, 0.60, 0.013, 0.11),
                  height=(0,0,0)),
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
 # Arid Reach: dust silhouetted against the glow, not lit motes on top of it.
 #
 # The first version was warm tan motes, #c8a878, on a warm tan terrain, #a8874a. Measured
 # afterwards: dE 10.8 between the two. The distinctness tool calls anything under 10 "cannot
 # tell apart", so the effect was invisible by construction - for comparison crystal sits 42.2
 # from its terrain and filament 37.3 from its.
 #
 # Inverted instead, the way debris is (q[0]=1): the motes are DARK and the gaps stay lit. That
 # fixes both problems at once. Dark on ochre actually contrasts, and it cannot be misread as
 # stars, which are always bright points - the confusion that cost the debris effect three
 # attempts. Coverage 9.4%, lc 0.032, peak 0.28, well inside the gates.
 # scale 13 -> 9 roughly doubles the count: coverage 9.4% -> 19.1%, lc 0.054, peak 0.360,
 # both still well inside the gates. Q.y/Q.z split the field into two populations - half the
 # motes render at 35% strength, so the field is half solid dust and half a thin grey veil
 # rather than a uniform stipple. Q.y = 0 on every other effect, so debris and the flares are
 # unchanged.
 "dust":     dict(kind=2, color=None, gain=0.00, dark=0.70, scale=9.0,
                  p=(1.60, 1.25, 0.12, 0.0), q=(1, 0.50, 0.35, 0), height=(0,0,0)),
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
# --- star size / brightness distributions (doc sections 4 and 4.1) -----------------------
# size  mean star size 0..1. Defaults to the terrain's own star_density, which is what used
#       to drive size directly - so an unlisted terrain looks exactly as it did before.
# ssk   size skew. 1.0 = even spread. >1 = mostly small with a rare large one. <1 = mostly
#       large. The draw is normalised by (skew+1) so the MEAN stays `size` at any skew.
# bsk   brightness skew, same shape, normalised the same way: a high skew means "mostly dim
#       with a rare bright one", not "uniformly dimmer".
#
# Size is deliberately NOT tied to density any more. That coupling is why the two Barren
# terrains read as uniformly tiny - they are meant to be sparse, not featureless, and a few
# large isolated stars say "empty" better than many small ones do.
# --- secondary effects ------------------------------------------------------------------
# A rare second effect, layered under the primary at reduced strength. Only worth giving to
# LARGE terrains: at ~1/8 coverage a terrain under a percent of the map would effectively
# never show one. The secondary must be a different KIND from the primary - they share the
# kind's slot, and the heavier weight would simply win.
FX2_GAIN_CAP = 0.35      # secondary emits at 35% of its normal gain
FX2_DARK_BLEND = 0.70    # and darkens 70% less, so it reads as texture, not as an effect
FX2 = {
    "impassable":       "strata",    # Impassable Barrier is 21.4% of the map on its own - the
                                     # single most repeated terrain, so the biggest payoff.
                                     # Occasional layered structure in an otherwise dead wall.
    "desert_mountains": "strands",   # Barren Barrier shares both its tint AND its primary
                                     # (nebula_dead) with impassable - the distinctness check
                                     # calls them TWINS at dE 0.0. Different secondaries are
                                     # the one thing currently telling them apart.
    "plains":           "strands",   # Open Cluster: the deliberately empty baseline. Rare
                                     # drifting wisps, so "empty" is not "uniform".
    "desert":           "debris",    # Barren Reach: an occasional debris field - something
                                     # happened here once.
    "hills":            "strands",   # Broken Cluster: wisps caught in the rubble.
}


STAR_PROFILE_DEFAULT = dict(ssk=1.0, bsk=1.0)
STAR_PROFILE = {
    "forest":           dict(size=0.30, ssk=2.6),            # Dense Cluster: crowded with small stars
    "farmlands":        dict(size=0.70, ssk=1.0, bsk=0.8),   # Fertile Reach: large and generally bright
    "oasis":            dict(size=0.90, ssk=0.7, bsk=0.6),   # Sanctuary Systems: few, large, bright
    "floodplains":      dict(size=0.65, ssk=1.2, bsk=0.5),   # Volatile Cluster: many flaring
    "desert":           dict(size=0.55, ssk=1.4),            # Barren Reach: sparse but each one reads
    "desert_mountains": dict(size=0.50, ssk=1.5),            # Barren Barrier: same, dimmer
    "mountains":        dict(size=0.30, ssk=2.0, bsk=1.8),   # Nebula Barrier: dim pinpricks through gas
    "jungle":           dict(size=0.35, ssk=2.2),            # Nebula Wilds: fine and tangled
    "taiga":            dict(size=0.50, bsk=1.6),            # Frozen Cluster: cold, mostly dim
}


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
 # Barren Reach and Barren Barrier raised again 0.10 -> 0.16 after provinces were found
 # with literally no stars. The real cause was the density GAMMA, fixed in the shader;
 # this is the second half, so the two barren terrains clear the floor with margin
 # while staying the emptiest on the map.
 # Star density raised across the board 2026-09-27: +0.06 on everything, except the two
 # Barren terrains which got +0.02. A flat bump would have lifted those proportionally the
 # most - 0.08 to 0.14 is +75% - and they are named for emptiness, so the thing that makes
 # them read would have been the thing most eroded. Forest, farmlands and oasis were
 # already at 1.00 and are unchanged; the ordering is preserved and nothing clamps.
 # Palette is spread deliberately: 15 terrains were crowded into 3 hue families (5 cool greys,
 # 3 tans, 3 golds) and collided in pairs. Run docs/tools/check_terrain_distinctness.py after any
 # edit here - it reads this table and will tell you which pairs you just merged.
 "plains":          ("Open Cluster",       "#6a7290", 0, 337, 0.55, 0.54, 0.60, "none"),  # the baseline everything else is read against
 "hills":           ("Broken Cluster",     "#85796a", 1, 520, 0.85, 0.54, 0.55, "debris"),  # warm stone-grey; kept well clear of plains, which it borders constantly
 "desert":          ("Barren Reach",       "#3f4a62", 2, 260, 0.35, 0.16, 0.45, "none"),  # cold near-black void
 # Barrier vs Wilds must not converge: they were 4 of 7 axes apart and read as the same purple
 # cloud in game. Barrier = a solid cold WALL (big, flat, starless); Wilds = a warm tangled
 # THICKET (fine, lumpy, stars showing through). See docs/terrain_scheme.md.
 # star_density 0.02 -> 0.22, star_bright 0.30 -> 0.38: a few stars showing THROUGH the
 # barrier, so it reads as dense cloud you can just see past rather than an opaque wall.
 # Still far below Wilds (0.55), which is the terrain Barrier must not converge with, and
 # below plains (0.48) so it stays the emptier of the two. Impassable mountains are NOT
 # affected: build_terrain_index forces every impassable province into "impassable" below.
 "mountains":       ("Nebula Barrier",     "#5c3f9e", 0, 150, 0.65, 0.28, 0.38, "nebula"),
 "taiga":           ("Frozen Cluster",     "#8fc0e0", 1, 430, 0.80, 0.54, 0.65, "packice"),
 "drylands":        ("Arid Reach",         "#a8874a", 2, 380, 0.60, 0.32, 0.45, "dust"),  # saturated ochre dust
 "forest":          ("Dense Cluster",      "#90a0b8", 0, 600, 0.55, 1.00, 0.75, "haze"),
 "steppe":          ("Frontier Reach",     "#8ea8ae", 2, 300, 0.40, 0.24, 0.50, "strands"),  # pale cyan-grey, emptier than plains
 "jungle":          ("Nebula Wilds",       "#d05c86", 1, 420, 1.00, 0.61, 0.45, "filament"),
 "desert_mountains":("Barren Barrier",     "#6b3a32", 0, 220, 0.90, 0.16, 0.35, "nebula_dead"),  # burnt rust, not grey. 304 real provinces; impassables have their OWN material now, see below.
 "wetlands":        ("Anomaly Fields",     "#3fbfb0", 1, 350, 0.70, 0.54, 0.60, "lens"),
 "farmlands":       ("Fertile Reach",      "#ffc861", 0, 450, 0.65, 1.00, 0.90, "none"),
 "floodplains":     ("Volatile Cluster",   "#e08a45", 2, 400, 0.70, 0.78, 0.85, "flare"),
 "oasis":           ("Sanctuary Systems",  "#fff2e4", 1, 500, 0.55, 1.00, 0.95, "none"),  # near-white cream: the brightest thing on the map, a visible sanctuary
 "terraced_hills":  ("Layered Cluster",    "#5d7f8a", 2, 300, 0.75, 0.78, 0.55, "strata"),  # muted slate-teal; the earlier olive green won the distinctness metric but was the one earth colour on a violet/teal/gold map
 # Impassable wastelands, split out of desert_mountains 2026-09-27. They had shared that
 # material, which was wrong in both directions: the two sets are completely DISJOINT - 1188
 # impassable provinces, 304 provinces whose province_terrain is actually desert_mountains, and
 # zero in both - so every star tuned for one was being applied to the other. Lowering
 # desert_mountains to quiet the wastelands would have emptied 304 real Barren Barriers instead.
 # This is a VISUAL material only. province_terrain still says whatever it said, so nothing about
 # gameplay, movement or loc changes; only what the 1188 impassable provinces are painted with.
 # Every field EXCEPT the two star fields is byte-identical to desert_mountains above, and that
 # is the point: the request was "fewer stars on impassable mountains", not a recolour. This
 # surface is 21.4% of the map - the largest single terrain on it, where real desert_mountains is
 # 1.0% - so any tint change here repaints a fifth of the world. A near-black violet was tried and
 # rejected for exactly that reason, as were six darkened rusts, none of which cleared the
 # distinctness gate against desert_mountains anyway (best was dE 12.5, threshold 14.0).
 # star_density 0.16 -> 0.06 is the whole change: the lowest on the map by a wide margin, because
 # a wall you can never enter should not be dotted with systems to look at. star_bright 0.35 ->
 # 0.30 so the few that remain do not compensate by shouting.
 # The identical tint is declared to check_terrain_distinctness.py as an INTENDED_TWIN.
 "impassable":      ("Impassable Barrier", "#6b3a32", 0, 220, 0.90, 0.06, 0.30, "nebula_dead"),
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
    def sprof(e, field, fallback):
        k = e[0].replace("eotg_", "").rsplit("_01", 1)[0]
        return STAR_PROFILE.get(k, {}).get(field, STAR_PROFILE_DEFAULT.get(field, fallback))
    # size falls back to the terrain's own density: that is what drove size before this split,
    # so terrains left out of STAR_PROFILE keep their previous mean exactly.
    # 1 for the coastal edge materials. A star whose ANCHOR sits in the coastal band would
    # have its seaward half clipped by the shoreline - stars are drawn by the terrain pass
    # only, and the water shader covers whatever crosses the waterline. Rejecting at the
    # anchor is free: EotgStarParamsAt already samples the index there.
    arr("EOTG_IS_EDGE", "float",
        [f"{1.0 if e[0] in ('eotg_edge_01', 'eotg_edge_02') else 0.0:.1f}f" for e in entries])
    arr("EOTG_STAR_SIZE", "float", [f"{sprof(e, 'size', e[5]):.2f}f" for e in entries])
    arr("EOTG_STAR_SIZE_SKEW", "float", [f"{sprof(e, 'ssk', 1.0):.2f}f" for e in entries])
    arr("EOTG_STAR_BRIGHT_SKEW", "float", [f"{sprof(e, 'bsk', 1.0):.2f}f" for e in entries])
    arr("EOTG_TILEBREAK", "float", [
        f"{TILEBREAK.get(e[0].replace('eotg_', '').rsplit('_01', 1)[0], 0.0):.3f}f" for e in entries])
    arr("EOTG_SHADE", "float", [
        f"{SHADE.get(e[0].replace('eotg_', '').rsplit('_01', 1)[0], 0.0):.3f}f" for e in entries])
    arr("EOTG_ALT_TINT", "float3", [
        (lambda c: f"float3( {c[0]:.3f}f, {c[1]:.3f}f, {c[2]:.3f}f )")(
            tint_rgb(alt(e)[0]) if alt(e)[0] else (0.0, 0.0, 0.0)) for e in entries])
    arr("EOTG_ALT_BAND", "float3", [
        (lambda v: f"float3( {v[0]:.3f}f, {v[1]:.3f}f, {v[2]:.3f}f )")(alt(e)[1]) for e in entries])
    def fx2(e):
        """Secondary effect for this entry, already weakened, or 'none'."""
        key = e[0].replace("eotg_", "").rsplit("_01", 1)[0]
        name = FX2.get(key)
        if not name:
            return FX["none"]
        base = FX[name]
        if base["kind"] == fx(e)["kind"]:
            raise SystemExit(
                f"FX2['{key}'] = '{name}' has the same kind as its primary; they share a slot")
        d = dict(base)
        d["gain"] = base["gain"] * FX2_GAIN_CAP
        d["dark"] = 1.0 - (1.0 - base["dark"]) * (1.0 - FX2_DARK_BLEND)
        return d

    def arr2(name, typ, val):
        """Emit a 2N array: primaries, then secondaries."""
        vals = [val(fx(e)) for e in entries] + [val(fx2(e)) for e in entries]
        F.append(f"\t\tstatic const {typ} {name}[{2 * n}] = {{")
        F.append("\t\t\t" + ", ".join(vals))
        F.append("\t\t};")

    def c3(c):
        return f"float3( {c[0]:.3f}f, {c[1]:.3f}f, {c[2]:.3f}f )"
    arr2("EOTG_FX_KIND", "int", lambda f: f"{f['kind']}")
    arr2("EOTG_FX_COLOR", "float3", lambda f: c3(hx(f["color"]) if f["color"] else (0.0, 0.0, 0.0)))
    arr2("EOTG_FX_USETINT", "float", lambda f: f"{0.0 if f['color'] else 1.0:.1f}f")
    arr2("EOTG_FX_GAIN", "float", lambda f: f"{f['gain']:.3f}f")
    arr2("EOTG_FX_DARK", "float", lambda f: f"{f['dark']:.3f}f")
    arr2("EOTG_FX_SCALE", "float", lambda f: f"{f['scale']:.5f}f")
    arr2("EOTG_FX_P", "float4", lambda f: f4(f["p"]))
    arr2("EOTG_FX_Q", "float4", lambda f: f4(f["q"]))
    arr2("EOTG_FX_SLOPE", "float3", lambda f: c3(f.get("slope", (0, 0, 0))))
    arr2("EOTG_FX_HEIGHT", "float3", lambda f: c3(f["height"]))
    n_fx2 = sum(1 for e in entries if fx2(e)["kind"])
    print(f"secondary effects: {n_fx2} of {n} entries carry one")
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
