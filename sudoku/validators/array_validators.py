import numpy as np


def is_square(arr: np.ndarray):
    shape = arr.shape
    if len(shape) == 2 and shape[0] == shape[1]:
        return True
    return False


def is_n_dimensional(arr: np.ndarray, n: int):
    if len(arr.shape) != n:
        return False
    return True


def is_row(arr: np.ndarray):
    return is_n_dimensional(arr, 1)


def is_col(arr: np.ndarray):
    if not is_n_dimensional(arr, 2):
        return False

    rows, cols = arr.shape
    if cols != 1:
        return False

    return True
