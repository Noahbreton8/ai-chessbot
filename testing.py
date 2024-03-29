import pygame as game
from ChessEngine import GameState
import time

def moveGenerationTest(depth, gs):
    if depth == 0:
        return 1

    numPosition = 0
    
    moves = gs.getValidMoves()

    #for index, move in enumerate(moves):
        #print(f"{depth}:  {index}")
    for move in moves:
        gs.movePiece(move)
        added = moveGenerationTest(depth-1, gs)
        # if depth == 2:
        #     print(f"{move.getChessNotation()}: {added}")
        numPosition = numPosition + added
        gs.undoMove()

    return numPosition

#Tests taken from https://www.chessprogramming.org/Perft_Results
#Some of these tests will fail due to pawn promotion only promoting to a queen and not all 4 option
#Easily seen in test case 5

#Old comment under test case 1 to track progress
##Passes 1-6, 3 depth takes about 1.5 seconds, 4 depth takes about 40 seconds, 5 depth takes about 12 minutes, 6 depth takes about 7.5 hours
#
def main():
    while True:
        num = int(input("Select a test to run 1-6, 0 to exit: "))
        if num == 0:
            break
        depth = int(input("Select a depth to go to, <=3 recommended: "))
        match num:
            case 1: #Passes 1-6, depth 3 takes 0.8 seconds, depth 4 takes 17 seconds, depth 5 takes 14 minutes
                fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
                expected = [20, 400, 8902, 197281, 4865609, 119060324]
            case 2: #Passes 1-4, depth 3 takes 9 seconds
                fen = 'r3k2r/p1ppqpb1/bn2pnp1/3PN3/1p2P3/2N2Q1p/PPPBBPPP/R3K2R w KQkq -'
                expected = [48, 2039, 97862, 4085603]
            case 3: #Passes 1-5, depth 4 takes 5.5 seconds, depth 5 takes 75 seconds
                fen = '8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - -'
                expected = [14, 191, 2812, 43238, 674624]
            case 4: #Passes 1-4, 3 depth takes 0.85 seconds, 4 depth takes 44 seconds
                fen = 'r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1'
                expected = [6, 264, 9467, 422333]
            case 5: #Passes 1-4, 3 depth takes 6.5 seconds 4 depth takes 220 seconds
                fen = 'rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8'
                expected = [44, 1486, 62379, 2103487]
            case 6: #Passes 1-3, 3 depth takes 7 seconds
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

