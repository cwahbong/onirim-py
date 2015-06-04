"""Location cards."""

from onirim.card._base import ColorCard
from onirim import exception
from onirim import util


class LocationKind(util.AutoNumberEnum):
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
        if content.explored[-1].kind != self.kind:
            content.explored.append(self)
            content.hand.discard(self)
            agent.notify("card played")
            if _can_obtain_door(content):
                # color = content.explored[-1].color
                # TODO try pull a door with specific color from deck
                pass
        else:
            raise exception.Onirim()

    def _on_discard(self, agent, content):
        pass

    def discard(self, agent, content):
        content.hand.remove(self)
        content.deck.put_discard(self)
        self._on_discard(agent, content)


def sun(color):
    """Make a sun location card."""
    return _Location(color, LocationKind.sun)


def moon(color):
    """Make a moon location card."""
    return _Location(color, LocationKind.moon)


class _KeyLocation(_Location):

    _kind = LocationKind.key

    def _on_discard(self, agent, content):
        # TODO draw at most 5 card, discard 1, and put 4 back.
        pass


def key(color):
    """Make a key location card."""
    return _KeyLocation(color)
