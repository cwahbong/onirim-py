"""
Tests for a nightmare card.
"""

import pytest

from onirim import action
from onirim import card
from onirim import core
from onirim import component
from onirim import agent


def test_nightmare_str():
    """
    Test its str()
    """
    assert str(card.nightmare()) == "nocolor nightmare card"


class NightmareActor(agent.Actor):
    """
    An agent that always return a fixed nightmare action.
    """
    def __init__(self, nightmare_action, additional):
        self._nightmare_action = nightmare_action
        self._additional = additional

    def nightmare_action(self, content):
        return self._nightmare_action, self._additional


BY_KEY_PARAMS = (
    action.Nightmare.by_key,
    {"idx": 1},
    component.Content(
        undrawn_cards=[],
        discarded=[],
        limbo=[],
        hand=[
            card.moon(card.Color.blue),
            card.key(card.Color.green),
            ] + [card.moon(card.Color.blue)] * 3,
        explored=[],
        opened=[]
        ),
    component.Content(
        undrawn_cards=[],
        discarded=[card.key(card.Color.green), card.nightmare()],
        limbo=[],
        hand=[card.moon(card.Color.blue)] * 4,
        explored=[],
        opened=[]
        ),
    )

BY_DOOR_PARAMS = (
    action.Nightmare.by_door,
    {"idx": 0},
    component.Content(
        undrawn_cards=[],
        discarded=[],
        limbo=[],
        hand=[card.moon(card.Color.blue)] * 5,
        explored=[],
        opened=[card.door(card.Color.blue), card.door(card.Color.yellow)]
        ),
    component.Content(
        undrawn_cards=[],
        discarded=[card.nightmare()],
        limbo=[card.door(card.Color.blue)],
        hand=[card.moon(card.Color.blue)] * 5,
        explored=[],
        opened=[card.door(card.Color.yellow)]
        ),
    )

BY_HAND_PARAMS = (
    action.Nightmare.by_hand,
    {},
    component.Content(
        undrawn_cards=[card.sun(card.Color.red)] * 5,
        discarded=[],
        limbo=[],
        hand=[card.moon(card.Color.blue)] * 5,
        explored=[],
        opened=[]
        ),
    component.Content(
        undrawn_cards=[],
        discarded=[card.moon(card.Color.blue)] * 5 + [card.nightmare()],
        limbo=[],
        hand=[card.sun(card.Color.red)] * 5,
        explored=[],
        opened=[]
        ),
    )

BY_DECK_PARAMS = (
    action.Nightmare.by_deck,
    {},
    component.Content(
        undrawn_cards=[card.door(card.Color.red)] + [card.sun(card.Color.red)] * 4,
        discarded=[],
        limbo=[],
        hand=[card.moon(card.Color.blue)] * 5,
        explored=[],
        opened=[]
        ),
    component.Content(
        undrawn_cards=[],
        discarded=[card.sun(card.Color.red)] * 4 + [card.nightmare()],
        limbo=[card.door(card.Color.red)],
        hand=[card.moon(card.Color.blue)] * 5,
        explored=[],
        opened=[]
        ),
    )

ACTION_HANDLING_CASES = [
    BY_KEY_PARAMS,
    BY_DOOR_PARAMS,
    BY_HAND_PARAMS,
    BY_DECK_PARAMS,
    ]

@pytest.mark.parametrize(
    "nightmare_action, additional, content, content_after",
    ACTION_HANDLING_CASES
    )
def test_action_handling(nightmare_action, additional, content, content_after):
    """
    Handling nightmare.
    """
    nightmare_actor = NightmareActor(nightmare_action, additional)
    nightmare_card = card.nightmare()
    nightmare_card.drawn(core.Core(nightmare_actor, agent.Observer(), content))
    assert content == content_after


ACTION_HANDLING_KWARGS_CASES = [
    (action.Nightmare.by_key, {}, ValueError),
    (action.Nightmare.by_key, {"bad_key": 0}, KeyError),
    (action.Nightmare.by_key, {"idx": 0}, None),
    (action.Nightmare.by_key, {"idx": 1}, ValueError),
    (action.Nightmare.by_door, {}, ValueError),
    (action.Nightmare.by_door, {"bad_key": 0}, KeyError),
    (action.Nightmare.by_door, {"idx": 0}, None),
    (action.Nightmare.by_hand, {}, None),
    (action.Nightmare.by_hand, {"non_empty": 0}, ValueError),
    (action.Nightmare.by_deck, {}, None),
    (action.Nightmare.by_deck, {"non_empty": 0}, ValueError),
    ]


@pytest.mark.parametrize(
    "nightmare_action, additional, raises",
    ACTION_HANDLING_KWARGS_CASES
    )
def test_action_handling_kwargs(nightmare_action, additional, raises):
    """
    Test kwargs format error.
    """
    nightmare_actor = NightmareActor(nightmare_action, additional)
    nightmare_card = card.nightmare()
    content = component.Content(
        undrawn_cards=[card.sun(card.Color.red)] * 5,
        discarded=[],
        limbo=[],
        hand=[card.key(card.Color.red)] + [card.moon(card.Color.red)] * 4,
        explored=[],
        opened=[card.door(card.Color.red)]
        )
    nightmare_core = core.Core(nightmare_actor, agent.Observer(), content)
    if raises is None:
        nightmare_card.drawn(nightmare_core)
    else:
        with pytest.raises(raises):
            nightmare_card.drawn(nightmare_core)
