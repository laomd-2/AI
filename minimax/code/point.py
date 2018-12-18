import numpy as np


class Point(tuple):

    @staticmethod
    def __new__(cls, *args):
        return super(Point, cls).__new__(cls, *args)

    def __add__(self, other):
        return self.__new__(Point, (a + b for a, b in zip(self, other)))

    def __radd__(self, other):
        return self + other


def where(condition):
    all_p = []
    res = np.where(condition)
    for i, j in zip(res[0], res[1]):
        p = (i, j)
        all_p.append(Point(p))
    return all_p
    # return np.where(condition)
