"""
Inner module for card utilities.
"""

def is_location(card):
    """
    Return true if `card` is a location card, false otherwise.
    """
    return card.kind is not None and card.color is not None


def is_door(card):
    """
    Return true if `card` is a door card, false otherwise.
    """
    return card.kind is None and card.color is not None


def is_nightmare(card):
    """
    Return true if `card` is a nightmare card, false otherwise.
    """
    return card.kind is None and card.color is None
