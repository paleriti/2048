import random, sys

EMPTY_SPACE = ' '
INITIAL_FILLED_CELL = 6
MAX_EXPONENT = 1 # Used when creating new board
TARGET = 2048
BOARD_WIDTH = 4
BOARD_HEIGHT = 4
assert BOARD_WIDTH == BOARD_HEIGHT == 4

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
	
	gameBoard = boardSetup()
	
	while True:
		displayBoard(gameBoard)
		isMovePossible, possibleDirections = canMakeAMove(gameBoard)
		if isMovePossible:
			print(f'Possible directions : {possibleDirections}\n')
			direction = getPlayerMove()
			gameBoard = makePlayerMove(gameBoard, direction)
			if isWinner(gameBoard):
				print(f'WELL DONE! You reached {TARGET}')
				displayBoard(gameBoard)
				sys.exit()
			else:
				gameBoard = addNewNumber(gameBoard, isMovePossible)
				saveToFile(gameBoard)
		else:
			print('GAME OVER!')
			print('You have no more valid move!')
			sys.exit()
			
def boardSetup():
	
	while True:
		print("Do you want to load your last board? (Y/N)")
		response = input("> ").upper().strip()
		
		if response.startswith('Y'):
			try:
				board = loadOldBoard()
				break
			except FileNotFoundError:
				print('There is no saved board. Getting you a new one.')
				board = getNewBoard()
				break
		elif response.startswith('N'):
			board = getNewBoard()
			break
	
	# Save the board to a file for later use.
	saveToFile(board)
	
	return board
	
def loadOldBoard():
	with open('2048-values.vdb', 'r') as fileObj:
		valueStr = fileObj.read()
	
	valueList = []
	n = 0
	while True:
		try:
			valueList.append(int(valueStr[n:n+4]))
		except ValueError:
			valueList.append(' ')
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
	
	board = {}
	for y in range(BOARD_HEIGHT):
		for x in range(BOARD_WIDTH):
			board[(x, y)] = EMPTY_SPACE
	
	cells = []
	while True:
		cell = (random.randint(0,3), random.randint(0,3))
		if not cell in cells:
			board[(cell)] = 2 ** random.randint(1, MAX_EXPONENT)
			cells.append(cell)
			if len(cells) == INITIAL_FILLED_CELL:
				break
				
	return board

def saveToFile(board):
	
	valueList = list(board.values())
	valueStr = ''
	for i in range(len(valueList)):
		valueStr += '{:4}'.format(valueList[i])
	
	with open('2048-values.vdb', 'w') as fileObj:
		fileObj.write(valueStr)

def displayBoard(board):
		
	cellDigits = []
	for y in range(BOARD_HEIGHT):
		for x in range(BOARD_WIDTH):
			cellDigits.append(str(board[(x, y)]).center(6))
	
	print(BOARD_TEMPLATE.format(*cellDigits))

def canMakeAMove(board):
		
		result = False
		possibleMoves = []
		directions = ['Up', 'Down', 'Right', 'Left']
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
	
	print("Please choose your direction : (U)p, (D)own, (L)eft, (R)ight or (Q)uit.")
	
	while True:
		response = input('> ').upper().strip()
		
		if response.startswith('Q'):
			print('Thank you for playing!')
			input('Press ENTER to exit.')
			sys.exit()
			
		elif response.startswith('U'):
			direction = 'Up'
			break
		elif response.startswith('D'):
			direction = 'Down'
			break
		elif response.startswith('L'):
			direction = 'Left'
			break
		elif response.startswith('R'):
			direction = 'Right'
			break
			
		else:
			print("Please choose your direction : (U)p, (D)own, (L)eft, (R)ight or (Q)uit.")
		
	return direction
	
def makePlayerMove(board, direction):
	
	if direction == 'Up':
		
		# move board digits all upward
		boardColomns = []
		for x in range(BOARD_WIDTH):
			subColomn = []
			for y in range(BOARD_HEIGHT):
				if not board[(x, y)] == EMPTY_SPACE:
					digit = board[(x, y)]
					subColomn.append(digit)
			boardColomns.append(subColomn)
		
		# add up if there are two same digits following each other
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
		
		# prepare a new board with updated data
		newBoard = {}
		for y in range(BOARD_HEIGHT):
			for x in range(BOARD_WIDTH):
				try:
					newBoard[(x, y)] = boardColomns[x][y]
				except IndexError:
					newBoard[(x, y)] = ' '
					
		return newBoard
		
	if direction == 'Down':
		
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
		for y in range(BOARD_HEIGHT -1, -1, -1):
			for x in range(BOARD_WIDTH -1, -1, -1):
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
				boardColomns[n].insert(0, ' ')
			n += 1
			if n == BOARD_HEIGHT:
				break
		
		# prepare a new board with updated data
		newBoard = {}
		for y in range(BOARD_HEIGHT):
			for x in range(BOARD_WIDTH):
					newBoard[(x, y)] = boardColomns[x][y]
					
		return newBoard

	if direction == 'Left':
		
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
					newBoard[(y, x)] = ' '
		
		return newBoard
		
	if direction == 'Right':
		
		# move board digits all rightward
		boardRows = []
		for y in range(BOARD_HEIGHT -1, -1, -1):
			subRow = []
			for x in range(BOARD_WIDTH -1, -1, -1):
				if not board[(x, y)] == EMPTY_SPACE:
					digit = board[(x, y)]
					subRow.append(digit)
			boardRows.append(subRow)
		
		# add up if there are two same digits following each other
		for x in range(BOARD_WIDTH -1, -1, -1):
			for y in range(BOARD_HEIGHT -1, -1, -1):
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
				boardRows[n].insert(0, ' ')
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
	
	result = False
	for y in range(BOARD_HEIGHT):
		for x in range(BOARD_WIDTH):
			if board[(x, y)] == TARGET:
				result = True
	return result
	
def addNewNumber(board, movePossible):
	
	emptyCells = []
	for y in range(BOARD_HEIGHT):
		for x in range(BOARD_WIDTH):
			if board[(x, y)] == EMPTY_SPACE:
				emptyCells.append((x, y))
				
	if len(emptyCells) == 0:
		if movePossible:
			return board
		else:
			print('There is no more empty cell to add a new number.')
			print('GAME OVER!')
			sys.exit()
	else:
		cell2PlaceNewNumber = random.choice(emptyCells)
		
		if random.randint(0,1) == 1:
			board[cell2PlaceNewNumber] = 2 ** random.randint(1, MAX_EXPONENT)
		
		return board

if __name__ == "__main__":
    main()