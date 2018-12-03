import numpy as np
from n_queen import n_queens_backtracking, n_queens_fc


if __name__ == '__main__':
    board = np.zeros((12, 12), int)
    print(n_queens_fc(board))
    # print(n_queens_backtracking(board))
