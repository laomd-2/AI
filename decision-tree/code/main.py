from tree import *
from utils import *


if __name__ == '__main__':
    clf = DecisionTreeClassifier(property_select_policy=gini_index)
    X, y = my_reader("lab2_data/Car_train.csv")
    y = y.astype(int)
    clf.fit(X, y)

    with open("16337113_laomadong_Car.csv", 'w') as res:
        X = np.asarray(my_reader("lab2_data/Car_test.csv")[0])
        for y in clf.predict(X):
            print(y, file=res)
