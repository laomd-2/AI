import math, sys
from KNN import KNN
from csv_io import read_csv
from collections import Counter


def classification_label_policy(k_neighbors):
    label = None
    cur_max = 0
    counter = Counter()
    while k_neighbors:
        dis, the_label = k_neighbors.get()
        counter[the_label] += 1
        if counter[the_label] > cur_max:
            cur_max = counter[the_label]
            label = the_label
    return label


def regression_label_policy(k_neighbors):
    y = [0.0] * 6
    y_sum = 0
    while k_neighbors:
        dis, the_label = k_neighbors.get()
        for i in range(len(the_label)):
            tmp = the_label[i] / dis
            y[i] += tmp
            y_sum += tmp
    for i in range(len(y)):
        y[i] /= y_sum
    return tuple(y)


def distance(x1, x2):
    return -len(x1 | x2) / (1 + math.log(len(x1 & x2) + 1))


def train(file, label_policy, label_type):
    knn = KNN(10, distance, label_policy)
    for x, *y in read_csv(file):
        knn.add(set(x.split(' ')), tuple(map(lambda a: label_type(a), y)))
    return knn


def validate(knn, validate_file, output_file):
    with open(output_file, 'w') as f:
        for x, *y in read_csv(validate_file):
            print(*knn.predict(set(x.split(' '))), sep=',', file=f)


if __name__ == '__main__':
    problem = sys.argv[1]

    prefix = "lab1_data/" + problem + "_dataset/"
    validate_file = prefix + "validation_set.csv"
    output = "result.csv"

    label_policy = regression_label_policy
    if problem == "classification":
        label_policy = classification_label_policy
    validate(train(prefix + "train_set.csv", label_policy, float),
             validate_file, output
             )
    results = [y.rstrip().split(',') for y in open(output).readlines()]
    standard = [y for x, *y in read_csv(validate_file)]
    total = len(results)
    correct = 0
    if problem == "classification":
        for i in range(total):
            if results[i] == standard[i]:
                correct += 1
        print("%g" % (correct / total))