import random


class Deck:
    """A deck."""

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
            raise NoCardException
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


class Content:

    def __init__(self, cards):
        self._deck = Deck(cards)
        self._hand = []
        self._explored = []
        self._opened = []

    @property
    def deck(self):
        return self._deck

    @property
    def explored(self):
        return self._explored

    @property
    def opened(self):
        return self._opened

    @property
    def hand(self):
        return self._hand


def replenish_hand(content):
    while len(content.hand) < 5:
        card = content.deck.draw()[0]
        if card.kind is None:
            content.deck.put_limbo(card)
        else:
            content.hand.append(card)
