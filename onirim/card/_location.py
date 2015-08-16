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
    """
    Check if the explored cards can obtain a door.
    """
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

    def drawn(self, core):
        core.content.hand.append(self)

    def play(self, core):
        observer = core.observer
        content = core.content
        if content.explored and content.explored[-1].kind == self.kind:
            raise exception.ConsecutiveSameKind
        content.explored.append(self)
        content.hand.remove(self)
        if _can_obtain_door(content):
            observer.on_door_obtained_by_explore(core.content)
            color = content.explored[-1].color
            card = content.piles.pull_door(color)
            if card is not None:
                content.opened.append(card)
                if len(content.opened) == 8:
                    raise exception.Win

    def _on_discard(self, core):
        """
        Do additional operations after discard a card from hand to discarded
        pile.
        """
        pass

    def discard(self, core):
        content = core.content
        content.hand.remove(self)
        content.piles.put_discard(self)
        self._on_discard(core)


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
    """
    Key location card implementation.
    """

    _kind = LocationKind.key

    def _on_discard(self, core):
        actor = core.actor
        content = core.content

        drawn = content.piles.draw(5)
        discarded_idx, back_idxes = actor.key_discard_react(core.content, drawn)
        # TODO check returned value

        content.piles.put_discard(drawn[discarded_idx])
        content.piles.put_undrawn_iter(drawn[idx] for idx in back_idxes)


def key(color):
    """
    Make a key location card with specific color.

    Args:
        color (Color): The specific color.

    Returns:
        Card: A key location card.
    """
    return _KeyLocation(color)
