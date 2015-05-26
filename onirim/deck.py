import random

class Deck:

    def __init__(self, cards):
        self._undrawn = list(cards)
        self._discarded = []
        self._limbo = []

    def draw(self, n=1):
        """Draw n cards."""
        if n > len(self._undrawn) or n < 0:
            raise ValueError()
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
