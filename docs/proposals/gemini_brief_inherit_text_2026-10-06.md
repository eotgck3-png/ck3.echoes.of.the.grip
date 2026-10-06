# Writing brief: A Fracturing Inheritance, event text (Gemini, round 1)

**For:** the external Gemini writing agent. **Date:** 2026-10-06.
**Deliver to:** `docs/proposals/inherit_text_gemini_r1.md`, and nowhere else. **Never edit `.yml` or `.txt` files.**
The project's localizer applies your draft once the lore-keeper and QA have reviewed it, against the built script.

## 0. Read first, in this order
1. `docs/proposals/gemini_rewrite_feedback_2026-10-06.md` §2 (setting), §3 (banned words and replacements) and §4 (rules for the text). **All of it applies.**
2. `docs/specs/cybernetics_v2_fracturing_inheritance.md`:
   - §5.3, the tree: what every event and option does;
   - §5A, the four profiles and five bonds;
   - §7, the loc surface: the key list, placeholders and the "true on every path" notes;
   - **§7.1, the lore wording fixes, which are binding**;
   - §8, the lore constraints.
3. `docs/proposals/kingpin_fragments_r1_apply_instructions.md`. It shows the kind of fixes your last draft needed; don't repeat them.

If this brief and the spec disagree, the spec wins. Tell us where they disagree.

## 1. What this is
A ruler's heir (`eotg_inh_heir`) has gone Neurofractured: an implant failure that makes the person unstable. The tree runs from the first signs through confrontation, confinement or attempts at control, to one of 17 endings. Among them, the heir kills the ruler, the heir empties the court, and the heir kills the next two in line. The other endings are confinement, exile by passage out, a faked death, disinheritance, regency, recovery and a cascade death.

Text varies along two axes (spec §5A):
- **Profile:** how the fracture shows. These are internal names; never use them in text.
  - **rage** ("Running Hot");
  - **ledger** (the heir trusts the implant's forecast of the heir's own body, and wrongly applies that certainty to other people);
  - **cold** (flat affect);
  - **certain** (grandiosity).
- **Bond:** what the heir is to the ruler: rival, estranged, claimant, favourite, dutiful.

## 2. What to write
**Every key in spec §7's table, events .001 to .027:** titles, descs and their variants, options and tooltips, plus the two modifiers. Event .028 is hidden and has no text. That's about 226 keys.
- Key form: `eotg_aug_inherit.<event>.<suffix>`, for example `eotg_aug_inherit.001.desc_rage`. The names come from spec §7. The scripter's build may rename a few; the localizer maps them.
- **Options:** read each option's effects in spec §5.3 before writing it. The text must not promise anything the option doesn't do. Where §7.1 or §5.3 gives fixed option wording, use it verbatim.
- **Descs** must be true on every path that shows them. Spec §7 lists the known traps: .006, .016, .017, .019, .021 and .026.

## 3. Rules
- **Length:** descs about 45–80 words; options 5–9 words; titles 2–4 words.
- **Placeholders:** bare form only, exactly as spec §7 lists them: `[eotg_inh_heir.GetFirstName]`, `[eotg_inh_heir.GetSheHe]`, `[eotg_inh_second.GetFirstName]`, `[eotg_inh_dead_1.GetFirstName]`, `[eotg_inh_witness.GetTitledFirstName]`, `[ROOT.Char.Custom('eotg_court_seat')]`.
  - Use `|U` when a line starts with a pronoun function: `[eotg_inh_heir.GetSheHe|U]`.
  - **Never `[scope:`. Never `GetHeir`.**
  - Never invent a scope or a person; use only those spec §7 lists. Unscoped people are described by role, with no gender.
- **Pronouns:** one scoped person takes GetSheHe, GetHerHis or GetHerHim. Never "they" for one person. Never assume the heir's gender.
- **Speech** goes in single quotes ('…'), **never `\"`**. Paragraph breaks are `\n\n` inside the quotes, with no literal newlines.
- **Voice:** the implant forecasts and logs **only its own user**. The heir may believe it predicts other people, as the ledger profile does, but the text must make clear that this is the heir's belief, never the machine's ability. The implant never "says", "speaks", "whispers" or "answers". Allowed verbs: *has [x] doing*, *runs [x] forward*, *shows*, *logs*, *flags*.
- **No eye implant.** No optical feeds, glowing eyes or irises. Don't assume where the implant sits beyond "the port" or "the casing".
- **Banned words.** Everything in feedback §3, plus:
  - from §7.1: tonight, today, dawn, morning, dungeon (use "the cells"), bury (use "lay to rest"), "the hardware" as a crutch, "half a second";
  - plus: registry, records office, certificate, warrant, authorities, magistrate, citizen, human, station, deck(s), breach, whisper(s), mortal, "No one…" as an opener.
  - Canadian spelling.
- **Death scenes:**
  - **The heir's suicide (.019):** found, not shown. Clinical, past tense, no method, no scene of discovery, no last words. Model sample from §7.1: "[eotg_inh_witness…] found [heir]'s quarters in perfect order. [heir] had answered every message, settled every account, and left nothing unfinished but [heir_herself]."
  - **Child victims (.016 `.child`):** one plain sentence, the name and the fact. No method, no scene.
- **Make the profiles and bonds sound different.**
  - Rage is heat, speed and interruption. Ledger is lists, certainty and figures. Cold is flat, polite and absent. Certain is grand and serene.
  - A rival heir resents, an estranged heir is a stranger, a claimant heir calculates, a favourite heir is the one you'd have chosen, and a dutiful heir is trying to stay good.
  - Don't give two variants the same sentence shape.
- **No institutions.** Disinheritance and exile are the ruler's own acts. No courts of law, no succession rolls.

## 4. Deliver
- One section per event. Each line is ` key:0 "text"`, with no `l_english:` header.
- Under each event, a short **truth note**: which paths show each desc and why your text holds on all of them.
- At the end, the ten words or phrases you used most, with their counts.
- **Report only checks you actually ran.** Your last draft claimed an "automated script" pairing test and a spelling check that didn't happen. If you didn't run a check, say so.
- After saving, re-open the file, confirm it isn't empty, and report its line count and the number of key lines. If you cannot write files, paste the whole draft into your reply.
