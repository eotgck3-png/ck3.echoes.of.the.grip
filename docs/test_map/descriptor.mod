# TEST MAP: not mod content. Sub-mod descriptor; install with install.py (see README.md).
# Load order: Echoes of the Grip, then EotG Test Map (the dependency below makes the launcher sort it).
version="0.1.0"
tags={
	"Map"
}
name="EotG Test Map"
supported_version="1.20.*"
dependencies={
	"Echoes of the Grip"
}

# replace_path: only folders this sub-mod ships (CLAUDE.md invariant 3, v1 lesson 3). Each one holds
# vanilla content keyed to vanilla titles, provinces or characters that do not exist on this map.
replace_path="common/landed_titles"						# vanilla 00_landed_titles + 01_japan..07_pam_*: the vanilla title tree
replace_path="common/province_terrain"					# vanilla 01_province_properties.txt sets winter bias on vanilla province ids (to ~13000)
replace_path="common/bookmarks/bookmarks"				# vanilla bookmarks name vanilla history_ids and titles
replace_path="common/bookmarks/groups"					# vanilla groups would sit empty; ours holds the 866 bookmark
replace_path="common/bookmarks/challenge_characters"	# vanilla challenge characters name vanilla characters and titles (c_kerak, ...)
replace_path="history/faiths"							# vanilla faith history creates rites whose founder titles do not exist here (crash)
replace_path="history/characters"						# vanilla characters
replace_path="history/titles"							# vanilla holders of vanilla titles
replace_path="history/provinces"						# vanilla province ids
replace_path="history/wars"								# vanilla wars between vanilla characters over vanilla titles
replace_path="history/struggles"						# Iberian, Persian, TGP struggles on vanilla regions
replace_path="history/situations"						# Great Steppe and Christian Church situations on vanilla regions
replace_path="map_data/geographical_regions"			# 10_natural_disaster_regions and tgp_chinesenaming_regions list vanilla counties
