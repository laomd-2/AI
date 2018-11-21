class MiniMax:

    def __init__(self, board, me='O', opp='X', blank='*', ismax=True):
        self.__board = board
        self.__me = me
        self.__opp = opp
        self.__blank = blank
        self.__ismax = ismax
        if ismax:
            self.__max_char, self.__min_char = self.__me, self.__opp
        else:
            self.__max_char, self.__min_char = self.__opp, self.__me

    def _evaluation(self):
        return self.__board.score()

    def decide(self, remain_depth=-1):
        return self._minimax(remain_depth, self.__ismax)[1]

    def _minimax(self, remain_depth, is_max):
        best_move = None
        best_score = float('inf')
        char = self.__min_char
        opp_char = self.__max_char
        if is_max:
            best_score = -best_score
            char = self.__max_char
            opp_char = self.__min_char
        if remain_depth == 0:
            best_score = self._evaluation()
        else:
            moves_list = self.__board.generate_moves(char)
            if moves_list:
                for move in moves_list:
                    all_reverse = self.__board.apply_move(move, char, False)
                    chosen_score = self._minimax(remain_depth - 1, not is_max)[0]
                    for p in all_reverse:
                        self.__board[p] = opp_char
                    if all_reverse:
                        self.__board[move] = self.__blank
                    if (is_max and chosen_score > best_score) or (not is_max and chosen_score < best_score):
                        best_score = chosen_score
                        best_move = move
            else:
                best_score = self._evaluation()
        return best_score, best_move
