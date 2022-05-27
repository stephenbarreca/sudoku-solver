import pytest
import numpy as np
import sudoku.validators.group_validators as validators

group_arrays_valid = [
    # rows
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [5, 6, 7, 8, 9, 1, 2, 3, 4],
    [1, 2, 3, 4, 5, 6, 7, 8, 0],
    [12, 2, 3, 4, 5, 6, 7, 8, 9],
    [9, 2, 3, 4, 5, 6, 7, 8, 9],

    # squares
    ([1, 2, 3], [4, 5, 6], [7, 8, 9]),
    ([3, 2, 1], [4, 8, 6], [7, 5, 9]),
    ([1, 2, 3], [1, 2, 3], [1, 2, 3]),

    # cols
    ([1], [2], [3], [4], [5], [6], [7], [8], [9]),
    ([9], [2], [3], [5], [4], [6], [7], [8], [1]),
]
group_arrays_valid = [np.array(arr, dtype=np.uint) for arr in group_arrays_valid]

group_arrays_invalid_shape = [
    ([1, 2], [4, 5], [7, 8]),
    ([3, 2, 5, 6], [4, 8, 6, 7], [7, 5, 7, 8]),
]
group_arrays_invalid_shape = [np.array(arr, dtype=np.uint) for arr in group_arrays_invalid_shape]

group_arrays_invalid_size = group_arrays_invalid_shape


@pytest.mark.parametrize('group, result', zip(group_arrays_valid, [
    True, True, False, False, False,
    True, True, False,
    True, True,
]))
def test_is_group_complete(group, result):
    assert validators.is_complete_group(group) is result


class TestFunc_is_valid_group_size:
    args_group_arrays_valid = list(zip(
        group_arrays_valid,
        [True] * len(group_arrays_valid)
    ))
    args_group_arrays_invalid = list(zip(
        group_arrays_invalid_size,
        [False] * len(group_arrays_valid)
    ))

    @pytest.mark.parametrize('group, result', args_group_arrays_valid + args_group_arrays_invalid)
    def test_with_size_kwarg(self, group, result):
        assert validators.is_valid_group_size(group, size=9) == result

    @pytest.mark.parametrize('group, result', args_group_arrays_valid + args_group_arrays_invalid)
    def test_without_size_kwarg(self, group, result):
        assert validators.is_valid_group_size(group) == result

    @pytest.mark.parametrize('group', group_arrays_valid)
    @pytest.mark.parametrize('size', list(range(0, 9, 4)) + list(range(10, 13)))
    def test_returns_false_with_size_kwarg(self, group, size):
        assert validators.is_valid_group_size(group, size=size) is False


is_valid_shape_args = (
        list(zip(group_arrays_valid, [True] * len(group_arrays_valid))) +
        list(zip(group_arrays_invalid_shape, [False] * len(group_arrays_invalid_shape)))
)


@pytest.mark.parametrize('group, result', is_valid_shape_args)
def test_is_valid_group_shape(group, result):
    assert validators.is_valid_group_shape(group) is result
