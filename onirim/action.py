"""Action classes here.
"""

from onirim import util

class Phase1(util.AutoNumberEnum):
    """Available actions in phase 1."""
    play = ()
    discard = ()


class Nightmare(util.AutoNumberEnum):
    """Available actions resolving nightmare."""
    by_key = ()
    by_door = ()
    by_hand = ()
    by_deck = ()
