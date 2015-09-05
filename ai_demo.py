import onirim.agent
import onirim.action
import onirim.card
import onirim.core
import onirim.data
import onirim.tool

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
        self.hand_card = card_counter(content.hand)
        self.hand_color = color_counter(content.hand)
        self.opened_color = color_counter(content.opened)

    def nightmare_key_score(self, key_card):
        if key_card.kind != onirim.card.LocationKind.key:
            return 0
        return 1 + self.opened_color[key_card.color]

    def discard_score(self, card):
        if onirim.card.is_nightmare(card):
            return self.nightmare_score

    def nondiscard_score(self, card):
        undrawn_count = self.undrawn_card[card]
        hand_count = self.hand_card[card]
        return [undrawn_count + hand_count, 0]


class AIHelper:

    def _choose_nightmare(self, cards):
        for idx, card in enumerate(cards):
            if onirim.card.is_nightmare(card):
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

        nondiscard_scores = [scorer.nondiscard_score(card) for card in cards]
        for idx, card in enumerate(cards):
            if onirim.card.is_door(card):
                nondiscard_scores[idx][0] -= 500
            if scorer.opened_color[card.color] == 1:
                nondiscard_scores[idx][0] *= 2
        if nokey:
            for idx, card in enumerate(cards):
                if card.kind == onirim.card.LocationKind.key:
                    nondiscard_scores[idx][0] -= 10
        return max(enumerate(nondiscard_scores), key=operator.itemgetter(1))[0]

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
        scorer = Scorer(content)
        candidates = []
        for idx, card in enumerate(content.hand):
            if card.kind != last.kind and card.color == last.color:
                candidates.append((idx, scorer.nondiscard_score(card)))
                if card.kind == onirim.card.LocationKind.key:
                    candidates[-1][1][0] -= 5
        if not candidates:
            return None
        return max(candidates, key=operator.itemgetter(1))[0]

    def _play_combo_three_idx(self, content):
        combo = self._combo_count(content)
        if combo > 0:
            combo_idx = self._play_combo_idx(content, 3 - combo)
            if combo_idx is not None:
                return combo_idx

    def _play_multi_idx(self, content, multi_num):
        scorer = Scorer(content)
        hand_color_count = scorer.hand_color
        card_count = card_counter(content.hand)
        door_count = scorer.opened_color

        multi_colors = set()
        for color in onirim.card.Color:
            if hand_color_count[color] >= multi_num and door_count[color] < 2:
                multi_colors.add(color)
        if not multi_colors:
            return None

        # TODO calc the best bridge

        last = onirim.card.nightmare() if not content.explored else content.explored[-1]
        multi_candidates = []
        for idx, card in enumerate(content.hand):
            if hand_color_count[card.color] >= multi_num:
                multi_candidates.append((idx, card))
        multi_kind_count = len(set(card.kind for _, card in multi_candidates))

        if multi_kind_count == multi_num:
            # (1 + 1 + 1) or (1 + 1), sun first if possible
            for idx, card in multi_candidates:
                if last.kind == onirim.card.LocationKind.sun:
                    if card.kind != last.kind:
                        return idx
                elif card.kind == onirim.card.LocationKind.sun:
                    return idx
        elif multi_kind_count == multi_num - 1:
            # DOING 2 + ?
            first_multi_card = None
            for idx, card in multi_candidates:
                if card.kind != last.kind and card_count[card] >= multi_num - 1:
                    return idx
                else:
                    first_multi_card = card
            for idx, card in enumerate(content.hand):
                if card.kind != last.kind and card.kind != first_multi_card.kind:
                    return idx
        else:
            for idx, card in multi_candidates:
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
        scorer = Scorer(content)

        play_idx = self._play_combo_three_idx(content)
        if play_idx is not None:
            return onirim.action.Phase1.play, play_idx

        play_idx = self._play_multi_idx(content, 3)
        if play_idx is not None:
            return onirim.action.Phase1.play, play_idx

        play_idx = self._play_same_color_idx(content)
        if play_idx is not None:
            return onirim.action.Phase1.play, play_idx

        discarded_idx = self._choose_discard(scorer, content.hand)
        return onirim.action.Phase1.discard, discarded_idx


def three_first_phase_1_action(content):
    return AIHelper().phase_1_action(content)


def sun_moon_only_phase_1_action(content):
    pass


def nightmare_first_key_discard_react(content, cards):
    scorer = Scorer(content)

    back = list(range(5))
    discarded_idx = AIHelper()._choose_discard(scorer, cards, nokey=True)
    back.remove(discarded_idx)
    random.shuffle(back)
    return discarded_idx, back


def key_first_nightmare_action(content):
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


def threat_based_nightmare_action(content):
    def nondiscard_sunmoon_min(scorer, color):
        sun = onirim.card.sun(color)
        moon = onirim.card.moon(color)
        return min(scorer.nondiscard_score(sun)[0], scorer.nondiscard_score(moon)[0])

    def key_safe(scorer, card):
        if card.kind != onirim.card.LocationKind.key:
            return False
        key_score = scorer.nondiscard_score(card)[0]
        sunmoon_score = nondiscard_sunmoon_min(scorer, card.color) / 1.5
        score = key_score + sunmoon_score
        return score >= 2 - scorer.opened_color[card.color]

    def door_safe(scorer, card):
        assert onirim.card.is_door(card)
        key = onirim.card.key(card.color)
        key_score = scorer.nondiscard_score(key)[0]
        sunmoon_score = nondiscard_sunmoon_min(scorer, card.color) / 1.5
        nonopened_becomes = 2 - scorer.opened_color[card.color] + 1
        return key_score + sunmoon_score > nonopened_becomes

    def door_easy(scorer, door):
        color = door.color
        key = onirim.card.key(color)
        key_score = scorer.nondiscard_score(key)[0]
        sunmoon_score = nondiscard_sunmoon_min(scorer, color) / 1.5
        nonopened = scorer.opened_color[color] + 1
        return (key_score + sunmoon_score) / nonopened

    if all(card.kind != onirim.card.LocationKind.key for card in content.hand):
        return onirim.action.Nightmare.by_hand, {}

    scorer = Scorer(content)

    for idx, card in enumerate(content.hand):
        if key_safe(scorer, card):
            return onirim.action.Nightmare.by_key, {"idx": idx}

    for idx, door in enumerate(content.opened):
        if door_safe(scorer, door):
            return onirim.action.Nightmare.by_door, {"idx": idx}

    if content.opened:
        door_easies = [door_easy(scorer, door) for door in content.opened]
        easiest_idx = max(enumerate(door_easies), key=operator.itemgetter(1))[0]
        return onirim.action.Nightmare.by_door, {"idx": easiest_idx}

    return key_first_nightmare_action(content)


class Actor:

    def phase_1_action(self, *args, **kwargs):
        return three_first_phase_1_action(*args, **kwargs)

    def key_discard_react(self, *args, **kwargs):
        return nightmare_first_key_discard_react(*args, **kwargs)

    def open_door(self, *args, **kwargs):
        return True

    def nightmare_action(self, *args, **kwargs):
        return threat_based_nightmare_action(*args, **kwargs)


def __main__():
    actor = Actor()
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
