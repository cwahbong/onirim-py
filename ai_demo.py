import onirim.agent
import onirim.action
import onirim.card
import onirim.core
import onirim.data

import collections
import operator
import random


def default_int_counter(iterator):
    return collections.defaultdict(int, collections.Counter(iterator))

def card_counter(cards):
    return default_int_counter(card for card in cards)

def kind_counter(cards):
    return default_int_counter(card.kind for card in cards)

def color_counter(cards):
    return default_int_counter(card.color for card in cards)


class Scorer:

    nightmare_score = 100000

    def __init__(self, content):
        self.undrawn_card = card_counter(content.piles.undrawn)
        self.undrawn_color = color_counter(content.piles.undrawn)
        self.hand_color = color_counter(content.hand)
        self.opened_color = color_counter(content.opened)

    def nightmare_key_score(self, key_card):
        if key_card.kind != onirim.card.LocationKind.key:
            return 0
        return 1 + self.opened_color[key_card.color]

    def discard_score(self, card):
        if card.color is None and card.kind is None:
            return self.nightmare_score

    def undrawn_score(self, card):
        color_undrawn_count = self.undrawn_color[card.color]
        undrawn_count = self.undrawn_card[card]
        return [undrawn_count, color_undrawn_count]


class AIAgent(onirim.agent.Agent):

    key_discarded = 0

    opened = 0
    opened_distribution = collections.defaultdict(int)

    def _choose_nightmare(self, cards):
        for idx, card in enumerate(cards):
            if card.kind is None and card.color is None:
                return idx
        return None

    def _choose_fullfilled_color(self, scorer, cards):
        nonkey = [onirim.card.LocationKind.sun, onirim.card.LocationKind.moon]
        for idx, card in enumerate(cards):
            if card.kind in nonkey and scorer.opened_color[card.color] == 2:
                return idx
        return None

    def _choose_discard(self, scorer, cards, nokey=False):
        nightmare_idx = self._choose_nightmare(cards)
        if nightmare_idx is not None:
            return nightmare_idx

        fullfilled_color_idx = self._choose_fullfilled_color(scorer, cards)
        if fullfilled_color_idx is not None:
            return fullfilled_color_idx

        undrawn_scores = [scorer.undrawn_score(card) for card in cards]
        for idx, card in enumerate(cards):
            if card.kind is None:
                undrawn_scores[idx][0] -= 500
            if scorer.opened_color[card.color] == 1:
                undrawn_scores[idx][0] *= 2
        if nokey:
            for idx, card in enumerate(cards):
                if card.kind == onirim.card.LocationKind.key:
                    undrawn_scores[idx][0] -= 10
        return max(enumerate(undrawn_scores), key=operator.itemgetter(1))[0]

    def _combo_count(self, content):
        if not content.explored:
            return 0
        last = content.explored[-1]
        same_count = 0
        for card in reversed(content.explored):
            if last.color == card.color:
                same_count += 1
            else:
                break
        return same_count % 3

    def _play_combo_idx(self, content, need):
        assert 0 < need < 3
        last = content.explored[-1]
        same_color_kind_count = len(set(card.kind for card in content.hand if
            card.color == last.color))
        if same_color_kind_count < need:
            return None
        for idx, card in enumerate(content.hand):
            # TODO sun first, then moon, then key
            if card.kind != last.kind and card.color == last.color:
                return idx

    def _play_combo_three_idx(self, content):
        combo = self._combo_count(content)
        if combo > 0:
            combo_idx = self._play_combo_idx(content, 3 - combo)
            if combo_idx is not None:
                return combo_idx

    def _play_three_idx(self, content):
        scorer = Scorer(content)
        hand_color_count = scorer.hand_color
        max_hand_color_count = max(hand_color_count.values())
        card_count = card_counter(content.hand)
        door_count = scorer.opened_color

        for color in onirim.card.Color:
            if hand_color_count[color] >= 3 and door_count[color] == 2:
                return None

        # TODO calc the best bridge

        last = onirim.card.nightmare() if not content.explored else content.explored[-1]
        three_candidates = []
        for idx, card in enumerate(content.hand):
            if hand_color_count[card.color] >= 3:
                three_candidates.append((idx, card))
        three_kind_count = len(set(card.kind for _, card in three_candidates))

        if three_kind_count == 3:
            # TODO 1 + 1 + 1
            for idx, card in three_candidates:
                if card.kind != last.kind:
                    return idx
        elif three_kind_count == 2:
            # DOING 2 + ?
            first_three_card = None
            for idx, card in three_candidates:
                if card.kind != last.kind and card_count[card] >= 2:
                    return idx
                else:
                    first_three_card = card
            for idx, card in enumerate(content.hand):
                if card.kind != last.kind and card.kind != first_three_card.kind:
                    return idx
        else:
            for idx, card in three_candidates:
                if card.kind != last.kind:
                    return idx
        return None

    def _play_same_color_idx(self, content):
        if not content.explored:
            return 0

        scorer = Scorer(content)
        door_counter = scorer.opened_color

        last = content.explored[-1]
        for idx, card in enumerate(content.hand):
            if (card.kind != last.kind and
                    card.color == last.color and
                    door_counter[card.color] < 2):
                return idx

    def phase_1_action(self, content):
        play_idx = self._play_combo_three_idx(content)
        if play_idx is not None:
            return onirim.action.Phase1.play, play_idx

        play_idx = self._play_three_idx(content)
        if play_idx is not None:
            return onirim.action.Phase1.play, play_idx

        play_idx = self._play_same_color_idx(content)
        if play_idx is not None:
            return onirim.action.Phase1.play, play_idx

        scorer = Scorer(content)
        discarded_idx = self._choose_discard(scorer, content.hand)
        return onirim.action.Phase1.discard, discarded_idx

    def key_discard_react(self, content, cards):
        AIAgent.key_discarded += 1
        back = list(range(5))
        scorer = Scorer(content)
        discarded_idx = self._choose_discard(scorer, cards, nokey=True)
        back.remove(discarded_idx)
        random.shuffle(back)
        return discarded_idx, back

    def open_door(self, content, door_card):
        return True

    def nightmare_action(self, content):
        if not content.hand:
            return onirim.action.Nightmare.by_hand, {}

        scorer = Scorer(content)

        # use key with most doors.
        key_scores = [scorer.nightmare_key_score(card) for card in content.hand]
        max_key_score = max(key_scores)
        if max_key_score > 0:
            for idx, score in enumerate(key_scores):
                if score == max_key_score:
                    return onirim.action.Nightmare.by_key, {"idx": idx}

        return onirim.action.Nightmare.by_hand, {}

    @classmethod
    def _update_result(cls, content):
        cls.opened += len(content.opened)
        cls.opened_distribution[len(content.opened)] += 1

    def on_win(self, content):
        assert len(content.opened) == 8
        self._update_result(content)

    def on_lose(self, content):
        self._update_result(content)


def __main__():
    win, total = 0, 0
    for _ in range(1000):
        total += 1
        win += onirim.core.run(AIAgent(), onirim.data.starting_content())
    print("{}/{}".format(win, total))
    print(AIAgent.opened, AIAgent.key_discarded)

if __name__ == "__main__":
    __main__()
print(str(AIAgent.opened_distribution))
