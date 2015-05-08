# -*- coding: utf-8 -*-
#CSE 150 Assignment #2, Problem 4
#Description: Custom Player class that we created ourselves, uses the AlphaBeta adversarial search algorithm as a base
# to determine the best possible to move to play in an mxn tic-tac-toe board.
# Additional optimizations include: Transition table,very modified evaluation function from p3, immediately returns a
# move that will win us the game, and a special play strategy for large boards.
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action
from collections import defaultdict
from pprint import pprint
from math import floor

#Function that holds and calls the main adversarial search algorithm.
#Input: A board that may or may not have moves already performed on it, and integer limit for the
# deepest depth to search for.
#Output: A "move" object for the best move given the limit.
def make_move(self, state, limit):
    import sys
    global tTable
    tTable = defaultdict(lambda: None)         #Transposition table

    #Customized alpha-beta algorithm that searches for the best possible move to make.
    #Input: A board that may or may not have moves already performed on it.
    #Output: A "move" object for the best move given the limit.
    def alpha_beta_search(state):
        #tTable = defaultdict(lambda: None)         #Transposition table
        v = float("-inf")
        for a in state.actions():
            res = min_value(state.result(a), float("-inf"), float("inf"), 0)
            if res > v:                            #If we found a move with better utility
                v = res
                move = (v,a)
        return move

    #"Max" player algorithm that searches for the best available move to "maximize" our utility.
    #Input: A board that may or may not have moves already performed on it, integers alpha and beta, and the current
    # integer depth of the current search.
    #Output: the utility for the best move performed
    def max_value(state, alpha, beta, depth):
        if tTable[state]:
            return tTable[state]                    #We already visited this state

        depth += 1
        move = None

        if state.is_terminal() or depth >= limit:
            other = 2 if state.to_play.color == 1 else 1            #Determine our color and return correct utility
            them = evaluate(self, state, other)
            return them * -1 if state.to_play == self else them

        v = float("-inf")
        for a in state.actions():
            v = max(v, min_value(state.result(a), alpha, beta, depth))
            tTable[state] = max(tTable[state], v)   #update transposition table values

            if v >= beta:                           #We can prune this branch
                return v
            alpha = max(alpha, v)
        return v

    #"Min" player algorithm that searches for the best available move to "minimize" our utility.
    #Input: A board that may or may not have moves already performed on it, integers alpha and beta, and the current
    # integer depth of the current search.
    #Output: the utility for the best move performed
    def min_value(state, alpha, beta, depth):
        if tTable[state]:
            return tTable[state]                    #We already visited this state

        depth += 1

        if state.is_terminal() or depth >= limit:
            other = 2 if state.to_play.color == 1 else 1            #Determine our color and return correct utility
            them = evaluate(self, state, other)
            return them * -1 if state.to_play == self else them

        v = float("inf")
        for a in state.actions():
            v = min(v, max_value(state.result(a), alpha, beta, depth))
            tTable[state] = max(tTable[state], v)   #update transposition table values

            if v <= alpha:                          #We can prune this branch
                return v
            beta = min(beta, v)
        return v

    return alpha_beta_search(state)                 #initial call to the alpha-beta function

# Evaluation class utilizes the supplied move function along with our
# evaluation heuristic to make the best possible move we have available
def evaluate(self, state, color):

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

#Custom Player class that we created ourselves, uses the AlphaBeta adversarial search algorithm as a base
# to determine the best possible to move to play in an mxn tic-tac-toe board.
#Input: a "Player" object that represents which player the agent will be (1 or 2)
#Output: the output of the "move" function
class Limit4(Player):
    global _move
    _move = None

    #Returns name of the agent.
    #Output: string for the name of the agent
    @property
    def name(self):
        return 'Limit4'

    #Function that determines the best possible move to play given the current state of the tic-tac-toe board
    #Input: An mxn tic-tac-toe "board" which may or may not have moves already performed on it.
    #Output: A "move" object, that states which player is placing his stone in an x,y coordinate of the board.
    def move(self, state):
        my_move = state.actions()[0]

        #Function that performs the next available move at the opposite corner of the board,
        #and blocks the default moves on the upper-right corner every couple of plys to ensure
        #that we win due to the fact that the opposing player can't search the board fast enough
        #Input a "board" mxn state that may or may not have moves performed on it
        #Output: The closest available move to the lower right corner of the board
        def specialStrategy(state):
            if((state.ply)%3 == 0 and (state.ply) != 0):    #Perform a "block" move every couple of ply
                return state.actions()[0]
            for move in reversed(state.actions()):          #Perform the next available "opposite end" move
                return move

        if(state.M >= 7 and state.N >= 7):                  #if board is big enough for us to abuse time limit
            return specialStrategy(state)

        #Check if the board is empty, if true, do a move near the center. Saves time.
        if(len(state.actions()) == state.M * state.N):
            return state.actions()[(len(state.actions()))/2]

        limit = 1                                           #current maximum depth that we will search
        while not (self.is_time_up() and self.feel_like_thinking() or limit >= 5):
            my_move = self.do_the_magic(state,limit)
            if(my_move[0] >= 0.7):    #The best move was win
                return my_move[1]
            limit += 1

        return my_move[1]

    #Ignore this, we don't really use it.
    def feel_like_thinking(self):
        return True

    #Calls the move function
    def do_the_magic(self, state, limit):
        return make_move(self,state,limit)