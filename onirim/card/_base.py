import onirim.color

class Card:
    @property
    def color(self):
        return None

    @property
    def kind(self):
        return None


class ColorCard(Card):

    def __init__(self, color):
        if not isinstance(color, onirim.color.Color):
            raise ValueError()
        self._color = color

    @property
    def color(self):
        return self._color
