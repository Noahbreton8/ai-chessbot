class Piece():
    def __init__(self, game, row, col, colour):
        self.row = row
        self.col = col
        self.image = game.transform.scale(game.image.load("images/"+colour+".png"), (100, 100))
    
    def draw(self, game, screen, size):
        screen.blit(self.image, game.Rect(self.col*size, self.row*size, size, size))