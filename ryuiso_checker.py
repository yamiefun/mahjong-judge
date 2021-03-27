from collections import defaultdict
from judge import judge_ryuiso
from itertools import combinations


class RyuisoChecker:
    def __init__(self):
        self._init_pool = {'2': 4, '3': 4, '4': 4, '6': 4, '8': 4, 'f': 4}
        self._pool = self._init_pool.copy()

    def parse_input(self, val):
        self._update_pool(val)
        ret = self._find_possibility()
        if ret:
            print("Still possible to Ryuiso.")
            print("Ex: ", ret)
        else:
            print("Not enough for Ryuiso.")

    def _update_pool(self, val):
        if val == 'reset':
            self._pool = self._init_pool.copy()
        elif val in self._init_pool:
            self._pool[val] -= 1
            if self._pool[val] < 0:
                self._pool[val] = 0
                print("Error: illegal input, card number greater than 4.")
            elif self._pool[val] == 0:
                self._pool.pop(val)
        print(self._pool)

    def _find_possibility(self):
        pool_list = []
        for key in self._pool:
            for i in range(self._pool[key]):
                pool_list.append(key)
        comb = combinations(pool_list, 14)
        for c in comb:
            tmp = "".join(c)
            if judge_ryuiso(tmp):
                return tmp
        else:
            return ""
