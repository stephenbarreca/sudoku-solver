import pytest
import numpy as np
from numpy.typing import NDArray
from sudoku.groups import Group
from copy import deepcopy

class TestGroup:
    @pytest.fixture()
    def group(self, group_array_9x1):
        return Group(0, group_array_9x1)

    def test_init_with_ndarray(self, group, group_array_9x1):
        assert isinstance(group, Group)
        assert np.array_equal(group.array, group_array_9x1)

    def test_array_equality(self, group, group_array_9x1: NDArray):
        group2 = Group(0, group_array_9x1.copy())
        assert group.array is not group2.array
        assert group == group2

    def test_init_with_list(self):
        item_list = list(range(1, 10))
        group = Group(1, item_list)
        assert isinstance(group, Group)
        assert list(group.array) == item_list