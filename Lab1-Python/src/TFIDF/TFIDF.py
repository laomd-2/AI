from collections import Counter
from mycollections import NumberOrderedDict
import math


def get_tf_idf(documents):
    TF = []
    IDF = NumberOrderedDict()

    for d in documents:
        TF.append(Counter())
        for word in d.split(' '):
            TF[-1][word] += 1
            if TF[-1][word] == 1:
                IDF[word] += 1

    D = len(documents)
    for i in range(D):
        row = TF[i]
        total = sum(row.values())
        TF[i] = []
        for word in IDF:
            TF[i].append(row[word] / total)

    for word in IDF:
        IDF[word] = math.log(D / (1 + IDF[word]))
    return IDF.keys(), TF, list(IDF.values())
