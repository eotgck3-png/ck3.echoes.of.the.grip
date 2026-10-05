# Religion brief — Firstlight

<!-- Cover the whole cluster in one brief: the family it belongs to, the religion, and each faith under it. The scripter builds all three tiers from this. -->

## Family
- Name (existing family, or new): Divine Order (`eotg_rf_divine_order`).
- How hostile it is to outsiders (tolerant / wary / hostile / at war with everyone): Wary to hostile (uses Abrahamic hostility doctrine; treats other families as hostile or evil, but coexists tensely with other Divine Order faiths).
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:500-503`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:45-46`.

## Religion
- Name: Firstlight (`eotg_religion_firstlight`).
- Core beliefs in a paragraph: The elven light-faith is older than the Elrossi canon and steadfastly unwilling to be absorbed into it. The Firstlight holds that cosmic light did not begin with the god Elross and belongs to no imperial hierarchy — it was first, existed before the calamity of the Grip, and will outlast whoever currently claims temporal or spiritual authority over it. Its priesthood teaches that sacred light asks to be tended rather than obeyed, honouring dawn observances, unbroken lamps, and ancestral vigilance against the encroaching dark.
- Head of faith? (none / spiritual / temporal) and who: Spiritual head (`doctrine_spiritual_head`), titled the Lampwarden (`eotg_firstlight_head`). Position vacant or held by the venerable high lamptender in the ancient elven retreats of Old Xerxes at 866 AG.
- Attitude to: gender roles, marriage and concubinage, divorce, bastards, close-kin marriage, homosexuality, adultery, kinslaying, witchcraft, deviancy. One line each; "no view" is fine:
  - Gender roles: Equal (`doctrine_gender_equal`).
  - Marriage and concubinage: Monogamous (`doctrine_monogamy`), concubinage disallowed.
  - Divorce: Allowed with religious approval (`doctrine_divorce_approval`).
  - Bastards: Legitimization permitted (`doctrine_bastardry_legitimization`).
  - Close-kin marriage: Cousin marriage permitted (`doctrine_consanguinity_cousins`), immediate family forbidden.
  - Homosexuality: Accepted (`doctrine_homosexuality_accepted`).
  - Adultery: Both men and women shunned (`doctrine_adultery_men_shunned`, `doctrine_adultery_women_shunned`).
  - Kinslaying: Close-kin kinslaying is considered a crime (`doctrine_kinslaying_close_kin_crime`).
  - Witchcraft: Shunned (`doctrine_witchcraft_shunned`).
  - Deviancy: Shunned (`doctrine_deviancy_shunned`).
- Clergy: who can be a priest, can they marry, who appoints them, do they pay tax: Either gender may serve as clergy (`doctrine_clerical_gender_either`). Clergy are permitted to marry (`doctrine_clerical_marriage_allowed`). Clerics are appointed through spiritual succession (`doctrine_clerical_succession_spiritual_appointment`). Clergy pay taxes to secular rulers (`doctrine_clerical_function_taxation`). Cremation is standard funeral practice (`doctrine_funeral_cremation`). Pilgrimage is encouraged (`doctrine_pilgrimage_encouraged`).
- Virtues and sins (three each, in words):
  - Virtues: Patient, Compassionate, Humble (`patient`, `compassionate`, `humble`).
  - Sins: Impatient, Callous, Arrogant.
- Holy orders / warrior brotherhoods, if any: None active at 866 AG; the ancient Lampwarden Guard was dispersed during the drowning of Old Xerxes.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:500-530`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:42-45, 687-730`.

## Vocabulary
The game fills vanilla strings from these. Give the in-world word for each: the name of the high god (and pronouns), an alternate name, good gods, evil gods, the devil figure, a house of worship (singular/plural), the religious symbol, the holy text, the title of the head of faith and of that office, an ordinary believer (m/f/plural), a priest (m/f/plural), a bishop-rank cleric (m/f/plural), the afterlife (good and bad), the god of death, the witch-god, a holy war and its fighters, a pilgrimage and pilgrims:
- High god: the Firstlight (`eotg_firstlight_firstlight`), pronouns it/its.
- Alternate name: the First Dawn (`eotg_firstlight_dawn`).
- Good gods / Pantheon: The Kindled (`eotg_firstlight_pantheon`) — Elross, Yu the Stained, Lunara, Solena.
- Evil gods: Malvrick (`eotg_god_malvrick`), the Void.
- Devil figure: The Guttering (`eotg_firstlight_negative_afterlife`) / Malvrick.
- House of worship: lamphall / lamphalls (`eotg_firstlight_house_of_worship`, `eotg_firstlight_house_of_worship_plural`).
- Religious symbol: the Unbroken Lamp (`eotg_firstlight_symbol`).
- Holy text: the Dawnsong (`eotg_firstlight_text`).
- Title of head of faith and office: the Lampwarden (`eotg_firstlight_head`), office of the Lampwarden (`eotg_firstlight_head_title`).
- Ordinary believer: firstlit (male) / firstlit (female) / firstlit (plural) (`eotg_firstlight_devotee_male`, `eotg_firstlight_devotee_female`, `eotg_firstlight_devotee_male_plural`).
- Priest: lamptender (male) / lamptender (female) / lamptenders (plural) (`eotg_firstlight_priest_male`, `eotg_firstlight_priest_female`, `eotg_firstlight_priest_male_plural`; alternate plural: the tenders).
- Bishop-rank cleric: dawnwarden (male) / dawnwarden (female) / dawnwardens (plural) (`eotg_firstlight_bishop_male`, `eotg_firstlight_bishop_female`, `eotg_firstlight_bishop_male_plural`).
- Afterlife: Good: the First Morning (`eotg_firstlight_positive_afterlife` / `eotg_firstlight_divine_realm`); Bad: the Guttering (`eotg_firstlight_negative_afterlife`).
- God of death: Mystara (`eotg_god_mystara`).
- Witch-god: Vexis (`eotg_god_vexis`).
- Holy war and fighters: Kindling / Kindlings (`eotg_firstlight_ghw`, `eotg_firstlight_ghw_plural`); fighters: Dawnkeepers / Kindled Blades.
- Pilgrimage and pilgrims: Dawn Pilgrimage; pilgrims: Lamptenders / Dawnseekers.

## Faiths
For each faith:
### Firstlit (`eotg_faith_firstlight`)
- Name / adjective / what a believer is called: Firstlit / Firstlit / Firstlit (`eotg_faith_firstlight_adj`, `eotg_faith_firstlight_adherent`, `eotg_faith_firstlight_adherent_plural`). Adherent of the wider religion is called Dawnkeeper (`eotg_religion_firstlight_adherent`).
- Where it is dominant: The Myr Core ([The Myr Core](titles_myr_core.md)), specifically across elven territories in Xerxes Reach, Aphionian Belt, and Coreward Expanse held by Prince [Vaelorin Sylvaerath](ruler_vaelorin_sylvaerath.md), Princess [Lyssa Varayne](ruler_lyssa_varayne.md), and Baroness [Lireth Davan](ruler_lireth_davan.md).
- The three tenets that define it (in words; the builder maps to CK3 tenets):
  1. Sun Worship (`tenet_sun_worship`): Sacred reverence for light, stars, and radiant energy as the primal ordering force.
  2. Ritual Celebrations (`tenet_ritual_celebrations`): Communal ceremonies of kindling and remembrance at every dawn and solar cycle.
  3. Pursuit of Knowledge (`tenet_pursuit_of_knowledge`): Preservation of pre-Grip chronicles, stellar navigation, and natural philosophies.
- Where it differs from the religion above (doctrine overrides): Inherits all religion-level doctrines without overrides.
- Holy sites (place, county, why):
  1. Old Xerxes (`c_eotg_old_xerxes`): The submerged pre-Grip provincial capital where the First Lamp was lit; pilgrimage destination despite tidal drowning.
  2. Aphiona (`c_eotg_aphiona`): Ancient monastic retreat of the first dawnwardens, preserving undisturbed astronomical astrolabes.
  3. Caer Myr (`c_eotg_caer_myr`): The ancestral citadel of the High Prince of Myr, marking the confluence of coreward ley-lines.
- Colour: Pale Dawn Gold (`{ 0.95 0.9 0.5 }`).
- Founder, if historical: Unknown; predates the Grip and is ascribed to the legendary First Dawnkeepers of the First Era.
- Sources: `OLD PROJECT VERSION/common/religion/religion_types/eotg_religions.txt:500-580`; `docs/lore/Third era Nations.md:1240-1260`; `OLD PROJECT VERSION/localization/english/eotg_religions_l_english.yml:686-730`.
