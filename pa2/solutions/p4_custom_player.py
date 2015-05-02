# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action
from collections import defaultdict
from pprint import pprint

def make_move(self, state):
    return AlphaBeta(self, state)

def AlphaBeta(self, state):
    """Calculates the best move from the given board using the minimax 
       algorithm.

    Args:
        state (State): The current state of the board.

    Returns:
        the next move (Action)
    """

    # internal function because otherwise python throws a hissy fit
    # (geddit, hissy, python, that's a pun)

    '''
    Args:
        state (State): The current state of the board.
    '''
    global move
    move = None
    prevScore = 0

    tTable = defaultdict(lambda: None)         #Transposition table

    def minimax_play(state, alpha, beta):
        global move
        global lastScore
        current_best = None

        #if state.is_terminal():
        #    return state.utility(self)

        if (tTable.get(state) == None):
            #tTable[state] = True

            if state.is_terminal():
                #return state.utility(self)
                #for x in state.board:
                #    print x
                #print state.last_action
                #print state.to_play
                
                other  = 2 if state.to_play.color == 1 else 1
                # if other > to_play ret positive
                # else ret neg
                them = evaluate(self, state, other)
                you = evaluate(self, state, state.to_play.color)
                #print "Them: ", them, " you: ",you
                #print "To play: ",state.to_play

                #if them > you:
                #    res =  them * -1
                #else:
                #    res = them
                #print "h(n): ", you * -1 if state.to_play == self else you, "util: ", state.utility(self)
                #print "#########"
                return them * -1 if state.to_play == self else them

            if state.to_play == self: # Maximize for us
                current_best = -2

                for (score,poss) in [(minimax_play(state.result(possibility),
                    alpha, beta), possibility) for possibility 
                    in state.actions()]:

                    #lastScore = score
                    if(tTable[state] < score):
                        tTable[state] = score

                    if score >= beta:
                        return score

                    alpha = max(score, alpha)

                    if score > current_best:
                        current_best = score
                        move = poss

            else:                     # Minimize for them
                current_best = 2
                
                for (score,poss) in [(minimax_play(state.result(possibility),
                    alpha, beta), possibility) for possibility 
                    in state.actions()]:

                    if(tTable[state] > score):
                        tTable[state] = score

                    if score <= alpha:
                        return score

                    beta = min(score, beta)

                    if score < current_best:
                        current_best = score
                        move = poss

            return current_best


        else:
            return tTable[state]

    #tTable[state] = True
    minimax_play(state,-2,2)
    return move

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

    return (float(max(diag_max_sum_dr, diag_max_sum_ul, max_col_sum, 
        max_row_sum))/state.K)

class Seabiscuit(Player):
    global _move
    _move = None

    @property
    def name(self):
        """Returns the name of this agent. Try to make it unique!"""
        return 'Seabiscuit'

    def move(self, state):
        """Calculates the absolute best move from the given board position using magic.
        
        Args:
            state (State): The current state of the board.

        Returns:
            your next Action instance
        """
        my_move = state.actions()[0]

        while not (self.is_time_up() and self.feel_like_thinking()):
            # Do some thinking here
            my_move = self.do_the_magic(state)

        # Time's up, return your move
        # You should only do a small amount of work here, less than one second.
        # Otherwise a random move will be played!
        return my_move

    def feel_like_thinking(self):
        # You can code here how long you want to think perhaps.
        return True

    def do_the_magic(self, state):
        return make_move(self,state)

