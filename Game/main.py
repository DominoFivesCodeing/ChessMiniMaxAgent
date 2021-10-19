import pygame as pygame
from pygame import display
from ChessGame.constants import LIGHT_SQUARE_COLOR, SCREEN_WIDTH,SCREEN_HEIGHT, SQUARE_SIZE, FONT,WHITE, WHITE_PIECE_IMAGES,BLACK_PIECE_IMAGES
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

            if event.type == pygame.USEREVENT:
                promotionType = promotionMenu(event.turn)
                print(promotionType)
                gameInstance.promotePawn(promotionType)

        gameInstance.update()
    
    pygame.quit()
def promotionMenu(turn):
    images = WHITE_PIECE_IMAGES if turn == WHITE else BLACK_PIECE_IMAGES
    menuWidth,menuHeight = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    menuSurface = pygame.Surface((menuWidth,menuHeight))
    menuSurface.fill((113,154,78))
    options = ["Queen", "Rook", "Bishop", "Knight"]
    optionSize = menuHeight//4
    
    for i in range(len(options)):
        textSurface = FONT.render(options[i], True, (255,254,223))
        imgSurface = pygame.Surface((optionSize,optionSize))
        textRect = textSurface.get_rect()
        textRect.top = optionSize*i
        textRect.left = optionSize
        
        imgRect = imgSurface.get_rect()
        imgRect.left = 0
        imgRect.top = optionSize*i
        menuSurface.blit(textSurface,textRect)
        menuSurface.blit(images.get(options[i]),imgRect)
    menuRect = menuSurface.get_rect()
    menuRect.centerx = SCREEN_WIDTH//2
    menuRect.centery = SCREEN_HEIGHT//2
    WINDOW.blit(menuSurface,menuRect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                print(x,y)
                print(menuWidth, optionSize*4)
                if 200 <= x <= 200+menuWidth and 0 <= y <= 200+optionSize*1:
                    print("Queen")
                    return "Queen"
                if 200 <= x <= 200+menuWidth and 200+optionSize*1 < y <= 200+optionSize*2:
                    print("Rook")
                    return "Rook"
                if 200 <= x <= 200+menuWidth and 200+optionSize*2 <= y <= 200+optionSize*3:
                    print("Bishop")
                    return "Bishop"
                if 200 <= x <= 200+menuWidth and 200+optionSize*3 <= y <= 200+optionSize*4:
                    print("Knight")
                    return "Knight"
                
if __name__ == "__main__":
    gameLoop()