# MOD(eotg) Void Ocean - full-file override of game/gfx/FX/pdxwater.shader (CK3 1.19.0.6)
# The sea is deep space: a near-black plane with slow nebula drift and faint stars. The coastline is an
# energy shore: a glowing rim where the void meets land, with bands of light rolling toward the coast,
# coloured through the same ramp (gfx/map/rivers/eotg_lane_ramp.dds) as the stellar-river lanes.
# Shore effects are driven by distance to land, measured by sampling the heightmap on rings around the
# pixel (the seabed depth is unreliable: continental shelves sit just under the water plane). Vertex shaders, samplers, map-mode colour overlay, fog of war,
# distance fog and the flat-map blend are kept from vanilla; only the colour composition is new.
# Tunables are the EOTG_* defines in EotgVoidWater below.

Includes = {
	"cw/heightmap.fxh"
	"cw/camera.fxh"		# MOD(eotg) CameraPosition, for the zoom fade below
	"bordercolor.fxh"
	"jomini/jomini_water_default.fxh"
	"jomini/jomini_water_pdxmesh.fxh"
	"jomini/jomini_water.fxh"
	"jomini/jomini_fog_of_war.fxh"
	"jomini/jomini_mapobject.fxh"
	"standardfuncsgfx.fxh"
	"paper_transition.fxh"
	"clouds.fxh"
	"utility_game.fxh"
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
	TextureSampler FlatMapTexture
	{
		Ref = TerrainFlatMap
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}

	Code
	[[
		// MOD(eotg) ---- tunables -------------------------------------------------
		// Master switch for everything drawn ON the void: stars and nebula clouds. Off.
		//
		// Three passes of fading these by camera distance and then by FlatMapLerp all failed the
		// same way, because the problem was never when they appear - it was that they are a NOISE
		// TEXTURE in world space. Zoomed in, a 'star' magnifies into a soft blob tens of pixels
		// across; zoomed out, the nebula reads as pink and cyan smears in open water. Neither is a
		// star field, and no fade curve turns one into the other.
		//
		// The ocean is now flat void. The land keeps its stars - those are drawn per-star in
		// pdxterrain.shader, at a real world size, which is why they hold up at every zoom.
		// Set to 1 to bring the field back; nothing else needs changing.
		#define EOTG_VOID_STARS          0

		#define EOTG_VOID_COLOR          float3( 0.002f, 0.002f, 0.003f )  // open-sea base: black
		#define EOTG_NEBULA_STRENGTH     0.012f    // brightness of the slow nebula drift over the void (0 = flat black)
		#define EOTG_NEBULA_SCALE        0.0008f  // world -> noise scale for the nebula (smaller = bigger clouds)
		#define EOTG_STAR_DENSITY        0.990f   // noise threshold for stars; higher = fewer stars (0.97 dense, 0.995 sparse)
		#define EOTG_STAR_STRENGTH       0.35f    // brightness of stars
		#define EOTG_STAR_SCALE          0.9f     // world -> noise scale for stars (higher = smaller/more)

		// Shore distances are in world units (map pixels) measured by sampling the heightmap on rings and
		// checking for land, so they do not depend on how deep the seabed is or on the engine height scale.
		#define EOTG_SHORE_RIM_RADIUS    2.6f     // world units: bright rim reaches this far from the waterline
		#define EOTG_SHORE_RIM_STRENGTH  0.30f     // brightness of the rim (spread over a wider band, so slightly dimmer to keep the same visual weight)
		#define EOTG_SHORE_GLOW_RADIUS   7.0f     // world units the soft glow reaches seaward
		#define EOTG_SHORE_GLOW_STRENGTH 0.07f    // brightness of the soft glow
		#define EOTG_BAND_RADIUS         5.0f    // world units the rolling bands reach seaward
		#define EOTG_BAND_COUNT          3.0f     // bands across that reach
		#define EOTG_BAND_SPEED          0.15f    // how fast bands roll toward the shore
		#define EOTG_BAND_STRENGTH       0.10f    // brightness of the bands
		#define EOTG_SHALLOW_TURB        0.10f    // turbulence/wisp strength near the coast

		#define EOTG_HUE_BASE            0.00f    // same hue scheme as the river lanes so the two match
		#define EOTG_HUE_SPREAD          0.28f   // narrower span of the ramp: coasts were banding into a rainbow
		#define EOTG_HUE_REGION_SCALE    0.00018f// ~3x larger regions, so hue changes over distance rather than along one coast
		#define EOTG_HUE_DRIFT_SPEED     0.02f
		#define EOTG_HUE_BAND_OFFSET     0.08f    // bands sit this far along the ramp from the rim

		// Zoomed out, the stars and the nebula drift in the void are just noise: too small to read
		// as anything and small enough to alias. Past FAR the void is a flat black plane with only
		// the shore rim left, which is the part that carries information at that range.
		#define EOTG_VOID_DETAIL_FAR    520.0f
		#define EOTG_VOID_DETAIL_RANGE  260.0f
		// The shore has to go too, and for a different reason. Its land test samples the heightmap
		// on rings a few world units across; zoomed out those rings are far below a pixel and the
		// heightmap is being read from a reduced mip, so the land fraction smears and the rim turns
		// into big soft blobs around island groups instead of a coastline. It survives longer than
		// the stars because it still reads as a coast at middle zoom, but by the strategic view the
		// flatmap is drawing the coastlines anyway.
		// Calibrated from a screenshot: at full zoom-out the stars (gone by 520) had disappeared
		// while the shore (gone by 900) had not, so the camera sits between those two distances
		// there. Matching the star threshold is therefore the one value guaranteed to clear it.
		#define EOTG_SHORE_FADE_FAR     520.0f
		#define EOTG_SHORE_FADE_RANGE   300.0f
		// -------------------------------------------------------------------------

		float3 EotgRamp( float t )
		{
			return PdxTex2DLod0( FoamRampTexture, float2( frac( t ), 0.5f ) ).rgb;
		}

		float EotgHue( float3 WorldSpacePos )
		{
			float regionNoise = PdxTex2D( FoamNoiseTexture, WorldSpacePos.xz * EOTG_HUE_REGION_SCALE ).r;
			return EOTG_HUE_BASE + EOTG_HUE_SPREAD * regionNoise + GlobalTime * EOTG_HUE_DRIFT_SPEED;
		}

		// Depth: distance from the water plane down to the terrain, as vanilla computes it. 0 at the waterline.
		float EotgDepth( float3 WorldSpacePos )
		{
			float2 HeightmapCoordinate = WorldSpacePos.xz;
			#ifdef JOMINIWATER_BORDER_LERP
				HeightmapCoordinate.x -= JOMINIWATER_MapSize.x;
			#endif
			return WorldSpacePos.y - GetHeightMultisample( HeightmapCoordinate, 0.65f );
		}

		float3 EotgVoid( float3 WorldSpacePos, float hue, float detail )
		{
			if ( detail < 0.01f )
			{
				return EOTG_VOID_COLOR;
			}
			// Faint nebula: a large slow layer tinted from the ramp, a smaller neutral dust layer
			float2 p = WorldSpacePos.xz * EOTG_NEBULA_SCALE;
			float n1 = PdxTex2D( FoamNoiseTexture, p + GlobalTime * float2( 0.0015f, 0.0007f ) ).r;
			float n2 = PdxTex2D( FoamNoiseTexture, p * 2.3f + 0.41f - GlobalTime * float2( 0.0009f, 0.0012f ) ).r;
			float big = PdxTex2D( FoamNoiseTexture, p * 0.35f + 0.77f + GlobalTime * float2( -0.0004f, 0.0006f ) ).g;
			float dust = saturate( n1 * n2 * 2.2f - 0.25f );
			float cloud = smoothstep( 0.45f, 0.85f, big ) * ( 0.5f + 0.5f * n1 );
			float3 dustCol  = float3( 0.4f, 0.4f, 0.45f );
			float3 cloudCol = EotgRamp( hue + 0.35f + big * 0.3f );

			// Stars: many faint white points plus a few brighter ramp-tinted ones, twinkling slowly
			float s  = PdxTex2D( FoamNoiseTexture, WorldSpacePos.xz * EOTG_STAR_SCALE ).g;
			float s2 = PdxTex2D( FoamNoiseTexture, WorldSpacePos.xz * EOTG_STAR_SCALE * 0.43f + 0.19f ).r;
			float twinkle = 0.6f + 0.4f * PdxTex2D( FoamNoiseTexture, WorldSpacePos.xz * 0.05f + GlobalTime * 0.03f ).b;
			float star    = smoothstep( EOTG_STAR_DENSITY, 1.0f, s ) * twinkle;
			float bright  = smoothstep( EOTG_STAR_DENSITY + 0.006f, 1.0f, s2 ) * ( 0.5f + 0.5f * twinkle );
			float3 brightCol = lerp( EotgRamp( hue + s2 ), float3( 1.0f, 1.0f, 1.0f ), 0.4f );

			return EOTG_VOID_COLOR
			     + ( dustCol  * dust  * EOTG_NEBULA_STRENGTH
			       + cloudCol * cloud * EOTG_NEBULA_STRENGTH * 3.0f
			       + float3( 1.0f, 0.94f, 0.80f ) * star * EOTG_STAR_STRENGTH
			       + brightCol * bright * EOTG_STAR_STRENGTH * 2.5f ) * detail;
		}

		#define EOTG_RING_TAPS 12			// 8 taps quantised each ring into 1/8ths, which showed as scalloping along straight
											// coasts. 12 + the per-pixel jitter below beats 16 without it, at 3/4 of the cost:
											// every tap here is a multisampled height fetch and there are three rings per pixel.
		#define EOTG_COAST_SOFTNESS 0.060f	// in 0..1 heightmap units; wider = softer, smoother shore edges (beach slopes span ~0.02-0.05)

		// Soft "is this land" for one heightmap sample: 0 well below water, 1 well above, smooth across
		// the beach slope. WaterY is the LOCAL water surface: identical to _WaterHeight for the ocean
		// plane, but lake meshes sit at their own elevation, and using the global sea level there made
		// every sample read as land (solid bright rim over the whole lake).
		float EotgLandAt( float2 xz, float WaterY )
		{
			float h01 = GetHeightMultisample01( xz, 1.0f );	// multisampled: point sampling quantised
														// the shore to heightmap texels (blocky stair-steps)
			float w01 = WaterY / HeightScale;
			return smoothstep( w01 - EOTG_COAST_SOFTNESS, w01 + EOTG_COAST_SOFTNESS, h01 );
		}

		// Average land-ness on a ring: for a straight coast at distance d < r this is ~acos(d/r)/pi,
		// 0 at d = r rising smoothly to 0.5 at the waterline, so it doubles as a continuous
		// distance-to-coast proxy inside the ring. 0 in open sea. Taps are soft so the result
		// varies continuously as the pixel moves instead of stepping in 1/8ths.
		float EotgLandFraction( float2 xz, float radius, float WaterY )
		{
			float n = 0.0f;
			float angleStep = 6.2831853f / float( EOTG_RING_TAPS );
			// One extra fetch for the whole ring: rotate each pixel's tap pattern by up to a full step, so the
			// 1/12th quantisation is dithered across neighbouring pixels instead of landing in the same place on
			// each of them. Scalloping becomes fine noise, which at this scale reads as blur. Much cheaper than
			// buying the same smoothness with more taps.
			float jitter = PdxTex2D( FoamNoiseTexture, xz * 0.37f ).r * angleStep;
			for ( int i = 0; i < EOTG_RING_TAPS; i++ )
			{
				float a = angleStep * float( i ) + radius * 0.37f + jitter;	// rotate rings relative to each other so their taps do not line up
				float2 o = float2( cos( a ), sin( a ) ) * radius;
				n += EotgLandAt( xz + o, WaterY );
			}
			return n / float( EOTG_RING_TAPS );
		}

		float3 EotgShore( float3 WorldSpacePos, float hue )
		{
			float3 rimCol  = lerp( EotgRamp( hue ), float3( 1.0f, 1.0f, 1.0f ), 0.5f );
			float3 bandCol = EotgRamp( hue + EOTG_HUE_BAND_OFFSET );
			float3 glowCol = EotgRamp( hue );

			// Three rings: fine (rim), medium (glow), wide (bands). Each fraction is 0 beyond its radius.
			float fRim  = EotgLandFraction( WorldSpacePos.xz, EOTG_SHORE_RIM_RADIUS, WorldSpacePos.y );
			float fGlow = EotgLandFraction( WorldSpacePos.xz, EOTG_SHORE_GLOW_RADIUS, WorldSpacePos.y );
			float fBand = EotgLandFraction( WorldSpacePos.xz, EOTG_BAND_RADIUS, WorldSpacePos.y );

			// Bright rim hugging the waterline, soft glow reaching seaward
			float rim  = saturate( fRim * 2.0f );
			rim = rim * rim * ( 3.0f - 2.0f * rim );	// smooth ease so the rim edge has no visible onset
			float glow = saturate( fGlow * 2.0f );

			// Bands rolling toward the shore: sharp leading edge, soft tail, using the wide-ring fraction
			// as the along-shore coordinate (grows toward land, so + time moves the bands shoreward)
			float shoreCoord = saturate( fBand * 2.0f );	// 0 at EOTG_BAND_RADIUS, 1 at the waterline
			float phase = frac( shoreCoord * EOTG_BAND_COUNT - GlobalTime * EOTG_BAND_SPEED );
			float band  = max( smoothstep( 0.80f, 1.0f, phase ), smoothstep( 0.10f, 0.80f, phase ) * 0.35f );
			band *= smoothstep( 0.0f, 0.35f, shoreCoord );
			// Break bands up along the coast so they are not a uniform ring
			float bandMask = PdxTex2D( FoamNoiseTexture, WorldSpacePos.xz * 0.006f + GlobalTime * float2( 0.0012f, -0.0009f ) ).r;
			band *= smoothstep( 0.25f, 0.75f, bandMask );

			// Turbulence: fast fine wisps near the coast
			float2 tuv = WorldSpacePos.xz * 0.03f + GlobalTime * float2( 0.05f, -0.04f );
			float turb = PdxTex2D( FoamNoiseTexture, tuv ).r * PdxTex2D( FoamNoiseTexture, tuv * 2.7f - GlobalTime * 0.02f ).g;
			turb = smoothstep( 0.18f, 0.6f, turb ) * glow * EOTG_SHALLOW_TURB;

			return rimCol * rim * EOTG_SHORE_RIM_STRENGTH
			     + glowCol * glow * EOTG_SHORE_GLOW_STRENGTH
			     + bandCol * band * EOTG_BAND_STRENGTH
			     + glowCol * turb;
		}

		// Full void-water colour and alpha for one pixel
		float4 EotgVoidWater( float3 WorldSpacePos )
		{
			float Depth = EotgDepth( WorldSpacePos );
			float hue = EotgHue( WorldSpacePos );

			float camDist = length( CameraPosition - WorldSpacePos );
			#if EOTG_VOID_STARS
				float detail = saturate( ( EOTG_VOID_DETAIL_FAR - camDist ) / EOTG_VOID_DETAIL_RANGE );
			#else
				float detail = 0.0f;
			#endif
			float shoreFade = saturate( ( EOTG_SHORE_FADE_FAR - camDist ) / EOTG_SHORE_FADE_RANGE );

			// Kill both outright once the paper map starts coming in. Distance alone was not enough:
			// camDist is measured per pixel, so with a tilted camera the near edge of the ocean stays
			// close even at full zoom out, and stars and nebulae went on twinkling under the
			// political map. FlatMapLerp is the engine's own 'the paper map is showing' signal and
			// does not depend on where the camera happens to be pointing.
			float flatLerp = saturate( FlatMapLerp );
			detail    *= 1.0f - flatLerp;
			shoreFade *= 1.0f - flatLerp;

			float3 Color = EotgVoid( WorldSpacePos, hue, detail );
			if ( shoreFade > 0.01f )
			{
				Color += EotgShore( WorldSpacePos, hue ) * shoreFade;
			}

			// Fade onto the beach exactly as vanilla does, using its shore-mask settings
			float WaterFade = 1.0f - saturate( ( _WaterFadeShoreMaskDepth - Depth ) * _WaterFadeShoreMaskSharpness );
			return float4( Color, WaterFade );
		}
	]]

	MainCode PixelShader
	{
		Input = "VS_OUTPUT_WATER"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float4 Water = EotgVoidWater( Input.WorldSpacePos );

				#ifdef WATER_COLOR_OVERLAY
					// Not enough texture slots, so use only secondary colors on water.
					#if defined( PDX_OSX ) && defined( PDX_OPENGL )
						ApplySecondaryColorGame( Water.rgb, float2( Input.UV01.x, 1.0f - Input.UV01.y ) );
					#else
						float3 BorderColor;
						float BorderPreLightingBlend;
						float BorderPostLightingBlend;
						GetProvinceOverlayAndBlend( Input.WorldSpacePos.xz, BorderColor, BorderPreLightingBlend, BorderPostLightingBlend );
						GetBorderColorAndBlendGame( Input.WorldSpacePos.xz, Water.rgb, BorderColor, BorderPreLightingBlend, BorderPostLightingBlend );

						// Don't draw too close to the shore to not duplicate the colors with stripes over the land.
						float AccurateHeight = GetHeight( Input.WorldSpacePos.xz );
						BorderPreLightingBlend *= 1.0f - Levels( max( AccurateHeight - ( _WaterHeight - 0.05f ), 0.0f ), 0.0f, 0.05f );

						Water.rgb = lerp( Water.rgb, BorderColor, BorderPreLightingBlend );
					#endif
				#endif

				Water.rgb = ApplyFogOfWarMultiSampled( Water.rgb, Input.WorldSpacePos, FogOfWarAlpha );
				Water.rgb = ApplyMapDistanceFogWithoutFoW( Water.rgb, Input.WorldSpacePos );

				// MOD(eotg) no blend to the flat-map texture: the void stays live at strategic zoom
				return Water;
			}
		]]
	}

	MainCode PixelShaderLowSpec
	{
		Input = "VS_OUTPUT_WATER"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				// Same look; the void/shore functions are cheap enough for the low-spec path
				float4 Water = EotgVoidWater( Input.WorldSpacePos );

				#ifdef WATER_COLOR_OVERLAY
					ApplySecondaryColorGame( Water.rgb, float2( Input.UV01.x, 1.0f - Input.UV01.y ) );
				#endif

				Water.rgb = ApplyFogOfWarMultiSampled( Water.rgb, Input.WorldSpacePos, FogOfWarAlpha );
				Water.rgb = ApplyMapDistanceFogWithoutFoW( Water.rgb, Input.WorldSpacePos );


				return Water;
			}
		]]
	}
}


Effect water
{
	VertexShader = "JominiWaterVertexShader"
	PixelShader = "PixelShader"
}

Effect waterLowSpec
{
	VertexShader = "JominiWaterVertexShader"
	PixelShader = "PixelShaderLowSpec"
}

Effect lake
{
	VertexShader = "VS_jomini_water_mesh"
	PixelShader = "PixelShader"
}
Effect lake_mapobject
{
	VertexShader = "VS_jomini_water_mapobject"
	PixelShader = "PixelShader"
}
