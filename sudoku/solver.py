import logging
from copy import deepcopy
from time import time

import numpy as np
from attrs import define, field
from numpy.typing import NDArray

from sudoku.puzzle import Board, SudokuPuzzle
from sudoku.cell import Cell
from sudoku.groups import Group
from sudoku.validators import is_square_array, is_valid_group_shape
from sudoku.validators.group_validators import is_col, is_row

logger = logging.getLogger(__name__)

def solve_simple_board(board: SudokuPuzzle):
    board = deepcopy(board)
    rows = [check_and_fill_group_with_one_missing(row) for row in board.rows]
    board = SudokuPuzzle.from_rows(rows)

    cols = [check_and_fill_group_with_one_missing(col) for col in board.cols]
    board = SudokuPuzzle.from_cols(cols)

    squares = [check_and_fill_group_with_one_missing(square) for square in board.squares]
    board = SudokuPuzzle.from_squares(squares)

    return board


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
    puzzle: SudokuPuzzle = field(converter=convert_to_puzzle, repr=lambda p: f'\n{repr(p.board_array)}\nsolved={p.is_solved}')
    timeout: int = field(default=10, eq=False, repr=False)

    @property
    def is_solved(self):
        return self.puzzle.is_solved

    @property
    def num_empty_cells(self):
        return self.puzzle.num_empty_cells

    def solve_hidden_values_single(self):
        for row in self.puzzle.rows:
            cells_with_hidden_values = self.puzzle.get_single_hidden_values_of_group(row)

        for col in self.puzzle.cols:
            cells_with_hidden_values = self.puzzle.get_single_hidden_values_of_group(col)

        for sq in self.puzzle.squares:
            cells_with_hidden_values = self.puzzle.get_single_hidden_values_of_group(sq)

    def solve_groups_with_one_missing(self):
        original_puzzle = deepcopy(self.puzzle.board.struct_cell_array)
        potentially_solved_puzzle = np.array([1,2,3])
        group_types = [self.puzzle.rows, self.puzzle.cols, self.puzzle.squares]

        while not self.is_solved and not np.array_equal(original_puzzle, potentially_solved_puzzle):
            original_puzzle = potentially_solved_puzzle
            for groups in group_types:
                for group in groups:
                    missing_row_values = self.puzzle.get_missing_values_of_group(group['value'])
                    if len(missing_row_values) == 1:
                        empty_cell = group[group['value'] == 0][0]
                        self.puzzle.board.set_cell_value(empty_cell['row'], empty_cell['col'], missing_row_values[0])

            potentially_solved_puzzle = deepcopy(self.puzzle.board.struct_cell_array['value'])
            logger.debug(f'{original_puzzle=}')
            logger.debug(f'{potentially_solved_puzzle=}')
        return

    def solve_cells_with_one_possibility(self):
        for row, col in self.puzzle.get_empty_cells()[['row', 'col']]:
            self.puzzle.determine_and_update_cell_candidates(row, col)

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
            logger.info(f'board: {self.puzzle.board_array}')
            logger.info(f'empty cells: {self.num_empty_cells}')
        return self
