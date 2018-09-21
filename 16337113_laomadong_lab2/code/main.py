from csv import reader
from DivisionTree import DivisionTree
from property_select_policy import *


def my_reader(filename):
    file = list(reader(open(filename)))
    return [(line[:len(line) - 1], line[-1]) for line in file]


def validate(tree, validation_set):
    cnt = 0
    total = 0
    for x, y in validation_set:
        yy, path = tree.predict(x)
        if y == yy:
            cnt += 1
        total += 1
    print(cnt / total)


if __name__ == '__main__':
    tree = DivisionTree(list(reader(open("lab2_data/Car_train.csv"))), gini_policy)
    # tree.pre_order()
    with open("16337113_laomadong_Car.csv", 'w') as res:
        for x, y in my_reader("lab2_data/Car_test.csv"):
            print(*x, tree.predict(x)[0], sep=',', file=res)
