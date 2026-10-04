# MOD(eotg) Stellar Rivers - full-file override of game/gfx/FX/river_surface.shader (CK3 1.19.0.6)
# Rivers are drawn as self-illuminated "stellar wind" energy lanes instead of water:
#   - a custom vertex shader widens the river ribbon so there is room for a soft glow halo
#   - additive blending so the lane adds light to the terrain instead of painting a strip on it
#   - pixel shader: gaussian halo + thin bright core + wandering filaments + fast sparse wisps
# Constant buffer (_FlowNormalSpeed etc.) and samplers come from the vanilla includes.
# Tunables are the EOTG_* defines (colour/shape in PS_surface, width in VS_eotg) plus gfx/map/rivers/rivers.settings.

Includes = {
	"jomini/jomini_river_surface.fxh"
	"jomini/jomini_fog_of_war.fxh"
	"standardfuncsgfx.fxh"
	"cw/pdxterrain.fxh"
	"shadow_tint.fxh"
	"clouds.fxh"
}

VertexShader =
{
	MainCode VS_eotg
	{
		Input = "VS_INPUT_RIVER"
		Output = "VS_OUTPUT_RIVER"
		Code
		[[
			// MOD(eotg) how much wider than the water the glow ribbon is (1.0 = vanilla width)
			#define EOTG_WIDEN 2.5f

			PDX_MAIN
			{
				VS_OUTPUT_RIVER Out;

				float WidthWorld = Input.Width * max( MapSize.x, MapSize.y );

				// Tangent runs along the river, so cross( Normal, Tangent ) points bank-to-bank.
				// Push each vertex outward from the centre line (UV.y = 0.5) to widen the ribbon.
				float3 Across = normalize( cross( normalize( Input.Normal ), normalize( Input.Tangent ) ) );
				float3 Pos = Input.Position + Across * ( Input.UV.y - 0.5f ) * WidthWorld * ( EOTG_WIDEN - 1.0f );

				Out.UV             = Input.UV;
				Out.Tangent        = Input.Tangent;
				Out.Normal         = Input.Normal;
				Out.WorldSpacePos  = Pos;
				Out.Transparency   = Input.Transparency;
				Out.Width          = WidthWorld;
				Out.DistanceToMain = Input.DistanceToMain;

				Out.Position = FixProjectionAndMul( ViewProjectionMatrix, float4( Pos, 1.0f ) );
				return Out;
			}
		]]
	}
}

PixelShader =
{
	TextureSampler FogOfWarAlpha
	{
		Ref = JominiFogOfWar
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
	}

	MainCode PS_surface
	{
		Input = "VS_OUTPUT_RIVER"
		Output = "PDX_COLOR"
		Code
		[[
			// MOD(eotg) ---- tunables -------------------------------------------------
			#define EOTG_PALETTE           3      // 0 = gold, 1 = purple, 2 = cosine-palette colour mix, 3 = ramp texture (gfx/map/rivers/eotg_lane_ramp.dds)
			#if EOTG_PALETTE == 1
				#define EOTG_COLOR_HALO    float3( 0.45f, 0.10f, 0.90f )  // wide soft glow
				#define EOTG_COLOR_CORE    float3( 0.95f, 0.75f, 1.00f )  // centre line / filaments
			#else
				#define EOTG_COLOR_HALO    float3( 1.00f, 0.55f, 0.08f )  // wide soft glow
				#define EOTG_COLOR_CORE    float3( 1.00f, 0.95f, 0.70f )  // centre line / filaments
			#endif
			// Cosine palette (Inigo Quilez): colour(t) = A + B * cos( 2pi * ( C * t + D ) ), t in 0..1.
			// A = brightness, B = contrast, C = how many times the colours cycle, D = per-channel phase (which colours).
			// Defaults sweep gold -> magenta -> violet -> blue over t = 0 .. 0.6.
			#define EOTG_PAL_A             float3( 0.60f, 0.40f, 0.60f )
			#define EOTG_PAL_B             float3( 0.40f, 0.40f, 0.40f )
			#define EOTG_PAL_C             float3( 1.00f, 1.00f, 1.00f )
			#define EOTG_PAL_D             float3( 0.00f, 0.15f, 0.55f )
			#define EOTG_HUE_BASE          0.00f  // where on the palette the lane sits on average
			#define EOTG_HUE_SPREAD        0.45f  // how far the hue wanders from the base (0 = single colour)
			#define EOTG_HUE_REGION_SCALE  0.0006f// how quickly the hue changes across the map (smaller = larger regions of one colour)
			#define EOTG_HUE_DRIFT_SPEED   0.02f  // slow hue drift over time
			#define EOTG_HUE_FILAMENT_STEP 0.12f  // hue offset between successive filaments
			#define EOTG_HUE_WISP_OFFSET   0.30f  // wisps sit this far along the palette from the halo
			#define EOTG_INTENSITY         1.0f   // overall brightness (additive, so 1.0 is already strong)
			#define EOTG_HALO_TIGHTNESS    3.0f   // higher = halo hugs the centre more (gaussian falloff)
			#define EOTG_CORE_TIGHTNESS    45.0f  // higher = thinner centre line
			#define EOTG_ALONG_SCALE       1.0f   // multiplier on the along-river coordinate; if streaks are microscopic try 0.1, if giant try 10
			#define EOTG_FLOW_SPEED        30.0f  // how fast streaks travel downstream (units of along-scale per second)
			#define EOTG_FILAMENT_LENGTH   60.0f  // length of one filament "comet" segment
			#define EOTG_FILAMENT_WIDTH    120.0f // higher = thinner filaments
			#define EOTG_WISP_LENGTH       25.0f  // length of the fast sparse wisps
			#define EOTG_KEEP_WHEN_ZOOMED_OUT 0   // 1 = ignore vanilla's zoom-out fade so lanes stay visible at strategic zoom
			// -------------------------------------------------------------------------

			float EotgGauss( float d, float k )
			{
				return exp( -d * d * k );
			}

			float3 EotgPalette( float t )
			{
				#if EOTG_PALETTE == 3
					// 256x1 ramp, left = 0, right = 1; frac() wraps so the slow hue drift never pins at the edge
					// (the ramp starts and ends on the same colour so the wrap is seamless).
					return PdxTex2DLod0( FoamRampTexture, float2( frac( t ), 0.5f ) ).rgb;
				#else
					return EOTG_PAL_A + EOTG_PAL_B * cos( 6.28318f * ( EOTG_PAL_C * t + EOTG_PAL_D ) );
				#endif
			}

			// Halo / core colours for a given hue parameter. In fixed-palette modes the hue is ignored.
			float3 EotgHaloColor( float hue )
			{
				#if EOTG_PALETTE >= 2
					return EotgPalette( hue );
				#else
					return EOTG_COLOR_HALO;
				#endif
			}
			float3 EotgCoreColor( float hue )
			{
				#if EOTG_PALETTE >= 2
					return lerp( EotgPalette( hue + 0.05f ), float3( 1.0f, 1.0f, 1.0f ), 0.55f );	// palette colour pushed toward white-hot
				#else
					return EOTG_COLOR_CORE;
				#endif
			}

			// One wandering filament: a thin bright line that snakes across the lane and is lit in
			// comet-like segments that travel downstream.
			float EotgFilament( float along, float across, float t, float freq, float amp, float speed, float phase, float seg )
			{
				float centre = 0.5f + amp * sin( along * freq + t * speed * 0.15f + phase );
				float d = ( across - centre ) * 2.0f;
				float lineMask = EotgGauss( d, EOTG_FILAMENT_WIDTH );

				// Segment mask scrolling downstream; pow makes segments sparse with bright heads
				float2 uv = float2( ( along - t * speed ) / EOTG_FILAMENT_LENGTH, phase );
				float segMask = PdxTex2D( FoamNoiseTexture, uv ).r;
				segMask = pow( saturate( segMask * 1.3f ), 3.0f );

				return lineMask * segMask * seg;
			}

			PDX_MAIN
			{
				// Vanilla zoom / flat-map gating
				float ZoomBlendOut = clamp( ( 1.0f - _WaterZoomedInZoomedOutFactor ) * 2.0f, 0.0f, 1.0f );
				#if EOTG_KEEP_WHEN_ZOOMED_OUT == 1
					ZoomBlendOut = 1.0f;
				#endif
				clip( ZoomBlendOut - 1e-5 );

				// Ribbon coordinates: UV.x runs along the river, UV.y runs 0..1 across the (widened) ribbon.
				float t      = GlobalTime * EOTG_FLOW_SPEED;
				float along  = Input.UV.x * EOTG_ALONG_SCALE;
				float across = Input.UV.y;
				float d      = abs( across - 0.5f ) * 2.0f;   // 0 at centre line, 1 at the outer glow edge

				// --- Shape --------------------------------------------------------------
				float halo = EotgGauss( d, EOTG_HALO_TIGHTNESS );
				float core = EotgGauss( d, EOTG_CORE_TIGHTNESS );

				// Slow turbulence breathing through the halo so it is not a flat gradient
				float2 turbUV = float2( ( along - t * 0.4f ) / 90.0f, across * 0.6f + Input.WorldSpacePos.x * 0.001f );
				float turb = PdxTex2D( FoamNoiseTexture, turbUV ).r;
				halo *= 0.6f + 0.8f * turb;

				// --- Hue: slow world-space noise (regions of colour) + gentle downstream drift + time drift
				float regionNoise = PdxTex2D( FoamNoiseTexture, Input.WorldSpacePos.xz * EOTG_HUE_REGION_SCALE ).r;
				float hue = EOTG_HUE_BASE
				          + EOTG_HUE_SPREAD * ( regionNoise * 0.7f + 0.3f * ( 0.5f + 0.5f * sin( along * 0.004f ) ) )
				          + GlobalTime * EOTG_HUE_DRIFT_SPEED;
				float3 haloCol = EotgHaloColor( hue );
				float3 coreCol = EotgCoreColor( hue );

				// --- Filaments: three snaking lines with comet segments, each a step further along the palette --
				float3 filRGB = float3( 0.0f, 0.0f, 0.0f );
				filRGB += EotgCoreColor( hue + EOTG_HUE_FILAMENT_STEP * 1.0f ) * EotgFilament( along, across, t, 0.020f, 0.22f, 1.00f, 0.10f, 1.0f );
				filRGB += EotgCoreColor( hue + EOTG_HUE_FILAMENT_STEP * 2.0f ) * EotgFilament( along, across, t, 0.031f, 0.16f, 1.35f, 0.55f, 0.8f );
				filRGB += EotgCoreColor( hue - EOTG_HUE_FILAMENT_STEP * 1.0f ) * EotgFilament( along, across, t, 0.013f, 0.28f, 0.75f, 0.83f, 0.7f );

				// --- Wisps: fast, sparse, stretched streaks over the whole lane, in a contrasting hue --
				float2 wispUV = float2( ( along - t * 2.2f ) / EOTG_WISP_LENGTH, across * 3.0f );
				float wisp = PdxTex2D( FoamNoiseTexture, wispUV ).r;
				wisp = smoothstep( 0.62f, 0.95f, wisp ) * halo;
				float3 wispCol = lerp( EotgHaloColor( hue + EOTG_HUE_WISP_OFFSET ), coreCol, 0.4f );

				// Subtle flicker
				float flicker = 0.92f + 0.08f * PdxTex2D( FoamNoiseTexture, float2( GlobalTime * 0.7f, along * 0.002f ) ).r;

				// --- Compose (additive, so these are light contributions, not a fill colour) --
				float3 rgb = haloCol * halo * 0.45f;
				rgb += coreCol * core * 0.9f;
				rgb += filRGB * 1.6f;
				rgb += wispCol * wisp * 1.1f;
				rgb *= flicker * EOTG_INTENSITY;

				// --- Alpha: guarantee a soft outer edge, tributary junction fade, coast fade, vanilla fades --
				float alpha = smoothstep( 1.0f, 0.85f, d );
				alpha *= Input.Transparency;
				alpha *= saturate( ( Input.DistanceToMain - 0.1f ) * 5.0f );

				alpha *= ( 1.0f - FlatMapLerp ) * ZoomBlendOut;
				clip( alpha - 1e-5 );

				// Energy is self-lit: no cloud/terrain shadow darkening, but keep fog of war and distance fog
				float3 Color = ApplyFogOfWar( rgb, Input.WorldSpacePos, FogOfWarAlpha );
				Color = ApplyMapDistanceFogWithoutFoW( Color, Input.WorldSpacePos );

				return float4( Color, alpha );
			}
		]]
	}
}

# MOD(eotg) additive: source * alpha is added on top of whatever is already on screen
BlendState EotgAdditive
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "ONE"
	WriteMask = "RED|GREEN|BLUE"
}

Effect river_surface
{
	VertexShader = "VS_eotg"
	PixelShader = "PS_surface"
	BlendState = "EotgAdditive"
	Defines = { "RIVER" }
}
