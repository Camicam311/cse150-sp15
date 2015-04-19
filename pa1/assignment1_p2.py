#CSE 150 Programming assignment 1, problem 2
#Student Names: Rene Sanchez, Chris Weller, Divyansh H Vaishnav
#IDs: Rene Sanchez: A11866286, Chris Weller: , Divyansh H Vaishnav
#Description: Reads an nxm n-puzzle from a .csv file and solves the
# puzzle using a Bread-First-Search traversal algorithm

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
    config = (factorial(size))/2           #total number of solvable configurations for board

    for x in range(horizontal):            #loop through rows
        for y in range(vertical):          #loop through columns
            if(board[x][y] == 0):
                row = x
                column = y
                return True;
    return False;

#checks if the board is in a "solved" state
#Input: An mxn 2d array "board" that you want to check if is "solved"
#Output: True if board is solved
def is_complete(board):
    curr = 0

    for row in board:                     #loop through rows
        for number in row:                #loop through columns
            if(number != curr):
                return False              #the puzzle isn't ordered correctly
            curr = curr + 1
    return True

#Breath First Search algorithm that searches all possible sets of moves until it finds the combination that gives
#   the board a "solved" state
#Input: A non-solved mxn 2d array "board" that you want to find the solution to.
#Output: A string of moves for the solution if found, "UNSOLVABLE" otherwise
def BFS(board):
    import sys
    global boardList, legal, configs, foundConfigs

    horizontal = len(board)
    vertical = len(board[0])
    size = horizontal*vertical
    configs = (factorial(size))/2        #total number of solvable board configurations
    foundConfigs = 1                     #1 because of original board configuration from input

    boardCopy = board
    legal = True                         #if set of moves are legal
    allMoves = ["U","D","L","R"]
    boardList = []                       #keeps track of past boards reached
    boardList.append(board)
    if is_complete(board):
        print("Board is already solved, no moves needed")
        return True
    q = Queue.Queue()
    findEmptySpace(board)
    q = enqueueMoves(board,q)           #Enqueue initial moves {U,D,L,R}
    while(q.empty() != True):
        move = q.get()                  #get a move that reached a new board
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
                        sys.exit()
                    addtoList(newBoard) #add board to list of newly reached boards
                    q.put(newMove)

    print("UNSOLVABLE")

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

#Checks if newBoard is in the boardList (where boardList stores the list of new
# board configurations found)
#Input: An mxn 2d array "board" in which a sequence of moves have been performed, a list
# containing mxn 2d "array" board of the same size as newBoard.
#Output: True if in boardList, otherwise False
def inList(newBoard, boardList):
    horizontal = len(newBoard)
    vertical = len(newBoard[0])
    totalNodes = horizontal*vertical
    i = 0

    for boards in boardList:
        if(newBoard == boards):
            for x in range(horizontal):      #loop through rows
                for y in range(vertical):    #loop through columns
                    a = newBoard[x][y]
                    b = boards[x][y]
                    if(a == b):
                        i = i + 1
                if(i >= totalNodes - 1):     #if all squares match
                    return True
                else:
                    i = 0
    return False

#Performs a set of moves on the board, but ignores illegal moves or redundant moves
#Input: An mxn 2d array "board" that is a copy of the original board from the input parameter, a string
# consisting of the chars {'U','D','L','R'}, which represent moves that will be performed
# on boardCopy
#Output:the resulting board from performing the moves
def doMoves(boardCopy,newMove):
    import sys
    global legal, row, column

    prev = "null"
    for move in newMove:                        #iterate over the moves in the string

        if(move == "U"):
            if(row != 0 and prev != "D"):       #If moveUp is legal
                moveUp(boardCopy)
                prev = "U"
            else:
                legal = False
                return boardCopy
        if(move == "D"):
            if(row != len(boardCopy) - 1 and prev != "U"):  #if moveDown is legal
                moveDown(boardCopy)
                prev = "D"
            else:
                legal = False
                return boardCopy
        if(move == "L"):
            if(column != 0 and prev != "R"):   #if moveLeft is legal
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

        if(is_complete(boardCopy)):         #check if found solution to board
            print(newMove)                  #print the solution to the board
            sys.exit()

    return boardCopy

#Inserts the inital set of moves into the queue
#Input: An mxn 2d array "board" that was created from the input parameter, a queueu that stores strings consisting of
# the moves {'U', 'D', 'L', 'R'} which represent moves performed on the board
#Output: the queue with the legal initial moves inserted
def enqueueMoves(board,q):
    import sys
    global boardList, foundConfigs, row, column

    if(row != 0):                           #if moveUp is a legal move
        moveUp(board)
        if(is_complete(board)):             #Check if this move solves the board
            print("U")
            sys.exit()
        q.put("U")
        addtoList(board)
        moveDown(board)
        foundConfigs = foundConfigs + 1

    if(row != len(board) - 1):              #if moveDown is a legal move
        moveDown(board)
        if(is_complete(board)):             #Check if this move solves the board
            print("D")
            sys.exit()
        q.put("D")
        addtoList(board)
        moveUp(board)
        foundConfigs = foundConfigs + 1

    if(column != 0):                        #if moveLeft is a legal move
        moveLeft(board)
        if(is_complete(board)):             #Check if this move solves the board
            print("L")
            sys.exit()
        q.put("L")
        addtoList(board)
        moveRight(board)

        foundConfigs = foundConfigs + 1

    if(column != len(board[0]) - 1):        #if moveRight is a legal move
        moveRight(board)
        if(is_complete(board)):             #Check if this move solves the board
            print("R")
            sys.exit()
        q.put("R")
        addtoList(board)
        moveLeft(board)
        foundConfigs = foundConfigs + 1

    return q

#Add the board to the boardList, which stores all new board configurations reached by performing move on the
# original board.
#Input: An mxn 2d array "board" that was created from the input parameter
#Output: None
def addtoList(board):
    global boardList

    horizontal = len(board)
    vertical = len(board[0])
    newBoard = [[0 for z in range(vertical)] for w in range(horizontal)]

    for x in range(horizontal):             #loop through rows
        for y in range(vertical):           #loop through columns
               newBoard[x][y] = board[x][y]
    boardList.append(newBoard)

#Moves the empty space up, if legal
#Input: An mxn 2d array "board" that was created from the input parameter
#Output: True if legal move, False otherwise
def moveUp(board):
    global row, column

    if(row != 0):                       #check if the empty space is at the top of the board
        num = board[row - 1][column]
        board[row - 1][column] = 0
        board[row][column] = num
        row = row - 1                   #the empty space is now one row higher

        return True
    return False

#Moves the empty space down, if legal
#Input: An mxn 2d array "board" that was created from the input parameter
#Output: True if legal move, False otherwise
def moveDown(board):
    global row, column

    if(row != len(board[0]) - 1):       #check if the empty space is at the bottom of the board
        num = board[row + 1][column]
        board[row + 1][column] = 0
        board[row][column] = num
        row = row + 1                   #the empty space is now one row lower

        return True
    return False

#Moves the empty space left, if legal
#Input: An mxn 2d array "board" that was created from the input parameter
#Output: True if legal move, False otherwise
def moveLeft(board):
    global row, column

    if(column != 0):                    #check if the empty space is at the left end of the board
        num = board[row][column - 1]
        board[row][column - 1] = 0
        board[row][column] = num
        column = column - 1             #the empty space is now one column to the left
        return True
    return False

#Moves the empty space right, if legal
#Input: An mxn 2d array "board" that was created from the input parameter
#Output: True if legal move, False otherwise
def moveRight(board):
    global row, column

    if (column != len(board[0]) - 1):  #check if the empty space is at the right end of the board
        num = board[row][column + 1]
        board[row][column + 1] = 0
        board[row][column] = num
        column = column + 1            #the empty space is now one column to the right
        return True
    return False

#saves copy of the original board to a global variable
#Input: An mxn 2d array "board" that was created from the input parameter
#Output: none
def storeCopy(board):
    global OriginalBoard
    horizontal = len(board)
    vertical = len(board[0])

    for x in range(horizontal):          #loop through rows
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

    if(is_complete(board)): #if already solved
        sys.exit()

    horizontal = len(board)
    vertical = len(board[0])
    OriginalBoard = [[0 for z in range(vertical)] for w in range(horizontal)]   #initialize the board

    storeCopy(board)    #make copy of original board


    BFS(board)  #Perform Breath First Search on board

if __name__ == "__main__":
    main()



