# -*- coding: utf-8 -*-
#CSE 150 programming assignment 3, problem 6
#Description: Series of methods that have been previously implemented in p1-p5 put together in a single file, when
# combined, they are capable of solving constraint satisfaction problems effectively. In this case, a Futoshoki game.
__author__ = 'Please write your names, separated by commas.'
__email__ = 'Please write your email addresses, separated by commas.'

from collections import deque
from Queue import PriorityQueue
from collections import defaultdict

def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P6, *you do not need to modify this method.*
    """
    return ac3(csp, csp.constraints[variable].arcs())

#Method that implements the minimum-remaining-values (MRV) and degree heuristic. That is,
# the variable with the smallest number of values left in its available domain.
#Input:A csp
#Output: An iterator that returns the next unassigned variable, ordered by the MRV.
def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    This method implements the minimum-remaining-values (MRV) and degree heuristic. That is,
    the variable with the smallest number of values left in its available domain.  If MRV ties,
    then it picks the variable that is involved in the largest number of constraints on other
    unassigned variables.
    """
    global numCons
    numCons = 0

    unassigned_vars = filter(lambda x: not x.is_assigned(),csp.variables)
    mrv_vars = filter(lambda x:len(x.domain) == len(min(unassigned_vars,key=lambda x:len(x.domain)).domain),unassigned_vars)

    '''
    gt = -1
    res = None
    for var in mrv_vars:
        x = len(csp.constraints[var])
        for o_var in unassigned_vars:
            if o_var == var: continue
            o_x = len(csp.constraints[var,o_var])
            if x + o_x > gt:
                gt = x+o_x
                res = var
                #print var.domain
    return res 
    '''
    return mrv_vars[0]

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

#Method that checks whether a constraint satisfaction problem has been "solved"
#Input: A constraint satisfaction problem [Variables, values, constraints]
#Output: Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned,
def is_complete(csp): 

    for variable in csp.variables:
        if variable.is_assigned() == False or len(variable.domain) != 1:   #variable doens't have a
            return False                                                   #specific value assigned to it

    return True

#Method that returns a list of (ordered) domain values for a given variable by the least-constraining-value heurisitc,
# that is, the values are ordered in the incresing order of the number of choices for the neighboring variables in
# the constraint graph
#Input:A csp, a variable of said csp.
#Output: an ordered list of variable's values, ordered according to LCV
def order_domain_values(csp, variable): # Good

    var = variable
    q = PriorityQueue()

    for value in var.domain:
        counter = 0
        for cons in csp.constraints[var]:                               #Iterate over neighbors of var
            if cons.var2.is_assigned():
                if cons.is_satisfied(value, cons.var2.value) == True:   #We found another satisfied constraint
                    counter += 1
            else:
                for val2 in cons.var2.domain:
                    if cons.is_satisfied(value, val2) == True:          #We found another satisfied constraint
                        counter += 1
        q.put((counter, value))                                         #Add (# of satisfied cons, value) to queue

    orderedDomain = []
    while(q.empty() == False):
        counter, value = q.get()
        orderedDomain.insert(0,value)                                      #add elements of queue to a list
                                                                         # with correct ordering
    return orderedDomain

def backtracking_search(csp):
    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P6, *you do not need to modify this method.*
    """
    if backtrack(csp):
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

#Helper method of ac3 that removes all elements from Xi's domain that don't satisfy (Xi,Xj) constraints
#Input: A csp, a variable Xi in the csp, another variable Xj in the csp
def revise(csp, Xi, Xj):
    revised = False
    for x in Xi.domain:
        if len([csp.constraints[x,y] for y in Xj.domain]) == 0:
            Xi.domain.remove(x)
            revised = True

    return revised

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
