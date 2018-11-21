from point import Point
from board import Board
from minimax import MiniMax
import numpy as np


if __name__ == '__main__':
    first, second = 'O', 'X'
    board = Board(np.array(np.loadtxt("../data/board.txt", dtype=str)), first, second, '*')
    computer = MiniMax(board, second, first, '*', False)
    turn = 0
    print(board)
    while not board.game_over():
        if turn == 0:
            move = tuple(map(int, input("your turn:").split(' ')))
            while not board.apply_move(Point(move), first):
                move = tuple(map(int, input("invalid move, input again:").strip().split(' ')))
        else:
            print("computer thinking...", end=' ')
            move = computer.decide()
            if move is not None:
                print(move)
                board.apply_move(move, second)
            else:
                print("cannot move")
        turn = not turn
        print(board)
    score = board.score()
    if score > 0:
        print(first, "win!")
    elif score < 0:
        print(second, "win!")
    else:
        print("平局")
