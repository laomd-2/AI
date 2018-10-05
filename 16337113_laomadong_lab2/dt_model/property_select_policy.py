from collections import Counter
import math

__all__ = ["info_gain_policy", "info_gain_rate_policy", "gini_policy"]


def entropy(vector):
    count = Counter()
    for x in vector:
        count[x] += 1
    n = len(vector)
    h = 0
    for x, cnt in count.items():
        p = (cnt / n)
        h += -p * math.log2(p)
    return h


def info_gain_policy(y, y_i, feature):
    return entropy(y) - entropy(y_i)


def info_gain_rate_policy(y, y_i, feature):
    return info_gain_policy(y, y_i, feature) / entropy(feature)


def gini_index(vector):
    count = Counter()
    for x in vector:
        count[x] += 1
    g = 0
    l = len(vector)
    for p in count.values():
        p /= l
        g += p * (1 - p)
    return g


def gini_policy(y, y_i, feature):
    return 1 / gini_index(y_i)
