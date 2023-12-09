from .piece import Piece

class Queen(Piece):
    def doNothing(self):
        print(self.colour)