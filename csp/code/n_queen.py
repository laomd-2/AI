import numpy as np


__all__ = ['n_queens_fc', 'n_queens_backtracking']


def _is_valid(p, n):
    return 0 <= p[0] < n and 0 <= p[1] < n


def csp(columns, k):
    for i in range(k):
        if columns[i] == columns[k] or k - i == abs(columns[i] - columns[k]):
            return False
    return True


def _n_queens_backtracking(chess_board, columns, row):
    n = len(columns)
    if row == n:
        # print(chess_board)
        return 1
    else:
        cnt = 0
        for i in range(n):
            columns[row] = i
            if csp(columns, row):
                chess_board[row][i] = 1
                cnt += _n_queens_backtracking(chess_board, columns, row + 1)
                chess_board[row][i] = 0
        return cnt


def n_queens_backtracking(chess_board):
    n = chess_board.shape[1]
    return _n_queens_backtracking(chess_board, [0] * n, 0)


def csp_update(domain, x, queen_id, other_queen):
    restore = set()
    if x in domain:
        restore.add(x)
        domain.remove(x)
    for j in domain.copy():
        if abs(j - x) == abs(other_queen - queen_id):
            restore.add(j)
            domain.remove(j)
    return restore


def _n_queens_fc(board, index, cnt, domains):
    n = board.shape[1]
    if index >= n:
        return cnt == n
    else:
        res = 0
        queen_id = domains[index][0]
        tmp = domains[index][1].copy()
        for x in tmp:
            restore = []
            min_remain = float('inf')
            min_remain_i = None
            for i in range(index + 1, n):
                other_queen, domain = domains[i]
                restore.append(csp_update(domain, x, queen_id, other_queen))
                length = len(domain)
                if length < min_remain:
                    min_remain = length
                    min_remain_i = i

            board[queen_id][x] = 1
            domains[index] = (domains[index][0], {x})
            if min_remain_i is not None:
                domains[index + 1], domains[min_remain_i] = domains[min_remain_i], domains[index + 1]
            res += _n_queens_fc(board, index + 1, cnt + 1, domains)
            if min_remain_i is not None:
                domains[index + 1], domains[min_remain_i] = domains[min_remain_i], domains[index + 1]

            for j, d in enumerate(restore):
                domains[index + j + 1][1].update(d)
            board[queen_id][x] = 0
        domains[index] = (domains[index][0], tmp)
    return res


def n_queens_fc(board):
    n = board.shape[1]
    domains = [(i, set(range(n))) for i in range(n)]
    return _n_queens_fc(board, 0, 0, domains)
