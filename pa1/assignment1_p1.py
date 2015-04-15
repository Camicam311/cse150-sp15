#CSE 150 Programming assignment 1,problem 1
#Student Names: Rene Sanchez, Chris Weller, Divyansh H Vaishnav
#IDs: Rene Sanchez: A11866286, Chris Weller: , Divyansh H Vaishnav
#Description: Reads an nxm n-puzzle from a .csv file and determines
# whether or not the puzzle is solved.

__author__ = 'risanche@ucsd.edu', 'chriskweller@gmail.com','dvaishna@ucsd.edu'

#checks if the board is in a "solved" state
#Input: an mxn 2d array "board" that you want to find the empty space of.
#Output: True if board is solved
def is_complete(board):
    curr = 0
    for row in board:             #loop through rows
        for number in row:        #loop through columns
            print(number)
            if(number != curr):
                return False      #the puzzle isn't ordered correctly
            curr = curr + 1
    return True

#MAIN
def main():
    import sys
    #read the input parameters and save the board into a 2d matrix
    board = [[int(n.strip()) for n in line.split(',')] for line in sys.stdin.readlines()]

    print(is_complete(board))   #Checks if board is solved

if __name__ == "__main__":
    main()