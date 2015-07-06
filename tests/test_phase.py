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
    core.setup(None, content)

    assert len(content.hand) == 5
    count_content = collections.Counter(content.hand + content.piles.undrawn)
    count_starting = collections.Counter(starting)
    assert count_content == count_starting


class DiscardAgent(agent.Agent):

    def phase_1_action(self, content):
        return action.Phase1.discard, 0


def test_phase_1_discard_action():
    discard_agent = DiscardAgent()
    content = component.Content(
        undrawn_cards=[],
        hand=[card.sun(card.Color.red), card.moon(card.Color.blue)]
        )
    core.phase_1(discard_agent, content)
    assert content == component.Content(
        undrawn_cards=[],
        hand=[card.moon(card.Color.blue)],
        discarded=[card.sun(card.Color.red)]
        )



class WinAgent(agent.Agent):

    def phase_1_action(self, content):
        return action.Phase1.play, 0

    def open_door(self, content, door_card):
        return True


def test_phase_1_pull_door_win():
    win_agent = WinAgent()
    content = component.Content(
        undrawn_cards=[card.door(card.Color.red)],
        opened=[card.door(card.Color.red)] * 7,
        explored=[card.sun(card.Color.red), card.moon(card.Color.red)],
        hand=[card.sun(card.Color.red)]
        )
    with pytest.raises(exception.Win):
        core.phase_1(win_agent, content)
        print(content)


def test_phase_2_draw_door_win():
    win_agent = WinAgent()
    content = component.Content(
        undrawn_cards=[card.door(card.Color.red)],
        opened=[card.door(card.Color.red)] * 7,
        hand=[card.key(card.Color.red)]
        )
    with pytest.raises(exception.Win):
        core.phase_2(win_agent, content)
