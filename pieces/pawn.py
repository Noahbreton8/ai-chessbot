from .piece import Piece

class Pawn(Piece):
    def doNothing(self):
        print(self.colour)