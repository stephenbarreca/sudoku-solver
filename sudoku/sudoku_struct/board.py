from math import isqrt

import numpy as np
from attrs import define, field
from numpy.typing import NDArray

from sudoku.sudoku_struct.cell import CellArray

cell_dtype = [
    ('row', 'int'), ('col', 'int'), ('value', 'int'), ('candidates', np.ndarray)
]

BoardValues = NDArray[NDArray[np.int]]
BoardArray = NDArray[NDArray[any]] | CellArray
BoardLike = list[list[any]] | list[NDArray[any]] | BoardArray
SqrNDArray = NDArray[NDArray[NDArray[any]]]
SqrCellArray = NDArray[NDArray[NDArray[cell_dtype]]]
SqrBoardArray = SqrNDArray | SqrCellArray


def convert_to_struct_cell_array(arr: BoardLike):
    if isinstance(arr, CellArray):
        return arr
    elif isinstance(arr[0][0], int):
        rows = []
        for r, row in enumerate(arr):
            row_array = []
            for c, val in enumerate(row):
                row_array.append((r, c, val, np.array([], dtype=int)))
            rows.append(np.array(row_array, dtype=cell_dtype))
        return np.array(rows).view(CellArray)
    else:
        return arr.view(CellArray)


def _make_squares_from_ndarray(board: BoardLike) -> SqrBoardArray:
    board_size = len(board[0])
    square_size = isqrt(board_size)
    groups = []

    for g_corner_row in range(0, board_size, square_size):
        for g_corner_col in range(0, board_size, square_size):
            group_arr = []
            for row_num in range(g_corner_row, g_corner_row + square_size):
                group_row = board[row_num][g_corner_col: g_corner_col + square_size]
                group_arr.append(group_row)
            groups.append(group_arr)
    return np.array(groups)


def _make_squares_from_cell_array(board: CellArray) -> SqrCellArray:
    board_size = len(board[0])
    square_size = isqrt(board_size)
    groups = []

    for g_corner_row in range(0, board_size, square_size):
        for g_corner_col in range(0, board_size, square_size):
            group = board[np.where((g_corner_row <= board['row']) & (board['row'] < g_corner_row + square_size)
                                   & (g_corner_col <= board['col']) & (board['col'] < g_corner_col + square_size))]
            groups.append(group.reshape(square_size, square_size))
    return np.array(groups)


def make_squares(board: BoardLike) -> SqrCellArray | SqrNDArray:
    if isinstance(board, CellArray):
        return _make_squares_from_cell_array(board)
    else:
        return _make_squares_from_ndarray(board)


@define
class SudokuBoardStruct:
    cell_array: CellArray | NDArray[NDArray[cell_dtype]] = field(repr=True, converter=convert_to_struct_cell_array)

    _side_len: int = field(init=False, eq=False, repr=False)
    _square_side_len: int = field(init=False, eq=False, repr=False)
    _square_shape: tuple[int, int] = field(init=False, eq=False, repr=False)

    def __attrs_post_init__(self):
        self._side_len = len(self.cell_array[0])
        self._square_side_len = isqrt(self.side_len)
        self._square_shape = (self.square_side_len, self.square_side_len)

    def __array__(self):
        return self.cell_array

    @classmethod
    def from_value_array(cls, arr: NDArray[NDArray[int]]):
        return cls(convert_to_struct_cell_array(arr))

    @property
    def side_len(self) -> int:
        return self._side_len

    @property
    def square_side_len(self) -> int:
        return isqrt(self.side_len)

    @property
    def square_shape(self) -> tuple[int, int]:
        return self._square_shape

    @property
    def value_array(self) -> BoardValues:
        return self.get_value_array()

    @property
    def cols(self) -> CellArray:
        return self.cell_array.transpose()

    @property
    def rows(self) -> CellArray:
        return self.cell_array

    @property
    def squares(self) -> SqrCellArray:
        return make_squares(self.board)

    @property
    def is_solved(self):
        value_array = self.value_array
        if self.count_empty_cell() > 0:
            return False
        for group_types in [self.rows, self.cols, self.squares]:
            for groups in group_types:
                for g in groups:
                    if np.setdiff1d(value_array, g.ravel()).size != 0:
                        return False
        return True

    def count_empty_cell(self) -> int:
        return self.get_empty_cells().size

    def get_value_array(self) -> BoardValues:
        return self.cell_array['value']

    def get_empty_cells(self) -> NDArray[cell_dtype]:
        return self.cell_array[self.value_array == 0]

    def get_cell(self, row: int, col: int) -> NDArray[cell_dtype]:
        return self.cell_array[row][col]

    def set_cell(self, row: int, col: int, value: int = None, candidates: NDArray = None):
        if value is not None:
            self.cell_array[row][col]['value'] = value
        if candidates is not None:
            self.cell_array[row][col]['candidates'] = candidates

    def get_cell_value(self, row: int, col: int) -> int:
        return self.get_cell(row, col)['value']

    def set_cell_value(self, row: int, col: int, value: int):
        candidates = None
        if value != 0:
            candidates = np.array([value])
        self.set_cell(row, col, value, candidates)

    def get_cell_candidates(self, row: int, col: int):
        return self.get_cell(row, col)['candidates']

    def set_cell_candidates(self, row: int, col: int, candidates: list[int] | NDArray[int]):
        if isinstance(candidates, list):
            candidates = np.array(candidates)
        value = None
        if len(candidates) == 1:
            value = candidates[0]
        self.set_cell(row, col, value, candidates)

    def refine_cell_candidates(self, row: int, col: int, candidates: list[int] | NDArray[int]):
        old_candidates = self.get_cell_candidates(row, col)
        if isinstance(candidates, list):
            candidates = np.array(candidates)
        if len(old_candidates) == 0:
            self.set_cell_candidates(row, col, candidates)
        else:
            self.set_cell_candidates(row, col, np.setdiff1d(old_candidates, candidates))