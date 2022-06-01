import numpy as np
import pytest

from sudoku.sudoku_struct.board import _make_squares_from_ndarray, make_squares, SudokuBoardStruct
from sudoku.sudoku_struct.cell import CellArray
from sudoku.validators import is_square_array
from ..board_lists import (
    puzzle_list_3x3_easy, puzzle_list_3x3_simple_b1, solution_list_2x2_a, solution_list_3x3_a,
    solution_list_3x3_simple_b,
)

class TestSudokuBoardStruct:
    def test_init_with_value_array(self, board):
        assert isinstance(board, SudokuBoardStruct)
        assert isinstance(board.cell_array, CellArray)

    def test_from_values(self, board):
        assert isinstance(board, SudokuBoardStruct)
        assert isinstance(board.cell_array, CellArray)

    def test_from_values_populates_cell_fields(self, board_value_list):
        board = SudokuBoardStruct.from_value_array(board_value_list)
        cell = board.cell_array[0][0]
        for k in ['row', 'col', 'value']:
            assert isinstance(cell[k], np.int32)
        assert isinstance(cell['candidates'], np.ndarray)
        assert cell['value'] == board_value_list[0][0]

    def test_value_array(self, board_value_list):
        board = SudokuBoardStruct.from_value_array(board_value_list)
        value_array = np.array(board_value_list)
        assert np.array_equal(value_array, board.value_array)

    def test_get_array(self, board):
        cell = board.get_cell(2, 2)
        assert np.array_equal(cell[['row', 'col', 'value']], board.cell_array[2][2][['row', 'col', 'value']])
        assert np.array_equal(cell['candidates'], board.cell_array[2][2]['candidates'])

    def test_get_cell_value(self, board):
        value = board.get_cell_value(2, 2)
        assert value == board.value_array[2][2]

    def test_make_squares_from_ndarray_using_list(self, board_value_list):
        squares = _make_squares_from_ndarray(board_value_list)
        for sq in squares:
            assert is_square_array(sq)
        assert squares[0][0][0] == board_value_list[0][0]

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

    @pytest.mark.parametrize(
        argnames=['board', 'expected'],
        argvalues=[(SudokuBoardStruct(solution_list_2x2_a), True),
                   (SudokuBoardStruct(solution_list_3x3_a), True),
                   (SudokuBoardStruct(solution_list_3x3_simple_b), True),
                   (SudokuBoardStruct(puzzle_list_3x3_simple_b1), False),
                   (SudokuBoardStruct(puzzle_list_3x3_easy), False)],
        ids=['Solved 2x2 A',
             'Solved 3x3 A',
             'Solved 3x3 Simple',
             'Unsolved 3x3 Simple',
             'Unsolved 3x3 Easy', ]
    )
    def test_is_solved(self, board, expected):
        assert board.is_solved is expected
