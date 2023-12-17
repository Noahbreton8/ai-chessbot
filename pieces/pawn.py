from .piece import Piece

class Pawn(Piece):
    def __init__(self, *args):
        self.hasMoved = False
        super().__init__(*args)

    def getMoves(self, moves, board):
        from ChessEngine import Move
        if self.colour == 'w':
            if board[self.row-1][self.col]==None:
                #move one square up
                moves.append(Move((self.row, self.col), (self.row-1, self.col), board)) 

                #If on starting square see if pawn can move two squares
                if not self.hasMoved and board[self.row-2][self.col]==None:
                    moves.append(Move((self.row, self.col), (self.row-2, self.col), board))
                
            #Capturing left
            if self.col > 0 and board[self.row-1][self.col-1] != None and board[self.row-1][self.col-1].colour =='b':
                moves.append(Move((self.row, self.col), (self.row-1, self.col-1), board))
            
            #Capturing right
            if self.col < 7 and board[self.row-1][self.col+1] != None and board[self.row-1][self.col+1].colour =='b':
                moves.append(Move((self.row, self.col), (self.row-1, self.col+1), board))
        
        else:
            if board[self.row+1][self.col]==None:
                #move one square down
                moves.append(Move((self.row, self.col), (self.row+1, self.col), board))

                #If on starting square see if pawn can move two squares + out of bounds check
                if not self.hasMoved and self.row + 2 < 8:
                    if board[self.row+2][self.col]==None:
                        moves.append(Move((self.row, self.col), (self.row+2, self.col), board))

            #Capturing right (from white side perspective)
            if self.col > 0 and board[self.row+1][self.col-1] != None and board[self.row+1][self.col-1].colour =='w':
                moves.append(Move((self.row, self.col), (self.row+1, self.col-1), board))
            
            #Capturing left (from white side perspective)
            if  self.col < 7 and board[self.row+1][self.col+1] != None and board[self.row+1][self.col+1].colour =='w':
                moves.append(Move((self.row, self.col), (self.row+1, self.col+1), board))

        return moves