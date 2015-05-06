# -*- coding: utf-8 -*-
#CSE 150 Assignment #2, Problem 1
#Description: Player class that uses the Minimax adversarial search algorithm to determine the best
# possible to move to play in an mxn tic-tac-toe board.
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu,chriskweller@gmail.com'

from assignment2 import Player, State, Action

#Player class that uses the Minimax adversarial search algorithm to determine the best
# possible to move to play in an mxn tic-tac-toe board.
# Input: a "Player" object that represents which player the agent will be (1 or 2)
# Output: the output of the "move" function.
class MinimaxPlayer(Player):

    #Function that determines the best possible move to play given the current state of the tic-tac-toe board
    #Input: An mxn tic-tac-toe "board" which may or may not have moves already performed on it.
    #Output: A "move" object, that states which player is placing his stone in an x,y coordinate of the board.
    def move(self, state):
        global move
        move = None

        # Recurssive function that performs the Minimax algorithm of the board, determines which move will
        # eventually produce the best utility, assuming that both player play optimally.
        #Input: An mxn tic-tac-toe "board" which may or may not have moves already performed on it by either
        # our player or by the adversary.
        #Output: The best available "move" object, that is, the move that will eventually produce the best utility for us.
        def minimax_play(state):
            global move
            current_best = None

            if state.is_terminal():                 #If either player has won in the current board
                return state.utility(self)          #return the utility (score) of the board

            if state.to_play == self:               # Maximize for us
                current_best = -2
                for (score, poss) in [(minimax_play(state.result(possibility)), #double for loop that iterates over the
                    possibility) for possibility in state.actions()]:           #possible moves available,recurssion occurs here

                    if score > current_best:        #We found a better move
                        current_best = score
                        move = poss

            else:                                   # Minimize for them
                current_best = 2
                for (score, poss) in [(minimax_play(state.result(possibility)), #double for loop that iterates over the
                    possibility) for possibility in state.actions()]:           #possible moves available,recurssion occurs here
 
                    if score < current_best:        #We found a better move
                        current_best = score
                        move = poss

            return current_best                     #Return the best move we found
        
        minimax_play(state)
        return move                                 #Return the best move we found
              



