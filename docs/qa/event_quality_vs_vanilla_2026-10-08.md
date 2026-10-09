# Event quality against vanilla (2026-10-08)

**Question (owner):** what do the mod's events lack that vanilla events have, in dynamic text, length, dialogue and anything else a quality total conversion needs?

**Status:** assessment only. No events or loc were changed. Items marked **DECISION** are the owner's call; the others can go to eotg-architect, as with the dynamic-terms ruling.

**Method:**
- A script read every non-hidden event in vanilla 1.20 and in the mod. It extracted the same features from each, and resolved each event's description keys through loc.
  - Vanilla: 6,631 character events, of which 2,242 are recent DLC events, the "polished" baseline.
  - Mod: 243 character events and 6 activity events, from all files in `events/` (cybernetics, Frontier and the rest).
- eotg-vanilla-scout documented the conventions a count can't see (fields from `G/events/_events.info`, excerpts from ep3/bp2/fp3/ce1 events).
- Script and data: scratchpad `evq/evq.py`, `evq/evq.json`.

**Caveats:** the dialogue and voice detection is pattern-based, so treat it to ±5 points. Counts are of options as **defined**, not as shown to any one player.

## Owner decisions (2026-10-08)
These supersede the recommendations in findings 2–4 below.
1. **Narration voice follows vanilla's mix and stance.** It is no longer all second person.
   - Target the vanilla DLC proportions: about 60% first person (root narrates their own scene: "As I…", "my…"), about 35% neutral or third person (scene description, NPCs and their speech), and about 5% second person.
   - Second person is kept to letters (the sender addressing "you") and short option and outcome lines.
2. **Trait depth stays, but varies its gates.** Gated options should come from **different axes**:
   - personality traits;
   - education traits (`education_*`);
   - title tier (`highest_held_title_tier`), e.g. a duke's answer against a count's.

   They should not stack several personality traits on one event. There is no cap on option count; the aim is variety of who gets the special option, following vanilla's pattern: trait icon, trigger and stress entry together, and `skill =` for skill and education gates.
3. **Quote style follows vanilla.** Dialogue uses straight double quotes inside the loc string (`"…"`, the form in vanilla `hold_court.7000.desc`), with `#EMP …#!` for stress. The mod's single-quote dialogue converts to this.

## The numbers

| Feature | Vanilla, all | Vanilla, DLC | **Mod** |
|---|---|---|---|
| Theme set | 100% | 100% | 100% |
| `override_background` (a specific location) | 52% | **66%** | **0%** |
| 2D effect overlay (rain/fog/smoke) | — | 166 uses | 0 |
| Three or more portraits (witness or liege in a lower slot) | 20% | 30% | 9% |
| Distinct animations used | — | 250 | 44 |
| `triggered_animation` (reaction keyed to traits), per event | — | 0.37 | 0.09 |
| `outfit_tags` / `camera` | 3% / 8% | 3% / 14% | 0% / 0% |
| **Spoken dialogue in the description** | 52% | **54%** | **8%** |
| **Narration in first person / second person** | 65% / 4% | 61% / 5% | **0% / 52%** |
| Custom loc in the description (`Custom()`, relation words, form of address) | 33% | 29% | 9% |
| `#EMP` or other text formatting | 11% | 14% | 0% |
| Paragraph breaks (`\n\n`) in the description | 60% | 67% | 48% |
| `random_valid` description (variety on repeats) | 4% | 3% | 0% |
| `triggered_desc` used | 33% | 34% | **57%** |
| Median description words (main key) | 47 | 55 | 43 |
| 10th / 90th percentile description words | 20 / 84 | 13 / 91 | **30 / 54** |
| Median options defined, 90th percentile | 2, p90 4 | 3, p90 4 | **5, p90 6** |
| Options with a trait icon | — | **2%** | **31%** |
| `ai_chance` on every option | 53% | 76% | **97%** |
| Stress on an option | 42% | 60% | 61% |
| `add_internal_flag` (dangerous/special highlight) | 2% | 4% | 0% |
| Option `flavor =` line | 12% | 16% | 0% |
| Toasts per event (`send_interface_toast`) | — | 0.79 | 0.12 |
| `send_interface_message` (telling other players) | — | 211 | 0 |
| `play_music_cue` (deaths, murders) | — | 220 | 0 |
| Letter events | 665 | 225 | 0 |
| `after = {}` block | 27% | 28% | 14% |

What the mod already does as well as vanilla, or better:
- `ai_chance` on every option.
- Description variants through `triggered_desc`.
- Stress use.
- Theme always set.
- Title length.
- Option-text length.
- Scoped names in text (71%, against 87% in vanilla; the dynamic-terms ruling raises it further).

The gaps are in **presentation, voice and craft**, not in logic.

## Findings, by priority

### 1. The presentation is medieval by default (TC-critical)
The mod never sets `override_background`, so every event shows its theme's default background. Those are vanilla's rooms: `realm` and `intrigue` resolve to throne rooms and torchlit `corridor_night`, `medicine` to a period physician's study. A total conversion set in space currently shows its implant surgery, syndicate envoys and neural cascades in medieval rooms.
- **Short term, no art:** set `override_background` per event to the least anachronistic vanilla key for the beat:
  - `corridor_night` for sleepwalking and the missing courtier;
  - `physicians_study` or `bedchamber` for surgery and fever;
  - `dungeon` for restraints;
  - `council_chamber` for the delegation and warrant;
  - `docks` for Frontier convoys;
  - `alley_night` for back-street clinics;
  - `battlefield` / `army_camp`.
- Add `override_effect_2d = { reference = smoke }` or `fog` where the beat is literal: heat spike, the cascade, the bleed.
- **Long term (art, deferred):** mod `common/event_backgrounds/` with sci-fi plates (clinic, station corridor, hangar, bridge, slum level), and mod themes (`common/event_themes/`) such as `eotg_cybernetics`. A theme bundles icon, header, sound and background, so new backgrounds pick themselves up with no per-event work. This sits with the deferred icon and art backlog. **DECISION:** when art starts, this should come first; it is the most visible gap in the mod.
- Portrait outfits are the same problem; vanilla `outfit_tags` are period clothes. Visible implants on portraits are a separate art track.

### 2. Dialogue is rare (8%, against 54%)
Vanilla lets characters talk in roughly every second event, using straight `"` quotes inside the string, with `#EMP …#!` for stress. The mod mostly describes speech ("They speak of governance concerns", "They ask what the household should do"). The kingpin and inheritance files already show the mod can do it well: "'Sorry. It ran ahead of me again.'"
- Proposal: for every event with a named NPC who talks (vassals, envoys, physicians, the heir, the spouse, the delegation), give that NPC one line of direct speech.
- **House rule needed:** quote style. The mod uses single quotes `'…'`; vanilla uses `"`. Pick one, and add it to eotg_lint.

### 3. Narration voice: second person against vanilla's first person (**DECISION**)
Vanilla flavour-event descriptions are about 61% first person ("As I am relaxing in my…") and about 5% second person. Second person is reserved mostly for letters. The mod is 52% second person ("You wake with blood on your sleeve") and has no first-person narration. No spec mandates second person, so it accumulated rather than being chosen.
- Second person suits this content: dissociation, a voice that isn't quite yours. It is defensible as the mod's house voice, and it reads well.
- Converting about 360 description keys to first person would be a large rewrite and would change the tone.
- Recommendation: **keep second person as a deliberate house style**, write it into the loc style guide, and use first person only where the model's "we" plays against it. The point is that it becomes a choice, not drift.

### 4. Too many options, too often personality-gated (**DECISION**, because G9 trait depth was owner-approved)
The mod defines a median of 5 options (90th percentile 6), against vanilla's 2–3 (p90 4). 31% of mod options carry a trait icon, against 2% in vanilla DLC. Vanilla events offer situational choices, with a trait option as occasional spice. Many mod events read as "pick your personality". The per-player count is lower, but a character with 3–4 of the gated traits sees 6–7 options.
- Proposal:
  - cap shown options at about 4 (vanilla's p90);
  - where several trait options can show together, show at most one or two, using a `first_valid`-style priority in the triggers;
  - keep the rest for other characters.
- Also pair trait options vanilla's way: trait icon, `has_trait` trigger, and that trait's stress entry. Check that every trait option has its stress entry.

### 5. Outcomes are silent (0.12 toasts per event, against 0.79)
Vanilla surfaces consequences through `send_interface_toast` (good, bad or neutral) and tells other affected players with `send_interface_message`. The mod mostly changes variables and modifiers silently. That is especially costly for a hidden-meter system like fracture risk or the countdown.
- Proposal:
  - a toast on every delayed or rolled outcome (surgery results, Frontier stage changes, the syndicate's moves);
  - `send_interface_message` to players whose character is affected: the heir in heir events, a vassal hit by a policy;
  - mark risky options `add_internal_flag = dangerous` (excision while awake, handing over control, executing on a flag) and rare opportunities `special`. There are 0 today.

### 6. Portraits are less expressive
- The mod uses 44 animations; vanilla uses 250.
- The mod relies heavily on `worry`, `personality_rational` and `stress`.
- A trait-keyed `triggered_animation` appears 0.09 times per event, against 0.37.
- Third portraits appear in 9% of events, against 30%.

Proposals:
- triggered reactions on root (paranoid → `paranoia`, wrathful → `anger`, compassionate → `crying`; vanilla pattern `ep3_camp_temperament_events.txt:317-352`);
- role animations for NPCs (`physician`, `spymaster`, `chancellor`, `throne_room_bow_1`, `threatening`, `beg`);
- a lower portrait for witnesses (heir.005, the delegation, the Court Massacre);
- `outfit_tags = { nightgown }` for sleepless and sleepwalker scenes;
- `hide_info = yes` for anonymous syndicate couriers.

### 7. Text variety and set pieces
- **Length band is narrow.** The 10th to 90th percentile runs 30–54 words, against 13–91. The mod has neither very short beats nor long set pieces. The endgame deserves length and ceremony:
  - fracture.027 The Cascade, end.009 Hand Over the Controls, end.010 There Is No Static;
  - fracture.004 The Court Massacre, heir.005 What Must Be Done, end.002 Silence.
- **Set-piece tools (all 0 in the mod):**
  - `window = fullscreen_event` with `queue_icon` for the endgames;
  - `play_music_cue = mx_cue_death` (cascade deaths, executions) and `mx_cue_murder` (heir.005);
  - `override_effect_2d`.
  - All of these reuse vanilla assets, so no art is needed.
- **Repeatable events read identically every time.** `random_valid` is 0%. Tier flavour events that can fire more than once should rotate 2–3 openings.
- **Custom loc words** are at 9%, against 29%. Vanilla leans on `Custom2('RelationToMe')` ("my cousin [Name]"), `FormOfAddressForLiege` (NPCs addressing the ruler), `AppropriateGreeting`, and `random_valid` customizable keys for flavour nouns. The mod's own `eotg_aug_cl_*` keys show the technique is already in use, and it extends naturally:
  - implant slang;
  - clinic names;
  - a `random_valid` "static" vocabulary.
- **Paragraphing:** 48%, against 67%. Longer descriptions should break at the beat with `\n\n`.

### 8. Missing event types
- **Letter events: 0** (vanilla has 225 in DLC). The mod already writes letter-shaped beats as character events, and these should be `type = letter_event` with `opening` and `sender`:
  - patron.006 `*_absent` ("A courier brings the final account, sealed");
  - patron.009 (the debt is sold);
  - Frontier sponsor offers.
  - Use `window = anonymous_letter_event` for the unsigned syndicate notes.
- **Court events: 0.** Petitions such as tier1.003 (a vassal's question), tier1.004 (the knight's request) and tier2.007 (a petitioner) fit `type = court_event` in a royal court. Royal court is DLC-gated, so this is optional and needs a fallback.

### 9. 1.20 form
All 310 mod stress blocks use the old `stress_impact = {}`. 1.20 vanilla uses `stress_and_fulfillment_impact` (4,837 against 63 old-form uses in DLC). The old form still works: vanilla itself still has 174 uses. Tiger 1.17 doesn't know the new form, so converting now would add noise. **Hold** until Tiger is updated, then convert in one mechanical pass. Recorded here so it isn't forgotten.

## Suggested order

| # | Work | Owner | Art needed |
|---|---|---|---|
| 1 | Write the voice and quote-style rules into the loc guide (findings 2, 3) | DECISION, then architect | no |
| 2 | `override_background` + 2D effect per event, from vanilla's least-medieval keys | scripter | no |
| 3 | Toasts for outcomes, `dangerous`/`special` flags, `send_interface_message` | scripter | no |
| 4 | One line of NPC dialogue per eligible event | localizer, after lore on voice | no |
| 5 | Option cap and trait-option rotation (finding 4) | DECISION, then architect | no |
| 6 | Portrait pass: triggered animations, role animations, witnesses, outfits | scripter | no |
| 7 | Endgame set pieces: fullscreen, music cues, longer text | architect spec, then scripter and localizer | no |
| 8 | `random_valid` openings on repeatable events; more Custom loc | localizer | no |
| 9 | Letter-event conversions | scripter | no |
| 10 | Sci-fi event backgrounds, themes and outfits | art track | **yes** |
| 11 | `stress_and_fulfillment_impact` conversion | scripter, after Tiger updates | no |

Items 2–9 reuse vanilla assets, so none of them is blocked on art.

## References
- Vanilla conventions, with excerpts: `G/events/_events.info`; `G/common/event_themes/00_event_themes.txt`; `G/common/event_backgrounds/01_event_backgrounds.txt`; `G/common/event_2d_effects/event_2d_effects.txt`; `G/gfx/portraits/portrait_animations/animations.txt`.
- Model events:
  - `G/events/dlc/ep3/ep3_admin_events.txt` (desc block, triggered animation);
  - `ep3_camp_temperament_events.txt:317-352` (trait-keyed reactions);
  - `bp2_hostage_system.txt:675-760` (letter, `after`);
  - `ce1/legend_ending_events.txt:10-53` (fullscreen set piece);
  - `hold_court_events_james.txt` (court event, chain widget).
- Related: `docs/qa/loc_dynamic_terms_audit_2026-10-08.md`, `docs/specs/loc_dynamic_terms_ruling.md`.
