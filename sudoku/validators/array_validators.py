import numpy as np
from numpy.typing import NDArray


def is_nd_array(arr: NDArray, n: int) -> bool:
    if len(arr.shape) != n:
        return False
    return True


def is_1d_array(arr: np.ndarray) -> bool:
    return is_nd_array(arr, 1)


def is_2d_array(arr: np.ndarray) -> bool:
    return is_nd_array(arr, 2)


def is_square_array(arr: np.ndarray) -> bool:
    shape = arr.shape
    if is_2d_array(arr) and shape[0] == shape[1]:
        return True
    return False
