from .piece import Piece

class Knight(Piece):
    def getMoves(self, moves, board):
        from ChessEngine import Move
        r, c = self.row, self.col
        if self.isOnBoard(r-2, c-1):
            if board[r-2][c-1] == None:
                moves.append(Move((r, c), (r-2,c-1), board))
            else:
                if board[r][c].colour != board[r-2][c-1].colour:
                    moves.append(Move((r, c), (r-2,c-1), board))

        if self.isOnBoard(r-2, c+1):
            if board[r-2][c+1] == None:
                moves.append(Move((r, c), (r-2,c+1), board))
            else:
                if board[r][c].colour != board[r-2][c+1].colour:
                    moves.append(Move((r, c), (r-2,c+1), board))
        
        if self.isOnBoard(r+2, c-1):
            if board[r+2][c-1] == None:
                moves.append(Move((r, c), (r+2,c-1), board))
            else:
                if board[r][c].colour != board[r+2][c-1].colour:
                    moves.append(Move((r, c), (r+2,c-1), board))

        if self.isOnBoard(r+2, c+1):
            if board[r+2][c+1] == None:
                moves.append(Move((r, c), (r+2,c+1), board))
            else:
                if board[r][c].colour != board[r+2][c+1].colour:
                    moves.append(Move((r, c), (r+2,c+1), board))

        if self.isOnBoard(r-1, c-2):
            if board[r-1][c-2] == None:
                moves.append(Move((r, c), (r-1,c-2), board))
            else:
                if board[r][c].colour != board[r-1][c-2].colour:
                    moves.append(Move((r, c), (r-1,c-2), board))

        if self.isOnBoard(r-1, c+2):
            if board[r-1][c+2] == None:
                moves.append(Move((r, c), (r-1, c+2), board))
            else:
                if board[r][c].colour != board[r-1][c+2].colour:
                    moves.append(Move((r, c), (r-1, c+2), board))

        if self.isOnBoard(r+1, c-2):
            if board[r+1][c-2] == None:
                moves.append(Move((r, c), (r+1, c-2), board))
            else:
                if board[r][c].colour != board[r+1][c-2].colour:
                    moves.append(Move((r, c), (r+1, c-2), board))
        
        if self.isOnBoard(r+1, c+2):
            if board[r+1][c+2] == None:
                moves.append(Move((r, c), (r+1, c+2), board))
            else:
                if board[r][c].colour != board[r+1][c+2].colour:
                    moves.append(Move((r, c), (r+1, c+2), board))

        return moves
    
    def isOnBoard(self, r, c):
        if r >= 0 and r <=7 and c >= 0 and c <= 7:
            return True
        return False