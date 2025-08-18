# tests/test_dice.py

import math

import pytest

from src.nos.dice import Die, Roll, binomial_cdf, binomial_pdf


@pytest.mark.parametrize("sides,expected", [(6, 3.5), (20, 10.5), (1, 1.0)])
def test_die_expected_value(sides, expected):
    assert Die(sides).expected_value() == expected


@pytest.mark.parametrize("sides", [2, 6, 20])
def test_die_roll_range(sides):
    die = Die(sides)
    for _ in range(100):
        result = die.roll()
        assert 1 <= result <= sides


def test_die_invalid_sides():
    with pytest.raises(ValueError):
        Die(0)
    with pytest.raises(ValueError):
        Die(-5)


def test_roll_straight_expected_value():
    roll = Roll((Die(6), Die(6), Die(6)))
    assert roll._straight_expected_value() == 10.5


def test_get_actual_roll_for_crit_raw():
    roll = Roll((Die(6), Die(6)))
    actual_roll = roll._get_actual_roll_for_crit("RAW")
    assert len(actual_roll.dice) == 4  # RAW doubles the dice
    assert all(isinstance(die, Die) for die in actual_roll.dice)


def test_get_actual_roll_for_crit_none():
    roll = Roll((Die(6), Die(6)))
    actual_roll = roll._get_actual_roll_for_crit(None)
    assert actual_roll == roll  # No change for None crit


def test_get_infinitely_exploding_value():
    roll = Roll((Die(6), Die(6)), explode_highest=1, max_explosions=math.inf)
    value = roll._get_infinitely_exploding_value(None)
    expected = roll._straight_expected_value() * 6 / 5
    assert pytest.approx(value, rel=1e-6) == expected


def test_get_infinitely_exploding_value_perkins():
    roll = Roll((Die(6), Die(6)), explode_highest=1, max_explosions=math.inf)
    value = roll._get_infinitely_exploding_value("Perkins")
    straight = roll._straight_expected_value() * 6 / 5
    bonus = 2 * 36 / 5
    assert pytest.approx(value, rel=1e-6) == straight + bonus


def test_get_perkins_bonus_infinite():
    roll = Roll((Die(6), Die(6)), explode_highest=1)
    bonus = roll._get_perkins_bonus(infinite=True)
    expected = 2 * 6**2 / 5
    assert pytest.approx(bonus, rel=1e-6) == expected


def test_get_perkins_bonus_finite():
    roll = Roll((Die(6), Die(6)), explode_highest=1)
    bonus = roll._get_perkins_bonus(infinite=False)
    expected = 6 * 2
    assert pytest.approx(bonus, rel=1e-6) == expected


def test_get_finite_explosion_value_no_outcomes():
    roll = Roll((Die(6), Die(6)))
    value = roll._get_finite_explosion_value(None, _depth=0)
    assert pytest.approx(value, rel=1e-6) == roll._straight_expected_value()


def test_get_finite_explosion_value_with_outcomes(mocker):
    roll = Roll((Die(6), Die(6)), explode_highest=1, max_explosions=2)
    mocker.patch.object(
        roll,
        "_outcomes",
        return_value=[(Roll((Die(6),)), 0.5), (Roll((Die(6), Die(6))), 0.5)],
    )
    value = roll._get_finite_explosion_value(None, _depth=0)
    expected = (
        roll._straight_expected_value()
        + 0.5 * Roll((Die(6),)).expected_value()
        + 0.5 * Roll((Die(6), Die(6))).expected_value()
    )
    assert pytest.approx(value, rel=1e-6) == expected


def test_roll_raw_crit_expected_value():
    roll = Roll((Die(6), Die(6)))
    raw_crit = roll.expected_value(crit_="RAW")
    assert raw_crit == 14.0  # 4d6: 4 * 3.5


def test_roll_infinitely_exploding_expected_value():
    roll = Roll((Die(6), Die(6)), explode_highest=1, max_explosions=math.inf)
    expected = roll._straight_expected_value() * 6 / (6 - 1)
    assert pytest.approx(roll.expected_value(), rel=1e-6) == expected


def test_roll_infinitely_exploding_high_threshold():
    roll = Roll((Die(6),), explode_highest=5, max_explosions=math.inf)
    expected = roll._straight_expected_value() * 6 / (6 - 5)
    assert pytest.approx(roll.expected_value(), rel=1e-6) == expected


def test_roll_perkins_crit_expected_value():
    roll = Roll((Die(6), Die(6)), explode_highest=1, max_explosions=math.inf)
    value = roll.expected_value(crit_="Perkins")
    straight = roll._straight_expected_value() * 6 / 5
    bonus = 2 * 36 / 5
    assert pytest.approx(value, rel=1e-6) == straight + bonus


@pytest.mark.parametrize(
    "dice,explode_highest,max_explosions",
    [
        ((Die(6), Die(6)), 1, 2),
        ((Die(8), Die(8)), 2, 3),
        ((Die(4), Die(4)), 1, 5),
    ],
)
def test_raw_crit_finite_vs_infinite(dice, explode_highest, max_explosions):
    roll_finite = Roll(
        dice, explode_highest=explode_highest, max_explosions=max_explosions
    )
    roll_infinite = Roll(dice, explode_highest=explode_highest, max_explosions=math.inf)
    raw_finite = roll_finite.expected_value(crit_="RAW")
    raw_infinite = roll_infinite.expected_value(crit_="RAW")
    # RAW crit with finite explosions should not equal infinite explosions
    assert not math.isclose(raw_finite, raw_infinite, rel_tol=1e-6)
    # RAW crit should be greater than or equal to straight expected value
    assert raw_finite >= roll_finite._straight_expected_value() * 2


def test_raw_crit_edge_case_one_explosion():
    roll = Roll((Die(6),), explode_highest=1, max_explosions=1)
    raw = roll.expected_value(crit_="RAW")
    # Should be greater than straight expected value, but less than infinite explosion
    assert raw > roll._straight_expected_value() * 2
    infinite = Roll(
        (Die(6),), explode_highest=1, max_explosions=math.inf
    ).expected_value(crit_="RAW")
    assert raw < infinite


def test_raw_crit_no_explosion():
    roll = Roll((Die(6), Die(6)))
    raw = roll.expected_value(crit_="RAW")
    # Should be exactly double the straight expected value
    assert raw == roll._straight_expected_value() * 2


def test_roll_outcomes_no_explode():
    roll = Roll((Die(6), Die(6)))
    assert roll._outcomes() == []


def test_roll_outcomes_with_explode():
    roll = Roll((Die(6), Die(6)), explode_highest=1, max_explosions=2)
    outcomes = roll._outcomes()
    assert len(outcomes) > 0
    for outcome, prob in outcomes:
        assert isinstance(outcome, Roll)
        assert 0 <= prob <= 1


@pytest.mark.parametrize(
    "k,n,p,expected",
    [
        (1, 2, 0.5, 0.5),
        (2, 2, 0.5, 0.25),
        (0, 2, 0.5, 0.25),
    ],
)
def test_binomial_pdf(k, n, p, expected):
    assert pytest.approx(binomial_pdf(k, n, p), rel=1e-6) == expected


@pytest.mark.parametrize(
    "k,n,p,expected",
    [
        (1, 2, 0.5, 0.75),
        (2, 2, 0.5, 1.0),
        (0, 2, 0.5, 0.25),
    ],
)
def test_binomial_cdf(k, n, p, expected):
    assert pytest.approx(binomial_cdf(k, n, p), rel=1e-6) == expected


def test_roll_repr_and_str():
    roll = Roll((Die(6), Die(8)))
    assert isinstance(repr(roll), str)
    assert isinstance(str(roll), str)
