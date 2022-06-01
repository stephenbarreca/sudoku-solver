import pytest
from sudoku.sudoku_struct.board import SudokuBoardStruct

@pytest.fixture()
def board(board_value_list):
    return SudokuBoardStruct(board_value_list)