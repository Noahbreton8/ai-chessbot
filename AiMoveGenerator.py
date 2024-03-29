import random, time 

CHECKMATE = 100000
STALEMATE = 0
pieceScore = {"K": 0, "Q": 900, "R": 500, "B": 330, "N": 320, "P": 100}
DEPTH = 3

kingMiddleGameScoresW = [[-30,-40,-40,-50,-50,-40,-40,-30],
                        [-30,-40,-40,-50,-50,-40,-40,-30],
                        [-30,-40,-40,-50,-50,-40,-40,-30],
                        [-30,-40,-40,-50,-50,-40,-40,-30],
                        [-20,-30,-30,-40,-40,-30,-30,-20],
                        [-10,-20,-20,-20,-20,-20,-20,-10],
                        [ 20, 20,  0,  0,  0,  0, 20, 20],
                        [ 20, 30, 10,  0,  0, 10, 30, 20]]

kingMiddleGameScoresB = [[ 20, 30, 10,  0,  0, 10, 30, 20],
                        [ 20, 20,  0,  0,  0,  0, 20, 20],
                        [-10, -20, -20, -20, -20, -20, -20, -10],
                        [-20, -30, -30, -40, -40, -30, -30, -20],
                        [-30, -40, -40, -50, -50, -40, -40, -30],
                        [-30, -40, -40, -50, -50, -40, -40, -30],
                        [-30, -40, -40, -50, -50, -40, -40, -30],
                        [-30, -40, -40, -50, -50, -40, -40, -30]]

kingEndGameScoresW =    [[-50,-40,-30,-20,-20,-30,-40,-50],
                        [-30,-20,-10,  0,  0,-10,-20,-30],
                        [-30,-10, 20, 30, 30, 20,-10,-30],
                        [-30,-10, 30, 40, 40, 30,-10,-30],
                        [-30,-10, 30, 40, 40, 30,-10,-30],
                        [-30,-10, 20, 30, 30, 20,-10,-30],
                        [-30,-30,  0,  0,  0,  0,-30,-30],
                        [-50,-30,-30,-30,-30,-30,-30,-50]]

kingEndGameScoresB =    [[-50, -30, -30, -30, -30, -30, -30, -50],
                        [-30, -30, 0, 0, 0, 0, -30, -30],
                        [-30, -10, 20, 30, 30, 20, -10, -30],
                        [-30, -10, 30, 40, 40, 30, -10, -30],
                        [-30, -10, 30, 40, 40, 30, -10, -30],
                        [-30, -10, 20, 30, 30, 20, -10, -30],
                        [-30, -20, -10, 0, 0, -10, -20, -30],
                        [-50, -40, -30, -20, -20, -30, -40, -50]]

knightScoresW = [[-50,-40,-30,-30,-30,-30,-40,-50],
                [-40,-20,  0,  0,  0,  0,-20,-40],
                [-30,  0, 10, 15, 15, 10,  0,-30],
                [-30,  5, 15, 20, 20, 15,  5,-30],
                [-30,  0, 15, 20, 20, 15,  0,-30],
                [-30,  5, 10, 15, 15, 10,  5,-30],
                [-40,-20,  0,  5,  5,  0,-20,-40],
                [-50,-40,-30,-30,-30,-30,-40,-50]]

knightScoresB = [[-50, -40, -30, -30, -30, -30, -40, -50],
                [-40, -20, 0, 0, 0, 0, -20, -40],
                [-30, 5, 10, 15, 15, 10, 5, -30],
                [-30, 0, 15, 20, 20, 15, 0, -30],
                [-30, 5, 15, 20, 20, 15, 5, -30],
                [-30, 0, 10, 15, 15, 10, 0, -30],
                [-40, -20, 0, 5, 5, 0, -20, -40],
                [-50, -40, -30, -30, -30, -30, -40, -50]]

bishopScoresW = [[-20,-10,-10,-10,-10,-10,-10,-20],
                [-10,  0,  0,  0,  0,  0,  0,-10],
                [-10,  0,  5, 10, 10,  5,  0,-10],
                [-10,  5,  5, 10, 10,  5,  5,-10],
                [-10,  0, 10, 10, 10, 10,  0,-10],
                [-10, 10, 10, 10, 10, 10, 10,-10],
                [-10,  5,  0,  0,  0,  0,  5,-10],
                [-20,-10,-10,-10,-10,-10,-10,-20]]


bishopScoresB = [[-20, -10, -10, -10, -10, -10, -10, -20],
                [-10, 5, 0, 0, 0, 0, 5, -10],
                [-10, 10, 10, 10, 10, 10, 10, -10],
                [-10, 0, 10, 10, 10, 10, 0, -10],
                [-10, 5, 5, 10, 10, 5, 5, -10],
                [-10, 0, 5, 10, 10, 5, 0, -10],
                [-10, 0, 0, 0, 0, 0, 0, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]]

pawnScoresW =   [[ 0,  0,  0,  0,  0,  0,  0,  0],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [5,  5, 10, 25, 25, 10,  5,  5],
                [0,  0,  0, 20, 20,  0,  0,  0],
                [5, -5,-10,  0,  0,-10, -5,  5],
                [5, 10, 10,-20,-20, 10, 10,  5],
                [0,  0,  0,  0,  0,  0,  0,  0]]

pawnScoresB =   [[0, 0, 0, 0, 0, 0, 0, 0],
                [5, 10, 10, -20, -20, 10, 10, 5],
                [5, -5, -10, 0, 0, -10, -5, 5],
                [0, 0, 0, 20, 20, 0, 0, 0],
                [5, 5, 10, 25, 25, 10, 5, 5],
                [10, 10, 20, 30, 30, 20, 10, 10],
                [50, 50, 50, 50, 50, 50, 50, 50],
                [0, 0, 0, 0, 0, 0, 0, 0]]

rookScoresW =   [[ 0,  0,  0,  0,  0,  0,  0,  0],
                [ 5, 10, 10, 10, 10, 10, 10,  5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [-5,  0,  0,  0,  0,  0,  0, -5],
                [ 0,  0,  0,  5,  5,  0,  0,  0]]

rookScoresB =   [[0, 0, 0, 5, 5, 0, 0, 0],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [-5, 0, 0, 0, 0, 0, 0, -5],
                [5, 10, 10, 10, 10, 10, 10, 5],
                [0, 0, 0, 0, 0, 0, 0, 0]]

queenScoresW =  [[-20,-10,-10, -5, -5,-10,-10,-20],
                [-10,  0,  0,  0,  0,  0,  0,-10],
                [-10,  0,  5,  5,  5,  5,  0,-10],
                [ -5,  0,  5,  5,  5,  5,  0, -5],
                [ 0,  0,  5,  5,  5,  5,  0, -5 ],
                [-10,  5,  5,  5,  5,  5,  0,-10],
                [-10,  0,  5,  0,  0,  0,  0,-10],
                [-20,-10,-10, -5, -5,-10,-10,-20]]

queenScoresB =  [[-20, -10, -10, -5, -5, -10, -10, -20],
                [-10, 0, 5, 0, 0, 0, 0, -10],
                [-10, 5, 5, 5, 5, 5, 0, -10],
                [0, 0, 5, 5, 5, 5, 0, -5],
                [-5, 0, 5, 5, 5, 5, 0, -5],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-10, 0, 5, 5, 5, 5, 0, -10],
                [-20, -10, -10, -5, -5, -10, -10, -20]]

piecePositionScoreW = {"K": kingMiddleGameScoresW, "Q": queenScoresW, "R": rookScoresW, "B": bishopScoresW, "N": knightScoresW, "P": pawnScoresW}
piecePositionScoreB = {"K": kingMiddleGameScoresB, "Q": queenScoresB, "R": rookScoresB, "B": bishopScoresB, "N": knightScoresB, "P": pawnScoresB}

def findBestMove(gs, validMoves):
    global nextMove, counter
    nextMove = None
    counter = 0
    startTime = time.time()
    findMoveNegaMaxABv2(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, True if gs.whiteTurn else False)
    endtime = time.time()
    print(counter)
    print(endtime - startTime)
    return nextMove

def findMoveNegaMaxABv2(gs, validMoves, depth, alpha, beta, maximize):
    global nextMove, counter
    counter+=1
    if depth == 0 or gs.checkmate or gs.stalemate or len(validMoves) == 0:
        if depth == 0:
            return scoreBoard(gs)
        elif gs.checkmate:
            if gs.whiteTurn:
                return -CHECKMATE 
            else:
                return CHECKMATE
        
        elif gs.stalemate:
            return STALEMATE
        
    if maximize:
        maxScore = -CHECKMATE-1
        for move in validMoves:
            gs.movePiece(move)
            moves = gs.getValidMoves()
            score = findMoveNegaMaxABv2(gs, moves, depth-1, alpha, beta, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
                    print(move.moveId, maxScore)
            gs.undoMove()
            if score > beta:
                break
            alpha = max(alpha, maxScore)
        return maxScore
    else:
        maxScore = CHECKMATE+1
        
        for move in validMoves:
            gs.movePiece(move)
            moves = gs.getValidMoves()
            score = findMoveNegaMaxABv2(gs, moves, depth-1, alpha, beta, True)
            if score < maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
                    print(move.moveId, maxScore)
            gs.undoMove()
            if score < alpha:
                break
            beta = min(beta, maxScore)
        return maxScore

def scoreBoard(gs):
    if gs.checkmate:
        if gs.whiteTurn:
            return -CHECKMATE 
        else:
            return CHECKMATE
        
    elif gs.stalemate:
        return STALEMATE

    score = 0

    for r, c in gs.whitePieces:
        piece = gs.board[r][c]
        score += pieceScore[piece.identity[1]] + piecePositionScoreW[piece.identity[1]][r][c]
    
    for r, c in gs.blackPieces:
        piece = gs.board[r][c]
        score -= pieceScore[piece.identity[1]] + piecePositionScoreB[piece.identity[1]][r][c]

    #Old way of doing it
    # for row in range(8):
    #     for col in range(8):
    #         square = gs.board[row][col]
    #         if square != None:
    #             if square.colour == 'w':
    #                 score += pieceScore[square.identity[1]] + piecePositionScoreW[square.identity[1]][row][col]

    #             elif square.colour == 'b':
    #                 score -= pieceScore[square.identity[1]] + piecePositionScoreB[square.identity[1]][row][col]

    return score