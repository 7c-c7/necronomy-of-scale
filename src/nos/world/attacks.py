from __future__ import annotations

import dataclasses

import nos.world as world
import nos.world.abilities as abilities
from nos import dice


@dataclasses.dataclass
class Attack(world.Action):
    name: str
    ability: abilities.Ability
    proficiency_bonus: int
    range: int
    description: str
    weapon: Weapon = None

    def resolve(
        self,
        attacker: world.Entity,
        target: world.Entity,
        situation: str = None,
        crit_range_min: int = 20,
    ):
        die_roll = dice.roll(dice.d20, situation)
        effects_on_hit = []
        effects_on_miss = []
        if die_roll == 1:
            return 0, 0, effects_on_miss
        damage = (
            self.weapon.damage_roll.roll()
            + self.weapon.damage_bonus
            + self.ability.bonus
        )
        if die_roll >= crit_range_min:
            damage += sum(die.sides for die in self.weapon.damage_roll.dice)
            return True, damage, effects_on_hit
        hit = (
            self.ability.bonus
            + self.proficiency_bonus
            + die_roll
            + self.weapon.attack_bonus
        )
        if hit < target.armor_class:
            damage = 0
            effects = effects_on_miss
        else:
            effects = effects_on_hit
        return hit, damage, effects


class Weapon(world.Item):
    attack_bonus: int
    damage_bonus: int
    damage_roll: dice.Roll
    range: int
    reach: int
    properties: list[str] = dataclasses.field(default_factory=list)

    def __str__(self):
        return f"{self.name}"
