import sys

from onirim import action


class Agent:

    def phase_1_action(self, content):
        raise NotImplementedError

    def key_discard_react(self, content, cards):
        raise NotImplementedError

    def open_door(self, content, door_card):
        raise NotImplementedError

    def nightmare_action(self, content):
        raise NotImplementedError

    def obtain_door(self, content):
        pass

    def on_lose(self, content):
        pass

    def on_win(self, content):
        pass


class File(Agent):

    _yesno_dict = {
        "yes": True,
        "no": False
        }

    _phase1_dict = {
        "play": action.Phase1.play,
        "discard": action.Phase1.discard
        }

    _nightmare_dict = {
        "key": action.Nightmare.by_key,
        "door": action.Nightmare.by_door,
        "hand": action.Nightmare.by_hand,
        "deck": action.Nightmare.by_deck
        }

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

    def _print_hand(self, content):
        """Print all cards in hand."""
        self._print("--- Hand ---")
        self._print(" ".join(self._short_card(card) for card in content.hand))

    def _print_opened(self, content):
        """Print all opened doors."""
        self._print("--- Opened ---")
        self._print(" ".join(self._short_card(card) for card in content.opened))

    def _print_explored(self, content):
        """Print all explored locations."""
        self._print("--- Explored ---")
        self._print(" ".join(self._short_card(card) for card in content.explored))

    def phase_1_action(self, content):
        self._print_explored(content)
        self._print_opened(content)
        self._print_hand(content)
        self._print("decide an action (play/discard)")
        action_input = self._input()
        phase1 = self._phase1_dict[action_input]
        idx = self._select("select from hand", content.hand)
        return phase1, idx

    def key_discard_react(self, content, cards):
        # TODO
        raise NotImplementedError

    def open_door(self, content, door_card):
        self._print("open this door? (yes/no)")
        yesno_input = self._input()
        return self._yesno_dict[yesno_input]

    def nightmare_action(self, content):
        self._print("choose a way to handle nightmare (key/door/hand/deck)")
        way_input = self._input()
        way = self._nightmare_dict[way_input]
        if way == action.Nightmare.by_door:
            idx = self._select("select a door", content.opened)
            return way, {"idx": idx}
        elif way == action.Nightmare.by_key:
            idx = self._select("select a key from hand", content.hand)
            return way, {"idx": idx}
        return way, {}

    def obtain_door(self, content):
        self._print("door obtained")

    def on_lose(self):
        self._print("lose")

    def on_win(self):
        self._print("win")


def console():
    """Make a console agent."""
    return File(sys.stdin, sys.stdout)
