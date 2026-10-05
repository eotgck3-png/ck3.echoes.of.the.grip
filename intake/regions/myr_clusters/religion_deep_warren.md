# Religion brief — The Deep Warren

<!-- Cover the whole cluster in one brief: the family it belongs to, the religion, and each faith under it. The scripter builds all three tiers from this. -->

## Family
- Name (existing family, or new): Ancestral (`eotg_rf_ancestral`).
- How hostile it is to outsiders (tolerant / wary / hostile / at war with everyone): Wary / Isolationist (`doctrine_pluralism_righteous`; suspicious of surface-dwellers and open-sky empires; defensive doctrine).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:837-841`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:59-62`.

## Religion
- Name: Warren (`eotg_religion_deep_warren`).
- Core beliefs in a paragraph: Down is safety, and down is also where everyone who came before you resides. The ratfolk survived the cosmic horror of the Grip by burrowing far beneath it, and they have never stopped viewing the open sky as a temporary, hazardous condition. The deep galleries are not merely shelters: each level was cut by a named generation of forebears, and their names are meticulously maintained. To delve further down is to venture deeper into ancestral memory, which is why depth itself is sacred and abandoning a consecrated gallery is judged a grave desertion.
- Head of faith? (none / spiritual / temporal) and who: Spiritual head (`doctrine_spiritual_head`), titled the Deepmost (`eotg_warren_head`). In 866 AG, held by [Mother-Vessel Threelatch](ruler_mother_vessel_threelatch.md) from the lowest consecrated gallery of The First Vault.
- Attitude to: gender roles, marriage and concubinage, divorce, bastards, close-kin marriage, homosexuality, adultery, kinslaying, witchcraft, deviancy. One line each; "no view" is fine:
  - Gender roles: Equal (`doctrine_gender_equal`).
  - Marriage and concubinage: Polygamous (`doctrine_polygamy`), multiple partners within the communal warren nest.
  - Divorce: Allowed (`doctrine_divorce_allowed`).
  - Bastards: All legitimate (`doctrine_bastardry_all`), community raises all pups equally.
  - Close-kin marriage: Cousin marriage permitted (`doctrine_consanguinity_cousins`), immediate line forbidden.
  - Homosexuality: Accepted (`doctrine_homosexuality_accepted`).
  - Adultery: Both men and women accepted (`doctrine_adultery_men_accepted`, `doctrine_adultery_women_accepted`).
  - Kinslaying: Extended family kinslaying is considered a crime (`doctrine_kinslaying_extended_family_crime`).
  - Witchcraft: Shunned (`doctrine_witchcraft_shunned`).
  - Deviancy: Accepted (`doctrine_deviancy_accepted`).
- Clergy: who can be a priest, can they marry, who appoints them, do they pay tax: Lay clergy (`doctrine_theocracy_lay_clergy`), either gender may serve (`doctrine_clerical_gender_either`). Clergy are permitted to marry (`doctrine_clerical_marriage_allowed`). Clerics are appointed through spiritual fixed appointment (`doctrine_clerical_succession_spiritual_fixed_appointment`). Clergy fulfil an alms and pacification function (`doctrine_clerical_function_alms_and_pacification`). Cremation funeral rites (`doctrine_funeral_cremation`). Pilgrimage consists of local subterranean rites (`doctrine_pilgrimage_local_rites`).
- Virtues and sins (three each, in words):
  - Virtues: Patient, Paranoid, Diligent (`patient`, `paranoid`, `diligent`).
  - Sins: Impatient, Trusting, Lazy.
- Holy orders / warrior brotherhoods, if any: The Warren Redoubt Guard; Tunnel-Keepers of the Undermost.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:837-917`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:208-254, 1038-1045`.

## Vocabulary
The game fills vanilla strings from these. Give the in-world word for each: the name of the high god (and pronouns), an alternate name, good gods, evil gods, the devil figure, a house of worship (singular/plural), the religious symbol, the holy text, the title of the head of faith and of that office, an ordinary believer (m/f/plural), a priest (m/f/plural), a bishop-rank cleric (m/f/plural), the afterlife (good and bad), the god of death, the witch-god, a holy war and its fighters, a pilgrimage and pilgrims:
- High god: the Deep (`eotg_warren_deep`), pronouns it/its.
- Alternate name: the Undermost (`eotg_warren_undermost`).
- Good gods / Pantheon: The Deep Forebears (`eotg_warren_pantheon`) — Gorgath, Thalvoria, Lunara, Yu the Stained.
- Evil concepts / Devil: The Open Sky (`eotg_warren_negative_afterlife`) / Surface Exposure.
- Functional pantheon roles: Knowledge: Gorgath (`eotg_god_gorgath`); War: Ravos (`eotg_god_ravos`); Trickster: Vexis (`eotg_god_vexis`); Night: Lunara (`eotg_god_lunara`); Water: Zephyrion (`eotg_god_zephyrion`).
- House of worship: deep gallery / deep galleries (`eotg_warren_house_of_worship`, `eotg_warren_house_of_worship_plural`).
- Religious symbol: the Descending Way (`eotg_warren_symbol`).
- Holy text: the Depth Rolls (`eotg_warren_text`).
- Title of head of faith and office: the Deepmost (`eotg_warren_head`), office of the Deepmost (`eotg_warren_head_title`).
- Ordinary believer: deepkeeper (male) / deepkeeper (female) / deepkeepers (plural) (`eotg_warren_devotee_male`, `eotg_warren_devotee_female`, `eotg_warren_devotee_male_plural`). Wider adherent: Warrenfolk (`eotg_religion_deep_warren_adherent`).
- Priest: gallery-keeper (male) / gallery-keeper (female) / gallery-keepers (plural) (`eotg_warren_priest_male`, `eotg_warren_priest_female`, `eotg_warren_priest_male_plural`; alternate plural: the gallery-keepers).
- Bishop-rank cleric: deepwarden (male) / deepwarden (female) / deepwardens (plural) (`eotg_warren_bishop_male`, `eotg_warren_bishop_female`, `eotg_warren_bishop_male_plural`).
- Afterlife: Good: the Undermost (`eotg_warren_positive_afterlife` / `eotg_warren_divine_realm`); Bad: the Open Sky (`eotg_warren_negative_afterlife`).
- God of death: Mystara.
- Witch-god: Vexis.
- Holy war and fighters: Delving / Delvings (`eotg_warren_ghw`, `eotg_warren_ghw_plural`); fighters: Tunnel-Fighters / Deep Wardens.
- Pilgrimage and pilgrims: Descent Rites; pilgrims: Delvers / Gallery Pilgrims.

## Faiths
For each faith:
### Deepkeeper (`eotg_faith_deep_warren`)
- Name / adjective / what a believer is called: Deepkeeper / Deepkeeper / Deepkeeper (`eotg_faith_deep_warren_adj`, `eotg_faith_deep_warren_adherent`, `eotg_faith_deep_warren_adherent_plural`).
- Where it is dominant: The Outer Marches ([The Outer Marches](titles_outer_marches.md)), dominant across the Warrens and Rust Verge duchies, led by [Mother-Vessel Threelatch](ruler_mother_vessel_threelatch.md) and [Marlen](ruler_marlen.md).
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Ancestor Worship (`tenet_ancestor_worship`): Daily veneration of named generational diggers who established subterranean habitats.
  2. Cthonic Redoubts (`tenet_cthonic_redoubts`): Deep underground defensive bonuses and spiritual power derived from subterranean life.
  3. Pastoral Isolation (`tenet_pastoral_isolation`): Deliberate detachment from planetary surface diplomacy and external alliances.
- Where it differs from the religion above (doctrine overrides): Inherits all religion-level doctrines without overrides.
- Holy sites (place, county, why):
  1. The First Vault (`c_eotg_the_first_vault`): The deepest habitable shelter excavated during the Grip's initial atmospheric burn.
  2. Warren Core (`c_eotg_warren_core`): The mother-nest where the original Threelatch clan covenant is sealed.
  3. Rust Sanctum (`c_eotg_rust_verge`): The vast subterranean salvage aquifer separating ratfolk territory from outer scavenger wastes.
- Colour: Subterranean Plum (`{ 0.4 0.3 0.5 }`).
- Founder, if historical: First Mother Threelatch (c. 10 AG), who led the descent into the deep bedrock.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:837-918`; `docs/lore/Third era Nations.md:1240-1280`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:1038-1045`.
