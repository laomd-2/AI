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


def info_gain_policy(properties, y):
    y_gain = entropy(y)
    max_gain = 0
    best_pro = None

    for col, pro in enumerate(properties):
        branches = dict()
        for x, y_x in zip(pro, y):
            branches.setdefault(x, [])
            branches[x].append(y_x)
        gain = 0
        for branch, p in branches.items():
            gain += len(p) / len(pro) * entropy(p)

        if y_gain - gain > max_gain:
            max_gain = y_gain - gain
            best_pro = col
    return best_pro


def info_gain_rate_policy(properties, y):
    y_gain = entropy(y)
    max_gain = 0
    best_pro = None

    for col, pro in enumerate(properties):
        branches = dict()
        for x, y_x in zip(pro, y):
            branches.setdefault(x, [])
            branches[x].append(y_x)
        gain = 0
        for branch, p in branches.items():
            gain += len(p) / len(pro) * entropy(p)

        if y_gain - gain / entropy(pro) > max_gain:
            max_gain = y_gain - gain
            best_pro = col
    return best_pro


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


def gini_policy(properties, y):
    min_gini = 1000000
    best_pro = None
    for col, pro in enumerate(properties):
        branches = dict()
        for x, y_x in zip(pro, y):
            branches.setdefault(x, [])
            branches[x].append(y_x)
        gini = 0
        for branch, p in branches.items():
            gini += len(p) / len(pro) * gini_index(p)

        if gini < min_gini:
            min_gini = gini
            best_pro = col
    return best_pro
