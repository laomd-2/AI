# from sklearn.tree import DecisionTreeClassifier
from tree import DecisionTreeClassifier
import sys
sys.path.append("D:/learning/AI/experiment")
from utils import *


if __name__ == '__main__':
    clf = DecisionTreeClassifier()
    X, y = my_reader("lab2_data/Car_train.csv")
    X = to_digit(X)
    y = to_digit(y)

    m = X.shape[0]
    last = int(m * 0.8)
    clf.fit(X[:last],
            y[:last])
    # clf.show()

    print(validate(clf, (X[last:]),
             (y[last:])))
    # with open("16337113_laomadong_Car.csv", 'w') as res:
    #     X = np.asarray(my_reader("lab2_data/Car_test.csv")[0])
    #     for x, y in zip(X, clf.predict(X)):
    #         print(*x, y, sep=',', file=res)