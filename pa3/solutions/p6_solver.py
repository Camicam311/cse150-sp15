# -*- coding: utf-8 -*-
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

def get_available_domain(csp, variable, value):
    global numCons

    for cons in csp.constraints[variable]: #Iterate over neighbors of var
        if cons.var2.domain == 1:
            if cons.is_satisfied(value, cons.var2.value) == False: #If this variable's value breaks the
                return -1                                      # constraint with a neighbor
        else:
            numCons +=1
            counter = 0
            for value2 in cons.var2.domain:
                if cons.is_satisfied(value, value2) == False:
                    counter += 1
            if counter == cons.var2.domain:
                return -1

    return 0

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

    q = PriorityQueue()
    for var in csp.variables:
        counter = 0
        if var.is_assigned == False:
            counter = 0
            for val in val.domain:
                counter += get_available_domain(csp,var,val)
        q.put((len(var.domain) + counter + 1, numCons, var))
        numCons = 0

    if(q):
        return q.get()[2]
    else:
        return None

def is_consistent(csp, variable, val):
    for cons in csp.constraints[variable]: #Iterate over neighbors of var
        #print "Size of domain ", len(cons.var2.domain)
        if cons.var2.domain == 1:
            if cons.is_satisfied(val, cons.var2.value) == False: #If this variable's value breaks the
                return False                                       # constraint with a neighbor
        else:
            counter = 0
            for value2 in cons.var2.domain:
                if cons.is_satisfied(val, value2) == False:
                    counter += 1
            if counter == len(cons.var2.domain):
                #print "Accept"
                return False

    #print "Reject"
    return True

def is_complete(csp):

    for variable in csp.variables:
        if variable.is_assigned() == False:
            return False
    return True

def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    This method implements the least-constraining-value (LCV) heuristic; that is, the values are
    ordered in the increasing order of the number choices for the neighboring variables in the constraint graph
    """
    var = variable
    q = PriorityQueue()

    for value in var.domain:
        counter = 0
        for cons in csp.constraints[var]: #Iterate over neighbors of var
            if cons.var2.is_assigned():
                if cons.is_satisfied(value, cons.var2.value) == True:
                    counter += 1
        q.put((counter, value))

    orderedDomain = []
    while(q.empty() == False):
        prio, item = q.get()
        orderedDomain.append(item)

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


def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns the successful assignment; otherwise, it returns None.
    """

    if is_complete(csp):
        #print "Finished"
        return csp.assignment
    var = select_unassigned_variable(csp)
    #print "New var"
    for value in order_domain_values(csp, var):
        #print "New value"
        #print var
        #print value
        csp.variables.begin_transaction()
        if is_consistent(csp, var, value):
            #print "Got here"
            csp.variables.begin_transaction()

            csp.assignment[var] = value
            var.is_assigned() == True
            var.domain = []
            var.domain.append(value)

            inferences = inference(csp, var)
            if inferences != False:
                csp.assignment[var] = value    #inferences isn't implemented, so this is just a dummy assignment
                result = backtrack(csp)

                if result != "Failure":
                    return csp.assignment

        csp.variables.rollback()
        csp.assignment[var] = None

    #print("Backtrack")
    csp.variables.rollback()
    return "Failure"

#Checks if there is a y in Dj that allows (x,y) to satisfy (Xi, Xj) constraint
def no_value_salt_is_fries(csp, x, Xi, Xj):
    foundValue = False
    for cons in csp.constraints[Xi]: #Iterate over neighbors of var
        if cons.var2 == Xj and cons.var2.is_assigned():
            if cons.is_satisfied(x, cons.var2.value) == True: #If this variable's value satisfies the
                return True                                   # constraint with a neighbor

    return False

def getNeighbors(csp,Xi):
    neighbors = defaultdict(lambda: None)
    for cons in csp.constraints[Xi]:
        neighbors[cons.var2] = cons.var2

    neighList = []
    for var in neighbors:
        neighList.append(var)

    return neighList

def revise(csp, Xi, Xj):
    # You may additionally want to implement the 'revise' method.
    revised = False
    for x in Xi.domain:
        if no_value_salt_is_fries(csp, x, Xi, Xj):
            Xi.domain.remove(x)
            revised = True

    return revised

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

        listXj = [Xj]
        if revise(csp,Xi,Xj):
            if len(Xi.domain) == 0:
                return False
            for Xk in list(set(getNeighbors(csp,Xi)) - set(listXj)):
                queue_arcs.append((Xk, Xi))

    return True