from typing import List
import numpy as np


def solved(solution: np.ndarray) -> bool:

    numbers = set(range(1, 10))

    # rows
    if not all(set(solution[row, :]) == numbers for row in range(9)):
        return False

    # cols
    if not all(set(solution[:, col]) == numbers for col in range(9)):
        return False

    # nonets
    if not all(
            set(solution[i:i+3,j:j+3].flatten()) == numbers
            for i in range(0, 9, 3)
            for j in range(0, 9, 3)
    ):
        return False

    return True
