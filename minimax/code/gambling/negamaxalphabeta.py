from board import Board
from gambling.zero_sum import ZeroSum


class NegamaxAlphaBeta(ZeroSum):

    def __init__(self, board, char, evaluation):
        super(NegamaxAlphaBeta, self).__init__(board, char, evaluation)
        self._table = dict()

    def _search_internal(self, remain_depth, char, opp_char, alpha, beta, **kwargs):
        color = kwargs['color']
        best_move = None
        best_score = -self.INF
        if remain_depth == 0:
            best_score = color * self._evaluation(self._board)
        else:
            moves_list = self._board.generate_moves(char)
            if moves_list:
                for move in moves_list:
                    all_reverse = self._board.apply_move(move, char, False)
                    chosen_score = self._search_internal(remain_depth - 1, opp_char, char, -beta, -alpha, color=-color)[0]
                    for p in all_reverse:
                        self._board[p] = opp_char
                    if all_reverse:
                        self._board[move] = Board.BLANK
                    if best_score < -chosen_score:
                        best_score = -chosen_score
                        best_move = move
                    alpha = max(alpha, best_score)
                    if alpha >= beta:
                        break
            else:
                best_score = color * self._evaluation(self._board)
        return best_score, best_move

