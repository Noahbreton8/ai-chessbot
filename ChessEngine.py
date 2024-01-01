from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.king import King
from pieces.knight import Knight
from pieces.pawn import Pawn
from pieces.queen import Queen
import copy

ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
rowsToRanks = {v: k for k, v in ranksToRows.items()}

filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
colsToFiles = {v: k for k, v in filesToCols.items()}
#starting fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
class GameState():
    def __init__(self, game, fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'):
        self.moveLog = []
        self.checkmate = False
        self.stalemate = False
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.inCheck2 = False
        self.pins = []
        self.checks = []
        self.whitePieces = set()
        self.blackPieces = set()

        self.loadFenPosition(game, fen)
        
        self.enPassanPossibleLog = [self.isEnPassantPossible]
        self.castleRightsLog = [CastleRights(self.currentCastleRights.wks, self.currentCastleRights.bks, self.currentCastleRights.wqs, self.currentCastleRights.bqs)]
    
    def loadFenPosition(self, game, fen):
        splitFen = fen.split(' ')
        fenBoard, turn, castling, enpassant = splitFen[0], splitFen[1], splitFen[2], splitFen[3]

        #setting up board
        row, col = 0, 0
        for character in fenBoard:
            if character == '/':
                row += 1
                col = 0
            elif character.isnumeric():
                col += int(character)
            else:
                colour = 'w' if character.isupper() else 'b'
                identity = character.upper()
                if identity == 'K':
                    self.board[row][col] = King(game, row, col, colour+identity)
                    if colour == 'w':
                        self.wKingPos = (row, col)
                        self.whitePieces.add((row, col))
                    else:
                        self.bKingPos = (row, col)
                        self.blackPieces.add((row, col))
                elif identity == 'R':
                    self.board[row][col] = Rook(game, row, col, colour+identity)
                    if colour == 'w':
                        self.whitePieces.add((row, col))
                    else:
                        self.blackPieces.add((row, col))
                elif identity == 'N':
                    self.board[row][col] = Knight(game, row, col, colour+identity)
                    if colour == 'w':
                        self.whitePieces.add((row, col))
                    else:
                        self.blackPieces.add((row, col))
                elif identity == 'B':
                    self.board[row][col] = Bishop(game, row, col, colour+identity)
                    if colour == 'w':
                        self.whitePieces.add((row, col))
                    else:
                        self.blackPieces.add((row, col))
                elif identity == 'Q':
                    self.board[row][col] = Queen(game, row, col, colour+identity)
                    if colour == 'w':
                        self.whitePieces.add((row, col))
                    else:
                        self.blackPieces.add((row, col))
                elif identity == 'P':
                    self.board[row][col] = Pawn(game, row, col, colour+identity)
                    if colour == 'w':
                        self.whitePieces.add((row, col))
                    else:
                        self.blackPieces.add((row, col))
                col += 1

        #setting up start
        self.whiteTurn = True if turn == 'w' else False

        #setting up starting castling rights
        self.currentCastleRights = CastleRights(True if 'K' in castling else False, True if 'k' in castling else False, True if 'Q' in castling else False, True if 'q' in castling else False)

        #setting up if en passant is possible
        #only 1 en passant is possible at a time, this stores coords
        self.isEnPassantPossible = ()
        if enpassant != '-':
            self.isEnPassantPossible = (ranksToRows[enpassant[1]], filesToCols[enpassant[0]])
        
        #FOR FUTURE USE
        # self.halfMoves = int(halfmoves)
        # self.fullMoves = int(fullmoves)-1


    def movePiece(self, move):
        self.board[move.startRow][move.startCol].moveTo(move.endRow, move.endCol, self.board)

        if self.whiteTurn:
            self.whitePieces.remove((move.startRow, move.startCol))
            self.whitePieces.add((move.endRow, move.endCol))
            if move.capturedSquare != None:
                self.blackPieces.discard((move.endRow, move.endCol)) #Safer to use discard than remove cause piece might not be there cause of en passant
        else:
            self.blackPieces.remove((move.startRow, move.startCol))
            self.blackPieces.add((move.endRow, move.endCol))
            if move.capturedSquare != None:
                self.whitePieces.discard((move.endRow, move.endCol)) #Safer to use discard than remove cause piece might not be there cause of en passant

        self.whiteTurn = not self.whiteTurn
        self.moveLog.append(move)

        #update kings locations
        if move.movingPiece.identity == "wK":
            self.wKingPos = (move.endRow, move.endCol)
        elif move.movingPiece.identity == "bK":
            self.bKingPos = (move.endRow, move.endCol)

        #is pawn promotion
        if move.isPawnPromotion:
            match move.promotionChoice:
                case 'Q':
                    if self.whiteTurn:
                        Queen(move.movingPiece.game, move.startRow, move.startCol, 'bQ').moveTo(move.endRow, move.endCol, self.board)
                    else: 
                        Queen(move.movingPiece.game, move.startRow, move.startCol, 'wQ').moveTo(move.endRow, move.endCol, self.board)
                case 'R':
                    if self.whiteTurn:
                        Rook(move.movingPiece.game, move.startRow, move.startCol, 'bR').moveTo(move.endRow, move.endCol, self.board)
                    else: 
                        Rook(move.movingPiece.game, move.startRow, move.startCol, 'wR').moveTo(move.endRow, move.endCol, self.board)
                case 'N':
                    if self.whiteTurn:
                        Knight(move.movingPiece.game, move.startRow, move.startCol, 'bN').moveTo(move.endRow, move.endCol, self.board)
                    else: 
                        Knight(move.movingPiece.game, move.startRow, move.startCol, 'wN').moveTo(move.endRow, move.endCol, self.board)
                case 'B':
                    if self.whiteTurn:
                        Bishop(move.movingPiece.game, move.startRow, move.startCol, 'bB').moveTo(move.endRow, move.endCol, self.board)
                    else: 
                        Bishop(move.movingPiece.game, move.startRow, move.startCol, 'wB').moveTo(move.endRow, move.endCol, self.board)

        #enpassant
        if move.isEnPassantMove:
            self.board[move.startRow][move.endCol] = None
            if self.whiteTurn:
                self.whitePieces.remove((move.startRow, move.endCol))
            else:
                self.blackPieces.remove((move.startRow, move.endCol))

        #update enPassant var on 2 square advances
        if ('wP' == move.movingPiece.identity or 'bP' == move.movingPiece.identity) and abs(move.startRow - move.endRow) == 2: 
            #first half calculates row , second is column
            self.isEnPassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.isEnPassantPossible = ()

        #enpassant log
        self.enPassanPossibleLog.append(self.isEnPassantPossible)

        #castle moves
        if move.isCastleMove:
            #king side castle
            if move.endCol - move.startCol == 2:
                self.board[move.endRow][move.endCol+1].moveTo(move.endRow, move.endCol-1, self.board)
                if move.movingPiece.identity == "wK":
                    self.whitePieces.remove((move.endRow, move.endCol+1))
                    self.whitePieces.add((move.endRow, move.endCol-1))
                elif move.movingPiece.identity == "bK":
                    self.blackPieces.remove((move.endRow, move.endCol+1))
                    self.blackPieces.add((move.endRow, move.endCol-1))
            
            #queen side castle
            else:
                self.board[move.endRow][move.endCol-2].moveTo(move.endRow, move.endCol+1, self.board)
                if move.movingPiece.identity == "wK":
                    self.whitePieces.remove((move.endRow, move.endCol-2))
                    self.whitePieces.add((move.endRow, move.endCol+1))
                elif move.movingPiece.identity == "bK":
                    self.blackPieces.remove((move.endRow, move.endCol-2))
                    self.blackPieces.add((move.endRow, move.endCol+1))

        #castle rights
        self.updateCastleRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastleRights.wks, self.currentCastleRights.bks, self.currentCastleRights.wqs, self.currentCastleRights.bqs))


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.endRow][move.endCol].moveTo(move.startRow, move.startCol, self.board)

            if self.whiteTurn:
                self.blackPieces.remove((move.endRow, move.endCol))
                self.blackPieces.add((move.startRow, move.startCol))
                if move.capturedSquare != None and not move.isEnPassantMove:
                    self.whitePieces.add((move.endRow, move.endCol))
                
            else:
                self.whitePieces.remove((move.endRow, move.endCol))
                self.whitePieces.add((move.startRow, move.startCol))
                if move.capturedSquare != None and not move.isEnPassantMove:
                    self.blackPieces.add((move.endRow, move.endCol))

            self.board[move.endRow][move.endCol] = move.capturedSquare
            self.whiteTurn = not self.whiteTurn

            #update kings locations
            if move.movingPiece.identity == "wK":
                self.wKingPos = (move.startRow, move.startCol)
            elif move.movingPiece.identity == "bK":
                self.bKingPos =(move.startRow, move.startCol)

            #is pawn promotion
            if move.isPawnPromotion:
                #undo queen creation
                removePromotionPiece = self.board[move.startRow][move.startCol]
                del removePromotionPiece
                move.movingPiece.moveTo(move.startRow, move.startCol, self.board)
                    
                if(move.capturedSquare is not None):
                    move.capturedSquare.moveTo(move.endRow, move.endCol, self.board)

            #undo enPassant        
            if move.isEnPassantMove:
                #leave blank square blank
                self.board[move.endRow][move.endCol] = None 
                self.board[move.startRow][move.endCol] = move.capturedSquare
                if self.whiteTurn:
                    self.blackPieces.add((move.startRow, move.endCol))
                else:
                    self.whitePieces.add((move.startRow, move.endCol))
                # self.isEnPassantPossible = (move.endRow, move.endCol) DONT NEED

            self.enPassanPossibleLog.pop()
            self.isEnPassantPossible = self.enPassanPossibleLog[-1]

            #undo 2square advance (pawn) DONT NEED
            # if ('wP' or 'bP' in move.movingPiece.identity) and abs(move.startRow - move.endRow) == 2:
            #     self.isEnPassantPossible = ()
            
            #undoing castle rights
            self.castleRightsLog.pop()
            castleRights = copy.deepcopy(self.castleRightsLog[-1])
            self.currentCastleRights = castleRights
                
            #undoing castle move
            if move.isCastleMove:
                #king side castle
                if move.endCol - move.startCol == 2:
                    self.board[move.endRow][move.endCol-1].moveTo(move.endRow, move.endCol+1, self.board)
                    if move.movingPiece.identity == "wK":
                        self.whitePieces.add((move.endRow, move.endCol+1))
                        self.whitePieces.remove((move.endRow, move.endCol-1))
                    elif move.movingPiece.identity == "bK":
                        self.blackPieces.add((move.endRow, move.endCol+1))
                        self.blackPieces.remove((move.endRow, move.endCol-1))
                
                #queen side castle
                else:
                    self.board[move.endRow][move.endCol+1].moveTo(move.endRow, move.endCol-2, self.board)
                    if move.movingPiece.identity == "wK":
                        self.whitePieces.add((move.endRow, move.endCol-2))
                        self.whitePieces.remove((move.endRow, move.endCol+1))
                    elif move.movingPiece.identity == "bK":
                        self.blackPieces.add((move.endRow, move.endCol-2))
                        self.blackPieces.remove((move.endRow, move.endCol+1))

        self.checkmate = False
        self.stalemate = False


    def updateCastleRights(self, move):
        if move.movingPiece.identity == 'wK':
            self.currentCastleRights.wks = False
            self.currentCastleRights.wqs = False
        elif move.movingPiece.identity == 'bK':
            self.currentCastleRights.bks = False
            self.currentCastleRights.bqs = False
        elif move.movingPiece.identity == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastleRights.wqs = False
                elif move.startCol == 7:
                    self.currentCastleRights.wks = False
        elif move.movingPiece.identity == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastleRights.bqs = False
                elif move.startCol == 7:
                    self.currentCastleRights.bks = False
        elif isinstance(move.capturedSquare, Rook):
            if move.capturedSquare.identity == 'wR':
                if move.capturedSquare.row == 7:
                    if move.capturedSquare.col == 7:
                        self.currentCastleRights.wks = False
                    elif move.capturedSquare.col == 0:
                        self.currentCastleRights.wqs = False
            else:
                if move.capturedSquare.row == 0:
                    if move.capturedSquare.col == 7:
                        self.currentCastleRights.bks = False
                    elif move.capturedSquare.col == 0:
                        self.currentCastleRights.bqs = False

    def getAllPossibleMoves(self):
        moves = []

        if self.whiteTurn:
            for r, c in self.whitePieces:
                piece = self.board[r][c]
                if isinstance(piece, Pawn):
                    moves, self.pins = piece.getMoves(moves, self.board, self.isEnPassantPossible, self.pins, self)
                elif isinstance(piece, King):
                    moves = piece.getMoves(moves, self.board, self)
                else: 
                    moves, self.pins = piece.getMoves(moves, self.board, self.pins)
        else:
            for r, c in self.blackPieces:
                piece = self.board[r][c]
                if isinstance(piece, Pawn):
                    moves, self.pins = piece.getMoves(moves, self.board, self.isEnPassantPossible, self.pins, self)
                elif isinstance(piece, King):
                    moves = piece.getMoves(moves, self.board, self)
                else: 
                    moves, self.pins = piece.getMoves(moves, self.board, self.pins)

        # for r in range(8):
        #     for c in range(8):
        #         if self.board[r][c] != None:
        #             piece = self.board[r][c]
        #             if piece.isColour(self.whiteTurn):
        #                 if isinstance(piece, Pawn):
        #                     moves, self.pins = piece.getMoves(moves, self.board, self.isEnPassantPossible, self.pins, self)
        #                 elif isinstance(piece, King):
        #                     moves = piece.getMoves(moves, self.board, self)
        #                 else: 
        #                     moves, self.pins = piece.getMoves(moves, self.board, self.pins)    
        return moves
        
    def getAllValidMoves(self):
        tempEnPassantPossible = self.isEnPassantPossible
        tempCastleRights = CastleRights(self.currentCastleRights.wks, self.currentCastleRights.bks, self.currentCastleRights.wqs, self.currentCastleRights.bqs)
        #generate all possible moves
        moves = self.getAllPossibleMoves()

        if self.whiteTurn:
            self.getCastleMoves(self.wKingPos[0], self.wKingPos[1], moves)  
        else: 
            self.getCastleMoves(self.bKingPos[0], self.bKingPos[1], moves)

        #for each possible move, make move
        for i in range (len(moves) -1, -1, -1): #start from end of list
            self.movePiece(moves[i])

            #after make move, generate all opponents moves (squareunderAttack)
            #for each opponent move, see if they attack king

            #flip because makeMoves changes the turn
            self.whiteTurn = not self.whiteTurn 
            if self.inCheck():
                moves.remove(moves[i])
            elif moves[i].isCastleMove:
                #king side castle
                if moves[i].endCol - moves[i].startCol == 2:
                    if self.squareUnderAttack(moves[i].endRow, moves[i].endCol-1):
                        moves.remove(moves[i])
                #queen side castle
                else:
                    if self.squareUnderAttack(moves[i].endRow, moves[i].endCol+1):
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
                   
        self.isEnPassantPossible = tempEnPassantPossible
        self.currentCastleRights = tempCastleRights     
        return moves     

    def getValidMoves(self):
        moves = []

        self.inCheck2, self.pins, self.checks = self.checkForPinsAndChecks()    
        if self.whiteTurn :
            kingRow = self.wKingPos[0]
            kingCol = self.wKingPos[1]
        else:
            kingRow = self.bKingPos[0]
            kingCol = self.bKingPos[1]
        if self.inCheck2:
            if len(self.checks) == 1:
                moves = self.getAllPossibleMoves()
                check = self.checks[0]
                checkRow = check [0]
                checkCol = check [1]
                pieceChecking = self.board[checkRow][checkCol]
                valideSquares = []

                if pieceChecking.identity[1] == 'N':
                    valideSquares = [(checkRow, checkCol)]
                else:
                    for i in range (1, 8):
                        valideSquare = (kingRow + check[2] * i, kingCol + check[3] * i)
                        valideSquares.append(valideSquare)
                        if valideSquare[0] == checkRow and valideSquare[1] == checkCol:
                            break
                for i in range (len(moves) -1, -1, -1):
                    if moves[i].movingPiece.identity[1] != 'K':
                        if moves[i].isEnPassantMove:
                            if not (moves[i].endRow+1, moves[i].endCol) in valideSquares:
                                moves.remove(moves[i])
                        else:
                            if not (moves[i].endRow, moves[i].endCol) in valideSquares:
                                moves.remove(moves[i])
            else:
                piece = self.board[kingRow][kingCol]
                if isinstance(piece, Pawn):
                    moves, self.pins = piece.getMoves(moves, self.board, self.isEnPassantPossible, self.pins, self)
                elif isinstance(piece, King):
                    moves = piece.getMoves(moves, self.board, self)
                else: 
                    moves, self.pins = piece.getMoves(moves, self.board, self.pins)  
        else: 
            moves = self.getAllPossibleMoves()

            if self.whiteTurn:
                self.getCastleMoves(self.wKingPos[0], self.wKingPos[1], moves)  
            else: 
                self.getCastleMoves(self.bKingPos[0], self.bKingPos[1], moves)

        #either stalemate or checkmate
        if(len(moves) == 0): 
            if self.inCheck():
                self.checkmate = True
            else:
                self.stalemate = True

        return moves

    #checks if is current player under attack
    def inCheck(self):
        if self.whiteTurn:
            return self.squareUnderAttack(self.wKingPos[0], self.wKingPos[1])
        else:
            return self.squareUnderAttack(self.bKingPos[0], self.bKingPos[1])
        
    def checkForPinsAndChecks(self) :
        pins = []
        checks = []
        inCheck2 = False

        if self.whiteTurn:
            enemyColour = 'b'
            allycolour = 'w'
            startRow = self.wKingPos[0]
            startCol = self.wKingPos[1]
        else:
            enemyColour = 'w'
            allycolour = 'b'
            startRow = self.bKingPos[0]
            startCol = self.bKingPos[1]
        
        directions = [(-1,0), (0, -1), (1, 0), (0, 1), (-1,-1), (-1, 1), (1, -1), (1, 1)]

        for j in range (len(directions)):
            d = directions[j]
            possiblePin = ()
            for i in range (1,8):
                endRow = startRow + d[0] * i
                endCol = startCol + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol<8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece != None and endPiece.colour == allycolour and endPiece.identity[1] != 'K':
                        if possiblePin == ():
                            possiblePin = (endRow, endCol, d[0], d[1])
                        else:
                            break
                    elif endPiece != None and endPiece.colour == enemyColour:
                        type = endPiece.identity[1]

                        if (0<=j <= 3 and type == 'R') or \
                            (4 <= j <= 7 and type == 'B') or \
                            (i == 1 and type == 'P' and ((enemyColour == 'w' and 6 <= j <= 7) or (enemyColour == 'b' and 4 <= j <= 5))) or \
                            (type == 'Q') or (i == 1 and type == 'K') :

                            if possiblePin == ():
                                inCheck2 = True
                                checks.append((endRow, endCol, d[0],d[1]))
                                break
                            else: 
                                pins.append(possiblePin)
                                break
                        else :
                            break
                else :
                    break
        knightMoves = [(-2,-1), (-2,1), (-1,-2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
        for m in knightMoves:
            endRow = startRow + m[0]
            endCol = startCol + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:
                endPiece = self.board[endRow][endCol]
                if endPiece != None and endPiece.colour == enemyColour and endPiece.identity[1] == 'N':
                    inCheck2 = True
                    checks.append((endRow, endCol, m[0], m[1]))
        return inCheck2, pins, checks
    

            
                            
                        

        
    #checks if can enemy attak square r, c
    def squareUnderAttack(self, r , c):
        self.whiteTurn = not self.whiteTurn #used to check opponent moves
        opponentMoves = self.getAllPossibleMoves()
        self.whiteTurn = not self.whiteTurn #flip turns back

        for move in opponentMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False
    
    def getCastleMoves(self, r, c, moves):
        if self.inCheck():
            return
        
        if (self.whiteTurn and self.currentCastleRights.wks) or (not self.whiteTurn and self.currentCastleRights.bks):
            self.getKingsideCastleMoves(r, c, moves)

        if (self.whiteTurn and self.currentCastleRights.wqs) or (not self.whiteTurn and self.currentCastleRights.bqs):
            self.getQueensideCastleMoves(r, c, moves)

    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == None and self.board[r][c+2] == None:
            #if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2): #moved into validate moves since it cannot check for pawn attacks
            if self.whiteTurn:
                self.wKingPos = (r,c + 1)
            else:
                self.bKingPos = (r,c + 1)
            inCheck3, pins, checks = self.checkForPinsAndChecks()
            if not inCheck3:
                if self.whiteTurn:
                    self.wKingPos = (r,c + 2)
                else:
                    self.bKingPos = (r,c + 2)
                inCheck4, pins, checks = self.checkForPinsAndChecks()
                if not inCheck4:
                        moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))

            if self.whiteTurn:
                    self.wKingPos = (r,c)
            else:
                    self.bKingPos = (r,c)
            
                
        
    
    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == None and self.board[r][c-2] == None and self.board[r][c-3] == None:
            if self.whiteTurn:
                self.wKingPos = (r,c - 1)
            else:
                self.bKingPos = (r,c - 1)
            inCheck3, pins, checks = self.checkForPinsAndChecks()
            if not inCheck3:
                if self.whiteTurn:
                    self.wKingPos = (r,c - 2)
                else:
                    self.bKingPos = (r,c - 2)
                inCheck4, pins, checks = self.checkForPinsAndChecks()
                if not inCheck4:
                        moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))

            if self.whiteTurn:
                    self.wKingPos = (r,c)
            else:
                    self.bKingPos = (r,c)
                
    
class Move():
    ranksToRows = {'1': 7, '2': 6, '3': 5, '4': 4, '5': 3, '6': 2, '7': 1, '8': 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, start, end, board, isEnPassantMove = False, isCastleMove = False, promotion = None):
        self.startRow = start[0]
        self.startCol = start[1]
        self.endRow = end[0]
        self.endCol = end[1]
        self.movingPiece = board[self.startRow][self.startCol]
        self.capturedSquare = board[self.endRow][self.endCol]
        
        self.isPawnPromotion = True if promotion != None else False
        self.promotionChoice = promotion
        
        self.isEnPassantMove = isEnPassantMove
        if self.isEnPassantMove:
            if self.movingPiece.identity == 'bP':
                self.capturedSquare = Pawn(self.movingPiece.game, self.endRow-1, self.endCol, 'wP')
            else:
                self.capturedSquare = Pawn(self.movingPiece.game, self.endRow+1, self.endCol, 'bP')

        self.isCastleMove = isCastleMove

        self.moveId = self.getChessNotation()

    def __eq__(self, other):
        if not isinstance(other, Move):
            return False
        
        return self.moveId == other.moveId

    def getChessNotation(self):
        #Uncomment for testing
        # if self.isPawnPromotion:
        #     return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol) + self.promotionChoice.lower()
        # else:
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getAlgebraicNotation(self):
    #always return self.movingPiece.identity's endingSquare unless 
    #two pieces can move to same square
    #captures 
    #castle
        if("P" in self.movingPiece.identity):
            if(self.capturedSquare != None):
                return self.getRankFile(self.startRow, self.startCol)[:-1]+ "x" + self.getRankFile(self.endRow, self.endCol)
            return self.getRankFile(self.endRow, self.endCol)

        return self.movingPiece.identity+ ": "+ self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
    
class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs

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
