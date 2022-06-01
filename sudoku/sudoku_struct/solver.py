from sudoku.sudoku_struct.board import SudokuBoardStruct
from attrs import define, field


@define
class SudokuSolverStruct:
    board: SudokuBoardStruct = field(repr=lambda b: f'\n{repr(b.value_array)}\nsolved={b.is_solved}')