import dataclasses

import nos.world as world
import nos.world.creatures as creatures


def new_skeleton():
    return creatures.Creature(
        1,
        "1",
        1,
    )


@dataclasses.dataclass
class Skeleton(creatures.Creature):
    name: str = "Skeleton"
    description: str = "An animated pile of bones hostile to all life."
    armor_class: int = 13
    max_hit_points = 13
    speed: int = 30
    proficiency_bonus: int = 2
    size: world.Size = world.Medium(height=5.5, width=1, length=1, weight=20)
    abilities: world.Abilities = world.abilities.Abilities(10, 14, 15, 6, 8, 5)
