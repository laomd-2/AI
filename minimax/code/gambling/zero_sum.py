from board import Board
from enum import Enum
import json


class Flag(Enum):
    VALUE = 0
    ALPHA = 1
    BETA = 2


class Entry:
    def __init__(self):
        self.value = self.flag = self.depth = self.move = None


class ZeroSum:
    INF = float("inf")

    def __init__(self, board, char, evaluation):
        self._board = board
        self._evaluation = evaluation
        self._me = char
        self._table = dict()

    def _search_internal(self, remain_depth, char, opp_char, alpha, beta, **kwargs):
        raise Exception("not implemented")

    def search(self, remain_depth, alpha=-INF, beta=INF, **kwargs):
        # s_board = str(self._board)
        # entry = self._table.get(s_board, None)
        # if entry is not None and entry.depth >= remain_depth:
        #     if entry.flag == Flag.VALUE:
        #         return entry.value, entry.move
        #     elif entry.flag == Flag.ALPHA:
        #         alpha = max(alpha, entry.value)
        #     else:
        #         beta = min(beta, entry.value)
        #     if alpha >= beta:
        #         return entry.value, entry.move
        # alpha_orig = alpha
        # beta_orig = beta

        if self._me == Board.FIRST:
            opp_char = Board.SECOND
        else:
            opp_char = Board.FIRST
        value, move = self._search_internal(remain_depth, self._me, opp_char, alpha, beta, **kwargs)

        # entry = Entry()
        # entry.value = value
        # entry.move = move
        # entry.depth = remain_depth
        # if value <= alpha_orig:
        #     entry.flag = Flag.BETA
        # elif value >= beta_orig:
        #     entry.flag = Flag.ALPHA
        # else:
        #     entry.flag = Flag.VALUE
        # self._table[s_board] = entry
        return value, move

    def get_player_char(self, even_level):
        opp_char = Board.SECOND if self._me == Board.FIRST else Board.FIRST
        if even_level:
            return self._me, opp_char
        else:
            return opp_char, self._me
