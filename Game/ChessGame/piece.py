from .constants import SQUARE_SIZE,WHITE_PIECE_IMAGES,BLACK_PIECE_IMAGES,WHITE,BLACK,ROWS,COLS

class Piece:
    def __init__(self, row, col, type, color):
        self.row = row
        self.col = col
        self.type = type
        self.color = color
        self.direction = -1 if self.color == WHITE else 1
        self.x = 0
        self.y = 0
        self.image = WHITE_PIECE_IMAGES.get(type) if self.color == WHITE else BLACK_PIECE_IMAGES.get(type)
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col 
        self.y = SQUARE_SIZE * self.row

    def draw(self,window):
        window.blit(self.image,(self.x+SQUARE_SIZE*0.1,self.y+SQUARE_SIZE*0.1))
    
    def __repr__(self):
        colorStr = "W" if self.color == WHITE else "B"
        return str(colorStr+ "." + self.type)

    def getValidMoves(self, board):
        pass

    def movePiece(self,row,col):
        self.row = row
        self.col = col
        self.calc_pos()

    def moveIsInbounds(self,row,col):
        return row >= 0 and row <= ROWS-1 and col >= 0 and col <= COLS-1

class pawnPiece(Piece):
    def __init__(self, row, col, type, color):
        super().__init__(row, col, type, color)
        self.firstTurn = True

    def movePiece(self, row, col):
        self.firstTurn = False
        return super().movePiece(row, col)

    def getValidMoves(self,board):
        moveList = []
        squaresToCheck = [(self.row + self.direction, self.col),(self.row + 2*self.direction, self.col),(self.row + self.direction, self.col + 1 ), (self.row + self.direction, self.col - 1 )]
        for checkSquareForMoveRow,checkSquareForMoveCol  in squaresToCheck:
            if self.moveIsInbounds(checkSquareForMoveRow, checkSquareForMoveCol):
                square = board.getPiece(checkSquareForMoveRow, checkSquareForMoveCol)
                rowDistance = abs(checkSquareForMoveRow-self.row)
                colDistance = abs(checkSquareForMoveCol-self.col)
                if rowDistance == 2 and colDistance == 0 and self.firstTurn and square == 0 and board.getPiece(checkSquareForMoveRow-self.direction, checkSquareForMoveCol) == 0:
                    moveList.append((checkSquareForMoveRow,checkSquareForMoveCol))
                if rowDistance == 1:
                    if colDistance == 0 and square == 0:
                        moveList.append((checkSquareForMoveRow,checkSquareForMoveCol))
                    elif colDistance == 1 and square != 0 and square.color != self.color:
                        moveList.append((checkSquareForMoveRow,checkSquareForMoveCol))
        return moveList
