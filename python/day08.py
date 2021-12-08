from typing import List

from day import Day
from parsers import read_file_lines


class Display:
    @staticmethod
    def make_pat_canonical(s: str):
        return "".join(sorted(s))

    def __init__(self, line: str) -> None:
        parts = line.split(" | ")

        self.patterns = list(map(self.make_pat_canonical, parts[0].split(" ")))
        self.output = list(map(self.make_pat_canonical, parts[1].split(" ")))

        self.numbers = [None] * 10
        self.letters = {
            "a": None,
            "b": None,
            "c": None,
            "d": None,
            "e": None,
            "f": None,
            "g": None,
        }

        self.find_mapping()

    def find_mapping(self) -> None:
        # determine 1, 4, 7, 8 on len only
        len5 = []
        len6 = []
        for pattern in self.patterns:
            l = len(pattern)
            if l == 2:
                self.numbers[1] = pattern
            elif l == 3:
                self.numbers[7] = pattern
            elif l == 4:
                self.numbers[4] = pattern
            elif l == 5:
                # len 5: 2, 3, 5
                len5.append(pattern)
            elif l == 6:
                # len 6: 0, 6, 9
                len6.append(pattern)
            elif l == 7:
                self.numbers[8] = pattern

        cf = set(self.numbers[1])
        self.letters["a"] = set(self.numbers[7]).difference(cf).pop()
        bd = set(self.numbers[4]).difference(cf)

        # determine 3
        self.numbers[3] = [p for p in len5 if set(p).issuperset(cf)][0]
        len5.remove(self.numbers[3])
        pat3_set = set(self.numbers[3])
        self.letters["d"] = pat3_set.intersection(bd).pop()
        self.letters["b"] = bd.difference(pat3_set).pop()
        self.letters["g"] = (
            pat3_set.difference(bd).difference(cf).difference(self.letters["a"])
        ).pop()

        # determine 2 and 5
        for pat in len5:
            pat_set = set(pat)
            if self.letters["b"] in pat_set:
                self.numbers[5] = pat
                self.letters["f"] = pat_set.intersection(cf).pop()
                self.letters["c"] = cf.difference(pat_set).pop()
            else:
                self.numbers[2] = pat
                self.letters["e"] = pat_set.difference(pat3_set).pop()

        # determine 0, 6, 9
        for pat in len6:
            pat_set = set(pat)
            if not self.letters["d"] in pat_set:
                self.numbers[0] = pat
            elif self.letters["c"] in pat_set:
                self.numbers[9] = pat
            else:
                self.numbers[6] = pat

    def get_output_numbers(self) -> List[int]:
        nums = []
        inverse_numbers = {pat: idx for idx, pat in enumerate(self.numbers)}
        for out in self.output:
            nums.append(inverse_numbers[out])
        return nums

    def get_output_number(self) -> int:
        final = 0
        for n in self.get_output_numbers():
            final *= 10
            final += n
        return final


class Day08(Day):
    @property
    def day_name(self) -> str:
        return "08"

    @staticmethod
    def custom_parser(path: str) -> str:
        lines = read_file_lines(path)
        return [Display(line) for line in lines]

    def get_parser(self):
        return self.custom_parser

    def star1(self, displays: List[Display]) -> str:
        unique_digits = 0
        for display in displays:
            unique = [
                digit for digit in display.output if len(digit) <= 4 or len(digit) == 7
            ]
            unique_digits += len(unique)
        return str(unique_digits)

    def star2(self, displays: List[Display]) -> str:
        ans = 0
        for display in displays:
            display.find_mapping()
            ans += display.get_output_number()

        return str(ans)


if __name__ == "__main__":
    Day08().main()
