import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.externals import joblib
from board import Board
from player import RandomPlayer
from evaluations import *

X = []
Y = []
board = Board(np.array(np.loadtxt("../../data/board8.txt", dtype=int)))
evaluation = FeatureEvaluation()
for i in range(1000):
    board = Board(np.array(np.loadtxt("../../data/board8.txt", dtype=int)))
    players = [RandomPlayer(Board.FIRST, board), RandomPlayer(Board.SECOND, board)]
    who = 0
    ones = np.ones((8, 8), dtype=int)
    while not board.game_over():
        X.append(board.getState().flatten().tolist())
        Y.append(evaluation(board))
        players[who].play()
        who = not who
clf = MLPRegressor(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(64, 64, 64), random_state=1)
print(X[0], Y[0])
clf.fit(X, Y)
joblib.dump(clf, 'NNRegressor.pkl')