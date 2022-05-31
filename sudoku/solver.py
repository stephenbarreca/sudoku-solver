import logging
from copy import deepcopy
from time import time

import numpy as np
from attrs import define, field
from numpy.typing import NDArray

from sudoku.puzzle import Board, Cell, SudokuPuzzle
from sudoku.groups import Group
from sudoku.validators import is_square_array, is_valid_group_shape
from sudoku.validators.group_validators import is_col, is_row

logging.basicConfig(level=logging.INFO)


def solve_simple_board(board: SudokuPuzzle):
    board = deepcopy(board)
    rows = [check_and_fill_group_with_one_missing(row) for row in board.rows]
    board = SudokuPuzzle.from_rows(rows)

    cols = [check_and_fill_group_with_one_missing(col) for col in board.cols]
    board = SudokuPuzzle.from_cols(cols)

    squares = [check_and_fill_group_with_one_missing(square) for square in board.squares]
    board = SudokuPuzzle.from_squares(squares)

    return board


def fill_groups_with_one_missing(group: Group) -> Group:
    """check if only 1 number is missing in the group. if it is fill it. """
    if not is_valid_group_shape(group.array):
        raise ValueError('group is invalid shape')

    if is_col(group.array):
        return check_and_fill_group_with_one_missing(group)
    elif is_row(group.array):
        return check_and_fill_group_with_one_missing(group)
    elif is_square_array(group.array):
        return check_and_fill_group_with_one_missing(group)


def check_and_fill_group_with_one_missing(group: Group) -> Group:
    if len(group.array[group.array == 0]) == 1:
        for i in range(1, group.array.size + 1):
            if i not in group:
                np.place(group.array, group.array == 0, i)
                break
    return group


def convert_to_puzzle(puzzle: SudokuPuzzle | Board) -> SudokuPuzzle:
    if isinstance(puzzle, SudokuPuzzle):
        return puzzle
    else:
        return SudokuPuzzle(puzzle)


@define
class SudokuSolver:
    puzzle: SudokuPuzzle = field(converter=convert_to_puzzle, repr=lambda p: f'\n{repr(p.board)}\nsolved={p.is_solved}')
    timeout: int = field(default=10, eq=False, repr=False)

    @property
    def is_solved(self):
        return self.puzzle.is_solved

    @property
    def num_empty_cells(self):
        return self.puzzle.num_empty_cells

    def solve_hidden_values_single(self):
        for row in self.puzzle.rows:
            cells_with_hidden_values = self.puzzle.get_hidden_values_of_group(row)
            for cell in cells_with_hidden_values:
                self.puzzle.put_cell(cell)

        for col in self.puzzle.cols:
            cells_with_hidden_values = self.puzzle.get_hidden_values_of_group(col)
            for cell in cells_with_hidden_values:
                self.puzzle.put_cell(cell)

        for sq in self.puzzle.squares:
            cells_with_hidden_values = self.puzzle.get_hidden_values_of_group(sq)
            for cell in cells_with_hidden_values:
                self.puzzle.put_cell(cell)

    def solve_groups_with_one_missing(self):
        original_puzzle = self.puzzle
        potentially_solved_puzzle = solve_simple_board(original_puzzle)
        logging.debug(f'{original_puzzle=}')
        logging.debug(f'{potentially_solved_puzzle=}')

        while original_puzzle != potentially_solved_puzzle:
            original_puzzle = potentially_solved_puzzle
            potentially_solved_puzzle = solve_simple_board(original_puzzle)
            logging.debug(f'{original_puzzle=}')
            logging.debug(f'{potentially_solved_puzzle=}')

        self.puzzle = potentially_solved_puzzle

    def solve_cells_with_one_possibility(self):
        for coord in self.puzzle.get_empty_cell_coords():
            cell = Cell(coord[0], coord[1], 0)
            possible_cell_values = self.puzzle.get_possible_cell_values(cell)
            if possible_cell_values.size == 1:
                self.puzzle.put_cell(cell, possible_cell_values[0])

    def solve(self):
        timer = time()
        num_empty_cells_prev = 0
        num_empty_cells_current = self.num_empty_cells

        while ((num_empty_cells_prev != num_empty_cells_current)
               and (time() - timer < self.timeout)
               and (self.is_solved is False)):
            num_empty_cells_prev = num_empty_cells_current

            self.solve_groups_with_one_missing()
            self.solve_hidden_values_single()
            self.solve_cells_with_one_possibility()

            num_empty_cells_current = self.num_empty_cells
            logging.info(f'board: {self.puzzle.board}')
            logging.info(f'empty cells: {self.num_empty_cells}')
        return self
