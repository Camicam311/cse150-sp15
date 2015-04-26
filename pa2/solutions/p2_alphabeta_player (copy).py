# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action

class AlphaBetaPlayer(Player):
    def move(self,state):
        global move
        global previousPlayer

        move = None

        def alphaBeta(state, alpha, beta):
            global move
            global tTable
            global bestMove

            #move = None
            tTable = {}         #Transposition table


            if state.is_terminal():
                return state.utility(self)

            if state.to_play == self:       #Maximize for us
                for (next_state, poss) in [(state.result(possibility),possibility) for possibility in state.actions()]:
                    score = alphaBeta(next_state, alpha, beta)
                    if alpha < score:
                        alpha = score
                        move = poss

                    if alpha >= beta:
                        break

                return alpha
            else:                           #Minimize for them
                for (next_state, poss) in [(state.result(possibility),possibility) for possibility in state.actions()]:

                    score = alphaBeta(next_state, alpha, beta)
                    if beta > score:
                        beta = score
                        move = poss

                    if alpha >= beta:
                        break

                return beta


        current_best = alphaBeta(state, -9999999, 999999)
        print("The move is ", move)
        print(move)
        return move
