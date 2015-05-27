from onirim import util

class Color(util.AutoNumberEnum):
    red = ()
    blue = ()
    green = ()
    yellow = ()


class Card:
    """A card in onirim."""

    _color = None

    @property
    def color(self):
        """Color of a card."""
        return self._color

    @property
    def kind(self):
        return None


class ColorCard(Card):
    """A card with color."""

    def __init__(self, color):
        if not isinstance(color, Color):
            raise ValueError()
        self._color = color
