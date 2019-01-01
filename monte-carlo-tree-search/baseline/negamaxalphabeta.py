from games.othello import OthelloGameState
from enum import Enum


class Flag(Enum):
    VALUE = 0
    ALPHA = 1
    BETA = 2


class Entry:
    def __init__(self):
        self.key = self.flag = self.depth = self.value = None


class NegamaxAlphaBeta:
    INF = float("inf")

    def __init__(self, state: OthelloGameState, evaluation):
        self.state = state
        self._evaluation = evaluation
        self._table = dict()

    def search(self, remain_depth):
        return self._search(self.state, remain_depth, self.state.next_to_move, self.state.get_next_move(),
                            -self.INF, self.INF, self.state.next_to_move)[1]

    def _search(self, state, remain_depth, char, opp_char, alpha, beta, color):
        alpha_orig = alpha
        entry: Entry = self._table.get(state, None)
        if entry is not None and entry.depth >= remain_depth:
            if entry.flag == Flag.VALUE:
                return entry.key, entry.value
            elif entry.flag == Flag.ALPHA:
                alpha = max(alpha, entry.key)
            else:
                beta = min(beta, entry.key)
            if alpha >= beta:
                return entry.key, entry.value

        best_move = None
        best_score = -self.INF
        if remain_depth == 0:
            best_score = color * self._evaluation(self.state)
        else:
            moves_list = state.get_legal_actions()
            if moves_list:
                for move in moves_list:
                    new_state = state.move(move)
                    chosen_score = self._search(new_state, remain_depth - 1, opp_char, char, -beta, -alpha, -color)[0]
                    if best_score < -chosen_score:
                        best_score = -chosen_score
                        best_move = move
                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        break
            else:
                best_score = color * self._evaluation(self.state)

        entry = Entry()
        entry.key = best_score
        entry.value = best_move
        entry.depth = remain_depth
        if best_score <= alpha_orig:
            entry.flag = Flag.BETA
        elif best_score >= beta:
            entry.flag = Flag.ALPHA
        else:
            entry.flag = Flag.VALUE
        self._table[state] = entry
        return best_score, best_move
