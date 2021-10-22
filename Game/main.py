import pygame as pygame
from ChessGame.constants import BLACK, SCREEN_WIDTH,SCREEN_HEIGHT, SQUARE_SIZE, FONT,WHITE, WHITE_PIECE_IMAGES,BLACK_PIECE_IMAGES
from ChessGame.game import Game
from ChessGame.AI.minimax import minimax
import time

WINDOW = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Chess Agent")
FPS = 60

"""Converts the cordinates of the mouse to row and col values used in the game"""
def getRowColOfMouse(pos):
    x,y = pos
    row, col = (y//SQUARE_SIZE, x//SQUARE_SIZE)
    return row,col

"""Main game loop"""
def gameLoop():
    running = True
    gameInstance = Game(WINDOW)
    playerColor = WHITE
    AiColor = BLACK
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(FPS)
        if gameInstance.turn == AiColor:
            startTime = time.time()
            value,newBoard = minimax(gameInstance.getBoard(), 3,False)
            print("--- %s seconds ---" % (time.time() - startTime))
            gameInstance.moveAI(newBoard)
            pass
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                row,col = getRowColOfMouse(pygame.mouse.get_pos())
                gameInstance.selectPiece(row,col)

            if event.type == pygame.USEREVENT:
                promotionType = promotionMenu(event.turn)
                gameInstance.promotePawn(promotionType)
        gameInstance.update()
    
    pygame.quit()

"""Creates a menu for choosing what piece to promote to when a promotion event is received"""
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
        menuRelativPos = SCREEN_WIDTH//4
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = pygame.mouse.get_pos()
                if menuRelativPos <= x <= menuRelativPos+menuWidth and 0 <= y <= menuRelativPos+optionSize*1:
                    return "Queen"
                if menuRelativPos <= x <= menuRelativPos+menuWidth and menuRelativPos+optionSize*1 < y <= menuRelativPos+optionSize*2:
                    return "Rook"
                if menuRelativPos <= x <= menuRelativPos+menuWidth and menuRelativPos+optionSize*2 <= y <= menuRelativPos+optionSize*3:
                    return "Bishop"
                if menuRelativPos <= x <= menuRelativPos+menuWidth and menuRelativPos+optionSize*3 <= y <= menuRelativPos+optionSize*4:
                    return "Knight"
                
if __name__ == "__main__":
    gameLoop()