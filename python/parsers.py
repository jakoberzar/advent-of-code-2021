from typing import List


def read_file_lines(path: str) -> List[str]:
    with open(path, encoding="utf-8") as file:
        lines = file.readlines()
        lines = [line.strip() for line in lines]
        if lines and lines[len(lines) - 1].strip() == "":
            lines.pop()
        return lines


def read_file_lines_int(path: str) -> List[int]:
    return [int(line) for line in read_file_lines(path)]


def read_file_commas_int(path: str) -> List[int]:
    with open(path, encoding="utf-8") as file:
        numbers = file.read().strip().split(",")
        return [int(n) for n in numbers]
