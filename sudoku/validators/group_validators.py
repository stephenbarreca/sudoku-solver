import numpy as np

from .array_validators import is_col, is_row, is_square
from .board_validators import is_valid_board_size


def is_complete_group(group: np.ndarray):
    """validate that a grouping of numbers is properly filled"""
    for i in range(1, group.size + 1):
        if i not in group:
            return False
    return True


def is_valid_group_size(group: np.ndarray, size: int = None):
    if size is None:
        size = group.size

    if group.size != size:
        return False
    return is_valid_board_size(group.size)


def is_valid_group_shape(group: np.ndarray):
    if is_square(group):
        return True
    elif is_row(group):
        return True
    elif is_col(group):
        return True
    return False
