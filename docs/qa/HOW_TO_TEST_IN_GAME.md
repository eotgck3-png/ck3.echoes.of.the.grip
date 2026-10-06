# How to test cybernetics in game

**For:** the human, playing Echoes of the Grip.

Each check comes from a numbered list on the taskboard (CB-31, CB-34, and later batches). This guide covers:
- setting the game up;
- forcing any situation with the console;
- what to send back when something looks wrong.

The full event list, and which events can be fired directly from the console, is in [cybernetics_test_plan.md](cybernetics_test_plan.md) §4.

**To test everything pending in one go** (engine checks, cybernetics, Frontier), follow [IN_GAME_SESSION_PLAN.md](IN_GAME_SESSION_PLAN.md). It orders and deduplicates the checks from every test plan and taskboard item, in three sittings.

---

## 1. Before you start

1. **The game runs the repo directly.** `mod/eotg_stellar_rivers` is a junction to the repo, so what you play is the working tree, **including any batch a session is still building.** For a stable test, ask the orchestrator first: "is the tree clean?"
2. **Turn on debug mode.** Debug mode enables the console and shows character and event IDs. Pick one:
   - **Steam:** right-click Crusader Kings III → Properties → Launch Options → add `-debug_mode`.
   - **Paradox launcher:** Game settings → Launch options → add `-debug_mode`.
3. **Use one playset:** "Echoes of the Grip" enabled and nothing else, unless you're running the observer sub-mod (see `docs/tools/observer/README.md`).
4. **Script and loc are read at startup.** After the orchestrator says a batch is committed, restart the game.
5. **Start any bookmark and pick any count or higher.** Cybernetics works on the vanilla map. Counts get the full ruler content; a duke or king makes the vassal-facing events easier to see.

## 2. The console

Open it with the key below Esc (`` ` `` or `§`, depending on your keyboard). Type `help` for the full list.

Commands run on **your own character** unless stated otherwise. In debug mode, hovering a character shows their **ID**, which some commands accept as a target.

| To do this | Type |
|---|---|
| Fire an event on yourself | `event eotg_aug_tier1.005` |
| Fire an event on someone else | `event eotg_aug_tier1.005 <character id>` |
| Become augmented (start of the track) | `effect eotg_aug_initiate_effect = yes` |
| Jump to Enhanced | `effect add_trait_xp = { trait = eotg_cybernetics value = 50 }` |
| Jump to Overclocked | `effect add_trait_xp = { trait = eotg_cybernetics value = 100 }` |
| Set the hidden fracture risk | `effect set_variable = { name = eotg_fracture_risk value = 55 }` |
| Add a personality trait (for trait options) | `add_trait gluttonous` (or chaste, fickle, impatient, lustful, temperate, arbitrary, forgiving…) |
| Remove a trait | `remove_trait gluttonous` |
| Give yourself gold | `effect add_gold = 500` |
| Add stress | `effect add_stress = 250` |
| Make the AI accept every interaction | `yesmen` (type it again to turn it off) |
| Remove every implant (for "formerly augmented" tests) | `effect eotg_aug_remove_all_effect = yes` |

**About firing events directly:** many events need setup first. A story must be running, a second character saved as "the heir" or "the envoy", and so on. Fired cold, those events show missing names or don't fire at all. That's expected, not a bug. Where the test plan §4 "Console" column says *no*, get there by the route in §3 below, or let time run.

**Letting time run:** set speed 5 and wait. The yearly checks fire on each ruler's own date, so give it 1–3 in-game years per check.

## 3. Recipes for the current checklists

### CB-31: tooltip fixes (batch eca9b9c)
Most of these are just "open it and look". Become augmented first (§2).
- **Decisions (items 1, 2, 4, 5, 6):**
  - Open the Decisions tab and hover the cybernetics decisions: Seek Augmentation, Pursue the Next Stage, Maintenance, Consult Physician, Remove Implants.
  - **Check that requirements read as plain sentences (no `eotg_flag_…`), and that no "You lose X" line appears for anything you don't have.**
  - For the "Overclocked only" line, jump to Overclocked and compare.
- **init.018, *The Offer You Sought* (item 3):** take Seek Augmentation. The event should mention a syndicate's offer, and option e's tooltip should say what follows. It appears only if you've never had a syndicate deal.
- **tier2.011 (item 10), fracture.018 (item 11), fracture.020 (item 12):** fire them with `event`. If one won't fire cold, raise your tier or risk and let time run.
- **Trait (item 13):** hover the cybernetics trait on your character sheet.
- **Patron with and without the envoy (items 14, 15):** run init.018 → option e to start a syndicate deal and play it through. To test "envoy absent", kill the envoy: hover them for their ID, then `kill <id>`. If `kill` isn't available, use `effect = { character:<id> = { death = { death_reason = death_murder } } }`.
- **error.log (item 16):** see §4.

### CB-34: G9 trait options and the new storylines
- **G9 (items 1–7):** add the trait, then fire the host event:

  | Trait | Event |
  |---|---|
  | gluttonous | `eotg_aug_tier1.005` |
  | impatient | `eotg_aug_tier1.007` |
  | chaste | `eotg_aug_tier2.004` |
  | fickle | `eotg_aug_tier2.020` |
  | lustful | `eotg_aug_tier3.003` |
  | temperate | `eotg_aug_tier3.010` |
  | arbitrary | `eotg_aug_tier3.021` |
  | forgiving | `eotg_aug_nr.004` (fire it on a knight or courtier, not on yourself) |

  Check that the option appears with the trait's icon. Hover it to check its stress line.
- **Heir's Arc round 2 (items 1–2):**
  1. Be Neurofractured with a primary heir aged 14+, and let the arc run (`event eotg_aug_heir.001` can start it).
  2. In heir.004, take the kill option.
  3. Make another character your heir, and let a year or two pass.
  4. Expect heir.007 *The Next in Line*, then heir.003 and heir.004 with "successor" text, and nothing after that.
- **The Paper (item 3):** start a syndicate deal (init.018 → e), let patron.001 resolve, then remove your implants (Remove Implants decision, or the console). Within a few years, patron.008 *The Paper* should fire once.
- **Once per life (item 4):** after settling the debt, take Seek Augmentation again for several years. You should never see a second syndicate offer.
- **Pronouns (item 7):** play with a female heir or champion and a male one, and read the heir and champion events.

## 4. When something is wrong: what to send

Send the orchestrator any of these. More is better, but a screenshot alone is fine.
1. **A screenshot of the window or tooltip.** In debug mode, an event shows its ID, so include it in the shot if you can.
2. **The event or decision name**, if there's no ID.
3. **The error log:** `Documents/Paradox Interactive/Crusader Kings III/logs/error.log`.
   - Send only lines containing `eotg`, or the whole file. The orchestrator filters it.
   - Lines about vanilla files with no `eotg` in them are usually version noise (CLAUDE.md lists the known ones).
4. **What you expected to see** versus what you saw, in one line.

The orchestrator routes each problem to the right session and adds a check to the taskboard so it doesn't come back.

## 5. Later batches
Each new batch (procedures, interactions, realm) adds its own numbered checks to the taskboard. They use the same console tools. Some need setup that only exists after Gate 1, such as pilgrimages, which need holy sites. Those are marked as such.
