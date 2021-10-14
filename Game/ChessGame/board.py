import pygame as pygame
from .constants import LIGHT_SQUARE_COLOR,DARK_SQUARE_COLOR,ROWS,COLS, SCREEN_WIDTH, SQUARE_SIZE,WHITE,BLACK
from .piece import Piece, pawnPiece

class Board:
    def __init__(self):
        pygame.init()
        self.board = []
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
            return Piece(row,col,"Rook",color)
        elif col == 1 or col == 6:
            return Piece(row,col,"Knight",color)
        elif col == 2 or col == 5:
            return Piece(row,col,"Bishop",color)
        elif col == 3:
            return Piece(row,col,"Queen",color)
        elif col == 4:
            return Piece(row,col,"King",color)

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

    def __repr__(self) -> str:
        returnStr = ""
        for i in range(ROWS):
            for n in range(1,COLS+1):
                returnStr = returnStr + str(self.board[i][n-1]) + " "
                if n % 8 == 0:
                    returnStr = returnStr + "\n"
        return returnStr