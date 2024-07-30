import dataclasses
from abc import ABC


@dataclasses.dataclass
class Ability(ABC):
    name: str
    score: int = 10
    bonus: int = dataclasses.field(init=False)

    def __post_init__(self):
        self.bonus = (self.score - 10) // 2

    def __str__(self):
        return f"{self.bonus:+d} {self.name} ({self.score})"


class Strength(Ability):
    name = "Strength"


class Dexterity(Ability):
    name = "Dexterity"


class Constitution(Ability):
    name = "Constitution"


class Intelligence(Ability):
    name = "Intelligence"


class Wisdom(Ability):
    name = "Wisdom"


class Charisma(Ability):
    name = "Charisma"


@dataclasses.dataclass
class Abilities:
    strength: Strength = dataclasses.field(default_factory=Strength)
    dexterity: Dexterity = dataclasses.field(default_factory=Dexterity)
    constitution: Constitution = dataclasses.field(default_factory=Constitution)
    intelligence: Intelligence = dataclasses.field(default_factory=Intelligence)
    wisdom: Wisdom = dataclasses.field(default_factory=Wisdom)
    charisma: Charisma = dataclasses.field(default_factory=Charisma)

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
