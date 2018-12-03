from tree import *
from utils import *
from sklearn.model_selection import cross_val_score


if __name__ == '__main__':
    X, y = my_reader("lab2_data/Car_train.csv")
    y = y.astype(int)
    Ms = [(entropy, ), (entropy, True), (gini_index, )]

    clf = DecisionTreeClassifier(gini_index, True)
    scores = cross_val_score(clf, X, y, cv=5, scoring='accuracy')
    print(scores, scores.mean())