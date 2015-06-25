"""
Tests for a door card.
"""

import pytest

from onirim import card
from onirim import action
from onirim import component
from onirim import agent


class DoorAgent(agent.Agent):
    """
    """
    def __init__(self, do_open):
        self._do_open = do_open

    def open_door(self, content, door_card):
        return self._do_open


DRAWN_CAN_NOT_OPEN = (
    card.Color.red,
    False,
    component.Content(
        undrawn_cards=[],
        hand=[card.key(card.Color.blue)]),
    component.Content(
        undrawn_cards=[],
        hand=[card.key(card.Color.blue)],
        limbo=[card.door(card.Color.red)]),
    )

DRAWN_DO_NOT_OPEN = (
    card.Color.red,
    False,
    component.Content(
        undrawn_cards=[],
        hand=[card.key(card.Color.red)]),
    component.Content(
        undrawn_cards=[],
        hand=[card.key(card.Color.red)],
        limbo=[card.door(card.Color.red)]),
    )

DRAWN_DO_OPEN = (
    card.Color.red,
    True,
    component.Content(
        undrawn_cards=[],
        hand=[card.key(card.Color.red)]),
    component.Content(
        undrawn_cards=[],
        discarded=[card.key(card.Color.red)],
        opened=[card.door(card.Color.red)]),
    )

DRAWN_CASES = [
    DRAWN_CAN_NOT_OPEN,
    DRAWN_DO_NOT_OPEN,
    DRAWN_DO_OPEN,
    ]


@pytest.mark.parametrize(
    "color, do_open, content, content_after",
    DRAWN_CASES)
def test_drawn(color, do_open, content, content_after):
    door_card = card.door(color)
    door_card.drawn(DoorAgent(do_open), content)
    assert content == content_after
