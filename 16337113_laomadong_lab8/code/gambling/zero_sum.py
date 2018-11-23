from board import Board


class ZeroSum:
    INF = float("inf")

    def __init__(self, board, evaluation, first=True):
        self._board = board
        self._evaluation = evaluation
        self._me = self.get_player_char(first)[0]

    def decide_and_drop(self, remain_depth=-1):
        move = self._decide(remain_depth)
        if move is not None:
            self._board.apply_move(move, self._me)
        else:
            move = "cannot move"
        return move

    def _decide(self, remain_depth):
        return None

    @staticmethod
    def get_player_char(first):
        if first:
            return Board.FIRST, Board.SECOND
        else:
            return Board.SECOND, Board.FIRST
