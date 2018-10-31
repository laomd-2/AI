__all__ = ['depth_first', 'iterative_deepen']


def valid(i, n):
    return 0 <= i < n


def get_neighbor(maze, origin, wall):
    m, n = maze.shape
    directions = ((-1, 0), (0, 1), (0, -1), (1, 0))
    neighbors = []
    for direction in directions:
        neighbor = origin + direction
        if valid(neighbor[0], m) and valid(neighbor[1], n):
            if maze[neighbor] != wall:
                neighbors.append(neighbor)
    return neighbors


def _depth_first(maze, cur, end, path, wall, depth):
    maze[cur] = wall
    path.append(cur)
    if cur == end:
        return True
    else:
        if depth != 0:
            for n in get_neighbor(maze, cur, wall):
                if _depth_first(maze, n, end, path, wall, depth - 1):
                    return True
    path.pop(-1)
    return False


def depth_first(maze, start, end, wall):
    path = []
    _depth_first(maze.copy(), start, end, path, wall, -1)
    return path


def iterative_deepen(maze, start, end, wall):
    m, n = maze.shape
    path = []
    for i in range(1, m * n):
        if _depth_first(maze.copy(), start, end, path, wall, i):
            break
    return path
