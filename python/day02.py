from typing import List, Tuple

from day import Day
from parsers import read_file_lines


class Day02(Day):
    @property
    def day_name(self) -> str:
        return "02"

    @staticmethod
    def custom_parser(path: str) -> str:
        lines = read_file_lines(path)

        def transform_line(line: str) -> Tuple[str, int]:
            (dir, amount) = line.split(" ")
            return (dir, int(amount))

        return [transform_line(line) for line in lines]

    def get_parser(self):
        return self.custom_parser

    def star1(self, lines: List[Tuple[str, int]]) -> str:
        horizontal = 0
        depth = 0
        for (dir, amount) in lines:
            if dir == "forward":
                horizontal += amount
            elif dir == "down":
                depth += amount
            elif dir == "up":
                depth -= amount

        return str(horizontal * depth)

    def star2(self, lines: List[Tuple[str, int]]) -> str:
        horizontal = 0
        depth = 0
        aim = 0
        for (dir, amount) in lines:
            if dir == "forward":
                horizontal += amount
                depth += aim * amount
            elif dir == "down":
                aim += amount
            elif dir == "up":
                aim -= amount

        return str(horizontal * depth)


if __name__ == "__main__":
    Day02().main()
