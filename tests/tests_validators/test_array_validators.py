import pytest
import numpy as np
import sudoku.validators.array_validators as validators

arrays = [
    (1,),
    (1, 2, 3),
    (1, 2, 3, 4, 5, 6, 7, 8, 9),

    ([1], [1]),

    ([1, 2], [1, 2]),
    ([1, 2], [3, 4]),

    ([1, 2, 3], [1, 2, 3]),

    ([1, 2], [1, 2], [1, 2]),
    ([1, 2], [3, 4], [5, 6]),

    ([1, 2, 3], [1, 2, 3], [1, 2, 3]),
    ([1, 2, 3], [3, 4, 5], [5, 6, 7]),

    ([1], [1], [1], [1], [1]),
]
arrays = [np.array(arr, dtype=np.uint) for arr in arrays]
arg_arr = ('arr', arrays)


@pytest.mark.parametrize(*arg_arr)
class TestFunc_is_n_dimensional:
    def test_is_n_dimensional_true(self, arr):
        n = len(arr.shape)
        assert validators.is_n_dimensional(arr, n) is True

    def test_is_n_dimensional_false(self, arr):
        n = len(arr.shape)
        assert validators.is_n_dimensional(arr, n + 1) is False
        assert validators.is_n_dimensional(arr, n - 1) is False


@pytest.mark.parametrize('arr,result', zip(arrays, [
    False, False, False,
    False,
    True, True,
    False,
    False, False,
    True, True,
    False
]))
def test_is_square(arr, result):
    assert validators.is_square(arr) is result


@pytest.mark.parametrize(*arg_arr)
def test_is_row(arr):
    result = validators.is_n_dimensional(arr, 1)
    assert validators.is_row(arr) is result


@pytest.mark.parametrize('arr,result', zip(arrays, [
    False, False, False,
    True,
    False, False,
    False,
    False, False,
    False, False,
    True
]))
def test_is_col(arr, result):
    assert validators.is_col(arr) is result
