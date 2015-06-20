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

    def _color_name(self):
        return self._color.name if self._color else "nocolor"

    def _class_name(self):
        return self.__class__.__name__[1:].lower()

    @property
    def color(self):
        """Color of a card."""
        return self._color

    @property
    def kind(self):
        """Kind of a card if it is a location."""
        return self._kind

    def drawn(self, agent, content):
        """Called whil this card is drawn."""
        pass

    def __eq__(self, other):
        return self._kind == other.kind and self._color == other.color

    def __str__(self):
        return "{1} {0} card".format(self._class_name(), self._color_name())

    def __repr__(self):
        return "Card{{color: {}, kind: {}}}".format(self._color, self._kind)


class ColorCard(Card):
    """A card with color."""

    def __init__(self, color):
        if not isinstance(color, Color):
            raise ValueError()
        self._color = color
