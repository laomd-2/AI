from board import Board
from gambling.minimax import MiniMax


class AlphaBeta(MiniMax):

    def _alpha_beta_pruning(self, remain_depth, alpha, beta, is_max):
        best_move = None
        best_score = self.INF
        if is_max:
            best_score = -best_score
        char, opp_char = self.get_player_char(is_max)
        if remain_depth == 0:
            best_score = self._evaluation()
        else:
            moves_list = self._board.generate_moves(char)
            if moves_list:
                for move in moves_list:
                    all_reverse = self._board.apply_move(move, char, False)
                    chosen_score = self._alpha_beta_pruning(remain_depth - 1, alpha, beta, not is_max)[0]
                    for p in all_reverse:
                        self._board[p] = opp_char
                    if all_reverse:
                        self._board[move] = Board.BLANK
                    if is_max:
                        if chosen_score > best_score:
                            best_score = chosen_score
                            best_move = move
                        alpha = max(alpha, best_score)
                    else:
                        if chosen_score < best_score:
                            best_score = chosen_score
                            best_move = move
                        beta = min(beta, best_score)
                    if alpha >= beta:
                        break
            else:
                best_score = self._evaluation()
        return best_score, best_move

    def decide_and_drop(self, remain_depth=-1):
        move = self._alpha_beta_pruning(remain_depth, -self.INF, self.INF, self._ismax)[1]
        if move is not None:
            self._board.apply_move(move, self._me)
        else:
            move = "cannot move"
        return move
