import pygame

from .board import Board
from .constants import SQUARE_SIZE, WHITE,BLACK,DOT_COLOR,FONT


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
        return False

    def _move(self,row,col):
        if self.selected and (row,col) in self.validMoves:
            self.board.movePiece(self.selected,row,col)
            if self.selected != 0 and self.selected.type == "Pawn" and (row == 0 or row == 7):
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'turn': self.turn}))
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
        #print(self.board.isCheckMateOrStaleMate(self.turn))

    def promotePawn(self, promotionType):
        self.board.pawnPromotion(self.selected, promotionType)
    
    def drawValidMoves(self, moves):
        for move in moves:
            row,col = move
            pygame.draw.circle(self.window,DOT_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), SQUARE_SIZE*0.1)