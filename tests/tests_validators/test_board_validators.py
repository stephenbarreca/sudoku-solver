import numpy as np
import pytest
import sudoku.validators.board_validators as validators

arrays_square = [
    ([1, 2, 3], [4, 5, 6], [7, 8, 9]),
    ([3, 2, 1], [4, 8, 6], [7, 5, 9]),
    ([1, 2], [1, 2]),
]
arrays_square = [np.array(arr, dtype=np.uint) for arr in arrays_square]

arrays_rows = [
    [1, 2, 3, 4, 5, 6, 7, 8, 9],
    [5, 6, 7, 8],
]
arrays_rows = [np.array(arr, dtype=np.uint) for arr in arrays_rows]

arrays_cols = [
    ([1], [2], [3], [4], [5], [6], [7], [8], [9]),
    ([9], [2], [3]),
]
arrays_cols = [np.array(arr, dtype=np.uint) for arr in arrays_cols]


@pytest.mark.parametrize('size, result', [
    (-1, False), (0, False), (1, False), (2, False),
    (3, False), (4, True), (5, False), (6, False),
    (9, True), (13, False), (16, True), (32, False),
    (4.0, True), (9.3, False), (16.0001, False), (16.000, True),
])
def test_is_valid_board_size(size, result):
    assert validators.is_valid_board_size(size) is result


valid_shape_arrays = arrays_square
args_valid_board_shape = list(zip(arrays_square, [True] * len(valid_shape_arrays)))

invalid_shape_arrays = arrays_rows + arrays_cols
args_invalid_board_shape = list(zip(invalid_shape_arrays, [False] * len(invalid_shape_arrays)))

args_is_valid_board_shape = args_valid_board_shape + args_invalid_board_shape


@pytest.mark.parametrize('board, result', args_is_valid_board_shape)
def test_is_valid_board_shape(board, result):
    assert validators.is_valid_board_shape(board) is result
