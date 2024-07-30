import dataclasses

import nos.world as world
import nos.world.attacks as atks


@dataclasses.dataclass
class Creature(world.Entity):
    attacks: [atks.Attack] = dataclasses.field(default_factory=list)
    actions: [world.Action] = dataclasses.field(default_factory=list)
    reactions: [world.Action] = dataclasses.field(default_factory=list)
    carrying_capacity: float = dataclasses.field(init=False)
    inventory: [world.Item] = dataclasses.field(default_factory=list)

    def __post_init__(self):
        self.carrying_capacity = (
            self.size.carrying_capacity_multiplier * self.abilities.strength.score
        )

    def move(self, dx, dy, dz=0):
        self.world_position.x += dx
        self.world_position.y += dy
        self.world_position.z += dz
        self.turn.movement += (dx**2 + dy**2 + dz**2) ** 0.5

    def attack(self, target: world.Entity, attack: atks.Attack):
        hit, damage, effects = attack.resolve(self, target)
        for effect in effects:
            if isinstance(effect, atks.Attack):
                self.attack(target, effect)
            elif isinstance(effect, world.Condition):
                target.conditions.append(effect)
