"""
Inner module for door card.
"""

from onirim.card._base import ColorCard
from onirim.card._location import LocationKind


def _is_openable(door_card, card):
    """Check if the door can be opened by another card."""
    return card.kind == LocationKind.key and door_card.color == card.color


def _may_open(door_card, content):
    """Check if the door may be opened by agent."""
    return any(_is_openable(door_card, card) for card in content.hand)


class _Door(ColorCard):
    """Door card."""

    def drawn(self, agent, content):
        do_open = agent.open_door(content, self) if _may_open(self, content) else False
        if do_open:
            content.opened.append(self)
            for card in content.hand:
                if _is_openable(self, card):
                    content.hand.remove(card)
                    break
        else:
            content.piles.put_limbo(self)


def door(color):
    """
    Make a door card with specific color.

    Args:
        color (Color): The specific color.

    Returns:
        Card: A door card.
    """
    return _Door(color)
