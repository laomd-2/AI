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


def n_queens_backtracking(board, row):
    n = board.shape[1]
    if row == n:
        print(board)
        print()
        return 1
    else:
        cnt = 0
        for i in range(n):
            if csp(board, (row, i)):
                board[row][i] = 1
                cnt += n_queens_backtracking(board, row + 1)
                board[row][i] = 0
        return cnt


def _n_queens_fc(board, row, domains):
    n = board.shape[1]
    if row == n:
        print(board)
        print()
        return 1
    else:
        tmp = domains[row].copy()
        if not tmp:
            return 0
        else:
            cnt = 0
            for x in tmp:
                restore = []
                for i in range(row + 1, n):
                    domain = domains[i]
                    restore.append(set())
                    if x in domain:
                        restore[-1].add(x)
                        domain.remove(x)
                    for j in domain.copy():
                        if abs(j - x) == i - row:
                            restore[-1].add(j)
                            domain.remove(j)
                board[row][x] = 1
                domains[row] = {x}
                cnt += _n_queens_fc(board, row + 1, domains)
                for i, res in enumerate(restore):
                    domains[row + i + 1].update(res)
                board[row][x] = 0
            domains[row] = tmp
            return cnt


def n_queens_fc(board, row):
    n = board.shape[1]
    domains = [set(range(n)) for _ in range(n)]
    return _n_queens_fc(board, row, domains)
