"""
Tests for a phase.
"""

import collections

import pytest

from onirim import card
from onirim import core
from onirim import action
from onirim import exception
from onirim import component
from onirim import agent


def test_setup():
    starting = [
        card.sun(card.Color.red),
        card.moon(card.Color.blue),
        card.key(card.Color.green),
        card.sun(card.Color.yellow),
        card.moon(card.Color.red),
        card.key(card.Color.blue),
        card.nightmare(),
        ]

    content = component.Content(starting)
    flow = core.Flow(core.Core(None, None, content))
    flow.setup()

    assert len(content.hand) == 5
    count_content = collections.Counter(content.hand + content.piles.undrawn)
    count_starting = collections.Counter(starting)
    assert count_content == count_starting


class DiscardActor(agent.Actor):

    def phase_1_action(self, content):
        return action.Phase1.discard, 0


def test_phase_1_discard_action():
    discard_actor = DiscardActor()
    content = component.Content(
        undrawn_cards=[],
        hand=[card.sun(card.Color.red), card.moon(card.Color.blue)]
        )
    flow = core.Flow(core.Core(discard_actor, agent.Observer(), content))
    flow.phase_1()
    assert content == component.Content(
        undrawn_cards=[],
        hand=[card.moon(card.Color.blue)],
        discarded=[card.sun(card.Color.red)]
        )



class WinActor(agent.Actor):

    def phase_1_action(self, content):
        return action.Phase1.play, 0

    def open_door(self, content, door_card):
        return True


def test_phase_1_pull_door_win():
    win_actor = WinActor()
    content = component.Content(
        undrawn_cards=[card.door(card.Color.red)],
        opened=[card.door(card.Color.red)] * 7,
        explored=[card.sun(card.Color.red), card.moon(card.Color.red)],
        hand=[card.sun(card.Color.red)]
        )
    flow = core.Flow(core.Core(win_actor, agent.Observer(), content))
    with pytest.raises(exception.Win):
        flow.phase_1()
        print(content)


def test_phase_2_draw_door_win():
    win_actor = WinActor()
    content = component.Content(
        undrawn_cards=[card.door(card.Color.red)],
        opened=[card.door(card.Color.red)] * 7,
        hand=[card.key(card.Color.red)]
        )
    flow = core.Flow(core.Core(win_actor, agent.Observer(), content))
    with pytest.raises(exception.Win):
        flow.phase_2()


class NightmareHandActor(agent.Actor):

    def nightmare_action(self, content):
        return action.Nightmare.by_hand, {}


def test_phase_2_draw_multiple_nightmare():
    nightmare_actor = NightmareHandActor()
    content = component.Content(
        undrawn_cards=[card.nightmare()] * 2 + [card.moon(card.Color.blue)] * 5,
        hand=[card.sun(card.Color.red)] * 4)
    content_after = component.Content(
        undrawn_cards=[],
        hand=[card.moon(card.Color.blue)] * 5,
        discarded=[card.sun(card.Color.red)] * 4 + [card.nightmare()] * 2)
    flow = core.Flow(core.Core(nightmare_actor, agent.Observer(), content))
    flow.phase_2()
    assert content == content_after
