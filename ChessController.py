import pygame as game
from ChessEngine import GameState

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

    gameOn = True
    while gameOn:
        for event in game.event.get():
            if event.type == game.QUIT:
                gameOn = False
        game.display.flip()
    game.quit()

def drawBoard(screen, board):
    colours = ((204, 183, 174), (112,102,119))
    for file in range(DIMENTION):
        for rank in range(DIMENTION):
            #Drawing background colour
            colour = colours[(file+rank) %2]
            game.draw.rect(screen, colour, game.Rect(rank*SQUARE_SIZE, file*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            #pieces draw themselves
            if board[file][rank] != None:
                board[file][rank].draw(game, screen, SQUARE_SIZE)

    

main()