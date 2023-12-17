from .piece import Piece

class King(Piece):
    def __init__(self, *args):
        self.directions = [(-1,0), (1,0), (0, -1), (0, 1), (-1,-1), (1, 1), (-1, 1), (1, -1)]
        self.hasMoved = False
        super().__init__(*args)

    def getMoves(self, moves, board):
        from ChessEngine import Move
        r, c = self.row, self.col
        for tup in self.directions:
            rowChange, colChange = tup[0], tup[1]
            if self.isOnBoard(r+rowChange, c+colChange):
                if board[r+rowChange][c+colChange] == None:
                    moves.append(Move((r, c), (r+rowChange,c+colChange), board))
                else:
                    if board[r][c].colour != board[r+rowChange][c+colChange].colour:
                        moves.append(Move((r, c), (r+rowChange,c+colChange), board))

        return moves
    
    def isOnBoard(self, r, c):
        if r >= 0 and r <=7 and c >= 0 and c <= 7:
            return True
        return False