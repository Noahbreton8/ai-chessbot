from .piece import Piece

class Pawn(Piece):
    def __init__(self, *args):
        super().__init__(*args)

    def getMoves(self, moves, board, isEnPassantPossible):
        from ChessEngine import Move
        if self.colour == 'w':
            if board[self.row-1][self.col]==None:
                #move one square up
                moves.append(Move((self.row, self.col), (self.row-1, self.col), board)) 

                #If on starting square see if pawn can move two squares
                if self.row == 6 and board[self.row-2][self.col] == None:
                    moves.append(Move((self.row, self.col), (self.row-2, self.col), board))

            #Capturing left
            if self.col > 0 and board[self.row-1][self.col-1] != None:
                if board[self.row-1][self.col-1].colour =='b':
                    moves.append(Move((self.row, self.col), (self.row-1, self.col-1), board))
                #capturing blank square (enPassant)
            elif self.col > 0 and board[self.row][self.col-1] != None:
                if board[self.row][self.col-1].colour =='b':
                    if (self.row-1, self.col-1) == isEnPassantPossible:
                        moves.append(Move((self.row, self.col), (self.row-1, self.col-1), board, True))

            #Capturing right
            if self.col < 7 and board[self.row-1][self.col+1] != None:
                if board[self.row-1][self.col+1].colour =='b':
                    moves.append(Move((self.row, self.col), (self.row-1, self.col+1), board))
                #capturing blank square (enPassant)
            elif self.col < 7 and board[self.row][self.col+1] != None:
                if board[self.row][self.col+1].colour =='b':
                    if (self.row-1, self.col+1) == isEnPassantPossible:
                        moves.append(Move((self.row, self.col), (self.row-1, self.col+1), board, True))

        else:
            if board[self.row+1][self.col]==None:
                #move one square down
                moves.append(Move((self.row, self.col), (self.row+1, self.col), board))

                if self.row == 1 and board[self.row+2][self.col] == None:
                    moves.append(Move((self.row, self.col), (self.row+2, self.col), board))

            #Capturing right (from white side perspective)
            if self.col > 0 and board[self.row+1][self.col-1] != None:
                if board[self.row+1][self.col-1].colour =='w':
                    moves.append(Move((self.row, self.col), (self.row+1, self.col-1), board))
                    #capturing blank square (enPassant)
            elif self.col > 0 and board[self.row][self.col-1] != None:
                if board[self.row][self.col-1].colour =='w':
                    if (self.row+1, self.col-1) == isEnPassantPossible:
                        moves.append(Move((self.row, self.col), (self.row+1, self.col-1), board, True))

            #Capturing left (from white side perspective)
            if  self.col < 7 and board[self.row+1][self.col+1] != None:
                if board[self.row+1][self.col+1].colour =='w':
                    moves.append(Move((self.row, self.col), (self.row+1, self.col+1), board))
                    #capturing blank square (enPassant)
            elif self.col < 7 and board[self.row][self.col+1] != None:
                if board[self.row][self.col+1].colour =='w':
                    if (self.row+1, self.col+1) == isEnPassantPossible:
                        moves.append(Move((self.row, self.col), (self.row+1, self.col+1), board, True))

        return moves
    