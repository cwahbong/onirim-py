"""
Inner module for door card.
"""

from onirim.card._base import ColorCard
from onirim.card._location import LocationKind
from onirim import exception


def _is_openable(door_card, card):
    """Check if the door can be opened by another card."""
    return card.kind == LocationKind.key and door_card.color == card.color


def _may_open(door_card, content):
    """Check if the door may be opened by agent."""
    return any(_is_openable(door_card, card) for card in content.hand)


class _Door(ColorCard):
    """Door card."""

    def drawn(self, agent, content):
        do_open = _may_open(self, content) and agent.open_door(content, self)
        if not do_open:
            content.piles.put_limbo(self)
            return
        content.opened.append(self)
        for card in content.hand:
            if _is_openable(self, card):
                content.hand.remove(card)
                content.piles.put_discard(card)
                break
        else:
            assert False
        if len(content.opened) == 8:
            raise exception.Win


def door(color):
    """
    Make a door card with specific color.

    Args:
        color (Color): The specific color.

    Returns:
        Card: A door card.
    """
    return _Door(color)
