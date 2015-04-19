#CSE 150 Programming assignment 1, problem 4
#Student Names: Rene Sanchez, Chris Weller, Divyansh H Vaishnav
#IDs: Rene Sanchez: A11866286, Chris Weller: , Divyansh H Vaishnav
#Description: Reads an nxm n-puzzle from a .csv file and solves the
# puzzle using a iterative deepening depth-first traversal algorithm

__author__ = 'risanche@ucsd.edu', 'chriskweller@gmail.com','dvaishna@ucsd.edu'
import Queue
from signal import signal, SIGPIPE, SIG_DFL
from math import factorial

#Finds the '0' or empty space of the board, and updates the global row and column variables
#Input: an mxn 2d array "board" that you want to find the empty space of.
#Ouput: True if a 0 was found, False otherwise.
def findEmptySpace(board):
    global row, column, configs

    horizontal = len(board)
    vertical = len(board[0])
    size = horizontal*vertical
    config = (factorial(size))/2         #total number of solvable configurations for board

    for x in range(horizontal):          #loop through rows
        for y in range(vertical):        #loop through columns
            if(board[x][y] == 0):
                row = x
                column = y
                return True
    return False

#checks if the board is in a "solved" state
#Input: An mxn 2d array "board" that you want to check if is "solved"
#Output: True if board is solved
def storeCopy(board):
    global OriginalBoard

    horizontal = len(board)
    vertical = len(board[0])

    for x in range(horizontal):          #loop through rows
        for y in range(vertical):        #loop through columns
               OriginalBoard[x][y] = board[x][y]

#checks if the board is in a "solved" state
#Input: An mxn 2d array "board" that you want to check if is "solved"
#Output: True if board is solved
def is_complete(board):
    curr = 0
    for row in board:               #loop through rows
        for number in row:          #loop through columns
            if(number != curr):
                return False        #the puzzle isn't ordered correctly
            curr = curr + 1
    return True

#Iterative Deepening Seach algorithm that
#Input: An mxn 2d array "board" that you want to find the solution to
#Output: "UNSOLVABLE" if IDS doens't find a solution
def IDS(board):
    for x in range(1,12): #hard limit is 12
        DLS(board, x)
    print("UNSOLVABLE")   #we didn't find a solution in 12 moves or less

#Depth Limited Seach algorithm that searches all possible sets of moves until it finds the combination that gives
#   the board a "solved" state
#Input: A non-solved mxn 2d array "board" that you want to find the solution to.
#Output: A string of moves for the solution if found, "UNSOLVABLE" otherwise
def DLS(board, maxLimit):
    import sys
    global stack, legal
    stack = []

    allMoves = ["U","D","L","R"]
    currMove = ""
    stack.insert(0,currMove)
    while(len(stack) != 0):                             #stack isn't empty
        stackMove = stack.pop(0)                        #get front element
        for move in allMoves:
            legal = True
            currMove = stackMove + move
            if(len(currMove) <= maxLimit):              #if has less moves than limit
                testBoard = resetBoard(board)
                findEmptySpace(testBoard)
                newBoard = doMoves(testBoard, currMove) #do set of moves on original board
                if(is_complete(newBoard) and legal == True):
                    print(newMove)
                    sys.exit()
                if(legal == True and len(currMove) < maxLimit): #if not over limit and legal moves
                    #stack.insert(0,currMove)
                    stack.append(currMove)


#Reverts the board back to the original (the one from the input parameters)
#Input: An mxn 2d array "board" in which moves have been performed.
#Output: The original board
def resetBoard(board):
    global OriginalBoard
    horizontal = len(OriginalBoard)
    vertical = len(OriginalBoard[0])

    for x in range(horizontal):                 #loop through rows
        for y in range(vertical):               #loop through columns
               board[x][y] = OriginalBoard[x][y]

    return board

#Performs a set of moves on the board, but ignores illegal moves or redundant moves
#Input: An mxn 2d array "board" in which a sequence of moves have been performed, a list
# containing mxn 2d "array" board of the same size as newBoard.
#Output:the resulting board from performing the moves
def doMoves(boardCopy,newMove):
    import sys
    global legal, row, column

    prev = "null"
    for move in newMove:                                #iterate over the moves in the string

        if(move == "U"):
            if(row != 0 and prev != "D"):               #If moveUp is legal
                moveUp(boardCopy)
                prev = "U"
            else:
                legal = False
                return boardCopy

        if(move == "D"):
            if(row != len(boardCopy) - 1 and prev != "U"): #if moveDown is legal
                moveDown(boardCopy)
                prev = "D"
            else:
                legal = False
                return boardCopy

        if(move == "L"):
            if(column != 0 and prev != "R"):              #if moveLeft is legal
               moveLeft(boardCopy)
               prev = "L"
            else:
                legal = False
                return boardCopy

        if(move == "R"):
            if(column != len(boardCopy[0]) - 1 and prev != "L"): # if moveRight is legal
                moveRight(boardCopy)
                prev = "R"
            else:
                legal = False
                return boardCopy

        if(is_complete(boardCopy)):                 #check if found solution to board
            print(newMove)                          #print the solution to the board
            sys.exit()

    return boardCopy

#Add the board to boardList
#Input: An mxn 2d array "board" that was created from the input parameter
#Output: None
def addtoList(board):
    global boardList
    horizontal = len(board)
    vertical = len(board[0])
    newBoard = [[0 for z in range(vertical)] for w in range(horizontal)]

    for x in range(horizontal):                 #loop through rows
        for y in range(vertical):               #loop through columns
               newBoard[x][y] = board[x][y]
    boardList.append(newBoard)

#Moves the empty space up, if legal
#Input: An mxn 2d array "board" that was created from the input parameter
#Output: True if legal move, False otherwise
def moveUp(board):
    global row, column

    if(row != 0):                               #check if the empty space is at the top of the board
        num = board[row - 1][column]
        board[row - 1][column] = 0
        board[row][column] = num
        row = row - 1                           #the empty space is now one row higher

        return True
    return False

#Moves the empty space down, if legal
#Input: An mxn 2d array "board" that was created from the input parameter
#Output: True if legal move, False otherwise
def moveDown(board):
    global row, column

    if(row != len(board[0]) - 1):               #check if the empty space is at the bottom of the board
        num = board[row + 1][column]
        board[row + 1][column] = 0
        board[row][column] = num
        row = row + 1                           #the empty space is now one row lower

        return True
    return False

#Moves the empty space left, if legal
#Input: An mxn 2d array "board" that was created from the input parameter
#Output: True if legal move, False otherwise
def moveLeft(board):
    global row, column

    if(column != 0):                            #check if the empty space is at the left end of the board
        num = board[row][column - 1]
        board[row][column - 1] = 0
        board[row][column] = num
        column = column - 1                     #the empty space is now one column to the left
        return True
    return False

#Moves the empty space right, if legal
#Input: An mxn 2d array "board" that was created from the input parameter
#Output: True if legal move, False otherwise
def moveRight(board):
    global row, column

    if (column != len(board[0]) - 1):           #check if the empty space is at the right end of the board
        num = board[row][column + 1]
        board[row][column + 1] = 0
        board[row][column] = num
        column = column + 1                     #the empty space is now one column to the right
        return True
    return False

#MAIN
def main():
    import sys
    global stack, OriginalBoard

    #read the input parameters and save the board into a 2d matrix
    board = [[int(n.strip()) for n in line.split(',')] for line in sys.stdin.readlines()]
    if(findEmptySpace(board) == False):
        print("Invalid board given, has no empty space")
        return
    if(is_complete(board)): #if already solved
        sys.exit()

    horizontal = len(board)
    vertical = len(board[0])
    OriginalBoard = [[0 for z in range(vertical)] for w in range(horizontal)]   #initialize the board

    storeCopy(board)    #save original board
    IDS(board)  #Perform iterative deepening search on board

if __name__ == "__main__":
    main()




