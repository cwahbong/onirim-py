"""Onirim logic."""

from onirim import action
from onirim import component
from onirim import exception


def setup(agent, content):
    """Prepare the initial hand."""
    content.piles.shuffle_undrawn()
    component.replenish_hand(content)
    content.piles.shuffle_limbo_to_undrawn()


def phase_1(agent, content):
    """The first phase of a turn."""
    is_play, idx = agent.phase_1_action(content)
    card = content.hand[idx]
    if is_play == action.Phase1.play:
        card.play(agent, content)
    elif is_play == action.Phase1.discard:
        card.discard(agent, content)
    else:
        raise ValueError


def phase_2(agent, content):
    """The second phase of a turn."""
    try:
        while len(content.hand) < 5:
            card = content.piles.draw()[0]
            card.drawn(agent, content)
    except ValueError:
        raise exception.Lose


def phase_3(agent, content):
    """The third phase of a turn."""
    content.piles.shuffle_limbo_to_undrawn()


def run(agent, content):
    """Run an Onirim and return the result."""
    try:
        setup(agent, content)
        while True:
            phase_1(agent, content)
            phase_2(agent, content)
            phase_3(agent, content)
    except exception.Win:
        agent.on_win(content)
        return True
    except component.CardNotEnoughException:
        agent.on_lose(content)
        return False
    except exception.Onirim as e:
        print("other errors: {}", e.message)
        return None
