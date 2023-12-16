from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen

class GameState():
    def __init__(self, game):
        self.whiteTurn = True
        self.moveLog = []
        self.wKingPos = (7, 4)
        self.bKingPos = (0, 4)
        self.checkmate = False
        self.stalemate = False

        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.board[7][0] = Rook(game, 7, 0, 'wR')
        self.board[7][7] = Rook(game, 7, 7, 'wR')
        self.board[7][1] = Knight(game, 7, 1, 'wN')
        self.board[7][6] = Knight(game, 7, 6, 'wN')
        self.board[7][2] = Bishop(game, 7, 2, 'wB')
        self.board[7][5] = Bishop(game, 7, 5, 'wB')
        self.board[7][3] = Queen(game, 7, 3, 'wQ')
        self.board[7][4] = King(game, 7, 4, 'wK')

        self.board[0][0] = Rook(game, 0, 0, 'bR')
        self.board[0][7] = Rook(game, 0, 7, 'bR')
        self.board[0][1] = Knight(game, 0, 1, 'bN')
        self.board[0][6] = Knight(game, 0, 6, 'bN')
        self.board[0][2] = Bishop(game, 0, 2, 'bB')
        self.board[0][5] = Bishop(game, 0, 5, 'bB')
        self.board[0][3] = Queen(game, 0, 3, 'bQ')
        self.board[0][4] = King(game, 0, 4, 'bK')

        for i in range(8):
            self.board[6][i] = Pawn(game, 6, i, 'wP')
            self.board[1][i] = Pawn(game, 1, i, 'bP')

    def movePiece(self, move):
        self.board[move.startRow][move.startCol].moveTo(move.endRow, move.endCol, self.board)
        self.whiteTurn = not self.whiteTurn
        self.moveLog.append(move)

        #update kings locations
        if move.movingPiece.identity == "wK":
            self.wKingPos = (move.endrow, move.endcol)
        elif move.movingPiece.identity == "bK":
            self.bKingPos = (move.endrow, move.endcol)
        
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop() 
            self.board[move.endRow][move.endCol].moveTo(move.startRow, move.startCol, self.board)
            self.board[move.endRow][move.endCol] = move.capturedSquare
            self.whiteTurn = not self.whiteTurn

            #update kings locations
            if move.movingPiece.identity == "wK":
                self.wKingPos = (move.startRow, move.startCol)
            elif move.movingPiece.identity == "bK":
                self.bKingPos =(move.startRow, move.startCol)

    def getAllPossibleMoves(self):
        moves = []
        for r in range(8):
            for c in range(8):
                if self.board[r][c] != None:
                    piece = self.board[r][c]
                    if piece.isColour(self.whiteTurn):
                        moves = piece.getMoves(moves, self.board)
        return moves
        
    def getAllValidMoves(self):
        #generate all possible moves
        moves = self.getAllPossibleMoves()
        #for each possible move, make move
        for i in range (len(moves) -1, -1, -1): #start from end of list
            self.movePiece(moves[i])

            #after make move, generate all opponents moves (squareunderAttack)
            #for each opponent move, see if they attack king

            #flip because makeMoves changes the turn
            self.whiteTurn = not self.whiteTurn 
            if self.inCheck():
                moves.remove(moves[i])
            #reset turn 
            self.whiteTurn = not self.whiteTurn
            self.undoMove()

        #either stalemate or checkmate
        if(len(moves) == 0): 
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True
        #if they do attack king, not valid move
        return moves
        
    #checks if is current player under attack
    def inCheck(self):
        
        if self.whiteTurn:
            return self.squareUnderAttack(self.wKingPos[0], self.wKingPos[1])
        else:
            return self.squareUnderAttack(self.bKingPos[0], self.bKingPos[1])
        
    #checks if can enemy attak square r, c
    def squareUnderAttack(self, r , c):
        self.whiteTurn = not self.whiteTurn #used to check opponent moves
        opponentMoves = self.getAllPossibleMoves()
        self.whiteTurn = not self.whiteTurn #flip turns back

        for move in opponentMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
    
class Move():
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, start, end, board):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.movingPiece = board[self.startRow][self.startCol]
        self.capturedSquare = board[self.endRow][self.endCol]
        self.moveId = self.getChessNotation()

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        
        return self.moveId == other.moveId

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]

#[[bR, bN, bB, bQ, bK, bB, bN, bR] <----8th rank (0th in the array)
# [bP, bP, bP, bP, bP, bP, bP, bP]
# []
# []
# []
# []
# [wP, wP, wP, wP, wP, wP, wP, wP]
# [wR, wN, wB, wQ, wK, wB, wK, wR]] <----1st rank (7th in the array)
#  ^                            ^
#  a file (0)                   h file (7)


# (1,0) down
# (-1, 0) up
# (0,1) right
# (0, -1) left
# (1, 1) down right
# (1, -1) down left
# (-1, 1) up right
# (-1, -1) up left
