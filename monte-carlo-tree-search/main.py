import random
from mcts.node import *
from mcts.search import MonteCarloTreeSearch
from games.othello import OthelloGameState


random.seed()
np.random.seed()

win = 0
for i in range(100):
    me = TwoPlayersGameState.x
    if i % 2 == 0:
        me = TwoPlayersGameState.o

    print('round', i)
    board = np.loadtxt('data/board8.txt', dtype=int)
    initial_board_state = OthelloGameState(board)

    while not initial_board_state.is_game_over():
        # print(initial_board_state)
        # print()
        move = None
        if initial_board_state.next_to_move == me:
            root = Node(state=initial_board_state, action=None, parent=None)
            mcts = MonteCarloTreeSearch(root)
            best_node = mcts.search(20)
            if best_node:
                move = best_node.action
        else:
            moves = initial_board_state.get_legal_actions()
            if moves:
                move = np.random.choice(moves)
        # print(move)
        if move is None:
            initial_board_state = initial_board_state.pass_()
        else:
            initial_board_state = initial_board_state.move(move)
        # print('score', initial_board_state.game_result())
    # print(initial_board_state)
    res = initial_board_state.game_result()
    print(res, 'win' if res * me > 0 else 'lose')
    win += res * me > 0
print('win', win, 'times')

