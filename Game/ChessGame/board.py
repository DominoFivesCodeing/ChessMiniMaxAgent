import pygame as pygame
from .constants import LIGHT_SQUARE_COLOR,DARK_SQUARE_COLOR,ROWS,COLS, SCREEN_WIDTH, SQUARE_SIZE,WHITE,BLACK
from .piece import bishopPiece, kingPiece, pawnPiece,knightPiece, queenPiece, rookPiece

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
        if destination != 0 and destination.color != piece.color:
            self.board[row][col] = 0
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.movePiece(row,col)
        print(self)
        self.pieceCount()

    def getValidMovesForPiece(self,piece):
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
        pins = []
        playerKing = self.whiteKing if color == WHITE else self.blackKing
        searchDirections = ((-1,-1),(-1,0), (-1,1), (0,-1),(0,1), (1,-1), (1,0),(1,1))
        knightDir = ((-1,-2),(-1,2),(1,-2),(1,2),(-2,-1),(-2,1),(2,-1),(2,1))
        pinList = []
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
                                pins.append(currentPin)
                                currentPin = None
                            else:
                                checks.append(currentSquare)

                    elif currentSquare.color == color:
                        if currentPin != None:
                            currentPin = None
                            searchDir = False
                        else:
                            currentPin = currentSquare
                            pinList.append(currentPin)
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
            

    
    def __repr__(self) -> str:
        returnStr = ""
        for i in range(ROWS):
            for n in range(1,COLS+1):
                returnStr = returnStr + str(self.board[i][n-1]) + " "
                if n % 8 == 0:
                    returnStr = returnStr + "\n"
        return returnStr