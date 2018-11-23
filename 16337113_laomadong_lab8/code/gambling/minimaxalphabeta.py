from board import Board
from gambling.zero_sum import ZeroSum


class MinimaxAlphaBeta(ZeroSum):

    def __init__(self, board, evaluation, first=True):
        super(MinimaxAlphaBeta, self).__init__(board, evaluation, first)
        self._is_max = first

    def _decide(self, remain_depth):
        return self._minimax(remain_depth, -self.INF, self.INF, self._is_max)[1]

    def _minimax(self, remain_depth, alpha, beta, ismax):
        best_move = None
        best_score = -self.INF
        if not ismax:
            best_score = self.INF
        char, opp_char = self.get_player_char(ismax)
        if remain_depth == 0:
            best_score = self._evaluation(self._board)
        else:
            moves_list = self._board.generate_moves(char)
            if moves_list:
                for move in moves_list:
                    all_reverse = self._board.apply_move(move, char, False)
                    chosen_score = self._minimax(remain_depth - 1, alpha, beta, not ismax)[0]
                    for p in all_reverse:
                        self._board[p] = opp_char
                    if all_reverse:
                        self._board[move] = Board.BLANK
                    if ismax:
                        if best_score < chosen_score:
                            best_score = chosen_score
                            best_move = move
                            alpha = max(alpha, best_score)
                            if alpha >= beta:
                                break
                    else:
                        if best_score > chosen_score:
                            best_score = chosen_score
                            best_move = move
                            beta = min(beta, best_score)
                            if alpha >= beta:
                                break
            else:
                best_score = self._evaluation(self._board)
        return best_score, best_move

