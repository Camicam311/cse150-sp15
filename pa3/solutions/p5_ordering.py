# -*- coding: utf-8 -*-
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu, chriskweller@gmail.com'

from Queue import PriorityQueue
from collections import defaultdict

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
        var = q.get()[2]
        return var
    else:
        return None

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
