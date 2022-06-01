import numpy as np
import pytest

from sudoku.puzzle import SudokuPuzzle, Cell
from sudoku.groups import ColArray, RowArray, SquareArray, Col, Row, Square
from sudoku.validators.array_validators import is_nd_array, is_square_array
from tests.board_lists import solution_list_2x2_a, solution_list_3x3_a


@pytest.mark.parametrize('puzzle_in', [
    SudokuPuzzle(solution_list_2x2_a),
    SudokuPuzzle(solution_list_3x3_a)
])
class TestPuzzleGroups:
    def test_convert_board_to_cols(self, puzzle_in: SudokuPuzzle):
        cols = puzzle_in.cols
        for j, col in enumerate(cols):
            assert isinstance(col, Col)
            assert is_nd_array(col.array, 1)
            np.array_equal(cols, col)

    def test_convert_board_to_rows(self, puzzle_in):
        rows = puzzle_in.rows
        for row in rows:
            assert isinstance(row, Row)
            assert is_nd_array(row.array, 1)

    def test_convert_board_to_squares(self, puzzle_in):
        squares = puzzle_in.squares
        for sq in squares:
            assert isinstance(sq, Square)
            assert is_square_array(sq.array)

    def test_from_cols(self, puzzle_in):
        cols = puzzle_in.cols
        puzzle_out = SudokuPuzzle.from_cols(cols)
        assert isinstance(puzzle_out, SudokuPuzzle)
        assert puzzle_in == puzzle_out
        assert puzzle_out.is_solved

    def test_from_rows(self, puzzle_in):
        rows = puzzle_in.rows
        puzzle_out = SudokuPuzzle.from_rows(rows)
        assert isinstance(puzzle_out, SudokuPuzzle)
        assert puzzle_in == puzzle_out
        assert puzzle_out.is_solved

    def test_from_squares(self, puzzle_in):
        squares = puzzle_in.squares
        puzzle_out = SudokuPuzzle.from_squares(squares)
        assert isinstance(puzzle_out, SudokuPuzzle)
        assert puzzle_in == puzzle_out
        assert puzzle_out.is_solved

    def test_get_square_from_cell(self, puzzle_in: SudokuPuzzle):
        squares = puzzle_in.squares
        square_correct = puzzle_in.squares[0]
        coords = (0, 0)
        cell = puzzle_in.get_cell(*coords)

        square_returned = puzzle_in.get_square_from_cell(cell)

        assert square_returned == square_correct
