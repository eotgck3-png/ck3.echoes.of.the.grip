# MOD(eotg) Stellar Rivers - full-file override of game/gfx/FX/river_bottom.shader (CK3 1.19.0.6)
# Energy streams have no riverbed. This pass is kept (the engine still issues the draw call)
# but discards every pixel so nothing is written to the refraction buffer.

Includes = {
	"cw/shadow.fxh"
	"cw/utility.fxh"
	"cw/camera.fxh"
	"jomini/jomini_lighting.fxh"
	"jomini/jomini_water.fxh"
	"jomini/jomini_river_bottom.fxh"
	"standardfuncsgfx.fxh"
}

PixelShader =
{
	MainCode PS_underwater
	{
		Input = "VS_OUTPUT_RIVER"
		Output = "PS_RIVER_BOTTOM_OUT"
		Code
		[[
			PDX_MAIN
			{
				clip( -1.0f );	// MOD(eotg) discard: no riverbed under an energy stream

				PS_RIVER_BOTTOM_OUT Out;
				Out.Color = vec4( 0.0f );
				Out.Blend = vec4( 0.0f );
				return Out;
			}
		]]
	}
}

Effect river_underwater
{
	VertexShader = "VertexShader"
	PixelShader = "PS_underwater"
}
