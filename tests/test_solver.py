from copy import copy
from itertools import chain, permutations

import numpy as np
import pytest

from sudoku.puzzle import make_line, make_square, SudokuPuzzle
from sudoku.solver import check_and_fill_group_with_one_missing, SudokuSolver
from sudoku.validators import is_square
from tests.conftest import solution_2x2_a, solution_3x3_b

def create_groups_with_one_empty_cell(group: np.ndarray) -> list[np.ndarray]:
    ret = [copy(group) for i in range(len(group))]
    for i, g in enumerate(ret):
        np.put(g, i, 0)
    return ret


def make_input_group_output_combos(max_board_size: int = 2):
    board_sizes = [i * i for i in range(2, max_board_size + 1)]
    complete_groups = tuple(chain(*[tuple(permutations(range(1, i + 1))) for i in board_sizes]))
    combos = []
    for cg in complete_groups:
        cg_array = np.array(cg)
        incomplete_groups = create_groups_with_one_empty_cell(cg_array)
        for ig in incomplete_groups:
            combos.append((ig, cg_array))
    return combos


input_group_output_combos = make_input_group_output_combos(2)


@pytest.mark.parametrize('input_group, output', input_group_output_combos)
class TestFunc_check_and_fill_simple_case:
    def test_line_group_with_one_missing_gets_filled(self, input_group, output):
        solved_group = check_and_fill_group_with_one_missing(input_group)
        assert np.array_equal(solved_group, output)

    def test_square_group_with_one_missing_gets_filled(self, input_group, output):
        square_group = make_square(input_group)
        solved_group = check_and_fill_group_with_one_missing(square_group)
        assert is_square(solved_group)
        assert np.array_equal(make_line(solved_group), output)




simplest_boards_puzzle_solution = (
    (  # test basic row fill solution
        solution_2x2_a,
        (
            [0, 2, 3, 4],
            [2, 0, 4, 1],
            [3, 4, 0, 2],
            [4, 1, 2, 0]
        )
    ),
    (  # test basic col fill solution
        solution_2x2_a,
        (
            [0, 0, 0, 0],
            [2, 3, 4, 1],
            [3, 4, 1, 2],
            [4, 1, 2, 3]
        )
    ),
    (  # test larger solution
        solution_3x3_b,
        (
            [0, 2, 3, 4, 5, 6, 7, 8, 9],
            [2, 0, 4, 5, 6, 7, 8, 9, 1],
            [3, 4, 0, 6, 7, 8, 9, 1, 2],
            [4, 5, 6, 0, 8, 9, 1, 2, 3],
            [5, 6, 7, 8, 0, 1, 2, 3, 4],
            [6, 7, 8, 9, 1, 0, 3, 4, 5],
            [7, 8, 9, 1, 2, 3, 0, 5, 6],
            [8, 9, 1, 2, 3, 4, 5, 0, 7],
            [9, 1, 2, 3, 4, 5, 6, 7, 0],
        ),
    ),
)


@pytest.mark.parametrize('solution, puzzle', simplest_boards_puzzle_solution)
def solve_groups_with_one_missing(puzzle, solution):
    solution = SudokuPuzzle(solution)
    solver = SudokuSolver(puzzle)
    assert solver.is_solved is False

    solver.solve_groups_with_one_missing()

    assert solver.is_solved is True
    assert solver.puzzle.board == solution.board


@pytest.mark.parametrize('output, puzzle', [
    (
            solution_2x2_a,
            (
                    [1, 0, 0, 4],
                    [2, 3, 4, 1],
                    [3, 0, 1, 2],
                    [4, 1, 2, 3]
            )
    ),
])
def test_solve_cells_with_one_possibility(output, puzzle):
    output = SudokuPuzzle(output)
    solver = SudokuSolver(puzzle)
    assert solver.is_solved is False

    solver.solve_cells_with_one_possibility()

    assert solver.is_solved is True
    assert solver.puzzle == output
