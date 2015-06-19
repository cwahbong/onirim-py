"""Onirim logic."""

from onirim import exception
from onirim import agent
from onirim import component


class Onirim:

    def __init__(self, cards):
        self._agent = agent.console()
        self._content = component.Content(cards)

    def _setup(self):
        """Prepare the initial hand."""
        self._content.deck.shuffle()
        component.replenish_hand(self._content)
        self._content.deck.shuffle_with_limbo()

    def _phase_1(self):
        """The first phase of a turn."""
        is_play, idx = self._agent.phase_1_action(self._content)
        card = self._content.hand[idx]
        if is_play:
            card.play(self._agent, self._content)
        else:
            card.discard(self._agent, self._content)

    def _phase_2(self):
        """The second phase of a turn."""
        while len(self._content.hand) < 5:
            try:
                card = self._content.deck.draw()[0]
                card.drawn(self._agent, self._content)
            except ValueError:
                raise exception.Lose

    def _phase_3(self):
        """The third phase of a turn."""
        self._content.deck.shuffle_with_limbo()

    def run(self):
        """Run an Onirim and return the result."""
        try:
            self._setup()
            while True:
                self._phase_1()
                self._phase_2()
                self._phase_3()
        except exception.Win:
            self._agent.on_win()
            return True
        except exception.Lose:
            self._agent.on_lose()
            return False
        except exception.Onirim:
            print("other errors")
            return None
