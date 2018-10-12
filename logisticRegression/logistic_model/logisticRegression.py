import numpy as np
import scipy.optimize as opt
from .cost import *


class LogisticRegression:
    
    def __init__(self):
        self.W = None
    
    @staticmethod
    def argmented(M):
        return np.column_stack((np.ones(M.shape[0]), M))

    def predict(self, X):
        X = self.argmented(X)
        prob = sigmoid(X.dot(self.W.T))
        return np.asarray([1 if p > 0.5 else 0 for p in prob])


class SimpleLogisticRegression(LogisticRegression):
    
    def fit(self, X, y):
        X = self.argmented(X)
        W = np.zeros(X.shape[1])
        result = opt.fmin_tnc(func=cross_entropy, x0=W, 
                              fprime=gradient_ce, args=(X, y))
        self.W = result[0]
        

class RegularizedLogisticRegression(LogisticRegression):
        
    def __init__(self, learning_rate):
        self.__learning_rate = learning_rate
    
    def fit(self, X, y):
        X = self.argmented(X)
        W = np.zeros(X.shape[1])
        result = opt.fmin_tnc(func=regularized_cross_entropy, x0=W, 
                              fprime=regularized_gradient_ce, args=(X, y, self.__learning_rate))
        self.W = result[0]
    