from onirim.card._base import ColorCard
from onirim.card._location import LocationKind


def _openable(door_card, card):
    """Check if the door can be opened by another card."""
    return card.kind == LocationKind.key and door_card.color == card.color

def _may_open(door_card, content):
    """Check if the door may be opened by agent."""
    return any(_openable(door_card, card) for card in content.hand())


class _Door(ColorCard):

    def drawn(self, agent, content):
        do_open = agent.ask("if open") if _may_open(self, content) else False
        if do_open:
            content.discard(self)
        else:
            content.limbo(self)


def door(color):
    """Make a door card."""
    return _Door(color)
