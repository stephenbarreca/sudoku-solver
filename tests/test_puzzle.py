import pytest

from sudoku.puzzle import SudokuPuzzle, Row, Col,Square
from sudoku.validators.array_validators import is_n_dimensional, is_square
from tests.conftest import solution_2x2_a, solution_3x3_a


@pytest.mark.parametrize('puzzle_in', [
    SudokuPuzzle(solution_2x2_a),
    SudokuPuzzle(solution_3x3_a)
])
class TestPuzzleGroups:
    def test_convert_board_to_cols(self, puzzle_in: SudokuPuzzle):
        cols = puzzle_in.cols
        for j, col in enumerate(cols):
            assert isinstance(col, Col)
            assert is_n_dimensional(col, 1)
            for i in range(len(cols)):
                assert col[i] == puzzle_in.board[i][j]

    def test_convert_board_to_rows(self, puzzle_in):
        rows = puzzle_in.rows
        for row in rows:
            assert isinstance(row, Row)
            assert is_n_dimensional(row, 1)

    def test_convert_board_to_squares(self, puzzle_in):
        squares = puzzle_in.squares
        for sq in squares:
            assert isinstance(sq, Square)
            assert is_square(sq)

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
