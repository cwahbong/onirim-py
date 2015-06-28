"""
Tests for a location card.
"""

import pytest

from onirim import card
from onirim import component
from onirim import agent
from onirim import exception

class LocationPlayAgent(agent.Agent):

    def obtain_door(self, content):
        pass


LOCATION_PLAY_CASES = [
    (
        card.sun(card.Color.red),
        component.Content(undrawn_cards=[], hand=[card.sun(card.Color.red)]),
        component.Content(undrawn_cards=[], explored=[card.sun(card.Color.red)]),
        ),
    ]


@pytest.mark.parametrize(
    "location_card, content, content_after",
    LOCATION_PLAY_CASES)
def test_location_play(location_card, content, content_after):
    location_agent = LocationPlayAgent()
    location_card.play(location_agent, content)
    assert content == content_after


LOCATION_PLAY_CONSECUTIVE = [
    (card.sun(card.Color.red), card.sun(card.Color.yellow), True),
    (card.moon(card.Color.blue), card.moon(card.Color.green), True),
    (card.key(card.Color.blue), card.key(card.Color.blue), True),
    (card.key(card.Color.blue), card.sun(card.Color.blue), False),
    ]


@pytest.mark.parametrize(
    "first_card, second_card, raises",
    LOCATION_PLAY_CONSECUTIVE)
def test_location_play_consecutive(first_card, second_card, raises):
    location_agent = LocationPlayAgent()
    content = component.Content(
        undrawn_cards=[],
        hand=[first_card, second_card])
    first_card.play(location_agent, content)
    if raises:
        with pytest.raises(exception.ConsecutiveSameKind):
            second_card.play(location_agent, content)
    else:
        second_card.play(location_agent, content)


class LocationDiscardAgent(agent.Agent):

    def key_discard_react(self, content, cards):
        return 1, [0, 2, 3, 4]


SUN_DISCARDED_CASE = (
    card.sun(card.Color.red),
    component.Content(
        undrawn_cards=[],
        hand=[card.sun(card.Color.red)]),
    component.Content(
        undrawn_cards=[],
        discarded=[card.sun(card.Color.red)]),
    )

MOON_DISCARDED_CASE = (
    card.moon(card.Color.blue),
    component.Content(
        undrawn_cards=[],
        hand=[card.moon(card.Color.blue)]),
    component.Content(
        undrawn_cards=[],
        discarded=[card.moon(card.Color.blue)]),
    )

KEY_DISCARDED_CASE = (
    card.key(card.Color.red),
    component.Content(
        undrawn_cards=[
            card.sun(card.Color.red),
            card.nightmare(),
            ] + [card.sun(card.Color.red)] * 3,
        hand=[card.key(card.Color.red)]),
    component.Content(
        undrawn_cards=[card.sun(card.Color.red)] * 4,
        discarded=[
            card.key(card.Color.red),
            card.nightmare()]),
    )



LOCATION_DISCARD_CASES = [
    SUN_DISCARDED_CASE,
    MOON_DISCARDED_CASE,
    KEY_DISCARDED_CASE,
    ]


@pytest.mark.parametrize(
    "location_card, content, content_after",
    LOCATION_DISCARD_CASES)
def test_location_discard(location_card, content, content_after):
    location_agent = LocationDiscardAgent()
    location_card.discard(location_agent, content)
    assert content == content_after
