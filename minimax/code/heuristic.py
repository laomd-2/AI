import math


def difference(board):
    score = board.score()
    return score[0] - score[1]


def sigmoid(board):
    score = board.score()
    e = math.exp(score[0] - score[1])
    return e / (e + 1)
