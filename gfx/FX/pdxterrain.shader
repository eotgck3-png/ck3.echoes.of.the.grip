# MOD(eotg) override of game/gfx/FX/pdxterrain.shader (CK3 1.19.0.6).
# Hybrid terrain: shared greyscale structure textures, per-terrain colour and stars applied
# here from the material index. All additions marked MOD(eotg).

Includes = {
	"cw/pdxterrain.fxh"
	"eotg_terrain_params.fxh"
	"cw/heightmap.fxh"
	"cw/shadow.fxh"
	"cw/utility.fxh"
	"cw/camera.fxh"
	"cw/lighting_util.fxh"
	"cw/lighting.fxh"
	"jomini/jomini_fog.fxh"
	"jomini/map_lighting.fxh"
	"jomini/jomini_fog_of_war.fxh"
	"jomini/jomini_water.fxh"
	"standardfuncsgfx.fxh"
	"bordercolor.fxh"
	"lowspec.fxh"
	"legend.fxh"
	"dynamic_masks.fxh"
	"disease.fxh"
	"shadow_tint.fxh"
	"clouds.fxh"
	"province_effects.fxh"
	"paper_transition.fxh"
	"utility_game.fxh"
}

VertexStruct VS_OUTPUT_PDX_TERRAIN
{
	float4 Position			: PDX_POSITION;
	float3 WorldSpacePos	: TEXCOORD1;
	float4 ShadowProj		: TEXCOORD2;
};

VertexStruct VS_OUTPUT_PDX_TERRAIN_LOW_SPEC
{
	float4 Position			: PDX_POSITION;
	float3 WorldSpacePos	: TEXCOORD1;
	float4 ShadowProj		: TEXCOORD2;
	float3 DetailDiffuse	: TEXCOORD3;
	float4 DetailMaterial	: TEXCOORD4;
	float3 ColorMap			: TEXCOORD5;
	float3 FlatMap			: TEXCOORD6;
	float3 Normal			: TEXCOORD7;
};

# Limited JominiEnvironment data to get nicer transitions between the Flatmap lighting and Terrain lighting
# Only used in terrain shader while lerping between flatmap and terrain.
ConstantBuffer( FlatMapLerpEnvironment )
{
	float	FlatMapLerpCubemapIntensity;
	float3	FlatMapLerpSunDiffuse;
	float	FlatMapLerpSunIntensity;
	float4x4 FlatMapLerpCubemapYRotation;
};

VertexShader =
{
	TextureSampler DetailTextures
	{
		Ref = PdxTerrainTextures0
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
		type = "2darray"
	}
	TextureSampler NormalTextures
	{
		Ref = PdxTerrainTextures1
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
		type = "2darray"
	}
	TextureSampler MaterialTextures
	{
		Ref = PdxTerrainTextures2
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
		type = "2darray"
	}
	TextureSampler DetailIndexTexture
	{
		Ref = PdxTerrainTextures3
		MagFilter = "Point"
		MinFilter = "Point"
		MipFilter = "Point"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}
	TextureSampler DetailMaskTexture
	{
		Ref = PdxTerrainTextures4
		MagFilter = "Point"
		MinFilter = "Point"
		MipFilter = "Point"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
	}
	TextureSampler ColorTexture
	{
		Ref = PdxTerrainColorMap
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
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
		VS_OUTPUT_PDX_TERRAIN TerrainVertex( float2 WithinNodePos, float2 NodeOffset, float NodeScale, float2 LodDirection, float LodLerpFactor )
		{
			STerrainVertex Vertex = CalcTerrainVertex( WithinNodePos, NodeOffset, NodeScale, LodDirection, LodLerpFactor );

			#ifdef TERRAIN_FLAT_MAP_LERP
				Vertex.WorldSpacePos.y = lerp( Vertex.WorldSpacePos.y, FlatMapHeight, FlatMapLerp );
			#endif
			#ifdef TERRAIN_FLAT_MAP
				Vertex.WorldSpacePos.y = FlatMapHeight;
			#endif

			VS_OUTPUT_PDX_TERRAIN Out;
			Out.WorldSpacePos = Vertex.WorldSpacePos;

			Out.Position = FixProjectionAndMul( ViewProjectionMatrix, float4( Vertex.WorldSpacePos, 1.0 ) );
			Out.ShadowProj = mul( ShadowMapTextureMatrix, float4( Vertex.WorldSpacePos, 1.0 ) );

			return Out;
		}

		// Copies of the pixels shader CalcHeightBlendFactors and CalcDetailUV functions
		float4 CalcHeightBlendFactors( float4 MaterialHeights, float4 MaterialFactors, float BlendRange )
		{
			float4 Mat = MaterialHeights + MaterialFactors;
			float BlendStart = max( max( Mat.x, Mat.y ), max( Mat.z, Mat.w ) ) - BlendRange;

			float4 MatBlend = max( Mat - vec4( BlendStart ), vec4( 0.0 ) );

			float Epsilon = 0.00001;
			return float4( MatBlend ) / ( dot( MatBlend, vec4( 1.0 ) ) + Epsilon );
		}

		float2 CalcDetailUV( float2 WorldSpacePosXZ )
		{
			return (WorldSpacePosXZ + DetailTileOffset) * DetailTileFactor;
		}

		// A low spec vertex buffer version of CalculateDetails
		void CalculateDetailsLowSpec( float2 WorldSpacePosXZ, out float3 DetailDiffuse, out float4 DetailMaterial )
		{
			float2 DetailCoordinates = WorldSpacePosXZ * WorldSpaceToDetail;
			float2 DetailCoordinatesScaled = DetailCoordinates * DetailTextureSize;
			float2 DetailCoordinatesScaledFloored = floor( DetailCoordinatesScaled );
			float2 DetailCoordinatesFrac = DetailCoordinatesScaled - DetailCoordinatesScaledFloored;
			DetailCoordinates = DetailCoordinatesScaledFloored * DetailTexelSize + DetailTexelSize * 0.5;

			float4 Factors = float4(
				(1.0 - DetailCoordinatesFrac.x) * (1.0 - DetailCoordinatesFrac.y),
				DetailCoordinatesFrac.x * (1.0 - DetailCoordinatesFrac.y),
				(1.0 - DetailCoordinatesFrac.x) * DetailCoordinatesFrac.y,
				DetailCoordinatesFrac.x * DetailCoordinatesFrac.y
			);

			float4 DetailIndex = PdxTex2DLod0( DetailIndexTexture, DetailCoordinates ) * 255.0;
			float4 DetailMask = PdxTex2DLod0( DetailMaskTexture, DetailCoordinates ) * Factors[0];

			float2 Offsets[3];
			Offsets[0] = float2( DetailTexelSize.x, 0.0 );
			Offsets[1] = float2( 0.0, DetailTexelSize.y );
			Offsets[2] = float2( DetailTexelSize.x, DetailTexelSize.y );

			for ( int k = 0; k < 3; ++k )
			{
				float2 DetailCoordinates2 = DetailCoordinates + Offsets[k];

				float4 DetailIndices = PdxTex2DLod0( DetailIndexTexture, DetailCoordinates2 ) * 255.0;
				float4 DetailMasks = PdxTex2DLod0( DetailMaskTexture, DetailCoordinates2 ) * Factors[k+1];

				for ( int i = 0; i < 4; ++i )
				{
					for ( int j = 0; j < 4; ++j )
					{
						if ( DetailIndex[j] == DetailIndices[i] )
						{
							DetailMask[j] += DetailMasks[i];
						}
					}
				}
			}

			// We don't use different detail UVs per material like in the normal pdxterrain shader
			float2 DetailUV = CalcDetailUV( WorldSpacePosXZ );

			float4 DiffuseTexture0 = PdxTex2DLod0( DetailTextures, float3( DetailUV, DetailIndex[0] ) ) * smoothstep( 0.0, 0.1, DetailMask[0] );
			float4 DiffuseTexture1 = PdxTex2DLod0( DetailTextures, float3( DetailUV, DetailIndex[1] ) ) * smoothstep( 0.0, 0.1, DetailMask[1] );
			float4 DiffuseTexture2 = PdxTex2DLod0( DetailTextures, float3( DetailUV, DetailIndex[2] ) ) * smoothstep( 0.0, 0.1, DetailMask[2] );
			float4 DiffuseTexture3 = PdxTex2DLod0( DetailTextures, float3( DetailUV, DetailIndex[3] ) ) * smoothstep( 0.0, 0.1, DetailMask[3] );

			float4 BlendFactors = CalcHeightBlendFactors( float4( DiffuseTexture0.a, DiffuseTexture1.a, DiffuseTexture2.a, DiffuseTexture3.a ), DetailMask, DetailBlendRange );

			DetailDiffuse = DiffuseTexture0.rgb * BlendFactors[0] +
							DiffuseTexture1.rgb * BlendFactors[1] +
							DiffuseTexture2.rgb * BlendFactors[2] +
							DiffuseTexture3.rgb * BlendFactors[3];

			DetailMaterial = vec4( 0.0 );

			for ( int i = 0; i < 4; ++i )
			{
				float BlendFactor = BlendFactors[i];
				if ( BlendFactor > 0.0 )
				{
					float3 ArrayUV = float3( DetailUV, DetailIndex[i] );
					float4 NormalTexture = PdxTex2DLod0( NormalTextures, ArrayUV );
					float4 MaterialTexture = PdxTex2DLod0( MaterialTextures, ArrayUV );

					DetailMaterial += MaterialTexture * BlendFactor;
				}
			}
		}

		VS_OUTPUT_PDX_TERRAIN_LOW_SPEC TerrainVertexLowSpec( float2 WithinNodePos, float2 NodeOffset, float NodeScale, float2 LodDirection, float LodLerpFactor )
		{
			STerrainVertex Vertex = CalcTerrainVertex( WithinNodePos, NodeOffset, NodeScale, LodDirection, LodLerpFactor );

			#ifdef TERRAIN_FLAT_MAP_LERP
				Vertex.WorldSpacePos.y = lerp( Vertex.WorldSpacePos.y, FlatMapHeight, FlatMapLerp );
			#endif
			#ifdef TERRAIN_FLAT_MAP
				Vertex.WorldSpacePos.y = FlatMapHeight;
			#endif

			VS_OUTPUT_PDX_TERRAIN_LOW_SPEC Out;
			Out.WorldSpacePos = Vertex.WorldSpacePos;

			Out.Position = FixProjectionAndMul( ViewProjectionMatrix, float4( Vertex.WorldSpacePos, 1.0 ) );
			Out.ShadowProj = mul( ShadowMapTextureMatrix, float4( Vertex.WorldSpacePos, 1.0 ) );

			CalculateDetailsLowSpec( Vertex.WorldSpacePos.xz, Out.DetailDiffuse, Out.DetailMaterial );

			float2 ColorMapCoords = Vertex.WorldSpacePos.xz * WorldSpaceToTerrain0To1;

#if defined( PDX_OSX ) && defined( PDX_OPENGL )
			// We're limited to the amount of samplers we can bind at any given time on Mac, so instead
			// we disable the usage of ColorTexture (since its effects are very subtle) and assign a
			// default value here instead.
			Out.ColorMap = float3( vec3( 0.5 ) );
#else
			Out.ColorMap = ToLinear( PdxTex2DLod0( ColorTexture, float2( ColorMapCoords.x, 1.0 - ColorMapCoords.y ) ).rgb );
#endif

			Out.FlatMap = float3( vec3( 0.5f ) ); // neutral overlay
			#ifdef TERRAIN_FLAT_MAP_LERP
				Out.FlatMap = lerp( Out.FlatMap, PdxTex2DLod0( FlatMapTexture, float2( ColorMapCoords.x, 1.0 - ColorMapCoords.y ) ).rgb, FlatMapLerp );
			#endif

			Out.Normal = CalculateNormal( Vertex.WorldSpacePos.xz );

			return Out;
		}
	]]

	MainCode VertexShader
	{
		Input = "VS_INPUT_PDX_TERRAIN"
		Output = "VS_OUTPUT_PDX_TERRAIN"
		Code
		[[
			PDX_MAIN
			{
				return TerrainVertex( Input.UV, Input.NodeOffset_Scale_Lerp.xy, Input.NodeOffset_Scale_Lerp.z, Input.LodDirection, Input.NodeOffset_Scale_Lerp.w );
			}
		]]
	}

	MainCode VertexShaderSkirt
	{
		Input = "VS_INPUT_PDX_TERRAIN_SKIRT"
		Output = "VS_OUTPUT_PDX_TERRAIN"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT_PDX_TERRAIN Out = TerrainVertex( Input.UV, Input.NodeOffset_Scale_Lerp.xy, Input.NodeOffset_Scale_Lerp.z, Input.LodDirection, Input.NodeOffset_Scale_Lerp.w );

				float3 Position = FixPositionForSkirt( Out.WorldSpacePos, Input.VertexID );
				Out.Position = FixProjectionAndMul( ViewProjectionMatrix, float4( Position, 1.0 ) );

				return Out;
			}
		]]
	}

	MainCode VertexShaderLowSpec
	{
		Input = "VS_INPUT_PDX_TERRAIN"
		Output = "VS_OUTPUT_PDX_TERRAIN_LOW_SPEC"
		Code
		[[
			PDX_MAIN
			{
				return TerrainVertexLowSpec( Input.UV, Input.NodeOffset_Scale_Lerp.xy, Input.NodeOffset_Scale_Lerp.z, Input.LodDirection, Input.NodeOffset_Scale_Lerp.w );
			}
		]]
	}

	MainCode VertexShaderLowSpecSkirt
	{
		Input = "VS_INPUT_PDX_TERRAIN_SKIRT"
		Output = "VS_OUTPUT_PDX_TERRAIN_LOW_SPEC"
		Code
		[[
			PDX_MAIN
			{
				VS_OUTPUT_PDX_TERRAIN_LOW_SPEC Out = TerrainVertexLowSpec( Input.UV, Input.NodeOffset_Scale_Lerp.xy, Input.NodeOffset_Scale_Lerp.z, Input.LodDirection, Input.NodeOffset_Scale_Lerp.w );

				float3 Position = FixPositionForSkirt( Out.WorldSpacePos, Input.VertexID );
				Out.Position = FixProjectionAndMul( ViewProjectionMatrix, float4( Position, 1.0 ) );

				return Out;
			}
		]]
	}
}


PixelShader =
{
	# PdxTerrain uses texture index 0 - 6

	# Jomini specific
	TextureSampler ShadowMap
	{
		Ref = PdxShadowmap
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
		CompareFunction = less_equal
		SamplerType = "Compare"
	}

	# Game specific
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
	TextureSampler EnvironmentMap
	{
		Ref = JominiEnvironmentMap
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
		Type = "Cube"
	}
	TextureSampler FlatMapEnvironmentMap
	{
		Ref = FlatMapEnvironmentMap
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
		Type = "Cube"
	}
	TextureSampler SurroundFlatMapMask
	{
		Ref = SurroundFlatMapMask
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Border"
		SampleModeV = "Border"
		Border_Color = { 1 1 1 1 }
		File = "gfx/map/surround_map/surround_mask.dds"
	}

	Code
	[[
		static const float UNDERWATER_CLIP_OFFSET = 0.00001f;
		static const float TERRAIN_SKIRT_CLIP_OFFSET = 0.01f;
		SLightingProperties GetFlatMapLerpSunLightingProperties( float3 WorldSpacePos, float ShadowTerm )
		{
			SLightingProperties LightingProps;
			LightingProps._ToCameraDir = normalize( CameraPosition - WorldSpacePos );
			LightingProps._ToLightDir = ToSunDir;
			LightingProps._LightIntensity = FlatMapLerpSunDiffuse * 5;
			LightingProps._ShadowTerm = ShadowTerm;
			LightingProps._CubemapIntensity = FlatMapLerpCubemapIntensity;
			LightingProps._CubemapYRotation = FlatMapLerpCubemapYRotation;

			return LightingProps;
		}
		void CheckClipNeeded( float TerrainHeight, float2 MapCoords, float StartColorOverlayHeightBlend )
		{
			#ifdef TERRAIN_SKIRT
				clip( TerrainHeight - TERRAIN_SKIRT_CLIP_OFFSET );
			#endif

			#ifdef UNDERWATER
				// When doing the refraction pass and applying the Color Overlay, skip the parts above the ocean.
				if ( StartColorOverlayHeightBlend > 0.99f )
				{
					clip( _RefractionCullHeight - TerrainHeight );
				}
			#endif
			clip( vec2( 1.0f ) - MapCoords );
		}

		// MOD(eotg) ---- hybrid terrain look -------------------------------------------------
		// The terrain textures carry only smooth greyscale structure, shared between terrains.
		// Each terrain's identity is applied here: DetailIndexTexture holds the material index
		// per pixel and DetailMaskTexture its blend weight, so we can look the terrain up and
		// tint/parameterise per pixel - and it blends across boundaries for free, using the same
		// weights the detail blend already uses.
		//
		// Stars are generated rather than baked. A baked pinpoint has a fixed texture size and
		// falls below one screen pixel as you zoom out, so it sparkles under the minification
		// terrain is always viewed with. These are two octaves, each faded out over the camera
		// range where its cell stops being well sampled.
		// Stars run along a temperature ramp rather than all being one white. Each terrain biases
		// the ramp (EOTG_STAR_TEMP, per material) and each star jitters around that bias, so a
		// Frozen Cluster reads blue and a Fertile Reach golden - which is what the art direction
		// in docs/terrain_texture_prompts.md has always said and the map never showed.
		#define EOTG_STAR_WARM        float3( 1.00f, 0.74f, 0.46f )   // K/M: amber
		#define EOTG_STAR_MID         float3( 1.00f, 0.96f, 0.88f )   // G: the old single colour
		#define EOTG_STAR_COOL        float3( 0.70f, 0.82f, 1.00f )   // B/A: blue-white
		#define EOTG_STAR_TEMP_JITTER 0.55f    // per-star spread around the terrain bias

		// Where the additive layers (stars, modifier FX) fade out, as a fraction of the camera's
		// zoom-in..zoom-out range. They are detail for looking at the world, not for reading it.
		#define EOTG_ZOOMOUT_START 0.55f
		#define EOTG_ZOOMOUT_END   0.90f

		// How opaque the political map mode is over the terrain at ordinary zoom. Vanilla covers
		// the ground almost completely, which is right for a parchment map and wrong here - the
		// terrain IS the setting, and burying the nebulae under flat realm colour throws away the
		// whole map. Borders come from pdxborder.shader and are not touched, so realms stay just
		// as readable; only the fill is thinned.
		// It returns to full strength as the paper map comes in, where there is no terrain to see.
		#define EOTG_POLITICAL_OPACITY 0.55f

		// The world just stops at the map border - terrain one pixel, nothing the next. Fade it
		// out instead, so the galaxy thins into empty space rather than being cut off. Measured
		// in map UV, where the whole map is 0..1 on each axis, so the band is a fraction of the
		// map's width and height rather than a world distance - the map is twice as wide as it
		// is tall, so a world-space band would be visibly wider at the poles than at the sides.
		#define EOTG_EDGE_FADE_START 0.055f   // fade begins this far in from the border
		#define EOTG_EDGE_FADE_END   0.004f   // fully gone this far in
		// Occupancy follows a POWER LAW, not a straight line: a linear map bottoms out at
		// 8% of the top (because the lowest tier's Density is 0.08) and the tiers read as
		// near-identical. The exponent pulls the empty end down and spreads everything.
		#define EOTG_OCC_MAX          0.45f   // Density 1 -> 45% of grid cells hold a star
		#define EOTG_DENSITY_GAMMA    1.45f
		// Density also drives star SIZE, so a dense region gains luminous area, not just count.
		#define EOTG_RADIUS_LO        0.75f
		#define EOTG_RADIUS_HI        1.30f
		#define EOTG_STAR_FINE_CELL   2.83f  // /sqrt(2): halves cell AREA, so 2x the stars
		#define EOTG_STAR_FINE_R      0.40f
		#define EOTG_STAR_COARSE_CELL 8.49f
		#define EOTG_STAR_COARSE_R    1.70f   // at full zoom out
		#define EOTG_STAR_COARSE_R_MIN 0.80f  // zoomed right in: 1.47x the fine star, measured at 10% falloff
		// Gaussian tightness. Higher is a crisper core with less halo. The coarse stars are the
		// ones you look at, so they get the tighter profile; the fine layer stays soft because at
		// its size a hard core aliases.
		#define EOTG_STAR_COARSE_FALLOFF 4.60f
		#define EOTG_STAR_FINE_FALLOFF   2.50f
		#define EOTG_STRUCTURE_FLOOR  0.30f   // level the structure fades toward when amount = 0
		// Overall terrain level. Solved so the set lands near 0.07 on screen after the colormap
		// soft-lights it: at 1.0 the mean came out 0.172, which read as washed-out grey.
		#define EOTG_TERRAIN_LEVEL    0.55f
		// Terrain is unlit: space has no sun. Albedo goes straight to screen, so the material
		// table's numbers are what you actually see, and stars are not washed out by a x8 sun.
		#define EOTG_TERRAIN_EMISSIVE 1.20f
		#define EOTG_STRUCTURE_SCALE  0.90f   // global: how much of the structure texture survives
		                                      // (0.45 suited a soft cloud; a grid wants to be seen)
		// Where the fine star layer fades in, as a fraction of the camera's zoom range.
		// The coarse layer has no such band - it is always on, so the constellations you pick
		// out zoomed out are still there, in the same places, when you come in close.
		#define EOTG_STAR_FINE_IN     0.22f   // fine stars at full strength at or below this
		#define EOTG_STAR_FINE_OUT    0.58f   // and gone at or above it
		#define EOTG_STAR_GAIN        1.00f

		// --- terrain modifiers: per-terrain appearance generated in-shader ---------------
		// Every one is a CONTINUOUS FIELD, never isolated points, and fades out before its
		// feature size drops below a screen pixel. Same rule the textures have to follow.
		#define EOTG_MOD_FADE_FAR     440.0f
		#define EOTG_MOD_FADE_RANGE   170.0f
		#define EOTG_MOD_GAIN           1.6f   // global dial for every effect at once
		// Effects are KINDS, not terrains. A kind is a shape-generating primitive that lives here;
		// every number that makes one kind look like a particular terrain lives in the generated
		// arrays (EOTG_FX_*) instead, indexed by material. So adding a terrain that reuses a kind
		// is a row in build_terrain_hybrid.py and nothing here. Only a genuinely new *shape* costs
		// shader work, which is the right place for that cost to land.
		//
		//   kind  primitive                        P                              Q
		//   0     none
		//   1     shard    Voronoi ridge           ridgeW, patchScale, bodyGain   -
		//   2     splat    rotated gaussians       len, width, sparsity, cross    -
		//   3     rings    lens + starlight warp   (fixed, see below)             -
		//   4     bands    warped sine bands       dirX, dirY, freq, warp         warpScale, grain
		//   5     filament ridged warped noise     freq, warp, thinness, grain    warpScale
		//
		// EOTG_FX_DARK is how far the effect may darken the terrain under it - what turns a glow
		// into a structure. 0.35 means the dark side drops to 35% of base brightness.
		//
		// Kind 3 keeps its constants here on purpose: it is the one effect whose parameters are
		// read at a neighbouring *anchor* rather than at this pixel, so it cannot use the
		// per-material arrays without also fetching that anchor's material.
		// Set to 0 if the shader fails to compile: GlobalTime is declared by the shared includes
		// that both this and pdxwater use, but it is the one symbol here not already proven in
		// the terrain pass. Everything else degrades to a static but still varied field.
		#define EOTG_MOD_ANIMATE            1

		#define EOTG_MOD_DARK_LENS      0.42f
		#define EOTG_MOD_LENS_CELL     34.0f
		#define EOTG_MOD_LENS_FREQ     13.0f
		#define EOTG_MOD_LENS_WARP      1.15f
		#define EOTG_MOD_LENS_REACH     0.52f   // base ring radius; varied per anchor below
		#define EOTG_MOD_LENS_GAIN      0.42f
		#define EOTG_MOD_LENS_DRIFT     0.22f   // how fast the rings breathe, per anchor and signed
		// Two ends of a hue range rather than one colour: every anomaly picked the same teal, which
		// is half of why they read as a repeated decal.
		#define EOTG_MOD_LENS_COLOR_A  float3( 0.16f, 0.90f, 0.78f )
		#define EOTG_MOD_LENS_COLOR_B  float3( 0.30f, 0.62f, 1.00f )
		#define EOTG_MOD_FLARE_FLICKER  0.55f

		// 1 well inside the map, 0 at the border.
		float EotgEdgeFade( float2 uv )
		{
			float e = min( min( uv.x, 1.0f - uv.x ), min( uv.y, 1.0f - uv.y ) );
			return smoothstep( EOTG_EDGE_FADE_END, EOTG_EDGE_FADE_START, e );
		}

		float EotgStarHash( float2 p )
		{
			return frac( sin( dot( p, float2( 127.1f, 311.7f ) ) ) * 43758.5453f );
		}

		// Star density and brightness at an arbitrary world position. Lod0 because this is called
		// inside divergent flow, where implicit derivatives are undefined.
		// 0 = amber, 0.5 = white, 1 = blue-white. Signed-square keeps most stars near the middle
		// of whatever bias they are given, so the colour reads as variation rather than confetti.
		float3 EotgStarTint( float t )
		{
			t = saturate( t );
			return ( t < 0.5f ) ? lerp( EOTG_STAR_WARM, EOTG_STAR_MID, t * 2.0f )
								: lerp( EOTG_STAR_MID, EOTG_STAR_COOL, ( t - 0.5f ) * 2.0f );
		}

		float3 EotgStarParamsAt( float2 xz )
		{
			float2 C = xz * WorldSpaceToDetail + DetailTexelSize * 0.5f;
			float4 Idx = PdxTex2DLod0( DetailIndexTexture, C ) * 255.0f;
			float4 W   = PdxTex2DLod0( DetailMaskTexture, C );
			float total = W.x + W.y + W.z + W.w + 1e-5f;
			int t0 = clamp( int( Idx.x + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int t1 = clamp( int( Idx.y + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int t2 = clamp( int( Idx.z + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int t3 = clamp( int( Idx.w + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			float w0 = W.x / total, w1 = W.y / total, w2 = W.z / total, w3 = W.w / total;
			return float3(
				EOTG_STAR_DENSITY[t0] * w0 + EOTG_STAR_DENSITY[t1] * w1
					+ EOTG_STAR_DENSITY[t2] * w2 + EOTG_STAR_DENSITY[t3] * w3,
				EOTG_STAR_BRIGHT[t0] * w0 + EOTG_STAR_BRIGHT[t1] * w1
					+ EOTG_STAR_BRIGHT[t2] * w2 + EOTG_STAR_BRIGHT[t3] * w3,
				EOTG_STAR_TEMP[t0] * w0 + EOTG_STAR_TEMP[t1] * w1
					+ EOTG_STAR_TEMP[t2] * w2 + EOTG_STAR_TEMP[t3] * w3 );
		}

		// A star belongs to the terrain it SITS ON, not to the terrain under the pixel currently
		// being shaded. Reading density and brightness per pixel meant a star straddling a border
		// had its existence, its radius and its brightness decided differently on each half, so it
		// came out sliced down the middle. Same fix, and the same reason, as the lens rings gating
		// on their own anchor.
		//
		// The terrain fetch is paid only by stars that actually reach this pixel: the conservative
		// radius test uses EOTG_RADIUS_HI, the largest any terrain could ask for, and rejects first.
		float3 EotgStarLayer( float2 xz, float cell, float radiusWorld, float falloff )
		{
			float2 baseCell = floor( xz / cell );
			float3 acc = vec3( 0.0f );
			float maxR = radiusWorld * EOTG_RADIUS_HI;
			for ( int j = -1; j <= 1; j++ )
			{
				for ( int i = -1; i <= 1; i++ )
				{
					float2 cc = baseCell + float2( float( i ), float( j ) );
					float2 off = float2( EotgStarHash( cc + 7.3f ), EotgStarHash( cc + 3.1f ) );
					float2 starPos = ( cc + off ) * cell;
					float2 delta = xz - starPos;
					if ( dot( delta, delta ) > maxR * maxR )
					{
						continue;
					}
					float3 sp = EotgStarParamsAt( starPos );
					float dn = saturate( sp.x );
					if ( dn < 0.01f )
					{
						continue;
					}
					float sparsity = 1.0f - EOTG_OCC_MAX * pow( dn, EOTG_DENSITY_GAMMA );
					if ( EotgStarHash( cc ) <= sparsity )
					{
						continue;
					}
					float r = radiusWorld * lerp( EOTG_RADIUS_LO, EOTG_RADIUS_HI, dn );
					float d = length( delta ) / r;
					float b = 0.30f + 0.70f * EotgStarHash( cc + 11.7f );
					// Temperature: the terrain's bias, jittered per star. Signed-square so most
					// sit near the bias and only a few go strongly amber or blue.
					float th = EotgStarHash( cc + 5.5f ) * 2.0f - 1.0f;
					float3 tint = EotgStarTint( sp.z + th * abs( th ) * EOTG_STAR_TEMP_JITTER );
					acc += tint * ( b * sp.y * exp( -d * d * falloff ) );
				}
			}
			return saturate( acc );
		}

		// Density/Bright are no longer read - each star reads its own - but the parameters stay so
		// the call sites and EotgTerrainLook do not have to change; the compiler strips them.
		// There is no early-out on pixel density any more, and there must not be: that is exactly
		// what cut stars off at borders. Cost is held down instead by the radius test inside the
		// layer, which rejects before paying for the terrain fetch, so only the ~30% of pixels
		// that actually have a star nearby pay for one.
		float3 EotgStars( float3 WorldSpacePos, float Density, float Bright )
		{
			// The coarse layer is ALWAYS drawn, at full strength, at every zoom. It is the sky:
			// fixed world-space cells and a positional hash, so a star sits at the same place
			// whatever the camera does, and its radius is in world units, so zooming in makes it
			// grow rather than vanish. The fine layer only adds smaller stars between them.
			//
			// These used to cross-fade on camDist: coarse faded OUT below 120 and fine faded IN
			// below 260, so zooming in swapped one star field for a completely different one.
			// camDist is also per pixel, which meant the near and far halves of a single frame
			// were showing different layers - the same mistake as the water nebula.
			float EotgZoomF = GetZoomedInZoomedOutFactor();
			float fine = 1.0f - smoothstep( EOTG_STAR_FINE_IN, EOTG_STAR_FINE_OUT, EotgZoomF );

			// The coarse radius is in world units, so holding it fixed meant that keeping the star
			// at full zoom out - where 1.70 units is a few pixels - turned it into a blob tens of
			// pixels across when zoomed in. It now shrinks as the camera comes down, which keeps
			// its SCREEN size roughly steady: the same star, still in the same place, still bigger
			// than its neighbours, but not a smear. It never goes below EOTG_STAR_COARSE_R_MIN,
			// which is set relative to the fine radius so it stays the larger of the two.
			float rCoarse = lerp( EOTG_STAR_COARSE_R_MIN, EOTG_STAR_COARSE_R,
				smoothstep( 0.15f, 1.0f, EotgZoomF ) );

			float3 s = EotgStarLayer( WorldSpacePos.xz, EOTG_STAR_COARSE_CELL,
				rCoarse, EOTG_STAR_COARSE_FALLOFF );
			if ( fine > 0.01f )
			{
				s += EotgStarLayer( WorldSpacePos.xz, EOTG_STAR_FINE_CELL,
					EOTG_STAR_FINE_R, EOTG_STAR_FINE_FALLOFF ) * fine;
			}
			return saturate( s ) * EOTG_STAR_GAIN;
		}


		float EotgValueNoise( float2 p )
		{
			float2 i = floor( p ), f = frac( p );
			f = f * f * ( 3.0f - 2.0f * f );
			float a = EotgStarHash( i );
			float b = EotgStarHash( i + float2( 1.0f, 0.0f ) );
			float c = EotgStarHash( i + float2( 0.0f, 1.0f ) );
			float d = EotgStarHash( i + float2( 1.0f, 1.0f ) );
			return lerp( lerp( a, b, f.x ), lerp( c, d, f.x ), f.y );
		}

		// Same as EotgFbm, but each octave is ROTATED as well as scaled.
		//
		// EotgFbm scales by 2.03 and never rotates, so every octave lands on the same
		// axis-aligned lattice and their cell edges stack. Value noise already shows its grid;
		// stacking three copies of it makes the grid a feature. At the low frequency the Frozen
		// Cluster warp needs, those cells are large, and they showed in game as soft rectangular
		// patches across the whole terrain. An incommensurate rotation per octave means no two
		// lattices ever line up.
		//
		// Deliberately a separate function: EotgFbm is used by the filament, strands and shard
		// effects, and changing the noise under them would change three terrains that nobody has
		// complained about.
		float EotgFbmRot( float2 p )
		{
			const float ca = 0.7373f, sa = 0.6755f;   // ~42.5 degrees
			float sum = 0.0f, amp = 0.5f;
			for ( int k = 0; k < 4; k++ )
			{
				sum += amp * EotgValueNoise( p );
				p = float2( p.x * ca + p.y * sa, -p.x * sa + p.y * ca ) * 2.03f;
				amp *= 0.5f;
			}
			return sum;
		}
		float EotgFbm( float2 p )
		{
			float sum = 0.0f, amp = 0.5f;
			for ( int k = 0; k < 3; k++ )
			{
				sum += amp * EotgValueNoise( p );
				p *= 2.03f;
				amp *= 0.5f;
			}
			return sum;
		}

		// Weight of one MODIFIER id at an arbitrary world position. Lets an effect ask
		// "is there an anomaly *there*", rather than only "am I standing in one".
		// Lod0 because this is called inside divergent flow, where implicit derivatives
		// are undefined.
		float EotgModWeightAt( float2 xz, int kind )
		{
			float2 C = xz * WorldSpaceToDetail + DetailTexelSize * 0.5f;
			float4 Idx = PdxTex2DLod0( DetailIndexTexture, C ) * 255.0f;
			float4 W   = PdxTex2DLod0( DetailMaskTexture, C );
			float total = W.x + W.y + W.z + W.w + 1e-5f;
			int t0 = clamp( int( Idx.x + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int t1 = clamp( int( Idx.y + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int t2 = clamp( int( Idx.z + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int t3 = clamp( int( Idx.w + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			float acc = 0.0f;
			acc += ( EOTG_FX_KIND[t0] == kind ) ? W.x : 0.0f;
			acc += ( EOTG_FX_KIND[t1] == kind ) ? W.y : 0.0f;
			acc += ( EOTG_FX_KIND[t2] == kind ) ? W.z : 0.0f;
			acc += ( EOTG_FX_KIND[t3] == kind ) ? W.w : 0.0f;
			return saturate( acc / total );
		}

		// Distance fade shared by every effect. Hoisted out of EotgModifierFX so the caller can
		// skip EotgLensField too: that runs for every land pixel, and at strategic zoom - where
		// the most pixels are on screen - it was still doing its 9-cell walk for effects that had
		// already faded to nothing. Stars stop being warped out there as well, which is correct:
		// the lens that would bend them is invisible.
		float EotgModFade( float3 WorldSpacePos )
		{
			float camDist = length( CameraPosition - WorldSpacePos );
			return saturate( ( EOTG_MOD_FADE_FAR - camDist ) / EOTG_MOD_FADE_RANGE );
		}

		// 1 -- Anomaly Fields. Gravitational lensing, evaluated for EVERY pixel rather than
		// only inside the terrain: each anchor is gated by the terrain at its own position, so
		// a ring centred near a border carries on into the neighbour instead of being cut off.
		// Returns xy = star-field warp, z = ring brightness, w = footprint (for darkening).
		float4 EotgLensField( float2 xz, out float hueMix )
		{
			float2 baseCell = floor( xz / EOTG_MOD_LENS_CELL );
			float4 acc = float4( 0.0f, 0.0f, 0.0f, 0.0f );
			float hueAcc = 0.0f;
			for ( int j = -1; j <= 1; j++ )
			{
				for ( int i = -1; i <= 1; i++ )
				{
					float2 cc = baseCell + float2( float( i ), float( j ) );
					if ( EotgStarHash( cc + 21.7f ) > 0.55f )
					{
						continue;
					}
					float2 off = float2( EotgStarHash( cc + 5.9f ), EotgStarHash( cc + 13.3f ) );
					float2 anchor = ( cc + off ) * EOTG_MOD_LENS_CELL;
					float2 toC = xz - anchor;

					// Size and shape vary per anchor, and have to be known before the reach test.
					// An ellipse at its own angle is what stops these reading as a stamped circle.
					float rad = EOTG_MOD_LENS_REACH * ( 0.62f + 0.76f * EotgStarHash( cc + 41.2f ) );
					float ang = EotgStarHash( cc + 27.6f ) * 6.2831853f;
					float asp = 0.68f + 0.64f * EotgStarHash( cc + 53.8f );
					float cs = cos( ang ), sn = sin( ang );
					float2 e = float2( toC.x * cs + toC.y * sn,
									 ( -toC.x * sn + toC.y * cs ) * asp );
					float r = length( e ) / ( EOTG_MOD_LENS_CELL * rad );
					if ( r > 1.0f )
					{
						continue;
					}
					// Only now, once we know this anchor reaches us, is the fetch worth paying for.
					float aw = EotgModWeightAt( anchor, 3 );   // kind 3 = rings
					if ( aw < 0.01f )
					{
						continue;
					}
					// Ring spacing, brightness and phase vary too, so no two anomalies match.
					float freq  = EOTG_MOD_LENS_FREQ * ( 0.70f + 0.75f * EotgStarHash( cc + 61.4f ) );
					float amp   = 0.55f + 0.45f * EotgStarHash( cc + 71.9f );
					float phase = EotgStarHash( cc + 83.1f ) * 6.2831853f;
					#if EOTG_MOD_ANIMATE
						// Signed drift: each one breathes at its own rate, some outward, some in,
						// so the field is never in step with itself.
						phase += GlobalTime * EOTG_MOD_LENS_DRIFT
							   * ( EotgStarHash( cc + 97.3f ) * 2.0f - 1.0f );
					#endif
					float falloff = ( 1.0f - r ) * ( 1.0f - r );
					float ring = sin( r * freq + phase );
					acc.z += ring * ring * falloff * aw * amp;
					acc.w += falloff * aw;
					hueAcc += EotgStarHash( cc + 17.1f ) * falloff * aw;
					if ( r > 1e-4f )
					{
						float pull = falloff / max( r, 0.18f );
						acc.xy -= normalize( toC ) * pull * EOTG_MOD_LENS_WARP * aw;
					}
				}
			}
			hueMix = saturate( hueAcc / max( acc.w, 1e-4f ) );
			return float4( acc.xy, saturate( acc.z ), saturate( acc.w ) );
		}

		// 2 -- Frozen Cluster. Voronoi cell walls read as crystalline facets. F2-F1 gives a
		// smooth ridge rather than a hard line, which is what keeps it from aliasing.
		// kind 1 -- P = ( ridge width, patch scale, body gain, - )
		float EotgFxShard( float2 xz, float cell, float4 P, float4 Q )
		{
			float2 baseCell = floor( xz / cell );
			float f1 = 1e9f, f2 = 1e9f;
			float2 nearCC = baseCell, nearP = xz;
			for ( int j = -1; j <= 1; j++ )
			{
				for ( int i = -1; i <= 1; i++ )
				{
					float2 cc = baseCell + float2( float( i ), float( j ) );
					float2 off = float2( EotgStarHash( cc + 2.7f ), EotgStarHash( cc + 8.1f ) );
					float d = length( xz - ( cc + off ) * cell ) / cell;
					if ( d < f1 )
					{
						f2 = f1;
						f1 = d;
						nearCC = cc;
						nearP  = ( cc + off ) * cell;
					}
					else if ( d < f2 )
					{
						f2 = d;
					}
				}
			}
			float ridge = saturate( 1.0f - ( f2 - f1 ) / max( P.x, 1e-4f ) );
			ridge = ridge * ridge * ridge;
			// A bare Voronoi ridge tiles the plane evenly, which is why it read as a honeycomb.
			// Mask it with a large-scale field so facets gather into floes with clear ice between,
			// and brighten the shard interiors so the cells are bodies rather than empty holes.
			float patch = saturate( EotgFbm( xz * P.y ) * 2.4f - 0.55f );
			float body = saturate( 1.0f - f1 * 2.2f ) * P.z;
			// Splinters. Q = ( -, length, width, gain ), both lengths as a fraction of the cell.
			// One elongated lobe per cell, rotated by the cell's own hash, so the fracture network
			// has actual shards lying in it rather than being only the lines between them. This
			// lives inside kind 1 because kind 1 has exactly one user - Frozen Cluster - so there
			// is nothing else to break. Gain 0 is a no-op, which is what every other preset uses.
			float splinter = 0.0f;
			if ( Q.w > 0.001f )
			{
				float sang = EotgStarHash( nearCC + 19.3f ) * 6.2831853f;
				float scs = cos( sang ), ssn = sin( sang );
				float2 sr = xz - nearP;
				float2 srr = float2( sr.x * scs + sr.y * ssn, -sr.x * ssn + sr.y * scs );
				float slx = max( Q.y * cell, 1e-4f ), swy = max( Q.z * cell, 1e-4f );
				splinter = exp( -( srr.x * srr.x ) / ( slx * slx )
				              - ( srr.y * srr.y ) / ( swy * swy ) ) * Q.w;
			}
			return saturate( ridge + body + splinter ) * patch;
		}

		// 3 -- Volatile Cluster. Anisotropic flares: a stretched lobe plus a weaker
		// perpendicular one, each cell rotated by its own hash so nothing looks stamped.
		// kind 2 -- P = ( length, width, sparsity, cross gain )
		float EotgFxSplat( float2 xz, float cell, float4 P, float4 Q )
		{
			float2 baseCell = floor( xz / cell );
			float acc = 0.0f;
			for ( int j = -1; j <= 1; j++ )
			{
				for ( int i = -1; i <= 1; i++ )
				{
					float2 cc = baseCell + float2( float( i ), float( j ) );
					if ( EotgStarHash( cc + 31.4f ) < P.z )
					{
						continue;
					}
					float2 off = float2( EotgStarHash( cc + 4.2f ), EotgStarHash( cc + 9.6f ) );
					float2 d = xz - ( cc + off ) * cell;
					float ang = EotgStarHash( cc + 17.5f ) * 6.2831853f;
					float cs = cos( ang ), sn = sin( ang );
					float2 r = float2( d.x * cs + d.y * sn, -d.x * sn + d.y * cs );
					// Size and brightness per anchor: rotation alone was not enough to stop these
					// reading as one sprite stamped over and over.
					float sc  = 0.65f + 0.70f * EotgStarHash( cc + 12.8f );
					float amp = 0.55f + 0.45f * EotgStarHash( cc + 22.4f );
					// Q.y = the fraction of sprites that render FAINT, Q.z = how faint.
					// The per-anchor amp above only spans 0.55-1.0, which is variation but not
					// contrast - every sprite still reads as the same weight. This splits the field
					// into two populations on its own hash, so a dust field can be half solid and
					// half a thin veil rather than a uniform stipple. Q.y = 0 leaves every existing
					// effect exactly as it was, which is why debris and the flares are untouched.
					if ( Q.y > 0.0f && EotgStarHash( cc + 55.1f ) < Q.y )
					{
						amp *= Q.z;
					}
					#if EOTG_MOD_ANIMATE
						// Volatile Cluster is meant to be unstable, so let them actually flare.
						amp *= 0.62f + 0.38f * sin( GlobalTime * EOTG_MOD_FLARE_FLICKER
							 * ( 0.6f + EotgStarHash( cc + 33.9f ) )
							 + EotgStarHash( cc + 44.5f ) * 6.2831853f );
					#endif
					float lx = max( P.x * sc, 1e-4f ), wy = max( P.y * sc, 1e-4f );
					acc += exp( -( r.x * r.x ) / ( lx * lx ) - ( r.y * r.y ) / ( wy * wy ) ) * amp;
					acc += exp( -( r.y * r.y ) / ( lx * lx ) - ( r.x * r.x ) / ( wy * wy ) ) * P.w * amp;
				}
			}
			return saturate( acc );
		}

		// 4 -- Nebula Barrier / Nebula Wilds. Domain-warped bands: turbulent gas that reads
		// as a wall you would rather go around than through.
		// kind 4 -- P = ( dirX, dirY, freq, warp ), Q = ( warp scale, grain, alt freq, alt amount )
		// Covers both the gas wall and the strata bands: they were the same warped-sine field with
		// different direction, frequency and shaping, which is exactly what a kind is for.
		//
		// Q.w blends the band coordinate from world space toward ALTITUDE. At 1 the bands are
		// iso-elevation lines, so the field layers itself along the landform: a peak reads as a set
		// of nested rings and a ridge as parallel strata following its spine. The shape of the
		// mountain gets drawn by the mountain. This replaces the gradient-direction alignment that
		// tiled the map with moire - there is no direction here to go noisy, only the height value
		// that is already being sampled for the height gate.
		float EotgFxBands( float2 xz, float scale, float4 P, float4 Q, float h01 )
		{
			float2 p = xz * scale;
			float warp = EotgFbm( p * Q.x );
			float coord = lerp( dot( p, P.xy ) * P.z, h01 * Q.z, Q.w );
			float t = 0.5f + 0.5f * sin( coord + warp * P.w );
			if ( Q.y > 0.0f )
			{
				// grain > 0: squared, so the gaps between the streams go properly dark instead of
				// grey, then broken up by a second octave.
				return saturate( t * t * ( 0.45f + Q.y * EotgFbm( p * 1.7f ) ) );
			}
			// grain 0: flat-topped bands with clean corridors between, instead of a soft ramp
			// that reads as one continuous blur.
			return smoothstep( 0.22f, 0.78f, saturate( t ) );
		}

		// kind 6 -- dense nebula.  P = ( layer altitude, parallax, opacity, puff )
		//                           Q = ( density gain, grazing max, emission threshold, churn )
		// The point of this kind is that it is NOT a texture. Its layers are offset against the
		// VIEW DIRECTION, so they slide over each other as the camera moves, and the whole field
		// thickens at grazing angles the way a volume does - neither of which a flat field can
		// fake. Layers composite front to back, so a near layer occludes a far one instead of
		// averaging with it.
		//
		// Both numbers that matter here were found by measurement, not by eye, in
		// docs/tools/preview_terrain_fx.py:
		//   * a RIDGED density ( 1 - |2n-1| ) draws closed filaments and reads as lace, not gas;
		//     billow ( |2n-1| ) gives the puffy clumps a nebula needs.
		//   * density gain above ~0.6 SATURATES the field: at 1.25, 94% of pixels sat above 0.5,
		//     which flattens it to a wash AND kills the parallax, because a field with no dynamic
		//     range left has nothing to reveal as it slides. Measured view response fell from
		//     0.85 to 0.10. Keep the dense fraction near 0.15-0.40.
		// Returns ( density, emission ).
		float2 EotgFxNebula( float2 xz, float3 WorldSpacePos, float scale, float4 P, float4 Q, float h01 )
		{
			float3 toCam = CameraPosition - WorldSpacePos;
			float3 V = toCam / max( length( toCam ), 1e-3f );
			float trans = 1.0f;
			float dens = 0.0f;
			float emis = 0.0f;
			for ( int i = 0; i < 3; i++ )
			{
				// Higher ground lifts the layers further, so the parallax is strongest exactly
				// where the mountain is tallest and the gas reads as sitting above the range.
				float alt = P.x * float( i + 1 ) * ( 0.30f + 0.70f * h01 );
				float2 p = ( xz - V.xz * alt * P.y ) * ( scale * ( 1.0f + 0.45f * float( i ) ) );
				#if EOTG_MOD_ANIMATE
					p += float2( sin( GlobalTime * Q.w * ( 0.6f + 0.3f * float( i ) ) ),
								 cos( GlobalTime * Q.w * ( 0.5f + 0.4f * float( i ) ) ) ) * 0.9f;
				#endif
				float d = pow( saturate( abs( EotgFbm( p ) * 2.0f - 1.0f ) ), P.w );
				dens += d * trans;
				trans *= ( 1.0f - d * P.z );
				if ( i == 0 )
				{
					emis = saturate( ( d - Q.z ) / max( 1e-3f, 1.0f - Q.z ) );
				}
			}
			float graze = 1.0f / max( abs( V.y ), 0.02f );
			return float2( saturate( dens * Q.x * min( graze, Q.y ) ), emis );
		}

		// kind 5 -- P = ( freq, warp, thinness, grain ), Q = ( warp scale, -, -, - )
		float EotgFxFilament( float2 xz, float scale, float4 P, float4 Q )
		{
			float2 p = xz * scale;
			// Warp the domain first: this is what makes strands braid and tangle rather than run
			// parallel. Without it, ridged noise reads as contour lines on a map.
			float2 w = float2( EotgFbm( p * Q.x ), EotgFbm( p * Q.x + 5.2f ) ) - 0.25f;
			p += w * P.y;
			float n = EotgFbm( p * P.x );
			float ridge = 1.0f - abs( n * 2.0f - 1.0f );   // thin bright strands, dark between them
			ridge = pow( saturate( ridge ), max( P.z, 1e-3f ) );
			return saturate( ridge * ( 0.65f + P.w * n ) );
		}

		// Offset for the gradient taps, in world units, and a gain that brings the raw slope into
		// a roughly 0..1 range so the per-terrain lo/hi numbers are readable. BOTH need calibrating
		// against the real heightmap - see docs/terrain_materials.md.
		// EPS must span SEVERAL heightmap texels. At 1.0 the two taps landed inside one texel, so
		// the "gradient" was quantisation noise - and normalising that for contour alignment turned
		// it into a full-swing direction that changed every texel, which tiled the map with moire.
		// The detail INDEX texture holds material ids, so it has to be point-sampled: terrain
		// boundaries therefore land on axis-aligned map-texel edges. Vanilla hides that behind
		// high-frequency detail textures; we replaced those with flat tint, so the blocks show.
		// Offsetting the lookup by a little noise turns the stair-steps into irregular organic
		// edges - the boundary still lands in the same place on average, it just stops being a
		// grid. JITTER is in texels; much past ~1.5 and single pixels start defecting to the
		// neighbouring terrain and it reads as speckle.
		// JITTER is in texels. SCALE is in CYCLES PER TEXEL and must be around 1 or more: the
		// first attempt sampled the noise in world space at 0.22, which varied over several
		// texels, so it slid whole boundaries sideways instead of breaking them up and the blocks
		// survived. The noise has to change *within* a texel to dissolve a texel-sized step.
		// Radius, in texels, over which the terrain COLOUR is averaged to make one terrain fade
		// into the next. The jitter above only makes the edge ragged; it cannot widen a transition,
		// because the mask carries barely a texel of blend and there is no more information in the
		// texture to recover. A real gradient has to be built by sampling the neighbourhood.
		// Costs 4 extra index+mask fetch pairs on land pixels in close range. 0 disables.
		#define EOTG_BLEND_SOFT_R       4.5f
		#define EOTG_BLEND_JITTER       1.60f
		#define EOTG_BLEND_JITTER_SCALE 1.30f

		// Relief shading. The engine already lights the terrain normals, but a flat tint plus
		// additive effects wash that out, which is why a mountain range was reading as fog. This
		// puts an explicit directional term back: slopes facing the light brighten, slopes turned
		// away darken. It is the strongest shape cue available and costs the gradient we already
		// compute. DIR is the direction the light comes FROM; GAIN converts raw gradient into a
		// usable range and needs calibrating with EOTG_GRAD_GAIN.
		// GAIN was 220 with a hard clamp, which railed 8.6% of pixels on real relief - and those
		// are exactly the steep faces, so every ridge got a solid black side and a solid white one.
		// Measured on the CK3 heightmap: median slope 0.0011, p99 0.025, so a linear map that is
		// visible on gentle ground is 10x past the rail on a mountain. The curve below compresses
		// instead of clipping, so steep slopes approach the limit and never reach it.
		// The detail texture repeats tile_factor times across the map. On a large terrain with
		// little else in it - the Sahara being the worst case - that grid is plainly visible as
		// wallpaper. Mixing in world-space noise, which by construction cannot repeat, breaks the
		// motif while keeping the detail. Per-material, because it only earns its cost on the big
		// empty terrains. Range is matched to the structure textures' own 0.33-0.70 clip.
		#define EOTG_NEB_CORE  float3( 1.00f, 0.86f, 0.72f )

		#define EOTG_TILEBREAK_SCALE 0.045f

		#define EOTG_SHADE_DIR  float2( -0.60f, -0.80f )
		#define EOTG_SHADE_GAIN 120.0f

		#define EOTG_GRAD_EPS   8.0f
		#define EOTG_GRAD_GAIN 150.0f

		// Local height gradient: 4 taps, giving both how rugged the ground is (z) and which way it
		// falls (xy). Ruggedness is a different question from altitude - Broken Cluster is about
		// terrain being fragmented, not about it being high - and the direction is what lets bands
		// follow contours instead of cutting across them.
		float3 EotgHeightGrad( float2 xz )
		{
			float e = EOTG_GRAD_EPS;
			float hx0 = GetHeightMultisample01( xz - float2( e, 0.0f ), 1.0f );
			float hx1 = GetHeightMultisample01( xz + float2( e, 0.0f ), 1.0f );
			float hy0 = GetHeightMultisample01( xz - float2( 0.0f, e ), 1.0f );
			float hy1 = GetHeightMultisample01( xz + float2( 0.0f, e ), 1.0f );
			float2 g = float2( hx1 - hx0, hy1 - hy0 ) / ( 2.0f * e );
			return float3( g, length( g ) * EOTG_GRAD_GAIN );
		}

		// amount 0 disables. Returns a multiplier around 1.
		float EotgHillshade( float3 Grad, float amount )
		{
			if ( amount <= 0.0f )
			{
				return 1.0f;
			}
			float x = dot( Grad.xy, EOTG_SHADE_DIR ) * EOTG_SHADE_GAIN;
			float s = x / ( 1.0f + abs( x ) );		// soft rolloff: asymptotic, never binary
			return 1.0f + amount * s;
		}

		// S = ( lo, hi, floor ) on gradient magnitude; hi <= lo disables it.
		float EotgFxSlope( float3 Grad, float3 S )
		{
			if ( S.y <= S.x )
			{
				return 1.0f;
			}
			return lerp( S.z, 1.0f, smoothstep( S.x, S.y, Grad.z ) );
		}

		// Any effect may be tied to altitude. H = ( lo, hi, floor ) in 0..1 heightmap units;
		// hi <= lo disables it. The effect runs at `floor` strength at height lo and full strength
		// at hi, so a barrier thickens with altitude and thins out in the passes - which is where
		// the chokepoints are, and where the player needs to be able to see.
		float EotgFxHeight( float h01, float3 H )
		{
			if ( H.y <= H.x )
			{
				return 1.0f;
			}
			return lerp( H.z, 1.0f, smoothstep( H.x, H.y, h01 ) );
		}


		// Each effect contributes light where its field is high and REMOVES light where it
		// is low. Additive-only looked like haze sitting on the terrain; this makes the
		// effect part of the terrain.
		// An effect either carries its own colour or borrows the terrain's, per material.
		float3 EotgFxColor( int t, float3 Tint )
		{
			return lerp( EOTG_FX_COLOR[t], Tint, EOTG_FX_USETINT[t] );
		}

		// 7 -- Frozen Cluster. The Pleiades, which is what this terrain actually is: an open
		// cluster that has drifted into a cold dust cloud. Two mechanics, both from the real
		// object, and neither of them cellular - which is the point, because a Voronoi can only
		// ever read as filled cells or as a net, and both were rejected.
		//
		//  * STRIAE. The nebulosity is streaky because the dust grains are combed into alignment
		//    by the interstellar magnetic field, so the wisps run parallel on ONE axis. That is
		//    what separates this from steppe's strands, which are sparse and randomly oriented,
		//    and from terraced_hills' bands, which follow altitude rather than a fixed heading.
		//  * REFLECTION. It is a reflection nebula, not an emission one: the cloud only glows
		//    where starlight reaches it. So the halos sit on the cluster's OWN star anchors, and
		//    the striae are modulated by that same glow - bright near a star, fading to nothing
		//    between them. No other terrain couples its effect to its stars, which is what makes
		//    this read as a cluster rather than as a texture laid over one.
		//
		// kind 7 -- P = ( stria freq, warp, stria gain, halo radius in star cells )
		//           Q = ( halo gain, direction radians, patch scale, fraction of stars lit )
		float EotgFxReflect( float2 xz, float scale, float4 P, float4 Q )
		{
			// Halos on the coarse star anchors - the same cell, offset and hash EotgStarLayer
			// uses, so a halo lands on a star rather than merely near one.
			float cellS = EOTG_STAR_COARSE_CELL;
			float2 bc = floor( xz / cellS );
			float rad = max( P.w * cellS, 1e-4f );
			float glow = 0.0f;
			for ( int j = -1; j <= 1; j++ )
			{
				for ( int i = -1; i <= 1; i++ )
				{
					float2 cc = bc + float2( float( i ), float( j ) );
					// Q.w: only some stars are bright enough to light the dust. Without this every
					// anchor glowed, the halos overlapped, and the measured coverage was 94% - a flat
					// wash with no cluster in it. At 0.55 it is 17%, which reads as knots.
					if ( EotgStarHash( cc + 41.2f ) >= Q.w )
					{
						continue;
					}
					float2 off = float2( EotgStarHash( cc + 7.3f ), EotgStarHash( cc + 3.1f ) );
					float2 dd = xz - ( cc + off ) * cellS;
					float t = dot( dd, dd ) / ( rad * rad );
					glow += exp( -t ) * ( 0.55f + 0.45f * EotgStarHash( cc + 27.6f ) );
				}
			}
			glow = saturate( glow );

			// Striae: a warped sine on one fixed heading, ridged so the wisps are thin.
			float cs = cos( Q.y ), sn = sin( Q.y );
			float across = -xz.x * sn + xz.y * cs;
			// Two warp octaves at different scales AND a rotated offset. One octave of value noise
			// is sampled on an axis-aligned grid, and at the low frequency these wisps need, that
			// grid shows through as square patches - visible in game as rectangular tiles across
			// the whole terrain. Summing a second, finer, rotated octave breaks the alignment.
			float2 wq = xz * max( Q.z, 1e-4f );
			float2 wr = float2( wq.x * 0.80f + wq.y * 0.60f, -wq.x * 0.60f + wq.y * 0.80f );
			float warpN = ( EotgFbmRot( wq ) - 0.5f ) + ( EotgFbmRot( wr * 2.7f + 19.1f ) - 0.5f ) * 0.55f;
			float warp = warpN * P.y * 6.2831853f;
			float s = sin( across * scale * P.x + warp );
			// 4.5, not 2.6: the softer power made broad bright bands that dominated the terrain.
			// Higher is a thinner, more delicate wisp with more dark between.
			float stria = pow( saturate( 1.0f - abs( s ) ), 5.0f ) * P.z;

			// Reflection: the striae are lit BY the cluster, so they fade out away from it.
			// Floor 0.18 -> 0.08. The floor is how much of the striae shows where NO star lights
			// them, and at 0.18 they were visible across the whole terrain - an all-over weave
			// rather than nebulosity gathered around a cluster. At 0.08 the ground between the
			// lit patches goes quiet.
			return saturate( stria * ( 0.08f + 0.92f * glow ) + glow * Q.x );
		}
		void EotgModifierFX( float3 WorldSpacePos, float3 Tint, float4 ModA, float4 ModB,
							 int4 IdxA, int4 IdxB, float4 Lens, float LensHue, float fade, float h01,
							 float3 Grad,
							 out float3 Additive, out float Multiplier )
		{
			Additive = vec3( 0.0f );
			Multiplier = 1.0f;
			if ( fade < 0.01f )
			{
				return;
			}
			float2 xz = WorldSpacePos.xz;
			float3 col = vec3( 0.0f );
			float mul = 1.0f;

			// Kind 3 is not gated on ModA.z: the rings already carry their own per-anchor weight,
			// which is what lets them spill past the edge of Anomaly Fields.
			if ( Lens.w > 0.003f )
			{
				col += lerp( EOTG_MOD_LENS_COLOR_A, EOTG_MOD_LENS_COLOR_B, LensHue )
					 * Lens.z * EOTG_MOD_LENS_GAIN;
				mul *= lerp( 1.0f, lerp( EOTG_MOD_DARK_LENS, 1.0f, Lens.z ), Lens.w * fade );
			}
			if ( ModA.x > 0.01f )								// kind 1 -- shard
			{
				int t = IdxA.x;
				float w = ModA.x * EotgFxHeight( h01, EOTG_FX_HEIGHT[t] )
							  * EotgFxSlope( Grad, EOTG_FX_SLOPE[t] );
				float f = EotgFxShard( xz, EOTG_FX_SCALE[t], EOTG_FX_P[t], EOTG_FX_Q[t] );
				col += EotgFxColor( t, Tint ) * f * w * EOTG_FX_GAIN[t];
				mul *= lerp( 1.0f, lerp( EOTG_FX_DARK[t], 1.0f, f ), w * fade );
			}
			if ( ModA.y > 0.01f )								// kind 2 -- splat
			{
				int t = IdxA.y;
				float w = ModA.y * EotgFxHeight( h01, EOTG_FX_HEIGHT[t] )
							  * EotgFxSlope( Grad, EOTG_FX_SLOPE[t] );
				float f = EotgFxSplat( xz, EOTG_FX_SCALE[t], EOTG_FX_P[t], EOTG_FX_Q[t] );
				// Q.x inverts the field. The dispatch below darkens where the effect is ABSENT, so
				// every effect is emissive by default and its features are always brighter than
				// their surroundings. That is wrong for rubble: it should occlude, not glow, and
				// a small bright blob is indistinguishable from a star no matter what shape it is.
				// Inverting makes the sprites the dark part and the gaps the lit part.
				if ( EOTG_FX_Q[t].x > 0.0f )
				{
					f = 1.0f - f;
				}
				col += EotgFxColor( t, Tint ) * f * w * EOTG_FX_GAIN[t];
				mul *= lerp( 1.0f, lerp( EOTG_FX_DARK[t], 1.0f, f ), w * fade );
			}
			if ( ModA.w > 0.01f )								// kind 4 -- bands
			{
				int t = IdxA.w;
				float w = ModA.w * EotgFxHeight( h01, EOTG_FX_HEIGHT[t] )
							  * EotgFxSlope( Grad, EOTG_FX_SLOPE[t] );
				float f = EotgFxBands( xz, EOTG_FX_SCALE[t], EOTG_FX_P[t], EOTG_FX_Q[t], h01 );
				col += EotgFxColor( t, Tint ) * f * w * EOTG_FX_GAIN[t];
				mul *= lerp( 1.0f, lerp( EOTG_FX_DARK[t], 1.0f, f ), w * fade );
			}
			if ( ModB.x > 0.01f )								// kind 5 -- filament
			{
				int t = IdxB.x;
				float w = ModB.x * EotgFxHeight( h01, EOTG_FX_HEIGHT[t] )
							  * EotgFxSlope( Grad, EOTG_FX_SLOPE[t] );
				float f = EotgFxFilament( xz, EOTG_FX_SCALE[t], EOTG_FX_P[t], EOTG_FX_Q[t] );
				col += EotgFxColor( t, Tint ) * f * w * EOTG_FX_GAIN[t];
				mul *= lerp( 1.0f, lerp( EOTG_FX_DARK[t], 1.0f, f ), w * fade );
			}
			if ( ModB.y > 0.01f )								// kind 6 -- dense nebula
			{
				int t = IdxB.y;
				float w = ModB.y * EotgFxHeight( h01, EOTG_FX_HEIGHT[t] )
							  * EotgFxSlope( Grad, EOTG_FX_SLOPE[t] );
				float2 ne = EotgFxNebula( xz, WorldSpacePos, EOTG_FX_SCALE[t],
										  EOTG_FX_P[t], EOTG_FX_Q[t], h01 );
				// Two colours: the gas body, and hotter cores where the densest layer peaks -
				// embedded stars lighting it from inside, which is what reads as *dense* rather
				// than as mist.
				col += EotgFxColor( t, Tint ) * ne.x * w * EOTG_FX_GAIN[t];
				col += EOTG_NEB_CORE * ne.y * w * EOTG_FX_GAIN[t] * 1.30f;
				mul *= lerp( 1.0f, lerp( EOTG_FX_DARK[t], 1.0f, ne.x ), w * fade );
			}
			if ( ModB.z > 0.01f )								// kind 7 -- reflection cluster
			{
				int t = IdxB.z;
				float w = ModB.z * EotgFxHeight( h01, EOTG_FX_HEIGHT[t] )
							  * EotgFxSlope( Grad, EOTG_FX_SLOPE[t] );
				float f = EotgFxReflect( xz, EOTG_FX_SCALE[t], EOTG_FX_P[t], EOTG_FX_Q[t] );
				col += EotgFxColor( t, Tint ) * f * w * EOTG_FX_GAIN[t];
				mul *= lerp( 1.0f, lerp( EOTG_FX_DARK[t], 1.0f, f ), w * fade );
			}
			Additive = col * fade * EOTG_MOD_GAIN;
			Multiplier = mul;
		}

		// Kinds are integers and cannot be interpolated, so each kind accumulates the weight of
		// the material slots carrying it, and remembers the heaviest of them. Two terrains meeting
		// cross-fade their effects. Where both use the SAME kind, the parameters are taken from
		// whichever is dominant at that pixel rather than blended - blending them would produce a
		// shape that belongs to neither terrain, and the weight cross-fade already carries the
		// transition.
		void EotgAccumMod( int t, float w, inout float4 ModA, inout float4 ModB,
						   inout int4 IdxA, inout int4 IdxB,
						   inout float4 BestA, inout float4 BestB )
		{
			int k = EOTG_FX_KIND[t];
			if ( k == 1 )      { ModA.x += w; if ( w > BestA.x ) { BestA.x = w; IdxA.x = t; } }
			else if ( k == 2 ) { ModA.y += w; if ( w > BestA.y ) { BestA.y = w; IdxA.y = t; } }
			else if ( k == 3 ) { ModA.z += w; if ( w > BestA.z ) { BestA.z = w; IdxA.z = t; } }
			else if ( k == 4 ) { ModA.w += w; if ( w > BestA.w ) { BestA.w = w; IdxA.w = t; } }
			else if ( k == 5 ) { ModB.x += w; if ( w > BestB.x ) { BestB.x = w; IdxB.x = t; } }
			else if ( k == 6 ) { ModB.y += w; if ( w > BestB.y ) { BestB.y = w; IdxB.y = t; } }
			else if ( k == 7 ) { ModB.z += w; if ( w > BestB.z ) { BestB.z = w; IdxB.z = t; } }
		}

		// One tap's worth of terrain colour, including the hypsometric ramp. Split out because the
		// tint - and only the tint - is averaged over a neighbourhood to get a gradient between
		// terrains. Structure, stars and effects all stay on the single centre tap: blurring those
		// would smear the effects across borders rather than fade the colours.
		float3 EotgTintAt( float2 uv, float h01 )
		{
			float4 Idx = PdxTex2D( DetailIndexTexture, uv ) * 255.0f;
			float4 W   = PdxTex2D( DetailMaskTexture, uv );
			float total = W.x + W.y + W.z + W.w + 1e-5f;
			int i0 = clamp( int( Idx.x + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int i1 = clamp( int( Idx.y + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int i2 = clamp( int( Idx.z + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int i3 = clamp( int( Idx.w + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			float w0 = W.x / total, w1 = W.y / total, w2 = W.z / total, w3 = W.w / total;

			float3 t = EOTG_TINT[i0] * w0 + EOTG_TINT[i1] * w1
					 + EOTG_TINT[i2] * w2 + EOTG_TINT[i3] * w3;
			float3 altTint = EOTG_ALT_TINT[i0] * w0 + EOTG_ALT_TINT[i1] * w1
						   + EOTG_ALT_TINT[i2] * w2 + EOTG_ALT_TINT[i3] * w3;
			float3 altBand = EOTG_ALT_BAND[i0] * w0 + EOTG_ALT_BAND[i1] * w1
						   + EOTG_ALT_BAND[i2] * w2 + EOTG_ALT_BAND[i3] * w3;
			if ( altBand.z > 0.0f )
			{
				t = lerp( t, altTint, altBand.z * smoothstep( altBand.x, altBand.y, h01 ) );
			}
			return t;
		}

		void EotgTerrainLook( float2 WorldSpacePosXZ, float h01, float soft, out float3 Tint, out float StructureAmount,
							  out float StarDensity, out float StarBright,
							  out float4 ModA, out float4 ModB,
							  out int4 IdxA, out int4 IdxB, out float ShadeAmount,
							  out float Breakup )
		{
			float2 uv = WorldSpacePosXZ * WorldSpaceToDetail;
			float2 tc = uv / DetailTexelSize;			// position measured in texels, so the jitter
														// frequency does not depend on map resolution
			float2 jit = float2( EotgValueNoise( tc * EOTG_BLEND_JITTER_SCALE ),
								 EotgValueNoise( tc * EOTG_BLEND_JITTER_SCALE + 31.7f ) )
					   + 0.5f * float2( EotgValueNoise( tc * EOTG_BLEND_JITTER_SCALE * 2.7f + 11.3f ),
										EotgValueNoise( tc * EOTG_BLEND_JITTER_SCALE * 2.7f + 53.1f ) )
					   - 0.75f;						// two octaves: one alone gives a smooth wobble,
														// the second is what makes the edge ragged
			float2 C = uv + DetailTexelSize * ( 0.5f + jit * EOTG_BLEND_JITTER );
			float4 Idx = PdxTex2D( DetailIndexTexture, C ) * 255.0f;
			float4 W   = PdxTex2D( DetailMaskTexture, C );
			float total = W.x + W.y + W.z + W.w + 1e-5f;

			int i0 = clamp( int( Idx.x + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int i1 = clamp( int( Idx.y + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int i2 = clamp( int( Idx.z + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			int i3 = clamp( int( Idx.w + 0.5f ), 0, EOTG_TERRAIN_COUNT - 1 );
			float w0 = W.x / total, w1 = W.y / total, w2 = W.z / total, w3 = W.w / total;

			Tint = EotgTintAt( C, h01 );
			if ( soft > 0.01f )
			{
				// Four taps on a cross whose ORIENTATION is random per pixel. A fixed cross with
				// this few taps shows as a four-lobed smear; rotating it per pixel makes the
				// neighbouring pixels cover different directions, so together they average to a
				// disc and the transition reads as a smooth fade.
				float2 r = DetailTexelSize * ( EOTG_BLEND_SOFT_R * soft );
				float a = EotgValueNoise( tc * 0.73f ) * 6.2831853f;
				float cs = cos( a ), sn = sin( a );
				float2 d0 = float2( cs, sn ) * r;
				float2 d1 = float2( -sn, cs ) * r;
				float3 sum = Tint * 2.0f;
				sum += EotgTintAt( C + d0, h01 );
				sum += EotgTintAt( C - d0, h01 );
				sum += EotgTintAt( C + d1, h01 );
				sum += EotgTintAt( C - d1, h01 );
				Tint = sum / 6.0f;
			}
			StructureAmount = EOTG_STRUCTURE_AMOUNT[i0] * w0 + EOTG_STRUCTURE_AMOUNT[i1] * w1
							+ EOTG_STRUCTURE_AMOUNT[i2] * w2 + EOTG_STRUCTURE_AMOUNT[i3] * w3;
			StarDensity = EOTG_STAR_DENSITY[i0] * w0 + EOTG_STAR_DENSITY[i1] * w1
						+ EOTG_STAR_DENSITY[i2] * w2 + EOTG_STAR_DENSITY[i3] * w3;
			StarBright = EOTG_STAR_BRIGHT[i0] * w0 + EOTG_STAR_BRIGHT[i1] * w1
					   + EOTG_STAR_BRIGHT[i2] * w2 + EOTG_STAR_BRIGHT[i3] * w3;

			Breakup = EOTG_TILEBREAK[i0] * w0 + EOTG_TILEBREAK[i1] * w1
					+ EOTG_TILEBREAK[i2] * w2 + EOTG_TILEBREAK[i3] * w3;
			ShadeAmount = EOTG_SHADE[i0] * w0 + EOTG_SHADE[i1] * w1
						+ EOTG_SHADE[i2] * w2 + EOTG_SHADE[i3] * w3;

			ModA = float4( 0.0f, 0.0f, 0.0f, 0.0f );
			ModB = float4( 0.0f, 0.0f, 0.0f, 0.0f );
			IdxA = int4( 0, 0, 0, 0 );
			IdxB = int4( 0, 0, 0, 0 );
			float4 BestA = float4( 0.0f, 0.0f, 0.0f, 0.0f );
			float4 BestB = float4( 0.0f, 0.0f, 0.0f, 0.0f );
			EotgAccumMod( i0, w0, ModA, ModB, IdxA, IdxB, BestA, BestB );
			EotgAccumMod( i1, w1, ModA, ModB, IdxA, IdxB, BestA, BestB );
			EotgAccumMod( i2, w2, ModA, ModB, IdxA, IdxB, BestA, BestB );
			EotgAccumMod( i3, w3, ModA, ModB, IdxA, IdxB, BestA, BestB );
		}

		// Replace the greyscale structure with the terrain's own colour.
		float3 EotgApplyTerrain( float3 Diffuse, float3 Tint, float StructureAmount,
			float ModMultiplier, float2 xz, float breakup )
		{
			float g = dot( Diffuse, vec3( 0.3333f ) );
			if ( breakup > 0.0f )
			{
				// One FBM, not two: what breaks the repeat is the PROPORTION of uncorrelated signal
				// mixed in, not how many octaves it has, and this runs on most of the land.
				float n = EotgFbm( xz * EOTG_TILEBREAK_SCALE );
				g = lerp( g, 0.33f + 0.37f * saturate( n / 0.875f ), breakup );
			}
			float structured = lerp( EOTG_STRUCTURE_FLOOR, g,
				saturate( StructureAmount * EOTG_STRUCTURE_SCALE ) );
			return Tint * structured * EOTG_TERRAIN_LEVEL * ModMultiplier;
		}
		// ----------------------------------------------------------------------------------

	]]

	MainCode PixelShader
	{
		Input = "VS_OUTPUT_PDX_TERRAIN"
		Output = "PDX_COLOR"
		Code
		[[

			PDX_MAIN
			{
				float FullColorOverlayFactor = 0.0f;
				bool IsFullyColorOverlay = false;

				const float2 ColorMapCoords = Input.WorldSpacePos.xz * WorldSpaceToTerrain0To1;
				CheckClipNeeded( Input.WorldSpacePos.y, ColorMapCoords, _StartColorOverlayHeightBlend * _EnabledTerrainCulling );

			#ifndef UNDERWATER
				// Skip terrain rendering below the ocean surface.
				if ( Input.WorldSpacePos.y < UNDERWATER_CLIP_OFFSET && _EnabledTerrainCulling > 0.99f)
				{
					return float4( _UnderwaterTerrainColor.rgb, 0.0f );
				}
			#endif

				float3 FlatMap = float3( 0.5f, 0.5f, 0.5f ); // neutral overlay
				#ifdef TERRAIN_FLAT_MAP_LERP
					FlatMap = lerp( FlatMap, PdxTex2D( FlatMapTexture,
						float2( ColorMapCoords.x, 1.0f - ColorMapCoords.y ) ).rgb,
						FlatMapLerp );
				#endif

				#ifdef TERRAIN_COLOR_OVERLAY
					float3 BorderColor;
					float BorderPreLightingBlend;
					float BorderPostLightingBlend;
					GetBorderColorAndBlendGame( Input.WorldSpacePos.xz, FlatMap, BorderColor, BorderPreLightingBlend, BorderPostLightingBlend );

					// MOD(eotg) thin the realm fill so the terrain reads through it. This must happen
					// BEFORE FullColorOverlayFactor is computed: that factor is what lets the shader
					// skip all terrain sampling when the overlay is opaque, and a thinned overlay that
					// still took the skip would blend against terrain that was never shaded.
					#ifdef TERRAIN_FLAT_MAP_LERP
						float EotgPolFade = lerp( EOTG_POLITICAL_OPACITY, 1.0f, FlatMapLerp );
					#else
						float EotgPolFade = EOTG_POLITICAL_OPACITY;
					#endif
					BorderPreLightingBlend  *= EotgPolFade;
					BorderPostLightingBlend *= EotgPolFade;

					FullColorOverlayFactor = BorderPreLightingBlend + BorderPostLightingBlend;
					FullColorOverlayFactor *= _FullyColorOverlayHeightBlend * _EnabledTerrainCulling;
				#endif
				if ( FullColorOverlayFactor > 0.99f )
				{
					IsFullyColorOverlay = true;
				}

				float4 DetailDiffuse = vec4( 0.0f );
				float3 DetailNormal = float3( 0.0f, 1.0f, 0.0f );
				float4 DetailMaterial = vec4( 0.0f );
				float ShadowTerm = 1.0f;
				if( !IsFullyColorOverlay )
				{
					CalculateDetails( Input.WorldSpacePos.xz, DetailDiffuse, DetailNormal, DetailMaterial );
					ShadowTerm = CalculateShadow( Input.ShadowProj, ShadowMap );
				}

				float FogOfWarAlphaValue = PdxTex2D( FogOfWarAlpha, ColorMapCoords).r;
#if defined( PDX_OSX ) && defined( PDX_OPENGL )
				// We're limited to the amount of samplers we can bind at any given time on Mac, so instead
				// we disable the usage of ColorTexture (since its effects are very subtle) and assign a
				// default value here instead.
				float3 ColorMap = float3( vec3( 0.5f ) );
				float ColorDarken = 1.0f;
#else
				float4 ColorMapSample = ToLinear( PdxTex2D( ColorTexture,
						float2( ColorMapCoords.x, 1.0f - ColorMapCoords.y ) ) );
				float ColorDarken = ColorMapSample.a;
				float3 ColorMap = ColorMapSample.rgb;
#endif

				float SnowHighlight = 0.0f;
				float3 Normal = CalculateNormal( Input.WorldSpacePos.xz );
				#ifndef UNDERWATER
					float3 ReorientedNormal = Normal;
					if( !IsFullyColorOverlay )
					{
						float WaterNormalLerp = 0.0f;
						EffectIntensities ConditionData;
						BilinearSampleProvinceEffectsMask( ColorMapCoords, ConditionData );
						ApplyProvinceEffectsTerrain( ConditionData, DetailDiffuse, DetailNormal, DetailMaterial, Input.WorldSpacePos, WaterNormalLerp );

						// Use the property that only water has lower roughness to adjust the terrain normals to face upward.
						float WaterNormalAdjustment = smoothstep( 0.6f, 1.0f, 1 - DetailMaterial.a);
						WaterNormalLerp = max( WaterNormalLerp, WaterNormalAdjustment);
						float3 ReorientedNormal = ReorientNormal(
							lerp( Normal, float3( 0.0f, 1.0f, 0.0f ), WaterNormalLerp ),
							DetailNormal );

						ApplySnowMaterialTerrain( DetailDiffuse, DetailNormal, DetailMaterial, Normal, Input.WorldSpacePos.xz, ColorMapCoords, SnowHighlight );

						if( ConditionData._Drought > 0.0f || SnowHighlight > 0.0f )
						{
							ShadowTerm = lerp( ShadowTerm + 0.4f , ShadowTerm , ShadowTerm );
						}
					}
				#else
					float3 ReorientedNormal = ReorientNormal( Normal, DetailNormal );
				#endif

				float3 EotgTint; float EotgStructure, EotgStarD, EotgStarB;        // MOD(eotg)
				float4 EotgModA, EotgModB; int4 EotgIdxA, EotgIdxB;
				// One height sample for the whole terrain path: the hypsometric ramp, the height
				// gates and the altitude banding all read it.
				float EotgH01 = GetHeightMultisample01( Input.WorldSpacePos.xz, 1.0f );
				float EotgShadeAmt, EotgBreakup;
				float EotgFade = EotgModFade( Input.WorldSpacePos );
				// The colour blur only matters where texels are bigger than a pixel, so it rides
				// the same distance fade as the effects and costs nothing at strategic zoom.
				EotgTerrainLook( Input.WorldSpacePos.xz, EotgH01, EotgFade, EotgTint, EotgStructure,
					EotgStarD, EotgStarB, EotgModA, EotgModB, EotgIdxA, EotgIdxB, EotgShadeAmt, EotgBreakup );
				float3 EotgModAdd; float EotgModMul;                               // MOD(eotg)
				// One gradient for the whole terrain path - relief shading and the slope gates
				// both read it - and only inside the range where either is visible.
				float3 EotgGrad = ( EotgFade > 0.01f )
					? EotgHeightGrad( Input.WorldSpacePos.xz )
					: vec3( 0.0f );
				float4 EotgLens = float4( 0.0f, 0.0f, 0.0f, 0.0f );
				float EotgLensHue = 0.0f;
				if ( EotgFade > 0.01f )
				{
					EotgLens = EotgLensField( Input.WorldSpacePos.xz, EotgLensHue );
				}
				EotgModifierFX( Input.WorldSpacePos, EotgTint, EotgModA, EotgModB,
					EotgIdxA, EotgIdxB, EotgLens, EotgLensHue, EotgFade, EotgH01, EotgGrad,
					EotgModAdd, EotgModMul );
				EotgModMul *= EotgHillshade( EotgGrad, EotgShadeAmt * EotgFade );
				DetailDiffuse.rgb = EotgApplyTerrain( DetailDiffuse.rgb, EotgTint,
					EotgStructure, EotgModMul, Input.WorldSpacePos.xz, EotgBreakup );

				float3 Diffuse = SoftLight( DetailDiffuse.rgb, ColorMap,
					( 1 - DetailMaterial.r ) * COLORMAP_OVERLAY_STRENGTH );

				#ifdef TERRAIN_COLOR_OVERLAY
					LerpBorderColorWithFogOfWarAlphaValue( Diffuse, FogOfWarAlphaValue, BorderColor, BorderPreLightingBlend );
					#ifdef TERRAIN_FLAT_MAP_LERP
						float3 FlatColor;
						// MOD(eotg) the last argument is normally FlatMapLerp, and passing it makes
						// bordercolor.fxh HardLight the realm colour against the desaturated flat map:
						//   BorderColor = HardLight( BorderColor, Desaturated, FlatmapLerp * 0.9 )
						// HardLight against a base below 0.5 MULTIPLIES. Vanilla's flat map is light
						// parchment so that tints the realm; ours is near-black, so it crushed realm
						// colours to nothing at strategic zoom. The coast rim is the one lighter part
						// of our flat map, which is exactly why the colour survived along coastlines
						// and died toward the interior. Passing 0 keeps realms their own colour.
						GetBorderColorAndBlendGameLerp( Input.WorldSpacePos.xz, FlatMap,
							FlatColor, BorderPreLightingBlend, BorderPostLightingBlend,
							0.0f );

						FlatMap = lerp( FlatMap, FlatColor,
							saturate( BorderPreLightingBlend + BorderPostLightingBlend ) );
					#endif
					float4 HighlightColor = GetHighlightColor( ColorMapCoords );
					ApplyHighlightColor( Diffuse, HighlightColor );
					CompensateWhiteHighlightColor( Diffuse, HighlightColor, SnowHighlight );
				#endif

				SMaterialProperties MaterialProps = GetMaterialProperties(
					Diffuse,
					ReorientedNormal,
					DetailMaterial.a,
					DetailMaterial.g,
					DetailMaterial.b
				);

				SLightingProperties LightingProps = GetMapLightingProperties( Input.WorldSpacePos, ShadowTerm );
				#ifdef TERRAIN_FLAT_MAP_LERP
					LightingProps._LightIntensity = lerp( TERRAIN_SUNNY_SUN_COLOR * TERRAIN_SUNNY_SUN_INTENSITY, FlatMapLerpSunIntensity * SunDiffuse, FlatMapLerp );
					LightingProps._CubemapIntensity =  lerp( DefaultEnvironmentCubemapIntensity * TERRAIN_SUNNY_IBL_SCALE, FlatMapLerpCubemapIntensity , FlatMapLerp );
					LightingProps._ToLightDir = lerp( ToTerrainSunnySunDir, ToSunDir , FlatMapLerp );
				#endif

				// Calculate combined shadow mask from clouds and shadow tint
				float CloudMask = 0.0f;
				float3 FinalColor = vec3( 0.0f );
				if( !IsFullyColorOverlay )
				{
					CloudMask = GetCloudShadowMask( Input.WorldSpacePos.xz, FogOfWarAlphaValue );
					// MOD(eotg): unlit terrain. No sun, no shadow tint, no overcast contrast --
					// the albedo is emissive and the procedural stars sit on top of near-black.
					FinalColor = Diffuse * EOTG_TERRAIN_EMISSIVE;
					float3 EotgStarPos = Input.WorldSpacePos;                       // MOD(eotg)
					EotgStarPos.xz += EotgLens.xy;                                 // anomalies bend starlight

					// MOD(eotg) drop everything additive as the paper map comes in.
					//
					// This is where the stars in the ocean at full zoom out were coming from, after
					// three wrong guesses at the water and the surround map. PixelShaderFlatMap draws
					// no stars at all, but it is composited with SurroundMapAlpha, and wherever that
					// goes transparent THIS shader shows through - sea floor included - carrying its
					// star field. A colour-coded diagnostic build settled it: at full zoom out the sea
					// was neither the water shader's red nor the surround's green, so it had to be
					// terrain.
					// Two signals, whichever is stronger. FlatMapLerp alone was not enough: gating on it
					// in the water, the surround and here produced no visible change whatsoever, which
					// means it is not reaching 1 at the zoom the player calls the paper view.
					// GetZoomedInZoomedOutFactor is camera height against ZoomInHeight/ZoomOutHeight,
					// so it always reaches 1 when the camera is all the way out.
					float EotgZoomOut = smoothstep( EOTG_ZOOMOUT_START, EOTG_ZOOMOUT_END,
						GetZoomedInZoomedOutFactor() );
					#ifdef TERRAIN_FLAT_MAP_LERP
						EotgZoomOut = max( EotgZoomOut, saturate( FlatMapLerp ) );
					#endif
					float EotgFlatFade = 1.0f - EotgZoomOut;
					FinalColor += EotgStars( EotgStarPos, EotgStarD, EotgStarB ) * EotgFlatFade;
					FinalColor += EotgModAdd * EotgFlatFade;                        // MOD(eotg)
				}

				#ifdef TERRAIN_COLOR_OVERLAY
				 	float NdotL = saturate( dot( MaterialProps._Normal, LightingProps._ToLightDir ) ) + 1e-5;
					BorderColor *= lerp( max( _WaterZoomedInZoomedOutFactor - 0.4f, 0.4f ), 1.0f, NdotL );
					FinalColor.rgb = lerp( FinalColor.rgb, BorderColor, BorderPostLightingBlend );
					ApplyHighlightColor( FinalColor.rgb, HighlightColor, 0.25f );
					ApplyDiseaseDiffuse( FinalColor, ColorMapCoords );
					ApplyLegendDiffuse( FinalColor, ColorMapCoords );
				#endif

				#ifndef UNDERWATER
					if( !IsFullyColorOverlay )
					{
						FinalColor = ApplyFogOfWar( FinalColor, Input.WorldSpacePos, FogOfWarAlpha );
						FinalColor = ApplyMapDistanceFogWithoutFoW( FinalColor, Input.WorldSpacePos );
					}	
				#endif

				#ifdef TERRAIN_FLAT_MAP_LERP
					float Blend = CalculatePaperTransitionBlend( ColorMapCoords, FlatMapLerp );
					FlatMap = ApplyFlatMapBrightnessAdjustment( FlatMap );
					FinalColor = lerp( FinalColor, FlatMap, Blend );
				#endif

				FinalColor *= EotgEdgeFade( ColorMapCoords );   // MOD(eotg)

				float Alpha = 1.0f;
				#ifdef UNDERWATER
					Alpha = CompressWorldSpace( Input.WorldSpacePos );
				#endif

				#ifdef TERRAIN_DEBUG
					TerrainDebug( FinalColor, Input.WorldSpacePos );
				#endif
				// DebugReturn( FinalColor, MaterialProps, LightingProps, EnvironmentMap );

				return float4( FinalColor, Alpha );
			}
		]]
	}

	MainCode PixelShaderLowSpec
	{
		Input = "VS_OUTPUT_PDX_TERRAIN_LOW_SPEC"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				float FullColorOverlayFactor = 0.0f;
				bool IsFullyColorOverlay = false;

				const float2 ColorMapCoords = Input.WorldSpacePos.xz * WorldSpaceToTerrain0To1;
				CheckClipNeeded( Input.WorldSpacePos.y, ColorMapCoords, _StartColorOverlayHeightBlend);

				float3 DetailDiffuse = Input.DetailDiffuse;
				float4 DetailMaterial = Input.DetailMaterial;
				float3 ColorMap = Input.ColorMap;
				float3 FlatMap = Input.FlatMap;
				float3 Normal = Input.Normal;

				#ifdef TERRAIN_COLOR_OVERLAY
					float3 BorderColor;
					float BorderPreLightingBlend;
					float BorderPostLightingBlend;
					GetBorderColorAndBlendGame( Input.WorldSpacePos.xz, FlatMap, BorderColor, BorderPreLightingBlend, BorderPostLightingBlend );

					// MOD(eotg) thin the realm fill so the terrain reads through it. This must happen
					// BEFORE FullColorOverlayFactor is computed: that factor is what lets the shader
					// skip all terrain sampling when the overlay is opaque, and a thinned overlay that
					// still took the skip would blend against terrain that was never shaded.
					#ifdef TERRAIN_FLAT_MAP_LERP
						float EotgPolFade = lerp( EOTG_POLITICAL_OPACITY, 1.0f, FlatMapLerp );
					#else
						float EotgPolFade = EOTG_POLITICAL_OPACITY;
					#endif
					BorderPreLightingBlend  *= EotgPolFade;
					BorderPostLightingBlend *= EotgPolFade;

					FullColorOverlayFactor = BorderPreLightingBlend + BorderPostLightingBlend;
					FullColorOverlayFactor *= _FullyColorOverlayHeightBlend * _EnabledTerrainCulling;
				#endif
				if ( FullColorOverlayFactor > 0.99f )
				{
					IsFullyColorOverlay = true;
				}

				float SnowHighlight = 0.0f;
				#ifndef UNDERWATER
					DetailDiffuse = ApplyDynamicMasksDiffuse( DetailDiffuse, Normal, ColorMapCoords );
				#endif

				float3 EotgTint; float EotgStructure, EotgStarD, EotgStarB;        // MOD(eotg)
				float4 EotgModA, EotgModB; int4 EotgIdxA, EotgIdxB;
				// One height sample for the whole terrain path: the hypsometric ramp, the height
				// gates and the altitude banding all read it.
				float EotgH01 = GetHeightMultisample01( Input.WorldSpacePos.xz, 1.0f );
				float EotgShadeAmt, EotgBreakup;
				float EotgFade = EotgModFade( Input.WorldSpacePos );
				// The colour blur only matters where texels are bigger than a pixel, so it rides
				// the same distance fade as the effects and costs nothing at strategic zoom.
				EotgTerrainLook( Input.WorldSpacePos.xz, EotgH01, EotgFade, EotgTint, EotgStructure,
					EotgStarD, EotgStarB, EotgModA, EotgModB, EotgIdxA, EotgIdxB, EotgShadeAmt, EotgBreakup );
				float3 EotgModAdd; float EotgModMul;                               // MOD(eotg)
				// One gradient for the whole terrain path - relief shading and the slope gates
				// both read it - and only inside the range where either is visible.
				float3 EotgGrad = ( EotgFade > 0.01f )
					? EotgHeightGrad( Input.WorldSpacePos.xz )
					: vec3( 0.0f );
				float4 EotgLens = float4( 0.0f, 0.0f, 0.0f, 0.0f );
				float EotgLensHue = 0.0f;
				if ( EotgFade > 0.01f )
				{
					EotgLens = EotgLensField( Input.WorldSpacePos.xz, EotgLensHue );
				}
				EotgModifierFX( Input.WorldSpacePos, EotgTint, EotgModA, EotgModB,
					EotgIdxA, EotgIdxB, EotgLens, EotgLensHue, EotgFade, EotgH01, EotgGrad,
					EotgModAdd, EotgModMul );
				EotgModMul *= EotgHillshade( EotgGrad, EotgShadeAmt * EotgFade );
				DetailDiffuse.rgb = EotgApplyTerrain( DetailDiffuse.rgb, EotgTint,
					EotgStructure, EotgModMul, Input.WorldSpacePos.xz, EotgBreakup );
				float3 Diffuse = SoftLight( DetailDiffuse.rgb, ColorMap, ( 1 - DetailMaterial.r ) * COLORMAP_OVERLAY_STRENGTH );

				#ifdef TERRAIN_COLOR_OVERLAY
					float FogOfWarAlphaValue = PdxTex2D( FogOfWarAlpha, ColorMapCoords).r;
					LerpBorderColorWithFogOfWarAlphaValue( Diffuse, FogOfWarAlphaValue, BorderColor, BorderPreLightingBlend );

					#ifdef TERRAIN_FLAT_MAP_LERP
						float3 FlatColor;
						// MOD(eotg) the last argument is normally FlatMapLerp, and passing it makes
						// bordercolor.fxh HardLight the realm colour against the desaturated flat map:
						//   BorderColor = HardLight( BorderColor, Desaturated, FlatmapLerp * 0.9 )
						// HardLight against a base below 0.5 MULTIPLIES. Vanilla's flat map is light
						// parchment so that tints the realm; ours is near-black, so it crushed realm
						// colours to nothing at strategic zoom. The coast rim is the one lighter part
						// of our flat map, which is exactly why the colour survived along coastlines
						// and died toward the interior. Passing 0 keeps realms their own colour.
						GetBorderColorAndBlendGameLerp( Input.WorldSpacePos.xz, FlatMap,
							FlatColor, BorderPreLightingBlend, BorderPostLightingBlend,
							0.0f );
						FlatMap = lerp( FlatMap, FlatColor,
							saturate( BorderPreLightingBlend + BorderPostLightingBlend ) );
					#endif
				#endif

				float3 FinalColor = vec3( 0.0f );
				SMaterialProperties MaterialProps = GetMaterialProperties(
					Diffuse,
					Normal,
					DetailMaterial.a,
					DetailMaterial.g,
					DetailMaterial.b
				);
				float ShadowTerm = 1.0f;
				SLightingProperties LightingProps = GetMapLightingProperties( Input.WorldSpacePos, ShadowTerm );
				if( !IsFullyColorOverlay )
				{
					FinalColor = Diffuse * EOTG_TERRAIN_EMISSIVE;                          // MOD(eotg) unlit
					float3 EotgStarPos = Input.WorldSpacePos;                       // MOD(eotg)
					EotgStarPos.xz += EotgLens.xy;                                 // anomalies bend starlight

					// MOD(eotg) drop everything additive as the paper map comes in.
					//
					// This is where the stars in the ocean at full zoom out were coming from, after
					// three wrong guesses at the water and the surround map. PixelShaderFlatMap draws
					// no stars at all, but it is composited with SurroundMapAlpha, and wherever that
					// goes transparent THIS shader shows through - sea floor included - carrying its
					// star field. A colour-coded diagnostic build settled it: at full zoom out the sea
					// was neither the water shader's red nor the surround's green, so it had to be
					// terrain.
					// Two signals, whichever is stronger. FlatMapLerp alone was not enough: gating on it
					// in the water, the surround and here produced no visible change whatsoever, which
					// means it is not reaching 1 at the zoom the player calls the paper view.
					// GetZoomedInZoomedOutFactor is camera height against ZoomInHeight/ZoomOutHeight,
					// so it always reaches 1 when the camera is all the way out.
					float EotgZoomOut = smoothstep( EOTG_ZOOMOUT_START, EOTG_ZOOMOUT_END,
						GetZoomedInZoomedOutFactor() );
					#ifdef TERRAIN_FLAT_MAP_LERP
						EotgZoomOut = max( EotgZoomOut, saturate( FlatMapLerp ) );
					#endif
					float EotgFlatFade = 1.0f - EotgZoomOut;
					FinalColor += EotgStars( EotgStarPos, EotgStarD, EotgStarB ) * EotgFlatFade;
					FinalColor += EotgModAdd * EotgFlatFade;                        // MOD(eotg)
				}
				#ifndef UNDERWATER
					if( !IsFullyColorOverlay )
					{
						FinalColor = ApplyFogOfWar( FinalColor, Input.WorldSpacePos, FogOfWarAlpha );
						FinalColor = ApplyMapDistanceFog( FinalColor, Input.WorldSpacePos, FogOfWarAlpha );
					}
				#endif

				#ifdef TERRAIN_COLOR_OVERLAY
					FinalColor.rgb = lerp( FinalColor.rgb, BorderColor, BorderPostLightingBlend );
				#endif

				#ifdef TERRAIN_COLOR_OVERLAY
					float4 HighlightColor = GetHighlightColor( ColorMapCoords );
					ApplyHighlightColor( FinalColor.rgb, HighlightColor );
					CompensateWhiteHighlightColor( FinalColor.rgb, HighlightColor, SnowHighlight );
				#endif

				#ifdef TERRAIN_FLAT_MAP_LERP
					FinalColor = lerp( FinalColor, FlatMap, FlatMapLerp );
				#endif

				FinalColor *= EotgEdgeFade( ColorMapCoords );   // MOD(eotg)

				float Alpha = 1.0f;
				#ifdef UNDERWATER
					Alpha = CompressWorldSpace( Input.WorldSpacePos );
				#endif

				#ifdef TERRAIN_DEBUG
					TerrainDebug( FinalColor, Input.WorldSpacePos );
				#endif

				DebugReturn( FinalColor, MaterialProps, LightingProps, EnvironmentMap );
				return float4( FinalColor, Alpha );
			}
		]]
	}

	MainCode PixelShaderFlatMap
	{
		Input = "VS_OUTPUT_PDX_TERRAIN"
		Output = "PDX_COLOR"
		Code
		[[
			PDX_MAIN
			{
				#ifdef TERRAIN_SKIRT
					return float4( 0, 0, 0, 0 );
				#endif

				clip( vec2( 1.0f ) - Input.WorldSpacePos.xz * WorldSpaceToTerrain0To1 );

				float2 ColorMapCoords = Input.WorldSpacePos.xz * WorldSpaceToTerrain0To1;
				float3 FlatMap = PdxTex2D( FlatMapTexture, float2( ColorMapCoords.x, 1.0 - ColorMapCoords.y ) ).rgb;


				#ifdef TERRAIN_COLOR_OVERLAY
					float3 BorderColor;
					float BorderPreLightingBlend;
					float BorderPostLightingBlend;

					// MOD(eotg) 1.0 here fed the same HardLight crush described above; see the note
					// in PixelShader. This is the one that actually draws at full zoom out.
					GetBorderColorAndBlendGameLerp( Input.WorldSpacePos.xz, FlatMap,
						BorderColor, BorderPreLightingBlend, BorderPostLightingBlend,
						0.0f );

					FlatMap = lerp( FlatMap, BorderColor,
						saturate( BorderPreLightingBlend + BorderPostLightingBlend ) );

				#endif

				float3 FinalColor = FlatMap;
				#ifdef TERRAIN_COLOR_OVERLAY
					float4 HighlightColor = GetHighlightColor( ColorMapCoords );
					ApplyHighlightColor( FinalColor, HighlightColor, 0.5f );
				#endif

				#ifdef TERRAIN_DEBUG
					TerrainDebug( FinalColor, Input.WorldSpacePos );
				#endif

				FinalColor = ApplyFlatMapBrightnessAdjustment( FinalColor );

				// Make flatmap transparent based on the SurroundFlatMapMask
				FinalColor *= EotgEdgeFade( ColorMapCoords );   // MOD(eotg) same fade at strategic zoom

				float SurroundMapAlpha = 1 - PdxTex2D( SurroundFlatMapMask, float2( ColorMapCoords.x, 1.0 - ColorMapCoords.y ) ).b;
				SurroundMapAlpha *= FlatMapLerp;

				return float4( FinalColor, SurroundMapAlpha );
			}
		]]
	}
}


Effect PdxTerrain
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShader"

	Defines = { "TERRAIN_FLAT_MAP_LERP" }
}

Effect PdxTerrainLowSpec
{
	VertexShader = "VertexShaderLowSpec"
	PixelShader = "PixelShaderLowSpec"
}

Effect PdxTerrainSkirt
{
	VertexShader = "VertexShaderSkirt"
	PixelShader = "PixelShader"
	Defines = { "TERRAIN_SKIRT" }
}

Effect PdxTerrainLowSpecSkirt
{
	VertexShader = "VertexShaderLowSpecSkirt"
	PixelShader = "PixelShaderLowSpec"
	Defines = { "TERRAIN_SKIRT" }
}

### FlatMap Effects

BlendState BlendStateAlpha
{
	BlendEnable = yes
	SourceBlend = "SRC_ALPHA"
	DestBlend = "INV_SRC_ALPHA"
}

Effect PdxTerrainFlat
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderFlatMap"
	BlendState = BlendStateAlpha

	Defines = { "TERRAIN_FLAT_MAP" "TERRAIN_FLATMAP_LIGHTING" }
}

Effect PdxTerrainFlatSkirt
{
	VertexShader = "VertexShaderSkirt"
	PixelShader = "PixelShaderFlatMap"
	BlendState = BlendStateAlpha

	Defines = { "TERRAIN_FLAT_MAP" "TERRAIN_SKIRT" }
}

# Low Spec flat map the same as regular effect
Effect PdxTerrainFlatLowSpec
{
	VertexShader = "VertexShader"
	PixelShader = "PixelShaderFlatMap"
	BlendState = BlendStateAlpha

	Defines = { "TERRAIN_FLAT_MAP" }
}

Effect PdxTerrainFlatLowSpecSkirt
{
	VertexShader = "VertexShaderSkirt"
	PixelShader = "PixelShaderFlatMap"
	BlendState = BlendStateAlpha

	Defines = { "TERRAIN_FLAT_MAP" "TERRAIN_SKIRT" }
}
