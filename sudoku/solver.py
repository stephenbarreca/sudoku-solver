from copy import deepcopy

import numpy as np

from sudoku.puzzle import Board, SudokuPuzzle
from sudoku.validators import is_square, is_valid_group_shape
from sudoku.validators.array_validators import is_col, is_row

import logging
logging.basicConfig(level=logging.INFO)

def solve_simple_board(board: SudokuPuzzle):
    board = deepcopy(board)
    rows = [check_and_fill_simple_case(row) for row in board.rows]
    board = SudokuPuzzle.from_rows(rows)

    cols = [check_and_fill_simple_case(col) for col in board.cols]
    board = SudokuPuzzle.from_rows(cols)

    squares = [check_and_fill_simple_case(square) for square in board.squares]
    # board = SudokuPuzzle.from_rows(squares)
    return board


def fill_group_simple_case(arr: np.ndarray) -> np.ndarray:
    """check if only 1 number is missing in the group. if it is fill it. """
    if not is_valid_group_shape(arr):
        raise ValueError('group is invalid shape')

    zero_array = arr == 0

    if is_col(arr):
        return check_and_fill_simple_case(arr)
    elif is_row(arr):
        return check_and_fill_simple_case(arr)
    elif is_square(arr):
        return check_and_fill_simple_case(arr)


def check_and_fill_simple_case(arr: np.ndarray) -> np.ndarray:
    if len(arr[arr == 0]) == 1:
        for i in range(1, arr.size + 1):
            if i not in arr:
                np.place(arr, arr == 0, i)
                break
    return arr


class SudokuSolver:
    def __init__(self, puzzle: SudokuPuzzle | Board, *args, **kwargs):
        if isinstance(puzzle, SudokuPuzzle):
            self.puzzle = puzzle
        else:
            self.puzzle = SudokuPuzzle(puzzle, *args, **kwargs)

    def __repr__(self):
        return repr(self.puzzle.board)

    @property
    def is_solved(self):
        return self.puzzle.is_solved

    def solve_simple_cases(self):
        original_puzzle = self.puzzle
        potentially_solved_puzzle = solve_simple_board(original_puzzle)
        logging.info(f'{original_puzzle=}')
        logging.info(f'{potentially_solved_puzzle=}')

        while not np.array_equal(original_puzzle.board, potentially_solved_puzzle.board):
            original_puzzle = potentially_solved_puzzle
            potentially_solved_puzzle = solve_simple_board(original_puzzle)
            logging.info(f'{original_puzzle=}')
            logging.info(f'{potentially_solved_puzzle=}')

        self.puzzle = potentially_solved_puzzle
        logging.info(f'{self.puzzle=}')
