import random
from baseline.negamaxalphabeta import NegamaxAlphaBeta
from baseline.evaluations import NNEvaluation
from sklearn.externals import joblib
from mcts.node import *
from mcts.search import MonteCarloTreeSearch
from games.othello import OthelloGameState


random.seed()
np.random.seed()
evaluation = NNEvaluation(joblib.load('data/NNRegressor.pkl'))

win = 0
for i in range(10):
    me = TwoPlayersGameState.x
    if i % 2 == 0:
        me = TwoPlayersGameState.o

    print('round', i)
    board = np.loadtxt('data/board8.txt', dtype=int)
    initial_board_state = OthelloGameState(board)

    while not initial_board_state.is_game_over():
        if initial_board_state.next_to_move == me:
            root = Node(state=initial_board_state, action=None, parent=None)
            computer = MonteCarloTreeSearch(root)
            move = computer.search(20)
        else:
            computer = NegamaxAlphaBeta(initial_board_state, evaluation)
            move = computer.search(5)
        if move is None:
            initial_board_state = initial_board_state.pass_()
        else:
            initial_board_state = initial_board_state.move(move)
    res = initial_board_state.game_result()
    print(res, 'win' if res * me > 0 else 'lose')
    win += res * me > 0
print('win', win, 'times')

