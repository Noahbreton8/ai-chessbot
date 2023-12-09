from .piece import Piece

class Bishop(Piece):
    def doNothing(self):
        print(self.colour)