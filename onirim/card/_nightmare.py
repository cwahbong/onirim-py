from onirim.card._base import Card

class _Nightmare(Card):

    def drawn(self, agent, content):
        # TODO must choose 1 of 4 effect.
        content.discard(self)


def nightmare():
    return _Nightmare()
