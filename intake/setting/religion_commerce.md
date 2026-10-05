# Religion brief — The Mercantile Creed (Bohemite)

<!-- Cover the whole cluster in one brief: the family it belongs to, the religion, and each faith under it. The scripter builds all three tiers from this. -->

## Family
- Name (existing family, or new): Divine Order (`eotg_rf_divine_order`).
- How hostile it is to outsiders (tolerant / wary / hostile / at war with everyone): Tolerant / Pragmatic (`doctrine_pluralism_pluralistic`, Abrahamic family; treats non-believers with transactional openness; trade treaties override doctrinal disputes).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:85-88`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:43-44`.

## Religion
- Name: Mercantile (`eotg_religion_commerce`).
- Core beliefs in a paragraph: Bohemut, Son of Yu, maintains the cosmic equilibrium that his brothers continually attempt to upend. His followers hold that universal balance is not a passive sentiment but an exact mathematical accounting: debts inevitably settle, intellectual knowledge compounds over time, and a contract struck freely between two consenting parties is a small, sacred act of cosmic order. Scholars and merchant houses read the exact same scripture, with scholars seeking philosophical balance while financiers calculate compound returns.
- Head of faith? (none / spiritual / temporal) and who: None / Lay Clergy (`doctrine_no_head`, `doctrine_theocracy_lay_clergy`), though the senior magistrate of the Free Exchanges holds the honorific title Arbiter (`eotg_commerce_head`).
- Attitude to: gender roles, marriage and concubinage, divorce, bastards, close-kin marriage, homosexuality, adultery, kinslaying, witchcraft, deviancy. One line each; "no view" is fine:
  - Gender roles: Equal (`doctrine_gender_equal`).
  - Marriage and concubinage: Monogamous commercial contracts (`doctrine_monogamy`), concubinage disallowed.
  - Divorce: Allowed (`doctrine_divorce_allowed`).
  - Bastards: All legitimate (`doctrine_bastardry_all`), assets distribute according to written will.
  - Close-kin marriage: Cousin marriage permitted (`doctrine_consanguinity_cousins`), immediate family forbidden.
  - Homosexuality: Accepted (`doctrine_homosexuality_accepted`).
  - Adultery: Both men and women shunned (`doctrine_adultery_men_shunned`, `doctrine_adultery_women_shunned`).
  - Kinslaying: Close-kin kinslaying is considered a crime (`doctrine_kinslaying_close_kin_crime`).
  - Witchcraft: Shunned (`doctrine_witchcraft_shunned`).
  - Deviancy: Accepted (`doctrine_deviancy_accepted`).
- Clergy: who can be a priest, can they marry, who appoints them, do they pay tax: Lay clergy (`doctrine_theocracy_lay_clergy`), either gender may serve (`doctrine_clerical_gender_either`). Clergy are permitted to marry (`doctrine_clerical_marriage_allowed`). Clerics are appointed through temporal civic appointments (`doctrine_clerical_succession_temporal_appointment`). Clergy perform taxation and accounting audit functions (`doctrine_clerical_function_taxation`). Stoic funeral rites (`doctrine_funeral_stoic`). Pilgrimages are forbidden (`doctrine_pilgrimage_forbidden`; business journeys suffice).
- Virtues and sins (three each, in words):
  - Virtues: Diligent, Honest, Temperate (`diligent`, `honest`, `temperate`).
  - Sins: Lazy, Deceitful, Gluttonous.
- Holy orders / warrior brotherhoods, if any: The League Mercenary Enforcers; The Guardians of the Balance.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:85-166`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:117-229, 450-492`.

## Vocabulary
The game fills vanilla strings from these. Give the in-world word for each: the name of the high god (and pronouns), an alternate name, good gods, evil gods, the devil figure, a house of worship (singular/plural), the religious symbol, the holy text, the title of the head of faith and of that office, an ordinary believer (m/f/plural), a priest (m/f/plural), a bishop-rank cleric (m/f/plural), the afterlife (good and bad), the god of death, the witch-god, a holy war and its fighters, a pilgrimage and pilgrims:
- High god: Bohemut (`eotg_god_bohemut`), pronouns he/him/his.
- Alternate name: the Ledger (`eotg_commerce_ledger`).
- Good gods / Pantheon: The Balance (`eotg_commerce_pantheon`) — Bohemut, Yu the Stained, Serephios, Mystara.
- Evil concepts / Devil: The Outstanding Debt (`eotg_commerce_negative_afterlife`) / Unbalanced Books.
- Functional pantheon roles: Creator: Yu the Stained (`eotg_god_yu`); Health: Core the Flowing (`eotg_god_core`); Fertility: Solena (`eotg_god_solena`); Wealth: Serephios (`eotg_god_serephios`); Household: Thalvoria (`eotg_god_thalvoria`); Fate: Mystara (`eotg_god_mystara`); Knowledge: Bohemut (`eotg_god_bohemut`); War: Ravos (`eotg_god_ravos`); Trickster: Vexis (`eotg_god_vexis`); Night: Lunara (`eotg_god_lunara`); Water: Zephyrion (`eotg_god_zephyrion`).
- House of worship: counting house / counting houses (`eotg_commerce_house_of_worship`, `eotg_commerce_house_of_worship_plural`).
- Religious symbol: the Balanced Scale (`eotg_commerce_symbol`).
- Holy text: the Great Ledger (`eotg_commerce_text`).
- Title of head of faith and office: the Arbiter (`eotg_commerce_head`), office of the Arbiter (`eotg_commerce_head_title`).
- Ordinary believer: signatory (male) / signatory (female) / signatories (plural) (`eotg_commerce_devotee_male`, `eotg_commerce_devotee_female`, `eotg_commerce_devotee_male_plural`). Wider adherent: Bohemite (`eotg_religion_commerce_adherent`).
- Priest: reckoner (male) / reckoner (female) / reckoners (plural) (`eotg_commerce_priest_male`, `eotg_commerce_priest_female`, `eotg_commerce_priest_male_plural`; alternate plural: the reckoners).
- Bishop-rank cleric: factor (male) / factor (female) / factors (plural) (`eotg_commerce_bishop_male`, `eotg_commerce_bishop_female`, `eotg_commerce_bishop_male_plural`).
- Afterlife: Good: the Settled Account (`eotg_commerce_positive_afterlife` / divine realm: the Reckoning `eotg_commerce_divine_realm`); Bad: the Outstanding Debt (`eotg_commerce_negative_afterlife`).
- God of death: Mystara.
- Witch-god: Vexis.
- Holy war and fighters: Reckoning / Reckonings (`eotg_commerce_ghw`, `eotg_commerce_ghw_plural`); fighters: Factors / Contract Guardians.
- Pilgrimage and pilgrims: None (forbidden; commercial voyages fulfill secular duties).

## Faiths
For each faith:
### Creed-Sworn (`eotg_faith_commerce`)
- Name / adjective / what a believer is called: Creed-Sworn / Creed-Sworn / Creed-Sworn (`eotg_faith_commerce_adj`, `eotg_faith_commerce_adherent`, `eotg_faith_commerce_adherent_plural`).
- Where it is dominant: Throughout the merchant league worlds of the Free Sectors and across the commercial ports of the Charter Principalities ([The Charter Principalities](../regions/myr_clusters/titles_charter_principalities.md)), shared by Bohemite human and ogre merchant patricians.
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Pursuit of Knowledge (`tenet_pursuit_of_knowledge`): Empirical study of economic variables, trade flows, navigational routes, and engineering sciences.
  2. Ritual Hospitality (`tenet_ritual_hospitality`): Sacred inviolability of trade envoys, neutral commercial ports, and safe passage for bonded merchants.
  3. Legalism (`tenet_legalism`): Absolute primacy of the written contract; breach of commercial covenant is treated as actionable cosmic sin.
- Where it differs from the religion above (doctrine overrides): Inherits all religion-level doctrines without overrides.
- Holy sites (place, county, why):
  1. Bohemut's Ledger (Free Worlds): The supreme planetary exchange where the universal galactic credit standard was first calibrated.
  2. Halcyon (`c_eotg_halcyon`): Sovereign trade station and free port linking Core goods to the Marches.
  3. Xerxes Exchange (`c_eotg_new_xerxes`): Dome 2 commercial quarter where the treaty between Bohemite traders and goblin syndicates was ratified.
- Colour: Bronze Gold (`{ 0.8 0.65 0.1 }`).
- Founder, if historical: Unknown; originated among the First Reconstruction Trade Convoys (c. 95 AG).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:85-166`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:450-492`.
