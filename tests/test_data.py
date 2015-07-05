"""
Tests for data.
"""

import collections

from onirim import card
from onirim import data

def test_basic_cards_len():
    """
    Test the number of basic cards.
    """
    assert len(list(data.basic_cards())) == 76


def test_data_count():
    """
    Test the content of basic cards by collections.Counter.
    """
    assert collections.Counter(data.basic_cards()) == {
        card.sun(card.Color.red): 9,
        card.sun(card.Color.blue): 8,
        card.sun(card.Color.green): 7,
        card.sun(card.Color.yellow): 6,
        card.moon(card.Color.red): 4,
        card.moon(card.Color.blue): 4,
        card.moon(card.Color.green): 4,
        card.moon(card.Color.yellow): 4,
        card.key(card.Color.red): 3,
        card.key(card.Color.blue): 3,
        card.key(card.Color.green): 3,
        card.key(card.Color.yellow): 3,
        card.door(card.Color.red): 2,
        card.door(card.Color.blue): 2,
        card.door(card.Color.green): 2,
        card.door(card.Color.yellow): 2,
        card.nightmare(): 10,
        }
