import numpy as np
import math


def gradient_decent(Xs, Ys, f, Ws=None, rate=0.1, times=-1, precision=0.000001):
    Xs = [np.asarray([1] + list(i)) for i in Xs]
    dimension = len(Xs[0])
    if Ws is None:
        Ws = np.asarray(np.random.rand(dimension), dtype=np.float)
    else:
        Ws = np.asarray(Ws, dtype=np.float)
    last_Ws = None

    while times != 0:
        if last_Ws is not None:
            if np.fabs(Ws - last_Ws).max() < precision:
                break
        last_Ws = Ws
        derivatives = f(Ws, Xs, Ys)
        for i in range(dimension):
            Ws[i] -= rate * derivatives[i]
        times -= 1
    return Ws


def sigmoid(x):
    ex = math.pow(math.e, x)
    return ex / (1 + ex)


class LogisticRegression:

    @staticmethod
    def derivative(Ws, Xs, Ys):
        dimension = len(Ws)
        tmps = []
        for X_i, Y_i in zip(Xs, Ys):
            tmps.append(sigmoid(Ws.dot(X_i.T)) - Y_i)
        res = []
        for i in range(dimension):
            res.append(0)
            for j, X_i in enumerate(Xs):
                res[-1] += tmps[j] * X_i[i]
        return res

    def fit(self, x, y):
        self.Ws = gradient_decent(x, y, self.derivative)
        print(self.Ws)

    def predict(self, x):
        x = np.asarray([1] + list(x))
        p = sigmoid(self.Ws.dot(x))
        return int(p > 0.5)


if __name__ == '__main__':
    model = LogisticRegression()
    Xs = [(0, 1), (1, 1), (3, 3), (4, 3)]
    model.fit(Xs, [0, 0, 1, 1])
    while True:
        x = map(int, input().split(' '))
        print(model.predict(x))
