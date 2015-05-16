# -*- coding: utf-8 -*-
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu, chriskweller@gmail.com'

from assignment3 import *

def is_complete(csp):
    """Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned."""

    # Hint: The list of all variables for the CSP can be obtained by csp.variables.
    # Also, if the variable is assigned, variable.is assigned() will be True.
    # (Note that this can happen either by explicit assignment using variable.assign(value),
    # or when the domain of the variable has been reduced to a single value.)
    for variable in csp.variables:
        if variable.is_assigned() == False:
            return False

    return True