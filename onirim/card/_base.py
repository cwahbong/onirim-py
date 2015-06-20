from onirim import util

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

Color.red.__doc__ = "asdf"


class Card:
    """
    A card in onirim.

    All cards in onirim inherits from this class.
    """

    _color = None
    _kind = None

    def _color_name(self):
        """
        Get the name of its color.
        """
        return self._color.name if self._color else "nocolor"

    def _class_name(self):
        """
        Get the name of its class.
        """
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

    def drawn(self, agent, content):
        """
        Called while this card is drawn.

        Args:
            agent (onirim.agent.Agent): The agent of onirim.
            content (onirim.component.Content): The content of onirim.
        """
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
