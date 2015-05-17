# -*- coding: utf-8 -*-
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu, chriskweller@gmail.com'

from collections import defaultdict

def select_unassigned_variable(csp):
    """Selects the next unassigned variable, or None if there is no more unassigned variables
    (i.e. the assignment is complete).

    For P3, *you do not need to modify this method.*
    """
    return next((variable for variable in csp.variables if not variable.is_assigned()))


def order_domain_values(csp, variable):
    """Returns a list of (ordered) domain values for the given variable.

    For P3, *you do not need to modify this method.*
    """
    return [value for value in variable.domain]


def inference(csp, variable):
    """Performs an inference procedure for the variable assignment.

    For P3, *you do not need to modify this method.*
    """
    return True

def is_consistent(csp, variable, val):
    for cons in csp.constraints[variable]: #Iterate over neighbors of var
        print "Size of domain ", cons.var2.domain
        if cons.var2.domain == 1:
            print "First if"
            if cons.is_satisfied(val, cons.var2.value) == False: #If this variable's value breaks the
                print "Bad ",val, " with ",cons.var2.value
                return False                                       # constraint with a neighbor
        else:
            counter = 0
            for value2 in cons.var2.domain:
                if cons.is_satisfied(val, value2) == False:
                    counter += 1
            if counter == len(cons.var2.domain):
                return False

    return True


def backtracking_search(csp):

    assignment = defaultdict(lambda: None)
    assignComplete = False

    """Entry method for the CSP solver.  This method calls the backtrack method to solve the given CSP.

    If there is a solution, this method returns the successful assignment (a dictionary of variable to value);
    otherwise, it returns None.

    For P3, *you do not need to modify this method.*
    """
    if backtrack(csp):
        return csp.assignment
    else:
        return None

def is_complete(csp):

    for variable in csp.variables:
        if variable.is_assigned() == False:
            return False
    return True

def backtrack(csp):
    """Performs the backtracking search for the given csp.

    If there is a solution, this method returns the successful assignment; otherwise, it returns None.
    """

    if is_complete(csp):
        print "Finished"
        return csp.assignment
    var = select_unassigned_variable(csp)
    for value in order_domain_values(csp, var):
        print "New value"
        print var
        print value
        if is_consistent(csp, var, value):
            print "Got here"
            csp.variables.begin_transaction()
            #csp.variable[var] = value
            csp.assignment[var] = value

            inferences = inference(csp, var)
            if inferences != False:
                csp.assignment[var] = value    #inferences isn't implemented, so this is just a dummy assignment
                result = backtrack(csp)

                if result != "Failure":
                    return csp.assignment

        csp.assignment[var] = None

    csp.variables.rollback()
    return "Failure"



