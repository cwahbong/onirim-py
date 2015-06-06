from onirim.card._base import Card
from onirim import action


def _by_key(content, **kwargs):
    print("by key not handled")


def _by_door(content, **kwargs):
    print("by door not handled")


def _by_hand(content, **kwargs):
    print("by hand not handled")


def _by_deck(content, **kwargs):
    print("by deck not handled")


_resolve = {
    action.Nightmare.by_key: _by_key,
    action.Nightmare.by_door: _by_door,
    action.Nightmare.by_hand: _by_hand,
    action.Nightmare.by_deck: _by_deck,
}


class _Nightmare(Card):

    def drawn(self, agent, content):
        action, additional = agent.nightmare_action(content)
        _resolve[action](content, **additional)
        content.deck.put_discard(self)


def nightmare():
    """Make a nightmare card."""
    return _Nightmare()
