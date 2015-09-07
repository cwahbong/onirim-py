"""Data that initializes onirim."""


import itertools

from onirim import card
from onirim import component


def _no_color_cards(card_factory, times):
    """Generates cards without color."""
    return itertools.repeat(card_factory(), times)


def _color_cards(card_factory, color, times):
    """Generates cards with specific color."""
    return itertools.repeat(card_factory(color), times)


def _all_color_cards(card_factory, times):
    """Generates cards with all colors."""
    return itertools.chain.from_iterable(
        _color_cards(card_factory, c, times) for c in card.Color
        )


def basic_cards():
    """
    Make an iterator that returns all cards in basic onirim.

    Returns:
        iterator: All cards in basic onirim.
    """
    return itertools.chain(
        _color_cards(card.sun, card.Color.red, 9),
        _color_cards(card.sun, card.Color.blue, 8),
        _color_cards(card.sun, card.Color.green, 7),
        _color_cards(card.sun, card.Color.yellow, 6),
        _all_color_cards(card.moon, 4),
        _all_color_cards(card.key, 3),
        _all_color_cards(card.door, 2),
        _no_color_cards(card.nightmare, 10),
        )


def starting_content():
    """
    Make a content for a new game.

    Returns:
        content (onirim.component.Content): A content with all basic cards in
        undrawn deck.
    """
    # TODO support for different expansions
    return component.Content(basic_cards())
