import random, time 

CHECKMATE = 100000
STALEMATE = 0
pieceScore = {"K": 0, "Q": 900, "R": 500, "B": 330, "N": 320, "P": 100}
DEPTH = 2

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
    #findMoveNegaMaxAB(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, 1 if gs.whiteTurn else -1)
    findMoveNegaMaxABv2(gs, validMoves, DEPTH, -CHECKMATE, CHECKMATE, True if gs.whiteTurn else False)
    endtime = time.time()
    print(counter)
    print(endtime - startTime)
    return nextMove


def findMoveNegaMaxAB(gs, validMoves, depth, alpha, beta, turnMultiplier):
    global nextMove, counter
    counter +=1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)

    #add move ordering -check captures
    maxScore = -CHECKMATE-1
    if len(validMoves) == 0:
        if gs.checkmate:
            if gs.whiteTurn:
                maxScore = -CHECKMATE 
            else:
                maxScore = CHECKMATE
            
        elif gs.stalemate:
            maxScore = STALEMATE

    for move in validMoves:
        gs.movePiece(move)
        nextMoves = gs.getAllValidMoves()
        score = -findMoveNegaMaxAB(gs, nextMoves, depth -1, beta, alpha, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
                print(move.moveId, maxScore)
        gs.undoMove()
        #prune
        if maxScore > alpha:
            alpha = maxScore

        if alpha >= beta:
            break

    return maxScore


def findMoveNegaMaxABv2(gs, validMoves, depth, alpha, beta, maximize):
    global nextMove
    if depth == 0 or gs.checkmate or gs.stalemate:
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
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.movePiece(move)
            moves = gs.getAllValidMoves()
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
        maxScore = CHECKMATE
        
        for move in validMoves:
            gs.movePiece(move)
            moves = gs.getAllValidMoves()
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
    for row in range(8):
        for col in range(8):
            square = gs.board[row][col]
            if square != None:
                if square.colour == 'w':
                    score += pieceScore[square.identity[1]] + piecePositionScoreW[square.identity[1]][row][col]

                elif square.colour == 'b':
                    score -= pieceScore[square.identity[1]] + piecePositionScoreB[square.identity[1]][row][col]

    return score


def makeBestMinMaxMove(gs, validMoves, depth, whiteTurn):
    global nextMove 
    if depth == 0:
        return scoreBoard(gs)
    
    if whiteTurn:
        maxScore = -CHECKMATE
        for move in validMoves:
            gs.movePiece(move)
            nextMoves = gs.getAllValidMoves()
            score = makeBestMinMaxMove(gs, nextMoves, depth -1, False)
            if score > maxScore:
                maxScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return maxScore
    
    else:
        minScore = CHECKMATE
        for move in validMoves:
            gs.movePiece(move)
            nextMoves = gs.getAllValidMoves()
            score = makeBestMinMaxMove(gs, nextMoves, depth -1, True)
            if score < minScore:
                minScore = score
                if depth == DEPTH:
                    nextMove = move
            gs.undoMove()
        return minScore
    
def findMoveNegaMax(gs, validMoves, depth, turnMultiplier):
    global nextMove, counter
    counter +=1
    if depth == 0:
        return turnMultiplier * scoreBoard(gs)
    
    maxScore = -CHECKMATE
    for move in validMoves:
        gs.movePiece(move)
        nextMoves = gs.getAllValidMoves()
        score = -findMoveNegaMax(gs, nextMoves, depth -1, -turnMultiplier)
        if score > maxScore:
            maxScore = score
            if depth == DEPTH:
                nextMove = move
        gs.undoMove()
    return maxScore

def makeBestMoveRandom(gs, validMoves):
    return validMoves[random.randint(0, len(validMoves)-1)]