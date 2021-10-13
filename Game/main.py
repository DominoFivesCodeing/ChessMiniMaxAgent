import pygame as pygame
from ChessGame.constants import SCREEN_WIDTH,SCREEN_HEIGHT
from ChessGame.board import Board

WINDOW = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Chess Agent")
FPS = 60

def gameLoop():
    running = True
    board = Board()
    print(board)
    
    while running == True:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass

        board.drawBoard(WINDOW)
        pygame.display.update()
    
    pygame.quit()

if __name__ == "__main__":
    gameLoop()