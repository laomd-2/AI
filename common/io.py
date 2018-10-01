import numpy


def to_digit(mat):
    mat = mat.T
    res = numpy.zeros_like(mat, dtype=numpy.float64)
    m, n = mat.shape
    for i in range(m):
        words = dict()
        for j in range(n):
            if mat[i, j] not in words:
                words[mat[i, j]] = len(words)
            res[i, j] = words[mat[i, j]]
    return res.T


def my_reader(filename):
    data = numpy.loadtxt(filename, delimiter=',', dtype=str)
    _, n = data.shape
    y = data.take((n - 1,), 1)
    X = data.take(range(0, n - 1), 1)
    return X, y
