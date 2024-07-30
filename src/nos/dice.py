import dataclasses
import random


class Situation:
    ADVANTAGE = "advantage"
    DISADVANTAGE = "disadvantage"
    ELVEN_ACCURACY = "elven_accuracy"


@dataclasses.dataclass
class Die:
    sides: int = 20

    def roll(self, situation: str = None):
        result = [random.randint(1, self.sides)]
        match situation:
            case Situation.ADVANTAGE:
                return max(self.roll(), result)
            case Situation.DISADVANTAGE:
                return min(self.roll(), result)
            case Situation.ELVEN_ACCURACY:
                return max(self.roll(), self.roll(), result)
            case _:
                return result

    def __str__(self):
        return f"d{self.sides}"

    def __repr__(self):
        return f"Die(sides={self.sides})"


coin = Die(2)
d2 = coin
d3 = Die(3)
d4 = Die(4)
d6 = Die(6)
d8 = Die(8)
d10 = Die(10)
d12 = Die(12)
d20 = Die(20)
d100 = Die(100)


class Roll:
    def __init__(self, *dice: Die):
        self.dice = dice

    def roll(self, highest: int = None, lowest: int = None):
        if highest and lowest:
            raise ValueError("Cannot specify both highest and lowest")
        dice = [d.roll() for d in self.dice]
        if highest:
            dice = sorted(dice)[-highest:]
        if lowest:
            dice = sorted(dice)[:lowest]
        return sum(dice)

    def __str__(self):
        return " + ".join(map(str, self.dice))

    def __repr__(self):
        return f'Roll({", ".join(map(repr, self.dice))})'


def roll(dice: list[Die], highest: int = None, lowest: int = None):
    return Roll(*dice).roll(highest, lowest)
