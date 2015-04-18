from guppy import hpy


'''
CSE 150 Programming assignment 1, problem 5
Student Name: Rene Sanchez
ID: A11866286
Description: Reads an nxm n-puzzle from a .csv file and solves the
 puzzle using a A* traversal algorithm with a Manhattan-distance heuristic
'''

__author__ = 'risanche@ucsd.edu'

from signal import signal, SIGPIPE, SIG_DFL
from math import factorial
from Queue import PriorityQueue
from memory_profiler import profile

global max_size
max_size = 0

'''
Makes a board of what the mxn solution to the puzzle should be
Input: A board that you want to find the solution board to
Output: What the solution board should be
'''
def makeSolution(board):
    global solutionBoard
    horizontal = len(board)
    vertical = len(board[0])

    solutionBoard = [[0 for z in range(vertical)] for w in range(horizontal)] #initialize board

    curr = 0
    for x in range(horizontal):
        for y in range(vertical):
            solutionBoard[x][y] = curr
            curr = curr + 1

#Finds the '0' or empty space of the board, and updates the global row and column variables
#Ouput: True if a 0 was found, False otherwise
def findEmptySpace(board):
    global row, column, configs

    horizontal = len(board)
    vertical = len(board[0])
    # TODO: Are we guaranteed the board won't be jagged/will be valid? 
    # What if the gap is in first collumn?

    size = horizontal*vertical - 1
    config = (factorial(size))/2

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
    #Check if solved
    curr = 0
    global foundConfigs
    for row in board:  #loop through rows
        for number in row:        #loop through columns
            if(number != curr):
                return False      #the puzzle isn't ordered correctly
            curr = curr + 1
    print foundConfigs
    return True

#A* search algorithm that searches all possible sets of moves until it finds the combination that gives
#   the board a "solved" state. Uses a Manhattan distance heuristic
#Output: A string of moves for the solution if found
def aStar(board):
    import sys
    global boardList, q, legal, configs, foundConfigs, max_size

    horizontal = len(board)
    vertical = len(board[0])
    size = horizontal*vertical
    configs = (factorial(size))/2
    foundConfigs = 1

    boardList = []
    boardCopy = board
    legal = True
    allMoves = ["U","D","L","R"]
    boardList.append(board)
    findEmptySpace(board)

    q = PriorityQueue()     #priority queue that orders according to least total distance
    enqueueMoves(board)     #add initial moves to queue
    while(q.empty() != True):
        move = q.get()[1]
        for action in allMoves:
            legal = True
            newMove = move + action
            testBoard = resetBoard(board)   #get original board
            findEmptySpace(testBoard)
            newBoard = doMoves(testBoard, newMove)  #do sequence of moves on board
            if(inList(newBoard, boardList) == False and legal == True): #reached a new board with legal moves
                    foundConfigs = foundConfigs + 1
                    if(is_complete(newBoard)):
                        sys.exit()
                    if(foundConfigs >= configs):    #found all solvable board configurations
                        print("UNSOLVABLE")
                        print h.heap()
                        print max_size
                        sys.exit()
                    addtoList(newBoard)
                    q.put((len(newMove) + findSimilarity(newBoard),newMove))    #add word to queue
                    l = []
                    for elem in list(q.queue):
                        l+=elem
                    print l
                    max_size = max(q.qsize(),max_size)
    print("UNSOLVABLE")
    print h.heap()
    print max_size

#Heuristic function that determines how close the board is to the "solved" board
#   based on how far each number is from their correct box
#Output: The heuristic value of the board, integer
def findSimilarity(newBoard):
    global solutionBoard
    vertical = len(newBoard[0])
    horizontal = len(newBoard)

    priority = 0
    for x in range(horizontal):  #loop through rows
        for y in range(vertical):        #loop through columns
               if(newBoard[x][y] != solutionBoard[x][y]):
                   thisLoc = (x,y)                                      #location of this value in newBoard
                   trueLoc = getCoordinates(solutionBoard, newBoard[x][y])      #get true location of this value
                   priority = priority + abs(thisLoc[0] - trueLoc[0]) + abs(thisLoc[1] - trueLoc[1]) #distance

    return priority

#Finds the coordinates for a given number in a board
#Output: None
def getCoordinates(board, number):
    vertical = len(board[0])
    horizontal = len(board)
    for x in range(horizontal):  #loop through rows
        for y in range(vertical):        #loop through columns
            if(board[x][y] == number):
                return (x,y)

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
                if(i >= totalNodes - 1):
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
            global max_size
            print max_size
            sys.exit()

    return boardCopy

#Inserts the inital set of moves into the queue
#Output: the queue with the legal initial moves inserted
def enqueueMoves(board):
    import sys
    global boardList, foundConfigs, row, column, q, max_size

    if(row != 0):
        moveUp(board)
        if(is_complete(board)):
            print("U")
            sys.exit()
        q.put((1 + findSimilarity(board),"U"))
        max_size = max(q.qsize(),max_size)
        addtoList(board)
        moveDown(board)
        foundConfigs = foundConfigs + 1

    if(row != len(board) - 1):
        moveDown(board)
        if(is_complete(board)):
            print("D")
            sys.exit()
        q.put((1 + findSimilarity(board),"D"))
        max_size = max(q.qsize(),max_size)
        addtoList(board)
        moveUp(board)
        foundConfigs = foundConfigs + 1

    if(column != 0):
        moveLeft(board)
        if(is_complete(board)):
            print("L")
            sys.exit()
        q.put((1 + findSimilarity(board),"L"))
        max_size = max(q.qsize(),max_size)
        addtoList(board)
        moveRight(board)

        foundConfigs = foundConfigs + 1

    if(column != len(board[0]) - 1):
        moveRight(board)
        if(is_complete(board)):
            print("R")
            sys.exit()
        q.put((1 + findSimilarity(board),"R"))
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
    is_complete(newBoard)

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

#saves copy of the original board to a global variable
#Output: none
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
    if(findEmptySpace(board) == False):
        print("Invalid board given, has no empty space")
        return

    if(is_complete(board)): #check if already solved
        sys.exit()

    horizontal = len(board)
    vertical = len(board[0])
    OriginalBoard = [[0 for z in range(vertical)] for w in range(horizontal)]

    storeCopy(board)    #make copy of original board

    makeSolution(board)

    aStar(board)    #perform A* seach on board

if __name__ == "__main__":
    h=hpy()
    main()


