"""
Inner module for enumerations and base types.
"""

import logging

from onirim import util


LOGGER = logging.getLogger(__name__)


class Color(util.AutoNumberEnum):
    """
    Enumerated colors of cards.

    Attributes:
        red
        blue
        green
        yellow
    """
    red = ()
    blue = ()
    green = ()
    yellow = ()


class Card:
    """
    A card in onirim.

    All cards in onirim inherits from this class. Methods called by some event
    has a single parameter `core` (:py:class:`onirim.core.Core`) for accessing the game
    information.
    """

    _color = None
    _kind = None

    def _color_name(self):
        return self._color.name if self._color else "nocolor"

    def _kind_name(self):
        return self._kind.name if self._kind else "nokind"

    def _class_name(self):
        return self.__class__.__name__[1:].lower()

    @property
    def color(self):
        """
        Color of a card.

        Returns:
            The color of card if it has color, None otherwise.
            Currently only nightmare cards have no color.
        """
        return self._color

    @property
    def kind(self):
        """
        Kind of a card if it is a location.

        Returns:
            The kind of card if it is a location, None otherwise.
        """
        return self._kind

    def _do_drawn(self, core):
        raise NotImplementedError

    def drawn(self, core):
        """
        Called while this card is drawn.
        """
        LOGGER.debug("A card is drawn, %r.", self)
        self._do_drawn(core)

    def _do_play(self, core):
        raise NotImplementedError

    def play(self, core):
        """
        Called while this card is played.
        """
        LOGGER.debug(
            "A card is played, color=%s, kind=%s.",
            self._color_name(),
            self._kind_name())
        self._do_play(core)

    def _do_discard(self, core):
        raise NotImplementedError

    def discard(self, core):
        """
        Called while this card is discarded.
        """
        LOGGER.debug(
            "A card is discarded, color=%s, kind=%s.",
            self._color_name(),
            self._kind_name())
        self._do_discard(core)

    def __eq__(self, other):
        return self._kind == other.kind and self._color == other.color

    def __hash__(self):
        key_int = self.kind.value if self.kind else 0
        color_int = self.color.value if self.color else 0
        return key_int * 10 + color_int

    def __str__(self):
        return "{1} {0} card".format(self._class_name(), self._color_name())

    def __repr__(self):
        return "Card{{color: {}, kind: {}}}".format(self._color, self._kind)


class ColorCard(Card):
    """A card with color."""

    def __init__(self, color):
        # pylint is not smart enough to recognize enum class so we disable the
        # function arguments check here.
        self._color = Color(color) #pylint: disable=too-many-function-args
