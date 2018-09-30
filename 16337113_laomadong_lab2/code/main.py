from DecisionTreeClassifier import DecisionTreeClassifier
import numpy as np


def my_reader(filename):
    data = np.loadtxt(filename, delimiter=',', dtype=str)
    _, n = data.shape
    y = data.take((n - 1,), 1)
    X = data.take(range(0, n - 1), 1)
    return X, y


def validate(tree, validation_X, y):
    cnt = 0
    total = 0
    res = tree.predict(validation_X)
    for yy, y in zip(res, y):
        if y == yy:
            cnt += 1
        total += 1
    print(cnt / total)


def digitalize(matrix, dtype=int):
    matrix = matrix.T
    res = np.zeros_like(matrix)
    for row, res_row in zip(matrix, res):
        all_word = dict()
        for i in range(row.size):
            if row[i] not in all_word:
                all_word[row[i]] = dtype(len(all_word))
            res_row[i] = all_word[row[i]]
    return res.T


if __name__ == '__main__':
    clf = DecisionTreeClassifier()
    X, y = my_reader("lab2_data/Car_train.csv")
    m = X.shape[0]
    last = int(m * 0.8)

    clf.fit(digitalize(X[last:]),
            digitalize(y[last:]))
    # clf.show()

    # validate(clf, digitalize(X[last: m]),
    #          digitalize(y[last: m]))
    with open("16337113_laomadong_Car2.csv", 'w') as res:
        X = np.asarray(my_reader("lab2_data/Car_test.csv")[0])
        test_X = digitalize(X)
        for x, y in zip(X, clf.predict(test_X)):
            print(*x, y, sep=',', file=res)