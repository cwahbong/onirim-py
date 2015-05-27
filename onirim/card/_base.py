from onirim import util

class Color(util.AutoNumberEnum):
    red = ()
    blue = ()
    green = ()
    yellow = ()


class Card:
    @property
    def color(self):
        return None

    @property
    def kind(self):
        return None


class ColorCard(Card):
    """A card with color."""

    def __init__(self, color):
        if not isinstance(color, Color):
            raise ValueError()
        self._color = color

    @property
    def color(self):
        return self._color
