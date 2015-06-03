import sys

from onirim import card


class Agent:

    def phase_1_action(self, content):
        pass

    def open_door(self, content, door_card):
        pass

    def nightmare_action(self, content):
        raise NotImplementedError

    def on_lose(self):
        pass

    def on_win(self):
        pass


class File(Agent):

    def __init__(self, in_file, out_file):
        super().__init__()
        self._in_file = in_file
        self._out_file = out_file

    def phase_1_action(self, content):
        print("decide a action (play/discard)")
        return False, 0

    def nightmare_action(self, content):
        return card.NightmareAction.by_key, {}

    def on_lose(self):
        print("lose")

    def on_win(self):
        print("win")


def console():
    """Make a console agent."""
    return File(sys.stdin, sys.stdout)
