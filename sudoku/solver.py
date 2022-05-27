from typing import Sequence, Type

import numpy as np

from sudoku.validators.array_validators import is_col, is_row, is_square
from sudoku.validators.board_validators import is_valid_board_size
from sudoku.validators.group_validators import is_valid_group_shape
from .constants import DEFAULT_SUDOKU_SIZE

Board = np.ndarray | Sequence[np.ndarray | Sequence[int]]

def fill_group_simple_case(arr: np.ndarray) -> np.ndarray:
    """check if only 1 number is missing in the group. if it is fill it. """
    if not is_valid_group_shape(arr):
        raise ValueError('group is invalid shape')

    zero_array = arr == 0

    if is_col(arr):
        return fill_simple_case_col(arr)
    elif is_row(arr):
        return fill_simple_case_row(arr)
    elif is_square(arr):
        return fill_simple_case_square(arr)


def fill_simple_case_col(arr: np.ndarray) -> np.ndarray:
    return arr


def fill_simple_case_row(arr: np.ndarray) -> np.ndarray:
    return arr


def fill_simple_case_square(arr: np.ndarray) -> np.ndarray:
    return arr


class SudokuSolver:
    """
    Sudoku puzzle solver
    """
    dtype: Type[np.number] = np.uint

    def __init__(self, board: Board, *, size=None):
        """"""
        if size is None:
            size = len(board[0])

        if is_valid_board_size(size) is False:
            raise ValueError(f'Invalid puzzle size: {size}')

        self._size = size
        self._square_group_side_len = int(np.sqrt(size))
        self.board = np.array(board, dtype=self.dtype)

    @property
    def size(self):
        return self._size

    @property
    def square_group_side_len(self):
        return self._square_group_side_len

    @property
    def square_group_shape(self):
        len_side = self.square_group_side_len
        return len_side, len_side

    @property
    def cols(self) -> list[np.ndarray]:
        return list(np.transpose(self.board))

    @property
    def rows(self) -> list[np.ndarray]:
        return list(self.board)

    @property
    def squares(self) -> list[np.ndarray]:
        return self._make_square_groups()

    def _make_square_groups(self):
        groups = []
        for g_corner_row in range(0, self.size, self.square_group_side_len):
            for g_corner_col in range(0, self.size, self.square_group_side_len):
                group_arr = []
                for row_num in range(g_corner_row, g_corner_row + self.square_group_side_len):
                    group_row = self.board[row_num][g_corner_col: g_corner_col + self.square_group_side_len]
                    group_arr.append(group_row)
                groups.append(np.array(group_arr, dtype=self.dtype))
        return groups

    @classmethod
    def from_cols(cls, cols: Board) -> 'SudokuSolver':
        arr = np.array(cols, dtype=cls.dtype)
        arr = np.transpose(arr)
        cls(arr)

    @classmethod
    def from_rows(cls, rows: Board) -> 'SudokuSolver':
        return cls(rows)

    @classmethod
    def from_squares(cls, squares: Board) -> 'SudokuSolver':
        pass