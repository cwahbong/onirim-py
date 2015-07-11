"""
Tests for a agent.
"""

import io
import os

import pytest

from onirim import action
from onirim import agent
from onirim import component

def file_agent(in_str):
    return agent.File(io.StringIO(in_str), open(os.devnull, "w"))

def content():
    return component.Content([])


@pytest.mark.parametrize(
    "in_str, expected",
    [
        ("play\n0\n", (action.Phase1.play, 0)),
        ("discard\n4\n", (action.Phase1.discard, 4)),
        ]
    )
def test_file_phase_1_action(in_str, expected):
    """
    Test input parsing of phase_1_action.
    """
    assert file_agent(in_str).phase_1_action(content()) == expected


@pytest.mark.parametrize(
    "in_str, expected",
    [
        ("key\n2\n", (action.Nightmare.by_key, {"idx": 2})),
        ("door\n3\n", (action.Nightmare.by_door, {"idx": 3})),
        ("hand\n", (action.Nightmare.by_hand, {})),
        ("deck\n", (action.Nightmare.by_deck, {})),
        ]
    )
def test_file_nightmare_action(in_str, expected):
    """
    Test input parsing of nightmare action.
    """
    assert file_agent(in_str).nightmare_action(content()) == expected

@pytest.mark.parametrize(
    "in_str, expected",
    [
        ("yes\n", True),
        ("no\n", False),
        ]
    )
def test_file_open_door(in_str, expected):
    """
    Test input parsing of open door.
    """
    assert file_agent(in_str).open_door(content(), None) == expected


#def test_file_key_discard_react(in_str, expected):
#TODO
