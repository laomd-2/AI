import numpy as np
from point import where, Point


class Board:

    def __init__(self, board, first='O', second='X', blank='*'):
        self.__board = board
        self.__players = first + second
        self.__now = False
        self.__blank = blank

    def __str__(self):
        char = self.__players[int(self.__now)]
        moves = self.generate_moves(char)
        str_type = ''
        n = self.__board.shape[0]
        for i in range(n):
            for j in range(n):
                pos = (i, j)
                if pos in moves:
                    str_type += '+ '
                else:
                    str_type += self.__board[pos] + ' '
            str_type += '\n'
        return str_type

    def __setitem__(self, key, value):
        self.__board[key] = value

    def _is_valid(self, pos):
        i, j = pos
        n = self.__board.shape[0]
        return 0 <= i < n and 0 <= j < n

    def _reverse_pos(self, chess_pos):
        char = self.__board[chess_pos]
        moves = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    continue
                cnt = 0
                pos = chess_pos + (i, j)
                while self._is_valid(pos):
                    if self.__board[pos] == self.__blank:
                        if cnt > 0:
                            moves.append(pos)
                        break
                    if self.__board[pos] != char:
                        cnt += 1
                    else:
                        break
                    pos = pos + (i, j)
        return moves

    def where(self, char):
        return self.__board[self.__board == char]

    def generate_moves(self, char):
        all_moves = set()
        for chess_pos in where(self.__board == char):
            all_moves.update(self._reverse_pos(chess_pos))
        return all_moves

    def apply_move(self, move, char, flag=True):
        res = self._apply_move(move, char)
        if flag and res:
            self.__now = not self.__now
        return res

    def _apply_move(self, move, char):
        if self.__board[move] != self.__blank:
            return []
        all_reverse = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    continue
                can_reverse = []
                pos = move + (i, j)
                while self._is_valid(pos) and self.__board[pos] != self.__blank:
                    if self.__board[pos] != char:
                        can_reverse.append(pos)
                    else:
                        break
                    pos = pos + (i, j)
                else:
                    can_reverse.clear()
                all_reverse += can_reverse
                for pos in can_reverse:
                    self.__board[pos] = char
        if all_reverse:
            self.__board[move] = char
        return all_reverse

    def score(self):
        max_chesses = self.where(self.__players[0])
        min_chesses = self.where(self.__players[1])
        return max_chesses.size - min_chesses.size

    def game_over(self):
        return not self.generate_moves(self.__players[0]) and not self.generate_moves(self.__players[1])
