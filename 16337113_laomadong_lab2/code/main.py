from tree import *
from utils import *


if __name__ == '__main__':
    clf = DecisionTreeClassifier(property_select_policy=gini_index)
    X, y = my_reader("lab2_data/Car_train.csv")
    clf.fit(X, y)

    # print(validate(clf, X, y, shuffle=False))
    clf.show()
    with open("16337113_laomadong_Car.csv", 'w') as res:
        X = np.asarray(my_reader("lab2_data/Car_test.csv")[0])
        for x, y in zip(X, clf.predict(X)):
            print(*x, y, sep=',', file=res)