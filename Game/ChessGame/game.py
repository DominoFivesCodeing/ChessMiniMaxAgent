import pygame

from .board import Board
from .constants import ROWS, SQUARE_SIZE, WHITE,BLACK,DOT_COLOR, COLS

"""Class for the game object, it is a package that both the player and the AI calls to change the game state"""
class Game:

    def __init__(self,window):
        self._init()
        self.window = window

    """Changes the board, selected, turn and validMoves to their appropriate values for a new game"""
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.validMoves = []

    """Resets the game by calling self._init()"""
    def reset(self):
        self._init()

    """Updates the visuals for the game"""
    def update(self):
        self.board.drawBoard(self.window)
        self.drawValidMoves(self.validMoves)
        pygame.display.update()


    """Selection handling of pieces"""
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

    """Private method for moveing a piece"""
    def _move(self,row,col):
        if self.selected and (row,col) in self.validMoves:
            self.board.movePiece(self.selected,row,col)
            if self.selected != 0 and self.selected.type == "Pawn" and (row == 0 or row == 7):
                pygame.event.post(pygame.event.Event(pygame.USEREVENT, {'turn': self.turn}))
            self.changeTurn()
        else:
            return False
        return True

    """Changes turn"""
    def changeTurn(self):
        self.validMoves = []
        if self.turn == WHITE:
            self.turn = BLACK
        else:
            self.turn = WHITE
        gameStatus = self.board.getGameStatus(self.turn)
        if gameStatus == 0:
            print("Game is not over")
        elif gameStatus == 1:
            print("CHECKMATE")
        else:
            print("STALEMATE")

    """Promotes pawn"""
    def promotePawn(self, promotionType):
        self.board.pawnPromotion(self.selected, promotionType)
    
    """Draws where the player can move their slected piece"""
    def drawValidMoves(self, moves):
        for move in moves:
            row,col = move
            pygame.draw.circle(self.window,DOT_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), SQUARE_SIZE*0.1)

    """Getter for board"""
    def getBoard(self):
        return self.board

    """Changes the board when the AI makes a move"""
    def moveAI(self,board):
        self.board = board
        self.changeTurn()