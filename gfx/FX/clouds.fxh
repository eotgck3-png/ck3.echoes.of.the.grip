# MOD(eotg) full-file override of game/gfx/FX/clouds.fxh (CK3 1.19.0.6)
# No drifting cloud shadows on a star chart. Both GetCloudShadowMask signatures are kept so every
# vanilla caller (terrain, water, borders, meshes, rivers) compiles unchanged and gets 0.

Includes = {
	"cw/camera.fxh"
	"cw/random.fxh"
	"jomini/jomini_fog_of_war.fxh"
	"jomini/jomini_water.fxh"
	"standardfuncsgfx.fxh"
}

PixelShader = {
	Code
	[[
		float GetCloudShadowMask( in float2 Coordinate, float FogOfWarAlphaValue )
		{
			return 0.0f;
		}
		float GetCloudShadowMask( in float2 Coordinate )
		{
			return 0.0f;
		}
	]]
}
