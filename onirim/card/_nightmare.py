from onirim.card._base import Card

class _Nightmare(Card):

    def drawn(self, agent, content):
        # TODO must choose 1 of 4 effect.
        print("warn! a non-handled night mare")
        content.deck.put_discard(self)


def nightmare():
    return _Nightmare()
