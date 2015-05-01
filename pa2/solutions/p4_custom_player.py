# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action
from collections import defaultdict

class Seabiscout(Player):
    @property
    def name(self):
        return 'Seabiscout'

    global _move
    global bestStates
    global newBestStates
    global solvedGame
    solvedGame = False
    #move = None

    def move(self, state):
        global _move
        _move = None
        tTable = defaultdict(lambda: None)         #Transposition table

        my_move = state.actions()[0]

        def evaluate(self, state, color):
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

            return (max(diag_max_sum_dr, diag_max_sum_ul, max_col_sum, max_row_sum))/state.K


        def iterativeMinimax_play(state, alpha, beta, limit,depth):
            global _move
            current_best = None

            if state.is_terminal() or depth >= limit:
                if(state.is_terminal()):
                    solvedGame = True
                if(state.to_play == self):
                    return evaluate(self, state, state.to_play)

            if (tTable.get(state) == None):

                if state.is_terminal() or depth >= limit:
                    if(state.is_terminal()):
                        solvedGame = True
                    return evaluate(self,state, state.to_play)


                if state.to_play == self: # Maximize for us
                    current_best = -2
                    depth = depth + 1
                    for (score, poss, depth) in [(iterativeMinimax_play(state.result(possibility), alpha, beta, limit, depth),
                        possibility) for possibility in state.actions()]:

                        if(tTable[state] > score):
                                tTable[state] = score

                        if score >= beta:
                            return score

                        alpha = max(score, alpha)

                        if score > current_best:
                            current_best = score
                            _move = poss
                            bestStates.append(state)

                else:                     # Minimize for them
                    current_best = 2
                    depth = depth + 1
                    for (score, poss) in [(iterativeMinimax_play(state.result(possibility), alpha, beta, limit,depth),
                        possibility) for possibility in state.actions()]:

                        if(tTable[state] > score):
                                tTable[state] = score

                        if score <= alpha:
                            return score

                        beta = min(score, beta)

                        if score < current_best:
                            current_best = score
                            _move = poss
                            bestStates.append(state)


                return current_best

            else:
                return tTable[state]

        def bestIterativeMinimax_play(state, alpha, beta, limit,depth):
            global move
            current_best = None

            if (tTable.get(state) == None):

                if state.is_terminal() or depth >= limit:
                    if(state.is_terminal()):
                        solvedGame = True
                    return evaluate(self,state, state.to_play)


                if state.to_play == self: # Maximize for us
                    current_best = -2
                    depth = depth + 1
                    for (score, poss) in [(bestIterativeMinimax_play(the_best_state.result(possibility), alpha, beta, limit, depth),
                        possibility) for (possibility, the_best_state) in (the_best_state.actions(), bestStates)]:

                        if(tTable[state] < score):
                                tTable[state] = score

                        if score >= beta:
                            return score

                        alpha = max(score, alpha)

                        if score > current_best:
                            current_best = score
                            _move = poss
                            newBestStates.append(state)

                else:                     # Minimize for them
                    current_best = 2
                    depth = depth + 1
                    for (score, poss) in [(bestIterativeMinimax_play(the_best_state.result(possibility), alpha, beta, limit, depth),
                        possibility) for (possibility, the_best_state) in (the_best_state.actions(), bestStates)]:

                        if(tTable[state] > score):
                                tTable[state] = score

                        if score <= alpha:
                            return score

                        beta = min(score, beta)

                        if score < current_best:
                            current_best = score
                            _move = poss
                            newBestStates.append(state)


                return current_best

            else:
                return tTable[state]

        limit = 1
        bestStates = []
        newBestStates = []
        while (not self.is_time_up() and self.feel_like_thinking()) or not solvedGame:
            if not bestStates:
                iterativeMinimax_play(state,float("-inf"), float("inf"), limit, 0)
            else:
                bestIterativeMinimax_play(state,float("-inf"), float("inf"), limit, limit)
            my_move = _move
            move = None
            limit += 1
            bestStates = newBestStates
            newBestStates = []

        return my_move


    def feel_like_thinking(self):
        # You can code here how long you want to think perhaps.
        return False

    def do_the_magic(self, state):
        # Do the magic, return the first available move!
        return state.actions()[0]
