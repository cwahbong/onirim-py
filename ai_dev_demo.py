import onirim.agent
import onirim.action
import onirim.card
import onirim.core
import onirim.data
import onirim.tool

import operator

from etaprogress.progress import ProgressBar
from onirim.action import Phase1


def max_index(iterator):
    return max(enumerate(iterator), key=operator.itemgetter(1))[0]


class Evaluator(onirim.agent.Actor):

    phase1_play_actions = [(Phase1.play, idx) for idx in range(5)]
    phase1_discard_actions = [(Phase1.discard, idx) for idx in range(5)]
    phase1_available_actions = phase1_play_actions + phase1_discard_actions

    available_open_door = [False, True]

    def __init__(self, evaluation_func):
        self._evaluate = evaluation_func

    def _after_phase_1_action(self, content, action):
        # TODO
        pass

    def _phase_1_action_scores(self, content):
        for action in self.phase1_available_actions:
            yield self._evaluate(self._after_phase_1_action(content, action))

    def phase_1_action(self, content):
        idx = max_index(self._phase_1_action_scores(content))
        return self.phase1_available_actions[idx]

    def _after_key_discard_react(self, content, cards, react):
        # TODO
        pass

    def _key_discard_react_scores(self, content, cards):
        for react in self.available_key_discard_reacts:
            yield self._evaluate(self._after_key_discard_react(content, cards, react))

    def key_discard_react(self, content, cards):
        idx = max_index(self._key_discard_react_scores(content, cards))
        return self.available_key_discard_react[idx]

    def _after_open_door(self, content, door_card, do_open):
        # TODO
        pass

    def _open_door_scores(self, content, door_card):
        for do_open in self.available_open_door:
            yield self._evaluate(self._after_open_door(content, door_card, do_open))

    def open_door(self, content, door_card):
        idx = max_index(self._open_door_scores(content, door_card))
        return self.available_open_door[idx]

    def _after_nightmare_action(self, content, action):
        # TODO
        pass

    def _nightmare_action_scores(self, content):
        for action in self.available_nightmare_actions:
            yield self._evaluate(self._after_nightmare_action(content, action))

    def nightmare_action(self, content):
        idx = max_index(self._nightmare_action_scores(content))
        return self.available_nightmare_actions[idx]


def evaluate(content):
    return 0


def __main__():
    actor = Evaluator(evaluate)
    observer = onirim.agent.ProfiledObserver()
    content_fac = onirim.data.starting_content
    onirim.tool.progressed_run(1000, actor, observer, content_fac)

    print("{}/{}".format(observer.win, observer.total))
    print("Opened door: {}".format(observer.opened_door))
    print("Opened by keys: {}".format(observer.opened_door_by_key))
    print("Keys discarded: {}".format(observer.key_discarded))
    print(str(observer.opened_distribution))

if __name__ == "__main__":
    __main__()
