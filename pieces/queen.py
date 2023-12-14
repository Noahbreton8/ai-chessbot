from .piece import Piece

class Queen(Piece):
    def getMoves(self, moves, board):
        return moves