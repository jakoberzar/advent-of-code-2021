from typing import Deque, List
from collections import Counter, deque

from day import Day
from parsers import read_file_commas_int


class Day06(Day):
    @property
    def day_name(self) -> str:
        return "06"

    @staticmethod
    def list_to_deq(list: List[int]) -> Deque[int]:
        deq = deque([0] * 9)
        counter = Counter(list)
        for key, incidence in counter.items():
            deq[int(key)] = incidence
        return deq

    def get_parser(self):
        return read_file_commas_int

    def simulate(self, lanterns: Deque[int], days: int) -> Deque[int]:
        deq = lanterns.copy()
        for _ in range(days):
            parents = deq.popleft()
            deq[6] += parents
            deq.append(parents)  # 1 child per parent
        return deq

    def star1(self, lanterns: List[int]) -> str:
        deq = Day06.list_to_deq(lanterns)
        deq = self.simulate(deq, 80)
        return str(sum(deq))

    def star2(self, lanterns: List[int]) -> str:
        deq = Day06.list_to_deq(lanterns)
        deq = self.simulate(deq, 256)
        return str(sum(deq))


if __name__ == "__main__":
    Day06().main()
