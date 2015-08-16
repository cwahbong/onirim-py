"""Onirim logic."""

from onirim import action
from onirim import component
from onirim import exception


class Core:
    def __init__(self, actor, observer, content):
        self._actor = actor
        self._observer = observer
        self._content = content

    @property
    def actor(self):
        return self._actor

    @property
    def observer(self):
        return self._observer

    @property
    def content(self):
        return self._content


class Flow:

    def __init__(self, core):
        self._core = core

    def setup(self):
        """Prepare the initial hand."""
        self._core.content.piles.shuffle_undrawn()
        component.replenish_hand(self._core.content)
        self._core.content.piles.shuffle_limbo_to_undrawn()

    def phase_1(self):
        """The first phase of a turn."""
        phase_1_action, idx = self._core.actor.phase_1_action(self._core.content)
        card = self._core.content.hand[idx]
        card_on = {
            action.Phase1.play: card.play,
            action.Phase1.discard: card.discard,
            }
        self._core.observer.on_phase_1_action(self._core.content, phase_1_action, idx)
        card_on[phase_1_action](self._core)

    def phase_2(self):
        """The second phase of a turn."""
        while len(self._core.content.hand) < 5:
            card = self._core.content.piles.draw()[0]
            card.drawn(self._core)

    def phase_3(self):
        """The third phase of a turn."""
        self._core.content.piles.shuffle_limbo_to_undrawn()

    def whole(self):
        """Run an Onirim and return the result."""
        try:
            self.setup()
            while True:
                self.phase_1()
                self.phase_2()
                self.phase_3()
        except exception.Win:
            self._core.observer.on_win(self._core.content)
            return True
        except component.CardNotEnoughException:
            self._core.observer.on_lose(self._core.content)
            return False
        except exception.Onirim as exp:
            print("other errors: {}", exp)
            return None


def run(actor, observer, content):
    return Flow(Core(actor, observer, content)).whole()
