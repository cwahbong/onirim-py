import sys

from onirim import card


class Agent:

    def phase_1_action(self, content):
        raise NotImplementedError

    def open_door(self, content, door_card):
        raise NotImplementedError

    def nightmare_action(self, content):
        raise NotImplementedError

    def obtain_door(self, content):
        pass

    def on_lose(self):
        pass

    def on_win(self):
        pass


class File(Agent):

    def __init__(self, in_file, out_file):
        super().__init__()
        self._in_file = in_file
        self._out_file = out_file

    def _input(self):
        """Get tripped input line."""
        line = self._in_file.readline()
        return line.strip() if line else None

    def _print(self, string):
        """Print string in a line."""
        self._out_file.write("{}\n".format(string))

    def _select(self, message, items):
        self._print(message)
        for idx, item in enumerate(items):
            self._print("[{}] {}".format(idx, item))
        try:
            idx = int(self._input())
            return idx
        except ValueError:
            self._print("Not a valid index.")
        except IndexError:
            self._print("Index out of range.")

    def _short_card(self, card):
        if card.kind:
            return "[{} {}]".format(card.color.name[0], card.kind.name[0])
        return "[{}]".format(card.color.name[0])

    def _print_explored(self, content):
        self._print(" ".join(self._short_card(card) for card in content.explored))

    def phase_1_action(self, content):
        self._print_explored(content)
        self._print("decide an action (play/discard)")
        action = self._input()
        is_play = None
        if action == "play":
            is_play = True
        elif action == "discard":
            is_play = False
        else:
            raise ValueError
        idx = self._select("select from hand", content.hand)
        return is_play, idx

    def open_door(self, content, door_card):
        self._print("open this door? (yes/no)")
        yn = self._input()
        if yn == "yes":
            return True
        elif yn == "no":
            return False
        raise ValueError

    def nightmare_action(self, content):
        self._print("choose a way to handle nightmare (key/door/hand/deck)")
        way = self._input()
        if way == "key":
            return card.NightmareAction.by_key, {}
        elif way == "door":
            return card.NightmareAction.by_door, {}
        elif way == "hand":
            return card.NightmareAction.by_hand, {}
        elif way == "deck":
            return card.NightmareAction.by_deck, {}
        raise ValueError

    def obtain_door(self, content):
        self._print("door obtained")

    def on_lose(self):
        self._print("lose")

    def on_win(self):
        self._print("win")


def console():
    """Make a console agent."""
    return File(sys.stdin, sys.stdout)
