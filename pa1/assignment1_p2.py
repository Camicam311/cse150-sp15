#CSE 150 Programming assignment 1, problem 2
#Student Name: Rene Sanchez
#ID: A11866286
#Description: Reads an nxm n-puzzle from a .csv file and solves the
# puzzle using a Bread-First-Search traversal algorithm

from guppy import hpy

__author__ = 'risanche@ucsd.edu'
import Queue
from signal import signal, SIGPIPE, SIG_DFL
from math import factorial

global max_size 
max_size = 0

#Finds the '0' or empty space of the board, and updates the global row and column variables
#Ouput: True if a 0 was found, False otherwise
def findEmptySpace(board):
    global row, column, configs
    horizontal = len(board)
    vertical = len(board[0])

    size = horizontal*vertical
    config = (factorial(size))/2        #total number of solvable configurations for board

    for x in range(horizontal):  #loop through rows
        for y in range(vertical):        #loop through columns
            if(board[x][y] == 0):
                row = x
                column = y
                return True;
    return False;

#checks if the board is in a "solved" state
#Output: True if board is solved
def is_complete(board):
    global foundConfigs
    curr = 0
    for row in board:  #loop through rows
        for number in row:        #loop through columns
            if(number != curr):
                return False      #the puzzle isn't ordered correctly
            curr = curr + 1
    print foundConfigs
    return True

#Breath First Search algorithm that searches all possible sets of moves until it finds the combination that gives
#   the board a "solved" state
#Output: A string of moves for the solution if found, "UNSOLVABLE" otherwise
def BFS(board):
    import sys
    global boardList, legal, configs, foundConfigs

    horizontal = len(board)
    vertical = len(board[0])
    size = horizontal*vertical
    configs = (factorial(size))/2   #total number of solvable board configurations
    foundConfigs = 1

    boardCopy = board
    legal = True                    #if set of moves are legal
    allMoves = ["U","D","L","R"]
    boardList = []                  #keeps track of past boards reached
    boardList.append(board)
    global max_size
    if is_complete(board):
        print("Board is already solved, no moves needed")
        print h.heap() 
        print max_size
        return True
    q = Queue.Queue()
    findEmptySpace(board)
    q = enqueueMoves(board,q)   #Enqueue initial moves
    while(q.empty() != True):
        move = q.get()          #get a move that reached a new board
        for action in allMoves:
            legal = True
            newMove = move + action
            testBoard = resetBoard(board)   #revert back to the original
            findEmptySpace(testBoard)
            newBoard = doMoves(testBoard, newMove)  #do set of moves on original board
            if(inList(newBoard, boardList) == False and legal == True): #if not in boardList and legal moves
                    foundConfigs = foundConfigs + 1
                    if(foundConfigs >= configs):    #if we have found all solvable boards
                        print("UNSOLVABLE")
                        print h.heap() 
                        print max_size
                        sys.exit()
                    addtoList(newBoard) #add board to list of newly reached boards
                    q.put(newMove)
                    max_size = max(q.qsize(),max_size)


    print("UNSOLVABLE")
    print h.heap() 
    print max_size

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

#Checks if newBoard is in the boardList
#Output: True if in boardList, otherwise False
def inList(newBoard, boardList):
    horizontal = len(newBoard)
    vertical = len(newBoard[0])
    totalNodes = horizontal*vertical
    i = 0

    for boards in boardList:
        if(newBoard == boards):
            for x in range(horizontal):
                for y in range(vertical):
                    a = newBoard[x][y]
                    b = boards[x][y]
                    if(a == b):
                        i = i + 1
                if(i >= totalNodes - 1): #if all squares match
                    return True
                else:
                    i = 0
    return False

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
            print h.heap() 
            print max_size
            sys.exit()

    return boardCopy

#Inserts the inital set of moves into the queue
#Output: the queue with the legal initial moves inserted
def enqueueMoves(board,q):
    import sys
    global boardList, foundConfigs, row, column, max_size

    if(row != 0):
        moveUp(board)
        if(is_complete(board)):
            print("U")
            print h.heap() 
            print max_size
            sys.exit()
        q.put("U")
        max_size = max(q.qsize(),max_size)
        addtoList(board)
        moveDown(board)
        foundConfigs = foundConfigs + 1

    if(row != len(board) - 1):
        moveDown(board)
        if(is_complete(board)):
            print("D")
            print h.heap() 
            print max_size
            sys.exit()
        q.put("D")
        max_size = max(q.qsize(),max_size)
        addtoList(board)
        moveUp(board)
        foundConfigs = foundConfigs + 1

    if(column != 0):
        moveLeft(board)
        if(is_complete(board)):
            print("L")
            print h.heap() 
            print max_size
            sys.exit()
        q.put("L")
        max_size = max(q.qsize(),max_size)
        addtoList(board)
        moveRight(board)

        foundConfigs = foundConfigs + 1

    if(column != len(board[0]) - 1):
        moveRight(board)
        if(is_complete(board)):
            print("R")
            print h.heap() 
            print max_size
            sys.exit()
        q.put("R")
        max_size = max(q.qsize(),max_size)
        addtoList(board)
        moveLeft(board)
        foundConfigs = foundConfigs + 1

    return q

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

def storeCopy(board):
    global OriginalBoard
    horizontal = len(board)
    vertical = len(board[0])

    for x in range(horizontal):  #loop through rows
        for y in range(vertical):        #loop through columns
               OriginalBoard[x][y] = board[x][y]

#MAIN
def main():
    import sys
    global OriginalBoard
    #read the input parameters and save the board into a 2d matrix
    board = [[int(n.strip()) for n in line.split(',')] for line in sys.stdin.readlines()]
    horizontal = len(board)
    vertical = len(board[0])
    OriginalBoard = [[0 for z in range(vertical)] for w in range(horizontal)]
    if(findEmptySpace(board) == False):
        print("Invalid board given, has no empty space")
        return

    if(is_complete(board)): #if already solved
        print h.heap() 
        print max_size
        sys.exit()
    storeCopy(board)
    BFS(board)  #Perform Breath First Search on board

if __name__ == "__main__":
    h=hpy()
    main()



