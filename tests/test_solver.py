from itertools import permutations, chain
from typing import Iterable, Sequence
from copy import copy
import numpy as np
import pytest

from sudoku.solver import fill_simple_case, make_square, make_line
from sudoku.validators import is_square


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

input_group_output_combos = make_input_group_output_combos()


@pytest.mark.parametrize('input_group, output', input_group_output_combos)
def test_fill_simple_case_line(input_group, output):
    solved_group = fill_simple_case(input_group)
    assert np.array_equal(solved_group, output)


@pytest.mark.parametrize('input_group, output', input_group_output_combos)
def test_fill_simple_case_square(input_group, output):
    square_group = make_square(input_group)
    solved_group = fill_simple_case(square_group)
    assert is_square(solved_group)
    assert np.array_equal(make_line(solved_group), output)
