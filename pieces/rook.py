from .piece import Piece

class Rook(Piece):
    def __init__(self, *args):
        self.hasMoved = False
        super().__init__(*args)
    
    def getMoves(self, moves, board):
        return moves