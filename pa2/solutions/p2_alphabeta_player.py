# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action
from collections import defaultdict
class AlphaBetaPlayer(Player):
    def move(self, state):
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
                    return state.utility(self)

                if state.to_play == self: # Maximize for us
                    current_best = -2

                    for (score,poss) in [(minimax_play(state.result(possibility),
                        alpha, beta), possibility) for possibility 
                        in state.actions()]:

                        #lastScore = score
                        if(tTable[state] < score):
                            tTable[state] = score

                        if score >= beta:
                            return tTable[state]

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
                            return tTable[state]

                        beta = min(score, beta)

                        if score < current_best:
                            current_best = score
                            move = poss

                return current_best


            else:
                return tTable[state]

        #tTable[state] = True
        '''
        def alpha_beta_search(state):
            v = float("-inf")
            for a in state.actions():
                res = max_value(state.result(a), float("-inf"), float("inf"))
                if res > v:
                    v = res
                    move = a
                    print "move",a
            return move

        def max_value(state, alpha, beta):

            if state.is_terminal():
                return state.utility(self)
            v = float("-inf")
            for a in state.actions():
                #temp_min = min_value(state.result(a), alpha, beta)
                #if temp_min > alpha:
                #    alpha = temp_min
                v = max(v, min_value(state.result(a), alpha, beta))
                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
        
        def min_value(state, alpha, beta):

            if state.is_terminal():
                return state.utility(self)
            v = float("inf")
            for a in state.actions():
                #temp_max = max_value(state.result(a), alpha, beta)
                #if temp_max < v:
                #    v = temp_max
                #    move = a
                v = min(v, max_value(state.result(a), alpha, beta))
                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        return alpha_beta_search(state)
