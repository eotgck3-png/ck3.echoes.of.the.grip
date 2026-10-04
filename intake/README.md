# Intake — lore briefs for the builders

**For:** the agent (Gemini or otherwise) exporting lore from the Obsidian vault into this repo, and the Claude agents that read the result. Read this whole file before writing a brief.

## What this is

`intake/` is where the setting is handed to the people who build it. Each brief is a Markdown document, written from the vault, that tells a builder *what exists* in a region — its polities, cultures, faiths, rulers, dynasties, titles — and *what matters most*. The Claude agents read the briefs and author the CK3 script themselves, using their own judgement about how to map prose to traits, tenets, traditions, and province counts. Nothing here is parsed by a program.

```
Obsidian vault ──(exporter writes briefs)──▶ intake/regions/<region>/  and  intake/setting/
        ──(eotg-intake reads, checks completeness, writes a build order)──▶ docs/specs/regions/<region>.md
        ──(cartographer / scripter / localizer build)──▶ common/  history/  localization/
        ──(lore-keeper checks the result against the briefs)
```

## Layout

```
intake/
  README.md                 this file
  templates/                one template per brief type — copy, keep the headings
  setting/                  briefs that span regions: religion families, wide-spread cultures, pan-galactic dynasties
  regions/<region>/
    REGION.md               the master brief for the region — always start here
    titles_<polity>.md      one per polity (kingdom / empire): the title tree and holders
    ruler_<name>.md         one per character who holds a title or leads a bookmark
    dynasty_<name>.md
    culture_<name>.md       cultures specific to this region (shared ones go in setting/)
    religion_<name>.md      faith clusters specific to this region (shared ones go in setting/)
```

Region folder names: lower-case, underscores, no diacritics (`myr_cluster`, `titan_reach`). Brief filenames follow the pattern above so a builder can glob them.

## How to write a brief

- Start from the matching file in `templates/`. **Keep every heading**, even if the answer under it is "Unknown" or "Nothing" — a missing heading looks like an omission; an explicit "Unknown" is an answer.
- Prose and bullets are both fine. Tables are fine. Write for a reader who has never opened the vault.
- **Say what the vault says.** Do not smooth over gaps or invent names, dates, or relationships to make a section look complete. If the vault contradicts itself, say so and quote both.
- **Sources** under each section: the vault note paths (and headings) the section was drawn from. Builders and the lore-keeper use these to go back to the vault when something needs checking.
- Link between briefs with relative links (`[Arren Halvard](ruler_arren_halvard.md)`), so a builder can walk from a region to its polities to their rulers.
- Names in the game will be exactly what you write in the brief. Spell them the way the vault does; put the ASCII form beside any name with diacritics.
- Dates are years After the Grip (AG). Month and day only if the vault has them.
- One region per export batch. Ship the `REGION.md` first, then the polity title briefs, then rulers and dynasties, then anything region-specific for cultures and faiths. Setting-wide briefs (`setting/`) go before the first region that depends on them.

## What a builder needs most (in priority order)

1. **REGION.md** with a real map footprint and build priorities — without it nobody knows how many provinces to draw or what to build first.
2. **Title briefs** with a full tree down to baronies and a holder for every county and above.
3. **Ruler briefs** for every holder named in a title brief.
4. **Religion and culture briefs** for every faith and culture named in a ruler brief — the game cannot load a character whose culture or faith does not exist.
5. Dynasties, holy sites, hooks.

## Things the project is firm about

- Landed title keys are **tier-first**: `k_eotg_veltran`, never `eotg_k_veltran`. If you suggest keys, use that form; if unsure, give names and let the builder key them.
- Every other identifier the builder creates will start with `eotg_`; you do not need to write identifiers at all — names are enough.
- Faiths have exactly **three** tenets. Religions have none.
- The 866 AG fixed points are canon: the Grip was 866 years ago and is living history; the Titan Exodus is ongoing; the Myr Cluster Wars ignited 850 AG; there is no Galactic League yet.
- **Nikios Khanate** content is deferred by the project owner. Do not export it yet.

## What happens after a brief lands

`eotg-intake` reads the region folder, checks it against the template headings and the priority list above, and writes a **build order** to `docs/specs/regions/<region>.md`: what can be built now, what is blocked on an unanswered "Open question", which briefs are referenced but missing. Gaps come back to the vault as a list of questions, phrased against your Sources lines. Builders then work from the build order and the briefs together; the lore-keeper reviews what they produce against the briefs.
