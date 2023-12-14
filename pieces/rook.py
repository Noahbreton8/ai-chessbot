from .slidingPiece import SlidingPiece

class Rook(SlidingPiece):
    def __init__(self, *args):
        self.hasMoved = False
        super().__init__(*args)