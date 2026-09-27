# MOD(eotg) override of game/gfx/FX/surroundmap.shader (CK3 1.19.0.6): the area beyond the map edge is
# void with faint stars instead of parallax clouds / paper table. Vertex shader, samplers and helpers are vanilla.

Includes = {
	"cw/camera.fxh"
	"cw/utility.fxh"
	"standardfuncsgfx.fxh"
	"jomini/jomini_fog.fxh"
	"jomini/jomini_lighting.fxh"
	"lowspec.fxh"
}


ConstantBuffer( PdxConstantBuffer0 )
{	
	float2	BaseCloudTileFactor;
	float2	BaseCloudScrolling;
	float2	Cloud1TileFactor; 
	float2	Cloud1Scrolling;
	float2	Cloud2TileFactor;
	float2	Cloud2Scrolling;
	float	BaseCloudStrength;
	float	Cloud1Strength;
	float	Cloud2Strength;
	float	CloudHeight;

	float3	LowCloudColor;
	float	PixelSize;
	float3	HighCloudColor;
	float	MinCloudAlpha;
	float3	ShadowColor;
	float	MaxCloudAlpha;
	
	float2	TileFactor;
	float	ParallaxStrength;
	float	ParallaxFadeFactor;
}

VertexStruct VS_OUTPUT
{
    float4 position			: PDX_POSITION;
	float2 uv				: TEXCOORD0;
	float3 WorldSpacePos	: TEXCOORD1;
};


VertexShader = {

	VertexStruct VS_INPUT
	{
		float2 position	: POSITION;
	};
	
	MainCode VS_surroundmap
	{
		Input = "VS_INPUT"
		Output = "VS_OUTPUT"
		Code
		[[
			PDX_MAIN
			{			
				VS_OUTPUT VertexOut;
				
				float3 WorldSpacePos = float3( Input.position.x, FlatMapHeight, Input.position.y );
				#ifndef SURROUND_SHADOW
					WorldSpacePos.y += CloudHeight * ( 1.0 - FlatMapLerp );
				#endif
				VertexOut.position = FixProjectionAndMul( ViewProjectionMatrix, float4( WorldSpacePos, 1.0 ) );
				VertexOut.uv = Input.position / MapSize;
				VertexOut.uv.y = 1.0 - VertexOut.uv.y;
				
				VertexOut.WorldSpacePos = WorldSpacePos;

				return VertexOut;
			}
		]]
	}
}


PixelShader =
{
	TextureSampler SurroundMask
	{
		Ref = PdxTexture0
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Border"
		SampleModeV = "Border"
		Border_Color = { 1 1 1 1 }
		File = "gfx/map/surround_map/surround_mask.dds"
	}
	TextureSampler SurroundTile
	{
		Ref = PdxTexture1
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
		File = "gfx/map/surround_map/surround_tile.dds"
		srgb = yes
	}
	TextureSampler CloudTexture
	{
		Ref = PdxTexture2
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
		#File = "gfx/map/surround_map/test2.dds"
	}
	TextureSampler BlackMask
	{
		Ref = PdxTexture3
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Clamp"
		SampleModeV = "Clamp"
		File = "gfx/map/surround_map/surround_fade.dds"
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
	
	Code
	[[
		// MOD(eotg) master switch for the star field beyond the map edge. Off - the stars are
		// sized in world units, so zooming in over open sea magnifies each into a large soft blob.
		// Declared once here because every pixel shader in this file needs it.
		#define EOTG_SURROUND_STARS 0

		// TEMPORARY DIAGNOSTIC - set back to 0.
		#define EOTG_DIAG_SURROUND 0
		float4 GetFlatMapSurround( float2 UV )
		{				
			float Mask = PdxTex2D( SurroundMask, UV ).b;

			// We no longer use the surround 'woodgrain' tiling (keeping this here for some mods backward compat hint)
			// float3 Tile = PdxTex2D( SurroundTile, UV * TileFactor ).rgb;
			float3 Tile = float3(0, 0, 0);
			
			return float4( Tile, Mask );
		}
		
		float3 CalculateNormal( PdxTextureSampler2D Texture, float2 UV, float Scale )
		{
			float3 n;
			
			//float4 h;
			//h[0] = PdxTex2DLod0( Texture, UV + float2(-PixelSize, 0) ).r;
			//h[1] = PdxTex2DLod0( Texture, UV + float2(PixelSize, 0) ).r;
			//h[2] = PdxTex2DLod0( Texture, UV + float2(0, -PixelSize) ).r;
			//h[3] = PdxTex2DLod0( Texture, UV + float2(0, PixelSize) ).r;
			//
			//n.z = h[3] - h[2];
			//n.x = h[0] - h[1];
			//n.y = Scale;
			
			
			float h00 = PdxTex2DLod0( Texture, UV + float2(-PixelSize, -PixelSize) ).r;
			float h10 = PdxTex2DLod0( Texture, UV + float2(PixelSize, -PixelSize) ).r;
			float h01 = PdxTex2DLod0( Texture, UV + float2(-PixelSize, PixelSize) ).r;
			
			n.z = h01 - h00;
			n.x = h00 - h10;
			n.y = Scale;
			
			return normalize(n);
		}
		
		float2 CalculateParallaxOffset( float3 TangentSpaceCameraDir, float2 UV, float ParallaxScale )
		{
			float Height = 1.0 - PdxTex2DLod0( CloudTexture, UV ).r;
			
			float Scale = Height / TangentSpaceCameraDir.y;
			Scale = Height;
			
			float2 Offset = -TangentSpaceCameraDir.xz * Scale * ParallaxStrength;
			return Offset * ParallaxScale;
		}
		
		float2 CalculateParallaxOffsetSteep( float3 TangentSpaceCameraDir, float2 UV, float ParallaxScale )
		{
			static const float MinNumLayers = 2;
			static const float MaxNumLayers = 10;
			
			float NumLayers = lerp( MaxNumLayers, MinNumLayers, TangentSpaceCameraDir.y );
			float LayerHeight = 1.0 / NumLayers;
			float CurrentHeight = 0.0;
			
			float2 Offset = vec2(0.0);
			float2 DV = -TangentSpaceCameraDir.xz * ParallaxStrength / TangentSpaceCameraDir.y / NumLayers;
			//float2 DV = -TangentSpaceCameraDir.xz * ParallaxStrength / NumLayers;
			
			float Height = 1.0 - PdxTex2DLod0( CloudTexture, UV ).r;
			
			while( Height > CurrentHeight )
			{
				CurrentHeight += LayerHeight;
				Offset += DV;
				
				Height = 1.0 - PdxTex2DLod0( CloudTexture, UV + Offset ).r;
			}
			
			float2 PrevOffset = Offset - DV;
			float PrevHeight = 1.0 - PdxTex2DLod0( CloudTexture, UV + PrevOffset ).r - CurrentHeight + LayerHeight;
			
			float NextHeight = Height - CurrentHeight;
			
			float Weight = NextHeight / (NextHeight - PrevHeight);
			Offset = lerp( Offset, PrevOffset, Weight );
			
			return Offset * ParallaxScale;
		}
	]]

	MainCode PS_surroundmap
	{
		Input = "VS_OUTPUT"
		Output = "PDX_COLOR"
		Code
		[[
			// MOD(eotg) the space beyond the map edge: black with a faint star field, no clouds, no table
			float EotgHash( float2 p )
			{
				return frac( sin( dot( p, float2( 127.1f, 311.7f ) ) ) * 43758.5453f );
			}
			PDX_MAIN
			{
				float2 UV = Input.uv;
				float3 SurroundMaskChannels = PdxTex2D( SurroundMask, UV ).rgb;
				float Mask = SurroundMaskChannels.g;	// 0 over the map itself

				// Two star layers: soft dots at a random spot inside each cell, big cells so they read at any zoom
				//
				// "at any zoom" was the bug. The cells are deliberately zoom-independent, so the stars
				// stayed at full strength under the paper map and speckled the whole view. Nothing else
				// in this file looks at zoom, which is why the water-side fade did not touch them.
				// Off, for the same reason as the void star field in pdxwater.shader: these are sized
				// in world units, so zooming in over open sea magnifies each one into a large soft
				// blob. Beyond the map edge is now plain black. Set EOTG_SURROUND_STARS to 1 to restore.
				#if EOTG_SURROUND_STARS
					float EotgStarFade = 1.0f - saturate( FlatMapLerp );
				#else
					float EotgStarFade = 0.0f;
				#endif
				float3 Color = float3( 0.002f, 0.002f, 0.003f );
				float2 cellSizes[2]; cellSizes[0] = float2( 40.0f, 0.985f ); cellSizes[1] = float2( 14.0f, 0.975f );
				for ( int i = 0; i < 2; i++ )
				{
					float2 p = Input.WorldSpacePos.xz / cellSizes[i].x;
					float2 cell = floor( p );
					float h  = EotgHash( cell + float( i ) * 31.0f );
					float h2 = EotgHash( cell + 17.0f + float( i ) * 31.0f );
					float2 centre = cell + float2( EotgHash( cell + 3.0f ), EotgHash( cell + 7.0f ) ) * 0.8f + 0.1f;
					float d = length( p - centre ) * cellSizes[i].x;	// world-unit distance to the star
					float radius = lerp( 1.0f, 3.0f, h2 ) * ( i == 0 ? 1.6f : 1.0f );
					float spot = exp( -d * d / ( radius * radius ) );
					float on = step( cellSizes[i].y, h );
					float twinkle = 0.6f + 0.4f * sin( GlobalTime * ( 0.4f + h2 * 1.2f ) + h2 * 6.28f );
					Color += float3( 1.0f, 0.94f, 0.82f ) * spot * on * twinkle * ( i == 0 ? 1.2f : 0.6f ) * EotgStarFade;
				}

				#if EOTG_DIAG_SURROUND
					return float4( 0.0f, 1.0f, 0.0f, saturate( Mask ) );
				#endif
				return float4( Color, saturate( Mask ) );
			}
		]]
	}
	
	MainCode PS_surroundmapLowSpec
	{
		Input = "VS_OUTPUT"
		Output = "PDX_COLOR"
		Code
		[[
			// MOD(eotg) the space beyond the map edge: black with a faint star field, no clouds, no table
			float EotgHash( float2 p )
			{
				return frac( sin( dot( p, float2( 127.1f, 311.7f ) ) ) * 43758.5453f );
			}
			PDX_MAIN
			{
				float2 UV = Input.uv;
				float3 SurroundMaskChannels = PdxTex2D( SurroundMask, UV ).rgb;
				float Mask = SurroundMaskChannels.g;	// 0 over the map itself

				// Two star layers: soft dots at a random spot inside each cell, big cells so they read at any zoom
				//
				// "at any zoom" was the bug. The cells are deliberately zoom-independent, so the stars
				// stayed at full strength under the paper map and speckled the whole view. Nothing else
				// in this file looks at zoom, which is why the water-side fade did not touch them.
				// Off, for the same reason as the void star field in pdxwater.shader: these are sized
				// in world units, so zooming in over open sea magnifies each one into a large soft
				// blob. Beyond the map edge is now plain black. Set EOTG_SURROUND_STARS to 1 to restore.
				#if EOTG_SURROUND_STARS
					float EotgStarFade = 1.0f - saturate( FlatMapLerp );
				#else
					float EotgStarFade = 0.0f;
				#endif
				float3 Color = float3( 0.002f, 0.002f, 0.003f );
				float2 cellSizes[2]; cellSizes[0] = float2( 40.0f, 0.985f ); cellSizes[1] = float2( 14.0f, 0.975f );
				for ( int i = 0; i < 2; i++ )
				{
					float2 p = Input.WorldSpacePos.xz / cellSizes[i].x;
					float2 cell = floor( p );
					float h  = EotgHash( cell + float( i ) * 31.0f );
					float h2 = EotgHash( cell + 17.0f + float( i ) * 31.0f );
					float2 centre = cell + float2( EotgHash( cell + 3.0f ), EotgHash( cell + 7.0f ) ) * 0.8f + 0.1f;
					float d = length( p - centre ) * cellSizes[i].x;	// world-unit distance to the star
					float radius = lerp( 1.0f, 3.0f, h2 ) * ( i == 0 ? 1.6f : 1.0f );
					float spot = exp( -d * d / ( radius * radius ) );
					float on = step( cellSizes[i].y, h );
					float twinkle = 0.6f + 0.4f * sin( GlobalTime * ( 0.4f + h2 * 1.2f ) + h2 * 6.28f );
					Color += float3( 1.0f, 0.94f, 0.82f ) * spot * on * twinkle * ( i == 0 ? 1.2f : 0.6f ) * EotgStarFade;
				}

				#if EOTG_DIAG_SURROUND
					return float4( 0.0f, 1.0f, 0.0f, saturate( Mask ) );
				#endif
				return float4( Color, saturate( Mask ) );
			}
		]]
	}
	
	MainCode PS_surroundmap_shadow
	{
		Input = "VS_OUTPUT"
		Output = "PDX_COLOR"
		Code
		[[			
			PDX_MAIN
			{
				float2 UV = Input.uv;
				float Mask = PdxTex2D( SurroundMask, UV ).r;
			
				return float4( ShadowColor, Mask * ( 1.0 - FlatMapLerp ) );
			}
		]]
	}
	
	MainCode PS_surroundmap_flat
	{
		Input = "VS_OUTPUT"
		Output = "PDX_COLOR"
		Code
		[[
			// MOD(eotg) the space beyond the map edge: black with a faint star field, no clouds, no table
			float EotgHash( float2 p )
			{
				return frac( sin( dot( p, float2( 127.1f, 311.7f ) ) ) * 43758.5453f );
			}
			PDX_MAIN
			{
				float2 UV = Input.uv;
				float3 SurroundMaskChannels = PdxTex2D( SurroundMask, UV ).rgb;
				float Mask = SurroundMaskChannels.g;	// 0 over the map itself

				// Two star layers: soft dots at a random spot inside each cell, big cells so they read at any zoom
				//
				// "at any zoom" was the bug. The cells are deliberately zoom-independent, so the stars
				// stayed at full strength under the paper map and speckled the whole view. Nothing else
				// in this file looks at zoom, which is why the water-side fade did not touch them.
				// Off, for the same reason as the void star field in pdxwater.shader: these are sized
				// in world units, so zooming in over open sea magnifies each one into a large soft
				// blob. Beyond the map edge is now plain black. Set EOTG_SURROUND_STARS to 1 to restore.
				#if EOTG_SURROUND_STARS
					float EotgStarFade = 1.0f - saturate( FlatMapLerp );
				#else
					float EotgStarFade = 0.0f;
				#endif
				float3 Color = float3( 0.002f, 0.002f, 0.003f );
				float2 cellSizes[2]; cellSizes[0] = float2( 40.0f, 0.985f ); cellSizes[1] = float2( 14.0f, 0.975f );
				for ( int i = 0; i < 2; i++ )
				{
					float2 p = Input.WorldSpacePos.xz / cellSizes[i].x;
					float2 cell = floor( p );
					float h  = EotgHash( cell + float( i ) * 31.0f );
					float h2 = EotgHash( cell + 17.0f + float( i ) * 31.0f );
					float2 centre = cell + float2( EotgHash( cell + 3.0f ), EotgHash( cell + 7.0f ) ) * 0.8f + 0.1f;
					float d = length( p - centre ) * cellSizes[i].x;	// world-unit distance to the star
					float radius = lerp( 1.0f, 3.0f, h2 ) * ( i == 0 ? 1.6f : 1.0f );
					float spot = exp( -d * d / ( radius * radius ) );
					float on = step( cellSizes[i].y, h );
					float twinkle = 0.6f + 0.4f * sin( GlobalTime * ( 0.4f + h2 * 1.2f ) + h2 * 6.28f );
					Color += float3( 1.0f, 0.94f, 0.82f ) * spot * on * twinkle * ( i == 0 ? 1.2f : 0.6f ) * EotgStarFade;
				}

				#if EOTG_DIAG_SURROUND
					return float4( 0.0f, 0.6f, 1.0f, saturate( Mask ) * FlatMapLerp );
				#endif
				return float4( Color, saturate( Mask ) * FlatMapLerp );
			}
		]]
	}
}


BlendState BlendState
{
	BlendEnable = yes
	SourceBlend = "src_alpha"
	DestBlend = "inv_src_alpha"
	WriteMask = "RED|GREEN|BLUE"
}

DepthStencilState DepthStencilState
{
	DepthEnable = no
	DepthWriteEnable = no
}

RasterizerState RasterizerState
{
	frontccw = yes
}


Effect surroundmap
{
	VertexShader = VS_surroundmap
	PixelShader = PS_surroundmap
}

Effect surroundmapLowSpec
{
	VertexShader = VS_surroundmap
	PixelShader = PS_surroundmapLowSpec
}

Effect surroundmap_shadow
{
	VertexShader = VS_surroundmap
	PixelShader = PS_surroundmap_shadow
	
	Defines = { "SURROUND_SHADOW" }
}

Effect surroundmap_flat
{
	VertexShader = VS_surroundmap
	PixelShader = PS_surroundmap_flat
}