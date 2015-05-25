# -*- coding: utf-8 -*-
#CSE 150 programming assignment 3, problem 5
#Description: Re-implementation of the select_unassigned_variable and order_domain_values methods,
# such that they order by Most Restricted Value and Least-Constraining value, respectively.
# This methods are used in the final implementation of the game solver.
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu, chriskweller@gmail.com'

from Queue import PriorityQueue
from collections import defaultdict

#Helper method for select_unassigned_variable, checks if a var-val combination violates
# neighboring constraints.And returns by how much we should reduce our variable's domain by.
#Input: A csp, a variable from said csp, a value from said variable
#Output: 0 if the value doesn't violate any constraints, -1 otherwise.
def get_available_domain(csp, variable, value):
    global numCons

    reduceDomainBy = 0

    for cons in csp.constraints[variable]: #Iterate over neighbors of var
        if cons.var2.domain == 1:
            if cons.is_satisfied(value, cons.var2.value) == False:
                reduceDomainBy = -1                                 #We can't use this value
        else:
            numCons += 1                                            #Xj in (Xi,Xj) is un-assigned, increase counter
            counter = 0
            for value2 in cons.var2.domain:
                if cons.is_satisfied(value, value2) == False:
                    counter += 1
            if counter == cons.var2.domain:                         #This value violates every constraint in neighbor
                reduceDomainBy = -1                                 #We can't use this value

    return reduceDomainBy

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
    q = PriorityQueue()
    for var in csp.variables:
        if not var.is_assigned:
            badValues = 0
            for val in var.domain:
                badValues += get_available_domain(csp,var,val)  #BadValues stores number of values that violate cons
        q.put((len(var.domain) - badValues + 1, numCons, var))  #Add (available values, num of cons, var) to queue
        numCons = 0

    if(q):                                                      #While queue not empty
        var = q.get()[2]
        return var
    else:                                                       #There were no unassigned variables in csp
        return None
    '''

#Method that returns a list of (ordered) domain values for a given variable by the least-constraining-value heurisitc,
# that is, the values are ordered in the incresing order of the number of choices for the neighboring variables in
# the constraint graph
#Input:A csp, a variable of said csp.
#Output: an ordered list of variable's values, ordered according to LCV
def order_domain_values(csp, variable):

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
