from __future__ import annotations
import argparse
from pathlib import Path
from typing import Optional, Union

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')


class GameBoard():
    def __init__(self, board_array: list[list[str]]):
        self.board_array = board_array
        self.bingo = False

    def check_row_for_bingo(self, called_numbers):
        for i, y in enumerate([x in called_numbers for x in item] for item in self.board_array):
            all_true = sum(bool(j) for j in y)
            if all_true == 5:
                self.bingo = True
            else:
                continue
        return self.bingo

    def check_col_for_bingo(self, called_numbers):
        for i in range(5):
            column = [row[i] in called_numbers for row in self.board_array]
            all_true = sum(bool(j) for j in column)
            if all_true == 5:
                self.bingo = True
            else:
                continue
        return self.bingo

    def calculate_score(self, called_numbers):
        joined_board = []
        for x in self.board_array:
            joined_board += x
        sum_of_unmarked = sum(int(x) for x in joined_board if x not in called_numbers)
        return sum_of_unmarked * int(called_numbers[-1])


def create_boards(lines):
    numbers = []
    game_boards = []
    board_array = []
    for idx, line in enumerate(lines):
        if idx == 0:
            numbers = line.split(',')
        elif not line:
            if not board_array:
                continue
            game_boards.append(GameBoard(board_array=board_array))
            board_array = []
        else:
            board_array.append(line.strip().replace('  ', ' ').split(' '))
    if board_array:
        game_boards.append(GameBoard(board_array=board_array))
    return game_boards, numbers


def check_bingo(game_boards, numbers):
    for i in range(len(numbers)):
        for idx, board in enumerate(game_boards):
            called_numbers = numbers[:i]
            if called_numbers == '':
                continue
            row_win = board.check_row_for_bingo(called_numbers)
            col_win = board.check_col_for_bingo(called_numbers)
            if row_win or col_win:
                return idx, numbers[:i]
            else:
                continue


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    lines = s if testing and type(s) == list[str] else s.splitlines()
    game_boards, numbers = create_boards(lines)
    winning_board, called_numbers = check_bingo(game_boards, numbers)
    return game_boards[winning_board].calculate_score(called_numbers)


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 4512


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
