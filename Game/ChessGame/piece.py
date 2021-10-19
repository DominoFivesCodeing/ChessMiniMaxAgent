import copy
from .constants import SQUARE_SIZE,WHITE_PIECE_IMAGES,BLACK_PIECE_IMAGES,WHITE,BLACK,ROWS,COLS

class _Piece:
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

    def getMovesIndirection(self, rowDir,colDir, board):
        newRow = self.row + rowDir
        newCol = self.col + colDir
        movesInDirection = []
        while self.moveIsInbounds(newRow,newCol) and board.getPiece(newRow,newCol) == 0:
            movesInDirection.append((newRow,newCol))
            newRow = newRow + rowDir
            newCol = newCol + colDir
        if self.moveIsInbounds(newRow,newCol) and board.getPiece(newRow,newCol) != 0 and board.getPiece(newRow,newCol).color != self.color:
            movesInDirection.append((newRow,newCol))
        return movesInDirection

class pawnPiece(_Piece):
    def __init__(self, row, col, type, color):
        super().__init__(row, col, type, color)
        self.firstTurn = True
        self.isEnPassantVulnerable = False

    def movePiece(self, row, col):
        if self.firstTurn and row == self.row+2*self.direction:
            self.isEnPassantVulnerable = True
        else:
            self.isEnPassantVulnerable = False
        self.firstTurn = False
        print(self.isEnPassantVulnerable)
        return super().movePiece(row, col)

    def getValidMoves(self,board):
        moveList = []
        squaresToCheck = [(self.row + self.direction, self.col),(self.row + 2*self.direction, self.col),(self.row + self.direction, self.col + 1 ), (self.row + self.direction, self.col - 1 ), \
                           (self.row, self.col - 1), (self.row, self.col + 1)]
        for checkSquareForMoveRow,checkSquareForMoveCol  in squaresToCheck:
            if self.moveIsInbounds(checkSquareForMoveRow, checkSquareForMoveCol):
                square = board.getPiece(checkSquareForMoveRow, checkSquareForMoveCol)
                rowDistance = abs(checkSquareForMoveRow-self.row)
                colDistance = abs(checkSquareForMoveCol-self.col)
                if rowDistance == 2 and colDistance == 0 and self.firstTurn and square == 0 and board.getPiece(checkSquareForMoveRow-self.direction, checkSquareForMoveCol) == 0:
                    moveList.append((checkSquareForMoveRow,checkSquareForMoveCol))
                elif rowDistance == 1:
                    if colDistance == 0 and square == 0:
                        moveList.append((checkSquareForMoveRow,checkSquareForMoveCol))
                    elif colDistance == 1 and square != 0 and square.color != self.color:
                        moveList.append((checkSquareForMoveRow,checkSquareForMoveCol))
                elif rowDistance == 0:
                    square = board.getPiece(checkSquareForMoveRow,checkSquareForMoveCol)
                    square2 = board.getPiece(checkSquareForMoveRow + self.direction,checkSquareForMoveCol)
                    if square != 0 and square.type == "Pawn" and square.color != self.color and square.isEnPassantVulnerable and square2 == 0:
                        moveList.append((square.row + self.direction, square.col))
        return moveList

class knightPiece(_Piece):
    def __init__(self, row, col, type, color):
        super().__init__(row, col, type, color)
    def getValidMoves(self, board):
        moveList = []
        for i in range(-2,3):
            for n in range(-2,3):
                if abs(i*n) == 2 and self.moveIsInbounds(self.row + i, self.col + n):
                    square = board.getPiece(self.row + i, self.col + n)
                    if square == 0 or square.color != self.color:
                        moveList.append((self.row + i, self.col + n))
        return moveList

class queenPiece(_Piece):
    def __init__(self, row, col, type, color):
        super().__init__(row, col, type, color)
    def getValidMoves(self, board):
        moveList = []
        for i in range(-1,2):
            for n in range(-1,2):
                if not (i == n and i == 0):
                    moveList = moveList + self.getMovesIndirection(i,n,board)
        return moveList

class rookPiece(_Piece):
    def __init__(self, row, col, type, color):
        super().__init__(row, col, type, color)
    
    def getValidMoves(self, board):
        moveList = []
        for i in range(-1,2):
            for n in range(-1,2):
                if i == 0 or n == 0 and i != n:
                    moveList = moveList + self.getMovesIndirection(i,n,board)
        return moveList

class bishopPiece(_Piece):
    def __init__(self, row, col, type, color):
        super().__init__(row, col, type, color)

    def getValidMoves(self, board):
        moveList = []
        for i in range(-1,2):
            for n in range(-1,2):
                if i != 0 and n != 0:
                    moveList = moveList + self.getMovesIndirection(i,n,board)
        return moveList

class kingPiece(_Piece):
    def __init__(self, row, col, type, color):
        super().__init__(row, col, type, color)

    def getValidMoves(self, board):
        moveList = []
        for i in range(-1,2):
            for n in range(-1,2):
                if not (i == n and i == 0):
                    newRow = self.row + i
                    newCol = self.col + n
                    if self.moveIsInbounds(newRow,newCol) and (board.getPiece(newRow,newCol) == 0 or board.getPiece(newRow,newCol).color != self.color):
                        oldRow = copy.deepcopy(self.row)
                        oldCol = copy.deepcopy(self.col)
                        oldDestination = board.getPiece(newRow,newCol)
                        if oldDestination != 0 and oldDestination.color != self.color:
                            board.board[newRow][newCol] = 0
                        board.board[self.row][self.col], board.board[newRow][newCol] = board.board[newRow][newCol], board.board[self.row][self.col]
                        self.row = newRow
                        self.col = newCol
                        if len(board.getChecksAndPins(self.color)[0]) == 0:
                            moveList.append((newRow,newCol))
                        board.board[oldRow][oldCol], board.board[newRow][newCol] = self, oldDestination
                        self.row = oldRow
                        self.col = oldCol
                        self.calc_pos()
        return moveList