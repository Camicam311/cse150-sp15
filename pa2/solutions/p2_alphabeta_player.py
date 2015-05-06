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
        minimax_play(state,float("-inf"), float("inf"))
        return move
