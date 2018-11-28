import numpy as np
from n_queen import n_queens_backtracking, n_queens_fc


if __name__ == '__main__':
    board = np.zeros((8, 8), int)
    print(n_queens_fc(board, 0))
