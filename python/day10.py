from typing import List

from day import Day
from parsers import read_file_lines


class Day10(Day):

    matching_closing = {"(": ")", "[": "]", "{": "}", "<": ">"}

    @property
    def day_name(self) -> str:
        return "10"

    @staticmethod
    def custom_parser(path: str) -> str:
        lines = read_file_lines(path)
        return [list(line) for line in lines]

    def get_parser(self):
        return self.custom_parser

    def line_corrupted_score(self, line: List[str]) -> int:
        stack = []
        for ch in line:
            if ch == "(" or ch == "[" or ch == "{" or ch == "<":
                stack.append(ch)
            else:
                # ch is one of the closing brackets
                top = stack[-1]
                if ch == self.matching_closing[top]:
                    stack.pop()
                else:
                    # wrong ch!
                    if ch == ")":
                        return 3
                    elif ch == "]":
                        return 57
                    elif ch == "}":
                        return 1197
                    elif ch == ">":
                        return 25137
        return 0

    def star1(self, lines: List[List[str]]) -> str:
        scores = [self.line_corrupted_score(line) for line in lines]
        return str(sum(scores))

    def line_completion_score(self, line: List[str]) -> int:
        stack = []
        for ch in line:
            if ch == "(" or ch == "[" or ch == "{" or ch == "<":
                stack.append(ch)
            else:
                # ch is one of the closing brackets
                top = stack[-1]
                if ch == self.matching_closing[top]:
                    stack.pop()
                else:
                    # wrong ch!
                    raise Exception("Corrupted line in incomplete line!!!")

        score = 0
        while stack:
            top = stack.pop()
            score *= 5
            if top == "(":
                score += 1
            elif top == "[":
                score += 2
            elif top == "{":
                score += 3
            elif top == "<":
                score += 4
        return score

    def star2(self, lines: List[List[str]]) -> str:
        scores = [
            self.line_completion_score(line)
            for line in lines
            if self.line_corrupted_score(line) == 0
        ]
        scores.sort()
        return str(scores[len(scores) // 2])


if __name__ == "__main__":
    Day10().main()
