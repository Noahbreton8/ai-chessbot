import pygame as game


HEIGHT = WIDTH = 800
SIZE = WIDTH, HEIGHT
DIMENTION = 8

def main():
    game.init()
    screen = game.display.set_mode(SIZE)
    screen.fill((255, 255, 255))

    gameOn = True
    while gameOn:
        for event in game.event.get():
            if event.type == game.QUIT:
                gameOn = False
        game.display.flip()
    game.quit()

main()