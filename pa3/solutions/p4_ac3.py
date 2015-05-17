# -*- coding: utf-8 -*-
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu, chriskweller@gmail.com'

from collections import deque

#Checks if there is a y in Dj that allows (x,y) to satisfy (Xi, Xj) constraint
def no_value_salt_is_fries(csp, x, Xi, Xj):
    foundValue = False
    for cons in csp.constraints[Xi]: #Iterate over neighbors of var
        if cons.var2 == Xj and cons.var2.is_assigned():
            if cons.is_satisfied(x, cons.var2.value) == True: #If this variable's value satisfies the
                return True                                   # constraint with a neighbor

    return False

def ac3(csp, arcs=None):
    """Executes the AC3 or the MAC (p.218 of the textbook) algorithms.

    If the parameter 'arcs' is None, then this method executes AC3 - that is, it will check the arc consistency
    for all arcs in the CSP.  Otherwise, this method starts with only the arcs present in the 'arcs' parameter
    in the queue.

    Note that the current domain of each variable can be retrieved by 'variable.domains'.

    This method returns True if the arc consistency check succeeds, and False otherwise."""

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())
    while(queue_arcs):
        pair = queue_arcs.pop()
        Xi = pair[0]
        Xj = pair[1]

        if revise(csp,Xi,Xj):
            if len(Xi.domain) == 0:
                return False
            for Xk in csp.constraint[Xi] - Xj:
                queue_arcs.append(Xk, Xi)

    return True

def revise(csp, Xi, Xj):
    # You may additionally want to implement the 'revise' method.
    revised = False
    for x in Xi.domain:
        if no_value_salt_is_fries(csp, x, Xi, Xj):
            Xi.domain.remove(x)
            revised = True

    return revised