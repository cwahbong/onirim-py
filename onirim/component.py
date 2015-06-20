import random

from onirim import exception


class NoUndrawnCardException(exception.Onirim):
    """
    Indicates that there is no undrawn card.
    """
    pass


class Piles:
    """
    Manages three piles: undrawn pile, discarded pile, and limbo pile.
    """

    def __init__(self, undrawn_cards, discarded=None, limbo=None):
        self._undrawn = list(undrawn_cards)
        self._discarded = [] if discarded is None else list(discarded)
        self._limbo = [] if limbo is None else list(limbo)

    def __eq__(self, other):
        return all((
            self._undrawn == other.undrawn,
            self._discarded == other.discarded,
            self._limbo == other.limbo,
            ))

    def __repr__(self):
        return """Piles{{undrawn: {}, discarded: {}, limbo: {}}}""".format(
            self._undrawn, self._discarded, self._limbo)

    @property
    def undrawn(self):
        return self._undrawn

    @property
    def discarded(self):
        return self._discarded

    @property
    def limbo(self):
        return self._limbo

    def pull_door(self, color):
        """
        Pull out a door card from undrawn pile with specific color.

        Args:
            color (onirim.card.Color): The color of door.
        """
        for card in self._undrawn:
            # XXX door does not has a kind now
            #     the only Non-kind card that has a color is a door.
            if card.kind == None and card.color == color:
                self._undrawn.remove(card)
                return card
        return None

    def draw(self, num=1):
        """
        Draw cards from undrawn pile.

        Args:
            num (int): The number of cards to draw.

        Returns:
            A list of cards drawn.

        Raises:
            CardNotEnoughException: If there is no enough card to draw.
            ValueError: If the number of cards to draw is negative.
        """
        if num > len(self._undrawn):
            raise NoUndrawnCardException
        if num < 0:
            raise ValueError("Negative card number.")
        drawn, self._undrawn = self._undrawn[:num], self._undrawn[num:]
        return drawn

    def put_discard(self, card):
        """
        Put a card to discard pile.

        Args:
            card (onirim.card.Card): The card to discard.
        """
        self._discarded.append(card)

    def put_limbo(self, card):
        """
        Put a card to Limbo pile.

        Args:
            card (onirim.card.Card): The card to discard.
        """
        self._limbo.append(card)

    def shuffle_undrawn(self):
        """
        Shuffle the undrawn pile.
        """
        random.shuffle(self._undrawn)

    def shuffle_limbo_to_undrawn(self):
        """
        Shuffle limbo pile back to undrawn pile.
        """
        self._undrawn += self._limbo
        self._limbo = []
        random.shuffle(self._undrawn)


class Content:

    def __init__(self, undrawn_cards, discarded=None, limbo=None, hand=None, explored=None, opened=None):
        self._piles = Piles(undrawn_cards, discarded, limbo)
        self._hand = [] if hand is None else hand
        self._explored = [] if explored is None else explored
        self._opened = [] if opened is None else opened

    def __eq__(self, other):
        return all((
            self._piles == other.piles,
            self._hand == other.hand,
            self._explored == other.explored,
            self._opened == other.opened,
            ))

    def __repr__(self):
        return """Content{{piles: {}, hand: {}, explored: {},opened: {}}}""".format(
            self._piles, self._hand, self._explored, self._opened)

    @property
    def piles(self):
        return self._piles

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
        card = content.piles.draw()[0]
        if card.kind is None:
            content.piles.put_limbo(card)
        else:
            content.hand.append(card)
