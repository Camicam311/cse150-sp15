# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

import heapq

from assignment2 import Player


class EvaluationPlayer(Player):
    def move(self, state):
        """Calculates the best move after 1-ply look-ahead with a simple evaluation function.

        Args:
            state (State): The current state of the board.

        Returns:
            the next move (Action)
        """

        # *You do not need to modify this method.*
        best_move = None
        max_value = -1.0
        my_color = state.to_play.color

        for action in state.actions():
            if self.is_time_up():
                break

            result_state = state.result(action)
            value = self.evaluate(result_state, my_color)
            if value > max_value:
                max_value = value
                best_move = action

        # Return the move with the highest evaluation value
        return best_move

    def evaluate(self, state, color):
        """Evaluates the state for the player with the given stone color.

        This function calculates the length of the longest ``streak'' on the board
        (of the given stone color) divided by K.  Since the longest streak you can
        achieve is K, the value returned will be in range [1 / state.K, 1.0].

        Args:
            state (State): The state instance for the current board.
            color (int): The color of the stone for which to calculate the streaks.

        Returns:
            the evaluation value (float), from 1.0 / state.K (worst) to 1.0 (win).
        """
        # Row search
        max_row_sum = -1.0
        max_col_sum = -1.0
        diag_max_sum_dr = 0.0
        diag_max_sum_ul = 0.0

        for row in state.board:
            max_row_sum = max(sum([1 for pos in row if pos==color]),max_row_sum)
      
        # Column search
        for j in range(len(state.board[0])):
            col_list = []
            for i in range(len(state.board)):
                if state.board[i][j] == color:
                    col_list.append(1)
            max_col_sum = max(sum(col_list),max_col_sum)

        # Diag search
        diag_count = len(state.board[0]) + len(state.board) - 1
        diag_x_s, diag_y_s = (0,0)
        x,y = (diag_x_s,diag_y_s)
        # up left
        for z in range(diag_count):
            cur_total = 0
            while(x >= 0 and y <= len(state.board[0]) - 1):
                if state.board[x][y] == color:
                    cur_total += 1
                x -= 1
                y += 1

            if diag_x_s < len(state.board) - 1:
                diag_x_s += 1
            else:
                diag_y_s += 1

            x,y = (diag_x_s,diag_y_s)
            diag_max_sum_ul = max(diag_max_sum_ul, cur_total)

        # down right
        diag_x_s, diag_y_s = (len(state.board[0])-1,0)
        x,y = (diag_x_s,diag_y_s)
        for z in range(diag_count):
            cur_total = 0
            while(x <= len(state.board[0])-1 and y <= len(state.board) - 1):
                if state.board[y][x] == color:
                    cur_total += 1
                x += 1
                y += 1

            if diag_x_s > 0:
                diag_x_s -= 1
            else:
                diag_y_s += 1

            x,y = (diag_x_s,diag_y_s)
            diag_max_sum_dr = max(diag_max_sum_dr, cur_total)

        return (max(diag_max_sum_dr, diag_max_sum_ul, max_col_sum, max_row_sum))/state.K
