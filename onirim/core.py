"""Onirim logic."""

from onirim import deck
from onirim import exception


class Content:

    def __init__(self, cards):
        self._deck = deck.Deck(cards)
        self._hand = []
        self._explored = []

    @property
    def deck(self):
        return self._deck

    @property
    def explored(self):
        return self._explored

    @property
    def hand(self):
        return self._hand


class Orinim:

    def __init__(self, cards):
        self._agent = None
        self._content = Content(cards)

    def _phase_1(self):
        """The first phase of a turn."""
        is_play, idx = self._agent.phase_1_action(self._content)
        card = self._content.hand[idx]
        if is_play:
            card.play()
        else:
            card.discard()

    def _phase_2(self):
        """The second phase of a turn."""
        while len(self._content.hand) < 5:
            card = self._content.deck.draw()[0]
            card.drawn()

    def _phase_3(self):
        """The third phase of a turn."""
        self._content.deck.shuffle_with_limbo()

    def run(self):
        """Run an Onirim and return the result."""
        try:
            while True:
                self._phase_1()
                self._phase_2()
                self._phase_3()
        except exception.Win:
            return True
        except exception.Lose:
            return False
        except exception.Onirim:
            return None
