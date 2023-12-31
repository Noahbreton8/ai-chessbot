from .piece import Piece

class SlidingPiece(Piece):

    def __init__(self, *args):
          #                   up   down   left     right    upleft  downright upright downleft
        self.directions = [(-1,0), (1,0), (0, -1), (0, 1), (-1,-1), (1, 1), (-1, 1), (1, -1)]
        self.numSquaresToEdge = [[None for _ in range(8)] for _ in range(8)]
        self.precomputerMoveData()
        super().__init__(*args)

    def getMoves(self, moves, board, pins):
        from ChessEngine import Move
        from .bishop import Bishop
        from .rook import Rook

        piecePinned = False
        pinDirection = ()
        for i in range(len(pins)-1,-1,-1):
            if pins[i][0] == self.row and pins[i][1] == self.col:   
                piecePinned = True
                pinDirection = (pins[i][2], pins[i][3])
                pins.remove(pins[i])
                break

        start = 4 if isinstance(self, Bishop) else 0
        end = 4 if isinstance(self, Rook) else 8

        for directionIndex in range(start, end):
            for moveFactor in range(1, self.numSquaresToEdge[self.row][self.col][directionIndex]+1):
                direction = self.directions[directionIndex]
                if not piecePinned or pinDirection == direction or pinDirection == (-direction[0], -direction[1]):
                    #moveFactor is the how far, self.directions[directionIndex] is one of the 8 tuples
                    #example: A bishop going 3 squares up and left starting at (4, 4):
                    #           result = 3 * (-1, -1) = (-3, -3)
                    #           newRow = -3+4 = 1
                    #           newCol = -3+4 = 1
                    #           Bishop ends at index (1,1)

                    #pretty much a vector to where the piece will go
                    result = tuple(factor * moveFactor for factor in direction)

                    #using vector to move to new row and column
                    newRow, newCol = result[0] + self.row, result[1] + self.col
                    targetSquare = board[newRow][newCol]

                    #if same team on square then can't move to or past
                    if targetSquare and targetSquare.colour == self.colour:
                        break

                    moves.append(Move((self.row, self.col), (newRow, newCol), board))

                    #if opposing team on sqaure can capture but cannot move past
                    if targetSquare and targetSquare.colour != self.colour:
                        break
        
        return moves, pins


    def precomputerMoveData(self):
        for file in range(8):
            for rank in range(8):
                numUp = rank
                numDown = 7-rank
                numRight = 7-file
                numLeft = file

                self.numSquaresToEdge[rank][file] = [numUp, numDown, numLeft, numRight, min(numUp, numLeft), min(numDown, numRight), min(numUp, numRight), min(numDown, numLeft)]

# (1,0) down
# (-1, 0) up
# (0,1) right
# (0, -1) left
# (1, 1) down right
# (1, -1) down left
# (-1, 1) up right
# (-1, -1) up left