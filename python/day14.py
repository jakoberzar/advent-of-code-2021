from typing import List, Tuple
from collections import Counter

import numpy as np

from day import Day
from parsers import read_file_lines

ALPHA_COUNT = 26
CACHE_IN_IDX = ALPHA_COUNT


class Day14(Day):
    Input = Tuple[List[int], List[str]]

    @property
    def day_name(self) -> str:
        return "14"

    @staticmethod
    def letter_to_int(letter: str) -> int:
        return ord(letter) - ord("A")

    @staticmethod
    def custom_parser(path: str) -> Input:
        lines = read_file_lines(path)
        template = list(lines[0])
        template_nums = [Day14.letter_to_int(c) for c in template]
        rule_table = [-1] * (ALPHA_COUNT * ALPHA_COUNT)
        for line in lines[2:]:
            parts = line.split(" -> ")
            idx = Day14.letter_to_int(parts[0][0]) * ALPHA_COUNT + Day14.letter_to_int(parts[0][1])
            rule_table[idx] = Day14.letter_to_int(parts[1])
        return (template_nums, rule_table)

    def get_parser(self):
        return self.custom_parser

    def do_one_step(self, template: List[int], rules: List[int]) -> List[int]:
        new_template = []

        for idx, el in enumerate(template[:-1]):
            new_template.append(el)
            nxt = template[idx + 1]
            rule_idx = el * ALPHA_COUNT + nxt
            to_insert = rules[rule_idx]
            if to_insert != -1:
                new_template.append(to_insert)

        new_template.append(template[-1])

        return new_template

    def star1(self, input: Input) -> str:
        (template_nums, rule_table) = input

        for _ in range(10):
            template_nums = self.do_one_step(template_nums, rule_table)

        counter = Counter(template_nums)
        freqs = counter.most_common()
        return str(freqs[0][1] - freqs[-1][1])

    # Star 2 efficient way?

    def count_children(
        self, cur: int, nxt: int, level: int, rules: List[int], cache: np.array
    ) -> np.array:

        if level < 0:
            return np.zeros(26, dtype=np.int64)

        vec = cache[cur, nxt, level]
        if vec[CACHE_IN_IDX] == 0:
            rule_idx = cur * ALPHA_COUNT + nxt
            to_insert = rules[rule_idx]
            if to_insert != -1:
                # cur and next are counted by the parent
                # therefore, to_insert will be the parent and we need to count it
                vec[to_insert] += 1
                # add left children
                vec[:-1] += self.count_children(cur, to_insert, level - 1, rules, cache)
                # add right children
                vec[:-1] += self.count_children(to_insert, nxt, level - 1, rules, cache)
            else:
                # zeroes are already in the vec
                pass

            vec[CACHE_IN_IDX] = 1

        return vec[:-1]

    def star2(self, input: Input) -> str:
        (template_nums, rule_table) = input

        cache = np.zeros((26, 26, 40, ALPHA_COUNT + 1), dtype=np.int64)

        for idx, res in enumerate(rule_table):
            cache[idx // ALPHA_COUNT, idx % ALPHA_COUNT, 0, res] = 1
            cache[idx // ALPHA_COUNT, idx % ALPHA_COUNT, 0, CACHE_IN_IDX] = 1

        sum_vec = np.zeros(ALPHA_COUNT, dtype=np.int64)
        for idx, el in enumerate(template_nums[:-1]):
            nxt = template_nums[idx + 1]
            sum_vec += self.count_children(el, nxt, 39, rule_table, cache)
            sum_vec[el] += 1
        sum_vec[template_nums[-1]] += 1
        non_zero = [n for n in sum_vec if n != 0]

        return str(max(non_zero) - min(non_zero))


if __name__ == "__main__":
    Day14().main()
