import re
from collections import Counter
from operator import attrgetter

class Hand:
    # card_map = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10, 'J': 11, 'Q': 12, 'K': 13, 'A': 14}
    card_map = {'2': 'a', '3': 'b', '4': 'c', '5': 'd', '6': 'e', '7': 'f',
                '8': 'g', '9': 'h', 'T': 'i', 'J': 'j', 'Q': 'k', 'K': 'l', 'A': 'm'}

    type_map = {
        'high-card': 'a',
        'pair': 'b',
        'two-pair': 'c',
        'three-of-a-kind': 'd',
        'full-house': 'e',
        'four-of-a-kind': 'f',
        'five-of-a-kind': 'g'
    }

    def __init__(self, cards, bid=0):
        self.cards = cards
        self.card_vals, self.card_vals_wild = self._get_card_vals()
        self.bid = int(bid)
        self.hand_type = self._find_type()
        self.score = self._calculate_score()
        self.cards_wild = self.update_wilds()
        self.hand_type_wild = self._find_type(wild=True)
        self.score_wild = self._calculate_score(wild=True)

    def _get_card_vals(self):
        card_vals = ''.join([self.card_map.get(card) for card in self.cards])
        card_vals_wild = card_vals.replace('j', '0')
        return card_vals, card_vals_wild

    def _find_type(self, wild=False):
        if wild:
            counts = Counter(list(self.cards_wild))
        else:
            counts = Counter(list(self.cards))
        count_max = max(counts.values())
        count_len = len(counts.values())
        if count_max == 5:
            hand_type = 'five-of-a-kind'
        elif count_max == 4:
            hand_type = 'four-of-a-kind'
        elif count_max == 3:
            if count_len == 2:
                hand_type = 'full-house'
            else:
                hand_type = 'three-of-a-kind'
        elif count_max == 2:
            if count_len == 3:
                hand_type = 'two-pair'
            else:
                hand_type = 'pair'
        elif count_max == 1:
            hand_type = 'high-card'
        return hand_type

    def card_from_val(self, val):
        key_list = list(self.card_map.keys())
        val_list = list(self.card_map.values())
        position = val_list.index(val)
        return key_list[position]


    def _calculate_score(self, wild=False):
        if wild:
            score = self.type_map.get(self.hand_type_wild) + self.card_vals_wild
        else:
            score = self.type_map.get(self.hand_type) + self.card_vals
        return score

    def update_wilds(self):
        if 'J' in self.cards:
            J_val = self.card_map.get("J")
            card_vals_without_wilds = self.card_vals.replace(J_val,'')
            counts = Counter(card_vals_without_wilds)
            most_common = [k for k,v in counts.items() if v == max(counts.values())]
            if len(most_common) > 0:
                best_char_val = max(most_common)
            else:
                best_char_val = self.card_map.get("A")
            best_card = self.card_from_val(best_char_val)
            self.cards_wild = self.cards.replace("J", best_card)
        else:
            self.cards_wild = self.cards
        return self.cards_wild


with open('input07.txt') as f:
    lines = f.read().splitlines()
hands = []
for line in lines:
    cards, bid = re.findall(r"(\w+)", line)
    hands.append(Hand(cards, bid))

hands.sort(key=attrgetter('score'))

running_winnings = 0
for i, hand in enumerate(hands):
    running_winnings += (i+1) * hand.bid

print('Part 1 Winnings: ', running_winnings)


# Part 2

running_winnings = 0
hands.sort(key=attrgetter('score_wild'))
for i, hand in enumerate(hands):
    running_winnings += (i+1) * hand.bid

print('Part 2 Winnings: ', running_winnings)





