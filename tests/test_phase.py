"""
Tests for a phase.
"""

import pytest

from onirim import card
from onirim import core
from onirim import action
from onirim import exception
from onirim import component
from onirim import agent


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
