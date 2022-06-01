from timeit import timeit
from tests.board_lists import puzzle_list_3x3_simple_b1
from sudoku import SudokuSolver
from sudoku.sudoku_struct.solver import SudokuSolverStruct
import logging

logging.basicConfig(level=logging.WARNING)

S_TO_MS = 1000


def main():
    n = 10

    performance_simple_puzzle = (timeit(lambda: SudokuSolver(puzzle_list_3x3_simple_b1).solve(), number=n) / n) * S_TO_MS
    print(f'Dataclass Performance{performance_simple_puzzle:.0f}ms')

    performance_simple_puzzle_struct = (timeit(lambda: SudokuSolverStruct(puzzle_list_3x3_simple_b1).solve(), number=n) / n) * S_TO_MS
    print(f'Struct Performance{performance_simple_puzzle_struct:.0f}ms')

if __name__ == "__main__":
    main()