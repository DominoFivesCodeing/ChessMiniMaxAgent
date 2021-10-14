import pygame

from ChessGame.piece import Piece
from .board import Board
from .constants import SQUARE_SIZE, WHITE,BLACK,DOT_COLOR

class Game:
    def __init__(self,window):
        self._init()
        self.window = window

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.validMoves = []

    def reset(self):
        self._init()

    def update(self):
        self.board.drawBoard(self.window)
        self.drawValidMoves(self.validMoves)
        pygame.display.update()

    def selectPiece(self,row,col):
        if self.selected:
            moveStatus = self._move(row,col)
            if not moveStatus:
                self.validMoves = []
                self.selected = None
                self.selectPiece(row,col)

        selectedPiece = self.board.getPiece(row,col)
        if selectedPiece != 0 and selectedPiece.color == self.turn:
            self.selected = selectedPiece
            self.validMoves = self.board.getValidMovesForPiece(selectedPiece)
            return True
        return False

    def _move(self,row,col):
        if self.selected and (row,col) in self.validMoves:
            self.board.movePiece(self.selected,row,col)
            self.changeTurn()
        else:
            return False
        return True

    def changeTurn(self):
        self.validMoves = []
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
    
    def drawValidMoves(self, moves):
        for move in moves:
            row,col = move
            pygame.draw.circle(self.window,DOT_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), SQUARE_SIZE*0.1)