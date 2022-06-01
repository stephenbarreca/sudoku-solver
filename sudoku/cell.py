import numpy as np
from attr import define, field
from numpy.typing import NDArray


@define
class Cell:
    row: int = field(eq=True)
    col: int = field(eq=True)
    _value: int = field(default=0, eq=False)
    _candidates: NDArray[int] = field(default=[], eq=False, converter=np.array)

    def __attrs_post_init__(self):
        if self.value != 0:
            self.candidates = np.array([self.value])

    def refine_candidates(self, candidate_values: NDArray[int]):
        if len(self.candidates) == 0:
            self.candidates = candidate_values
        else:
            self.candidates = np.setdiff1d(self.candidates, candidate_values)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val
        self._candidates = np.array([val])

    @property
    def candidates(self):
        return self._candidates

    @candidates.setter
    def candidates(self, candidates: NDArray[int]):
        self._candidates = candidates
        if len(candidates) == 1:
            self._value = candidates[0]

    @classmethod
    def from_coords(cls, coords):
        return cls(*coords)
