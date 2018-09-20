from csv import reader
from DivisionTree import DivisionTree
from collections import Counter
import math


def f(vector):
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
    y_gain = f(y)
    max_gain = 0
    best_pro = None

    for col, pro in properties:
        branches = dict()
        for x, y_x in zip(pro, y):
            branches.setdefault(x, [])
            branches[x].append(y_x)
        gain = 0
        for branch, p in branches.items():
            gain += len(p) / len(pro) * f(p)

        if y_gain - gain > max_gain:
            max_gain = y_gain - gain
            best_pro = col
    return best_pro


def info_gain_rate_policy(properties, y):
    y_gain = f(y)
    max_gain = 0
    best_pro = None

    for col, pro in properties:
        branches = dict()
        for x, y_x in zip(pro, y):
            branches.setdefault(x, [])
            branches[x].append(y_x)
        gain = 0
        for branch, p in branches.items():
            gain += len(p) / len(pro) * f(p)

        if y_gain - gain / f(pro) > max_gain:
            max_gain = y_gain - gain
            best_pro = col
    return best_pro


def gini(vector):
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
    min_gini = 100
    best_pro = 0
    for col, pro in properties:
        gini_pro = gini(pro)
        if gini_pro < min_gini:
            min_gini = gini_pro
            best_pro = col
    return best_pro


if __name__ == '__main__':
    tree = DivisionTree(list(reader(open("lab2_data/Car_train.csv"))), info_gain_rate_policy)
    # tree.pre_order()
    cnt = 0
    total = 0
    for line in list(reader(open("lab2_data/Car_validation.csv"))):
        y = line[-1]
        x = line[:len(line) - 1]
        yy, path = tree.predict(x)
        if y == yy:
            cnt += 1
        else:
            print(x, y, yy, path)
        total += 1
    print(cnt / total)
