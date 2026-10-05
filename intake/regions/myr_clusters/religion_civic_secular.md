# Religion brief — Civic Secular

<!-- Cover the whole cluster in one brief: the family it belongs to, the religion, and each faith under it. The scripter builds all three tiers from this. -->

## Family
- Name (existing family, or new): Pragmatic (`eotg_rf_pragmatic`).
- How hostile it is to outsiders (tolerant / wary / hostile / at war with everyone): Tolerant / Pragmatic (`doctrine_pluralism_pluralistic`; tolerates foreign faiths while legally prohibiting them from holding civic or constitutional office).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:666-670`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:67-70`.

## Religion
- Name: Secular (`eotg_religion_secular_codes`).
- Core beliefs in a paragraph: The Secular Codes represent not an atheistic denial of the gods — since 850 AG, public denial of divine existence has become impossible — but an absolute refusal to permit divine entities or their priestly hierarchies to hold civic governance. Authority must be written down, constitutional, audited, and answerable to literate citizens who can inspect the laws. Power that cannot be scrutinized by an elected assembly is owed no obedience, regardless of whether it claims supernatural light or ancient prophecy.
- Head of faith? (none / spiritual / temporal) and who: None / Lay Clergy (`doctrine_no_head`, `doctrine_theocracy_lay_clergy`), though the senior presiding officer of the constitutional legislature bears the title Speaker (`eotg_codes_head`).
- Attitude to: gender roles, marriage and concubinage, divorce, bastards, close-kin marriage, homosexuality, adultery, kinslaying, witchcraft, deviancy. One line each; "no view" is fine:
  - Gender roles: Equal (`doctrine_gender_equal`).
  - Marriage and concubinage: Monogamous civil contracts (`doctrine_monogamy`), concubinage disallowed.
  - Divorce: Allowed by civil petition (`doctrine_divorce_allowed`).
  - Bastards: All legitimate (`doctrine_bastardry_all`), legal inheritance recognized for all offspring.
  - Close-kin marriage: Cousin marriage permitted (`doctrine_consanguinity_cousins`), immediate family forbidden.
  - Homosexuality: Accepted (`doctrine_homosexuality_accepted`).
  - Adultery: Both men and women accepted (`doctrine_adultery_men_accepted`, `doctrine_adultery_women_accepted`), treated as civil contract matters.
  - Kinslaying: Close-kin kinslaying is considered a crime (`doctrine_kinslaying_close_kin_crime`).
  - Witchcraft: Shunned (`doctrine_witchcraft_shunned`).
  - Deviancy: Accepted (`doctrine_deviancy_accepted`).
- Clergy: who can be a priest, can they marry, who appoints them, do they pay tax: Lay clergy (`doctrine_theocracy_lay_clergy`), either gender may serve (`doctrine_clerical_gender_either`). Clergy are permitted to marry (`doctrine_clerical_marriage_allowed`). Clerics are appointed through civic election or temporal magistrate appointments (`doctrine_clerical_succession_temporal_appointment`). Clergy fulfil an alms and civil pacification function (`doctrine_clerical_function_alms_and_pacification`). Stoic funeral rites (`doctrine_funeral_stoic`). Pilgrimages are forbidden (`doctrine_pilgrimage_forbidden`; civic duty resides at home).
- Virtues and sins (three each, in words):
  - Virtues: Just, Honest, Diligent (`just`, `honest`, `diligent`).
  - Sins: Arbitrary, Deceitful, Lazy.
- Holy orders / warrior brotherhoods, if any: The Republican Home Guard; Constitutional Citizen Militia.
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
- Ordinary believer: citizen (male) / citizen (female) / citizens (plural) (`eotg_faith_civic_secular_adherent`, `eotg_faith_civic_secular_adherent_plural`). Wider adherent: Codebound (`eotg_religion_secular_codes_adherent`).
- Priest: clerk (male) / clerk (female) / clerks (plural) (`eotg_codes_priest_male`, `eotg_codes_priest_female`, `eotg_codes_priest_male_plural`; alternate plural: the clerks).
- Bishop-rank cleric: magistrate (male) / magistrate (female) / magistrates (plural) (`eotg_codes_bishop_male`, `eotg_codes_bishop_female`, `eotg_codes_bishop_male_plural`).
- Afterlife: Good: the Standing Record (`eotg_codes_positive_afterlife` / divine realm: the Record `eotg_codes_divine_realm`); Bad: the Struck Clause (`eotg_codes_negative_afterlife`).
- God of death: the Final Clause (`eotg_codes_final_clause`).
- Witch-god: the Loophole.
- Holy war and fighters: Enforcement / Enforcements (`eotg_codes_ghw`, `eotg_codes_ghw_plural`); fighters: Constitutional Constables / Enforcers.
- Pilgrimage and pilgrims: None (pilgrimage forbidden; attendance at republican assemblies is required).

## Faiths
For each faith:
### Civic Secular (`eotg_faith_civic_secular`)
- Name / adjective / what a believer is called: Civic / Civic / Citizen (`eotg_faith_civic_secular_adj`, `eotg_faith_civic_secular_adherent`, `eotg_faith_civic_secular_adherent_plural`). Cross-reference: see also setting-wide brief [Secular Codes](../../setting/religion_secular_codes.md) for the pan-galactic mercenary variant [Secular Contract](../../setting/religion_secular_codes.md).
- Where it is dominant: The Cauldron Marches ([The Cauldron Marches](titles_cauldron_marches.md)), dominant throughout the Republic of Cauldron (Vanguard March, Emberline March), led by Consul [Clayd Kestrel-Vire](ruler_clayd_kestrel_vire.md) and Praetor [Mirelle Voss](ruler_mirelle_voss.md).
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Legalism (`tenet_legalism`): Constitutional codified law, statutory supremacy, and court precedent govern all decisions.
  2. Communal Identity (`tenet_communal_identity`): Bound patriotic commitment to republican civic fellowship and civic voting duty.
  3. Pursuit of Knowledge (`tenet_pursuit_of_knowledge`): Public education, bureaucratic archives, and open parliamentary inquiry.
- Where it differs from the religion above (doctrine overrides): Emphasizes universal citizen franchise and regular electoral turnover over corporate charters.
- Holy sites (place, county, why):
  1. New Cauldron (`c_eotg_new_cauldron`): The Senate Plaza and Great Rotunda where the First Articles of Confederation were countersigned in 150 AG.
  2. Emberline Assembly (`c_eotg_emberline`): Frontier legislative forum upholding civilian border administration.
  3. Vanguard Hall (`c_eotg_vanguard`): Commemorative military tribunal hall preserving republican oversight over standing legions.
- Colour: Republican Teal (`{ 0.4 0.6 0.5 }`).
- Founder, if historical: First Consul Vane Kestrel (c. 150 AG), who established the New Cauldron charter.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:666-752`; `docs/lore/Third era Nations.md:1240-1280`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:881-885`.
