from .piece import Piece

class Pawn(Piece):
    def __init__(self, *args):
        super().__init__(*args)

    def handlePromotionMoves(self, moves, board, startRow, startCol, endRow, endCol):
        from ChessEngine import Move
        moves.append(Move((startRow, startCol), (endRow, endCol), board, promotion="Q"))
        moves.append(Move((startRow, startCol), (endRow, endCol), board, promotion="N"))
        moves.append(Move((startRow, startCol), (endRow, endCol), board, promotion="B"))
        moves.append(Move((startRow, startCol), (endRow, endCol), board, promotion="R"))


    def getMoves(self, moves, board, isEnPassantPossible):
        from ChessEngine import Move
        promotion = False
        if self.colour == 'w':
            if self.row-1 == 0:
                promotion = True
            if board[self.row-1][self.col]==None:

                #move one square up
                if promotion:
                    self.handlePromotionMoves(moves, board, self.row, self.col, self.row-1, self.col)
                else:
                    moves.append(Move((self.row, self.col), (self.row-1, self.col), board))

                #If on starting square see if pawn can move two squares
                if self.row == 6 and board[self.row-2][self.col] == None:
                    moves.append(Move((self.row, self.col), (self.row-2, self.col), board))

            #Capturing left
            if self.col > 0 and board[self.row-1][self.col-1] != None:
                if board[self.row-1][self.col-1].colour =='b':
                    if promotion:
                        self.handlePromotionMoves(moves, board, self.row, self.col, self.row-1, self.col-1)
                    else:
                        moves.append(Move((self.row, self.col), (self.row-1, self.col-1), board))
                #capturing blank square (enPassant)
            elif self.col > 0 and board[self.row][self.col-1] != None:
                if board[self.row][self.col-1].colour =='b':
                    if (self.row-1, self.col-1) == isEnPassantPossible:
                        moves.append(Move((self.row, self.col), (self.row-1, self.col-1), board, isEnPassantMove = True))

            #Capturing right
            if self.col < 7 and board[self.row-1][self.col+1] != None:
                if board[self.row-1][self.col+1].colour =='b':
                    if promotion:
                        self.handlePromotionMoves(moves, board, self.row, self.col, self.row-1, self.col+1)
                    else:
                        moves.append(Move((self.row, self.col), (self.row-1, self.col+1), board))
                #capturing blank square (enPassant)
            elif self.col < 7 and board[self.row][self.col+1] != None:
                if board[self.row][self.col+1].colour =='b':
                    if (self.row-1, self.col+1) == isEnPassantPossible:
                        moves.append(Move((self.row, self.col), (self.row-1, self.col+1), board, isEnPassantMove = True))

        else:
            if self.row+1 == 7:
                promotion = True
            if board[self.row+1][self.col]==None:
                #move one square down
                if promotion:
                    self.handlePromotionMoves(moves, board, self.row, self.col, self.row+1, self.col)
                else:
                    moves.append(Move((self.row, self.col), (self.row+1, self.col), board))

                #if on starting square move 2 up
                if self.row == 1 and board[self.row+2][self.col] == None:
                    moves.append(Move((self.row, self.col), (self.row+2, self.col), board))

            #Capturing left (from white side perspective)
            if self.col > 0 and board[self.row+1][self.col-1] != None:
                if board[self.row+1][self.col-1].colour =='w':
                    if promotion:
                        self.handlePromotionMoves(moves, board, self.row, self.col, self.row+1, self.col-1)
                    else:
                        moves.append(Move((self.row, self.col), (self.row+1, self.col-1), board))
                    #capturing blank square (enPassant)
            elif self.col > 0 and board[self.row][self.col-1] != None:
                if board[self.row][self.col-1].colour =='w':
                    if (self.row+1, self.col-1) == isEnPassantPossible:
                        moves.append(Move((self.row, self.col), (self.row+1, self.col-1), board, isEnPassantMove = True))

            #Capturing right (from white side perspective)
            if  self.col < 7 and board[self.row+1][self.col+1] != None:
                if board[self.row+1][self.col+1].colour =='w':
                    if promotion:
                        self.handlePromotionMoves(moves, board, self.row, self.col, self.row+1, self.col+1)
                    else:
                        moves.append(Move((self.row, self.col), (self.row+1, self.col+1), board))
                    #capturing blank square (enPassant)
            elif self.col < 7 and board[self.row][self.col+1] != None:
                if board[self.row][self.col+1].colour =='w':
                    if (self.row+1, self.col+1) == isEnPassantPossible:
                        moves.append(Move((self.row, self.col), (self.row+1, self.col+1), board, isEnPassantMove = True))

        return moves
    