from timeit import timeit
from tests.board_lists import puzzle_list_3x3_simple
from sudoku import SudokuSolver
import logging

logging.basicConfig(level=logging.WARNING)

S_TO_MS = 1000


def main():
    n = 10

    performance_simple_puzzle = (timeit(lambda: SudokuSolver(puzzle_list_3x3_simple).solve(), number=n) / n) * S_TO_MS
    print(f'{performance_simple_puzzle=:.0f}ms')


if __name__ == "__main__":
    main()