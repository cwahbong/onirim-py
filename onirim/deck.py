import random

from onirim.card import LocationKind

class Deck:

    def __init__(self, cards):
        self._undrawn = list(cards)
        self._discarded = []
        self._limbo = []

    def pull_door(self, color):
        """Pull out a door card by color."""
        for card in self._undrawn:
            # XXX door does not has a kind now
            #     the only Non-kind card that has a color is a door.
            if card.kind == None and card.color == color:
                self._undrawn.remove(card)
                return card
        return None

    def draw(self, n=1):
        """Draw n cards."""
        if n > len(self._undrawn):
            raise ValueError("Card is not enough.")
        if n < 0:
            raise ValueError("Negative card number.")
        drawn, self._undrawn = self._undrawn[:n], self._undrawn[n:]
        return drawn

    def put_discard(self, card):
        """Put a card to discard pile."""
        self._discarded.append(card)

    def put_limbo(self, card):
        """Put a card to Limbo pile."""
        self._limbo.append(card)

    def shuffle(self):
        """Shuffle the undrawn pile."""
        random.shuffle(self._undrawn)

    def shuffle_with_limbo(self):
        """Shuffle limbo pile back to undrawn pile."""
        self._undrawn += self._limbo
        self._limbo = []
        random.shuffle(self._undrawn)
