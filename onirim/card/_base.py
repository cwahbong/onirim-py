from onirim import util

class Color(util.AutoNumberEnum):
    red = ()
    blue = ()
    green = ()
    yellow = ()


class Card:
    """A card in onirim."""

    _color = None
    _kind = None

    @property
    def color(self):
        """Color of a card."""
        return self._color

    @property
    def kind(self):
        """Kind of a card if it is a location."""
        return self._kind


class ColorCard(Card):
    """A card with color."""

    def __init__(self, color):
        if not isinstance(color, Color):
            raise ValueError()
        self._color = color
