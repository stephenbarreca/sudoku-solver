import numpy as np
import pytest

from sudoku.solver import fill_simple_case_col, fill_simple_case_row, fill_simple_case_square


@pytest.mark.parametrize('arr,output', [
    (
            ([1], [2], [3], [0]),
            ([1], [2], [3], [4])
    )
])
def test_fill_simple_case_col(arr, output):
    arr = np.array(arr, dtype=np.uint)
    assert np.array_equal(fill_simple_case_col(arr), output)


@pytest.mark.parametrize('arr,output', [
    (
            ([1, 2, 3, 0]),
            ([1, 2, 3, 4])
    )

])
def test_fill_simple_case_row(arr, output):
    arr = np.array(arr, dtype=np.uint)
    assert np.array_equal(fill_simple_case_row(arr), output)


@pytest.mark.parametrize('arr,output', [
    (
            ([1, 2], [3, 0]),
            ([1, 2], [3, 4])
    )
])
def test_fill_simple_case_square(arr, output):
    arr = np.array(arr, dtype=np.uint)
    assert np.array_equal(fill_simple_case_square(arr), output)
