from collections import Counter, deque
from typing import Callable, List, Set, Tuple
import sys

import numpy as np

from day import Day
from parsers import read_file_lines


class Day09(Day):
    Coords = Tuple[int, int]

    @property
    def day_name(self) -> str:
        return "09"

    @staticmethod
    def custom_parser(path: str) -> str:
        lines = read_file_lines(path)
        return np.array([[int(n) for n in list(line)] for line in lines], dtype=np.int8)

    def get_parser(self):
        return self.custom_parser

    def get_neighbors(
        self, coords: Coords, input: np.array, op: Callable[[int, int], bool]
    ) -> List[Coords]:
        neighbors = []
        (row, col) = coords

        el = input[row, col]
        # left
        if col > 0 and op(input[row, col - 1], el):
            neighbors.append((row, col - 1))
        # right
        if col < input.shape[1] - 1 and op(input[row, col + 1], el):
            neighbors.append((row, col + 1))
        # up
        if row > 0 and op(input[row - 1, col], el):
            neighbors.append((row - 1, col))
        # down
        if row < input.shape[0] - 1 and op(input[row + 1, col], el):
            neighbors.append((row + 1, col))

        return neighbors

    def get_lower_eq_neighbors(self, coords: Coords, input: np.array) -> List[Coords]:
        return self.get_neighbors(coords, input, lambda x, y: x <= y)

    def get_lower_neighbors(self, coords: Coords, input: np.array) -> List[Coords]:
        return self.get_neighbors(coords, input, lambda x, y: x < y)

    def get_upper_neighbors(self, coords: Coords, input: np.array) -> List[Coords]:
        return self.get_neighbors(coords, input, lambda x, y: x > y)

    def find_low_points(self, input: np.array) -> List[Coords]:
        coords = []
        for row_idx in range(input.shape[0]):
            for col_idx in range(input.shape[1]):
                if len(self.get_lower_eq_neighbors((row_idx, col_idx), input)) == 0:
                    coords.append((row_idx, col_idx))
        return coords

    def star1(self, input: np.array) -> str:
        low_points = self.find_low_points(input)
        return str(sum(input[coords] + 1 for coords in low_points))

    def dfs_color_map(self, coords: Coords, input: np.array, basin_map: np.array) -> int:
        if basin_map[coords] != 0:
            return basin_map[coords]

        if input[coords] == 9:
            basin_map[coords] = -1
            return -1

        lower_neighbors = self.get_lower_neighbors(coords, input)
        my_color = -1
        if lower_neighbors:
            colors = [
                self.dfs_color_map(nb_coords, input, basin_map) for nb_coords in lower_neighbors
            ]
            if all(colors[0] == color for color in colors):
                my_color = colors[0]

        basin_map[coords] = my_color

        return my_color

    def dfs_coloring(self, input: np.array, basin_map: np.array) -> Counter:
        basin_sizes = Counter()
        for row in range(input.shape[0]):
            for col in range(input.shape[1]):
                color = self.dfs_color_map((row, col), input, basin_map)
                if color != -1:
                    basin_sizes[color] += 1

        return basin_sizes

    def bfs_coloring(
        self, input: np.array, basin_map: np.array, low_points: List[Coords]
    ) -> Counter:
        basin_sizes = Counter()
        for color, coords in enumerate(low_points, start=1):
            q = deque([coords])
            while q:
                coords = q.popleft()
                basin_sizes[color] += 1
                basin_map[coords] = color
                upper = self.get_upper_neighbors(coords, input)
                for up_coords in upper:
                    if (
                        input[up_coords] != 9
                        and basin_map[up_coords] == 0
                        and all(
                            basin_map[y, x] == color
                            for y, x in self.get_lower_neighbors(up_coords, input)
                        )
                    ):
                        q.append(up_coords)
        return basin_sizes

    def star2(self, input: np.array) -> str:
        basin_map = np.zeros(input.shape, dtype=np.int32)

        # color the map
        low_points = self.find_low_points(input)
        for color, coords in enumerate(low_points, start=1):
            basin_map[coords] = color

        # bfs coloring
        basin_sizes = self.bfs_coloring(input, basin_map, low_points)

        # dfs
        # basin_sizes = self.dfs_coloring(input, basin_map)

        biggest = [count for (_, count) in basin_sizes.most_common(3)]
        return str(np.product(biggest))


if __name__ == "__main__":
    Day09().main()
