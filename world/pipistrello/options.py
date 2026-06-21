from dataclasses import dataclass
from Options import Toggle, Range, PerGameCommonOptions


class RandomizeAbilities(Toggle):
    """Shuffle movement abilities (Double Jump, Dash) into the item pool."""
    display_name = "Randomize Abilities"
    default = 1


class TrapFrequency(Range):
    """Percentage of filler slots replaced with traps."""
    display_name = "Trap Frequency"
    range_start = 0
    range_end = 50
    default = 10


class DeathLink(Toggle):
    """When you die, all DeathLink players die. When any of them die, so do you."""
    display_name = "Death Link"
    default = 0


@dataclass
class PipistrelloOptions(PerGameCommonOptions):
    randomize_abilities: RandomizeAbilities
    trap_frequency: TrapFrequency
    death_link: DeathLink
