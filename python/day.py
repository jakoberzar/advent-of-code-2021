from abc import ABC, abstractmethod
from os.path import join
from sys import argv

from parsers import read_file_lines


class Day(ABC):

    INPUT_FOLDER_PATH = "inputs"

    @property
    @abstractmethod
    def day_name(self) -> str:
        return

    @property
    def day_input(self) -> int:
        return join(self.INPUT_FOLDER_PATH, f"day-{self.day_name}")

    def get_parser(self):
        """Get a parser that gets a path and returns the file parsed"""
        return read_file_lines

    @abstractmethod
    def star1(self, input) -> str:
        return

    @abstractmethod
    def star2(self, input) -> str:
        return

    def parse_arguments_file_path(self) -> str:
        file_txt_name = argv[1].removesuffix(".txt")
        return join(self.day_input, file_txt_name + ".txt")

    def main(self):
        full_path = self.parse_arguments_file_path()
        parser = self.get_parser()
        file_parsed = parser(full_path)
        print("Star 1: " + self.star1(file_parsed))
        print("Star 2: " + self.star2(file_parsed))
