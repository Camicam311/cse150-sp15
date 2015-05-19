# -*- coding: utf-8 -*--
#CSE 150 programming assignment 3, problem 2
#Description: Implementation of the is_consistent method, which checks if a value pertaining to a specific variable
# violates any constraints regarding that variable. This method is used in the final implementation of the game solver.
__author__ = 'Rene Sanchez, Chris Weller'
__email__ = 'risanche@ucsd.edu, chriskweller@gmail.com'

#Checks if a value pertaining to a specific variable violates any constraits  regarding that variable.
#Input: A constraint satisfaction problem to check for violations, a variable in said csp, and a value of said variable
#Output: Returns True when the variable assignment to value is consistent, False otherwise
def is_consistent(csp, variable, value):

    for cons in csp.constraints[variable]:          #Iterate over neighbors of var
        if cons.var2.domain == 1:                   #var2 is a neighbor variable that we have a constraint with
            if cons.is_satisfied(value, cons.var2.value) == False: #If this variable's value breaks the
                return False                                       # constraint with a neighbor
        else:                                       #var2 isn't assigned yet, check all of its values
            counter = 0
            for value2 in cons.var2.domain:
                if cons.is_satisfied(value, value2) == False:
                    counter += 1
            if counter == len(cons.var2.domain):    #If value violated the constraint for entire domain of var2
                return False

    return True                                     #value satisfied constraint for at-least 1 value in all neighbors