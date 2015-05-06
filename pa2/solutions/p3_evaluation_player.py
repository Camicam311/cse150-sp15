# -*- coding: utf-8 -*-
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu,chriskweller@gmail.com'

# CSE 150 Assignment #2, Problem 3
# Description: Player class that uses the longest streak evaluation function to determine
# the best heuristic output possible to move to play in an mxn tic-tac-toe board.

from assignment2 import Player

# Evaluation Player class utilizes the supplied move function along with our 
# evaluation heuristic to make the best possible move we have available
class EvaluationPlayer(Player):

    # Supplied move function that handles the determination of the best move possible
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

        # Define variables for max sums for each search
        # (Max of row search, column search, diagonal down-right, diagonal down
        # left respectively.
        max_row_sum = -1.0
        max_col_sum = -1.0
        diag_max_sum_dr = 0.0
        diag_max_sum_ul = 0.0

        ### Row search ###

        # Iterate over every row
        for row in state.board:

            # Current sum and max sum for the row initialized to 0
            cur_sum = 0
            cur_max = 0

            # Iterate over every element in the row
            for it in row:

                # If the element matches our color, increment the count
                if it == color:
                    cur_sum += 1

                # Otherwise, perserve the max of current sum and the max in the row
                # And reset the current sum back down to zero
                else:
                    cur_max = max(cur_sum,cur_max)
                    cur_sum = 0

            # Perserve the max of the end of the row and the max thus far for all rows
            max_row_sum = max(max_row_sum, cur_max, cur_sum)

        ### Column search ###

        # Iterate over indexes in the range corresponding to the number of collumns
        for j in range(len(state.board[0])):
            
            # Current sum and max sum for the column initialized to 0
            cur_sum = 0
            cur_max = 0

            # Iterate over indexes in the range corresponding to the number of rows
            for i in range(len(state.board)):

                # If the element matches our color, increment the count
                if state.board[i][j] == color:
                    cur_sum += 1

                # Otherwise, perserve the max of current sum and the max in the column
                # And reset the current sum back down to zero
                else:
                    cur_max = max(cur_sum,cur_max)
                    cur_sum = 0
                    
            # Perserve the max of the end of the col and the max thus far for all cols
            max_col_sum = max(max_col_sum, cur_max, cur_sum)

        ### Diagonal search -- Up,left movement ###

        # Determine the number of diagonals in the current board, and initialize 
        # the starting positions
        diag_count = len(state.board[0]) + len(state.board) - 1
        diag_x_s, diag_y_s = (0,0)
        x,y = (diag_x_s,diag_y_s)

        # Iterate number_of_diagonals times
        for z in range(diag_count):

            # Current sum and max sum for the diagonal initialized to 0
            cur_max = 0
            cur_sum = 0

            # While our board index coordinates are within the bounds of the board...
            while(x >= 0 and y <= len(state.board[0]) - 1):

                # If the element matches our color, increment the count
                if state.board[x][y] == color:
                    cur_sum += 1

                # Otherwise, perserve the max of current sum and the max in the diagonal
                # And reset the current sum back down to zero
                else: 
                    cur_max = max(cur_max, cur_sum)
                    cur_sum = 0

                # Move our current indexing location up and left
                x -= 1
                y += 1
            
            # If the starting x location has reached the end of the board, shift
            # it over, otherwise shift our y position over
            if diag_x_s < len(state.board) - 1:
                diag_x_s += 1
            else:
                diag_y_s += 1

            # Reassign our initial indexing location to the appropriate start locations
            # for the diagonal
            x,y = (diag_x_s,diag_y_s)


            # Perserve the max of the end of the diagonal and the max thus far for 
            # all diagonals
            diag_max_sum_ul = max(cur_max, cur_sum, diag_max_sum_ul)

        ### Diagonal search -- Down,right movement ###

        # Initialize the starting positions for the diagonal search
        diag_x_s, diag_y_s = (len(state.board[0])-1,0)
        x,y = (diag_x_s,diag_y_s)

        # Iterate number_of_diagonals times
        for z in range(diag_count):

            # Current sum and max sum for the diagonal initialized to 0
            cur_max = 0
            cur_sum = 0

            # While our board index coordinates are within the bounds of the board...
            while(x <= len(state.board[0])-1 and y <= len(state.board) - 1):

                # If the element matches our color, increment the count
                if state.board[y][x] == color:
                    cur_sum += 1

                # Otherwise, perserve the max of current sum and the max in the diagonal
                # And reset the current sum back down to zero
                else:
                    cur_max = max(cur_max,cur_sum)
                    cur_sum = 0

                # Move our current indexing location down and right
                x += 1
                y += 1

            # If the starting x location has reached the end of the board, shift
            # it over, otherwise shift our y position over
            if diag_x_s > 0:
                diag_x_s -= 1
            else:
                diag_y_s += 1

            # Reassign our initial indexing location to the appropriate start locations
            # for the diagonal
            x,y = (diag_x_s,diag_y_s)

            # Perserve the max of the end of the diagonal and the max thus far for 
            # all diagonals
            diag_max_sum_dr = max(diag_max_sum_dr, cur_max, cur_sum)

        # Finally, return the max of all the searches conducted averaged over the 
        # length of the streak required to win
        return (float(max(diag_max_sum_dr, diag_max_sum_ul, max_col_sum, 
            max_row_sum))/state.K)
