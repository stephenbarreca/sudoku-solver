import logging
from copy import deepcopy
from attrs import define, field

import numpy as np

from sudoku.puzzle import Board, SudokuPuzzle, Cell
from sudoku.validators import is_square, is_valid_group_shape
from sudoku.validators.array_validators import is_col, is_row

logging.basicConfig(level=logging.INFO)


def solve_simple_board(board: SudokuPuzzle):
    board = deepcopy(board)
    rows = [check_and_fill_group_with_one_missing(row) for row in board.rows]
    board = SudokuPuzzle.from_rows(rows)

    cols = [check_and_fill_group_with_one_missing(col) for col in board.cols]
    board = SudokuPuzzle.from_rows(cols)

    squares = [check_and_fill_group_with_one_missing(square) for square in board.squares]
    # board = SudokuPuzzle.from_rows(squares)
    return board


def fill_groups_with_one_missing(arr: np.ndarray) -> np.ndarray:
    """check if only 1 number is missing in the group. if it is fill it. """
    if not is_valid_group_shape(arr):
        raise ValueError('group is invalid shape')

    zero_array = arr == 0

    if is_col(arr):
        return check_and_fill_group_with_one_missing(arr)
    elif is_row(arr):
        return check_and_fill_group_with_one_missing(arr)
    elif is_square(arr):
        return check_and_fill_group_with_one_missing(arr)


def check_and_fill_group_with_one_missing(group: np.ndarray) -> np.ndarray:
    if len(group[group == 0]) == 1:
        for i in range(1, group.size + 1):
            if i not in group:
                np.place(group, group == 0, i)
                break
    return group


def convert_to_puzzle(puzzle: SudokuPuzzle | Board) -> SudokuPuzzle:
    if isinstance(puzzle, SudokuPuzzle):
        return puzzle
    else:
        return SudokuPuzzle(puzzle)

@define
class SudokuSolver:
    puzzle: SudokuPuzzle = field(converter=SudokuPuzzle, repr=lambda p: f'\n{repr(p.board)}\nsolved={p.is_solved}')

    @property
    def is_solved(self):
        return self.puzzle.is_solved

    def solve_groups_with_one_missing(self):
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

    def solve_cells_with_one_possibility(self):
        for coord in self.puzzle.get_empty_cell_coords():
            cell = Cell(coord[0], coord[1], 0)
            possible_cell_values = self.puzzle.get_possible_cell_values(cell)
            if possible_cell_values.size == 1:
                self.puzzle.put_cell(cell, possible_cell_values[0])

    def solve(self):
        self.solve_groups_with_one_missing()
