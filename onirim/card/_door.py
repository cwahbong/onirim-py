"""
Inner module for door card.
"""

import logging

from onirim.card._base import ColorCard
from onirim.card._location import LocationKind
from onirim import exception


LOGGER = logging.getLogger(__name__)


def _is_openable(door_card, card):
    """Check if the door can be opened by another card."""
    return card.kind == LocationKind.key and door_card.color == card.color


def _may_open(door_card, content):
    """Check if the door may be opened by actor."""
    return any(_is_openable(door_card, card) for card in content.hand)


class _Door(ColorCard):
    """Door card."""

    def _do_drawn(self, core):
        actor = core.actor
        observer = core.observer
        content = core.content

        do_open = False
        if _may_open(self, content):
            do_open = actor.open_door(content, self)
            LOGGER.info("Actor choose open door: %s.", do_open)
        else:
            LOGGER.info("Cannot open drawn door.")
        if not do_open:
            content.piles.put_limbo(self)
            return
        content.opened.append(self)
        observer.on_door_obtained_by_key(core.content)
        for card in content.hand:
            if _is_openable(self, card):
                content.hand.remove(card)
                content.piles.put_discard(card)
                break
        else:
            assert False
        LOGGER.debug("Door opened by key in hand, color=%s.", self._color_name())
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
