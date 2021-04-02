from collections import UserDict
from collections import Counter
from collections import defaultdict
from itertools import combinations
import re

TILE_KIND = ['sou', 'man', 'pin', 'tsu']
TILE_PATTERN = r'(?P<card_id>[1-9]*)(?P<kind>mon|sou|tsu|pin)'


class UnknownKindError(Exception):
    pass


class InvalidOperationError(Exception):
    pass


class Tiles(UserDict):
    def __init__(
            self,
            sou='',  # 索
            man='',  # 萬
            pin='',  # 餅
            tsu=''  # 字
    ):
        super().__init__(
            sou=''.join(sorted(sou)),
            man=''.join(sorted(man)),
            pin=''.join(sorted(pin)),
            tsu=''.join(sorted(tsu))
        )

        self._counter = {
            key: Counter(value)
            for key, value in self.data.items()
        }

    def remove_tile(self, kind, card_id):
        """ Remove ONE card for given kind """

        if kind not in TILE_KIND:
            raise UnknownKindError(f'Unknown kind {kind}')

        remain_cards = self._counter.get(kind)
        if not (card_id in remain_cards and remain_cards[card_id]):
            raise InvalidOperationError(
                f"Can't remove {card_id}{kind} from {self}")
        remain_cards[card_id] -= 1
        self.data[kind].replace(card_id, '', 1)

    @property
    def _combinations(self):
        # card pair like: ('sou', 1)
        card_pairs = [
            (key, v)
            for key, value in self.data.items()
            for v in value
        ]
        all_combinations = set(combinations(card_pairs, 14))
        for combination in all_combinations:
            combination_dict = defaultdict(str)
            # organize all kind to mapping like: 'sou: 1123'
            for kind, card_id in combination:
                combination_dict[kind] += card_id

            # construct cards string
            combination_str = ''
            for kind, value in combination_dict.items():
                combination_str += ''.join(sorted(value))
                combination_str += kind
            yield combination_str

    @property
    def win_combinations(self):
        for combination in self._combinations:
            if self._is_valid_combination(combination):
                yield combination

    def _get_eyes(self, card_count):
        """
        input -> dict: {card id: number of the card}
        output -> list of str: legal eyes
        """
        for key in card_count:
            if card_count[key] >= 2:
                yield key

    def _is_valid_combination(self, combination):
        card_count = {}
        for matched in re.finditer(TILE_PATTERN, combination):
            card_count[matched.group('kind')] = (
                Counter(matched.group('card_id'))
            )
        for kind in TILE_KIND:
            is_other_valid = False
            # First, assuming others kind without eyes
            for other_kind, count in card_count.items():
                if other_kind == kind:
                    continue
                if not self._check_combination_without_eyes(count.copy()):
                    continue
                is_other_valid = True
                break
            if not is_other_valid:
                continue
            # Check remain cards
            count = card_count[kind].copy()
            for eye in self._get_eyes(count):
                count[eye] -= 2
                if self._check_combination_without_eyes(count):
                    return True
        return False

    def _check_combination_without_eyes(self, card_count):
        """
        Check if a card set exclude eyes is legal or not.
        input: -> dict: {card point: number of the card}
        output -> bool: legal or not
        """
        key_list = sorted(list(card_count.keys()))
        # if nothing left in card set, is legal
        if not card_count:
            return True

        # check by recursive
        # remove smallest Triplet
        if card_count[key_list[0]] >= 3:
            tmp = card_count
            tmp[key_list[0]] -= 3
            if tmp[key_list[0]] == 0:
                tmp.pop(key_list[0], None)
            return self._check_combination_without_eyes(tmp)

        # remove smallest Sequence
        elif len(key_list) >= 3 and\
                card_count[key_list[0]] > 0 and\
                card_count[key_list[1]] > 0 and\
                card_count[key_list[2]] > 0 and\
                key_list[1] == str(int(key_list[0])+1) and\
                key_list[2] == str(int(key_list[1])+1):
            tmp = card_count
            tmp[key_list[0]] -= 1
            tmp[key_list[1]] -= 1
            tmp[key_list[2]] -= 1
            for i in range(3):
                if tmp[key_list[i]] == 0:
                    tmp.pop(key_list[i], None)
            return self._check_combination_without_eyes(tmp)
        else:
            return False

    def __str__(self):
        represetation = ''
        for key, value in self.data.items():
            if value:
                represetation += (value + key)
        return represetation
