from typing import List

from day import Day
from parsers import read_file_lines_int


class DayXX(Day):
    @property
    def day_name(self) -> str:
        return "XX"

    @staticmethod
    def custom_parser(path: str) -> str:
        pass

    def get_parser(self):
        return read_file_lines_int

    def star1(self, lines: List[int]) -> str:
        pass

    def star2(self, lines: List[int]) -> str:
        pass


if __name__ == "__main__":
    DayXX().main()
