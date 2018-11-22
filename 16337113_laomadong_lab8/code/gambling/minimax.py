from board import Board


class MiniMax:
    INF = float("inf")

    def __init__(self, board, first=True):
        self._board = board
        self._ismax = first
        self._me = self.get_player_char(first)[0]

    def _evaluation(self):
        return self._board.score()

    def decide_and_drop(self, remain_depth=-1):
        move = self._minimax(remain_depth, self._ismax)[1]
        if move is not None:
            self._board.apply_move(move, self._me)
        else:
            move = "cannot move"
        return move

    @staticmethod
    def get_player_char(first):
        if first:
            return Board.FIRST, Board.SECOND
        else:
            return Board.SECOND, Board.FIRST

    def _minimax(self, remain_depth, is_max):
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
                    chosen_score = self._minimax(remain_depth - 1, not is_max)[0]
                    for p in all_reverse:
                        self._board[p] = opp_char
                    if all_reverse:
                        self._board[move] = Board.BLANK
                    if is_max:
                        if chosen_score > best_score:
                            best_score = chosen_score
                            best_move = move
                    else:
                        if chosen_score < best_score:
                            best_score = chosen_score
                            best_move = move
            else:
                best_score = self._evaluation()
        return best_score, best_move

