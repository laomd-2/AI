import numpy as np
import scipy.optimize as opt
from cost import *
from base import Validable


class LogisticRegression(Validable):
 
    @staticmethod
    def argmented(M):
        return np.column_stack((np.ones(M.shape[0]), M))
    
    def get_theta(self):
        pass
    
    def predict(self, X):
        prob = self.predict_prob(X)
        return np.asarray([1 if p > 0.5 else 0 for p in prob])
    
    def predict_prob(self, X):
        X = self.argmented(X)
        return sigmoid(X.dot(self.get_theta().T))

class SimpleLogisticRegression(LogisticRegression):
    
    def __init__(self):
        self.__W = None
    
    def get_theta(self):
        return self.__W
    
    def fit(self, X, y):
        X = self.argmented(X)
        W = np.zeros(X.shape[1])
        result = opt.fmin_tnc(func=cross_entropy, x0=W, 
                              fprime=gradient_ce, args=(X, y))
        self.__W = result[0]
        

class RegularizedLogisticRegression(LogisticRegression):
        
    def __init__(self, learning_rate):
        self.learning_rate = learning_rate
        self.__W = None
        
    def get_theta(self):
        return self.__W
    
    def fit(self, X, y):
        X = self.argmented(X)
        W = np.zeros(X.shape[1])
        result = opt.fmin_tnc(func=regularized_cross_entropy, x0=W, 
                              fprime=regularized_gradient_ce, args=(X, y, self.learning_rate))
        self.__W = result[0]
        return result[1]
