import numpy as np


def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def cross_entropy(W, X, y):
    h_x = sigmoid(X.dot(W.T))
    first = np.multiply(-y, np.log(h_x))
    second = np.multiply(1-y, np.log(1 - h_x))
    return np.sum(first - second) / len(X)

def gradient_ce(W, X, y):
    error = sigmoid(X.dot(W.T)) - y
    grad = np.zeros_like(W)
    for i in range(W.shape[0]):
        term = np.multiply(error, X[:, i])
        grad[i] += np.sum(term)
    return grad / len(X)