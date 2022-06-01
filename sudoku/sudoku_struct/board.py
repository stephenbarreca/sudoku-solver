from math import isqrt

import numpy as np
from attrs import define, field
from numpy.typing import NDArray

from sudoku.sudoku_struct.cell import CellArray

cell_dtype = [
    ('row', 'int'), ('col', 'int'), ('value', 'int'), ('candidates', np.ndarray)
]

GroupArrayCol = NDArray[cell_dtype]
GroupArrayRow = NDArray[cell_dtype]
GroupArraySquare = NDArray[NDArray[cell_dtype]]
GroupArray = GroupArrayCol | GroupArrayRow | GroupArraySquare

Cols = NDArray[GroupArrayCol]
Rows = NDArray[GroupArrayRow]
Sqrs = NDArray[GroupArraySquare]
Groups = NDArray[GroupArray]

BoardValues = NDArray[NDArray[np.int]]
BoardArray = NDArray[NDArray[any]] | CellArray
BoardLike = list[list[any]] | list[NDArray[any]] | BoardArray

SqrNDArray = NDArray[NDArray[NDArray[any]]]
BoardLikeArraySqr = SqrNDArray | Sqrs

Cell = np.void


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


def _make_squares_from_ndarray(board: BoardLike) -> BoardLikeArraySqr:
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


def _make_squares_from_cell_array(board: CellArray) -> Sqrs:
    board_size = len(board[0])
    square_size = isqrt(board_size)
    groups = []

    for g_corner_row in range(0, board_size, square_size):
        for g_corner_col in range(0, board_size, square_size):
            group = board[np.where((g_corner_row <= board['row']) & (board['row'] < g_corner_row + square_size)
                                   & (g_corner_col <= board['col']) & (board['col'] < g_corner_col + square_size))]
            groups.append(group.reshape(square_size, square_size))
    return np.array(groups)


def make_squares(board: BoardLike) -> Sqrs | SqrNDArray:
    if isinstance(board, CellArray):
        return _make_squares_from_cell_array(board)
    else:
        return _make_squares_from_ndarray(board)


class BoardException(Exception):
    pass


class CellException(Exception):
    pass


@define
class SudokuBoardStruct:
    cell_array: CellArray | NDArray[NDArray[cell_dtype]] = field(repr=True, converter=convert_to_struct_cell_array)

    _side_len: int = field(init=False, eq=False, repr=False)
    _square_side_len: int = field(init=False, eq=False, repr=False)
    _square_shape: tuple[int, int] = field(init=False, eq=False, repr=False)
    _value_range: NDArray[np.int] = field(init=False, eq=False, repr=False)

    def __attrs_post_init__(self):
        self._side_len = len(self.cell_array[0])
        self._square_side_len = isqrt(self.side_len)
        self._square_shape = (self.square_side_len, self.square_side_len)
        self._value_range = np.array(range(1, self.side_len + 1))

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
    def value_range(self):
        return self._value_range

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
    def squares(self) -> Sqrs:
        return make_squares(self.cell_array)

    @property
    def is_solved(self):
        value_array = self.get_value_array()
        if value_array[value_array == 0].size > 0:
            return False
        for groups in [self.rows, self.cols, self.squares]:
            for g in groups:
                if np.setdiff1d(self.value_range, g['value'].ravel()).size != 0:
                    return False
        return True

    def count_empty_cell(self) -> int:
        return self.get_empty_cells().size

    def get_empty_cells(self) -> NDArray[cell_dtype]:
        return self.cell_array[self.value_array == 0]

    def get_value_array(self) -> BoardValues:
        return self.cell_array['value']

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
        if value is not None and value != 0:
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
        return

    def refine_cell_candidates_by_coords(self, row: int, col: int, candidates: list[int] | NDArray[int]):
        if len(candidates) == 0:
            raise CellException('cell has no candidates')
        cell_value = self.get_cell_value(row, col)
        if cell_value != 0:
            self.set_cell_candidates(row, col, np.array([cell_value]))
        else:
            if isinstance(candidates, list):
                candidates = np.array(candidates)
            old_candidates = self.get_cell_candidates(row, col)
            if len(old_candidates) == 0:
                self.set_cell_candidates(row, col, candidates)
            else:
                self.set_cell_candidates(row, col, np.intersect1d(old_candidates, candidates))

    def refine_cell_candidates(self, cell: np.void, candidates: list[int] | NDArray[int]):
        return self.refine_cell_candidates_by_coords(*self.get_cell_coords(cell), candidates=candidates)

    @staticmethod
    def get_cell_coords(cell: np.void) -> np.void:
        return cell[['row', 'col']]

    def get_row_from_coords(self, row: int, col: int) -> GroupArrayRow:
        return self.rows[row]

    def get_row_from_cell(self, cell: np.void) -> GroupArrayRow:
        return self.get_row_from_coords(*self.get_cell_coords(cell))

    def get_col_from_coords(self, row: int, col: int) -> GroupArrayCol:
        return self.cols[col]

    def get_col_from_cell(self, cell: np.void) -> GroupArrayCol:
        return self.get_col_from_coords(*self.get_cell_coords(cell))

    def get_square_from_coords(self, row: int, col: int) -> GroupArraySquare:
        squares = self.squares
        sqr = squares[((squares['row'] == row) & (squares['col'] == col)).any(1).any(1)]
        return sqr

    def get_square_from_cell(self, cell: np.void) -> GroupArraySquare:
        return self.get_square_from_coords(*self.get_cell_coords(cell))

    def get_missing_values_of_group(self, group: GroupArray) -> NDArray[np.int]:
        group_values = group['value']
        return np.setdiff1d(self.value_range, group_values)

    def determine_group_candidates(self, group: GroupArray):
        candidates = self.get_missing_values_of_group(group)
        if candidates.size != 0:
            for cell in group.ravel():
                self.refine_cell_candidates(cell, candidates)


    def determine_group_hidden_candidates_single(self, group: GroupArray):
        missing_values = self.get_missing_values_of_group(group)

        for v in missing_values:
            cells_with_v = [cell for cell in group if v in cell['candidates']]
            if len(cells_with_v) == 1:
                self.set_cell_value(cells_with_v[0]['row'], cells_with_v[0]['col'], v)

    def determine_board_candidates_groupwise(self):
        group_types = [self.rows, self.cols, self.squares]
        for groups in group_types:
            for group in groups:
                self.determine_group_candidates(group)

    def determine_board_hidden_candidates_single(self):
        group_types = [self.rows, self.cols, self.squares]
        for groups in group_types:
            for group in groups:
                self.determine_group_hidden_candidates_single(group)

    def determine_cell_candidates_by_group_intersection(self, cell: np.void, refine_group_cells: bool = True):
        if cell['value'] != 0:
            return cell['candidates']
        row = self.get_row_from_cell(cell)
        col = self.get_col_from_cell(cell)
        square = self.get_square_from_cell(cell)
        if refine_group_cells is True:
            self.determine_group_candidates(row)
            self.determine_group_candidates(col)
            self.determine_group_candidates(square)
        else:
            row_col = np.union1d(row, col)
            row_col_square = np.union1d(row_col, square)
            candidates = self.get_missing_values_of_group(row_col_square)
            self.refine_cell_candidates(cell, candidates)
        return
    def determine_cell_candidates(self, cell: np.void):
        if cell['candidates'].size == 1:
            return
        self.determine_cell_candidates_by_group_intersection(cell)
        if cell['candidates'].size == 1:
            return
        return


def convert_to_board(board: BoardLike | SudokuBoardStruct) -> SudokuBoardStruct:
    if isinstance(board, SudokuBoardStruct):
        return board
    else:
        return SudokuBoardStruct(board)
