import dataclasses
import typing
from abc import ABC


@dataclasses.dataclass
class Ability(ABC):
    score: int = 10

    @property
    def bonus(self):
        return (self.score - 10) // 2

    @property
    def name(self):
        return self.__class__.name

    def __str__(self):
        return f"{self.bonus:+d} {self.name} ({self.score})"


class Strength(Ability):
    pass


class Dexterity(Ability):
    pass


class Constitution(Ability):
    pass


class Intelligence(Ability):
    pass


class Wisdom(Ability):
    pass


class Charisma(Ability):
    pass


@dataclasses.dataclass
class Abilities:
    _types: typing.ClassVar[list[type[Ability]]] = [
        Strength,
        Dexterity,
        Constitution,
        Intelligence,
        Wisdom,
        Charisma,
    ]
    strength: Strength | int | tuple[int, int, int, int, int, int] = dataclasses.field(
        default_factory=Strength
    )
    dexterity: Dexterity | int = dataclasses.field(default_factory=Dexterity)
    constitution: Constitution | int = dataclasses.field(default_factory=Constitution)
    intelligence: Intelligence | int = dataclasses.field(default_factory=Intelligence)
    wisdom: Wisdom | int = dataclasses.field(default_factory=Wisdom)
    charisma: Charisma | int = dataclasses.field(default_factory=Charisma)

    def __post_init__(self):
        if isinstance(self.strength, tuple):
            strength, dex, con, intelligence, wis, cha = self.strength
            self.strength = Strength(strength)
            self.dexterity = Dexterity(dex)
            self.constitution = Constitution(con)
            self.intelligence = Intelligence(intelligence)
            self.wisdom = Wisdom(wis)
            self.charisma = Charisma(cha)
        for field, type_ in zip(dataclasses.fields(self), self._types):
            if isinstance(score := getattr(self, field.name), Ability):
                continue
            if not isinstance(score, int):
                raise TypeError(
                    f"Expected {field.name} to be an Ability or an int, not {type(score)}"
                )
            setattr(self, field.name, type_(score))

    def __str__(self):
        return "\n".join(str(ability) for ability in dataclasses.astuple(self))


@dataclasses.dataclass
class Skill:
    name: str
    associated_ability: type[Ability]

    def __str__(self):
        return self.name


acrobatics = Skill("Acrobatics", Dexterity)
animal_handling = Skill("Animal Handling", Wisdom)
arcana = Skill("Arcana", Intelligence)
athletics = Skill("Athletics", Strength)
deception = Skill("Deception", Charisma)
history = Skill("History", Intelligence)
insight = Skill("Insight", Wisdom)
intimidation = Skill("Intimidation", Charisma)
investigation = Skill("Investigation", Intelligence)
medicine = Skill("Medicine", Wisdom)
nature = Skill("Nature", Intelligence)
perception = Skill("Perception", Wisdom)
performance = Skill("Performance", Charisma)
persuasion = Skill("Persuasion", Charisma)
religion = Skill("Religion", Intelligence)
sleight_of_hand = Skill("Sleight of Hand", Dexterity)
stealth = Skill("Stealth", Dexterity)
survival = Skill("Survival", Wisdom)
standard_skills = [
    acrobatics,
    animal_handling,
    arcana,
    athletics,
    deception,
    history,
    insight,
    intimidation,
    investigation,
    medicine,
    nature,
    perception,
    performance,
    persuasion,
    religion,
    sleight_of_hand,
    stealth,
    survival,
]
