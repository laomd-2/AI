import numpy as np
import scipy.optimize as opt
from cost import sigmoid, cross_entropy, gradient_ce


class LogisticRegression:
    
    def __init__(self):
        self.__W = None
    
    @staticmethod
    def argmented(M):
        return np.column_stack((np.ones(M.shape[0]), M))
        
    def fit(self, X, y):
        X = self.argmented(X)
        W = np.zeros(X.shape[1])
        result = opt.fmin_tnc(func=cross_entropy, x0=W, 
                              fprime=gradient_ce, args=(X, y))
        self.__W = result[0]

    def predict(self, X):
        X = self.argmented(X)
        prob = sigmoid(X.dot(self.__W.T))
        return np.asarray([1 if p > 0.5 else 0 for p in prob])