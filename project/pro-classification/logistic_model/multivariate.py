import numpy as np
from tqdm import tqdm


class OneVsAll:
    
    def __init__(self, type_clf, **kargs):
        self.__type_clf = type_clf
        self.__kargs = kargs
        self.classifiers = dict()
        
    def fit(self, X, y):
        self.__y_unique = np.unique(y)
        for i in tqdm(range(self.__y_unique.shape[0])):
            c = self.__y_unique[i]
            if self.__kargs:
                clf = self.__type_clf(self.__kargs)
            else:
                clf = self.__type_clf()
            y_c = np.array([1 if label == c else 0 for label in y])
            clf.fit(X, y_c)
            self.classifiers[c] = clf
     
    def predict(self, X):
        y_pred = np.zeros(X.shape[0])
        y_prob = np.zeros(X.shape[0])
        for c in self.__y_unique:
            y_p = self.classifiers[c].predict_prob(X)
            for i in range(X.shape[0]):
                if y_p[i] > y_prob[i]:
                    y_prob[i] = y_p[i]
                    y_pred[i] = c
        return y_pred