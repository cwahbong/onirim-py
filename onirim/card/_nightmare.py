from onirim.card._base import Card
from onirim.card._location import LocationKind
from onirim import action
from onirim import core


def _by_key(content, **kwargs):
    """Nightmare card resolved by key."""
    if len(kwargs) != 1:
        raise ValueError
    idx = kwargs["idx"]
    card = content.hand[idx]
    if card.kind != LocationKind.key:
        raise ValueError("Not a key")
    content.hand.remove(card)
    content.deck.put_discard(card)


def _by_door(content, **kwargs):
    """Nightmare card resolved by door."""
    if len(kwargs) != 1:
        raise ValueError
    idx = kwargs["idx"]
    card = content.opened[idx]
    content.opened.remove(card)
    content.deck.put_limbo(card)


def _by_hand(content, **kwargs):
    """Nightmare card resolved by hand."""
    if kwargs:
        raise ValueError
    for card in content.hand:
        content.deck.put_discard(card)
    content.hand.clear()
    core.replenish_hand(content)


def _by_deck(content, **kwargs):
    """Nightmare card resolved by deck."""
    if kwargs:
        raise ValueError
    for card in content.deck.draw(5):
        if card.kind is None:
            content.deck.put_limbo(card)
        else:
            content.deck.put_discard(card)


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
