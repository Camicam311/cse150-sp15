#CSE 150 Programming assignment 1, problem 3
#Student Name: Rene Sanchez
#ID: A11866286
#Description: Reads an nxm n-puzzle from a .csv file and solves the
# puzzle using a depth-limited search traversal algorithm

__author__ = 'risanche@ucsd.edu'
from multiprocessing import Queue
from signal import signal, SIGPIPE, SIG_DFL
from math import factorial

#Finds the '0' or empty space of the board, and updates the global row and column variables
#Ouput: True if a 0 was found, False otherwise
def findEmptySpace(board):
    global row, column, configs

    horizontal = len(board)
    vertical = len(board[0])
    size = horizontal*vertical
    config = (factorial(size))/2    #total number of solvable configurations for board

    for x in range(horizontal):  #loop through rows
        for y in range(vertical):        #loop through columns
            if(board[x][y] == 0):
                row = x
                column = y
                return True;
    return False;

#Saves a copy of the original board into a global variable
#Output: None
def storeCopy(board):
    global OriginalBoard

    horizontal = len(board)
    vertical = len(board[0])

    for x in range(horizontal):  #loop through rows
        for y in range(vertical):        #loop through columns
               OriginalBoard[x][y] = board[x][y]

#checks if the board is in a "solved" state
#Output: True if board is solved
def is_complete(board):
    curr = 0
    for row in board:  #loop through rows
        for number in row:        #loop through columns
            if(number != curr):
                return False      #the puzzle isn't ordered correctly
            curr = curr + 1
    return True

#Depth Limited Seach algorithm that searches all possible sets of moves until it finds the combination that gives
#   the board a "solved" state
#Output: A string of moves for the solution if found, "UNSOLVABLE" otherwise
def DLS(board):
    import sys
    global maxLimit, stack, legal

    stack = []
    maxLimit = 5

    allMoves = ["U","D","L","R"]
    currMove = ""
    stack.insert(0,currMove)
    while(len(stack) != 0):   #stack isn't empty
        stackMove = stack.pop(0)    #get front element
        for move in allMoves:
            legal = True
            currMove = stackMove + move
            if(len(currMove) <= maxLimit): #if has less moves than limit
                testBoard = resetBoard(board)
                findEmptySpace(testBoard)
                newBoard = doMoves(testBoard, currMove) #do set of moves on original board
                if(is_complete(newBoard) and legal == True):
                    print(newMove)
                    sys.exit()
                if(legal == True and len(currMove) < maxLimit): #if not over limit and legal moves
                    stack.insert(0,currMove)
    print("UNSOLVABLE")

#Reverts the board back to the original (the one from the input parameters)
#Output: The original board
def resetBoard(board):
    global OriginalBoard
    horizontal = len(OriginalBoard)
    vertical = len(OriginalBoard[0])

    for x in range(horizontal):  #loop through rows
        for y in range(vertical):        #loop through columns
               board[x][y] = OriginalBoard[x][y]

    return board

#Performs a set of moves on the board, but ignores illegal moves or redundant moves
#Output:the resulting board from performing the moves
def doMoves(boardCopy,newMove):
    import sys
    global legal, row, column

    prev = "null"
    for move in newMove:
        if(move == "U"):
            if(row != 0 and prev != "D"):
                moveUp(boardCopy)
                prev = "U"
            else:
                legal = False
                return boardCopy
        if(move == "D"):
            if(row != len(boardCopy) - 1 and prev != "U"):
                moveDown(boardCopy)
                prev = "D"
            else:
                legal = False
                return boardCopy
        if(move == "L"):
            if(column != 0 and prev != "R"):
               moveLeft(boardCopy)
               prev = "L"
            else:
                legal = False
                return boardCopy
        if(move == "R"):
            if(column != len(boardCopy[0]) - 1 and prev != "L"):
                moveRight(boardCopy)
                prev = "R"
            else:
                legal = False
                return boardCopy

        if(is_complete(boardCopy)):
            print(newMove)
            sys.exit()

    return boardCopy

#Inserts the inital set of moves into the queue
#Output: the queue with the legal initial moves inserted
def enqueueMoves(board):
    import sys
    global row, column, stack
    stack = []

    if(row != 0):
        moveUp(board)
        if(is_complete(board)):
            print("U")
            sys.exit()
        stack.append("U")
        moveDown(board)

    if(row != len(board) - 1):
        moveDown(board)
        if(is_complete(board)):
            print("D")
            sys.exit()
        stack.append("D")
        moveUp(board)

    if(column != 0):
        moveLeft(board)
        if(is_complete(board)):
            print("L")
            sys.exit()
        stack.append("L")
        moveRight(board)

    if(column != len(board[0]) - 1):
        moveRight(board)
        if(is_complete(board)):
            print("R")
            sys.exit()
        stack.append("R")
        moveLeft(board)

    return stack

#Add the board to boardList
#Output: None
def addtoList(board):
    global boardList
    horizontal = len(board)
    vertical = len(board[0])
    newBoard = [[0 for z in range(vertical)] for w in range(horizontal)]

    for x in range(horizontal):  #loop through rows
        for y in range(vertical):        #loop through columns
               newBoard[x][y] = board[x][y]
    boardList.append(newBoard)

#Moves the empty space up, if legal
#Output: True if legal move, False otherwise
def moveUp(board):
    global row, column

    if(row != 0):   #check if we are moving up from the top of the puzzle
        num = board[row - 1][column]
        board[row - 1][column] = 0
        board[row][column] = num
        row = row - 1

        return True
    return False

#Moves the empty space down, if legal
#Output: True if legal move, False otherwise
def moveDown(board):
    global row, column

    if(row != len(board[0]) - 1): #check if we are moving down from the bottom of the puzzle
        num = board[row + 1][column]
        board[row + 1][column] = 0
        board[row][column] = num
        row = row + 1

        return True
    return False

#Moves the empty space left, if legal
#Output: True if legal move, False otherwise
def moveLeft(board):
    global row, column

    if(column != 0): #check if we are moving left from the left edge of the puzzle
        num = board[row][column - 1]
        board[row][column - 1] = 0
        board[row][column] = num
        column = column - 1
        return True
    return False

#Moves the empty space right, if legal
#Output: True if legal move, False otherwise
def moveRight(board):
    global row, column

    if (column != len(board[0]) - 1):  #check if we are moving right from the right edge of the puzzle
        num = board[row][column + 1]
        board[row][column + 1] = 0
        board[row][column] = num
        column = column + 1
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
    OriginalBoard = [[0 for z in range(vertical)] for w in range(horizontal)]

    storeCopy(board)    #save original board

    DLS(board)  #Perform depth limited search on board

if __name__ == "__main__":
    main()



