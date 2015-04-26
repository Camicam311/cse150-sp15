# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action
from collections import defaultdict

class AlphaBetaPlayer(Player):
    def move(self,state):
        global move
        global bestMove
        bestMove = 0
        move = None

        tTable = defaultdict(lambda: False)         #Transposition table

        def max_value(state, alpha, beta):
            global move
            global bestMove

            if state.is_terminal():
                return state.utility(self)

            current_best = float("-inf")
            for (next_state, poss) in [(state.result(possibility),
                possibility) for possibility in state.actions()]:
                
                if tTable[next_state]:
                    continue
                else: tTable[next_state] = True

                current_best = max(min_value(next_state, alpha, beta),
                        current_best)

                if current_best >= beta:
                    return current_best

                alpha = max(alpha, current_best)

                if(current_best > bestMove):
                    move = poss
                    bestMove = current_best

            return current_best

        def min_value(state, alpha, beta):
            global move
            global bestMove

            if state.is_terminal():
                return state.utility(self)

            current_best = float("inf")
            for (next_state, poss) in [(state.result(possibility),
                possibility) for possibility in state.actions()]:

                if tTable[next_state]:
                    continue
                else:
                    tTable[next_state] = True

                current_best = min(max_value(next_state, alpha, beta), 
                        current_best)

                if current_best <= alpha:
                    return current_best

                beta = min(beta, current_best)

                if(current_best < bestMove):
                    move = poss
                    bestMove = current_best

            return current_best


        current_best = max_value(state, float("-inf"), float("inf"))
        print("The move is ", move, "And utility: ", current_best)
        move.color = 1
        return move
