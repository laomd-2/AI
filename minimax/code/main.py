from board import Board
from point import Point
from gambling.negamaxalphabeta import NegamaxAlphaBeta
from gambling.minimaxalphabeta import MinimaxAlphaBeta
import numpy as np
from heuristic import difference, sigmoid


if __name__ == '__main__':
    board = Board(np.array(np.loadtxt("../data/board8.txt", dtype=str)))
    # computers = [NegamaxAlphaBeta(board, sigmoid, True), MinimaxAlphaBeta(board, sigmoid, False)]
    computer = NegamaxAlphaBeta(board, difference, True)
    turn = 0
    print(board)
    print()
    while not board.game_over():
        # computer = computers[turn]
        if turn == 0:
            print("computer", turn + 1, "thinking...", end=' ')
            print(computer.decide_and_drop(8))
        else:
            move = tuple(map(int, input("your turn:").strip().split()))
            board.apply_move(Point(move), Board.SECOND)
        turn = not turn
        print(board)
        print("score:", difference(board))
        print()
    score = difference(board)
    if score > 0:
        print(board.FIRST, "win!")
    elif score < 0:
        print(board.SECOND, "win!")
    else:
        print("平局")
