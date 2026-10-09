# W7 samples: set-piece loc (fracture.004, fracture.027, end.002, end.009, end.010, heir.005)

File: `localization/english/eotg_augmentation_l_english.yml`. 13 keys rewritten; `eotg_fracture.027.tt` was already the ruled text and is unchanged. Spec: `docs/specs/event_quality_w7_set_pieces.md` section 6, L-W7-1 to L-W7-4.

Scorecard rows after W7 (first / second / neutral): endgame 63.6 / 0 / 36.4 (the four Seamless events are the neutral share), fracture 100 / 0 / 0, heir 20 / 0 / 80 (only heir.001, .003 and .007 lead with a Seamless branch, which the scorecard reads as neutral; heir.004 leads with desc_successor and is genuinely neutral; heir.005 is first person). Second person is 0 in all three rows. Lint against baseline: 0 new.

## Samples

**1. eotg_fracture.027.desc (trimmed to 72 words; the person at the door is unnamed so it holds for the spouse, the heir 14+ or the court physician, and when no portrait shows)**
"Everything fires at once. Every sensor, every channel, every forecast the implant has run arrives together, and I stand in the middle of the delivery. The room is a long way off.

Someone at the door is saying my name. I hear it three times: early, on time, late. I cannot tell which I replied to.

Little is left between my thoughts and the system, and every second it thins."

**2. eotg_fracture.027.desc_voice3 (L-W7-2: possession framing replaced; the "we" stays in the ruler's own mouth)**
- Before: "There is no "you" and "it" left in the room, only "we", and we are running out of room to be two."
- After: "I keep starting sentences with "we". There is less and less room in the word for two."

**3. eotg_aug_end.010.desc (the threshold fade; the tail after "Reading complete." has no I, me, my, we, our or you, checked)**
"The static stops. I notice it the way I would notice a sound ending. ... I can see the forecast for the next thought. I am reading it. It is accurate.

Reading complete. Next item.

Static: none logged. Standing preferences: none on file. Grievances: none on file. Relations marked friend or closer: closed, filed. Temperament: not required, pruned. Residual habits: three on file, logged for pruning. Next item."
L-W7-1: the old "There is no voice now. There is no one left for it to speak to." ending is retired.

**4. eotg_aug_end.009.a.seamless and .c.seamless (log register, no pronouns)**
- a: "Handover complete. No seam found. Next item."
- c: "Handover complete, all of it. No seam found. Next item."

## Length checks (scorecard counter)
- fracture.027: main 72 words; worst case (main + premonition + voice4) 140.
- fracture.004: main 105; with desc_killed and desc_wounded 131; with desc_none 122.
- end.002: main 102 (with desc_maimed 132). end.009: main 96. end.010: main 94. heir.005: main 100.
- Every main desc has at least two paragraph breaks.

## Notes for the reviewer
- fracture.027.desc_premonition took one word out ("and" became a comma: "a forecast, stored as a memory") to bring the worst case within 140. The facts are unchanged.
- No time-of-day words in any of the six events (grep returns 0); heir.005 and fracture.004 name no time of day, although their lighting widgets are night scenes.
- heir.005 uses the bare `[eotg_parent_ruler.GetFirstName]` form; end.002 and heir.005 name no speaker; fracture.004 has no speech.
- Unchanged keys are exactly those listed in the worklist.
