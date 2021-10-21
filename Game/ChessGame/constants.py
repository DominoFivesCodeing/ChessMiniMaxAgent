import pygame as pygame
from pathlib import Path

IMAGE_FOLDER_PATH = Path("ChessGame/Assets")
SCREEN_WIDTH, SCREEN_HEIGHT = 800,800
ROWS, COLS = 8,8
SQUARE_SIZE = SCREEN_WIDTH//COLS
SPRITE_SIZE = SQUARE_SIZE*0.8
BOARD_DIRECTIONS = ((-1,-1),(-1,0), (-1,1), (0,-1),(0,1), (1,-1), (1,0),(1,1))

LIGHT_SQUARE_COLOR = (241, 217, 181)
DARK_SQUARE_COLOR = (181, 135, 99)
DOT_COLOR = (255,255,255)
WHITE,BLACK = "WHITE", "BLACK"
pygame.init()
FONT = pygame.font.SysFont(None, SCREEN_WIDTH//32)


WHITE_PIECE_IMAGES = {"King": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_king.png"), (SPRITE_SIZE,SPRITE_SIZE)), 
                "Queen": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_queen.png"), (SPRITE_SIZE,SPRITE_SIZE)),
                "Rook": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_rook.png"), (SPRITE_SIZE,SPRITE_SIZE)),
                "Knight": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_knight.png"), (SPRITE_SIZE,SPRITE_SIZE)),
                "Bishop": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_bishop.png"), (SPRITE_SIZE,SPRITE_SIZE)),
                "Pawn": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_pawn.png"), (SPRITE_SIZE,SPRITE_SIZE))}

BLACK_PIECE_IMAGES = {"King": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_king.png"), (SPRITE_SIZE,SPRITE_SIZE)), 
                "Queen": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_queen.png"), (SPRITE_SIZE,SPRITE_SIZE)),
                "Rook": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_rook.png"), (SPRITE_SIZE,SPRITE_SIZE)),
                "Knight": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_knight.png"), (SPRITE_SIZE,SPRITE_SIZE)),
                "Bishop": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_bishop.png"), (SPRITE_SIZE,SPRITE_SIZE)),
                "Pawn": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_pawn.png"), (SPRITE_SIZE,SPRITE_SIZE))}