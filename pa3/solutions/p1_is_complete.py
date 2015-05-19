# -*- coding: utf-8 -*-
#CSE 150 programming assignment 3, problem 1
#Description: Implementation of the is_complete method, which checks whetherr a csp has been
# solved or not. This method is used in the final implementation of the game solver.
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu, chriskweller@gmail.com'

from assignment3 import *

#Method that checks whether a constraint satisfaction problem has been "solved"
#Input: A constraint satisfaction problem [Variables, values, constraints]
#Output: Returns True when the CSP assignment is complete, i.e. all of the variables in the CSP have values assigned,
def is_complete(csp):

    for variable in csp.variables:
        if variable.is_assigned() == False:   #variable's domain isn't reduced to a single value, and
            return False                      #doens't have a specific value assigned to it

    return True