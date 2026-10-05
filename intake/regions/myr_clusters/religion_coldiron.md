# Religion brief — Coldiron

<!-- Cover the whole cluster in one brief: the family it belongs to, the religion, and each faith under it. The scripter builds all three tiers from this. -->

## Family
- Name (existing family, or new): Divine Order (`eotg_rf_divine_order`).
- How hostile it is to outsiders (tolerant / wary / hostile / at war with everyone): Hostile / Fundamentalist (`doctrine_pluralism_fundamentalist`; considers other faiths evil or heretical, especially the Elrossi orthodoxy with whom it contests divine authority).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:168-172`; `docs/lore/Third era Events.md:413-415`.

## Religion
- Name: Coldiron (`eotg_religion_coldiron`).
- Core beliefs in a paragraph: Frozt teaches through cold and through loss — not loss as an accidental misfortune, but loss as an uncompromising moral curriculum. Coldiron doctrine teaches that what is taken from you honestly was never owed to you, leaving the survivor harder, purer, and more enduring for its absence. Its warrior-monks and covenanters govern the frozen marches, viewing physical comfort as a dangerous form of spiritual dishonesty. Since 850 AG, Frozt has been answering their prayers directly, vindicating their rigorous martial discipline.
- Head of faith? (none / spiritual / temporal) and who: Temporal head (`doctrine_temporal_head`), titled the Caliph (`eotg_coldiron_head`). In 866 AG, held by Caliph [Marzuk al-Khadrin](ruler_marzuk_al_khadrin.md) from the fortress-palace of Yashuun.
- Attitude to: gender roles, marriage and concubinage, divorce, bastards, close-kin marriage, homosexuality, adultery, kinslaying, witchcraft, deviancy. One line each; "no view" is fine:
  - Gender roles: Male-dominated (`doctrine_gender_male_dominated`).
  - Marriage and concubinage: Polygamous (`doctrine_polygamy`), multiple lawful wives permitted.
  - Divorce: Allowed with caliphal approval (`doctrine_divorce_approval`).
  - Bastards: None / No bastardry distinction recognised (`doctrine_bastardry_none`; all acknowledged children inherit).
  - Close-kin marriage: Cousin marriage permitted (`doctrine_consanguinity_cousins`), immediate family forbidden.
  - Homosexuality: Considered a crime (`doctrine_homosexuality_crime`).
  - Adultery: Men accepted, women considered a crime (`doctrine_adultery_men_accepted`, `doctrine_adultery_women_crime`).
  - Kinslaying: Close-kin kinslaying is considered a crime (`doctrine_kinslaying_close_kin_crime`).
  - Witchcraft: Considered a crime (`doctrine_witchcraft_crime`).
  - Deviancy: Considered a crime (`doctrine_deviancy_crime`).
- Clergy: who can be a priest, can they marry, who appoints them, do they pay tax: Male-only clergy (`doctrine_clerical_gender_male_only`). Clergy are permitted to marry (`doctrine_clerical_marriage_allowed`). Clerics are appointed through temporal fixed appointment by the Caliph or local emirs (`doctrine_clerical_succession_temporal_fixed_appointment`). Clergy fulfil a recruitment and military muster function (`doctrine_clerical_function_recruitment`). Monasticism is strongly encouraged (`doctrine_monasticism_encouraged`). Stoic funeral rites (`doctrine_funeral_stoic`). Pilgrimage is mandatory (`doctrine_pilgrimage_mandatory`).
- Virtues and sins (three each, in words):
  - Virtues: Temperate, Patient, Brave (`temperate`, `patient`, `brave`).
  - Sins: Gluttonous, Impatient, Craven.
- Holy orders / warrior brotherhoods, if any: The Ironbound Monks of Frozt; the Caliphal Ghazis.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:168-245`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:47-50, 301-341`.

## Vocabulary
The game fills vanilla strings from these. Give the in-world word for each: the name of the high god (and pronouns), an alternate name, good gods, evil gods, the devil figure, a house of worship (singular/plural), the religious symbol, the holy text, the title of the head of faith and of that office, an ordinary believer (m/f/plural), a priest (m/f/plural), a bishop-rank cleric (m/f/plural), the afterlife (good and bad), the god of death, the witch-god, a holy war and its fighters, a pilgrimage and pilgrims:
- High god: Frozt (`eotg_god_frozt`), pronouns he/him/his.
- Alternate name: the Cold (`eotg_coldiron_cold`).
- Good gods / Pantheon: The Cold Host (`eotg_coldiron_pantheon`) — Frozt, Yu the Stained, Elross, Thalvoria.
- Evil gods: Malvrick, the Void.
- Devil figure: The Thaw (`eotg_coldiron_negative_afterlife`).
- House of worship: chapterhouse / chapterhouses (`eotg_coldiron_house_of_worship`, `eotg_coldiron_house_of_worship_plural`).
- Religious symbol: the Riven Iron (`eotg_coldiron_symbol`).
- Holy text: the Covenant (`eotg_coldiron_text`).
- Title of head of faith and office: the Caliph (`eotg_coldiron_head`), office of the Caliph (`eotg_coldiron_head_title`).
- Ordinary believer: covenanter (male) / covenanter (female) / covenanters (plural) (`eotg_coldiron_devotee_male`, `eotg_coldiron_devotee_female`, `eotg_coldiron_devotee_male_plural`). Wider adherent: Ironbound (`eotg_religion_coldiron_adherent`).
- Priest: monk (male) / sister (female) / monks (plural) (`eotg_coldiron_priest_male`, `eotg_coldiron_priest_female`, `eotg_coldiron_priest_male_plural`; alternate plural: the sworn).
- Bishop-rank cleric: abbot (male) / abbess (female) / abbots (plural) (`eotg_coldiron_bishop_male`, `eotg_coldiron_bishop_female`, `eotg_coldiron_bishop_male_plural`).
- Afterlife: Good: the White Silence (`eotg_coldiron_positive_afterlife` / `eotg_coldiron_divine_realm`); Bad: the Thaw (`eotg_coldiron_negative_afterlife`).
- God of death: Frozt / Mystara.
- Witch-god: Vexis (`eotg_god_vexis`).
- Holy war and fighters: Covenant War / Covenant Wars (`eotg_coldiron_ghw`, `eotg_coldiron_ghw_plural`); fighters: Ghazis / Sworn Covenanters.
- Pilgrimage and pilgrims: Mandatory Ice Pilgrimage; pilgrims: Hajji / Ice Pilgrim.

## Faiths
For each faith:
### Covenant (`eotg_faith_coldiron`)
- Name / adjective / what a believer is called: Covenant / Covenant / Covenanter (`eotg_faith_coldiron_adj`, `eotg_faith_coldiron_adherent`, `eotg_faith_coldiron_adherent_plural`).
- Where it is dominant: The Coldiron Marches ([The Coldiron Marches](titles_coldiron_marches.md)), encompassing the Coldiron March, Aegis Corridor, and Sable Verge, governed by Caliph [Marzuk al-Khadrin](ruler_marzuk_al_khadrin.md), Emir [Qadir al-Khadrin](ruler_qadir_al_khadrin.md), and Sheikh [Samir al-Khadrin](ruler_samir_al_khadrin.md).
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Exaltation of Pain (`tenet_exaltation_of_pain`): Spiritual purification achieved through bodily endurance, freezing mortification, and stoic battle trauma.
  2. Monasticism (`doctrine_monasticism_encouraged` / `tenet_monasticism`): Pervasive martial-monastic orders that drill recruits and preserve caliphal scripture.
  3. Asceticism (`tenet_asceticism`): Renunciation of luxury, vanity, and unnecessary planetary comforts in favour of survivalist purity.
- Where it differs from the religion above (doctrine overrides): Enforces strict martial-monastic encampment codes across all frontier redoubts.
- Holy sites (place, county, why):
  1. Yashuun (`c_eotg_yashuun`): Seat of the Caliph and site of the Grand Glacier Chapterhouse where the First Covenant was inscribed on meteorite iron.
  2. Coldiron (`c_eotg_coldiron`): The frozen fortress-world where Frozt answered the founding ghazis during the First Crusade defense.
  3. Saint Argoth's Hold (`c_eotg_saint_argoths_hold`): The frontier redoubt contested between the Caliphate and Elrossi crusaders, sanctified by fallen covenanters.
- Colour: Steel Blue (`{ 0.3 0.5 0.8 }`).
- Founder, if historical: First Caliph Tariq al-Khadrin (c. 120 AG), who codified the Covenant during the post-Grip ice storms.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:168-245`; `docs/lore/Third era Events.md:413-415, 514`; `docs/lore/Third era Nations.md:1241-1310`.
