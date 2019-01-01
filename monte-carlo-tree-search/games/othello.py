import numpy as np
from games.common import TwoPlayersGameState, Action, where


class OthelloAction(Action):
    pass


class OthelloGameState(TwoPlayersGameState):
    BLANK = 0

    def __init__(self, state, next_to_move=TwoPlayersGameState.x):
        if len(state.shape) != 2 or state.shape[0] != state.shape[1]:
            raise ValueError("Please play on 2D square board")
        super(OthelloGameState, self).__init__(state, next_to_move)

    def __str__(self):
        show = 'O*X'
        moves = [(i, j) for i, j, _ in self.get_legal_actions()]
        str_type = '  0 1 2 3 4 5 6 7\n'
        n = self.state.shape[0]
        for i in range(n):
            str_type += str(i) + ' '
            for j in range(n):
                pos = (i, j)
                if pos in moves:
                    str_type += '+ '
                else:
                    str_type += show[self.state[pos] + 1] + ' '
            str_type += '\n'
        return str_type.rstrip('\n')

    def game_result(self):
        return np.sum(self.state)

    def is_game_over(self):
        if not self.get_legal_actions():
            tmp = self.next_to_move
            self.next_to_move = self.get_next_move()
            over = not self.get_legal_actions()
            self.next_to_move = tmp
            return over
        return False

    def is_move_legal(self, move):
        res = self.get_legal_actions()
        return move in res

    def pass_(self):
        return OthelloGameState(np.copy(self.state), self.get_next_move())

    def move(self, action):
        if not self.is_move_legal(action):
            raise ValueError("move " + str(action) + " on board \n" + str(self.state) + " is not legal")
        new_state = OthelloGameState(np.copy(self.state), self.get_next_move())
        new_state._apply_move(action)
        return new_state

    def _reverse_pos(self, x, y):
        char = self.state[x, y]
        moves = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    continue
                cnt = 0
                xx = x + i
                yy = y + j
                while self._is_valid(xx, yy):
                    if self.state[xx, yy] == self.BLANK:
                        if cnt > 0:
                            moves.append((xx, yy))
                        break
                    if self.state[xx, yy] != char:
                        cnt += 1
                    else:
                        break
                    xx += i
                    yy += j
        return moves

    def get_legal_actions(self):
        all_moves = set()
        for i, j in where(self.state == self.next_to_move):
            all_moves.update(self._reverse_pos(i, j))
        return [OthelloAction(coords[0], coords[1], self.next_to_move) for coords in all_moves]

    def _is_valid(self, i, j):
        n = self.state.shape[0]
        return 0 <= i < n and 0 <= j < n

    def _apply_move(self, move):
        x, y, char = move
        all_reverse = []
        for i in (-1, 0, 1):
            for j in (-1, 0, 1):
                if i == 0 and j == 0:
                    continue
                can_reverse = []
                xx = x + i
                yy = y + j
                while self._is_valid(xx, yy) and self.state[xx, yy] != self.BLANK:
                    if self.state[xx, yy] != char:
                        can_reverse.append((xx, yy))
                    else:
                        break
                    xx += i
                    yy += j
                else:
                    can_reverse.clear()
                all_reverse += can_reverse
                for pos in can_reverse:
                    self.state[pos] = char
        if all_reverse:
            self.state[x, y] = char
        return all_reverse
