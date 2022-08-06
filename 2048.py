""" Game:2048, by Yasar Murat, yasarmurat@msn.com

A single-player sliding tile puzzle game.
"""

import random, sys

# Constants used for displaying the board:
EMPTY_SPACE = " "
INITIAL_FILLED_CELL = 6  # Used for filling cells with '2's when creating new board.
MAX_EXPONENT = 1  # Used when creating new board and placing numbers in random cells while playing game.
TARGET = 2048  # The goal of the game is to reach the TARGET and the TARGET can be changed.
BOARD_WIDTH = 4
BOARD_HEIGHT = 4
assert BOARD_WIDTH == BOARD_HEIGHT == 4

# The string for displaying the board:
BOARD_TEMPLATE = """
   ___________________________________
  |        |        |        |        |
  | {} | {} | {} | {} |
  |________|________|________|________|
  |        |        |        |        |
  | {} | {} | {} | {} |
  |________|________|________|________|
  |        |        |        |        |
  | {} | {} | {} | {} |
  |________|________|________|________|
  |        |        |        |        |
  | {} | {} | {} | {} |
  |________|________|________|________|
"""


def main():
    """Runs a single game of 2048."""

    print(
        """Game:2048, by Yasar Murat, yasarmurat@msn.com

Slide numbered tiles on a grid to combine them to create a tile with the number 2048
"""
    )

    # Set up the game:
    gameBoard = boardSetup()

    while True:  # Run a player's turn.

        # Display the board:
        displayBoard(gameBoard)

        # Decide whether a move is possible and get possible directions.
        isMovePossible, possibleDirections = canMakeAMove(gameBoard)

        if isMovePossible:
            print(f"Possible directions : {possibleDirections}\n")

            # Get player move
            direction = getPlayerMove()

            # Make the move and update the game board accordingly
            gameBoard = makePlayerMove(gameBoard, direction)

            # Check whether the TARGET is reached
            if isWinner(gameBoard):
                print(f"WELL DONE! You reached {TARGET}")
                input("Press ENTER to exit!")
                sys.exit()
            else:
                gameBoard = addNewNumber(gameBoard, isMovePossible)
                saveToFile(gameBoard)
        else:
            print("GAME OVER!")
            print("The board is full and there is no more valid move!")
            input("Press ENTER to exit!")
            sys.exit()


def boardSetup():
    """Asks player if they want to load previous board or get a new one and returns a dictionary that represents a 2048 board."""

    while True:
        print("Do you want to load your last board? (Y/N)")
        response = input("> ").upper().strip()

        if response.startswith("Y"):
            try:
                board = loadOldBoard()
                break
            except FileNotFoundError:
                print("There is no saved board. Getting you a new one.")
                board = getNewBoard()
                break
        elif response.startswith("N"):
            board = getNewBoard()
            break

    # Save the board to a file for later use.
    saveToFile(board)

    return board


def loadOldBoard():
    """Reads a certain file and returns a dictionary that represents the last played 2048 board."""

    with open("2048.values", "r") as fileObj:
        valueStr = fileObj.read()

    valueList = []
    n = 0
    while True:
        try:  # Used for integers
            valueList.append(int(valueStr[n : n + 4]))  # Since '2048' has 4 digits, it reads values as blocks of 4
        except ValueError:  # Used for empty spaces
            valueList.append(" ")
        n += 4
        if n == 4 * BOARD_HEIGHT * BOARD_WIDTH:
            break

    board = {}
    i = 0
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            board[(x, y)] = valueList[i]
            i += 1

    return board


def getNewBoard():
    """Returns a dictionary that represents a new 2048 board.
    The keys are (columnIndex, rowIndex) tuples of two integers and the values are '2's and empty space strings."""

    board = {}
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            board[(x, y)] = EMPTY_SPACE

    cells = []
    while True:
        cell = (random.randint(0, 3), random.randint(0, 3))
        if not cell in cells:
            board[(cell)] = 2 ** random.randint(1, MAX_EXPONENT)
            cells.append(cell)
            if len(cells) == INITIAL_FILLED_CELL:
                break

    return board


def saveToFile(board):
    """Takes the board as parameter and converts its values into one single string value to write to a file for later use."""

    valueList = list(board.values())
    valueStr = ""
    for i in range(len(valueList)):
        # Every cell value is converted to a string of a lenght of 4 since 2048 has maximum 4 digits
        valueStr += "{:4}".format(valueList[i])

    with open("2048.values", "w") as fileObj:
        fileObj.write(valueStr)


def displayBoard(board):
    """Displays the board and its cells on the screen.

    Prepares a list to pass to the format() string method for the board template.
    The list holds all of the board's digits (and empty spaces) going left to right, top to bottom:"""

    cellDigits = []
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            cellDigits.append(str(board[(x, y)]).center(6))

    print(BOARD_TEMPLATE.format(*cellDigits))


def canMakeAMove(board):
    """Returns True if there is still empty cells on the board, else returns False.

    The function also returns Possible Moves to use as a Hint."""

    result = False
    possibleMoves = []
    directions = ["Up", "Down", "Right", "Left"]

    # Simulates every direction one by one and tries to get empty cells
    for direction in directions:
        tempBoard = makePlayerMove(board, direction)
        emptyCells = []
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if tempBoard[(x, y)] == EMPTY_SPACE:
                    emptyCells.append((x, y))

        numOfEmptyCells = len(emptyCells)
        if not numOfEmptyCells == 0:
            result = True
            possibleMoves.append(direction)

    return result, possibleMoves


def getPlayerMove():
    """Let the player select a direction to make a move."""

    print("Please choose your direction : (W) Up, (S) Down, (A) Left, (D) Right or (Q)uit.")
    while True:
        response = input("> ").upper().strip()

        if response.startswith("Q"):
            print("Thank you for playing!")
            input("Press ENTER to exit.")
            sys.exit()
        elif response.startswith("W"):
            direction = "Up"
            break
        elif response.startswith("S"):
            direction = "Down"
            break
        elif response.startswith("A"):
            direction = "Left"
            break
        elif response.startswith("D"):
            direction = "Right"
            break
        else:
            print("Please choose your direction : (W) Up, (S) Down, (A) Left, (D) Right or (Q)uit.")

    return direction


def makePlayerMove(board, direction):
    """Moves all digits according to the selected direction and adds all successive same digits while moving."""

    if direction == "Up":
        # move board digits all upward.

        boardColomns = []
        for x in range(BOARD_WIDTH):
            subColomn = []
            for y in range(BOARD_HEIGHT):
                if not board[(x, y)] == EMPTY_SPACE:
                    digit = board[(x, y)]
                    subColomn.append(digit)
            boardColomns.append(subColomn)

        # add up if there are two same digits following each other.
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                try:
                    digit = boardColomns[y][x]
                    nextDigit = boardColomns[y][x + 1]
                    if digit == nextDigit:
                        digit += nextDigit
                        boardColomns[y][x] = digit
                        del boardColomns[y][x + 1]
                except IndexError:
                    pass

        # prepare a new board with updated data.
        newBoard = {}
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                try:
                    newBoard[(x, y)] = boardColomns[x][y]
                except IndexError:
                    newBoard[(x, y)] = " "

        return newBoard

    if direction == "Down":
        # move board digits all downward

        boardColomns = []
        for x in range(BOARD_WIDTH - 1, -1, -1):
            subColomn = []
            for y in range(BOARD_HEIGHT - 1, -1, -1):
                if not board[(x, y)] == EMPTY_SPACE:
                    digit = board[(x, y)]
                    subColomn.append(digit)
            boardColomns.append(subColomn)

        # add up if there are two same digits following each other
        for y in range(BOARD_HEIGHT - 1, -1, -1):
            for x in range(BOARD_WIDTH - 1, -1, -1):
                try:
                    digit = boardColomns[y][x]
                    nextDigit = boardColomns[y][x + 1]
                    if digit == nextDigit:
                        digit += nextDigit
                        boardColomns[y][x] = digit
                        del boardColomns[y][x + 1]
                except IndexError:
                    pass

        # arrange the boardColomns list so as to prepare the board dictionary
        for i in range(BOARD_HEIGHT):
            boardColomns[i].reverse()
        boardColomns.reverse()
        n = 0
        while True:
            numOfDigits = len(boardColomns[n])
            for i in range(BOARD_HEIGHT - numOfDigits):
                boardColomns[n].insert(0, " ")
            n += 1
            if n == BOARD_HEIGHT:
                break

        # prepare a new board with updated data
        newBoard = {}
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                newBoard[(x, y)] = boardColomns[x][y]

        return newBoard

    if direction == "Left":
        # move board digits all rightward

        boardRows = []
        for y in range(BOARD_HEIGHT):
            subRow = []
            for x in range(BOARD_WIDTH):
                if not board[(x, y)] == EMPTY_SPACE:
                    digit = board[(x, y)]
                    subRow.append(digit)
            boardRows.append(subRow)

        # add up if there are two same digits following each other
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                try:
                    digit = boardRows[x][y]
                    nextDigit = boardRows[x][y + 1]
                    if digit == nextDigit:
                        digit += nextDigit
                        boardRows[x][y] = digit
                        del boardRows[x][y + 1]
                except IndexError:
                    pass

        # prepare a new board with updated data
        newBoard = {}
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                try:
                    newBoard[(y, x)] = boardRows[x][y]
                except IndexError:
                    newBoard[(y, x)] = " "

        return newBoard

    if direction == "Right":
        # move board digits all rightward

        boardRows = []
        for y in range(BOARD_HEIGHT - 1, -1, -1):
            subRow = []
            for x in range(BOARD_WIDTH - 1, -1, -1):
                if not board[(x, y)] == EMPTY_SPACE:
                    digit = board[(x, y)]
                    subRow.append(digit)
            boardRows.append(subRow)

        # add up if there are two same digits following each other
        for x in range(BOARD_WIDTH - 1, -1, -1):
            for y in range(BOARD_HEIGHT - 1, -1, -1):
                try:
                    digit = boardRows[x][y]
                    nextDigit = boardRows[x][y + 1]
                    if digit == nextDigit:
                        digit += nextDigit
                        boardRows[x][y] = digit
                        del boardRows[x][y + 1]
                except IndexError:
                    pass

        # arrange the boardRows list so as to prepare the board dictionary
        for i in range(BOARD_HEIGHT):
            boardRows[i].reverse()
        boardRows.reverse()
        n = 0
        while True:
            numOfDigits = len(boardRows[n])
            for i in range(BOARD_HEIGHT - numOfDigits):
                boardRows[n].insert(0, " ")
            n += 1
            if n == BOARD_HEIGHT:
                break

        # prepare a new board with updated data
        newBoard = {}
        for y in range(BOARD_WIDTH):
            for x in range(BOARD_HEIGHT):
                newBoard[(x, y)] = boardRows[y][x]

        return newBoard


def isWinner(board):
    """Checks whether in any of the board cells the TARGET is reached."""

    result = False
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[(x, y)] == TARGET:
                result = True

    return result


def addNewNumber(board, movePossible):
    """Adds a new number according to 'MAX_EXPONENT' to the board with a %50 chance."""

    emptyCells = []
    for y in range(BOARD_HEIGHT):
        for x in range(BOARD_WIDTH):
            if board[(x, y)] == EMPTY_SPACE:
                emptyCells.append((x, y))

    if len(emptyCells) == 0:
        if movePossible:
            return board
        else:
            print("GAME OVER!")
            print("The board is full and there is no more valid move.")
            input("Press ENTER to exit!")
            sys.exit()
    else:
        cellToPlaceNewNumber = random.choice(emptyCells)
        if random.randint(0, 1) == 1:
            board[cellToPlaceNewNumber] = 2 ** random.randint(1, MAX_EXPONENT)

        return board


if __name__ == "__main__":
    main()
