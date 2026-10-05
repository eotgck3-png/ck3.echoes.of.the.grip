# Religion brief — Secular Codes

<!-- Cover the whole cluster in one brief: the family it belongs to, the religion, and each faith under it. The scripter builds all three tiers from this. -->

## Family
- Name (existing family, or new): Pragmatic (`eotg_rf_pragmatic`).
- How hostile it is to outsiders (tolerant / wary / hostile / at war with everyone): Tolerant / Pragmatic (`doctrine_pluralism_pluralistic`, pragmatic family; rejects religious supremacy and interacts with all factions via legal treaty).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:666-670`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:67-70`.

## Religion
- Name: Secular (`eotg_religion_secular_codes`).
- Core beliefs in a paragraph: The Secular Codes represent a pan-galactic philosophical framework that declines theological metaphysics. While not denying that divine beings exist, the Codes adamantly refuse to grant them constitutional or legal authority. The Codes insist that sovereignty must be written down, clearly bounded, audited by accountable officials, and answerable to people who can read the statutes. A power that cannot be audited by civil law is owed no obedience, whether it is an emperor claiming solar grace or a cosmic titan speaking from a rift.
- Head of faith? (none / spiritual / temporal) and who: None / Lay Clergy (`doctrine_no_head`, `doctrine_theocracy_lay_clergy`), though parliamentary speakers or senior company judges hold the civic title Speaker (`eotg_codes_head`).
- Attitude to: gender roles, marriage and concubinage, divorce, bastards, close-kin marriage, homosexuality, adultery, kinslaying, witchcraft, deviancy. One line each; "no view" is fine:
  - Gender roles: Equal (`doctrine_gender_equal`).
  - Marriage and concubinage: Monogamous civil contracts (`doctrine_monogamy`), concubinage disallowed.
  - Divorce: Allowed (`doctrine_divorce_allowed`).
  - Bastards: All legitimate (`doctrine_bastardry_all`).
  - Close-kin marriage: Cousin marriage permitted (`doctrine_consanguinity_cousins`), immediate family forbidden.
  - Homosexuality: Accepted (`doctrine_homosexuality_accepted`).
  - Adultery: Both men and women accepted (`doctrine_adultery_men_accepted`, `doctrine_adultery_women_accepted`), governed by civil damages.
  - Kinslaying: Close-kin kinslaying is considered a crime (`doctrine_kinslaying_close_kin_crime`).
  - Witchcraft: Shunned (`doctrine_witchcraft_shunned`).
  - Deviancy: Accepted (`doctrine_deviancy_accepted`).
- Clergy: who can be a priest, can they marry, who appoints them, do they pay tax: Lay clerks (`doctrine_theocracy_lay_clergy`), either gender may serve (`doctrine_clerical_gender_either`). Clergy are permitted to marry (`doctrine_clerical_marriage_allowed`). Clerics are appointed through civic election or temporal magistrate appointments (`doctrine_clerical_succession_temporal_appointment`). Clergy fulfil an alms and civil pacification function (`doctrine_clerical_function_alms_and_pacification`). Stoic funeral rites (`doctrine_funeral_stoic`). Pilgrimages are forbidden (`doctrine_pilgrimage_forbidden`).
- Virtues and sins (three each, in words):
  - Virtues: Just, Honest, Diligent (`just`, `honest`, `diligent`).
  - Sins: Arbitrary, Deceitful, Lazy.
- Holy orders / warrior brotherhoods, if any: The Mercenary Guild Arbitrators; The Constitutional Militia.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:666-752`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:332-404, 881-885`.

## Vocabulary
The game fills vanilla strings from these. Give the in-world word for each: the name of the high god (and pronouns), an alternate name, good gods, evil gods, the devil figure, a house of worship (singular/plural), the religious symbol, the holy text, the title of the head of faith and of that office, an ordinary believer (m/f/plural), a priest (m/f/plural), a bishop-rank cleric (m/f/plural), the afterlife (good and bad), the god of death, the witch-god, a holy war and its fighters, a pilgrimage and pilgrims:
- High god: the Code (`eotg_codes_code`), pronouns it/its.
- Alternate name: the Charter (`eotg_codes_charter`).
- Good gods / Pantheon: The Articles (`eotg_codes_pantheon`) — the Code, the Charter, the Record (`eotg_codes_record`).
- Evil concepts / Devil: Tyranny (`eotg_codes_tyranny`), the Mob (`eotg_codes_mob`), the Unaccountable (`eotg_codes_unaccountable`), the Unwritten (`eotg_codes_unwritten`), the Struck Clause (`eotg_codes_negative_afterlife`).
- Functional pantheon roles: Creator: the Founders (`eotg_codes_founders`); Health: the Physicians (`eotg_codes_physicians`); Fertility: the Census (`eotg_codes_census`); Wealth: the Treasury (`eotg_codes_treasury`); Household: the Household (`eotg_codes_household`); Fate: the Precedent (`eotg_codes_precedent`); War: the Contract (`eotg_codes_contract`); Trickster: the Loophole (`eotg_codes_loophole`); Night: the Curfew (`eotg_codes_curfew`); Water: the Commons (`eotg_codes_commons`).
- House of worship: assembly hall / assembly halls (`eotg_codes_house_of_worship`, `eotg_codes_house_of_worship_plural`).
- Religious symbol: the Countersigned Seal (`eotg_codes_symbol`).
- Holy text: the Articles (`eotg_codes_text`).
- Title of head of faith and office: the Speaker (`eotg_codes_head`), office of the Speaker (`eotg_codes_head_title`).
- Ordinary believer: codebound (male) / codebound (female) / codebound (plural) (`eotg_codes_devotee_male`, `eotg_codes_devotee_female`, `eotg_codes_devotee_male_plural`). Wider adherent: Codebound (`eotg_religion_secular_codes_adherent`).
- Priest: clerk (male) / clerk (female) / clerks (plural) (`eotg_codes_priest_male`, `eotg_codes_priest_female`, `eotg_codes_priest_male_plural`; alternate plural: the clerks).
- Bishop-rank cleric: magistrate (male) / magistrate (female) / magistrates (plural) (`eotg_codes_bishop_male`, `eotg_codes_bishop_female`, `eotg_codes_bishop_male_plural`).
- Afterlife: Good: the Standing Record (`eotg_codes_positive_afterlife` / divine realm: the Record `eotg_codes_divine_realm`); Bad: the Struck Clause (`eotg_codes_negative_afterlife`).
- God of death: the Final Clause (`eotg_codes_final_clause`).
- Witch-god: the Loophole.
- Holy war and fighters: Enforcement / Enforcements (`eotg_codes_ghw`, `eotg_codes_ghw_plural`); fighters: Enforcers / Sworn Bailiffs.
- Pilgrimage and pilgrims: None (forbidden).

## Faiths
For each faith:
### Contract-Sworn (`eotg_faith_secular_contract`)
- Name / adjective / what a believer is called: Contract / Contract / Contract-Sworn (`eotg_faith_secular_contract_adj`, `eotg_faith_secular_contract_adherent`, `eotg_faith_secular_contract_adherent_plural`).
- Where it is dominant: Pan-galactic mercenary companies, independent free-trader flotillas, and border legion encampments across settled space.
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Warmonger (`tenet_warmonger`): Military contracts and mercenary service are treated as sacred obligations; martial readiness incurs no peace-weariness penalty.
  2. Legalism (`tenet_legalism`): Absolute adherence to signed articles of engagement, bounty terms, and client guarantees.
  3. Adaptive (`tenet_adaptive`): Pragmatic operational flexibility across foreign cultures and shifting battlefields.
- Where it differs from the religion above (doctrine overrides): Elevates military force and contractual armed engagement over civic legislative processes.
- Holy sites (place, county, why):
  1. Port Vanguard (`c_eotg_vanguard`): The Grand Muster Hall where multi-cluster mercenary charters are registered and arbitrated.
  2. Sol-Drift Station: Neutral deep-space repository of military bond deposits.
  3. Dead Reach (`c_eotg_dead_reach`): Salvage fortress where veteran mercenary companies deposit historical service banners.
- Colour: Mercenary Slate (`{ 0.5 0.5 0.6 }`).
- Founder, if historical: Unknown; codified by the Great Free Companies during the Second Reconstruction Wars (c. 280 AG).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:666-745`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:332-404`.

### Civic Secular (`eotg_faith_civic_secular`)
- Name / adjective / what a believer is called: Civic / Civic / Citizen (`eotg_faith_civic_secular_adj`, `eotg_faith_civic_secular_adherent`, `eotg_faith_civic_secular_adherent_plural`). Cross-reference: see detailed regional brief in [Civic Secular (Myr Clusters)](../regions/myr_clusters/religion_civic_secular.md).
- Where it is dominant: The Republic of Cauldron and constitutional federation worlds.
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Legalism (`tenet_legalism`): Supremacy of statutory constitutional codes.
  2. Communal Identity (`tenet_communal_identity`): Republican civic fraternity and voting responsibility.
  3. Pursuit of Knowledge (`tenet_pursuit_of_knowledge`): Public scientific inquiry, archives, and debate.
- Where it differs from the religion above (doctrine overrides): Emphasizes civilian parliamentary supremacy over martial mercenary command.
- Holy sites (place, county, why):
  1. New Cauldron (`c_eotg_new_cauldron`): Site of the Confederation Charter ratification.
  2. Emberline (`c_eotg_emberline`): Frontier legislative forum.
  3. Vanguard Hall (`c_eotg_vanguard`): Republican constitutional tribunal.
- Colour: Republican Teal (`{ 0.4 0.6 0.5 }`).
- Founder, if historical: Consul Vane Kestrel (c. 150 AG).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:666-752`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:881-885`.
