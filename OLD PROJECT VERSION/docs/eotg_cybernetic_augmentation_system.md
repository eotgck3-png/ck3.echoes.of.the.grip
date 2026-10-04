# Cybernetic Augmentation System — Echoes of the Grip
**Design Reference for Claude Code Implementation**
**Mod prefix: `eotg_`**

---

## Overview

The augmentation system is a progressive trait chain representing voluntary cybernetic enhancement. Power escalates faster than stability — augmentation grants real mechanical advantages, but social penalties, psychological instability, and stress consequences increase disproportionately at each tier. The terminal state (Neurofracture) is permanent and irreversible, creating genuine long-term stakes.

This system affects rulers, knights, generals, and courtiers — not players alone. AI participation is essential for emergent storytelling.

---

## Trait Chain

| Tier | Trait Key | State |
|------|-----------|-------|
| 1 | `eotg_augmented` | Early enhancement — socially legible, personally seductive |
| 2 | `eotg_enhanced` | Significant modification — dependency forming, visible alteration |
| 3 | `eotg_overclocked` | Dangerous dependence — unstable, paranoid, near threshold |
| Terminal | `eotg_neurofractured` | Neural collapse — permanent, feared, catastrophic |

Traits are mutually exclusive within the chain. Each tier replaces the previous via `remove_trait` / `add_trait` in the progression event.

---

## File Structure

```
common/
  traits/
    eotg_augmentation_traits.txt
  modifiers/
    eotg_augmentation_modifiers.txt
  scripted_triggers/
    eotg_augmentation_triggers.txt
  scripted_effects/
    eotg_augmentation_effects.txt
  on_actions/
    eotg_augmentation_on_actions.txt
events/
  eotg_augmentation_initiation.txt   # Entry events
  eotg_augmentation_tier1.txt        # Augmented events
  eotg_augmentation_tier2.txt        # Enhanced events
  eotg_augmentation_tier3.txt        # Overclocked events
  eotg_augmentation_fracture.txt     # Neurofracture transformation + Neurofractured events
localization/
  english/
    eotg_augmentation_l_english.yml
```

---

## Trait Definitions

### `eotg_augmented`

```pdx
eotg_augmented = {
    category = physical

    character_modifier = {
        prowess = 2
        health = 0.5
        disease_resistance_add = 10
        monthly_stress_gain_mult = 0.1
        attraction_opinion = -5
    }

    # Education synergy applied via on_action or hidden scripted effect at acquisition
    # See: eotg_augmentation_edu_bonus scripted effect

    opposites = { eotg_enhanced  eotg_overclocked  eotg_neurofractured }

    ai_honor = -1
    ai_energy = 2
    ai_zeal = -1

    ruler_designer_cost = 20
    # Icon: gfx/interface/icons/traits/eotg_augmented.dds
}
```

### `eotg_enhanced`

```pdx
eotg_enhanced = {
    category = physical

    character_modifier = {
        prowess = 4
        health = 0.5
        scheme_resistance_add = 15
        monthly_stress_gain_mult = 0.2
        attraction_opinion = -15
        diplomacy = -2
        fertility = -0.2
    }

    opposites = { eotg_augmented  eotg_overclocked  eotg_neurofractured }

    ai_honor = -1
    ai_energy = 3
    ai_zeal = -2

    ruler_designer_cost = 0   # Not available at start; must be earned
    # Icon: gfx/interface/icons/traits/eotg_enhanced.dds
}
```

### `eotg_overclocked`

```pdx
eotg_overclocked = {
    category = physical

    character_modifier = {
        prowess = 8
        dread_gain_mult = 0.3
        monthly_war_contribution_mult = 0.15
        injury_resistance_add = 20
        monthly_stress_gain_mult = 0.4
        attraction_opinion = -30
        diplomacy = -5
        fertility = -0.4
    }

    opposites = { eotg_augmented  eotg_enhanced  eotg_neurofractured }

    ai_honor = -2
    ai_energy = 4
    ai_zeal = -3

    ruler_designer_cost = 0
    # Icon: gfx/interface/icons/traits/eotg_overclocked.dds
    # Note: monthly Neurofracture risk check runs via on_action eotg_on_monthly_overclocked
}
```

### `eotg_neurofractured`

```pdx
eotg_neurofractured = {
    category = physical

    character_modifier = {
        prowess = 14
        dread_gain_mult = 0.6
        knight_effectiveness_mult = 0.25
        scheme_resistance_add = 25
        monthly_stress_gain_mult = 0.6
        attraction_opinion = -50
        diplomacy = -10
        fertility = -0.8
        health = -1.0
    }

    # Education distortion applied via separate hidden modifier at fracture time
    # See: eotg_neurofracture_edu_distortion scripted effect

    opposites = { eotg_augmented  eotg_enhanced  eotg_overclocked }

    ai_honor = -3
    ai_energy = 4
    ai_zeal = -4

    ruler_designer_cost = 0
    # Icon: gfx/interface/icons/traits/eotg_neurofractured.dds
}
```

---

## Static Modifiers

Defined in `common/modifiers/eotg_augmentation_modifiers.txt`. Icons reference vanilla `gfx/interface/icons/modifiers/`.

```pdx
# Temporary stability from maintenance
eotg_mod_implant_calibrated = {
    icon = health_positive
    monthly_stress_gain_mult = -0.15
    health = 0.3
}

# Black market complications
eotg_mod_illegal_implants = {
    icon = intrigue_negative
    health = -0.5
    monthly_stress_gain_mult = 0.1
    diplomacy = -2
}

# Education synergy bonuses (applied at tier gain, removed at fracture or regression)
eotg_mod_aug_martial_bonus = {
    icon = martial_positive
    martial = 1
}
eotg_mod_aug_steward_bonus = {
    icon = stewardship_positive
    stewardship = 1
}
eotg_mod_aug_intrigue_bonus = {
    icon = intrigue_positive
    intrigue = 1
}
eotg_mod_aug_learning_bonus = {
    icon = learning_positive
    learning = 1
}
eotg_mod_aug_diplomacy_bonus = {
    icon = diplomacy_positive
    diplomacy = 1
}

# Enhanced tier variants (higher values)
eotg_mod_enh_martial_bonus = {
    icon = martial_positive
    martial = 2
}
eotg_mod_enh_steward_bonus = {
    icon = stewardship_positive
    stewardship = 2
}
eotg_mod_enh_intrigue_bonus = {
    icon = intrigue_positive
    intrigue = 2
}
eotg_mod_enh_learning_bonus = {
    icon = learning_positive
    learning = 2
}
eotg_mod_enh_diplomacy_bonus = {
    icon = diplomacy_positive
    diplomacy = 2
}

# Overclocked tier variants
eotg_mod_oc_martial_bonus = {
    icon = martial_positive
    martial = 3
    monthly_stress_gain_mult = 0.1
}
eotg_mod_oc_steward_bonus = {
    icon = stewardship_positive
    stewardship = 3
    monthly_stress_gain_mult = 0.1
}
eotg_mod_oc_intrigue_bonus = {
    icon = intrigue_positive
    intrigue = 3
    monthly_stress_gain_mult = 0.1
}
eotg_mod_oc_learning_bonus = {
    icon = learning_positive
    learning = 3
    monthly_stress_gain_mult = 0.1
}
eotg_mod_oc_diplomacy_bonus = {
    icon = diplomacy_positive
    diplomacy = 3
    monthly_stress_gain_mult = 0.1
}

# Neurofracture — education distortion modifiers (extreme bonuses with heavy collateral)
eotg_mod_nf_martial_distortion = {
    icon = martial_positive
    martial = 5
    diplomacy = -5
    monthly_stress_gain_mult = 0.2
}
eotg_mod_nf_steward_distortion = {
    icon = stewardship_positive
    stewardship = 5
    diplomacy = -5
    monthly_stress_gain_mult = 0.2
}
eotg_mod_nf_intrigue_distortion = {
    icon = intrigue_positive
    intrigue = 5
    diplomacy = -5
    monthly_stress_gain_mult = 0.2
}
eotg_mod_nf_learning_distortion = {
    icon = learning_positive
    learning = 5
    diplomacy = -5
    monthly_stress_gain_mult = 0.2
}
eotg_mod_nf_diplomacy_distortion = {
    icon = diplomacy_positive
    diplomacy_per_piety_level = 1   # Twisted diplomacy — dependent on fear/piety, not genuine
    attraction_opinion = -20
    monthly_stress_gain_mult = 0.2
}

# Isolation — from Lucid Moment or Containment
eotg_mod_withdrawn_from_court = {
    icon = diplomacy_negative
    diplomacy = -3
    monthly_stress_gain_mult = -0.1
    monthly_prestige_gain_mult = -0.2
}

# Overclocked instability risk accumulation (hidden, tracked as variable not modifier)
# Use character variable eotg_fracture_risk (integer, 0-100) tracked in scripted effects
```

---

## Scripted Triggers

```pdx
# eotg_is_augmented_any = yes/no — true if character has any augmentation trait
eotg_is_augmented_any = {
    OR = {
        has_trait = eotg_augmented
        has_trait = eotg_enhanced
        has_trait = eotg_overclocked
        has_trait = eotg_neurofractured
    }
}

# Eligible for initial augmentation
eotg_can_receive_augmented = {
    is_adult = yes
    is_alive = yes
    NOT = { eotg_is_augmented_any = yes }
    # Development gate: capital barony development >= 10
    # (adjust threshold to match your development scale)
    capital_county = {
        any_county_province = {
            development_level >= 10
        }
    }
}

# Eligible to progress Augmented → Enhanced
eotg_can_progress_to_enhanced = {
    has_trait = eotg_augmented
    NOT = { has_character_flag = eotg_flag_suppress_progression }
    capital_county = {
        any_county_province = {
            development_level >= 20
        }
    }
}

# Eligible to progress Enhanced → Overclocked
eotg_can_progress_to_overclocked = {
    has_trait = eotg_enhanced
    NOT = { has_character_flag = eotg_flag_suppress_progression }
    capital_county = {
        any_county_province = {
            development_level >= 35
        }
    }
}

# Neurofracture risk check — runs monthly for Overclocked characters
eotg_neurofracture_threshold_met = {
    has_trait = eotg_overclocked
    OR = {
        var:eotg_fracture_risk >= 80
        AND = {
            var:eotg_fracture_risk >= 60
            stress >= high_stress_threshold
        }
    }
}

# AI augmentation interest
eotg_ai_wants_augmentation = {
    is_ai = yes
    OR = {
        has_trait = ambitious
        has_trait = brave
        has_trait = greedy
    }
    NOT = {
        OR = {
            has_trait = zealous
            has_trait = content
        }
    }
}
```

---

## Scripted Effects

```pdx
# Apply education synergy modifier at tier gain
# Call with: eotg_apply_edu_synergy_augmented = yes
eotg_apply_edu_synergy_augmented = {
    # Remove all previous synergy modifiers first
    remove_character_modifier = eotg_mod_aug_martial_bonus
    remove_character_modifier = eotg_mod_aug_steward_bonus
    remove_character_modifier = eotg_mod_aug_intrigue_bonus
    remove_character_modifier = eotg_mod_aug_learning_bonus
    remove_character_modifier = eotg_mod_aug_diplomacy_bonus

    switch = {
        on_trigger = highest_skill_is
        martial = { add_character_modifier = { modifier = eotg_mod_aug_martial_bonus } }
        stewardship = { add_character_modifier = { modifier = eotg_mod_aug_steward_bonus } }
        intrigue = { add_character_modifier = { modifier = eotg_mod_aug_intrigue_bonus } }
        learning = { add_character_modifier = { modifier = eotg_mod_aug_learning_bonus } }
        diplomacy = { add_character_modifier = { modifier = eotg_mod_aug_diplomacy_bonus } }
        fallback = { add_character_modifier = { modifier = eotg_mod_aug_martial_bonus } }
    }
}

eotg_apply_edu_synergy_enhanced = {
    remove_character_modifier = eotg_mod_aug_martial_bonus
    remove_character_modifier = eotg_mod_aug_steward_bonus
    remove_character_modifier = eotg_mod_aug_intrigue_bonus
    remove_character_modifier = eotg_mod_aug_learning_bonus
    remove_character_modifier = eotg_mod_aug_diplomacy_bonus
    remove_character_modifier = eotg_mod_enh_martial_bonus
    remove_character_modifier = eotg_mod_enh_steward_bonus
    remove_character_modifier = eotg_mod_enh_intrigue_bonus
    remove_character_modifier = eotg_mod_enh_learning_bonus
    remove_character_modifier = eotg_mod_enh_diplomacy_bonus

    switch = {
        on_trigger = highest_skill_is
        martial = { add_character_modifier = { modifier = eotg_mod_enh_martial_bonus } }
        stewardship = { add_character_modifier = { modifier = eotg_mod_enh_steward_bonus } }
        intrigue = { add_character_modifier = { modifier = eotg_mod_enh_intrigue_bonus } }
        learning = { add_character_modifier = { modifier = eotg_mod_enh_learning_bonus } }
        diplomacy = { add_character_modifier = { modifier = eotg_mod_enh_diplomacy_bonus } }
        fallback = { add_character_modifier = { modifier = eotg_mod_enh_martial_bonus } }
    }
}

eotg_apply_edu_synergy_overclocked = {
    # Remove enhanced tier modifiers
    remove_character_modifier = eotg_mod_enh_martial_bonus
    remove_character_modifier = eotg_mod_enh_steward_bonus
    remove_character_modifier = eotg_mod_enh_intrigue_bonus
    remove_character_modifier = eotg_mod_enh_learning_bonus
    remove_character_modifier = eotg_mod_enh_diplomacy_bonus
    remove_character_modifier = eotg_mod_oc_martial_bonus
    remove_character_modifier = eotg_mod_oc_steward_bonus
    remove_character_modifier = eotg_mod_oc_intrigue_bonus
    remove_character_modifier = eotg_mod_oc_learning_bonus
    remove_character_modifier = eotg_mod_oc_diplomacy_bonus

    switch = {
        on_trigger = highest_skill_is
        martial = { add_character_modifier = { modifier = eotg_mod_oc_martial_bonus } }
        stewardship = { add_character_modifier = { modifier = eotg_mod_oc_steward_bonus } }
        intrigue = { add_character_modifier = { modifier = eotg_mod_oc_intrigue_bonus } }
        learning = { add_character_modifier = { modifier = eotg_mod_oc_learning_bonus } }
        diplomacy = { add_character_modifier = { modifier = eotg_mod_oc_diplomacy_bonus } }
        fallback = { add_character_modifier = { modifier = eotg_mod_oc_martial_bonus } }
    }
}

# Apply Neurofracture education distortion
eotg_apply_neurofracture_distortion = {
    remove_character_modifier = eotg_mod_oc_martial_bonus
    remove_character_modifier = eotg_mod_oc_steward_bonus
    remove_character_modifier = eotg_mod_oc_intrigue_bonus
    remove_character_modifier = eotg_mod_oc_learning_bonus
    remove_character_modifier = eotg_mod_oc_diplomacy_bonus

    switch = {
        on_trigger = highest_skill_is
        martial = { add_character_modifier = { modifier = eotg_mod_nf_martial_distortion } }
        stewardship = { add_character_modifier = { modifier = eotg_mod_nf_steward_distortion } }
        intrigue = { add_character_modifier = { modifier = eotg_mod_nf_intrigue_distortion } }
        learning = { add_character_modifier = { modifier = eotg_mod_nf_learning_distortion } }
        diplomacy = { add_character_modifier = { modifier = eotg_mod_nf_diplomacy_distortion } }
        fallback = { add_character_modifier = { modifier = eotg_mod_nf_martial_distortion } }
    }
}

# Clean all augmentation modifiers — use on death or full removal
eotg_clean_all_aug_modifiers = {
    remove_character_modifier = eotg_mod_aug_martial_bonus
    remove_character_modifier = eotg_mod_aug_steward_bonus
    remove_character_modifier = eotg_mod_aug_intrigue_bonus
    remove_character_modifier = eotg_mod_aug_learning_bonus
    remove_character_modifier = eotg_mod_aug_diplomacy_bonus
    remove_character_modifier = eotg_mod_enh_martial_bonus
    remove_character_modifier = eotg_mod_enh_steward_bonus
    remove_character_modifier = eotg_mod_enh_intrigue_bonus
    remove_character_modifier = eotg_mod_enh_learning_bonus
    remove_character_modifier = eotg_mod_enh_diplomacy_bonus
    remove_character_modifier = eotg_mod_oc_martial_bonus
    remove_character_modifier = eotg_mod_oc_steward_bonus
    remove_character_modifier = eotg_mod_oc_intrigue_bonus
    remove_character_modifier = eotg_mod_oc_learning_bonus
    remove_character_modifier = eotg_mod_oc_diplomacy_bonus
    remove_character_modifier = eotg_mod_nf_martial_distortion
    remove_character_modifier = eotg_mod_nf_steward_distortion
    remove_character_modifier = eotg_mod_nf_intrigue_distortion
    remove_character_modifier = eotg_mod_nf_learning_distortion
    remove_character_modifier = eotg_mod_nf_diplomacy_distortion
    remove_character_modifier = eotg_mod_implant_calibrated
    remove_character_modifier = eotg_mod_illegal_implants
    remove_character_modifier = eotg_mod_withdrawn_from_court
}

# Increment fracture risk variable
eotg_add_fracture_risk = {
    # Expects: $AMOUNT$ parameter
    if = {
        limit = { NOT = { has_variable = eotg_fracture_risk } }
        set_variable = { name = eotg_fracture_risk  value = 0 }
    }
    change_variable = { name = eotg_fracture_risk  add = $AMOUNT$ }
    clamp_variable = { name = eotg_fracture_risk  min = 0  max = 100 }
}

# Trigger the Neural Cascade (fracture transformation)
eotg_trigger_neurofracture = {
    remove_trait = eotg_overclocked
    add_trait = eotg_neurofractured
    eotg_apply_neurofracture_distortion = yes
    set_variable = { name = eotg_fracture_risk  value = 0 }
    trigger_event = { id = eotg_fracture.0001  days = 1 }
}
```

---

## On Actions

```pdx
# eotg_augmentation_on_actions.txt

# Monthly check for Overclocked → Neurofracture risk
on_monthly_pulse = {
    on_actions = { eotg_on_monthly_overclocked_check }
}

eotg_on_monthly_overclocked_check = {
    effect = {
        every_ruler = {
            limit = { has_trait = eotg_overclocked }
            # Passive risk accumulation each month
            eotg_add_fracture_risk = { AMOUNT = 1 }
            # Stress accelerates risk
            if = {
                limit = { stress >= high_stress_threshold }
                eotg_add_fracture_risk = { AMOUNT = 3 }
            }
            # Check for threshold crossing
            if = {
                limit = { eotg_neurofracture_threshold_met = yes }
                eotg_trigger_neurofracture = yes
            }
            # Random monthly Overclocked events
            random = {
                chance = 8
                trigger_event = { id = eotg_aug_tier3.001  days = { 1 15 } }
            }
        }
    }
}

# Random Augmented events
on_monthly_pulse = {
    on_actions = { eotg_on_monthly_augmented_events }
}
eotg_on_monthly_augmented_events = {
    effect = {
        every_ruler = {
            limit = {
                has_trait = eotg_augmented
                NOT = { has_character_flag = eotg_flag_aug_event_cooldown }
            }
            random = {
                chance = 5
                trigger_event = { id = eotg_aug_tier1.001  days = { 1 10 } }
            }
        }
    }
}

# Random Enhanced events  
on_monthly_pulse = {
    on_actions = { eotg_on_monthly_enhanced_events }
}
eotg_on_monthly_enhanced_events = {
    effect = {
        every_ruler = {
            limit = {
                has_trait = eotg_enhanced
                NOT = { has_character_flag = eotg_flag_enh_event_cooldown }
            }
            random = {
                chance = 6
                trigger_event = { id = eotg_aug_tier2.001  days = { 1 10 } }
            }
        }
    }
}

# Neurofractured random events (more frequent)
on_monthly_pulse = {
    on_actions = { eotg_on_monthly_neurofractured_events }
}
eotg_on_monthly_neurofractured_events = {
    effect = {
        every_ruler = {
            limit = { has_trait = eotg_neurofractured }
            random = {
                chance = 12
                trigger_event = { id = eotg_fracture.002  days = { 1 20 } }
            }
        }
    }
}

# Risk modifiers on battle/wound
on_combat_finished = {
    on_actions = { eotg_on_combat_fracture_risk }
}
eotg_on_combat_fracture_risk = {
    effect = {
        every_combatant = {
            limit = {
                has_trait = eotg_overclocked
                is_alive = yes
            }
            eotg_add_fracture_risk = { AMOUNT = 5 }
        }
    }
}
```

---

## Events — Initiation

File: `events/eotg_augmentation_initiation.txt`
Namespace: `eotg_aug_init`

### `eotg_aug_init.001` — The Cost of Survival

```pdx
eotg_aug_init.001 = {
    type = character_event
    title = eotg_aug_init.001.t
    desc = eotg_aug_init.001.desc
    theme = battle
    # Trigger: via on_action after battle wound — NOT self-firing
    # On action: on_combat_finished, limit = { is_wounded = yes  NOT = { eotg_is_augmented_any = yes } }

    immediate = {
        hidden_effect = {
            set_character_flag = { flag = eotg_flag_aug_event_cooldown  years = 2 }
        }
    }

    option = {    # Accept
        name = eotg_aug_init.001.a
        add_trait = eotg_augmented
        remove_trait = wounded
        eotg_apply_edu_synergy_augmented = yes
        hidden_effect = { set_variable = { name = eotg_fracture_risk  value = 0 } }
        stress_impact = {
            base = minor_stress_impact_loss
            humble = minor_stress_impact_gain
            content = minor_stress_impact_gain
            zealous = medium_stress_impact_gain
            ambitious = minor_stress_impact_loss
        }
    }

    option = {    # Find another way
        name = eotg_aug_init.001.b
        add_health = 0.5
        stress_impact = {
            zealous = minor_stress_impact_loss
            ambitious = minor_stress_impact_gain
        }
    }

    option = {    # Refuse entirely — zealous/principled
        name = eotg_aug_init.001.c
        trigger = {
            OR = { has_trait = zealous  has_trait = content  has_trait = humble }
        }
        add_piety = 100
        stress_impact = {
            zealous = minor_stress_impact_loss
            ambitious = medium_stress_impact_gain
        }
    }
}
```

### `eotg_aug_init.002` — A Corporate Offer

```pdx
eotg_aug_init.002 = {
    type = character_event
    title = eotg_aug_init.002.t
    desc = eotg_aug_init.002.desc
    theme = stewardship_wealth
    # Trigger: on_action yearly pulse, limit = { is_landed = yes  gold >= 500  eotg_can_receive_augmented = yes }

    option = {    # Accept
        name = eotg_aug_init.002.a
        add_trait = eotg_augmented
        eotg_apply_edu_synergy_augmented = yes
        hidden_effect = {
            set_variable = { name = eotg_fracture_risk  value = 0 }
            # Corporation gains hook — implement when hook system is available
        }
        stress_impact = {
            base = no_stress_impact
            zealous = medium_stress_impact_gain
            humble = minor_stress_impact_gain
        }
    }

    option = {    # Decline
        name = eotg_aug_init.002.b
        add_intrigue_experience = 50
        stress_impact = {
            base = no_stress_impact
            ambitious = minor_stress_impact_gain
        }
    }

    option = {    # Offer to a knight instead
        name = eotg_aug_init.002.c
        trigger = { any_knight = { is_alive = yes } }
        random_knight = {
            add_trait = eotg_augmented
        }
        add_dread = 5
    }
}
```

### `eotg_aug_init.003` — Aging Hands

```pdx
eotg_aug_init.003 = {
    type = character_event
    title = eotg_aug_init.003.t
    desc = eotg_aug_init.003.desc
    theme = lifestyle
    # Trigger: yearly pulse, limit = { age >= 50  prowess <= 8  eotg_can_receive_augmented = yes }

    option = {
        name = eotg_aug_init.003.a
        add_trait = eotg_augmented
        eotg_apply_edu_synergy_augmented = yes
        hidden_effect = { set_variable = { name = eotg_fracture_risk  value = 0 } }
        stress_impact = {
            base = no_stress_impact
            ambitious = minor_stress_impact_loss
            content = minor_stress_impact_gain
        }
    }

    option = {
        name = eotg_aug_init.003.b
        add_prestige = 100
        stress_impact = {
            base = no_stress_impact
            zealous = minor_stress_impact_loss
        }
    }
}
```

---

## Events — Tier 1 (Augmented)

File: `events/eotg_augmentation_tier1.txt`
Namespace: `eotg_aug_tier1`

### `eotg_aug_tier1.001` — Phantom Sensation

```pdx
eotg_aug_tier1.001 = {
    type = character_event
    title = eotg_aug_tier1.001.t
    desc = eotg_aug_tier1.001.desc
    theme = health
    # Cooldown flag set in immediate

    immediate = {
        hidden_effect = {
            set_character_flag = { flag = eotg_flag_aug_event_cooldown  years = 2 }
        }
    }

    option = {
        name = eotg_aug_tier1.001.a    # "Ignore it"
        stress_impact = { base = minor_stress_impact_gain }
    }

    option = {
        name = eotg_aug_tier1.001.b    # "Recalibrate"
        trigger = { gold >= 25 }
        add_gold = -25
        add_character_modifier = { modifier = eotg_mod_implant_calibrated  years = 2 }
    }

    option = {
        name = eotg_aug_tier1.001.c    # "Fascinating"
        add_learning_experience = 50
        hidden_effect = {
            if = {
                limit = { eotg_can_progress_to_enhanced = yes }
                eotg_add_fracture_risk = { AMOUNT = 2 }
            }
        }
    }
}
```

### `eotg_aug_tier1.002` — The Upgrade (Progression Gate — Augmented → Enhanced)

```pdx
eotg_aug_tier1.002 = {
    type = character_event
    title = eotg_aug_tier1.002.t
    desc = eotg_aug_tier1.002.desc
    theme = health
    # Trigger: on_action yearly pulse, limit = { eotg_can_progress_to_enhanced = yes  gold >= 100 }

    option = {
        name = eotg_aug_tier1.002.a    # "Proceed"
        trigger = { gold >= 100 }
        add_gold = -100
        remove_trait = eotg_augmented
        add_trait = eotg_enhanced
        eotg_apply_edu_synergy_enhanced = yes
        stress_impact = {
            base = no_stress_impact
            compassionate = minor_stress_impact_gain
            humble = minor_stress_impact_gain
        }
    }

    option = {
        name = eotg_aug_tier1.002.b    # "Not yet"
        stress_impact = {
            base = no_stress_impact
            ambitious = minor_stress_impact_gain
        }
    }

    option = {
        name = eotg_aug_tier1.002.c    # "This concerns me"
        set_character_flag = { flag = eotg_flag_suppress_progression  years = 5 }
        stress_impact = {
            base = minor_stress_impact_loss
        }
    }
}
```

---

## Events — Tier 2 (Enhanced)

File: `events/eotg_augmentation_tier2.txt`
Namespace: `eotg_aug_tier2`

### `eotg_aug_tier2.001` — Emotional Delay

```pdx
eotg_aug_tier2.001 = {
    type = character_event
    title = eotg_aug_tier2.001.t
    desc = eotg_aug_tier2.001.desc
    theme = lifestyle

    immediate = {
        hidden_effect = {
            set_character_flag = { flag = eotg_flag_enh_event_cooldown  years = 2 }
        }
    }

    option = {
        name = eotg_aug_tier2.001.a    # "Emotion clouds judgment"
        add_character_modifier = { modifier = eotg_mod_enh_intrigue_bonus  years = 3 }
    }

    option = {
        name = eotg_aug_tier2.001.b    # "I do not like this"
        stress_impact = { base = minor_stress_impact_gain }
    }

    option = {
        name = eotg_aug_tier2.001.c    # "Increase neural responsiveness"
        trigger = { gold >= 50 }
        add_gold = -50
        eotg_add_fracture_risk = { AMOUNT = 8 }
    }
}
```

### `eotg_aug_tier2.002` — Children Fear Me

```pdx
eotg_aug_tier2.002 = {
    type = character_event
    title = eotg_aug_tier2.002.t
    desc = eotg_aug_tier2.002.desc
    theme = family
    # Trigger: limit = { has_trait = eotg_enhanced  any_child = { is_alive = yes } }

    option = {
        name = eotg_aug_tier2.002.a    # "They will understand strength"
        add_dread = 10
        every_child = {
            limit = { is_alive = yes  age < 16 }
            add_opinion = { modifier = dread_fearful_opinion  target = root  years = 5 }
        }
    }

    option = {
        name = eotg_aug_tier2.002.b    # "What have I become?"
        stress_impact = { base = medium_stress_impact_gain }
        set_character_flag = { flag = eotg_flag_suppress_progression  years = 3 }
    }
}
```

### `eotg_aug_tier2.003` — Enhanced → Overclocked Progression Gate

```pdx
eotg_aug_tier2.003 = {
    type = character_event
    title = eotg_aug_tier2.003.t
    desc = eotg_aug_tier2.003.desc
    theme = health
    # Trigger: yearly pulse, limit = { eotg_can_progress_to_overclocked = yes  gold >= 200 }

    option = {
        name = eotg_aug_tier2.003.a    # "Proceed"
        trigger = { gold >= 200 }
        add_gold = -200
        remove_trait = eotg_enhanced
        add_trait = eotg_overclocked
        eotg_apply_edu_synergy_overclocked = yes
        stress_impact = {
            base = minor_stress_impact_gain
            brave = minor_stress_impact_loss
            ambitious = no_stress_impact
        }
    }

    option = {
        name = eotg_aug_tier2.003.b    # "The risks are unacceptable"
        stress_impact = {
            base = no_stress_impact
            ambitious = medium_stress_impact_gain
        }
    }

    option = {
        name = eotg_aug_tier2.003.c    # "Test it on prisoners first"
        trigger = { any_prisoner = { is_alive = yes } }
        random_prisoner = {
            add_health = -1
            stress_impact = { base = no_stress_impact }
        }
        add_dread = 15
        eotg_add_fracture_risk = { AMOUNT = 5 }
        remove_trait = eotg_enhanced
        add_trait = eotg_overclocked
        eotg_apply_edu_synergy_overclocked = yes
    }
}
```

---

## Events — Tier 3 (Overclocked)

File: `events/eotg_augmentation_tier3.txt`
Namespace: `eotg_aug_tier3`

### `eotg_aug_tier3.001` — Violent Impulse

```pdx
eotg_aug_tier3.001 = {
    type = character_event
    title = eotg_aug_tier3.001.t
    desc = eotg_aug_tier3.001.desc
    theme = intrigue
    # Trigger: monthly on_action (Overclocked)

    immediate = {
        hidden_effect = {
            set_character_flag = { flag = eotg_flag_oc_event_cooldown  months = 6 }
        }
    }

    option = {
        name = eotg_aug_tier3.001.a    # "Control yourself"
        stress_impact = { base = medium_stress_impact_gain }
        eotg_add_fracture_risk = { AMOUNT = -3 }
    }

    option = {
        name = eotg_aug_tier3.001.b    # "Strike first"
        trigger = { any_courtier = { is_alive = yes  NOT = { is_imprisoned = yes } } }
        random_courtier = {
            add_trait = wounded
        }
        add_dread = 15
        eotg_add_fracture_risk = { AMOUNT = 5 }
    }

    option = {
        name = eotg_aug_tier3.001.c    # "Kill them"
        trigger = { any_courtier = { is_alive = yes  NOT = { is_imprisoned = yes } } }
        random_courtier = {
            kill_character = yes
        }
        add_dread = 30
        add_tyranny = 10
        eotg_add_fracture_risk = { AMOUNT = 15 }
    }
}
```

### `eotg_aug_tier3.002` — The Mirror

```pdx
eotg_aug_tier3.002 = {
    type = character_event
    title = eotg_aug_tier3.002.t
    desc = eotg_aug_tier3.002.desc
    theme = lifestyle

    option = {
        name = eotg_aug_tier3.002.a    # "This is evolution"
        add_prestige = 100
        eotg_add_fracture_risk = { AMOUNT = 10 }
    }

    option = {
        name = eotg_aug_tier3.002.b    # "I miss who I was"
        stress_impact = { base = medium_stress_impact_gain }
        eotg_add_fracture_risk = { AMOUNT = -5 }
    }

    option = {
        name = eotg_aug_tier3.002.c    # "Remove more flesh"
        add_prowess = 3
        eotg_add_fracture_risk = { AMOUNT = 25 }
        hidden_effect = {
            if = {
                limit = { eotg_neurofracture_threshold_met = yes }
                eotg_trigger_neurofracture = yes
            }
        }
    }
}
```

### `eotg_aug_tier3.003` — Sleepless

```pdx
eotg_aug_tier3.003 = {
    type = character_event
    title = eotg_aug_tier3.003.t
    desc = eotg_aug_tier3.003.desc
    theme = health

    option = {
        name = eotg_aug_tier3.003.a    # "Sedate me"
        add_health = -0.3
        stress_impact = { base = medium_stress_impact_loss }
    }

    option = {
        name = eotg_aug_tier3.003.b    # "I no longer require rest"
        add_character_modifier = { modifier = eotg_mod_oc_martial_bonus  years = 2 }
        eotg_add_fracture_risk = { AMOUNT = 20 }
    }

    option = {
        name = eotg_aug_tier3.003.c    # "Disconnect the neural feed"
        add_martial = -2
        add_prowess = -2
        eotg_add_fracture_risk = { AMOUNT = -10 }
    }
}
```

---

## Events — Neurofracture

File: `events/eotg_augmentation_fracture.txt`
Namespace: `eotg_fracture`

### `eotg_fracture.0001` — Neural Cascade (Transformation Event)

```pdx
eotg_fracture.0001 = {
    type = character_event
    title = eotg_fracture.0001.t
    desc = eotg_fracture.0001.desc
    theme = battle
    # Fired by eotg_trigger_neurofracture scripted effect
    # trait already changed before this fires — this is the narrative reveal

    immediate = {
        hidden_effect = {
            add_dread = 40
            stress_impact = { base = massive_stress_impact_gain }
            # Chance to injure a random courtier
            random = {
                chance = 40
                random_courtier = {
                    limit = { is_alive = yes }
                    add_trait = wounded
                }
            }
        }
    }

    option = {    # Single option — this is not a choice, it is a revelation
        name = eotg_fracture.0001.a
    }
}
```

### `eotg_fracture.002` — Containment Breach

```pdx
eotg_fracture.002 = {
    type = character_event
    title = eotg_fracture.002.t
    desc = eotg_fracture.002.desc
    theme = battle

    immediate = {
        hidden_effect = {
            set_character_flag = { flag = eotg_flag_nf_event_cooldown  months = 12 }
            # Random outcomes
            random = {
                chance = 50
                random_courtier = { limit = { is_alive = yes }  add_trait = wounded }
            }
            random = {
                chance = 20
                random_courtier = { limit = { is_alive = yes }  kill_character = yes }
            }
        }
    }

    option = {
        name = eotg_fracture.002.a    # "No chains"
        add_dread = 30
        add_tyranny = 5
    }

    option = {
        name = eotg_fracture.002.b    # "Someone help me"
        stress_impact = { base = medium_stress_impact_gain }
        add_character_modifier = { modifier = eotg_mod_withdrawn_from_court  years = 2 }
    }

    option = {
        name = eotg_fracture.002.c    # "Execute the survivors"
        every_courtier = {
            limit = { is_alive = yes  has_trait = wounded }
            kill_character = yes
        }
        add_dread = 50
        add_tyranny = 20
    }
}
```

### `eotg_fracture.003` — Lucid Moment

```pdx
eotg_fracture.003 = {
    type = character_event
    title = eotg_fracture.003.t
    desc = eotg_fracture.003.desc
    theme = lifestyle
    # Trigger: rare — monthly chance 3%

    option = {
        name = eotg_fracture.003.a    # "End this"
        # Suicide attempt — health check
        random = {
            chance = 40
            modifier = { add = 20  health < 3 }
            kill_character = { death_reason = death_suicide }
        }
        stress_impact = { base = massive_stress_impact_gain }
    }

    option = {
        name = eotg_fracture.003.b    # "Isolate myself"
        add_character_modifier = { modifier = eotg_mod_withdrawn_from_court  years = 3 }
        stress_impact = { base = minor_stress_impact_loss }
    }

    option = {
        name = eotg_fracture.003.c    # "Weakness disgusts me"
        stress_impact = { base = massive_stress_impact_loss }
        add_dread = 20
        eotg_add_fracture_risk = { AMOUNT = 10 }
    }
}
```

### `eotg_fracture.004` — The Court Massacre

```pdx
eotg_fracture.004 = {
    type = character_event
    title = eotg_fracture.004.t
    desc = eotg_fracture.004.desc
    theme = battle
    # Trigger: monthly, limit = { has_trait = eotg_neurofractured  stress >= very_high_stress_threshold }

    immediate = {
        hidden_effect = {
            set_character_flag = { flag = eotg_flag_nf_event_cooldown  years = 2 }
            # Mandatory court deaths
            random_courtier = {
                limit = { is_alive = yes }
                kill_character = yes
            }
            random_courtier = {
                limit = { is_alive = yes }
                add_trait = wounded
            }
            # Chance to kill spouse
            random = {
                chance = 20
                if = {
                    limit = { has_spouse = yes }
                    random_spouse = { kill_character = yes }
                }
            }
        }
    }

    option = {
        name = eotg_fracture.004.a    # "They were threats"
        add_dread = 40
    }

    option = {
        name = eotg_fracture.004.b    # "I do not remember"
        stress_impact = { base = medium_stress_impact_gain }
        random = {
            chance = 30
            add_trait = melancholic
        }
    }
}
```

---

## Regression System

Regression is possible before Neurofracture via events or decisions. Neurofracture is **permanent — no regression path exists.**

### Regression Paths

| From | To | Mechanism |
|------|-----|-----------|
| `eotg_enhanced` | `eotg_augmented` | Decision: Partial Removal (gold cost, stress loss) |
| `eotg_overclocked` | `eotg_enhanced` | Event: Implant Failure / Financial Crisis |
| `eotg_neurofractured` | — | **Impossible** |

### Regression Decision (Enhanced → Augmented)

```pdx
eotg_decision_partial_removal = {
    picture = "gfx/interface/illustrations/decisions/decision_misc.dds"
    major = no
    ai_check_interval = 120

    is_shown = {
        has_trait = eotg_enhanced
    }

    is_valid = {
        gold >= 150
        stress >= medium_stress_threshold
    }

    is_valid_showing_failures_only = {
        gold >= 150
    }

    cost = { gold = 150 }

    effect = {
        remove_trait = eotg_enhanced
        add_trait = eotg_augmented
        eotg_apply_edu_synergy_augmented = yes
        remove_character_modifier = eotg_mod_enh_martial_bonus
        remove_character_modifier = eotg_mod_enh_steward_bonus
        remove_character_modifier = eotg_mod_enh_intrigue_bonus
        remove_character_modifier = eotg_mod_enh_learning_bonus
        remove_character_modifier = eotg_mod_enh_diplomacy_bonus
        stress_impact = { base = medium_stress_impact_loss }
        custom_tooltip = eotg_decision_partial_removal_tooltip
    }

    ai_potential = {
        stress >= high_stress_threshold
    }
    ai_will_do = {
        base = 5
        modifier = { add = 20  stress >= very_high_stress_threshold }
        modifier = { add = 10  has_trait = content }
        modifier = { add = -15  has_trait = ambitious }
    }
}
```

---

## Cultural & Religious Reactions

### Opinion Modifier Suggestions

Define in `common/opinion_modifiers/eotg_augmentation_opinions.txt`:

```pdx
eotg_opinion_aug_admiration = {
    opinion = 15
    monthly_decay = 0
}

eotg_opinion_aug_unease = {
    opinion = -10
    monthly_decay = 0
}

eotg_opinion_aug_fear = {
    opinion = -25
    monthly_decay = 0
}

eotg_opinion_aug_disgust = {
    opinion = -20
    monthly_decay = 0
}
```

### Cultural Reactions (apply at trait gain via `eotg_apply_cultural_aug_reaction` scripted effect)

| Culture/Religion Type | At Augmented | At Enhanced | At Neurofractured |
|----------------------|--------------|-------------|-------------------|
| Technophile | `+admiration` | `+admiration` | `+fear` only |
| Militarist | `+admiration` | `+admiration` | Mixed |
| Traditionalist | `-unease` | `-fear` | `-disgust` |
| Spiritualist / Flesh Purity | `-unease` | `-disgust` | `-disgust` |

Implementation: use culture `has_cultural_parameter` checks once cultural pillars are defined; for beta, use `has_trait = zealous` / `has_trait = cynical` as proxies on opinion holders.

---

## AI Behavior Weights

Reference in `ai_will_do` blocks across decisions and interactions:

```pdx
# Ambitious rulers augment readily
modifier = { add = 30  has_trait = ambitious }

# Brave rulers push to Overclocked
modifier = { add = 20  has_trait = brave }

# Zealous rulers refuse
modifier = { add = -100  has_trait = zealous }

# Paranoid rulers spiral faster
modifier = { add = 20  has_trait = paranoid }
# Also: in eotg_add_fracture_risk calls, add 2 extra per month if paranoid

# Content/humble resist escalation
modifier = { add = -20  has_trait = content }
modifier = { add = -15  has_trait = humble }
```

---

## Development Gate Reference

| Tier | Development Threshold | Notes |
|------|----------------------|-------|
| `eotg_augmented` | `>= 10` | Urbanized holding required |
| `eotg_enhanced` | `>= 20` | Specialized clinic building (post-beta: `eotg_building_aug_clinic`) |
| `eotg_overclocked` | `>= 35` | Advanced infrastructure; very rare at start date |

For beta: gate on `development_level` of capital province only. Post-beta: add building requirements.

---

## Localization Keys (Stub)

File: `localization/english/eotg_augmentation_l_english.yml`

```yaml
l_english:
 # Traits
 eotg_augmented: "Augmented"
 eotg_augmented_desc: "This character has undergone voluntary cybernetic enhancement. Implants are sharp, new, and still legible to the world."
 eotg_enhanced: "Enhanced"
 eotg_enhanced_desc: "Heavy modification has remade this character visibly. Dependency is forming. Emotion arrives slower than it should."
 eotg_overclocked: "Overclocked"
 eotg_overclocked_desc: "The implants dominate. Sleep is a memory. The static never fully stops."
 eotg_neurofractured: "Neurofractured"
 eotg_neurofractured_desc: "Neural collapse. Identity fragmentation. The machine and the person have ceased to agree on what is real."

 # Modifiers
 eotg_mod_implant_calibrated: "Calibrated Systems"
 eotg_mod_implant_calibrated_desc: "Recent maintenance has stabilized the implants. The noise is manageable."
 eotg_mod_illegal_implants: "Black Market Implants"
 eotg_mod_illegal_implants_desc: "Unlicensed modifications of uncertain origin. They work. Mostly."
 eotg_mod_withdrawn_from_court: "Withdrawn from Court"
 eotg_mod_withdrawn_from_court_desc: "The ruler has retreated from public life. Those who remain nearby walk carefully."

 # Events — titles and descriptions are authored separately
 # See: eotg_augmentation_initiation.txt, eotg_augmentation_tier1-3.txt, eotg_augmentation_fracture.txt
```

---

## Beta Scope vs Post-Beta

| Feature | Beta | Post-Beta |
|---------|------|-----------|
| 4 traits + modifiers | ✅ | — |
| Initiation events (wound, corporate, aging) | ✅ | Duel shame, military arms race |
| Tier 1–3 random events | ✅ Core set | Full expanded event ecosystem |
| Neurofracture transformation + events | ✅ | — |
| Regression decision | ✅ | — |
| Development gates | ✅ Simple | Building requirements |
| Cultural opinion reactions | Trait proxy | Full pillar integration |
| Building chain (clinics, neural forge) | ❌ | ✅ |
| Knight/courtier augmentation spread | ❌ | ✅ |
| Dynastic events (Cult of Steel, heir fear) | ❌ | ✅ |
| Nikios Khanate government interaction | ❌ | ✅ |
| 3D holding visuals for augmented rulers | ❌ | Stretch goal |

---

## Implementation Order (Suggested)

1. `eotg_augmentation_traits.txt` — define all four traits
2. `eotg_augmentation_modifiers.txt` — define all static modifiers
3. `eotg_augmentation_triggers.txt` — define scripted triggers
4. `eotg_augmentation_effects.txt` — define scripted effects
5. `eotg_augmentation_initiation.txt` — wire entry events, test trait gain in-engine
6. `eotg_augmentation_tier1.txt` — Augmented events + progression gate
7. `eotg_augmentation_tier2.txt` — Enhanced events + progression gate
8. `eotg_augmentation_fracture.txt` — Neurofracture transform event first, then NF random events
9. `eotg_augmentation_tier3.txt` — Overclocked events (risk accumulation loop)
10. `eotg_augmentation_on_actions.txt` — wire monthly pulses last, after events exist to call
11. Localization pass
12. CK3 Tiger validation run
