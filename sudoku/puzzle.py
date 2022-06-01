from math import isqrt
from typing import Sequence

import numpy as np
from attrs import cmp_using, define, evolve, field
from numpy.typing import NDArray

from sudoku.board import cell_dtype, convert_to_sudoku_board, SudokuBoard
from sudoku.cell import Cell
from sudoku.groups import Col, Row, Square
from sudoku.validators import is_valid_board_size

Board = np.ndarray | Sequence[np.ndarray | Sequence[int]]

dtype_coord = [('row', 'int'), ('col', 'int')]


def rows_to_cols(rows: np.ndarray) -> np.ndarray:
    return np.transpose(rows)


def make_square(arr: np.array) -> np.array:
    row_len = int(np.sqrt(arr.size))
    return arr.reshape((row_len, row_len))


def make_line(arr: NDArray[int]) -> NDArray[int]:
    return arr.reshape(arr.size)


def make_squares(board, board_size, square_size) -> NDArray[NDArray[cell_dtype]]:
    groups = []
    for g_corner_row in range(0, board_size, square_size):
        for g_corner_col in range(0, board_size, square_size):
            group = board[np.where((g_corner_row <= board['row']) & (board['row'] < g_corner_row + square_size)
                                   & (g_corner_col <= board['col']) & (board['col'] < g_corner_col + square_size))]
            groups.append(group.reshape(square_size, square_size))
    return np.array(groups)


class PuzzleException(Exception):
    pass


@define(slots=False)
class SudokuPuzzle:
    """
    Sudoku puzzle solver
    """
    # dtype: Type[np.number] = np.uint
    board: SudokuBoard = field(eq=cmp_using(eq=np.array_equal), converter=convert_to_sudoku_board)

    size: int = field(init=False, eq=False, repr=False)
    square_group_side_len: int = field(init=False, eq=False, repr=False)
    square_group_shape: tuple[int, int] = field(init=False, eq=False, repr=False)
    value_range: NDArray[int] = field(init=False, eq=False, repr=False)

    def __attrs_post_init__(self):
        self.size = len(self.board.struct_cell_array[0])
        self.validate_board_size()

        self.square_group_side_len = int(np.sqrt(self.size))
        self.square_group_shape = (self.square_group_side_len, self.square_group_side_len)
        self.value_range = np.array(range(1, self.size + 1))

    def validate_board_size(self):
        if is_valid_board_size(self.size) is False:
            raise ValueError(f'Invalid puzzle size: {self.size}')

    @property
    def board_array(self):
        return self.board.value_array

    @property
    def cols(self) -> NDArray[NDArray[cell_dtype]]:
        return self.board.struct_cell_array.transpose()

    @property
    def rows(self) -> NDArray[NDArray[cell_dtype]]:
        return self.board.struct_cell_array

    @property
    def squares(self) -> NDArray[NDArray[cell_dtype]]:
        return make_squares(self.board.struct_cell_array, self.size, self.square_group_side_len)

    @property
    def coord_array(self) -> NDArray[NDArray[NDArray]]:
        return self.board.struct_cell_array[['row', 'col']]

    @property
    def coord_array_squares(self):
        return np.array(make_squares(self.coord_array, self.size, self.square_group_side_len))

    def get_cell(self, row: int, col: int) -> NDArray[cell_dtype]:
        return self.board.get_cell(row, col)

    def put_cell(self, cell, value: int = None):
        if value is None:
            value = cell.value
        self.board.set_cell_value(cell.row, cell.col, value)

    def get_row_from_cell(self, row: int, col: int) -> Row:
        return self.rows[row]

    def get_cells_from_row(self, row: int) -> NDArray[Cell]:
        return self.board.cell_array[row]

    def get_col_from_cell(self, row: int, col: int) -> Col:
        return self.cols[col]

    def get_cells_from_col(self, col: int) -> NDArray[Cell]:
        return self.board.cell_array.transpose()[col]

    def get_square_from_cell(self, row: int, col: int) -> Square:
        for cells in self.squares:
            if len(cells[np.where((cells['row'] == row) & (cells['col'] == col))]) == 1:
                return cells

        return

    def get_cells_from_square(self, sq: int) -> NDArray[Cell]:
        coords_squares = np.array(make_squares(self.board.cell_array, self.size, self.square_group_side_len))
        return coords_squares[sq.index].flatten()

    def get_missing_values_of_group(self, value_arr: NDArray[int]):
        return np.setdiff1d(self.value_range, value_arr)

    def get_single_hidden_values_of_group(self, cells: NDArray[cell_dtype]) -> list[Cell]:
        missing_group_values = self.get_missing_values_of_group(cells)
        empty_group_cells = cells[cells['value'] == 0]
        cells_with_possible_values = list(zip(
            empty_group_cells,
            [self._determine_cell_candidates_values_from_group_intersection(c['row'], c['col']) for c in empty_group_cells]
        ))
        for cell, candidates in cells_with_possible_values:
            self.board.refine_cell_candidates(cell['row'], cell['col'], candidates)
        cells_with_hidden_values: list[cell_dtype] = []
        for v in missing_group_values:
            cells_with_v = [cell for cell, values in cells_with_possible_values if v in values]
            if len(cells_with_v) == 1:
                cell = cells_with_v[0]
                self.board.set_cell_value(cell['row'], cell['col'], v)
                cells_with_hidden_values.append(self.board.get_cell(cell['row'], cell['col']))
        return cells_with_hidden_values

    def _determine_cell_candidates_values_from_group_intersection(self, row: int, col: int) -> NDArray:
        if self.board.get_cell_value(row, col) != 0:
            return np.array(self.board.struct_cell_array[row][col]['value'])

        row_array = self.get_row_from_cell(row, col)
        col_array = self.get_col_from_cell(row, col)
        square_array = self.get_square_from_cell(row, col)
        row_col = np.union1d(row_array['value'], col_array['value'])
        row_col_square = np.union1d(row_col, square_array['value'])
        missing_values = self.get_missing_values_of_group(row_col_square)
        if len(missing_values) == 0:
            raise PuzzleException('cell has no possible values')
        return missing_values

    def determine_and_update_cell_candidates(self, row: int, col: int) -> NDArray[int]:
        candidates = self._determine_cell_candidates_values_from_group_intersection(row, col)
        self.board.refine_cell_candidates(row, col, candidates)
        if len(self.board.get_cell_candidates(row, col)) == 1:
            return self.board.get_cell_candidates(row, col)
        return self.board.get_cell_candidates(row, col)

    def get_empty_cells(self) -> NDArray[cell_dtype]:
        return self.board.get_empty_cells()

    @property
    def num_empty_cells(self) -> int:
        return self.board_array[self.board_array == 0].size

    @classmethod
    def from_cols(cls, cols: NDArray[NDArray[cell_dtype]]) -> 'SudokuPuzzle':
        return cls(SudokuBoard(cols.transpose()))

    @classmethod
    def from_rows(cls, rows: NDArray[NDArray[cell_dtype]]) -> 'SudokuPuzzle':
        return cls(SudokuBoard(rows))

    @classmethod
    def from_squares(cls, squares: NDArray[NDArray[NDArray[cell_dtype]]]) -> 'SudokuPuzzle':
        groups_per_row = isqrt(len(squares))
        square_rows = []
        for i in range(0, len(squares), groups_per_row):
            square_row = np.hstack(squares[i: i + groups_per_row])
            square_rows.append(square_row)

        board = np.vstack(square_rows)
        return cls(SudokuBoard(board))

    @property
    def is_solved(self):
        board = self.board.struct_cell_array['value']
        if len(board[board == 0]) > 0:
            return False
        for row in self.rows:
            if len(np.setdiff1d(self.value_range, row['value'])) != 0:
                return False
        for col in self.cols:
            if len(np.setdiff1d(self.value_range, col['value'])) != 0:
                return False
        for sq in self.squares:
            if len(np.setdiff1d(self.value_range, sq['value'].ravel())) != 0:
                return False
        return True
