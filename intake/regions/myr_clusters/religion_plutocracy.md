# Religion brief — Plutocracy

<!-- Cover the whole cluster in one brief: the family it belongs to, the religion, and each faith under it. The scripter builds all three tiers from this. -->

## Family
- Name (existing family, or new): Pragmatic (`eotg_rf_pragmatic`).
- How hostile it is to outsiders (tolerant / wary / hostile / at war with everyone): Tolerant / Pragmatic (`doctrine_pluralism_pluralistic`; treats outsiders transactionally; non-believers are assessed for tax rather than exterminated).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:920-924`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:51-54`.

## Religion
- Name: Plutocratic (`eotg_religion_plutocracy`).
- Core beliefs in a paragraph: The goblin mercantile classes trade alongside the Bohemites, bank with them, and share the Gob-Ogre Trade League, but they have never shared their faith. Where Bohemites venerate balance, the Plutocracy rejects such restraint as sentimental nonsense: the sacred act is not the exchange but the accumulation, and capital that stops multiplying has died. It recognises no metaphysical deities because the Hoard is tangible, answers petitions in proportion to capital invested, and requires arithmetic rather than faith.
- Head of faith? (none / spiritual / temporal) and who: None / Lay Clergy (`doctrine_no_head`, `doctrine_theocracy_lay_clergy`), though the chief assessor carries the ceremonial title of Hoardmaster (`eotg_pluto_head`).
- Attitude to: gender roles, marriage and concubinage, divorce, bastards, close-kin marriage, homosexuality, adultery, kinslaying, witchcraft, deviancy. One line each; "no view" is fine:
  - Gender roles: Equal (`doctrine_gender_equal`).
  - Marriage and concubinage: Concubines permitted (`doctrine_concubines`), partners taken according to financial arrangement.
  - Divorce: Allowed (`doctrine_divorce_allowed`).
  - Bastards: All legitimate (`doctrine_bastardry_all`), inheritance governed by asset ledgers.
  - Close-kin marriage: Dynastic / Unrestricted within banking consortiums (`doctrine_consanguinity_dynastic`).
  - Homosexuality: Accepted (`doctrine_homosexuality_accepted`).
  - Adultery: Both men and women shunned (`doctrine_adultery_men_shunned`, `doctrine_adultery_women_shunned`).
  - Kinslaying: Close-kin kinslaying is considered a crime (`doctrine_kinslaying_close_kin_crime`).
  - Witchcraft: Shunned (`doctrine_witchcraft_shunned`).
  - Deviancy: Accepted (`doctrine_deviancy_accepted`).
- Clergy: who can be a priest, can they marry, who appoints them, do they pay tax: Lay clergy (`doctrine_theocracy_lay_clergy`), either gender may serve (`doctrine_clerical_gender_either`). Clergy are permitted to marry (`doctrine_clerical_marriage_allowed`). Clerics are appointed through temporal office appointment (`doctrine_clerical_succession_temporal_appointment`). Clergy perform taxation functions (`doctrine_clerical_function_taxation`). Stoic funeral rites (`doctrine_funeral_stoic`). Pilgrimages are forbidden (`doctrine_pilgrimage_forbidden`; commerce must never pause for travel rites).
- Virtues and sins (three each, in words):
  - Virtues: Greedy, Diligent, Ambitious (`greedy`, `diligent`, `ambitious`).
  - Sins: Generous, Lazy, Content.
- Holy orders / warrior brotherhoods, if any: Corporate Enforcers / Debt Collector Guilds.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:920-955`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:90-164, 1118-1126`.

## Vocabulary
The game fills vanilla strings from these. Give the in-world word for each: the name of the high god (and pronouns), an alternate name, good gods, evil gods, the devil figure, a house of worship (singular/plural), the religious symbol, the holy text, the title of the head of faith and of that office, an ordinary believer (m/f/plural), a priest (m/f/plural), a bishop-rank cleric (m/f/plural), the afterlife (good and bad), the god of death, the witch-god, a holy war and its fighters, a pilgrimage and pilgrims:
- High god: the Hoard (`eotg_pluto_hoard`), pronouns it/its.
- Alternate name: the Increase (`eotg_pluto_increase`).
- Good gods / Pantheon: The Accounts (`eotg_pluto_pantheon`) — the Hoard, the Increase, the Dividend (`eotg_pluto_dividend`).
- Evil concepts / Devil: The Default (`eotg_pluto_default`), Insolvency (`eotg_pluto_insolvency`), the Foreclosure (`eotg_pluto_foreclosure`), the Counterfeit (`eotg_pluto_counterfeit`).
- Functional pantheon roles: Creator: the First Debt (`eotg_pluto_first_debt`); Health: the Fee (`eotg_pluto_fee`); Fertility: the Dividend; Household: the Vault (`eotg_pluto_vault`); Fate: the Market (`eotg_pluto_market`); Knowledge: the Appraisal (`eotg_pluto_appraisal`); War: the Hostile Bid (`eotg_pluto_hostile_bid`); Trickster: the Discount (`eotg_pluto_discount`); Night: the Shortfall (`eotg_pluto_shortfall`); Water: the Flow (`eotg_pluto_flow`).
- House of worship: hoardhouse / hoardhouses (`eotg_pluto_house_of_worship`, `eotg_pluto_house_of_worship_plural`).
- Religious symbol: the Stamped Coin (`eotg_pluto_symbol`).
- Holy text: the Book of Takings (`eotg_pluto_text`).
- Title of head of faith and office: the Hoardmaster (`eotg_pluto_head`), office of the Hoardmaster (`eotg_pluto_head_title`).
- Ordinary believer: shareholder (male) / shareholder (female) / shareholders (plural) (`eotg_pluto_devotee_male`, `eotg_pluto_devotee_female`, `eotg_pluto_devotee_male_plural`). Wider adherent: Hoarder (`eotg_religion_plutocracy_adherent`).
- Priest: assessor (male) / assessor (female) / assessors (plural) (`eotg_pluto_priest_male`, `eotg_pluto_priest_female`, `eotg_pluto_priest_male_plural`; alternate plural: the assessors).
- Bishop-rank cleric: hoardmaster (male) / hoardmaster (female) / hoardmasters (plural) (`eotg_pluto_bishop_male`, `eotg_pluto_bishop_female`, `eotg_pluto_bishop_male_plural`).
- Afterlife: Good: the Great Vault (`eotg_pluto_positive_afterlife` / `eotg_pluto_divine_realm`); Bad: the Debtor's Pit (`eotg_pluto_negative_afterlife`).
- God of death: The Write-Off (`eotg_pluto_write_off`).
- Witch-god: The Loophole / Counterfeit.
- Holy war and fighters: Hostile Takeover / Hostile Takeovers (`eotg_pluto_ghw`, `eotg_pluto_ghw_plural`); fighters: Liquidators / Corporate Mercenaries.
- Pilgrimage and pilgrims: None (pilgrimage forbidden; trade routes serve as practical journeys).

## Faiths
For each faith:
### Goblin Plutocratic (`eotg_faith_goblin_plutocracy`)
- Name / adjective / what a believer is called: Goblin Plutocratic / Goblin Plutocratic / Shareholder (`eotg_faith_goblin_plutocracy_adj`, `eotg_faith_goblin_plutocracy_adherent`, `eotg_faith_goblin_plutocracy_adherent_plural`).
- Where it is dominant: The Charter Principalities ([The Charter Principalities](titles_charter_principalities.md)), dominant across the financial hubs of Broker's Reach and Halcyon Strip, led by Chancellor [Grezzik Gildspanner](ruler_grezzik_gildspanner.md) and Consul [Nibrak Coilmint](ruler_nibrak_coilmint.md).
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Tax Nonbelievers (`tenet_tax_nonbelievers`): Assessing mandatory tithes, tariff surcharges, and ledger fees upon unbelieving foreign merchants as a devotional obligation.
  2. Pursuit of Power (`tenet_pursuit_of_power`): Right of expansion, consolidation, and hostile acquisition justified through economic superiority.
  3. Adaptive (`tenet_adaptive`): Rapid doctrinal accommodation to foreign markets, shifting currencies, and advantageous peace treaties.
- Where it differs from the religion above (doctrine overrides): Inherits all religion-level doctrines without overrides.
- Holy sites (place, county, why):
  1. Broker's Deep (`c_eotg_brokers_deep`): The grand subterranean mint where the Gildspanner counting-vaults were first chartered.
  2. Gildhall (`c_eotg_gildhall`): The sovereign market exchange where all inter-cluster exchange rates are fixed.
  3. Xerxes Exchange (`c_eotg_new_xerxes`): Dome 2 commercial trading quarter, linking core wealth to outer march mining revenues.
- Colour: Acid Gold (`{ 0.75 0.8 0.2 }`).
- Founder, if historical: Unknown; credited to the original Founders of the Gildspanner Banking Syndicate (c. 300 AG).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:920-995`; `docs/lore/Third era Nations.md:1240-1280`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:1118-1126`.
