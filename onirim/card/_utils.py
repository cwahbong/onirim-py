"""
Inner module for card utilities.
"""

def is_location(card):
    return card.kind is not None and card.color is not None


def is_door(card):
    return card.kind is None and card.color is not None


def is_nightmare(card):
    return card.kind is None and card.color is None
