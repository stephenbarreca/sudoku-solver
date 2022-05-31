from typing import Sequence
from math import isqrt
import numpy as np
import attrs
from attrs import define, field, cmp_using
from numpy.typing import NDArray

from sudoku.validators import is_valid_board_size

Board = np.ndarray | Sequence[np.ndarray | Sequence[int]]


def rows_to_cols(rows: np.ndarray) -> np.ndarray:
    return np.transpose(rows)


def make_square(arr: np.array) -> np.array:
    row_len = int(np.sqrt(arr.size))
    return arr.reshape((row_len, row_len))


def make_line(arr: NDArray[int]) -> NDArray[int]:
    return arr.reshape(arr.size)


class Row(np.ndarray):
    pass


class Col(np.ndarray):
    pass


class Square(np.ndarray):
    pass


@define(frozen=True)
class Cell:
    row: int = field(eq=False)
    col: int = field(eq=False)
    value: int = field(eq=True)


@define(slots=False)
class SudokuPuzzle:
    """
    Sudoku puzzle solver
    """
    # dtype: Type[np.number] = np.uint
    board: NDArray[int] = field(eq=cmp_using(eq=np.array_equal), converter=np.array)

    size: int = field(init=False, eq=False, repr=False)
    square_group_side_len: int = field(init=False, eq=False, repr=False)
    square_group_shape: tuple[int, int] = field(init=False, eq=False, repr=False)
    coord_array: NDArray[NDArray[NDArray[int]]] = field(init=False, eq=False, repr=False)
    value_range: NDArray[int] = field(init=False, eq=False, repr=False)

    def __attrs_post_init__(self):
        self.size = len(self.board[0])
        self.validate_board_size()

        self.square_group_side_len = int(np.sqrt(self.size))
        self.square_group_shape = (self.square_group_side_len, self.square_group_side_len)
        self.coord_array = self._make_coord_array()
        self.value_range = np.array(range(1, self.size+1))

    def validate_board_size(self):
        if is_valid_board_size(self.size) is False:
            raise ValueError(f'Invalid puzzle size: {self.size}')

    @property
    def cols(self) -> list[Col]:
        return [c.view(Col) for c in rows_to_cols(self.board)]

    @property
    def rows(self) -> list[Row]:
        return [r.view(Row) for r in rows_to_cols(self.board)]

    @property
    def squares(self) -> list[np.ndarray]:
        return [s.view(Square) for s in self._make_square_groups()]

    def _make_coord_array(self) -> NDArray[NDArray[NDArray]]:
        return np.array([[(i, j) for j, col in enumerate(row)] for i, row in enumerate(self.board)])

    def _make_square_groups(self) -> list[NDArray[int]]:
        groups = []
        for g_corner_row in range(0, self.size, self.square_group_side_len):
            for g_corner_col in range(0, self.size, self.square_group_side_len):
                group_arr = []
                for row_num in range(g_corner_row, g_corner_row + self.square_group_side_len):
                    group_row = self.board[row_num][g_corner_col: g_corner_col + self.square_group_side_len]
                    group_arr.append(group_row)
                groups.append(np.array(group_arr))
        return groups

    def get_cell(self, row: int, col: int) -> Cell:
        return Cell(row, col, self.board[row][col])

    def put_cell(self, cell, value: int = None):
        if value is None:
            value = cell.value
        self.board[cell.row][cell.col] = value

    def get_row_from_cell(self, cell: Cell) -> NDArray:
        return self.board[cell.row]

    def get_col_from_cell(self, cell: Cell) -> NDArray:
        return self.cols[cell.col]

    def get_cell_square(self, cell: Cell) -> NDArray:
        pass

    def get_missing_values_of_group(self, group: NDArray):
        return np.setdiff1d(self.value_range, group)

    def get_possible_cell_values(self, cell: Cell) -> NDArray:
        if cell.value != 0:
            return np.array([cell.value])

        row = self.get_row_from_cell(cell)
        col = self.get_col_from_cell(cell)
        row_col = np.union1d(row, col)

        row_col_values = self.get_missing_values_of_group(row_col)

        return row_col_values

    def get_empty_cell_coords(self) -> NDArray[NDArray[int]]:
        return self.coord_array[self.board == 0]

    @classmethod
    def from_cols(cls, cols: list[NDArray[int]]) -> 'SudokuPuzzle':
        arr = np.array(cols)
        arr = np.transpose(arr)
        return cls(arr)

    @classmethod
    def from_rows(cls, rows: list[NDArray[int]]) -> 'SudokuPuzzle':
        return cls(rows)

    @classmethod
    def from_squares(cls, squares: list[NDArray[int]]) -> 'SudokuPuzzle':
        groups_per_row = isqrt(len(squares))
        square_rows = []
        for i in range(0, len(squares), groups_per_row):
            square_row = np.hstack(squares[i: i+groups_per_row])
            square_rows.append(square_row)

        board = np.vstack(square_rows)
        return cls(board)

    @property
    def is_solved(self):
        board = self.board
        if len(board[board == 0]) > 0:
            return False
        return True
