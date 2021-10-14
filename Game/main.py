import pygame as pygame
from ChessGame.constants import SCREEN_WIDTH,SCREEN_HEIGHT, SQUARE_SIZE
from ChessGame.board import Board
from ChessGame.game import Game

WINDOW = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Chess Agent")
FPS = 60

def getRowColOfMouse(pos):
    x,y = pos
    row, col = (y//SQUARE_SIZE, x//SQUARE_SIZE)
    return row,col

def gameLoop():
    running = True
    gameInstance = Game(WINDOW)
    print(gameInstance.board)
    
    while running == True:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                row,col = getRowColOfMouse(pygame.mouse.get_pos())
                gameInstance.selectPiece(row,col)
                #piece = board.getPiece(row,col)
                #board.movePiece(piece,4,5)
                #board.setSelectedPiece(mouseY,mouseX)
                pass

        gameInstance.update()
    
    pygame.quit()

if __name__ == "__main__":
    gameLoop()