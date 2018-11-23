from board import Board
from gambling.zero_sum import ZeroSum


class NegamaxAlphaBeta(ZeroSum):

    def __init__(self, board, evaluation, first=True):
        super(NegamaxAlphaBeta, self).__init__(board, evaluation, first)
        self._color = 1 if first else -1

    def _decide(self, remain_depth):
        return self._negamax(remain_depth, -self.INF, self.INF, self._color)[1]

    def _negamax(self, remain_depth, alpha, beta, color):
        best_move = None
        best_score = -self.INF
        char, opp_char = self.get_player_char(color == 1)
        if remain_depth == 0:
            best_score = color * self._evaluation(self._board)
        else:
            moves_list = self._board.generate_moves(char)
            if moves_list:
                for move in moves_list:
                    all_reverse = self._board.apply_move(move, char, False)
                    chosen_score = self._negamax(remain_depth - 1, -beta, -alpha, -color)[0]
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

