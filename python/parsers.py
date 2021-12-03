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
