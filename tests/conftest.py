from copy import deepcopy

import numpy as np
import pytest

from tests.board_lists import (
    puzzle_list_2x2_a1, puzzle_list_2x2_a2, puzzle_list_3x3_easy, puzzle_list_3x3_simple_a1,
    puzzle_list_3x3_simple_b1, solution_list_2x2_a,
    solution_list_3x3_a,
    solution_list_3x3_easy, solution_list_3x3_simple_a, solution_list_3x3_simple_b,
)


@pytest.fixture()
def solution_2x2_a():
    return deepcopy(solution_list_2x2_a)


@pytest.fixture()
def solution_3x3_a():
    return deepcopy(solution_list_3x3_a)


@pytest.fixture()
def solution_3x3_simple():
    return deepcopy(solution_list_3x3_simple_b)


@pytest.fixture()
def puzzle_3x3_simple():
    return deepcopy(puzzle_list_3x3_simple_b1)


@pytest.fixture()
def solution_3x3_easy():
    return deepcopy(solution_list_3x3_easy)


@pytest.fixture()
def puzzle_3x3_easy():
    return deepcopy(puzzle_list_3x3_easy)


@pytest.fixture(params=[solution_list_2x2_a, solution_list_3x3_a], ids=['2x2', '3x3'])
def board_value_list(request):
    return deepcopy(request.param)


@pytest.fixture(
    params=[
        (puzzle_list_2x2_a1, solution_list_2x2_a),
        (puzzle_list_2x2_a2, solution_list_2x2_a),
        (puzzle_list_3x3_simple_a1, solution_list_3x3_simple_a),
        (puzzle_list_3x3_simple_b1, solution_list_3x3_simple_b),
        (puzzle_list_3x3_easy, solution_list_3x3_easy)
    ],
    ids=['2x2 a1', '2x2 a2', 'simple a1', 'simple b1', 'easy']
)
def puzzle_pair(request):
    pair = deepcopy(request.param)
    return {'puzzle': pair[0], 'solution': pair[1]}


@pytest.fixture()
def group_array_9x1():
    return np.array(range(1, 10))
