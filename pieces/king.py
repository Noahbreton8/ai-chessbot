from .piece import Piece

class King(Piece):
    def doNothing(self):
        print(self.colour)