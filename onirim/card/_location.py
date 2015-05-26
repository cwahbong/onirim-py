from onirim.card._base import ColorCard

class _Location(ColorCard):

    def drawn(self, agent, content):
        content.add_hand(self)

    def play(self, agent, content):
        if content.explored[-1].kind != self.kind:
            content.explored.append(self)
            content.hand.discard(self)
            agent.notify("card played")
            if False: # Three cards with same color
                pass
        else:
            raise Onirim()

def sun(color):
    pass

def moon(color):
    pass

def key(color):
    pass
