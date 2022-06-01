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

    @property
    def is_solved(self):
        return self.board.is_solved

    def solve(self):
        timer = time()
        num_empty_cells_prev = 0
        num_empty_cells_current = self.board.count_empty_cell()

        while ((num_empty_cells_prev != num_empty_cells_current)
               and (time() - timer < self.timeout)
               and (self.is_solved is False)):
            num_empty_cells_prev = num_empty_cells_current

            self.board.determine_board_candidates_groupwise()
            if self.is_solved is True:
                break

            for cell in self.board.get_empty_cells():
                self.board.determine_cell_candidates(cell)

            if self.is_solved is True:
                break

            self.board.determine_board_hidden_candidates_single()
            if self.is_solved is True:
                break
            num_empty_cells_current = self.board.count_empty_cell()
            logger.info(f'board: {self.board.cell_array}')
            logger.info(f'empty cells: {num_empty_cells_current}')
        return self
