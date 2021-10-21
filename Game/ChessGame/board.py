import pygame as pygame
from .constants import BOARD_DIRECTIONS, FONT, LIGHT_SQUARE_COLOR,DARK_SQUARE_COLOR,ROWS,COLS, SCREEN_WIDTH, SQUARE_SIZE,WHITE,BLACK
from .piece import bishopPiece, kingPiece, pawnPiece,knightPiece, queenPiece, rookPiece
import copy

"""The class for the chess board, holds all methods used to manipulate and draw the board"""
class Board:
    def __init__(self):
        self.board = []
        self.whiteKing = kingPiece(7,4,"King",WHITE)
        self.blackKing = kingPiece(0,4,"King",BLACK)
        self.createInitialBoard()

    """draws the board object using functionality from pygame"""
    def drawBoard(self, window):
        window.fill(LIGHT_SQUARE_COLOR)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, DARK_SQUARE_COLOR,(row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        self.drawPieces(window)
        self.drawText(window,FONT)

    """Helper function for drawBoard that draws all the pieces onto the board"""
    def drawPieces(self,window):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)
        
    """Helper function for drawBoard that draws the letters and numbers used in chess to denote all squares"""
    def drawText(self,window,font):
        for row in range(ROWS):
            color = LIGHT_SQUARE_COLOR if row % 2 == 0 else DARK_SQUARE_COLOR
            text = font.render(str(8-row), True, color)
            window.blit(text, (0,row*SQUARE_SIZE))
        for col in range(COLS):
            color = DARK_SQUARE_COLOR if col % 2 == 0 else LIGHT_SQUARE_COLOR
            #chr(65) is the ASCII value for "A"
            text = font.render(chr(65+col), True, color)
            window.blit(text, (col*SQUARE_SIZE+SQUARE_SIZE*0.85,SCREEN_WIDTH*(COLS-1)//COLS + SQUARE_SIZE*0.85))

    """Function for filling the self.board variable and placeing the pieces on their correct positions at the start of the game"""
    def createInitialBoard(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row < 2:
                    self.board[row].append(self.getInitialPieceType(row,col,BLACK))
                elif row > 5:
                    self.board[row].append(self.getInitialPieceType(row,col,WHITE))
                else:
                    self.board[row].append(0)

    """Helper function for createInitialBoard that return the appropriate piece object"""
    def getInitialPieceType(self, row, col,color):
        if row == 1 or row == 6:
            return pawnPiece(row,col,"Pawn",color)
        if col == 0 or col == 7:
            return rookPiece(row,col,"Rook",color)
        elif col == 1 or col == 6:
            return knightPiece(row,col,"Knight",color)
        elif col == 2 or col == 5:
            return bishopPiece(row,col,"Bishop",color)
        elif col == 3:
            return queenPiece(row,col,"Queen",color)
        elif col == 4:
            king = self.whiteKing if color == WHITE else self.blackKing
            return king

    """returns the object at board[row][col]"""
    def getPiece(self,row, col):
        return self.board[row][col]

    """Takes in "color" that is either WHITE or BLACK and returns a list of all pieces that has the desired color."""
    def getAllPiecesOfColor(self,color):
        pieceList = []
        for row in self.board:
            for col in row:
                if col != 0 and col.color == color:
                    pieceList.append(col)
        return pieceList

    """Takes in a piece object, two ints for the row and col that
       the piece should be moved to"""
    def movePiece(self,piece,row,col):
        destination = self.getPiece(row,col)
        if piece.type == "King" and self.isKingMoveCastling(piece,row,col):
            rookCol = 0 if col == 2 else 7
            rookSide = 1 if col == 2 else -1
            self.board[row][rookCol], self.board[row][col+rookSide] = self.board[row][col+rookSide], self.board[row][rookCol]
            self.board[row][col+rookSide].movePiece(row,col+rookSide)
        elif piece.type == "Pawn" and self.isPawnMoveEnPassant(piece,row,col):
            self.board[row-piece.direction][col] = 0
        if destination != 0 and destination.color != piece.color:
            self.board[row][col] = 0
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.movePiece(row,col)

    """Helper function for movePiece that returns wather or not a pawn move is en passant"""
    def isPawnMoveEnPassant(self,piece,row,col):
        isPieceMoveCorrect = piece.row + piece.direction == row and abs(piece.col - col) == 1
        takenPawnSquare = self.board[row-piece.direction][col]
        isTakenPawnValid = takenPawnSquare != 0 and takenPawnSquare.type == "Pawn" and takenPawnSquare.color != piece.color and takenPawnSquare.isEnPassantVulnerable
        return isPieceMoveCorrect and isTakenPawnValid

    """Helper function for movePiece that returns wather or not a king move is castling"""
    def isKingMoveCastling(self,piece,row,col):
        return piece.row == row and (col == 2 or col == 6) and not piece.hasMoved

    """Takes in a piece and returns a list containing all valid moves for it"""
    def getValidMovesForPiece(self,piece):
        checks,pins = self.getChecksAndPins(piece.color)
        playerKing = self.whiteKing if piece.color == WHITE else self.blackKing
        if len(checks) > 0:
            if piece.type == "King":
                return piece.getValidMoves(self)
            if len(checks) == 1:
                checkingPiece = checks[0]
                pieceMoves = piece.getValidMoves(self)
                if checkingPiece.type == "Knight":
                    return [(checkingPiece.row, checkingPiece.col)] if ((checkingPiece.row, checkingPiece.col)) in pieceMoves else []
                rowDIr = (checkingPiece.row - playerKing.row)//abs(checkingPiece.row - playerKing.row) if checkingPiece.row - playerKing.row != 0 else 0
                colDir = (checkingPiece.col - playerKing.col)//abs(checkingPiece.col - playerKing.col) if checkingPiece.col - playerKing.col != 0 else 0
                tempRow = playerKing.row + rowDIr
                tempCol = playerKing.col + colDir
                legalMoves = []
                while(tempRow != checkingPiece.row or tempCol != checkingPiece.col):
                    if (tempRow,tempCol) in pieceMoves:
                        legalMoves.append((tempRow,tempCol))
                    tempRow = tempRow + rowDIr
                    tempCol = tempCol + colDir
                if (checkingPiece.row, checkingPiece.col) in pieceMoves:
                    legalMoves.append((checkingPiece.row, checkingPiece.col))
                return legalMoves
            return []

        if piece in pins.keys():
            pinningPiece = pins.get(piece)
            pieceMoves = piece.getValidMoves(self)
            rowDIr = (pinningPiece.row - piece.row)//abs(pinningPiece.row - piece.row) if pinningPiece.row - piece.row != 0 else 0
            colDir = (pinningPiece.col - piece.col)//abs(pinningPiece.col - piece.col) if pinningPiece.col - piece.col != 0 else 0
            tempRow = playerKing.row + rowDIr
            tempCol = playerKing.col + colDir
            legalMoves = []
            while(tempRow != pinningPiece.row or tempCol != pinningPiece.col):
                if (tempRow,tempCol) in pieceMoves:
                    legalMoves.append((tempRow,tempCol))
                tempRow = tempRow + rowDIr
                tempCol = tempCol + colDir
            if (pinningPiece.row, pinningPiece.col) in pieceMoves:
                    legalMoves.append((pinningPiece.row, pinningPiece.col))
            return legalMoves

        return piece.getValidMoves(self)

    """Returns two lists, one containing all pieces that checks color's king and one of containing color's pins. Takes in "color" that is either WHITE or BLACK
    pins are peices that protect the king from an attack and moveing them would result in the king being attacked (unless the pin takes the attacking piece)"""
    def getChecksAndPins(self,color):
        checks = []
        pins = {}
        playerKing = self.whiteKing if color == WHITE else self.blackKing
        for dir in BOARD_DIRECTIONS:
            row,col = dir
            tempRow,tempCol = playerKing.row + row, playerKing.col + col
            searchDir = True
            currentPin = None
            #Check in all directions for pins and checks
            while(searchDir and 0 <= tempRow <= 7 and 0 <= tempCol <= 7):
                currentSquare = self.board[tempRow][tempCol]
                threats = ["Rook","Queen"] if (row == 0 or col == 0) else ["Bishop", "Queen", "Pawn"]
                if currentSquare != 0:
                    if currentSquare.color != color:
                        if currentSquare.type in threats and not (currentSquare.type == "Pawn" and currentSquare.row != playerKing.row + playerKing.direction and abs(currentSquare.col - playerKing.col) != 1):
                            if currentPin != None:
                                pins[currentPin] = currentSquare
                                currentPin = None
                            else:
                                checks.append(currentSquare)
                        searchDir = False

                    elif currentSquare.color == color:
                        if currentPin != None:
                            currentPin = None
                            searchDir = False
                        else:
                            currentPin = currentSquare
                tempRow = tempRow + row
                tempCol = tempCol + col
        #Since knights can jump over pieces they cannot be pinned and require their own logic to find
        knightPos = ((-1,-2),(-1,2),(1,-2),(1,2),(-2,-1),(-2,1),(2,-1),(2,1))
        for dir in knightPos:
            row,col = dir
            newRow,newCol = playerKing.row + row,playerKing.col + col
            if 0 <= newRow <= 7 and 0 <= newCol <= 7 and self.board[newRow][newCol] != 0:
                piece = self.board[newRow][newCol]
                if piece.color != color and piece.type == "Knight":
                    checks.append(piece)
        return checks,pins

    """Takes in "color" that is either WHITE or BLACK and returns the current "ending state" of the game.
            if the game should not end than 0 will be returned
            if the game should end now in a checkmate, 1 will be returned
            if the game should end not in a stalemate, 2 will be returned"""
    def getGameStatus(self,color):
        checks = self.getChecksAndPins(color)[0]
        playersPieces = self.getAllPiecesOfColor(color)
        for piece in playersPieces:
            if piece.color == color and len(self.getValidMovesForPiece(piece)) > 0:
                return 0
        if len(checks) > 0:
            return 1
        return 2
                    
    """Takes in a piece object that is supposed to be a pawn and a string of what piece 
       the pawn will be promoted to. Replaces the pawn with the desired promotionType."""
    def pawnPromotion(self,piece,promotionType):
        assert piece.type == "Pawn" and (piece.row == 0 or piece.row == 7)
        newPiece = None
        if promotionType == "Queen":
            newPiece = queenPiece(piece.row,piece.col,promotionType,piece.color)
        elif promotionType == "Rook":
            newPiece = rookPiece(piece.row,piece.col,promotionType, piece.color)
        elif promotionType == "Bishop":
            newPiece = bishopPiece(piece.row,piece.col,promotionType,piece.color)
        elif promotionType == "Knight":
            newPiece = knightPiece(piece.row,piece.col,promotionType,piece.color)
        else:
            newPiece = queenPiece(piece.row,piece.col,promotionType,piece.color)

        self.board[piece.row][piece.col] = newPiece
        del piece
    
    """Custom __repr__ that returns a string showing where all pieces are on the board"""
    def __repr__(self) -> str:
        returnStr = "\n"
        for row in self.board:
            for col in row:
                if col == 0:
                    returnStr = returnStr + "Empty     "
                else:
                    pieceColor = "W." if col.color == WHITE else "B."
                    newStringPortion = pieceColor + col.type + " "
                    while len(newStringPortion) <= 9:
                        newStringPortion = newStringPortion + " " 
                    returnStr = returnStr + newStringPortion

            returnStr = returnStr + "\n"
        return returnStr

    """Evaluation function used by the AI"""
    def evaluteBoard(self):
        if self.getGameStatus(WHITE) == 1:
            return -1000
        if self.getGameStatus(BLACK) == 1:
            return 10000

        whitePieces = self.getAllPiecesOfColor(WHITE)
        blackPieces = self.getAllPiecesOfColor(BLACK)
        whiteTotalValue = 0
        blackTotalValue = 0
        for i in whitePieces:
            if i.type == "Pawn":
                whiteTotalValue = whiteTotalValue + 1
            elif i.type == "Knight":
                whiteTotalValue = whiteTotalValue + 3
            elif i.type == "Bishop":
                whiteTotalValue = whiteTotalValue + 3
            elif i.type == "Rook":
                whiteTotalValue = whiteTotalValue + 5
            elif i.type == "Queen":
                whiteTotalValue = whiteTotalValue + 9
        for i in blackPieces:
            if i.type == "Pawn":
                blackTotalValue = blackTotalValue + 1
            elif i.type == "Knight":
                blackTotalValue = blackTotalValue + 3
            elif i.type == "Bishop":
                blackTotalValue = blackTotalValue + 3
            elif i.type == "Rook":
                blackTotalValue = blackTotalValue + 5
            elif i.type == "Queen":
                blackTotalValue = blackTotalValue + 9
        return whiteTotalValue - blackTotalValue