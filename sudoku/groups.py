import numpy as np
from attrs import cmp_using, define, field
from numpy.typing import NDArray

from .cell import Cell
from .validators import is_1d_array


class GroupException(Exception):
    pass


def convert_to_row_array(arr: NDArray | list):
    if isinstance(arr, RowArray):
        return arr
    elif isinstance(arr, np.ndarray):
        return arr.view(RowArray)
    return np.array(arr).view(RowArray)


class RowArray(np.ndarray):
    class RowException(GroupException):
        pass
    #
    # def __array_finalize__(self, obj: convert_to_row_array):
    #     if is_1d_array(obj) is False:
    #         raise self.RowException(f'row group must be 1-dimensional. got {len(obj.shape)} dimensions')


def convert_to_col_array(arr: NDArray | list):
    if isinstance(arr, ColArray):
        return arr
    elif isinstance(arr, np.ndarray):
        return arr.view(ColArray)
    return np.array(arr).view(ColArray)


class ColArray(np.ndarray):
    class ColException(GroupException):
        pass

    # def __array_finalize__(self, obj: NDArray | list):
    #     if is_1d_array(obj) is False:
    #         raise self.ColException(f'col group must be 1-dimensional. got {len(obj.shape)} dimensions')


def convert_to_square_array(arr: NDArray | list):
    if isinstance(arr, SquareArray):
        return arr
    elif isinstance(arr, np.ndarray):
        return arr.view(SquareArray)
    return np.array(arr).view(SquareArray)


class SquareArray(np.ndarray):
    class SquareException(GroupException):
        pass

    # def __array_finalize__(self, obj: NDArray):
    #     if is_square_array(obj) is False:
    #         raise self.SquareException(f'square group must be 2-dimensional. got {len(obj.shape)} dimensions')


def convert_group_array(arr: NDArray | list):
    if isinstance(arr, np.ndarray):
        return arr
    return np.array(arr)


@define(slots=False)
class Group:
    index: int
    array: NDArray[int] = field(eq=cmp_using(eq=np.array_equal), converter=convert_group_array)

    def __contains__(self, item):
        return item in self.array

    def __array__(self):
        return self.array



@define(slots=False)
class Row(Group):
    array: RowArray = field(eq=cmp_using(eq=np.array_equal), converter=convert_to_row_array)

@define(slots=False)
class Col(Group):
    array: ColArray = field(eq=cmp_using(eq=np.array_equal), converter=convert_to_col_array)


@define(slots=False)
class Square(Group):
    array: SquareArray = field(eq=cmp_using(eq=np.array_equal), converter=convert_to_square_array)

