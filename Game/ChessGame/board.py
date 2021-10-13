import pygame as pygame
from .constants import LIGHT_SQUARE_COLOR,DARK_SQUARE_COLOR,ROWS,COLS, SQUARE_SIZE
from .piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.selectedPiece = None
        self.createBoard()
        #Add inital pieces latter

    def drawBoard(self, window):
        window.fill(LIGHT_SQUARE_COLOR)
        for row in range(ROWS):
            for col in range(row % 2, ROWS, 2):
                pygame.draw.rect(window, DARK_SQUARE_COLOR,(row * SQUARE_SIZE, col * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        self.drawPieces(window)

    def drawPieces(self,window):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(window)
        

    def createBoard(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row < 2:
                    self.board[row].append(Piece(row,col,self.getInitialPieceType(row,col),False))
                elif row > 5:
                    self.board[row].append(Piece(row,col,self.getInitialPieceType(row,col),True))
                else:
                    self.board[row].append(0)

    def getInitialPieceType(self, row, col):
        if row == 1 or row == 6:
            return "Pawn"
        if col == 0 or col == 7:
            return "Rook"
        elif col == 1 or col == 6:
            return "Knight"
        elif col == 2 or col == 5:
            return "Bishop"
        elif col == 3:
            return "Queen"
        elif col == 4:
            return "King"

    def __repr__(self) -> str:
        returnStr = ""
        for i in range(ROWS):
            for n in range(COLS):
                returnStr = returnStr + str(self.board[i][n]) + " "
                if n % 8 == 0:
                    returnStr = returnStr + "\n"
        return returnStr