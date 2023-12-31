from .piece import Piece

class Knight(Piece):
    def getMoves(self, moves, board, pins):
        from ChessEngine import Move

        piecePinned = False
        for i in range(len(pins)-1,-1,-1):
            if pins[i][0] == self.row and pins[i][1] == self.col:   
                piecePinned = True
                pins.remove(pins[i])
                break

        r, c = self.row, self.col
        if self.isOnBoard(r-2, c-1) and not piecePinned:
            if board[r-2][c-1] == None:
                moves.append(Move((r, c), (r-2,c-1), board))
            else:
                if board[r][c].colour != board[r-2][c-1].colour:
                    moves.append(Move((r, c), (r-2,c-1), board))

        if self.isOnBoard(r-2, c+1) and not piecePinned:
            if board[r-2][c+1] == None:
                moves.append(Move((r, c), (r-2,c+1), board))
            else:
                if board[r][c].colour != board[r-2][c+1].colour:
                    moves.append(Move((r, c), (r-2,c+1), board))
        
        if self.isOnBoard(r+2, c-1) and not piecePinned:
            if board[r+2][c-1] == None:
                moves.append(Move((r, c), (r+2,c-1), board))
            else:
                if board[r][c].colour != board[r+2][c-1].colour:
                    moves.append(Move((r, c), (r+2,c-1), board))

        if self.isOnBoard(r+2, c+1) and not piecePinned:
            if board[r+2][c+1] == None:
                moves.append(Move((r, c), (r+2,c+1), board))
            else:
                if board[r][c].colour != board[r+2][c+1].colour:
                    moves.append(Move((r, c), (r+2,c+1), board))

        if self.isOnBoard(r-1, c-2) and not piecePinned:
            if board[r-1][c-2] == None:
                moves.append(Move((r, c), (r-1,c-2), board))
            else:
                if board[r][c].colour != board[r-1][c-2].colour:
                    moves.append(Move((r, c), (r-1,c-2), board))

        if self.isOnBoard(r-1, c+2) and not piecePinned:
            if board[r-1][c+2] == None:
                moves.append(Move((r, c), (r-1, c+2), board))
            else:
                if board[r][c].colour != board[r-1][c+2].colour:
                    moves.append(Move((r, c), (r-1, c+2), board))

        if self.isOnBoard(r+1, c-2) and not piecePinned:
            if board[r+1][c-2] == None:
                moves.append(Move((r, c), (r+1, c-2), board))
            else:
                if board[r][c].colour != board[r+1][c-2].colour:
                    moves.append(Move((r, c), (r+1, c-2), board))
        
        if self.isOnBoard(r+1, c+2) and not piecePinned:
            if board[r+1][c+2] == None:
                moves.append(Move((r, c), (r+1, c+2), board))
            else:
                if board[r][c].colour != board[r+1][c+2].colour:
                    moves.append(Move((r, c), (r+1, c+2), board))

        return moves, pins
    
    def isOnBoard(self, r, c):
        if r >= 0 and r <=7 and c >= 0 and c <= 7:
            return True
        return False