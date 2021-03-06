"""
Inner module for nightmare card.
"""

import logging


from onirim.card._base import Card
from onirim.card._location import LocationKind
from onirim import action
from onirim import component


LOGGER = logging.getLogger(__name__)


def _by_key(content, **kwargs):
    """Nightmare card resolved by key."""
    if len(kwargs) != 1:
        raise ValueError
    idx = kwargs["idx"]
    card = content.hand[idx]
    if card.kind != LocationKind.key:
        raise ValueError("Not a key")
    content.hand.remove(card)
    content.piles.put_discard(card)
    LOGGER.debug("Nightmare resolved by key.")


def _by_door(content, **kwargs):
    """Nightmare card resolved by door."""
    if len(kwargs) != 1:
        raise ValueError
    idx = kwargs["idx"]
    card = content.opened[idx]
    content.opened.remove(card)
    content.piles.put_limbo(card)
    LOGGER.debug("Nightmare resolved by door.")


def _by_hand(content, **kwargs):
    """Nightmare card resolved by hand."""
    if kwargs:
        raise ValueError
    for card in content.hand:
        content.piles.put_discard(card)
    content.hand.clear()
    component.replenish_hand(content)
    LOGGER.debug("Nightmare resolved by hand.")


def _by_deck(content, **kwargs):
    """Nightmare card resolved by deck."""
    if kwargs:
        raise ValueError
    for card in content.piles.draw(5):
        if card.kind is None:
            content.piles.put_limbo(card)
        else:
            content.piles.put_discard(card)
    LOGGER.debug("Nightmare resolved by deck.")


_RESOLVE = {
    action.Nightmare.by_key: _by_key,
    action.Nightmare.by_door: _by_door,
    action.Nightmare.by_hand: _by_hand,
    action.Nightmare.by_deck: _by_deck,
}


class _Nightmare(Card):
    """Nightmare card."""

    def _do_drawn(self, core):
        actor = core.actor
        content = core.content
        nightmare_action, additional = actor.nightmare_action(content)
        LOGGER.info(
            "Actor choose nightmare_action %s, additional %s.",
            nightmare_action.name,
            additional)
        _RESOLVE[nightmare_action](content, **additional)
        content.piles.put_discard(self)


def nightmare():
    """
    Make a nightmare card.

    Returns:
        Card: A nightmare card.
    """
    return _Nightmare()
