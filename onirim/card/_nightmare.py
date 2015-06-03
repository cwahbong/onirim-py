from onirim.card._base import Card
from onirim import util

class NightmareAction(util.AutoNumberEnum):
    """Available actions resolving nightmare."""
    by_key = ()
    by_door = ()
    by_hand = ()
    by_deck = ()


def _by_key(content, **kwargs):
    print("by key not handled")


def _by_door(content, **kwargs):
    print("by door not handled")


def _by_hand(content, **kwargs):
    print("by hand not handled")


def _by_deck(content, **kwargs):
    print("by deck not handled")


_resolve = {
    NightmareAction.by_key: _by_key,
    NightmareAction.by_door: _by_door,
    NightmareAction.by_hand: _by_hand,
    NightmareAction.by_deck: _by_deck,
}


class _Nightmare(Card):

    def drawn(self, agent, content):
        action, additional = agent.nightmare_action(content)
        _resolve[action](content, **additional)
        content.deck.put_discard(self)


def nightmare():
    """Make a nightmare card."""
    return _Nightmare()
