from typing import List, Optional

from day import Day
from parsers import read_file_lines


class Game:
    def __init__(self, lines: List[str]) -> None:
        self.draws = [int(draw) for draw in lines[0].split(",")]
        self.boards = []
        line = 2
        while line < len(lines):
            board = []
            for row in range(5):
                board.append(
                    [[int(n), False] for n in lines[line + row].split(" ") if n.strip() != ""]
                )
                assert len(board[row]) == 5
            self.boards.append(board)
            line += 6


class Day04(Day):
    @property
    def day_name(self) -> str:
        return "04"

    @staticmethod
    def custom_parser(path: str) -> Game:
        lines = read_file_lines(path)
        return Game(lines)

    def get_parser(self):
        return self.custom_parser

    def mark_boards(self, game: Game, draw: int) -> None:
        for board in game.boards:
            for row in board:
                for col in row:
                    if col[0] == draw:
                        col[1] = True

    def check_wins(self, game: Game) -> List[Optional[int]]:
        wins = []
        for board in game.boards:
            unmarked = 0
            found_win = False
            # check rows
            for row in board:
                all_marked = True
                for col in row:
                    if not col[1]:
                        unmarked += col[0]
                        all_marked = False
                if all_marked:
                    found_win = True

            # check cols
            for col in range(5):
                all_marked = True
                for row in range(5):
                    val = board[row][col]
                    if not val[1]:
                        all_marked = False
                if all_marked:
                    found_win = True

            wins.append(unmarked if found_win else None)
        return wins

    def check_win(self, game: Game) -> Optional[int]:
        wins = self.check_wins(game)
        for win in wins:
            if win is not None:
                return win
        return None

    def star1(self, game: Game) -> str:
        # print(game.draws)
        # for board in game.boards:
        #     print("Board:")
        #     print(board)
        for draw in game.draws:
            self.mark_boards(game, draw)
            win = self.check_win(game)
            if win is not None:
                return str(win * draw)

    def star2(self, game: Game) -> str:
        last_wins = [None for _ in game.boards]
        for draw in game.draws:
            self.mark_boards(game, draw)
            wins = self.check_wins(game)
            if all([win is not None for win in wins]):
                for idx in range(len(game.boards)):
                    if last_wins[idx] is None:
                        return str(wins[idx] * draw)
            last_wins = wins


if __name__ == "__main__":
    Day04().main()
