import numpy as np
from maze_io import read_maze
from search import *
from point import Point


def where(condition):
    a, b = np.where(condition)
    res = a[0], b[0]
    return Point(res)


if __name__ == '__main__':
    maze = read_maze('../data/MazeData.txt')
    start = where(maze == 'S')
    end = where(maze == 'E')

    search_policy = depth_first
    path = search_policy(maze, start, end, '%')
    print(len(path))

    directions = 'lrdu'
    for i in range(len(path) - 1):
        p, next_p = path[i], path[i + 1]
        maze[p] = directions[int(p[0] < next_p[0]) * 2 + int(p[1] < next_p[1])]
    np.savetxt('../data/path-' + search_policy.__name__ + '.txt', maze, '%s', delimiter='')
