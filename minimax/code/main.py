from sklearn.externals import joblib
from gambling.evaluations import *
from gambling.player import *


if __name__ == '__main__':
    board = Board(np.array(np.loadtxt("../data/board8.txt", dtype=int)))
    clf = joblib.load('../data/NNRegressor.pkl')
    computers = [HumanPlayer(Board.FIRST, board),
                 SearchPlayer(board.SECOND, board, NNEvaluation(clf))]
    turn = 0
    print(board)
    print()
    while not board.game_over():
        computer = computers[turn]
        print("computer", turn + 1, "thinking...", end=' ')
        print(computer.play())
        turn = not turn
        print(board)
        print()
