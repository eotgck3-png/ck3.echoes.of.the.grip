# MOD(eotg) full-file override of game/gfx/FX/paper_transition.fxh (CK3 1.19.0.6)
# Vanilla wipes to the paper map through a torn-paper mask. The star chart just cross-fades.
# Sampler and function signature are kept so pdxterrain / pdxwater callers compile unchanged.

PixelShader = {
    TextureSampler PaperTearMask
	{
		Index = 8
		MagFilter = "Linear"
		MinFilter = "Linear"
		MipFilter = "Linear"
		SampleModeU = "Wrap"
		SampleModeV = "Wrap"
		File = "gfx/map/terrain/flat_maps/paper_tear_mask.dds"
		srgb = yes
	}

	Code
	[[
		float CalculatePaperTransitionBlend(
			float2 UV,
			float TransitionAmount,
			float2 MainUVScale = float2( 12.0f, 6.0f ),
			float2 DetailUVScale = float2( 16.0f, 8.0f ),
			float2 LargeUVScale = float2( 1.0f, 1.0f ) )
		{
			return smoothstep( 0.0f, 1.0f, TransitionAmount );
		}
	]]
}
