#CSE 150 Programming assignment 1,problem 1
#Student Name: Rene Sanchez
#ID: A11866286
#Description: Reads an nxm n-puzzle from a .csv file and determines
# whether or not the puzzle is solved.

__author__ = 'risanche@ucsd.edu'

#checks if the board is in a "solved" state
#Output: True if board is solved
def is_complete(board):
    curr = 0
    for row in board:  #loop through rows
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

    print(is_complete(board))

if __name__ == "__main__":
    main()