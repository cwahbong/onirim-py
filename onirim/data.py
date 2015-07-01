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
    """Get all cards used in basic onirim."""
    return itertools.chain(
        _color_cards(card.sun, card.Color.red, 9),
        _color_cards(card.sun, card.Color.blue, 8),
        _color_cards(card.sun, card.Color.green, 7),
        _color_cards(card.sun, card.Color.yellow, 6),
        _all_color_cards(card.moon, 3),
        _all_color_cards(card.key, 3),
        _all_color_cards(card.door, 2),
        _no_color_cards(card.nightmare, 10),
        )


def starting_content():
    # TODO support for different expansions
    return component.Content(basic_cards())
