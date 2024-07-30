from __future__ import annotations

import dataclasses
import typing
from abc import ABC

from nos import assets
from nos.world.abilities import Abilities, Skill
from nos.world.conditions import Condition
from nos.world.movement import Movement, Position


@dataclasses.dataclass
class Size(ABC):
    square_size: typing.ClassVar[
        float
    ]  # in 5 ft. squares, length of size (1 medium, 2 large, 0.5 tiny...)
    carrying_capacity_multiplier: typing.ClassVar[
        float
    ]  # factor of strength score to determine carrying capacity
    height: float = None  # in feet
    width: float = None  # in feet
    length: float = None  # in feet
    weight: float = None  # in pounds


@dataclasses.dataclass
class Tiny(Size):
    square_size: typing.ClassVar[float] = 0.5
    carrying_capacity_multiplier: typing.ClassVar[float] = 7.5
    height: float = 1.25
    width: float = 1.25
    length: float = 1.25
    weight: float = 10


@dataclasses.dataclass
class Small(Size):
    square_size: typing.ClassVar[float] = 1
    carrying_capacity_multiplier: typing.ClassVar[float] = 15
    height: float = 2.5
    width: float = 2.5
    length: float = 2.5
    weight: float = 50


@dataclasses.dataclass
class Medium(Size):
    square_size: typing.ClassVar[float] = 1
    carrying_capacity_multiplier: typing.ClassVar[float] = 15
    height: float = 5
    width: float = 5
    length: float = 5
    weight: float = 150


@dataclasses.dataclass
class Large(Size):
    square_size: typing.ClassVar[float] = 2
    carrying_capacity_multiplier: typing.ClassVar[float] = 30
    height: float = 10
    width: float = 10
    length: float = 10
    weight: float = 600


@dataclasses.dataclass
class Huge(Size):
    square_size: typing.ClassVar[float] = 3
    carrying_capacity_multiplier: typing.ClassVar[float] = 60
    height: float = 15
    width: float = 15
    length: float = 15
    weight: float = 2500


@dataclasses.dataclass
class Gargantuan(Size):
    square_size: typing.ClassVar[float] = 4
    carrying_capacity_multiplier: typing.ClassVar[float] = 120
    height: float = 20
    width: float = 20
    length: float = 20
    weight: float = 8000


@dataclasses.dataclass
class Phase(ABC):
    name: str
    description: str


class Action(Phase):
    pass


class BonusAction(Action):
    pass


class Reaction(Action):
    pass


class ItemInteraction(Action):
    pass


@dataclasses.dataclass
class Turn:
    """
    A turn in combat. If the attribute is None, it is available to be used.

    Attributes:
    action: Action
    bonus_action: BonusAction
    movement: float The only exception, movement simply tracks the total movement on this turn
        for comparison with speed.
    item_interaction: Action
    reaction: Reaction
    phase_options: list[list[Phase]]
        each sublist contains the options available to the Entity
    """

    action: Action | None = None
    bonus_action: Action | None = None
    movement: float = 0
    item_interaction: ItemInteraction | None = None
    reaction: Action | None = None
    phase_options: list[list[Phase]] = dataclasses.field(default_factory=list)

    def start(self):
        self.action = None
        self.bonus_action = None
        self.movement = 0
        self.item_interaction = None
        self.reaction = None


@dataclasses.dataclass
class Entity:
    name: str
    description: str
    size: Size
    armor_class: int
    max_hit_points: int
    current_hit_points: int = dataclasses.field(default=None)
    asset: assets.Asset = None
    movements: list[Movement] = dataclasses.field(default_factory=list)
    conditions: list[Condition] = dataclasses.field(default_factory=list)
    abilities: Abilities = dataclasses.field(default_factory=Abilities)
    proficiencies: list[Skill] = dataclasses.field(default_factory=list)
    world_position: Position = dataclasses.field(default_factory=Position)
    turn: Turn = dataclasses.field(default_factory=Turn)
    critical_hit_minimum: int = 20
    proficiency_bonus: int = 2

    def __post_init__(self):
        self.current_hit_points = (
            self.max_hit_points
            if self.current_hit_points is None
            else self.current_hit_points
        )

    def start_turn(self):
        self.turn.start()
        for condition in self.conditions:
            if condition.remaining_duration:
                condition.remaining_duration -= 1
        self.conditions = [
            condition
            for condition in self.conditions
            if condition.remaining_duration is None or condition.remaining_duration > 0
        ]
        for condition in self.conditions:
            condition.apply_to(self)


@dataclasses.dataclass
class Item(Entity):
    value: int = 0


@dataclasses.dataclass
class Container(Item):
    capacity: float = None  # weight in pounds
    volume: float = None  # in cubic feet
    items: list[Item] = dataclasses.field(default_factory=list)

    def get_weight(self):
        return (
            sum(
                item.get_weight() if isinstance(item, Container) else item.size.weight
                for item in self.items
            )
            + self.size.weight
        )
