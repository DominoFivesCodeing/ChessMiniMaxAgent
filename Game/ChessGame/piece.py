from .constants import SQUARE_SIZE,WHITE_PIECE_IMAGES,BLACK_PIECE_IMAGES

class Piece:
    def __init__(self, row, col, type, isWhite):
        self.row = row
        self.col = col
        self.type = type
        self.isWhite = isWhite
        self.direction = -1 if isWhite else 1
        self.x = 0
        self.y = 0
        self.image = WHITE_PIECE_IMAGES.get(type) if isWhite else BLACK_PIECE_IMAGES.get(type)
        self.calc_pos()
    
    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col 
        self.y = SQUARE_SIZE * self.row

    def draw(self,window):
        window.blit(self.image,(self.x+10,self.y+10))
    
    def __repr__(self):
        colorStr = "W" if self.isWhite else "B"
        return str(colorStr+ "." + self.type)