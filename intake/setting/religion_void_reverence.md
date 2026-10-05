# Religion brief — Void Reverence

<!-- Cover the whole cluster in one brief: the family it belongs to, the religion, and each faith under it. The scripter builds all three tiers from this. -->

## Family
- Name (existing family, or new): Titan Worship (`eotg_rf_titan_worship`).
- How hostile it is to outsiders (tolerant / wary / hostile / at war with everyone): Hostile / Fundamentalist (`doctrine_pluralism_fundamentalist`, pagan hostility doctrine; outlawed across civilized space; treats all orthodox light-faiths as mortal adversaries).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:417-421`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:25-30`.

## Religion
- Name: Void-Reverent (`eotg_religion_void_reverence`).
- Core beliefs in a paragraph: Malvrick, the unwanted son of Yu, holds the dark, the unlit depths, and the cosmic Void — a metaphysical abyss that was constructed as a prison for the primordial entity Orrin. The prison no longer holds him, yet the Void has not gone quiet. Voidwalkers were systematically hunted across five centuries by Elrossi crusaders and are officially proclaimed extinct, but clandestine covens endure. They venerate the catastrophic breach of the Grip itself as the single moment the universe ceased dissembling and revealed its brutal, unlit nature, seeking communion with what still whispers from the empty cell.
- Head of faith? (none / spiritual / temporal) and who: None / Hidden spiritual guide (`doctrine_no_head`, `doctrine_theocracy_lay_clergy`), though underground covens whisper reverence to the legendary Silent Speaker (`eotg_void_head`).
- Attitude to: gender roles, marriage and concubinage, divorce, bastards, close-kin marriage, homosexuality, adultery, kinslaying, witchcraft, deviancy. One line each; "no view" is fine:
  - Gender roles: Equal (`doctrine_gender_equal`).
  - Marriage and concubinage: Concubines permitted (`doctrine_concubines`), fluid dark covenants.
  - Divorce: Allowed (`doctrine_divorce_allowed`).
  - Bastards: All legitimate (`doctrine_bastardry_all`).
  - Close-kin marriage: Unrestricted consanguinity (`doctrine_consanguinity_unrestricted`).
  - Homosexuality: Accepted (`doctrine_homosexuality_accepted`).
  - Adultery: Both men and women accepted (`doctrine_adultery_men_accepted`, `doctrine_adultery_women_accepted`).
  - Kinslaying: Kinslaying is accepted (`doctrine_kinslaying_accepted`).
  - Witchcraft: Virtuous (`doctrine_witchcraft_virtuous`), communion with void entities is sacred.
  - Deviancy: Virtuous (`doctrine_deviancy_virtuous`).
- Clergy: who can be a priest, can they marry, who appoints them, do they pay tax: Lay clergy (`doctrine_theocracy_lay_clergy`), either gender may serve (`doctrine_clerical_gender_either`). Clergy are permitted to marry (`doctrine_clerical_marriage_allowed`). Clerics are appointed through spiritual appointment (`doctrine_clerical_succession_spiritual_appointment`). Clergy fulfil an alms and pacification function (`doctrine_clerical_function_alms_and_pacification`). Sky burial funeral rites (`doctrine_funeral_sky_burial`; bodies exposed to open void space). Pilgrimage consists of local secret rites (`doctrine_pilgrimage_local_rites`).
- Virtues and sins (three each, in words):
  - Virtues: Eccentric, Ambitious, Callous (`eccentric`, `ambitious`, `callous`).
  - Sins: Content, Craven, Compassionate.
- Holy orders / warrior brotherhoods, if any: The Unlit Brotherhood; The Harbingers of the Tear.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:417-498`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:494-535, 611-615`.

## Vocabulary
The game fills vanilla strings from these. Give the in-world word for each: the name of the high god (and pronouns), an alternate name, good gods, evil gods, the devil figure, a house of worship (singular/plural), the religious symbol, the holy text, the title of the head of faith and of that office, an ordinary believer (m/f/plural), a priest (m/f/plural), a bishop-rank cleric (m/f/plural), the afterlife (good and bad), the god of death, the witch-god, a holy war and its fighters, a pilgrimage and pilgrims:
- High god: Malvrick (`eotg_god_malvrick`), pronouns he/him/his.
- Alternate name: the Unwanted Son (`eotg_void_unwanted`).
- Good gods / Pantheon: The Unlit (`eotg_void_pantheon`) — Malvrick, Carrigore (`eotg_god_carrigore`), Gorgath, Orrin the Eye (`eotg_god_orrin`).
- Evil gods / Devil: The Light (`eotg_void_negative_afterlife`) / Elross (the false sun that blinds mortals).
- Functional pantheon roles: Creator: Yu the Stained (`eotg_god_yu`); Health: Sanguis (`eotg_god_sanguis`); Fertility: Sanguis; Wealth: Vexis (`eotg_god_vexis`); Household: Malvrick; Fate: Gorgath (`eotg_god_gorgath`); War: Orrin the Eye; Trickster: Ikarath (`eotg_god_ikarath`); Night: Malvrick; Water: Carrigore.
- House of worship: breachhouse / breachhouses (`eotg_void_house_of_worship`, `eotg_void_house_of_worship_plural`).
- Religious symbol: the Tear (`eotg_void_symbol`).
- Holy text: the Hollow Canon (`eotg_void_text`).
- Title of head of faith and office: the Silent Speaker (`eotg_void_head`), office of the Silent Speaker (`eotg_void_head_title`).
- Ordinary believer: grip-touched (male) / grip-touched (female) / grip-touched (plural) (`eotg_void_devotee_male`, `eotg_void_devotee_female`, `eotg_void_devotee_male_plural`). Wider adherent: Voidwalker (`eotg_religion_void_reverence_adherent`).
- Priest: celebrant (male) / celebrant (female) / celebrants (plural) (`eotg_void_priest_male`, `eotg_void_priest_female`, `eotg_void_priest_male_plural`; alternate plural: the celebrants).
- Bishop-rank cleric: warden of the tear (male) / warden of the tear (female) / wardens of the tear (plural) (`eotg_void_bishop_male`, `eotg_void_bishop_female`, `eotg_void_bishop_male_plural`).
- Afterlife: Good: the Quiet (`eotg_void_positive_afterlife` / divine realm: the Void `eotg_void_divine_realm`); Bad: the Light (`eotg_void_negative_afterlife`).
- God of death: Orrin the Eye.
- Witch-god: Malvrick / Ikarath.
- Holy war and fighters: Unmaking / Unmakings (`eotg_void_ghw`, `eotg_void_ghw_plural`); fighters: Grip-Touched / Void Harbingers.
- Pilgrimage and pilgrims: Rift Pilgrimage; pilgrims: Tear-Seekers / Celebrants.

## Faiths
For each faith:
### Grip-Touched (`eotg_faith_void_cult`)
- Name / adjective / what a believer is called: Grip-Reverent / Grip-Reverent / Grip-Touched (`eotg_faith_void_cult_adj`, `eotg_faith_void_cult_adherent`, `eotg_faith_void_cult_adherent_plural`).
- Where it is dominant: Subterranean breach ruins, isolated asteroid rifts, and fringe frontier star systems across the galaxy (including clandestine cells in Dead Reach and Rust Verge).
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Esotericism (`tenet_esotericism`): Pursuit of occult cosmic truths, astrological rift divination, and forbidden void philosophy.
  2. Sacred Destruction (`tenet_sacred_destruction`): Religious conviction that breaking stagnant material forms liberates latent cosmic energy.
  3. Human Sacrifice (`tenet_human_sacrifice`): Blood rites and physical offerings cast into open rift anomalies to propitiate the Unlit.
- Where it differs from the religion above (doctrine overrides): Inherits all religion-level doctrines without overrides.
- Holy sites (place, county, why):
  1. The Great Rift Core: The deep-space metaphysical epicenter where the fabric of reality tore in 0 AG.
  2. Dead Reach Chasm (`c_eotg_dead_reach`): An abyssal rift fissure in the Outer Marches where derelicts vanish into silent gravity folds.
  3. The Unlit Tear (`c_eotg_rust_verge`): Subterranean tear sanctuary where the void cult conducts secret blood initiations.
- Colour: Deep Void Purple (`{ 0.2 0.0 0.4 }`).
- Founder, if historical: Unknown; emergent from the surviving witnesses of the Grip in 0 AG.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:417-498`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:494-535`.
