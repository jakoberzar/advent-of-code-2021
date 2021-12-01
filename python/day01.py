from typing import List

from day import Day
from parsers import read_file_lines_int


class Day01(Day):
    @property
    def day_name(self) -> str:
        return "01"

    def get_parser(self):
        return read_file_lines_int

    def star1(self, lines: List[int]) -> str:
        count = 0
        last = lines[0]
        for line in lines[1:]:
            if line > last:
                count += 1
            last = line

        return str(count)

    def star2(self, lines: List[int]) -> str:
        count = 0
        window_sum = sum(lines[0:3])
        last = window_sum
        for idx, line in enumerate(lines[3:], start=3):
            window_sum += line
            window_sum -= lines[idx - 3]
            if window_sum > last:
                count += 1
            last = window_sum

        return str(count)


if __name__ == "__main__":
    Day01().main()
