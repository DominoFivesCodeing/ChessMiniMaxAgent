import pygame as pygame
from ChessGame.constants import SCREEN_WIDTH,SCREEN_HEIGHT

WINDOW = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Chess Agent")
FPS = 60

def gameLoop():
    running = True
    
    while running == True:
        clock = pygame.time.Clock()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
    
    pygame.quit()

if __name__ == "__main__":
    gameLoop()