import numpy as np


class TwoPlayersGameState:
    x = 1
    o = -1

    def __init__(self, state, next_to_move):
        self.state = state
        self.next_to_move = next_to_move

    def __str__(self):
        return str(self.state)

    def game_result(self):
        raise NotImplemented("Implement game_result function")

    def is_game_over(self):
        raise NotImplemented("Implement is_game_over function")

    def pass_(self):
        raise NotImplemented("Implement give_up function")

    def move(self, action):
        raise NotImplemented("Implement move function")

    def get_legal_actions(self):
        raise NotImplemented("Implement get_legal_actions function")

    def get_next_move(self):
        return TwoPlayersGameState.o if self.next_to_move == TwoPlayersGameState.x else TwoPlayersGameState.x


class Action:

    def __init__(self, x_coordinate, y_coordinate, player):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.player = player

    def __repr__(self):
        return "player:" + str(self.player) + " x:" + str(self.x_coordinate) + " y:" + str(self.y_coordinate)

    def __eq__(self, other):
        return self.x_coordinate == other.x_coordinate \
               and self.y_coordinate == other.y_coordinate \
               and self.player == other.player

    def __iter__(self):
        return iter((self.x_coordinate, self.y_coordinate, self.player))

    def __hash__(self):
        return int(self.player * (self.x_coordinate * 8 + self.y_coordinate))


def where(condition):
    res = np.where(condition)
    return zip(res[0], res[1])
