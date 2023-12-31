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


    def getMoves(self, moves, board, isEnPassantPossible, pins, gs):
        from ChessEngine import Move

        piecePinned = False
        pinDirection = ()
        for i in range(len(pins)-1,-1,-1):
            if pins[i][0] == self.row and pins[i][1] == self.col:   
                piecePinned = True
                pinDirection = (pins[i][2], pins[i][3])
                pins.remove(pins[i])
                break

        if self.colour == 'w':
            startRow = 6
            enemyColour = 'b'
            kingRow, kingCol = gs.wKingPos
        else:
            startRow = 1
            enemyColour = 'w'
            kingRow, kingCol = gs.bKingPos

        promotion = False
        if self.colour == 'w':
            if self.row-1 == 0:
                promotion = True
            if board[self.row-1][self.col]==None:
                if not piecePinned or pinDirection == (-1,0):
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
                if not piecePinned or pinDirection == (-1,-1):
                    if board[self.row-1][self.col-1].colour =='b':
                        if promotion:
                            self.handlePromotionMoves(moves, board, self.row, self.col, self.row-1, self.col-1)
                        else:
                            moves.append(Move((self.row, self.col), (self.row-1, self.col-1), board))
                #capturing blank square (enPassant)
            elif self.col > 0 and board[self.row][self.col-1] != None:

                #FIX LATER

                if board[self.row][self.col-1].colour =='b':
                    if (self.row-1, self.col-1) == isEnPassantPossible:
                        attackingPiece = blockingPiece = False
                        if kingRow == self.row:
                            if kingCol < self.col:
                                #inside between king and pawn, outside is between pawn border
                                insideRange = range(kingCol + 1, self.col -1)
                                outsideRange = range(self.col + 1, 8)
                            else:
                                insideRange = range(kingCol -1, self.col, -1)
                                outsideRange = range(self.col-2, -1, -1)
                            for i in insideRange:
                                if board[self.row][i]: #some other piece blocking 
                                    blockingPiece = True
                            for i in outsideRange:
                                square = board[self.row][i]
                                if square != None and square.colour == enemyColour and (square.identity[1] == 'R' or square.identity[1] =='Q'):
                                    attackingPiece =True
                                elif square != None:
                                    blockingPiece = True

                        if not attackingPiece or blockingPiece:
                            moves.append(Move((self.row, self.col), (self.row-1, self.col-1), board, isEnPassantMove = True))

            #Capturing right
            if self.col < 7 and board[self.row-1][self.col+1] != None:
                if not piecePinned or pinDirection == (-1, 1):
                    if board[self.row-1][self.col+1].colour =='b':
                        if promotion:
                            self.handlePromotionMoves(moves, board, self.row, self.col, self.row-1, self.col+1)
                        else:
                            moves.append(Move((self.row, self.col), (self.row-1, self.col+1), board))
                #capturing blank square (enPassant)
            elif self.col < 7 and board[self.row][self.col+1] != None:
                if board[self.row][self.col+1].colour =='b':
                    if (self.row-1, self.col+1) == isEnPassantPossible:
                        attackingPiece = blockingPiece = False
                        if kingRow == self.row:
                            if kingCol < self.col:
                                #inside between king and pawn, outside is between pawn border
                                insideRange = range(kingCol + 1, self.col)
                                outsideRange = range(self.col + 2, 8)
                            else:
                                insideRange = range(kingCol -1, self.col + 1, -1)
                                outsideRange = range(self.col -1, -1, -1)
                            for i in insideRange:
                                if board[self.row][i]: #some other piece blocking 
                                    blockingPiece = True
                            for i in outsideRange:
                                square = board[self.row][i]
                                if square != None and square.colour == enemyColour and (square.identity[1] == 'R' or square.identity[1] =='Q'):
                                    attackingPiece =True
                                elif square != None:
                                    blockingPiece = True

                        if not attackingPiece or blockingPiece:
                            moves.append(Move((self.row, self.col), (self.row-1, self.col+1), board, isEnPassantMove = True))

        else:
            if self.row+1 == 7:
                promotion = True
            if board[self.row+1][self.col]==None:
                if not piecePinned or pinDirection == (1, 0):
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
                if not piecePinned or pinDirection == (1, -1):
                    if board[self.row+1][self.col-1].colour =='w':
                        if promotion:
                            self.handlePromotionMoves(moves, board, self.row, self.col, self.row+1, self.col-1)
                        else:
                            moves.append(Move((self.row, self.col), (self.row+1, self.col-1), board))
                    #capturing blank square (enPassant)
            elif self.col > 0 and board[self.row][self.col-1] != None:
                #FIX
                if board[self.row][self.col-1].colour =='w':
                    if (self.row+1, self.col-1) == isEnPassantPossible:
                        attackingPiece = blockingPiece = False
                        if kingRow == self.row:
                            if kingCol < self.col:
                                #inside between king and pawn, outside is between pawn border
                                insideRange = range(kingCol + 1, self.col -1)
                                outsideRange = range(self.col + 1, 8)
                            else:
                                insideRange = range(kingCol -1, self.col, -1)
                                outsideRange = range(self.col-2, -1, -1)
                            for i in insideRange:
                                if board[self.row][i]: #some other piece blocking 
                                    blockingPiece = True
                            for i in outsideRange:
                                square = board[self.row][i]
                                if square != None and square.colour == enemyColour and (square.identity[1] == 'R' or square.identity[1] =='Q'):
                                    attackingPiece =True
                                elif square != None:
                                    blockingPiece = True

                        if not attackingPiece or blockingPiece:
                            moves.append(Move((self.row, self.col), (self.row+1, self.col-1), board, isEnPassantMove = True))

            #Capturing right (from white side perspective)
            if  self.col < 7 and board[self.row+1][self.col+1] != None:
                if not piecePinned or pinDirection == (1, 1):
                    if board[self.row+1][self.col+1].colour =='w':
                        if promotion:
                            self.handlePromotionMoves(moves, board, self.row, self.col, self.row+1, self.col+1)
                        else:
                            moves.append(Move((self.row, self.col), (self.row+1, self.col+1), board))
                    #capturing blank square (enPassant)
            elif self.col < 7 and board[self.row][self.col+1] != None:
                if board[self.row][self.col+1].colour =='w':
                    if (self.row+1, self.col+1) == isEnPassantPossible:
                        attackingPiece = blockingPiece = False
                        if kingRow == self.row:
                            if kingCol < self.col:
                                #inside between king and pawn, outside is between pawn border
                                insideRange = range(kingCol + 1, self.col)
                                outsideRange = range(self.col + 2, 8)
                            else:
                                insideRange = range(kingCol -1, self.col + 1, -1)
                                outsideRange = range(self.col -1, -1, -1)
                            for i in insideRange:
                                if board[self.row][i]: #some other piece blocking 
                                    blockingPiece = True
                            for i in outsideRange:
                                square = board[self.row][i]
                                if square != None and square.colour == enemyColour and (square.identity[1] == 'R' or square.identity[1] =='Q'):
                                    attackingPiece =True
                                elif square != None:
                                    blockingPiece = True

                        if not attackingPiece or blockingPiece:
                            moves.append(Move((self.row, self.col), (self.row+1, self.col+1), board, isEnPassantMove = True))

        return moves, pins
    