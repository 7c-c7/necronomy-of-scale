import dataclasses
import math
import random
from typing import Self

TAB = 4 * " "  # 4 spaces for indentation


class Situation:
    ADVANTAGE = "advantage"
    DISADVANTAGE = "disadvantage"
    ELVEN_ACCURACY = "elven_accuracy"


@dataclasses.dataclass(frozen=True)
class Die:
    sides: int = 20

    def __post_init__(self):
        if self.sides < 1:
            raise ValueError("Die must have at least 1 side")
        if not isinstance(self.sides, int):
            raise TypeError("Die sides must be an integer")

    def roll(self, situation: str = None) -> int:
        result = random.randint(1, self.sides)
        match situation:
            case Situation.ADVANTAGE:
                return max(self.roll(), result)
            case Situation.DISADVANTAGE:
                return min(self.roll(), result)
            case Situation.ELVEN_ACCURACY:
                return max(self.roll(), self.roll(), result)
            case _:
                return result

    def expected_value(self) -> float:
        return (self.sides + 1) / 2

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


@dataclasses.dataclass
class Roll:
    dice: tuple[Die, ...]  # Using tuple for immutability
    explode_highest: int = 0
    max_explosions: int | float = math.inf

    def __post_init__(self):
        if not self.explode_highest:
            return
        for die in self.dice:
            if die != self.dice[0]:
                raise NotImplementedError(
                    "All dice in an exploding dice roll must be of the same type for now."
                )

    @property
    def die(self) -> Die | set[Die]:
        """
        Returns the type of die used in the roll.
        """
        if not self.dice:
            raise ValueError("No dice in the roll")
        dice = set(self.dice)
        if len(dice) == 1:
            return next(iter(dice))
        return dice

    def roll(self, highest: int = None, lowest: int = None):
        if highest and lowest:
            raise ValueError("Cannot specify both highest and lowest")
        dice = [d.roll() for d in self.dice]
        if highest:
            dice = sorted(dice)[-highest:]
        if lowest:
            dice = sorted(dice)[:lowest]
        return sum(dice)

    def expected_value(self, crit_: str = None, _depth=0) -> float:
        print(f"{_depth * TAB}Calculating: {f'{crit_} Crit' if crit_ else ''} {self}")
        actual_roll = self._get_actual_roll_for_crit(crit_)
        if actual_roll.max_explosions == math.inf:
            return actual_roll._get_infinitely_exploding_value(crit_)
        return actual_roll._get_finite_explosion_value(crit_, _depth)

    def _straight_expected_value(self) -> float:
        """
        Calculate the expected value of the roll on a straight roll (no advantage or disadvantage or explosions).
        :return:
            The expected value of the roll. e.g. for 3d6, the expected value is 10.5.
        """
        return sum(die.expected_value() for die in self.dice)

    def _infinitely_exploding_expected_value(self, crit_: str | None) -> float:
        straight = self._straight_expected_value()
        if not self.explode_highest:
            return straight
        crit_fac = 2 if crit_ == "RAW" else 1
        if crit_fac * self.explode_highest >= self.die.sides:
            raise ValueError(
                "Explode highest times number of dice generated on explosion must be "
                "less than the number of sides on the die for infinite explosion."
            )
        return (
            straight
            * self.die.sides
            / (self.die.sides - crit_fac * self.explode_highest)
        )

    def _get_actual_roll_for_crit(self, crit_: str | None):
        if crit_ == "RAW":
            return Roll(
                dice=tuple(2 * [die for die in self.dice]),
                explode_highest=self.explode_highest,
                max_explosions=self.max_explosions,
            )
        return self

    def _get_infinitely_exploding_value(self, crit_: str | None):
        value = self._infinitely_exploding_expected_value(crit_)
        if crit_ == "Perkins":
            value += self._get_perkins_bonus(infinite=True)
        return value

    def _get_perkins_bonus(self, infinite=False):
        if infinite:
            return (
                len(self.dice)
                * self.die.sides**2
                / (self.die.sides - self.explode_highest)
            )
        else:
            return self.die.sides * len(self.dice)

    def _get_die_finite_explosion_value(self, crit_: str | None):
        base_value = self.die.expected_value()
        if crit_ == "Perkins":
            base_value += self.die.sides

        def explode(val) -> float:
            return base_value + self.explode_highest / self.die.sides * val

        for i in range(self.max_explosions):
            base_value = explode(base_value)
        return base_value

    def _get_finite_explosion_value(self, crit_: str | None, _depth):
        if len(self.dice) == 1:
            return self._get_die_finite_explosion_value(crit_)
        value = self._straight_expected_value()
        if crit_ == "Perkins":
            value += self._get_perkins_bonus(infinite=False)
        outcomes = self._outcomes()
        if not outcomes:
            return value
        subvalues = [
            p_roll * explosion_roll.expected_value(crit_, _depth + 1)
            for (explosion_roll, p_roll) in outcomes
        ]
        return value + sum(subvalues)

    def _outcomes(self) -> list[(Self, float)]:
        """
        Generate all possible outcomes of the roll, considering the explode_highest and max_explosions.
        :return:
            list of tuples, where each tuple contains a Roll object and its probability of occurring.
        """
        outcomes = []
        if not self.explode_highest:
            return outcomes
        if not self.max_explosions or self.max_explosions == math.inf:
            return outcomes
        probability_exploding = self.explode_highest / self.die.sides
        exploded_dice = []

        for number_exploded in range(1, min(self.max_explosions, len(self.dice)) + 1):
            exploded_dice.append(self.die)
            probability_exploding_n = (
                binomial_pdf(number_exploded, len(self.dice), probability_exploding)
                if number_exploded < self.max_explosions
                else (
                    1
                    - binomial_cdf(
                        number_exploded - 1, len(self.dice), probability_exploding
                    )
                )
            )
            outcomes.append(
                (
                    Roll(
                        tuple(exploded_dice),
                        self.explode_highest,
                        self.max_explosions - number_exploded,
                    ),
                    probability_exploding_n,
                )
            )
        return outcomes

    def __str__(self):
        if isinstance(self.die, Die):
            string = f"{len(self.dice)}{self.die}"
            if self.explode_highest and self.max_explosions:
                exploding_values = list(
                    reversed(
                        range(
                            self.die.sides - self.explode_highest + 1,
                            self.die.sides + 1,
                        )
                    )
                )
                string += f" (explode on {exploding_values}"
                if self.max_explosions != math.inf:
                    string += f", up to {self.max_explosions} times"
                string += ")"
            return string
        return " + ".join(map(str, self.dice))


def roll(dice: list[Die], highest: int = None, lowest: int = None):
    return Roll(*dice).roll(highest, lowest)


def binomial_pdf(k: int, n: int, p: float) -> float:
    if k < 0 or k > n:
        return 0.0
    return math.comb(n, k) * (p**k) * ((1 - p) ** (n - k))


def binomial_cdf(k: int, n: int, p: float) -> float:
    """
    Calculate the cumulative distribution function (CDF) for a binomial random variable
    using the PDF.
    """
    return sum(binomial_pdf(i, n, p) for i in range(k + 1))
