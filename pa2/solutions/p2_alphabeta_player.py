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
        tTable = defaultdict(lambda: None)         #Transposition table

        def alpha_beta_search(state):
            v = float("-inf")
            for a in state.actions():
                res = min_value(state.result(a), float("-inf"), float("inf"))
                if res > v:
                    v = res
                    move = a
            return move

        def max_value(state, alpha, beta):
            if tTable[state]:
                return tTable[state]

            if state.is_terminal():
                return state.utility(self)
            v = float("-inf")
            for a in state.actions():
                v = max(v, min_value(state.result(a), alpha, beta))
                tTable[state] = max(tTable[state], v)

                if v >= beta:
                    return v
                alpha = max(alpha, v)
            return v
        
        def min_value(state, alpha, beta):
            if tTable[state]:
                return tTable[state]

            if state.is_terminal():
                return state.utility(self)
            v = float("inf")
            for a in state.actions():
                v = min(v, max_value(state.result(a), alpha, beta))
                tTable[state] = max(tTable[state], v)

                if v <= alpha:
                    return v
                beta = min(beta, v)
            return v

        return alpha_beta_search(state)
