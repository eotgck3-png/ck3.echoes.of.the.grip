# Religion brief — The Faith of Elross

<!-- Cover the whole cluster in one brief: the family it belongs to, the religion, and each faith under it. The scripter builds all three tiers from this. -->

## Family
- Name (existing family, or new): Divine Order (`eotg_rf_divine_order`).
- How hostile it is to outsiders (tolerant / wary / hostile / at war with everyone): Hostile / Righteous (`doctrine_pluralism_righteous`, uses Abrahamic hostility doctrine; treats non-Divine Order faiths as evil and hostile, and treats dissident branches as heresies).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:5-83`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:1-41`.

## Religion
- Name: Elrossi (`eotg_religion_elross`).
- Core beliefs in a paragraph: Elross, Son of Yu, is the cosmic light that survived the catastrophic tearing of the Grip. Where his creator-father lies sealed in the Dream, Elross acts — and since the celestial resurgence of 850 AG he has been acting openly across the stars, blessing crusaders and marking the unworthy in ways that none can dismiss as mere coincidence. His faithful maintain that light is not an idle comfort but a strict moral and military obligation: justice owed, righteousness enforced with iron discipline, and the void dark pushed back one system at a time under the imperial banner.
- Head of faith? (none / spiritual / temporal) and who: Temporal head (`doctrine_temporal_head`), titled the Pontifex (`eotg_elross_head`), vested in the Emperor of the Second Elrossi Imperium in Elyria. In the forward marches of the Myr Clusters, imperial crusades are led by Arch-Legate [Corven Vultarre](../regions/myr_clusters/ruler_corven_vultarre.md) and Preceptor [Serapion Vale](../regions/myr_clusters/ruler_serapion_vale.md).
- Attitude to: gender roles, marriage and concubinage, divorce, bastards, close-kin marriage, homosexuality, adultery, kinslaying, witchcraft, deviancy. One line each; "no view" is fine:
  - Gender roles: Male-dominated (`doctrine_gender_male_dominated`).
  - Marriage and concubinage: Monogamous (`doctrine_monogamy`), concubinage disallowed.
  - Divorce: Allowed with pontifical / imperial approval (`doctrine_divorce_approval`).
  - Bastards: Legitimization permitted by imperial decree (`doctrine_bastardry_legitimization`).
  - Close-kin marriage: Aunt-nephew and uncle-niece permitted (`doctrine_consanguinity_aunt_nephew_and_uncle_niece`), sibling marriage forbidden.
  - Homosexuality: Shunned (`doctrine_homosexuality_shunned`).
  - Adultery: Men shunned, women considered a crime (`doctrine_adultery_men_shunned`, `doctrine_adultery_women_crime`).
  - Kinslaying: Close-kin kinslaying is considered a crime (`doctrine_kinslaying_close_kin_crime`).
  - Witchcraft: Considered a crime (`doctrine_witchcraft_crime`).
  - Deviancy: Considered a crime (`doctrine_deviancy_crime`).
- Clergy: who can be a priest, can they marry, who appoints them, do they pay tax: Male-only clergy (`doctrine_clerical_gender_male_only`). Clerical marriage is strictly disallowed (`doctrine_clerical_marriage_disallowed`). Clerics are appointed through spiritual fixed appointment (`doctrine_clerical_succession_spiritual_fixed_appointment`). Clergy perform taxation functions (`doctrine_clerical_function_taxation`). Stoic funeral rites (`doctrine_funeral_stoic`). Pilgrimage is encouraged (`doctrine_pilgrimage_encouraged`).
- Virtues and sins (three each, in words):
  - Virtues: Just, Brave, Zealous (`just`, `brave`, `zealous`).
  - Sins: Arbitrary, Craven, Cynical.
- Holy orders / warrior brotherhoods, if any: The Knights of the Luminary Sun; The Holy Order of Saint Argoth; The Palatines of Elyria.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:5-83`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:72-115, 405-449`.

## Vocabulary
The game fills vanilla strings from these. Give the in-world word for each: the name of the high god (and pronouns), an alternate name, good gods, evil gods, the devil figure, a house of worship (singular/plural), the religious symbol, the holy text, the title of the head of faith and of that office, an ordinary believer (m/f/plural), a priest (m/f/plural), a bishop-rank cleric (m/f/plural), the afterlife (good and bad), the god of death, the witch-god, a holy war and its fighters, a pilgrimage and pilgrims:
- High god: Elross (`eotg_god_elross`), pronouns he/him/his.
- Alternate name: the Light (`eotg_elross_light`).
- Good gods / Pantheon: The Choir of Yu (`eotg_elross_pantheon`) — Elross, Yu the Stained, Bohemut, Frozt.
- Evil gods: Malvrick, the Void.
- Devil figure: Malvrick / The Long Dark.
- Functional pantheon roles: Creator: Yu the Stained (`eotg_god_yu`); Health: Core the Flowing (`eotg_god_core`); Fertility: Solena (`eotg_god_solena`); Wealth: Serephios (`eotg_god_serephios`); Household: Thalvoria (`eotg_god_thalvoria`); Fate: Mystara (`eotg_god_mystara`); Knowledge: Bohemut (`eotg_god_bohemut`); War: Elross (`eotg_god_elross`); Trickster: Vexis (`eotg_god_vexis`); Night: Lunara (`eotg_god_lunara`); Water: Zephyrion (`eotg_god_zephyrion`).
- House of worship: cathedral / cathedrals (`eotg_elross_house_of_worship`, `eotg_elross_house_of_worship_plural`).
- Religious symbol: the Sunburst (`eotg_elross_symbol`).
- Holy text: the Luminary Canon (`eotg_elross_text`).
- Title of head of faith and office: the Pontifex (`eotg_elross_head`), office of the Pontifex (`eotg_elross_head_title`).
- Ordinary believer: faithful (male) / faithful (female) / faithful (plural) (`eotg_elross_devotee_male`, `eotg_elross_devotee_female`, `eotg_elross_devotee_male_plural`). Wider adherent: Elrossi (`eotg_religion_elross_adherent`).
- Priest: priest (male) / priestess (female) / priests (plural) (`eotg_elross_priest_male`, `eotg_elross_priest_female`, `eotg_elross_priest_male_plural`; alternate plural: the clergy).
- Bishop-rank cleric: bishop (male) / bishop (female) / bishops (plural) (`eotg_elross_bishop_male`, `eotg_elross_bishop_female`, `eotg_elross_bishop_male_plural`).
- Afterlife: Good: the Radiance (`eotg_elross_positive_afterlife` / divine realm: `eotg_elross_divine_realm`); Bad: the Long Dark (`eotg_elross_negative_afterlife`).
- God of death: Mystara.
- Witch-god: Vexis.
- Holy war and fighters: Crusade / Crusades (`eotg_elross_ghw`, `eotg_elross_ghw_plural`); fighters: Crusaders / Luminary Knights.
- Pilgrimage and pilgrims: Sacred Pilgrimage; pilgrims: Pilgrims / Wayfarers of the Sun.

## Faiths
For each faith:
### Orthodox Elrossi (`eotg_faith_elross_canonical`)
- Name / adjective / what a believer is called: Orthodox Elrossi / Orthodox Elrossi / Orthodox Elrossi (`eotg_faith_elross_canonical_adj`, `eotg_faith_elross_canonical_adherent`, `eotg_faith_elross_canonical_adherent_plural`).
- Where it is dominant: The Second Elrossi Imperium, pushing aggressively into the Lanius Expanse ([The Lanius Expanse](../regions/myr_clusters/titles_lanius_expanse.md)) via Lanius Systems and Starward Reach, held by Arch-Legate [Corven Vultarre](../regions/myr_clusters/ruler_corven_vultarre.md), Preceptor [Serapion Vale](../regions/myr_clusters/ruler_serapion_vale.md), and Tribune [Ilyr Kavos](../regions/myr_clusters/ruler_ilyr_kavos.md).
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Unrelenting Faith (`tenet_unrelenting_faith`): Fanatical devotion granting fierce combat bonuses against infidels and resistance to conversion.
  2. Armed Pilgrimages (`tenet_armed_pilgrimages`): Consecration of holy crusade conquests, righteous claims on foreign worlds, and discounts for sacred warfare.
  3. Legalism (`tenet_legalism`): Strict institutional codification where imperial edict and divine law are considered indistinguishable.
- Where it differs from the religion above (doctrine overrides): Enforces imperial centralisation and strict military discipline under the Pontifex.
- Holy sites (place, county, why):
  1. Elyria (Galactic Core): The Imperial Capital and High Cathedral of the Sunburst, seat of the Holy Roman / Byzantine-styled imperial Pontifex.
  2. Caer Myr (`c_eotg_caer_myr`): The historic elven planetary capital claimed by imperial crusade to subjugate the Prince of Myr.
  3. Saint Argoth's Hold (`c_eotg_saint_argoths_hold`): The frontier martyrium where Saint Argoth stood against Coldiron caliphate raiders in the 4th century.
- Colour: Radiant Imperial Gold (`{ 0.9 0.85 0.3 }`).
- Founder, if historical: Saint Argoth the Founder and Emperor Cassian I (c. 80 AG).
- Sources: `OLD PROJECT VERSION/docs/866_bookmark_design.md:43-46`; `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:5-83`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:72-80`.
