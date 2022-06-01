import pytest
import numpy as np
from sudoku.sudoku_struct.solver import SudokuSolverStruct
from sudoku.sudoku_struct.board import SudokuBoardStruct


@pytest.fixture()
def board_as_list(board_value_list):
    return board_value_list

class TestSudokuSolverStruct:
    def test_init_with_list(self, board_as_list):
        solver = SudokuSolverStruct(board_as_list)
        assert isinstance(solver, SudokuSolverStruct)
        assert isinstance(solver.board, SudokuBoardStruct)

    def test_init_with_board(self, board):
        solver = SudokuSolverStruct(board)
        assert isinstance(solver, SudokuSolverStruct)
        assert isinstance(solver.board, SudokuBoardStruct)

def test_solve(puzzle_pair):
    solver = SudokuSolverStruct(puzzle_pair['puzzle'])
    solution = SudokuBoardStruct(puzzle_pair['solution'])
    assert solver.is_solved is False

    solver.solve()

    assert solver.is_solved is True