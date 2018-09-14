import csv
import math
from KNN import KNN


def read_csv(path):
    csv_file = csv.reader(open(path))
    next(csv_file)
    return csv_file


def distance(x1, x2):
    return -len(x1 | x2) / (1 + math.log(len(x1 & x2) + 1))


def test(k, dis):
    knn = KNN(distance=dis)
    for x, y in read_csv("lab1_data/classification_dataset/train_set.csv"):
        knn.add(set(x.split(' ')), y)
    count = 0
    total = 0
    for x, y in read_csv("lab1_data/classification_dataset/validation_set.csv"):
        yy = knn.predict(set(x.split(' ')), k)
        total += 1
        if y == yy:
            count += 1
    acc = count / total
    print("k=", k, acc)
    return acc


if __name__ == '__main__':
    for k in range(9, 20, 1):
        test(k, distance)
