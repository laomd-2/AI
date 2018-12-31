from mcts.node import *
from mcts.search import MonteCarloTreeSearch
from games.othello import OthelloGameState, OthelloAction


random.seed()
np.random.seed()
#
# win = 0
# for i in range(100):
#
#     win += res < 0
# print('win', win, 'times')
# print('round', i)
board = np.loadtxt('data/board8.txt', dtype=int)
initial_board_state = OthelloGameState(board, next_to_move=1)

while not initial_board_state.is_game_over():
    print(initial_board_state)
    print()
    move = None
    if initial_board_state.next_to_move == TwoPlayersGameState.x:
        root = TwoPlayersGameMonteCarloTreeSearchNode(state=initial_board_state, action=None, parent=None)
        mcts = MonteCarloTreeSearch(root)
        best_node = mcts.search(50)
        if best_node:
            move = best_node.action
    else:
        move = None
        try:
            tmp = list(map(int, input("(i, j): ").strip().split()))
            move = OthelloAction(tmp[0], tmp[1], initial_board_state.next_to_move)
        except Exception as e:
            print(e)
    print(move)
    if move is None:
        initial_board_state = initial_board_state.pass_()
    else:
        initial_board_state = initial_board_state.move(move)
    print('score', initial_board_state.game_result())
print(initial_board_state)
res = initial_board_state.game_result()
print(res)