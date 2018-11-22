from board import Board
from gambling.minimax import MiniMax
from gambling.alpha_beta import AlphaBeta
import numpy as np


if __name__ == '__main__':
    board = Board(np.array(np.loadtxt("../data/board.txt", dtype=str)))
    computers = [MiniMax(board, True), AlphaBeta(board, False)]
    turn = 0
    print(board)
    while not board.game_over():
        computer = computers[turn]
        print(computer.__class__.__name__, "thinking...", end=' ')
        print(computer.decide_and_drop())
        turn = not turn
        print(board)
    score = board.score()
    if score > 0:
        print(board.FIRST, "win!")
    elif score < 0:
        print(board.SECOND, "win!")
    else:
        print("平局")
