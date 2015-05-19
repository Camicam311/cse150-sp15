# -*- coding: utf-8 -*-
#CSE 150 programming assignment 3, problem 4
#Description: Implementation of the AC-3 (forward checking) algorithm, which updates the domains of variables as
# variables are assigned, and determines if a constraint has been violated ahead of time.
# This algorithm is used in the final implementation of the game solver.
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu, chriskweller@gmail.com'

from collections import deque
from collections import defaultdict

#Method that checks if there is no y in Dj that allows values (x,y) to satisfy a (Xi, Xj) variable constraint
#Input: a csp, a value x in the domain of variable Xi, variable Xi, variable Xj. where both variables are members
#   of the given csp.
#Output: True if the is no value that satisfies any constraint (Xi,Xj) for x, False otherwise
def no_value_satisfies(csp, x, Xi, Xj):

    for cons in csp.constraints[Xi]:                                #Iterate over neighbors of var
        if cons.var2 == Xj:                                         #If we are looking at (Xi,Xj) constraints
            if cons.var2.is_assigned():
                if cons.is_satisfied(x, cons.var2.value) == True:   #The value does satisfy
                    return False
            else:
                for y in cons.var2.domain:                          #Iterate over Xj values
                    if cons.is_satisfied(x,y) == True:              #A value does satisfy
                        return False

    return True

#Method that returns a list of neighbor variables for a variable Xi
#Input: A csp, a variable Xi that is a member of said csp.
#Output a list of variables that Xi shares a constraint with.
def getNeighbors(csp,Xi):
    neighbors = defaultdict(lambda: None)                   #Use a dictionary to store individual variables
                                                            # b/c there may be more than 1 constraint per var
    for cons in csp.constraints[Xi]:
        neighbors[cons.var2] = cons.var2                    #Record neighbor variable

    neighList = []
    for var in neighbors:
        neighList.append(var)                               #Add neighbor variables to a list

    return neighList

#Method that performs the AC-3 (forward checking) algorithm on a csp.
#Input: A csp, a boolean variable that decides whether the algorithm runs normal AC-3 on the csp,
# otherwise it starts with only the arcs present in the 'arc' param in the queue
#Output: True if the arc consistency check succeeds, False otherwise.
def ac3(csp, arcs=None):

    queue_arcs = deque(arcs if arcs is not None else csp.constraints.arcs())    #contains (var1,var2) pairings
    while(queue_arcs):
        pair = queue_arcs.pop()
        Xi = pair[0]
        Xj = pair[1]

        listXj = [Xj]                           #create a set containing just the Xj variable
        if revise(csp,Xi,Xj):                   #If we find values in Xi's domain that don't satisfy (Xi,Xj)
            if len(Xi.domain) == 0:
                return False                    #csp has no solution with current configuration
            for Xk in list(set(getNeighbors(csp,Xi)) - set(listXj)):        #iterate over neighbors of Xi that aren't Xj
                queue_arcs.append((Xk, Xi))     #Add variables with reduced domain to queue

    return True

#Helper method of ac3 that removes all elements from Xi's domain that don't satisfy (Xi,Xj) constraints
#Input: A csp, a variable Xi in the csp, another variable Xj in the csp
def revise(csp, Xi, Xj):

    revised = False
    for x in Xi.domain:
        if no_value_satisfies(csp, x, Xi, Xj):      #value x doesn't satisfy (Xi,Xj) constraints
            Xi.domain.remove(x)
            revised = True

    return revised