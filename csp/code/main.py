import numpy as np
import time
from n_queen import n_queens_backtracking, n_queens_fc


if __name__ == '__main__':
    board = np.zeros((8, 8), int)
    start = time.time()
    print(n_queens_fc(board))
    # print(n_queens_backtracking(board))
    print(time.time() - start)
