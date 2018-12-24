import numpy as np
from games.common import TwoPlayersGameState, Action


class TicTacToeMove(Action):

    def __init__(self, x_coordinate, y_coordinate, value):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.value = value

    def __repr__(self):
        return "x:" + str(self.x_coordinate) + " y:" + str(self.y_coordinate) + " v:" + str(self.value)


class TicTacToeGameState(TwoPlayersGameState):
    x = 1
    o = -1

    def __init__(self, state, next_to_move=1):
        super(TicTacToeGameState, self).__init__(state, next_to_move)
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Please play on 2D square board")
        self.board_size = state.shape[0]

    @property
    def game_result(self):
        # check if game is over
        rowsum = np.sum(self.state, 0)
        colsum = np.sum(self.state, 1)
        diag_sum_tl = self.state.trace()
        diag_sum_tr = self.state[::-1].trace()

        if any(rowsum == self.board_size) or any(
                colsum == self.board_size) or diag_sum_tl == self.board_size or diag_sum_tr == self.board_size:
            return 1.
        elif any(rowsum == -self.board_size) or any(
                colsum == -self.board_size) or diag_sum_tl == -self.board_size or diag_sum_tr == -self.board_size:

            return -1.
        elif np.all(self.state != 0):
            return 0.
        else:
            # if not over - no result
            return None

    def is_game_over(self):
        return self.game_result is not None

    def is_move_legal(self, move):
        # check if correct player moves
        if move.value != self.next_to_move:
            return False

        # check if inside the board
        x_in_range = self.board_size > move.x_coordinate >= 0
        if not x_in_range:
            return False

        # check if inside the board
        y_in_range = self.board_size > move.y_coordinate >= 0
        if not y_in_range:
            return False

        # finally check if board field not occupied yet
        return self.state[move.x_coordinate, move.y_coordinate] == 0

    def move(self, move):
        if not self.is_move_legal(move):
            raise ValueError("move " + move + " on board " + self.state + " is not legal")
        new_board = np.copy(self.state)
        new_board[move.x_coordinate, move.y_coordinate] = move.value
        next_to_move = TicTacToeGameState.o if self.next_to_move == TicTacToeGameState.x else TicTacToeGameState.x
        return TicTacToeGameState(new_board, next_to_move)

    def get_legal_actions(self):
        indices = np.where(self.state == 0)
        return [TicTacToeMove(coords[0], coords[1], self.next_to_move) for coords in list(zip(indices[0], indices[1]))]

    def __str__(self):
        return str(self.state)
