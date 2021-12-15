from typing import Dict, List

from day import Day
from parsers import read_file_lines


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.neighbors = []
        self.big = name.isupper()
        self.visited = False

    def is_start(self) -> bool:
        return self.name == "start"

    def is_end(self) -> bool:
        return self.name == "end"

    def add_neigh(self, neigh) -> None:
        self.neighbors.append(neigh)

    def visit(self) -> int:
        if self.is_end():
            return 1

        if not self.big:
            self.visited = True

        count = 0
        for neigh in self.neighbors:
            if not neigh.visited:
                count += neigh.visit()

        self.visited = False

        return count

    def visit_more(self, visit_joker: bool) -> int:
        if self.is_end():
            return 1

        if not self.big:
            self.visited = True

        count = 0
        for neigh in self.neighbors:
            if neigh.big:
                count += neigh.visit_more(visit_joker)
            else:
                if not neigh.visited:
                    count += neigh.visit_more(visit_joker)
                elif visit_joker and not neigh.is_end() and not neigh.is_start():
                    count += neigh.visit_more(False)
                    neigh.visited = True  # reset to True

        self.visited = False

        return count


class Day12(Day):
    @property
    def day_name(self) -> str:
        return "12"

    @staticmethod
    def custom_parser(path: str) -> Dict[str, Node]:
        lines = read_file_lines(path)
        nodes = {}
        for line in lines:
            node_names = line.split("-")
            left = nodes.setdefault(node_names[0], Node(node_names[0]))
            right = nodes.setdefault(node_names[1], Node(node_names[1]))
            left.add_neigh(right)
            right.add_neigh(left)
        return nodes

    def get_parser(self):
        return self.custom_parser

    def star1(self, nodes: Dict[str, Node]) -> str:
        start = nodes["start"]
        return str(start.visit())

    def star2(self, nodes: Dict[str, Node]) -> str:
        start = nodes["start"]
        return str(start.visit_more(visit_joker=True))


if __name__ == "__main__":
    Day12().main()
