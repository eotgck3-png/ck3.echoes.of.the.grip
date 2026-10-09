# Spec addendum: W7 endgame set pieces (event_quality_v1)

**Author:** eotg-architect, 2026-10-09
**Parent:** [`event_quality_v1.md`](event_quality_v1.md) §11 W7. The parent spec's rules bind here unless this file says otherwise: §8 lore, §12 voice and quotes, §14 backgrounds.
**Approval:** NEW content, approved by the owner on 2026-10-09 (Q2). Tone ruled the same day (Q3): the Seamless fade is staged once, at the threshold, as a record.
**State read:** the working tree on `v2-space-map` after 25eb918 (W2 landed). W3 is in flight on the same event files. No `play_music_cue` or `add_internal_flag` existed in `events/` when this was written. Vanilla is 1.20.0.3; every vanilla path and line below was checked this session.

---

## 1. Purpose & gate

Six terminal or near-terminal beats of the cybernetics endgame currently use the same small window, the same length and the same silence as a yearly flavour event. This addendum stages them as **set pieces**. Each gets `window = big_event_window`, 90 to 140 words in 2 to 4 `\n\n` paragraphs, a 2D effect (and vanilla VFX widgets where they fit), one opening music cue, and deliberate portrait staging. Later, when art exists, some move to `fullscreen_event`.

**A set piece presents an outcome. It never changes one.** Event ids, callers, triggers, option sets, option effects, `ai_chance` and every `random_list` weight stay exactly as they are. W7 changes only presentation fields (window, effect, widgets, portraits, music) and the text of existing loc keys.

**Gate:** same basis as the parent (§1): mod-exclusive cybernetics, with no title, province, culture or faith dependency. Not blocked by Gate 1.

---

## 2. Signature resource

The parent's signature measure (the scorecard) applies: length, paragraphing, background, effect and music columns. W7 also **protects** the cybernetics resources. These six events move or end `eotg_fracture_risk`, change tier (Seamless, Excision, death) and read `eotg_aug_voice`. The set piece leaves every one of those moves byte-identical. `risk_moves.py` and `option_outcomes.py` must show no change for `eotg_augmentation_fracture.txt`, `eotg_augmentation_endgame.txt` and `eotg_augmentation_heir.txt` beyond the W3 additions (§5).

---

## 3. Identifier table

| Key | Type | Owner | Notes |
|---|---|---|---|
| `eotg_cascade_witness` | saved scope (presentation only) | eotg-scripter | fracture.027 right portrait (§6.1). Set in `immediate` inside `hidden_effect`; read by nothing else. |
| `eotg_surgeon` | saved scope (existing name, reused) | eotg-scripter | end.002 re-saves the court physician the way end.001 does (`eotg_augmentation_endgame.txt:96-103`), only when it doesn't already exist. |
| `eotg_witness` | saved scope (presentation only) | eotg-scripter (W6) | Proposed name for the W6 witness portrait on fracture.004 and heir.005 (parent §11 W6). If W6 lands a different name, W7 uses that. |
| Existing loc keys of the six events | loc text | eotg-localizer | Text replaced; **no new loc keys**. The full list is in §7. |
| *(deferred)* `eotg_bg_fs_cascade`, `eotg_bg_fs_threshold`, `eotg_bg_fs_succession` | fullscreen background keys | eotg-scripter, after art | §9. Not created now. |
| *(deferred)* `gfx/interface/icons/splash_icons/eotg_splash_cybernetics.dds` | fullscreen `queue_icon` | art, then eotg-scripter | §9. One icon shared by every cybernetics fullscreen event. |

No new events, namespaces, flags, variables, modifiers, effects or on_actions. Vanilla keys used (all verified): window `big_event_window`; 2D effects `smoke`, `fog`, `legend_glow`; VFX widgets `event_window_widget_vfx_background_double_vision_severe`, `event_window_widget_vfx_left_character_double_vision_severe`, `event_window_widget_vfx_background_double_vision_milder`, `event_window_widget_vfx_left_character_double_vision_milder`, `event_window_widget_vfx_heavy_smoke`, `event_window_widget_vfx_background_night_scene`, `event_window_widget_vfx_left_character_night_scene`; music and animation keys in §6.

---

## 4. File placement

| What | Path |
|---|---|
| Event edits (presentation fields only) | `events/eotg_augmentation_fracture.txt` (fracture.004, .027), `events/eotg_augmentation_endgame.txt` (end.002, .009, .010), `events/eotg_augmentation_heir.txt` (heir.005) |
| Loc text | `localization/english/eotg_augmentation_l_english.yml` (all keys are already there, lines 323-332, 721-732, 785-790, 814-837) |
| Background mapping | no new key. §14.2 of the parent changes for two events only (§6.5, §6.6). |

---

## 5. Wiring, and coordination with W3

**No wiring changes.** Each set piece is the existing event, fired by its existing caller:

| Set piece | Event | Fired by (unchanged) | Position in the chain |
|---|---|---|---|
| The Cascade | `eotg_fracture.027` | NF on_action terminal step, risk ≥ 95, `eotg_flag_aug_terminal_cooldown` | Terminal fork of chain 6 (story_chains_overview §6): death, Seamless (→ end.010), Excision (→ end.001), abdication (→ end.030), it passes (→ fracture.029) |
| Hand Over the Controls | `eotg_aug_end.009` | `eotg_decision_aug_embrace_cascade` (5-year decision cooldown) | The chosen route to Seamless; visible roll: Seamless (→ end.010), death, storm (→ fracture.029) |
| There Is No Static | `eotg_aug_end.010` | `eotg_aug_total_integration_effect` (only from fracture.027 and end.009) | **The threshold.** The single place the fade is staged; fires end.011 in 180 days |
| The Court Massacre | `eotg_fracture.004` | NF on_action, Storm list, 23-month cooldown | Storm-band climax of the yearly pool |
| What Must Be Done | `eotg_aug_heir.005` | `eotg_aug_heir.006` (5 days after the ruler's death), to the heir | The "you are killed" ending of the Heir's Arc (§3 of the overview), seen by the successor |
| Silence | `eotg_aug_end.002` | `eotg_aug_excision_surgery_effect`, survival branches | The Excision exit: the first event out of the system |

Cooldown authority stays where it is (the on_action, the decision, the chain). Nothing is added to any event `trigger = {}`.

### 5.1 Coordination with W3 (toasts, flags, music; in flight on the same files)

W3 runs now (P2). W7 runs at P5, after the P3 batches. So W7's scripter always finds W3's work already in the file. The rules:

1. **Music in the six events belongs to W7.** Each set piece has exactly one **opening cue** in `immediate` (§6). If W3 has put a different opening cue in one of the six, W7 replaces it and lists the swap in its batch report. heir.005 needs no swap: W3's `mx_cue_murder` is also W7's choice.
2. **Death branches are the one exception to "at most one cue per event".** The only cascade deaths in the mod are in the death branches of fracture.027 and end.009 (checked: `eotg_aug_cascade_death_effect` has no other caller). W3's `mx_cue_death` goes **inline in those branches**, just before `eotg_aug_cascade_death_effect = yes`. It must **never** go inside the shared effect itself (`common/scripted_effects/eotg_augmentation_effects.txt:1024`). The same rule covers `eotg_aug_total_integration_effect` and `eotg_aug_excision_surgery_effect`: no cue inside shared effects, because they fire from these set pieces and would stack a second cue on the opening one. Whether a cue plays at all after the player character's own death is unverified, so CB-44 listens for it (§8).
3. **Flags are W3's; W7 keeps them.** Recommended, matching W3's rule (parent §11 W3): `dangerous` on end.009.a and .c (handover), on all four fracture.027 options (every stance can roll death), and on heir.005.d (re-entry with a hidden flaw); `special` is not needed on any of the six. W7 does not add or remove flags.
4. **Toasts.** In fracture.027 and end.009, each non-death branch already surfaces through a follow-up event (end.010, end.001, end.030, fracture.029). W3 adds **no toast** to those branches, because a toast there would land three days before the event that tells the same story. The death branches get no toast (the player is dead). The other four set pieces have no rolled outcome, so no toast is needed. This is a stated exception to W3's "every `random_list` branch" rule, and W3's DoD count excludes these two events.
5. **Order on the shared files.** W3 commits first. B4, B5 and B7 (P3) then do W5 and W6 on these events, but **not their desc text** (§7.2). W7 goes last. Only one agent edits a given file at a time (parent §11 W1 risk).

---

## 6. The six set pieces

Common to all six:
- `window = big_event_window` (`_events.info:19`). It has left, center and right animated portraits and three **static** lower portraits (`gui/event_windows/big_event_window.gui:136-290`, lower slots use `GetStaticEventPortraitTexture` at :606). It also has `foreground_shader_vfx_container` (:375) for VFX widgets.
- The opening cue goes in `immediate`, outside `hidden_effect`, as `play_music_cue = <key>`.
- Every existing portrait guard (`trigger = { exists = … }`, `animate_if_dead`) stays.
- Paragraphs break at the beat with `\n\n`. The **rendered** desc, meaning the main key plus whichever fragments show, is 90 to 140 words in every reachable combination.
- Voice per parent §12.1. Quotes per §12.2. Canadian English, no dashes, no time-of-day words, and no "you" in narration.

Words marked **[new]** in the text drafts are added sentences or clauses, listed for the lore-keeper (parent W7 risk). Everything else is the shipped text converted to first person. The localizer may polish the drafts; the facts may not change.

### 6.1 The Cascade: `eotg_fracture.027`

- **Trigger point:** wraps the existing terminal event in place. Nothing replaced.
- **Window:** `big_event_window` now. **Fullscreen later**: priority 1 (§9).
- **Background / effect / widgets:** `eotg_bg_private_quarters` + `smoke` (both W2, kept). Add widgets:
  - `event_window_widget_vfx_background_double_vision_severe`
  - `event_window_widget_vfx_left_character_double_vision_severe`

  Both use `container = foreground_shader_vfx_container`. Precedent: `events/dlc/pam/pam_secular_faith_events.txt:6718-6725` (pam_secular_faith_events.0048, severe double vision plus fog on a tormenting dream).
- **Music:** `mx_cue_stress` (`music/in_game/music.txt:358`; vanilla use `events/interaction_events/character_interaction_events.txt:1329`). It carries `calls = 3`: after it plays, the next three requests are skipped. Nothing else in the mod plays it, so only vanilla stress events compete. **Fallback** if CB-44 finds it skipped: `mx_cue_combat_stinger` (:325, no cooldown).
- **Portraits:**
  - `left_portrait` = root, `animation = pain` (kept), plus `triggered_animation`: `brave` → `rage` (:5081), `stubborn` → `anger` (:4468), `craven` → `fear` (:4760).
  - **[new]** `right_portrait` = `scope:eotg_cascade_witness`, `animation = shock` (:5280), guarded with `exists`. Pick it in `immediate` inside `hidden_effect`, first match wins:
    1. `primary_spouse`, alive, not imprisoned;
    2. `primary_heir`, alive, age ≥ 14;
    3. the court physician (`employs_court_position = court_physician_court_position`, as end.001 does).

    If none matches, the scope is not saved and the portrait hides.
  - Animation lines cite `gfx/portraits/portrait_animations/animations.txt`.
- **Beats:**
  1. Everything fires at once.
  2. Someone at the door says my name, and I hear it out of sync.
  3. The gap between me and the system is closing.
  4. One appended fragment: the premonition (if flagged) and the voice-stage line.
- **Options (unchanged; effects reused exactly):**

  | Opt | Text | Gate | Effect (as shipped, `eotg_augmentation_fracture.txt`) |
  |---|---|---|---|
  | a | "Let go." | none | hidden roll: death 35, Seamless 40, Excision 15, abdication 15 (needs an heir), passes 10, with their modifiers (:4495-4545) |
  | b | "Hold on." | none | death 45, Seamless 25, Excision 15, abdication 15, passes 40 (:4548-4598) |
  | c | "Fight it." | brave | death 35, Seamless 15, Excision 15, abdication 15, passes 50 (:4601-4653) |
  | d | "Not yet. I am not finished." | stubborn | death 35, Seamless 15, Excision 15, abdication 15, passes 40 (:4656-4708) |

  W5 (B5) may re-axe c or d. W7 takes whatever gate B5 leaves; the effects never change.
- **Threshold fade: not staged here.** Q3 made fracture.027 optional, and W7 recommends **no**. Four of its five outcomes (death, Excision, abdication, it passes) keep a self that is still first person afterwards: fracture.029, end.001 and end.030 all narrate in "I". A fade here would therefore be followed by the "I" returning, which §12.1 rule 7 forbids. fracture.027 stays full Neurofractured first person. Question L-W7-4 asks the lore-keeper to confirm this.
- **Loc keys and drafts:**

  | Key | Draft | Voice note |
  |---|---|---|
  | `eotg_fracture.027.desc` | "Everything fires at once. Every sensor, every channel, every forecast the implant has ever run arrives together, and I am standing in the middle of the delivery. The room is a long way off.\n\n**[new]** Someone at the door is saying my name. I hear it three times: once early, once on time, once late. I cannot tell which one I replied to.\n\nThere is very little left between my thoughts and the system, and every second it gets thinner." | Neurofractured, first person. "Hearing one's own words late" and the forecast running ahead are both allowed. The name comes from a person, not from the implant. |
  | `.desc_premonition` | "\n\nI remember this. It was filed months ago as a forecast and stored as a memory: this room, these hands. The memory stops where the forecast's confidence did, before the ending." | converted and **shortened** (44 to 30 words) so the worst case fits the band; same facts |
  | `.desc_voice01` | "\n\nThe thought that arrives half a second early is arriving earlier now: a full second, then three, then too many to follow." | already neutral; unchanged |
  | `.desc_voice2` | "\n\nThe model is running in plain view. Every future it has computed for me scrolls past, each one ranked, and the list is converging." | conversion only |
  | `.desc_voice3` | **L-W7-2.** Shipped: "There is no "you" and "it" left in the room, only "we", and we are running out of room to be two." Proposed: "\n\nI keep starting sentences with "we". There is less and less room in the word for two." | The shipped line has the narrator itself speak as "we", which edges toward possession framing. The proposal keeps the "we" in the ruler's mouth (rule 6). |
  | `.desc_voice4` | "\n\nThe terms I agreed to are being exercised all at once. Every permission is live. It is a clean, orderly cascade, and nothing in it is out of bounds. That is what makes it frightening." | conversion only |
  | `.tt` | **L-W7-3.** Shipped: "The implant decides what happens next." Proposed: "What happens next is no longer mine to choose." | The shipped line gives the implant decisions, which the Neurofractured banned list forbids (parent §12.1 rule 7). Text only; the tooltip still sits on every option. |
  | `.a`–`.d`, `.t` | unchanged | |

  Rendered length: main 78 words as drafted; with one voice fragment 100 to 113; worst case (premonition + voice4) 143. **The localizer trims the main desc to 72 to 75 words**, so the worst case lands at or under 140.
- **Art (later fullscreen):** a private room seen from the doorway. The ruler is standing, and every surface (walls, glass, the ruler's own casings) carries overlapping, slightly offset overlay text in several registers at once. A figure in the doorway is out of focus. Cool palette with one warm spill from the corridor. No throne, no religious symbol, no species-specific anatomy in focus (back or silhouette).

### 6.2 Hand Over the Controls: `eotg_aug_end.009`

- **Trigger point:** wraps the decision outcome in place. Vanilla puts decision outcomes in `big_event_window` (`_events.info:19`; `events/decisions_events/major_decisions_events.txt:1677-1698`, major_decisions.3400).
- **Window:** `big_event_window`, and it **stays** there when art arrives. A single-option decision outcome with an odds list reads better in the big window than in the splash queue.
- **Background / effect / widgets:** `eotg_bg_private_quarters` (W2, kept). Add `override_effect_2d = { reference = fog }` and the widgets:
  - `event_window_widget_vfx_background_double_vision_milder`
  - `event_window_widget_vfx_left_character_double_vision_milder`

  Precedent: `pam_secular_faith_events.txt:3414-3418` (pam_secular_faith_events.0026). Milder than the Cascade: here the ruler is choosing.
- **Music:** `mx_cue_secret` (`music.txt:411`, no cooldown; vanilla use `events/dlc/ep3/ep3_story_cycle_admin_eunuch_events.txt:4280`).
- **Portraits:** `left_portrait` = root, `animation = personality_rational` (kept; :3952), plus `triggered_animation`: `compassionate` → `sadness` (:5113), `ambitious` → `ecstasy` (:4728). No other portrait: the decision is made alone.
- **Beats:**
  1. The terms, read twice.
  2. What goes: friends, temperament, children.
  3. What remains will not be a self.
  4. Once only.
- **Options (unchanged):**

  | Opt | Text | Gate | Effect (as shipped, `eotg_augmentation_endgame.txt`) |
  |---|---|---|---|
  | a | "Yes." | none | `eotg_aug_stress_embrace_effect`; visible roll: Seamless 40 (+20 voice 4, +15 may_embrace) → `eotg_aug_total_integration_effect`; death 30 (+15 stress 3, +10 health < 2) → `eotg_aug_cascade_death_effect`; storm 30 → flag `eotg_flag_aug_embrace_failed` 30 days + fracture.029 in 3 days (:312-347) |
  | b | "...No." | none | risk −10, `eotg_aug_stress_reject_effect` (:350-359) |
  | c | "Yes. All of it." | ambitious | as a, Seamless base 50 and +200 prestige on Seamless (:362-399) |
- **The Seamless outcome lines are the first log entries (Q3).** They are visible in the option tooltip before the choice, which is where the log register first shows. They contain no I and no "you", and they address no one.
- **Loc keys and drafts:**

  | Key | Draft | Voice note |
  |---|---|---|
  | `eotg_aug_end.009.desc` | "The terms are plain, **[new]** and I have read them twice. Nothing on the list is hidden. If I hand over the controls, the system runs me.\n\nMy friends will go: it will not remember why they mattered. My temperament will go: it does not need one. My children will become names in a file, **[new]** kept current and never opened. What remains will work, and decide, and be correct. It will not be a self, and nothing in it will mind.\n\nI make this decision once. Afterward there is no one left to make another." | Neurofractured, first person. "Self", never "humanity". No "open" or "through" in the **options** (lore naming rule 7); "opened" here is in the desc and refers to a file. Swap it for "read" if the lore-keeper prefers. |
  | `.a.seamless` | "Handover complete. No seam found. Next item." | log register |
  | `.c.seamless` | "Handover complete, all of it. No seam found. Next item." | log register |
  | `.a.death`, `.c.death`, `.a.storm`, `.c.storm` | unchanged (already neutral) | |
  | `.a`, `.b`, `.c`, `.t` | unchanged | |

  Rendered length: about 91 words.
- **Art (later):** none needed; it stays in the big window. Optional: a bespoke `eotg_bg_*` interior later under W10.

### 6.3 There Is No Static: `eotg_aug_end.010` (the threshold)

- **Trigger point:** wraps the Total Integration notice in place. It is reached only from fracture.027's Seamless branch and end.009's a/c Seamless branches. This is **the** threshold set piece: the only event where the "I" fades into the log.
- **Window:** `big_event_window` now. **Fullscreen later**: priority 1 (§9).
- **Background / effect / widgets:** `eotg_bg_private_quarters` + `fog` (both W2, kept). **No VFX widgets, on purpose.** fracture.027 and end.009 double the image; end.010 is the first steady frame. The contrast is the effect.
- **Music:** `mx_cue_succession_instrumental` (`music.txt:385`, plays every time; vanilla use `events/decisions_events/iberia_north_africa_events.txt:1336`). The seat changes hands without changing holder. If CB-44 finds that it reads as a real succession, fall back to `mx_cue_secret`.
- **Portraits:** `left_portrait` = root, `animation = idle` (kept; :14). No triggered animations: the personality traits have just been removed by `eotg_aug_total_integration_effect`, and that absence is the point. It renders centred, because it is the only portrait (`big_event_window.gui:119`).
- **Beats:**
  1. The static stops, noticed as a sound ending.
  2. "I can see the forecast for the next thought. I am reading it." (the Q3 sample).
  3. The log takes over: "Reading complete. Next item."
  4. Log entries that mirror exactly what the effect just did (relations closed, temperament pruned), then "Next item."
- **Option (unchanged):** a "Acknowledged." No effects. The `immediate` still fires end.011 in 180 days.
- **Loc keys and drafts:**

  | Key | Draft | Voice note |
  |---|---|---|
  | `eotg_aug_end.010.desc` | "The static stops. **[new]** I notice it the way I would notice a sound ending. The overlay is steady, the forecasts are clean, and the second pass over my thoughts has nothing left to correct. It is very quiet.\n\n**[new]** I can see the forecast for the next thought. I am reading it. It is accurate.\n\n**[new]** Reading complete. Next item.\n\n**[new]** Standing preferences: none on file. Grievances: none on file. Relations marked friend: closed, filed. Temperament: not required, pruned. Residual habits: three on file, logged for pruning. Pending decisions: three. Resolved: three. Next item." | **The fade.** First person up to "I am reading it." From "Reading complete." on, it is log register: no I, me, my, we or our, no "you", nobody addressed. Every entry ends logged, filed or pruned (procedures_lore ruling (a)). Entries are the mind's own state, never realm records (tech ceiling). "Residual habits: three" mirrors `eotg_aug_residue = 3`, which the effect has just set (`eotg_augmentation_effects.txt:1119`); it is a word, not a displayed number. |
  | `.a`, `.t` | unchanged | bare acknowledgement |

  Rendered length: about 92 words.
- **L-W7-1.** The pinned wording item in `cybernetics_v2.md` §5 rule 8 ("There is no voice now. There is no one left for it to speak to.") is the shipped end.010 ending. W7 recommends **retiring it here**. It names "the voice" and "speak", which brings back the second-speaker frame at the exact moment Q3 says the text is a record, not a speaker. It also follows the log, so the narration would return after the "I" is gone. If the lore-keeper keeps it, it goes **before** "Reading complete." as the last first-person-era line, never after the log.
- **Art (later fullscreen):** the same private room as the Cascade plate, now perfectly still. The overlay is a single clean column of log lines and nothing else. The figure is seated, and its posture is exact. Grey and flat light. The doorway is empty. The two plates are meant to be read as a before/after pair.

### 6.4 The Court Massacre: `eotg_fracture.004`

- **Trigger point:** wraps the Storm-band event in place.
- **Window:** `big_event_window`, and it **stays** there: the scene needs the victim's portrait, which the fullscreen window cannot show (`gui/event_windows/fullscreen_event.gui` has no portrait slots).
- **Background / effect / widgets:** `eotg_bg_council` + `smoke` (both W2, kept). Add the widget `event_window_widget_vfx_heavy_smoke` (container `foreground_shader_vfx_container`). Precedent: `pam_secular_faith_events.txt:125-127` (pam_secular_faith_events.0002). The smoke is the coolant venting the desc describes.
- **Music:** `mx_cue_murder` (`music.txt:372`, `years = 1`; vanilla use `events/blackmail_events.txt:28`) when `scope:eotg_victim_dead` exists after the victim pick; else `mx_cue_negative` (:403, no cooldown; vanilla use `events/dlc/bp1/bp1_yearly_events_nick.txt:3105`). This is one `if`/`else` placed after the existing `hidden_effect` in `immediate`, so exactly one cue plays.
- **Portraits:**
  - `left_portrait` = root, `animation = stress` (kept), plus `triggered_animation`: `wrathful` → `rage`, `callous` → `personality_callous` (:4184), `compassionate` → `shock`.
  - `right_portrait` = `scope:eotg_victim_portrait` with the dead/pain logic (kept exactly; :505-514).
  - `lower_center_portrait` = the W6 witness (`scope:eotg_witness`, guarded). If W6 has not added it, W7 adds it: a courtier who is not root, either victim or imprisoned, saved in the existing `hidden_effect`. Lower portraits are static in this window, so it needs no animation.
- **Beats:**
  1. The official account to come.
  2. What the witnesses saw.
  3. **[new]** My own memory against the log's, filed as granted motor access.
  4. **[new]** The room afterwards.
  5. One fragment: killed, wounded, or none.
- **Options (unchanged):**

  | Opt | Text | Gate | Effect (as shipped) |
  |---|---|---|---|
  | a | "They were threats. The implant confirmed it." | none | dread +40, risk +10, `eotg_aug_stress_cruelty_effect` (:550-560) |
  | b | "I do not remember." | none | stress medium gain, risk −5, 30% `depressed_1` (:563-576) |
  | c | "Bury them with honours." | zealous + someone died | prestige −100, piety +50, risk −3 (:581-596) |
  | d | "Confess to the court and accept the cost." | just | prestige −200, tyranny −20, risk −8, just stress loss (:600-615) |
  | e | "Fill the empty places by the next watch." | callous + a victim | dread +20, risk +5, callous stress loss (:620-640) |

  Three personality gates, so B4 (W5) will re-axe two of them. W7 takes the result and does not touch effects.
- **Loc keys and drafts:**

  | Key | Draft | Voice note |
  |---|---|---|
  | `eotg_fracture.004.desc` | "There will be an official account. It will speak of a loss of control in the audience chamber, and it will not resemble what the witnesses saw: me crossing the room faster than the guards could follow, coolant hissing from my hot casings, screens shattered and sparking along the wall, and the guards backing away from me.\n\n**[new]** My own memory of it is three seconds long and does not match. The log has all of it, to the tenth of a second, filed under granted motor access.\n\n**[new]** The guards will not look at me. Someone is already at the wall with a cloth." | Neurofractured, first person. Allowed items used: motor pre-emption as granted and logged access, and unreliable narration set against the log. No second speaker. The "three seconds" is a memory, not a risk figure, so it is allowed (parent §8). |
  | `.desc_killed`, `.desc_wounded`, `.desc_none` | unchanged (already neutral) | |
  | `.a`–`.e`, `.t` | unchanged, except where B4 re-axes an option's text | |

  Rendered length: main about 92 words; with one or both fragments 104 to 124.
- **Art:** stays in the big window. Under W10, a bespoke `eotg_bg_*` audience chamber (screens along one wall, shattered) would replace `eotg_bg_council` for this event alone.

### 6.5 What Must Be Done: `eotg_aug_heir.005`

- **Trigger point:** wraps the heir's aftermath in place. root = the heir, after succession (who receives it is CB-21 H3, still unverified in game).
- **Window:** `big_event_window` now. **Fullscreen later**: priority 2 (§9). Fullscreen loses the dead-parent portrait, so it moves only if the plate carries the parent.
- **Background / effect / widgets:** `eotg_bg_corridor_night` (W2, kept). **Change for §14.2:** add `override_effect_2d = { reference = fog }`, plus the widgets `event_window_widget_vfx_background_night_scene` and `event_window_widget_vfx_left_character_night_scene`. Precedent: `pam_secular_faith_events.txt:6718-6725` (night_scene with fog). The widgets are lighting only; no time-of-day word goes in the text.
- **Music:** `mx_cue_murder` (the same key W3 assigns; `music.txt:372`). Its `years = 1` cooldown can collide with fracture.004 only when the same player sees both within a year, which is rare because they are different characters.
- **Portraits:**
  - `left_portrait` = root (the heir), `animation = grief` (kept; :4810), plus `triggered_animation`: `callous` → `personality_callous`, `compassionate` → `crying` (:4518).
  - `right_portrait` = `scope:eotg_parent_ruler`, `dead`, `animate_if_dead = yes` (kept).
  - `lower_center_portrait` = the W6 witness, guarded. Suggested pick: the dead ruler's primary spouse if alive, else any adult close family of root.
- **Beats:**
  1. The parent is dead; it was quick.
  2. **[new]** My hands are still steady.
  3. **[new]** Nobody asks me what to call it; they wait to see what I do with the seat and the hardware.
  4. The implants kept logging; the last entry is my arrival.
- **Options (unchanged):**

  | Opt | Text | Gate | Effect (as shipped, `eotg_augmentation_heir.txt`) |
  |---|---|---|---|
  | a | "It was mercy." | none | `eotg_aug_stress_murder_effect` (:912-920) |
  | b | "It was murder." | compassionate | stress major gain (:923-933) |
  | c | "It was necessary." | callous | prestige +100, `eotg_aug_stress_murder_effect` (:936-947) |
  | d | "Take the implants." | not augmented, gold ≥ tiny | initiate; risk 25; hidden flaw; voice stage 1 if the parent's voice ≥ 2; clear the parent hardware; murder and surgery stress (:952-983) |
- **Loc keys and drafts:**

  | Key | Draft | Voice note |
  |---|---|---|
  | `eotg_aug_heir.005.desc` | "[eotg_parent_ruler.GetFirstName] is dead, and the succession is done. It was quick, in the lull between two incidents, and it caught the residence unprepared. My hands were steady. **[new]** They are still steady, and that is the part I keep returning to.\n\nThe household has called it whatever it needed to call it. **[new]** Nobody has asked me what to call it. They are waiting to see what I will do with the seat, and with the hardware.\n\nIn the next room the implants kept logging **[new]** after the rest of [eotg_parent_ruler.GetHerHim] had stopped. The last entry is a timestamp: my arrival." | Heir's own first person; the heir may be unaugmented, so it is ordinary narration. "Hardware" sets up option d without promising it. Bare `[x.GetName]` form. The parent may have been Seamless (the Heir's Arc jumps to the Choice on Total Integration), and the logging line holds either way. |
  | `.a`–`.d`, `.t` | unchanged | |

  Rendered length: about 100 words.
- **Art (later fullscreen):** a corridor outside a closed door, light under it from status displays still running inside. The heir stands with their back to the viewer. No body in frame; the door does the work.

### 6.6 Silence: `eotg_aug_end.002`

- **Trigger point:** wraps the Excision survivor event in place (both survival branches of `eotg_aug_excision_surgery_effect`, `common/scripted_effects/eotg_augmentation_effects.txt:1254`).
- **Window:** `big_event_window`, and it **stays** there (the physician portrait). The end of a system deserves the big frame, not the splash queue.
- **Background / effect / widgets:** `eotg_bg_clinic` (W2, kept). **Change for §14.2:** add `override_effect_2d = { reference = legend_glow }` (vanilla use `events/activities/coronation_activity/coronation_events.txt:1426-1428`), a soft light where the overlay used to be. Fallback if CB-44 finds it reads as "legendary": `fog`. No widgets: after the noise, nothing doubles.
- **Music:** `mx_cue_peace_ensues` (`music.txt:339`, plays every time). Vanilla uses it for recovery from severe injury: `events/health_events.txt:163`, health.0002, `theme = recovery`, the same theme end.002 has.
- **Portraits:**
  - `left_portrait` = root, `animation = sadness` (kept), plus `triggered_animation`: `scope:eotg_excision_outcome = flag:maimed` (guarded with `exists`) → `pain` (:4980); `content` or `calm` → `personality_content` (:3720).
  - **[new]** `right_portrait` = `scope:eotg_surgeon`, `animation = physician` (:6586), guarded with `exists`. In `immediate`, inside `hidden_effect`: if `scope:eotg_surgeon` doesn't exist and root employs a court physician, save it (end.001's own block, `eotg_augmentation_endgame.txt:96-103`). The back-street path (`PHYSICIAN = no`) usually has no court physician involved, and the guard then hides the portrait. That matches lore ruling (d): option e never mentions the physician.
- **Beats:**
  1. Nothing arrives early.
  2. **[new]** Habit reaches for an answer and finds only the question; I count the steps.
  3. **[new]** I wait for my own sentences to end, and I am the one who ends them.
  4. **[new]** Nobody says how long the quiet lasts.
  5. The maimed fragment, if it shows.
- **Options (unchanged):**

  | Opt | Text | Gate | Effect (as shipped) |
  |---|---|---|---|
  | a | "It's quiet." | none | stress medium loss (:243-251) |
  | b | "I miss it." | none | stress minor gain (:254-262) |
  | c | "Quiet. At last." | zealous | piety +100 (:265-275) |
- **Loc keys and drafts:**

  | Key | Draft | Voice note |
  |---|---|---|
  | `eotg_aug_end.002.desc` | "Nothing arrives early. The overlay does not flicker, no forecast files itself, and the next thought is mine alone, slow and unassisted. After the noise, the silence is almost physical. **[new]** The room sounds larger than it did.\n\n**[new]** I reach for an answer out of habit and find only the question. I have to count the steps to the door. I have to wait for a sentence to end before I know how it ends, and every time I wait, I am the one who finishes it.\n\n**[new]** Nobody tells me how long the quiet lasts." | Ordinary first person: root is out of the system. The last line points toward Phantom Static without naming anything arriving. That line is internal and bodily (procedures_lore (c)), with no signal and no "something". |
  | `.desc_maimed` | "\n\nThey took more out of me than they were there to take. I will not be what I was, and I will feel the difference every time I move." | "The surgeons" becomes "They", so the line also fits the back-street path. |
  | `.a`–`.c`, `.t` | unchanged | |

  Rendered length: about 94 words; 123 with the maimed fragment.
- **Art:** stays in the big window. Under W10, a bespoke recovery-room `eotg_bg_*` (dark displays, one window) could replace `eotg_bg_clinic` here.

### 6.7 Changes to parent §14.2

| Event | Before (W2) | After (W7) |
|---|---|---|
| heir.005 | CN | CN + fog (+ night_scene widgets) |
| end.002 | CL | CL + legend_glow |
| end.009 | PQ | PQ + fog (+ double_vision_milder widgets) |
| fracture.027, fracture.004, end.010 | PQ+smoke, CO+smoke, PQ+fog | unchanged (widgets added per §6.1 and §6.4) |

---

## 7. Loc surface

### 7.1 Keys

All keys are existing; **0 new keys**. Text is replaced in:
- `eotg_fracture.027.desc`, `.desc_premonition`, `.desc_voice2`, `.desc_voice3`, `.desc_voice4`, `.tt`
- `eotg_aug_end.009.desc`, `.a.seamless`, `.c.seamless`
- `eotg_aug_end.010.desc`
- `eotg_fracture.004.desc`
- `eotg_aug_heir.005.desc`
- `eotg_aug_end.002.desc`, `.desc_maimed`

That is 15 keys. `replace/`: none.

### 7.2 Ownership against the P3 batches

The desc text of the six events belongs to **W7, not to their batches**. The parent already says so for fracture.027 (B5), end.009 and end.010 (B7). This addendum extends it to fracture.004 (B4), heir.005 (B7) and end.002 (B7). The batches still do W5 (option re-gating and option text) and W6 (portraits) on these events. W7 then edits the desc keys once, in the new voice. That avoids a double rewrite.

### 7.3 Scorecard pinned Seamless set

The test's pinned set (parent §9 item 2) becomes:
- `eotg_aug_end.010.desc`
- `eotg_aug_end.009.a.seamless`, `.c.seamless`

`eotg_fracture.027.*` leaves the set if L-W7-4 is accepted: it is Neurofractured and counts toward the first-person floor. end.010 is a special case, because it contains "I" by design before the log starts. The test checks **only the text after "Reading complete."** for I, me, my, we, our and you.

---

## 8. Definition of done

1. All six events have `window = big_event_window`. Every option's effect block, trigger (apart from B4/B5 re-gating), `ai_chance` and `random_list` weights are unchanged: `option_outcomes.py` and `risk_moves.py` show identical output for the three files, apart from W3's lines.
2. `event_graph.py` shows no new or removed edges, and no orphans.
3. Each event has exactly one `play_music_cue` in `immediate`, with the key in §6. The only other cues allowed are W3's `mx_cue_death` in the death branches of fracture.027 and end.009. No shared scripted effect contains `play_music_cue`.
4. Every rendered desc combination is 90 to 140 words (the scorecard's `--event` output for each of the six, plus a combination check in the W7 batch report for fracture.027 and fracture.004). Each has ≥ 2 `\n\n` paragraph breaks in the main key.
5. Voice:
   - fracture.027, fracture.004, end.009 (desc), heir.005 and end.002 are first person, with no "you" in narration;
   - end.010 after "Reading complete." and both `*.seamless` lines carry no I, me, my, we, our or you;
   - L012 (banned and register terms) is clean on the 15 keys, including "voice", "answers", "whisper", "prison", "tear", "grip" and "Void", and "the implant decides".
6. Every portrait that names a saved scope is guarded with `exists`. The `triggered_animation` keys are the verified ones in §6. Tiger shows no unknown-animation or unknown-widget error.
7. Tiger clean except the CLAUDE.md known-benign list. PX LSP and vocab show no new findings. eotg_lint shows no new findings against the baseline, and `loc_mechanical.py` is clean.
8. The lore-keeper signs off every **[new]** sentence and rules on L-W7-1 to L-W7-4.
9. **In game (CB-44):**
   - each set piece opens in the big window;
   - both double-vision pairs and the heavy-smoke and night-scene widgets render in it;
   - each cue is heard, including `mx_cue_stress` against its `calls` cooldown;
   - whether W3's `mx_cue_death` plays after the player's own cascade death is recorded;
   - `legend_glow` on end.002 is judged for tone.

---

## 9. Deferred

| Item | Why | Re-open when |
|---|---|---|
| `window = fullscreen_event` for fracture.027 and end.010 (priority 1) and heir.005 (priority 2) | It needs a plate per event and a `queue_icon` (`_events.info:62-66`, required). Vanilla plates are about 3840 × 1252 (`gfx/interface/illustrations/event_story/fp4_heroic_legend.dds`, `fp4_black_death.dds`), and the splash icon is 70 × 70 (`gfx/interface/icons/splash_icons/splash_legends.dds`). `fullscreen_event.gui` has **no portrait slots and no `foreground_shader_vfx_container`**, so the plate must carry the figures and the mood. Precedent: `events/dlc/ce1/legend_ending_events.txt:10-53` (fullscreen, `queue_icon`, `override_background`, `override_sound`, `play_music_cue` in `immediate`). | W10 art. Then add `eotg_bg_fs_cascade`, `eotg_bg_fs_threshold` and `eotg_bg_fs_succession` to `common/event_backgrounds/eotg_event_backgrounds.txt`, plus the shared `eotg_splash_cybernetics.dds`. Whether `override_effect_2d` renders in the fullscreen window is checked then. |
| fracture.004, end.009 and end.002 in fullscreen | They need their portraits (victim, physician) or are decision outcomes, which vanilla keeps in the big window. | Never, unless the owner asks. |
| `override_sound` stingers | Vanilla's are DLC-specific FMOD events (`legend_ending_events.txt:33`). The music cue is enough now. | W10 audio, if any. |
| Trait-keyed desc variants for the set pieces | They would be new beats; option and portrait variety already carry the traits. | Owner asks. |
| The threshold fade at fracture.027 | L-W7-4: the "I" would return on four of the five outcomes. | Never, unless the lore-keeper rules otherwise. |

---

## 10. Vanilla precedent (verified 1.20.0.3)

| Technique | File:line |
|---|---|
| `big_event_window`, its purpose | `events/_events.info:19` |
| Big window, root only, decision outcome, `widget` in the same event | `events/decisions_events/major_decisions_events.txt:1677-1698` (3400) |
| Big window with left and right portraits, and `legend_glow` | `events/decisions_events/ep4_decision_events.txt:30-38` (major_decisions.4000) |
| Big window with `override_effect_2d` | `events/dlc/ce1/epidemic_events.txt:2276-2280` (epidemic_events.1060) |
| Big window on a dramatic personal beat | `events/bookmark_events.txt:2324-2335` (bookmark.0500) |
| Big window portrait slots; lower slots static; VFX container | `gui/event_windows/big_event_window.gui:115-290, 375, 606` |
| `widgets = { widget = { gui container } }` field | `events/_events.info:165-188` |
| Double vision, severe, with fog | `events/dlc/pam/pam_secular_faith_events.txt:6718-6725` |
| Double vision, milder, background and characters | `events/dlc/pam/pam_secular_faith_events.txt:3414-3418` |
| Heavy smoke widget | `events/dlc/pam/pam_secular_faith_events.txt:125-127` |
| Dead portrait, `animate_if_dead` | already in the mod (fracture.004, heir.005); vanilla `events/activities/chariot_race_activity/chariot_ongoing_events_jp.txt:2544` |
| Fullscreen event, `queue_icon`, cue in `immediate` | `events/dlc/ce1/legend_ending_events.txt:10-53`; `events/decisions_events/mpo_greatest_of_khans_events.txt:1001-1017` |
| Music keys and cooldowns | `music/in_game/music.txt` (`mx_cue_secret` 411, `mx_cue_stress` 358, `mx_cue_murder` 372, `mx_cue_negative` 403, `mx_cue_peace_ensues` 339, `mx_cue_succession_instrumental` 385, `mx_cue_combat_stinger` 325); semantics of `calls`/`years` in `music/_music.info` |

---

## 11. Lore questions (for eotg-lore-keeper)

- **L-W7-1:** retire the pinned end.010 line "There is no voice now. There is no one left for it to speak to." (recommended), or keep it placed before the log (§6.3).
- **L-W7-2:** fracture.027.desc_voice3. Is the shipped narrator "we" ("we are running out of room to be two") possession framing? If so, adopt the proposed line (§6.1).
- **L-W7-3:** fracture.027.tt "The implant decides what happens next." gives the implant decisions. Adopt "What happens next is no longer mine to choose." (§6.1).
- **L-W7-4:** confirm that the threshold fade is **not** staged in fracture.027 (§6.1), and that fracture.027 leaves the scorecard's pinned Seamless set (§7.3).
- **Every [new] sentence** in §6.1 to §6.6, notably:
  - the log entries in end.010 (do they stay inside the tech ceiling?);
  - "granted motor access" in fracture.004;
  - "Nobody tells me how long the quiet lasts" in end.002, as a Phantom Static foreshadow.

---

### HANDOFF
- status: done (addendum written; parent W7 section points here)
- next: eotg-lore-keeper (review), then eotg-scripter (P5, after B4/B5/B7 have landed on these files and W3 has committed)
- ask (lore-keeper): rule on L-W7-1 to L-W7-4 and sign off, or amend, every **[new]** sentence in §6. Write the rulings into §11 of this file, or return them for the architect to fold in.
- ask (scripter, after the lore sign-off): apply §6 presentation fields to the six events (window, effect, widgets, music, portraits, the two presentation-only scopes) and §5.1's coordination rules. Change no option effect, trigger, weight or caller. Report any W3 cue you replace.
- files: docs/specs/event_quality_w7_set_pieces.md, docs/specs/event_quality_v1.md
- needs-loc: eotg-localizer writes the 15 keys in §7.1 from the lore-approved drafts, after the scripter (§7.2: these keys are W7's, not B4/B5/B7's)
- needs-lore: L-W7-1 to L-W7-4 plus the [new] sentences
- needs-human: CB-44 in-game checks in §8 item 9; art for §9 when W10 opens
