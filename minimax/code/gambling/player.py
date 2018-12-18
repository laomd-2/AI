import random
from gambling.negamaxalphabeta import NegamaxAlphaBeta
from board import Board
from copy import deepcopy
from point import Point


class PlayerBase:
    def __init__(self, char, board):
        self.char = char
        self.board = board

    def decide(self):
        return None

    def play(self):
        move = self.decide()
        if move is not None:
            self.board.apply_move(move, self.char)
            return move
        else:
            return "can not move"


class RandomPlayer(PlayerBase):

    def decide(self):
        plays = self.board.generate_moves(self.char)
        if plays:
            return random.choice(list(plays))


class HumanPlayer(PlayerBase):

    def decide(self):
        valids = self.board.generate_moves(self.char)
        while True:
            try:
                pos = Point(tuple(map(int, input("position:").strip().split())))
                if pos in valids:
                    return pos
            except:
                pass


class SearchPlayer(PlayerBase):

    def __init__(self, char, board, evaluation):
        super(SearchPlayer, self).__init__(char, board)
        self._policy = NegamaxAlphaBeta(board, char, evaluation)

    def decide(self):
        res = self._policy.search(8, self.char, color=1 if self.char == Board.FIRST else -1)
        print(res[0])
        return res[1]


class MLPlayer(PlayerBase):
    def __init__(self, char, board, evaluation):
        super(MLPlayer, self).__init__(char, board)
        self.evaluation = evaluation

    def decide(self):
        plays = self.board.generate_moves(self.char)
        bestPlay = None
        if self.char == Board.FIRST:
            bestValue = -1000
            for play in plays:
                board = deepcopy(self.board)
                board.apply_move(play, self.char)
                value = self.evaluation(board)
                if value > bestValue:
                    bestPlay = play
                    bestValue = value
        else:
            bestValue = 1000
            for play in plays:
                board = deepcopy(self.board)
                board.apply_move(play, self.char)
                value = self.evaluation(board)
                if value < bestValue:
                    bestPlay = play
                    bestValue = value
        print(bestValue)
        return bestPlay
