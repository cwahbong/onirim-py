"""
Tests for is_XXX functions for card.
"""

import pytest

from onirim import card


IS_LOCATION_CASES = [
    (card.sun(card.Color.red), True),
    (card.moon(card.Color.blue), True),
    (card.key(card.Color.yellow), True),
    (card.door(card.Color.green), False),
    (card.nightmare(), False),
    ]

@pytest.mark.parametrize(
    "ocard, expected",
    IS_LOCATION_CASES)
def test_is_location(ocard, expected):
    assert card.is_location(ocard) == expected


IS_DOOR_CASES = [
    (card.sun(card.Color.red), False),
    (card.moon(card.Color.blue), False),
    (card.key(card.Color.yellow), False),
    (card.door(card.Color.green), True),
    (card.nightmare(), False),
    ]

@pytest.mark.parametrize(
    "ocard, expected",
    IS_DOOR_CASES)
def test_is_door(ocard, expected):
    assert card.is_door(ocard) == expected


IS_NIGHTMARE_CASES = [
    (card.sun(card.Color.red), False),
    (card.moon(card.Color.blue), False),
    (card.key(card.Color.yellow), False),
    (card.door(card.Color.green), False),
    (card.nightmare(), True),
    ]

@pytest.mark.parametrize(
    "ocard, expected",
    IS_NIGHTMARE_CASES)
def test_is_nightmare(ocard, expected):
    assert card.is_nightmare(ocard) == expected
