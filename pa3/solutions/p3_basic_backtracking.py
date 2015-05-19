# -*- coding: utf-8 -*-
#CSE 150 programming assignment 3, problem 3
#Description: Implementation of the backtracking search algorithm, which recursively looks for a correct configuration
# of variable-value pairings that solves the csp, and backtracks to earlier states when a variable is not assignable.
# This algorithm is used in the final implementation of the game solver.
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu, chriskweller@gmail.com'

from collections import defaultdict
from p1_is_complete import is_complete
from p2_is_consistent import is_consistent

#Method that selectsthe next unassigned variable, or None if there is no more unassigned variables
#    (i.e. the assignment is complete)
def select_unassigned_variable(csp):
    return next((variable for variable in csp.variables if not variable.is_assigned()))

#Method that returns a list of (ordered) domain values for the given variable.
def order_domain_values(csp, variable):
    return [value for value in variable.domain]

#Method that performs an inference procedure for the variable assignment. For this implementation of
# the backtracking search algorithm, we always assume that this returns True.
def inference(csp, variable):
    return True

#Entry method for the CSP fsolve. This method calls the backtrack method to solve the given csp.
#Input: A csp to solve.
#Output: If the csp has a solution, returns a dictionary of variable -> value of the solution. Otherwise, None.
def backtracking_search(csp):

    if backtrack(csp):              #if csp has a solution
        return csp.assignment
    else:
        return None

#Method that performs the Backtracking search algorithm on a given csp.
#Input: a csp to solve.
#Output: True if a solution to the csp is found, None otherwise.
def backtrack(csp):

    if is_complete(csp):                            #if all variables in csp are assigned
        return True
    var = select_unassigned_variable(csp)           #Get an unassigned variable from the csp
    for value in order_domain_values(csp, var):     #Iterate over values of the unassigned variable

        csp.variables.begin_transaction()           #Save your game (in case of incorrect value is chosen)

        if is_consistent(csp, var, value):          #Value doesn't violate any constraint with any neighbor

            csp.variables.begin_transaction()       #Save your game again again (needed)

            csp.assignment[var] = value             #update our dictionary
            var.is_assigned() == True
            var.domain = []
            var.domain.append(value)                #Have the value be the only element in var's domain

            inferences = inference(csp, var)
            if inferences != False:
                csp.assignment[var] = value         #inferences isn't implemented, so this is just a dummy assignment
                result = backtrack(csp)

                if result == True:                  #We found a completed csp
                    return True

        csp.variables.rollback()                    #Load the game (revert changes to csp variables and domains)

    csp.variables.rollback()                        #csp has no solution, revert changes we have made to csp
    return None



