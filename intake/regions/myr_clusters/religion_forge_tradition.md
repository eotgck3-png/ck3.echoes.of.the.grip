# Religion brief — The Forge Tradition

<!-- Cover the whole cluster in one brief: the family it belongs to, the religion, and each faith under it. The scripter builds all three tiers from this. -->

## Family
- Name (existing family, or new): Ancestral (`eotg_rf_ancestral`).
- How hostile it is to outsiders (tolerant / wary / hostile / at war with everyone): Wary / Communal (`doctrine_pluralism_righteous`; views other faiths with deep skepticism unless their craft and commitments are tested by stone and fire).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:754-758`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:55-58`.

## Religion
- Name: Forge (`eotg_religion_forge_tradition`).
- Core beliefs in a paragraph: Stone endures, and what is worked into stone endures with it. The Forge Tradition venerates structural foundation over ornamental flourish: the hall cut deep to withstand planetary bombardment, the masonry joint that will hold true across millennia, and the labour signed by a master craftsman who expects to be judged by people not yet born. Its adherents treat hasty construction as a species of cowardice, preserving ancient industrial secrets across ogre and dwarven foundries.
- Head of faith? (none / spiritual / temporal) and who: None / Lay Clergy (`doctrine_no_head`, `doctrine_theocracy_lay_clergy`), though the senior artisan carries the title of Masterwright (`eotg_forge_head`).
- Attitude to: gender roles, marriage and concubinage, divorce, bastards, close-kin marriage, homosexuality, adultery, kinslaying, witchcraft, deviancy. One line each; "no view" is fine:
  - Gender roles: Equal (`doctrine_gender_equal`).
  - Marriage and concubinage: Polygamous (`doctrine_polygamy`), multiple spouses bound to hearth and workshop.
  - Divorce: Allowed with guild council approval (`doctrine_divorce_approval`).
  - Bastards: Legitimization permitted upon guild apprenticeship (`doctrine_bastardry_legitimization`).
  - Close-kin marriage: Cousin marriage permitted (`doctrine_consanguinity_cousins`), immediate family forbidden.
  - Homosexuality: Shunned (`doctrine_homosexuality_shunned`).
  - Adultery: Men shunned, women considered a crime (`doctrine_adultery_men_shunned`, `doctrine_adultery_women_crime`).
  - Kinslaying: Close-kin kinslaying is considered a crime (`doctrine_kinslaying_close_kin_crime`).
  - Witchcraft: Shunned (`doctrine_witchcraft_shunned`).
  - Deviancy: Shunned (`doctrine_deviancy_shunned`).
- Clergy: who can be a priest, can they marry, who appoints them, do they pay tax: Lay clergy (`doctrine_theocracy_lay_clergy`), either gender may serve (`doctrine_clerical_gender_either`). Clergy are permitted to marry (`doctrine_clerical_marriage_allowed`). Clerics are appointed through temporal artisan appointments (`doctrine_clerical_succession_temporal_appointment`). Clergy fulfil a military recruitment and fortification function (`doctrine_clerical_function_recruitment`). Stoic funeral rites (`doctrine_funeral_stoic`). Pilgrimage involves local rites to ancient quarries and megastructures (`doctrine_pilgrimage_local_rites`).
- Virtues and sins (three each, in words):
  - Virtues: Patient, Diligent, Stubborn (`patient`, `diligent`, `stubborn`).
  - Sins: Impatient, Lazy, Fickle.
- Holy orders / warrior brotherhoods, if any: The Order of the Set Keystone; Hammer-Wrights of Thalvoria.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:754-830`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:165-207, 958-965`.

## Vocabulary
The game fills vanilla strings from these. Give the in-world word for each: the name of the high god (and pronouns), an alternate name, good gods, evil gods, the devil figure, a house of worship (singular/plural), the religious symbol, the holy text, the title of the head of faith and of that office, an ordinary believer (m/f/plural), a priest (m/f/plural), a bishop-rank cleric (m/f/plural), the afterlife (good and bad), the god of death, the witch-god, a holy war and its fighters, a pilgrimage and pilgrims:
- High god: Thalvoria (`eotg_god_thalvoria`), pronouns she/her/hers.
- Alternate name: the Deep Foundation (`eotg_forge_foundation`).
- Good gods / Pantheon: The Deep Makers (`eotg_forge_pantheon`) — Thalvoria, Yu the Stained, Bohemut, Core the Flowing.
- Evil concepts / Devil: The Rubble (`eotg_forge_negative_afterlife`) / Structural Collapse.
- Functional pantheon roles: War: Ferros (`eotg_god_ferros`); Knowledge: Gorgath (`eotg_god_gorgath`); Trickster: Vexis (`eotg_god_vexis`); Night: Lunara (`eotg_god_lunara`); Water: Zephyrion (`eotg_god_zephyrion`).
- House of worship: forgehall / forgehalls (`eotg_forge_house_of_worship`, `eotg_forge_house_of_worship_plural`).
- Religious symbol: the Set Keystone (`eotg_forge_symbol`).
- Holy text: the Maker's Marks (`eotg_forge_text`).
- Title of head of faith and office: the Masterwright (`eotg_forge_head`), office of the Masterwright (`eotg_forge_head_title`).
- Ordinary believer: forge-sworn (male) / forge-sworn (female) / forge-sworn (plural) (`eotg_forge_devotee_male`, `eotg_forge_devotee_female`, `eotg_forge_devotee_male_plural`). Wider adherent: Forgeborn (`eotg_religion_forge_tradition_adherent`).
- Priest: wright (male) / wright (female) / wrights (plural) (`eotg_forge_priest_male`, `eotg_forge_priest_female`, `eotg_forge_priest_male_plural`; alternate plural: the wrights).
- Bishop-rank cleric: masterwright (male) / masterwright (female) / masterwrights (plural) (`eotg_forge_bishop_male`, `eotg_forge_bishop_female`, `eotg_forge_bishop_male_plural`).
- Afterlife: Good: the Standing Work (`eotg_forge_positive_afterlife` / `eotg_forge_divine_realm`); Bad: the Rubble (`eotg_forge_negative_afterlife`).
- God of death: Mystara.
- Witch-god: Vexis.
- Holy war and fighters: Foundation War / Foundation Wars (`eotg_forge_ghw`, `eotg_forge_ghw_plural`); fighters: Hammer-Sworn / Keystone Breakers.
- Pilgrimage and pilgrims: Local Quarry Pilgrimage; pilgrims: Stone-Pilgrims / Wrights.

## Faiths
For each faith:
### Forge-Sworn (`eotg_faith_forge_tradition`)
- Name / adjective / what a believer is called: Forge-Sworn / Forge-Sworn / Forge-Sworn (`eotg_faith_forge_tradition_adj`, `eotg_faith_forge_tradition_adherent`, `eotg_faith_forge_tradition_adherent_plural`).
- Where it is dominant: The Cauldron Marches ([The Cauldron Marches](titles_cauldron_marches.md)), dominant across the industrial holdings of The Forge Marches, led by High Forge-Lord [Rughan Broad-Jaw](ruler_rughan_broad_jaw.md) and Baron [Skrit Grimweave](ruler_skrit_grimweave.md).
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Mountain Worship (`tenet_mountain_worship`): Sanctity of planetary bedrock, tectonic veins, and subterranean basalt bastions.
  2. Megaliths (`tenet_megaliths`): Monumental construction of unyielding vaulted halls, blast doors, and titan-scale smelters.
  3. Communal Identity (`tenet_communal_identity`): Bound loyalty to the industrial clan and ancestral foundry registry.
- Where it differs from the religion above (doctrine overrides): Inherits all religion-level doctrines without overrides.
- Holy sites (place, county, why):
  1. The Great Anvil (`c_eotg_the_great_anvil`): The monolithic volcanic anvil where the first starship hull-plates were forged after the Grip.
  2. Forge Reach (`c_eotg_forge_reach`): Ancestral deep smelters of the Broad-Jaw clan, in continuous operation since 120 AG.
  3. Cauldron Deep (`c_eotg_new_cauldron`): The sub-crustal foundry level underlying the republican capital.
- Colour: Furnace Bronze (`{ 0.6 0.3 0.1 }`).
- Founder, if historical: Masterwright Borun Broad-Jaw (c. 150 AG), author of the first Maker's Marks ledger.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:754-835`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:958-965`.
