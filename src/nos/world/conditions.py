from __future__ import annotations

import dataclasses
import typing

import nos.world as world
import nos.world.movement as world_movement


@dataclasses.dataclass
class Condition:
    description: typing.ClassVar[str] = None
    name: str = None
    duration: int = None  # in turns (6 seconds)
    remaining_duration: int = dataclasses.field(default=None)  # in turns (6 seconds)

    def __post_init__(self):
        self.name = self.name or type(self).__name__
        self.remaining_duration = (
            self.duration
            if self.remaining_duration is None or self.duration is None
            else self.remaining_duration
        )

    def __str__(self):
        string = self.name
        if self.remaining_duration:
            string += f" for {self.remaining_duration} turns"
        return string

    def apply_to(self, entity):
        pass

    def remove_from(self, entity):
        pass


class Blinded(Condition):
    description = "A blinded creature can't see and automatically fails any ability check that requires sight."


class Charmed(Condition):
    description = (
        "A charmed creature can't attack the charmer "
        "or target the charmer with harmful abilities or magical effects."
    )
    by: object = None


class Deafened(Condition):
    description = "A deafened creature can't hear and automatically fails any ability check that requires hearing."


class Frightened(Condition):
    description = (
        "A frightened creature has disadvantage on ability checks and attack rolls "
        "while the source of its fear is within line of sight."
    )
    by: object = None


class Immobilized(Condition):
    description = "An immobilized creature has zero movement speed."
    _original_speed: dict[str, int] = dataclasses.field(
        init=False, default_factory=dict
    )

    def apply_to(self, entity):
        self._original_speed = {}
        for movement in entity.movements:
            self._original_speed[movement] = movement.speed
            movement.speed = 0

    def remove_from(self, entity):
        for movement in entity.movements:
            movement.speed = self._original_speed[movement.name]


class Grappled(Condition):
    description = "A grappled creature's speed becomes 0, and it can't benefit from any bonus to its speed."
    by: object = None


class Incapacitated(Condition):
    description = "An incapacitated creature can't take actions or reactions."
    _action: typing.ClassVar[world.Action] = world.Action(
        name="Incapacitated", description=description
    )

    def apply_to(self, entity):
        entity.action = self._action
        entity.bonus_action = self._action
        entity.reaction = self._action

    def remove_from(self, entity):
        entity.action = None
        entity.bonus_action = None
        entity.reaction = None


class Invisible(Condition):
    description = (
        "An invisible creature is impossible to see without the aid of magic or a special sense. "
        "For the purpose of hiding, the creature is heavily obscured. "
        "The creature's location can be detected by any noise it makes or any tracks it leaves."
    )


class Paralyzed(Incapacitated, Immobilized):
    description = (
        "A paralyzed creature is incapacitated and can't move or speak. "
        + Incapacitated.description
        + "The creature automatically fails Strength and Dexterity saving throws. "
        "Attack rolls against the creature have advantage. "
        "Any attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature."
    )

    def apply_to(self, entity):
        Incapacitated.apply_to(self, entity)
        Immobilized.apply_to(self, entity)

    def remove_from(self, entity):
        Incapacitated.apply_to(self, entity)
        Immobilized.apply_to(self, entity)


class Petrified(Incapacitated, Immobilized):
    description = (
        "A petrified creature is transformed, along with any nonmagical object it is wearing or carrying, "
        "into a solid inanimate substance (usually stone). "
        "Its weight increases by a factor of ten, and it ceases aging."
    )

    def apply_to(self, entity):
        Incapacitated.apply_to(self, entity)
        Immobilized.apply_to(self, entity)

    def remove_from(self, entity):
        Incapacitated.apply_to(self, entity)
        Immobilized.apply_to(self, entity)


class Poisoned(Condition):
    description = (
        "A poisoned creature has disadvantage on attack rolls and ability checks."
    )


class Prone(Condition):
    description = (
        "A prone creature's only movement option is to crawl, "
        "unless it stands up and thereby ends the condition."
    )
    _original_movements: list[world.Movement] = dataclasses.field(
        init=False, default_factory=list
    )

    def apply_to(self, entity):
        self._original_movements = entity.movements.copy()
        walking_movements = [
            movement
            for movement in self._original_movements
            if isinstance(movement, world.movement.Walk)
        ]
        crawl_speed = (
            max(
                movement.speed
                // (1 if isinstance(movement, world_movement.Crawl) else 2)
                for movement in walking_movements
            )
            if walking_movements
            else None
        )
        entity.movements = []
        if crawl_speed is not None:
            entity.movements = [world_movement.Crawl(crawl_speed)]

    def remove_from(self, entity):
        entity.movements = self._original_movements


class Restrained(Immobilized):
    description = (
        "A restrained creature's speed becomes 0, "
        "and it can't benefit from any bonus to its speed. "
        "Attack rolls against the creature have advantage, "
        "and the creature's attack rolls have disadvantage."
    )


class Stunned(Incapacitated, Immobilized):
    description = "A stunned creature is incapacitated, can't move, and can speak only falteringly."


@dataclasses.dataclass
class Unconscious(Incapacitated, Immobilized, Prone):
    description: typing.ClassVar[str] = (
        "An unconscious creature is incapacitated, can't move or speak, and is unaware of its surroundings. "
        "The creature drops whatever it's holding and falls prone. "
        "The creature automatically fails Strength and Dexterity saving throws. "
        "Attack rolls against the creature have advantage. "
        "Any attack that hits the creature is a critical hit "
        "if the attacker is within 5 feet of the creature."
    )
    dying: bool = False
    saves: int = 0
    fails: int = 0


@dataclasses.dataclass
class Exhaustion(Condition):
    description = (
        "Some special abilities and environmental hazards, "
        "such as starvation and the long-term effects of freezing or scorching temperatures, "
        "can lead to a special condition called exhaustion. "
        "Exhaustion is measured in six levels. "
    )
    levels: int = None

    def __post_init__(self):
        super().__post_init__()
        if self.levels is None:
            raise ValueError("Exhaustion must have a number of points.")


class Dead(Unconscious):
    description = "A dead creature is an ex-creature."
