import copy
from .constants import BOARD_DIRECTIONS, SQUARE_SIZE,WHITE_PIECE_IMAGES,BLACK_PIECE_IMAGES,WHITE,ROWS,COLS

"""Piece class that all other piece types inherit from"""
class _Piece:
    def __init__(self, row, col, type, color):
        self.row = row
        self.col = col
        self.type = type
        self.color = color
        self.direction = -1 if self.color == WHITE else 1
        self.x = 0
        self.y = 0
        self.calc_pos()

    """Calculate the pixel position of the top left corner for the piece"""
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col 
        self.y = SQUARE_SIZE * self.row

    """Draws the piece onto the window"""
    def draw(self,window):
        img = WHITE_PIECE_IMAGES.get(self.type) if self.color == WHITE else BLACK_PIECE_IMAGES.get(self.type)
        window.blit(img,(self.x+SQUARE_SIZE*0.1,self.y+SQUARE_SIZE*0.1))
    
    """Custom __repr__ that prints the color and type of the piece"""
    def __repr__(self):
        colorStr = "W" if self.color == WHITE else "B"
        return str(colorStr+ "." + self.type)

    """Empty function that all piece types override"""
    def getValidMoves(self, board):
        pass

    """Method for changing the piece's internal values of where it is on the board"""
    def movePiece(self,row,col):
        self.row = row
        self.col = col
        self.calc_pos()

    """Returns a boolean for if the given position is inside the board or not"""
    def moveIsInbounds(self,row,col):
        return row >= 0 and row <= ROWS-1 and col >= 0 and col <= COLS-1
    def getMovesIndirection(self, rowDir,colDir, board):
        newRow = self.row + rowDir
        newCol = self.col + colDir
        movesInDirection = []
        while self.moveIsInbounds(newRow,newCol) and board.getPiece(newRow,newCol) == 0:
            movesInDirection.append((newRow,newCol))
            newRow = newRow + rowDir
            newCol = newCol + colDir
        if self.moveIsInbounds(newRow,newCol) and board.getPiece(newRow,newCol) != 0 and board.getPiece(newRow,newCol).color != self.color:
            movesInDirection.append((newRow,newCol))
        return movesInDirection



"""Class for the pawn piece, is a subclass of piece"""
class pawnPiece(_Piece):
    def __init__(self, row, col, type, color):
        super().__init__(row, col, type, color)
        #Variable used for knowing of the pawn can move two square "forward"
        self.hasMoved = False
        #Variable for if this pawn can be captured with en passant, enemy pawn check for this value
        self.isEnPassantVulnerable = False

    """Extra functionality added for movePiece that makes sure 
       hasMoved and isEnPassantVulnerable have their correct values"""
    def movePiece(self, row, col):
        if  not self.hasMoved and row == self.row+2*self.direction:
            self.isEnPassantVulnerable = True
        else:
            self.isEnPassantVulnerable = False
        self.hasMoved = True
        return super().movePiece(row, col)

    """Returns all valid moves the piece can make, does not check how this effects the rest of the board,
       it only determains that the piece could potentially move their"""
    def getValidMoves(self,board):
        moveList = []
        squaresToCheck = [(self.row + self.direction, self.col),(self.row + 2*self.direction, self.col),(self.row + self.direction, self.col + 1 ), (self.row + self.direction, self.col - 1 ), \
                           (self.row, self.col - 1), (self.row, self.col + 1)]
        for checkSquareForMoveRow,checkSquareForMoveCol  in squaresToCheck:
            if self.moveIsInbounds(checkSquareForMoveRow, checkSquareForMoveCol):
                square = board.getPiece(checkSquareForMoveRow, checkSquareForMoveCol)
                rowDistance = abs(checkSquareForMoveRow-self.row)
                colDistance = abs(checkSquareForMoveCol-self.col)
                if rowDistance == 2 and colDistance == 0 and not self.hasMoved and square == 0 and board.getPiece(checkSquareForMoveRow-self.direction, checkSquareForMoveCol) == 0:
                    moveList.append((checkSquareForMoveRow,checkSquareForMoveCol))
                elif rowDistance == 1:
                    if colDistance == 0 and square == 0:
                        moveList.append((checkSquareForMoveRow,checkSquareForMoveCol))
                    elif colDistance == 1 and square != 0 and square.color != self.color:
                        moveList.append((checkSquareForMoveRow,checkSquareForMoveCol))
                elif rowDistance == 0:
                    square = board.getPiece(checkSquareForMoveRow,checkSquareForMoveCol)
                    square2 = board.getPiece(checkSquareForMoveRow + self.direction,checkSquareForMoveCol)
                    if square != 0 and square.type == "Pawn" and square.color != self.color and square.isEnPassantVulnerable and square2 == 0:
                        moveList.append((square.row + self.direction, square.col))
        return moveList


"""Class for the knight piece, is a subclass of piece"""
class knightPiece(_Piece):
    def __init__(self, row, col, type, color):
        super().__init__(row, col, type, color)

    """Returns all valid moves the piece can make, does not check how this effects the rest of the board,
    it only determains that the piece could potentially move their"""
    def getValidMoves(self, board):
        moveList = []
        for i in range(-2,3):
            for n in range(-2,3):
                if abs(i*n) == 2 and self.moveIsInbounds(self.row + i, self.col + n):
                    square = board.getPiece(self.row + i, self.col + n)
                    if square == 0 or square.color != self.color:
                        moveList.append((self.row + i, self.col + n))
        return moveList

"""Class for the queen piece, is a subclass of piece"""
class queenPiece(_Piece):
    def __init__(self, row, col, type, color):
        super().__init__(row, col, type, color)
    """Returns all valid moves the piece can make, does not check how this effects the rest of the board,
    it only determains that the piece could potentially move their"""
    def getValidMoves(self, board):
        moveList = []
        for dir in BOARD_DIRECTIONS:
            rowDir,colDir = dir
            tempRow = rowDir + self.row
            tempCol = colDir + self.col
            while(self.moveIsInbounds(tempRow,tempCol) and board.getPiece(tempRow,tempCol) == 0):
                moveList.append((tempRow,tempCol))
                tempRow = tempRow + rowDir
                tempCol = tempCol + colDir
            if self.moveIsInbounds(tempRow,tempCol) and board.getPiece(tempRow,tempCol) != 0 and board.getPiece(tempRow,tempCol).color != self.color:
                moveList.append((tempRow,tempCol))
        return moveList

"""Class for the Rook piece, is a subclass of piece"""
class rookPiece(_Piece):
    """Rook contains a attribute for if it has been moved before, used for castling"""
    def __init__(self, row, col, type, color):
        self.hasMoved = False
        super().__init__(row, col, type, color)
        
    """Returns all valid moves the piece can make, does not check how this effects the rest of the board,
    it only determains that the piece could potentially move their"""    
    def getValidMoves(self, board):
        moveList = []
        validDirections = [i for i in BOARD_DIRECTIONS if i[0] == 0 or i[1] == 0]
        for dir in validDirections:
            rowDir,colDir = dir
            tempRow = rowDir + self.row
            tempCol = colDir + self.col
            while(self.moveIsInbounds(tempRow,tempCol) and board.getPiece(tempRow,tempCol) == 0):
                moveList.append((tempRow,tempCol))
                tempRow = tempRow + rowDir
                tempCol = tempCol + colDir
            if self.moveIsInbounds(tempRow,tempCol) and board.getPiece(tempRow,tempCol) != 0 and board.getPiece(tempRow,tempCol).color != self.color:
                moveList.append((tempRow,tempCol))
        return moveList
    
    """Extra functionality added for movePiece that makes sure hasMoved is false if the rook is moves"""
    def movePiece(self, row, col):
        self.hasMoved = True
        return super().movePiece(row, col)

"""Class for the bishop piece, is a subclass of piece"""
class bishopPiece(_Piece):
    def __init__(self, row, col, type, color):
        super().__init__(row, col, type, color)

    """Returns all valid moves the piece can make, does not check how this effects the rest of the board,
    it only determains that the piece could potentially move their"""    
    def getValidMoves(self, board):
        moveList = []
        validDirections = [i for i in BOARD_DIRECTIONS if i[0] != 0 and i[1] != 0]
        for dir in validDirections:
            rowDir,colDir = dir
            tempRow = rowDir + self.row
            tempCol = colDir + self.col
            while(self.moveIsInbounds(tempRow,tempCol) and board.getPiece(tempRow,tempCol) == 0):
                moveList.append((tempRow,tempCol))
                tempRow = tempRow + rowDir
                tempCol = tempCol + colDir
            if self.moveIsInbounds(tempRow,tempCol) and board.getPiece(tempRow,tempCol) != 0 and board.getPiece(tempRow,tempCol).color != self.color:
                moveList.append((tempRow,tempCol))
        return moveList

"""Class for the king piece, is a subclass of piece"""
class kingPiece(_Piece):
    """King contains a attribute for if it has been moved before, used for castling"""
    def __init__(self, row, col, type, color):
        self.hasMoved = False
        super().__init__(row, col, type, color)

    def movePiece(self, row, col):
        self.hasMoved = True
        return super().movePiece(row, col)

    """Returns all valid moves the piece can make, does not check how this effects the rest of the board,
    it only determains that the piece could potentially move their"""    
    def getValidMoves(self, board):
        moveList = []
        for dir in BOARD_DIRECTIONS:
            dirRow,dirCol = dir
            newRow = self.row + dirRow
            newCol = self.col + dirCol
            if self.moveIsInbounds(newRow,newCol) and (board.getPiece(newRow,newCol) == 0 or board.getPiece(newRow,newCol).color != self.color):
                if self.isKingSafeAtSquare(newRow,newCol,board):
                    moveList.append((newRow,newCol))

        if not self.hasMoved:
            moveList = moveList + self.getValidCastling(board)
        return moveList

    """Returns a boolean of weather or not the king will be placed in check by moveing to (row,col).
       Creates a copy of the board and moves the copy of the king on that board and returns the result"""
    def isKingSafeAtSquare(self,row,col,board):
        newBoard = copy.deepcopy(board)
        if self.color == WHITE:
            newBoard.movePiece(newBoard.whiteKing,row,col)
        else:
            newBoard.movePiece(newBoard.blackKing,row,col)
        dirsToCheck = [(dirRow,dirCol) for (dirRow,dirCol) in BOARD_DIRECTIONS if self.moveIsInbounds(row+dirRow,col+dirCol)]
        for dir in dirsToCheck:
            dirRow,dirCol = dir
            squareToCheck = newBoard.getPiece(row + dirRow, col + dirCol)
            if squareToCheck != 0 and squareToCheck.type == "King" and squareToCheck.color != self.color:
                return False
        return len(newBoard.getChecksAndPins(self.color)[0]) == 0

    """Returns a list of all valid castle options, will be 0,1 or 2 elements in the list"""
    def getValidCastling(self,board):
        validCastlingMoves = []
        directions = [-1,1]
        for dir in directions:
            currentCol = self.col + dir
            validateDir = True
            while(validateDir):
                if currentCol == 0 or currentCol == 7:
                    rookSquare = board.getPiece(self.row, currentCol)
                    if rookSquare != 0 and rookSquare.type == "Rook" and rookSquare.color == self.color and not rookSquare.hasMoved:
                        castlingCol = 2 if currentCol == 0 else 6
                        validCastlingMoves.append((self.row,castlingCol))
                        validateDir = False
                if board.getPiece(self.row,currentCol) != 0 or not self.isKingSafeAtSquare(self.row,currentCol,board):
                    validateDir = False
                currentCol = currentCol + dir
        return validCastlingMoves