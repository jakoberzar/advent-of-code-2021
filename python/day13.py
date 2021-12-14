from typing import List, Tuple

import numpy as np

from day import Day
from parsers import read_file_lines


class Day13(Day):
    Input = Tuple[np.array, List[Tuple[str, int]]]

    @property
    def day_name(self) -> str:
        return "13"

    @staticmethod
    def custom_parser(path: str) -> Input:
        lines = read_file_lines(path)
        parsing_coords = True
        coords = []
        folds = []
        for line in lines:
            if line == "" and parsing_coords:
                parsing_coords = False
                continue
            if parsing_coords:
                (x, y) = line.split(",")
                coords.append((int(x), int(y)))
            else:
                fold = line.removeprefix("fold along ")
                (axis, val) = fold.split("=")
                folds.append((axis, int(val)))
        max_x = max(x for (x, _) in coords)
        max_y = max(y for (_, y) in coords)
        grid = np.zeros((max_y + 1, max_x + 1), dtype=np.int32)
        for (x, y) in coords:
            grid[y, x] = 1

        return (grid, folds)

    def get_parser(self):
        return self.custom_parser

    def fold(self, grid: np.array, fold: Tuple[str, int]) -> np.array:
        (axis, val) = fold
        if axis == "x":
            part1 = grid[:, 0:val]
            part2 = grid[:, :val:-1]
            dim1 = val
            dim2 = grid.shape[1] - val - 1
            buffer = np.zeros((grid.shape[0], abs(dim2 - dim1)), dtype=np.int32)
            if dim1 > dim2:
                part2 = np.append(buffer, part2, axis=1)
            else:
                part1 = np.append(buffer, part1, axis=1)
            grid = part1 | part2
        elif axis == "y":
            part1 = grid[0:val, :]
            part2 = grid[:val:-1, :]
            dim1 = val
            dim2 = grid.shape[0] - val - 1
            buffer = np.zeros((abs(dim2 - dim1), grid.shape[1]), dtype=np.int32)
            if dim1 > dim2:
                part2 = np.append(buffer, part2, axis=0)
            else:
                part1 = np.append(buffer, part1, axis=0)

            grid = part1 | part2
        else:
            raise Exception("Invalid axis!")

        return grid

    def star1(self, input: Input) -> str:
        (grid, folds) = input
        grid = np.copy(grid)

        print(grid)
        grid = self.fold(grid, folds[0])

        print(grid)
        return str(np.sum(grid))

    def star2(self, input: Input) -> str:
        (grid, folds) = input
        grid = np.copy(grid)

        for fold in folds:
            grid = self.fold(grid, fold)

        np.set_printoptions(edgeitems=30, linewidth=10000)
        print(grid)
        return str(np.sum(grid))


if __name__ == "__main__":
    Day13().main()
