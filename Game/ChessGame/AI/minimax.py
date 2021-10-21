import copy
from ..constants import WHITE,BLACK
import sys

def minimax(state, depth, isMaxPlayer, alpha = float("-inf"),beta = float("inf")):
    if depth == 0:
        return state.evaluteBoard(), state

    if isMaxPlayer:
        maxEval = float('-inf')
        bestMove = None
        for board in getAllBoards(state,WHITE):
            evalution = minimax(board,depth-1,False,alpha,beta)[0]
            maxEval = max(maxEval,evalution)
            if maxEval == evalution:
                bestMove = board
            alpha = max(alpha,evalution)
            if beta <= alpha:
                break
        return maxEval, bestMove
    else:
        miniEval = float('inf')
        bestMove = None
        for board in getAllBoards(state,BLACK):
            evalution = minimax(board,depth-1,True,alpha,beta)[0]
            miniEval = min(miniEval,evalution)
            if miniEval == evalution:
                bestMove = board
            beta = min(beta,evalution)
            if beta <= alpha:
                break
        return miniEval, bestMove

def getAllBoards(board,color):
    pieces = board.getAllPiecesOfColor(color)
    newBoards = []
    for piece in pieces:
        validMoves = board.getValidMovesForPiece(piece)
        for move in validMoves:
            tempBoard = copy.deepcopy(board)
            tempPiece = tempBoard.getPiece(piece.row,piece.col)
            row,col = move
            tempBoard.movePiece(tempPiece,row,col)
            newBoards.append(tempBoard)
    return newBoards