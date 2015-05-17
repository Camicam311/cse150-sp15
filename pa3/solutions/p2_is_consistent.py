# -*- coding: utf-8 -*-
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu, chriskweller@gmail.com'


def is_consistent(csp, variable, value):
    """Returns True when the variable assignment to value is consistent, i.e. it does not violate any of the constraints
    associated with the given variable for the variables that have values assigned.

    For example, if the current variable is X and its neighbors are Y and Z (there are constraints (X,Y) and (X,Z)
    in csp.constraints), and the current assignment as Y=y, we want to check if the value x we want to assign to X
    violates the constraint c(x,y).  This method does not check c(x,Z), because Z is not yet assigned."""

    #for cons in csp.constraints[variable]: #Iterate over neighbors of var
    #    if cons.var2.is_assigned():
    #        if cons.is_satisfied(value, cons.var2.value) == False: #If this variable's value breaks the
    #            return False                                       # constraint with a neighbor

    #return True

    for cons in csp.constraints[variable]: #Iterate over neighbors of var
        if cons.var2.domain == 1:
            if cons.is_satisfied(value, cons.var2.value) == False: #If this variable's value breaks the
                return False                                       # constraint with a neighbor
        else:
            counter = 0
            for value2 in cons.var2.domain:
                if cons.is_satisfied(value, value2) == False:
                    counter += 1
            if counter == len(cons.var2.domain):
                return False

    return True