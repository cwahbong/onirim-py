import onirim.agent
import onirim.action
import onirim.card
import onirim.data
import onirim.tool

import collections
import concurrent.futures
import itertools
import logging
import math
import operator
import statistics


def max_index(iterator):
    return max(enumerate(iterator), key=operator.itemgetter(1))[0]


def _can_obtain_door(content):
    """
    Check if the explored cards can obtain a door.
    """
    last_card = content.explored[-1]
    same_count = 0
    for card in reversed(content.explored):
        if last_card.color == card.color:
            same_count += 1
        else:
            break
    return same_count % 3 == 0


def _is_openable(door_card, card):
    """Check if the door can be opened by another card."""
    return card.kind == onirim.card.LocationKind.key and door_card.color == card.color


def back_idxes(idx):
    return list(range(idx)) + list(range(idx + 1, 5))


class Evaluator(onirim.agent.Actor):

    phase1_available_actions = list(itertools.chain(
        ((onirim.action.Phase1.play, idx) for idx in range(5)),
        ((onirim.action.Phase1.discard, idx) for idx in range(5))))

    available_key_discard_react = [(idx, back_idxes(idx)) for idx in range(5)]

    available_open_door = [False, True]

    available_nightmare_actions = list(itertools.chain(
        ((onirim.action.Nightmare.by_key, {"idx": idx}) for idx in range(5)),
        ((onirim.action.Nightmare.by_door, {"idx": idx}) for idx in range(8)),
        [
            (onirim.action.Nightmare.by_hand, {}),
            (onirim.action.Nightmare.by_deck, {})]))

    def __init__(self, evaluation_func):
        self._evaluate = evaluation_func

    def _after_phase_1_action(self, content, action):
        new_content = content.copy()
        phase_1_action, idx = action
        card = new_content.hand[idx]
        if phase_1_action == onirim.action.Phase1.play:
            if new_content.explored and card.kind == new_content.explored[-1].kind:
                # consecutive same kind
                return None
            new_content.explored.append(card)
            new_content.hand.remove(card)
            if _can_obtain_door(new_content):
                color = new_content.explored[-1].color
                door_card = new_content.piles.pull_door(color)
                if door_card is not None:
                    new_content.opened.append(door_card)
        elif phase_1_action == onirim.action.Phase1.discard:
            new_content.hand.remove(card)
            new_content.piles.put_discard(card)
        return new_content

    def _phase_1_action_scores(self, content):
        for action in self.phase1_available_actions:
            yield self._evaluate(self._after_phase_1_action(content, action))

    def phase_1_action(self, content):
        idx = max_index(self._phase_1_action_scores(content))
        return self.phase1_available_actions[idx]

    def _after_key_discard_react(self, content, cards, react):
        new_content = content.copy()
        discarded_idx, back_idxes = react
        new_content.piles.put_discard(cards[discarded_idx])
        new_content.piles.put_undrawn_iter(cards[idx] for idx in back_idxes)
        return new_content

    def _key_discard_react_scores(self, content, cards):
        for react in self.available_key_discard_react:
            yield self._evaluate(self._after_key_discard_react(content, cards, react))

    def key_discard_react(self, content, cards):
        idx = max_index(self._key_discard_react_scores(content, cards))
        return self.available_key_discard_react[idx]

    def _after_open_door(self, content, door_card, do_open):
        new_content = content.copy()
        if not do_open:
            new_content.piles.put_limbo(door_card)
            return new_content
        new_content.opened.append(door_card)
        for card in new_content.hand:
            if _is_openable(door_card, card):
                new_content.hand.remove(card)
                new_content.piles.put_discard(card)
                break
        return new_content

    def _open_door_scores(self, content, door_card):
        for do_open in self.available_open_door:
            yield self._evaluate(self._after_open_door(content, door_card, do_open))

    def open_door(self, content, door_card):
        idx = max_index(self._open_door_scores(content, door_card))
        return self.available_open_door[idx]

    def _nightmare_action_by_key(self, content, **additional):
        try:
            idx = additional["idx"]
            card = content.hand[idx]
            if card.kind != onirim.card.LocationKind.key:
                return False
            content.hand.remove(card)
            content.piles.put_discard(card)
        except IndexError:
            return False
        return True

    def _nightmare_action_by_door(self, content, **additional):
        try:
            idx = additional["idx"]
            card = content.opened[idx]
            content.opened.remove(card)
            content.piles.put_limbo(card)
        except IndexError:
            return False
        return True

    def _nightmare_action_by_hand(self, content, **additional):
        for card in content.hand:
            content.piles.put_discard(card)
        content.hand.clear()
        # do not replenish hand or it may trigger the second nightmare
        return True

    def _nightmare_action_by_deck(self, content, **additional):
        return False
        # XXX know the future
        #try:
        #    for card in content.piles.draw(5):
        #        if card.kind is None:
        #            content.piles.put_limbo(card)
        #        else:
        #            content.piles.put_discard(card)
        #    # TODO card not enough is okay??
        #except:
        #    return False
        #return True

    _resolve = {
        onirim.action.Nightmare.by_key: _nightmare_action_by_key,
        onirim.action.Nightmare.by_door: _nightmare_action_by_door,
        onirim.action.Nightmare.by_hand: _nightmare_action_by_hand,
        onirim.action.Nightmare.by_deck: _nightmare_action_by_deck,
    }

    def _after_nightmare_action(self, content, action):
        new_content = content.copy()
        nightmare_action, additional = action
        if not Evaluator._resolve[nightmare_action](self, new_content, **additional):
            return None
        new_content.piles.put_discard(onirim.card.nightmare())
        return new_content

    def _nightmare_action_scores(self, content):
        for action in self.available_nightmare_actions:
            yield self._evaluate(self._after_nightmare_action(content, action))

    def nightmare_action(self, content):
        idx = max_index(self._nightmare_action_scores(content))
        return self.available_nightmare_actions[idx]


def default_int_counter(iterator):
    return collections.defaultdict(int, collections.Counter(iterator))


def card_counter(cards):
    return default_int_counter(card for card in cards)


def kind_counter(cards):
    return default_int_counter(card.kind for card in cards)


def color_counter(cards):
    return default_int_counter(card.color for card in cards)


def combo_count(content):
    """
    Check if the explored cards can obtain a door.
    """
    if not content.explored:
        return 0
    last_card = content.explored[-1]
    same_count = 0
    for card in reversed(content.explored):
        if last_card.color == card.color:
            same_count += 1
        else:
            break
    return same_count % 3


def do_evaluate(content):
    # Invalid game state
    if content is None:
        return -10 ** 20

    score = 0
    known_lose = False

    # Door discarded, but still try its best
    for card in content.piles.discarded:
        if onirim.card.is_door(card) and not known_lose:
            score -= 10 ** 17
            known_lose = True
            break

    if content.explored:
        last_explored = content.explored[-1]
    else:
        last_explored = onirim.card.nightmare()
    last_color = last_explored.color
    opened_color_counter = color_counter(content.opened)
    nondiscard = content.piles.undrawn + content.piles.limbo + content.hand
    nondiscard_card_counter = card_counter(nondiscard)

    hand_combo = combo_count(content)

    # Prevent no card to win, but still try its best
    for color in onirim.card.Color:
        if opened_color_counter[color] == 2:
            continue
        sun_count = nondiscard_card_counter[onirim.card.sun(color)]
        moon_count = nondiscard_card_counter[onirim.card.moon(color)]
        key_count = nondiscard_card_counter[onirim.card.key(color)]
        need_open = 2 - opened_color_counter[color]
        has_combo = 0
        if content.explored and color == content.explored[-1].color:
            has_combo = hand_combo
        if (sun_count + moon_count + has_combo) / 3 + key_count < need_open:
            if not known_lose:
                known_lose = True
                score -= 10 ** 16
        else:
            count_bound = need_open - key_count - has_combo
            if moon_count < count_bound or sun_count < count_bound:
                if not known_lose:
                    known_lose = True
                    score -= 10 ** 16

    for card in nondiscard:
        if onirim.card.is_nightmare(card):
            score -= 10000000
        elif onirim.card.is_door(card):
            score -= 100000

    # for keys
    for color in onirim.card.Color:
        opened_count = opened_color_counter[color]
        key_count = nondiscard_card_counter[onirim.card.key(color)]
        if key_count:
            key_score = (1 - 0.99 ** key_count) / (1 - 0.99) * 10000
            key_score *= 1 + 0.1 * (2 - opened_count)
            score += key_score

    # for three combo

    combo_weight = 2 - opened_color_counter[last_color]
    if combo_weight:
        combo_weight = 1 + 0.1 * combo_weight
    score += hand_combo * 6000 * combo_weight

    color_cards = set(c for c in content.hand if c.color == last_color
                      and c.kind != onirim.card.LocationKind.key)
    max_cont_count = 0
    for card_perm in itertools.permutations(color_cards):
        prev_card = last_explored
        cont_count = 0
        for card in card_perm:
            if card.kind != prev_card.kind:
                cont_count += 1
            else:
                break
            prev_card = card
        max_cont_count = max(max_cont_count, cont_count)
    cont_combo = min(3 - hand_combo, max_cont_count)
    score += cont_combo * 4000 * combo_weight

    # for card discarding
    for color in onirim.card.Color:
        sun_count = nondiscard_card_counter[onirim.card.sun(color)]
        moon_count = nondiscard_card_counter[onirim.card.moon(color)]
        count = min(sun_count, moon_count)
        weight = 2 - opened_color_counter[color]
        score += (1 - 0.9 ** count) / (1 - 0.9) * 500 * weight
        useless_count = max(sun_count, moon_count) - count
        score += (1 - 0.9 ** useless_count) / (1 - 0.9) * 5 * weight
    return score


def evaluate(content):
    try:
        return do_evaluate(content)
    except Exception as e:
        print("ERR", e)


def print_stat(data):
    mean = statistics.mean(data)
    if mean == 0:
        print("mean: 0")
        return
    stdev = statistics.stdev(data, mean)
    sem = stdev / math.sqrt(len(data))
    res_fmt = "mean: {:.2f}, stdev: {:.2f}({:5.2f}%), sem: {:.2f}({:5.2f}%)"
    print(res_fmt.format(mean, stdev, stdev / mean * 100, sem, sem / mean * 100))


def run_group(times, actor, observer, content_fac):
    for _ in range(times):
        onirim.core.run(actor, observer, content_fac())
    return observer


def __main__():
    logging.basicConfig(
        filename="ai_dev_demo.log",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.WARNING)

    group_num = 50
    group_size = 30

    executor = concurrent.futures.ProcessPoolExecutor()
    actor = Evaluator(evaluate)
    content_fac = onirim.data.starting_content
    params = ((group_size, actor, onirim.agent.ProfiledObserver(),
               content_fac) for _ in range(group_num))
    observers = []
    for observer in onirim.tool.progressed(executor.map(run_group, *zip(*params)), group_num):
        observers.append(observer)

    print("{} group(s) with size {}".format(group_num, group_size))

    print("--- Won ratio --- ")
    wons = list(observer.win / group_size for observer in observers)
    print_stat(wons)

    print("--- Opened doors --- ")
    opens = list(observer.opened_door / group_size for observer in observers)
    print_stat(opens)

    print("--- Opened by keys ---")
    by_keys = list(observer.opened_door_by_key / group_size for observer in observers)
    print_stat(by_keys)

    print("--- Key discarded ---")
    keys_discarded = list(observer.key_discarded / group_size for observer in observers)
    print_stat(keys_discarded)

    for door_count in range(8, -1, -1):
        print("--- Open {} doors ratio ---".format(door_count))
        door_count = list(observer.opened_distribution[door_count] / group_size
                          for observer in observers)
        print_stat(door_count)

if __name__ == "__main__":
    __main__()
