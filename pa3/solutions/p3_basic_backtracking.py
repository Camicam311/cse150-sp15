# -*- coding: utf-8 -*-
#CSE 150 programming assignment 3, problem 3
#Description: Implementation of the backtracking search algorithm, which recursively looks for a correct configuration
# of variable-value pairings that solves the csp, and backtracks to earlier states when a variable is not assignable.
# This algorithm is used in the final implementation of the game solver.
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu, chriskweller@gmail.com'

from collections import defaultdict

### Problem 1 and Problem 2 code ###

#Method that checks whether a constraint satisfaction problem has been "solved"
#Input: A constraint satisfaction problem [Variables, values, constraints]
#Output: Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned,
def is_complete(csp):

    for variable in csp.variables:
        if variable.is_assigned() == False or len(variable.domain) != 1:   #variable doens't have a
            return False                                                   #specific value assigned to it

    return True

#Checks if a value pertaining to a specific variable violates any constraits  regarding that variable.
#Input: A constraint satisfaction problem to check for violations, a variable in said csp, and a value of said variable
#Output: Returns True when the variable assignment to value is consistent, False otherwise
def is_consistent(csp, variable, value):

    for cons in csp.constraints[variable]:          #Iterate over neighbors of var
        if cons.var2.domain == 1 and cons.var2.is_assigned() == True:
            if cons.is_satisfied(value, cons.var2.value) == False: #If this variable's value breaks the
                return False                                       # constraint with a neighbor
        else:                                       #var2 isn't assigned yet, check all of its values
            counter = 0
            for value2 in cons.var2.domain:
                if cons.is_satisfied(value, value2) == False:
                    counter += 1

            if counter >= len(cons.var2.domain):         #if value violated the constraint for entire domain of var2
               return False

    return True                                     #value satisfied constraint for at-least 1 value in all neighbors

### End of Problem 1 and Problem 2 code ###

#Method that selects the next unassigned variable, or None if there is no more unassigned variables
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
    for value in order_domain_values(csp, var):     #Iterate over values of the unassigned variab

        csp.variables.begin_transaction()           #Save your game (in case of incorrect value is chosen)

        if is_consistent(csp, var, value):          #Value doesn't violate any constraint with any neighbor

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

    return None



