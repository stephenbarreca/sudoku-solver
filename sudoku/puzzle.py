from typing import Sequence, Type

import numpy as np
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


class SudokuPuzzle:
    """
    Sudoku puzzle solver
    """
    dtype: Type[np.number] = np.uint

    class Row(np.ndarray):
        pass

    class Col(np.ndarray):
        pass

    class Square(np.ndarray):
        pass

    def __init__(self, board: Board, *, size=None):
        """"""
        if size is None:
            size = len(board[0])

        if is_valid_board_size(size) is False:
            raise ValueError(f'Invalid puzzle size: {size}')

        self._size = size
        self._square_group_side_len = int(np.sqrt(size))
        self.board = np.array(board, dtype=self.dtype)

    def __repr__(self):
        return repr(self.board)

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
    def cols(self) -> list[Col]:
        return [c.view(self.Col) for c in rows_to_cols(self.board)]

    @property
    def rows(self) -> list[Row]:
        return [r.view(self.Row) for r in rows_to_cols(self.board)]

    @property
    def squares(self) -> list[np.ndarray]:
        return [s.view(self.Square) for s in self._make_square_groups()]

    def _make_square_groups(self) -> list[NDArray[int]]:
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
    def from_cols(cls, cols: list[NDArray[int]]) -> 'SudokuPuzzle':
        arr = np.array(cols, dtype=cls.dtype)
        arr = np.transpose(arr)
        cls(arr)

    @classmethod
    def from_rows(cls, rows: list[NDArray[int]]) -> 'SudokuPuzzle':
        return cls(rows)

    @classmethod
    def from_squares(cls, squares: list[NDArray[int]]) -> 'SudokuPuzzle':
        pass

    @property
    def is_solved(self):
        board = self.board
        if len(board[board == 0]) > 0:
            return False
        return True