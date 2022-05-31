import numpy as np

from .array_validators import is_square_array


def is_valid_board_size(size: int):
    if size < 4 or int(size) != size:
        return False
    inner_square_size = np.sqrt(size)
    if inner_square_size != int(inner_square_size):
        return False
    return True


def is_valid_board_shape(board: np.ndarray):
    """
    validate that the sudoku board is a square. Optionally test the size of the board

    Args:
        board: the board grid to test
        size: the length of the board's size

    Returns:

    """
    return is_square_array(board)
