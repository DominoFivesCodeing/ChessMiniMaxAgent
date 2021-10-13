import pygame as pygame
from pathlib import Path

IMAGE_FOLDER_PATH = Path("ChessGame/Assets")
SCREEN_WIDTH, SCREEN_HEIGHT = 800,800
ROWS, COLS = 8,8
SQUARE_SIZE = SCREEN_WIDTH//COLS

LIGHT_SQUARE_COLOR = (241, 217, 181)
DARK_SQUARE_COLOR = (181, 135, 99)
DOT_COLOR = (255,255,255)


WHITE_PIECE_IMAGES = {"King": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_king.png"), (80,80)), 
                "Queen": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_queen.png"), (80,80)),
                "Rook": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_rook.png"), (80,80)),
                "Knight": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_knight.png"), (80,80)),
                "Bishop": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_bishop.png"), (80,80)),
                "Pawn": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "w_pawn.png"), (80,80))}

BLACK_PIECE_IMAGES = {"King": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_king.png"), (80,80)), 
                "Queen": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_queen.png"), (80,80)),
                "Rook": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_rook.png"), (80,80)),
                "Knight": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_knight.png"), (80,80)),
                "Bishop": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_bishop.png"), (80,80)),
                "Pawn": pygame.transform.scale(pygame.image.load(IMAGE_FOLDER_PATH / "b_pawn.png"), (80,80))}