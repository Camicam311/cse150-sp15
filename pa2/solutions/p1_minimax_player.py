# -*- coding: utf-8 -*-
__author__ = 'Sivasubramanian Chandrasegarampillai, Walter Curnow'
__email__ = 'rchandra@uci.edu,wcurnow@uci.edu'

from assignment2 import Player, State, Action
class MinimaxPlayer(Player):
    def move(self, state):
        """Calculates the best move from the given board using the minimax algorithm.

        Args:
            state (State): The current state of the board.

        Returns:
            the next move (Action)
        """

        # internal function because otherwise python throws a hissy fit
        # (geddit, hissy fit, that's a pun)

        # I think this shit is busted. It returns moves, but I managed to
        # beat it, which isn't a good sign. We need to investigate further.
        # @itsweller is the one that fuckered this all up

        # TODO: Check how min sorts and orders. We could be selecting the 
        # "wrong" move even though it may be correct for breaking ties
        # if min doesn't perserve ordering. This can be fixed with a for
        # loop, but that's not as sexy as 1 line list comprehensions and 
        # lambdas
        '''
        Args:
            state (State): The current state of the board.
            min_or_max (String): Whether we're to perform min or max stage,
                                 accepted values are 'min' and 'max'
        '''
        def minimax_play(state, min_or_max):
            if state.is_terminal():
                return state.utility(self)
            if min_or_max == 'min':
                return min([(minimax_play(state.result(possibility),'max'), 
                    possibility) for possibility in state.actions()], 
                    key=lambda x:x[0])
            if min_or_max == 'max':
                return max([(minimax_play(state.result(possibility),'min'), 
                    possibility) for possibility in state.actions()], 
                    key=lambda x:x[0])

        return max([(minimax_play(state.result(possibility),'min'), 
            possibility) for possibility in state.actions()],
            key=lambda x:x[0])[1]


