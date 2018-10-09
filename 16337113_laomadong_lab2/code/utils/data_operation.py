import numpy as np


def is_same(iterable):
    last = None
    for x in iterable:
        if last is not None:
            if last != x:
                return False
        last = x
    return last is not None


def mode(iterable):
    ary = np.bincount(iterable)
    return np.argmax(ary)