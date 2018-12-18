from point import where


class Board:
    FIRST = 1
    SECOND = -1
    BLANK = 0

    def __init__(self, board):
        self.__board = board
        self.__now = False

    def __str__(self):
        char = (self.FIRST, self.SECOND)[int(self.__now)]
        show = 'X*O'
        moves = self.generate_moves(char)
        str_type = ''
        n = self.__board.shape[0]
        for i in range(n):
            for j in range(n):
                pos = (i, j)
                if pos in moves:
                    str_type += '+ '
                else:
                    str_type += show[self.__board[pos] + 1] + ' '
            str_type += '\n'
        return str_type.rstrip('\n')

    def __setitem__(self, key, value):
        self.__board[key] = value

    def __getitem__(self, item):
        return self.__board[item]

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
                    if self.__board[pos] == self.BLANK:
                        if cnt > 0:
                            moves.append(pos)
                        break
                    if self.__board[pos] != char:
                        cnt += 1
                    else:
                        break
                    pos = pos + (i, j)
        return moves

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
        if self.__board[move] != self.BLANK:
            return []
        all_reverse = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    continue
                can_reverse = []
                pos = move + (i, j)
                while self._is_valid(pos) and self.__board[pos] != self.BLANK:
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

    def getState(self):
        return self.__board

    def game_over(self):
        return not self.generate_moves(self.FIRST) and not self.generate_moves(self.SECOND)
