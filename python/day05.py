from typing import List, Tuple

from day import Day
from parsers import read_file_lines


class Day05(Day):
    Lines = List[List[Tuple[int, int]]]
    Grid = List[List[int]]

    @property
    def day_name(self) -> str:
        return "05"

    @staticmethod
    def custom_parser(path: str) -> str:
        lines = read_file_lines(path)
        lines_parsed = []
        for line in lines:
            split = line.split(" -> ")
            start = split[0].split(",")
            end = split[1].split(",")
            lines_parsed.append(
                [(int(start[1]), int(start[0])), (int(end[1]), int(end[0]))]
            )

        return lines_parsed

    def get_parser(self):
        return self.custom_parser

    def create_grid(self, lines: Lines) -> Grid:
        grid = []
        max_x = None
        max_y = None
        for [(x1, y1), (x2, y2)] in lines:
            if max_x is None or x1 > max_x:
                max_x = x1
            if max_x is None or x2 > max_x:
                max_x = x2
            if max_y is None or y1 > max_y:
                max_y = y1
            if max_y is None or y2 > max_y:
                max_y = y2

        for _ in range(max_y + 1):
            row = [0] * (max_x + 1)
            grid.append(row)
        return grid

    def count_overlaps(self, grid: Grid) -> int:
        count = 0
        for row in grid:
            for col in row:
                if col > 1:
                    count += 1
        return count

    def draw_lines(self, grid: Grid, lines: Lines, diagonal: bool = False) -> None:
        for [(x1, y1), (x2, y2)] in lines:
            if x1 == x2:
                l = min(y1, y2)
                u = max(y1, y2) + 1
                for y in range(l, u):
                    grid[y][x1] += 1
            elif y1 == y2:
                l = min(x1, x2)
                u = max(x1, x2) + 1
                for x in range(l, u):
                    grid[y1][x] += 1
            elif diagonal:
                if x1 > x2:
                    diff = x1 - x2
                    x_multiplier = -1
                else:
                    diff = x2 - x1
                    x_multiplier = 1
                y_multiplier = 1 if y1 < y2 else -1

                for add in range(diff + 1):
                    grid[y1 + add * y_multiplier][x1 + add * x_multiplier] += 1

    def star1(self, lines: Lines) -> str:
        grid = self.create_grid(lines)
        self.draw_lines(grid, lines)
        return str(self.count_overlaps(grid))

    def star2(self, lines: Lines) -> str:
        grid = self.create_grid(lines)
        self.draw_lines(grid, lines, diagonal=True)
        return str(self.count_overlaps(grid))


if __name__ == "__main__":
    Day05().main()
