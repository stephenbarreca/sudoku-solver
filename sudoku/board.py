import numpy as np
from attrs import cmp_using, define, field
from numpy.typing import NDArray

from sudoku.cell import Cell

cell_dtype = [
    ('row', 'int'), ('col', 'int'), ('value', 'int'), ('candidates', np.ndarray)
]

def convert_to_struct_cell_array(arr):
    if isinstance(arr[0][0], int):
        rows = []
        for r, row in enumerate(arr):
            row_array = []
            for c, val in enumerate(row):
                row_array.append((r, c, val, np.array([], dtype=int)))
            rows.append(np.array(row_array, dtype=cell_dtype))
        return np.array(rows)
    else:
        return arr

@define
class SudokuBoard:
    struct_cell_array: NDArray[NDArray[cell_dtype]] = field(repr=True, converter=np.array)

    # def __attrs_post_init__(self):
    #     self.cell_array = self._make_cell_array_from_value_array()

    def __array__(self):
        return self.value_array

    @classmethod
    def from_value_array(cls, arr: NDArray[NDArray[int]]):
        return cls(convert_to_struct_cell_array(arr))

    @property
    def value_array(self):
        return self.struct_cell_array['value']

    def get_cell(self, row: int, col: int) -> NDArray[cell_dtype]:
        return self.struct_cell_array[row][col]

    def get_empty_cells(self) -> NDArray[cell_dtype]:
        return self.struct_cell_array[self.value_array == 0]

    def get_cell_value(self, row:int, col: int) -> int:
        return self.struct_cell_array[row][col]['value']

    def set_cell_value(self, row:int, col: int, value: int):
        self.struct_cell_array[row][col]['value'] = value
        if value != 0:
            self.struct_cell_array[row][col]['candidates'] = np.array([value])

    def get_cell_candidates(self, row: int, col: int) -> NDArray[int]:
        return self.get_cell(row, col)['candidates']

    def set_cell_candidates(self,  row: int, col: int, candidates: list[int] | NDArray[int]):
        if isinstance(candidates, list):
            candidates = np.array(candidates)
        self.struct_cell_array[row][col]['candidates'] = candidates
        if len(self.get_cell_candidates(row, col)) == 1:
            self.set_cell_value(row, col, candidates[0])

    def refine_cell_candidates(self, row: int, col: int, candidates: list[int] | NDArray[int]):
        old_cell_value = self.struct_cell_array[row][col]['value']
        old_candidates = self.struct_cell_array[row][col]['candidates']
        if isinstance(candidates, list):
            candidates = np.array(candidates)
        if len(old_candidates) == 0:
            self.set_cell_candidates(row, col, candidates)
        else:
            self.set_cell_candidates(row, col, np.setdiff1d(old_candidates, candidates))

    def update_value_array(self):
        pass

    def _make_cell_array_from_value_array(self):
        return np.array(
            [
                [Cell(r, c, val) for c, val in enumerate(row)]
                for r, row in enumerate(self.value_array)
            ]
        )

    def _make_value_array_from_cell_array(self):
        return np.array(
            [
                [self.get_cell(r, c).value for c in range(len(row))]
                for r, row in enumerate(self.cell_array)
            ]
        )


def convert_to_sudoku_board(board) -> SudokuBoard:
    if isinstance(board, SudokuBoard):
        return board
    return SudokuBoard.from_value_array(board)
