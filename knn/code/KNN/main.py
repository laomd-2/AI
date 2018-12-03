import math
import sys
from KNN import KNN
from classification.label_policy import classification_label_policy
from regression.label_policy import regression_label_policy
from csv_io import read_csv
from IDF import IDF


def distance(x1, x2):
    if id(x1) == id(x2):
        return 1
    interact = set()
    a, b = 0, 0
    for word, tfidf in x1.items():
        interact.add(word)
        a += tfidf * tfidf
    for word, tfidf in x2.items():
        interact.add(word)
        b += tfidf * tfidf
    c = 0
    for word in interact:
        c += x1[word] * x2[word]
    return c / math.sqrt(a * b)


def train(k, file, label_policy, label_type):
    knn = KNN(k, distance, label_policy)
    documents = []
    labels = []

    file = iter(read_csv(file))
    next(file)
    for x, *y in file:
        documents.append(x)
        labels.append(y)
    idf = IDF(documents)
    for i in range(len(documents)):
        knn.add(idf.get_tf_idf(documents[i]), tuple(map(lambda a: label_type(a), labels[i])))
    return knn, idf


def test(knn, idf, file):
    file = read_csv(file)
    return [next(file)] + [(text_id, x, knn.predict(idf.get_tf_idf(x))) for text_id, x, *y in file]


if __name__ == '__main__':
    problem = sys.argv[1]

    prefix = "lab1_data/" + problem + "_dataset/"

    label_policy = regression_label_policy
    label_type = float
    k = 5

    if problem == "classification":
        label_policy = classification_label_policy
        label_type = str
        k = 8
    output = "16337113_laomadong_KNN_" + problem + ".csv"
    knn, idf = train(k, prefix + "train_set.csv", label_policy, label_type)

    with open(output, 'w') as file:
        results = iter(test(knn, idf, prefix + "test_set.csv"))
        print(*next(results), sep=',', file=file)
        for text_id, x, y in results:
            print(text_id, x, *y, sep=',', file=file)
