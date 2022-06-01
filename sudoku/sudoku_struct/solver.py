import logging
from time import time

from attrs import define, field

from sudoku.sudoku_struct.board import convert_to_board, SudokuBoardStruct

logger = logging.getLogger(__name__)


@define
class SudokuSolverStruct:
    board: SudokuBoardStruct = field(repr=lambda b: f'\n{repr(b.value_array)}\nsolved={b.is_solved}',
                                     converter=convert_to_board)
    timeout: int = field(default=10, eq=False, repr=False)
    timer: float = field(default=0, eq=False, repr=False)

    @property
    def is_solved(self):
        return self.board.is_solved

    def loop_step(self, func, empty_cell_count, *args, **kwargs):
        num_empty_cells_prev = 0
        num_empty_cells_current = empty_cell_count
        while ((num_empty_cells_prev != num_empty_cells_current)
               and (time() - self.timer < self.timeout)
               and (self.is_solved is False)):
            num_empty_cells_prev = num_empty_cells_current

            func(*args, **kwargs)
            if self.is_solved is True:
                return self.board.count_empty_cell()

            num_empty_cells_current = self.board.count_empty_cell()
        return self.board.count_empty_cell()

    def solve(self):
        self.timer = time()
        num_empty_cells_prev = 0
        num_empty_cells = self.board.count_empty_cell()
        while ((num_empty_cells_prev != num_empty_cells)
               and (time() - self.timer < self.timeout)
               and (self.is_solved is False)):
            num_empty_cells_prev = num_empty_cells

            num_empty_cells = self.loop_step(self.board.determine_board_candidates_groupwise, num_empty_cells)
            if self.is_solved is True:
                return self

            num_empty_cells = self.loop_step(self.board.determine_board_hidden_candidates_single, num_empty_cells)
            if self.is_solved is True:
                return self

        return self
