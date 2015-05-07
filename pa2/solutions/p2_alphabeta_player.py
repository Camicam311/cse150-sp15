# -*- coding: utf-8 -*-
#CSE 150 Assignment #2, Problem 1
#Description: Player class that uses the Minimax adversarial search algorithm to determine the best
# possible to move to play in an mxn tic-tac-toe board.
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu,chriskweller@gmail.com'

from assignment2 import Player, State, Action
from collections import defaultdict

# Player class that uses the AlphaBetaPruning adversarial search algorithm 
# and transposition tables to determine the best possible to move to play 
# in an mxn tic-tac-toe board.
#
# Input: a "Player" object that represents which player the agent will be 
# (either 1 or 2)
# 
# Output: the output of the "move" function.
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
    
        # Function that handles the intial call to min_value, which in turn
        # recurses on max_value and min_value untill it finds the appropriate
        # node at the bottom of the tree, at which point it returns the 
        # corresponding move.

        def alpha_beta_search(state):
            # -infinity ensures the var for the largest score will be updated
            v = float("-inf")

            # Iterate over every possible action from the current board state
            for a in state.actions():

                # Keep updating "v" and move with the best possible scores and 
                # and moves accordingly
                res = min_value(state.result(a), float("-inf"), float("inf"))
                if res > v:
                    v = res
                    move = a

            # Finally, return the best move found
            return move

        # Function that handles maximizing the score of the possible results
        # of the next state. Calls min_value.

        def max_value(state, alpha, beta):

            # If we've already seen this state before, return it's score
            if tTable[state]:
                return tTable[state]

            # Base case. If the state is terminal, return the utility.
            if state.is_terminal():
                return state.utility(self)
            v = float("-inf")

            # For every action from our current board...
            for a in state.actions():

                # Store the utility of the best move we've seen so far.
                v = max(v, min_value(state.result(a), alpha, beta))
                tTable[state] = max(tTable[state], v)

                # Prune if possible, otherwise continue iterating
                if v >= beta:
                    return v

                # and update alpha accordingly
                alpha = max(alpha, v)

            # Finally, return the best utility of all seen actions
            return v
        
        # Function that handles minimzing the score of the possible results
        # of the next state. Calls max_value.

        def min_value(state, alpha, beta):

            # If we've already seen this state before, return it's score
            if tTable[state]:
                return tTable[state]

            # Base case. If the state is terminal, return the utility.
            if state.is_terminal():
                return state.utility(self)
            v = float("inf")

            # For every action from our current board...
            for a in state.actions():

                # Store the utility of the best move we've seen so far.
                v = min(v, max_value(state.result(a), alpha, beta))
                tTable[state] = max(tTable[state], v)

                # Prune if possible, otherwise continue iterating
                if v <= alpha:
                    return v
                
                # and update beta accordingly
                beta = min(beta, v)

            # Finally, return the best utility of all seen actions
            return v

        # Begin the recursive madness and pass on the state it finds to the board
        return alpha_beta_search(state)
