from typing import List

import numpy as np

from day import Day
from parsers import read_file_lines

FLASHED = 20


class Day11(Day):
    @property
    def day_name(self) -> str:
        return "11"

    @staticmethod
    def custom_parser(path: str) -> str:
        lines = read_file_lines(path)
        return np.array([[int(n) for n in line] for line in lines], dtype=np.int8)

    def get_parser(self):
        return self.custom_parser

    def flash(self, row: int, col: int, grid: np.array) -> int:
        if grid[row, col] <= 9 or grid[row, col] >= FLASHED:
            return 0

        grid[row, col] = FLASHED
        flash_count = 1

        # above row
        if row > 0:
            if col > 0:
                grid[row - 1][col - 1] += 1
                flash_count += self.flash(row - 1, col - 1, grid)

            grid[row - 1][col] += 1
            flash_count += self.flash(row - 1, col, grid)

            if col < grid.shape[1] - 1:
                grid[row - 1][col + 1] += 1
                flash_count += self.flash(row - 1, col + 1, grid)

        # same row
        if col > 0:
            grid[row][col - 1] += 1
            flash_count += self.flash(row, col - 1, grid)

        if col < grid.shape[1] - 1:
            grid[row][col + 1] += 1
            flash_count += self.flash(row, col + 1, grid)

        # below row
        if row < grid.shape[0] - 1:
            if col > 0:
                grid[row + 1][col - 1] += 1
                flash_count += self.flash(row + 1, col - 1, grid)

            grid[row + 1][col] += 1
            flash_count += self.flash(row + 1, col, grid)

            if col < grid.shape[1] - 1:
                grid[row + 1][col + 1] += 1
                flash_count += self.flash(row + 1, col + 1, grid)

        return flash_count

    def do_step(self, grid: np.array) -> int:
        highlight_count = 0
        grid += 1
        for row in range(grid.shape[0]):
            for col in range(grid.shape[1]):
                if grid[row, col] > 9 and grid[row, col] < FLASHED:
                    highlight_count += self.flash(row, col, grid)
        grid[grid > 9] = 0
        return highlight_count

    def star1(self, input: np.array) -> str:
        highlight_count = 0
        grid = np.copy(input)
        for _ in range(100):
            highlight_count += self.do_step(grid)

        return str(highlight_count)

    def star2(self, input: np.array) -> str:
        grid = np.copy(input)
        step = 1
        while True:
            highlight_count = self.do_step(grid)
            if highlight_count == grid.shape[0] * grid.shape[1]:
                return str(step)
            step += 1


if __name__ == "__main__":
    Day11().main()
