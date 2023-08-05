import numpy as np
import random
from pyslab.solver import brute_force


def generate(seed: np.ndarray = np.zeros([9, 9])):
    solution = brute_force(seed)


def permute_row_blocks(board: np.ndarray) -> np.ndarray:
    a, b, c = random.sample([0, 1, 2], k=3)
    return np.concatenate([board[a * 3:a * 3 + 3, :], board[b * 3:b * 3 + 3, :], board[c * 3:c * 3 + 3, :]])


def permute_col_blocks(board: np.ndarray) -> np.ndarray:
    a, b, c = random.sample([0, 1, 2], k=3)
    return np.concatenate([board[:, a * 3:a * 3 + 3], board[:, b * 3:b * 3 + 3], board[:, c * 3:c * 3 + 3]], axis=1)

