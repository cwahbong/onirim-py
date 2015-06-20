"""Location cards."""

from onirim.card._base import ColorCard
from onirim import exception
from onirim import util


class LocationKind(util.AutoNumberEnum):
    """
    Enumerated kinds of locations.

    Attributes:
        sun
        moon
        key
    """
    sun = ()
    moon = ()
    key = ()


def _can_obtain_door(content):
    last_card = content.explored[-1]
    same_count = 0
    for card in reversed(content.explored):
        if last_card.color == card.color:
            same_count += 1
        else:
            break
    return same_count % 3 == 0


class _Location(ColorCard):
    """Location card without special effect."""

    def __init__(self, color, kind=None):
        super().__init__(color)
        if kind is not None:
            self._kind = kind

    def _class_name(self):
        return "{} location".format(self._kind.name)

    def drawn(self, agent, content):
        content.hand.append(self)

    def play(self, agent, content):
        if content.explored and content.explored[-1].kind == self.kind:
            raise exception.ConsecutiveSameKind
        content.explored.append(self)
        content.hand.remove(self)
        if _can_obtain_door(content):
            agent.obtain_door(agent)
            color = content.explored[-1].color
            card = content.piles.pull_door(color)
            if card is not None:
                content.opened.append(card)

    def _on_discard(self, agent, content):
        pass

    def discard(self, agent, content):
        content.hand.remove(self)
        content.piles.put_discard(self)
        self._on_discard(agent, content)


def sun(color):
    """
    Make a sun location card with specific color.

    Args:
        color (Color): The specific color.

    Returns:
        Card: A sun location card.
    """
    return _Location(color, LocationKind.sun)


def moon(color):
    """
    Make a moon location card with specific color.

    Args:
        color (Color): The specific color.

    Returns:
        Card: A moon location card.
    """
    return _Location(color, LocationKind.moon)


class _KeyLocation(_Location):

    _kind = LocationKind.key

    def _on_discard(self, agent, content):
        # TODO draw at most 5 card, discard 1, and put 4 back.
        pass


def key(color):
    """
    Make a key location card with specific color.

    Args:
        color (Color): The specific color.

    Returns:
        Card: A key location card.
    """
    return _KeyLocation(color)
