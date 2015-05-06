#singular extension implementation

#in the while:
    #after iterative minimax call
    singularExtension(state,float("-inf"), float("inf"), limit + 3, 0):

    #save the best state, with the best move

global bestMoveList = []

def singularExtension(state,float("-inf"), float("inf"), limit, 0, move):
    global move
            current_best = None

            if (tTable.get(state) == None):

                if state.is_terminal() or depth >= limit:
                    if(state.is_terminal()):
                        solvedGame = True
                    return evaluate(self,state, 2)


                if state.to_play == self: # Maximize for us
                    current_best = -2
                    depth = depth + 1
                    for (score, poss) in [(bestIterativeMinimax_play(the_best_state.result(possibility), alpha, beta, limit, depth),
                        possibility)]: #for (possibility, the_best_state) in (the_best_state.actions(), bestStates)]:

                        if(tTable[state] < score):
                                tTable[state] = score

                        if score >= beta:
                            return score

                        alpha = max(score, alpha)

                        if score > current_best:
                            current_best = score
                            _move = poss
                            bestMoveList.append(score, move)

                else:                     # Minimize for them
                    current_best = 2
                    depth = depth + 1
                    for (score, poss) in [(bestIterativeMinimax_play(the_best_state.result(possibility), alpha, beta, limit, depth),
                        possibility)]: # for (possibility, the_best_state) in (the_best_state.actions(), bestStates)]:

                        if(tTable[state] > score):
                                tTable[state] = score

                        if score <= alpha:
                            return score

                        beta = min(score, beta)

                        if score < current_best:
                            current_best = score
                            _move = poss
                            bestMoveList.append(score, move)


                return current_best

            else:
                return tTable[state]


