import numpy as np


class GreedyEvaluation:

    def __call__(self, board):
        return np.sum(board.getState())


class FeatureEvaluation:

    def __init__(self):
        self._position_values = np.array(
            [
                [10, 2, 4, 4, 4, 4, 2, 10],
                [2, 0, 0, 0, 0, 0, 0, 2],
                [4, 0, 2, 1, 1, 2, 0, 4],
                [4, 0, 1, 0, 0, 1, 0, 4],
                [4, 0, 1, 0, 0, 1, 0, 4],
                [4, 0, 2, 1, 1, 2, 0, 4],
                [2, 0, 0, 0, 0, 0, 0, 2],
                [10, 2, 4, 4, 4, 4, 2, 10]
            ])

    def __call__(self, board):
        return (.7*np.sum(board.getState()) + .3*np.dot(board.getState(), self._position_values))/75


class NNEvaluation:
    def __init__(self, clf):
        self.clf = clf
    
    def __call__(self, board):
        return self.clf.predict([board.getState().flatten()])[0]
