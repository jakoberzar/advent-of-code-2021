from typing import List
from collections import Counter

from day import Day
from parsers import read_file_lines


class Day07(Day):
    @property
    def day_name(self) -> str:
        return "07"

    @staticmethod
    def custom_parser(path: str) -> str:
        lines = read_file_lines(path)
        return [int(n) for n in lines[0].split(",")]

    def get_parser(self):
        return self.custom_parser

    def calculate_fuel(self, position_count: List[tuple[int, int]], target: int) -> int:
        return sum(abs(target - pos) * count for (pos, count) in position_count)

    def calculate_fuel_crab_way(
        self, position_count: List[tuple[int, int]], target: int
    ) -> int:
        def calculate_diff(x: int) -> int:
            return int(abs(target - x) * (abs(target - x) + 1) / 2)

        return sum(calculate_diff(pos) * count for (pos, count) in position_count)

    def star1(self, positions: List[int]) -> str:
        counter = Counter(positions)
        frequencies = counter.most_common()
        min_fuel = None
        for (pos, _) in frequencies:
            fuel = self.calculate_fuel(frequencies, pos)
            if min_fuel is None or fuel < min_fuel:
                min_fuel = fuel
        return str(min_fuel)

    def star2(self, positions: List[int]) -> str:
        counter = Counter(positions)
        frequencies = counter.most_common()
        min_pos = min(positions)
        max_pos = max(positions)
        max_min_diff = max_pos - min_pos
        avg = round(max_min_diff / 2)
        min_fuel = self.calculate_fuel_crab_way(frequencies, avg)
        for i in range(max_min_diff):
            pos = min_pos + i
            fuel = self.calculate_fuel_crab_way(frequencies, pos)
            if fuel < min_fuel:
                min_fuel = fuel
        return str(min_fuel)


if __name__ == "__main__":
    Day07().main()
