from onirim.card._base import ColorCard

class _Door(ColorCard):

    def drawn(self, agent, content):
        do_open = agent.ask("if open") if content.can_open(self) else False
        if do_open:
            content.discard(self)
        else:
            content.limbo(self)

def door(color):
    return _Door(color)
