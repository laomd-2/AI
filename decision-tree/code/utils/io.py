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


def my_reader(filename, head=False, sep=','):
    data = numpy.loadtxt(filename, delimiter=sep, dtype=str)
    _, n = data.shape
    y = data[:, n-1]
    X = data[:, : n-1]
    if head:
        X = np.delete(X, 0, 0)
        y = np.delete(y, 0, 0)
    return X, y
