from copy import deepcopy

import numpy as np
import pytest

from tests.board_lists import (
    puzzle_list_3x3_easy, puzzle_list_3x3_simple, solution_list_2x2_a, solution_list_3x3_a, solution_list_3x3_easy,
    solution_list_3x3_simple,
)


@pytest.fixture()
def solution_2x2_a():
    return deepcopy(solution_list_2x2_a)


@pytest.fixture()
def solution_3x3_a():
    return deepcopy(solution_list_3x3_a)


@pytest.fixture()
def solution_3x3_simple():
    return deepcopy(solution_list_3x3_simple)


@pytest.fixture()
def puzzle_3x3_simple():
    return deepcopy(puzzle_list_3x3_simple)


@pytest.fixture()
def solution_3x3_easy():
    return deepcopy(solution_list_3x3_easy)


@pytest.fixture()
def puzzle_3x3_easy():
    return deepcopy(puzzle_list_3x3_easy)


@pytest.fixture(params=[solution_list_2x2_a, solution_list_3x3_a], ids=['2x2', '3x3'])
def value_list(request):
    return request.param


@pytest.fixture(
    params=[
        (puzzle_list_3x3_simple, solution_list_3x3_simple),
        (puzzle_list_3x3_easy, solution_list_3x3_easy)
    ],
    ids=['simple', 'easy']
)
def puzzle_pair(request):
    pair = deepcopy(request.param)
    return {'puzzle': pair[0], 'solution': pair[1]}


@pytest.fixture()
def group_array_9x1():
    return np.array(range(1, 10))
