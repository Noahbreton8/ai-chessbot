from .piece import Piece

class Rook(Piece):
    def doNothing(self):
        print(self.colour)