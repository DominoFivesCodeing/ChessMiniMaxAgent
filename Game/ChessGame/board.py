import pygame as pygame
from .constants import LIGHT_SQUARE_COLOR,DARK_SQUARE_COLOR,ROWS,COLS, SCREEN_WIDTH, SQUARE_SIZE,WHITE,BLACK
from .piece import bishopPiece, kingPiece, pawnPiece,knightPiece, queenPiece, rookPiece
import copy

class Board:
    def __init__(self):
        pygame.init()
        self.board = []
        self.whiteKing = kingPiece(7,4,"King",WHITE)
        self.blackKing = kingPiece(0,4,"King",BLACK)
        self.createBoard()
        self.textFont = pygame.font.SysFont(None, SCREEN_WIDTH//32)

        #Add inital pieces latter

    def drawBoard(self, window):
        window.fill(LIGHT_SQUARE_COLOR)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, DARK_SQUARE_COLOR,(row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        self.drawPieces(window)
        self.drawText(window,self.textFont)

    def drawPieces(self,window):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)
        
    def drawText(self,window,font):
        for row in range(ROWS):
            color = LIGHT_SQUARE_COLOR if row % 2 == 0 else DARK_SQUARE_COLOR
            text = font.render(str(8-row), True, color)
            window.blit(text, (0,row*SQUARE_SIZE))
        for col in range(COLS):
            color = DARK_SQUARE_COLOR if col % 2 == 0 else LIGHT_SQUARE_COLOR
            text = font.render(chr(65+col), True, color)
            window.blit(text, (col*SQUARE_SIZE+SQUARE_SIZE*0.85,SCREEN_WIDTH*(COLS-1)//COLS + SQUARE_SIZE*0.85))

    def createBoard(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row < 2:
                    self.board[row].append(self.getInitialPieceType(row,col,BLACK))
                elif row > 5:
                    self.board[row].append(self.getInitialPieceType(row,col,WHITE))
                else:
                    self.board[row].append(0)

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

    def getPiece(self,row, col):
        return self.board[row][col]

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
        self.pieceCount()

    def isPawnMoveEnPassant(self,piece,row,col):
        isPieceMoveCorrect = piece.row + piece.direction == row and abs(piece.col - col) == 1
        takenPawnSquare = self.board[row-piece.direction][col]
        isTakenPawnValid = takenPawnSquare != 0 and takenPawnSquare.type == "Pawn" and takenPawnSquare.color != piece.color and takenPawnSquare.isEnPassantVulnerable
        return isPieceMoveCorrect and isTakenPawnValid

    def isKingMoveCastling(self,piece,row,col):
        return piece.row == row and (col == 2 or col == 6) and not piece.hasMoved

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

    def pieceCount(self):
        counter = 0
        for i in range(ROWS):
            for n in range(COLS):
                if self.board[i][n] != 0:
                    counter = counter + 1
        print(counter)

    def getChecksAndPins(self,color):
        checks = []
        pins = {}
        playerKing = self.whiteKing if color == WHITE else self.blackKing
        searchDirections = ((-1,-1),(-1,0), (-1,1), (0,-1),(0,1), (1,-1), (1,0),(1,1))
        knightDir = ((-1,-2),(-1,2),(1,-2),(1,2),(-2,-1),(-2,1),(2,-1),(2,1))
        for dir in searchDirections:
            row,col = dir
            tempRow,tempCol = playerKing.row + row, playerKing.col + col
            searchDir = True
            currentPin = None
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

        for dir in knightDir:
            row,col = dir
            newRow,newCol = playerKing.row + row,playerKing.col + col
            if 0 <= newRow <= 7 and 0 <= newCol <= 7 and self.board[newRow][newCol] != 0:
                piece = self.board[newRow][newCol]
                if piece.color != color and piece.type == "Knight":
                    checks.append(piece)
        return checks,pins

    def isCheckMateOrStaleMate(self,color):
        checks = self.getChecksAndPins(color)[0]
        for row in self.board:
            for square in row:
                if square != 0 and square.color == color and len(self.getValidMovesForPiece(square)) > 0:
                    return None
        if len(checks) > 0:
            return "Checkmate"
        return "Stalemate"
                    

                    

            

    
    def __repr__(self) -> str:
        returnStr = ""
        for i in range(ROWS):
            for n in range(1,COLS+1):
                returnStr = returnStr + str(self.board[i][n-1]) + " "
                if n % 8 == 0:
                    returnStr = returnStr + "\n"
        return returnStr