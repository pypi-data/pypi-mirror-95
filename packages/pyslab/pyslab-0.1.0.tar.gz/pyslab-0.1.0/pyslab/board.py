import numpy as np
from typing import Iterator, Tuple, Set


def unsolved(board: np.ndarray) -> Iterator[Tuple[int, int]]:
    return zip(*np.where(board == 0))


def row_values(board: np.ndarray, row: int) -> Set:
    return set(board[row, :]) - {0}


def col_values(board: np.ndarray, col: int) -> Set:
    return set(board[:, col]) - {0}


def nonet_values(board: np.ndarray, row: int, col: int) -> Set:
    r, c = row//3*3, col//3*3
    return set(board[r:r+3,c:c+3].flatten()) - {0}


def peer_values(board: np.ndarray, row: int, col: int) -> Set:
    return row_values(board, row).union(col_values(board, col)).union(nonet_values(board, row, col))
