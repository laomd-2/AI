from board import Board
from enum import Enum


class Flag(Enum):
    EXACT = 0
    LOWERBOUND = 1
    UPPERBOUND = 2


class Entry:
    def __init__(self):
        self.value = self.flag = self.depth = None


class ZeroSum:
    INF = float("inf")

    def __init__(self, board, evaluation, first=True):
        self._board = board
        self._evaluation = evaluation
        self._me = self.get_player_char(first)[0]
        self._table = dict()

    def decide_and_drop(self, remain_depth=-1):
        move = self._decide(remain_depth)
        if move is not None:
            self._board.apply_move(move, self._me)
        else:
            move = "cannot move"
        return move

    def _decide(self, remain_depth):
        return None

    def search_internal(self, remain_depth, alpha, beta, *args):
        raise Exception("not implemented")

    def search(self, remain_depth, alpha, beta, *args):
        s_board = str(self._board)
        entry = self._table.get(s_board, None)
        if entry is not None and entry.depth >= remain_depth:
            if entry.flag == Flag.EXACT:
                return entry.value, None
            elif entry.flag == Flag.LOWERBOUND:
                alpha = max(alpha, entry.value)
            else:
                beta = min(beta, entry.value)
            if alpha >= beta:
                return entry.value, None
        alpha_orig = alpha
        beta_orig = beta

        value, move = self.search_internal(remain_depth, alpha, beta, args)

        entry = Entry()
        entry.value = value
        entry.depth = remain_depth
        if value <= alpha_orig:
            entry.flag = Flag.UPPERBOUND
        elif value >= beta_orig:
            entry.flag = Flag.LOWERBOUND
        else:
            entry.flag = Flag.EXACT
        self._table[s_board] = entry
        return value, move

    @staticmethod
    def get_player_char(first):
        if first:
            return Board.FIRST, Board.SECOND
        else:
            return Board.SECOND, Board.FIRST
