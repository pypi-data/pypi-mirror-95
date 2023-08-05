import numpy as np
from pyslab.board import unsolved, row_values, col_values, nonet_values, peer_values


def brute_force(board: np.ndarray):
    try:
        next_to_solve = next(unsolved(board))

    except StopIteration:
        return board

    possible_values = set(range(1, 10)) - peer_values(board, *next_to_solve)

    for v in possible_values:
        possible_board = np.copy(board)
        possible_board[next_to_solve] = v
        solution = brute_force(possible_board)
        if solution is not None:
            return solution
