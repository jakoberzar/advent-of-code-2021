from typing import Any, List, Tuple
from heapq import heappush, heappop
from math import inf

import numpy as np

from day import Day
from parsers import read_file_lines

Coords = Tuple[int, int]


class Node:
    def __init__(self, pos: Coords, value: int, tent_dist=0) -> None:
        self.pos = pos
        self.tent_dist = tent_dist
        self.value = value
        self.visited = False


class Day15(Day):
    @property
    def day_name(self) -> str:
        return "15"

    @staticmethod
    def custom_parser(path: str) -> str:
        lines = read_file_lines(path)

        return np.array([[int(n) for n in list(line)] for line in lines], dtype=np.int64)

    def get_parser(self):
        return self.custom_parser

    def get_node_neigh(self, pos: Coords, node_grid: List[List[Node]]) -> List[Node]:
        (row, col) = pos
        neighs = []
        if row > 0:
            neighs.append(node_grid[row - 1][col])
        if row < len(node_grid) - 1:
            neighs.append(node_grid[row + 1][col])
        if col > 0:
            neighs.append(node_grid[row][col - 1])
        if col < len(node_grid[0]) - 1:
            neighs.append(node_grid[row][col + 1])
        return neighs

    def np_array_to_node_grid(self, grid: np.array) -> List[List[Node]]:
        return [
            [
                Node(pos=(row, col), value=grid[row, col], tent_dist=inf)
                for col in range(grid.shape[1])
            ]
            for row in range(grid.shape[0])
        ]

    def find_shortest_path(self, grid: np.array) -> int:
        node_grid = self.np_array_to_node_grid(grid)
        start_node = node_grid[0][0]
        end_node = node_grid[-1][-1]

        unvisited = []
        start_node.tent_dist = 0
        heappush(unvisited, ((start_node.tent_dist, 0, start_node.pos), start_node))
        while not end_node.visited:
            (_, node) = heappop(unvisited)
            node.visited = True

            neighs = self.get_node_neigh(node.pos, node_grid)
            for neigh in neighs:
                if neigh.visited:
                    continue

                new_tent_dist = neigh.value + node.tent_dist
                if new_tent_dist < neigh.tent_dist:
                    neigh.tent_dist = new_tent_dist

                    heuristic = (end_node.pos[0] - neigh.pos[0]) + (end_node.pos[1] - neigh.pos[1])
                    heappush(unvisited, ((new_tent_dist, heuristic, neigh.pos), neigh))

        return end_node.tent_dist

    def star1(self, grid: np.array) -> str:
        return str(self.find_shortest_path(grid))

    def star2(self, grid: np.array) -> str:
        end_grid = None
        for i in range(5):
            row = None
            for j in range(5):
                add = i + j
                sub_grid = np.copy(grid)
                sub_grid += add
                sub_grid[sub_grid > 9] -= 9
                row = sub_grid if row is None else np.hstack((row, sub_grid))

            end_grid = row if end_grid is None else np.vstack((end_grid, row))
        return str(self.find_shortest_path(end_grid))


if __name__ == "__main__":
    Day15().main()
