import pygame as game
from ChessEngine import GameState
import time

def moveGenerationTest(depth, gs):
    if depth == 0:
        return 1

    numPosition = 0
    
    moves = gs.getAllValidMoves()

    for move in moves:
        gs.movePiece(move)
        numPosition = numPosition + moveGenerationTest(depth-1, gs)
        gs.undoMove()

    return numPosition

#Tests taken from https://www.chessprogramming.org/Perft_Results
#Some of these tests will fail due to pawn promotion only promoting to a queen and not all 4 option
#Easily seen in test case 5

def main():
    while True:
        num = int(input("Select a test to run 1-6, 0 to exit: "))
        if num == 0:
            break
        depth = int(input("Select a depth to go to, <=3 recommended: "))
        match num:
            case 1:
                fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
                expected = [20, 400, 8902, 197281, 4865609, 119060324]
            case 2:
                fen = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -'
                expected = [48, 2039, 97862, 4085603]
            case 3:
                fen = '8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - -'
                expected = [14, 191, 2812, 43238, 674624]
            case 4:
                fen = 'r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1'
                expected = [6, 264, 9467, 422333]
            case 5:
                fen = 'rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8'
                expected = [44, 1486, 62379, 2103487]
            case 6:
                fen = 'r4rk1/1pp1qppp/p1np1n2/2b1p1B1/2B1P1b1/P1NP1N2/1PP1QPPP/R4RK1 w - - 0 10 '
                expected = [46, 2079, 89890, 3894594]

        for i in range(depth):
            gs = GameState(game, fen)
            startTime = time.time()
            totalPositions = moveGenerationTest(i+1, gs)
            endTime = time.time()
            elapsedTime = endTime-startTime

            print(f"Depth: {i+1} Result: {totalPositions} positions Time: {elapsedTime} seconds")
            if totalPositions == expected[i]:
                print("SUCCESS")
            else:
                print(f"FAILURE, expected {expected[i]}")
                break
            print()

main()

