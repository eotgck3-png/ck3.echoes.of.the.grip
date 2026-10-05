# Religion brief — Industrial Survivalism

<!-- Cover the whole cluster in one brief: the family it belongs to, the religion, and each faith under it. The scripter builds all three tiers from this. -->

## Family
- Name (existing family, or new): Pragmatic (`eotg_rf_pragmatic`).
- How hostile it is to outsiders (tolerant / wary / hostile / at war with everyone): Tolerant / Pragmatic (`doctrine_pluralism_pluralistic`; evaluates outsiders by practical utility, engineering competence, and spare parts rather than theological purity).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:583-587`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:63-66`.

## Religion
- Name: Survivalist (`eotg_religion_survivalism`).
- Core beliefs in a paragraph: The catastrophe of the Grip proved beyond doubt that the universe will not catch you. What caught the survivors was machinery: shelters that held pressure, atmospheric scrubbers that stayed online, and salvage that could be repaired and retrofitted. Industrial Survivalism elevates that material reality into sacred doctrine: the single holy act is maintenance, the cardinal sin is allowing a functioning apparatus to fail through neglect, and a deity who requires prayer is less useful than a hydraulic pump that needs a gasket.
- Head of faith? (none / spiritual / temporal) and who: None / Lay Clergy (`doctrine_no_head`, `doctrine_theocracy_lay_clergy`), though the chief engineer of a fleet carries the honorific Chief Wright (`eotg_survival_head`).
- Attitude to: gender roles, marriage and concubinage, divorce, bastards, close-kin marriage, homosexuality, adultery, kinslaying, witchcraft, deviancy. One line each; "no view" is fine:
  - Gender roles: Equal (`doctrine_gender_equal`).
  - Marriage and concubinage: Monogamous (`doctrine_monogamy`), concubinage disallowed.
  - Divorce: Allowed (`doctrine_divorce_allowed`).
  - Bastards: All legitimate (`doctrine_bastardry_all`), every capable pair of hands is valued.
  - Close-kin marriage: Cousin marriage permitted (`doctrine_consanguinity_cousins`), immediate line forbidden.
  - Homosexuality: Accepted (`doctrine_homosexuality_accepted`).
  - Adultery: Both men and women accepted (`doctrine_adultery_men_accepted`, `doctrine_adultery_women_accepted`).
  - Kinslaying: Close-kin kinslaying is considered a crime (`doctrine_kinslaying_close_kin_crime`).
  - Witchcraft: Shunned (`doctrine_witchcraft_shunned`).
  - Deviancy: Accepted (`doctrine_deviancy_accepted`).
- Clergy: who can be a priest, can they marry, who appoints them, do they pay tax: Lay clergy (`doctrine_theocracy_lay_clergy`), either gender may serve (`doctrine_clerical_gender_either`). Clergy are permitted to marry (`doctrine_clerical_marriage_allowed`). Clerics are appointed through temporal technical appointments (`doctrine_clerical_succession_temporal_appointment`). Clergy perform taxation and resource allocation functions (`doctrine_clerical_function_taxation`). Cremation funeral rites (`doctrine_funeral_cremation`; biological recovery). Pilgrimages are strictly forbidden (`doctrine_pilgrimage_forbidden`; unnecessary fuel expenditure is sinful).
- Virtues and sins (three each, in words):
  - Virtues: Diligent, Temperate, Patient (`diligent`, `temperate`, `patient`).
  - Sins: Lazy, Gluttonous, Impatient.
- Holy orders / warrior brotherhoods, if any: Scavenger Fleet Wardens; Habitat Maintenance Corps.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:583-664`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:255-331, 802-809`.

## Vocabulary
The game fills vanilla strings from these. Give the in-world word for each: the name of the high god (and pronouns), an alternate name, good gods, evil gods, the devil figure, a house of worship (singular/plural), the religious symbol, the holy text, the title of the head of faith and of that office, an ordinary believer (m/f/plural), a priest (m/f/plural), a bishop-rank cleric (m/f/plural), the afterlife (good and bad), the god of death, the witch-god, a holy war and its fighters, a pilgrimage and pilgrims:
- High god: the Work (`eotg_survival_work`), pronouns it/its.
- Alternate name: the Long Maintenance (`eotg_survival_upkeep`).
- Good gods / Pantheon: The Working Order (`eotg_survival_pantheon`) — the Work, the Archive (`eotg_survival_archive`), the Stores (`eotg_survival_stores`).
- Evil concepts / Devil: Entropy (`eotg_survival_entropy`), Rust (`eotg_survival_rust`), the Breach (`eotg_survival_breach`), the Failure (`eotg_survival_failure`), the Unlicensed (`eotg_survival_unlicensed`).
- Functional pantheon roles: Creator: the Builders (`eotg_survival_builders`); Health: the Regimen (`eotg_survival_regimen`); Fertility: the Line (`eotg_survival_line`); Household: the Hearth (`eotg_survival_hearth`); Fate: the Odds (`eotg_survival_odds`); War: the Muster (`eotg_survival_muster`); Trickster: the Chancer (`eotg_survival_chancer`); Night: the Dark (`eotg_survival_dark`); Water: the Filters (`eotg_survival_filters`).
- House of worship: workshop / workshops (`eotg_survival_house_of_worship`, `eotg_survival_house_of_worship_plural`).
- Religious symbol: the Turned Gear (`eotg_survival_symbol`).
- Holy text: the Maintenance Log (`eotg_survival_text`).
- Title of head of faith and office: the Chief Wright (`eotg_survival_head`), office of the Chief Wright (`eotg_survival_head_title`).
- Ordinary believer: creedwright (male) / creedwright (female) / creedwrights (plural) (`eotg_survival_devotee_male`, `eotg_survival_devotee_female`, `eotg_survival_devotee_male_plural`). Wider adherent: Survivalist (`eotg_religion_survivalism_adherent`).
- Priest: wright (male) / wright (female) / wrights (plural) (`eotg_survival_priest_male`, `eotg_survival_priest_female`, `eotg_survival_priest_male_plural`; alternate plural: the wrights).
- Bishop-rank cleric: overwright (male) / overwright (female) / overwrights (plural) (`eotg_survival_bishop_male`, `eotg_survival_bishop_female`, `eotg_survival_bishop_male_plural`).
- Afterlife: Good: the Salvage (`eotg_survival_positive_afterlife` / divine realm: the Running State `eotg_survival_divine_realm`); Bad: the Scrap (`eotg_survival_negative_afterlife`).
- God of death: Entropy / the Failure.
- Witch-god: the Chancer.
- Holy war and fighters: Salvage War / Salvage Wars (`eotg_survival_ghw`, `eotg_survival_ghw_plural`); fighters: Scrappers / Breaker-Crews.
- Pilgrimage and pilgrims: None (pilgrimage forbidden; exploration is technical prospecting).

## Faiths
For each faith:
### Creedwright (`eotg_faith_industrial_survivalism`)
- Name / adjective / what a believer is called: Creedwright / Creedwright / Creedwright (`eotg_faith_industrial_survivalism_adj`, `eotg_faith_industrial_survivalism_adherent`, `eotg_faith_industrial_survivalism_adherent_plural`).
- Where it is dominant: The Outer Marches ([The Outer Marches](titles_outer_marches.md)), dominant across Dead Reach, Uvrek, and The Far Drift, led by warlords like [Dorian Valek](ruler_dorian_valek.md), as well as frontier salvage operations in Helix Fringe.
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Communal Identity (`tenet_communal_identity`): Tight communal solidarity within salvage flotillas, where survival requires collective coordination.
  2. Pursuit of Knowledge (`tenet_pursuit_of_knowledge`): Reverse-engineering pre-Grip technology, blueprint preservation, and technical improvisation.
  3. Adaptive (`tenet_adaptive`): Utilitarian flexibility in cultural adaptation, scavenging, and political compromise.
- Where it differs from the religion above (doctrine overrides): Inherits all religion-level doctrines without overrides.
- Holy sites (place, county, why):
  1. Helix Prime (`c_eotg_helix_prime`): Remnant AI hub and automated nanofactory nexus held by the remnant Helix Corporation.
  2. Dead Reach (`c_eotg_dead_reach`): Massive starship graveyard providing raw plating and functional fusion cores for three centuries.
  3. Far Drift Station (`c_eotg_far_drift`): Sovereign deep-space habitat operating continuously since 45 AG.
- Colour: Salvage Grey (`{ 0.4 0.4 0.4 }`).
- Founder, if historical: Unknown; emergent from 1st-century survivor-crews of the Titan Exodus flotillas.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:583-664`; `docs/lore/Third era Nations.md:1240-1280`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:802-809`.
