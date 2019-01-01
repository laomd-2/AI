import numpy as np


def search(initial_board_state):
    moves = initial_board_state.get_legal_actions()
    move = None
    if moves:
        move = np.random.choice(moves)
    return move
