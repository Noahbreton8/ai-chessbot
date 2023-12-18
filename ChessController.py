import pygame as game
from ChessEngine import GameState
from ChessEngine import Move

HEIGHT = WIDTH = 800
SIZE = WIDTH, HEIGHT
DIMENTION = 8
SQUARE_SIZE = WIDTH/DIMENTION

def main():
    game.init()
    screen = game.display.set_mode(SIZE)
    screen.fill((255, 255, 255))

    gs = GameState(game)
    drawBoard(screen, gs.board)

    validMoves = gs.getAllValidMoves()
    moveMade = False #until valid move is made don't regenerate validMoves

    currSelection = () #keeps track of current choice
    playerMoves = [] #keeps track of at most 2 choices for moving pieces

    gameOn = True
    while gameOn:
        for event in game.event.get():
            if event.type == game.QUIT:
                gameOn = False
            
            #Selecting squares
            elif event.type == game.MOUSEBUTTONDOWN:
                x,y = game.mouse.get_pos()

                #Turns mouse position into rank and file
                col = int(x//SQUARE_SIZE)
                row = int(y//SQUARE_SIZE)

                #if we reselect a sqaure deselect it
                if currSelection == (row, col):
                    currSelection = ()
                    playerMoves = []

                else:
                    #if our first click is an empty square do nothing
                    if len(playerMoves) == 0 and gs.board[row][col] == None:
                        continue
                    
                    currSelection = (row, col)
                    playerMoves.append(currSelection)

                    #check if more than one click has been made
                    if len(playerMoves) == 2:
                        #check if second choice colour is same as first choice colour
                        if gs.board[playerMoves[1][0]][int(playerMoves[1][1])] and gs.board[playerMoves[0][0]][playerMoves[0][1]].colour == gs.board[playerMoves[1][0]][playerMoves[1][1]].colour:
                            playerMoves = playerMoves[1:] #remove the first move 

                        # second click is an opponent's piece or a empty square
                        else:
                            move = Move(playerMoves[0], playerMoves[1], gs.board)
                            print(move.getAlgebraicNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    #do check for pawn promotion for selection, add var for choice
                                    moveMade = True
                                    gs.movePiece(validMoves[i])
                                currSelection = []
                                playerMoves = []
                            if not moveMade:
                                currSelection = []
                                playerMoves = []
            
            elif event.type == game.KEYDOWN:
                if event.key == game.K_u:
                    gs.undoMove()
                    moveMade = True
        
        if moveMade:
            validMoves = gs.getAllValidMoves()
            moveMade = False
        
        drawBoard(screen, gs.board)
        game.display.flip()
    game.quit()

def drawBoard(screen, board):
    colours = ((204, 183, 174), (112,102,119)) #((light colour), (dark colour)) feel free to change it
    for row in range(DIMENTION):
        for col in range(DIMENTION):
            #Drawing background colour
            colour = colours[(col+row) %2]
            game.draw.rect(screen, colour, game.Rect(col*SQUARE_SIZE, row*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            #pieces draw themselves
            if board[row][col] != None:
                board[row][col].draw(game, screen, SQUARE_SIZE)

    

main()

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