import numpy as np
import pytest

from sudoku.sudoku_struct.board import _make_squares_from_ndarray, SudokuBoardStruct, make_squares
from sudoku.sudoku_struct.cell import CellArray
from sudoku.validators import is_square_array
from ..board_lists import solution_list_2x2_a, solution_list_3x3_a


@pytest.fixture()
def board(value_list):
    return SudokuBoardStruct.from_value_array(value_list)

class TestSudokuBoardStruct:
    def test_from_values(self, board):
        assert isinstance(board, SudokuBoardStruct)
        assert isinstance(board.cell_array, CellArray)

    def test_from_values_populates_cell_fields(self, value_list):
        board = SudokuBoardStruct.from_value_array(value_list)
        cell = board.cell_array[0][0]
        for k in ['row', 'col', 'value']:
            assert isinstance(cell[k], np.int32)
        assert isinstance(cell['candidates'], np.ndarray)
        assert cell['value'] == value_list[0][0]

    def test_value_array(self, value_list):
        board = SudokuBoardStruct.from_value_array(value_list)
        value_array = np.array(value_list)
        assert np.array_equal(value_array, board.value_array)

    def test_get_array(self, board):
        cell = board.get_cell(2, 2)
        assert np.array_equal(cell[['row', 'col', 'value']], board.cell_array[2][2][['row', 'col', 'value']])
        assert np.array_equal(cell['candidates'], board.cell_array[2][2]['candidates'])

    def test_get_cell_value(self, board):
        value = board.get_cell_value(2, 2)
        assert value == board.value_array[2][2]

    def test_make_squares_from_ndarray_using_list(self, value_list):
        squares = _make_squares_from_ndarray(value_list)
        for sq in squares:
            assert is_square_array(sq)
        assert squares[0][0][0] == value_list[0][0]

    def test_make_squares_from_ndarray_using_cell_array(self, board):
        squares = _make_squares_from_ndarray(board.cell_array)
        for sq in squares:
            assert is_square_array(sq)

    def test_make_squares_from_cell_array(self, board):
        squares = make_squares(board.cell_array)
        for sq in squares:
            assert is_square_array(sq)
        cell = squares[0][0][0]
        assert cell['row'] == 0
        assert cell['col'] == 0
        assert cell['value'] == board.get_cell_value(0, 0)
        assert np.array_equal(cell['candidates'], board.get_cell_candidates(0, 0))

    def test_is_solved(self):
        assert False