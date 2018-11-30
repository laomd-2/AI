from point import Point

__all__ = ['n_queens_fc', 'n_queens_backtracking']


def _is_valid(p, n):
    return 0 <= p[0] < n and 0 <= p[1] < n


def csp(board, point):
    point = Point(point)
    n = board.shape[1]
    for d in (-1, 0, 1):
        direction = (-1, d)
        p = point + direction
        while _is_valid(p, n):
            if board[p] == 1:
                return False
            p = p + direction
    return True


def n_queens_backtracking(board, row=0):
    n = board.shape[1]
    if row == n:
        # print(board)
        # print()
        return 1
    else:
        cnt = 0
        for i in range(n):
            if csp(board, (row, i)):
                board[row][i] = 1
                cnt += n_queens_backtracking(board, row + 1)
                board[row][i] = 0
        return cnt


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
                restore.append(set())
                if x in domain:
                    restore[-1].add(x)
                    domain.remove(x)
                for j in domain.copy():
                    if abs(j - x) == abs(other_queen - queen_id):
                        restore[-1].add(j)
                        domain.remove(j)
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
