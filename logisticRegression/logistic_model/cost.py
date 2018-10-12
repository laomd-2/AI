import numpy as np


def acc(y, y_pred):
    return y[y == y_pred].size / y.size

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def cross_entropy(W, X, y):
    W = np.ravel(W)
    y = np.ravel(y)
    h_x = sigmoid(X.dot(W.T))
    first = np.multiply(-y, np.log(h_x))
    second = np.multiply(1-y, np.log(1 - h_x))
    return np.sum(first - second) / len(X)

def regularized_cross_entropy(W, X, y, learning_rate):
    ce = cross_entropy(W, X, y)
    W = np.ravel(W)
    y = np.ravel(y)
    reg = (learning_rate / 2 * len(X)) * np.sum(np.power(W[1:W.shape[0]], 2))
    return ce + reg

def gradient_ce(W, X, y):
    W = np.ravel(W)
    y = np.ravel(y)
    error = sigmoid(X.dot(W.T)) - y
    grad = np.sum(np.multiply(error, X.T).T, axis=0)
    return grad / len(X)

def regularized_gradient_ce(W, X, y, learning_rate):
    W = np.ravel(W)
    y = np.ravel(y)
    error = sigmoid(X.dot(W.T)) - y
    grad = np.sum(np.multiply(error, X.T).T, axis=0) + learning_rate * W
    return grad / len(X)
